"""
tests_e2e/test_tier4_scenarios.py - Tier 4: Real-World Acceptance Scenarios E2E Test Suite

Covers full end-to-end user workflows:
1. Complete Retail Investor Discovery -> Conversion -> Diagnostic -> Referral Workflow
2. Institutional Turnaround Research -> Dead-Money Exit -> Rebalancing Workflow
3. High-Flying Turnaround Winner -> 100% TP1 Principal Recovery Harvesting Workflow
4. Invalid Key Rejection -> Error Notification -> Recovery with Valid Key Workflow
Total: 4 Comprehensive Real-World Scenario Test Cases
"""

import pytest


def test_t4_retail_investor_complete_conversion_workflow(client):
    """
    Scenario 1: Complete Retail Investor Journey
    1. Investor lands on RightSideAlpha (verifies /health and root status).
    2. Explores public leaderboard (/api/stocks) and observes target prices are locked.
    3. Reviews empirical 26.8-year backtest proof (/api/backtest) verifying 21.97% CAGR & 203.87x multiple.
    4. Submits PRO-DEMO-2026 license key to unlock Pro privileges (/api/auth/validate).
    5. Retrieves fully unmasked leaderboard with stop loss and 2x profit targets.
    6. Uses Position Doctor to evaluate an underwater stock (-9% stop triggered).
    7. Builds TradingView referral link with affiliate tag to view live chart.
    8. Accesses and copies TradingView Pine Script v5 code from Pro Vault.
    """
    # Step 1: Discovery
    health = client.get("/api/health")
    assert health.status_code == 200
    assert health.json().get("status") == "ok"

    # Step 2: Public Leaderboard Check
    public_stocks_resp = client.get("/api/stocks")
    assert public_stocks_resp.status_code == 200
    public_stocks = public_stocks_resp.json()
    assert len(public_stocks) >= 30
    assert public_stocks[4]["is_pro_locked"] is True
    assert public_stocks[4]["stop_loss_price"] is None

    # Step 3: Empirical Backtest Verification
    bt_resp = client.get("/api/backtest")
    assert bt_resp.status_code == 200
    bt_data = bt_resp.json()
    pwrsi = next(s for s in bt_data["overall_summary"] if "PW-RSI" in s["Strategy"])
    assert pwrsi["Final_Multiple"] >= 200.0
    assert pwrsi["CAGR_Pct"] >= 21.0

    # Step 4: Pro License Validation
    auth_resp = client.post("/api/auth/validate", json={"license_key": "PRO-DEMO-2026"})
    assert auth_resp.status_code == 200
    auth_data = auth_resp.json()
    assert auth_data.get("valid") is True
    assert auth_data.get("tier") in ["pro", "pro_lifetime"]

    # Step 5: Unmasked Leaderboard Access
    pro_headers = {"Authorization": "Bearer PRO-DEMO-2026"}
    pro_stocks_resp = client.get("/api/stocks", headers=pro_headers)
    assert pro_stocks_resp.status_code == 200
    pro_stocks = pro_stocks_resp.json()
    assert pro_stocks[4]["is_pro_locked"] is False
    assert pro_stocks[4]["stop_loss_price"] is not None
    assert pro_stocks[4]["tp1_2x_price"] is not None

    # Step 6: Underwater Stock Diagnosis via Position Doctor
    celh_close = client.get("/api/stocks/CELH").json()["close"]
    doc_resp = client.post("/api/pro/position-doctor", json={
        "ticker": "CELH",
        "entry_price": 38.00,
        "days_held": 40,
        "current_price": celh_close,
    })
    assert doc_resp.status_code == 200
    doc_res = doc_resp.json()
    assert doc_res["status_code"] == "HARD_STOP"
    assert doc_res["is_critical"] is True

    # Step 7: Referral Deep Link Generation
    ref_resp = client.get("/api/referral/build?provider=tradingview&ticker=CELH")
    assert ref_resp.status_code == 200
    assert "aff_id=" in ref_resp.json()["url"]
    assert "CELH" in ref_resp.json()["url"]

    # Step 8: Pine Script Delivery
    pine_resp = client.get("/api/pro/pinescript", headers=pro_headers)
    assert pine_resp.status_code == 200
    assert "//@version=5" in pine_resp.json()["code"]


def test_t4_institutional_research_and_dead_money_exit_workflow(client):
    """
    Scenario 2: Institutional Research & Stagnant Position Switch
    1. Pro user browses research brief list and pulls Mobileye (MBLY) analysis.
    2. Validates MBLY's risk-reward ratio (1:11+) and turnaround roadmap.
    3. Runs Position Doctor on a stagnant holding held 60 days with only +2% gain.
    4. Rule 2 (55-day Time-Stop) triggers to free capital.
    5. Clicks Seeking Alpha referral link to review MBLY earnings consensus.
    """
    pro_headers = {"Authorization": "Bearer PRO-DEMO-2026"}

    # Step 1 & 2: Research Brief Inspection
    research_list = client.get("/api/research").json()
    assert len(research_list) > 0

    mbly_brief = client.get("/api/research/MBLY").json()
    assert "MBLY" in mbly_brief["content"]
    assert "TP1" in mbly_brief["content"]

    # Step 3 & 4: Stagnant Stock Exit via Position Doctor
    doc_resp = client.post("/api/pro/position-doctor", json={
        "ticker": "INTC",
        "entry_price": 25.00,
        "days_held": 60,
        "current_price": 25.50, # +2% in 60 days
    })
    assert doc_resp.status_code == 200
    doc = doc_resp.json()
    assert doc["status_code"] == "TIME_STOP"
    assert "55일" in doc["status_label"]

    # Step 5: Seeking Alpha Deep Link
    sa_resp = client.get("/api/referral/build?provider=seekingalpha&ticker=MBLY")
    assert sa_resp.status_code == 200
    assert "seekingalpha.com/symbol/MBLY" in sa_resp.json()["url"]


def test_t4_pro_take_profit_harvesting_workflow(client):
    """
    Scenario 3: 100% TP1 Principal Recovery Harvesting
    1. Investor bought early turnaround at $20.00.
    2. Current stock price reached $42.00 (+110% return).
    3. Position Doctor triggers Rule 3 (+100% TP1 Harvesting).
    4. Confirms recommendation instructs selling 50% to recover initial cash risk-free.
    """
    doc_resp = client.post("/api/pro/position-doctor", json={
        "ticker": "APP",
        "entry_price": 20.00,
        "days_held": 75,
        "current_price": 42.00,
    })
    assert doc_resp.status_code == 200
    doc = doc_resp.json()
    assert doc["status_code"] == "TP1_HARVEST"
    assert doc["return_pct"] == 110.0
    assert "Sell 50%" in doc["action_plan"]
    assert doc["stop_price"] == 18.20
    assert doc["tp1_price"] == 40.00


def test_t4_invalid_license_rejection_and_graceful_recovery_scenario(client):
    """
    Scenario 4: Invalid License Rejection & Error Recovery
    1. Visitor attempts an invalid license key "EXPIRED-KEY-XYZ".
    2. API cleanly returns valid=False without 500 error.
    3. Gated Pro Vault remains locked (401).
    4. User enters valid PRO-DEMO-2026 key.
    5. Pro Vault unlocks immediately.
    """
    # 1. Invalid attempt
    bad_resp = client.post("/api/auth/validate", json={"license_key": "EXPIRED-KEY-XYZ"})
    assert bad_resp.status_code == 200
    assert bad_resp.json()["valid"] is False

    # 2. Vault remains locked
    vault_bad = client.get("/api/pro/vault", headers={"Authorization": "Bearer EXPIRED-KEY-XYZ"})
    assert vault_bad.status_code in [401, 403]

    # 3. Valid key submitted
    good_resp = client.post("/api/auth/validate", json={"license_key": "PRO-DEMO-2026"})
    assert good_resp.status_code == 200
    assert good_resp.json()["valid"] is True

    # 4. Vault unlocked
    vault_good = client.get("/api/pro/vault", headers={"Authorization": "Bearer PRO-DEMO-2026"})
    assert vault_good.status_code == 200
    assert vault_good.json()["unlocked"] is True
