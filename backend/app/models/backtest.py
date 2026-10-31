"""
backend/app/models/backtest.py - Backtest and strategy schemas
"""
from typing import List, Optional, Any, Dict
from pydantic import BaseModel, Field, ConfigDict


class StrategySummary(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    strategy_name: str = Field(..., alias="Strategy", description="Strategy name or comparison benchmark")
    final_multiple: float = Field(..., alias="Final_Multiple", description="Final equity multiple (e.g. 203.87x)")
    cumulative_return_pct: float = Field(..., alias="Cumulative_Return_Pct", description="Cumulative total return percentage")
    cagr_pct: float = Field(..., alias="CAGR_Pct", description="Compound annual growth rate (%)")
    max_drawdown_pct: float = Field(..., alias="Max_Drawdown_Pct", description="Maximum drawdown percentage (MDD)")
    sharpe_ratio: float = Field(..., alias="Sharpe_Ratio", description="Annualized Sharpe ratio")
    calmar_ratio: float = Field(..., alias="Calmar_Ratio", description="Calmar ratio")


class YearlyPerformance(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    year: int = Field(..., alias="Year", description="Calendar year (2000-2026)")
    pw_rsi_return_pct: float = Field(..., alias="PW_RSI_Return_Pct", description="PW-RSI annual return (%)")
    pw_pure_price_return_pct: float = Field(..., alias="PW_PurePrice_Return_Pct", description="Pure price/vol return without earnings filter (%)")
    naive_52w_low_return_pct: float = Field(..., alias="Naive_52W_Low_Return_Pct", description="Blind 52W low return (%)")
    qqq_return_pct: float = Field(..., alias="QQQ_Return_Pct", description="Nasdaq-100 (QQQ) return (%)")
    spy_return_pct: float = Field(..., alias="SPY_Return_Pct", description="S&P 500 (SPY) return (%)")
    alpha_vs_qqq_pct: float = Field(..., alias="Alpha_vs_QQQ_Pct", description="Excess alpha over QQQ (%)")
    pw_rsi_mdd_pct: float = Field(..., alias="PW_RSI_IntraYear_MDD_Pct", description="Intra-year maximum drawdown (%)")
    nav_multiple: float = Field(..., alias="Nav_Multiple", description="Cumulative NAV multiple at year end")
    key_switched_stocks: Optional[str] = Field(None, alias="Key_Switched_Stocks", description="Key switched trade symbols")


class BacktestKpis(BaseModel):
    hit_rate_2x_pct: float = Field(55.24, description="1Y 2x (+100%) hit rate (%)")
    median_days_underwater: float = Field(29.0, description="Median days held underwater before recovery")
    cagr_pct: float = Field(21.97, description="26.8-year compound annual growth rate (%)")
    cagr_after_tax_pct: float = Field(17.81, description="26.8-year after-tax and slippage CAGR (%)")
    us_only_net_cagr_pct: float = Field(17.81, description="US equity net CAGR after tax and friction (%)")
    final_multiple: float = Field(203.87, description="Final cumulative equity multiple (gross)")
    final_multiple_after_tax: float = Field(80.5, description="Final cumulative equity multiple (net after 22% tax)")
    severe_loss_risk_pct: float = Field(0.93, description="Risk of severe drawdown <= -20% via -9% stop")
    baseline_severe_loss_risk_pct: float = Field(24.82, description="Baseline severe loss risk without stops")
    period: str = Field("2000-01-03 ~ 2026-10-13 (26.78 Years)", description="Verified backtest time window")
    universe_size: int = Field(126, description="Total historical universe size")


class BacktestSummaryResponse(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    period: str
    universe_size: int
    kpis: BacktestKpis
    strategies: List[Any] = Field(default_factory=list)
    overall_summary: List[Any] = Field(default_factory=list)
    yearly_performance: List[Any] = Field(default_factory=list)
    total_trades_count: int


class TradeLog(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    entry_date: str = Field(..., description="Trade entry execution date (YYYY-MM-DD)")
    exit_date: str = Field(..., description="Trade exit execution date (YYYY-MM-DD)")
    ticker: str = Field(..., description="Stock symbol (e.g. CELH, URI, REGN)")
    name: str = Field(..., description="Stock display name")
    entry_price: float = Field(..., description="Entry execution price")
    exit_price: float = Field(..., description="Exit execution price")
    return_pct: float = Field(..., description="Realized net trade return (%)")
    peak_return_pct: float = Field(..., description="Maximum unrealized peak return during trade (%)")
    days_held: int = Field(..., description="Trading days held")
    entry_score: float = Field(..., description="PW-RSI conviction score at entry")
    exit_reason: str = Field(..., description="Exit rule triggered")


class TradeLogsResponse(BaseModel):
    total_trades: int
    win_rate_pct: float
    trades: List[TradeLog]


class PositionDoctorRequest(BaseModel):
    ticker: str
    entry_price: float
    days_held: int
    current_price: Optional[float] = None


class PositionDoctorResponse(BaseModel):
    ticker: str
    status_code: str
    status_label: str
    return_pct: float
    rule_triggered: str
    action_plan: str
    is_critical: bool
    current_price: Optional[float] = Field(None, description="Latest closing price ($)")
    entry_price: Optional[float] = Field(None, description="User cost basis ($)")
    stop_price: Optional[float] = Field(None, description="-9% Hard Stop price from entry ($)")
    tp1_price: Optional[float] = Field(None, description="2x (+100%) TP1 price from entry ($)")
    as_of_date: Optional[str] = Field(None, description="Latest closing price date")
