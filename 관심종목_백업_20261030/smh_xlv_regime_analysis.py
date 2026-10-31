import pandas as pd
import numpy as np
from verify_top5_champions import series_dict

smh = series_dict['SMH'].pct_change().dropna()
xlv = series_dict['XLV'].pct_change().dropna()
qqq = series_dict['QQQ'].pct_change().dropna()
schd = series_dict['SCHD'].pct_change().dropna()

common_all = smh.index.intersection(xlv.index).intersection(qqq.index)
smh_c = smh.loc[common_all]
xlv_c = xlv.loc[common_all]
qqq_c = qqq.loc[common_all]

periods = [
    ('2000~2008 (Dot-com Bust & GFC)', '2000-06-05', '2008-12-31'),
    ('2009~2019 (Zero-Rate Cloud/Mobile Era)', '2009-01-01', '2019-12-31'),
    ('2020~2026 (COVID, Rate Hike & AI Era)', '2020-01-01', '2026-10-13'),
    ('Full 26.4 Yrs (2000~2026)', '2000-06-05', '2026-10-13')
]

print("=== CORRELATION & BETA BY MACRO REGIME ===")
for label, s, e in periods:
    r_smh = smh_c.loc[s:e]
    r_xlv = xlv_c.loc[s:e]
    r_qqq = qqq_c.loc[s:e]
    corr_smh_xlv = r_smh.corr(r_xlv)
    corr_smh_qqq = r_smh.corr(r_qqq)
    
    # Down-market correlation (when SMH drops > 1.5% in a day)
    crash_days = r_smh < -0.015
    avg_smh_drop = r_smh[crash_days].mean()
    avg_xlv_on_smh_drop = r_xlv[crash_days].mean()
    avg_qqq_on_smh_drop = r_qqq[crash_days].mean()
    
    print(f"{label:38s} | Corr(SMH,XLV): {corr_smh_xlv:.2f} (vs QQQ {corr_smh_qqq:.2f}) | On SMH >-1.5% Crash Days (avg {avg_smh_drop:.2%}): XLV {avg_xlv_on_smh_drop:.2%} vs QQQ {avg_qqq_on_smh_drop:.2%}")
