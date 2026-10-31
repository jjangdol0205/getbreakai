"""
backend/tests/test_api.py - Integration tests for Milestone 1 REST API endpoints
"""
import pytest


def test_health_check(client):
    """GET /api/health and GET /health -> 200 OK with system status."""
    for path in ["/api/health", "/health"]:
        res = client.get(path)
        assert res.status_code == 200
        data = res.json()
        assert data["status"] == "ok"
        assert data["engine_loaded"] is True
        assert data["stock_count"] == 72
        assert data["stocks_loaded"] == 72
        assert data["backtest_loaded"] is True
        assert data["backtest_trades"] == 84


def test_stocks_public_masking_rules(client):
    """GET /api/stocks -> Rows 0..3 unmasked, Rows 4+ masked for free tier."""
    res = client.get("/api/stocks")
    assert res.status_code == 200
    assert res.headers.get("X-Total-Count") == "72"
    assert res.headers.get("X-Pro-Unlocked") == "false"

    stocks = res.json()
    assert len(stocks) == 72

    # Rows 0..3 (first 4 preview rows: CELH, CCL, TSLA, UPST)
    for i in range(4):
        row = stocks[i]
        assert row["is_pro_locked"] is False
        assert row["stop_loss_price"] is not None
        assert row["tp1_2x_price"] is not None
        assert row["ma60_price"] is not None

    # Rows >= 4 (pro locked rows: MBLY, APP, ENPH...)
    for i in range(4, len(stocks)):
        row = stocks[i]
        assert row["is_pro_locked"] is True
        assert row["stop_loss_price"] is None
        assert row["tp1_2x_price"] is None
        assert row["ma60_price"] is None


def test_stocks_pro_demo_bypass(client):
    """GET /api/stocks?license_key=PRO-DEMO-2026 returns all rows unmasked."""
    res = client.get("/api/stocks?license_key=PRO-DEMO-2026")
    assert res.status_code == 200
    assert res.headers.get("X-Pro-Unlocked") == "true"

    stocks = res.json()
    assert len(stocks) == 72
    for row in stocks:
        assert row["is_pro_locked"] is False
        assert row["stop_loss_price"] is not None
        assert row["tp1_2x_price"] is not None
        assert row["ma60_price"] is not None


def test_stocks_bearer_token(client):
    """GET /api/stocks with Authorization: Bearer PRO-DEMO-2026 unlocks all rows."""
    headers = {"Authorization": "Bearer PRO-DEMO-2026"}
    res = client.get("/api/stocks", headers=headers)
    assert res.status_code == 200
    assert res.headers.get("X-Pro-Unlocked") == "true"

    stocks = res.json()
    for row in stocks:
        assert row["is_pro_locked"] is False
        assert row["stop_loss_price"] is not None
        assert row["tp1_2x_price"] is not None


def test_stocks_zone_filtering(client):
    """GET /api/stocks?zone=IGNITION_ZONE filters properly."""
    res = client.get("/api/stocks?zone=IGNITION_ZONE")
    assert res.status_code == 200
    stocks = res.json()
    assert len(stocks) > 0
    for s in stocks:
        assert s["zone_code"] == "IGNITION_ZONE"


def test_stocks_ticker_search(client):
    """GET /api/stocks?search=... searches by ticker substring."""
    res = client.get("/api/stocks?search=CELH")
    assert res.status_code == 200
    stocks = res.json()
    assert any(s["ticker"] == "CELH" for s in stocks)


def test_stocks_query_alias(client):
    """GET /api/stocks?query=... works as alias for search."""
    res = client.get("/api/stocks?query=TSLA")
    assert res.status_code == 200
    stocks = res.json()
    assert any(s["ticker"] == "TSLA" for s in stocks)


def test_stocks_sort_by_score(client):
    """GET /api/stocks?sort_by=score&order=desc returns sorted list."""
    res = client.get("/api/stocks?sort_by=score&order=desc")
    assert res.status_code == 200
    stocks = res.json()
    scores = [s["score"] for s in stocks]
    assert scores == sorted(scores, reverse=True)


def test_stock_detail_valid(client):
    """GET /api/stocks/{ticker} returns single stock detail."""
    res = client.get("/api/stocks/CELH")
    assert res.status_code == 200
    data = res.json()
    assert data["ticker"] == "CELH"
    assert data["close"] == 27.93
    assert data["zone_code"] == "IGNITION_ZONE"
    assert data["is_pro_locked"] is False
    assert data["stop_loss_price"] == 25.42
    assert data["tp1_2x_price"] == 55.86


def test_stock_detail_non_preview_masked_vs_pro(client):
    """GET /api/stocks/MBLY is masked for free user, unmasked for Pro user."""
    # Free tier
    res_free = client.get("/api/stocks/MBLY")
    assert res_free.status_code == 200
    data_free = res_free.json()
    assert data_free["ticker"] == "MBLY"
    assert data_free["is_pro_locked"] is True
    assert data_free["stop_loss_price"] is None
    assert data_free["tp1_2x_price"] is None

    # Pro tier
    res_pro = client.get("/api/stocks/MBLY?license_key=PRO-DEMO-2026")
    assert res_pro.status_code == 200
    data_pro = res_pro.json()
    assert data_pro["is_pro_locked"] is False
    assert data_pro["stop_loss_price"] is not None
    assert data_pro["tp1_2x_price"] is not None


def test_stock_detail_not_found(client):
    """GET /api/stocks/{ticker} returns 404 for unknown ticker."""
    res = client.get("/api/stocks/UNKNOWN999XYZ")
    assert res.status_code == 404
    assert "detail" in res.json()


def test_backtest_summary(client):
    """GET /api/backtest/summary returns 26.8-year backtest stats."""
    res = client.get("/api/backtest/summary")
    assert res.status_code == 200
    data = res.json()
    assert "overall_summary" in data
    assert "yearly_performance" in data
    assert "kpis" in data
    assert any(s["Final_Multiple"] == 203.87 for s in data["overall_summary"])
    assert data["kpis"]["hit_rate_2x_pct"] == 55.24


def test_backtest_trades(client):
    """GET /api/backtest/trades returns trade log entries."""
    res = client.get("/api/backtest/trades")
    assert res.status_code == 200
    trades = res.json()
    assert isinstance(trades, list)
    assert len(trades) == 84

    # Test filtering by ticker
    res_filtered = client.get("/api/backtest/trades?ticker=CELH")
    assert res_filtered.status_code == 200
    celh_trades = res_filtered.json()
    assert all(t["ticker"] == "CELH" for t in celh_trades)


def test_research_list(client):
    """GET /api/research returns list of research briefs."""
    res = client.get("/api/research")
    assert res.status_code == 200
    data = res.json()
    assert isinstance(data, list)
    assert len(data) >= 2
    assert any(r["ticker"] == "CELH" for r in data)


def test_research_brief_valid(client):
    """GET /api/research/{ticker} returns markdown content."""
    res = client.get("/api/research/CELH")
    assert res.status_code == 200
    data = res.json()
    assert data["ticker"] == "CELH"
    assert "content" in data or "markdown" in data


def test_research_brief_not_found(client):
    """GET /api/research/{ticker} returns 404 for missing brief."""
    res = client.get("/api/research/NONEXISTENT999")
    assert res.status_code == 404


def test_cors_headers_on_options(client):
    """OPTIONS request returns proper CORS allow headers."""
    headers = {
        "Origin": "http://localhost:3000",
        "Access-Control-Request-Method": "GET"
    }
    res = client.options("/api/stocks", headers=headers)
    assert res.status_code in (200, 204)
    assert res.headers.get("access-control-allow-origin") == "http://localhost:3000"


def test_position_doctor_endpoint(client):
    """POST /api/stocks/diagnose evaluates 4 exit rules."""
    payload = {
        "ticker": "MBLY",
        "entry_price": 20.0,
        "days_held": 5,
        "current_price": 18.0
    }
    res = client.post("/api/stocks/diagnose", json=payload)
    assert res.status_code == 200
    data = res.json()
    assert data["status_code"] == "CRITICAL_STOP"
    assert data["is_critical"] is True
    assert data["return_pct"] == -10.0
