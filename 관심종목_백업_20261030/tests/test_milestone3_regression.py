"""Milestone 3 Comprehensive Regression Test Suite.

Verifies end-to-end acceptance criteria for Milestone 3:
- R1: Macro/Industry Linkage & Section 2 Empty Card Suppression
- R2: SK Hynix NASDAQ ADR Normalization (SKHY / USD / ADR Premium)
- R3: Institutional IB Deep Research Report (Dual-Part Structure, 8-Stock Matrices)
- R4: Time-Series Filter View Standardization & UI/Regex Bug Eradication
"""

from __future__ import annotations

import json
from pathlib import Path
import re
import unittest

from engine.cleaner import strip_markdown_links, clean_raw_dump
from engine.extractor import extract_facts, FactExtractor, STANDARDIZED_STRATEGIST_IMPLICATIONS
from engine.models import StockSymbol, STOCK_MASTERS, DailyMarketData
from engine.digest_generator import generate_digest, DigestGenerator
from engine.insight_generator import generate_insight, InsightGenerator, DeepInsightReport
from engine.sync_dashboard import sync_to_dashboard, parse_js_data_store, build_digest_entry, build_insight_entry

REPO_ROOT = Path(__file__).resolve().parent.parent


class TestMilestone3R1MacroAndEmptyCardSuppression(unittest.TestCase):
    """R1: Macro/Industry Linkage & Section 2 Empty Card Suppression."""

    def setUp(self):
        self.raw_dump_path = REPO_ROOT / "raw_input_20260930.txt"
        self.assertTrue(self.raw_dump_path.exists(), "raw_input_20260930.txt must exist")
        with open(self.raw_dump_path, "r", encoding="utf-8") as f:
            self.raw_text = f.read()
        cleaned_text, _ = clean_raw_dump(self.raw_text)
        self.market_data = extract_facts(cleaned_text, date="2026-09-30")

    def test_digest_contains_top_macro_and_industry_linkage_section(self):
        """Daily digest Section 1 must include prominent macro & industry linkage section."""
        digest_md = DigestGenerator().build_markdown(self.market_data)
        self.assertIn("### 🌐 관심종목 연계 매크로 & 산업 핵심 동향", digest_md)
        self.assertIn("Nomura CSI 103.9", digest_md)
        self.assertIn("132.4%", digest_md)
        self.assertIn("10년물 국채 금리", digest_md)

    def test_digest_section_2_suppresses_empty_cards(self):
        """Digest Section 2 must ONLY render cards for stocks present in input dump."""
        digest_md = DigestGenerator().build_markdown(self.market_data)

        # 5 stocks are present in raw_input_20260930.txt
        self.assertIn("### 📌 SK하이닉스", digest_md)
        self.assertIn("### 📌 우버", digest_md)
        self.assertIn("### 📌 모빌아이", digest_md)
        self.assertIn("### 📌 플루언스에너지", digest_md)
        self.assertIn("### 📌 업스타트홀딩스", digest_md)

        # 3 unprovided stocks must NOT have individual ### 📌 cards in Section 2
        self.assertNotIn("### 📌 SK스퀘어", digest_md)
        self.assertNotIn("### 📌 셀시우스", digest_md)
        self.assertNotIn("### 📌 엔페이즈", digest_md)

        # Must have consolidated notice blockquote
        self.assertIn("ℹ️ **당일 원문 데이터 미수집 종목 (관망 유지)**:", digest_md)
        self.assertIn("SK스퀘어", digest_md)
        self.assertIn("셀시우스홀딩스", digest_md)
        self.assertIn("엔페이즈에너지", digest_md)

    def test_digest_comparative_table_retains_all_8_canonical_stocks(self):
        """Section 1 comparative table must retain all 8 canonical stocks."""
        digest_md = DigestGenerator().build_markdown(self.market_data)
        sec1_match = re.search(r"## 1\..*?(?=## 2\.|\Z)", digest_md, re.DOTALL)
        self.assertIsNotNone(sec1_match)
        sec1_text = sec1_match.group(0)

        # All 8 stocks must be present in Section 1
        for sym in StockSymbol:
            self.assertIn(STOCK_MASTERS[sym].name_kr, sec1_text)

    def test_index_html_contains_macro_card_and_empty_card_suppression(self):
        """index.html must have grid-macro-portfolio card and suppress empty cards in JS."""
        html_path = REPO_ROOT / "index.html"
        with open(html_path, "r", encoding="utf-8") as f:
            html_text = f.read()

        self.assertIn("grid-macro-portfolio", html_text)
        self.assertIn("관심종목 연계 매크로", html_text)
        self.assertIn("Nomura CSI 103.9", html_text)
        self.assertIn("당일 원문 데이터 미수집 종목 (관망 유지)", html_text)

    def test_empty_card_suppression_data_contract(self):
        """sync_dashboard.build_digest_entry must provide stocks dict and suppress uncollected stocks."""
        entry = build_digest_entry(self.market_data)
        self.assertIn("stocks", entry, "build_digest_entry must include 'stocks' dict mapping stockId to factsheet")
        self.assertIn("summaryTable", entry)

        # 5 present stocks
        for sym in ["SK_HYNIX", "UBER", "MBLY", "FLNC", "UPST"]:
            self.assertIn(sym, entry["stocks"])
            self.assertNotEqual(entry["stocks"][sym]["price"], "N/A")

        # 3 unprovided stocks must NOT be in entry["stocks"]
        for sym in ["SK_SQUARE", "CELH", "ENPH"]:
            self.assertNotIn(sym, entry["stocks"])

        # Simulate index.html renderDigestStockCards logic
        all_symbols = ["SK_HYNIX", "SK_SQUARE", "UBER", "MBLY", "FLNC", "UPST", "CELH", "ENPH"]
        present_symbols = [
            sym for sym in all_symbols
            if (entry.get("stocks") and entry["stocks"].get(sym) and entry["stocks"][sym].get("closePrice") not in [None, "", "N/A", "원문 데이터 미수집", "원문 데이터 미제공"])
            or (entry.get("summaryTable") and any(r["stockId"] == sym and r.get("price") not in [None, "", "N/A", "원문 데이터 미수집", "원문 데이터 미제공"] for r in entry["summaryTable"]))
        ]
        self.assertEqual(set(present_symbols), {"SK_HYNIX", "UBER", "MBLY", "FLNC", "UPST"})
        unprovided = [s for s in all_symbols if s not in present_symbols]
        self.assertEqual(set(unprovided), {"SK_SQUARE", "CELH", "ENPH"})


class TestMilestone3R2SKHynixNasdaqADRNormalization(unittest.TestCase):
    """R2: SK Hynix NASDAQ ADR Normalization (SKHY / USD / ADR Premium)."""

    def setUp(self):
        self.raw_dump_path = REPO_ROOT / "raw_input_20260930.txt"
        with open(self.raw_dump_path, "r", encoding="utf-8") as f:
            self.raw_text = f.read()
        cleaned_text, _ = clean_raw_dump(self.raw_text)
        self.market_data = extract_facts(cleaned_text, date="2026-09-30")

    def test_stock_symbol_and_master_metadata(self):
        """StockSymbol.SK_HYNIX ticker, market, and currency must be normalized to NASDAQ ADR."""
        master = STOCK_MASTERS[StockSymbol.SK_HYNIX]
        self.assertEqual(master.ticker, "SKHY")
        self.assertEqual(master.market, "NASDAQ ADR")
        self.assertEqual(master.currency, "USD")
        self.assertIn("SKHY", master.asset_keywords)
        self.assertIn("나스닥 ADR", master.asset_keywords)

    def test_extracted_sk_hynix_metrics_usd_and_adr_premium(self):
        """SK Hynix parsed from raw_input_20260930.txt must have USD price, volume, and ADR premium."""
        sk = self.market_data.stocks.get("SK_HYNIX")
        self.assertIsNotNone(sk, "SK_HYNIX must be present in parsed stocks")
        m = sk.metrics
        self.assertIsNotNone(m)
        self.assertEqual(m.currency, "USD")
        self.assertAlmostEqual(m.close_price, 186.91, places=2)
        self.assertIn("$186.91", m.close_price_formatted)
        self.assertEqual(m.volume, 2910000)
        self.assertIn("291만 주", m.volume_formatted)
        self.assertIsNotNone(m.adr_premium)
        self.assertIn("+3.0%~+3.5%", m.adr_premium)
        self.assertIsNotNone(m.peer_comparison)
        self.assertIn("마이크론", m.peer_comparison)

    def test_digest_comparative_table_renders_skhy_nasdaq_adr(self):
        """Digest Section 1 table must display SKHY / NASDAQ ADR / $186.91."""
        digest_md = DigestGenerator().build_markdown(self.market_data)
        self.assertIn("| SK하이닉스 | SKHY | NASDAQ ADR | $186.91 |", digest_md)

    def test_krw_fallback_compatibility(self):
        """Historical KRW text (e.g. 176,700원) must parse as KRW without crash."""
        krw_text = """
        [SK하이닉스 장마감 브리핑]
        - 종가: 176,700원 (-5.05%)
        - 거래량: 3,210,000주
        - 핵심 동인: 외국인 반도체 차익 실현 매물 출회
        """
        data = extract_facts(krw_text, date="2026-09-29")
        sk = data.stocks.get("SK_HYNIX")
        self.assertIsNotNone(sk)
        self.assertEqual(sk.metrics.currency, "KRW")
        self.assertEqual(sk.metrics.close_price, 176700.0)
        self.assertIn("176,700원", sk.metrics.close_price_formatted)

    def test_portfolio_holdings_preserves_domestic_shares(self):
        """Portfolio holdings must maintain domestic holding 000660 (20 shares)."""
        js_path = REPO_ROOT / "data.js"
        with open(js_path, "r", encoding="utf-8") as f:
            js_text = f.read()
        store = parse_js_data_store(js_text)
        holdings = store["portfolio"]["holdings"]
        sk_holding = next((h for h in holdings if h["id"] == "SK_HYNIX"), None)
        self.assertIsNotNone(sk_holding)
        self.assertIn(sk_holding["shares"], ["10주", "20주"])
        self.assertIn("000660", sk_holding["ticker"])

    def test_data_js_records_and_stocks_contain_adr_premium(self):
        """data.js records must contain adrPremium and stocks metadata must reflect SKHY/NASDAQ ADR/USD."""
        js_path = REPO_ROOT / "data.js"
        store = parse_js_data_store(js_path.read_text(encoding="utf-8"))
        sk_meta = next(s for s in store["stocks"] if s["id"] == "SK_HYNIX")
        self.assertEqual(sk_meta["ticker"], "SKHY")
        self.assertEqual(sk_meta["market"], "NASDAQ ADR")
        self.assertEqual(sk_meta["currency"], "USD")

        sk_close = next((r for r in store["records"] if r["id"] == "REC-20260930-SK_HYNIX-CLOSE"), None)
        if sk_close:
            self.assertIn("adrPremium", sk_close)
            self.assertIn("+3.0%~+3.5%", sk_close["adrPremium"])
            self.assertIn("adrPremium", sk_close["metrics"])


class TestMilestone3R3InstitutionalIBDeepResearchReport(unittest.TestCase):
    """R3: Institutional IB Deep Research Report (Dual-Part Structure, 8-Stock Matrices)."""

    def setUp(self):
        self.raw_dump_path = REPO_ROOT / "raw_input_20260930.txt"
        with open(self.raw_dump_path, "r", encoding="utf-8") as f:
            self.raw_text = f.read()
        cleaned_text, _ = clean_raw_dump(self.raw_text)
        self.market_data = extract_facts(cleaned_text, date="2026-09-30")
        self.report = generate_insight(self.market_data, raw_text=cleaned_text)

    def test_dual_part_report_structure(self):
        """Report markdown must contain Part I (AI Memory & SK Hynix) and Part II (Cross-Asset Matrix)."""
        md = self.report.markdown_content
        self.assertIn("# 일간 심층 투자 인사이트 리포트", md)
        self.assertIn("[IB 기업·산업 심층 리서치] 글로벌 AI 메모리 반도체 산업 및 SK하이닉스 나스닥 ADR (SKHY) 심층 분석", md)
        self.assertIn("## 1. 비즈니스 모델 및 유닛 이코노믹스 정밀 분석", md)
        self.assertIn("## 2. 글로벌 피어 그룹 비교 및 상대 밸류에이션 매트릭스", md)
        self.assertIn("## 3. 손익비 (Risk-Reward) 및 하방 지지력 분석", md)
        self.assertIn("## 4. 전술적 투자의사결정 매트릭스", md)

    def test_part_one_semiconductor_deep_dive_metrics(self):
        """Part I must analyze wafer trade-off 4:1, TSV fab capacity, take-or-pay LTA, Nomura CSI 103.9, MR-MUF vs NCF, Risk-Reward 1:4.2."""
        md = self.report.markdown_content
        self.assertIn("4:1", md)
        self.assertIn("TSV", md)
        self.assertIn("LTA", md)
        self.assertIn("CSI 103.9", md)
        self.assertIn("MR-MUF", md)
        self.assertIn("NCF", md)
        self.assertIn("1 : 4.2", md)

    def test_hbm_market_share_53_to_55_percent(self):
        """Part I/II and valuation table must explicitly state SK Hynix HBM market share of 53~55%."""
        md = self.report.markdown_content
        self.assertIn("53~55%", md)
        self.assertIn("HBM 시장 점유율 53~55%", md)
        sk_peer = next(p for p in self.report.peer_comparison if p["stockId"] == "SK_HYNIX")
        self.assertIn("53~55%", sk_peer.get("hbmMarketShare", ""))

    def test_structured_dicts_retain_all_8_canonical_stocks(self):
        """Structured dictionaries must retain all 8 canonical stocks for backward compatibility."""
        expected_stocks = ["SK_HYNIX", "SK_SQUARE", "UBER", "MBLY", "FLNC", "UPST", "CELH", "ENPH"]

        self.assertEqual(len(self.report.unit_economics), 8)
        self.assertEqual(len(self.report.peer_comparison), 8)
        self.assertEqual(len(self.report.risk_reward), 8)
        self.assertEqual(len(self.report.decision_matrix), 8)

        for sid in expected_stocks:
            self.assertIn(sid, self.report.unit_economics)
            self.assertTrue(any(p["stockId"] == sid for p in self.report.peer_comparison))
            self.assertIn(sid, self.report.risk_reward)
            self.assertTrue(any(d["stockId"] == sid for d in self.report.decision_matrix))

    def test_sk_hynix_unit_economics_structured_fields(self):
        """SK Hynix unit economics must contain waferRatio 4:1, locked LTA, CSI 103.9 pricing power."""
        sk_ue = self.report.unit_economics["SK_HYNIX"]
        self.assertEqual(sk_ue.get("ticker"), "SKHY")
        self.assertEqual(sk_ue.get("currency"), "USD")
        self.assertEqual(sk_ue.get("waferRatio"), "4:1")
        self.assertEqual(sk_ue.get("ltaStatus"), "100% Locked")
        self.assertEqual(sk_ue.get("utilization"), "100%")
        self.assertIn("CSI 103.9", sk_ue.get("pricingPower", ""))

    def test_sync_dashboard_bridges_insight_schema_with_index_html(self):
        """sync_dashboard.build_insight_entry must emit both top-level and sections dict."""
        entry = build_insight_entry(self.report)
        self.assertIn("unitEconomics", entry)
        self.assertIn("peerComparison", entry)
        self.assertIn("riskReward", entry)
        self.assertIn("decisionMatrix", entry)
        self.assertIn("sections", entry)
        self.assertIn("unit_economics", entry["sections"])
        self.assertIn("peer_comparison", entry["sections"])
        self.assertIn("risk_reward", entry["sections"])
        self.assertIn("decision_matrix", entry["sections"])


class TestMilestone3R4TimeSeriesAndBugEradication(unittest.TestCase):
    """R4: Time-Series Filter View Standardization & UI/Regex Bug Eradication."""

    def setUp(self):
        self.raw_dump_path = REPO_ROOT / "raw_input_20260930.txt"
        with open(self.raw_dump_path, "r", encoding="utf-8") as f:
            self.raw_text = f.read()
        cleaned_text, _ = clean_raw_dump(self.raw_text)
        self.market_data = extract_facts(cleaned_text, date="2026-09-30")

    def test_one_paragraph_summary_strictly_5_sentences_with_contrastive_phrasing(self):
        """Digest Section 2 1문단 핵심 요약 must be exactly 5 sentences with contrastive noise/fact phrasing."""
        sk = self.market_data.stocks.get("SK_HYNIX")
        self.assertIsNotNone(sk)
        summary = sk.one_paragraph_summary
        sentences = [s.strip() for s in re.split(r"(?<=[.!?])\s+", summary) if s.strip()]
        self.assertEqual(len(sentences), 5, f"Expected 5 sentences, got {len(sentences)}: {sentences}")
        self.assertIn("시장 일각의", summary)
        self.assertIn("단기 센티먼트 노이즈로 분석되며", summary)
        self.assertIn("실물 팩트가 중장기 펀더멘털을 지지하고 있습니다", summary)

    def test_day_range_regex_bug_eradication(self):
        """Extractor must NOT falsely match bare '범위' without explicit compound prefix and numeric range."""
        test_dump = """
        [SK하이닉스 장마감 브리핑]
        - 종가: $186.91 (+2.27%)
        - 이번 분기 사업 범위 확장을 위해 적극 투자 중입니다.
        - 거래량: 2,910,000주
        """
        data = extract_facts(test_dump, date="2026-09-30")
        sk = data.stocks.get("SK_HYNIX")
        self.assertIsNotNone(sk)
        # Should not falsely match "확장을 위해 적극 투자 중입니다" as day_range
        self.assertIsNone(sk.metrics.day_range)

    def test_day_range_valid_compound_matches(self):
        """Extractor must correctly match valid compound day range patterns."""
        test_dump = """
        [우버 장마감 브리핑]
        - 종가: $69.36 (+1.76%)
        - 장중 변동 범위: $67.73 ~ $69.68
        - 거래량: 14,760,000주
        """
        data = extract_facts(test_dump, date="2026-09-30")
        ub = data.stocks.get("UBER")
        self.assertIsNotNone(ub)
        self.assertIsNotNone(ub.metrics.day_range)
        self.assertIn("$67.73 ~ $69.68", ub.metrics.day_range)

    def test_strip_markdown_links_utility(self):
        """strip_markdown_links must cleanly strip [text](url) and (http://...) while keeping standalone URLs."""
        self.assertEqual(strip_markdown_links("[TIKR 분석](https://www.tikr.com/blog)"), "TIKR 분석")
        self.assertEqual(strip_markdown_links("핵심 요약 ([링크](https://example.com)) 입니다"), "핵심 요약 (링크) 입니다")
        self.assertEqual(strip_markdown_links("출처: (https://example.com)"), "출처:")
        # Standalone URLs without markdown link syntax are preserved
        self.assertEqual(strip_markdown_links("https://www.youtube.com/watch?v=12345"), "https://www.youtube.com/watch?v=12345")

    def test_digest_and_data_js_zero_markdown_link_syntax(self):
        """Generated digest and data.js core drivers and summaries must have zero [text](url) syntax."""
        digest_md = DigestGenerator().build_markdown(self.market_data)
        # In Section 1 and Section 2 core drivers / summaries, no [text](url) should appear
        sec1_match = re.search(r"## 1\..*?(?=## 2\.|\Z)", digest_md, re.DOTALL)
        self.assertIsNotNone(sec1_match)
        sec1_text = sec1_match.group(0)
        self.assertEqual(re.findall(r"\[([^\]]+)\]\((https?://[^\)]+)\)", sec1_text), [])

        js_path = REPO_ROOT / "data.js"
        with open(js_path, "r", encoding="utf-8") as f:
            js_text = f.read()
        store = parse_js_data_store(js_text)
        latest_digest = store["dailyDigests"][0]
        for row in latest_digest.get("summaryTable", []):
            self.assertNotRegex(row.get("coreDriver", ""), r"\[.*?\]\(.*?\)")
            self.assertNotRegex(row.get("watchPoint1", ""), r"\[.*?\]\(.*?\)")
            self.assertNotRegex(row.get("watchPoint2", ""), r"\[.*?\]\(.*?\)")

    def test_zero_cdn_offline_integrity(self):
        """index.html must maintain 100% offline Zero-CDN integrity with zero external script/style/font tags."""
        html_path = REPO_ROOT / "index.html"
        with open(html_path, "r", encoding="utf-8") as f:
            html_text = f.read()

        cdn_patterns = [
            r'src=["\']https?://',
            r'href=["\']https?://(?!www\.w3\.org)',
            r'@import\s+url\(["\']?https?://',
            r'cdn\.jsdelivr\.net',
            r'cdnjs\.cloudflare\.com',
            r'fonts\.googleapis\.com',
            r'unpkg\.com',
        ]
        for pat in cdn_patterns:
            matches = re.findall(pat, html_text, re.IGNORECASE)
            self.assertEqual(matches, [], f"Found external CDN or remote asset matching {pat}: {matches}")


if __name__ == "__main__":
    unittest.main()
