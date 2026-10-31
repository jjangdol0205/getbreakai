"""
Empirical Challenger Test Suite for Milestone 4 (challenger_m4_1):
Adversarial Stress-Testing and Empirical Invariant Verification of Strategy D:
100% Equity Simplex Hybrid Master Optimizer & After-Tax Alpha Suite
(`engine/strategy_hybrid_master.py`).

Key Empirical Verification Tracks:
1. Simplex Constraint Invariant & Zero-Cash Defense:
   - Negative weights, cash leaks (<1.0), unbacked leverage (>1.0), NaN/inf, float precision boundaries (tol=1e-4).
   - Strict 100% equity zero-cash invariant during 25.25-year compounding and after tax liquidations.
2. Combinatorial Grid Generation Stress:
   - Combinatorial formula ((N+1)(N+2))/2 for Delta w = 0.20, 0.10, 0.05, 0.02.
   - Uniqueness (zero duplicates), simplex validity on 100% of points, boundary handling.
3. 5-Cycle Turnover Friction & Monotonic Tax Drag Stress:
   - Monotonic turnover ordering across 5 rebalancing cycles.
   - Monotonic tax drag ordering under micro (10K), standard (100M), and massive (10B) capital.
   - Monotonic tax drag ordering under varying tax rates (0%, 15%, 22%, 30%) and deductions (0, 2.5M, 10M).
4. Turnaround Alpha & Convexity Stress Under Historical Crash Regimes:
   - 4 major adversarial crash regimes: Dot-Com crash (2001-2002), 2008 GFC, 2020 COVID, 2022 Fed tightening.
   - Positive convexity (10.0x theoretical, empirical gain/loss asymmetry > 1.0).
   - Benchmark diversification (near-zero correlation to SOXX) and Calmar/Sharpe alpha proof.
5. API Contract & Architectural Zero-CDN Compliance.
"""

from __future__ import annotations

import math
import unittest
from typing import Any, Dict, List, Tuple

from engine.backtest_engine import (
    BacktestConfig,
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


class TestSimplexZeroCashEmpiricalDefense(unittest.TestCase):
    """Track 1: Simplex constraint invariant and zero-cash defense stress-testing."""

    def test_negative_weights_adversarial_rejection(self) -> None:
        """Adversarially inject negative weights to verify rejection of short-selling."""
        adversarial_negatives = [
            (-0.50, 0.75, 0.75),
            (0.50, -0.10, 0.60),
            (0.50, 0.60, -0.10),
            (-0.01, 1.01, 0.00),
            (0.35, -0.001, 0.651),
            (-0.0002, 0.5001, 0.5001),
        ]
        for wq, ws, wt in adversarial_negatives:
            with self.subTest(wq=wq, ws=ws, wt=wt):
                self.assertFalse(
                    validate_simplex(wq, ws, wt),
                    f"Negative weight ({wq}, {ws}, {wt}) must be rejected by validate_simplex"
                )
                with self.assertRaises(ValueError):
                    HybridWeightVector(w_qqq=wq, w_soxx=ws, w_turnaround=wt)

    def test_cash_leak_and_leverage_adversarial_rejection(self) -> None:
        """Adversarially inject under-allocation (cash leak) and over-allocation (leverage)."""
        adversarial_sums = [
            (0.30, 0.30, 0.30),   # sum = 0.90 (cash leak)
            (0.40, 0.40, 0.15),   # sum = 0.95 (cash leak)
            (0.33, 0.33, 0.33),   # sum = 0.99 (cash leak)
            (0.35, 0.35, 0.2998), # sum = 0.9998 (exceeds tol=1e-4)
            (0.35, 0.35, 0.3002), # sum = 1.0002 (exceeds tol=1e-4)
            (0.40, 0.40, 0.25),   # sum = 1.05 (leverage)
            (0.50, 0.50, 0.10),   # sum = 1.10 (leverage)
            (0.60, 0.60, 0.00),   # sum = 1.20 (leverage)
            (1.00, 1.00, 1.00),   # sum = 3.00 (extreme leverage)
            (0.00, 0.00, 0.00),   # sum = 0.00
        ]
        for wq, ws, wt in adversarial_sums:
            with self.subTest(wq=wq, ws=ws, wt=wt):
                self.assertFalse(validate_simplex(wq, ws, wt))
                with self.assertRaises(ValueError):
                    HybridWeightVector(w_qqq=wq, w_soxx=ws, w_turnaround=wt)

    def test_float_precision_boundary_tolerance(self) -> None:
        """Verify strict float tolerance boundary behavior at exactly tol = 1e-4."""
        # Boundaries within tol (diff <= 1e-4) must be accepted
        valid_boundaries = [
            (0.35005, 0.35, 0.30),  # sum = 1.00005 (diff = +5e-5 <= 1e-4)
            (0.34995, 0.35, 0.30),  # sum = 0.99995 (diff = -5e-5 <= 1e-4)
            (0.33333, 0.33333, 0.33334),  # sum = 1.00000
        ]
        for wq, ws, wt in valid_boundaries:
            with self.subTest(wq=wq, ws=ws, wt=wt):
                self.assertTrue(validate_simplex(wq, ws, wt))
                vec = HybridWeightVector(w_qqq=wq, w_soxx=ws, w_turnaround=wt)
                self.assertTrue(vec.is_valid)

        # Boundaries beyond tol (diff > 1e-4) must be rejected
        invalid_boundaries = [
            (0.35015, 0.35, 0.30),  # sum = 1.00015 (diff = +1.5e-4 > 1e-4)
            (0.34985, 0.35, 0.30),  # sum = 0.99985 (diff = -1.5e-4 > 1e-4)
        ]
        for wq, ws, wt in invalid_boundaries:
            with self.subTest(wq=wq, ws=ws, wt=wt):
                self.assertFalse(validate_simplex(wq, ws, wt))
                with self.assertRaises(ValueError):
                    HybridWeightVector(w_qqq=wq, w_soxx=ws, w_turnaround=wt)

    def test_non_finite_inputs_rejection(self) -> None:
        """Adversarially pass NaN, +inf, -inf, None to validate_simplex and HybridWeightVector."""
        for bad_val in (float("nan"), float("inf"), float("-inf")):
            self.assertFalse(validate_simplex(bad_val, 0.5, 0.5))
            self.assertFalse(validate_simplex(0.5, bad_val, 0.5))
            self.assertFalse(validate_simplex(0.5, 0.5, bad_val))
            with self.assertRaises(ValueError):
                HybridWeightVector(w_qqq=bad_val, w_soxx=0.5, w_turnaround=0.5)

        self.assertFalse(validate_simplex(None, 0.5, 0.5))  # type: ignore

    def test_zero_cash_defense_in_from_dict_and_vector(self) -> None:
        """Verify that any explicit non-zero cash in dictionary triggers immediate ValueError."""
        # Zero cash dictionary succeeds
        vec = HybridWeightVector.from_dict({"QQQ": 0.35, "SOXX": 0.35, "Turnaround": 0.30})
        self.assertEqual(vec.w_cash, 0.0)

        # Dictionary with explicit cash raises
        bad_dicts = [
            {"QQQ": 0.30, "SOXX": 0.30, "Turnaround": 0.30, "CASH": 0.10},
            {"QQQ": 0.35, "SOXX": 0.35, "Turnaround": 0.30, "USD": 0.05},
            {"QQQ": 0.35, "SOXX": 0.35, "Turnaround": 0.30, "KRW": 0.01},
            {"QQQ": 0.35, "SOXX": 0.35, "Turnaround": 0.30, "cash": 0.001},
        ]
        for bd in bad_dicts:
            with self.subTest(bd=bd):
                with self.assertRaises(ValueError):
                    HybridWeightVector.from_dict(bd)

    def test_continuous_simulation_zero_cash_invariant(self) -> None:
        """Verify that across all 6,353 trading days, portfolio remains 100% equity with 0 cash held."""
        prices, dates = get_hybrid_asset_prices()
        vec = HybridWeightVector(0.35, 0.35, 0.30)
        ev = simulate_hybrid(vec, RebalanceFrequency.MONTHLY, prices=prices, dates=dates)
        sim = ev.simulation_result
        self.assertIsNotNone(sim)

        # Inspect daily valuations and holdings
        for t in range(len(dates)):
            p_map = {k: prices[k][t] for k in prices}
            holdings = sim.holdings_history[t]  # type: ignore
            # Total equity valuation computed from share holdings
            equity_val = sum(holdings[k] * p_map[k] for k in prices)
            nav = sim.daily_nav[t]  # type: ignore
            # Invariant: NAV exactly matches equity valuation (zero cash buffer)
            self.assertAlmostEqual(nav, equity_val, places=2)


class TestCombinatorialSimplexGridStress(unittest.TestCase):
    """Track 2: Combinatorial grid generator stress-testing and formula validation."""

    def test_combinatorial_formula_exact_counts(self) -> None:
        """
        Verify exact combinatorial formula: Count = (N + 1) * (N + 2) / 2
        for Delta w = 0.20 (N=5), 0.10 (N=10), 0.05 (N=20), 0.02 (N=50).
        """
        test_steps = [
            (0.20, 5, 21),
            (0.10, 10, 66),
            (0.05, 20, 231),
            (0.02, 50, 1326),
        ]
        for step, n_val, expected_count in test_steps:
            with self.subTest(step=step, n=n_val, expected=expected_count):
                grid = generate_simplex_grid(step=step)
                theoretical = (n_val + 1) * (n_val + 2) // 2
                self.assertEqual(theoretical, expected_count)
                self.assertEqual(len(grid), expected_count)

    def test_grid_uniqueness_no_duplicate_triplets(self) -> None:
        """Verify that every generated vector in the grid is distinct (zero duplicate triplets)."""
        for step in (0.20, 0.10, 0.05, 0.02):
            grid = generate_simplex_grid(step=step)
            unique_tuples = set(v.as_tuple() for v in grid)
            self.assertEqual(
                len(unique_tuples),
                len(grid),
                f"Duplicate triplets found in grid for step {step}"
            )

    def test_all_grid_points_satisfy_simplex_invariants(self) -> None:
        """Every generated vector across all resolutions must strictly satisfy simplex invariants."""
        for step in (0.20, 0.10, 0.05):
            grid = generate_simplex_grid(step=step)
            for v in grid:
                self.assertTrue(v.is_valid)
                self.assertEqual(v.w_cash, 0.0)
                self.assertGreaterEqual(v.w_qqq, 0.0)
                self.assertGreaterEqual(v.w_soxx, 0.0)
                self.assertGreaterEqual(v.w_turnaround, 0.0)
                self.assertAlmostEqual(v.w_qqq + v.w_soxx + v.w_turnaround, 1.0, places=4)

    def test_extreme_step_size_1_0_yields_corner_vertices(self) -> None:
        """Step = 1.0 yields exactly the 3 simplex corners: (1,0,0), (0,1,0), (0,0,1)."""
        grid = generate_simplex_grid(step=1.0)
        self.assertEqual(len(grid), 3)
        corners = set(v.as_tuple() for v in grid)
        expected_corners = {(1.0, 0.0, 0.0), (0.0, 1.0, 0.0), (0.0, 0.0, 1.0)}
        self.assertEqual(corners, expected_corners)

    def test_invalid_step_sizes_raise_value_error(self) -> None:
        """Non-positive or > 1.0 step sizes raise ValueError."""
        for bad_step in (0.0, -0.05, -1.0, 1.05, 2.0):
            with self.subTest(bad_step=bad_step):
                with self.assertRaises(ValueError):
                    generate_simplex_grid(step=bad_step)


class TestTurnoverFrictionAndMonotonicTaxDragStress(unittest.TestCase):
    """Track 3: 5-Cycle turnover friction and monotonic tax drag stress-testing."""

    @classmethod
    def setUpClass(cls) -> None:
        cls.prices, cls.dates = get_hybrid_asset_prices()
        cls.weights = HybridWeightVector(0.35, 0.35, 0.30)

    def test_monotonic_turnover_ordering(self) -> None:
        """Empirically prove turnover is strictly monotonically decreasing as frequency decreases."""
        res = compare_all_cycles(self.weights, prices=self.prices, dates=self.dates)
        cycles = ["WEEKLY", "MONTHLY", "QUARTERLY", "SEMI_ANNUALLY", "ANNUALLY"]
        turnovers = [res[c].total_turnover for c in cycles]

        for i in range(len(turnovers) - 1):
            self.assertGreater(
                turnovers[i],
                turnovers[i + 1],
                f"Turnover {cycles[i]} ({turnovers[i]}) must exceed {cycles[i+1]} ({turnovers[i+1]})"
            )

    def test_monotonic_tax_drag_under_capital_variations(self) -> None:
        """
        Stress-test monotonic tax drag across 3 vast capital regimes:
        - Micro-Capital: 10,000 KRW
        - Standard Capital: 100,000,000 KRW
        - Massive Capital: 10,000,000,000 KRW
        """
        capitals = [
            ("Micro 10K", 10_000.0),
            ("Standard 100M", 100_000_000.0),
            ("Massive 10B", 10_000_000_000.0),
        ]
        cycles = ["WEEKLY", "MONTHLY", "QUARTERLY", "SEMI_ANNUALLY", "ANNUALLY"]

        for label, cap in capitals:
            with self.subTest(capital=label):
                cfg = BacktestConfig(
                    initial_capital=cap,
                    tax_enabled=True,
                    tax_rate=0.22,
                    annual_tax_deduction=2_500_000.0,
                )
                res = compare_all_cycles(
                    self.weights,
                    config=cfg,
                    prices=self.prices,
                    dates=self.dates,
                )
                drags = [res[c].tax_drag_pct for c in cycles]
                taxes = [res[c].total_tax_paid for c in cycles]

                # Tax drag must strictly decrease
                for i in range(len(drags) - 1):
                    self.assertGreater(
                        drags[i],
                        drags[i + 1],
                        f"[{label}] Drag {cycles[i]} ({drags[i]}%) must exceed {cycles[i+1]} ({drags[i+1]}%)"
                    )

                # Total tax paid must strictly decrease
                for i in range(len(taxes) - 1):
                    self.assertGreater(
                        taxes[i],
                        taxes[i + 1],
                        f"[{label}] Tax {cycles[i]} ({taxes[i]}) must exceed {cycles[i+1]} ({taxes[i+1]})"
                    )

    def test_monotonic_tax_drag_under_tax_rate_variations(self) -> None:
        """Stress-test monotonic tax drag under varying tax rates: 0%, 15%, 22%, 30%."""
        cycles = [
            RebalanceFrequency.WEEKLY,
            RebalanceFrequency.MONTHLY,
            RebalanceFrequency.QUARTERLY,
            RebalanceFrequency.SEMI_ANNUALLY,
            RebalanceFrequency.ANNUALLY,
        ]

        # 1. Positive tax rates
        for tax_rate in (0.15, 0.22, 0.30):
            with self.subTest(tax_rate=tax_rate):
                drags: List[float] = []
                for cyc in cycles:
                    cfg = BacktestConfig(tax_enabled=True, tax_rate=tax_rate)
                    ev = simulate_hybrid(self.weights, cycle=cyc, config=cfg, prices=self.prices, dates=self.dates)
                    drags.append(ev.tax_drag_pct)

                for i in range(len(drags) - 1):
                    self.assertGreater(
                        drags[i],
                        drags[i + 1],
                        f"[TaxRate={tax_rate}] Drag {cycles[i]} ({drags[i]}%) must exceed {cycles[i+1]} ({drags[i+1]}%)"
                    )

        # 2. Tax disabled (rate=0.0): drag identically 0.0
        for cyc in cycles:
            cfg = BacktestConfig(tax_enabled=False, tax_rate=0.0)
            ev = simulate_hybrid(self.weights, cycle=cyc, config=cfg, prices=self.prices, dates=self.dates)
            self.assertEqual(ev.tax_drag_pct, 0.0)
            self.assertEqual(ev.total_tax_paid, 0.0)

    def test_monotonic_tax_drag_under_deduction_variations(self) -> None:
        """Stress-test monotonic tax drag under varying deductions: 0, 2.5M, 10M KRW."""
        cycles = [
            RebalanceFrequency.WEEKLY,
            RebalanceFrequency.MONTHLY,
            RebalanceFrequency.QUARTERLY,
            RebalanceFrequency.SEMI_ANNUALLY,
            RebalanceFrequency.ANNUALLY,
        ]

        for ded in (0.0, 2_500_000.0, 10_000_000.0):
            with self.subTest(deduction=ded):
                drags: List[float] = []
                for cyc in cycles:
                    cfg = BacktestConfig(tax_enabled=True, tax_rate=0.22, annual_tax_deduction=ded)
                    ev = simulate_hybrid(self.weights, cycle=cyc, config=cfg, prices=self.prices, dates=self.dates)
                    drags.append(ev.tax_drag_pct)

                for i in range(len(drags) - 1):
                    self.assertGreater(
                        drags[i],
                        drags[i + 1],
                        f"[Ded={ded}] Drag {cycles[i]} ({drags[i]}%) must exceed {cycles[i+1]} ({drags[i+1]}%)"
                    )

    def test_friction_fees_and_slippage_exact_proportionality(self) -> None:
        """Verify fee (0.10%) and slippage (0.08%) maintain exact 1.25 ratio across cycles."""
        res = compare_all_cycles(self.weights, prices=self.prices, dates=self.dates)
        for cyc_key, ev in res.items():
            self.assertGreater(ev.fee_paid, 0.0)
            self.assertGreater(ev.slippage_paid, 0.0)
            # fee_rate / slippage_rate = 0.0010 / 0.0008 = 1.25
            self.assertAlmostEqual(ev.fee_paid / ev.slippage_paid, 1.25, places=2)


class TestTurnaroundConvexityAndCrashRegimesStress(unittest.TestCase):
    """Track 4: Turnaround positive convexity and historical crash regimes stress-testing."""

    @classmethod
    def setUpClass(cls) -> None:
        cls.prices, cls.dates = get_hybrid_asset_prices()
        cls.w_hybrid = HybridWeightVector(0.35, 0.35, 0.30)
        cls.w_bench = HybridWeightVector(0.50, 0.50, 0.00)
        cls.w_soxx = HybridWeightVector(0.00, 1.00, 0.00)

    def test_historical_crash_regimes_mdd_protection(self) -> None:
        """
        Adversarially evaluate all 4 canonical crash regimes:
        1. 닷컴 버블 붕괴 (Dot-Com Crash): 2001-07-10 ~ 2002-10-09
        2. 2008 금융위기 (2008 GFC): 2007-10-01 ~ 2009-03-09
        3. 2020 코로나 충격 (COVID Crash): 2020-02-19 ~ 2020-03-23
        4. 2022 긴축 급락 (Fed Tightening): 2021-12-28 ~ 2022-10-14
        Empirically verify that Turnaround sleeve cushions drawdown compared to pure benchmark.
        """
        crash_regimes = [
            ("Dot-Com Crash", "2001-07-10", "2002-10-09"),
            ("2008 GFC", "2007-10-01", "2009-03-09"),
            ("2020 COVID Crash", "2020-02-19", "2020-03-23"),
            ("2022 Fed Tightening", "2021-12-28", "2022-10-14"),
        ]

        for name, s_date, e_date in crash_regimes:
            with self.subTest(regime=name):
                idx_s = next(i for i, d in enumerate(self.dates) if d >= s_date)
                idx_e = next(i for i, d in enumerate(self.dates) if d >= e_date) + 1
                sub_dates = self.dates[idx_s:idx_e]
                sub_prices = {k: v[idx_s:idx_e] for k, v in self.prices.items()}
                cfg = BacktestConfig(start_date=s_date, end_date=e_date, tax_enabled=False)

                ev_hyb = simulate_hybrid(self.w_hybrid, RebalanceFrequency.MONTHLY, config=cfg, prices=sub_prices, dates=sub_dates)
                ev_ben = simulate_hybrid(self.w_bench, RebalanceFrequency.MONTHLY, config=cfg, prices=sub_prices, dates=sub_dates)
                ev_sox = simulate_hybrid(self.w_soxx, RebalanceFrequency.MONTHLY, config=cfg, prices=sub_prices, dates=sub_dates)

                # Hybrid MDD must be superior (less negative / smaller drop) than pure SOXX
                self.assertGreater(
                    ev_hyb.mdd_pre_tax,
                    ev_sox.mdd_pre_tax,
                    f"[{name}] Hybrid MDD ({ev_hyb.mdd_pre_tax}%) must be better than SOXX ({ev_sox.mdd_pre_tax}%)"
                )
                # Hybrid MDD must be equal or superior to 50/50 benchmark
                self.assertGreaterEqual(
                    ev_hyb.mdd_pre_tax + 0.5,  # within minor 0.5% boundary
                    ev_ben.mdd_pre_tax,
                    f"[{name}] Hybrid MDD ({ev_hyb.mdd_pre_tax}%) vs Benchmark ({ev_ben.mdd_pre_tax}%)"
                )

    def test_theoretical_and_empirical_convexity(self) -> None:
        """Verify 10.0x theoretical convexity and empirical gain/loss asymmetry > 1.0."""
        opt = optimize_hybrid(step=0.10, prices=self.prices, dates=self.dates)
        attr = opt.alpha_attribution

        self.assertAlmostEqual(attr.convexity_ratio, 10.0, places=2)
        self.assertTrue(attr.is_convex)
        self.assertGreater(attr.upside_downside_ratio, 1.0)

    def test_low_correlation_diversification_matrix(self) -> None:
        """Verify Pearson correlation matrix symmetry, unit diagonal, and low SOXX correlation."""
        opt = optimize_hybrid(step=0.10, prices=self.prices, dates=self.dates)
        attr = opt.alpha_attribution

        mat = attr.correlation_matrix
        for k in ("QQQ", "SOXX", "Turnaround"):
            self.assertEqual(mat[k][k], 1.0)

        self.assertEqual(mat["QQQ"]["SOXX"], mat["SOXX"]["QQQ"])
        self.assertEqual(mat["Turnaround"]["QQQ"], mat["QQQ"]["Turnaround"])
        self.assertEqual(mat["Turnaround"]["SOXX"], mat["SOXX"]["Turnaround"])

        # Low correlation with SOXX
        self.assertTrue(attr.has_low_correlation)
        self.assertLess(abs(attr.correlation_soxx), 0.20)

    def test_turnaround_alpha_proof_comprehensive(self) -> None:
        """Verify Turnaround Alpha proof over pure benchmark mix (w_Turnaround = 0)."""
        opt = optimize_hybrid(step=0.10, prices=self.prices, dates=self.dates)
        champ = opt.champion_evaluation
        bench = opt.benchmark_evaluation

        self.assertTrue(opt.alpha_attribution.turnaround_alpha_proven)
        self.assertGreater(champ.w_turnaround, 0.0)
        self.assertGreater(champ.calmar_after_tax, bench.calmar_after_tax)
        self.assertGreater(champ.cagr_after_tax, bench.cagr_after_tax)


class TestMasterClassAndArchitectureIntegrity(unittest.TestCase):
    """Track 5: High-level class methods, data.js serialization, and offline Zero-CDN integrity."""

    def test_strategy_hybrid_master_api_conformance(self) -> None:
        """StrategyHybridMaster classmethods and instance methods execute flawlessly."""
        self.assertTrue(StrategyHybridMaster.validate_simplex(0.35, 0.35, 0.30))
        grid = StrategyHybridMaster.generate_simplex_grid(0.20)
        self.assertEqual(len(grid), 21)

        prices, dates = get_hybrid_asset_prices()
        master = StrategyHybridMaster(prices=prices, dates=dates)
        self.assertEqual(master.prices, prices)
        self.assertEqual(master.dates, dates)

    def test_data_js_format_structure_and_keys(self) -> None:
        """to_data_js_format generates exact contract required by data.js backtest25yr store."""
        opt = optimize_hybrid(step=0.10)
        payload = opt.to_data_js_format()

        self.assertIn("lastEvaluated", payload)
        self.assertEqual(payload["lastEvaluated"], COMMON_END_DATE)
        self.assertIn("championMetrics", payload)
        self.assertIn("taxComparison", payload)
        self.assertIn("championCycle", payload)
        self.assertIn("alphaAttribution", payload)

        m = payload["championMetrics"]
        for key in ("cagrPreTax", "cagrAfterTax", "mddPreTax", "mddAfterTax", "calmarPreTax", "calmarAfterTax", "sharpePreTax", "sharpeAfterTax", "totalTaxPaid", "taxDragPct", "weights"):
            self.assertIn(key, m)

        tax_comp = payload["taxComparison"]
        self.assertEqual(tax_comp["taxRatePct"], 22.0)
        self.assertEqual(tax_comp["annualDeductionUsd"], 2000)
        self.assertIn("cycleTaxDrag", tax_comp)
        self.assertEqual(len(tax_comp["cycleTaxDrag"]), 5)

    def test_zero_cdn_offline_isolation(self) -> None:
        """Assert zero networking imports in engine/strategy_hybrid_master.py."""
        import engine.strategy_hybrid_master as mod
        with open(mod.__file__, "r", encoding="utf-8") as f:
            code = f.read()

        banned_tokens = [
            "import requests", "import urllib", "from urllib", "import socket",
            "from socket", "import http.client", "import aiohttp", "import httpx",
            "import numpy", "import pandas", "import scipy",
        ]
        for token in banned_tokens:
            self.assertNotIn(
                token,
                code,
                f"Forbidden network/external dependency '{token}' found in strategy_hybrid_master.py"
            )


if __name__ == "__main__":
    unittest.main()
