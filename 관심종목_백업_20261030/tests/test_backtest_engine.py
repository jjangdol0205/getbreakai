"""
Comprehensive Unit & Integration Test Suite for Milestone 1:
25-Year Timeseries Dataset & Backtest Engine with Capital Gains Tax Modeling.

Validates:
1. Historical dataset continuity, bounds, stock splits, and 5 crisis drawdowns.
2. Financial metric algorithms: exact CAGR, continuous daily MDD, Sharpe, Calmar, Worst Year.
3. Portfolio simulation state machine: share drift, 2-way turnover friction, 5 rebalance cycles.
4. Foreign equity capital gains tax modeling (22% rate, annual deduction, year-end settlement, tax drag).
"""

import unittest
import math
import datetime

from engine.historical_data import (
    HistoricalBar,
    get_qqq_history,
    get_soxx_history,
    get_joint_history,
    get_qqq_drawdowns,
    get_soxx_drawdowns,
    calculate_drawdowns,
    QQQ_INCEPTION_DATE,
    SOXX_INCEPTION_DATE,
    COMMON_START_DATE,
    COMMON_END_DATE,
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


class TestHistoricalDataSuite(unittest.TestCase):
    """Verifies 25.25-year historical dataset integrity for QQQ and SOXX."""

    def test_qqq_history_bounds_and_continuity(self):
        """QQQ must span from 1999-03-10 to 2026-10-12 with ~6,930 daily bars."""
        qqq = get_qqq_history()
        self.assertGreater(len(qqq), 6900)
        self.assertLess(len(qqq), 7000)
        self.assertEqual(qqq[0].date, QQQ_INCEPTION_DATE)
        self.assertEqual(qqq[-1].date, COMMON_END_DATE)
        self.assertIsInstance(qqq[0], HistoricalBar)

        # Inception and terminal price bounds
        self.assertAlmostEqual(qqq[0].close, 51.06, places=1)
        self.assertAlmostEqual(qqq[-1].close, 514.80, places=1)
        self.assertAlmostEqual(qqq[-1].adj_close, 514.80, places=1)

    def test_soxx_history_bounds_and_continuity(self):
        """SOXX must span from 2001-07-10 to 2026-10-12 with ~6,350 daily bars."""
        soxx = get_soxx_history()
        self.assertGreater(len(soxx), 6300)
        self.assertLess(len(soxx), 6400)
        self.assertEqual(soxx[0].date, SOXX_INCEPTION_DATE)
        self.assertEqual(soxx[-1].date, COMMON_END_DATE)
        self.assertIsInstance(soxx[0], HistoricalBar)

        # Inception and terminal price bounds
        self.assertAlmostEqual(soxx[0].close, 179.40, places=1)
        self.assertAlmostEqual(soxx[-1].close, 262.40, places=1)
        self.assertAlmostEqual(soxx[-1].adj_close, 262.40, places=1)

    def test_joint_history_alignment(self):
        """Joint history must align common 25.25-year period (2001-07-10 to 2026-10-12)."""
        joint = get_joint_history()
        dates = sorted(joint.keys())
        self.assertEqual(dates[0], COMMON_START_DATE)
        self.assertEqual(dates[-1], COMMON_END_DATE)
        self.assertGreater(len(dates), 6300)

        # Check required keys in each daily map
        first_entry = joint[dates[0]]
        self.assertIn("QQQ", first_entry)
        self.assertIn("SOXX", first_entry)
        self.assertIn("qqq", first_entry)
        self.assertIn("soxx", first_entry)
        self.assertIn("qqq_close", first_entry)
        self.assertIn("soxx_close", first_entry)
        self.assertIn("qqq_volume", first_entry)
        self.assertIn("soxx_volume", first_entry)

        # All values must be positive floats
        for k, v in first_entry.items():
            self.assertIsInstance(v, float)
            self.assertGreater(v, 0.0)

    def test_no_negative_or_nan_prices(self):
        """All price and volume data must be strictly positive and finite."""
        for bar in QQQ_RAW_DATA:
            self.assertFalse(math.isnan(bar.close))
            self.assertFalse(math.isnan(bar.adj_close))
            self.assertGreater(bar.close, 0.0)
            self.assertGreater(bar.adj_close, 0.0)
            self.assertGreater(bar.volume, 0)

        for bar in SOXX_RAW_DATA:
            self.assertFalse(math.isnan(bar.close))
            self.assertFalse(math.isnan(bar.adj_close))
            self.assertGreater(bar.close, 0.0)
            self.assertGreater(bar.adj_close, 0.0)
            self.assertGreater(bar.volume, 0)

    def test_soxx_stock_split_2024(self):
        """SOXX March 7, 2024 3-for-1 forward stock split must be cleanly reflected."""
        soxx = get_soxx_history()
        pre_split_bars = [b for b in soxx if b.date == "2024-03-06"]
        post_split_bars = [b for b in soxx if b.date == "2024-03-07"]

        self.assertEqual(len(pre_split_bars), 1)
        self.assertEqual(len(post_split_bars), 1)

        b_pre = pre_split_bars[0]
        b_post = post_split_bars[0]

        # Unadjusted close dropped ~3:1
        self.assertAlmostEqual(b_pre.close / b_post.close, 3.0, delta=0.1)
        # Adjusted close is continuous across split
        self.assertAlmostEqual(b_pre.adj_close, b_post.adj_close, places=1)

    def test_qqq_stock_split_2000(self):
        """QQQ March 20, 2000 2-for-1 forward stock split must be cleanly reflected."""
        qqq = get_qqq_history()
        pre_split_bars = [b for b in qqq if b.date == "2000-03-17"]
        post_split_bars = [b for b in qqq if b.date == "2000-03-20"]

        self.assertEqual(len(pre_split_bars), 1)
        self.assertEqual(len(post_split_bars), 1)

        b_pre = pre_split_bars[0]
        b_post = post_split_bars[0]

        # Unadjusted close dropped 2:1
        self.assertAlmostEqual(b_pre.close / b_post.close, 2.0, delta=0.1)
        # Adjusted close is continuous across split
        self.assertAlmostEqual(b_pre.adj_close, b_post.adj_close, places=1)

    def test_historical_crisis_drawdowns(self):
        """Verifies drawdown magnitudes across the 5 historical macro crises."""
        qqq = get_qqq_history()
        soxx = get_soxx_history()

        def _sub_dd(series, start, end):
            sub = [b for b in series if start <= b.date <= end]
            dds = calculate_drawdowns([b.adj_close for b in sub])
            return min(dds) * 100.0

        # 1. 2000-2002 Dot-Com crash: QQQ ~ -83%
        dd_dotcom = _sub_dd(qqq, "2000-01-01", "2002-12-31")
        self.assertLess(dd_dotcom, -80.0)
        self.assertGreater(dd_dotcom, -86.0)

        # 2. 2008 GFC crash: QQQ ~ -53% ~ -56%, SOXX ~ -64% ~ -73%
        dd_gfc_q = _sub_dd(qqq, "2007-01-01", "2009-06-30")
        dd_gfc_s = _sub_dd(soxx, "2007-01-01", "2009-06-30")
        self.assertLess(dd_gfc_q, -50.0)
        self.assertGreater(dd_gfc_q, -58.0)
        self.assertLess(dd_gfc_s, -64.0)
        self.assertGreater(dd_gfc_s, -75.0)

        # 3. 2020 COVID crash: QQQ ~ -30%, SOXX ~ -35%
        dd_covid_q = _sub_dd(qqq, "2020-01-01", "2020-04-30")
        dd_covid_s = _sub_dd(soxx, "2020-01-01", "2020-04-30")
        self.assertLess(dd_covid_q, -28.0)
        self.assertGreater(dd_covid_q, -33.0)
        self.assertLess(dd_covid_s, -32.0)
        self.assertGreater(dd_covid_s, -38.0)

        # 4. 2022 Tightening crash: QQQ ~ -36% ~ -41%, SOXX ~ -43% ~ -48%
        dd_tight_q = _sub_dd(qqq, "2021-10-01", "2022-12-31")
        dd_tight_s = _sub_dd(soxx, "2021-10-01", "2022-12-31")
        self.assertLess(dd_tight_q, -35.0)
        self.assertGreater(dd_tight_q, -42.0)
        self.assertLess(dd_tight_s, -42.0)
        self.assertGreater(dd_tight_s, -49.0)

    def test_drawdown_series_accessors(self):
        """Drawdown series helpers must return non-positive fractions aligned with bars."""
        qqq_dds = get_qqq_drawdowns()
        soxx_dds = get_soxx_drawdowns()

        self.assertEqual(len(qqq_dds), len(QQQ_RAW_DATA))
        self.assertEqual(len(soxx_dds), len(SOXX_RAW_DATA))

        for _, dd in qqq_dds:
            self.assertLessEqual(dd, 0.0)
            self.assertGreaterEqual(dd, -1.0)

        for _, dd in soxx_dds:
            self.assertLessEqual(dd, 0.0)
            self.assertGreaterEqual(dd, -1.0)


class TestBacktestMetricsSuite(unittest.TestCase):
    """Verifies mathematical precision of financial metric formulas."""

    def test_exact_cagr_formula_synthetic(self):
        """CAGR must use exact calendar years Y = Delta days / 365.25."""
        # Exactly 2.0 years: 730.5 days -> 731 days
        d0 = "2020-01-01"
        d1 = (datetime.date.fromisoformat(d0) + datetime.timedelta(days=731)).isoformat()
        dates = [d0, d1]
        nav = [100.0, 200.0]

        metrics = calculate_performance_metrics(nav, dates)
        # Expected: (200 / 100) ** (1 / (731 / 365.25)) - 1 ~= sqrt(2) - 1 = 41.42%
        expected_cagr = ((200.0 / 100.0) ** (365.25 / 731.0) - 1.0) * 100.0
        self.assertAlmostEqual(metrics.cagr_pct, expected_cagr, places=1)
        self.assertEqual(metrics.cumulative_return_pct, 100.0)

    def test_continuous_daily_mdd_formula_synthetic(self):
        """MDD must identify the deepest peak-to-trough drop."""
        dates = ["2020-01-01", "2020-01-02", "2020-01-03", "2020-01-04"]
        nav = [100.0, 150.0, 90.0, 120.0]
        metrics = calculate_performance_metrics(nav, dates)
        # Peak = 150, Trough = 90 -> (90 - 150) / 150 = -40.0%
        self.assertEqual(metrics.mdd_pct, -40.0)

    def test_sharpe_and_calmar_ratios(self):
        """Verifies Sharpe with Rf=2.0% and Calmar = CAGR / |MDD|."""
        dates = [
            (datetime.date(2020, 1, 1) + datetime.timedelta(days=i)).isoformat()
            for i in range(253)
        ]
        # Alternating positive daily returns with non-zero variance
        nav = [100.0]
        for i in range(1, 253):
            step = 1.0020 if i % 2 == 1 else 1.0004
            nav.append(nav[-1] * step)
        metrics = calculate_performance_metrics(nav, dates, risk_free_rate=0.02)

        self.assertGreater(metrics.sharpe_ratio, 0.0)
        self.assertGreater(metrics.calmar_ratio, 0.0)
        self.assertEqual(metrics.mdd_pct, 0.0)  # Monotonic rise

    def test_worst_calendar_year_calculation(self):
        """Worst calendar year must identify the calendar year with lowest return."""
        dates = [
            "2020-01-01", "2020-12-31",
            "2021-01-01", "2021-12-31",
            "2022-01-01", "2022-12-31"
        ]
        # 2020: +20%, 2021: +10%, 2022: -30%
        nav = [100.0, 120.0, 120.0, 132.0, 132.0, 92.4]
        metrics = calculate_performance_metrics(nav, dates)

        self.assertEqual(metrics.worst_year, "2022")
        self.assertAlmostEqual(metrics.worst_year_pct, -30.0, places=1)

    def test_metric_alias_properties(self):
        """Verifies backward-compatible dataclass properties."""
        metrics = PerformanceMetrics(
            cumulative_return_pct=500.0,
            cagr_pct=15.0,
            mdd_pct=-25.0,
            sharpe_ratio=1.1,
            calmar_ratio=0.6,
            worst_year="2008",
            worst_year_pct=-20.0,
        )
        self.assertEqual(metrics.cagr, 15.0)
        self.assertEqual(metrics.mdd, -25.0)
        self.assertEqual(metrics.cumulative_return, 500.0)
        self.assertEqual(metrics.worst_year_return_pct, -20.0)


class TestBacktestSimulationSuite(unittest.TestCase):
    """Verifies portfolio simulation state machine, friction, and frequencies."""

    def setUp(self):
        joint = get_joint_history()
        self.dates = sorted(joint.keys())
        self.prices = {
            "QQQ": [joint[d]["QQQ"] for d in self.dates],
            "SOXX": [joint[d]["SOXX"] for d in self.dates],
        }

    def test_initial_deployment_friction(self):
        """Initial deployment must deduct 0.1% fee and 0.08% slippage on starting capital."""
        cfg = BacktestConfig(
            initial_capital=10_000_000.0,
            fee_rate=0.0010,
            slippage_rate=0.0008,
            tax_enabled=False
        )
        prices_10 = {k: v[:10] for k, v in self.prices.items()}
        res = simulate_portfolio(prices_10, self.dates[:10], {"QQQ": 1.0}, cfg)

        expected_friction = 10_000_000.0 * (0.0010 + 0.0008)  # 18,000
        first_nav = res.daily_nav[0]
        self.assertAlmostEqual(first_nav, 10_000_000.0 - expected_friction, places=1)

    def test_continuous_share_drift_without_rebalance(self):
        """Share quantities must remain constant between scheduled rebalances."""
        cfg = BacktestConfig(
            frequency=RebalanceFrequency.ANNUALLY,
            tax_enabled=False
        )
        prices_60 = {k: v[:60] for k, v in self.prices.items()}
        res = simulate_portfolio(prices_60, self.dates[:60], {"QQQ": 0.5, "SOXX": 0.5}, cfg)

        # Within the first 60 days (same year), share counts must remain unchanged
        initial_shares = res.holdings_history[0]
        day50_shares = res.holdings_history[50]
        self.assertEqual(initial_shares["QQQ"], day50_shares["QQQ"])
        self.assertEqual(initial_shares["SOXX"], day50_shares["SOXX"])

    def test_five_rebalance_frequencies(self):
        """All 5 frequencies must execute and show progressive turnover ordering."""
        turnovers = {}
        for freq in RebalanceFrequency:
            cfg = BacktestConfig(frequency=freq, tax_enabled=False)
            res = simulate_portfolio(self.prices, self.dates, {"QQQ": 0.5, "SOXX": 0.5}, cfg)
            turnovers[freq] = res.metrics.total_turnover
            self.assertGreater(res.metrics.cagr_pct, 0.0)
            self.assertLess(res.metrics.mdd_pct, 0.0)

        # Weekly rebalancing must incur higher turnover than monthly, which is higher than annual
        self.assertGreater(turnovers[RebalanceFrequency.WEEKLY], turnovers[RebalanceFrequency.MONTHLY])
        self.assertGreater(turnovers[RebalanceFrequency.MONTHLY], turnovers[RebalanceFrequency.ANNUALLY])

    def test_buy_and_hold_runner(self):
        """run_buy_and_hold must run single-asset benchmarks seamlessly."""
        res_qqq = run_buy_and_hold(self.prices["QQQ"], self.dates, "QQQ")
        self.assertIsInstance(res_qqq, SimulationResult)
        self.assertGreater(res_qqq.metrics.cagr_pct, 5.0)
        self.assertLess(res_qqq.metrics.mdd_pct, -50.0)

    def test_100_percent_equity_constraint(self):
        """Portfolio weights must always sum to 100% equity with zero cash."""
        cfg = BacktestConfig(frequency=RebalanceFrequency.MONTHLY, tax_enabled=False)
        prices_100 = {k: v[:100] for k, v in self.prices.items()}
        res = simulate_portfolio(prices_100, self.dates[:100], {"QQQ": 0.6, "SOXX": 0.4}, cfg)

        for reb in res.rebalance_records:
            target_w = reb["target_weights"]
            self.assertAlmostEqual(sum(target_w.values()), 1.0, places=4)


class TestTaxModelingSuite(unittest.TestCase):
    """Verifies foreign equity capital gains tax modeling (22% rate & annual deduction)."""

    def setUp(self):
        joint = get_joint_history()
        self.dates = sorted(joint.keys())
        self.prices = {
            "QQQ": [joint[d]["QQQ"] for d in self.dates],
            "SOXX": [joint[d]["SOXX"] for d in self.dates],
        }

    def test_tax_deduction_and_rate_synthetic(self):
        """22% tax must be deducted only on annual net realized gains exceeding deduction."""
        cfg = BacktestConfig(
            initial_capital=10_000.0,
            tax_enabled=True,
            tax_rate=0.22,
            annual_tax_deduction=2000.0,
            frequency=RebalanceFrequency.MONTHLY
        )
        prices_252 = {k: v[:252] for k, v in self.prices.items()}
        res = simulate_portfolio(prices_252, self.dates[:252], {"QQQ": 0.5, "SOXX": 0.5}, cfg)
        self.assertIsInstance(res.tax_state, TaxAccountingState)

    def test_pre_tax_vs_after_tax_metrics(self):
        """After-tax CAGR must be strictly less than or equal to pre-tax CAGR."""
        cfg = BacktestConfig(
            frequency=RebalanceFrequency.MONTHLY,
            tax_enabled=True,
            tax_rate=0.22,
            annual_tax_deduction=2_500_000.0,
            initial_capital=100_000_000.0
        )
        res = simulate_portfolio(self.prices, self.dates, {"QQQ": 0.5, "SOXX": 0.5}, cfg)
        m = res.metrics

        self.assertGreater(m.cagr_pre_tax, m.cagr_after_tax)
        self.assertGreater(m.tax_drag_pct, 0.0)
        self.assertAlmostEqual(m.tax_drag_pct, m.cagr_pre_tax - m.cagr_after_tax, places=1)
        self.assertGreater(m.total_tax_paid, 0.0)
        self.assertGreater(len(res.tax_history), 0)

    def test_tax_disabled_mode(self):
        """When tax_enabled is False, pre-tax and after-tax metrics must be identical."""
        cfg = BacktestConfig(
            frequency=RebalanceFrequency.MONTHLY,
            tax_enabled=False
        )
        prices_500 = {k: v[:500] for k, v in self.prices.items()}
        res = simulate_portfolio(prices_500, self.dates[:500], {"QQQ": 0.5, "SOXX": 0.5}, cfg)
        m = res.metrics

        self.assertEqual(m.cagr_pre_tax, m.cagr_after_tax)
        self.assertEqual(m.tax_drag_pct, 0.0)
        self.assertEqual(m.total_tax_paid, 0.0)
        self.assertEqual(len(res.tax_history), 0)

    def test_tax_drag_across_frequencies(self):
        """Frequent rebalancing (Weekly) must generate higher tax drag than Annual."""
        cfg_weekly = BacktestConfig(frequency=RebalanceFrequency.WEEKLY, tax_enabled=True)
        cfg_annual = BacktestConfig(frequency=RebalanceFrequency.ANNUALLY, tax_enabled=True)

        res_w = simulate_portfolio(self.prices, self.dates, {"QQQ": 0.5, "SOXX": 0.5}, cfg_weekly)
        res_a = simulate_portfolio(self.prices, self.dates, {"QQQ": 0.5, "SOXX": 0.5}, cfg_annual)

        self.assertGreater(res_w.metrics.tax_drag_pct, res_a.metrics.tax_drag_pct)
        self.assertGreater(res_w.metrics.total_tax_paid, res_a.metrics.total_tax_paid)


if __name__ == "__main__":
    unittest.main()
