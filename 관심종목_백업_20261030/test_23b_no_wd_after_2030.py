import numpy as np
from compare_25b_loan_60_vs_70 import sell_for_net_cash

# 1. Deterministic Scenario Table (No monthly withdrawals from Account 1 starting 2030!)
def sim_timeline_no_wd_after_2030(cagr_smh, cagr_xlv, w_base=0.60, payoff_2037=230000.0):
    r1 = (1.0 + cagr_smh) ** (1/12) - 1.0
    r2 = (1.0 + cagr_xlv) ** (1/12) - 1.0
    tx = 0.0015; cg = 0.22
    
    v1_a = 40000.0 * w_base * (1 - tx)
    v2_a = 40000.0 * (1 - w_base) * (1 - tx)
    b1_a = v1_a; b2_a = v2_a
    rg_a = 0.0; wd_a = 0.0
    
    v1_b = 0.0; v2_b = 0.0; b1_b = 0.0; b2_b = 0.0; rg_b = 0.0
    sf_b = 0.0
    
    rows = []
    for yr_idx, cal_yr in enumerate(range(2027, 2041)):
        if cal_yr == 2030:
            v1_b = 100000.0 * w_base * (1 - tx)
            v2_b = 100000.0 * (1 - w_base) * (1 - tx)
            b1_b = v1_b; b2_b = v2_b
            
        for m in range(12):
            m_global = yr_idx * 12 + m
            v1_a *= (1 + r1); v2_a *= (1 + r2)
            # Withdraw ONLY for 15 <= m_global < 36 (May 2028 ~ Dec 2029, 21 months = 0.63억 total)
            if 15 <= m_global < 36:
                tot_a = v1_a + v2_a
                ex1 = v1_a - (tot_a - 300.0) * w_base
                tk1 = min(300.0, max(0.0, ex1)); tk2 = 300.0 - tk1
                if tk1 > 0:
                    gs1 = tk1*(1+tx); f1 = min(1.0, gs1/v1_a); c1 = b1_a*f1
                    rg_a += (tk1 - c1); v1_a -= gs1; b1_a -= c1
                if tk2 > 0:
                    gs2 = tk2*(1+tx); f2 = min(1.0, gs2/v2_a); c2 = b2_a*f2
                    rg_a += (tk2 - c2); v2_a -= gs2; b2_a -= c2
                wd_a += 300.0
                
            if cal_yr >= 2030 and (v1_b + v2_b) > 0:
                v1_b *= (1 + r1); v2_b *= (1 + r2)
                
        # Year-end rebalance & tax for Account 1
        wt_a = 0.70 if cal_yr > 2037 else w_base
        tot_a = v1_a + v2_a
        if tot_a > 0:
            t1_a = tot_a * wt_a
            if v1_a > t1_a:
                s1 = v1_a - t1_a; c1 = b1_a*(s1/v1_a); rg_a += (s1 - c1); v1_a -= s1; b1_a -= c1
                buy2 = s1*0.997; v2_a += buy2; b2_a += buy2
            elif v2_a > (tot_a - t1_a):
                s2 = v2_a - (tot_a - t1_a); c2 = b2_a*(s2/v2_a); rg_a += (s2 - c2); v2_a -= s2; b2_a -= c2
                buy1 = s2*0.997; v1_a += buy1; b1_a += buy1
            if rg_a > 250.0:
                tax_a = (rg_a - 250.0) * cg; tn = v1_a + v2_a
                if tn > tax_a:
                    f1 = v1_a/tn; b1_a -= b1_a*(tax_a*f1/v1_a); b2_a -= b2_a*(tax_a*(1-f1)/v2_a)
                    v1_a -= tax_a*f1; v2_a -= tax_a*(1-f1)
            rg_a = 0.0
            
        if cal_yr >= 2030:
            wt_b = 0.70 if cal_yr > 2037 else w_base
            tot_b = v1_b + v2_b
            if tot_b > 0:
                t1_b = tot_b * wt_b
                if v1_b > t1_b:
                    s1 = v1_b - t1_b; c1 = b1_b*(s1/v1_b); rg_b += (s1 - c1); v1_b -= s1; b1_b -= c1
                    buy2 = s1*0.997; v2_b += buy2; b2_b += buy2
                elif v2_b > (tot_b - t1_b):
                    s2 = v2_b - (tot_b - t1_b); c2 = b2_b*(s2/v2_b); rg_b += (s2 - c2); v2_b -= s2; b2_b -= c2
                    buy1 = s2*0.997; v1_b += buy1; b1_b += buy1
                if rg_b > 250.0:
                    tax_b = (rg_b - 250.0) * cg; tn = v1_b + v2_b
                    if tn > tax_b:
                        f1 = v1_b/tn; b1_b -= b1_b*(tax_b*f1/v1_b); b2_b -= b2_b*(tax_b*(1-f1)/v2_b)
                        v1_b -= tax_b*f1; v2_b -= tax_b*(1-f1)
                rg_b = 0.0
            if cal_yr == 2037:
                v1_b, v2_b, b1_b, b2_b, sf_b, _ = sell_for_net_cash(v1_b, v2_b, b1_b, b2_b, payoff_2037, 0.70)
                if sf_b > 0 and (v1_a + v2_a) > 0:
                    # Also check how much remains in Account 1 if we cover sf_b from Account 1
                    v1_a_cov, v2_a_cov, b1_a_cov, b2_a_cov, sf_tot, _ = sell_for_net_cash(v1_a, v2_a, b1_a, b2_a, sf_b, 0.70)
                    v1_a, v2_a, b1_a, b2_a = v1_a_cov, v2_a_cov, b1_a_cov, b2_a_cov
                else:
                    sf_tot = sf_b
        bal_a = (v1_a + v2_a) / 10000.0
        bal_b = ((v1_b + v2_b) - (sf_b if cal_yr == 2037 else 0.0)) / 10000.0
        tot_net = ((v1_a + v2_a) + (v1_b + v2_b) - (sf_tot if cal_yr >= 2037 else 0.0)) / 10000.0
        rows.append((cal_yr, bal_a, wd_a/10000.0, bal_b, tot_net))
    return rows

print("==========================================================================")
print(" [2030년(10억 계좌 투입)부터 월 300만 원 인출 중단 시나리오별 잔고]")
print("==========================================================================")
for label, cs, cx in [
    ('0) 극보수 스트레스 (SMH 11.0%, XLV 7.5%)', 0.11, 0.075),
    ('1) 보수적 가정 (SMH 14.0%, XLV 9.0%)', 0.14, 0.09),
    ('2-A) 일반 가정 [표준 컨센서스] (SMH 16.0%, XLV 10.0%)', 0.16, 0.10),
    ('2-B) 일반 가정 [중립 상단] (SMH 18.0%, XLV 10.5%)', 0.18, 0.105),
    ('3) 낙관적 가정 [AI·헬스케어 고성장] (SMH 22.0%, XLV 11.5%)', 0.22, 0.115),
]:
    print(f"\n▶ {label}")
    res = {y: (ba, wda, bb, tot) for y, ba, wda, bb, tot in sim_timeline_no_wd_after_2030(cs, cx)}
    for y in [2029, 2036, 2037, 2040]:
        ba, wda, bb, tot = res[y]
        print(f"  {y}년말 | 4억계좌: {ba:6.2f}억 (누적인출 {wda:.2f}억) | 10억계좌: {bb:+6.2f}억 | 합산 순자산: {tot:+6.2f}억")

# 2. 20,000-path Regime-Weighted Monte Carlo with NO withdrawals after 2030
np.random.seed(20261021)
n_total = 20000
regimes = [
    (0.15, 0.105, 0.075),
    (0.30, 0.140, 0.090),
    (0.35, 0.170, 0.102),
    (0.20, 0.220, 0.115),
]
vol1 = 0.27; vol2 = 0.14; corr = 0.42; dt = 1.0/12.0
cov = np.array([[vol1**2, corr*vol1*vol2], [corr*vol1*vol2, vol2**2]]) * dt
L = np.linalg.cholesky(cov)
tx = 0.0015; cg = 0.22

res_2037_a = []; res_2037_b = []; res_2037_tot = []
res_2040_a = []; res_2040_b = []; res_2040_tot = []
b_solo_23b = []; comb_23b = []

for w_prob, c1, c2 in regimes:
    n_s = int(n_total * w_prob)
    mu1 = np.log(1 + c1)*dt - 0.5*(vol1**2)*dt
    mu2 = np.log(1 + c2)*dt - 0.5*(vol2**2)*dt
    Z = np.random.normal(size=(n_s, 168, 2))
    R = np.exp(np.array([mu1, mu2]) + Z @ L.T) - 1.0
    for s in range(n_s):
        v1_a = 40000.0*0.60*(1-tx); v2_a = 40000.0*0.40*(1-tx); b1_a = v1_a; b2_a = v2_a; rg_a = 0.0
        v1_b = 0.0; v2_b = 0.0; b1_b = 0.0; b2_b = 0.0; rg_b = 0.0; sf_b = 0.0; sf_tot = 0.0
        peak_s = 1.0; cur_s = 1.0
        for m_i in range(168):
            if m_i == 36:
                v1_b = 100000.0*0.60*(1-tx); v2_b = 100000.0*0.40*(1-tx); b1_b = v1_b; b2_b = v2_b
            r1 = R[s, m_i, 0]; r2 = R[s, m_i, 1]
            cur_s *= (1 + r1)
            if cur_s > peak_s: peak_s = cur_s
            smh_dd = (cur_s - peak_s)/peak_s
            if v1_a + v2_a > 0:
                v1_a *= (1 + r1); v2_a *= (1 + r2)
                # Withdraw ONLY for 15 <= m_i < 36 (21 months)
                if 15 <= m_i < 36:
                    tot_a = v1_a + v2_a
                    if tot_a <= 300.0: v1_a = 0.0; v2_a = 0.0
                    else:
                        ex1 = v1_a - (tot_a - 300.0)*0.60
                        tk1 = min(300.0, max(0.0, ex1)); tk2 = 300.0 - tk1
                        if tk1 > 0:
                            gs1 = tk1*(1+tx); f1 = min(1.0, gs1/v1_a); c_1 = b1_a*f1; rg_a += (tk1-c_1); v1_a -= gs1; b1_a -= c_1
                        if tk2 > 0:
                            gs2 = tk2*(1+tx); f2 = min(1.0, gs2/v2_a); c_2 = b2_a*f2; rg_a += (tk2-c_2); v2_a -= gs2; b2_a -= c_2
            if m_i >= 36 and (v1_b + v2_b) > 0:
                v1_b *= (1 + r1); v2_b *= (1 + r2)
            if (m_i + 1) % 12 == 0:
                wt_a = 0.70 if (m_i >= 132 or smh_dd <= -0.20) else 0.60
                tot_a = v1_a + v2_a
                if tot_a > 0:
                    t1_a = tot_a * wt_a
                    if v1_a > t1_a:
                        s1 = v1_a - t1_a; c_1 = b1_a*(s1/v1_a); rg_a += (s1-c_1); v1_a -= s1; b1_a -= c_1; buy2 = s1*0.997; v2_a += buy2; b2_a += buy2
                    elif v2_a > (tot_a - t1_a):
                        s2 = v2_a - (tot_a - t1_a); c_2 = b2_a*(s2/v2_a); rg_a += (s2-c_2); v2_a -= s2; b2_a -= c_2; buy1 = s2*0.997; v1_a += buy1; b1_a += buy1
                    if rg_a > 250.0:
                        tax_a = (rg_a - 250.0)*cg; tn = v1_a+v2_a
                        if tn > tax_a:
                            f1 = v1_a/tn; b1_a -= b1_a*(tax_a*f1/v1_a); b2_a -= b2_a*(tax_a*(1-f1)/v2_a); v1_a -= tax_a*f1; v2_a -= tax_a*(1-f1)
                    rg_a = 0.0
                if m_i >= 36:
                    wt_b = 0.70 if (m_i >= 132 or smh_dd <= -0.20) else 0.60
                    tot_b = v1_b + v2_b
                    if tot_b > 0:
                        t1_b = tot_b * wt_b
                        if v1_b > t1_b:
                            s1 = v1_b - t1_b; c_1 = b1_b*(s1/v1_b); rg_b += (s1-c_1); v1_b -= s1; b1_b -= c_1; buy2 = s1*0.997; v2_b += buy2; b2_b += buy2
                        elif v2_b > (tot_b - t1_b):
                            s2 = v2_b - (tot_b - t1_b); c_2 = b2_b*(s2/v2_b); rg_b += (s2-c_2); v2_b -= s2; b2_b -= c_2; buy1 = s2*0.997; v1_b += buy1; b1_b += buy1
                        if rg_b > 250.0:
                            tax_b = (rg_b - 250.0)*cg; tn = v1_b+v2_b
                            if tn > tax_b:
                                f1 = v1_b/tn; b1_b -= b1_b*(tax_b*f1/v1_b); b2_b -= b2_b*(tax_b*(1-f1)/v2_b); v1_b -= tax_b*f1; v2_b -= tax_b*(1-f1)
                        rg_b = 0.0
            if m_i == 131:
                na_pre = (v1_a + v2_a)/10000.0
                v1_b, v2_b, b1_b, b2_b, sf_b, _ = sell_for_net_cash(v1_b, v2_b, b1_b, b2_b, 230000.0, 0.70)
                b_solo_23b.append(sf_b == 0)
                nb_solo = ((v1_b + v2_b) - sf_b)/10000.0
                if sf_b > 0 and (v1_a + v2_a) > 0:
                    v1_a, v2_a, b1_a, b2_a, sf_tot, _ = sell_for_net_cash(v1_a, v2_a, b1_a, b2_a, sf_b, 0.70)
                else:
                    sf_tot = sf_b
                comb_23b.append(sf_tot == 0)
                tot_37 = ((v1_a + v2_a) + (v1_b + v2_b) - sf_tot)/10000.0
                res_2037_a.append(na_pre); res_2037_b.append(nb_solo); res_2037_tot.append(tot_37)
        tot_40 = ((v1_a + v2_a) + (v1_b + v2_b) - sf_tot)/10000.0
        res_2040_a.append((v1_a + v2_a)/10000.0); res_2040_b.append(((v1_b + v2_b) - sf_b)/10000.0); res_2040_tot.append(tot_40)

res_2037_tot = np.array(res_2037_tot); res_2040_tot = np.array(res_2040_tot)
res_2037_a = np.array(res_2037_a); res_2037_b = np.array(res_2037_b)
print("\n=== [2030년부터 월 300만 원 인출 중단 반영] 20,000회 몬테카를로 확률 전망 ===")
print(f"  10억 계좌 단독 23억 완납 확률: {np.mean(b_solo_23b)*100:.1f}%")
print(f"  두 계좌(4억+10억) 합산 23억 완납 확률: {np.mean(comb_23b)*100:.1f}%")
for p in [10, 25, 50, 60, 65, 70, 75, 90]:
    print(f"  P{p:2d} (상위 {100-p:2d}%) | 2037년(23억상환직후) 합산: {np.percentile(res_2037_tot, p):+6.2f}억 (4억계좌: {np.percentile(res_2037_a, p):5.2f}억 / 10억계좌: {np.percentile(res_2037_b, p):+6.2f}억) | 2040년 합산: {np.percentile(res_2040_tot, p):+6.2f}억")
m37 = np.mean(res_2037_tot); m40 = np.mean(res_2040_tot)
print(f"  평균값 (Mean) | 2037년 합산: {m37:+6.2f}억 (상위 {np.mean(res_2037_tot>=m37)*100:.1f}%) | 2040년 합산: {m40:+6.2f}억 (상위 {np.mean(res_2040_tot>=m40)*100:.1f}%)")
