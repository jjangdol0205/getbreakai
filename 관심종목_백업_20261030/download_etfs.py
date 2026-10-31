import os
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
import requests
import pandas as pd
from datetime import datetime
import time

tickers = [
    'QQQ', 'SMH', 'SOXX', 'XSD', 'PSI', 'XLK', 'VGT', 'IYW', 'QTEC', 'FDN',
    'SCHG', 'VUG', 'MGK', 'IWF', 'SPY', 'VOO', 'IVV', 'RSP',
    'QUAL', 'MTUM', 'MOAT', 'COWZ', 'SCHD', 'VIG', 'DGRO', 'VYM', 'NOBL',
    'USMV', 'SPLV', 'XLV', 'XLP', 'XLU', 'XLI', 'XLY', 'XLE', 'XLF', 'XLB',
    'VNQ', 'IYR', 'IBB', 'XBI',
    'GLD', 'IAU', 'SLV', 'TLT', 'IEF', 'SHY', 'BIL', 'BND', 'AGG', 'TIP', 'LQD', 'HYG', 'DBC'
]

os.makedirs('data', exist_ok=True)
print(f'Starting download for {len(tickers)} tickers...')

successful = []
failed = []

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}

for t in tickers:
    try:
        url = f'https://query1.finance.yahoo.com/v8/finance/chart/{t}?period1=0&period2=1999999999&interval=1d'
        r = requests.get(url, headers=headers, verify=False, timeout=15)
        if r.status_code != 200:
            print(f'{t}: HTTP {r.status_code}')
            failed.append(t)
            continue
        data = r.json()
        result = data['chart']['result'][0]
        timestamps = result['timestamp']
        quote = result['indicators']['quote'][0]
        adjclose = result['indicators'].get('adjclose', [{}])[0].get('adjclose', quote['close'])
        
        dates = [datetime.fromtimestamp(ts).strftime('%Y-%m-%d') for ts in timestamps]
        df = pd.DataFrame({
            'Date': dates,
            'Close': quote['close'],
            'AdjClose': adjclose
        })
        df.dropna(subset=['AdjClose'], inplace=True)
        df.to_csv(f'data/{t}.csv', index=False)
        successful.append(t)
        print(f'{t}: {df["Date"].iloc[0]} to {df["Date"].iloc[-1]} ({len(df)} rows)')
    except Exception as e:
        print(f'{t}: error {e}')
        failed.append(t)
    time.sleep(0.15)

print(f'Success: {len(successful)}, Failed: {len(failed)}')
