"""Adversarial challenge and empirical stress-test suite for Milestone M1 (Revamp 1).

Author: Challenger 1 (teamwork_preview_challenger_m1_revamp_1)
Target Scope: engine/models.py, engine/cleaner.py, engine/extractor.py

Coverage:
1. Cleaner preservation of substantive financial facts amidst realistic messy Gemini chat dumps.
2. Extractor recognition of CELH and ENPH across diverse alias permutations.
3. Accurate extraction of metrics (prices, % change, volume), drivers, 1-paragraph summary, 2-line watch points.
4. Executive interviews extraction for John Fieldly and Badri Kothandaraman.
5. Negative collision stress testing:
   - "섭씨 35도 (Celsius)"
   - "Phase 2 임상시험"
   - "인플루언서 마케팅"
   - "타임스퀘어"
   - Competitor peer comparison lists
6. Empirical Bug Probes:
   - Bug Probe 1: False positive CELH instantiation on "섭씨 35도 (Celsius)".
   - Bug Probe 2: Short unbulleted URL lines misclassified as section headers and discarded.
   - Bug Probe 3: Casual sector mentions containing "관련주가" triggering phantom stock instantiation.
"""

import unittest
from engine.cleaner import RawDumpCleaner, clean_raw_dump
from engine.extractor import FactExtractor, extract_facts
from engine.models import STOCK_MASTERS, StockSymbol


class TestMessyGeminiCleanerStress(unittest.TestCase):
    """Stress tests for cleaner.py against realistic messy Gemini chat dumps."""

    def setUp(self) -> None:
        self.cleaner = RawDumpCleaner()

    def test_cleaner_realistic_messy_gemini_dump_with_substantive_phrases(self) -> None:
        """Verify that UI chrome and sidebar entries are stripped while substantive facts are preserved."""
        raw_text = """
Google Gemini
새 대화
대화 시작
2시간 전
수정됨
우버의 투자자 및 IB 시각 분석우버의 일일 주가 동향과 상승 원인을 분석함.
관심사 일기 정리어제 작성한 관심사 일기 내 주요 내용을 분석함
모빌아이 투자 분석 리포트모빌아이 주가 변동 요인과 시장 성과를 분석함
플루언스에너지 투자 분석 방안플루언스 에너지의 당일 시세와 변동 요인을 분석함
업스타트홀딩스 투자 분석 정보업스타트홀딩스의 당일 주가 흐름과 시장 요인을 분석함
SK스퀘어 투자 분석 방안한국 반도체 시장의 저평가 요인과 기회를 분석함
인페이즈 에너지 기업 분석Analyzed Enphase Air system announcement and strategic implications.
주요 AI 리더 인터뷰 추적주요 인사들의 인터뷰 발언과 전략적 시사점을 요약함.
셀시우스 홀딩스 기업 분석골드만삭스 리포트 분석 및 모니터링 체계를 고도화함.
Ai시대 이준이 교육AI 시대 자녀 교육 원칙 세 가지를 요약함.
Gemini와의 대화
알았음
네, 요청하신 8개 관심 종목의 시황 브리핑 결과입니다:

```markdown
## 1. 셀시우스 홀딩스 (Celsius Holdings, Inc. - NASDAQ: CELH)
- 종가: $38.50
- 등락률: +4.20% (+$1.55)
- 거래량: 4.85M
- 주요 동인: 골드만삭스 리서치 분석에 따르면 모니터링 체계를 고도화함과 동시에 에너지 드링크 점유율 확대 전망.
- Fact vs Noise:
  - 공시 팩트: 펩시(PepsiCo) 유통망 재고 최적화 완료 및 북미 스캐너 데이터 반등 확인.
  - 시장 노이즈: 유통망 수수료 갈등 루머는 근거 없는 일시적 센티먼트 왜곡에 불과함.
- 경영진 인터뷰:
  - 존 필들리(John Fieldly) CEO는 "북미뿐 아니라 영국, 프랑스 등 글로벌 신규 시장 침투 속도가 가속화되고 있다"고 강조함.
  - 출처: https://www.goldmansachs.com/insights/celsius-deep-dive.html
- Line 1: $35.00 핵심 지지선 및 $42.00 저항선 돌파 여부.
- Line 2: 3분기 실적 발표 및 펩시 유통 인센티브 마진 가이던스.

## 2. 엔페이즈 에너지 (Enphase Energy, Inc. - NASDAQ: ENPH)
- 종가: $58.20
- 등락률: -3.36% (-$2.02)
- 거래량: 3,120,000주
- 주요 동인: The newly announced Enphase Air system provides grid-agnostic microinverter capabilities and European residential expansion.
- Fact vs Noise:
  - 공시 팩트: IQ8 및 IQ9 차세대 마이크로인버터와 신규 소프트웨어 플랫폼 Solargraf 출시.
  - 시장 노이즈: 유럽 태양광 유통 재고 소진 지연에 대한 과도한 비관론.
- 경영진 인터뷰:
  - 바드리 코탄다라만(Badri Kothandaraman) CEO: "Enphase Air system announcement and strategic deployment will lead market turnaround."
  - 인터뷰 영상: https://youtu.be/enphase-ceo-interview-2026
- Line 1: $55.00 심리적 지지선 사수 여부.
- Line 2: 차세대 IQ9 상용화 및 NEM 3.0 배터리 부착률 추이.
```

Google Docs로 내보내기
답변 복사
좋아요
싫어요
동영상 시청 시 YouTube 서비스 약관이 적용됩니다.
본 자료는 정보 제공만을 목적으로 하며 특정 증권의 매수·매도를 추천하거나 투자 권유를 위한 것이 아닙니다.
"""
        cleaned, meta = self.cleaner.clean_with_metadata(raw_text)

        # 1. UI Chrome & Sidebar stripping check
        self.assertNotIn("Google Gemini", cleaned)
        self.assertNotIn("새 대화", cleaned)
        self.assertNotIn("2시간 전", cleaned)
        self.assertNotIn("우버의 투자자 및 IB 시각 분석", cleaned)
        self.assertNotIn("관심사 일기 정리어제", cleaned)
        self.assertNotIn("Ai시대 이준이 교육", cleaned)
        self.assertNotIn("셀시우스 홀딩스 기업 분석골드만삭스 리포트 분석 및 모니터링 체계를 고도화함.", cleaned)
        self.assertNotIn("인페이즈 에너지 기업 분석Analyzed Enphase Air system announcement and strategic implications.", cleaned)
        self.assertNotIn("Google Docs로 내보내기", cleaned)
        self.assertNotIn("답변 복사", cleaned)
        self.assertNotIn("YouTube 서비스 약관", cleaned)
        self.assertNotIn("투자 권유를 위한 것이 아닙니다", cleaned)
        self.assertNotIn("```markdown", cleaned)

        # 2. Substantive facts preservation check
        self.assertIn("모니터링 체계를 고도화함과 동시에 에너지 드링크 점유율 확대 전망", cleaned)
        self.assertIn("The newly announced Enphase Air system provides grid-agnostic microinverter capabilities", cleaned)
        self.assertIn("https://www.goldmansachs.com/insights/celsius-deep-dive.html", cleaned)
        self.assertIn("https://youtu.be/enphase-ceo-interview-2026", cleaned)
        self.assertIn("존 필들리", cleaned)
        self.assertIn("바드리 코탄다라만", cleaned)

    def test_cleaner_all_10_gemini_sidebar_entries_stripped(self) -> None:
        """All 10 known Gemini sidebar history lines must be cleanly stripped."""
        sidebar_entries = [
            "우버의 투자자 및 IB 시각 분석우버의 일일 주가 동향과 상승 원인을 분석함.",
            "관심사 일기 정리어제 작성한 관심사 일기 내 주요 내용을 분석함",
            "모빌아이 투자 분석 리포트모빌아이 주가 변동 요인과 시장 성과를 분석함",
            "플루언스에너지 투자 분석 방안플루언스 에너지의 당일 시세와 변동 요인을 분석함",
            "업스타트홀딩스 투자 분석 정보업스타트홀딩스의 당일 주가 흐름과 시장 요인을 분석함",
            "SK스퀘어 투자 분석 방안한국 반도체 시장의 저평가 요인과 기회를 분석함",
            "인페이즈 에너지 기업 분석Analyzed Enphase Air system announcement and strategic implications.",
            "주요 AI 리더 인터뷰 추적주요 인사들의 인터뷰 발언과 전략적 시사점을 요약함.",
            "셀시우스 홀딩스 기업 분석골드만삭스 리포트 분석 및 모니터링 체계를 고도화함.",
            "Ai시대 이준이 교육AI 시대 자녀 교육 원칙 세 가지를 요약함.",
        ]
        raw = "\n".join(sidebar_entries) + "\n\n## SK하이닉스\n- 종가: 180,000원\n"
        cleaned, _ = self.cleaner.clean_with_metadata(raw)
        for entry in sidebar_entries:
            self.assertNotIn(entry.strip("."), cleaned, f"Sidebar entry was not stripped: {entry}")
        self.assertIn("SK하이닉스", cleaned)

    def test_cleaner_phrase_variations_with_korean_conjugations_preserved(self) -> None:
        """Substantive sentences containing phrases similar to sidebar items must NOT be dropped."""
        samples = [
            "당사는 리스크 관리 모니터링 체계를 고도화함에 따라 펀더멘털 가시성을 확보했습니다.",
            "신규 수급 체계를 고도화함으로써 불확실성을 최소화하고 있습니다.",
            "당일 시세와 변동 요인을 분석함에 있어서 핵심 원자재 가격 추이를 우선 고려해야 합니다.",
            "어제 정리된 일기 내 주요 내용을 분석함에 근거하여 소비 트렌드를 도출했습니다.",
        ]
        for s in samples:
            cleaned, _ = self.cleaner.clean_with_metadata(s)
            self.assertIn(s, cleaned, f"Failed to preserve substantive sentence: '{s}'")


class TestStockExtractionAliasesAndMetrics(unittest.TestCase):
    """Stress tests for CELH and ENPH aliases, metrics, drivers, and 2-block format."""

    def setUp(self) -> None:
        self.extractor = FactExtractor()

    def test_celh_all_alias_permutations(self) -> None:
        """CELH must be recognized across various alias forms in section headers."""
        alias_cases = [
            ("## 1. 셀시우스 (CELH)", "셀시우스 (CELH)"),
            ("## 셀시우스홀딩스", "셀시우스홀딩스"),
            ("## Celsius Holdings, Inc. (CELH)", "Celsius Holdings"),
            ("## Celsius", "Celsius"),
            ("## CELH", "CELH"),
        ]
        for header, label in alias_cases:
            text = f"""{header}
- 종가: $38.50
- 등락률: +4.20%
- 거래량: 4.85M
- 주요 동인: 북미 에너지 드링크 점유율 확대 및 펩시 유통 시너지
"""
            data = self.extractor.extract(text, date_override="2026-09-29")
            self.assertIn("CELH", data.stocks, f"CELH was not recognized with header: {header}")
            s = data.stocks["CELH"]
            self.assertEqual(s.metrics.close_price, 38.50, f"Close price failed for {label}")
            self.assertEqual(s.metrics.change_percent, 4.20, f"Change percent failed for {label}")
            self.assertEqual(s.metrics.volume, 4_850_000, f"Volume failed for {label}")

    def test_enph_all_alias_permutations(self) -> None:
        """ENPH must be recognized across various alias forms in section headers."""
        alias_cases = [
            ("## 1. 엔페이즈 (ENPH)", "엔페이즈 (ENPH)"),
            ("## 인페이즈 에너지 (ENPH)", "인페이즈 에너지"),
            ("## Enphase Energy, Inc.", "Enphase Energy"),
            ("## Enphase", "Enphase"),
            ("## ENPH", "ENPH"),
        ]
        for header, label in alias_cases:
            text = f"""{header}
- 종가: $58.20
- 등락률: -3.36%
- 거래량: 3.12M
- 주요 동인: IQ8 및 Enphase Air 시스템 출시와 마이크로인버터 수요
"""
            data = self.extractor.extract(text, date_override="2026-09-29")
            self.assertIn("ENPH", data.stocks, f"ENPH was not recognized with header: {header}")
            s = data.stocks["ENPH"]
            self.assertEqual(s.metrics.close_price, 58.20, f"Close price failed for {label}")
            self.assertEqual(s.metrics.change_percent, -3.36, f"Change percent failed for {label}")
            self.assertEqual(s.metrics.volume, 3_120_000, f"Volume failed for {label}")

    def test_celh_enph_prices_percentages_and_volumes(self) -> None:
        """Test varied metric formats: dollar sign, Korean '달러', signed change %, volume units."""
        text = """
## 1. CELH
- 정규장 종가: 38.50달러
- 등락률: ▲4.20% (+$1.55)
- 거래량: 485만 주
- 주요 동인: 북미 편의점 NACS 스캐너 데이터 서프라이즈

## 2. ENPH
- 정규장 종가: 58.20 USD
- 등락률: ▼3.36% (-$2.02)
- 거래량: 3.12M
- 주요 동인: 주거용 솔라 인버터 출하량 가이던스 발표
"""
        data = self.extractor.extract(text, date_override="2026-09-29")
        celh = data.stocks["CELH"]
        self.assertEqual(celh.metrics.close_price, 38.50)
        self.assertEqual(celh.metrics.change_percent, 4.20)
        self.assertEqual(celh.metrics.volume, 4_850_000)

        enph = data.stocks["ENPH"]
        self.assertEqual(enph.metrics.close_price, 58.20)
        self.assertEqual(enph.metrics.change_percent, -3.36)
        self.assertEqual(enph.metrics.volume, 3_120_000)

    def test_celh_enph_one_paragraph_summary_and_2line_watchpoints(self) -> None:
        """Verify 1-paragraph summary synthesis and 2-line key watch points for CELH and ENPH."""
        text = """
## 1. 셀시우스 (CELH)
- 종가: $38.50
- 등락률: +4.20%
- 거래량: 4.85M
- 주요 동인: 펩시 유통망 재고 조정 완료 및 점유율 상승
- Fact vs Noise:
  - 공시 팩트: 3분기 북미 스캐너 데이터 매출 반등 확인.
  - 시장 노이즈: 유통 파트너십 결별 루머는 일시적 불안 심리임.
- Line 1: $35.00 지지선 및 단기 공매도 숏커버링 수급선
- Line 2: 차기 분기 유럽 진출 가이던스 및 신제품 양산 일정

## 2. 엔페이즈 (ENPH)
- 종가: $58.20
- 등락률: -3.36%
- 거래량: 3.12M
- 주요 동인: Enphase Air 마이크로인버터 혁신 발표
- Fact vs Noise:
  - 공시 팩트: 유럽 유통 채널 정상화 및 신제품 출하 시작.
  - 시장 노이즈: 고금리 장기화에 따른 태양광 수요 위축 과민반응.
- Line 1: $55.00 주요 지지선 및 태양광 ETF(TAN) 패시브 수급
- Line 2: IQ9 마이크로인버터 양산 및 NEM 3.0 배터리 부착률 체크포인트
"""
        data = self.extractor.extract(text, date_override="2026-09-29")
        self.assertIn("CELH", data.stocks)
        self.assertIn("ENPH", data.stocks)

        celh = data.stocks["CELH"]
        self.assertTrue(len(celh.one_paragraph_summary) > 30, "CELH summary too short")
        self.assertIn("셀시우스", celh.one_paragraph_summary)
        self.assertTrue(celh.key_points.line1_short_term.startswith("$35.00 지지선"))
        self.assertTrue(celh.key_points.line2_mid_long_term.startswith("차기 분기 유럽 진출"))

        enph = data.stocks["ENPH"]
        self.assertTrue(len(enph.one_paragraph_summary) > 30, "ENPH summary too short")
        self.assertIn("엔페이즈", enph.one_paragraph_summary)
        self.assertTrue(enph.key_points.line1_short_term.startswith("$55.00 주요 지지선"))
        self.assertTrue(enph.key_points.line2_mid_long_term.startswith("IQ9 마이크로인버터"))

    def test_celh_enph_macro_shock_attribution(self) -> None:
        """Verify direct macro attribution for ENPH and UPST upon interest rate shocks."""
        text = """
## 글로벌 거시 매크로 동향
미 국채 10년물 금리 급등 및 고금리 장기화로 자금 조달비용 상승 압박.

## 1. 엔페이즈 (ENPH)
- 종가: $58.20
- 등락률: -3.36%
- 거래량: 3.12M
- 주요 동인: 주거용 태양광 인버터 수요 점검
"""
        data = self.extractor.extract(text, date_override="2026-09-29")
        enph = data.stocks["ENPH"]
        self.assertIn("고금리", enph.macro_attribution)
        self.assertIn("주거용 태양광", enph.macro_attribution)
        self.assertIn("태양광", enph.one_paragraph_summary)


class TestExecutiveInterviewExtraction(unittest.TestCase):
    """Stress tests for John Fieldly (CELH) and Badri Kothandaraman (ENPH) interview extraction."""

    def setUp(self) -> None:
        self.extractor = FactExtractor()

    def test_john_fieldly_interview_extraction_bulleted(self) -> None:
        """Extract John Fieldly executive interview details, quotes, and URL (bulleted format)."""
        text = """
## 셀시우스 (CELH)
- 종가: $38.50
- 등락률: +4.20%
- 경영진 인터뷰:
  - 존 필들리(John Fieldly) 최고경영자(CEO) 인터뷰:
  "북미 에너지 드링크 시장에서 셀시우스의 점유율 반등은 구조적이며, 펩시와의 글로벌 파트너십은 강력합니다."
  - 출처: https://www.bloomberg.com/news/celsius-fieldly-interview
"""
        data = self.extractor.extract(text, date_override="2026-09-29")
        celh = data.stocks.get("CELH")
        self.assertIsNotNone(celh)
        self.assertTrue(len(celh.interviews) >= 1, "Failed to extract John Fieldly interview")
        inv = celh.interviews[0]
        self.assertEqual(inv.speaker_name, "존 필들리")
        self.assertIn("최고경영자", inv.speaker_title)
        self.assertIn("셀시우스", inv.affiliation)
        self.assertEqual(inv.source_url, "https://www.bloomberg.com/news/celsius-fieldly-interview")
        self.assertTrue(len(inv.core_quotes) >= 1)
        self.assertIn("점유율 반등은 구조적", inv.core_quotes[0])

    def test_badri_kothandaraman_interview_extraction_bulleted(self) -> None:
        """Extract Badri Kothandaraman executive interview details, quotes, and URL (bulleted format)."""
        text = """
## 엔페이즈 (ENPH)
- 종가: $58.20
- 등락률: -3.36%
- 경영진 인터뷰:
  - 바드리 코탄다라만(Badri Kothandaraman) 대표이사 인터뷰:
  "Enphase Air 시스템은 전력망 독립형 주거 에너지의 새로운 패러다임이며 글로벌 확장의 열쇠입니다."
  - 출처: https://enphase.com/news/badri-keynote-2026
"""
        data = self.extractor.extract(text, date_override="2026-09-29")
        enph = data.stocks.get("ENPH")
        self.assertIsNotNone(enph)
        self.assertTrue(len(enph.interviews) >= 1, "Failed to extract Badri Kothandaraman interview")
        inv = enph.interviews[0]
        self.assertEqual(inv.speaker_name, "바드리 코탄다라만")
        self.assertIn("최고경영자", inv.speaker_title)
        self.assertIn("엔페이즈", inv.affiliation)
        self.assertEqual(inv.source_url, "https://enphase.com/news/badri-keynote-2026")
        self.assertTrue(len(inv.core_quotes) >= 1)
        self.assertIn("전력망 독립형", inv.core_quotes[0])


class TestNegativeCollisionAdversarial(unittest.TestCase):
    """Adversarial stress testing against negative collisions and false positive instantiations."""

    def setUp(self) -> None:
        self.extractor = FactExtractor()

    def test_negative_collision_phase_2_clinical_trial(self) -> None:
        """'Phase 2 임상시험' must NOT trigger ENPH (Enphase)."""
        text = """
## 1. 바이오 신약 개발 현황
- 주요 파이프라인의 Phase 2 임상시험 환자 모집 완료.
- Phase 2 임상 데이터는 올해 하반기 공개 예정.
"""
        data = self.extractor.extract(text, date_override="2026-09-29")
        self.assertNotIn("ENPH", data.stocks, "FALSE POSITIVE: 'Phase 2 임상시험' triggered ENPH!")

    def test_negative_collision_influencer_marketing(self) -> None:
        """'인플루언서 마케팅' must NOT trigger FLNC (Fluence)."""
        text = """
## 1. 소비재 마케팅 전략
- SNS 인플루언서 마케팅 예산 집행 증액.
- 인플루언서 협업 콘텐츠를 통한 바이럴 확산.
"""
        data = self.extractor.extract(text, date_override="2026-09-29")
        self.assertNotIn("FLNC", data.stocks, "FALSE POSITIVE: '인플루언서 마케팅' triggered FLNC!")

    def test_negative_collision_times_square(self) -> None:
        """'타임스퀘어' must NOT trigger SK_SQUARE (SK Square)."""
        text = """
## 1. 글로벌 옥외 광고 현황
- 뉴욕 타임스퀘어(Times Square) 빌보드 광고 집행.
- 타임스퀘어 광장 유동인구 대상 브랜드 노출.
"""
        data = self.extractor.extract(text, date_override="2026-09-29")
        self.assertNotIn("SK_SQUARE", data.stocks, "FALSE POSITIVE: '타임스퀘어' triggered SK_SQUARE!")

    def test_negative_collision_peer_comparison_list_no_phantom_enph(self) -> None:
        """Competitor peer mention '[피어 비교] ... 인페이즈(-3.36%)' must NOT instantiate ENPH."""
        text = """
## 1. 플루언스에너지 (FLNC)
- 종가: $7.82
- 등락률: -0.64%

[섹터 및 피어 비교]
- 선런(Sunrun, -4.32%), 인페이즈(Enphase, -3.36%), 퍼스트솔라(First Solar, -2.52%)
"""
        data = self.extractor.extract(text, date_override="2026-09-29")
        self.assertIn("FLNC", data.stocks)
        self.assertNotIn("ENPH", data.stocks, "FALSE POSITIVE: Peer comparison list instantiated ENPH!")


class TestEmpiricalBugProbes(unittest.TestCase):
    """Pinpointed empirical tests exposing reproducible bugs in engine/extractor.py."""

    def setUp(self) -> None:
        self.extractor = FactExtractor()

    def test_bug_probe_1_celsius_temperature_collision(self) -> None:
        """BUG PROBE 1: '섭씨 35도 (Celsius)' in weather notes falsely instantiates CELH.

        Root Cause in engine/extractor.py:
        Line 375 & Line 440: Regex includes bare `\bCelsius\b` without negative guard against
        temperature / degree words ('섭씨', '도', '기온', '℃').
        In `_classify_line_or_paragraph`, `\bCelsius\b` earns score 4 (>= 3), assigning the
        line to `sections['CELH']` and instantiating CELH with close_price=None.
        """
        text = """
## 오늘의 날씨 및 기후
- 금일 서울 낮 최고 기온은 섭씨 35도 (Celsius)를 기록하며 폭염 경보가 발효되었습니다.
- 무더위로 인한 전력 소비량 급증 및 에어컨 가동률 증가.
"""
        data = self.extractor.extract(text, date_override="2026-09-29")
        # When this assertion fails, it confirms the bug exists!
        self.assertNotIn(
            "CELH",
            data.stocks,
            "EMPIRICAL BUG REPRODUCED: '섭씨 35도 (Celsius)' weather text falsely instantiated CELH!"
        )

    def test_bug_probe_2_short_unbulleted_url_classified_as_header(self) -> None:
        """BUG PROBE 2: Unbulleted short URLs containing stock keywords are misclassified as headers and dropped.

        Root Cause in engine/extractor.py:
        `_identify_section_header` treats any non-bulleted line <= 65 chars not ending in Korean verb
        suffixes as `is_short_title = True`.
        `출처 링크: https://www.bloomberg.com/news/celsius-fieldly-interview` (64 chars)
        matches `\bCelsius\b`, so `_identify_section_header` returns 'CELH'.
        In `_segment_document`, headers are skipped (`continue`), so the URL is deleted from section
        content, leaving `inv.source_url` empty!
        """
        text = """
## 셀시우스 (CELH)
- 종가: $38.50
- 등락률: +4.20%
- 경영진 인터뷰:
  - 존 필들리(John Fieldly) 최고경영자(CEO) 인터뷰:
  "북미 에너지 드링크 시장에서 점유율 반등은 구조적입니다."
  출처 링크: https://www.bloomberg.com/news/celsius-fieldly-interview
"""
        data = self.extractor.extract(text, date_override="2026-09-29")
        celh = data.stocks.get("CELH")
        self.assertIsNotNone(celh)
        self.assertTrue(len(celh.interviews) >= 1)
        # When this assertion fails, it confirms the URL dropping bug!
        self.assertEqual(
            celh.interviews[0].source_url,
            "https://www.bloomberg.com/news/celsius-fieldly-interview",
            "EMPIRICAL BUG REPRODUCED: Short unbulleted URL line was discarded as a false header!"
        )

    def test_bug_probe_3_casual_mention_with_gwanryeonjuga(self) -> None:
        """BUG PROBE 3: Casual sector mention containing '관련주가' falsely triggers stock presence.

        Root Cause in engine/extractor.py:
        In `_is_stock_present` (Line 248):
        `re.search(r'(?:종가|마감가|현재가|주가|...)', content)`
        matches '주가' inside the compound word '관련주가' ('관련주' + '가'),
        causing fallback instantiation of ENPH even though no ENPH price, volume, or driver exists.
        """
        text = """
## 플루언스에너지 (FLNC)
- 종가: $7.82
- 등락률: -0.64%

태양광 및 ESS 시장 전반에서 선런 및 엔페이즈 등 관련주가 동반 약세를 기록했습니다.
"""
        data = self.extractor.extract(text, date_override="2026-09-29")
        self.assertIn("FLNC", data.stocks)
        # When this assertion fails, it confirms phantom stock instantiation on '관련주가'!
        self.assertNotIn(
            "ENPH",
            data.stocks,
            "EMPIRICAL BUG REPRODUCED: '엔페이즈 등 관련주가 동반 약세' falsely instantiated ENPH with price=None!"
        )


if __name__ == "__main__":
    unittest.main()
