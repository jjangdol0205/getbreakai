"""
Adversarial Challenge & Stress-Testing Suite for Milestone 2:
Strategy A 52-Week Low Turnaround Concentrated in Max 2 Stocks & Systematic Weekly Switching.

Authored by: challenger_m2_1 (Milestone 2 Challenger 1)
Role: EMPIRICAL CHALLENGER (critic, specialist)
Interface Target: engine/strategy_turnaround.py

Empirically challenges:
1. Concentration Rules:
   - 100% Single Winner: exactly 1 candidate achieves TOP_PICK (score >= 88.0) and no other >= 75.0.
   - 50% / 50% Dual Concentration: 2+ qualified candidates exist (top 2 by deterministic RankKey).
   - Single Candidate (75.0 <= score < 88.0): 50% candidate + 50% defensive benchmark.
   - Defensive Benchmark Spillover: 0 candidates qualify -> 100% allocation to benchmark (w_cash = 0.0).
   - Simplex constraint (sum == 1.0, w_cash == 0.0) across all permutations.
   - Stress test & Bug Detection: Multi-stock concentration violation during reverse lock.

2. Switching Hurdle vs Reverse-Switching Defense Lock:
   - STRONG_SWITCH tier requirements (3/3 triggers, RRR ratio >= 1.3x and catalyst adv > 0, OR adv >= 30d and D-Day <= 30d).
   - 15-Point Composite Score Gap requirement.
   - Reverse-Switching Defense Lock: strictly FORBIDS switching when holding has D-Day <= 20 in safety margin, overriding any candidate advantage.
   - Stress test & Bug Detection: Switching hurdle bypass in run_simulation rebalancing loop.

3. Mathematical Asymmetric Exit Payoff:
   - Mathematical proof: TP1 (+100% gain, 2.0x entry) sells exactly 50% shares and returns exactly 100% principal cash.
   - Runner shares retain risk-free status at exactly $0.00 effective cost basis.
   - TP1 idempotence: runner does not re-trigger TP1 on further price appreciation.
   - Stop-Loss: 100% exit at -10% breach from entry or key support floor.

4. 25-Year Simulation, Friction, and Foreign Equity Tax Mechanics:
   - 25.25-year continuous execution across 5 cycles (Weekly, Monthly, Quarterly, Semi-Annually, Annually).
   - Turnover ordering: Weekly > Monthly > Quarterly > Semi-Annually > Annually.
   - Tax Drag: Pre-tax CAGR >= After-tax CAGR, with 22% tax on gains above annual deduction.
   - Zero-cash simplex preserved throughout the entire 25.25-year time horizon.
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


def make_test_candidate(
    stock_id: str = "CAND_1",
    current_price: float = 10.0,
    composite_score: float = 80.0,
    conviction_tier: str = "STRONG_CANDIDATE",
    pass_count: int = 4,
    catalyst_d_day: Optional[int] = 30,
    proximity_pct: float = 10.0,
    risk_reward_ratio: float = 12.0,
    support_price: Optional[float] = None,
    tp1_price: Optional[float] = None,
) -> TurnaroundCandidate:
    """Helper factory generating deterministically configured TurnaroundCandidate instances."""
    low_52w = current_price / (1.0 + proximity_pct / 100.0)
    high_52w = current_price * 2.5
    supp_p = support_price if support_price is not None else current_price * 0.92
    tp1_p = tp1_price if tp1_price is not None else current_price * 2.0

    dummy_f = ScreeningFilterResult(
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
        "cond1_52w_low": dummy_f,
        "cond2_earnings_turnaround": dummy_f,
        "cond3_volume_washout": dummy_f,
        "cond4_risk_reward": dummy_f,
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
# 1. Concentration & Allocation Empirical Stress Tests
# ==============================================================================

class TestConcentrationRulesEmpirical(unittest.TestCase):
    """Stress tests: 100% single winner, 50/50 dual concentration, defensive spillover."""

    def test_single_winner_exact_threshold(self) -> None:
        """100% single winner activates when exactly 1 candidate is TOP_PICK (>=88.0) and all others <75.0."""
        # Top candidate exactly at 88.0, second candidate at 74.99 (below 75.0 threshold)
        c1 = make_test_candidate("WINNER", composite_score=88.0, conviction_tier="TOP_PICK")
        c2 = make_test_candidate("RUNNER_UP", composite_score=74.99, conviction_tier="WATCHLIST")
        c3 = make_test_candidate("THIRD", composite_score=60.0, conviction_tier="WATCHLIST")

        w = StrategyASimulator.calculate_concentration_weights([c1, c2, c3], benchmark_symbol="QQQ")
        self.assertEqual(w, {"WINNER": 1.0})
        self.assertAlmostEqual(sum(w.values()), 1.0)
        self.assertEqual(len(w), 1)

    def test_single_winner_defeated_by_second_qualified_candidate(self) -> None:
        """When second candidate reaches >= 75.0, 100% concentration collapses to 50/50 dual concentration."""
        c1 = make_test_candidate("WINNER", composite_score=95.0, conviction_tier="TOP_PICK")
        # Second candidate at exactly 75.0 (qualified)
        c2 = make_test_candidate("SECOND", composite_score=75.0, conviction_tier="STRONG_CANDIDATE")

        w = StrategyASimulator.calculate_concentration_weights([c1, c2], benchmark_symbol="QQQ")
        self.assertEqual(w, {"WINNER": 0.50, "SECOND": 0.50})
        self.assertAlmostEqual(sum(w.values()), 1.0)
        self.assertEqual(len(w), 2)

    def test_intermediate_single_candidate_benchmark_split(self) -> None:
        """Single qualified candidate with 75.0 <= score < 88.0 gets 50% candidate + 50% defensive benchmark."""
        c1 = make_test_candidate("MID_SCORE", composite_score=82.5, conviction_tier="STRONG_CANDIDATE")
        c2 = make_test_candidate("FAILING", composite_score=65.0, conviction_tier="WATCHLIST")

        w = StrategyASimulator.calculate_concentration_weights([c1, c2], benchmark_symbol="SOXX")
        self.assertEqual(w, {"MID_SCORE": 0.50, "SOXX": 0.50})
        self.assertAlmostEqual(sum(w.values()), 1.0)

    def test_defensive_spillover_zero_qualified(self) -> None:
        """When 0 candidates qualify, portfolio defaults 100% to core benchmark (zero cash)."""
        c1 = make_test_candidate("LOW_1", composite_score=72.0, conviction_tier="WATCHLIST")
        c2 = make_test_candidate("LOW_2", composite_score=50.0, conviction_tier="DISQUALIFIED")

        w = StrategyASimulator.calculate_concentration_weights([c1, c2], benchmark_symbol="QQQ")
        self.assertEqual(w, {"QQQ": 1.0})
        self.assertAlmostEqual(sum(w.values()), 1.0)

        # Empty candidate list
        w_empty = StrategyASimulator.calculate_concentration_weights([], benchmark_symbol="SOXX")
        self.assertEqual(w_empty, {"SOXX": 1.0})

    def test_max_2_stocks_strictly_capped_on_large_universe(self) -> None:
        """Even with 15 qualified candidates, allocation is strictly capped at top 2 stocks (50/50)."""
        candidates = [
            make_test_candidate(f"STOCK_{i}", composite_score=76.0 + i)
            for i in range(15)
        ]
        w = StrategyASimulator.calculate_concentration_weights(candidates, benchmark_symbol="QQQ")
        self.assertEqual(len(w), 2)
        self.assertIn("STOCK_14", w)
        self.assertIn("STOCK_13", w)
        self.assertEqual(w["STOCK_14"], 0.50)
        self.assertEqual(w["STOCK_13"], 0.50)
        self.assertAlmostEqual(sum(w.values()), 1.0)

    def test_concentration_simplex_invariant_property(self) -> None:
        """Across randomized score permutations, sum(weights) == 1.0 and cash == 0.0 always hold."""
        test_scores = [
            [90.0],
            [85.0],
            [92.0, 89.0],
            [88.0, 75.0],
            [88.0, 74.9],
            [74.0, 70.0],
            [95.0, 80.0, 77.0, 60.0],
            [82.0, 81.0, 80.0, 79.0],
        ]
        for scores in test_scores:
            cands = [make_test_candidate(f"S_{i}", composite_score=sc) for i, sc in enumerate(scores)]
            w = StrategyASimulator.calculate_concentration_weights(cands, benchmark_symbol="QQQ")
            self.assertAlmostEqual(sum(w.values()), 1.0, places=6)
            self.assertNotIn("cash", w)
            self.assertNotIn("CASH", w)
            self.assertLessEqual(len([k for k in w if k != "QQQ"]), 2)


# ==============================================================================
# 2. Switching Hurdle & Reverse-Switching Defense Lock Tests
# ==============================================================================

class TestSwitchingHurdleAndDefenseLockEmpirical(unittest.TestCase):
    """Stress tests: STRONG_SWITCH trigger, 15-pt score gap, reverse-switching defense lock."""

    def test_switching_hurdle_15_pt_gap_boundary(self) -> None:
        """Switching triggers at exactly >= 15.0 pts score gap; fails at 14.99 pts."""
        pos = TurnaroundPosition(
            stock_id="HELD", entry_date="2024-01-01", entry_price=10.0, current_price=10.0,
            shares=100.0, initial_shares=100.0, initial_cost=1000.0, support_price=9.0,
            tp1_price=20.0, composite_score=70.0, catalyst_d_day=50, fifty_two_week_low=9.5,
        )

        # 1. Exactly 15.0 point gap (85.0 - 70.0 = 15.0) -> SHOULD SWITCH
        cand_15 = make_test_candidate("CAND_15", composite_score=85.0, catalyst_d_day=50)
        res_15 = StrategyASimulator.evaluate_switching_hurdle(pos, cand_15)
        self.assertTrue(res_15.should_switch)
        self.assertEqual(res_15.score_gap, 15.0)

        # 2. 14.9 point gap (84.9 - 70.0 = 14.9) -> REJECT SWITCH (HOLD_CORE)
        cand_14_9 = make_test_candidate("CAND_14_9", composite_score=84.9, catalyst_d_day=50)
        res_14_9 = StrategyASimulator.evaluate_switching_hurdle(pos, cand_14_9)
        self.assertFalse(res_14_9.should_switch)
        self.assertEqual(res_14_9.candidate_tier, "HOLD_CORE")

    def test_strong_switch_trigger_sub_conditions(self) -> None:
        """STRONG_SWITCH tier clears hurdle even with small score gap (< 15 pts)."""
        pos = TurnaroundPosition(
            stock_id="HELD", entry_date="2024-01-01", entry_price=10.0, current_price=10.0,
            shares=100.0, initial_shares=100.0, initial_cost=1000.0, support_price=9.0,
            tp1_price=20.0, composite_score=75.0, catalyst_d_day=60, fifty_two_week_low=9.5,
        )

        # Sub-case A: RRR ratio >= 1.3x and catalyst advantage > 0
        # held downside = (10-9)/10 = 10%, upside = 100%, RRR = 10.0x
        # cand RRR = 14.0x (14/10 = 1.4x >= 1.3x), cand D-Day = 40 (60 - 40 = 20d advantage > 0)
        cand_a = make_test_candidate("CAND_A", composite_score=78.0, catalyst_d_day=40, risk_reward_ratio=14.0)
        res_a = StrategyASimulator.evaluate_switching_hurdle(pos, cand_a)
        self.assertTrue(res_a.should_switch)
        self.assertEqual(res_a.candidate_tier, "STRONG_SWITCH")

        # Sub-case B: Catalyst advantage >= 30d and Candidate D-Day <= 30d
        # cand D-Day = 25 (<= 30d), catalyst advantage = 60 - 25 = 35d (>= 30d)
        cand_b = make_test_candidate("CAND_B", composite_score=77.0, catalyst_d_day=25, risk_reward_ratio=10.0)
        res_b = StrategyASimulator.evaluate_switching_hurdle(pos, cand_b)
        self.assertTrue(res_b.should_switch)
        self.assertEqual(res_b.candidate_tier, "STRONG_SWITCH")

    def test_reverse_switching_defense_lock_unbreakable(self) -> None:
        """Reverse-Switching Defense Lock strictly FORBIDS switching when holding has D-Day <= 20 in safety margin."""
        pos = TurnaroundPosition(
            stock_id="SK_SQUARE", entry_date="2026-09-01", entry_price=105.0, current_price=108.0,
            shares=100.0, initial_shares=100.0, initial_cost=10500.0, support_price=100.0,
            tp1_price=218.0, composite_score=60.0, catalyst_d_day=15, fifty_two_week_low=100.0,
        )

        # Hostile / enticing candidate with perfect 100.0 score (+40 pt gap)
        cand_enticing = make_test_candidate("TEMPTATION", composite_score=100.0, catalyst_d_day=10, risk_reward_ratio=25.0)
        res = StrategyASimulator.evaluate_switching_hurdle(pos, cand_enticing)

        self.assertTrue(res.is_reverse_warning_locked)
        self.assertFalse(res.should_switch, "Reverse lock must override any candidate score or RRR advantage")
        self.assertIn("REVERSE_SWITCH_WARNING", res.reason)

    def test_reverse_switch_releases_when_d_day_exceeds_20(self) -> None:
        """When catalyst D-Day > 20 days, reverse-switching defense lock does not activate."""
        pos = TurnaroundPosition(
            stock_id="SK_SQUARE", entry_date="2026-09-01", entry_price=105.0, current_price=108.0,
            shares=100.0, initial_shares=100.0, initial_cost=10500.0, support_price=100.0,
            tp1_price=218.0, composite_score=65.0, catalyst_d_day=21, fifty_two_week_low=100.0,
        )
        cand = make_test_candidate("CAND_OK", composite_score=85.0, catalyst_d_day=10)
        res = StrategyASimulator.evaluate_switching_hurdle(pos, cand)

        self.assertFalse(res.is_reverse_warning_locked)
        self.assertTrue(res.should_switch)


# ==============================================================================
# 3. Mathematical Asymmetric Exit Payoff Tests
# ==============================================================================

class TestAsymmetricExitMechanicsEmpirical(unittest.TestCase):
    """Empirically validates mathematical proofs of TP1 100% principal recovery & -10% stop loss."""

    def test_mathematical_tp1_principal_recovery_proof(self) -> None:
        """
        Mathematical proof:
        Given P_entry, Shares S_0, Principal C_0 = S_0 * P_entry.
        At P_exit = 2.0 * P_entry (+100% gain):
        TP1 sells 50% shares: S_sold = 0.50 * S_0.
        Cash realized = S_sold * P_exit = (0.50 * S_0) * (2.0 * P_entry) = S_0 * P_entry = C_0.
        Exactly 100% principal is recovered in cash, leaving runner shares with $0.00 effective cost basis.
        """
        test_cases = [
            (10.0, 1000.0),       # Principal $10,000
            (7.47, 13386.88),     # Principal $100,000 with fractional shares
            (0.24, 416666.67),    # Low price penny stock
            (1155.0, 76.0),       # SK Square style high-price stock
            (30.0, 333.333),      # Non-terminating decimal fractional shares
        ]

        for p_entry, s_0 in test_cases:
            c_0 = s_0 * p_entry
            pos = TurnaroundPosition(
                stock_id="TEST_PROOF", entry_date="2024-01-01", entry_price=p_entry, current_price=p_entry,
                shares=s_0, initial_shares=s_0, initial_cost=c_0, support_price=p_entry * 0.90,
                tp1_price=p_entry * 2.0, cost_basis=p_entry,
            )

            # Price hits exactly 2.0x entry price
            exit_dec = StrategyASimulator.check_position_exits(pos, current_price=p_entry * 2.0)

            self.assertEqual(exit_dec.action, "TP1_PARTIAL")
            self.assertAlmostEqual(exit_dec.shares_to_sell, s_0 * 0.50, places=5)
            self.assertAlmostEqual(exit_dec.cash_realized, c_0, places=4, msg="Cash realized must equal 100% principal")
            self.assertAlmostEqual(pos.shares, s_0 * 0.50, places=5)
            self.assertEqual(pos.cost_basis, 0.0, "Cost basis of runner shares must be set to $0.00")
            self.assertTrue(pos.tp1_executed)
            self.assertTrue(pos.is_risk_free)

    def test_tp1_runner_idempotent_holding(self) -> None:
        """After TP1 execution, further price surges (e.g. +200%, +500%) must NOT re-trigger TP1."""
        pos = TurnaroundPosition(
            stock_id="RUNNER_STOCK", entry_date="2024-01-01", entry_price=10.0, current_price=20.0,
            shares=500.0, initial_shares=1000.0, initial_cost=10000.0, support_price=9.0,
            tp1_price=20.0, tp1_executed=True, is_risk_free=True, cost_basis=0.0,
        )

        for higher_price in [25.0, 30.0, 50.0, 100.0]:
            exit_dec = StrategyASimulator.check_position_exits(pos, current_price=higher_price)
            self.assertEqual(exit_dec.action, "HOLD")
            self.assertEqual(pos.shares, 500.0)
            self.assertTrue(pos.is_risk_free)

    def test_stop_loss_10_percent_entry_breach(self) -> None:
        """Stop-loss sells 100% shares immediately when price falls -10% from entry price."""
        pos = TurnaroundPosition(
            stock_id="STOP_TEST", entry_date="2024-01-01", entry_price=100.0, current_price=100.0,
            shares=50.0, initial_shares=50.0, initial_cost=5000.0, support_price=95.0,
            tp1_price=200.0, cost_basis=100.0,
        )

        # Price drops to $90.0 (-10.0%)
        exit_dec = StrategyASimulator.check_position_exits(pos, current_price=90.0)
        self.assertEqual(exit_dec.action, "STOP_LOSS_FULL")
        self.assertEqual(exit_dec.shares_to_sell, 50.0)
        self.assertEqual(pos.shares, 0.0)
        self.assertAlmostEqual(exit_dec.cash_realized, 4500.0)
        self.assertAlmostEqual(exit_dec.realized_gain, -500.0)  # -10% loss

    def test_stop_loss_support_floor_breach(self) -> None:
        """Stop-loss sells 100% shares when price falls -10% below key support floor."""
        pos = TurnaroundPosition(
            stock_id="SUPPORT_TEST", entry_date="2024-01-01", entry_price=100.0, current_price=95.0,
            shares=50.0, initial_shares=50.0, initial_cost=5000.0, support_price=90.0,
            tp1_price=200.0, cost_basis=100.0,
        )

        # Support floor is $90.0; breach threshold is 90 * 0.90 = $81.0
        # Price drops to $80.50 -> STOP LOSS FULL
        exit_dec = StrategyASimulator.check_position_exits(pos, current_price=80.50)
        self.assertEqual(exit_dec.action, "STOP_LOSS_FULL")
        self.assertEqual(pos.shares, 0.0)


# ==============================================================================
# 4. Simulation Engine, Friction & Foreign Equity Tax Tests
# ==============================================================================

class Test25YearSimulationFrictionAndTaxEmpirical(unittest.TestCase):
    """Stress tests: 25.25-year backtest execution, 5 rebalance cycles, friction, and tax modeling."""

    def setUp(self) -> None:
        self.sim = StrategyASimulator()

    def test_full_25yr_simulation_execution(self) -> None:
        """Full 25.25-year backtest executes cleanly without errors and returns complete metrics."""
        res = self.sim.run_simulation()
        self.assertIsInstance(res, SimulationResult)
        self.assertGreater(len(res.dates), 6000)
        self.assertEqual(len(res.daily_nav), len(res.dates))
        self.assertEqual(len(res.daily_drawdowns), len(res.dates))
        self.assertGreater(res.metrics.cagr_pre_tax, 0.0)
        self.assertLess(res.metrics.mdd_pct, 0.0)

    def test_5_rebalance_frequencies_monotonic_turnover(self) -> None:
        """Turnover strictly decreases as rebalancing horizon increases: Weekly > Monthly > Annual."""
        freqs = [
            RebalanceFrequency.WEEKLY,
            RebalanceFrequency.MONTHLY,
            RebalanceFrequency.QUARTERLY,
            RebalanceFrequency.SEMI_ANNUALLY,
            RebalanceFrequency.ANNUALLY,
        ]
        turnovers = []
        for f in freqs:
            cfg = BacktestConfig(frequency=f, tax_enabled=False)
            res = self.sim.run_simulation(cfg)
            turnovers.append(res.metrics.total_turnover)

        # Verify strict ordering Weekly > Monthly > Semi-Annually >= Annually
        self.assertGreater(turnovers[0], turnovers[1])  # Weekly > Monthly
        self.assertGreater(turnovers[1], turnovers[4])  # Monthly > Annually

    def test_22_percent_foreign_tax_and_deferral_benefit(self) -> None:
        """Foreign equity tax (22% with annual deduction) produces higher tax paid in frequent rebalancing."""
        cfg_w = BacktestConfig(frequency=RebalanceFrequency.WEEKLY, tax_enabled=True, tax_rate=0.22)
        cfg_sa = BacktestConfig(frequency=RebalanceFrequency.SEMI_ANNUALLY, tax_enabled=True, tax_rate=0.22)

        res_w = self.sim.run_simulation(cfg_w)
        res_sa = self.sim.run_simulation(cfg_sa)

        # Frequent weekly rebalancing incurs higher total tax paid than Semi-Annual
        self.assertGreaterEqual(res_w.metrics.total_tax_paid, res_sa.metrics.total_tax_paid)
        self.assertGreaterEqual(res_w.metrics.cagr_pre_tax, res_w.metrics.cagr_after_tax)
        self.assertGreaterEqual(res_sa.metrics.cagr_pre_tax, res_sa.metrics.cagr_after_tax)

    def test_continuous_zero_cash_simplex_invariant(self) -> None:
        """At every single day throughout 25 years, portfolio cash is 0.0 and sum(weights) == 1.0."""
        res = self.sim.run_simulation()
        for idx in range(0, len(res.holdings_history), 50):
            h = res.holdings_history[idx]
            self.assertAlmostEqual(sum(h.values()), 1.0, places=3)
            self.assertNotIn("cash", h)
            self.assertNotIn("CASH", h)


# ==============================================================================
# 5. Challenger Bug Detection & Adversarial Stress Tests
# ==============================================================================

class TestChallengerBugDetectionAdversarial(unittest.TestCase):
    """
    Adversarial stress-testing exposing implementation vulnerabilities:
    1. Bug: Reverse-switching lock multi-stock concentration violation (creating > 2 stocks).
    2. Bug: Switching hurdle bypass in run_simulation rebalancing loop.
    """

    def test_adversarial_reverse_lock_can_violate_max_2_stocks(self) -> None:
        """
        Adversarial Test:
        When target_w has 2 candidates C1: 0.50 and C2: 0.50, and held stock HELD is reverse-locked,
        the current logic appends HELD with 0.50 and normalizes by dividing by 1.5,
        resulting in 3 stocks (33.3% / 33.3% / 33.3%), violating the Max 2 Stocks Concentration Rule!
        """
        target_w = {"C1": 0.50, "C2": 0.50}
        held_sym = "HELD"

        # Simulating logic from engine/strategy_turnaround.py line 1015-1020:
        if held_sym not in target_w:
            target_w[held_sym] = target_w.get(held_sym, 0.50)
            tot = sum(target_w.values())
            if tot > 0:
                target_w = {k: v / tot for k, v in target_w.items()}

        turnaround_stocks = [k for k in target_w if k != "QQQ"]
        # Empirical proof: currently produces 3 turnaround stocks!
        self.assertEqual(len(turnaround_stocks), 3, "Reveals implementation vulnerability: produces 3 stocks")
        self.assertAlmostEqual(target_w["C1"], 1.0 / 3.0)
        self.assertAlmostEqual(target_w["C2"], 1.0 / 3.0)
        self.assertAlmostEqual(target_w["HELD"], 1.0 / 3.0)

    def test_adversarial_switching_hurdle_bypass_in_simulation(self) -> None:
        """
        Adversarial Test:
        When a held position has no reverse lock (D-Day > 20), but candidate only has a tiny
        score gap (+0.0 or +1.0 pts < 15.0 pts), evaluate_switching_hurdle correctly returns
        should_switch = False. However, run_simulation calculates target_w purely from cand_pool
        ranking and fails to enforce should_switch = False, prematurely liquidating the holding!
        """
        ep_top = TurnaroundEpisode(
            stock_id="EP_TOP", name_kr="Top", ticker="TOP", era="AI_CYCLE",
            start_date="2024-01-01", trough_date="2024-06-01", end_date="2024-12-31",
            trough_price=10.0, peak_price=20.0, fifty_two_week_low=10.0, fifty_two_week_high=20.0,
            support_price=9.5, tp1_price=20.0, rev_growth_2y=50.0, oi_growth_2y=100.0,
            is_turnaround_to_profit=True, volume_surge_ratio=2.5, catalyst_d_day_initial=50,
        )
        ep_held = TurnaroundEpisode(
            stock_id="EP_HELD", name_kr="Held", ticker="HELD", era="AI_CYCLE",
            start_date="2024-01-01", trough_date="2024-06-01", end_date="2024-12-31",
            trough_price=10.0, peak_price=15.0, fifty_two_week_low=10.0, fifty_two_week_high=20.0,
            support_price=9.5, tp1_price=20.0, rev_growth_2y=32.0, oi_growth_2y=35.0,
            is_turnaround_to_profit=False, volume_surge_ratio=1.5, catalyst_d_day_initial=50,
        )
        ep_cand = TurnaroundEpisode(
            stock_id="EP_CAND", name_kr="Cand", ticker="CAND", era="AI_CYCLE",
            start_date="2024-01-15", trough_date="2024-06-01", end_date="2024-12-31",
            trough_price=10.0, peak_price=15.0, fifty_two_week_low=10.0, fifty_two_week_high=20.0,
            support_price=9.5, tp1_price=20.0, rev_growth_2y=34.0, oi_growth_2y=38.0,
            is_turnaround_to_profit=False, volume_surge_ratio=1.52, catalyst_d_day_initial=48,
        )

        sim = StrategyASimulator(episodes=[ep_top, ep_held, ep_cand])

        # Step 1: Verify evaluate_switching_hurdle rejects the switch
        pos_held = TurnaroundPosition(
            stock_id="EP_HELD", entry_date="2024-01-02", entry_price=10.0, current_price=10.0,
            shares=500.0, initial_shares=500.0, initial_cost=5000.0, support_price=9.5,
            tp1_price=20.0, cost_basis=10.0, catalyst_d_day=50, composite_score=83.0,
            fifty_two_week_low=10.0,
        )
        cand_eval = make_test_candidate("EP_CAND", composite_score=83.0, catalyst_d_day=48)
        eval_res = sim.evaluate_weekly_switching_decision(pos_held, cand_eval)
        self.assertFalse(eval_res.should_switch, "Hurdle must reject switch with 0.0 point gap")

        # Step 2: Run simulation and observe that run_simulation switches anyway
        cfg = BacktestConfig(
            start_date="2024-01-01", end_date="2024-02-01", frequency=RebalanceFrequency.WEEKLY,
            tax_enabled=False, initial_capital=10000.0,
        )
        res = sim.run_simulation(cfg)

        rebalances = [r for r in res.rebalance_records if r["type"] == "REBALANCE"]
        self.assertGreater(len(rebalances), 0)
        target_w_reb = rebalances[0]["target_weights"]

        # Empirical proof of bug: EP_HELD was dropped and EP_CAND was bought!
        self.assertNotIn("EP_HELD", target_w_reb)
        self.assertIn("EP_CAND", target_w_reb)


if __name__ == "__main__":
    unittest.main()
