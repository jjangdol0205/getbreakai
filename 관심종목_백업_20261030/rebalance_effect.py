import pandas as pd
import numpy as np
from detailed_metrics import load_series, qqq

def test_rebalancing_bonus(t1, t2, w1, w2, start_date):
    s1 = load_series(t1)
    s2 = load_series(t2)
    common_idx = s1.index.intersection(s2.index).intersection(qqq.index)
    if start_date:
        common_idx = common_idx[common_idx >= pd.to_datetime(start_date)]
    
    p1 = s1.loc[common_idx]
    p2 = s2.loc[common_idx]
    
    # 1. With Annual Rebalancing
    n = len(common_idx)
    years = common_idx.year
    rebalance_mask = np.zeros(n, dtype=bool)
    rebalance_mask[0] = True
    for i in range(1, n):
        if years[i] != years[i-1]:
            rebalance_mask[i] = True
            
    val_reb = np.zeros(n)
    val_reb[0] = 10000.0
    sh1 = (val_reb[0] * w1) / p1.iloc[0]
    sh2 = (val_reb[0] * w2) / p2.iloc[0]
    
    for i in range(1, n):
        if rebalance_mask[i]:
            cur = sh1 * p1.iloc[i] + sh2 * p2.iloc[i]
            val_reb[i] = cur
            sh1 = (cur * w1) / p1.iloc[i]
            sh2 = (cur * w2) / p2.iloc[i]
        else:
            val_reb[i] = sh1 * p1.iloc[i] + sh2 * p2.iloc[i]
            
    # 2. Buy and Hold (No Rebalance)
    sh1_bh = (10000.0 * w1) / p1.iloc[0]
    sh2_bh = (10000.0 * w2) / p2.iloc[0]
    val_bh = sh1_bh * p1.values + sh2_bh * p2.values
    
    total_years = (common_idx[-1] - common_idx[0]).days / 365.25
    cagr_reb = (val_reb[-1] / val_reb[0]) ** (1 / total_years) - 1
    cagr_bh = (val_bh[-1] / val_bh[0]) ** (1 / total_years) - 1
    
    dd_reb = (val_reb - np.maximum.accumulate(val_reb)) / np.maximum.accumulate(val_reb)
    mdd_reb = dd_reb.min()
    
    dd_bh = (val_bh - np.maximum.accumulate(val_bh)) / np.maximum.accumulate(val_bh)
    mdd_bh = dd_bh.min()
    
    print(f'=== {t1} ({w1:.0%}) + {t2} ({w2:.0%}) since {start_date} ===')
    print(f'Annual Rebalancing: Final ${val_reb[-1]:,.0f} | CAGR: {cagr_reb:.2%} | MDD: {mdd_reb:.2%}')
    print(f'Buy & Hold (No Reb): Final ${val_bh[-1]:,.0f} | CAGR: {cagr_bh:.2%} | MDD: {mdd_bh:.2%}')
    print(f'Rebalancing Effect:   MDD improvement: {abs(mdd_bh) - abs(mdd_reb):.2%}p safer drawdown!')
    print(f'Final Weight without Rebalancing: {t1} grew to {(sh1_bh*p1.iloc[-1])/val_bh[-1]:.1%}, {t2} dropped to {(sh2_bh*p2.iloc[-1])/val_bh[-1]:.1%}!\n')

test_rebalancing_bonus('SMH', 'GLD', 0.7, 0.3, '2005-01-01')
test_rebalancing_bonus('SMH', 'SCHD', 0.6, 0.4, '2011-10-20')
