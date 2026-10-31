"""
backend/tests/test_adversarial.py - Empirical Adversarial Challenge Suite for Milestone 1

Covers:
1. Data Masking Security & Leakage Vectors (Search bypass, Zone bypass, Sort bypass, Spoofing)
2. Malicious & Fuzz Inputs (SQL Injection, XSS, Path Traversal, Unicode, Boundary Limits)
3. Mathematical Edge Cases (Zero division, Negative values, Extreme Volatility in Position Doctor)
4. High-Volume & Concurrency Simulation
"""
import concurrent.futures
import math
import pytest
from fastapi.testclient import TestClient

from backend.app.main import app


@pytest.fixture(scope="module")
def client():
    with TestClient(app) as c:
        yield c


# ==============================================================================
# CATEGORY 1: DATA MASKING SECURITY & LEAKAGE VECTORS
# ==============================================================================

class TestDataMaskingSecurity:
    """
    Verifies that a free user CANNOT recover stop_loss_price, tp1_2x_price,
    or ma60_price for rows >= 4 through query parameters, headers, or manipulation.
    """

    def test_default_unauthenticated_masking_boundary(self, client):
        """Free user requesting default /api/stocks must only get 4 preview rows unmasked."""
        res = client.get("/api/stocks")
        assert res.status_code == 200
        stocks = res.json()
        assert len(stocks) == 72
        assert all("." not in s["ticker"] for s in stocks)

        # First 4 rows (0..3) are public previews
        for i in range(4):
            assert stocks[i]["is_pro_locked"] is False
            assert stocks[i]["stop_loss_price"] is not None

        # All subsequent rows (4..98) must be masked
        for i in range(4, len(stocks)):
            assert stocks[i]["is_pro_locked"] is True
            assert stocks[i]["stop_loss_price"] is None
            assert stocks[i]["tp1_2x_price"] is None
            assert stocks[i]["ma60_price"] is None

    def test_search_parameter_leakage_vector(self, client):
        """
        SECURITY CHALLENGE:
        When a free user searches for a specific non-preview ticker (e.g. MBLY, APP, ENPH),
        does the API leak proprietary target prices because the filtered list places it at index 0?
        """
        # MBLY is at index 4 in default list, so it is a PRO-only row.
        res = client.get("/api/stocks?search=MBLY")
        assert res.status_code == 200
        stocks = res.json()
        assert len(stocks) > 0
        mbly = next((s for s in stocks if s["ticker"] == "MBLY"), None)
        assert mbly is not None

        # EXPECTED DEFENSE: Free users MUST NOT recover MBLY target prices via search!
        # If this fails, it proves the data masking vulnerability.
        assert mbly["is_pro_locked"] is True, "VULNERABILITY: Non-preview ticker unmasked via search!"
        assert mbly["stop_loss_price"] is None, "VULNERABILITY: stop_loss_price leaked via search!"
        assert mbly["tp1_2x_price"] is None, "VULNERABILITY: tp1_2x_price leaked via search!"
        assert mbly["ma60_price"] is None, "VULNERABILITY: ma60_price leaked via search!"

    def test_query_parameter_leakage_vector(self, client):
        """SECURITY CHALLENGE: Test search alias `query` parameter for leakage."""
        res = client.get("/api/stocks?query=APP")
        assert res.status_code == 200
        stocks = res.json()
        app_stock = next((s for s in stocks if s["ticker"] == "APP"), None)
        assert app_stock is not None
        assert app_stock["is_pro_locked"] is True, "VULNERABILITY: APP unmasked via query alias!"
        assert app_stock["stop_loss_price"] is None, "VULNERABILITY: stop_loss_price leaked via query alias!"

    def test_zone_filtering_leakage_vector(self, client):
        """
        SECURITY CHALLENGE:
        Filtering by zone (e.g. LEFT_SIDE_KNIFE) puts non-preview stocks into indices 0..3 of filtered list.
        Verify they remain masked for free users.
        """
        res = client.get("/api/stocks?zone=LEFT_SIDE_KNIFE")
        assert res.status_code == 200
        stocks = res.json()
        assert len(stocks) > 0
        for s in stocks:
            # Check non-preview tickers in the filtered zone
            if s["ticker"] not in {"CELH", "CCL", "TSLA", "UPST"}:
                assert s["is_pro_locked"] is True, f"VULNERABILITY: Non-preview {s['ticker']} unmasked via zone filter!"
                assert s["stop_loss_price"] is None, f"VULNERABILITY: stop_loss_price leaked for {s['ticker']}!"

    def test_sort_by_leakage_vector(self, client):
        """
        SECURITY CHALLENGE:
        Sorting by score descending or price changes which stocks occupy rows 0..3.
        Verify that non-preview stocks do not get accidentally unmasked.
        """
        res = client.get("/api/stocks?sort_by=score&order=desc")
        assert res.status_code == 200
        stocks = res.json()
        for idx, s in enumerate(stocks):
            if s["ticker"] not in {"CELH", "CCL", "TSLA", "UPST"}:
                assert s["is_pro_locked"] is True, f"VULNERABILITY: Non-preview {s['ticker']} unmasked via sorting!"
                assert s["stop_loss_price"] is None

    def test_header_spoofing_defense(self, client):
        """Arbitrary spoofed headers must NOT grant Pro access."""
        spoofed_headers = [
            {"X-Pro-Unlocked": "true"},
            {"X-Is-Pro": "true"},
            {"X-User-Role": "admin"},
            {"Authorization": "Bearer INVALID_TOKEN_123"},
            {"Authorization": "Bearer "},
            {"Authorization": "Basic YWRtaW46cGFzc3dvcmQ="},
        ]
        for headers in spoofed_headers:
            res = client.get("/api/stocks", headers=headers)
            assert res.status_code == 200
            assert res.headers.get("X-Pro-Unlocked") == "false"
            row_4 = res.json()[4]
            assert row_4["is_pro_locked"] is True
            assert row_4["stop_loss_price"] is None

    def test_license_key_tampering_and_case(self, client):
        """Test variations and near-misses of demo license key."""
        invalid_keys = [
            "PRO-DEMO-2025",
            "PRO-DEMO-2027",
            "PRO-DEMO",
            "DEMO-2026",
            "PRO_DEMO_2026",
            "' OR '1'='1",
            "<script>",
            "null",
            "None",
            "True",
        ]
        for key in invalid_keys:
            res = client.get(f"/api/stocks?license_key={key}")
            assert res.status_code == 200
            assert res.headers.get("X-Pro-Unlocked") == "false"
            assert res.json()[4]["is_pro_locked"] is True

        # Valid key in lowercase or padded must unlock
        res_lower = client.get("/api/stocks?license_key=pro-demo-2026")
        assert res_lower.status_code == 200
        assert res_lower.headers.get("X-Pro-Unlocked") == "true"
        assert res_lower.json()[4]["is_pro_locked"] is False


# ==============================================================================
# CATEGORY 2: MALICIOUS & FUZZ INPUTS
# ==============================================================================

class TestMaliciousAndFuzzInputs:
    """Stress tests input validation and error handling against hostile payloads."""

    @pytest.mark.parametrize("payload", [
        "' OR 1=1 --",
        "'; DROP TABLE stocks; --",
        "\" UNION SELECT * FROM users --",
        "1' OR '1'='1",
        "admin'--",
    ])
    def test_sql_injection_payloads(self, client, payload):
        """Endpoints must not crash (500) when fed SQL injection strings."""
        # 1. Stocks search
        r1 = client.get(f"/api/stocks?search={payload}")
        assert r1.status_code == 200
        assert isinstance(r1.json(), list)

        # 2. Stock detail path
        r2 = client.get(f"/api/stocks/{payload}")
        assert r2.status_code in (404, 422)

        # 3. Backtest trades filter
        r3 = client.get(f"/api/backtest/trades?ticker={payload}")
        assert r3.status_code == 200
        assert isinstance(r3.json(), list)

    @pytest.mark.parametrize("payload", [
        "<script>alert('XSS')</script>",
        "<img src=x onerror=alert(1)>",
        "\"><svg/onload=alert('XSS')>",
        "javascript:alert(1)",
    ])
    def test_xss_payloads(self, client, payload):
        """XSS payloads must be handled without 500 error or reflected execution."""
        r1 = client.get(f"/api/stocks?search={payload}")
        assert r1.status_code == 200

        r2 = client.get(f"/api/stocks/{payload}")
        assert r2.status_code in (404, 422)

    def test_path_traversal_payloads(self, client):
        """Path traversal attempts in stock and research routes must return 404, not 500."""
        traversal_attempts = [
            "/api/stocks/..%2f..%2fapp%2fconfig.py",
            "/api/stocks/..%5c..%5capp%5cconfig.py",
            "/api/research/..%2f..%2f..%2f..%2fetc%2fpasswd",
            "/api/research/....//....//config.py",
        ]
        for path in traversal_attempts:
            res = client.get(path)
            assert res.status_code in (404, 422)

    def test_unicode_and_extreme_strings(self, client):
        """Unicode characters, RTL markers, zero-width spaces, and large strings."""
        unicode_cases = [
            "삼성전자",               # Korean Hangul
            "トヨタ自動車",           # Japanese Kanji/Katakana
            "\u202Ereversed_txt",    # Right-to-Left Override
            "ZERO\u200BWIDTH",       # Zero-width space
            "🚀🔥💰📈",              # Emojis
            "A" * 5000,              # Very long string
            "   %20%20   ",          # Whitespace
        ]
        for u in unicode_cases:
            res = client.get("/api/stocks", params={"search": u})
            assert res.status_code == 200
            assert isinstance(res.json(), list)

    def test_query_parameter_boundary_and_type_confusion(self, client):
        """Invalid types or boundary violations in query parameters."""
        # limit == 0 returns empty list (HTTP 200)
        r_zero = client.get("/api/stocks?limit=0")
        assert r_zero.status_code == 200
        assert r_zero.json() == []

        # large limit returns all available stocks (HTTP 200)
        r_over = client.get("/api/stocks?limit=10000")
        assert r_over.status_code == 200
        assert len(r_over.json()) >= 30

        # limit string returns 422
        r_str = client.get("/api/stocks?limit=abc")
        assert r_str.status_code == 422

        # negative limit returns 400 Bad Request
        r_neg = client.get("/api/stocks?limit=-5")
        assert r_neg.status_code == 400

        # negative offset returns 400 Bad Request
        r_neg_off = client.get("/api/stocks?offset=-1")
        assert r_neg_off.status_code == 400

        # trades limit validation (pydantic ge=1)
        r_bt_zero = client.get("/api/backtest/trades?limit=0")
        assert r_bt_zero.status_code == 422


# ==============================================================================
# CATEGORY 3: MATHEMATICAL EDGE CASES IN POSITION DOCTOR
# ==============================================================================

class TestMathematicalEdgeCases:
    """Stress tests calculation boundaries, zero division, and extreme values."""

    def test_zero_entry_price(self, client):
        """entry_price = 0.0 must not crash with ZeroDivisionError."""
        payload = {
            "ticker": "CELH",
            "entry_price": 0.0,
            "days_held": 10,
            "current_price": 27.93,
        }
        res = client.post("/api/stocks/diagnose", json=payload)
        assert res.status_code == 200
        data = res.json()
        assert not math.isnan(data["return_pct"])
        assert not math.isinf(data["return_pct"])

    def test_negative_entry_price(self, client):
        """entry_price < 0 must be handled safely."""
        payload = {
            "ticker": "CELH",
            "entry_price": -50.0,
            "days_held": 10,
            "current_price": 25.0,
        }
        res = client.post("/api/stocks/diagnose", json=payload)
        assert res.status_code == 200
        data = res.json()
        assert isinstance(data["return_pct"], float)

    def test_negative_current_price(self, client):
        """current_price < 0 (abnormal crash/short) must trigger Rule 1 Hard Stop."""
        payload = {
            "ticker": "CELH",
            "entry_price": 50.0,
            "days_held": 5,
            "current_price": -10.0,
        }
        res = client.post("/api/stocks/diagnose", json=payload)
        assert res.status_code == 200
        data = res.json()
        assert data["status_code"] == "CRITICAL_STOP"
        assert data["is_critical"] is True

    def test_extreme_volatility_and_huge_numbers(self, client):
        """Extremely high returns or prices must not overflow float representation."""
        # 10,000x gain
        payload = {
            "ticker": "TSLA",
            "entry_price": 10.0,
            "days_held": 100,
            "current_price": 100000.0,
        }
        res = client.post("/api/stocks/diagnose", json=payload)
        assert res.status_code == 200
        data = res.json()
        assert data["status_code"] == "TP1_REACHED"
        assert data["return_pct"] == 999900.0

    def test_negative_days_held(self, client):
        """Negative days held (invalid clock) must not trigger dead money time stop."""
        payload = {
            "ticker": "CELH",
            "entry_price": 27.0,
            "days_held": -50,
            "current_price": 27.0,
        }
        res = client.post("/api/stocks/diagnose", json=payload)
        assert res.status_code == 200
        data = res.json()
        assert data["status_code"] != "DEAD_MONEY"

    def test_unknown_ticker_with_none_current_price(self, client):
        """Unknown ticker when current_price is None must default cleanly without crash."""
        payload = {
            "ticker": "NON_EXISTENT_TICKER_999",
            "entry_price": 100.0,
            "days_held": 10,
            "current_price": None,
        }
        res = client.post("/api/stocks/diagnose", json=payload)
        assert res.status_code == 200
        data = res.json()
    def test_untracked_ticker_zero_or_negative_entry_price_anomaly(self, client):
        """
        MATHEMATICAL EDGE CASE:
        When an untracked ticker has entry_price <= 0 and current_price is None,
        quant_engine assigns c_price = entry_price before correcting entry_price to 1.0,
        causing a false -100% or extreme negative return.
        """
        payload = {
            "ticker": "UNKNOWN_TICKER",
            "entry_price": 0.0,
            "days_held": 5,
            "current_price": None,
        }
        res = client.post("/api/stocks/diagnose", json=payload)
        assert res.status_code == 200
        data = res.json()
        # Ideal math handling: If entry_price is invalid/0 and no current price, return should be 0.0, not -100.0!
        assert data["return_pct"] == 0.0, f"MATHEMATICAL ANOMALY: return_pct calculated as {data['return_pct']}% for zero entry with no current price"


# ==============================================================================
# CATEGORY 4: CONCURRENCY & HIGH-VOLUME SIMULATION
# ==============================================================================

class TestConcurrencyAndHighVolume:
    """Simulates multi-threaded burst queries against the quant engine."""

    def test_concurrent_burst_requests(self, client):
        """100 concurrent requests across 10 threads hitting diverse endpoints."""
        endpoints = [
            "/api/stocks",
            "/api/stocks?search=CELH",
            "/api/stocks?zone=IGNITION_ZONE",
            "/api/stocks/CELH",
            "/api/stocks/MBLY",
            "/api/stocks?license_key=PRO-DEMO-2026",
            "/api/backtest/summary",
            "/api/backtest/trades?limit=10",
            "/api/research",
            "/api/health",
        ]

        def send_request(url):
            return client.get(url)

        tasks = endpoints * 10  # 100 requests total
        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
            responses = list(executor.map(send_request, tasks))

        assert len(responses) == 100
        for r in responses:
            assert r.status_code == 200, f"Failed with status {r.status_code}: {r.text}"
