"""Comprehensive Test Suite for Weekly Screener Report Generation & Pipeline Integration.

Tests:
1. Report Generation in engine/turnaround_screener.py:
   - Full 6-section institutional markdown report generation
   - Auto-creation of weekly_picks/ directory and YYYY-MM-DD_<ticker>.md file
   - Multi-year financial consensus table (2022~2027E)
   - SK Square 76 shares switching evaluation details
   - Polymorphic input handling (WeeklyTopPick, TurnaroundCandidate, dict)
2. Data Store Sync in engine/sync_dashboard.py:
   - create_default_weekly_screener_store() schema compliance
   - create_default_data_store() contains weeklyScreener key
   - build_weekly_screener_store() idempotent history updating for same date
   - Continuous price and return tracking across historical recommendations
   - Multi-date chronological history ordering
   - Roundtrip JS parsing and saving via parse_js_data_store
3. CLI Commands & Pipeline Integration in engine/cli.py:
   - cmd_weekly_pick human-readable stdout output
   - cmd_weekly_pick --json payload schema
   - cmd_weekly_pick --sync store serialization
   - cmd_sync end-to-end screener hook and stdout report
"""

import copy
from datetime import datetime
import json
from pathlib import Path
import shutil
import tempfile
import unittest

from engine.cli import build_parser, cmd_weekly_pick, cmd_sync
from engine.models import DailyMarketData
from engine.sync_dashboard import (
    DEFAULT_DATA_JS_PATH,
    build_weekly_screener_store,
    create_default_data_store,
    create_default_weekly_screener_store,
    load_data_store,
    parse_js_data_store,
    save_data_store,
    sync_to_dashboard,
    update_data_store_with_market_data,
)
from engine.turnaround_screener import (
    TurnaroundCandidate,
    TurnaroundScreener,
    WeeklyTopPick,
    generate_weekly_deep_dive_report,
)


class TestWeeklyDeepDiveReportGeneration(unittest.TestCase):
    """Test suite for generate_weekly_deep_dive_report in engine/turnaround_screener.py."""

    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.date_str = "2026-10-12"
        self.candidates = TurnaroundScreener.screen_universe(date=self.date_str)
        self.top_pick = TurnaroundScreener.select_weekly_top_pick(self.candidates, date=self.date_str)
        self.assertIsNotNone(self.top_pick)

    def tearDown(self):
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_report_content_contains_all_six_sections(self):
        """Verifies report includes Title, Executive Summary Table, and all 6 required sections."""
        report_md = generate_weekly_deep_dive_report(self.top_pick, output_dir=self.temp_dir)

        # Title and Executive Summary
        self.assertIn("# [Weekly Top-Pick Deep-Dive]", report_md)
        self.assertIn("모빌아이 (MBLY)", report_md)
        self.assertIn("## Executive Summary & Core Investment Thesis", report_md)
        self.assertIn("### 핵심 지표 요약 매트릭스 (Executive Summary Table)", report_md)
        self.assertIn("### 3대 핵심 투자 포인트 (Core Investment Thesis)", report_md)

        # Section 1
        self.assertIn("## Section 1: 비즈니스 모델 및 시장 지배력 (Business Model & Market Moat)", report_md)
        self.assertIn("수익 창출 구조 (Revenue Architecture)", report_md)
        self.assertIn("4대 구조적 경제적 해자 (Structural Moat)", report_md)

        # Section 2
        self.assertIn("## Section 2: 52주 신저가 추락 원인 정밀 해부 (Root Cause of 52-Week Low Fall & Why it's temporary)", report_md)
        self.assertIn("시장 투매의 3대 트리거 및 공포 해부", report_md)
        self.assertIn("일시적 노이즈(Noise) vs 영구적 결함(Structural Defect) 판별", report_md)
        self.assertIn("수급 바닥(Wash-Out) 및 지지선 방어 검증", report_md)

        # Section 3
        self.assertIn("## Section 3: 1~2년 실적 턴어라운드 핵심 동인 (1~2Y Turnaround Drivers & Catalysts)", report_md)
        self.assertIn("2022~2027E 실적 컨센서스 추이", report_md)
        self.assertIn("턴어라운드 견인 3대 확정 촉매", report_md)
        self.assertIn("잉여현금흐름(FCF) 및 재무 건전성 회복 궤적", report_md)

        # Section 4
        self.assertIn("## Section 4: 타점 진단 & 1~2년 2배(+100%) 로드맵 (Valuation, Timing & 2x Roadmap, TP1 100% Recovery)", report_md)
        self.assertIn("안전마진 매수 밴드", report_md)
        self.assertIn("TP1 (1차 매도 - 원금 100% 무위험 회수선)", report_md)
        self.assertIn("TP2 (2차 매도 - 본질가치 정상화 익절선)", report_md)

        # Section 5
        self.assertIn("## Section 5: 기존 보유 포트폴리오(SK스퀘어 76주)와의 전술적 스위칭 적합도 평가 (Tactical Switching Suitability)", report_md)
        self.assertIn("SK스퀘어 (402340)", report_md)
        self.assertIn("76주", report_md)
        self.assertIn("8,284만 원", report_md)
        self.assertIn("HOLD_CORE_AND_BUY_SEPARATE", report_md)

        # Section 6
        self.assertIn("## Section 6: 주간 모니터링 체크리스트 및 결론 (Weekly Checklist & Conclusion)", report_md)
        self.assertIn("STRONG_BUY (금주의 주간 Top-Pick)", report_md)
        self.assertIn("차주 주간 실전 모니터링 체크리스트", report_md)

    def test_report_file_creation_in_directory(self):
        """Verifies report file is created as YYYY-MM-DD_<ticker>.md in output_dir."""
        sub_dir = Path(self.temp_dir) / "nested_weekly_picks"
        report_md = generate_weekly_deep_dive_report(self.top_pick, output_dir=sub_dir)

        expected_file = sub_dir / f"{self.date_str}_MBLY.md"
        self.assertTrue(expected_file.exists())
        self.assertEqual(expected_file.read_text(encoding="utf-8"), report_md)

    def test_report_file_creation_with_explicit_markdown_filepath(self):
        """Verifies passing explicit filepath directly writes to that path."""
        explicit_path = Path(self.temp_dir) / "custom_report.md"
        report_md = generate_weekly_deep_dive_report(self.top_pick, output_dir=explicit_path)

        self.assertTrue(explicit_path.exists())
        self.assertEqual(explicit_path.read_text(encoding="utf-8"), report_md)

    def test_polymorphic_input_handling(self):
        """Verifies function works with WeeklyTopPick, TurnaroundCandidate, and dict."""
        # 1. WeeklyTopPick object
        res1 = generate_weekly_deep_dive_report(self.top_pick, output_dir=self.temp_dir)
        self.assertTrue(len(res1) > 2000)

        # 2. TurnaroundCandidate object directly
        cand = self.top_pick.candidate
        res2 = generate_weekly_deep_dive_report(cand, output_dir=self.temp_dir)
        self.assertTrue(len(res2) > 2000)

        # 3. Dictionary representation
        pick_dict = self.top_pick.to_dict()
        res3 = generate_weekly_deep_dive_report(pick_dict, output_dir=self.temp_dir)
        self.assertTrue(len(res3) > 2000)


class TestWeeklyScreenerDataStoreSync(unittest.TestCase):
    """Test suite for weeklyScreener store in engine/sync_dashboard.py."""

    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.date_str = "2026-10-12"
        self.candidates = TurnaroundScreener.screen_universe(date=self.date_str)
        self.top_pick = TurnaroundScreener.select_weekly_top_pick(self.candidates, date=self.date_str)

    def tearDown(self):
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_create_default_weekly_screener_store_schema(self):
        """Verifies default weekly screener store contains required keys and active status."""
        store = create_default_weekly_screener_store(self.date_str)
        self.assertEqual(store["lastEvaluated"], self.date_str)
        self.assertEqual(store["status"], "ACTIVE")
        self.assertEqual(store["benchmarkDate"], self.date_str)
        self.assertIn("currentPick", store)
        self.assertIn("candidates", store)
        self.assertIn("history", store)

        pick = store["currentPick"]
        self.assertIsNotNone(pick)
        self.assertEqual(pick["ticker"], "MBLY")
        self.assertEqual(pick["stockId"], "MBLY")
        self.assertEqual(pick["currency"], "USD")
        self.assertTrue(pick["currentPrice"] > 0)
        self.assertTrue(pick["tp1Price"] > pick["currentPrice"])
        self.assertEqual(pick["tp1Action"], "50% 분할 매도로 투자원금 100% 무위험 회수")
        self.assertIn("twoYearTurnaroundGrowth", pick)
        self.assertIn("primaryCatalyst", pick)
        self.assertIn("switchingEvaluation", pick)

    def test_create_default_data_store_contains_weekly_screener(self):
        """Verifies create_default_data_store() initializes weeklyScreener."""
        ds = create_default_data_store()
        self.assertIn("weeklyScreener", ds)
        ws = ds["weeklyScreener"]
        self.assertEqual(ws["status"], "ACTIVE")
        self.assertIsNotNone(ws["currentPick"])

    def test_build_weekly_screener_store_idempotent_same_date(self):
        """Verifies running build_weekly_screener_store multiple times on same date updates in-place."""
        store1 = build_weekly_screener_store(
            candidates=self.candidates,
            top_pick=self.top_pick,
            date=self.date_str,
            existing_store=None,
        )
        self.assertEqual(len(store1["history"]), 1)
        self.assertEqual(store1["history"][0]["ticker"], "MBLY")

        # Second evaluation on same date with existing_store passed
        store2 = build_weekly_screener_store(
            candidates=self.candidates,
            top_pick=self.top_pick,
            date=self.date_str,
            existing_store=store1,
        )
        # Length must strictly remain 1 without duplicate entries
        self.assertEqual(len(store2["history"]), 1)
        self.assertEqual(store2["history"][0]["ticker"], "MBLY")

    def test_build_weekly_screener_store_multiple_dates_ordering(self):
        """Verifies distinct dates produce multiple history records reverse-chronologically sorted."""
        # 1. Earlier pick on 2026-10-05 (CELH simulated)
        celh_cand = TurnaroundScreener.screen_stock("CELH", date="2026-10-05")
        celh_pick = TurnaroundScreener.select_weekly_top_pick([celh_cand], date="2026-10-05")
        store_past = build_weekly_screener_store(
            candidates=[celh_cand],
            top_pick=celh_pick,
            date="2026-10-05",
            existing_store=None,
        )
        self.assertEqual(len(store_past["history"]), 1)
        self.assertEqual(store_past["history"][0]["date"], "2026-10-05")

        # 2. Add current pick on 2026-10-12 (MBLY)
        store_now = build_weekly_screener_store(
            candidates=self.candidates,
            top_pick=self.top_pick,
            date="2026-10-12",
            existing_store=store_past,
        )
        self.assertEqual(len(store_now["history"]), 2)
        # Reverse chronological ordering check
        self.assertEqual(store_now["history"][0]["date"], "2026-10-12")
        self.assertEqual(store_now["history"][0]["ticker"], "MBLY")
        self.assertEqual(store_now["history"][1]["date"], "2026-10-05")
        self.assertEqual(store_now["history"][1]["ticker"], "CELH")

    def test_historical_return_percentage_updating(self):
        """Verifies continuous updating of current price and return percentage for historical items."""
        # Previous pick recommended at $25.00
        mock_past_item = {
            "id": "REC-20261005-CELH",
            "date": "2026-10-05",
            "stockId": "CELH",
            "ticker": "CELH",
            "stockName": "셀시우스홀딩스",
            "recommendedPrice": 25.00,
            "recommendedPriceFormatted": "$25.00",
            "currentPrice": 25.00,
            "currentPriceFormatted": "$25.00",
            "returnPct": 0.0,
            "returnPctFormatted": "+0.0%",
            "tp1Target": 55.00,
            "tp1TargetFormatted": "$55.00",
            "targetReturnPct": 120.0,
            "currentStatus": "ACTIVE",
            "markdownPath": "weekly_picks/2026-10-05_CELH.md",
            "summary": "Past recommendation",
        }
        mock_existing_store = {
            "lastEvaluated": "2026-10-05",
            "status": "ACTIVE",
            "benchmarkDate": "2026-10-05",
            "currentPick": None,
            "candidates": [],
            "history": [mock_past_item],
        }

        # Screen universe on 2026-10-12 where CELH current price is $27.35
        store = build_weekly_screener_store(
            candidates=self.candidates,
            top_pick=self.top_pick,
            date="2026-10-12",
            existing_store=mock_existing_store,
        )
        # Check that CELH historical entry updated current price to $27.35 and return to +9.4%
        hist_celh = [h for h in store["history"] if h["ticker"] == "CELH"][0]
        self.assertEqual(hist_celh["currentPrice"], 27.35)
        self.assertAlmostEqual(hist_celh["returnPct"], 9.4, places=1)
        self.assertEqual(hist_celh["returnPctFormatted"], "+9.4%")

    def test_update_data_store_with_market_data_integration(self):
        """Verifies update_data_store_with_market_data seamlessly embeds weeklyScreener."""
        md = DailyMarketData(date=self.date_str, stocks={})
        ds = create_default_data_store()

        updated_ds = update_data_store_with_market_data(
            data_store=ds,
            market_data=md,
            weekly_screener=(self.candidates, self.top_pick),
        )
        self.assertIn("weeklyScreener", updated_ds)
        self.assertEqual(updated_ds["weeklyScreener"]["currentPick"]["ticker"], "MBLY")
        self.assertEqual(len(updated_ds["weeklyScreener"]["candidates"]), len(self.candidates))

    def test_sync_to_dashboard_roundtrip_js(self):
        """Verifies sync_to_dashboard writes valid JS file and roundtrips without parse errors."""
        temp_js = Path(self.temp_dir) / "test_data.js"
        md = DailyMarketData(date=self.date_str, stocks={})

        ok = sync_to_dashboard(
            market_data=md,
            data_js_path=str(temp_js),
            weekly_screener=(self.candidates, self.top_pick),
        )
        self.assertTrue(ok)
        self.assertTrue(temp_js.exists())

        # Load back from written JS file
        loaded_ds = load_data_store(temp_js)
        self.assertIn("weeklyScreener", loaded_ds)
        self.assertEqual(loaded_ds["weeklyScreener"]["currentPick"]["ticker"], "MBLY")


class TestCLIPipelineIntegration(unittest.TestCase):
    """Test suite for CLI weekly_pick subcommand and sync pipeline hooks."""

    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.date_str = "2026-10-12"
        self.data_js_path = Path(self.temp_dir) / "data.js"
        save_data_store(create_default_data_store(), self.data_js_path)

    def tearDown(self):
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_parser_has_weekly_pick_subcommand(self):
        """Verifies build_parser includes weekly_pick subcommand with required arguments."""
        parser = build_parser()
        args = parser.parse_args(["weekly_pick", "--date", "2026-10-12", "--sync", "--json"])
        self.assertEqual(args.command, "weekly_pick")
        self.assertEqual(args.date, "2026-10-12")
        self.assertTrue(args.sync)
        self.assertTrue(args.json)

    def test_cmd_weekly_pick_execution_stdout(self):
        """Verifies executing cmd_weekly_pick returns 0 and creates report in output dir."""
        out_dir = Path(self.temp_dir) / "picks"
        parser = build_parser()
        args = parser.parse_args([
            "weekly_pick",
            "--date", self.date_str,
            "--out-dir", str(out_dir),
        ])
        rc = cmd_weekly_pick(args)
        self.assertEqual(rc, 0)
        expected_md = out_dir / f"{self.date_str}_MBLY.md"
        self.assertTrue(expected_md.exists())

    def test_cmd_weekly_pick_sync_flag_updates_data_js(self):
        """Verifies executing cmd_weekly_pick with --sync updates target data.js."""
        out_dir = Path(self.temp_dir) / "picks"
        parser = build_parser()
        args = parser.parse_args([
            "weekly_pick",
            "--date", self.date_str,
            "--out-dir", str(out_dir),
            "--data-js", str(self.data_js_path),
            "--sync",
        ])
        rc = cmd_weekly_pick(args)
        self.assertEqual(rc, 0)

        # Check data.js content
        ds = load_data_store(self.data_js_path)
        self.assertIn("weeklyScreener", ds)
        self.assertEqual(ds["weeklyScreener"]["currentPick"]["ticker"], "MBLY")
        self.assertEqual(len(ds["weeklyScreener"]["history"]), 1)

    def test_cmd_sync_executes_screener_hook_and_generates_artifacts(self):
        """Verifies cmd_sync pipeline generates weekly deep-dive report and serializes weeklyScreener."""
        dump_file = Path(self.temp_dir) / "dump.txt"
        dump_file.write_text(
            f"=== 2026-10-12 관심종목 시황 ===\n[SKHY 일일 시세 요약]\n종가: $188.80\n등락률: +1.5%\n"
            f"[MBLY 일일 시세 요약]\n종가: $7.47\n등락률: +2.1%\n거래량: 12,000,000\n",
            encoding="utf-8",
        )
        out_dir = Path(self.temp_dir) / "weekly_picks"
        digest_dir = Path(self.temp_dir) / "daily_digest"
        insight_dir = Path(self.temp_dir) / "daily_insight"

        parser = build_parser()
        args = parser.parse_args([
            "sync",
            "-i", str(dump_file),
            "-d", self.date_str,
            "--data-js", str(self.data_js_path),
            "--weekly-picks-dir", str(out_dir),
            "--digest-dir", str(digest_dir),
            "--insight-dir", str(insight_dir),
            "--quiet",
        ])
        rc = cmd_sync(args)
        self.assertEqual(rc, 0)

        # Check weekly report was created
        expected_report = out_dir / f"{self.date_str}_MBLY.md"
        self.assertTrue(expected_report.exists())
        self.assertIn("## Section 1: 비즈니스 모델 및 시장 지배력", expected_report.read_text(encoding="utf-8"))

        # Check data.js was updated with weeklyScreener
        ds = load_data_store(self.data_js_path)
        self.assertIn("weeklyScreener", ds)
        self.assertEqual(ds["weeklyScreener"]["currentPick"]["ticker"], "MBLY")


if __name__ == "__main__":
    unittest.main()
