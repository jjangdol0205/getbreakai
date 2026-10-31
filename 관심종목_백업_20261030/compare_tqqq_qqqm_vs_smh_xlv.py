import os
import pandas as pd
import numpy as np
from compare_25b_loan_60_vs_70 import sell_for_net_cash

data_dir = 'data'
df_qqq = pd.read_csv(os.path.join(data_dir, 'QQQ.csv'))
df_smh = pd.read_csv(os.path.join(data_dir, 'SMH.csv'))
df_xlv = pd.read_csv(os.path.join(data_dir, 'XLV.csv'))
for d in (df_qqq, df_smh, df_xlv):
    d['Date'] = pd.to_datetime(d['Date'])
    d.set_index('Date', inplace=True)

common = df_qqq.index.intersection(df_smh.index).intersection(df_xlv.index).sort_values()

def get_daily_tr(df):
    a = df.loc[common, 'AdjClose'].astype(float)
    c = df.loc[common, 'Close'].astype(float)
    pr = c.pct_change().fillna(0.0)
    tr = a.pct_change().fillna(0.0)
    div = np.maximum(0.0, tr - pr)
    return pr, div, pr + div * (1 - 0.154)

pr_q, div_q, net_q = get_daily_tr(df_qqq)
pr_s, div_s, net_s = get_daily_tr(df_smh)
pr_x, div_x, net_x = get_daily_tr(df_xlv)
ret_tqqq = 3.0 * pr_q - (0.045 / 252.0)

df_daily = pd.DataFrame({
    'QQQM': (1 + net_q).cumprod(),
    'TQQQ': (1 + ret_tqqq).cumprod(),
    'SMH': (1 + net_s).cumprod(),
    'XLV': (1 + net_x).cumprod(),
    'QQQ_vol20': pr_q.rolling(21).std() * np.sqrt(252)
}, index=common).dropna()

df_m = df_daily.resample('ME').last()
m_qqqm = df_m['QQQM'].pct_change().dropna()
m_tqqq = df_m['TQQQ'].pct_change().dropna()
m_smh = df_m['SMH'].pct_change().dropna()
m_xlv = df_m['XLV'].pct_change().dropna()
m_vol = df_m['QQQ_vol20'].loc[m_qqqm.index]
m_dates = m_qqqm.index

def get_tqqq_weight(vol_q, target_vol=0.28, max_tqqq=0.50):
    L = target_vol / max(0.08, vol_q)
    return float(np.clip((L - 1.0) / 2.0, 0.0, max_tqqq))

def sim_acct1_compare(start_idx, mode='tq_vol'):
    sub = m_dates[start_idx : start_idx + 168]
    if len(sub) < 168: return None
    tx = 0.0015; cg = 0.22
    w_init = get_tqqq_weight(m_vol.loc[sub[0]]) if mode == 'tq_vol' else 0.60
    v1 = 40000.0 * w_init * (1 - tx); v2 = 40000.0 * (1 - w_init) * (1 - tx)
    b1 = v1; b2 = v2; rg = 0.0
    pk = 40000.0; mdd = 0.0
    for i, dt in enumerate(sub):
        if mode == 'tq_vol':
            v1 *= (1 + m_tqqq.loc[dt]); v2 *= (1 + m_qqqm.loc[dt])
        else:
            v1 *= (1 + m_smh.loc[dt]); v2 *= (1 + m_xlv.loc[dt])
        tot = v1 + v2
        if tot <= 300.0:
            v1 = 0.0; v2 = 0.0; mdd = -1.0; break
        wt = get_tqqq_weight(m_vol.loc[dt]) if mode == 'tq_vol' else 0.60
        ex1 = v1 - (tot - 300.0) * wt
        tk1 = min(300.0, max(0.0, ex1)); tk2 = 300.0 - tk1
        if tk1 > 0 and v1 > 0:
            gs1 = tk1*(1+tx); f1 = min(1.0, gs1/v1); c1 = b1*f1; rg += (tk1-c1); v1 -= gs1; b1 -= c1
        if tk2 > 0 and v2 > 0:
            gs2 = tk2*(1+tx); f2 = min(1.0, gs2/v2); c2 = b2*f2; rg += (tk2-c2); v2 -= gs2; b2 -= c2
        tot = v1 + v2
        if mode == 'tq_vol' or (i + 1) % 12 == 0:
            t1 = tot * wt
            if v1 > t1:
                s1 = v1 - t1; c1 = b1*(s1/v1); rg += (s1-c1); v1 -= s1; b1 -= c1; buy2 = s1*0.997; v2 += buy2; b2 += buy2
            elif v2 > (tot - t1):
                s2 = v2 - (tot - t1); c2 = b2*(s2/v2); rg += (s2-c2); v2 -= s2; b2 -= c2; buy1 = s2*0.997; v1 += buy1; b1 += buy1
        if (i + 1) % 12 == 0:
            if rg > 250.0:
                tax = (rg - 250.0)*cg; tn = v1 + v2
                if tn > tax:
                    f1 = v1/tn
                    if v1 > 0: b1 -= b1*(tax*f1/v1); v1 -= tax*f1
                    if v2 > 0: b2 -= b2*(tax*(1-f1)/v2); v2 -= tax*(1-f1)
            rg = 0.0
        tot = v1 + v2
        if tot > pk: pk = tot
        dd = (tot - pk)/pk
        if dd < mdd: mdd = dd
    return {'final': (v1 + v2)/10000.0, 'mdd': mdd, 'depleted': (v1 + v2) == 0}

def sim_acct2_compare(start_idx, mode='tq_vol'):
    sub = m_dates[start_idx : start_idx + 132]
    if len(sub) < 132: return None
    tx = 0.0015; cg = 0.22
    w_init = get_tqqq_weight(m_vol.loc[sub[0]]) if mode == 'tq_vol' else 0.60
    v1 = 100000.0 * w_init * (1 - tx); v2 = 100000.0 * (1 - w_init) * (1 - tx)
    b1 = v1; b2 = v2; rg = 0.0
    pk = 100000.0; mdd8 = 0.0; sf = 0.0
    for i, dt in enumerate(sub):
        if mode == 'tq_vol':
            v1 *= (1 + m_tqqq.loc[dt]); v2 *= (1 + m_qqqm.loc[dt])
        else:
            v1 *= (1 + m_smh.loc[dt]); v2 *= (1 + m_xlv.loc[dt])
        tot = v1 + v2
        wt = get_tqqq_weight(m_vol.loc[dt]) if mode == 'tq_vol' else 0.60
        if (mode == 'tq_vol' or (i + 1) % 12 == 0) and tot > 0:
            t1 = tot * wt
            if v1 > t1:
                s1 = v1 - t1; c1 = b1*(s1/v1); rg += (s1-c1); v1 -= s1; b1 -= c1; buy2 = s1*0.997; v2 += buy2; b2 += buy2
            elif v2 > (tot - t1):
                s2 = v2 - (tot - t1); c2 = b2*(s2/v2); rg += (s2-c2); v2 -= s2; b2 -= c2; buy1 = s2*0.997; v1 += buy1; b1 += buy1
        if (i + 1) % 12 == 0:
            if rg > 250.0 and (v1 + v2) > 0:
                tax = (rg - 250.0)*cg; tn = v1 + v2
                if tn > tax:
                    f1 = v1/tn
                    if v1 > 0: b1 -= b1*(tax*f1/v1); v1 -= tax*f1
                    if v2 > 0: b2 -= b2*(tax*(1-f1)/v2); v2 -= tax*(1-f1)
            rg = 0.0
        tot = v1 + v2
        if tot > pk: pk = tot
        dd = (tot - pk)/pk
        if i < 96 and dd < mdd8: mdd8 = dd
        if i == 95:
            v1, v2, b1, b2, sf, _ = sell_for_net_cash(v1, v2, b1, b2, 180000.0, wt)
    return {'final': ((v1 + v2) - sf)/10000.0, 'sf': sf/10000.0, 'mdd8': mdd8}

for label, s_yr in [('2000~2026 전체 (닷컴+금융위기 포함)', '2000-06-01'), ('2005~2026 (금융위기 포함)', '2005-01-01')]:
    s_idx = np.where(m_dates >= s_yr)[0][0]
    r1_tq = [sim_acct1_compare(i, 'tq_vol') for i in range(s_idx, len(m_dates)-168)]
    r1_sx = [sim_acct1_compare(i, 'smh_xlv') for i in range(s_idx, len(m_dates)-168)]
    print(f"\n=== [계좌 1: 4억 + 월 300만 원 인출 (14년)] {label} ===")
    print(f"  TQQQ+QQQM(월변동성): 고갈확률 {np.mean([x['depleted'] for x in r1_tq])*100:5.1f}% | 최악잔고 {np.min([x['final'] for x in r1_tq]):5.2f}억 | 하위25% {np.percentile([x['final'] for x in r1_tq],25):5.2f}억 | 중앙값 {np.median([x['final'] for x in r1_tq]):6.2f}억 | 평균MDD {np.median([x['mdd'] for x in r1_tq])*100:5.1f}%")
    print(f"  SMH60+XLV40(연1회) : 고갈확률 {np.mean([x['depleted'] for x in r1_sx])*100:5.1f}% | 최악잔고 {np.min([x['final'] for x in r1_sx]):5.2f}억 | 하위25% {np.percentile([x['final'] for x in r1_sx],25):5.2f}억 | 중앙값 {np.median([x['final'] for x in r1_sx]):6.2f}억 | 평균MDD {np.median([x['mdd'] for x in r1_sx])*100:5.1f}%")

    r2_tq = [sim_acct2_compare(i, 'tq_vol') for i in range(s_idx, len(m_dates)-132)]
    r2_sx = [sim_acct2_compare(i, 'smh_xlv') for i in range(s_idx, len(m_dates)-132)]
    print(f"=== [계좌 2: 10억 -> 8년 차 18억 상환 -> 11년] {label} ===")
    print(f"  TQQQ+QQQM(월변동성): 18억완납성공률 {np.mean([x['sf']==0 for x in r2_tq])*100:5.1f}% | 최악잔고 {np.min([x['final'] for x in r2_tq]):+6.2f}억 | 하위25% {np.percentile([x['final'] for x in r2_tq],25):+6.2f}억 | 중앙값 {np.median([x['final'] for x in r2_tq]):+6.2f}억 | 8년MDD {np.median([x['mdd8'] for x in r2_tq])*100:5.1f}%")
    print(f"  SMH60+XLV40(연1회) : 18억완납성공률 {np.mean([x['sf']==0 for x in r2_sx])*100:5.1f}% | 최악잔고 {np.min([x['final'] for x in r2_sx]):+6.2f}억 | 하위25% {np.percentile([x['final'] for x in r2_sx],25):+6.2f}억 | 중앙값 {np.median([x['final'] for x in r2_sx]):+6.2f}억 | 8년MDD {np.median([x['mdd8'] for x in r2_sx])*100:5.1f}%")
