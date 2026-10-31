import pandas as pd
import numpy as np
from verify_top5_champions import series_dict, eval_one_pair

def get_daily_curve(t1, t2, w1, start_date_str='2011-10-20'):
    start_dt = pd.to_datetime(start_date_str)
    s1 = series_dict[t1]
    s2 = series_dict[t2]
    qqq = series_dict['QQQ']
    common = s1.index.intersection(s2.index).intersection(qqq.index)
    common = common[common >= start_dt]
    p1 = s1.loc[common].values.astype(np.float64)
    p2 = s2.loc[common].values.astype(np.float64)
    years = common.year.values
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
    return pd.Series(val, index=common)

base_curve = get_daily_curve('SMH', 'SCHD', 0.60, '2011-10-20')
qqq_curve = get_daily_curve('QQQ', 'QQQ', 1.00, '2011-10-20')

candidates = [
    ('SMH(60%) + XLV(40%)', 'SMH', 'XLV', 0.60),
    ('SMH(65%) + XLV(35%)', 'SMH', 'XLV', 0.65),
    ('SMH(80%) + UUP(20%)', 'SMH', 'UUP', 0.80),
    ('SMH(75%) + UUP(25%)', 'SMH', 'UUP', 0.75),
    ('SMH(80%) + BTAL(20%)', 'SMH', 'BTAL', 0.80),
    ('SMH(70%) + PPA(30%)', 'SMH', 'PPA', 0.70),
    ('SMH(60%) + BRK-B(40%)', 'SMH', 'BRK-B', 0.60),
]

print("=== ROLLING 3Y & 5Y WIN RATES (2011 ~ 2026) ===")
for label, t1, t2, w1 in candidates:
    c = get_daily_curve(t1, t2, w1, '2011-10-20')
    c_3y = (c / c.shift(252*3))**(1/3) - 1
    b_3y = (base_curve / base_curve.shift(252*3))**(1/3) - 1
    q_3y = (qqq_curve / qqq_curve.shift(252*3))**(1/3) - 1
    
    c_5y = (c / c.shift(252*5))**(1/5) - 1
    b_5y = (base_curve / base_curve.shift(252*5))**(1/5) - 1
    q_5y = (qqq_curve / qqq_curve.shift(252*5))**(1/5) - 1
    
    win_b_3y = (c_3y.dropna() > b_3y.dropna()).mean()
    win_b_5y = (c_5y.dropna() > b_5y.dropna()).mean()
    win_q_5y = (c_5y.dropna() > q_5y.dropna()).mean()
    print(f"{label:24s} | Beat SMH+SCHD (3Y): {win_b_3y:5.1%} | Beat SMH+SCHD (5Y): {win_b_5y:5.1%} | Beat QQQ (5Y): {win_q_5y:5.1%}")

print("\n=== LONG-TERM TRACK RECORD INCLUDING 2008 GFC (2007-03 ~ 2026-10, 19.6 Yrs) ===")
for label, t1, t2, w1 in [
    ('Benchmark: QQQ(100%)', 'QQQ', 'QQQ', 1.00),
    ('SMH(60%) + XLV(40%)', 'SMH', 'XLV', 0.60),
    ('SMH(65%) + XLV(35%)', 'SMH', 'XLV', 0.65),
    ('SMH(80%) + UUP(20%)', 'SMH', 'UUP', 0.80),
    ('SMH(75%) + UUP(25%)', 'SMH', 'UUP', 0.75),
    ('SMH(70%) + PPA(30%)', 'SMH', 'PPA', 0.70),
    ('SMH(60%) + BRK-B(40%)', 'SMH', 'BRK-B', 0.60),
    ('SMH(70%) + IAU(30%)', 'SMH', 'IAU', 0.70),
]:
    fv, cagr, mdd, vol, sh, so, cal = eval_one_pair(t1, t2, w1, '2007-03-05')
    print(f"{label:24s} | CAGR: {cagr:6.2%} | MDD: {mdd:7.2%} | Sharpe: {sh:.3f} | Sortino: {so:.3f} | Final: ${fv:,.0f}")
