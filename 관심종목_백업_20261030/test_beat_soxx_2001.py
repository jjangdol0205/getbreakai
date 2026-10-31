import pandas as pd
import numpy as np
from detailed_metrics import load_series
from test_multi_etf import backtest_multi

# Benchmark is SOXX since 2001-07-13
soxx_res_2001 = backtest_multi({'SOXX': 1.0}, start_date='2001-07-13')
print('=== BENCHMARK: SOXX (2001 ~ 2026, 25.3 Years) ===')
print(f"CAGR: {soxx_res_2001['cagr']:.2%}, MDD: {soxx_res_2001['mdd']:.2%}, Vol: {soxx_res_2001['vol']:.2%}, Sharpe: {soxx_res_2001['sharpe']:.2f}, Final: ${soxx_res_2001['final_val']:,.0f}")

candidates_2001 = [
    {'SOXX': 1.0},
    {'SMH': 1.0},
    {'SMH': 0.85, 'QQQ': 0.15},
    {'SMH': 0.80, 'XLK': 0.20},
    {'SMH': 0.70, 'XLV': 0.30},
    {'SMH': 0.60, 'XLV': 0.40},
    {'SMH': 0.70, 'GLD': 0.30}, # GLD starts 2004-11
]

records = []
for p in candidates_2001:
    res = backtest_multi(p, start_date='2001-07-13')
    label = ' + '.join([f'{k}({int(v*100)}%)' for k, v in p.items()])
    
    beat_cagr = res['cagr'] > soxx_res_2001['cagr']
    beat_mdd = abs(res['mdd']) < abs(soxx_res_2001['mdd'])
    
    status = 'Beat BOTH' if (beat_cagr and beat_mdd) else ('CAGR only' if beat_cagr else ('MDD/Sharpe only' if beat_mdd else 'None'))
    
    records.append({
        'Portfolio': label,
        'CAGR': f"{res['cagr']:.2%}",
        'Diff_CAGR': f"{res['cagr'] - soxx_res_2001['cagr']:+.2%}",
        'MDD': f"{res['mdd']:.2%}",
        'Diff_MDD': f"{abs(soxx_res_2001['mdd']) - abs(res['mdd']):+.2%}",
        'Sharpe': f"{res['sharpe']:.2f}",
        'Final ($10k)': f"${res['final_val']:,.0f}",
        'Result vs SOXX': status
    })

df = pd.DataFrame(records)
print('\n=== COMPARISON WITH SOXX (2001 ~ 2026, 25.3 Years) ===')
print(df.to_string(index=False))
