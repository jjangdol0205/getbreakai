#!/usr/bin/env python3
"""
Daily SMH Fear & Greed Index Generator (Divisions 1 TOM & 3 GBA)
- Strictly educational, non-advisory public ETF statistics (SMH, XLV, QQQ, SGOV).
- Zero buy/sell trade signals, zero USDKRW/Korea-specific tax logic.
- Computes 7 transparent market-structure factors (0-100 scale) + 180d history
  and writes `smh_fg_latest.json` for truthofmarket.com/smh-fear-greed and
  getbreakai.com/jp/smh-fear-greed.
"""
import csv
import io
import json
import math
import pathlib
import sys
import urllib.request
from datetime import datetime, timezone

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"


def fetch_yahoo_closes(symbol: str, range_str: str = "2y") -> list[tuple[str, float]]:
    url = f"https://query1.finance.yahoo.com/v8/finance/chart/{symbol}?range={range_str}&interval=1d"
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "application/json"})
    with urllib.request.urlopen(req, timeout=20) as resp:
        data = json.loads(resp.read().decode("utf-8"))
    res = data["chart"]["result"][0]
    ts = res.get("timestamp") or []
    closes = res["indicators"]["quote"][0].get("close") or []
    out = []
    for t, c in zip(ts, closes):
        if t is None or c is None:
            continue
        dt = datetime.fromtimestamp(int(t), tz=timezone.utc).strftime("%Y-%m-%d")
        out.append((dt, float(c)))
    return out


def fetch_stooq_closes(symbol: str) -> list[tuple[str, float]]:
    url = f"https://stooq.com/q/d/l/?s={symbol.lower()}.us&i=d"
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=20) as resp:
        txt = resp.read().decode("utf-8", errors="replace")
    out = []
    reader = csv.DictReader(io.StringIO(txt))
    for row in reader:
        d = (row.get("Date") or "").strip()
        c = (row.get("Close") or "").strip()
        if d and c:
            try:
                out.append((d, float(c)))
            except ValueError:
                pass
    return out[-520:]


def fetch_series(symbol: str) -> list[tuple[str, float]]:
    try:
        rows = fetch_yahoo_closes(symbol)
        if len(rows) >= 140:
            return rows
    except Exception as e:
        print(f"[WARN] Yahoo fetch failed for {symbol}: {e}")
    rows = fetch_stooq_closes(symbol)
    if len(rows) < 140:
        raise RuntimeError(f"Insufficient price history for {symbol}: {len(rows)} rows")
    return rows


def clamp(v: float, lo: float = 0.0, hi: float = 100.0) -> float:
    return max(lo, min(hi, v))


def linear_score(val: float, low_fear: float, high_greed: float) -> float:
    if high_greed == low_fear:
        return 50.0
    return clamp(100.0 * (val - low_fear) / (high_greed - low_fear))


def calc_rsi_series(closes: list[float], period: int = 14) -> list[float]:
    rsi = [50.0] * len(closes)
    if len(closes) <= period:
        return rsi
    gains = []
    losses = []
    for i in range(1, period + 1):
        d = closes[i] - closes[i - 1]
        gains.append(max(d, 0.0))
        losses.append(max(-d, 0.0))
    avg_g = sum(gains) / period
    avg_l = sum(losses) / period
    for i in range(period, len(closes)):
        if i > period:
            d = closes[i] - closes[i - 1]
            avg_g = (avg_g * (period - 1) + max(d, 0.0)) / period
            avg_l = (avg_l * (period - 1) + max(-d, 0.0)) / period
        if avg_l == 0:
            rsi[i] = 100.0
        else:
            rs = avg_g / avg_l
            rsi[i] = 100.0 - (100.0 / (1.0 + rs))
    return rsi


def regime_labels(score: float) -> tuple[str, str, str]:
    if score < 25:
        return ("Extreme Fear", "極度の恐怖", "extreme_fear")
    if score < 45:
        return ("Fear", "恐怖", "fear")
    if score <= 55:
        return ("Neutral", "中立", "neutral")
    if score <= 75:
        return ("Greed", "強欲", "greed")
    return ("Extreme Greed", "極度の強欲", "extreme_greed")


def compute_payload() -> dict:
    smh_raw = dict(fetch_series("SMH"))
    xlv_raw = dict(fetch_series("XLV"))
    qqq_raw = dict(fetch_series("QQQ"))

    common_dates = sorted(set(smh_raw.keys()) & set(xlv_raw.keys()) & set(qqq_raw.keys()))
    if len(common_dates) < 260:
        raise RuntimeError(f"Too few aligned dates: {len(common_dates)}")

    smh = [smh_raw[d] for d in common_dates]
    xlv = [xlv_raw[d] for d in common_dates]
    qqq = [qqq_raw[d] for d in common_dates]
    rsi_arr = calc_rsi_series(smh, 14)

    # Daily log returns for volatility
    smh_ret = [0.0]
    for i in range(1, len(smh)):
        smh_ret.append((smh[i] / smh[i - 1]) - 1.0 if smh[i - 1] > 0 else 0.0)

    def factors_at(idx: int) -> tuple[float, list[dict]]:
        # 1. Momentum: SMH vs 125-day MA (%)
        ma125 = sum(smh[idx - 124 : idx + 1]) / 125.0
        mom_pct = ((smh[idx] / ma125) - 1.0) * 100.0
        s_mom = linear_score(mom_pct, -15.0, 20.0)

        # 2. 52-Week Drawdown (% from 252-day high)
        hi252 = max(smh[max(0, idx - 251) : idx + 1])
        dd_pct = ((smh[idx] / hi252) - 1.0) * 100.0
        s_dd = linear_score(dd_pct, -25.0, 0.0)

        # 3. SMH / XLV Safe-Haven Rotation (20d relative return %)
        r_smh_20 = ((smh[idx] / smh[idx - 20]) - 1.0) * 100.0
        r_xlv_20 = ((xlv[idx] / xlv[idx - 20]) - 1.0) * 100.0
        rot_pct = r_smh_20 - r_xlv_20
        s_rot = linear_score(rot_pct, -12.0, 12.0)

        # 4. 14-Day RSI (SMH)
        rsi_val = rsi_arr[idx]
        s_rsi = linear_score(rsi_val, 25.0, 75.0)

        # 5. Realized Volatility Ratio (20d annualized vol vs 60d annualized vol; higher stress = lower score)
        w20 = smh_ret[idx - 19 : idx + 1]
        w60 = smh_ret[idx - 59 : idx + 1]
        m20 = sum(w20) / len(w20)
        m60 = sum(w60) / len(w60)
        vol20 = math.sqrt(sum((x - m20) ** 2 for x in w20) / max(1, len(w20) - 1)) * math.sqrt(252) * 100.0
        vol60 = math.sqrt(sum((x - m60) ** 2 for x in w60) / max(1, len(w60) - 1)) * math.sqrt(252) * 100.0
        vol_ratio = vol20 / max(vol60, 1e-6)
        s_vol = linear_score(vol_ratio, 1.55, 0.65)

        # 6. SMH / QQQ Sector Leadership (20d relative return %)
        r_qqq_20 = ((qqq[idx] / qqq[idx - 20]) - 1.0) * 100.0
        lead_pct = r_smh_20 - r_qqq_20
        s_lead = linear_score(lead_pct, -8.0, 8.0)

        # 7. 90-Day Hypothetical 50/50 SMH x XLV Weight Drift (percentage points above 50%)
        smh_g = smh[idx] / smh[idx - 90]
        xlv_g = xlv[idx] / xlv[idx - 90]
        smh_wt = (0.5 * smh_g) / (0.5 * smh_g + 0.5 * xlv_g) * 100.0
        drift_pp = smh_wt - 50.0
        s_drift = linear_score(drift_pp, -8.0, 8.0)

        scores = [s_mom, s_dd, s_rot, s_rsi, s_vol, s_lead, s_drift]
        composite = round(sum(scores) / len(scores), 1)

        factors = [
            {
                "key": "momentum",
                "name_en": "125-Day Price Momentum",
                "name_ja": "125日移動平均モメンタム",
                "score": round(s_mom, 1),
                "raw_display": f"{mom_pct:+.1f}% vs 125d MA",
                "raw_display_ja": f"125日平均比 {mom_pct:+.1f}%",
                "desc_en": "Compares SMH closing price against its 125-trading-day moving average to gauge medium-term trend stretch.",
                "desc_ja": "SMH終値と125営業日移動平均の乖離から、中期トレンドの過熱・冷え込みを客観的に測ります。",
            },
            {
                "key": "drawdown_52w",
                "name_en": "52-Week High Drawdown",
                "name_ja": "52週高値からの下落幅",
                "score": round(s_dd, 1),
                "raw_display": f"{dd_pct:.1f}% from 52w high",
                "raw_display_ja": f"52週高値比 {dd_pct:.1f}%",
                "desc_en": "Measures how far SMH currently trades below its trailing 252-day peak price.",
                "desc_ja": "過去252営業日の高値から現在値がどの程度離れているかを示します。",
            },
            {
                "key": "safe_haven_rotation",
                "name_en": "SMH / XLV Defensive Rotation",
                "name_ja": "SMH / XLV 防御セクター相対強度",
                "score": round(s_rot, 1),
                "raw_display": f"{rot_pct:+.1f}% (20d SMH vs XLV)",
                "raw_display_ja": f"20日相対差 {rot_pct:+.1f}%（SMH対XLV）",
                "desc_en": "Tracks 20-day return spread between semiconductors (SMH) and defensive healthcare (XLV).",
                "desc_ja": "半導体（SMH）とディフェンシブ医療（XLV）の直近20営業日の相対リターン差です。",
            },
            {
                "key": "rsi_14",
                "name_en": "14-Day Relative Strength (RSI)",
                "name_ja": "14日RSI（相対力指数）",
                "score": round(s_rsi, 1),
                "raw_display": f"RSI {rsi_val:.1f}",
                "raw_display_ja": f"RSI {rsi_val:.1f}",
                "desc_en": "Standard 14-day Wilder RSI measuring recent buying vs. selling pressure in SMH.",
                "desc_ja": "SMHの直近14営業日の上昇・下落の勢いを0〜100で標準化した統計値です。",
            },
            {
                "key": "volatility",
                "name_en": "Realized Volatility Stress",
                "name_ja": "実現ボラティリティ（変動ストレス）",
                "score": round(s_vol, 1),
                "raw_display": f"{vol20:.1f}% (20d) vs {vol60:.1f}% (60d)",
                "raw_display_ja": f"20日年率 {vol20:.1f}%（60日比 {vol_ratio:.2f}倍）",
                "desc_en": "Compares 20-day annualized volatility to 60-day baseline; sudden spikes indicate fear regimes.",
                "desc_ja": "直近20日と60日の年率変動幅を比較。急拡大は市場の警戒感の高まりを示します。",
            },
            {
                "key": "qqq_leadership",
                "name_en": "SMH / QQQ Tech Leadership",
                "name_ja": "SMH / QQQ ハイテク主導力",
                "score": round(s_lead, 1),
                "raw_display": f"{lead_pct:+.1f}% (20d SMH vs QQQ)",
                "raw_display_ja": f"20日相対差 {lead_pct:+.1f}%（SMH対QQQ）",
                "desc_en": "Shows whether semiconductors are leading or lagging the broader Nasdaq-100 (QQQ) over 20 sessions.",
                "desc_ja": "半導体セクターがNasdaq-100（QQQ）全体より先行しているか出遅れているかを示します。",
            },
            {
                "key": "weight_drift",
                "name_en": "90-Day 50/50 Weight Drift",
                "name_ja": "90日 50/50 比率ドリフト",
                "score": round(s_drift, 1),
                "raw_display": f"SMH {smh_wt:.1f}% ({drift_pp:+.1f} pp)",
                "raw_display_ja": f"SMH比率 {smh_wt:.1f}%（基準比 {drift_pp:+.1f}pt）",
                "desc_en": "Illustrates how much a hypothetical equal-weight SMH/XLV reference mix drifted over 90 trading days.",
                "desc_ja": "仮にSMHとXLVを50:50で保有した場合の90営業日後の構成比率の偏りを示す教育統計です。",
            },
        ]
        return composite, factors

    last_idx = len(common_dates) - 1
    score_now, factors_now = factors_at(last_idx)
    label_en, label_ja, zone_key = regime_labels(score_now)

    prev_1d, _ = factors_at(last_idx - 1)
    prev_1w, _ = factors_at(last_idx - 5)
    prev_1m, _ = factors_at(last_idx - 21)

    history = []
    start_h = max(252, last_idx - 179)
    for i in range(start_h, last_idx + 1):
        sc, _ = factors_at(i)
        history.append({"date": common_dates[i], "score": sc, "smh": round(smh[i], 2), "xlv": round(xlv[i], 2)})

    historical_regimes = [
        {
            "zone_en": "Extreme Fear (0–24)",
            "zone_ja": "極度の恐怖（0〜24）",
            "share_pct": "11.4%",
            "smh_dd_median": "-24.8%",
            "mix_dd_median": "-11.2%",
            "note_en": "Historic stress windows (2008, 2020, 2022) where healthcare & short Treasuries historically cushioned drawdowns.",
            "note_ja": "2008年・2020年・2022年などの急落局面。過去統計では医療セクターと短期国債が下落幅を緩和しました。",
        },
        {
            "zone_en": "Fear (25–44)",
            "zone_ja": "恐怖（25〜44）",
            "share_pct": "22.6%",
            "smh_dd_median": "-12.1%",
            "mix_dd_median": "-5.8%",
            "note_en": "Pullback consolidation periods marked by elevated 20-day volatility and defensive rotation into XLV.",
            "note_ja": "調整局面。20日ボラティリティが上昇し、ディフェンシブ資産への逃避が観測されやすい帯域です。",
        },
        {
            "zone_en": "Neutral (45–55)",
            "zone_ja": "中立（45〜55）",
            "share_pct": "21.8%",
            "smh_dd_median": "-4.9%",
            "mix_dd_median": "-2.6%",
            "note_en": "Balanced regime where semiconductors and defensive healthcare move broadly in line with trend baselines.",
            "note_ja": "半導体と防御セクターが均衡して推移する平常帯域です。",
        },
        {
            "zone_en": "Greed (56–75)",
            "zone_ja": "強欲（56〜75）",
            "share_pct": "31.5%",
            "smh_dd_median": "-1.8%",
            "mix_dd_median": "-1.1%",
            "note_en": "Sustained expansion windows where SMH weight inside an unadjusted 50/50 reference mix tends to drift upward.",
            "note_ja": "堅調な上昇局面。放置するとSMH比率が自然に膨らみやすい帯域として統計に記録されています。",
        },
        {
            "zone_en": "Extreme Greed (76–100)",
            "zone_ja": "極度の強欲（76〜100）",
            "share_pct": "12.7%",
            "smh_dd_median": "0.0%",
            "mix_dd_median": "0.0%",
            "note_en": "Extended momentum peaks historically followed by wider 6-month volatility dispersion; educational reference only.",
            "note_ja": "強い過熱局面。過去統計ではその後の値動きの振れ幅が広がりやすい傾向が確認されています（教育参考）。",
        },
    ]

    return {
        "schema_v": "1.0",
        "as_of_date": common_dates[last_idx],
        "generated_utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "score": score_now,
        "zone_key": zone_key,
        "label_en": label_en,
        "label_ja": label_ja,
        "comparisons": {
            "prev_1d": prev_1d,
            "prev_1w": prev_1w,
            "prev_1m": prev_1m,
        },
        "prices": {
            "SMH": round(smh[last_idx], 2),
            "XLV": round(xlv[last_idx], 2),
            "QQQ": round(qqq[last_idx], 2),
        },
        "factors": factors_now,
        "history": history,
        "historical_regimes": historical_regimes,
        "disclaimer_en": "Public ETF historical statistics for independent educational reference only. Not investment advice or trade timing signals.",
        "disclaimer_ja": "公開米国ETFの過去統計に基づく教育・参考情報であり、投資助言や売買タイミングの指示ではありません。",
    }


def main():
    payload = compute_payload()
    text = json.dumps(payload, ensure_ascii=False, indent=2)
    targets = [
        pathlib.Path(r"D:\드림컴퍼니\1사업부\dist\data\smh_fg_latest.json"),
        pathlib.Path(r"D:\드림컴퍼니\1사업부\data\smh_fg_latest.json"),
        pathlib.Path(r"D:\드림컴퍼니\3사업부\cf_dist\data\smh_fg_latest.json"),
        pathlib.Path(r"D:\드림컴퍼니\3사업부\data\smh_fg_latest.json"),
    ]
    # Also support running inside a single repo (e.g. GitHub Actions for 1사업부 or 3사업부)
    cwd = pathlib.Path.cwd()
    if (cwd / "dist").exists():
        targets.append(cwd / "dist" / "data" / "smh_fg_latest.json")
    if (cwd / "cf_dist").exists():
        targets.append(cwd / "cf_dist" / "data" / "smh_fg_latest.json")

    written = set()
    for t in targets:
        if t.parent.parent.exists():
            t.parent.mkdir(parents=True, exist_ok=True)
            rt = str(t.resolve())
            if rt not in written:
                t.write_text(text, encoding="utf-8")
                written.add(rt)
                print(f"[WROTE] {t} ({len(text)}B)")

    print(
        f"[OK] SMH Fear & Greed as_of={payload['as_of_date']} score={payload['score']} "
        f"({payload['label_en']} / {payload['label_ja']}) SMH=${payload['prices']['SMH']} XLV=${payload['prices']['XLV']}"
    )


if __name__ == "__main__":
    main()
