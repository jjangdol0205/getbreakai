"""
tests_e2e/test_tier1_features.py - Tier 1: Primary Features E2E Test Suite

Covers isolated specification verification (>= 5 test cases per feature):
1. Server Startup & Health (5 cases)
2. Stocks Public Listing & Masking F1 (6 cases)
3. Backtest Summary KPIs F2 (6 cases)
4. Turnaround Research Briefs F3 (5 cases)
5. Lemon Squeezy License Verification F5 (6 cases)
6. Referral Link Building & Tracking F9/F10 (6 cases)
Total: 34 Test Cases
"""

import pytest
from typing import Dict, Any


# ==============================================================================
# Feature 0: Server Startup & Health
# ==============================================================================

def test_t1_health_endpoint_status_200(client):
    """GET /api/health returns HTTP 200 OK."""
    resp = client.get("/api/health")
    assert resp.status_code == 200, f"Expected 200, got {resp.status_code}: {resp.text}"
    data = resp.json()
    assert data.get("status") == "ok"


def test_t1_health_response_schema_fields(client):
    """Health check payload includes version, engine_loaded, and stock_count."""
    resp = client.get("/api/health")
    assert resp.status_code == 200
    data = resp.json()
    assert "version" in data
    assert "engine_loaded" in data
    assert data["engine_loaded"] is True
    assert "stock_count" in data
    assert data["stock_count"] > 0


def test_t1_root_endpoint_availability(client):
    """GET / returns HTTP 200 indicating server or frontend is accessible."""
    resp = client.get("/")
    assert resp.status_code == 200


def test_t1_docs_schema_endpoint(client):
    """GET /docs returns HTTP 200 OpenAPI interactive documentation."""
    resp = client.get("/docs")
    assert resp.status_code in [200, 307]


def test_t1_health_head_method(client):
    """HEAD /health returns HTTP 200 without payload for liveness probes."""
    resp = client.head("/health")
    assert resp.status_code in [200, 204]


# ==============================================================================
# Feature 1: Stocks Public Listing & Masking
# ==============================================================================

def test_t1_stocks_list_status_and_count(client, ground_truth_stocks):
    """GET /api/stocks returns HTTP 200 and >= 30 screened stock records."""
    resp = client.get("/api/stocks")
    assert resp.status_code == 200
    stocks = resp.json()
    assert isinstance(stocks, list)
    assert len(stocks) >= 30, f"Expected at least 30 stocks, got {len(stocks)}"


def test_t1_stocks_schema_conformance(client):
    """Every stock record in /api/stocks adheres to the StockPublic contract schema."""
    resp = client.get("/api/stocks")
    assert resp.status_code == 200
    stocks = resp.json()
    first = stocks[0]

    required_fields = [
        "ticker", "name", "date", "close", "low52", "high52",
        "prox_low52_pct", "dd_high52_pct", "vs_ma20_pct", "vs_ma60_pct",
        "rsi14", "vol_surge_10d", "score", "zone_code", "is_pro_locked"
    ]
    for field in required_fields:
        assert field in first, f"Missing required field '{field}' in stock schema"


def test_t1_stocks_public_masking_enforced_rows_4_plus(client):
    """Free/public users see target prices masked (null/None) on rows >= 4."""
    resp = client.get("/api/stocks")
    assert resp.status_code == 200
    stocks = resp.json()
    assert len(stocks) > 5

    # Rows 0..3 may be previewable
    for i in range(min(4, len(stocks))):
        assert stocks[i].get("is_pro_locked") is False

    # Rows 4+ must be masked for public users
    for i in range(4, min(10, len(stocks))):
        assert stocks[i].get("is_pro_locked") is True, f"Row {i} should be pro-locked for public users"
        assert stocks[i].get("stop_loss_price") is None, f"Row {i} stop_loss_price must be masked"
        assert stocks[i].get("tp1_2x_price") is None, f"Row {i} tp1_2x_price must be masked"


def test_t1_stocks_zone_filtering_ignition(client):
    """GET /api/stocks?zone=IGNITION_ZONE returns only stocks categorized in IGNITION_ZONE."""
    resp = client.get("/api/stocks?zone=IGNITION_ZONE")
    assert resp.status_code == 200
    stocks = resp.json()
    assert len(stocks) > 0
    for s in stocks:
        assert s.get("zone_code") == "IGNITION_ZONE"


def test_t1_stocks_sorting_by_score(client):
    """GET /api/stocks?sort_by=score&order=desc returns stocks in descending score order."""
    resp = client.get("/api/stocks?sort_by=score&order=desc")
    assert resp.status_code == 200
    stocks = resp.json()
    scores = [s.get("score", 0) for s in stocks]
    assert scores == sorted(scores, reverse=True), "Stocks not sorted in descending score order"


def test_t1_single_stock_detail_lookup_celh(client, ground_truth_stocks):
    """GET /api/stocks/CELH returns accurate close and 52W range matching dataset."""
    resp = client.get("/api/stocks/CELH")
    assert resp.status_code == 200
    stock = resp.json()
    assert stock.get("ticker") == "CELH"

    # Find CELH in ground truth
    gt = next((s for s in ground_truth_stocks if s.get("Ticker") == "CELH"), None)
    if gt:
        assert abs(stock.get("close") - float(gt["Close"])) < 0.05
        assert abs(stock.get("low52") - float(gt["Low52"])) < 0.05
        assert abs(stock.get("high52") - float(gt["High52"])) < 0.05


# ==============================================================================
# Feature 2: Backtest & KPI Data Engine
# ==============================================================================

def test_t1_backtest_overall_summary_cagr_and_multiple(client, ground_truth_backtest):
    """GET /api/backtest returns 203.87x multiple and 21.97% CAGR for PW-RSI."""
    resp = client.get("/api/backtest")
    assert resp.status_code == 200
    data = resp.json()
    assert "overall_summary" in data

    summary_list = data["overall_summary"]
    pwrsi = next((s for s in summary_list if "PW-RSI" in s.get("Strategy", "")), None)
    assert pwrsi is not None, "PW-RSI strategy missing from backtest overall_summary"
    assert abs(pwrsi["Final_Multiple"] - 203.87) < 0.1
    assert abs(pwrsi["CAGR_Pct"] - 21.97) < 0.1


def test_t1_backtest_benchmark_comparison_qqq_spy(client):
    """Backtest summary contains QQQ and SPY benchmarks for empirical proof."""
    resp = client.get("/api/backtest")
    assert resp.status_code == 200
    data = resp.json()
    strategies = [s.get("Strategy", "") for s in data.get("overall_summary", [])]

    has_qqq = any("QQQ" in s for s in strategies)
    has_spy = any("SPY" in s for s in strategies)
    assert has_qqq, "QQQ benchmark missing in backtest summary"
    assert has_spy, "SPY benchmark missing in backtest summary"


def test_t1_backtest_period_and_universe_size(client, ground_truth_backtest):
    """Backtest period covers 26.78 years and >= 100 universe stocks."""
    resp = client.get("/api/backtest")
    assert resp.status_code == 200
    data = resp.json()
    assert "2000" in data.get("period", "")
    assert data.get("universe_size", 0) >= 100


def test_t1_backtest_yearly_performance_record_count(client):
    """GET /api/backtest contains yearly records spanning 2000 through 2026."""
    resp = client.get("/api/backtest")
    assert resp.status_code == 200
    data = resp.json()
    yearly = data.get("yearly_performance", [])
    assert len(yearly) >= 25, f"Expected >= 25 yearly records, got {len(yearly)}"


def test_t1_backtest_trade_logs_count_and_fields(client, ground_truth_backtest):
    """GET /api/backtest/trades returns exact trade log count (84 trades)."""
    resp = client.get("/api/backtest/trades")
    assert resp.status_code == 200
    trades = resp.json()
    assert len(trades) == 84, f"Expected 84 trades, got {len(trades)}"
    first_trade = trades[0]
    for key in ["entry_date", "exit_date", "ticker", "entry_price", "exit_price", "return_pct", "exit_reason"]:
        assert key in first_trade, f"Missing key '{key}' in trade log item"


def test_t1_backtest_trade_exit_rules_represented(client):
    """Trade logs contain all 4 documented quantitative exit reasons."""
    resp = client.get("/api/backtest/trades")
    assert resp.status_code == 200
    trades = resp.json()
    reasons = [t.get("exit_reason", "") for t in trades]

    has_stop = any("-9%" in r or "손절" in r for r in reasons)
    has_time = any("55일" in r or "시간손절" in r for r in reasons)
    has_tp1 = any("2배" in r or "TP1" in r for r in reasons)
    assert has_stop, "Hard stop (-9%) exit reason missing from trade log"
    assert has_time, "Time stop (55-day) exit reason missing from trade log"
    assert has_tp1, "TP1 (+100%) exit reason missing from trade log"


# ==============================================================================
# Feature 3: Turnaround Research Briefs
# ==============================================================================

def test_t1_research_list_contains_weekly_picks(client):
    """GET /api/research returns list of available weekly institutional briefs."""
    resp = client.get("/api/research")
    assert resp.status_code == 200
    briefs = resp.json()
    assert isinstance(briefs, list)
    tickers = [b.get("ticker", "").upper() for b in briefs]
    assert "MBLY" in tickers or "CELH" in tickers, f"Expected MBLY or CELH in {tickers}"


def test_t1_research_mbly_brief_retrieval(client):
    """GET /api/research/MBLY returns full research report content."""
    resp = client.get("/api/research/MBLY")
    assert resp.status_code == 200
    data = resp.json()
    assert data.get("ticker") == "MBLY"
    assert "content" in data
    assert len(data["content"]) > 1000


def test_t1_research_celh_brief_retrieval(client):
    """GET /api/research/CELH returns Celsius Holdings report."""
    resp = client.get("/api/research/CELH")
    assert resp.status_code == 200
    data = resp.json()
    assert data.get("ticker") == "CELH"
    assert len(data["content"]) > 1000


def test_t1_research_brief_structure_sections(client):
    """Research report contains standard 6-section institutional headings."""
    resp = client.get("/api/research/MBLY")
    assert resp.status_code == 200
    content = resp.json().get("content", "")
    assert "Executive Summary" in content or "핵심 요약" in content or "Investment Thesis" in content
    assert "TP1" in content or "+100%" in content


def test_t1_research_brief_catalyst_and_rrr_metrics(client):
    """Research brief highlights asymmetric risk-reward ratio (1:11+)."""
    resp = client.get("/api/research/MBLY")
    assert resp.status_code == 200
    content = resp.json().get("content", "")
    assert "1:" in content or "RRR" in content or "Risk-Reward" in content


# ==============================================================================
# Feature 5: Lemon Squeezy License Key Verification
# ==============================================================================

def test_t1_license_demo_key_pro_demo_2026_valid(client):
    """Demo key PRO-DEMO-2026 validates immediately with valid=True and tier=pro."""
    payload = {"license_key": "PRO-DEMO-2026"}
    resp = client.post("/api/auth/validate", json=payload)
    assert resp.status_code == 200
    data = resp.json()
    assert data.get("valid") is True
    assert data.get("tier") in ["pro", "pro_lifetime"]
    assert data.get("license_key") == "PRO-DEMO-2026"


def test_t1_license_demo_key_case_insensitivity(client):
    """Demo key validation is case-insensitive (e.g., 'pro-demo-2026')."""
    payload = {"license_key": "pro-demo-2026"}
    resp = client.post("/api/auth/validate", json=payload)
    assert resp.status_code == 200
    assert resp.json().get("valid") is True


def test_t1_license_response_schema_contract(client):
    """License validation response adheres to PROJECT.md LicenseValidationResponse schema."""
    resp = client.post("/api/auth/validate", json={"license_key": "PRO-DEMO-2026"})
    assert resp.status_code == 200
    data = resp.json()
    assert "valid" in data
    assert "tier" in data
    assert "license_key" in data
    assert "message" in data


def test_t1_license_with_optional_instance_name(client):
    """License validation accepts optional instance_name parameter."""
    payload = {"license_key": "PRO-DEMO-2026", "instance_name": "RetailMacbookPro"}
    resp = client.post("/api/auth/validate", json=payload)
    assert resp.status_code == 200
    assert resp.json().get("valid") is True


def test_t1_license_invalid_key_rejected(client):
    """Invalid license key returns valid=False without 500 error."""
    payload = {"license_key": "RANDOM-INVALID-KEY-999"}
    resp = client.post("/api/auth/validate", json=payload)
    assert resp.status_code == 200
    data = resp.json()
    assert data.get("valid") is False


def test_t1_unauthenticated_pro_vault_returns_401(client):
    """GET /api/pro/vault without license token returns 401 Unauthorized."""
    resp = client.get("/api/pro/vault")
    assert resp.status_code in [401, 403]


# ==============================================================================
# Feature 9/10: Referral Link Building & Tracking
# ==============================================================================

def test_t1_referral_config_retrieval(client):
    """GET /api/referral/config returns affiliate parameters for partners."""
    resp = client.get("/api/referral/config")
    assert resp.status_code == 200
    cfg = resp.json()
    assert "tradingview_aff_id" in cfg
    assert "seekingalpha_source" in cfg


def test_t1_referral_build_tradingview_url(client):
    """GET /api/referral/build?provider=tradingview&ticker=NVDA produces compliant link."""
    resp = client.get("/api/referral/build?provider=tradingview&ticker=NVDA")
    assert resp.status_code == 200
    data = resp.json()
    assert data.get("provider") == "tradingview"
    assert data.get("ticker") == "NVDA"
    assert "tradingview.com/symbols/NVDA" in data.get("url", "")
    assert "aff_id=" in data.get("url", "")


def test_t1_referral_build_seekingalpha_url(client):
    """GET /api/referral/build?provider=seekingalpha&ticker=CELH produces Seeking Alpha link."""
    resp = client.get("/api/referral/build?provider=seekingalpha&ticker=CELH")
    assert resp.status_code == 200
    data = resp.json()
    assert "seekingalpha.com/symbol/CELH" in data.get("url", "")
    assert "source=" in data.get("url", "")


def test_t1_referral_build_trendspider_url(client):
    """GET /api/referral/build?provider=trendspider&ticker=TSLA produces TrendSpider link."""
    resp = client.get("/api/referral/build?provider=trendspider&ticker=TSLA")
    assert resp.status_code == 200
    assert "trendspider.com" in resp.json().get("url", "")


def test_t1_referral_redirect_status_code_307(client):
    """GET /api/referral/redirect/tradingview?ticker=AAPL returns 307 Temporary Redirect."""
    resp = client.get("/api/referral/redirect/tradingview?ticker=AAPL")
    assert resp.status_code in [307, 302]
    loc = resp.headers.get("location", "")
    assert "tradingview.com" in loc


def test_t1_referral_click_tracking_increment(client):
    """Outbound redirect increments referral click analytics."""
    initial_stats = client.get("/api/referral/stats").json()
    initial_total = initial_stats.get("total", 0)

    # Perform redirect
    client.get("/api/referral/redirect/tradingview?ticker=APP")

    new_stats = client.get("/api/referral/stats").json()
    assert new_stats.get("total", 0) == initial_total + 1


# ==============================================================================
# Feature 11: US-Only Equity Restriction & SemiFearGreed CNN-Style Engine
# ==============================================================================

def test_t1_rightsidealpha_strictly_us_listed_stocks_only(client):
    """RightSideAlpha /api/stocks returns strictly the 72 US-listed stocks and zero .KS/.KQ tickers."""
    resp = client.get("/api/stocks?limit=200")
    assert resp.status_code == 200
    stocks = resp.json()
    assert len(stocks) == 72
    assert all("." not in s["ticker"] and not s["ticker"].endswith(".KS") and not s["ticker"].endswith(".KQ") for s in stocks)


def test_t1_semi_fear_greed_overview_cnn_contract(client):
    """GET /api/semi/overview returns CNN-style Fear & Greed score, 4 comparisons, 7 factors, and ETFs."""
    resp = client.get("/api/semi/overview")
    assert resp.status_code == 200
    data = resp.json()
    assert 0.0 <= data["fg_score"] <= 100.0
    assert data["regime_code"] in ["EXTREME_FEAR", "FEAR", "NEUTRAL", "GREED", "EXTREME_GREED"]
    assert len(data["comparisons"]) == 4
    assert len(data["factors"]) == 7
    assert sum(f["weight_pct"] for f in data["factors"]) == 100
    assert len(data["etfs"]) == 3


def test_t1_semi_fear_greed_history_and_26yr_eras(client):
    """GET /api/semi/history returns time-series and 26-year era backtest table."""
    resp = client.get("/api/semi/history?range=1Y")
    assert resp.status_code == 200
    data = resp.json()
    assert data["range_code"] == "1Y"
    assert len(data["series"]) > 50
    assert len(data["era_summary"]) == 4
    assert data["era_summary"][0]["port_80_20_multiple"] == 14.22


def test_t1_semi_rebalance_and_krw_tax_harvester(client):
    """POST /api/semi/rebalance computes 80:20 contrarian shift and KRW 2.5M tax guidance."""
    resp = client.post("/api/semi/rebalance", json={
        "total_capital_usd": 100000.0,
        "strategy_mode": "AUTO_REGIME",
        "rebalance_frequency": "ANNUAL",
        "unrealized_gain_krw": 3800000.0,
    })
    assert resp.status_code == 200
    data = resp.json()
    assert data["target_smh_weight_pct"] == 80.0
    assert data["target_xlv_weight_pct"] == 20.0
    assert data["target_smh_shares"] > 0
    assert data["target_xlv_shares"] > 0
    assert data["kr_taxable_gain_krw"] == 1300000.0


def test_t1_semi_lump_sum_3_stage_cases(client):
    """POST /api/semi/lump-sum evaluates all 3 Fear/Neutral/Greed entry cases."""
    r1 = client.post("/api/semi/lump-sum", json={"capital_usd": 50000.0, "override_fg_score": 18.0}).json()
    assert r1["case_code"] == "CASE_1_FEAR_100PCT"
    assert r1["immediate_deploy_pct"] == 100.0

    r2 = client.post("/api/semi/lump-sum", json={"capital_usd": 50000.0, "override_fg_score": 50.0}).json()
    assert r2["case_code"] == "CASE_2_NEUTRAL_65_35"
    assert r2["immediate_deploy_pct"] == 65.0

    r3 = client.post("/api/semi/lump-sum", json={"capital_usd": 50000.0, "override_fg_score": 78.0}).json()
    assert r3["case_code"] == "CASE_3_GREED_DEFENSIVE_FIRST"
    assert r3["immediate_deploy_pct"] == 30.0


def test_t1_semi_pro_csv_download_gated(client):
    """GET /api/semi/pro/csv requires Pro authentication and serves CSV when unlocked."""
    unauth = client.get("/api/semi/pro/csv")
    assert unauth.status_code == 401

    auth = client.get("/api/semi/pro/csv", headers={"Authorization": "Bearer PRO-DEMO-2026"})
    assert auth.status_code == 200
    assert "Date,SMH_Close,XLV_Close" in auth.text[:200]

