"""Timing & Valuation Engine for Multi-Stock Investment Processing Hub.

Implements:
1. Quantitative Valuation Bands & Downside Support Floors (R1)
2. 3-Condition Composite Trigger Engine (Safety Margin + Catalyst D-Day + Volume Wash-Out) (R1)
3. 3-Tier Take-Profit Framework (TP1, TP2, TP3) (R2)
4. Opportunity-Cost Stock Switching Engine (R4)
5. Continuous Daily Analysis & History Tracking Pipeline (R5)
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import datetime, date as dt_date
import json
import math
from typing import Any, Dict, List, Optional, Tuple, Union

from engine.models import (
    StockSymbol,
    STOCK_MASTERS,
    DailyMarketData,
    StockFactSheet,
)


@dataclass
class ValuationBandConfig:
    """Quantitative valuation multiples, safety margin buy band, and downside support floor."""
    stock_id: str
    currency: str
    metric_type: str
    metric_value_current: str
    metric_band_trough: str
    metric_band_target: str
    min_price: float
    max_price: float
    min_price_formatted: str
    max_price_formatted: str
    key_support_price: float
    key_support_formatted: str
    rationale: str

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class CatalystEvent:
    """Actionable confirmed catalyst with target date, countdown D-Day, and impact level."""
    name: str
    target_date: str
    days_remaining: Optional[int]
    impact_level: str  # "HIGH", "CRITICAL"
    description: str
    is_confirmed: bool = True

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class TakeProfitConfig:
    """3-Tier profit-taking roadmap (TP1, TP2, TP3) for long-term wave maximization."""
    tp1_price: float
    tp1_price_formatted: str
    tp1_action: str
    tp1_gain_pct: float
    tp2_price: float
    tp2_price_formatted: str
    tp2_action: str
    tp2_gain_pct: float
    tp2_valuation_target: str
    tp3_condition: str
    tp3_action: str
    tp3_trigger_indicators: List[str]

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class CompositeTriggerResult:
    """3-Condition composite trigger evaluation result eliminating dead money."""
    stock_id: str
    date: str
    current_price: float
    current_price_formatted: str
    cond1_safety_margin: bool
    cond1_detail: str
    cond2_catalyst_imminent: bool
    cond2_days_remaining: int
    cond2_detail: str
    cond3_volume_washout: bool
    cond3_detail: str
    composite_score: int  # 0 to 3
    signal: str  # "STRONG_BUY", "ACCUMULATE", "WATCH_CATALYST", "HOLD", "TAKE_PROFIT"
    signal_label: str
    dead_money_risk: str  # "LOW", "MEDIUM", "HIGH"
    risk_reward_ratio: float
    downside_risk_pct: float
    upside_tp1_pct: float
    upside_tp2_pct: float

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class StockTimingEvaluation:
    """Complete timing evaluation package for a single stock."""
    stock_id: str
    stock_name: str
    ticker: str
    valuation_band: ValuationBandConfig
    catalysts: List[CatalystEvent]
    take_profit: TakeProfitConfig
    trigger: CompositeTriggerResult

    def to_dict(self) -> Dict[str, Any]:
        return {
            "stockId": self.stock_id,
            "stockName": self.stock_name,
            "ticker": self.ticker,
            "valuationBand": self.valuation_band.to_dict(),
            "catalysts": [c.to_dict() for c in self.catalysts],
            "takeProfit": self.take_profit.to_dict(),
            "trigger": self.trigger.to_dict(),
        }


@dataclass
class SwitchingRecommendation:
    """Opportunity-cost based switching recommendation vs holding core asset."""
    holding_stock_id: str
    holding_shares: int
    holding_price: float
    holding_eval_amount: str
    holding_rrr: float
    holding_catalyst_d_day: int
    status: str  # "HOLD_CORE", "SWITCH_OPPORTUNITY", "REVERSE_SWITCH_WARNING"
    summary: str
    top_candidate_id: Optional[str]
    candidates: List[Dict[str, Any]]
    scenarios: List[Dict[str, Any]]

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class PortfolioDiagnostic:
    """Real-time portfolio diagnostic for core holding (SK Square 76 shares)."""
    stock_id: str = "SK_SQUARE"
    stock_name: str = "SK스퀘어"
    shares: int = 76
    principal_krw: int = 82840000
    avg_cost_krw: int = 1090000
    current_price: float = 1050000.0
    current_price_formatted: str = "1,050,000원"
    current_valuation_krw: int = 79800000
    pnl_amount_krw: int = -3040000
    pnl_rate_pct: float = -3.67
    tp1_target_price: float = 2180000.0
    tp1_target_formatted: str = "2,180,000원"
    tp1_shares_to_sell: int = 38
    tp1_recovered_amount: int = 82840000
    tp1_recovered_formatted: str = "8,284만 원"
    tp1_progress_pct: float = 48.2
    status_phase: str = "ACCUMULATION_AND_WAITING"
    recovery_roadmap: str = (
        "1~2년 내 TP1(218만 원) 도달 시 38주 매도로 원금 8,284만 원(82,840,000 KRW) 100% 무위험(Risk-Free) 회수. "
        "잔여 38주는 원가 0원 상태로 TP2(500만 원) 및 TP3 사이클 완주."
    )

    def to_dict(self) -> Dict[str, Any]:
        return {
            "stockId": self.stock_id,
            "stockName": self.stock_name,
            "shares": self.shares,
            "principalKrw": self.principal_krw,
            "principalFormatted": f"{self.principal_krw // 10000:,}만 원",
            "avgCostKrw": self.avg_cost_krw,
            "avgCostFormatted": f"{self.avg_cost_krw:,}원",
            "currentPrice": self.current_price,
            "currentPriceFormatted": self.current_price_formatted,
            "currentValuationKrw": self.current_valuation_krw,
            "currentValuationFormatted": f"{self.current_valuation_krw // 10000:,}만 원",
            "pnlAmountKrw": self.pnl_amount_krw,
            "pnlAmountFormatted": f"{self.pnl_amount_krw:,}원",
            "pnlRatePct": self.pnl_rate_pct,
            "tp1TargetPrice": self.tp1_target_price,
            "tp1TargetFormatted": self.tp1_target_formatted,
            "tp1SharesToSell": self.tp1_shares_to_sell,
            "tp1RecoveredAmount": self.tp1_recovered_amount,
            "tp1RecoveredFormatted": self.tp1_recovered_formatted,
            "tp1ProgressPct": self.tp1_progress_pct,
            "statusPhase": self.status_phase,
            "recoveryRoadmap": self.recovery_roadmap,
        }

    def __getitem__(self, key: str) -> Any:
        if hasattr(self, key):
            return getattr(self, key)
        d = self.to_dict()
        if key in d:
            return d[key]
        raise KeyError(key)

    def get(self, key: str, default: Any = None) -> Any:
        try:
            return self[key]
        except KeyError:
            return default


@dataclass
class SwitchingActionScenario:
    """Tactical switching action scenario comparing core holding vs candidates."""
    candidate_id: str
    candidate_name: str
    action_type: str  # "TACTICAL_SWITCH", "HOLD_DEFENSE", "NONE"
    shares_to_sell: int
    freed_capital_krw: int
    candidate_shares_to_buy: int
    holding_tp1_upside_pct: float
    candidate_tp1_upside_pct: float
    reason: str

    def to_dict(self) -> Dict[str, Any]:
        return {
            "candidateId": self.candidate_id,
            "candidateName": self.candidate_name,
            "actionType": self.action_type,
            "sharesToSell": self.shares_to_sell,
            "freedCapitalKrw": self.freed_capital_krw,
            "candidateSharesToBuy": self.candidate_shares_to_buy,
            "holdingTp1UpsidePct": self.holding_tp1_upside_pct,
            "candidateTp1UpsidePct": self.candidate_tp1_upside_pct,
            "reason": self.reason,
        }

    def __getitem__(self, key: str) -> Any:
        if hasattr(self, key):
            return getattr(self, key)
        d = self.to_dict()
        if key in d:
            return d[key]
        raise KeyError(key)

    def get(self, key: str, default: Any = None) -> Any:
        try:
            return self[key]
        except KeyError:
            return default


@dataclass
class RiskManagementAlert:
    """Actionable risk management alert preventing dead money and reverse switching."""
    alert_type: str  # "REVERSE_SWITCH_DEFENSE", "DEAD_MONEY", "SUPPORT_DEFENSE", "CATALYST_DUE"
    severity: str    # "INFO", "WARNING", "CRITICAL"
    stock_id: str
    message: str
    action_guideline: str

    def to_dict(self) -> Dict[str, Any]:
        return {
            "alertType": self.alert_type,
            "severity": self.severity,
            "stockId": self.stock_id,
            "message": self.message,
            "actionGuideline": self.action_guideline,
        }

    def __getitem__(self, key: str) -> Any:
        if hasattr(self, key):
            return getattr(self, key)
        d = self.to_dict()
        if key in d:
            return d[key]
        raise KeyError(key)

    def get(self, key: str, default: Any = None) -> Any:
        try:
            return self[key]
        except KeyError:
            return default


@dataclass
class FundManagerProposal:
    """Actionable holistic investment proposal generated by Value+Timing Genius Fund Manager AI."""
    date: str
    timestamp: str
    manager_persona: str
    investment_horizon: str
    target_objective: str
    core_holding: PortfolioDiagnostic
    tactical_action: str  # "HOLD_CORE", "TACTICAL_SWITCH", "TAKE_PROFIT_TP1", "REVERSE_SWITCH_WARNING"
    action_headline: str
    executive_summary: str
    reasoning_pillars: Dict[str, str]
    time_to_100_ranking: List[Dict[str, Any]]
    switching_proposal: Optional[SwitchingActionScenario]
    risk_warnings: List[RiskManagementAlert]
    journal_markdown: str

    def to_dict(self) -> Dict[str, Any]:
        return {
            "date": self.date,
            "timestamp": self.timestamp,
            "managerPersona": self.manager_persona,
            "investmentHorizon": self.investment_horizon,
            "targetObjective": self.target_objective,
            "coreHolding": self.core_holding.to_dict(),
            "tacticalAction": self.tactical_action,
            "actionHeadline": self.action_headline,
            "executiveSummary": self.executive_summary,
            "reasoningPillars": self.reasoning_pillars,
            "timeTo100Ranking": self.time_to_100_ranking,
            "switchingProposal": self.switching_proposal.to_dict() if self.switching_proposal else None,
            "riskWarnings": [w.to_dict() for w in self.risk_warnings],
            "riskWarningMessages": [w.message for w in self.risk_warnings],
            "journalMarkdown": self.journal_markdown,
        }

    def __getitem__(self, key: str) -> Any:
        if hasattr(self, key):
            return getattr(self, key)
        d = self.to_dict()
        if key in d:
            return d[key]
        raise KeyError(key)

    def get(self, key: str, default: Any = None) -> Any:
        try:
            return self[key]
        except KeyError:
            return default


@dataclass
class DailyTimingSnapshot:
    """Comprehensive daily timing snapshot including all 8 stocks, switching guidance, and manager proposal."""
    date: str
    timestamp: str
    stocks: Dict[str, StockTimingEvaluation]
    switching: SwitchingRecommendation
    manager_proposal: Optional[FundManagerProposal] = None

    def to_dict(self) -> Dict[str, Any]:
        res = {
            "date": self.date,
            "timestamp": self.timestamp,
            "stocks": {k: v.to_dict() for k, v in self.stocks.items()},
            "switching": self.switching.to_dict(),
        }
        if self.manager_proposal is not None:
            res["managerProposal"] = self.manager_proposal.to_dict()
        return res


# ==============================================================================
# Master Benchmark Configurations for 8 Monitored Stocks
# ==============================================================================

# Canonical 20-Day Average Volume Benchmarks
STOCK_BENCHMARK_20D_VOLUME: Dict[str, int] = {
    "SK_HYNIX": 180000,       # NASDAQ ADR regular trading volume
    "SK_SQUARE": 80000,       # KRX regular volume
    "UBER": 14500000,         # NYSE regular volume
    "MBLY": 4260000,          # NASDAQ regular volume
    "FLNC": 1500000,          # NASDAQ regular volume
    "UPST": 3500000,          # NASDAQ regular volume
    "CELH": 2500000,          # NASDAQ regular volume
    "ENPH": 2200000,          # NASDAQ regular volume
}

# Reference Fallback Prices
STOCK_REFERENCE_PRICES: Dict[str, float] = {
    "SK_HYNIX": 169.66,
    "SK_SQUARE": 1065000.0,
    "UBER": 71.51,
    "MBLY": 7.10,
    "FLNC": 16.20,
    "UPST": 37.90,
    "CELH": 27.35,
    "ENPH": 33.07,
}

# Wash-Out & Support Defense Thresholds
MIN_WASHOUT_VOLUME_RATIO: float = 1.4       # Primary volume surge threshold (1.4x 20d average)
DEFAULT_SUPPORT_BREACH_PENALTY_PCT: float = 10.0  # Base downside risk penalty when price breaks support


class TimingEngine:
    """Core timing and valuation engine for multi-stock investment processing hub."""

    # --------------------------------------------------------------------------
    # 1. Valuation Bands & Support Floors (R1)
    # --------------------------------------------------------------------------

    @classmethod
    def get_valuation_band(cls, stock_id: str, current_price: Optional[float] = None) -> ValuationBandConfig:
        """Return quantitative valuation band and downside support floor configuration.
        
        Supports dual-currency normalization for SK_HYNIX (USD ADR vs KRW Domestic).
        """
        sid = stock_id.upper()

        if sid == "SK_HYNIX":
            # Dual currency check: if price > 10,000 and finite, treat as KRW domestic share
            is_krw = (
                current_price is not None
                and isinstance(current_price, (int, float))
                and math.isfinite(current_price)
                and current_price > 10000.0
            )
            if is_krw:
                return ValuationBandConfig(
                    stock_id="SK_HYNIX",
                    currency="KRW",
                    metric_type="Forward P/E & P/B",
                    metric_value_current="12M Fwd P/E 6.5x / P/B 1.35x",
                    metric_band_trough="Fwd P/E 4.0x~5.5x / P/B 1.3x",
                    metric_band_target="Fwd P/E 10.0x~11.0x / P/B 2.8x",
                    min_price=1650000.0,
                    max_price=1750000.0,
                    min_price_formatted="1,650,000원",
                    max_price_formatted="1,750,000원",
                    key_support_price=1580000.0,
                    key_support_formatted="1,580,000원",
                    rationale="12M Fwd P/E 4.0x~5.5x 역사적 밸류에이션 바닥, P/B 1.3x 청산가치 근접, 2027 HBM 완판 및 독점적 마진 방어",
                )
            return ValuationBandConfig(
                stock_id="SK_HYNIX",
                currency="USD",
                metric_type="Forward P/E & P/B",
                metric_value_current="12M Fwd P/E 6.5x / P/B 1.35x",
                metric_band_trough="Fwd P/E 4.0x~5.5x / P/B 1.3x",
                metric_band_target="Fwd P/E 10.0x~11.0x / P/B 2.8x",
                min_price=160.0,
                max_price=175.0,
                min_price_formatted="$160.00",
                max_price_formatted="$175.00",
                key_support_price=155.0,
                key_support_formatted="$155.00",
                rationale="12M Fwd P/E 4.0x~5.5x 역사적 밸류에이션 바닥, P/B 1.3x 청산가치 근접, 2027 HBM 완판 및 독점적 마진 방어",
            )

        elif sid == "SK_SQUARE":
            return ValuationBandConfig(
                stock_id="SK_SQUARE",
                currency="KRW",
                metric_type="Holding Company NAV Discount",
                metric_value_current="NAV 1,855,000원 / 할인율 43.4%",
                metric_band_trough="NAV 할인율 55%~62%",
                metric_band_target="NAV 할인율 30% 정상화",
                min_price=1000000.0,
                max_price=1120000.0,
                min_price_formatted="1,000,000원",
                max_price_formatted="1,120,000원",
                key_support_price=980000.0,
                key_support_formatted="980,000원",
                rationale="주당 NAV 1,855,000원 대비 할인율 43%~55% 극단적 저평가, 솔리다임 150조 원 가치 장부 미반영 및 지분율 21% 확정",
            )

        elif sid == "UBER":
            return ValuationBandConfig(
                stock_id="UBER",
                currency="USD",
                metric_type="Forward P/E & EV/FCF",
                metric_value_current="12M Fwd P/E 17.5x / FCF $8.2B",
                metric_band_trough="Fwd P/E 15.0x~17.0x",
                metric_band_target="Fwd P/E 30.0x",
                min_price=62.0,
                max_price=68.5,
                min_price_formatted="$62.00",
                max_price_formatted="$68.50",
                key_support_price=60.0,
                key_support_formatted="$60.00",
                rationale="연간 FCF 82억 달러 창출, 자율주행 하이브리드 플랫폼 전환기 Fwd P/E 15x 바닥권 및 에셋라이트 플랫폼 해자",
            )

        elif sid == "MBLY":
            return ValuationBandConfig(
                stock_id="MBLY",
                currency="USD",
                metric_type="EV/Sales & Net Cash Defense",
                metric_value_current="EV/Sales 3.2x / 순현금 $1.6B",
                metric_band_trough="EV/Sales 2.5x~3.2x",
                metric_band_target="EV/Sales 8.0x~10.0x",
                min_price=6.5,
                max_price=7.5,
                min_price_formatted="$6.50",
                max_price_formatted="$7.50",
                key_support_price=6.2,
                key_support_formatted="$6.20",
                rationale="순현금 16억 달러(주당 $2.0) 보유로 부도 위험 전무, 인텔 오버행 투매 흡수 완료 및 턴키 ADAS 4대 해자",
            )

        elif sid == "FLNC":
            return ValuationBandConfig(
                stock_id="FLNC",
                currency="USD",
                metric_type="EV/Sales & Backlog Support",
                metric_value_current="EV/Sales 1.1x / 수주잔고 $6.4B",
                metric_band_trough="EV/Sales 0.8x~1.1x",
                metric_band_target="EV/Sales 3.5x~4.5x",
                min_price=14.0,
                max_price=16.5,
                min_price_formatted="$14.00",
                max_price_formatted="$16.50",
                key_support_price=13.5,
                key_support_formatted="$13.50",
                rationale="수주잔고 64억 달러 대비 시총 28억 달러 극저평가, EVE Power 배터리 LTA 기반 휴스턴 모듈 공장 원가 경쟁력",
            )

        elif sid == "UPST":
            return ValuationBandConfig(
                stock_id="UPST",
                currency="USD",
                metric_type="P/S Multiple & AI Loan Bottom",
                metric_value_current="P/S 4.2x / 자동승인 91%",
                metric_band_trough="P/S 3.2x~4.2x",
                metric_band_target="P/S 12.0x~15.0x",
                min_price=32.0,
                max_price=36.0,
                min_price_formatted="$32.00",
                max_price_formatted="$36.00",
                key_support_price=30.0,
                key_support_formatted="$30.00",
                rationale="금리 인하 사이클 진입 시 AI 신용평가 대출 취급액 레버리지 폭발, 대손충당금 정점 통과 및 숏스퀴즈 모멘텀",
            )

        elif sid == "CELH":
            return ValuationBandConfig(
                stock_id="CELH",
                currency="USD",
                metric_type="Forward P/E & Post-Pepsi Reset",
                metric_value_current="12M Fwd P/E 21.5x / 북미점유율 15%+",
                metric_band_trough="Fwd P/E 18.0x~22.0x",
                metric_band_target="Fwd P/E 30.0x~35.0x",
                min_price=25.0,
                max_price=28.5,
                min_price_formatted="$25.00",
                max_price_formatted="$28.50",
                key_support_price=23.5,
                key_support_formatted="$23.50",
                rationale="펩시코 유통망 재고 조정(Inventory Reset) 완료, 내부자 4인 $26.50 장내 매수 지지선 사수 및 글로벌 확장",
            )

        elif sid == "ENPH":
            return ValuationBandConfig(
                stock_id="ENPH",
                currency="USD",
                metric_type="Forward P/E & Net Cash Fortress",
                metric_value_current="12M Fwd P/E 23.0x / 순현금 $360M",
                metric_band_trough="Fwd P/E 19.0x~26.0x",
                metric_band_target="Fwd P/E 35.0x~40.0x",
                min_price=30.0,
                max_price=35.0,
                min_price_formatted="$30.00",
                max_price_formatted="$35.00",
                key_support_price=28.0,
                key_support_formatted="$28.00",
                rationale="30달러 역사적 바닥권, 순현금 3.6억 달러 방어력, GAAP GPM 45%의 압도적 마진 구조 및 AI 데이터센터 DER 진출",
            )

        else:
            raise ValueError(f"Unknown stock identifier: {stock_id}")

    # --------------------------------------------------------------------------
    # 2. Confirmed Catalyst Events (R1)
    # --------------------------------------------------------------------------

    @classmethod
    def get_catalysts(cls, stock_id: str, as_of_date: Optional[str] = None) -> List[CatalystEvent]:
        """Return confirmed catalyst events with real D-Day calculation relative to as_of_date."""
        sid = stock_id.upper()

        if as_of_date:
            try:
                base_dt = datetime.strptime(as_of_date, "%Y-%m-%d").date()
            except Exception:
                base_dt = dt_date(2026, 10, 12)
        else:
            base_dt = dt_date(2026, 10, 12)

        def _make_event(name: str, target_str: str, impact: str, desc: str) -> CatalystEvent:
            t_dt = datetime.strptime(target_str, "%Y-%m-%d").date()
            diff_days = (t_dt - base_dt).days
            return CatalystEvent(
                name=name,
                target_date=target_str,
                days_remaining=diff_days,
                impact_level=impact,
                description=desc,
                is_confirmed=True,
            )

        events_map: Dict[str, List[Tuple[str, str, str, str]]] = {
            "SK_HYNIX": [
                ("3Q26 실적 발표 및 배당 결의", "2026-10-27", "CRITICAL", "분기 영업이익 7.5조~8.0조 원 달성 및 주주환원 배당 결의"),
                ("40조 원 자사주 소각 집행 완료", "2026-10-20", "HIGH", "자사주 소각 80%+ 달성 및 완료로 주당 가치 급증, SK스퀘어 지분율 21.0%+ 상향"),
                ("용인 반도체 클러스터 1기 팹 착공", "2026-11-25", "HIGH", "차세대 HBM4 16단 패키징 라인 구축 및 장기 공급계약(LTA) 확대"),
            ],
            "SK_SQUARE": [
                ("자사주 2,000억 소각 및 지분율 21% 확정", "2026-10-22", "CRITICAL", "하이닉스 주식 소각 수혜로 스퀘어 보유 지분율 21.0%+ 영구 상승 및 지주사 밸류업 소각 집행"),
                ("SK하이닉스 3Q 결산 배당금 유입 결의", "2026-11-10", "HIGH", "하이닉스 FCF 급증에 따른 수천억 원 규모 지주사 배당금 수혈 및 현금 유동성 확보"),
                ("솔리다임(Solidigm) 기업공개(IPO) 주관사 선정", "2026-12-05", "HIGH", "AI eSSD 세계 1위 솔리다임 150조~200조 상장 가시화 및 지분가치 41조 원 재평가"),
            ],
            "UBER": [
                ("3Q26 실적 발표 및 연간 FCF 상향", "2026-11-04", "CRITICAL", "모빌리티/배달 통합 총 예약액 가속 및 FCF $8.5B+ 상향 가이던스"),
                ("ezCater B2B 케이터링 결합 완료", "2026-11-20", "HIGH", "23억 달러 B2B 식음료 플랫폼 합병 시너지로 법인 배차 및 케이터링 독점력 강화"),
                ("유럽 4개 도시 무인 로보택시 2,000대 확장", "2026-12-10", "HIGH", "크로아티아 자그레브 상용화 성공 후 독일/프랑스 무인택시 배차망 독점 확대"),
            ],
            "MBLY": [
                ("암논 샤슈아 $2,000 미만 차세대 AI 논문 발표", "2026-10-30", "CRITICAL", "컴파운드 AI 및 30~50W 저전력 ASIC 혁신으로 엔비디아 200W 대비 1/4 전력 자율주행 공개"),
                ("3Q26 실적 발표 및 영구 CEO 선임", "2026-10-31", "HIGH", "ADAS EyeQ6 재고 정상화 및 고단가 서라운드 ADAS(ASP $90~150) 수주 확인"),
                ("2027 SuperVision 포르쉐/VW 30만 대 SOP 확정", "2026-11-28", "CRITICAL", "BOM $10,000 이하 2027 로보택시 턴어라운드 및 잉여현금흐름 폭발 시점 가시화"),
            ],
            "FLNC": [
                ("FY26 4Q 실적 발표 및 2027 흑자 전환 가이던스", "2026-11-18", "CRITICAL", "분기 EBITDA 흑자 안착 및 미국 내 현지화 배터리 세액공제(45X) 수혜 가시화"),
                ("EVE Power LTA 휴스턴 팩 생산 가동", "2026-11-30", "HIGH", "배터리 공급망 탈중국화 완성 및 400MWh 유틸리티 상업 운전 개시"),
                ("텍사스 ERCOT 1.2GWh 그리드 연결 준공", "2026-12-15", "HIGH", "AI 데이터센터 직결 전력망 ESS 운영으로 분기 매출 $1.2B 돌파"),
            ],
            "UPST": [
                ("3Q26 실적 발표 및 M18 AI 전환율 공개", "2026-11-06", "CRITICAL", "자동 승인율 91% 돌파 및 사모신용(Private Credit) 대출 풀 $4.5B 재개"),
                ("미 연준(FOMC) 추가 금리 인하 결정", "2026-11-07", "HIGH", "조달 금리 50bp 하락에 따른 파트너 은행 대출 유동성 급증"),
                ("자동차/담보대출 100개 파트너 확보", "2026-12-01", "HIGH", "신용대출 외 담보대출 비중 35%로 다변화하여 수익 안정성 제고"),
            ],
            "CELH": [
                ("3Q26 실적 발표 및 펩시코 주문 정상화", "2026-11-05", "CRITICAL", "도매 출하량 저점 확인 및 스캐너 소매 판매액 두 자릿수 성장 재확인"),
                ("가을 NACS 편의점 매대 17% 확장 리셋", "2026-11-15", "HIGH", "미국 편의점 에너지 음료 매대 2위(점유율 16%) 굳히기 및 전국 배포"),
                ("영국/유럽 펩시 글로벌 유통망 2차 확장", "2026-12-08", "HIGH", "해외 매출 비중 5% -> 15%로 확대되는 글로벌 퀀텀 점프 시동"),
            ],
            "ENPH": [
                ("3Q26 실적 발표 및 채널 재고 소진 완료", "2026-10-28", "CRITICAL", "재고 소진 종료 및 분기 매출 $400M+ 회복 가이던스 제시"),
                ("AI 데이터센터 800V DC 'IQ SST' 파일럿 발표", "2026-11-12", "CRITICAL", "빅테크 AI 데이터센터 전력 분산에너지(DER) 수주 공시로 리레이팅"),
                ("Enphase Air 스마트 관리 시스템 글로벌 출하", "2026-12-05", "HIGH", "가정용 토탈 에너지 매니지먼트 생태계 완성으로 설치당 매출 30% 증가"),
            ],
        }

        raw_events = events_map.get(sid, [])
        return [_make_event(name, t_str, impact, desc) for name, t_str, impact, desc in raw_events]

    # --------------------------------------------------------------------------
    # 3. 3-Tier Take-Profit Framework (TP1, TP2, TP3) (R2)
    # --------------------------------------------------------------------------

    @classmethod
    def get_take_profit(cls, stock_id: str, current_price: Optional[float] = None) -> TakeProfitConfig:
        """Return 3-Tier profit-taking configuration (TP1 Risk-Free, TP2 Normalization, TP3 Cycle Peak-Out)."""
        sid = stock_id.upper()

        if sid == "SK_HYNIX":
            is_krw = (
                current_price is not None
                and isinstance(current_price, (int, float))
                and math.isfinite(current_price)
                and current_price > 10000.0
            )
            if is_krw:
                return TakeProfitConfig(
                    tp1_price=3400000.0,
                    tp1_price_formatted="3,400,000원",
                    tp1_action="매수 원금 상당액(35%~50%) 분할 매도하여 포지션을 'Risk-Free' 상태로 전환",
                    tp1_gain_pct=100.0,
                    tp2_price=7000000.0,
                    tp2_price_formatted="7,000,000원",
                    tp2_action="잔여 비중의 50% 분할 익절 (시총 4,000조~5,000조 원, Fwd P/E 10~11배 본질가치 정상화)",
                    tp2_gain_pct=312.0,
                    tp2_valuation_target="시가총액 5,000조 원 / Fwd P/E 10.5x",
                    tp3_condition="전방 산업 빅테크 AI CapEx 축소 및 메모리 사이클 피크아웃 감지",
                    tp3_action="잔여 비중 100% 전량 청산",
                    tp3_trigger_indicators=[
                        "빅테크 AI CapEx 증가율 둔화 또는 축소 전환",
                        "DRAM/NAND 블렌디드 ASP 분기 대비 하락 전환",
                        "노무라 반도체 부족 지수(CSI) 90pt 하회",
                        "차세대 HBM 수주 경쟁 심화 및 마진 축소",
                    ],
                )
            return TakeProfitConfig(
                tp1_price=340.0,
                tp1_price_formatted="$340.00",
                tp1_action="매수 원금 상당액(35%~50%) 분할 매도하여 포지션을 'Risk-Free' 상태로 전환",
                tp1_gain_pct=100.4,
                tp2_price=700.0,
                tp2_price_formatted="$700.00",
                tp2_action="잔여 비중의 50% 분할 익절 (시총 4,000조~5,000조 원, Fwd P/E 10~11배 본질가치 정상화)",
                tp2_gain_pct=312.6,
                tp2_valuation_target="시가총액 5,000조 원 / Fwd P/E 10.5x",
                tp3_condition="전방 산업 빅테크 AI CapEx 축소 및 메모리 사이클 피크아웃 감지",
                tp3_action="잔여 비중 100% 전량 청산",
                tp3_trigger_indicators=[
                    "빅테크 AI CapEx 증가율 둔화 또는 축소 전환",
                    "DRAM/NAND 블렌디드 ASP 분기 대비 하락 전환",
                    "노무라 반도체 부족 지수(CSI) 90pt 하회",
                    "차세대 HBM 수주 경쟁 심화 및 마진 축소",
                ],
            )

        elif sid == "SK_SQUARE":
            return TakeProfitConfig(
                tp1_price=2180000.0,
                tp1_price_formatted="2,180,000원",
                tp1_action="38주 매도로 원금 8,284만 원(82,840,000 KRW) 100% 무위험(Risk-Free) 회수",
                tp1_gain_pct=105.7,
                tp2_price=5000000.0,
                tp2_price_formatted="5,000,000원",
                tp2_action="잔여 비중의 50% 분할 익절 (NAV 할인율 30% 정상화, 솔리다임 IPO 장부가 반영)",
                tp2_gain_pct=369.5,
                tp2_valuation_target="NAV 할인율 30% / 솔리다임 $150B 상장 가치 반영",
                tp3_condition="SK하이닉스 다운사이클 진입 및 지주사 디스카운트 고착 시 전량 청산",
                tp3_action="잔여 비중 100% 전량 청산",
                tp3_trigger_indicators=[
                    "SK하이닉스 다운사이클 진입 및 FCF 급감",
                    "지주사 지배구조 개편 지연 및 할인율 확대",
                    "자사주 소각 중단 및 주주환원율 축소",
                ],
            )

        elif sid == "UBER":
            return TakeProfitConfig(
                tp1_price=140.0,
                tp1_price_formatted="$140.00",
                tp1_action="원금 상당액 분할 매도하여 무위험 포지션 전환",
                tp1_gain_pct=95.8,
                tp2_price=210.0,
                tp2_price_formatted="$210.00",
                tp2_action="잔여 비중 50% 분할 익절 (Fwd P/E 30x 정상화, 자율주행 에셋라이트 플랫폼 독점)",
                tp2_gain_pct=193.7,
                tp2_valuation_target="12M Fwd P/E 30.0x / FCF $14B+",
                tp3_condition="로보택시 제조사 독자 배차망 확산 시 전량 청산",
                tp3_action="잔여 비중 100% 전량 청산",
                tp3_trigger_indicators=[
                    "완성차/자율주행 제조사(웨이모/테슬라)의 우버 배차망 독립 이탈",
                    "배차 수수료율(Take-rate) 정부 규제 상한 도입",
                    "운전자 인건비 급증 또는 법적 근로자 인정 판결",
                ],
            )

        elif sid == "MBLY":
            return TakeProfitConfig(
                tp1_price=15.0,
                tp1_price_formatted="$15.00",
                tp1_action="매수 원금 상당액 매도하여 무위험(Risk-Free) 포지션 전환",
                tp1_gain_pct=111.3,
                tp2_price=35.0,
                tp2_price_formatted="$35.00",
                tp2_action="잔여 비중 50% 분할 익절 (SuperVision 100만 대 SOP 및 2027 흑자 턴어라운드 본질가치)",
                tp2_gain_pct=393.0,
                tp2_valuation_target="SuperVision 100만 대 양산 / EV/Sales 8.5x",
                tp3_condition="중저가 전력효율 해자 붕괴 시 전량 청산",
                tp3_action="잔여 비중 100% 전량 청산",
                tp3_trigger_indicators=[
                    "엔비디아/퀄컴의 30W급 저전력 엣지 SoC 역전 출시",
                    "주요 OEM(포르쉐, 지커, 폭스바겐)의 EyeQ 채택 취소 및 자체 개발 선회",
                    "인텔의 지분 강제 블록딜 투매 재개",
                ],
            )

        elif sid == "FLNC":
            return TakeProfitConfig(
                tp1_price=32.0,
                tp1_price_formatted="$32.00",
                tp1_action="원금 전액 회수하여 Risk-Free 전환",
                tp1_gain_pct=97.5,
                tp2_price=65.0,
                tp2_price_formatted="$65.00",
                tp2_action="잔여 비중 50% 분할 익절 (20GWh 양산 안착, OPM 15% 본질가치 정상화)",
                tp2_gain_pct=301.2,
                tp2_valuation_target="20GWh 양산 / OPM 15% / EV/Sales 4.0x",
                tp3_condition="배터리 원가 급등 및 전력망 규제 시 전량 청산",
                tp3_action="잔여 비중 100% 전량 청산",
                tp3_trigger_indicators=[
                    "LFP 배터리 셀 가격 폭등 및 프로젝트 마진 적자 전환",
                    "미국 IRA 전력 인센티브 법안 폐지 또는 축소",
                    "빅테크 데이터센터 전력 증설 투자 중단",
                ],
            )

        elif sid == "UPST":
            return TakeProfitConfig(
                tp1_price=75.0,
                tp1_price_formatted="$75.00",
                tp1_action="원금 상당액 매도하여 무위험(Risk-Free) 포지션 전환",
                tp1_gain_pct=97.9,
                tp2_price=150.0,
                tp2_price_formatted="$150.00",
                tp2_action="잔여 비중 50% 분할 익절 (대출 취급액 $50B 돌파, 플랫폼 수수료 고마진 정상화)",
                tp2_gain_pct=295.8,
                tp2_valuation_target="대출 취급액 $50B / P/S 12.0x",
                tp3_condition="개인 신용 부실 및 연체율 급등 시 전량 청산",
                tp3_action="잔여 비중 100% 전량 청산",
                tp3_trigger_indicators=[
                    "미국 기준금리 긴급 재인상",
                    "30일+ 대출 연체율 6.0% 돌파",
                    "파트너 은행 자금 회수 및 자금 조달 스프레드 급등",
                ],
            )

        elif sid == "CELH":
            return TakeProfitConfig(
                tp1_price=55.0,
                tp1_price_formatted="$55.00",
                tp1_action="원금 상당액 매도하여 무위험 포지션 전환",
                tp1_gain_pct=101.1,
                tp2_price=110.0,
                tp2_price_formatted="$110.00",
                tp2_action="잔여 비중 50% 분할 익절 (북미 점유율 25% 달성, Monster 피어 P/E 30x 수렴)",
                tp2_gain_pct=302.2,
                tp2_valuation_target="북미 점유율 25% / 12M Fwd P/E 30.0x",
                tp3_condition="카테고리 성장 둔화 및 유통 분쟁 시 전량 청산",
                tp3_action="잔여 비중 100% 전량 청산",
                tp3_trigger_indicators=[
                    "에너지 드링크 카테고리 전체 성장률 역성장",
                    "펩시코와의 유통 계약 파기 또는 수수료율 인상 갈등",
                    "GPM 45% 붕괴 및 과도한 판촉비 출혈",
                ],
            )

        elif sid == "ENPH":
            return TakeProfitConfig(
                tp1_price=65.0,
                tp1_price_formatted="$65.00",
                tp1_action="원금 상당액 매도하여 Risk-Free 전환",
                tp1_gain_pct=104.1,
                tp2_price=140.0,
                tp2_price_formatted="$140.00",
                tp2_action="잔여 비중 50% 분할 익절 (AI 데이터센터 DER 매출 반영, 피어 P/E 28x 정상화)",
                tp2_gain_pct=339.6,
                tp2_valuation_target="AI 데이터센터 DER 수주 / Fwd P/E 35.0x",
                tp3_condition="태양광 보조금 폐지 및 인버터 결함 시 전량 청산",
                tp3_action="잔여 비중 100% 전량 청산",
                tp3_trigger_indicators=[
                    "미국 NEM 3.0 이상으로 주택용 태양광 보조금 완전 폐지",
                    "고전압 IQ SST 양산 실패 또는 대규모 리콜 발생",
                    "글로벌 금리 급등으로 주택용 태양광 설치 대출 마비",
                ],
            )

        else:
            raise ValueError(f"Unknown stock identifier: {stock_id}")

    # --------------------------------------------------------------------------
    # 4. 3-Condition Composite Trigger Evaluation Engine (R1)
    # --------------------------------------------------------------------------

    @classmethod
    def evaluate_trigger(
        cls,
        stock_id: str,
        current_price: float,
        price_formatted: Optional[str] = None,
        daily_change_pct: float = 0.0,
        volume: int = 0,
        date: str = "",
        avg_volume: Optional[int] = None,
        key_support: Optional[float] = None,
    ) -> CompositeTriggerResult:
        """Evaluate the 3-condition composite trigger to eliminate dead money.
        
        Condition 1: Safety Margin Band Entry (min_price <= current_price <= max_price)
        Condition 2: Confirmed Catalyst in 30~60 Days (0 <= days_remaining <= 60)
        Condition 3: Volume Wash-Out & Support Rebound (volume surge >= 1.4x + support defense + green rebound)
        """
        sid = stock_id.upper()
        band = cls.get_valuation_band(sid, current_price=current_price)
        tp = cls.get_take_profit(sid, current_price=current_price)
        catalysts = cls.get_catalysts(sid, as_of_date=date)

        # Price finite validation & positive validity check
        is_finite_price = (
            current_price is not None
            and isinstance(current_price, (int, float))
            and math.isfinite(current_price)
        )
        is_positive_price = is_finite_price and current_price > 0.0

        # Formatted price fallback
        if not price_formatted:
            if not is_finite_price:
                price_formatted = "N/A"
            elif band.currency == "KRW":
                price_formatted = f"{int(current_price):,}원"
            else:
                price_formatted = f"${current_price:,.2f}"

        # ----------------------------------------------------------------------
        # Condition 1: Safety Margin Band Entry
        # ----------------------------------------------------------------------
        # Stock enters safety margin if current_price is within [min_price, max_price]
        # or below max_price while defending the support floor.
        cond1_safety_margin = False
        if is_positive_price:
            if band.min_price <= current_price <= band.max_price:
                cond1_safety_margin = True
                cond1_detail = (
                    f"적극 매수 밴드 안착: {price_formatted} "
                    f"(기준 밴드: {band.min_price_formatted} ~ {band.max_price_formatted})"
                )
            elif current_price < band.min_price:
                if current_price >= band.key_support_price:
                    cond1_safety_margin = True
                    cond1_detail = (
                        f"극저점 안전마진 진입: {price_formatted} "
                        f"(하단 지지선 {band.key_support_formatted} 수호)"
                    )
                else:
                    cond1_safety_margin = False
                    cond1_detail = (
                        f"핵심 지지선 이탈 주의: {price_formatted} < {band.key_support_formatted}"
                    )
            else:
                cond1_safety_margin = False
                cond1_detail = (
                    f"매수 밴드 상단 초과: {price_formatted} > {band.max_price_formatted}"
                )
        else:
            cond1_detail = "가격 데이터 결손"

        # ----------------------------------------------------------------------
        # Condition 2: Confirmed Catalyst in 30~60 Days
        # ----------------------------------------------------------------------
        active_catalysts = [c for c in catalysts if c.days_remaining is not None and c.days_remaining >= 0 and c.is_confirmed]
        imminent_catalysts = [c for c in active_catalysts if 0 <= c.days_remaining <= 60]

        cond2_catalyst_imminent = len(imminent_catalysts) > 0
        min_days_remaining = (
            min((c.days_remaining for c in active_catalysts), default=999)
        )

        if cond2_catalyst_imminent:
            top_cat = min(imminent_catalysts, key=lambda c: c.days_remaining)
            cond2_detail = (
                f"확정 촉매 도래 임박: [{top_cat.name}] D-{top_cat.days_remaining}일 "
                f"({top_cat.target_date}, {top_cat.impact_level})"
            )
        else:
            if active_catalysts:
                cond2_detail = f"최단 촉매 D-{min_days_remaining}일 (60일 초과 대기 상태)"
            else:
                cond2_detail = "진행 중인 단기 확정 촉매 부재"

        # ----------------------------------------------------------------------
        # Condition 3: Volume Wash-Out & Support Rebound
        # ----------------------------------------------------------------------
        support_level = key_support if key_support is not None else band.key_support_price
        bench_vol = avg_volume if (avg_volume is not None and avg_volume > 0) else STOCK_BENCHMARK_20D_VOLUME.get(sid, 100000)

        price_holds_support = is_positive_price and (current_price >= (support_level * 0.99))
        is_green_rebound = daily_change_pct >= 0.0

        # Volume threshold: strictly require volume > 0 and vol_ratio >= 1.4 (no green bypass)
        vol_ratio = (volume / bench_vol) if bench_vol > 0 else 0.0
        is_volume_washout = (volume > 0 and vol_ratio >= MIN_WASHOUT_VOLUME_RATIO)

        cond3_volume_washout = (is_volume_washout and price_holds_support and is_green_rebound)

        if cond3_volume_washout:
            cond3_detail = (
                f"수급 바닥 확인: 지지선({band.key_support_formatted}) 방어 성공 및 "
                f"양봉 반등({daily_change_pct:+.2f}%, 거래량 배율 {vol_ratio:.1f}x)"
            )
        elif not price_holds_support:
            cond3_detail = f"수급 지지 실패: 현재가({price_formatted}) 지지선 하회"
        elif not is_green_rebound:
            cond3_detail = f"바닥 털기(Wash-out) 진행 중: 음봉/투매 출회({daily_change_pct:+.2f}%), 첫 양봉 대기"
        else:
            cond3_detail = f"거래량 바닥 탈출 수급 미확인 (현재 배율 {vol_ratio:.1f}x < {MIN_WASHOUT_VOLUME_RATIO:.1f}x)"

        # ----------------------------------------------------------------------
        # Composite Score (0~3) & Signals
        # ----------------------------------------------------------------------
        score = int(cond1_safety_margin) + int(cond2_catalyst_imminent) + int(cond3_volume_washout)

        # Risk-Reward Metrics
        if is_positive_price:
            if current_price >= support_level:
                downside_risk_pct = round((current_price - support_level) / current_price * 100.0, 2)
            else:
                breach_distance_pct = (support_level - current_price) / current_price * 100.0
                downside_risk_pct = round(breach_distance_pct + DEFAULT_SUPPORT_BREACH_PENALTY_PCT, 2)

            upside_tp1_pct = round((tp.tp1_price - current_price) / current_price * 100.0, 2)
            upside_tp2_pct = round((tp.tp2_price - current_price) / current_price * 100.0, 2)
            risk_reward_ratio = round(max(upside_tp1_pct, 0.0) / max(downside_risk_pct, 0.1), 2)
        else:
            downside_risk_pct = 0.0
            upside_tp1_pct = 0.0
            upside_tp2_pct = 0.0
            risk_reward_ratio = 0.0

        # Signal Synthesis
        if is_positive_price and current_price >= tp.tp1_price:
            signal = "TAKE_PROFIT"
            signal_label = "분할 익절 도달 (TP1 달성)"
            dead_money_risk = "LOW"
        elif cond1_safety_margin and cond2_catalyst_imminent and cond3_volume_washout:
            signal = "STRONG_BUY"
            signal_label = "강력 매수 (3대 복합 트리거 교차 충족)"
            dead_money_risk = "LOW"
        elif cond1_safety_margin and (cond2_catalyst_imminent or cond3_volume_washout):
            signal = "ACCUMULATE"
            signal_label = "분할 매집 (안전마진 + 촉매/수급 점등)"
            dead_money_risk = "MEDIUM"
        elif cond1_safety_margin:
            signal = "WATCH_CATALYST"
            signal_label = "촉매 대기 (안전마진 진입 / 자금 정체 위험)"
            dead_money_risk = "HIGH"
        else:
            signal = "HOLD"
            signal_label = "보유 관망 (밴드 상단 대기 / 추세 지속)"
            dead_money_risk = "LOW"

        return CompositeTriggerResult(
            stock_id=sid,
            date=date,
            current_price=current_price,
            current_price_formatted=price_formatted,
            cond1_safety_margin=cond1_safety_margin,
            cond1_detail=cond1_detail,
            cond2_catalyst_imminent=cond2_catalyst_imminent,
            cond2_days_remaining=min_days_remaining,
            cond2_detail=cond2_detail,
            cond3_volume_washout=cond3_volume_washout,
            cond3_detail=cond3_detail,
            composite_score=score,
            signal=signal,
            signal_label=signal_label,
            dead_money_risk=dead_money_risk,
            risk_reward_ratio=risk_reward_ratio,
            downside_risk_pct=downside_risk_pct,
            upside_tp1_pct=upside_tp1_pct,
            upside_tp2_pct=upside_tp2_pct,
        )

    # --------------------------------------------------------------------------
    # 5. Single Stock Full Evaluation Helper
    # --------------------------------------------------------------------------

    @classmethod
    def evaluate_stock(
        cls,
        stock_id: str,
        current_price: float,
        price_formatted: Optional[str] = None,
        daily_change_pct: float = 0.0,
        volume: int = 0,
        date: str = "",
        avg_volume: Optional[int] = None,
        key_support: Optional[float] = None,
    ) -> StockTimingEvaluation:
        """Produce full timing evaluation for a single stock."""
        sid = stock_id.upper()
        master = STOCK_MASTERS.get(getattr(StockSymbol, sid, None))
        stock_name = master.name_kr if master else sid
        ticker = master.ticker if master else sid

        band = cls.get_valuation_band(sid, current_price=current_price)
        catalysts = cls.get_catalysts(sid, as_of_date=date)
        tp = cls.get_take_profit(sid, current_price=current_price)
        trigger = cls.evaluate_trigger(
            stock_id=sid,
            current_price=current_price,
            price_formatted=price_formatted,
            daily_change_pct=daily_change_pct,
            volume=volume,
            date=date,
            avg_volume=avg_volume,
            key_support=key_support,
        )

        return StockTimingEvaluation(
            stock_id=sid,
            stock_name=stock_name,
            ticker=ticker,
            valuation_band=band,
            catalysts=catalysts,
            take_profit=tp,
            trigger=trigger,
        )

    # --------------------------------------------------------------------------
    # 6. Opportunity-Cost Stock Switching Engine (R4)
    # --------------------------------------------------------------------------

    @classmethod
    def evaluate_switching(
        cls,
        holding_stock_id: str,
        holding_shares: int,
        evaluations: Dict[str, StockTimingEvaluation],
        date: str = "",
    ) -> SwitchingRecommendation:
        """Evaluate stock switching opportunity vs core holding position."""
        holding_sid = holding_stock_id.upper()
        holding_eval = evaluations.get(holding_sid)

        if not holding_eval:
            # Fallback if holding evaluation missing
            ref_p = STOCK_REFERENCE_PRICES.get(holding_sid, 1065000.0)
            holding_eval = cls.evaluate_stock(holding_sid, ref_p, date=date)

        h_price = holding_eval.trigger.current_price
        h_rrr = holding_eval.trigger.risk_reward_ratio
        h_d_day = min((c.days_remaining for c in holding_eval.catalysts if c.days_remaining is not None and c.days_remaining >= 0), default=999)

        # Reverse Switching Warning Rule:
        # If holding stock has imminent critical catalyst (D-Day <= 20) and is within safety margin,
        # warn against emotional selling right before the breakout.
        is_reverse_warning = (
            h_d_day <= 20
            and h_price is not None
            and h_price < holding_eval.take_profit.tp1_price
            and (holding_eval.trigger.cond1_safety_margin or h_price >= holding_eval.valuation_band.key_support_price)
        )

        candidates: List[Dict[str, Any]] = []
        scenarios: List[Dict[str, Any]] = []
        top_candidate_id: Optional[str] = None

        for sid, ev in evaluations.items():
            if sid == holding_sid:
                continue

            c_rrr = ev.trigger.risk_reward_ratio
            c_d_day = min((c.days_remaining for c in ev.catalysts if c.days_remaining is not None and c.days_remaining >= 0), default=999)
            c_score = ev.trigger.composite_score

            rrr_ratio = round(c_rrr / max(h_rrr, 0.1), 2)
            catalyst_advantage = h_d_day - c_d_day  # positive if candidate catalyst arrives sooner

            # Determine switching tier based on composite score, catalyst velocity, and RRR
            if c_score == 3:
                if (rrr_ratio >= 1.3 and catalyst_advantage > 0) or (catalyst_advantage >= 30 and c_d_day <= 30):
                    tier = "STRONG_SWITCH"
                elif rrr_ratio >= 1.1 or catalyst_advantage > 0:
                    tier = "PARTIAL_SWITCH"
                else:
                    tier = "HOLD_CORE"
            elif c_score >= 2:
                if rrr_ratio >= 1.3 or (catalyst_advantage >= 30 and c_d_day <= 30):
                    tier = "PARTIAL_SWITCH"
                else:
                    tier = "HOLD_CORE"
            else:
                tier = "HOLD_CORE"

            candidates.append({
                "stockId": sid,
                "stockName": ev.stock_name,
                "tier": tier,
                "candidateRrr": round(c_rrr, 2),
                "holdingRrr": round(h_rrr, 2),
                "rrrRatio": rrr_ratio,
                "candidateDDay": c_d_day,
                "holdingDDay": h_d_day,
                "catalystAdvantageDays": catalyst_advantage,
                "compositeScore": c_score,
                "signal": ev.trigger.signal,
            })

        # Sort candidates: tier priority, then catalystAdvantageDays desc, then rrrRatio desc
        tier_weights = {"STRONG_SWITCH": 3, "PARTIAL_SWITCH": 2, "HOLD_CORE": 1}
        candidates.sort(
            key=lambda x: (tier_weights.get(x["tier"], 0), x["catalystAdvantageDays"], x["rrrRatio"]),
            reverse=True,
        )

        if candidates and candidates[0]["tier"] in ("STRONG_SWITCH", "PARTIAL_SWITCH"):
            top_candidate_id = candidates[0]["stockId"]

        # Reallocation Scenario Simulation: dynamic reallocated shares
        usd_rate = 1380.0
        h_currency = holding_eval.valuation_band.currency
        realloc_shares = max(1, min(15, holding_shares)) if holding_shares > 0 else 0

        if top_candidate_id and not is_reverse_warning and realloc_shares > 0:
            cand_eval = evaluations[top_candidate_id]
            cand_price = cand_eval.trigger.current_price

            if h_currency == "USD":
                freed_capital_krw = realloc_shares * h_price * usd_rate
            else:
                freed_capital_krw = realloc_shares * h_price

            is_cand_finite = (
                cand_price is not None
                and isinstance(cand_price, (int, float))
                and math.isfinite(cand_price)
                and cand_price > 0
            )

            if cand_eval.valuation_band.currency == "USD":
                cand_shares = int((freed_capital_krw / usd_rate) / cand_price) if is_cand_finite else 0
            else:
                cand_shares = int(freed_capital_krw / cand_price) if is_cand_finite else 0

            freed_cap_str = (
                f"약 {int(freed_capital_krw / 10000):,}만 원"
                if (isinstance(freed_capital_krw, (int, float)) and math.isfinite(freed_capital_krw) and freed_capital_krw >= 0)
                else "평가 불가"
            )

            scenarios.append({
                "title": f"전술적 교체 매매: {holding_eval.stock_name} {realloc_shares}주 → {cand_eval.stock_name} {cand_shares:,}주",
                "freedCapital": freed_cap_str,
                "candidateShares": f"{cand_shares:,}주",
                "expectedGainHoldingTp1": f"{holding_eval.trigger.upside_tp1_pct:+.1f}%",
                "expectedGainCandidateTp1": f"{cand_eval.trigger.upside_tp1_pct:+.1f}%",
                "catalystComparison": f"{holding_eval.stock_name} D-{h_d_day} vs {cand_eval.stock_name} D-{min((c.days_remaining for c in cand_eval.catalysts if c.days_remaining is not None and c.days_remaining >= 0), default=999)}",
            })

        if is_reverse_warning:
            status = "REVERSE_SWITCH_WARNING"
            summary = (
                f"{holding_eval.stock_name} {holding_shares}주 코어 보유 엄수 — 자체 확정 촉매 D-{h_d_day}일 "
                f"임박으로 역(逆)스위칭 리스크 경고 (매도 금지 및 밸류업 결실 향유 권고)."
            )
        elif top_candidate_id:
            status = "SWITCH_OPPORTUNITY"
            top_c = evaluations[top_candidate_id]
            summary = (
                f"{top_c.stock_name} 스위칭 기회 포착 — 3대 복합 트리거 및 기대 손익비(RRR {top_c.trigger.risk_reward_ratio:.1f}) "
                f"우위에 따른 전술적 부분 교체 권고."
            )
        else:
            status = "HOLD_CORE"
            summary = f"{holding_eval.stock_name} {holding_shares}주 코어 과비중 유지 — 현재 교체 매매 실익 제한적."

        if h_price is None or not (isinstance(h_price, (int, float)) and math.isfinite(h_price)):
            eval_amount_str = "평가 불가 (가격 데이터 결손)"
        elif h_price <= 0.0:
            eval_amount_str = "$0.00" if h_currency == "USD" else "0원"
        elif h_currency == "USD":
            holding_eval_usd = h_price * holding_shares
            holding_eval_krw = holding_eval_usd * usd_rate
            eval_amount_str = f"${holding_eval_usd:,.2f} (약 {int(holding_eval_krw / 10000):,}만 원)"
        else:
            holding_eval_krw = h_price * holding_shares
            eval_amount_str = f"약 {int(holding_eval_krw / 10000):,}만 원"

        return SwitchingRecommendation(
            holding_stock_id=holding_sid,
            holding_shares=holding_shares,
            holding_price=h_price,
            holding_eval_amount=eval_amount_str,
            holding_rrr=round(h_rrr, 2),
            holding_catalyst_d_day=h_d_day,
            status=status,
            summary=summary,
            top_candidate_id=top_candidate_id,
            candidates=candidates,
            scenarios=scenarios,
        )

    # --------------------------------------------------------------------------
    # 7. Continuous Daily Pipeline Master Evaluator (R5)
    # --------------------------------------------------------------------------

    @classmethod
    def evaluate_daily_timing(
        cls,
        market_data: DailyMarketData,
        portfolio: Optional[Dict[str, Any]] = None,
        as_of_date: Optional[str] = None,
    ) -> DailyTimingSnapshot:
        """Master entrypoint executing the timing pipeline for all 8 stocks across DailyMarketData."""
        eval_date = as_of_date or market_data.date or dt_date.today().strftime("%Y-%m-%d")
        timestamp = datetime.now().isoformat()

        # Parse portfolio holding stock and shares
        holding_stock_id = "SK_SQUARE"
        holding_shares = 76

        if portfolio:
            if "holdingStock" in portfolio:
                holding_stock_id = portfolio["holdingStock"]
            if "shares" in portfolio:
                try:
                    holding_shares = int(portfolio["shares"])
                except Exception:
                    pass
            elif "holdings" in portfolio and isinstance(portfolio["holdings"], dict):
                sq_holding = portfolio["holdings"].get("SK_SQUARE")
                if isinstance(sq_holding, dict) and "shares" in sq_holding:
                    holding_shares = int(sq_holding["shares"])

        evaluations: Dict[str, StockTimingEvaluation] = {}

        # Evaluate all 8 monitored canonical stocks
        canonical_stocks = [
            "SK_HYNIX", "SK_SQUARE", "UBER", "MBLY", "FLNC", "UPST", "CELH", "ENPH"
        ]

        for sid in canonical_stocks:
            fact_sheet = market_data.stocks.get(sid)
            if fact_sheet and fact_sheet.metrics:
                m = fact_sheet.metrics
                p = m.close_price if m.close_price is not None else STOCK_REFERENCE_PRICES.get(sid, 0.0)
                p_fmt = m.close_price_formatted or m.price
                chg = m.change_percent if m.change_percent is not None else 0.0
                vol = m.volume if m.volume is not None else 0
            else:
                p = STOCK_REFERENCE_PRICES.get(sid, 0.0)
                p_fmt = None
                chg = 0.0
                vol = 0

            eval_res = cls.evaluate_stock(
                stock_id=sid,
                current_price=p,
                price_formatted=p_fmt,
                daily_change_pct=chg,
                volume=vol,
                date=eval_date,
            )
            evaluations[sid] = eval_res

        # Evaluate switching opportunities
        switching_res = cls.evaluate_switching(
            holding_stock_id=holding_stock_id,
            holding_shares=holding_shares,
            evaluations=evaluations,
            date=eval_date,
        )

        # Generate holistic Fund Manager AI Proposal
        proposal_res = cls.generate_manager_proposal(
            evaluations=evaluations,
            switching=switching_res,
            portfolio=portfolio,
            date=eval_date,
            market_data=market_data,
        )

        return DailyTimingSnapshot(
            date=eval_date,
            timestamp=timestamp,
            stocks=evaluations,
            switching=switching_res,
            manager_proposal=proposal_res,
        )

    # --------------------------------------------------------------------------
    # 8. Fund Manager AI Persona Reasoning & Execution Proposal Engine (R1)
    # --------------------------------------------------------------------------

    @classmethod
    def generate_manager_proposal(
        cls,
        evaluations: Optional[Dict[str, StockTimingEvaluation]] = None,
        switching: Optional[SwitchingRecommendation] = None,
        portfolio: Optional[Dict[str, Any]] = None,
        date: Optional[str] = None,
        market_data: Optional[DailyMarketData] = None,
        **kwargs: Any,
    ) -> FundManagerProposal:
        """Synthesizes Benjamin Graham intrinsic value floor + Jesse Livermore timing trigger

        into an actionable holistic investment proposal for the user's SK Square 76 shares position
        and 8 monitored watchlist stocks.
        """
        eval_date = date or (market_data.date if market_data else None) or dt_date.today().strftime("%Y-%m-%d")
        timestamp = datetime.now().isoformat()

        canonical_stocks = [
            "SK_HYNIX", "SK_SQUARE", "UBER", "MBLY", "FLNC", "UPST", "CELH", "ENPH"
        ]

        # 1. Ensure evaluations exist for all 8 stocks
        evals: Dict[str, StockTimingEvaluation] = {}
        if evaluations:
            evals = dict(evaluations)
        else:
            for sid in canonical_stocks:
                p = STOCK_REFERENCE_PRICES.get(sid, 0.0)
                vol = STOCK_BENCHMARK_20D_VOLUME.get(sid, 1000000)
                if market_data and sid in market_data.stocks:
                    fs = market_data.stocks[sid]
                    if fs.metrics:
                        p = fs.metrics.close_price if fs.metrics.close_price is not None else p
                        vol = fs.metrics.volume if fs.metrics.volume is not None else vol
                evals[sid] = cls.evaluate_stock(
                    stock_id=sid,
                    current_price=p,
                    daily_change_pct=0.0,
                    volume=vol,
                    date=eval_date,
                )

        # 2. Extract portfolio parameters for core holding (SK Square)
        holding_sid = "SK_SQUARE"
        shares = 76
        principal_krw = 82840000
        avg_cost_krw = 1090000
        tp1_target_price = 2180000.0
        tp1_shares_to_sell = 38
        tp1_recovered_amount = 82840000

        if portfolio:
            if "holdingStock" in portfolio:
                holding_sid = str(portfolio["holdingStock"])
            if "shares" in portfolio:
                try:
                    shares = int(portfolio["shares"])
                except Exception:
                    pass
            if "principal" in portfolio or "principalKrw" in portfolio:
                try:
                    val = portfolio.get("principal") if portfolio.get("principal") is not None else portfolio.get("principalKrw")
                    principal_krw = int(val) if val is not None else principal_krw
                except Exception:
                    pass
            if "avgCost" in portfolio or "avgCostKrw" in portfolio:
                try:
                    val = portfolio.get("avgCost") if portfolio.get("avgCost") is not None else portfolio.get("avgCostKrw")
                    avg_cost_krw = int(val) if val is not None else avg_cost_krw
                except Exception:
                    pass
            elif principal_krw > 0 and shares > 0:
                avg_cost_krw = int(round(principal_krw / shares))

        sq_eval = evals.get(holding_sid)

        # Determine current price
        # If explicitly passed in portfolio or kwargs, use that.
        # Otherwise, if holding is default 76 shares SK Square and no live market_data price override,
        # anchor to authoritative 105만 원 (1,050,000 KRW).
        if portfolio and ("currentPrice" in portfolio or "current_price" in portfolio):
            val = portfolio.get("currentPrice") if portfolio.get("currentPrice") is not None else portfolio.get("current_price")
            sq_price = float(val) if val is not None else 1050000.0
        elif "current_price" in kwargs:
            sq_price = float(kwargs["current_price"])
        elif sq_eval and sq_eval.trigger and sq_eval.trigger.current_price is not None and sq_eval.trigger.current_price != STOCK_REFERENCE_PRICES.get("SK_SQUARE"):
            sq_price = float(sq_eval.trigger.current_price)
        else:
            sq_price = 1050000.0

        current_valuation_krw = int(round(shares * sq_price))
        pnl_amount_krw = current_valuation_krw - principal_krw
        pnl_rate_pct = round((pnl_amount_krw / principal_krw) * 100.0, 2) if principal_krw > 0 else 0.0
        tp1_progress_pct = round((sq_price / tp1_target_price) * 100.0, 1) if tp1_target_price > 0 else 0.0

        # Holding nearest catalyst D-Day
        sq_cats = sq_eval.catalysts if sq_eval else cls.get_catalysts(holding_sid, eval_date)
        valid_cats = [c for c in sq_cats if c.days_remaining is not None and c.days_remaining >= 0]
        h_d_day = min((c.days_remaining for c in valid_cats), default=999)

        # Status phase determination
        if sq_price >= tp1_target_price:
            status_phase = "TP1_REACHED_EXECUTE_SELL_38"
        elif h_d_day <= 20 and sq_price < tp1_target_price and (sq_price >= (sq_eval.valuation_band.key_support_price if sq_eval else 980000.0)):
            status_phase = "CATALYST_IMMINENT_STRICT_HOLD"
        elif sq_price <= 1120000.0:
            status_phase = "ACCUMULATION_MARGIN_AND_COUNTDOWN"
        else:
            status_phase = "HOLD_RIDE_TO_TP1"

        core_holding = PortfolioDiagnostic(
            stock_id=holding_sid,
            stock_name=STOCK_MASTERS[holding_sid].name_kr if holding_sid in STOCK_MASTERS else "SK스퀘어",
            shares=shares,
            principal_krw=principal_krw,
            avg_cost_krw=avg_cost_krw,
            current_price=sq_price,
            current_price_formatted=f"{int(sq_price):,}원" if sq_price >= 1000 else f"${sq_price:.2f}",
            current_valuation_krw=current_valuation_krw,
            pnl_amount_krw=pnl_amount_krw,
            pnl_rate_pct=pnl_rate_pct,
            tp1_target_price=tp1_target_price,
            tp1_target_formatted=f"{int(tp1_target_price):,}원",
            tp1_shares_to_sell=tp1_shares_to_sell,
            tp1_recovered_amount=tp1_recovered_amount,
            tp1_recovered_formatted=f"{tp1_recovered_amount // 10000:,}만 원",
            tp1_progress_pct=tp1_progress_pct,
            status_phase=status_phase,
            recovery_roadmap=(
                f"1~2년 내 TP1({int(tp1_target_price // 10000):,}만 원) 도달 시 {tp1_shares_to_sell}주 매도로 "
                f"원금 {principal_krw // 10000:,}만 원({principal_krw:,} KRW) 100% 무위험(Risk-Free) 회수. "
                f"잔여 {shares - tp1_shares_to_sell}주는 취득원가 0원 상태로 TP2(500만 원) 및 TP3 사이클 완주."
            ),
        )

        # 3. Ensure switching recommendation exists
        switching_rec = switching or cls.evaluate_switching(
            holding_stock_id=holding_sid,
            holding_shares=shares,
            evaluations=evals,
            date=eval_date,
        )

        # 4. Calculate 8-Stock Time-to-100% Ranking
        time_to_100_ranking: List[Dict[str, Any]] = []
        for sid in canonical_stocks:
            if sid not in evals:
                continue
            ev = evals[sid]
            tr = ev.trigger
            imminent_cats = [c for c in ev.catalysts if c.days_remaining is not None and c.days_remaining >= 0]
            cat_d_day = min((c.days_remaining for c in imminent_cats), default=999)

            # Speed score synthesis:
            # - Composite trigger score: max 90 pts (3 * 30)
            # - Catalyst urgency (0 <= D <= 60): max 100 pts (100 - min_d_day)
            # - Risk-Reward Ratio: up to 50 pts (min(50, rrr * 2.0))
            # - TP1 Upside: up to 30 pts (min(30, upside * 0.2))
            cat_score = max(0, 100 - cat_d_day) if cat_d_day <= 100 else 0
            rrr_score = min(50.0, max(0.0, tr.risk_reward_ratio * 2.0))
            upside_score = min(30.0, max(0.0, tr.upside_tp1_pct * 0.2))
            base_speed = (tr.composite_score * 30.0) + cat_score + rrr_score + upside_score

            # Dead money penalty
            if tr.dead_money_risk == "HIGH":
                base_speed = max(10.0, base_speed - 40.0)

            speed_score = round(base_speed, 1)

            if speed_score >= 140.0:
                rating = "FAST"
                est_time = "6~12개월"
            elif speed_score >= 85.0:
                rating = "MODERATE"
                est_time = "1~2년"
            else:
                rating = "SLOW"
                est_time = "2년 이상 / 촉매 대기"

            time_to_100_ranking.append({
                "stockId": sid,
                "stockName": ev.stock_name,
                "ticker": ev.ticker,
                "currentPrice": tr.current_price,
                "currentPriceFormatted": tr.current_price_formatted,
                "tp1Target": ev.take_profit.tp1_price,
                "tp1TargetFormatted": ev.take_profit.tp1_price_formatted,
                "upsideTp1": tr.upside_tp1_pct,
                "downsideRisk": tr.downside_risk_pct,
                "riskRewardRatio": tr.risk_reward_ratio,
                "compositeScore": tr.composite_score,
                "nearestCatalystDDay": cat_d_day,
                "deadMoneyRisk": tr.dead_money_risk,
                "speedScore": speed_score,
                "timeTo100Rating": rating,
                "estimatedTime": est_time,
                "signal": tr.signal,
            })

        time_to_100_ranking.sort(key=lambda x: x["speedScore"], reverse=True)
        for idx, item in enumerate(time_to_100_ranking):
            item["rank"] = idx + 1

        # 5. Determine Tactical Action & Reverse Switching Rule
        # Reverse switching defense rule:
        # If holding stock has imminent confirmed catalyst (D <= 20) and is within safety margin or defends key support,
        # switching is strictly prohibited!
        is_reverse_warning = (
            h_d_day <= 20
            and sq_price < tp1_target_price
            and (sq_price >= (sq_eval.valuation_band.key_support_price if sq_eval else 980000.0))
        )

        switching_proposal: Optional[SwitchingActionScenario] = None

        if sq_price >= tp1_target_price:
            tactical_action = "TAKE_PROFIT_TP1"
            action_headline = "🎯 TP1(218만 원) 달성! SK스퀘어 38주 분할 매도로 원금 8,284만 원 100% 무위험 회수 실행"
            executive_summary = (
                "SK스퀘어가 1차 목표가 218만 원에 도달했습니다. 사전 정의된 로드맵에 따라 정확히 38주를 매도하여 "
                "매수 원금 8,284만 원(82,840,000 KRW)을 100.0% 전액 현금 회수하십시오. "
                "원금 전액 회수 후 시장에 남은 38주는 취득원가 0원의 완전 무위험(Risk-Free) 하우스머니로 전환되며, "
                "2차 목표가(TP2 500만 원, NAV 정상화 및 솔리다임 가치 반영)까지 심리적 동요 없이 끝까지 완주합니다."
            )
        elif is_reverse_warning:
            tactical_action = "REVERSE_SWITCH_WARNING"
            action_headline = f"🛡️ 역(逆)스위칭 엄금 경고: SK스퀘어 자체 확정 촉매 D-{h_d_day}일 임박 — 76주 코어 홀딩 결사 사수"
            executive_summary = (
                f"보유종목 SK스퀘어의 자체 확정 촉매(자사주 2,000억 소각 완료 및 하이닉스 실적 배당 결의)가 D-{h_d_day}일로 임박했습니다. "
                "이 시점에서 타 종목의 단기 상승률이나 모멘텀에 유혹되어 매도할 경우, 주가 급등 분기점 직전 물량을 털리는 "
                "전형적인 역(逆)스위칭 함정에 빠질 수 있습니다. 76주 전량 매도를 엄격히 금지하고 코어 과비중을 결사 사수하십시오."
            )
        elif switching_rec.status == "SWITCH_OPPORTUNITY" and switching_rec.top_candidate_id:
            top_cand_id = switching_rec.top_candidate_id
            top_cand = evals[top_cand_id]
            tactical_action = "TACTICAL_SWITCH"
            action_headline = f"⚡ 전술적 부분 스위칭 제안: {top_cand.stock_name} 손익비·촉매 도달 속도 우위에 따른 일부 교체 매매"
            executive_summary = (
                f"{top_cand.stock_name}이(가) 확정 촉매 D-{top_cand.trigger.cond2_days_remaining}일 및 복합 트리거 우위로 "
                f"1~2년 100%+ 도달 시기(Time-to-100%)에서 보유종목을 앞서고 있습니다. "
                "코어 76주 중 5~10주(소액) 전술적 부분 스위칭을 통해 포트폴리오 수익률 가속화를 검토할 수 있습니다."
            )
            # Calculate tactical switching scenario parameters robustly
            sell_shares = 10
            freed_cap = int(round(sell_shares * sq_price))
            cand_price = top_cand.trigger.current_price
            usd_rate = 1380.0
            if top_cand.valuation_band.currency == "USD":
                cand_buy_shares = int((freed_cap / usd_rate) / cand_price) if cand_price > 0 else 0
            else:
                cand_buy_shares = int(freed_cap / cand_price) if cand_price > 0 else 0

            switching_proposal = SwitchingActionScenario(
                candidate_id=top_cand_id,
                candidate_name=top_cand.stock_name,
                action_type="TACTICAL_SWITCH",
                shares_to_sell=sell_shares,
                freed_capital_krw=freed_cap,
                candidate_shares_to_buy=cand_buy_shares,
                holding_tp1_upside_pct=round(sq_eval.trigger.upside_tp1_pct, 1) if sq_eval else 107.6,
                candidate_tp1_upside_pct=round(top_cand.trigger.upside_tp1_pct, 1),
                reason=f"{top_cand.stock_name} 촉매 D-{top_cand.trigger.cond2_days_remaining}일 및 RRR {top_cand.trigger.risk_reward_ratio:.1f} 우위",
            )
        else:
            tactical_action = "HOLD_CORE"
            action_headline = "💎 SK스퀘어 76주 코어 과비중 유지 — 저평가 안전마진 속 Big Wave 1차 목표(TP1) 대기"
            executive_summary = (
                "SK스퀘어는 역사적 NAV 할인율 43%~55% 바닥권에서 안전마진을 완벽히 확보하고 있습니다. "
                "잦은 뇌동매매를 엄격히 차단하고, 확정 촉매 클러스터 D-Day 카운트다운과 함께 "
                "1~2년 내 TP1(218만 원, 38주 매도로 원금 8,284만 원 전액 무위험 회수) 도달까지 우직하게 코어 포지션을 완주합니다."
            )

        # 6. Four-Pillar Deep Reasoning Synthesis
        reasoning_pillars = {
            "valuation_thesis": (
                "SK스퀘어는 주당 NAV(순자산가치) 1,855,000원 대비 할인율 43%~55%의 역사적 극저평가 구간에 위치함. "
                "자회사 SK하이닉스의 2027년 HBM 완판 및 사상 최대 실적, 비상장 자회사 솔리다임(Solidigm)의 150조 원 상장 가치 및 eSSD 흑자전환 가치가 "
                "시가총액에 전혀 반영되지 않은 극단적 저평가 상태로 벤저민 그레이엄식 본질가치 안전마진(하방 98만 원 지지선)이 완벽히 구축되어 있음."
            ),
            "catalyst_timing": (
                f"제시 리버모어의 시간 축 타이밍 이론에 따라 자금 정체(Dead Money)를 회피할 확정 촉매 클러스터 도래 중. "
                f"SK스퀘어 자체 자사주 2,000억 소각 및 지분율 21% 확정(D-{h_d_day if h_d_day < 999 else 10})과 3Q 결산 배당금 유입(D-29), "
                "SK하이닉스 3Q26 실적 발표 및 배당 결의(D-15) 등 30~60일 이내 핵심 모멘텀이 집중되어 주가 탄력의 변곡점에 진입함."
            ),
            "volume_supply_dynamics": (
                "수급적 측면에서 나스닥 ADR 상장 및 락업 해제 충격 매물이 대량 거래량 폭증과 함께 흡수(Wash-out)되었으며, "
                "핵심 마디 가격 지지선 방어 후 반등 양봉을 시현함. 악성 대기 매물이 소화된 상태로 저항선 상향 돌파 시 호가 공백을 통한 가파른 시세 분출이 전개될 수 있는 수급 바닥형 차트 구조를 형성함."
            ),
            "risk_reward_assessment": (
                f"현재가({int(sq_price // 10000):,}만 원) 기준 하방 지지선(98만 원)까지의 최대 다운사이드는 -6.7%에 불과한 반면, "
                "1~2년 1차 목표가(TP1 218만 원)까지의 업사이드는 +107.6%로 손익비(Risk-Reward Ratio) 15.0+의 압도적 우위 구간. "
                "TP1 도달 시 38주 분할 매도로 매수 원금 8,284만 원(82,840,000 KRW)을 100% 무위험 회수하고 잔여 38주로 TP2(500만 원) 및 TP3 Big Wave를 완주하는 무결점 포트폴리오 관리 공식이 적용됨."
            ),
        }

        # 7. Risk Management Alerts
        risk_warnings: List[RiskManagementAlert] = []

        # Reverse Switching Alert
        if is_reverse_warning:
            risk_warnings.append(RiskManagementAlert(
                alert_type="REVERSE_SWITCH_DEFENSE",
                severity="CRITICAL",
                stock_id=holding_sid,
                message=f"{STOCK_MASTERS[holding_sid].name_kr} 자체 확정 촉매 D-{h_d_day}일 이내 임박으로 역스위칭 발생 위험 최고조.",
                action_guideline="타 종목으로의 교체 매매를 엄격히 금지하고 76주 전량 홀딩 유지. 촉매 직전 물량 털림 방지.",
            ))
        else:
            risk_warnings.append(RiskManagementAlert(
                alert_type="REVERSE_SWITCH_DEFENSE",
                severity="INFO",
                stock_id=holding_sid,
                message=f"{STOCK_MASTERS[holding_sid].name_kr} 확정 촉매 D-{h_d_day}일 대기 중. 역스위칭 방지 가드레일 활성화.",
                action_guideline="촉매 D-20 진입 전까지는 후보 종목과의 상대 손익비 상시 비교 허용.",
            ))

        # Dead Money Alerts across 8 stocks
        for sid in canonical_stocks:
            ev = evals.get(sid)
            if ev and ev.trigger.dead_money_risk == "HIGH":
                risk_warnings.append(RiskManagementAlert(
                    alert_type="DEAD_MONEY",
                    severity="WARNING",
                    stock_id=sid,
                    message=f"{ev.stock_name}은(는) 안전마진 밴드 진입에도 불구하고 60일 내 확정 촉매 부재로 자금 정체(Dead Money) 위험 높음.",
                    action_guideline="선취매를 자제하고 확정 촉매 공시 또는 거래량 1.4배 폭증 수급 바닥 확인 시까지 관망 권고.",
                ))

        # Support defense alert
        if sq_eval and sq_price < sq_eval.valuation_band.key_support_price:
            risk_warnings.append(RiskManagementAlert(
                alert_type="SUPPORT_DEFENSE",
                severity="CRITICAL",
                stock_id=holding_sid,
                message=f"핵심 하방 지지선({sq_eval.valuation_band.key_support_formatted}) 일시 이탈. 다운사이드 리스크 모니터링 요망.",
                action_guideline="지지선 회복 여부 확인 전까지 추가 매수 보류.",
            ))

        # 8. Dynamic Journal Markdown Generation
        ranking_table_rows = []
        for item in time_to_100_ranking:
            ranking_table_rows.append(
                f"| {item['rank']} | **{item['stockName']}** ({item['ticker']}) | {item['currentPriceFormatted']} | "
                f"{item['tp1TargetFormatted']} | +{item['upsideTp1']:.1f}% | D-{item['nearestCatalystDDay']} | "
                f"{item['compositeScore']}/3 | {item['riskRewardRatio']:.1f} | **{item['speedScore']}** | {item['timeTo100Rating']} ({item['estimatedTime']}) |"
            )
        ranking_table_str = "\n".join(ranking_table_rows)

        alert_bullets = "\n".join([f"- **[{w.severity}] {w.alert_type}** ({w.stock_id}): {w.message} → *{w.action_guideline}*" for w in risk_warnings])

        tex_share = f"{tp1_shares_to_sell}\\text{{주}}"
        tex_target = f"{int(tp1_target_price):,}\\text{{원}}"
        tex_val = f"{tp1_recovered_amount:,}\\text{{원 ({tp1_recovered_amount // 10000:,}만 원)}}"
        tex_recovery_line = f"$${tex_share} \\times {tex_target} = \\mathbf{{{tex_val}}}\\; (100.0\\%\\text{{ 원금 전액 회수}})$$"

        journal_markdown = f"""# 🤖 가치투자 + 타이밍 천재 수석 펀드매니저 AI 일일 전략 제안 & 포트폴리오 진단

**기준일자**: {eval_date} | **투자 시계**: 1~2년 (Big Wave & 100%+ 수익률 추구)  
**핵심 목표**: TP1(218만 원) 38주 매도로 매수 원금 8,284만 원 100% 무위험(Risk-Free) 회수

---

## 1. 📌 코어 보유자산 실시간 정밀 진단 (SK스퀘어 76주)
- **보유 수량**: {shares}주 (포트폴리오 코어 자산)
- **매수 원금**: {principal_krw // 10000:,}만 원 ({principal_krw:,} KRW) | **매수 평단가**: {avg_cost_krw // 10000:,}만 원 ({avg_cost_krw:,} KRW)
- **현재 평가액**: {current_valuation_krw // 10000:,}만 원 ({current_valuation_krw:,} KRW, 현재가 {int(sq_price):,}원 기준) | **평가 손익**: {pnl_amount_krw // 10000:,}만 원 ({pnl_amount_krw:,} KRW, {pnl_rate_pct:+.2f}%)
- **🎯 1차 목표(TP1) 무위험 회수 로드맵**:
  - 목표 주가: **{int(tp1_target_price):,}원 (218만 원)** (+{((tp1_target_price - sq_price) / sq_price * 100.0 if sq_price > 0 else 0.0):.1f}% 도달 구간)
  - 실행 행동: **{tp1_shares_to_sell}주 분할 매도** (전체 {shares}주의 정확히 50%)
  - 회수 금액: {tex_recovery_line}
  - 무위험 전환: 잔여 {shares - tp1_shares_to_sell}주는 취득원가 0원의 **완전 무위험(Risk-Free) 하우스머니**로 전환되어 2차 목표가(TP2 500만 원, 솔리다임 가치 반영)까지 지속 완주.
  - 현재 TP1 진행률: **{tp1_progress_pct:.1f}%** (카운트다운 지속 중)

---

## 2. ⚡ 펀드매니저 핵심 전술 판단 & 실행 지침
- **전술적 권고**: `{tactical_action}`
- **핵심 헤드라인**: **{action_headline}**
- **매니저 브리핑**:
  {executive_summary}

---

## 3. 🧠 4대 심층 추론 필러 (그레이엄 본질가치 앵커 + 리버모어 촉매 타이밍)
1. **[본질가치 앵커 (Graham Value Floor)]**: {reasoning_pillars['valuation_thesis']}
2. **[촉매 타이밍 (Livermore Catalyst Trigger)]**: {reasoning_pillars['catalyst_timing']}
3. **[수급 워시아웃 (Supply & Wash-Out Dynamics)]**: {reasoning_pillars['volume_supply_dynamics']}
4. **[손익비 및 시간우위 (Risk-Reward & Time-to-100%)]**: {reasoning_pillars['risk_reward_assessment']}

---

## 4. 📊 8대 관심종목 1~2년 100%+ 도달 속도(Time-to-100%) 비교 매트릭스
| 순위 | 종목명 (티커) | 현재가 | TP1 목표가 | TP1 업사이드 | 최근 촉매 D-Day | 복합 스코어 | RRR | 속도 평점 | 도달 속도 판정 |
|---|---|---|---|---|---|---|---|---|---|
{ranking_table_str}

---

## 5. 🛡️ 리스크 관리 경고 (Dead Money 회피 & 역스위칭 방어)
{alert_bullets}
"""

        return FundManagerProposal(
            date=eval_date,
            timestamp=timestamp,
            manager_persona="가치투자 + 타이밍 천재 수석 펀드매니저 AI",
            investment_horizon="1~2년 (Big Wave & 100%+ 수익률 추구)",
            target_objective="TP1(218만 원) 38주 매도로 매수 원금 8,284만 원 100% 무위험 회수",
            core_holding=core_holding,
            tactical_action=tactical_action,
            action_headline=action_headline,
            executive_summary=executive_summary,
            reasoning_pillars=reasoning_pillars,
            time_to_100_ranking=time_to_100_ranking,
            switching_proposal=switching_proposal,
            risk_warnings=risk_warnings,
            journal_markdown=journal_markdown.strip(),
        )
