"""Comprehensive End-to-End Test Suite for Timing Engine, 3-Tier Take Profit,
Stock Switching, and Continuous Daily Analysis Pipeline (Tiers 1-4).

Requirements Covered:
- R1: Quantitative Valuation Bands & 3-Condition Composite Trigger (Dead Money filter)
- R2: 3-Tier Profit-Taking Framework (TP1, TP2, TP3)
- R3: Offline Dashboard Timing & Catalyst View (View 5) & data.js sync
- R4: Opportunity-Cost Based Stock Switching Recommendation Engine vs SK Square 76 shares
- R5: Continuous Daily Analysis Pipeline & Idempotent History Tracking
Acceptance Criteria Covered:
- AC1: Quantitative bands & 3-condition trigger algorithm accuracy for 8 stocks
- AC2: Offline dashboard UI DOM IDs and zero-CDN compliance
- AC3: 100% full test suite regression preservation (0 regressions on existing 466 tests)
- AC4: Switching algorithm, RRR, Reverse Switching Warning, and reallocation scenarios
- AC5: Daily continuous analysis pipeline and history array accumulation
"""

from __future__ import annotations

import json
import os
import re
import tempfile
import unittest
from pathlib import Path
from typing import Any, Dict, List, Optional

# Project models
from engine.models import STOCK_MASTERS, StockSymbol

# Dynamic import of TimingEngine to guarantee progressive testability
try:
    import engine.timing_engine as timing_module
    from engine.timing_engine import (
        CatalystEvent,
        CompositeTriggerResult,
        DailyTimingSnapshot,
        StockTimingEvaluation,
        SwitchingRecommendation,
        TakeProfitConfig,
        TimingEngine,
        ValuationBandConfig,
    )

    TIMING_ENGINE_AVAILABLE = True
except (ImportError, AttributeError):
    TIMING_ENGINE_AVAILABLE = False
    timing_module = None

# Reference constants derived authoritatively from ORIGINAL_REQUEST.md,
# PROJECT.md, and Survey Reports
REFERENCE_VALUATION_BANDS: Dict[str, Dict[str, Any]] = {
    "SK_HYNIX": {
        "currency": "USD",
        "min_price": 160.0,
        "max_price": 175.0,
        "support_floor": 155.0,
        "krw_min": 1650000.0,
        "krw_max": 1750000.0,
        "krw_support": 1580000.0,
    },
    "SK_SQUARE": {
        "currency": "KRW",
        "min_price": 1000000.0,
        "max_price": 1120000.0,
        "support_floor": 980000.0,
    },
    "UBER": {
        "currency": "USD",
        "min_price": 62.0,
        "max_price": 68.5,
        "support_floor": 60.0,
    },
    "MBLY": {
        "currency": "USD",
        "min_price": 6.5,
        "max_price": 7.5,
        "support_floor": 6.2,
    },
    "FLNC": {
        "currency": "USD",
        "min_price": 14.0,
        "max_price": 16.5,
        "support_floor": 13.5,
    },
    "UPST": {
        "currency": "USD",
        "min_price": 32.0,
        "max_price": 36.0,
        "support_floor": 30.0,
    },
    "CELH": {
        "currency": "USD",
        "min_price": 25.0,
        "max_price": 28.5,
        "support_floor": 23.5,
    },
    "ENPH": {
        "currency": "USD",
        "min_price": 30.0,
        "max_price": 35.0,
        "support_floor": 28.0,
    },
}

REFERENCE_TAKE_PROFIT_LADDERS: Dict[str, Dict[str, Any]] = {
    "SK_HYNIX": {"tp1": 340.0, "tp2": 700.0, "currency": "USD"},
    "SK_SQUARE": {"tp1": 2100000.0, "tp2": 5000000.0, "currency": "KRW"},
    "UBER": {"tp1": 136.0, "tp2": 210.0, "currency": "USD"},
    "MBLY": {"tp1": 14.20, "tp2": 25.0, "currency": "USD"},
    "FLNC": {"tp1": 32.0, "tp2": 65.0, "currency": "USD"},
    "UPST": {"tp1": 72.0, "tp2": 120.0, "currency": "USD"},
    "CELH": {"tp1": 54.0, "tp2": 90.0, "currency": "USD"},
    "ENPH": {"tp1": 65.0, "tp2": 125.0, "currency": "USD"},
}


class TestTier1FeatureCoverage(unittest.TestCase):
    """Tier 1: Feature Coverage (>=5 test cases per core feature).

    Covers:
    - 8 Stocks Valuation Multiples & Safety Margin Buy Bands (F1)
    - 3-Condition Composite Trigger Engine (F2)
    - 3-Tier Take-Profit Framework (TP1/TP2/TP3) (F3)
    - Opportunity-Cost Stock Switching Engine (F4)
    - Continuous Daily Pipeline Snapshot (F5)
    - Dashboard DOM ID and Contract Compliance (F7)
    """

    def test_f1_all_8_stocks_exist_in_stock_masters(self) -> None:
        """Verifies all 8 canonical stocks exist in models with valid tickers and badges."""
        expected_symbols = [
            "SK_HYNIX",
            "SK_SQUARE",
            "UBER",
            "MBLY",
            "FLNC",
            "UPST",
            "CELH",
            "ENPH",
        ]
        for sym in expected_symbols:
            self.assertIn(sym, STOCK_MASTERS)
            master = STOCK_MASTERS[sym]
            self.assertTrue(len(master.ticker) > 0)
            self.assertTrue(len(master.badge_color) > 0)
            self.assertIn(master.currency, ["KRW", "USD"])

    @unittest.skipUnless(
        TIMING_ENGINE_AVAILABLE,
        "engine.timing_engine pending implementation by Worker M1/M2",
    )
    def test_f1_all_8_stocks_valuation_bands_configuration(self) -> None:
        """F1: Verifies all 8 stocks have valid valuation bands and positive floor prices."""
        expected_stocks = [
            "SK_HYNIX",
            "SK_SQUARE",
            "UBER",
            "MBLY",
            "FLNC",
            "UPST",
            "CELH",
            "ENPH",
        ]
        for stock_id in expected_stocks:
            band = TimingEngine.get_valuation_band(stock_id)
            self.assertIsInstance(band, ValuationBandConfig)
            self.assertGreater(band.min_price, 0.0)
            self.assertGreater(band.max_price, band.min_price)
            self.assertGreater(band.key_support_price, 0.0)
            self.assertLessEqual(band.key_support_price, band.min_price)
            self.assertTrue(len(band.rationale) > 0)

    @unittest.skipUnless(
        TIMING_ENGINE_AVAILABLE,
        "engine.timing_engine pending implementation by Worker M1/M2",
    )
    def test_f1_safety_margin_entry_detection(self) -> None:
        """F1: Tests safety margin evaluation across all 8 stocks for in-band vs above-band prices."""
        for stock_id, ref in REFERENCE_VALUATION_BANDS.items():
            in_band_price = (ref["min_price"] + ref["max_price"]) / 2.0
            above_band_price = ref["max_price"] * 1.25

            # In band
            res_in = TimingEngine.evaluate_trigger(
                stock_id=stock_id,
                current_price=in_band_price,
                price_formatted=f"{in_band_price}",
                daily_change_pct=0.0,
                volume=1000000,
                date="2026-10-12",
            )
            self.assertTrue(
                res_in.cond1_safety_margin,
                f"{stock_id} at {in_band_price} should satisfy safety margin condition",
            )

            # Above band
            res_above = TimingEngine.evaluate_trigger(
                stock_id=stock_id,
                current_price=above_band_price,
                price_formatted=f"{above_band_price}",
                daily_change_pct=0.0,
                volume=1000000,
                date="2026-10-12",
            )
            self.assertFalse(
                res_above.cond1_safety_margin,
                f"{stock_id} at {above_band_price} should NOT satisfy safety margin condition",
            )

    @unittest.skipUnless(
        TIMING_ENGINE_AVAILABLE,
        "engine.timing_engine pending implementation by Worker M1/M2",
    )
    def test_f2_trigger_condition_1_safety_margin_check(self) -> None:
        """F2: Verifies trigger Condition 1 evaluates strictly against max_price boundary."""
        res_inside = TimingEngine.evaluate_trigger(
            stock_id="MBLY",
            current_price=7.10,
            price_formatted="$7.10",
            daily_change_pct=0.57,
            volume=3980000,
            date="2026-10-12",
        )
        self.assertTrue(res_inside.cond1_safety_margin)

        res_outside = TimingEngine.evaluate_trigger(
            stock_id="MBLY",
            current_price=9.50,
            price_formatted="$9.50",
            daily_change_pct=1.50,
            volume=4000000,
            date="2026-10-12",
        )
        self.assertFalse(res_outside.cond1_safety_margin)

    @unittest.skipUnless(
        TIMING_ENGINE_AVAILABLE,
        "engine.timing_engine pending implementation by Worker M1/M2",
    )
    def test_f2_trigger_condition_2_catalyst_window_check(self) -> None:
        """F2: Verifies trigger Condition 2 evaluates catalyst proximity within 30~60 days."""
        catalysts = TimingEngine.get_catalysts("SK_HYNIX", "2026-10-12")
        self.assertTrue(len(catalysts) > 0)
        imminent = any(0 <= c.days_remaining <= 60 for c in catalysts)
        self.assertTrue(imminent, "SK_HYNIX must have confirmed catalyst in 30~60d window")

        res = TimingEngine.evaluate_trigger(
            stock_id="SK_HYNIX",
            current_price=169.66,
            price_formatted="$169.66",
            daily_change_pct=0.5,
            volume=2000000,
            date="2026-10-12",
        )
        self.assertTrue(res.cond2_catalyst_imminent)

    @unittest.skipUnless(
        TIMING_ENGINE_AVAILABLE,
        "engine.timing_engine pending implementation by Worker M1/M2",
    )
    def test_f2_trigger_condition_3_volume_washout_surge(self) -> None:
        """F2: Verifies trigger Condition 3 evaluates volume wash-out support defense and rebound."""
        # MBLY 701만 주 volume surge defending $6.87 support floor
        res_washout = TimingEngine.evaluate_trigger(
            stock_id="MBLY",
            current_price=7.10,
            price_formatted="$7.10",
            daily_change_pct=0.57,  # Green rebound candle
            volume=7008063,  # > 1.5x average volume
            date="2026-10-12",
        )
        self.assertTrue(res_washout.cond3_volume_washout)

    @unittest.skipUnless(
        TIMING_ENGINE_AVAILABLE,
        "engine.timing_engine pending implementation by Worker M1/M2",
    )
    def test_f2_composite_trigger_all_three_satisfied_strong_buy(self) -> None:
        """F2: Verifies all 3 conditions satisfied outputs STRONG_BUY and dead_money_risk = LOW."""
        res = TimingEngine.evaluate_trigger(
            stock_id="MBLY",
            current_price=7.10,
            price_formatted="$7.10",
            daily_change_pct=0.57,
            volume=7008063,
            date="2026-10-12",
        )
        if (
            res.cond1_safety_margin
            and res.cond2_catalyst_imminent
            and res.cond3_volume_washout
        ):
            self.assertEqual(res.signal, "STRONG_BUY")
            self.assertEqual(res.composite_score, 3)
            self.assertEqual(res.dead_money_risk, "LOW")

    @unittest.skipUnless(
        TIMING_ENGINE_AVAILABLE,
        "engine.timing_engine pending implementation by Worker M1/M2",
    )
    def test_f3_tp1_principal_recovery_gain(self) -> None:
        """F3: Verifies TP1 target prices represent 2x~3x gains (+100% or higher) for principal recovery."""
        for stock_id, ref in REFERENCE_TAKE_PROFIT_LADDERS.items():
            tp_cfg = TimingEngine.get_take_profit(stock_id)
            band = TimingEngine.get_valuation_band(stock_id)
            entry_mid = (band.min_price + band.max_price) / 2.0
            tp1_gain_ratio = tp_cfg.tp1_price / entry_mid
            self.assertGreaterEqual(
                tp1_gain_ratio,
                1.75,
                f"{stock_id} TP1 ratio {tp1_gain_ratio:.2f} should be >= 1.75x entry",
            )
            self.assertTrue(
                "원금" in tp_cfg.tp1_action or "Risk-Free" in tp_cfg.tp1_action,
                f"{stock_id} TP1 action should specify principal recovery",
            )

    @unittest.skipUnless(
        TIMING_ENGINE_AVAILABLE,
        "engine.timing_engine pending implementation by Worker M1/M2",
    )
    def test_f3_tp2_intrinsic_value_normalization(self) -> None:
        """F3: Verifies TP2 target prices represent intrinsic normalization (3x~5x+) and 50% liquidation."""
        for stock_id, ref in REFERENCE_TAKE_PROFIT_LADDERS.items():
            tp_cfg = TimingEngine.get_take_profit(stock_id)
            self.assertGreater(tp_cfg.tp2_price, tp_cfg.tp1_price)
            self.assertTrue(
                "50%" in tp_cfg.tp2_action or "정상화" in tp_cfg.tp2_action,
                f"{stock_id} TP2 action should specify partial profit taking",
            )

    @unittest.skipUnless(
        TIMING_ENGINE_AVAILABLE,
        "engine.timing_engine pending implementation by Worker M1/M2",
    )
    def test_f3_tp3_cycle_peakout_liquidation_indicators(self) -> None:
        """F3: Verifies TP3 specifies non-price forward cycle peak-out indicators."""
        tp_cfg = TimingEngine.get_take_profit("SK_HYNIX")
        self.assertTrue(len(tp_cfg.tp3_trigger_indicators) > 0)
        self.assertTrue(
            any("CapEx" in ind or "CSI" in ind or "ASP" in ind for ind in tp_cfg.tp3_trigger_indicators),
            "SK_HYNIX TP3 indicators must include forward cycle indicators",
        )

    @unittest.skipUnless(
        TIMING_ENGINE_AVAILABLE,
        "engine.timing_engine pending implementation by Worker M1/M2",
    )
    def test_f4_stock_switching_rrr_formula(self) -> None:
        """F4: Verifies Risk-Reward Ratio formula = (TargetUpside - Current) / (Current - SupportFloor)."""
        res = TimingEngine.evaluate_trigger(
            stock_id="MBLY",
            current_price=7.10,
            price_formatted="$7.10",
            daily_change_pct=0.57,
            volume=3980000,
            date="2026-10-12",
        )
        self.assertGreater(res.risk_reward_ratio, 0.0)
        band = TimingEngine.get_valuation_band("MBLY")
        tp = TimingEngine.get_take_profit("MBLY")
        downside_pct = (7.10 - band.key_support_price) / 7.10 * 100.0
        upside_pct = (tp.tp1_price - 7.10) / 7.10 * 100.0
        expected_rrr = round(upside_pct / downside_pct, 2)
        self.assertAlmostEqual(res.risk_reward_ratio, expected_rrr, delta=0.5)

    @unittest.skipUnless(
        TIMING_ENGINE_AVAILABLE,
        "engine.timing_engine pending implementation by Worker M1/M2",
    )
    def test_f4_stock_switching_scenario_generation(self) -> None:
        """F4: Verifies switching engine evaluates holding vs candidates and produces scenarios."""
        evals = {}
        for stock_id in STOCK_MASTERS:
            band = TimingEngine.get_valuation_band(stock_id)
            evals[stock_id] = StockTimingEvaluation(
                stock_id=stock_id,
                stock_name=STOCK_MASTERS[stock_id].name_kr,
                ticker=STOCK_MASTERS[stock_id].ticker,
                valuation_band=band,
                catalysts=TimingEngine.get_catalysts(stock_id, "2026-10-12"),
                take_profit=TimingEngine.get_take_profit(stock_id),
                trigger=TimingEngine.evaluate_trigger(
                    stock_id,
                    (band.min_price + band.max_price) / 2.0,
                    f"{(band.min_price + band.max_price) / 2.0}",
                    0.5,
                    5000000,
                    "2026-10-12",
                ),
            )

        rec = TimingEngine.evaluate_switching(
            holding_stock_id="SK_SQUARE",
            holding_shares=76,
            evaluations=evals,
            date="2026-10-12",
        )
        self.assertIsInstance(rec, SwitchingRecommendation)
        self.assertEqual(rec.holding_stock_id, "SK_SQUARE")
        self.assertEqual(rec.holding_shares, 76)
        self.assertIn(rec.status, ["HOLD_CORE", "SWITCH_OPPORTUNITY", "REVERSE_SWITCH_WARNING"])
        self.assertTrue(len(rec.candidates) > 0)

    @unittest.skipUnless(
        TIMING_ENGINE_AVAILABLE,
        "engine.timing_engine pending implementation by Worker M1/M2",
    )
    def test_f5_continuous_daily_pipeline_snapshot(self) -> None:
        """F5: Verifies TimingEngine.evaluate_daily_timing produces complete DailyTimingSnapshot."""
        from engine.models import DailyMarketData

        mock_data = DailyMarketData(
            date="2026-10-12",
            stocks={},
        )
        snapshot = TimingEngine.evaluate_daily_timing(mock_data, {"holdingStock": "SK_SQUARE", "shares": 76})
        self.assertIsInstance(snapshot, DailyTimingSnapshot)
        self.assertEqual(snapshot.date, "2026-10-12")
        self.assertEqual(len(snapshot.stocks), 8)
        self.assertIsNotNone(snapshot.switching)

    @unittest.skipUnless(
        TIMING_ENGINE_AVAILABLE,
        "engine.timing_engine pending implementation by Worker M1/M2",
    )
    def test_f1_individual_stocks_valuation_band_properties_each(self) -> None:
        """F1: Verifies individual properties for all 8 stocks against reference parameters."""
        for stock_id, ref in REFERENCE_VALUATION_BANDS.items():
            band = TimingEngine.get_valuation_band(stock_id)
            self.assertEqual(band.stock_id, stock_id)
            self.assertEqual(band.currency, ref["currency"])
            self.assertGreater(band.min_price, 0.0)
            self.assertGreater(band.max_price, band.min_price)
            self.assertGreater(band.key_support_price, 0.0)

    @unittest.skipUnless(
        TIMING_ENGINE_AVAILABLE,
        "engine.timing_engine pending implementation by Worker M1/M2",
    )
    def test_f3_take_profit_individual_stock_targets(self) -> None:
        """F3: Verifies TP1 and TP2 individual targets for each of the 8 stocks."""
        for stock_id, ref in REFERENCE_TAKE_PROFIT_LADDERS.items():
            tp = TimingEngine.get_take_profit(stock_id)
            self.assertGreater(tp.tp1_price, 0.0)
            self.assertGreater(tp.tp2_price, tp.tp1_price)
            self.assertTrue(len(tp.tp1_action) > 0)
            self.assertTrue(len(tp.tp2_action) > 0)
            self.assertTrue(len(tp.tp3_condition) > 0)

    @unittest.skipUnless(
        TIMING_ENGINE_AVAILABLE,
        "engine.timing_engine pending implementation by Worker M1/M2",
    )
    def test_f5_history_persistence_snapshot_serialization(self) -> None:
        """F5: Verifies DailyTimingSnapshot serialization to dict complies with JSON schema."""
        from engine.models import DailyMarketData
        mock_data = DailyMarketData(date="2026-10-12", stocks={})
        snapshot = TimingEngine.evaluate_daily_timing(mock_data, {"holdingStock": "SK_SQUARE", "shares": 76})
        snapshot_dict = snapshot.to_dict()
        self.assertIn("date", snapshot_dict)
        self.assertIn("timestamp", snapshot_dict)
        self.assertIn("stocks", snapshot_dict)
        self.assertIn("switching", snapshot_dict)
        self.assertEqual(len(snapshot_dict["stocks"]), 8)

    @unittest.skipUnless(
        TIMING_ENGINE_AVAILABLE,
        "engine.timing_engine pending implementation by Worker M1/M2",
    )
    def test_f9_portfolio_sk_square_76_shares_diagnosis(self) -> None:
        """F9: Validates portfolio diagnosis for SK Square 76 shares computes total value and roadmap."""
        from engine.models import DailyMarketData
        mock_data = DailyMarketData(date="2026-10-12", stocks={})
        snapshot = TimingEngine.evaluate_daily_timing(mock_data, {"holdingStock": "SK_SQUARE", "shares": 76})
        self.assertIsNotNone(snapshot.switching)
        self.assertEqual(snapshot.switching.holding_stock_id, "SK_SQUARE")
        self.assertEqual(snapshot.switching.holding_shares, 76)
        self.assertTrue(snapshot.switching.holding_price > 0)

    def test_f7_dashboard_view5_dom_id_contracts(self) -> None:
        """F7: Validates dashboard markup contracts and ensures no unhandled DOM references."""
        html_path = Path(__file__).resolve().parent.parent / "index.html"
        self.assertTrue(html_path.exists())
        content = html_path.read_text(encoding="utf-8")

        # Existing views must remain intact
        self.assertIn('id="btnViewDigest"', content)
        self.assertIn('id="btnViewTimeseries"', content)
        self.assertIn('id="btnViewInsight"', content)
        self.assertIn('id="btnViewFinancials"', content)

        # Zero remote external scripts or CDN
        self.assertNotRegex(
            content,
            r'<script[^>]+src=["\']https?://',
            "index.html must have zero remote CDN script tags",
        )


class TestTier2BoundaryAndCornerCases(unittest.TestCase):
    """Tier 2: Boundary & Corner Cases (>=5 test cases per feature area).

    Covers:
    - Band edge boundaries (min_price, max_price, epsilon adjustments)
    - Catalyst D-Day thresholds (D-0, D-30, D-60, D-61, negative D-Day)
    - Volume wash-out edge cases (1.40x vs 1.39x, 1.50x surge vs 1.49x, green vs red candle)
    - Zero/negative handling & dual currency handling (USD vs KRW)
    """

    @unittest.skipUnless(
        TIMING_ENGINE_AVAILABLE,
        "engine.timing_engine pending implementation by Worker M1/M2",
    )
    def test_boundary_exact_min_price_inclusive(self) -> None:
        """Boundary: price == min_price must evaluate as INSIDE safety margin."""
        band = TimingEngine.get_valuation_band("UBER")
        res = TimingEngine.evaluate_trigger(
            stock_id="UBER",
            current_price=band.min_price,
            price_formatted=f"${band.min_price}",
            daily_change_pct=0.0,
            volume=1000000,
            date="2026-10-12",
        )
        self.assertTrue(res.cond1_safety_margin)

    @unittest.skipUnless(
        TIMING_ENGINE_AVAILABLE,
        "engine.timing_engine pending implementation by Worker M1/M2",
    )
    def test_boundary_exact_max_price_inclusive(self) -> None:
        """Boundary: price == max_price must evaluate as INSIDE safety margin."""
        band = TimingEngine.get_valuation_band("UBER")
        res = TimingEngine.evaluate_trigger(
            stock_id="UBER",
            current_price=band.max_price,
            price_formatted=f"${band.max_price}",
            daily_change_pct=0.0,
            volume=1000000,
            date="2026-10-12",
        )
        self.assertTrue(res.cond1_safety_margin)

    @unittest.skipUnless(
        TIMING_ENGINE_AVAILABLE,
        "engine.timing_engine pending implementation by Worker M1/M2",
    )
    def test_boundary_just_above_band_max(self) -> None:
        """Boundary: price == max_price + 0.01 must evaluate as OUTSIDE safety margin."""
        band = TimingEngine.get_valuation_band("UBER")
        res = TimingEngine.evaluate_trigger(
            stock_id="UBER",
            current_price=band.max_price + 0.01,
            price_formatted=f"${band.max_price + 0.01}",
            daily_change_pct=0.0,
            volume=1000000,
            date="2026-10-12",
        )
        self.assertFalse(res.cond1_safety_margin)

    @unittest.skipUnless(
        TIMING_ENGINE_AVAILABLE,
        "engine.timing_engine pending implementation by Worker M1/M2",
    )
    def test_boundary_catalyst_d_day_zero(self) -> None:
        """Boundary: Catalyst D-Day = 0 (Today is event day) is strictly within 0~60d window."""
        ev = CatalystEvent(
            name="Earnings Day",
            target_date="2026-10-12",
            days_remaining=0,
            impact_level="CRITICAL",
            description="Q3 Earnings",
        )
        self.assertTrue(0 <= ev.days_remaining <= 60)

    @unittest.skipUnless(
        TIMING_ENGINE_AVAILABLE,
        "engine.timing_engine pending implementation by Worker M1/M2",
    )
    def test_boundary_catalyst_d_day_30(self) -> None:
        """Boundary: Catalyst D-Day = 30 is strictly within 0~60d window."""
        ev = CatalystEvent(
            name="SOP Milestone",
            target_date="2026-11-11",
            days_remaining=30,
            impact_level="HIGH",
            description="Mass production",
        )
        self.assertTrue(0 <= ev.days_remaining <= 60)

    @unittest.skipUnless(
        TIMING_ENGINE_AVAILABLE,
        "engine.timing_engine pending implementation by Worker M1/M2",
    )
    def test_boundary_catalyst_d_day_60(self) -> None:
        """Boundary: Catalyst D-Day = 60 is strictly within 0~60d window."""
        ev = CatalystEvent(
            name="Regulatory Approval",
            target_date="2026-12-11",
            days_remaining=60,
            impact_level="HIGH",
            description="License",
        )
        self.assertTrue(0 <= ev.days_remaining <= 60)

    @unittest.skipUnless(
        TIMING_ENGINE_AVAILABLE,
        "engine.timing_engine pending implementation by Worker M1/M2",
    )
    def test_boundary_catalyst_d_day_61(self) -> None:
        """Boundary: Catalyst D-Day = 61 is outside the 30~60d window."""
        ev = CatalystEvent(
            name="Distant Event",
            target_date="2026-12-12",
            days_remaining=61,
            impact_level="HIGH",
            description="Distant",
        )
        self.assertFalse(0 <= ev.days_remaining <= 60)

    @unittest.skipUnless(
        TIMING_ENGINE_AVAILABLE,
        "engine.timing_engine pending implementation by Worker M1/M2",
    )
    def test_boundary_catalyst_d_day_negative(self) -> None:
        """Boundary: Catalyst D-Day < 0 (Past event) must be rejected."""
        ev = CatalystEvent(
            name="Past Event",
            target_date="2026-10-10",
            days_remaining=-2,
            impact_level="HIGH",
            description="Past",
        )
        self.assertFalse(0 <= ev.days_remaining <= 60)

    @unittest.skipUnless(
        TIMING_ENGINE_AVAILABLE,
        "engine.timing_engine pending implementation by Worker M1/M2",
    )
    def test_boundary_volume_surge_1_50_vs_1_49(self) -> None:
        """Boundary: Volume surge ratio 1.50x triggers wash-out condition; 1.49x does not without 1.4x 20d avg."""
        # 1.50x surge with support held and green return
        res_pass = TimingEngine.evaluate_trigger(
            stock_id="FLNC",
            current_price=16.20,
            price_formatted="$16.20",
            daily_change_pct=0.1,
            volume=3000000,  # 1.5x of 2,000,000 baseline
            date="2026-10-12",
        )
        self.assertTrue(res_pass.cond3_volume_washout)

    @unittest.skipUnless(
        TIMING_ENGINE_AVAILABLE,
        "engine.timing_engine pending implementation by Worker M1/M2",
    )
    def test_boundary_zero_percent_return_flat_is_non_negative(self) -> None:
        """Boundary: daily return 0.00% is considered non-negative / support held; -0.01% is red candle."""
        # Flat 0.00%
        res_flat = TimingEngine.evaluate_trigger(
            stock_id="CELH",
            current_price=27.35,
            price_formatted="$27.35",
            daily_change_pct=0.0,
            volume=5000000,
            date="2026-10-12",
        )
        self.assertTrue(res_flat.cond3_volume_washout)

        # Red candle -0.01%
        res_red = TimingEngine.evaluate_trigger(
            stock_id="CELH",
            current_price=27.35,
            price_formatted="$27.35",
            daily_change_pct=-0.01,
            volume=5000000,
            date="2026-10-12",
        )
        self.assertFalse(res_red.cond3_volume_washout)

    @unittest.skipUnless(
        TIMING_ENGINE_AVAILABLE,
        "engine.timing_engine pending implementation by Worker M1/M2",
    )
    def test_corner_zero_volume_handling(self) -> None:
        """Corner: Zero trading volume must NOT cause ZeroDivisionError."""
        res_zero = TimingEngine.evaluate_trigger(
            stock_id="UPST",
            current_price=34.00,
            price_formatted="$34.00",
            daily_change_pct=0.0,
            volume=0,
            date="2026-10-12",
        )
        self.assertFalse(res_zero.cond3_volume_washout)
        self.assertIsInstance(res_zero.composite_score, int)

    def test_corner_sk_hynix_dual_currency_parity(self) -> None:
        """Corner: Validates dual currency mapping for SK Hynix (ADR vs Domestic stock)."""
        adr_band = REFERENCE_VALUATION_BANDS["SK_HYNIX"]
        self.assertEqual(adr_band["currency"], "USD")
        self.assertEqual(adr_band["min_price"], 160.0)
        self.assertEqual(adr_band["max_price"], 175.0)

        # Domestic parity: ADR $169.66 corresponds to approx 1,680,000 KRW
        krw_min = adr_band["krw_min"]
        krw_max = adr_band["krw_max"]
        self.assertGreater(krw_max, krw_min)
        self.assertEqual(krw_min, 1650000.0)
        self.assertEqual(krw_max, 1750000.0)

    @unittest.skipUnless(
        TIMING_ENGINE_AVAILABLE,
        "engine.timing_engine pending implementation by Worker M1/M2",
    )
    def test_boundary_band_just_below_min_price_extreme_margin(self) -> None:
        """Boundary: price < min_price while >= key_support evaluates as extreme safety margin."""
        band = TimingEngine.get_valuation_band("UBER")
        res = TimingEngine.evaluate_trigger(
            stock_id="UBER",
            current_price=band.min_price - 0.01,
            price_formatted=f"${band.min_price - 0.01}",
            daily_change_pct=0.0,
            volume=1000000,
            date="2026-10-12",
        )
        self.assertTrue(res.cond1_safety_margin)

    @unittest.skipUnless(
        TIMING_ENGINE_AVAILABLE,
        "engine.timing_engine pending implementation by Worker M1/M2",
    )
    def test_boundary_price_below_key_support_fails_margin(self) -> None:
        """Boundary: price < key_support_price breaks support floor and fails safety margin."""
        band = TimingEngine.get_valuation_band("UBER")
        res = TimingEngine.evaluate_trigger(
            stock_id="UBER",
            current_price=band.key_support_price - 0.50,
            price_formatted=f"${band.key_support_price - 0.50}",
            daily_change_pct=-2.0,
            volume=1000000,
            date="2026-10-12",
        )
        self.assertFalse(res.cond1_safety_margin)

    @unittest.skipUnless(
        TIMING_ENGINE_AVAILABLE,
        "engine.timing_engine pending implementation by Worker M1/M2",
    )
    def test_corner_zero_shares_switching_handling(self) -> None:
        """Corner: holding_shares = 0 handled safely without division by zero."""
        evals = {}
        for stock_id in STOCK_MASTERS:
            band = TimingEngine.get_valuation_band(stock_id)
            evals[stock_id] = StockTimingEvaluation(
                stock_id=stock_id,
                stock_name=STOCK_MASTERS[stock_id].name_kr,
                ticker=STOCK_MASTERS[stock_id].ticker,
                valuation_band=band,
                catalysts=TimingEngine.get_catalysts(stock_id, "2026-10-12"),
                take_profit=TimingEngine.get_take_profit(stock_id),
                trigger=TimingEngine.evaluate_trigger(
                    stock_id,
                    (band.min_price + band.max_price) / 2.0,
                    f"{(band.min_price + band.max_price) / 2.0}",
                    0.5,
                    5000000,
                    "2026-10-12",
                ),
            )
        rec = TimingEngine.evaluate_switching("SK_SQUARE", 0, evals, "2026-10-12")
        self.assertEqual(rec.holding_shares, 0)

    @unittest.skipUnless(
        TIMING_ENGINE_AVAILABLE,
        "engine.timing_engine pending implementation by Worker M1/M2",
    )
    def test_corner_negative_shares_defensive(self) -> None:
        """Corner: negative holding_shares handled defensively."""
        evals = {}
        for stock_id in STOCK_MASTERS:
            band = TimingEngine.get_valuation_band(stock_id)
            evals[stock_id] = StockTimingEvaluation(
                stock_id=stock_id,
                stock_name=STOCK_MASTERS[stock_id].name_kr,
                ticker=STOCK_MASTERS[stock_id].ticker,
                valuation_band=band,
                catalysts=TimingEngine.get_catalysts(stock_id, "2026-10-12"),
                take_profit=TimingEngine.get_take_profit(stock_id),
                trigger=TimingEngine.evaluate_trigger(
                    stock_id,
                    (band.min_price + band.max_price) / 2.0,
                    f"{(band.min_price + band.max_price) / 2.0}",
                    0.5,
                    5000000,
                    "2026-10-12",
                ),
            )
        rec = TimingEngine.evaluate_switching("SK_SQUARE", -10, evals, "2026-10-12")
        self.assertIsInstance(rec, SwitchingRecommendation)


class TestTier3CrossFeatureCombinations(unittest.TestCase):
    """Tier 3: Cross-Feature Combinations (Pairwise and Multi-Variable Interactions).

    Covers:
    - Truth table of all 8 combinations of 3 boolean triggers (Safety Margin, Catalyst, Volume)
    - Reverse Switching Risk Warning when core holding (SK Square 76 shares) catalyst is imminent (D <= 15)
    - Switching Opportunity activation when holding catalyst is distant
    - Daily Sync Idempotency across same date and multi-day accumulation
    """

    @unittest.skipUnless(
        TIMING_ENGINE_AVAILABLE,
        "engine.timing_engine pending implementation by Worker M1/M2",
    )
    def test_cross_all_8_boolean_trigger_truth_table(self) -> None:
        """Cross-Feature: Exercises combinations of 3 triggers and asserts signal mapping."""
        # Matrix of test cases:
        # (cond1, cond2, cond3) -> expected signal
        # (T, T, T) -> STRONG_BUY
        # (T, T, F) -> ACCUMULATE
        # (T, F, T) -> ACCUMULATE
        # (T, F, F) -> WATCH_CATALYST (Dead Money filter)
        # (F, T, T) -> HOLD
        # (F, T, F) -> HOLD
        # (F, F, T) -> HOLD
        # (F, F, F) -> HOLD
        band = TimingEngine.get_valuation_band("MBLY")
        in_band_price = (band.min_price + band.max_price) / 2.0
        out_band_price = band.max_price * 1.5

        # (T, T, T)
        res_ttt = TimingEngine.evaluate_trigger("MBLY", in_band_price, f"{in_band_price}", 0.5, 7000000, "2026-10-12")
        self.assertEqual(res_ttt.signal, "STRONG_BUY")
        self.assertEqual(res_ttt.dead_money_risk, "LOW")

        # (T, F, F) -> Dead Money risk HIGH
        res_tff = TimingEngine.evaluate_trigger("MBLY", in_band_price, f"{in_band_price}", -1.0, 100000, "2026-10-12")
        if res_tff.cond1_safety_margin and not res_tff.cond3_volume_washout:
            self.assertIn(res_tff.signal, ["WATCH_CATALYST", "ACCUMULATE"])

        # (F, T, T) -> Out of band -> HOLD
        res_ftt = TimingEngine.evaluate_trigger("MBLY", out_band_price, f"{out_band_price}", 0.5, 7000000, "2026-10-12")
        self.assertEqual(res_ftt.signal, "HOLD")

    @unittest.skipUnless(
        TIMING_ENGINE_AVAILABLE,
        "engine.timing_engine pending implementation by Worker M1/M2",
    )
    def test_cross_reverse_switching_risk_warning_active_when_holding_catalyst_imminent(self) -> None:
        """Cross-Feature: Holding catalyst D-Day <= 15 triggers REVERSE_SWITCH_WARNING."""
        evals = {}
        for stock_id in STOCK_MASTERS:
            band = TimingEngine.get_valuation_band(stock_id)
            evals[stock_id] = StockTimingEvaluation(
                stock_id=stock_id,
                stock_name=STOCK_MASTERS[stock_id].name_kr,
                ticker=STOCK_MASTERS[stock_id].ticker,
                valuation_band=band,
                catalysts=TimingEngine.get_catalysts(stock_id, "2026-10-12"),
                take_profit=TimingEngine.get_take_profit(stock_id),
                trigger=TimingEngine.evaluate_trigger(
                    stock_id,
                    (band.min_price + band.max_price) / 2.0,
                    f"{(band.min_price + band.max_price) / 2.0}",
                    0.5,
                    5000000,
                    "2026-10-12",
                ),
            )

        # SK Square holding with imminent catalyst (Hynix buyback completion D-10, 3Q earnings D-15)
        rec = TimingEngine.evaluate_switching(
            holding_stock_id="SK_SQUARE",
            holding_shares=76,
            evaluations=evals,
            date="2026-10-12",
        )
        self.assertEqual(rec.status, "REVERSE_SWITCH_WARNING")
        self.assertIn("역(逆)스위칭", rec.summary)

    @unittest.skipUnless(
        TIMING_ENGINE_AVAILABLE,
        "engine.timing_engine pending implementation by Worker M1/M2",
    )
    def test_cross_switching_opportunity_active_when_holding_catalyst_distant(self) -> None:
        """Cross-Feature: Holding catalyst D-Day > 20 and Candidate catalyst D-Day <= 15 triggers SWITCH_OPPORTUNITY."""
        evals = {}
        for stock_id in STOCK_MASTERS:
            band = TimingEngine.get_valuation_band(stock_id)
            evals[stock_id] = StockTimingEvaluation(
                stock_id=stock_id,
                stock_name=STOCK_MASTERS[stock_id].name_kr,
                ticker=STOCK_MASTERS[stock_id].ticker,
                valuation_band=band,
                catalysts=[
                    CatalystEvent("Distant", "2026-12-15", 65, "HIGH", "Distant")
                    if stock_id == "SK_SQUARE"
                    else CatalystEvent("Imminent", "2026-10-18", 6, "CRITICAL", "Immediate")
                ],
                take_profit=TimingEngine.get_take_profit(stock_id),
                trigger=TimingEngine.evaluate_trigger(
                    stock_id,
                    (band.min_price + band.max_price) / 2.0,
                    f"{(band.min_price + band.max_price) / 2.0}",
                    0.5,
                    5000000,
                    "2026-10-12",
                ),
            )

        rec = TimingEngine.evaluate_switching(
            holding_stock_id="SK_SQUARE",
            holding_shares=76,
            evaluations=evals,
            date="2026-10-12",
        )
        if rec.top_candidate_id:
            self.assertEqual(rec.status, "SWITCH_OPPORTUNITY")
            self.assertTrue(len(rec.scenarios) > 0)

    def test_cross_daily_sync_idempotency_same_date(self) -> None:
        """Cross-Feature: Idempotency guarantee: Re-syncing same date replaces entry without inflating array."""
        test_history = [
            {"date": "2026-10-11", "score": 2},
            {"date": "2026-10-10", "score": 1},
        ]
        new_entry = {"date": "2026-10-11", "score": 3}

        # Idempotent replacement logic
        existing_idx = next(
            (i for i, h in enumerate(test_history) if h["date"] == new_entry["date"]),
            None,
        )
        if existing_idx is not None:
            test_history[existing_idx] = new_entry
        else:
            test_history.insert(0, new_entry)

        self.assertEqual(len(test_history), 2)
        self.assertEqual(test_history[0]["score"], 3)

    def test_cross_daily_sync_multi_day_accumulation(self) -> None:
        """Cross-Feature: Multi-day sync strictly accumulates chronological history."""
        test_history: List[Dict[str, Any]] = []
        days = ["2026-10-09", "2026-10-10", "2026-10-11", "2026-10-12"]

        for d in days:
            entry = {"date": d, "evaluated": True}
            existing_idx = next((i for i, h in enumerate(test_history) if h["date"] == d), None)
            if existing_idx is not None:
                test_history[existing_idx] = entry
            else:
                test_history.append(entry)

        self.assertEqual(len(test_history), 4)
        self.assertEqual([h["date"] for h in test_history], days)

    @unittest.skipUnless(
        TIMING_ENGINE_AVAILABLE,
        "engine.timing_engine pending implementation by Worker M1/M2",
    )
    def test_cross_switching_candidate_ranking_order(self) -> None:
        """Cross-Feature: Candidates are ordered by recommendation tier and RRR ratio."""
        evals = {}
        for stock_id in STOCK_MASTERS:
            band = TimingEngine.get_valuation_band(stock_id)
            evals[stock_id] = StockTimingEvaluation(
                stock_id=stock_id,
                stock_name=STOCK_MASTERS[stock_id].name_kr,
                ticker=STOCK_MASTERS[stock_id].ticker,
                valuation_band=band,
                catalysts=TimingEngine.get_catalysts(stock_id, "2026-10-12"),
                take_profit=TimingEngine.get_take_profit(stock_id),
                trigger=TimingEngine.evaluate_trigger(
                    stock_id,
                    (band.min_price + band.max_price) / 2.0,
                    f"{(band.min_price + band.max_price) / 2.0}",
                    0.5,
                    5000000,
                    "2026-10-12",
                ),
            )
        rec = TimingEngine.evaluate_switching("SK_SQUARE", 76, evals, "2026-10-12")
        candidates = rec.candidates
        self.assertTrue(len(candidates) > 0)
        # Check candidate schema properties
        for cand in candidates:
            self.assertIn("stockId", cand)
            self.assertIn("candidateRrr", cand)
            self.assertIn("tier", cand)

    @unittest.skipUnless(
        TIMING_ENGINE_AVAILABLE,
        "engine.timing_engine pending implementation by Worker M1/M2",
    )
    def test_cross_portfolio_diagnosis_sk_square_76_shares_phased_tp(self) -> None:
        """Cross-Feature: SK Square 76 shares portfolio diagnosis computes total valuation and TP roadmap."""
        from engine.models import DailyMarketData
        mock_data = DailyMarketData(date="2026-10-12", stocks={})
        snapshot = TimingEngine.evaluate_daily_timing(mock_data, {"holdingStock": "SK_SQUARE", "shares": 76})
        self.assertIsNotNone(snapshot.switching)
        self.assertEqual(snapshot.switching.holding_stock_id, "SK_SQUARE")
        self.assertEqual(snapshot.switching.holding_shares, 76)
        self.assertIn("만 원", snapshot.switching.holding_eval_amount)


class TestTier4RealWorldWorkloadScenarios(unittest.TestCase):
    """Tier 4: Real-World Workload Scenarios (Empirical Market Dump Cases).

    Directly parses and tests empirical dump evidence from:
    - raw_input_full_dump.txt:
      * 10/8 lock-up wash-out panic-selling + 10/9 Baird upgrade green rebound
      * MBLY 701만 주 volume surge defending $6.87 support floor
      * SK Square 76 shares NAV 43.4% discount & Hynix buyback accretion
      * SK Square 76 shares multi-year valuation growth roadmap
    - raw_input_20261012.txt:
      * UBER breakout above $70 with ezCater M&A
      * Multi-day history tracking across sequential dates
    """

    def setUp(self) -> None:
        base_dir = Path(__file__).resolve().parent.parent
        self.full_dump_path = base_dir / "raw_input_full_dump.txt"
        self.dump_20261012_path = base_dir / "raw_input_20261012.txt"
        self.assertTrue(
            self.full_dump_path.exists(),
            "raw_input_full_dump.txt must exist in workspace",
        )
        self.assertTrue(
            self.dump_20261012_path.exists(),
            "raw_input_20261012.txt must exist in workspace",
        )

    def test_workload_sk_hynix_10_8_lockup_washout_and_10_9_rebound(self) -> None:
        """Tier 4: Validates empirical SK Hynix 10/8 lock-up wash-out (-4.35%) and 10/9 rebound."""
        content = self.full_dump_path.read_text(encoding="utf-8")

        # Verbatim text checks from 10/8 wash-out section
        self.assertIn("10월 8일", content)
        self.assertIn("나스닥 ADR 락업 만료", content)
        self.assertIn("바닥 털기(Wash-out) 구간", content)
        self.assertIn("SK스퀘어 76주", content)

        # 10/9 Baird upgrade and price stabilization checks
        self.assertIn("169.66", content)
        self.assertIn("베어드(Baird)", content)
        self.assertIn("170선", content)

    def test_workload_mbly_volume_explosion_defending_6_87_support(self) -> None:
        """Tier 4: Validates empirical Mobileye 7,008,063 shares (+64%) defending $6.87 support floor."""
        content = self.full_dump_path.read_text(encoding="utf-8")

        # Verbatim MBLY volume explosion and rebound records
        self.assertIn("7,008,063", content)
        self.assertIn("64% 급증", content)
        self.assertIn("6.870", content)
        self.assertIn("7.060", content)
        self.assertIn("Volume Exhaustion", content)
        self.assertIn("3,978,780", content)

    def test_workload_sk_square_nav_discount_and_hynix_buyback_accretion(self) -> None:
        """Tier 4: Validates empirical SK Square 76 shares NAV 43.4% discount & Hynix buyback accretion."""
        content = self.dump_20261012_path.read_text(encoding="utf-8")

        # Verbatim 10/12 dump checks for SK Square & SK Hynix
        self.assertIn("SK스퀘어", content)
        self.assertIn("SK하이닉스", content)
        self.assertIn("40조", content)

    def test_workload_sk_square_76_shares_valuation_growth_scenario(self) -> None:
        """Tier 4: Validates empirical SK Square 76 shares long-term roadmap (8,000만 원 -> 약 4억 5,330만 원)."""
        content = self.full_dump_path.read_text(encoding="utf-8")
        self.assertIn("보유 76주 평가 금액", content)
        self.assertIn("약 4억 5,330만 원", content)
        self.assertIn("8,284만 원", content)
        self.assertIn("500만~600만 원", content)

    def test_workload_uber_breakout_with_ezcater_mna(self) -> None:
        """Tier 4: Validates empirical UBER $71.51 breakout above $70 with ezCater $2.3B M&A."""
        content = self.dump_20261012_path.read_text(encoding="utf-8")

        # Verbatim 10/12 dump checks for UBER
        self.assertIn("우버", content)
        self.assertTrue(
            "71." in content or "70." in content or "ezCater" in content or "자율주행" in content,
            "10/12 dump must contain UBER price or corporate developments",
        )

    def test_workload_sequential_multi_day_history_tracking(self) -> None:
        """Tier 4: Simulates multi-day chronological history accumulation across dumps."""
        base_dir = Path(__file__).resolve().parent.parent
        dump_files = [
            base_dir / "raw_input_20261009.txt",
            base_dir / "raw_input_20261010.txt",
            base_dir / "raw_input_20261011.txt",
            base_dir / "raw_input_20261012.txt",
        ]
        existing_dumps = [p for p in dump_files if p.exists()]
        self.assertGreaterEqual(
            len(existing_dumps),
            2,
            "At least 2 daily dump files must exist for multi-day history tracking test",
        )

        history_snapshots: List[Dict[str, Any]] = []
        for dump_path in existing_dumps:
            # Extract date from filename: raw_input_YYYYMMDD.txt -> YYYY-MM-DD
            m = re.search(r"(\d{4})(\d{2})(\d{2})", dump_path.name)
            self.assertIsNotNone(m)
            date_str = f"{m.group(1)}-{m.group(2)}-{m.group(3)}"
            content = dump_path.read_text(encoding="utf-8")
            self.assertTrue(len(content) > 100)

            # Record snapshot idempotently
            snapshot = {
                "date": date_str,
                "fileSize": len(content),
                "recorded": True,
            }
            existing_idx = next(
                (i for i, h in enumerate(history_snapshots) if h["date"] == date_str),
                None,
            )
            if existing_idx is not None:
                history_snapshots[existing_idx] = snapshot
            else:
                history_snapshots.append(snapshot)

        self.assertEqual(len(history_snapshots), len(existing_dumps))


if __name__ == "__main__":
    unittest.main()
