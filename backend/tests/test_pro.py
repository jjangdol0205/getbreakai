"""
backend/tests/test_pro.py - Unit and Integration Tests for Pro Access Control and Tools
"""
import pytest
from fastapi.testclient import TestClient

from backend.app.main import app


@pytest.fixture
def api_client():
    return TestClient(app)


def test_pro_vault_unauthenticated_blocked(api_client):
    """Unauthenticated access to /api/pro/vault returns 401 Unauthorized."""
    res = api_client.get("/api/pro/vault")
    assert res.status_code == 401


def test_pro_vault_authenticated_success(api_client):
    """Pro access to /api/pro/vault with Bearer PRO-DEMO-2026 returns 200 OK."""
    headers = {"Authorization": "Bearer PRO-DEMO-2026"}
    res = api_client.get("/api/pro/vault", headers=headers)
    assert res.status_code == 200
    data = res.json()
    assert data["unlocked"] is True
    assert data["tier"] == "pro"
    assert "position_doctor" in data["tools"]


def test_pine_script_unauthenticated_blocked(api_client):
    """Unauthenticated access to /api/pro/pine-script returns 401 Unauthorized."""
    res = api_client.get("/api/pro/pine-script")
    assert res.status_code == 401


def test_pine_script_authenticated_delivery(api_client):
    """Authenticated access returns TradingView Pine Script v5 indicator code."""
    headers = {"Authorization": "Bearer PRO-DEMO-2026"}
    res = api_client.get("/api/pro/pine-script", headers=headers)
    assert res.status_code == 200
    data = res.json()
    assert data["version"] == "v5"
    assert "//@version=5" in data["code"]
    assert "RightSideAlpha" in data["code"]


def test_pinescript_alias_route(api_client):
    """GET /api/pro/pinescript works as alias for /api/pro/pine-script."""
    headers = {"Authorization": "Bearer PRO-DEMO-2026"}
    res = api_client.get("/api/pro/pinescript", headers=headers)
    assert res.status_code == 200
    assert "indicator" in res.json()["code"]


def test_pro_stocks_unmasked(api_client):
    """GET /api/pro/stocks-unmasked returns all 72 US stocks with target prices."""
    headers = {"Authorization": "Bearer PRO-DEMO-2026"}
    res = api_client.get("/api/pro/stocks-unmasked", headers=headers)
    assert res.status_code == 200
    stocks = res.json()
    assert len(stocks) == 72
    for s in stocks:
        assert s["is_pro_locked"] is False
        assert s["stop_loss_price"] is not None
        assert s["tp1_2x_price"] is not None


def test_position_doctor_rule_1_hard_stop(api_client):
    """Position Doctor Rule 1 (-9.0% hard stop)."""
    payload = {"ticker": "CELH", "entry_price": 100.0, "days_held": 10, "current_price": 91.0}
    res = api_client.post("/api/pro/position-doctor", json=payload)
    assert res.status_code == 200
    data = res.json()
    assert data["status_code"] == "HARD_STOP"
    assert data["is_critical"] is True
    assert data["return_pct"] == -9.0


def test_position_doctor_rule_2_time_stop(api_client):
    """Position Doctor Rule 2 (55-day time stop when return < 8%)."""
    payload = {"ticker": "CELH", "entry_price": 100.0, "days_held": 55, "current_price": 105.0}
    res = api_client.post("/api/pro/position-doctor", json=payload)
    assert res.status_code == 200
    data = res.json()
    assert data["status_code"] == "TIME_STOP"
    assert "Rule 2" in data["rule_triggered"]


def test_position_doctor_rule_3_tp1_harvest(api_client):
    """Position Doctor Rule 3 (+100% TP1 harvesting)."""
    payload = {"ticker": "CELH", "entry_price": 50.0, "days_held": 40, "current_price": 100.0}
    res = api_client.post("/api/pro/position-doctor", json=payload)
    assert res.status_code == 200
    data = res.json()
    assert data["status_code"] == "TP1_HARVEST"
    assert "Sell 50%" in data["action_plan"]


def test_position_doctor_rule_4_hold(api_client):
    """Position Doctor Rule 4 (Normal hold)."""
    payload = {"ticker": "CELH", "entry_price": 100.0, "days_held": 20, "current_price": 115.0}
    res = api_client.post("/api/pro/position-doctor", json=payload)
    assert res.status_code == 200
    data = res.json()
    assert data["status_code"] == "HOLD"


def test_position_doctor_negative_entry_price_returns_422(api_client):
    """Invalid entry_price <= 0 returns 422 Unprocessable Entity."""
    payload = {"ticker": "CELH", "entry_price": -10.0, "days_held": 5}
    res = api_client.post("/api/pro/position-doctor", json=payload)
    assert res.status_code == 422


def test_position_doctor_returns_entry_and_current_price(api_client):
    """Position Doctor returns entry_price, current_price, and as_of_date."""
    payload = {"ticker": "CELH", "entry_price": 25.0, "days_held": 12}
    res = api_client.post("/api/pro/position-doctor", json=payload)
    assert res.status_code == 200
    data = res.json()
    assert data["entry_price"] == 25.0
    assert data["current_price"] == 27.93
    assert data["as_of_date"] == "2026-10-13"


def test_semi_pro_csv_head_and_alias(api_client):
    """HEAD and GET on /api/semi/pro/csv and /api/semi/download-csv work with X-License-Key."""
    headers = {"X-License-Key": "PRO-DEMO-2026"}
    for path in ["/api/semi/pro/csv", "/api/semi/download-csv"]:
        r_head = api_client.head(path, headers=headers)
        assert r_head.status_code == 200
        r_get = api_client.get(path, headers=headers)
        assert r_get.status_code == 200
