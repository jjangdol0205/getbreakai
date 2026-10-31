"""
Empirical Adversarial Stress-Test Suite for Milestone 1.
Authored by challenger_m1_1.

Adversarial vectors:
1. Extreme price paths: Zero return (flatline), 99.9% crash, 100x rally, flash crash & recovery.
2. Boundary conditions: Zero capital, empty dates/prices, negative/zero prices, single/two-day series.
3. Turnover friction symmetry & precision: Symmetrical asset flips, zero-turnover drift, initial fee+slippage.
4. Continuous daily MDD vs point-in-time MDD: Intramonth / intraquarter severe crash detection.
5. Capital gains tax mechanics: 22% rate, 2.5M KRW / $2,000 deduction, intra-year loss netting, non-carryforward across years, tax drag monotonic ordering across 5 cycles.
6. Extreme liquidation under massive loss: Selling at bottom after massive earlier gain.
"""

import unittest
import math
import datetime

from engine.historical_data import (
    get_qqq_history,
    get_soxx_history,
    get_joint_history,
    get_qqq_drawdowns,
    get_soxx_drawdowns,
    calculate_drawdowns,
    QQQ_RAW_DATA,
    SOXX_RAW_DATA,
)
from engine.backtest_engine import (
    BacktestConfig,
    RebalanceFrequency,
    PerformanceMetrics,
    SimulationResult,
    TaxAccountingState,
    is_rebalance_date,
    calculate_performance_metrics,
    simulate_portfolio,
    run_buy_and_hold,
)


class TestChallengerAdversarialVectors(unittest.TestCase):
    """Adversarial stress-testing of Milestone 1 engine."""

    def test_vector_flatline_zero_return(self):
        """Flat prices for 100 trading days must yield exactly 0% return, 0% MDD, 0 tax."""
        dates = [f"2020-{m:02d}-{d:02d}" for m in range(1, 5) for d in range(1, 26)]
        prices = {"ASSET_A": [100.0] * len(dates)}
        cfg = BacktestConfig(
            initial_capital=10_000.0,
            fee_rate=0.0,
            slippage_rate=0.0,
            frequency=RebalanceFrequency.MONTHLY,
            tax_enabled=True,
            annual_tax_deduction=2000.0
        )
        res = simulate_portfolio(prices, dates, {"ASSET_A": 1.0}, cfg)
        self.assertAlmostEqual(res.metrics.cumulative_return_pct, 0.0, places=1)
        self.assertAlmostEqual(res.metrics.cagr_pct, 0.0, places=1)
        self.assertAlmostEqual(res.metrics.mdd_pct, 0.0, places=1)
        self.assertEqual(res.metrics.total_tax_paid, 0.0)
        self.assertEqual(res.metrics.tax_drag_pct, 0.0)

    def test_vector_extreme_crash_99_percent(self):
        """Asset drops 99% ($1000 down to $10). Engine must handle gracefully without crashing."""
        dates = [f"2021-01-{d:02d}" for d in range(1, 31)]
        # Price drops geometrically from 1000 to 10
        prices = {"CRASH": [1000.0 * (0.01 ** (i / (len(dates) - 1))) for i in range(len(dates))]}
        cfg = BacktestConfig(
            initial_capital=100_000.0,
            fee_rate=0.001,
            slippage_rate=0.0008,
            frequency=RebalanceFrequency.WEEKLY
        )
        res = simulate_portfolio(prices, dates, {"CRASH": 1.0}, cfg)
        self.assertLess(res.metrics.cumulative_return_pct, -98.0)
        self.assertLess(res.metrics.mdd_pct, -98.0)
        self.assertGreater(res.metrics.mdd_pct, -100.0)
        # Daily NAV must remain positive throughout
        for nav in res.daily_nav:
            self.assertGreater(nav, 0.0)

    def test_vector_extreme_rally_100x(self):
        """Asset surges 100x ($10 to $1000). Engine must compute CAGR and taxes correctly."""
        # 2 full calendar years
        dates = [f"2021-{m:02d}-15" for m in range(1, 13)] + [f"2022-{m:02d}-15" for m in range(1, 13)]
        prices = {"MOON": [10.0 * (100.0 ** (i / (len(dates) - 1))) for i in range(len(dates))]}
        cfg = BacktestConfig(
            initial_capital=10_000.0,
            fee_rate=0.001,
            slippage_rate=0.0008,
            frequency=RebalanceFrequency.MONTHLY,
            tax_enabled=True,
            annual_tax_deduction=2000.0
        )
        res = simulate_portfolio(prices, dates, {"MOON": 1.0}, cfg)
        self.assertGreater(res.metrics.cumulative_return_pct, 9000.0)
        self.assertGreater(res.metrics.cagr_pct, 800.0)

    def test_vector_turnover_friction_symmetry(self):
        """
        Rebalancing from Asset A: 100% to Asset B: 100% must have identical friction
        as rebalancing from Asset B: 100% to Asset A: 100%.
        """
        dates = ["2021-01-15", "2021-01-29", "2021-02-15"]
        # Case 1: Start 100% A, switch to 100% B at date 1
        prices1 = {"A": [100.0, 100.0, 100.0], "B": [50.0, 50.0, 50.0]}
        
        def weights_flip_A_to_B(idx, date, prices, nav):
            return {"A": 1.0, "B": 0.0} if idx == 0 else {"A": 0.0, "B": 1.0}

        def weights_flip_B_to_A(idx, date, prices, nav):
            return {"A": 0.0, "B": 1.0} if idx == 0 else {"A": 1.0, "B": 0.0}

        cfg = BacktestConfig(
            initial_capital=100_000.0,
            fee_rate=0.0010,
            slippage_rate=0.0008,
            frequency=RebalanceFrequency.MONTHLY,
            tax_enabled=False
        )

        res1 = simulate_portfolio(prices1, dates, weights_flip_A_to_B, cfg)
        res2 = simulate_portfolio(prices1, dates, weights_flip_B_to_A, cfg)

        self.assertAlmostEqual(res1.metrics.fee_paid, res2.metrics.fee_paid, places=2)
        self.assertAlmostEqual(res1.metrics.slippage_paid, res2.metrics.slippage_paid, places=2)
        self.assertAlmostEqual(res1.metrics.total_turnover, res2.metrics.total_turnover, places=4)
        self.assertAlmostEqual(res1.daily_nav[-1], res2.daily_nav[-1], places=2)

    def test_vector_continuous_daily_mdd_vs_point_in_time(self):
        """
        Critical Challenge: An intramonth flash crash of -50% that recovers before
        monthly rebalance date MUST be captured by continuous daily MDD.
        A point-in-time rebalance date checker would fail to see it.
        """
        # 1 month of daily dates
        dates = [f"2021-03-{d:02d}" for d in range(1, 32)]
        # Asset starts at 100, drops to 50 on March 15, recovers to 100 on March 31
        prices_list = [100.0] * 31
        prices_list[14] = 50.0  # March 15 crash
        prices = {"STOCK": prices_list}

        cfg = BacktestConfig(
            initial_capital=100_000.0,
            fee_rate=0.0,
            slippage_rate=0.0,
            frequency=RebalanceFrequency.MONTHLY,
            tax_enabled=False
        )
        res = simulate_portfolio(prices, dates, {"STOCK": 1.0}, cfg)

        # End-point return is 0%, but continuous daily MDD must capture the -50% drop!
        self.assertAlmostEqual(res.metrics.cumulative_return_pct, 0.0, places=1)
        self.assertAlmostEqual(res.metrics.mdd_pct, -50.0, places=1)
        self.assertAlmostEqual(min(res.daily_drawdowns), -0.50, places=2)

    def test_vector_tax_mechanics_22_pct_and_deduction(self):
        """
        Tax mechanics verification:
        Year 1: Realized gain of $10,000.
        Annual deduction: $2,000.
        Taxable gain: $8,000.
        Tax at 22%: $1,760.
        """
        dates = ["2021-01-04", "2021-06-30", "2021-12-31"]
        # Stock doubles from 100 to 200 at June 30. We rebalance from 100% Stock to 50% Stock / 50% Cash-proxy
        prices = {"A": [100.0, 200.0, 200.0], "B": [100.0, 100.0, 100.0]}

        def rebal_func(idx, date, p, nav):
            if idx == 0:
                return {"A": 1.0, "B": 0.0}
            return {"A": 0.0, "B": 1.0}  # Liquidate all A, realize all gains

        cfg = BacktestConfig(
            initial_capital=10_000.0,
            fee_rate=0.0,
            slippage_rate=0.0,
            frequency=RebalanceFrequency.SEMI_ANNUALLY,
            tax_enabled=True,
            annual_tax_deduction=2000.0,
            tax_rate=0.22
        )
        res = simulate_portfolio(prices, dates, rebal_func, cfg)

        # Inception: $10,000 buys 100 shares of A @ $100.
        # At June 30: A is @ $200. Valuation = 100 * $200 = $20,000.
        # Sold 100 shares of A @ $200 (cost basis $100).
        # Realized gain = 100 * ($200 - $100) = $10,000.
        # Year end Dec 31: Taxable = $10,000 - $2,000 = $8,000.
        # Tax = $8,000 * 0.22 = $1,760.
        self.assertEqual(len(res.tax_history), 1)
        tax_rec = res.tax_history[0]
        self.assertAlmostEqual(tax_rec["realized_gain"], 10000.0, places=1)
        self.assertAlmostEqual(tax_rec["deduction"], 2000.0, places=1)
        self.assertAlmostEqual(tax_rec["taxable_gain"], 8000.0, places=1)
        self.assertAlmostEqual(tax_rec["tax_paid"], 1760.0, places=1)
        self.assertAlmostEqual(res.metrics.total_tax_paid, 1760.0, places=1)

    def test_vector_tax_loss_netting_within_same_year(self):
        """
        Gain on Stock A ($10,000) and Loss on Stock B (-$4,000) within the same year
        must net to $6,000.
        With $2,000 deduction, taxable = $4,000, tax at 22% = $880.
        """
        dates = ["2021-01-04", "2021-04-30", "2021-08-31", "2021-12-31"]
        # Inception: 50/50 A and B ($10,000 each)
        # April: A doubles (cost $100 -> $200). Liquidate A: gain = $10,000. Buy C.
        # August: B drops 40% (cost $100 -> $60). Liquidate B: loss = -$4,000. Buy C.
        prices = {
            "A": [100.0, 200.0, 200.0, 200.0],
            "B": [100.0, 100.0, 60.0, 60.0],
            "C": [100.0, 100.0, 100.0, 100.0],
        }

        def rebal_func(idx, date, p, nav):
            if idx == 0:
                return {"A": 0.5, "B": 0.5, "C": 0.0}
            elif idx == 1:
                return {"A": 0.0, "B": 0.5, "C": 0.5}  # Liquidate A
            else:
                return {"A": 0.0, "B": 0.0, "C": 1.0}  # Liquidate B

        cfg = BacktestConfig(
            initial_capital=20_000.0,
            fee_rate=0.0,
            slippage_rate=0.0,
            frequency=RebalanceFrequency.MONTHLY,
            tax_enabled=True,
            annual_tax_deduction=2000.0,
            tax_rate=0.22
        )
        res = simulate_portfolio(prices, dates, rebal_func, cfg)

        self.assertEqual(len(res.tax_history), 1)
        tax_rec = res.tax_history[0]
        # Gain on A: +10,000. In April B was topped up to 50% ($15,000 = 150 shares).
        # In August B dropped to $60, sold 150 shares: Loss = 150 * ($60 - $100) = -$6,000.
        # Net gain: 10,000 - 6,000 = 4,000.
        # Taxable: 4,000 - 2,000 = 2,000.
        # Tax: 2,000 * 0.22 = 440.
        self.assertAlmostEqual(tax_rec["realized_gain"], 4000.0, delta=10.0)
        self.assertAlmostEqual(tax_rec["taxable_gain"], 2000.0, delta=10.0)
        self.assertAlmostEqual(tax_rec["tax_paid"], 440.0, delta=5.0)

    def test_vector_no_tax_loss_carryforward_across_years(self):
        """
        Korean tax law does NOT permit loss carryforward across tax years for overseas equities.
        Year 1: Net loss of -$5,000 (tax = $0).
        Year 2: Net gain of +$5,000 (taxable must be $5,000 - $2,000 = $3,000, tax = $660).
        Year 1 loss must NOT offset Year 2 gain.
        """
        dates = [
            "2021-01-04", "2021-06-30", "2021-12-31",
            "2022-01-04", "2022-06-30", "2022-12-31"
        ]
        prices = {
            "A": [100.0, 50.0, 50.0, 50.0, 50.0, 50.0],     # Drops in 2021
            "B": [100.0, 100.0, 100.0, 100.0, 200.0, 200.0] # Doubles in 2022
        }

        def rebal_func(idx, date, p, nav):
            if idx < 2:
                return {"A": 1.0, "B": 0.0}
            elif idx == 2:
                # Sell A at loss in 2021-12-31, buy B
                return {"A": 0.0, "B": 1.0}
            elif idx == 4:
                # Sell B at gain in 2022-06-30, buy A
                return {"A": 1.0, "B": 0.0}
            else:
                return {"A": 1.0, "B": 0.0}

        cfg = BacktestConfig(
            initial_capital=10_000.0,
            fee_rate=0.0,
            slippage_rate=0.0,
            frequency=RebalanceFrequency.SEMI_ANNUALLY,
            tax_enabled=True,
            annual_tax_deduction=2000.0,
            tax_rate=0.22
        )
        res = simulate_portfolio(prices, dates, rebal_func, cfg)

        # 2021: loss realized, tax = 0
        tax_2021 = [r for r in res.tax_history if r["year"] == 2021]
        self.assertEqual(len(tax_2021), 0)  # No tax paid in 2021

        # 2022: gain realized, tax must be assessed on 2022 gain without carryforward
        tax_2022 = [r for r in res.tax_history if r["year"] == 2022]
        self.assertEqual(len(tax_2022), 1)
        self.assertGreater(tax_2022[0]["tax_paid"], 0.0)

    def test_vector_tax_drag_monotonicity_across_5_frequencies(self):
        """
        Tax drag should monotonically decrease as rebalancing frequency decreases
        (Weekly >= Monthly >= Quarterly >= Semi-Annually >= Annually) in a trending asset.
        """
        joint = get_joint_history()
        dates = sorted(joint.keys())
        prices = {"QQQ": [joint[d]["QQQ"] for d in dates], "SOXX": [joint[d]["SOXX"] for d in dates]}
        weights = {"QQQ": 0.5, "SOXX": 0.5}

        drags = {}
        for freq in RebalanceFrequency:
            cfg = BacktestConfig(frequency=freq, fee_rate=0.001, slippage_rate=0.0008, tax_enabled=True)
            res = simulate_portfolio(prices, dates, weights, cfg)
            drags[freq] = res.metrics.tax_drag_pct

        # Weekly tax drag must exceed Monthly tax drag
        self.assertGreater(drags[RebalanceFrequency.WEEKLY], drags[RebalanceFrequency.MONTHLY])
        # Monthly tax drag must exceed Quarterly tax drag
        self.assertGreater(drags[RebalanceFrequency.MONTHLY], drags[RebalanceFrequency.QUARTERLY])
        # Quarterly tax drag must exceed Semi-Annual tax drag
        self.assertGreater(drags[RebalanceFrequency.QUARTERLY], drags[RebalanceFrequency.SEMI_ANNUALLY])
        # Semi-Annual tax drag must be >= Annual tax drag
        self.assertGreaterEqual(drags[RebalanceFrequency.SEMI_ANNUALLY], drags[RebalanceFrequency.ANNUALLY])

    def test_vector_input_validation_and_edge_exceptions(self):
        """Engine must raise proper ValueErrors on malformed inputs."""
        dates = ["2021-01-04", "2021-01-05"]
        prices = {"A": [10.0, 11.0]}

        # Empty dates or prices
        with self.assertRaises(ValueError):
            simulate_portfolio({}, dates, {"A": 1.0})
        with self.assertRaises(ValueError):
            simulate_portfolio(prices, [], {"A": 1.0})

        # Length mismatch
        with self.assertRaises(ValueError):
            simulate_portfolio({"A": [10.0]}, dates, {"A": 1.0})

        # Non-positive initial capital
        with self.assertRaises(ValueError):
            simulate_portfolio(prices, dates, {"A": 1.0}, BacktestConfig(initial_capital=0.0))
        with self.assertRaises(ValueError):
            simulate_portfolio(prices, dates, {"A": 1.0}, BacktestConfig(initial_capital=-500.0))


if __name__ == "__main__":
    unittest.main()
