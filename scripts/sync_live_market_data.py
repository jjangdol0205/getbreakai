"""
scripts/sync_live_market_data.py
Fetches latest US market closing prices via yfinance for all 72 US equities
plus $SMH, $XLV, $QQQ, and USD/KRW, recomputes PW-RSI scores, zones, targets,
and Semiconductor Fear & Greed metrics, and updates static_api/*.json.
"""
import json
from pathlib import Path
import numpy as np
import pandas as pd
import yfinance as yf

ROOT_DIR = Path(__file__).resolve().parent.parent
STATIC_DIRS = [
    ROOT_DIR / "frontend" / "public" / "static_api",
    ROOT_DIR / "dist" / "static_api",
    ROOT_DIR / "static_api",
]

VALUE_TRAPS = {"INTC", "BA", "PFE", "PARA", "WBD", "NKE", "ALB"}


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
    pro_path = STATIC_DIRS[0] / "stocks_pro.json"
    semi_path = STATIC_DIRS[0] / "semi_overview.json"

    stocks_pro = json.loads(pro_path.read_text(encoding="utf-8"))
    semi_ov = json.loads(semi_path.read_text(encoding="utf-8"))

    tickers = sorted({s["ticker"] for s in stocks_pro if s.get("ticker")})
    etf_tickers = ["SMH", "XLV", "QQQ", "KRW=X"]
    all_Downloads = tickers + etf_tickers

    print(f"Downloading 1Y daily OHLCV for {len(all_Downloads)} symbols via yfinance...")
    data = yf.download(all_Downloads, period="1y", interval="1d", group_by="ticker", progress=False, threads=True)

    latest_date_str = None
    updated_pro = []

    for item in stocks_pro:
        t = item["ticker"]
        try:
            df = data[t].dropna(subset=["Close"])
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

    # Sort updated_pro: IGNITION_ZONE first, then by score desc
    updated_pro.sort(key=lambda x: (0 if x.get("zone_code") == "IGNITION_ZONE" else 1, -int(x.get("score", 0))))

    # Create stocks_free.json: Only 1 showcase ticker (first row / CELH) is unlocked; all other 71 rows require Pro!
    updated_free = []
    for idx, s in enumerate(updated_pro):
        f_row = dict(s)
        if idx == 0:
            f_row["is_pro_locked"] = False
        else:
            f_row["is_pro_locked"] = True
            f_row["stop_loss_price"] = None
            f_row["tp1_2x_price"] = None
            f_row["entry_trigger_price"] = None
            f_row["ma20_price"] = None
            f_row["ma60_price"] = None
        updated_free.append(f_row)

    # Update SemiFearGreed overview ($SMH, $XLV, $QQQ, KRW=X)
    try:
        smh_df = data["SMH"].dropna(subset=["Close"])
        xlv_df = data["XLV"].dropna(subset=["Close"])
        qqq_df = data["QQQ"].dropna(subset=["Close"])
        krw_df = data["KRW=X"].dropna(subset=["Close"])

        semi_dt = str(smh_df.index[-1].date())
        smh_c = round(float(smh_df["Close"].iloc[-1]), 2)
        xlv_c = round(float(xlv_df["Close"].iloc[-1]), 2)
        qqq_c = round(float(qqq_df["Close"].iloc[-1]), 2)
        usdkrw = round(float(krw_df["Close"].iloc[-1]), 2) if not krw_df.empty else semi_ov.get("usdkrw", 1380.0)

        smh_hi52 = float(smh_df["High"].tail(252).max()) if "High" in smh_df else float(smh_df["Close"].tail(252).max())
        smh_dd = round(((smh_c / max(smh_c, smh_hi52)) - 1.0) * 100.0, 2)

        semi_ov["date"] = semi_dt
        semi_ov["smh_close"] = smh_c
        semi_ov["xlv_close"] = xlv_c
        semi_ov["qqq_close"] = qqq_c
        semi_ov["usdkrw"] = usdkrw
        semi_ov["smh_dd_pct"] = smh_dd

        for etf_obj, df_e, sym in [
            (next((e for e in semi_ov.get("etfs", []) if e["ticker"] == "SMH"), None), smh_df, "SMH"),
            (next((e for e in semi_ov.get("etfs", []) if e["ticker"] == "XLV"), None), xlv_df, "XLV"),
            (next((e for e in semi_ov.get("etfs", []) if e["ticker"] == "QQQ"), None), qqq_df, "QQQ"),
        ]:
            if etf_obj and not df_e.empty:
                c_ser = df_e["Close"].astype(float)
                h_ser = df_e["High"].astype(float) if "High" in df_e else c_ser
                c_now = round(float(c_ser.iloc[-1]), 2)
                c_prev = float(c_ser.iloc[-2]) if len(c_ser) >= 2 else c_now
                c_20d = float(c_ser.iloc[-21]) if len(c_ser) >= 21 else c_now
                hi_52 = max(c_now, float(h_ser.tail(252).max()))
                etf_obj["close"] = c_now
                etf_obj["ret_1d_pct"] = round(((c_now / c_prev) - 1.0) * 100.0, 2)
                etf_obj["ret_20d_pct"] = round(((c_now / c_20d) - 1.0) * 100.0, 2)
                etf_obj["dd_52w_pct"] = round(((c_now / hi_52) - 1.0) * 100.0, 2)
                etf_obj["rsi14"] = compute_rsi14(c_ser)
    except Exception as exc:
        print(f"Warning updating semi_overview: {exc}")

    for sdir in STATIC_DIRS:
        if sdir.exists():
            (sdir / "stocks_pro.json").write_text(json.dumps(updated_pro, ensure_ascii=False, indent=2), encoding="utf-8")
            (sdir / "stocks_free.json").write_text(json.dumps(updated_free, ensure_ascii=False, indent=2), encoding="utf-8")
            (sdir / "semi_overview.json").write_text(json.dumps(semi_ov, ensure_ascii=False, indent=2), encoding="utf-8")

    ign_list = [s["ticker"] for s in updated_pro if s.get("zone_code") == "IGNITION_ZONE"]
    print(f"Synced 72 US stocks & ETFs as of {latest_date_str} | Active Ignition Zone ({len(ign_list)}): {ign_list}")


if __name__ == "__main__":
    main()
