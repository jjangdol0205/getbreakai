import numpy as np
import pandas as pd
from compare_25b_loan_60_vs_70 import m_dates, m_smh, m_xlv, sim_historical_25b, sell_for_net_cash, configs

print("=== [1] 주요 역사적 시기별 8년 만기(18억 상환 vs 8억 이자상환) 및 11년(2040) 비교 ===")
key_starts = [
    ('2007-10', '2007.10 금융위기 최고점 진입 (만기 2015.10, 11년차 2018.10)'),
    ('2011-10', '2011.10 평균적 장세 진입 (만기 2019.10, 11년차 2022.10 폭락장)'),
    ('2014-12', '2014.12 진입 -> 8년 만기일이 하필 2022.12 반도체 대폭락장 바닥! (11년차 2025.12)'),
    ('2015-10', '2015.10 최근 11년 완주 구간 (만기 2023.10, 11년차 2026.10)'),
]

for ym, desc in key_starts:
    idx_pos = np.where(m_dates.strftime('%Y-%m') == ym)[0][0]
    print(f"\n▶ {desc}")
    for name, wb, wc in configs:
        r_18 = sim_historical_25b(idx_pos, 11, wb, wc, '18b_full')
        r_08 = sim_historical_25b(idx_pos, 11, wb, wc, '8b_int_only')
        print(f"  {name:<22} | 8년차세전평가: {r_18['val_8yr_pre']:6.2f}억 | [18억상환후] 8년차:{r_18['net_8yr_post']:+6.2f}억 -> 11년차:{r_18['final_2040']:+6.2f}억 | [이자8억상환후] 8년차:{r_08['net_8yr_post']:+6.2f}억 -> 11년차:{r_08['final_2040']:+6.2f}억 | 8년MDD:{r_18['mdd_8yr']*100:5.1f}%")

# Monte Carlo for 2029~2040 (8 years to 2037 + 3 years to 2040 = 11 years)
def run_mc_25b(cagr_smh, cagr_xlv, n_sims=5000, seed=42):
    np.random.seed(seed)
    vol_smh = 0.28; vol_xlv = 0.145; corr = 0.42
    dt = 1.0 / 12.0
    mu1 = np.log(1 + cagr_smh) * dt - 0.5 * (vol_smh**2) * dt
    mu2 = np.log(1 + cagr_xlv) * dt - 0.5 * (vol_xlv**2) * dt
    cov = np.array([[vol_smh**2, corr*vol_smh*vol_xlv], [corr*vol_smh*vol_xlv, vol_xlv**2]]) * dt
    L = np.linalg.cholesky(cov)
    
    n_months = 132 # 11 years (8 yrs + 3 yrs)
    Z = np.random.normal(size=(n_sims, n_months, 2))
    R = np.exp( np.array([mu1, mu2]) + Z @ L.T ) - 1.0
    
    print(f"\n=== [2] 2029~2040 몬테카를로 (SMH 연 {cagr_smh*100:.1f}%, XLV 연 {cagr_xlv*100:.1f}%, 25억 대출: 15억 전세 + 10억 투자) ===")
    for name, wb, wc in configs:
        for lock_18b in [False, True]:
            lock_str = "+5~7년차Lock" if lock_18b else "기본(NoLock)"
            s_18 = []; med_18_2040 = []; p10_18_2040 = []; p25_18_2040 = []
            s_08 = []; med_08_2040 = []; p10_08_2040 = []
            for s in range(n_sims):
                # Run Case A (18억 payoff at yr 8)
                v1 = 100000.0 * wb * 0.9985; v2 = 100000.0 * (1 - wb) * 0.9985
                b1 = v1; b2 = v2
                rg_yr = 0.0; peak_s = 1.0; cur_s = 1.0
                locked_cash = 0.0
                shortfall = 0.0
                for m_i in range(n_months):
                    r1 = R[s, m_i, 0]; r2 = R[s, m_i, 1]
                    v1 *= (1 + r1); v2 *= (1 + r2)
                    cur_s *= (1 + r1)
                    if cur_s > peak_s: peak_s = cur_s
                    smh_dd = (cur_s - peak_s) / peak_s
                    if locked_cash > 0:
                        locked_cash *= (1 + 0.035/12.0) # SGOV ~3.5% after tax
                    if (m_i + 1) % 12 == 0:
                        tot = v1 + v2
                        if tot > 0:
                            wt = wc if smh_dd <= -0.30 else wb
                            t1 = tot * wt
                            if v1 > t1:
                                sell1 = v1 - t1; c1 = b1*(sell1/v1); rg_yr += (sell1 - c1)
                                v1 -= sell1; b1 -= c1; buy2 = sell1*0.997; v2 += buy2; b2 += buy2
                            elif v2 > (tot - t1):
                                sell2 = v2 - (tot - t1); c2 = b2*(sell2/v2); rg_yr += (sell2 - c2)
                                v2 -= sell2; b2 -= c2; buy1 = sell2*0.997; v1 += buy1; b1 += buy1
                            if rg_yr > 250.0:
                                tax = (rg_yr - 250.0) * 0.22
                                tn = v1 + v2; f1 = v1/tn
                                b1 -= b1*(tax*f1/v1); b2 -= b2*(tax*(1-f1)/v2)
                                v1 -= tax*f1; v2 -= tax*(1-f1)
                        rg_yr = 0.0
                        # Check Year 5, 6, 7 (m_i == 59, 71, 83) for Lock-in of 18억 if tot >= 26억
                        if lock_18b and locked_cash == 0 and m_i in (59, 71, 83) and (v1 + v2) >= 260000.0:
                            v1, v2, b1, b2, sf, _ = sell_for_net_cash(v1, v2, b1, b2, 170000.0, wb)
                            locked_cash = 170000.0
                    if m_i == 95: # End of Year 8: Pay 180,000 (18억)
                        need = max(0.0, 180000.0 - locked_cash)
                        surplus_cash = max(0.0, locked_cash - 180000.0)
                        locked_cash = 0.0
                        if need > 0:
                            v1, v2, b1, b2, shortfall, _ = sell_for_net_cash(v1, v2, b1, b2, need, wb)
                        else:
                            v1 += surplus_cash * wb; b1 += surplus_cash * wb
                            v2 += surplus_cash * (1 - wb); b2 += surplus_cash * (1 - wb)
                final_net = (v1 + v2) - shortfall
                s_18.append(shortfall == 0)
                med_18_2040.append(final_net / 10000.0)
            print(f"  {name:<20} [{lock_str}] | 18억상환성공률: {np.mean(s_18)*100:5.1f}% | 2040년 순자산 P10(최악10%): {np.percentile(med_18_2040, 10):+6.2f}억 | P25: {np.percentile(med_18_2040, 25):+6.2f}억 | 중앙값(Median): {np.median(med_18_2040):+6.2f}억")

run_mc_25b(0.14, 0.09)
run_mc_25b(0.18, 0.105)
run_mc_25b(0.22, 0.115)
