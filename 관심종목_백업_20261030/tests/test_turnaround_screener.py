"""Comprehensive Unit Test Suite for US Market 52-Week Low Turnaround Screener Engine.

Tests:
1. Filter 1 (52-Week Low Proximity & Deep-Crash Safety Margin)
   - Happy path, crash elasticity bonuses, boundary conditions (19.9% vs 20.0% vs 20.1%)
   - Edge cases: 0 price, 0 low, negative values, division-by-zero protection, support floor holding
2. Filter 2 (1~2 Year Forward Earnings Turnaround Visibility)
   - Loss-to-profit swing (is_turnaround_to_profit, 30 pts max conviction)
   - Multi-year revenue and operating income growth, sequential acceleration
   - Boundary conditions (29.9% vs 30.0% vs 30.1%)
   - Edge cases: missing financials, missing arrays, zero base revenue/OI
3. Filter 3 (Volume Wash-Out Capitulation & Support Defense)
   - Volume surge ratio >= 1.40x, support defense (support * 0.99), green rebound candle (>= 0.0%)
   - Boundary conditions: 1.39x vs 1.40x, -0.01% vs 0.00%, support * 0.99 vs 0.989
   - Edge cases: 0 volume, 0 benchmark, missing support
4. Filter 4 (Asymmetric Risk/Reward Ratio)
   - Downside <= 10.0%, TP1 Upside >= 100.0%, RRR >= 10.0x
   - Boundary conditions: 9.9% vs 10.0% vs 10.1%, 99.9% vs 100.0% vs 100.1%
   - Edge cases: price <= 0, support <= 0, tp1 <= 0, price below support penalty
5. Composite Scoring & Institutional Conviction Tiers
   - Pillars summing to 0~100 points
   - Conviction tier thresholds: TOP_PICK (>=88), STRONG_CANDIDATE (75~87), WATCHLIST (55~74), DISQUALIFIED (<55)
6. Empirical Real Watchlist Equity Verification
   - MBLY: Top candidate, TOP_PICK (90.0 pts) with confirmed wash-out, passes all 4 filters
   - CELH: Strong candidate, STRONG_CANDIDATE (76~80 pts), qualifies
   - UPST (+91% from 52w low): Disqualified (<55 pts)
   - FLNC (+33% from 52w low): Disqualified (<55 pts)
7. Universe Screening & Weekly Top-Pick Selection
   - screen_universe ranking order
   - select_weekly_top_pick selects #1 top pick with rich deep-dive metadata
8. Schema Validation, Immutability & JSON Serialization
   - to_dict() compliance, json.dumps round-trip, zero external dependencies
"""

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


class TestFilter1Proximity52wLow(unittest.TestCase):
    """Test suite for Filter 1: 52-Week Low Proximity Safety Margin."""

    def test_happy_path_deep_bottom_proximity(self):
        """Current price within 5% of 52w low earns 20 base pts + 5 crash bonus = 25 pts."""
        res = TurnaroundScreener.evaluate_filter_52w_low(
            stock_id="MBLY",
            current_price=6.60,
            fifty_two_week_low=6.47,
            fifty_two_week_high=34.50,
        )
        self.assertTrue(res.passed)
        self.assertEqual(res.score, 25.0)
        self.assertAlmostEqual(res.actual_value, 2.01, places=1)
        self.assertIn("52주 신저가 안전마진 확보", res.detail)

    def test_happy_path_moderate_proximity_bracket(self):
        """Current price between 5% and 10% from low earns 17.5 base pts."""
        res = TurnaroundScreener.evaluate_filter_52w_low(
            stock_id="TEST",
            current_price=10.80,
            fifty_two_week_low=10.00,
            fifty_two_week_high=20.00,  # -46% crash (no bonus)
        )
        self.assertTrue(res.passed)
        self.assertEqual(res.score, 17.5)
        self.assertEqual(res.actual_value, 8.0)

    def test_happy_path_fifteen_percent_bracket(self):
        """Current price between 10% and 16% from low earns 15 base pts."""
        res = TurnaroundScreener.evaluate_filter_52w_low(
            stock_id="TEST",
            current_price=11.50,
            fifty_two_week_low=10.00,
            fifty_two_week_high=20.00,
        )
        self.assertTrue(res.passed)
        self.assertEqual(res.score, 15.0)
        self.assertEqual(res.actual_value, 15.0)

    def test_epsilon_boundary_19_9_vs_20_0_vs_20_1(self):
        """Strict boundary check at 20.0%: 19.9% passes, 20.0% passes, 20.1% fails."""
        # 19.9% proximity -> passes
        res_19_9 = TurnaroundScreener.evaluate_filter_52w_low(
            stock_id="TEST",
            current_price=119.90,
            fifty_two_week_low=100.00,
            fifty_two_week_high=200.00,
        )
        self.assertTrue(res_19_9.passed)
        self.assertEqual(res_19_9.score, 12.0)

        # Exact 20.0% proximity -> passes
        res_20_0 = TurnaroundScreener.evaluate_filter_52w_low(
            stock_id="TEST",
            current_price=120.00,
            fifty_two_week_low=100.00,
            fifty_two_week_high=200.00,
        )
        self.assertTrue(res_20_0.passed)
        self.assertEqual(res_20_0.score, 12.0)

        # 20.1% proximity -> fails
        res_20_1 = TurnaroundScreener.evaluate_filter_52w_low(
            stock_id="TEST",
            current_price=120.10,
            fifty_two_week_low=100.00,
            fifty_two_week_high=200.00,
        )
        self.assertFalse(res_20_1.passed)
        self.assertEqual(res_20_1.score, 0.0)
        self.assertIn("이격 과다", res_20_1.detail)

    def test_crash_elasticity_bonus_tiers(self):
        """Validates crash bonuses: >=70% drop (+5 pts), >=50% drop (+3 pts), <50% drop (+0 pts)."""
        # >= 70% drop: price 10.0 vs high 40.0 (-75%)
        res_75 = TurnaroundScreener.evaluate_filter_52w_low(
            stock_id="T1",
            current_price=10.0,
            fifty_two_week_low=10.0,
            fifty_two_week_high=40.0,
        )
        self.assertEqual(res_75.score, 25.0)  # 20 base + 5 bonus = 25

        # >= 50% drop: price 10.0 vs high 22.0 (-54.5%)
        res_55 = TurnaroundScreener.evaluate_filter_52w_low(
            stock_id="T2",
            current_price=10.0,
            fifty_two_week_low=10.0,
            fifty_two_week_high=22.0,
        )
        self.assertEqual(res_55.score, 23.0)  # 20 base + 3 bonus = 23

        # < 50% drop: price 10.0 vs high 18.0 (-44.4%)
        res_44 = TurnaroundScreener.evaluate_filter_52w_low(
            stock_id="T3",
            current_price=10.0,
            fifty_two_week_low=10.0,
            fifty_two_week_high=18.0,
        )
        self.assertEqual(res_44.score, 20.0)  # 20 base + 0 bonus = 20

    def test_edge_case_zero_price_and_zero_low_safety(self):
        """Zero price or zero low must not raise ZeroDivisionError and safely fail."""
        res_zero_price = TurnaroundScreener.evaluate_filter_52w_low(
            stock_id="T_ZERO_P",
            current_price=0.0,
            fifty_two_week_low=10.0,
        )
        self.assertFalse(res_zero_price.passed)
        self.assertEqual(res_zero_price.score, 0.0)

        res_zero_low = TurnaroundScreener.evaluate_filter_52w_low(
            stock_id="T_ZERO_L",
            current_price=10.0,
            fifty_two_week_low=0.0,
        )
        self.assertFalse(res_zero_low.passed)
        self.assertEqual(res_zero_low.score, 0.0)

    def test_edge_case_negative_and_nan_prices(self):
        """Negative and NaN values safely rejected."""
        res_neg = TurnaroundScreener.evaluate_filter_52w_low(
            stock_id="T_NEG",
            current_price=-5.0,
            fifty_two_week_low=10.0,
        )
        self.assertFalse(res_neg.passed)
        self.assertEqual(res_neg.score, 0.0)

        res_nan = TurnaroundScreener.evaluate_filter_52w_low(
            stock_id="T_NAN",
            current_price=float("nan"),
            fifty_two_week_low=10.0,
        )
        self.assertFalse(res_nan.passed)
        self.assertEqual(res_nan.score, 0.0)

    def test_edge_case_price_below_52w_low_holds_support(self):
        """Intraday tick slightly below 52w low (>=95% low) holds bottom floor."""
        res_held = TurnaroundScreener.evaluate_filter_52w_low(
            stock_id="T_TICK_LOW",
            current_price=9.80,
            fifty_two_week_low=10.00,
            fifty_two_week_high=50.00,
        )
        self.assertTrue(res_held.passed)
        self.assertEqual(res_held.actual_value, 0.0)
        self.assertEqual(res_held.score, 25.0)  # clamped to 0.0% proximity

        # Below 95% threshold fails
        res_collapsed = TurnaroundScreener.evaluate_filter_52w_low(
            stock_id="T_COLLAPSED",
            current_price=9.20,
            fifty_two_week_low=10.00,
            fifty_two_week_high=50.00,
        )
        self.assertFalse(res_collapsed.passed)
        self.assertEqual(res_collapsed.score, 0.0)


class TestFilter2EarningsTurnaround(unittest.TestCase):
    """Test suite for Filter 2: 1~2 Year Forward Earnings Turnaround Visibility."""

    def test_happy_path_loss_to_profit_swing(self):
        """Operating loss swinging to operating profit achieves max 30.0 points."""
        fin = {
            "years": ["2022", "2023", "2024", "2025", "2026E", "2027E"],
            "income_statement": {
                "revenue": [1.0, 1.2, 1.5, 1.8, 2.1, 2.5],
                "operating_income": [-0.5, -0.3, -0.8, -0.39, 0.12, 0.45],
            },
        }
        res = TurnaroundScreener.evaluate_filter_earnings_turnaround(
            stock_id="MBLY",
            financials=fin,
        )
        self.assertTrue(res.passed)
        self.assertEqual(res.score, 30.0)
        self.assertEqual(res.actual_value, "흑자전환")
        self.assertIn("구조적 흑자 전환", res.detail)

    def test_happy_path_massive_operating_income_growth_100pct(self):
        """Operating income growth >= 100% achieves 25 base pts (+5 rev bonus if rev >= 50%)."""
        fin = {
            "years": ["2022", "2023", "2024", "2025", "2026E", "2027E"],
            "income_statement": {
                "revenue": [1.0, 1.0, 1.0, 2.0, 3.2, 3.8],  # +90% 2y growth
                "operating_income": [0.1, 0.1, 0.1, 0.14, 0.38, 0.50],  # +257% 2y growth
            },
        }
        res = TurnaroundScreener.evaluate_filter_earnings_turnaround(
            stock_id="CELH",
            financials=fin,
        )
        self.assertTrue(res.passed)
        self.assertEqual(res.score, 30.0)  # 25 base + 5 rev bonus = 30
        self.assertAlmostEqual(float(res.actual_value), 257.14, places=1)

    def test_happy_path_moderate_oi_growth_30_to_100pct(self):
        """Operating income growth between 30% and 100% achieves 20 pts."""
        fin = {
            "years": ["2022", "2023", "2024", "2025", "2026E", "2027E"],
            "income_statement": {
                "revenue": [1.0, 1.0, 1.0, 1.0, 1.2, 1.3],
                "operating_income": [0.1, 0.1, 0.1, 1.0, 1.45, 1.5],  # +45% in 2026E, +50% in 2027E
            },
        }
        res = TurnaroundScreener.evaluate_filter_earnings_turnaround(
            stock_id="TEST",
            financials=fin,
        )
        self.assertTrue(res.passed)
        self.assertEqual(res.score, 20.0)
        self.assertAlmostEqual(float(res.actual_value), 50.0, places=1)

    def test_happy_path_revenue_growth_only_qualification(self):
        """Revenue growth >= 30% qualifies with 15 pts even if OI growth is flat."""
        fin = {
            "years": ["2022", "2023", "2024", "2025", "2026E", "2027E"],
            "income_statement": {
                "revenue": [1.0, 1.0, 1.0, 1.0, 1.2, 1.40],  # +40%
                "operating_income": [0.1, 0.1, 0.1, 1.0, 1.05, 1.10],  # +10%
            },
        }
        res = TurnaroundScreener.evaluate_filter_earnings_turnaround(
            stock_id="REV_ONLY",
            financials=fin,
        )
        self.assertTrue(res.passed)
        self.assertEqual(res.score, 15.0)
        self.assertAlmostEqual(float(res.actual_value), 40.0, places=1)

    def test_epsilon_boundary_29_9_vs_30_0_vs_30_1(self):
        """Epsilon boundary check at 30.0% growth threshold."""
        # 29.9% growth fails
        fin_29_9 = {
            "years": ["2022", "2023", "2024", "2025", "2026E", "2027E"],
            "income_statement": {
                "revenue": [1.0, 1.0, 1.0, 100.0, 110.0, 120.0],
                "operating_income": [1.0, 1.0, 1.0, 100.0, 120.0, 129.9],  # +29.9%
            },
        }
        res_29_9 = TurnaroundScreener.evaluate_filter_earnings_turnaround("T", fin_29_9)
        self.assertFalse(res_29_9.passed)
        self.assertEqual(res_29_9.score, 0.0)

        # 30.0% growth passes
        fin_30_0 = {
            "years": ["2022", "2023", "2024", "2025", "2026E", "2027E"],
            "income_statement": {
                "revenue": [1.0, 1.0, 1.0, 100.0, 110.0, 120.0],
                "operating_income": [1.0, 1.0, 1.0, 100.0, 120.0, 130.0],  # +30.0%
            },
        }
        res_30_0 = TurnaroundScreener.evaluate_filter_earnings_turnaround("T", fin_30_0)
        self.assertTrue(res_30_0.passed)
        self.assertEqual(res_30_0.score, 20.0)

        # 30.1% growth passes
        fin_30_1 = {
            "years": ["2022", "2023", "2024", "2025", "2026E", "2027E"],
            "income_statement": {
                "revenue": [1.0, 1.0, 1.0, 100.0, 110.0, 120.0],
                "operating_income": [1.0, 1.0, 1.0, 100.0, 120.0, 130.1],  # +30.1%
            },
        }
        res_30_1 = TurnaroundScreener.evaluate_filter_earnings_turnaround("T", fin_30_1)
        self.assertTrue(res_30_1.passed)
        self.assertEqual(res_30_1.score, 20.0)

    def test_edge_cases_empty_financials_and_zero_division(self):
        """Empty or corrupt financials handled safely with zero division protection."""
        res_empty = TurnaroundScreener.evaluate_filter_earnings_turnaround("UNKNOWN", {})
        self.assertFalse(res_empty.passed)
        self.assertEqual(res_empty.score, 0.0)

        # Base revenue == 0 handled safely
        fin_zero_rev = {
            "years": ["2025", "2026E", "2027E"],
            "income_statement": {
                "revenue": [0.0, 10.0, 20.0],
                "operating_income": [0.0, -5.0, -10.0],
            },
        }
        res_zero = TurnaroundScreener.evaluate_filter_earnings_turnaround("T_ZERO", fin_zero_rev)
        self.assertFalse(res_zero.passed)
        self.assertEqual(res_zero.score, 0.0)


class TestFilter3VolumeWashout(unittest.TestCase):
    """Test suite for Filter 3: Volume Wash-Out Capitulation Spike & Support Defense."""

    def test_happy_path_volume_surge_and_green_candle_rebound(self):
        """Volume surge >= 2.0x, support floor defended, green candle scores max 20 pts."""
        res = TurnaroundScreener.evaluate_filter_volume_washout(
            stock_id="MBLY",
            current_price=7.10,
            daily_change_pct=1.5,
            volume=8600000,
            support_price=6.87,
            benchmark_20d_volume=4260000,  # 8.6M / 4.26M = 2.018x
        )
        self.assertTrue(res.passed)
        self.assertEqual(res.score, 20.0)
        self.assertAlmostEqual(res.actual_value, 2.02, places=1)
        self.assertIn("대량 거래량 폭증", res.detail)

    def test_happy_path_moderate_volume_surge_1_4_to_2_0(self):
        """Volume surge between 1.4x and 2.0x scores 15 pts."""
        res = TurnaroundScreener.evaluate_filter_volume_washout(
            stock_id="MBLY",
            current_price=7.10,
            daily_change_pct=0.57,
            volume=7008063,
            support_price=6.87,
            benchmark_20d_volume=4260000,  # 7.008M / 4.26M = 1.645x
        )
        self.assertTrue(res.passed)
        self.assertEqual(res.score, 15.0)
        self.assertAlmostEqual(res.actual_value, 1.65, places=1)

    def test_epsilon_boundary_surge_ratio_1_39_vs_1_40_vs_1_41(self):
        """Volume surge boundary at 1.40x: 1.39x fails, 1.40x passes, 1.41x passes."""
        # 1.39x surge ratio
        res_1_39 = TurnaroundScreener.evaluate_filter_volume_washout(
            stock_id="TEST",
            current_price=10.0,
            daily_change_pct=0.5,
            volume=1390000,
            support_price=9.5,
            benchmark_20d_volume=1000000,
        )
        self.assertFalse(res_1_39.passed)
        self.assertEqual(res_1_39.score, 8.0)  # Support held with green candle, but no surge

        # 1.40x surge ratio
        res_1_40 = TurnaroundScreener.evaluate_filter_volume_washout(
            stock_id="TEST",
            current_price=10.0,
            daily_change_pct=0.5,
            volume=1400000,
            support_price=9.5,
            benchmark_20d_volume=1000000,
        )
        self.assertTrue(res_1_40.passed)
        self.assertEqual(res_1_40.score, 15.0)

        # 1.41x surge ratio
        res_1_41 = TurnaroundScreener.evaluate_filter_volume_washout(
            stock_id="TEST",
            current_price=10.0,
            daily_change_pct=0.5,
            volume=1410000,
            support_price=9.5,
            benchmark_20d_volume=1000000,
        )
        self.assertTrue(res_1_41.passed)
        self.assertEqual(res_1_41.score, 15.0)

    def test_epsilon_boundary_daily_change_minus_0_01_vs_zero_vs_plus_0_01(self):
        """Daily return boundary at 0.00%: -0.01% is red candle (fails), 0.00% is flat rebound (passes)."""
        # -0.01% red candle
        res_minus = TurnaroundScreener.evaluate_filter_volume_washout(
            stock_id="TEST",
            current_price=10.0,
            daily_change_pct=-0.01,
            volume=2000000,
            support_price=9.5,
            benchmark_20d_volume=1000000,
        )
        self.assertFalse(res_minus.passed)
        self.assertEqual(res_minus.score, 4.0)  # Red candle adjustment

        # 0.00% flat candle
        res_zero = TurnaroundScreener.evaluate_filter_volume_washout(
            stock_id="TEST",
            current_price=10.0,
            daily_change_pct=0.00,
            volume=2000000,
            support_price=9.5,
            benchmark_20d_volume=1000000,
        )
        self.assertTrue(res_zero.passed)
        self.assertEqual(res_zero.score, 20.0)

        # +0.01% green candle
        res_plus = TurnaroundScreener.evaluate_filter_volume_washout(
            stock_id="TEST",
            current_price=10.0,
            daily_change_pct=0.01,
            volume=2000000,
            support_price=9.5,
            benchmark_20d_volume=1000000,
        )
        self.assertTrue(res_plus.passed)
        self.assertEqual(res_plus.score, 20.0)

    def test_support_floor_defense_boundary_99_pct(self):
        """Price defending support * 0.99 passes; price below support * 0.99 breaks support (0 pts)."""
        support = 10.0
        # price == 9.90 (exact 0.99x) -> defended
        res_defended = TurnaroundScreener.evaluate_filter_volume_washout(
            stock_id="TEST",
            current_price=9.90,
            daily_change_pct=1.0,
            volume=2000000,
            support_price=support,
            benchmark_20d_volume=1000000,
        )
        self.assertTrue(res_defended.passed)

        # price == 9.88 (< 9.90x) -> breached
        res_breached = TurnaroundScreener.evaluate_filter_volume_washout(
            stock_id="TEST",
            current_price=9.88,
            daily_change_pct=1.0,
            volume=2000000,
            support_price=support,
            benchmark_20d_volume=1000000,
        )
        self.assertFalse(res_breached.passed)
        self.assertEqual(res_breached.score, 0.0)
        self.assertIn("방어 실패", res_breached.detail)

    def test_edge_cases_zero_volume_and_zero_benchmark(self):
        """Zero volume or zero benchmark safely handled without ZeroDivisionError."""
        res_zero_vol = TurnaroundScreener.evaluate_filter_volume_washout(
            stock_id="T_ZERO_VOL",
            current_price=10.0,
            daily_change_pct=1.0,
            volume=0,
            support_price=9.0,
            benchmark_20d_volume=1000000,
        )
        self.assertFalse(res_zero_vol.passed)
        self.assertEqual(res_zero_vol.score, 8.0)  # Holds support & green, but 0 volume

        res_zero_bench = TurnaroundScreener.evaluate_filter_volume_washout(
            stock_id="T_ZERO_BENCH",
            current_price=10.0,
            daily_change_pct=1.0,
            volume=100000,
            support_price=9.0,
            benchmark_20d_volume=0,
        )
        self.assertFalse(res_zero_bench.passed)


class TestFilter4RiskReward(unittest.TestCase):
    """Test suite for Filter 4: Asymmetric Risk/Reward Ratio (RRR >= 10.0x)."""

    def test_happy_path_supreme_asymmetry(self):
        """Downside <= 8.5% and RRR >= 12.0x earns max 25.0 points."""
        # MBLY scenario: P = 7.47, S = 6.87, TP1 = 15.00
        # Downside: (7.47 - 6.87) / 7.47 = 8.03% <= 8.5%
        # Upside: (15.00 - 7.47) / 7.47 = 100.80% >= 100.0%
        # RRR = 100.80 / 8.03 = 12.55x >= 12.0x
        res = TurnaroundScreener.evaluate_filter_risk_reward(
            stock_id="MBLY",
            current_price=7.47,
            support_price=6.87,
            tp1_price=15.00,
        )
        self.assertTrue(res.passed)
        self.assertEqual(res.score, 25.0)
        self.assertAlmostEqual(res.actual_value, 12.55, places=1)
        self.assertIn("손익비", res.detail)

    def test_happy_path_celh_asymmetry(self):
        """CELH scenario: P = 27.35, S = 25.00, TP1 = 55.00 earns 22.0 points."""
        # Downside: (27.35 - 25.00) / 27.35 = 8.59% <= 10.0%
        # Upside: (55.00 - 27.35) / 27.35 = 101.10% >= 100.0%
        # RRR = 101.10 / 8.59 = 11.77x >= 10.0x
        res = TurnaroundScreener.evaluate_filter_risk_reward(
            stock_id="CELH",
            current_price=27.35,
            support_price=25.00,
            tp1_price=55.00,
        )
        self.assertTrue(res.passed)
        self.assertEqual(res.score, 22.0)
        self.assertAlmostEqual(res.actual_value, 11.77, places=1)

    def test_epsilon_boundary_downside_9_9_vs_10_0_vs_10_1(self):
        """Downside risk boundary at 10.0%: 9.9% passes, 10.0% passes, 10.1% fails."""
        # 9.9% downside risk
        res_9_9 = TurnaroundScreener.evaluate_filter_risk_reward(
            stock_id="T",
            current_price=100.0,
            support_price=90.1,  # Downside = 9.9%
            tp1_price=210.0,     # Upside = 110.0%
        )
        self.assertTrue(res_9_9.passed)
        self.assertEqual(res_9_9.score, 22.0)

        # 10.0% downside risk
        res_10_0 = TurnaroundScreener.evaluate_filter_risk_reward(
            stock_id="T",
            current_price=100.0,
            support_price=90.0,  # Downside = 10.0%
            tp1_price=210.0,     # Upside = 110.0%
        )
        self.assertTrue(res_10_0.passed)
        self.assertEqual(res_10_0.score, 22.0)

        # 10.1% downside risk (fails 10% threshold)
        res_10_1 = TurnaroundScreener.evaluate_filter_risk_reward(
            stock_id="T",
            current_price=100.0,
            support_price=89.9,  # Downside = 10.1%
            tp1_price=210.0,     # Upside = 110.0%
        )
        self.assertFalse(res_10_1.passed)
        self.assertEqual(res_10_1.score, 16.0)  # Sub-bracket 8x~10x score

    def test_epsilon_boundary_upside_99_9_vs_100_0_vs_100_1(self):
        """Upside to TP1 boundary at 100.0%: 99.9% fails, 100.0% passes, 100.1% passes."""
        # 99.9% upside
        res_99_9 = TurnaroundScreener.evaluate_filter_risk_reward(
            stock_id="T",
            current_price=100.0,
            support_price=92.0,  # Downside = 8.0%
            tp1_price=199.9,     # Upside = 99.9%
        )
        self.assertFalse(res_99_9.passed)

        # 100.0% upside
        res_100_0 = TurnaroundScreener.evaluate_filter_risk_reward(
            stock_id="T",
            current_price=100.0,
            support_price=92.0,  # Downside = 8.0%
            tp1_price=200.0,     # Upside = 100.0%
        )
        self.assertTrue(res_100_0.passed)

        # 100.1% upside
        res_100_1 = TurnaroundScreener.evaluate_filter_risk_reward(
            stock_id="T",
            current_price=100.0,
            support_price=92.0,  # Downside = 8.0%
            tp1_price=200.1,     # Upside = 100.1%
        )
        self.assertTrue(res_100_1.passed)

    def test_price_below_support_floor_penalty(self):
        """Price broken below support applies +10% penalty and fails condition 4."""
        res_below = TurnaroundScreener.evaluate_filter_risk_reward(
            stock_id="T_BELOW",
            current_price=9.0,
            support_price=10.0,  # Below support: breach distance 11.1% + 10% = 21.1%
            tp1_price=20.0,
        )
        self.assertFalse(res_below.passed)
        self.assertEqual(res_below.score, 5.0)

    def test_edge_cases_zero_price_and_tp1_below_current(self):
        """Zero price or TP1 below current handled safely."""
        res_zero = TurnaroundScreener.evaluate_filter_risk_reward("T", 0.0, 10.0, 20.0)
        self.assertFalse(res_zero.passed)
        self.assertEqual(res_zero.score, 0.0)

        res_tp_below = TurnaroundScreener.evaluate_filter_risk_reward("T", 100.0, 90.0, 80.0)
        self.assertFalse(res_tp_below.passed)
        self.assertEqual(res_tp_below.score, 0.0)


class TestCompositeScoringAndTiers(unittest.TestCase):
    """Test suite for Composite Score (0~100 Points) and Conviction Tiers."""

    def test_composite_score_summation(self):
        """Sums 4 sub-scores correctly and clamps between 0.0 and 100.0."""
        f1 = ScreeningFilterResult("c1", "F1", True, 20.0, 25.0, 5.0, "", "")
        f2 = ScreeningFilterResult("c2", "F2", True, 30.0, 30.0, "흑자전환", "", "")
        f3 = ScreeningFilterResult("c3", "F3", True, 15.0, 20.0, 1.6, "", "")
        f4 = ScreeningFilterResult("c4", "F4", True, 25.0, 25.0, 12.0, "", "")

        score = TurnaroundScreener.calculate_composite_score(f1, f2, f3, f4)
        self.assertEqual(score, 90.0)

    def test_conviction_tier_boundaries(self):
        """Strict verification of institutional conviction tier thresholds."""
        # TOP_PICK: >= 88.0 pts
        self.assertEqual(TurnaroundScreener.determine_conviction_tier(100.0), "TOP_PICK")
        self.assertEqual(TurnaroundScreener.determine_conviction_tier(88.0), "TOP_PICK")
        self.assertEqual(TurnaroundScreener.determine_conviction_tier(87.9), "STRONG_CANDIDATE")

        # STRONG_CANDIDATE: 75.0 ~ 87.9 pts
        self.assertEqual(TurnaroundScreener.determine_conviction_tier(85.0), "STRONG_CANDIDATE")
        self.assertEqual(TurnaroundScreener.determine_conviction_tier(75.0), "STRONG_CANDIDATE")
        self.assertEqual(TurnaroundScreener.determine_conviction_tier(74.9), "WATCHLIST")

        # WATCHLIST: 55.0 ~ 74.9 pts
        self.assertEqual(TurnaroundScreener.determine_conviction_tier(70.0), "WATCHLIST")
        self.assertEqual(TurnaroundScreener.determine_conviction_tier(55.0), "WATCHLIST")
        self.assertEqual(TurnaroundScreener.determine_conviction_tier(54.9), "DISQUALIFIED")

        # DISQUALIFIED: < 55.0 pts
        self.assertEqual(TurnaroundScreener.determine_conviction_tier(40.0), "DISQUALIFIED")
        self.assertEqual(TurnaroundScreener.determine_conviction_tier(0.0), "DISQUALIFIED")


class TestEmpiricalScreeningRealWatchlist(unittest.TestCase):
    """Test suite validating empirical behavior on verified real-world watchlist equities."""

    def test_mbly_qualifies_as_top_pick_with_confirmed_washout(self):
        """MBLY with confirmed 7.0M volume wash-out rebound achieves TOP_PICK conviction."""
        cand = TurnaroundScreener.screen_stock(
            stock_id="MBLY",
            current_price=7.10,
            volume=7008063,
            daily_change_pct=0.57,
            date="2026-10-07",
        )
        self.assertEqual(cand.stock_id, "MBLY")
        self.assertEqual(cand.name_kr, "모빌아이")
        self.assertEqual(cand.ticker, "MBLY")
        self.assertTrue(cand.is_qualified)
        self.assertEqual(cand.pass_count, 4)
        self.assertEqual(cand.conviction_tier, "TOP_PICK")
        self.assertGreaterEqual(cand.composite_turnaround_score, 88.0)
        self.assertEqual(cand.composite_turnaround_score, 92.5)  # 22.5 + 30 + 15 + 25 = 92.5

        # Verify all 4 individual filters
        self.assertTrue(cand.filters["cond1_52w_low"].passed)
        self.assertTrue(cand.filters["cond2_earnings_turnaround"].passed)
        self.assertTrue(cand.filters["cond3_volume_washout"].passed)
        self.assertTrue(cand.filters["cond4_risk_reward"].passed)

    def test_mbly_qualifies_as_strong_candidate_on_default_quote(self):
        """MBLY on default 2026-10-07 quote achieves STRONG_CANDIDATE and qualifies."""
        cand = TurnaroundScreener.screen_stock(stock_id="MBLY", date="2026-10-07")
        self.assertEqual(cand.stock_id, "MBLY")
        self.assertTrue(cand.is_qualified)
        self.assertGreaterEqual(cand.composite_turnaround_score, 75.0)
        self.assertIn(cand.conviction_tier, ("TOP_PICK", "STRONG_CANDIDATE"))
        self.assertEqual(cand.pass_count, 3)  # F1, F2, F4 pass

    def test_celh_qualifies_as_strong_candidate(self):
        """CELH achieves STRONG_CANDIDATE (76~80 pts) and qualifies."""
        cand = TurnaroundScreener.screen_stock(
            stock_id="CELH",
            volume=2850000,
            daily_change_pct=0.0,
            date="2026-10-07",
        )
        self.assertEqual(cand.stock_id, "CELH")
        self.assertIn("셀시우스", cand.name_kr)
        self.assertTrue(cand.is_qualified)
        self.assertEqual(cand.conviction_tier, "STRONG_CANDIDATE")
        self.assertGreaterEqual(cand.composite_turnaround_score, 75.0)
        self.assertEqual(cand.composite_turnaround_score, 80.0)

        # F1, F2, F4 pass
        self.assertTrue(cand.filters["cond1_52w_low"].passed)
        self.assertTrue(cand.filters["cond2_earnings_turnaround"].passed)
        self.assertTrue(cand.filters["cond4_risk_reward"].passed)

    def test_upst_is_disqualified_due_to_high_proximity(self):
        """UPST (+91.4% from 52w low) fails Filter 1 & Filter 4 and is DISQUALIFIED."""
        cand = TurnaroundScreener.screen_stock(stock_id="UPST", date="2026-10-07")
        self.assertEqual(cand.stock_id, "UPST")
        self.assertFalse(cand.is_qualified)
        self.assertEqual(cand.conviction_tier, "DISQUALIFIED")
        self.assertLess(cand.composite_turnaround_score, 55.0)

        # Filter 1 and Filter 4 must fail
        self.assertFalse(cand.filters["cond1_52w_low"].passed)
        self.assertFalse(cand.filters["cond4_risk_reward"].passed)
        self.assertGreater(cand.proximity_52w_low_pct, 50.0)

    def test_flnc_is_disqualified_due_to_high_proximity(self):
        """FLNC (+33.3% from 52w low) fails Filter 1 & Filter 4 and is DISQUALIFIED."""
        cand = TurnaroundScreener.screen_stock(stock_id="FLNC", date="2026-10-07")
        self.assertEqual(cand.stock_id, "FLNC")
        self.assertFalse(cand.is_qualified)
        self.assertEqual(cand.conviction_tier, "DISQUALIFIED")
        self.assertLess(cand.composite_turnaround_score, 55.0)

        # Filter 1 and Filter 4 must fail
        self.assertFalse(cand.filters["cond1_52w_low"].passed)
        self.assertFalse(cand.filters["cond4_risk_reward"].passed)


class TestUniverseScreeningAndWeeklyTopPick(unittest.TestCase):
    """Test suite for Universe Screening & Weekly Top Pick Selection."""

    def test_screen_universe_ranks_candidates_correctly(self):
        """Universe screening returns candidates ranked by composite score descending."""
        universe = TurnaroundScreener.screen_universe(date="2026-10-07")
        self.assertIsInstance(universe, list)
        self.assertGreaterEqual(len(universe), 6)

        # Scores must be monotonically non-increasing
        for i in range(len(universe) - 1):
            self.assertGreaterEqual(
                universe[i].composite_turnaround_score,
                universe[i + 1].composite_turnaround_score,
            )

        # Top 2 candidates must be MBLY and CELH
        top_ids = [c.stock_id for c in universe[:2]]
        self.assertIn("MBLY", top_ids)
        self.assertIn("CELH", top_ids)

        # Disqualified stocks at bottom
        bottom_ids = [c.stock_id for c in universe[-2:]]
        self.assertIn("FLNC", bottom_ids)
        self.assertIn("UPST", bottom_ids)

    def test_select_weekly_top_pick_returns_valid_object(self):
        """Selects single best Top-Pick turnaround stock with deep-dive metadata."""
        universe = TurnaroundScreener.screen_universe(date="2026-10-07")
        top_pick = TurnaroundScreener.select_weekly_top_pick(universe, date="2026-10-07")

        self.assertIsNotNone(top_pick)
        self.assertIsInstance(top_pick, WeeklyTopPick)
        self.assertEqual(top_pick.stock_id, "MBLY")
        self.assertEqual(top_pick.week_date, "2026-10-07")
        self.assertIn("자율주행", top_pick.business_model)
        self.assertIn("재고", top_pick.low_price_root_cause)
        self.assertGreaterEqual(len(top_pick.turnaround_catalyst_facts), 3)
        self.assertIn("TP1", top_pick.take_profit_roadmap)
        self.assertIn("SK스퀘어", top_pick.sk_square_switching_rationale)

    def test_select_weekly_top_pick_empty_universe(self):
        """Empty universe safely returns None."""
        top_pick = TurnaroundScreener.select_weekly_top_pick([], date="2026-10-07")
        self.assertIsNone(top_pick)

    def test_select_weekly_top_pick_returns_none_when_all_candidates_disqualified(self):
        """Disqualified candidate pool must strictly return None and never select a top pick."""
        c_upst = TurnaroundScreener.screen_stock("UPST", date="2026-10-07")
        c_flnc = TurnaroundScreener.screen_stock("FLNC", date="2026-10-07")
        top_pick = TurnaroundScreener.select_weekly_top_pick([c_upst, c_flnc], date="2026-10-07")
        self.assertIsNone(top_pick, "Disqualified candidates must never be promoted to weekly top pick")

    def test_candidate_rank_key_deterministic_tie_breaking(self):
        """When composite score and RRR are tied, selection is deterministic and order-independent."""
        c_a = TurnaroundScreener.screen_stock("MBLY", date="2026-10-07")
        c_b = TurnaroundScreener.screen_stock("CELH", date="2026-10-07")
        # Artificially tie scores
        c_a.composite_turnaround_score = 80.0
        c_a.risk_reward_ratio = 10.0
        c_b.composite_turnaround_score = 80.0
        c_b.risk_reward_ratio = 10.0

        pick1 = TurnaroundScreener.select_weekly_top_pick([c_a, c_b], date="2026-10-07")
        pick2 = TurnaroundScreener.select_weekly_top_pick([c_b, c_a], date="2026-10-07")
        self.assertIsNotNone(pick1)
        self.assertIsNotNone(pick2)
        self.assertEqual(pick1.stock_id, pick2.stock_id, "Tie breaking must be order independent")

    def test_epsilon_hardening_representation_exact_boundaries(self):
        """Float epsilon 1e-6 hardening ensures exact mathematical boundary multiples pass."""
        # Exact +20.0% proximity: 3.60 / 3.00
        res_f1 = TurnaroundScreener.evaluate_filter_52w_low("T", 3.60, 3.00, 10.0)
        self.assertTrue(res_f1.passed, "Exact 20.0% proximity must pass Filter 1")
        self.assertEqual(res_f1.actual_value, 20.0)

        # Exact +30.0% growth: 1.17 / 0.90
        fin_30 = {
            "years": ["2022", "2023", "2024", "2025", "2026E", "2027E"],
            "income_statement": {
                "revenue": [1.0, 1.0, 1.0, 0.90, 1.17, 1.17],
                "operating_income": [0.1, 0.1, 0.1, 0.1, 0.1, 0.1],
            },
        }
        res_f2 = TurnaroundScreener.evaluate_filter_earnings_turnaround("T", fin_30)
        self.assertTrue(res_f2.passed, "Exact 30.0% growth must pass Filter 2")
        self.assertEqual(res_f2.actual_value, 30.0)

        # Exact 10.0% downside: 1.10 / 0.99
        res_f4 = TurnaroundScreener.evaluate_filter_risk_reward("T", 1.10, 0.99, 2.50)
        self.assertTrue(res_f4.passed, "Exact 10.0% downside must pass Filter 4")


class TestSerializationAndContractCompliance(unittest.TestCase):
    """Test suite verifying contract compliance, JSON schema, and immutability."""

    def test_52w_range_string_parser(self):
        """Tests parsing of USD, KRW, and raw range strings."""
        low_usd, high_usd = parse_52w_range_string("$6.47 ~ $34.50")
        self.assertEqual(low_usd, 6.47)
        self.assertEqual(high_usd, 34.50)

        low_krw, high_krw = parse_52w_range_string("42,500원 ~ 1,189,000원")
        self.assertEqual(low_krw, 42500.0)
        self.assertEqual(high_krw, 1189000.0)

        self.assertEqual(parse_52w_range_string(""), (None, None))
        self.assertEqual(parse_52w_range_string("invalid"), (None, None))

    def test_screening_filter_result_serialization(self):
        """ScreeningFilterResult to_dict() produces valid schema with dual naming."""
        res = ScreeningFilterResult(
            filter_id="cond1_52w_low",
            filter_name="52주 신저가 근접도",
            passed=True,
            score=20.0,
            max_score=25.0,
            actual_value=15.46,
            threshold_description="<= 20.0%",
            detail="안전마진 확보",
        )
        d = res.to_dict()
        self.assertEqual(d["filterId"], "cond1_52w_low")
        self.assertEqual(d["filter_id"], "cond1_52w_low")
        self.assertEqual(d["passed"], True)
        self.assertEqual(d["score"], 20.0)

    def test_turnaround_candidate_serialization_roundtrip(self):
        """TurnaroundCandidate to_dict() produces 100% JSON-compliant dictionary."""
        cand = TurnaroundScreener.screen_stock("MBLY", date="2026-10-07")
        d = cand.to_dict()

        # Check required schema keys
        required_keys = [
            "stockId", "nameKr", "ticker", "market", "currency",
            "currentPrice", "currentPriceFormatted", "fiftyTwoWeekLow", "fiftyTwoWeekHigh",
            "proximity52wLowPct", "crashFromHighPct", "supportPrice", "downsideRiskPct",
            "tp1Price", "upsideTp1Pct", "riskRewardRatio", "revenueGrowth2yPct",
            "operatingIncomeGrowth2yPct", "isTurnaroundToProfit", "volumeSurgeRatio",
            "filters", "passCount", "isQualified", "compositeTurnaroundScore",
            "convictionTier", "recommendationSummary", "catalystDDay",
            "switchingFeasibilityVsSkSquare",
        ]
        for key in required_keys:
            self.assertIn(key, d, f"Missing required JSON key: {key}")

        # JSON dumps / loads roundtrip
        json_str = json.dumps(d, ensure_ascii=False)
        reloaded = json.loads(json_str)
        self.assertEqual(reloaded["stockId"], "MBLY")
        self.assertEqual(reloaded["convictionTier"], cand.conviction_tier)
        self.assertIsInstance(reloaded["filters"], dict)
        self.assertEqual(len(reloaded["filters"]), 4)

    def test_weekly_top_pick_serialization(self):
        """WeeklyTopPick to_dict() produces 100% JSON-compliant dictionary."""
        universe = TurnaroundScreener.screen_universe(date="2026-10-07")
        top_pick = TurnaroundScreener.select_weekly_top_pick(universe, date="2026-10-07")
        self.assertIsNotNone(top_pick)

        d = top_pick.to_dict()
        self.assertIn("weekDate", d)
        self.assertIn("stockId", d)
        self.assertIn("candidate", d)
        self.assertIn("businessModel", d)
        self.assertIn("lowPriceRootCause", d)
        self.assertIn("turnaroundCatalystFacts", d)

        json_str = json.dumps(d, ensure_ascii=False)
        self.assertIn("MBLY", json_str)


if __name__ == "__main__":
    unittest.main()
