import os
import pandas as pd
import numpy as np

data_dir = 'data'
files = [f for f in os.listdir(data_dir) if f.endswith('.csv')]
series_dict = {}
for f in sorted(files):
    ticker = f.replace('.csv', '')
    df = pd.read_csv(os.path.join(data_dir, f))
    df['Date'] = pd.to_datetime(df['Date'])
    df.set_index('Date', inplace=True)
    series_dict[ticker] = df['AdjClose'].sort_index()

def eval_one_pair(t1, t2, w1, start_date_str='2011-10-20'):
    start_dt = pd.to_datetime(start_date_str)
    s1 = series_dict[t1]
    s2 = series_dict[t2]
    qqq = series_dict['QQQ']
    common = s1.index.intersection(s2.index).intersection(qqq.index)
    common = common[common >= start_dt]
    
    p1 = s1.loc[common].values.astype(np.float64)
    p2 = s2.loc[common].values.astype(np.float64)
    years = common.year.values
    total_years = (common[-1] - common[0]).days / 365.25
    
    n = len(common)
    val = np.zeros(n, dtype=np.float64)
    val[0] = 10000.0
    w2 = 1.0 - w1
    sh1 = (val[0] * w1) / p1[0]
    sh2 = (val[0] * w2) / p2[0]
    
    for i in range(1, n):
        cur = sh1 * p1[i] + sh2 * p2[i]
        val[i] = cur
        if years[i] != years[i-1]:
            sh1 = (cur * w1) / p1[i]
            sh2 = (cur * w2) / p2[i]
            
    cagr = (val[-1] / val[0]) ** (1.0 / total_years) - 1.0
    peak = np.maximum.accumulate(val)
    mdd = ((val - peak) / peak).min()
    dret = np.diff(val) / val[:-1]
    vol = np.std(dret) * np.sqrt(252)
    sharpe = (cagr - 0.02) / vol
    neg = dret[dret < 0]
    sortino = (cagr - 0.02) / (np.std(neg) * np.sqrt(252))
    calmar = cagr / abs(mdd)
    return val[-1], cagr, mdd, vol, sharpe, sortino, calmar

champions = [
    ('Baseline: SMH(60%) + SCHD(40%)', 'SMH', 'SCHD', 0.60),
    ('Benchmark: QQQ(100%)', 'QQQ', 'QQQ', 1.00),
    ('Champ 1A: SMH(60%) + XLV(40%) [Healthcare]', 'SMH', 'XLV', 0.60),
    ('Champ 1B: SMH(65%) + XLV(35%) [Healthcare]', 'SMH', 'XLV', 0.65),
    ('Champ 2A: SMH(80%) + UUP(20%) [US Dollar]', 'SMH', 'UUP', 0.80),
    ('Champ 2B: SMH(75%) + UUP(25%) [US Dollar]', 'SMH', 'UUP', 0.75),
    ('Champ 3A: SMH(80%) + BTAL(20%) [Anti-Beta]', 'SMH', 'BTAL', 0.80),
    ('Champ 3B: SMH(75%) + BTAL(25%) [Anti-Beta]', 'SMH', 'BTAL', 0.75),
    ('Champ 4A: SMH(65%) + PPA(35%) [Defense]', 'SMH', 'PPA', 0.65),
    ('Champ 4B: SMH(70%) + PPA(30%) [Defense]', 'SMH', 'PPA', 0.70),
    ('Champ 5A: SMH(75%) + FDL(25%) [Div Leader]', 'SMH', 'FDL', 0.75),
    ('Champ 5B: SMH(70%) + HDV(30%) [High Div]', 'SMH', 'HDV', 0.70),
    ('Champ 6:  SMH(70%) + IAU(30%) [Gold]', 'SMH', 'IAU', 0.70),
]

rows = []
for name, t1, t2, w1 in champions:
    fv, cagr, mdd, vol, sh, so, cal = eval_one_pair(t1, t2, w1, '2011-10-20')
    rows.append({
        'Strategy': name,
        'CAGR': f"{cagr:.2%}",
        'MDD': f"{mdd:.2%}",
        'Vol': f"{vol:.2%}",
        'Sharpe': f"{sh:.3f}",
        'Sortino': f"{so:.3f}",
        'Calmar': f"{cal:.3f}",
        'Final ($10k)': f"${fv:,.0f}"
    })

print("=== HEAD-TO-HEAD SUMMARY (2011-10-20 ~ 2026-10-13, 15.0 Yrs) ===")
print(pd.DataFrame(rows).to_string(index=False))

def get_2022_return(t1, t2, w1):
    s1 = series_dict[t1].loc['2022-01-01':'2022-12-31']
    s2 = series_dict[t2].loc['2022-01-01':'2022-12-31']
    common = s1.index.intersection(s2.index)
    p1 = s1.loc[common].values
    p2 = s2.loc[common].values
    val = w1 * (p1 / p1[0]) + (1.0 - w1) * (p2 / p2[0])
    ret_2022 = val[-1] - 1.0
    peak = np.maximum.accumulate(val)
    mdd_2022 = ((val - peak) / peak).min()
    return ret_2022, mdd_2022

print("\n=== 2022 BEAR MARKET STRESS TEST (2022-01 ~ 2022-12) ===")
for name, t1, t2, w1 in champions:
    r22, mdd22 = get_2022_return(t1, t2, w1)
    print(f"{name:44s} | 2022 Return: {r22:>+7.2%} | 2022 Intra-year MDD: {mdd22:>7.2%}")
