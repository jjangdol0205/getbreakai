"""Multi-Stock Personal Investment Processing & Fact Extraction Engine (R1).

Modules:
- models: Dataclass contracts for 6 target stocks, metrics, drivers, interviews, IB comments, portfolio strategies.
- cleaner: 8-category UI noise and chatbot chrome removal pipeline.
- extractor: Disambiguation and structured fact extraction engine.
- cli: Command-line interface for clean and parse commands.
"""

from engine.cleaner import RawDumpCleaner, clean_raw_dump
from engine.extractor import FactExtractor, extract_facts
from engine.models import (
    STOCK_MASTERS,
    CorePriceDriver,
    DailyDigestPayload,
    DailyMarketData,
    ExecutiveInterviewFact,
    IBComment,
    IBReportFact,
    InterviewFact,
    InterviewSummary,
    MarketMetrics,
    PairStrategy,
    PortfolioImpactFact,
    PortfolioPairStrategy,
    StockFactSheet,
    StockMaster,
    StockSymbol,
)

__all__ = [
    "RawDumpCleaner",
    "clean_raw_dump",
    "FactExtractor",
    "extract_facts",
    "StockSymbol",
    "StockMaster",
    "STOCK_MASTERS",
    "MarketMetrics",
    "CorePriceDriver",
    "ExecutiveInterviewFact",
    "InterviewFact",
    "InterviewSummary",
    "IBReportFact",
    "IBComment",
    "PortfolioPairStrategy",
    "PairStrategy",
    "PortfolioImpactFact",
    "StockFactSheet",
    "DailyMarketData",
    "DailyDigestPayload",
]
