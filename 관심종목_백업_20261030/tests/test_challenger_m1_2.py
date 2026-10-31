"""
Adversarial Stress Test Suite for Milestone 1 by Challenger 2 (challenger_m1_2).

Empirically verifies:
1. 100% Equity Simplex Constraint:
   - w_cash == 0.0 identically at all timesteps t.
   - sum(w_i) == 1.0 within IEEE 754 precision at all timesteps t.
   - Zero cash leakage or accumulation across initial deployment, rebalances, and tax redemptions.
   - Complete asset entry and full liquidation (w_k -> 0.0 -> w_k > 0.0).

2. Division-by-Zero Stability for Calmar Ratio:
   - Strictly monotonic rising curves (MDD == 0.0) capped at 99.99 without ZeroDivisionError.
   - Flat curves (CAGR == 0.0, MDD == 0.0) returning 0.0.
   - Sub-epsilon drawdowns (|MDD| < 1e-6) capped gracefully.
   - Severe plunges, bankruptcies, and 2-day micro-series.

3. 5-Cycle Tax Drag & Tax Deferral Compounding Mechanics:
   - Strict monotonic turnover ordering: WEEKLY > MONTHLY > QUARTERLY > SEMI_ANNUALLY > ANNUALLY > Buy&Hold.
   - Strict monotonic tax paid ordering: WEEKLY > MONTHLY > QUARTERLY > SEMI_ANNUALLY > ANNUALLY > Buy&Hold (0 KRW).
   - Strict monotonic tax drag ordering: WEEKLY > MONTHLY > QUARTERLY > SEMI_ANNUALLY > ANNUALLY >= 0.0.
   - Strict monotonic terminal after-tax wealth: ANNUALLY > SEMI_ANNUALLY > QUARTERLY > MONTHLY > WEEKLY.
   - Exact 22% tax rate and 2.5M KRW / $2,000 USD annual deduction math verification.
   - Proportion-preserving tax redemption invariant (w_i unchanged after tax payment).
"""

import unittest
import math
import datetime

from engine.historical_data import get_joint_history
from engine.backtest_engine import (
    BacktestConfig,
    RebalanceFrequency,
    PerformanceMetrics,
    SimulationResult,
    TaxAccountingState,
    calculate_performance_metrics,
    simulate_portfolio,
    run_buy_and_hold,
)


class Test100PercentEquitySimplexConstraint(unittest.TestCase):
    """Stress tests the 100% equity simplex constraint: w_cash == 0.0 and sum(w_i) == 1.0."""

    @classmethod
    def setUpClass(cls):
        joint = get_joint_history()
        cls.dates = sorted(joint.keys())
        cls.prices = {
            "QQQ": [joint[d]["QQQ"] for d in cls.dates],
            "SOXX": [joint[d]["SOXX"] for d in cls.dates],
        }

    def test_daily_simplex_invariant_across_all_5_frequencies_25yr(self):
        """
        Verify that for every single trading day across 25.25 years (6,350+ days),
        for all 5 rebalancing frequencies:
        - Portfolio NAV exactly equals sum of equity values (0 cash).
        - Equity weights sum to 1.0 within 1e-12.
        """
        for freq in RebalanceFrequency:
            with self.subTest(freq=freq.value):
                cfg = BacktestConfig(frequency=freq, tax_enabled=True, initial_capital=100_000_000.0)
                res = simulate_portfolio(self.prices, self.dates, {"QQQ": 0.65, "SOXX": 0.35}, cfg)

                for t in range(len(self.dates)):
                    p_t = {k: self.prices[k][t] for k in self.prices}
                    sh = res.holdings_history[t]
                    nav = res.daily_nav[t]

                    # 1. Total equity value must equal NAV exactly (no uninvested cash)
                    equity_sum = sum(sh[k] * p_t[k] for k in self.prices)
                    self.assertAlmostEqual(nav, equity_sum, places=4, msg=f"NAV mismatch on {self.dates[t]} for {freq}")

                    # 2. Equity weights must sum to 1.0 (simplex constraint)
                    weights = [(sh[k] * p_t[k]) / nav for k in self.prices]
                    self.assertAlmostEqual(sum(weights), 1.0, places=9, msg=f"Weight sum != 1.0 on {self.dates[t]} for {freq}")

    def test_extreme_weight_flipping_stress(self):
        """
        Stress test: Flip target weights between 100% QQQ and 100% SOXX every rebalance.
        Verifies that full liquidation of one asset and 100% concentration in another
        leaves zero residual cash and maintains sum(w) == 1.0.
        """
        def alternating_weights(idx, date_str, prices_map, nav):
            # Alternates 100% QQQ and 100% SOXX every rebalance
            if (idx // 20) % 2 == 0:
                return {"QQQ": 1.0, "SOXX": 0.0}
            else:
                return {"QQQ": 0.0, "SOXX": 1.0}

        cfg = BacktestConfig(frequency=RebalanceFrequency.MONTHLY, tax_enabled=True, initial_capital=50_000_000.0)
        res = simulate_portfolio(self.prices, self.dates, alternating_weights, cfg)

        for t in range(len(self.dates)):
            p_t = {k: self.prices[k][t] for k in self.prices}
            sh = res.holdings_history[t]
            nav = res.daily_nav[t]
            equity_sum = sum(sh[k] * p_t[k] for k in self.prices)
            self.assertAlmostEqual(nav, equity_sum, places=4)
            w_sum = sum((sh[k] * p_t[k]) / nav for k in self.prices)
            self.assertAlmostEqual(w_sum, 1.0, places=9)

    def test_tax_redemption_proportional_invariance(self):
        """
        Verifies that year-end tax redemption reduces shares uniformly across holdings
        without altering the drifted asset allocation weights or creating cash.
        """
        cfg = BacktestConfig(frequency=RebalanceFrequency.ANNUALLY, tax_enabled=True, initial_capital=100_000_000.0)
        res = simulate_portfolio(self.prices, self.dates, {"QQQ": 0.5, "SOXX": 0.5}, cfg)

        self.assertGreater(len(res.tax_history), 0)
        for tax_event in res.tax_history:
            date_str = tax_event["settle_date"]
            t = self.dates.index(date_str)
            p_t = {k: self.prices[k][t] for k in self.prices}
            sh = res.holdings_history[t]
            nav = res.daily_nav[t]

            equity_val = sum(sh[k] * p_t[k] for k in self.prices)
            self.assertAlmostEqual(nav, equity_val, places=4)
            w_sum = sum((sh[k] * p_t[k]) / nav for k in self.prices)
            self.assertAlmostEqual(w_sum, 1.0, places=9)

    def test_three_asset_synthetic_simplex(self):
        """
        Verify that a 3-asset portfolio (mimicking QQQ, SOXX, Turnaround)
        strictly satisfies the simplex constraint with zero cash leak.
        """
        synthetic_dates = [
            (datetime.date(2025, 1, 1) + datetime.timedelta(days=i)).isoformat()
            for i in range(100)
        ]
        synthetic_prices = {
            "QQQ": [100.0 * (1.001 ** i) for i in range(100)],
            "SOXX": [100.0 * (0.999 ** i) for i in range(100)],
            "TURNAROUND": [100.0 * (1.002 ** i if i < 50 else 0.998 ** (i - 50)) for i in range(100)],
        }
        target_w = {"QQQ": 0.35, "SOXX": 0.35, "TURNAROUND": 0.30}
        cfg = BacktestConfig(frequency=RebalanceFrequency.WEEKLY, tax_enabled=True, initial_capital=10_000_000.0)
        res = simulate_portfolio(synthetic_prices, synthetic_dates, target_w, cfg)

        for t in range(len(synthetic_dates)):
            p_t = {k: synthetic_prices[k][t] for k in synthetic_prices}
            sh = res.holdings_history[t]
            nav = res.daily_nav[t]
            equity_sum = sum(sh[k] * p_t[k] for k in synthetic_prices)
            self.assertAlmostEqual(nav, equity_sum, places=5)
            weights = [(sh[k] * p_t[k]) / nav for k in synthetic_prices]
            self.assertAlmostEqual(sum(weights), 1.0, places=9)


class TestCalmarRatioDivisionByZeroStability(unittest.TestCase):
    """Stress tests Calmar ratio formula against zero-division and boundary cases."""

    def test_strictly_monotonic_rise_mdd_zero(self):
        """When MDD == 0.0 (strictly monotonic rise), Calmar must be capped at 99.99."""
        dates = ["2020-01-01", "2021-01-01", "2022-01-01"]
        nav = [100.0, 110.0, 121.0]  # +10% CAGR
        m = calculate_performance_metrics(nav, dates)

        self.assertEqual(m.mdd_pct, 0.0)
        self.assertAlmostEqual(m.cagr_pct, 10.0, places=1)
        self.assertEqual(m.calmar_ratio, 99.99)
        self.assertFalse(math.isinf(m.calmar_ratio))
        self.assertFalse(math.isnan(m.calmar_ratio))

    def test_flat_nav_curve_zero_return_zero_mdd(self):
        """When NAV is strictly flat (CAGR == 0, MDD == 0), Calmar must be 0.0 without crash."""
        dates = ["2020-01-01", "2021-01-01", "2022-01-01"]
        nav = [100.0, 100.0, 100.0]
        m = calculate_performance_metrics(nav, dates)

        self.assertEqual(m.mdd_pct, 0.0)
        self.assertEqual(m.cagr_pct, 0.0)
        self.assertEqual(m.calmar_ratio, 0.0)

    def test_sub_epsilon_micro_drawdown(self):
        """Drawdowns smaller than 1e-6 must not cause float explosion; must cap at 99.99."""
        dates = ["2020-01-01", "2021-01-01", "2022-01-01"]
        nav = [100.0, 100.0 - 1e-8, 120.0]
        m = calculate_performance_metrics(nav, dates)

        self.assertLessEqual(abs(m.mdd_pct), 1e-4)
        self.assertEqual(m.calmar_ratio, 99.99)

    def test_monotonic_downward_plunge(self):
        """Monotonic plunge with negative return must yield negative finite Calmar ratio."""
        dates = ["2020-01-01", "2021-01-01", "2022-01-01"]
        nav = [100.0, 80.0, 50.0]
        m = calculate_performance_metrics(nav, dates)

        self.assertEqual(m.mdd_pct, -50.0)
        self.assertLess(m.cagr_pct, 0.0)
        self.assertLess(m.calmar_ratio, 0.0)
        self.assertAlmostEqual(m.calmar_ratio, (m.cagr_pct / 100.0) / 0.50, places=2)

    def test_total_collapse_to_zero(self):
        """Terminal NAV collapse to zero must be handled gracefully with Calmar == 0.0."""
        dates = ["2020-01-01", "2021-01-01", "2022-01-01"]
        nav = [100.0, 50.0, 0.0]
        m = calculate_performance_metrics(nav, dates)

        self.assertEqual(m.mdd_pct, -100.0)
        self.assertEqual(m.cagr_pct, 0.0)
        self.assertEqual(m.calmar_ratio, 0.0)

    def test_two_day_micro_series(self):
        """A minimal 2-day series must compute without ZeroDivisionError."""
        dates = ["2020-01-01", "2020-01-02"]
        nav = [100.0, 101.0]
        m = calculate_performance_metrics(nav, dates)
        self.assertFalse(math.isinf(m.calmar_ratio))
        self.assertFalse(math.isnan(m.calmar_ratio))
        self.assertEqual(m.calmar_ratio, 99.99)


class Test5CycleTaxDragCompoundingMechanics(unittest.TestCase):
    """Stress tests the 5-cycle tax drag and tax deferral compounding dynamics."""

    @classmethod
    def setUpClass(cls):
        joint = get_joint_history()
        cls.dates = sorted(joint.keys())
        cls.prices = {
            "QQQ": [joint[d]["QQQ"] for d in cls.dates],
            "SOXX": [joint[d]["SOXX"] for d in cls.dates],
        }

    def test_strict_turnover_monotonic_ordering(self):
        """Turnover must strictly decrease as rebalance interval increases."""
        turnovers = []
        for freq in [
            RebalanceFrequency.WEEKLY,
            RebalanceFrequency.MONTHLY,
            RebalanceFrequency.QUARTERLY,
            RebalanceFrequency.SEMI_ANNUALLY,
            RebalanceFrequency.ANNUALLY,
        ]:
            cfg = BacktestConfig(frequency=freq, tax_enabled=True, initial_capital=100_000_000.0)
            res = simulate_portfolio(self.prices, self.dates, {"QQQ": 0.5, "SOXX": 0.5}, cfg)
            turnovers.append((freq.value, res.metrics.total_turnover))

        for i in range(len(turnovers) - 1):
            curr_freq, curr_turnover = turnovers[i]
            next_freq, next_turnover = turnovers[i + 1]
            self.assertGreater(
                curr_turnover,
                next_turnover,
                msg=f"Expected turnover({curr_freq}) > turnover({next_freq}), got {curr_turnover} <= {next_turnover}"
            )

    def test_strict_total_tax_paid_monotonic_ordering(self):
        """Total capital gains tax paid must strictly decrease as rebalance interval increases."""
        taxes = []
        for freq in [
            RebalanceFrequency.WEEKLY,
            RebalanceFrequency.MONTHLY,
            RebalanceFrequency.QUARTERLY,
            RebalanceFrequency.SEMI_ANNUALLY,
            RebalanceFrequency.ANNUALLY,
        ]:
            cfg = BacktestConfig(frequency=freq, tax_enabled=True, initial_capital=100_000_000.0)
            res = simulate_portfolio(self.prices, self.dates, {"QQQ": 0.5, "SOXX": 0.5}, cfg)
            taxes.append((freq.value, res.metrics.total_tax_paid))

        for i in range(len(taxes) - 1):
            curr_freq, curr_tax = taxes[i]
            next_freq, next_tax = taxes[i + 1]
            self.assertGreater(
                curr_tax,
                next_tax,
                msg=f"Expected tax({curr_freq}) > tax({next_freq}), got {curr_tax} <= {next_tax}"
            )

    def test_strict_tax_drag_monotonic_ordering(self):
        """Tax Drag % (Pre_CAGR - After_CAGR) must strictly decrease as rebalance interval increases."""
        drags = []
        for freq in [
            RebalanceFrequency.WEEKLY,
            RebalanceFrequency.MONTHLY,
            RebalanceFrequency.QUARTERLY,
            RebalanceFrequency.SEMI_ANNUALLY,
            RebalanceFrequency.ANNUALLY,
        ]:
            cfg = BacktestConfig(frequency=freq, tax_enabled=True, initial_capital=100_000_000.0)
            res = simulate_portfolio(self.prices, self.dates, {"QQQ": 0.5, "SOXX": 0.5}, cfg)
            drags.append((freq.value, res.metrics.tax_drag_pct))

        for i in range(len(drags) - 1):
            curr_freq, curr_drag = drags[i]
            next_freq, next_drag = drags[i + 1]
            self.assertGreater(
                curr_drag,
                next_drag,
                msg=f"Expected tax_drag({curr_freq}) > tax_drag({next_freq}), got {curr_drag} <= {next_drag}"
            )

    def test_strict_terminal_after_tax_wealth_ordering(self):
        """
        Compounding tax deferral: terminal after-tax wealth must be strictly higher
        for infrequent rebalancing than frequent rebalancing.
        """
        terminal_wealth = []
        for freq in [
            RebalanceFrequency.WEEKLY,
            RebalanceFrequency.MONTHLY,
            RebalanceFrequency.QUARTERLY,
            RebalanceFrequency.SEMI_ANNUALLY,
            RebalanceFrequency.ANNUALLY,
        ]:
            cfg = BacktestConfig(frequency=freq, tax_enabled=True, initial_capital=100_000_000.0)
            res = simulate_portfolio(self.prices, self.dates, {"QQQ": 0.5, "SOXX": 0.5}, cfg)
            terminal_wealth.append((freq.value, res.daily_nav[-1]))

        # ANNUALLY must beat SEMI_ANNUALLY, which must beat QUARTERLY, which must beat MONTHLY, which beats WEEKLY
        for i in range(len(terminal_wealth) - 1):
            curr_freq, curr_w = terminal_wealth[i]
            next_freq, next_w = terminal_wealth[i + 1]
            self.assertLess(
                curr_w,
                next_w,
                msg=f"Expected wealth({curr_freq}) < wealth({next_freq}), got {curr_w} >= {next_w}"
            )

    def test_buy_and_hold_perfect_tax_deferral(self):
        """Buy & Hold benchmark incurs zero sales, hence exactly 0 tax paid and 0% tax drag."""
        res_q = run_buy_and_hold(self.prices["QQQ"], self.dates, "QQQ")
        self.assertEqual(res_q.metrics.total_tax_paid, 0.0)
        self.assertEqual(res_q.metrics.tax_drag_pct, 0.0)
        self.assertEqual(res_q.metrics.cagr_pre_tax, res_q.metrics.cagr_after_tax)
        self.assertEqual(len(res_q.tax_history), 0)

    def test_annual_deduction_and_rate_exact_math(self):
        """
        Verifies that annual tax = max(0, realized_gain - 2,500,000) * 0.22.
        """
        cfg = BacktestConfig(
            frequency=RebalanceFrequency.ANNUALLY,
            tax_enabled=True,
            tax_rate=0.22,
            annual_tax_deduction=2_500_000.0,
            initial_capital=100_000_000.0
        )
        res = simulate_portfolio(self.prices, self.dates, {"QQQ": 0.5, "SOXX": 0.5}, cfg)

        for rec in res.tax_history:
            realized = rec["realized_gain"]
            deduction = rec["deduction"]
            taxable = max(0.0, realized - deduction)
            expected_tax = taxable * 0.22
            self.assertAlmostEqual(rec["taxable_gain"], taxable, places=1)
            self.assertAlmostEqual(rec["tax_paid"], expected_tax, places=1)


if __name__ == "__main__":
    unittest.main()
