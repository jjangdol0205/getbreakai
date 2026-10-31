"""Unit and integration tests for Daily Deep Insight Report Generator.

Tests engine.insight_generator.InsightGenerator, DeepInsightReport, and generate_insight:
1. Markdown report structure with 4 required sections:
   - Section 1: 비즈니스 모델 및 유닛 이코노믹스 정밀 분석 (가동률, LTA, SOP, 플랫폼 수수료율)
   - Section 2: 글로벌 피어 그룹 비교 및 상대 밸류에이션 매트릭스
   - Section 3: 손익비 (Risk-Reward) 및 하방 지지력 분석
   - Section 4: 전술적 투자의사결정 매트릭스 (매수/매도/홀딩 밴드)
2. All 8 canonical stocks represented across all 4 sections.
3. File writing to daily_insight/YYYY-MM-DD_insight.md with UTF-8 encoding.
4. DeepInsightReport dataclass serialization (to_dict, to_json).
5. Robustness against empty DailyMarketData and custom dates.
"""

from __future__ import annotations

import json
from pathlib import Path
import tempfile
import unittest

from engine.cleaner import clean_raw_dump
from engine.extractor import extract_facts
from engine.insight_generator import (
    CANONICAL_STOCKS,
    DeepInsightReport,
    InsightGenerator,
    generate_insight,
)
from engine.models import (
    DailyMarketData,
    MarketMetrics,
    StockFactSheet,
    StockSymbol,
)
from tests.fixtures.sample_dumps import SAMPLE_RAW_DUMP_FULL_DAY


class TestInsightGeneratorStructure(unittest.TestCase):
    """Verifies that InsightGenerator builds markdown with all 4 required sections and 8 stocks."""

    @classmethod
    def setUpClass(cls) -> None:
        cleaned_text, meta = clean_raw_dump(SAMPLE_RAW_DUMP_FULL_DAY)
        cls.market_data = extract_facts(cleaned_text, date=meta.get("date_hint") or "2026-09-29")
        cls.generator = InsightGenerator()
        cls.markdown = cls.generator.build_markdown(cls.market_data)

    def test_document_header_and_date(self) -> None:
        """Title contains daily deep insight heading with correct date and key callouts."""
        self.assertIn("# 일간 심층 투자 인사이트 리포트 (2026-09-29)", self.markdown)
        self.assertIn("핵심 전략 테제", self.markdown)
        self.assertIn("포트폴리오 집행 원칙", self.markdown)

    def test_section_1_unit_economics(self) -> None:
        """Section 1 must analyze unit economics: utilization, LTA, SOP, take rates for 8 stocks."""
        self.assertIn("## 1. 비즈니스 모델 및 유닛 이코노믹스 정밀 분석", self.markdown)
        self.assertIn("가동률", self.markdown)
        self.assertIn("LTA", self.markdown)
        self.assertIn("SOP", self.markdown)
        self.assertTrue("수수료율" in self.markdown or "Take Rate" in self.markdown)

        # All 8 stocks present in Section 1
        expected_section1_stocks = [
            "SK하이닉스",
            "SK스퀘어",
            "우버",
            "모빌아이",
            "플루언스에너지",
            "업스타트홀딩스",
            "셀시우스홀딩스",
            "엔페이즈에너지",
        ]
        for stock_name in expected_section1_stocks:
            self.assertIn(stock_name, self.markdown, f"Section 1 must include {stock_name}")

    def test_section_2_peer_group_comparison_matrix(self) -> None:
        """Section 2 must present peer group comparisons and relative valuation table."""
        self.assertIn("## 2. 글로벌 피어 그룹 비교 및 상대 밸류에이션 매트릭스", self.markdown)
        self.assertIn("| 종목명 (티커) | 핵심 피어 그룹 | 주요 비교 지표 |", self.markdown)

        # Verify peer entities and comparison metrics
        self.assertIn("마이크론", self.markdown)
        self.assertIn("소프트뱅크", self.markdown)
        self.assertIn("도어대시", self.markdown)
        self.assertIn("테슬라", self.markdown)
        self.assertIn("소파이", self.markdown)
        self.assertIn("몬스터", self.markdown)
        self.assertIn("솔라엣지", self.markdown)

        # Table rows for all 8 stocks
        for stock_name in ["SK하이닉스", "SK스퀘어", "우버", "모빌아이", "플루언스", "업스타트", "셀시우스", "엔페이즈"]:
            self.assertIn(f"| **{stock_name}**", self.markdown, f"Section 2 table must include row for {stock_name}")

    def test_section_3_risk_reward_analysis(self) -> None:
        """Section 3 must specify downside floor, target upside, and risk-reward ratio."""
        self.assertIn("## 3. 손익비 (Risk-Reward) 및 하방 지지력 분석", self.markdown)
        self.assertIn("하방 지지선 (Downside Floor)", self.markdown)
        self.assertIn("목표 상방 (Target Upside)", self.markdown)
        self.assertIn("손익비 (Risk-Reward)", self.markdown)

        # 8 stocks with explicit risk-reward ratios
        for stock_name in ["SK하이닉스", "SK스퀘어", "우버", "모빌아이", "플루언스", "업스타트", "셀시우스", "엔페이즈"]:
            self.assertIn(f"### 🎯 {stock_name}", self.markdown, f"Section 3 must include {stock_name}")

    def test_section_4_decision_matrix_bands(self) -> None:
        """Section 4 must provide tactical decision matrix with Buy, Hold, Sell bands and Stop-loss."""
        self.assertIn("## 4. 전술적 투자의사결정 매트릭스 (매수/매도/홀딩 밴드)", self.markdown)
        self.assertIn("| 종목명 (티커) | 현재 포지션 | 적극 매수 밴드 (Buy) | 홀딩 / 관망 밴드 (Hold) | 분할 익절 밴드 (Sell) | 리스크 컷 (손절가) |", self.markdown)

        # Table rows for all 8 stocks with tactical guidelines
        for stock_name in ["SK하이닉스", "SK스퀘어", "우버", "모빌아이", "플루언스", "업스타트", "셀시우스", "엔페이즈"]:
            self.assertIn(f"| **{stock_name}**", self.markdown, f"Section 4 table must include row for {stock_name}")

        self.assertIn("역스위칭 절대 금지", self.markdown)


class TestInsightGeneratorFileSystem(unittest.TestCase):
    """Integration tests verifying file generation and output directory management."""

    def test_generate_writes_file_and_returns_payload(self) -> None:
        """generate() creates daily_insight/YYYY-MM-DD_insight.md with full content."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            out_dir = Path(tmp_dir) / "daily_insight"
            generator = InsightGenerator(output_dir=out_dir)

            market_data = DailyMarketData(
                date="2026-09-29",
                stocks={
                    "SK_HYNIX": StockFactSheet(
                        stock_id="SK_HYNIX",
                        stock_name="SK하이닉스",
                        name_kr="SK하이닉스",
                        name_en="SK Hynix Inc.",
                        ticker="000660",
                        market="KRX",
                        category="반도체/AI메모리",
                        badge_color="red",
                        metrics=MarketMetrics(stock_id="SK_HYNIX", close_price=176700.0, close_price_formatted="176,700원"),
                    )
                },
            )

            report = generator.generate(market_data)

            # Check return dataclass
            self.assertIsInstance(report, DeepInsightReport)
            self.assertEqual(report.date, "2026-09-29")
            self.assertEqual(report.title, "일간 심층 투자 인사이트 리포트 (2026-09-29)")
            self.assertIn("## 1. 비즈니스 모델", report.markdown_content)

            # Check file on disk
            expected_file = out_dir / "2026-09-29_insight.md"
            self.assertTrue(expected_file.exists(), f"Insight file must exist at {expected_file}")

            # Verify UTF-8 encoding reading
            content = expected_file.read_text(encoding="utf-8")
            self.assertEqual(content, report.markdown_content)
            self.assertIn("176,700원", content)

    def test_generate_insight_helper_function(self) -> None:
        """Top-level convenience function generate_insight works seamlessly."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            out_dir = Path(tmp_dir) / "daily_insight"
            market_data = DailyMarketData(date="2026-10-05")

            report = generate_insight(market_data, output_dir=out_dir)
            self.assertEqual(report.date, "2026-10-05")

            expected_file = out_dir / "2026-10-05_insight.md"
            self.assertTrue(expected_file.exists())
            self.assertIn("# 일간 심층 투자 인사이트 리포트 (2026-10-05)", report.markdown_content)

    def test_report_serialization_to_dict_and_json(self) -> None:
        """DeepInsightReport serializes to dict and JSON without error."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            generator = InsightGenerator(output_dir=tmp_dir)
            report = generator.generate(DailyMarketData(date="2026-09-29"))

            data_dict = report.to_dict()
            self.assertIsInstance(data_dict, dict)
            self.assertEqual(data_dict["date"], "2026-09-29")
            self.assertIn("unit_economics", data_dict)
            self.assertIn("peer_comparison", data_dict)
            self.assertIn("risk_reward", data_dict)
            self.assertIn("decision_matrix", data_dict)

            # All 8 canonical stocks mapped in structured fields
            self.assertEqual(len(data_dict["unit_economics"]), 8)
            self.assertEqual(len(data_dict["peer_comparison"]), 8)
            self.assertEqual(len(data_dict["risk_reward"]), 8)
            self.assertEqual(len(data_dict["decision_matrix"]), 8)

            # JSON roundtrip
            json_str = report.to_json()
            parsed = json.loads(json_str)
            self.assertEqual(parsed["date"], "2026-09-29")
            self.assertEqual(parsed["title"], "일간 심층 투자 인사이트 리포트 (2026-09-29)")


class TestInsightGeneratorResilience(unittest.TestCase):
    """Edge case and boundary condition tests for InsightGenerator."""

    def test_empty_market_data_resilience(self) -> None:
        """Handles completely empty DailyMarketData without KeyError or crash."""
        empty_data = DailyMarketData()
        generator = InsightGenerator()
        md = generator.build_markdown(empty_data)

        self.assertIsInstance(md, str)
        self.assertIn("일간 심층 투자 인사이트 리포트", md)
        self.assertIn("## 1. 비즈니스 모델 및 유닛 이코노믹스 정밀 분석", md)
        self.assertIn("## 2. 글로벌 피어 그룹 비교 및 상대 밸류에이션 매트릭스", md)
        self.assertIn("## 3. 손익비 (Risk-Reward) 및 하방 지지력 분석", md)
        self.assertIn("## 4. 전술적 투자의사결정 매트릭스 (매수/매도/홀딩 밴드)", md)

    def test_canonical_stocks_coverage(self) -> None:
        """Verifies that CANONICAL_STOCKS contains exactly 8 stocks including CELH and ENPH."""
        self.assertEqual(len(CANONICAL_STOCKS), 8)
        self.assertIn(StockSymbol.CELH, CANONICAL_STOCKS)
        self.assertIn(StockSymbol.ENPH, CANONICAL_STOCKS)

    def test_special_characters_in_raw_text(self) -> None:
        """Handles special characters and unicode in raw_text argument."""
        generator = InsightGenerator()
        market_data = DailyMarketData(date="2026-09-29")
        raw_text = "特殊文字 \u200b\u202e [Test] <div>HTML tag</div> & 'quotes'"
        md = generator.build_markdown(market_data, raw_text=raw_text)
        self.assertIsInstance(md, str)
        self.assertIn("일간 심층 투자 인사이트 리포트", md)


if __name__ == "__main__":
    unittest.main()
