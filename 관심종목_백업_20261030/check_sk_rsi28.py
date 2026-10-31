import sys
import pandas as pd
import numpy as np

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

for tkr, name in [("402340_KS", "SK스퀘어"), ("000660_KS", "SK하이닉스")]:
    df = pd.read_csv(f"data_stocks/{tkr}.csv").dropna(subset=["Close"]).reset_index(drop=True)
    c = df["Close"].astype(float)
    delta = c.diff()
    up = delta.clip(lower=0).ewm(com=13, adjust=True, min_periods=14).mean()
    dn = (-delta.clip(upper=0)).ewm(com=13, adjust=True, min_periods=14).mean()
    df["RSI14"] = 100.0 - 100.0 / (1.0 + up / (dn + 1e-9))
    df["Fwd_5D"] = (c.shift(-5) / c - 1.0) * 100.0
    df["Fwd_20D"] = (c.shift(-20) / c - 1.0) * 100.0
    df["Fwd_40D"] = (c.shift(-40) / c - 1.0) * 100.0
    df["Fwd_60D"] = (c.shift(-60) / c - 1.0) * 100.0

    # If today drops -5% on SK Square (852,000 -> 809,000), what is RSI14?
    if tkr == "402340_KS":
        for drop in [-4.0, -5.0, -6.0]:
            c_sim = pd.concat([c, pd.Series([c.iloc[-1] * (1.0 + drop / 100.0)])], ignore_index=True)
            d_sim = c_sim.diff()
            u_sim = d_sim.clip(lower=0).ewm(com=13, adjust=True, min_periods=14).mean()
            n_sim = (-d_sim.clip(upper=0)).ewm(com=13, adjust=True, min_periods=14).mean()
            rsi_sim = float((100.0 - 100.0 / (1.0 + u_sim / (n_sim + 1e-9))).iloc[-1])
            print(f"[시뮬레이션] 오늘 SK스퀘어 {drop:+.1f}% ({c_sim.iloc[-1]:,.0f}원) 시 예상 RSI(14) = {rsi_sim:.1f}")

    sub = df[df["RSI14"] <= 29.5].dropna(subset=["Fwd_20D", "Fwd_60D"])
    print(f"\n=== {name} 역사상 RSI(14) <= 29.5 극과매도 투매 발생 시 향후 수익률 (총 {len(sub)}회) ===")
    if len(sub) > 0:
        print(f" * 5거래일(1주) 뒤 평균: {sub['Fwd_5D'].mean():+.2f}% (승률 {(sub['Fwd_5D']>0).mean()*100:.1f}%)")
        print(f" * 20거래일(1달) 뒤 평균: {sub['Fwd_20D'].mean():+.2f}% (승률 {(sub['Fwd_20D']>0).mean()*100:.1f}%)")
        print(f" * 40거래일(2달) 뒤 평균: {sub['Fwd_40D'].mean():+.2f}% (승률 {(sub['Fwd_40D']>0).mean()*100:.1f}%)")
        print(f" * 60거래일(3달) 뒤 평균: {sub['Fwd_60D'].mean():+.2f}% (승률 {(sub['Fwd_60D']>0).mean()*100:.1f}%)")
        print(sub[["Date", "Close", "RSI14", "Fwd_5D", "Fwd_20D", "Fwd_40D", "Fwd_60D"]].tail(10).to_string(index=False))
