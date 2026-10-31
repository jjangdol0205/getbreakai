"""
Comprehensive Unit & Integration Test Suite for Milestone 2:
Strategy A 52-Week Low Turnaround Concentrated in Max 2 Stocks & Systematic Weekly Switching.

Validates:
1. 4-Filter Screening: 52W low proximity (<=20%), earnings turnaround (>=30%), volume wash-out (>=1.40x), asymmetric RRR (>=10x).
2. Max 2 Stocks Concentration: 100% single winner (TOP_PICK >= 88.0 and no other >= 75.0) vs 50/50 dual concentration.
3. Defensive Benchmark Spillover: when 0 candidates qualify -> 100% benchmark spillover (zero cash constraint w_cash = 0.0).
4. Weekly Switching Hurdles: STRONG_SWITCH tier requirement vs >= 15-pt score gap.
5. Reverse-Switching Defense Lock: strictly forbids switching away from holding with imminent catalyst (D-Day <= 20) in safety margin.
6. Asymmetric Exit Rules: TP1 (+100% gain -> 50% exit -> 100% principal recovered in cash, runner held risk-free) and -10% stop loss.
7. Seamless Integration with BacktestEngine: 0.1% fee, 0.08% slippage, 5 rebalance cycles, 22% foreign equity tax, annual deduction.
8. 25-Year Full Simulation & Financial Metrics Suite: pre/after-tax CAGR, MDD, Sharpe, Calmar, and Tax Drag.

100% Offline, Zero-CDN, Pure Python Standard Library.
"""

from __future__ import annotations

import math
import unittest
from typing import Dict, List, Optional

from engine.backtest_engine import (
    BacktestConfig,
    PerformanceMetrics,
    RebalanceFrequency,
    SimulationResult,
    TaxAccountingState,
)
from engine.turnaround_screener import (
    ScreeningFilterResult,
    TurnaroundCandidate,
    TurnaroundScreener,
)
from engine.strategy_turnaround import (
    ExitDecision,
    HISTORICAL_TURNAROUND_EPISODES,
    StrategyASimulator,
    SwitchingEvaluation,
    TurnaroundEpisode,
    TurnaroundPosition,
)


def make_candidate_helper(
    stock_id: str = "TEST_STOCK",
    current_price: float = 10.0,
    composite_score: float = 80.0,
    conviction_tier: str = "STRONG_CANDIDATE",
    pass_count: int = 4,
    catalyst_d_day: Optional[int] = 30,
    proximity_pct: float = 10.0,
    risk_reward_ratio: float = 12.0,
) -> TurnaroundCandidate:
    """Helper factory creating valid TurnaroundCandidate instances for deterministic unit tests."""
    low_52w = current_price / (1.0 + proximity_pct / 100.0)
    high_52w = current_price * 2.5
    supp_p = current_price * 0.92
    tp1_p = current_price * 2.0

    dummy_filter = ScreeningFilterResult(
        filter_id="test_filter",
        filter_name="Test Filter",
        passed=True,
        score=20.0,
        max_score=25.0,
        actual_value=1.0,
        threshold_description="test",
        detail="test passed",
    )

    filters = {
        "cond1_52w_low": dummy_filter,
        "cond2_earnings_turnaround": dummy_filter,
        "cond3_volume_washout": dummy_filter,
        "cond4_risk_reward": dummy_filter,
    }

    is_qualified = (pass_count == 4) or (pass_count >= 3 and composite_score >= 75.0)

    return TurnaroundCandidate(
        stock_id=stock_id,
        name_kr=stock_id,
        ticker=stock_id,
        market="US",
        currency="USD",
        current_price=current_price,
        current_price_formatted=f"${current_price:.2f}",
        fifty_two_week_low=low_52w,
        fifty_two_week_high=high_52w,
        proximity_52w_low_pct=proximity_pct,
        crash_from_high_pct=-60.0,
        support_price=supp_p,
        downside_risk_pct=8.0,
        tp1_price=tp1_p,
        upside_tp1_pct=100.0,
        risk_reward_ratio=risk_reward_ratio,
        revenue_growth_2y_pct=35.0,
        operating_income_growth_2y_pct=120.0,
        is_turnaround_to_profit=True,
        volume_surge_ratio=2.0,
        filters=filters,
        pass_count=pass_count,
        is_qualified=is_qualified,
        composite_turnaround_score=composite_score,
        conviction_tier=conviction_tier,
        recommendation_summary=f"[{conviction_tier}] {stock_id}",
        catalyst_d_day=catalyst_d_day,
    )


# ==============================================================================
# 1. 4-Filter Screening Unit Tests
# ==============================================================================

class TestStrategyA4FilterScreening(unittest.TestCase):
    """Verifies quantitative 4-filter screening logic and conviction tiering."""

    def setUp(self) -> None:
        self.sim = StrategyASimulator()

    def test_filter_1_52w_low_proximity_and_crash_depth_bonus(self) -> None:
        """Filter 1: Proximity <= 20.0% passes with crash depth bonuses (+3 / +5 pts)."""
        # Price $11.0 near 52W low $10.0 -> proximity +10.0% -> PASS
        f1_pass = TurnaroundScreener.evaluate_filter_52w_low(
            stock_id="MBLY",
            current_price=11.0,
            fifty_two_week_low=10.0,
            fifty_two_week_high=40.0,  # crash -72.5% -> +5 pts bonus
        )
        self.assertTrue(f1_pass.passed)
        self.assertGreaterEqual(f1_pass.score, 20.0)
        self.assertEqual(f1_pass.actual_value, 10.0)

        # Price $13.5 vs 52W low $10.0 -> proximity +35.0% -> FAIL (> 20.0%)
        f1_fail = TurnaroundScreener.evaluate_filter_52w_low(
            stock_id="UPST",
            current_price=13.5,
            fifty_two_week_low=10.0,
            fifty_two_week_high=20.0,
        )
        self.assertFalse(f1_fail.passed)
        self.assertEqual(f1_fail.score, 0.0)

    def test_filter_2_earnings_turnaround(self) -> None:
        """Filter 2: Forward Rev/OI growth >= 30.0% or operating loss -> profit turnaround."""
        # Turnaround loss to profit -> PASS with full 30.0 points
        cand_profit = self.sim.screen_candidate(
            stock_id="MBLY",
            current_price=7.47,
            fifty_two_week_low=6.47,
            fifty_two_week_high=34.50,
            support_price=6.87,
            tp1_price=15.0,
            revenue_growth_2y=38.0,
            operating_income_growth_2y=150.0,
            is_turnaround_to_profit=True,
            volume=2_000_000,
            benchmark_20d_volume=1_000_000,
        )
        f2 = cand_profit.filters["cond2_earnings_turnaround"]
        self.assertTrue(f2.passed)
        self.assertEqual(f2.score, 30.0)

        # Anemic growth (< 30%) without profit swing -> FAIL
        cand_weak = self.sim.screen_candidate(
            stock_id="WEAK",
            current_price=10.0,
            fifty_two_week_low=9.5,
            fifty_two_week_high=15.0,
            support_price=9.0,
            tp1_price=20.0,
            revenue_growth_2y=10.0,
            operating_income_growth_2y=12.0,
            is_turnaround_to_profit=False,
            volume=1_000_000,
            benchmark_20d_volume=1_000_000,
        )
        f2_weak = cand_weak.filters["cond2_earnings_turnaround"]
        self.assertFalse(f2_weak.passed)
        self.assertEqual(f2_weak.score, 0.0)

    def test_filter_3_volume_washout_and_support_defense(self) -> None:
        """Filter 3: Volume >= 1.40x benchmark, defends key floor (P >= Supp * 0.99), rebound candle."""
        f3_pass = TurnaroundScreener.evaluate_filter_volume_washout(
            stock_id="CELH",
            current_price=27.35,
            daily_change_pct=1.2,
            volume=3_000_000,
            support_price=25.0,
            benchmark_20d_volume=1_500_000,  # 2.0x surge
        )
        self.assertTrue(f3_pass.passed)
        self.assertEqual(f3_pass.score, 20.0)

        # Support floor breach -> FAIL immediately
        f3_breach = TurnaroundScreener.evaluate_filter_volume_washout(
            stock_id="CELH",
            current_price=23.0,
            daily_change_pct=1.0,
            volume=3_000_000,
            support_price=25.0,
            benchmark_20d_volume=1_500_000,
        )
        self.assertFalse(f3_breach.passed)
        self.assertEqual(f3_breach.score, 0.0)

    def test_filter_4_asymmetric_risk_reward(self) -> None:
        """Filter 4: Downside <= 10.0%, Upside to TP1 >= 100.0%, RRR >= 10.0x."""
        f4_pass = TurnaroundScreener.evaluate_filter_risk_reward(
            stock_id="ENPH",
            current_price=30.0,
            support_price=28.0,  # downside 6.67%
            tp1_price=60.0,      # upside 100.0% -> RRR 15.0x
        )
        self.assertTrue(f4_pass.passed)
        self.assertGreaterEqual(f4_pass.score, 22.0)

        # Downside too large (15% > 10%) -> FAIL
        f4_fail = TurnaroundScreener.evaluate_filter_risk_reward(
            stock_id="ENPH",
            current_price=30.0,
            support_price=25.0,  # downside 16.7%
            tp1_price=60.0,
        )
        self.assertFalse(f4_fail.passed)

    def test_composite_score_and_conviction_tiers(self) -> None:
        """Validates composite score summation (0~100) and conviction tier thresholds."""
        self.assertEqual(TurnaroundScreener.determine_conviction_tier(92.0), "TOP_PICK")
        self.assertEqual(TurnaroundScreener.determine_conviction_tier(88.0), "TOP_PICK")
        self.assertEqual(TurnaroundScreener.determine_conviction_tier(87.9), "STRONG_CANDIDATE")
        self.assertEqual(TurnaroundScreener.determine_conviction_tier(75.0), "STRONG_CANDIDATE")
        self.assertEqual(TurnaroundScreener.determine_conviction_tier(74.9), "WATCHLIST")
        self.assertEqual(TurnaroundScreener.determine_conviction_tier(55.0), "WATCHLIST")
        self.assertEqual(TurnaroundScreener.determine_conviction_tier(54.9), "DISQUALIFIED")


# ==============================================================================
# 2. Max 2 Stocks Concentration & Allocation Unit Tests
# ==============================================================================

class TestStrategyAConcentrationAndAllocation(unittest.TestCase):
    """Verifies 100% single winner vs 50/50 dual concentration and defensive spillover."""

    def test_single_winner_100_percent_concentration(self) -> None:
        """100% Single Winner: 1 candidate achieves TOP_PICK (score >= 88.0) and no other >= 75.0."""
        c1 = make_candidate_helper(stock_id="MBLY", composite_score=92.0, conviction_tier="TOP_PICK")
        c2 = make_candidate_helper(stock_id="CELH", composite_score=68.0, conviction_tier="WATCHLIST")
        c3 = make_candidate_helper(stock_id="ENPH", composite_score=50.0, conviction_tier="DISQUALIFIED")

        weights = StrategyASimulator.calculate_concentration_weights([c1, c2, c3], benchmark_symbol="QQQ")
        self.assertEqual(weights, {"MBLY": 1.0})
        self.assertEqual(sum(weights.values()), 1.0)

    def test_dual_top_pick_50_50_concentration(self) -> None:
        """50% / 50% Dual Concentration: 2 or more candidates have score >= 75.0."""
        c1 = make_candidate_helper(stock_id="MBLY", composite_score=90.0, conviction_tier="TOP_PICK")
        c2 = make_candidate_helper(stock_id="CELH", composite_score=82.0, conviction_tier="STRONG_CANDIDATE")
        c3 = make_candidate_helper(stock_id="ENPH", composite_score=78.0, conviction_tier="STRONG_CANDIDATE")

        weights = StrategyASimulator.calculate_concentration_weights([c1, c2, c3], benchmark_symbol="QQQ")
        self.assertEqual(weights, {"MBLY": 0.50, "CELH": 0.50})
        self.assertEqual(sum(weights.values()), 1.0)
        self.assertEqual(len(weights), 2)

    def test_single_candidate_between_75_and_88(self) -> None:
        """Single candidate with 75.0 <= score < 88.0 -> 50% candidate + 50% defensive benchmark."""
        c1 = make_candidate_helper(stock_id="MBLY", composite_score=82.0, conviction_tier="STRONG_CANDIDATE")
        c2 = make_candidate_helper(stock_id="CELH", composite_score=60.0, conviction_tier="WATCHLIST")

        weights = StrategyASimulator.calculate_concentration_weights([c1, c2], benchmark_symbol="QQQ")
        self.assertEqual(weights, {"MBLY": 0.50, "QQQ": 0.50})
        self.assertEqual(sum(weights.values()), 1.0)

    def test_zero_qualified_candidates_defensive_spillover(self) -> None:
        """0 qualified candidates -> 100% allocation to core benchmark to maintain simplex (w_cash = 0)."""
        c1 = make_candidate_helper(stock_id="CELH", composite_score=62.0, conviction_tier="WATCHLIST")
        c2 = make_candidate_helper(stock_id="ENPH", composite_score=45.0, conviction_tier="DISQUALIFIED")

        weights = StrategyASimulator.calculate_concentration_weights([c1, c2], benchmark_symbol="QQQ")
        self.assertEqual(weights, {"QQQ": 1.0})
        self.assertEqual(sum(weights.values()), 1.0)

        # Empty candidate pool also yields 100% benchmark
        weights_empty = StrategyASimulator.calculate_concentration_weights([], benchmark_symbol="SOXX")
        self.assertEqual(weights_empty, {"SOXX": 1.0})

    def test_overload_candidates_strictly_capped_at_max_2_stocks(self) -> None:
        """Universe with 8 qualified candidates is compressed into strictly top 2 stocks."""
        candidates = [
            make_candidate_helper(stock_id=f"STK_{i}", composite_score=75.0 + i * 2.0)
            for i in range(8)
        ]
        weights = StrategyASimulator.calculate_concentration_weights(candidates, benchmark_symbol="QQQ")
        self.assertEqual(len(weights), 2)
        self.assertIn("STK_7", weights)
        self.assertIn("STK_6", weights)
        self.assertEqual(weights["STK_7"], 0.50)
        self.assertEqual(weights["STK_6"], 0.50)


# ==============================================================================
# 3. Weekly Switching & Reverse-Switching Defense Lock Tests
# ==============================================================================

class TestStrategyASwitchingAndDefenseLock(unittest.TestCase):
    """Verifies weekly switching hurdles and reverse-switching warning locks."""

    def test_switching_hurdle_score_gap_15_pts(self) -> None:
        """Switching executes when candidate score is >= 15.0 points higher than holding."""
        pos = TurnaroundPosition(
            stock_id="CELH",
            entry_date="2024-01-01",
            entry_price=30.0,
            current_price=31.0,
            shares=100.0,
            initial_shares=100.0,
            initial_cost=3000.0,
            support_price=28.0,
            tp1_price=60.0,
            composite_score=70.0,
            catalyst_d_day=50,  # Not locked (D-Day > 20)
            fifty_two_week_low=28.0,
        )

        cand = make_candidate_helper(stock_id="MBLY", composite_score=86.0, catalyst_d_day=40)
        eval_res = StrategyASimulator.evaluate_switching_hurdle(pos, cand)

        self.assertTrue(eval_res.should_switch)
        self.assertFalse(eval_res.is_reverse_warning_locked)
        self.assertGreaterEqual(eval_res.score_gap, 15.0)  # 86.0 - 70.0 = 16.0 >= 15.0

    def test_switching_hurdle_fails_when_gap_under_15_pts(self) -> None:
        """Switching is rejected when score gap is < 15.0 pts and STRONG_SWITCH not met."""
        pos = TurnaroundPosition(
            stock_id="CELH",
            entry_date="2024-01-01",
            entry_price=30.0,
            current_price=31.0,
            shares=100.0,
            initial_shares=100.0,
            initial_cost=3000.0,
            support_price=28.0,
            tp1_price=60.0,
            composite_score=75.0,
            catalyst_d_day=45,
            fifty_two_week_low=28.0,
        )

        cand = make_candidate_helper(stock_id="ENPH", composite_score=82.0, catalyst_d_day=40)
        eval_res = StrategyASimulator.evaluate_switching_hurdle(pos, cand)

        self.assertFalse(eval_res.should_switch)
        self.assertLess(eval_res.score_gap, 15.0)  # 82.0 - 75.0 = 7.0 < 15.0
        self.assertEqual(eval_res.candidate_tier, "HOLD_CORE")

    def test_switching_strong_switch_tier(self) -> None:
        """Candidate with STRONG_SWITCH tier clears hurdle even with modest score gap."""
        pos = TurnaroundPosition(
            stock_id="FLNC",
            entry_date="2024-01-01",
            entry_price=15.0,
            current_price=15.5,
            shares=100.0,
            initial_shares=100.0,
            initial_cost=1500.0,
            support_price=14.0,
            tp1_price=30.0,
            composite_score=74.0,
            catalyst_d_day=60,
            fifty_two_week_low=14.0,
        )

        # Candidate with catalyst advantage >= 30 days and D-Day <= 30 days
        cand = make_candidate_helper(
            stock_id="MBLY",
            composite_score=85.0,
            catalyst_d_day=25,  # 60 - 25 = 35 days advantage
            risk_reward_ratio=15.0,
        )
        eval_res = StrategyASimulator.evaluate_switching_hurdle(pos, cand)

        self.assertTrue(eval_res.should_switch)
        self.assertEqual(eval_res.candidate_tier, "STRONG_SWITCH")

    def test_reverse_switching_warning_lock_active(self) -> None:
        """Reverse-Switching Warning Lock FORBIDS switching when holding has D-Day <= 20 in safety margin."""
        pos = TurnaroundPosition(
            stock_id="MBLY",
            entry_date="2024-01-01",
            entry_price=7.0,
            current_price=7.4,
            shares=1000.0,
            initial_shares=1000.0,
            initial_cost=7000.0,
            support_price=6.87,
            tp1_price=14.0,
            composite_score=72.0,
            catalyst_d_day=12,  # Imminent catalyst D-Day <= 20!
            fifty_two_week_low=6.5,
        )

        # New candidate with massive score advantage (+23 pts)
        cand = make_candidate_helper(stock_id="ENPH", composite_score=95.0, catalyst_d_day=50)
        eval_res = StrategyASimulator.evaluate_switching_hurdle(pos, cand)

        self.assertTrue(eval_res.is_reverse_warning_locked)
        self.assertFalse(eval_res.should_switch, "Defense lock must override candidate score advantage")
        self.assertIn("REVERSE_SWITCH_WARNING", eval_res.reason)

    def test_reverse_switching_lock_releases_when_d_day_over_20(self) -> None:
        """Defense lock is inactive when catalyst D-Day > 20 days."""
        pos = TurnaroundPosition(
            stock_id="MBLY",
            entry_date="2024-01-01",
            entry_price=7.0,
            current_price=7.4,
            shares=1000.0,
            initial_shares=1000.0,
            initial_cost=7000.0,
            support_price=6.87,
            tp1_price=14.0,
            composite_score=70.0,
            catalyst_d_day=25,  # D-Day > 20
            fifty_two_week_low=6.5,
        )

        cand = make_candidate_helper(stock_id="ENPH", composite_score=88.0, catalyst_d_day=50)
        eval_res = StrategyASimulator.evaluate_switching_hurdle(pos, cand)

        self.assertFalse(eval_res.is_reverse_warning_locked)
        self.assertTrue(eval_res.should_switch)


# ==============================================================================
# 4. Asymmetric Exit Rules Unit Tests
# ==============================================================================

class TestStrategyAAsymmetricExits(unittest.TestCase):
    """Verifies TP1 100% principal recovery and -10% stop-loss mechanics."""

    def test_tp1_principal_recovery_math(self) -> None:
        """TP1: Price doubles (2.0x entry) -> sells 50% of position -> recovers 100% of principal in cash."""
        pos = TurnaroundPosition(
            stock_id="MBLY",
            entry_date="2024-01-01",
            entry_price=7.50,
            current_price=7.50,
            shares=1000.0,
            initial_shares=1000.0,
            initial_cost=7500.0,
            support_price=6.87,
            tp1_price=15.00,
            cost_basis=7.50,
        )

        # Price hits TP1 ($15.00)
        exit_dec = StrategyASimulator.check_position_exits(pos, current_price=15.00)

        self.assertEqual(exit_dec.action, "TP1_PARTIAL")
        self.assertEqual(exit_dec.shares_to_sell, 500.0)
        self.assertEqual(exit_dec.cash_realized, 7500.0)
        self.assertEqual(exit_dec.cash_realized, pos.initial_cost, "Recovered cash must equal 100% of initial principal")
        self.assertEqual(pos.shares, 500.0)
        self.assertTrue(pos.tp1_executed)
        self.assertTrue(pos.is_risk_free)
        self.assertEqual(pos.cost_basis, 0.0, "Cost basis of runner becomes $0.00")

    def test_tp1_runner_preservation_and_idempotence(self) -> None:
        """TP1 executes once; runner continues to hold and does not re-trigger TP1."""
        pos = TurnaroundPosition(
            stock_id="MBLY",
            entry_date="2024-01-01",
            entry_price=7.50,
            current_price=15.00,
            shares=500.0,
            initial_shares=1000.0,
            initial_cost=7500.0,
            support_price=6.87,
            tp1_price=15.00,
            tp1_executed=True,
            is_risk_free=True,
            cost_basis=0.0,
        )

        # Price climbs further to $18.00 -> should HOLD runner
        exit_dec = StrategyASimulator.check_position_exits(pos, current_price=18.00)
        self.assertEqual(exit_dec.action, "HOLD")
        self.assertEqual(pos.shares, 500.0)

    def test_stop_loss_10_percent_loss_cap(self) -> None:
        """Stop-Loss: Price drops -10% from entry -> sells 100% of shares immediately."""
        pos = TurnaroundPosition(
            stock_id="CELH",
            entry_date="2024-01-01",
            entry_price=30.00,
            current_price=30.00,
            shares=200.0,
            initial_shares=200.0,
            initial_cost=6000.0,
            support_price=27.50,
            tp1_price=60.00,
            cost_basis=30.00,
        )

        # Price drops to $27.00 (-10.0%)
        exit_dec = StrategyASimulator.check_position_exits(pos, current_price=27.00)

        self.assertEqual(exit_dec.action, "STOP_LOSS_FULL")
        self.assertEqual(exit_dec.shares_to_sell, 200.0)
        self.assertEqual(pos.shares, 0.0)
        self.assertEqual(exit_dec.cash_realized, 5400.0)
        self.assertEqual(exit_dec.realized_gain, -600.0)  # Exactly -10% loss

    def test_stop_loss_support_floor_breach(self) -> None:
        """Stop-Loss: Price drops below support floor by -10% -> sells 100% of shares."""
        pos = TurnaroundPosition(
            stock_id="CELH",
            entry_date="2024-01-01",
            entry_price=30.00,
            current_price=28.00,
            shares=200.0,
            initial_shares=200.0,
            initial_cost=6000.0,
            support_price=26.00,
            tp1_price=60.00,
            cost_basis=30.00,
        )

        # Support is $26.00; price breaches $23.00 (below 26.0 * 0.90 = 23.40)
        exit_dec = StrategyASimulator.check_position_exits(pos, current_price=23.00)
        self.assertEqual(exit_dec.action, "STOP_LOSS_FULL")
        self.assertEqual(pos.shares, 0.0)

    def test_hold_decision_within_normal_fluctuation(self) -> None:
        """Price fluctuating between -5% and +80% maintains normal HOLD status."""
        pos = TurnaroundPosition(
            stock_id="ENPH",
            entry_date="2024-01-01",
            entry_price=30.00,
            current_price=30.00,
            shares=100.0,
            initial_shares=100.0,
            initial_cost=3000.0,
            support_price=28.00,
            tp1_price=60.00,
            cost_basis=30.00,
        )

        exit_dec = StrategyASimulator.check_position_exits(pos, current_price=35.00)
        self.assertEqual(exit_dec.action, "HOLD")
        self.assertEqual(pos.shares, 100.0)


# ==============================================================================
# 5. Full Simulation, Friction & Tax Modeling Tests
# ==============================================================================

class TestStrategyABacktestSimulationAndTax(unittest.TestCase):
    """Verifies full simulation across 5 rebalancing cycles and capital gains tax modeling."""

    def setUp(self) -> None:
        self.sim = StrategyASimulator()

    def test_25yr_simulation_runs_successfully(self) -> None:
        """Full 25.25-year backtest simulation executes and returns valid SimulationResult."""
        res = self.sim.run_simulation()
        self.assertIsInstance(res, SimulationResult)
        self.assertIsInstance(res.metrics, PerformanceMetrics)
        self.assertGreater(len(res.dates), 6000)
        self.assertEqual(len(res.daily_nav), len(res.dates))
        self.assertEqual(len(res.daily_drawdowns), len(res.dates))
        self.assertGreater(res.metrics.cagr_pre_tax, 5.0)
        self.assertLess(res.metrics.mdd_pct, 0.0)
        self.assertGreater(res.metrics.calmar_ratio, 0.0)

    def test_all_5_rebalance_frequencies(self) -> None:
        """All 5 rebalancing frequencies execute cleanly and produce valid metrics."""
        for freq in RebalanceFrequency:
            cfg = BacktestConfig(frequency=freq, tax_enabled=False)
            res = self.sim.run_simulation(cfg)
            self.assertGreater(res.metrics.cagr_pct, 0.0)
            self.assertLess(res.metrics.mdd_pct, 0.0)
            self.assertGreater(len(res.rebalance_records), 0)

    def test_turnover_ordering_across_frequencies(self) -> None:
        """Weekly rebalancing incurs strictly higher turnover than Monthly and Annually."""
        cfg_w = BacktestConfig(frequency=RebalanceFrequency.WEEKLY, tax_enabled=False)
        cfg_m = BacktestConfig(frequency=RebalanceFrequency.MONTHLY, tax_enabled=False)
        cfg_a = BacktestConfig(frequency=RebalanceFrequency.ANNUALLY, tax_enabled=False)

        res_w = self.sim.run_simulation(cfg_w)
        res_m = self.sim.run_simulation(cfg_m)
        res_a = self.sim.run_simulation(cfg_a)

        self.assertGreater(res_w.metrics.total_turnover, res_m.metrics.total_turnover)
        self.assertGreater(res_m.metrics.total_turnover, res_a.metrics.total_turnover)

    def test_friction_deductions_applied(self) -> None:
        """Brokerage commission (0.10%) and execution slippage (0.08%) are deducted."""
        res = self.sim.run_simulation()
        self.assertGreater(res.metrics.fee_paid, 0.0)
        self.assertGreater(res.metrics.slippage_paid, 0.0)
        # Ratio of fee to slippage should be exactly 0.0010 / 0.0008 = 1.25
        self.assertAlmostEqual(res.metrics.fee_paid / res.metrics.slippage_paid, 1.25, places=2)

    def test_foreign_equity_tax_modeling(self) -> None:
        """22% foreign equity tax creates quantifiable tax drag and after-tax CAGR <= pre-tax."""
        cfg = BacktestConfig(
            frequency=RebalanceFrequency.WEEKLY,
            tax_enabled=True,
            tax_rate=0.22,
            annual_tax_deduction=2_500_000.0,
            initial_capital=100_000_000.0,
        )
        res = self.sim.run_simulation(cfg)

        self.assertGreaterEqual(res.metrics.cagr_pre_tax, res.metrics.cagr_after_tax)
        self.assertGreater(res.metrics.tax_drag_pct, 0.0)
        self.assertGreater(res.metrics.total_tax_paid, 0.0)
        self.assertGreater(len(res.tax_history), 0)

    def test_tax_drag_higher_in_frequent_rebalancing(self) -> None:
        """Weekly rebalancing incurs higher total tax paid and drag than Annual rebalancing."""
        cfg_w = BacktestConfig(frequency=RebalanceFrequency.WEEKLY, tax_enabled=True)
        cfg_a = BacktestConfig(frequency=RebalanceFrequency.ANNUALLY, tax_enabled=True)

        res_w = self.sim.run_simulation(cfg_w)
        res_a = self.sim.run_simulation(cfg_a)

        self.assertGreaterEqual(res_w.metrics.total_tax_paid, res_a.metrics.total_tax_paid)

    def test_zero_cash_simplex_throughout_simulation(self) -> None:
        """Holdings history confirms 100% equity simplex constraint (zero cash) at all times."""
        res = self.sim.run_simulation()
        for idx in range(0, len(res.holdings_history), 100):
            weights = res.holdings_history[idx]
            self.assertAlmostEqual(sum(weights.values()), 1.0, places=3)
            self.assertNotIn("cash", weights)
            self.assertNotIn("CASH", weights)


if __name__ == "__main__":
    unittest.main()
