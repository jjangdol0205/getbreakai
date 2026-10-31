"""
backend/tests/conftest.py - Shared fixtures for unit and integration tests
"""
import sys
from pathlib import Path
import pytest
from fastapi.testclient import TestClient

# Ensure workspace root is in sys.path
BASE_DIR = Path(__file__).resolve().parent.parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from backend.app.main import app
from backend.app.services.quant_engine import quant_engine


@pytest.fixture(scope="session", autouse=True)
def setup_quant_engine():
    """Ensure quant engine is loaded once for all test sessions."""
    quant_engine.initialize()
    return quant_engine


@pytest.fixture(scope="session")
def client():
    """FastAPI TestClient fixture."""
    with TestClient(app) as test_client:
        yield test_client


@pytest.fixture
def sample_stock_raw():
    """Raw stock fixture mimicking all_100_stocks_screened.json entry."""
    return {
        "Ticker": "CELH",
        "Date": "2026-10-14",
        "Close": 27.93,
        "Low52": 23.56,
        "High52": 66.74,
        "ProxLow52_Pct": 18.5,
        "DDHigh52_Pct": -58.2,
        "Vs_MA20_Pct": 0.0,
        "Vs_MA60_Pct": -4.1,
        "Vs_MA200_Pct": -15.0,
        "RSI14": 47.4,
        "VolSurge10D": 1.45,
        "Ret5D_Pct": 1.1,
        "Ret20D_Pct": 1.1,
    }
