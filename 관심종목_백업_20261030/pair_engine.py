import os
import itertools
import pandas as pd
import numpy as np

# Load all ETF daily data
data_dir = 'data'
files = [f for f in os.listdir(data_dir) if f.endswith('.csv')]

data = {}
for f in files:
    ticker = f.replace('.csv', '')
    df = pd.read_csv(os.path.join(data_dir, f))
    df['Date'] = pd.to_datetime(df['Date'])
    df.set_index('Date', inplace=True)
    data[ticker] = df['AdjClose'].sort_index()

qqq = data['QQQ']

def backtest_pair(s1, s2, w1, w2, start_year=None):
    # Find common index
    common_idx = s1.index.intersection(s2.index).intersection(qqq.index)
    if start_year:
        common_idx = common_idx[common_idx.year >= start_year]
    
    if len(common_idx) < 252 * 5: # At least 5 years
        return None
    
    p1 = s1.loc[common_idx]
    p2 = s2.loc[common_idx]
    pq = qqq.loc[common_idx]
    
    # Identify rebalancing dates: first trading day of each year
    years = common_idx.year
    rebalance_mask = np.zeros(len(common_idx), dtype=bool)
    rebalance_mask[0] = True
    for i in range(1, len(common_idx)):
        if years[i] != years[i-1]:
            rebalance_mask[i] = True
            
    rebalance_indices = np.where(rebalance_mask)[0]
    
    # Portfolio simulation
    n = len(common_idx)
    port_val = np.zeros(n)
    port_val[0] = 10000.0
    
    sh1 = (port_val[0] * w1) / p1.iloc[0]
    sh2 = (port_val[0] * w2) / p2.iloc[0]
    
    for i in range(1, n):
        if rebalance_mask[i]:
            current_val = sh1 * p1.iloc[i] + sh2 * p2.iloc[i]
            port_val[i] = current_val
            sh1 = (current_val * w1) / p1.iloc[i]
            sh2 = (current_val * w2) / p2.iloc[i]
        else:
            port_val[i] = sh1 * p1.iloc[i] + sh2 * p2.iloc[i]
            
    # QQQ buy and hold value
    qqq_val = 10000.0 * (pq / pq.iloc[0]).values
    
    total_years = (common_idx[-1] - common_idx[0]).days / 365.25
    if total_years <= 0:
        return None
        
    cagr_port = (port_val[-1] / port_val[0]) ** (1 / total_years) - 1
    cagr_qqq = (qqq_val[-1] / qqq_val[0]) ** (1 / total_years) - 1
    
    # MDD calculation
    peak_port = np.maximum.accumulate(port_val)
    dd_port = (port_val - peak_port) / peak_port
    mdd_port = dd_port.min()
    
    peak_qqq = np.maximum.accumulate(qqq_val)
    dd_qqq = (qqq_val - peak_qqq) / peak_qqq
    mdd_qqq = dd_qqq.min()
    
    # Daily returns for Sharpe
    daily_ret = np.diff(port_val) / port_val[:-1]
    vol_port = np.std(daily_ret) * np.sqrt(252)
    sharpe = (cagr_port - 0.02) / vol_port if vol_port > 0 else 0
    
    return {
        'start_date': common_idx[0].strftime('%Y-%m-%d'),
        'end_date': common_idx[-1].strftime('%Y-%m-%d'),
        'years': round(total_years, 1),
        'cagr_port': cagr_port,
        'cagr_qqq': cagr_qqq,
        'diff_cagr': cagr_port - cagr_qqq,
        'mdd_port': mdd_port,
        'mdd_qqq': mdd_qqq,
        'diff_mdd': mdd_port - mdd_qqq, # Positive means port MDD is shallower (e.g. -30% vs -35% => +0.05)
        'sharpe': sharpe,
        'vol': vol_port
    }

print('Script loaded.')
