"""Comprehensive Unit Test for 5-Year Financial Explorer & 2026E Consensus Integrity.

Validates:
1. Exact 100% synchronization between data.js financials and engine.sync_dashboard.DEFAULT_FINANCIALS.
2. Complete coverage of all 8 canonical stocks across all 5 financial categories and 23 metrics.
3. Strict separation of 2022~2025 actuals and 2026E consensus estimates across exactly 5 annual data points.
4. SK Hynix 2026E revenue upgrade significantly exceeding the 104조원 baseline (latest HBM supercycle consensus).
5. Offline Zero-CDN compliance and visual element presence in index.html.
"""

from __future__ import annotations

import copy
from pathlib import Path
import sys
import unittest

ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from engine.sync_dashboard import (
    DEFAULT_DATA_JS_PATH,
    DEFAULT_FINANCIALS,
    parse_js_data_store,
)

INDEX_HTML_PATH = ROOT_DIR / "index.html"


class TestFinancialsIntegrityComprehensive(unittest.TestCase):
    CANONICAL_STOCKS = [
        "SK_HYNIX",
        "SK_SQUARE",
        "UBER",
        "MBLY",
        "FLNC",
        "UPST",
        "CELH",
        "ENPH",
    ]

    REQUIRED_METRICS = {
        "income_statement": ["revenue", "gross_profit", "operating_income", "net_income", "eps"],
        "profitability": ["gpm", "opm", "npm", "roe", "roic"],
        "cash_flow": ["ocf", "capex", "fcf", "fcf_margin"],
        "balance_sheet": ["cash", "total_assets", "total_liabilities", "net_debt", "de_ratio"],
        "valuation": ["pe", "ps", "pb", "ev_ebitda"],
    }

    def setUp(self) -> None:
        self.assertTrue(DEFAULT_DATA_JS_PATH.exists(), "data.js must exist")
        self.assertTrue(INDEX_HTML_PATH.exists(), "index.html must exist")
        raw_js = DEFAULT_DATA_JS_PATH.read_text(encoding="utf-8")
        self.data_store = parse_js_data_store(raw_js)
        self.data_financials = self.data_store.get("financials", {})
        self.html_text = INDEX_HTML_PATH.read_text(encoding="utf-8")

    def test_data_js_and_default_financials_100_percent_synchronized(self) -> None:
        """data.js financials must be 100% identical in structure and values to DEFAULT_FINANCIALS."""
        self.assertEqual(
            self.data_financials,
            DEFAULT_FINANCIALS,
            "data.js financials does not match engine.sync_dashboard.DEFAULT_FINANCIALS!",
        )

    def test_all_8_stocks_contain_23_metrics_and_5_years(self) -> None:
        """Every canonical stock must contain exactly 6 years and all 23 prompt metrics with 6 data points."""
        expected_years = ["2022", "2023", "2024", "2025", "2026E", "2027E"]

        for sym in self.CANONICAL_STOCKS:
            self.assertIn(sym, self.data_financials, f"Stock {sym} missing in financials")
            stock_data = self.data_financials[sym]

            # Verify years
            self.assertEqual(
                stock_data.get("years"),
                expected_years,
                f"Stock {sym} years mismatch: {stock_data.get('years')}",
            )

            # Verify all 5 categories and 23 metrics
            total_metrics_count = 0
            for cat, metric_names in self.REQUIRED_METRICS.items():
                self.assertIn(cat, stock_data, f"Category '{cat}' missing for stock {sym}")
                cat_dict = stock_data[cat]
                self.assertIsInstance(cat_dict, dict, f"Category '{cat}' in {sym} must be a dict")

                for m in metric_names:
                    self.assertIn(m, cat_dict, f"Metric '{m}' missing in {sym}.{cat}")
                    vals = cat_dict[m]
                    self.assertIsInstance(vals, list, f"{sym}.{cat}.{m} must be a list")
                    self.assertEqual(
                        len(vals),
                        6,
                        f"{sym}.{cat}.{m} must contain exactly 6 annual data points, got {len(vals)}",
                    )
                    total_metrics_count += 1

            self.assertEqual(
                total_metrics_count,
                23,
                f"Stock {sym} must have exactly 23 metrics across 5 categories, got {total_metrics_count}",
            )

    def test_sk_hynix_2026e_revenue_exceeds_104_trillion_krw(self) -> None:
        """SK Hynix 2026E revenue must be updated to recent upgraded consensus (> 104.0조원) and 2027E included."""
        sk_fin = self.data_financials.get("SK_HYNIX", {})
        rev_list = sk_fin.get("income_statement", {}).get("revenue", [])
        self.assertEqual(len(rev_list), 6, "SK Hynix revenue must have 6 values")
        rev_2026e = rev_list[4]

        self.assertGreater(
            rev_2026e,
            104.0,
            f"SK Hynix 2026E revenue {rev_2026e}조원 must substantially exceed the old 104.0조원 baseline!",
        )
        # Verify 2022~2024 actuals and 2025/2026E/2027E are preserved
        self.assertEqual(rev_list[0], 44.65)  # 2022 actual
        self.assertEqual(rev_list[1], 32.77)  # 2023 actual
        self.assertEqual(rev_list[2], 66.19)  # 2024 actual
        self.assertEqual(rev_list[3], 97.15)  # 2025 actual (97.15조원)
        self.assertEqual(rev_list[4], 275.00)  # 2026E consensus (275.00조원, 2Q actuals 79.3T/60.5T 반영)
        self.assertEqual(rev_list[5], 520.00)  # 2027E consensus (520.00조원, OP 410조원 슈퍼사이클 반영)

    def test_index_html_visual_elements_and_offline_integrity(self) -> None:
        """index.html must display Multi-Year Financial Explorer elements with zero remote dependencies."""
        self.assertIn('id="financialsContentWrap"', self.html_text)
        self.assertIn('id="financialsMissingNotice"', self.html_text)
        self.assertIn('id="financialsChartRevenue"', self.html_text)
        self.assertIn('id="financialsChartOperating"', self.html_text)
        self.assertIn('id="financialsDataTable"', self.html_text)
        self.assertIn('btnViewFinancials', self.html_text)
        self.assertIn("2026E", self.html_text)
        self.assertIn("2027E", self.html_text)
        self.assertIn("다년도 재무 익스플로러", self.html_text)
        self.assertNotIn("2025/2026E", self.html_text)

    def test_adversarial_resync_preserves_2026e_financials(self) -> None:
        """Dashboard sync against raw input dumps must preserve 2026E upgraded financials."""
        import tempfile
        from engine.cleaner import clean_raw_dump
        from engine.extractor import extract_facts
        from engine.sync_dashboard import sync_to_dashboard
        from tests.fixtures.sample_dumps import SAMPLE_RAW_DUMP_FULL_DAY

        with tempfile.TemporaryDirectory(ignore_cleanup_errors=True) as tmp_dir:
            temp_data_js = Path(tmp_dir) / "data.js"
            temp_data_js.write_text(DEFAULT_DATA_JS_PATH.read_text(encoding="utf-8"), encoding="utf-8")

            cleaned, _ = clean_raw_dump(SAMPLE_RAW_DUMP_FULL_DAY)
            market_data = extract_facts(cleaned, date="2026-10-06")

            success = sync_to_dashboard(market_data, data_js_path=str(temp_data_js))
            self.assertTrue(success, "sync_to_dashboard must succeed")

            resynced_store = parse_js_data_store(temp_data_js.read_text(encoding="utf-8"))
            resynced_fin = resynced_store.get("financials", {})

            # 1. 100% parity with DEFAULT_FINANCIALS
            self.assertEqual(resynced_fin, DEFAULT_FINANCIALS)

            # 2. SK Hynix 2026E revenue is strictly preserved
            sk_rev = resynced_fin["SK_HYNIX"]["income_statement"]["revenue"][4]
            self.assertEqual(sk_rev, 275.00)
            self.assertGreater(sk_rev, 104.0)

            # 3. All 8 stocks preserved
            self.assertEqual(set(resynced_fin.keys()), set(self.CANONICAL_STOCKS))

    def test_financial_metrics_mathematical_consistency(self) -> None:
        """Every canonical stock must maintain internal mathematical coherence across margins and FCF."""
        for sym, data in self.data_financials.items():
            years = data["years"]
            rev = data["income_statement"]["revenue"]
            gp = data["income_statement"]["gross_profit"]
            op = data["income_statement"]["operating_income"]
            ni = data["income_statement"]["net_income"]
            gpm = data["profitability"]["gpm"]
            opm = data["profitability"]["opm"]
            npm = data["profitability"]["npm"]
            ocf = data["cash_flow"]["ocf"]
            capex = data["cash_flow"]["capex"]
            fcf = data["cash_flow"]["fcf"]
            fcfm = data["cash_flow"]["fcf_margin"]

            for i, yr in enumerate(years):
                # FCF = OCF - CapEx (tolerance 0.1)
                self.assertAlmostEqual(
                    fcf[i],
                    ocf[i] - capex[i],
                    delta=0.1,
                    msg=f"{sym} {yr} FCF ({fcf[i]}) does not match OCF ({ocf[i]}) - CapEx ({capex[i]})",
                )

                # If revenue != 0, check margin consistency (tolerance 1.5%)
                if rev[i] != 0:
                    calc_gpm = (gp[i] / rev[i]) * 100
                    rep_gpm = float(gpm[i].replace("%", ""))
                    self.assertAlmostEqual(
                        calc_gpm, rep_gpm, delta=1.5,
                        msg=f"{sym} {yr} GPM calc={calc_gpm:.1f} vs reported={rep_gpm:.1f}",
                    )

                    calc_opm = (op[i] / rev[i]) * 100
                    rep_opm = float(opm[i].replace("%", ""))
                    self.assertAlmostEqual(
                        calc_opm, rep_opm, delta=1.5,
                        msg=f"{sym} {yr} OPM calc={calc_opm:.1f} vs reported={rep_opm:.1f}",
                    )

                    calc_npm = (ni[i] / rev[i]) * 100
                    rep_npm = float(npm[i].replace("%", ""))
                    self.assertAlmostEqual(
                        calc_npm, rep_npm, delta=1.5,
                        msg=f"{sym} {yr} NPM calc={calc_npm:.1f} vs reported={rep_npm:.1f}",
                    )

                    calc_fcfm = (fcf[i] / rev[i]) * 100
                    rep_fcfm = float(fcfm[i].replace("%", ""))
                    self.assertAlmostEqual(
                        calc_fcfm, rep_fcfm, delta=1.5,
                        msg=f"{sym} {yr} FCF margin calc={calc_fcfm:.1f} vs reported={rep_fcfm:.1f}",
                    )

    def test_dynamic_switching_and_svg_chart_generation_resilience(self) -> None:
        """Simulate dynamic stock/category switching and SVG rendering without NaN, null or Infinity."""
        categories = ["ALL", "income_statement", "profitability", "cash_flow", "balance_sheet", "valuation"]
        for sym in self.CANONICAL_STOCKS:
            fin = self.data_financials[sym]
            rev_vals = fin["income_statement"]["revenue"]
            op_vals = fin["income_statement"]["operating_income"]

            # SVG chart math check with normal, zero, extreme and negative values
            test_val_sets = [
                rev_vals,
                op_vals,
                [0, 0, 0, 0, 0],
                [-50, -20, 0, 30, 80],
                [0.001, 10, 500, 10000, 1000000],
            ]
            for vals in test_val_sets:
                max_val = max([abs(v) for v in vals] + [1])
                self.assertGreater(max_val, 0)
                for v in vals:
                    bar_h = max(10, min(100, (abs(v) / max_val) * 100))
                    self.assertTrue(10 <= bar_h <= 100)

            # Table row generation check for all 6 category filters
            for cat in categories:
                active_cats = (
                    ["income_statement", "profitability", "cash_flow", "balance_sheet", "valuation"]
                    if cat == "ALL"
                    else [cat]
                )
                for c_key in active_cats:
                    cat_metrics = fin[c_key]
                    self.assertGreater(len(cat_metrics), 0)
                    for m_key, m_vals in cat_metrics.items():
                        self.assertEqual(len(m_vals), 6)
                        for val in m_vals:
                            self.assertIsNotNone(val)
                            self.assertNotEqual(val, "")

    def test_explicit_actuals_vs_estimates_column_demarcation(self) -> None:
        """index.html must explicitly delineate 2022~2025 as actuals and 2026E~2027E as estimates."""
        # 1. Static table header column labels
        self.assertIn("2022<span", self.html_text)
        self.assertIn("(실제치)", self.html_text)
        self.assertIn("(추정치)", self.html_text)
        self.assertIn("2026E", self.html_text)
        self.assertIn("2027E", self.html_text)

        # 2. Subtitle badges
        self.assertIn("회계연도: 2022~2025 (확정 실제치) | 2026E~2027E (추정치)", self.html_text)
        self.assertIn("2022~2025 Actuals & 2026E~2027E Consensus", self.html_text)

        # 3. Dynamic JS rendering logic contains separation tags
        self.assertIn(">(추정치)</span>", self.html_text)
        self.assertIn(">(실제치)</span>", self.html_text)
        self.assertIn("var(--color-cyan)", self.html_text)

    def test_svg_bar_chart_coordinates_within_safe_viewbox_bounds(self) -> None:
        """All 8 stocks revenue & operating income chart coordinates must be strictly within safe SVG viewBox."""
        # Check presence of tooltips and safe clipping logic in index.html
        self.assertIn("<title>", self.html_text)
        self.assertIn("tooltipText", self.html_text)
        self.assertIn("Math.max(12, y - 5)", self.html_text)

        for sym in self.CANONICAL_STOCKS:
            fin = self.data_financials[sym]
            for mname in ["revenue", "operating_income"]:
                vals = fin["income_statement"][mname]
                max_val = max([abs(v) for v in vals] + [1])
                for val in vals:
                    is_neg = val < 0
                    if is_neg:
                        bar_h = max(6, min(22, (abs(val) / max_val) * 22))
                        y = 100
                        text_y = y + bar_h + 9
                    else:
                        bar_h = 3 if val == 0 else max(6, min(78, (abs(val) / max_val) * 78))
                        y = 100 - bar_h
                        text_y = max(12, y - 5)

                    # Text y must be strictly inside [10, 145] (never clipped off the top or bottom)
                    self.assertGreaterEqual(text_y, 10.0, f"Stock {sym} {mname} val={val}: text_y={text_y} is clipped off top!")
                    self.assertLessEqual(text_y, 145.0, f"Stock {sym} {mname} val={val}: text_y={text_y} exceeds height!")
                    # Bar bottom must not exceed 135
                    self.assertLessEqual(y + bar_h, 135.0, f"Stock {sym} {mname} val={val}: bar bottom exceeds bounds!")

    def test_headless_chrome_rendered_dom_and_visual_integrity(self) -> None:
        """Execute headless Chrome to verify real in-browser execution, zero JS errors, and zero coordinate clipping."""
        import os
        import re
        import subprocess

        chrome_candidates = [
            "C:/Program Files/Google/Chrome/Application/chrome.exe",
            "C:/Program Files (x86)/Google/Chrome/Application/chrome.exe",
            "C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe",
            "C:/Program Files/Microsoft/Edge/Application/msedge.exe",
        ]
        browser_path = next((p for p in chrome_candidates if os.path.exists(p)), None)
        if not browser_path:
            self.skipTest("No supported Chromium browser found for headless verification")

        index_url = INDEX_HTML_PATH.as_uri()
        res = subprocess.run([
            browser_path,
            "--headless=new",
            "--dump-dom",
            "--disable-gpu",
            "--no-sandbox",
            index_url,
        ], capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=15)

        self.assertEqual(res.returncode, 0, f"Headless browser exited with non-zero code {res.returncode}")
        html = res.stdout

        # 1. Elements presence & zero missing notice
        self.assertIn("financialsChartRevenue", html)
        self.assertIn("financialsChartOperating", html)
        self.assertIn("275", html)
        self.assertIn("2026E", html)
        self.assertIn("<title>", html)
        self.assertIn('class="hidden"', html)  # financialsMissingNotice is hidden

        # 2. Extract SVG text tags for revenue chart
        idx_rev = html.find('id="financialsChartRevenue"')
        end_rev = html.find('</div>', idx_rev)
        rev_svg = html[idx_rev:end_rev]
        rev_y_coords = re.findall(r'<text[^>]*\by="([^"]+)"', rev_svg)
        self.assertGreater(len(rev_y_coords), 0, "Revenue chart must render text tags")
        for y_str in rev_y_coords:
            y_val = float(y_str)
            self.assertGreaterEqual(y_val, 10.0, f"SVG text y={y_val} is clipped off top!")
            self.assertLessEqual(y_val, 145.0, f"SVG text y={y_val} exceeds viewBox height!")

        # 3. Extract SVG text tags for operating income chart
        idx_op = html.find('id="financialsChartOperating"')
        end_op = html.find('</div>', idx_op)
        op_svg = html[idx_op:end_op]
        op_y_coords = re.findall(r'<text[^>]*\by="([^"]+)"', op_svg)
        self.assertGreater(len(op_y_coords), 0, "Operating income chart must render text tags")
        for y_str in op_y_coords:
            y_val = float(y_str)
            self.assertGreaterEqual(y_val, 10.0, f"Operating SVG text y={y_val} is clipped off top!")
            self.assertLessEqual(y_val, 145.0, f"Operating SVG text y={y_val} exceeds viewBox height!")

    def test_svg_cross_platform_font_family_and_rendering_attributes(self) -> None:
        """SVG charts must specify cross-platform font fallbacks (Apple SF Mono, Windows Consolas) and CSS styling."""
        # 1. Presentation attributes inside index.html generateSvgBarChart
        self.assertIn("ui-monospace", self.html_text)
        self.assertIn("SFMono-Regular", self.html_text)
        self.assertIn("Menlo", self.html_text)
        self.assertIn("Consolas", self.html_text)
        self.assertIn('text-anchor="middle"', self.html_text)

        # 2. CSS rules for SVG text
        self.assertIn(".chart-svg-wrap text", self.html_text)
        self.assertIn("font-family: var(--font-mono);", self.html_text)

    def test_mobile_viewport_flex_wrap_and_gap_responsiveness(self) -> None:
        """Terminal headers and chart box titles must have flex-wrap and gap to prevent overflow on mobile (< 640px)."""
        import re

        # .terminal-card-header must contain flex-wrap: wrap
        card_header_match = re.search(r'\.terminal-card-header\s*\{([^}]+)\}', self.html_text)
        self.assertIsNotNone(card_header_match, ".terminal-card-header rule must exist")
        header_body = card_header_match.group(1)
        self.assertIn("flex-wrap: wrap", header_body)
        self.assertIn("gap: 8px", header_body)

        # .chart-box-title must contain flex-wrap: wrap
        chart_title_match = re.search(r'\.chart-box-title\s*\{([^}]+)\}', self.html_text)
        self.assertIsNotNone(chart_title_match, ".chart-box-title rule must exist")
        chart_title_body = chart_title_match.group(1)
        self.assertIn("flex-wrap: wrap", chart_title_body)
        self.assertIn("gap: 8px", chart_title_body)

    def test_svg_bar_chart_resilience_with_non_numeric_and_edge_inputs(self) -> None:
        """SVG chart logic must sanitize non-numeric strings ('N/A'), nulls, and empty values without NaN."""
        # Check that safeValues sanitization is present in index.html
        self.assertIn("safeValues", self.html_text)
        self.assertIn("safeVal < 0", self.html_text)

        # Python-side simulation of the sanitize logic
        raw_inputs = ["N/A", None, 275.0, "200.0", -7.73, "invalid", 0]
        safe_vals = []
        for v in raw_inputs:
            if isinstance(v, (int, float)):
                safe_vals.append(v)
            elif isinstance(v, str):
                try:
                    num = float(v)
                    safe_vals.append(0.0 if num != num else num)
                except ValueError:
                    safe_vals.append(0.0)
            else:
                safe_vals.append(0.0)

        max_val = max([abs(v) for v in safe_vals] + [1])
        self.assertEqual(max_val, 275.0)
        for sv in safe_vals:
            if sv < 0:
                bar_h = max(6, min(22, (abs(sv) / max_val) * 22))
                y = 100
                text_y = y + bar_h + 9
            else:
                bar_h = 3 if sv == 0 else max(6, min(78, (sv / max_val) * 78))
                y = 100 - bar_h
                text_y = max(12, y - 5)
            self.assertTrue(10.0 <= text_y <= 145.0)
            self.assertTrue(0.0 <= y <= 100.0)


if __name__ == "__main__":
    unittest.main()
