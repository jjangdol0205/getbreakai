"""
backend/tests/test_referral.py - Unit and Integration Tests for Referral Monetization
"""
import pytest
from fastapi.testclient import TestClient

from backend.app.main import app


@pytest.fixture
def api_client():
    return TestClient(app)


def test_referral_config_retrieval(api_client):
    """GET /api/referral/config returns affiliate parameters."""
    res = api_client.get("/api/referral/config")
    assert res.status_code == 200
    data = res.json()
    assert "tradingview_aff_id" in data
    assert "seekingalpha_source" in data
    assert "trendspider_aff_id" in data


def test_referral_config_update(api_client):
    """POST /api/referral/config modifies active partner IDs."""
    new_cfg = {
        "tradingview_aff_id": "test_partner_tv",
        "seekingalpha_source": "test_partner_sa",
        "trendspider_aff_id": "test_partner_ts",
    }
    res = api_client.post("/api/referral/config", json=new_cfg)
    assert res.status_code == 200

    cfg_check = api_client.get("/api/referral/config").json()
    assert cfg_check["tradingview_aff_id"] == "test_partner_tv"


def test_referral_build_link_providers(api_client):
    """GET /api/referral/build constructs valid deep links."""
    r_tv = api_client.get("/api/referral/build?provider=tradingview&ticker=NVDA")
    assert r_tv.status_code == 200
    assert "tradingview.com/symbols/NVDA" in r_tv.json()["url"]

    r_sa = api_client.get("/api/referral/build?provider=seekingalpha&ticker=CELH")
    assert r_sa.status_code == 200
    assert "seekingalpha.com/symbol/CELH" in r_sa.json()["url"]

    r_ts = api_client.get("/api/referral/build?provider=trendspider&ticker=TSLA")
    assert r_ts.status_code == 200
    assert "trendspider.com" in r_ts.json()["url"]


def test_referral_build_unknown_provider_rejected(api_client):
    """GET /api/referral/build with unknown provider returns 400 Bad Request."""
    res = api_client.get("/api/referral/build?provider=nonexistent_network&ticker=AAPL")
    assert res.status_code == 400


def test_referral_build_empty_provider_rejected(api_client):
    """GET /api/referral/build with empty provider returns 400 Bad Request."""
    res = api_client.get("/api/referral/build?provider=&ticker=AAPL")
    assert res.status_code == 400


def test_referral_redirect_307_and_click_tracking(api_client):
    """GET /api/referral/redirect/{provider} returns 307 and increments counters."""
    initial_stats = api_client.get("/api/referral/stats").json()
    initial_total = initial_stats.get("total", 0)
    initial_tv = initial_stats.get("tradingview", 0)

    res = api_client.get("/api/referral/redirect/tradingview?ticker=APP", follow_redirects=False)
    assert res.status_code == 307
    assert "tradingview.com" in res.headers["location"]

    new_stats = api_client.get("/api/referral/stats").json()
    assert new_stats.get("total", 0) == initial_total + 1
    assert new_stats.get("tradingview", 0) == initial_tv + 1


def test_referral_redirect_invalid_provider_returns_404(api_client):
    """GET /api/referral/redirect/unknown returns 404 Not Found."""
    res = api_client.get("/api/referral/redirect/unknown_network?ticker=AAPL", follow_redirects=False)
    assert res.status_code == 404
