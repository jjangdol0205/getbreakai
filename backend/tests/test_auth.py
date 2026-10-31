"""
backend/tests/test_auth.py - Unit and Integration Tests for Milestone 2 Monetization & Auth
"""
import pytest
from fastapi.testclient import TestClient

from backend.app.main import app
from backend.app.services.license_service import license_service


@pytest.fixture
def api_client():
    return TestClient(app)


def test_license_service_demo_key_valid():
    """Validates PRO-DEMO-2026 returns valid=True and tier=pro."""
    res = license_service.validate_key("PRO-DEMO-2026")
    assert res.valid is True
    assert res.tier == "pro"
    assert res.license_key == "PRO-DEMO-2026"
    assert res.expires_at is not None


def test_license_service_case_insensitivity_and_trim():
    """Validates that casing and whitespace are trimmed correctly."""
    res = license_service.validate_key("  pro-demo-2026  ")
    assert res.valid is True
    assert res.tier == "pro"
    assert res.license_key == "PRO-DEMO-2026"


def test_license_service_empty_and_short_keys():
    """Validates that empty and short keys are safely rejected."""
    r_empty = license_service.validate_key("")
    assert r_empty.valid is False
    assert r_empty.tier == "free"

    r_space = license_service.validate_key("   ")
    assert r_space.valid is False

    r_short = license_service.validate_key("ABC")
    assert r_short.valid is False


def test_license_service_invalid_keys():
    """Validates that non-demo keys are rejected."""
    res = license_service.validate_key("INVALID-KEY-12345")
    assert res.valid is False
    assert res.tier == "free"


def test_api_auth_validate_endpoint_success(api_client):
    """POST /api/auth/validate with demo key returns 200 OK."""
    payload = {"license_key": "PRO-DEMO-2026"}
    res = api_client.post("/api/auth/validate", json=payload)
    assert res.status_code == 200
    data = res.json()
    assert data["valid"] is True
    assert data["tier"] == "pro"
    assert data["license_key"] == "PRO-DEMO-2026"


def test_api_auth_license_validate_endpoint_alias(api_client):
    """POST /api/auth/license/validate works identically to /api/auth/validate."""
    payload = {"license_key": "PRO-DEMO-2026", "instance_name": "TestMac"}
    res = api_client.post("/api/auth/license/validate", json=payload)
    assert res.status_code == 200
    data = res.json()
    assert data["valid"] is True
    assert data["tier"] == "pro"


def test_api_auth_validate_invalid_key_returns_valid_false(api_client):
    """POST /api/auth/validate with invalid key returns 200 with valid=False."""
    payload = {"license_key": "EXPIRED-KEY-999"}
    res = api_client.post("/api/auth/validate", json=payload)
    assert res.status_code == 200
    data = res.json()
    assert data["valid"] is False
    assert data["tier"] == "free"


def test_api_auth_validate_missing_field_returns_422(api_client):
    """POST /api/auth/validate with missing required license_key returns 422."""
    res = api_client.post("/api/auth/validate", json={})
    assert res.status_code == 422
