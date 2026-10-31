import os
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
import requests
import pandas as pd
import numpy as np
from datetime import datetime
from verify_top5_champions import series_dict, eval_one_pair

bonus_tickers = ['BRK-B', 'GDX', 'GRID', 'NLR', 'CIBR']
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}

for t in bonus_tickers:
    path = f'data/{t}.csv'
    if not os.path.exists(path):
        url = f'https://query1.finance.yahoo.com/v8/finance/chart/{t}?period1=0&period2=1999999999&interval=1d'
        r = requests.get(url, headers=headers, verify=False, timeout=15)
        if r.status_code == 200:
            res = r.json()['chart']['result'][0]
            ts = res['timestamp']
            quote = res['indicators']['quote'][0]
            adj = res['indicators'].get('adjclose', [{}])[0].get('adjclose', quote['close'])
            df = pd.DataFrame({'Date': [datetime.fromtimestamp(x).strftime('%Y-%m-%d') for x in ts], 'Close': quote['close'], 'AdjClose': adj}).dropna(subset=['AdjClose'])
            df.to_csv(path, index=False)
            df['Date'] = pd.to_datetime(df['Date'])
            df.set_index('Date', inplace=True)
            series_dict[t] = df['AdjClose'].sort_index()

for t in ['BRK-B', 'GDX', 'GRID', 'NLR']:
    if t in series_dict:
        for w1 in [0.55, 0.60, 0.65, 0.70]:
            fv, cagr, mdd, vol, sh, so, cal = eval_one_pair('SMH', t, w1, '2011-10-20')
            print(f"SMH({int(w1*100)}%) + {t}({int(round((1-w1)*100))}%) | CAGR: {cagr:.2%} | MDD: {mdd:.2%} | Sharpe: {sh:.3f} | Sortino: {so:.3f} | Calmar: {cal:.3f} | Final: ${fv:,.0f}")
