import pandas as pd
import numpy as np
from test_advanced_rebalancing_rules import df_dict, simulate_strategy

def test_dynamic_rules(t1, t2, start_str, label):
    print(f"\n================================================================================")
    print(f"PAIR: {t1} + {t2} | HORIZON: {label} (from {start_str})")
    print(f"================================================================================")
    
    # 1. Fixed 60:40
    r_fix60_g = simulate_strategy(t1, t2, 0.60, start_str, reb_month=1, band=0.0, dd_tilt=False, div_tax=0.0, tx_cost=0.0, cg_tax=0.0)
    r_fix60_n = simulate_strategy(t1, t2, 0.60, start_str, reb_month=1, band=0.0, dd_tilt=False, div_tax=0.154, tx_cost=0.0015, cg_tax=0.22)
    
    # 2. Fixed 65:35
    r_fix65_g = simulate_strategy(t1, t2, 0.65, start_str, reb_month=1, band=0.0, dd_tilt=False, div_tax=0.0, tx_cost=0.0, cg_tax=0.0)
    r_fix65_n = simulate_strategy(t1, t2, 0.65, start_str, reb_month=1, band=0.0, dd_tilt=False, div_tax=0.154, tx_cost=0.0015, cg_tax=0.22)
    
    # 3. Dynamic Contrarian Drawdown-Tilt (Base 60:40 -> 75:25 when SMH 1Y DD <= -20%)
    r_tilt60_g = simulate_strategy(t1, t2, 0.60, start_str, reb_month=1, band=0.0, dd_tilt=True, div_tax=0.0, tx_cost=0.0, cg_tax=0.0)
    r_tilt60_n = simulate_strategy(t1, t2, 0.60, start_str, reb_month=1, band=0.0, dd_tilt=True, div_tax=0.154, tx_cost=0.0015, cg_tax=0.22)

    # 4. Dynamic Contrarian Drawdown-Tilt (Base 65:35 -> 80:20 when SMH 1Y DD <= -20%)
    r_tilt65_g = simulate_strategy(t1, t2, 0.65, start_str, reb_month=1, band=0.0, dd_tilt=True, div_tax=0.0, tx_cost=0.0, cg_tax=0.0)
    r_tilt65_n = simulate_strategy(t1, t2, 0.65, start_str, reb_month=1, band=0.0, dd_tilt=True, div_tax=0.154, tx_cost=0.0015, cg_tax=0.22)

    rows = [
        ('Fixed 60:40 (Standard Jan)', r_fix60_g, r_fix60_n),
        ('Fixed 65:35 (Standard Jan)', r_fix65_g, r_fix65_n),
        ('Dynamic Tilt (60:40 -> 75:25 in Crash)', r_tilt60_g, r_tilt60_n),
        ('Dynamic Tilt (65:35 -> 80:20 in Crash)', r_tilt65_g, r_tilt65_n),
    ]
    for name, rg, rn in rows:
        print(f"{name:40s} | Gross CAGR: {rg['cagr_ongoing']:.2%} (MDD {rg['mdd']:.2%}, Sh {rg['sharpe']:.3f}, Cal {rg['calmar']:.3f}, ${rg['final_ongoing']:,.0f}) | Full-Tax Net: {rn['cagr_ongoing']:.2%} (Liq {rn['cagr_liq']:.2%}, MDD {rn['mdd']:.2%}, ${rn['final_liq']:,.0f})")

test_dynamic_rules('SMH', 'XLV', '2011-10-20', '2011~2026 (15.0 Yrs)')
test_dynamic_rules('SMH', 'XLV', '2005-01-03', '2005~2026 (21.8 Yrs, Includes 2008 GFC)')
test_dynamic_rules('SMH', 'XLV', '2000-06-05', '2000~2026 (26.4 Yrs, Includes Dot-Com & GFC)')

test_dynamic_rules('SMH', 'IAU', '2011-10-20', '2011~2026 (15.0 Yrs)')
test_dynamic_rules('SMH', 'IAU', '2005-01-28', '2005~2026 (21.7 Yrs, Includes 2008 GFC)')

test_dynamic_rules('SMH', 'PPA', '2011-10-20', '2011~2026 (15.0 Yrs)')
test_dynamic_rules('SMH', 'UUP', '2011-10-20', '2011~2026 (15.0 Yrs)')
test_dynamic_rules('SMH', 'BRK-B', '2011-10-20', '2011~2026 (15.0 Yrs)')
