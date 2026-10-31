"""Empirical Adversarial Audit Suite for Milestone M1 Remediation.

Author: Challenger 1 (teamwork_preview_challenger_m1_revamp_1)
Mission:
Adversarially re-verify the 4 critical remediation fixes:
1. Volume wash-out 1-share bypass elimination.
2. Downside risk and RRR stabilization on broken support.
3. Non-finite price ingestion (NaN, Inf, -Inf, None).
4. Multi-currency switching and dynamic share allocation.
"""

from __future__ import annotations

import math
import unittest
from typing import Dict

from engine.timing_engine import (
    CompositeTriggerResult,
    STOCK_BENCHMARK_20D_VOLUME,
    STOCK_REFERENCE_PRICES,
    SwitchingRecommendation,
    TimingEngine,
)


class TestWashoutBypassAdversarial(unittest.TestCase):
    """Adversarially probe volume wash-out condition to guarantee no bypass exists."""

    def test_volume_1_share_rejection(self):
        """Passing volume=1 share on a flat day (+0.00%) must NOT satisfy Cond3 or trigger STRONG_BUY."""
        for sid in ["UBER", "SK_SQUARE", "MBLY", "SK_HYNIX"]:
            band = TimingEngine.get_valuation_band(sid)
            p = band.min_price
            res = TimingEngine.evaluate_trigger(
                stock_id=sid,
                current_price=p,
                daily_change_pct=0.0,
                volume=1,
                date="2026-10-12",
            )
            self.assertFalse(res.cond3_volume_washout, f"{sid}: 1-share trade must NOT satisfy Cond 3")
            self.assertNotEqual(res.signal, "STRONG_BUY", f"{sid}: 1-share trade must NOT produce STRONG_BUY")
            self.assertIn("거래량 바닥 탈출 수급 미확인", res.cond3_detail)

    def test_volume_zero_rejection(self):
        """Passing volume=0 must NOT satisfy Cond3."""
        for sid in ["UBER", "SK_SQUARE", "MBLY"]:
            band = TimingEngine.get_valuation_band(sid)
            p = band.min_price
            res = TimingEngine.evaluate_trigger(
                stock_id=sid,
                current_price=p,
                daily_change_pct=1.0,
                volume=0,
                date="2026-10-12",
            )
            self.assertFalse(res.cond3_volume_washout)

    def test_volume_below_threshold_rejection(self):
        """Volume ratio 1.39x benchmark (< 1.4x threshold) must NOT satisfy Cond3."""
        sid = "UBER"
        bench = STOCK_BENCHMARK_20D_VOLUME[sid]
        vol_sub = int(bench * 1.39)
        res = TimingEngine.evaluate_trigger(
            stock_id=sid,
            current_price=65.0,
            daily_change_pct=1.0,
            volume=vol_sub,
            date="2026-10-12",
        )
        self.assertFalse(res.cond3_volume_washout)
        self.assertIn("거래량 바닥 탈출 수급 미확인", res.cond3_detail)

    def test_volume_at_or_above_threshold_acceptance(self):
        """Volume ratio >= 1.4x benchmark with positive rebound and support held must satisfy Cond3."""
        sid = "UBER"
        bench = STOCK_BENCHMARK_20D_VOLUME[sid]
        vol_surge = int(bench * 1.45)
        res = TimingEngine.evaluate_trigger(
            stock_id=sid,
            current_price=65.0,
            daily_change_pct=1.0,
            volume=vol_surge,
            date="2026-10-12",
        )
        self.assertTrue(res.cond3_volume_washout)
        self.assertEqual(res.signal, "STRONG_BUY")


class TestBrokenSupportDownsideAdversarial(unittest.TestCase):
    """Adversarially probe downside risk and RRR calculation on broken support floors."""

    def test_mbly_6_00_downside_and_rrr(self):
        """MBLY at $6.00 (support $6.20, TP1 $15.00) must properly penalize downside and eliminate 1500x RRR."""
        res = TimingEngine.evaluate_trigger("MBLY", 6.00, date="2026-10-12")
        # Breach distance = (6.20 - 6.00) / 6.00 * 100 = 3.33%
        # Downside risk = 3.33% + 10.0% penalty = 13.33%
        self.assertEqual(res.downside_risk_pct, 13.33)
        # Upside TP1 = (15.00 - 6.00) / 6.00 * 100 = 150.0%
        self.assertEqual(res.upside_tp1_pct, 150.0)
        # RRR = 150.0 / 13.33 = 11.25
        self.assertEqual(res.risk_reward_ratio, 11.25)
        self.assertLess(res.risk_reward_ratio, 50.0, "RRR must not be artificially inflated to 1500x")

    def test_downside_support_boundary(self):
        """At exact support boundary P == S, downside risk must be 0.0% without division-by-zero."""
        for sid in ["MBLY", "UBER", "SK_SQUARE"]:
            band = TimingEngine.get_valuation_band(sid)
            res = TimingEngine.evaluate_trigger(sid, band.key_support_price, date="2026-10-12")
            self.assertEqual(res.downside_risk_pct, 0.0)
            self.assertGreater(res.risk_reward_ratio, 0.0)

    def test_downside_severe_breach_proportionality(self):
        """Severe price collapse (e.g. 50% below support) scales downside risk monotonically and penalizes RRR."""
        band = TimingEngine.get_valuation_band("MBLY")
        supp = band.key_support_price  # 6.20
        # 50% below support -> P = 3.10
        # Breach distance = (6.20 - 3.10) / 3.10 * 100 = 100.0%
        # Downside risk = 100.0 + 10.0 = 110.0%
        res = TimingEngine.evaluate_trigger("MBLY", supp * 0.5, date="2026-10-12")
        self.assertEqual(res.downside_risk_pct, 110.0)
        # Upside TP1 = (15.00 - 3.10) / 3.10 * 100 = 383.87%
        # RRR = 383.87 / 110.0 = 3.49
        self.assertEqual(res.risk_reward_ratio, 3.49)


class TestNonFinitePriceAdversarial(unittest.TestCase):
    """Adversarially probe non-finite price inputs (NaN, Inf, -Inf, None) across KRW and USD tickers."""

    def test_krw_and_usd_non_finite_inputs(self):
        """NaN, Inf, -Inf, and None must evaluate safely without unhandled exceptions."""
        stocks = ["SK_SQUARE", "SK_HYNIX", "UBER", "MBLY", "ENPH"]
        bad_inputs = [float("nan"), float("inf"), float("-inf"), None]

        for sid in stocks:
            for bad_p in bad_inputs:
                with self.subTest(stock=sid, price=bad_p):
                    try:
                        res = TimingEngine.evaluate_trigger(sid, bad_p, date="2026-10-12")
                    except Exception as exc:
                        self.fail(f"Unhandled exception for {sid} with price {bad_p}: {exc}")

                    self.assertIsInstance(res, CompositeTriggerResult)
                    self.assertEqual(res.current_price_formatted, "N/A")
                    self.assertFalse(res.cond1_safety_margin)
                    self.assertEqual(res.cond1_detail, "가격 데이터 결손")
                    self.assertEqual(res.risk_reward_ratio, 0.0)
                    self.assertEqual(res.downside_risk_pct, 0.0)
                    self.assertEqual(res.upside_tp1_pct, 0.0)
                    self.assertEqual(res.signal, "HOLD")


class TestMultiCurrencySwitchingAdversarial(unittest.TestCase):
    """Adversarially probe multi-currency switching, dynamic capital conversion, and share allocation."""

    def setUp(self):
        self.evals = {
            sid: TimingEngine.evaluate_stock(
                sid, TimingEngine.get_valuation_band(sid).min_price, date="2026-08-01"
            )
            for sid in STOCK_BENCHMARK_20D_VOLUME
        }
        # Inject MBLY as top candidate
        self.evals["MBLY"] = TimingEngine.evaluate_stock(
            "MBLY", 7.10, daily_change_pct=1.0, volume=7000000, date="2026-10-12"
        )

    def test_usd_holding_asset_evaluation_and_parity(self):
        """Holding USD stock (e.g. UBER 100 shares @ $65.0) formats dual currency and converts freed capital accurately."""
        self.evals["UBER"] = TimingEngine.evaluate_stock("UBER", 65.0, date="2026-08-01")
        rec = TimingEngine.evaluate_switching("UBER", 100, self.evals, date="2026-10-12")

        # 100 shares * $65.0 = $6,500.00 -> 6500 * 1380 = 8,970,000 KRW = 약 897만 원
        self.assertIn("$6,500.00", rec.holding_eval_amount)
        self.assertIn("897만 원", rec.holding_eval_amount)

        self.assertGreaterEqual(len(rec.scenarios), 1)
        scenario = rec.scenarios[0]

        # 15 shares reallocated -> 15 * $65.0 * 1380 = 1,345,500 KRW = 약 134만 원
        self.assertEqual(scenario["freedCapital"], "약 134만 원")
        # Candidate MBLY @ $7.10 -> 1,345,500 / 1380 / 7.10 = 137.46 -> 137 shares
        self.assertEqual(scenario["candidateShares"], "137주")
        self.assertIn("15주", scenario["title"])

    def test_dynamic_share_allocation_bounds(self):
        """Holding fewer than 15 shares scales reallocated shares dynamically and never proposes short sales."""
        self.evals["UBER"] = TimingEngine.evaluate_stock("UBER", 65.0, date="2026-08-01")

        # Holding 5 shares
        rec_5 = TimingEngine.evaluate_switching("UBER", 5, self.evals, date="2026-10-12")
        self.assertEqual(len(rec_5.scenarios), 1)
        scen_5 = rec_5.scenarios[0]
        self.assertIn("5주", scen_5["title"])
        self.assertNotIn("15주", scen_5["title"])
        # 5 * $65.0 * 1380 = 448,500 KRW = 약 44만 원
        self.assertEqual(scen_5["freedCapital"], "약 44만 원")
        # 448,500 / 1380 / 7.10 = 45 shares
        self.assertEqual(scen_5["candidateShares"], "45주")

        # Holding 0 shares -> 0 scenarios
        rec_0 = TimingEngine.evaluate_switching("UBER", 0, self.evals, date="2026-10-12")
        self.assertEqual(len(rec_0.scenarios), 0)


if __name__ == "__main__":
    unittest.main()
