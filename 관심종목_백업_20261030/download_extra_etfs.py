import os
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
import requests
import pandas as pd
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed

extra_tickers = [
    # Tech & Growth
    'IGV', 'FTEC', 'IXN', 'IGM', 'SPMO', 'PDP', 'RPG', 'SPYG', 'IWY', 'OEF', 'XLG', 'ONEQ',
    # Defense, Insurance, Healthcare sub-sectors, Homebuilders
    'ITA', 'PPA', 'XAR', 'ITB', 'XHB', 'KIE', 'IAK', 'IHI', 'IHF', 'PPH',
    # Dividend, Value, Buyback
    'PKW', 'SDY', 'DVY', 'HDV', 'FDL', 'DHS', 'DLN', 'DON', 'RPV', 'PRF', 'VTV', 'IWD',
    # Treasury STRIPS, Dollar, Alternatives, Commodities
    'EDV', 'ZROZ', 'TLH', 'DBA', 'DBB', 'DBE', 'BTAL', 'UUP', 'FXF', 'FXY', 'PDBC', 'KMLM', 'CTA'
]

os.makedirs('data', exist_ok=True)
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}

def fetch_one(t):
    path = f'data/{t}.csv'
    if os.path.exists(path):
        return (t, 'exists', 0)
    try:
        url = f'https://query1.finance.yahoo.com/v8/finance/chart/{t}?period1=0&period2=1999999999&interval=1d'
        r = requests.get(url, headers=headers, verify=False, timeout=15)
        if r.status_code != 200:
            return (t, f'HTTP {r.status_code}', 0)
        data = r.json()
        result = data['chart']['result'][0]
        timestamps = result['timestamp']
        quote = result['indicators']['quote'][0]
        adjclose = result['indicators'].get('adjclose', [{}])[0].get('adjclose', quote['close'])
        dates = [datetime.fromtimestamp(ts).strftime('%Y-%m-%d') for ts in timestamps]
        df = pd.DataFrame({'Date': dates, 'Close': quote['close'], 'AdjClose': adjclose})
        df.dropna(subset=['AdjClose'], inplace=True)
        df.to_csv(path, index=False)
        return (t, f'{df["Date"].iloc[0]} ~ {df["Date"].iloc[-1]}', len(df))
    except Exception as e:
        return (t, f'ERR: {e}', 0)

with ThreadPoolExecutor(max_workers=8) as ex:
    futures = [ex.submit(fetch_one, t) for t in extra_tickers]
    for f in as_completed(futures):
        t, msg, rows = f.result()
        print(f'{t:6s}: {msg} ({rows} rows)')
