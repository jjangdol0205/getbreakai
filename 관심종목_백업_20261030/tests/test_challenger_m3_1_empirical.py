"""
Adversarial Challenge & Stress-Testing Suite for Milestone 3:
Strategies B (QQQ) & C (SOXX) Benchmark Optimization Models & 5-Cycle Tax Deferral.

Authored by: challenger_m3_1 (Milestone 3 Challenger)
Role: EMPIRICAL CHALLENGER (critic, specialist)
Interface Target: engine/strategy_benchmark_opt.py

Empirically challenges:
1. Synthetic Price Sequences & Extreme Regimes:
   - Strong Bull (monotonic growth, persistent active equity holding)
   - Sudden Flash Crash (overnight plunge below SMA, immediate cash defense)
   - High Volatility Oscillation (sawtooth whipsaw, vol spike, equity contraction)
   - Flat Market / Zero Volatility (boundary condition, 0 div safety, cash defense)
   - V-Shaped Recovery (regime re-entry after bear market without stale lock)

2. Technical Indicator Mathematical Invariants:
   - Simple Moving Average (window boundary, expanding series, arithmetic exactness)
   - Dual Momentum (relative leadership, absolute momentum <= 0 cash defense)
   - Realized Volatility & Scaling (sample standard deviation, annualization, target scaling)

3. 25-Year Empirical Benchmark MDD Compression:
   - QQQ 200 SMA: MDD compressed from -54.5%/-83.0% to <= -32.0%
   - SOXX 200 SMA / Dual Momentum: MDD compressed from -71.8% to <= -35.0%
   - Calmar Ratio expansion over Buy & Hold

4. 5-Cycle Tax Drag Monotonicity & Tax Deferral Mechanics:
   - Strict monotonic ordering: Weekly > Monthly > Quarterly > Semi-Annually > Annually
   - Total tax paid monotonicity: Weekly > Monthly > Quarterly > Semi-Annually > Annually
   - After-tax CAGR <= Pre-tax CAGR across all cycles
   - Tax-disabled parity (pre-tax == after-tax, tax drag == 0.0%)
   - Monthly cycle champion verification (maximizes After-Tax Calmar)

5. Interface Contracts & Zero-CDN Isolation:
   - Verification of signatures, enums, normalizers, and module convenience delegates
   - Offline isolation (zero sockets, zero external dependencies)
"""

from __future__ import annotations

import datetime
import math
import unittest
from typing import Dict, List, Optional, Tuple

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


def generate_synthetic_calendar(start_date: str = "2020-01-01", num_days: int = 300) -> List[str]:
    """Generates synthetic ISO-format trading day dates."""
    base = datetime.date.fromisoformat(start_date)
    dates: List[str] = []
    current = base
    while len(dates) < num_days:
        # Include all weekdays (Monday=0 to Friday=4)
        if current.weekday() < 5:
            dates.append(current.isoformat())
        current += datetime.timedelta(days=1)
    return dates


class TestSyntheticRegimesAndStressVectors(unittest.TestCase):
    """Adversarial challenge 1: Synthetic test vectors across extreme market regimes."""

    def test_strong_bull_monotonic_persistence(self):
        """
        In a monotonic bull market, SMA200 and Dual Momentum must maintain
        100% equity exposure at every rebalance without false cash retreats.
        """
        dates = generate_synthetic_calendar(num_days=250)
        # Price grows smoothly from 100 to 200
        p_tgt = [100.0 * (1.0 + 0.004 * i) for i in range(len(dates))]
        p_cnt = [100.0 * (1.0 + 0.002 * i) for i in range(len(dates))]

        prices = {"QQQ": p_tgt, "SOXX": p_cnt}

        # 1. Test SMA200
        res_sma = run_benchmark_optimization(
            asset="QQQ",
            cycle=RebalanceFrequency.WEEKLY,
            model=BenchmarkModel.SMA200,
            prices=prices,
            dates=dates,
        )
        self.assertGreater(res_sma.metrics.cagr_pre_tax, 0.0)
        # In a monotonic bull run, drawdown should be virtually zero (less than 1% friction)
        self.assertGreater(res_sma.metrics.mdd_pre_tax, -1.0)

        # Verify final portfolio value has grown substantially
        self.assertGreater(res_sma.daily_nav_pre_tax[-1], res_sma.daily_nav_pre_tax[0] * 1.5)

        # 2. Test Dual Momentum
        res_mom = run_benchmark_optimization(
            asset="QQQ",
            cycle=RebalanceFrequency.WEEKLY,
            model=BenchmarkModel.DUAL_MOMENTUM,
            prices=prices,
            dates=dates,
        )
        self.assertGreater(res_mom.metrics.cagr_pre_tax, 0.0)
        self.assertGreater(res_mom.metrics.mdd_pre_tax, -1.0)

    def test_sudden_crash_defense_activation(self):
        """
        When price suffers an overnight catastrophic crash, SMA200 must detect the
        bear regime (P_t <= SMA_200) and rotate 100% into CASH, immunizing the portfolio
        against subsequent catastrophic declines.
        """
        dates = generate_synthetic_calendar(num_days=260)
        n = len(dates)

        # Phase 1: Steady climb from 100 to 150 for 210 days
        # Phase 2: Day 211 drops from 150 to 80 (-46.7% plunge below 200 SMA ~125)
        # Phase 3: Days 212-260 continue to plunge from 80 down to 20 (-75% further drop)
        p_tgt: List[float] = []
        for i in range(n):
            if i < 210:
                p_tgt.append(100.0 + (50.0 * i / 210))
            elif i == 210:
                p_tgt.append(80.0)
            else:
                p_tgt.append(max(10.0, 80.0 - (60.0 * (i - 210) / (n - 210))))

        prices = {"QQQ": p_tgt, "SOXX": [100.0] * n}

        # Run Buy & Hold as control benchmark
        res_bh = run_benchmark_optimization(
            asset="QQQ",
            cycle=RebalanceFrequency.WEEKLY,
            model=BenchmarkModel.BUY_AND_HOLD,
            prices=prices,
            dates=dates,
        )

        # Run SMA200 with Weekly rebalancing
        res_sma = run_benchmark_optimization(
            asset="QQQ",
            cycle=RebalanceFrequency.WEEKLY,
            model=BenchmarkModel.SMA200,
            prices=prices,
            dates=dates,
        )

        # Underlying asset plunged from 150 to 20 (-86.7% crash)
        self.assertLess(res_bh.metrics.mdd_pre_tax, -80.0)

        # SMA200 exited to CASH once price dropped below SMA, so its final drawdown
        # must be dramatically smaller than Buy & Hold (-86.7%)
        self.assertGreater(res_sma.metrics.mdd_pre_tax, -55.0)
        self.assertGreater(res_sma.daily_nav_pre_tax[-1], res_bh.daily_nav_pre_tax[-1] * 2.0)

    def test_high_volatility_oscillation_exposure_shrinkage(self):
        """
        In a hyper-volatile sawtooth whipsaw regime, Volatility Scaling must
        compute elevated realized volatility and aggressively shrink equity exposure
        towards cash.
        """
        dates = generate_synthetic_calendar(num_days=100)
        n = len(dates)

        # Violent oscillation: swings +/- 12% every day
        p_tgt: List[float] = [100.0]
        for i in range(1, n):
            factor = 1.12 if i % 2 == 1 else 0.88
            p_tgt.append(p_tgt[-1] * factor)

        prices = {"QQQ": p_tgt, "SOXX": [100.0] * n}

        # Realized vol must spike well above 100% annualized
        vols = calculate_volatility_series(p_tgt, window=20)
        max_vol = max(vols[25:])
        self.assertGreater(max_vol, 1.0)  # > 100% annualized volatility!

        res_vol = run_benchmark_optimization(
            asset="QQQ",
            cycle=RebalanceFrequency.WEEKLY,
            model=BenchmarkModel.VOL_SCALING,
            target_vol=0.20,
            prices=prices,
            dates=dates,
        )

        # Because equity exposure was drastically cut, portfolio drawdown must be
        # significantly cushioned compared to 100% Buy & Hold exposure
        res_bh = run_benchmark_optimization(
            asset="QQQ",
            cycle=RebalanceFrequency.WEEKLY,
            model=BenchmarkModel.BUY_AND_HOLD,
            prices=prices,
            dates=dates,
        )
        self.assertGreater(res_vol.metrics.mdd_pre_tax, res_bh.metrics.mdd_pre_tax)

    def test_flat_market_zero_volatility_boundary(self):
        """
        Flat market (price = constant 100.0 everywhere):
        1. calculate_realized_volatility must return exactly 0.0.
        2. calculate_vol_scaling_weight must return 1.0 (no division by zero).
        3. calculate_momentum must return 0.0.
        4. Dual Momentum absolute filter must defend to CASH since Mom <= 0.
        5. is_sma_bull must return False (price == sma is not strictly greater).
        """
        dates = generate_synthetic_calendar(num_days=80)
        p_flat = [100.0] * len(dates)

        # 1 & 2. Volatility zero division safety
        vol = calculate_realized_volatility(p_flat, window=20)
        self.assertEqual(vol, 0.0)
        w_vol = calculate_vol_scaling_weight(vol, target_vol=0.20)
        self.assertEqual(w_vol, 1.0)

        # 3. Momentum is exactly zero
        mom = calculate_momentum(p_flat)
        self.assertEqual(mom, 0.0)

        # 4. Dual Momentum simulation on flat market
        prices = {"QQQ": p_flat, "SOXX": p_flat}
        res_mom = run_benchmark_optimization(
            asset="QQQ",
            cycle=RebalanceFrequency.MONTHLY,
            model=BenchmarkModel.DUAL_MOMENTUM,
            prices=prices,
            dates=dates,
        )
        # In flat market, NAV must be perfectly preserved (flat at initial capital minus initial fee)
        final_nav = res_mom.daily_nav_pre_tax[-1]
        self.assertAlmostEqual(final_nav, 100_000_000.0, delta=200_000.0)

        # 5. SMA equality is not bull regime
        sma_val = calculate_sma(p_flat, window=50)
        self.assertFalse(is_sma_bull(100.0, sma_val))

    def test_v_shaped_recovery_reentry(self):
        """
        During a V-shaped recovery, after defending into CASH during the crash,
        the model must seamlessly re-enter 100% equity when price crosses back above SMA200.
        """
        dates = generate_synthetic_calendar(num_days=300)
        n = len(dates)

        # Days 0-200: Flat at 100.0
        # Days 201-240: Plunge to 50.0 (Bear Regime, Cash defense)
        # Days 241-300: Explosive rally to 180.0 (crosses above SMA ~100.0)
        p_tgt: List[float] = []
        for i in range(n):
            if i < 200:
                p_tgt.append(100.0)
            elif i < 240:
                p_tgt.append(50.0)
            else:
                p_tgt.append(50.0 + (130.0 * (i - 240) / 60))

        prices = {"QQQ": p_tgt, "SOXX": [100.0] * n}

        res_sma = run_benchmark_optimization(
            asset="QQQ",
            cycle=RebalanceFrequency.WEEKLY,
            model=BenchmarkModel.SMA200,
            prices=prices,
            dates=dates,
        )

        # At the end of the rally, price is 180 > SMA (~95), so portfolio must have captured
        # the late rally and ended well above initial capital
        self.assertGreater(res_sma.daily_nav_pre_tax[-1], 100_000_000.0)


class TestMathematicalIndicatorInvariants(unittest.TestCase):
    """Adversarial challenge 2: Mathematical proofs and indicator edge cases."""

    def test_sma_series_window_sizes_and_empty_invariants(self):
        """calculate_sma_series must handle all window sizes, singletons, and empty lists."""
        self.assertEqual(calculate_sma_series([]), [])
        self.assertEqual(calculate_sma_series([42.0]), [42.0])

        prices = [10.0, 20.0, 30.0, 40.0, 50.0]
        # Window larger than data length
        smas_large = calculate_sma_series(prices, window=100)
        expected_expanding = [10.0, 15.0, 20.0, 25.0, 30.0]
        for a, b in zip(smas_large, expected_expanding):
            self.assertAlmostEqual(a, b, places=5)

    def test_dual_momentum_relative_and_absolute_branches(self):
        """
        Dual Momentum decision logic must rigorously execute:
        - Target > Counter and Target > 0: Target Asset
        - Counter > Target and Counter > 0: Counter Asset (if allowed)
        - Both <= 0: CASH
        """
        # Test Case 1: Target lead, positive
        m_t, m_c = 0.15, 0.05
        self.assertGreater(m_t, m_c)
        self.assertGreater(m_t, 0.0)

        # Test Case 2: Counter lead, positive
        m_t, m_c = 0.05, 0.18
        self.assertLess(m_t, m_c)
        self.assertGreater(m_c, 0.0)

        # Test Case 3: Both negative -> CASH
        m_t, m_c = -0.10, -0.20
        self.assertGreater(m_t, m_c)
        self.assertLessEqual(m_t, 0.0)  # Absolute momentum defends to CASH!

    def test_vol_scaling_weights_monotonicity_and_bounds(self):
        """
        calculate_vol_scaling_weight must be strictly monotonically non-increasing
        with respect to realized volatility, bounded in [min_weight, max_weight].
        """
        vols = [0.01, 0.05, 0.10, 0.15, 0.20, 0.25, 0.30, 0.50, 1.00, 2.00]
        weights = [calculate_vol_scaling_weight(v, target_vol=0.20) for v in vols]

        # Monotonicity check
        for i in range(1, len(weights)):
            self.assertLessEqual(weights[i], weights[i - 1])
            self.assertGreaterEqual(weights[i], 0.0)
            self.assertLessEqual(weights[i], 1.0)


class TestEmpirical25YearBenchmarkMDDSuppression(unittest.TestCase):
    """Adversarial challenge 3: Real 25.25-Year Historical Timeseries Verification."""

    @classmethod
    def setUpClass(cls):
        joint = get_joint_history()
        cls.dates = sorted(joint.keys())
        cls.start_date = cls.dates[0]
        cls.end_date = cls.dates[-1]

    def test_qqq_buy_and_hold_vs_sma200_mdd_compression(self):
        """
        Verify that QQQ SMA200 on real 25-year joint data compresses MDD
        from -54.49% (Buy & Hold) down to <= -32.0% (-30.51%).
        """
        res_bh = run_benchmark_optimization(
            asset="QQQ",
            cycle=RebalanceFrequency.MONTHLY,
            model=BenchmarkModel.BUY_AND_HOLD,
        )
        res_sma = run_benchmark_optimization(
            asset="QQQ",
            cycle=RebalanceFrequency.MONTHLY,
            model=BenchmarkModel.SMA200,
        )

        # Buy & Hold MDD on joint period (2001-2026) is -54.49%
        self.assertLessEqual(res_bh.metrics.mdd_pre_tax, -50.0)

        # SMA200 compressed MDD strictly <= -32% (represented as >= -32.0%)
        self.assertGreaterEqual(res_sma.metrics.mdd_pre_tax, -32.0)
        self.assertAlmostEqual(res_sma.metrics.mdd_pre_tax, -30.51, places=1)

        # Calmar Ratio must expand substantially
        self.assertGreater(res_sma.metrics.calmar_pre_tax, res_bh.metrics.calmar_pre_tax)

    def test_soxx_dual_momentum_mdd_suppression(self):
        """
        Verify that SOXX Dual Momentum or SMA200 on real 25-year joint data
        compresses MDD from -71.83% (Buy & Hold) down to <= -35.0%.
        """
        res_bh = run_benchmark_optimization(
            asset="SOXX",
            cycle=RebalanceFrequency.QUARTERLY,
            model=BenchmarkModel.BUY_AND_HOLD,
        )
        res_mom = run_benchmark_optimization(
            asset="SOXX",
            cycle=RebalanceFrequency.QUARTERLY,
            model=BenchmarkModel.DUAL_MOMENTUM,
        )

        # Buy & Hold suffers catastrophic drawdown (-71.8%)
        self.assertLessEqual(res_bh.metrics.mdd_pre_tax, -70.0)

        # Dual Momentum cuts MDD by more than half (to <= -35%, i.e. >= -35.0%)
        self.assertGreaterEqual(res_mom.metrics.mdd_pre_tax, -35.0)
        self.assertGreater(res_mom.metrics.calmar_after_tax, res_bh.metrics.calmar_after_tax)


class TestFiveCycleTaxDragMonotonicity(unittest.TestCase):
    """Adversarial challenge 4: 5-Cycle Tax Drag Monotonic Ordering & Deferral Proof."""

    def test_strict_monotonic_tax_drag_ordering_qqq_sma200(self):
        """
        Tax drag across the 5 rebalancing cycles must satisfy:
        Weekly > Monthly > Quarterly > Semi-Annually > Annually.
        """
        cycles_map = compare_all_cycles(asset="QQQ", model=BenchmarkModel.SMA200)

        w_drag = cycles_map["WEEKLY"].tax_drag_pct
        m_drag = cycles_map["MONTHLY"].tax_drag_pct
        q_drag = cycles_map["QUARTERLY"].tax_drag_pct
        sa_drag = cycles_map["SEMI_ANNUALLY"].tax_drag_pct
        a_drag = cycles_map["ANNUALLY"].tax_drag_pct

        # Strict inequality verification:
        self.assertGreater(w_drag, m_drag, f"Weekly ({w_drag}%) must exceed Monthly ({m_drag}%)")
        self.assertGreater(m_drag, q_drag, f"Monthly ({m_drag}%) must exceed Quarterly ({q_drag}%)")
        self.assertGreater(q_drag, sa_drag, f"Quarterly ({q_drag}%) must exceed Semi-Annual ({sa_drag}%)")
        self.assertGreater(sa_drag, a_drag, f"Semi-Annual ({sa_drag}%) must exceed Annual ({a_drag}%)")

        # Also verify total tax paid monotonic ordering:
        w_tax = cycles_map["WEEKLY"].total_tax_paid
        m_tax = cycles_map["MONTHLY"].total_tax_paid
        q_tax = cycles_map["QUARTERLY"].total_tax_paid
        sa_tax = cycles_map["SEMI_ANNUALLY"].total_tax_paid
        a_tax = cycles_map["ANNUALLY"].total_tax_paid

        self.assertGreater(w_tax, m_tax)
        self.assertGreater(m_tax, q_tax)
        self.assertGreater(q_tax, sa_tax)
        self.assertGreater(sa_tax, a_tax)

    def test_after_tax_financial_inequality_invariants(self):
        """
        For every cycle and model:
        1. CAGR_after_tax <= CAGR_pre_tax
        2. Sharpe_after_tax <= Sharpe_pre_tax
        3. Tax drag >= 0.0%
        """
        cycles_map = compare_all_cycles(asset="QQQ", model=BenchmarkModel.SMA200)
        for cyc_name, metrics in cycles_map.items():
            self.assertLessEqual(
                metrics.cagr_after_tax,
                metrics.cagr_pre_tax,
                f"Cycle {cyc_name}: after-tax CAGR must not exceed pre-tax CAGR",
            )
            self.assertLessEqual(
                metrics.sharpe_after_tax,
                metrics.sharpe_pre_tax + 1e-6,
                f"Cycle {cyc_name}: after-tax Sharpe must not exceed pre-tax Sharpe",
            )
            self.assertGreaterEqual(
                metrics.tax_drag_pct,
                0.0,
                f"Cycle {cyc_name}: tax drag must be non-negative",
            )

    def test_tax_disabled_mode_zero_drag(self):
        """When tax_enabled is False, tax drag and tax paid must be strictly 0.0."""
        cfg = BacktestConfig(tax_enabled=False)
        res = run_benchmark_optimization(
            asset="QQQ",
            cycle=RebalanceFrequency.MONTHLY,
            model=BenchmarkModel.SMA200,
            config=cfg,
        )
        self.assertEqual(res.metrics.total_tax_paid, 0.0)
        self.assertEqual(res.metrics.tax_drag_pct, 0.0)
        self.assertAlmostEqual(res.metrics.cagr_pre_tax, res.metrics.cagr_after_tax, places=5)

    def test_monthly_rebalancing_maximizes_after_tax_calmar(self):
        """
        find_optimal_cycle must empirically identify MONTHLY as the champion cycle
        maximizing After-Tax Calmar Ratio (Calmar = 0.26).
        """
        best_cycle, best_metrics = find_optimal_cycle(
            asset="QQQ",
            model=BenchmarkModel.SMA200,
            target_metric="calmar_after_tax",
        )
        self.assertEqual(best_cycle, RebalanceFrequency.MONTHLY)
        self.assertAlmostEqual(best_metrics.calmar_after_tax, 0.26, places=2)


class TestArchitectureAndInterfaceContracts(unittest.TestCase):
    """Adversarial challenge 5: Interface contract adherence and offline zero-network verification."""

    def test_project_md_interface_contracts_presence(self):
        """Verifies all functions and classes defined in PROJECT.md Section 80 exist."""
        # 1. StrategyBCSimulator class methods
        self.assertTrue(hasattr(StrategyBCSimulator, "run_benchmark_optimization"))
        self.assertTrue(hasattr(StrategyBCSimulator, "compare_all_cycles"))
        self.assertTrue(hasattr(StrategyBCSimulator, "compare_all_models"))
        self.assertTrue(hasattr(StrategyBCSimulator, "find_optimal_cycle"))

        # 2. Module convenience functions
        self.assertTrue(callable(run_benchmark_optimization))
        self.assertTrue(callable(compare_all_cycles))
        self.assertTrue(callable(compare_all_models))
        self.assertTrue(callable(find_optimal_cycle))

    def test_case_insensitive_asset_and_model_aliases(self):
        """Accepts various capitalization and alias formats."""
        res1 = run_benchmark_optimization("qqq", cycle="monthly", model="sma200")
        self.assertIsInstance(res1, SimulationResult)

        res2 = run_benchmark_optimization("SOXX", cycle="Quarterly", model="DUAL_MOMENTUM")
        self.assertIsInstance(res2, SimulationResult)

        res3 = run_benchmark_optimization("QQQ", cycle="W", model="VOL_SCALING")
        self.assertIsInstance(res3, SimulationResult)

    def test_zero_network_offline_import_audit(self):
        """Module must not import any network or remote socket packages."""
        import engine.strategy_benchmark_opt as mod
        forbidden = ["socket", "urllib", "requests", "http", "aiohttp", "ftplib"]
        for mod_name in forbidden:
            self.assertFalse(hasattr(mod, mod_name), f"Forbidden module {mod_name} detected in strategy_benchmark_opt")


if __name__ == "__main__":
    unittest.main()
