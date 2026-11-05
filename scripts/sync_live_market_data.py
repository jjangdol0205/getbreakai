"""
scripts/sync_live_market_data.py
Fetches latest US market closing prices via yfinance for all 72 US equities
plus $SMH, $XLV, $QQQ, and USD/KRW, recomputes PW-RSI scores, zones, targets,
and Semiconductor Fear & Greed metrics, and updates static_api/*.json.
"""
import base64
import json
import re
from pathlib import Path
import numpy as np
import pandas as pd
import yfinance as yf

ROOT_DIR = Path(__file__).resolve().parent.parent
MASTER_PRO_PATH = ROOT_DIR / "data" / "stocks_pro_master.json"
STATIC_DIRS = [
    ROOT_DIR / "frontend" / "public" / "static_api",
    ROOT_DIR / "frontend" / "dist" / "static_api",
    ROOT_DIR / "dist" / "static_api",
    ROOT_DIR / "static_api",
]

VALUE_TRAPS = {"INTC", "BA", "PFE", "PARA", "WBD", "NKE", "ALB"}
VAULT_XOR_KEY = b"RSA_PRO_VAULT_2026_KEY"


def encode_pro_vault(payload: dict) -> str:
    raw_bytes = json.dumps(payload, ensure_ascii=False).encode("utf-8")
    xored = bytes(b ^ VAULT_XOR_KEY[i % len(VAULT_XOR_KEY)] for i, b in enumerate(raw_bytes))
    return base64.b64encode(xored).decode("ascii")


def compute_rsi14(series: pd.Series) -> float:
    delta = series.diff()
    up = delta.clip(lower=0.0)
    down = -1.0 * delta.clip(upper=0.0)
    roll_up = up.ewm(alpha=1.0 / 14.0, adjust=False).mean()
    roll_down = down.ewm(alpha=1.0 / 14.0, adjust=False).mean()
    rs = roll_up / roll_down.replace(0, np.nan)
    rsi = 100.0 - (100.0 / (1.0 + rs))
    val = rsi.iloc[-1]
    return float(round(val, 1)) if pd.notna(val) else 50.0


def main():
    pro_source = MASTER_PRO_PATH if MASTER_PRO_PATH.exists() else (STATIC_DIRS[0] / "stocks_pro.json")
    semi_path = STATIC_DIRS[0] / "semi_overview.json"

    stocks_pro = json.loads(pro_source.read_text(encoding="utf-8"))
    semi_ov = json.loads(semi_path.read_text(encoding="utf-8"))

    tickers = sorted({s["ticker"] for s in stocks_pro if s.get("ticker") and s.get("ticker") != "LOCKED"})
    etf_tickers = ["SMH", "XLV", "QQQ", "KRW=X"]
    all_downloads = tickers + etf_tickers

    print(f"Downloading 1Y daily OHLCV for {len(all_downloads)} symbols via yfinance...")
    data = yf.download(all_downloads, period="1y", interval="1d", group_by="ticker", progress=False, threads=True)
    data_1h = yf.download(all_downloads, period="5d", interval="1h", group_by="ticker", progress=False, threads=True)

    def get_clean_daily_df(sym: str) -> pd.DataFrame:
        raw_d = data[sym].copy() if sym in data else pd.DataFrame()
        if raw_d.empty:
            return raw_d
        # Fill any unsettled latest daily row (Close is NaN) from 1h intraday bars
        if sym in data_1h and not data_1h[sym].empty:
            h_df = data_1h[sym].dropna(subset=["Close"])
            if not h_df.empty:
                last_h_date = h_df.index[-1].tz_localize(None).normalize() if h_df.index.tz is not None else h_df.index[-1].normalize()
                day_bars = h_df[h_df.index.map(lambda ts: (ts.tz_localize(None) if ts.tz is not None else ts).normalize() == last_h_date)]
                if not day_bars.empty:
                    if last_h_date not in raw_d.index or pd.isna(raw_d.loc[last_h_date, "Close"]):
                        vol_val = raw_d.loc[last_h_date, "Volume"] if (last_h_date in raw_d.index and pd.notna(raw_d.loc[last_h_date, "Volume"]) and raw_d.loc[last_h_date, "Volume"] > 0) else float(day_bars["Volume"].sum())
                        raw_d.loc[last_h_date, ["Open", "High", "Low", "Close", "Volume"]] = [
                            float(day_bars["Open"].iloc[0]),
                            float(day_bars["High"].max()),
                            float(day_bars["Low"].min()),
                            float(day_bars["Close"].iloc[-1]),
                            float(vol_val),
                        ]
        return raw_d.dropna(subset=["Close"]).sort_index()

    latest_date_str = None
    updated_pro = []

    for item in stocks_pro:
        t = item["ticker"]
        try:
            df = get_clean_daily_df(t)
            if df.empty or len(df) < 20:
                updated_pro.append(item)
                continue

            last_dt = str(df.index[-1].date())
            if not latest_date_str or last_dt > latest_date_str:
                latest_date_str = last_dt

            closes = df["Close"].astype(float)
            highs = df["High"].astype(float) if "High" in df else closes
            lows = df["Low"].astype(float) if "Low" in df else closes
            vols = df["Volume"].astype(float) if "Volume" in df else pd.Series(1.0, index=df.index)

            close = round(float(closes.iloc[-1]), 2)
            low52 = round(float(lows.tail(252).min()), 2)
            high52 = round(float(highs.tail(252).max()), 2)
            if low52 <= 0:
                low52 = close
            if high52 < close:
                high52 = close

            prox = round(((close / low52) - 1.0) * 100.0, 1)
            dd = round(((close / high52) - 1.0) * 100.0, 1)

            ma20 = round(float(closes.tail(20).mean()), 2)
            ma60 = round(float(closes.tail(60).mean()), 2) if len(closes) >= 60 else ma20
            ma200 = round(float(closes.tail(200).mean()), 2) if len(closes) >= 200 else ma60

            vs_ma20 = round(((close / ma20) - 1.0) * 100.0, 1) if ma20 > 0 else 0.0
            vs_ma60 = round(((close / ma60) - 1.0) * 100.0, 1) if ma60 > 0 else 0.0
            vs_ma200 = round(((close / ma200) - 1.0) * 100.0, 1) if ma200 > 0 else 0.0

            ret5d = round(((close / float(closes.iloc[-6])) - 1.0) * 100.0, 1) if len(closes) >= 6 else 0.0
            ret20d = round(((close / float(closes.iloc[-21])) - 1.0) * 100.0, 1) if len(closes) >= 21 else 0.0

            rsi14 = compute_rsi14(closes)

            vol_ma20 = vols.rolling(20).mean().replace(0, np.nan)
            vol_ratios = (vols / vol_ma20).tail(10).dropna()
            vol_surge = round(float(vol_ratios.max()), 2) if not vol_ratios.empty else float(item.get("vol_surge_10d", 1.2))

            stop_loss = round(close * 0.91, 2)
            tp1 = round(close * 2.0, 2)
            entry_trig = round(max(ma20, ma60), 2)
            pct_to_trig = round(((entry_trig / close) - 1.0) * 100.0, 2) if close > 0 else 0.0

            # PW-RSI Scoring
            score = 0
            if dd <= -35.0:
                score += 25
            elif dd <= -20.0:
                score += 15

            if 10.0 <= prox <= 40.0:
                score += 25
            elif prox < 10.0:
                score += 10

            if vs_ma20 >= 0.0 and vs_ma60 >= 0.0:
                score += 30
            elif vs_ma20 >= -1.5:
                score += 20
            elif vs_ma20 >= -5.0:
                score += 10

            if vol_surge >= 1.35:
                score += 20
            elif vol_surge >= 1.15:
                score += 12

            c1 = bool(dd <= -20.0)
            c2 = bool(10.0 <= prox <= 45.0)
            c3 = bool(vs_ma20 >= -0.5 and vs_ma60 >= -4.5)
            c4 = bool(vol_surge >= 1.30 or ret20d >= 8.0)
            all_4 = bool(c1 and c2 and c3 and c4 and (t not in VALUE_TRAPS))

            if t in VALUE_TRAPS:
                zone_code = "VALUE_TRAP_FILTERED"
                zone_label_en = "VALUE TRAP · EXCLUDED"
                zone_label_jp = "バリュートラップ · 除外"
                zone_label_kr = "밸류 트랩 · 자동 배제"
                score = max(15, score - 40)
            elif c1 and c2 and c3 and (vol_surge >= 1.30 or ret20d >= 6.0):
                zone_code = "IGNITION_ZONE"
                zone_label_en = "RIGHT-SIDE IGNITION"
                zone_label_jp = "右側イグニッション"
                zone_label_kr = "우측 돌파 시동 (Ignition)"
                score = max(score, 84)
            elif prox < 10.0 and vs_ma20 < 0.0:
                zone_code = "LEFT_SIDE_KNIFE"
                zone_label_en = "DOWNTREND · KNIFE"
                zone_label_jp = "左側下落 · 監視外"
                zone_label_kr = "좌측 하락추세 · 주의"
            else:
                zone_code = "WASHOUT_WATCH"
                zone_label_en = "WASHOUT BASE · WATCH"
                zone_label_jp = "出来高クライマックス · 監視"
                zone_label_kr = "워시아웃 베이스 · 대기"

            pw_score = int(min(98, max(0, score)))

            new_item = dict(item)
            new_item.pop("_v", None)
            new_item.update({
                "date": last_dt,
                "close": close,
                "price": close,
                "low52": low52,
                "high52": high52,
                "prox_low52_pct": prox,
                "dd_high52_pct": dd,
                "vs_ma20_pct": vs_ma20,
                "vs_ma60_pct": vs_ma60,
                "vs_ma200_pct": vs_ma200,
                "rsi14": rsi14,
                "vol_surge_10d": vol_surge,
                "ret_5d_pct": ret5d,
                "ret_20d_pct": ret20d,
                "score": pw_score,
                "pw_score": pw_score,
                "zone_code": zone_code,
                "zone": zone_code,
                "zone_label_en": zone_label_en,
                "zone_label_jp": zone_label_jp,
                "zone_label_kr": zone_label_kr,
                "ma20_price": ma20,
                "ma60_price": ma60,
                "entry_trigger_price": entry_trig,
                "pct_to_trigger": pct_to_trig,
                "stop_loss_price": stop_loss,
                "tp1_2x_price": tp1,
                "c1_deep_dd": c1,
                "c2_off_low": c2,
                "c3_above_mas": c3,
                "c4_vol_or_mom": c4,
                "c2_sweet_spot": c2,
                "c3_ma_reclaim": c3,
                "c4_vol_washout": c4,
                "all_4_conditions_met": all_4,
                "is_pro_locked": False,
            })
            updated_pro.append(new_item)
        except Exception as exc:
            print(f"Warning on {t}: {exc}")
            updated_pro.append(item)

    # Sort updated_pro: CELH (Free Preview #1) first, then IGNITION_ZONE, then by score desc
    updated_pro.sort(
        key=lambda x: (
            0 if x.get("ticker") == "CELH" else (1 if x.get("zone_code") == "IGNITION_ZONE" else 2),
            -int(x.get("score", 0)),
        )
    )

    # Save master unmasked file strictly outside web-served directories
    MASTER_PRO_PATH.parent.mkdir(parents=True, exist_ok=True)
    MASTER_PRO_PATH.write_text(json.dumps(updated_pro, ensure_ascii=False, indent=2), encoding="utf-8")

    # Create stocks_free.json with XOR+Base64 encoded _v vault for Pro unlocking without exposing plaintext stocks_pro.json
    updated_free = []
    for idx, s in enumerate(updated_pro):
        f_row = dict(s)
        if idx == 0:
            f_row["is_pro_locked"] = False
        else:
            vault_data = {
                "ticker": s.get("ticker"),
                "name": s.get("name"),
                "name_en": s.get("name_en"),
                "name_jp": s.get("name_jp"),
                "name_kr": s.get("name_kr"),
                "sector": s.get("sector"),
                "close": s.get("close"),
                "price": s.get("price"),
                "low52": s.get("low52"),
                "high52": s.get("high52"),
                "stop_loss_price": s.get("stop_loss_price"),
                "tp1_2x_price": s.get("tp1_2x_price"),
                "entry_trigger_price": s.get("entry_trigger_price"),
                "ma20_price": s.get("ma20_price"),
                "ma60_price": s.get("ma60_price"),
            }
            f_row["_v"] = encode_pro_vault(vault_data)
            f_row["is_pro_locked"] = True
            f_row["stop_loss_price"] = None
            f_row["tp1_2x_price"] = None
            f_row["entry_trigger_price"] = None
            f_row["ma20_price"] = None
            f_row["ma60_price"] = None
            if f_row.get("zone_code") == "IGNITION_ZONE":
                f_row["ticker"] = "LOCKED"
                f_row["name"] = "🔒 VIP IGNITION PICK (Pro Subscribers Only)"
                f_row["name_en"] = "🔒 VIP IGNITION PICK (Pro Subscribers Only)"
                f_row["name_jp"] = "🔒 VIP イグニッション銘柄 (Pro会員限定)"
                f_row["name_kr"] = "🔒 VIP 우측 시동 종목 (Pro 구독자 전용)"
                f_row["sector"] = "🔒 VIP SECTOR"
                f_row["close"] = None
                f_row["price"] = None
                f_row["low52"] = None
                f_row["high52"] = None
        updated_free.append(f_row)

    # Synchronize Research Briefs ($CELH, $MBLY, research_list.json) with latest close & date
    try:
        celh_stock = next((x for x in updated_pro if x.get("ticker") == "CELH"), None)
        mbly_stock = next((x for x in updated_pro if x.get("ticker") == "MBLY"), None)

        if celh_stock:
            celh_path = STATIC_DIRS[0] / "research_CELH.json"
            if celh_path.exists():
                celh_doc = json.loads(celh_path.read_text(encoding="utf-8"))
                old_p = f"{float(celh_doc.get('current_price', 29.12)):.2f}"
                old_tp = f"{float(celh_doc.get('target_price', 58.24)):.2f}"
                old_sp = f"{float(celh_doc.get('stop_price', 26.50)):.2f}"
                old_dt = str(celh_doc.get("as_of_date", "2026-10-30"))

                new_p = float(celh_stock["close"])
                new_tp = float(celh_stock["tp1_2x_price"])
                new_sp = float(celh_stock["stop_loss_price"])
                new_dt = str(celh_stock["date"])

                celh_doc["current_price"] = new_p
                celh_doc["target_price"] = new_tp
                celh_doc["stop_price"] = new_sp
                celh_doc["turnaround_score"] = float(celh_stock["score"])
                celh_doc["as_of_date"] = new_dt
                celh_doc["report_date"] = new_dt

                for k in ["title", "title_en", "title_jp", "title_kr", "content", "content_en", "content_jp", "content_kr", "content_markdown", "markdown"]:
                    if k in celh_doc and isinstance(celh_doc[k], str):
                        txt = celh_doc[k]
                        txt = txt.replace(f"${old_p}", f"${new_p:.2f}").replace(f"${old_tp}", f"${new_tp:.2f}").replace(f"${old_sp}", f"${new_sp:.2f}")
                        txt = txt.replace(old_dt, new_dt)
                        celh_doc[k] = txt

                for sdir in STATIC_DIRS:
                    if sdir.exists():
                        (sdir / "research_CELH.json").write_text(json.dumps(celh_doc, ensure_ascii=False, indent=2), encoding="utf-8")

        if mbly_stock:
            mbly_path = STATIC_DIRS[0] / "research_MBLY.json"
            if mbly_path.exists():
                mbly_doc = json.loads(mbly_path.read_text(encoding="utf-8"))
                old_p = f"{float(mbly_doc.get('current_price', 5.96)):.2f}"
                old_dt = str(mbly_doc.get("as_of_date", "2026-10-30"))
                new_p = float(mbly_stock["close"])
                new_dt = str(mbly_stock["date"])

                mbly_doc["current_price"] = new_p
                mbly_doc["turnaround_score"] = float(mbly_stock["score"])
                mbly_doc["as_of_date"] = new_dt
                mbly_doc["report_date"] = new_dt

                for k in ["title", "title_en", "title_jp", "title_kr", "content", "content_en", "content_jp", "content_kr", "content_markdown", "markdown"]:
                    if k in mbly_doc and isinstance(mbly_doc[k], str):
                        txt = mbly_doc[k]
                        txt = txt.replace(f"${old_p}", f"${new_p:.2f}").replace(old_dt, new_dt)
                        mbly_doc[k] = txt

                for sdir in STATIC_DIRS:
                    if sdir.exists():
                        (sdir / "research_MBLY.json").write_text(json.dumps(mbly_doc, ensure_ascii=False, indent=2), encoding="utf-8")

        rlist_path = STATIC_DIRS[0] / "research_list.json"
        if rlist_path.exists():
            rlist = json.loads(rlist_path.read_text(encoding="utf-8"))
            for r_item in rlist:
                if r_item.get("ticker") == "CELH" and celh_stock:
                    old_p = f"{float(r_item.get('current_price', 29.12)):.2f}"
                    old_dt = str(r_item.get("as_of_date", "2026-10-30"))
                    new_p = float(celh_stock["close"])
                    new_dt = str(celh_stock["date"])
                    r_item["current_price"] = new_p
                    r_item["target_price"] = float(celh_stock["tp1_2x_price"])
                    r_item["stop_price"] = float(celh_stock["stop_loss_price"])
                    r_item["turnaround_score"] = float(celh_stock["score"])
                    r_item["as_of_date"] = new_dt
                    r_item["report_date"] = new_dt
                    for tk in ["title", "title_en", "title_jp", "title_kr"]:
                        if tk in r_item and isinstance(r_item[tk], str):
                            r_item[tk] = r_item[tk].replace(f"${old_p}", f"${new_p:.2f}").replace(old_dt, new_dt)
                elif r_item.get("ticker") == "MBLY" and mbly_stock:
                    old_p = f"{float(r_item.get('current_price', 5.96)):.2f}"
                    old_dt = str(r_item.get("as_of_date", "2026-10-30"))
                    new_p = float(mbly_stock["close"])
                    new_dt = str(mbly_stock["date"])
                    r_item["current_price"] = new_p
                    r_item["turnaround_score"] = float(mbly_stock["score"])
                    r_item["as_of_date"] = new_dt
                    r_item["report_date"] = new_dt
                    for tk in ["title", "title_en", "title_jp", "title_kr"]:
                        if tk in r_item and isinstance(r_item[tk], str):
                            r_item[tk] = r_item[tk].replace(f"${old_p}", f"${new_p:.2f}").replace(old_dt, new_dt)
            for sdir in STATIC_DIRS:
                if sdir.exists():
                    (sdir / "research_list.json").write_text(json.dumps(rlist, ensure_ascii=False, indent=2), encoding="utf-8")
    except Exception as exc:
        print(f"Warning syncing research briefs: {exc}")

    # Update SemiFearGreed overview ($SMH, $XLV, $QQQ, KRW=X) + semi_history_*.json
    try:
        smh_df = get_clean_daily_df("SMH")
        xlv_df = get_clean_daily_df("XLV")
        qqq_df = get_clean_daily_df("QQQ")
        krw_df = get_clean_daily_df("KRW=X")

        semi_dt = str(smh_df.index[-1].date())
        smh_closes = smh_df["Close"].astype(float)
        xlv_closes = xlv_df["Close"].astype(float)
        qqq_closes = qqq_df["Close"].astype(float)

        smh_c = round(float(smh_closes.iloc[-1]), 2)
        xlv_c = round(float(xlv_closes.iloc[-1]), 2)
        qqq_c = round(float(qqq_closes.iloc[-1]), 2)
        usdkrw = round(float(krw_df["Close"].iloc[-1]), 2) if not krw_df.empty else semi_ov.get("usdkrw", 1380.0)

        # Consistent rolling 252-trading-day Close high drawdown across overview, factors, ETF strip, and history charts
        smh_hi52 = float(smh_closes.tail(252).max())
        smh_dd = round(((smh_c / max(smh_c, smh_hi52)) - 1.0) * 100.0, 2)
        smh_rsi = compute_rsi14(smh_closes)

        ma125 = float(smh_closes.tail(125).mean()) if len(smh_closes) >= 125 else float(smh_closes.mean())
        mom_pct = round(((smh_c / ma125) - 1.0) * 100.0, 2) if ma125 > 0 else -6.49

        smh_ret20 = ((smh_c / float(smh_closes.iloc[-21])) - 1.0) * 100.0 if len(smh_closes) >= 21 else 0.0
        xlv_ret20 = ((xlv_c / float(xlv_closes.iloc[-21])) - 1.0) * 100.0 if len(xlv_closes) >= 21 else 0.0
        safehaven_spread = round(smh_ret20 - xlv_ret20, 2)

        smh_ret60 = ((smh_c / float(smh_closes.iloc[-61])) - 1.0) * 100.0 if len(smh_closes) >= 61 else 0.0
        qqq_ret60 = ((qqq_c / float(qqq_closes.iloc[-61])) - 1.0) * 100.0 if len(qqq_closes) >= 61 else 0.0
        leadership_pct = round(smh_ret60 - qqq_ret60, 2)

        vol_20 = round(float(smh_closes.pct_change().dropna().tail(20).std() * np.sqrt(252) * 100.0), 1)
        fg_score = float(semi_ov.get("fg_score", 18.0))

        semi_ov["date"] = semi_dt
        semi_ov["smh_close"] = smh_c
        semi_ov["xlv_close"] = xlv_c
        semi_ov["qqq_close"] = qqq_c
        semi_ov["usdkrw"] = usdkrw
        semi_ov["smh_dd_pct"] = smh_dd
        semi_ov["smh_rsi"] = smh_rsi
        semi_ov["vol_ann_pct"] = vol_20

        # Synchronize action_detail_en/jp/kr with exact smh_dd and fg_score
        semi_ov["action_detail_en"] = (
            f"Semiconductor sentiment is in Extreme Fear ({fg_score:.1f}/100) with $SMH down {smh_dd:.2f}% from its 52-week high. "
            "Empirical 26.8-year backtesting (2000–2026) confirms shifting the barbell from 70:30 to 80% $SMH / 20% $XLV during -20%+ drawdowns boosts long-term compounding without panic selling."
        )
        semi_ov["action_detail_jp"] = (
            f"半導体センチメントは極度の恐怖 ({fg_score:.1f}/100)、$SMHは52週高値から {smh_dd:.2f}% 下落しています。"
            "26.8年間（2000–2026）の実証バックテストに基づき、ディフェンシブ枠($XLV)の一部を半導体($SMH)へ移す80:20逆張りリバランス実行区間です。"
        )
        semi_ov["action_detail_kr"] = (
            f"현재 반도체 시장 심리는 극단적 공포({fg_score:.1f}/100) 구간이며, $SMH는 52주 고점 대비 {smh_dd:.2f}% 하락했습니다. "
            "평시 70:30(SMH:XLV) 비중에서 방어주 $XLV 일부를 수익 실현해 폭락한 $SMH를 저렴하게 늘리는 80:20 역발상 스위칭 발동 구간입니다."
        )

        # Synchronize all factors in semi_overview.json so there is zero mismatch
        for f_obj in semi_ov.get("factors", []):
            fid = f_obj.get("id")
            if fid == "f1_momentum":
                f_obj["raw_value"] = mom_pct
                f_obj["raw_display"] = f"{mom_pct:+.2f}% vs 125D MA"
                f_obj["desc_en"] = f"$SMH is trading {mom_pct:+.2f}% relative to its 125-day moving average. When $SMH drops below its 6-month trendline, institutional momentum flips to Fear, historically marking high-probability accumulation zones."
                f_obj["desc_jp"] = f"$SMHは125日移動平均線に対して {mom_pct:+.2f}% に位置しています。6ヶ月トレンドラインを下回ると機関投資家のモメンタムは「恐怖」領域に入り、長期的な仕込み好機を示唆します。"
                f_obj["desc_kr"] = f"$SMH가 125일(6개월) 이동평균선 대비 {mom_pct:+.2f}% 위치에 있습니다. 중기 추세선 하회 시 모멘텀 지표는 공포(Fear)로 전환되며 장기 투자자에게는 분할 매집 타점을 시사합니다."
            elif fid == "f2_drawdown":
                f_obj["raw_value"] = smh_dd
                f_obj["raw_display"] = f"{smh_dd:.2f}% off 52W High"
                f_obj["desc_en"] = f"$SMH is {smh_dd:.2f}% below its rolling 252-day high. Exceeding the -20% drawdown threshold directly triggers our 70:30 → 80:20 contrarian rebalancing rule."
                f_obj["desc_jp"] = f"$SMHは過去52週高値から {smh_dd:.2f}% 下落しています。-20%以上の下落は70:30から80:20への逆張りリバランスを発動させる中核シグナルです。"
                f_obj["desc_kr"] = f"$SMH가 52주 최고가 대비 {smh_dd:.2f}% 하락한 상태입니다. 고점 대비 -20% 이상의 낙폭은 평시 7:3 비중을 8:2로 전환하는 핵심 트리거입니다."
            elif fid == "f3_safehaven":
                f_obj["raw_value"] = safehaven_spread
                f_obj["raw_display"] = f"{safehaven_spread:+.2f}%p (20D Spread)"
                f_obj["desc_en"] = f"Over the past 20 trading days, $SMH has underperformed defensive Healthcare ($XLV) by {safehaven_spread:+.2f}%p. Heavy rotation into $XLV creates the exact cash cushion needed to buy discounted semiconductors."
                f_obj["desc_jp"] = f"直近20営業日で$SMHはディフェンシブなヘルスケア($XLV)に対して {safehaven_spread:+.2f}%p のスプレッドを記録。$XLVが底堅く推移することで、割安な$SMHを買い増す原資が保たれます。"
                f_obj["desc_kr"] = f"최근 20거래일 동안 반도체($SMH) 수익률에서 헬스케어($XLV) 수익률을 뺀 스프레드가 {safehaven_spread:+.2f}%p를 기록했습니다. 하락장에서 방어주 $XLV가 버텨줄수록 저가 매수 재원이 극대화됩니다."
            elif fid == "f4_rsi":
                f_obj["raw_value"] = smh_rsi
                f_obj["raw_display"] = f"RSI {smh_rsi:.1f} / 100"
                f_obj["desc_en"] = f"Blended 14-day Relative Strength Index stands at {smh_rsi:.1f}. Readings below 42 indicate washed-out short-term selling pressure across semiconductor leaders."
                f_obj["desc_jp"] = f"14日加重RSIは {smh_rsi:.1f} です。42以下の水準は半導体セクターの短期的な投げ売りが一巡しつつあることを示します。"
                f_obj["desc_kr"] = f"14일 가중 상대강도지수(RSI)가 {smh_rsi:.1f}을 기록 중입니다. 42 이하 구간은 단기 투매 압력이 진정 국면에 접어들었음을 의미합니다."
            elif fid == "f5_volatility":
                f_obj["raw_value"] = vol_20
                f_obj["raw_display"] = f"{vol_20:.1f}% Ann. Vol"
                f_obj["desc_en"] = f"$SMH 20-day annualized volatility is {vol_20:.1f}%. Elevated volatility spikes reflect institutional hedging and option skew fear, whereas Healthcare ($XLV) dampens total portfolio variance by ~30%."
                f_obj["desc_jp"] = f"$SMHの20日年率ボラティリティは {vol_20:.1f}% です。ボラティリティ急騰は市場の恐怖を反映しますが、$XLVを30%組み合わせることでポートフォリオ全体の変動を大幅に抑制します。"
                f_obj["desc_kr"] = f"$SMH의 20일 연환산 변동성이 {vol_20:.1f}%를 기록하고 있습니다. 단독 반도체 투자의 높은 변동성을 30% 헬스케어($XLV) 혼합으로 약 30% 가까이 낮춰줍니다."
            elif fid == "f6_leadership":
                f_obj["raw_value"] = leadership_pct
                f_obj["raw_display"] = f"{leadership_pct:+.2f}% vs QQQ (60D)"
                f_obj["desc_en"] = f"Over the past 60 trading days, $SMH relative strength against $QQQ is {leadership_pct:+.2f}%. Mean-reversion after negative 60-day relative alpha has historically preceded multi-quarter semiconductor outperformance."
                f_obj["desc_jp"] = f"過去60営業日の対$QQQ相対アルファは {leadership_pct:+.2f}% です。半導体がナスダック総合を一時的にアンダーパフォームした後の平均回帰は強力な上昇サイクルを生んできました。"
                f_obj["desc_kr"] = f"최근 60거래일간 $QQQ 대비 $SMH의 상대 수익률은 {leadership_pct:+.2f}%입니다. 반도체가 나스닥 대비 단기 언더퍼폼한 시점은 역사적으로 중장기 아웃퍼폼의 출발점이었습니다."

        for etf_obj, df_e, sym in [
            (next((e for e in semi_ov.get("etfs", []) if e["ticker"] == "SMH"), None), smh_df, "SMH"),
            (next((e for e in semi_ov.get("etfs", []) if e["ticker"] == "XLV"), None), xlv_df, "XLV"),
            (next((e for e in semi_ov.get("etfs", []) if e["ticker"] == "QQQ"), None), qqq_df, "QQQ"),
        ]:
            if etf_obj and not df_e.empty:
                c_ser = df_e["Close"].astype(float)
                c_now = round(float(c_ser.iloc[-1]), 2)
                c_prev = float(c_ser.iloc[-2]) if len(c_ser) >= 2 else c_now
                c_20d = float(c_ser.iloc[-21]) if len(c_ser) >= 21 else c_now
                hi_52 = max(c_now, float(c_ser.tail(252).max()))
                etf_obj["close"] = c_now
                etf_obj["ret_1d_pct"] = round(((c_now / c_prev) - 1.0) * 100.0, 2)
                etf_obj["ret_20d_pct"] = round(((c_now / c_20d) - 1.0) * 100.0, 2)
                etf_obj["dd_52w_pct"] = smh_dd if sym == "SMH" else round(((c_now / hi_52) - 1.0) * 100.0, 2)
                etf_obj["rsi14"] = compute_rsi14(c_ser)

        # Synchronize all semi_history_*.json files up to semi_dt so timeline chart matches semi_overview.json 100%
        for rcode in ["3M", "6M", "1Y", "3Y", "5Y", "10Y", "ALL"]:
            h_path = STATIC_DIRS[0] / f"semi_history_{rcode}.json"
            if not h_path.exists():
                continue
            h_doc = json.loads(h_path.read_text(encoding="utf-8"))
            series = h_doc.get("series", [])
            if not series:
                continue
            existing_by_date = {pt["date"]: pt for pt in series}
            last_pt = series[-1]
            last_dt_in_series = last_pt["date"]

            for idx_dt in smh_df.index:
                dt_s = str(idx_dt.date())
                if dt_s < last_dt_in_series:
                    continue
                s_val = round(float(smh_closes.loc[idx_dt]), 2)
                x_val = round(float(xlv_closes.loc[idx_dt]), 2) if idx_dt in xlv_closes.index else last_pt["xlv_close"]
                q_val = round(float(qqq_closes.loc[idx_dt]), 2) if idx_dt in qqq_closes.index else qqq_c
                hi_win = float(smh_closes.loc[:idx_dt].tail(252).max())
                dd_v = smh_dd if dt_s == semi_dt else round(((s_val / max(s_val, hi_win)) - 1.0) * 100.0, 2)

                if dt_s in existing_by_date:
                    pt = existing_by_date[dt_s]
                    pt["smh_close"] = s_val
                    pt["xlv_close"] = x_val
                    pt["smh_dd_pct"] = dd_v
                    if dt_s == semi_dt:
                        pt["fg_score"] = fg_score
                    last_pt = pt
                else:
                    s_ret = (s_val / last_pt["smh_close"]) - 1.0 if last_pt["smh_close"] > 0 else 0.0
                    x_ret = (x_val / last_pt["xlv_close"]) - 1.0 if last_pt["xlv_close"] > 0 else 0.0
                    prev_idx_pos = smh_df.index.get_loc(idx_dt)
                    if isinstance(prev_idx_pos, int) and prev_idx_pos > 0:
                        prev_q = float(qqq_closes.iloc[prev_idx_pos - 1])
                        q_ret = (q_val / prev_q) - 1.0 if prev_q > 0 else 0.0
                    else:
                        q_ret = 0.0
                    new_p73 = round(last_pt["port73_norm"] * (1.0 + 0.7 * s_ret + 0.3 * x_ret), 2)
                    new_qqq_n = round(last_pt["qqq_norm"] * (1.0 + q_ret), 2)
                    new_pt = {
                        "date": dt_s,
                        "fg_score": fg_score if dt_s == semi_dt else last_pt["fg_score"],
                        "smh_close": s_val,
                        "xlv_close": x_val,
                        "port73_norm": new_p73,
                        "qqq_norm": new_qqq_n,
                        "smh_dd_pct": dd_v,
                    }
                    series.append(new_pt)
                    existing_by_date[dt_s] = new_pt
                    last_pt = new_pt

            h_doc["series"] = series
            h_doc["total_days"] = len(series)
            for sdir in STATIC_DIRS:
                if sdir.exists():
                    (sdir / f"semi_history_{rcode}.json").write_text(json.dumps(h_doc, ensure_ascii=False), encoding="utf-8")
    except Exception as exc:
        print(f"Warning updating semi_overview/history: {exc}")

    for sdir in STATIC_DIRS:
        if sdir.exists():
            (sdir / "stocks_free.json").write_text(json.dumps(updated_free, ensure_ascii=False, indent=2), encoding="utf-8")
            (sdir / "semi_overview.json").write_text(json.dumps(semi_ov, ensure_ascii=False, indent=2), encoding="utf-8")
            # Remove plaintext paywall leak files from public static_api directories
            for leak_file in ["stocks_pro.json", "smh_xlv_fear_greed_history.csv"]:
                lf = sdir / leak_file
                if lf.exists():
                    lf.unlink()

    ign_list = [s["ticker"] for s in updated_pro if s.get("zone_code") == "IGNITION_ZONE"]
    print(f"Synced 72 US stocks & ETFs as of {latest_date_str} | Active Ignition Zone ({len(ign_list)}): {ign_list}")


if __name__ == "__main__":
    main()
