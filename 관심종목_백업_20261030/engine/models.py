"""Structured dataclass models for Multi-Stock Investment Processing Engine.

Supports 8 watchlist stocks:
- UBER (Uber Technologies, Inc. - NYSE)
- SK_HYNIX (SK Hynix Inc. - KRX:000660 / SKHY)
- SK_SQUARE (SK Square Co., Ltd. - KRX:402340)
- MBLY (Mobileye Global Inc. - NASDAQ)
- FLNC (Fluence Energy, Inc. - NASDAQ)
- UPST (Upstart Holdings, Inc. - NASDAQ)
- CELH (Celsius Holdings, Inc. - NASDAQ)
- ENPH (Enphase Energy, Inc. - NASDAQ)
"""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional


class StockSymbol(str, Enum):
    """Canonical identifier for the 8 monitored watchlist stocks."""
    UBER = "UBER"
    SK_HYNIX = "SK_HYNIX"
    SK_SQUARE = "SK_SQUARE"
    MBLY = "MBLY"
    FLNC = "FLNC"
    UPST = "UPST"
    CELH = "CELH"
    ENPH = "ENPH"


@dataclass(frozen=True)
class StockMaster:
    """Immutable master definition for a watchlist stock."""
    stock_id: StockSymbol
    name_kr: str
    name_en: str
    ticker: str
    market: str
    currency: str
    category: str
    badge_color: str
    executive_keywords: List[str] = field(default_factory=list)
    asset_keywords: List[str] = field(default_factory=list)


STOCK_MASTERS: Dict[StockSymbol, StockMaster] = {
    StockSymbol.UBER: StockMaster(
        stock_id=StockSymbol.UBER,
        name_kr="우버",
        name_en="Uber Technologies, Inc.",
        ticker="UBER",
        market="NYSE",
        currency="USD",
        category="모빌리티/플랫폼",
        badge_color="emerald",
        executive_keywords=["다라 코스로샤히", "Dara Khosrowshahi", "빌 걸리", "Bill Gurley", "브래드 거스너", "Brad Gerstner"],
        asset_keywords=["로보택시", "웨이모", "Waymo", "딜리버리 히어로", "Delivery Hero", "도어대시", "우버이츠", "플릿 배차"]
    ),
    StockSymbol.SK_HYNIX: StockMaster(
        stock_id=StockSymbol.SK_HYNIX,
        name_kr="SK하이닉스",
        name_en="SK Hynix Inc.",
        ticker="SKHY",
        market="NASDAQ ADR",
        currency="USD",
        category="메모리/HBM",
        badge_color="indigo",
        executive_keywords=["곽노정", "Kwak Noh-jung", "김창욱"],
        asset_keywords=["HBM", "HBM3E", "HBM4", "TSMC", "엔비디아", "용인 클러스터", "LTA", "CSI", "칩 부족 지수", "SKHY", "나스닥 ADR"]
    ),
    StockSymbol.SK_SQUARE: StockMaster(
        stock_id=StockSymbol.SK_SQUARE,
        name_kr="SK스퀘어",
        name_en="SK Square Co., Ltd.",
        ticker="402340",
        market="KRX",
        currency="KRW",
        category="지주/반도체",
        badge_color="blue",
        executive_keywords=["한명진"],
        asset_keywords=["솔리다임", "Solidigm", "NAV", "할인율", "중복상장", "지주사", "자사주 소각", "하이닉스 지분"]
    ),
    StockSymbol.MBLY: StockMaster(
        stock_id=StockSymbol.MBLY,
        name_kr="모빌아이",
        name_en="Mobileye Global Inc.",
        ticker="MBLY",
        market="NASDAQ",
        currency="USD",
        category="자율주행/ADAS",
        badge_color="amber",
        executive_keywords=["암논 샤슈아", "Amnon Shashua"],
        asset_keywords=["EyeQ", "EyeQ5", "EyeQ6", "EyeQ6L", "EyeQ6H", "SuperVision", "Chauffeur", "인텔", "Intel", "오버행", "폭스바겐", "지커", "Zeekr"]
    ),
    StockSymbol.FLNC: StockMaster(
        stock_id=StockSymbol.FLNC,
        name_kr="플루언스에너지",
        name_en="Fluence Energy, Inc.",
        ticker="FLNC",
        market="NASDAQ",
        currency="USD",
        category="AI 전력/BESS",
        badge_color="teal",
        executive_keywords=["줄리안 네브레다", "Julian Nebreda", "허먼 불스", "Herman Bulls"],
        asset_keywords=["BESS", "ESS", "배터리", "전력망", "지멘스", "AES", "휴스턴", "EVE Power", "400MWh", "가이던스"]
    ),
    StockSymbol.UPST: StockMaster(
        stock_id=StockSymbol.UPST,
        name_kr="업스타트홀딩스",
        name_en="Upstart Holdings, Inc.",
        ticker="UPST",
        market="NASDAQ",
        currency="USD",
        category="AI 핀테크/대출",
        badge_color="purple",
        executive_keywords=["폴 구", "Paul Gu", "데이브 지루아드", "Dave Girouard"],
        asset_keywords=["AI 신용평가", "무담보 대출", "개인대출", "국채금리", "사모신용", "연체율", "숏스퀴즈", "조달비용"]
    ),
    StockSymbol.CELH: StockMaster(
        stock_id=StockSymbol.CELH,
        name_kr="셀시우스홀딩스",
        name_en="Celsius Holdings, Inc.",
        ticker="CELH",
        market="NASDAQ",
        currency="USD",
        category="기능성음료/소비재",
        badge_color="orange",
        executive_keywords=["존 필들리", "John Fieldly", "자로드 번스톡", "Jarrod Langhans", "토니 휜", "Tony Guilfoyle"],
        asset_keywords=["펩시", "Pepsi", "에너지 드링크", "골드만삭스", "Goldman Sachs", "스캐너 데이터", "NACS", "인센티브", "점유율", "유통망", "마진"]
    ),
    StockSymbol.ENPH: StockMaster(
        stock_id=StockSymbol.ENPH,
        name_kr="엔페이즈에너지",
        name_en="Enphase Energy, Inc.",
        ticker="ENPH",
        market="NASDAQ",
        currency="USD",
        category="태양광/마이크로인버터",
        badge_color="cyan",
        executive_keywords=["바드리 코탄다라만", "Badri Kothandaraman", "맨디 양", "Mandy Yang", "라구 벨루리가파티", "Raghu Belur"],
        asset_keywords=["마이크로인버터", "Microinverter", "IQ8", "IQ9", "Enphase Air", "태양광", "NEM 3.0", "ESS", "인버터", "Solargraf", "분산에너지"]
    ),
}


@dataclass
class MarketMetrics:
    """Market price, percentage change, and volume metrics."""
    stock_id: str
    date: str = ""
    currency: str = "USD"
    close_price: Optional[float] = None
    close_price_formatted: Optional[str] = None
    change_percent: Optional[float] = None
    change_percent_formatted: Optional[str] = None
    change_amount: Optional[float] = None
    change_amount_formatted: Optional[str] = None
    volume: Optional[int] = None
    volume_formatted: Optional[str] = None
    market_status: str = "REGULAR_CLOSE"
    relative_performance: Optional[str] = None
    pe_ratio: Optional[str] = None
    after_hours: Optional[str] = None
    day_range: Optional[str] = None
    adr_premium: Optional[str] = None
    peer_comparison: Optional[str] = None

    @property
    def price(self) -> str:
        return self.close_price_formatted or (str(self.close_price) if self.close_price is not None else "")

    @property
    def change(self) -> str:
        return self.change_percent_formatted or (f"{self.change_percent:+.2f}%" if self.change_percent is not None else "")

    def to_dict(self) -> Dict[str, Any]:
        return {
            "stock_id": self.stock_id,
            "date": self.date,
            "currency": self.currency,
            "close_price": self.close_price,
            "close_price_formatted": self.close_price_formatted,
            "change_percent": self.change_percent,
            "change_percent_formatted": self.change_percent_formatted,
            "change_amount": self.change_amount,
            "change_amount_formatted": self.change_amount_formatted,
            "volume": self.volume,
            "volume_formatted": self.volume_formatted,
            "market_status": self.market_status,
            "relative_performance": self.relative_performance,
            "pe_ratio": self.pe_ratio,
            "after_hours": self.after_hours,
            "day_range": self.day_range,
            "adr_premium": self.adr_premium,
            "peer_comparison": self.peer_comparison,
        }


@dataclass
class CorePriceDriver:
    """Key catalyst or risk driving stock price move."""
    stock_id: str
    date: str = ""
    driver_type: str = "CATALYST"  # CATALYST, RISK, EARNINGS, GOVERNANCE, MACRO
    classification: str = "FACT"   # FACT, NOISE, FACT_VS_NOISE
    is_noise: bool = False
    title: str = ""
    headline_summary: str = ""
    catalyst_category: str = ""
    impact_direction: str = "NEUTRAL"  # POSITIVE, NEGATIVE, NEUTRAL
    evidence_facts: List[str] = field(default_factory=list)
    market_noise_points: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class ExecutiveInterviewFact:
    """Executive or expert interview insights, quotes, and trajectory."""
    stock_id: str
    date: str = ""
    speaker_name: str = ""
    speaker_title: str = ""
    affiliation: str = ""
    source_media: str = ""
    source_url: str = ""
    core_quotes: List[str] = field(default_factory=list)
    context_trajectory: str = ""
    investment_takeaway: str = ""

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


# Aliases for compatibility
InterviewFact = ExecutiveInterviewFact
InterviewSummary = ExecutiveInterviewFact


@dataclass
class IBReportFact:
    """Investment bank or brokerage research report analysis."""
    stock_id: str
    date: str = ""
    brokerage: str = ""
    analyst_name: str = ""
    report_title: str = ""
    rating_current: str = ""  # BUY, HOLD, UNDERPERFORM, OUTPERFORM
    rating_prior: Optional[str] = None
    target_price_current: Optional[float] = None
    target_price_prior: Optional[float] = None
    target_price_currency: str = "USD"
    key_thesis: str = ""
    valuation_metrics: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


# Alias for compatibility
IBComment = IBReportFact


@dataclass
class PortfolioPairStrategy:
    """Portfolio pair analysis and tactical execution guidance (SK Square vs SK Hynix)."""
    date: str = ""
    sk_square_weight: float = 0.0
    sk_hynix_weight: float = 0.0
    relative_spread: str = ""
    tactical_action: str = "HOLD_POSITION"  # HOLD_POSITION, SWITCH_TO_SQUARE, SWITCH_TO_HYNIX, REBALANCE
    action_label: str = "스위칭 보류 / 현 비중 유지"
    risk_warning: str = ""
    rationale: str = ""
    holdings_summary: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


# Aliases for compatibility
PairStrategy = PortfolioPairStrategy
PortfolioImpactFact = PortfolioPairStrategy


@dataclass
class KeyWatchPoints:
    """Two-line focus checkpoints for a monitored stock."""
    line1_short_term: str = ""    # 단기 수급/가격선 (핵심 지지/저항 가격대, 단기 수급 및 변동성 트리거)
    line2_mid_long_term: str = "" # 중장기 펀더멘털/이벤트 (차기 실적, 신제품 양산, 계약/가이던스)

    def to_dict(self) -> Dict[str, str]:
        return {
            "line1_short_term": self.line1_short_term,
            "line2_mid_long_term": self.line2_mid_long_term,
        }


@dataclass
class StockFactSheet:
    """Consolidated fact sheet for a single stock."""
    stock_id: str
    stock_name: str
    name_kr: str
    name_en: str
    ticker: str
    market: str
    category: str
    badge_color: str
    metrics: MarketMetrics
    core_drivers: List[str] = field(default_factory=list)
    structured_drivers: List[CorePriceDriver] = field(default_factory=list)
    fact_vs_noise: Dict[str, List[str]] = field(default_factory=lambda: {"facts": [], "noise": []})
    interviews: List[ExecutiveInterviewFact] = field(default_factory=list)
    ib_comments: List[IBReportFact] = field(default_factory=list)
    raw_summary: str = ""
    strategist_insight: str = ""
    portfolio_impact: str = ""
    # New Standard Format Fields (Requirement R2)
    one_paragraph_summary: str = ""
    key_points: KeyWatchPoints = field(default_factory=KeyWatchPoints)
    macro_attribution: str = ""

    def __post_init__(self) -> None:
        # Guarantee cross-attribute population for 100% backward compatibility
        if not self.one_paragraph_summary and self.raw_summary:
            self.one_paragraph_summary = self.raw_summary
        elif not self.raw_summary and self.one_paragraph_summary:
            self.raw_summary = self.one_paragraph_summary

    @property
    def close_price(self) -> Optional[float]:
        return self.metrics.close_price

    @property
    def currency(self) -> str:
        return self.metrics.currency

    @property
    def change_pct(self) -> Optional[float]:
        return self.metrics.change_percent

    @property
    def volume(self) -> Optional[int]:
        return self.metrics.volume

    def to_dict(self) -> Dict[str, Any]:
        return {
            "stock_id": self.stock_id,
            "stock_name": self.stock_name,
            "name_kr": self.name_kr,
            "name_en": self.name_en,
            "ticker": self.ticker,
            "market": self.market,
            "category": self.category,
            "badge_color": self.badge_color,
            "metrics": self.metrics.to_dict(),
            "core_drivers": list(self.core_drivers),
            "structured_drivers": [d.to_dict() for d in self.structured_drivers],
            "fact_vs_noise": self.fact_vs_noise,
            "interviews": [i.to_dict() for i in self.interviews],
            "ib_comments": [b.to_dict() for b in self.ib_comments],
            "raw_summary": self.raw_summary,
            "strategist_insight": self.strategist_insight,
            "portfolio_impact": self.portfolio_impact,
            # Augmented standard fields
            "one_paragraph_summary": self.one_paragraph_summary,
            "key_points": self.key_points.to_dict() if isinstance(self.key_points, KeyWatchPoints) else self.key_points,
            "watch_points": [self.key_points.line1_short_term, self.key_points.line2_mid_long_term] if isinstance(self.key_points, KeyWatchPoints) else [],
            "macro_attribution": self.macro_attribution,
        }


@dataclass
class DailyMarketData:
    """Master aggregated market payload for all 8 stocks, macro briefing, and portfolio guidance."""
    date: str = "2026-09-29"
    macro_summary: str = ""
    macro_overview: str = ""
    stocks: Dict[str, StockFactSheet] = field(default_factory=dict)
    pair_strategy: PortfolioPairStrategy = field(default_factory=PortfolioPairStrategy)
    portfolio_guidance: Dict[str, Any] = field(default_factory=dict)
    cleaned_metadata: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not self.macro_overview and self.macro_summary:
            self.macro_overview = self.macro_summary
        elif not self.macro_summary and self.macro_overview:
            self.macro_summary = self.macro_overview

        if not self.portfolio_guidance and self.pair_strategy:
            self.portfolio_guidance = self.pair_strategy.to_dict()

    def to_dict(self) -> Dict[str, Any]:
        return {
            "date": self.date,
            "macro_summary": self.macro_summary,
            "macro_overview": self.macro_overview,
            "stocks": {k: v.to_dict() for k, v in self.stocks.items()},
            "pair_strategy": self.pair_strategy.to_dict(),
            "portfolio_guidance": self.portfolio_guidance or self.pair_strategy.to_dict(),
            "cleaned_metadata": self.cleaned_metadata,
        }

    def to_json(self, indent: int = 2) -> str:
        return json.dumps(self.to_dict(), ensure_ascii=False, indent=indent)


# Alias for compatibility
DailyDigestPayload = DailyMarketData

# Known Interviewees Dictionary: name -> (title, affiliation)
KNOWN_INTERVIEWEES: Dict[str, Tuple[str, str]] = {
    "김창욱": ("MD파트너 (반도체 부문 총괄)", "보스턴컨설팅그룹 (BCG)"),
    "곽노정": ("대표이사 사장 (CEO)", "SK하이닉스"),
    "한명진": ("대표이사 사장 (CEO)", "SK스퀘어"),
    "빌 걸리": ("초기 벤치마크 파트너 / 벤처투자자", "Benchmark"),
    "Bill Gurley": ("General Partner", "Benchmark"),
    "브래드 거스너": ("설립자 겸 CEO", "Altimeter Capital"),
    "Brad Gerstner": ("Founder & CEO", "Altimeter Capital"),
    "다라 코스로샤히": ("최고경영자 (CEO)", "우버"),
    "Dara Khosrowshahi": ("CEO", "Uber Technologies"),
    "돔 테일러": ("아시아태평양 총괄 대표 (APAC GM)", "우버 (Uber)"),
    "Dom Taylor": ("General Manager, APAC", "Uber Technologies"),
    "암논 샤슈아": ("설립자 겸 CEO", "모빌아이"),
    "Amnon Shashua": ("President & CEO", "Mobileye"),
    "댄 갈베스": ("최고커뮤니케이션책임자 (CCO)", "모빌아이 (Mobileye)"),
    "Dan Galves": ("Chief Communications Officer (CCO)", "Mobileye"),
    "줄리안 네브레다": ("최고경영자 (CEO)", "플루언스에너지"),
    "Julian Nebreda": ("President & CEO", "Fluence Energy"),
    "허먼 불스": ("이사회 이사", "플루언스에너지"),
    "Herman Bulls": ("Board Director", "Fluence Energy"),
    "데이브 지루아르": ("공동설립자 겸 최고경영자 (CEO)", "업스타트"),
    "Dave Girouard": ("Co-Founder & CEO", "Upstart Holdings"),
    "존 필드": ("최고재무책임자 (CFO)", "셀시우스홀딩스"),
    "John Fieldly": ("Chairman & CEO", "Celsius Holdings"),
    "바드리 코탄다라만": ("사장 겸 최고경영자 (CEO)", "엔페이즈에너지"),
    "Badri Kothandaraman": ("President & CEO", "Enphase Energy"),
}

# Known Brokerages & Research Firms
KNOWN_BROKERAGES: List[str] = [
    "노무라", "Nomura", "제프리스", "Jefferies", "미즈호", "Mizuho",
    "BNP파리바", "BNP Paribas", "모건스탠리", "Morgan Stanley", "골드만삭스", "Goldman Sachs",
    "JP모건", "JPMorgan", "바클레이스", "Barclays", "울프리서치", "Wolfe Research",
    "씨티", "Citi", "미래에셋", "삼성증권", "한국투자증권", "KB증권", "신한투자증권",
    "NH투자증권", "대신증권", "키움증권", "하나증권", "메리츠증권", "Seeking Alpha", "PropNotes",
    "번스타인", "Bernstein", "에버코어", "Evercore"
]

