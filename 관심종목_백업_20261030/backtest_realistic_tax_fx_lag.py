"""
2000~2026 (26.8년) 초현실적(Ultra-Realistic) 백테스트 엔진:
1) 실제 원/달러 환율(USD/KRW, KRW=X) 일별 변동 완전 반영 (모든 자산을 '원화(KRW)' 기준으로 정산)
2) 한<->미 국가 간 스위칭 시 '3거래일(3-Day) 결제·환전·송금 대기 시차' 반영 (3일 뒤 종가로 진입, 그 사이 조건 이탈 시 패스)
3) 실전 거래비용 & 세금 완전 반영:
   - 한국 주식: 매수/매도 수수료+슬리피지(편도 0.165%) + 매도 시 증권거래세(0.20%)
   - 미국 주식: 매수/매도 수수료+슬리피지(편도 0.20%)
   - 환전 비용: 한<->미 통화 전환 시 편도 0.12% (환전 스프레드)
   - 미국 주식 양도소득세: 연간 실현 순이익(원화 환산, 미국 주식 내 손익통산 후)에서 기본공제 250만 원 차감 후 22% 과세 (매년 말 정산 차감)
   - 한국 주식 대주주 양도세 옵션: 종목당 보유액 10억 원 이상 시 국내 주식 실현이익에도 22% 과세 비교
4) 대안 전략 비교: [한·미 혼합 스위칭(3일 시차+환전 반복)] vs [미국 주식 전용(US-Only) 스위칭(달러 계좌 내 즉시 교체+손익통산 100%)]
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
    KR_NAMES,
    ALWAYS_TRAP_TICKERS,
    POST_2021_TRAPS,
    POST_2023_TRAPS,
)

HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}


def load_usdkrw_series(cal: pd.DatetimeIndex) -> pd.Series:
    """Fetches daily USD/KRW exchange rate (1998~2026) from Yahoo Finance with historical fallback."""
    fx_path = os.path.join("data", "USDKRW.csv")
    os.makedirs("data", exist_ok=True)
    if not os.path.exists(fx_path):
        try:
            p1 = int(datetime(1998, 1, 1).timestamp())
            p2 = int(datetime(2026, 10, 15).timestamp())
            url = f"https://query1.finance.yahoo.com/v8/finance/chart/KRW=X?period1={p1}&period2={p2}&interval=1d"
            r = requests.get(url, headers=HEADERS, verify=False, timeout=15)
            if r.status_code == 200:
                res = r.json()["chart"]["result"][0]
                ts = res["timestamp"]
                q = res["indicators"]["quote"][0]
                df = pd.DataFrame({
                    "Date": [datetime.fromtimestamp(t).strftime("%Y-%m-%d") for t in ts],
                    "Close": q["close"],
                }).dropna()
                df.to_csv(fx_path, index=False)
        except Exception as e:
            print("FX fetch warning:", e)

    # Historical annual/monthly anchor points for USD/KRW (1998~2003 before Yahoo KRW=X full coverage)
    hist_anchors = {
        "1998-06-01": 1390.0,
        "1999-01-04": 1188.0,
        "2000-01-03": 1128.0,
        "2000-12-29": 1265.0,
        "2001-06-29": 1300.0,
        "2001-12-31": 1313.0,
        "2002-06-28": 1201.0,
        "2002-12-31": 1186.0,
        "2003-06-30": 1193.0,
        "2003-12-31": 1192.0,
    }
    fx_s = pd.Series(index=cal, dtype=float)
    for dt_str, val in hist_anchors.items():
        idx = cal.searchsorted(pd.to_datetime(dt_str))
        if idx < len(cal):
            fx_s.iloc[idx] = val

    if os.path.exists(fx_path):
        df = pd.read_csv(fx_path)
        df["Date"] = pd.to_datetime(df["Date"])
        df.sort_values("Date", inplace=True)
        df.drop_duplicates("Date", inplace=True)
        df.set_index("Date", inplace=True)
        c = pd.to_numeric(df["Close"], errors="coerce")
        c = c[(c >= 850.0) & (c <= 2000.0)]
        c_re = c.reindex(cal)
        fx_s.update(c_re)

    fx_s = fx_s.interpolate(method="time").bfill().ffill()
    return fx_s


def run_realistic_simulation():
    cal, C, H, L, V, benchmarks = load_aligned_panel()
    fx_series = load_usdkrw_series(cal)
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

    def score_candidates_at_day(i: int, us_only: bool = False):
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

    def simulate_realistic(
        initial_krw=100_000_000.0,  # 1억 원 시작
        apply_taxes=True,
        apply_fx_and_lag=True,
        cross_border_lag_days=3,    # 한<->미 전환 시 3거래일 대기
        us_only=False,
        kr_major_shareholder_tax=False,
    ):
        """
        Tracks exact KRW portfolio value day-by-day.
        Also tracks current cash currency ('KRW' or 'USD').
        """
        nav_krw = np.zeros(n_days, dtype=np.float64)
        cur_krw = initial_krw
        cash_currency = "USD" if us_only else "KRW"
        if us_only and apply_fx_and_lag:
            # Initial one-time FX conversion fee from KRW to USD (0.12%)
            cur_krw *= (1.0 - 0.0012)

        held_j = None
        entry_date = None
        entry_price_local = 0.0
        entry_fx = 1.0
        entry_krw_principal = 0.0
        entry_score = 0.0
        peak_price_local = 0.0
        days_held = 0
        tp1_reached = False

        # Settlement cooldown when switching across borders (KR <-> US)
        cooldown_until_idx = -1
        pending_target_j = None

        # Annual Tax Tracking (in KRW)
        yr_us_realized_net_gain_krw = 0.0
        yr_kr_realized_net_gain_krw = 0.0
        total_tax_paid_krw = 0.0
        total_fee_fx_paid_krw = 0.0
        cross_border_switch_count = 0
        yearly_tax_log = {}
        trade_log = []

        # Fee parameters
        kr_buy_fee = 0.00165 if apply_fx_and_lag else 0.0015
        kr_sell_fee = (0.00165 + 0.0020) if apply_fx_and_lag else 0.0015  # includes 0.20% KR transaction tax
        us_buy_fee = 0.0020 if apply_fx_and_lag else 0.0015
        us_sell_fee = 0.0020 if apply_fx_and_lag else 0.0015
        fx_spread_oneway = 0.0012 if apply_fx_and_lag else 0.0

        for i in range(n_days):
            dt = sim_dates[i]
            dt_str = dt.strftime("%Y-%m-%d")
            fx_now = fx_arr[i] if apply_fx_and_lag else 1.0
            fx_prev = fx_arr[i - 1] if (i > 0 and apply_fx_and_lag) else fx_now

            # 1. If holding a position, mark-to-market in KRW (including daily FX change for US stocks!)
            if held_j is not None:
                is_kr = is_kr_arr[held_j]
                p_prev = c_arr[i - 1, held_j] if i > 0 else entry_price_local
                p_cur = c_arr[i, held_j]
                p_high = h_arr[i, held_j]

                if np.isnan(p_cur) or p_prev <= 0:
                    p_cur = p_prev
                else:
                    local_mult = p_cur / p_prev
                    if not is_kr and apply_fx_and_lag:
                        fx_mult = fx_now / fx_prev
                        cur_krw *= (local_mult * fx_mult)
                    else:
                        cur_krw *= local_mult

                days_held += 1
                peak_price_local = max(peak_price_local, p_cur if not np.isnan(p_high) else p_cur)
                cur_ret_local = (p_cur / entry_price_local - 1.0)
                if cur_ret_local >= 1.00:
                    tp1_reached = True

                exit_reason = None
                if not tp1_reached and cur_ret_local <= -0.09:
                    exit_reason = "손절(-9% 칼손절 방어)"
                elif not tp1_reached and days_held >= 55 and cur_ret_local < 0.08:
                    exit_reason = "55일 시간손절(데드머니 탈출)"
                elif tp1_reached and ((p_cur / peak_price_local - 1.0) <= -0.18 and p_cur < ma60_arr[i, held_j]):
                    exit_reason = "2배+(TP1) 달성 후 트레일링 익절"
                elif (not tp1_reached) and (peak_price_local / entry_price_local - 1.0 >= 0.40) and (p_cur < ma60_arr[i, held_j] * 0.97):
                    exit_reason = "중기 추세선(60일선) 이탈 익절"

                if exit_reason is not None:
                    sell_fee_rate = kr_sell_fee if is_kr else us_sell_fee
                    fee_krw = cur_krw * sell_fee_rate
                    cur_krw -= fee_krw
                    total_fee_fx_paid_krw += fee_krw

                    realized_pnl_krw = cur_krw - entry_krw_principal
                    if not is_kr:
                        yr_us_realized_net_gain_krw += realized_pnl_krw
                        cash_currency = "USD"
                    else:
                        if kr_major_shareholder_tax and entry_krw_principal >= 1_000_000_000.0:
                            yr_kr_realized_net_gain_krw += realized_pnl_krw
                        cash_currency = "KRW"

                    trade_log.append({
                        "entry_date": entry_date,
                        "exit_date": dt_str,
                        "ticker": tickers[held_j],
                        "name": KR_NAMES.get(tickers[held_j], tickers[held_j]),
                        "market": "KR" if is_kr else "US",
                        "entry_price": round(float(entry_price_local), 2),
                        "exit_price": round(float(p_cur), 2),
                        "entry_fx": round(float(entry_fx), 1),
                        "exit_fx": round(float(fx_now), 1),
                        "local_return_pct": round(float(cur_ret_local * 100.0), 2),
                        "krw_return_pct": round(float((cur_krw / entry_krw_principal - 1.0) * 100.0), 2),
                        "realized_pnl_man_krw": round(float(realized_pnl_krw / 10000.0), 1),
                        "days_held": days_held,
                        "exit_reason": exit_reason,
                    })
                    held_j = None
            else:
                # In cash (either waiting for signal or in 3-day cross-border settlement lag)
                if cash_currency == "USD" and apply_fx_and_lag:
                    # USD RP interest (~2.2% annualized) + daily FX fluctuation
                    cur_krw *= (1.0 + 0.022 / 252.0) * (fx_now / fx_prev)
                else:
                    cur_krw *= (1.0 + 0.022 / 252.0)

            # 2. Check if we are in a 3-day cross-border settlement lag
            if held_j is None and i < cooldown_until_idx:
                # Cannot buy yet! Waiting for T+3 settlement & FX wire
                pass
            else:
                # Weekly scan or immediate scan if in cash after cooldown
                is_weekly_scan = (i % 5 == 0) or (held_j is None)
                if is_weekly_scan:
                    best_j, best_score = score_candidates_at_day(i, us_only=us_only)

                    if held_j is None and best_j is not None:
                        target_is_kr = is_kr_arr[best_j]
                        target_currency = "KRW" if target_is_kr else "USD"

                        # If switching across borders (KRW <-> USD) and lag is enabled, must wait 3 trading days!
                        if apply_fx_and_lag and (cash_currency != target_currency) and (pending_target_j != best_j):
                            # Initiate FX conversion & 3-day wire/settlement
                            fx_cost = cur_krw * fx_spread_oneway
                            cur_krw -= fx_cost
                            total_fee_fx_paid_krw += fx_cost
                            cash_currency = target_currency
                            cross_border_switch_count += 1
                            cooldown_until_idx = i + cross_border_lag_days
                            pending_target_j = best_j
                        else:
                            # Same currency (or 3-day lag just completed): execute buy immediately
                            pending_target_j = None
                            buy_fee_rate = kr_buy_fee if target_is_kr else us_buy_fee
                            fee_krw = cur_krw * buy_fee_rate
                            cur_krw -= fee_krw
                            total_fee_fx_paid_krw += fee_krw

                            held_j = best_j
                            entry_date = dt_str
                            entry_price_local = c_arr[i, held_j]
                            entry_fx = fx_now
                            entry_krw_principal = cur_krw
                            peak_price_local = entry_price_local
                            entry_score = best_score
                            days_held = 0
                            tp1_reached = False

                    elif held_j is not None and best_j is not None and best_j != held_j:
                        # Weekly Upgrade Switch check
                        p_cur = c_arr[i, held_j]
                        cur_ret_local = (p_cur / entry_price_local - 1.0)
                        if (days_held >= 25) and (cur_ret_local < 0.12) and (p_cur < ma20_arr[i, held_j]) and (best_score >= entry_score + 10.0):
                            is_kr = is_kr_arr[held_j]
                            sell_fee_rate = kr_sell_fee if is_kr else us_sell_fee
                            fee_krw = cur_krw * sell_fee_rate
                            cur_krw -= fee_krw
                            total_fee_fx_paid_krw += fee_krw

                            realized_pnl_krw = cur_krw - entry_krw_principal
                            if not is_kr:
                                yr_us_realized_net_gain_krw += realized_pnl_krw
                                cash_currency = "USD"
                            else:
                                if kr_major_shareholder_tax and entry_krw_principal >= 1_000_000_000.0:
                                    yr_kr_realized_net_gain_krw += realized_pnl_krw
                                cash_currency = "KRW"

                            trade_log.append({
                                "entry_date": entry_date,
                                "exit_date": dt_str,
                                "ticker": tickers[held_j],
                                "name": KR_NAMES.get(tickers[held_j], tickers[held_j]),
                                "market": "KR" if is_kr else "US",
                                "entry_price": round(float(entry_price_local), 2),
                                "exit_price": round(float(p_cur), 2),
                                "entry_fx": round(float(entry_fx), 1),
                                "exit_fx": round(float(fx_now), 1),
                                "local_return_pct": round(float(cur_ret_local * 100.0), 2),
                                "krw_return_pct": round(float((cur_krw / entry_krw_principal - 1.0) * 100.0), 2),
                                "realized_pnl_man_krw": round(float(realized_pnl_krw / 10000.0), 1),
                                "days_held": days_held,
                                "exit_reason": f"주간 상위종목 교체(->{KR_NAMES.get(tickers[best_j], tickers[best_j])})",
                            })
                            held_j = None

                            # Now check if the new target is same country or cross-border
                            target_is_kr = is_kr_arr[best_j]
                            target_currency = "KRW" if target_is_kr else "USD"
                            if apply_fx_and_lag and (cash_currency != target_currency):
                                fx_cost = cur_krw * fx_spread_oneway
                                cur_krw -= fx_cost
                                total_fee_fx_paid_krw += fx_cost
                                cash_currency = target_currency
                                cross_border_switch_count += 1
                                cooldown_until_idx = i + cross_border_lag_days
                                pending_target_j = best_j
                            else:
                                buy_fee_rate = kr_buy_fee if target_is_kr else us_buy_fee
                                fee_krw = cur_krw * buy_fee_rate
                                cur_krw -= fee_krw
                                total_fee_fx_paid_krw += fee_krw

                                held_j = best_j
                                entry_date = dt_str
                                entry_price_local = c_arr[i, held_j]
                                entry_fx = fx_now
                                entry_krw_principal = cur_krw
                                peak_price_local = entry_price_local
                                entry_score = best_score
                                days_held = 0
                                tp1_reached = False

            # 3. Year-End Tax Settlement (US 22% Capital Gains Tax after 2.5M KRW deduction)
            is_year_end = (i == n_days - 1) or (sim_dates[i + 1].year != dt.year)
            if is_year_end and apply_taxes:
                yr_tax = 0.0
                if yr_us_realized_net_gain_krw > 2_500_000.0:
                    yr_tax += (yr_us_realized_net_gain_krw - 2_500_000.0) * 0.22
                if kr_major_shareholder_tax and yr_kr_realized_net_gain_krw > 2_500_000.0:
                    yr_tax += (yr_kr_realized_net_gain_krw - 2_500_000.0) * 0.22

                if yr_tax > 0:
                    cur_krw -= yr_tax
                    # If currently holding a position, proportional reduction in principal
                    if held_j is not None:
                        entry_krw_principal *= (cur_krw / (cur_krw + yr_tax))
                    total_tax_paid_krw += yr_tax

                yearly_tax_log[dt.year] = {
                    "us_net_gain_man_krw": round(yr_us_realized_net_gain_krw / 10000.0, 1),
                    "tax_paid_man_krw": round(yr_tax / 10000.0, 1),
                }
                yr_us_realized_net_gain_krw = 0.0
                yr_kr_realized_net_gain_krw = 0.0

            nav_krw[i] = cur_krw

        return {
            "nav": pd.Series(nav_krw / initial_krw, index=sim_dates),
            "final_krw": float(nav_krw[-1]),
            "total_tax_paid_krw": float(total_tax_paid_krw),
            "total_fee_fx_paid_krw": float(total_fee_fx_paid_krw),
            "cross_border_switch_count": cross_border_switch_count,
            "yearly_tax_log": yearly_tax_log,
            "trade_log": trade_log,
        }

    # Run 4 comparison scenarios
    res_ideal = simulate_realistic(apply_taxes=False, apply_fx_and_lag=False, us_only=False)
    res_kr_us_real = simulate_realistic(apply_taxes=True, apply_fx_and_lag=True, cross_border_lag_days=3, us_only=False, kr_major_shareholder_tax=False)
    res_kr_us_majortax = simulate_realistic(apply_taxes=True, apply_fx_and_lag=True, cross_border_lag_days=3, us_only=False, kr_major_shareholder_tax=True)
    res_us_only_real = simulate_realistic(apply_taxes=True, apply_fx_and_lag=True, cross_border_lag_days=0, us_only=True, kr_major_shareholder_tax=False)

    # Also compute QQQ in KRW (with 22% exit tax at the end or Buy & Hold)
    qqq_usd = benchmarks["QQQ"].reindex(sim_dates).ffill()
    qqq_krw_mult = (qqq_usd / qqq_usd.iloc[0]).values * (fx_arr / fx_arr[0])
    qqq_krw_s = pd.Series(qqq_krw_mult, index=sim_dates)

    total_years = (sim_dates[-1] - sim_dates[0]).days / 365.25

    def summarize(res_dict, label):
        s = res_dict["nav"]
        final_mult = float(s.iloc[-1])
        cagr = (final_mult ** (1.0 / total_years) - 1.0) * 100.0
        peaks = np.maximum.accumulate(s.values)
        mdd = float(np.min((s.values - peaks) / peaks) * 100.0)
        return {
            "Strategy": label,
            "Final_Multiple": round(final_mult, 2),
            "Final_Asset_Eok_KRW": round(res_dict["final_krw"] / 1e8, 2),
            "CAGR_Pct": round(cagr, 2),
            "MDD_Pct": round(mdd, 2),
            "Total_Tax_Paid_Eok_KRW": round(res_dict["total_tax_paid_krw"] / 1e8, 2),
            "Total_Fee_FX_Paid_Eok_KRW": round(res_dict["total_fee_fx_paid_krw"] / 1e8, 2),
            "Cross_Border_Switches": res_dict["cross_border_switch_count"],
            "Total_Trades": len(res_dict["trade_log"]),
        }

    summary_table = [
        summarize(res_ideal, "1. 이론적 백테스트 (세금·환율·3일시차 미반영)"),
        summarize(res_kr_us_real, "2. [현실 반영] 한·미 혼합 스위칭 (3일시차 + 환율/환전비 + 미 양도세 22% + 국장 거래세)"),
        summarize(res_kr_us_majortax, "3. [현실 엄격] 한·미 혼합 + 10억 초과시 국내 대주주 양도세(22%)까지 부과"),
        summarize(res_us_only_real, "4. [실전 최적화] 미국 주식 전용(US-Only) 스위칭 (환전·3일시차 제거 + 손익통산 100% + 양도세 22%)"),
    ]

    # Yearly comparison table
    years = sorted(list(set(sim_dates.year)))
    yearly_comp = []
    for y in years:
        idx_y = np.where(sim_dates.year == y)[0]
        si, ei = idx_y[0], idx_y[-1]

        def yr_ret(s):
            b = s.iloc[si - 1] if si > 0 else 1.0
            return round(float((s.iloc[ei] / b - 1.0) * 100.0), 2)

        fx_start = fx_arr[si - 1] if si > 0 else fx_arr[0]
        fx_end = fx_arr[ei]
        fx_chg = round(float((fx_end / fx_start - 1.0) * 100.0), 2)

        tax_info_mix = res_kr_us_real["yearly_tax_log"].get(y, {"tax_paid_man_krw": 0.0})
        tax_info_us = res_us_only_real["yearly_tax_log"].get(y, {"tax_paid_man_krw": 0.0})

        yearly_comp.append({
            "Year": y,
            "USDKRW_End": round(float(fx_end), 0),
            "USDKRW_Chg_Pct": fx_chg,
            "Ideal_Ret_Pct": yr_ret(res_ideal["nav"]),
            "Real_KR_US_Mix_Ret_Pct": yr_ret(res_kr_us_real["nav"]),
            "Real_US_Only_Ret_Pct": yr_ret(res_us_only_real["nav"]),
            "QQQ_KRW_Ret_Pct": yr_ret(qqq_krw_s),
            "Mix_Nav_Eok": round(float(res_kr_us_real["nav"].iloc[ei]), 2),
            "US_Only_Nav_Eok": round(float(res_us_only_real["nav"].iloc[ei]), 2),
            "Mix_Tax_Paid_Man_KRW": tax_info_mix["tax_paid_man_krw"],
            "US_Only_Tax_Paid_Man_KRW": tax_info_us["tax_paid_man_krw"],
        })

    out = {
        "summary_table": summary_table,
        "yearly_comparison": yearly_comp,
        "kr_us_mix_trades": res_kr_us_real["trade_log"],
        "us_only_trades": res_us_only_real["trade_log"],
    }
    with open("pw_rsi_realistic_tax_fx_lag.json", "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=2)

    print("=== REALISTIC TAX + FX + 3-DAY LAG SUMMARY ===")
    print(pd.DataFrame(summary_table).to_string(index=False))
    print("\n=== YEARLY COMPARISON (2000~2026) ===")
    print(pd.DataFrame(yearly_comp).to_string(index=False))


if __name__ == "__main__":
    run_realistic_simulation()
