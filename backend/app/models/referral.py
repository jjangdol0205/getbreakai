"""
backend/app/models/referral.py - CPA Referral Affiliate and Outbound Tracking schemas
"""
from typing import Optional
from pydantic import BaseModel, Field


class ReferralConfig(BaseModel):
    tradingview_aff_id: str = Field("rightsidealpha", description="TradingView partner affiliate ID")
    seekingalpha_source: str = Field("affiliate_rightside", description="Seeking Alpha tracking source tag")
    trendspider_aff_id: str = Field("rightside", description="TrendSpider partner tracking ID")
    ls_site1_monthly_url: str = Field(
        default="https://rightsidealpha.lemonsqueezy.com/checkout/buy/pro-monthly",
        description="Lemon Squeezy Pro Monthly checkout URL",
    )
    ls_site1_ltd_url: str = Field(
        default="https://rightsidealpha.lemonsqueezy.com/checkout/buy/lifetime-pass",
        description="Lemon Squeezy Lifetime Pass checkout URL",
    )
    site1_url: str = Field(
        default="https://truthofmarket.com",
        description="Primary production domain URL",
    )
    broker_name: str = Field("IBKR / Webull", description="Broker/Exchange partner label")
    broker_referral_url: str = Field(
        "https://ibkr.com/referral/rightsidealpha",
        description="Broker/Exchange affiliate referral URL",
    )
    telegram_channel_url: Optional[str] = Field("https://t.me/SemifearGreedbot")
    youtube_url: Optional[str] = Field("https://youtube.com/@rightsidealpha")
    instagram_url: Optional[str] = Field("https://www.instagram.com/semifeargreed")


class ReferralClickStats(BaseModel):
    total: int = Field(0, description="Cumulative outbound click count across all networks")
    tradingview: int = Field(0, description="TradingView click count")
    seekingalpha: int = Field(0, description="Seeking Alpha click count")
    trendspider: int = Field(0, description="TrendSpider click count")
    broker: int = Field(0, description="Broker/Exchange click count")
    last_clicked_at: Optional[str] = Field(None, description="ISO timestamp of most recent outbound referral click")
    last_provider: Optional[str] = Field(None, description="Partner network of most recent click")
    last_ticker: Optional[str] = Field(None, description="Target symbol of most recent click")


class ReferralBuildResponse(BaseModel):
    provider: str = Field(..., description="Affiliate partner network (tradingview, seekingalpha, trendspider)")
    ticker: str = Field(..., description="Target US equity ticker")
    url: str = Field(..., description="Fully constructed affiliate deep link URL")
