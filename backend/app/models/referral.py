"""
backend/app/models/referral.py - CPA Referral Affiliate and Outbound Tracking schemas
"""
from typing import Optional
from pydantic import BaseModel, Field


class ReferralConfig(BaseModel):
    tradingview_aff_id: str = Field("rightsidealpha", description="TradingView partner affiliate ID")
    seekingalpha_source: str = Field("affiliate_rightside", description="Seeking Alpha tracking source tag")
    trendspider_aff_id: str = Field("rightside", description="TrendSpider partner tracking ID")


class ReferralClickStats(BaseModel):
    total: int = Field(0, description="Cumulative outbound click count across all networks")
    tradingview: int = Field(0, description="TradingView click count")
    seekingalpha: int = Field(0, description="Seeking Alpha click count")
    trendspider: int = Field(0, description="TrendSpider click count")
    last_clicked_at: Optional[str] = Field(None, description="ISO timestamp of most recent outbound referral click")
    last_provider: Optional[str] = Field(None, description="Partner network of most recent click")
    last_ticker: Optional[str] = Field(None, description="Target symbol of most recent click")


class ReferralBuildResponse(BaseModel):
    provider: str = Field(..., description="Affiliate partner network (tradingview, seekingalpha, trendspider)")
    ticker: str = Field(..., description="Target US equity ticker")
    url: str = Field(..., description="Fully constructed affiliate deep link URL")
