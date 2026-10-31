import os
import time
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

def analyze_horizon(start_date, label):
    valid, idx, yrs, eval_fn = build_fast_evaluator(start_date)
    print(f"\n================================================================================")
    print(f"HORIZON: {label} ({idx[0].strftime('%Y-%m-%d')} ~ {idx[-1].strftime('%Y-%m-%d')}, {yrs:.1f} yrs, {len(valid)} ETFs)")
    print(f"================================================================================")
    
    q_fv, q_cagr, q_mdd, q_vol, q_sh, q_cal = eval_fn('QQQ', 'QQQ', np.array([1.0]))
    print(f"QQQ (100%)           : Final=${q_fv[0]:,.0f} | CAGR={q_cagr[0]:.2%} | MDD={q_mdd[0]:.2%} | Sharpe={q_sh[0]:.3f} | Calmar={q_cal[0]:.3f}")
    
    if 'SCHD' in valid:
        b_fv, b_cagr, b_mdd, b_vol, b_sh, b_cal = eval_fn('SMH', 'SCHD', np.array([0.60]))
        b_cagr, b_mdd, b_sh, b_cal, b_fv = b_cagr[0], b_mdd[0], b_sh[0], b_cal[0], b_fv[0]
        print(f"Baseline SMH60+SCHD40: Final=${b_fv:,.0f} | CAGR={b_cagr:.2%} | MDD={b_mdd:.2%} | Sharpe={b_sh:.3f} | Calmar={b_cal:.3f}")
    else:
        b_fv, b_cagr, b_mdd, b_vol, b_sh, b_cal = eval_fn('SMH', 'GLD', np.array([0.70]))
        b_cagr, b_mdd, b_sh, b_cal, b_fv = b_cagr[0], b_mdd[0], b_sh[0], b_cal[0], b_fv[0]
        print(f"Ref SMH70+GLD30      : Final=${b_fv:,.0f} | CAGR={b_cagr:.2%} | MDD={b_mdd:.2%} | Sharpe={b_sh:.3f} | Calmar={b_cal:.3f}")

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
    print(f"\n[Strict Dominance: Both Higher CAGR & Lower MDD than Baseline] ({len(dom)} found):")
    if len(dom) > 0:
        print(dom[['Pair', 'CAGR', 'MDD', 'Sharpe', 'Calmar', 'Final']].head(15).to_string(index=False))
        
    better = df[(df['CAGR'] > b_cagr) & (df['Sharpe'] > b_sh) & (df['MDD'] > q_mdd[0])].sort_values(by='CAGR', ascending=False)
    print(f"\n[Higher CAGR & Higher Sharpe than Baseline, MDD < QQQ] ({len(better)} found):")
    if len(better) > 0:
        print(better[['Pair', 'CAGR', 'MDD', 'Sharpe', 'Calmar', 'Final']].head(15).to_string(index=False))

analyze_horizon('2014-06-15', '2014~2026 (Includes MOAT, QUAL, MTUM, DGRO, NOBL, FTEC)')
analyze_horizon('2016-12-23', '2017~2026 (Includes COWZ, SPMO)')
analyze_horizon('2007-03-05', '2007~2026 (Includes 2008 GFC, UUP, PPA, XLV, GLD, VIG, FDL)')
