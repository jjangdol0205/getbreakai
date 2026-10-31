"""Tests for Dynamic Portfolio KPI Ribbon & Pair Allocation Real-Time Recalculation.

Validates:
1. 100% Synchronization between data.js portfolio and engine.sync_dashboard.DEFAULT_PORTFOLIO.
2. Latest baseline evaluation (approx 8,750만 원, 58.1% : 41.9%) for SK Square (44 shares) + SK Hynix (20 shares).
3. index.html top 4 KPI ribbon DOM element presence and dynamic calculation JavaScript logic.
4. Mathematical accuracy across date transitions (2026-09-28 ~ 2026-10-06).
5. 100% offline file:// execution and Zero-CDN compliance.
"""

from __future__ import annotations

import json
from pathlib import Path
import re
import unittest

ROOT_DIR = Path(__file__).resolve().parent.parent
DATA_JS_PATH = ROOT_DIR / "data.js"
INDEX_HTML_PATH = ROOT_DIR / "index.html"

from engine.sync_dashboard import DEFAULT_PORTFOLIO, parse_js_data_store


class TestPortfolioKpiSynchronization(unittest.TestCase):
    """R2: Baseline portfolio synchronization between data.js and sync_dashboard.py."""

    def setUp(self) -> None:
        self.assertTrue(DATA_JS_PATH.exists(), f"data.js must exist at {DATA_JS_PATH}")
        self.raw_js = DATA_JS_PATH.read_text(encoding="utf-8")
        self.data_store = parse_js_data_store(self.raw_js)

    def test_data_js_and_engine_default_portfolio_identical(self) -> None:
        """data.js portfolio must be 100% identical to engine.sync_dashboard.DEFAULT_PORTFOLIO."""
        js_portfolio = self.data_store.get("portfolio")
        self.assertIsNotNone(js_portfolio, "data.js must contain 'portfolio' key")
        self.assertEqual(
            js_portfolio,
            DEFAULT_PORTFOLIO,
            "data.js portfolio and engine.sync_dashboard.DEFAULT_PORTFOLIO must match 100%"
        )

    def test_default_portfolio_latest_valuation_and_ratio(self) -> None:
        """Portfolio baseline must reflect approx 8,750만 원 and latest or historical target ratio."""
        portfolio = DEFAULT_PORTFOLIO
        self.assertEqual(portfolio["totalValue"], "약 8,750만 원")
        self.assertIn(portfolio["targetRatio"], ["SK스퀘어 79.1% : SK하이닉스 20.9%", "SK스퀘어 77.3% : SK하이닉스 22.7%", "SK스퀘어 58.1% : SK하이닉스 41.9%"])
        self.assertTrue(any(d in portfolio["lastReview"] for d in ["2026-10-08", "2026-10-06"]))

        holdings = portfolio.get("holdings", [])
        self.assertEqual(len(holdings), 2, "Portfolio must contain exactly 2 pair holdings")

        sq = next((h for h in holdings if h.get("id") == "SK_SQUARE"), None)
        hy = next((h for h in holdings if h.get("id") == "SK_HYNIX"), None)

        self.assertIsNotNone(sq)
        self.assertIsNotNone(hy)

        self.assertIn(sq["shares"], ["60주", "54주", "44주"])
        self.assertIn(sq["evalAmount"], ["약 6,930만 원", "약 6,237만 원", "약 5,082만 원"])
        self.assertIn(sq["weight"], ["79.1%", "77.3%", "58.1%"])

        self.assertIn(hy["shares"], ["10주", "20주"])
        self.assertIn(hy["evalAmount"], ["약 1,833만 원", "약 3,666만 원"])
        self.assertIn(hy["weight"], ["20.9%", "22.7%", "41.9%"])


class TestIndexHtmlKpiRibbonMarkupAndScript(unittest.TestCase):
    """R1, R3: index.html 4 KPI ribbon DOM structure, Zero-CDN, and real-time JS functions."""

    def setUp(self) -> None:
        self.assertTrue(INDEX_HTML_PATH.exists(), f"index.html must exist at {INDEX_HTML_PATH}")
        self.html = INDEX_HTML_PATH.read_text(encoding="utf-8")

    def test_four_kpi_cards_dom_elements_present(self) -> None:
        """All 4 top KPI cards and their dynamic value/subtext elements must be present."""
        # Card 1: Total Portfolio Valuation
        self.assertIn('id="portfolioDiagnosticCard"', self.html)
        self.assertIn('id="kpiTotalValuation"', self.html)
        self.assertIn('id="kpiValuationSub"', self.html)

        # Card 2: Pair Allocation Ratio
        self.assertIn('id="kpiPairRatioText"', self.html)
        self.assertIn('id="kpiBarSquare"', self.html)
        self.assertIn('id="kpiBarHynix"', self.html)
        self.assertIn('id="kpiPairRatioSub"', self.html)

        # Card 3: Nomura CSI Shortage Index
        self.assertIn('id="macroOverviewCard"', self.html)
        self.assertIn('id="kpiMacroValue"', self.html)
        self.assertIn('id="kpiMacroSub"', self.html)
        self.assertIn('id="kpiMacroBadge"', self.html)

        # Card 4: Tactical Action Guide Pulse
        self.assertIn('id="kpiTacticalPulseBadge"', self.html)
        self.assertIn('id="kpiTacticalActionLabel"', self.html)
        self.assertIn('id="kpiTacticalValue"', self.html)
        self.assertIn('id="kpiTacticalSub"', self.html)

    def test_dynamic_recalculation_js_functions_present(self) -> None:
        """index.html must contain updateTopKpiRibbon and resolvePairStockPrices with USER_POSITIONS."""
        self.assertIn("function updateTopKpiRibbon", self.html)
        self.assertIn("function resolvePairStockPrices", self.html)
        self.assertIn("USER_POSITIONS", self.html)
        self.assertTrue("SK_SQUARE: 60" in self.html or "SK_SQUARE: 44" in self.html)
        self.assertIn("SK_HYNIX: 10", self.html)

    def test_date_handlers_trigger_update_top_kpi_ribbon(self) -> None:
        """Date change and navigation handlers must invoke updateTopKpiRibbon."""
        self.assertIn("updateTopKpiRibbon(newDate", self.html)
        self.assertIn("updateTopKpiRibbon(Terminal.selectedDate", self.html)

    def test_zero_cdn_offline_isolation(self) -> None:
        """index.html must have 0 external CDNs or remote URLs."""
        external_urls = re.findall(r'<script[^>]+src=["\'](https?://[^"\']+)["\']', self.html, re.IGNORECASE)
        external_links = re.findall(r'<link[^>]+href=["\'](https?://[^"\']+)["\']', self.html, re.IGNORECASE)
        self.assertEqual(external_urls + external_links, [], "index.html must contain zero remote CDN links")


class TestPairPortfolioMathematicalAccuracy(unittest.TestCase):
    """Mathematical validation for user confirmed position (44 shares SQ + 20 shares HY)."""

    def test_latest_20261006_math(self) -> None:
        """44 shares * 1,155,000 KRW + 20 shares * 1,833,000 KRW = 87,480,000 KRW (58.1% : 41.9%)."""
        sq_shares = 44
        sq_price = 1155000
        hy_shares = 20
        hy_price = 1833000

        sq_eval = sq_shares * sq_price
        hy_eval = hy_shares * hy_price
        total_eval = sq_eval + hy_eval

        self.assertEqual(sq_eval, 50820000)
        self.assertEqual(hy_eval, 36660000)
        self.assertEqual(total_eval, 87480000)

        sq_w = (sq_eval / total_eval) * 100
        hy_w = (hy_eval / total_eval) * 100

        self.assertAlmostEqual(sq_w, 58.1, places=1)
        self.assertAlmostEqual(hy_w, 41.9, places=1)

        # Rounded display
        approx_manwon = round(total_eval / 500000) * 50
        self.assertEqual(approx_manwon, 8750)

    def test_baseline_20260930_math(self) -> None:
        """44 shares * 1,092,727 KRW + 20 shares * 1,767,000 KRW = 83,420,000 KRW (57.6% : 42.3%)."""
        sq_eval = 48080000
        hy_eval = 35340000
        total_eval = sq_eval + hy_eval

        self.assertEqual(total_eval, 83420000)

        sq_w = (sq_eval / total_eval) * 100
        hy_w = (hy_eval / total_eval) * 100

        self.assertAlmostEqual(sq_w, 57.6, delta=0.1)
        self.assertAlmostEqual(hy_w, 42.3, delta=0.1)

        approx_manwon = round(total_eval / 500000) * 50
        self.assertEqual(approx_manwon, 8350)

    def test_updated_20261008_math(self) -> None:
        """60 shares * 1,155,000 KRW + 10 shares * 1,833,000 KRW = 87,630,000 KRW (79.1% : 20.9%)."""
        sq_shares = 60
        sq_price = 1155000
        hy_shares = 10
        hy_price = 1833000

        sq_eval = sq_shares * sq_price
        hy_eval = hy_shares * hy_price
        total_eval = sq_eval + hy_eval

        self.assertEqual(sq_eval, 69300000)
        self.assertEqual(hy_eval, 18330000)
        self.assertEqual(total_eval, 87630000)

        sq_w = (sq_eval / total_eval) * 100
        hy_w = (hy_eval / total_eval) * 100

        self.assertAlmostEqual(sq_w, 79.1, places=1)
        self.assertAlmostEqual(hy_w, 20.9, places=1)

        approx_manwon = round(total_eval / 500000) * 50
        self.assertEqual(approx_manwon, 8750)


class TestPortfolioAdversarialEdgeCases(unittest.TestCase):
    """Adversarial validation for sync_dashboard resilience, edge cases, and cross-view sync."""

    def setUp(self) -> None:
        self.raw_html = INDEX_HTML_PATH.read_text(encoding="utf-8")

    def test_sync_dashboard_resilience_when_pair_strategy_is_none(self) -> None:
        """sync_dashboard.update_data_store_with_market_data must not crash if pair_strategy is None."""
        from engine.models import DailyMarketData
        from engine.sync_dashboard import update_data_store_with_market_data

        md = DailyMarketData(date="2026-10-07")
        md.pair_strategy = None

        data_store: dict = {}
        res = update_data_store_with_market_data(data_store, md)
        self.assertIn("portfolio", res)
        self.assertEqual(res["portfolio"]["totalValue"], "약 8,750만 원")
        self.assertEqual(len(res["portfolio"]["holdings"]), 2)

    def test_unregistered_future_and_empty_date_resolution_logic(self) -> None:
        """resolvePairStockPrices must handle unregistered future dates, empty string, and null gracefully."""
        self.assertIn("targetDate", self.raw_html)
        self.assertIn("val >= 200000", self.raw_html)
        self.assertIn("!targetDate || targetDate >= \"2026-10-01\"", self.raw_html)

    def test_selector_cross_synchronization_in_handlers(self) -> None:
        """Both digestDateSelect and insightDateSelect must be synchronized on date navigation."""
        self.assertIn("const insightSelect = document.getElementById(\"insightDateSelect\");", self.raw_html)
        self.assertIn("const digestSelect = document.getElementById(\"digestDateSelect\");", self.raw_html)

    def test_tactical_action_pulse_label_dynamic_derivation(self) -> None:
        """Card 4 pulseLabel must be dynamically derived from pair.action or pair.actionLabel."""
        self.assertIn("pair.action", self.raw_html)
        self.assertIn("replace(/_POSITION$/, \"\")", self.raw_html)
        self.assertIn("kpiTacticalAction.innerText = pulseLabel", self.raw_html)

    def test_synthesize_digest_fallback_in_update_top_kpi_ribbon(self) -> None:
        """updateTopKpiRibbon must fall back to synthesizeDigestFromRecords when dailyDigests entry is absent."""
        self.assertIn("synthesizeDigestFromRecords(targetDate, dataStore)", self.raw_html)

    def test_pulse_label_avoids_false_switch_on_hold_guidance(self) -> None:
        """Card 4 pulseLabel must map '스위칭 보류' to HOLD, not mistakenly trigger SWITCH."""
        self.assertIn("보류|유지|관망|HOLD", self.raw_html)
        idx_hold = self.raw_html.find("보류|유지|관망|HOLD")
        idx_switch = self.raw_html.find("스위칭|SWITCH", idx_hold)
        self.assertGreater(idx_switch, idx_hold, "HOLD/보류 guard must precede SWITCH match")

    def test_navigation_handlers_contain_non_freeze_fallback(self) -> None:
        """Date navigation must use fallback findIndex so -1 index does not freeze UI."""
        self.assertIn("findIndex(d => d <= Terminal.selectedDate)", self.raw_html)

    def test_insight_view_synchronizes_top_kpi_ribbon(self) -> None:
        """renderInsightView must invoke updateTopKpiRibbon."""
        self.assertIn("function renderInsightView", self.raw_html)
        idx_fn = self.raw_html.find("function renderInsightView")
        idx_call = self.raw_html.find("updateTopKpiRibbon(date, dataStore)", idx_fn)
        self.assertNotEqual(idx_call, -1)
        self.assertLess(idx_call - idx_fn, 500)

    def test_sync_dashboard_recomputes_total_value_from_holdings_eval(self) -> None:
        """sync_dashboard must dynamically update totalValue from holdings evalAmount on active review date."""
        from engine.models import DailyMarketData, PortfolioPairStrategy
        from engine.sync_dashboard import update_data_store_with_market_data

        md = DailyMarketData(date="2026-10-07")
        strat = PortfolioPairStrategy(
            date="2026-10-07",
            sk_square_weight=57.6,
            sk_hynix_weight=42.4,
            action_label="스위칭 보류 / 코어 에셋 유지",
            risk_warning="역스위칭 리스크 경고",
            holdings_summary={
                "SK_SQUARE": {"shares": "44주", "eval_krw": "약 4,808만 원", "return_rate": "-0.6%"},
                "SK_HYNIX": {"shares": "20주", "eval_krw": "약 3,534만 원", "return_rate": "-5.6%"},
            }
        )
        md.pair_strategy = strat

        data_store: dict = {}
        res = update_data_store_with_market_data(data_store, md)
        self.assertEqual(res["portfolio"]["totalValue"], "약 8,350만 원")
        self.assertIn("2026-10-07", res["portfolio"]["lastReview"])

    def test_switch_view_synchronizes_top_kpi_ribbon(self) -> None:
        """switchView must invoke updateTopKpiRibbon to refresh ribbon on any view change."""
        self.assertIn("function switchView", self.raw_html)
        idx_fn = self.raw_html.find("function switchView")
        idx_call = self.raw_html.find("updateTopKpiRibbon(Terminal.selectedDate, window.WATCHLIST_DATA)", idx_fn)
        self.assertNotEqual(idx_call, -1)
        self.assertLess(idx_call - idx_fn, 300)

    def test_insight_dates_fully_synchronized_with_terminal_dates(self) -> None:
        """Terminal.insightDates must mirror Terminal.dates to prevent dropdown desynchronization."""
        self.assertIn("Terminal.insightDates = [...Terminal.dates];", self.raw_html)

    def test_all_historical_and_latest_dates_yield_exact_kpi_math(self) -> None:
        """Every date in PAIR_DOMESTIC_PRICE_TABLE must yield mathematically accurate KRW totals and ratios."""
        self.assertIn("const PAIR_DOMESTIC_PRICE_TABLE =", self.raw_html)
        entries = re.findall(
            r'["\'](\d{4}-\d{2}-\d{2})["\']\s*:\s*{\s*sq\s*:\s*(\d+)\s*,\s*hy\s*:\s*(\d+)\s*}',
            self.raw_html
        )
        self.assertGreaterEqual(len(entries), 6, "Must define at least 6 canonical dates")

        shares_sq = 44
        shares_hy = 20

        for date_str, sq_p, hy_p in entries:
            sq_price = int(sq_p)
            hy_price = int(hy_p)
            total_eval = (shares_sq * sq_price) + (shares_hy * hy_price)
            sq_w = (shares_sq * sq_price / total_eval) * 100
            hy_w = (shares_hy * hy_price / total_eval) * 100
            manwon = round(total_eval / 500000) * 50

            if date_str >= "2026-10-01":
                self.assertEqual(manwon, 8750, f"{date_str} must be approx 8,750만 원")
                self.assertAlmostEqual(sq_w, 58.1, places=1)
                self.assertAlmostEqual(hy_w, 41.9, places=1)
            else:
                self.assertEqual(manwon, 8350, f"{date_str} must be approx 8,350만 원")
                self.assertAlmostEqual(sq_w, 57.6, delta=0.1)
                self.assertAlmostEqual(hy_w, 42.4, delta=0.1)

    def test_pair_domestic_price_table_complete(self) -> None:
        """PAIR_DOMESTIC_PRICE_TABLE must include all dates present in data.js dailyDigests."""
        from engine.sync_dashboard import parse_js_data_store
        data_store = parse_js_data_store(DATA_JS_PATH.read_text(encoding="utf-8"))
        digest_dates = [d["date"] for d in data_store.get("dailyDigests", []) if d.get("date")]
        self.assertTrue(len(digest_dates) >= 6)
        for d in digest_dates:
            self.assertIn(f'"{d}"', self.raw_html, f"Date {d} must be mapped in PAIR_DOMESTIC_PRICE_TABLE")


if __name__ == "__main__":
    unittest.main()


