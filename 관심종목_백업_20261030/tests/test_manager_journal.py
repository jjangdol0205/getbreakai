"""Comprehensive Acceptance Criteria & Adversarial Verification Suite for AI Fund Manager Journal.

Tests for Milestone 4:
- AC1: Manager Reasoning Engine & Proposal Logic Consistency (Benjamin Graham floor + Jesse Livermore
       catalyst 30~60d + Volume Wash-Out trigger synthesis; SK Square 76 shares exact math: 8,284만 원,
       109만 원, 105만 원, TP1 218만 원 38 shares sold -> 8,284만 원 100% recovery; Time-to-100% ranking;
       tactical switching; reverse switching defense; dead money warnings).
- AC2: Daily Permanent Archiving Pipeline (data.js managerJournal schema, idempotent in-place updates,
       markdown sections in daily_digest.md and daily_insight.md).
- AC3: Dashboard UI & Offline Zero-CDN Integrity (managerTodayProposalCard, managerJournalTimelineCard,
       14 baseline View 5 DOM IDs preserved, zero CDN/remote imports).
- AC4: Adversarial Stress & Edge Cases (None/corrupted inputs, boundary conditions, zero-division guards).
"""

from __future__ import annotations

from copy import deepcopy
from datetime import datetime, date as dt_date
import json
from pathlib import Path
import re
from typing import Any, Dict, List, Optional
import unittest

from engine.models import (
    StockSymbol,
    STOCK_MASTERS,
    DailyMarketData,
    StockFactSheet,
    MarketMetrics,
)
from engine.timing_engine import (
    TimingEngine,
    FundManagerProposal,
    PortfolioDiagnostic,
    SwitchingActionScenario,
    RiskManagementAlert,
    DailyTimingSnapshot,
    StockTimingEvaluation,
    SwitchingRecommendation,
    ValuationBandConfig,
    CatalystEvent,
    TakeProfitConfig,
    CompositeTriggerResult,
    STOCK_REFERENCE_PRICES,
    STOCK_BENCHMARK_20D_VOLUME,
)
from engine.sync_dashboard import (
    build_manager_journal_store,
    create_default_manager_journal_store,
    build_digest_entry,
)
from engine.digest_generator import DigestGenerator
from engine.insight_generator import InsightGenerator

REPO_ROOT = Path(__file__).resolve().parent.parent
INDEX_HTML = REPO_ROOT / "index.html"
DATA_JS = REPO_ROOT / "data.js"


def parse_watchlist_data_from_js(js_path: Path) -> Dict[str, Any]:
    """Safely extracts window.WATCHLIST_DATA JSON object from data.js."""
    content = js_path.read_text(encoding="utf-8").strip()
    match = re.search(r"window\.WATCHLIST_DATA\s*=\s*(\{[\s\S]*\});?\s*$", content)
    if not match:
        raise ValueError("Could not find window.WATCHLIST_DATA assignment in data.js")
    return json.loads(match.group(1))


# ==============================================================================
# AC1: Manager Reasoning Engine & Proposal Logic Consistency
# ==============================================================================

class TestManagerReasoningEngineAC1(unittest.TestCase):
    """Verifies Benjamin Graham intrinsic floor + Jesse Livermore timing trigger synthesis,

    exact SK Square 76 shares math, Time-to-100% velocity ranking, and risk guardrails.
    """

    def setUp(self) -> None:
        self.eval_date = "2026-10-12"
        self.portfolio_sk_square = {
            "holdingStock": "SK_SQUARE",
            "shares": 76,
            "principal": 82840000,
            "avgCost": 1090000,
            "currentPrice": 1050000.0,
        }

    def test_manager_persona_and_horizon_objective(self) -> None:
        """AC1.1: Verify fund manager persona, 1~2 year investment horizon, and TP1 objective."""
        proposal = TimingEngine.generate_manager_proposal(
            date=self.eval_date,
            portfolio=self.portfolio_sk_square,
        )

        self.assertIsInstance(proposal, FundManagerProposal)
        self.assertEqual(proposal.date, self.eval_date)
        self.assertEqual(proposal.manager_persona, "가치투자 + 타이밍 천재 수석 펀드매니저 AI")
        self.assertEqual(proposal.investment_horizon, "1~2년 (Big Wave & 100%+ 수익률 추구)")
        self.assertEqual(
            proposal.target_objective,
            "TP1(218만 원) 38주 매도로 매수 원금 8,284만 원 100% 무위험 회수",
        )

    def test_sk_square_76_shares_exact_mathematics(self) -> None:
        """AC1.2: Strict verification of SK Square 76 shares mathematics:

        - 76 shares, 82,840,000 KRW principal, 1,090,000 KRW avg cost, 1,050,000 KRW current price.
        - Valuation: 76 * 1,050,000 = 79,800,000 KRW (7,980만 원).
        - PnL: 79,800,000 - 82,840,000 = -3,040,000 KRW (-3.67%).
        - TP1: 2,180,000 KRW (218만 원).
        - TP1 execution: selling 38 shares recovers 38 * 2,180,000 = 82,840,000 KRW (100.0% recovery!).
        - Remaining 38 shares enter Risk-Free status with cost basis 0 KRW.
        - Progress: 1,050,000 / 2,180,000 = 48.2%.
        """
        proposal = TimingEngine.generate_manager_proposal(
            date=self.eval_date,
            portfolio=self.portfolio_sk_square,
            current_price=1050000.0,
        )

        diag = proposal.core_holding
        self.assertIsInstance(diag, PortfolioDiagnostic)
        self.assertEqual(diag.stock_id, "SK_SQUARE")
        self.assertEqual(diag.stock_name, "SK스퀘어")
        self.assertEqual(diag.shares, 76)
        self.assertEqual(diag.principal_krw, 82840000)
        self.assertEqual(diag.avg_cost_krw, 1090000)
        self.assertEqual(diag.current_price, 1050000.0)

        # Exact calculated math
        expected_valuation = 76 * 1050000  # 79,800,000
        self.assertEqual(diag.current_valuation_krw, expected_valuation)
        self.assertEqual(diag.pnl_amount_krw, expected_valuation - 82840000)  # -3,040,000
        self.assertAlmostEqual(diag.pnl_rate_pct, -3.67, places=2)

        # TP1 roadmap math
        self.assertEqual(diag.tp1_target_price, 2180000.0)
        self.assertEqual(diag.tp1_shares_to_sell, 38)
        self.assertEqual(diag.tp1_shares_to_sell * diag.tp1_target_price, diag.principal_krw)
        self.assertEqual(diag.tp1_recovered_amount, 82840000)
        self.assertEqual(diag.shares - diag.tp1_shares_to_sell, 38)
        self.assertAlmostEqual(diag.tp1_progress_pct, 48.2, places=1)

        # Dict representation consistency
        diag_dict = diag.to_dict()
        self.assertEqual(diag_dict["principalFormatted"], "8,284만 원")
        self.assertEqual(diag_dict["currentValuationFormatted"], "7,980만 원")
        self.assertEqual(diag_dict["tp1RecoveredFormatted"], "8,284만 원")
        self.assertIn("100% 무위험(Risk-Free) 회수", diag.recovery_roadmap)

    def test_four_pillar_deep_reasoning_synthesis(self) -> None:
        """AC1.3: Verify 4-pillar deep reasoning synthesis:

        1. Graham Value Floor (NAV discount, intrinsic value, support floor)
        2. Livermore Catalyst Timing (30~60d clusters, share buyback cancellation)
        3. Volume Wash-Out Dynamics (ADR lockup wash-out, support rebound)
        4. Risk-Reward Assessment (15.0+ RRR, -6.7% downside vs +107.6% upside)
        """
        proposal = TimingEngine.generate_manager_proposal(
            date=self.eval_date,
            portfolio=self.portfolio_sk_square,
        )

        pillars = proposal.reasoning_pillars
        self.assertIn("valuation_thesis", pillars)
        self.assertIn("catalyst_timing", pillars)
        self.assertIn("volume_supply_dynamics", pillars)
        self.assertIn("risk_reward_assessment", pillars)

        # Content validations
        self.assertIn("NAV", pillars["valuation_thesis"])
        self.assertIn("솔리다임", pillars["valuation_thesis"])
        self.assertIn("안전마진", pillars["valuation_thesis"])

        self.assertIn("리버모어", pillars["catalyst_timing"])
        self.assertIn("소각", pillars["catalyst_timing"])

        self.assertIn("Wash-out", pillars["volume_supply_dynamics"])
        self.assertIn("지지선", pillars["volume_supply_dynamics"])

        self.assertIn("8,284만 원", pillars["risk_reward_assessment"])
        self.assertIn("38주", pillars["risk_reward_assessment"])
        self.assertIn("218만 원", pillars["risk_reward_assessment"])

    def test_time_to_100_ranking_covers_all_8_stocks_in_velocity_order(self) -> None:
        """AC1.4: Verify Time-to-100% velocity ranking covers all 8 canonical stocks

        strictly sorted in descending order of speedScore with valid ratings and horizons.
        """
        proposal = TimingEngine.generate_manager_proposal(
            date=self.eval_date,
            portfolio=self.portfolio_sk_square,
        )

        ranking = proposal.time_to_100_ranking
        self.assertEqual(len(ranking), 8)

        expected_stocks = {
            "SK_HYNIX", "SK_SQUARE", "UBER", "MBLY", "FLNC", "UPST", "CELH", "ENPH"
        }
        actual_stocks = {item["stockId"] for item in ranking}
        self.assertEqual(actual_stocks, expected_stocks)

        # Check strict descending sort by speedScore
        scores = [item["speedScore"] for item in ranking]
        self.assertEqual(scores, sorted(scores, reverse=True))

        # Check consecutive rank numbering 1 to 8
        ranks = [item["rank"] for item in ranking]
        self.assertEqual(ranks, list(range(1, 9)))

        # Check schema of each ranking item
        for item in ranking:
            self.assertIn("stockId", item)
            self.assertIn("stockName", item)
            self.assertIn("ticker", item)
            self.assertIn("currentPrice", item)
            self.assertIn("tp1Target", item)
            self.assertIn("upsideTp1", item)
            self.assertIn("nearestCatalystDDay", item)
            self.assertIn("compositeScore", item)
            self.assertIn("riskRewardRatio", item)
            self.assertIn("speedScore", item)
            self.assertIn(item["timeTo100Rating"], {"FAST", "MODERATE", "SLOW"})
            self.assertIn(item["estimatedTime"], {"6~12개월", "1~2년", "2년 이상 / 촉매 대기"})

    def test_reverse_switching_defense_when_catalyst_due_within_20_days(self) -> None:
        """AC1.5: Strict defense against switching when holding catalyst D-Day <= 20.

        Holding 76 shares SK Square must be fiercely defended against premature switching.
        """
        # SK Square has catalysts on 2026-10-28 (D-16 from 2026-10-12), which is <= 20 days.
        proposal = TimingEngine.generate_manager_proposal(
            date="2026-10-12",
            portfolio=self.portfolio_sk_square,
            current_price=1050000.0,
        )

        self.assertEqual(proposal.tactical_action, "REVERSE_SWITCH_WARNING")
        self.assertIn("역(逆)스위칭 엄금 경고", proposal.action_headline)
        self.assertIn("76주 코어 홀딩 결사 사수", proposal.action_headline)
        self.assertIn("물량을 털리는", proposal.executive_summary)

        # Check critical alert in risk warnings
        critical_alerts = [
            w for w in proposal.risk_warnings
            if w.alert_type == "REVERSE_SWITCH_DEFENSE" and w.severity == "CRITICAL"
        ]
        self.assertTrue(len(critical_alerts) >= 1)
        self.assertIn("역스위칭 발생 위험 최고조", critical_alerts[0].message)
        self.assertIn("76주 전량 홀딩 유지", critical_alerts[0].action_guideline)

    def test_tactical_partial_switching_scenario_generation(self) -> None:
        """AC1.6: Verify tactical partial switching when candidate is faster and holding catalyst > 20."""
        # Provide an evaluation set where holding has catalyst far in the future (> 20 days)
        # and candidate (UBER) has SWITCH_OPPORTUNITY
        eval_date = "2026-10-12"
        evals = {}
        for sid in STOCK_MASTERS:
            evals[sid] = TimingEngine.evaluate_stock(
                stock_id=sid,
                current_price=STOCK_REFERENCE_PRICES[sid],
                date=eval_date,
            )

        # Force SK Square catalyst far away (D-45)
        sq_eval = deepcopy(evals["SK_SQUARE"])
        sq_eval.catalysts = [
            CatalystEvent(
                name="원거리 촉매",
                target_date="2026-11-26",
                days_remaining=45,
                impact_level="HIGH",
                description="45일 후 촉매",
            )
        ]
        evals["SK_SQUARE"] = sq_eval

        # Create a switching recommendation indicating SWITCH_OPPORTUNITY for UBER
        switching_rec = SwitchingRecommendation(
            holding_stock_id="SK_SQUARE",
            holding_shares=76,
            holding_price=1050000.0,
            holding_eval_amount="7,980만 원",
            holding_rrr=15.0,
            holding_catalyst_d_day=45,
            status="SWITCH_OPPORTUNITY",
            summary="우버가 촉매 D-10으로 임박",
            top_candidate_id="UBER",
            candidates=[],
            scenarios=[],
        )

        proposal = TimingEngine.generate_manager_proposal(
            evaluations=evals,
            switching=switching_rec,
            portfolio={"holdingStock": "SK_SQUARE", "shares": 76, "currentPrice": 1050000.0},
            date=eval_date,
        )

        self.assertEqual(proposal.tactical_action, "TACTICAL_SWITCH")
        self.assertIn("전술적 부분 스위칭 제안", proposal.action_headline)
        self.assertIsNotNone(proposal.switching_proposal)
        sp = proposal.switching_proposal
        self.assertEqual(sp.candidate_id, "UBER")
        self.assertEqual(sp.shares_to_sell, 10)
        self.assertEqual(sp.freed_capital_krw, 10 * 1050000)
        self.assertTrue(sp.candidate_shares_to_buy > 0)

    def test_dead_money_risk_warnings_emitted(self) -> None:
        """AC1.7: Verify dead money warnings are emitted for stocks in safety margin lacking catalysts."""
        proposal = TimingEngine.generate_manager_proposal(
            date=self.eval_date,
            portfolio=self.portfolio_sk_square,
        )

        dead_money_alerts = [
            w for w in proposal.risk_warnings
            if w.alert_type == "DEAD_MONEY"
        ]
        # Any stock evaluated as HIGH dead money must have warning
        for alert in dead_money_alerts:
            self.assertEqual(alert.severity, "WARNING")
            self.assertIn("자금 정체(Dead Money) 위험 높음", alert.message)
            self.assertIn("선취매를 자제", alert.action_guideline)

    def test_tp1_achieved_transition(self) -> None:
        """AC1.8: When SK Square reaches TP1 (>= 2,180,000 KRW), engine signals TP1 execution."""
        portfolio_tp1 = {
            "holdingStock": "SK_SQUARE",
            "shares": 76,
            "principal": 82840000,
            "currentPrice": 2180000.0,
        }
        proposal = TimingEngine.generate_manager_proposal(
            date=self.eval_date,
            portfolio=portfolio_tp1,
            current_price=2180000.0,
        )

        self.assertEqual(proposal.tactical_action, "TAKE_PROFIT_TP1")
        self.assertIn("TP1(218만 원) 달성", proposal.action_headline)
        self.assertIn("38주 분할 매도로 원금 8,284만 원 100% 무위험 회수 실행", proposal.action_headline)
        self.assertEqual(proposal.core_holding.status_phase, "TP1_REACHED_EXECUTE_SELL_38")
        self.assertAlmostEqual(proposal.core_holding.tp1_progress_pct, 100.0, places=1)


# ==============================================================================
# AC2: Daily Permanent Archiving Pipeline
# ==============================================================================

class TestManagerJournalArchivingPipelineAC2(unittest.TestCase):
    """Verifies managerJournal data.js store creation, in-place idempotence,

    and permanent markdown section generation in daily_digest.md and daily_insight.md.
    """

    def setUp(self) -> None:
        self.test_date = "2026-10-12"

    def test_build_manager_journal_store_schema(self) -> None:
        """AC2.1: Verify build_manager_journal_store produces lastEvaluated, todayProposal, history."""
        store = build_manager_journal_store(
            existing_journal_store=None,
            today_str=self.test_date,
        )

        self.assertIn("lastEvaluated", store)
        self.assertIn("todayProposal", store)
        self.assertIn("history", store)
        self.assertEqual(store["lastEvaluated"], self.test_date)
        self.assertIsInstance(store["history"], list)
        self.assertTrue(len(store["history"]) >= 1)

        tp = store["todayProposal"]
        self.assertIsInstance(tp, dict)
        self.assertEqual(tp["date"], self.test_date)
        self.assertEqual(tp["managerPersona"], "가치투자 + 타이밍 천재 수석 펀드매니저 AI")
        self.assertIn("TP1(218만 원) 38주 매도로 매수 원금 8,284만 원 100% 무위험", tp["targetObjective"])

        ch = tp["coreHolding"]
        self.assertEqual(ch["shares"], 76)
        self.assertEqual(ch["principalKrw"], 82840000)
        self.assertEqual(ch["tp1SharesToSell"], 38)
        self.assertEqual(ch["tp1RecoveredAmount"], 82840000)

    def test_idempotent_in_place_updates_no_duplicates(self) -> None:
        """AC2.2: Verify multiple sync runs on the same date update in-place without duplicating records."""
        # Initial run on 2026-10-12
        store_1 = build_manager_journal_store(
            existing_journal_store=None,
            today_str="2026-10-12",
        )
        count_1 = len(store_1["history"])
        self.assertEqual(count_1, 1)
        first_timestamp = store_1["history"][0]["timestamp"]

        # Run 2 on same date
        store_2 = build_manager_journal_store(
            existing_journal_store=store_1,
            today_str="2026-10-12",
        )
        count_2 = len(store_2["history"])
        self.assertEqual(count_2, 1, "Running sync on the same date must NOT duplicate history entries")
        self.assertEqual(store_2["history"][0]["date"], "2026-10-12")

        # Run 3 on same date with specific proposal modification
        custom_proposal = TimingEngine.generate_manager_proposal(date="2026-10-12")
        custom_proposal.action_headline = "MODIFIED_IN_PLACE_HEADLINE"
        store_3 = build_manager_journal_store(
            existing_journal_store=store_2,
            manager_proposal=custom_proposal,
            today_str="2026-10-12",
        )
        self.assertEqual(len(store_3["history"]), 1)
        self.assertEqual(store_3["history"][0]["actionHeadline"], "MODIFIED_IN_PLACE_HEADLINE")
        self.assertEqual(store_3["todayProposal"]["actionHeadline"], "MODIFIED_IN_PLACE_HEADLINE")

    def test_multi_date_chronological_history_accumulation(self) -> None:
        """AC2.3: Verify multi-date history records accumulate properly and sort reverse-chronologically."""
        # Day 1: 2026-10-01
        store = build_manager_journal_store(existing_journal_store=None, today_str="2026-10-01")
        self.assertEqual(len(store["history"]), 1)

        # Day 2: 2026-10-06
        store = build_manager_journal_store(existing_journal_store=store, today_str="2026-10-06")
        self.assertEqual(len(store["history"]), 2)

        # Day 3: 2026-10-12
        store = build_manager_journal_store(existing_journal_store=store, today_str="2026-10-12")
        self.assertEqual(len(store["history"]), 3)

        # Verify reverse-chronological order: 2026-10-12, 2026-10-06, 2026-10-01
        dates = [item["date"] for item in store["history"]]
        self.assertEqual(dates, ["2026-10-12", "2026-10-06", "2026-10-01"])

        # Re-running 2026-10-06 in between must update in place and keep 3 entries
        store = build_manager_journal_store(existing_journal_store=store, today_str="2026-10-06")
        self.assertEqual(len(store["history"]), 3)
        dates_after = [item["date"] for item in store["history"]]
        self.assertEqual(dates_after, ["2026-10-12", "2026-10-06", "2026-10-01"])

    def test_daily_digest_contains_manager_proposal_subsection(self) -> None:
        """AC2.4: Verify daily_digest.md includes subsection 4.0:

        '### 🧠 AI 수석 펀드매니저의 일일 전략 제안 및 타점 진단'
        with SK Square 76 shares math and Time-to-100% velocity ranking.
        """
        generator = DigestGenerator()
        m = STOCK_MASTERS["SK_SQUARE"]
        market_data = DailyMarketData(
            date="2026-10-12",
            stocks={
                "SK_SQUARE": StockFactSheet(
                    stock_id=m.stock_id,
                    stock_name=m.name_kr,
                    name_kr=m.name_kr,
                    name_en=m.name_en,
                    ticker=m.ticker,
                    market=m.market,
                    category=m.category,
                    badge_color=m.badge_color,
                    metrics=MarketMetrics(stock_id=m.stock_id, close_price=1050000.0, volume=120000),
                )
            },
        )

        digest_md = generator.generate(market_data)

        # Section header check
        self.assertIn("### 🧠 AI 수석 펀드매니저의 일일 전략 제안 및 타점 진단", digest_md)
        # Math content check
        self.assertIn("SK스퀘어 76주", digest_md)
        self.assertIn("8,284만 원", digest_md)
        self.assertIn("38주", digest_md)
        self.assertIn("2,180,000원", digest_md)
        self.assertIn("100% 무위험 회수", digest_md)

    def test_daily_insight_contains_manager_journal_section(self) -> None:
        """AC2.5: Verify daily_insight.md includes Section 5:

        '## 5. AI 수석 펀드매니저의 일일 전략 제안 및 타점 진단 (Manager's Daily Journal)'
        with 4 reasoning pillars and risk guardrails.
        """
        generator = InsightGenerator()
        m = STOCK_MASTERS["SK_SQUARE"]
        market_data = DailyMarketData(
            date="2026-10-12",
            stocks={
                "SK_SQUARE": StockFactSheet(
                    stock_id=m.stock_id,
                    stock_name=m.name_kr,
                    name_kr=m.name_kr,
                    name_en=m.name_en,
                    ticker=m.ticker,
                    market=m.market,
                    category=m.category,
                    badge_color=m.badge_color,
                    metrics=MarketMetrics(stock_id=m.stock_id, close_price=1050000.0, volume=120000),
                )
            },
        )

        insight_md = generator.build_markdown(market_data)

        # Section header check
        self.assertIn(
            "## 5. AI 수석 펀드매니저의 일일 전략 제안 및 타점 진단 (Manager's Daily Journal)",
            insight_md,
        )
        # Content checks
        self.assertIn("그레이엄", insight_md)
        self.assertIn("리버모어", insight_md)
        self.assertIn("8,284만 원", insight_md)
        self.assertIn("38주", insight_md)
        self.assertIn("리스크 관리 경고", insight_md)


# ==============================================================================
# AC3: Dashboard UI & Offline Zero-CDN Integrity
# ==============================================================================

class TestDashboardUIAndOfflineIntegrityAC3(unittest.TestCase):
    """Verifies manager proposal cards, baseline 14 View 5 DOM IDs, controller functions,

    and strict 100% Zero-CDN offline compliance.
    """

    def setUp(self) -> None:
        self.html_content = INDEX_HTML.read_text(encoding="utf-8")
        self.data_js_content = DATA_JS.read_text(encoding="utf-8")
        self.watchlist_data = parse_watchlist_data_from_js(DATA_JS)

    def test_index_html_contains_manager_cards(self) -> None:
        """AC3.1: Verify index.html contains managerTodayProposalCard and managerJournalTimelineCard."""
        self.assertIn('id="managerTodayProposalCard"', self.html_content)
        self.assertIn('id="managerTodayProposalContent"', self.html_content)
        self.assertIn('id="managerJournalTimelineCard"', self.html_content)
        self.assertIn('id="managerJournalTimelineContent"', self.html_content)

    def test_all_14_baseline_view_5_dom_ids_preserved(self) -> None:
        """AC3.2: Verify all 14 baseline View 5 DOM IDs are preserved without regression."""
        required_view5_ids = [
            "btnViewTiming",
            "viewTimingSection",
            "timingKpiRibbon",
            "timingPortfolioDiagnosisCard",
            "portfolioDiagnosisContent",
            "timingSwitchingCard",
            "switchingCardContent",
            "timingGaugesGrid",
            "timingCatalystGrid",
            "timingDateSelect",
            "timingCoverageLabel",
            "timingHistoryTable",
            "timingHistoryTableBody",
            "timingStockPills",
        ]
        dom_ids = set(re.findall(r'\bid=["\']([^"\']+)["\']', self.html_content))
        for vid in required_view5_ids:
            self.assertIn(vid, dom_ids, f"Required View 5 DOM ID '{vid}' was lost in index.html!")

    def test_view_5_and_manager_controller_functions_declared(self) -> None:
        """AC3.3: Verify all controller functions for View 5 and manager journal are declared in inline scripts."""
        required_functions = [
            "renderTimingView",
            "getActiveTimingSnapshot",
            "renderTimingDateSelector",
            "handleTimingDateChange",
            "navigateTimingDate",
            "renderTimingStockPills",
            "setTimingStockFilter",
            "renderTimingKpiRibbon",
            "renderTimingPortfolioDiagnosis",
            "renderTimingSwitching",
            "renderTimingGauges",
            "renderTimingCatalysts",
            "renderTimingHistoryTimeline",
            "selectTimingHistoryDate",
            # Milestone 4 additions
            "renderManagerTodayProposalCard",
            "renderManagerJournalTimeline",
        ]

        # Extract all inline script blocks
        script_blocks = re.findall(r'<script(?![^>]*src)[^>]*>([\s\S]*?)</script>', self.html_content)
        combined_scripts = "\n".join(script_blocks)

        for fn in required_functions:
            pattern = rf'(?:function\s+{fn}\b|\b{fn}\s*=\s*(?:function|\([^)]*\)\s*=>)|window\.{fn}\s*=)'
            self.assertTrue(
                re.search(pattern, combined_scripts),
                f"Required controller function '{fn}' is missing from inline JavaScript!",
            )

    def test_strict_zero_cdn_offline_compliance(self) -> None:
        """AC3.4: Strict Zero-CDN verification: zero remote scripts, zero remote links, zero external CDNs."""
        # 1. No remote script tags
        script_srcs = re.findall(r'<script[^>]+src=["\']([^"\']+)["\']', self.html_content, re.IGNORECASE)
        for src in script_srcs:
            self.assertFalse(
                re.match(r"^(https?:)?//", src, re.IGNORECASE),
                f"Forbidden remote script found in index.html: {src}",
            )

        # 2. No remote stylesheet links
        link_hrefs = re.findall(r'<link[^>]+href=["\']([^"\']+)["\']', self.html_content, re.IGNORECASE)
        for href in link_hrefs:
            self.assertFalse(
                re.match(r"^(https?:)?//", href, re.IGNORECASE),
                f"Forbidden remote stylesheet link found in index.html: {href}",
            )

        # 3. No remote CSS @import
        css_imports = re.findall(r'@import\s+["\']?([^"\';]+)["\']?;', self.html_content, re.IGNORECASE)
        for imp in css_imports:
            self.assertFalse(
                re.match(r"^(https?:)?//", imp.strip(), re.IGNORECASE),
                f"Forbidden remote CSS @import found: {imp}",
            )

        # 4. No remote url() in styles
        style_urls = re.findall(r'url\s*\(\s*["\']?([^"\')]+)["\']?\s*\)', self.html_content, re.IGNORECASE)
        for u in style_urls:
            self.assertFalse(
                re.match(r"^(https?:)?//", u.strip(), re.IGNORECASE),
                f"Forbidden remote CSS url() found: {u}",
            )

        # 5. Check against known CDN domains
        known_cdns = [
            "cdn.jsdelivr.net",
            "cdnjs.cloudflare.com",
            "unpkg.com",
            "fonts.googleapis.com",
            "fonts.gstatic.com",
            "cdn.tailwindcss.com",
            "ajax.googleapis.com",
        ]
        for cdn in known_cdns:
            self.assertNotIn(cdn, self.html_content, f"Known CDN '{cdn}' detected in index.html")
            self.assertNotIn(cdn, self.data_js_content, f"Known CDN '{cdn}' detected in data.js")

        # 6. Local data.js loading check
        self.assertRegex(
            self.html_content,
            r'<script\s+src=["\']\./data\.js["\']>\s*</script>',
            "index.html must load ./data.js via relative local path",
        )

    def test_data_js_manager_journal_payload_integrity(self) -> None:
        """AC3.5: Verify data.js contains valid managerJournal store with todayProposal and history."""
        self.assertIn("managerJournal", self.watchlist_data)
        mj = self.watchlist_data["managerJournal"]
        self.assertIsInstance(mj, dict)
        self.assertIn("lastEvaluated", mj)
        self.assertIn("todayProposal", mj)
        self.assertIn("history", mj)

        tp = mj["todayProposal"]
        self.assertIsInstance(tp, dict)
        self.assertEqual(tp["managerPersona"], "가치투자 + 타이밍 천재 수석 펀드매니저 AI")

        # Math verification inside live data.js
        ch = tp["coreHolding"]
        self.assertEqual(ch["shares"], 76)
        self.assertEqual(ch["principalKrw"], 82840000)
        self.assertEqual(ch["tp1SharesToSell"], 38)
        self.assertEqual(ch["tp1RecoveredAmount"], 82840000)


# ==============================================================================
# AC4: Adversarial Stress & Edge Cases
# ==============================================================================

class TestManagerJournalAdversarialStressAC4(unittest.TestCase):
    """Adversarial stress-testing of proposal generation, edge conditions, and error paths."""

    def test_adversarial_none_and_empty_inputs(self) -> None:
        """AC4.1: Verify engine handles None and empty inputs without unhandled exceptions."""
        # Call with complete None
        prop_none = TimingEngine.generate_manager_proposal(
            evaluations=None,
            switching=None,
            portfolio=None,
            date=None,
            market_data=None,
        )
        self.assertIsInstance(prop_none, FundManagerProposal)
        self.assertEqual(prop_none.core_holding.shares, 76)
        self.assertEqual(prop_none.core_holding.principal_krw, 82840000)

        # Call with empty evaluations dict
        prop_empty_evals = TimingEngine.generate_manager_proposal(evaluations={})
        self.assertIsInstance(prop_empty_evals, FundManagerProposal)
        self.assertEqual(len(prop_empty_evals.time_to_100_ranking), 8)

    def test_adversarial_zero_division_guard(self) -> None:
        """AC4.2: Verify zero-division safety when portfolio has 0 shares or 0 principal."""
        prop_zeros = TimingEngine.generate_manager_proposal(
            portfolio={"holdingStock": "SK_SQUARE", "shares": 0, "principal": 0},
            current_price=0.0,
        )
        self.assertEqual(prop_zeros.core_holding.shares, 0)
        self.assertEqual(prop_zeros.core_holding.pnl_rate_pct, 0.0)

    def test_adversarial_corrupted_existing_history_store(self) -> None:
        """AC4.3: Verify build_manager_journal_store handles malformed existing stores."""
        malformed_inputs = [
            None,
            "",
            12345,
            {"history": "not_a_list"},
            {"history": [None, "invalid_item", 999]},
            [],
        ]
        for bad_store in malformed_inputs:
            store = build_manager_journal_store(
                existing_journal_store=bad_store,
                today_str="2026-10-12",
            )
            self.assertIsInstance(store, dict)
            self.assertIn("lastEvaluated", store)
            self.assertIn("todayProposal", store)
            self.assertIsInstance(store["history"], list)

    def test_support_breakdown_critical_alert(self) -> None:
        """AC4.4: Verify critical support defense alert when price drops below key support."""
        # Key support for SK Square is 980,000 KRW. Price 900,000 KRW breaches support.
        proposal = TimingEngine.generate_manager_proposal(
            portfolio={"holdingStock": "SK_SQUARE", "shares": 76, "principal": 82840000},
            current_price=900000.0,
        )
        support_alerts = [
            w for w in proposal.risk_warnings
            if w.alert_type == "SUPPORT_DEFENSE"
        ]
        self.assertTrue(len(support_alerts) >= 1)
        self.assertEqual(support_alerts[0].severity, "CRITICAL")
        self.assertIn("핵심 하방 지지선", support_alerts[0].message)

    def test_json_serialization_roundtrip_fidelity(self) -> None:
        """AC4.5: Verify proposal dictionary serializes cleanly to JSON without special character corruption."""
        proposal = TimingEngine.generate_manager_proposal(date="2026-10-12")
        prop_dict = proposal.to_dict()

        json_str = json.dumps(prop_dict, ensure_ascii=False)
        roundtrip = json.loads(json_str)

        self.assertEqual(roundtrip["managerPersona"], prop_dict["managerPersona"])
        self.assertEqual(roundtrip["coreHolding"]["principalKrw"], 82840000)
        self.assertEqual(roundtrip["coreHolding"]["tp1RecoveredAmount"], 82840000)
        self.assertEqual(len(roundtrip["timeTo100Ranking"]), 8)

    def test_reverse_switching_boundary_catalyst_days(self) -> None:
        """AC4.6: Verify exact boundary condition: D-Day <= 20 triggers defense, D-Day >= 21 does not."""
        eval_date = "2026-10-12"
        evals = {}
        for sid in STOCK_MASTERS:
            evals[sid] = TimingEngine.evaluate_stock(
                stock_id=sid,
                current_price=STOCK_REFERENCE_PRICES[sid],
                date=eval_date,
            )

        # Case A: Exactly D-20 -> must trigger REVERSE_SWITCH_WARNING
        sq_eval_d20 = deepcopy(evals["SK_SQUARE"])
        sq_eval_d20.catalysts = [
            CatalystEvent(
                name="경계선 촉매 D20",
                target_date="2026-11-01",
                days_remaining=20,
                impact_level="HIGH",
                description="20일 후 촉매",
            )
        ]
        evals_d20 = dict(evals)
        evals_d20["SK_SQUARE"] = sq_eval_d20

        prop_d20 = TimingEngine.generate_manager_proposal(
            evaluations=evals_d20,
            portfolio={"holdingStock": "SK_SQUARE", "shares": 76, "currentPrice": 1050000.0},
            date=eval_date,
        )
        self.assertEqual(prop_d20.tactical_action, "REVERSE_SWITCH_WARNING")

        # Case B: Exactly D-21 -> should NOT trigger REVERSE_SWITCH_WARNING
        sq_eval_d21 = deepcopy(evals["SK_SQUARE"])
        sq_eval_d21.catalysts = [
            CatalystEvent(
                name="경계선 촉매 D21",
                target_date="2026-11-02",
                days_remaining=21,
                impact_level="HIGH",
                description="21일 후 촉매",
            )
        ]
        evals_d21 = dict(evals)
        evals_d21["SK_SQUARE"] = sq_eval_d21

        prop_d21 = TimingEngine.generate_manager_proposal(
            evaluations=evals_d21,
            portfolio={"holdingStock": "SK_SQUARE", "shares": 76, "currentPrice": 1050000.0},
            date=eval_date,
        )
        self.assertNotEqual(prop_d21.tactical_action, "REVERSE_SWITCH_WARNING")

    def test_manager_journal_markdown_has_latex_and_ranking_table(self) -> None:
        """AC4.7: Verify markdown report generates LaTeX math recovery formula and ranking table."""
        proposal = TimingEngine.generate_manager_proposal(date="2026-10-12")
        md = proposal.journal_markdown

        # LaTeX formula check
        self.assertIn("38\\text{주}", md)
        self.assertIn("2,180,000\\text{원}", md)
        self.assertIn("82,840,000\\text{원 (8,284만 원)}", md)
        self.assertIn("100.0\\%\\text{ 원금 전액 회수}", md)

        # Ranking table check
        self.assertIn("| 순위 | 종목명 (티커) | 현재가 | TP1 목표가 | TP1 업사이드 | 최근 촉매 D-Day | 복합 스코어 | RRR | 속도 평점 | 도달 속도 판정 |", md)


if __name__ == "__main__":
    unittest.main()
