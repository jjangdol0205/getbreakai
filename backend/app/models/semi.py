"""
backend/app/models/semi.py - Pydantic schemas for SemiFearGreed (CNN-style Semiconductor Fear & Greed Index & SMH/XLV Barbell Engine)
"""
from typing import List, Optional
from pydantic import BaseModel, Field


class HistoricalPointComparison(BaseModel):
    key: str
    label_en: str
    label_jp: str
    label_kr: str
    date: str
    score: float
    regime_code: str
    regime_en: str
    regime_jp: str
    regime_kr: str


class FearGreedFactor(BaseModel):
    id: str
    order: int
    weight_pct: int
    score: float
    raw_value: float
    raw_display: str
    regime_code: str
    regime_en: str
    regime_jp: str
    regime_kr: str
    title_en: str
    title_jp: str
    title_kr: str
    subtitle_en: str
    subtitle_jp: str
    subtitle_kr: str
    desc_en: str
    desc_jp: str
    desc_kr: str
    sparkline: List[float] = Field(default_factory=list)
    sparkline_dates: List[str] = Field(default_factory=list)


class EtfSnapshot(BaseModel):
    ticker: str
    name_en: str
    name_jp: str
    name_kr: str
    role_en: str
    role_jp: str
    role_kr: str
    close: float
    ret_1d_pct: float
    ret_20d_pct: float
    dd_52w_pct: float
    rsi14: float
    target_weight_normal: int
    target_weight_fear: int


class SemiOverviewResponse(BaseModel):
    date: str
    fg_score: float
    regime_code: str
    regime_en: str
    regime_jp: str
    regime_kr: str
    action_headline_en: str
    action_headline_jp: str
    action_headline_kr: str
    action_detail_en: str
    action_detail_jp: str
    action_detail_kr: str
    smh_close: float
    xlv_close: float
    qqq_close: float
    usdkrw: float
    smh_dd_pct: float
    smh_rsi: float
    vol_ann_pct: float
    natural_smh_weight_pct: float
    recommended_smh_weight: int
    recommended_xlv_weight: int
    comparisons: List[HistoricalPointComparison]
    factors: List[FearGreedFactor]
    etfs: List[EtfSnapshot]


class SemiHistoryPoint(BaseModel):
    date: str
    fg_score: float
    smh_close: float
    xlv_close: float
    port73_norm: float
    qqq_norm: float
    smh_dd_pct: float


class EraBacktestRow(BaseModel):
    horizon_en: str
    horizon_jp: str
    horizon_kr: str
    period: str
    qqq_cagr_pct: float
    qqq_multiple: float
    qqq_mdd_pct: float
    port_70_30_cagr_pct: float
    port_80_20_cagr_pct: float
    port_80_20_multiple: float
    port_80_20_mdd_pct: float


class SemiHistoryResponse(BaseModel):
    range_code: str
    total_days: int
    series: List[SemiHistoryPoint]
    era_summary: List[EraBacktestRow]


class RebalanceRequest(BaseModel):
    total_capital_usd: float = Field(default=100000.0, gt=0.0, le=1000000000.0)
    rebalance_frequency: str = Field(default="ANNUAL")
    strategy_mode: str = Field(default="AUTO_REGIME")
    current_smh_usd: Optional[float] = Field(default=None, ge=0.0)
    current_xlv_usd: Optional[float] = Field(default=None, ge=0.0)
    unrealized_gain_krw: float = Field(default=3800000.0, ge=0.0)


class RebalanceResponse(BaseModel):
    as_of_date: str = Field(default="2026-10-26", description="Latest closing price reference date")
    smh_close: float = Field(default=541.62, description="Latest $SMH closing price ($)")
    xlv_close: float = Field(default=179.28, description="Latest $XLV closing price ($)")
    total_capital_usd: float
    total_capital_krw: float
    usdkrw: float
    fg_score: float
    smh_dd_pct: float
    regime_code: str
    active_rule_en: str
    active_rule_jp: str
    active_rule_kr: str
    target_smh_weight_pct: float
    target_xlv_weight_pct: float
    target_smh_usd: float
    target_xlv_usd: float
    target_smh_shares: int
    target_xlv_shares: int
    residual_cash_usd: float
    delta_smh_usd: float
    delta_xlv_usd: float
    delta_smh_shares: int
    delta_xlv_shares: int
    rebalance_frequency: str
    estimated_tax_drag_pct: float
    expected_net_cagr_pct: float
    kr_tax_deduction_limit_krw: float
    kr_taxable_gain_krw: float
    kr_estimated_tax_saved_krw: float
    kr_tax_guidance_en: str
    kr_tax_guidance_jp: str
    kr_tax_guidance_kr: str


class LumpSumTranche(BaseModel):
    step: int
    title_en: str
    title_jp: str
    title_kr: str
    timing_en: str
    timing_jp: str
    timing_kr: str
    allocation_pct: float
    amount_usd: float
    smh_usd: float
    xlv_usd: float
    cash_rp_usd: float
    smh_shares: int
    xlv_shares: int
    note_en: str
    note_jp: str
    note_kr: str


class LumpSumRequest(BaseModel):
    capital_usd: float = Field(default=50000.0, gt=0.0, le=1000000000.0)
    override_fg_score: Optional[float] = Field(default=None, ge=0.0, le=100.0)


class LumpSumResponse(BaseModel):
    as_of_date: str = Field(default="2026-10-26", description="Latest closing price reference date")
    smh_close: float = Field(default=541.62, description="Latest $SMH closing price ($)")
    xlv_close: float = Field(default=179.28, description="Latest $XLV closing price ($)")
    capital_usd: float
    fg_score_used: float
    case_code: str
    case_title_en: str
    case_title_jp: str
    case_title_kr: str
    summary_en: str
    summary_jp: str
    summary_kr: str
    immediate_deploy_pct: float
    parked_cash_rp_pct: float
    tranches: List[LumpSumTranche]
