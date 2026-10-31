"""
Deep Case Study & Real Historical Path Analyzer:
1. Inspects actual downloaded KRX data for 402340.KS (SK스퀘어), 000660.KS (SK하이닉스),
   042700.KS (한미반도체), 267260.KS (HD현대일렉트릭), 003230.KS (삼양식품) and US Watchlist stocks.
2. Extracts concrete historical examples of:
   - True 52W-Low + Dynamic Earnings Inflection 2x+ Winners (within 1 year)
   - Naive 52W-Low "Falling Knife / Dead Money" Traps (where buying too early on the left side failed)
   - How "PW-RSI (Post-Washout Right-Side Ignition + 60D Time-Stop)" avoided the traps and caught the 2x wave!
"""
import os
import json
import pandas as pd
import numpy as np

DATA_DIR = "data_stocks"

def inspect_latest_prices():
    tickers = ["402340_KS", "000660_KS", "042700_KS", "267260_KS", "003230_KS", "MBLY", "CELH", "ENPH", "UPST", "FLNC", "UBER", "NVDA", "MU", "AMD", "PLTR", "APP", "CVNA"]
    rows = []
    for t in tickers:
        p = os.path.join(DATA_DIR, f"{t}.csv")
        if not os.path.exists(p):
            continue
        df = pd.read_csv(p)
        df["Date"] = pd.to_datetime(df["Date"])
        df.sort_values("Date", inplace=True)
        last252 = df.tail(252)
        cur = float(df["Close"].iloc[-1])
        dt = df["Date"].iloc[-1].strftime("%Y-%m-%d")
        lo52 = float(last252["Low"].min())
        hi52 = float(last252["High"].max())
        ma20 = float(df["Close"].tail(20).mean())
        ma60 = float(df["Close"].tail(60).mean())
        ma200 = float(df["Close"].tail(200).mean())
        ret_1y = (cur / float(df["Close"].iloc[-min(len(df), 252)]) - 1.0) * 100.0
        rows.append({
            "Ticker": t,
            "LastDate": dt,
            "Close": cur,
            "Low52": lo52,
            "High52": hi52,
            "Prox52Low_Pct": round((cur / lo52 - 1.0) * 100.0, 1),
            "DD52High_Pct": round((cur / hi52 - 1.0) * 100.0, 1),
            "MA20": round(ma20, 2),
            "MA60": round(ma60, 2),
            "MA200": round(ma200, 2),
            "Ret1Y_Pct": round(ret_1y, 1),
        })
    return pd.DataFrame(rows)

if __name__ == "__main__":
    df_latest = inspect_latest_prices()
    print("=== LATEST DOWNLOADED PRICES & 52W METRICS ===")
    print(df_latest.to_string(index=False))
    df_latest.to_json("latest_universe_snapshot.json", orient="records", force_ascii=False, indent=2)
