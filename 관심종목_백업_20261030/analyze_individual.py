import os
import pandas as pd
import numpy as np

data_dir = 'data'
files = [f for f in os.listdir(data_dir) if f.endswith('.csv')]

qqq_df = pd.read_csv(os.path.join(data_dir, 'QQQ.csv'))
qqq_df['Date'] = pd.to_datetime(qqq_df['Date'])
qqq_df.set_index('Date', inplace=True)
qqq_series = qqq_df['AdjClose']

results = []

for f in files:
    ticker = f.replace('.csv', '')
    df = pd.read_csv(os.path.join(data_dir, f))
    df['Date'] = pd.to_datetime(df['Date'])
    df.set_index('Date', inplace=True)
    series = df['AdjClose']
    
    # Common dates with QQQ
    common_dates = series.index.intersection(qqq_series.index)
    if len(common_dates) < 252 * 5: # At least 5 years
        continue
    
    sub_s = series.loc[common_dates].sort_index()
    sub_q = qqq_series.loc[common_dates].sort_index()
    
    start_date = common_dates[0]
    end_date = common_dates[-1]
    years = (end_date - start_date).days / 365.25
    
    # CAGR
    cagr_etf = (sub_s.iloc[-1] / sub_s.iloc[0]) ** (1 / years) - 1
    cagr_qqq = (sub_q.iloc[-1] / sub_q.iloc[0]) ** (1 / years) - 1
    
    # Daily returns
    ret_etf = sub_s.pct_change().dropna()
    ret_qqq = sub_q.pct_change().dropna()
    
    # MDD
    cum_etf = (1 + ret_etf).cumprod()
    peak_etf = cum_etf.cummax()
    dd_etf = (cum_etf - peak_etf) / peak_etf
    mdd_etf = dd_etf.min()
    
    cum_qqq = (1 + ret_qqq).cumprod()
    peak_qqq = cum_qqq.cummax()
    dd_qqq = (cum_qqq - peak_qqq) / peak_qqq
    mdd_qqq = dd_qqq.min()
    
    # Annualized Volatility
    vol_etf = ret_etf.std() * np.sqrt(252)
    vol_qqq = ret_qqq.std() * np.sqrt(252)
    
    # Sharpe (rf = 0.02)
    sharpe_etf = (cagr_etf - 0.02) / vol_etf
    sharpe_qqq = (cagr_qqq - 0.02) / vol_qqq
    
    results.append({
        'Ticker': ticker,
        'StartDate': start_date.strftime('%Y-%m-%d'),
        'Years': round(years, 1),
        'CAGR': cagr_etf,
        'QQQ_CAGR': cagr_qqq,
        'Diff_CAGR': cagr_etf - cagr_qqq,
        'MDD': mdd_etf,
        'QQQ_MDD': mdd_qqq,
        'Vol': vol_etf,
        'Sharpe': sharpe_etf
    })

res_df = pd.DataFrame(results)
res_df.sort_values(by='Diff_CAGR', ascending=False, inplace=True)
print('--- Top Outperformers vs QQQ over their common history ---')
print(res_df[res_df['Diff_CAGR'] > 0][['Ticker', 'StartDate', 'Years', 'CAGR', 'QQQ_CAGR', 'Diff_CAGR', 'MDD', 'QQQ_MDD', 'Sharpe']].to_string())

print('\n--- All ETFs summary ---')
print(res_df[['Ticker', 'StartDate', 'Years', 'CAGR', 'QQQ_CAGR', 'Diff_CAGR', 'MDD', 'QQQ_MDD']].head(20).to_string())
