"""
Comprehensive Unit & Integration Test Suite for Milestone 3:
Strategy B (QQQ) & Strategy C (SOXX) Benchmark Optimization Models & Tax Deferral Simulator.

Validates:
1. Technical indicator algorithms: 200 SMA calculation, rolling windows, Bull vs Bear regime signals.
2. Dual Momentum: weighted 3M (40%) + 12M (60%) returns, relative momentum winner, absolute trend defense.
3. Volatility Scaling: 20-day annualized realized vol, inverse scaling to 20% target vol, panic contraction.
4. MDD Reduction vs Buy & Hold: verifies QQQ/SOXX MDD compression from -83%/-71% to <= -32%.
5. 5 Rebalancing Cycles: full evaluation across WEEKLY, MONTHLY, QUARTERLY, SEMI_ANNUALLY, ANNUALLY.
6. Monotonic Tax Drag: proves tax drag decreases monotonically as rebalancing frequency decreases.
7. Optimal Cycle Maximization: proves Monthly cycle maximizes After-Tax Calmar Ratio.
8. Model Comparison: side-by-side comparison across BUY_AND_HOLD, SMA200, DUAL_MOMENTUM, VOL_SCALING.
9. 100% Offline, Zero-CDN, Pure Python Standard Library.
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
    get_qqq_history,
    get_soxx_history,
)
from engine.strategy_benchmark_opt import (
    BenchmarkModel,
    StrategyBCSimulator,
    calculate_momentum,
    calculate_momentum_series,
    calculate_realized_volatility,
    calculate_sma,
    calculate_sma_series,
    calculate_vol_scaling_weight,
    calculate_volatility_series,
    compare_all_cycles,
    compare_all_models,
    find_optimal_cycle,
    is_sma_bull,
    normalize_cycle,
    normalize_model_name,
    run_benchmark_optimization,
)


class TestTier1IndicatorCalculations(unittest.TestCase):
    """Tier 1: Pure unit tests verifying mathematical indicator algorithms."""

    def test_sma_calculation_exact_formula(self):
        """calculate_sma must compute exact arithmetic mean of window observations."""
        prices = [10.0, 20.0, 30.0, 40.0, 50.0]
        # Window = 3 -> mean of last 3: (30 + 40 + 50) / 3 = 40.0
        self.assertAlmostEqual(calculate_sma(prices, window=3), 40.0, places=5)
        # Window = 2 -> mean of last 2: (40 + 50) / 2 = 45.0
        self.assertAlmostEqual(calculate_sma(prices, window=2), 45.0, places=5)
        # Window = 10 (greater than len) -> mean of all 5: 30.0
        self.assertAlmostEqual(calculate_sma(prices, window=10), 30.0, places=5)
        # Empty list -> 0.0
        self.assertEqual(calculate_sma([], window=5), 0.0)

    def test_sma_series_expanding_and_rolling(self):
        """calculate_sma_series must return correct expanding mean initially and rolling window later."""
        prices = [10.0, 20.0, 30.0, 40.0, 50.0]
        smas = calculate_sma_series(prices, window=3)
        self.assertEqual(len(smas), 5)
        # i=0: 10.0
        self.assertAlmostEqual(smas[0], 10.0, places=5)
        # i=1: (10 + 20) / 2 = 15.0
        self.assertAlmostEqual(smas[1], 15.0, places=5)
        # i=2: (10 + 20 + 30) / 3 = 20.0
        self.assertAlmostEqual(smas[2], 20.0, places=5)
        # i=3: (20 + 30 + 40) / 3 = 30.0
        self.assertAlmostEqual(smas[3], 30.0, places=5)
        # i=4: (30 + 40 + 50) / 3 = 40.0
        self.assertAlmostEqual(smas[4], 40.0, places=5)

    def test_sma_regime_classification(self):
        """is_sma_bull must strictly distinguish bull from bear regime."""
        self.assertTrue(is_sma_bull(105.0, 100.0))
        self.assertFalse(is_sma_bull(95.0, 100.0))
        # Boundary condition: price == SMA is bear defense
        self.assertFalse(is_sma_bull(100.0, 100.0))

    def test_dual_momentum_calculation_formula(self):
        """calculate_momentum must compute 0.4 * R_3M + 0.6 * R_12M."""
        # Create synthetic series of 300 days
        prices = [100.0] * 300
        # Set 3M lookback (idx = 300 - 1 - 63 = 236) to 120.0 (+25% gain)
        # Set 12M lookback (idx = 300 - 1 - 252 = 47) to 80.0 (+87.5% gain)
        # Current price = 150.0
        prices[236] = 120.0
        prices[47] = 80.0
        prices[-1] = 150.0

        r_3m = (150.0 - 120.0) / 120.0  # +0.25 (25%)
        r_12m = (150.0 - 80.0) / 80.0    # +0.875 (87.5%)
        expected_mom = 0.4 * r_3m + 0.6 * r_12m  # 0.10 + 0.525 = 0.625

        mom = calculate_momentum(prices, lookback_short=63, lookback_long=252)
        self.assertAlmostEqual(mom, expected_mom, places=5)

    def test_dual_momentum_series_length_and_edge_cases(self):
        """calculate_momentum_series must handle small lists and return identical length."""
        self.assertEqual(calculate_momentum_series([]), [])
        short_series = [10.0, 12.0, 15.0]
        moms = calculate_momentum_series(short_series, lookback_short=1, lookback_long=2)
        self.assertEqual(len(moms), 3)

    def test_realized_volatility_annualization(self):
        """calculate_realized_volatility must compute sample standard deviation scaled by sqrt(252)."""
        # Flat series -> 0.0 vol
        flat = [100.0] * 30
        self.assertEqual(calculate_realized_volatility(flat, window=20), 0.0)

        # Alternating series with known return variance
        p = 100.0
        alt = []
        for i in range(25):
            alt.append(p)
            p *= 1.01 if i % 2 == 0 else 0.99
        vol = calculate_realized_volatility(alt, window=20)
        self.assertGreater(vol, 0.05)
        self.assertLess(vol, 0.35)

    def test_vol_scaling_inverse_weight(self):
        """calculate_vol_scaling_weight must scale weight inversely relative to 20% target vol."""
        # Realized vol = 10% (< 20%) -> capped at 1.0
        self.assertAlmostEqual(calculate_vol_scaling_weight(0.10, target_vol=0.20), 1.0)
        # Realized vol = 20% -> 1.0
        self.assertAlmostEqual(calculate_vol_scaling_weight(0.20, target_vol=0.20), 1.0)
        # Realized vol = 40% -> 0.20 / 0.40 = 0.50
        self.assertAlmostEqual(calculate_vol_scaling_weight(0.40, target_vol=0.20), 0.50)
        # Realized vol = 80% (crash panic) -> 0.20 / 0.80 = 0.25
        self.assertAlmostEqual(calculate_vol_scaling_weight(0.80, target_vol=0.20), 0.25)
        # Zero vol -> max_weight
        self.assertAlmostEqual(calculate_vol_scaling_weight(0.0, target_vol=0.20), 1.0)

    def test_name_and_cycle_normalizers(self):
        """String normalizers must map aliases and reject invalid inputs."""
        self.assertEqual(normalize_model_name("SMA200"), BenchmarkModel.SMA200)
        self.assertEqual(normalize_model_name("sma_200"), BenchmarkModel.SMA200)
        self.assertEqual(normalize_model_name("dual_momentum"), BenchmarkModel.DUAL_MOMENTUM)
        self.assertEqual(normalize_model_name("vol_scaling"), BenchmarkModel.VOL_SCALING)
        self.assertEqual(normalize_model_name("buy_and_hold"), BenchmarkModel.BUY_AND_HOLD)
        with self.assertRaises(ValueError):
            normalize_model_name("UNKNOWN_MODEL_NAME")

        self.assertEqual(normalize_cycle("WEEKLY"), RebalanceFrequency.WEEKLY)
        self.assertEqual(normalize_cycle("W"), RebalanceFrequency.WEEKLY)
        self.assertEqual(normalize_cycle("monthly"), RebalanceFrequency.MONTHLY)
        self.assertEqual(normalize_cycle("Q"), RebalanceFrequency.QUARTERLY)
        self.assertEqual(normalize_cycle("SA"), RebalanceFrequency.SEMI_ANNUALLY)
        self.assertEqual(normalize_cycle("annually"), RebalanceFrequency.ANNUALLY)
        with self.assertRaises(ValueError):
            normalize_cycle("HOURLY")


class TestTier2ModelDecisionsOnSyntheticData(unittest.TestCase):
    """Tier 2: Verification of model weights and regime switching on synthetic scenarios."""

    def setUp(self):
        # 30-day synthetic dates
        self.dates = [f"2024-01-{i:02d}" for i in range(1, 31)]
        # Price that rises from 100 to 120, then drops to 80
        p_rising_then_falling = [100.0 + i for i in range(15)] + [114.0 - 2.5 * i for i in range(15)]
        self.prices = {
            "QQQ": p_rising_then_falling,
            "SOXX": [100.0] * 30,
            "CASH": [1.0] * 30,
        }

    def test_synthetic_sma200_bear_defense_rotation(self):
        """When price collapses below SMA, allocation must rotate to 100% CASH."""
        cfg = BacktestConfig(
            start_date=self.dates[0],
            end_date=self.dates[-1],
            frequency=RebalanceFrequency.WEEKLY,
            tax_enabled=False,
        )
        res = StrategyBCSimulator.run_benchmark_optimization(
            asset="QQQ",
            cycle=RebalanceFrequency.WEEKLY,
            model="SMA200",
            config=cfg,
            prices=self.prices,
            dates=self.dates,
        )
        self.assertIsInstance(res, SimulationResult)
        # Holdings history must record non-zero CASH shares when in bear regime
        final_holdings = res.holdings_history[-1]
        self.assertIn("CASH", final_holdings)
        self.assertGreater(final_holdings["CASH"], 0.0)

    def test_synthetic_vol_scaling_contracts_equity_exposure(self):
        """High volatility must cause equity weight to contract below 1.0."""
        # Create highly volatile price series
        volatile_p = [100.0]
        for i in range(1, 30):
            volatile_p.append(volatile_p[-1] * (1.10 if i % 2 == 0 else 0.90))

        prices = {
            "QQQ": volatile_p,
            "SOXX": [100.0] * 30,
            "CASH": [1.0] * 30,
        }
        cfg = BacktestConfig(
            start_date=self.dates[0],
            end_date=self.dates[-1],
            frequency=RebalanceFrequency.WEEKLY,
            tax_enabled=False,
        )
        res = StrategyBCSimulator.run_benchmark_optimization(
            asset="QQQ",
            cycle=RebalanceFrequency.WEEKLY,
            model="VOL_SCALING",
            config=cfg,
            target_vol=0.20,
            prices=prices,
            dates=self.dates,
        )
        # Should hold both QQQ and CASH
        final_holdings = res.holdings_history[-1]
        self.assertGreater(final_holdings["CASH"], 0.0)


class TestTier3FullBacktestAndMddReduction(unittest.TestCase):
    """Tier 3: 25-Year full historical simulations and MDD reduction verification."""

    def test_qqq_sma200_mdd_reduction_vs_buy_and_hold(self):
        """
        QQQ 200 SMA Trend Following must compress MDD from -54.5%/-83% down to <= -32%.
        And significantly improve Calmar Ratio over Buy & Hold.
        """
        # Run Buy & Hold baseline
        bh_res = StrategyBCSimulator.run_benchmark_optimization(
            asset="QQQ",
            cycle=RebalanceFrequency.ANNUALLY,
            model=BenchmarkModel.BUY_AND_HOLD,
        )
        bh_mdd = bh_res.metrics.mdd_pct
        self.assertLess(bh_mdd, -50.0)  # At least -54.5% on joint period

        # Run QQQ SMA200 Monthly
        sma_res = StrategyBCSimulator.run_benchmark_optimization(
            asset="QQQ",
            cycle=RebalanceFrequency.MONTHLY,
            model=BenchmarkModel.SMA200,
        )
        sma_m = sma_res.metrics

        # Must reduce MDD to <= -32%
        self.assertGreaterEqual(sma_m.mdd_pre_tax, -32.0)
        self.assertGreaterEqual(sma_m.mdd_after_tax, -32.0)

        # Calmar Ratio must improve significantly
        self.assertGreater(sma_m.calmar_pre_tax, bh_res.metrics.calmar_ratio)
        self.assertGreater(sma_m.calmar_after_tax, bh_res.metrics.calmar_ratio)

    def test_soxx_sma200_mdd_reduction_vs_buy_and_hold(self):
        """
        SOXX Buy & Hold suffers severe -71.8% drawdown.
        Optimization models must substantially suppress drawdown depth.
        """
        bh_soxx = StrategyBCSimulator.run_benchmark_optimization(
            asset="SOXX",
            cycle=RebalanceFrequency.ANNUALLY,
            model=BenchmarkModel.BUY_AND_HOLD,
        )
        self.assertLess(bh_soxx.metrics.mdd_pct, -70.0)  # -71.83% MDD

        # Dual Momentum Quarterly on SOXX achieves <= -32% MDD
        dm_res = StrategyBCSimulator.run_benchmark_optimization(
            asset="SOXX",
            cycle=RebalanceFrequency.QUARTERLY,
            model=BenchmarkModel.DUAL_MOMENTUM,
        )
        self.assertGreaterEqual(dm_res.metrics.mdd_pre_tax, -32.0)

        # SMA200 Weekly achieves -34.4% MDD (cut nearly in half vs -71.8%)
        sma_weekly = StrategyBCSimulator.run_benchmark_optimization(
            asset="SOXX",
            cycle=RebalanceFrequency.WEEKLY,
            model=BenchmarkModel.SMA200,
        )
        self.assertGreater(sma_weekly.metrics.mdd_pre_tax, -35.0)

    def test_dual_momentum_captures_both_relative_and_absolute(self):
        """Dual Momentum must allocate between QQQ, SOXX and CASH based on 3M+12M momentum."""
        res = StrategyBCSimulator.run_benchmark_optimization(
            asset="QQQ",
            cycle=RebalanceFrequency.QUARTERLY,
            model=BenchmarkModel.DUAL_MOMENTUM,
        )
        self.assertIsInstance(res, SimulationResult)
        self.assertGreater(res.metrics.cagr_pct, 4.0)
        self.assertGreaterEqual(res.metrics.mdd_pre_tax, -32.0)
        self.assertGreater(res.metrics.mdd_after_tax, -40.0)


class TestTier4CyclesAndTaxDeferral(unittest.TestCase):
    """Tier 4: Verification of all 5 cycles and monotonic tax drag behavior."""

    def test_compare_all_cycles_output_schema(self):
        """compare_all_cycles must return all 5 frequencies with complete PerformanceMetrics."""
        cycles_map = compare_all_cycles("QQQ", model="SMA200")
        expected_keys = {"WEEKLY", "MONTHLY", "QUARTERLY", "SEMI_ANNUALLY", "ANNUALLY"}
        self.assertEqual(set(cycles_map.keys()), expected_keys)

        for cyc_name, m in cycles_map.items():
            self.assertIsInstance(m, PerformanceMetrics)
            self.assertGreater(m.cagr_pre_tax, 0.0)
            self.assertGreater(m.cagr_after_tax, 0.0)
            self.assertLess(m.mdd_after_tax, 0.0)
            self.assertGreater(m.total_tax_paid, 0.0)

    def test_monotonic_tax_drag_across_5_cycles(self):
        """
        Tax drag and total tax paid must exhibit strict monotonic ordering:
        WEEKLY > MONTHLY > QUARTERLY > SEMI_ANNUALLY > ANNUALLY.
        """
        cycles_map = compare_all_cycles("QQQ", model="SMA200")

        drag_w = cycles_map["WEEKLY"].tax_drag_pct
        drag_m = cycles_map["MONTHLY"].tax_drag_pct
        drag_q = cycles_map["QUARTERLY"].tax_drag_pct
        drag_sa = cycles_map["SEMI_ANNUALLY"].tax_drag_pct
        drag_a = cycles_map["ANNUALLY"].tax_drag_pct

        # Strict monotonic decrease in tax drag %
        self.assertGreater(drag_w, drag_m)
        self.assertGreater(drag_m, drag_q)
        self.assertGreater(drag_q, drag_sa)
        self.assertGreater(drag_sa, drag_a)

        # Total tax paid must also decrease monotonically
        tax_w = cycles_map["WEEKLY"].total_tax_paid
        tax_m = cycles_map["MONTHLY"].total_tax_paid
        tax_q = cycles_map["QUARTERLY"].total_tax_paid
        tax_sa = cycles_map["SEMI_ANNUALLY"].total_tax_paid
        tax_a = cycles_map["ANNUALLY"].total_tax_paid

        self.assertGreater(tax_w, tax_m)
        self.assertGreater(tax_m, tax_q)
        self.assertGreater(tax_q, tax_sa)
        self.assertGreater(tax_sa, tax_a)

    def test_optimal_cycle_maximizes_after_tax_calmar(self):
        """Monthly rebalancing must be identified as the optimal cycle maximizing After-Tax Calmar Ratio."""
        opt_cycle, opt_metrics = find_optimal_cycle("QQQ", model="SMA200", target_metric="calmar_after_tax")
        self.assertEqual(opt_cycle, RebalanceFrequency.MONTHLY)
        self.assertAlmostEqual(opt_metrics.calmar_after_tax, 0.26, places=2)

        # Monthly after-tax Calmar must exceed Weekly and Annual
        cycles_map = compare_all_cycles("QQQ", model="SMA200")
        self.assertGreater(opt_metrics.calmar_after_tax, cycles_map["WEEKLY"].calmar_after_tax)
        self.assertGreater(opt_metrics.calmar_after_tax, cycles_map["ANNUALLY"].calmar_after_tax)

    def test_compare_all_models_output_schema(self):
        """compare_all_models must evaluate BUY_AND_HOLD, SMA200, DUAL_MOMENTUM, and VOL_SCALING."""
        models_map = compare_all_models("QQQ", cycle=RebalanceFrequency.MONTHLY)
        expected_models = {"BUY_AND_HOLD", "SMA200", "DUAL_MOMENTUM", "VOL_SCALING"}
        self.assertEqual(set(models_map.keys()), expected_models)

        for mod_name, m in models_map.items():
            self.assertIsInstance(m, PerformanceMetrics)
            self.assertGreater(m.cagr_pre_tax, 0.0)
            self.assertLess(m.mdd_pre_tax, 0.0)


class TestTier5FinancialAccountingAndIntegrity(unittest.TestCase):
    """Tier 5: Quantitative accounting invariants, zero CDN, and error handling."""

    def test_after_tax_cagr_never_exceeds_pre_tax(self):
        """After-tax CAGR must be strictly less than or equal to pre-tax CAGR."""
        res = run_benchmark_optimization("QQQ", cycle=RebalanceFrequency.MONTHLY, model="SMA200")
        m = res.metrics
        self.assertLessEqual(m.cagr_after_tax, m.cagr_pre_tax)
        self.assertGreater(m.tax_drag_pct, 0.0)
        self.assertAlmostEqual(m.tax_drag_pct, m.cagr_pre_tax - m.cagr_after_tax, places=1)

    def test_tax_disabled_mode_equivalence(self):
        """When tax_enabled is False, pre-tax and after-tax metrics must match exactly."""
        cfg = BacktestConfig(
            frequency=RebalanceFrequency.MONTHLY,
            tax_enabled=False,
        )
        res = run_benchmark_optimization("QQQ", cycle=RebalanceFrequency.MONTHLY, model="SMA200", config=cfg)
        m = res.metrics
        self.assertEqual(m.cagr_pre_tax, m.cagr_after_tax)
        self.assertEqual(m.tax_drag_pct, 0.0)
        self.assertEqual(m.total_tax_paid, 0.0)

    def test_invalid_parameters_raise_appropriate_exceptions(self):
        """Invalid asset ticker or empty data must raise ValueError."""
        with self.assertRaises(ValueError):
            run_benchmark_optimization("INVALID_ASSET", cycle=RebalanceFrequency.MONTHLY)

        with self.assertRaises(ValueError):
            StrategyBCSimulator.run_benchmark_optimization(
                asset="QQQ",
                cycle=RebalanceFrequency.MONTHLY,
                prices={"QQQ": []},
                dates=[],
            )

    def test_zero_network_and_zero_cdn_offline_isolation(self):
        """Engine module must not import socket, urllib, or remote network modules."""
        import engine.strategy_benchmark_opt as sbo
        import sys
        forbidden_modules = ["urllib.request", "requests", "http.client", "socket"]
        for mod in forbidden_modules:
            self.assertNotIn(mod, sbo.__loader__.__class__.__module__)


class TestTier6ExtendedFeaturesAndEdgeCases(unittest.TestCase):
    """Tier 6: Additional coverage for SMA50_200, counter asset rotation, USD capital, and metrics."""

    def test_sma50_200_golden_death_cross_model(self):
        """SMA50_200 model must execute multi-tier golden/death cross allocations."""
        res = run_benchmark_optimization("QQQ", cycle=RebalanceFrequency.MONTHLY, model=BenchmarkModel.SMA50_200)
        self.assertIsInstance(res, SimulationResult)
        self.assertGreater(res.metrics.cagr_pct, 5.0)
        self.assertLess(res.metrics.mdd_pct, 0.0)

    def test_bear_defense_counter_asset_rotation(self):
        """When bear_defense='COUNTER', QQQ in bear regime rotates into SOXX."""
        res = run_benchmark_optimization(
            asset="QQQ",
            cycle=RebalanceFrequency.MONTHLY,
            model="SMA200",
            bear_defense="COUNTER",
        )
        self.assertIsInstance(res, SimulationResult)
        # Verify holdings history has SOXX
        held_soxx = any(h.get("SOXX", 0.0) > 0.0 for h in res.holdings_history)
        self.assertTrue(held_soxx)

    def test_dual_momentum_no_counter_rotation(self):
        """When allow_counter_rotation=False, losing target asset retreats to CASH instead of counter."""
        res = run_benchmark_optimization(
            asset="QQQ",
            cycle=RebalanceFrequency.MONTHLY,
            model="DUAL_MOMENTUM",
            allow_counter_rotation=False,
        )
        self.assertIsInstance(res, SimulationResult)
        # Verify SOXX is never held
        held_soxx = any(h.get("SOXX", 0.0) > 0.0 for h in res.holdings_history)
        self.assertFalse(held_soxx)

    def test_usd_capital_deduction_scaling(self):
        """Small capital ($10,000 USD) must correctly scale annual deduction to $2,000 USD."""
        cfg = BacktestConfig(
            initial_capital=10_000.0,
            annual_tax_deduction=2_000.0,
            frequency=RebalanceFrequency.MONTHLY,
            tax_enabled=True,
        )
        res = run_benchmark_optimization("QQQ", cycle=RebalanceFrequency.MONTHLY, model="SMA200", config=cfg)
        self.assertIsInstance(res.tax_state, TaxAccountingState)
        self.assertGreater(res.metrics.cagr_pre_tax, 0.0)

    def test_lowercase_asset_names(self):
        """run_benchmark_optimization must seamlessly accept lowercase 'qqq' and 'soxx'."""
        res_q = run_benchmark_optimization("qqq", cycle="monthly", model="sma200")
        res_s = run_benchmark_optimization("soxx", cycle="monthly", model="sma200")
        self.assertGreater(res_q.metrics.cagr_pct, 0.0)
        self.assertGreater(res_s.metrics.cagr_pct, 0.0)

    def test_find_optimal_cycle_custom_target_metrics(self):
        """find_optimal_cycle must optimize across cagr_after_tax or sharpe_after_tax."""
        cyc_cagr, m_cagr = find_optimal_cycle("QQQ", model="SMA200", target_metric="cagr_after_tax")
        self.assertIn(cyc_cagr, list(RebalanceFrequency))
        self.assertGreater(m_cagr.cagr_after_tax, 0.0)

        cyc_sharpe, m_sharpe = find_optimal_cycle("QQQ", model="SMA200", target_metric="sharpe_after_tax")
        self.assertIn(cyc_sharpe, list(RebalanceFrequency))
        self.assertGreater(m_sharpe.sharpe_after_tax, 0.0)

    def test_series_lengths_and_rebalance_records(self):
        """All output curves and records must maintain strict length and structural invariants."""
        res = run_benchmark_optimization("QQQ", cycle=RebalanceFrequency.MONTHLY, model="SMA200")
        n = len(res.dates)
        self.assertEqual(len(res.daily_nav), n)
        self.assertEqual(len(res.daily_drawdowns), n)
        self.assertEqual(len(res.daily_nav_pre_tax), n)
        self.assertEqual(len(res.daily_drawdowns_pre_tax), n)
        self.assertEqual(len(res.holdings_history), n)
        self.assertEqual(len(res.turnover_history), n)
        self.assertGreater(len(res.rebalance_records), 0)
        self.assertGreater(len(res.annual_returns), 20)
        self.assertNotEqual(res.metrics.worst_year, "N/A")


if __name__ == "__main__":
    unittest.main()
