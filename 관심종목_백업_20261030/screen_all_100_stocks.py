"""
Screens all 100 downloaded stocks as of 2026-10-14 for:
1. Current 52-Week Low Proximity & 52-Week High Drawdown
2. Moving Average Structure (MA20, MA60, MA200), RSI(14), Volume Wash-out / Accumulation
3. Historical 1-Year 2x (+100%) DNA per stock (how many times did each stock double in 1 year after a -45%+ crash?)
"""
import os
import glob
import json
import numpy as np
import pandas as pd

DATA_DIR = "data_stocks"

def compute_rsi(series, period=14):
    delta = series.diff()
    up = delta.clip(lower=0)
    down = -1 * delta.clip(upper=0)
    ma_up = up.ewm(com=period - 1, adjust=True, min_periods=period).mean()
    ma_down = down.ewm(com=period - 1, adjust=True, min_periods=period).mean()
    rs = ma_up / (ma_down + 1e-9)
    return 100.0 - (100.0 / (1.0 + rs))

rows = []
for path in sorted(glob.glob(os.path.join(DATA_DIR, "*.csv"))):
    t = os.path.basename(path).replace(".csv", "")
    df = pd.read_csv(path)
    if len(df) < 260:
        continue
    df["Date"] = pd.to_datetime(df["Date"])
    df.sort_values("Date", inplace=True)
    df.dropna(subset=["Close"], inplace=True)
    c = df["Close"].astype(float)
    h = df["High"].fillna(c).astype(float)
    lo = df["Low"].fillna(c).astype(float)
    v = df["Volume"].fillna(0).astype(float)

    cur = float(c.iloc[-1])
    dt = df["Date"].iloc[-1].strftime("%Y-%m-%d")
    lo52 = float(lo.tail(252).min())
    hi52 = float(h.tail(252).max())
    prox_low = (cur / lo52 - 1.0) * 100.0
    dd_high = (cur / hi52 - 1.0) * 100.0

    ma20 = float(c.tail(20).mean())
    ma60 = float(c.tail(60).mean())
    ma200 = float(c.tail(200).mean())
    rsi14 = float(compute_rsi(c).iloc[-1])

    vol20 = float(v.tail(20).mean()) + 1.0
    max_vol_10d = float(v.tail(10).max() / vol20)
    ret_5d = (cur / float(c.iloc[-6]) - 1.0) * 100.0 if len(c) >= 6 else 0.0
    ret_20d = (cur / float(c.iloc[-21]) - 1.0) * 100.0 if len(c) >= 21 else 0.0

    # Historical DNA: when this stock dropped >= 40% from 52W High in the past, how often did it hit +100% (2x) within 252 days?
    hi_roll = h.rolling(252, min_periods=120).max()
    dd_series = (c / hi_roll - 1.0) * 100.0
    rev_high_252 = h.iloc[::-1].rolling(252, min_periods=60).max().iloc[::-1].shift(-1)
    fwd_max_gain = (rev_high_252 / c - 1.0) * 100.0
    deep_dd_mask = (dd_series <= -40.0) & fwd_max_gain.notna()
    if deep_dd_mask.sum() > 20:
        hist_2x_rate_after_crash = float((fwd_max_gain[deep_dd_mask] >= 100.0).mean() * 100.0)
        hist_med_peak_after_crash = float(fwd_max_gain[deep_dd_mask].median())
    else:
        hist_2x_rate_after_crash = 0.0
        hist_med_peak_after_crash = 0.0

    rows.append({
        "Ticker": t.replace("_KS", ".KS").replace("_KQ", ".KQ"),
        "Date": dt,
        "Close": round(cur, 2),
        "Low52": round(lo52, 2),
        "High52": round(hi52, 2),
        "ProxLow52_Pct": round(prox_low, 1),
        "DDHigh52_Pct": round(dd_high, 1),
        "Vs_MA20_Pct": round((cur / ma20 - 1.0) * 100.0, 1),
        "Vs_MA60_Pct": round((cur / ma60 - 1.0) * 100.0, 1),
        "Vs_MA200_Pct": round((cur / ma200 - 1.0) * 100.0, 1),
        "RSI14": round(rsi14, 1),
        "VolSurge10D": round(max_vol_10d, 2),
        "Ret5D_Pct": round(ret_5d, 1),
        "Ret20D_Pct": round(ret_20d, 1),
        "Hist_2x_Rate_After_40Pct_Crash": round(hist_2x_rate_after_crash, 1),
        "Hist_Med_PeakGain_After_Crash": round(hist_med_peak_after_crash, 1),
    })

sdf = pd.DataFrame(rows)
sdf.to_json("all_100_stocks_screened.json", orient="records", force_ascii=False, indent=2)

print("=== A. NEAR 52-WEEK LOW (ProxLow52 <= 30% & DDHigh52 <= -40%) SORTED BY HISTORICAL 2x DNA ===")
near_low = sdf[(sdf["ProxLow52_Pct"] <= 30.0) & (sdf["DDHigh52_Pct"] <= -40.0)].sort_values("Hist_2x_Rate_After_40Pct_Crash", ascending=False)
print(near_low[["Ticker", "Close", "ProxLow52_Pct", "DDHigh52_Pct", "Vs_MA20_Pct", "RSI14", "VolSurge10D", "Hist_2x_Rate_After_40Pct_Crash", "Hist_Med_PeakGain_After_Crash"]].to_string(index=False))

print("\n=== B. SUPER-CYCLE PULLBACK (-35% to -65% from 52W High, testing 200D MA or Deep Value) ===")
pullback = sdf[(sdf["DDHigh52_Pct"] <= -35.0) & (sdf["ProxLow52_Pct"] > 30.0)].sort_values("Hist_2x_Rate_After_40Pct_Crash", ascending=False)
print(pullback[["Ticker", "Close", "ProxLow52_Pct", "DDHigh52_Pct", "Vs_MA200_Pct", "RSI14", "VolSurge10D", "Hist_2x_Rate_After_40Pct_Crash", "Hist_Med_PeakGain_After_Crash"]].head(25).to_string(index=False))
