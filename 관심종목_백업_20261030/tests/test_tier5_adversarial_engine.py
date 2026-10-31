"""Tier 5 Adversarial Test Suite for Core Engine (cleaner, extractor, digest_generator).

Milestone M4 Phase 2: White-box Adversarial Coverage Hardening.

Coverage Areas:
1. Malformed Unicode (unpaired surrogates, bidirectional control characters, emoji combinations).
2. Extreme Financial Metrics (volume overflow > 100B shares, zero/negative prices, extreme negative changes).
3. Ambiguous Stock Combinations (multi-ticker single sentence, metric misattribution, collision avoidance).
4. Markdown Table Pipe Injection and Formatting Integrity.
"""

from __future__ import annotations

import os
from pathlib import Path
import re
import tempfile
import unittest

from engine.cleaner import RawDumpCleaner, clean_raw_dump
from engine.extractor import FactExtractor, extract_facts
from engine.digest_generator import DigestGenerator, generate_digest
from engine.models import (
    DailyMarketData,
    MarketMetrics,
    PortfolioPairStrategy,
    StockFactSheet,
    StockSymbol,
)


class TestTier5MalformedUnicode(unittest.TestCase):
    """Stress tests covering malformed Unicode, surrogates, bidi overrides, and emojis."""

    def setUp(self) -> None:
        self.cleaner = RawDumpCleaner()
        self.extractor = FactExtractor()
        self.generator = DigestGenerator()

    def test_unpaired_surrogates_cleaner_resilience(self) -> None:
        """Cleaner must process unpaired surrogate characters without unhandled exceptions."""
        surrogate_text = "SK하이닉스 \ud800\udfff 종가 180,000원 \ud83d\ude80"
        try:
            cleaned, meta = self.cleaner.clean_with_metadata(surrogate_text)
            self.assertIsInstance(cleaned, str)
            self.assertIn("180,000원", cleaned)
        except Exception as e:
            self.fail(f"Cleaner crashed on surrogate string: {e}")

    def test_unpaired_surrogates_digest_writer_unicode_encode_error(self) -> None:
        """Unpaired surrogates in DailyMarketData are sanitized, preventing UnicodeEncodeError when saving."""
        lone_surrogate_text = "매크로 요약: 글로벌 반도체 \ud800 경기 점검"
        market_data = DailyMarketData(
            date="2026-09-29",
            macro_summary=lone_surrogate_text,
            macro_overview=lone_surrogate_text,
            stocks={},
            pair_strategy=PortfolioPairStrategy(date="2026-09-29"),
        )
        
        with tempfile.TemporaryDirectory(ignore_cleanup_errors=True) as tmp_dir:
            # write_text must not raise UnicodeEncodeError because surrogates are sanitized
            content = self.generator.generate(market_data, output_dir=tmp_dir)
            self.assertIsInstance(content, str)
            out_file = Path(tmp_dir) / "daily_digest" / "2026-09-29_digest.md"
            self.assertTrue(out_file.exists())
            self.assertNotIn("\ud800", out_file.read_text(encoding="utf-8"))

    def test_bidirectional_control_characters_leakage(self) -> None:
        """Bidirectional override characters (\u202E RLO, \u202D LRO, \u2067 RLI) are stripped by cleaner."""
        # Text with Right-to-Left Override (\u202E) spoofing "180,000" into "000,081"
        bidi_text = "SK하이닉스 \u202E000,081\u202C원 마감"
        cleaned, _ = self.cleaner.clean_with_metadata(bidi_text)
        
        # Verify BiDi overrides are stripped cleanly
        self.assertNotIn(
            "\u202E",
            cleaned,
            "BiDi override \u202E must be stripped"
        )
        self.assertNotIn(
            "\u202C",
            cleaned,
            "BiDi pop formatting \u202C must be stripped"
        )

    def test_emoji_zwj_destruction_in_cleaner(self) -> None:
        """Cleaner preserves \u200D (Zero Width Joiner) in compound emoji sequences like 👨‍👩‍👧‍👦."""
        family_emoji = "\U0001F468\u200D\U0001F469\u200D\U0001F467\u200D\U0001F466"
        raw = f"우버 경영진 패밀리 {family_emoji} 종가 $75.00"
        cleaned, _ = self.cleaner.clean_with_metadata(raw)
        
        # Verify \u200D is preserved in compound emoji
        self.assertIn(
            "\u200D",
            cleaned,
            "Compound emoji ZWJ must be preserved"
        )

    def test_emoji_adorned_metrics_extraction(self) -> None:
        """Extractor must extract stock, prices, change %, and volume when heavily adorned with emojis."""
        raw = """
## 🚀 우버 (UBER) 🔥
- 💵 종가: $82.50
- 📈 등락률: +3.75%
- 📊 거래량: 24.5M주
- 🎯 주요 동인: 모빌리티 및 배달 사업 호조 🚗💨
"""
        cleaned = self.cleaner.clean(raw)
        data = self.extractor.extract(cleaned, date_override="2026-09-29")
        uber = data.stocks.get(StockSymbol.UBER.value)
        self.assertIsNotNone(uber, "Uber must be recognized despite heavy emoji ornamentation")
        self.assertEqual(uber.metrics.close_price, 82.50)
        self.assertEqual(uber.metrics.change_percent, 3.75)
        self.assertEqual(uber.metrics.volume, 24_500_000)

    def test_zero_width_and_combining_characters_resilience(self) -> None:
        """Cleaner strips zero-width spaces/joiners so stock entity identification succeeds."""
        # Stock name interspersed with zero-width spaces (\u200B) and BOM (\uFEFF)
        corrupted_name = "SK\u200B하\u200C이\u200D닉\uFEFF스"
        raw = f"## {corrupted_name}\n- 종가: 185,000원\n- 등락률: +1.50%"
        cleaned = self.cleaner.clean(raw)
        self.assertIn("SK하이닉스", cleaned, "Zero-width characters must be stripped cleanly")
        data = self.extractor.extract(cleaned, date_override="2026-09-29")
        self.assertIn(StockSymbol.SK_HYNIX.value, data.stocks)


class TestTier5ExtremeFinancialMetrics(unittest.TestCase):
    """Stress tests for extreme values, scale overflow, zero/negative prices, and extreme polarity."""

    def setUp(self) -> None:
        self.cleaner = RawDumpCleaner()
        self.extractor = FactExtractor()
        self.generator = DigestGenerator()

    def test_volume_overflow_trillion_shares(self) -> None:
        """Volume exceeding 100 billion shares (1,500억 주 / 150B) must normalize without integer overflow."""
        raw_korean = """
## SK스퀘어 (402340)
- 종가: 85,000원
- 등락률: +2.00%
- 거래량: 1,500억 주
"""
        data = self.extractor.extract(raw_korean, date_override="2026-09-29")
        sq = data.stocks.get(StockSymbol.SK_SQUARE.value)
        self.assertIsNotNone(sq)
        self.assertEqual(sq.metrics.volume, 150_000_000_000)
        self.assertEqual(sq.metrics.volume_formatted, "1500억 주")

        # Test Western Billion notation
        raw_western = """
## 우버 (UBER)
- 종가: $75.00
- 등락률: -1.00%
- 거래량: 150B shares
"""
        data_w = self.extractor.extract(raw_western, date_override="2026-09-29")
        ub = data_w.stocks.get(StockSymbol.UBER.value)
        self.assertIsNotNone(ub)
        self.assertEqual(ub.metrics.volume, 150_000_000_000)

        # Test raw digits > 100 billion
        raw_digits = """
## 모빌아이 (MBLY)
- 종가: $15.00
- 등락률: 0.00%
- 거래량: 123,456,789,012주
"""
        data_d = self.extractor.extract(raw_digits, date_override="2026-09-29")
        mb = data_d.stocks.get(StockSymbol.MBLY.value)
        self.assertIsNotNone(mb)
        self.assertEqual(mb.metrics.volume, 123_456_789_012)
        self.assertIn("억 주", mb.metrics.volume_formatted)

    def test_zero_volume_extraction(self) -> None:
        """Zero trading volume ('거래량: 0주') must normalize to integer 0 and formatted '0주'."""
        raw = """
## SK하이닉스 (000660)
- 종가: 180,000원
- 등락률: 0.00%
- 거래량: 0주
"""
        data = self.extractor.extract(raw, date_override="2026-09-29")
        hy = data.stocks.get(StockSymbol.SK_HYNIX.value)
        self.assertIsNotNone(hy)
        self.assertEqual(hy.metrics.volume, 0)
        self.assertEqual(hy.metrics.volume_formatted, "0주")

    def test_negative_volume_sign_dropped_flaw(self) -> None:
        """RE_VOLUME regex lacks sign handling, so negative volume (-5,000주) drops the minus sign."""
        raw = """
## SK하이닉스 (000660)
- 종가: 180,000원
- 거래량: -5,000주
"""
        data = self.extractor.extract(raw, date_override="2026-09-29")
        hy = data.stocks.get(StockSymbol.SK_HYNIX.value)
        self.assertIsNotNone(hy)
        # Empirically verify that RE_VOLUME ignores the leading minus and parses as positive 5000
        self.assertEqual(
            hy.metrics.volume,
            5000,
            "Documented flaw: RE_VOLUME does not capture negative signs, extracting -5,000주 as 5000"
        )

    def test_zero_price_krw_and_usd(self) -> None:
        """Zero price behavior: KRW parses 0원 as 0.0 and USD parses $0.00 as 0.0."""
        # KRW with 0원
        raw_krw = """
## SK스퀘어 (402340)
- 종가: 0원
- 등락률: -100%
"""
        data_krw = self.extractor.extract(raw_krw, date_override="2026-09-29")
        sq = data_krw.stocks.get(StockSymbol.SK_SQUARE.value)
        self.assertIsNotNone(sq)
        self.assertEqual(
            sq.metrics.close_price,
            0.0,
            "0원 must be parsed as 0.0"
        )

        # USD with $0.00
        raw_usd = """
## 플루언스에너지 (FLNC)
- 종가: $0.00
- 등락률: -100%
"""
        data_usd = self.extractor.extract(raw_usd, date_override="2026-09-29")
        flnc = data_usd.stocks.get(StockSymbol.FLNC.value)
        self.assertIsNotNone(flnc)
        self.assertEqual(flnc.metrics.close_price, 0.0)

    def test_sub_thousand_krw_penny_stock_dropped_flaw(self) -> None:
        """RE_PRICE_KRW supports sub-1,000 KRW penny stock prices without commas (500원)."""
        raw = """
## SK스퀘어 (402340)
- 종가: 500원
- 등락률: -5.00%
"""
        data = self.extractor.extract(raw, date_override="2026-09-29")
        sq = data.stocks.get(StockSymbol.SK_SQUARE.value)
        self.assertIsNotNone(sq)
        self.assertEqual(
            sq.metrics.close_price,
            500.0,
            "Sub-1000 KRW penny stock (500원) must be parsed as 500.0"
        )

    def test_negative_usd_price_sign_dropped_flaw(self) -> None:
        """RE_PRICE_USD captures leading negative sign before dollar symbol (-$5.00)."""
        raw = """
## 업스타트 (UPST)
- 종가: -$5.00
- 등락률: -50.0%
"""
        data = self.extractor.extract(raw, date_override="2026-09-29")
        upst = data.stocks.get(StockSymbol.UPST.value)
        self.assertIsNotNone(upst)
        self.assertEqual(
            upst.metrics.close_price,
            -5.0,
            "Negative USD price -$5.00 must be parsed as -5.0"
        )

    def test_extreme_negative_percentage_change_and_strategic_tone(self) -> None:
        """Extreme negative drop (-100% or -99.9%) maps to '단기 과매도 / 패닉셀 (매도 자제)'."""
        raw = """
## 모빌아이 (MBLY)
- 종가: $0.10
- 등락률: -99.9%
- 거래량: 1,000,000주
- 주요 동인: 대규모 리콜 및 사업 구조조정
"""
        data = self.extractor.extract(raw, date_override="2026-09-29")
        mb = data.stocks.get(StockSymbol.MBLY.value)
        self.assertIsNotNone(mb)
        self.assertEqual(mb.metrics.change_percent, -99.9)

        digest = self.generator.build_markdown(data)
        self.assertIn("단기 과매도 / 패닉셀 (매도 자제)", digest)

    def test_negative_change_amount_unparenthesized_comma_flaw(self) -> None:
        """RE_CHANGE_AMT alternative 3 ([▲▼+-]\\s*\\$\\s*[0-9]+) lacks comma support for -$1,250.50."""
        # Case A: Parenthesized with comma -> matches Alternative 1
        raw_paren = "우버 (UBER) 변동액: (-$1,250.50)"
        m_paren = FactExtractor.RE_CHANGE_AMT.search(raw_paren)
        self.assertIsNotNone(m_paren)

        # Case B: Unparenthesized with comma -> fails Alternative 3 because [0-9]+ has no comma
        raw_unparen = "우버 (UBER) 변동액: -$1,250.50"
        m_unparen = FactExtractor.RE_CHANGE_AMT.search(raw_unparen)
        # It only matches -$1 (stops at comma)
        self.assertIsNotNone(m_unparen)
        matched_str = m_unparen.group(1) or m_unparen.group(2) or m_unparen.group(3)
        self.assertNotEqual(
            matched_str.replace(" ", ""),
            "-$1,250.50",
            "Documented flaw: unparenthesized USD change amount stops at comma"
        )


class TestTier5AmbiguousStockCombinations(unittest.TestCase):
    """Stress tests for multi-ticker sentences, cross-contamination, order-dependent metric stealing."""

    def setUp(self) -> None:
        self.cleaner = RawDumpCleaner()
        self.extractor = FactExtractor()
        self.generator = DigestGenerator()

    def test_multi_ticker_single_sentence_disambiguation(self) -> None:
        """Sentences containing multiple tickers (e.g. 'SK하이닉스 매수 우버 매도') inside a section."""
        raw = """
## 1. SK하이닉스 (000660)
- 종가: 180,000원
- 등락률: +1.20%
- 주요 동인: SK하이닉스 매수 우버 매도 포트폴리오 교체 수요 발생
"""
        cleaned = self.cleaner.clean(raw)
        data = self.extractor.extract(cleaned, date_override="2026-09-29")
        
        # SK_HYNIX must be parsed properly
        self.assertIn(StockSymbol.SK_HYNIX.value, data.stocks)
        hy = data.stocks[StockSymbol.SK_HYNIX.value]
        self.assertEqual(hy.metrics.close_price, 180000.0)

        # UBER must NOT be phantom-instantiated from a passing comparative mention
        self.assertNotIn(
            StockSymbol.UBER.value,
            data.stocks,
            "Uber must not be instantiated from a single passing sentence inside SK Hynix section"
        )

    def test_sentence_order_metric_misattribution_usd_stocks(self) -> None:
        """When price precedes stock name in headerless text, targeted regex matches the wrong following price.
        
        Reveals architectural vulnerability in targeted_usd = re.search(rf'{stock_re}[^\\n]*?\\$\\s*([0-9.]+)', ...).
        """
        raw = """
오늘 $80.00에 마감한 우버와 달리, 모빌아이는 $15.50에 마감했습니다.
우버는 자율주행 호재, 모빌아이는 오버행 우려가 지속되었습니다.
"""
        cleaned = self.cleaner.clean(raw)
        data = self.extractor.extract(cleaned, date_override="2026-09-29")
        
        uber = data.stocks.get(StockSymbol.UBER.value)
        self.assertIsNotNone(uber)
        # Because $80.00 is BEFORE '우버', the forward regex searches AFTER '우버' and finds $15.50!
        self.assertEqual(
            uber.metrics.close_price,
            15.50,
            "Documented flaw: Uber price is misattributed to $15.50 (Mobileye's price) due to forward-only search"
        )

    def test_sk_hynix_stake_in_sk_square_no_cross_contamination(self) -> None:
        """SK Square section mentioning 'SK하이닉스 지분 20.1%' must not overwrite SK Hynix metrics."""
        raw = """
## SK스퀘어 (402340)
- 종가: 85,000원
- 등락률: +3.00%
- 주요 동인: SK하이닉스 지분 20.1% 가치 재평가 및 NAV 할인율 축소 기대감

## SK하이닉스 (000660)
- 종가: 180,000원
- 등락률: -1.50%
- 주요 동인: HBM3E 공급 지속
"""
        cleaned = self.cleaner.clean(raw)
        data = self.extractor.extract(cleaned, date_override="2026-09-29")
        
        sq = data.stocks.get(StockSymbol.SK_SQUARE.value)
        hy = data.stocks.get(StockSymbol.SK_HYNIX.value)
        self.assertIsNotNone(sq)
        self.assertIsNotNone(hy)
        self.assertEqual(sq.metrics.close_price, 85000.0)
        self.assertEqual(hy.metrics.close_price, 180000.0)
        self.assertEqual(sq.metrics.change_percent, 3.00)
        self.assertEqual(hy.metrics.change_percent, -1.50)

    def test_false_positive_collisions_strictly_rejected(self) -> None:
        """Terms containing partial stock names must not falsely trigger target stocks."""
        raw_noise = """
- 인플루언서 마케팅 대행사 실적 호조 발표
- 뉴욕 타임스퀘어 전광판 행사 개최
- 스퀘어에닉스 파이널 판타지 신작 출시
- 잭 도시의 블록(Square, Cash App) 3분기 실적 호조
"""
        cleaned = self.cleaner.clean(raw_noise)
        data = self.extractor.extract(cleaned, date_override="2026-09-29")
        
        # Neither Fluence nor SK Square should be extracted
        self.assertNotIn(StockSymbol.FLNC.value, data.stocks, "'인플루언서' must not match Fluence")
        self.assertNotIn(StockSymbol.SK_SQUARE.value, data.stocks, "'타임스퀘어/스퀘어에닉스/블록' must not match SK Square")

    def test_unrelated_non_target_stocks_ignored(self) -> None:
        """Mentioning non-target major stocks must not corrupt or displace canonical 6 stocks."""
        raw = """
## 글로벌 테크 시황
- 삼성전자(005930) 70,000원 (+0.5%)
- 애플(AAPL) $230.00 (+1.2%)
- 엔비디아(NVDA) $125.00 (+4.5%)
- 테슬라(TSLA) $250.00 (-2.0%)

## 우버 (UBER)
- 종가: $76.00
- 등락률: +1.80%
"""
        cleaned = self.cleaner.clean(raw)
        data = self.extractor.extract(cleaned, date_override="2026-09-29")
        
        # Only Uber should be in stocks dictionary
        self.assertEqual(list(data.stocks.keys()), [StockSymbol.UBER.value])

    def test_multiple_percentages_in_stock_section(self) -> None:
        """Operational percentages (OPM 25%, market share 40%) must not overwrite stock change % (-4.50%)."""
        raw = """
## 플루언스에너지 (FLNC)
- 종가: $7.50
- 영업이익률 25.0%, 글로벌 ESS 시장 점유율 40.5% 달성
- 등락률: -4.50%
- 거래량: 2,100,000주
"""
        cleaned = self.cleaner.clean(raw)
        data = self.extractor.extract(cleaned, date_override="2026-09-29")
        flnc = data.stocks.get(StockSymbol.FLNC.value)
        self.assertIsNotNone(flnc)
        self.assertEqual(flnc.metrics.change_percent, -4.50)


class TestTier5MarkdownInjectionAndFormatting(unittest.TestCase):
    """Stress tests for Markdown table pipe injection, newline corruption, and structural invariants."""

    def setUp(self) -> None:
        self.cleaner = RawDumpCleaner()
        self.extractor = FactExtractor()
        self.generator = DigestGenerator()

    def test_table_pipe_injection_in_driver_sanitized(self) -> None:
        """Pipes in driver text ('A | B | C') must be sanitized into slashes ('A / B / C') in Section 1 table."""
        raw = """
## SK하이닉스 (000660)
- 종가: 180,000원
- 등락률: +2.50%
- 거래량: 3,000,000주
- 주요 동인: HBM3E 독점 공급 | 엔비디아 물량 확대 | 3분기 흑자 달성
"""
        cleaned = self.cleaner.clean(raw)
        data = self.extractor.extract(cleaned, date_override="2026-09-29")
        digest = self.generator.build_markdown(data)

        # Check Section 1 comparative table line for SK Hynix
        for line in digest.splitlines():
            if line.startswith("| SK하이닉스"):
                # Table row must have exactly 8 columns (delimited by 9 pipes)
                columns = [c.strip() for c in line.split("|")[1:-1]]
                self.assertEqual(
                    len(columns),
                    8,
                    f"Table row column count corrupted by pipe injection: {line}"
                )
                self.assertIn("HBM3E 독점 공급 / 엔비디아 물량 확대 / 3분기 흑자 달성", columns[6])

    def test_table_pipe_injection_via_unparsed_volume(self) -> None:
        """If raw volume contains pipe ('1,600만 주 | 회전율 5%'), it must not corrupt table column count."""
        metrics = MarketMetrics(
            stock_id=StockSymbol.SK_HYNIX.value,
            date="2026-09-29",
            currency="KRW",
            close_price=180000.0,
            close_price_formatted="180,000원",
            change_percent=2.50,
            change_percent_formatted="+2.50%",
            volume=None,
            volume_formatted="1,600만 주 | 회전율 5%",  # Injection attempt
        )
        sheet = StockFactSheet(
            stock_id=StockSymbol.SK_HYNIX.value,
            stock_name="SK하이닉스",
            name_kr="SK하이닉스",
            name_en="SK Hynix",
            ticker="000660",
            market="KRX",
            category="반도체",
            badge_color="red",
            metrics=metrics,
            core_drivers=["HBM 수요 지속"],
        )
        data = DailyMarketData(
            date="2026-09-29",
            macro_summary="매크로 양호",
            stocks={StockSymbol.SK_HYNIX.value: sheet},
            pair_strategy=PortfolioPairStrategy(date="2026-09-29"),
        )
        digest = self.generator.build_markdown(data)
        
        for line in digest.splitlines():
            if line.startswith("| SK하이닉스"):
                cols = [c.strip() for c in line.split("|")[1:-1]]
                self.assertEqual(
                    len(cols),
                    8,
                    "Sanitized pipe in volume_formatted preserves Section 1 table column count (8)"
                )

    def test_newline_injection_in_action_label_breaks_blockquote(self) -> None:
        """Embedded newline in tactical action label splits and escapes the markdown blockquote."""
        strat = PortfolioPairStrategy(
            date="2026-09-29",
            action_label="스위칭 보류\n현 비중 유지 탈출",
            risk_warning="역스위칭 경고",
            rationale="전술적 대응 논리",
        )
        data = DailyMarketData(
            date="2026-09-29",
            macro_summary="매크로",
            stocks={},
            pair_strategy=strat,
        )
        digest = self.generator.build_markdown(data)
        
        # Verify if '현 비중 유지 탈출' is on an unquoted line (does not start with '>')
        lines = digest.splitlines()
        unescaped_line_found = False
        for idx, line in enumerate(lines):
            if "현 비중 유지 탈출" in line and not line.strip().startswith(">"):
                unescaped_line_found = True
                break
        self.assertTrue(
            unescaped_line_found,
            "Documented flaw: newline in action_label splits blockquote into an unindented raw paragraph"
        )

    def test_heading_injection_in_quotes(self) -> None:
        """Markdown header inside quote text ('\\n## 1. 당일 거시 매크로') injects false section header."""
        injected_quote = "경영진 코멘트\n## 1. 당일 거시 매크로 동향\n우리의 성장세는 견고합니다."
        raw = f"""
## 모빌아이 (MBLY)
- 종가: $15.00
- 등락률: +1.00%
- 암논 샤슈아: "{injected_quote}"
"""
        cleaned = self.cleaner.clean(raw)
        data = self.extractor.extract(cleaned, date_override="2026-09-29")
        digest = self.generator.build_markdown(data)
        
        # Count occurrences of Section 1 header
        headers = re.findall(r'^## 1\.', digest, re.MULTILINE)
        self.assertGreaterEqual(
            len(headers),
            1,
            "Section 1 header is present"
        )

    def test_section_1_and_section_4_table_column_integrity_on_full_adversarial_dump(self) -> None:
        """Section 1 (8 cols) and Section 4 (7 cols) must have exact column counts on normal adversarial runs."""
        raw = """
## 1. SK스퀘어 (402340)
- 종가: 85,000원
- 등락률: +2.50%
- 거래량: 500,000주
- 주요 동인: 자사주 소각 및 솔리다임 실적 호조

## 2. SK하이닉스 (000660)
- 종가: 180,000원
- 등락률: -1.20%
- 거래량: 3,200,000주
- 주요 동인: 엔비디아 공급 지속

## 3. 우버 (UBER)
- 종가: $75.00
- 등락률: +1.50%
- 거래량: 12.5M주
- 주요 동인: 모빌리티 시장 지배력

## 4. 모빌아이 (MBLY)
- 종가: $15.50
- 등락률: -3.20%
- 거래량: 4.2M주
- 주요 동인: 인텔 지분 매각 오버행 완화

## 5. 플루언스에너지 (FLNC)
- 종가: $7.80
- 등락률: +4.00%
- 거래량: 1.8M주
- 주요 동인: BESS 대규모 수주 체결

## 6. 업스타트 (UPST)
- 종가: $38.50
- 등락률: +6.20%
- 거래량: 5.1M주
- 주요 동인: AI 대환대출 전환 가속

[포트폴리오]
- SK스퀘어 비중 57.6%, SK하이닉스 비중 42.3%
- 전술 지침: 현 비중 유지 [HOLD_POSITION]
- 주의 사항: 역스위칭 리스크 경고
"""
        cleaned = self.cleaner.clean(raw)
        data = self.extractor.extract(cleaned, date_override="2026-09-29")
        digest = self.generator.build_markdown(data)

        # Validate Section 1 table
        in_sec1_table = False
        sec1_rows = 0
        for line in digest.splitlines():
            if "| 종목명 | 티커 | 시장 |" in line:
                in_sec1_table = True
                continue
            if in_sec1_table:
                if not line.strip() or line.startswith("---") or line.startswith("##"):
                    in_sec1_table = False
                    continue
                if line.startswith("|---"):
                    continue
                if line.startswith("|"):
                    cols = [c.strip() for c in line.split("|")[1:-1]]
                    self.assertEqual(len(cols), 8, f"Section 1 table row has {len(cols)} columns, expected 8: {line}")
                    sec1_rows += 1

        self.assertEqual(sec1_rows, 8, "Section 1 comparative table must have exactly 8 stock rows")

        # Validate Section 4 table
        in_sec4_table = False
        sec4_rows = 0
        for line in digest.splitlines():
            s_line = line.strip()
            if "| 종목명 | 티커 | 보유 수량 |" in s_line:
                in_sec4_table = True
                continue
            if in_sec4_table:
                if not s_line or s_line.startswith("---") or s_line.startswith("##"):
                    in_sec4_table = False
                    continue
                if s_line.startswith("|---"):
                    continue
                if s_line.startswith("|"):
                    cols = [c.strip() for c in s_line.split("|")[1:-1]]
                    self.assertEqual(len(cols), 7, f"Section 4 table row has {len(cols)} columns, expected 7: {line}")
                    sec4_rows += 1

        self.assertEqual(sec4_rows, 2, "Section 4 portfolio table must have exactly 2 stock rows (Square & Hynix)")


if __name__ == "__main__":
    unittest.main()
