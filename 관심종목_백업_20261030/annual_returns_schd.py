import pandas as pd
from detailed_metrics import run_simulation

sim_smh_schd = run_simulation({'SMH': 0.60, 'SCHD': 0.40}, start_date='2011-10-20')
df_ts = sim_smh_schd['df_ts']

# Yearly returns
yearly = df_ts.resample('YE').last().pct_change().dropna()
# Also add 2011 first year
y2011_p = (df_ts['Port'].loc['2011'].iloc[-1] / df_ts['Port'].iloc[0]) - 1
y2011_q = (df_ts['QQQ'].loc['2011'].iloc[-1] / df_ts['QQQ'].iloc[0]) - 1

records = [{'Year': 2011, 'Port_Return': y2011_p, 'QQQ_Return': y2011_q, 'Diff': y2011_p - y2011_q}]
for date, row in yearly.iterrows():
    p = row['Port']
    q = row['QQQ']
    records.append({'Year': date.year, 'Port_Return': p, 'QQQ_Return': q, 'Diff': p - q})

y2026_p = (df_ts['Port'].iloc[-1] / df_ts['Port'].loc['2025'].iloc[-1]) - 1
y2026_q = (df_ts['QQQ'].iloc[-1] / df_ts['QQQ'].loc['2025'].iloc[-1]) - 1
records.append({'Year': '2026 (YTD)', 'Port_Return': y2026_p, 'QQQ_Return': y2026_q, 'Diff': y2026_p - y2026_q})

df_cal = pd.DataFrame(records)
print('======================================================================')
print('ANNUAL RETURNS: SMH 60% + SCHD 40% vs QQQ (2011 - 2026)')
print('======================================================================')
for _, r in df_cal.iterrows():
    y = r['Year']
    p = r['Port_Return']
    q = r['QQQ_Return']
    diff = r['Diff']
    win = 'PORT' if diff > 0 else 'QQQ'
    print(f"{y:>10} | Port: {p:>7.2%} | QQQ: {q:>7.2%} | Diff: {diff:>+7.2%} [{win}]")

port_wins = sum(1 for r in records if r['Diff'] > 0)
total_years = len(records)
print(f"\nPortfolio won in {port_wins} out of {total_years} years ({port_wins/total_years:.1%})")
