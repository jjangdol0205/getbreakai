"""
Analyze how frequently PW-RSI (Condition 1 + 2 + 3 + 4 + Value Trap Exclusion) signals appear:
1) Year-by-year count of weeks with active signals & distinct stocks triggered (2000~2026)
2) Recent 2024~2026 actual stocks that triggered [BUY: 우측 시동 켜짐!] with exact dates & subsequent returns
3) Today's (2026-10-15) KRX closing price check for SK Square (402340.KS) & SK Hynix (000660.KS)
"""

import sys
from datetime import datetime
import urllib3
import requests
import numpy as np
import pandas as pd

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

from backtest_pw_rsi_2000_2026 import (
    load_aligned_panel,
    KR_NAMES,
    ALWAYS_TRAP_TICKERS,
    POST_2021_TRAPS,
    POST_2023_TRAPS,
)


def main():
    # 0. Check today's (2026-10-15) KRX close for SK Square & SK Hynix
    headers = {"User-Agent": "Mozilla/5.0"}
    print("=== [참고] 오늘(2026-10-15) 한국장 마감 종가 확인 ===")
    for tkr, name in [("402340.KS", "SK스퀘어"), ("000660.KS", "SK하이닉스")]:
        try:
            url = f"https://query1.finance.yahoo.com/v8/finance/chart/{tkr}?range=5d&interval=1d"
            r = requests.get(url, headers=headers, verify=False, timeout=6).json()["chart"]["result"][0]
            ts = r["timestamp"]
            c = r["indicators"]["quote"][0]["close"]
            lo = r["indicators"]["quote"][0]["low"]
            hi = r["indicators"]["quote"][0]["high"]
            dt = datetime.fromtimestamp(ts[-1]).strftime("%Y-%m-%d")
            prev_c = c[-2] if len(c) >= 2 else c[-1]
            chg = (c[-1] / prev_c - 1.0) * 100.0
            tail_up = (c[-1] / lo[-1] - 1.0) * 100.0
            print(f" * {name}({tkr}) [{dt} 마감]: 종가 {c[-1]:,.0f}원 (전일대비 {chg:+.2f}% | 장중저가 {lo[-1]:,.0f}원 대비 +{tail_up:.2f}% 아랫꼬리 반등 | 장중고가 {hi[-1]:,.0f}원)")
        except Exception as e:
            print("Error:", e)

    # 1. Load panel and analyze signal frequency across 2000~2026
    cal, C, H, L, V, _ = load_aligned_panel()
    tickers = list(C.columns)
    is_kr_arr = np.array([t.endswith(".KS") or t.endswith(".KQ") for t in tickers], dtype=bool)

    Low52 = L.rolling(252, min_periods=180).min()
    High52 = H.rolling(252, min_periods=180).max()
    ProxLow52 = (C / Low52 - 1.0) * 100.0
    DDHigh52 = (C / High52 - 1.0) * 100.0

    MA20 = C.rolling(20).mean()
    MA60 = C.rolling(60).mean()
    MA20_Slope = MA20 / MA20.shift(5) - 1.0

    VolMA20 = V.rolling(20).mean() + 1.0
    VolRatio = V / VolMA20
    MaxVol10D = VolRatio.rolling(10).max()
    Ret20D = (C / C.shift(20) - 1.0) * 100.0
    Fwd60D = (C.shift(-60) / C - 1.0) * 100.0
    MaxFwd120D = (H.rolling(120, min_periods=1).max().shift(-120) / C - 1.0) * 100.0

    start_idx = int(np.searchsorted(cal, pd.to_datetime("2000-01-03")))
    sim_dates = cal[start_idx:]
    n_days = len(sim_dates)

    c_arr = C.iloc[start_idx:].values
    prox_arr = ProxLow52.iloc[start_idx:].values
    dd_arr = DDHigh52.iloc[start_idx:].values
    ma20_arr = MA20.iloc[start_idx:].values
    ma60_arr = MA60.iloc[start_idx:].values
    ma20_sl_arr = MA20_Slope.iloc[start_idx:].values
    vol10_arr = MaxVol10D.iloc[start_idx:].values
    ret20_arr = Ret20D.iloc[start_idx:].values
    max120_arr = MaxFwd120D.iloc[start_idx:].values

    qual_mask = np.ones_like(c_arr, dtype=bool)
    for j, t in enumerate(tickers):
        if t in ALWAYS_TRAP_TICKERS:
            qual_mask[:, j] = False
        elif t in POST_2021_TRAPS:
            for i in range(n_days):
                if sim_dates[i].year >= 2021:
                    qual_mask[i, j] = False
        elif t in POST_2023_TRAPS:
            for i in range(n_days):
                if sim_dates[i].year >= 2023:
                    qual_mask[i, j] = False

    # Cond 1 + 2 + 3 + 4 matrix
    sig_matrix = (
        qual_mask
        & (dd_arr <= -38.0)
        & (prox_arr >= 10.0) & (prox_arr <= 40.0)
        & (c_arr > ma20_arr) & (c_arr > ma60_arr) & (ma20_sl_arr > 0)
        & ((vol10_arr >= 1.35) | (ret20_arr >= 8.0))
    )

    us_sig_matrix = sig_matrix[:, ~is_kr_arr]
    us_tickers = [t for t, kr in zip(tickers, is_kr_arr) if not kr]

    # Sample weekly (every 5 trading days)
    weekly_indices = list(range(0, n_days, 5))
    yr_stats = []
    for y in range(2000, 2027):
        w_idx = [i for i in weekly_indices if sim_dates[i].year == y]
        weeks_total = len(w_idx)
        weeks_with_any = sum(1 for i in w_idx if sig_matrix[i].any())
        weeks_with_us = sum(1 for i in w_idx if us_sig_matrix[i].any())

        # Distinct stocks that triggered at least once during year y
        d_idx = np.where(sim_dates.year == y)[0]
        distinct_all = int(sig_matrix[d_idx].any(axis=0).sum())
        distinct_us = int(us_sig_matrix[d_idx].any(axis=0).sum())
        names_us = [KR_NAMES.get(us_tickers[k], us_tickers[k]) for k in np.where(us_sig_matrix[d_idx].any(axis=0))[0]]

        yr_stats.append({
            "Year": y,
            "Total_Weeks": weeks_total,
            "Weeks_With_Signal_All": weeks_with_any,
            "Weeks_With_Signal_US": weeks_with_us,
            "Distinct_Stocks_All": distinct_all,
            "Distinct_Stocks_US": distinct_us,
            "Sample_US_Stocks_Triggered": ", ".join(names_us[:6]),
        })

    df_yr = pd.DataFrame(yr_stats)
    print("\n=== 2000~2026년 연도별 'PW-RSI 우측 시동(조건 ①+②+③+④)' 출현 빈도 통계 ===")
    print(df_yr.to_string(index=False))
    print(f"\n * 27년 평균 연간 포착 종목 수 (한·미 전체): 연평균 {df_yr['Distinct_Stocks_All'].mean():.1f}개 종목 (미국 주식만: 연평균 {df_yr['Distinct_Stocks_US'].mean():.1f}개 종목)")
    print(f" * 연간 52주 중 매수 신호가 떠 있는 주간 비율: 한·미 전체 평균 {(df_yr['Weeks_With_Signal_All']/df_yr['Total_Weeks']).mean()*100:.1f}% (미국 주식만: {(df_yr['Weeks_With_Signal_US']/df_yr['Total_Weeks']).mean()*100:.1f}%)")

    # Show recent 2023~2026 first-ignition events in US stocks
    print("\n=== 최근 2023~2026년 실제 포착된 주요 '우측 시동(조건 ①~④ 완비)' 점등 사례 ===")
    recent_events = []
    last_trig = {}
    for i in range(n_days):
        dt = sim_dates[i]
        if dt.year < 2023:
            continue
        for j, t in enumerate(tickers):
            if sig_matrix[i, j]:
                if t not in last_trig or (i - last_trig[t]) >= 30:
                    last_trig[t] = i
                    recent_events.append({
                        "Date": dt.strftime("%Y-%m-%d"),
                        "Ticker": KR_NAMES.get(t, t),
                        "Market": "KR" if is_kr_arr[j] else "US",
                        "Close": round(float(c_arr[i, j]), 2),
                        "DD_52W_High_Pct": round(float(dd_arr[i, j]), 1),
                        "Off_52W_Low_Pct": round(float(prox_arr[i, j]), 1),
                        "Vol_Surge_10D": round(float(vol10_arr[i, j]), 2),
                        "Max_120D_Gain_After_Signal_Pct": round(float(max120_arr[i, j]), 1) if not np.isnan(max120_arr[i, j]) else None,
                    })
    ev_df = pd.DataFrame(recent_events)
    print(f"2023~2026년 총 {len(ev_df)}건의 독립적인 '우측 시동 첫 점등' 발생 (연평균 {len(ev_df)/3.8:.1f}건, 한 달 평균 {len(ev_df)/45.5:.1f}건!):")
    print(ev_df.tail(35).to_string(index=False))


if __name__ == "__main__":
    main()
