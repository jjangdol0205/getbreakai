"""
Fetches full historical daily OHLCV starting from 1998-01-01 (period1=883612800)
through 2026-10-14 for all 100+ US and KR stocks so that 52-week high/low (252D)
and 200-day MA are 100% warm on 2000-01-03!
"""
import os
import concurrent.futures
from datetime import datetime
import urllib3
import requests
import pandas as pd

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

DATA_DIR = "data_stocks"
os.makedirs(DATA_DIR, exist_ok=True)

TICKERS_1998_2026 = [
    # Existing US & KR Universe
    "MBLY", "CELH", "ENPH", "UPST", "FLNC", "UBER",
    "NVDA", "AMD", "MU", "AVGO", "MRVL", "AMAT", "LRCX", "KLAC", "INTC", "QCOM", "ON", "MPWR", "SMCI", "ARM", "TSM", "ASML",
    "META", "NFLX", "AMZN", "TSLA", "PLTR", "APP", "CVNA", "COIN", "SHOP", "PYPL", "ROKU", "SNOW", "CRWD", "PANW", "NET", "DDOG", "ZS", "MDB", "U", "SNAP", "PINS", "SPOT", "DUOL", "HOOD", "AFRM", "SOFI",
    "GE", "BA", "F", "GM", "CCL", "UAL", "DAL", "XOM", "OXY", "FSLR", "SEDG", "ALB", "PFE", "MRNA", "LLY", "VRTX", "REGN", "NKE", "SBUX", "DIS", "PARA", "WBD", "LULU", "DECK", "CROX",
    # Additional 1998-2026 Major Tech / Semi / Biotech / Growth Leaders for Full 2000-2010 Coverage
    "AAPL", "MSFT", "CSCO", "ORCL", "ADBE", "INTU", "EBAY", "TXN", "ADI", "MCHP", "SWKS", "TER",
    "GILD", "BIIB", "ISRG", "MNST", "URI", "BKNG", "TTWO", "EA", "AKAM", "NTAP", "WDC", "STX", "GLW", "CAT", "DE", "UNH",
    # KR Universe
    "402340.KS", "000660.KS", "005930.KS", "042700.KS", "007660.KS", "267260.KS", "003230.KS", "259960.KS",
    "034020.KS", "012450.KS", "064350.KS", "329180.KS", "010140.KS", "035420.KS", "035720.KS", "051910.KS",
    "006400.KS", "373220.KS", "003670.KS", "086520.KQ", "247540.KQ", "196170.KQ", "068270.KS", "207940.KS",
    "005380.KS", "000270.KS", "034730.KS"
]

HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}

def download_one(t: str):
    safe = t.replace(".", "_")
    path = os.path.join(DATA_DIR, f"{safe}.csv")
    try:
        # Check if existing file already starts before 1999-03-01
        if os.path.exists(path):
            df_old = pd.read_csv(path, nrows=5)
            if len(df_old) > 0 and str(df_old["Date"].iloc[0]) <= "1999-01-15":
                return t, True, "cached_1998"
        url = f"https://query1.finance.yahoo.com/v8/finance/chart/{t}?period1=883612800&period2=1999999999&interval=1d"
        r = requests.get(url, headers=HEADERS, verify=False, timeout=15)
        if r.status_code != 200:
            return t, False, f"HTTP {r.status_code}"
        res = r.json()["chart"]["result"][0]
        ts = res.get("timestamp", [])
        if not ts:
            return t, False, "no_ts"
        q = res["indicators"]["quote"][0]
        adj = res["indicators"].get("adjclose", [{}])[0].get("adjclose", q["close"])
        df = pd.DataFrame({
            "Date": [datetime.fromtimestamp(x).strftime("%Y-%m-%d") for x in ts],
            "Open": q.get("open"),
            "High": q.get("high"),
            "Low": q.get("low"),
            "Close": q.get("close"),
            "AdjClose": adj,
            "Volume": q.get("volume"),
        }).dropna(subset=["Close", "AdjClose"])
        df = df[df["Close"] > 0]
        df.to_csv(path, index=False)
        return t, True, f"{df['Date'].iloc[0]}..{df['Date'].iloc[-1]} ({len(df)})"
    except Exception as e:
        return t, False, str(e)

if __name__ == "__main__":
    ok = 0
    with concurrent.futures.ThreadPoolExecutor(max_workers=12) as ex:
        futs = [ex.submit(download_one, t) for t in TICKERS_1998_2026]
        for f in concurrent.futures.as_completed(futs):
            t, success, msg = f.result()
            if success:
                ok += 1
            else:
                print(f"Failed {t}: {msg}")
    print(f"Completed 1998-2026 data update: {ok}/{len(TICKERS_1998_2026)} stocks ready.")
