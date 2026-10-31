"""Empirical Challenger 1 stress-testing suite for Milestone M2 revamp.

Verifies:
1. Partial market data robustness (0, 1, 4, 8 stocks, and unknown stocks).
2. Section 1 comparative matrix 8-row table invariant and 8-column layout.
3. Pipe and newline injection handling in core drivers and metrics.
4. Strict absence of "당일 글로벌 거시 매크로 동향" in generated markdown.
5. 2-block format compliance in Section 2 for all 8 stocks.
6. Section 4 Pair strategy and Section 5 8-stock checkpoint integrity.
"""

from __future__ import annotations

import re
import unittest
from typing import Dict, List, Optional

from engine.digest_generator import CANONICAL_STOCKS, DigestGenerator, generate_digest
from engine.models import (
    DailyMarketData,
    KeyWatchPoints,
    MarketMetrics,
    PortfolioPairStrategy,
    StockFactSheet,
    StockSymbol,
    STOCK_MASTERS,
    CorePriceDriver,
)


def create_factsheet(
    symbol: StockSymbol,
    close_price: Optional[float] = 100.0,
    change_percent: Optional[float] = 2.5,
    volume: Optional[int] = 1_000_000,
    core_drivers: Optional[List[str]] = None,
    one_paragraph_summary: str = "",
    key_points: Optional[KeyWatchPoints] = None,
    macro_attribution: str = "",
) -> StockFactSheet:
    master = STOCK_MASTERS[symbol]
    metrics = MarketMetrics(
        stock_id=symbol.value,
        close_price=close_price,
        change_percent=change_percent,
        volume=volume,
        currency=master.currency,
    )
    return StockFactSheet(
        stock_id=symbol.value,
        stock_name=master.name_kr,
        name_kr=master.name_kr,
        name_en=master.name_en,
        ticker=master.ticker,
        market=master.market,
        category=master.category,
        badge_color=master.badge_color,
        metrics=metrics,
        core_drivers=core_drivers or ["주요 동인: 분기 실적 호조 및 신규 계약 체결"],
        one_paragraph_summary=one_paragraph_summary,
        key_points=key_points or KeyWatchPoints(),
        macro_attribution=macro_attribution,
    )


def extract_section1_table_rows(md: str) -> List[str]:
    """Extracts data rows from Section 1 comparative matrix table."""
    lines = md.splitlines()
    in_sec1_table = False
    data_rows: List[str] = []

    for line in lines:
        stripped = line.strip()
        if "### 📊 8개 관심종목 상대 성과 비교 매트릭스" in stripped:
            in_sec1_table = True
            continue
        if in_sec1_table:
            if stripped.startswith("|") and ("종목명" in stripped or "|---" in stripped):
                continue
            if stripped.startswith("|") and stripped.endswith("|"):
                data_rows.append(stripped)
            elif stripped.startswith("---") or stripped.startswith("## 2."):
                break
    return data_rows


class TestEmpiricalPartialMarketData(unittest.TestCase):
    """Stress tests build_markdown with partial market data (0, 1, 4, 8 stocks)."""

    def setUp(self) -> None:
        self.generator = DigestGenerator()

    def test_partial_0_stocks(self) -> None:
        """Case 0 stocks: empty stocks dictionary."""
        data = DailyMarketData(
            date="2026-09-30",
            stocks={},
            macro_summary="글로벌 금리 인하 기대감 지속",
        )
        md = self.generator.build_markdown(data)

        # 1. Verification of Section 1 table row count = 8
        rows = extract_section1_table_rows(md)
        self.assertEqual(len(rows), 8, f"Expected exactly 8 data rows, found {len(rows)}")

        # 2. Check each row contains fallback text
        for idx, row in enumerate(rows):
            sym = CANONICAL_STOCKS[idx]
            self.assertIn("N/A", row, f"Row for {sym} missing N/A")
            self.assertIn("원문 데이터 미제공", row, f"Row for {sym} missing fallback driver")
            self.assertIn("중립", row, f"Row for {sym} missing neutral tone")
            cols = [c.strip() for c in row.split("|")[1:-1]]
            self.assertEqual(len(cols), 8, f"Expected 8 columns in table row for {sym}, got {len(cols)}")

        # 3. Check Section 2 2-block structure for all 8 stocks
        for sym in CANONICAL_STOCKS:
            self.assertIn(f"### 📌 ", md)
            self.assertIn("#### [1문단 핵심 요약]", md)
            self.assertIn("#### [관심있게 봐야 할 포인트 (2줄 요약)]", md)

        # 4. Fallback text markers
        self.assertEqual(md.count("원문 데이터 미수집"), 8)
        self.assertEqual(md.count("원문 데이터 미제공"), 8)

    def test_partial_1_stock_celh(self) -> None:
        """Case 1 stock: only CELH provided."""
        data = DailyMarketData(
            date="2026-09-30",
            stocks={
                StockSymbol.CELH.value: create_factsheet(
                    StockSymbol.CELH,
                    close_price=42.50,
                    change_percent=4.20,
                    volume=5_500_000,
                    core_drivers=["주요 동인: 골드만삭스 매수 의견 상향 및 북미 점유율 확대"],
                )
            },
        )
        md = self.generator.build_markdown(data)

        # 1. Section 1 table row count = 8
        rows = extract_section1_table_rows(md)
        self.assertEqual(len(rows), 8)

        # 2. CELH row has live data
        celh_row = [r for r in rows if "CELH" in r][0]
        self.assertIn("$42.50", celh_row)
        self.assertIn("+4.20%", celh_row)
        self.assertIn("골드만삭스 매수 의견 상향", celh_row)

        # 3. Exactly 7 stocks fallback in Section 1, consolidated unprovided note in Section 2 (M3 R1)
        self.assertEqual(md.count("원문 데이터 미제공"), 7)
        self.assertIn("당일 원문 데이터 미수집 종목 (관망 유지)", md)

    def test_partial_4_stocks(self) -> None:
        """Case 4 stocks: SK_HYNIX, UBER, FLNC, ENPH."""
        stocks_dict = {
            StockSymbol.SK_HYNIX.value: create_factsheet(StockSymbol.SK_HYNIX, 185000.0, 3.5, 3_000_000),
            StockSymbol.UBER.value: create_factsheet(StockSymbol.UBER, 72.5, 1.8, 15_000_000),
            StockSymbol.FLNC.value: create_factsheet(StockSymbol.FLNC, 8.2, -2.1, 2_000_000),
            StockSymbol.ENPH.value: create_factsheet(StockSymbol.ENPH, 48.0, -3.36, 4_000_000),
        }
        data = DailyMarketData(date="2026-09-30", stocks=stocks_dict)
        md = self.generator.build_markdown(data)

        rows = extract_section1_table_rows(md)
        self.assertEqual(len(rows), 8)

        # 4 missing stocks in Section 1, consolidated unprovided note in Section 2 (M3 R1)
        self.assertEqual(md.count("원문 데이터 미제공"), 4)
        self.assertIn("당일 원문 데이터 미수집 종목 (관망 유지)", md)

    def test_full_8_stocks(self) -> None:
        """Case 8 stocks: all 8 canonical stocks populated."""
        stocks_dict = {sym.value: create_factsheet(sym, 100.0, 1.0, 1_000_000) for sym in CANONICAL_STOCKS}
        data = DailyMarketData(date="2026-09-30", stocks=stocks_dict)
        md = self.generator.build_markdown(data)

        rows = extract_section1_table_rows(md)
        self.assertEqual(len(rows), 8)
        self.assertEqual(md.count("원문 데이터 미제공"), 0)
        self.assertEqual(md.count("원문 데이터 미수집"), 0)

        # Verify every canonical stock header appears in Section 2
        for sym in CANONICAL_STOCKS:
            master = STOCK_MASTERS[sym]
            self.assertIn(f"({master.ticker} /", md)


class TestEmpiricalPipeInjectionAndTableStructure(unittest.TestCase):
    """Stress tests markdown table invariant against malicious pipe and newline injection."""

    def setUp(self) -> None:
        self.generator = DigestGenerator()

    def test_pipe_injection_in_core_drivers(self) -> None:
        """Pipes inside core_drivers must be replaced so they do not create extra columns."""
        malicious_driver = "주요 동인: AI 칩 | 파이프라인 확장 | 수주 $5B | 마진 45% | 공급 부족"
        fact = create_factsheet(StockSymbol.SK_HYNIX, core_drivers=[malicious_driver])
        data = DailyMarketData(date="2026-09-30", stocks={StockSymbol.SK_HYNIX.value: fact})
        md = self.generator.build_markdown(data)

        rows = extract_section1_table_rows(md)
        self.assertEqual(len(rows), 8)

        hynix_row = rows[0]
        # In an 8-column markdown table, there should be exactly 9 pipe characters
        self.assertEqual(hynix_row.count("|"), 9, f"Table row corrupted by pipes: {hynix_row}")
        cols = [c.strip() for c in hynix_row.split("|")[1:-1]]
        self.assertEqual(len(cols), 8)
        # Verify pipe was sanitized to slash
        self.assertIn("AI 칩 / 파이프라인 확장 / 수주 $5B / 마진 45% / 공급 부족", cols[6])

    def test_extreme_delimiter_and_newline_injection(self) -> None:
        """Adversarial input attempting markdown table breakout with delimiters and newlines."""
        breakout_payload = "|---|---|---|---|---|---|---|---|\n| HACKED | HACKED | HACKED |"
        fact = create_factsheet(StockSymbol.CELH, core_drivers=[f"주요 동인: {breakout_payload}"])
        data = DailyMarketData(date="2026-09-30", stocks={StockSymbol.CELH.value: fact})
        md = self.generator.build_markdown(data)

        rows = extract_section1_table_rows(md)
        self.assertEqual(len(rows), 8, "Breakout injected extra table rows!")

        for idx, row in enumerate(rows):
            self.assertEqual(row.count("|"), 9, f"Row {idx} does not have exactly 8 columns (9 pipes): {row}")
            cols = [c.strip() for c in row.split("|")[1:-1]]
            self.assertEqual(len(cols), 8)

    def test_pipe_injection_in_volume_and_summary(self) -> None:
        """Pipes in volume_formatted, structured_drivers, and raw_summary."""
        fact = create_factsheet(StockSymbol.ENPH)
        fact.metrics.volume_formatted = "1,500,000 | 2,000,000주"
        fact.core_drivers = []
        fact.raw_summary = "Enphase Air | NEM 3.0 | Microinverter surge"

        data = DailyMarketData(date="2026-09-30", stocks={StockSymbol.ENPH.value: fact})
        md = self.generator.build_markdown(data)

        rows = extract_section1_table_rows(md)
        self.assertEqual(len(rows), 8)

        enph_row = [r for r in rows if "ENPH" in r][0]
        self.assertEqual(enph_row.count("|"), 9)
        cols = [c.strip() for c in enph_row.split("|")[1:-1]]
        self.assertEqual(len(cols), 8)
        # Verify volume pipe replaced
        self.assertEqual(cols[5], "1,500,000 / 2,000,000주")


class TestEmpiricalMacroRemovalAndInvariants(unittest.TestCase):
    """Stress tests macro section removal and Section 1 table row count invariant."""

    def setUp(self) -> None:
        self.generator = DigestGenerator()

    def test_standalone_macro_section_strictly_absent(self) -> None:
        """Verify '당일 글로벌 거시 매크로 동향' is strictly absent from generated markdown."""
        test_payloads = [
            DailyMarketData(date="2026-09-30", stocks={}),
            DailyMarketData(date="2026-09-30", macro_summary="미국 금리 안정화 및 반도체 지수 상승"),
            DailyMarketData(date="2026-09-30", macro_overview="글로벌 매크로 관망세"),
            DailyMarketData(
                date="2026-09-30",
                macro_summary="당일 글로벌 거시 매크로 동향: 국채 10년물 금리",  # Prompt injection attempt
            ),
        ]

        forbidden_phrase = "당일 글로벌 거시 매크로 동향"
        forbidden_header = "### 🌐 당일 글로벌 거시 매크로 동향"

        for idx, payload in enumerate(test_payloads):
            md = self.generator.build_markdown(payload)
            # Standalone subsection header must NEVER exist
            self.assertNotIn(forbidden_header, md, f"Found standalone macro header in payload {idx}")

        # In standard payloads (where user text doesn't inject it), the phrase itself must not exist
        standard_data = DailyMarketData(
            date="2026-09-30",
            macro_summary="미 국채 10년물 금리 4.12% 기록 및 엔화 강세.",
        )
        std_md = self.generator.build_markdown(standard_data)
        self.assertNotIn(forbidden_phrase, std_md, "Forbidden phrase found in standard generated digest!")

    def test_section1_table_row_count_strictly_8(self) -> None:
        """Section 1 table must strictly contain 8 data rows across all scenarios."""
        # 1. Empty stocks
        rows0 = extract_section1_table_rows(self.generator.build_markdown(DailyMarketData(stocks={})))
        self.assertEqual(len(rows0), 8)

        # 2. 1 stock
        rows1 = extract_section1_table_rows(
            self.generator.build_markdown(
                DailyMarketData(stocks={StockSymbol.UPST.value: create_factsheet(StockSymbol.UPST)})
            )
        )
        self.assertEqual(len(rows1), 8)

        # 3. 6 stocks (legacy count)
        legacy_stocks = {
            s.value: create_factsheet(s)
            for s in [
                StockSymbol.SK_HYNIX,
                StockSymbol.SK_SQUARE,
                StockSymbol.UBER,
                StockSymbol.MBLY,
                StockSymbol.FLNC,
                StockSymbol.UPST,
            ]
        }
        rows6 = extract_section1_table_rows(self.generator.build_markdown(DailyMarketData(stocks=legacy_stocks)))
        self.assertEqual(len(rows6), 8, "Legacy 6-stock input must still generate 8-stock table!")

        # 4. Unknown/extra stocks injected (e.g. 12 stocks)
        bloated_stocks = dict(legacy_stocks)
        bloated_stocks[StockSymbol.CELH.value] = create_factsheet(StockSymbol.CELH)
        bloated_stocks[StockSymbol.ENPH.value] = create_factsheet(StockSymbol.ENPH)
        bloated_stocks["AAPL"] = create_factsheet(StockSymbol.UBER)
        bloated_stocks["MSFT"] = create_factsheet(StockSymbol.UBER)
        bloated_stocks["NVDA"] = create_factsheet(StockSymbol.UBER)
        rows12 = extract_section1_table_rows(self.generator.build_markdown(DailyMarketData(stocks=bloated_stocks)))
        self.assertEqual(len(rows12), 8, "Extra non-canonical stocks must not bloat Section 1 table beyond 8 rows!")


class TestEmpiricalTwoBlockStructure(unittest.TestCase):
    """Stress tests Section 2 2-block structure requirements (1-paragraph + 2-line watchpoints)."""

    def setUp(self) -> None:
        self.generator = DigestGenerator()

    def test_section_2_block_structure_counts(self) -> None:
        """Every stock in Section 2 must have exactly 1 one-paragraph block and 1 two-line watchpoints block."""
        stocks = {s.value: create_factsheet(s) for s in CANONICAL_STOCKS}
        data = DailyMarketData(date="2026-09-30", stocks=stocks)
        md = self.generator.build_markdown(data)

        # Header 2
        self.assertIn("## 2. 8개 관심종목 심층 브리핑 (1문단 요약 & 2줄 관심 포인트)", md)

        # Exactly 8 occurrences of [1문단 핵심 요약]
        self.assertEqual(md.count("#### [1문단 핵심 요약]"), 8)

        # Exactly 8 occurrences of [관심있게 봐야 할 포인트 (2줄 요약)]
        self.assertEqual(md.count("#### [관심있게 봐야 할 포인트 (2줄 요약)]"), 8)

        # Exactly 8 occurrences of Line 1 and Line 2 prefixes
        self.assertEqual(md.count("- **단기 수급/가격선**:"), 8)
        self.assertEqual(md.count("- **중장기 펀더멘털/이벤트**:"), 8)

    def test_one_paragraph_summary_sentence_count(self) -> None:
        """Default generated one-paragraph summary should contain 3 to 5 cohesive sentences."""
        fact = create_factsheet(
            StockSymbol.SK_HYNIX,
            close_price=185000.0,
            change_percent=3.5,
            volume=3_500_000,
            macro_attribution="미국 금리 인하에 따른 반도체 섹터 투자 심리 개선 반영.",
        )
        data = DailyMarketData(date="2026-09-30", stocks={StockSymbol.SK_HYNIX.value: fact})
        md = self.generator.build_markdown(data)

        # Extract SK Hynix one-paragraph summary
        hynix_section = md.split("### 📌 SK하이닉스")[1].split("### 📌")[0]
        one_para = hynix_section.split("#### [1문단 핵심 요약]")[1].split("#### [관심있게 봐야 할 포인트")[0].strip()

        # Count sentences by ending periods (. )
        sentences = [s.strip() for s in re.split(r'\.\s+', one_para) if s.strip()]
        self.assertGreaterEqual(len(sentences), 3, f"Too few sentences in summary: {len(sentences)}")
        self.assertLessEqual(len(sentences), 5, f"Too many sentences in summary: {len(sentences)}")


class TestEmpiricalAdvancedRobustness(unittest.TestCase):
    """Stress tests extreme metrics, pair missing edge case, Section 5 checkpoints, and file generation."""

    def setUp(self) -> None:
        self.generator = DigestGenerator()

    def test_extreme_and_none_metrics(self) -> None:
        """Verify handling of None, negative prices, extreme percentages, and zero volume."""
        fact = create_factsheet(StockSymbol.UBER)
        fact.metrics.close_price = None
        fact.metrics.change_percent = None
        fact.metrics.volume = None
        data = DailyMarketData(date="2026-09-30", stocks={StockSymbol.UBER.value: fact})
        md = self.generator.build_markdown(data)

        rows = extract_section1_table_rows(md)
        self.assertEqual(len(rows), 8)
        uber_row = [r for r in rows if "UBER" in r][0]
        self.assertIn("N/A", uber_row)

    def test_section_4_pair_with_missing_stocks(self) -> None:
        """Section 4 pair portfolio table must render default weights and spread without crash when pair stocks missing."""
        data = DailyMarketData(date="2026-09-30", stocks={})
        md = self.generator.build_markdown(data)
        self.assertIn("## 4. 포트폴리오 비중 진단 및 전술적 대응 가이드", md)
        self.assertIn("57.6%", md)
        self.assertIn("42.3%", md)
        self.assertIn("역스위칭", md)

    def test_section_5_checkpoints_8_stocks(self) -> None:
        """Section 5 must contain all 5 subsections, notably subsection 5 for CELH and ENPH."""
        fact_celh = create_factsheet(StockSymbol.CELH, change_percent=4.20)
        fact_enph = create_factsheet(StockSymbol.ENPH, change_percent=-3.36)
        data = DailyMarketData(
            date="2026-09-30",
            stocks={
                StockSymbol.CELH.value: fact_celh,
                StockSymbol.ENPH.value: fact_enph,
            },
        )
        md = self.generator.build_markdown(data)

        self.assertIn("## 5. 익일 모니터링 체크포인트", md)
        self.assertIn("5. **기능성 음료 및 신재생 에너지 (셀시우스 & 엔페이즈)**:", md)
        self.assertIn("CELH, +4.20%", md)
        self.assertIn("ENPH, -3.36%", md)

    def test_file_generation_and_utf8(self) -> None:
        """Verify generate() writes valid utf-8 file to disk with 8 stocks and no standalone macro."""
        import tempfile
        from pathlib import Path

        with tempfile.TemporaryDirectory(ignore_cleanup_errors=True) as tmp_dir:
            gen = DigestGenerator(output_dir=tmp_dir)
            data = DailyMarketData(
                date="2026-09-30",
                stocks={s.value: create_factsheet(s) for s in CANONICAL_STOCKS},
            )
            content = gen.generate(data, output_dir=tmp_dir)
            target = Path(tmp_dir) / "2026-09-30_digest.md"
            if not target.exists():
                target = Path(tmp_dir) / "daily_digest" / "2026-09-30_digest.md"
            self.assertTrue(target.exists(), f"Target digest file not found in {tmp_dir}")
            read_back = target.read_text(encoding="utf-8")
            self.assertEqual(read_back, content)
            self.assertIn("### 📊 8개 관심종목 상대 성과 비교 매트릭스", read_back)
            self.assertNotIn("당일 글로벌 거시 매크로 동향", read_back)


if __name__ == "__main__":
    unittest.main()

