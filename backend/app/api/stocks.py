"""
backend/app/api/stocks.py - Screened stocks API routes
"""
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, Response

from backend.app.api.deps import get_is_pro
from backend.app.models.stock import StockResponse
from backend.app.models.backtest import PositionDoctorRequest, PositionDoctorResponse
from backend.app.services.quant_engine import quant_engine

router = APIRouter()


@router.get("", response_model=List[StockResponse])
@router.get("/", response_model=List[StockResponse], include_in_schema=False)
def get_screened_stocks(
    response: Response,
    zone: Optional[str] = Query(None, description="Filter by zone (e.g. IGNITION_ZONE, WASHOUT_WATCH)"),
    search: Optional[str] = Query(None, description="Search ticker or name substring"),
    query: Optional[str] = Query(None, description="Alias for search"),
    sort_by: Optional[str] = Query(None, description="Sort field (score, close, prox, dd, vol)"),
    order: str = Query("asc", description="Sort order: asc | desc"),
    limit: Optional[int] = Query(None, description="Limit results"),
    offset: Optional[int] = Query(0, description="Offset results"),
    is_pro: bool = Depends(get_is_pro),
):
    """
    Returns screened equities list.
    Free tier: preview tickers (CELH, CCL, TSLA, UPST) unmasked, non-preview tickers have target prices masked.
    Pro tier (license_key or Bearer token): all rows unmasked.
    """
    if offset is not None and offset < 0:
        raise HTTPException(status_code=400, detail="Offset cannot be negative")
    if limit is not None and limit < 0:
        raise HTTPException(status_code=400, detail="Limit cannot be negative")
    if limit == 0:
        response.headers["X-Total-Count"] = "0"
        response.headers["X-Pro-Unlocked"] = "true" if is_pro else "false"
        return []

    stocks = quant_engine.get_stocks(
        is_pro=is_pro,
        zone=zone,
        search=search,
        query=query,
        sort_by=sort_by,
        order=order,
        limit=limit,
        offset=offset,
    )
    response.headers["X-Total-Count"] = str(len(stocks))
    response.headers["X-Pro-Unlocked"] = "true" if is_pro else "false"
    return stocks


@router.post("/diagnose", response_model=PositionDoctorResponse)
def diagnose_stock_position(payload: PositionDoctorRequest):
    """
    Position Doctor diagnostic endpoint evaluating holdings against 4 exit rules.
    """
    return quant_engine.diagnose_position(
        ticker=payload.ticker,
        entry_price=payload.entry_price,
        days_held=payload.days_held,
        current_price=payload.current_price,
    )


@router.get("/{ticker}", response_model=StockResponse)
def get_stock_detail(
    ticker: str,
    is_pro: bool = Depends(get_is_pro),
):
    """
    Returns single stock details.
    Preview stocks (CELH, CCL, TSLA, UPST) are unmasked for all users.
    Other stocks require Pro authentication to unmask target prices.
    """
    stock = quant_engine.get_stock(ticker=ticker, is_pro=is_pro)
    if not stock:
        raise HTTPException(
            status_code=404,
            detail=f"Ticker '{ticker}' not found in screened universe",
        )
    return stock
