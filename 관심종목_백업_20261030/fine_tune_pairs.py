import pandas as pd
import numpy as np
from pair_engine import data, qqq, backtest_pair

target_pairs = [
    ('SMH', 'GLD'),
    ('SMH', 'IAU'),
    ('SMH', 'SCHD'),
    ('SMH', 'XLV'),
    ('SOXX', 'GLD'),
    ('SOXX', 'SCHD'),
    ('XLK', 'GLD'),
    ('SMH', 'SHY'),
    ('SMH', 'QQQ')
]

weights_fine = [0.2, 0.25, 0.3, 0.35, 0.4, 0.45, 0.5, 0.55, 0.6, 0.65, 0.7, 0.75, 0.8, 0.85]

results_all = []

for t1, t2 in target_pairs:
    if t1 not in data or t2 not in data:
        continue
    s1 = data[t1]
    s2 = data[t2]
    
    # Check max common period
    common = s1.index.intersection(s2.index).intersection(qqq.index)
    start_year = common[0].year
    
    for w1 in weights_fine:
        w2 = round(1.0 - w1, 2)
        res = backtest_pair(s1, s2, w1, w2)
        if res:
            results_all.append({
                'Pair': f'{t1}({int(w1*100)}) + {t2}({int(w2*100)})',
                'T1': t1, 'T2': t2, 'W1': w1, 'W2': w2,
                'Start': res['start_date'],
                'Years': res['years'],
                'CAGR': res['cagr_port'],
                'QQQ_CAGR': res['cagr_qqq'],
                'Diff_CAGR': res['diff_cagr'],
                'MDD': res['mdd_port'],
                'QQQ_MDD': res['mdd_qqq'],
                'Diff_MDD': res['diff_mdd'],
                'Sharpe': res['sharpe'],
                'Vol': res['vol']
            })

df_res = pd.DataFrame(results_all)
# Filter for beating QQQ on both CAGR and MDD
df_winners = df_res[(df_res['Diff_CAGR'] > 0) & (df_res['Diff_MDD'] > 0)].copy()
df_winners.sort_values(by='CAGR', ascending=False, inplace=True)

print(f'Total candidates tested: {len(df_res)}')
print(f'Total winning combinations (CAGR > QQQ and MDD < QQQ): {len(df_winners)}')
print('\n--- ALL WINNING STRATEGIES OVER FULL INCEPTION ---')
print(df_winners[['Pair', 'Start', 'Years', 'CAGR', 'QQQ_CAGR', 'Diff_CAGR', 'MDD', 'QQQ_MDD', 'Sharpe']].to_string())
