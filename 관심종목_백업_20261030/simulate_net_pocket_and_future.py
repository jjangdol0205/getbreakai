import pandas as pd
import numpy as np
from simulate_user_plan import m_dates, m_ret_smh, m_ret_xlv

def sim_part1_full_tax(start_ym, n_years=10, init_krw=40000, monthly_wd=300, w1_target=0.60, delay_months=0):
    sub_idx = m_dates[m_dates >= pd.to_datetime(start_ym)][:n_years*12]
    tx_cost = 0.0015
    cg_tax_rate = 0.22
    v1 = init_krw * w1_target * (1 - tx_cost)
    v2 = init_krw * (1 - w1_target) * (1 - tx_cost)
    b1 = v1; b2 = v2
    
    yearly_log = []
    total_wd_pocket = 0.0
    total_cg_tax_paid = 0.0
    min_bal = init_krw
    realized_gain_this_year = 0.0
    
    for m_i, dt in enumerate(sub_idx):
        r1 = m_ret_smh.loc[dt]; r2 = m_ret_xlv.loc[dt]
        v1 *= (1.0 + r1); v2 *= (1.0 + r2)
        
        if m_i >= delay_months:
            tot = v1 + v2
            if tot <= monthly_wd:
                v1 = 0; v2 = 0; break
            cur_w1 = v1 / tot
            if cur_w1 >= w1_target:
                excess1 = v1 - (tot - monthly_wd) * w1_target
                take1 = min(monthly_wd, max(0.0, excess1))
                take2 = monthly_wd - take1
            else:
                excess2 = v2 - (tot - monthly_wd) * (1 - w1_target)
                take2 = min(monthly_wd, max(0.0, excess2))
                take1 = monthly_wd - take2
                
            if take1 > 0:
                gross_sell1 = take1 * (1 + tx_cost)
                frac1 = min(1.0, gross_sell1 / v1)
                cost1 = b1 * frac1
                realized_gain_this_year += (take1 - cost1)
                v1 -= gross_sell1; b1 -= cost1
            if take2 > 0:
                gross_sell2 = take2 * (1 + tx_cost)
                frac2 = min(1.0, gross_sell2 / v2)
                cost2 = b2 * frac2
                realized_gain_this_year += (take2 - cost2)
                v2 -= gross_sell2; b2 -= cost2
            total_wd_pocket += monthly_wd
            
        # Annual rebalance + Annual Capital Gains Tax settlement (above 250만원 deduction)
        if (m_i + 1) % 12 == 0:
            tot = v1 + v2
            diff1 = v1 - tot * w1_target
            if abs(diff1) > tot * 0.02:
                if diff1 > 0:
                    frac = diff1 / v1
                    cost_sold = b1 * frac
                    realized_gain_this_year += (diff1 - cost_sold)
                    cost = diff1 * tx_cost * 2
                    v1 -= diff1; b1 -= cost_sold
                    v2 += (diff1 - cost); b2 += (diff1 - cost)
                else:
                    sell2 = -diff1
                    frac = sell2 / v2
                    cost_sold = b2 * frac
                    realized_gain_this_year += (sell2 - cost_sold)
                    cost = sell2 * tx_cost * 2
                    v2 -= sell2; b2 -= cost_sold
                    v1 += (sell2 - cost); b1 += (sell2 - cost)
                    
            # Pay annual capital gains tax out of portfolio (22% above 250만원 basic deduction)
            taxable = max(0.0, realized_gain_this_year - 250.0)
            cg_tax = taxable * cg_tax_rate
            if cg_tax > 0 and (v1 + v2) > cg_tax:
                tot_now = v1 + v2
                f1 = v1 / tot_now
                v1 -= cg_tax * f1; b1 -= b1 * (cg_tax * f1 / (v1 + cg_tax * f1))
                v2 -= cg_tax * (1 - f1); b2 -= b2 * (cg_tax * (1 - f1) / (v2 + cg_tax * (1 - f1)))
                total_cg_tax_paid += cg_tax
            realized_gain_this_year = 0.0
            yearly_log.append(((m_i+1)//12, dt.strftime('%Y-%m'), total_wd_pocket, total_cg_tax_paid, v1 + v2))
            
        min_bal = min(min_bal, v1 + v2)
    return yearly_log, total_wd_pocket, total_cg_tax_paid, v1 + v2, min_bal

print("=== [FULL AFTER-TAX POCKET 300만원/월] 최근 10년 (2016.10 ~ 2026.10) ===")
log_t, wd_t, tax_t, fin_t, min_t = sim_part1_full_tax('2016-10-01', n_years=10, delay_months=0)
for yr, ym, wd, tx, bal in log_t:
    print(f"  {yr:2d}년차 ({ym}) | 실수령 누적: {wd:6,.0f}만 | 누적 납부 양도세: {tx:5,.0f}만 | 세후 계좌 잔고: {bal:8,.0f}만 ({bal/10000:.2f}억)")

_, _, _, fin_t_delay, _ = sim_part1_full_tax('2016-10-01', n_years=10, delay_months=15)
print(f"--> SK스퀘어 버퍼로 15개월 인출 유예 시 10년 후 세후 잔고: {fin_t_delay:,.0f}만 원 ({fin_t_delay/10000:.2f}억 원, +{fin_t_delay - fin_t:,.0f}만 원 이득!)")

# Rolling 10Y with full annual CG tax
start_candidates = m_dates[(m_dates >= '2005-01-01') & (m_dates <= '2016-10-31')]
finals_net = np.array([sim_part1_full_tax(sc.strftime('%Y-%m-%d'), n_years=10, delay_months=0)[3] for sc in start_candidates])
finals_mod = np.array([sim_part1_full_tax(sc.strftime('%Y-%m-%d'), n_years=10, delay_months=0)[3] for sc in m_dates[(m_dates >= '2011-01-01') & (m_dates <= '2016-10-31')]])
print(f"\n2005~2026 롤링 10년 세후 잔고: 하위25% {np.percentile(finals_net,25)/10000:.2f}억 | 중위값 {np.median(finals_net)/10000:.2f}억 | 상위25% {np.percentile(finals_net,75)/10000:.2f}억")
print(f"2011~2026 롤링 10년 세후 잔고: 최악 {np.min(finals_mod)/10000:.2f}억 | 중위값 {np.median(finals_mod)/10000:.2f}억 | 상위25% {np.percentile(finals_mod,75)/10000:.2f}억")
