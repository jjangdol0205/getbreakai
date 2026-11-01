"""
backend/app/models/referral.py - CPA Referral Affiliate and Outbound Tracking schemas
"""
from typing import Optional
from pydantic import BaseModel, Field


class ReferralConfig(BaseModel):
    site1_name: Optional[str] = Field("RightSideAlpha", description="Primary platform brand name")
    site1_url: str = Field(
        default="https://truthofmarket.com",
        description="Primary production domain URL",
    )
    site2_url: Optional[str] = Field(
        default="https://truthofmarket.com",
        description="Secondary production domain URL",
    )
    ls_site1_monthly_url: str = Field(
        default="https://truthofmarket.lemonsqueezy.com/checkout/buy/bad98d00-7175-41f6-9d58-eeb2471d0da4",
        description="Lemon Squeezy Pro Monthly checkout URL",
    )
    ls_site1_ltd_url: str = Field(
        default="https://truthofmarket.lemonsqueezy.com/checkout/buy/00c9f6e1-c8be-42a4-b5a5-e05af1a41ed9",
        description="Lemon Squeezy Lifetime Pass checkout URL",
    )
    tradingview_aff_id: str = Field("1173809", description="TradingView partner affiliate ID")
    seekingalpha_source: str = Field("better_life333", description="Seeking Alpha tracking source tag")
    trendspider_aff_id: str = Field("rightside", description="TrendSpider partner tracking ID")
    broker_name: str = Field("Bitget (7nja)", description="Broker/Exchange partner label")
    broker_referral_url: str = Field(
        "https://www.bitget.com/referral/register?clacCode=7nja",
        description="Broker/Exchange affiliate referral URL",
    )
    telegram_channel_url: Optional[str] = Field("https://t.me/truthofmarketss")
    telegram_vip_channel_url: Optional[str] = Field("https://t.me/+a6Sl2yLirbwyODQ1")
    telegram_chat_id: Optional[str] = Field("@truthofmarketss")
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
