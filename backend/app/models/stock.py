"""
backend/app/models/stock.py - Stock Pydantic schemas
"""
from typing import Optional
from pydantic import BaseModel, Field, ConfigDict


class StockBase(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    ticker: str = Field(..., description="Stock ticker symbol (e.g. CELH, TSLA, 000660.KS)")
    name: str = Field(..., description="Default display name")
    name_en: str = Field(..., description="English company name")
    name_jp: str = Field(..., description="Japanese company name")
    name_kr: str = Field(..., description="Korean company name")
    sector: str = Field(..., description="Industry or sector classification")
    date: str = Field(..., description="Screening point-in-time date (YYYY-MM-DD)")
    close: float = Field(..., description="Latest closing price in USD or local currency")
    low52: float = Field(..., description="52-week lowest price")
    high52: float = Field(..., description="52-week highest price")
    prox_low52_pct: float = Field(..., description="Proximity to 52W low (%)")
    dd_high52_pct: float = Field(..., description="Drawdown from 52W high (%)")
    vs_ma20_pct: float = Field(..., description="% difference vs 20-day SMA")
    vs_ma60_pct: float = Field(..., description="% difference vs 60-day SMA")
    vs_ma200_pct: Optional[float] = Field(None, description="% difference vs 200-day SMA")
    ma20_price: float = Field(..., description="20-day Simple Moving Average price")
    ma60_price: Optional[float] = Field(None, description="60-day Simple Moving Average price")
    rsi14: float = Field(..., description="14-period RSI indicator")
    vol_surge_10d: float = Field(..., description="10-day volume surge ratio over 20-day average")
    ret_5d_pct: Optional[float] = Field(None, description="5-day return (%)")
    ret_20d_pct: Optional[float] = Field(None, description="20-day return (%)")
    hist_2x_rate: float = Field(..., description="Historical 1Y 2x (+100%) win rate after -40% crash")
    hist_med_gain: float = Field(..., description="Historical median peak gain (%)")
    score: int = Field(..., description="PW-RSI composite score (0-98)")
    zone_code: str = Field(
        ...,
        description="Technical zone code: IGNITION_ZONE | WASHOUT_WATCH | LEFT_SIDE_KNIFE | VALUE_TRAP_FILTERED",
    )
    zone_label_en: str = Field(..., description="English zone badge label")
    zone_label_jp: str = Field(..., description="Japanese zone badge label")
    zone_label_kr: str = Field(..., description="Korean zone badge label")

    # 4 Ignition Conditions & Diagnostic flags
    c1_deep_dd: bool = Field(False, description="Condition 1: Drawdown <= -20%")
    c2_off_low: bool = Field(False, description="Condition 2: 10% <= Prox <= 45%")
    c3_above_mas: bool = Field(False, description="Condition 3: MA20% >= -0.5% and MA60% >= -4.5%")
    c4_vol_or_mom: bool = Field(False, description="Condition 4: Vol >= 1.30 or Ret20D >= 8%")
    c2_sweet_spot: bool = Field(False, description="Alias for c2_off_low")
    c3_ma_reclaim: bool = Field(False, description="Alias for c3_above_mas")
    c4_vol_washout: bool = Field(False, description="Alias for c4_vol_or_mom")
    all_4_ignition_met: bool = Field(False, description="True if c1-c4 met and not a value trap")

    # Calculated target prices
    stop_loss_price: Optional[float] = Field(None, description="-9% hard stop loss price")
    tp1_2x_price: Optional[float] = Field(None, description="+100% 2x target price")
    entry_trigger_price: Optional[float] = Field(None, description="Max(MA20, MA60) breakout trigger price")
    pct_to_trigger: Optional[float] = Field(None, description="% distance from close to trigger price")


class StockResponse(StockBase):
    """Unified stock response model supporting public masked and pro unmasked views."""
    is_pro_locked: bool = Field(False, description="True if proprietary price targets are blurred/locked")


class StockPublic(StockResponse):
    """Alias for backwards compatibility and clarity in interface contracts."""
    pass
