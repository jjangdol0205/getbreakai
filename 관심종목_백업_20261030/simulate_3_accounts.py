import numpy as np

# Fast, self-contained 3-Account Simulator (2027 ~ 2040, Full After-Tax & Transaction Cost):
# - [계좌 1] 본인 명의 SK스퀘어 전환 계좌:
#     Case 1A: 2027.02까지 4개월(16주, 1,200만 원) 사용 후 남은 60주 = 4,536만 원으로 시작 (14년 무인출 거치)
#     Case 1B: 지금 즉시 76주 전량 = 5,745.6만 원으로 시작 (2027년 2월 전까지 4개월 생활비는 아버지 계좌나 여유자금 활용 시)
# - [계좌 2] 아버지 명의 4억 원 계좌:
#     2027.02 ~ 2029.12 (35개월간 월 300만 원 = 총 1.05억 원) 인출 후, 2030.01부터 인출 중단하고 2040년까지 무인출 거치!
# - [계좌 3] 본인 명의 10억 원 계좌 (25억 이주비 대출 중 10억 투자):
#     2030.01에 10억 원 투입 -> 8년간 무인출 복리 운용 후 2037년 말 '세후 23억 원' 확정 상환!

def step_account_year(v1, v2, b1, b2, r1, r2, wt, monthly_wd=0.0, n_wd_months=0, deduct_tax=True):
    tx = 0.0015; cg = 0.22
    rg = 0.0; wd_tot = 0.0
    for m in range(12):
        v1 *= (1 + r1); v2 *= (1 + r2)
        if m < n_wd_months and monthly_wd > 0:
            tot = v1 + v2
            if tot <= monthly_wd:
                wd_tot += tot; v1 = 0.0; v2 = 0.0
            else:
                ex1 = v1 - (tot - monthly_wd) * 0.60
                tk1 = min(monthly_wd, max(0.0, ex1)); tk2 = monthly_wd - tk1
                if tk1 > 0:
                    gs1 = tk1*(1+tx); f1 = min(1.0, gs1/v1); c1 = b1*f1
                    rg += (tk1 - c1); v1 -= gs1; b1 -= c1
                if tk2 > 0:
                    gs2 = tk2*(1+tx); f2 = min(1.0, gs2/v2); c2 = b2*f2
                    rg += (tk2 - c2); v2 -= gs2; b2 -= c2
                wd_tot += monthly_wd
    tot = v1 + v2
    if tot > 0:
        t1 = tot * wt
        if v1 > t1:
            s1 = v1 - t1; c1 = b1*(s1/v1); rg += (s1 - c1); v1 -= s1; b1 -= c1
            buy2 = s1*0.997; v2 += buy2; b2 += buy2
        elif v2 > (tot - t1):
            s2 = v2 - (tot - t1); c2 = b2*(s2/v2); rg += (s2 - c2); v2 -= s2; b2 -= c2
            buy1 = s2*0.997; v1 += buy1; b1 += buy1
        if deduct_tax and rg > 250.0:
            tax = (rg - 250.0) * cg; tn = v1 + v2
            if tn > tax:
                f1 = v1/tn; b1 -= b1*(tax*f1/v1); b2 -= b2*(tax*(1-f1)/v2)
                v1 -= tax*f1; v2 -= tax*(1-f1)
    return v1, v2, b1, b2, rg, wd_tot

def get_net_liquidation_val(v1, v2, b1, b2, exemption_left=0.0):
    tx = 0.0015; cg = 0.22
    tot = v1 + v2; tot_b = b1 + b2
    if tot <= 0: return 0.0
    gain = max(0.0, tot - tot_b)
    tax = max(0.0, gain - exemption_left) * cg
    return tot * (1.0 - tx) - tax

def liquidate_net_target(v1, v2, b1, b2, target_net, w_post=0.70, exemption_left=0.0):
    tx = 0.0015; cg = 0.22
    tot = v1 + v2; tot_b = b1 + b2
    if tot <= 0:
        return 0.0, 0.0, 0.0, 0.0, target_net
    gain_ratio = max(0.0, (tot - tot_b) / tot)
    eff_rate = 1.0 - tx - cg * gain_ratio
    max_net = tot * eff_rate + min(exemption_left, max(0.0, tot - tot_b)) * cg
    if max_net >= target_net:
        gross_sell = max(0.0, (target_net - min(exemption_left, max(0.0, tot - tot_b)) * cg) / eff_rate)
        rem_ratio = max(0.0, 1.0 - (gross_sell / tot))
        v1_new = (tot * rem_ratio) * w_post
        v2_new = (tot * rem_ratio) * (1.0 - w_post)
        b1_new = (tot_b * rem_ratio) * w_post
        b2_new = (tot_b * rem_ratio) * (1.0 - w_post)
        return v1_new, v2_new, b1_new, b2_new, 0.0
    else:
        shortfall = target_net - max_net
        return 0.0, 0.0, 0.0, 0.0, shortfall

def sim_3_accounts(cagr_smh, cagr_xlv, sk_init=5745.6, sk_wd_4m=True, payoff_2037=230000.0):
    r1 = (1.0 + cagr_smh)**(1/12) - 1.0
    r2 = (1.0 + cagr_xlv)**(1/12) - 1.0
    tx = 0.0015; cg = 0.22
    w_base = 0.60
    
    # If sk_wd_4m is True: start with 4,536만원 in Feb 2027 (after selling 16 shares for 4m Oct 2026~Jan 2027)
    init_1 = 4536.0 if sk_wd_4m else 5745.6
    v1_1 = init_1 * w_base * (1 - tx); v2_1 = init_1 * (1 - w_base) * (1 - tx)
    b1_1 = v1_1; b2_1 = v2_1
    # Also track standalone Account 1 (if it never has to cover Account 3)
    v1_1s = v1_1; v2_1s = v2_1; b1_1s = b1_1; b2_1s = b2_1
    
    # Account 2: Father's 4억 account
    v1_2 = 40000.0 * w_base * (1 - tx); v2_2 = 40000.0 * (1 - w_base) * (1 - tx)
    b1_2 = v1_2; b2_2 = v2_2; wd_2_cum = 0.0
    
    # Account 3: User's 10억 loan account
    v1_3 = 0.0; v2_3 = 0.0; b1_3 = 0.0; b2_3 = 0.0
    sf_3_solo = 0.0; sf_my_comb = 0.0
    
    rows = []
    for cal_yr in range(2027, 2041):
        if cal_yr == 2030:
            v1_3 = 100000.0 * w_base * (1 - tx); v2_3 = 100000.0 * (1 - w_base) * (1 - tx)
            b1_3 = v1_3; b2_3 = v2_3
            
        wt = 0.70 if cal_yr > 2037 else w_base
        
        # Account 2 (Father: withdraws 300만원/mo in 2027(11m), 2028(12m), 2029(12m) = 35m = 1.05억)
        n_wd = 11 if cal_yr == 2027 else (12 if cal_yr in (2028, 2029) else 0)
        v1_2, v2_2, b1_2, b2_2, _, wd_yr = step_account_year(v1_2, v2_2, b1_2, b2_2, r1, r2, wt, 300.0, n_wd, deduct_tax=True)
        wd_2_cum += wd_yr
        
        # Standalone Account 1
        v1_1s, v2_1s, b1_1s, b2_1s, _, _ = step_account_year(v1_1s, v2_1s, b1_1s, b2_1s, r1, r2, wt, 0.0, 0, deduct_tax=True)
        
        # Account 1 & Account 3 (User's accounts)
        v1_1, v2_1, b1_1, b2_1, rg_1, _ = step_account_year(v1_1, v2_1, b1_1, b2_1, r1, r2, wt, 0.0, 0, deduct_tax=False)
        rg_3 = 0.0
        if cal_yr >= 2030 and (v1_3 + v2_3) > 0:
            v1_3, v2_3, b1_3, b2_3, rg_3, _ = step_account_year(v1_3, v2_3, b1_3, b2_3, r1, r2, wt, 0.0, 0, deduct_tax=False)
            
        rg_user = rg_1 + rg_3
        if rg_user > 250.0:
            tax_u = (rg_user - 250.0) * cg
            tot_u = (v1_1 + v2_1) + (v1_3 + v2_3)
            if tot_u > tax_u:
                sh1 = (v1_1 + v2_1) / tot_u; sh3 = (v1_3 + v2_3) / tot_u
                t_1 = tax_u * sh1; t_3 = tax_u * sh3
                if (v1_1 + v2_1) > 0:
                    f1 = t_1 / (v1_1 + v2_1)
                    v1_1 *= (1-f1); v2_1 *= (1-f1); b1_1 *= (1-f1); b2_1 *= (1-f1)
                if (v1_3 + v2_3) > 0:
                    f3 = t_3 / (v1_3 + v2_3)
                    v1_3 *= (1-f3); v2_3 *= (1-f3); b1_3 *= (1-f3); b2_3 *= (1-f3)
                    
        if cal_yr == 2037:
            v1_3, v2_3, b1_3, b2_3, sf_3_solo = liquidate_net_target(v1_3, v2_3, b1_3, b2_3, payoff_2037, 0.70, exemption_left=0.0)
            if sf_3_solo > 0:
                v1_1, v2_1, b1_1, b2_1, sf_my_comb = liquidate_net_target(v1_1, v2_1, b1_1, b2_1, sf_3_solo, 0.70, exemption_left=0.0)
            else:
                sf_my_comb = 0.0
                
        b1_solo = (v1_1s + v2_1s)/10000.0
        b2_val = (v1_2 + v2_2)/10000.0
        b3_solo = ((v1_3 + v2_3) - (sf_3_solo if cal_yr >= 2037 else 0.0))/10000.0
        my_net = ((v1_1 + v2_1) + (v1_3 + v2_3) - (sf_my_comb if cal_yr >= 2037 else 0.0))/10000.0
        tot_all = my_net + b2_val
        rows.append((cal_yr, b1_solo, b2_val, wd_2_cum/10000.0, b3_solo, my_net, tot_all))
    return rows

print("=========================================================================================================")
print(" [3개 계좌 개별 및 통합 시뮬레이션: ① 본인 SK계좌(4,536만) | ② 아버지 4억계좌 | ③ 본인 10억계좌]")
print("=========================================================================================================")
for label, cs, cx in [
    ('0) 극보수 스트레스 (SMH 11.0%, XLV 7.5%)', 0.11, 0.075),
    ('1) 보수적 가정 (SMH 14.0%, XLV 9.0%)', 0.14, 0.09),
    ('2-A) 일반 가정 [표준 컨센서스] (SMH 16.0%, XLV 10.0%)', 0.16, 0.10),
    ('2-B) 일반 가정 [중립 상단] (SMH 18.0%, XLV 10.5%)', 0.18, 0.105),
    ('3) 낙관적 가정 [AI·헬스케어 고성장] (SMH 22.0%, XLV 11.5%)', 0.22, 0.115),
]:
    print(f"\n▶ {label}")
    rows_45 = {r[0]: r for r in sim_3_accounts(cs, cx, sk_wd_4m=True)}
    rows_57 = {r[0]: r for r in sim_3_accounts(cs, cx, sk_wd_4m=False)}
    for y in [2029, 2036, 2037, 2040]:
        _, b1_s, b2, wd2, b3_s, my_net, tot_all = rows_45[y]
        _, b1_s57, _, _, _, my_net57, tot_all57 = rows_57[y]
        print(f"  {y}년말 | ①본인SK: {b1_s:5.2f}억(76주전액시 {b1_s57:5.2f}억) | ③본인10억단독: {b3_s:+6.2f}억 -> [본인합산(①+③): {my_net:+6.2f}억(76주시 {my_net57:+6.2f}억)] || ②아버지4억: {b2:6.2f}억 || 3계좌총합: {tot_all:+6.2f}억")

# Monte Carlo 20,000 paths for the 3 Accounts
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

acc1_37 = []; acc2_37 = []; acc3_37 = []; my_comb_37 = []; all_37 = []
acc1_40 = []; acc2_40 = []; acc3_40 = []; my_comb_40 = []; all_40 = []
succ_acc3_only = []; succ_my_comb = []; succ_with_gift = []

for w_prob, c1, c2 in regimes:
    n_s = int(n_total * w_prob)
    mu1 = np.log(1 + c1)*dt - 0.5*(vol1**2)*dt
    mu2 = np.log(1 + c2)*dt - 0.5*(vol2**2)*dt
    Z = np.random.normal(size=(n_s, 168, 2))
    R = np.exp(np.array([mu1, mu2]) + Z @ L.T) - 1.0
    for s in range(n_s):
        # Account 1 (User SK Square: 4,536만원)
        v1_1 = 4536.0*0.60*(1-tx); v2_1 = 4536.0*0.40*(1-tx); b1_1 = v1_1; b2_1 = v2_1; rg_1 = 0.0
        # Account 2 (Father 4억: 40,000만원)
        v1_2 = 40000.0*0.60*(1-tx); v2_2 = 40000.0*0.40*(1-tx); b1_2 = v1_2; b2_2 = v2_2; rg_2 = 0.0
        # Account 3 (User 10억: starts m_i == 36)
        v1_3 = 0.0; v2_3 = 0.0; b1_3 = 0.0; b2_3 = 0.0; rg_3 = 0.0
        
        peak_s = 1.0; cur_s = 1.0
        sf_3 = 0.0; sf_my = 0.0
        for m_i in range(168):
            if m_i == 36:
                v1_3 = 100000.0*0.60*(1-tx); v2_3 = 100000.0*0.40*(1-tx); b1_3 = v1_3; b2_3 = v2_3
            r1 = R[s, m_i, 0]; r2 = R[s, m_i, 1]
            cur_s *= (1 + r1)
            if cur_s > peak_s: peak_s = cur_s
            smh_dd = (cur_s - peak_s)/peak_s
            
            # Step 3 accounts
            v1_1 *= (1 + r1); v2_1 *= (1 + r2)
            if (v1_2 + v2_2) > 0:
                v1_2 *= (1 + r1); v2_2 *= (1 + r2)
                if m_i < 35: # 35 months of 300만원 withdrawal from Father's account
                    tot_2 = v1_2 + v2_2
                    if tot_2 <= 300.0: v1_2 = 0.0; v2_2 = 0.0
                    else:
                        ex1 = v1_2 - (tot_2 - 300.0)*0.60
                        tk1 = min(300.0, max(0.0, ex1)); tk2 = 300.0 - tk1
                        if tk1 > 0:
                            gs1 = tk1*(1+tx); f1 = min(1.0, gs1/v1_2); c_1 = b1_2*f1; rg_2 += (tk1-c_1); v1_2 -= gs1; b1_2 -= c_1
                        if tk2 > 0:
                            gs2 = tk2*(1+tx); f2 = min(1.0, gs2/v2_2); c_2 = b2_2*f2; rg_2 += (tk2-c_2); v2_2 -= gs2; b2_2 -= c_2
            if m_i >= 36 and (v1_3 + v2_3) > 0:
                v1_3 *= (1 + r1); v2_3 *= (1 + r2)
                
            if (m_i + 1) % 12 == 0:
                wt = 0.70 if (m_i >= 132 or smh_dd <= -0.20) else 0.60
                # Rebalance Account 1
                tot_1 = v1_1 + v2_1
                if tot_1 > 0:
                    t1 = tot_1 * wt
                    if v1_1 > t1:
                        s1 = v1_1 - t1; c_1 = b1_1*(s1/v1_1); rg_1 += (s1-c_1); v1_1 -= s1; b1_1 -= c_1; buy2 = s1*0.997; v2_1 += buy2; b2_1 += buy2
                    elif v2_1 > (tot_1 - t1):
                        s2 = v2_1 - (tot_1 - t1); c_2 = b2_1*(s2/v2_1); rg_1 += (s2-c_2); v2_1 -= s2; b2_1 -= c_2; buy1 = s2*0.997; v1_1 += buy1; b1_1 += buy1
                    if rg_1 > 250.0:
                        tax_1 = (rg_1 - 250.0)*cg; tn = v1_1+v2_1
                        if tn > tax_1:
                            f1 = v1_1/tn; b1_1 -= b1_1*(tax_1*f1/v1_1); b2_1 -= b2_1*(tax_1*(1-f1)/v2_1); v1_1 -= tax_1*f1; v2_1 -= tax_1*(1-f1)
                    rg_1 = 0.0
                # Rebalance Account 2
                tot_2 = v1_2 + v2_2
                if tot_2 > 0:
                    t1 = tot_2 * wt
                    if v1_2 > t1:
                        s1 = v1_2 - t1; c_1 = b1_2*(s1/v1_2); rg_2 += (s1-c_1); v1_2 -= s1; b1_2 -= c_1; buy2 = s1*0.997; v2_2 += buy2; b2_2 += buy2
                    elif v2_2 > (tot_2 - t1):
                        s2 = v2_2 - (tot_2 - t1); c_2 = b2_2*(s2/v2_2); rg_2 += (s2-c_2); v2_2 -= s2; b2_2 -= c_2; buy1 = s2*0.997; v1_2 += buy1; b1_2 += buy1
                    if rg_2 > 250.0:
                        tax_2 = (rg_2 - 250.0)*cg; tn = v1_2+v2_2
                        if tn > tax_2:
                            f1 = v1_2/tn; b1_2 -= b1_2*(tax_2*f1/v1_2); b2_2 -= b2_2*(tax_2*(1-f1)/v2_2); v1_2 -= tax_2*f1; v2_2 -= tax_2*(1-f1)
                    rg_2 = 0.0
                # Rebalance Account 3
                if m_i >= 36:
                    tot_3 = v1_3 + v2_3
                    if tot_3 > 0:
                        t1 = tot_3 * wt
                        if v1_3 > t1:
                            s1 = v1_3 - t1; c_1 = b1_3*(s1/v1_3); rg_3 += (s1-c_1); v1_3 -= s1; b1_3 -= c_1; buy2 = s1*0.997; v2_3 += buy2; b2_3 += buy2
                        elif v2_3 > (tot_3 - t1):
                            s2 = v2_3 - (tot_3 - t1); c_2 = b2_3*(s2/v2_3); rg_3 += (s2-c_2); v2_3 -= s2; b2_3 -= c_2; buy1 = s2*0.997; v1_3 += buy1; b1_3 += buy1
                        if rg_3 > 250.0:
                            tax_3 = (rg_3 - 250.0)*cg; tn = v1_3+v2_3
                            if tn > tax_3:
                                f1 = v1_3/tn; b1_3 -= b1_3*(tax_3*f1/v1_3); b2_3 -= b2_3*(tax_3*(1-f1)/v2_3); v1_3 -= tax_3*f1; v2_3 -= tax_3*(1-f1)
                        rg_3 = 0.0
            if m_i == 131:
                a1_pre = (v1_1 + v2_1)/10000.0
                a2_37 = (v1_2 + v2_2)/10000.0
                v1_3, v2_3, b1_3, b2_3, sf_3 = liquidate_net_target(v1_3, v2_3, b1_3, b2_3, 230000.0, 0.70, 0.0)
                a3_post_solo = ((v1_3 + v2_3) - sf_3)/10000.0
                succ_acc3_only.append(sf_3 == 0.0)
                
                # Cover sf_3 using Account 1 (User's SK Square account)
                v1_1_c, v2_1_c, b1_1_c, b2_1_c = v1_1, v2_1, b1_1, b2_1
                if sf_3 > 0:
                    v1_1_c, v2_1_c, b1_1_c, b2_1_c, sf_my = liquidate_net_target(v1_1, v2_1, b1_1, b2_1, sf_3, 0.70, 0.0)
                else:
                    sf_my = 0.0
                succ_my_comb.append(sf_my == 0.0)
                succ_with_gift.append(sf_my <= 26700.0)
                my_c37 = ((v1_1_c + v2_1_c) + (v1_3 + v2_3) - sf_my)/10000.0
                
                acc1_37.append(a1_pre); acc2_37.append(a2_37); acc3_37.append(a3_post_solo)
                my_comb_37.append(my_c37); all_37.append(my_c37 + a2_37)
                # Update Account 1 if used to cover
                v1_1, v2_1, b1_1, b2_1 = v1_1_c, v2_1_c, b1_1_c, b2_1_c
                
        a1_40 = (v1_1 + v2_1)/10000.0
        a2_40 = (v1_2 + v2_2)/10000.0
        a3_40 = ((v1_3 + v2_3) - sf_3)/10000.0
        my_c40 = ((v1_1 + v2_1) + (v1_3 + v2_3) - sf_my)/10000.0
        acc1_40.append(a1_40); acc2_40.append(a2_40); acc3_40.append(a3_40)
        my_comb_40.append(my_c40); all_40.append(my_c40 + a2_40)

print("\n=========================================================================================================")
print(" [3개 계좌 20,000회 다중 국면 몬테카를로 확률 전망]")
print("=========================================================================================================")
print(f"  • ③번 계좌(10억) 단독 23억 완납 확률           : {np.mean(succ_acc3_only)*100:.1f}%")
print(f"  • 본인 명의 합산(①SK계좌 + ③10억계좌) 23억 완납 : {np.mean(succ_my_comb)*100:.1f}%")
print(f"  • 본인 합산 + 비과세 가족차용(2.67억) 내 완납  : {np.mean(succ_with_gift)*100:.1f}%")
for p in [25, 50, 60, 65, 70, 75, 90]:
    print(f"  P{p:2d} (상위 {100-p:2d}%) | [2037말] ①SK(상환전): {np.percentile(acc1_37, p):4.2f}억 + ③10억(23억상환후): {np.percentile(acc3_37, p):+6.2f}억 = 본인합산: {np.percentile(my_comb_37, p):+6.2f}억 (②아버지4억: {np.percentile(acc2_37, p):5.2f}억) | [2040말] 본인합산: {np.percentile(my_comb_40, p):+6.2f}억 / ②아버지4억: {np.percentile(acc2_40, p):5.2f}억")
print(f"  평균값 (Mean) | [2037말] ①SK(상환전): {np.mean(acc1_37):4.2f}억 + ③10억(23억상환후): {np.mean(acc3_37):+6.2f}억 = 본인합산: {np.mean(my_comb_37):+6.2f}억 (②아버지4억: {np.mean(acc2_37):5.2f}억) | [2040말] 본인합산: {np.mean(my_comb_40):+6.2f}억 / ②아버지4억: {np.mean(acc2_40):5.2f}억")
