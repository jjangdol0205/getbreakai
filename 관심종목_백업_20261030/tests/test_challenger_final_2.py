"""Final System Acceptance Gate Challenger Test Suite (Challenger Final 2).

Adversarial stress-testing of:
1. index.html offline isolation (Zero-CDN, zero remote links, zero external calls)
2. Triple-View DOM element consistency and data.js loadability
3. engine.insight_generator.InsightGenerator stress harness:
   - Empty data
   - Partial data
   - Adversarial noise & injection
   - Malformed Unicode & surrogates
   - Extreme financial metrics
   - 4-section structure and unit economics verification
"""

import copy
from datetime import datetime
import json
import os
from pathlib import Path
import re
import tempfile
import unittest

from engine.models import (
    STOCK_MASTERS,
    DailyMarketData,
    KeyWatchPoints,
    MarketMetrics,
    PairStrategy,
    StockFactSheet,
    StockSymbol,
)
from engine.insight_generator import (
    CANONICAL_STOCKS,
    DeepInsightReport,
    InsightGenerator,
    generate_insight,
)
from engine.sync_dashboard import (
    DEFAULT_DATA_JS_PATH,
    ROOT_DIR,
    create_default_data_store,
    parse_js_data_store,
    update_data_store_with_market_data,
)


def make_mock_factsheet(symbol: StockSymbol, **kwargs) -> StockFactSheet:
    master = STOCK_MASTERS.get(symbol)
    metrics = kwargs.pop("metrics", None)
    if metrics is None:
        metrics = MarketMetrics(
            stock_id=symbol.value,
            close_price=100.0,
            close_price_formatted="$100.00",
            change_percent=1.5,
            change_percent_formatted="+1.50%",
            volume=10000,
            volume_formatted="10,000주",
        )
    return StockFactSheet(
        stock_id=symbol.value,
        stock_name=master.name_kr if master else symbol.value,
        name_kr=master.name_kr if master else symbol.value,
        name_en=master.name_en if master else symbol.value,
        ticker=master.ticker if master else symbol.value,
        market=master.market if master else "NASDAQ",
        category=master.category if master else "TECH",
        badge_color=master.badge_color if master else "blue",
        metrics=metrics,
        **kwargs,
    )


class TestIndexHtmlOfflineIsolation(unittest.TestCase):
    """Rigorous offline isolation scanning of index.html."""

    def setUp(self):
        self.html_path = ROOT_DIR / "index.html"
        self.assertTrue(self.html_path.exists(), f"index.html not found at {self.html_path}")
        self.html_content = self.html_path.read_text(encoding="utf-8")

    def test_zero_remote_script_and_link_tags(self):
        """Scans for remote script and link tags in index.html."""
        remote_scripts = re.findall(
            r"<script[^>]+src=[\"']\s*(?:https?:|//)[^\"']+[\"']",
            self.html_content,
            re.IGNORECASE,
        )
        self.assertEqual(
            remote_scripts,
            [],
            f"Found remote <script> tags: {remote_scripts}",
        )

        remote_links = re.findall(
            r"<link[^>]+href=[\"']\s*(?:https?:|//)[^\"']+[\"']",
            self.html_content,
            re.IGNORECASE,
        )
        self.assertEqual(
            remote_links,
            [],
            f"Found remote <link> tags: {remote_links}",
        )

    def test_zero_css_remote_imports_and_urls(self):
        """Ensures <style> blocks contain zero @import or url() pointing to external resources."""
        style_blocks = re.findall(r"<style[^>]*>(.*?)</style>", self.html_content, re.DOTALL | re.IGNORECASE)
        for idx, block in enumerate(style_blocks):
            remote_imports = re.findall(r"@import\s+(?:url\()?[\"']?\s*(?:https?:|//)", block, re.IGNORECASE)
            self.assertEqual(
                remote_imports,
                [],
                f"Style block {idx} contains remote @import: {remote_imports}",
            )

            remote_urls = re.findall(r"url\s*\(\s*[\"']?\s*(?:https?:|//)", block, re.IGNORECASE)
            self.assertEqual(
                remote_urls,
                [],
                f"Style block {idx} contains remote url(): {remote_urls}",
            )

    def test_zero_external_cdn_references_in_markup(self):
        """Verifies no unpkg, jsdelivr, cdnjs, gstatic, googleapis CDNs are referenced in markup."""
        prohibited_cdns = [
            "unpkg.com",
            "jsdelivr.net",
            "cdnjs.cloudflare.com",
            "gstatic.com",
            "fonts.googleapis.com",
            "bootstrapcdn.com",
            "fontawesome",
        ]
        for cdn in prohibited_cdns:
            matches = re.findall(rf"[\"'][^\"']*{re.escape(cdn)}[^\"']*[\"']", self.html_content, re.IGNORECASE)
            self.assertEqual(
                matches,
                [],
                f"Prohibited CDN '{cdn}' referenced in markup: {matches}",
            )

    def test_local_relative_data_js_source(self):
        """Verifies that data.js is loaded strictly via local relative script path."""
        data_script_matches = re.findall(
            r"<script[^>]+src=[\"'](\./data\.js|data\.js)[\"'][^>]*>",
            self.html_content,
            re.IGNORECASE,
        )
        self.assertTrue(
            len(data_script_matches) >= 1,
            "index.html must load data.js via local relative path (./data.js)",
        )

    def test_no_browser_network_request_api_in_script(self):
        """Verifies that client-side JS does not initiate live fetch/xhr network requests."""
        script_blocks = re.findall(r"<script[^>]*>(.*?)</script>", self.html_content, re.DOTALL | re.IGNORECASE)
        js_text = "\n".join(script_blocks)
        fetch_calls = re.findall(r"\bfetch\s*\(", js_text)
        xhr_calls = re.findall(r"\bnew\s+XMLHttpRequest\s*\(", js_text)
        ws_calls = re.findall(r"\bnew\s+WebSocket\s*\(", js_text)
        self.assertEqual(fetch_calls, [], f"Unexpected fetch() calls in offline JS: {fetch_calls}")
        self.assertEqual(xhr_calls, [], f"Unexpected XMLHttpRequest calls in offline JS: {xhr_calls}")
        self.assertEqual(ws_calls, [], f"Unexpected WebSocket calls in offline JS: {ws_calls}")


class TestTripleViewAndDataJsConsistency(unittest.TestCase):
    """Verifies data.js loadability and Triple-View DOM element consistency in index.html."""

    def setUp(self):
        self.html_content = (ROOT_DIR / "index.html").read_text(encoding="utf-8")
        self.data_js_content = DEFAULT_DATA_JS_PATH.read_text(encoding="utf-8")
        self.parsed_data = parse_js_data_store(self.data_js_content)

    def test_data_js_parses_successfully(self):
        """Verifies data.js parse_js_data_store succeeds and contains required top-level keys."""
        self.assertIsInstance(self.parsed_data, dict)
        self.assertIn("portfolio", self.parsed_data)
        self.assertIn("stocks", self.parsed_data)
        self.assertIn("records", self.parsed_data)
        self.assertIn("dailyDigests", self.parsed_data)
        self.assertIn("dailyInsights", self.parsed_data)

    def test_data_js_stocks_contain_all_8_symbols(self):
        """Verifies stocks metadata in data.js covers all 8 target stocks."""
        stock_ids = [s["id"] for s in self.parsed_data["stocks"]]
        expected = ["SK_HYNIX", "SK_SQUARE", "UBER", "MBLY", "FLNC", "UPST", "CELH", "ENPH"]
        for sym in expected:
            self.assertIn(sym, stock_ids, f"Stock ID {sym} missing from data.js stocks metadata")

    def test_triple_view_sections_exist_in_dom(self):
        """Verifies all 3 View container sections exist in index.html."""
        view_sections = ["viewDigestSection", "viewTimeseriesSection", "viewInsightSection"]
        for view_id in view_sections:
            self.assertRegex(
                self.html_content,
                rf'id=[\"\']{view_id}[\"\']',
                f"Triple-View section id='{view_id}' missing in index.html",
            )

    def test_triple_view_switch_buttons_exist(self):
        """Verifies view switch buttons exist and bind to switchView."""
        buttons = ["btnViewDigest", "btnViewTimeseries", "btnViewInsight"]
        for btn_id in buttons:
            self.assertRegex(
                self.html_content,
                rf'id=[\"\']{btn_id}[\"\']',
                f"Switcher button id='{btn_id}' missing in index.html",
            )
        self.assertIn("switchView('digest')", self.html_content)
        self.assertIn("switchView('timeseries')", self.html_content)
        self.assertIn("switchView('insight')", self.html_content)

    def test_view_1_digest_required_dom_elements(self):
        """Verifies View 1 (Daily Digest) has all required interactive elements."""
        required_elements = [
            "digestDateSelect",
            "pairRationaleBox",
            "pairActionBadge",
            "digestMatrixBody",
            "digestStockCardsGrid",
        ]
        for el_id in required_elements:
            self.assertRegex(
                self.html_content,
                rf'id=[\"\']{el_id}[\"\']',
                f"View 1 element id='{el_id}' missing in index.html",
            )

    def test_view_2_timeseries_required_dom_elements(self):
        """Verifies View 2 (Time-Series) has all required filter & feed elements."""
        required_elements = [
            "timeseriesSearchInput",
            "stockFilterPillsContainer",
            "typeFilterPillsContainer",
            "timeseriesFeedContainer",
            "timeseriesEmptyState",
        ]
        for el_id in required_elements:
            self.assertRegex(
                self.html_content,
                rf'id=[\"\']{el_id}[\"\']',
                f"View 2 element id='{el_id}' missing in index.html",
            )

    def test_view_3_deep_insight_required_dom_elements(self):
        """Verifies View 3 (Deep Insight) has date selector and report container."""
        required_elements = [
            "insightDateSelect",
            "insightCoverageLabel",
            "insightContainer",
        ]
        for el_id in required_elements:
            self.assertRegex(
                self.html_content,
                rf'id=[\"\']{el_id}[\"\']',
                f"View 3 element id='{el_id}' missing in index.html",
            )

    def test_stock_meta_in_javascript_covers_8_stocks(self):
        """Verifies STOCK_META inside JavaScript contains all 8 target stock definitions."""
        for sym in ["SK_HYNIX", "SK_SQUARE", "UBER", "MBLY", "FLNC", "UPST", "CELH", "ENPH"]:
            self.assertIn(
                f'"{sym}"',
                self.html_content,
                f"STOCK_META in index.html missing key '{sym}'",
            )


class TestInsightGeneratorAdversarialStress(unittest.TestCase):
    """Adversarial stress-testing of InsightGenerator and DeepInsightReport."""

    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.output_dir = Path(self.temp_dir.name)
        self.generator = InsightGenerator(output_dir=self.output_dir)

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_stress_empty_market_data(self):
        """Stress-tests InsightGenerator when DailyMarketData is completely empty."""
        empty_data = DailyMarketData(
            date="",
            macro_summary="",
            stocks={},
            pair_strategy=PairStrategy(),
        )

        report = self.generator.generate(empty_data, raw_text="")
        self.assertIsInstance(report, DeepInsightReport)
        self.assertTrue(report.markdown_content)
        self.assertTrue(Path(report.markdown_path).exists())

        md = report.markdown_content
        self.assertIn("## 1. 비즈니스 모델 및 유닛 이코노믹스", md)
        self.assertIn("## 2. 글로벌 피어 그룹 비교 및 상대 밸류에이션 매트릭스", md)
        self.assertIn("## 3. 손익비 (Risk-Reward) 및 하방 지지력 분석", md)
        self.assertIn("## 4. 전술적 투자의사결정 매트릭스 (매수/매도/홀딩 밴드)", md)

        for sym in CANONICAL_STOCKS:
            self.assertIn(sym.value, report.unit_economics)
            self.assertIn(sym.value, report.risk_reward)
        self.assertEqual(len(report.peer_comparison), 8)
        self.assertEqual(len(report.decision_matrix), 8)

    def test_stress_partial_data_with_nones(self):
        """Stress-tests InsightGenerator with partial stocks having None and empty attributes."""
        partial_data = DailyMarketData(
            date="2026-09-30",
            macro_summary="매크로 노이즈 지속",
            stocks={
                StockSymbol.CELH.value: make_mock_factsheet(
                    StockSymbol.CELH,
                    metrics=MarketMetrics(stock_id="CELH"),
                    core_drivers=[],
                    key_points=None,
                ),
                StockSymbol.ENPH.value: make_mock_factsheet(
                    StockSymbol.ENPH,
                    metrics=MarketMetrics(
                        stock_id="ENPH",
                        close_price=None,
                        change_percent=None,
                        volume=None,
                    ),
                    core_drivers=["NEM 3.0 전환"],
                    key_points=KeyWatchPoints(
                        line1_short_term="",
                        line2_mid_long_term="",
                    ),
                ),
            },
            pair_strategy=PairStrategy(
                sk_square_weight=0.0,
                sk_hynix_weight=0.0,
            ),
        )

        report = self.generator.generate(partial_data, raw_text="")
        self.assertEqual(report.date, "2026-09-30")
        self.assertIn("셀시우스", report.markdown_content)
        self.assertIn("엔페이즈", report.markdown_content)

    def test_stress_adversarial_noise_and_markdown_injection(self):
        """Stress-tests InsightGenerator against malicious markdown and HTML injections."""
        injection_text = (
            "## 1. Fake Header Injection\n"
            "| Bad | Table | Injection | Column |\n"
            "|---|---|---|---|\n"
            "<script>alert('XSS')</script>\n"
            "''' DROP TABLE stocks; --\n"
            "\"\"\" unclosed quotes \n"
        )
        data = DailyMarketData(
            date="2026-09-30",
            macro_summary=injection_text,
            stocks={
                StockSymbol.SK_HYNIX.value: make_mock_factsheet(
                    StockSymbol.SK_HYNIX,
                    metrics=MarketMetrics(
                        stock_id="SK_HYNIX",
                        close_price=175000.0,
                        close_price_formatted="175,000원 | injected",
                        change_percent=-3.5,
                        change_percent_formatted="-3.5% | injected",
                    ),
                    core_drivers=[injection_text],
                )
            },
            pair_strategy=PairStrategy(),
        )

        report = self.generator.generate(data, raw_text=injection_text)
        self.assertTrue(report.markdown_content)
        saved_file = Path(report.markdown_path)
        content_from_disk = saved_file.read_text(encoding="utf-8")
        self.assertEqual(content_from_disk, report.markdown_content)

    def test_stress_malformed_unicode_and_emojis(self):
        """Stress-tests InsightGenerator with complex Unicode, emojis, ZWJ, and control characters."""
        unicode_title = "SK하이닉스 🚀 HBM4 🔥 16단 👨‍👩‍👧‍👦 \u200b\u200d\u2060 \u202eRLO"
        data = DailyMarketData(
            date="2026-09-30",
            stocks={
                StockSymbol.SK_HYNIX.value: make_mock_factsheet(
                    StockSymbol.SK_HYNIX,
                    core_drivers=[unicode_title],
                )
            },
            pair_strategy=PairStrategy(),
        )

        report = self.generator.generate(data, raw_text=unicode_title)
        self.assertIn("2026-09-30", report.date)
        saved_content = Path(report.markdown_path).read_text(encoding="utf-8")
        self.assertTrue(len(saved_content) > 1000)

    def test_stress_extreme_financial_metrics(self):
        """Stress-tests InsightGenerator with extreme price, negative values, and zero prices."""
        data = DailyMarketData(
            date="2026-09-30",
            stocks={
                StockSymbol.SK_HYNIX.value: make_mock_factsheet(
                    StockSymbol.SK_HYNIX,
                    metrics=MarketMetrics(
                        stock_id="SK_HYNIX",
                        close_price=0.0,
                        close_price_formatted="0원",
                        change_percent=-100.0,
                        change_percent_formatted="-100.0%",
                        volume=10**15,
                        volume_formatted="1,000조 주",
                    ),
                ),
                StockSymbol.UBER.value: make_mock_factsheet(
                    StockSymbol.UBER,
                    metrics=MarketMetrics(
                        stock_id="UBER",
                        close_price=-5.0,
                        close_price_formatted="-$5.00",
                        change_percent=9999.9,
                        change_percent_formatted="+9999.9%",
                    ),
                ),
            },
            pair_strategy=PairStrategy(),
        )

        report = self.generator.generate(data)
        self.assertIn("0원", report.markdown_content)
        self.assertIn("1. 비즈니스 모델 및 유닛 이코노믹스", report.markdown_content)

    def test_all_four_original_request_sections_verified(self):
        """Verifies that all 4 sections mandated in ORIGINAL_REQUEST.md R4 exist and have exact content."""
        report = self.generator.generate(DailyMarketData(date="2026-09-30"))
        md = report.markdown_content

        self.assertIn("가동률", md)
        self.assertIn("LTA", md)
        self.assertIn("SOP", md)
        self.assertIn("수수료율", md)

        self.assertIn("핵심 피어 그룹", md)
        self.assertIn("마이크론", md)
        self.assertIn("소프트뱅크", md)
        self.assertIn("몬스터", md)

        self.assertIn("손익비", md)
        self.assertIn("하방 지지선", md)
        self.assertIn("목표 상방", md)

        self.assertIn("적극 매수 밴드", md)
        self.assertIn("홀딩", md)
        self.assertIn("분할 익절", md)
        self.assertIn("리스크 컷", md)

    def test_sync_to_data_js_pipeline_integration(self):
        """Verifies full end-to-end integration: InsightGenerator -> update_data_store_with_market_data."""
        market_data = DailyMarketData(
            date="2026-09-30",
            stocks={StockSymbol.SK_HYNIX.value: make_mock_factsheet(StockSymbol.SK_HYNIX)},
            pair_strategy=PairStrategy(sk_square_weight=57.6, sk_hynix_weight=42.3),
        )
        report = self.generator.generate(market_data)

        store = create_default_data_store()
        updated_store = update_data_store_with_market_data(
            store,
            market_data,
            digest_md="# Digest",
            insight_report=report,
        )

        self.assertIn("dailyInsights", updated_store)
        self.assertEqual(len(updated_store["dailyInsights"]), 1)
        ins = updated_store["dailyInsights"][0]
        self.assertEqual(ins["date"], "2026-09-30")
        self.assertIn("unitEconomics", ins)
        self.assertIn("peerComparison", ins)
        self.assertIn("riskReward", ins)
        self.assertIn("decisionMatrix", ins)


if __name__ == "__main__":
    unittest.main()
