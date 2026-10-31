import os
import pandas as pd
import numpy as np

data_dir = 'data'
df_smh = pd.read_csv(os.path.join(data_dir, 'SMH.csv'))
df_xlv = pd.read_csv(os.path.join(data_dir, 'XLV.csv'))
for d in (df_smh, df_xlv):
    d['Date'] = pd.to_datetime(d['Date'])
    d.set_index('Date', inplace=True)

common = df_smh.index.intersection(df_xlv.index).sort_values()

def get_net_daily_ret(df):
    c = df.loc[common, 'Close'].astype(float)
    a = df.loc[common, 'AdjClose'].astype(float)
    pr = c.pct_change().fillna(0.0)
    tr = a.pct_change().fillna(0.0)
    div = np.maximum(0.0, tr - pr)
    return pr + div * (1.0 - 0.154), c, a

ret_smh, _, _ = get_net_daily_ret(df_smh)
ret_xlv, _, _ = get_net_daily_ret(df_xlv)

df_cum = pd.DataFrame({'SMH': (1 + ret_smh).cumprod(), 'XLV': (1 + ret_xlv).cumprod()}, index=common)
df_m = df_cum.resample('ME').last()
m_smh = df_m['SMH'].pct_change().dropna()
m_xlv = df_m['XLV'].pct_change().dropna()
m_dates = m_smh.index

# Structure of the 25억 Loan Account:
# - Total Loan = 25억 (250,000 만원)
# - Jeonse Deposit = 15억 (150,000 만원) -> 0% return, 15억 recovered at Year 8
# - Portfolio Investment = 10억 (100,000 만원) in SMH + XLV
# - Interest = 25억 * 4% simple interest * 8 years = 8억 (80,000 만원) [1억/year]
# - At Year 8 Maturity (2037 end):
#   * Option A (Full Loan Payoff without new loan): Recover 15억 Jeonse + Pay 18억 (10억 principal + 8억 interest) from Stock Account (plus 22% capital gains tax on the partial sale needed to raise 18억 cash). Hold remaining stock until 2040 (3 more years, total 11 years: 2029~2040).
#   * Option B (Refinance 10억 principal to Mortgage/Jeonse, Pay ONLY 8억 interest from Stock Account): Recover 15억 Jeonse + Refinance 10억 + Pay 8억 interest from Stock Account (plus 22% capital gains tax on partial sale to raise 8억 cash). Hold remaining stock until 2040.

def sell_for_net_cash(v1, v2, b1, b2, target_net_cash, w_target):
    """
    Sell proportionally (or to target weights) from (v1, v2) to raise `target_net_cash`
    after 0.15% transaction cost and 22% capital gains tax (with 250만원 deduction).
    Returns: remaining (v1, v2, b1, b2), shortfall (if any), tax_paid
    """
    tot = v1 + v2
    if tot <= 0:
        return 0.0, 0.0, 0.0, 0.0, target_net_cash, 0.0
    
    tot_basis = b1 + b2
    gain_ratio = max(0.0, (tot - tot_basis) / tot)
    # Effective tax + tx rate on gross sale S:
    # Net cash = S * (1 - 0.0015) - max(0, (S * gain_ratio - 250) * 0.22)
    # Solve for S:
    if tot * gain_ratio <= 250.0:
        gross_needed = target_net_cash / (1.0 - 0.0015)
    else:
        gross_needed = (target_net_cash - 250.0 * 0.22) / (1.0 - 0.0015 - gain_ratio * 0.22)
        
    if gross_needed >= tot:
        # Liquidate everything
        realized_gain = max(0.0, tot * (1.0 - 0.0015) - tot_basis)
        tax = max(0.0, (realized_gain - 250.0) * 0.22)
        net_raised = tot * (1.0 - 0.0015) - tax
        shortfall = max(0.0, target_net_cash - net_raised)
        return 0.0, 0.0, 0.0, 0.0, shortfall, tax
    else:
        frac = gross_needed / tot
        rem_tot = tot - gross_needed
        # Rebalance remaining to w_target
        v1_new = rem_tot * w_target
        v2_new = rem_tot * (1.0 - w_target)
        b1_new = b1 * (1.0 - frac)
        b2_new = b2 * (1.0 - frac)
        realized_gain = gross_needed * gain_ratio
        tax = max(0.0, (realized_gain - 250.0) * 0.22)
        return v1_new, v2_new, b1_new, b2_new, 0.0, tax

def sim_historical_25b(start_idx, n_years_total=11, w_base=0.60, w_crash=0.60, payoff_mode='18b_full'):
    # 8 years to loan maturity + 3 more years to 2040 (total 11 years from 2029 to 2040)
    n_months = n_years_total * 12
    sub_dates = m_dates[start_idx : start_idx + n_months]
    if len(sub_dates) < n_months:
        return None
    
    tx_cost = 0.0015
    cg_tax = 0.22
    init_krw = 100000.0 # 10억
    v1 = init_krw * w_base * (1.0 - tx_cost)
    v2 = init_krw * (1.0 - w_base) * (1.0 - tx_cost)
    b1 = v1; b2 = v2
    
    peak_smh = 1.0; cur_smh = 1.0
    peak_port = init_krw
    mdd_8yr = 0.0
    mdd_total = 0.0
    realized_gain_yr = 0.0
    
    val_at_8yr_pre_payoff = 0.0
    net_at_8yr_after_payoff = 0.0
    shortfall_8yr = 0.0
    
    for m_i, dt in enumerate(sub_dates):
        r1 = m_smh.loc[dt]; r2 = m_xlv.loc[dt]
        v1 *= (1.0 + r1); v2 *= (1.0 + r2)
        cur_smh *= (1.0 + r1)
        if cur_smh > peak_smh: peak_smh = cur_smh
        smh_dd = (cur_smh - peak_smh) / peak_smh
        
        tot = v1 + v2
        if tot > peak_port: peak_port = tot
        dd = (tot - peak_port) / peak_port
        if m_i < 96 and dd < mdd_8yr: mdd_8yr = dd
        if dd < mdd_total: mdd_total = dd
        
        # Annual rebalancing every 12 months
        if (m_i + 1) % 12 == 0:
            tot = v1 + v2
            w_t = w_crash if smh_dd <= -0.30 else w_base
            t1 = tot * w_t
            if v1 > t1:
                sell1 = v1 - t1
                cost1 = b1 * (sell1 / v1)
                realized_gain_yr += (sell1 - cost1)
                v1 -= sell1; b1 -= cost1
                buy2 = sell1 * (1.0 - tx_cost * 2)
                v2 += buy2; b2 += buy2
            elif v2 > (tot - t1):
                sell2 = v2 - (tot - t1)
                cost2 = b2 * (sell2 / v2)
                realized_gain_yr += (sell2 - cost2)
                v2 -= sell2; b2 -= cost2
                buy1 = sell2 * (1.0 - tx_cost * 2)
                v1 += buy1; b1 += buy1
                
            if realized_gain_yr > 250.0:
                tax = (realized_gain_yr - 250.0) * cg_tax
                tot_now = v1 + v2
                f1 = v1 / tot_now
                b1 -= b1 * (tax * f1 / v1)
                b2 -= b2 * (tax * (1 - f1) / v2)
                v1 -= tax * f1
                v2 -= tax * (1 - f1)
            realized_gain_yr = 0.0
            
        # At exact end of Year 8 (month 95, i.e., m_i == 95): Pay off Loan!
        if m_i == 95:
            val_at_8yr_pre_payoff = v1 + v2
            target_cash = 180000.0 if payoff_mode == '18b_full' else 80000.0
            v1, v2, b1, b2, shortfall_8yr, _ = sell_for_net_cash(v1, v2, b1, b2, target_cash, w_base)
            net_at_8yr_after_payoff = (v1 + v2) - shortfall_8yr
            peak_port = max(1.0, v1 + v2)
            
    final_2040 = (v1 + v2) - shortfall_8yr
    return {
        'start_dt': sub_dates[0].strftime('%Y-%m'),
        'val_8yr_pre': val_at_8yr_pre_payoff / 10000.0,
        'net_8yr_post': net_at_8yr_after_payoff / 10000.0,
        'shortfall_8yr': shortfall_8yr / 10000.0,
        'final_2040': final_2040 / 10000.0,
        'mdd_8yr': mdd_8yr
    }

configs = [
    ('SMH 60% : XLV 40%', 0.60, 0.60),
    ('SMH 65% : XLV 35%', 0.65, 0.65),
    ('SMH 70% : XLV 30%', 0.70, 0.70),
    ('역발상 (평시60%->폭락70%)', 0.60, 0.70),
]

print("==========================================================================================")
print(" [실제 구조 반영] 25억 이주비 대출 (15억 전세 + 10억 SMH+XLV, 연 4% 단리 8년 이자 = 8억)")
print(" -> 8년 뒤(2037말) 주식계좌 필요 상환액: [전액상환 시 18억(원금10+이자8)] / [대환 시 이자 8억]")
print(" -> 상환 후 남은 주식을 2040년(총 11년)까지 보유 시 60:40 vs 70:30 비교")
print("==========================================================================================")

for mode, mode_desc in [('18b_full', 'Case A: 8년차에 18억(원금10억+이자8억) 전액 상환 후 2040년까지 보유'),
                        ('8b_int_only', 'Case B: 8년차에 원금10억은 주담대 대환, 이자 8억만 상환 후 2040년까지 보유')]:
    print(f"\n--- {mode_desc} ---")
    print("1) 전체 역사적 롤링 구간 (2000~2026, 총 184개 구간, 닷컴버블·2008금융위기 포함)")
    for name, wb, wc in configs:
        res_all = [sim_historical_25b(i, 11, wb, wc, mode) for i in range(len(m_dates) - 132)]
        res_all = [r for r in res_all if r is not None]
        success_rate = np.mean([r['shortfall_8yr'] == 0 for r in res_all]) * 100
        med_8yr = np.median([r['net_8yr_post'] for r in res_all])
        p25_8yr = np.percentile([r['net_8yr_post'] for r in res_all], 25)
        med_2040 = np.median([r['final_2040'] for r in res_all])
        p25_2040 = np.percentile([r['final_2040'] for r in res_all], 25)
        p75_2040 = np.percentile([r['final_2040'] for r in res_all], 75)
        mdd_med = np.median([r['mdd_8yr'] for r in res_all]) * 100
        print(f"  {name:<24} | 8년상환성공률: {success_rate:5.1f}% | 8년차상환후잔고(중간값): {med_8yr:6.2f}억 (하위25%: {p25_8yr:5.2f}억) | 11년차(2040)잔고 중앙값: {med_2040:6.2f}억 (하위25%: {p25_2040:6.2f}억 / 상위25%: {p75_2040:6.2f}억) | 평균MDD: {mdd_med:5.1f}%")

    print("2) 2005년 이후 롤링 구간 (2005~2026, 2008 금융위기 포함)")
    start_2005 = np.where(m_dates >= '2005-01-01')[0][0]
    for name, wb, wc in configs:
        res_05 = [sim_historical_25b(i, 11, wb, wc, mode) for i in range(start_2005, len(m_dates) - 132)]
        res_05 = [r for r in res_05 if r is not None]
        success_rate = np.mean([r['shortfall_8yr'] == 0 for r in res_05]) * 100
        med_8yr = np.median([r['net_8yr_post'] for r in res_05])
        min_8yr = np.min([r['net_8yr_post'] for r in res_05])
        med_2040 = np.median([r['final_2040'] for r in res_05])
        min_2040 = np.min([r['final_2040'] for r in res_05])
        print(f"  {name:<24} | 8년상환성공률: {success_rate:5.1f}% | 8년차상환후잔고(중간값): {med_8yr:6.2f}억 (최악: {min_8yr:6.2f}억) | 11년차(2040)잔고 중앙값: {med_2040:6.2f}억 (최악: {min_2040:6.2f}억)")
