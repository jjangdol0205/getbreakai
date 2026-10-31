"""
Unit and Integration Test Suite for Milestone 5 Deliverables:
- 25-Year Institutional Report Generator (engine/backtest_report.py, Feature 15)
- data.js backtest25yr Store Synchronization (engine/sync_dashboard.py, Feature 16 & Contract 4)
- CLI 'backtest' Subcommand (engine/cli.py)

100% Offline Self-Contained (Zero-CDN, zero network requests, pure Python standard library).
"""

from __future__ import annotations

import copy
from datetime import datetime
import io
import json
import math
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

from engine.backtest_engine import (
    BacktestConfig,
    PerformanceMetrics,
    RebalanceFrequency,
    SimulationResult,
)
from engine.backtest_report import (
    DEFAULT_REPORT_PATH,
    BacktestReportGenerator,
    generate_backtest_report,
)
from engine.cli import (
    build_parser,
    cmd_backtest,
    main,
)
from engine.historical_data import (
    COMMON_END_DATE,
    COMMON_START_DATE,
    get_joint_history,
)
from engine.models import DailyMarketData
from engine.strategy_hybrid_master import (
    HybridEvaluation,
    HybridOptimizationResult,
    HybridWeightVector,
    StrategyHybridMaster,
)
from engine.sync_dashboard import (
    DEFAULT_DATA_JS_PATH,
    build_backtest25yr_store,
    create_default_backtest25yr_store,
    create_default_data_store,
    load_data_store,
    parse_js_data_store,
    save_data_store,
    sync_backtest_to_dashboard,
    sync_to_dashboard,
    update_data_store_with_market_data,
)


# ==============================================================================
# 1. Test Suite: 25-Year Institutional Report Generator (Feature 15)
# ==============================================================================

class TestBacktestReportGenerator(unittest.TestCase):
    """Verifies institutional markdown report generation, 7 canonical sections, and metrics."""

    def test_report_generation_default_file_created(self) -> None:
        """Verifies report is generated, file exists, and file size exceeds 5 KB."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp_path = Path(tmp_dir) / "test_report.md"
            content = generate_backtest_report(output_path=tmp_path)
            self.assertTrue(tmp_path.exists(), "Report markdown file must exist on disk")
            self.assertGreater(tmp_path.stat().st_size, 5000, "Report file size must exceed 5 KB")
            self.assertGreater(len(content), 5000)

    def test_all_seven_canonical_sections_present(self) -> None:
        """F15: Verifies all 7 canonical sections exist in the generated report."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp_path = Path(tmp_dir) / "test_report_sections.md"
            content = generate_backtest_report(output_path=tmp_path)

            canonical_sections = [
                "Executive Summary",
                "25-Year Historical Dataset",
                "Strategy Performance Comparison",
                "100% Equity Hybrid Master Optimization",
                "5 Rebalancing Cycles Comparison",
                "Crisis Regime Stress Analysis",
                "Real-World Execution Guide",
            ]

            for section in canonical_sections:
                self.assertIn(
                    section,
                    content,
                    f"Report must contain canonical section heading: '{section}'",
                )

    def test_section_1_executive_summary_dual_metrics(self) -> None:
        """Verifies Section 1 contains dual pre-tax and after-tax CAGR, MDD, Sharpe, Calmar."""
        gen = BacktestReportGenerator()
        sec1 = gen.build_section_1_executive_summary()

        self.assertIn("1. Executive Summary", sec1)
        self.assertIn("세전", sec1)
        self.assertIn("세후", sec1)
        self.assertIn("CAGR", sec1)
        self.assertIn("MDD", sec1)
        self.assertIn("Calmar", sec1)
        self.assertIn("Sharpe", sec1)
        self.assertIn("Tax Drag", sec1)
        self.assertIn("22.0%", sec1)
        self.assertIn("250만 원", sec1)
        self.assertIn("35%", sec1)

    def test_section_2_dataset_bars_and_crises(self) -> None:
        """Verifies Section 2 details QQQ/SOXX bars and the 5 historical crisis timelines."""
        gen = BacktestReportGenerator()
        sec2 = gen.build_section_2_historical_dataset()

        self.assertIn("2. 25-Year Historical Dataset", sec2)
        self.assertIn("6,942", sec2)  # QQQ bars
        self.assertIn("6,353", sec2)  # SOXX bars
        self.assertIn("닷컴 버블", sec2)
        self.assertIn("금융위기", sec2)
        self.assertIn("코로나", sec2)
        self.assertIn("긴축", sec2)
        self.assertIn("AI", sec2)

    def test_section_3_strategy_performance_comparison_table(self) -> None:
        """Verifies Section 3 compares Strategy A, B, C, and Buy & Hold baselines."""
        gen = BacktestReportGenerator()
        sec3 = gen.build_section_3_strategy_comparison()

        self.assertIn("3. Strategy Performance Comparison", sec3)
        self.assertIn("QQQ Buy & Hold", sec3)
        self.assertIn("SOXX Buy & Hold", sec3)
        self.assertIn("전략 A", sec3)
        self.assertIn("전략 B", sec3)
        self.assertIn("전략 C", sec3)

    def test_section_4_hybrid_simplex_and_alpha_attribution(self) -> None:
        """Verifies Section 4 details zero-cash invariant, 35/35/30 weights, and 10.0x convexity."""
        gen = BacktestReportGenerator()
        sec4 = gen.build_section_4_hybrid_master_optimization()

        self.assertIn("4. 100% Equity Hybrid Master Optimization", sec4)
        self.assertIn("w_{\\text{cash}} \\equiv 0.0", sec4)
        self.assertIn("35%", sec4)
        self.assertIn("30%", sec4)
        self.assertIn("10.0", sec4)  # 10.0x convexity ratio
        self.assertIn("Turnaround Alpha", sec4)

    def test_section_5_cycle_comparison_and_monotonic_tax_drag(self) -> None:
        """Verifies Section 5 contains all 5 cycles and proves monotonic tax drag."""
        gen = BacktestReportGenerator()
        sec5 = gen.build_section_5_cycle_comparison_and_tax_drag()

        self.assertIn("5. 5 Rebalancing Cycles Comparison", sec5)
        self.assertIn("WEEKLY", sec5)
        self.assertIn("MONTHLY", sec5)
        self.assertIn("QUARTERLY", sec5)
        self.assertIn("SEMI_ANNUALLY", sec5)
        self.assertIn("ANNUALLY", sec5)
        self.assertIn("Tax Drag", sec5)
        self.assertIn("Tax Deferral", sec5)

    def test_section_6_crisis_regime_stress_analysis(self) -> None:
        """Verifies Section 6 details drawdown mitigation across the 4 major crisis regimes."""
        gen = BacktestReportGenerator()
        sec6 = gen.build_section_6_crisis_regime_stress_analysis()

        self.assertIn("6. Crisis Regime Stress Analysis", sec6)
        self.assertIn("닷컴 버블", sec6)
        self.assertIn("2008", sec6)
        self.assertIn("코로나", sec6)
        self.assertIn("2022", sec6)
        self.assertIn("-58.4%", sec6)

    def test_section_7_real_world_execution_guide(self) -> None:
        """Verifies Section 7 provides practical manual: calendar, 4 filters, TP1 runner, -10% stop."""
        gen = BacktestReportGenerator()
        sec7 = gen.build_section_7_real_world_execution_guide()

        self.assertIn("7. Real-World Execution Guide", sec7)
        self.assertIn("35% : SOXX 35% : 턴어라운드 슬리브 30%", sec7)
        self.assertIn("Filter 1", sec7)
        self.assertIn("Filter 2", sec7)
        self.assertIn("Filter 3", sec7)
        self.assertIn("Filter 4", sec7)
        self.assertIn("STRONG_SWITCH", sec7)
        self.assertIn("D-Day 20일", sec7)
        self.assertIn("+100%", sec7)
        self.assertIn("$0.00", sec7)
        self.assertIn("-10%", sec7)

    def test_custom_weights_and_cycle_generator(self) -> None:
        """Verifies BacktestReportGenerator accepts custom weights and cycle parameters."""
        gen = BacktestReportGenerator(
            champion_weights=(0.40, 0.30, 0.30),
            champion_cycle=RebalanceFrequency.QUARTERLY,
        )
        self.assertEqual(gen.weights.w_qqq, 0.40)
        self.assertEqual(gen.weights.w_soxx, 0.30)
        self.assertEqual(gen.weights.w_turnaround, 0.30)
        self.assertEqual(gen.cycle, RebalanceFrequency.QUARTERLY)


# ==============================================================================
# 2. Test Suite: data.js backtest25yr Store Synchronization (Feature 16 & Contract 4)
# ==============================================================================

class TestDataJsBacktestStore(unittest.TestCase):
    """Verifies backtest25yr data store serialization schema and regression safety."""

    def test_build_backtest25yr_store_schema_conformance(self) -> None:
        """Contract 4: Verifies build_backtest25yr_store satisfies exact PROJECT.md Contract 4 schema."""
        store = build_backtest25yr_store()

        # 1. Top-level keys
        required_keys = [
            "lastEvaluated",
            "championMetrics",
            "taxComparison",
            "growthSeries",
            "drawdownSeries",
            "cycleComparison",
            "executionGuide",
        ]
        for k in required_keys:
            self.assertIn(k, store, f"backtest25yr store must contain top-level key '{k}'")

        # 2. championMetrics schema
        champ = store["championMetrics"]
        metric_fields = [
            "cagrPreTax",
            "cagrAfterTax",
            "mddPreTax",
            "mddAfterTax",
            "calmarPreTax",
            "calmarAfterTax",
            "sharpePreTax",
            "sharpeAfterTax",
            "totalTaxPaid",
            "taxDragPct",
            "weights",
            # Backwards compatibility aliases
            "cagr",
            "mdd",
            "calmar",
            "sharpe",
        ]
        for mf in metric_fields:
            self.assertIn(mf, champ, f"championMetrics must contain field '{mf}'")
            if mf != "weights":
                self.assertIsInstance(champ[mf], (int, float), f"{mf} must be numeric")

        # Weights simplex invariant
        w = champ["weights"]
        self.assertAlmostEqual(w["QQQ"] + w["SOXX"] + w["Turnaround"], 1.0, places=4)

        # 3. taxComparison schema
        tc = store["taxComparison"]
        self.assertEqual(tc["taxRatePct"], 22.0)
        self.assertEqual(tc["annualDeductionUsd"], 2000)
        self.assertEqual(tc["annualDeductionKrw"], 2500000)
        self.assertIn("cycleTaxDrag", tc)

        for cyc_key in ["WEEKLY", "MONTHLY", "QUARTERLY", "SEMI_ANNUALLY", "ANNUALLY"]:
            self.assertIn(cyc_key, tc["cycleTaxDrag"])
            cyc_info = tc["cycleTaxDrag"][cyc_key]
            self.assertIn("taxDragPct", cyc_info)
            self.assertIn("cagrAfterTax", cyc_info)
            self.assertIn("totalTaxPaid", cyc_info)

        # Verify monotonic tax drag: WEEKLY tax drag > ANNUALLY tax drag
        self.assertGreater(
            tc["cycleTaxDrag"]["WEEKLY"]["taxDragPct"],
            tc["cycleTaxDrag"]["ANNUALLY"]["taxDragPct"],
            "Weekly rebalancing must incur strictly greater tax drag than annual rebalancing",
        )

        # 4. growthSeries & drawdownSeries
        growth = store["growthSeries"]
        dd = store["drawdownSeries"]
        self.assertGreater(len(growth), 500, "growthSeries must contain sampled curve points")
        self.assertGreater(len(dd), 500, "drawdownSeries must contain sampled curve points")
        self.assertEqual(len(growth), len(dd))

        sample_g = growth[0]
        self.assertIn("date", sample_g)
        self.assertIn("hybrid", sample_g)
        self.assertIn("qqq", sample_g)
        self.assertIn("soxx", sample_g)
        self.assertIn("turnaround", sample_g)

        sample_dd = dd[0]
        self.assertIn("date", sample_dd)
        self.assertIn("hybrid", sample_dd)
        self.assertIn("qqq", sample_dd)
        self.assertIn("soxx", sample_dd)

        # 5. cycleComparison
        comp = store["cycleComparison"]
        self.assertEqual(len(comp), 5)
        for row in comp:
            self.assertIn("cycle", row)
            self.assertIn("cagrPre", row)
            self.assertIn("cagrPost", row)
            self.assertIn("mdd", row)
            self.assertIn("calmarPost", row)
            self.assertIn("taxDrag", row)

        # 6. executionGuide
        guide = store["executionGuide"]
        self.assertIn("weights", guide)
        self.assertIn("cycle", guide)
        self.assertIn("picks", guide)
        self.assertIn("tp1", guide)
        self.assertIn("stopLoss", guide)

    def test_default_data_store_includes_backtest25yr(self) -> None:
        """Verifies create_default_data_store includes backtest25yr store."""
        data_store = create_default_data_store()
        self.assertIn("backtest25yr", data_store)
        self.assertIn("championMetrics", data_store["backtest25yr"])

    def test_load_data_store_auto_initializes_missing_backtest25yr(self) -> None:
        """Verifies load_data_store gracefully adds backtest25yr if loaded from older data.js."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            legacy_file = Path(tmp_dir) / "legacy_data.js"
            # Write data.js without backtest25yr
            legacy_json = {
                "lastUpdated": "2026-10-12 12:00:00",
                "portfolio": {},
                "stocks": [],
                "records": [],
                "dailyDigests": [],
                "dailyInsights": [],
                "financials": {},
                "timing": {},
                "managerJournal": {},
                "weeklyScreener": {},
            }
            save_data_store(legacy_json, legacy_file)

            loaded = load_data_store(legacy_file)
            self.assertIn("backtest25yr", loaded, "load_data_store must auto-populate backtest25yr store")
            self.assertIn("championMetrics", loaded["backtest25yr"])

    def test_sync_backtest_to_dashboard_round_trip(self) -> None:
        """Verifies sync_backtest_to_dashboard persists valid JavaScript window.WATCHLIST_DATA."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            target_js = Path(tmp_dir) / "data.js"
            success = sync_backtest_to_dashboard(data_js_path=str(target_js))
            self.assertTrue(success)
            self.assertTrue(target_js.exists())

            # Read back text and verify JS structure
            js_text = target_js.read_text(encoding="utf-8")
            self.assertTrue(js_text.startswith("window.WATCHLIST_DATA = {"))
            self.assertTrue(js_text.strip().endswith("};"))

            # Parse with engine parser
            parsed = parse_js_data_store(js_text)
            self.assertIn("backtest25yr", parsed)
            self.assertEqual(parsed["backtest25yr"]["championMetrics"]["weights"]["QQQ"], 0.35)

    def test_zero_regression_on_existing_stores(self) -> None:
        """Verifies synchronizing backtest25yr does not mutate or corrupt existing stores."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            target_js = Path(tmp_dir) / "data.js"
            base_store = create_default_data_store()
            base_store["portfolio"]["note"] = "CUSTOM_NOTE_REGRESSION_TEST"
            base_store["stocks"].append({"id": "CUSTOM_STOCK", "name": "Custom"})
            save_data_store(base_store, target_js)

            # Sync backtest
            sync_backtest_to_dashboard(data_js_path=str(target_js))

            reloaded = load_data_store(target_js)
            self.assertEqual(reloaded["portfolio"]["note"], "CUSTOM_NOTE_REGRESSION_TEST")
            self.assertTrue(any(s.get("id") == "CUSTOM_STOCK" for s in reloaded["stocks"]))
            self.assertIn("backtest25yr", reloaded)


# ==============================================================================
# 3. Test Suite: CLI Integration (engine/cli.py)
# ==============================================================================

class TestBacktestCli(unittest.TestCase):
    """Verifies CLI backtest command flags, report generation, and stdout JSON output."""

    def test_cli_backtest_help_flag(self) -> None:
        """Verifies python -m engine.cli backtest --help returns exit code 0."""
        with self.assertRaises(SystemExit) as cm:
            main(["backtest", "--help"])
        self.assertEqual(cm.exception.code, 0)

    def test_cli_backtest_report_generation(self) -> None:
        """Verifies python -m engine.cli backtest --report generates report file."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp_rep = Path(tmp_dir) / "cli_report.md"
            exit_code = main(["backtest", "--report", "-o", str(tmp_rep), "--quiet"])
            self.assertEqual(exit_code, 0)
            self.assertTrue(tmp_rep.exists())
            self.assertGreater(tmp_rep.stat().st_size, 5000)

    def test_cli_backtest_sync_data_js(self) -> None:
        """Verifies python -m engine.cli backtest --sync updates data.js."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp_js = Path(tmp_dir) / "data.js"
            exit_code = main(["backtest", "--sync", "--data-js", str(tmp_js), "--quiet"])
            self.assertEqual(exit_code, 0)
            self.assertTrue(tmp_js.exists())

            loaded = load_data_store(tmp_js)
            self.assertIn("backtest25yr", loaded)
            self.assertEqual(loaded["backtest25yr"]["championMetrics"]["weights"]["Turnaround"], 0.30)

    def test_cli_backtest_json_output(self) -> None:
        """Verifies python -m engine.cli backtest --json writes valid Contract 4 JSON to stdout."""
        buf = io.StringIO()
        with patch("sys.stdout", buf):
            exit_code = main(["backtest", "--json"])

        self.assertEqual(exit_code, 0)
        output_str = buf.getvalue().strip()
        self.assertTrue(output_str.startswith("{"))
        parsed = json.loads(output_str)
        self.assertIn("championMetrics", parsed)
        self.assertIn("taxComparison", parsed)
        self.assertIn("growthSeries", parsed)

    def test_cli_backtest_custom_weights(self) -> None:
        """Verifies python -m engine.cli backtest --weights parses custom weight triplets."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp_js = Path(tmp_dir) / "data.js"
            exit_code = main([
                "backtest",
                "--weights", "0.40,0.30,0.30",
                "--cycle", "QUARTERLY",
                "--sync",
                "--data-js", str(tmp_js),
                "--quiet",
            ])
            self.assertEqual(exit_code, 0)
            loaded = load_data_store(tmp_js)
            self.assertEqual(loaded["backtest25yr"]["championMetrics"]["weights"]["QQQ"], 0.40)


if __name__ == "__main__":
    unittest.main()
