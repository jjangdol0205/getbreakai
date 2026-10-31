import os
import itertools
import pandas as pd
import numpy as np

data_dir = 'data'
files = [f for f in os.listdir(data_dir) if f.endswith('.csv')]
series_dict = {}
for f in sorted(files):
    ticker = f.replace('.csv', '')
    df = pd.read_csv(os.path.join(data_dir, f))
    df['Date'] = pd.to_datetime(df['Date'])
    df.set_index('Date', inplace=True)
    series_dict[ticker] = df['AdjClose'].sort_index()

print(f"Total tickers loaded: {len(series_dict)}")

def build_fast_evaluator(start_date_str, min_start_tolerance_days=10):
    start_dt = pd.to_datetime(start_date_str)
    qqq_s = series_dict['QQQ']
    base_idx = qqq_s.index[qqq_s.index >= start_dt]
    
    valid_tickers = []
    aligned_prices = {}
    for t, s in series_dict.items():
        if s.index[0] <= base_idx[0] + pd.Timedelta(days=min_start_tolerance_days):
            sub = s.reindex(base_idx).ffill().bfill()
            if not sub.isna().any():
                valid_tickers.append(t)
                aligned_prices[t] = sub.values.astype(np.float64)
                
    n_days = len(base_idx)
    years = base_idx.year.values
    total_years = (base_idx[-1] - base_idx[0]).days / 365.25
    
    reb_indices = [0]
    for i in range(1, n_days):
        if years[i] != years[i-1]:
            reb_indices.append(i)
    reb_indices = np.array(reb_indices)
    n_periods = len(reb_indices)
    
    day_to_period = np.zeros(n_days, dtype=np.int32)
    for p_idx in range(n_periods):
        start_i = reb_indices[p_idx]
        end_i = reb_indices[p_idx + 1] if p_idx + 1 < n_periods else n_days
        day_to_period[start_i:end_i] = p_idx
        
    rel_curves = {}
    period_transitions = {}
    for t in valid_tickers:
        p = aligned_prices[t]
        p_reb = p[reb_indices]
        rel_curves[t] = p / p_reb[day_to_period]
        period_transitions[t] = p_reb[1:] / p_reb[:-1] if n_periods > 1 else np.array([])
            
    def eval_pair_weights(t1, t2, weights_arr):
        w1 = weights_arr[:, None]
        w2 = 1.0 - w1
        trans = w1 * period_transitions[t1][None, :] + w2 * period_transitions[t2][None, :]
        period_start_wealth = np.ones((len(weights_arr), n_periods), dtype=np.float64) * 10000.0
        if n_periods > 1:
            period_start_wealth[:, 1:] = 10000.0 * np.cumprod(trans, axis=1)
        daily_base = period_start_wealth[:, day_to_period]
        daily_rel = w1 * rel_curves[t1][None, :] + w2 * rel_curves[t2][None, :]
        port_vals = daily_base * daily_rel
        
        final_vals = port_vals[:, -1]
        cagrs = (final_vals / 10000.0) ** (1.0 / total_years) - 1.0
        peaks = np.maximum.accumulate(port_vals, axis=1)
        mdds = ((port_vals - peaks) / peaks).min(axis=1)
        daily_rets = np.diff(port_vals, axis=1) / port_vals[:, :-1]
        vols = np.std(daily_rets, axis=1) * np.sqrt(252)
        sharpes = (cagrs - 0.02) / vols
        calmars = cagrs / np.abs(mdds)
        return final_vals, cagrs, mdds, vols, sharpes, calmars

    return valid_tickers, base_idx, total_years, eval_pair_weights

for start_str, label in [
    ('2011-10-20', '15.0 Yrs (2011~2026)'),
    ('2006-05-10', '20.4 Yrs (2006~2026, Includes 2008 GFC + 2020 + 2022)')
]:
    valid, idx, yrs, eval_fn = build_fast_evaluator(start_str)
    b_fv, b_cagr, b_mdd, b_vol, b_sh, b_cal = eval_fn('SMH', 'XLV', np.array([0.60]))
    b_fv, b_cagr, b_mdd, b_vol, b_sh, b_cal = b_fv[0], b_cagr[0], b_mdd[0], b_vol[0], b_sh[0], b_cal[0]
    
    b65_fv, b65_cagr, b65_mdd, b65_vol, b65_sh, b65_cal = eval_fn('SMH', 'XLV', np.array([0.65]))
    
    print(f"\n================================================================================")
    print(f"[{label}] ({len(valid)} ETFs)")
    print(f"BASELINE SMH(60%)+XLV(40%): CAGR={b_cagr:.2%}, MDD={b_mdd:.2%}, Sharpe={b_sh:.3f}, Calmar={b_cal:.3f}, Final=${b_fv:,.0f}")
    print(f"BASELINE SMH(65%)+XLV(35%): CAGR={b65_cagr[0]:.2%}, MDD={b65_mdd[0]:.2%}, Sharpe={b65_sh[0]:.3f}, Calmar={b65_cal[0]:.3f}, Final=${b65_fv[0]:,.0f}")
    print(f"================================================================================")
    
    weights_grid = np.round(np.arange(0.10, 0.95, 0.05), 2)
    pairs = list(itertools.combinations(valid, 2))
    rows = []
    for t1, t2 in pairs:
        fvs, cagrs, mdds, vols, shs, cals = eval_fn(t1, t2, weights_grid)
        for k, w1 in enumerate(weights_grid):
            w2 = round(1.0 - w1, 2)
            rows.append({
                'Pair': f"{t1}({int(round(w1*100))}%) + {t2}({int(round(w2*100))}%)",
                'T1': t1, 'T2': t2, 'W1': w1, 'W2': w2,
                'Final': fvs[k], 'CAGR': cagrs[k], 'MDD': mdds[k], 'Vol': vols[k],
                'Sharpe': shs[k], 'Calmar': cals[k]
            })
    df = pd.DataFrame(rows)
    
    dom = df[(df['CAGR'] > b_cagr) & (df['MDD'] > b_mdd)].sort_values(by='CAGR', ascending=False)
    print(f"\n--> A. Strict Dominance over SMH(60)+XLV(40) (CAGR > {b_cagr:.2%} AND MDD > {b_mdd:.2%}) [{len(dom)} found]:")
    if len(dom) > 0:
        print(dom[['Pair', 'CAGR', 'MDD', 'Sharpe', 'Calmar', 'Final']].head(20).to_string(index=False))
        
    sh_dom = df[(df['Sharpe'] > b_sh) & (df['CAGR'] >= b_cagr - 0.015)].sort_values(by='Sharpe', ascending=False)
    print(f"\n--> B. Higher Sharpe (> {b_sh:.3f}) with High CAGR [{len(sh_dom)} found]:")
    if len(sh_dom) > 0:
        print(sh_dom[['Pair', 'CAGR', 'MDD', 'Sharpe', 'Calmar', 'Final']].head(15).to_string(index=False))
