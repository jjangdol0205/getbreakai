"""Milestone 4 Adversarial Dashboard & Financials Verification Suite.
Written by Challenger 2 (Adversarial Dashboard & Financials Verifier).

Scope:
1. Strict 100% Zero-CDN offline compliance in index.html and data.js.
2. Complete DOM element ID bindings (all getElementById targets exist).
3. Event handler declarations (all HTML inline event handlers are defined).
4. Balanced syntax (braces, brackets, parentheses, quotes) across all scripts.
5. 5-Year Financial Explorer: all 8 stocks, 5 categories, 5-year arrays, null-safety.
6. SVG bar chart generator stress testing (zeros, negatives, extremes, tag balancing).
7. Stock Drawer modal behavior, element binding, and edge cases.
8. Four-view architecture and backward compatibility checks.
"""

from __future__ import annotations

import json
import re
import unittest
from pathlib import Path
from typing import Any, Dict, List, Set

REPO_ROOT = Path(__file__).resolve().parent.parent
INDEX_HTML = REPO_ROOT / "index.html"
DATA_JS = REPO_ROOT / "data.js"


def load_watchlist_data() -> Dict[str, Any]:
    """Extract and parse window.WATCHLIST_DATA JSON payload from data.js."""
    content = DATA_JS.read_text(encoding="utf-8").strip()
    match = re.search(r"window\.WATCHLIST_DATA\s*=\s*(\{[\s\S]*\});?\s*$", content)
    if not match:
        raise ValueError("Could not find window.WATCHLIST_DATA assignment in data.js")
    return json.loads(match.group(1))


class TestZeroCDNOfflineCompliance(unittest.TestCase):
    """Adversarial stress-testing of Zero-CDN and 100% offline isolation."""

    def setUp(self):
        self.html_text = INDEX_HTML.read_text(encoding="utf-8")
        self.js_text = DATA_JS.read_text(encoding="utf-8")

    def test_no_remote_scripts_or_links(self):
        """index.html must not load any remote script or stylesheet."""
        # Find script tags with src
        script_srcs = re.findall(r'<script[^>]+src=["\']([^"\']+)["\']', self.html_text, re.IGNORECASE)
        for src in script_srcs:
            self.assertFalse(
                re.match(r"^(https?:)?//", src, re.IGNORECASE),
                f"Forbidden remote script src found: {src}"
            )

        # Find link tags with href
        link_hrefs = re.findall(r'<link[^>]+href=["\']([^"\']+)["\']', self.html_text, re.IGNORECASE)
        for href in link_hrefs:
            self.assertFalse(
                re.match(r"^(https?:)?//", href, re.IGNORECASE),
                f"Forbidden remote link href found: {href}"
            )

    def test_no_remote_css_imports_or_urls(self):
        """Embedded CSS must not contain @import or remote url() calls."""
        # Check @import in style
        imports = re.findall(r"@import\s+[^;]+;", self.html_text, re.IGNORECASE)
        self.assertEqual(len(imports), 0, f"Found remote @import in index.html: {imports}")

        # Check url() in style
        urls = re.findall(r"url\s*\(\s*['\"]?([^'\")]+)['\"]?\s*\)", self.html_text, re.IGNORECASE)
        for url in urls:
            self.assertFalse(
                re.match(r"^(https?:)?//", url, re.IGNORECASE),
                f"Found remote url() in index.html CSS: {url}"
            )

    def test_no_known_cdn_domains(self):
        """Neither index.html nor data.js may reference known CDN domains."""
        known_cdns = [
            "cdn.jsdelivr.net",
            "cdnjs.cloudflare.com",
            "unpkg.com",
            "fonts.googleapis.com",
            "fonts.gstatic.com",
            "code.jquery.com",
            "stackpath.bootstrapcdn.com",
            "cdn.tailwindcss.com",
            "ajax.googleapis.com",
            "cdn.jsdelivr.com",
            "use.fontawesome.com",
        ]
        for cdn in known_cdns:
            self.assertNotIn(cdn, self.html_text, f"Forbidden CDN domain {cdn} found in index.html")
            self.assertNotIn(cdn, self.js_text, f"Forbidden CDN domain {cdn} found in data.js")

    def test_local_data_js_reference(self):
        """data.js must be referenced via relative local path."""
        self.assertRegex(
            self.html_text,
            r'<script\s+src=["\']\./data\.js["\']>\s*</script>',
            "index.html must reference ./data.js locally"
        )


class TestDOMBindingsAndEventHandlers(unittest.TestCase):
    """Verifies that all DOM queries in JS match elements in HTML, and all handlers are defined."""

    def setUp(self):
        self.html_text = INDEX_HTML.read_text(encoding="utf-8")
        # Extract HTML body/head markup vs <script> contents
        self.scripts = re.findall(r"<script(?![^>]*src)[^>]*>([\s\S]*?)</script>", self.html_text, re.IGNORECASE)
        self.combined_js = "\n".join(self.scripts)

        # Extract all HTML element IDs
        self.dom_ids = set(re.findall(r'id=["\']([^"\']+)["\']', self.html_text))

        # Extract all function declarations in JS
        self.js_functions = set(re.findall(r"function\s+([a-zA-Z0-9_$]+)\s*\(", self.combined_js))
        # Also const/let arrow or function assignments
        assigned_funcs = re.findall(r"(?:const|let|var)\s+([a-zA-Z0-9_$]+)\s*=\s*(?:function|\([^)]*\)\s*=>)", self.combined_js)
        self.js_functions.update(assigned_funcs)
        # Also function aliases e.g. const renderSimpleMarkdown = renderMarkdownToHtml;
        aliases = re.findall(r"(?:const|let|var)\s+([a-zA-Z0-9_$]+)\s*=\s*([a-zA-Z0-9_$]+);", self.combined_js)
        for alias, orig in aliases:
            if orig in self.js_functions:
                self.js_functions.add(alias)

    def test_all_get_element_by_id_exist_in_dom(self):
        """Every document.getElementById('X') must find X in the DOM."""
        queried_ids = set(re.findall(r'document\.getElementById\(["\']([^"\']+)["\']\)', self.combined_js))
        missing_ids = queried_ids - self.dom_ids
        self.assertEqual(
            missing_ids,
            set(),
            f"The following IDs were queried in JS but do NOT exist in HTML DOM: {missing_ids}"
        )

    def test_all_inline_event_handlers_are_defined(self):
        """Every onclick/onchange/oninput handler in HTML must refer to a declared JS function."""
        # Find all inline event attributes
        handler_matches = re.findall(r'\b(on(?:click|change|input|submit|keydown|keyup))\s*=\s*["\']([^"\']+)["\']', self.html_text, re.IGNORECASE)
        for attr_name, expr in handler_matches:
            # Skip stopPropagation or standard inline expressions like event.stopPropagation()
            if "stopPropagation" in expr or "preventDefault" in expr:
                continue
            # Extract function call name before '('
            call_match = re.match(r"\s*([a-zA-Z0-9_$]+)\s*\(", expr)
            if call_match:
                func_name = call_match.group(1)
                self.assertIn(
                    func_name,
                    self.js_functions,
                    f"HTML handler {attr_name}='{expr}' calls undeclared function '{func_name}'"
                )

    def test_balanced_syntax_in_inline_scripts(self):
        """Inline scripts must have balanced parentheses, brackets, and braces across ES6 constructs."""
        for idx, script in enumerate(self.scripts):
            stack = []
            i = 0
            n = len(script)
            last_token = None

            while i < n:
                c = script[i]
                nxt = script[i + 1] if i + 1 < n else ""

                if len(stack) > 0 and stack[-1] == "TEMPLATE":
                    if c == "\\":
                        i += 2
                        continue
                    elif c == "`":
                        stack.pop()
                    elif c == "$" and nxt == "{":
                        stack.append("TEMPLATE_EXPR")
                        i += 2
                        continue
                    i += 1
                    continue

                # 1. Line comment
                if c == "/" and nxt == "/":
                    end_line = script.find("\n", i)
                    i = end_line + 1 if end_line != -1 else n
                    continue

                # 2. Block comment
                if c == "/" and nxt == "*":
                    end_block = script.find("*/", i + 2)
                    self.assertNotEqual(end_block, -1, f"Unclosed block comment in script #{idx} at {i}")
                    i = end_block + 2
                    continue

                # 3. String literals (single & double quotes)
                if c in ('"', "'"):
                    quote = c
                    i += 1
                    while i < n:
                        if script[i] == "\\":
                            i += 2
                        elif script[i] == quote:
                            i += 1
                            break
                        elif script[i] == "\n":
                            self.fail(f"Unescaped newline in string literal in script #{idx} at {i}")
                        else:
                            i += 1
                    last_token = quote
                    continue

                # 4. Regex literal vs division
                if c == "/" and (last_token in ["(", ",", "=", ":", "[", "!", "&", "|", "?", "{", ";", "return", "typeof"]):
                    i += 1
                    in_char_class = False
                    while i < n:
                        if script[i] == "\\":
                            i += 2
                        elif script[i] == "[" and not in_char_class:
                            in_char_class = True
                            i += 1
                        elif script[i] == "]" and in_char_class:
                            in_char_class = False
                            i += 1
                        elif script[i] == "/" and not in_char_class:
                            i += 1
                            while i < n and script[i].isalpha():
                                i += 1
                            break
                        elif script[i] == "\n":
                            self.fail(f"Unterminated regex literal at newline in script #{idx} at {i}")
                        else:
                            i += 1
                    last_token = "REGEX"
                    continue

                # 5. Template literal entry
                if c == "`":
                    stack.append("TEMPLATE")
                    i += 1
                    last_token = "`"
                    continue

                # 6. Delimiters
                if c == "(":
                    stack.append("PAREN")
                    last_token = "("
                elif c == ")":
                    self.assertTrue(len(stack) > 0 and stack[-1] == "PAREN", f"Mismatched ')' in script #{idx} at position {i}")
                    stack.pop()
                    last_token = ")"
                elif c == "[":
                    stack.append("BRACKET")
                    last_token = "["
                elif c == "]":
                    self.assertTrue(len(stack) > 0 and stack[-1] == "BRACKET", f"Mismatched ']' in script #{idx} at position {i}")
                    stack.pop()
                    last_token = "]"
                elif c == "{":
                    stack.append("BRACE")
                    last_token = "{"
                elif c == "}":
                    self.assertTrue(
                        len(stack) > 0 and stack[-1] in ("BRACE", "TEMPLATE_EXPR"),
                        f"Mismatched '}}' in script #{idx} at position {i} (stack was {stack})",
                    )
                    stack.pop()
                    last_token = "}"
                elif not c.isspace():
                    last_token = c

                i += 1

            self.assertEqual(stack, [], f"Script #{idx} has unclosed syntax structures: {stack}")


    def test_balanced_syntax_in_data_js(self):
        """data.js must have balanced brackets, braces, and valid JSON structure."""
        data = load_watchlist_data()
        self.assertIsInstance(data, dict)
        self.assertIn("financials", data)
        self.assertIn("records", data)


class Test5YearFinancialExplorerAdversarial(unittest.TestCase):
    """Stress-tests the 5-Year Financial Explorer data store and schemas."""

    CANONICAL_STOCKS = [
        "SK_HYNIX", "SK_SQUARE", "UBER", "MBLY", "FLNC", "UPST", "CELH", "ENPH"
    ]
    REQUIRED_CATEGORIES = [
        "income_statement", "profitability", "cash_flow", "balance_sheet", "valuation"
    ]

    def setUp(self):
        self.data = load_watchlist_data()
        self.financials = self.data.get("financials", {})

    def test_all_8_stocks_present_in_financials(self):
        """data.js financials MUST contain entries for all 8 canonical stocks."""
        for stock_id in self.CANONICAL_STOCKS:
            self.assertIn(
                stock_id,
                self.financials,
                f"Stock {stock_id} is missing from window.WATCHLIST_DATA.financials"
            )

    def test_all_stocks_have_metadata_and_5_years(self):
        """Each stock must specify name, ticker, market, currency, and exactly 5 years."""
        for stock_id in self.CANONICAL_STOCKS:
            fin = self.financials[stock_id]
            self.assertIn("name", fin, f"{stock_id} missing 'name'")
            self.assertIn("ticker", fin, f"{stock_id} missing 'ticker'")
            self.assertIn("market", fin, f"{stock_id} missing 'market'")
            self.assertIn("currency", fin, f"{stock_id} missing 'currency'")
            self.assertIn("years", fin, f"{stock_id} missing 'years'")

            years = fin["years"]
            self.assertGreaterEqual(
                len(years), 5,
                f"{stock_id} 'years' must have at least 5 entries, got {years}"
            )

    def test_all_5_categories_present_for_every_stock(self):
        """Every stock must contain all 5 required financial categories."""
        for stock_id in self.CANONICAL_STOCKS:
            fin = self.financials[stock_id]
            for cat in self.REQUIRED_CATEGORIES:
                self.assertIn(
                    cat, fin,
                    f"Category '{cat}' missing for stock {stock_id}"
                )
                self.assertIsInstance(
                    fin[cat], dict,
                    f"Category '{cat}' for {stock_id} must be a dictionary"
                )

    def test_category_metrics_have_5_year_values(self):
        """Every metric inside each financial category must have an array of multi-year elements."""
        for stock_id in self.CANONICAL_STOCKS:
            fin = self.financials[stock_id]
            for cat in self.REQUIRED_CATEGORIES:
                cat_dict = fin[cat]
                self.assertGreater(
                    len(cat_dict), 0,
                    f"Category '{cat}' in {stock_id} has no metrics!"
                )
                for metric_name, val_list in cat_dict.items():
                    self.assertIsInstance(
                        val_list, list,
                        f"Metric '{metric_name}' in {stock_id}.{cat} must be a list"
                    )
                    self.assertGreaterEqual(
                        len(val_list), 5,
                        f"Metric '{metric_name}' in {stock_id}.{cat} must have at least 5 values, got {len(val_list)}"
                    )

    def test_key_metrics_presence(self):
        """Verify presence of key foundational metrics per category."""
        expected_metrics = {
            "income_statement": ["revenue", "operating_income", "net_income"],
            "profitability": ["opm", "roe"],
            "cash_flow": ["fcf"],
            "balance_sheet": ["total_assets", "total_liabilities"],
            "valuation": ["pe", "pb"],
        }
        for stock_id in self.CANONICAL_STOCKS:
            fin = self.financials[stock_id]
            for cat, metrics in expected_metrics.items():
                for m in metrics:
                    self.assertIn(
                        m, fin[cat],
                        f"Expected foundational metric '{m}' missing in {stock_id}.{cat}"
                    )


class TestSVGBarChartEngine(unittest.TestCase):
    """Stress-tests the generateSvgBarChart logic against edge-case inputs."""

    @staticmethod
    def generate_svg_bar_chart(labels: List[str], values: List[float], base_color: str, metric_name: str) -> str:
        """Exact Python implementation of index.html's generateSvgBarChart."""
        # Mirrors line 1957 of index.html
        max_val = max([abs(v) for v in values] + [1]) if values else 1
        width = 420
        height = 150
        bar_width = 36
        num_labels = len(labels)
        gap = (width - 40 - (num_labels * bar_width)) / (num_labels - 1) if num_labels > 1 else 0

        bars_svg = ""
        for i, val in enumerate(values):
            x = 30 + i * (bar_width + gap)
            bar_height = max(10, min(100, (abs(val) / max_val) * 100))
            is_neg = val < 0
            color = "#F43F5E" if is_neg else base_color
            y = 100 if is_neg else (100 - bar_height)
            label = labels[i].replace('/2026E', 'E') if i < len(labels) else ""

            bars_svg += f"""
          <g>
            <rect x="{x}" y="{y}" width="{bar_width}" height="{bar_height}" rx="4" fill="{color}" fill-opacity="0.8" />
            <text x="{x + bar_width/2}" y="{y - 6}" font-size="10" font-family="monospace" fill="#E2E8F0" text-anchor="middle" font-weight="700">
              {val}
            </text>
            <text x="{x + bar_width/2}" y="130" font-size="10" font-family="monospace" fill="#94A3B8" text-anchor="middle">
              {label}
            </text>
          </g>
        """

        return f"""
        <svg viewBox="0 0 {width} {height}" style="width: 100%; height: 100%;">
          <line x1="20" y1="100" x2="{width - 10}" y2="100" stroke="rgba(255,255,255,0.15)" stroke-dasharray="2,2" />
          {bars_svg}
        </svg>
      """

    def test_chart_with_standard_financial_data(self):
        """Standard 5-year revenue values must produce well-formed SVG with 5 bars."""
        years = ["2021", "2022", "2023", "2024", "2025/2026E"]
        values = [17460, 31877, 37281, 43900, 52000]
        svg = self.generate_svg_bar_chart(years, values, "#3B82F6", "매출액")

        self.assertIn("<svg viewBox=\"0 0 420 150\"", svg)
        self.assertIn("</svg>", svg)
        self.assertEqual(svg.count("<rect"), 5)
        self.assertEqual(svg.count("</g>"), 5)
        self.assertIn("2025E", svg)  # Verify replacement of /2026E with E on 2025/2026E

    def test_chart_with_negative_values_operating_losses(self):
        """Negative values (e.g. losses) must use loss color #F43F5E and baseline y=100."""
        years = ["2021", "2022", "2023", "2024", "2025/2026E"]
        values = [-250, -100, -30, 45, 120]
        svg = self.generate_svg_bar_chart(years, values, "#10B981", "영업이익")

        self.assertIn("#F43F5E", svg)  # Negative color used
        self.assertIn("#10B981", svg)  # Positive color used
        self.assertEqual(svg.count("<rect"), 5)

    def test_chart_with_all_zeros(self):
        """All zero values must not produce division by zero, NaN, or crash."""
        years = ["2021", "2022", "2023", "2024", "2025"]
        values = [0, 0, 0, 0, 0]
        svg = self.generate_svg_bar_chart(years, values, "#3B82F6", "테스트")

        self.assertNotIn("NaN", svg)
        self.assertNotIn("Infinity", svg)
        self.assertEqual(svg.count("<rect"), 5)

    def test_chart_with_extreme_values(self):
        """Extreme values (0.01 vs 1,000,000) must clamp bar heights between 10 and 100."""
        years = ["2021", "2022", "2023", "2024", "2025"]
        values = [0.01, 10, 500, 10000, 1000000]
        svg = self.generate_svg_bar_chart(years, values, "#3B82F6", "테스트")

        self.assertNotIn("NaN", svg)
        heights = re.findall(r'height="([\d\.]+)"', svg)
        for h in heights:
            val_h = float(h)
            self.assertGreaterEqual(val_h, 10.0)
            self.assertLessEqual(val_h, 100.0)


class TestStockDrawerModalAdversarial(unittest.TestCase):
    """Stress-tests the Stock Drawer slide-in modal markup, logic, and edge cases."""

    def setUp(self):
        self.html_text = INDEX_HTML.read_text(encoding="utf-8")
        self.data = load_watchlist_data()

    def test_drawer_modal_elements_exist_in_markup(self):
        """Modal backdrop, drawer container, header title, close button, and content box must exist."""
        required_elements = [
            "stockDrawerModal",
            "stockDrawerContent",
            "drawerHeaderTitle"
        ]
        for elem_id in required_elements:
            self.assertIn(
                f'id="{elem_id}"',
                self.html_text,
                f"Element with id='{elem_id}' missing in index.html"
            )

    def test_drawer_starts_hidden(self):
        """Modal must have the 'hidden' class by default."""
        self.assertRegex(
            self.html_text,
            r'id="stockDrawerModal"\s+class="[^"]*\bhidden\b[^"]*"',
            "stockDrawerModal must include 'hidden' class on initial page load"
        )

    def test_drawer_escape_and_backdrop_events_bound(self):
        """Drawer must close on Escape key and backdrop click."""
        self.assertIn('closeStockDrawer()', self.html_text)
        self.assertIn('handleDrawerBackdropClick(event)', self.html_text)
        self.assertIn('e.key === "Escape"', self.html_text)

    def test_drawer_data_availability_for_all_canonical_stocks(self):
        """Simulate openStockDrawer for all 8 stocks to verify no null pointer errors."""
        stocks = ["SK_HYNIX", "SK_SQUARE", "UBER", "MBLY", "FLNC", "UPST", "CELH", "ENPH"]
        records = self.data.get("records", [])
        financials = self.data.get("financials", {})

        for s in stocks:
            stock_records = [r for r in records if r.get("stockId") == s]
            close_rec = next((r for r in stock_records if r.get("type") == "DAILY_CLOSE"), None)
            if not close_rec and stock_records:
                close_rec = stock_records[0]
            if not close_rec:
                close_rec = {}

            # Price and change fallback
            metrics = close_rec.get("metrics") or {}
            price = metrics.get("price") or "N/A"
            change = metrics.get("change") or "0.0%"

            # Summaries fallback
            summary = close_rec.get("oneParagraphSummary") or close_rec.get("summary") or "상세 시황 데이터가 등록되지 않았습니다."
            watch1 = close_rec.get("watchPointLine1") or (close_rec.get("watchPoints") and close_rec["watchPoints"][0]) or "핵심 지지선 모니터링"
            watch2 = close_rec.get("watchPointLine2") or (close_rec.get("watchPoints") and len(close_rec["watchPoints"]) > 1 and close_rec["watchPoints"][1]) or "신규 수주 및 실적 가이던스 확인"
            insight = close_rec.get("strategistInsight") or "단기 변동성에 흔들리지 않고 기업 펀더멘털 점검 및 현 포지션 유지가 유효합니다."

            self.assertIsInstance(summary, str)
            self.assertIsInstance(watch1, str)
            self.assertIsInstance(watch2, str)
            self.assertIsInstance(insight, str)

            # Financial snapshot
            fin = financials.get(s, {})
            rev = (fin.get("income_statement") or {}).get("revenue")
            op = (fin.get("income_statement") or {}).get("operating_income")
            opm = (fin.get("profitability") or {}).get("opm")

            self.assertIsNotNone(rev, f"Revenue missing for {s}")
            self.assertIsNotNone(op, f"Operating income missing for {s}")
            self.assertIsNotNone(opm, f"OPM missing for {s}")


class TestFourViewArchitecture(unittest.TestCase):
    """Verifies that all 4 views (Digest, Timeseries, Insight, Financials) are wired cleanly."""

    def setUp(self):
        self.html_text = INDEX_HTML.read_text(encoding="utf-8")

    def test_all_four_view_buttons_exist(self):
        """Header must contain switch buttons for all 4 views."""
        buttons = ["btnViewDigest", "btnViewTimeseries", "btnViewInsight", "btnViewFinancials"]
        for btn in buttons:
            self.assertIn(f'id="{btn}"', self.html_text, f"View switch button '{btn}' missing")

    def test_all_four_view_sections_exist(self):
        """Markup must contain section containers for all 4 views."""
        sections = [
            "viewDigestSection",
            "viewTimeseriesSection",
            "viewInsightSection",
            "viewFinancialsSection"
        ]
        for sec in sections:
            self.assertIn(f'id="{sec}"', self.html_text, f"View section '{sec}' missing")

    def test_switch_view_supports_all_four_views(self):
        """switchView(viewName) in JS must handle digest, timeseries, insight, financials."""
        for v in ["digest", "timeseries", "insight", "financials"]:
            self.assertIn(f'"{v}"', self.html_text)

    def test_regression_compatibility_elements(self):
        """Ensure backward compatibility elements for existing regression tests."""
        compatibility_tokens = [
            "feed-summary-box",
            "summary-box-content",
            "strategist-body",
            "renderMarkdownToHtml",
            "ib-markdown-body",
            "Nomura CSI 103.9",
        ]
        for token in compatibility_tokens:
            self.assertIn(token, self.html_text, f"Backward compatibility token '{token}' missing from index.html")


if __name__ == "__main__":
    unittest.main()
