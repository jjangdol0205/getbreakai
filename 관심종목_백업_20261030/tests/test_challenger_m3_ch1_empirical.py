"""Milestone 3 Gate Adversarial Stress-Testing Suite by Challenger 1.

Targets:
1. Adversarial Range Regex: Non-numeric sentences with '범위' rejected, numeric ranges preserved.
2. Adversarial Markdown Link Leak: Nested, malformed, and multiple links sanitized in titles, drivers, summaries.
3. Adversarial Currency & ADR: SK Hynix NASDAQ ADR quote normalization vs KRW domestic fallback.
4. Adversarial Empty Dump: Zero/partial stocks handling, Section 2 card suppression, Section 1 table integrity.
"""

from __future__ import annotations

import re
import unittest
from pathlib import Path
from typing import Any, Dict, List

from engine.cleaner import strip_markdown_links, clean_raw_dump
from engine.extractor import extract_facts, FactExtractor, STANDARDIZED_STRATEGIST_IMPLICATIONS
from engine.models import StockSymbol, STOCK_MASTERS, DailyMarketData
from engine.digest_generator import generate_digest, DigestGenerator
from engine.sync_dashboard import (
    generate_records_for_market_data,
    build_digest_entry,
    create_default_data_store,
)

REPO_ROOT = Path(__file__).resolve().parent.parent


class TestAdversarialRangeRegex(unittest.TestCase):
    """Probes extractor day_range regex against adversarial prose containing '범위'."""

    def test_non_numeric_sentences_with_range_keyword_strictly_none(self):
        """Verifies day_range is NEVER populated from prose sentences containing '범위'."""
        adversarial_sentences = [
            "양사 간의 기술 공유 범위가 불명확하다는 지적도 상존합니다.",
            "트래킹 범위\n분기 실적 발표 전까지 관망세를 권고합니다.",
            "외국계 IB 범위:\n골드만삭스 및 모건스탠리 리포트 참조.",
            "적용 범위: 전사적 사업 부문 구조조정 진행 중.",
            "가격 범위: 골드만삭스 리포트 목표가 제시 및 관망.",
            "52주 변동 범위: 분석 중이며 데이터 미집계 상태입니다.",
            "장중 변동 범위: 미정 (데이터 집계 중)",
            "가격 범위: 불명확한 시장 루머에 유의할 필요가 있습니다.",
            "일중 범위: 발표 대기 중",
            "Trading Range: TBD pending earnings report",
            "Day's Range: N/A due to trading halt",
        ]

        for idx, sentence in enumerate(adversarial_sentences, 1):
            raw_text = f"""
            [우버 장마감 브리핑]
            - 종가: $69.36 (+1.76%)
            - {sentence}
            - 거래량: 14,760,000주
            """
            data = extract_facts(raw_text, date="2026-09-30")
            ub = data.stocks.get("UBER")
            self.assertIsNotNone(ub, f"Case {idx}: Stock UBER must be parsed")
            self.assertIsNone(
                ub.metrics.day_range,
                f"Case {idx} FAILED: Non-numeric text '{sentence}' was falsely parsed as day_range: '{ub.metrics.day_range}'"
            )

    def test_valid_numeric_day_ranges_correctly_extracted(self):
        """Verifies legitimate numeric day range formats are accurately extracted."""
        valid_cases = [
            ("장중 변동 범위: $67.73 ~ $69.68", "$67.73 ~ $69.68"),
            ("장중 변동 범위: $67.73 - $69.68", "$67.73 - $69.68"),
            ("Day's Range: 180.50 - 188.20 USD", "180.50 - 188.20 USD"),
            ("일중 범위: 175,000원 ~ 182,000원", "175,000원 ~ 182,000원"),
            ("52주 변동 범위: $52.50 ~ $85.00", "$52.50 ~ $85.00"),
            ("Trading Range: 65.50 - 70.20", "65.50 - 70.20"),
            ("장중 고가: $70.50, 저가: $66.20", None),  # Compound without colon range
        ]

        for text_line, expected in valid_cases:
            raw_text = f"""
            [우버 장마감 브리핑]
            - 종가: $69.36 (+1.76%)
            - {text_line}
            - 거래량: 14,760,000주
            """
            data = extract_facts(raw_text, date="2026-09-30")
            ub = data.stocks.get("UBER")
            self.assertIsNotNone(ub)
            if expected:
                self.assertIsNotNone(ub.metrics.day_range, f"Failed to extract valid range from '{text_line}'")
                self.assertIn(expected, ub.metrics.day_range)
                # Verify numeric presence
                self.assertTrue(any(c.isdigit() for c in ub.metrics.day_range))
                # Verify no prose corruption
                for bad in ["불명확", "상존", "범위가", "부근", "발표", "골드만삭스"]:
                    self.assertNotIn(bad, ub.metrics.day_range)

    def test_dashboard_sync_rejects_corrupted_range(self):
        """Verifies dashboard record generator strictly rejects corrupted ranges."""
        raw_text = """
        [우버 장마감 브리핑]
        - 종가: $69.36 (+1.76%)
        - 장중 변동 범위: 불명확하다는 지적도 상존합니다.
        - 거래량: 14,760,000주
        """
        data = extract_facts(raw_text, date="2026-09-30")
        records = generate_records_for_market_data(data)
        ub_record = next((r for r in records if r["stockId"] == "UBER" and r["type"] == "DAILY_CLOSE"), None)
        self.assertIsNotNone(ub_record)
        self.assertNotIn("range", ub_record["metrics"], "Corrupted range must not be present in dashboard metrics")


class TestAdversarialMarkdownLinkLeak(unittest.TestCase):
    """Probes markdown link stripper and fact extractor against adversarial link syntax."""

    def test_strip_markdown_links_adversarial_patterns(self):
        """Stress-tests strip_markdown_links utility across malformed, multiple, and nested link inputs."""
        cases = [
            # Standard single link
            ("[TIKR 분석](https://www.tikr.com/blog)", "TIKR 분석"),
            # Multiple links in single sentence
            ("[TIKR 분석](https://tikr.com) 및 [Seeking Alpha](https://seekingalpha.com) 리포트", "TIKR 분석 및 Seeking Alpha 리포트"),
            # Link with query parameters and hash
            ("[DART 공시](https://dart.fss.or.kr/dsaf001/main.do?rcpNo=202609300001#target)", "DART 공시"),
            # Parenthesized raw URL
            ("참고 리포트 (https://example.com/report.pdf)", "참고 리포트"),
            # Empty parentheses cleanup
            ("핵심 요약 (  ) 발언", "핵심 요약 발언"),
            # Leading bullet and punctuation artifacts
            ("- . [분석](https://test.com)", "분석"),
            # Link with internal quotes
            ('[참고 "자료"](https://test.com)', '참고 "자료"'),
            # Multiple Korean links
            ("[텍스트](http://url1.com) 및 [텍스트2](http://url2.com)", "텍스트 및 텍스트2"),
        ]

        for input_text, expected_substring in cases:
            cleaned = strip_markdown_links(input_text)
            self.assertNotIn("](http", cleaned, f"Markdown URL leak in '{cleaned}' from '{input_text}'")
            self.assertIn(expected_substring, cleaned, f"Expected '{expected_substring}' in '{cleaned}'")

    def test_extractor_driver_and_summary_strip_markdown_links(self):
        """Verifies extractor driver, fact/noise, and summary never leak [text](url)."""
        adversarial_dump = """
        [우버 장마감 브리핑]
        - 종가: $69.36 (+1.76%)
        - 거래량: 14,760,000주
        - 주요 동인: [TIKR 분석](https://tikr.com/uber) 및 [Seeking Alpha](https://seekingalpha.com/article/123) 로보택시 상용화 가속
        - 공시 팩트: [웨이모 파트너십](https://waymo.com) 공식 계약 체결
        - 시장 노이즈: [블룸버그 루머](https://bloomberg.com) 규제 우려는 단순 노이즈
        - 포트폴리오 영향: [골드만삭스 포트폴리오](https://gs.com) 비중 15% 유지 권고
        """
        data = extract_facts(adversarial_dump, date="2026-09-30")
        ub = data.stocks.get("UBER")
        self.assertIsNotNone(ub)

        # Check core_drivers
        for d in ub.core_drivers:
            self.assertNotRegex(d, r"\[.*?\]\(https?://.*?\)", f"Driver contains markdown link: {d}")

        # Check structured_drivers
        for sd in ub.structured_drivers:
            self.assertNotRegex(sd.title, r"\[.*?\]\(https?://.*?\)", f"SD title contains markdown link: {sd.title}")
            self.assertNotRegex(sd.headline_summary, r"\[.*?\]\(https?://.*?\)", f"SD headline contains markdown link: {sd.headline_summary}")

        # Check one_paragraph_summary
        self.assertNotRegex(ub.one_paragraph_summary, r"\[.*?\]\(https?://.*?\)", f"Summary contains markdown link: {ub.one_paragraph_summary}")

        # Check portfolio_impact
        self.assertNotRegex(ub.portfolio_impact, r"\[.*?\]\(https?://.*?\)", f"Portfolio impact contains markdown link: {ub.portfolio_impact}")

    def test_dashboard_records_zero_markdown_link_leak(self):
        """Verifies generate_records_for_market_data outputs zero raw markdown links in titles, summaries, watch points."""
        adversarial_dump = """
        [모빌아이 장마감 브리핑]
        - 종가: $7.44 (-1.33%)
        - 거래량: 4,890,000주
        - 주요 동인: [인텔 지분 매각](https://intel.com/news) 오버행 우려로 단기 변동성 확대
        - Line 1: [단기 지지선](https://support.com) $7.00~$7.50 지지력 확인
        - Line 2: [차기 실적](https://earnings.com) EyeQ6 양산 일정 확인
        """
        data = extract_facts(adversarial_dump, date="2026-09-30")
        records = generate_records_for_market_data(data)
        mbly_rec = next((r for r in records if r["stockId"] == "MBLY" and r["type"] == "DAILY_CLOSE"), None)
        self.assertIsNotNone(mbly_rec)

        self.assertNotRegex(mbly_rec["title"], r"\[.*?\]\(https?://.*?\)")
        self.assertNotRegex(mbly_rec["summary"], r"\[.*?\]\(https?://.*?\)")
        self.assertNotRegex(mbly_rec["oneParagraphSummary"], r"\[.*?\]\(https?://.*?\)")
        self.assertNotRegex(mbly_rec["watchPointLine1"], r"\[.*?\]\(https?://.*?\)")
        self.assertNotRegex(mbly_rec["watchPointLine2"], r"\[.*?\]\(https?://.*?\)")

    def test_digest_markdown_table_and_cards_zero_link_leak(self):
        """Verifies daily digest markdown Section 1 and Section 2 contain zero raw markdown links in drivers/titles."""
        adversarial_dump = """
        [우버 장마감 브리핑]
        - 종가: $69.36 (+1.76%)
        - 거래량: 14,760,000주
        - 주요 동인: [TIKR 분석](https://tikr.com) 자율주행 모빌리티 확대
        """
        data = extract_facts(adversarial_dump, date="2026-09-30")
        digest_md = DigestGenerator().build_markdown(data)

        # Check Section 1 table
        sec1_match = re.search(r"## 1\..*?(?=## 2\.|\Z)", digest_md, re.DOTALL)
        self.assertIsNotNone(sec1_match)
        sec1_text = sec1_match.group(0)
        self.assertEqual(re.findall(r"\[([^\]]+)\]\((https?://[^\)]+)\)", sec1_text), [])

        # Check Section 2 cards
        sec2_match = re.search(r"## 2\..*?(?=## 3\.|\Z)", digest_md, re.DOTALL)
        self.assertIsNotNone(sec2_match)
        sec2_text = sec2_match.group(0)
        self.assertEqual(re.findall(r"\[([^\]]+)\]\((https?://[^\)]+)\)", sec2_text), [])


class TestAdversarialCurrencyAndADR(unittest.TestCase):
    """Probes SK Hynix NASDAQ ADR (SKHY/USD) normalization and KRW fallback resilience."""

    def test_sk_hynix_parses_usd_adr_quote_and_premium(self):
        """SK Hynix with USD ADR quotes must parse ticker SKHY, USD, $186.91, and premium."""
        # Test with Korean '만' volume notation
        adr_dump_man = """
        [SK하이닉스 장마감 브리핑]
        - 종가: $186.91 (+2.27%)
        - 거래량: 291만 주
        - ADR 프리미엄: +3.0%~+3.5% (원주 대비)
        - 주요 동인: 나스닥 ADR 상장 프리미엄 유지 및 마이크론(MU) +1.74% 동반 상승
        """
        data_man = extract_facts(adr_dump_man, date="2026-09-30")
        sk_man = data_man.stocks.get("SK_HYNIX")
        self.assertIsNotNone(sk_man)
        m_man = sk_man.metrics
        self.assertEqual(m_man.currency, "USD")
        self.assertAlmostEqual(m_man.close_price, 186.91, places=2)
        self.assertEqual(m_man.close_price_formatted, "$186.91")
        self.assertEqual(m_man.volume, 2910000)
        self.assertEqual(m_man.volume_formatted, "291만 주")
        self.assertIsNotNone(m_man.adr_premium)
        self.assertIn("+3.0%~+3.5%", m_man.adr_premium)
        self.assertIsNotNone(m_man.peer_comparison)
        self.assertIn("마이크론(MU)", m_man.peer_comparison)

        # Also test with raw integer volume notation (2,910,000주)
        adr_dump_raw = """
        [SK하이닉스 장마감 브리핑]
        - 종가: $186.91 (+2.27%)
        - 거래량: 2,910,000주
        """
        data_raw = extract_facts(adr_dump_raw, date="2026-09-30")
        sk_raw = data_raw.stocks.get("SK_HYNIX")
        self.assertEqual(sk_raw.metrics.volume, 2910000)
        self.assertEqual(sk_raw.metrics.volume_formatted, "2,910,000주")

        # Check Digest Section 1 display
        digest_md = DigestGenerator().build_markdown(data_man)
        self.assertIn("| SK하이닉스 | SKHY | NASDAQ ADR | $186.91 |", digest_md)

        # Check Dashboard records
        records = generate_records_for_market_data(data_man)
        sk_rec = next((r for r in records if r["stockId"] == "SK_HYNIX" and r["type"] == "DAILY_CLOSE"), None)
        self.assertIsNotNone(sk_rec)
        self.assertEqual(sk_rec["ticker"], "SKHY")
        self.assertEqual(sk_rec["source"], "NASDAQ ADR 정규장 마감")
        self.assertEqual(sk_rec["metrics"]["price"], "$186.91")

    def test_sk_hynix_krw_domestic_fallback_preservation(self):
        """SK Hynix with KRW domestic price must parse KRW, 176,700원, without crash."""
        krw_dump = """
        [SK하이닉스 장마감 브리핑]
        - 종가: 176,700원 (-5.05%)
        - 거래량: 3,210,000주
        - 주요 동인: 외국인 반도체 대규모 차익 실현 매물 출회
        """
        data = extract_facts(krw_dump, date="2026-09-29")
        sk = data.stocks.get("SK_HYNIX")
        self.assertIsNotNone(sk)
        m = sk.metrics
        self.assertIsNotNone(m)
        self.assertEqual(m.currency, "KRW")
        self.assertEqual(m.close_price, 176700.0)
        self.assertEqual(m.close_price_formatted, "176,700원")
        self.assertEqual(m.volume, 3210000)

        # Digest Section 1 must display 000660 / KRX / 176,700원 when KRW
        digest_md = DigestGenerator().build_markdown(data)
        self.assertIn("| SK하이닉스 | 000660 | KRX | 176,700원 |", digest_md)

        # Dashboard records must reflect KRX and 000660
        records = generate_records_for_market_data(data)
        sk_rec = next((r for r in records if r["stockId"] == "SK_HYNIX" and r["type"] == "DAILY_CLOSE"), None)
        self.assertIsNotNone(sk_rec)
        self.assertEqual(sk_rec["ticker"], "000660")
        self.assertEqual(sk_rec["source"], "KRX 정규장 마감")
        self.assertEqual(sk_rec["metrics"]["price"], "176,700원")

    def test_sk_hynix_mixed_mention_prioritizes_adr_quote(self):
        """When text contains both domestic reference and ADR quote, USD ADR quote is prioritized."""
        mixed_dump = """
        [SK하이닉스 나스닥 ADR 장마감 브리핑]
        - 종가: $186.91 (+2.27%)
        - 국내 원주 175,000원 대비 약 3.2% 프리미엄 형성
        - 거래량: 2,910,000주
        """
        data = extract_facts(mixed_dump, date="2026-09-30")
        sk = data.stocks.get("SK_HYNIX")
        self.assertIsNotNone(sk)
        self.assertEqual(sk.metrics.currency, "USD")
        self.assertAlmostEqual(sk.metrics.close_price, 186.91, places=2)


class TestAdversarialEmptyDump(unittest.TestCase):
    """Probes behavior under empty, partial, and omitted stock dumps."""

    def test_completely_empty_text_dump(self):
        """Completely empty dump text must not crash extractor, digest generator, or dashboard sync."""
        data = extract_facts("", date="2026-09-30")
        self.assertEqual(len(data.stocks), 0)

        # Digest generation must not crash
        digest_md = DigestGenerator().build_markdown(data)
        self.assertIn("종합 다이제스트", digest_md)
        self.assertIn("### 🌐 관심종목 연계 매크로 & 산업 핵심 동향", digest_md)

        # Section 1 table must retain all 8 canonical stocks with N/A
        sec1_match = re.search(r"## 1\..*?(?=## 2\.|\Z)", digest_md, re.DOTALL)
        self.assertIsNotNone(sec1_match)
        sec1_text = sec1_match.group(0)
        for sym in StockSymbol:
            self.assertIn(STOCK_MASTERS[sym].name_kr, sec1_text)

        # Section 1 table must have exact column integrity (8 columns per row)
        table_rows = [line.strip() for line in sec1_text.splitlines() if line.strip().startswith("|") and not line.strip().startswith("|---")]
        self.assertGreater(len(table_rows), 1, "Must contain header and data rows")
        for row in table_rows:
            pipes = row.count("|")
            self.assertEqual(pipes, 9, f"Row must have 8 columns (9 pipes): '{row}'")

        # Dashboard record generation must produce zero stock close records
        records = generate_records_for_market_data(data)
        stock_close_records = [r for r in records if r["type"] == "DAILY_CLOSE"]
        self.assertEqual(stock_close_records, [], "No DAILY_CLOSE records should be generated for empty dump")

    def test_single_stock_dump_suppresses_remaining_7_cards(self):
        """Dump with only 1 stock (UBER) must ONLY render UBER card in Section 2, suppressing other 7."""
        uber_only_dump = """
        [우버 장마감 브리핑]
        - 종가: $69.36 (+1.76%)
        - 거래량: 14,760,000주
        - 주요 동인: 자율주행 파트너십 상용화 가속
        - Line 1: $65.00~$68.00 주요 지지선
        - Line 2: 웨이모/웨이브 플랫폼 파트너십 상용 확대
        """
        data = extract_facts(uber_only_dump, date="2026-09-30")
        self.assertEqual(len(data.stocks), 1)
        self.assertIn("UBER", data.stocks)

        digest_md = DigestGenerator().build_markdown(data)

        # Section 2 must have UBER card
        self.assertIn("### 📌 우버", digest_md)

        # Section 2 must NOT have cards for unprovided stocks
        unprovided = [s for s in StockSymbol if s != StockSymbol.UBER]
        for s in unprovided:
            m = STOCK_MASTERS[s]
            self.assertNotIn(f"### 📌 {m.name_kr}", digest_md)

        # Must have consolidated notice blockquote for the 7 unprovided stocks
        self.assertIn("ℹ️ **당일 원문 데이터 미수집 종목 (관망 유지)**:", digest_md)
        for s in unprovided:
            self.assertIn(STOCK_MASTERS[s].name_kr, digest_md)

        # Section 1 table must maintain 8 canonical rows with exact 8 columns
        sec1_match = re.search(r"## 1\..*?(?=## 2\.|\Z)", digest_md, re.DOTALL)
        self.assertIsNotNone(sec1_match)
        table_rows = [line.strip() for line in sec1_match.group(0).splitlines() if line.strip().startswith("|") and not line.strip().startswith("|---")]
        # 1 header + 8 stock rows = 9 rows
        self.assertEqual(len(table_rows), 9, f"Expected 9 table rows (1 header + 8 stocks), got {len(table_rows)}")
        for r in table_rows:
            self.assertEqual(r.count("|"), 9, f"Row must have 8 columns (9 pipes): '{r}'")

    def test_five_stock_dump_suppresses_3_cards(self):
        """Dump with 5 stocks (SKHY, UBER, MBLY, FLNC, UPST) must suppress SK_SQUARE, CELH, ENPH."""
        raw_path = REPO_ROOT / "raw_input_20260930.txt"
        self.assertTrue(raw_path.exists())
        with open(raw_path, "r", encoding="utf-8") as f:
            raw_text = f.read()

        cleaned_text, _ = clean_raw_dump(raw_text)
        data = extract_facts(cleaned_text, date="2026-09-30")
        self.assertEqual(len(data.stocks), 5)

        digest_md = DigestGenerator().build_markdown(data)

        # 5 present stocks
        for sid in ["SK_HYNIX", "UBER", "MBLY", "FLNC", "UPST"]:
            name = STOCK_MASTERS[StockSymbol(sid)].name_kr
            self.assertIn(f"### 📌 {name}", digest_md)

        # 3 unprovided stocks must be absent from individual ### 📌 cards
        for sid in ["SK_SQUARE", "CELH", "ENPH"]:
            name = STOCK_MASTERS[StockSymbol(sid)].name_kr
            self.assertNotIn(f"### 📌 {name}", digest_md)

        # Consolidated notice box must list all 3 unprovided stocks
        self.assertIn("SK스퀘어", digest_md)
        self.assertIn("셀시우스홀딩스", digest_md)
        self.assertIn("엔페이즈에너지", digest_md)

        # Section 1 table must have all 8 stocks
        sec1_match = re.search(r"## 1\..*?(?=## 2\.|\Z)", digest_md, re.DOTALL)
        table_rows = [line.strip() for line in sec1_match.group(0).splitlines() if line.strip().startswith("|") and not line.strip().startswith("|---")]
        self.assertEqual(len(table_rows), 9)


if __name__ == "__main__":
    unittest.main()
