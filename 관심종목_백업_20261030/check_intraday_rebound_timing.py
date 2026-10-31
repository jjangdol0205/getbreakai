import sys
from datetime import datetime
import urllib3
import requests
import pandas as pd
import numpy as np

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
HEADERS = {"User-Agent": "Mozilla/5.0"}

# 1. Fetch live intraday price of SK Square (402340.KS) and SK Hynix (000660.KS)
for tkr, name in [("402340.KS", "SK스퀘어"), ("000660.KS", "SK하이닉스")]:
    try:
        url = f"https://query1.finance.yahoo.com/v8/finance/chart/{tkr}?range=5d&interval=5m"
        r = requests.get(url, headers=HEADERS, verify=False, timeout=6).json()["chart"]["result"][0]
        meta = r["meta"]
        cur_p = meta.get("regularMarketPrice")
        prev_c = meta.get("chartPreviousClose") or meta.get("previousClose")
        day_high = meta.get("regularMarketDayHigh")
        day_low = meta.get("regularMarketDayLow")
        chg = (cur_p / prev_c - 1.0) * 100.0 if (cur_p and prev_c) else 0.0
        print(f"[실시간 장중 시세] {name}({tkr}): 현재가 {cur_p:,.0f}원 (전일대비 {chg:+.2f}% | 장중저가 {day_low:,.0f}원 ~ 고가 {day_high:,.0f}원)")
    except Exception as e:
        print(f"Live fetch error for {tkr}: {e}")

# 2. Fetch daily series and calculate exact drawdown duration & rebound timing statistics
for tkr, name in [("402340.KS", "SK스퀘어"), ("000660.KS", "SK하이닉스")]:
    url = f"https://query1.finance.yahoo.com/v8/finance/chart/{tkr}?range=5y&interval=1d"
    res = requests.get(url, headers=HEADERS, verify=False, timeout=8).json()["chart"]["result"][0]
    ts = res["timestamp"]
    q = res["indicators"]["quote"][0]
    df = pd.DataFrame({
        "Date": [datetime.fromtimestamp(x).strftime("%Y-%m-%d") for x in ts],
        "Close": q["close"],
        "High": q["high"],
        "Low": q["low"],
        "Volume": q["volume"],
    }).dropna(subset=["Close"]).reset_index(drop=True)

    c = df["Close"].astype(float)
    h = df["High"].fillna(c).astype(float)
    lo = df["Low"].fillna(c).astype(float)
    df["High60"] = h.rolling(60, min_periods=20).max()
    df["DD60"] = (c / df["High60"] - 1.0) * 100.0
    df["MA20"] = c.rolling(20).mean()
    df["MA60"] = c.rolling(60).mean()
    df["MA120"] = c.rolling(120).mean()
    df["MA200"] = c.rolling(200).mean()

    delta = c.diff()
    up = delta.clip(lower=0).ewm(com=13, adjust=True, min_periods=14).mean()
    dn = (-delta.clip(upper=0)).ewm(com=13, adjust=True, min_periods=14).mean()
    df["RSI14"] = 100.0 - 100.0 / (1.0 + up / (dn + 1e-9))

    last = df.iloc[-1]
    # Find date of recent 60D peak
    recent_slice = df.tail(45)
    peak_idx = recent_slice["High"].idxmax()
    peak_date = df.loc[peak_idx, "Date"]
    peak_price = df.loc[peak_idx, "High"]
    trading_days_down = len(df) - 1 - peak_idx

    print(f"\n=== {name} ({tkr}) 현재 조정 진행 일수 및 지지선 위치 ===")
    print(f" * 직전 고점일: {peak_date} ({peak_price:,.0f}원) -> 오늘까지 {trading_days_down}거래일째 조정 중 (고점 대비 {last['DD60']:+.2f}%)")
    print(f" * 현재가: {last['Close']:,.0f}원 | RSI(14): {last['RSI14']:.1f}")
    print(f" * 주요 이평선: 20일선 {last['MA20']:,.0f}원 | 60일선 {last['MA60']:,.0f}원 | 120일선 {last['MA120']:,.0f}원 | 200일선 {last['MA200']:,.0f}원")

    # Find historical episodes where RSI14 dropped below 31 and DD60 <= -25%
    episodes = []
    in_ep = False
    for i in range(60, len(df) - 20):
        if not in_ep and df.loc[i, "RSI14"] <= 31.5 and df.loc[i, "DD60"] <= -22.0:
            in_ep = True
            # Find local trough within next 10 trading days
            win = df.iloc[i:min(len(df), i + 12)]
            trough_i = win["Close"].idxmin()
            trough_d = df.loc[trough_i, "Date"]
            trough_p = df.loc[trough_i, "Close"]
            days_to_bottom = trough_i - i

            # Find rebound after trough: +10%, +20%, +30%
            post = df.iloc[trough_i + 1:min(len(df), trough_i + 90)]
            d_10 = next((idx - trough_i for idx, r in post.iterrows() if r["Close"] >= trough_p * 1.10), None)
            d_20 = next((idx - trough_i for idx, r in post.iterrows() if r["Close"] >= trough_p * 1.20), None)
            d_30 = next((idx - trough_i for idx, r in post.iterrows() if r["Close"] >= trough_p * 1.30), None)
            max_60d_ret = (post["Close"].max() / trough_p - 1.0) * 100.0 if len(post) > 0 else 0.0

            episodes.append({
                "Signal_Date": df.loc[i, "Date"],
                "RSI_at_Signal": round(df.loc[i, "RSI14"], 1),
                "Bottom_Date": trough_d,
                "Days_Signal_to_Bottom": days_to_bottom,
                "Days_to_+10%_Rebound": d_10,
                "Days_to_+20%_Rebound": d_20,
                "Days_to_+30%_Rebound": d_30,
                "Max_90D_Rebound_Pct": round(max_60d_ret, 1),
            })
        elif in_ep and df.loc[i, "RSI14"] >= 45.0:
            in_ep = False

    print(f"\n=== {name} 과거 유사 급락장(RSI<=31.5 & 고점대비 -22% 이상) 진입 후 진바닥 & 반등 소요 시간 ===")
    if episodes:
        ep_df = pd.DataFrame(episodes)
        print(ep_df.to_string(index=False))
