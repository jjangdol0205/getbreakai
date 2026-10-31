"""
backend/app/models/auth.py - Authentication and Pro Access Control Pydantic schemas
"""
from typing import Optional, List
from pydantic import BaseModel, Field, field_validator


class LicenseValidateRequest(BaseModel):
    license_key: str = Field(..., description="Lemon Squeezy or Demo license key")
    instance_name: Optional[str] = Field(None, description="Optional client instance identifier")


class LicenseValidateResponse(BaseModel):
    valid: bool = Field(..., description="Whether license is valid and active")
    tier: str = Field("free", description="Subscription tier: 'pro', 'pro_lifetime', or 'free'")
    license_key: str = Field(..., description="Validated license key")
    expires_at: Optional[str] = Field(None, description="ISO timestamp for license expiration")
    message: str = Field(..., description="Human-readable validation message")


class ProVaultResponse(BaseModel):
    unlocked: bool = Field(..., description="Pro vault unlock status")
    tier: str = Field("pro", description="Access tier")
    pine_script_available: bool = Field(True, description="Indicator code access flag")
    tools: List[str] = Field(default_factory=list, description="Enabled pro quantitative tools")


class PineScriptResponse(BaseModel):
    version: str = Field("v5", description="TradingView Pine Script syntax version")
    name: str = Field("RightSideAlpha PW-RSI", description="Script title")
    code: str = Field(..., description="TradingView Pine Script v5 source code")


class ProPositionDoctorRequest(BaseModel):
    ticker: str = Field(..., description="Stock symbol")
    entry_price: float = Field(..., description="Entry execution price (must be positive)")
    days_held: int = Field(..., description="Trading days held (must be non-negative)")
    current_price: Optional[float] = Field(None, description="Optional current stock price")

    @field_validator("entry_price")
    @classmethod
    def validate_entry_price(cls, v: float) -> float:
        if v <= 0:
            raise ValueError("Entry price must be positive")
        return v

    @field_validator("days_held")
    @classmethod
    def validate_days_held(cls, v: int) -> int:
        if v < 0:
            raise ValueError("Days held cannot be negative")
        return v


class ProPositionDoctorResponse(BaseModel):
    ticker: str
    status_code: str
    status_label: str
    return_pct: float
    rule_triggered: str
    action_plan: str
    is_critical: bool
    stop_price: Optional[float] = None
    tp1_price: Optional[float] = None
