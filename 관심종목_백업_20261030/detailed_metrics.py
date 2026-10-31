import os
import pandas as pd
import numpy as np

# Load data
data_dir = 'data'
def load_series(ticker):
    df = pd.read_csv(os.path.join(data_dir, f'{ticker}.csv'))
    df['Date'] = pd.to_datetime(df['Date'])
    df.set_index('Date', inplace=True)
    return df['AdjClose'].sort_index()

qqq = load_series('QQQ')
smh = load_series('SMH')
gld = load_series('GLD')
iau = load_series('IAU')
schd = load_series('SCHD')
xlv = load_series('XLV')
xlk = load_series('XLK')
vgt = load_series('VGT')

def run_simulation(weights_dict, start_date=None, end_date=None):
    # weights_dict: {'SMH': 0.7, 'GLD': 0.3}
    tickers = list(weights_dict.keys())
    series_list = [load_series(t) for t in tickers]
    
    # Common index
    common_idx = qqq.index
    for s in series_list:
        common_idx = common_idx.intersection(s.index)
        
    if start_date:
        common_idx = common_idx[common_idx >= pd.to_datetime(start_date)]
    if end_date:
        common_idx = common_idx[common_idx <= pd.to_datetime(end_date)]
        
    prices = pd.DataFrame({t: load_series(t).loc[common_idx] for t in tickers})
    pq = qqq.loc[common_idx]
    
    n = len(common_idx)
    years = common_idx.year
    rebalance_mask = np.zeros(n, dtype=bool)
    rebalance_mask[0] = True
    for i in range(1, n):
        if years[i] != years[i-1]:
            rebalance_mask[i] = True
            
    # Simulate portfolio
    port_val = np.zeros(n)
    port_val[0] = 10000.0
    shares = {t: (port_val[0] * weights_dict[t]) / prices[t].iloc[0] for t in tickers}
    
    for i in range(1, n):
        if rebalance_mask[i]:
            current_val = sum(shares[t] * prices[t].iloc[i] for t in tickers)
            port_val[i] = current_val
            for t in tickers:
                shares[t] = (current_val * weights_dict[t]) / prices[t].iloc[i]
        else:
            port_val[i] = sum(shares[t] * prices[t].iloc[i] for t in tickers)
            
    # QQQ
    qqq_val = 10000.0 * (pq / pq.iloc[0]).values
    
    total_years = (common_idx[-1] - common_idx[0]).days / 365.25
    cagr_port = (port_val[-1] / port_val[0]) ** (1 / total_years) - 1
    cagr_qqq = (qqq_val[-1] / qqq_val[0]) ** (1 / total_years) - 1
    
    # Drawdowns
    peak_port = np.maximum.accumulate(port_val)
    dd_port = (port_val - peak_port) / peak_port
    mdd_port = dd_port.min()
    
    peak_qqq = np.maximum.accumulate(qqq_val)
    dd_qqq = (qqq_val - peak_qqq) / peak_qqq
    mdd_qqq = dd_qqq.min()
    
    # Returns & Vol
    daily_ret_p = np.diff(port_val) / port_val[:-1]
    daily_ret_q = np.diff(qqq_val) / qqq_val[:-1]
    
    vol_port = np.std(daily_ret_p) * np.sqrt(252)
    vol_qqq = np.std(daily_ret_q) * np.sqrt(252)
    
    rf = 0.02
    sharpe_p = (cagr_port - rf) / vol_port
    sharpe_q = (cagr_qqq - rf) / vol_qqq
    
    neg_ret_p = daily_ret_p[daily_ret_p < 0]
    downside_vol_p = np.std(neg_ret_p) * np.sqrt(252) if len(neg_ret_p) > 0 else vol_port
    sortino_p = (cagr_port - rf) / downside_vol_p
    
    neg_ret_q = daily_ret_q[daily_ret_q < 0]
    downside_vol_q = np.std(neg_ret_q) * np.sqrt(252) if len(neg_ret_q) > 0 else vol_qqq
    sortino_q = (cagr_qqq - rf) / downside_vol_q
    
    calmar_p = cagr_port / abs(mdd_port)
    calmar_q = cagr_qqq / abs(mdd_qqq)
    
    # Calendar year returns
    df_ts = pd.DataFrame({
        'Port': port_val,
        'QQQ': qqq_val
    }, index=common_idx)
    
    yearly = df_ts.resample('YE').last().pct_change().dropna()
    # First year partial or full
    first_year_p = (df_ts['Port'].loc[str(common_idx[0].year)].iloc[-1] / df_ts['Port'].iloc[0]) - 1
    first_year_q = (df_ts['QQQ'].loc[str(common_idx[0].year)].iloc[-1] / df_ts['QQQ'].iloc[0]) - 1
    
    return {
        'start_date': common_idx[0].strftime('%Y-%m-%d'),
        'end_date': common_idx[-1].strftime('%Y-%m-%d'),
        'years': round(total_years, 2),
        'initial': port_val[0],
        'final_port': port_val[-1],
        'final_qqq': qqq_val[-1],
        'cagr_port': cagr_port,
        'cagr_qqq': cagr_qqq,
        'mdd_port': mdd_port,
        'mdd_qqq': mdd_qqq,
        'vol_port': vol_port,
        'vol_qqq': vol_qqq,
        'sharpe_port': sharpe_p,
        'sharpe_qqq': sharpe_q,
        'sortino_port': sortino_p,
        'sortino_qqq': sortino_q,
        'calmar_port': calmar_p,
        'calmar_qqq': calmar_q,
        'yearly': yearly,
        'df_ts': df_ts
    }

print('Simulation engine ready.')
