import pandas as pd
import numpy as np
from compare_60_vs_70_to_2040 import m_dates, m_smh, m_xlv, sim_14yr_window

# 1. Check specific crisis-start 14-year windows (e.g., 2007-10 GFC peak start, 2006-01 start, 2011-10 start, 2012-10 start)
test_starts = [
    ('2006-10 (금융위기 1년 전 시작 ~ 2020.10)', '2006-10-01'),
    ('2007-10 (리먼사태 최고점 시작 ~ 2021.10)', '2007-10-01'),
    ('2009-03 (금융위기 직후 시작 ~ 2023.03)', '2009-03-01'),
    ('2012-10 (최근 14년: 2012.10 ~ 2026.10)', '2012-10-01'),
]

print("=== [A] 역사적 주요 시점별 14년(2027~2040 동일 기간) 정밀 비교: 60:40 vs 65:35 vs 70:30 ===")
for title, s_dt in test_starts:
    idx = np.where(m_dates >= pd.to_datetime(s_dt))[0][0]
    print(f"\n▶ {title}")
    for w_label, wb in [('SMH 60% : XLV 40%', 0.60), ('SMH 65% : XLV 35%', 0.65), ('SMH 70% : XLV 30%', 0.70)]:
        r_wd = sim_14yr_window(idx, wb, wb, monthly_wd=300.0, init_krw=40000.0)
        r_lump = sim_14yr_window(idx, wb, wb, monthly_wd=0.0, init_krw=100000.0)
        print(f"  {w_label} | [4억 월300인출] 14년후 잔고: {r_wd['final']/10000:6.2f}억 (최저잔고 {r_wd['min_bal']/10000:4.2f}억, MDD {r_wd['mdd']:6.1%}) | [10억 거치] 14년후 잔고: {r_lump['final']/10000:6.2f}억 (MDD {r_lump['mdd']:6.1%})")

# 2. Forward projection to 2040 (14 years: 2027~2040) under 3 Future Return Regimes (Monte Carlo 5,000 runs each)
np.random.seed(42)

def run_mc_2040(smh_cagr, xlv_cagr, smh_vol=0.28, xlv_vol=0.14, corr=0.45, n_sims=5000):
    # Monthly parameters
    dt = 1.0 / 12.0
    mu1 = np.log(1 + smh_cagr) * dt
    mu2 = np.log(1 + xlv_cagr) * dt
    sig1 = smh_vol * np.sqrt(dt)
    sig2 = xlv_vol * np.sqrt(dt)
    cov = np.array([[sig1**2, corr*sig1*sig2], [corr*sig1*sig2, sig2**2]])
    L = np.linalg.cholesky(cov)
    
    results = {}
    for w_label, wb in [('60:40', 0.60), ('65:35', 0.65), ('70:30', 0.70)]:
        wd_finals = []
        wd_survived = 0
        lump_8y = []
        lump_14y = []
        
        for _ in range(n_sims):
            z = np.random.normal(0, 1, size=(2, 168))
            shocks = L @ z
            r1_path = np.exp(mu1 - 0.5*sig1**2 + shocks[0]) - 1.0
            r2_path = np.exp(mu2 - 0.5*sig2**2 + shocks[1]) - 1.0
            
            # Sim 1: 4억 + 월 300만원 인출 (with 15-month SK Square bridge delay = 153 months withdrawal out of 168)
            v1 = 40000.0 * wb; v2 = 40000.0 * (1 - wb)
            alive = True
            for m in range(168):
                v1 *= (1 + r1_path[m]); v2 *= (1 + r2_path[m])
                if m >= 15: # After 15m SK Square buffer
                    tot = v1 + v2
                    if tot <= 300.0:
                        v1 = 0; v2 = 0; alive = False; break
                    if v1 / tot >= wb:
                        t1 = min(300.0, max(0.0, v1 - (tot - 300.0)*wb))
                        t2 = 300.0 - t1
                    else:
                        t2 = min(300.0, max(0.0, v2 - (tot - 300.0)*(1 - wb)))
                        t1 = 300.0 - t2
                    v1 -= t1; v2 -= t2
                if (m + 1) % 12 == 0 and alive:
                    tot = v1 + v2
                    # Approximate 3% annual tax/cost drag on rebalance gain
                    v1 = tot * wb * 0.995
                    v2 = tot * (1 - wb) * 0.995
            wd_finals.append((v1 + v2) / 10000.0)
            if alive and (v1 + v2) >= 40000.0:
                wd_survived += 1
                
            # Sim 2: 10억 거치 (starts 2030, 8 yrs to 2038, or 11 yrs to 2040)
            u1 = 100000.0 * wb; u2 = 100000.0 * (1 - wb)
            for m in range(132): # 11 years (2030 ~ 2040)
                u1 *= (1 + r1_path[m]); u2 *= (1 + r2_path[m])
                if (m + 1) % 12 == 0:
                    tot = (u1 + u2) * 0.995
                    u1 = tot * wb; u2 = tot * (1 - wb)
                if m == 95: # 8 years mark (repay 13.2억 after 22% tax on gain)
                    tot8 = u1 + u2
                    net8 = tot8 - max(0.0, (tot8 - 100000.0) * 0.20)
                    lump_8y.append(net8 / 10000.0)
                    # Deduct 13.2억 repayment at year 8 and keep compounding until 2040 (year 11)!
                    rem = max(0.0, net8 - 132000.0)
                    u1 = rem * wb; u2 = rem * (1 - wb)
            lump_14y.append((u1 + u2) / 10000.0)
            
        results[w_label] = {
            'wd_med': np.median(wd_finals),
            'wd_p10': np.percentile(wd_finals, 10),
            'wd_p25': np.percentile(wd_finals, 25),
            'wd_keep_prin': wd_survived / n_sims,
            'l8_med': np.median(lump_8y),
            'l8_p10': np.percentile(lump_8y, 10),
            'l2040_med': np.median(lump_14y),
            'l2040_p25': np.percentile(lump_14y, 25)
        }
    return results

print("\n=== [B] 2027~2040 몬테카를로 시뮬레이션 (5,000회, SK스퀘어 15개월 버퍼 + 8년차 13.2억 상환 후 2040년까지 보유) ===")
scenarios = [
    ('1. 보수적 둔화 시나리오 (SMH 연 14%, XLV 연 9%)', 0.14, 0.09),
    ('2. 중립적 성장 시나리오 (SMH 연 18%, XLV 연 10.5%)', 0.18, 0.105),
    ('3. 역사적 추세 시나리오 (SMH 연 23%, XLV 연 12%)', 0.23, 0.12),
]

for s_name, c1, c2 in scenarios:
    print(f"\n▶ {s_name}")
    res = run_mc_2040(c1, c2)
    for w_label in ['60:40', '65:35', '70:30']:
        r = res[w_label]
        print(f"  [{w_label}] 4억계좌 2040년 잔고: 중위 {r['wd_med']:5.2f}억 (하위10% {r['wd_p10']:4.2f}억, 원금4억유지확률 {r['wd_keep_prin']:5.1%}) | 10억계좌(13.2억 상환후 2040년 순자산): 중위 {r['l2040_med']:5.2f}억 (8년차 상환직전 세후중위 {r['l8_med']:5.2f}억, 하위10% {r['l8_p10']:5.2f}억)")
