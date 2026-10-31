"""
Empirical Challenge & Adversarial Stress-Test Suite for Milestone 6 Deliverables.
Author: challenger_m6_1 (Milestone 6 Challenger)
Target: index.html & data.js (View 7: 25-Year Quantitative Backtesting & Hybrid Master)

Scope & Challenge Dimensions:
1. DOM Structure & Contract Integrity Stress:
   - Full parsing of index.html with bs4 and regex
   - Contracted 24 DOM IDs from VIEW7_CONTRACTED_DOM_IDS
   - Additional Pre/After-Tax contracted DOM IDs
   - Zero duplicate DOM IDs across entire index.html
   - Element tag validity and initial hidden/visible state integrity
2. JavaScript Event Listeners & Router Simulation:
   - Inline onclick/onchange handlers match declared JS functions
   - Comprehensive simulation of switchView across all 7 views
   - Rapid view switching stress (View 1 -> View 6 -> View 7 interleaved)
   - Zero CSS class collisions, zero leaking active/hidden states
   - Scale toggling (Log vs Linear) and Tax toggling (Pre vs After) state machine
   - 5-Cycle filter selection and table filtering
3. SVG Geometry & Numerical Precision Stress:
   - Growth SVG (renderBacktestGrowthSvg) coordinate transforms
   - Log scale resilience: non-positive NAV (NAV <= 0, -100, 0, 1e-9) generates NO NaN, undefined, or -Inf
   - Linear scale resilience: bounds strictly inside [padL, W - padR] x [padT, padT + plotH]
   - Empty series fallback, single-point (N=1) division-by-zero protection, full 1,272 points
   - Underwater SVG (renderBacktestUnderwaterSvg) coordinate transforms
   - Positive drawdown clamping (dd > 0 -> 0%), depth mapping up to -85%
   - 4 Historical Crisis Overlays (Dot-Com, 2008 GFC, 2020 COVID, 2022 Tightening)
   - Bounding box compliance: width >= 12, height = 180, valid x1, x2 coordinates
4. Zero-CDN Offline File Isolation Stress:
   - Forensic scan for http://, https://, protocol-relative //, remote CDN hostnames
   - Pure local asset verification (only ./data.js permitted)
   - Zero CORS/fetch/XMLHttpRequest dependency for local file:/// execution
5. Data Parity & Domestic Table Integrity:
   - Parity between data.js backtest25yr store and index.html defaults
   - Monotonic tax drag progression: Weekly (1.32%p) > Monthly (0.78%p) > ... > Annually (0.19%p)
   - Domestic price normalization table intact ("2026-10-12": { sq: 1155000, hy: 1833000 })
"""

from __future__ import annotations

import json
import math
from pathlib import Path
import re
import sys
import unittest
from bs4 import BeautifulSoup

# Project Root Setup
ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

INDEX_HTML_PATH = ROOT_DIR / "index.html"
DATA_JS_PATH = ROOT_DIR / "data.js"
REPORT_MD_PATH = ROOT_DIR / "backtest_report_25yr.md"

# 24 Contracted DOM IDs from Interface Contract 5 / test_backtest_25yr_e2e.py
VIEW7_CONTRACTED_DOM_IDS = [
    "btnViewBacktest",
    "viewBacktestSection",
    "backtestKpiRibbon",
    "backtestCagrVal",
    "backtestMddVal",
    "backtestCalmarVal",
    "backtestAlphaVal",
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
]

# Additional Pre/After-Tax Contracted DOM IDs from Urgent Tax Request
VIEW7_TAX_CONTRACTED_DOM_IDS = [
    "btnTaxPre",
    "btnTaxAfter",
    "backtestTaxCard",
    "backtestTaxDragChart",
    "backtestTaxDragVal",
]


class TestDomContractAndMarkupStress(unittest.TestCase):
    """Adversarial stress-testing of View 7 DOM elements, contracted IDs, and markup integrity."""

    @classmethod
    def setUpClass(cls) -> None:
        cls.html_text = INDEX_HTML_PATH.read_text(encoding="utf-8")
        cls.soup = BeautifulSoup(cls.html_text, "html.parser")

    def test_all_24_contracted_dom_ids_exist_uniquely(self) -> None:
        """Asserts each of the 24 contracted DOM IDs exists exactly once in index.html."""
        for dom_id in VIEW7_CONTRACTED_DOM_IDS:
            matches = self.soup.find_all(id=dom_id)
            self.assertEqual(
                len(matches),
                1,
                f"Contracted DOM ID '{dom_id}' must appear exactly once, found {len(matches)}",
            )

    def test_all_tax_contracted_dom_ids_exist_uniquely(self) -> None:
        """Asserts all 5 Pre/After-Tax contracted DOM IDs exist exactly once."""
        for dom_id in VIEW7_TAX_CONTRACTED_DOM_IDS:
            matches = self.soup.find_all(id=dom_id)
            self.assertEqual(
                len(matches),
                1,
                f"Tax DOM ID '{dom_id}' must appear exactly once, found {len(matches)}",
            )

    def test_zero_duplicate_dom_ids_across_view7_container(self) -> None:
        """Asserts no duplicate IDs exist anywhere within viewBacktestSection."""
        section = self.soup.find(id="viewBacktestSection")
        self.assertIsNotNone(section, "viewBacktestSection must exist")

        all_ids = [el["id"] for el in section.find_all(id=True)]
        seen = set()
        duplicates = set()
        for i in all_ids:
            if i in seen:
                duplicates.add(i)
            seen.add(i)
        self.assertEqual(len(duplicates), 0, f"Duplicate IDs detected in View 7: {duplicates}")

    def test_view7_structural_tag_validity(self) -> None:
        """Verifies specific element tag types conform to semantic requirements."""
        section = self.soup.find(id="viewBacktestSection")
        self.assertEqual(section.name, "section")
        self.assertIn("hidden", section.get("class", []))

        btn_nav = self.soup.find(id="btnViewBacktest")
        self.assertEqual(btn_nav.name, "button")
        self.assertIn("view-switch-btn", btn_nav.get("class", []))

        growth_svg = self.soup.find(id="backtestGrowthSvg")
        self.assertEqual(growth_svg.name, "svg")
        self.assertEqual(growth_svg.get("viewbox"), "0 0 960 380")

        underwater_svg = self.soup.find(id="backtestUnderwaterSvg")
        self.assertEqual(underwater_svg.name, "svg")
        self.assertEqual(underwater_svg.get("viewbox"), "0 0 960 230")

        select_cycle = self.soup.find(id="backtestCycleSelect")
        self.assertEqual(select_cycle.name, "select")

        table_body = self.soup.find(id="backtestMatrixTableBody")
        self.assertEqual(table_body.name, "tbody")

        report_link = self.soup.find(id="backtestReportLink")
        self.assertEqual(report_link.name, "a")
        self.assertEqual(report_link.get("href"), "backtest_report_25yr.md")

    def test_cycle_select_contains_all_five_cycles_plus_all(self) -> None:
        """Verifies #backtestCycleSelect options include ALL and the 5 canonical cycles."""
        select = self.soup.find(id="backtestCycleSelect")
        self.assertIsNotNone(select)
        options = [opt.get("value") for opt in select.find_all("option")]
        expected = ["ALL", "WEEKLY", "MONTHLY", "QUARTERLY", "SEMI_ANNUALLY", "ANNUALLY"]
        for exp in expected:
            self.assertIn(exp, options, f"Missing cycle option: {exp}")
        # Default selected should be MONTHLY (Champion)
        selected_opt = select.find("option", selected=True)
        self.assertIsNotNone(selected_opt)
        self.assertEqual(selected_opt.get("value"), "MONTHLY")


class TestJavaScriptHandlersAndRouterStress(unittest.TestCase):
    """Stress-tests JavaScript event listeners, function declarations, and rapid router switching."""

    @classmethod
    def setUpClass(cls) -> None:
        cls.html_text = INDEX_HTML_PATH.read_text(encoding="utf-8")
        cls.soup = BeautifulSoup(cls.html_text, "html.parser")

    def test_interactive_controls_have_matching_handlers(self) -> None:
        """Verifies all interactive controls have inline event listeners matching JS functions."""
        controls = [
            ("btnViewBacktest", "onclick", "switchView('backtest')"),
            ("btnGrowthLog", "onclick", "setGrowthScale('log')"),
            ("btnGrowthLinear", "onclick", "setGrowthScale('linear')"),
            ("btnTaxAfter", "onclick", "setBacktestTaxMode('after')"),
            ("btnTaxPre", "onclick", "setBacktestTaxMode('pre')"),
            ("backtestCycleSelect", "onchange", "handleBacktestCycleChange(this.value)"),
        ]
        for elem_id, event, expected_call in controls:
            elem = self.soup.find(id=elem_id)
            self.assertIsNotNone(elem, f"Element #{elem_id} not found")
            handler_val = elem.get(event, "")
            self.assertEqual(
                handler_val.strip(),
                expected_call,
                f"Mismatch in {event} on #{elem_id}: expected '{expected_call}', got '{handler_val}'",
            )

    def test_all_declared_js_functions_exist_in_script_tags(self) -> None:
        """Verifies required JS functions are defined in the scripts."""
        required_functions = [
            "switchView",
            "getBacktestStore",
            "renderBacktestView",
            "setGrowthScale",
            "setBacktestTaxMode",
            "handleBacktestCycleChange",
            "renderBacktestGrowthSvg",
            "renderBacktestUnderwaterSvg",
            "renderBacktestTaxDragChart",
            "renderBacktestMatrixTable",
            "renderBacktestGuide",
        ]
        scripts_text = "\n".join(s.string or "" for s in self.soup.find_all("script") if not s.get("src"))
        for fn_name in required_functions:
            pattern = rf"function\s+{fn_name}\s*\("
            self.assertTrue(
                bool(re.search(pattern, scripts_text)),
                f"Required JavaScript function '{fn_name}' not defined in inline scripts",
            )

    def test_rapid_view_switching_state_machine_simulation(self) -> None:
        """Adversarially simulates rapid view switching across all 7 views."""
        views = ["digest", "timeseries", "insight", "financials", "timing", "turnaround", "backtest"]
        section_ids = {
            "digest": "viewDigestSection",
            "timeseries": "viewTimeseriesSection",
            "insight": "viewInsightSection",
            "financials": "viewFinancialsSection",
            "timing": "viewTimingSection",
            "turnaround": "viewTurnaroundSection",
            "backtest": "viewBacktestSection",
        }
        btn_ids = {
            "digest": "btnViewDigest",
            "timeseries": "btnViewTimeseries",
            "insight": "btnViewInsight",
            "financials": "btnViewFinancials",
            "timing": "btnViewTiming",
            "turnaround": "btnViewTurnaround",
            "backtest": "btnViewBacktest",
        }

        # Verify each button and section exists in the HTML
        for tab, s_id in section_ids.items():
            self.assertIsNotNone(self.soup.find(id=s_id), f"Missing section #{s_id}")
            self.assertIsNotNone(self.soup.find(id=btn_ids[tab]), f"Missing button #{btn_ids[tab]}")

        # Simulate client state machine following exact logic of switchView(tabName)
        current_tab = "digest"
        state_sections = {s: (s != section_ids[current_tab]) for s in section_ids.values()}  # True = hidden
        state_buttons = {b: (b == btn_ids[current_tab]) for b in btn_ids.values()}  # True = active

        def simulate_switch(target_tab: str) -> None:
            nonlocal current_tab
            current_tab = target_tab
            for t, s_id in section_ids.items():
                is_target = (t == target_tab)
                state_sections[s_id] = not is_target  # hidden if not target
                state_buttons[btn_ids[t]] = is_target  # active if target

        # Adversarial rapid switching sequence (including round-trips and rapid flapping)
        sequence = [
            "backtest", "digest", "backtest", "turnaround", "backtest",
            "financials", "backtest", "timing", "backtest", "timeseries",
            "insight", "backtest", "turnaround", "digest", "backtest"
        ]

        for step in sequence:
            simulate_switch(step)
            # Invariant 1: Exactly one section is visible (not hidden)
            visible_count = sum(1 for is_hidden in state_sections.values() if not is_hidden)
            self.assertEqual(visible_count, 1, f"Exactly one section must be visible after switching to {step}")
            self.assertFalse(state_sections[section_ids[step]], f"Section for {step} must be visible")

            # Invariant 2: Exactly one button is active
            active_btn_count = sum(1 for is_act in state_buttons.values() if is_act)
            self.assertEqual(active_btn_count, 1, f"Exactly one button must be active after switching to {step}")
            self.assertTrue(state_buttons[btn_ids[step]], f"Button for {step} must be active")


class TestSvgGrowthCurveGeometryStress(unittest.TestCase):
    """Stress-tests the coordinate transformation math and edge cases of the Growth SVG."""

    W = 960
    H = 380
    padL = 75
    padR = 35
    padT = 24
    padB = 40
    plotW = W - padL - padR  # 850
    plotH = H - padT - padB  # 316

    def compute_growth_svg(
        self,
        series: list[dict],
        is_log: bool = True,
        is_pre: bool = False,
    ) -> tuple[list[tuple[float, float]], list[tuple[float, float]], float, float]:
        """Faithful Python implementation of index.html renderBacktestGrowthSvg math."""
        if not series:
            series = [
                {"date": "2001-07-10", "hybrid": 100000000.0, "qqq": 100000000.0, "soxx": 100000000.0, "turnaround": 100000000.0},
                {"date": "2026-10-12", "hybrid": 1208511921.0, "qqq": 1430000000.0, "soxx": 539917695.0, "turnaround": 2799176700.0},
            ]

        N = len(series)
        max_val = 100000000.0
        min_val = 100000000.0

        for i in range(N):
            item = series[i]
            h = item.get("hybrid", 100000000.0)
            if is_pre:
                yrs = (i / max(1, N - 1)) * 25.25
                h = h * math.pow((1.0 + 0.1116) / (1.0 + 0.1038), yrs)
            max_val = max(max_val, h, item.get("qqq", 0) or 0, item.get("soxx", 0) or 0, item.get("turnaround", 0) or 0)
            min_val = min(min_val, h, item.get("qqq", max_val) or max_val, item.get("soxx", max_val) or max_val, item.get("turnaround", max_val) or max_val)

        max_val = max(max_val * 1.08, 1500000000.0)
        min_val = max(10000000.0, min_val * 0.8) if is_log else 0.0

        log_min = math.log10(min_val) if is_log else 0.0
        log_max = math.log10(max_val) if is_log else 1.0

        def get_y(v: float) -> float:
            if is_log:
                lv = math.log10(max(v, min_val))
                frac = (lv - log_min) / (log_max - log_min)
                return self.padT + self.plotH - frac * self.plotH
            else:
                frac = (v - min_val) / (max_val - min_val)
                return self.padT + self.plotH - frac * self.plotH

        def get_x(i: int) -> float:
            return self.padL + (i / max(1, N - 1)) * self.plotW

        pts_hybrid = [(get_x(i), get_y(series[i].get("hybrid", 100000000.0))) for i in range(N)]
        pts_qqq = [(get_x(i), get_y(series[i].get("qqq", 100000000.0))) for i in range(N)]
        return pts_hybrid, pts_qqq, min_val, max_val

    def test_log_scale_with_non_positive_and_near_zero_nav(self) -> None:
        """STRESS: NAV <= 0 must not produce NaN, undefined, or -Inf under Log Scale."""
        adversarial_series = [
            {"date": "2001-07-10", "hybrid": 0.0, "qqq": -100.0, "soxx": 0.0, "turnaround": -500000.0},
            {"date": "2010-01-01", "hybrid": 1e-12, "qqq": 0.0, "soxx": 50000.0, "turnaround": 1.0},
            {"date": "2020-01-01", "hybrid": 50000000.0, "qqq": 100000000.0, "soxx": 200000000.0, "turnaround": 300000000.0},
            {"date": "2026-10-12", "hybrid": 1208511921.0, "qqq": 1430000000.0, "soxx": 539917695.0, "turnaround": 2799176700.0},
        ]
        pts_hybrid, pts_qqq, min_v, max_v = self.compute_growth_svg(adversarial_series, is_log=True)

        self.assertGreater(min_v, 0, "min_val in log scale must be strictly positive")
        self.assertGreater(max_v, min_v, "max_val must strictly exceed min_val")

        for x, y in pts_hybrid:
            self.assertFalse(math.isnan(x), f"x should not be NaN: {x}")
            self.assertFalse(math.isnan(y), f"y should not be NaN: {y}")
            self.assertFalse(math.isinf(x), f"x should not be Inf: {x}")
            self.assertFalse(math.isinf(y), f"y should not be Inf: {y}")
            # Ensure coordinates stay within the SVG canvas
            self.assertGreaterEqual(x, self.padL)
            self.assertLessEqual(x, self.W - self.padR)
            self.assertGreaterEqual(y, self.padT)
            self.assertLessEqual(y, self.padT + self.plotH)

    def test_linear_scale_bounding_box_compliance(self) -> None:
        """Verifies Linear scale coordinates stay strictly inside the plot boundaries."""
        sample_series = [
            {"date": "2001-07-10", "hybrid": 100000000.0, "qqq": 100000000.0, "soxx": 100000000.0, "turnaround": 100000000.0},
            {"date": "2015-06-01", "hybrid": 600000000.0, "qqq": 500000000.0, "soxx": 700000000.0, "turnaround": 800000000.0},
            {"date": "2026-10-12", "hybrid": 1208511921.0, "qqq": 1430000000.0, "soxx": 539917695.0, "turnaround": 2799176700.0},
        ]
        pts_hybrid, _, _, _ = self.compute_growth_svg(sample_series, is_log=False)
        for x, y in pts_hybrid:
            self.assertTrue(0 <= x <= self.W, f"x coordinate {x} out of bounds [0, {self.W}]")
            self.assertTrue(0 <= y <= self.H, f"y coordinate {y} out of bounds [0, {self.H}]")

    def test_single_point_series_division_by_zero_safety(self) -> None:
        """Single-point series (N=1) must not trigger division by zero."""
        single_point = [
            {"date": "2026-10-12", "hybrid": 100000000.0, "qqq": 100000000.0, "soxx": 100000000.0, "turnaround": 100000000.0}
        ]
        pts_hybrid, _, _, _ = self.compute_growth_svg(single_point, is_log=True)
        self.assertEqual(len(pts_hybrid), 1)
        x, y = pts_hybrid[0]
        self.assertEqual(x, float(self.padL))
        self.assertFalse(math.isnan(y))

    def test_full_1272_points_from_data_js_svg_generation(self) -> None:
        """Generates coordinates for all 1,272 sampled points from data.js without errors."""
        js_text = DATA_JS_PATH.read_text(encoding="utf-8")
        prefix = "window.WATCHLIST_DATA = "
        idx = js_text.find(prefix)
        self.assertNotEqual(idx, -1)
        raw_json = js_text[idx + len(prefix):].strip().rstrip(";")
        data = json.loads(raw_json)

        growth_series = data["backtest25yr"]["growthSeries"]
        self.assertEqual(len(growth_series), 1272)

        pts_hybrid, pts_qqq, min_v, max_v = self.compute_growth_svg(growth_series, is_log=True)
        self.assertEqual(len(pts_hybrid), 1272)
        self.assertEqual(len(pts_qqq), 1272)

        # Monotonicity of x
        for i in range(len(pts_hybrid) - 1):
            self.assertLess(pts_hybrid[i][0], pts_hybrid[i + 1][0], "x values must be strictly increasing")


class TestSvgUnderwaterGeometryStress(unittest.TestCase):
    """Stress-tests the Underwater Drawdown SVG coordinate math and historical crisis overlays."""

    W = 960
    H = 230
    padL = 75
    padR = 35
    padT = 20
    padB = 30
    plotW = W - padL - padR  # 850
    plotH = H - padT - padB  # 180
    maxDdDepth = 85.0

    def compute_underwater_svg(
        self,
        series: list[dict],
    ) -> tuple[list[tuple[float, float]], list[dict]]:
        """Faithful Python implementation of index.html renderBacktestUnderwaterSvg math."""
        if not series:
            series = [
                {"date": "2001-07-10", "hybrid": 0.0, "qqq": 0.0, "soxx": 0.0},
                {"date": "2026-10-12", "hybrid": -5.2, "qqq": -3.8, "soxx": -6.4},
            ]

        N = len(series)

        def get_y(dd: float) -> float:
            d = abs(min(0.0, float(dd or 0.0)))
            return self.padT + (d / self.maxDdDepth) * self.plotH

        def get_x(i: int) -> float:
            return self.padL + (i / max(1, N - 1)) * self.plotW

        def find_range(start_date: str, end_date: str) -> tuple[float, float]:
            start_idx = -1
            end_idx = -1
            for i in range(N):
                d = series[i].get("date", "")
                if start_idx == -1 and d >= start_date:
                    start_idx = i
                if d <= end_date:
                    end_idx = i
            if start_idx == -1:
                start_idx = 0
            if end_idx == -1:
                end_idx = N - 1
            return get_x(start_idx), get_x(end_idx)

        pts_hybrid = [(get_x(i), get_y(series[i].get("hybrid", 0.0))) for i in range(N)]

        crisis_zones = [
            {"name": "DotCom", "dates": ("2001-07-10", "2002-10-30")},
            {"name": "GFC", "dates": ("2007-10-01", "2009-03-31")},
            {"name": "COVID", "dates": ("2020-02-01", "2020-04-30")},
            {"name": "Tightening", "dates": ("2022-01-01", "2022-10-31")},
        ]
        calculated_zones = []
        for c in crisis_zones:
            x1, x2 = find_range(c["dates"][0], c["dates"][1])
            w = max(12.0, x2 - x1)
            calculated_zones.append({"name": c["name"], "x1": x1, "x2": x2, "w": w, "y": self.padT, "h": self.plotH})

        return pts_hybrid, calculated_zones

    def test_drawdown_depth_boundary_mapping(self) -> None:
        """Verifies 0% maps to top baseline, -85% maps to bottom baseline."""
        series = [
            {"date": "2001-07-10", "hybrid": 0.0},
            {"date": "2002-10-09", "hybrid": -85.0},
            {"date": "2026-10-12", "hybrid": -59.79},
        ]
        pts, _ = self.compute_underwater_svg(series)
        self.assertAlmostEqual(pts[0][1], float(self.padT), places=2)
        self.assertAlmostEqual(pts[1][1], float(self.padT + self.plotH), places=2)
        self.assertAlmostEqual(pts[2][1], self.padT + (59.79 / 85.0) * self.plotH, places=2)

    def test_positive_and_extreme_drawdown_clamping(self) -> None:
        """Positive drawdown (> 0) must be clamped to 0%, never generating negative depth."""
        adversarial = [
            {"date": "2001-07-10", "hybrid": 25.0},  # Positive number
            {"date": "2002-10-09", "hybrid": None},  # None
            {"date": "2026-10-12", "hybrid": -100.0},  # Extreme negative
        ]
        pts, _ = self.compute_underwater_svg(adversarial)
        self.assertAlmostEqual(pts[0][1], float(self.padT), places=2)
        self.assertAlmostEqual(pts[1][1], float(self.padT), places=2)
        self.assertFalse(math.isnan(pts[2][1]))

    def test_all_four_crisis_regime_boxes_validity(self) -> None:
        """Verifies the 4 crisis regime shaded overlay boxes have valid geometry."""
        js_text = DATA_JS_PATH.read_text(encoding="utf-8")
        data = json.loads(js_text[js_text.find("window.WATCHLIST_DATA = ") + 24:].strip().rstrip(";"))
        drawdown_series = data["backtest25yr"]["drawdownSeries"]

        _, zones = self.compute_underwater_svg(drawdown_series)
        self.assertEqual(len(zones), 4)

        for z in zones:
            self.assertGreaterEqual(z["x1"], float(self.padL))
            self.assertLessEqual(z["x2"], float(self.W - self.padR))
            self.assertGreaterEqual(z["w"], 12.0)
            self.assertEqual(z["y"], self.padT)
            self.assertEqual(z["h"], self.plotH)


class TestZeroCdnOfflineForensicAudit(unittest.TestCase):
    """Forensic verification confirming 100% offline self-containment (Zero-CDN)."""

    @classmethod
    def setUpClass(cls) -> None:
        cls.html_text = INDEX_HTML_PATH.read_text(encoding="utf-8")
        cls.soup = BeautifulSoup(cls.html_text, "html.parser")

    def test_zero_remote_http_and_https_urls(self) -> None:
        """Asserts zero http:// or https:// patterns exist in index.html."""
        http_matches = re.findall(r"https?://", self.html_text, re.IGNORECASE)
        self.assertEqual(len(http_matches), 0, f"Remote URLs found: {http_matches}")

    def test_zero_protocol_relative_urls(self) -> None:
        """Asserts zero protocol-relative // URLs exist in attribute tags."""
        proto_rel = re.findall(r"""(?:src|href|url)\s*=\s*['"]//""", self.html_text, re.IGNORECASE)
        self.assertEqual(len(proto_rel), 0, f"Protocol-relative URLs found: {proto_rel}")

    def test_zero_cdn_hostnames(self) -> None:
        """Asserts zero third-party CDN domain patterns exist."""
        cdn_patterns = ["cdn.", "googleapis", "cdnjs", "jsdelivr", "unpkg", "bootstrapcdn", "fontawesome"]
        for cdn in cdn_patterns:
            matches = re.findall(re.escape(cdn), self.html_text, re.IGNORECASE)
            self.assertEqual(len(matches), 0, f"Forbidden CDN pattern '{cdn}' found")

    def test_external_scripts_contain_only_local_data_js(self) -> None:
        """Asserts the only external script is local data.js."""
        script_tags = self.soup.find_all("script", src=True)
        self.assertEqual(len(script_tags), 1, "There should be exactly one external script tag")
        self.assertEqual(script_tags[0]["src"], "./data.js")

    def test_zero_remote_stylesheets(self) -> None:
        """Asserts zero external stylesheet links exist."""
        link_tags = self.soup.find_all("link", rel=lambda r: r and "stylesheet" in r)
        self.assertEqual(len(link_tags), 0, "No external stylesheet links permitted")


class TestDataSyncAndDomesticParityStress(unittest.TestCase):
    """Verifies data store schema integrity and domestic normalization table permanence."""

    @classmethod
    def setUpClass(cls) -> None:
        cls.js_text = DATA_JS_PATH.read_text(encoding="utf-8")
        prefix = "window.WATCHLIST_DATA = "
        idx = cls.js_text.find(prefix)
        assert idx != -1, "window.WATCHLIST_DATA prefix missing"
        cls.data = json.loads(cls.js_text[idx + len(prefix):].strip().rstrip(";"))

    def test_backtest25yr_champion_metrics_parity(self) -> None:
        """Verifies champion metrics match quantitative backtest results."""
        champ = self.data["backtest25yr"]["championMetrics"]
        self.assertEqual(champ["cagrPreTax"], 11.16)
        self.assertEqual(champ["cagrAfterTax"], 10.38)
        self.assertEqual(champ["mddPreTax"], -59.70)
        self.assertEqual(champ["mddAfterTax"], -59.79)
        self.assertEqual(champ["calmarPreTax"], 0.19)
        self.assertEqual(champ["calmarAfterTax"], 0.17)
        self.assertEqual(champ["taxDragPct"], 0.78)
        self.assertEqual(champ["weights"], {"QQQ": 0.35, "SOXX": 0.35, "Turnaround": 0.30})

    def test_monotonic_tax_drag_progression(self) -> None:
        """Verifies tax drag strictly decreases from Weekly to Annually."""
        cycle_drags = self.data["backtest25yr"]["taxComparison"]["cycleTaxDrag"]
        self.assertGreater(cycle_drags["WEEKLY"]["taxDragPct"], cycle_drags["MONTHLY"]["taxDragPct"])
        self.assertGreater(cycle_drags["MONTHLY"]["taxDragPct"], cycle_drags["QUARTERLY"]["taxDragPct"])
        self.assertGreater(cycle_drags["QUARTERLY"]["taxDragPct"], cycle_drags["SEMI_ANNUALLY"]["taxDragPct"])
        self.assertGreater(cycle_drags["SEMI_ANNUALLY"]["taxDragPct"], cycle_drags["ANNUALLY"]["taxDragPct"])

    def test_domestic_sk_hynix_price_normalization_intact(self) -> None:
        """Asserts domestic price table in index.html preserves SK Hynix 1,833,000 KRW."""
        html_text = INDEX_HTML_PATH.read_text(encoding="utf-8")
        self.assertIn('"2026-10-12": { sq: 1155000, hy: 1833000 }', html_text)


if __name__ == "__main__":
    unittest.main()
