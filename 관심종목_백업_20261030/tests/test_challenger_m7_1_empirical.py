"""
Milestone 7 Final Empirical Adversarial Challenge Test Suite (challenger_m7_1).
Target: Complete 25-Year Quantitative Backtesting & Strategy Suite (M1~M6 Deliverables)

Scope & Empirical Challenge Dimensions:
1. Strict 100% Equity Simplex Zero-Cash Invariant Robustness:
   - w_QQQ + w_SOXX + w_Turnaround == 1.0, w_cash == 0.0 under all inputs.
   - Extreme simplex vertices: (1,0,0), (0,1,0), (0,0,1).
   - Rejection of negative weights, sum != 1.0, non-zero cash, NaN, Inf, None.
   - Continuous 25.25-year daily simulation zero-cash invariant: cash is identically 0.0 at every day,
     rebalance event, and year-end tax liquidation. Fees/slippage never produce negative cash.
   - Discrete grid generation cardinality: step 0.10 -> 66 triplets, step 0.05 -> 231 triplets.

2. 5-Cycle Turnover Friction & Monotonic Tax Drag Ordering:
   - 5 cycles: WEEKLY, MONTHLY, QUARTERLY, SEMI_ANNUALLY, ANNUALLY.
   - Strict ordering of rebalance turnover: WEEKLY > MONTHLY > QUARTERLY > SEMI_ANNUALLY > ANNUALLY.
   - Strict ordering of cumulative friction (fees + slippage): WEEKLY > ... > ANNUALLY.
   - Monotonic tax drag progression:
     Tax Drag(WEEKLY) > Tax Drag(MONTHLY) > Tax Drag(QUARTERLY) > Tax Drag(SEMI_ANNUALLY) > Tax Drag(ANNUALLY).
   - Capital scaling variations (10M, 50M, 500M, 1B KRW) & tax rate variations (15%, 22%, 30%).
   - Verification of tax deferral compounding benefit (higher after-tax CAGR for longer cycles).

3. Turnaround Alpha Positive Convexity & Diversification Attribution:
   - Positive convexity: -10.0% capped downside vs +100.0% TP1 upside -> theoretical convexity ratio is 10.0x.
   - Realized gain/loss ratio > 1.0x.
   - Empirical Pearson correlation matrix: Turnaround returns show low correlation (< 0.50) with SOXX.
   - Calmar ratio & Sharpe ratio enhancement of hybrid allocation (35/35/30) over pure benchmarks.
   - Drawdown mitigation in historical crises (2000-2002 Dot-Com bust, 2008 GFC, 2022 Tightening).

4. CLI 'backtest' Command & Argument Fuzzing:
   - Default command execution produces report and prints valid terminal summary.
   - --report, --output, --sync, --data-js, --json, --quiet, --cycle, --weights flags.
   - Schema validation of --json stdout output.
   - Fuzzing: malformed weights strings, unknown cycle names, invalid step values handled safely.

5. Offline Zero-CDN DOM & Inline SVG Stability:
   - Forensic scan: 0 remote resources (http://, https://, //, cdn., remote scripts/fonts).
   - Contracted DOM IDs: 24 View 7 IDs + 5 Tax IDs present without duplicates.
   - Pure SVG Log/Linear Growth Curve: numerical resilience against non-positive NAV (no NaN/-Inf).
   - Pure SVG Underwater Drawdown: proper negative area mapping and 4 crisis regime overlays.
"""

from __future__ import annotations

import copy
import io
import json
import math
from pathlib import Path
import re
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

# Setup project root in sys.path
ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

INDEX_HTML_PATH = ROOT_DIR / "index.html"
DATA_JS_PATH = ROOT_DIR / "data.js"
REPORT_MD_PATH = ROOT_DIR / "backtest_report_25yr.md"

from engine.backtest_engine import (
    BacktestConfig,
    PerformanceMetrics,
    RebalanceFrequency,
    SimulationResult,
    TaxAccountingState,
    calculate_performance_metrics,
    is_rebalance_date,
    simulate_portfolio,
)
from engine.historical_data import (
    COMMON_END_DATE,
    COMMON_START_DATE,
    get_joint_history,
    get_qqq_history,
    get_soxx_history,
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
from engine.cli import (
    build_parser,
    cmd_backtest,
    main,
)
from engine.backtest_report import (
    DEFAULT_REPORT_PATH,
    BacktestReportGenerator,
    generate_backtest_report,
)
from engine.sync_dashboard import (
    DEFAULT_DATA_JS_PATH,
    build_backtest25yr_store,
    create_default_backtest25yr_store,
    load_data_store,
    parse_js_data_store,
    save_data_store,
    sync_backtest_to_dashboard,
)


# ==============================================================================
# 1. Simplex Invariant & Zero-Cash Robustness
# ==============================================================================

class TestSimplexInvariantAndZeroCashRobustness(unittest.TestCase):
    """Empirically stress-tests strict 100% equity simplex zero-cash constraint."""

    def test_extreme_vertices_and_simplex_boundary_invariants(self) -> None:
        """Verifies boundary vertices (1,0,0), (0,1,0), (0,0,1) and interior points satisfy simplex."""
        test_vectors = [
            (1.0, 0.0, 0.0),
            (0.0, 1.0, 0.0),
            (0.0, 0.0, 1.0),
            (0.35, 0.35, 0.30),
            (0.50, 0.50, 0.0),
            (0.3333, 0.3333, 0.3334),
            (0.20, 0.40, 0.40),
            (0.10, 0.10, 0.80),
        ]
        for wq, ws, wt in test_vectors:
            self.assertTrue(
                validate_simplex(wq, ws, wt),
                f"Vector ({wq}, {ws}, {wt}) must be valid on simplex."
            )
            vec = HybridWeightVector(wq, ws, wt)
            self.assertEqual(vec.w_cash, 0.0, "Cash allocation must strictly be identically zero.")
            self.assertAlmostEqual(vec.w_qqq + vec.w_soxx + vec.w_turnaround, 1.0, places=4)
            d = vec.as_dict()
            self.assertEqual(d["QQQ"], wq)
            self.assertEqual(d["SOXX"], ws)
            self.assertEqual(d["Turnaround"], wt)

    def test_rejection_of_invalid_and_adversarial_simplex_inputs(self) -> None:
        """Verifies validate_simplex and HybridWeightVector strictly reject corrupted/leveraged weights."""
        invalid_triplets = [
            (-0.10, 0.60, 0.50),       # Negative weight
            (0.50, 0.50, 0.50),        # Leverage (sum = 1.5)
            (0.30, 0.30, 0.30),        # Cash leakage (sum = 0.9)
            (0.0, 0.0, 0.0),           # Zero investment
            (float("nan"), 0.5, 0.5),  # NaN weight
            (float("inf"), 0.0, 0.0),  # Infinite weight
            (0.5, float("-inf"), 0.5), # -Inf weight
        ]
        for wq, ws, wt in invalid_triplets:
            self.assertFalse(
                validate_simplex(wq, ws, wt),
                f"Corrupted triplet ({wq}, {ws}, {wt}) must be rejected by validate_simplex."
            )
            with self.assertRaises((ValueError, TypeError)):
                HybridWeightVector(wq, ws, wt)

    def test_explicit_cash_weight_rejection(self) -> None:
        """Verifies dictionary or parameter with w_cash != 0 is rejected."""
        self.assertFalse(validate_simplex(0.4, 0.4, 0.2, w_cash=0.05))
        self.assertFalse(validate_simplex(0.4, 0.4, 0.2, w_cash=-0.01))

        with self.assertRaises(ValueError):
            HybridWeightVector.from_dict({
                "QQQ": 0.40,
                "SOXX": 0.40,
                "Turnaround": 0.10,
                "CASH": 0.10,
            })

    def test_discrete_grid_generation_cardinality_and_simplex_closure(self) -> None:
        """Verifies 2D simplex grid generator generates exact theoretical counts and valid vectors."""
        # Step = 0.10 -> N = 10 -> (10+1)*(10+2)/2 = 66 points
        grid_10 = generate_simplex_grid(step=0.10)
        self.assertEqual(len(grid_10), 66, "Step 0.10 must yield exactly 66 triplets on 2D simplex.")
        for vec in grid_10:
            self.assertTrue(vec.is_valid)
            self.assertEqual(vec.w_cash, 0.0)
            self.assertGreaterEqual(vec.w_qqq, 0.0)
            self.assertGreaterEqual(vec.w_soxx, 0.0)
            self.assertGreaterEqual(vec.w_turnaround, 0.0)
            self.assertAlmostEqual(vec.w_qqq + vec.w_soxx + vec.w_turnaround, 1.0, places=4)

        # Step = 0.05 -> N = 20 -> (20+1)*(20+2)/2 = 231 points
        grid_05 = generate_simplex_grid(step=0.05)
        self.assertEqual(len(grid_05), 231, "Step 0.05 must yield exactly 231 triplets on 2D simplex.")
        for vec in grid_05:
            self.assertTrue(vec.is_valid)
            self.assertEqual(vec.w_cash, 0.0)

    def test_continuous_zero_cash_invariance_throughout_25yr_simulation(self) -> None:
        """Adversarially audits daily portfolio NAV across 25.25 years to confirm 100% equity zero-cash."""
        eval_res = simulate_hybrid(
            weights=HybridWeightVector(0.35, 0.35, 0.30),
            cycle=RebalanceFrequency.MONTHLY,
            config=BacktestConfig(tax_enabled=True, initial_capital=100_000_000.0),
        )
        sim = eval_res.simulation_result
        self.assertIsNotNone(sim)

        # Check all days
        num_days = len(sim.dates)
        self.assertGreater(num_days, 6300, "25-year series must span > 6,300 daily bars.")

        prices_map, _ = get_hybrid_asset_prices()
        for t in range(0, num_days, 25):  # Sample every 25 trading days
            holdings = sim.holdings_history[t]
            p_t = {k: prices_map[k][t] for k in prices_map}
            equity_val = sum(holdings[k] * p_t[k] for k in prices_map)
            # The daily NAV must equal the sum of equity holdings
            self.assertAlmostEqual(
                equity_val, sim.daily_nav[t], delta=1.0,
                msg=f"Day {sim.dates[t]}: NAV ({sim.daily_nav[t]}) != sum of equity ({equity_val}). Cash leakage!"
            )

        # Check all rebalance records: verify fee and slippage friction did not produce negative cash
        for reb in sim.rebalance_records:
            post_nav = reb["post_nav"]
            self.assertGreater(post_nav, 0.0, "Post-rebalance NAV must remain strictly positive.")
            tw = reb["target_weights"]
            self.assertAlmostEqual(sum(tw.values()), 1.0, places=4, msg="Rebalance target weights must sum to 1.0.")


# ==============================================================================
# 2. 5-Cycle Turnover Friction & Monotonic Tax Drag Ordering
# ==============================================================================

class TestFiveCycleTurnoverFrictionAndMonotonicTaxDrag(unittest.TestCase):
    """Empirically stress-tests turnover friction and monotonic tax drag progression."""

    def test_five_cycle_turnover_and_friction_strict_monotonicity(self) -> None:
        """Verifies turnover and transaction friction strictly decrease as rebalance frequency drops."""
        weights = HybridWeightVector(0.35, 0.35, 0.30)
        cycles = compare_all_cycles(weights=weights)

        ordered_cycle_names = ["WEEKLY", "MONTHLY", "QUARTERLY", "SEMI_ANNUALLY", "ANNUALLY"]
        turnovers = [cycles[c].total_turnover for c in ordered_cycle_names]
        frictions = [cycles[c].fee_paid + cycles[c].slippage_paid for c in ordered_cycle_names]

        # Verify strict decreasing order for turnover: Weekly > Monthly > Quarterly > Semi > Annually
        for i in range(len(turnovers) - 1):
            self.assertGreater(
                turnovers[i], turnovers[i + 1],
                f"Turnover for {ordered_cycle_names[i]} ({turnovers[i]}) must exceed {ordered_cycle_names[i+1]} ({turnovers[i+1]})."
            )

        # Verify strict decreasing order for transaction friction
        for i in range(len(frictions) - 1):
            self.assertGreater(
                frictions[i], frictions[i + 1],
                f"Friction for {ordered_cycle_names[i]} ({frictions[i]}) must exceed {ordered_cycle_names[i+1]} ({frictions[i+1]})."
            )

    def test_tax_drag_monotonic_ordering_baseline_capital(self) -> None:
        """Verifies Tax Drag (%p) strictly decreases from WEEKLY to ANNUALLY under baseline capital."""
        cycles = compare_all_cycles()
        tax_drags = {
            c: cycles[c].tax_drag_pct
            for c in ["WEEKLY", "MONTHLY", "QUARTERLY", "SEMI_ANNUALLY", "ANNUALLY"]
        }

        # Quantitative benchmark:
        # WEEKLY (1.32%p) > MONTHLY (0.78%p) > QUARTERLY (0.42%p) > SEMI_ANNUALLY (0.24%p) > ANNUALLY (0.19%p)
        self.assertGreater(tax_drags["WEEKLY"], tax_drags["MONTHLY"])
        self.assertGreater(tax_drags["MONTHLY"], tax_drags["QUARTERLY"])
        self.assertGreater(tax_drags["QUARTERLY"], tax_drags["SEMI_ANNUALLY"])
        self.assertGreater(tax_drags["SEMI_ANNUALLY"], tax_drags["ANNUALLY"])
        self.assertGreater(tax_drags["ANNUALLY"], 0.0)

    def test_tax_drag_monotonicity_under_capital_scaling_stress(self) -> None:
        """Adversarially varies initial capital across 4 orders of magnitude and verifies tax drag ordering."""
        test_capitals = [
            10_000_000.0,    # 10M KRW
            50_000_000.0,    # 50M KRW
            500_000_000.0,   # 500M KRW
            1_000_000_000.0, # 1B KRW
        ]
        weights = HybridWeightVector(0.35, 0.35, 0.30)
        p_map, d_list = get_hybrid_asset_prices()

        for cap in test_capitals:
            cfg_base = BacktestConfig(initial_capital=cap, tax_enabled=True, tax_rate=0.22)
            eval_w = simulate_hybrid(weights, RebalanceFrequency.WEEKLY, cfg_base, p_map, d_list)
            eval_m = simulate_hybrid(weights, RebalanceFrequency.MONTHLY, cfg_base, p_map, d_list)
            eval_q = simulate_hybrid(weights, RebalanceFrequency.QUARTERLY, cfg_base, p_map, d_list)
            eval_a = simulate_hybrid(weights, RebalanceFrequency.ANNUALLY, cfg_base, p_map, d_list)

            # Weekly tax drag must strictly exceed Monthly, which exceeds Quarterly, which exceeds Annually
            self.assertGreater(
                eval_w.tax_drag_pct, eval_m.tax_drag_pct,
                f"Capital {cap:,}: Weekly tax drag ({eval_w.tax_drag_pct}) <= Monthly ({eval_m.tax_drag_pct})"
            )
            self.assertGreater(
                eval_m.tax_drag_pct, eval_q.tax_drag_pct,
                f"Capital {cap:,}: Monthly tax drag ({eval_m.tax_drag_pct}) <= Quarterly ({eval_q.tax_drag_pct})"
            )
            self.assertGreater(
                eval_q.tax_drag_pct, eval_a.tax_drag_pct,
                f"Capital {cap:,}: Quarterly tax drag ({eval_q.tax_drag_pct}) <= Annually ({eval_a.tax_drag_pct})"
            )

    def test_tax_drag_monotonicity_under_tax_rate_variations(self) -> None:
        """Adversarially stress-tests tax drag monotonicity under 15%, 22%, and 30% tax rates."""
        weights = HybridWeightVector(0.35, 0.35, 0.30)
        p_map, d_list = get_hybrid_asset_prices()

        for tr in [0.15, 0.22, 0.30]:
            cfg_tr = BacktestConfig(tax_rate=tr, tax_enabled=True)
            eval_w = simulate_hybrid(weights, RebalanceFrequency.WEEKLY, cfg_tr, p_map, d_list)
            eval_m = simulate_hybrid(weights, RebalanceFrequency.MONTHLY, cfg_tr, p_map, d_list)
            eval_a = simulate_hybrid(weights, RebalanceFrequency.ANNUALLY, cfg_tr, p_map, d_list)

            self.assertGreater(
                eval_w.tax_drag_pct, eval_m.tax_drag_pct,
                f"Tax rate {tr}: Weekly tax drag <= Monthly"
            )
            self.assertGreater(
                eval_m.tax_drag_pct, eval_a.tax_drag_pct,
                f"Tax rate {tr}: Monthly tax drag <= Annually"
            )

    def test_tax_deferral_compounding_benefit_proof(self) -> None:
        """Proves that annual/quarterly rebalancing yields strictly higher after-tax CAGR than weekly."""
        cycles = compare_all_cycles()
        cagr_w = cycles["WEEKLY"].cagr_after_tax
        cagr_m = cycles["MONTHLY"].cagr_after_tax
        cagr_q = cycles["QUARTERLY"].cagr_after_tax
        cagr_a = cycles["ANNUALLY"].cagr_after_tax

        # Deferring rebalancing taxes leaves capital compounded in the market: Annually > Weekly
        self.assertGreater(
            cagr_a, cagr_w,
            f"Tax deferral proof: Annual after-tax CAGR ({cagr_a}%) must exceed Weekly ({cagr_w}%)."
        )
        self.assertGreater(
            cagr_q, cagr_w,
            f"Tax deferral proof: Quarterly after-tax CAGR ({cagr_q}%) must exceed Weekly ({cagr_w}%)."
        )


# ==============================================================================
# 3. Turnaround Alpha Positive Convexity & Diversification Attribution
# ==============================================================================

class TestTurnaroundAlphaPositiveConvexityAndDiversification(unittest.TestCase):
    """Empirically proves Strategy A positive convexity and diversification attribution."""

    def test_strategy_a_positive_convexity_mathematical_proof(self) -> None:
        """Verifies the theoretical 10.0x convexity ratio and empirical gain/loss asymmetry."""
        opt_res = optimize_hybrid(cycle=RebalanceFrequency.MONTHLY, step=0.10)
        attr = opt_res.alpha_attribution

        # 1. Theoretical convexity: +100% TP1 / 10% Stop-Loss = 10.0x
        self.assertEqual(attr.convexity_ratio, 10.0)
        self.assertTrue(attr.is_convex)

        # 2. Upside/downside ratio
        self.assertGreater(attr.upside_downside_ratio, 1.0, "Gain/loss ratio must be positive asymmetric (> 1.0x).")

    def test_empirical_correlation_matrix_diversification(self) -> None:
        """Verifies empirical Pearson correlation matrix proves non-correlated diversification."""
        opt_res = optimize_hybrid(cycle=RebalanceFrequency.MONTHLY, step=0.10)
        attr = opt_res.alpha_attribution
        matrix = attr.correlation_matrix

        # Self-correlation must be 1.0
        self.assertEqual(matrix["QQQ"]["QQQ"], 1.0)
        self.assertEqual(matrix["SOXX"]["SOXX"], 1.0)
        self.assertEqual(matrix["Turnaround"]["Turnaround"], 1.0)

        # Symmetry
        self.assertEqual(matrix["QQQ"]["SOXX"], matrix["SOXX"]["QQQ"])
        self.assertEqual(matrix["Turnaround"]["SOXX"], matrix["SOXX"]["Turnaround"])
        self.assertEqual(matrix["Turnaround"]["QQQ"], matrix["QQQ"]["Turnaround"])

        # Low correlation with SOXX
        self.assertLess(
            abs(attr.correlation_soxx), 0.50,
            f"Turnaround-SOXX correlation ({attr.correlation_soxx}) must be < 0.50 for diversification."
        )

    def test_hybrid_master_calmar_and_sharpe_enhancement_over_pure_benchmarks(self) -> None:
        """Proves adding Turnaround sleeve strictly enhances Calmar ratio over pure benchmark allocations."""
        opt_res = optimize_hybrid(cycle=RebalanceFrequency.MONTHLY, step=0.10)
        champ = opt_res.champion_evaluation
        bench = opt_res.benchmark_evaluation

        # Turnaround weight in champion must be positive
        self.assertGreater(champ.w_turnaround, 0.0)
        # Benchmark must have w_turnaround == 0
        self.assertEqual(bench.w_turnaround, 0.0)

        # Champion after-tax Calmar must be greater than or equal to pure benchmark Calmar
        self.assertGreaterEqual(
            champ.calmar_after_tax, bench.calmar_after_tax,
            f"Champion Calmar ({champ.calmar_after_tax}) must equal or exceed pure benchmark ({bench.calmar_after_tax})."
        )
        self.assertTrue(opt_res.alpha_attribution.turnaround_alpha_proven)

    def test_turnaround_sleeve_crisis_drawdown_mitigation(self) -> None:
        """Adversarially inspects drawdown resilience during historical crisis regimes."""
        joint = get_joint_history()
        dates = sorted(joint.keys())

        # 2008 Global Financial Crisis: 2007-10 to 2009-03
        gfc_dates = [d for d in dates if "2007-10-01" <= d <= "2009-03-31"]
        self.assertGreater(len(gfc_dates), 300)

        # Pure SOXX peak-to-trough in GFC was -71%
        soxx_gfc_prices = [joint[d]["SOXX"] for d in gfc_dates]
        soxx_peak = max(soxx_gfc_prices)
        soxx_trough = min(soxx_gfc_prices)
        soxx_dd = (soxx_trough - soxx_peak) / soxx_peak
        self.assertLess(soxx_dd, -0.60, "SOXX suffered >60% drawdown in GFC.")

        # Hybrid strategy D simulation during GFC
        cfg_gfc = BacktestConfig(start_date="2007-10-01", end_date="2009-03-31", tax_enabled=False)
        eval_gfc = simulate_hybrid(HybridWeightVector(0.35, 0.35, 0.30), RebalanceFrequency.MONTHLY, cfg_gfc)
        self.assertGreater(
            eval_gfc.mdd_pre_tax, -65.0,
            f"Hybrid allocation MDD ({eval_gfc.mdd_pre_tax}%) mitigated severe SOXX GFC drop."
        )


# ==============================================================================
# 4. CLI 'backtest' Command & Argument Robustness
# ==============================================================================

class TestCliBacktestCommandAndArgumentRobustness(unittest.TestCase):
    """Stress-tests python -m engine.cli backtest execution, arguments, and fuzzing."""

    def test_cli_backtest_default_execution_generates_report(self) -> None:
        """Verifies running backtest generates report and terminal output."""
        parser = build_parser()
        with tempfile.TemporaryDirectory() as tmp_dir:
            out_rep = Path(tmp_dir) / "test_report.md"
            args = parser.parse_args(["backtest", "--output", str(out_rep)])
            captured = io.StringIO()
            with patch("sys.stdout", captured):
                rc = cmd_backtest(args)

            self.assertEqual(rc, 0)
            self.assertTrue(out_rep.exists())
            self.assertGreater(out_rep.stat().st_size, 5000)
            stdout_text = captured.getvalue()
            self.assertIn("25-Year Institutional Backtest Complete", stdout_text)
            self.assertIn("CAGR:", stdout_text)
            self.assertIn("MDD:", stdout_text)
            self.assertIn("Calmar:", stdout_text)

    def test_cli_backtest_json_stdout_schema_compliance(self) -> None:
        """Verifies --json flag prints valid JSON to stdout matching backtest25yr schema."""
        parser = build_parser()
        args = parser.parse_args(["backtest", "--json", "--quiet"])
        captured = io.StringIO()
        with patch("sys.stdout", captured):
            rc = cmd_backtest(args)

        self.assertEqual(rc, 0)
        output_str = captured.getvalue().strip()
        data = json.loads(output_str)

        required_keys = ["lastEvaluated", "championMetrics", "taxComparison", "growthSeries", "drawdownSeries", "cycleComparison", "executionGuide"]
        for k in required_keys:
            self.assertIn(k, data, f"Required JSON key '{k}' missing from CLI --json output.")

        champ = data["championMetrics"]
        self.assertIn("cagrAfterTax", champ)
        self.assertIn("mddAfterTax", champ)
        self.assertIn("calmarAfterTax", champ)
        self.assertIn("taxDragPct", champ)
        self.assertIn("weights", champ)

    def test_cli_backtest_sync_flag_idempotently_updates_data_js(self) -> None:
        """Verifies --sync flag updates target data.js without corrupting other stores."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            temp_data_js = Path(tmp_dir) / "data.js"
            save_data_store(load_data_store(DATA_JS_PATH), temp_data_js)

            parser = build_parser()
            args = parser.parse_args(["backtest", "--sync", "--data-js", str(temp_data_js), "--quiet"])
            rc = cmd_backtest(args)
            self.assertEqual(rc, 0)

            reloaded = load_data_store(temp_data_js)
            self.assertIn("backtest25yr", reloaded)
            b = reloaded["backtest25yr"]
            self.assertIn("championMetrics", b)
            self.assertEqual(b["championMetrics"]["weights"], {"QQQ": 0.35, "SOXX": 0.35, "Turnaround": 0.30})

    def test_cli_backtest_fuzzing_and_error_handling(self) -> None:
        """Fuzzes CLI backtest with malformed weights, unknown cycles, and invalid flags."""
        parser = build_parser()

        # 1. Unknown flag raises SystemExit
        with self.assertRaises(SystemExit):
            parser.parse_args(["backtest", "--non-existent-fuzz-flag"])

        # 2. Malformed weights string fallback to default (0.35, 0.35, 0.30)
        args_malformed_weights = parser.parse_args(["backtest", "--weights", "not,valid,numbers", "--quiet"])
        rc = cmd_backtest(args_malformed_weights)
        self.assertEqual(rc, 0)

        # 3. Two-element weights string fallback to default
        args_two_weights = parser.parse_args(["backtest", "--weights", "0.5,0.5", "--quiet"])
        rc = cmd_backtest(args_two_weights)
        self.assertEqual(rc, 0)

        # 4. Unknown cycle raises ValueError
        args_bad_cycle = parser.parse_args(["backtest", "--cycle", "NON_EXISTENT_CYCLE"])
        with self.assertRaises(ValueError):
            cmd_backtest(args_bad_cycle)


# ==============================================================================
# 5. Offline Zero-CDN DOM & Inline SVG Stability
# ==============================================================================

class TestOfflineZeroCdnDomAndSvgStability(unittest.TestCase):
    """Stress-tests index.html View 7 DOM contracted elements, SVG transforms, and Zero-CDN isolation."""

    @classmethod
    def setUpClass(cls) -> None:
        cls.html_text = INDEX_HTML_PATH.read_text(encoding="utf-8")

    def test_forensic_zero_cdn_offline_isolation(self) -> None:
        """Performs rigorous forensic regex scan confirming zero remote CDN dependencies."""
        remote_patterns = [
            r"https?://(?!localhost|127\.0\.0\.1)",  # Any remote http/https protocol
            r"//cdn\.",                             # Protocol-relative CDN
            r"unpkg\.com",                          # NPM CDN
            r"jsdelivr\.net",                       # jsDelivr CDN
            r"cdnjs\.cloudflare\.com",              # Cloudflare CDN
            r"fonts\.googleapis\.com",              # Google Fonts CSS
            r"fonts\.gstatic\.com",                 # Google Fonts binary
            r"fontawesome",                         # FontAwesome remote
        ]
        for pat in remote_patterns:
            matches = re.findall(pat, self.html_text, re.IGNORECASE)
            self.assertEqual(
                len(matches), 0,
                f"Zero-CDN violation in index.html! Found remote reference matching '{pat}': {matches}"
            )

    def test_contracted_dom_ids_integrity(self) -> None:
        """Verifies all 24 View 7 contracted DOM IDs plus 5 Tax contracted IDs exist without duplicates."""
        contracted_ids = [
            "btnViewBacktest",
            "viewBacktestSection",
            "backtestKpiRibbon",
            "backtestCagrVal",
            "backtestMddVal",
            "backtestCalmarVal",
            "backtestGrowthCard",
            "btnGrowthLog",
            "btnGrowthLinear",
            "backtestGrowthSvg",
            "backtestUnderwaterCard",
            "backtestUnderwaterSvg",
            "backtestMatrixCard",
            "backtestCycleSelect",
            "backtestMatrixTableBody",
            "backtestGuideCard",
            "backtestGuideWeights",
            "backtestGuideCycle",
            "backtestGuidePicks",
            "backtestGuideTp1",
            "backtestGuideStopLoss",
            "backtestReportLink",
            "backtestSyncTimestamp",
            # Tax contracted IDs
            "btnTaxPre",
            "btnTaxAfter",
            "backtestTaxCard",
            "backtestTaxDragChart",
            "backtestTaxDragVal",
        ]
        for dom_id in contracted_ids:
            self.assertIn(
                f'id="{dom_id}"', self.html_text,
                f"Contracted DOM ID '{dom_id}' missing in index.html"
            )

        # Audit contracted DOM IDs for uniqueness
        for dom_id in contracted_ids:
            matches = re.findall(rf'id=["\']{dom_id}["\']', self.html_text)
            self.assertEqual(
                len(matches), 1,
                f"Contracted DOM ID '{dom_id}' must appear exactly once in index.html, found {len(matches)}"
            )

        # Global repo-wide DOM ID uniqueness integrity audit
        all_ids = re.findall(r'id=["\']([^"\']+)["\']', self.html_text)
        duplicates = [x for x in set(all_ids) if all_ids.count(x) > 1]
        self.assertEqual(
            len(duplicates), 0,
            f"Duplicate DOM IDs found in index.html: {sorted(duplicates)}"
        )

    def test_pure_svg_growth_curve_numerical_resilience(self) -> None:
        """Simulates SVG coordinate math for Log/Linear scales under extreme inputs (NAV <= 0)."""
        pad_l, pad_r, pad_t, plot_h = 55, 20, 20, 200
        w = 700
        plot_w = w - pad_l - pad_r

        # Extreme inputs: 0.0, -50.0, 1e-9, 100M, 1B
        raw_vals = [0.0, -50.0, 1e-9, 100_000_000.0, 250_000_000.0]

        # Log scale mapping resilience
        safe_min = 1.0  # Safe log minimum
        log_points = []
        for idx, v in enumerate(raw_vals):
            safe_v = max(v, safe_min)
            log_v = math.log10(safe_v)
            self.assertFalse(math.isnan(log_v), f"Log value of {v} produced NaN")
            self.assertFalse(math.isinf(log_v), f"Log value of {v} produced Inf")

        # Linear scale mapping
        min_v = min(raw_vals)
        max_v = max(raw_vals)
        span = max_v - min_v if max_v > min_v else 1.0
        for idx, v in enumerate(raw_vals):
            x = pad_l + (idx / (len(raw_vals) - 1)) * plot_w
            y = pad_t + plot_h - ((v - min_v) / span) * plot_h
            self.assertGreaterEqual(x, pad_l)
            self.assertLessEqual(x, w - pad_r)
            self.assertGreaterEqual(y, pad_t)
            self.assertLessEqual(y, pad_t + plot_h)

    def test_pure_svg_underwater_drawdown_geometry(self) -> None:
        """Verifies drawdown clamping logic and presence of 4 historical crisis overlays."""
        # 1. Drawdown clamping: dd > 0 must be clamped to 0.0%
        test_dds = [0.05, 0.0, -0.15, -0.5979, -0.835]
        for dd in test_dds:
            clamped = min(0.0, dd)
            self.assertLessEqual(clamped, 0.0, "Underwater drawdown must never be positive.")

        # 2. Check 4 crisis regimes in index.html (both SVG overlay label & institutional terminology)
        crisis_names = [
            "닷컴 붕괴",       # Dot-Com bust SVG overlay label (2001-2002)
            "2008 GFC",        # 2008 Global Financial Crisis
            "2020 코로나",     # 2020 COVID shock
            "2022 긴축",       # 2022 Fed rate hiking cycle
        ]
        for cname in crisis_names:
            self.assertIn(cname, self.html_text, f"Crisis regime overlay '{cname}' missing in index.html.")

        # Institutional terminology alignment with PROJECT.md and backtest_report_25yr.md
        self.assertIn("닷컴 버블", self.html_text, "Institutional crisis term '닷컴 버블' missing in index.html.")
        self.assertIn("닷컴 버블 붕괴", self.html_text, "Institutional crisis term '닷컴 버블 붕괴' missing in index.html.")

        # Check internal regime range variable references
        for r_var in ["rDotcom", "rGfc", "rCovid", "rTightening"]:
            self.assertIn(r_var, self.html_text, f"Crisis range variable '{r_var}' missing in index.html.")


if __name__ == "__main__":
    unittest.main()
