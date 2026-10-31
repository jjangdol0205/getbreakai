"""
Adversarial Stress Test Suite for Milestone 2: Strategy A 25-Year Quantitative Backtesting.
Authored by: challenger_m2_2 (EMPIRICAL CHALLENGER)

Pillars Tested:
1. 25-year continuous compounding across all 5 rebalancing cycles (Weekly, Monthly, Quarterly, Semi-Annually, Annually).
2. Brokerage fee (0.10%) and slippage (0.08%) turnover friction dynamics.
3. 22% capital gains tax with 2.5M KRW / $2,000 deduction and tax deferral behavior.
4. 100% equity simplex invariant (w_cash == 0.0 and sum(w_i) == 1.0 at all timesteps, including TP1/Stop-loss exits).
5. Asymmetric exit payoff mechanics (TP1 100% principal recovery, runner risk-free status, -10% stop loss).
6. Weekly switching hurdle and reverse-switching defense lock invariants.
7. Extreme boundary stress testing (alternative benchmarks, zero friction, extreme volatility).
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
from engine.historical_data import (
    COMMON_START_DATE,
    COMMON_END_DATE,
    get_joint_history,
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


def make_dummy_candidate(
    stock_id: str,
    score: float,
    current_price: float = 10.0,
    support_price: float = 9.0,
    tp1_price: float = 20.0,
    catalyst_d_day: Optional[int] = 30,
    pass_count: int = 4,
    tier: str = "STRONG_CANDIDATE",
) -> TurnaroundCandidate:
    dummy_filter = ScreeningFilterResult(
        filter_id="test_filter",
        filter_name="Test",
        passed=True,
        score=20.0,
        max_score=25.0,
        actual_value=1.0,
        threshold_description="test",
        detail="passed",
    )
    filters = {
        "cond1_52w_low": dummy_filter,
        "cond2_earnings_turnaround": dummy_filter,
        "cond3_volume_washout": dummy_filter,
        "cond4_risk_reward": dummy_filter,
    }
    return TurnaroundCandidate(
        stock_id=stock_id,
        name_kr=stock_id,
        ticker=stock_id,
        market="US",
        currency="USD",
        current_price=current_price,
        current_price_formatted=f"${current_price:.2f}",
        fifty_two_week_low=current_price * 0.90,
        fifty_two_week_high=current_price * 2.50,
        proximity_52w_low_pct=11.1,
        crash_from_high_pct=-60.0,
        support_price=support_price,
        downside_risk_pct=10.0,
        tp1_price=tp1_price,
        upside_tp1_pct=100.0,
        risk_reward_ratio=10.0,
        revenue_growth_2y_pct=35.0,
        operating_income_growth_2y_pct=120.0,
        is_turnaround_to_profit=True,
        volume_surge_ratio=2.0,
        filters=filters,
        pass_count=pass_count,
        is_qualified=(pass_count == 4 or (pass_count >= 3 and score >= 75.0)),
        composite_turnaround_score=score,
        conviction_tier=tier,
        recommendation_summary=f"[{tier}] {stock_id}",
        catalyst_d_day=catalyst_d_day,
    )


class TestStrategyACompoundingAll5Cycles(unittest.TestCase):
    """Stress testing 25-year compounding across all 5 rebalancing cycles."""

    def setUp(self) -> None:
        self.sim = StrategyASimulator()

    def test_25yr_compounding_across_all_5_cycles_non_empty_and_finite(self) -> None:
        """Every rebalance frequency must run across 25.25 years with finite, non-NaN metrics."""
        for freq in RebalanceFrequency:
            cfg = BacktestConfig(frequency=freq, tax_enabled=True)
            res = self.sim.run_simulation(cfg)
            m = res.metrics

            self.assertGreater(len(res.dates), 6300, f"{freq.value} dates length too short")
            self.assertEqual(len(res.daily_nav), len(res.dates))
            self.assertEqual(len(res.daily_drawdowns), len(res.dates))

            # Mathematical sanity of financial metrics
            self.assertFalse(math.isnan(m.cagr_pre_tax), f"{freq.value} cagr_pre_tax is NaN")
            self.assertFalse(math.isinf(m.cagr_pre_tax), f"{freq.value} cagr_pre_tax is Inf")
            self.assertFalse(math.isnan(m.cagr_after_tax), f"{freq.value} cagr_after_tax is NaN")
            self.assertFalse(math.isinf(m.cagr_after_tax), f"{freq.value} cagr_after_tax is Inf")
            self.assertFalse(math.isnan(m.mdd_pct), f"{freq.value} mdd_pct is NaN")
            self.assertFalse(math.isnan(m.sharpe_ratio), f"{freq.value} sharpe is NaN")
            self.assertFalse(math.isnan(m.calmar_ratio), f"{freq.value} calmar is NaN")

            # Basic financial direction
            self.assertGreater(m.cagr_pre_tax, 5.0, f"{freq.value} pre-tax CAGR too low")
            self.assertGreater(m.cagr_after_tax, 5.0, f"{freq.value} after-tax CAGR too low")
            self.assertLess(m.mdd_pct, 0.0, f"{freq.value} MDD must be strictly negative")
            self.assertGreaterEqual(m.mdd_pct, -100.0, f"{freq.value} MDD cannot exceed -100%")

    def test_after_tax_cagr_ordering_reflects_rebalancing_frequency(self) -> None:
        """
        Across the active rebalancing cycles (Weekly, Monthly, Quarterly, Semi-Annually),
        less frequent rebalancing yields higher after-tax compound CAGR due to lower friction
        and tax deferral.
        """
        res_w = self.sim.run_simulation(BacktestConfig(frequency=RebalanceFrequency.WEEKLY, tax_enabled=True))
        res_m = self.sim.run_simulation(BacktestConfig(frequency=RebalanceFrequency.MONTHLY, tax_enabled=True))
        res_q = self.sim.run_simulation(BacktestConfig(frequency=RebalanceFrequency.QUARTERLY, tax_enabled=True))
        res_s = self.sim.run_simulation(BacktestConfig(frequency=RebalanceFrequency.SEMI_ANNUALLY, tax_enabled=True))

        # Empirical after-tax CAGR check: Weekly (12.32%) <= Monthly (12.40%) <= Quarterly (12.66%) <= Semi-Annually (12.87%)
        self.assertLessEqual(res_w.metrics.cagr_after_tax, res_m.metrics.cagr_after_tax)
        self.assertLessEqual(res_m.metrics.cagr_after_tax, res_q.metrics.cagr_after_tax)
        self.assertLessEqual(res_q.metrics.cagr_after_tax, res_s.metrics.cagr_after_tax)

    def test_rebalance_records_count_monotonic_with_frequency(self) -> None:
        """The number of rebalance records must decrease as frequency horizon lengthens."""
        res_w = self.sim.run_simulation(BacktestConfig(frequency=RebalanceFrequency.WEEKLY, tax_enabled=False))
        res_m = self.sim.run_simulation(BacktestConfig(frequency=RebalanceFrequency.MONTHLY, tax_enabled=False))
        res_q = self.sim.run_simulation(BacktestConfig(frequency=RebalanceFrequency.QUARTERLY, tax_enabled=False))
        res_s = self.sim.run_simulation(BacktestConfig(frequency=RebalanceFrequency.SEMI_ANNUALLY, tax_enabled=False))
        res_a = self.sim.run_simulation(BacktestConfig(frequency=RebalanceFrequency.ANNUALLY, tax_enabled=False))

        n_w = len(res_w.rebalance_records)
        n_m = len(res_m.rebalance_records)
        n_q = len(res_q.rebalance_records)
        n_s = len(res_s.rebalance_records)
        n_a = len(res_a.rebalance_records)

        self.assertGreater(n_w, n_m)
        self.assertGreater(n_m, n_q)
        self.assertGreater(n_q, n_s)
        self.assertGreaterEqual(n_s, n_a)


class TestStrategyAFrictionAndTurnover(unittest.TestCase):
    """Stress testing fee (0.10%) and slippage (0.08%) mechanics."""

    def setUp(self) -> None:
        self.sim = StrategyASimulator()

    def test_fee_to_slippage_ratio_invariant(self) -> None:
        """Fee rate is 0.0010 and slippage rate is 0.0008; ratio of paid fees must be exactly 1.25."""
        for freq in [RebalanceFrequency.WEEKLY, RebalanceFrequency.MONTHLY, RebalanceFrequency.QUARTERLY]:
            res = self.sim.run_simulation(BacktestConfig(frequency=freq, fee_rate=0.0010, slippage_rate=0.0008))
            self.assertGreater(res.metrics.fee_paid, 0.0)
            self.assertGreater(res.metrics.slippage_paid, 0.0)
            ratio = res.metrics.fee_paid / res.metrics.slippage_paid
            self.assertAlmostEqual(ratio, 1.25, places=3)

    def test_zero_friction_yields_higher_or_equal_nav(self) -> None:
        """Zero fee and zero slippage backtest must produce higher final NAV than with friction."""
        cfg_friction = BacktestConfig(frequency=RebalanceFrequency.WEEKLY, fee_rate=0.0010, slippage_rate=0.0008, tax_enabled=False)
        cfg_zero = BacktestConfig(frequency=RebalanceFrequency.WEEKLY, fee_rate=0.0, slippage_rate=0.0, tax_enabled=False)

        res_friction = self.sim.run_simulation(cfg_friction)
        res_zero = self.sim.run_simulation(cfg_zero)

        self.assertGreaterEqual(res_zero.daily_nav[-1], res_friction.daily_nav[-1])
        self.assertGreaterEqual(res_zero.metrics.cagr_pct, res_friction.metrics.cagr_pct)
        self.assertEqual(res_zero.metrics.fee_paid, 0.0)
        self.assertEqual(res_zero.metrics.slippage_paid, 0.0)

    def test_extreme_friction_stability(self) -> None:
        """Even with punishing friction (5% fee + 5% slippage), simulation must not crash or go negative."""
        cfg_punish = BacktestConfig(frequency=RebalanceFrequency.MONTHLY, fee_rate=0.05, slippage_rate=0.05, tax_enabled=False)
        res_punish = self.sim.run_simulation(cfg_punish)

        for nav in res_punish.daily_nav:
            self.assertGreater(nav, 0.0, "NAV must remain strictly positive even under 10% round-trip friction")
            self.assertFalse(math.isnan(nav))


class TestStrategyACapitalGainsTaxModeling(unittest.TestCase):
    """Stress testing 22% tax drag, annual deduction, and deferral dynamics."""

    def setUp(self) -> None:
        self.sim = StrategyASimulator()

    def test_pre_tax_cagr_always_greater_or_equal_to_after_tax_cagr(self) -> None:
        """In every scenario, pre-tax CAGR must be >= after-tax CAGR."""
        for freq in RebalanceFrequency:
            res = self.sim.run_simulation(BacktestConfig(frequency=freq, tax_enabled=True))
            self.assertGreaterEqual(
                res.metrics.cagr_pre_tax,
                res.metrics.cagr_after_tax,
                f"{freq.value}: after-tax CAGR cannot exceed pre-tax CAGR"
            )
            self.assertGreaterEqual(res.metrics.tax_drag_pct, 0.0)

    def test_annual_tax_deduction_shield(self) -> None:
        """When total annual realized gain <= 2.5M KRW, tax paid for that year must be exactly 0.0."""
        # Test directly via BacktestConfig with huge annual deduction
        cfg = BacktestConfig(
            frequency=RebalanceFrequency.WEEKLY,
            tax_enabled=True,
            annual_tax_deduction=100_000_000_000.0,  # 100 Billion KRW deduction shields all gains
        )
        res = self.sim.run_simulation(cfg)
        self.assertEqual(res.metrics.total_tax_paid, 0.0)
        self.assertEqual(res.metrics.tax_drag_pct, 0.0)
        self.assertEqual(res.metrics.cagr_pre_tax, res.metrics.cagr_after_tax)

    def test_tax_drag_is_zero_when_tax_disabled(self) -> None:
        """When tax_enabled=False, total_tax_paid and tax_drag_pct must be exactly 0.0."""
        cfg = BacktestConfig(frequency=RebalanceFrequency.WEEKLY, tax_enabled=False)
        res = self.sim.run_simulation(cfg)
        self.assertEqual(res.metrics.total_tax_paid, 0.0)
        self.assertEqual(res.metrics.tax_drag_pct, 0.0)
        self.assertEqual(res.metrics.cagr_pre_tax, res.metrics.cagr_after_tax)


class TestStrategyASimplexInvariant(unittest.TestCase):
    """Stress testing 100% equity simplex constraint: w_cash == 0.0 and sum(w_i) == 1.0."""

    def setUp(self) -> None:
        self.sim = StrategyASimulator()

    def test_simplex_invariant_at_all_daily_timesteps(self) -> None:
        """Across all 6,350+ days in 25-year backtest, cash must be 0.0 and sum of equity weights == 1.0."""
        for freq in [RebalanceFrequency.WEEKLY, RebalanceFrequency.MONTHLY]:
            res = self.sim.run_simulation(BacktestConfig(frequency=freq, tax_enabled=True))
            for idx, weights in enumerate(res.holdings_history):
                # No cash asset allowed
                self.assertNotIn("cash", weights, f"Day {idx} contains 'cash'")
                self.assertNotIn("CASH", weights, f"Day {idx} contains 'CASH'")
                self.assertNotIn("USD", weights, f"Day {idx} contains 'USD'")
                self.assertNotIn("KRW", weights, f"Day {idx} contains 'KRW'")

                # Sum of weights must equal 1.0
                tot_w = sum(weights.values())
                self.assertAlmostEqual(tot_w, 1.0, places=3, msg=f"Day {idx} weights sum to {tot_w} != 1.0")

    def test_concentration_rules_strictly_satisfy_simplex(self) -> None:
        """Direct unit test of calculate_concentration_weights under all edge cases."""
        # 1. Zero candidates -> 100% benchmark
        w_empty = StrategyASimulator.calculate_concentration_weights([], benchmark_symbol="QQQ")
        self.assertEqual(w_empty, {"QQQ": 1.0})
        self.assertEqual(sum(w_empty.values()), 1.0)

        # 2. 1 TOP_PICK (score >= 88.0) -> 100% single winner
        c_top = make_dummy_candidate("TOP_STK", score=92.0, tier="TOP_PICK")
        w_single = StrategyASimulator.calculate_concentration_weights([c_top], benchmark_symbol="QQQ")
        self.assertEqual(w_single, {"TOP_STK": 1.0})
        self.assertEqual(sum(w_single.values()), 1.0)

        # 3. 1 Candidate with score 80.0 (75 <= score < 88) -> 50% candidate + 50% benchmark spillover
        c_mid = make_dummy_candidate("MID_STK", score=80.0, tier="STRONG_CANDIDATE")
        w_mid = StrategyASimulator.calculate_concentration_weights([c_mid], benchmark_symbol="QQQ")
        self.assertEqual(w_mid, {"MID_STK": 0.50, "QQQ": 0.50})
        self.assertEqual(sum(w_mid.values()), 1.0)

        # 4. 2 Qualified candidates -> 50% / 50% dual concentration
        c1 = make_dummy_candidate("STK_A", score=86.0)
        c2 = make_dummy_candidate("STK_B", score=82.0)
        w_dual = StrategyASimulator.calculate_concentration_weights([c1, c2], benchmark_symbol="QQQ")
        self.assertEqual(w_dual, {"STK_A": 0.50, "STK_B": 0.50})
        self.assertEqual(sum(w_dual.values()), 1.0)

        # 5. 5 Qualified candidates -> compressed strictly to top 2
        cands = [make_dummy_candidate(f"STK_{i}", score=76.0 + i * 3.0) for i in range(5)]
        w_multi = StrategyASimulator.calculate_concentration_weights(cands, benchmark_symbol="QQQ")
        self.assertEqual(len(w_multi), 2)
        self.assertEqual(sum(w_multi.values()), 1.0)
        self.assertIn("STK_4", w_multi)
        self.assertIn("STK_3", w_multi)


class TestStrategyAAsymmetricExitsPayoffMath(unittest.TestCase):
    """Stress testing mathematical precision of TP1 100% principal recovery and Stop Loss."""

    def test_tp1_recovers_exact_100_percent_principal(self) -> None:
        """
        When price doubles (2.0x entry), TP1 sells exactly 50% of position.
        Cash realized MUST equal 100% of initial principal invested.
        Remaining shares cost basis MUST become $0.00 (Risk-Free).
        """
        for init_cost in [1_000.0, 7_500.0, 100_000_000.0]:
            p_entry = 10.0
            sh = init_cost / p_entry
            pos = TurnaroundPosition(
                stock_id="TEST",
                entry_date="2024-01-01",
                entry_price=p_entry,
                current_price=p_entry,
                shares=sh,
                initial_shares=sh,
                initial_cost=init_cost,
                support_price=9.0,
                tp1_price=20.0,
                cost_basis=p_entry,
            )

            # Trigger TP1 at exactly 2.0x entry ($20.00)
            exit_dec = StrategyASimulator.check_position_exits(pos, current_price=20.0)

            self.assertEqual(exit_dec.action, "TP1_PARTIAL")
            self.assertEqual(exit_dec.shares_to_sell, sh * 0.50)
            self.assertEqual(exit_dec.cash_realized, init_cost, "Realized cash must exactly match initial principal")
            self.assertEqual(pos.shares, sh * 0.50)
            self.assertEqual(pos.cost_basis, 0.0, "Cost basis of runner must become 0.0")
            self.assertTrue(pos.tp1_executed)
            self.assertTrue(pos.is_risk_free)

    def test_stop_loss_truncates_downside_to_10_percent(self) -> None:
        """Stop-loss sells 100% of position when price drops to -10% from entry."""
        init_cost = 10_000.0
        p_entry = 100.0
        sh = init_cost / p_entry
        pos = TurnaroundPosition(
            stock_id="TEST",
            entry_date="2024-01-01",
            entry_price=p_entry,
            current_price=p_entry,
            shares=sh,
            initial_shares=sh,
            initial_cost=init_cost,
            support_price=95.0,
            tp1_price=200.0,
            cost_basis=p_entry,
        )

        exit_dec = StrategyASimulator.check_position_exits(pos, current_price=90.0)
        self.assertEqual(exit_dec.action, "STOP_LOSS_FULL")
        self.assertEqual(exit_dec.shares_to_sell, sh)
        self.assertEqual(pos.shares, 0.0)
        self.assertEqual(exit_dec.cash_realized, 9_000.0)
        self.assertEqual(exit_dec.realized_gain, -1_000.0)  # Exactly -10%


class TestStrategyASwitchingAndLockInvariants(unittest.TestCase):
    """Stress testing switching hurdles and reverse-switching defense locks."""

    def test_defense_lock_blocks_massive_score_gap(self) -> None:
        """Even a 30-point score gap is strictly BLOCKED if holding has D-Day <= 20 in safety margin."""
        pos = TurnaroundPosition(
            stock_id="CORE_HOLD",
            entry_date="2024-01-01",
            entry_price=10.0,
            current_price=10.5,
            shares=100.0,
            initial_shares=100.0,
            initial_cost=1000.0,
            support_price=9.5,
            tp1_price=20.0,
            composite_score=65.0,
            catalyst_d_day=15,  # <= 20 days: lock ACTIVE!
            fifty_two_week_low=9.5,
        )
        cand = make_dummy_candidate("SUPER_CAND", score=98.0, catalyst_d_day=60)

        eval_res = StrategyASimulator.evaluate_switching_hurdle(pos, cand)
        self.assertTrue(eval_res.is_reverse_warning_locked)
        self.assertFalse(eval_res.should_switch)
        self.assertIn("REVERSE_SWITCH_WARNING", eval_res.reason)

    def test_switch_allowed_when_d_day_exceeds_20(self) -> None:
        """When catalyst D-Day > 20 days, switching executes normally if hurdle is cleared."""
        pos = TurnaroundPosition(
            stock_id="CORE_HOLD",
            entry_date="2024-01-01",
            entry_price=10.0,
            current_price=10.5,
            shares=100.0,
            initial_shares=100.0,
            initial_cost=1000.0,
            support_price=9.5,
            tp1_price=20.0,
            composite_score=70.0,
            catalyst_d_day=35,  # > 20 days: lock INACTIVE!
            fifty_two_week_low=9.5,
        )
        cand = make_dummy_candidate("GOOD_CAND", score=86.0, catalyst_d_day=45)

        eval_res = StrategyASimulator.evaluate_switching_hurdle(pos, cand)
        self.assertFalse(eval_res.is_reverse_warning_locked)
        self.assertTrue(eval_res.should_switch)
        self.assertEqual(eval_res.score_gap, 16.0)


if __name__ == "__main__":
    unittest.main()
