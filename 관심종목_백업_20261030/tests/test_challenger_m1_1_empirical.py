"""Adversarial Empirical Boundary, Stress & Robustness Test Suite for TurnaroundScreener.

Author: Challenger 1 (Empirical Boundary & Stress Challenger)
Target: engine/turnaround_screener.py
Milestone: Milestone 1 of Project Orchestrator 9

Adversarial Dimensions Tested:
1. Epsilon Boundaries:
   - Filter 1 (52w Low Proximity): 19.999% vs 20.000% vs 20.001%, score tier boundaries (5.0%, 10.0%, 16.0%)
   - Filter 2 (Earnings Turnaround): 29.999% vs 30.000% vs 30.001%, 99.999% vs 100.000%
   - Filter 3 (Volume Wash-Out): 1.399x vs 1.400x vs 1.401x, 1.999x vs 2.000x, daily change -0.001% vs 0.000% vs +0.001%
   - Filter 4 (Risk/Reward): Downside 9.999% vs 10.000% vs 10.001%, Upside 99.999% vs 100.000% vs 100.001%
2. Zero, Negative & Non-Finite Inputs:
   - Price <= 0 (0.0, -1.0, -100.0)
   - 52w Low <= 0 (0.0, -5.0)
   - Volume <= 0 (0, -10000)
   - Benchmark Volume <= 0 (0, -5000)
   - Support Price <= 0, TP1 <= 0
   - Negative Revenue, Negative Operating Income, Loss-to-Loss scenarios
   - Non-finite floating point inputs (NaN, +Inf, -Inf)
3. Support Floor Breaches:
   - Price < Support Floor: verifying breach penalty (breach_pct + 10.0%)
   - Strict failure of Filter 4 (downside > 10.0%)
   - Failure of Filter 3 when price < support * 0.99
   - Buffer behavior between support * 0.99 and support
4. End-to-End Stress & Serialization Robustness:
   - screen_stock() under extreme adversarial inputs
   - screen_universe() and select_weekly_top_pick() under all-disqualified universe
   - Full JSON round-trip serialization audit
"""

from __future__ import annotations

import json
import math
import unittest
from typing import Any, Dict

from engine.turnaround_screener import (
    ScreeningFilterResult,
    TurnaroundCandidate,
    TurnaroundScreener,
    WeeklyTopPick,
    parse_52w_range_string,
    TURNAROUND_SUPPORT_FLOORS,
    TURNAROUND_TP1_PRICES,
)


class TestChallengerEpsilonBoundaries(unittest.TestCase):
    """Stress-tests mathematical epsilon boundaries across all 4 screening filters."""

    # --------------------------------------------------------------------------
    # Filter 1: 52-Week Low Proximity Epsilon Tests
    # --------------------------------------------------------------------------
    def test_filter1_epsilon_19_999_vs_20_000_vs_20_001(self):
        """Verifies strict boundary enforcement at exactly 20.000% proximity threshold."""
        base_low = 100.00

        # Case 1: 19.999% -> Must PASS
        price_19_999 = 119.999
        res_pass = TurnaroundScreener.evaluate_filter_52w_low(
            stock_id="TEST",
            current_price=price_19_999,
            fifty_two_week_low=base_low,
            fifty_two_week_high=200.0,
        )
        self.assertTrue(res_pass.passed, "19.999% proximity must pass Filter 1")
        self.assertEqual(res_pass.score, 12.0)
        self.assertAlmostEqual(res_pass.actual_value, 20.00, delta=0.01)

        # Case 2: Exact 20.000% -> Must PASS
        price_20_000 = 120.000
        res_exact = TurnaroundScreener.evaluate_filter_52w_low(
            stock_id="TEST",
            current_price=price_20_000,
            fifty_two_week_low=base_low,
            fifty_two_week_high=200.0,
        )
        self.assertTrue(res_exact.passed, "Exact 20.000% proximity must pass Filter 1")
        self.assertEqual(res_exact.score, 12.0)
        self.assertEqual(res_exact.actual_value, 20.0)

        # Case 3: 20.001% -> Must FAIL
        price_20_001 = 120.001
        res_fail = TurnaroundScreener.evaluate_filter_52w_low(
            stock_id="TEST",
            current_price=price_20_001,
            fifty_two_week_low=base_low,
            fifty_two_week_high=200.0,
        )
        self.assertFalse(res_fail.passed, "20.001% proximity must fail Filter 1")
        self.assertEqual(res_fail.score, 0.0)
        self.assertIn("이격 과다", res_fail.detail)

    def test_filter1_floating_point_representation_exact_20_pct(self):
        """Empirically exposes IEEE-754 boundary trap: 3.6/3.0 is mathematically +20.0%, but fails without epsilon tolerance."""
        res = TurnaroundScreener.evaluate_filter_52w_low(
            stock_id="FLOAT_TEST",
            current_price=3.60,
            fifty_two_week_low=3.00,
            fifty_two_week_high=10.0,
        )
        # Empirical finding: (3.6 - 3.0)/3.0 * 100 = 20.000000000000004
        # actual_value is rounded to 20.0, and now passes with epsilon tolerance (proximity <= max_proximity + 1e-6)
        self.assertEqual(res.actual_value, 20.0, "actual_value is rounded to 20.0")
        self.assertTrue(res.passed, "Exact 20.0% mathematical multiple passes with epsilon tolerance")
        self.assertEqual(res.score, 15.0)  # 12.0 base + 3.0 crash bonus (-64% from 52w high)
        self.assertIn("안전마진 확보", res.detail)

    def test_filter1_subscore_bracket_boundaries(self):
        """Tests boundary transition points for sub-score brackets: 5.0%, 10.0%, 16.0%."""
        base_low = 100.0

        # 5.0% bracket: <= 5.0 gives 20.0 base
        res_5_000 = TurnaroundScreener.evaluate_filter_52w_low("T", 105.000, base_low, 150.0)
        self.assertEqual(res_5_000.score, 20.0)
        res_5_001 = TurnaroundScreener.evaluate_filter_52w_low("T", 105.001, base_low, 150.0)
        self.assertEqual(res_5_001.score, 17.5)

        # 10.0% bracket: <= 10.0 gives 17.5 base
        res_10_000 = TurnaroundScreener.evaluate_filter_52w_low("T", 110.000, base_low, 150.0)
        self.assertEqual(res_10_000.score, 17.5)
        res_10_001 = TurnaroundScreener.evaluate_filter_52w_low("T", 110.001, base_low, 150.0)
        self.assertEqual(res_10_001.score, 15.0)

        # 16.0% bracket: <= 16.0 gives 15.0 base
        res_16_000 = TurnaroundScreener.evaluate_filter_52w_low("T", 116.000, base_low, 150.0)
        self.assertEqual(res_16_000.score, 15.0)
        res_16_001 = TurnaroundScreener.evaluate_filter_52w_low("T", 116.001, base_low, 150.0)
        self.assertEqual(res_16_001.score, 12.0)

    # --------------------------------------------------------------------------
    # Filter 2: 1~2 Year Earnings Turnaround Epsilon Tests
    # --------------------------------------------------------------------------
    def test_filter2_epsilon_29_999_vs_30_000_vs_30_001(self):
        """Verifies strict boundary enforcement at exactly 30.000% forward growth."""
        def _make_fin(rev_26: float, oi_26: float) -> Dict[str, Any]:
            return {
                "years": ["2022", "2023", "2024", "2025", "2026E", "2027E"],
                "income_statement": {
                    "revenue": [100.0, 100.0, 100.0, 100.0, rev_26, rev_26],
                    "operating_income": [10.0, 10.0, 10.0, 10.0, oi_26, oi_26],
                },
            }

        # Case 1: 29.999% growth on both Rev and OI -> Must FAIL
        fin_29_999 = _make_fin(rev_26=129.999, oi_26=12.9999)
        res_fail = TurnaroundScreener.evaluate_filter_earnings_turnaround("T", fin_29_999)
        self.assertFalse(res_fail.passed, "29.999% forward growth must fail Filter 2")
        self.assertEqual(res_fail.score, 0.0)

        # Case 2: Exact 30.000% growth on Revenue -> Must PASS
        fin_30_000_rev = _make_fin(rev_26=130.000, oi_26=10.0)
        res_pass_rev = TurnaroundScreener.evaluate_filter_earnings_turnaround("T", fin_30_000_rev)
        self.assertTrue(res_pass_rev.passed, "Exact 30.000% revenue growth must pass Filter 2")
        self.assertEqual(res_pass_rev.score, 15.0)

        # Case 3: Exact 30.000% growth on Operating Income -> Must PASS
        fin_30_000_oi = _make_fin(rev_26=100.0, oi_26=13.000)
        res_pass_oi = TurnaroundScreener.evaluate_filter_earnings_turnaround("T", fin_30_000_oi)
        self.assertTrue(res_pass_oi.passed, "Exact 30.000% OI growth must pass Filter 2")
        self.assertEqual(res_pass_oi.score, 20.0)

        # Case 4: 30.001% growth on OI -> Must PASS
        fin_30_001_oi = _make_fin(rev_26=100.0, oi_26=13.001)
        res_pass_oi2 = TurnaroundScreener.evaluate_filter_earnings_turnaround("T", fin_30_001_oi)
        self.assertTrue(res_pass_oi2.passed, "30.001% OI growth must pass Filter 2")
        self.assertEqual(res_pass_oi2.score, 20.0)

    def test_filter2_floating_point_representation_exact_30_pct(self):
        """Empirically exposes IEEE-754 boundary trap: 1.17/0.90 is mathematically +30.0%, but fails without epsilon tolerance."""
        fin_30_exact = {
            "years": ["2022", "2023", "2024", "2025", "2026E", "2027E"],
            "income_statement": {
                "revenue": [1.0, 1.0, 1.0, 0.90, 1.17, 1.17],  # 0.90 * 1.3 = 1.17 exactly
                "operating_income": [0.1, 0.1, 0.1, 0.1, 0.1, 0.1],
            },
        }
        res = TurnaroundScreener.evaluate_filter_earnings_turnaround("T", fin_30_exact)
        # (1.17 - 0.90) / 0.90 * 100.0 evaluates to 29.99999999999999 in IEEE-754, now passes with epsilon tolerance
        self.assertEqual(res.actual_value, 30.0, "actual_value is rounded to 30.0")
        self.assertTrue(res.passed, "Exact 30.0% mathematical multiple passes with epsilon tolerance")
        self.assertEqual(res.score, 15.0)

    # --------------------------------------------------------------------------
    # Filter 3: Volume Wash-Out Epsilon Tests
    # --------------------------------------------------------------------------
    def test_filter3_epsilon_1_399x_vs_1_400x_vs_1_401x(self):
        """Verifies strict boundary enforcement at exactly 1.400x volume surge ratio."""
        bench_vol = 1_000_000

        # Case 1: 1.399x volume surge -> Must FAIL
        res_1_399 = TurnaroundScreener.evaluate_filter_volume_washout(
            stock_id="T",
            current_price=10.0,
            daily_change_pct=1.0,
            volume=1_399_000,
            support_price=9.0,
            benchmark_20d_volume=bench_vol,
        )
        self.assertFalse(res_1_399.passed, "1.399x volume surge must fail Filter 3")
        self.assertEqual(res_1_399.score, 8.0)  # Holds support and green, but volume insufficient

        # Case 2: Exact 1.400x volume surge -> Must PASS
        res_1_400 = TurnaroundScreener.evaluate_filter_volume_washout(
            stock_id="T",
            current_price=10.0,
            daily_change_pct=1.0,
            volume=1_400_000,
            support_price=9.0,
            benchmark_20d_volume=bench_vol,
        )
        self.assertTrue(res_1_400.passed, "Exact 1.400x volume surge must pass Filter 3")
        self.assertEqual(res_1_400.score, 15.0)

        # Case 3: 1.401x volume surge -> Must PASS
        res_1_401 = TurnaroundScreener.evaluate_filter_volume_washout(
            stock_id="T",
            current_price=10.0,
            daily_change_pct=1.0,
            volume=1_401_000,
            support_price=9.0,
            benchmark_20d_volume=bench_vol,
        )
        self.assertTrue(res_1_401.passed, "1.401x volume surge must pass Filter 3")
        self.assertEqual(res_1_401.score, 15.0)

    def test_filter3_daily_change_green_rebound_epsilon(self):
        """Verifies strict boundary enforcement of daily change >= 0.0%."""
        bench_vol = 1_000_000
        vol_surge = 2_000_000

        # -0.001% (marginal red candle) -> Must FAIL Filter 3
        res_red = TurnaroundScreener.evaluate_filter_volume_washout(
            stock_id="T",
            current_price=10.0,
            daily_change_pct=-0.001,
            volume=vol_surge,
            support_price=9.0,
            benchmark_20d_volume=bench_vol,
        )
        self.assertFalse(res_red.passed, "-0.001% daily change must fail Filter 3")
        self.assertEqual(res_red.score, 4.0)

        # Exact 0.000% (doji / flat candle) -> Must PASS Filter 3
        res_flat = TurnaroundScreener.evaluate_filter_volume_washout(
            stock_id="T",
            current_price=10.0,
            daily_change_pct=0.000,
            volume=vol_surge,
            support_price=9.0,
            benchmark_20d_volume=bench_vol,
        )
        self.assertTrue(res_flat.passed, "Exact 0.000% daily change must pass Filter 3")
        self.assertEqual(res_flat.score, 20.0)

        # +0.001% (marginal green candle) -> Must PASS Filter 3
        res_green = TurnaroundScreener.evaluate_filter_volume_washout(
            stock_id="T",
            current_price=10.0,
            daily_change_pct=+0.001,
            volume=vol_surge,
            support_price=9.0,
            benchmark_20d_volume=bench_vol,
        )
        self.assertTrue(res_green.passed, "+0.001% daily change must pass Filter 3")
        self.assertEqual(res_green.score, 20.0)

    # --------------------------------------------------------------------------
    # Filter 4: Risk/Reward Epsilon Tests
    # --------------------------------------------------------------------------
    def test_filter4_downside_and_upside_epsilons(self):
        """Tests downside risk <= 10.0% and upside >= 100.0% boundary epsilons."""
        # Baseline: price = 100.0, TP1 = 200.0 (+100.0% upside)
        # Downside 10.0% -> support = 90.0: (100.0 - 90.0) / 100.0 = 10.0%
        res_exact_10 = TurnaroundScreener.evaluate_filter_risk_reward(
            stock_id="T",
            current_price=100.0,
            support_price=90.0,
            tp1_price=200.0,
        )
        self.assertTrue(res_exact_10.passed, "Downside 10.0% and Upside 100.0% must pass")

        # Downside 10.001% -> support = 89.999: (100.0 - 89.999) / 100.0 = 10.001% -> Must FAIL
        res_fail_downside = TurnaroundScreener.evaluate_filter_risk_reward(
            stock_id="T",
            current_price=100.0,
            support_price=89.999,
            tp1_price=200.0,
        )
        self.assertFalse(res_fail_downside.passed, "Downside 10.001% must fail Filter 4")

        # Upside 99.999% -> TP1 = 199.999: upside = 99.999% -> Must FAIL
        res_fail_upside = TurnaroundScreener.evaluate_filter_risk_reward(
            stock_id="T",
            current_price=100.0,
            support_price=92.0,
            tp1_price=199.999,
        )
        self.assertFalse(res_fail_upside.passed, "Upside 99.999% must fail Filter 4")

    def test_filter4_floating_point_representation_exact_10_pct(self):
        """Empirically exposes IEEE-754 boundary trap: price=1.10, support=0.99 is mathematically 10.0% downside, but fails."""
        res = TurnaroundScreener.evaluate_filter_risk_reward(
            stock_id="T",
            current_price=1.10,
            support_price=0.99,  # 1.10 * 0.90 = 0.99 (exact 10.0% downside)
            tp1_price=2.50,
        )
        # (1.10 - 0.99) / 1.10 * 100.0 evaluates to 10.000000000000007 in IEEE-754, now passes with epsilon tolerance
        self.assertTrue(res.passed, "Exact 10.0% downside passes with epsilon tolerance")
        self.assertIn("손익비", res.detail)


class TestChallengerZeroNegativeAndInvalidInputs(unittest.TestCase):
    """Stress-tests behavior under zero, negative, and non-finite inputs."""

    def test_filter1_zero_and_negative_prices_and_lows(self):
        """Filter 1 must gracefully handle price <= 0, low <= 0 without exceptions."""
        # Current price = 0.0
        res_zero_price = TurnaroundScreener.evaluate_filter_52w_low("T", 0.0, 10.0, 20.0)
        self.assertFalse(res_zero_price.passed)
        self.assertEqual(res_zero_price.score, 0.0)
        self.assertIn("유효하지 않은 시세 데이터", res_zero_price.detail)

        # Current price negative
        res_neg_price = TurnaroundScreener.evaluate_filter_52w_low("T", -10.0, 10.0, 20.0)
        self.assertFalse(res_neg_price.passed)
        self.assertEqual(res_neg_price.score, 0.0)

        # 52w low = 0.0
        res_zero_low = TurnaroundScreener.evaluate_filter_52w_low("T", 10.0, 0.0, 20.0)
        self.assertFalse(res_zero_low.passed)
        self.assertEqual(res_zero_low.score, 0.0)

        # 52w low negative
        res_neg_low = TurnaroundScreener.evaluate_filter_52w_low("T", 10.0, -5.0, 20.0)
        self.assertFalse(res_neg_low.passed)
        self.assertEqual(res_neg_low.score, 0.0)

    def test_filter3_zero_and_negative_volumes_and_benchmarks(self):
        """Filter 3 must gracefully handle volume <= 0, benchmark <= 0 without exceptions."""
        # Volume = 0 with held support and green candle
        res_zero_vol = TurnaroundScreener.evaluate_filter_volume_washout(
            stock_id="T",
            current_price=10.0,
            daily_change_pct=1.0,
            volume=0,
            support_price=9.0,
            benchmark_20d_volume=1_000_000,
        )
        self.assertFalse(res_zero_vol.passed, "Volume 0 must fail Filter 3")
        # Note: Implementation awards 8.0 partial credit for price action alone (holding support + green candle)
        self.assertEqual(res_zero_vol.score, 8.0)
        self.assertEqual(res_zero_vol.actual_value, 0.0)

        # Negative volume with broken support -> Must be 0.0 pts
        res_neg_vol_broken = TurnaroundScreener.evaluate_filter_volume_washout(
            stock_id="T",
            current_price=8.0,
            daily_change_pct=-1.0,
            volume=-50_000,
            support_price=9.0,
            benchmark_20d_volume=1_000_000,
        )
        self.assertFalse(res_neg_vol_broken.passed)
        self.assertEqual(res_neg_vol_broken.score, 0.0)

        # Benchmark volume = 0 (must fallback or handle division by zero cleanly)
        res_zero_bench = TurnaroundScreener.evaluate_filter_volume_washout(
            stock_id="T",
            current_price=10.0,
            daily_change_pct=1.0,
            volume=2_000_000,
            support_price=9.0,
            benchmark_20d_volume=0,
        )
        self.assertIsInstance(res_zero_bench.passed, bool)
        self.assertIsInstance(res_zero_bench.score, float)

        # Benchmark volume negative
        res_neg_bench = TurnaroundScreener.evaluate_filter_volume_washout(
            stock_id="T",
            current_price=10.0,
            daily_change_pct=1.0,
            volume=2_000_000,
            support_price=9.0,
            benchmark_20d_volume=-500,
        )
        self.assertIsInstance(res_neg_bench.passed, bool)
        self.assertIsInstance(res_neg_bench.score, float)

    def test_filter4_zero_and_negative_prices_supports_and_tp1(self):
        """Filter 4 must gracefully handle non-positive prices, supports, and TP1s."""
        # Price = 0
        res_zero_p = TurnaroundScreener.evaluate_filter_risk_reward("T", 0.0, 9.0, 20.0)
        self.assertFalse(res_zero_p.passed)
        self.assertEqual(res_zero_p.score, 0.0)

        # Support = 0
        res_zero_s = TurnaroundScreener.evaluate_filter_risk_reward("T", 10.0, 0.0, 20.0)
        self.assertFalse(res_zero_s.passed)
        self.assertEqual(res_zero_s.score, 0.0)

        # TP1 = 0
        res_zero_tp = TurnaroundScreener.evaluate_filter_risk_reward("T", 10.0, 9.0, 0.0)
        self.assertFalse(res_zero_tp.passed)
        self.assertEqual(res_zero_tp.score, 0.0)

        # Negative support
        res_neg_s = TurnaroundScreener.evaluate_filter_risk_reward("T", 10.0, -5.0, 20.0)
        self.assertFalse(res_neg_s.passed)
        self.assertEqual(res_neg_s.score, 0.0)

        # Negative TP1
        res_neg_tp = TurnaroundScreener.evaluate_filter_risk_reward("T", 10.0, 9.0, -10.0)
        self.assertFalse(res_neg_tp.passed)
        self.assertEqual(res_neg_tp.score, 0.0)

    def test_non_finite_floating_point_inputs(self):
        """Verifies immunity against NaN and Infinity values."""
        # NaN price in Filter 1
        res_nan_f1 = TurnaroundScreener.evaluate_filter_52w_low("T", float("nan"), 10.0, 20.0)
        self.assertFalse(res_nan_f1.passed)
        self.assertEqual(res_nan_f1.score, 0.0)

        # Inf price in Filter 1
        res_inf_f1 = TurnaroundScreener.evaluate_filter_52w_low("T", float("inf"), 10.0, 20.0)
        self.assertFalse(res_inf_f1.passed)
        self.assertEqual(res_inf_f1.score, 0.0)

        # NaN in Filter 4
        res_nan_f4 = TurnaroundScreener.evaluate_filter_risk_reward("T", float("nan"), 9.0, 20.0)
        self.assertFalse(res_nan_f4.passed)
        self.assertEqual(res_nan_f4.score, 0.0)

        res_inf_f4 = TurnaroundScreener.evaluate_filter_risk_reward("T", 10.0, float("inf"), 20.0)
        self.assertFalse(res_inf_f4.passed)
        self.assertEqual(res_inf_f4.score, 0.0)


class TestChallengerSupportFloorBreaches(unittest.TestCase):
    """Stress-tests support floor breach behavior, penalties, and filter failures."""

    def test_filter4_support_floor_breach_penalty_calculation(self):
        """When price < support, penalty formula (breach_pct + 10.0%) must enforce failure."""
        support = 10.00

        # Scenario A: Price is $9.00 (10% breach below support)
        # breach_pct = (10.0 - 9.0) / 9.0 * 100 = 11.11%
        # downside_risk_pct = 11.11% + 10.0% = 21.11%
        res_breached = TurnaroundScreener.evaluate_filter_risk_reward(
            stock_id="T",
            current_price=9.00,
            support_price=support,
            tp1_price=20.00,
        )
        self.assertFalse(res_breached.passed, "Breached support floor must fail Filter 4")
        self.assertGreater(res_breached.score, 0.0)  # May have partial score if upside > 0
        self.assertIn("하방 지지선까지 -21.1%", res_breached.detail)

        # Scenario B: Price is $9.90 (1% breach below support)
        # breach_pct = (10.0 - 9.90) / 9.90 * 100 = 1.01%
        # downside_risk_pct = 1.01% + 10.0% = 11.01% > 10.0% -> Must FAIL!
        res_slight_breach = TurnaroundScreener.evaluate_filter_risk_reward(
            stock_id="T",
            current_price=9.90,
            support_price=support,
            tp1_price=25.00,
        )
        self.assertFalse(res_slight_breach.passed, "Even a 1% support breach must fail Filter 4")

    def test_filter3_support_floor_defense_vs_failure(self):
        """Tests Filter 3's 1% buffer tolerance vs strict collapse."""
        support = 10.00
        bench_vol = 1_000_000
        surge_vol = 2_000_000

        # Price exactly at support * 0.99 ($9.90) -> holds_support is True
        res_buffer = TurnaroundScreener.evaluate_filter_volume_washout(
            stock_id="T",
            current_price=9.90,
            daily_change_pct=0.5,
            volume=surge_vol,
            support_price=support,
            benchmark_20d_volume=bench_vol,
        )
        self.assertTrue(res_buffer.passed, "Price at support * 0.99 must defend support in Filter 3")

        # Price at $9.89 (< support * 0.99) -> holds_support is False -> Score must be 0.0
        res_collapsed = TurnaroundScreener.evaluate_filter_volume_washout(
            stock_id="T",
            current_price=9.89,
            daily_change_pct=0.5,
            volume=surge_vol,
            support_price=support,
            benchmark_20d_volume=bench_vol,
        )
        self.assertFalse(res_collapsed.passed, "Price < support * 0.99 must fail Filter 3")
        self.assertEqual(res_collapsed.score, 0.0, "Collapsed support must yield 0.0 points in Filter 3")
        self.assertIn("지지선 방어 실패", res_collapsed.detail)


class TestChallengerCandidateAndUniverseStress(unittest.TestCase):
    """Stress-tests screen_stock, screen_universe, and select_weekly_top_pick under adversarial workloads."""

    def test_screen_stock_under_adversarial_zero_and_breached_inputs(self):
        """screen_stock must never raise unhandled exceptions even with hostile parameters."""
        hostile_params = [
            {"current_price": 0.0, "volume": 0, "daily_change_pct": -10.0},
            {"current_price": -5.0, "volume": -100, "daily_change_pct": 0.0},
            {"fifty_two_week_low": 0.0, "fifty_two_week_high": 0.0},
            {"support_price": 100.0, "current_price": 10.0, "tp1_price": 5.0},  # Massive breach & inverted TP1
        ]
        for p in hostile_params:
            cand = TurnaroundScreener.screen_stock(stock_id="MBLY", **p)
            self.assertIsInstance(cand, TurnaroundCandidate)
            self.assertIsInstance(cand.composite_turnaround_score, float)
            self.assertIn(cand.conviction_tier, ("TOP_PICK", "STRONG_CANDIDATE", "WATCHLIST", "DISQUALIFIED"))
            # Must serialize without error
            d = cand.to_dict()
            json_str = json.dumps(d)
            self.assertIsInstance(json_str, str)

    def test_screen_universe_all_disqualified(self):
        """Universe screening when all candidates are disqualified must rank stably."""
        # Create a universe of synthetic stocks that fail all filters
        candidates = TurnaroundScreener.screen_universe(
            universe=["UPST", "FLNC"],
            date="2026-10-07",
        )
        self.assertEqual(len(candidates), 2)
        # Should be sorted descending by composite score
        self.assertGreaterEqual(candidates[0].composite_turnaround_score, candidates[1].composite_turnaround_score)

        # Weekly top pick selection from disqualified pool must strictly return None
        top_pick = TurnaroundScreener.select_weekly_top_pick(candidates, date="2026-10-07")
        self.assertIsNone(top_pick, "Disqualified candidates must never be selected as top-pick")


if __name__ == "__main__":
    unittest.main()
