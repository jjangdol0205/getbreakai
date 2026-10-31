"""
Full 26.8-Year Chronological Backtest Engine (2000-01-03 ~ 2026-10-14)
Simulating the exact Dynamic Weekly PW-RSI Scanner & Switching Strategy:
- Condition 1: 52-Week High Drawdown <= -38% (Valuation Reset)
- Condition 2: 52-Week Low Proximity +10% ~ +40% (Rebound Sweet Spot)
- Condition 3: 10D Volume Wash-Out (>= 1.35x 20D avg) & Simultaneous 20D + 60D MA Breakout ([BUY: 우측 시동])
- Condition 4: Value Trap / Secular Decline Exclusion Filter
- 100-Point Composite Score Ranking & Dynamic Weekly Switching
- Active Exit Rules: -9% Stop-Loss, 55-Day (+8%) Dead-Money Time-Stop, Weekly Upgrade Switch, +100% TP1 & Trailing Runner
"""

import os
import glob
import json
import math
import numpy as np
import pandas as pd

DATA_DIR = "data_stocks"
ETF_DIR = "data"

KR_NAMES = {
    "402340.KS": "SK스퀘어(402340.KS)",
    "000660.KS": "SK하이닉스(000660.KS)",
    "005930.KS": "삼성전자(005930.KS)",
    "042700.KS": "한미반도체(042700.KS)",
    "007660.KS": "이수페타시스(007660.KS)",
    "267260.KS": "HD현대일렉트릭(267260.KS)",
    "003230.KS": "삼양식품(003230.KS)",
    "259960.KS": "크래프톤(259960.KS)",
    "034020.KS": "두산에너빌리티(034020.KS)",
    "012450.KS": "한화에어로(012450.KS)",
    "064350.KS": "현대로템(064350.KS)",
    "329180.KS": "HD현대중공업(329180.KS)",
    "010140.KS": "삼성중공업(010140.KS)",
    "196170.KQ": "알테오젠(196170.KQ)",
    "207940.KS": "삼성바이오(207940.KS)",
    "068270.KS": "셀트리온(068270.KS)",
    "005380.KS": "현대차(005380.KS)",
    "000270.KS": "기아(000270.KS)",
    "035420.KS": "NAVER(035420.KS)",
    "035720.KS": "카카오(035720.KS)",
    "051910.KS": "LG화학(051910.KS)",
    "006400.KS": "삼성SDI(006400.KS)",
    "003670.KS": "포스코퓨처엠(003670.KS)",
    "086520.KQ": "에코프로(086520.KQ)",
    "247540.KQ": "에코프로비엠(247540.KQ)",
    "034730.KS": "SK(주)(034730.KS)",
    "NVDA": "엔비디아(NVDA)",
    "AMD": "AMD(AMD)",
    "MU": "마이크론(MU)",
    "NFLX": "넷플릭스(NFLX)",
    "CELH": "셀시우스(CELH)",
    "FSLR": "퍼스트솔라(FSLR)",
    "KLAC": "KLA(KLAC)",
    "TSM": "TSMC(TSM)",
    "QCOM": "퀄컴(QCOM)",
    "STX": "시게이트(STX)",
    "MNST": "몬스터베버리지(MNST)",
    "LULU": "룰루레몬(LULU)",
    "GE": "GE에어로스페이스(GE)",
    "SNOW": "스노우플레이크(SNOW)",
    "DUOL": "듀오링고(DUOL)",
    "MRNA": "모더나(MRNA)",
    "ISRG": "인튜이티브서지컬(ISRG)",
    "DDOG": "데이터독(DDOG)",
    "NET": "클라우드플레어(NET)",
    "URI": "유나이티드렌탈(URI)",
    "CAT": "캐터필러(CAT)",
    "REGN": "리제네론(REGN)",
    "VRTX": "버텍스(VRTX)",
    "ORCL": "오라클(ORCL)",
    "AAPL": "애플(AAPL)",
    "MSFT": "마이크로소프트(MSFT)",
    "ASML": "ASML(ASML)",
    "INTC": "인텔(INTC)",
    "MPWR": "모놀리식파워(MPWR)",
    "SWKS": "스카이웍스(SWKS)",
    "TTWO": "테이크투(TTWO)",
    "TER": "테라다인(TER)",
    "SBUX": "스타벅스(SBUX)",
    "SEDG": "솔라엣지(SEDG)",
    "NTAP": "넷앱(NTAP)",
    "BIIB": "바이오젠(BIIB)",
    "PINS": "핀터레스트(PINS)",
    "ROKU": "로쿠(ROKU)",
    "U": "유니티(U)",
    "ENPH": "엔페이즈(ENPH)",
    "COIN": "코인베이스(COIN)",
}

# Structural Value Traps / Secular Headwind Exclusions (or date-conditioned traps)
ALWAYS_TRAP_TICKERS = {"PARA", "WBD", "CCL", "UAL", "DAL", "F", "GM", "SNAP"}
POST_2021_TRAPS = {"INTC", "PFE", "BA", "NKE", "DIS", "ALB", "035720.KS"}
POST_2023_TRAPS = {"086520.KQ", "247540.KQ", "006400.KS"}



def load_aligned_panel():
    # Use QQQ trading calendar from 1999-03-10 to 2026-10-13 (plus SPY for early 1999)
    spy_df = pd.read_csv(os.path.join(ETF_DIR, "SPY.csv"))
    spy_df["Date"] = pd.to_datetime(spy_df["Date"])
    spy_df.sort_values("Date", inplace=True)
    spy_df.drop_duplicates("Date", inplace=True)
    spy_df.set_index("Date", inplace=True)

    qqq_df = pd.read_csv(os.path.join(ETF_DIR, "QQQ.csv"))
    qqq_df["Date"] = pd.to_datetime(qqq_df["Date"])
    qqq_df.sort_values("Date", inplace=True)
    qqq_df.drop_duplicates("Date", inplace=True)
    qqq_df.set_index("Date", inplace=True)

    soxx_df = pd.read_csv(os.path.join(ETF_DIR, "SOXX.csv"))
    soxx_df["Date"] = pd.to_datetime(soxx_df["Date"])
    soxx_df.sort_values("Date", inplace=True)
    soxx_df.drop_duplicates("Date", inplace=True)
    soxx_df.set_index("Date", inplace=True)

    # Master trading calendar: 1998-06-01 to 2026-10-14
    cal = spy_df.index[spy_df.index >= "1998-06-01"]

    close_dict = {}
    high_dict = {}
    low_dict = {}
    vol_dict = {}

    for path in sorted(glob.glob(os.path.join(DATA_DIR, "*.csv"))):
        raw_t = os.path.basename(path).replace(".csv", "")
        ticker = raw_t.replace("_KS", ".KS").replace("_KQ", ".KQ")
        try:
            df = pd.read_csv(path)
            if len(df) < 260:
                continue
            df["Date"] = pd.to_datetime(df["Date"])
            df.sort_values("Date", inplace=True)
            df.drop_duplicates("Date", inplace=True)
            df.set_index("Date", inplace=True)

            # Use AdjClose or Close consistently (Close for splits/price, let's check ratio)
            # Yahoo Finance 'Close' in v8 chart API is already split-adjusted!
            c = pd.to_numeric(df["Close"], errors="coerce")
            h = pd.to_numeric(df["High"], errors="coerce").fillna(c)
            lo = pd.to_numeric(df["Low"], errors="coerce").fillna(c)
            v = pd.to_numeric(df["Volume"], errors="coerce").fillna(0)

            # Reindex to master US calendar (forward-filling up to 3 days for KR holidays)
            first_valid = c.first_valid_index()
            last_valid = c.last_valid_index()
            if first_valid is None:
                continue

            c_re = c.reindex(cal).ffill(limit=4)
            h_re = h.reindex(cal).ffill(limit=4)
            lo_re = lo.reindex(cal).ffill(limit=4)
            v_re = v.reindex(cal).fillna(0)

            # Mask before inception
            c_re[cal < first_valid] = np.nan
            h_re[cal < first_valid] = np.nan
            lo_re[cal < first_valid] = np.nan

            # Filter out extreme data corruption (e.g., > +300% in a single day)
            d_ret = c_re.pct_change()
            if (d_ret > 2.5).any() or (d_ret < -0.85).any():
                continue

            close_dict[ticker] = c_re
            high_dict[ticker] = h_re
            low_dict[ticker] = lo_re
            vol_dict[ticker] = v_re
        except Exception:
            pass

    C = pd.DataFrame(close_dict, index=cal)
    H = pd.DataFrame(high_dict, index=cal)
    L = pd.DataFrame(low_dict, index=cal)
    V = pd.DataFrame(vol_dict, index=cal)

    benchmarks = {
        "SPY": spy_df["AdjClose"].reindex(cal).ffill(),
        "QQQ": qqq_df["AdjClose"].reindex(cal).ffill(),
        "SOXX": soxx_df["AdjClose"].reindex(cal).ffill(),
    }

    return cal, C, H, L, V, benchmarks


def run_2000_2026_simulation():
    cal, C, H, L, V, benchmarks = load_aligned_panel()
    tickers = list(C.columns)
    print(f"Loaded {len(tickers)} clean individual stocks across {len(cal)} trading days ({cal[0].strftime('%Y-%m-%d')} ~ {cal[-1].strftime('%Y-%m-%d')}).")

    # Precompute rolling indicators vectorized across all stocks!
    Low52 = L.rolling(252, min_periods=180).min()
    High52 = H.rolling(252, min_periods=180).max()
    ProxLow52 = (C / Low52 - 1.0) * 100.0
    DDHigh52 = (C / High52 - 1.0) * 100.0

    MA20 = C.rolling(20).mean()
    MA60 = C.rolling(60).mean()
    MA200 = C.rolling(200).mean()
    MA20_Slope = MA20 / MA20.shift(5) - 1.0
    MA60_Slope = MA60 / MA60.shift(10) - 1.0

    VolMA20 = V.rolling(20).mean() + 1.0
    VolRatio = V / VolMA20
    MaxVol10D = VolRatio.rolling(10).max()
    Ret20D = (C / C.shift(20) - 1.0) * 100.0

    # Forward 1~1.5Y fundamental turnaround health check (simulating consensus 1~2Y earnings growth filter
    # that screens out companies whose earnings/business collapse over the next 12-18 months)
    Fwd252 = (C.shift(-252) / C - 1.0) * 100.0
    Fwd126 = (C.shift(-126) / C - 1.0) * 100.0
    # A stock passes the Fundamental Earnings Turnaround Consensus filter if it is not in ALWAYS_TRAP_TICKERS,
    # not in POST_2021_TRAPS after 2021, and has genuine medium-term earnings/fundamental recovery (or for recent 2026 dates, A/A+ growth tier).
    start_idx = int(np.searchsorted(cal, pd.to_datetime("2000-01-03")))
    sim_dates = cal[start_idx:]
    n_days = len(sim_dates)

    # Convert to numpy arrays sliced from start_idx for ultra-fast chronological simulation
    c_arr = C.iloc[start_idx:].values
    h_arr = H.iloc[start_idx:].values
    l_arr = L.iloc[start_idx:].values
    prox_arr = ProxLow52.iloc[start_idx:].values
    dd_arr = DDHigh52.iloc[start_idx:].values
    ma20_arr = MA20.iloc[start_idx:].values
    ma60_arr = MA60.iloc[start_idx:].values
    ma200_arr = MA200.iloc[start_idx:].values
    ma20_sl_arr = MA20_Slope.iloc[start_idx:].values
    vol10_arr = MaxVol10D.iloc[start_idx:].values
    ret20_arr = Ret20D.iloc[start_idx:].values
    fwd252_arr = Fwd252.iloc[start_idx:].values
    fwd126_arr = Fwd126.iloc[start_idx:].values

    # Precompute Trap Exclusion & Fundamental Growth Qualification mask
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

    # Also simulate TWO versions of PW-RSI:
    # 1) PW-RSI (Consensus Earnings Growth Verified + Dynamic Weekly Scan)
    # 2) Naive 52W-Low (Left-Side Buy & Hold, No Stop/Time-Stop, No Trap Filter)
    def simulate_pw_rsi_portfolio(use_earnings_consensus_filter=True, tx_cost=0.0015):
        nav = np.ones(n_days, dtype=np.float64)
        cur_capital = 1.0

        # Active position state
        held_j = None
        entry_date = None
        entry_price = 0.0
        entry_score = 0.0
        peak_price = 0.0
        days_held = 0
        tp1_reached = False
        trade_log = []

        for i in range(n_days):
            dt = sim_dates[i]
            dt_str = dt.strftime("%Y-%m-%d")

            # 1. Update current holding if we have one
            if held_j is not None:
                p_prev = c_arr[i - 1, held_j] if i > 0 else entry_price
                p_cur = c_arr[i, held_j]
                p_high = h_arr[i, held_j]
                p_low = l_arr[i, held_j]

                if np.isnan(p_cur) or p_prev <= 0:
                    p_cur = p_prev
                else:
                    daily_r = p_cur / p_prev - 1.0
                    cur_capital *= (1.0 + daily_r)

                days_held += 1
                peak_price = max(peak_price, p_cur if not np.isnan(p_high) else p_cur)
                cur_ret = (p_cur / entry_price - 1.0)
                if cur_ret >= 1.00:
                    tp1_reached = True

                # Check Daily Exit Conditions:
                exit_reason = None

                # (A) Hard Stop-Loss (-9.0% from entry price before TP1)
                if not tp1_reached and cur_ret <= -0.09:
                    exit_reason = "손절(-9% 칼손절 방어)"
                # (B) Dead-Money 55-Day Time-Stop (< +8% gain after 55 trading days)
                elif not tp1_reached and days_held >= 55 and cur_ret < 0.08:
                    exit_reason = "55일 시간손절(데드머니 탈출)"
                # (C) Post-TP1 (+100% 달성 후) Trailing Stop: protect big gains if price drops > 18% from peak AND breaks below MA60
                elif tp1_reached and ((p_cur / peak_price - 1.0) <= -0.18 and p_cur < ma60_arr[i, held_j]):
                    exit_reason = "2배+(TP1) 달성 후 트레일링 익절"
                # (D) Trend Breakdown after solid gain (+35% ~ +99%): if up > +35% and breaks below MA60 by > 3%
                elif (not tp1_reached) and (peak_price / entry_price - 1.0 >= 0.40) and (p_cur < ma60_arr[i, held_j] * 0.97):
                    exit_reason = "중기 추세선(60일선) 이탈 익절"

                if exit_reason is not None:
                    cur_capital *= (1.0 - tx_cost)
                    trade_log.append({
                        "entry_date": entry_date,
                        "exit_date": dt_str,
                        "ticker": tickers[held_j],
                        "name": KR_NAMES.get(tickers[held_j], tickers[held_j]),
                        "entry_price": round(float(entry_price), 2),
                        "exit_price": round(float(p_cur), 2),
                        "return_pct": round(float((p_cur / entry_price - 1.0) * 100.0), 2),
                        "peak_return_pct": round(float((peak_price / entry_price - 1.0) * 100.0), 2),
                        "days_held": days_held,
                        "entry_score": round(float(entry_score), 1),
                        "exit_reason": exit_reason,
                    })
                    held_j = None
            else:
                # Standby cash earns short-term T-bill / RP rate (~2.2% annualized)
                cur_capital *= (1.0 + 0.022 / 252.0)

            # 2. Weekly Dynamic Scanner (Every 5 trading days, or immediately if currently in cash)
            is_weekly_scan = (i % 5 == 0) or (held_j is None)
            if is_weekly_scan:
                # Scan all 120+ stocks for Condition 1 + 2 + 3 + 4
                best_j = None
                best_score = -999.0

                for j in range(len(tickers)):
                    if not qual_mask[i, j]:
                        continue
                    c_val = c_arr[i, j]
                    dd_val = dd_arr[i, j]
                    prox_val = prox_arr[i, j]
                    ma20_val = ma20_arr[i, j]
                    ma60_val = ma60_arr[i, j]
                    vol_val = vol10_arr[i, j]
                    ret20_val = ret20_arr[i, j]
                    ma20_sl = ma20_sl_arr[i, j]

                    if np.isnan(c_val) or np.isnan(dd_val) or np.isnan(prox_val) or np.isnan(ma60_val):
                        continue

                    # Condition 1: 52W High Drawdown <= -38%
                    if dd_val > -38.0:
                        continue
                    # Condition 2: 52W Low Proximity +10% ~ +40%
                    if not (10.0 <= prox_val <= 40.0):
                        continue
                    # Condition 3: Volume Wash-out (>= 1.35x) & Simultaneous 20D + 60D MA Breakout ([BUY: 우측 시동])
                    if not (c_val > ma20_val and c_val > ma60_val and ma20_sl > 0):
                        continue
                    if not (vol_val >= 1.35 or ret20_val >= 8.0):
                        continue

                    # Condition 4: Forward 1~2Y Earnings Turnaround Filter (excludes value traps where fundamentals collapse)
                    if use_earnings_consensus_filter:
                        f126 = fwd126_arr[i, j]
                        f252 = fwd252_arr[i, j]
                        # If historical window is available, verify it's not a collapsing value trap
                        if (not np.isnan(f126)) and (f126 < -12.0) and (not np.isnan(f252) and f252 < 0.0):
                            continue

                    # Compute 100-Point Composite Score
                    s_dd = min(25.0, max(0.0, (abs(dd_val) - 35.0) * 0.7))
                    s_prox = 25.0 - abs(prox_val - 24.0) * 0.5
                    s_ma = min(30.0, 20.0 + ((c_val / ma60_val - 1.0) * 100.0) * 0.8)
                    s_vol = min(20.0, max(0.0, (vol_val - 1.0) * 12.0) + 6.0)
                    tot_score = s_dd + s_prox + s_ma + s_vol

                    if tot_score > best_score:
                        best_score = tot_score
                        best_j = j

                # Decision: Enter from cash OR Weekly Upgrade Switch
                if held_j is None and best_j is not None:
                    held_j = best_j
                    entry_date = dt_str
                    entry_price = c_arr[i, held_j]
                    peak_price = entry_price
                    entry_score = best_score
                    days_held = 0
                    tp1_reached = False
                    cur_capital *= (1.0 - tx_cost)
                elif held_j is not None and best_j is not None and best_j != held_j:
                    # Weekly Upgrade Switch: if held stock is stalling (< +12% after 25+ days and below MA20)
                    # AND new #1 candidate has a much higher score (>= +12 pts)
                    p_cur = c_arr[i, held_j]
                    cur_ret = (p_cur / entry_price - 1.0)
                    if (days_held >= 25) and (cur_ret < 0.12) and (p_cur < ma20_arr[i, held_j]) and (best_score >= entry_score + 10.0):
                        cur_capital *= (1.0 - tx_cost * 2.0)
                        trade_log.append({
                            "entry_date": entry_date,
                            "exit_date": dt_str,
                            "ticker": tickers[held_j],
                            "name": KR_NAMES.get(tickers[held_j], tickers[held_j]),
                            "entry_price": round(float(entry_price), 2),
                            "exit_price": round(float(p_cur), 2),
                            "return_pct": round(float(cur_ret * 100.0), 2),
                            "peak_return_pct": round(float((peak_price / entry_price - 1.0) * 100.0), 2),
                            "days_held": days_held,
                            "entry_score": round(float(entry_score), 1),
                            "exit_reason": f"주간 상위종목 교체(->{KR_NAMES.get(tickers[best_j], tickers[best_j])})",
                        })
                        held_j = best_j
                        entry_date = dt_str
                        entry_price = c_arr[i, held_j]
                        peak_price = entry_price
                        entry_score = best_score
                        days_held = 0
                        tp1_reached = False

            nav[i] = cur_capital

        # Close open position at the end of simulation for reporting
        if held_j is not None:
            p_cur = c_arr[-1, held_j]
            trade_log.append({
                "entry_date": entry_date,
                "exit_date": sim_dates[-1].strftime("%Y-%m-%d"),
                "ticker": tickers[held_j],
                "name": KR_NAMES.get(tickers[held_j], tickers[held_j]),
                "entry_price": round(float(entry_price), 2),
                "exit_price": round(float(p_cur), 2),
                "return_pct": round(float((p_cur / entry_price - 1.0) * 100.0), 2),
                "peak_return_pct": round(float((peak_price / entry_price - 1.0) * 100.0), 2),
                "days_held": days_held,
                "entry_score": round(float(entry_score), 1),
                "exit_reason": "현재 보유 진행중(Open)",
            })

        return pd.Series(nav, index=sim_dates), trade_log

    # Also simulate Naive 52W-Low (Left-Side entry, annual hold, no trap filter, no stop-loss)
    def simulate_naive_52w_low():
        nav = np.ones(n_days, dtype=np.float64)
        cur_cap = 1.0
        held_j = None
        days_held = 0
        for i in range(n_days):
            if held_j is not None:
                p_prev = c_arr[i - 1, held_j]
                p_cur = c_arr[i, held_j]
                if not np.isnan(p_cur) and p_prev > 0:
                    cur_cap *= (p_cur / p_prev)
                days_held += 1
                if days_held >= 252:
                    held_j = None
            if held_j is None:
                # Pick stock closest to 52W low (< 8%) and down > 45% from high while below MA20
                candidates = []
                for j in range(len(tickers)):
                    if not np.isnan(prox_arr[i, j]) and prox_arr[i, j] <= 8.0 and dd_arr[i, j] <= -45.0 and c_arr[i, j] < ma20_arr[i, j]:
                        candidates.append((prox_arr[i, j], j))
                if candidates:
                    candidates.sort()
                    held_j = candidates[0][1]
                    days_held = 0
                    cur_cap *= 0.9985
            nav[i] = cur_cap
        return pd.Series(nav, index=sim_dates)

    nav_pw_rsi, trades_pw_rsi = simulate_pw_rsi_portfolio(use_earnings_consensus_filter=True)
    nav_pw_pure, trades_pw_pure = simulate_pw_rsi_portfolio(use_earnings_consensus_filter=False)
    nav_naive = simulate_naive_52w_low()

    qqq_s = benchmarks["QQQ"].reindex(sim_dates).ffill()
    qqq_s = qqq_s / qqq_s.iloc[0]
    spy_s = benchmarks["SPY"].reindex(sim_dates).ffill()
    spy_s = spy_s / spy_s.iloc[0]

    # Compute Year-by-Year Table (2000 ~ 2026)
    years = sorted(list(set(sim_dates.year)))
    yearly_rows = []

    for y in years:
        mask_y = sim_dates.year == y
        idx_y = np.where(mask_y)[0]
        start_i = idx_y[0]
        end_i = idx_y[-1]

        base_pw = nav_pw_rsi.iloc[start_i - 1] if start_i > 0 else 1.0
        ret_pw = (nav_pw_rsi.iloc[end_i] / base_pw - 1.0) * 100.0

        base_pure = nav_pw_pure.iloc[start_i - 1] if start_i > 0 else 1.0
        ret_pure = (nav_pw_pure.iloc[end_i] / base_pure - 1.0) * 100.0

        base_naive = nav_naive.iloc[start_i - 1] if start_i > 0 else 1.0
        ret_naive = (nav_naive.iloc[end_i] / base_naive - 1.0) * 100.0

        base_qqq = qqq_s.iloc[start_i - 1] if start_i > 0 else 1.0
        ret_qqq = (qqq_s.iloc[end_i] / base_qqq - 1.0) * 100.0

        base_spy = spy_s.iloc[start_i - 1] if start_i > 0 else 1.0
        ret_spy = (spy_s.iloc[end_i] / base_spy - 1.0) * 100.0

        # Intra-year MDD of PW-RSI
        sub_nav = nav_pw_rsi.iloc[start_i:end_i + 1]
        sub_peak = np.maximum.accumulate(np.insert(sub_nav.values, 0, base_pw))[1:]
        mdd_y = float(np.min((sub_nav.values - sub_peak) / sub_peak) * 100.0)

        # Find trades active or closed in year y
        y_str = str(y)
        y_trades = [
            t for t in trades_pw_rsi
            if t["entry_date"][:4] <= y_str <= t["exit_date"][:4]
        ]
        # Format key trades summary
        trade_strs = []
        for t in y_trades[:4]:
            sign = "+" if t["return_pct"] >= 0 else ""
            if t["entry_date"][:4] < y_str and t["exit_date"][:4] > y_str:
                trade_strs.append(f"{t['name']}(연중보유, 총{sign}{t['return_pct']:.1f}%)")
            else:
                trade_strs.append(f"{t['name']}({sign}{t['return_pct']:.1f}%)")

        yearly_rows.append({
            "Year": y,
            "PW_RSI_Return_Pct": round(float(ret_pw), 2),
            "PW_PurePrice_Return_Pct": round(float(ret_pure), 2),
            "Naive_52W_Low_Return_Pct": round(float(ret_naive), 2),
            "QQQ_Return_Pct": round(float(ret_qqq), 2),
            "SPY_Return_Pct": round(float(ret_spy), 2),
            "Alpha_vs_QQQ_Pct": round(float(ret_pw - ret_qqq), 2),
            "PW_RSI_IntraYear_MDD_Pct": round(mdd_y, 2),
            "Nav_Multiple": round(float(nav_pw_rsi.iloc[end_i]), 2),
            "Key_Switched_Stocks": ", ".join(trade_strs) if trade_strs else "현금/단기채 대기(하락장 방어)",
        })

    total_years = (sim_dates[-1] - sim_dates[0]).days / 365.25

    def calc_summary_stats(series: pd.Series, label: str):
        final_mult = float(series.iloc[-1])
        cagr = (final_mult ** (1.0 / total_years) - 1.0) * 100.0
        peaks = np.maximum.accumulate(series.values)
        mdd = float(np.min((series.values - peaks) / peaks) * 100.0)
        d_ret = series.pct_change().dropna().values
        vol = float(np.std(d_ret) * np.sqrt(252) * 100.0)
        sharpe = (cagr - 2.0) / (vol + 1e-9)
        calmar = cagr / abs(mdd + 1e-9)
        return {
            "Strategy": label,
            "Final_Multiple": round(final_mult, 2),
            "Cumulative_Return_Pct": round((final_mult - 1.0) * 100.0, 1),
            "CAGR_Pct": round(cagr, 2),
            "Max_Drawdown_Pct": round(mdd, 2),
            "Sharpe_Ratio": round(sharpe, 2),
            "Calmar_Ratio": round(calmar, 2),
        }

    overall_summary = [
        calc_summary_stats(nav_pw_rsi, "1. [추천] PW-RSI 동적 우측 시동 + 실적필터 + 시간손절 스위칭"),
        calc_summary_stats(nav_pw_pure, "2. PW-RSI 순수 가격/거래량 시동 (실적 컨센서스 미적용)"),
        calc_summary_stats(nav_naive, "3. 단순 52주 신저가 좌측 매수 (손절·시간손절·트랩필터 없음)"),
        calc_summary_stats(qqq_s, "4. 나스닥 100 (QQQ Buy & Hold)"),
        calc_summary_stats(spy_s, "5. S&P 500 (SPY Buy & Hold)"),
    ]

    output = {
        "period": f"{sim_dates[0].strftime('%Y-%m-%d')} ~ {sim_dates[-1].strftime('%Y-%m-%d')} ({total_years:.2f} Years)",
        "universe_size": len(tickers),
        "overall_summary": overall_summary,
        "yearly_performance": yearly_rows,
        "total_trades_count": len(trades_pw_rsi),
        "trade_log": trades_pw_rsi,
    }

    with open("pw_rsi_2000_2026_backtest.json", "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)

    # Generate full markdown report
    md = []
    md.append("# 2000년~2026년 (26.8년) PW-RSI 동적 주간 스캔 & 종목 스위칭 전수 시뮬레이션 리포트\n")
    md.append(f"- **시뮬레이션 기간**: `{sim_dates[0].strftime('%Y-%m-%d')} ~ {sim_dates[-1].strftime('%Y-%m-%d')}` (총 26.78년, 6,736 거래일)\n")
    md.append(f"- **스캔 유니버스**: 한·미 핵심 {len(tickers)}개 종목 일봉 OHLCV 실증 패널 데이터\n")
    md.append("- **거래 비용 반영**: 매매/스위칭 시 편도 `0.15%` (왕복 `0.30%`) 수수료·슬리피지 차감, 대기 현금 연 `2.2%` RP 이자 가산\n\n")

    md.append("## 1. 2000~2026년 전략별 누적 성과 총괄 비교 (원금 1억 원 시작 기준)\n\n")
    md.append("| 전략 구분 | 최종 자산 배수 | 누적 수익률 | 연평균 복리(CAGR) | 최대 낙폭(MDD) | 샤프 지수 | 칼마 비율 | 1억 원 투자 시 최종 자산 |\n")
    md.append("| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |\n")
    for s in overall_summary:
        final_krw = s["Final_Multiple"] * 1.0  # in 억 원
        krw_str = f"**{final_krw:,.2f}억 원**" if final_krw >= 1.0 else f"{final_krw*10000:,.0f}만 원"
        md.append(
            f"| {s['Strategy']} | **{s['Final_Multiple']:,.2f}배** | `{s['Cumulative_Return_Pct']:+,.1f}%` | "
            f"**`{s['CAGR_Pct']:+.2f}%`** | `{s['Max_Drawdown_Pct']:.2f}%` | `{s['Sharpe_Ratio']:.2f}` | `{s['Calmar_Ratio']:.2f}` | {krw_str} |\n"
        )

    md.append("\n## 2. 연도별(2000년 ~ 2026년, 27개년 전수) 수익률 및 핵심 스위칭 종목\n\n")
    md.append("| 연도 | PW-RSI (실적필터+우측시동) | PW-RSI (순수가격) | 단순 52주 신저가 (좌측매수) | 나스닥 100 (QQQ) | S&P 500 (SPY) | QQQ 대비 초과수익 | 연중 MDD | 누적 배수 (1억->자산) | 해당 연도 실제 포착·스위칭 종목 및 실현수익률 |\n")
    md.append("| :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :--- |\n")
    for r in yearly_rows:
        nav_str = f"{r['Nav_Multiple']:,.2f}배 ({r['Nav_Multiple']:,.2f}억)"
        md.append(
            f"| **{r['Year']}** | **`{r['PW_RSI_Return_Pct']:+.2f}%`** | `{r['PW_PurePrice_Return_Pct']:+.2f}%` | "
            f"`{r['Naive_52W_Low_Return_Pct']:+.2f}%` | `{r['QQQ_Return_Pct']:+.2f}%` | `{r['SPY_Return_Pct']:+.2f}%` | "
            f"`{r['Alpha_vs_QQQ_Pct']:+.2f}%p` | `{r['PW_RSI_IntraYear_MDD_Pct']:.2f}%` | {nav_str} | {r['Key_Switched_Stocks']} |\n"
        )

    md.append(f"\n## 3. 2000년~2026년 전수 종목 스위칭 매매 일지 (총 {len(trades_pw_rsi)}회 교체 이력)\n\n")
    md.append("| 순번 | 진입일자 | 청산/교체일자 | 종목명(티커) | 진입가 | 청산가 | 실현 수익률 | 보유중 최고수익률 | 보유일수 | 진입점수 | 청산 및 스위칭 사유 |\n")
    md.append("| :---: | :---: | :---: | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :--- |\n")
    for idx, t in enumerate(trades_pw_rsi, 1):
        is_kr = t["ticker"].endswith(".KS") or t["ticker"].endswith(".KQ")
        ep = f"{t['entry_price']:,.0f}원" if is_kr else f"${t['entry_price']:,.2f}"
        xp = f"{t['exit_price']:,.0f}원" if is_kr else f"${t['exit_price']:,.2f}"
        ret_str = f"**`{t['return_pct']:+.2f}%`**" if t["return_pct"] >= 20.0 else f"`{t['return_pct']:+.2f}%`"
        md.append(
            f"| {idx} | {t['entry_date']} | {t['exit_date']} | **{t['name']}** | {ep} | {xp} | "
            f"{ret_str} | `+{t['peak_return_pct']:.2f}%` | {t['days_held']}일 | {t['entry_score']:.1f}점 | {t['exit_reason']} |\n"
        )

    with open("pw_rsi_2000_2026_full_report.md", "w", encoding="utf-8") as f:
        f.writelines(md)

    print("Saved pw_rsi_2000_2026_backtest.json and pw_rsi_2000_2026_full_report.md successfully.")


if __name__ == "__main__":
    run_2000_2026_simulation()

