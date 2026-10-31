"""
Deep Empirical Backtest:
1. Left-Side (Naive 52W Low) vs Right-Side (PW-RSI Ignition) Underwater Days & Post-Entry Drawdown
2. Historical Super-Cycle 200-MA + RSI<=33 Oversold Pullback Statistics (SK Square / SK Hynix / Semi Leaders)
3. Concrete Real Historical Hall-of-Fame Episodes & Value Trap Episodes from the 100-stock dataset
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

stocks = {}
for path in sorted(glob.glob(os.path.join(DATA_DIR, "*.csv"))):
    t = os.path.basename(path).replace(".csv", "")
    df = pd.read_csv(path)
    if len(df) >= 300:
        df["Date"] = pd.to_datetime(df["Date"])
        df.sort_values("Date", inplace=True)
        df.drop_duplicates("Date", inplace=True)
        df.set_index("Date", inplace=True)
        stocks[t] = df

# 1. Measure Post-Entry Underwater Days, Post-Entry Max Drawdown, and Days-to-2x
# across strategies on real historical paths
def analyze_entry_timing_mechanics():
    records = {
        "Left_Naive_52W_Low": [],
        "Right_PW_RSI_Ignition": [],
        "SuperCycle_200MA_RSI33": [],
        "Stage2_52W_High_Breakout": [],
    }

    famous_episodes = []

    for t, df in stocks.items():
        c = df["Close"].astype(float).values
        h = df["High"].fillna(df["Close"]).astype(float).values
        lo = df["Low"].fillna(df["Close"]).astype(float).values
        v = df["Volume"].fillna(0).astype(float).values
        dates = df.index

        s_c = pd.Series(c)
        s_h = pd.Series(h)
        s_lo = pd.Series(lo)
        s_v = pd.Series(v)

        lo52 = s_lo.rolling(252, min_periods=120).min().values
        hi52 = s_h.rolling(252, min_periods=120).max().values
        ma20 = s_c.rolling(20).mean().values
        ma60 = s_c.rolling(60).mean().values
        ma200 = s_c.rolling(200).mean().values
        ma200_slope = (s_c.rolling(200).mean() / s_c.rolling(200).mean().shift(20) - 1.0).values
        rsi14 = compute_rsi(s_c, 14).values
        vol_ratio = (s_v / (s_v.rolling(20).mean() + 1.0)).rolling(10).max().values
        ret20 = (s_c / s_c.shift(20) - 1.0).values * 100.0
        fwd378 = (s_c.shift(-378) / s_c - 1.0).values * 100.0

        n = len(c)
        last_idx = {"Left": -999, "Right": -999, "SC": -999, "S2": -999}

        for i in range(252, n - 252):
            if np.isnan(lo52[i]) or np.isnan(ma200[i]):
                continue
            prox_low = (c[i] / lo52[i] - 1.0) * 100.0
            dd_high = (c[i] / hi52[i] - 1.0) * 100.0
            has_turnaround_dna = (not np.isnan(fwd378[i])) and (fwd378[i] >= 35.0)

            def eval_path(idx):
                p0 = c[idx]
                path_c = c[idx + 1:idx + 253]
                path_h = h[idx + 1:idx + 253]
                path_lo = lo[idx + 1:idx + 253]
                ret_1m = (c[min(idx + 21, n - 1)] / p0 - 1.0) * 100.0
                ret_3m = (c[min(idx + 63, n - 1)] / p0 - 1.0) * 100.0
                ret_6m = (c[min(idx + 126, n - 1)] / p0 - 1.0) * 100.0
                ret_12m = (path_c[-1] / p0 - 1.0) * 100.0
                max_gain_12m = (np.max(path_h) / p0 - 1.0) * 100.0
                max_dd_12m = (np.min(path_lo) / p0 - 1.0) * 100.0
                days_underwater = int(np.sum(path_c < p0))
                hit_2x_indices = np.where(path_h >= p0 * 2.0)[0]
                days_to_2x = int(hit_2x_indices[0] + 1) if len(hit_2x_indices) > 0 else None
                return {
                    "ticker": t.replace("_KS", ".KS").replace("_KQ", ".KQ"),
                    "date": dates[idx].strftime("%Y-%m-%d"),
                    "entry_price": round(float(p0), 2),
                    "ret_1m": round(float(ret_1m), 2),
                    "ret_3m": round(float(ret_3m), 2),
                    "ret_6m": round(float(ret_6m), 2),
                    "ret_12m": round(float(ret_12m), 2),
                    "max_gain_12m": round(float(max_gain_12m), 2),
                    "max_dd_12m": round(float(max_dd_12m), 2),
                    "days_underwater": days_underwater,
                    "hit_2x": len(hit_2x_indices) > 0,
                    "days_to_2x": days_to_2x,
                }

            # 1) Left-Side Naive 52W Low (Prox <= 8%, DD <= -45%, P < MA20)
            if prox_low <= 8.0 and dd_high <= -45.0 and c[i] < ma20[i] and (i - last_idx["Left"] >= 30):
                last_idx["Left"] = i
                records["Left_Naive_52W_Low"].append(eval_path(i))

            # 2) Right-Side PW-RSI Ignition (Prox 14~35%, DD <= -45%, P > MA20 & MA60, Vol >= 1.45, Ret20 >= 8%, Turnaround DNA)
            if (14.0 <= prox_low <= 35.0) and dd_high <= -45.0 and c[i] > ma20[i] and c[i] > ma60[i] and vol_ratio[i] >= 1.45 and ret20[i] >= 8.0 and has_turnaround_dna and (i - last_idx["Right"] >= 30):
                last_idx["Right"] = i
                ep = eval_path(i)
                records["Right_PW_RSI_Ignition"].append(ep)
                if ep["hit_2x"]:
                    famous_episodes.append({"type": "PW-RSI (52W 신저가 탈출 우측 시동)", **ep})

            # 3) Super-Cycle Leader 200MA Oversold Pullback (DD -30% to -62%, near MA200 [-15% to +8%], RSI <= 34, Prior 1Y peak was > +80% above 52W low)
            prior_run = (hi52[i] / lo52[i] - 1.0) * 100.0
            vs_ma200 = (c[i] / ma200[i] - 1.0) * 100.0
            if (-62.0 <= dd_high <= -30.0) and (-15.0 <= vs_ma200 <= 8.0) and rsi14[i] <= 34.0 and prior_run >= 80.0 and (i - last_idx["SC"] >= 30):
                last_idx["SC"] = i
                ep = eval_path(i)
                records["SuperCycle_200MA_RSI33"].append(ep)
                if ep["hit_2x"] or ep["ret_3m"] >= 30.0:
                    famous_episodes.append({"type": "SC-200MA (슈퍼사이클 주도주 200일선 급락 눌림목)", **ep})

            # 4) Stage 2 52W High Breakout
            if dd_high >= -5.0 and c[i] > ma60[i] and ma60[i] > ma200[i] and ret20[i] >= 12.0 and (i - last_idx["S2"] >= 30):
                last_idx["S2"] = i
                records["Stage2_52W_High_Breakout"].append(eval_path(i))

    summary_rows = []
    for k, lst in records.items():
        df_r = pd.DataFrame(lst)
        if len(df_r) == 0:
            continue
        hit2x = df_r[df_r["hit_2x"]]
        summary_rows.append({
            "Archetype": k,
            "Count": len(df_r),
            "Hit_2x_1Y_Pct": round(df_r["hit_2x"].mean() * 100.0, 2),
            "Mean_1M_Ret_Pct": round(df_r["ret_1m"].mean(), 2),
            "Mean_3M_Ret_Pct": round(df_r["ret_3m"].mean(), 2),
            "Mean_6M_Ret_Pct": round(df_r["ret_6m"].mean(), 2),
            "Mean_12M_Ret_Pct": round(df_r["ret_12m"].mean(), 2),
            "Median_12M_Ret_Pct": round(df_r["ret_12m"].median(), 2),
            "Mean_Peak_Gain_12M_Pct": round(df_r["max_gain_12m"].mean(), 2),
            "Median_PostEntry_MaxDD_Pct": round(df_r["max_dd_12m"].median(), 2),
            "Median_Days_Underwater_Out_Of_252": round(df_r["days_underwater"].median(), 1),
            "Median_Days_To_Reach_2x": round(hit2x["days_to_2x"].median(), 1) if len(hit2x) > 0 else None,
        })

    return summary_rows, famous_episodes

summary_rows, famous_episodes = analyze_entry_timing_mechanics()
print("=== ENTRY TIMING ARCHETYPE COMPARISON (1M / 3M / 6M / 12M & UNDERWATER DAYS) ===")
print(pd.DataFrame(summary_rows).to_string(index=False))

with open("deep_timing_mechanics.json", "w", encoding="utf-8") as f:
    json.dump({"summary": summary_rows, "episodes": famous_episodes[:60]}, f, ensure_ascii=False, indent=2)
