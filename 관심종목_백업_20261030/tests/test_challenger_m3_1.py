"""Milestone M3 Gate Adversarial Stress-Testing Suite by Challenger 1.

Target: engine/sync_dashboard.py & data.js integrity

Adversarial Vectors:
1. Malformed / Corrupted data.js (fallback to default template without crashing)
2. 0-Byte Empty and Whitespace-only data.js
3. Idempotent Synchronization (zero duplicate records / digests on repeated runs)
4. In-Place Update on Re-sync (values updated in place for existing date)
5. Partial Stock Dumps (1 stock, 2 stocks, 0 stocks, missing pair stocks)
6. Extreme Inputs & Escaping (quotes, newlines, URLs, U+2028/U+2029, emojis, HTML/XSS payloads)
7. Currency / Metric Nullability Edge Cases
8. Multi-Date Accumulation and Chronological Sorting
"""

import copy
import json
from pathlib import Path
import tempfile
import unittest

from engine.models import (
    DailyMarketData,
    ExecutiveInterviewFact,
    IBReportFact,
    MarketMetrics,
    PortfolioPairStrategy,
    StockFactSheet,
    StockSymbol,
)
import engine.sync_dashboard as sync_module
from tests.test_dashboard import parse_js_data_store


def create_minimal_market_data(
    date: str = "2026-09-29",
    stocks: dict = None,
    pair_strategy: PortfolioPairStrategy = None,
    macro_summary: str = "글로벌 매크로 요약 테스트",
) -> DailyMarketData:
    """Helper to assemble a clean DailyMarketData fixture."""
    if stocks is None:
        stocks = {
            "SK_HYNIX": StockFactSheet(
                stock_id="SK_HYNIX",
                stock_name="SK하이닉스",
                name_kr="SK하이닉스",
                name_en="SK Hynix Inc.",
                ticker="000660",
                market="KRX",
                category="메모리/HBM",
                badge_color="indigo",
                metrics=MarketMetrics(
                    stock_id="SK_HYNIX",
                    date=date,
                    currency="KRW",
                    close_price=175000.0,
                    change_percent=-2.5,
                    volume=3500000,
                ),
                core_drivers=["HBM 공급 과잉 우려는 과도하며 4분기 실적 호조 전망"],
                raw_summary="SK하이닉스 마감 시황 요약",
            ),
            "SK_SQUARE": StockFactSheet(
                stock_id="SK_SQUARE",
                stock_name="SK스퀘어",
                name_kr="SK스퀘어",
                name_en="SK Square Co., Ltd.",
                ticker="402340",
                market="KRX",
                category="지주/반도체",
                badge_color="blue",
                metrics=MarketMetrics(
                    stock_id="SK_SQUARE",
                    date=date,
                    currency="KRW",
                    close_price=82000.0,
                    change_percent=-1.2,
                    volume=850000,
                ),
                core_drivers=["솔리다임 지분가치 부각 및 NAV 할인율 68% 도달"],
                raw_summary="SK스퀘어 마감 시황 요약",
            ),
        }

    if pair_strategy is None:
        pair_strategy = PortfolioPairStrategy(
            sk_square_weight=57.6,
            sk_hynix_weight=42.3,
            relative_spread="스퀘어(57.6%) : 하이닉스(42.3%)",
            tactical_action="HOLD_POSITION",
            action_label="현 비중 유지",
            risk_warning="역스위칭 리스크 경고",
            rationale="현재 비중 유지 유효.",
        )

    return DailyMarketData(
        date=date,
        macro_summary=macro_summary,
        stocks=stocks,
        pair_strategy=pair_strategy,
    )


class TestAdversarialDataJsCorruption(unittest.TestCase):
    """Stress tests handling of corrupted, malformed, and truncated data.js files."""

    def test_corrupted_json_syntax_falls_back_cleanly(self):
        """When data.js has broken syntax, load_data_store must NOT crash and return default."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            bad_file = Path(tmp_dir) / "data.js"
            bad_file.write_text("window.WATCHLIST_DATA = { invalid json : [ unmatched },;\n", encoding="utf-8")

            # Must not raise exception
            store = sync_module.load_data_store(bad_file)
            self.assertIsInstance(store, dict)
            self.assertIn("portfolio", store)
            self.assertIn("stocks", store)
            self.assertIn("records", store)
            self.assertIn("dailyDigests", store)

            # Syncing to this file should overwrite with valid syntax
            md = create_minimal_market_data()
            ok = sync_module.sync_to_dashboard(md, data_js_path=str(bad_file))
            self.assertTrue(ok)

            # Verify saved file is parseable
            saved_content = bad_file.read_text(encoding="utf-8")
            re_parsed = parse_js_data_store(saved_content)
            self.assertIn("records", re_parsed)
            self.assertGreater(len(re_parsed["records"]), 0)

    def test_missing_watchlist_data_identifier(self):
        """When file does not contain WATCHLIST_DATA, fall back gracefully."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            bad_file = Path(tmp_dir) / "data.js"
            bad_file.write_text("const someOtherVariable = 12345;\nconsole.log('hello');", encoding="utf-8")

            store = sync_module.load_data_store(bad_file)
            self.assertIsInstance(store, dict)
            self.assertIn("stocks", store)

    def test_unmatched_braces_in_data_js(self):
        """When file has unclosed opening brace, fall back gracefully."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            bad_file = Path(tmp_dir) / "data.js"
            bad_file.write_text("window.WATCHLIST_DATA = { 'lastUpdated': '2026-09-29'", encoding="utf-8")

            store = sync_module.load_data_store(bad_file)
            self.assertIsInstance(store, dict)
            self.assertIn("portfolio", store)

    def test_partial_schema_keys_patched(self):
        """When data.js is valid JSON but missing portfolio or dailyDigests, patch them."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            partial_file = Path(tmp_dir) / "data.js"
            partial_file.write_text("window.WATCHLIST_DATA = { 'records': [] };\n", encoding="utf-8")

            store = sync_module.load_data_store(partial_file)
            self.assertIn("portfolio", store)
            self.assertIn("stocks", store)
            self.assertIn("dailyDigests", store)
            self.assertEqual(store["records"], [])


class TestAdversarialEmptyDataJs(unittest.TestCase):
    """Stress tests 0-byte, whitespace-only, and non-existent files."""

    def test_zero_byte_file(self):
        """0-byte file must initialize default template without error."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            empty_file = Path(tmp_dir) / "data.js"
            empty_file.write_bytes(b"")
            self.assertEqual(empty_file.stat().st_size, 0)

            store = sync_module.load_data_store(empty_file)
            self.assertIsInstance(store, dict)
            self.assertIn("stocks", store)
            self.assertEqual(len(store["records"]), 0)

            # Sync to 0-byte file
            md = create_minimal_market_data()
            ok = sync_module.sync_to_dashboard(md, data_js_path=str(empty_file))
            self.assertTrue(ok)
            self.assertGreater(empty_file.stat().st_size, 0)

            # Re-read
            parsed = parse_js_data_store(empty_file.read_text(encoding="utf-8"))
            self.assertEqual(len(parsed["records"]), 3)  # 2 stock close + 1 strategy

    def test_whitespace_only_file(self):
        """File containing only whitespace characters must initialize default template."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            ws_file = Path(tmp_dir) / "data.js"
            ws_file.write_text("   \n\t\r\n   ", encoding="utf-8")

            store = sync_module.load_data_store(ws_file)
            self.assertIsInstance(store, dict)
            self.assertIn("portfolio", store)

    def test_non_existent_file(self):
        """Non-existent file must initialize default template."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            non_file = Path(tmp_dir) / "nested" / "dir" / "data.js"
            self.assertFalse(non_file.exists())

            store = sync_module.load_data_store(non_file)
            self.assertIsInstance(store, dict)
            self.assertIn("portfolio", store)

            md = create_minimal_market_data()
            ok = sync_module.sync_to_dashboard(md, data_js_path=str(non_file))
            self.assertTrue(ok)
            self.assertTrue(non_file.exists())


class TestAdversarialIdempotency(unittest.TestCase):
    """Stress tests idempotency: repeated syncs on the same date must not create duplicate records."""

    def test_exact_duplicate_sync_does_not_multiply_records(self):
        """Running sync twice with the exact same DailyMarketData must NOT duplicate records."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            target_file = Path(tmp_dir) / "data.js"
            md = create_minimal_market_data(date="2026-09-29")

            # Run 1
            sync_module.sync_to_dashboard(md, digest_md="# Digest Day 1", data_js_path=str(target_file))
            data1 = parse_js_data_store(target_file.read_text(encoding="utf-8"))
            num_records_1 = len(data1["records"])
            num_digests_1 = len(data1["dailyDigests"])

            self.assertGreater(num_records_1, 0)
            self.assertEqual(num_digests_1, 1)

            # Run 2 (Identical input and date)
            sync_module.sync_to_dashboard(md, digest_md="# Digest Day 1 (re-synced)", data_js_path=str(target_file))
            data2 = parse_js_data_store(target_file.read_text(encoding="utf-8"))
            num_records_2 = len(data2["records"])
            num_digests_2 = len(data2["dailyDigests"])

            # Must have EXACT same number of records and digests
            self.assertEqual(num_records_1, num_records_2, "Idempotency violation: records count changed on duplicate sync!")
            self.assertEqual(num_digests_1, num_digests_2, "Idempotency violation: dailyDigests count changed on duplicate sync!")
            self.assertEqual(data2["dailyDigests"][0]["markdownReport"], "# Digest Day 1 (re-synced)")

    def test_resync_updates_values_in_place(self):
        """When resyncing the same date with updated metrics, values must update in-place."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            target_file = Path(tmp_dir) / "data.js"
            md1 = create_minimal_market_data(date="2026-09-29")
            sync_module.sync_to_dashboard(md1, data_js_path=str(target_file))

            # Modify prices for the same date
            md2 = create_minimal_market_data(date="2026-09-29")
            md2.stocks["SK_HYNIX"].metrics.close_price = 182000.0
            md2.stocks["SK_HYNIX"].metrics.close_price_formatted = "182,000원"
            md2.stocks["SK_HYNIX"].metrics.change_percent = +4.5
            md2.stocks["SK_HYNIX"].metrics.change_percent_formatted = "+4.50%"

            sync_module.sync_to_dashboard(md2, data_js_path=str(target_file))
            data = parse_js_data_store(target_file.read_text(encoding="utf-8"))

            hynix_recs = [r for r in data["records"] if r["stockId"] == "SK_HYNIX" and r["type"] == "DAILY_CLOSE"]
            self.assertEqual(len(hynix_recs), 1, "Expected exactly 1 in-place updated record for SK_HYNIX close")
            self.assertEqual(hynix_recs[0]["metrics"]["price"], "182,000원")
            self.assertEqual(hynix_recs[0]["metrics"]["change"], "+4.50%")

    def test_multi_date_accumulation(self):
        """Syncing two distinct dates should accumulate records and digests cleanly."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            target_file = Path(tmp_dir) / "data.js"
            md_day1 = create_minimal_market_data(date="2026-09-28")
            md_day2 = create_minimal_market_data(date="2026-09-29")

            sync_module.sync_to_dashboard(md_day1, digest_md="Day 1", data_js_path=str(target_file))
            sync_module.sync_to_dashboard(md_day2, digest_md="Day 2", data_js_path=str(target_file))

            data = parse_js_data_store(target_file.read_text(encoding="utf-8"))
            self.assertEqual(len(data["dailyDigests"]), 2)
            digest_dates = [d["date"] for d in data["dailyDigests"]]
            self.assertIn("2026-09-28", digest_dates)
            self.assertIn("2026-09-29", digest_dates)


class TestAdversarialPartialStockDumps(unittest.TestCase):
    """Stress tests syncing when only a subset of the 6 stocks are present."""

    def test_single_stock_only(self):
        """When only 1 stock is provided in market_data, sync must succeed."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            target_file = Path(tmp_dir) / "data.js"
            single_stock_data = DailyMarketData(
                date="2026-09-29",
                macro_summary="단일 종목 시황",
                stocks={
                    "UBER": StockFactSheet(
                        stock_id="UBER",
                        stock_name="우버",
                        name_kr="우버",
                        name_en="Uber Technologies, Inc.",
                        ticker="UBER",
                        market="NYSE",
                        category="모빌리티/플랫폼",
                        badge_color="emerald",
                        metrics=MarketMetrics(
                            stock_id="UBER",
                            currency="USD",
                            close_price=78.5,
                            change_percent=1.8,
                            volume=12000000,
                        ),
                        core_drivers=["자율주행 파트너십 확장 및 모빌리티 수요 견조"],
                    )
                },
                pair_strategy=None,
            )

            ok = sync_module.sync_to_dashboard(single_stock_data, data_js_path=str(target_file))
            self.assertTrue(ok)

            data = parse_js_data_store(target_file.read_text(encoding="utf-8"))
            # Global stock metadata must still retain all 6 stocks
            self.assertGreaterEqual(len(data["stocks"]), 6)
            # Records should contain only the 1 UBER record
            self.assertEqual(len(data["records"]), 1)
            self.assertEqual(data["records"][0]["stockId"], "UBER")
            # summaryTable in dailyDigests should have 1 row
            self.assertEqual(len(data["dailyDigests"][0]["summaryTable"]), 1)
            self.assertEqual(data["dailyDigests"][0]["summaryTable"][0]["stockId"], "UBER")

    def test_empty_stocks_dict(self):
        """When market_data has 0 stocks, sync must not crash."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            target_file = Path(tmp_dir) / "data.js"
            empty_stock_data = DailyMarketData(
                date="2026-09-29",
                macro_summary="휴장일 매크로 요약",
                stocks={},
                pair_strategy=None,
            )

            ok = sync_module.sync_to_dashboard(empty_stock_data, data_js_path=str(target_file))
            self.assertTrue(ok)

            data = parse_js_data_store(target_file.read_text(encoding="utf-8"))
            self.assertEqual(len(data["records"]), 0)
            self.assertEqual(len(data["dailyDigests"]), 1)
            self.assertEqual(data["dailyDigests"][0]["summaryTable"], [])

    def test_missing_pair_strategy(self):
        """When pair_strategy is None, strategy records are omitted and safe defaults are used."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            target_file = Path(tmp_dir) / "data.js"
            data_no_strat = create_minimal_market_data(date="2026-09-29")
            data_no_strat.pair_strategy = None

            ok = sync_module.sync_to_dashboard(data_no_strat, data_js_path=str(target_file))
            self.assertTrue(ok)

            data = parse_js_data_store(target_file.read_text(encoding="utf-8"))
            strategy_recs = [r for r in data["records"] if r["type"] == "STRATEGY"]
            self.assertEqual(len(strategy_recs), 0)
            self.assertIn("portfolioGuidance", data["dailyDigests"][0])


class TestAdversarialExtremeInputsAndEscaping(unittest.TestCase):
    """Stress tests weird quotes, newlines, URLs, U+2028/U+2029, and XSS payloads in strings."""

    def test_quotes_newlines_and_urls_in_driver(self):
        """Double quotes, single quotes, newlines, and URLs must be properly escaped."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            target_file = Path(tmp_dir) / "data.js"

            extreme_driver = (
                "CEO \"Julian Nebreda\" said: 'We are expanding BESS 400MWh!'\n"
                "Check out: https://youtu.be/test_url?param=1&foo=bar//subpath\n"
                "Warning // do not truncate this line!\n"
                "Backslash \\ and backtick `escaped` safely."
            )

            md = DailyMarketData(
                date="2026-09-29",
                macro_summary="매크로 \"특수문자\" '테스트' & <script>alert('x')</script>",
                stocks={
                    "FLNC": StockFactSheet(
                        stock_id="FLNC",
                        stock_name="플루언스에너지",
                        name_kr="플루언스에너지",
                        name_en="Fluence Energy, Inc.",
                        ticker="FLNC",
                        market="NASDAQ",
                        category="AI 전력/BESS",
                        badge_color="teal",
                        metrics=MarketMetrics(
                            stock_id="FLNC",
                            currency="USD",
                            close_price=22.5,
                            change_percent=-3.1,
                            volume=500000,
                        ),
                        core_drivers=[extreme_driver],
                        raw_summary="플루언스 요약\n줄바꿈 테스트\r\n다음 줄",
                        interviews=[
                            ExecutiveInterviewFact(
                                stock_id="FLNC",
                                date="2026-09-29",
                                speaker_name="Julian Nebreda",
                                core_quotes=["\"Quote inside quote\"", "Another 'quote'"],
                                context_trajectory="Trajectory with URL https://reuters.com/fluence//article",
                                source_url="https://youtu.be/xyz123",
                            )
                        ],
                    )
                },
                pair_strategy=None,
            )

            ok = sync_module.sync_to_dashboard(md, data_js_path=str(target_file))
            self.assertTrue(ok)

            # Must parse cleanly via test harness regex parser
            raw_text = target_file.read_text(encoding="utf-8")
            data = parse_js_data_store(raw_text)

            flnc_close = next(r for r in data["records"] if r["stockId"] == "FLNC" and r["type"] == "DAILY_CLOSE")
            self.assertIn("Julian Nebreda", flnc_close["summary"])
            self.assertIn("https://youtu.be", flnc_close["summary"])
            self.assertIn("Warning // do not truncate this line!", flnc_close["summary"])

    def test_ecmascript_line_paragraph_separators_u2028_u2029(self):
        """U+2028 and U+2029 can break JavaScript evaluation if unescaped."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            target_file = Path(tmp_dir) / "data.js"

            text_with_separators = "Line1\u2028Line2\u2029Line3"
            md = DailyMarketData(
                date="2026-09-29",
                macro_summary=text_with_separators,
                stocks={
                    "UBER": StockFactSheet(
                        stock_id="UBER",
                        stock_name="우버",
                        name_kr="우버",
                        name_en="Uber",
                        ticker="UBER",
                        market="NYSE",
                        category="모빌리티",
                        badge_color="emerald",
                        metrics=MarketMetrics(stock_id="UBER", currency="USD", close_price=80.0, change_percent=1.0, volume=1000),
                        core_drivers=[text_with_separators],
                    )
                },
                pair_strategy=None,
            )

            ok = sync_module.sync_to_dashboard(md, data_js_path=str(target_file))
            self.assertTrue(ok)

            raw_text = target_file.read_text(encoding="utf-8")
            # In raw JS text, literal \u2028 and \u2029 should be escaped as \\u2028 and \\u2029
            self.assertNotIn("\u2028", raw_text)
            self.assertNotIn("\u2029", raw_text)

            # Parsing should recover the text
            data = parse_js_data_store(raw_text)
            self.assertEqual(data["dailyDigests"][0]["macroSummary"], text_with_separators)

    def test_extreme_length_driver(self):
        """Very long driver strings (10,000+ characters) must not cause buffer or regex issues."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            target_file = Path(tmp_dir) / "data.js"
            huge_driver = "반도체 수급 사이클 분석 " * 500  # ~6,500 chars

            md = create_minimal_market_data()
            md.stocks["SK_HYNIX"].core_drivers = [huge_driver]

            ok = sync_module.sync_to_dashboard(md, data_js_path=str(target_file))
            self.assertTrue(ok)

            data = parse_js_data_store(target_file.read_text(encoding="utf-8"))
            hynix_close = next(r for r in data["records"] if r["stockId"] == "SK_HYNIX" and r["type"] == "DAILY_CLOSE")
            self.assertIn("반도체 수급 사이클 분석", hynix_close["summary"])


class TestAdversarialMetricsNullability(unittest.TestCase):
    """Stress tests boundary and null metric values in StockFactSheet and MarketMetrics."""

    def test_null_and_extreme_metrics(self):
        """None, 0, negative prices and extreme percentages must format without exceptions."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            target_file = Path(tmp_dir) / "data.js"

            test_cases = [
                ("SK_HYNIX", "KRW", None, None, None),
                ("SK_SQUARE", "KRW", 0.0, 0.0, 0),
                ("UBER", "USD", -10.5, -99.99, 100_000_000_000),
                ("MBLY", "USD", 5000.25, 1500.0, None),
                ("FLNC", "", 25.0, 1.5, 50000),
            ]

            stocks_dict = {}
            for sid, curr, price, pct, vol in test_cases:
                stocks_dict[sid] = StockFactSheet(
                    stock_id=sid,
                    stock_name=sid,
                    name_kr=sid,
                    name_en=sid,
                    ticker=sid,
                    market="NASDAQ" if curr == "USD" else "KRX",
                    category="테스트",
                    badge_color="blue",
                    metrics=MarketMetrics(
                        stock_id=sid,
                        currency=curr,
                        close_price=price,
                        change_percent=pct,
                        volume=vol,
                    ),
                    core_drivers=["극단값 테스트 동인"],
                )

            md = DailyMarketData(
                date="2026-09-29",
                macro_summary="극단값 매트릭스 테스트",
                stocks=stocks_dict,
                pair_strategy=None,
            )

            ok = sync_module.sync_to_dashboard(md, data_js_path=str(target_file))
            self.assertTrue(ok)

            data = parse_js_data_store(target_file.read_text(encoding="utf-8"))
            self.assertEqual(len(data["records"]), 5)


class TestAdversarialCliSyncIntegration(unittest.TestCase):
    """Stress tests unified CLI entrypoint for 'sync' subcommand."""

    def test_cli_sync_pipeline_execution(self):
        """CLI sync subcommand executes cleaner -> extractor -> digest -> sync_dashboard."""
        import sys
        from unittest.mock import patch
        from engine.cli import main
        from tests.fixtures.sample_dumps import SAMPLE_RAW_DUMP_FULL_DAY

        with tempfile.TemporaryDirectory() as tmp_dir:
            input_file = Path(tmp_dir) / "raw_dump.txt"
            input_file.write_text(SAMPLE_RAW_DUMP_FULL_DAY, encoding="utf-8")

            out_digest_dir = Path(tmp_dir) / "daily_digest"
            out_data_js = Path(tmp_dir) / "data.js"

            cli_args = [
                "sync",
                "-i", str(input_file),
                "-d", "2026-09-29",
                "--digest-dir", str(out_digest_dir),
                "--data-js", str(out_data_js),
                "--quiet",
            ]

            exit_code = main(cli_args)
            self.assertEqual(exit_code, 0, "CLI sync subcommand exited with non-zero code!")

            # Verify digest file created
            expected_digest_file = out_digest_dir / "2026-09-29_digest.md"
            self.assertTrue(expected_digest_file.exists(), f"Expected digest file not created: {expected_digest_file}")

            # Verify data.js created and valid
            self.assertTrue(out_data_js.exists(), f"Expected data.js not created: {out_data_js}")
            data = parse_js_data_store(out_data_js.read_text(encoding="utf-8"))
            self.assertIn("records", data)
            self.assertGreaterEqual(len(data["records"]), 6)
            self.assertEqual(len(data["dailyDigests"]), 1)


if __name__ == "__main__":
    unittest.main()

