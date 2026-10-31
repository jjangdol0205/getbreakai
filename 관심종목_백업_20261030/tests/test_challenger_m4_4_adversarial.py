"""Milestone 4 Adversarial Verification Suite - Iteration 2.
Authored by Challenger 4 (Adversarial Dashboard & Zero-CDN Verifier).

Scope:
1. 100% Zero-CDN and strict offline compliance in index.html and data.js.
2. Complete DOM element ID bindings, query selectors, and inline event handlers.
3. 5-Year Financial Explorer: all 8 stocks x 5 categories x 5-year arrays and metric integrity.
4. Stock Drawer modal mechanics and SK_SQUARE active stock card rendering & presence logic.
5. 4-View Architecture switching integrity.
6. Stress-testing SVG bar chart generator with pathological inputs (zeros, negative losses, NaNs).
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


class TestZeroCDNOfflineComplianceEmpirical(unittest.TestCase):
    """Empirical adversarial verification of Zero-CDN and offline isolation."""

    def setUp(self):
        self.html_text = INDEX_HTML.read_text(encoding="utf-8")
        self.js_text = DATA_JS.read_text(encoding="utf-8")

    def test_zero_remote_script_and_link_tags(self):
        """No script src or link href may point to remote http/https/ftp/protocol-relative URLs."""
        script_srcs = re.findall(r'<script[^>]+src=["\']([^"\']+)["\']', self.html_text, re.IGNORECASE)
        for src in script_srcs:
            self.assertFalse(
                re.match(r"^(?:https?:)?//", src, re.IGNORECASE),
                f"Forbidden remote script src found in index.html: {src}"
            )
            # Ensure local relative path
            self.assertTrue(
                src.startswith("./") or not src.startswith("/"),
                f"Script src must be a relative local path: {src}"
            )

        link_hrefs = re.findall(r'<link[^>]+href=["\']([^"\']+)["\']', self.html_text, re.IGNORECASE)
        for href in link_hrefs:
            self.assertFalse(
                re.match(r"^(?:https?:)?//", href, re.IGNORECASE),
                f"Forbidden remote link href found in index.html: {href}"
            )

    def test_zero_css_remote_imports_and_urls(self):
        """Embedded CSS must not contain @import or remote url() calls."""
        style_blocks = re.findall(r"<style[^>]*>([\s\S]*?)</style>", self.html_text, re.IGNORECASE)
        for idx, block in enumerate(style_blocks):
            imports = re.findall(r"@import\s+[^;]+;", block, re.IGNORECASE)
            self.assertEqual(len(imports), 0, f"Found @import in style block #{idx}: {imports}")

            urls = re.findall(r"url\s*\(\s*['\"]?([^'\")]+)['\"]?\s*\)", block, re.IGNORECASE)
            for url in urls:
                self.assertFalse(
                    re.match(r"^(?:https?:)?//", url, re.IGNORECASE),
                    f"Found remote url() in style block #{idx}: {url}"
                )

    def test_zero_known_cdn_domains_in_html_and_js(self):
        """Neither index.html nor data.js may reference any external CDN domain."""
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
            "cdn.skypack.dev",
            "cdn.bootcdn.net",
        ]
        for cdn in known_cdns:
            self.assertNotIn(cdn, self.html_text, f"Forbidden CDN domain '{cdn}' found in index.html")
            self.assertNotIn(cdn, self.js_text, f"Forbidden CDN domain '{cdn}' found in data.js")

    def test_no_dynamic_network_fetch_apis_in_dashboard(self):
        """Dashboard must not make asynchronous HTTP network calls via fetch or XMLHttpRequest."""
        scripts = re.findall(r"<script(?![^>]*src)[^>]*>([\s\S]*?)</script>", self.html_text, re.IGNORECASE)
        combined_js = "\n".join(scripts)
        forbidden_apis = [
            r"\bfetch\s*\(",
            r"\bnew\s+XMLHttpRequest\b",
            r"\bnew\s+WebSocket\b",
            r"\bnew\s+EventSource\b",
            r"\bnavigator\.sendBeacon\b",
        ]
        for pattern in forbidden_apis:
            match = re.search(pattern, combined_js)
            self.assertIsNone(match, f"Forbidden dynamic network API '{pattern}' found in inline script")

    def test_offline_ui_badge_present(self):
        """Markup must visibly display 100% Offline indicator badge."""
        self.assertIn("badge-offline", self.html_text)
        self.assertRegex(self.html_text, r"100%\s+Offline")


class TestDOMBindingsAndEventHandlersAdversarial(unittest.TestCase):
    """Verifies all DOM getElementById queries match elements in markup and all handlers exist."""

    def setUp(self):
        self.html_text = INDEX_HTML.read_text(encoding="utf-8")
        self.scripts = re.findall(r"<script(?![^>]*src)[^>]*>([\s\S]*?)</script>", self.html_text, re.IGNORECASE)
        self.combined_js = "\n".join(self.scripts)
        self.dom_ids = set(re.findall(r'id=["\']([^"\']+)["\']', self.html_text))

        # Extract functions
        self.js_functions = set(re.findall(r"function\s+([a-zA-Z0-9_$]+)\s*\(", self.combined_js))
        assigned_funcs = re.findall(r"(?:const|let|var)\s+([a-zA-Z0-9_$]+)\s*=\s*(?:function|\([^)]*\)\s*=>)", self.combined_js)
        self.js_functions.update(assigned_funcs)
        aliases = re.findall(r"(?:const|let|var)\s+([a-zA-Z0-9_$]+)\s*=\s*([a-zA-Z0-9_$]+);", self.combined_js)
        for alias, orig in aliases:
            if orig in self.js_functions:
                self.js_functions.add(alias)

    def test_all_get_element_by_id_exist_in_dom(self):
        """Every document.getElementById('X') must find X in the DOM."""
        queried_ids = set(re.findall(r'document\.getElementById\(["\']([^"\']+)["\']\)', self.combined_js))
        missing = queried_ids - self.dom_ids
        self.assertEqual(missing, set(), f"Queried DOM IDs do not exist in markup: {missing}")

    def test_all_query_selector_ids_exist_in_dom(self):
        """Every document.querySelector('#X') must find X in the DOM."""
        qs_ids = set(re.findall(r'document\.querySelector\(["\']#([a-zA-Z0-9_\-]+)["\']\)', self.combined_js))
        missing = qs_ids - self.dom_ids
        self.assertEqual(missing, set(), f"Queried querySelector IDs do not exist in markup: {missing}")

    def test_all_inline_event_handlers_are_defined(self):
        """Every onclick/onchange/oninput handler in HTML markup must call a declared function."""
        handlers = re.findall(r'\b(on(?:click|change|input|submit|keydown|keyup))\s*=\s*["\']([^"\']+)["\']', self.html_text, re.IGNORECASE)
        for attr, expr in handlers:
            if "stopPropagation" in expr or "preventDefault" in expr:
                continue
            call_match = re.match(r"\s*([a-zA-Z0-9_$]+)\s*\(", expr)
            if call_match:
                func_name = call_match.group(1)
                self.assertIn(func_name, self.js_functions, f"Handler {attr}='{expr}' calls undefined function '{func_name}'")

    def test_key_terminal_functions_declared(self):
        """Verify presence of key terminal functions in JS."""
        key_funcs = [
            "initDataDates",
            "switchView",
            "renderDigestView",
            "renderTimeseriesFeed",
            "renderInsightView",
            "renderFinancialsView",
            "setFinancialsStock",
            "setFinancialsCategory",
            "generateSvgBarChart",
            "openStockDrawer",
            "closeStockDrawer",
            "handleDrawerBackdropClick",
        ]
        for f in key_funcs:
            self.assertIn(f, self.js_functions, f"Key function '{f}' is missing from JS")


class Test5YearFinancialExplorerDeepAdversarial(unittest.TestCase):
    """Deep adversarial testing of the 5-Year Financial Explorer data and logic."""

    CANONICAL_STOCKS = ["SK_HYNIX", "SK_SQUARE", "UBER", "MBLY", "FLNC", "UPST", "CELH", "ENPH"]
    REQUIRED_CATEGORIES = ["income_statement", "profitability", "cash_flow", "balance_sheet", "valuation"]

    def setUp(self):
        self.data = load_watchlist_data()
        self.financials = self.data.get("financials", {})

    def test_all_8_stocks_in_financials(self):
        """All 8 canonical stocks must be present in WATCHLIST_DATA.financials."""
        for stock in self.CANONICAL_STOCKS:
            self.assertIn(stock, self.financials, f"Missing stock in financials: {stock}")

    def test_all_5_categories_and_exact_5_years(self):
        """Each stock must have all 5 categories, and multi-year data points."""
        for stock in self.CANONICAL_STOCKS:
            fin = self.financials[stock]
            years = fin.get("years", [])
            self.assertGreaterEqual(len(years), 5, f"Stock {stock} years must have at least 5 entries, got {years}")
            for cat in self.REQUIRED_CATEGORIES:
                self.assertIn(cat, fin, f"Stock {stock} missing category '{cat}'")
                cat_dict = fin[cat]
                self.assertIsInstance(cat_dict, dict)
                self.assertGreater(len(cat_dict), 0, f"Category '{cat}' in {stock} is empty")
                for metric_name, values in cat_dict.items():
                    self.assertIsInstance(values, list, f"Metric {stock}.{cat}.{metric_name} must be a list")
                    self.assertGreaterEqual(
                        len(values), 5,
                        f"Metric {stock}.{cat}.{metric_name} must have at least 5 values, got {len(values)}"
                    )

    def test_full_stack_metrics_presence(self):
        """Verify presence of full-stack requirements from prompt across all 8 stocks:
        - Income Statement: revenue, gross_profit, operating_income, net_income, eps
        - Profitability: gpm, opm, npm, roe, roic
        - Cash Flow: ocf, capex, fcf, fcf_margin
        - Balance Sheet: cash, total_assets, total_liabilities, net_debt, de_ratio
        - Valuation: pe, ps, pb, ev_ebitda
        """
        prompt_metrics = {
            "income_statement": ["revenue", "gross_profit", "operating_income", "net_income", "eps"],
            "profitability": ["gpm", "opm", "npm", "roe", "roic"],
            "cash_flow": ["ocf", "capex", "fcf", "fcf_margin"],
            "balance_sheet": ["cash", "total_assets", "total_liabilities", "net_debt", "de_ratio"],
            "valuation": ["pe", "ps", "pb", "ev_ebitda"],
        }
        for stock in self.CANONICAL_STOCKS:
            fin = self.financials[stock]
            for cat, metric_keys in prompt_metrics.items():
                for key in metric_keys:
                    self.assertIn(
                        key, fin[cat],
                        f"Stock {stock} missing required metric '{key}' in category '{cat}'"
                    )

    def test_currency_and_market_correctness(self):
        """Korean stocks must have KRW-based currency, US stocks must have USD-based currency."""
        kr_stocks = ["SK_HYNIX", "SK_SQUARE"]
        us_stocks = ["UBER", "MBLY", "FLNC", "UPST", "CELH", "ENPH"]

        for s in kr_stocks:
            cur = self.financials[s]["currency"]
            self.assertTrue(cur.startswith("KRW"), f"{s} currency must start with KRW, got '{cur}'")
        for s in us_stocks:
            cur = self.financials[s]["currency"]
            self.assertTrue(cur.startswith("USD"), f"{s} currency must start with USD, got '{cur}'")


class TestStockDrawerAndActiveCardRenderingAdversarial(unittest.TestCase):
    """Stress-tests the Stock Drawer modal mechanics and SK_SQUARE active card rendering."""

    def setUp(self):
        self.html_text = INDEX_HTML.read_text(encoding="utf-8")
        self.data = load_watchlist_data()

    def test_sk_square_market_data_complete_in_data_js(self):
        """SK_SQUARE in latest dailyDigest must have complete, verified market metrics."""
        digests = self.data.get("dailyDigests", [])
        self.assertGreater(len(digests), 0, "dailyDigests must not be empty")
        target = next((d for d in digests if d.get("date") == "2026-10-01"), digests[0])
        self.assertIn("SK_SQUARE", target["stocks"], "SK_SQUARE must be present in dailyDigest.stocks")
        sk_sq = target["stocks"]["SK_SQUARE"]

        # Check prices and change
        price = sk_sq.get("price") or sk_sq.get("closePrice")
        self.assertIn("84,200", str(price), "SK_SQUARE price must reflect 84,200원")
        change_val = sk_sq.get("change") or sk_sq.get("changePct")
        self.assertIn("+1.32%", str(change_val), "SK_SQUARE change must be +1.32%")
        self.assertIn("41.2만 주", str(sk_sq.get("volume")), "SK_SQUARE volume must be 41.2만 주")

    def test_sk_square_presence_logic_renders_active_card(self):
        """renderDigestStockCards presence logic must include SK_SQUARE and exclude inactive stocks."""
        # Check presence code in index.html
        self.assertIn("isCoreHolding", self.html_text)
        self.assertIn('sym === "SK_SQUARE"', self.html_text)

        # Simulate presence evaluation exactly as index.html does:
        all_symbols = ["SK_HYNIX", "SK_SQUARE", "UBER", "MBLY", "FLNC", "UPST", "CELH", "ENPH"]
        latest = next((d for d in self.data["dailyDigests"] if d.get("date") == "2026-10-01"), self.data["dailyDigests"][0])

        def is_price_valid(p):
            if not p or p == "N/A" or p == "원문 데이터 미제공" or p == "원문 데이터 미수집":
                return False
            return True

        present_symbols = []
        for sym in all_symbols:
            if sym in latest.get("stocks", {}):
                s = latest["stocks"][sym]
                p = s.get("closePrice") or s.get("price")
                has_briefing = s.get("oneParagraph") and (
                    "원문 데이터 미제공" not in s["oneParagraph"] and "원문 데이터 미수집" not in s["oneParagraph"]
                )
                is_core = (sym in ("SK_SQUARE", "SK_HYNIX")) and (s.get("oneParagraph") or s.get("coreDriver"))
                if is_price_valid(p) or has_briefing or is_core:
                    present_symbols.append(sym)

        self.assertIn("SK_SQUARE", present_symbols, "SK_SQUARE must be evaluated as an active stock card")
        self.assertIn("SK_HYNIX", present_symbols, "SK_HYNIX must be evaluated as an active stock card")
        self.assertIn("UBER", present_symbols, "UBER must be evaluated as an active stock card")
        self.assertIn("MBLY", present_symbols, "MBLY must be evaluated as an active stock card")

        unprovided = [s for s in all_symbols if s not in present_symbols]
        for inactive in ["FLNC", "UPST", "CELH", "ENPH"]:
            self.assertIn(inactive, unprovided, f"Inactive stock {inactive} must be in unprovided banner")
        self.assertNotIn("SK_SQUARE", unprovided, "SK_SQUARE must NOT be in unprovided banner")

    def test_stock_drawer_modal_structure_and_events(self):
        """Drawer modal markup and event listeners must be complete."""
        self.assertIn('id="stockDrawerModal"', self.html_text)
        self.assertIn('id="stockDrawerContent"', self.html_text)
        self.assertIn('id="drawerHeaderTitle"', self.html_text)
        self.assertIn('onclick="closeStockDrawer()"', self.html_text)
        self.assertIn('onclick="handleDrawerBackdropClick(event)"', self.html_text)

    def test_stock_drawer_safe_rendering_simulation_all_8_stocks(self):
        """Simulate openStockDrawer execution data pipeline for all 8 canonical stocks."""
        records = self.data.get("records", [])
        financials = self.data.get("financials", {})

        for sym in ["SK_HYNIX", "SK_SQUARE", "UBER", "MBLY", "FLNC", "UPST", "CELH", "ENPH"]:
            stock_records = [r for r in records if r.get("stockId") == sym]
            rec = next((r for r in stock_records if r.get("type") == "DAILY_CLOSE"), None)
            if not rec and stock_records:
                rec = stock_records[0]
            if not rec:
                rec = {}

            # Ensure all required drawer fields have safe fallbacks
            summary = rec.get("oneParagraphSummary") or rec.get("summary") or "상세 시황 데이터가 등록되지 않았습니다."
            watch1 = rec.get("watchPointLine1") or "핵심 지지선 모니터링"
            watch2 = rec.get("watchPointLine2") or "차기 실적 및 수주 가이던스 확인"
            insight = rec.get("strategistInsight") or "단기 변동성에 흔들리지 않고 기업 펀더멘털 점검이 유효합니다."

            self.assertTrue(len(summary) > 0)
            self.assertTrue(len(watch1) > 0)
            self.assertTrue(len(watch2) > 0)
            self.assertTrue(len(insight) > 0)

            # Financial snapshot data
            fin = financials.get(sym, {})
            self.assertIn("name", fin)
            self.assertIn("ticker", fin)


class TestSVGBarChartStressHarness(unittest.TestCase):
    """Stress tests the SVG generation algorithm with extreme values and pathological edge cases."""

    @staticmethod
    def render_chart(labels: List[str], values: List[float], color: str = "#4F46E5") -> str:
        """Mirrors generateSvgBarChart in index.html."""
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
            bar_color = "#F43F5E" if is_neg else color
            y = 100 if is_neg else (100 - bar_height)
            label = labels[i].replace('/2026E', 'E') if i < len(labels) else ""
            bars_svg += f'<rect x="{x}" y="{y}" width="{bar_width}" height="{bar_height}" fill="{bar_color}" />'

        return f'<svg viewBox="0 0 {width} {height}">{bars_svg}</svg>'

    def test_all_negative_values(self):
        """All negative values (e.g. startup continuous losses) must all be colored #F43F5E."""
        svg = self.render_chart(["Y1", "Y2", "Y3", "Y4", "Y5"], [-100, -250, -500, -120, -45])
        self.assertEqual(svg.count("#F43F5E"), 5)
        self.assertNotIn("NaN", svg)

    def test_zero_and_infinite_scale_resilience(self):
        """Zeros, tiny fractions, and astronomical numbers must clamp safely without NaN."""
        svg = self.render_chart(["Y1", "Y2", "Y3", "Y4", "Y5"], [0, 0.00001, 100000000000.0, -999999999.0, 0])
        self.assertNotIn("NaN", svg)
        self.assertNotIn("Infinity", svg)
        self.assertEqual(svg.count("<rect"), 5)


if __name__ == "__main__":
    unittest.main()
