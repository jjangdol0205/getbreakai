"""Unit tests for engine.digest_generator (Daily Multi-Stock Digest Markdown Generator).

Validates:
- Generation of D:/투자홈페이지/관심종목_백업_20261030/daily_digest/YYYY-MM-DD_digest.md
- Strict compliance with the 5 required markdown sections:
  1. 당일 거시 매크로 및 6종목 상대 성과 요약 (Macro Overview & 6-Stock Comparative Matrix)
  2. 종목별 핵심 동인 및 팩트 vs 노이즈 판별 (Fact vs Noise for 6 Stocks)
  3. 경영진 인터뷰 궤적 및 이전 발언 대조 (Interview Trajectory Analysis)
  4. 포트폴리오 비중 진단 및 전술적 대응 가이드 (SK Square 57.6% vs SK Hynix 42.3% & 역스위칭 경고)
  5. 익일 모니터링 체크포인트
- Output file path, UTF-8 encoding, comparative markdown table formatting.
"""

import os
import tempfile
import unittest
from pathlib import Path
from typing import Any, Dict

from tests.fixtures.sample_dumps import (
    SAMPLE_RAW_DUMP_FULL_DAY,
    EXPECTED_EXTRACTED_FACTS_20260929,
)

try:
    import engine.digest_generator as digest_module
    DIGEST_AVAILABLE = True
except ImportError:
    DIGEST_AVAILABLE = False

try:
    from engine.cleaner import clean_raw_dump
    from engine.extractor import extract_facts
    from engine.models import DailyMarketData
    EXTRACTION_PIPELINE_AVAILABLE = True
except ImportError:
    EXTRACTION_PIPELINE_AVAILABLE = False


def generate_digest_helper(market_data: Any, output_dir: str = "") -> str:
    """Helper to invoke digest generator regardless of API shape."""
    if hasattr(digest_module, "generate_digest"):
        try:
            return digest_module.generate_digest(market_data, output_dir=output_dir)
        except TypeError:
            return digest_module.generate_digest(market_data)
    if hasattr(digest_module, "DigestGenerator"):
        instance = digest_module.DigestGenerator(output_dir=output_dir) if output_dir else digest_module.DigestGenerator()
        if hasattr(instance, "generate"):
            try:
                return instance.generate(market_data, output_dir=output_dir)
            except TypeError:
                return instance.generate(market_data)
        elif hasattr(instance, "build_markdown"):
            return instance.build_markdown(market_data)
    raise AttributeError("No recognizable digest generation function in engine.digest_generator")


@unittest.skipUnless(DIGEST_AVAILABLE and EXTRACTION_PIPELINE_AVAILABLE, "digest_generator or extraction pipeline not yet available")
class TestDigestGeneratorStructure(unittest.TestCase):
    """Tier 1: 5-Section Markdown Schema Validation."""

    @classmethod
    def setUpClass(cls) -> None:
        cleaned_text, _ = clean_raw_dump(SAMPLE_RAW_DUMP_FULL_DAY)
        cls.market_data = extract_facts(cleaned_text, date="2026-09-29")
        cls.temp_dir = tempfile.TemporaryDirectory(ignore_cleanup_errors=True)
        cls.digest_content = generate_digest_helper(cls.market_data, output_dir=cls.temp_dir.name)

    @classmethod
    def tearDownClass(cls) -> None:
        try:
            cls.temp_dir.cleanup()
        except Exception:
            pass

    def test_header_and_title(self) -> None:
        """Validates title with date and callout boxes."""
        self.assertTrue(
            "일간 8개 관심종목 종합 다이제스트" in self.digest_content or "일간 6개 관심종목 종합 다이제스트" in self.digest_content
        )
        self.assertIn("2026-09-29", self.digest_content)
        self.assertTrue(
            "> **일간 시장 총평**:" in self.digest_content or "시장 총평" in self.digest_content,
            "Must contain daily market summary callout",
        )
        self.assertTrue(
            "포트폴리오 핵심 지침" in self.digest_content or "핵심 지침" in self.digest_content,
            "Must contain portfolio tactical guidance callout",
        )

    def test_section_1_macro_and_comparative_matrix_table(self) -> None:
        """Section 1: Comparative matrix table containing all 8 stocks."""
        self.assertTrue(
            "비교 매트릭스" in self.digest_content or "상대 성과" in self.digest_content or "Comparative" in self.digest_content
        )

        # Comparative table must list all 8 stocks with tickers
        for stock_id in ["SK스퀘어", "SK하이닉스", "우버", "모빌아이", "플루언스", "업스타트", "셀시우스", "엔페이즈"]:
            self.assertIn(stock_id, self.digest_content, f"Section 1 must include {stock_id}")

        for ticker in ["402340", "000660", "UBER", "MBLY", "FLNC", "UPST", "CELH", "ENPH"]:
            self.assertIn(ticker, self.digest_content, f"Comparative table must include ticker {ticker}")

        # Check table formatting tokens
        self.assertIn("|", self.digest_content)
        self.assertIn("---", self.digest_content)

    def test_section_2_drivers_and_fact_vs_noise(self) -> None:
        """Section 2: Stock-by-stock core drivers and Fact vs Noise classification."""
        self.assertTrue(
            "2. 종목별 핵심 동인" in self.digest_content or "핵심 동인 및 팩트 vs 노이즈" in self.digest_content
        )
        # Should contain noise and fact markers
        self.assertTrue("노이즈" in self.digest_content or "Noise" in self.digest_content)
        self.assertTrue("팩트" in self.digest_content or "Fact" in self.digest_content)

        # Specific drivers
        self.assertTrue(
            "솔리다임" in self.digest_content or "Solidigm" in self.digest_content,
            "Must mention Solidigm in SK Square section",
        )
        self.assertTrue(
            "HBM" in self.digest_content,
            "Must mention HBM in SK Hynix section",
        )

    def test_section_3_executive_interview_trajectory(self) -> None:
        """Section 3: Executive interview trajectory and comparison with previous statements."""
        self.assertTrue(
            "3. 경영진 인터뷰 궤적" in self.digest_content or "인터뷰 궤적" in self.digest_content or "Trajectory" in self.digest_content
        )
        # Must include BCG partner or 삼프로TV or quote
        self.assertTrue(
            "김창욱" in self.digest_content or "BCG" in self.digest_content or "EBITDA는 멀쩡" in self.digest_content
        )

    def test_section_4_portfolio_pair_and_reverse_switching_warning(self) -> None:
        """Section 4: Portfolio pair (SK Square 57.6% vs SK Hynix 42.3%) & Reverse Switching Warning."""
        self.assertTrue(
            "4. 포트폴리오 비중" in self.digest_content or "포트폴리오" in self.digest_content
        )
        self.assertIn("57.6%", self.digest_content)
        self.assertIn("42.3%", self.digest_content)
        self.assertTrue(
            "역스위칭" in self.digest_content or "스위칭" in self.digest_content,
            "Must warn about reverse switching risk",
        )
        self.assertTrue(
            "HOLD" in self.digest_content or "보류" in self.digest_content or "유지" in self.digest_content
        )

    def test_section_5_next_day_monitoring_checkpoints(self) -> None:
        """Section 5: Next day monitoring checkpoints."""
        self.assertTrue(
            "5. 익일 모니터링" in self.digest_content or "체크포인트" in self.digest_content or "모니터링" in self.digest_content
        )


@unittest.skipUnless(DIGEST_AVAILABLE and EXTRACTION_PIPELINE_AVAILABLE, "digest_generator not yet available")
class TestDigestGeneratorFileSystem(unittest.TestCase):
    """Tier 3: File system output and encoding."""

    def test_output_file_creation_and_utf8(self) -> None:
        """Generates daily_digest/YYYY-MM-DD_digest.md in specified directory."""
        with tempfile.TemporaryDirectory(ignore_cleanup_errors=True) as tmp_dir:
            cleaned_text, _ = clean_raw_dump(SAMPLE_RAW_DUMP_FULL_DAY)
            market_data = extract_facts(cleaned_text, date="2026-09-29")
            generate_digest_helper(market_data, output_dir=tmp_dir)

            expected_file = Path(tmp_dir) / "daily_digest" / "2026-09-29_digest.md"
            if not expected_file.exists():
                # Check directly under tmp_dir
                expected_file = Path(tmp_dir) / "2026-09-29_digest.md"

            self.assertTrue(expected_file.exists(), f"Digest file must be created at {expected_file}")

            # Verify UTF-8 reading without error
            content = expected_file.read_text(encoding="utf-8")
            self.assertIn("SK하이닉스", content)
            self.assertIn("SK스퀘어", content)


if __name__ == "__main__":
    unittest.main()
