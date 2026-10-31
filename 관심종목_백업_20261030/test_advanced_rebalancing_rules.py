import os
import pandas as pd
import numpy as np

data_dir = 'data'
files = [f for f in os.listdir(data_dir) if f.endswith('.csv')]
df_dict = {}
for f in sorted(files):
    ticker = f.replace('.csv', '')
    df = pd.read_csv(os.path.join(data_dir, f))
    df['Date'] = pd.to_datetime(df['Date'])
    df.set_index('Date', inplace=True)
    df_dict[ticker] = df[['Close', 'AdjClose']].sort_index()

def simulate_strategy(t1, t2, w1_base=0.60, start_date_str='2011-10-20',
                      reb_month=1, band=0.0, dd_tilt=False,
                      div_tax=0.154, tx_cost=0.0015, cg_tax=0.22):
    start_dt = pd.to_datetime(start_date_str)
    d1 = df_dict[t1]
    d2 = df_dict[t2]
    dq = df_dict['QQQ']
    common = d1.index.intersection(d2.index).intersection(dq.index)
    common = common[common >= start_dt]
    
    n = len(common)
    dates = common
    months = common.month.values
    years = common.year.values
    total_years = (common[-1] - common[0]).days / 365.25
    
    c1 = d1.loc[common, 'Close'].values.astype(np.float64)
    a1 = d1.loc[common, 'AdjClose'].values.astype(np.float64)
    c2 = d2.loc[common, 'Close'].values.astype(np.float64)
    a2 = d2.loc[common, 'AdjClose'].values.astype(np.float64)
    
    pr1 = np.zeros(n); pr2 = np.zeros(n)
    div1 = np.zeros(n); div2 = np.zeros(n)
    pr1[1:] = c1[1:] / c1[:-1] - 1.0
    pr2[1:] = c2[1:] / c2[:-1] - 1.0
    tr1 = a1[1:] / a1[:-1] - 1.0
    tr2 = a2[1:] / a2[:-1] - 1.0
    div1[1:] = np.maximum(0.0, tr1 - pr1[1:])
    div2[1:] = np.maximum(0.0, tr2 - pr2[1:])
    
    init_cap = 10000.0
    val1 = init_cap * w1_base * (1.0 - tx_cost)
    val2 = init_cap * (1.0 - w1_base) * (1.0 - tx_cost)
    basis1 = val1
    basis2 = val2
    
    port_val = np.zeros(n, dtype=np.float64)
    port_val[0] = val1 + val2
    
    reb_count = 0
    
    for i in range(1, n):
        # Daily return + after-tax dividend reinvestment
        net_div1 = val1 * div1[i] * (1.0 - div_tax)
        val1 = val1 * (1.0 + pr1[i]) + net_div1
        basis1 += net_div1
        
        net_div2 = val2 * div2[i] * (1.0 - div_tax)
        val2 = val2 * (1.0 + pr2[i]) + net_div2
        basis2 += net_div2
        
        # Check if first trading day of target rebalance month
        is_reb_day = (months[i] == reb_month and months[i-1] != reb_month)
        # Avoid rebalancing within first 60 days of start
        if is_reb_day and i > 60:
            tot = val1 + val2
            cur_w1 = val1 / tot
            
            # Determine target weight w1_target
            w1_target = w1_base
            if dd_tilt:
                # Check 1-year drawdown of asset 1 (SMH)
                lookback = max(0, i - 252)
                peak_a1 = np.max(a1[lookback:i+1])
                dd_a1 = (a1[i] - peak_a1) / peak_a1
                if dd_a1 <= -0.20:
                    w1_target = min(0.80, w1_base + 0.15) # Contrarian buy more SMH in deep drawdown
                elif dd_a1 > -0.05 and cur_w1 > w1_base + 0.05:
                    w1_target = w1_base # Harvest profit back to base weight
            
            # Check tolerance band
            if abs(cur_w1 - w1_target) >= band:
                reb_count += 1
                target1 = tot * w1_target
                diff1 = val1 - target1
                if diff1 > 0:
                    sell_amt = diff1
                    sell_frac = sell_amt / val1
                    cost_sold = basis1 * sell_frac
                    gain = sell_amt - cost_sold
                    tax = max(0.0, gain * cg_tax)
                    cost = sell_amt * tx_cost * 2.0
                    val1 -= sell_amt
                    basis1 -= cost_sold
                    net_buy2 = sell_amt - tax - cost
                    val2 += net_buy2
                    basis2 += net_buy2
                elif diff1 < 0:
                    sell_amt = -diff1
                    sell_frac = sell_amt / val2
                    cost_sold = basis2 * sell_frac
                    gain = sell_amt - cost_sold
                    tax = max(0.0, gain * cg_tax)
                    cost = sell_amt * tx_cost * 2.0
                    val2 -= sell_amt
                    basis2 -= cost_sold
                    net_buy1 = sell_amt - tax - cost
                    val1 += net_buy1
                    basis1 += net_buy1
                    
        port_val[i] = val1 + val2
        
    final_ongoing = port_val[-1]
    cagr_ongoing = (final_ongoing / init_cap) ** (1.0 / total_years) - 1.0
    
    # Final liquidation tax
    ug1 = max(0.0, val1 - basis1)
    ug2 = max(0.0, val2 - basis2)
    final_liq = final_ongoing - (ug1 + ug2) * cg_tax
    cagr_liq = (final_liq / init_cap) ** (1.0 / total_years) - 1.0
    
    peak = np.maximum.accumulate(port_val)
    mdd = ((port_val - peak) / peak).min()
    dret = np.diff(port_val) / port_val[:-1]
    vol = np.std(dret) * np.sqrt(252)
    sharpe = (cagr_ongoing - 0.02) / vol
    calmar = cagr_ongoing / abs(mdd)
    
    return {
        'cagr_ongoing': cagr_ongoing,
        'cagr_liq': cagr_liq,
        'mdd': mdd,
        'sharpe': sharpe,
        'calmar': calmar,
        'final_ongoing': final_ongoing,
        'final_liq': final_liq,
        'reb_count': reb_count
    }

print("=== 1. TESTING REBALANCING MONTH SEASONALITY ON SMH(60%) + XLV(40%) (2011~2026) ===")
for m in range(1, 13):
    r_gross = simulate_strategy('SMH', 'XLV', 0.60, reb_month=m, div_tax=0.0, tx_cost=0.0, cg_tax=0.0)
    r_net = simulate_strategy('SMH', 'XLV', 0.60, reb_month=m, div_tax=0.154, tx_cost=0.0015, cg_tax=0.22)
    print(f"Month {m:2d} Rebalance | Gross CAGR: {r_gross['cagr_ongoing']:.2%} (MDD {r_gross['mdd']:.2%}, Sharpe {r_gross['sharpe']:.3f}) | Full-Tax Net CAGR: {r_net['cagr_ongoing']:.2%} (Liq {r_net['cagr_liq']:.2%}, MDD {r_net['mdd']:.2%})")

print("\n=== 2. TESTING ADVANCED ANNUAL RULES ON SMH + XLV (2011~2026) ===")
configs = [
    ('Standard: Jan Rebalance (60:40)', 0.60, 1, 0.0, False),
    ('Upgrade A: Oct Rebalance [Autumn Low] (60:40)', 0.60, 10, 0.0, False),
    ('Upgrade B: Nov Rebalance [Halloween] (60:40)', 0.60, 11, 0.0, False),
    ('Upgrade C: Jan Rebalance + 5% Band [Tax Saver] (60:40)', 0.60, 1, 0.05, False),
    ('Upgrade D: Oct Rebalance + 5% Band (60:40)', 0.60, 10, 0.05, False),
    ('Upgrade E: Jan Contrarian Drawdown-Tilt (60->75% in Crash)', 0.60, 1, 0.0, True),
    ('Upgrade F: Oct Contrarian Drawdown-Tilt (60->75% in Crash)', 0.60, 10, 0.0, True),
    ('Upgrade G: Oct + 5% Band + Drawdown-Tilt (65:35 base)', 0.65, 10, 0.05, True),
]

for label, w, m, b, tilt in configs:
    rg = simulate_strategy('SMH', 'XLV', w, reb_month=m, band=b, dd_tilt=tilt, div_tax=0.0, tx_cost=0.0, cg_tax=0.0)
    rn = simulate_strategy('SMH', 'XLV', w, reb_month=m, band=b, dd_tilt=tilt, div_tax=0.154, tx_cost=0.0015, cg_tax=0.22)
    print(f"{label:58s} | Gross: {rg['cagr_ongoing']:.2%} (MDD {rg['mdd']:.2%}, Sh {rg['sharpe']:.3f}) | Net(22%세금): {rn['cagr_ongoing']:.2%} (청산 {rn['cagr_liq']:.2%}, MDD {rn['mdd']:.2%}, Reb {rn['reb_count']}회, ${rn['final_liq']:,.0f})")
