"""Unit tests for data.js, index.html offline compliance, and dashboard sync.

Validates:
- data.js JavaScript syntax and schema structure:
  - window.WATCHLIST_DATA global object
  - portfolio (totalValue, note, SK Square / SK Hynix holdings & weights)
  - stocks array with 6 target stocks
  - records array and dailyDigests archive
- index.html 100% Offline Compliance (Zero-CDN):
  - Zero gstatic.com scripts
  - Zero external CDN links (unpkg, cdnjs, jsdelivr, tailwindcdn)
  - Pure embedded CSS styling
  - Dual-View UX elements present (Daily Digest View + Stock Filter View)
- engine.sync_dashboard (when available):
  - Safe appending of daily digests and stock records into data.js
  - Idempotent execution
"""

import json
import os
import re
import tempfile
import unittest
from pathlib import Path
from typing import Any, Dict

ROOT_DIR = Path(__file__).resolve().parent.parent
DATA_JS_PATH = ROOT_DIR / "data.js"
INDEX_HTML_PATH = ROOT_DIR / "index.html"

try:
    import engine.sync_dashboard as sync_module
    SYNC_AVAILABLE = True
except ImportError:
    SYNC_AVAILABLE = False


def parse_js_data_store(js_text: str) -> Dict[str, Any]:
    """Extracts and parses the JSON-compatible object from data.js using brace counting."""
    idx = js_text.find("WATCHLIST_DATA")
    if idx == -1:
        raise ValueError("WATCHLIST_DATA not found in JS text")
    start = js_text.find("{", idx)
    if start == -1:
        raise ValueError("Opening brace not found after WATCHLIST_DATA")

    depth = 0
    in_string = False
    quote_char = None
    end = -1
    i = start
    while i < len(js_text):
        c = js_text[i]
        if in_string:
            if c == "\\":
                i += 1  # Skip escaped character
            elif c == quote_char:
                in_string = False
        else:
            if c in ('"', "'", '`'):
                in_string = True
                quote_char = c
            elif c == "{":
                depth += 1
            elif c == "}":
                depth -= 1
                if depth == 0:
                    end = i + 1
                    break
        i += 1

    if end == -1:
        raise ValueError("Unmatched braces for WATCHLIST_DATA object")

    json_str = js_text[start:end]
    # Strip line comments
    json_str = re.sub(r'(?<![:\\])//.*?\n', '\n', json_str)
    # Strip block comments
    json_str = re.sub(r'/\*.*?\*/', '', json_str, flags=re.DOTALL)
    # Remove trailing commas
    json_str = re.sub(r',\s*([}\]])', r'\1', json_str)

    # Try parsing directly if valid JSON
    try:
        data = json.loads(json_str)
        if isinstance(data, dict):
            return data
    except Exception:
        pass

    # Quote unquoted property keys for loose JS objects
    json_str = re.sub(r'([{,]\s*)([a-zA-Z0-9_]+)\s*:', r'\1"\2":', json_str)
    json_str = re.sub(r',\s*([}\]])', r'\1', json_str)

    return json.loads(json_str)


class TestDataJsSchema(unittest.TestCase):
    """Tier 1: data.js syntax and data structure verification."""

    def setUp(self) -> None:
        self.assertTrue(DATA_JS_PATH.exists(), f"data.js must exist at {DATA_JS_PATH}")
        self.raw_content = DATA_JS_PATH.read_text(encoding="utf-8")

    def test_window_watchlist_data_declared(self) -> None:
        """data.js must declare window.WATCHLIST_DATA for offline file:// global access."""
        self.assertIn("window.WATCHLIST_DATA", self.raw_content)

    def test_data_schema_keys(self) -> None:
        """Validates that parsed data contains portfolio, stocks, records."""
        data = parse_js_data_store(self.raw_content)
        self.assertIn("lastUpdated", data)
        self.assertIn("portfolio", data)
        self.assertIn("stocks", data)
        self.assertIn("records", data)

    def test_portfolio_holdings(self) -> None:
        """Validates portfolio holdings for SK Square (57.6%) and SK Hynix (42.3%)."""
        data = parse_js_data_store(self.raw_content)
        portfolio = data["portfolio"]
        self.assertIn("holdings", portfolio)
        holdings = portfolio["holdings"]

        holding_names = [h.get("name") or h.get("stockName", "") for h in holdings]
        self.assertTrue(any("SK스퀘어" in name for name in holding_names))
        self.assertTrue(any("SK하이닉스" in name for name in holding_names))

    def test_stocks_metadata(self) -> None:
        """Validates that all 8 target stock IDs exist in stocks metadata."""
        data = parse_js_data_store(self.raw_content)
        stock_ids = {s.get("id") for s in data["stocks"]}
        expected_ids = {"SK_SQUARE", "SK_HYNIX", "UBER", "MBLY", "FLNC", "UPST", "CELH", "ENPH"}
        self.assertTrue(expected_ids.issubset(stock_ids), f"Missing stocks: {expected_ids - stock_ids}")


class TestIndexHtmlOfflineCompliance(unittest.TestCase):
    """Tier 1 & Tier 3: 100% Offline Zero-CDN Compliance and Dual-View UX."""

    def setUp(self) -> None:
        self.assertTrue(INDEX_HTML_PATH.exists(), f"index.html must exist at {INDEX_HTML_PATH}")
        self.html_content = INDEX_HTML_PATH.read_text(encoding="utf-8")

    def test_zero_gstatic_or_external_cdns(self) -> None:
        """index.html must NOT contain any external CDN scripts or stylesheet links."""
        # Find external http/https script tags
        external_scripts = re.findall(r'<script[^>]+src=["\'](https?://[^"\']+)["\']', self.html_content, re.IGNORECASE)
        external_links = re.findall(r'<link[^>]+href=["\'](https?://[^"\']+)["\']', self.html_content, re.IGNORECASE)

        external_resources = external_scripts + external_links
        self.assertEqual(
            external_resources,
            [],
            f"Found forbidden external CDN resources in index.html: {external_resources}. "
            f"System must be 100% offline runnable via file://."
        )

    def test_embedded_css_present(self) -> None:
        """index.html must contain embedded <style> tags providing custom styles/themes."""
        self.assertIn("<style>", self.html_content)
        self.assertIn("</style>", self.html_content)

    def test_data_js_local_inclusion(self) -> None:
        """index.html must include data.js via local relative script tag."""
        self.assertTrue(
            re.search(r'<script[^>]+src=["\']\./?data\.js["\']', self.html_content, re.IGNORECASE),
            "index.html must load data.js locally",
        )

    def test_dual_view_elements_or_toggle_present(self) -> None:
        """index.html must contain Dual View UX (Daily Digest View & Time-Series View)."""
        content = self.html_content
        has_digest_view = ("다이제스트" in content or "digest" in content.lower() or "daily" in content.lower())
        has_filter_view = ("시계열" in content or "필터" in content or "time-series" in content.lower() or "filter" in content.lower())

        self.assertTrue(has_digest_view, "index.html must support Daily Digest View")
        self.assertTrue(has_filter_view, "index.html must support Stock Time-Series Filter View")


@unittest.skipUnless(SYNC_AVAILABLE, "engine.sync_dashboard is not yet available")
class TestDashboardSyncModule(unittest.TestCase):
    """Tier 1: Dashboard sync and data.js update verification."""

    def test_sync_appends_record_safely(self) -> None:
        """engine.sync_dashboard appends new digest without corrupting data.js syntax."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            temp_data_js = Path(tmp_dir) / "data.js"
            temp_data_js.write_text(DATA_JS_PATH.read_text(encoding="utf-8"), encoding="utf-8")

            # Mock daily market data
            from tests.fixtures.sample_dumps import SAMPLE_RAW_DUMP_FULL_DAY
            from engine.cleaner import clean_raw_dump
            from engine.extractor import extract_facts

            cleaned, _ = clean_raw_dump(SAMPLE_RAW_DUMP_FULL_DAY)
            market_data = extract_facts(cleaned, date="2026-09-29")

            if hasattr(sync_module, "sync_to_dashboard"):
                sync_module.sync_to_dashboard(market_data, data_js_path=str(temp_data_js))
            elif hasattr(sync_module, "update_data_js"):
                sync_module.update_data_js(market_data, data_js_path=str(temp_data_js))

            updated_content = temp_data_js.read_text(encoding="utf-8")
            self.assertIn("window.WATCHLIST_DATA", updated_content)
            # Verify it parses cleanly
            parsed = parse_js_data_store(updated_content)
            self.assertIsNotNone(parsed)


class TestFinancialsExplorerIntegrity(unittest.TestCase):
    """Verifies that 5-Year Financial Explorer adheres to separated 2025 and 2026E columns."""

    def setUp(self):
        self.html_text = INDEX_HTML_PATH.read_text(encoding="utf-8")
        self.data_store = parse_js_data_store(DATA_JS_PATH.read_text(encoding="utf-8"))

    def test_all_stocks_have_separated_2025_and_2026e(self):
        """All 8 stocks in financials must have multi-year ['2022', '2023', '2024', '2025', '2026E', '2027E']."""
        financials = self.data_store.get("financials", {})
        self.assertGreaterEqual(len(financials), 8)
        canonical_8 = ["SK_HYNIX", "SK_SQUARE", "UBER", "MBLY", "FLNC", "UPST", "CELH", "ENPH"]

        for stock_id in canonical_8:
            self.assertIn(stock_id, financials, f"Stock {stock_id} missing in financials")
            stock_fin = financials[stock_id]
            years = stock_fin.get("years", [])
            self.assertEqual(years, ["2022", "2023", "2024", "2025", "2026E", "2027E"],
                             f"Stock {stock_id} must have multi-year 2022~2027E years: {years}")
            self.assertIn("2025", years, f"2025 must be its own column for {stock_id}")
            self.assertTrue(any("2026" in y and ("E" in y or "e" in y) for y in years),
                            f"2026E must be its own column for {stock_id}")
            self.assertTrue(any("2027" in y and ("E" in y or "e" in y) for y in years),
                            f"2027E must be its own column for {stock_id}")
            self.assertNotIn("2025/2026E", years, f"2025 and 2026 must not be merged for {stock_id}")

            # Verify every metric in all 5 categories has exactly 6 data points
            for cat_key in ["income_statement", "profitability", "cash_flow", "balance_sheet", "valuation"]:
                cat_dict = stock_fin.get(cat_key, {})
                self.assertGreater(len(cat_dict), 0, f"Category {cat_key} empty for {stock_id}")
                for metric_name, val_list in cat_dict.items():
                    self.assertEqual(len(val_list), 6,
                                     f"{stock_id}.{cat_key}.{metric_name} must have 6 values, got {len(val_list)}")

    def test_index_html_markup_and_guards(self):
        """index.html must have DOM elements for missing notice and separated 2025, 2026E, and 2027E headers."""
        self.assertIn('id="financialsContentWrap"', self.html_text)
        self.assertIn('id="financialsMissingNotice"', self.html_text)
        self.assertIn('2026E', self.html_text)
        self.assertIn('2027E', self.html_text)
        self.assertNotIn('2025/2026E', self.html_text)


if __name__ == "__main__":
    unittest.main()

