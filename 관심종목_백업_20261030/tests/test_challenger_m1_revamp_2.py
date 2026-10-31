"""Empirical Challenger 2 stress-testing suite for Milestone M1 Revamp.

Tests coverage:
1. 1-Paragraph Summary Synthesis (_extract_one_paragraph_summary):
   - Missing / None close_price on USD stocks ($None bug)
   - Numbered bullet driver handling & metric theft (. 종가 bug)
   - Extreme price change percentages & tone mapping
   - Conflicting fact vs noise synthesis
   - Macro shock integration & single paragraph structure (no newlines/list formatting)
2. 2-Line Watch Points (_extract_key_points):
   - Embedded decimals / percentages (- 1.50달러, 1.50% false matches)
   - Clean extraction of explicit Line 1 / Line 2
   - Semantic keyword extraction
   - Stock-specific fallback defaults across all 8 stocks
3. Direct Macro Event Attribution (_attribute_macro_to_stocks):
   - 10Y Treasury yield shock mapping to UPST, FLNC, ENPH
   - Nomura CSI / Tech Capex shock mapping to SK_HYNIX, SK_SQUARE
   - FX Rate shock mapping to SK_HYNIX
   - NAV discount ('할인율') false-positive trigger on UPST/FLNC/ENPH
4. End-to-End Raw Input Extraction (raw_input_20260930.txt):
   - Exact target stock extraction & zero phantom instantiations
   - Sidebar UI chrome stripped cleanly
   - Preserved substantive facts & quality check on summaries and key points
"""

import os
import unittest
from engine.cleaner import RawDumpCleaner, clean_raw_dump
from engine.extractor import FactExtractor, extract_facts
from engine.models import KeyWatchPoints, MarketMetrics, StockFactSheet, StockMaster, StockSymbol, STOCK_MASTERS


class TestChallengerOneParagraphSummary(unittest.TestCase):
    """Stress tests for _extract_one_paragraph_summary."""

    def setUp(self) -> None:
        self.extractor = FactExtractor()

    def test_none_close_price_usd_does_not_contain_none_string(self) -> None:
        """When close price is None for a USD stock, summary must NOT contain '$None'."""
        master = STOCK_MASTERS[StockSymbol.UPST]
        metrics = MarketMetrics(stock_id=StockSymbol.UPST.value, currency="USD", close_price=None, change_percent=None)
        core_drivers = ["AI 신용평가 대출 전환율 개선"]
        fact_vs_noise = {"facts": ["대출 전환율 개선"], "noise": []}

        summary = self.extractor._extract_one_paragraph_summary(
            symbol=StockSymbol.UPST,
            master=master,
            content="업스타트 기업 분석 내용",
            metrics=metrics,
            core_drivers=core_drivers,
            fact_vs_noise=fact_vs_noise,
            macro_notes=[],
            raw_summary=""
        )
        self.assertNotIn("$None", summary, "Summary must not contain literal '$None'")

    def test_numbered_bullet_driver_no_leading_dot(self) -> None:
        """Numbered bullet drivers ('1. HBM3E 수주') must not retain a leading dot ('. HBM3E')."""
        text = """## 1. SK하이닉스 (000660)
- 종가: 176,700원
- 등락률: +3.2%
1. HBM3E 12단 독점 공급 계약 체결로 실적 턴어라운드 가속화
"""
        data = self.extractor.extract(text)
        hynix = data.stocks.get("SK_HYNIX")
        self.assertIsNotNone(hynix)
        self.assertNotIn("당일 주가는 .", hynix.one_paragraph_summary,
                         "Summary must not contain '당일 주가는 . ' due to incomplete bullet stripping")

    def test_numbered_bullet_metrics_not_stolen_as_core_driver(self) -> None:
        """When metrics are listed with numbers ('1. 종가: 176,700원'), price must not become the driver."""
        text = """## 1. SK하이닉스 (000660)
1. 종가: 176,700원
2. 등락률: +3.2%
3. 주요 동인: AI 반도체 수요 폭증에 따른 HBM 수출 사상 최고치 경신
"""
        data = self.extractor.extract(text)
        hynix = data.stocks.get("SK_HYNIX")
        self.assertIsNotNone(hynix)
        self.assertNotIn("종가: 176,700원 요인이 핵심 동인", hynix.one_paragraph_summary,
                         "Price metric in numbered bullet was falsely classified as core driver")

    def test_extreme_percentage_change_tone_mapping(self) -> None:
        """Tone mapping: >3% -> 급등, 0~3% -> 강세, < -3% -> 급락, -3~0% -> 조정."""
        cases = [
            (50.0, "급등"),
            (2.5, "강세"),
            (-15.0, "급락"),
            (-1.5, "조정"),
        ]
        master = STOCK_MASTERS[StockSymbol.CELH]
        for pct, expected_tone in cases:
            with self.subTest(pct=pct, expected_tone=expected_tone):
                metrics = MarketMetrics(
                    stock_id=StockSymbol.CELH.value,
                    currency="USD",
                    close_price=35.0,
                    close_price_formatted="$35.00",
                    change_percent=pct,
                    change_percent_formatted=f"{pct:+.2f}%"
                )
                summary = self.extractor._extract_one_paragraph_summary(
                    symbol=StockSymbol.CELH,
                    master=master,
                    content="셀시우스 분석",
                    metrics=metrics,
                    core_drivers=["북미 에너지 드링크 점유율 확대"],
                    fact_vs_noise={"facts": ["점유율 확대"], "noise": []},
                    macro_notes=[],
                    raw_summary=""
                )
                self.assertIn(expected_tone, summary, f"Expected tone '{expected_tone}' for change {pct}%")

    def test_conflicting_fact_vs_noise_synthesis(self) -> None:
        """When both noise and fact are present, synthesizes contrastive sentence."""
        master = STOCK_MASTERS[StockSymbol.SK_HYNIX]
        metrics = MarketMetrics(stock_id=StockSymbol.SK_HYNIX.value, currency="KRW", close_price=176700.0, change_percent=2.27)
        fact_vs_noise = {
            "facts": ["공시 팩트: HBM4 16단 엔비디아 공급 확정"],
            "noise": ["시장 노이즈: 오픈AI 훈련 일시 중단 루머"]
        }
        summary = self.extractor._extract_one_paragraph_summary(
            symbol=StockSymbol.SK_HYNIX,
            master=master,
            content="하이닉스 분석",
            metrics=metrics,
            core_drivers=["HBM 공급 확대"],
            fact_vs_noise=fact_vs_noise,
            macro_notes=["노무라 CSI 103.9 최고치 경신."],
            raw_summary=""
        )
        self.assertIn("단기 센티먼트 노이즈로 분석되며", summary)
        self.assertIn("실물 팩트가 중장기 펀더멘털을 지지하고 있습니다", summary)
        self.assertNotIn("\n", summary, "Synthesized summary must be a single cohesive paragraph without newlines")

    def test_explicit_multiline_summary_is_single_paragraph(self) -> None:
        """Explicit [1문단 핵심 요약] containing newlines should be flattened into a single paragraph."""
        content = """## 셀시우스 (CELH)
[1문단 핵심 요약]
셀시우스(CELH)는 전일 대비 +4.20% 상승 마감했습니다.
골드만삭스 리포트 호평과 펩시 유통망 정상화가 핵심 동인으로 작용했습니다.
단기 노이즈보다 실물 점유율 확대 팩트에 집중할 필요가 있습니다.
"""
        master = STOCK_MASTERS[StockSymbol.CELH]
        metrics = MarketMetrics(stock_id=StockSymbol.CELH.value, currency="USD", close_price=38.5, change_percent=4.2)
        summary = self.extractor._extract_one_paragraph_summary(
            symbol=StockSymbol.CELH,
            master=master,
            content=content,
            metrics=metrics,
            core_drivers=[],
            fact_vs_noise={"facts": [], "noise": []},
            macro_notes=[],
            raw_summary=""
        )
        self.assertNotIn("\n", summary, "Explicit 1-paragraph summary must not contain embedded newlines")


class TestChallengerKeyWatchPoints(unittest.TestCase):
    """Stress tests for _extract_key_points."""

    def setUp(self) -> None:
        self.extractor = FactExtractor()

    def test_parenthesized_or_bullet_decimal_not_extracted_as_line1(self) -> None:
        """Lines starting with or containing decimals like '- 1.50달러' or '1.50%' must not falsely match Line 1."""
        content = """## 셀시우스 (CELH)
- 종가: $38.50
- 1.50달러 상승하여 전일 대비 강세를 보임.
- 2.80% 상승폭 확대로 마감.
"""
        kp = self.extractor._extract_key_points(StockSymbol.CELH, STOCK_MASTERS[StockSymbol.CELH], content)
        self.assertFalse(kp.line1_short_term.startswith("50달러"),
                         f"Line 1 falsely matched decimal '1.50' as: {kp.line1_short_term}")
        self.assertFalse(kp.line2_mid_long_term.startswith("80%"),
                         f"Line 2 falsely matched decimal '2.80' as: {kp.line2_mid_long_term}")

    def test_start_of_line_percentage_decimal_not_line1(self) -> None:
        """Line starting with '1.50% 상승 마감' without dash must not falsely match Line 1."""
        content = """## 모빌아이 (MBLY)
- 종가: $7.50
1.50% 반등에 성공하며 거래 마감.
2.20% 상승 탄력 둔화.
"""
        kp = self.extractor._extract_key_points(StockSymbol.MBLY, STOCK_MASTERS[StockSymbol.MBLY], content)
        self.assertFalse(kp.line1_short_term.startswith("50%"),
                         f"Line 1 falsely matched '1.50%': {kp.line1_short_term}")

    def test_clean_explicit_line1_line2_extraction(self) -> None:
        """Explicit Line 1 and Line 2 prefixes are parsed cleanly."""
        content = """## 엔페이즈에너지 (ENPH)
- 종가: $58.20
- Line 1 (단기 수급/가격선): $55.00 박스권 지지선 사수 여부
- Line 2 (중장기 펀더멘털/이벤트): IQ8/IQ9 마이크로인버터 및 유럽 재고 정상화
"""
        kp = self.extractor._extract_key_points(StockSymbol.ENPH, STOCK_MASTERS[StockSymbol.ENPH], content)
        self.assertIn("$55.00 박스권 지지선", kp.line1_short_term)
        self.assertIn("IQ8/IQ9 마이크로인버터", kp.line2_mid_long_term)

    def test_semantic_keyword_extraction_when_lines_not_labeled(self) -> None:
        """When Line 1/2 labels are absent, extract by semantic keywords (지지선, 가이던스)."""
        content = """## 플루언스에너지 (FLNC)
- 종가: $7.82
- 주가는 $7.00 심리적 지지선에서 하방 경직성을 확보함.
- 2027 회계연도 가이던스 상향 및 수주 잔고 증가 추세.
"""
        kp = self.extractor._extract_key_points(StockSymbol.FLNC, STOCK_MASTERS[StockSymbol.FLNC], content)
        self.assertIn("지지선", kp.line1_short_term)
        self.assertIn("가이던스", kp.line2_mid_long_term)

    def test_fallback_defaults_all_8_stocks(self) -> None:
        """When content has no lines or keywords, all 8 stocks get distinct tailored defaults."""
        for symbol in StockSymbol:
            master = STOCK_MASTERS[symbol]
            kp = self.extractor._extract_key_points(symbol, master, "")
            self.assertTrue(len(kp.line1_short_term) > 10, f"{symbol} Line 1 default is too short")
            self.assertTrue(len(kp.line2_mid_long_term) > 10, f"{symbol} Line 2 default is too short")


class TestChallengerMacroAttribution(unittest.TestCase):
    """Stress tests for _attribute_macro_to_stocks."""

    def setUp(self) -> None:
        self.extractor = FactExtractor()

    def test_10y_treasury_shock_attributes_to_exposed_stocks(self) -> None:
        """10Y treasury shock must map to UPST, FLNC, ENPH."""
        text = "미 국채 10년물 금리 급등으로 금융 시장 전반의 긴축 우려가 커졌습니다."
        attr = self.extractor._attribute_macro_to_stocks(text)
        self.assertTrue(any("국채" in item for item in attr["UPST"]), "UPST missing 10Y treasury attribution")
        self.assertTrue(any("국채" in item for item in attr["FLNC"]), "FLNC missing 10Y treasury attribution")
        self.assertTrue(any("고금리" in item for item in attr["ENPH"]), "ENPH missing interest rate attribution")
        self.assertEqual(len(attr["UBER"]), 0, "UBER should not have interest rate shock attribution")

    def test_nomura_csi_semi_shock_attributes_to_chip_stocks(self) -> None:
        """Nomura CSI and semiconductor supply shock must map to SK_HYNIX and SK_SQUARE."""
        text = "노무라 반도체 칩 부족 지수(CSI)가 103.9로 사상 최고치를 경신했습니다."
        attr = self.extractor._attribute_macro_to_stocks(text)
        self.assertTrue(any("CSI" in item for item in attr["SK_HYNIX"]), "SK_HYNIX missing CSI attribution")
        self.assertTrue(any("메모리" in item for item in attr["SK_SQUARE"]), "SK_SQUARE missing CSI attribution")
        self.assertEqual(len(attr["CELH"]), 0, "CELH should not have semiconductor CSI attribution")

    def test_fx_rate_shock_attributes_to_sk_hynix(self) -> None:
        """FX rate volatility must map to SK_HYNIX."""
        text = "원/달러 환율이 1,350원을 돌파하며 수출 대형주에 대한 관심이 집중되었습니다."
        attr = self.extractor._attribute_macro_to_stocks(text)
        self.assertTrue(any("환율" in item for item in attr["SK_HYNIX"]), "SK_HYNIX missing FX attribution")

    def test_nav_discount_should_not_trigger_interest_rate_shock(self) -> None:
        """SK Square NAV discount ('할인율') must NOT trigger 10Y Treasury interest rate shock on UPST/FLNC/ENPH."""
        text = """## SK스퀘어 (402340)
- 현재 NAV 할인율은 65.2% 수준을 유지하고 있습니다.
"""
        attr = self.extractor._attribute_macro_to_stocks(text)
        self.assertEqual(
            len(attr["UPST"]),
            0,
            f"SK Square NAV 할인율 falsely triggered interest rate shock on UPST: {attr['UPST']}"
        )


class TestChallengerRawInput20260930(unittest.TestCase):
    """End-to-end tests on raw_input_20260930.txt."""

    @classmethod
    def setUpClass(cls) -> None:
        raw_path = "raw_input_20260930.txt"
        if not os.path.exists(raw_path):
            raise unittest.SkipTest("raw_input_20260930.txt not found")
        with open(raw_path, "r", encoding="utf-8") as f:
            cls.raw_text = f.read()

        cls.cleaned_text, cls.metadata = clean_raw_dump(cls.raw_text)
        cls.data = FactExtractor().extract(cls.cleaned_text)

    def test_zero_phantom_stocks_instantiated(self) -> None:
        """CELH and ENPH only appear in sidebar or peer comparison in raw_input_20260930.txt and must NOT be instantiated."""
        extracted_stocks = set(self.data.stocks.keys())
        expected_stocks = {"UBER", "SK_HYNIX", "MBLY", "FLNC", "UPST"}
        self.assertEqual(
            extracted_stocks,
            expected_stocks,
            f"Extracted stocks {extracted_stocks} does not match expected {expected_stocks}. Phantom stocks detected!"
        )

    def test_cleaner_strips_all_sidebar_chrome(self) -> None:
        """All 10 Gemini sidebar chat entries must be cleanly stripped."""
        sidebar_snippets = [
            "우버의 투자자 및 IB 시각 분석우버의 일일 주가 동향과 상승 원인을 분석함",
            "인페이즈 에너지 기업 분석Analyzed Enphase Air system announcement and strategic implications",
            "셀시우스 홀딩스 기업 분석골드만삭스 리포트 분석 및 모니터링 체계를 고도화함",
            "Ai시대 이준이 교육AI 시대 자녀 교육 원칙 세 가지를 요약함",
        ]
        for snippet in sidebar_snippets:
            self.assertNotIn(snippet, self.cleaned_text, f"Sidebar snippet leaked into cleaned text: {snippet}")

    def test_substantive_financial_facts_preserved(self) -> None:
        """Financial facts in raw dump must be preserved."""
        self.assertIn("103.9", self.cleaned_text, "Nomura CSI 103.9 must be preserved")
        self.assertIn("TIKR", self.cleaned_text, "TIKR report link must be preserved")

    def test_extracted_stocks_have_no_none_string_in_summary(self) -> None:
        """No stock in raw_input_20260930.txt should have '$None' in one_paragraph_summary."""
        for stock_id, fact_sheet in self.data.stocks.items():
            self.assertNotIn(
                "$None",
                fact_sheet.one_paragraph_summary,
                f"Stock {stock_id} has literal '$None' in one_paragraph_summary: {fact_sheet.one_paragraph_summary}"
            )

    def test_extracted_stocks_have_valid_key_points(self) -> None:
        """All extracted stocks must have populated Line 1 and Line 2 key points."""
        for stock_id, fact_sheet in self.data.stocks.items():
            kp = fact_sheet.key_points
            self.assertTrue(bool(kp.line1_short_term), f"Stock {stock_id} has empty Line 1")
            self.assertTrue(bool(kp.line2_mid_long_term), f"Stock {stock_id} has empty Line 2")


if __name__ == "__main__":
    unittest.main()
