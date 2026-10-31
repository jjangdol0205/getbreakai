"""
backend/app/api/research.py - Turnaround research briefs API routes
"""
from typing import List
from fastapi import APIRouter, Depends, HTTPException

from backend.app.api.deps import get_is_pro
from backend.app.models.research import ResearchBriefDetail, ResearchBriefSummary
from backend.app.services.quant_engine import quant_engine

router = APIRouter()


@router.get("", response_model=List[ResearchBriefSummary])
@router.get("/", response_model=List[ResearchBriefSummary], include_in_schema=False)
def list_research_briefs(
    is_pro: bool = Depends(get_is_pro),
):
    """
    Returns available turnaround research briefs summaries.
    """
    return quant_engine.list_research_briefs(is_pro=is_pro)


@router.get("/{ticker}", response_model=ResearchBriefDetail)
def get_research_brief_detail(
    ticker: str,
    is_pro: bool = Depends(get_is_pro),
):
    """
    Returns turnaround research brief details for a given ticker.
    Preview tickers (e.g. CELH) or Pro subscribers receive full report.
    Free tier requesting non-preview tickers receive preview teaser.
    """
    detail = quant_engine.get_research_brief_detail(ticker=ticker, is_pro=is_pro)
    if not detail:
        raise HTTPException(
            status_code=404,
            detail=f"No research brief found for ticker '{ticker}'",
        )
    return detail
