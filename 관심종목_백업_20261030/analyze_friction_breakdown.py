"""
Step-by-step Friction Waterfall Analysis (2000~2026) on the 84 PW-RSI Trades
+ Comparison with US-Only Dynamic Switching (Zero Cross-Border Lag, 100% Tax Loss Harvesting)
"""

import json
import sys
import numpy as np
import pandas as pd

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

from backtest_pw_rsi_2000_2026 import load_aligned_panel
from backtest_realistic_tax_fx_lag import load_usdkrw_series


def run_waterfall():
    cal, C, H, L, V, benchmarks = load_aligned_panel()
    fx_s = load_usdkrw_series(cal)

    with open("pw_rsi_2000_2026_backtest.json", "r", encoding="utf-8") as f:
        base_data = json.load(f)

    trades = base_data["trade_log"]
    print(f"Loaded {len(trades)} base trades from 2000-2026.")

    # Analyze each trade with:
    # Step 1: Base Return (0.15% one-way tx cost, no FX, no 3-day lag, no 22% tax)
    # Step 2: + USD/KRW Exchange Rate effect (KRW-denominated return)
    # Step 3: + Realistic Brokerage/Slippage + KR 0.20% Transaction Tax + FX Spread (0.12% one-way on cross-border switches)
    # Step 4: + 3-Day Cross-Border Settlement Lag (buying 3 trading days later at actual Close[t+3] whenever switching KR <-> US)
    # Step 5: + Annual 22% US Capital Gains Tax (after 2.5M KRW deduction, US-to-US loss offsetting only)

    cap_step1 = 100_000_000.0  # 1억 원
    cap_step2 = 100_000_000.0
    cap_step3 = 100_000_000.0
    cap_step4 = 100_000_000.0
    cap_step5 = 100_000_000.0

    prev_market = "KR"  # Start with KRW in Korea
    cross_border_count = 0
    lag_3d_slippage_list = []

    # Group by exit year for annual tax calculation in Step 5
    yr_us_pnl_step5 = {}
    yr_taxes_paid_step5 = {}
    total_tax_step5 = 0.0
    total_fees_step4 = 0.0

    yearly_waterfall = {y: {} for y in range(2000, 2027)}
    cur_yr = 2000

    trade_details = []

    for idx, t in enumerate(trades):
        tkr = t["ticker"]
        is_kr = tkr.endswith(".KS") or tkr.endswith(".KQ")
        cur_market = "KR" if is_kr else "US"
        is_cross_border = (cur_market != prev_market)
        if is_cross_border:
            cross_border_count += 1

        ed = pd.to_datetime(t["entry_date"])
        xd = pd.to_datetime(t["exit_date"])
        e_idx = int(cal.searchsorted(ed))
        x_idx = int(cal.searchsorted(xd))

        # Before processing trade if exit_year advanced, settle taxes for finished years
        exit_yr = xd.year
        while cur_yr < exit_yr:
            # Settle tax for cur_yr
            us_net = yr_us_pnl_step5.get(cur_yr, 0.0)
            tax_yr = max(0.0, (us_net - 2_500_000.0) * 0.22) if us_net > 2_500_000.0 else 0.0
            cap_step5 -= tax_yr
            total_tax_step5 += tax_yr
            yr_taxes_paid_step5[cur_yr] = tax_yr
            yearly_waterfall[cur_yr] = {
                "step1_eok": round(cap_step1 / 1e8, 2),
                "step2_fx_eok": round(cap_step2 / 1e8, 2),
                "step3_fee_eok": round(cap_step3 / 1e8, 2),
                "step4_lag3d_eok": round(cap_step4 / 1e8, 2),
                "step5_aftertax_eok": round(cap_step5 / 1e8, 2),
                "tax_paid_man": round(tax_yr / 1e4, 1),
            }
            cur_yr += 1

        p_entry_orig = float(C[tkr].iloc[e_idx])
        p_exit_orig = float(C[tkr].iloc[x_idx])
        fx_entry_orig = float(fx_s.iloc[e_idx])
        fx_exit_orig = float(fx_s.iloc[x_idx])

        # If cross-border switch, entry is delayed by 3 trading days!
        if is_cross_border:
            e_idx_lag = min(x_idx - 1, e_idx + 3) if x_idx > e_idx + 1 else e_idx
            p_entry_lag = float(C[tkr].iloc[e_idx_lag])
            fx_entry_lag = float(fx_s.iloc[e_idx_lag])
            lag_slip_pct = (p_entry_lag / p_entry_orig - 1.0) * 100.0
            lag_3d_slippage_list.append(lag_slip_pct)
        else:
            e_idx_lag = e_idx
            p_entry_lag = p_entry_orig
            fx_entry_lag = fx_entry_orig
            lag_slip_pct = 0.0

        # Step 1: Base local return (with 0.15% one-way fee)
        r_local = p_exit_orig / p_entry_orig
        cap_step1 *= r_local * (1.0 - 0.0030)

        # Step 2: + FX effect (if US stock, multiply by fx_exit / fx_entry)
        fx_mult_orig = (fx_exit_orig / fx_entry_orig) if not is_kr else 1.0
        cap_step2 *= r_local * fx_mult_orig * (1.0 - 0.0030)

        # Step 3: + Realistic Fees (KR: 0.165%*2 + 0.20% tax = 0.53%, US: 0.20%*2 = 0.40%, + 0.12% FX spread if cross-border)
        fee_roundtrip = 0.0053 if is_kr else 0.0040
        fx_spread = 0.0012 if is_cross_border else 0.0
        cap_step3 *= r_local * fx_mult_orig * (1.0 - fee_roundtrip - fx_spread)

        # Step 4: + 3-Day Cross-Border Settlement Lag (buying at p_entry_lag and fx_entry_lag)
        r_local_lag = p_exit_orig / p_entry_lag
        fx_mult_lag = (fx_exit_orig / fx_entry_lag) if not is_kr else 1.0
        net_mult_step4 = r_local_lag * fx_mult_lag * (1.0 - fee_roundtrip - fx_spread)
        cap_step4 *= net_mult_step4

        # Step 5: Same as Step 4 + Annual 22% US Capital Gains Tax
        before_trade_step5 = cap_step5
        fee_cost_krw = before_trade_step5 * (fee_roundtrip + fx_spread)
        total_fees_step4 += fee_cost_krw
        cap_step5 *= net_mult_step4
        pnl_step5 = cap_step5 - before_trade_step5
        if not is_kr:
            yr_us_pnl_step5[exit_yr] = yr_us_pnl_step5.get(exit_yr, 0.0) + pnl_step5

        trade_details.append({
            "idx": idx + 1,
            "entry_date": t["entry_date"],
            "lagged_entry_date": cal[e_idx_lag].strftime("%Y-%m-%d"),
            "exit_date": t["exit_date"],
            "name": t["name"],
            "market": cur_market,
            "cross_border": is_cross_border,
            "orig_ret_pct": round((r_local - 1.0) * 100.0, 2),
            "lag3d_entry_diff_pct": round(lag_slip_pct, 2),
            "fx_entry": round(fx_entry_lag, 1),
            "fx_exit": round(fx_exit_orig, 1),
            "net_krw_ret_pct": round((net_mult_step4 - 1.0) * 100.0, 2),
            "pnl_step5_man_krw": round(pnl_step5 / 1e4, 1),
        })

        prev_market = cur_market

    # Settle remaining years up to 2026
    while cur_yr <= 2026:
        us_net = yr_us_pnl_step5.get(cur_yr, 0.0)
        tax_yr = max(0.0, (us_net - 2_500_000.0) * 0.22) if us_net > 2_500_000.0 else 0.0
        cap_step5 -= tax_yr
        total_tax_step5 += tax_yr
        yr_taxes_paid_step5[cur_yr] = tax_yr
        yearly_waterfall[cur_yr] = {
            "step1_eok": round(cap_step1 / 1e8, 2),
            "step2_fx_eok": round(cap_step2 / 1e8, 2),
            "step3_fee_eok": round(cap_step3 / 1e8, 2),
            "step4_lag3d_eok": round(cap_step4 / 1e8, 2),
            "step5_aftertax_eok": round(cap_step5 / 1e8, 2),
            "tax_paid_man": round(tax_yr / 1e4, 1),
        }
        cur_yr += 1

    # Add standby RP interest factor from base simulation (~1.16x over 26.8 years of cash days)
    rp_factor = base_data["overall_summary"][0]["Final_Multiple"] / (cap_step1 / 1e8)
    for k in yearly_waterfall:
        for col in ["step1_eok", "step2_fx_eok", "step3_fee_eok", "step4_lag3d_eok", "step5_aftertax_eok"]:
            yearly_waterfall[k][col] = round(yearly_waterfall[k][col] * rp_factor, 2)

    final_w = yearly_waterfall[2026]
    total_years = 26.78

    def cagr(mult):
        return round(((mult ** (1.0 / total_years)) - 1.0) * 100.0, 2)

    waterfall_summary = [
        {"Stage": "Step 1. 기본 백테스트 (수수료 0.15%, 세금·환율·3일시차 미적용)", "Final_Multiple": final_w["step1_eok"], "CAGR_Pct": cagr(final_w["step1_eok"])},
        {"Stage": "Step 2. + 원/달러 환율(USD/KRW) 실전 변동 반영 (원화 환산)", "Final_Multiple": final_w["step2_fx_eok"], "CAGR_Pct": cagr(final_w["step2_fx_eok"])},
        {"Stage": "Step 3. + 국내 증권거래세(0.20%)·해외수수료·환전스프레드(33회) 차감", "Final_Multiple": final_w["step3_fee_eok"], "CAGR_Pct": cagr(final_w["step3_fee_eok"])},
        {"Stage": "Step 4. + 한<->미 스위칭(33회) 시 '3거래일(T+3) 결제·환전 시차' 반영", "Final_Multiple": final_w["step4_lag3d_eok"], "CAGR_Pct": cagr(final_w["step4_lag3d_eok"])},
        {"Stage": "Step 5. + 미국 주식 양도소득세(22%, 연 250만 공제·손익통산) 매년 납부 후 최종 세후 자산", "Final_Multiple": final_w["step5_aftertax_eok"], "CAGR_Pct": cagr(final_w["step5_aftertax_eok"])},
    ]

    print("=== 5-STEP FRICTION WATERFALL ON THE 84 TRADES (1억 원 시작 기준) ===")
    print(pd.DataFrame(waterfall_summary).to_string(index=False))
    print(f"\nTotal Cross-Border Switches (KR <-> US): {cross_border_count} / {len(trades)} trades")
    print(f"Average 3-Day Lag Entry Price Penalty on Cross-Border Switches: {np.mean(lag_3d_slippage_list):+.2f}% (Max penalty: {np.max(lag_3d_slippage_list):+.2f}%)")
    print(f"Total US Capital Gains Tax Paid (2000~2026): {total_tax_step5 * rp_factor / 1e8:,.2f}억 원")

    with open("pw_rsi_waterfall_summary.json", "w", encoding="utf-8") as f:
        json.dump({
            "waterfall_summary": waterfall_summary,
            "cross_border_count": cross_border_count,
            "avg_3d_lag_penalty_pct": round(float(np.mean(lag_3d_slippage_list)), 2),
            "yearly_waterfall": yearly_waterfall,
            "trade_details": trade_details,
        }, f, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    run_waterfall()
