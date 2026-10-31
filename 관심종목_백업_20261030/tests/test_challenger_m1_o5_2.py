"""Adversarial Challenge & Stress Test Suite for Timing Engine & Stock Switching Engine (Milestone M1 Challenger 2).

Tests:
1. Combinatorial Truth Table Stress (all 8 permutations of Cond1, Cond2, Cond3 across all 8 stocks = 64 tests + signal checks).
2. Boundary Condition Testing for Individual Trigger Conditions (Safety Margin, Catalyst D-Day, Volume Washout).
3. Extreme RRR Situations (downside <= 0, candidate at/above TP1/TP2, current_price <= 0, extreme ratios).
4. Reverse-Switching Warning Triggers & Suppression (D<=20 trigger, D>20, D=180 6+ months, price outside margin, candidate switching scenarios).
5. Data Integrity, Edge Fuzzing & JSON Serialization Safety.
"""

from __future__ import annotations

import json
import unittest
from datetime import date, timedelta
from typing import Any, Dict, List

from engine.models import STOCK_MASTERS, StockSymbol
from engine.timing_engine import (
    CatalystEvent,
    CompositeTriggerResult,
    DailyTimingSnapshot,
    StockTimingEvaluation,
    SwitchingRecommendation,
    TakeProfitConfig,
    TimingEngine,
    ValuationBandConfig,
    STOCK_BENCHMARK_20D_VOLUME,
    STOCK_REFERENCE_PRICES,
)


class TestCombinatorialTruthTableStress(unittest.TestCase):
    """Stress-tests all 8 truth table combinations of the 3-condition composite trigger across all 8 stocks."""

    CANONICAL_STOCKS = [
        "SK_HYNIX", "SK_SQUARE", "UBER", "MBLY", "FLNC", "UPST", "CELH", "ENPH"
    ]

    def test_truth_table_all_8_stocks_all_8_permutations(self):
        """Test all 8 combinations of (cond1, cond2, cond3) across all 8 canonical stocks (64 cases)."""
        eval_date = "2026-10-12"

        for sid in self.CANONICAL_STOCKS:
            band = TimingEngine.get_valuation_band(sid)
            tp = TimingEngine.get_take_profit(sid)

            # Price inside safety margin band
            p_in_margin = (band.min_price + band.max_price) / 2.0
            # Price outside safety margin band (above max_price, but below TP1)
            p_out_margin = band.max_price + (tp.tp1_price - band.max_price) * 0.1

            # Prepare parameters for Condition 2 (Catalyst Imminent: 0 <= D <= 60)
            # Default catalysts for 2026-10-12 are already within 60 days for all stocks.
            # To simulate Cond2=False, we evaluate with an as_of_date far past the catalysts
            date_cat_imminent = eval_date
            date_cat_distant = "2025-01-01"  # in 2025, 2026 catalysts are > 600 days away

            # Prepare parameters for Condition 3 (Volume Washout & Support Rebound)
            # Cond3=True: volume >= 1.5x benchmark, positive daily change, price >= support
            bench_vol = STOCK_BENCHMARK_20D_VOLUME.get(sid, 100000)
            vol_washout_true = int(bench_vol * 1.5)
            chg_washout_true = 2.5

            # Cond3=False: negative change (red day / continuing selloff)
            vol_washout_false = int(bench_vol * 1.5)
            chg_washout_false = -2.5

            test_cases = [
                # (cond1_target, cond2_target, cond3_target, expected_score, expected_signal, expected_dead_money)
                (True, True, True, 3, "STRONG_BUY", "LOW"),
                (True, True, False, 2, "ACCUMULATE", "MEDIUM"),
                (True, False, True, 2, "ACCUMULATE", "MEDIUM"),
                (True, False, False, 1, "WATCH_CATALYST", "HIGH"),
                (False, True, True, 2, "HOLD", "LOW"),
                (False, True, False, 1, "HOLD", "LOW"),
                (False, False, True, 1, "HOLD", "LOW"),
                (False, False, False, 0, "HOLD", "LOW"),
            ]

            for c1, c2, c3, exp_score, exp_signal, exp_dead_money in test_cases:
                with self.subTest(stock=sid, c1=c1, c2=c2, c3=c3):
                    p = p_in_margin if c1 else p_out_margin
                    eval_d = date_cat_imminent if c2 else date_cat_distant
                    v = vol_washout_true if c3 else vol_washout_false
                    c = chg_washout_true if c3 else chg_washout_false

                    res = TimingEngine.evaluate_trigger(
                        stock_id=sid,
                        current_price=p,
                        daily_change_pct=c,
                        volume=v,
                        date=eval_d,
                    )

                    self.assertEqual(res.cond1_safety_margin, c1, f"Stock {sid} Cond1 mismatch: expected {c1}")
                    self.assertEqual(res.cond2_catalyst_imminent, c2, f"Stock {sid} Cond2 mismatch: expected {c2}")
                    self.assertEqual(res.cond3_volume_washout, c3, f"Stock {sid} Cond3 mismatch: expected {c3}")
                    self.assertEqual(res.composite_score, exp_score, f"Stock {sid} Score mismatch")
                    self.assertEqual(res.signal, exp_signal, f"Stock {sid} Signal mismatch")
                    self.assertEqual(res.dead_money_risk, exp_dead_money, f"Stock {sid} Dead money risk mismatch")

    def test_dead_money_filter_activation(self):
        """Verify that when stock is in safety margin band but has no imminent catalyst or washout,
        the signal is strictly WATCH_CATALYST with HIGH dead_money_risk.
        """
        for sid in self.CANONICAL_STOCKS:
            band = TimingEngine.get_valuation_band(sid)
            p_in_margin = (band.min_price + band.max_price) / 2.0

            res = TimingEngine.evaluate_trigger(
                stock_id=sid,
                current_price=p_in_margin,
                daily_change_pct=-1.5,  # Red day (no washout green rebound)
                volume=1000,
                date="2025-01-01",      # Distant catalyst (>600 days)
            )

            self.assertTrue(res.cond1_safety_margin)
            self.assertFalse(res.cond2_catalyst_imminent)
            self.assertFalse(res.cond3_volume_washout)
            self.assertEqual(res.composite_score, 1)
            self.assertEqual(res.signal, "WATCH_CATALYST")
            self.assertEqual(res.dead_money_risk, "HIGH")
            self.assertIn("촉매 대기", res.signal_label)

    def test_strong_buy_intersection_activation(self):
        """Verify that STRONG_BUY requires all 3 conditions to be True simultaneously."""
        for sid in self.CANONICAL_STOCKS:
            band = TimingEngine.get_valuation_band(sid)
            p_in_margin = (band.min_price + band.max_price) / 2.0
            bench_vol = STOCK_BENCHMARK_20D_VOLUME.get(sid, 100000)

            res = TimingEngine.evaluate_trigger(
                stock_id=sid,
                current_price=p_in_margin,
                daily_change_pct=1.5,
                volume=int(bench_vol * 1.5),
                date="2026-10-12",
            )

            self.assertTrue(res.cond1_safety_margin)
            self.assertTrue(res.cond2_catalyst_imminent)
            self.assertTrue(res.cond3_volume_washout)
            self.assertEqual(res.composite_score, 3)
            self.assertEqual(res.signal, "STRONG_BUY")
            self.assertEqual(res.dead_money_risk, "LOW")
            self.assertIn("강력 매수", res.signal_label)


class TestTriggerBoundaryConditions(unittest.TestCase):
    """Fine-grained boundary value analysis on trigger conditions."""

    def test_condition_1_safety_margin_boundaries(self):
        """Test exact boundary points of the safety margin band and support floor."""
        sid = "MBLY"
        band = TimingEngine.get_valuation_band(sid)  # min 6.5, max 7.5, support 6.2

        # 1. Exactly at min_price (6.50)
        res_min = TimingEngine.evaluate_trigger(sid, current_price=band.min_price)
        self.assertTrue(res_min.cond1_safety_margin)
        self.assertIn("적극 매수 밴드 안착", res_min.cond1_detail)

        # 2. Exactly at max_price (7.50)
        res_max = TimingEngine.evaluate_trigger(sid, current_price=band.max_price)
        self.assertTrue(res_max.cond1_safety_margin)
        self.assertIn("적극 매수 밴드 안착", res_max.cond1_detail)

        # 3. Just below min_price but above support (6.30)
        res_sub_min = TimingEngine.evaluate_trigger(sid, current_price=6.30)
        self.assertTrue(res_sub_min.cond1_safety_margin)
        self.assertIn("극저점 안전마진 진입", res_sub_min.cond1_detail)

        # 4. Exactly at key_support_price (6.20)
        res_support = TimingEngine.evaluate_trigger(sid, current_price=band.key_support_price)
        self.assertTrue(res_support.cond1_safety_margin)
        self.assertIn("극저점 안전마진 진입", res_support.cond1_detail)

        # 5. Below key_support_price (6.10)
        res_below_support = TimingEngine.evaluate_trigger(sid, current_price=6.10)
        self.assertFalse(res_below_support.cond1_safety_margin)
        self.assertIn("핵심 지지선 이탈 주의", res_below_support.cond1_detail)

        # 6. Above max_price (7.60)
        res_above_max = TimingEngine.evaluate_trigger(sid, current_price=7.60)
        self.assertFalse(res_above_max.cond1_safety_margin)
        self.assertIn("매수 밴드 상단 초과", res_above_max.cond1_detail)

    def test_condition_3_washout_boundaries(self):
        """Test boundary conditions for volume surge and rebound."""
        sid = "UBER"
        band = TimingEngine.get_valuation_band(sid)
        bench_vol = STOCK_BENCHMARK_20D_VOLUME[sid]

        # Case A: Volume >= 1.4x bench, positive change -> cond3 True
        res_a = TimingEngine.evaluate_trigger(
            sid, current_price=band.min_price, daily_change_pct=0.01, volume=int(bench_vol * 1.4)
        )
        self.assertTrue(res_a.cond3_volume_washout)

        # Case B: Volume >= 1.4x bench, NEGATIVE change (-0.1%) -> cond3 False (selloff continuing)
        res_b = TimingEngine.evaluate_trigger(
            sid, current_price=band.min_price, daily_change_pct=-0.1, volume=int(bench_vol * 1.4)
        )
        self.assertFalse(res_b.cond3_volume_washout)
        self.assertIn("바닥 털기", res_b.cond3_detail)

        # Case C: Zero volume -> cond3 False
        res_c = TimingEngine.evaluate_trigger(
            sid, current_price=band.min_price, daily_change_pct=1.0, volume=0
        )
        self.assertFalse(res_c.cond3_volume_washout)

        # Case D: Support breach (price < 0.99 * support) -> cond3 False even with volume & green candle
        res_d = TimingEngine.evaluate_trigger(
            sid, current_price=band.key_support_price * 0.98, daily_change_pct=1.0, volume=int(bench_vol * 2.0)
        )
        self.assertFalse(res_d.cond3_volume_washout)
        self.assertIn("지지선 하회", res_d.cond3_detail)


class TestExtremeRRRSituations(unittest.TestCase):
    """Stress-tests extreme and pathological RRR (Risk-Reward Ratio) inputs."""

    def test_downside_zero_at_support_price(self):
        """When current_price == key_support_price, downside_risk_pct is 0.0.
        Must not divide by zero; must clamp downside denominator to at least 0.1.
        """
        for sid in TestCombinatorialTruthTableStress.CANONICAL_STOCKS:
            band = TimingEngine.get_valuation_band(sid)
            tp = TimingEngine.get_take_profit(sid)

            res = TimingEngine.evaluate_trigger(sid, current_price=band.key_support_price)

            self.assertEqual(res.downside_risk_pct, 0.0)
            self.assertGreater(res.upside_tp1_pct, 0.0)
            # RRR = upside_tp1_pct / 0.1
            expected_rrr = round(res.upside_tp1_pct / 0.1, 2)
            self.assertEqual(res.risk_reward_ratio, expected_rrr)
            self.assertFalse(res.risk_reward_ratio != res.risk_reward_ratio)  # Not NaN

    def test_downside_below_support_floor(self):
        """When current_price is below key_support_price, downside calculation should penalize risk."""
        for sid in TestCombinatorialTruthTableStress.CANONICAL_STOCKS:
            band = TimingEngine.get_valuation_band(sid)

            res = TimingEngine.evaluate_trigger(sid, current_price=band.key_support_price * 0.8)
            self.assertGreater(res.downside_risk_pct, 0.0)
            self.assertEqual(res.downside_risk_pct, 35.0)  # 25.0% breach + 10.0% base penalty
            self.assertGreater(res.risk_reward_ratio, 0.0)
            self.assertLess(res.risk_reward_ratio, 50.0)  # Realistic RRR without 1,500x inflation

    def test_candidate_price_at_or_above_tp1(self):
        """When current_price >= tp1_price, signal must be TAKE_PROFIT, upside_tp1 <= 0, and RRR == 0.0."""
        for sid in TestCombinatorialTruthTableStress.CANONICAL_STOCKS:
            tp = TimingEngine.get_take_profit(sid)

            # Test exactly at TP1
            res_tp1 = TimingEngine.evaluate_trigger(sid, current_price=tp.tp1_price)
            self.assertEqual(res_tp1.signal, "TAKE_PROFIT")
            self.assertEqual(res_tp1.upside_tp1_pct, 0.0)
            self.assertEqual(res_tp1.risk_reward_ratio, 0.0)

            # Test between TP1 and TP2
            mid_p = (tp.tp1_price + tp.tp2_price) / 2.0
            res_mid = TimingEngine.evaluate_trigger(sid, current_price=mid_p)
            self.assertEqual(res_mid.signal, "TAKE_PROFIT")
            self.assertLess(res_mid.upside_tp1_pct, 0.0)
            self.assertEqual(res_mid.risk_reward_ratio, 0.0)

    def test_candidate_price_at_or_above_tp2(self):
        """When candidate price is at or above TP2, upside_tp2 <= 0, RRR == 0.0, signal is TAKE_PROFIT."""
        for sid in TestCombinatorialTruthTableStress.CANONICAL_STOCKS:
            tp = TimingEngine.get_take_profit(sid)

            res_tp2 = TimingEngine.evaluate_trigger(sid, current_price=tp.tp2_price * 1.05)
            self.assertEqual(res_tp2.signal, "TAKE_PROFIT")
            self.assertLess(res_tp2.upside_tp1_pct, 0.0)
            self.assertLess(res_tp2.upside_tp2_pct, 0.0)
            self.assertEqual(res_tp2.risk_reward_ratio, 0.0)

    def test_zero_or_negative_current_price_safety(self):
        """Robustness check: zero or negative price must not raise ZeroDivisionError."""
        for p in [0.0, -10.0, -0.0001]:
            res = TimingEngine.evaluate_trigger("SK_SQUARE", current_price=p)
            self.assertEqual(res.downside_risk_pct, 0.0)
            self.assertEqual(res.upside_tp1_pct, 0.0)
            self.assertEqual(res.risk_reward_ratio, 0.0)
            self.assertFalse(res.cond1_safety_margin)


class TestReverseSwitchingEdgeCases(unittest.TestCase):
    """Stress-tests reverse switching warning triggers and ensures no false suppressions."""

    def _build_mock_evaluations(
        self,
        holding_sid: str = "SK_SQUARE",
        holding_price: float = 1065000.0,
        holding_d_day: int = 10,
        candidate_sid: str = "MBLY",
        candidate_price: float = 7.10,
        candidate_d_day: int = 18,
        candidate_score: int = 3,
        candidate_rrr: float = 40.0,
    ) -> Dict[str, StockTimingEvaluation]:
        """Helper to build custom evaluations for switching engine tests."""
        # Holding eval
        h_band = TimingEngine.get_valuation_band(holding_sid, current_price=holding_price)
        h_tp = TimingEngine.get_take_profit(holding_sid, current_price=holding_price)
        h_trig = TimingEngine.evaluate_trigger(
            holding_sid, current_price=holding_price, date="2026-10-12"
        )
        # Inject custom catalyst D-Day for holding
        h_cat = [
            CatalystEvent(
                name="Holding Catalyst",
                target_date="2026-10-22",
                days_remaining=holding_d_day,
                impact_level="CRITICAL",
                description="Custom test event",
            )
        ]
        h_eval = StockTimingEvaluation(
            stock_id=holding_sid,
            stock_name="SK스퀘어",
            ticker="402340",
            valuation_band=h_band,
            catalysts=h_cat,
            take_profit=h_tp,
            trigger=h_trig,
        )

        # Candidate eval
        c_band = TimingEngine.get_valuation_band(candidate_sid, current_price=candidate_price)
        c_tp = TimingEngine.get_take_profit(candidate_sid, current_price=candidate_price)
        c_trig = TimingEngine.evaluate_trigger(
            candidate_sid, current_price=candidate_price, date="2026-10-12"
        )
        # Override score and RRR if specified
        c_trig.composite_score = candidate_score
        c_trig.risk_reward_ratio = candidate_rrr
        c_cat = [
            CatalystEvent(
                name="Candidate Catalyst",
                target_date="2026-10-30",
                days_remaining=candidate_d_day,
                impact_level="CRITICAL",
                description="Custom test event",
            )
        ]
        c_eval = StockTimingEvaluation(
            stock_id=candidate_sid,
            stock_name="모빌아이",
            ticker="MBLY",
            valuation_band=c_band,
            catalysts=c_cat,
            take_profit=c_tp,
            trigger=c_trig,
        )

        return {holding_sid: h_eval, candidate_sid: c_eval}

    def test_reverse_switch_warning_triggers_when_d_less_than_equal_20_and_in_margin(self):
        """REVERSE_SWITCH_WARNING must trigger when holding D-Day <= 20 and holding is in safety margin."""
        for d in [0, 5, 10, 15, 20]:
            evals = self._build_mock_evaluations(
                holding_sid="SK_SQUARE",
                holding_price=1065000.0,  # inside 1,000,000 ~ 1,120,000
                holding_d_day=d,
                candidate_sid="MBLY",
                candidate_score=3,
                candidate_rrr=50.0,
            )
            rec = TimingEngine.evaluate_switching(
                holding_stock_id="SK_SQUARE",
                holding_shares=76,
                evaluations=evals,
            )
            self.assertEqual(
                rec.status,
                "REVERSE_SWITCH_WARNING",
                f"Failed to trigger REVERSE_SWITCH_WARNING at D-{d}",
            )
            self.assertIn("역(逆)스위칭 리스크 경고", rec.summary)
            # Scenarios MUST be suppressed
            self.assertEqual(len(rec.scenarios), 0)

    def test_no_false_suppression_when_holding_catalyst_distant_d_over_20(self):
        """When holding catalyst is D=21 (just over 20) and candidate has strong setup,
        must switch to SWITCH_OPPORTUNITY (not suppressed).
        """
        evals = self._build_mock_evaluations(
            holding_sid="SK_SQUARE",
            holding_price=1065000.0,
            holding_d_day=21,  # > 20
            candidate_sid="MBLY",
            candidate_d_day=10,
            candidate_score=3,
            candidate_rrr=50.0,
        )
        rec = TimingEngine.evaluate_switching(
            holding_stock_id="SK_SQUARE",
            holding_shares=76,
            evaluations=evals,
        )
        self.assertEqual(rec.status, "SWITCH_OPPORTUNITY")
        self.assertEqual(rec.top_candidate_id, "MBLY")
        self.assertGreater(len(rec.scenarios), 0)

    def test_no_false_suppression_when_holding_has_no_catalyst_for_6_months(self):
        """When holding has no catalyst for 6+ months (e.g. D=180 or D=999),
        switching to candidate with score=3 and imminent catalyst must NEVER be suppressed.
        """
        for d_day in [180, 240, 365, 999]:
            evals = self._build_mock_evaluations(
                holding_sid="SK_SQUARE",
                holding_price=1065000.0,
                holding_d_day=d_day,
                candidate_sid="MBLY",
                candidate_d_day=15,
                candidate_score=3,
                candidate_rrr=35.0,
            )
            rec = TimingEngine.evaluate_switching(
                holding_stock_id="SK_SQUARE",
                holding_shares=76,
                evaluations=evals,
            )
            self.assertEqual(
                rec.status,
                "SWITCH_OPPORTUNITY",
                f"Falsely suppressed switch when holding D-Day is {d_day}",
            )
            self.assertEqual(rec.top_candidate_id, "MBLY")
            self.assertEqual(len(rec.scenarios), 1)
            scenario = rec.scenarios[0]
            self.assertIn("15주", scenario["title"])
            self.assertIn(evals["MBLY"].stock_name, scenario["catalystComparison"])

    def test_reverse_switch_not_triggered_if_holding_outside_safety_margin(self):
        """If holding stock has D <= 20 and price has surged above entry band (1,500,000) but below TP1,
        reverse switching warning strictly triggers. If price exceeds TP1 (2,500,000), reverse warning does not trigger.
        """
        evals = self._build_mock_evaluations(
            holding_sid="SK_SQUARE",
            holding_price=1500000.0,  # Above max_price 1,120,000, but below TP1 2,180,000
            holding_d_day=10,
            candidate_sid="MBLY",
            candidate_d_day=5,
            candidate_score=3,
            candidate_rrr=50.0,
        )
        rec = TimingEngine.evaluate_switching(
            holding_stock_id="SK_SQUARE",
            holding_shares=76,
            evaluations=evals,
        )
        self.assertEqual(rec.status, "REVERSE_SWITCH_WARNING")

        # When price reaches or exceeds TP1 target price (2,180,000), reverse switching defense deactivates
        evals_tp1 = self._build_mock_evaluations(
            holding_sid="SK_SQUARE",
            holding_price=2500000.0,  # Exceeding TP1
            holding_d_day=10,
            candidate_sid="MBLY",
            candidate_d_day=5,
            candidate_score=3,
            candidate_rrr=50.0,
        )
        rec_tp1 = TimingEngine.evaluate_switching(
            holding_stock_id="SK_SQUARE",
            holding_shares=76,
            evaluations=evals_tp1,
        )
        self.assertNotEqual(rec_tp1.status, "REVERSE_SWITCH_WARNING")

    def test_reverse_switch_not_triggered_if_holding_below_support_floor(self):
        """If holding stock has D <= 20 but price broke BELOW support floor (900,000 < 980,000),
        cond1_safety_margin is False, so reverse warning does NOT trigger.
        """
        evals = self._build_mock_evaluations(
            holding_sid="SK_SQUARE",
            holding_price=900000.0,  # Broken support
            holding_d_day=10,
            candidate_sid="MBLY",
            candidate_d_day=5,
            candidate_score=3,
            candidate_rrr=50.0,
        )
        rec = TimingEngine.evaluate_switching(
            holding_stock_id="SK_SQUARE",
            holding_shares=76,
            evaluations=evals,
        )
        self.assertNotEqual(rec.status, "REVERSE_SWITCH_WARNING")

    def test_hold_core_when_candidate_inferior(self):
        """When candidate has lower RRR and score <= 1, engine correctly stays on HOLD_CORE."""
        evals = self._build_mock_evaluations(
            holding_sid="SK_SQUARE",
            holding_price=1065000.0,
            holding_d_day=45,  # > 20
            candidate_sid="MBLY",
            candidate_score=1,
            candidate_rrr=2.0,  # very low RRR
        )
        rec = TimingEngine.evaluate_switching(
            holding_stock_id="SK_SQUARE",
            holding_shares=76,
            evaluations=evals,
        )
        self.assertEqual(rec.status, "HOLD_CORE")
        self.assertIsNone(rec.top_candidate_id)
        self.assertEqual(len(rec.scenarios), 0)


class TestFullDailyTimingPipelineAndSerialization(unittest.TestCase):
    """Stress-tests the full daily timing pipeline and serialization."""

    def test_evaluate_daily_timing_all_canonical_stocks_serialized(self):
        """Verify evaluate_daily_timing runs on all 8 stocks and serializes to valid JSON."""
        from engine.models import DailyMarketData, StockFactSheet, MarketMetrics

        market_data = DailyMarketData(date="2026-10-12")
        for sid, ref_p in STOCK_REFERENCE_PRICES.items():
            master = STOCK_MASTERS[StockSymbol(sid)]
            metrics = MarketMetrics(
                stock_id=sid,
                close_price=ref_p,
                close_price_formatted=f"${ref_p:.2f}" if ref_p < 1000 else f"{int(ref_p):,}원",
                change_percent=0.5,
                volume=STOCK_BENCHMARK_20D_VOLUME.get(sid, 100000),
            )
            market_data.stocks[sid] = StockFactSheet(
                stock_id=sid,
                stock_name=master.name_kr,
                name_kr=master.name_kr,
                name_en=master.name_en,
                ticker=master.ticker,
                market=master.market,
                category=master.category,
                badge_color=master.badge_color,
                metrics=metrics,
            )

        portfolio = {
            "holdingStock": "SK_SQUARE",
            "shares": 76,
        }

        snapshot = TimingEngine.evaluate_daily_timing(market_data, portfolio=portfolio)

        self.assertEqual(snapshot.date, "2026-10-12")
        self.assertEqual(len(snapshot.stocks), 8)
        self.assertIn("SK_HYNIX", snapshot.stocks)
        self.assertIn("SK_SQUARE", snapshot.stocks)

        # JSON serialization check
        snapshot_dict = snapshot.to_dict()
        serialized_json = json.dumps(snapshot_dict, ensure_ascii=False)
        self.assertIsInstance(serialized_json, str)
        self.assertIn("switching", snapshot_dict)
        self.assertIn("stocks", snapshot_dict)


class TestAdversarialStressFuzzingAndSorting(unittest.TestCase):
    """Stress tests candidate sorting, fallback branches, dual-currency, and fuzzing."""

    def test_candidate_priority_sorting(self):
        """Candidates must be sorted strictly by tier priority, then catalyst advantage, then RRR ratio."""
        holding_eval = TimingEngine.evaluate_stock("SK_SQUARE", 1065000.0, date="2026-10-12")
        # Give holding distant catalyst so reverse switch is disabled
        holding_eval.catalysts = [
            CatalystEvent("H", "2027-01-01", 100, "HIGH", "desc")
        ]

        # Candidate A: PARTIAL_SWITCH (score 2, RRR 20.0, D-10)
        cand_a = TimingEngine.evaluate_stock("FLNC", 15.0, date="2026-10-12")
        cand_a.trigger.composite_score = 2
        cand_a.trigger.risk_reward_ratio = 20.0
        cand_a.catalysts = [CatalystEvent("A", "2026-10-22", 10, "HIGH", "desc")]

        # Candidate B: STRONG_SWITCH (score 3, RRR 30.0, D-10) -> advantage = 90
        cand_b = TimingEngine.evaluate_stock("UBER", 65.0, date="2026-10-12")
        cand_b.trigger.composite_score = 3
        cand_b.trigger.risk_reward_ratio = 30.0
        cand_b.catalysts = [CatalystEvent("B", "2026-10-22", 10, "HIGH", "desc")]

        # Candidate C: STRONG_SWITCH (score 3, RRR 35.0, D-5) -> advantage = 95
        cand_c = TimingEngine.evaluate_stock("MBLY", 7.0, date="2026-10-12")
        cand_c.trigger.composite_score = 3
        cand_c.trigger.risk_reward_ratio = 35.0
        cand_c.catalysts = [CatalystEvent("C", "2026-10-17", 5, "HIGH", "desc")]

        evals = {
            "SK_SQUARE": holding_eval,
            "FLNC": cand_a,
            "UBER": cand_b,
            "MBLY": cand_c,
        }

        rec = TimingEngine.evaluate_switching("SK_SQUARE", 76, evals)

        self.assertEqual(rec.status, "SWITCH_OPPORTUNITY")
        # Top candidate must be MBLY (tier STRONG_SWITCH, catalyst advantage 95 vs UBER's 90)
        self.assertEqual(rec.top_candidate_id, "MBLY")
        self.assertEqual(rec.candidates[0]["stockId"], "MBLY")
        self.assertEqual(rec.candidates[1]["stockId"], "UBER")
        self.assertEqual(rec.candidates[2]["stockId"], "FLNC")

    def test_missing_holding_stock_fallback(self):
        """When holding stock is absent from evaluations dict, engine must fallback safely without KeyError."""
        cand = TimingEngine.evaluate_stock("MBLY", 7.0, date="2026-10-12")
        evals = {"MBLY": cand}

        rec = TimingEngine.evaluate_switching("SK_SQUARE", 76, evals)
        self.assertEqual(rec.holding_stock_id, "SK_SQUARE")
        self.assertEqual(rec.holding_price, STOCK_REFERENCE_PRICES["SK_SQUARE"])
        self.assertIn("SK스퀘어", rec.summary)

    def test_zero_and_extreme_shares_fuzzing(self):
        """Zero or extreme shares must calculate valid strings without crash."""
        evals = {
            "SK_SQUARE": TimingEngine.evaluate_stock("SK_SQUARE", 1065000.0, date="2026-10-12"),
            "MBLY": TimingEngine.evaluate_stock("MBLY", 7.0, date="2026-10-12"),
        }

        for shares in [0, -10, 1000000]:
            rec = TimingEngine.evaluate_switching("SK_SQUARE", shares, evals)
            self.assertIsInstance(rec.holding_eval_amount, str)
            self.assertEqual(rec.holding_shares, shares)

    def test_invalid_date_formats_resilience(self):
        """Malformed date strings must fallback gracefully to default date without crashing."""
        for bad_date in ["not-a-date", "", "9999-99-99", "2026/10/12"]:
            cats = TimingEngine.get_catalysts("SK_HYNIX", as_of_date=bad_date)
            self.assertGreater(len(cats), 0)
            self.assertIsInstance(cats[0].days_remaining, int)

    def test_sk_hynix_dual_currency_normalization(self):
        """SK Hynix must seamlessly differentiate USD ADR vs domestic KRW ordinary shares."""
        # Case 1: USD ADR price ($170.0)
        eval_usd = TimingEngine.evaluate_stock("SK_HYNIX", 170.0)
        self.assertEqual(eval_usd.valuation_band.currency, "USD")
        self.assertEqual(eval_usd.valuation_band.min_price, 160.0)
        self.assertEqual(eval_usd.take_profit.tp1_price, 340.0)

        # Case 2: KRW Ordinary share price (1,700,000 KRW)
        eval_krw = TimingEngine.evaluate_stock("SK_HYNIX", 1700000.0)
        self.assertEqual(eval_krw.valuation_band.currency, "KRW")
        self.assertEqual(eval_krw.valuation_band.min_price, 1650000.0)
        self.assertEqual(eval_krw.take_profit.tp1_price, 3400000.0)

    def test_candidate_price_zero_scenario_freed_capital(self):
        """When candidate price is 0.0, scenario calculation must not throw ZeroDivisionError."""
        h_eval = TimingEngine.evaluate_stock("SK_SQUARE", 1065000.0, date="2026-10-12")
        h_eval.catalysts = [CatalystEvent("H", "2027-01-01", 100, "HIGH", "desc")]

        c_eval = TimingEngine.evaluate_stock("MBLY", 0.0, date="2026-10-12")
        c_eval.trigger.composite_score = 3
        c_eval.trigger.risk_reward_ratio = 50.0
        c_eval.catalysts = [CatalystEvent("C", "2026-10-22", 10, "HIGH", "desc")]

        evals = {"SK_SQUARE": h_eval, "MBLY": c_eval}
        rec = TimingEngine.evaluate_switching("SK_SQUARE", 76, evals)

        self.assertEqual(rec.status, "SWITCH_OPPORTUNITY")
        self.assertEqual(len(rec.scenarios), 1)
        self.assertEqual(rec.scenarios[0]["candidateShares"], "0주")


if __name__ == "__main__":
    unittest.main()

