"""End-to-End (E2E) Integration Tests for Multi-Stock Investment System.

Covers Tier 4 Workload and Real-World Application Scenarios:
1. Scenario 1: Complete daily workflow (Raw Dump -> Clean -> Extract -> Digest -> data.js).
2. Scenario 2: Incomplete dump scenario (3 stocks only, graceful degradation).
3. Scenario 3: Multi-day sequential ingestion (Day 1: 2026-09-29, Day 2: 2026-09-30).
4. Scenario 4: Heavy adversarial noise injection (BOM, zero-width spaces, markdown code fences).
5. Scenario 5: CLI interface execution (engine.cli clean & parse).
"""

import json
import tempfile
import unittest
from pathlib import Path
from typing import Any, Dict

from tests.fixtures.sample_dumps import (
    SAMPLE_RAW_DUMP_FULL_DAY,
    SAMPLE_RAW_DUMP_PARTIAL_STOCKS,
    SAMPLE_RAW_DUMP_DAY2,
    SAMPLE_RAW_DUMP_ADVERSARIAL_NOISE,
)

try:
    from engine.cleaner import RawDumpCleaner, clean_raw_dump
    from engine.extractor import FactExtractor, extract_facts
    from engine.cli import main as cli_main
    CORE_ENGINE_AVAILABLE = True
except ImportError:
    CORE_ENGINE_AVAILABLE = False

try:
    import engine.digest_generator as digest_module
    DIGEST_AVAILABLE = True
except ImportError:
    DIGEST_AVAILABLE = False

try:
    import engine.sync_dashboard as sync_module
    SYNC_AVAILABLE = True
except ImportError:
    SYNC_AVAILABLE = False


@unittest.skipUnless(CORE_ENGINE_AVAILABLE, "Core engine (cleaner/extractor/cli) not yet available")
class TestE2EDailyPipeline(unittest.TestCase):
    """Tier 4: Scenario 1 - Complete daily processing workflow."""

    def test_full_pipeline_raw_dump_to_market_data(self) -> None:
        """Runs raw dump through cleaner and extractor, verifying consolidated output."""
        # Step 1: Clean raw dump
        cleaner = RawDumpCleaner()
        cleaned_text, metadata = cleaner.clean_with_metadata(SAMPLE_RAW_DUMP_FULL_DAY)

        self.assertNotIn("Google Gemini", cleaned_text)
        self.assertNotIn("YouTube 서비스 약관", cleaned_text)
        self.assertEqual(metadata["date_hint"], "2026-09-29")

        # Step 2: Extract structured market facts
        extractor = FactExtractor()
        market_data = extractor.extract(cleaned_text, date_override=metadata["date_hint"])

        self.assertEqual(market_data.date, "2026-09-29")
        self.assertEqual(len(market_data.stocks), 8)

        # Check all 8 stocks present
        expected_stocks = {"SK_SQUARE", "SK_HYNIX", "UBER", "MBLY", "FLNC", "UPST", "CELH", "ENPH"}
        self.assertEqual(set(market_data.stocks.keys()), expected_stocks)

        # Verify key metrics
        self.assertEqual(market_data.stocks["SK_SQUARE"].metrics.close_price, 1100000.0)
        self.assertEqual(market_data.stocks["SK_HYNIX"].metrics.close_price, 176700.0)
        self.assertAlmostEqual(market_data.stocks["UBER"].metrics.close_price, 68.16, places=2)
        self.assertAlmostEqual(market_data.stocks["MBLY"].metrics.close_price, 7.795, places=3)
        self.assertAlmostEqual(market_data.stocks["FLNC"].metrics.close_price, 7.50, places=2)
        self.assertAlmostEqual(market_data.stocks["UPST"].metrics.close_price, 23.03, places=2)
        self.assertAlmostEqual(market_data.stocks["CELH"].metrics.close_price, 32.45, places=2)
        self.assertAlmostEqual(market_data.stocks["ENPH"].metrics.close_price, 98.20, places=2)

        # Verify portfolio pair strategy
        self.assertAlmostEqual(market_data.pair_strategy.sk_square_weight, 57.6, places=1)
        self.assertAlmostEqual(market_data.pair_strategy.sk_hynix_weight, 42.3, places=1)
        self.assertIn("HOLD", market_data.pair_strategy.tactical_action.upper())

        # Step 3: Optional Digest Generation (if available)
        if DIGEST_AVAILABLE:
            with tempfile.TemporaryDirectory(ignore_cleanup_errors=True) as tmp_dir:
                digest_path = Path(tmp_dir) / "2026-09-29_digest.md"
                if hasattr(digest_module, "generate_digest"):
                    content = digest_module.generate_digest(market_data, output_dir=tmp_dir)
                    self.assertTrue(
                        "일간 8개 관심종목 종합 다이제스트" in content or "일간 6개 관심종목 종합 다이제스트" in content
                    )


@unittest.skipUnless(CORE_ENGINE_AVAILABLE, "Core engine not yet available")
class TestE2EPartialDump(unittest.TestCase):
    """Tier 4: Scenario 2 - Incomplete dump containing only 3 stocks."""

    def test_partial_dump_pipeline(self) -> None:
        """Processes a partial dump without crashing or fabricating missing stocks."""
        cleaned_text, meta = clean_raw_dump(SAMPLE_RAW_DUMP_PARTIAL_STOCKS)
        market_data = extract_facts(cleaned_text, date="2026-09-29")

        # Must extract the 3 present stocks
        self.assertEqual(len(market_data.stocks), 3)
        self.assertIn("SK_HYNIX", market_data.stocks)
        self.assertIn("SK_SQUARE", market_data.stocks)
        self.assertIn("UBER", market_data.stocks)

        # Must NOT fabricate missing stocks
        self.assertNotIn("MBLY", market_data.stocks)
        self.assertNotIn("FLNC", market_data.stocks)
        self.assertNotIn("UPST", market_data.stocks)


@unittest.skipUnless(CORE_ENGINE_AVAILABLE, "Core engine not yet available")
class TestE2EMultiDayIngestion(unittest.TestCase):
    """Tier 4: Scenario 3 - Sequential ingestion of consecutive trading days."""

    def test_multi_day_sequential_processing(self) -> None:
        """Ingests Day 1 (2026-09-29) followed by Day 2 (2026-09-30)."""
        # Day 1
        cleaned_day1, _ = clean_raw_dump(SAMPLE_RAW_DUMP_FULL_DAY)
        data_day1 = extract_facts(cleaned_day1, date="2026-09-29")
        self.assertEqual(data_day1.date, "2026-09-29")
        self.assertEqual(data_day1.stocks["SK_HYNIX"].metrics.close_price, 176700.0)

        # Day 2
        cleaned_day2, _ = clean_raw_dump(SAMPLE_RAW_DUMP_DAY2)
        data_day2 = extract_facts(cleaned_day2, date="2026-09-30")
        self.assertEqual(data_day2.date, "2026-09-30")
        self.assertEqual(data_day2.stocks["SK_HYNIX"].metrics.close_price, 182500.0)
        self.assertAlmostEqual(data_day2.stocks["SK_HYNIX"].metrics.change_percent, 3.28, places=2)

        # Verify independence of the two data objects
        self.assertNotEqual(data_day1.date, data_day2.date)
        self.assertNotEqual(
            data_day1.stocks["SK_HYNIX"].metrics.close_price,
            data_day2.stocks["SK_HYNIX"].metrics.close_price,
        )


@unittest.skipUnless(CORE_ENGINE_AVAILABLE, "Core engine not yet available")
class TestE2EAdversarialNoiseInjection(unittest.TestCase):
    """Tier 4 & Tier 5: Scenario 4 - Heavy noise injection with BOM, zero-width chars, codeblocks."""

    def test_adversarial_noise_resilience(self) -> None:
        """Pipeline must succeed even when inputs contain weird Unicode and markdown wrappers."""
        cleaned_text, meta = clean_raw_dump(SAMPLE_RAW_DUMP_ADVERSARIAL_NOISE)

        # BOM and zero-width chars must be eliminated
        self.assertNotIn("\uFEFF", cleaned_text)
        self.assertNotIn("\u200B", cleaned_text)

        # Stocks must still be successfully extracted
        market_data = extract_facts(cleaned_text, date="2026-09-29")
        self.assertEqual(len(market_data.stocks), 6)
        self.assertEqual(market_data.stocks["SK_HYNIX"].metrics.close_price, 176700.0)
        self.assertEqual(market_data.stocks["SK_SQUARE"].metrics.close_price, 1100000.0)


@unittest.skipUnless(CORE_ENGINE_AVAILABLE, "Core engine not yet available")
class TestE2ECommandLineInterface(unittest.TestCase):
    """Tier 4: Scenario 5 - CLI command verification."""

    def test_cli_clean_command(self) -> None:
        """CLI 'clean' command processes file and writes output."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            input_file = Path(tmp_dir) / "raw.txt"
            output_file = Path(tmp_dir) / "cleaned.txt"

            input_file.write_text(SAMPLE_RAW_DUMP_FULL_DAY, encoding="utf-8")

            exit_code = cli_main(["clean", "-i", str(input_file), "-o", str(output_file)])
            self.assertEqual(exit_code, 0)
            self.assertTrue(output_file.exists())

            cleaned_content = output_file.read_text(encoding="utf-8")
            self.assertNotIn("Google Gemini", cleaned_content)
            self.assertIn("176,700원", cleaned_content)

    def test_cli_parse_command_to_json(self) -> None:
        """CLI 'parse' command produces valid structured JSON output."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            input_file = Path(tmp_dir) / "raw.txt"
            output_file = Path(tmp_dir) / "facts.json"

            input_file.write_text(SAMPLE_RAW_DUMP_FULL_DAY, encoding="utf-8")

            exit_code = cli_main(["parse", "-i", str(input_file), "-o", str(output_file), "-d", "2026-09-29"])
            self.assertEqual(exit_code, 0)
            self.assertTrue(output_file.exists())

            facts = json.loads(output_file.read_text(encoding="utf-8"))
            self.assertEqual(facts["date"], "2026-09-29")
            self.assertIn("stocks", facts)
            self.assertIn("SK_HYNIX", facts["stocks"])
            self.assertIn("SK_SQUARE", facts["stocks"])


if __name__ == "__main__":
    unittest.main()
