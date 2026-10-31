"""
backend/app/api/backtest.py - Empirical backtest API routes
"""
from typing import List, Optional, Any, Dict
from fastapi import APIRouter, Query

from backend.app.services.quant_engine import quant_engine

router = APIRouter()


@router.get("", response_model=Dict[str, Any])
@router.get("/", response_model=Dict[str, Any], include_in_schema=False)
@router.get("/summary", response_model=Dict[str, Any])
def get_backtest_summary() -> Dict[str, Any]:
    """
    Returns 26.8-year empirical backtest summary, including:
    - 5 benchmark comparison strategies
    - Annual performance records (2000-2026)
    - Headline KPIs (203.87x multiple, 21.97% CAGR, 55.24% 2x hit rate)
    """
    return quant_engine.backtest_data or {}


@router.get("/trades")
def get_backtest_trades(
    ticker: Optional[str] = Query(None, description="Filter trades by ticker symbol"),
    limit: Optional[int] = Query(None, ge=1, le=500, description="Limit trade log entries"),
) -> List[Dict[str, Any]]:
    """
    Returns historical closed trade log records (84 empirical simulation trades).
    """
    trades = quant_engine.trade_logs
    if ticker:
        t_clean = ticker.strip().upper()
        trades = [t for t in trades if t.get("ticker", "").upper() == t_clean]

    if limit is not None and limit > 0:
        trades = trades[:limit]

    return trades
