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

def simulate_realistic(t1, t2, w1, start_date_str='2011-10-20',
                       div_tax_rate=0.15, tx_cost_rate=0.0015, cap_gains_tax_rate=0.22,
                       deduct_final_liquidation_tax=False):
    start_dt = pd.to_datetime(start_date_str)
    d1 = df_dict[t1]
    d2 = df_dict[t2]
    dq = df_dict['QQQ']
    common = d1.index.intersection(d2.index).intersection(dq.index)
    common = common[common >= start_dt]
    
    n = len(common)
    years = common.year.values
    total_years = (common[-1] - common[0]).days / 365.25
    
    # Extract Close (price return) and AdjClose (total return)
    c1 = d1.loc[common, 'Close'].values.astype(np.float64)
    a1 = d1.loc[common, 'AdjClose'].values.astype(np.float64)
    c2 = d2.loc[common, 'Close'].values.astype(np.float64)
    a2 = d2.loc[common, 'AdjClose'].values.astype(np.float64)
    
    # Daily price return and dividend yield
    pr1 = np.zeros(n)
    pr2 = np.zeros(n)
    div1 = np.zeros(n)
    div2 = np.zeros(n)
    
    pr1[1:] = c1[1:] / c1[:-1] - 1.0
    pr2[1:] = c2[1:] / c2[:-1] - 1.0
    
    tr1 = a1[1:] / a1[:-1] - 1.0
    tr2 = a2[1:] / a2[:-1] - 1.0
    
    # Dividend yield on day t (as fraction of previous close)
    div1[1:] = np.maximum(0.0, tr1 - pr1[1:])
    div2[1:] = np.maximum(0.0, tr2 - pr2[1:])
    
    # Track holdings by value and cost basis
    w2 = 1.0 - w1
    init_cap = 10000.0
    # Deduct initial purchase transaction cost
    val1 = init_cap * w1 * (1.0 - tx_cost_rate)
    val2 = init_cap * w2 * (1.0 - tx_cost_rate)
    basis1 = val1
    basis2 = val2
    
    port_val = np.zeros(n, dtype=np.float64)
    port_val[0] = val1 + val2
    
    total_div_tax_paid = 0.0
    total_cg_tax_paid = 0.0
    total_tx_cost_paid = init_cap * tx_cost_rate
    
    for i in range(1, n):
        # 1. Apply daily price return & after-tax dividend reinvestment
        net_div1 = val1 * div1[i] * (1.0 - div_tax_rate)
        div_tax1 = val1 * div1[i] * div_tax_rate
        val1 = val1 * (1.0 + pr1[i]) + net_div1
        basis1 += net_div1 # Reinvested dividend increases cost basis
        
        net_div2 = val2 * div2[i] * (1.0 - div_tax_rate)
        div_tax2 = val2 * div2[i] * div_tax_rate
        val2 = val2 * (1.0 + pr2[i]) + net_div2
        basis2 += net_div2
        
        total_div_tax_paid += (div_tax1 + div_tax2)
        
        # 2. Check if annual rebalance day (and w1 < 1.0)
        if years[i] != years[i-1] and 0.0 < w1 < 1.0:
            tot = val1 + val2
            target1 = tot * w1
            diff1 = val1 - target1 # If > 0, sell asset 1 and buy asset 2
            
            if abs(diff1) > 1e-6:
                if diff1 > 0:
                    # Selling fraction of asset 1
                    sell_amt = diff1
                    sell_frac = sell_amt / val1
                    cost_sold = basis1 * sell_frac
                    realized_gain = sell_amt - cost_sold
                    
                    cg_tax = max(0.0, realized_gain * cap_gains_tax_rate)
                    tx_cost = sell_amt * tx_cost_rate * 2.0 # sell 1 + buy 2
                    
                    val1 -= sell_amt
                    basis1 -= cost_sold
                    
                    net_buy2 = sell_amt - cg_tax - tx_cost
                    val2 += net_buy2
                    basis2 += net_buy2
                    
                    total_cg_tax_paid += cg_tax
                    total_tx_cost_paid += tx_cost
                else:
                    # Selling fraction of asset 2
                    sell_amt = -diff1
                    sell_frac = sell_amt / val2
                    cost_sold = basis2 * sell_frac
                    realized_gain = sell_amt - cost_sold
                    
                    cg_tax = max(0.0, realized_gain * cap_gains_tax_rate)
                    tx_cost = sell_amt * tx_cost_rate * 2.0 # sell 2 + buy 1
                    
                    val2 -= sell_amt
                    basis2 -= cost_sold
                    
                    net_buy1 = sell_amt - cg_tax - tx_cost
                    val1 += net_buy1
                    basis1 += net_buy1
                    
                    total_cg_tax_paid += cg_tax
                    total_tx_cost_paid += tx_cost
                    
        port_val[i] = val1 + val2
        
    final_pre_liq = port_val[-1]
    cagr_pre_liq = (final_pre_liq / init_cap) ** (1.0 / total_years) - 1.0
    
    # Final liquidation tax (if investor sells everything at the end of year 15)
    unrealized_gain1 = max(0.0, val1 - basis1)
    unrealized_gain2 = max(0.0, val2 - basis2)
    final_liq_tax = (unrealized_gain1 + unrealized_gain2) * cap_gains_tax_rate
    final_after_liq = final_pre_liq - final_liq_tax
    cagr_after_liq = (final_after_liq / init_cap) ** (1.0 / total_years) - 1.0
    
    peak = np.maximum.accumulate(port_val)
    mdd = ((port_val - peak) / peak).min()
    dret = np.diff(port_val) / port_val[:-1]
    vol = np.std(dret) * np.sqrt(252)
    sharpe = (cagr_pre_liq - 0.02) / vol
    
    return {
        'cagr_gross_or_ongoing': cagr_pre_liq,
        'final_ongoing': final_pre_liq,
        'cagr_liquidated': cagr_after_liq,
        'final_liquidated': final_after_liq,
        'mdd': mdd,
        'sharpe': sharpe,
        'div_tax': total_div_tax_paid,
        'cg_tax': total_cg_tax_paid,
        'tx_cost': total_tx_cost_paid
    }

strategies = [
    ('Benchmark: QQQ (100%)', 'QQQ', 'QQQ', 1.00),
    ('Baseline:  SMH(60%) + SCHD(40%)', 'SMH', 'SCHD', 0.60),
    ('Champ 1A:  SMH(60%) + XLV(40%)', 'SMH', 'XLV', 0.60),
    ('Champ 1B:  SMH(65%) + XLV(35%)', 'SMH', 'XLV', 0.65),
    ('Champ 2A:  SMH(80%) + UUP(20%)', 'SMH', 'UUP', 0.80),
    ('Champ 2B:  SMH(75%) + UUP(25%)', 'SMH', 'UUP', 0.75),
    ('Champ 3:   SMH(80%) + BTAL(20%)', 'SMH', 'BTAL', 0.80),
    ('Champ 4:   SMH(70%) + PPA(30%)', 'SMH', 'PPA', 0.70),
    ('Champ 5:   SMH(60%) + BRK-B(40%)', 'SMH', 'BRK-B', 0.60),
]

rows = []
for name, t1, t2, w1 in strategies:
    # 0. Gross (ETF Expense Ratio already included in prices, 0 tax/slippage)
    r0 = simulate_realistic(t1, t2, w1, div_tax_rate=0.0, tx_cost_rate=0.0, cap_gains_tax_rate=0.0)
    # 1. Div Tax (15.4%) + Tx Cost/Slippage (0.15% one-way) [Tax-deferred / under deduction threshold]
    r1 = simulate_realistic(t1, t2, w1, div_tax_rate=0.154, tx_cost_rate=0.0015, cap_gains_tax_rate=0.0)
    # 2. Full Tax: Div Tax (15.4%) + Tx Cost (0.15%) + Annual Rebalance Cap Gains Tax (22%)
    r2 = simulate_realistic(t1, t2, w1, div_tax_rate=0.154, tx_cost_rate=0.0015, cap_gains_tax_rate=0.22)
    
    rows.append({
        'Strategy': name,
        'Gross_CAGR': f"{r0['cagr_gross_or_ongoing']:.2%}",
        'Net1_CAGR(배당세+수수료)': f"{r1['cagr_gross_or_ongoing']:.2%}",
        'Net2_CAGR(+양도세22%차감)': f"{r2['cagr_gross_or_ongoing']:.2%}",
        'Liq_CAGR(최종청산세후)': f"{r2['cagr_liquidated']:.2%}",
        'Net2_MDD': f"{r2['mdd']:.2%}",
        'Net2_Final': f"${r2['final_ongoing']:,.0f}",
        'Liq_Final': f"${r2['final_liquidated']:,.0f}"
    })

print("=== AFTER-TAX & TRANSACTION COST COMPARISON (2011-10-20 ~ 2026-10-13, 15.0 Yrs) ===")
print(pd.DataFrame(rows).to_string(index=False))
