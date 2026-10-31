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

tickers = ["NVDA", "MU", "AVGO", "AMD", "TSM", "ASML", "ARM", "SOXX", "QQQ", "EWY", "KRW=X", "NFLX", "CELH", "UPST", "FSLR"]
rows = []
for t in tickers:
    try:
        url = f"https://query1.finance.yahoo.com/v8/finance/chart/{t}?range=10d&interval=1d"
        r = requests.get(url, headers=HEADERS, verify=False, timeout=6).json()["chart"]["result"][0]
        ts = r["timestamp"]
        c = r["indicators"]["quote"][0]["close"]
        valid = [(datetime.fromtimestamp(x).strftime("%Y-%m-%d"), y) for x, y in zip(ts, c) if y is not None]
        if len(valid) >= 2:
            d_cur, p_cur = valid[-1]
            d_prev, p_prev = valid[-2]
            chg = (p_cur / p_prev - 1.0) * 100.0
            rows.append({"Ticker": t, "Date": d_cur, "Prev": round(p_prev, 2), "Close": round(p_cur, 2), "Chg_Pct": round(chg, 2)})
    except Exception as e:
        pass

print("=== OVERNIGHT US & GLOBAL SEMI CLOSE ===")
print(pd.DataFrame(rows).to_string(index=False))

# Also calculate SK Square (402340.KS) intraday scenarios today (2026-10-15) if SK Hynix drops -4% ~ -7%
sk_close = 852000.0
hy_close = 1419000.0
print("\n=== TODAY (2026-10-15) SK SQUARE (402340.KS) & SK HYNIX SCENARIOS ===")
for drop_pct in [-3.0, -4.0, -5.0, -6.0, -7.0, -8.0]:
    sk_p = round(sk_close * (1.0 + drop_pct / 100.0), -3)
    hy_p = round(hy_close * (1.0 + drop_pct / 100.0), -3)
    val_76 = sk_p * 76 / 10000.0
    pnl_pct = (sk_p / 1090000.0 - 1.0) * 100.0
    vs_floor = (sk_p / 780000.0 - 1.0) * 100.0
    print(f"Scenario {drop_pct:+.1f}%: SK스퀘어 {sk_p:,.0f}원 (SK하이닉스 {hy_p:,.0f}원) | 76주 평가액: {val_76:,.1f}만 원 ({pnl_pct:+.2f}%) | 78만 지지선 대비: {vs_floor:+.2f}%")
