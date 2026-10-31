import os
import itertools
import pandas as pd
import numpy as np
from detailed_metrics import load_series, qqq
from test_multi_etf import backtest_multi

data_dir = 'data'
files = [f for f in os.listdir(data_dir) if f.endswith('.csv')]
all_tickers = sorted([f.replace('.csv', '') for f in files])

# Baseline: SMH 60% + SCHD 40% since 2011-10-20
baseline_res = backtest_multi({'SMH': 0.60, 'SCHD': 0.40}, start_date='2011-10-20')
b_cagr = baseline_res['cagr']
b_mdd = baseline_res['mdd']
b_sharpe = baseline_res['sharpe']
b_calmar = baseline_res['calmar']

print(f"=== BASELINE: SMH 60% + SCHD 40% (2011 ~ 2026) ===")
print(f"CAGR: {b_cagr:.2%}, MDD: {b_mdd:.2%}, Sharpe: {b_sharpe:.2f}, Calmar: {b_calmar:.2f}, Final: ${baseline_res['final_val']:,.0f}\n")

# 1. Test all 1-ETF portfolios
single_results = []
for t in all_tickers:
    try:
        res = backtest_multi({t: 1.0}, start_date='2011-10-20')
        single_results.append({
            'ETF': t,
            'CAGR': res['cagr'],
            'MDD': res['mdd'],
            'Sharpe': res['sharpe'],
            'Calmar': res['calmar'],
            'Final': res['final_val']
        })
    except Exception:
        pass

df_single = pd.DataFrame(single_results)

# 2. Test all 2-ETF pairs
pairs = list(itertools.combinations(all_tickers, 2))
print(f"Evaluating {len(pairs)} pairs with fine weights...")

weights = [0.5, 0.55, 0.6, 0.65, 0.7, 0.75, 0.8, 0.85]

pair_results = []

for t1, t2 in pairs:
    s1 = load_series(t1)
    s2 = load_series(t2)
    common = s1.index.intersection(s2.index).intersection(qqq.index)
    common = common[common >= pd.to_datetime('2011-10-20')]
    # Require data from 2011-10-20 (or within 2011)
    if len(common) == 0 or common[0].year > 2012:
        continue
        
    start_str = common[0].strftime('%Y-%m-%d')
    
    for w1 in weights:
        w2 = round(1.0 - w1, 2)
        try:
            res = backtest_multi({t1: w1, t2: w2}, start_date=start_str)
            if res is None:
                continue
                
            pair_results.append({
                'T1': t1, 'T2': t2, 'W1': w1, 'W2': w2,
                'Start': start_str,
                'CAGR': res['cagr'],
                'MDD': res['mdd'],
                'Sharpe': res['sharpe'],
                'Calmar': res['calmar'],
                'Final': res['final_val']
            })
        except Exception:
            pass

df_pairs = pd.DataFrame(pair_results)
print(f"Total valid 2-ETF backtests completed: {len(df_pairs)}")

# Filter for:
# Category 1: Beating baseline on BOTH CAGR and MDD (Strict Dominance)
dom = df_pairs[(df_pairs['CAGR'] > b_cagr) & (abs(df_pairs['MDD']) < abs(b_mdd))].copy()
dom.sort_values(by='CAGR', ascending=False, inplace=True)

# Category 2: Higher CAGR with MDD <= -35% (QQQ level MDD)
high_cagr = df_pairs[(df_pairs['CAGR'] > b_cagr) & (abs(df_pairs['MDD']) <= 0.3512)].copy()
high_cagr.sort_values(by='CAGR', ascending=False, inplace=True)

# Category 3: Higher Sharpe than baseline (Sharpe > 0.957)
high_sharpe = df_pairs[df_pairs['Sharpe'] > b_sharpe].copy()
high_sharpe.sort_values(by='Sharpe', ascending=False, inplace=True)

# Category 4: Higher Calmar than baseline (Calmar > 0.717)
high_calmar = df_pairs[df_pairs['Calmar'] > b_calmar].copy()
high_calmar.sort_values(by='Calmar', ascending=False, inplace=True)

print(f"\n--- Category 1: Strict Dominance (CAGR > {b_cagr:.2%} AND MDD < {abs(b_mdd):.2%}) ---")
print(f"Found {len(dom)} combinations:")
if len(dom) > 0:
    for _, r in dom.head(15).iterrows():
        print(f"{r['T1']}({int(r['W1']*100)}) + {r['T2']}({int(r['W2']*100)}) | CAGR: {r['CAGR']:.2%} (+{r['CAGR']-b_cagr:.2%}) | MDD: {r['MDD']:.2%} ({abs(b_mdd)-abs(r['MDD']):.2%} better) | Sharpe: {r['Sharpe']:.2f}")

print(f"\n--- Category 2: Higher CAGR with MDD <= QQQ (-35.12%) ---")
for _, r in high_cagr.head(15).iterrows():
    print(f"{r['T1']}({int(r['W1']*100)}) + {r['T2']}({int(r['W2']*100)}) | CAGR: {r['CAGR']:.2%} | MDD: {r['MDD']:.2%} | Sharpe: {r['Sharpe']:.2f} | Final: ${r['Final']:,.0f}")

print(f"\n--- Category 3: Higher Sharpe Ratio (> {b_sharpe:.2f}) ---")
for _, r in high_sharpe.head(15).iterrows():
    print(f"{r['T1']}({int(r['W1']*100)}) + {r['T2']}({int(r['W2']*100)}) | Sharpe: {r['Sharpe']:.2f} | CAGR: {r['CAGR']:.2%} | MDD: {r['MDD']:.2%}")
