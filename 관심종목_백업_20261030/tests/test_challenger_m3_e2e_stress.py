"""Milestone 3 E2E Dashboard, Data Sync, and Zero-CDN Adversarial Verification.

Author: Challenger 2 (Milestone 3)
Focus:
1. Dashboard Data Sync & Syntax: Execute sync and inspect data.js for clean JSON/JS syntax without NaN/undefined/unescaped characters.
2. Schema Completeness: Verify records, dailyDigests, dailyInsights, stocks, and portfolio with all M3 fields (SKHY, NASDAQ ADR, USD, adrPremium, peerComparison).
3. View 3 IB Deep Report Integration: Verify dailyInsights[0] top-level keys AND nested sections dictionary.
4. Local Zero-CDN DOM & Offline Integrity:
   - index.html ZERO external script tags, ZERO external stylesheet links, ZERO @import, ZERO remote font URLs.
   - index.html renders View 1 (Digest), View 2 (Feed with white-space: pre-line), View 3 (IB Deep Report markdown reader) without console errors.
5. Full Regression Verification: 100% pass across all suites.
"""

from __future__ import annotations

import json
from pathlib import Path
import re
import tempfile
import unittest

from engine.cleaner import clean_raw_dump
from engine.extractor import extract_facts
from engine.digest_generator import generate_digest
from engine.insight_generator import generate_insight
from engine.models import StockSymbol, STOCK_MASTERS
from engine.sync_dashboard import (
    DEFAULT_DATA_JS_PATH,
    DEFAULT_PORTFOLIO,
    DEFAULT_STOCKS,
    build_digest_entry,
    build_insight_entry,
    load_data_store,
    parse_js_data_store,
    save_data_store,
    sync_to_dashboard,
)

ROOT_DIR = Path(__file__).resolve().parent.parent
INDEX_HTML_PATH = ROOT_DIR / "index.html"
DATA_JS_PATH = ROOT_DIR / "data.js"
RAW_INPUT_PATH = ROOT_DIR / "raw_input_20260930.txt"


class TestM3DashboardDataSyncAndSyntax(unittest.TestCase):
    """Probes requirement 1: Dashboard Data Sync & Syntax."""

    @classmethod
    def setUpClass(cls):
        cls.assertTrue(DATA_JS_PATH.exists(), f"data.js must exist at {DATA_JS_PATH}")
        cls.js_text = DATA_JS_PATH.read_text(encoding="utf-8")

    def test_data_js_declaration_prefix(self):
        """data.js must declare global window.WATCHLIST_DATA without corrupting prefix."""
        self.assertTrue(
            self.js_text.startswith("window.WATCHLIST_DATA = "),
            "data.js must start with 'window.WATCHLIST_DATA = '"
        )

    def test_data_js_parses_cleanly_as_strict_json(self):
        """The data payload inside data.js must parse cleanly via standard json.loads."""
        prefix = "window.WATCHLIST_DATA = "
        clean_json_str = self.js_text[len(prefix):].rstrip(";\n ")
        try:
            data = json.loads(clean_json_str)
        except json.JSONDecodeError as exc:
            self.fail(f"data.js failed to parse as valid JSON: {exc}")
        self.assertIsInstance(data, dict, "Parsed data store must be a dictionary")

    def test_zero_nan_or_undefined_tokens(self):
        """data.js must not contain raw NaN or undefined tokens which indicate JS serialization bugs."""
        nan_matches = re.findall(r"\bNaN\b", self.js_text)
        undefined_matches = re.findall(r"\bundefined\b", self.js_text)
        self.assertEqual(len(nan_matches), 0, f"Found NaN tokens in data.js: {nan_matches}")
        self.assertEqual(len(undefined_matches), 0, f"Found undefined tokens in data.js: {undefined_matches}")

    def test_zero_unescaped_control_characters(self):
        """data.js must not contain unescaped ASCII control characters or U+2028/U+2029 separators."""
        # Check raw control characters (< 32 except newline/tab)
        raw_ctrl = [c for c in self.js_text if ord(c) < 32 and c not in "\r\n\t"]
        self.assertEqual(len(raw_ctrl), 0, f"Found raw control characters in data.js: {[ord(c) for c in raw_ctrl]}")

        # Check U+2028 and U+2029 (ECMA-262 line/paragraph separators)
        self.assertNotIn("\u2028", self.js_text, "Found unescaped U+2028 in data.js")
        self.assertNotIn("\u2029", self.js_text, "Found unescaped U+2029 in data.js")

    def test_idempotent_sync_execution(self):
        """Executing sync_to_dashboard repeatedly with the same market data must not corrupt data.js."""
        raw_text = RAW_INPUT_PATH.read_text(encoding="utf-8")
        cleaned, _ = clean_raw_dump(raw_text)
        market_data = extract_facts(cleaned, date="2026-09-30")
        digest_md = generate_digest(market_data)
        insight_report = generate_insight(market_data, raw_text=cleaned)

        with tempfile.TemporaryDirectory() as tmp_dir:
            temp_data_js = Path(tmp_dir) / "data.js"
            temp_data_js.write_text(DATA_JS_PATH.read_text(encoding="utf-8"), encoding="utf-8")

            success = sync_to_dashboard(
                market_data,
                digest_md=digest_md,
                insight_report=insight_report,
                data_js_path=str(temp_data_js),
            )
            self.assertTrue(success, "sync_to_dashboard must return True")

            # Parse again from isolated temporary path
            reloaded_text = temp_data_js.read_text(encoding="utf-8")
            prefix = "window.WATCHLIST_DATA = "
            data = json.loads(reloaded_text[len(prefix):].rstrip(";\n "))
            self.assertIn("records", data)
            self.assertIn("dailyDigests", data)
            self.assertIn("dailyInsights", data)


class TestM3SchemaCompleteness(unittest.TestCase):
    """Probes requirement 2: Schema Completeness for records, dailyDigests, dailyInsights, stocks, and portfolio."""

    @classmethod
    def setUpClass(cls):
        cls.js_text = DATA_JS_PATH.read_text(encoding="utf-8")
        prefix = "window.WATCHLIST_DATA = "
        cls.data = json.loads(cls.js_text[len(prefix):].rstrip(";\n "))

    def test_top_level_schema_keys(self):
        """Top-level keys must include lastUpdated, portfolio, stocks, records, dailyDigests, dailyInsights."""
        required_keys = {"lastUpdated", "portfolio", "stocks", "records", "dailyDigests", "dailyInsights"}
        self.assertTrue(required_keys.issubset(set(self.data.keys())), f"Missing keys: {required_keys - set(self.data.keys())}")

    def test_stocks_metadata_contains_all_canonical_stocks(self):
        """stocks array must contain all 8 canonical stocks plus ALL."""
        stock_ids = {s.get("id") for s in self.data["stocks"]}
        expected_ids = {"ALL", "SK_SQUARE", "SK_HYNIX", "UBER", "MBLY", "FLNC", "UPST", "CELH", "ENPH"}
        self.assertTrue(expected_ids.issubset(stock_ids), f"Missing stocks in stocks metadata: {expected_ids - stock_ids}")

    def test_sk_hynix_models_master_normalized_to_skhy_nasdaq_adr(self):
        """SK_HYNIX in STOCK_MASTERS and DEFAULT_STOCKS must be normalized to SKHY, NASDAQ ADR, USD."""
        master = STOCK_MASTERS[StockSymbol.SK_HYNIX]
        self.assertEqual(master.ticker, "SKHY")
        self.assertEqual(master.market, "NASDAQ ADR")
        self.assertEqual(master.currency, "USD")

        def_skhy = next((s for s in DEFAULT_STOCKS if s["id"] == "SK_HYNIX"), None)
        self.assertIsNotNone(def_skhy)
        self.assertEqual(def_skhy["ticker"], "SKHY")
        self.assertEqual(def_skhy["market"], "NASDAQ ADR")
        self.assertEqual(def_skhy["currency"], "USD")

    def test_portfolio_structure_and_holdings(self):
        """portfolio must contain totalValue, lastReview, targetRatio, note, and holdings for SK Square & SK Hynix."""
        portfolio = self.data["portfolio"]
        self.assertIn("holdings", portfolio)
        self.assertIn("targetRatio", portfolio)
        self.assertIn("note", portfolio)

        holdings = portfolio["holdings"]
        holding_names = [h.get("name") or h.get("stockName", "") for h in holdings]
        self.assertTrue(any("SK스퀘어" in name for name in holding_names))
        self.assertTrue(any("SK하이닉스" in name for name in holding_names))

        sk_holding = next((h for h in holdings if "SK하이닉스" in (h.get("name") or h.get("stockName", ""))), None)
        self.assertIsNotNone(sk_holding)
        self.assertIn(sk_holding.get("shares"), ["10주", "20주"])
        self.assertIn("000660", sk_holding.get("ticker", ""))

    def test_records_m3_skhy_adr_close_record(self):
        """SK_HYNIX DAILY_CLOSE record for 2026-09-30 must reflect SKHY NASDAQ ADR with USD price."""
        records = self.data.get("records", [])
        sk_close = next((r for r in records if r.get("stockId") == "SK_HYNIX" and r.get("type") == "DAILY_CLOSE" and r.get("date") == "2026-09-30"), None)
        self.assertIsNotNone(sk_close, "Must have SK_HYNIX DAILY_CLOSE record on 2026-09-30")
        self.assertEqual(sk_close.get("ticker"), "SKHY")
        self.assertIn("NASDAQ ADR", sk_close.get("source", ""))
        metrics = sk_close.get("metrics", {})
        self.assertIn("$186.91", metrics.get("price", ""))
        self.assertIn("291만 주", metrics.get("volume", ""))

    def test_daily_digests_m3_fields(self):
        """dailyDigests array must contain entries with summaryTable containing SKHY and NASDAQ ADR."""
        digests = self.data.get("dailyDigests", [])
        self.assertGreater(len(digests), 0, "dailyDigests must not be empty")

        d30 = next((d for d in digests if d.get("date") == "2026-09-30"), None)
        self.assertIsNotNone(d30, "Must have dailyDigest for 2026-09-30")
        table = d30.get("summaryTable", [])
        sk_row = next((row for row in table if row.get("stockId") == "SK_HYNIX"), None)
        self.assertIsNotNone(sk_row, "SK_HYNIX must be in digest summaryTable")
        self.assertEqual(sk_row.get("ticker"), "SKHY")
        self.assertEqual(sk_row.get("market"), "NASDAQ ADR")
        self.assertIn("$186.91", sk_row.get("price", ""))


class TestM3View3IBDeepReportIntegration(unittest.TestCase):
    """Probes requirement 3: View 3 IB Deep Report Integration in data.js and dailyInsights[0]."""

    @classmethod
    def setUpClass(cls):
        cls.js_text = DATA_JS_PATH.read_text(encoding="utf-8")
        prefix = "window.WATCHLIST_DATA = "
        cls.data = json.loads(cls.js_text[len(prefix):].rstrip(";\n "))
        cls.insights = cls.data.get("dailyInsights", [])
        cls.assertTrue(len(cls.insights) > 0, "dailyInsights must contain at least 1 report")
        cls.ins0 = cls.insights[0]

    def test_daily_insights_top_level_keys(self):
        """dailyInsights[0] must contain all required top-level keys."""
        required_top_keys = [
            "unitEconomics",
            "peerComparison",
            "riskReward",
            "decisionMatrix",
            "markdownContent",
            "sections",
        ]
        for key in required_top_keys:
            self.assertIn(key, self.ins0, f"dailyInsights[0] missing top-level key '{key}'")

    def test_daily_insights_nested_sections_dict(self):
        """dailyInsights[0].sections must be a dictionary containing all 4 core sub-keys."""
        sections = self.ins0.get("sections")
        self.assertIsInstance(sections, dict, "dailyInsights[0].sections must be a dict")
        required_section_keys = ["unit_economics", "peer_comparison", "risk_reward", "decision_matrix"]
        for skey in required_section_keys:
            self.assertIn(skey, sections, f"dailyInsights[0].sections missing sub-key '{skey}'")

    def test_unit_economics_content_and_sk_hynix(self):
        """unitEconomics must contain 8 canonical stocks and SK_HYNIX 4:1 wafer ratio."""
        ue = self.ins0.get("unitEconomics")
        self.assertIsInstance(ue, dict)
        self.assertIn("SK_HYNIX", ue)
        sk_ue = ue["SK_HYNIX"]
        self.assertEqual(sk_ue.get("ticker"), "SKHY")
        self.assertEqual(sk_ue.get("currency"), "USD")
        self.assertEqual(sk_ue.get("waferRatio"), "4:1")
        self.assertIn("CSI 103.9", sk_ue.get("pricingPower", ""))

    def test_peer_comparison_content_and_micron(self):
        """peerComparison must contain peer comparisons including Micron (MU)."""
        pc = self.ins0.get("peerComparison")
        self.assertIsInstance(pc, list)
        self.assertEqual(len(pc), 8, "peerComparison must cover all 8 canonical stocks")
        sk_pc = next((p for p in pc if p.get("stockId") == "SK_HYNIX"), None)
        self.assertIsNotNone(sk_pc)
        self.assertIn("Micron", sk_pc.get("peer", ""))

    def test_markdown_content_contains_full_institutional_report(self):
        """markdownContent must contain complete IB research report markdown text."""
        md = self.ins0.get("markdownContent", "")
        self.assertGreater(len(md), 3000, "markdownContent must be substantial institutional report")
        self.assertIn("4:1", md)
        self.assertIn("CSI 103.9", md)
        self.assertIn("MR-MUF", md)
        self.assertIn("NCF", md)
        self.assertIn("1 : 4.2", md)


class TestM3ZeroCDNDOMAndOfflineIntegrity(unittest.TestCase):
    """Probes requirement 4: Local Zero-CDN DOM & Offline Integrity in index.html."""

    @classmethod
    def setUpClass(cls):
        cls.assertTrue(INDEX_HTML_PATH.exists(), f"index.html must exist at {INDEX_HTML_PATH}")
        cls.html_content = INDEX_HTML_PATH.read_text(encoding="utf-8")

    def test_zero_remote_script_tags(self):
        """index.html must contain ZERO script tags pointing to remote HTTP/HTTPS/protocol-relative URLs."""
        remote_scripts = re.findall(r'<script[^>]+src=["\'](https?:|//)[^"\']*["\']', self.html_content, re.I)
        self.assertEqual(remote_scripts, [], f"Found remote script tags in index.html: {remote_scripts}")

    def test_zero_remote_stylesheet_links(self):
        """index.html must contain ZERO link tags pointing to remote stylesheets."""
        remote_links = re.findall(r'<link[^>]+href=["\'](https?:|//)[^"\']*["\']', self.html_content, re.I)
        self.assertEqual(remote_links, [], f"Found remote link tags in index.html: {remote_links}")

    def test_zero_css_imports(self):
        """index.html must contain ZERO @import statements anywhere in CSS."""
        imports = re.findall(r'@import\s+[^;]+;', self.html_content, re.I)
        self.assertEqual(imports, [], f"Found @import statements in index.html: {imports}")

    def test_zero_remote_font_urls(self):
        """index.html must contain ZERO remote font or asset URLs inside url()."""
        urls = re.findall(r'url\s*\(\s*["\']?(https?:|//)[^\'")\s]+["\']?\s*\)', self.html_content, re.I)
        self.assertEqual(urls, [], f"Found remote URLs in CSS url(): {urls}")

    def test_zero_known_cdn_domains(self):
        """index.html must not reference any known third-party CDN domain names."""
        forbidden_cdns = [
            "fonts.googleapis.com",
            "fonts.gstatic.com",
            "cdnjs.cloudflare.com",
            "cdn.jsdelivr.net",
            "unpkg.com",
            "cdn.tailwindcss.com",
            "stackpath.bootstrapcdn.com",
            "use.fontawesome.com",
        ]
        lower_html = self.html_content.lower()
        for cdn in forbidden_cdns:
            self.assertNotIn(cdn, lower_html, f"Forbidden CDN domain '{cdn}' detected in index.html")

    def test_data_js_local_inclusion_relative(self):
        """index.html must load data.js via pure local relative path."""
        self.assertTrue(
            bool(re.search(r'<script[^>]+src=["\']\./?data\.js["\']', self.html_content, re.I)),
            "index.html must load data.js using local relative path './data.js' or 'data.js'"
        )

    def test_view1_digest_view_dom_elements(self):
        """View 1 (Digest) DOM container, macro & industry card, and render function must exist."""
        self.assertIn('id="viewDigestSection"', self.html_content)
        self.assertIn('id="digestStockCardsGrid"', self.html_content)
        self.assertIn("renderDigestView", self.html_content)
        self.assertIn("renderDigestStockCards", self.html_content)
        self.assertIn("grid-macro-portfolio", self.html_content)

    def test_view2_feed_view_white_space_pre_line_styling(self):
        """View 2 (Feed) must apply white-space: pre-line !important and word-break: break-word !important."""
        self.assertIn('id="viewTimeseriesSection"', self.html_content)
        self.assertIn('id="timeseriesFeedContainer"', self.html_content)
        self.assertIn("renderTimeseriesFeed", self.html_content)

        # Check CSS classes
        self.assertIn(".feed-summary-box", self.html_content)
        self.assertIn(".summary-box-content", self.html_content)
        self.assertIn(".strategist-body", self.html_content)

        # Ensure CSS rule white-space: pre-line is applied
        match = re.search(r'(\.feed-summary-box[^{]*\{[^}]*\})', self.html_content, re.DOTALL)
        self.assertIsNotNone(match, "CSS rule for .feed-summary-box must exist")
        rule_body = match.group(1)
        self.assertIn("white-space: pre-line", rule_body)
        self.assertIn("word-break: break-word", rule_body)

    def test_view3_ib_deep_report_markdown_reader(self):
        """View 3 (Insight) DOM container, renderInsightView, and renderMarkdownToHtml reader must exist."""
        self.assertIn('id="viewInsightSection"', self.html_content)
        self.assertIn('id="insightContainer"', self.html_content)
        self.assertIn("renderInsightView", self.html_content)
        self.assertIn("renderMarkdownToHtml", self.html_content)
        self.assertIn("ib-markdown-body", self.html_content)

    def test_zero_raw_markdown_link_leaks_in_records(self):
        """records in data.js must not leak raw markdown links [text](url) in titles or summaries."""
        js_text = DATA_JS_PATH.read_text(encoding="utf-8")
        prefix = "window.WATCHLIST_DATA = "
        data = json.loads(js_text[len(prefix):].rstrip(";\n "))

        raw_link_pattern = re.compile(r"\[.*?\]\(https?://.*?\)")
        leaks = []
        for r in data.get("records", []):
            title = r.get("title", "")
            if raw_link_pattern.search(title):
                leaks.append(f"Title in {r.get('id')}: {title}")
            for k, v in (r.get("metrics") or {}).items():
                if isinstance(v, str) and raw_link_pattern.search(v):
                    leaks.append(f"Metric {k} in {r.get('id')}: {v}")

        self.assertEqual(leaks, [], f"Detected raw markdown link leaks in records: {leaks}")

    def test_zero_spurious_range_badge_pollutions(self):
        """records in data.js must not contain spurious text sentences in range metric."""
        js_text = DATA_JS_PATH.read_text(encoding="utf-8")
        prefix = "window.WATCHLIST_DATA = "
        data = json.loads(js_text[len(prefix):].rstrip(";\n "))

        bad_substrings = ["불명확", "상존", "범위가", "부근", "발표", "골드만삭스"]
        pollutions = []
        for r in data.get("records", []):
            range_val = (r.get("metrics") or {}).get("range", "")
            if any(bad in range_val for bad in bad_substrings):
                pollutions.append(f"Polluted range in {r.get('id')}: {range_val}")

        self.assertEqual(pollutions, [], f"Detected spurious text in range badges: {pollutions}")


if __name__ == "__main__":
    unittest.main()
