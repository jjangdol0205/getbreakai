"""
backend/app/api/referral.py - CPA Referral Monetization and Click Tracking API
"""
from typing import Optional, Dict, Any
from fastapi import APIRouter, HTTPException, Query, Response, status
from fastapi.responses import RedirectResponse

from backend.app.models.referral import ReferralConfig, ReferralBuildResponse
from backend.app.services.referral_service import referral_service

router = APIRouter()


@router.get("/config")
def get_referral_config():
    """
    Returns active affiliate IDs and source tags for partner networks.
    """
    return referral_service.get_config().model_dump()


@router.post("/config")
def update_referral_config(payload: ReferralConfig):
    """
    Updates affiliate partner tracking parameters.
    """
    updated = referral_service.update_config(payload)
    return {"status": "updated", "config": updated.model_dump(), **updated.model_dump()}


@router.get("/build", response_model=ReferralBuildResponse)
def build_referral_link(
    provider: Optional[str] = Query(None, description="Partner network (tradingview, seekingalpha, trendspider)"),
    ticker: Optional[str] = Query("SPY", description="Target US equity ticker"),
):
    """
    Builds dynamic affiliate deep link incorporating current referral credentials.
    """
    if not provider or not provider.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Referral provider cannot be empty",
        )

    prov = provider.strip().lower()
    try:
        url = referral_service.build_url(provider=prov, ticker=ticker)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )

    clean_ticker = (ticker or "SPY").strip().upper()
    return ReferralBuildResponse(
        provider=prov,
        ticker=clean_ticker,
        url=url,
    )


@router.get("/redirect/{provider}")
def redirect_referral(
    provider: str,
    ticker: Optional[str] = Query("SPY", description="Target US equity ticker"),
):
    """
    Tracks outbound referral click and performs HTTP 307 Temporary Redirect to partner destination.
    """
    prov = (provider or "").strip().lower()
    try:
        dest_url = referral_service.record_click(provider=prov, ticker=ticker)
    except (KeyError, ValueError):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Invalid referral provider: '{provider}'",
        )

    return RedirectResponse(url=dest_url, status_code=status.HTTP_307_TEMPORARY_REDIRECT)


@router.get("/stats")
@router.get("/clicks", include_in_schema=False)
def get_referral_stats() -> Dict[str, Any]:
    """
    Returns cumulative and per-network outbound referral click statistics.
    """
    return referral_service.get_stats()
