import pandas as pd
import numpy as np
from detailed_metrics import run_simulation, load_series

# 1. SMH 70% + GLD 30% (From 2005-01-01 to 2026-10)
sim_smh_gld = run_simulation({'SMH': 0.70, 'GLD': 0.30}, start_date='2005-01-01')

# 2. SMH 60% + GLD 40%
sim_smh_gld60 = run_simulation({'SMH': 0.60, 'GLD': 0.40}, start_date='2005-01-01')

# 3. SMH 60% + SCHD 40% (From 2011-10-20 to 2026-10)
sim_smh_schd = run_simulation({'SMH': 0.60, 'SCHD': 0.40}, start_date='2011-10-20')

# 4. SMH 60% + XLV 40% (From 2000-06-05 to 2026-10)
sim_smh_xlv_full = run_simulation({'SMH': 0.60, 'XLV': 0.40}, start_date='2000-06-05')
sim_smh_xlv_2005 = run_simulation({'SMH': 0.60, 'XLV': 0.40}, start_date='2005-01-01')

print('======================================================================')
print('STRATEGY 1: SMH 70% + GLD 30% (2005 - 2026, 21.8 Years)')
print('======================================================================')
print(f'Final Value ($10k inv): Portfolio ${sim_smh_gld["final_port"]:,.0f} | QQQ ${sim_smh_gld["final_qqq"]:,.0f}')
print(f'CAGR:                  Portfolio {sim_smh_gld["cagr_port"]:.2%} | QQQ {sim_smh_gld["cagr_qqq"]:.2%} (Diff: {sim_smh_gld["cagr_port"]-sim_smh_gld["cagr_qqq"]:+.2%})')
print(f'MDD:                   Portfolio {sim_smh_gld["mdd_port"]:.2%} | QQQ {sim_smh_gld["mdd_qqq"]:.2%} (Milder by: {abs(sim_smh_gld["mdd_qqq"])-abs(sim_smh_gld["mdd_port"]):.2%})')
print(f'Sharpe Ratio:          Portfolio {sim_smh_gld["sharpe_port"]:.2f} | QQQ {sim_smh_gld["sharpe_qqq"]:.2f}')
print(f'Sortino Ratio:         Portfolio {sim_smh_gld["sortino_port"]:.2f} | QQQ {sim_smh_gld["sortino_qqq"]:.2f}')
print(f'Calmar Ratio:          Portfolio {sim_smh_gld["calmar_port"]:.2f} | QQQ {sim_smh_gld["calmar_qqq"]:.2f}')

print('\n======================================================================')
print('STRATEGY 1B: SMH 60% + GLD 40% (2005 - 2026, 21.8 Years)')
print('======================================================================')
print(f'Final Value ($10k inv): Portfolio ${sim_smh_gld60["final_port"]:,.0f} | QQQ ${sim_smh_gld60["final_qqq"]:,.0f}')
print(f'CAGR:                  Portfolio {sim_smh_gld60["cagr_port"]:.2%} | QQQ {sim_smh_gld60["cagr_qqq"]:.2%}')
print(f'MDD:                   Portfolio {sim_smh_gld60["mdd_port"]:.2%} | QQQ {sim_smh_gld60["mdd_qqq"]:.2%}')
print(f'Sharpe Ratio:          Portfolio {sim_smh_gld60["sharpe_port"]:.2f} | QQQ {sim_smh_gld60["sharpe_qqq"]:.2f}')

print('\n======================================================================')
print('STRATEGY 2: SMH 60% + SCHD 40% (2011 - 2026, 15.0 Years)')
print('======================================================================')
print(f'Final Value ($10k inv): Portfolio ${sim_smh_schd["final_port"]:,.0f} | QQQ ${sim_smh_schd["final_qqq"]:,.0f}')
print(f'CAGR:                  Portfolio {sim_smh_schd["cagr_port"]:.2%} | QQQ {sim_smh_schd["cagr_qqq"]:.2%} (Diff: {sim_smh_schd["cagr_port"]-sim_smh_schd["cagr_qqq"]:+.2%})')
print(f'MDD:                   Portfolio {sim_smh_schd["mdd_port"]:.2%} | QQQ {sim_smh_schd["mdd_qqq"]:.2%} (Milder by: {abs(sim_smh_schd["mdd_qqq"])-abs(sim_smh_schd["mdd_port"]):.2%})')
print(f'Sharpe Ratio:          Portfolio {sim_smh_schd["sharpe_port"]:.2f} | QQQ {sim_smh_schd["sharpe_qqq"]:.2f}')
print(f'Sortino Ratio:         Portfolio {sim_smh_schd["sortino_port"]:.2f} | QQQ {sim_smh_schd["sortino_qqq"]:.2f}')
print(f'Calmar Ratio:          Portfolio {sim_smh_schd["calmar_port"]:.2f} | QQQ {sim_smh_schd["calmar_qqq"]:.2f}')

print('\n======================================================================')
print('STRATEGY 3: SMH 60% + XLV 40% (2000 - 2026, 26.4 Years)')
print('======================================================================')
print(f'Final Value ($10k inv): Portfolio ${sim_smh_xlv_full["final_port"]:,.0f} | QQQ ${sim_smh_xlv_full["final_qqq"]:,.0f}')
print(f'CAGR:                  Portfolio {sim_smh_xlv_full["cagr_port"]:.2%} | QQQ {sim_smh_xlv_full["cagr_qqq"]:.2%}')
print(f'MDD:                   Portfolio {sim_smh_xlv_full["mdd_port"]:.2%} | QQQ {sim_smh_xlv_full["mdd_qqq"]:.2%}')

# Crisis period breakdown for SMH 70% + GLD 30%
print('\n======================================================================')
print('CRISIS BREAKDOWN: SMH 70% + GLD 30% vs QQQ')
print('======================================================================')
crises = [
    ('2008 Financial Crisis', '2007-10-01', '2009-03-31'),
    ('2018 Rate Hike / Trade War', '2018-09-01', '2018-12-31'),
    ('2020 COVID Crash', '2020-02-01', '2020-04-30'),
    ('2022 Inflation & Rate Hike Bear Market', '2021-12-31', '2022-12-31')
]

for name, s_date, e_date in crises:
    sim_c = run_simulation({'SMH': 0.70, 'GLD': 0.30}, start_date=s_date, end_date=e_date)
    p_ret = (sim_c['final_port'] / sim_c['initial']) - 1
    q_ret = (sim_c['final_qqq'] / sim_c['initial']) - 1
    print(f'[{name}] ({s_date} ~ {e_date})')
    print(f'  Portfolio Return: {p_ret:+.2%} | Max Drawdown: {sim_c["mdd_port"]:.2%}')
    print(f'  QQQ Return:       {q_ret:+.2%} | Max Drawdown: {sim_c["mdd_qqq"]:.2%}')

# Crisis breakdown for SMH 60% + SCHD 40% (since 2011)
print('\n======================================================================')
print('CRISIS BREAKDOWN: SMH 60% + SCHD 40% vs QQQ')
print('======================================================================')
for name, s_date, e_date in crises[1:]:
    sim_c = run_simulation({'SMH': 0.60, 'SCHD': 0.40}, start_date=s_date, end_date=e_date)
    p_ret = (sim_c['final_port'] / sim_c['initial']) - 1
    q_ret = (sim_c['final_qqq'] / sim_c['initial']) - 1
    print(f'[{name}] ({s_date} ~ {e_date})')
    print(f'  Portfolio Return: {p_ret:+.2%} | Max Drawdown: {sim_c["mdd_port"]:.2%}')
    print(f'  QQQ Return:       {q_ret:+.2%} | Max Drawdown: {sim_c["mdd_qqq"]:.2%}')
