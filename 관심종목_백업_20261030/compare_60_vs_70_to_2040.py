import os
import pandas as pd
import numpy as np

data_dir = 'data'
df_smh = pd.read_csv(os.path.join(data_dir, 'SMH.csv'))
df_xlv = pd.read_csv(os.path.join(data_dir, 'XLV.csv'))
df_qqq = pd.read_csv(os.path.join(data_dir, 'QQQ.csv'))
for d in (df_smh, df_xlv, df_qqq):
    d['Date'] = pd.to_datetime(d['Date'])
    d.set_index('Date', inplace=True)

common = df_smh.index.intersection(df_xlv.index).intersection(df_qqq.index).sort_values()

def get_net_daily_ret(df):
    c = df.loc[common, 'Close'].astype(float)
    a = df.loc[common, 'AdjClose'].astype(float)
    pr = c.pct_change().fillna(0.0)
    tr = a.pct_change().fillna(0.0)
    div = np.maximum(0.0, tr - pr)
    return pr + div * (1.0 - 0.154), c, a

ret_smh, c_smh, a_smh = get_net_daily_ret(df_smh)
ret_xlv, c_xlv, a_xlv = get_net_daily_ret(df_xlv)

df_cum = pd.DataFrame({'SMH': (1 + ret_smh).cumprod(), 'XLV': (1 + ret_xlv).cumprod()}, index=common)
df_m = df_cum.resample('ME').last()
m_smh = df_m['SMH'].pct_change().dropna()
m_xlv = df_m['XLV'].pct_change().dropna()
m_dates = m_smh.index

# 1. Compare 60:40 vs 65:35 vs 70:30 vs Dynamic (60->70 / 60->75) over 14-Year Horizon (2027~2040 length = 14 yrs)
def sim_14yr_window(start_dt_idx, w_base=0.60, w_crash=0.60, monthly_wd=0.0, init_krw=40000.0):
    # 14 years = 168 months
    sub_dates = m_dates[start_dt_idx : start_dt_idx + 168]
    if len(sub_dates) < 168:
        return None
    tx_cost = 0.0015
    cg_tax_rate = 0.22
    v1 = init_krw * w_base * (1 - tx_cost)
    v2 = init_krw * (1 - w_base) * (1 - tx_cost)
    b1 = v1; b2 = v2
    
    peak_tot = v1 + v2
    mdd = 0.0
    min_bal = v1 + v2
    realized_gain_yr = 0.0
    smh_12m_window = []
    
    for m_i, dt in enumerate(sub_dates):
        r1 = m_smh.loc[dt]; r2 = m_xlv.loc[dt]
        v1 *= (1.0 + r1); v2 *= (1.0 + r2)
        smh_12m_window.append(1.0 + r1)
        if len(smh_12m_window) > 12:
            smh_12m_window.pop(0)
            
        # Monthly withdrawal (Smart Withdrawal from overweight asset)
        if monthly_wd > 0:
            tot = v1 + v2
            if tot <= monthly_wd:
                return {'final': 0.0, 'mdd': -1.0, 'min_bal': 0.0, 'cagr': -1.0}
            cur_w1 = v1 / tot
            if cur_w1 >= w_base:
                excess1 = v1 - (tot - monthly_wd) * w_base
                take1 = min(monthly_wd, max(0.0, excess1))
                take2 = monthly_wd - take1
            else:
                excess2 = v2 - (tot - monthly_wd) * (1 - w_base)
                take2 = min(monthly_wd, max(0.0, excess2))
                take1 = monthly_wd - take2
            if take1 > 0:
                gs1 = take1 * (1 + tx_cost)
                f1 = min(1.0, gs1 / v1)
                c1_sold = b1 * f1
                realized_gain_yr += (take1 - c1_sold)
                v1 -= gs1; b1 -= c1_sold
            if take2 > 0:
                gs2 = take2 * (1 + tx_cost)
                f2 = min(1.0, gs2 / v2)
                c2_sold = b2 * f2
                realized_gain_yr += (take2 - c2_sold)
                v2 -= gs2; b2 -= c2_sold
                
        # Annual rebalance every 12 months
        if (m_i + 1) % 12 == 0:
            tot = v1 + v2
            # Check if SMH had a -15% or worse 12-month return (or drawdown)
            ret_12m_smh = np.prod(smh_12m_window) - 1.0
            w_target = w_crash if ret_12m_smh <= -0.15 else w_base
            diff1 = v1 - tot * w_target
            if abs(diff1) > tot * 0.02:
                if diff1 > 0:
                    f1 = diff1 / v1
                    c_sold = b1 * f1
                    realized_gain_yr += (diff1 - c_sold)
                    cost = diff1 * tx_cost * 2
                    v1 -= diff1; b1 -= c_sold
                    v2 += (diff1 - cost); b2 += (diff1 - cost)
                else:
                    s2 = -diff1
                    f2 = s2 / v2
                    c_sold = b2 * f2
                    realized_gain_yr += (s2 - c_sold)
                    cost = s2 * tx_cost * 2
                    v2 -= s2; b2 -= c_sold
                    v1 += (s2 - cost); b1 += (s2 - cost)
            # Settle annual capital gains tax above 250만원
            taxable = max(0.0, realized_gain_yr - 250.0)
            cg_tax = taxable * cg_tax_rate
            if cg_tax > 0 and (v1 + v2) > cg_tax:
                tot_now = v1 + v2
                f1 = v1 / tot_now
                v1 -= cg_tax * f1; b1 *= (1.0 - (cg_tax * f1) / (v1 + cg_tax * f1))
                v2 -= cg_tax * (1 - f1); b2 *= (1.0 - (cg_tax * (1 - f1)) / (v2 + cg_tax * (1 - f1)))
            realized_gain_yr = 0.0
            
        tot_now = v1 + v2
        peak_tot = max(peak_tot, tot_now)
        dd_now = (tot_now - peak_tot) / peak_tot
        mdd = min(mdd, dd_now)
        min_bal = min(min_bal, tot_now)
        
    final_val = v1 + v2
    cagr = (final_val / init_krw) ** (1.0 / 14.0) - 1.0
    return {'final': final_val, 'mdd': mdd, 'min_bal': min_bal, 'cagr': cagr}

configs = [
    ('SMH 60% : XLV 40% (고정)', 0.60, 0.60),
    ('SMH 65% : XLV 35% (고정)', 0.65, 0.65),
    ('SMH 70% : XLV 30% (고정)', 0.70, 0.70),
    ('SMH 60% -> 폭락시 70% (스위칭)', 0.60, 0.70),
    ('SMH 60% -> 폭락시 75% (스위칭)', 0.60, 0.75),
]

print("=== [1] 거치식(인출 없음, 10억 기준) 14년(2027~2040 길이) 롤링 백테스트 (2000~2026 전 구간, 148개 윈도우) ===")
for name, wb, wc in configs:
    res_all = [sim_14yr_window(i, wb, wc, monthly_wd=0.0, init_krw=100000.0) for i in range(len(m_dates) - 168)]
    res_mod = [sim_14yr_window(i, wb, wc, monthly_wd=0.0, init_krw=100000.0) for i in range(len(m_dates) - 168) if m_dates[i].year >= 2009]
    f_all = np.array([r['final']/10000.0 for r in res_all])
    mdd_all = np.array([r['mdd'] for r in res_all])
    f_mod = np.array([r['final']/10000.0 for r in res_mod])
    mdd_mod = np.array([r['mdd'] for r in res_mod])
    print(f"{name:28s} | 전체14년 중위: {np.median(f_all):5.1f}억 (최악 {np.min(f_all):4.1f}억, 평균MDD {np.mean(mdd_all):6.1%}) | 최근14년 중위: {np.median(f_mod):5.1f}억 (최악 {np.min(f_mod):5.1f}억, 최악MDD {np.min(mdd_mod):6.1%})")

print("\n=== [2] 월 300만 원 인출 계좌(4억 시작, 14년간 총 5.04억 인출) 롤링 백테스트 (2000~2026 전 구간) ===")
for name, wb, wc in configs:
    res_all = [sim_14yr_window(i, wb, wc, monthly_wd=300.0, init_krw=40000.0) for i in range(len(m_dates) - 168) if m_dates[i].year >= 2004]
    res_mod = [sim_14yr_window(i, wb, wc, monthly_wd=300.0, init_krw=40000.0) for i in range(len(m_dates) - 168) if m_dates[i].year >= 2009]
    f_all = np.array([r['final']/10000.0 for r in res_all])
    min_all = np.array([r['min_bal']/10000.0 for r in res_all])
    f_mod = np.array([r['final']/10000.0 for r in res_mod])
    min_mod = np.array([r['min_bal']/10000.0 for r in res_mod])
    print(f"{name:28s} | 2004~ 중위잔고: {np.median(f_all):5.1f}억 (하위10% {np.percentile(f_all,10):4.2f}억, 과정중 최저잔고 중위 {np.median(min_all):4.2f}억) | 2009~ 중위잔고: {np.median(f_mod):5.1f}억 (최악 {np.min(f_mod):5.1f}억)")
