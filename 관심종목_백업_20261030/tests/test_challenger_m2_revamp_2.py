"""Milestone M2 Iteration 2 Challenger 2 Empirical Stress Test Suite.

Authored by: Challenger 2 (EMPIRICAL CHALLENGER)
Target: engine/digest_generator.py (DigestGenerator, generate_digest)

Mission & Acceptance Criteria:
1. End-to-end extraction and digest generation on raw_input_20260930.txt.
2. Format validation of each stock section (8 canonical stocks):
   - Header: '#### [1문단 핵심 요약]' followed by single paragraph.
     * No sub-bullets ('-', '*', '•').
     * No blank lines separating sentences.
     * Sentence count between 3 and 6.
   - Header: '#### [관심있게 봐야 할 포인트 (2줄 요약)]' followed by exactly:
     * '- **단기 수급/가격선**:'
     * '- **중장기 펀더멘털/이벤트**:'
3. Verification that SK Square vs SK Hynix pair ratio (57.6% : 42.3%) and tactical instructions are intact.
4. Verification that standalone macro section ('당일 글로벌 거시 매크로 동향') is completely eliminated.
"""

from __future__ import annotations

from pathlib import Path
import re
from typing import Dict, List, Optional
import unittest

from engine.cleaner import clean_raw_dump
from engine.digest_generator import CANONICAL_STOCKS, DigestGenerator, generate_digest
from engine.extractor import FactExtractor
from engine.models import (
    STOCK_MASTERS,
    DailyMarketData,
    KeyWatchPoints,
    MarketMetrics,
    PortfolioPairStrategy,
    StockFactSheet,
    StockSymbol,
)


def count_sentences(text: str) -> int:
    """Accurately counts sentences in Korean/English financial text, ignoring decimal points."""
    # Replace decimal numbers (e.g. 1.5, 69.36, -5.05%) so dots are not treated as sentence endings
    cleaned = re.sub(r'\d+\.\d+', 'NUM', text)
    # Replace common abbreviations with periods
    cleaned = re.sub(r'\bvs\.', 'vs', cleaned, flags=re.IGNORECASE)
    cleaned = re.sub(r'\be\.g\.', 'eg', cleaned, flags=re.IGNORECASE)
    cleaned = re.sub(r'\bi\.e\.', 'ie', cleaned, flags=re.IGNORECASE)
    cleaned = re.sub(r'\bInc\.', 'Inc', cleaned)
    cleaned = re.sub(r'\bCorp\.', 'Corp', cleaned)
    # Split by sentence ending punctuation followed by whitespace or end of string
    sents = [s.strip() for s in re.split(r'[\.!?]+(?:\s+|$)', cleaned) if s.strip()]
    return len(sents)


def parse_stock_sections(md_text: str) -> Dict[str, Dict[str, any]]:
    """Parses Section 2 of generated digest markdown into structured per-stock data."""
    sec2_match = re.search(r'## 2\. 8개 관심종목 심층 브리핑.*?(?=\n---\n|\Z)', md_text, re.DOTALL)
    if not sec2_match:
        return {}

    sec2_text = sec2_match.group(0)
    stock_blocks = re.split(r'\n### 📌\s+', sec2_text)[1:]
    results = {}

    for block in stock_blocks:
        lines = [l.rstrip() for l in block.splitlines()]
        header = lines[0].strip() if lines else ""

        # Extract [1문단 핵심 요약] text
        b1_lines = []
        b2_lines = []
        in_b1 = False
        in_b2 = False

        for line in lines[1:]:
            stripped = line.strip()
            if '#### [1문단 핵심 요약]' in stripped:
                in_b1 = True
                in_b2 = False
                continue
            elif '#### [관심있게 봐야 할 포인트 (2줄 요약)]' in stripped:
                in_b1 = False
                in_b2 = True
                continue
            elif stripped.startswith('###') or stripped.startswith('---'):
                in_b1 = False
                in_b2 = False
                continue

            if in_b1:
                b1_lines.append(line)
            elif in_b2:
                if stripped:
                    b2_lines.append(stripped)

        # Non-empty lines in B1
        b1_content_lines = [l.strip() for l in b1_lines if l.strip()]
        # Check for blank lines between text in B1
        has_blank_lines_inside_b1 = False
        if len(b1_lines) > 1:
            # Check if any empty line occurs between non-empty lines
            first_non_empty = next((i for i, l in enumerate(b1_lines) if l.strip()), None)
            last_non_empty = len(b1_lines) - 1 - next((i for i, l in enumerate(reversed(b1_lines)) if l.strip()), None)
            if first_non_empty is not None and last_non_empty is not None:
                for l in b1_lines[first_non_empty:last_non_empty + 1]:
                    if not l.strip():
                        has_blank_lines_inside_b1 = True
                        break

        b1_full_text = " ".join(b1_content_lines)
        has_subbullets_b1 = any(l.startswith(('-', '*', '•', '1.', '2.', '3.')) for l in b1_content_lines)

        results[header] = {
            "header": header,
            "b1_has_header": any('#### [1문단 핵심 요약]' in l for l in lines),
            "b1_lines": b1_content_lines,
            "b1_has_blank_lines": has_blank_lines_inside_b1,
            "b1_has_subbullets": has_subbullets_b1,
            "b1_full_text": b1_full_text,
            "b1_sentence_count": count_sentences(b1_full_text),
            "b2_has_header": any('#### [관심있게 봐야 할 포인트 (2줄 요약)]' in l for l in lines),
            "b2_lines": b2_lines,
        }

    return results


class TestMilestoneM2EndToEndRawInput(unittest.TestCase):
    """Empirical testing on real raw_input_20260930.txt."""

    @classmethod
    def setUpClass(cls) -> None:
        raw_file = Path("raw_input_20260930.txt")
        if not raw_file.exists():
            raise FileNotFoundError("raw_input_20260930.txt not found in workspace root!")
        raw_text = raw_file.read_text(encoding="utf-8")
        cleaned, meta = clean_raw_dump(raw_text)
        extractor = FactExtractor()
        cls.data = extractor.extract(cleaned, date_override="2026-09-30")
        cls.gen = DigestGenerator()
        cls.md = cls.gen.build_markdown(cls.data)
        cls.parsed_stocks = parse_stock_sections(cls.md)

    def test_canonical_8_stocks_in_section_1_matrix(self) -> None:
        """Section 1 must render the 8-stock comparative matrix table."""
        self.assertIn("### 📊 8개 관심종목 상대 성과 비교 매트릭스", self.md)
        lines = self.md.splitlines()
        table_rows = [l for l in lines if l.startswith("|") and not l.startswith("| 종목명") and not l.startswith("|---")]
        # Must have exactly 8 stock rows
        self.assertEqual(len(table_rows), 8, f"Expected 8 rows in comparative table, got {len(table_rows)}")
        for sym in CANONICAL_STOCKS:
            master = STOCK_MASTERS[sym]
            self.assertTrue(
                any(master.name_kr in row for row in table_rows),
                f"Missing {master.name_kr} in Section 1 comparative table"
            )

    def test_section_2_contains_all_8_stocks(self) -> None:
        """Section 2 must render detailed briefings for present stocks and consolidated note for missing stocks (M3 R1)."""
        self.assertEqual(
            len(self.parsed_stocks), len(self.data.stocks),
            f"Expected {len(self.data.stocks)} present stock sections in Section 2, got {len(self.parsed_stocks)}"
        )
        self.assertIn("당일 원문 데이터 미수집 종목 (관망 유지)", self.md)

    def test_section_2_stock_briefing_headers_and_subbullets(self) -> None:
        """For each of the 8 stocks, verify headers, no sub-bullets, and no blank lines in paragraph 1."""
        for header, info in self.parsed_stocks.items():
            with self.subTest(stock=header):
                self.assertTrue(info["b1_has_header"], f"{header}: Missing '#### [1문단 핵심 요약]'")
                self.assertFalse(info["b1_has_subbullets"], f"{header}: [1문단 핵심 요약] must not contain sub-bullets")
                self.assertFalse(info["b1_has_blank_lines"], f"{header}: [1문단 핵심 요약] must be a single paragraph with no blank lines separating sentences")
                self.assertTrue(info["b2_has_header"], f"{header}: Missing '#### [관심있게 봐야 할 포인트 (2줄 요약)]'")

    def test_section_2_sentence_count_3_to_6(self) -> None:
        """For each of the 8 stocks, [1문단 핵심 요약] must have between 3 and 6 sentences."""
        for header, info in self.parsed_stocks.items():
            with self.subTest(stock=header):
                cnt = info["b1_sentence_count"]
                self.assertGreaterEqual(
                    cnt, 3,
                    f"{header}: [1문단 핵심 요약] sentence count {cnt} is less than 3! Text: {info['b1_full_text']}"
                )
                self.assertLessEqual(
                    cnt, 6,
                    f"{header}: [1문단 핵심 요약] sentence count {cnt} is greater than 6! Text: {info['b1_full_text']}"
                )

    def test_section_2_two_line_watchpoints_exact_format(self) -> None:
        """For each of the 8 stocks, Line 1 and Line 2 must have exact required prefixes."""
        for header, info in self.parsed_stocks.items():
            with self.subTest(stock=header):
                lines = info["b2_lines"]
                self.assertEqual(len(lines), 2, f"{header}: Expected exactly 2 lines in watchpoints, got {len(lines)}: {lines}")
                self.assertTrue(
                    lines[0].startswith("- **단기 수급/가격선**:"),
                    f"{header}: Line 1 must start with '- **단기 수급/가격선**:', got: {lines[0]}"
                )
                self.assertTrue(
                    lines[1].startswith("- **중장기 펀더멘털/이벤트**:"),
                    f"{header}: Line 2 must start with '- **중장기 펀더멘털/이벤트**:', got: {lines[1]}"
                )
                # Verify substantive content after prefix
                l1_val = lines[0][len("- **단기 수급/가격선**:"):].strip()
                l2_val = lines[1][len("- **중장기 펀더멘털/이벤트**:"):].strip()
                self.assertGreaterEqual(len(l1_val), 5, f"{header}: Line 1 value is too short: {l1_val}")
                self.assertGreaterEqual(len(l2_val), 5, f"{header}: Line 2 value is too short: {l2_val}")

    def test_section_4_sk_pair_ratio_and_tactical_instructions(self) -> None:
        """Section 4 must preserve SK Square 57.6% vs SK Hynix 42.3% and tactical instructions."""
        self.assertIn("## 4. 포트폴리오 비중 진단 및 전술적 대응 가이드", self.md)
        self.assertIn("### ⚖️ SK스퀘어 - SK하이닉스 페어 포트폴리오 현황", self.md)
        self.assertIn("57.6%", self.md)
        self.assertIn("42.3%", self.md)
        self.assertIn("### 🎯 전술적 실행 지침 (Tactical Action Guide)", self.md)
        self.assertIn("HOLD_POSITION", self.md)
        self.assertIn("역", self.md)  # 역스위칭 경고
        self.assertIn("스위칭", self.md)

    def test_standalone_macro_elimination(self) -> None:
        """Standalone macro subsection '당일 글로벌 거시 매크로 동향' must NOT appear in digest."""
        self.assertNotIn("### 🌐 당일 글로벌 거시 매크로 동향", self.md)
        self.assertNotIn("당일 글로벌 거시 매크로 동향", self.md)


class TestSentenceCountEdgeCases(unittest.TestCase):
    """Stress tests on sentence count generation logic in DigestGenerator."""

    def setUp(self) -> None:
        self.gen = DigestGenerator()

    def test_fallback_summary_sentence_count_for_missing_stocks(self) -> None:
        """When a stock is not in input dump, fallback [1문단 핵심 요약] must still have 3 to 6 sentences."""
        for sym in CANONICAL_STOCKS:
            with self.subTest(symbol=sym.value):
                text = self.gen._build_one_paragraph_summary(None, sym)
                cnt = count_sentences(text)
                self.assertGreaterEqual(
                    cnt, 3,
                    f"Fallback summary for {sym.value} has only {cnt} sentences (must be >= 3): '{text}'"
                )
                self.assertLessEqual(
                    cnt, 6,
                    f"Fallback summary for {sym.value} has {cnt} sentences (must be <= 6): '{text}'"
                )

    def test_sheet_with_minimal_metrics_sentence_count(self) -> None:
        """When sheet has metrics but zero drivers/noise, summary must still have 3 to 6 sentences."""
        for sym in CANONICAL_STOCKS:
            with self.subTest(symbol=sym.value):
                master = STOCK_MASTERS[sym]
                sheet = StockFactSheet(
                    stock_id=sym.value,
                    stock_name=master.name_kr,
                    name_kr=master.name_kr,
                    name_en=sym.value,
                    ticker=master.ticker,
                    market=master.market,
                    category=master.category,
                    badge_color=master.badge_color,
                    metrics=MarketMetrics(stock_id=sym.value, close_price=50.0, change_percent=1.2, volume=10000),
                )
                text = self.gen._build_one_paragraph_summary(sheet, sym)
                cnt = count_sentences(text)
                self.assertGreaterEqual(
                    cnt, 3,
                    f"Minimal sheet summary for {sym.value} has only {cnt} sentences (must be >= 3): '{text}'"
                )
                self.assertLessEqual(
                    cnt, 6,
                    f"Minimal sheet summary for {sym.value} has {cnt} sentences (must be <= 6): '{text}'"
                )


class TestTwoLineWatchpointsCoverage(unittest.TestCase):
    """Validates Line 1 and Line 2 watchpoints for all 8 stocks."""

    def setUp(self) -> None:
        self.gen = DigestGenerator()

    def test_all_8_stock_default_watchpoints_contain_substantive_catalysts(self) -> None:
        """Fallback watchpoints for all 8 stocks must be non-generic and match target thesis."""
        for sym in CANONICAL_STOCKS:
            with self.subTest(symbol=sym.value):
                l1, l2 = self.gen._build_two_line_watchpoints(None, sym)
                self.assertTrue(len(l1.strip()) > 10, f"Line 1 too short for {sym.value}")
                self.assertTrue(len(l2.strip()) > 10, f"Line 2 too short for {sym.value}")

        # Pinpointed thesis checks
        _, hynix_l2 = self.gen._build_two_line_watchpoints(None, StockSymbol.SK_HYNIX)
        self.assertIn("HBM", hynix_l2)

        _, square_l2 = self.gen._build_two_line_watchpoints(None, StockSymbol.SK_SQUARE)
        self.assertIn("솔리다임", square_l2)

        celh_l1, celh_l2 = self.gen._build_two_line_watchpoints(None, StockSymbol.CELH)
        self.assertIn("골드만삭스", celh_l1)
        self.assertIn("펩시코", celh_l2)

        enph_l1, enph_l2 = self.gen._build_two_line_watchpoints(None, StockSymbol.ENPH)
        self.assertIn("Enphase Air", enph_l1)
        self.assertIn("NEM 3.0", enph_l2)


if __name__ == "__main__":
    unittest.main()
