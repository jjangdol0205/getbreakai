"""Adversarial Empirical Stress Tests for TimingEngine and FundManagerProposal (M1-1).

Authored by Challenger M1-1 (critic, specialist).
Empirically stress-tests engine/timing_engine.py against:
1. Extreme price variations (500k KRW crash below support, 3M KRW moonshot above TP1, zero, negative).
2. Catalyst D-Day edge cases (0 days, negative days, missing/None, distant >60 days).
3. Candidate stock RRR variations (all candidates worse, zero RRR, huge RRR, negative RRR).
4. Reverse switching warning strict activation at holding D-Day <= 20 and deactivation at D-Day >= 21.
5. Mathematical integrity of PortfolioDiagnostic and FundManagerProposal serialization.
"""

import math
import unittest
from datetime import date as dt_date
from typing import Any, Dict, List

from engine.models import StockSymbol, STOCK_MASTERS
from engine.timing_engine import (
    CatalystEvent,
    CompositeTriggerResult,
    DailyTimingSnapshot,
    FundManagerProposal,
    PortfolioDiagnostic,
    RiskManagementAlert,
    StockTimingEvaluation,
    STOCK_REFERENCE_PRICES,
    SwitchingActionScenario,
    SwitchingRecommendation,
    TakeProfitConfig,
    TimingEngine,
    ValuationBandConfig,
)


class TestTimingEngineEmpiricalStressM1_1(unittest.TestCase):
    """Adversarial empirical stress suite for engine/timing_engine.py."""

    def setUp(self) -> None:
        self.as_of_date = "2026-10-12"
        # Standard baseline evaluations
        self.base_evaluations = {
            sid: TimingEngine.evaluate_stock(
                stock_id=sid,
                current_price=STOCK_REFERENCE_PRICES.get(sid, 100.0),
                date=self.as_of_date,
            )
            for sid in ["SK_HYNIX", "SK_SQUARE", "UBER", "MBLY", "FLNC", "UPST", "CELH", "ENPH"]
        }

    # ==========================================================================
    # 1. EXTREME PRICE EDGE CASES
    # ==========================================================================

    def test_extreme_price_crash_500k_krw_below_support(self) -> None:
        """Stress Test 1.1: SK Square price crashes to 500,000 KRW (below 980k support).

        - Valuation: 76 * 500,000 = 38,000,000 KRW
        - PnL Amount: 38,000,000 - 82,840,000 = -44,840,000 KRW
        - PnL Rate: -54.13%
        - TP1 Progress: (500,000 / 2,180,000) * 100 = 22.9%
        - Safety Margin Condition: False (breaks key support 980,000)
        - Critical SUPPORT_DEFENSE alert generated
        - Zero crashes, zero division by zero.
        """
        eval_500k = TimingEngine.evaluate_stock(
            stock_id="SK_SQUARE",
            current_price=500000.0,
            date=self.as_of_date,
        )
        self.assertFalse(eval_500k.trigger.cond1_safety_margin)
        self.assertIn("핵심 지지선 이탈", eval_500k.trigger.cond1_detail)

        evals = dict(self.base_evaluations)
        evals["SK_SQUARE"] = eval_500k

        portfolio_input = {
            "holdingStock": "SK_SQUARE",
            "shares": 76,
            "principalKrw": 82840000,
            "avgCostKrw": 1090000,
            "currentPrice": 500000.0,
        }

        proposal = TimingEngine.generate_manager_proposal(
            evaluations=evals,
            portfolio=portfolio_input,
            date=self.as_of_date,
        )

        diag = proposal.core_holding
        self.assertEqual(diag.shares, 76)
        self.assertEqual(diag.current_price, 500000.0)
        self.assertEqual(diag.current_valuation_krw, 38000000)
        self.assertEqual(diag.pnl_amount_krw, -44840000)
        self.assertAlmostEqual(diag.pnl_rate_pct, -54.13, places=2)
        self.assertAlmostEqual(diag.tp1_progress_pct, 22.9, places=1)
        self.assertEqual(diag.tp1_target_price, 2180000.0)
        self.assertEqual(diag.tp1_shares_to_sell, 38)
        self.assertEqual(diag.tp1_recovered_amount, 82840000)

        # Support defense alert must be triggered
        support_alerts = [w for w in proposal.risk_warnings if w.alert_type == "SUPPORT_DEFENSE"]
        self.assertEqual(len(support_alerts), 1)
        self.assertEqual(support_alerts[0].severity, "CRITICAL")
        self.assertIn("980,000원", support_alerts[0].message)

        # Serialization to dict must be completely valid
        d = proposal.to_dict()
        self.assertEqual(d["coreHolding"]["currentValuationKrw"], 38000000)
        self.assertIn("3,800만 원", d["coreHolding"]["currentValuationFormatted"])

    def test_extreme_price_moonshot_3m_krw_above_tp1(self) -> None:
        """Stress Test 1.2: SK Square price surges to 3,000,000 KRW (exceeding TP1 2,180,000).

        - Valuation: 76 * 3,000,000 = 228,000,000 KRW
        - PnL Amount: 228,000,000 - 82,840,000 = +145,160,000 KRW
        - PnL Rate: +175.23%
        - TP1 Progress: 137.6%
        - Status Phase: TP1_REACHED_EXECUTE_SELL_38
        - Tactical Action: TAKE_PROFIT_TP1
        """
        eval_3m = TimingEngine.evaluate_stock(
            stock_id="SK_SQUARE",
            current_price=3000000.0,
            date=self.as_of_date,
        )
        evals = dict(self.base_evaluations)
        evals["SK_SQUARE"] = eval_3m

        portfolio_input = {
            "holdingStock": "SK_SQUARE",
            "shares": 76,
            "principalKrw": 82840000,
            "avgCostKrw": 1090000,
            "currentPrice": 3000000.0,
        }

        proposal = TimingEngine.generate_manager_proposal(
            evaluations=evals,
            portfolio=portfolio_input,
            date=self.as_of_date,
        )

        diag = proposal.core_holding
        self.assertEqual(diag.current_valuation_krw, 228000000)
        self.assertEqual(diag.pnl_amount_krw, 145160000)
        self.assertAlmostEqual(diag.pnl_rate_pct, 175.23, places=2)
        self.assertAlmostEqual(diag.tp1_progress_pct, 137.6, places=1)
        self.assertEqual(diag.status_phase, "TP1_REACHED_EXECUTE_SELL_38")

        self.assertEqual(proposal.tactical_action, "TAKE_PROFIT_TP1")
        self.assertIn("TP1(218만 원) 달성", proposal.action_headline)
        self.assertIn("38주를 매도하여", proposal.executive_summary)

    def test_extreme_negative_price_resilience(self) -> None:
        """Stress Test 1.3: Negative prices are handled safely without unhandled exceptions."""
        bad_p = -1000.0
        eval_bad = TimingEngine.evaluate_stock(
            stock_id="SK_SQUARE",
            current_price=bad_p,
            date=self.as_of_date,
        )
        self.assertFalse(eval_bad.trigger.cond1_safety_margin)

        proposal = TimingEngine.generate_manager_proposal(
            evaluations=self.base_evaluations,
            portfolio={"currentPrice": bad_p, "shares": 76, "principalKrw": 82840000},
            date=self.as_of_date,
        )
        self.assertIsNotNone(proposal)
        self.assertEqual(proposal.core_holding.current_price, bad_p)
        self.assertEqual(proposal.core_holding.tp1_progress_pct, 0.0)

    def test_vulnerability_portfolio_zero_price_causes_type_error(self) -> None:
        """Remediation Verification: When portfolio has currentPrice=0.0,

        timing_engine explicitly checks is not None and evaluates cleanly without TypeError.
        """
        prop = TimingEngine.generate_manager_proposal(
            evaluations=self.base_evaluations,
            portfolio={"currentPrice": 0.0, "shares": 76, "principalKrw": 82840000},
            date=self.as_of_date,
        )
        self.assertIsNotNone(prop)
        self.assertEqual(prop.core_holding.current_price, 0.0)

    def test_extreme_zero_principal_does_not_divide_by_zero(self) -> None:
        """Stress Test 1.4: principal_krw = 0 does not raise ZeroDivisionError."""
        proposal = TimingEngine.generate_manager_proposal(
            evaluations=self.base_evaluations,
            portfolio={"principalKrw": 0, "shares": 76, "currentPrice": 1050000.0},
            date=self.as_of_date,
        )
        self.assertEqual(proposal.core_holding.pnl_rate_pct, 0.0)

    # ==========================================================================
    # 2. CATALYST D-DAY EDGE CASES (0 days, negative days, distant >60 days)
    # ==========================================================================

    def test_catalyst_d_day_zero_is_active_and_imminent(self) -> None:
        """Stress Test 2.1: Catalyst D-Day = 0 (event occurring today) is recognized as active."""
        sq_eval = TimingEngine.evaluate_stock(
            stock_id="SK_SQUARE",
            current_price=1050000.0,
            date=self.as_of_date,
        )
        # Inject D-Day = 0 catalyst
        sq_eval.catalysts = [
            CatalystEvent(
                name="오늘 당일 결의 공시",
                target_date="2026-10-12",
                days_remaining=0,
                impact_level="CRITICAL",
                description="당일 도래 촉매",
                is_confirmed=True,
            )
        ]

        evals = dict(self.base_evaluations)
        evals["SK_SQUARE"] = sq_eval

        proposal = TimingEngine.generate_manager_proposal(
            evaluations=evals,
            date=self.as_of_date,
        )

        # D-Day = 0 is <= 20, so reverse switching must trigger!
        self.assertEqual(proposal.tactical_action, "REVERSE_SWITCH_WARNING")
        self.assertIn("D-0일", proposal.action_headline)

        # Check speed score calculation handles D-Day = 0 without error
        ranking_sq = next(item for item in proposal.time_to_100_ranking if item["stockId"] == "SK_SQUARE")
        self.assertEqual(ranking_sq["nearestCatalystDDay"], 0)
        self.assertGreater(ranking_sq["speedScore"], 100.0)

    def test_catalyst_all_negative_d_days_past_events(self) -> None:
        """Stress Test 2.2: When all catalysts have negative days_remaining (past events),

        they are excluded from active countdown, nearest D-Day falls back to 999,
        and reverse switching does NOT trigger.
        """
        sq_eval = TimingEngine.evaluate_stock(
            stock_id="SK_SQUARE",
            current_price=1050000.0,
            date=self.as_of_date,
        )
        # All catalysts in the past
        sq_eval.catalysts = [
            CatalystEvent(
                name="과거 1차 소각",
                target_date="2026-09-01",
                days_remaining=-41,
                impact_level="HIGH",
                description="이미 지난 이벤트",
                is_confirmed=True,
            ),
            CatalystEvent(
                name="과거 2차 실적",
                target_date="2026-10-01",
                days_remaining=-11,
                impact_level="CRITICAL",
                description="이미 지난 실적",
                is_confirmed=True,
            ),
        ]

        evals = dict(self.base_evaluations)
        evals["SK_SQUARE"] = sq_eval

        proposal = TimingEngine.generate_manager_proposal(
            evaluations=evals,
            date=self.as_of_date,
        )

        # Since active catalysts are none, h_d_day must fallback to 999
        ranking_sq = next(item for item in proposal.time_to_100_ranking if item["stockId"] == "SK_SQUARE")
        self.assertEqual(ranking_sq["nearestCatalystDDay"], 999)

        # Should NOT trigger REVERSE_SWITCH_WARNING
        self.assertNotEqual(proposal.tactical_action, "REVERSE_SWITCH_WARNING")

    def test_catalyst_distant_greater_than_60_days_causes_dead_money_warning(self) -> None:
        """Stress Test 2.3: Holding stock in safety margin with catalyst > 60 days

        triggers DEAD_MONEY warning risk alert.
        """
        # On 2026-08-01, FLNC catalysts (starting 2026-11-18) are 109 days away (> 60 days)
        flnc_eval = TimingEngine.evaluate_stock(
            stock_id="FLNC",
            current_price=15.0,  # inside safety margin
            date="2026-08-01",
        )
        self.assertEqual(flnc_eval.trigger.dead_money_risk, "HIGH")

        evals = dict(self.base_evaluations)
        evals["FLNC"] = flnc_eval

        proposal = TimingEngine.generate_manager_proposal(
            evaluations=evals,
            date="2026-08-01",
        )

        dead_money_alerts = [
            w for w in proposal.risk_warnings
            if w.alert_type == "DEAD_MONEY" and w.stock_id == "FLNC"
        ]
        self.assertEqual(len(dead_money_alerts), 1)
        self.assertEqual(dead_money_alerts[0].severity, "WARNING")
        self.assertIn("자금 정체(Dead Money)", dead_money_alerts[0].message)

    def test_vulnerability_catalyst_none_d_day_raises_type_error(self) -> None:
        """Remediation Verification: When a catalyst has days_remaining=None,

        timing_engine guards is not None and evaluates cleanly without TypeError.
        """
        bad_cat = CatalystEvent(
            name="미정 촉매",
            target_date="2026-10-30",
            days_remaining=None,  # type: ignore
            impact_level="HIGH",
            description="D-Day 계산 불가 촉매",
            is_confirmed=True,
        )
        sq_eval = TimingEngine.evaluate_stock(
            stock_id="SK_SQUARE",
            current_price=1050000.0,
            date=self.as_of_date,
        )
        sq_eval.catalysts = [bad_cat]
        evals = dict(self.base_evaluations)
        evals["SK_SQUARE"] = sq_eval

        prop = TimingEngine.generate_manager_proposal(
            evaluations=evals,
            date=self.as_of_date,
        )
        self.assertIsNotNone(prop)

    # ==========================================================================
    # 3. CANDIDATE STOCK RRR VARIATIONS
    # ==========================================================================

    def test_all_candidates_have_worse_rrr_holds_core(self) -> None:
        """Stress Test 3.1: When all candidate stocks have worse RRR than holding stock,

        evaluate_switching returns status HOLD_CORE and empty scenarios,
        and generate_manager_proposal returns HOLD_CORE with switching_proposal=None.
        """
        # Holding stock has RRR = 15.0, D-Day = 35 (so reverse switching defense is not active)
        sq_eval = TimingEngine.evaluate_stock(stock_id="SK_SQUARE", current_price=1050000.0, date=self.as_of_date)
        sq_eval.catalysts = [
            CatalystEvent("촉매", "2026-11-16", 35, "HIGH", "35일 후 촉매", True)
        ]
        sq_eval.trigger.risk_reward_ratio = 15.0
        sq_eval.trigger.cond2_days_remaining = 35

        evals: Dict[str, StockTimingEvaluation] = {"SK_SQUARE": sq_eval}

        # Make all other 7 stocks have abysmal RRR = 0.5 and worse catalysts
        for sid in ["SK_HYNIX", "UBER", "MBLY", "FLNC", "UPST", "CELH", "ENPH"]:
            ev = TimingEngine.evaluate_stock(
                stock_id=sid,
                current_price=STOCK_REFERENCE_PRICES.get(sid, 100.0),
                date=self.as_of_date,
            )
            ev.trigger.risk_reward_ratio = 0.5
            ev.trigger.composite_score = 1
            ev.catalysts = [CatalystEvent("원격 촉매", "2026-12-30", 79, "HIGH", "먼 촉매", True)]
            ev.trigger.cond2_days_remaining = 79
            evals[sid] = ev

        switching_rec = TimingEngine.evaluate_switching(
            holding_stock_id="SK_SQUARE",
            holding_shares=76,
            evaluations=evals,
            date=self.as_of_date,
        )

        self.assertEqual(switching_rec.status, "HOLD_CORE")
        self.assertIsNone(switching_rec.top_candidate_id)
        self.assertEqual(len(switching_rec.scenarios), 0)
        self.assertIn("교체 매매 실익 제한적", switching_rec.summary)

        proposal = TimingEngine.generate_manager_proposal(
            evaluations=evals,
            switching=switching_rec,
            date=self.as_of_date,
        )

        self.assertEqual(proposal.tactical_action, "HOLD_CORE")
        self.assertIsNone(proposal.switching_proposal)
        self.assertIn("SK스퀘어 76주 코어 과비중 유지", proposal.action_headline)

    def test_candidate_with_zero_or_negative_rrr_handles_cleanly(self) -> None:
        """Stress Test 3.2: Candidates with zero or negative RRR calculate cleanly without crashing."""
        sq_eval = self.base_evaluations["SK_SQUARE"]
        evals = dict(self.base_evaluations)

        # Set Uber RRR to 0.0 and MBLY to -5.0
        evals["UBER"].trigger.risk_reward_ratio = 0.0
        evals["MBLY"].trigger.risk_reward_ratio = -5.0

        rec = TimingEngine.evaluate_switching(
            holding_stock_id="SK_SQUARE",
            holding_shares=76,
            evaluations=evals,
            date=self.as_of_date,
        )
        self.assertIsNotNone(rec)

        cand_uber = next(c for c in rec.candidates if c["stockId"] == "UBER")
        self.assertEqual(cand_uber["candidateRrr"], 0.0)

        cand_mbly = next(c for c in rec.candidates if c["stockId"] == "MBLY")
        self.assertEqual(cand_mbly["candidateRrr"], -5.0)

    # ==========================================================================
    # 4. REVERSE SWITCHING TRIGGER STRICTNESS (D-Day <= 20)
    # ==========================================================================

    def test_reverse_switching_boundary_d_day_20_triggers_strict_defense(self) -> None:
        """Stress Test 4.1: When holding catalyst is exactly D-Day = 20 (and in safety margin),

        Reverse Switching defense strictly activates, blocking any switching opportunity
        even if candidate stock has superior RRR and score 3.
        """
        sq_eval = TimingEngine.evaluate_stock(stock_id="SK_SQUARE", current_price=1050000.0, date=self.as_of_date)
        sq_eval.catalysts = [
            CatalystEvent("20일 후 확정 촉매", "2026-11-01", 20, "CRITICAL", "D-20 촉매", True)
        ]
        self.assertTrue(sq_eval.trigger.cond1_safety_margin)

        # Create an enticing candidate (e.g. UBER) with composite score 3 and high RRR
        uber_eval = TimingEngine.evaluate_stock(stock_id="UBER", current_price=68.0, date=self.as_of_date)
        uber_eval.trigger.composite_score = 3
        uber_eval.trigger.risk_reward_ratio = 30.0
        uber_eval.catalysts = [
            CatalystEvent("우버 당일 촉매", "2026-10-15", 3, "CRITICAL", "D-3 촉매", True)
        ]

        evals = dict(self.base_evaluations)
        evals["SK_SQUARE"] = sq_eval
        evals["UBER"] = uber_eval

        # 1. Test evaluate_switching
        rec = TimingEngine.evaluate_switching(
            holding_stock_id="SK_SQUARE",
            holding_shares=76,
            evaluations=evals,
            date=self.as_of_date,
        )
        self.assertEqual(rec.status, "REVERSE_SWITCH_WARNING")
        self.assertIn("역(逆)스위칭 리스크 경고", rec.summary)
        # Reallocation scenario must be blocked when reverse warning is active
        self.assertEqual(len(rec.scenarios), 0)

        # 2. Test generate_manager_proposal
        proposal = TimingEngine.generate_manager_proposal(
            evaluations=evals,
            switching=rec,
            date=self.as_of_date,
        )
        self.assertEqual(proposal.tactical_action, "REVERSE_SWITCH_WARNING")
        self.assertIn("역(逆)스위칭 엄금 경고", proposal.action_headline)
        self.assertIn("D-20일", proposal.action_headline)
        self.assertIsNone(proposal.switching_proposal)

        # Check CRITICAL alert is present in risk_warnings
        critical_alerts = [
            w for w in proposal.risk_warnings
            if w.alert_type == "REVERSE_SWITCH_DEFENSE" and w.severity == "CRITICAL"
        ]
        self.assertEqual(len(critical_alerts), 1)
        self.assertIn("역스위칭 발생 위험 최고조", critical_alerts[0].message)

    def test_reverse_switching_boundary_d_day_21_permits_switching_if_advantageous(self) -> None:
        """Stress Test 4.2: When holding catalyst is D-Day = 21,

        Reverse Switching defense does NOT activate.
        If a candidate stock has superior catalyst (D-3) and RRR ratio >= 1.3,
        SWITCH_OPPORTUNITY is permitted.
        """
        sq_eval = TimingEngine.evaluate_stock(stock_id="SK_SQUARE", current_price=1050000.0, date=self.as_of_date)
        sq_eval.catalysts = [
            CatalystEvent("21일 후 확정 촉매", "2026-11-02", 21, "CRITICAL", "D-21 촉매", True)
        ]
        sq_eval.trigger.risk_reward_ratio = 5.0
        self.assertTrue(sq_eval.trigger.cond1_safety_margin)

        uber_eval = TimingEngine.evaluate_stock(stock_id="UBER", current_price=68.0, date=self.as_of_date)
        uber_eval.trigger.composite_score = 3
        uber_eval.trigger.risk_reward_ratio = 15.0  # ratio 3.0x > 1.3
        uber_eval.catalysts = [
            CatalystEvent("우버 초임박 촉매", "2026-10-15", 3, "CRITICAL", "D-3 촉매", True)
        ]

        evals = dict(self.base_evaluations)
        evals["SK_SQUARE"] = sq_eval
        evals["UBER"] = uber_eval

        rec = TimingEngine.evaluate_switching(
            holding_stock_id="SK_SQUARE",
            holding_shares=76,
            evaluations=evals,
            date=self.as_of_date,
        )

        self.assertEqual(rec.status, "SWITCH_OPPORTUNITY")
        self.assertEqual(rec.top_candidate_id, "UBER")
        self.assertGreater(len(rec.scenarios), 0)

        proposal = TimingEngine.generate_manager_proposal(
            evaluations=evals,
            switching=rec,
            date=self.as_of_date,
        )

        self.assertEqual(proposal.tactical_action, "TACTICAL_SWITCH")
        self.assertIsNotNone(proposal.switching_proposal)
        self.assertEqual(proposal.switching_proposal.candidate_id, "UBER")

    def test_vulnerability_reverse_switching_fails_when_price_exceeds_entry_band(self) -> None:
        """Remediation Verification: When holding stock price is slightly above entry buy band
        (e.g. 1,157,000 KRW > 1,120,000 max_price, as in live market data) but well below TP1 (2,180,000),
        reverse switching defense strictly triggers when holding catalyst <= 20 days and key support defended.
        """
        sq_eval = TimingEngine.evaluate_stock(
            stock_id="SK_SQUARE",
            current_price=1157000.0,  # Live price in FinanceFeed
            date=self.as_of_date,
        )
        self.assertFalse(sq_eval.trigger.cond1_safety_margin)  # > 1,120,000
        # SK Square catalyst is D-10
        h_d_day = min(c.days_remaining for c in sq_eval.catalysts if c.days_remaining is not None and c.days_remaining >= 0)
        self.assertEqual(h_d_day, 10)  # D-10 <= 20

        evals = dict(self.base_evaluations)
        evals["SK_SQUARE"] = sq_eval

        rec = TimingEngine.evaluate_switching(
            holding_stock_id="SK_SQUARE",
            holding_shares=76,
            evaluations=evals,
            date=self.as_of_date,
        )
        self.assertEqual(rec.status, "REVERSE_SWITCH_WARNING")

    # ==========================================================================
    # 5. MATHEMATICAL & SCHEMA INTEGRITY OF PORTFOLIODIAGNOSTIC
    # ==========================================================================

    def test_portfolio_diagnostic_exact_math_sk_square_76_shares(self) -> None:
        """Stress Test 5.1: Mathematical integrity of SK Square 76 shares formulas.

        - Principal: 82,840,000 KRW
        - Shares: 76
        - Avg Cost: 1,090,000 KRW (82,840,000 / 76 = 1,090,000)
        - Anchor Price: 1,050,000 KRW
        - Valuation: 76 * 1,050,000 = 79,800,000 KRW
        - PnL Amount: 79,800,000 - 82,840,000 = -3,040,000 KRW
        - PnL Rate: -3,040,000 / 82,840,000 = -3.67%
        - TP1 Price: 2,180,000 KRW
        - TP1 Shares to sell: 38 (50% of 76)
        - TP1 Recovered Amount: 38 * 2,180,000 = 82,840,000 KRW (exact 100.0% recovery)
        - Remaining Shares: 38 shares at effective cost 0 KRW.
        """
        proposal = TimingEngine.generate_manager_proposal(
            evaluations=self.base_evaluations,
            date=self.as_of_date,
        )
        diag = proposal.core_holding

        self.assertEqual(diag.shares, 76)
        self.assertEqual(diag.principal_krw, 82840000)
        self.assertEqual(diag.avg_cost_krw, 1090000)
        self.assertEqual(diag.current_price, 1050000.0)
        self.assertEqual(diag.current_valuation_krw, 79800000)
        self.assertEqual(diag.pnl_amount_krw, -3040000)
        self.assertAlmostEqual(diag.pnl_rate_pct, -3.67, places=2)

        self.assertEqual(diag.tp1_target_price, 2180000.0)
        self.assertEqual(diag.tp1_shares_to_sell, 38)
        self.assertEqual(diag.tp1_recovered_amount, 82840000)
        self.assertEqual(diag.tp1_shares_to_sell * diag.tp1_target_price, diag.principal_krw)
        self.assertAlmostEqual(diag.tp1_progress_pct, 48.2, places=1)

    def test_daily_timing_snapshot_roundtrip_with_manager_proposal(self) -> None:
        """Stress Test 5.2: DailyTimingSnapshot serialization and deserialization

        preserves managerProposal structure without data loss.
        """
        from engine.models import DailyMarketData
        md = DailyMarketData(date=self.as_of_date, stocks={})

        snapshot = TimingEngine.evaluate_daily_timing(
            market_data=md,
            as_of_date=self.as_of_date,
        )

        self.assertIsNotNone(snapshot.manager_proposal)
        snap_dict = snapshot.to_dict()
        self.assertIn("managerProposal", snap_dict)

        mp_dict = snap_dict["managerProposal"]
        self.assertEqual(mp_dict["managerPersona"], "가치투자 + 타이밍 천재 수석 펀드매니저 AI")
        self.assertIn("coreHolding", mp_dict)
        self.assertEqual(mp_dict["coreHolding"]["tp1RecoveredAmount"], 82840000)
        self.assertIn("journalMarkdown", mp_dict)
        self.assertIn("## 1. 📌 코어 보유자산 실시간 정밀 진단", mp_dict["journalMarkdown"])


if __name__ == "__main__":
    unittest.main()
