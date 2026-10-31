import os
import time
import itertools
import pandas as pd
import numpy as np

t0 = time.time()
data_dir = 'data'
files = [f for f in os.listdir(data_dir) if f.endswith('.csv')]

series_dict = {}
for f in sorted(files):
    ticker = f.replace('.csv', '')
    df = pd.read_csv(os.path.join(data_dir, f))
    df['Date'] = pd.to_datetime(df['Date'])
    df.set_index('Date', inplace=True)
    series_dict[ticker] = df['AdjClose'].sort_index()

print(f"Loaded {len(series_dict)} ETFs in {time.time() - t0:.2f}s")

def run_fast_grid_search(start_date_str, min_start_tolerance_days=10):
    start_dt = pd.to_datetime(start_date_str)
    qqq_s = series_dict['QQQ']
    base_idx = qqq_s.index[qqq_s.index >= start_dt]
    
    # Filter tickers that have complete data over base_idx
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
    
    # Identify rebalance indices (first trading day of each year)
    reb_indices = [0]
    for i in range(1, n_days):
        if years[i] != years[i-1]:
            reb_indices.append(i)
    reb_indices = np.array(reb_indices)
    n_periods = len(reb_indices)
    
    # Map each day to its period index (0 .. n_periods-1)
    day_to_period = np.zeros(n_days, dtype=np.int32)
    for p_idx in range(n_periods):
        start_i = reb_indices[p_idx]
        end_i = reb_indices[p_idx + 1] if p_idx + 1 < n_periods else n_days
        day_to_period[start_i:end_i] = p_idx
        
    # Precompute for each ticker:
    # 1) rel_curve[t]: P(day) / P(reb_day_of_period)
    # 2) period_Transition[t]: P(reb_day_{p+1}) / P(reb_day_p) for p = 0 .. n_periods-2
    rel_curves = {}
    period_transitions = {}
    for t in valid_tickers:
        p = aligned_prices[t]
        p_reb = p[reb_indices] # shape (n_periods,)
        rel_curves[t] = p / p_reb[day_to_period]
        if n_periods > 1:
            period_transitions[t] = p_reb[1:] / p_reb[:-1]
        else:
            period_transitions[t] = np.array([])
            
    def eval_pair_weights(t1, t2, weights_arr):
        # weights_arr: shape (W, 1)
        w1 = weights_arr[:, None] # (W, 1)
        w2 = 1.0 - w1
        
        # Period transitions: shape (W, n_periods - 1)
        trans = w1 * period_transitions[t1][None, :] + w2 * period_transitions[t2][None, :]
        # Cumulative wealth at start of each period: shape (W, n_periods)
        period_start_wealth = np.ones((len(weights_arr), n_periods), dtype=np.float64) * 10000.0
        if n_periods > 1:
            period_start_wealth[:, 1:] = 10000.0 * np.cumprod(trans, axis=1)
            
        # Expand period_start_wealth to all days: shape (W, n_days)
        daily_base = period_start_wealth[:, day_to_period]
        daily_rel = w1 * rel_curves[t1][None, :] + w2 * rel_curves[t2][None, :]
        port_vals = daily_base * daily_rel # shape (W, n_days)
        
        final_vals = port_vals[:, -1]
        cagrs = (final_vals / 10000.0) ** (1.0 / total_years) - 1.0
        
        peaks = np.maximum.accumulate(port_vals, axis=1)
        dds = (port_vals - peaks) / peaks
        mdds = dds.min(axis=1)
        
        daily_rets = np.diff(port_vals, axis=1) / port_vals[:, :-1]
        vols = np.std(daily_rets, axis=1) * np.sqrt(252)
        sharpes = (cagrs - 0.02) / vols
        calmars = cagrs / np.abs(mdds)
        
        # Sortino
        neg_rets = np.where(daily_rets < 0, daily_rets, 0.0)
        # Note: standard downside deviation or std of negative returns
        sortinos = []
        for idx in range(len(weights_arr)):
            nr = daily_rets[idx][daily_rets[idx] < 0]
            dvol = np.std(nr) * np.sqrt(252) if len(nr) > 0 else vols[idx]
            sortinos.append((cagrs[idx] - 0.02) / dvol)
        sortinos = np.array(sortinos)
        
        return final_vals, cagrs, mdds, vols, sharpes, sortinos, calmars

    return valid_tickers, base_idx, total_years, eval_pair_weights

# Test 1: Modern Era since SCHD inception (2011-10-20 to 2026-10-13, 15.0 years)
valid_2011, idx_2011, yrs_2011, eval_2011 = run_fast_grid_search('2011-10-20')
print(f"\n[2011~2026 ({yrs_2011:.1f} yrs)] Valid ETFs: {len(valid_2011)} -> {valid_2011}")

# Verify baseline SMH 60% + SCHD 40%
b_fv, b_cagr, b_mdd, b_vol, b_sh, b_so, b_cal = eval_2011('SMH', 'SCHD', np.array([0.60]))
b_fv, b_cagr, b_mdd, b_vol, b_sh, b_so, b_cal = b_fv[0], b_cagr[0], b_mdd[0], b_vol[0], b_sh[0], b_so[0], b_cal[0]
print(f"Baseline SMH(60)+SCHD(40): Final=${b_fv:,.0f}, CAGR={b_cagr:.2%}, MDD={b_mdd:.2%}, Vol={b_vol:.2%}, Sharpe={b_sh:.3f}, Sortino={b_so:.3f}, Calmar={b_cal:.3f}")

# Run all pairs and weights from 0.05 to 0.95 step 0.05
weights_grid = np.round(np.arange(0.05, 1.00, 0.05), 2)
pairs_2011 = list(itertools.combinations(valid_2011, 2))

t1_start = time.time()
rows = []
# Also evaluate single ETFs (weight = 1.0)
for t in valid_2011:
    fv, cagr, mdd, vol, sh, so, cal = eval_2011(t, t, np.array([1.0]))
    rows.append({
        'Type': '1-ETF', 'T1': t, 'T2': '-', 'W1': 1.0, 'W2': 0.0,
        'Pair': f"{t}(100%)",
        'Final': fv[0], 'CAGR': cagr[0], 'MDD': mdd[0], 'Vol': vol[0],
        'Sharpe': sh[0], 'Sortino': so[0], 'Calmar': cal[0]
    })

for t1, t2 in pairs_2011:
    fvs, cagrs, mdds, vols, shs, sos, cals = eval_2011(t1, t2, weights_grid)
    for k, w1 in enumerate(weights_grid):
        w2 = round(1.0 - w1, 2)
        # Ensure high-weight or primary ticker is shown cleanly
        rows.append({
            'Type': '2-ETF', 'T1': t1, 'T2': t2, 'W1': w1, 'W2': w2,
            'Pair': f"{t1}({int(round(w1*100))}%) + {t2}({int(round(w2*100))}%)",
            'Final': fvs[k], 'CAGR': cagrs[k], 'MDD': mdds[k], 'Vol': vols[k],
            'Sharpe': shs[k], 'Sortino': sos[k], 'Calmar': cals[k]
        })

df_all = pd.DataFrame(rows)
print(f"Evaluated {len(df_all):,} portfolios in {time.time() - t1_start:.2f}s!")

# 1. Strict Dominance over SMH(60)+SCHD(40): CAGR >= b_cagr AND MDD > b_mdd (shallower)
strict_dom = df_all[(df_all['CAGR'] > b_cagr) & (df_all['MDD'] > b_mdd)].sort_values(by='CAGR', ascending=False)
print(f"\n=== 1. STRICT DOMINANCE (CAGR > {b_cagr:.2%} AND MDD shallower than {b_mdd:.2%}) [{len(strict_dom)} found] ===")
if len(strict_dom) > 0:
    print(strict_dom[['Pair', 'CAGR', 'MDD', 'Sharpe', 'Sortino', 'Calmar', 'Final']].head(25).to_string(index=False))

# 2. Higher Sharpe AND Higher CAGR than Baseline
better_cagr_sharpe = df_all[(df_all['CAGR'] > b_cagr) & (df_all['Sharpe'] > b_sh)].sort_values(by='Sharpe', ascending=False)
print(f"\n=== 2. HIGHER CAGR (> {b_cagr:.2%}) AND HIGHER SHARPE (> {b_sh:.3f}) [{len(better_cagr_sharpe)} found] ===")
if len(better_cagr_sharpe) > 0:
    print(better_cagr_sharpe[['Pair', 'CAGR', 'MDD', 'Sharpe', 'Sortino', 'Calmar', 'Final']].head(25).to_string(index=False))

# 3. Top Sharpe Ratio with CAGR >= 22.0% (Still crushing QQQ's 19.79% by +2.2%p+)
top_sharpe_22 = df_all[df_all['CAGR'] >= 0.22].sort_values(by='Sharpe', ascending=False)
print(f"\n=== 3. TOP SHARPE RATIO WITH CAGR >= 22.0% ===")
print(top_sharpe_22[['Pair', 'CAGR', 'MDD', 'Sharpe', 'Sortino', 'Calmar', 'Final']].head(25).to_string(index=False))

# 4. Top Calmar Ratio (CAGR / |MDD|) with CAGR >= 21.0%
top_calmar_21 = df_all[df_all['CAGR'] >= 0.21].sort_values(by='Calmar', ascending=False)
print(f"\n=== 4. TOP CALMAR RATIO (CAGR / |MDD|) WITH CAGR >= 21.0% ===")
print(top_calmar_21[['Pair', 'CAGR', 'MDD', 'Sharpe', 'Sortino', 'Calmar', 'Final']].head(25).to_string(index=False))

# 5. Higher CAGR (> 24.5%) with MDD still better than QQQ (-35.12%)
high_cagr_qqq_mdd = df_all[(df_all['CAGR'] > 0.24) & (df_all['MDD'] > -0.3512)].sort_values(by='CAGR', ascending=False)
print(f"\n=== 5. MAXIMUM CAGR WITH MDD SAFER THAN QQQ (-35.12%) ===")
print(high_cagr_qqq_mdd[['Pair', 'CAGR', 'MDD', 'Sharpe', 'Sortino', 'Calmar', 'Final']].head(25).to_string(index=False))
