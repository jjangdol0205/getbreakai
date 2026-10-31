"""Empirical Adversarial Challenge Test Suite for Milestone M3 Gate (Challenger 2).

Specific Challenge Objectives from DISPATCH.md:
1. Challenge Pipeline Idempotency:
   - Repeatedly run `update_data_store_with_market_data` with the same date (5 times in a loop).
     Verify `history` array does NOT duplicate entries.
   - Run across arbitrary date orders (out-of-order dates, past dates, future dates)
     and verify `history` array stays properly sorted and valid.
2. Challenge Data Invariant Preservation:
   - Verify `d["portfolio"] == DEFAULT_PORTFOLIO` invariant is preserved under all conditions.
   - Verify all existing keys (`lastUpdated`, `portfolio`, `stocks`, `records`, `dailyDigests`,
     `dailyInsights`, `financials`) remain completely unharmed.
3. Challenge Multi-Date Switching & History UI:
   - In `data.js`, verify `timing.history` structure across all 12 dates.
   - Verify that switching recommendations update dynamically across dates.
"""

from __future__ import annotations

import copy
import json
from pathlib import Path
import re
import unittest

ROOT_DIR = Path(__file__).resolve().parent.parent
DATA_JS_PATH = ROOT_DIR / "data.js"
INDEX_HTML_PATH = ROOT_DIR / "index.html"

from engine.models import DailyMarketData, StockFactSheet, MarketMetrics, StockSymbol
from engine.sync_dashboard import (
    DEFAULT_DATA_JS_PATH,
    DEFAULT_FINANCIALS,
    DEFAULT_PORTFOLIO,
    DEFAULT_STOCKS,
    build_timing_store_from_snapshot,
    create_default_data_store,
    create_default_timing_store,
    load_data_store,
    parse_js_data_store,
    update_data_store_with_market_data,
)
from engine.timing_engine import TimingEngine


class TestChallengerM3PipelineIdempotency(unittest.TestCase):
    """Adversarially challenges idempotency and sorting of timing history in sync_dashboard."""

    def setUp(self) -> None:
        self.raw_js = DATA_JS_PATH.read_text(encoding="utf-8")
        self.data_store = parse_js_data_store(self.raw_js)

    def test_challenge_same_date_repeated_runs_no_duplication(self) -> None:
        """Adversarial Challenge: Run update_data_store_with_market_data 5 times on the same date.

        Must NOT inflate data_store['timing']['history'] array.
        """
        store = copy.deepcopy(self.data_store)
        initial_history_len = len(store.get("timing", {}).get("history", []))
        self.assertGreaterEqual(initial_history_len, 1, "Initial history must have at least 1 entry")

        target_date = "2026-10-12"
        mock_market_data = DailyMarketData(date=target_date, stocks={})

        # Run 5 times in a loop
        for run_idx in range(5):
            updated_store = update_data_store_with_market_data(
                store,
                mock_market_data,
                digest_md=f"# Digest for {target_date} run {run_idx}",
            )
            history = updated_store.get("timing", {}).get("history", [])
            dates = [h.get("date") for h in history]

            # The target date must appear exactly once
            count_target = dates.count(target_date)
            self.assertEqual(
                count_target,
                1,
                f"Date {target_date} must appear exactly once, but appeared {count_target} times on run {run_idx + 1}"
            )

            # All dates in history must be strictly unique
            self.assertEqual(
                len(dates),
                len(set(dates)),
                f"History must contain strictly unique dates on run {run_idx + 1}: duplicates found in {dates}"
            )

            # History length must stay constant across repeated runs on the same date
            self.assertEqual(
                len(history),
                initial_history_len,
                f"History length inflated from {initial_history_len} to {len(history)} on run {run_idx + 1}"
            )

    def test_challenge_arbitrary_and_out_of_order_date_insertions(self) -> None:
        """Adversarial Challenge: Insert dates out-of-order (past, future, interleaved).

        The history list must remain strictly sorted in descending chronological order.
        """
        store = create_default_data_store()
        # Start with an empty history
        store["timing"]["history"] = []

        scrambled_dates = [
            "2026-10-05",
            "2027-01-15",  # Future date
            "2025-12-31",  # Past date
            "2026-10-01",
            "2026-10-10",
            "2026-09-15",  # Past date
            "2026-10-12",
            "2026-10-05",  # Duplicate insertion of 10-05
        ]

        for d in scrambled_dates:
            md = DailyMarketData(date=d, stocks={})
            store = update_data_store_with_market_data(store, md)
            history = store.get("timing", {}).get("history", [])
            hist_dates = [h.get("date") for h in history]

            # Verify no duplicates
            self.assertEqual(len(hist_dates), len(set(hist_dates)), f"Duplicate dates found after inserting {d}: {hist_dates}")

            # Verify strictly descending chronological sort order
            sorted_desc = sorted(hist_dates, reverse=True)
            self.assertEqual(
                hist_dates,
                sorted_desc,
                f"History array must stay strictly sorted descending. Got {hist_dates}, expected {sorted_desc}"
            )

        # Expected unique dates
        expected_unique = sorted(list(set(scrambled_dates)), reverse=True)
        final_dates = [h.get("date") for h in store["timing"]["history"]]
        self.assertEqual(final_dates, expected_unique)


class TestChallengerM3DataInvariantPreservation(unittest.TestCase):
    """Adversarially challenges preservation of data.js and engine invariants."""

    def setUp(self) -> None:
        self.raw_js = DATA_JS_PATH.read_text(encoding="utf-8")
        self.data_store = parse_js_data_store(self.raw_js)

    def test_challenge_portfolio_equals_default_portfolio_invariant(self) -> None:
        """Invariant: d['portfolio'] must equal DEFAULT_PORTFOLIO 100%."""
        portfolio = self.data_store.get("portfolio")
        self.assertIsNotNone(portfolio, "data.js must contain 'portfolio'")
        self.assertEqual(
            portfolio,
            DEFAULT_PORTFOLIO,
            "data.js portfolio must be 100% identical to DEFAULT_PORTFOLIO"
        )

    def test_challenge_all_existing_keys_intact(self) -> None:
        """Invariant: All 8 core keys must exist and contain non-empty valid structures."""
        required_keys = [
            "lastUpdated",
            "portfolio",
            "stocks",
            "records",
            "dailyDigests",
            "dailyInsights",
            "financials",
            "timing",
        ]
        for key in required_keys:
            self.assertIn(key, self.data_store, f"Required top-level key '{key}' missing from data.js")

        # 1. stocks invariant: must have 9 elements (ALL + 8 stocks)
        stocks = self.data_store.get("stocks", [])
        self.assertEqual(len(stocks), len(DEFAULT_STOCKS))
        stock_ids = [s.get("id") for s in stocks]
        for expected_id in ["ALL", "SK_SQUARE", "SK_HYNIX", "UBER", "MBLY", "FLNC", "UPST", "CELH", "ENPH"]:
            self.assertIn(expected_id, stock_ids)

        # 2. financials invariant: must have 8 stocks and 2022~2027E years
        financials = self.data_store.get("financials", {})
        self.assertEqual(len(financials), 8)
        for s_id in ["SK_HYNIX", "SK_SQUARE", "UBER", "MBLY", "FLNC", "UPST", "CELH", "ENPH"]:
            self.assertIn(s_id, financials)
            self.assertIn("income_statement", financials[s_id])
            self.assertIn("profitability", financials[s_id])
            self.assertIn("cash_flow", financials[s_id])
            self.assertIn("balance_sheet", financials[s_id])
            self.assertIn("valuation", financials[s_id])

        # 3. records invariant: non-empty list of historical briefing records
        records = self.data_store.get("records", [])
        self.assertIsInstance(records, list)
        self.assertGreater(len(records), 0)

        # 4. dailyDigests and dailyInsights: non-empty lists
        digests = self.data_store.get("dailyDigests", [])
        self.assertIsInstance(digests, list)
        self.assertGreater(len(digests), 0)

        insights = self.data_store.get("dailyInsights", [])
        self.assertIsInstance(insights, list)
        self.assertGreater(len(insights), 0)

    def test_challenge_sync_does_not_mutate_portfolio_invariant_when_updating_earlier_dates(self) -> None:
        """Adversarial Challenge: Syncing an earlier date must NOT mutate default portfolio in memory."""
        store = copy.deepcopy(self.data_store)
        initial_portfolio = copy.deepcopy(store["portfolio"])

        # Sync an earlier date e.g. 2026-09-29
        past_md = DailyMarketData(date="2026-09-29", stocks={})
        updated = update_data_store_with_market_data(store, past_md)

        self.assertEqual(
            updated["portfolio"],
            initial_portfolio,
            "Syncing an earlier date must not overwrite top-level portfolio with outdated values"
        )


class TestChallengerM3MultiDateSwitchingAndHistory(unittest.TestCase):
    """Adversarially challenges multi-date switching dynamics across all 12 dates in data.js."""

    def setUp(self) -> None:
        self.raw_js = DATA_JS_PATH.read_text(encoding="utf-8")
        self.data_store = parse_js_data_store(self.raw_js)
        self.timing = self.data_store.get("timing", {})
        self.history = self.timing.get("history", [])

    def test_challenge_all_12_dates_present_in_timing_history(self) -> None:
        """Adversarial Challenge: Verify exactly 12 dates in timing.history."""
        self.assertEqual(len(self.history), 12, f"Expected 12 dates in timing.history, got {len(self.history)}")

        history_dates = [h.get("date") for h in self.history]
        expected_dates = [
            "2026-10-12",
            "2026-10-11",
            "2026-10-10",
            "2026-10-09",
            "2026-10-08",
            "2026-10-07",
            "2026-10-06",
            "2026-10-02",
            "2026-10-01",
            "2026-09-30",
            "2026-09-29",
            "2026-09-28",
        ]
        self.assertEqual(history_dates, expected_dates, "timing.history dates must match exact 12 expected dates in descending order")

    def test_challenge_history_entry_internal_structure_integrity(self) -> None:
        """Every history entry across all 12 dates must possess a complete, valid schema."""
        for entry in self.history:
            date_str = entry.get("date")
            self.assertIsNotNone(date_str)

            # Portfolio diagnosis
            diag = entry.get("portfolioDiagnosis")
            self.assertIsNotNone(diag, f"portfolioDiagnosis missing in history entry {date_str}")
            self.assertEqual(diag.get("holdingStock"), "SK_SQUARE")
            self.assertEqual(diag.get("shares"), 76)
            self.assertGreater(diag.get("basePrice", 0), 0)
            self.assertIn("currentPhase", diag)
            self.assertIn("tpGuide", diag)
            tp_guide = diag["tpGuide"]
            self.assertIn("tp1", tp_guide)
            self.assertIn("tp2", tp_guide)
            self.assertIn("tp3", tp_guide)

            # Stocks mapping
            stocks = entry.get("stocks")
            self.assertIsNotNone(stocks, f"stocks missing in history entry {date_str}")
            for sid in ["SK_HYNIX", "SK_SQUARE", "UBER", "MBLY", "FLNC", "UPST", "CELH", "ENPH"]:
                self.assertIn(sid, stocks, f"Stock {sid} missing from stocks in history entry {date_str}")

            # Switching opportunities
            sw = entry.get("switchingOpportunities")
            self.assertIsNotNone(sw, f"switchingOpportunities missing in history entry {date_str}")
            self.assertIn(
                sw.get("status"),
                {"REVERSE_SWITCH_WARNING", "SWITCH_OPPORTUNITY", "HOLD_CORE"},
                f"Invalid switching status in history entry {date_str}: {sw.get('status')}"
            )
            self.assertIsInstance(sw.get("candidates"), list)
            self.assertIsInstance(sw.get("scenarios"), list)

    def test_challenge_switching_recommendations_vary_dynamically_across_dates(self) -> None:
        """Adversarial Challenge: Switching recommendations must NOT be static canned strings.

        They must dynamically reflect market condition shifts across dates.
        """
        statuses = {h.get("date"): h.get("status") for h in self.history}
        unique_statuses = set(statuses.values())

        # Assert that we don't have a single hardcoded status across all 12 days
        self.assertGreater(
            len(unique_statuses),
            1,
            f"Switching statuses must vary across historical dates, but only saw: {unique_statuses}"
        )

        # Specifically verify both REVERSE_SWITCH_WARNING and other statuses occur
        self.assertIn(
            "REVERSE_SWITCH_WARNING",
            unique_statuses,
            "REVERSE_SWITCH_WARNING must be triggered on dates where SK Square catalyst is imminent"
        )

        # Verify prices change across history
        prices = [h.get("portfolioDiagnosis", {}).get("basePrice") for h in self.history]
        unique_prices = set(prices)
        self.assertGreater(
            len(unique_prices),
            1,
            f"Base prices must reflect dynamic market prices across dates, but were static: {unique_prices}"
        )

    def test_challenge_index_html_history_timeline_and_selector_support_all_12_dates(self) -> None:
        """index.html must cleanly handle all 12 dates in its JavaScript controller."""
        html_content = INDEX_HTML_PATH.read_text(encoding="utf-8")

        # Must bind timing history in renderTimingHistoryTimeline
        self.assertIn("renderTimingHistoryTimeline", html_content)
        self.assertIn("timingHistoryTableBody", html_content)
        self.assertIn("selectTimingHistoryDate", html_content)

        # Must support dynamic switching card rendering
        self.assertIn("renderTimingSwitching", html_content)
        self.assertIn("timingSwitchingCard", html_content)
        self.assertIn("switchingCardContent", html_content)

        # Must properly extract history from dataStore.timing.history
        self.assertIn("dataStore.timing.history", html_content)


class TestChallengerM3ExtremeEdgeCasesAndCli(unittest.TestCase):
    """Adversarial stress-testing of extreme inputs, edge cases, and CLI integration."""

    def test_build_timing_store_with_extreme_base_prices(self) -> None:
        """Adversarial test: Validate currentPhase and tpGuide calculation across price regimes."""
        from engine.models import DailyMarketData
        mock_md = DailyMarketData(date="2026-10-12", stocks={})

        # 1. Price in Safety Margin (< 1,120,000)
        snap1 = TimingEngine.evaluate_daily_timing(mock_md, portfolio={"holdingStock": "SK_SQUARE", "shares": 76}, as_of_date="2026-10-12")
        snap1.stocks["SK_SQUARE"].trigger.current_price = 1065000.0
        store1 = build_timing_store_from_snapshot(snap1, date_str="2026-10-12")
        self.assertEqual(store1["portfolioDiagnosis"]["currentPhase"], "안전마진 밴드 진입 / TP1 대기")

        # 2. Price in Rally (1,120,000 ~ 2,100,000)
        snap2 = TimingEngine.evaluate_daily_timing(mock_md, portfolio={"holdingStock": "SK_SQUARE", "shares": 76}, as_of_date="2026-10-12")
        snap2.stocks["SK_SQUARE"].trigger.current_price = 1500000.0
        store2 = build_timing_store_from_snapshot(snap2, date_str="2026-10-12")
        self.assertEqual(store2["portfolioDiagnosis"]["currentPhase"], "안전마진 탈출 / 상승 랠리 (TP1 대기)")

        # 3. Price reaching TP1 (2,100,000 ~ 5,000,000)
        snap3 = TimingEngine.evaluate_daily_timing(mock_md, portfolio={"holdingStock": "SK_SQUARE", "shares": 76}, as_of_date="2026-10-12")
        snap3.stocks["SK_SQUARE"].trigger.current_price = 2500000.0
        store3 = build_timing_store_from_snapshot(snap3, date_str="2026-10-12")
        self.assertEqual(store3["portfolioDiagnosis"]["currentPhase"], "TP1 도달 / 1차 원금 회수 구간")

        # 4. Price reaching TP2 (>= 5,000,000)
        snap4 = TimingEngine.evaluate_daily_timing(mock_md, portfolio={"holdingStock": "SK_SQUARE", "shares": 76}, as_of_date="2026-10-12")
        snap4.stocks["SK_SQUARE"].trigger.current_price = 5500000.0
        store4 = build_timing_store_from_snapshot(snap4, date_str="2026-10-12")
        self.assertEqual(store4["portfolioDiagnosis"]["currentPhase"], "TP2 도달 / 2차 분할 익절 구간")

        # 5. Price = 0.0 (Zero price defensive handling: no ZeroDivisionError)
        snap5 = TimingEngine.evaluate_daily_timing(mock_md, portfolio={"holdingStock": "SK_SQUARE", "shares": 76}, as_of_date="2026-10-12")
        snap5.stocks["SK_SQUARE"].trigger.current_price = 0.0
        store5 = build_timing_store_from_snapshot(snap5, date_str="2026-10-12")
        self.assertIsNotNone(store5["portfolioDiagnosis"]["tpGuide"]["tp1"]["gainPct"])

    def test_update_data_store_with_missing_or_corrupted_timing_key(self) -> None:
        """Adversarial test: update_data_store_with_market_data must recover gracefully if timing key is None or empty."""
        store = create_default_data_store()
        store["timing"] = None

        mock_md = DailyMarketData(date="2026-10-12", stocks={})
        updated = update_data_store_with_market_data(store, mock_md)

        self.assertIsNotNone(updated.get("timing"))
        self.assertIn("history", updated["timing"])
        self.assertGreaterEqual(len(updated["timing"]["history"]), 1)

    def test_cli_timing_subcommand_execution_and_json_parsing(self) -> None:
        """Adversarial test: CLI timing subcommand must execute cleanly and yield valid JSON."""
        import subprocess
        import sys

        result = subprocess.run(
            [sys.executable, "-m", "engine.cli", "timing", "--date", "2026-10-12", "--json"],
            cwd=str(ROOT_DIR),
            capture_output=True,
            text=True,
            encoding="utf-8",
            check=False,
        )
        self.assertEqual(result.returncode, 0, f"CLI timing failed with error: {result.stderr}")
        parsed = json.loads(result.stdout)
        self.assertIn("date", parsed)
        self.assertIn("stocks", parsed)
        self.assertIn("switching", parsed)
        self.assertEqual(parsed["switching"]["holding_stock_id"], "SK_SQUARE")
        self.assertEqual(parsed["switching"]["holding_shares"], 76)


if __name__ == "__main__":
    unittest.main()
