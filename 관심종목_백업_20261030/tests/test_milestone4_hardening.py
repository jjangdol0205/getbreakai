"""Milestone 4 Hardening and Verification Test Suite.

Verifies:
1. Cleaner hardening against Gemini sidebar histories, public earnings disclaimers,
   variation selectors, decorative header emojis, and YouTube preamble peeling.
2. Extractor hardening for interviewees, brokerages, ratio masking, SK Square
   +87% false-positive prevention, and inactive stock non-activation.
3. Official quote verification for 2026-10-01 inputs.
4. 8-stock 5-year financials schema completeness in data.js.
5. Index.html terminal overhaul, 4th view (5-Year Financial Explorer),
   drawer modal, and Zero-CDN offline compliance.
6. Finance feed module integrity.
"""

from __future__ import annotations

import json
from pathlib import Path
import re
import unittest

ROOT_DIR = Path(__file__).resolve().parent.parent
DATA_JS_PATH = ROOT_DIR / "data.js"
INDEX_HTML_PATH = ROOT_DIR / "index.html"
RAW_INPUT_1001_PATH = ROOT_DIR / "raw_input_20261001.txt"

from engine.cleaner import RawDumpCleaner, clean_raw_dump
from engine.extractor import FactExtractor
from engine.finance_feed import FinanceFeed, OfficialQuote
from engine.models import KNOWN_BROKERAGES, KNOWN_INTERVIEWEES, StockSymbol
from engine.sync_dashboard import parse_js_data_store


class TestCleanerHardening(unittest.TestCase):
    """Verifies regex filtering enhancements in engine/cleaner.py."""

    def setUp(self) -> None:
        self.cleaner = RawDumpCleaner()

    def test_gemini_sidebar_chat_titles_stripped(self) -> None:
        raw_text = (
            "## 1. 당일 주요 시황\n"
            "- 2026년 9월 28일 플루언스에너지(FLNC) 주가 흐름을 분석함\n"
            "- 업스타트홀딩스 투자 분석 정보업스타트홀딩스의 주가 흐름과 시장 영향 요인을 분석함\n"
            "- 셀시우스 홀딩스 기업 분석Analyzed Celsius Holdings' latest stock performance\n"
            "- 인페이즈 에너지 기업 분석Analyzed Wall Street analyst ratings for Enphase Energy\n"
            "- YouTube Video Content Analysis: AI semiconductor market overview\n"
            "SK하이닉스는 전일 대비 견조한 상승세를 유지했습니다.\n"
        )
        cleaned, meta = self.cleaner.clean_with_metadata(raw_text)

        self.assertNotIn("플루언스에너지(FLNC) 주가 흐름을 분석함", cleaned)
        self.assertNotIn("업스타트홀딩스의 주가 흐름과 시장 영향 요인을 분석함", cleaned)
        self.assertNotIn("Analyzed Celsius Holdings", cleaned)
        self.assertNotIn("Analyzed Wall Street analyst ratings", cleaned)
        self.assertNotIn("YouTube Video Content Analysis", cleaned)
        self.assertIn("SK하이닉스는 전일 대비 견조한 상승세를 유지했습니다.", cleaned)

    def test_disclaimers_stripped(self) -> None:
        raw_text = (
            "SK하이닉스 장마감 브리핑\n"
            "위 내용은 공개 실적발표 내용으로 별도의 승인절차 없이 제공합니다.\n"
            "본 자료는 정보 제공만을 목적으로 하며 투자 결과에 대한 책임은 본인에게 있습니다.\n"
            "실적 호조가 지속되고 있습니다.\n"
        )
        cleaned = self.cleaner.clean(raw_text)
        self.assertNotIn("별도의 승인절차 없이 제공합니다", cleaned)
        self.assertNotIn("투자 결과에 대한 책임은 본인에게 있습니다", cleaned)
        self.assertIn("실적 호조가 지속되고 있습니다.", cleaned)

    def test_variation_selectors_normalized(self) -> None:
        raw_text = "SK하이닉스\uFE0E 주가\uFE0F 브리핑"
        cleaned = self.cleaner.clean(raw_text)
        self.assertNotIn("\uFE0E", cleaned)
        self.assertNotIn("\uFE0F", cleaned)

    def test_decorative_emojis_in_headers_stripped(self) -> None:
        raw_text = "### ▶️ 주요 실적 발표 코멘트\n실적 발표 내용\n### ▶️ 주요 Q&A 분석\n질의응답 내용\n"
        cleaned = self.cleaner.clean(raw_text)
        self.assertNotIn("▶️", cleaned)
        self.assertIn("주요 실적 발표 코멘트", cleaned)
        self.assertIn("주요 Q&A 분석", cleaned)

    def test_youtube_preamble_peeled(self) -> None:
        raw_text = "YouTube 서비스 약관이 적용됩니다. https://youtube.com/watch?v=12345"
        cleaned = self.cleaner.clean(raw_text)
        self.assertNotIn("YouTube 서비스 약관이 적용됩니다.", cleaned)
        self.assertIn("https://youtube.com/watch?v=12345", cleaned)


class TestExtractorHardening(unittest.TestCase):
    """Verifies extractor hardening against false positives and entity extensions."""

    def test_known_interviewees_and_brokerages_extended(self) -> None:
        self.assertIn("Dom Taylor", KNOWN_INTERVIEWEES)
        self.assertIn("Dan Galves", KNOWN_INTERVIEWEES)
        self.assertIn("Bernstein", KNOWN_BROKERAGES)
        self.assertIn("Evercore", KNOWN_BROKERAGES)

    def test_sk_square_gpm_ratio_not_misattributed_as_change_pct(self) -> None:
        dump_text = (
            "## SK스퀘어\n"
            "지주사 할인율 및 비즈니스 펀더멘털 분석.\n"
            "## 마이크론 컨퍼런스콜 Q&A 전문\n"
            "Q: 낸드와 HBM 마진 전망은 어떠한가?\n"
            "A: 이번 분기 GPM 86.25%를 기록했으며 연간 총마진(GPM) 87% 수준에 도달할 전망입니다.\n"
        )
        extractor = FactExtractor()
        data = extractor.extract(dump_text, date_override="2026-10-01")

        sq_sheet = data.stocks.get("SK_SQUARE")
        if sq_sheet and sq_sheet.metrics:
            self.assertNotEqual(sq_sheet.metrics.change_percent, 87.0)
            self.assertNotEqual(sq_sheet.metrics.change_percent, -87.0)

    def test_raw_dump_20261001_extraction_metrics(self) -> None:
        self.assertTrue(RAW_INPUT_1001_PATH.exists(), "raw_input_20261001.txt must exist")
        raw_text = RAW_INPUT_1001_PATH.read_text(encoding="utf-8")
        cleaned, _ = clean_raw_dump(raw_text)
        data = FactExtractor().extract(cleaned, date_override="2026-10-01")

        # 1. Active stocks check
        self.assertIn("SK_HYNIX", data.stocks)
        self.assertIn("UBER", data.stocks)
        self.assertIn("MBLY", data.stocks)
        self.assertIn("SK_SQUARE", data.stocks)

        # 2. Inactive stocks must NOT be falsely activated
        for inactive in ["FLNC", "UPST", "CELH", "ENPH"]:
            self.assertNotIn(
                inactive,
                data.stocks,
                f"Inactive stock {inactive} should not be in extracted stocks for 2026-10-01",
            )

        # 3. Verified metrics
        skhy_m = data.stocks["SK_HYNIX"].metrics
        self.assertIsNotNone(skhy_m)
        self.assertAlmostEqual(skhy_m.close_price, 188.80, places=2)
        self.assertAlmostEqual(skhy_m.change_percent, 1.01, places=2)
        self.assertEqual(skhy_m.volume, 2150000)

        uber_m = data.stocks["UBER"].metrics
        self.assertIsNotNone(uber_m)
        self.assertAlmostEqual(uber_m.close_price, 68.51, places=2)
        self.assertAlmostEqual(uber_m.change_percent, -1.23, places=2)
        self.assertEqual(uber_m.volume, 15600000)

        mbly_m = data.stocks["MBLY"].metrics
        self.assertIsNotNone(mbly_m)
        self.assertAlmostEqual(mbly_m.close_price, 7.565, places=3)
        self.assertAlmostEqual(mbly_m.change_percent, -2.95, places=2)
        self.assertEqual(mbly_m.volume, 4890000)

        sq_m = data.stocks["SK_SQUARE"].metrics
        if sq_m:
            self.assertIsNone(sq_m.close_price)
            self.assertIsNone(sq_m.change_percent)


class TestDataJsFinancials(unittest.TestCase):
    """Verifies that data.js contains the full 5-year financials schema for all 8 stocks."""

    def setUp(self) -> None:
        self.assertTrue(DATA_JS_PATH.exists())
        self.data = parse_js_data_store(DATA_JS_PATH.read_text(encoding="utf-8"))

    def test_financials_object_exists_with_all_8_stocks(self) -> None:
        self.assertIn("financials", self.data, "data.js must contain 'financials' key")
        financials = self.data["financials"]

        canonical_8 = ["SK_HYNIX", "SK_SQUARE", "UBER", "MBLY", "FLNC", "UPST", "CELH", "ENPH"]
        for sym in canonical_8:
            self.assertIn(sym, financials, f"Missing financials for stock {sym}")

    def test_financial_statement_categories_and_years(self) -> None:
        financials = self.data["financials"]
        categories = ["income_statement", "profitability", "cash_flow", "balance_sheet", "valuation"]

        for sym, fin in financials.items():
            self.assertIn("years", fin, f"Missing 'years' in financials for {sym}")
            self.assertGreaterEqual(len(fin["years"]), 5, f"Expected at least 5 years in financials for {sym}")
            self.assertTrue("2021" in fin["years"] or "2022" in fin["years"], f"Expected 2021 or 2022 in financials for {sym}")
            self.assertIn("2025", fin["years"], f"Expected 2025 in financials for {sym}")
            self.assertTrue(any("2026" in y for y in fin["years"]), f"Expected 2026 in financials for {sym}")

            for cat in categories:
                self.assertIn(cat, fin, f"Missing category '{cat}' in financials for {sym}")
                self.assertIsInstance(fin[cat], dict, f"Category '{cat}' must be a dictionary in {sym}")
                for metric, vals in fin[cat].items():
                    self.assertGreaterEqual(
                        len(vals),
                        5,
                        f"Metric '{metric}' in category '{cat}' for {sym} must have at least 5 annual data points, got {len(vals)}",
                    )


class TestIndexHtmlTerminalHardening(unittest.TestCase):
    """Verifies modern fintech terminal UI/UX, 4th view, and Zero-CDN compliance."""

    def setUp(self) -> None:
        self.assertTrue(INDEX_HTML_PATH.exists())
        self.html = INDEX_HTML_PATH.read_text(encoding="utf-8")

    def test_zero_cdn_offline_compliance(self) -> None:
        remote_scripts = re.findall(r'<script[^>]+src=["\'](https?://[^"\']+)["\']', self.html, re.I)
        remote_links = re.findall(r'<link[^>]+href=["\'](https?://[^"\']+)["\']', self.html, re.I)
        self.assertEqual(remote_scripts, [], "index.html must not load external scripts")
        self.assertEqual(remote_links, [], "index.html must not load external stylesheets")

    def test_offline_badges_present(self) -> None:
        self.assertIn("100% Offline Core", self.html)
        self.assertIn("badge-offline", self.html)

    def test_4th_view_elements_present(self) -> None:
        self.assertIn('id="btnViewFinancials"', self.html)
        self.assertTrue(
            'id="containerViewFinancials"' in self.html or 'id="viewFinancialsSection"' in self.html,
            "index.html must contain 5-Year Financial Explorer view container",
        )

    def test_stock_drawer_modal_present(self) -> None:
        self.assertIn('id="stockDrawerModal"', self.html)
        self.assertIn('id="stockDrawerContent"', self.html)

    def test_all_view_switch_buttons_present(self) -> None:
        expected_buttons = ["btnViewDigest", "btnViewTimeseries", "btnViewInsight", "btnViewFinancials"]
        for btn in expected_buttons:
            self.assertIn(f'id="{btn}"', self.html, f"Missing view switch button: {btn}")


class TestFinanceFeed(unittest.TestCase):
    """Verifies that engine/finance_feed.py provides accurate official market quotes."""

    def test_finance_feed_quotes_all_8_stocks(self) -> None:
        feed = FinanceFeed()
        quotes = feed.get_all_quotes()
        canonical_8 = ["SK_HYNIX", "SK_SQUARE", "UBER", "MBLY", "FLNC", "UPST", "CELH", "ENPH"]

        for sym in canonical_8:
            self.assertIn(sym, quotes, f"Missing quote for {sym} in finance feed")
            q = quotes[sym]
            self.assertIsInstance(q, OfficialQuote)
            self.assertGreater(q.close, 0.0, f"Quote close price for {sym} must be positive")
            self.assertIsNotNone(q.volume, f"Quote volume for {sym} must be populated")


if __name__ == "__main__":
    unittest.main()
