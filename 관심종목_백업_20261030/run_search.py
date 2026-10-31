import os
import itertools
import pandas as pd
import numpy as np
from pair_engine import data, qqq, backtest_pair

all_tickers = sorted(list(data.keys()))
print(f'Total available ETFs: {len(all_tickers)}')

# Generate all 2-ETF combinations
pairs = list(itertools.combinations(all_tickers, 2))
print(f'Total pairs to evaluate: {len(pairs)}')

weights = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]

def search_period(start_year, label):
    print(f'\n========================================')
    print(f'Evaluating for period starting {start_year} ({label})...')
    print(f'========================================')
    
    winning_candidates = []
    
    for t1, t2 in pairs:
        s1 = data[t1]
        s2 = data[t2]
        
        # Check if both have data for this period
        common = s1.index.intersection(s2.index).intersection(qqq.index)
        if start_year:
            common = common[common.year >= start_year]
            if len(common) == 0 or common[0].year > start_year:
                continue
        
        for w1 in weights:
            w2 = round(1.0 - w1, 2)
            res = backtest_pair(s1, s2, w1, w2, start_year=start_year)
            if res is None:
                continue
            
            # Constraint check:
            # 1. CAGR > QQQ CAGR
            # 2. MDD better (shallower) than QQQ MDD (diff_mdd > 0)
            if res['diff_cagr'] > 0 and res['diff_mdd'] > 0:
                winning_candidates.append({
                    'ETF1': t1,
                    'ETF2': t2,
                    'W1': w1,
                    'W2': w2,
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
                
    win_df = pd.DataFrame(winning_candidates)
    if len(win_df) == 0:
        print(f'No combination beat QQQ on BOTH CAGR and MDD for {label}.')
        return win_df
        
    print(f'Found {len(win_df)} winning combinations for {label}!')
    
    # Sort by CAGR
    win_df.sort_values(by='CAGR', ascending=False, inplace=True)
    print('\n--- Top 15 by CAGR (Outperforming QQQ with LOWER MDD) ---')
    print(win_df[['ETF1', 'ETF2', 'W1', 'W2', 'CAGR', 'QQQ_CAGR', 'Diff_CAGR', 'MDD', 'QQQ_MDD', 'Sharpe']].head(15).to_string())
    
    # Sort by Sharpe
    win_df.sort_values(by='Sharpe', ascending=False, inplace=True)
    print('\n--- Top 10 by Sharpe Ratio ---')
    print(win_df[['ETF1', 'ETF2', 'W1', 'W2', 'CAGR', 'QQQ_CAGR', 'MDD', 'QQQ_MDD', 'Sharpe']].head(10).to_string())
    
    return win_df

# Run for 2005 (21+ years)
res_2005 = search_period(2005, '2005 to 2026 (21+ years, GFC + Covid + 2022)')
# Run for 2011 (15+ years)
res_2011 = search_period(2011, '2011 to 2026 (15+ years, Modern Bull + 2020 + 2022)')
# Run for 2001 (25+ years)
res_2001 = search_period(2001, '2001 to 2026 (25+ years)')
