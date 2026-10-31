"""
Comprehensive Unit & Integration Test Suite for Milestone 4:
Strategy D 100% Equity Simplex Hybrid Master Optimizer & After-Tax Alpha Suite.

Validates:
1. Simplex Zero-Cash Invariant (Feature 12):
   - Strict validation of w_QQQ + w_SOXX + w_Turnaround = 1.0 and w_cash == 0.0.
   - Rejection of negative weights, sum != 1.0, cash leaks, and leverage.
   - Robust properties of HybridWeightVector.
2. 2D Simplex Grid Generator (Feature 13):
   - Step 0.10 yields exactly 66 triplets.
   - Step 0.05 yields exactly 231 triplets.
   - Every generated triplet satisfies the simplex invariant.
3. 25-Year Hybrid Compounding, Friction & Tax Modeling (Features 13, 23, 24):
   - Brokerage fee (0.10%) and slippage (0.08%) applied to turnover.
   - 22.0% foreign equity capital gains tax with 2,500,000 KRW annual deduction.
   - 5 rebalancing cycles (WEEKLY, MONTHLY, QUARTERLY, SEMI_ANNUALLY, ANNUALLY).
   - Strict monotonic tax drag ordering across rebalancing cycles.
4. Calmar Ratio Maximization & Champion Weight Selection (Feature 13):
   - 2D simplex grid search maximizes after-tax Calmar ratio.
   - Champion weight triplet selection with w_Turnaround > 0.
   - Superior Calmar and Sharpe ratios over pure benchmark mix (w_Turnaround = 0).
   - Champion cycle selection and cycle comparison matrix.
5. Turnaround Alpha Mathematical Attribution (Feature 14):
   - Positive convexity (+100% TP1 vs -10% stop loss, 10.0x ratio).
   - Empirical Pearson correlation matrix proving benchmark diversification.
   - Turnaround alpha proof (calmar and sharpe enhancement).
6. 100% Offline, Zero-CDN, Pure Python Standard Library Compliance.
"""

from __future__ import annotations

import math
import sys
import unittest
from typing import Any, Dict, List, Tuple

from engine.backtest_engine import (
    BacktestConfig,
    PerformanceMetrics,
    RebalanceFrequency,
    SimulationResult,
)
from engine.historical_data import (
    COMMON_START_DATE,
    COMMON_END_DATE,
    get_joint_history,
)
from engine.strategy_hybrid_master import (
    AlphaAttribution,
    HybridEvaluation,
    HybridOptimizationResult,
    HybridWeightVector,
    StrategyHybridMaster,
    compare_all_cycles,
    compute_alpha_attribution,
    generate_simplex_grid,
    get_hybrid_asset_prices,
    normalize_cycle,
    optimize_hybrid,
    simulate_hybrid,
    validate_simplex,
)


# ==============================================================================
# Tier 1: Simplex Zero-Cash Invariant Validation (Feature 12)
# ==============================================================================

class TestSimplexZeroCashValidation(unittest.TestCase):
    """Tier 1: Verifies strict 100% equity zero-cash simplex constraint validation."""

    def test_valid_simplex_weights_accepted(self) -> None:
        """Valid non-negative weights summing to 1.0 with w_cash == 0.0 must be accepted."""
        valid_triplets = [
            (0.35, 0.35, 0.30),
            (1.0, 0.0, 0.0),
            (0.0, 1.0, 0.0),
            (0.0, 0.0, 1.0),
            (0.5, 0.5, 0.0),
            (0.3333, 0.3333, 0.3334),
            (0.20, 0.40, 0.40),
            (0.05, 0.05, 0.90),
        ]
        for wq, ws, wt in valid_triplets:
            with self.subTest(wq=wq, ws=ws, wt=wt):
                self.assertTrue(
                    validate_simplex(wq, ws, wt),
                    f"Expected valid simplex for ({wq}, {ws}, {wt})"
                )
                vec = HybridWeightVector(w_qqq=wq, w_soxx=ws, w_turnaround=wt)
                self.assertTrue(vec.is_valid)
                self.assertEqual(vec.w_cash, 0.0)

    def test_negative_weights_rejected(self) -> None:
        """Any negative weight violates no-shorting simplex constraint and must be rejected."""
        invalid_negative = [
            (-0.10, 0.60, 0.50),
            (0.50, -0.20, 0.70),
            (0.50, 0.60, -0.10),
            (-0.01, 1.01, 0.00),
            (0.50, 0.50, -0.001),
        ]
        for wq, ws, wt in invalid_negative:
            with self.subTest(wq=wq, ws=ws, wt=wt):
                self.assertFalse(validate_simplex(wq, ws, wt))
                with self.assertRaises(ValueError):
                    HybridWeightVector(w_qqq=wq, w_soxx=ws, w_turnaround=wt)

    def test_sum_deviation_rejected(self) -> None:
        """Weight sums deviating from 1.0 (under-allocation or leverage) must be rejected."""
        deviating_triplets = [
            (0.50, 0.50, 0.10),   # sum = 1.10 (unbacked leverage)
            (0.30, 0.30, 0.30),   # sum = 0.90 (unallocated cash leak)
            (0.00, 0.00, 0.00),   # sum = 0.00
            (0.40, 0.40, 0.15),   # sum = 0.95
            (0.60, 0.60, 0.00),   # sum = 1.20
        ]
        for wq, ws, wt in deviating_triplets:
            with self.subTest(wq=wq, ws=ws, wt=wt):
                self.assertFalse(validate_simplex(wq, ws, wt))
                with self.assertRaises(ValueError):
                    HybridWeightVector(w_qqq=wq, w_soxx=ws, w_turnaround=wt)

    def test_cash_leak_explicitly_rejected(self) -> None:
        """Any non-zero cash allocation violates w_cash == 0.0 constraint."""
        self.assertFalse(validate_simplex(0.30, 0.30, 0.30, w_cash=0.10))
        self.assertFalse(validate_simplex(0.35, 0.35, 0.30, w_cash=0.01))

        # HybridWeightVector.from_dict must reject explicit cash key
        with self.assertRaises(ValueError):
            HybridWeightVector.from_dict({"QQQ": 0.30, "SOXX": 0.30, "Turnaround": 0.30, "CASH": 0.10})

    def test_nan_inf_none_rejected(self) -> None:
        """Non-finite or missing numeric inputs must return False from validate_simplex."""
        self.assertFalse(validate_simplex(float("nan"), 0.5, 0.5))
        self.assertFalse(validate_simplex(0.5, float("inf"), 0.5))
        self.assertFalse(validate_simplex(None, 0.5, 0.5))  # type: ignore

    def test_hybrid_weight_vector_methods_and_properties(self) -> None:
        """HybridWeightVector provides full dictionary, tuple, and normalization support."""
        vec = HybridWeightVector(0.35, 0.35, 0.30)
        self.assertEqual(vec.w_cash, 0.0)
        self.assertTrue(vec.is_valid)

        d = vec.as_dict()
        self.assertEqual(d["QQQ"], 0.35)
        self.assertEqual(d["SOXX"], 0.35)
        self.assertEqual(d["Turnaround"], 0.30)

        t = vec.as_tuple()
        self.assertEqual(t, (0.35, 0.35, 0.30))

        # Normalized test
        vec_norm = vec.normalized()
        self.assertAlmostEqual(sum(vec_norm.as_tuple()), 1.0, places=4)

        # from_dict case-insensitivity and aliases
        from_d = HybridWeightVector.from_dict({"qqq": 0.35, "soxx": 0.35, "turnaround": 0.30})
        self.assertEqual(from_d, vec)

        # from_tuple
        from_t = HybridWeightVector.from_tuple((0.35, 0.35, 0.30))
        self.assertEqual(from_t, vec)

        # Invalid tuple length raises ValueError
        with self.assertRaises(ValueError):
            HybridWeightVector.from_tuple((0.5, 0.5))  # type: ignore


# ==============================================================================
# Tier 2: 2D Simplex Grid Generator (Feature 13)
# ==============================================================================

class TestSimplexGridGenerator(unittest.TestCase):
    """Tier 2: Verifies mathematical grid generation across the 2D simplex."""

    def test_grid_count_step_010_exact_66(self) -> None:
        """Step Delta w = 0.10 (N=10) must generate exactly (11 * 12) / 2 = 66 triplets."""
        grid = generate_simplex_grid(step=0.10)
        self.assertEqual(len(grid), 66, f"Expected exactly 66 triplets, got {len(grid)}")

    def test_grid_count_step_005_exact_231(self) -> None:
        """Step Delta w = 0.05 (N=20) must generate exactly (21 * 22) / 2 = 231 triplets."""
        grid = generate_simplex_grid(step=0.05)
        self.assertEqual(len(grid), 231, f"Expected exactly 231 triplets, got {len(grid)}")

    def test_all_grid_points_satisfy_simplex_invariant(self) -> None:
        """Every generated vector across both grid resolutions must strictly satisfy simplex."""
        for step in (0.10, 0.05):
            grid = generate_simplex_grid(step=step)
            for vec in grid:
                self.assertTrue(
                    vec.is_valid,
                    f"Grid vector {vec} failed simplex validation"
                )
                self.assertEqual(vec.w_cash, 0.0)
                self.assertAlmostEqual(vec.w_qqq + vec.w_soxx + vec.w_turnaround, 1.0, places=4)
                self.assertGreaterEqual(vec.w_qqq, 0.0)
                self.assertGreaterEqual(vec.w_soxx, 0.0)
                self.assertGreaterEqual(vec.w_turnaround, 0.0)

    def test_canonical_champion_allocation_in_step_005_grid(self) -> None:
        """Canonical allocation (0.35, 0.35, 0.30) must be present in Delta w = 0.05 grid."""
        grid = generate_simplex_grid(step=0.05)
        has_canonical = any(
            abs(v.w_qqq - 0.35) < 1e-4 and abs(v.w_soxx - 0.35) < 1e-4 and abs(v.w_turnaround - 0.30) < 1e-4
            for v in grid
        )
        self.assertTrue(has_canonical, "Canonical vector (0.35, 0.35, 0.30) missing from 0.05 grid")

    def test_invalid_step_size_raises(self) -> None:
        """Non-positive or > 1.0 step sizes must raise ValueError."""
        with self.assertRaises(ValueError):
            generate_simplex_grid(step=0.0)
        with self.assertRaises(ValueError):
            generate_simplex_grid(step=-0.05)
        with self.assertRaises(ValueError):
            generate_simplex_grid(step=1.5)


# ==============================================================================
# Tier 3: 25-Year Hybrid Compounding, Friction & Tax Modeling (Features 13, 23, 24)
# ==============================================================================

class TestHybridCompoundingAndTaxModeling(unittest.TestCase):
    """Tier 3: Verifies 25-year compounding simulation, friction, and 22% tax modeling."""

    @classmethod
    def setUpClass(cls) -> None:
        # Pre-load price cache to ensure maximum execution speed across test cases
        cls.prices, cls.dates = get_hybrid_asset_prices()

    def test_25yr_hybrid_simulation_executes_successfully(self) -> None:
        """Hybrid simulation executes across full 25.25-year history (6,350+ dates)."""
        vec = HybridWeightVector(0.35, 0.35, 0.30)
        ev = simulate_hybrid(
            weights=vec,
            cycle=RebalanceFrequency.MONTHLY,
            prices=self.prices,
            dates=self.dates,
        )
        self.assertIsInstance(ev, HybridEvaluation)
        self.assertEqual(ev.cycle, RebalanceFrequency.MONTHLY)
        self.assertEqual(ev.weights, vec)
        self.assertGreater(ev.cagr_pre_tax, 5.0)
        self.assertGreater(ev.cagr_after_tax, 5.0)
        self.assertLess(ev.mdd_pre_tax, 0.0)
        self.assertLess(ev.mdd_after_tax, 0.0)
        self.assertGreater(ev.calmar_after_tax, 0.0)
        self.assertGreater(ev.sharpe_after_tax, 0.0)
        self.assertIsNotNone(ev.simulation_result)
        self.assertEqual(len(ev.simulation_result.dates), len(self.dates))  # type: ignore

    def test_friction_fees_and_slippage_applied(self) -> None:
        """Brokerage fee (0.10%) and slippage (0.08%) are deducted on turnover."""
        vec = HybridWeightVector(0.35, 0.35, 0.30)
        ev = simulate_hybrid(
            weights=vec,
            cycle=RebalanceFrequency.MONTHLY,
            prices=self.prices,
            dates=self.dates,
        )
        self.assertGreater(ev.fee_paid, 0.0)
        self.assertGreater(ev.slippage_paid, 0.0)
        self.assertGreater(ev.total_turnover, 0.0)
        # Expected fee / slippage ratio = 0.0010 / 0.0008 = 1.25
        self.assertAlmostEqual(ev.fee_paid / ev.slippage_paid, 1.25, places=2)

    def test_foreign_equity_tax_drag_behavior(self) -> None:
        """22% foreign equity tax produces quantifiable tax drag with after-tax CAGR <= pre-tax."""
        vec = HybridWeightVector(0.35, 0.35, 0.30)
        ev = simulate_hybrid(
            weights=vec,
            cycle=RebalanceFrequency.MONTHLY,
            prices=self.prices,
            dates=self.dates,
        )
        self.assertGreaterEqual(ev.cagr_pre_tax, ev.cagr_after_tax)
        self.assertGreater(ev.total_tax_paid, 0.0)
        self.assertGreater(ev.tax_drag_pct, 0.0)
        # Verify tax drag formula: cagr_pre_tax - cagr_after_tax
        self.assertAlmostEqual(ev.tax_drag_pct, ev.cagr_pre_tax - ev.cagr_after_tax, places=2)

    def test_all_5_cycles_execute_cleanly(self) -> None:
        """WEEKLY, MONTHLY, QUARTERLY, SEMI_ANNUALLY, and ANNUALLY all return valid evaluations."""
        vec = HybridWeightVector(0.35, 0.35, 0.30)
        cycle_results = compare_all_cycles(
            weights=vec,
            prices=self.prices,
            dates=self.dates,
        )
        self.assertEqual(len(cycle_results), 5)
        for freq in RebalanceFrequency:
            self.assertIn(freq.value, cycle_results)
            ev = cycle_results[freq.value]
            self.assertGreater(ev.cagr_after_tax, 0.0)
            self.assertLess(ev.mdd_after_tax, 0.0)
            self.assertGreater(ev.calmar_after_tax, 0.0)

    def test_turnover_ordering_across_cycles(self) -> None:
        """Turnover is strictly monotonically decreasing as rebalancing frequency decreases."""
        vec = HybridWeightVector(0.35, 0.35, 0.30)
        res = compare_all_cycles(weights=vec, prices=self.prices, dates=self.dates)

        turn_w = res["WEEKLY"].total_turnover
        turn_m = res["MONTHLY"].total_turnover
        turn_q = res["QUARTERLY"].total_turnover
        turn_s = res["SEMI_ANNUALLY"].total_turnover
        turn_a = res["ANNUALLY"].total_turnover

        self.assertGreater(turn_w, turn_m)
        self.assertGreater(turn_m, turn_q)
        self.assertGreater(turn_q, turn_s)
        self.assertGreater(turn_s, turn_a)

    def test_monotonic_tax_drag_ordering(self) -> None:
        """
        Proves tax drag decreases monotonically from WEEKLY down to ANNUALLY:
        WEEKLY > MONTHLY > QUARTERLY > SEMI_ANNUALLY > ANNUALLY.
        """
        vec = HybridWeightVector(0.35, 0.35, 0.30)
        res = compare_all_cycles(weights=vec, prices=self.prices, dates=self.dates)

        drag_w = res["WEEKLY"].tax_drag_pct
        drag_m = res["MONTHLY"].tax_drag_pct
        drag_q = res["QUARTERLY"].tax_drag_pct
        drag_s = res["SEMI_ANNUALLY"].tax_drag_pct
        drag_a = res["ANNUALLY"].tax_drag_pct

        self.assertGreater(drag_w, drag_m, f"Weekly tax drag ({drag_w}%) should exceed Monthly ({drag_m}%)")
        self.assertGreater(drag_m, drag_q, f"Monthly tax drag ({drag_m}%) should exceed Quarterly ({drag_q}%)")
        self.assertGreater(drag_q, drag_s, f"Quarterly tax drag ({drag_q}%) should exceed Semi-Annually ({drag_s}%)")
        self.assertGreater(drag_s, drag_a, f"Semi-Annually tax drag ({drag_s}%) should exceed Annually ({drag_a}%)")

        # Also verify total tax paid ordering
        tax_w = res["WEEKLY"].total_tax_paid
        tax_m = res["MONTHLY"].total_tax_paid
        tax_q = res["QUARTERLY"].total_tax_paid
        tax_s = res["SEMI_ANNUALLY"].total_tax_paid
        tax_a = res["ANNUALLY"].total_tax_paid

        self.assertGreater(tax_w, tax_m)
        self.assertGreater(tax_m, tax_q)
        self.assertGreater(tax_q, tax_s)
        self.assertGreater(tax_s, tax_a)


# ==============================================================================
# Tier 4: Calmar Ratio Maximization & Champion Weight Selection (Feature 13)
# ==============================================================================

class TestCalmarOptimizationAndChampion(unittest.TestCase):
    """Tier 4: Verifies 2D simplex Calmar optimization and champion weight selection."""

    @classmethod
    def setUpClass(cls) -> None:
        cls.prices, cls.dates = get_hybrid_asset_prices()

    def test_optimize_hybrid_step_010_full_grid(self) -> None:
        """optimize_hybrid evaluates all 66 vectors at step=0.10 and returns valid result."""
        result = optimize_hybrid(
            step=0.10,
            prices=self.prices,
            dates=self.dates,
        )
        self.assertIsInstance(result, HybridOptimizationResult)
        self.assertEqual(len(result.all_evaluations), 66)
        self.assertEqual(len(result.top_5_evaluations), 5)
        self.assertIsInstance(result.champion_weights, HybridWeightVector)
        self.assertIsInstance(result.champion_cycle, RebalanceFrequency)
        self.assertIsInstance(result.alpha_attribution, AlphaAttribution)
        self.assertEqual(len(result.cycle_evaluations), 5)

    def test_champion_turnaround_weight_greater_than_zero(self) -> None:
        """Champion allocation selected by Calmar ratio must have w_turnaround > 0."""
        result = optimize_hybrid(
            step=0.10,
            prices=self.prices,
            dates=self.dates,
        )
        self.assertGreater(
            result.champion_weights.w_turnaround,
            0.0,
            f"Expected w_turnaround > 0 in champion, got {result.champion_weights.w_turnaround}"
        )

    def test_champion_calmar_strictly_beats_pure_benchmark(self) -> None:
        """Champion hybrid after-tax Calmar ratio strictly beats pure benchmark allocation."""
        result = optimize_hybrid(
            step=0.10,
            prices=self.prices,
            dates=self.dates,
        )
        champ_calmar = result.champion_evaluation.calmar_after_tax
        bench_calmar = result.benchmark_evaluation.calmar_after_tax

        self.assertGreater(
            champ_calmar,
            bench_calmar,
            f"Champion Calmar ({champ_calmar:.2f}) must exceed pure benchmark Calmar ({bench_calmar:.2f})"
        )

    def test_top_5_evaluations_ordered_descending(self) -> None:
        """top_5_evaluations are sorted in strictly descending order of Calmar ratio."""
        result = optimize_hybrid(
            step=0.10,
            prices=self.prices,
            dates=self.dates,
        )
        top_5 = result.top_5_evaluations
        for i in range(len(top_5) - 1):
            self.assertGreaterEqual(
                top_5[i].calmar_after_tax,
                top_5[i + 1].calmar_after_tax,
                f"Evaluation {i} ({top_5[i].calmar_after_tax}) < {i+1} ({top_5[i+1].calmar_after_tax})"
            )

    def test_optimize_hybrid_specific_cycle(self) -> None:
        """When cycle is explicitly passed, optimization preserves requested cycle."""
        result = optimize_hybrid(
            cycle=RebalanceFrequency.MONTHLY,
            step=0.10,
            prices=self.prices,
            dates=self.dates,
        )
        self.assertEqual(result.champion_cycle, RebalanceFrequency.MONTHLY)
        self.assertEqual(result.champion_evaluation.cycle, RebalanceFrequency.MONTHLY)

    def test_data_js_format_compliance(self) -> None:
        """to_data_js_format produces valid dictionary matching data.js backtest25yr contract."""
        result = optimize_hybrid(
            step=0.10,
            prices=self.prices,
            dates=self.dates,
        )
        payload = result.to_data_js_format()
        self.assertIn("lastEvaluated", payload)
        self.assertIn("championMetrics", payload)
        self.assertIn("taxComparison", payload)
        self.assertIn("championCycle", payload)
        self.assertIn("alphaAttribution", payload)

        m = payload["championMetrics"]
        self.assertIn("cagrPreTax", m)
        self.assertIn("cagrAfterTax", m)
        self.assertIn("mddPreTax", m)
        self.assertIn("mddAfterTax", m)
        self.assertIn("calmarPreTax", m)
        self.assertIn("calmarAfterTax", m)
        self.assertIn("sharpePreTax", m)
        self.assertIn("sharpeAfterTax", m)
        self.assertIn("totalTaxPaid", m)
        self.assertIn("taxDragPct", m)
        self.assertIn("weights", m)


# ==============================================================================
# Tier 5: Turnaround Alpha Mathematical Attribution (Feature 14)
# ==============================================================================

class TestTurnaroundAlphaAttribution(unittest.TestCase):
    """Tier 5: Verifies positive convexity, benchmark diversification, and alpha proof."""

    @classmethod
    def setUpClass(cls) -> None:
        cls.prices, cls.dates = get_hybrid_asset_prices()
        cls.result = optimize_hybrid(
            step=0.10,
            prices=cls.prices,
            dates=cls.dates,
        )
        cls.attr = cls.result.alpha_attribution

    def test_theoretical_positive_convexity(self) -> None:
        """Theoretical convexity ratio (+100% TP1 vs -10% Stop Loss) is exactly 10.0x."""
        self.assertAlmostEqual(self.attr.convexity_ratio, 10.0, places=2)
        self.assertTrue(self.attr.is_convex)
        self.assertGreater(self.attr.upside_downside_ratio, 1.0)

    def test_correlation_matrix_integrity_and_diversification(self) -> None:
        """
        Pearson correlation matrix is symmetric, diagonal elements equal 1.0,
        and Turnaround exhibits low correlation to SOXX (< 0.20).
        """
        mat = self.attr.correlation_matrix
        for asset in ("QQQ", "SOXX", "Turnaround"):
            self.assertEqual(mat[asset][asset], 1.0)

        # Symmetry
        self.assertEqual(mat["QQQ"]["SOXX"], mat["SOXX"]["QQQ"])
        self.assertEqual(mat["Turnaround"]["QQQ"], mat["QQQ"]["Turnaround"])
        self.assertEqual(mat["Turnaround"]["SOXX"], mat["SOXX"]["Turnaround"])

        # Low correlation with SOXX
        self.assertTrue(self.attr.has_low_correlation)
        self.assertLess(abs(self.attr.correlation_soxx), 0.20)

    def test_turnaround_alpha_proven(self) -> None:
        """Turnaround alpha is proven via higher Calmar, higher CAGR, and positive enhancement."""
        self.assertTrue(self.attr.turnaround_alpha_proven)
        self.assertGreater(self.attr.calmar_enhancement_after_tax, 0.0)
        self.assertGreater(self.attr.cagr_enhancement_after_tax, 0.0)
        self.assertIn("Turnaround sleeve", self.attr.explanation)

    def test_alpha_attribution_as_dict(self) -> None:
        """as_dict returns serializable dictionary with expected keys."""
        d = self.attr.as_dict()
        self.assertIn("convexityRatio", d)
        self.assertIn("correlationQqq", d)
        self.assertIn("correlationSoxx", d)
        self.assertIn("calmarEnhancementAfterTax", d)
        self.assertIn("turnaroundAlphaProven", d)


# ==============================================================================
# Tier 6: High-Level Class & Architectural Offline Integrity
# ==============================================================================

class TestArchitecturalAndOfflineIntegrity(unittest.TestCase):
    """Tier 6: Verifies 100% offline isolation and StrategyHybridMaster class contracts."""

    def test_zero_cdn_offline_isolation(self) -> None:
        """engine.strategy_hybrid_master must not import network or remote modules."""
        import engine.strategy_hybrid_master as mod
        source_code = open(mod.__file__, "r", encoding="utf-8").read()  # type: ignore
        forbidden_imports = [
            "import requests",
            "import urllib",
            "from urllib",
            "import socket",
            "from socket",
            "import http.client",
            "from http.client",
            "import aiohttp",
            "import httpx",
        ]
        for forbidden in forbidden_imports:
            self.assertNotIn(
                forbidden,
                source_code,
                f"Forbidden remote networking import '{forbidden}' found in strategy_hybrid_master.py"
            )

    def test_pure_python_standard_library_compliance(self) -> None:
        """strategy_hybrid_master must not depend on numpy, pandas, or scipy."""
        import engine.strategy_hybrid_master as mod
        source_code = open(mod.__file__, "r", encoding="utf-8").read()  # type: ignore
        for banned in ("import numpy", "import pandas", "import scipy", "from numpy", "from pandas", "from scipy"):
            self.assertNotIn(
                banned,
                source_code,
                f"Forbidden third-party library import '{banned}' in strategy_hybrid_master.py"
            )

    def test_strategy_hybrid_master_classmethods(self) -> None:
        """StrategyHybridMaster class methods mirror module-level functions exactly."""
        self.assertTrue(StrategyHybridMaster.validate_simplex(0.35, 0.35, 0.30))
        self.assertFalse(StrategyHybridMaster.validate_simplex(-0.1, 0.5, 0.6))

        grid = StrategyHybridMaster.generate_simplex_grid(0.10)
        self.assertEqual(len(grid), 66)

    def test_synthetic_prices_mock_simulation(self) -> None:
        """simulate_hybrid functions properly with synthetic custom prices for unit testing."""
        dates = [f"2020-01-{i:02d}" for i in range(1, 31)]
        prices = {
            "QQQ": [100.0 + i for i in range(30)],
            "SOXX": [100.0 + 2 * i for i in range(30)],
            "Turnaround": [100.0 + 1.5 * i for i in range(30)],
        }
        vec = HybridWeightVector(0.35, 0.35, 0.30)
        cfg = BacktestConfig(start_date="2020-01-01", end_date="2020-01-30", tax_enabled=False)
        ev = simulate_hybrid(vec, RebalanceFrequency.WEEKLY, config=cfg, prices=prices, dates=dates)
        self.assertIsInstance(ev, HybridEvaluation)
        self.assertGreater(ev.cagr_pre_tax, 0.0)

    def test_normalize_cycle_aliases(self) -> None:
        """normalize_cycle handles string aliases and enums properly."""
        self.assertEqual(normalize_cycle("WEEKLY"), RebalanceFrequency.WEEKLY)
        self.assertEqual(normalize_cycle("w"), RebalanceFrequency.WEEKLY)
        self.assertEqual(normalize_cycle("monthly"), RebalanceFrequency.MONTHLY)
        self.assertEqual(normalize_cycle("Q"), RebalanceFrequency.QUARTERLY)
        self.assertEqual(normalize_cycle("SEMI"), RebalanceFrequency.SEMI_ANNUALLY)
        self.assertEqual(normalize_cycle("ANNUAL"), RebalanceFrequency.ANNUALLY)

        with self.assertRaises(ValueError):
            normalize_cycle("DAILY")


if __name__ == "__main__":
    unittest.main()
