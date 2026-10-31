import pandas as pd
import numpy as np
from detailed_metrics import run_simulation

def rolling_analysis(name, sim_res):
    df = sim_res['df_ts'].copy()
    df['Port_1Y'] = df['Port'].pct_change(252)
    df['QQQ_1Y'] = df['QQQ'].pct_change(252)
    
    df['Port_3Y'] = (df['Port'] / df['Port'].shift(252*3)) ** (1/3) - 1
    df['QQQ_3Y'] = (df['QQQ'] / df['QQQ'].shift(252*3)) ** (1/3) - 1
    
    df['Port_5Y'] = (df['Port'] / df['Port'].shift(252*5)) ** (1/5) - 1
    df['QQQ_5Y'] = (df['QQQ'] / df['QQQ'].shift(252*5)) ** (1/5) - 1
    
    df.dropna(inplace=True)
    
    win_1y = (df['Port_1Y'] > df['QQQ_1Y']).mean()
    win_3y = (df['Port_3Y'] > df['QQQ_3Y']).mean()
    win_5y = (df['Port_5Y'] > df['QQQ_5Y']).mean()
    
    print(f'=== ROLLING WIN RATES VS QQQ: {name} ===')
    print(f'Rolling 1-Year Win Rate: {win_1y:.1%} (Port median: {df["Port_1Y"].median():.2%}, QQQ: {df["QQQ_1Y"].median():.2%})')
    print(f'Rolling 3-Year Win Rate: {win_3y:.1%} (Port median: {df["Port_3Y"].median():.2%}, QQQ: {df["QQQ_3Y"].median():.2%})')
    print(f'Rolling 5-Year Win Rate: {win_5y:.1%} (Port median: {df["Port_5Y"].median():.2%}, QQQ: {df["QQQ_5Y"].median():.2%})')
    print(f'Min 5-Year Annualized Return: Port {df["Port_5Y"].min():.2%} vs QQQ {df["QQQ_5Y"].min():.2%}\n')

sim_smh_gld = run_simulation({'SMH': 0.70, 'GLD': 0.30}, start_date='2005-01-01')
rolling_analysis('SMH 70% + GLD 30% (2005~2026)', sim_smh_gld)

sim_smh_schd = run_simulation({'SMH': 0.60, 'SCHD': 0.40}, start_date='2011-10-20')
rolling_analysis('SMH 60% + SCHD 40% (2011~2026)', sim_smh_schd)
