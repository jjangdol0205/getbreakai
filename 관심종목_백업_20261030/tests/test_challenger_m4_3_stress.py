"""Challenger M4 Iteration 2 Adversarial Stress Verification Suite.

Exhaustive empirical testing of:
1. Multi-format date prefix permutations and quote variations in RawDumpCleaner.
2. English and Korean financial ratios forward/reverse order masking in FactExtractor.
3. Inactive stock ghost-instantiation attacks across extreme variants.
4. Coexistence of legitimate stock prices with dozens of ratio keywords.
5. End-to-end processing of raw_input_20261001.txt.
"""

from __future__ import annotations

from pathlib import Path
import unittest

ROOT_DIR = Path(__file__).resolve().parent.parent
RAW_INPUT_1001_PATH = ROOT_DIR / "raw_input_20261001.txt"

from engine.cleaner import RawDumpCleaner, clean_raw_dump
from engine.extractor import FactExtractor
from engine.models import StockSymbol


class TestDateVariantsAndQuotesAdversarial(unittest.TestCase):
    """Stress-tests date formatting permutations and quote variations in cleaner."""

    def setUp(self) -> None:
        self.cleaner = RawDumpCleaner()

    def test_all_date_format_permutations_stripped(self) -> None:
        """Every date format permutation on sidebar items must be stripped."""
        date_variants = [
            "2026-10-01",
            "2026.10.01",
            "2026. 10. 01.",
            "2026. 10. 1.",
            "2026/10/01",
            "2026/10/1",
            "2026-10-1",
            "10/01",
            "10. 01.",
            "10-01",
            "10월 1일",
            "2026년 10월 1일",
        ]
        bullet_variants = ["", "- ", "• ", "* ", "▶ ", "▪ ", "◆ ", "\t- ", "   • "]
        topics = [
            "플루언스에너지 투자 분석 방안",
            "플루언스에너지(FLNC) 주가 5% 급락 분석",
            "업스타트홀딩스 투자 분석",
            "업스타트 대출 실적 호조 분석",
            "셀시우스 홀딩스 기업 분석",
            "셀시우스 실적 점검",
            "인페이즈 에너지 기업 분석",
            "인페이즈 에너지 주가 동향",
            "SK스퀘어 투자 분석",
            "SK 스퀘어 기업 분석",
            "모빌아이 투자 분석 리포트",
            "우버 투자자 및 IB 시각 분석",
        ]

        test_lines = []
        for d in date_variants:
            for b in bullet_variants[:3]:
                for t in topics[:4]:
                    test_lines.append(f"{b}{d} {t}")

        # Mix with a legitimate stock line
        payload = "\n".join(test_lines) + "\n\n## SK하이닉스 ADR\n- 종가: $188.80\n- 등락률: +1.01%\n"
        cleaned, _ = self.cleaner.clean_with_metadata(payload)

        for line in test_lines:
            stripped = line.strip().lstrip("-•*▶▪◆ \t")
            self.assertNotIn(stripped, cleaned, f"Leaked date variant line: {stripped}")

        self.assertIn("SK하이닉스 ADR", cleaned)
        self.assertIn("$188.80", cleaned)

    def test_all_track_quote_encapsulation_variants_stripped(self) -> None:
        """Every permutation of Track / Summarize quotes must be stripped."""
        quotes = [
            'Track "Celsius Holdings" developments is up to date.',
            "Track 'Celsius Holdings' developments is up to date.",
            "Track “Celsius Holdings” developments is up to date.",
            "Track ‘Celsius Holdings’ developments is up to date.",
            'Track "SK hynix" developments is up to date.',
            'Track "Enphase Energy" developments are up to date.',
            'Track "Uber Technologies" developments is up to date',
            'Track "Fluence Energy" developments are up to date.',
            'Track "Upstart Holdings" developments is up to date.',
            'Track "Mobileye" developments is up to date.',
            'Track "SK Square" developments are up to date.',
            'Summarize "Uber" developments is up to date.',
            '• Track "Celsius Holdings" developments is up to date.',
            '- Track "Enphase Energy" developments are up to date.',
            '▶ Track "Fluence Energy" developments is up to date.',
        ]
        payload = "\n".join(quotes) + "\n\n## 우버 (UBER)\n- 종가: $68.51\n"
        cleaned, _ = self.cleaner.clean_with_metadata(payload)

        for q in quotes:
            self.assertNotIn(q.strip().lstrip("•-▶ \t"), cleaned, f"Leaked Track quote: {q}")
        self.assertIn("우버 (UBER)", cleaned)
        self.assertIn("$68.51", cleaned)


class TestEnglishAndKoreanRatiosAdversarial(unittest.TestCase):
    """Stress-tests ratio masking with dozens of forward and reverse-order ratios."""

    def setUp(self) -> None:
        self.extractor = FactExtractor()

    def test_all_forward_english_ratios_masked_when_no_price(self) -> None:
        """When no price change is present, forward English ratios must never become change_percent."""
        ratios = [
            "Gross Margin: +87%",
            "Gross Margin 87%",
            "Operating Margin: +42.5%",
            "Operating Margin 35%",
            "Net Margin: +28%",
            "Net Margin 20%",
            "EBITDA Margin: +51%",
            "FCF Margin: +33%",
            "YoY: +35%",
            "YoY +35% 성장",
            "YoY -12%",
            "QoQ: +15.5%",
            "QoQ +15% 증가",
            "QoQ -8.2%",
            "MoM: +4.1%",
            "CAGR: +25%",
            "CAGR +25% 지속",
            "Revenue Growth: +60%",
            "Revenue Growth +50% 기록",
            "Growth rate: +18%",
            "Growth rate 15%",
            "Fee rate: +22%",
            "Fee rate +15% 상승",
            "Take rate: +28.5%",
            "Discount rate: +14%",
        ]
        for r in ratios:
            text = f"## SK스퀘어 (402340)\n자회사 관련 {r} 소식이 전해졌습니다."
            data = self.extractor.extract(text, date_override="2026-10-01")
            sq = data.stocks.get(StockSymbol.SK_SQUARE.value)
            self.assertIsNotNone(sq, f"SK_SQUARE should exist for test with {r}")
            self.assertIsNone(
                sq.metrics.change_percent,
                f"Ratio '{r}' was misattributed as change_percent: {sq.metrics.change_percent}",
            )

    def test_all_reverse_english_ratios_masked_when_no_price(self) -> None:
        """When no price change is present, reverse-order English ratios must never become change_percent."""
        reverse_ratios = [
            "+87% Gross Margin 달성",
            "87% Gross Margin 달성",
            "+42.5% Operating Margin 기록",
            "+28% Net Margin 시현",
            "+51% EBITDA Margin 전망",
            "+33% FCF Margin 유지",
            "+35% YoY 성장",
            "-12% YoY 감소",
            "+15.5% QoQ 증가",
            "-8.2% QoQ 하락",
            "+4.1% MoM 상승",
            "+25% CAGR 달성",
            "+60% Revenue Growth 전망",
            "+18% Growth rate 기록",
            "+22% Fee rate 적용",
            "+28.5% Take rate 수취",
            "+14% Discount rate 반영",
        ]
        for r in reverse_ratios:
            text = f"## SK스퀘어 (402340)\n사업부에서 {r} 소식이 확인되었습니다."
            data = self.extractor.extract(text, date_override="2026-10-01")
            sq = data.stocks.get(StockSymbol.SK_SQUARE.value)
            self.assertIsNotNone(sq, f"SK_SQUARE should exist for test with {r}")
            self.assertIsNone(
                sq.metrics.change_percent,
                f"Reverse ratio '{r}' was misattributed as change_percent: {sq.metrics.change_percent}",
            )

    def test_legitimate_price_change_preserved_with_multiple_ratios(self) -> None:
        """Legitimate price change must NOT be displaced by surrounding multiple English and Korean ratios."""
        raw = """
## 우버 (UBER)
- 종가: $68.51 (-1.23%)
- 모빌리티 부문 YoY +35% 성장 및 Gross Bookings $40B 달성.
- Take rate 28.5% 유지 및 EBITDA Margin 15.2% 시현.
- 5개년 예상 CAGR +25% 및 배민 인수 효과로 Gross Margin +12% 개선 전망.
"""
        data = self.extractor.extract(raw, date_override="2026-10-01")
        ub = data.stocks.get(StockSymbol.UBER.value)
        self.assertIsNotNone(ub)
        self.assertEqual(ub.metrics.close_price, 68.51)
        self.assertEqual(ub.metrics.change_percent, -1.23)
        self.assertEqual(ub.metrics.currency, "USD")


class TestGhostStockAdversarialIsolation(unittest.TestCase):
    """Stress-tests isolation of inactive stocks (FLNC, UPST, CELH, ENPH)."""

    def setUp(self) -> None:
        self.extractor = FactExtractor()

    def test_all_ghost_patterns_fail_to_instantiate_inactive_stocks(self) -> None:
        """Adversarial dump containing multiple ghost patterns for FLNC, UPST, CELH, ENPH."""
        adversarial_noise = """
- 2026. 10. 01. 플루언스에너지(FLNC) 주가 5% 급락 분석 리포트
- 2026/10/01 업스타트 대출 실적 호조 분석 및 전망
- 2026-10-01 셀시우스 홀딩스 기업 분석 확인
- 2026. 10. 1. 인페이즈 에너지 주가 동향 점검
Track "Celsius Holdings" developments is up to date.
Track "Enphase Energy" developments are up to date.
Track "Fluence Energy" developments are up to date.
Track "Upstart Holdings" developments is up to date.

[섹터 및 피어 비교]
- 신재생 및 고성장주 피어 그룹: 셀시우스(CELH -2.5%), 엔페이즈(ENPH +1.2%), 업스타트(UPST -3.8%), 플루언스에너지(FLNC +0.5%)

## 우버 (UBER)
- 종가: $68.51 (-1.23%)
- 주요 동인: SNS 유명 인플루언서 대상 자그레브 무인택시 시승 프로모션 진행.

## SK하이닉스 ADR (SKHY)
- 종가: $188.80 (+1.01%)
- 고온 웨이퍼 테스트: 섭씨 35도(35 Celsius) 및 120 Celsius 환경 신뢰성 검증.
"""
        cleaned, _ = clean_raw_dump(adversarial_noise)
        data = self.extractor.extract(cleaned, date_override="2026-10-01")

        # Active stocks verified
        self.assertIn("UBER", data.stocks)
        self.assertIn("SK_HYNIX", data.stocks)

        # Inactive stocks strictly rejected
        for inactive in ["FLNC", "UPST", "CELH", "ENPH"]:
            self.assertNotIn(
                inactive,
                data.stocks,
                f"Ghost stock {inactive} was instantiated by adversarial dump!",
            )


class TestRealWorldDump1001EndToEnd(unittest.TestCase):
    """Verifies end-to-end processing of real 100k dump raw_input_20261001.txt."""

    def test_full_pipeline_clean_and_extract(self) -> None:
        """raw_input_20261001.txt produces exactly 4 active stocks and 0 ghost stocks."""
        self.assertTrue(RAW_INPUT_1001_PATH.exists())
        raw_text = RAW_INPUT_1001_PATH.read_text(encoding="utf-8")

        cleaned, meta = clean_raw_dump(raw_text)
        self.assertGreater(len(cleaned), 50_000)

        data = FactExtractor().extract(cleaned, date_override="2026-10-01")

        # 4 active stocks must be present
        self.assertIn("SK_HYNIX", data.stocks)
        self.assertIn("UBER", data.stocks)
        self.assertIn("MBLY", data.stocks)
        self.assertIn("SK_SQUARE", data.stocks)

        # 4 inactive stocks must NOT be in data.stocks
        for inactive in ["FLNC", "UPST", "CELH", "ENPH"]:
            self.assertNotIn(inactive, data.stocks)

        # Specific metric checks
        skhy = data.stocks["SK_HYNIX"]
        self.assertEqual(skhy.metrics.close_price, 188.80)
        self.assertEqual(skhy.metrics.currency, "USD")

        uber = data.stocks["UBER"]
        self.assertEqual(uber.metrics.close_price, 68.51)
        self.assertEqual(uber.metrics.change_percent, -1.23)

        mbly = data.stocks["MBLY"]
        self.assertEqual(mbly.metrics.close_price, 7.565)
        self.assertEqual(mbly.metrics.change_percent, -2.95)

        # SK_SQUARE must NOT steal Micron's 87% GPM
        sq = data.stocks["SK_SQUARE"]
        if sq.metrics and sq.metrics.change_percent is not None:
            self.assertNotEqual(sq.metrics.change_percent, 87.0)
            self.assertNotEqual(sq.metrics.change_percent, 30.0)


if __name__ == "__main__":
    unittest.main()
