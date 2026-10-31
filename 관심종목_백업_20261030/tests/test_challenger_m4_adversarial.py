"""Challenger M4 Empirical Adversarial Verification Suite.

Adversarial Stress Harness attacking:
1. Mutated Gemini sidebar titles (cleaner.py & extractor.py).
2. Tricky percentage & financial ratio masking (Gross Margin, YoY, QoQ, CAGR, Revenue Growth, Fee rate).
3. Inactive stock ghost-instantiation attacks (FLNC, UPST, CELH, ENPH).
4. Extreme payloads & stability (real 100k+ char dump, synthetic 500k+ char fuzzing).
5. Preservation of legitimate financial content, URLs, and interview quotes.
"""

from __future__ import annotations

from pathlib import Path
import re
import time
import unittest

ROOT_DIR = Path(__file__).resolve().parent.parent
RAW_INPUT_1001_PATH = ROOT_DIR / "raw_input_20261001.txt"

from engine.cleaner import RawDumpCleaner, clean_raw_dump, strip_markdown_links
from engine.extractor import FactExtractor, extract_facts
from engine.models import StockSymbol


class TestMutatedGeminiSidebarAttacks(unittest.TestCase):
    """Stress-tests cleaner.py with severely mutated and dirty Gemini sidebar titles."""

    def setUp(self) -> None:
        self.cleaner = RawDumpCleaner()

    def test_varied_date_formats_and_bullet_mutations(self) -> None:
        """Tests that canonical date styles and bullet symbols on sidebar entries are stripped."""
        mutated_sidebar_lines = [
            "- 2026년 9월 28일 플루언스에너지(FLNC) 주가 흐름을 분석함",
            "  * 2026년 9월 30일 SK 스퀘어 투자 분석 검토",
            "- 2026년 10월 1일 주요 AI 리더 인터뷰 추적",
            "- Ai 시대 이준이 교육 방안 모색",
            "- YouTube Video Content Analysis: AI and Autonomous Driving",
            "- SK 하이닉스 ADR 투자 분석 및 전망",
        ]
        raw_text = "\n".join(mutated_sidebar_lines) + "\n\nSK하이닉스 ADR($188.80) 정규장 마감."
        cleaned, meta = self.cleaner.clean_with_metadata(raw_text)

        self.assertNotIn("플루언스에너지(FLNC) 주가 흐름을 분석함", cleaned)
        self.assertNotIn("Ai 시대 이준이 교육", cleaned)
        self.assertNotIn("YouTube Video Content Analysis", cleaned)
        self.assertIn("SK하이닉스 ADR($188.80) 정규장 마감.", cleaned)

    def test_sidebar_with_tabs_and_irregular_spacing(self) -> None:
        """Tests tab-indented and space-padded sidebar entries."""
        raw = (
            "\t\t- 2026년 10월 1일 플루언스에너지 투자 분석 방안\n"
            "   •   업스타트홀딩스 투자 분석   \n"
            "\t- 인페이즈 에너지 기업 분석\n"
            "모빌아이 종가: $7.565 (-2.95%)\n"
        )
        cleaned = self.cleaner.clean(raw)
        self.assertNotIn("플루언스에너지 투자 분석 방안", cleaned)
        self.assertNotIn("인페이즈 에너지 기업 분석", cleaned)
        self.assertIn("모빌아이 종가: $7.565 (-2.95%)", cleaned)

    def test_empirical_sidebar_leak_on_non_korean_date_formats(self) -> None:
        """VERIFIED REMEDIATION: cleaner.py cleanly strips sidebar entries with dot, hyphen, or slash dates."""
        leaking_lines = [
            "• 2026. 10. 01. 모빌아이 투자 분석 리포트 확인",
            "▶ 2026/10/01 업스타트홀딩스 투자 분석 정보 요약",
            "▪ 2026-10-01 셀시우스 홀딩스 기업 분석 리포트",
        ]
        raw = "\n".join(leaking_lines) + "\n\nSK하이닉스 ADR 종가 $188.80\n"
        cleaned, _ = self.cleaner.clean_with_metadata(raw)

        has_leak = any(line.split()[-1] in cleaned for line in leaking_lines)
        self.assertFalse(
            has_leak,
            "Remediated: cleaner.py strips sidebar titles with non-Korean date formats (2026.10.01, 2026-10-01, 2026/10/01)",
        )

    def test_empirical_gemini_track_quotes_leak(self) -> None:
        """VERIFIED REMEDIATION: cleaner.py cleanly strips Track \"Stock Name\" developments lines."""
        line = 'Track "Celsius Holdings" developments is up to date.'
        raw = f"{line}\n\n우버 정규장 종가 $68.51 (-1.23%) 마감."
        cleaned, _ = self.cleaner.clean_with_metadata(raw)

        self.assertNotIn(
            line,
            cleaned,
            "Remediated: cleaner.py strips Track \"Stock Name\" lines cleanly",
        )


class TestTrickyPercentagesAndRatioMasking(unittest.TestCase):
    """Stress-tests extractor.py with financial ratios, margins, growth rates, and operational metrics."""

    def setUp(self) -> None:
        self.extractor = FactExtractor()

    def test_sk_square_not_polluted_by_micron_gpm_87_pct(self) -> None:
        """Verifies the specific patch worker made for GPM 87% in Micron call."""
        raw = """
## 1. SK스퀘어 (402340)
- 종가: 1,048,000원
- 등락률: -4.73%
- 거래량: 280,000주
- 주요 동인: 솔리다임 eSSD 가치 부각 및 자사주 소각 추진

## 2. 마이크론 FY4Q26 실적발표 컨퍼런스콜 Q&A
- 산제이 메흐로트라 CEO: "2026E 전체 HBM 및 고부가 메모리 GPM 87% 수준에 도달할 것으로 확신합니다."
- 낸드 ASP +30% 상승 및 영업이익률(OPM) 45.5% 달성.
"""
        cleaned = clean_raw_dump(raw)[0]
        data = self.extractor.extract(cleaned, date_override="2026-10-01")

        sq = data.stocks.get(StockSymbol.SK_SQUARE.value)
        self.assertIsNotNone(sq)
        self.assertEqual(sq.metrics.close_price, 1048000.0)
        self.assertEqual(sq.metrics.change_percent, -4.73)
        self.assertNotEqual(sq.metrics.change_percent, 87.0)
        self.assertNotEqual(sq.metrics.change_percent, 45.5)

    def test_multi_ratio_sentence_in_stock_section(self) -> None:
        """Stock section with multiple competing financial percentages must not overwrite actual stock delta."""
        raw = """
## SK스퀘어 (402340)
- 당일 종가 1,048,000원 (-4.73%) 급락 마감.
- 자회사 솔리다임 2026E 매출총이익률(GPM) 55.2%, 영업이익률 38.4%, EBITDA 마진율 42.0% 전망.
- 지주사 NAV 할인율 62.5% 수준 유지, SK하이닉스 지분율 20.1% 가치 반영.
- 플랫폼 수수료율 25.0% 및 연체율 3.1%, AI Capex 비중 40.0% 확대.
"""
        cleaned = clean_raw_dump(raw)[0]
        data = self.extractor.extract(cleaned, date_override="2026-10-01")

        sq = data.stocks.get(StockSymbol.SK_SQUARE.value)
        self.assertIsNotNone(sq)
        self.assertEqual(sq.metrics.close_price, 1048000.0)
        self.assertEqual(sq.metrics.change_percent, -4.73)

    def test_no_price_change_present_korean_ratios_masked(self) -> None:
        """When a stock has Korean operational ratios (GPM 87%, OPM 35%) but NO price change, change_percent is None."""
        raw = """
## SK스퀘어 (402340)
- 솔리다임 eSSD 사업 호조로 2026E GPM 87% 예상.
- 영업이익률(OPM) 35% 달성 가능성 제시.
- NAV 할인율 60% 구간 지속.
"""
        cleaned = clean_raw_dump(raw)[0]
        data = self.extractor.extract(cleaned, date_override="2026-10-01")

        sq = data.stocks.get(StockSymbol.SK_SQUARE.value)
        if sq and sq.metrics:
            self.assertIsNone(sq.metrics.change_percent)

    def test_empirical_english_gross_margin_87_pct_misattribution(self) -> None:
        """VERIFIED REMEDIATION: 'Gross Margin +87% 상승' is masked and not misattributed as stock change."""
        raw = """
## SK스퀘어 (402340)
SK스퀘어는 자회사 Gross Margin +87% 상승 소식이 전해졌습니다.
"""
        data = self.extractor.extract(raw, date_override="2026-10-01")
        sq = data.stocks.get(StockSymbol.SK_SQUARE.value)
        self.assertIsNotNone(sq)
        self.assertIsNotNone(sq.metrics)

        self.assertIsNone(
            sq.metrics.change_percent,
            "Remediated: 'Gross Margin +87% 상승' is masked and not misattributed as stock change",
        )

    def test_empirical_uber_growth_rate_misattribution(self) -> None:
        """VERIFIED REMEDIATION: Uber YoY +35% bookings growth is masked and not extracted as stock surge +35%."""
        raw = """
## 우버 (UBER)
우버는 연간 총예약(Gross Bookings) YoY +35% 성장을 기록했습니다.
"""
        data = self.extractor.extract(raw, date_override="2026-10-01")
        ub = data.stocks.get(StockSymbol.UBER.value)
        self.assertIsNotNone(ub)
        self.assertIsNotNone(ub.metrics)

        self.assertIsNone(
            ub.metrics.change_percent,
            "Remediated: 'YoY +35% 성장' is masked and not misattributed as stock change",
        )
        self.assertNotIn("전일 대비 +35.00%", ub.one_paragraph_summary)

    def test_empirical_hybrid_growth_metrics_misattribution(self) -> None:
        """VERIFIED REMEDIATION: QoQ, CAGR, Revenue Growth, and Fee rate are masked and not misattributed as stock changes."""
        buggy_cases = [
            ("SK스퀘어는 자회사 Revenue Growth +50% 상승 소식이 전해졌습니다.", 50.0),
            ("SK스퀘어는 자회사 QoQ +15% 증가 소식이 전해졌습니다.", 15.0),
            ("SK스퀘어는 플랫폼 Fee rate +15% 상승 소식이 전해졌습니다.", 15.0),
        ]
        for text, _ in buggy_cases:
            data = self.extractor.extract(f"## SK스퀘어 (402340)\n{text}", date_override="2026-10-01")
            sq = data.stocks.get(StockSymbol.SK_SQUARE.value)
            self.assertIsNotNone(sq)
            self.assertIsNone(
                sq.metrics.change_percent,
                f"Remediated: {text} is masked and not parsed as stock change",
            )


class TestInactiveStockGhostingAttacks(unittest.TestCase):
    """Stress-tests that inactive stocks (FLNC, UPST, CELH, ENPH) are NEVER falsely instantiated from noisy dumps."""

    def setUp(self) -> None:
        self.extractor = FactExtractor()

    def test_sidebar_residuals_do_not_instantiate_inactive_stocks(self) -> None:
        """Residual sidebar lines mentioning inactive stocks with canonical names must NOT appear in data.stocks."""
        noisy_dump = """
## 1. 글로벌 테크 시황
- 2026년 9월 28일 플루언스에너지(FLNC) 주가 흐름을 분석함
- 업스타트홀딩스 투자 분석 정보업스타트홀딩스의 주가 흐름과 시장 영향 요인을 분석함
- 셀시우스 홀딩스 기업 분석Analyzed Celsius Holdings' latest stock performance
- 인페이즈 에너지 기업 분석Analyzed Wall Street analyst ratings for Enphase Energy

## 2. SK하이닉스 ADR (SKHY)
- 종가: $188.80
- 등락률: +1.01%
- 거래량: 2,150,000주
- 주요 동인: 마이크론 FY4Q26 서프라이즈 및 HBM 2027 완판 수혜
"""
        cleaned = clean_raw_dump(noisy_dump)[0]
        data = self.extractor.extract(cleaned, date_override="2026-10-01")

        self.assertIn("SK_HYNIX", data.stocks)
        for inactive in ["FLNC", "UPST", "CELH", "ENPH"]:
            self.assertNotIn(
                inactive,
                data.stocks,
                f"Inactive stock {inactive} was falsely instantiated from sidebar titles!",
            )

    def test_empirical_sidebar_leak_triggers_fake_stock_instantiation(self) -> None:
        """VERIFIED REMEDIATION: Leaked sidebar titles with dates/percentages do NOT instantiate inactive stocks."""
        noisy_dump = """
- 2026-10-01 플루언스에너지(FLNC) 주가 5% 급락 분석
- 2026. 10. 01. 업스타트 대출 실적 호조 분석
- 2026/10/01 셀시우스 실적 점검

## SK하이닉스 ADR (SKHY)
- 종가: $188.80
- 등락률: +1.01%
"""
        cleaned = clean_raw_dump(noisy_dump)[0]
        data = self.extractor.extract(cleaned, date_override="2026-10-01")

        self.assertIn("SK_HYNIX", data.stocks)
        for inactive in ["FLNC", "UPST", "CELH"]:
            self.assertNotIn(
                inactive,
                data.stocks,
                f"Remediated: inactive stock {inactive} must not be instantiated from sidebar lines",
            )

    def test_passing_peer_comparison_mentions_do_not_instantiate_inactive_stocks(self) -> None:
        """Mentioning inactive stocks purely as peer comparison benchmarks must NOT instantiate them."""
        raw = """
## SK하이닉스 ADR (SKHY)
- 종가: $188.80
- 등락률: +1.01%
- 피어 비교: 셀시우스(CELH) 및 엔페이즈 에너지(ENPH), 업스타트(UPST), 플루언스에너지(FLNC) 등 고밸류 성장주 전반이 매크로 금리 경계감에 횡보했습니다.
"""
        cleaned = clean_raw_dump(raw)[0]
        data = self.extractor.extract(cleaned, date_override="2026-10-01")

        self.assertIn("SK_HYNIX", data.stocks)
        for inactive in ["FLNC", "UPST", "CELH", "ENPH"]:
            self.assertNotIn(
                inactive,
                data.stocks,
                f"Peer comparison mention falsely instantiated inactive stock {inactive}!",
            )

    def test_temperature_celsius_does_not_instantiate_celh(self) -> None:
        """Text discussing physical temperature in Celsius must never trigger Celsius Holdings (CELH)."""
        raw = """
## SK하이닉스 ADR (SKHY)
- 종가: $188.80
- HBM3E 제조 공정에서 웨이퍼 챔버 온도를 섭씨 25도(25 Celsius) 및 고온 120 Celsius degrees 테스트 환경에서 수율을 검증했습니다.
"""
        cleaned = clean_raw_dump(raw)[0]
        data = self.extractor.extract(cleaned, date_override="2026-10-01")

        self.assertNotIn("CELH", data.stocks, "Physical temperature 'Celsius' triggered false CELH instantiation!")

    def test_influencer_does_not_instantiate_flnc(self) -> None:
        """Text containing '인플루언서' (Influencer) must never trigger Fluence Energy (FLNC)."""
        raw = """
## 우버 (UBER)
- 종가: $68.51
- 등락률: -1.23%
- 주요 동인: SNS 유명 인플루언서 대상 자그레브 무인택시 시승 프로모션 진행.
"""
        cleaned = clean_raw_dump(raw)[0]
        data = self.extractor.extract(cleaned, date_override="2026-10-01")

        self.assertNotIn("FLNC", data.stocks, "'인플루언서' triggered false FLNC instantiation!")

    def test_block_square_does_not_pollute_sk_square(self) -> None:
        """News about Jack Dorsey's Block (Square / Cash App) must not corrupt SK Square factsheet."""
        raw = """
## 글로벌 핀테크 뉴스
- 잭 도시(Jack Dorsey)의 블록(Square, Cash App)이 비트코인 결제 수수료 인하 발표.
- 스퀘어(Square) 주가 $72.00 (+4.5%).

## SK스퀘어 (402340)
- 지주사 자사주 소각 추진 및 하이닉스 지분가치 부각.
"""
        cleaned = clean_raw_dump(raw)[0]
        data = self.extractor.extract(cleaned, date_override="2026-10-01")

        sq = data.stocks.get("SK_SQUARE")
        if sq and sq.metrics:
            self.assertNotEqual(sq.metrics.close_price, 72.0)
            self.assertNotEqual(sq.metrics.change_percent, 4.5)


class TestLargeDumpStabilityAndThroughput(unittest.TestCase):
    """Stress-tests the pipeline with 100k+ character real-world dump and massive synthetic fuzz payload."""

    def test_real_100k_dump_processing_speed_and_completeness(self) -> None:
        """The 100k+ character raw_input_20261001.txt dump must clean and extract in under 3.0 seconds."""
        self.assertTrue(RAW_INPUT_1001_PATH.exists(), "raw_input_20261001.txt must exist")
        raw_text = RAW_INPUT_1001_PATH.read_text(encoding="utf-8")
        self.assertGreater(len(raw_text), 80_000, "Real dump should be at least 80k characters")

        start_time = time.perf_counter()
        cleaned_text, metadata = clean_raw_dump(raw_text)
        clean_time = time.perf_counter() - start_time

        self.assertLess(clean_time, 2.0, f"clean_raw_dump took too long: {clean_time:.3f}s")
        self.assertGreater(len(cleaned_text), 40_000)

        start_time = time.perf_counter()
        data = FactExtractor().extract(cleaned_text, date_override="2026-10-01")
        extract_time = time.perf_counter() - start_time

        self.assertLess(extract_time, 2.5, f"FactExtractor.extract took too long: {extract_time:.3f}s")

        # Active stocks verified
        self.assertIn("SK_HYNIX", data.stocks)
        self.assertIn("UBER", data.stocks)
        self.assertIn("MBLY", data.stocks)
        self.assertIn("SK_SQUARE", data.stocks)

        # Inactive stocks strictly excluded
        for sym in ["FLNC", "UPST", "CELH", "ENPH"]:
            self.assertNotIn(sym, data.stocks, f"Inactive stock {sym} should not be extracted")

    def test_synthetic_500k_fuzz_dump_catastrophic_backtracking_resilience(self) -> None:
        """500k character synthetic adversarial dump does not freeze or crash from catastrophic backtracking."""
        base_noise = (
            "Google Gemini Advanced\n"
            "새 대화 시작\n"
            "- 2026년 9월 28일 플루언스에너지(FLNC) 주가 흐름을 분석함\n"
            "- Analyzed Wall Street analyst ratings for Upstart Holdings\n"
            "본 자료는 정보 제공만을 목적으로 하며 투자 결과에 대한 최종 책임은 본인에게 있습니다.\n"
            "YouTube 동영상 시청 시 YouTube 서비스 약관이 적용됩니다. https://youtu.be/dummy\n"
            "더보기 예약은 지정된 시간 근처에 실행되며 [1] 출처\n"
            "질문: 마이크론 실적 전망은? 답변: GPM 87% 달성 전망입니다.\n"
        )
        # 1600 repetitions creates > 500KB text
        huge_dump = (base_noise * 1600) + "\n\n## SK하이닉스 ADR\n- 종가: $188.80\n- 등락률: +1.01%\n"
        self.assertGreater(len(huge_dump), 500_000)

        start_time = time.perf_counter()
        cleaned, _ = clean_raw_dump(huge_dump)
        elapsed = time.perf_counter() - start_time

        self.assertLess(elapsed, 5.0, f"Cleaner suffered catastrophic backtracking on 500k dump: {elapsed:.2f}s")
        self.assertIn("SK하이닉스 ADR", cleaned)


class TestPreservationOfLegitimateContent(unittest.TestCase):
    """Verifies that legitimate financial analysis, URLs, and interview quotes are NEVER accidentally destroyed."""

    def setUp(self) -> None:
        self.cleaner = RawDumpCleaner()
        self.extractor = FactExtractor()

    def test_youtube_media_links_preserved_while_ui_preamble_peeled(self) -> None:
        """Preamble 'YouTube 서비스 약관이 적용됩니다.' is peeled, but the URL is 100% preserved."""
        raw = (
            "YouTube 서비스 약관이 적용됩니다. https://www.youtube.com/watch?v=kXoP9s8W8c4\n"
            "다라 코스로샤히 CEO 단독 인터뷰 영상입니다.\n"
        )
        cleaned = self.cleaner.clean(raw)
        self.assertNotIn("YouTube 서비스 약관이 적용됩니다.", cleaned)
        self.assertIn("https://www.youtube.com/watch?v=kXoP9s8W8c4", cleaned)
        self.assertIn("다라 코스로샤히 CEO 단독 인터뷰", cleaned)

    def test_interview_questions_with_q_and_a_preserved(self) -> None:
        """Interview Q&A dialogue ('질문: ... 답변: ...') must NOT be pruned by user prompt filters."""
        raw = """
## 우버 (UBER)
- 종가: $68.51
- 다라 코스로샤히 인터뷰:
  질문: 유럽 로보택시 규제 장벽을 어떻게 돌파할 것인가?
  답변: "우리는 규제 당국과 직접 협력하며 안전성 데이터를 공유하고 있습니다."
"""
        cleaned = self.cleaner.clean(raw)
        self.assertIn("질문: 유럽 로보택시 규제 장벽", cleaned)
        self.assertIn("답변:", cleaned)

    def test_strip_markdown_links_utility(self) -> None:
        """Ensures strip_markdown_links cleanly converts links to anchor text without residual brackets or URLs."""
        test_cases = [
            ("[TIKR 리서치 보고서](https://tikr.com/skhy)", "TIKR 리서치 보고서"),
            ("핵심 동인: [블룸버그 단독](https://bloomberg.com/news) 자율주행 상용화", "핵심 동인: 블룸버그 단독 자율주행 상용화"),
            ("- [모빌아이 포럼](https://evercore.com/forum) 참석", "모빌아이 포럼 참석"),
            ("[텍스트](https://url.com) (https://url.com)", "텍스트"),
        ]
        for inp, expected in test_cases:
            res = strip_markdown_links(inp)
            self.assertEqual(res, expected, f"Failed on input '{inp}': got '{res}'")


if __name__ == "__main__":
    unittest.main()
