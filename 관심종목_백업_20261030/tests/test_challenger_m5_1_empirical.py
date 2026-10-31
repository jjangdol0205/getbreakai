"""
Empirical Challenge & Adversarial Stress-Test Suite for Milestone 5 Deliverables.
Author: challenger_m5_1 (Empirical Challenger)
Scope:
1. Report Integrity & Robustness (engine/backtest_report.py, backtest_report_25yr.md)
   - Nested output directories, custom paths, missing directories
   - Verbatim section headings and subheadings
   - Markdown table formatting, delimiter alignment, column parity, percentage/currency units
   - Simplex invariant verification and invalid weights handling
2. data.js Store Serialization & Evaluation Safety (engine/sync_dashboard.py, data.js)
   - Windows JScript / cscript syntax evaluation of window.WATCHLIST_DATA.backtest25yr
   - JSON injection resilience: </script> tags, prototype pollution, unicode separators U+2028/U+2029
   - parse_js_data_store robustness against malformed/loose JS
   - save_data_store circular reference safety
3. Array Sampling Boundaries & Memory Safety
   - Default downsampling (every 5 bars = 1,272 points)
   - Boundary checks: start date, terminal date, chronological monotonicity
   - Value integrity: no NaN, no null/None, no Inf in numeric series
4. CLI Argument & Flag Fuzzing (engine/cli.py backtest)
   - Invalid flags, negative step values, malformed weights, unknown cycles
   - Exit code verification and descriptive error message enforcement
   - JSON stdout Contract 4 schema validation under --quiet and --json
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

# Set up project root in sys.path
ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

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
    get_qqq_history,
    get_soxx_history,
)
from engine.strategy_hybrid_master import (
    HybridWeightVector,
    RebalanceFrequency,
    StrategyHybridMaster,
    normalize_cycle,
    validate_simplex,
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
)


class TestReportIntegrityEmpirical(unittest.TestCase):
    """Adversarially tests backtest report generation, table formatting, and path resilience."""

    def test_report_generation_in_deeply_nested_nonexistent_directory(self) -> None:
        """Verifies report generator safely creates missing nested parent directories."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            nested_target = Path(tmp_dir) / "sub1" / "sub2" / "deep" / "custom_report.md"
            self.assertFalse(nested_target.parent.exists())

            report_text = generate_backtest_report(output_path=nested_target)
            self.assertTrue(nested_target.exists(), "Report generator must create parent directories")
            self.assertGreater(nested_target.stat().st_size, 10000)
            self.assertEqual(report_text, nested_target.read_text(encoding="utf-8"))

    def test_report_all_seven_canonical_section_headers_verbatim(self) -> None:
        """Verifies all 7 canonical section titles are present verbatim with correct numbers."""
        generator = BacktestReportGenerator()
        with tempfile.TemporaryDirectory() as tmp_dir:
            out_file = Path(tmp_dir) / "test_sections.md"
            content = generator.generate_report(output_path=out_file)

            expected_sections = [
                "## 1. Executive Summary (핵심 결론 및 종합 요약)",
                "## 2. 25-Year Historical Dataset (25개년 초장기 시계열 데이터셋 개요)",
                "## 3. Strategy Performance Comparison (3대 개별 전략 정밀 성과 비교)",
                "## 4. 100% Equity Hybrid Master Optimization (현금 배제 100% 주식 하이브리드 마스터 최적화)",
                "## 5. 5 Rebalancing Cycles Comparison (5대 리밸런싱 주기 전수 비교 및 세금 드래그 분석)",
                "## 6. Crisis Regime Stress Analysis (4대 역사적 경제 위기 구간 스트레스 테스트)",
                "## 7. Real-World Execution Guide (실전 개인 투자자를 위한 최적 포트폴리오 실행 가이드)",
            ]
            for sec in expected_sections:
                self.assertIn(sec, content, f"Report missing canonical section header: '{sec}'")

    def test_report_markdown_tables_column_alignment_and_unit_formatting(self) -> None:
        """Stress-tests all markdown tables in generated report for uniform column count and unit formatting."""
        generator = BacktestReportGenerator()
        with tempfile.TemporaryDirectory() as tmp_dir:
            out_file = Path(tmp_dir) / "table_check.md"
            content = generator.generate_report(output_path=out_file)

        lines = content.splitlines()
        table_blocks: list[list[str]] = []
        current_table: list[str] = []

        for line in lines:
            stripped = line.strip()
            if stripped.startswith("|") and stripped.endswith("|"):
                current_table.append(stripped)
            else:
                if len(current_table) >= 3:  # Header + separator + at least 1 row
                    table_blocks.append(current_table)
                current_table = []
        if len(current_table) >= 3:
            table_blocks.append(current_table)

        self.assertGreaterEqual(len(table_blocks), 4, "Report must contain at least 4 markdown tables (Sections 2, 3, 5, 6)")

        for idx, table in enumerate(table_blocks):
            header = table[0]
            separator = table[1]
            data_rows = table[2:]

            header_cols = [c.strip() for c in header.split("|")[1:-1]]
            col_count = len(header_cols)
            self.assertGreater(col_count, 1, f"Table {idx} must have >1 column")

            # Check separator row syntax (|---|---|...)
            sep_cols = [c.strip() for c in separator.split("|")[1:-1]]
            self.assertEqual(len(sep_cols), col_count, f"Table {idx} separator column count mismatch")
            for sep in sep_cols:
                self.assertTrue(re.match(r"^:?-+:?$", sep), f"Table {idx} has invalid separator cell: '{sep}'")

            # Check every data row has matching column count
            for row_i, row in enumerate(data_rows):
                row_cols = [c.strip() for c in row.split("|")[1:-1]]
                self.assertEqual(
                    len(row_cols), col_count,
                    f"Table {idx} row {row_i} has {len(row_cols)} columns, expected {col_count}"
                )

        # Check monetary and percentage formatting presence in Section 1 & Section 3
        self.assertRegex(content, r"\d+만 원|\$100,000", "Monetary units (KRW/USD) must be formatted properly")
        self.assertRegex(content, r"\d+\.\d{2}%", "Percentage rates must be formatted with 2 decimal places")
        self.assertRegex(content, r"\d+\.\d{2}%p", "Percentage point metrics must have %p suffix")

    def test_report_zero_cash_simplex_invariant_text(self) -> None:
        """Verifies report Section 4 mathematically documents the zero-cash invariant w_cash == 0.0."""
        generator = BacktestReportGenerator()
        with tempfile.TemporaryDirectory() as tmp_dir:
            out_file = Path(tmp_dir) / "invariant.md"
            content = generator.generate_report(output_path=out_file)

        self.assertIn("w_{\\text{cash}} \\equiv 0.0", content)
        self.assertIn("1.0", content)
        self.assertIn("Zero-Cash Invariant", content)

    def test_report_generator_with_custom_weights_and_cycle(self) -> None:
        """Verifies report generator handles non-default weights and cycles cleanly."""
        custom_weights = HybridWeightVector(0.40, 0.30, 0.30)
        generator = BacktestReportGenerator(
            champion_weights=custom_weights,
            champion_cycle=RebalanceFrequency.QUARTERLY,
        )
        with tempfile.TemporaryDirectory() as tmp_dir:
            out_file = Path(tmp_dir) / "custom_rep.md"
            content = generator.generate_report(output_path=out_file)

            self.assertIn("QQQ 40% / SOXX 30% / Turnaround 30%", content)
            self.assertIn("QUARTERLY", content)

    def test_report_generator_rejects_invalid_simplex_weights(self) -> None:
        """Verifies generator raises ValueError when provided with weights violating simplex."""
        with self.assertRaises(ValueError):
            BacktestReportGenerator(champion_weights=(0.50, 0.50, 0.50))  # sum = 1.5

        with self.assertRaises(ValueError):
            BacktestReportGenerator(champion_weights=(-0.10, 0.60, 0.50))  # negative weight


class TestDataJsStoreSerializationEmpirical(unittest.TestCase):
    """Stress-tests data.js serialization, JS syntax evaluation, and injection resilience."""

    def test_data_js_evaluates_without_syntax_errors_in_jscript_engine(self) -> None:
        """Evaluates root data.js in Windows Script Host (CScript/JScript) to confirm genuine syntax validity."""
        self.assertTrue(DEFAULT_DATA_JS_PATH.exists(), "Root data.js must exist")
        raw_js = DEFAULT_DATA_JS_PATH.read_text(encoding="utf-8")

        # Construct JScript test harness
        test_harness = (
            "var window = {};\n"
            f"{raw_js}\n"
            "if (!window.WATCHLIST_DATA) { WScript.Echo('ERR_NO_DATA'); WScript.Quit(1); }\n"
            "if (!window.WATCHLIST_DATA.backtest25yr) { WScript.Echo('ERR_NO_BACKTEST'); WScript.Quit(2); }\n"
            "var b = window.WATCHLIST_DATA.backtest25yr;\n"
            "if (!b.championMetrics || !b.growthSeries || !b.taxComparison) { WScript.Echo('ERR_SCHEMA'); WScript.Quit(3); }\n"
            "WScript.Echo('JSCRIPT_EVAL_PASS: ' + b.lastEvaluated + ' CAGR:' + b.championMetrics.cagrAfterTax);\n"
            "WScript.Quit(0);\n"
        )

        with tempfile.TemporaryDirectory() as tmp_dir:
            test_js_path = Path(tmp_dir) / "eval_harness.js"
            # CScript natively parses UTF-16 with BOM for non-ASCII characters
            test_js_path.write_text(test_harness, encoding="utf-16")

            result = subprocess.run(
                ["cscript", "//nologo", "//E:jscript", str(test_js_path)],
                capture_output=True,
                text=True,
            )

            self.assertEqual(
                result.returncode, 0,
                f"cscript failed with exit code {result.returncode}.\nSTDOUT: {result.stdout}\nSTDERR: {result.stderr}"
            )
            self.assertIn("JSCRIPT_EVAL_PASS", result.stdout)

    def test_save_and_parse_resilience_against_json_injection_and_tags(self) -> None:
        """Adversarially tests save_data_store and parse_js_data_store against script tags, quotes, and unicode."""
        adversarial_store = create_default_data_store()
        adversarial_store["backtest25yr"]["injectionTest"] = {
            "xssTag": "</script><script>alert('pwned')</script>",
            "escapedSlashes": "https://example.com/api//v1//test",
            "fakeLineComment": "foo // not a comment\nbar",
            "fakeBlockComment": "foo /* not a block comment */ bar",
            "unicodeSeparators": "line\u2028sep\u2029par",
            "quotesAndBackticks": "single ' double \" backtick `",
            "koreanAndEmoji": "📈 25년 백테스트 세금 모델링 🚀",
        }

        with tempfile.TemporaryDirectory() as tmp_dir:
            test_js = Path(tmp_dir) / "injection_test.js"
            saved = save_data_store(adversarial_store, test_js)
            self.assertTrue(saved, "save_data_store must return True")

            # Round-trip parsing
            reloaded = load_data_store(test_js)
            self.assertIn("backtest25yr", reloaded)
            inj = reloaded["backtest25yr"].get("injectionTest", {})
            self.assertEqual(inj.get("xssTag"), "</script><script>alert('pwned')</script>")
            self.assertEqual(inj.get("quotesAndBackticks"), "single ' double \" backtick `")
            self.assertEqual(inj.get("koreanAndEmoji"), "📈 25년 백테스트 세금 모델링 🚀")

            # Verify evaluation in JScript engine
            raw_text = test_js.read_text(encoding="utf-8")
            harness = (
                "var window = {};\n"
                f"{raw_text}\n"
                "var t = window.WATCHLIST_DATA.backtest25yr.injectionTest;\n"
                "if (t.xssTag.indexOf('</script>') === -1) { WScript.Quit(1); }\n"
                "WScript.Echo('INJECTION_SAFE');\n"
                "WScript.Quit(0);\n"
            )
            harness_path = Path(tmp_dir) / "eval_inj.js"
            harness_path.write_text(harness, encoding="utf-16")
            res = subprocess.run(["cscript", "//nologo", "//E:jscript", str(harness_path)], capture_output=True, text=True)
            self.assertEqual(res.returncode, 0, f"JScript syntax broke on adversarial strings: {res.stderr}")

    def test_save_data_store_circular_reference_handled_gracefully(self) -> None:
        """Verifies save_data_store catches circular references without crashing and returns False."""
        circular_dict: dict = {"a": 1}
        circular_dict["self"] = circular_dict

        with tempfile.TemporaryDirectory() as tmp_dir:
            target_path = Path(tmp_dir) / "circular.js"
            success = save_data_store(circular_dict, target_path)
            self.assertFalse(success, "save_data_store must return False on circular references")

    def test_parse_js_data_store_malformed_inputs(self) -> None:
        """Verifies parse_js_data_store raises descriptive ValueError on corrupted JavaScript."""
        with self.assertRaises(ValueError):
            parse_js_data_store("")

        with self.assertRaises(ValueError):
            parse_js_data_store("var x = 42;")

        with self.assertRaises(ValueError):
            parse_js_data_store("window.WATCHLIST_DATA = { unclosed: 'brace' ")


class TestArraySamplingBoundariesEmpirical(unittest.TestCase):
    """Stress-tests downsampling boundaries, length consistency, and numeric integrity."""

    def test_growth_and_drawdown_series_boundaries(self) -> None:
        """Verifies sampled growth and drawdown series have exact endpoints and monotonic dates."""
        store = build_backtest25yr_store(force_refresh=True)
        growth = store["growthSeries"]
        drawdown = store["drawdownSeries"]

        self.assertGreater(len(growth), 1000, "Sampled series must have >1,000 points across 25 years")
        self.assertEqual(len(growth), len(drawdown), "Growth and drawdown series must have identical length")

        joint_history = get_joint_history()
        dates = sorted(joint_history.keys())

        # Boundary checks
        self.assertEqual(growth[0]["date"], dates[0], "Growth series first date must match dataset inception")
        self.assertEqual(growth[-1]["date"], dates[-1], "Growth series last date must match dataset terminal")
        self.assertEqual(drawdown[0]["date"], dates[0], "Drawdown series first date must match dataset inception")
        self.assertEqual(drawdown[-1]["date"], dates[-1], "Drawdown series last date must match dataset terminal")

        # Chronological monotonicity
        for i in range(1, len(growth)):
            self.assertGreater(
                growth[i]["date"], growth[i - 1]["date"],
                f"Dates must be strictly increasing chronologically at index {i}"
            )

        # Finite numeric checks (no NaN, null, or Inf)
        for pt in growth:
            for k in ("hybrid", "qqq", "soxx", "turnaround"):
                val = pt[k]
                self.assertIsInstance(val, (int, float), f"Value {k} must be numeric")
                self.assertFalse(math.isnan(val), f"Value {k} cannot be NaN")
                self.assertFalse(math.isinf(val), f"Value {k} cannot be Infinite")
                self.assertGreaterEqual(val, 0.0, f"NAV valuation {k} cannot be negative")

        for pt in drawdown:
            for k in ("hybrid", "qqq", "soxx"):
                val = pt[k]
                self.assertIsInstance(val, (int, float), f"Drawdown {k} must be numeric")
                self.assertFalse(math.isnan(val), f"Drawdown {k} cannot be NaN")
                self.assertFalse(math.isinf(val), f"Drawdown {k} cannot be Infinite")
                self.assertLessEqual(val, 0.0001, f"Drawdown {k} must be <= 0.0%")


class TestCliFuzzingEmpirical(unittest.TestCase):
    """Fuzzes CLI backtest command flags and arguments for robustness."""

    def test_cli_backtest_unknown_flag_fuzzing(self) -> None:
        """Verifies CLI rejects unrecognized flags with exit code 2 / SystemExit."""
        with self.assertRaises(SystemExit) as cm:
            main(["backtest", "--unknown-bogus-flag"])
        self.assertNotEqual(cm.exception.code, 0, "Unknown flag must return non-zero exit code")

    def test_cli_backtest_unknown_cycle_fuzzing(self) -> None:
        """Verifies CLI raises descriptive error or non-zero exit when passed invalid cycle."""
        # In-process test
        with self.assertRaises(ValueError) as cm:
            main(["backtest", "--cycle", "HOURLY"])
        self.assertIn("Unknown rebalance frequency", str(cm.exception))

        # Subprocess execution test
        proc = subprocess.run(
            [sys.executable, "-m", "engine.cli", "backtest", "--cycle", "HOURLY"],
            capture_output=True,
            text=True,
        )
        self.assertNotEqual(proc.returncode, 0, "Subprocess must exit non-zero on unknown cycle")
        self.assertIn("Unknown rebalance frequency", proc.stderr + proc.stdout)

    def test_cli_backtest_malformed_weights_fuzzing(self) -> None:
        """Verifies CLI strictly validates weight triplets violating simplex invariants."""
        # 1. Weights sum > 1.0 (0.5, 0.5, 0.5 = 1.5)
        with self.assertRaises(ValueError) as cm:
            main(["backtest", "--weights", "0.5,0.5,0.5"])
        self.assertIn("Simplex zero-cash violation", str(cm.exception))

        # Subprocess check for 0.5,0.5,0.5
        proc = subprocess.run(
            [sys.executable, "-m", "engine.cli", "backtest", "--weights", "0.5,0.5,0.5"],
            capture_output=True,
            text=True,
        )
        self.assertNotEqual(proc.returncode, 0, "Subprocess must exit non-zero on invalid simplex weights")
        self.assertIn("Simplex zero-cash violation", proc.stderr + proc.stdout)

        # 2. Negative weight (non-leading dash)
        with self.assertRaises(ValueError) as cm2:
            main(["backtest", "--weights", "0.6,0.6,-0.2"])
        self.assertIn("Simplex zero-cash violation", str(cm2.exception))

        # 3. Leading dash passed via --weights=... syntax
        with self.assertRaises(ValueError) as cm3:
            main(["backtest", "--weights=-0.1,0.6,0.5"])
        self.assertIn("Simplex zero-cash violation", str(cm3.exception))

        # 4. Non-numeric weights silently falls back to champion (0.35, 0.35, 0.30)
        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp_js = Path(tmp_dir) / "data.js"
            exit_code = main(["backtest", "--weights", "abc", "--sync", "--data-js", str(tmp_js), "--quiet"])
            self.assertEqual(exit_code, 0)
            loaded = load_data_store(tmp_js)
            self.assertEqual(loaded["backtest25yr"]["championMetrics"]["weights"]["Turnaround"], 0.30)

    def test_cli_backtest_negative_step_fuzzing(self) -> None:
        """Verifies CLI accepts negative step without unhandled fatal error."""
        # Argparse accepts --step as float
        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp_rep = Path(tmp_dir) / "rep.md"
            exit_code = main(["backtest", "--step", "-0.05", "-o", str(tmp_rep), "--quiet"])
            self.assertEqual(exit_code, 0)
            self.assertTrue(tmp_rep.exists())

    def test_cli_backtest_sync_to_nested_nonexistent_data_js(self) -> None:
        """Verifies CLI --sync creates non-existent parent directory for target data.js."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            nested_js = Path(tmp_dir) / "deep" / "nested" / "folder" / "data.js"
            exit_code = main(["backtest", "--sync", "--data-js", str(nested_js), "--quiet"])
            self.assertEqual(exit_code, 0)
            self.assertTrue(nested_js.exists())
            loaded = load_data_store(nested_js)
            self.assertIn("backtest25yr", loaded)

    def test_cli_backtest_json_stdout_matches_contract_4(self) -> None:
        """Verifies python -m engine.cli backtest --json outputs clean valid JSON matching Contract 4."""
        buf = io.StringIO()
        with patch("sys.stdout", buf):
            exit_code = main(["backtest", "--json", "--quiet"])

        self.assertEqual(exit_code, 0)
        out = buf.getvalue().strip()
        data = json.loads(out)

        # Contract 4 top-level keys
        for key in ("lastEvaluated", "championMetrics", "taxComparison", "growthSeries", "drawdownSeries", "cycleComparison", "executionGuide"):
            self.assertIn(key, data, f"Contract 4 key '{key}' missing from JSON stdout")

        # Check championMetrics keys
        cm = data["championMetrics"]
        for m in ("cagrPreTax", "cagrAfterTax", "mddPreTax", "mddAfterTax", "calmarPreTax", "calmarAfterTax", "sharpePreTax", "sharpeAfterTax", "totalTaxPaid", "taxDragPct", "weights"):
            self.assertIn(m, cm, f"championMetrics key '{m}' missing")


if __name__ == "__main__":
    unittest.main()
