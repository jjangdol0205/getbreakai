"""
Adversarial & Empirical Stress Test Suite for primary_feed_us_cn.py (Milestone 1)
Author: challenger_m1_1 (Empirical Challenger)
Target: engine/primary_feed_us_cn.py and generate_morning_pdf.py

Verification Dimensions:
1. Offline Network Failure Simulation:
   - All 15 proxies (MU, NVDA, AVGO, SMH, XLV, QQQ, EWY, KORU, 0981.HK, 002371.SZ, 2408.TW, KRW=X, ^TNX, 402340.KS, 000660.KS)
   - Mock network failure (ConnectionError, Timeout) falling back to Tier 2 local CSV
   - No None, NaN, or Inf in calculated quote metrics
2. Wilder RSI(14) Edge Cases:
   - Zero variance (flat series) -> exactly 50.0
   - Monomorphic up series -> 100.0
   - Monomorphic down series -> 0.0
   - Row count boundaries (len=14, len=15, len=13, len=1)
   - Alternating series & extreme price shocks (+100%, -50%)
3. CSV Input Robustness:
   - Out-of-order / reversed / shuffled Date sorting
   - Comma separators, dollar signs ($), won signs (₩), and whitespace stripping
4. 52-Week Metrics Edge Cases:
   - At 52W High (DD52 = 0.0%)
   - At 52W Low (Prox52 = 0.0%)
   - Sub-252 row history (w52 = min(252, len(df)))
   - Zero or non-positive price guards
   - 252-day rolling window isolating spikes older than 252 trading days
   - Missing optional columns (High, Low, Volume) and missing Date column
5. Media Blacklist Firewall Adversarial Defense:
   - URL-encoded & double-encoded parameters (hl=ko, gl=KR, ceid=KR:ko)
   - Shorthand brokerage names & English institutions
   - Zero false-positive rejection of valid US/China primary sources
6. Market Snapshot Interface Contract:
   - Full snapshot generation offline and contract verification
"""

import math
import os
import sys
import unittest
from datetime import datetime
from unittest.mock import patch
import pandas as pd
import numpy as np

# Add repository root to path
REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)

from engine.primary_feed_us_cn import (
    PROXIES_META,
    SYMBOL_ALIASES,
    assert_zero_korean_media,
    build_primary_news_feed,
    compute_quote_metrics,
    fetch_market_snapshot,
    fetch_proxy_quotes,
    fetch_ticker_df,
    find_blacklisted_media,
    get_safe_csv_names,
    normalize_symbol,
)


class TestOfflineProxyIngestion(unittest.TestCase):
    """Stress tests Tier 2 offline fallback and quote calculations for all 15 proxies."""

    EXPECTED_15_PROXIES = [
        "MU", "NVDA", "AVGO", "SMH", "XLV", "QQQ", "EWY", "KORU",
        "0981.HK", "002371.SZ", "2408.TW", "KRW=X", "^TNX", "402340.KS", "000660.KS"
    ]

    REQUIRED_METRIC_FIELDS = [
        "ticker", "name", "market", "currency", "date",
        "close", "prev_close", "chg1d", "chg5d", "chg20d",
        "hi52", "lo52", "dd52", "prox52",
        "ma20", "ma60", "ma200", "vs_ma20", "vs_ma60", "vs_ma200",
        "rsi14", "vol_ratio",
    ]

    def test_all_15_proxies_in_meta(self):
        """Verifies that PROXIES_META defines exactly all 15 proxies."""
        for p in self.EXPECTED_15_PROXIES:
            self.assertIn(p, PROXIES_META, f"Missing proxy {p} in PROXIES_META")

    def test_all_15_proxies_offline_fallback(self):
        """Verifies that every single one of the 15 proxies falls back to local CSV with valid metrics."""
        for proxy in self.EXPECTED_15_PROXIES:
            can_sym, df = fetch_ticker_df(proxy, force_offline=True)
            self.assertEqual(can_sym, proxy, f"Canonical symbol mismatch for {proxy}")
            self.assertIsNotNone(df, f"Offline fallback failed: df is None for proxy {proxy}")
            self.assertGreater(len(df), 20, f"DataFrame too short ({len(df)}) for proxy {proxy}")

            # Compute quote metrics
            q = compute_quote_metrics(df, proxy)
            self.assertIsInstance(q, dict, f"compute_quote_metrics did not return a dict for {proxy}")

            # Verify every required field is present and non-null/non-NaN
            for field in self.REQUIRED_METRIC_FIELDS:
                self.assertIn(field, q, f"Field '{field}' missing in quote metrics for {proxy}")
                val = q[field]
                self.assertIsNotNone(val, f"Field '{field}' is None for {proxy}")
                if isinstance(val, (int, float)):
                    self.assertFalse(math.isnan(val), f"Field '{field}' is NaN for {proxy}")
                    self.assertFalse(math.isinf(val), f"Field '{field}' is Inf for {proxy}")

            # Positive price checks
            self.assertGreater(q["close"], 0, f"Close price must be > 0 for {proxy}")
            self.assertGreater(q["hi52"], 0, f"52W High must be > 0 for {proxy}")
            self.assertGreater(q["lo52"], 0, f"52W Low must be > 0 for {proxy}")
            self.assertLessEqual(q["lo52"], q["hi52"], f"52W Low > 52W High for {proxy}")

    def test_mock_network_exception_fallback(self):
        """Verifies that network exceptions (Timeout, ConnectionError, 500) trigger Tier 2 CSV fallback."""
        import requests

        with patch("requests.get", side_effect=requests.exceptions.ConnectTimeout("Simulated Network Timeout")):
            for proxy in ["NVDA", "402340.KS", "SMH", "KRW=X"]:
                can_sym, df = fetch_ticker_df(proxy, force_offline=False)
                self.assertIsNotNone(df, f"Failed to fall back to Tier 2 on timeout for {proxy}")
                self.assertGreater(len(df), 20)

        with patch("requests.get", side_effect=requests.exceptions.ConnectionError("Simulated DNS Failure")):
            for proxy in ["MU", "000660.KS", "0981.HK"]:
                can_sym, df = fetch_ticker_df(proxy, force_offline=False)
                self.assertIsNotNone(df, f"Failed to fall back to Tier 2 on ConnectionError for {proxy}")
                self.assertGreater(len(df), 20)

    def test_fetch_proxy_quotes_coverage_and_aliases(self):
        """Verifies fetch_proxy_quotes returns all 15 proxies and standard aliases."""
        quotes = fetch_proxy_quotes(force_offline=True)
        self.assertGreaterEqual(len(quotes), 15)

        for p in self.EXPECTED_15_PROXIES:
            self.assertIn(p, quotes, f"Proxy {p} missing in fetch_proxy_quotes output")

        # Test aliases
        aliases_to_check = ["SK_SQUARE", "SK_HYNIX", "USD/KRW", "TNX", "0981_HK", "002371_SZ", "2408_TW"]
        for a in aliases_to_check:
            self.assertIn(a, quotes, f"Alias {a} missing in fetch_proxy_quotes output")
            can = normalize_symbol(a)
            self.assertEqual(quotes[a]["close"], quotes[can]["close"])

    def test_real_local_csv_files_detailed_metrics(self):
        """Deep mathematical property audit on actual local CSV data for all 15 proxies."""
        quotes = fetch_proxy_quotes(force_offline=True)
        for sym in self.EXPECTED_15_PROXIES:
            q = quotes[sym]

            # 1. RSI(14) must strictly be bounded [0.0, 100.0]
            self.assertGreaterEqual(q["rsi14"], 0.0, f"{sym} RSI14 < 0.0: {q['rsi14']}")
            self.assertLessEqual(q["rsi14"], 100.0, f"{sym} RSI14 > 100.0: {q['rsi14']}")

            # 2. DD52 must strictly be <= 0.0 (distance from 52-week peak)
            self.assertLessEqual(q["dd52"], 0.0001, f"{sym} DD52 > 0: {q['dd52']}")

            # 3. Prox52 must strictly be >= 0.0 (distance above 52-week trough)
            self.assertGreaterEqual(q["prox52"], -0.0001, f"{sym} Prox52 < 0: {q['prox52']}")

            # 4. 52W High must be >= Close and 52W Low must be <= Close
            self.assertGreaterEqual(q["hi52"], q["close"] - 1e-3, f"{sym} hi52 < close")
            self.assertLessEqual(q["lo52"], q["close"] + 1e-3, f"{sym} lo52 > close")

            # 5. Price metrics must be strictly positive
            self.assertGreater(q["close"], 0.0, f"{sym} close <= 0")
            self.assertGreater(q["prev_close"], 0.0, f"{sym} prev_close <= 0")
            self.assertGreater(q["ma20"], 0.0, f"{sym} ma20 <= 0")
            self.assertGreater(q["ma60"], 0.0, f"{sym} ma60 <= 0")
            self.assertGreater(q["ma200"], 0.0, f"{sym} ma200 <= 0")

            # 6. Volume ratio must be non-negative
            self.assertGreaterEqual(q["vol_ratio"], 0.0, f"{sym} vol_ratio < 0")


class TestWilderRSIEdgeCases(unittest.TestCase):
    """Stress tests Wilder's RSI(14) edge cases."""

    def _make_df(self, prices):
        dates = pd.date_range("2026-01-01", periods=len(prices), freq="D").strftime("%Y-%m-%d")
        return pd.DataFrame({"Date": dates, "Close": prices})

    def test_rsi_flat_zero_variance_series(self):
        """Flat series (zero variance) must return neutral 50.0, never 0.0 or NaN."""
        for n in [30, 20, 15, 14]:
            df = self._make_df([100.0] * n)
            q = compute_quote_metrics(df, "SMH")
            self.assertEqual(q["rsi14"], 50.0, f"RSI for flat series of len {n} must be 50.0, got {q['rsi14']}")

    def test_rsi_monomorphic_up_series(self):
        """Monomorphic strictly increasing series must return 100.0."""
        # 30 days of consecutive +1 gains
        df30 = self._make_df([100.0 + i for i in range(30)])
        q30 = compute_quote_metrics(df30, "NVDA")
        self.assertEqual(q30["rsi14"], 100.0, f"RSI for monotonic up series must be 100.0, got {q30['rsi14']}")

        # 15 days of consecutive +2 gains (exactly 14 return deltas)
        df15 = self._make_df([100.0 + i * 2.0 for i in range(15)])
        q15 = compute_quote_metrics(df15, "NVDA")
        self.assertEqual(q15["rsi14"], 100.0, f"RSI for 15-row monotonic up series must be 100.0, got {q15['rsi14']}")

    def test_rsi_monomorphic_down_series(self):
        """Monomorphic strictly decreasing series must return 0.0."""
        # 30 days of consecutive -1 losses
        df30 = self._make_df([200.0 - i for i in range(30)])
        q30 = compute_quote_metrics(df30, "MU")
        self.assertEqual(q30["rsi14"], 0.0, f"RSI for monotonic down series must be 0.0, got {q30['rsi14']}")

        # 15 days of consecutive -3 losses
        df15 = self._make_df([200.0 - i * 3.0 for i in range(15)])
        q15 = compute_quote_metrics(df15, "MU")
        self.assertEqual(q15["rsi14"], 0.0, f"RSI for 15-row monotonic down series must be 0.0, got {q15['rsi14']}")

    def test_rsi_row_count_boundaries(self):
        """Tests exact 14 rows, 13 rows, and short series boundaries."""
        # 14 rows -> 13 delta values (below min_periods=14) -> must return default 50.0
        df14 = self._make_df([100.0 + i for i in range(14)])
        q14 = compute_quote_metrics(df14, "AVGO")
        self.assertEqual(q14["rsi14"], 50.0, f"RSI for 14 rows must default to 50.0, got {q14['rsi14']}")

        # 13 rows
        df13 = self._make_df([100.0 + i for i in range(13)])
        q13 = compute_quote_metrics(df13, "AVGO")
        self.assertEqual(q13["rsi14"], 50.0)

        # 1 row
        df1 = self._make_df([100.0])
        q1 = compute_quote_metrics(df1, "AVGO")
        self.assertEqual(q1["rsi14"], 50.0)
        self.assertEqual(q1["close"], 100.0)
        self.assertEqual(q1["chg1d"], 0.0)

    def test_rsi_alternating_oscillation(self):
        """Tests that alternating +1/-1 series produces neutral RSI near 50.0."""
        # [100, 101, 100, 101, ...] for 40 days
        prices = [100.0 if i % 2 == 0 else 101.0 for i in range(40)]
        df_alt = self._make_df(prices)
        q_alt = compute_quote_metrics(df_alt, "SMH")
        self.assertGreaterEqual(q_alt["rsi14"], 45.0)
        self.assertLessEqual(q_alt["rsi14"], 55.0)

    def test_rsi_spike_and_crash_reactions(self):
        """Tests RSI behavior under sudden 1-day extreme shock."""
        # 30 flat days followed by +100% surge
        prices_spike = [100.0] * 30 + [200.0]
        df_spike = self._make_df(prices_spike)
        q_spike = compute_quote_metrics(df_spike, "NVDA")
        self.assertGreater(q_spike["rsi14"], 85.0, "RSI must surge on +100% jump")

        # 30 flat days followed by -50% plunge
        prices_plunge = [200.0] * 30 + [100.0]
        df_plunge = self._make_df(prices_plunge)
        q_plunge = compute_quote_metrics(df_plunge, "NVDA")
        self.assertLess(q_plunge["rsi14"], 15.0, "RSI must collapse on -50% plunge")


class TestCSVInputRobustness(unittest.TestCase):
    """Stress tests out-of-order dates and comma/currency string stripping."""

    def test_out_of_order_dates_sorting(self):
        """Verifies that unsorted/reversed CSV inputs are sorted chronologically ascending."""
        dates = ["2026-10-15", "2026-10-14", "2026-10-13", "2026-10-12", "2026-10-11"]
        closes = [104.0, 103.0, 102.0, 101.0, 100.0]
        df_rev = pd.DataFrame({"Date": dates, "Close": closes})

        q = compute_quote_metrics(df_rev, "402340.KS")
        self.assertEqual(q["date"], "2026-10-15", "Latest date must be 2026-10-15")
        self.assertEqual(q["close"], 104.0, "Close price must be latest date's close (104.0)")
        self.assertEqual(q["prev_close"], 103.0, "Prev close must be 103.0")
        expected_chg = round((104.0 / 103.0 - 1.0) * 100.0, 2)
        self.assertEqual(q["chg1d"], expected_chg)

    def test_shuffled_dates_sorting(self):
        """Verifies randomly scrambled dates sort correctly."""
        dates = ["2026-10-12", "2026-10-15", "2026-10-10", "2026-10-14", "2026-10-11", "2026-10-13"]
        closes = [102.0, 105.0, 100.0, 104.0, 101.0, 103.0]
        df_shuf = pd.DataFrame({"Date": dates, "Close": closes})

        q = compute_quote_metrics(df_shuf, "000660.KS")
        self.assertEqual(q["date"], "2026-10-15")
        self.assertEqual(q["close"], 105.0)
        self.assertEqual(q["prev_close"], 104.0)

    def test_comma_and_currency_string_cleaning(self):
        """Verifies strings with commas, $, ₩, and whitespace are properly sanitized."""
        df_dirty = pd.DataFrame({
            "Date": ["2026-10-11", "2026-10-12", "2026-10-13", "2026-10-14"],
            "Close": [" 1,000,000 ", "₩1,050,000", "$1,080,000.50", " 1,090,000 "],
            "High": ["1,010,000", "₩1,060,000", "$1,090,000", "1,100,000"],
            "Low": ["990,000", "₩1,040,000", "$1,070,000", "1,080,000"],
            "Volume": [" 10,000 ", "25,000", "30,000", "50,000"],
        })

        q = compute_quote_metrics(df_dirty, "402340.KS")
        self.assertEqual(q["close"], 1090000.0)
        self.assertEqual(q["prev_close"], 1080000.0)  # Banker's rounding for KRW (1080000.5 -> 1080000.0)
        self.assertEqual(q["hi52"], 1100000.0)
        self.assertEqual(q["lo52"], 990000.0)
        self.assertGreater(q["vol_ratio"], 0.0)
        self.assertFalse(math.isnan(q["chg1d"]))


class Test52WeekMetricsEdgeCases(unittest.TestCase):
    """Stress tests 52-week metrics (DD52, Prox52) mathematical boundaries."""

    def test_at_52w_high_and_low(self):
        """Verifies exact 0.0% metrics when at 52-week boundaries."""
        # Constant series: cur == hi52 and cur == lo52
        dates = pd.date_range("2025-01-01", periods=260, freq="D").strftime("%Y-%m-%d")
        df_flat = pd.DataFrame({"Date": dates, "Close": [100.0] * 260})
        q_flat = compute_quote_metrics(df_flat, "QQQ")
        self.assertEqual(q_flat["dd52"], 0.0)
        self.assertEqual(q_flat["prox52"], 0.0)

        # Series peaking today: cur == hi52 (DD52 = 0.0%)
        prices = [50.0 + i * 0.5 for i in range(260)]  # 50.0 to 179.5
        df_high = pd.DataFrame({"Date": dates, "Close": prices})
        q_high = compute_quote_metrics(df_high, "QQQ")
        self.assertEqual(q_high["dd52"], 0.0)
        self.assertGreater(q_high["prox52"], 100.0)

        # Series at 52W low today: cur == lo52 (Prox52 = 0.0%)
        prices_down = [200.0 - i * 0.5 for i in range(260)]
        df_low = pd.DataFrame({"Date": dates, "Close": prices_down})
        q_low = compute_quote_metrics(df_low, "QQQ")
        self.assertEqual(q_low["prox52"], 0.0)
        self.assertLess(q_low["dd52"], -50.0)

    def test_sub_252_history(self):
        """Verifies that series with fewer than 252 days compute correctly without IndexError."""
        for n in [1, 5, 20, 50, 100, 251]:
            dates = pd.date_range("2026-01-01", periods=n, freq="D").strftime("%Y-%m-%d")
            closes = [100.0 + (i % 10) for i in range(n)]
            df = pd.DataFrame({"Date": dates, "Close": closes})
            q = compute_quote_metrics(df, "XLV")
            self.assertIsNotNone(q["dd52"])
            self.assertIsNotNone(q["prox52"])
            self.assertFalse(math.isnan(q["dd52"]))
            self.assertFalse(math.isnan(q["prox52"]))

    def test_non_positive_price_guards(self):
        """Verifies zero division safety when prices are 0."""
        df_zero = pd.DataFrame({"Date": ["2026-10-14", "2026-10-15"], "Close": [0.0, 0.0]})
        q_zero = compute_quote_metrics(df_zero, "XLV")
        self.assertEqual(q_zero["dd52"], 0.0)
        self.assertEqual(q_zero["prox52"], 0.0)
        self.assertEqual(q_zero["chg1d"], 0.0)

    def test_52w_rolling_window_excludes_old_spikes(self):
        """Verifies that 52-week (252-day) window ignores spikes older than 252 trading days."""
        # Create 350 days of data. Day 10 has a huge spike of 999.0.
        # But the last 252 days are strictly between 100.0 and 150.0.
        dates = pd.date_range("2025-01-01", periods=350, freq="D").strftime("%Y-%m-%d")
        prices = [100.0] * 350
        prices[10] = 999.0  # Old spike (340 days ago)
        prices[-1] = 150.0  # Recent high in the 252d window

        df = pd.DataFrame({"Date": dates, "Close": prices})
        q = compute_quote_metrics(df, "SMH")

        # hi52 must be 150.0, NOT 999.0
        self.assertEqual(q["hi52"], 150.0, f"hi52 must ignore spike >252 days ago, got {q['hi52']}")
        self.assertEqual(q["dd52"], 0.0)

    def test_missing_optional_columns(self):
        """Verifies that compute_quote_metrics works when High, Low, Volume are missing."""
        dates = pd.date_range("2026-01-01", periods=30, freq="D").strftime("%Y-%m-%d")
        df_min = pd.DataFrame({"Date": dates, "Close": [100.0 + i for i in range(30)]})

        q = compute_quote_metrics(df_min, "QQQ")
        self.assertEqual(q["close"], 129.0)
        self.assertEqual(q["hi52"], 129.0)
        self.assertEqual(q["lo52"], 100.0)
        self.assertEqual(q["vol_ratio"], 1.0)

    def test_missing_date_column_fallback(self):
        """Verifies that compute_quote_metrics defaults date to today when Date column is missing."""
        df_nodate = pd.DataFrame({"Close": [100.0, 105.0, 110.0]})
        q = compute_quote_metrics(df_nodate, "QQQ")
        self.assertEqual(q["close"], 110.0)
        self.assertEqual(q["prev_close"], 105.0)
        self.assertEqual(q["date"], datetime.now().strftime("%Y-%m-%d"))


class TestMediaBlacklistFirewallAdversarial(unittest.TestCase):
    """Stress tests the 0% South Korean Media Firewall against evasion techniques."""

    def test_url_encoded_evasion_blocked(self):
        """Verifies percent-encoded and double percent-encoded query params are trapped."""
        test_cases = [
            "https://news.google.com/search?q=Hynix&hl%3Dko&gl%3DKR",
            "https://news.google.com/search?q=Hynix&ceid%3DKR%3Ako",
            "https://finance.yahoo.com/news?lang=%68%6c%3d%6b%6f",
            "https://example.com/api?param=%2568%256c%253d%256b%256f",  # double encoded
        ]
        for url in test_cases:
            found = find_blacklisted_media(url)
            self.assertGreater(len(found), 0, f"Firewall failed to catch encoded evasion: {url}")
            with self.assertRaises(ValueError):
                assert_zero_korean_media(url)

    def test_brokerage_shorthand_and_english_blocked(self):
        """Verifies colloquial 4-char brokerage names and English names are trapped."""
        brokerages = [
            "신한증권 리포트", "한투증권 전망", "토스증권 브리핑", "카카오페이증권",
            "DB증권", "IBK증권", "Mirae Asset Research", "Samsung Securities",
            "NH Investment & Securities", "Korea Investment & Securities",
            "Shinhan Securities", "Kiwoom Securities", "Yonhap News Agency",
            "The Korea Herald Tech", "The Korea Times"
        ]
        for item in brokerages:
            found = find_blacklisted_media(item)
            self.assertGreater(len(found), 0, f"Firewall failed to catch entity: {item}")
            with self.assertRaises(ValueError):
                assert_zero_korean_media(item)

    def test_legitimate_us_and_china_sources_allowed(self):
        """Ensures NO false positives for legitimate US & China primary intelligence."""
        legitimate = [
            "Reuters: Micron technology reports record DRAM revenue",
            "Bloomberg: TSMC 3Q profit surges on AI chip demand",
            "CNBC: Nvidia expands datacenter networking with Broadcom",
            "Sina Finance: 新浪财经 报道 华尔街见闻 财联社 东方财富",
            "TechNews: 科技新報 報導 長鑫存儲(CXMT) 4F2 DDR5 設計完成",
            "Economic Daily: 經濟日報 報導 南亞科技 2408.TW 營收",
            "SMIC 0981.HK and NAURA 002371.SZ supply chain expansion",
            "Eli Lilly GLP-1 revenue exceeds Wall Street consensus",
            "Invesco QQQ Trust and VanEck Semiconductor ETF (SMH)",
        ]
        for text in legitimate:
            found = find_blacklisted_media(text)
            self.assertEqual(len(found), 0, f"False positive rejection for valid source: {text}")
            self.assertTrue(assert_zero_korean_media(text))


class TestMarketSnapshotInterfaceContract(unittest.TestCase):
    """End-to-end interface contract verification for fetch_market_snapshot."""

    def test_market_snapshot_offline_full_contract(self):
        """Generates a complete offline snapshot and verifies all contract requirements."""
        snap = fetch_market_snapshot(force_offline=True)

        self.assertEqual(snap["status"], "VERIFIED_100_PCT_US_CN")
        self.assertEqual(snap["proxies_count"], 15)
        self.assertGreaterEqual(len(snap["quotes"]), 15)

        # Check all 15 proxies exist in quotes
        for p in TestOfflineProxyIngestion.EXPECTED_15_PROXIES:
            self.assertIn(p, snap["quotes"], f"Proxy {p} missing in snapshot quotes")
            q = snap["quotes"][p]
            self.assertFalse(math.isnan(q["close"]))
            self.assertFalse(math.isnan(q["rsi14"]))

        # Check news structure
        news = snap["news"]
        self.assertIn("page1_news", news)
        self.assertIn("page2_news", news)
        self.assertEqual(len(news["page1_news"]), 3)
        self.assertEqual(len(news["page2_news"]), 3)

        for item in news["page1_news"] + news["page2_news"]:
            self.assertIn("origin_badge", item)
            self.assertTrue(
                "[🇺🇸 US" in item["origin_badge"] or "[🇨🇳 CN" in item["origin_badge"] or "US/CN" in item["origin_badge"],
                f"Invalid origin badge: {item['origin_badge']}"
            )
            self.assertIn("orig_headline", item)
            self.assertIn("kr_summary", item)

        # Verify zero Korean media across entire snapshot
        self.assertTrue(assert_zero_korean_media(snap))


if __name__ == "__main__":
    unittest.main(verbosity=2)
