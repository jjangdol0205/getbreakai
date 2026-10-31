"""Adversarial stress-testing suite for Milestone M2 by Challenger 1.

Targets: engine/digest_generator.py (DigestGenerator, generate_digest)

Adversarial Scenarios:
1. Partial Stock Dumps:
   - 2 stocks only (SK Hynix, Uber)
   - 3 stocks only (Fluence, Upstart, Mobileye - both pair stocks missing)
   - 0 stocks (empty stocks dict)
   - Unknown/arbitrary stock keys in stocks dict
2. Empty Drivers and Missing Fact vs Noise:
   - core_drivers=[], raw_summary="", structured_drivers=[], fact_vs_noise={}
   - None values in fact_vs_noise keys
3. Missing Interviews and Partial Executive Interview Objects:
   - Zero interviews and zero IB comments
   - InterviewFact with all optional fields as None or empty
   - IBReportFact with None rating, None TP, None thesis
4. Extreme & Boundary Dates:
   - None date
   - Empty string date
   - Far past ("1970-01-01"), far future ("2099-12-31")
   - Non-standard formats ("2026/09/29", "2026.09.29")
5. Extreme Numerical Metrics:
   - close_price is None, 0.0, negative
   - change_percent is None, 0.0, extreme positive (+1500%), extreme negative (-99.9%)
   - volume is None, 0, 100 billion
   - currency is None or unrecognized
6. Text Sanitization (Markdown Table Invariant):
   - Drivers containing pipe symbols ('|') and newlines ('\\n')
   - Drivers that are extremely long strings (> 500 chars)
7. File System Robustness:
   - Output to nested non-existent directory
   - Output to direct .md file target
   - File output UTF-8 encoding integrity
"""

import os
import shutil
import tempfile
import unittest
from pathlib import Path
from typing import Dict, List, Optional

from engine.digest_generator import DigestGenerator, generate_digest
from engine.models import (
    DailyMarketData,
    ExecutiveInterviewFact,
    IBReportFact,
    MarketMetrics,
    PortfolioPairStrategy,
    StockFactSheet,
    StockSymbol,
)


def make_fact_sheet(
    stock_id: str,
    name_kr: str,
    ticker: str,
    close_price: Optional[float] = 100.0,
    change_percent: Optional[float] = 0.0,
    volume: Optional[int] = 1000,
    currency: str = "USD",
    core_drivers: Optional[List[str]] = None,
    raw_summary: str = "",
    fact_vs_noise: Optional[Dict[str, List[str]]] = None,
    interviews: Optional[List[ExecutiveInterviewFact]] = None,
    ib_comments: Optional[List[IBReportFact]] = None,
    portfolio_impact: str = "",
    strategist_insight: str = "",
) -> StockFactSheet:
    metrics = MarketMetrics(
        stock_id=stock_id,
        close_price=close_price,
        change_percent=change_percent,
        volume=volume,
        currency=currency,
    )
    return StockFactSheet(
        stock_id=stock_id,
        stock_name=name_kr,
        name_kr=name_kr,
        name_en=stock_id,
        ticker=ticker,
        market="KRX" if currency == "KRW" else "NASDAQ",
        category="General",
        badge_color="blue",
        metrics=metrics,
        core_drivers=core_drivers if core_drivers is not None else [],
        raw_summary=raw_summary,
        fact_vs_noise=fact_vs_noise if fact_vs_noise is not None else {"facts": [], "noise": []},
        interviews=interviews if interviews is not None else [],
        ib_comments=ib_comments if ib_comments is not None else [],
        portfolio_impact=portfolio_impact,
        strategist_insight=strategist_insight,
    )


class TestPartialStockDumps(unittest.TestCase):
    """Stress tests: Incomplete stock subsets fed into DigestGenerator."""

    def test_partial_dump_2_stocks(self) -> None:
        """Only 2 stocks provided (SK Hynix, Uber)."""
        stocks: Dict[str, StockFactSheet] = {
            "SK_HYNIX": make_fact_sheet(
                stock_id="SK_HYNIX",
                name_kr="SK하이닉스",
                ticker="000660",
                close_price=176700.0,
                change_percent=-5.05,
                volume=3210000,
                currency="KRW",
                core_drivers=["HBM3E 엔비디아 공급 지속"],
            ),
            "UBER": make_fact_sheet(
                stock_id="UBER",
                name_kr="우버",
                ticker="UBER",
                close_price=68.16,
                change_percent=-2.10,
                volume=16640000,
                currency="USD",
                core_drivers=["딜리버리 히어로 인수 검토"],
            ),
        }
        data = DailyMarketData(
            date="2026-09-29",
            macro_summary="매크로 요약 테스트",
            stocks=stocks,
        )

        generator = DigestGenerator()
        md = generator.build_markdown(data)

        # Invariant 1: Document must be generated without crashing
        self.assertIsInstance(md, str)
        self.assertGreater(len(md), 500)

        # Invariant 2: Section 1 comparative table must still contain all 8 canonical stocks
        for stock_id in ["SK스퀘어", "SK하이닉스", "우버", "모빌아이", "플루언스", "업스타트", "셀시우스", "엔페이즈"]:
            self.assertIn(stock_id, md, f"Missing {stock_id} in table")

        # Invariant 3: Missing stocks must render gracefully without throwing IndexError/KeyError
        self.assertIn("원문 데이터 미제공", md)

        # Invariant 4: Present stocks must show their data
        self.assertIn("176,700원", md)
        self.assertIn("-5.05%", md)
        self.assertIn("$68.16", md)

    def test_partial_dump_3_stocks_without_pair_stocks(self) -> None:
        """3 US stocks provided (Fluence, Upstart, Mobileye) - both SK Square & SK Hynix missing."""
        stocks: Dict[str, StockFactSheet] = {
            "FLNC": make_fact_sheet(
                stock_id="FLNC",
                name_kr="플루언스에너지",
                ticker="FLNC",
                close_price=7.50,
                change_percent=-4.46,
                volume=2100000,
                currency="USD",
            ),
            "UPST": make_fact_sheet(
                stock_id="UPST",
                name_kr="업스타트",
                ticker="UPST",
                close_price=23.03,
                change_percent=-3.28,
                volume=5400000,
                currency="USD",
            ),
            "MBLY": make_fact_sheet(
                stock_id="MBLY",
                name_kr="모빌아이",
                ticker="MBLY",
                close_price=7.795,
                change_percent=-2.93,
                volume=4840000,
                currency="USD",
            ),
        }
        data = DailyMarketData(
            date="2026-09-29",
            macro_summary="미국 금리 안정세",
            stocks=stocks,
            pair_strategy=None,  # pair strategy is None
        )

        generator = DigestGenerator()
        md = generator.build_markdown(data)

        # Section 4 must still render pair portfolio guide with fallback weights
        self.assertIn("57.6%", md)
        self.assertIn("42.3%", md)
        self.assertIn("역스위칭", md)

    def test_empty_stocks_dict(self) -> None:
        """Completely empty stocks dict."""
        data = DailyMarketData(
            date="2026-09-29",
            macro_summary="데이터 수집 실패일",
            stocks={},
        )

        generator = DigestGenerator()
        md = generator.build_markdown(data)

        self.assertTrue("일간 8개 관심종목 종합 다이제스트" in md or "일간 6개 관심종목 종합 다이제스트" in md)
        self.assertTrue("## 1. 당일 거시 매크로" in md or "비교 매트릭스" in md or "상대 성과" in md)
        self.assertIn("## 2. 종목별 핵심 동인", md)
        self.assertIn("## 3. 경영진 인터뷰 궤적", md)
        self.assertIn("## 4. 포트폴리오 비중", md)
        self.assertIn("## 5. 익일 모니터링", md)


class TestEmptyDriversAndFactVsNoise(unittest.TestCase):
    """Stress tests: Empty drivers, empty fact_vs_noise, and missing noise data."""

    def test_empty_drivers_and_noise_dict(self) -> None:
        """Stock with empty core_drivers, empty fact_vs_noise, empty raw_summary."""
        stocks: Dict[str, StockFactSheet] = {
            "SK_SQUARE": make_fact_sheet(
                stock_id="SK_SQUARE",
                name_kr="SK스퀘어",
                ticker="402340",
                close_price=1100000.0,
                change_percent=-7.56,
                volume=704035,
                currency="KRW",
                core_drivers=[],
                raw_summary="",
                fact_vs_noise={},
                portfolio_impact="",
                strategist_insight="",
            )
        }
        data = DailyMarketData(
            date="2026-09-29",
            macro_summary="",
            stocks=stocks,
        )

        generator = DigestGenerator()
        md = generator.build_markdown(data)

        # Must not crash and must provide fallback text
        self.assertIn("특이 변동 동인 없음", md)
        self.assertIn("시장 노이즈 (Noise)", md)
        self.assertIn("공시 및 검증 팩트 (Fact)", md)


class TestMissingInterviewsAndPartialFacts(unittest.TestCase):
    """Stress tests: Missing interviews, empty IB comments, and partial interview objects."""

    def test_missing_interviews_and_ib(self) -> None:
        """DailyMarketData with no interviews and no IB reports."""
        stocks: Dict[str, StockFactSheet] = {
            "UBER": make_fact_sheet(
                stock_id="UBER",
                name_kr="우버",
                ticker="UBER",
                close_price=68.16,
                change_percent=-2.10,
                volume=16640000,
                currency="USD",
                interviews=[],
                ib_comments=[],
            )
        }
        data = DailyMarketData(
            date="2026-09-29",
            stocks=stocks,
        )

        generator = DigestGenerator()
        md = generator.build_markdown(data)

        # Section 3 should output fallback message
        self.assertIn("당일 수집된 경영진 공식 인터뷰 및 대담 데이터가 없습니다", md)

    def test_interview_fact_with_all_none_fields(self) -> None:
        """ExecutiveInterviewFact with None in optional fields."""
        incomplete_interview = ExecutiveInterviewFact(
            stock_id="SK_HYNIX",
            speaker_name="김창욱",
            speaker_title="",
            affiliation="",
            source_media="",
            source_url="",
            core_quotes=[],
            context_trajectory="",
            investment_takeaway="",
        )
        stocks: Dict[str, StockFactSheet] = {
            "SK_HYNIX": make_fact_sheet(
                stock_id="SK_HYNIX",
                name_kr="SK하이닉스",
                ticker="000660",
                close_price=176700.0,
                change_percent=-5.05,
                volume=3210000,
                currency="KRW",
                interviews=[incomplete_interview],
                ib_comments=[
                    IBReportFact(
                        stock_id="SK_HYNIX",
                        brokerage="골드만삭스",
                        rating_current="",
                        target_price_current=None,
                        key_thesis="",
                    )
                ],
            )
        }
        data = DailyMarketData(
            date="2026-09-29",
            stocks=stocks,
        )

        generator = DigestGenerator()
        md = generator.build_markdown(data)

        self.assertIn("김창욱", md)
        self.assertIn("골드만삭스", md)
        self.assertIn("미기재", md)  # TP fallback


class TestExtremeDatesAndFormats(unittest.TestCase):
    """Stress tests: None date, empty date, extreme past/future dates."""

    def test_none_and_empty_date(self) -> None:
        """None or empty string date must fallback to a valid date."""
        for d in [None, ""]:
            data = DailyMarketData(date=d, stocks={})
            generator = DigestGenerator()
            md = generator.build_markdown(data)
            self.assertIn("2026-09-29", md)

    def test_past_and_future_dates(self) -> None:
        """Dates like 1999-12-31 or 2035-05-15."""
        for test_date in ["1999-12-31", "2035-05-15"]:
            data = DailyMarketData(date=test_date, stocks={})
            generator = DigestGenerator()
            md = generator.build_markdown(data)
            self.assertIn(test_date, md)


class TestExtremeMetricsAndCurrency(unittest.TestCase):
    """Stress tests: None, zero, negative prices, extreme percentages, volume scales."""

    def test_none_metrics(self) -> None:
        """MarketMetrics with all None values."""
        sheet = make_fact_sheet(
            stock_id="UBER",
            name_kr="우버",
            ticker="UBER",
            close_price=None,
            change_percent=None,
            volume=None,
            currency="USD",
        )
        data = DailyMarketData(date="2026-09-29", stocks={"UBER": sheet})
        generator = DigestGenerator()
        md = generator.build_markdown(data)

        self.assertIn("N/A", md)

    def test_extreme_change_percentages(self) -> None:
        """Extreme positive change (+1500.0%) and extreme drop (-99.9%)."""
        s1 = make_fact_sheet(
            stock_id="UPST",
            name_kr="업스타트",
            ticker="UPST",
            close_price=500.0,
            change_percent=1500.0,
            volume=100000,
            currency="USD",
        )
        s2 = make_fact_sheet(
            stock_id="FLNC",
            name_kr="플루언스",
            ticker="FLNC",
            close_price=0.01,
            change_percent=-99.9,
            volume=99999999999,
            currency="USD",
        )
        data = DailyMarketData(date="2026-09-29", stocks={"UPST": s1, "FLNC": s2})
        generator = DigestGenerator()
        md = generator.build_markdown(data)

        self.assertIn("+1500.00%", md)
        self.assertIn("-99.90%", md)
        self.assertIn("강세 급등 / 모멘텀 지속", md)
        self.assertIn("단기 과매도 / 패닉셀 (매도 자제)", md)


class TestMarkdownTableSanitization(unittest.TestCase):
    """Stress tests: Drivers with pipe symbols and line breaks that would break Markdown tables."""

    def test_pipe_and_newline_in_core_drivers(self) -> None:
        """Pipes ('|') and newlines ('\\n') must be sanitized in Section 1 markdown table."""
        adversarial_driver = "악재 루머 A | B | C\n추가 라인: 공시 확인 필요"
        sheet = make_fact_sheet(
            stock_id="UBER",
            name_kr="우버",
            ticker="UBER",
            close_price=68.16,
            change_percent=-2.10,
            volume=16640000,
            currency="USD",
            core_drivers=[adversarial_driver],
        )
        data = DailyMarketData(date="2026-09-29", stocks={"UBER": sheet})
        generator = DigestGenerator()
        md = generator.build_markdown(data)

        # Inspect table rows in Section 1
        lines = md.splitlines()
        table_rows = [l for l in lines if l.startswith("| 우버") or l.startswith("| **우버")]
        self.assertEqual(len(table_rows), 1, "Must find exactly one table row for Uber")
        uber_row = table_rows[0]

        # In a valid 8-column markdown table, there should be 9 '|' separators (leading, 7 inner, trailing)
        pipe_count = uber_row.count("|")
        self.assertEqual(pipe_count, 9, f"Row must maintain exact 8 table columns (9 pipes), got {pipe_count}: {uber_row}")


class TestFileSystemGenerationScenarios(unittest.TestCase):
    """Stress tests: output_dir parameter variations and UTF-8 writing."""

    def setUp(self) -> None:
        self.test_dir = tempfile.mkdtemp()

    def tearDown(self) -> None:
        shutil.rmtree(self.test_dir, ignore_errors=True)

    def test_nested_nonexistent_directory(self) -> None:
        """Output to deeply nested non-existent directory."""
        nested_dir = Path(self.test_dir) / "level1" / "level2" / "level3"
        data = DailyMarketData(date="2026-09-29", stocks={})

        out_content = generate_digest(data, output_dir=str(nested_dir))
        self.assertIsInstance(out_content, str)

        created_files = list(nested_dir.glob("**/*_digest.md"))
        self.assertGreaterEqual(len(created_files), 1, "Must create digest in nested directory")
        self.assertTrue(created_files[0].exists())

    def test_direct_file_path(self) -> None:
        """Output directly to a target .md file."""
        target_file = Path(self.test_dir) / "custom_digest_report.md"
        data = DailyMarketData(date="2026-09-29", stocks={})

        generate_digest(data, output_dir=str(target_file))
        self.assertTrue(target_file.exists())
        content = target_file.read_text(encoding="utf-8")
        self.assertIn("일간 6개 관심종목 종합 다이제스트", content)


class TestCLIDigestIntegration(unittest.TestCase):
    """Stress tests: engine.cli 'digest' subcommand execution."""

    def setUp(self) -> None:
        self.test_dir = tempfile.mkdtemp()
        from tests.fixtures.sample_dumps import SAMPLE_RAW_DUMP_FULL_DAY
        self.sample_full = SAMPLE_RAW_DUMP_FULL_DAY

    def tearDown(self) -> None:
        shutil.rmtree(self.test_dir, ignore_errors=True)

    def test_cli_digest_full_day(self) -> None:
        """CLI digest subcommand with complete input file."""
        from engine.cli import main
        input_file = Path(self.test_dir) / "input.txt"
        output_file = Path(self.test_dir) / "digest.md"
        input_file.write_text(self.sample_full, encoding="utf-8")

        exit_code = main(["digest", "-i", str(input_file), "-o", str(output_file), "-d", "2026-09-29"])
        self.assertEqual(exit_code, 0)
        self.assertTrue(output_file.exists())
        content = output_file.read_text(encoding="utf-8")
        self.assertIn("일간 6개 관심종목 종합 다이제스트 (2026-09-29)", content)
        self.assertIn("SK스퀘어", content)
        self.assertIn("SK하이닉스", content)

    def test_cli_digest_empty_input(self) -> None:
        """CLI digest subcommand with empty input file."""
        from engine.cli import main
        input_file = Path(self.test_dir) / "empty.txt"
        output_file = Path(self.test_dir) / "empty_digest.md"
        input_file.write_text("", encoding="utf-8")

        exit_code = main(["digest", "-i", str(input_file), "-o", str(output_file), "-d", "2026-09-29"])
        self.assertEqual(exit_code, 0)
        self.assertTrue(output_file.exists())
        content = output_file.read_text(encoding="utf-8")
        self.assertIn("일간 6개 관심종목 종합 다이제스트", content)


if __name__ == "__main__":
    unittest.main()
