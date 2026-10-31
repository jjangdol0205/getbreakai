"""
backend/app/api/semi.py - FastAPI router for SemiFearGreed (CNN-style Semiconductor Fear & Greed Index & SMH/XLV Barbell Platform)
"""
from fastapi import APIRouter, Depends, Query
from fastapi.responses import FileResponse

from backend.app.api.deps import require_pro
from backend.app.config import settings
from backend.app.models.semi import (
    SemiOverviewResponse,
    SemiHistoryResponse,
    RebalanceRequest,
    RebalanceResponse,
    LumpSumRequest,
    LumpSumResponse,
)
from backend.app.services.semi_engine import semi_engine

router = APIRouter()


@router.get("/overview", response_model=SemiOverviewResponse)
def get_semi_overview():
    """
    Returns live/latest Semiconductor 7-Factor Fear & Greed Index overview,
    historical comparisons (Previous close, 1W, 1M, 1Y), 7-factor CNN breakdown,
    and SMH / XLV / QQQ ETF snapshots.
    """
    return semi_engine.get_overview()


@router.get("/history", response_model=SemiHistoryResponse)
def get_semi_history(
    range: str = Query(default="1Y", description="Range code: 3M, 6M, 1Y, 3Y, 5Y, 10Y, ALL"),
):
    """
    Returns historical time-series for the Semiconductor Fear & Greed Index,
    normalized $10,000 growth comparison (SMH 70% : XLV 30% vs QQQ 100%),
    and 26-year empirical era performance summary table.
    """
    return semi_engine.get_history(range_code=range)


@router.post("/rebalance", response_model=RebalanceResponse)
def post_semi_rebalance(payload: RebalanceRequest):
    """
    Calculates exact $SMH and $XLV target allocations, share counts, rebalancing deltas,
    and South Korean 2,500,000 KRW annual foreign equity capital gains tax deduction optimization.
    """
    return semi_engine.calculate_rebalance(payload)


@router.post("/lump-sum", response_model=LumpSumResponse)
def post_semi_lump_sum(payload: LumpSumRequest):
    """
    Calculates 3-stage lump-sum entry deployment tranches based on the active or simulated
    Semiconductor Fear & Greed Index score.
    """
    return semi_engine.calculate_lump_sum(payload)


@router.get("/pro/csv")
def download_semi_pro_csv(_: bool = Depends(require_pro)):
    """
    Delivers full 26-year (2000-2026) daily Semiconductor Fear & Greed Index CSV dataset to Pro subscribers.
    """
    return FileResponse(
        path=str(settings.SEMI_HISTORY_CSV_PATH),
        media_type="text/csv",
        filename="smh_xlv_fear_greed_history_2000_2026.csv",
    )
