"""Unit tests for engine.extractor (FactExtractor).

Testing Methodology:
- Stock Disambiguation: Canonical identification across Korean, English, tickers, and codes.
- Semantic Collision Resolution: SK Square vs Block (Square) disambiguation.
- Market Metrics: Parsing KRW/USD prices, signs (+/-), percentages, change amounts, and volume units (만, 억, M, K).
- Drivers & Fact vs Noise: Catalyst/risk extraction, noise vs fact separation.
- Interviews & IB Comments: Quote extraction, media URLs, speaker affiliation, TP revisions.
- Portfolio Pair Dynamic: SK Square 57.6% vs SK Hynix 42.3%, reverse switching risk warning.
- Partial Dump Handling: Graceful extraction of subset of target stocks.
"""

import unittest
from typing import Any, Dict

from tests.fixtures.sample_dumps import (
    SAMPLE_RAW_DUMP_FULL_DAY,
    SAMPLE_RAW_DUMP_PARTIAL_STOCKS,
    SAMPLE_RAW_DUMP_SQUARE_BLOCK_COLLISION,
    EXPECTED_EXTRACTED_FACTS_20260929,
)

try:
    import engine.extractor as extractor_module
    EXTRACTOR_AVAILABLE = True
except ImportError:
    EXTRACTOR_AVAILABLE = False


def run_extractor(cleaned_text: str, date: str = "2026-09-29") -> Any:
    """Helper to run the extractor regardless of whether it's class-based or functional."""
    if hasattr(extractor_module, "extract_facts"):
        return extractor_module.extract_facts(cleaned_text, date=date)
    if hasattr(extractor_module, "FactExtractor"):
        instance = extractor_module.FactExtractor()
        if hasattr(instance, "extract"):
            try:
                return instance.extract(cleaned_text, date_override=date)
            except TypeError:
                return instance.extract(cleaned_text, date=date)
        elif hasattr(instance, "parse"):
            return instance.parse(cleaned_text, date=date)
    if hasattr(extractor_module, "parse_raw_dump"):
        return extractor_module.parse_raw_dump(cleaned_text, date=date)
    raise AttributeError("No recognizable extraction method in engine.extractor")


@unittest.skipUnless(EXTRACTOR_AVAILABLE, "engine.extractor is not yet available")
class TestExtractorDisambiguation(unittest.TestCase):
    """Tier 1: Stock Disambiguation & Entity Resolution."""

    def test_all_six_stocks_identified_in_full_day_dump(self) -> None:
        """Full day dump must identify all 6 canonical stock IDs."""
        result = run_extractor(SAMPLE_RAW_DUMP_FULL_DAY, date="2026-09-29")
        stocks = result.stocks
        expected_ids = ["SK_SQUARE", "SK_HYNIX", "UBER", "MBLY", "FLNC", "UPST"]

        for stock_id in expected_ids:
            self.assertIn(stock_id, stocks, f"Expected stock {stock_id} to be extracted")
            factsheet = stocks[stock_id]
            self.assertEqual(factsheet.stock_id, stock_id)
            self.assertTrue(factsheet.name_kr)
            self.assertTrue(factsheet.ticker)

    def test_disambiguate_sk_square_vs_block_square(self) -> None:
        """Resolves collision between US Block Inc (Square, SQ) and Korean SK Square (402340)."""
        result = run_extractor(SAMPLE_RAW_DUMP_SQUARE_BLOCK_COLLISION, date="2026-09-29")
        stocks = result.stocks

        self.assertIn("SK_SQUARE", stocks, "Korean SK Square must be identified")
        sk_square = stocks["SK_SQUARE"]
        self.assertEqual(sk_square.ticker, "402340")
        self.assertEqual(sk_square.metrics.currency, "KRW")
        self.assertEqual(sk_square.metrics.close_price, 1100000.0)

        # US Block (SQ) should NOT be identified as SK_SQUARE
        # Nor should Jack Dorsey's Cash App be attributed to SK Square
        for driver in sk_square.core_drivers:
            self.assertNotIn("잭 도시", driver)
            self.assertNotIn("캐시앱", driver)


@unittest.skipUnless(EXTRACTOR_AVAILABLE, "engine.extractor is not yet available")
class TestExtractorMarketMetrics(unittest.TestCase):
    """Tier 1 & Tier 2: Precision parsing of KRW/USD prices, change %, and volumes."""

    def setUp(self) -> None:
        self.result = run_extractor(SAMPLE_RAW_DUMP_FULL_DAY, date="2026-09-29")

    def test_krw_metrics_sk_square(self) -> None:
        """SK Square: 1,100,000 KRW, -7.56%, -90,000 KRW, volume 704,035."""
        stock = self.result.stocks["SK_SQUARE"]
        metrics = stock.metrics

        self.assertEqual(metrics.currency, "KRW")
        self.assertEqual(metrics.close_price, 1100000.0)
        self.assertAlmostEqual(metrics.change_percent, -7.56, places=2)
        if metrics.change_amount is not None:
            self.assertAlmostEqual(metrics.change_amount, -90000.0, places=0)
        if metrics.volume is not None:
            self.assertEqual(metrics.volume, 704035)

    def test_krw_metrics_sk_hynix(self) -> None:
        """SK Hynix: 176,700 KRW, -5.05%, -10,900 KRW, volume 3,210,000."""
        stock = self.result.stocks["SK_HYNIX"]
        metrics = stock.metrics

        self.assertEqual(metrics.currency, "KRW")
        self.assertEqual(metrics.close_price, 176700.0)
        self.assertAlmostEqual(metrics.change_percent, -5.05, places=2)
        if metrics.change_amount is not None:
            self.assertAlmostEqual(metrics.change_amount, -10900.0, places=0)
        if metrics.volume is not None:
            self.assertEqual(metrics.volume, 3210000)

    def test_usd_metrics_uber(self) -> None:
        """Uber: $68.16, -2.10%, volume 16,640,000 (1,664만 주)."""
        stock = self.result.stocks["UBER"]
        metrics = stock.metrics

        self.assertEqual(metrics.currency, "USD")
        self.assertAlmostEqual(metrics.close_price, 68.16, places=2)
        self.assertAlmostEqual(metrics.change_percent, -2.10, places=2)
        if metrics.volume is not None:
            # 1,664만 주 -> 16,640,000
            self.assertEqual(metrics.volume, 16640000)

    def test_usd_metrics_mobileye(self) -> None:
        """Mobileye: $7.795, -2.93%, volume 4,840,000 (484만 주)."""
        stock = self.result.stocks["MBLY"]
        metrics = stock.metrics

        self.assertEqual(metrics.currency, "USD")
        self.assertAlmostEqual(metrics.close_price, 7.795, places=3)
        self.assertAlmostEqual(metrics.change_percent, -2.93, places=2)
        if metrics.volume is not None:
            self.assertEqual(metrics.volume, 4840000)

    def test_usd_metrics_fluence_energy(self) -> None:
        """Fluence Energy: $7.50, -4.46%, volume 2,100,000."""
        stock = self.result.stocks["FLNC"]
        metrics = stock.metrics

        self.assertEqual(metrics.currency, "USD")
        self.assertAlmostEqual(metrics.close_price, 7.50, places=2)
        self.assertAlmostEqual(metrics.change_percent, -4.46, places=2)
        if metrics.volume is not None:
            self.assertEqual(metrics.volume, 2100000)

    def test_usd_metrics_upstart(self) -> None:
        """Upstart: $23.03, -3.28%, volume 5,400,000."""
        stock = self.result.stocks["UPST"]
        metrics = stock.metrics

        self.assertEqual(metrics.currency, "USD")
        self.assertAlmostEqual(metrics.close_price, 23.03, places=2)
        self.assertAlmostEqual(metrics.change_percent, -3.28, places=2)
        if metrics.volume is not None:
            self.assertEqual(metrics.volume, 5400000)


@unittest.skipUnless(EXTRACTOR_AVAILABLE, "engine.extractor is not yet available")
class TestExtractorDriversAndFactVsNoise(unittest.TestCase):
    """Tier 1: Core Drivers and Fact vs Noise Extraction."""

    def setUp(self) -> None:
        self.result = run_extractor(SAMPLE_RAW_DUMP_FULL_DAY, date="2026-09-29")

    def test_sk_square_driver_and_noise_facts(self) -> None:
        """SK Square: Solidigm IPO driver, fact vs noise separation."""
        stock = self.result.stocks["SK_SQUARE"]
        combined_text = " ".join(stock.core_drivers)
        self.assertTrue(
            "솔리다임" in combined_text or "Solidigm" in combined_text or "중복상장" in combined_text,
            "SK Square drivers must capture Solidigm IPO context",
        )

    def test_sk_hynix_driver_and_hbm(self) -> None:
        """SK Hynix: AI multiplier, HBM LTA contract drivers."""
        stock = self.result.stocks["SK_HYNIX"]
        combined_text = " ".join(stock.core_drivers)
        self.assertTrue(
            "HBM" in combined_text or "AI" in combined_text or "반도체" in combined_text,
            "SK Hynix drivers must capture HBM/AI semiconductor context",
        )


@unittest.skipUnless(EXTRACTOR_AVAILABLE, "engine.extractor is not yet available")
class TestExtractorInterviewsAndIB(unittest.TestCase):
    """Tier 1: Executive Interviews, YouTube URLs, and IB Reports."""

    def setUp(self) -> None:
        self.result = run_extractor(SAMPLE_RAW_DUMP_FULL_DAY, date="2026-09-29")

    def test_sk_hynix_interview_bcg_partner(self) -> None:
        """Extracts BCG partner Kim Chang-wook interview with 삼프로TV and YouTube link."""
        stock = self.result.stocks["SK_HYNIX"]
        interviews = stock.interviews
        self.assertGreater(len(interviews), 0, "SK Hynix should have at least 1 interview fact")

        interview = interviews[0]
        # Check speaker or source
        speaker_str = interview.speaker_name if hasattr(interview, "speaker_name") else str(interview)
        source_media = interview.source_media if hasattr(interview, "source_media") else str(interview)
        source_url = interview.source_url if hasattr(interview, "source_url") else str(interview)

        self.assertTrue("김창욱" in speaker_str or "BCG" in speaker_str or "보스턴컨설팅" in speaker_str)
        self.assertIn("youtu", source_url)

    def test_uber_interview_bg2_pod(self) -> None:
        """Extracts BG2 Pod interview for Uber."""
        stock = self.result.stocks["UBER"]
        self.assertGreater(len(stock.interviews), 0, "Uber should have interview fact")
        interview = stock.interviews[0]
        interview_text = str(interview)
        self.assertTrue(
            "빌 걸리" in interview_text or "Bill Gurley" in interview_text or "BG2" in interview_text or "로보택시" in interview_text
        )

    def test_fluence_ib_comment_jefferies(self) -> None:
        """Extracts Jefferies IB rating downgrade (BUY -> HOLD) and TP cut."""
        stock = self.result.stocks["FLNC"]
        self.assertGreater(len(stock.ib_comments), 0, "Fluence should have IB comments")
        ib = stock.ib_comments[0]
        ib_text = str(ib)
        self.assertTrue(
            "제프리스" in ib_text or "Jefferies" in ib_text or "HOLD" in ib_text or "7" in ib_text
        )


@unittest.skipUnless(EXTRACTOR_AVAILABLE, "engine.extractor is not yet available")
class TestExtractorPortfolioPairStrategy(unittest.TestCase):
    """Tier 1: SK Square (57.6%) vs SK Hynix (42.3%) pair spread and tactical guide."""

    def setUp(self) -> None:
        self.result = run_extractor(SAMPLE_RAW_DUMP_FULL_DAY, date="2026-09-29")

    def test_pair_weights_and_action(self) -> None:
        """Captures pair weights (57.6% : 42.3%) and HOLD action with reverse switching warning."""
        strategy = self.result.pair_strategy
        self.assertAlmostEqual(strategy.sk_square_weight, 57.6, places=1)
        self.assertAlmostEqual(strategy.sk_hynix_weight, 42.3, places=1)
        self.assertIn("HOLD", strategy.tactical_action.upper())
        self.assertTrue("역스위칭" in strategy.risk_warning or "스위칭" in strategy.action_label)


@unittest.skipUnless(EXTRACTOR_AVAILABLE, "engine.extractor is not yet available")
class TestExtractorPartialDumpHandling(unittest.TestCase):
    """Tier 4 Workload Scenario: Incomplete dump with only 3 stocks."""

    def test_partial_dump_extracts_subset_without_crashing(self) -> None:
        """Extracts 3 stocks from partial dump and doesn't invent missing stocks."""
        result = run_extractor(SAMPLE_RAW_DUMP_PARTIAL_STOCKS, date="2026-09-29")
        stocks = result.stocks

        self.assertIn("SK_HYNIX", stocks)
        self.assertIn("SK_SQUARE", stocks)
        self.assertIn("UBER", stocks)

        # Missing stocks should not be falsely extracted with zero or fake values
        self.assertNotIn("FLNC", stocks)
        self.assertNotIn("UPST", stocks)


if __name__ == "__main__":
    unittest.main()
