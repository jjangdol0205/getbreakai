"""
Downloads daily historical OHLCV data for a broad universe of US and Korean individual stocks
to empirically test 1-Year 2x+ (+100%) Single-Stock Alpha Strategies:
- US Tech / Semi / Growth / Turnaround / Value-Trap stocks (55+ tickers)
- KR Semiconductor / Holding / Industrial / Growth / Turnaround stocks (25+ tickers)
"""
import os
import time
from datetime import datetime
import urllib3
import requests
import pandas as pd

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

OUT_DIR = "data_stocks"
os.makedirs(OUT_DIR, exist_ok=True)

US_TICKERS = [
    # Watchlist & Recent 52W-Low Turnaround Candidates
    "MBLY", "CELH", "ENPH", "UPST", "FLNC", "UBER",
    # Semiconductors & AI Hardware
    "NVDA", "AMD", "MU", "AVGO", "MRVL", "AMAT", "LRCX", "KLAC", "INTC", "QCOM", "ON", "MPWR", "SMCI", "ARM", "TSM", "ASML",
    # High-Beta Growth / Software / Platform (Famous 2x Turnarounds & Traps)
    "META", "NFLX", "AMZN", "TSLA", "PLTR", "APP", "CVNA", "COIN", "SHOP", "SQ", "PYPL", "ROKU", "SNOW", "CRWD", "PANW", "NET", "DDOG", "ZS", "MDB", "U", "SNAP", "PINS", "SPOT", "DUOL", "HOOD", "AFRM", "SOFI",
    # Industrials / Energy / Biotech / Consumer Turnarounds & Value Traps
    "GE", "BA", "F", "GM", "CCL", "UAL", "DAL", "XOM", "OXY", "FSLR", "SEDG", "ALB", "PFE", "MRNA", "LLY", "VRTX", "REGN", "NKE", "SBUX", "DIS", "PARA", "WBD", "LULU", "DECK", "CROX"
]

KR_TICKERS = [
    "402340.KS",  # SK스퀘어
    "000660.KS",  # SK하이닉스
    "005930.KS",  # 삼성전자
    "042700.KS",  # 한미반도체
    "007660.KS",  # 이수페타시스
    "267260.KS",  # HD현대일렉트릭
    "003230.KS",  # 삼양식품
    "259960.KS",  # 크래프톤
    "034020.KS",  # 두산에너빌리티
    "012450.KS",  # 한화에어로스페이스
    "064350.KS",  # 현대로템
    "329180.KS",  # HD현대중공업
    "010140.KS",  # 삼성중공업
    "035420.KS",  # NAVER
    "035720.KS",  # 카카오
    "051910.KS",  # LG화학
    "006400.KS",  # 삼성SDI
    "373220.KS",  # LG에너지솔루션
    "003670.KS",  # 포스코퓨처엠
    "086520.KQ",  # 에코프로
    "247540.KQ",  # 에코프로비엠
    "196170.KQ",  # 알테오젠
    "068270.KS",  # 셀트리온
    "207940.KS",  # 삼성바이오로직스
    "005380.KS",  # 현대차
    "000270.KS",  # 기아
    "034730.KS",  # SK(주)
]

ALL_TICKERS = US_TICKERS + KR_TICKERS
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}

success = 0
failed = []

print(f"Fetching {len(ALL_TICKERS)} stocks from Yahoo Finance...")
for t in ALL_TICKERS:
    safe_name = t.replace(".", "_")
    csv_path = os.path.join(OUT_DIR, f"{safe_name}.csv")
    if os.path.exists(csv_path) and os.path.getsize(csv_path) > 5000:
        success += 1
        continue
    try:
        url = f"https://query1.finance.yahoo.com/v8/finance/chart/{t}?period1=946684800&period2=1999999999&interval=1d"
        r = requests.get(url, headers=headers, verify=False, timeout=12)
        if r.status_code != 200:
            failed.append((t, f"HTTP {r.status_code}"))
            continue
        data = r.json()
        res = data["chart"]["result"][0]
        timestamps = res.get("timestamp", [])
        if not timestamps:
            failed.append((t, "No timestamps"))
            continue
        quote = res["indicators"]["quote"][0]
        adjclose = res["indicators"].get("adjclose", [{}])[0].get("adjclose", quote["close"])
        dates = [datetime.fromtimestamp(ts).strftime("%Y-%m-%d") for ts in timestamps]
        df = pd.DataFrame({
            "Date": dates,
            "Open": quote.get("open"),
            "High": quote.get("high"),
            "Low": quote.get("low"),
            "Close": quote.get("close"),
            "AdjClose": adjclose,
            "Volume": quote.get("volume"),
        })
        df.dropna(subset=["Close", "AdjClose"], inplace=True)
        df = df[df["Close"] > 0]
        df.to_csv(csv_path, index=False)
        success += 1
    except Exception as e:
        failed.append((t, str(e)))
    time.sleep(0.08)

print(f"Done! Successfully fetched {success}/{len(ALL_TICKERS)} stocks. Failed: {len(failed)}")
if failed:
    print("Failed tickers:", failed)
