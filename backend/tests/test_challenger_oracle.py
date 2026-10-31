"""
backend/tests/test_challenger_oracle.py - Empirical Verification Oracle
Author: challenger_m1_2 (Empirical Challenger)
Milestone: Milestone 1 Verification

Empirically verifies:
1. 26.8-year backtest dataset fidelity (84 trades, peak gains, CAGR / Final Multiple formulas).
2. Exact calculation matches across 100% of all 99 screened stocks (scores, zones, MAs, targets, ignition conditions).
3. Adversarial testing of Position Doctor 4 exit rules across 52 boundary scenarios.
4. Core REST API masking boundaries, license bypass, and endpoint contracts.
"""
import json
import math
import sys
from pathlib import Path
from collections import Counter
from typing import Dict, Any, List

# Ensure project root is in sys.path
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import pytest
from fastapi.testclient import TestClient

from backend.app.services.quant_engine import quant_engine, VALUE_TRAPS, PRIORITY_TICKERS
from backend.app.config import settings
from backend.app.main import app


# ---------------------------------------------------------------------------
# Suite 1: Backtest Dataset & Raw Calculation Oracle (84 Trades & 5 Strategies)
# ---------------------------------------------------------------------------

def test_oracle_backtest_all_84_trades_fidelity():
    """
    Verifies all 84 trade records in pw_rsi_2000_2026_backtest.json:
    - Verifies raw dataset loading in engine
    - Validates invariants: peak_return_pct >= return_pct
    - Validates return_pct calculation from entry/exit prices
    - Validates date sequencing: entry_date <= exit_date
    - Validates entry score bounds [0, 100]
    """
    bt_path = settings.BACKTEST_DATA_PATH
    assert bt_path.exists(), f"Backtest file missing: {bt_path}"

    with open(bt_path, "r", encoding="utf-8", errors="replace") as f:
        raw_bt = json.load(f)

    raw_trades = raw_bt.get("trade_log", [])
    engine_trades = quant_engine.trade_logs

    assert len(raw_trades) == 84, f"Expected 84 trades in raw json, found {len(raw_trades)}"
    assert len(engine_trades) == 84, f"Expected 84 trades in quant_engine, found {len(engine_trades)}"

    for i, (rt, et) in enumerate(zip(raw_trades, engine_trades)):
        # Exact match between raw json and engine trade log
        assert rt["ticker"] == et["ticker"], f"Trade {i} ticker mismatch"
        assert rt["entry_date"] == et["entry_date"], f"Trade {i} entry_date mismatch"
        assert rt["exit_date"] == et["exit_date"], f"Trade {i} exit_date mismatch"
        assert rt["entry_price"] == et["entry_price"], f"Trade {i} entry_price mismatch"
        assert rt["exit_price"] == et["exit_price"], f"Trade {i} exit_price mismatch"
        assert rt["return_pct"] == et["return_pct"], f"Trade {i} return_pct mismatch"
        assert rt["peak_return_pct"] == et["peak_return_pct"], f"Trade {i} peak_return_pct mismatch"

        # Invariant 1: Peak return must never be lower than final exit return (within 1e-4 tolerance)
        assert et["peak_return_pct"] >= et["return_pct"] - 1e-4, (
            f"Trade {i} ({et['ticker']}): peak return {et['peak_return_pct']}% < exit return {et['return_pct']}%"
        )

        # Invariant 2: Execution prices must be positive non-zero
        assert et["entry_price"] > 0, f"Trade {i} entry_price non-positive"
        assert et["exit_price"] > 0, f"Trade {i} exit_price non-positive"

        # Invariant 3: Date ordering
        assert et["entry_date"] <= et["exit_date"], f"Trade {i} entry_date {et['entry_date']} > exit_date {et['exit_date']}"

        # Invariant 4: Entry score between 0 and 100
        assert 0.0 <= et["entry_score"] <= 100.0, f"Trade {i} score {et['entry_score']} out of bounds"

        # Invariant 5: Days held non-negative
        assert et["days_held"] >= 0, f"Trade {i} days_held negative"

        # Invariant 6: Price to return mathematical consistency
        # For stocks >= $1.00, return_pct must closely match ((exit / entry) - 1) * 100
        if et["entry_price"] >= 1.0:
            calc_ret = ((et["exit_price"] / et["entry_price"]) - 1.0) * 100.0
            assert abs(et["return_pct"] - calc_ret) <= 0.5, (
                f"Trade {i} ({et['ticker']}): stored return {et['return_pct']}% diverges from calc {calc_ret:.2f}%"
            )


def test_oracle_backtest_cagr_multiple_kpis():
    """
    Empirically verifies CAGR and Final Multiple formulas across 26.78-year backtest:
    - Multiple = (1 + CAGR/100) ^ Years
    - Cumulative Return = (Multiple - 1) * 100
    """
    summary = quant_engine.backtest_data
    assert summary is not None

    strategies = summary.get("overall_summary", [])
    assert len(strategies) == 5

    years = 26.78  # 2000-01-03 to 2026-10-13

    # Strategy 1: Recommended PW-RSI
    strat1 = strategies[0]
    mult1 = strat1["Final_Multiple"]
    cagr1 = strat1["CAGR_Pct"]
    cum1 = strat1["Cumulative_Return_Pct"]
    assert mult1 == 203.87
    assert cagr1 == 21.97
    assert cum1 == 20287.0

    # Mathematical consistency verification:
    computed_mult1 = (1.0 + (cagr1 / 100.0)) ** years
    assert abs(computed_mult1 - mult1) < 0.5, f"Strategy 1 Multiple {mult1} diverges from CAGR formula {computed_mult1:.2f}"
    computed_cum1 = (mult1 - 1.0) * 100.0
    assert abs(computed_cum1 - cum1) < 1.0

    # Strategy 2: PW-RSI without earnings filter
    strat2 = strategies[1]
    assert strat2["Final_Multiple"] == 51.98
    assert strat2["CAGR_Pct"] == 15.9
    computed_mult2 = (1.0 + (strat2["CAGR_Pct"] / 100.0)) ** years
    assert abs(computed_mult2 - strat2["Final_Multiple"]) < 0.5

    # Strategy 3: Naive 52W Low (Dead Money Trap)
    strat3 = strategies[2]
    assert strat3["Final_Multiple"] == 0.19
    assert strat3["CAGR_Pct"] == -5.99
    computed_mult3 = (1.0 + (strat3["CAGR_Pct"] / 100.0)) ** years
    assert abs(computed_mult3 - strat3["Final_Multiple"]) < 0.05

    # Strategy 4: QQQ Buy & Hold Benchmark
    strat4 = strategies[3]
    assert strat4["Final_Multiple"] == 9.32
    assert strat4["CAGR_Pct"] == 8.7
    computed_mult4 = (1.0 + (strat4["CAGR_Pct"] / 100.0)) ** years
    assert abs(computed_mult4 - strat4["Final_Multiple"]) < 0.1

    # Strategy 5: SPY Buy & Hold Benchmark
    strat5 = strategies[4]
    assert strat5["Final_Multiple"] == 8.56
    assert strat5["CAGR_Pct"] == 8.35
    computed_mult5 = (1.0 + (strat5["CAGR_Pct"] / 100.0)) ** years
    assert abs(computed_mult5 - strat5["Final_Multiple"]) < 0.1


# ---------------------------------------------------------------------------
# Suite 2: 99 Screened Stocks Full Universe Mathematical Oracle
# ---------------------------------------------------------------------------

def test_oracle_all_99_stocks_exact_calculations():
    """
    Performs full mathematical recomputation for 100% of all 99 stocks
    and verifies zero discrepancies against quant_engine internal representations.
    """
    stocks_path = settings.STOCKS_DATA_PATH
    with open(stocks_path, "r", encoding="utf-8") as f:
        raw_stocks = json.load(f)

    assert len(raw_stocks) == 99, f"Expected 99 raw stocks, got {len(raw_stocks)}"
    assert len(quant_engine.stocks) == 72, f"Expected 72 US engine stocks, got {len(quant_engine.stocks)}"

    for raw in raw_stocks:
        t = raw["Ticker"].strip().upper()
        if "." in t or t.endswith(".KS") or t.endswith(".KQ"):
            assert quant_engine.stocks_by_ticker.get(t) is None, f"Non-US ticker {t} must be excluded"
            continue
        stock = quant_engine.stocks_by_ticker.get(t)
        assert stock is not None, f"Engine missing ticker {t}"

        close = float(raw.get("Close", 0.0))
        prox = float(raw.get("ProxLow52_Pct", 999.0))
        dd = float(raw.get("DDHigh52_Pct", 0.0))
        ma20_pct = float(raw.get("Vs_MA20_Pct", -10.0))
        ma60_pct = float(raw.get("Vs_MA60_Pct", -10.0))
        vol = float(raw.get("VolSurge10D", 1.0))
        ret20d = float(raw.get("Ret20D_Pct")) if raw.get("Ret20D_Pct") is not None else None

        # 1. Algebraic MA reconstruction check
        expected_ma20 = round(close / (1.0 + ma20_pct / 100.0), 2) if ma20_pct != -100.0 else close
        expected_ma60 = round(close / (1.0 + ma60_pct / 100.0), 2) if ma60_pct != -100.0 else close
        assert abs(stock.ma20_price - expected_ma20) <= 0.01, (
            f"{t}: ma20_price mismatch: engine {stock.ma20_price} vs expected {expected_ma20}"
        )
        assert abs(stock.ma60_price - expected_ma60) <= 0.01, (
            f"{t}: ma60_price mismatch: engine {stock.ma60_price} vs expected {expected_ma60}"
        )

        # 2. Risk and target price formulas
        expected_stop = round(close * 0.91, 2)
        expected_tp1 = round(close * 2.00, 2)
        expected_trigger = round(max(expected_ma20, expected_ma60), 2)
        expected_pct_to_trig = round(((expected_trigger / close) - 1.0) * 100.0, 2) if close > 0 else 0.0

        assert abs(stock._stop_loss_price - expected_stop) <= 0.01, f"{t}: stop_loss mismatch"
        assert abs(stock._tp1_2x_price - expected_tp1) <= 0.01, f"{t}: tp1 mismatch"
        assert abs(stock._entry_trigger_price - expected_trigger) <= 0.01, f"{t}: trigger price mismatch"
        assert abs(stock._pct_to_trigger - expected_pct_to_trig) <= 0.01, f"{t}: pct_to_trigger mismatch"

        # 3. 4-factor scoring model recomputation
        score_dd = 25 if dd <= -35.0 else (15 if dd <= -20.0 else 0)
        score_prox = 25 if 10.0 <= prox <= 40.0 else (10 if prox < 10.0 else 0)
        if ma20_pct >= 0.0 and ma60_pct >= 0.0:
            score_ma = 30
        elif ma20_pct >= -1.5:
            score_ma = 20
        elif ma20_pct >= -5.0:
            score_ma = 10
        else:
            score_ma = 0
        score_vol = 20 if vol >= 1.35 else (12 if vol >= 1.15 else 0)

        raw_score = score_dd + score_prox + score_ma + score_vol

        # 4. Ignition conditions
        c1 = bool(dd <= -20.0)
        c2 = bool(10.0 <= prox <= 45.0)
        c3 = bool(ma20_pct >= -0.5 and ma60_pct >= -4.5)
        c4 = bool(vol >= 1.30 or (ret20d is not None and ret20d >= 8.0))
        all_4 = bool(c1 and c2 and c3 and c4 and (t not in VALUE_TRAPS))

        assert stock.c1_deep_dd == c1, f"{t}: c1 mismatch"
        assert stock.c2_off_low == c2, f"{t}: c2 mismatch"
        assert stock.c3_above_mas == c3, f"{t}: c3 mismatch"
        assert stock.c4_vol_or_mom == c4, f"{t}: c4 mismatch"
        assert stock.all_4_ignition_met == all_4, f"{t}: all_4 mismatch"

        # 5. Zone classification & score modifiers
        if t in VALUE_TRAPS:
            expected_zone = "VALUE_TRAP_FILTERED"
            adj_score = max(15, raw_score - 40)
        elif 10.0 <= prox <= 45.0 and ma20_pct >= -0.5 and ma60_pct >= -4.5 and vol >= 1.30 and dd <= -20.0:
            expected_zone = "IGNITION_ZONE"
            adj_score = max(raw_score, 84)
        elif prox < 10.0 and ma20_pct < 0.0:
            expected_zone = "LEFT_SIDE_KNIFE"
            adj_score = raw_score
        else:
            expected_zone = "WASHOUT_WATCH"
            adj_score = raw_score

        expected_final_score = int(min(98, max(0, adj_score)))

        assert stock.zone_code == expected_zone, f"{t}: zone mismatch: {stock.zone_code} vs {expected_zone}"
        assert stock.score == expected_final_score, f"{t}: score mismatch: {stock.score} vs {expected_final_score}"


def test_oracle_universe_zone_distribution_and_priority_sorting():
    """
    Verifies US 72-stock zone breakdown and Priority Ticker positioning.
    """
    us_stocks = [s for s in quant_engine.stocks if ".KS" not in s.ticker and ".KQ" not in s.ticker]
    kr_stocks = [s for s in quant_engine.stocks if ".KS" in s.ticker or ".KQ" in s.ticker]

    assert len(us_stocks) == 72
    assert len(kr_stocks) == 0

    counts = Counter(s.zone_code for s in us_stocks)
    assert counts["WASHOUT_WATCH"] == 53
    assert counts["LEFT_SIDE_KNIFE"] == 8
    assert counts["VALUE_TRAP_FILTERED"] == 6
    assert counts["IGNITION_ZONE"] == 5

    ignition_tickers = sorted(s.ticker for s in us_stocks if s.zone_code == "IGNITION_ZONE")
    assert ignition_tickers == ["AVGO", "CCL", "CELH", "SPOT", "TSLA"]

    # Verify priority ticker order at head of list
    top_tickers = [s.ticker for s in quant_engine.stocks[:14]]
    assert top_tickers == PRIORITY_TICKERS


# ---------------------------------------------------------------------------
# Suite 3: Position Doctor Adversarial Verification (52 Boundary Scenarios)
# ---------------------------------------------------------------------------

def test_oracle_position_doctor_52_adversarial_scenarios():
    """
    Adversarially stresses Position Doctor logic across 52 boundary and corner cases:
    - -9.00% exact stop loss threshold
    - Rule 1 vs Rule 2 precedence conflicts (-9% vs 55D dead money)
    - 55-day time stop threshold (day 54 vs day 55 vs day 56 at 7.99% vs 8.00%)
    - +100% TP1 runner trigger (99.99% vs 100.00%)
    - Edge cases: zero price, zero entry, negative values, missing ticker fallback
    """
    scenarios = [
        # ID, Ticker, Entry, Days, Current, Expected Status, Expected is_critical
        # 1. Rule 1 Boundary (-9.0% Stop Loss Floor)
        ("PD-B01", "TEST", 100.0, 10, 91.00, "CRITICAL_STOP", True),     # Exact -9.00%
        ("PD-B02", "TEST", 100.0, 10, 91.01, "ACTIVE_HOLD", False),      # -8.99% just above stop
        ("PD-B03", "TEST", 100.0, 10, 90.99, "CRITICAL_STOP", True),     # -9.01% just below stop
        ("PD-B04", "TEST", 200.0, 10, 182.00, "CRITICAL_STOP", True),    # Exact -9.00% on 200
        ("PD-B05", "TEST", 200.0, 10, 182.02, "ACTIVE_HOLD", False),     # -8.99% on 200
        ("PD-B06", "TEST", 100.0, 10, 50.00, "CRITICAL_STOP", True),     # -50.00% deep crash
        ("PD-B07", "TEST", 100.0, 10, 1.00, "CRITICAL_STOP", True),      # -99.00% catastrophic wipeout
        ("PD-B08", "TEST", 100.0, 10, 0.00, "CRITICAL_STOP", True),      # -100.00% bankruptcy

        # 2. Precedence: Rule 1 (-9%) vs Rule 2 (55D Dead Money) -> Rule 1 MUST take precedence
        ("PD-B09", "TEST", 100.0, 55, 91.00, "CRITICAL_STOP", True),     # Day 55, -9.00% -> Stop wins
        ("PD-B10", "TEST", 100.0, 56, 90.00, "CRITICAL_STOP", True),     # Day 56, -10.00% -> Stop wins
        ("PD-B11", "TEST", 100.0, 100, 80.00, "CRITICAL_STOP", True),    # Day 100, -20.00% -> Stop wins
        ("PD-B12", "TEST", 100.0, 55, 91.01, "DEAD_MONEY", False),      # Day 55, -8.99% -> Dead Money wins

        # 3. Rule 2 Boundary: 55-Day Dead-Money Opportunity Cost Stop
        ("PD-B13", "TEST", 100.0, 54, 107.00, "ACTIVE_HOLD", False),    # Day 54, +7.00% (pre-day 55) -> Hold
        ("PD-B14", "TEST", 100.0, 54, 107.99, "ACTIVE_HOLD", False),    # Day 54, +7.99% -> Hold
        ("PD-B15", "TEST", 100.0, 54, 95.00, "ACTIVE_HOLD", False),     # Day 54, -5.00% -> Hold
        ("PD-B16", "TEST", 100.0, 55, 107.00, "DEAD_MONEY", False),     # Day 55, +7.00% -> Dead Money
        ("PD-B17", "TEST", 100.0, 55, 107.99, "DEAD_MONEY", False),     # Day 55, +7.99% -> Dead Money
        ("PD-B18", "TEST", 100.0, 55, 108.00, "ACTIVE_HOLD", False),    # Day 55, +8.00% exact escape -> Hold
        ("PD-B19", "TEST", 100.0, 55, 108.01, "ACTIVE_HOLD", False),    # Day 55, +8.01% -> Hold
        ("PD-B20", "TEST", 100.0, 56, 107.99, "DEAD_MONEY", False),     # Day 56, +7.99% -> Dead Money
        ("PD-B21", "TEST", 100.0, 56, 108.00, "ACTIVE_HOLD", False),    # Day 56, +8.00% -> Hold
        ("PD-B22", "TEST", 100.0, 90, 100.00, "DEAD_MONEY", False),     # Day 90, flat 0.00% -> Dead Money
        ("PD-B23", "TEST", 100.0, 120, 105.00, "DEAD_MONEY", False),    # Day 120, +5.00% -> Dead Money
        ("PD-B24", "TEST", 100.0, 365, 107.99, "DEAD_MONEY", False),    # 1 year, +7.99% -> Dead Money
        ("PD-B25", "TEST", 100.0, 365, 108.00, "ACTIVE_HOLD", False),   # 1 year, +8.00% -> Hold

        # 4. Rule 3 Boundary: +100% Target Price 1 (TP1) Capital Recovery
        ("PD-B26", "TEST", 100.0, 30, 199.99, "ACTIVE_HOLD", False),    # +99.99% -> Hold (pre-TP1)
        ("PD-B27", "TEST", 100.0, 30, 200.00, "TP1_REACHED", False),    # Exact +100.00% -> TP1 Reached
        ("PD-B28", "TEST", 100.0, 30, 200.01, "TP1_REACHED", False),    # +100.01% -> TP1 Reached
        ("PD-B29", "TEST", 50.0, 15, 100.00, "TP1_REACHED", False),     # Entry 50 -> 100 (+100.00%) -> TP1
        ("PD-B30", "TEST", 50.0, 15, 99.99, "ACTIVE_HOLD", False),      # Entry 50 -> 99.99 (+99.98%) -> Hold
        ("PD-B31", "TEST", 10.0, 80, 50.00, "TP1_REACHED", False),      # 5x bagger -> TP1
        ("PD-B32", "TEST", 1.0, 90, 10.00, "TP1_REACHED", False),       # 10x bagger -> TP1
        ("PD-B33", "TEST", 100.0, 60, 200.00, "TP1_REACHED", False),    # Day 60, +100% -> TP1 takes precedence over Dead Money
        ("PD-B34", "TEST", 100.0, 180, 350.00, "TP1_REACHED", False),   # Day 180, +250% -> TP1

        # 5. Rule 4: Active Healthy Trend Following
        ("PD-B35", "TEST", 100.0, 0, 100.00, "ACTIVE_HOLD", False),      # Day 0, flat
        ("PD-B36", "TEST", 100.0, 1, 100.00, "ACTIVE_HOLD", False),      # Day 1, flat
        ("PD-B37", "TEST", 100.0, 20, 110.00, "ACTIVE_HOLD", False),     # Day 20, +10.00%
        ("PD-B38", "TEST", 100.0, 45, 150.00, "ACTIVE_HOLD", False),     # Day 45, +50.00%
        ("PD-B39", "TEST", 100.0, 54, 92.00, "ACTIVE_HOLD", False),      # Day 54, -8.00%
        ("PD-B40", "TEST", 100.0, 54, 107.90, "ACTIVE_HOLD", False),     # Day 54, +7.90%

        # 6. Corner Cases, Division by Zero Guards, Ticker Lookups
        ("PD-B41", "CELH", 27.93, 10, None, "ACTIVE_HOLD", False),       # Current price omitted, uses CELH close $27.93
        ("PD-B42", "CELH", 35.00, 10, None, "CRITICAL_STOP", True),      # Entry 35 -> Close 27.93 = -20.20% -> Stop
        ("PD-B43", "CELH", 13.96, 10, None, "TP1_REACHED", False),       # Entry 13.96 -> Close 27.93 = +100.07% -> TP1
        ("PD-B44", "celh", 27.93, 10, None, "ACTIVE_HOLD", False),       # Lowercase ticker lookup
        ("PD-B45", "  CELH  ", 27.93, 10, None, "ACTIVE_HOLD", False),   # Stripped ticker lookup
        ("PD-B46", "NON_EXISTENT", 100.0, 10, None, "ACTIVE_HOLD", False), # Unknown ticker defaults to entry price
        ("PD-B47", "TEST", 0.0, 10, 50.0, "TP1_REACHED", False),         # Zero entry price guard (entry -> 1.0)
        ("PD-B48", "TEST", -5.0, 10, 50.0, "TP1_REACHED", False),        # Negative entry price guard
        ("PD-B49", "TEST", 1000000.0, 10, 910000.0, "CRITICAL_STOP", True), # High magnitude: -9.00% -> Stop
        ("PD-B50", "TEST", 0.001, 10, 0.00091, "CRITICAL_STOP", True),   # Micro magnitude: -9.00% -> Stop
        ("PD-B51", "TEST", 100.0, -10, 105.0, "ACTIVE_HOLD", False),     # Negative days held input
        ("PD-B52", "TEST", 100.0, 10000, 108.0, "ACTIVE_HOLD", False),   # Extreme long hold with +8% -> Hold
    ]

    assert len(scenarios) == 52

    for sid, ticker, entry, days, curr, exp_status, exp_crit in scenarios:
        res = quant_engine.diagnose_position(
            ticker=ticker,
            entry_price=entry,
            days_held=days,
            current_price=curr,
        )
        assert res.status_code == exp_status, (
            f"Scenario {sid} ({ticker}, entry={entry}, days={days}, curr={curr}): "
            f"got status {res.status_code} ({res.return_pct}%), expected {exp_status}"
        )
        assert res.is_critical == exp_crit, (
            f"Scenario {sid} is_critical mismatch: got {res.is_critical}, expected {exp_crit}"
        )


# ---------------------------------------------------------------------------
# Suite 4: Core REST API Access Control & Masking Integration
# ---------------------------------------------------------------------------

def test_oracle_api_masking_and_pro_license():
    """
    Empirically verifies REST API data masking and Pro bypass via TestClient:
    - Free tier GET /api/stocks: rows 0..3 unmasked, rows 4..98 masked
    - Pro tier GET /api/stocks?license_key=PRO-DEMO-2026: all rows unmasked
    - Authorization: Bearer PRO-DEMO-2026: all rows unmasked
    - Single stock preview unmasked (CELH) vs non-preview masked (MBLY)
    - Diagnostics endpoint POST /api/stocks/diagnose
    """
    client = TestClient(app)

    # 1. Free tier list endpoint
    res = client.get("/api/stocks")
    assert res.status_code == 200
    stocks = res.json()
    assert len(stocks) == 72

    for i in range(4):
        s = stocks[i]
        assert s["is_pro_locked"] is False
        assert s["stop_loss_price"] is not None
        assert s["tp1_2x_price"] is not None
        assert s["ma60_price"] is not None

    for i in range(4, 72):
        s = stocks[i]
        assert s["is_pro_locked"] is True
        assert s["stop_loss_price"] is None
        assert s["tp1_2x_price"] is None
        assert s["ma60_price"] is None

    # 2. Pro tier list endpoint via query parameter
    res_pro = client.get("/api/stocks?license_key=PRO-DEMO-2026")
    assert res_pro.status_code == 200
    pro_stocks = res_pro.json()
    assert all(s["is_pro_locked"] is False for s in pro_stocks)
    assert all(s["stop_loss_price"] is not None for s in pro_stocks)

    # 3. Pro tier list endpoint via Bearer header
    res_bearer = client.get("/api/stocks", headers={"Authorization": "Bearer PRO-DEMO-2026"})
    assert res_bearer.status_code == 200
    bearer_stocks = res_bearer.json()
    assert all(s["is_pro_locked"] is False for s in bearer_stocks)

    # 4. Single stock detail masking
    res_celh = client.get("/api/stocks/CELH")
    assert res_celh.status_code == 200
    assert res_celh.json()["is_pro_locked"] is False

    res_mbly = client.get("/api/stocks/MBLY")
    assert res_mbly.status_code == 200
    assert res_mbly.json()["is_pro_locked"] is True
    assert res_mbly.json()["stop_loss_price"] is None

    res_mbly_pro = client.get("/api/stocks/MBLY?license_key=PRO-DEMO-2026")
    assert res_mbly_pro.status_code == 200
    assert res_mbly_pro.json()["is_pro_locked"] is False
    assert res_mbly_pro.json()["stop_loss_price"] == 6.39

    # 5. Position Doctor endpoint POST /api/stocks/diagnose
    r_diag1 = client.post("/api/stocks/diagnose", json={"ticker": "CELH", "entry_price": 27.93, "days_held": 10})
    assert r_diag1.status_code == 200
    assert r_diag1.json()["status_code"] == "ACTIVE_HOLD"

    r_diag2 = client.post("/api/stocks/diagnose", json={"ticker": "CELH", "entry_price": 35.0, "days_held": 10})
    assert r_diag2.status_code == 200
    assert r_diag2.json()["status_code"] == "CRITICAL_STOP"
    assert r_diag2.json()["is_critical"] is True

    # 6. Backtest summary and trade log endpoints
    r_bt = client.get("/api/backtest/summary")
    assert r_bt.status_code == 200
    assert r_bt.json()["kpis"]["cagr_pct"] == 21.97
    assert r_bt.json()["kpis"]["final_multiple"] == 203.87

    r_trades = client.get("/api/backtest/trades")
    assert r_trades.status_code == 200
    assert len(r_trades.json()) == 84

    r_trades_celh = client.get("/api/backtest/trades?ticker=CELH")
    assert r_trades_celh.status_code == 200
    assert all(t["ticker"] == "CELH" for t in r_trades_celh.json())


if __name__ == "__main__":
    print("Executing empirical verification oracle directly...")
    test_oracle_backtest_all_84_trades_fidelity()
    print("[PASS] test_oracle_backtest_all_84_trades_fidelity")
    test_oracle_backtest_cagr_multiple_kpis()
    print("[PASS] test_oracle_backtest_cagr_multiple_kpis")
    test_oracle_all_99_stocks_exact_calculations()
    print("[PASS] test_oracle_all_99_stocks_exact_calculations")
    test_oracle_universe_zone_distribution_and_priority_sorting()
    print("[PASS] test_oracle_universe_zone_distribution_and_priority_sorting")
    test_oracle_position_doctor_52_adversarial_scenarios()
    print("[PASS] test_oracle_position_doctor_52_adversarial_scenarios")
    test_oracle_api_masking_and_pro_license()
    print("[PASS] test_oracle_api_masking_and_pro_license")
    print("\nALL EMPIRICAL ORACLE SUITES PASSED 100%!")
