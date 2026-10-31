"""Tier 5 White-box Adversarial Coverage Hardening Test Suite for Dashboard & Sync.

Target Modules:
- engine/sync_dashboard.py
- engine/cli.py
- index.html
- data.js

Adversarial Vectors:
1. Malformed data.js formats (truncated JSON, corrupted comments, illegal tokens, non-dict payloads, missing keys).
2. Massive sequential sync stress (syncing 30 consecutive simulated trading days).
3. Duplicate record resilience (repeated idempotent ingestion, interleaved resyncs, partial-to-full intraday upgrades).
4. 100% offline isolation checks on index.html (zero remote URI schemas, zero CDNs, zero @import, zero remote CSS urls).
5. Browser DOM safety for index.html (balanced script brackets/quotes, DOM ID integrity, event handler resolution, Node syntax check).
6. CLI adversarial stress (empty inputs, consecutive invocations, robust error codes).
"""

from __future__ import annotations

import copy
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile
from typing import Any, Dict, List, Optional
import unittest

ROOT_DIR = Path(__file__).resolve().parent.parent
INDEX_HTML_PATH = ROOT_DIR / "index.html"
DATA_JS_PATH = ROOT_DIR / "data.js"

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
import engine.cli as cli_module
from tests.test_dashboard import parse_js_data_store


def create_adversarial_market_data(
    date: str,
    day_offset: int = 0,
    stocks_subset: Optional[List[str]] = None,
) -> DailyMarketData:
    """Generates realistic varying DailyMarketData for simulated sequential trading days."""
    canonical_stocks = {
        "SK_SQUARE": {
            "name": "SK스퀘어",
            "ticker": "402340",
            "market": "KRX",
            "base_price": 82000.0,
            "currency": "KRW",
            "delta": (-1.5 + (day_offset % 7) * 0.6),
            "vol": 800000 + day_offset * 12500,
            "driver": f"솔리다임 지분가치 및 자사주 소각 추진 모멘텀 (Day {day_offset})",
            "category": "지주/반도체",
        },
        "SK_HYNIX": {
            "name": "SK하이닉스",
            "ticker": "000660 / SKHY",
            "market": "KRX / NASDAQ",
            "base_price": 178000.0,
            "currency": "KRW",
            "delta": (-2.0 + (day_offset % 5) * 1.1),
            "vol": 3200000 + day_offset * 35000,
            "driver": f"HBM3E 12단 양산 출하 확대 및 글로벌 빅테크 공급 계약 (Day {day_offset})",
            "category": "메모리/HBM",
        },
        "UBER": {
            "name": "우버",
            "ticker": "UBER",
            "market": "NYSE",
            "base_price": 72.0,
            "currency": "USD",
            "delta": (0.8 - (day_offset % 4) * 0.5),
            "vol": 15000000 + day_offset * 50000,
            "driver": f"로보택시 파트너십 확장 및 배달 EBITDA 마진 개선 (Day {day_offset})",
            "category": "모빌리티/플랫폼",
        },
        "MBLY": {
            "name": "모빌아이",
            "ticker": "MBLY",
            "market": "NASDAQ",
            "base_price": 12.5,
            "currency": "USD",
            "delta": (-1.0 + (day_offset % 6) * 0.4),
            "vol": 4500000 + day_offset * 18000,
            "driver": f"EyeQ6 미드 티어 양산 수주 및 OEM 탑재 라인업 확대 (Day {day_offset})",
            "category": "자율주행/ADAS",
        },
        "FLNC": {
            "name": "플루언스에너지",
            "ticker": "FLNC",
            "market": "NASDAQ",
            "base_price": 9.2,
            "currency": "USD",
            "delta": (1.2 - (day_offset % 3) * 0.9),
            "vol": 2100000 + day_offset * 10000,
            "driver": f"BESS 대규모 수주 및 IRA 국내생산 보조금 가시화 (Day {day_offset})",
            "category": "AI 전력/BESS",
        },
        "UPST": {
            "name": "업스타트홀딩스",
            "ticker": "UPST",
            "market": "NASDAQ",
            "base_price": 24.0,
            "currency": "USD",
            "delta": (-2.5 + (day_offset % 8) * 0.8),
            "vol": 5800000 + day_offset * 25000,
            "driver": f"사모신용 유동화 완료 및 T-모바일 제휴 대출 공급 개시 (Day {day_offset})",
            "category": "AI 핀테크/대출",
        },
    }

    selected_keys = stocks_subset if stocks_subset is not None else list(canonical_stocks.keys())
    stocks_dict: Dict[str, StockFactSheet] = {}

    for sid in selected_keys:
        info = canonical_stocks[sid]
        price = max(1.0, info["base_price"] * (1.0 + info["delta"] / 100.0))
        stocks_dict[sid] = StockFactSheet(
            stock_id=sid,
            stock_name=info["name"],
            name_kr=info["name"],
            name_en=sid,
            ticker=info["ticker"],
            market=info["market"],
            category=info["category"],
            badge_color="blue",
            metrics=MarketMetrics(
                stock_id=sid,
                date=date,
                currency=info["currency"],
                close_price=round(price, 2),
                change_percent=round(info["delta"], 2),
                volume=info["vol"],
            ),
            core_drivers=[info["driver"]],
            raw_summary=f"{info['name']} {date} 장마감 시황 요약",
            interviews=[
                ExecutiveInterviewFact(
                    stock_id=sid,
                    date=date,
                    speaker_name=f"{info['name']} 대표이사",
                    core_quotes=[f"{info['name']}의 핵심 경쟁력은 독보적 기술력과 시장 지배력입니다."],
                    context_trajectory=f"이전 분기 발언 대비 실행 속도 가속화 확인 (Day {day_offset}).",
                    investment_takeaway="중장기 해자 유지 유효.",
                )
            ] if (day_offset % 2 == 0 and sid in ["SK_HYNIX", "UBER"]) else [],
            ib_comments=[
                IBReportFact(
                    stock_id=sid,
                    date=date,
                    brokerage="골드만삭스" if day_offset % 2 == 0 else "모건스탠리",
                    rating_current="BUY",
                    target_price_current=f"{round(price * 1.25, 2)}",
                    target_price_currency=info["currency"],
                    key_thesis=f"글로벌 AI 밸류체인 핵심 수혜 및 실적 상향 여력 충분 (Day {day_offset}).",
                )
            ] if (day_offset % 3 == 0 and sid in ["SK_SQUARE", "FLNC"]) else [],
        )

    sq_weight = round(57.6 + (day_offset % 5) * 0.2 - 0.4, 1)
    hy_weight = round(100.0 - sq_weight, 1)

    pair_strategy = PortfolioPairStrategy(
        sk_square_weight=sq_weight,
        sk_hynix_weight=hy_weight,
        relative_spread=f"스퀘어({sq_weight:.1f}%) : 하이닉스({hy_weight:.1f}%)",
        tactical_action="HOLD_POSITION" if day_offset % 4 != 0 else "PARTIAL_REBALANCE",
        action_label="현 비중 유지" if day_offset % 4 != 0 else "비중 미세 조정",
        risk_warning="역스위칭 리스크 경고",
        rationale=f"스프레드 괴리 점검 결과 현재 비중 유지 권고 (Day {day_offset}).",
    )

    return DailyMarketData(
        date=date,
        macro_summary=f"글로벌 매크로 요약 (Day {day_offset}): 금리 및 AI 인프라 수급 변동성 모니터링.",
        stocks=stocks_dict,
        pair_strategy=pair_strategy,
    )


class TestTier5MalformedDataJs(unittest.TestCase):
    """Tier 5 Adversarial: Malformed data.js formats, corrupted comments, and recovery."""

    def test_truncated_json_mid_string_recovers_gracefully(self) -> None:
        """When data.js is truncated midway through a string or array, load must not crash."""
        with tempfile.TemporaryDirectory(ignore_cleanup_errors=True) as tmp_dir:
            truncated_file = Path(tmp_dir) / "data.js"
            truncated_file.write_text(
                'window.WATCHLIST_DATA = {\n  "lastUpdated": "2026-09-29",\n  "records": [\n    {"id": "REC-20260929-SK_HYNIX", "title": "SK하이닉스 장마감',
                encoding="utf-8",
            )

            # load_data_store must catch syntax error and return default template without raising
            data = sync_module.load_data_store(truncated_file)
            self.assertIsInstance(data, dict)
            self.assertIn("portfolio", data)
            self.assertIn("stocks", data)
            self.assertIn("records", data)
            self.assertIn("dailyDigests", data)

            # Syncing must repair the file and save valid JS
            md = create_adversarial_market_data("2026-09-29")
            ok = sync_module.sync_to_dashboard(md, data_js_path=str(truncated_file))
            self.assertTrue(ok)

            re_parsed = parse_js_data_store(truncated_file.read_text(encoding="utf-8"))
            self.assertEqual(len(re_parsed["records"]), 11)  # 6 stocks + 2 interviews + 2 IB + 1 strategy
            self.assertEqual(len(re_parsed["dailyDigests"]), 1)

    def test_corrupted_comments_varieties(self) -> None:
        """Unclosed block comments, special chars in comments, and comments at EOF."""
        with tempfile.TemporaryDirectory(ignore_cleanup_errors=True) as tmp_dir:
            corrupted_file_a = Path(tmp_dir) / "data_a.js"

            # Case A: Unclosed block comment
            corrupted_file_a.write_text(
                "/* Unclosed block comment at the top\nwindow.WATCHLIST_DATA = {\"records\": []};\n",
                encoding="utf-8",
            )
            data_a = sync_module.load_data_store(corrupted_file_a)
            self.assertIsInstance(data_a, dict)

            # Case B: Line comment containing braces, quotes, and regex-confusing tokens
            corrupted_file_b = Path(tmp_dir) / "data_b.js"
            comment_with_braces = (
                "// Comment containing { \"unclosed_brace\": true, 'quotes': [1,2,3] }\n"
                "window.WATCHLIST_DATA = {\n"
                "  // another line comment with http://example.com/api//test\n"
                '  "records": [],\n'
                '  "dailyDigests": []\n'
                "}; // trailing comment without newline"
            )
            corrupted_file_b.write_text(comment_with_braces, encoding="utf-8")
            data_b = sync_module.load_data_store(corrupted_file_b)
            self.assertIsInstance(data_b, dict)
            self.assertIn("records", data_b)

    def test_illegal_tokens_and_non_dict_payloads(self) -> None:
        """Illegal JS tokens (e.g. %%%, null, array, string) must default cleanly."""
        with tempfile.TemporaryDirectory(ignore_cleanup_errors=True) as tmp_dir:
            bad_file = Path(tmp_dir) / "data.js"

            bad_payloads = [
                "window.WATCHLIST_DATA = { %%% !@#$ illegal tokens };\n",
                "window.WATCHLIST_DATA = 'I am a string, not an object';\n",
                "window.WATCHLIST_DATA = [1, 2, 3, 4, 5];\n",
                "window.WATCHLIST_DATA = 999999;\n",
                "window.WATCHLIST_DATA = null;\n",
                "window.WATCHLIST_DATA = undefined;\n",
                "const OTHER_VAR = { records: [] };\n",
            ]

            for idx, payload in enumerate(bad_payloads):
                f = Path(tmp_dir) / f"data_{idx}.js"
                f.write_text(payload, encoding="utf-8")
                store = sync_module.load_data_store(f)
                self.assertIsInstance(store, dict, f"Failed on payload: {payload}")
                self.assertIn("portfolio", store)
                self.assertIn("stocks", store)
                self.assertIn("records", store)
                self.assertIn("dailyDigests", store)

    def test_missing_nested_schema_keys_patched(self) -> None:
        """When data.js has valid JSON but missing portfolio.holdings or stocks, patch safely."""
        with tempfile.TemporaryDirectory(ignore_cleanup_errors=True) as tmp_dir:
            partial_file = Path(tmp_dir) / "data.js"
            partial_file.write_text(
                'window.WATCHLIST_DATA = {\n  "portfolio": {},\n  "stocks": []\n};\n',
                encoding="utf-8",
            )
            store = sync_module.load_data_store(partial_file)
            self.assertIn("holdings", store["portfolio"])
            self.assertEqual(len(store["stocks"]), len(sync_module.DEFAULT_STOCKS))


class TestTier5MassiveSequentialSync(unittest.TestCase):
    """Tier 5 Adversarial: Ingesting 30 consecutive simulated trading days without corruption."""

    def test_30_consecutive_days_massive_sync(self) -> None:
        """Syncs 30 consecutive simulated days, verifying strict accumulation and valid serialization."""
        with tempfile.TemporaryDirectory(ignore_cleanup_errors=True) as tmp_dir:
            target_data_js = Path(tmp_dir) / "data.js"
            num_days = 30
            base_year, base_month = 2026, 10

            expected_dates = []
            for d in range(1, num_days + 1):
                # Format dates: 2026-10-01 to 2026-10-30
                date_str = f"{base_year}-{base_month:02d}-{d:02d}"
                expected_dates.append(date_str)

                md = create_adversarial_market_data(date=date_str, day_offset=d)
                digest_md = (
                    f"# 일간 6개 관심종목 종합 다이제스트 ({date_str})\n\n"
                    f"## 1. 당일 거시 매크로 (Day {d})\n- Day {d} 종합 브리핑\n"
                )

                ok = sync_module.sync_to_dashboard(
                    md,
                    digest_md=digest_md,
                    data_js_path=str(target_data_js),
                )
                self.assertTrue(ok, f"Failed to sync day {d} ({date_str})")

            # Verify target file exists and has healthy size
            self.assertTrue(target_data_js.exists())
            file_size = target_data_js.stat().st_size
            self.assertGreater(file_size, 50000, "30-day data.js should have substantial size (>50KB)")

            # Parse and verify integrity
            raw_js = target_data_js.read_text(encoding="utf-8")
            parsed = parse_js_data_store(raw_js)

            # 1. Verify exactly 30 daily digests
            digests = parsed["dailyDigests"]
            self.assertEqual(len(digests), num_days, f"Expected {num_days} digests, got {len(digests)}")

            # 2. Verify all 30 dates exist and are unique
            digest_dates = [dg["date"] for dg in digests]
            self.assertEqual(len(set(digest_dates)), num_days, "Digest dates must all be unique")
            for exp_date in expected_dates:
                self.assertIn(exp_date, digest_dates, f"Missing digest date: {exp_date}")

            # 3. Verify digests are indexed with latest first
            self.assertEqual(digests[0]["date"], expected_dates[-1])

            # 4. Verify records accumulation across all 30 days
            records = parsed["records"]
            record_dates = {r["date"] for r in records}
            self.assertEqual(len(record_dates), num_days, "All 30 dates must be represented in records")

            # Check that each day has at least 6 stock records + 1 strategy record = 7 records
            self.assertGreaterEqual(len(records), num_days * 7)

            # 5. Verify NO duplicate record IDs exist anywhere in records
            record_ids = [r["id"] for r in records]
            self.assertEqual(len(record_ids), len(set(record_ids)), "Record IDs must be strictly unique!")

            # 6. Verify portfolio reflects the final day's strategy
            last_day_md = create_adversarial_market_data(date=expected_dates[-1], day_offset=num_days)
            expected_sq_w = last_day_md.pair_strategy.sk_square_weight
            self.assertIn(f"{expected_sq_w:.1f}%", parsed["portfolio"]["targetRatio"])

    def test_rapid_burst_resync_stability(self) -> None:
        """10 rapid back-to-back sync operations in the same thread must not corrupt file."""
        with tempfile.TemporaryDirectory(ignore_cleanup_errors=True) as tmp_dir:
            burst_file = Path(tmp_dir) / "data.js"
            for i in range(10):
                date_str = f"2026-11-{i + 1:02d}"
                md = create_adversarial_market_data(date=date_str, day_offset=i)
                ok = sync_module.sync_to_dashboard(md, data_js_path=str(burst_file))
                self.assertTrue(ok)

            parsed = parse_js_data_store(burst_file.read_text(encoding="utf-8"))
            self.assertEqual(len(parsed["dailyDigests"]), 10)


class TestTier5DuplicateRecordResilience(unittest.TestCase):
    """Tier 5 Adversarial: Duplicate record prevention and idempotent updates."""

    def test_repeated_idempotent_ingestion_single_day(self) -> None:
        """Ingesting the identical day 10 times consecutively must yield exactly 1 day of records."""
        with tempfile.TemporaryDirectory(ignore_cleanup_errors=True) as tmp_dir:
            target_file = Path(tmp_dir) / "data.js"
            md = create_adversarial_market_data("2026-09-29")
            digest_text = "# Digest 2026-09-29"

            initial_record_count: Optional[int] = None
            initial_digest_count: Optional[int] = None

            for iteration in range(10):
                ok = sync_module.sync_to_dashboard(
                    md,
                    digest_md=digest_text,
                    data_js_path=str(target_file),
                )
                self.assertTrue(ok)

                parsed = parse_js_data_store(target_file.read_text(encoding="utf-8"))
                current_recs = len(parsed["records"])
                current_dgs = len(parsed["dailyDigests"])

                if iteration == 0:
                    initial_record_count = current_recs
                    initial_digest_count = current_dgs
                    self.assertGreater(initial_record_count, 0)
                    self.assertEqual(initial_digest_count, 1)
                else:
                    self.assertEqual(
                        current_recs,
                        initial_record_count,
                        f"Record count leaked on iteration {iteration}!",
                    )
                    self.assertEqual(
                        current_dgs,
                        initial_digest_count,
                        f"Digest count leaked on iteration {iteration}!",
                    )

            # Ensure zero duplicate IDs
            parsed_final = parse_js_data_store(target_file.read_text(encoding="utf-8"))
            r_ids = [r["id"] for r in parsed_final["records"]]
            self.assertEqual(len(r_ids), len(set(r_ids)))

    def test_interleaved_multi_day_duplicate_ingestion(self) -> None:
        """Ingesting Day 1, Day 2, Day 3, then re-ingesting with updates preserves exact counts."""
        with tempfile.TemporaryDirectory(ignore_cleanup_errors=True) as tmp_dir:
            target_file = Path(tmp_dir) / "data.js"

            md1 = create_adversarial_market_data("2026-09-28", day_offset=1)
            md2 = create_adversarial_market_data("2026-09-29", day_offset=2)
            md3 = create_adversarial_market_data("2026-09-30", day_offset=3)

            # Initial sequence: 1 -> 2 -> 3
            sync_module.sync_to_dashboard(md1, digest_md="Day 1 v1", data_js_path=str(target_file))
            sync_module.sync_to_dashboard(md2, digest_md="Day 2 v1", data_js_path=str(target_file))
            sync_module.sync_to_dashboard(md3, digest_md="Day 3 v1", data_js_path=str(target_file))

            data_before = parse_js_data_store(target_file.read_text(encoding="utf-8"))
            self.assertEqual(len(data_before["dailyDigests"]), 3)
            count_before = len(data_before["records"])

            # Interleaved re-ingest: Day 2 (revised price) -> Day 1 (unchanged) -> Day 3 (revised)
            md2_revised = copy.deepcopy(md2)
            md2_revised.stocks["SK_HYNIX"].metrics.close_price = 199999.0
            md2_revised.stocks["SK_HYNIX"].metrics.close_price_formatted = "199,999원"

            sync_module.sync_to_dashboard(md2_revised, digest_md="Day 2 v2", data_js_path=str(target_file))
            sync_module.sync_to_dashboard(md1, digest_md="Day 1 v1", data_js_path=str(target_file))
            sync_module.sync_to_dashboard(md3, digest_md="Day 3 v2", data_js_path=str(target_file))
            sync_module.sync_to_dashboard(md2_revised, digest_md="Day 2 v3", data_js_path=str(target_file))

            data_after = parse_js_data_store(target_file.read_text(encoding="utf-8"))

            # Must still have exactly 3 digests
            self.assertEqual(len(data_after["dailyDigests"]), 3)
            # Record count must NOT grow
            self.assertEqual(len(data_after["records"]), count_before)

            # SK_HYNIX Day 2 close record must have the updated price in-place
            hynix_day2 = next(
                r for r in data_after["records"]
                if r["date"] == "2026-09-29" and r["stockId"] == "SK_HYNIX" and r["type"] == "DAILY_CLOSE"
            )
            self.assertEqual(hynix_day2["metrics"]["price"], "199,999원")

    def test_partial_then_full_ingestion_for_same_date(self) -> None:
        """Morning partial dump (2 stocks) followed by evening full dump (6 stocks) for same date."""
        with tempfile.TemporaryDirectory(ignore_cleanup_errors=True) as tmp_dir:
            target_file = Path(tmp_dir) / "data.js"
            date = "2026-09-29"

            # Morning: only UBER and MBLY
            md_morning = create_adversarial_market_data(date=date, stocks_subset=["UBER", "MBLY"])
            sync_module.sync_to_dashboard(md_morning, digest_md="Morning Partial", data_js_path=str(target_file))

            data_morning = parse_js_data_store(target_file.read_text(encoding="utf-8"))
            morning_stock_ids = {r["stockId"] for r in data_morning["records"] if r.get("type") != "STRATEGY"}
            self.assertEqual(morning_stock_ids, {"UBER", "MBLY"})

            # Evening: full 6 stocks
            md_evening = create_adversarial_market_data(date=date)
            sync_module.sync_to_dashboard(md_evening, digest_md="Evening Full", data_js_path=str(target_file))

            data_evening = parse_js_data_store(target_file.read_text(encoding="utf-8"))
            # Exactly 1 digest entry for the date
            self.assertEqual(len(data_evening["dailyDigests"]), 1)
            self.assertEqual(data_evening["dailyDigests"][0]["markdownReport"], "Evening Full")

            # All 6 stocks present
            evening_stock_ids = {r["stockId"] for r in data_evening["records"] if r["type"] == "DAILY_CLOSE"}
            expected_stocks = {"SK_SQUARE", "SK_HYNIX", "UBER", "MBLY", "FLNC", "UPST"}
            self.assertTrue(expected_stocks.issubset(evening_stock_ids))

            # Exactly 1 close record per stock
            for sid in expected_stocks:
                recs = [r for r in data_evening["records"] if r["stockId"] == sid and r["type"] == "DAILY_CLOSE"]
                self.assertEqual(len(recs), 1, f"Expected 1 close record for {sid}, found {len(recs)}")


class TestTier5OfflineIsolation(unittest.TestCase):
    """Tier 5 Adversarial: 100% Offline Zero-Remote Isolation checks on index.html."""

    def setUp(self) -> None:
        self.assertTrue(INDEX_HTML_PATH.exists(), f"index.html must exist at {INDEX_HTML_PATH}")
        self.html_content = INDEX_HTML_PATH.read_text(encoding="utf-8")

    def test_zero_remote_script_and_link_tags(self) -> None:
        """No script src or link href may point to remote http/https/ftp/protocol-relative URLs."""
        # Check <script src="...">
        script_sources = re.findall(r'<script[^>]+src=["\']([^"\']+)["\']', self.html_content, re.IGNORECASE)
        for src in script_sources:
            src_clean = src.strip()
            self.assertFalse(
                src_clean.startswith(("http://", "https://", "ftp://", "//")),
                f"Forbidden remote script source: {src}",
            )
            # Must only reference local relative path (e.g. ./data.js or data.js)
            self.assertTrue(
                src_clean in ["./data.js", "data.js"],
                f"Unexpected external script reference: {src}",
            )

        # Check <link href="...">
        link_hrefs = re.findall(r'<link[^>]+href=["\']([^"\']+)["\']', self.html_content, re.IGNORECASE)
        for href in link_hrefs:
            href_clean = href.strip()
            self.assertFalse(
                href_clean.startswith(("http://", "https://", "ftp://", "//")),
                f"Forbidden remote link stylesheet/asset: {href}",
            )

    def test_zero_css_remote_imports_and_urls(self) -> None:
        """Embedded <style> must NOT contain @import or url() pointing to remote assets."""
        style_blocks = re.findall(r'<style[^>]*>(.*?)</style>', self.html_content, re.DOTALL | re.IGNORECASE)
        self.assertGreater(len(style_blocks), 0, "index.html must have embedded <style> blocks")

        for style in style_blocks:
            # Check @import
            imports = re.findall(r'@import\s+[^;]+;', style, re.IGNORECASE)
            self.assertEqual(imports, [], f"Forbidden CSS @import found in style: {imports}")

            # Check url(...) with remote schemas
            remote_urls = re.findall(r'url\s*\(\s*["\']?(https?:|ftp:|//)[^)]+["\']?\s*\)', style, re.IGNORECASE)
            self.assertEqual(remote_urls, [], f"Forbidden remote asset url() in CSS: {remote_urls}")

    def test_zero_external_cdn_references(self) -> None:
        """Scan for known CDN domains in HTML resource loaders."""
        forbidden_cdns = [
            "gstatic.com",
            "tailwindcss.com",
            "cdn.jsdelivr.net",
            "cdnjs.cloudflare.com",
            "unpkg.com",
            "googleapis.com",
        ]

        # Scan resource-loading tags only (script, link, img, iframe, style)
        resource_tags = re.findall(r'<(script|link|img|iframe|embed|object)[^>]+>', self.html_content, re.IGNORECASE)
        tag_texts = re.findall(r'<(?P<tag>script|link|img|iframe|embed|object)[^>]+>', self.html_content, re.IGNORECASE)

        for cdn in forbidden_cdns:
            # Resource tags must not mention any CDN
            matches = [t for t in tag_texts if cdn in t.lower()]
            self.assertEqual(matches, [], f"Forbidden CDN '{cdn}' detected in resource tag: {matches}")

    def test_offline_ui_badge_present(self) -> None:
        """index.html must display explicit offline indicators."""
        self.assertIn("100% Offline Core", self.html_content)
        self.assertIn("badge-offline", self.html_content)


class TestTier5BrowserDOMSafety(unittest.TestCase):
    """Tier 5 Adversarial: Script block parsing, syntax error absence, and DOM contract safety."""

    def setUp(self) -> None:
        self.assertTrue(INDEX_HTML_PATH.exists())
        self.html_content = INDEX_HTML_PATH.read_text(encoding="utf-8")

    def _extract_inline_scripts(self) -> List[str]:
        """Extracts contents of all inline <script> tags without src attribute."""
        pattern = re.compile(r'<script(?![^>]*\bsrc=)[^>]*>(.*?)</script>', re.DOTALL | re.IGNORECASE)
        return pattern.findall(self.html_content)

    def test_inline_script_bracket_and_quote_balance(self) -> None:
        """Verifies that all inline JavaScript scripts have perfectly balanced braces, quotes, and brackets."""
        scripts = self._extract_inline_scripts()
        self.assertGreater(len(scripts), 0, "No inline <script> block found in index.html")

        for idx, script in enumerate(scripts):
            # Context stack tracks delimiters: 'PAREN', 'BRACKET', 'BRACE', 'TEMPLATE', 'TEMPLATE_EXPR'
            stack: List[str] = []
            i = 0
            n = len(script)
            last_token = ""

            while i < n:
                c = script[i]
                nxt = script[i + 1] if i + 1 < n else ""
                current_ctx = stack[-1] if stack else None

                # Inside raw template literal text
                if current_ctx == "TEMPLATE":
                    if c == "\\":
                        i += 2
                        continue
                    elif c == "`":
                        stack.pop()
                    elif c == "$" and nxt == "{":
                        stack.append("TEMPLATE_EXPR")
                        i += 2
                        continue
                    i += 1
                    continue

                # 1. Line comment
                if c == "/" and nxt == "/":
                    end_line = script.find("\n", i)
                    i = end_line + 1 if end_line != -1 else n
                    continue

                # 2. Block comment
                if c == "/" and nxt == "*":
                    end_block = script.find("*/", i + 2)
                    self.assertNotEqual(end_block, -1, f"Unclosed block comment in script #{idx} at {i}")
                    i = end_block + 2
                    continue

                # 3. String literals (single & double quotes)
                if c in ('"', "'"):
                    quote = c
                    i += 1
                    while i < n:
                        if script[i] == "\\":
                            i += 2
                        elif script[i] == quote:
                            i += 1
                            break
                        elif script[i] == "\n":
                            self.fail(f"Unescaped newline in string literal in script #{idx} at {i}")
                        else:
                            i += 1
                    last_token = quote
                    continue

                # 4. Regex literal vs division
                if c == "/" and (last_token in ["(", ",", "=", ":", "[", "!", "&", "|", "?", "{", ";", "return", "typeof"]):
                    i += 1
                    in_char_class = False
                    while i < n:
                        if script[i] == "\\":
                            i += 2
                        elif script[i] == "[" and not in_char_class:
                            in_char_class = True
                            i += 1
                        elif script[i] == "]" and in_char_class:
                            in_char_class = False
                            i += 1
                        elif script[i] == "/" and not in_char_class:
                            i += 1
                            # Consume regex flags (e.g. g, i, m, s, u, y)
                            while i < n and script[i].isalpha():
                                i += 1
                            break
                        elif script[i] == "\n":
                            self.fail(f"Unterminated regex literal at newline in script #{idx} at {i}")
                        else:
                            i += 1
                    last_token = "REGEX"
                    continue

                # 5. Template literal entry
                if c == "`":
                    stack.append("TEMPLATE")
                    i += 1
                    last_token = "`"
                    continue

                # 6. Delimiters
                if c == "(":
                    stack.append("PAREN")
                    last_token = "("
                elif c == ")":
                    self.assertTrue(len(stack) > 0 and stack[-1] == "PAREN", f"Mismatched ')' in script #{idx} at position {i}")
                    stack.pop()
                    last_token = ")"
                elif c == "[":
                    stack.append("BRACKET")
                    last_token = "["
                elif c == "]":
                    self.assertTrue(len(stack) > 0 and stack[-1] == "BRACKET", f"Mismatched ']' in script #{idx} at position {i}")
                    stack.pop()
                    last_token = "]"
                elif c == "{":
                    stack.append("BRACE")
                    last_token = "{"
                elif c == "}":
                    self.assertTrue(
                        len(stack) > 0 and stack[-1] in ("BRACE", "TEMPLATE_EXPR"),
                        f"Mismatched '}}' in script #{idx} at position {i} (stack was {stack})",
                    )
                    stack.pop()
                    last_token = "}"
                elif not c.isspace():
                    last_token = c

                i += 1

            self.assertEqual(stack, [], f"Script #{idx} has unclosed syntax structures: {stack}")

    def test_dom_element_ids_referenced_in_js_exist_in_markup(self) -> None:
        """Every element ID queried via getElementById in script MUST exist as id='...' in the DOM."""
        scripts = self._extract_inline_scripts()
        all_js = "\n".join(scripts)

        # Find all getElementById("...")
        referenced_ids = set(re.findall(r'document\.getElementById\(["\']([^"\']+)["\']\)', all_js))
        self.assertGreater(len(referenced_ids), 0, "Expected getElementById calls in script")

        # Find all id="..." in HTML markup
        markup_ids = set(re.findall(r'\bid=["\']([^"\']+)["\']', self.html_content))

        # Check each referenced ID
        missing_ids = referenced_ids - markup_ids
        self.assertEqual(
            missing_ids,
            set(),
            f"JavaScript queries DOM elements that do NOT exist in HTML: {missing_ids}. "
            f"This would cause null pointer exceptions at runtime!",
        )

    def test_html_event_handlers_defined_in_javascript(self) -> None:
        """Every onclick/onchange/oninput function in HTML tags must be defined in the script."""
        scripts = self._extract_inline_scripts()
        all_js = "\n".join(scripts)

        # Find event handler calls: e.g. onclick="switchView('digest')"
        handler_calls = re.findall(r'\bon[a-z]+=["\']\s*([a-zA-Z0-9_]+)\s*\(', self.html_content)
        unique_handlers = set(handler_calls)
        self.assertGreater(len(unique_handlers), 0)

        for handler in unique_handlers:
            # Verify function declaration: function handlerName( or handlerName = (
            func_pattern = re.compile(rf'(?:function\s+{handler}\b|\b{handler}\s*=\s*(?:function|\([^)]*\)\s*=>))')
            self.assertTrue(
                func_pattern.search(all_js),
                f"HTML event handler '{handler}' is invoked in markup but NOT declared in JavaScript!",
            )

    def test_node_syntax_check_if_node_available(self) -> None:
        """If Node.js is installed on the host, run node --check with mock DOM globals."""
        node_bin = shutil.which("node")
        if not node_bin:
            self.skipTest("Node.js binary not available on this machine (skipping optional Node check)")

        scripts = self._extract_inline_scripts()
        combined_js = "\n".join(scripts)

        # Wrap in mock DOM environment to verify syntax and top-level evaluation
        mock_wrapper = f"""
        const window = {{ WATCHLIST_DATA: {{ records: [], dailyDigests: [] }} }};
        const document = {{
          addEventListener: () => {{}},
          getElementById: () => ({{
            classList: {{ add: () => {{}}, remove: () => {{}}, toggle: () => {{}} }},
            style: {{}},
            innerHTML: '',
            innerText: '',
            value: ''
          }}),
          querySelectorAll: () => []
        }};
        const console = {{ log: () => {{}}, warn: () => {{}}, error: () => {{}} }};

        // Extracted script from index.html:
        {combined_js}
        """

        with tempfile.NamedTemporaryFile("w", suffix=".js", delete=False, encoding="utf-8") as tf:
            tf.write(mock_wrapper)
            tf_path = tf.name

        try:
            res = subprocess.run(
                [node_bin, "--check", tf_path],
                capture_output=True,
                text=True,
                timeout=10,
            )
            self.assertEqual(
                res.returncode,
                0,
                f"Node.js syntax check failed on index.html script:\nSTDOUT: {res.stdout}\nSTDERR: {res.stderr}",
            )
        finally:
            if os.path.exists(tf_path):
                os.remove(tf_path)


class TestTier5CliAdversarialSync(unittest.TestCase):
    """Tier 5 Adversarial: Stress testing unified CLI sync entrypoint."""

    def test_cli_sync_empty_input_fails_with_code_1(self) -> None:
        """CLI sync with empty file must cleanly return exit code 1 with stderr warning."""
        with tempfile.TemporaryDirectory(ignore_cleanup_errors=True) as tmp_dir:
            empty_file = Path(tmp_dir) / "empty.txt"
            empty_file.write_text("", encoding="utf-8")

            exit_code = cli_module.main(["sync", "-i", str(empty_file)])
            self.assertEqual(exit_code, 1, "CLI sync on empty input must return code 1")

    def test_cli_sync_consecutive_multi_day_execution(self) -> None:
        """Simulate sequential pipeline runs via CLI main entrypoint."""
        from tests.fixtures.sample_dumps import SAMPLE_RAW_DUMP_FULL_DAY, SAMPLE_RAW_DUMP_DAY2

        with tempfile.TemporaryDirectory(ignore_cleanup_errors=True) as tmp_dir:
            dump1 = Path(tmp_dir) / "day1.txt"
            dump2 = Path(tmp_dir) / "day2.txt"
            dump1.write_text(SAMPLE_RAW_DUMP_FULL_DAY, encoding="utf-8")
            dump2.write_text(SAMPLE_RAW_DUMP_DAY2, encoding="utf-8")

            target_data_js = Path(tmp_dir) / "data.js"
            digest_dir = Path(tmp_dir) / "daily_digest"

            # Run 1: Day 1
            code1 = cli_module.main([
                "sync",
                "-i", str(dump1),
                "-d", "2026-09-29",
                "--digest-dir", str(digest_dir),
                "--data-js", str(target_data_js),
                "--quiet",
            ])
            self.assertEqual(code1, 0)

            # Run 2: Day 2
            code2 = cli_module.main([
                "sync",
                "-i", str(dump2),
                "-d", "2026-09-30",
                "--digest-dir", str(digest_dir),
                "--data-js", str(target_data_js),
                "--quiet",
            ])
            self.assertEqual(code2, 0)

            # Run 3: Day 1 Re-run (Idempotency via CLI)
            code3 = cli_module.main([
                "sync",
                "-i", str(dump1),
                "-d", "2026-09-29",
                "--digest-dir", str(digest_dir),
                "--data-js", str(target_data_js),
                "--quiet",
            ])
            self.assertEqual(code3, 0)

            # Verify outputs
            self.assertTrue((digest_dir / "2026-09-29_digest.md").exists())
            self.assertTrue((digest_dir / "2026-09-30_digest.md").exists())

            parsed = parse_js_data_store(target_data_js.read_text(encoding="utf-8"))
            self.assertEqual(len(parsed["dailyDigests"]), 2, "Expected exactly 2 distinct daily digests")


if __name__ == "__main__":
    unittest.main()
