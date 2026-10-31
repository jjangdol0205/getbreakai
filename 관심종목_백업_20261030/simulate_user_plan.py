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
smh_c = df_smh.loc[common, 'Close'].astype(float)
smh_a = df_smh.loc[common, 'AdjClose'].astype(float)
xlv_c = df_xlv.loc[common, 'Close'].astype(float)
xlv_a = df_xlv.loc[common, 'AdjClose'].astype(float)

# Create monthly total return series (after 15.4% dividend tax)
pr_smh = smh_c.pct_change().fillna(0.0)
tr_smh = smh_a.pct_change().fillna(0.0)
div_smh = np.maximum(0.0, tr_smh - pr_smh)
net_ret_smh = pr_smh + div_smh * (1.0 - 0.154)

pr_xlv = xlv_c.pct_change().fillna(0.0)
tr_xlv = xlv_a.pct_change().fillna(0.0)
div_xlv = np.maximum(0.0, tr_xlv - pr_xlv)
net_ret_xlv = pr_xlv + div_xlv * (1.0 - 0.154)

# Build monthly return dataframe
df_daily_net = pd.DataFrame({'SMH': (1 + net_ret_smh).cumprod(), 'XLV': (1 + net_ret_xlv).cumprod()}, index=common)
df_monthly = df_daily_net.resample('ME').last()
m_ret_smh = df_monthly['SMH'].pct_change().dropna()
m_ret_xlv = df_monthly['XLV'].pct_change().dropna()
m_dates = m_ret_smh.index

# ==============================================================================
# PART 1: 400M KRW (4억 원), Monthly 3M KRW (월 300만 원) Withdrawal Simulation
# ==============================================================================
def sim_part1_withdrawal(start_ym, n_years=10, init_krw=40000, monthly_wd=300, w1_target=0.60, smart_wd=True, delay_months=0):
    # Units in 만원 (4억 = 40,000만원, 월 300만원 = 300만원)
    sub_idx = m_dates[m_dates >= pd.to_datetime(start_ym)]
    if len(sub_idx) < n_years * 12:
        n_months = len(sub_idx)
    else:
        n_months = n_years * 12
    sub_idx = sub_idx[:n_months]
    
    tx_cost = 0.0015
    v1 = init_krw * w1_target * (1 - tx_cost)
    v2 = init_krw * (1 - w1_target) * (1 - tx_cost)
    
    yearly_log = []
    total_withdrawn = 0.0
    min_bal = init_krw
    
    for m_i, dt in enumerate(sub_idx):
        # Apply monthly return
        v1 *= (1.0 + m_ret_smh.loc[dt])
        v2 *= (1.0 + m_ret_xlv.loc[dt])
        
        # Monthly withdrawal (if past delay_months)
        if m_i >= delay_months:
            tot = v1 + v2
            if tot <= monthly_wd:
                v1 = 0; v2 = 0
                break
            if smart_wd:
                # Withdraw from the overweight asset relative to 60:40 target
                cur_w1 = v1 / tot
                if cur_w1 >= w1_target:
                    # Take from SMH first
                    excess1 = v1 - (tot - monthly_wd) * w1_target
                    take1 = min(monthly_wd, max(0.0, excess1))
                    take2 = monthly_wd - take1
                else:
                    excess2 = v2 - (tot - monthly_wd) * (1 - w1_target)
                    take2 = min(monthly_wd, max(0.0, excess2))
                    take1 = monthly_wd - take2
                v1 -= take1 * (1 + tx_cost)
                v2 -= take2 * (1 + tx_cost)
            else:
                v1 -= monthly_wd * w1_target * (1 + tx_cost)
                v2 -= monthly_wd * (1 - w1_target) * (1 + tx_cost)
            total_withdrawn += monthly_wd
            
        # Annual rebalance every 12 months
        if (m_i + 1) % 12 == 0:
            tot = v1 + v2
            # Check 12m return of SMH for contrarian tilt
            t1_target_now = w1_target
            diff1 = v1 - tot * t1_target_now
            if abs(diff1) > tot * 0.02:
                cost = abs(diff1) * tx_cost * 2
                tot_after = tot - cost
                v1 = tot_after * t1_target_now
                v2 = tot_after * (1 - t1_target_now)
            yearly_log.append(( (m_i+1)//12, dt.strftime('%Y-%m'), total_withdrawn, v1 + v2 ))
            
        min_bal = min(min_bal, v1 + v2)
        
    return yearly_log, total_withdrawn, v1 + v2, min_bal

print("=== [PART 1] 4억 원 시작 + 월 300만 원 인출 백테스트 (최근 10년: 2016.10 ~ 2026.10) ===")
log_10y, wd_10y, fin_10y, min_10y = sim_part1_withdrawal('2016-10-01', n_years=10, smart_wd=True, delay_months=0)
for yr, ym, wd, bal in log_10y:
    print(f"  {yr:2d}년차 ({ym}) | 누적 인출액: {wd:6,.0f}만 원 | 남은 계좌 잔고: {bal:8,.0f}만 원 ({bal/10000:.2f}억 원)")

print("\n=== [PART 1-B] 만약 SK스퀘어 잔여분(15개월)을 먼저 쓰고 4억 원 인출을 15개월 유예했을 때 (2016.10 ~ 2026.10) ===")
log_10y_d, wd_10y_d, fin_10y_d, min_10y_d = sim_part1_withdrawal('2016-10-01', n_years=10, smart_wd=True, delay_months=15)
print(f"  즉시 인출 시 10년 후 잔고: {fin_10y:,.0f}만 원 ({fin_10y/10000:.2f}억 원) [최저 잔고: {min_10y:,.0f}만 원]")
print(f"  15개월 유예 시 10년 후 잔고: {fin_10y_d:,.0f}만 원 ({fin_10y_d/10000:.2f}억 원) [최저 잔고: {min_10y_d:,.0f}만 원] -> 잔고 +{fin_10y_d - fin_10y:,.0f}만 원 증가!")

print("\n=== [PART 1-C] 최악의 폭락장 직전 시작 스트레스 테스트 (2022년 1월 최고점 시작 ~ 2026.10, 4년 9개월) ===")
log_22, wd_22, fin_22, min_22 = sim_part1_withdrawal('2022-01-01', n_years=5, smart_wd=True, delay_months=0)
for yr, ym, wd, bal in log_22:
    print(f"  {yr:2d}년차 ({ym}) | 누적 인출액: {wd:6,.0f}만 원 | 남은 계좌 잔고: {bal:8,.0f}만 원 ({bal/10000:.2f}억 원)")
print(f"  2022년 폭락장 중 최저 계좌 잔고: {min_22:,.0f}만 원 ({min_22/10000:.2f}억 원) | 2026.10 현재 잔고: {fin_22:,.0f}만 원 ({fin_22/10000:.2f}억 원, 누적 인출 {wd_22:,.0f}만 원)")

# Rolling 10-year window analysis for Part 1 (from 2005 to 2026)
start_candidates = m_dates[(m_dates >= '2005-01-01') & (m_dates <= '2016-10-31')]
finals_p1 = []
mins_p1 = []
for sc in start_candidates:
    _, _, f_b, m_b = sim_part1_withdrawal(sc.strftime('%Y-%m-%d'), n_years=10, smart_wd=True, delay_months=0)
    finals_p1.append(f_b)
    mins_p1.append(m_b)
finals_p1 = np.array(finals_p1)
mins_p1 = np.array(mins_p1)
print(f"\n=== [PART 1 ROLLING 10-YEAR WINDOWS (2005~2026, {len(finals_p1)}개 구간, 2008 금융위기 포함)] ===")
print(f"  10년간 3억 6,000만 원 인출 후 원금(4억) 이상 유지 확률: {(finals_p1 >= 40000).mean():.1%}")
print(f"  10년간 원금 고갈(0원) 발생 건수: {(finals_p1 <= 0).sum()}건 (0.0%)")
print(f"  10년 후 잔고 - 최악(Worst): {np.min(finals_p1):,.0f}만 원 ({np.min(finals_p1)/10000:.2f}억) | 하위25%: {np.percentile(finals_p1, 25):,.0f}만 원 ({np.percentile(finals_p1, 25)/10000:.2f}억) | 중위값(Median): {np.median(finals_p1):,.0f}만 원 ({np.median(finals_p1)/10000:.2f}억) | 상위25%: {np.percentile(finals_p1, 75):,.0f}만 원 ({np.percentile(finals_p1, 75)/10000:.2f}억)")

# ==============================================================================
# PART 2: 1,000M KRW (10억 원), 8 Years, 4%/yr Interest Paid at Maturity (만기 일시 납입)
# ==============================================================================
def sim_part2_8yr(start_ym, init_krw=100000, w1_target=0.60):
    # 10억 = 100,000만원
    sub_idx = m_dates[m_dates >= pd.to_datetime(start_ym)][:8*12]
    tx_cost = 0.0015
    cg_tax = 0.22
    v1 = init_krw * w1_target * (1 - tx_cost)
    v2 = init_krw * (1 - w1_target) * (1 - tx_cost)
    b1 = v1; b2 = v2
    
    for m_i, dt in enumerate(sub_idx):
        v1 *= (1.0 + m_ret_smh.loc[dt])
        v2 *= (1.0 + m_ret_xlv.loc[dt])
        if (m_i + 1) % 12 == 0 and m_i < 8*12 - 1:
            tot = v1 + v2
            diff1 = v1 - tot * w1_target
            if diff1 > 0:
                frac = diff1 / v1
                cost_sold = b1 * frac
                gain = max(0.0, diff1 - cost_sold)
                tax = max(0.0, (gain - 250.0) * cg_tax) # 250만원 연간 기본공제 반영
                cost = diff1 * tx_cost * 2
                v1 -= diff1; b1 -= cost_sold
                nb2 = diff1 - tax - cost
                v2 += nb2; b2 += nb2
            elif diff1 < 0:
                sell2 = -diff1
                frac = sell2 / v2
                cost_sold = b2 * frac
                gain = max(0.0, sell2 - cost_sold)
                tax = max(0.0, (gain - 250.0) * cg_tax)
                cost = sell2 * tx_cost * 2
                v2 -= sell2; b2 -= cost_sold
                nb1 = sell2 - tax - cost
                v1 += nb1; b1 += nb1
                
    gross_8y = v1 + v2
    # Deduct 22% capital gains tax on remaining unrealized gain at year 8 maturity
    ug = max(0.0, (v1 - b1) + (v2 - b2) - 250.0)
    liq_tax = ug * cg_tax
    net_8y = gross_8y - liq_tax
    return gross_8y, net_8y

start_8y = m_dates[(m_dates >= '2005-01-01') & (m_dates <= '2018-10-31')]
gross_list = []; net_list = []
for sc in start_8y:
    g8, n8 = sim_part2_8yr(sc.strftime('%Y-%m-%d'))
    gross_list.append(g8); net_list.append(n8)
gross_arr = np.array(gross_list)
net_arr = np.array(net_list)

# Also filter for modern era (2011~2018 starts)
start_8y_mod = m_dates[(m_dates >= '2011-01-01') & (m_dates <= '2018-10-31')]
net_mod = np.array([sim_part2_8yr(sc.strftime('%Y-%m-%d'))[1] for sc in start_8y_mod])
gross_mod = np.array([sim_part2_8yr(sc.strftime('%Y-%m-%d'))[0] for sc in start_8y_mod])

print(f"\n=== [PART 2] 10억 원 거치 + 8년 만기 일시 상환 (원금 10억 + 연 4%x8년 이자 3.2억 = 총 13.2억 상환) ===")
print(f"1) 2005~2026 전체 8년 롤링 구간 ({len(net_arr)}개 구간, 2008 금융위기 포함):")
print(f"   - 세후 만기 상환(13.2억) 성공 확률: {(net_arr >= 132000).mean():.1%}")
print(f"   - 최악(Worst, 2007 고점 진입): 세전 {np.min(gross_arr)/10000:.2f}억 / 세후 {np.min(net_arr)/10000:.2f}억 -> 상환 후 순수익 {(np.min(net_arr)-132000)/10000:+.2f}억")
print(f"   - 하위 25%(보수적):            세전 {np.percentile(gross_arr,25)/10000:.2f}억 / 세후 {np.percentile(net_arr,25)/10000:.2f}억 -> 상환 후 순수익 {(np.percentile(net_arr,25)-132000)/10000:+.2f}억")
print(f"   - 중위값(Median):              세전 {np.median(gross_arr)/10000:.2f}억 / 세후 {np.median(net_arr)/10000:.2f}억 -> 상환 후 순수익 {(np.median(net_arr)-132000)/10000:+.2f}억")
print(f"   - 상위 25%(강세장):            세전 {np.percentile(gross_arr,75)/10000:.2f}억 / 세후 {np.percentile(net_arr,75)/10000:.2f}억 -> 상환 후 순수익 {(np.percentile(net_arr,75)-132000)/10000:+.2f}억")

print(f"2) 2011~2026 현대 기술주 구간 ({len(net_mod)}개 구간):")
print(f"   - 세후 만기 상환(13.2억) 성공 확률: {(net_mod >= 132000).mean():.1%}")
print(f"   - 최악(Worst):                 세전 {np.min(gross_mod)/10000:.2f}억 / 세후 {np.min(net_mod)/10000:.2f}억 -> 상환 후 순수익 {(np.min(net_mod)-132000)/10000:+.2f}억")
print(f"   - 중위값(Median):              세전 {np.median(gross_mod)/10000:.2f}억 / 세후 {np.median(net_mod)/10000:.2f}억 -> 상환 후 순수익 {(np.median(net_mod)-132000)/10000:+.2f}억")
print(f"   - 상위 25%(강세장):            세전 {np.percentile(gross_mod,75)/10000:.2f}억 / 세후 {np.percentile(net_mod,75)/10000:.2f}억 -> 상환 후 순수익 {(np.percentile(net_mod,75)-132000)/10000:+.2f}억")
