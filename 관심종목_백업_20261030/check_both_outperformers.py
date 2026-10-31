import pandas as pd
import numpy as np
from pair_engine import data, qqq, backtest_pair

# Individual outperformers vs QQQ
outperformers = ['SMH', 'SOXX', 'PSI', 'VGT', 'XLK', 'IYW', 'XSD', 'QTEC']

print('Testing combinations where BOTH ETFs individually outperform QQQ...')

for i in range(len(outperformers)):
    for j in range(i+1, len(outperformers)):
        t1 = outperformers[i]
        t2 = outperformers[j]
        s1 = data[t1]
        s2 = data[t2]
        
        # Test full common history
        for w1 in [0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8]:
            w2 = round(1 - w1, 2)
            # Full history
            res_full = backtest_pair(s1, s2, w1, w2)
            # Since 2011
            res_2011 = backtest_pair(s1, s2, w1, w2, start_year=2011)
            
            if res_full and res_full['diff_cagr'] > 0 and res_full['diff_mdd'] > 0:
                print(f'[FULL] {t1}({w1}) + {t2}({w2}) from {res_full["start_date"]}: CAGR {res_full["cagr_port"]:.2%} vs QQQ {res_full["cagr_qqq"]:.2%}, MDD {res_full["mdd_port"]:.2%} vs QQQ {res_full["mdd_qqq"]:.2%}')
            if res_2011 and res_2011['diff_cagr'] > 0 and res_2011['diff_mdd'] > 0:
                print(f'[2011] {t1}({w1}) + {t2}({w2}): CAGR {res_2011["cagr_port"]:.2%} vs QQQ {res_2011["cagr_qqq"]:.2%}, MDD {res_2011["mdd_port"]:.2%} vs QQQ {res_2011["mdd_qqq"]:.2%}')

