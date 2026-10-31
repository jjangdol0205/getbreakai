import pandas as pd
import numpy as np
from deep_empirical_backtest_2x import stocks, compute_rsi

target_tickers = [
    "402340_KS", "000660_KS", "042700_KS", "267260_KS", "003230_KS",
    "NVDA", "META", "NFLX", "MU", "AMD", "CELH", "ENPH", "UPST", "APP", "PLTR", "CVNA", "MBLY"
]

out = []
for t in target_tickers:
    if t not in stocks:
        continue
    df = stocks[t]
    c = df["Close"].astype(float).values
    h = df["High"].fillna(df["Close"]).astype(float).values
    lo = df["Low"].fillna(df["Close"]).astype(float).values
    dates = df.index
    s_c = pd.Series(c)
    lo52 = pd.Series(lo).rolling(252, min_periods=120).min().values
    hi52 = pd.Series(h).rolling(252, min_periods=120).max().values
    ma20 = s_c.rolling(20).mean().values
    ma60 = s_c.rolling(60).mean().values
    ma200 = s_c.rolling(200).mean().values
    rsi14 = compute_rsi(s_c, 14).values

    for i in range(252, len(c) - 252):
        if dates[i].year < 2018:
            continue
        prox = (c[i] / lo52[i] - 1.0) * 100.0
        dd = (c[i] / hi52[i] - 1.0) * 100.0
        vs200 = (c[i] / ma200[i] - 1.0) * 100.0

        if 14.0 <= prox <= 35.0 and dd <= -45.0 and c[i] > ma20[i] and c[i] > ma60[i]:
            mode = "PW-RSI (52W 신저가 탈출 우측시동)"
        elif -62.0 <= dd <= -30.0 and -12.0 <= vs200 <= 5.0 and rsi14[i] <= 33.0:
            mode = "SC-200MA (슈퍼사이클 200일선 급락)"
        else:
            continue

        if out and out[-1]["t"] == t and (dates[i] - pd.to_datetime(out[-1]["d"])).days < 120:
            continue

        p0 = c[i]
        max_g = (np.max(h[i + 1:i + 253]) / p0 - 1.0) * 100.0
        ret12 = (c[i + 252] / p0 - 1.0) * 100.0
        ret3 = (c[i + 63] / p0 - 1.0) * 100.0
        out.append({
            "t": t.replace("_KS", ".KS"),
            "mode": mode,
            "d": dates[i].strftime("%Y-%m-%d"),
            "p0": round(p0, 2),
            "dd": round(dd, 1),
            "prox": round(prox, 1),
            "ret3m": round(ret3, 1),
            "ret12m": round(ret12, 1),
            "max_1y": round(max_g, 1),
        })

df_out = pd.DataFrame(out)
print(df_out.to_string(index=False))
df_out.to_json("hall_of_fame_episodes.json", orient="records", force_ascii=False, indent=2)
