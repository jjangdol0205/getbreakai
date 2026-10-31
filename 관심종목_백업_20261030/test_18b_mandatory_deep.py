import os
import pandas as pd
import numpy as np
from compare_25b_loan_60_vs_70 import m_dates, m_smh, m_xlv, sell_for_net_cash

# Deep-dive analysis for MANDATORY 18B KRW (180,000 만원) net payoff at Year 8 (96 months),
# then holding remaining portfolio for 3 more years until 2040 (total 11 years = 132 months).

def sim_18b_mandatory(start_idx, w_base=0.60, w_crash=0.60, lock_rule='none', post_lock_w=None):
    n_months = 132 # 8 yrs (96m) + 3 yrs (36m)
    sub_dates = m_dates[start_idx : start_idx + n_months]
    if len(sub_dates) < n_months:
        return None
    if post_lock_w is None:
        post_lock_w = w_base
        
    tx_cost = 0.0015
    cg_tax = 0.22
    init_krw = 100000.0 # 10억
    v1 = init_krw * w_base * (1.0 - tx_cost)
    v2 = init_krw * (1.0 - w_base) * (1.0 - tx_cost)
    b1 = v1; b2 = v2
    
    peak_smh = 1.0; cur_smh = 1.0
    peak_port = init_krw
    mdd_8yr = 0.0
    realized_gain_yr = 0.0
    
    sgov_cash = 0.0 # Safe T-bill bucket (earns ~3.4% net/yr -> 0.28%/mo)
    sgov_rate_mo = (1.034 ** (1/12)) - 1.0
    locked_stage = 0 # 0: none, 1: half locked, 2: full 18B locked
    
    ever_able_to_pay_18b = False
    
    for m_i, dt in enumerate(sub_dates):
        r1 = m_smh.loc[dt]; r2 = m_xlv.loc[dt]
        v1 *= (1.0 + r1); v2 *= (1.0 + r2)
        if sgov_cash > 0:
            sgov_cash *= (1.0 + sgov_rate_mo)
            
        cur_smh *= (1.0 + r1)
        if cur_smh > peak_smh: peak_smh = cur_smh
        smh_dd = (cur_s_dd := (cur_smh - peak_smh) / peak_smh)
        
        tot_all = v1 + v2 + sgov_cash
        if tot_all > peak_port: peak_port = tot_all
        dd = (tot_all - peak_port) / peak_port
        if m_i < 96 and dd < mdd_8yr: mdd_8yr = dd
        
        # Check if current liquidation value >= 18억 during Years 1..8
        if m_i < 96:
            tot_eq = v1 + v2
            gain_eq = max(0.0, tot_eq - (b1 + b2))
            net_eq = tot_eq * (1 - tx_cost) - max(0.0, (gain_eq - 250.0) * cg_tax)
            if net_eq + sgov_cash >= 180000.0:
                ever_able_to_pay_18b = True
                
            # Check Lock-in triggers (monthly check from Year 4 to Year 7.9, i.e., m_i in 36..94)
            if lock_rule == 'lock_at_23b_net' and locked_stage == 0 and m_i >= 36:
                # Discount 180,000 back from month 95 to current month m_i at sgov_rate_mo
                months_left = 95 - m_i
                pv_18b = 180000.0 / ((1.0 + sgov_rate_mo) ** months_left)
                # Lock if after locking pv_18b, at least 50,000 (5억) equity remains as growth seed!
                if net_eq >= pv_18b + 50000.0:
                    v1, v2, b1, b2, sf, _ = sell_for_net_cash(v1, v2, b1, b2, pv_18b, post_lock_w)
                    sgov_cash += (pv_18b - sf)
                    locked_stage = 2
            elif lock_rule == 'lock_at_21b_net' and locked_stage == 0 and m_i >= 48:
                months_left = 95 - m_i
                pv_18b = 180000.0 / ((1.0 + sgov_rate_mo) ** months_left)
                if net_eq >= pv_18b + 30000.0:
                    v1, v2, b1, b2, sf, _ = sell_for_net_cash(v1, v2, b1, b2, pv_18b, post_lock_w)
                    sgov_cash += (pv_18b - sf)
                    locked_stage = 2

        # Annual rebalancing on equity sleeve
        if (m_i + 1) % 12 == 0:
            tot = v1 + v2
            if tot > 0:
                w_curr_base = post_lock_w if locked_stage == 2 else w_base
                w_curr_crash = max(post_lock_w, w_crash) if locked_stage == 2 else w_crash
                w_t = w_curr_crash if smh_dd <= -0.30 else w_curr_base
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
                    if tot_now > tax:
                        f1 = v1 / tot_now
                        b1 -= b1 * (tax * f1 / v1)
                        b2 -= b2 * (tax * (1 - f1) / v2)
                        v1 -= tax * f1
                        v2 -= tax * (1 - f1)
            realized_gain_yr = 0.0
            
        # Mandatory 18억 (180,000만원) payoff at end of Year 8 (m_i == 95)
        if m_i == 95:
            val_8yr_pre = v1 + v2 + sgov_cash
            need_from_eq = max(0.0, 180000.0 - sgov_cash)
            surplus_sgov = max(0.0, sgov_cash - 180000.0)
            sgov_cash = 0.0
            if need_from_eq > 0:
                v1, v2, b1, b2, shortfall_8yr, _ = sell_for_net_cash(v1, v2, b1, b2, need_from_eq, post_lock_w)
            else:
                shortfall_8yr = 0.0
                v1 += surplus_sgov * post_lock_w; b1 += surplus_sgov * post_lock_w
                v2 += surplus_sgov * (1.0 - post_lock_w); b2 += surplus_sgov * (1.0 - post_lock_w)
            net_8yr_post = (v1 + v2) - shortfall_8yr
            
    final_2040 = (v1 + v2) - shortfall_8yr
    return {
        'val_8yr_pre': val_8yr_pre / 10000.0,
        'net_8yr_post': net_8yr_post / 10000.0,
        'shortfall_8yr': shortfall_8yr / 10000.0,
        'final_2040': final_2040 / 10000.0,
        'mdd_8yr': mdd_8yr,
        'ever_18b': ever_able_to_pay_18b
    }

start_2005 = np.where(m_dates >= '2005-01-01')[0][0]
print("=== [2005~2026 롤링 구간] 입주 시 18억(원금10+이자8) 전액 의무 상환 조건: 60% vs 70% 및 Lock-in 효과 ===")
for lock_r, lock_desc in [('none', '기본 (만기일 일시상환)'), ('lock_at_21b_net', '안심잠금 (5~7년차 세후21억 도달시 18억 SGOV 확정후 70:30)')]:
    print(f"\n▶ 운용방식: {lock_desc}")
    for name, wb, wc in [
        ('SMH 60% : XLV 40% 고정', 0.60, 0.60),
        ('SMH 65% : XLV 35% 고정', 0.65, 0.65),
        ('SMH 70% : XLV 30% 고정', 0.70, 0.70),
        ('역발상 (평시60% -> 폭락70%)', 0.60, 0.70),
    ]:
        res = [sim_18b_mandatory(i, wb, wc, lock_r, post_lock_w=0.70) for i in range(start_2005, len(m_dates) - 132)]
        res = [r for r in res if r is not None]
        succ = np.mean([r['shortfall_8yr'] == 0 for r in res]) * 100
        med_8 = np.median([r['net_8yr_post'] for r in res])
        p20_8 = np.percentile([r['net_8yr_post'] for r in res], 20)
        min_8 = np.min([r['net_8yr_post'] for r in res])
        med_11 = np.median([r['final_2040'] for r in res])
        p20_11 = np.percentile([r['final_2040'] for r in res], 20)
        mdd = np.median([r['mdd_8yr'] for r in res]) * 100
        print(f"  {name:<24} | 18억상환성공률: {succ:5.1f}% | 8년차상환후 중앙값:{med_8:+6.2f}억 (하위20%:{p20_8:+6.2f}억, 최악:{min_8:+6.2f}억) | 2040년(11년차) 중앙값:{med_11:+6.2f}억 | 평균MDD:{mdd:5.1f}%")
