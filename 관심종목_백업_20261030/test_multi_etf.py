import pandas as pd
import numpy as np
from detailed_metrics import load_series, qqq

def backtest_multi(weights_dict, start_date='2011-10-20'):
    tickers = list(weights_dict.keys())
    series_list = [load_series(t) for t in tickers]
    
    common_idx = qqq.index
    for s in series_list:
        common_idx = common_idx.intersection(s.index)
        
    common_idx = common_idx[common_idx >= pd.to_datetime(start_date)]
    
    prices = pd.DataFrame({t: load_series(t).loc[common_idx] for t in tickers})
    pq = qqq.loc[common_idx]
    
    n = len(common_idx)
    years = common_idx.year
    rebalance_mask = np.zeros(n, dtype=bool)
    rebalance_mask[0] = True
    for i in range(1, n):
        if years[i] != years[i-1]:
            rebalance_mask[i] = True
            
    port_val = np.zeros(n)
    port_val[0] = 10000.0
    shares = {t: (port_val[0] * weights_dict[t]) / prices[t].iloc[0] for t in tickers}
    
    for i in range(1, n):
        if rebalance_mask[i]:
            current_val = sum(shares[t] * prices[t].iloc[i] for t in tickers)
            port_val[i] = current_val
            for t in tickers:
                shares[t] = (current_val * weights_dict[t]) / prices[t].iloc[i]
        else:
            port_val[i] = sum(shares[t] * prices[t].iloc[i] for t in tickers)
            
    total_years = (common_idx[-1] - common_idx[0]).days / 365.25
    cagr = (port_val[-1] / port_val[0]) ** (1 / total_years) - 1
    
    peak = np.maximum.accumulate(port_val)
    mdd = ((port_val - peak) / peak).min()
    
    daily_ret = np.diff(port_val) / port_val[:-1]
    vol = np.std(daily_ret) * np.sqrt(252)
    sharpe = (cagr - 0.02) / vol if vol > 0 else 0
    
    return {
        'weights': weights_dict,
        'final_val': port_val[-1],
        'cagr': cagr,
        'mdd': mdd,
        'vol': vol,
        'sharpe': sharpe,
        'calmar': cagr / abs(mdd)
    }

portfolios = [
    # 1 Asset (Pure Benchmark / Pure Alpha)
    {'QQQ': 1.0},
    {'SMH': 1.0},
    
    # 2 Assets (Baseline)
    {'SMH': 0.60, 'SCHD': 0.40},
    {'SMH': 0.70, 'GLD': 0.30},
    {'SMH': 0.60, 'GLD': 0.40},
    
    # 3 Assets
    {'SMH': 0.50, 'QQQ': 0.20, 'SCHD': 0.30},
    {'SMH': 0.50, 'SCHD': 0.30, 'GLD': 0.20},
    {'SMH': 0.60, 'SCHD': 0.20, 'GLD': 0.20},
    {'SMH': 0.50, 'XLK': 0.20, 'SCHD': 0.30},
    
    # 4 Assets
    {'SMH': 0.40, 'QQQ': 0.20, 'SCHD': 0.20, 'GLD': 0.20},
    {'SMH': 0.50, 'QQQ': 0.20, 'SCHD': 0.20, 'GLD': 0.10},
    {'SMH': 0.40, 'XLK': 0.20, 'SCHD': 0.20, 'GLD': 0.20},
    
    # 5 Assets
    {'SMH': 0.35, 'QQQ': 0.20, 'XLK': 0.15, 'SCHD': 0.15, 'GLD': 0.15},
    {'SMH': 0.40, 'QQQ': 0.20, 'SCHD': 0.20, 'GLD': 0.10, 'BIL': 0.10}
]

records = []
for p in portfolios:
    res = backtest_multi(p, start_date='2011-10-20')
    label = ' + '.join([f'{k}({int(v*100)}%)' for k, v in p.items()])
    n_assets = len(p)
    records.append({
        'N': n_assets,
        'Portfolio': label,
        'Final ($10k)': f"${res['final_val']:,.0f}",
        'CAGR': f"{res['cagr']:.2%}",
        'MDD': f"{res['mdd']:.2%}",
        'Sharpe': f"{res['sharpe']:.2f}",
        'Calmar': f"{res['calmar']:.2f}"
    })

df_res = pd.DataFrame(records)
print(df_res.to_string(index=False))
