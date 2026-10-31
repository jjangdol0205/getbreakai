"""
시계열 정밀 비교 분석:
[SMH 70% + XLV 30% (반도체 70% + 헬스케어 30%)] vs [PW-RSI 알파 스위칭 전략]
1) 2000~2026 (26.8년 전체), 2010~2026 (16.8년), 2015~2026 (11.8년), 2020~2026 (최근 6.8년) 구간별 성과 비교
2) 세전(Pre-Tax) vs 세후(After-Tax, 매년 22% 양도세 vs ETF 장기보유 과세이연 효과) 정밀 비교
3) 백테스트의 '이익성장 프록시(Look-ahead 편향 가능성)'를 완전히 제거한 100% 순수 실전(Point-in-Time) PW-RSI 성과 검증
4) 하이브리드 결합: 대기 자금을 현금(RP 2.2%)이 아니라 [SMH 70% + XLV 30%]에 파킹하거나, [코어 SMH 70%+XLV 30% + 알파 위성]으로 운용할 때의 성과 비교
"""

import os
import sys
import json
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
    ALWAYS_TRAP_TICKERS,
    POST_2021_TRAPS,
    POST_2023_TRAPS,
)
from backtest_realistic_tax_fx_lag import load_usdkrw_series

HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}


def fetch_yahoo_daily(ticker: str):
    p1 = int(datetime(1998, 1, 1).timestamp())
    p2 = int(datetime(2026, 10, 30).timestamp())
    url = f"https://query1.finance.yahoo.com/v8/finance/chart/{ticker}?period1={p1}&period2={p2}&interval=1d"
    r = requests.get(url, headers=HEADERS, verify=False, timeout=15)
    if r.status_code == 200:
        res = r.json()["chart"]["result"][0]
        ts = res["timestamp"]
        q = res["indicators"]["quote"][0]
        adj = res["indicators"].get("adjclose", [{}])[0].get("adjclose", q["close"])
        df = pd.DataFrame({
            "Date": pd.to_datetime([datetime.fromtimestamp(t).strftime("%Y-%m-%d") for t in ts]),
            "Close": adj if adj is not None else q["close"],
        }).dropna()
        df.set_index("Date", inplace=True)
        return df
    return None


def load_smh_xlv(cal: pd.DatetimeIndex):
    os.makedirs("data", exist_ok=True)
    for t in ["SMH", "XLV", "^SOX"]:
        safe = t.replace("^", "IDX_")
        path = os.path.join("data", f"{safe}.csv")
        if not os.path.exists(path):
            df = fetch_yahoo_daily(t)
            if df is not None and not df.empty:
                df.to_csv(path)

    def read_close(t):
        safe = t.replace("^", "IDX_")
        path = os.path.join("data", f"{safe}.csv")
        if not os.path.exists(path):
            return pd.Series(index=cal, dtype=float)
        df = pd.read_csv(path, index_col=0, parse_dates=True)
        df = df[~df.index.duplicated(keep="last")].sort_index()
        s = pd.to_numeric(df["Close"], errors="coerce")
        return s.reindex(cal).ffill()

    smh = read_close("SMH")
    xlv = read_close("XLV")
    sox = read_close("^SOX")

    # SMH started in May 2000; backfill Jan~Apr 2000 using ^SOX daily returns
    if smh.isna().any() and not sox.isna().all():
        first_valid = smh.first_valid_index()
        if first_valid is not None:
            loc = cal.get_loc(first_valid)
            for idx in range(loc - 1, -1, -1):
                if sox.iloc[idx] > 0 and sox.iloc[idx + 1] > 0:
                    smh.iloc[idx] = smh.iloc[idx + 1] * (sox.iloc[idx] / sox.iloc[idx + 1])
    smh = smh.bfill().ffill()
    xlv = xlv.bfill().ffill()
    return smh, xlv


def calc_stats(nav: np.ndarray, dates: pd.DatetimeIndex):
    n_years = (dates[-1] - dates[0]).days / 365.25
    total_mult = float(nav[-1] / nav[0])
    cagr = (total_mult ** (1.0 / n_years) - 1.0) * 100.0
    peak = np.maximum.accumulate(nav)
    dd = (nav / peak - 1.0) * 100.0
    mdd = float(dd.min())
    daily_ret = pd.Series(nav).pct_change().dropna()
    vol = float(daily_ret.std() * np.sqrt(252) * 100.0)
    sharpe = float(((cagr / 100.0) - 0.025) / (vol / 100.0)) if vol > 0 else 0.0
    downside = daily_ret[daily_ret < 0].std() * np.sqrt(252) * 100.0
    sortino = float(((cagr / 100.0) - 0.025) / (downside / 100.0)) if downside > 0 else 0.0
    return {
        "n_years": round(n_years, 2),
        "total_mult": round(total_mult, 2),
        "total_return_pct": round((total_mult - 1.0) * 100.0, 1),
        "cagr_pct": round(cagr, 2),
        "mdd_pct": round(mdd, 2),
        "vol_pct": round(vol, 2),
        "sharpe": round(sharpe, 2),
        "sortino": round(sortino, 2),
    }


def simulate_smh_xlv(
    sim_dates: pd.DatetimeIndex,
    smh_arr: np.ndarray,
    xlv_arr: np.ndarray,
    fx_arr: np.ndarray,
    w_smh: float = 0.70,
    w_xlv: float = 0.30,
    rebalance: str = "annual",  # 'none' (Buy & Hold), 'annual', 'quarterly'
    apply_tax_and_fx: bool = True,
    initial_krw: float = 100_000_000.0,
):
    n_days = len(sim_dates)
    nav_krw = np.zeros(n_days, dtype=np.float64)

    # Initial conversion to USD (-0.12% FX spread + -0.10% ETF buy fee)
    cur_krw = initial_krw * (1.0 - (0.0022 if apply_tax_and_fx else 0.0))
    val_smh = cur_krw * w_smh
    val_xlv = cur_krw * w_xlv
    cost_smh = val_smh
    cost_xlv = val_xlv

    for i in range(n_days):
        dt = sim_dates[i]
        if i > 0:
            fx_mult = (fx_arr[i] / fx_arr[i - 1]) if apply_tax_and_fx else 1.0
            r_smh = (smh_arr[i] / smh_arr[i - 1]) if smh_arr[i - 1] > 0 else 1.0
            r_xlv = (xlv_arr[i] / xlv_arr[i - 1]) if xlv_arr[i - 1] > 0 else 1.0
            # Add approximate ETF dividend yield reinvested (SMH ~0.8%/yr, XLV ~1.5%/yr after 15% US dividend tax)
            div_smh = (0.008 * 0.85) / 252.0
            div_xlv = (0.015 * 0.85) / 252.0
            val_smh *= (r_smh + div_smh) * fx_mult
            val_xlv *= (r_xlv + div_xlv) * fx_mult

        tot_val = val_smh + val_xlv

        # Rebalancing check at year-end
        is_year_end = (i == n_days - 1) or (sim_dates[i + 1].year != dt.year)
        if is_year_end and rebalance == "annual" and i < n_days - 1:
            target_smh = tot_val * w_smh
            target_xlv = tot_val * w_xlv
            diff_smh = val_smh - target_smh
            realized_gain = 0.0
            if diff_smh > 0:
                # Selling excess SMH to buy XLV
                sell_amt = diff_smh
                prop_sold = sell_amt / val_smh
                cost_sold = cost_smh * prop_sold
                gain = sell_amt - cost_sold
                realized_gain += gain
                cost_smh -= cost_sold
                cost_xlv += sell_amt
            elif diff_smh < 0:
                # Selling excess XLV to buy SMH
                sell_amt = -diff_smh
                prop_sold = sell_amt / val_xlv
                cost_sold = cost_xlv * prop_sold
                gain = sell_amt - cost_sold
                realized_gain += gain
                cost_xlv -= cost_sold
                cost_smh += sell_amt

            # Fee on rebalanced amount
            rebal_fee = abs(diff_smh) * (0.0020 if apply_tax_and_fx else 0.0)
            tax_krw = 0.0
            if apply_tax_and_fx and realized_gain > 2_500_000.0:
                tax_krw = (realized_gain - 2_500_000.0) * 0.22

            tot_after = tot_val - rebal_fee - tax_krw
            val_smh = tot_after * w_smh
            val_xlv = tot_after * w_xlv
            tot_val = val_smh + val_xlv

        nav_krw[i] = tot_val

    # Also compute final liquidation after-tax value (if liquidated at the very end)
    final_pre_liquidation = nav_krw[-1]
    remaining_unrealized_gain = (val_smh - cost_smh) + (val_xlv - cost_xlv)
    final_liquidation_tax = max(0.0, remaining_unrealized_gain - 2_500_000.0) * 0.22 if apply_tax_and_fx else 0.0
    final_after_all_tax = final_pre_liquidation - final_liquidation_tax

    return nav_krw, final_after_all_tax


def run_comparison():
    cal, C, H, L, V, benchmarks = load_aligned_panel()
    fx_series = load_usdkrw_series(cal)
    smh_s, xlv_s = load_smh_xlv(cal)

    tickers = list(C.columns)
    is_kr_arr = np.array([t.endswith(".KS") or t.endswith(".KQ") for t in tickers], dtype=bool)

    Low52 = L.rolling(252, min_periods=180).min()
    High52 = H.rolling(252, min_periods=180).max()
    ProxLow52 = (C / Low52 - 1.0) * 100.0
    DDHigh52 = (C / High52 - 1.0) * 100.0

    MA20 = C.rolling(20).mean()
    MA60 = C.rolling(60).mean()
    MA200 = C.rolling(200).mean()
    MA20_Slope = MA20 / MA20.shift(5) - 1.0

    VolMA20 = V.rolling(20).mean() + 1.0
    VolRatio = V / VolMA20
    MaxVol10D = VolRatio.rolling(10).max()
    Ret20D = (C / C.shift(20) - 1.0) * 100.0

    Fwd252 = (C.shift(-252) / C - 1.0) * 100.0
    Fwd126 = (C.shift(-126) / C - 1.0) * 100.0

    start_idx = int(np.searchsorted(cal, pd.to_datetime("2000-01-03")))
    sim_dates = cal[start_idx:]
    n_days = len(sim_dates)

    c_arr = C.iloc[start_idx:].values
    h_arr = H.iloc[start_idx:].values
    prox_arr = ProxLow52.iloc[start_idx:].values
    dd_arr = DDHigh52.iloc[start_idx:].values
    ma20_arr = MA20.iloc[start_idx:].values
    ma60_arr = MA60.iloc[start_idx:].values
    ma20_sl_arr = MA20_Slope.iloc[start_idx:].values
    vol10_arr = MaxVol10D.iloc[start_idx:].values
    ret20_arr = Ret20D.iloc[start_idx:].values
    fwd252_arr = Fwd252.iloc[start_idx:].values
    fwd126_arr = Fwd126.iloc[start_idx:].values
    fx_arr = fx_series.iloc[start_idx:].values
    smh_arr = smh_s.iloc[start_idx:].values
    xlv_arr = xlv_s.iloc[start_idx:].values
    qqq_arr = benchmarks["QQQ"].iloc[start_idx:].values

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

    def score_candidates_at_day(i: int, us_only: bool = True, use_fwd_proxy: bool = True):
        best_j = None
        best_score = -999.0
        for j in range(len(tickers)):
            if us_only and is_kr_arr[j]:
                continue
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
            if dd_val > -38.0:
                continue
            if not (10.0 <= prox_val <= 40.0):
                continue
            if not (c_val > ma20_val and c_val > ma60_val and ma20_sl > 0):
                continue
            if not (vol_val >= 1.35 or ret20_val >= 8.0):
                continue

            if use_fwd_proxy:
                f126 = fwd126_arr[i, j]
                f252 = fwd252_arr[i, j]
                if (not np.isnan(f126)) and (f126 < -12.0) and (not np.isnan(f252) and f252 < 0.0):
                    continue

            s_dd = min(25.0, max(0.0, (abs(dd_val) - 35.0) * 0.7))
            s_prox = 25.0 - abs(prox_val - 24.0) * 0.5
            s_ma = min(30.0, 20.0 + ((c_val / ma60_val - 1.0) * 100.0) * 0.8)
            s_vol = min(20.0, max(0.0, (vol_val - 1.0) * 12.0) + 6.0)
            tot_score = s_dd + s_prox + s_ma + s_vol

            if tot_score > best_score:
                best_score = tot_score
                best_j = j
        return best_j, best_score

    def simulate_pw_rsi(
        use_fwd_proxy: bool = True,
        idle_mode: str = "cash",  # 'cash' (2.2% RP) or 'smh_xlv' (park in SMH 70% + XLV 30%)
        apply_tax_and_fx: bool = True,
        initial_krw: float = 100_000_000.0,
    ):
        nav_krw = np.zeros(n_days, dtype=np.float64)
        cur_krw = initial_krw * (1.0 - (0.0012 if apply_tax_and_fx else 0.0))

        held_j = None
        entry_price_local = 0.0
        entry_krw_principal = 0.0
        entry_score = 0.0
        peak_price_local = 0.0
        days_held = 0
        tp1_reached = False
        yr_us_realized_net_gain_krw = 0.0

        us_buy_fee = 0.0020 if apply_tax_and_fx else 0.0015
        us_sell_fee = 0.0020 if apply_tax_and_fx else 0.0015

        for i in range(n_days):
            dt = sim_dates[i]
            fx_now = fx_arr[i] if apply_tax_and_fx else 1.0
            fx_prev = fx_arr[i - 1] if (i > 0 and apply_tax_and_fx) else fx_now
            fx_mult = fx_now / fx_prev

            if held_j is not None:
                p_prev = c_arr[i - 1, held_j] if i > 0 else entry_price_local
                p_cur = c_arr[i, held_j]
                p_high = h_arr[i, held_j]
                if np.isnan(p_cur) or p_prev <= 0:
                    p_cur = p_prev
                else:
                    cur_krw *= (p_cur / p_prev) * fx_mult

                days_held += 1
                peak_price_local = max(peak_price_local, p_cur if not np.isnan(p_high) else p_cur)
                cur_ret_local = (p_cur / entry_price_local - 1.0)
                if cur_ret_local >= 1.00:
                    tp1_reached = True

                exit_reason = None
                if not tp1_reached and cur_ret_local <= -0.09:
                    exit_reason = "SL"
                elif not tp1_reached and days_held >= 55 and cur_ret_local < 0.08:
                    exit_reason = "TIME"
                elif tp1_reached and ((p_cur / peak_price_local - 1.0) <= -0.18 and p_cur < ma60_arr[i, held_j]):
                    exit_reason = "TP1_TRAIL"
                elif (not tp1_reached) and (peak_price_local / entry_price_local - 1.0 >= 0.40) and (p_cur < ma60_arr[i, held_j] * 0.97):
                    exit_reason = "MA60_TRAIL"

                if exit_reason is not None:
                    cur_krw *= (1.0 - us_sell_fee)
                    realized_pnl_krw = cur_krw - entry_krw_principal
                    yr_us_realized_net_gain_krw += realized_pnl_krw
                    held_j = None
            else:
                if idle_mode == "smh_xlv" and i > 0:
                    r_smh = (smh_arr[i] / smh_arr[i - 1]) if smh_arr[i - 1] > 0 else 1.0
                    r_xlv = (xlv_arr[i] / xlv_arr[i - 1]) if xlv_arr[i - 1] > 0 else 1.0
                    r_blend = 0.70 * r_smh + 0.30 * r_xlv
                    cur_krw *= r_blend * fx_mult
                else:
                    cur_krw *= (1.0 + 0.022 / 252.0) * fx_mult

            is_weekly_scan = (i % 5 == 0) or (held_j is None)
            if is_weekly_scan:
                best_j, best_score = score_candidates_at_day(i, us_only=True, use_fwd_proxy=use_fwd_proxy)
                if held_j is None and best_j is not None:
                    cur_krw *= (1.0 - us_buy_fee)
                    held_j = best_j
                    entry_price_local = c_arr[i, held_j]
                    entry_krw_principal = cur_krw
                    peak_price_local = entry_price_local
                    entry_score = best_score
                    days_held = 0
                    tp1_reached = False
                elif held_j is not None and best_j is not None and best_j != held_j:
                    p_cur = c_arr[i, held_j]
                    cur_ret_local = (p_cur / entry_price_local - 1.0)
                    if (days_held >= 25) and (cur_ret_local < 0.12) and (p_cur < ma20_arr[i, held_j]) and (best_score >= entry_score + 10.0):
                        cur_krw *= (1.0 - us_sell_fee)
                        yr_us_realized_net_gain_krw += (cur_krw - entry_krw_principal)
                        cur_krw *= (1.0 - us_buy_fee)
                        held_j = best_j
                        entry_price_local = c_arr[i, held_j]
                        entry_krw_principal = cur_krw
                        peak_price_local = entry_price_local
                        entry_score = best_score
                        days_held = 0
                        tp1_reached = False

            is_year_end = (i == n_days - 1) or (sim_dates[i + 1].year != dt.year)
            if is_year_end and apply_tax_and_fx:
                if yr_us_realized_net_gain_krw > 2_500_000.0:
                    tax_krw = (yr_us_realized_net_gain_krw - 2_500_000.0) * 0.22
                    cur_krw = max(1000.0, cur_krw - tax_krw)
                    if held_j is not None:
                        entry_krw_principal *= (cur_krw / (cur_krw + tax_krw))
                yr_us_realized_net_gain_krw = 0.0

            nav_krw[i] = cur_krw

        return nav_krw

    # Run all strategies
    nav_smh100, _ = simulate_smh_xlv(sim_dates, smh_arr, xlv_arr, fx_arr, w_smh=1.0, w_xlv=0.0, rebalance="none", apply_tax_and_fx=True)
    nav_xlv100, _ = simulate_smh_xlv(sim_dates, smh_arr, xlv_arr, fx_arr, w_smh=0.0, w_xlv=1.0, rebalance="none", apply_tax_and_fx=True)
    nav_70_30_rebal, final_70_30_liq = simulate_smh_xlv(sim_dates, smh_arr, xlv_arr, fx_arr, w_smh=0.70, w_xlv=0.30, rebalance="annual", apply_tax_and_fx=True)
    nav_70_30_bh, final_70_30_bh_liq = simulate_smh_xlv(sim_dates, smh_arr, xlv_arr, fx_arr, w_smh=0.70, w_xlv=0.30, rebalance="none", apply_tax_and_fx=True)

    # Also test: SMH 70% + XLV 30% + Dynamic Right-Side Overweight (90/10 when SMH DD <= -22% & > MA20 & > MA60)
    smh_hi52 = smh_s.rolling(252, min_periods=180).max().iloc[start_idx:].values
    smh_lo52 = smh_s.rolling(252, min_periods=180).min().iloc[start_idx:].values
    smh_dd = (smh_arr / smh_hi52 - 1.0) * 100.0
    smh_prox = (smh_arr / smh_lo52 - 1.0) * 100.0
    smh_ma20 = smh_s.rolling(20).mean().iloc[start_idx:].values
    smh_ma60 = smh_s.rolling(60).mean().iloc[start_idx:].values

    nav_70_30_tilt = np.zeros(n_days, dtype=np.float64)
    c_krw = 100_000_000.0 * (1.0 - 0.0022)
    v_smh = c_krw * 0.70
    v_xlv = c_krw * 0.30
    cost_s = v_smh
    cost_x = v_xlv
    ow_mode = False
    ow_entry_p = 0.0
    for i in range(n_days):
        dt = sim_dates[i]
        if i > 0:
            fx_m = fx_arr[i] / fx_arr[i - 1]
            r_s = (smh_arr[i] / smh_arr[i - 1]) + (0.008 * 0.85) / 252.0
            r_x = (xlv_arr[i] / xlv_arr[i - 1]) + (0.015 * 0.85) / 252.0
            v_smh *= r_s * fx_m
            v_xlv *= r_x * fx_m
        tot = v_smh + v_xlv
        if (not ow_mode) and (smh_dd[i] <= -22.0) and (8.0 <= smh_prox[i] <= 40.0) and (smh_arr[i] > smh_ma20[i]) and (smh_arr[i] > smh_ma60[i]):
            target_s = tot * 0.90
            if target_s > v_smh:
                buy_s = target_s - v_smh
                prop_x = buy_s / v_xlv
                gain_x = buy_s - cost_x * prop_x
                cost_x *= (1.0 - prop_x)
                cost_s += buy_s
                fee = buy_s * 0.0020
                tax = max(0.0, gain_x - 2_500_000.0) * 0.22
                tot -= (fee + tax)
                v_smh = tot * 0.90
                v_xlv = tot * 0.10
                ow_mode = True
                ow_entry_p = smh_arr[i]
        elif ow_mode and (smh_arr[i] / ow_entry_p - 1.0 >= 0.45):
            target_s = tot * 0.70
            if v_smh > target_s:
                sell_s = v_smh - target_s
                prop_s = sell_s / v_smh
                gain_s = sell_s - cost_s * prop_s
                cost_s *= (1.0 - prop_s)
                cost_x += sell_s
                fee = sell_s * 0.0020
                tax = max(0.0, gain_s - 2_500_000.0) * 0.22
                tot -= (fee + tax)
                v_smh = tot * 0.70
                v_xlv = tot * 0.30
            ow_mode = False

        is_ye = (i == n_days - 1) or (sim_dates[i + 1].year != dt.year)
        if is_ye and (not ow_mode) and i < n_days - 1:
            target_s = tot * 0.70
            diff = v_smh - target_s
            gain = 0.0
            if diff > 0:
                prop = diff / v_smh
                gain = diff - cost_s * prop
                cost_s *= (1.0 - prop)
                cost_x += diff
            elif diff < 0:
                sell_x = -diff
                prop = sell_x / v_xlv
                gain = sell_x - cost_x * prop
                cost_x *= (1.0 - prop)
                cost_s += sell_x
            fee = abs(diff) * 0.0020
            tax = max(0.0, gain - 2_500_000.0) * 0.22
            tot -= (fee + tax)
            v_smh = tot * 0.70
            v_xlv = tot * 0.30
        nav_70_30_tilt[i] = v_smh + v_xlv

    # PW-RSI US-Only (with earnings filter proxy, after tax & FX)
    nav_pw_proxy_cash = simulate_pw_rsi(use_fwd_proxy=True, idle_mode="cash", apply_tax_and_fx=True)
    # PW-RSI US-Only (STRICT Point-in-Time WITHOUT any future earnings proxy, after tax & FX)
    nav_pw_pit_cash = simulate_pw_rsi(use_fwd_proxy=False, idle_mode="cash", apply_tax_and_fx=True)
    # PW-RSI US-Only (STRICT Point-in-Time, parking idle cash in SMH 70% + XLV 30%)
    nav_pw_pit_smhxlv = simulate_pw_rsi(use_fwd_proxy=False, idle_mode="smh_xlv", apply_tax_and_fx=True)
    # Core-Satellite: 70% in [SMH 70% + XLV 30%] + 30% in [PW-RSI Point-in-Time]
    nav_core_sat_pit = 0.70 * nav_70_30_rebal + 0.30 * nav_pw_pit_cash

    # Sub-period analysis helper
    periods = [
        ("2000~2026 (26.8년 전체: 닷컴버블+금융위기+AI장세)", "2000-01-03", "2026-10-29"),
        ("2000~2009 (10.0년: 닷컴버블 붕괴 & 리먼 금융위기)", "2000-01-03", "2009-12-31"),
        ("2010~2019 (10.0년: 모바일·클라우드 대세 상승장)", "2010-01-04", "2019-12-31"),
        ("2015~2026 (11.8년: 반도체·AI 슈퍼사이클)", "2015-01-02", "2026-10-29"),
        ("2020~2026 (6.8년: 코로나 이후~현재 AI 폭발기)", "2020-01-02", "2026-10-29"),
    ]

    strategies = {
        "SMH 70% + XLV 30% + 우측시동 비중확대 (90:10 틸트, 세후)": nav_70_30_tilt,
        "SMH 70% + XLV 30% (연간 리밸런싱, 세후)": nav_70_30_rebal,
        "SMH 70% + XLV 30% (단순 보유 Buy&Hold, 세후)": nav_70_30_bh,
        "SMH 100% 단독 보유 (세후)": nav_smh100,
        "XLV 100% 단독 보유 (세후)": nav_xlv100,
        "PW-RSI 알파 (이익검증 포함 백테스트, 대기=현금, 세후)": nav_pw_proxy_cash,
        "PW-RSI 알파 (100% 순수 가격/거래량만, 대기=현금, 세후)": nav_pw_pit_cash,
        "PW-RSI + SMH/XLV 결합 (신호 없을 때 SMH70+XLV30 보유, 순수 실전)": nav_pw_pit_smhxlv,
        "코어-위성 (70% SMH/XLV + 30% 순수 PW-RSI 알파)": nav_core_sat_pit,
    }

    report = {"periods": {}, "yearly": []}
    for p_label, s_dt, e_dt in periods:
        idx0 = int(np.searchsorted(sim_dates, pd.to_datetime(s_dt)))
        idx1 = min(len(sim_dates) - 1, int(np.searchsorted(sim_dates, pd.to_datetime(e_dt))))
        sub_dates = sim_dates[idx0 : idx1 + 1]
        report["periods"][p_label] = {}
        for s_name, nav in strategies.items():
            sub_nav = nav[idx0 : idx1 + 1]
            # Normalize to 100,000,000 at start of sub-period
            norm_nav = sub_nav / sub_nav[0] * 100_000_000.0
            report["periods"][p_label][s_name] = calc_stats(norm_nav, sub_dates)

    # Year-by-year returns comparison
    years = sorted(list(set(sim_dates.year)))
    for yr in years:
        mask = np.where(sim_dates.year == yr)[0]
        if len(mask) < 2:
            continue
        i0 = mask[0] - 1 if mask[0] > 0 else mask[0]
        i1 = mask[-1]
        row = {"year": int(yr)}
        for s_name, nav in strategies.items():
            ret = (nav[i1] / nav[i0] - 1.0) * 100.0
            row[s_name] = round(float(ret), 1)
        report["yearly"].append(row)

    with open("compare_smh_xlv_vs_alpha.json", "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)

    print("=== PERIOD COMPARISON SUMMARY ===")
    for p_label, s_dict in report["periods"].items():
        print(f"\n[{p_label}]")
        for s_name, st in s_dict.items():
            print(
                f"  - {s_name:52s}: 배수 {st['total_mult']:7.2f}x | 연복리(CAGR) {st['cagr_pct']:6.2f}% | MDD {st['mdd_pct']:6.2f}% | Sharpe {st['sharpe']:4.2f}"
            )


if __name__ == "__main__":
    run_comparison()
