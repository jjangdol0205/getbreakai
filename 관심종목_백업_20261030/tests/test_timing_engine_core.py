"""Unit tests for Timing Engine Core (Milestone M1).

Verifies:
1. Data models and serialization (ValuationBandConfig, CatalystEvent, TakeProfitConfig,
   CompositeTriggerResult, StockTimingEvaluation, SwitchingRecommendation, DailyTimingSnapshot)
2. Quantitative valuation bands and downside floors for all 8 stocks
3. Confirmed catalysts mapping, impact levels, and exact D-Day countdown math
4. 3-Condition composite trigger evaluation:
   (1) Safety margin band entry
   (2) Confirmed catalyst proximity (30~60 days)
   (3) Volume wash-out support defense and green rebound candle
   -> Signals: STRONG_BUY, ACCUMULATE, WATCH_CATALYST, HOLD, TAKE_PROFIT, RRR, downside/upside %
5. 3-Tier profit-taking configurations (TP1, TP2, TP3)
6. Switching opportunity and reverse-switching warning logic
7. Daily timing snapshot generation and DailyMarketData integration
8. Edge cases: malformed dates, zero/negative prices, volume thresholds, dual currency
"""

import json
import unittest
from datetime import date, timedelta

from engine.models import DailyMarketData, MarketMetrics, StockFactSheet
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


class TestTimingEngineDataModels(unittest.TestCase):
    """Test data class structures, fields, and to_dict / JSON serialization."""

    def test_valuation_band_config_serialization(self):
        band = TimingEngine.get_valuation_band("SK_SQUARE")
        self.assertIsInstance(band, ValuationBandConfig)
        d = band.to_dict()
        self.assertEqual(d["stock_id"], "SK_SQUARE")
        self.assertEqual(d["currency"], "KRW")
        self.assertIn("min_price", d)
        self.assertIn("max_price", d)
        self.assertIn("key_support_price", d)
        # Ensure json serializable
        json_str = json.dumps(d)
        self.assertIn("SK_SQUARE", json_str)

    def test_catalyst_event_serialization(self):
        cat = CatalystEvent(
            name="Q3 실적 발표",
            target_date="2026-10-27",
            days_remaining=15,
            impact_level="CRITICAL",
            description="분기 실적 발표 및 배당 결의",
            is_confirmed=True,
        )
        d = cat.to_dict()
        self.assertEqual(d["name"], "Q3 실적 발표")
        self.assertEqual(d["days_remaining"], 15)
        self.assertTrue(d["is_confirmed"])

    def test_take_profit_config_serialization(self):
        tp = TimingEngine.get_take_profit("UBER")
        self.assertIsInstance(tp, TakeProfitConfig)
        d = tp.to_dict()
        self.assertEqual(d["tp1_price"], 140.0)
        self.assertEqual(d["tp2_price"], 210.0)
        self.assertIsInstance(d["tp3_trigger_indicators"], list)
        self.assertTrue(len(d["tp3_trigger_indicators"]) >= 3)

    def test_composite_trigger_result_serialization(self):
        res = TimingEngine.evaluate_trigger(
            stock_id="MBLY",
            current_price=7.10,
            daily_change_pct=0.57,
            volume=7008063,
            date="2026-10-12",
        )
        self.assertIsInstance(res, CompositeTriggerResult)
        d = res.to_dict()
        self.assertEqual(d["stock_id"], "MBLY")
        self.assertIn("composite_score", d)
        self.assertIn("signal", d)
        self.assertIn("risk_reward_ratio", d)
        json_str = json.dumps(d)
        self.assertIn("MBLY", json_str)


class TestValuationBandsAllStocks(unittest.TestCase):
    """Test quantitative valuation bands and downside floors for all 8 canonical stocks."""

    CANONICAL_STOCKS = [
        "SK_HYNIX", "SK_SQUARE", "UBER", "MBLY", "FLNC", "UPST", "CELH", "ENPH"
    ]

    def test_all_8_stocks_valuation_bands_exist_and_valid(self):
        for sid in self.CANONICAL_STOCKS:
            band = TimingEngine.get_valuation_band(sid)
            self.assertEqual(band.stock_id, sid)
            self.assertGreater(band.max_price, band.min_price)
            self.assertGreater(band.min_price, 0.0)
            self.assertGreater(band.key_support_price, 0.0)
            self.assertLessEqual(band.key_support_price, band.min_price)
            self.assertTrue(len(band.rationale) > 10)
            self.assertTrue(len(band.metric_type) > 0)

    def test_sk_hynix_dual_currency_adaptation(self):
        # USD ADR (default when price <= 10000)
        band_usd = TimingEngine.get_valuation_band("SK_HYNIX", current_price=169.66)
        self.assertEqual(band_usd.currency, "USD")
        self.assertEqual(band_usd.min_price, 160.0)
        self.assertEqual(band_usd.max_price, 175.0)
        self.assertEqual(band_usd.key_support_price, 155.0)

        # KRW Domestic (when price > 10000)
        band_krw = TimingEngine.get_valuation_band("SK_HYNIX", current_price=1681000.0)
        self.assertEqual(band_krw.currency, "KRW")
        self.assertEqual(band_krw.min_price, 1650000.0)
        self.assertEqual(band_krw.max_price, 1750000.0)
        self.assertEqual(band_krw.key_support_price, 1580000.0)

    def test_unknown_stock_raises_value_error(self):
        with self.assertRaises(ValueError):
            TimingEngine.get_valuation_band("UNKNOWN_STOCK_XYZ")


class TestConfirmedCatalystsAndDDay(unittest.TestCase):
    """Test catalyst mapping, impact levels, and exact D-Day countdown math."""

    def test_catalysts_exist_for_all_8_stocks(self):
        for sid in TestValuationBandsAllStocks.CANONICAL_STOCKS:
            cats = TimingEngine.get_catalysts(sid, as_of_date="2026-10-12")
            self.assertGreaterEqual(len(cats), 2)
            for c in cats:
                self.assertIn(c.impact_level, ("HIGH", "CRITICAL"))
                self.assertTrue(c.is_confirmed)
                self.assertTrue(len(c.description) > 5)

    def test_exact_d_day_calculation(self):
        # As of 2026-10-12, SK_HYNIX 3Q earnings is 2026-10-27 -> exactly 15 days
        cats = TimingEngine.get_catalysts("SK_HYNIX", as_of_date="2026-10-12")
        earnings_cat = next(c for c in cats if "실적 발표" in c.name)
        self.assertEqual(earnings_cat.target_date, "2026-10-27")
        self.assertEqual(earnings_cat.days_remaining, 15)

        # As of 2026-10-25, D-Day should be exactly 2
        cats_later = TimingEngine.get_catalysts("SK_HYNIX", as_of_date="2026-10-25")
        earnings_cat_later = next(c for c in cats_later if "실적 발표" in c.name)
        self.assertEqual(earnings_cat_later.days_remaining, 2)

        # As of 2026-10-28 (passed), D-Day should be -1
        cats_past = TimingEngine.get_catalysts("SK_HYNIX", as_of_date="2026-10-28")
        earnings_cat_past = next(c for c in cats_past if "실적 발표" in c.name)
        self.assertEqual(earnings_cat_past.days_remaining, -1)


class TestTakeProfitFrameworkAllStocks(unittest.TestCase):
    """Test 3-Tier profit-taking framework (TP1, TP2, TP3) for all 8 stocks."""

    def test_all_8_stocks_take_profit_rules(self):
        for sid in TestValuationBandsAllStocks.CANONICAL_STOCKS:
            tp = TimingEngine.get_take_profit(sid)
            band = TimingEngine.get_valuation_band(sid)

            # TP1 must represent ~2x from entry band
            self.assertGreater(tp.tp1_price, band.max_price)
            self.assertGreaterEqual(tp.tp1_gain_pct, 90.0)

            # TP2 must be significantly higher than TP1 (~3x-5x)
            self.assertGreater(tp.tp2_price, tp.tp1_price)
            self.assertGreaterEqual(tp.tp2_gain_pct, 190.0)

            # TP3 must contain structural peak-out indicators
            self.assertTrue(len(tp.tp3_condition) > 10)
            self.assertEqual(tp.tp3_action, "잔여 비중 100% 전량 청산")
            self.assertGreaterEqual(len(tp.tp3_trigger_indicators), 3)

    def test_sk_hynix_dual_currency_take_profit(self):
        tp_usd = TimingEngine.get_take_profit("SK_HYNIX", current_price=170.0)
        self.assertEqual(tp_usd.tp1_price, 340.0)
        self.assertEqual(tp_usd.tp2_price, 700.0)

        tp_krw = TimingEngine.get_take_profit("SK_HYNIX", current_price=1700000.0)
        self.assertEqual(tp_krw.tp1_price, 3400000.0)
        self.assertEqual(tp_krw.tp2_price, 7000000.0)


class TestCompositeTriggerEvaluation(unittest.TestCase):
    """Test 3-Condition Composite Trigger Engine across market scenarios."""

    def test_strong_buy_when_all_3_conditions_met(self):
        # Mobileye (MBLY) scenario:
        # 1. Price $7.10 in safety margin band ($6.50 ~ $7.50) -> Cond 1 = True
        # 2. Confirmed catalyst in 18 days (AI paper 10/30) -> Cond 2 = True
        # 3. Volume 7,008,063 shares (> 1.4x 20d avg 4,260,000), holds support $6.20, green rebound +0.57% -> Cond 3 = True
        res = TimingEngine.evaluate_trigger(
            stock_id="MBLY",
            current_price=7.10,
            daily_change_pct=0.57,
            volume=7008063,
            date="2026-10-12",
        )
        self.assertTrue(res.cond1_safety_margin)
        self.assertTrue(res.cond2_catalyst_imminent)
        self.assertTrue(res.cond3_volume_washout)
        self.assertEqual(res.composite_score, 3)
        self.assertEqual(res.signal, "STRONG_BUY")
        self.assertEqual(res.dead_money_risk, "LOW")
        self.assertGreater(res.risk_reward_ratio, 3.0)

    def test_washout_selloff_day_red_candle_rejects_cond3(self):
        # 10/8 Lock-up drop scenario: heavy volume but negative return (red candle)
        # Cond 1 = True, Cond 2 = True, Cond 3 = False (washout in progress, not yet rebound)
        res = TimingEngine.evaluate_trigger(
            stock_id="MBLY",
            current_price=6.87,
            daily_change_pct=-4.35,
            volume=7008063,
            date="2026-10-12",
        )
        self.assertTrue(res.cond1_safety_margin)
        self.assertTrue(res.cond2_catalyst_imminent)
        self.assertFalse(res.cond3_volume_washout)
        self.assertEqual(res.composite_score, 2)
        self.assertEqual(res.signal, "ACCUMULATE")
        self.assertEqual(res.dead_money_risk, "MEDIUM")

    def test_watch_catalyst_when_only_condition1_met(self):
        # Price in band, but catalyst distant (>60d) and no volume surge/rebound
        res = TimingEngine.evaluate_trigger(
            stock_id="FLNC",
            current_price=16.20,
            daily_change_pct=-0.50,
            volume=500000,
            date="2026-08-01",  # 2.5 months before catalysts
        )
        self.assertTrue(res.cond1_safety_margin)
        self.assertFalse(res.cond2_catalyst_imminent)
        self.assertFalse(res.cond3_volume_washout)
        self.assertEqual(res.composite_score, 1)
        self.assertEqual(res.signal, "WATCH_CATALYST")
        self.assertEqual(res.dead_money_risk, "HIGH")

    def test_hold_when_price_above_safety_margin_band(self):
        # UBER at $71.51 is above buy band max $68.50, but below TP1 $140
        res = TimingEngine.evaluate_trigger(
            stock_id="UBER",
            current_price=71.51,
            daily_change_pct=1.50,
            volume=16540000,
            date="2026-10-12",
        )
        self.assertFalse(res.cond1_safety_margin)
        self.assertEqual(res.signal, "HOLD")

    def test_take_profit_when_price_exceeds_tp1(self):
        # SK_SQUARE price hits 2,250,000 KRW (above TP1 2,200,000 KRW)
        res = TimingEngine.evaluate_trigger(
            stock_id="SK_SQUARE",
            current_price=2250000.0,
            daily_change_pct=2.00,
            volume=120000,
            date="2026-10-12",
        )
        self.assertEqual(res.signal, "TAKE_PROFIT")
        self.assertIn("TP1 달성", res.signal_label)


class TestSwitchingRecommendationEngine(unittest.TestCase):
    """Test opportunity-cost switching and reverse-switching warning."""

    def setUp(self):
        self.evaluations = {}
        for sid in TestValuationBandsAllStocks.CANONICAL_STOCKS:
            ref_p = STOCK_REFERENCE_PRICES[sid]
            self.evaluations[sid] = TimingEngine.evaluate_stock(
                stock_id=sid,
                current_price=ref_p,
                daily_change_pct=0.5,
                volume=STOCK_BENCHMARK_20D_VOLUME.get(sid, 100000),
                date="2026-10-12",
            )

    def test_reverse_switching_warning_when_holding_catalyst_imminent(self):
        # SK_SQUARE has buyback catalyst in 10 days (2026-10-22) as of 2026-10-12
        # Engine MUST trigger REVERSE_SWITCH_WARNING to prevent panic selling
        rec = TimingEngine.evaluate_switching(
            holding_stock_id="SK_SQUARE",
            holding_shares=76,
            evaluations=self.evaluations,
            date="2026-10-12",
        )
        self.assertIsInstance(rec, SwitchingRecommendation)
        self.assertEqual(rec.status, "REVERSE_SWITCH_WARNING")
        self.assertIn("역(逆)스위칭 리스크 경고", rec.summary)
        self.assertEqual(rec.holding_shares, 76)
        self.assertIn("8,094만 원", rec.holding_eval_amount)

    def test_switch_opportunity_when_candidate_has_superior_rrr_and_catalyst(self):
        # Simulate scenario where holding stock catalyst is distant (months away)
        # while MBLY has imminent catalyst (D-5) and score 3
        custom_evals = dict(self.evaluations)
        # Create distant holding evaluation
        holding_eval = TimingEngine.evaluate_stock(
            stock_id="SK_SQUARE",
            current_price=1065000.0,
            date="2026-06-01",  # catalysts are months away
        )
        custom_evals["SK_SQUARE"] = holding_eval

        # Create strong MBLY evaluation with immediate D-5 catalyst
        mbly_eval = TimingEngine.evaluate_stock(
            stock_id="MBLY",
            current_price=7.10,
            daily_change_pct=1.2,
            volume=7500000,
            date="2026-10-25",  # MBLY 10/30 catalyst is D-5
        )
        custom_evals["MBLY"] = mbly_eval

        rec = TimingEngine.evaluate_switching(
            holding_stock_id="SK_SQUARE",
            holding_shares=76,
            evaluations=custom_evals,
            date="2026-10-25",
        )
        self.assertEqual(rec.status, "SWITCH_OPPORTUNITY")
        self.assertEqual(rec.top_candidate_id, "MBLY")
        self.assertTrue(len(rec.scenarios) > 0)
        self.assertIn("15주", rec.scenarios[0]["title"])


class TestDailyTimingSnapshot(unittest.TestCase):
    """Test full daily timing snapshot pipeline and serialization."""

    def test_evaluate_daily_timing_with_daily_market_data(self):
        from engine.models import STOCK_MASTERS, StockSymbol

        md = DailyMarketData(date="2026-10-12")
        mbly_master = STOCK_MASTERS[StockSymbol.MBLY]
        sq_master = STOCK_MASTERS[StockSymbol.SK_SQUARE]

        md.stocks["MBLY"] = StockFactSheet(
            stock_id="MBLY",
            stock_name=mbly_master.name_kr,
            name_kr=mbly_master.name_kr,
            name_en=mbly_master.name_en,
            ticker=mbly_master.ticker,
            market=mbly_master.market,
            category=mbly_master.category,
            badge_color=mbly_master.badge_color,
            metrics=MarketMetrics(
                stock_id="MBLY",
                close_price=7.10,
                close_price_formatted="$7.10",
                change_percent=0.57,
                volume=7008063,
            ),
        )
        md.stocks["SK_SQUARE"] = StockFactSheet(
            stock_id="SK_SQUARE",
            stock_name=sq_master.name_kr,
            name_kr=sq_master.name_kr,
            name_en=sq_master.name_en,
            ticker=sq_master.ticker,
            market=sq_master.market,
            category=sq_master.category,
            badge_color=sq_master.badge_color,
            metrics=MarketMetrics(
                stock_id="SK_SQUARE",
                close_price=1065000.0,
                close_price_formatted="1,065,000원",
                change_percent=1.43,
                volume=92500,
            ),
        )

        snapshot = TimingEngine.evaluate_daily_timing(
            market_data=md,
            portfolio={"holdingStock": "SK_SQUARE", "shares": 76},
            as_of_date="2026-10-12",
        )

        self.assertIsInstance(snapshot, DailyTimingSnapshot)
        self.assertEqual(snapshot.date, "2026-10-12")
        self.assertEqual(len(snapshot.stocks), 8)
        self.assertIn("SK_HYNIX", snapshot.stocks)
        self.assertIn("MBLY", snapshot.stocks)

        # Verify to_dict output schema matches PROJECT.md interface contract
        d = snapshot.to_dict()
        self.assertIn("date", d)
        self.assertIn("stocks", d)
        self.assertIn("switching", d)
        self.assertEqual(len(d["stocks"]), 8)

        # JSON round-trip test
        json_output = json.dumps(d, ensure_ascii=False)
        self.assertIn("MBLY", json_output)
        self.assertIn("SK_SQUARE", json_output)


class TestTimingEngineEdgeCases(unittest.TestCase):
    """Test edge cases: zero/negative prices, boundary volumes, malformed dates."""

    def test_zero_and_negative_price_handling(self):
        res = TimingEngine.evaluate_trigger(
            stock_id="UBER",
            current_price=0.0,
            date="2026-10-12",
        )
        self.assertFalse(res.cond1_safety_margin)
        self.assertEqual(res.downside_risk_pct, 0.0)
        self.assertEqual(res.risk_reward_ratio, 0.0)

        res_neg = TimingEngine.evaluate_trigger(
            stock_id="UBER",
            current_price=-10.0,
            date="2026-10-12",
        )
        self.assertFalse(res_neg.cond1_safety_margin)

    def test_zero_volume_handling(self):
        res = TimingEngine.evaluate_trigger(
            stock_id="ENPH",
            current_price=33.0,
            daily_change_pct=1.0,
            volume=0,
            date="2026-10-12",
        )
        self.assertFalse(res.cond3_volume_washout)

    def test_malformed_date_defaults_safely(self):
        cats = TimingEngine.get_catalysts("SK_HYNIX", as_of_date="INVALID_DATE_FORMAT")
        self.assertGreaterEqual(len(cats), 2)
        # Should not raise exception


if __name__ == "__main__":
    unittest.main()
