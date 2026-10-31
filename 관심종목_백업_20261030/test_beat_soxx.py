import pandas as pd
import numpy as np
from detailed_metrics import load_series
from test_multi_etf import backtest_multi

# Benchmark is SOXX
soxx_res = backtest_multi({'SOXX': 1.0}, start_date='2011-10-20')
print('=== BENCHMARK: SOXX (2011 ~ 2026) ===')
print(f"CAGR: {soxx_res['cagr']:.2%}, MDD: {soxx_res['mdd']:.2%}, Vol: {soxx_res['vol']:.2%}, Sharpe: {soxx_res['sharpe']:.2f}, Final: ${soxx_res['final_val']:,.0f}")

candidates = [
    {'SOXX': 1.0},
    {'SMH': 1.0},
    {'SMH': 0.90, 'SCHD': 0.10},
    {'SMH': 0.85, 'SCHD': 0.15},
    {'SMH': 0.80, 'SCHD': 0.20},
    {'SMH': 0.70, 'SCHD': 0.30},
    {'SMH': 0.60, 'SCHD': 0.40},
    
    {'SMH': 0.90, 'GLD': 0.10},
    {'SMH': 0.85, 'GLD': 0.15},
    {'SMH': 0.80, 'GLD': 0.20},
    {'SMH': 0.70, 'GLD': 0.30},
    
    {'SMH': 0.85, 'QQQ': 0.15},
    {'SMH': 0.80, 'XLK': 0.20},
]

records = []
for p in candidates:
    res = backtest_multi(p, start_date='2011-10-20')
    label = ' + '.join([f'{k}({int(v*100)}%)' for k, v in p.items()])
    
    beat_cagr = res['cagr'] > soxx_res['cagr']
    beat_mdd = abs(res['mdd']) < abs(soxx_res['mdd'])
    beat_sharpe = res['sharpe'] > soxx_res['sharpe']
    
    status = 'Beat BOTH' if (beat_cagr and beat_mdd) else ('CAGR only' if beat_cagr else ('MDD/Sharpe only' if beat_mdd else 'None'))
    
    records.append({
        'Portfolio': label,
        'CAGR': f"{res['cagr']:.2%}",
        'Diff_CAGR': f"{res['cagr'] - soxx_res['cagr']:+.2%}",
        'MDD': f"{res['mdd']:.2%}",
        'Diff_MDD': f"{abs(soxx_res['mdd']) - abs(res['mdd']):+.2%}",
        'Sharpe': f"{res['sharpe']:.2f}",
        'Final ($10k)': f"${res['final_val']:,.0f}",
        'Result vs SOXX': status
    })

df = pd.DataFrame(records)
print('\n=== COMPARISON WITH SOXX (2011 ~ 2026) ===')
print(df.to_string(index=False))
