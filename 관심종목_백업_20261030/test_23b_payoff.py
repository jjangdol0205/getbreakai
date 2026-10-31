import numpy as np
from compare_25b_loan_60_vs_70 import m_dates, m_smh, m_xlv, sell_for_net_cash

start_2005 = np.where(m_dates >= '2005-01-01')[0][0]

def sim_hist_23b(start_idx, w_base=0.60, w_crash=0.60, w_post=0.70):
    sub_dates = m_dates[start_idx : start_idx + 132]
    if len(sub_dates) < 132: return None
    tx = 0.0015; cg = 0.22
    v1 = 100000.0 * w_base * (1 - tx); v2 = 100000.0 * (1 - w_base) * (1 - tx)
    b1 = v1; b2 = v2; rg_yr = 0.0
    peak_s = 1.0; cur_s = 1.0
    sf_8yr = 0.0; net_8yr = 0.0
    for m_i, dt in enumerate(sub_dates):
        r1 = m_smh.loc[dt]; r2 = m_xlv.loc[dt]
        v1 *= (1 + r1); v2 *= (1 + r2)
        cur_s *= (1 + r1)
        if cur_s > peak_s: peak_s = cur_s
        smh_dd = (cur_s - peak_s) / peak_s
        if (m_i + 1) % 12 == 0 and (v1 + v2) > 0:
            tot = v1 + v2
            wt = w_post if m_i >= 96 else (w_crash if smh_dd <= -0.20 else w_base)
            t1 = tot * wt
            if v1 > t1:
                s1 = v1 - t1; c1 = b1*(s1/v1); rg_yr += (s1-c1); v1 -= s1; b1 -= c1; buy2 = s1*0.997; v2 += buy2; b2 += buy2
            elif v2 > (tot - t1):
                s2 = v2 - (tot - t1); c2 = b2*(s2/v2); rg_yr += (s2-c2); v2 -= s2; b2 -= c2; buy1 = s2*0.997; v1 += buy1; b1 += buy1
            if rg_yr > 250.0:
                tax = (rg_yr - 250.0)*cg; tn = v1 + v2
                if tn > tax:
                    f1 = v1/tn; b1 -= b1*(tax*f1/v1); b2 -= b2*(tax*(1-f1)/v2); v1 -= tax*f1; v2 -= tax*(1-f1)
            rg_yr = 0.0
        if m_i == 95:
            # Pay 230,000만원 (23억) net of tax!
            v1, v2, b1, b2, sf_8yr, _ = sell_for_net_cash(v1, v2, b1, b2, 230000.0, w_post)
            net_8yr = ((v1 + v2) - sf_8yr) / 10000.0
    final_2040 = ((v1 + v2) - sf_8yr) / 10000.0
    return {'sf': sf_8yr/10000.0, 'net_8yr': net_8yr, 'final_2040': final_2040}

print("=== [2005~2026 역사적 롤링] 8년 뒤 세후 23억 원 확정 상환 비교 ===")
for name, wb, wc, wp in [
    ('SMH 60% : XLV 40% 고정', 0.60, 0.60, 0.60),
    ('SMH 65% : XLV 35% 고정', 0.65, 0.65, 0.65),
    ('SMH 70% : XLV 30% 고정', 0.70, 0.70, 0.70),
    ('역발상 (평시60% -> 하락70% -> 상환후70%)', 0.60, 0.70, 0.70),
]:
    res = [sim_hist_23b(i, wb, wc, wp) for i in range(start_2005, len(m_dates)-132)]
    res = [r for r in res if r is not None]
    succ = np.mean([r['sf'] == 0 for r in res]) * 100
    med8 = np.median([r['net_8yr'] for r in res])
    p25_8 = np.percentile([r['net_8yr'] for r in res], 25)
    min8 = np.min([r['net_8yr'] for r in res])
    med11 = np.median([r['final_2040'] for r in res])
    print(f"  {name:<36} | 23억단독완납성공률: {succ:5.1f}% | 8년차상환후 중앙값:{med8:+6.2f}억 (하위25%:{p25_8:+6.2f}억, 최악:{min8:+6.2f}억) | 2040년 중앙값:{med11:+6.2f}억")

# Regime-Weighted Monte Carlo for 23B Payoff (Account 1 + Account 2 Combined)
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
        v1_b = 0.0; v2_b = 0.0; b1_b = 0.0; b2_b = 0.0; rg_b = 0.0; sf_b = 0.0
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
                if m_i >= 15:
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
                wt_a = 0.70 if smh_dd <= -0.20 else 0.60
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
                v1_b, v2_b, b1_b, b2_b, sf_b, _ = sell_for_net_cash(v1_b, v2_b, b1_b, b2_b, 230000.0, 0.70)
                b_solo_23b.append(sf_b == 0)
                na = (v1_a + v2_a)/10000.0; nb = ((v1_b + v2_b) - sf_b)/10000.0
                res_2037_a.append(na); res_2037_b.append(nb); res_2037_tot.append(na + nb)
                comb_23b.append((na + nb) >= 0)
        na40 = (v1_a + v2_a)/10000.0; nb40 = ((v1_b + v2_b) - sf_b)/10000.0
        res_2040_a.append(na40); res_2040_b.append(nb40); res_2040_tot.append(na40 + nb40)

res_2037_tot = np.array(res_2037_tot); res_2040_tot = np.array(res_2040_tot)
print("\n=== [23억 확정 상환] 20,000회 다중 국면 몬테카를로 확률 전망 ===")
print(f"  10억 계좌 단독 23억 완납 확률: {np.mean(b_solo_23b)*100:.1f}%")
print(f"  두 계좌(4억+10억) 합산 23억 완납 확률: {np.mean(comb_23b)*100:.1f}%")
for p in [10, 25, 50, 75, 90]:
    print(f"  P{p:2d} (상위 {100-p:2d}%) | 2037년(23억상환직후) 합산: {np.percentile(res_2037_tot, p):+6.2f}억 (10억계좌 단독: {np.percentile(res_2037_b, p):+6.2f}억) | 2040년 합산: {np.percentile(res_2040_tot, p):+6.2f}억")
