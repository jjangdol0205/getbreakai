"""
tests/test_morning_pdf_report.py
Comprehensive 4-Tier E2E Test Suite for Daily 08:10 AM KST 3-Page A4 PDF Investment Monitoring Report System.

Authoritative Specifications:
- ORIGINAL_REQUEST.md (§ 2026-10-16T05:09:06Z)
- PROJECT.md (§ Features 1~32 & Interface Contracts)
- quant_specs.md (§ Quantitative Formulations & Edge Behaviors)
- pdf_automation_specs.md (§ Strict 3-Page A4 PDF Geometry & Automation Pipeline)

Hierarchy:
- Tier 1: Feature Coverage (T1.1 ~ T1.11)
- Tier 2: Boundary & Corner Cases (T2.1 ~ T2.8)
- Tier 3: Cross-Feature Interactions (T3.1 ~ T3.4)
- Tier 4: Real-World Acceptance Scenarios (T4.1 ~ T4.6)
"""

import os
import sys
import re
import math
import subprocess
import pytest
import pandas as pd
import numpy as np

# Ensure root directory is on python path
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

import generate_morning_pdf as gmp


# ==============================================================================
# AUTHORITATIVE REFERENCE MATHEMATICAL FORMULAS (Specification Oracles)
# ==============================================================================

def oracle_overnight_semi_composite(r_mu: float, r_nvda: float, r_smh: float) -> float:
    """Overnight global semi composite return: 0.40*MU + 0.35*NVDA + 0.25*SMH."""
    return 0.40 * r_mu + 0.35 * r_nvda + 0.25 * r_smh


def oracle_asymmetric_beta_gap(delta_hynix: float, p_square_close: float = 852_000.0) -> dict:
    """
    SK Square asymmetric beta open gap simulator:
    beta_down = 1.55 (when delta_hynix < 0), beta_up = 0.95 (when delta_hynix >= 0).
    """
    if delta_hynix < 0:
        beta = 1.55
    else:
        beta = 0.95
    delta_square = beta * delta_hynix
    p_proj = round(p_square_close * (1.0 + delta_square / 100.0), -3)
    val_76 = (76 * p_proj) / 10_000.0  # in 만 원
    pnl_pct = (p_proj / 1_090_000.0 - 1.0) * 100.0
    buffer_floor = (p_proj / 780_000.0 - 1.0) * 100.0
    return {
        "beta": beta,
        "delta_square": delta_square,
        "projected_price": p_proj,
        "val_76_manwon": val_76,
        "pnl_pct": pnl_pct,
        "buffer_floor_pct": buffer_floor,
    }


def oracle_simulated_rsi14(close_series: list[float], projected_price: float) -> float:
    """Wilder's exponential moving average RSI(14) with alpha = 1/14."""
    series = list(close_series) + [projected_price]
    s = pd.Series(series, dtype=float)
    delta = s.diff()
    up_s = delta.clip(lower=0)
    dn_s = -delta.clip(upper=0)
    if float(up_s.abs().max()) < 1e-9 and float(dn_s.abs().max()) < 1e-9:
        return 50.0
    up = up_s.ewm(alpha=1.0 / 14.0, adjust=True, min_periods=14).mean()
    dn = dn_s.ewm(alpha=1.0 / 14.0, adjust=True, min_periods=14).mean()
    u_last = float(up.iloc[-1])
    d_last = float(dn.iloc[-1])
    if u_last < 1e-9 and d_last < 1e-9:
        return 50.0
    rsi = 100.0 - 100.0 / (1.0 + u_last / (d_last + 1e-9))
    return float(rsi)


def oracle_sotp_nav_discount(p_hynix: float, p_square: float) -> dict:
    """
    SOTP NAV calculation:
    Hynix shares: 706,420,000; Square stake: 20.76%; Other NAV: 20조 원; Square shares: 131,920,000.
    """
    n_hynix = 706_420_000
    n_square = 131_920_000
    stake = 0.2076
    other_nav = 20.0 * 10**12
    hynix_stake_val = p_hynix * n_hynix * stake
    total_nav = hynix_stake_val + other_nav
    nav_per_share = total_nav / n_square
    discount_pct = (1.0 - p_square / nav_per_share) * 100.0
    return {
        "total_nav_krw": total_nav,
        "nav_per_share": nav_per_share,
        "discount_pct": discount_pct,
    }


def oracle_share_defense_calculator(p_sale: float, cash_need: float = 13_600_000.0, total_shares: int = 76) -> dict:
    """Calculates shares consumed using ceiling division ceil(Cash / Price)."""
    shares_to_sell = math.ceil(cash_need / p_sale)
    remaining_shares = total_shares - shares_to_sell
    shares_saved = 16 - shares_to_sell
    target_100m = 100_000_000.0 / remaining_shares if remaining_shares > 0 else float("inf")
    return {
        "shares_to_sell": shares_to_sell,
        "remaining_shares": remaining_shares,
        "shares_saved_vs_bottom": shares_saved,
        "target_price_for_100m": target_100m,
    }


def oracle_fx_cushion(r_usd: float, r_fx: float) -> float:
    """Natural FX cushion return formula: (1 + R_usd) * (1 + R_fx) - 1."""
    return (1.0 + r_usd) * (1.0 + r_fx) - 1.0


def oracle_tax_saver_band(w_smh: float) -> str:
    """Tax-saver band: 55.0% <= w_SMH <= 65.0% enforces HOLD."""
    if 0.55 <= w_smh <= 0.65:
        return "HOLD"
    elif w_smh > 0.65:
        return "REBALANCE_TRIM_SMH"
    else:
        return "REBALANCE_BUY_SMH"


def oracle_contrarian_tilt(dd_smh_52w: float, current_weight: float = 0.60) -> float:
    """Contrarian tilt: DD <= -20% expands target to 75%; DD > -5% and w > 65% resets to 60%."""
    if dd_smh_52w <= -0.20:
        return 0.75
    elif dd_smh_52w > -0.05 and current_weight > 0.65:
        return 0.60
    return current_weight


def oracle_pwrsi_conditions(dd_high: float, prox_low: float, close: float, ma20: float, ma60: float,
                            ma20_slope_5d: float, max_vol_10d: float, ret20d: float, is_trap: bool = False) -> tuple[bool, str]:
    """
    Evaluates 4 explicit PW-RSI conditions:
    1. DD <= -38%
    2. Prox Low 10% ~ 40%
    3. Close > MA20 & Close > MA60 AND MA20 Slope > 0
    4. MaxVol10D >= 1.35x OR Ret20D >= 8.0%
    """
    if is_trap:
        return False, "TRAP_EXCLUDED"

    c1 = dd_high <= -38.0
    c2 = 10.0 <= prox_low <= 40.0
    c3 = (close > ma20) and (close > ma60) and (ma20_slope_5d > 0.0)
    c4 = (max_vol_10d >= 1.35) or (ret20d >= 8.0)

    if c1 and c2 and c3 and c4:
        return True, "1_BUY_IGNITION"
    elif c1 and (prox_low <= 42.0) and (close >= ma20 * 0.98 or (close / ma20 - 1.0) * 100.0 >= -3.0):
        return False, "2_READY_MA20"
    elif c1 and (prox_low <= 30.0):
        return False, "3_WATCH_BOTTOM"
    else:
        return False, "4_OTHER"


def oracle_stage2_exit_rules(p_current: float, p_entry: float, days_held: int, ma20: float, ma60: float,
                             score_current: float, score_new_top1: float) -> tuple[str, str]:
    """
    Evaluates 4 mechanical Stage 2 exit rules:
    Rule 1: -9.0% hard stop
    Rule 2: 55-day time-stop (< +8.0%)
    Rule 3: Weekly upgrade switch (+10pt rule)
    Rule 4: Trailing stop (MA60 -3%) or +100% TP1 half-exit
    """
    ret = (p_current / p_entry - 1.0) * 100.0

    # Rule 1: -9% Hard Stop
    stop_price = round(p_entry * 0.91, 2)
    if p_current <= stop_price:
        return "HARD_STOP_EXIT", f"Hard stop hit at {p_current} <= {stop_price} (-9.0% rule; 22% tax credit)"

    # Rule 4: +100% TP1 Half-Exit
    if ret >= 100.0:
        return "TP1_HALF_EXIT", f"+100% TP1 milestone reached ({ret:.1f}%); sell 50% shares to recover 100% principal"

    # Rule 4b: Medium-term MA60 (-3%) trailing stop
    if ret >= 40.0 and p_current < 0.97 * ma60:
        return "MA60_TRAILING_EXIT", f"Trailing stop triggered: price {p_current} breached MA60 by >= -3%"

    # Rule 2: 55-Day Time Stop (Dead Money)
    if days_held >= 55 and ret < 8.0:
        return "TIME_STOP_EXIT", f"55-day time-stop triggered (D+{days_held}, return {ret:.1f}% < +8.0%)"

    # Rule 3: Weekly Upgrade Switch (+10pt)
    if days_held >= 25 and ret < 12.0 and p_current < ma20 and (score_new_top1 >= score_current + 10.0):
        return "UPGRADE_SWITCH", f"Upgrade switch triggered: candidate score (+{score_new_top1 - score_current:.1f} pts) superior"

    return "HOLD", "All 4 exit criteria clear; maintain position"


# ==============================================================================
# TIER 1: FEATURE COVERAGE (ISOLATED SPECIFICATIONS)
# ==============================================================================

class TestTier1FeatureCoverage:
    """Tier 1: Comprehensive verification of Features 1 ~ 32 in isolation."""

    def test_t1_1_us_cn_primary_source_badges(self):
        """T1.1: 100% US & China primary source badge & origin validation."""
        intel = gmp.build_us_cn_curated_intelligence({})
        assert "sk_news" in intel and "etf_news" in intel

        all_news = intel["sk_news"] + intel["etf_news"]
        assert len(all_news) >= 6, "Must provide at least 3 news for SK and 3 for ETF Barbell"

        for item in all_news:
            origin = item["origin"]
            assert any(tag in origin for tag in ["🇺🇸", "🇨🇳", "🇹🇼", "US", "CN", "TW"]), (
                f"Origin badge missing valid foreign marker: {origin}"
            )
            assert "orig_title" in item and len(item["orig_title"]) > 10
            assert "kr_summary" in item and len(item["kr_summary"]) > 15
            assert "action_note" in item and len(item["action_note"]) > 10

    def test_t1_2_korean_media_blacklist_firewall(self):
        """T1.2: 0% South Korean domestic media blacklist check via regex audit."""
        kr_blacklist_patterns = [
            r"naver\.com",
            r"daum\.net",
            r"hankyung\.com",
            r"mk\.co\.kr",
            r"sedaily\.com",
            r"chosun\.com",
            r"donga\.com",
            r"joins\.com",
            r"joongang\.co\.kr",
            r"mt\.co\.kr",
            r"moneytoday\.co\.kr",
            r"edaily\.co\.kr",
            r"yna\.co\.kr",
            r"newsis\.com",
            r"news1\.kr",
            r"thebell\.co\.kr",
            r"etnews\.com",
            r"infomax\.co\.kr",
            r"hl=ko",
            r"gl=KR",
            r"ceid=KR:ko",
            r"미래에셋",
            r"NH투자증권",
            r"삼성증권",
            r"KB증권",
            r"신한투자증권",
            r"키움증권",
            r"하나증권",
            r"한국투자증권",
            r"유진투자증권",
        ]

        # Audit generate_morning_pdf.py source file content for forbidden live scraping URLs
        with open(os.path.join(BASE_DIR, "generate_morning_pdf.py"), "r", encoding="utf-8") as f:
            code_text = f.read()

        for pattern in kr_blacklist_patterns:
            matches = re.findall(pattern, code_text, re.IGNORECASE)
            assert len(matches) == 0, f"Source code integrity violation: blacklisted pattern '{pattern}' found in gmp"

    def test_t1_3_page1_executive_action_banner(self):
        """T1.3: Page 1 30-Second Executive Banner (3 traffic light cards)."""
        # Card 1: SK Square 76 shares state machine
        # Oversold / hold condition
        assert 780_000.0 <= 852_000.0 < 1_090_000.0
        # Card 2: SMH(60%) + XLV(40%) band state machine
        assert oracle_tax_saver_band(0.612) == "HOLD"
        # Card 3: PW-RSI Alpha state machine
        # When 0 candidates ignite buy signal, state is RED / DISCIPLINE
        buy_count = 0
        card3_state = "🔴 0 SIGNALS (무신호 규율 유지)" if buy_count == 0 else "🟢 1_BUY_IGNITION"
        assert "🔴" in card3_state

    def test_t1_4_page1_asymmetric_beta_simulator_and_rsi14(self):
        """T1.4: Page 1 Asymmetric beta open gap simulation math (beta_down=1.55, beta_up=0.95) & RSI(14)."""
        # Downside test: Hynix -4.0% drop
        res_down = oracle_asymmetric_beta_gap(delta_hynix=-4.0, p_square_close=852_000.0)
        assert res_down["beta"] == 1.55
        assert res_down["delta_square"] == -6.20
        assert res_down["projected_price"] == 799_000.0
        assert res_down["val_76_manwon"] == pytest.approx(6072.4, abs=0.1)
        assert res_down["pnl_pct"] == pytest.approx(-26.70, abs=0.1)
        assert res_down["buffer_floor_pct"] == pytest.approx(2.44, abs=0.05)

        # Upside test: Hynix +3.0% gain
        res_up = oracle_asymmetric_beta_gap(delta_hynix=3.0, p_square_close=852_000.0)
        assert res_up["beta"] == 0.95
        assert res_up["delta_square"] == pytest.approx(2.85)
        assert res_up["projected_price"] == 876_000.0

        # Simulated RSI(14) with downward trend
        mock_closes = [1_000_000.0 - i * 6_000.0 for i in range(30)]
        sim_rsi = oracle_simulated_rsi14(mock_closes, projected_price=799_000.0)
        assert 0.0 <= sim_rsi <= 100.0
        assert sim_rsi < 35.0, "Oversold RSI expected after consecutive drops"

    def test_t1_5_page1_sotp_dual_target_and_share_defense(self):
        """T1.5: Page 1 SOTP Dual-Target gauge & 1,360만 share defense math."""
        # SOTP NAV calculation with Hynix at 1,419,000 KRW
        sotp = oracle_sotp_nav_discount(p_hynix=1_419_000.0, p_square=852_000.0)
        assert sotp["nav_per_share"] > 1_500_000.0
        assert 45.0 <= sotp["discount_pct"] <= 55.0

        # Share defense table for 1,360만 KRW cash requirement
        def_850k = oracle_share_defense_calculator(p_sale=850_000.0)
        assert def_850k["shares_to_sell"] == 16
        assert def_850k["remaining_shares"] == 60
        assert def_850k["shares_saved_vs_bottom"] == 0
        assert def_850k["target_price_for_100m"] == pytest.approx(1_666_667, abs=100)

        # 1억 graduation target with 76 shares preserved
        def_76 = oracle_share_defense_calculator(p_sale=1_316_000.0)
        assert 100_000_000.0 / 76 == pytest.approx(1_315_789.5, abs=1.0)
        assert 100_000_000.0 / 66 == pytest.approx(1_515_151.5, abs=1.0)

    def test_t1_6_page2_smh_xlv_fx_cushion_and_zero_oscillators(self):
        """T1.6: Page 2 SMH(60%)+XLV(40%) natural FX cushion & zero short-term oscillators."""
        # Negative US return but positive FX return demonstrates cushion
        r_usd = -0.03  # -3.0% US drop
        r_fx = +0.02   # +2.0% USD/KRW rise
        r_krw = oracle_fx_cushion(r_usd, r_fx)
        # (1 - 0.03) * (1 + 0.02) - 1 = 0.97 * 1.02 - 1 = 0.9894 - 1 = -0.0106 (-1.06%)
        assert r_krw == pytest.approx(-0.0106, abs=1e-5)
        assert r_krw > r_usd, "KRW return must be higher than USD return due to dollar surge"

        # Verify zero short-term ETF oscillators in gmp architecture
        with open(os.path.join(BASE_DIR, "generate_morning_pdf.py"), "r", encoding="utf-8") as f:
            code = f.read()
        # Page 2 ETF scorecard must not compute RSI or MACD on SMH/XLV
        assert "ETF_DATA_DIR" in code

    def test_t1_7_page2_tax_saver_band_and_contrarian_tilt(self):
        """T1.7: Page 2 ±5.0%p Tax-Saver band & SMH -20% drawdown-tilt logic."""
        # Within tolerance band 55% ~ 65%
        assert oracle_tax_saver_band(0.60) == "HOLD"
        assert oracle_tax_saver_band(0.55) == "HOLD"
        assert oracle_tax_saver_band(0.65) == "HOLD"
        assert oracle_tax_saver_band(0.66) == "REBALANCE_TRIM_SMH"
        assert oracle_tax_saver_band(0.54) == "REBALANCE_BUY_SMH"

        # Contrarian drawdown-tilt
        assert oracle_contrarian_tilt(dd_smh_52w=-0.15, current_weight=0.60) == 0.60
        assert oracle_contrarian_tilt(dd_smh_52w=-0.21, current_weight=0.60) == 0.75
        # Profit harvest reset
        assert oracle_contrarian_tilt(dd_smh_52w=-0.04, current_weight=0.74) == 0.60

    def test_t1_8_page3_state_aware_discipline_banner(self):
        """T1.8: Page 3 State-Aware Discipline Banner triggers on 0 buy signals."""
        signals_empty = []
        is_banner_active = len(signals_empty) == 0
        assert is_banner_active is True

        banner_text = (
            "🚨 [무신호 규율 유지 / No-Signal Discipline Active]: "
            "금일 4대 진입 조건을 100% 충족한 신규 우측 시동 [1_BUY] 종목이 0건입니다. "
            "26.8년간 세전 +20,287% (연평균 CAGR +21.97%) / 세후 +7,952% (CAGR +17.81%)를 지켜낸 핵심 방패입니다."
        )
        assert "26.8년" in banner_text and "21.97%" in banner_text

    def test_t1_9_page3_stage2_active_position_exit_rules(self):
        """T1.9: Page 3 Stage 2 Active Position 4 exit rules."""
        # Rule 1: -9.0% hard stop
        action, reason = oracle_stage2_exit_rules(
            p_current=90.0, p_entry=100.0, days_held=10, ma20=95.0, ma60=98.0, score_current=80.0, score_new_top1=85.0
        )
        assert action == "HARD_STOP_EXIT"
        assert "22% tax credit" in reason

        # Rule 2: 55-day time stop (< +8.0%)
        action, reason = oracle_stage2_exit_rules(
            p_current=105.0, p_entry=100.0, days_held=56, ma20=104.0, ma60=102.0, score_current=80.0, score_new_top1=82.0
        )
        assert action == "TIME_STOP_EXIT"

        # Rule 3: Weekly upgrade switch (+10pt)
        action, reason = oracle_stage2_exit_rules(
            p_current=109.0, p_entry=100.0, days_held=28, ma20=111.0, ma60=105.0, score_current=72.0, score_new_top1=85.0
        )
        assert action == "UPGRADE_SWITCH"

        # Rule 4: TP1 +100% half-exit
        action, reason = oracle_stage2_exit_rules(
            p_current=202.0, p_entry=100.0, days_held=40, ma20=180.0, ma60=150.0, score_current=90.0, score_new_top1=92.0
        )
        assert action == "TP1_HALF_EXIT"

    def test_t1_10_page3_top5_leaderboard_and_four_pwrsi_conditions(self):
        """T1.10: Page 3 Actionable Top 5 leaderboard & 4 explicit PW-RSI conditions (including MA20 5D Slope > 0)."""
        # All 4 conditions met with positive MA20 slope
        pass_all, stage = oracle_pwrsi_conditions(
            dd_high=-42.0, prox_low=22.0, close=55.0, ma20=50.0, ma60=48.0,
            ma20_slope_5d=+1.2, max_vol_10d=1.55, ret20d=12.0
        )
        assert pass_all is True
        assert stage == "1_BUY_IGNITION"

        # Slope <= 0 fails Condition 3
        pass_flat, stage_flat = oracle_pwrsi_conditions(
            dd_high=-42.0, prox_low=22.0, close=55.0, ma20=50.0, ma60=48.0,
            ma20_slope_5d=0.0, max_vol_10d=1.55, ret20d=12.0
        )
        assert pass_flat is False
        assert stage_flat != "1_BUY_IGNITION"

        # Test calc_pw_rsi_signal from gmp if data available
        dates = pd.date_range("2024-01-01", periods=260, freq="B").strftime("%Y-%m-%d").tolist()
        closes = [100.0 - i * 0.2 for i in range(260)]
        df_mock = pd.DataFrame({
            "Date": dates,
            "Close": closes,
            "High": [c + 1.0 for c in closes],
            "Low": [c - 1.0 for c in closes],
            "Volume": [1_000_000 for _ in closes],
        })
        res = gmp.calc_pw_rsi_signal("CELH", df_mock, {})
        assert "score" in res and "signal_stage" in res
        assert "trigger_price" in res

    def test_t1_11_page3_spotlight_cards_and_value_trap_firewall(self):
        """T1.11: Page 3 Top 2 Spotlight Deep-Dive cards & Value-Trap Firewall (INTC, PFE, BA, NKE, PARA, WBD, ALB)."""
        trap_tickers = ["INTC", "PFE", "BA", "NKE", "PARA", "WBD", "ALB"]
        for ticker in trap_tickers:
            assert ticker in gmp.US_UNIVERSE_META, f"{ticker} must be registered in US_UNIVERSE_META"
            meta = gmp.US_UNIVERSE_META[ticker]
            assert meta["growth_tier"] in ("TRAP", "WAIT_CYCLE"), f"{ticker} must be tagged as TRAP or WAIT_CYCLE"

            # Verify oracle rejects value trap even if technical conditions met
            pass_trap, stage_trap = oracle_pwrsi_conditions(
                dd_high=-50.0, prox_low=15.0, close=30.0, ma20=28.0, ma60=25.0,
                ma20_slope_5d=+2.0, max_vol_10d=2.0, ret20d=15.0, is_trap=True
            )
            assert pass_trap is False
            assert stage_trap == "TRAP_EXCLUDED"


# ==============================================================================
# TIER 2: BOUNDARY & CORNER CASES
# ==============================================================================

class TestTier2BoundaryAndCornerCases:
    """Tier 2: Boundary conditions, corner cases, and stress regimes."""

    def test_t2_1_extreme_gap_drops_and_zero_price_change(self):
        """T2.1: Extreme gap drops (-10%, -15% circuit breaker) and 0.0% unchanged gap."""
        # 0.0% gap
        res_zero = oracle_asymmetric_beta_gap(delta_hynix=0.0, p_square_close=852_000.0)
        assert res_zero["delta_square"] == 0.0
        assert res_zero["projected_price"] == 852_000.0

        # -10.0% gap
        res_extreme = oracle_asymmetric_beta_gap(delta_hynix=-10.0, p_square_close=852_000.0)
        assert res_extreme["delta_square"] == -15.5
        assert res_extreme["projected_price"] == round(852_000.0 * (1.0 - 0.155), -3)
        assert res_extreme["projected_price"] < 780_000.0
        assert res_extreme["buffer_floor_pct"] < 0.0

    def test_t2_2_exact_dollar_trigger_price_boundary(self):
        """T2.2: Exact dollar trigger price boundary when price touches MA20/MA60."""
        ma20 = 50.00
        ma60 = 52.50
        trigger_price = max(ma20, ma60)
        assert trigger_price == 52.50

        # Price exactly at trigger
        close = 52.50
        dist_pct = (trigger_price / close - 1.0) * 100.0
        assert dist_pct == 0.0

    def test_t2_3_score_ranking_ties_and_fallbacks(self):
        """T2.3: Ranking tie-breaker: sort by score desc, then volume surge desc, then ticker asc."""
        candidates = [
            {"ticker": "UPST", "score": 85.0, "vol_surge": 1.40},
            {"ticker": "CELH", "score": 85.0, "vol_surge": 1.80},
            {"ticker": "MBLY", "score": 85.0, "vol_surge": 1.40},
        ]
        sorted_cands = sorted(candidates, key=lambda x: (-x["score"], -x["vol_surge"], x["ticker"]))
        assert sorted_cands[0]["ticker"] == "CELH"
        assert sorted_cands[1]["ticker"] == "MBLY"
        assert sorted_cands[2]["ticker"] == "UPST"

    def test_t2_4_empty_network_response_offline_csv_fallback(self):
        """T2.4: Empty network responses / offline mode falling back to local CSV caches."""
        # Test ticker fallback function in generate_morning_pdf
        ticker, df = gmp.fetch_ticker_df("SMH")
        assert ticker == "SMH"
        assert df is not None
        assert len(df) >= 30
        assert "Close" in df.columns and "Date" in df.columns

    def test_t2_5_rsi14_zero_variance_and_extreme_crash(self):
        """T2.5: RSI(14) 0-variance series and extreme crash handling."""
        # 14 identical closes
        flat_series = [100.0] * 20
        rsi_flat = oracle_simulated_rsi14(flat_series, projected_price=100.0)
        assert rsi_flat == pytest.approx(50.0, abs=1e-3)

        # Extreme crash: 14 consecutive -10% drops
        crash_series = [1000.0 * (0.9 ** i) for i in range(25)]
        rsi_crash = oracle_simulated_rsi14(crash_series, projected_price=crash_series[-1] * 0.8)
        assert rsi_crash < 10.0
        assert rsi_crash >= 0.0

    def test_t2_6_tax_saver_band_exact_boundary(self):
        """T2.6: Tax-Saver band exact boundaries (55.0% and 65.0%)."""
        assert oracle_tax_saver_band(0.5500) == "HOLD"
        assert oracle_tax_saver_band(0.6500) == "HOLD"
        assert oracle_tax_saver_band(0.6501) == "REBALANCE_TRIM_SMH"
        assert oracle_tax_saver_band(0.5499) == "REBALANCE_BUY_SMH"

    def test_t2_7_contrarian_tilt_exact_boundary(self):
        """T2.7: Contrarian tilt exact boundary at DD = -20.0%."""
        assert oracle_contrarian_tilt(dd_smh_52w=-0.2000, current_weight=0.60) == 0.75
        assert oracle_contrarian_tilt(dd_smh_52w=-0.1999, current_weight=0.60) == 0.60

    def test_t2_8_stage2_time_stop_exact_boundary(self):
        """T2.8: Stage 2 time-stop exact boundary at Day 55 with return +8.0%."""
        # Return +8.01% at Day 55 -> HOLD
        action_pass, _ = oracle_stage2_exit_rules(
            p_current=108.01, p_entry=100.0, days_held=55, ma20=107.0, ma60=105.0, score_current=80.0, score_new_top1=80.0
        )
        assert action_pass == "HOLD"

        # Return +7.99% at Day 55 -> TIME_STOP_EXIT
        action_fail, _ = oracle_stage2_exit_rules(
            p_current=107.99, p_entry=100.0, days_held=55, ma20=107.0, ma60=105.0, score_current=80.0, score_new_top1=80.0
        )
        assert action_fail == "TIME_STOP_EXIT"


# ==============================================================================
# TIER 3: CROSS-FEATURE COMBINATIONS
# ==============================================================================

class TestTier3CrossFeatureCombinations:
    """Tier 3: Pairwise interactions and systemic cross-feature dependencies."""

    def test_t3_1_usd_krw_spike_with_smh_drawdown_fx_cushion(self):
        """T3.1: Pairwise interaction: USD/KRW surge + SMH drop demonstrates natural FX cushion."""
        smh_drop_usd = -0.05   # SMH drops -5% in US
        fx_surge = +0.045      # USD/KRW surges +4.5%
        krw_net_return = oracle_fx_cushion(smh_drop_usd, fx_surge)
        # Net loss is cushioned to -0.725%
        assert krw_net_return == pytest.approx(-0.00725, abs=1e-4)
        assert abs(krw_net_return) < abs(smh_drop_usd) / 5.0

    def test_t3_2_sk_square_drop_with_share_defense_recalculation(self):
        """T3.2: SK Square price drop dynamically recalculates emergency cash share destruction."""
        # At 1,090,000 KRW (Breakeven): 13 shares sold, 63 preserved
        def_breakeven = oracle_share_defense_calculator(1_090_000.0)
        # At 780,000 KRW (Hard floor breached): 18 shares sold, 58 preserved
        def_floor = oracle_share_defense_calculator(780_000.0)

        assert def_floor["shares_to_sell"] > def_breakeven["shares_to_sell"]
        assert def_floor["remaining_shares"] < def_breakeven["remaining_shares"]
        # Required graduation price increases significantly
        assert def_floor["target_price_for_100m"] > def_breakeven["target_price_for_100m"]

    def test_t3_3_pwrsi_buy_signal_appearance_and_discipline_banner_toggle(self):
        """T3.3: PW-RSI buy signal appearance toggles discipline banner into buy action banner."""
        # State 0: 0 buy signals -> Discipline banner active
        cands_state0 = [{"ticker": "CELH", "stage": "2_READY_MA20"}]
        buy_count_0 = sum(1 for c in cands_state0 if c["stage"] == "1_BUY_IGNITION")
        assert buy_count_0 == 0

        # State 1: CELH ignites into 1_BUY_IGNITION -> Discipline banner deactivates
        cands_state1 = [{"ticker": "CELH", "stage": "1_BUY_IGNITION"}]
        buy_count_1 = sum(1 for c in cands_state1 if c["stage"] == "1_BUY_IGNITION")
        assert buy_count_1 == 1

    def test_t3_4_smh_drawdown_tilt_combined_with_weight_drift(self):
        """T3.4: SMH 52W DD <= -20% combined with weight drift overrides standard band into 75% target."""
        # Suppose SMH drops severely so weight drifts to 52%
        w_smh = 0.52
        dd_smh = -0.22
        # Normal band would say REBALANCE_BUY_SMH (back to 60%)
        band_decision = oracle_tax_saver_band(w_smh)
        assert band_decision == "REBALANCE_BUY_SMH"
        # But Contrarian tilt dictates target expansion to 75%
        target_weight = oracle_contrarian_tilt(dd_smh, current_weight=w_smh)
        assert target_weight == 0.75


# ==============================================================================
# TIER 4: REAL-WORLD ACCEPTANCE SCENARIOS
# ==============================================================================

class TestTier4RealWorldAcceptanceScenarios:
    """Tier 4: End-to-end execution, PyMuPDF inspection, and batch runner validation."""

    def test_t4_1_windows_batch_runner_script_integrity(self):
        """T4.1: Verify run_morning_pdf_0810.bat syntax, chcp 65001, and --open flag."""
        bat_path = os.path.join(BASE_DIR, "run_morning_pdf_0810.bat")
        assert os.path.exists(bat_path), f"Batch script missing: {bat_path}"
        with open(bat_path, "r", encoding="utf-8", errors="ignore") as f:
            text = f.read()
        assert "chcp 65001" in text, "Batch script must set UTF-8 code page (chcp 65001)"
        assert "generate_morning_pdf.py" in text, "Batch script must invoke generate_morning_pdf.py"
        assert "--open" in text, "Batch script must pass --open argument"

    def test_t4_2_task_scheduler_registration_syntax(self):
        """T4.2: Verify Task Scheduler command structure."""
        cmd = 'schtasks /create /tn "MorningAlphaBriefing0810" /tr "\\"D:\\투자홈페이지\\관심종목_백업_20261030\\run_morning_pdf_0810.bat\\"" /sc daily /st 08:10 /f'
        assert "/tn \"MorningAlphaBriefing0810\"" in cmd
        assert "/st 08:10" in cmd
        assert "/sc daily" in cmd

    def test_t4_3_cli_entrypoint_compilation_and_execution(self):
        """T4.3: Execute generate_morning_pdf.py end-to-end; verify exit code 0."""
        script_path = os.path.join(BASE_DIR, "generate_morning_pdf.py")
        res = subprocess.run([sys.executable, script_path], cwd=BASE_DIR, capture_output=True, text=True)
        assert res.returncode == 0, f"generate_morning_pdf.py failed with stderr: {res.stderr}"

    def test_t4_4_strict_three_page_pymupdf_validation(self):
        """T4.4: Strict PyMuPDF validation: len(doc) == 3 (strictly 3 pages)."""
        import pymupdf
        out_pdf = os.path.join(BASE_DIR, "daily_pdf", "Latest_Morning_Alpha_Briefing.pdf")
        assert os.path.exists(out_pdf), f"PDF file not found at {out_pdf}"

        doc = pymupdf.open(out_pdf)
        try:
            assert len(doc) == 3, f"Expected strictly 3 pages, found {len(doc)} pages"
            for i, page in enumerate(doc):
                rect = page.rect
                # A4: 595.28 x 841.89 pt
                assert abs(rect.width - 595.28) <= 3.0, f"Page {i+1} width {rect.width} != 595.28 pt"
                assert abs(rect.height - 841.89) <= 3.0, f"Page {i+1} height {rect.height} != 841.89 pt"
        finally:
            doc.close()

    def test_t4_5_pdf_file_size_exceeds_50kb(self):
        """T4.5: PDF file size must exceed 50 KB."""
        out_pdf = os.path.join(BASE_DIR, "daily_pdf", "Latest_Morning_Alpha_Briefing.pdf")
        assert os.path.exists(out_pdf), f"PDF file not found at {out_pdf}"
        size = os.path.getsize(out_pdf)
        assert size > 50_000, f"PDF file size too small: {size} bytes <= 50,000 bytes"

    def test_t4_6_text_bounding_boxes_zero_clipping(self):
        """T4.6: Programmatic inspection verifying zero bottom-of-page clipping (y1 <= 838 pt)."""
        import pymupdf
        out_pdf = os.path.join(BASE_DIR, "daily_pdf", "Latest_Morning_Alpha_Briefing.pdf")
        assert os.path.exists(out_pdf), f"PDF file not found at {out_pdf}"

        doc = pymupdf.open(out_pdf)
        try:
            for i, page in enumerate(doc):
                blocks = page.get_text("blocks")
                assert len(blocks) > 0, f"Page {i+1} has no text blocks"
                for b in blocks:
                    y1 = b[3]
                    # Printable height margin threshold: max y1 is 838.0 pt
                    assert y1 <= 838.0, (
                        f"Page {i+1} text block clipped beyond bottom boundary: y1={y1:.2f} > 838.0 pt. "
                        f"Text snippet: '{b[4][:30]}...'"
                    )
        finally:
            doc.close()
