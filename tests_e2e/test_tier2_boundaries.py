"""
tests_e2e/test_tier2_boundaries.py - Tier 2: Boundary & Corner Cases E2E Test Suite

Covers boundary conditions and adversarial resilience (>= 5 cases per feature):
1. Search & Query Boundaries F1 (6 cases)
2. Filter & Pagination Boundaries F1 (5 cases)
3. License Key Boundaries F5 (6 cases)
4. Position Doctor Mathematical Boundaries F7 (7 cases)
5. Headers & Security Boundaries (5 cases)
6. Referral Provider & URL Boundaries F9/F10 (5 cases)
Total: 34 Boundary Test Cases
"""

import pytest


# ==============================================================================
# 1. Search & Query Boundaries (F1)
# ==============================================================================

def test_t2_search_empty_string_returns_all_stocks(client):
    """Empty search parameter ?search= returns all stocks without crashing."""
    resp = client.get("/api/stocks?search=")
    assert resp.status_code == 200
    stocks = resp.json()
    assert len(stocks) >= 30


def test_t2_search_whitespace_only_returns_all_stocks(client):
    """Whitespace-only search ?search=%20%20%20 is stripped and returns all stocks."""
    resp = client.get("/api/stocks?search=%20%20%20")
    assert resp.status_code == 200
    stocks = resp.json()
    assert len(stocks) >= 30


def test_t2_search_nonexistent_ticker_lookup_returns_404(client):
    """GET /api/stocks/NONEXISTENT999 returns HTTP 404 Not Found."""
    resp = client.get("/api/stocks/NONEXISTENT999")
    assert resp.status_code == 404
    data = resp.json()
    assert "not found" in data.get("detail", "").lower()


def test_t2_search_sql_injection_metacharacters(client):
    """Search query containing SQL injection fragments is safely handled without 500 error."""
    payload = "' OR '1'='1; --"
    resp = client.get("/api/stocks", params={"search": payload})
    assert resp.status_code == 200
    # Must return empty list or safe filtered results, never dump internal DB errors
    assert isinstance(resp.json(), list)


def test_t2_search_xss_script_tags(client):
    """Search query containing XSS script tags is safely handled."""
    payload = "<script>alert('xss')</script>"
    resp = client.get("/api/stocks", params={"search": payload})
    assert resp.status_code == 200
    assert isinstance(resp.json(), list)


def test_t2_search_extreme_unicode_and_emojis(client):
    """Search with emojis and complex unicode strings handles gracefully."""
    resp = client.get("/api/stocks", params={"search": "🚀🔥💎Alpha"})
    assert resp.status_code == 200
    assert isinstance(resp.json(), list)


# ==============================================================================
# 2. Filter & Pagination Boundaries (F1)
# ==============================================================================

def test_t2_filter_invalid_zone_code_returns_empty_list(client):
    """Querying an unrecognized zone code returns empty list without 500 crash."""
    resp = client.get("/api/stocks?zone=INVALID_ZONE_999")
    assert resp.status_code == 200
    assert resp.json() == []


def test_t2_pagination_limit_zero_returns_empty_list(client):
    """Query with limit=0 returns 0 stock records."""
    resp = client.get("/api/stocks?limit=0")
    assert resp.status_code == 200
    assert len(resp.json()) == 0


def test_t2_pagination_negative_offset_rejected(client):
    """Query with negative offset ?offset=-1 returns HTTP 400 Bad Request."""
    resp = client.get("/api/stocks?offset=-1")
    assert resp.status_code == 400


def test_t2_pagination_negative_limit_rejected(client):
    """Query with negative limit ?limit=-5 returns HTTP 400 Bad Request."""
    resp = client.get("/api/stocks?limit=-5")
    assert resp.status_code == 400


def test_t2_pagination_extreme_large_limit(client):
    """Query with limit=10000 returns all available stocks without memory crash."""
    resp = client.get("/api/stocks?limit=10000")
    assert resp.status_code == 200
    stocks = resp.json()
    assert len(stocks) >= 30


# ==============================================================================
# 3. License Key Boundaries (F5)
# ==============================================================================

def test_t2_license_empty_string_rejected(client):
    """License validation with empty string returns valid=False."""
    resp = client.post("/api/auth/validate", json={"license_key": ""})
    assert resp.status_code == 200
    data = resp.json()
    assert data.get("valid") is False


def test_t2_license_whitespace_only_rejected(client):
    """License validation with whitespace returns valid=False."""
    resp = client.post("/api/auth/validate", json={"license_key": "    "})
    assert resp.status_code == 200
    assert resp.json().get("valid") is False


def test_t2_license_very_short_key_rejected(client):
    """Short 2-character license key returns valid=False."""
    resp = client.post("/api/auth/validate", json={"license_key": "AB"})
    assert resp.status_code == 200
    assert resp.json().get("valid") is False


def test_t2_license_massive_buffer_overflow_string(client):
    """Massive 4096-character string is rejected gracefully without DoS or crash."""
    massive_key = "DEMO-" + "A" * 4096
    resp = client.post("/api/auth/validate", json={"license_key": massive_key})
    assert resp.status_code == 200
    assert resp.json().get("valid") is False


def test_t2_license_missing_required_field_returns_422(client):
    """Request missing 'license_key' field returns 422 Unprocessable Entity."""
    resp = client.post("/api/auth/validate", json={})
    assert resp.status_code == 422


def test_t2_license_sql_injection_payload_rejected(client):
    """SQL injection in license_key payload is safely rejected."""
    payload = {"license_key": "' OR '1'='1' --"}
    resp = client.post("/api/auth/validate", json=payload)
    assert resp.status_code == 200
    assert resp.json().get("valid") is False


# ==============================================================================
# 4. Position Doctor Mathematical Boundaries (F7)
# ==============================================================================

def test_t2_doctor_zero_entry_price_rejected(client):
    """Position Doctor rejects entry_price = 0.0 with 422 validation error."""
    payload = {"ticker": "CELH", "entry_price": 0.0, "days_held": 10, "current_price": 27.0}
    resp = client.post("/api/pro/position-doctor", json=payload)
    assert resp.status_code == 422


def test_t2_doctor_negative_entry_price_rejected(client):
    """Position Doctor rejects negative entry_price with 422 validation error."""
    payload = {"ticker": "CELH", "entry_price": -25.0, "days_held": 10, "current_price": 27.0}
    resp = client.post("/api/pro/position-doctor", json=payload)
    assert resp.status_code == 422


def test_t2_doctor_negative_days_held_rejected(client):
    """Position Doctor rejects negative days_held with 422 validation error."""
    payload = {"ticker": "CELH", "entry_price": 30.0, "days_held": -5, "current_price": 27.0}
    resp = client.post("/api/pro/position-doctor", json=payload)
    assert resp.status_code == 422


def test_t2_doctor_exact_minus_9_pct_boundary(client):
    """Exact -9.00% return triggers Rule 1 (-9% Hard Stop Loss)."""
    # entry 100.0, current 91.0 -> exactly -9.0%
    payload = {"ticker": "MBLY", "entry_price": 100.0, "days_held": 10, "current_price": 91.0}
    resp = client.post("/api/pro/position-doctor", json=payload)
    assert resp.status_code == 200
    data = resp.json()
    assert data.get("status_code") == "HARD_STOP"
    assert data.get("is_critical") is True


def test_t2_doctor_55_days_and_7_9_pct_triggers_time_stop(client):
    """Held 55 days with +7.9% return (< +8%) triggers Rule 2 (55D Time-Stop)."""
    payload = {"ticker": "MBLY", "entry_price": 100.0, "days_held": 55, "current_price": 107.9}
    resp = client.post("/api/pro/position-doctor", json=payload)
    assert resp.status_code == 200
    data = resp.json()
    assert data.get("status_code") == "TIME_STOP"
    assert "Rule 2" in data.get("rule_triggered", "")


def test_t2_doctor_55_days_and_8_1_pct_maintains_hold(client):
    """Held 55 days with +8.1% return (>= +8%) stays in Rule 4 (Normal Hold)."""
    payload = {"ticker": "MBLY", "entry_price": 100.0, "days_held": 55, "current_price": 108.1}
    resp = client.post("/api/pro/position-doctor", json=payload)
    assert resp.status_code == 200
    data = resp.json()
    assert data.get("status_code") == "HOLD"


def test_t2_doctor_exact_100_pct_tp1_harvest(client):
    """Exact +100.0% return triggers Rule 3 (+100% TP1 Principal Recovery)."""
    payload = {"ticker": "MBLY", "entry_price": 50.0, "days_held": 30, "current_price": 100.0}
    resp = client.post("/api/pro/position-doctor", json=payload)
    assert resp.status_code == 200
    data = resp.json()
    assert data.get("status_code") == "TP1_HARVEST"
    assert "50%" in data.get("action_plan", "")


# ==============================================================================
# 5. Headers & Security Boundaries
# ==============================================================================

def test_t2_header_missing_auth_on_vault_returns_401(client):
    """Accessing /api/pro/vault with no Authorization header returns 401."""
    resp = client.get("/api/pro/vault")
    assert resp.status_code in [401, 403]


def test_t2_header_malformed_auth_header_returns_401(client):
    """Malformed Authorization header without 'Bearer ' prefix returns 401."""
    resp = client.get("/api/pro/vault", headers={"Authorization": "Basic PRO-DEMO-2026"})
    assert resp.status_code in [401, 403]


def test_t2_header_invalid_bearer_token_returns_401(client):
    """Bearer with invalid random token returns 401."""
    resp = client.get("/api/pro/vault", headers={"Authorization": "Bearer INVALID-GARBAGE-TOKEN"})
    assert resp.status_code in [401, 403]


def test_t2_method_not_allowed_on_stocks(client):
    """DELETE /api/stocks returns 405 Method Not Allowed."""
    resp = client.delete("/api/stocks")
    assert resp.status_code in [405, 404]


def test_t2_nonexistent_endpoint_returns_404(client):
    """GET /api/nonexistent_route_xyz returns 404 Not Found."""
    resp = client.get("/api/nonexistent_route_xyz")
    assert resp.status_code == 404


# ==============================================================================
# 6. Referral Provider & URL Boundaries (F9/F10)
# ==============================================================================

def test_t2_referral_unknown_provider_rejected(client):
    """Building referral link with unsupported provider returns 400 Bad Request."""
    resp = client.get("/api/referral/build?provider=unsupported_network&ticker=AAPL")
    assert resp.status_code == 400


def test_t2_referral_empty_provider_rejected(client):
    """Building referral link with empty provider returns 400 Bad Request."""
    resp = client.get("/api/referral/build?provider=&ticker=AAPL")
    assert resp.status_code in [400, 422]


def test_t2_referral_special_characters_in_ticker(client):
    """Ticker containing slashes or symbols is handled without crashing."""
    resp = client.get("/api/referral/build?provider=tradingview&ticker=BRK.B")
    assert resp.status_code == 200
    assert "BRK.B" in resp.json().get("url", "")


def test_t2_referral_redirect_invalid_provider_returns_404(client):
    """Redirecting through invalid referral provider returns 404."""
    resp = client.get("/api/referral/redirect/invalid_provider?ticker=AAPL")
    assert resp.status_code == 404


def test_t2_referral_missing_ticker_defaults_safely(client):
    """Omitting ticker defaults to safe benchmark ticker without crashing."""
    resp = client.get("/api/referral/build?provider=tradingview")
    assert resp.status_code == 200
    assert "url" in resp.json()
