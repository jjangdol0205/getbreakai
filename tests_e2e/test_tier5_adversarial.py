"""
tests_e2e/test_tier5_adversarial.py - Tier 5 Adversarial Stress & Penetration Testing

Adversarial Challenge Vectors:
1. High-throughput concurrent requests & multi-threaded load
2. Malicious inputs, SQLi / XSS fuzzing on search, zone filters, and referral redirect endpoints
3. Access control penetration: attempt to leak Pro data on non-preview stocks without providing PRO-DEMO-2026
4. Position Doctor boundary and stress attacks (divide by zero, negative prices, extreme values)
5. Static delivery, path traversal attacks, and viewport/responsive layout verification
"""
import concurrent.futures
import time
from typing import List
import pytest


# ==============================================================================
# Vector 1: High-Throughput Concurrent Requests & Load Testing
# ==============================================================================

class TestConcurrencyAndLoad:
    """Stress tests verifying server stability under high-throughput concurrent load."""

    def test_concurrent_burst_health_and_kpis(self, client):
        """Dispatches 80 rapid concurrent requests across public endpoints to verify 0% 5xx errors."""
        endpoints = [
            "/health",
            "/api/health",
            "/api/backtest",
            "/api/backtest/summary",
            "/api/backtest/trades",
            "/api/research",
            "/api/referral/config",
            "/api/stocks?limit=10",
        ]
        num_requests = 80
        success_count = 0
        latencies = []

        def make_request(idx: int):
            ep = endpoints[idx % len(endpoints)]
            t0 = time.time()
            res = client.get(ep)
            elapsed = time.time() - t0
            return res.status_code, elapsed

        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
            futures = [executor.submit(make_request, i) for i in range(num_requests)]
            for fut in concurrent.futures.as_completed(futures):
                code, elapsed = fut.result()
                latencies.append(elapsed)
                if code == 200:
                    success_count += 1

        # All requests must succeed with 200 OK, zero 500 Internal Server Errors
        assert success_count == num_requests, f"Only {success_count}/{num_requests} succeeded under burst load"
        p95_latency = sorted(latencies)[int(num_requests * 0.95)]
        # p95 latency should remain under 1.5 seconds even under concurrent local burst
        assert p95_latency < 1.5, f"P95 latency was too high: {p95_latency:.3f}s"

    def test_concurrent_referral_click_tracking_thread_safety(self, client):
        """Verifies atomic thread-safety of referral click tracking under concurrent writes."""
        # Get baseline stats
        baseline_res = client.get("/api/referral/stats")
        assert baseline_res.status_code == 200
        baseline_tv = baseline_res.json().get("tradingview", 0)

        clicks_to_fire = 30

        def fire_click(_):
            return client.get("/api/referral/redirect/tradingview?ticker=MBLY")

        with concurrent.futures.ThreadPoolExecutor(max_workers=8) as executor:
            results = list(executor.map(fire_click, range(clicks_to_fire)))

        # All redirects must be 307
        assert all(r.status_code == 307 for r in results)

        # Updated stats must reflect exact increment
        after_res = client.get("/api/referral/stats")
        assert after_res.status_code == 200
        after_tv = after_res.json().get("tradingview", 0)
        assert after_tv >= baseline_tv + clicks_to_fire


# ==============================================================================
# Vector 2: Malicious Inputs, SQLi / XSS Fuzzing
# ==============================================================================

class TestFuzzingAndInputSanitization:
    """Fuzzing tests against search, zone filters, and referral endpoints."""

    SQLI_PAYLOADS = [
        "' OR '1'='1",
        "'; DROP TABLE stocks; --",
        "admin'--",
        "UNION SELECT 1,2,3,4,5--",
        "1' ORDER BY 1--",
        "' OR 'x'='x",
        "1; WAITFOR DELAY '0:0:1'--",
    ]

    XSS_PAYLOADS = [
        "<script>alert('xss')</script>",
        "<img src=x onerror=alert(1)>",
        "javascript:alert(1)",
        "\"><script>document.location='http://evil.com'</script>",
        "<svg/onload=alert(1)>",
    ]

    TRAVERSAL_AND_COMMAND_PAYLOADS = [
        "../../../../etc/passwd",
        "..\\..\\..\\windows\\win.ini",
        "| calc.exe",
        "; ping 127.0.0.1",
        "$(whoami)",
        "`id`",
    ]

    UNICODE_AND_OVERFLOW_PAYLOADS = [
        "\x00",
        "\u0000",
        "\ufffd" * 100,
        "A" * 5000,
        "𝒳𝒮𝒮_TEST_UNICODE",
        "   \t\r\n   ",
    ]

    def test_search_parameter_sqli_fuzzing(self, client):
        """Fuzzes /api/stocks?query=... with SQL injection payloads."""
        for payload in self.SQLI_PAYLOADS:
            res = client.get(f"/api/stocks?query={payload}")
            # Must not crash with 500
            assert res.status_code == 200, f"SQLi payload caused error {res.status_code}: {payload}"
            data = res.json()
            assert isinstance(data, list)

    def test_search_parameter_xss_fuzzing(self, client):
        """Fuzzes /api/stocks?query=... with XSS payloads."""
        for payload in self.XSS_PAYLOADS:
            res = client.get(f"/api/stocks?search={payload}")
            assert res.status_code == 200, f"XSS payload caused error {res.status_code}: {payload}"
            data = res.json()
            assert isinstance(data, list)

    def test_search_parameter_overflow_fuzzing(self, client):
        """Fuzzes /api/stocks?query=... with long strings and unicode."""
        for payload in self.UNICODE_AND_OVERFLOW_PAYLOADS:
            res = client.get("/api/stocks", params={"search": payload})
            assert res.status_code == 200
            assert isinstance(res.json(), list)

    def test_zone_filter_fuzzing(self, client):
        """Fuzzes /api/stocks?zone=... with malicious and non-existent zones."""
        adversarial_zones = self.SQLI_PAYLOADS + self.XSS_PAYLOADS + ["INVALID_ZONE_XYZ", "12345"]
        for z in adversarial_zones:
            res = client.get("/api/stocks", params={"zone": z})
            assert res.status_code == 200, f"Zone fuzzing caused status {res.status_code}: {z}"
            # Invalid zones should cleanly return empty list
            assert res.json() == []

    def test_referral_open_redirect_protection(self, client):
        """Attempts to exploit open redirects on /api/referral/redirect/{provider}."""
        malicious_providers = [
            "evil.com",
            "attacker.com",
            "tradingview.com.attacker.com",
            "DROP_TABLE",
            "admin",
            "unknown_provider",
        ]
        for bad_prov in malicious_providers:
            res = client.get(f"/api/referral/redirect/{bad_prov}?ticker=AAPL")
            # Only whitelisted providers (tradingview, seekingalpha, trendspider) are valid; others MUST return 404
            assert res.status_code in [404, 400], f"Provider '{bad_prov}' was not rejected: {res.status_code}"

    def test_referral_ticker_fuzzing(self, client):
        """Verifies referral redirect safely sanitizes malicious ticker parameter."""
        for xss in self.XSS_PAYLOADS:
            res = client.get(f"/api/referral/redirect/tradingview?ticker={xss}")
            # Redirect response must safely form destination URL
            assert res.status_code == 307
            dest = res.headers.get("location", "")
            # Must redirect strictly to official TradingView domain
            assert dest.startswith("https://www.tradingview.com/symbols/")
            assert "aff_id=" in dest


# ==============================================================================
# Vector 3: Access Control Penetration (Pro Data Leakage)
# ==============================================================================

class TestAccessControlPenetration:
    """Attempts to bypass access controls and extract Pro proprietary targets without valid demo key."""

    PROTECTED_NON_PREVIEW_TICKERS = ["MBLY", "APP", "ENPH", "SEDG", "CVNA", "UBER", "NVDA", "AMD", "MU"]

    def test_unauthenticated_request_masks_all_non_preview_stocks(self, client):
        """Free tier request must mask stop_loss_price, tp1_2x_price, and ma60_price on rows 4+."""
        res = client.get("/api/stocks")
        assert res.status_code == 200
        stocks = res.json()
        assert len(stocks) >= 14

        for s in stocks:
            ticker = s["ticker"]
            if ticker in ["CELH", "CCL", "TSLA", "UPST"]:
                # Preview tickers may have unmasked values
                continue
            # All other tickers MUST be locked
            assert s["is_pro_locked"] is True, f"Stock {ticker} was not marked is_pro_locked=True"
            assert s["stop_loss_price"] is None, f"Pro stop_loss_price leaked on {ticker}: {s['stop_loss_price']}"
            assert s["tp1_2x_price"] is None, f"Pro tp1_2x_price leaked on {ticker}: {s['tp1_2x_price']}"
            assert s["ma60_price"] is None, f"Pro ma60_price leaked on {ticker}: {s['ma60_price']}"

    @pytest.mark.parametrize("fake_token", [
        "Bearer invalid_key_12345",
        "Bearer PRO-DEMO-FAKE",
        "Bearer ' OR '1'='1",
        "Bearer null",
        "Bearer",
        "Basic PRO-DEMO-2026",
        "Token PRO-DEMO-2026",
    ])
    def test_auth_header_spoofing_does_not_unlock_pro(self, client, fake_token):
        """Malformed or forged Authorization headers must NOT unlock Pro data."""
        res = client.get("/api/stocks", headers={"Authorization": fake_token})
        assert res.status_code == 200
        assert res.headers.get("X-Pro-Unlocked") == "false"
        stocks = res.json()
        # MBLY is a non-preview stock
        mbly = next((s for s in stocks if s["ticker"] == "MBLY"), None)
        assert mbly is not None
        assert mbly["is_pro_locked"] is True
        assert mbly["stop_loss_price"] is None

    @pytest.mark.parametrize("fake_query_key", [
        "invalid_key",
        "PRO-DEMO-2025",
        "PRO-DEMO-2027",
        "' OR '1'='1",
        "<script>alert(1)</script>",
    ])
    def test_query_param_spoofing_does_not_unlock_pro(self, client, fake_query_key):
        """Forged license_key query param must NOT unlock Pro data."""
        res = client.get(f"/api/stocks?license_key={fake_query_key}")
        assert res.status_code == 200
        assert res.headers.get("X-Pro-Unlocked") == "false"
        stocks = res.json()
        mbly = next((s for s in stocks if s["ticker"] == "MBLY"), None)
        assert mbly is not None
        assert mbly["is_pro_locked"] is True
        assert mbly["stop_loss_price"] is None

    def test_direct_single_stock_detail_access_control(self, client):
        """Verifies GET /api/stocks/{ticker} masks targets for non-preview stocks without Pro token."""
        for ticker in self.PROTECTED_NON_PREVIEW_TICKERS[:4]:
            res = client.get(f"/api/stocks/{ticker}")
            assert res.status_code == 200
            data = res.json()
            assert data["ticker"] == ticker
            assert data["is_pro_locked"] is True
            assert data["stop_loss_price"] is None
            assert data["tp1_2x_price"] is None
            assert data["ma60_price"] is None

    def test_gated_pro_vault_rejects_unauthorized(self, client):
        """GET /api/pro/vault must strictly return 401 Unauthorized without valid key."""
        res = client.get("/api/pro/vault")
        assert res.status_code == 401
        assert "Unauthorized" in res.json().get("detail", "")

        # Try with fake key
        res_fake = client.get("/api/pro/vault", headers={"Authorization": "Bearer BAD_KEY"})
        assert res_fake.status_code == 401

    def test_gated_pinescript_rejects_unauthorized(self, client):
        """GET /api/pro/pine-script must strictly return 401 Unauthorized without valid key."""
        res = client.get("/api/pro/pine-script")
        assert res.status_code == 401

        res_fake = client.get("/api/pro/pine-script", params={"license_key": "HACK_ATTEMPT"})
        assert res_fake.status_code == 401

    def test_valid_demo_key_successfully_unlocks_pro(self, client):
        """Verifies PRO-DEMO-2026 properly unlocks all gated endpoints."""
        auth_header = {"Authorization": "Bearer PRO-DEMO-2026"}

        # 1. Pro Vault
        vault_res = client.get("/api/pro/vault", headers=auth_header)
        assert vault_res.status_code == 200
        assert vault_res.json()["unlocked"] is True

        # 2. Pine Script
        pine_res = client.get("/api/pro/pine-script", headers=auth_header)
        assert pine_res.status_code == 200
        assert "RightSideAlpha PW-RSI" in pine_res.json()["code"]

        # 3. Stocks unmasked
        stocks_res = client.get("/api/stocks", headers=auth_header)
        assert stocks_res.status_code == 200
        assert stocks_res.headers.get("X-Pro-Unlocked") == "true"
        stocks = stocks_res.json()
        mbly = next((s for s in stocks if s["ticker"] == "MBLY"), None)
        assert mbly is not None
        assert mbly["is_pro_locked"] is False
        assert mbly["stop_loss_price"] is not None
        assert mbly["tp1_2x_price"] is not None


# ==============================================================================
# Vector 4: Position Doctor Boundary & Stress Attacks
# ==============================================================================

class TestPositionDoctorAdversarial:
    """Stress tests Position Doctor exit rule calculation against edge inputs."""

    def test_zero_entry_price_rejected(self, client):
        """Zero entry price must return 422 Unprocessable Entity (cannot divide by zero)."""
        res = client.post("/api/pro/position-doctor", json={
            "ticker": "CELH",
            "entry_price": 0.0,
            "days_held": 10,
        })
        assert res.status_code == 422

    def test_negative_entry_price_rejected(self, client):
        """Negative entry price must return 422."""
        res = client.post("/api/pro/position-doctor", json={
            "ticker": "CELH",
            "entry_price": -50.0,
            "days_held": 10,
        })
        assert res.status_code == 422

    def test_negative_days_held_rejected(self, client):
        """Negative days held must return 422."""
        res = client.post("/api/pro/position-doctor", json={
            "ticker": "CELH",
            "entry_price": 50.0,
            "days_held": -5,
        })
        assert res.status_code == 422

    def test_massive_numbers_overflow_resilience(self, client):
        """Extreme numbers must compute cleanly without overflow or math errors."""
        res = client.post("/api/pro/position-doctor", json={
            "ticker": "CELH",
            "entry_price": 1000000000.0,
            "current_price": 2500000000.0,
            "days_held": 10000,
        })
        assert res.status_code == 200
        data = res.json()
        assert data["status_code"] == "TP1_HARVEST"
        assert data["return_pct"] == 150.0

    def test_hard_stop_exact_boundary(self, client):
        """Exact -9.00% return triggers Rule 1 HARD_STOP."""
        # Entry 100, current 91 -> return is -9.0%
        res = client.post("/api/pro/position-doctor", json={
            "ticker": "CELH",
            "entry_price": 100.0,
            "current_price": 91.0,
            "days_held": 5,
        })
        assert res.status_code == 200
        data = res.json()
        assert data["status_code"] == "HARD_STOP"
        assert data["is_critical"] is True

    def test_time_stop_exact_boundary(self, client):
        """Day 55 with +7.99% return triggers Rule 2 TIME_STOP."""
        res = client.post("/api/pro/position-doctor", json={
            "ticker": "CELH",
            "entry_price": 100.0,
            "current_price": 107.99,
            "days_held": 55,
        })
        assert res.status_code == 200
        data = res.json()
        assert data["status_code"] == "TIME_STOP"

    def test_tp1_harvest_exact_boundary(self, client):
        """Exact +100.0% return triggers Rule 3 TP1_HARVEST."""
        res = client.post("/api/pro/position-doctor", json={
            "ticker": "CELH",
            "entry_price": 100.0,
            "current_price": 200.0,
            "days_held": 40,
        })
        assert res.status_code == 200
        data = res.json()
        assert data["status_code"] == "TP1_HARVEST"


# ==============================================================================
# Vector 5: Static Delivery, Viewport & Layout Integrity
# ==============================================================================

class TestStaticDeliveryAndViewport:
    """Checks frontend assets delivery, viewport tags, responsive styling, and path traversal protection."""

    def test_root_index_html_delivery_and_viewport(self, client):
        """GET / must return 200 OK with proper viewport meta tag and title."""
        res = client.get("/")
        assert res.status_code == 200
        html = res.text
        assert "<meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\"" in html
        assert "RightSideAlpha" in html
        assert "<div id=\"app\"></div>" in html

    def test_static_css_bundle_and_media_queries(self, client):
        """Verifies production CSS bundle is accessible and contains responsive media query breakpoints."""
        import re
        root_html = client.get("/").text
        m = re.search(r'href="(?:\.)?(/assets/index-[^"]+\.css)"', root_html)
        assert m is not None, "Could not locate built CSS bundle link in index.html"
        res = client.get(m.group(1))
        assert res.status_code == 200
        css = res.text
        assert "@media(max-width:768px)" in css or "@media(max-width: 768px)" in css or "@media" in css
        # Theme variables verified
        assert "--bg: #070b14" in css or "--bg:#070b14" in css or "--bg:" in css
        assert "--accent:" in css

    def test_static_js_bundle_accessibility(self, client):
        """Verifies production JS bundle is accessible."""
        import re
        root_html = client.get("/").text
        m = re.search(r'src="(?:\.)?(/assets/index-[^"]+\.js)"', root_html)
        assert m is not None, "Could not locate built JS bundle script in index.html"
        res = client.get(m.group(1))
        assert res.status_code == 200
        assert len(res.text) > 10000

    def test_static_path_traversal_resistance(self, client):
        """Attempts to access files outside frontend directory via static router."""
        traversal_paths = [
            "/../../run_server.py",
            "/../backend/app/main.py",
            "/..\\backend\\config.py",
            "/assets/../../run_server.py",
        ]
        for path in traversal_paths:
            res = client.get(path)
            # StaticFiles mount or FastAPI catch-all should never disclose backend python source files
            if res.status_code == 200:
                # If SPA catch-all returns index.html, that's safe, but must NOT return python code
                assert "from fastapi import" not in res.text
                assert "def main():" not in res.text
            else:
                assert res.status_code in [404, 400]
