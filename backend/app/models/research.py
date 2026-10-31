"""
backend/app/models/research.py - Research brief schemas
"""
from typing import Optional
from pydantic import BaseModel, Field, ConfigDict


class ResearchBriefSummary(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    ticker: str = Field(..., description="Stock symbol (e.g. CELH, MBLY)")
    company_name: str = Field(..., description="Company name")
    title: str = Field("", description="Formatted institutional brief title")
    report_date: str = Field(..., description="Report publication date (YYYY-MM-DD)")
    opinion: str = Field(..., description="Conviction tier (e.g. STRONG_BUY Top-Pick)")
    turnaround_score: float = Field(..., description="Turnaround score (e.g. 76.0 / 100)")
    current_price: Optional[float] = Field(None, description="Latest closing price ($)")
    target_price: Optional[float] = Field(None, description="2x TP1 target price ($)")
    stop_price: Optional[float] = Field(None, description="-9% Stop loss price ($)")
    as_of_date: Optional[str] = Field(None, description="Latest closing price date")
    file_name: str = Field(..., description="Source markdown filename")
    is_pro_locked: bool = Field(False, description="Whether full report is restricted")


class ResearchBriefDetail(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    ticker: str
    company_name: str
    title: str = Field("", description="Formatted institutional brief title")
    report_date: str
    opinion: str
    turnaround_score: float
    current_price: Optional[float] = None
    target_price: Optional[float] = None
    stop_price: Optional[float] = None
    rrr_ratio: Optional[str] = None
    as_of_date: Optional[str] = None
    content: str = Field(..., description="Full or preview markdown body")
    content_markdown: str = Field(..., description="Full or preview markdown body")
    markdown: str = Field(..., description="Full or preview markdown body")
    is_pro_locked: bool = Field(False, description="True if body was truncated due to free tier access")
