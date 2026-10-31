"""Unit tests for engine.cleaner (RawDumpCleaner).

Testing Methodology:
- Category-Partition: Tests each of the 8 distinct UI noise classes in isolation and combination.
- Boundary Value Analysis (BVA): Empty inputs, whitespace-only, pure noise, pure content, large inputs.
- Preservation Verification: Ensures financial facts, URLs, and quotes are 100% preserved.
"""

import unittest
from typing import Dict, Any

from tests.fixtures.sample_dumps import (
    SAMPLE_RAW_DUMP_FULL_DAY,
    SAMPLE_RAW_DUMP_DIRTY_NOISE_ONLY,
    SAMPLE_RAW_DUMP_ADVERSARIAL_NOISE,
)

try:
    from engine.cleaner import RawDumpCleaner, clean_raw_dump
    CLEANER_AVAILABLE = True
except ImportError:
    CLEANER_AVAILABLE = False


@unittest.skipUnless(CLEANER_AVAILABLE, "engine.cleaner is not yet available")
class TestCleanerCategoryPartition(unittest.TestCase):
    """Tier 1 & Tier 2: Category-Partition tests covering each noise category."""

    def setUp(self) -> None:
        self.cleaner = RawDumpCleaner()

    def test_category_1_ui_chrome_navigation(self) -> None:
        """Category 1: Gemini chrome, navigation headers, account menus."""
        raw = (
            "Google Gemini\n"
            "Gemini Advanced\n"
            "새 대화\n"
            "최근 대화\n"
            "도움말\n"
            "설정\n"
            "Google 계정\n"
            "## 1. SK하이닉스\n"
            "종가: 176,700원\n"
        )
        cleaned, meta = self.cleaner.clean_with_metadata(raw)
        self.assertNotIn("Google Gemini", cleaned)
        self.assertNotIn("Gemini Advanced", cleaned)
        self.assertNotIn("새 대화", cleaned)
        self.assertNotIn("Google 계정", cleaned)
        self.assertIn("## 1. SK하이닉스", cleaned)
        self.assertIn("176,700원", cleaned)
        self.assertGreater(meta["removed_categories"]["ui_chrome"], 0)

    def test_category_2_model_markers_and_timestamps(self) -> None:
        """Category 2: Timestamps, editing indicators, answer sequence counters."""
        raw = (
            "2026. 9. 29. 오전 8:15:30\n"
            "수정됨\n"
            "답변 1 / 1\n"
            "방금\n"
            "우버: $68.16\n"
        )
        cleaned, meta = self.cleaner.clean_with_metadata(raw)
        self.assertNotIn("2026. 9. 29. 오전 8:15:30", cleaned)
        self.assertNotIn("수정됨", cleaned)
        self.assertNotIn("답변 1", cleaned)
        self.assertIn("우버: $68.16", cleaned)
        self.assertGreater(meta["removed_categories"]["timestamps"], 0)

    def test_category_3_user_prompts_and_chatter(self) -> None:
        """Category 3: User prompt lines and AI introductory/closing pleasantries."""
        raw = (
            "나: 오늘 6개 관심종목 시황 알려줘\n"
            "네, 요청하신 6개 관심 종목의 시황 브리핑입니다.\n"
            "모빌아이 종가 $7.795\n"
            "도움이 되셨기를 바랍니다. 추가 질문이 있으시면 언제든지 말씀해 주세요.\n"
        )
        cleaned, meta = self.cleaner.clean_with_metadata(raw)
        self.assertNotIn("나: 오늘", cleaned)
        self.assertNotIn("요청하신 6개 관심 종목", cleaned)
        self.assertNotIn("도움이 되셨기를 바랍니다", cleaned)
        self.assertIn("모빌아이 종가 $7.795", cleaned)
        self.assertGreater(meta["removed_categories"]["user_prompt"], 0)

    def test_category_4_legal_financial_disclaimers(self) -> None:
        """Category 4: AI hallucination caveats and financial investment disclaimers."""
        raw = (
            "플루언스에너지 종가 $7.50\n"
            "Gemini는 사람, 장소 또는 사실에 대해 부정확한 정보를 표시할 수 있으므로 Gemini의 대답을 한 번 더 확인하세요.\n"
            "본 자료는 정보 제공만을 목적으로 하며 투자 권유를 위한 것이 아닙니다.\n"
            "개인정보처리방침\n"
            "서비스 약관\n"
        )
        cleaned, meta = self.cleaner.clean_with_metadata(raw)
        self.assertNotIn("부정확한 정보를 표시할 수 있으므로", cleaned)
        self.assertNotIn("투자 권유를 위한 것이 아닙니다", cleaned)
        self.assertNotIn("개인정보처리방침", cleaned)
        self.assertNotIn("서비스 약관", cleaned)
        self.assertIn("플루언스에너지 종가 $7.50", cleaned)
        self.assertGreater(meta["removed_categories"]["disclaimers"], 0)

    def test_category_5_youtube_widget_noise_and_preservation(self) -> None:
        """Category 5: Strips player controls but STRICTLY PRESERVES valid URLs."""
        raw = (
            "영상 링크: https://youtu.be/jSm5Gd8qEOA?si=VLQIYymu6TG0-D_P\n"
            "동영상 시청 시 YouTube 서비스 약관이 적용됩니다.\n"
            "자막\n"
            "음소거\n"
            "음소거 해제\n"
            "재생\n"
            "일시중지\n"
            "전체화면\n"
            "구독\n"
            "좋아요\n"
            "공유\n"
            "핵심 발언: EBITDA는 멀쩡\n"
        )
        cleaned, meta = self.cleaner.clean_with_metadata(raw)
        # URL must be retained!
        self.assertIn("https://youtu.be/jSm5Gd8qEOA?si=VLQIYymu6TG0-D_P", cleaned)
        self.assertIn("핵심 발언: EBITDA는 멀쩡", cleaned)
        # Widget noise must be stripped
        self.assertNotIn("동영상 시청 시 YouTube", cleaned)
        self.assertNotIn("음소거 해제", cleaned)
        self.assertNotIn("전체화면", cleaned)
        self.assertGreater(meta["removed_categories"]["media_widgets"], 0)

    def test_category_6_action_and_feedback_buttons(self) -> None:
        """Category 6: Export and feedback buttons rendered under AI responses."""
        raw = (
            "업스타트 종가 $23.03\n"
            "Google Docs로 내보내기\n"
            "Gmail로 임시보관 작성\n"
            "복사\n"
            "공유\n"
            "수정\n"
            "좋은 답변\n"
            "부정확한 답변\n"
            "피드백 제출\n"
            "더보기\n"
        )
        cleaned, meta = self.cleaner.clean_with_metadata(raw)
        self.assertNotIn("Google Docs로 내보내기", cleaned)
        self.assertNotIn("Gmail로 임시보관", cleaned)
        self.assertNotIn("피드백 제출", cleaned)
        self.assertIn("업스타트 종가 $23.03", cleaned)
        self.assertGreater(meta["removed_categories"]["action_buttons"], 0)

    def test_category_7_inline_citations_and_search_chips(self) -> None:
        """Category 7: Inline footnote brackets [1], [2], [출처] and search chips."""
        raw = (
            "G 검색어: SK하이닉스 3분기 실적\n"
            "출처 3개\n"
            "하이닉스 LTA 계약 체결 [1] 및 용인 메가팹 조기 착공 [출처].\n"
        )
        cleaned, meta = self.cleaner.clean_with_metadata(raw)
        self.assertNotIn("G 검색어:", cleaned)
        self.assertNotIn("출처 3개", cleaned)
        self.assertNotIn("[1]", cleaned)
        self.assertNotIn("[출처]", cleaned)
        self.assertIn("하이닉스 LTA 계약 체결", cleaned)
        self.assertIn("용인 메가팹 조기 착공", cleaned)
        self.assertGreater(meta["removed_categories"]["inline_citations"], 0)

    def test_category_8_character_normalization_and_fences(self) -> None:
        """Category 8: Strips BOM, zero-width chars, enclosing markdown fences, bullet symbols."""
        raw = (
            "\uFEFF```markdown\n"
            "• 우버 UBER: $68.16\n"
            "▶ SK\u200B하이닉스: 176,700원\n"
            "▪ SK\u200C스퀘어: 1,100,000원\n"
            "```\n"
        )
        cleaned, _ = self.cleaner.clean_with_metadata(raw)
        self.assertNotIn("\uFEFF", cleaned)
        self.assertNotIn("\u200B", cleaned)
        self.assertNotIn("\u200C", cleaned)
        self.assertNotIn("```", cleaned)
        self.assertIn("- 우버 UBER: $68.16", cleaned)
        self.assertIn("- SK하이닉스: 176,700원", cleaned)
        self.assertIn("- SK스퀘어: 1,100,000원", cleaned)


@unittest.skipUnless(CLEANER_AVAILABLE, "engine.cleaner is not yet available")
class TestCleanerBoundaryValueAnalysis(unittest.TestCase):
    """Tier 2: Boundary Value Analysis (BVA) for edge cases."""

    def setUp(self) -> None:
        self.cleaner = RawDumpCleaner()

    def test_bva_empty_string(self) -> None:
        """Empty input must produce empty string without crashing."""
        cleaned, meta = self.cleaner.clean_with_metadata("")
        self.assertEqual(cleaned, "")
        self.assertEqual(meta["original_length"], 0)
        self.assertEqual(meta["cleaned_length"], 0)

    def test_bva_whitespace_only(self) -> None:
        """Whitespace-only input must produce empty string."""
        cleaned, _ = self.cleaner.clean_with_metadata("   \n\n\t  \n  ")
        self.assertEqual(cleaned, "")

    def test_bva_pure_noise_dump(self) -> None:
        """Pure noise dump should result in empty or noise-free text."""
        cleaned, meta = self.cleaner.clean_with_metadata(SAMPLE_RAW_DUMP_DIRTY_NOISE_ONLY)
        # Verify no disclaimer or UI button remains
        self.assertNotIn("Gemini", cleaned)
        self.assertNotIn("YouTube", cleaned)
        self.assertNotIn("Google Docs", cleaned)
        self.assertNotIn("약관", cleaned)
        self.assertGreater(meta["removed_categories"]["ui_chrome"], 0)
        self.assertGreater(meta["removed_categories"]["disclaimers"], 0)

    def test_bva_pure_clean_content(self) -> None:
        """Input without any UI noise should preserve all lines."""
        content = (
            "## 1. SK하이닉스 (000660)\n"
            "- 종가: 176,700원\n"
            "- 등락률: -5.05%\n"
            "- 거래량: 3,210,000주\n"
        )
        cleaned, meta = self.cleaner.clean_with_metadata(content)
        self.assertIn("176,700원", cleaned)
        self.assertIn("-5.05%", cleaned)
        self.assertEqual(meta["removed_categories"]["ui_chrome"], 0)
        self.assertEqual(meta["removed_categories"]["disclaimers"], 0)

    def test_bva_consecutive_newlines_collapse(self) -> None:
        """More than 2 consecutive newlines must collapse to 2 newlines."""
        raw = "Line 1\n\n\n\n\n\nLine 2"
        cleaned, _ = self.cleaner.clean_with_metadata(raw)
        self.assertEqual(cleaned, "Line 1\n\nLine 2")

    def test_bva_date_hint_discovery(self) -> None:
        """Date hint discovers YYYY-MM-DD from various formats."""
        self.assertEqual(self.cleaner.extract_date_hint("2026. 9. 29. 오전 8:15"), "2026-09-29")
        self.assertEqual(self.cleaner.extract_date_hint("2026-09-30 마감 브리핑"), "2026-09-30")
        self.assertEqual(self.cleaner.extract_date_hint("2026년 10월 5일"), "2026-10-05")
        self.assertEqual(self.cleaner.extract_date_hint("날짜 없는 텍스트"), "")

    def test_full_day_dump_cleans_thoroughly(self) -> None:
        """Full day sample dump is thoroughly sanitized while keeping all 6 stocks."""
        cleaned, meta = self.cleaner.clean_with_metadata(SAMPLE_RAW_DUMP_FULL_DAY)
        # Check noise stripped
        self.assertNotIn("Google Gemini", cleaned)
        self.assertNotIn("Gemini Advanced", cleaned)
        self.assertNotIn("Google Docs로 내보내기", cleaned)
        self.assertNotIn("YouTube 서비스 약관", cleaned)
        self.assertNotIn("음소거", cleaned)
        self.assertNotIn("피드백 제출", cleaned)

        # Check all 8 stocks preserved
        for stock_name in ["SK스퀘어", "SK하이닉스", "우버", "모빌아이", "플루언스에너지", "업스타트", "셀시우스", "엔페이즈"]:
            self.assertIn(stock_name, cleaned, f"Stock {stock_name} must be preserved in cleaned text")

        # Check prices preserved
        self.assertIn("1,100,000원", cleaned)
        self.assertIn("176,700원", cleaned)
        self.assertIn("$68.16", cleaned)
        self.assertIn("$7.795", cleaned)
        self.assertIn("$7.50", cleaned)
        self.assertIn("$23.03", cleaned)
        self.assertIn("$32.45", cleaned)
        self.assertIn("$98.20", cleaned)

        # Check YouTube link preserved
        self.assertIn("https://youtu.be/jSm5Gd8qEOA", cleaned)
        self.assertEqual(meta["date_hint"], "2026-09-29")


if __name__ == "__main__":
    unittest.main()
