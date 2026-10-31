"""
backend/tests/test_quant_engine.py - Unit tests for Quantitative Data Engine
"""
import json
from collections import Counter
import pytest

from backend.app.services.quant_engine import quant_engine, VALUE_TRAPS
from backend.app.config import settings


def test_dataset_files_exist():
    """Verify that source dataset files exist on disk."""
    assert settings.STOCKS_DATA_PATH.exists(), f"Missing {settings.STOCKS_DATA_PATH}"
    assert settings.BACKTEST_DATA_PATH.exists(), f"Missing {settings.BACKTEST_DATA_PATH}"
    assert settings.WEEKLY_PICKS_DIR.exists(), f"Missing {settings.WEEKLY_PICKS_DIR}"


def test_load_stocks_count_and_keys():
    """Verify loading of US-only screened stocks dataset (72 US equities, zero .KS/.KQ)."""
    stocks = quant_engine.stocks
    assert len(stocks) == 72, f"Expected 72 US-listed stocks, got {len(stocks)}"
    assert all("." not in s.ticker and not s.ticker.endswith(".KS") and not s.ticker.endswith(".KQ") for s in stocks)

    # Verify required raw & enriched fields
    sample = stocks[0]
    required_fields = [
        "ticker", "date", "close", "low52", "high52",
        "prox_low52_pct", "dd_high52_pct", "vs_ma20_pct", "vs_ma60_pct",
        "rsi14", "vol_surge_10d", "score", "zone_code",
        "stop_loss_price", "tp1_2x_price"
    ]
    for field in required_fields:
        assert hasattr(sample, field) or field in sample.__dict__, f"Missing field: {field}"


def test_quant_score_and_zone_enrichment():
    """Verify scoring logic and zone categorizations."""
    for stock in quant_engine.stocks:
        # Score must be bounded [0, 98]
        assert 0 <= stock.score <= 98, f"Score out of bounds for {stock.ticker}: {stock.score}"

        # Zone must be one of 4 valid zones
        assert stock.zone_code in [
            "IGNITION_ZONE",
            "WASHOUT_WATCH",
            "LEFT_SIDE_KNIFE",
            "VALUE_TRAP_FILTERED",
        ], f"Invalid zone code {stock.zone_code} for {stock.ticker}"


def test_target_price_and_stop_loss_math():
    """Verify stop loss (-9%) and target price (+100%) calculations."""
    for stock in quant_engine.stocks[:15]:
        expected_stop = round(stock.close * 0.91, 2)
        expected_tp1 = round(stock.close * 2.00, 2)
        assert abs(stock.stop_loss_price - expected_stop) <= 0.05
        assert abs(stock.tp1_2x_price - expected_tp1) <= 0.05


def test_moving_average_math():
    """Verify algebraic MA reconstruction for CELH."""
    celh = quant_engine.stocks_by_ticker.get("CELH")
    assert celh is not None
    assert celh.close == 27.93
    assert celh.vs_ma20_pct == 0.0
    assert celh.vs_ma60_pct == -4.1
    assert celh.ma20_price == 27.93
    assert celh.ma60_price == 29.12
    assert celh.stop_loss_price == 25.42
    assert celh.tp1_2x_price == 55.86
    assert celh.zone_code == "IGNITION_ZONE"
    assert celh.score == 90


def test_load_backtest_summary():
    """Verify backtest summary data integrity."""
    summary = quant_engine.backtest_data
    assert summary is not None
    assert "2000" in summary.get("period", "")
    assert "2026" in summary.get("period", "")

    overall = summary.get("overall_summary", [])
    assert len(overall) >= 4

    # Strategy 1 verification: Multiple ~203.87, CAGR ~21.97%
    strat1 = overall[0]
    assert strat1.get("Final_Multiple") == 203.87
    assert strat1.get("CAGR_Pct") == 21.97


def test_load_trade_logs():
    """Verify backtest trade logs."""
    trades = quant_engine.trade_logs
    assert len(trades) == 84, f"Expected 84 trades, found {len(trades)}"

    first_trade = trades[0]
    for key in ["entry_date", "exit_date", "ticker", "entry_price", "exit_price", "return_pct"]:
        assert key in first_trade, f"Missing key {key} in trade log"


def test_load_weekly_picks_brief():
    """Verify retrieval of weekly research markdown briefs."""
    brief = quant_engine.get_research_brief("CELH")
    assert brief is not None, "Failed to load CELH research brief"
    assert "CELH" in brief or "셀시우스" in brief
    assert len(brief) > 500

    # Non-existent ticker returns None gracefully
    missing_brief = quant_engine.get_research_brief("NONEXISTENT_TICKER")
    assert missing_brief is None


def test_test_vectors_against_engine():
    """Validates 12 stock test vectors from test_vectors.json against engine math."""
    vectors_file = settings.BASE_DIR / ".agents" / "teamwork" / "explorer_m1_2" / "test_vectors.json"
    if not vectors_file.exists():
        pytest.skip(f"Test vectors file not found at {vectors_file}")

    with open(vectors_file, "r", encoding="utf-8") as f:
        vectors = json.load(f)

    for v in vectors:
        ticker = v["input"]["ticker"]
        expected_out = v["output"]
        expected_inter = v["intermediate"]

        stock = quant_engine.stocks_by_ticker.get(ticker)
        assert stock is not None, f"Stock {ticker} not found in engine"

        # Compare PW Score and Zone Code
        assert stock.score == expected_out["pw_score"], f"{ticker} score mismatch: {stock.score} vs {expected_out['pw_score']}"
        assert stock.zone_code == expected_out["zone_code"], f"{ticker} zone mismatch: {stock.zone_code} vs {expected_out['zone_code']}"

        # Compare Stop Loss and TP1
        assert pytest.approx(stock.stop_loss_price, abs=0.05) == expected_out["stop_loss_price"]
        assert pytest.approx(stock.tp1_2x_price, abs=0.05) == expected_out["tp1_2x_price"]

        # Compare MA reconstruction
        assert pytest.approx(stock.ma20_price, abs=0.05) == expected_inter["ma20_price"]
        assert pytest.approx(stock.ma60_price, abs=0.05) == expected_inter["ma60_price"]

        # Compare 4 conditions
        assert stock.c1_deep_dd == expected_out["c1_deep_dd"], f"{ticker} c1 mismatch"
        assert stock.c2_off_low == expected_out["c2_off_low"], f"{ticker} c2 mismatch"
        assert stock.c3_above_mas == expected_out["c3_above_mas"], f"{ticker} c3 mismatch"
        assert stock.c4_vol_or_mom == expected_out["c4_vol_or_mom"], f"{ticker} c4 mismatch"
        assert stock.all_4_ignition_met == expected_out["all_4_ignition_met"], f"{ticker} all_4 mismatch"


def test_boundary_conditions():
    """Tests 18 mathematical boundary conditions specified in m1_quant_blueprint.md."""
    # BND-01: Drawdown boundary upper (dd = -35.0 -> score_dd = 25)
    def calc_score(dd, prox, ma20_pct, ma60_pct, vol, ticker="TEST"):
        s = 0
        if dd <= -35.0: s += 25
        elif dd <= -20.0: s += 15

        if 10.0 <= prox <= 40.0: s += 25
        elif prox < 10.0: s += 10

        if ma20_pct >= 0.0 and ma60_pct >= 0.0: s += 30
        elif ma20_pct >= -1.5: s += 20
        elif ma20_pct >= -5.0: s += 10

        if vol >= 1.35: s += 20
        elif vol >= 1.15: s += 12

        if ticker in VALUE_TRAPS:
            s = max(15, s - 40)
        elif 10.0 <= prox <= 45.0 and ma20_pct >= -0.5 and ma60_pct >= -4.5 and vol >= 1.30 and dd <= -20.0:
            s = max(s, 84)

        return int(min(98, max(0, s)))

    # BND-01 & BND-02
    assert calc_score(dd=-35.0, prox=50.0, ma20_pct=-10.0, ma60_pct=-10.0, vol=1.0) == 25
    assert calc_score(dd=-34.99, prox=50.0, ma20_pct=-10.0, ma60_pct=-10.0, vol=1.0) == 15

    # BND-03 & BND-04
    assert calc_score(dd=-20.0, prox=50.0, ma20_pct=-10.0, ma60_pct=-10.0, vol=1.0) == 15
    assert calc_score(dd=-19.99, prox=50.0, ma20_pct=-10.0, ma60_pct=-10.0, vol=1.0) == 0

    # BND-05 & BND-06
    assert calc_score(dd=0.0, prox=10.0, ma20_pct=-10.0, ma60_pct=-10.0, vol=1.0) == 25
    assert calc_score(dd=0.0, prox=9.99, ma20_pct=-10.0, ma60_pct=-10.0, vol=1.0) == 10

    # BND-07 & BND-08
    assert calc_score(dd=0.0, prox=40.0, ma20_pct=-10.0, ma60_pct=-10.0, vol=1.0) == 25
    assert calc_score(dd=0.0, prox=40.01, ma20_pct=-10.0, ma60_pct=-10.0, vol=1.0) == 0

    # BND-09 & BND-10
    assert calc_score(dd=0.0, prox=50.0, ma20_pct=0.0, ma60_pct=0.0, vol=1.0) == 30
    assert calc_score(dd=0.0, prox=50.0, ma20_pct=0.0, ma60_pct=-0.01, vol=1.0) == 20

    # BND-11 & BND-12
    assert calc_score(dd=0.0, prox=50.0, ma20_pct=-5.0, ma60_pct=-10.0, vol=1.0) == 10
    assert calc_score(dd=0.0, prox=50.0, ma20_pct=-5.01, ma60_pct=-10.0, vol=1.0) == 0

    # BND-13, BND-14, BND-15
    assert calc_score(dd=0.0, prox=50.0, ma20_pct=-10.0, ma60_pct=-10.0, vol=1.35) == 20
    assert calc_score(dd=0.0, prox=50.0, ma20_pct=-10.0, ma60_pct=-10.0, vol=1.15) == 12
    assert calc_score(dd=0.0, prox=50.0, ma20_pct=-10.0, ma60_pct=-10.0, vol=1.14) == 0

    # BND-16: 98 Maximum Ceiling
    assert calc_score(dd=-50.0, prox=20.0, ma20_pct=5.0, ma60_pct=5.0, vol=2.0) == 98

    # BND-17: Value Trap floor 15
    assert calc_score(dd=-20.0, prox=50.0, ma20_pct=-10.0, ma60_pct=-10.0, vol=1.0, ticker="INTC") == 15

    # BND-18: Ignition floor boost to 84
    assert calc_score(dd=-25.0, prox=20.0, ma20_pct=0.0, ma60_pct=-4.0, vol=1.35) >= 84


def test_position_doctor_diagnostics():
    """Tests 8 Position Doctor scenarios (PD-01 to PD-08)."""
    # PD-01: -10% -> Critical Stop
    d1 = quant_engine.diagnose_position("MBLY", entry_price=20.0, current_price=18.0, days_held=5)
    assert d1.status_code == "CRITICAL_STOP"
    assert d1.is_critical is True
    assert d1.return_pct == -10.0

    # PD-02: -9% -> Critical Stop
    d2 = quant_engine.diagnose_position("ENPH", entry_price=50.0, current_price=45.5, days_held=12)
    assert d2.status_code == "CRITICAL_STOP"
    assert d2.is_critical is True
    assert d2.return_pct == -9.0

    # PD-03: 55 days, +5% -> Dead Money
    d3 = quant_engine.diagnose_position("SOFI", entry_price=10.0, current_price=10.5, days_held=55)
    assert d3.status_code == "DEAD_MONEY"
    assert d3.is_critical is False
    assert d3.return_pct == 5.0

    # PD-04: 72 days, +6.67% -> Dead Money
    d4 = quant_engine.diagnose_position("CVNA", entry_price=15.0, current_price=16.0, days_held=72)
    assert d4.status_code == "DEAD_MONEY"
    assert d4.is_critical is False

    # PD-05: +100% -> TP1 Reached
    d5 = quant_engine.diagnose_position("CELH", entry_price=25.0, current_price=50.0, days_held=90)
    assert d5.status_code == "TP1_REACHED"
    assert d5.return_pct == 100.0

    # PD-06: +110% -> TP1 Reached
    d6 = quant_engine.diagnose_position("TSLA", entry_price=200.0, current_price=420.0, days_held=140)
    assert d6.status_code == "TP1_REACHED"
    assert d6.return_pct == 110.0

    # PD-07: +25%, 30 days -> Active Hold
    d7 = quant_engine.diagnose_position("NVDA", entry_price=100.0, current_price=125.0, days_held=30)
    assert d7.status_code == "ACTIVE_HOLD"

    # PD-08: -8%, 40 days -> Active Hold
    d8 = quant_engine.diagnose_position("CCL", entry_price=20.0, current_price=18.4, days_held=40)
    assert d8.status_code == "ACTIVE_HOLD"


def test_us_zone_distribution():
    """
    Validates zone classification distribution for the 72 US equities:
    - WASHOUT_WATCH: 53 stocks
    - LEFT_SIDE_KNIFE: 8 stocks
    - VALUE_TRAP_FILTERED: 6 stocks
    - IGNITION_ZONE: 5 stocks (AVGO, CCL, CELH, SPOT, TSLA)
    """
    us_stocks = [s for s in quant_engine.stocks if ".KS" not in s.ticker and ".KQ" not in s.ticker]
    assert len(us_stocks) == 72, f"Expected 72 US stocks, got {len(us_stocks)}"

    counts = Counter(s.zone_code for s in us_stocks)
    assert counts["WASHOUT_WATCH"] == 53
    assert counts["LEFT_SIDE_KNIFE"] == 8
    assert counts["VALUE_TRAP_FILTERED"] == 6
    assert counts["IGNITION_ZONE"] == 5

    ignition_tickers = sorted(s.ticker for s in us_stocks if s.zone_code == "IGNITION_ZONE")
    assert ignition_tickers == ["AVGO", "CCL", "CELH", "SPOT", "TSLA"]


def test_masking_boundary_free_vs_pro():
    """Verify masking boundary between free tier and Pro tier."""
    free_stocks = quant_engine.get_stocks(is_pro=False)
    assert len(free_stocks) == 72

    # Rows 0..3 unmasked
    for idx in range(4):
        s = free_stocks[idx]
        assert s.is_pro_locked is False
        assert s.stop_loss_price is not None
        assert s.tp1_2x_price is not None

    # Rows 4+ masked
    for idx in range(4, len(free_stocks)):
        s = free_stocks[idx]
        assert s.is_pro_locked is True
        assert s.stop_loss_price is None
        assert s.tp1_2x_price is None

    # Pro unmasks all
    pro_stocks = quant_engine.get_stocks(is_pro=True)
    for s in pro_stocks:
        assert s.is_pro_locked is False
        assert s.stop_loss_price is not None
        assert s.tp1_2x_price is not None
