import pandas as pd
import numpy as np
from detailed_metrics import load_series

soxx = load_series('SOXX')
smh = load_series('SMH')
qqq = load_series('QQQ')
schd = load_series('SCHD')
gld = load_series('GLD')

# Let's inspect SOXX standalone metrics vs SMH and QQQ since 2001
common_2001 = soxx.index.intersection(smh.index).intersection(qqq.index)
p_soxx_2001 = soxx.loc[common_2001]
p_smh_2001 = smh.loc[common_2001]
p_qqq_2001 = qqq.loc[common_2001]

def get_stats(series):
    years = (series.index[-1] - series.index[0]).days / 365.25
    cagr = (series.iloc[-1] / series.iloc[0]) ** (1 / years) - 1
    daily_ret = series.pct_change().dropna()
    vol = daily_ret.std() * np.sqrt(252)
    peak = series.cummax()
    mdd = ((series - peak) / peak).min()
    sharpe = (cagr - 0.02) / vol
    return {'CAGR': cagr, 'MDD': mdd, 'Vol': vol, 'Sharpe': sharpe, 'Final ($10k)': 10000 * (series.iloc[-1]/series.iloc[0])}

print('=== 2001 ~ 2026 (25.3 Years) Standalone ===')
print('SOXX:', get_stats(p_soxx_2001))
print('SMH: ', get_stats(p_smh_2001))
print('QQQ: ', get_stats(p_qqq_2001))

# Compare since 2011 (SCHD inception)
common_2011 = soxx.index.intersection(smh.index).intersection(schd.index).intersection(qqq.index)
print('\n=== 2011 ~ 2026 (15.0 Years) Standalone ===')
print('SOXX:', get_stats(soxx.loc[common_2011]))
print('SMH: ', get_stats(smh.loc[common_2011]))
print('QQQ: ', get_stats(qqq.loc[common_2011]))
