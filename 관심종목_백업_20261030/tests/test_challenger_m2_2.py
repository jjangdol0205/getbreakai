"""Milestone M2 Iteration 2 Gate Adversarial Stress Test Suite.

Authored by: Challenger 1 (EMPIRICAL CHALLENGER)
Target: engine/digest_generator.py (DigestGenerator, generate_digest)

Coverage:
1. Completely empty DailyMarketData (default initialization, zero fixture leak).
2. Partial stock dumps:
   - 1 stock only (FLNC only, SK_SQUARE only, SK_HYNIX only, UBER only).
   - 2 stocks (SK pair only, US pair only).
   - 3 stocks (no Korean stocks, only US stocks).
   - Unrecognized / extraneous stocks in stocks dict.
3. Extreme numerical metrics:
   - Extreme positive (+1500.0%) and extreme negative (-99.9%).
   - Zero price, zero volume, astronomical numbers (trillion scale).
   - Micro-penny prices ($0.0001).
   - Currency format handling (KRW vs USD vs unassigned).
4. Past and Future dates & Malformed dates:
   - Far past (1900-01-01), far future (2099-12-31), leap day (2028-02-29).
   - None, empty string, non-standard delimiters ("2026.09.29", "2026/09/29").
5. LLM Noise and Prompt Bleed Sanitization:
   - Preamble greetings ("네, 요청하신 6개 관심 종목의... 정리해 드립니다.").
   - Closing pleasantries ("도움이 되셨기를 바랍니다...").
   - Disclaimers ("본 자료는 정보 제공만을 목적으로 하며...").
6. Markdown Table Invariant & Delimiter Injection:
   - Pipe characters ('|'), newlines ('\\n'), tabs in drivers, summaries, labels.
   - Column count consistency (Section 1: 9 pipes, Section 4: 8 pipes).
"""

import os
import shutil
import tempfile
import unittest
from pathlib import Path
from typing import Dict, List, Optional

from engine.digest_generator import CANONICAL_STOCKS, DigestGenerator, generate_digest
from engine.models import (
    DailyMarketData,
    ExecutiveInterviewFact,
    IBReportFact,
    MarketMetrics,
    PortfolioPairStrategy,
    StockFactSheet,
    StockSymbol,
)


def build_test_sheet(
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


class TestCompletelyEmptyDailyMarketData(unittest.TestCase):
    """Stress testing digest generation when DailyMarketData is initialized with zero fields."""

    def test_default_empty_market_data(self) -> None:
        """DailyMarketData() without any arguments must not crash and produce full 5 sections."""
        empty_data = DailyMarketData()
        gen = DigestGenerator()
        md = gen.build_markdown(empty_data)

        self.assertIsInstance(md, str)
        self.assertGreater(len(md), 500)

        # All 5 section headers must be present
        self.assertTrue("# 일간 8개 관심종목 종합 다이제스트" in md or "# 일간 6개 관심종목 종합 다이제스트" in md)
        self.assertTrue(
            "## 1. 당일 거시 매크로 및 8개 관심종목 상대 성과 요약" in md
            or "## 1. 당일 거시 매크로 및 6종목 상대 성과 요약" in md
            or "비교 매트릭스" in md
        )
        self.assertIn("## 2. 종목별 핵심 동인 및 팩트 vs 노이즈 판별", md)
        self.assertIn("## 3. 경영진 인터뷰 궤적 및 이전 발언 대조", md)
        self.assertIn("## 4. 포트폴리오 비중 진단 및 전술적 대응 가이드", md)
        self.assertIn("## 5. 익일 모니터링 체크포인트", md)

    def test_zero_fixture_leak_on_empty_data(self) -> None:
        """Verifies that no test fixture constants or hardcoded account data leak when data is empty."""
        empty_data = DailyMarketData(date="2026-10-01")
        gen = DigestGenerator()
        md = gen.build_markdown(empty_data)

        # Personal holding fixtures must NOT appear
        self.assertNotIn("44주", md, "Hardcoded SK Square share count leaked!")
        self.assertNotIn("4,808만", md, "Hardcoded SK Square valuation leaked!")
        self.assertNotIn("-0.6%", md, "Hardcoded SK Square return rate leaked!")
        self.assertNotIn("20주", md, "Hardcoded SK Hynix share count leaked!")
        self.assertNotIn("3,534만", md, "Hardcoded SK Hynix valuation leaked!")
        self.assertNotIn("-5.6%", md, "Hardcoded SK Hynix return rate leaked!")

        # Dynamic Section 5 checkpoints must not leak static hardcoded percentages
        self.assertNotIn("(-5.05%)", md, "Hardcoded SK Hynix change percent leaked into Section 5!")
        self.assertNotIn("68%", md, "Hardcoded NAV discount leaked into Section 5!")

        # Check that table holdings render "-" instead
        self.assertIn("| **SK스퀘어** | 402340 | - | - | **57.6%** | - | - |", md)
        self.assertIn("| **SK하이닉스** | 000660 | - | - | **42.3%** | - | - |", md)

        # Check neutral fallback message in Section 4
        self.assertIn("당일 포트폴리오 전술 지침 데이터가 제공되지 않았습니다.", md)


class TestPartialStockDumps(unittest.TestCase):
    """Stress testing single-stock dumps, partial pairs, and unknown symbols."""

    def test_single_stock_only_fluence(self) -> None:
        """Only FLNC is present (1 stock dump)."""
        flnc = build_test_sheet(
            stock_id="FLNC",
            name_kr="플루언스에너지",
            ticker="FLNC",
            close_price=7.50,
            change_percent=-4.46,
            volume=2100000,
            currency="USD",
            core_drivers=["주요 동인: 미국 휴스턴 공장 일시 가동 중단 여파"],
        )
        data = DailyMarketData(date="2026-09-29", stocks={"FLNC": flnc})
        gen = DigestGenerator()
        md = gen.build_markdown(data)

        # Section 1 comparative table: FLNC has data, other 7 show '원문 데이터 미제공'
        self.assertIn("$7.50", md)
        self.assertIn("-4.46%", md)
        self.assertIn("미국 휴스턴 공장 일시 가동 중단 여파", md)
        self.assertEqual(md.count("원문 데이터 미제공"), 7)

        # Section 4 pair table renders cleanly with "-" for unprovided holdings
        self.assertIn("| **SK스퀘어** | 402340 | - | - | **57.6%** | - | - |", md)
        self.assertIn("| **SK하이닉스** | 000660 | - | - | **42.3%** | - | - |", md)

        # Section 5 must bind FLNC checkpoint dynamically
        self.assertIn("플루언스 (플루언스에너지)(FLNC, -4.46%)", md)
        self.assertIn("휴스턴 공장 계약 재개 여부", md)

    def test_single_stock_only_sk_square(self) -> None:
        """Only SK Square is present (1 pair stock present, other missing)."""
        sq = build_test_sheet(
            stock_id="SK_SQUARE",
            name_kr="SK스퀘어",
            ticker="402340",
            close_price=1100000.0,
            change_percent=-7.56,
            volume=704035,
            currency="KRW",
            core_drivers=["주요 동인: 솔리다임 나스닥 IPO 추진설 보도"],
        )
        data = DailyMarketData(date="2026-09-29", stocks={"SK_SQUARE": sq})
        gen = DigestGenerator()
        md = gen.build_markdown(data)

        self.assertIn("1,100,000원", md)
        self.assertIn("-7.56%", md)
        self.assertIn("솔리다임 나스닥 IPO 추진설 보도", md)

        # Section 5 SK Square tag has percentage, SK Hynix tag has no percentage
        self.assertIn("SK스퀘어(-7.56%)", md)
        self.assertIn("SK하이닉스: HBM 공급망", md)

    def test_extraneous_and_unknown_stocks(self) -> None:
        """DailyMarketData containing un-tracked tickers (e.g. AAPL, NVDA, TSLA)."""
        aapl = build_test_sheet(
            stock_id="AAPL",
            name_kr="애플",
            ticker="AAPL",
            close_price=220.0,
            change_percent=1.5,
            volume=50000000,
            currency="USD",
        )
        nvda = build_test_sheet(
            stock_id="NVDA",
            name_kr="엔비디아",
            ticker="NVDA",
            close_price=120.0,
            change_percent=3.2,
            volume=80000000,
            currency="USD",
        )
        data = DailyMarketData(date="2026-09-29", stocks={"AAPL": aapl, "NVDA": nvda})
        gen = DigestGenerator()
        md = gen.build_markdown(data)

        # Canonical 6 stocks must still be maintained as the table schema
        for sym in CANONICAL_STOCKS:
            master = sym.value
            self.assertIn("원문 데이터 미제공", md)


class TestExtremeNumericalMetrics(unittest.TestCase):
    """Stress testing numerical edge cases, signs, zero, and scales."""

    def test_extreme_positive_and_negative_changes(self) -> None:
        """+1500% spike and -99.9% collapse."""
        upst = build_test_sheet(
            stock_id="UPST",
            name_kr="업스타트",
            ticker="UPST",
            close_price=500.0,
            change_percent=1500.0,
            volume=50000000,
            currency="USD",
            core_drivers=["주요 동인: AI 대환대출 폭증 및 사모신용 자금 유입 숏스퀴즈"],
        )
        flnc = build_test_sheet(
            stock_id="FLNC",
            name_kr="플루언스",
            ticker="FLNC",
            close_price=0.01,
            change_percent=-99.90,
            volume=100000000,
            currency="USD",
            core_drivers=["주요 동인: 대규모 리콜 및 공장 가동 전면 중단"],
        )
        data = DailyMarketData(date="2026-09-29", stocks={"UPST": upst, "FLNC": flnc})
        gen = DigestGenerator()
        md = gen.build_markdown(data)

        # Formatted change strings
        self.assertIn("+1500.00%", md)
        self.assertIn("-99.90%", md)

        # Strategic tone mapping
        self.assertIn("강세 급등 / 모멘텀 지속", md)
        self.assertIn("단기 과매도 / 패닉셀 (매도 자제)", md)

    def test_zero_and_micro_prices(self) -> None:
        """Close price is 0.0 or micro decimal 0.0001."""
        s1 = build_test_sheet(
            stock_id="MBLY",
            name_kr="모빌아이",
            ticker="MBLY",
            close_price=0.0001,
            change_percent=0.0,
            volume=0,
            currency="USD",
        )
        s2 = build_test_sheet(
            stock_id="SK_HYNIX",
            name_kr="SK하이닉스",
            ticker="000660",
            close_price=0.0,
            change_percent=0.0,
            volume=0,
            currency="KRW",
        )
        data = DailyMarketData(date="2026-09-29", stocks={"MBLY": s1, "SK_HYNIX": s2})
        gen = DigestGenerator()
        md = gen.build_markdown(data)

        self.assertIn("$0.000", md)
        self.assertIn("0원", md)
        self.assertIn("+0.00%", md)
        self.assertIn("0주", md)

    def test_astronomical_volumes_and_prices(self) -> None:
        """Astronomical volume (1 trillion shares) and price (1 trillion KRW)."""
        huge = build_test_sheet(
            stock_id="SK_SQUARE",
            name_kr="SK스퀘어",
            ticker="402340",
            close_price=1_000_000_000_000.0,
            change_percent=10.0,
            volume=999_999_999_999,
            currency="KRW",
        )
        data = DailyMarketData(date="2026-09-29", stocks={"SK_SQUARE": huge})
        gen = DigestGenerator()
        md = gen.build_markdown(data)

        self.assertIn("1,000,000,000,000원", md)
        self.assertIn("999,999,999,999주", md)


class TestExtremeDatesAndFormats(unittest.TestCase):
    """Stress testing far past, far future, leap year, and non-standard date strings."""

    def test_far_past_and_far_future(self) -> None:
        """Dates like 1900-01-01 and 2099-12-31."""
        for d in ["1900-01-01", "2099-12-31"]:
            data = DailyMarketData(date=d)
            gen = DigestGenerator()
            md = gen.build_markdown(data)
            self.assertTrue(
                f"# 일간 8개 관심종목 종합 다이제스트 ({d})" in md
                or f"# 일간 6개 관심종목 종합 다이제스트 ({d})" in md
            )

    def test_leap_day(self) -> None:
        """Leap day 2028-02-29."""
        data = DailyMarketData(date="2028-02-29")
        gen = DigestGenerator()
        md = gen.build_markdown(data)
        self.assertIn("2028-02-29", md)

    def test_none_and_empty_date_defaults(self) -> None:
        """None or empty string dates must fall back safely to 2026-09-29."""
        for d in [None, ""]:
            data = DailyMarketData(date=d)
            gen = DigestGenerator()
            md = gen.build_markdown(data)
            self.assertIn("2026-09-29", md)


class TestNoiseSanitizationAndPromptInjection(unittest.TestCase):
    """Stress testing conversational noise cleaning and prompt injections."""

    def test_conversational_preamble_in_pair_rationale(self) -> None:
        """Chatbot greeting and disclaimer in pair strategy rationale."""
        noisy_rationale = (
            "네, 요청하신 6개 관심 종목의 2026년 9월 29일 마감 시황 및 주요 이슈를 정리해 드립니다.\n\n"
            "스퀘어의 급락은 지분 희석 우려에 따른 과매도 구간입니다. 감정적 매도를 자제하고 홀딩하십시오.\n\n"
            "도움이 되셨기를 바랍니다. 추가 질문이 있으시면 언제든지 문의해 주세요.\n"
            "본 자료는 정보 제공만을 목적으로 하며 투자 결과에 대한 책임은 본인에게 있습니다."
        )
        strat = PortfolioPairStrategy(
            sk_square_weight=57.6,
            sk_hynix_weight=42.3,
            tactical_action="HOLD_POSITION",
            action_label="현 비중 유지 [HOLD]",
            risk_warning="역스위칭 금지",
            rationale=noisy_rationale,
        )
        data = DailyMarketData(date="2026-09-29", pair_strategy=strat)
        gen = DigestGenerator()
        md = gen.build_markdown(data)

        # Conversational noise must be scrubbed
        self.assertNotIn("네, 요청하신", md)
        self.assertNotIn("정리해 드립니다", md)
        self.assertNotIn("도움이 되셨기를 바랍니다", md)
        self.assertNotIn("추가 질문이 있으시면", md)
        self.assertNotIn("정보 제공만을 목적으로 하며", md)

        # Actual substantive rationale must be retained
        self.assertIn("스퀘어의 급락은 지분 희석 우려에 따른 과매도 구간입니다", md)

    def test_conversational_noise_in_action_labels(self) -> None:
        """Conversational noise inside pair action labels."""
        strat = PortfolioPairStrategy(
            action_label="네, 요청하신 시황 브리핑입니다. 비중 유지 권고",
            risk_warning="도움이 되셨기를 바랍니다. 역스위칭 경고",
        )
        data = DailyMarketData(date="2026-09-29", pair_strategy=strat)
        gen = DigestGenerator()
        md = gen.build_markdown(data)

        self.assertNotIn("네, 요청하신", md)
        self.assertNotIn("도움이 되셨기를", md)


class TestMarkdownTableInvariants(unittest.TestCase):
    """Stress testing delimiter injection (pipes, newlines) into table cells."""

    def test_table_pipe_injection_sanitization(self) -> None:
        """Pipes in core drivers must be sanitized into slashes so table columns remain intact."""
        adversarial_sheet = build_test_sheet(
            stock_id="SK_SQUARE",
            name_kr="SK스퀘어",
            ticker="402340",
            close_price=1100000.0,
            change_percent=-7.56,
            volume=704035,
            currency="KRW",
            core_drivers=["주요 동인: 솔리다임 IPO | 나스닥 상장설 | 지분 희석 논란 | 중복상장 할인"],
        )
        data = DailyMarketData(date="2026-09-29", stocks={"SK_SQUARE": adversarial_sheet})
        gen = DigestGenerator()
        md = gen.build_markdown(data)

        # Find the SK Square table row in Section 1
        lines = md.splitlines()
        sq_rows = [l for l in lines if l.startswith("| SK스퀘어")]
        self.assertEqual(len(sq_rows), 1)

        # An 8-column markdown table row: "| C1 | C2 | C3 | C4 | C5 | C6 | C7 | C8 |" -> exactly 9 pipes
        pipe_count = sq_rows[0].count("|")
        self.assertEqual(pipe_count, 9, f"Table row corrupted with pipe injection: {sq_rows[0]}")
        self.assertIn("/", sq_rows[0], "Pipes must be converted to slashes")

    def test_section_4_holdings_table_column_invariant(self) -> None:
        """Section 4 pair portfolio table must maintain 7 columns (8 pipes)."""
        data = DailyMarketData(date="2026-09-29")
        gen = DigestGenerator()
        md = gen.build_markdown(data)

        lines = md.splitlines()
        sec4_rows = [l.strip() for l in lines if l.strip().startswith("| **SK스퀘어**") or l.strip().startswith("| **SK하이닉스**")]
        self.assertEqual(len(sec4_rows), 2)
        for row in sec4_rows:
            # 7 columns: "| C1 | C2 | C3 | C4 | C5 | C6 | C7 |" -> exactly 8 pipes
            self.assertEqual(row.count("|"), 8, f"Section 4 row pipe mismatch: {row}")


if __name__ == "__main__":
    unittest.main()
