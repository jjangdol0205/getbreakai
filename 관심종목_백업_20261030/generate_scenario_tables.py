import numpy as np
import pandas as pd
from test_18b_mandatory_deep import m_dates, m_smh, m_xlv, sell_for_net_cash, start_2005

# 1. Historical Rolling 14-Year for 4억 Account (with 15m SK Square delay vs immediate)
def sim_400m_hist(start_idx, n_years=14, w_base=0.60, w_crash=0.60, delay_months=15):
    n_months = n_years * 12
    sub_dates = m_dates[start_idx : start_idx + n_months]
    if len(sub_dates) < n_months:
        return None
    tx_cost = 0.0015; cg_tax = 0.22
    v1 = 40000.0 * w_base * (1 - tx_cost)
    v2 = 40000.0 * (1 - w_base) * (1 - tx_cost)
    b1 = v1; b2 = v2
    peak_s = 1.0; cur_s = 1.0
    rg_yr = 0.0
    total_wd = 0.0
    for m_i, dt in enumerate(sub_dates):
        r1 = m_smh.loc[dt]; r2 = m_xlv.loc[dt]
        v1 *= (1 + r1); v2 *= (1 + r2)
        cur_s *= (1 + r1)
        if cur_s > peak_s: peak_s = cur_s
        smh_dd = (cur_s - peak_s) / peak_s
        if m_i >= delay_months:
            tot = v1 + v2
            if tot <= 300.0:
                total_wd += tot; v1 = 0.0; v2 = 0.0; break
            cur_w1 = v1 / tot
            if cur_w1 >= w_base:
                ex1 = v1 - (tot - 300.0) * w_base
                tk1 = min(300.0, max(0.0, ex1)); tk2 = 300.0 - tk1
            else:
                ex2 = v2 - (tot - 300.0) * (1 - w_base)
                tk2 = min(300.0, max(0.0, ex2)); tk1 = 300.0 - tk2
            if tk1 > 0:
                gs1 = tk1 * (1 + tx_cost); f1 = min(1.0, gs1/v1); c1 = b1*f1
                rg_yr += (tk1 - c1); v1 -= gs1; b1 -= c1
            if tk2 > 0:
                gs2 = tk2 * (1 + tx_cost); f2 = min(1.0, gs2/v2); c2 = b2*f2
                rg_yr += (tk2 - c2); v2 -= gs2; b2 -= c2
            total_wd += 300.0
        if (m_i + 1) % 12 == 0 and (v1 + v2) > 0:
            tot = v1 + v2
            wt = w_crash if smh_dd <= -0.20 else w_base
            t1 = tot * wt
            if v1 > t1:
                s1 = v1 - t1; c1 = b1*(s1/v1); rg_yr += (s1 - c1); v1 -= s1; b1 -= c1; buy2 = s1*0.997; v2 += buy2; b2 += buy2
            elif v2 > (tot - t1):
                s2 = v2 - (tot - t1); c2 = b2*(s2/v2); rg_yr += (s2 - c2); v2 -= s2; b2 -= c2; buy1 = s2*0.997; v1 += buy1; b1 += buy1
            if rg_yr > 250.0:
                tax = (rg_yr - 250.0)*cg_tax; tn = v1 + v2
                if tn > tax:
                    f1 = v1/tn; b1 -= b1*(tax*f1/v1); b2 -= b2*(tax*(1-f1)/v2); v1 -= tax*f1; v2 -= tax*(1-f1)
            rg_yr = 0.0
    return {'final': (v1 + v2)/10000.0, 'total_wd': total_wd/10000.0}

print("=== [표 1 데이터] 역사적 롤링 (2005~2026) 4억 계좌 (14년) & 10억 계좌 (11년, 8년차 18억 상환) ===")
for name, wb, wc, post_w in [
    ('SMH 60% : XLV 40% 고정', 0.60, 0.60, 0.60),
    ('SMH 70% : XLV 30% 고정', 0.70, 0.70, 0.70),
    ('역발상 (평시60% -> 하락시70%)', 0.60, 0.70, 0.70),
]:
    r4 = [sim_400m_hist(i, 14, wb, wc, 15) for i in range(start_2005, len(m_dates)-168)]
    r4 = [x['final'] for x in r4 if x is not None]
    print(f"[4억계좌-15m유예] {name:<26} | 최악:{np.min(r4):6.2f}억 | 하위25%:{np.percentile(r4,25):6.2f}억 | 중앙값:{np.median(r4):6.2f}억 | 상위25%:{np.percentile(r4,75):6.2f}억 | 최근14년:{r4[-1]:6.2f}억")

# Deterministic / Median Trajectory Year-by-Year (2027~2040) under 3 Return Regimes
def sim_timeline_2027_2040(cagr_smh, cagr_xlv, w_base=0.60):
    # Monthly deterministic equivalent with annual tax & rebalancing
    r1_m = (1.0 + cagr_smh) ** (1/12) - 1.0
    r2_m = (1.0 + cagr_xlv) ** (1/12) - 1.0
    tx = 0.0015; cg = 0.22
    
    # Account 1: Starts Feb 2027 (Year 1 = 2027, 14 years to 2040). First 15 months funded by SK Square 60 shares.
    v1_a = 40000.0 * w_base * (1 - tx)
    v2_a = 40000.0 * (1 - w_base) * (1 - tx)
    b1_a = v1_a; b2_a = v2_a; rg_a = 0.0; cum_wd_a = 0.0
    
    # Account 2: Starts End of 2029 (i.e. runs 2030..2037 = 8 years, pays 18억 at end of 2037, runs 2038..2040 = 3 years)
    v1_b = 0.0; v2_b = 0.0; b1_b = 0.0; b2_b = 0.0; rg_b = 0.0
    
    rows = []
    for yr_idx, year in enumerate(range(2027, 2041)):
        if year == 2030: # Start of 8-year loan investment (2030~2037 = 8 full years)
            v1_b = 100000.0 * w_base * (1 - tx)
            v2_b = 100000.0 * (1 - w_base) * (1 - tx)
            b1_b = v1_b; b2_b = v2_b
            
        for m in range(12):
            global_m = yr_idx * 12 + m
            # Account 1 step
            v1_a *= (1 + r1_m); v2_a *= (1 + r2_m)
            if global_m >= 15: # After 15 months of SK Square bridge
                tot_a = v1_a + v2_a
                if tot_a > 300.0:
                    ex1 = v1_a - (tot_a - 300.0)*w_base
                    tk1 = min(300.0, max(0.0, ex1)); tk2 = 300.0 - tk1
                    if tk1 > 0:
                        gs1 = tk1*(1+tx); f1 = gs1/v1_a; c1 = b1_a*f1; rg_a += (tk1-c1); v1_a -= gs1; b1_a -= c1
                    if tk2 > 0:
                        gs2 = tk2*(1+tx); f2 = gs2/v2_a; c2 = b2_a*f2; rg_a += (tk2-c2); v2_a -= gs2; b2_a -= c2
                    cum_wd_a += 300.0
                else:
                    cum_wd_a += tot_a; v1_a = 0; v2_a = 0
            
            # Account 2 step (if active)
            if year >= 2030:
                w_b = 0.70 if year >= 2038 else w_base
                v1_b *= (1 + r1_m); v2_b *= (1 + r2_m)
                
        # End of Year Rebalance & Tax for Account 1
        tot_a = v1_a + v2_a
        if tot_a > 0:
            t1_a = tot_a * w_base
            if v1_a > t1_a:
                s1 = v1_a - t1_a; c1 = b1_a*(s1/v1_a); rg_a += (s1-c1); v1_a -= s1; b1_a -= c1; buy2 = s1*0.997; v2_a += buy2; b2_a += buy2
            elif v2_a > (tot_a - t1_a):
                s2 = v2_a - (tot_a - t1_a); c2 = b2_a*(s2/v2_a); rg_a += (s2-c2); v2_a -= s2; b2_a -= c2; buy1 = s2*0.997; v1_a += buy1; b1_a += buy1
            if rg_a > 250.0:
                tax_a = (rg_a - 250.0)*cg; tn = v1_a+v2_a; f1 = v1_a/tn
                b1_a -= b1_a*(tax_a*f1/v1_a); b2_a -= b2_a*(tax_a*(1-f1)/v2_a); v1_a -= tax_a*f1; v2_a -= tax_a*(1-f1)
            rg_a = 0.0
            
        # End of Year Rebalance & Tax for Account 2
        if year >= 2030:
            w_b = 0.70 if year >= 2038 else w_base
            tot_b = v1_b + v2_b
            if tot_b > 0:
                t1_b = tot_b * w_b
                if v1_b > t1_b:
                    s1 = v1_b - t1_b; c1 = b1_b*(s1/v1_b); rg_b += (s1-c1); v1_b -= s1; b1_b -= c1; buy2 = s1*0.997; v2_b += buy2; b2_b += buy2
                elif v2_b > (tot_b - t1_b):
                    s2 = v2_b - (tot_b - t1_b); c2 = b2_b*(s2/v2_b); rg_b += (s2-c2); v2_b -= s2; b2_b -= c2; buy1 = s2*0.997; v1_b += buy1; b1_b += buy1
                if rg_b > 250.0:
                    tax_b = (rg_b - 250.0)*cg; tn = v1_b+v2_b; f1 = v1_b/tn
                    b1_b -= b1_b*(tax_b*f1/v1_b); b2_b -= b2_b*(tax_b*(1-f1)/v2_b); v1_b -= tax_b*f1; v2_b -= tax_b*(1-f1)
                rg_b = 0.0
            if year == 2037: # End of Year 8 -> Pay off 18억 (180,000만원) net of tax!
                pre_pay = (v1_b + v2_b)/10000.0
                v1_b, v2_b, b1_b, b2_b, sf_b, tax_pay = sell_for_net_cash(v1_b, v2_b, b1_b, b2_b, 180000.0, 0.70)
                
        rows.append((year, (v1_a+v2_a)/10000.0, cum_wd_a/10000.0, (v1_b+v2_b)/10000.0))
    return rows

for scen_name, cs, cx in [
    ('보수적 시나리오 (SMH 연 14%, XLV 연 9%)', 0.14, 0.09),
    ('중립적 시나리오 (SMH 연 18%, XLV 연 10.5%)', 0.18, 0.105),
    ('역사적 추세 시나리오 (SMH 연 22%, XLV 연 11.5%)', 0.22, 0.115),
]:
    print(f"\n=== [연차별 타임라인] {scen_name} ===")
    rows = sim_timeline_2027_2040(cs, cx, 0.60)
    for y, ba, wda, bb in rows:
        print(f"  {y}년말 | 4억계좌 잔고: {ba:6.2f}억 (누적인출: {wda:4.2f}억) | 10억계좌 잔고: {bb:6.2f}억 | 합산 순금융자산: {ba+bb:6.2f}억")
