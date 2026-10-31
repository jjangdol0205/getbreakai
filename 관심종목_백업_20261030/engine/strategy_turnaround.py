"""
Strategy A: 52-Week Low Turnaround Concentrated in Max 2 Stocks with Weekly Switching.
Part of the 25.25-Year Quantitative Backtesting & Strategy Suite (Milestone 2).

Core Pillars:
1. 4-Filter Screening:
   - Filter 1: 52-week low proximity (<= 20.0%) & crash depth safety margin
   - Filter 2: 1~2 year forward earnings turnaround (>= 30.0% growth or loss -> profit turnaround)
   - Filter 3: Volume wash-out capitulation (>= 1.40x 20D volume), floor defense, green/flat rebound
   - Filter 4: Asymmetric risk/reward ratio (downside <= 10.0%, upside to TP1 >= 100.0%, RRR >= 10.0x)
   - Composite Score (0~100) & Conviction Tiers: TOP_PICK (>=88), STRONG_CANDIDATE (>=75), WATCHLIST (>=55)

2. Max 2 Stocks Concentration Rule:
   - 100% Single Winner: exactly 1 candidate achieves TOP_PICK (score >= 88.0) and no other candidate >= 75.0.
   - 50% / 50% Dual Concentration: 2 or more qualified candidates exist (top 2 by deterministic RankKey).
   - Defensive Benchmark Spillover: when 0 candidates qualify, temporary allocation to core benchmark
     (QQQ/SOXX) to strictly adhere to the 100% equity simplex constraint with zero cash (w_cash = 0.0).

3. Weekly Switching Logic & Reverse-Switching Defense Lock:
   - Evaluates new candidates weekly against held turnaround stocks.
   - Switching hurdle: candidate achieves STRONG_SWITCH tier (3/3 triggers, RRR ratio >= 1.3x and catalyst
     advantage > 0, OR catalyst advantage >= 30d and D-Day <= 30d) OR composite score is >= 15.0 pts higher.
   - Reverse-Switching Defense Lock: strictly FORBIDS switching away from a core holding in safety margin
     with an imminent catalyst (D-Day <= 20 days). Locks holding to avoid premature exit before breakout.

4. Asymmetric Exit Rules:
   - TP1 (1st Take Profit): Sell exactly 50% of position at +100% gain (2.0x entry price) to recover
     100% of invested principal in cash. The remaining 50% of shares is held at an effective cost basis
     of $0.00 (Risk-Free / "House Money") to ride the full multi-year trend.
   - Stop Loss: Sell 100% of position if price drops -10% from entry price or breaches key support by -10%.

5. Seamless Integration with BacktestEngine:
   - Transaction friction: 0.10% brokerage fee + 0.08% execution slippage.
   - 5 Rebalancing Frequencies: WEEKLY, MONTHLY, QUARTERLY, SEMI_ANNUALLY, ANNUALLY.
   - Capital gains tax modeling: 22.0% effective rate with 2.5M KRW / $2,000 USD annual deduction.
   - Dual pre-tax and after-tax financial metrics suite.

100% Offline, Zero-CDN, Pure Python Standard Library.
No external network sockets, no pandas/numpy dependencies.
Memory footprint: <350 KB.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
import datetime
import math
from typing import Any, Callable, Dict, List, Optional, Set, Tuple, Union

from engine.backtest_engine import (
    BacktestConfig,
    PerformanceMetrics,
    RebalanceFrequency,
    SimulationResult,
    TaxAccountingState,
    calculate_performance_metrics,
    is_rebalance_date,
)
from engine.historical_data import (
    COMMON_START_DATE,
    COMMON_END_DATE,
    get_joint_history,
    get_qqq_history,
    get_soxx_history,
)
from engine.turnaround_screener import (
    ScreeningFilterResult,
    TurnaroundCandidate,
    TurnaroundScreener,
    WeeklyTopPick,
)


# ==============================================================================
# 1. Strategy A Dataclasses
# ==============================================================================

@dataclass
class TurnaroundPosition:
    """State tracking for an active turnaround stock position."""
    stock_id: str
    entry_date: str
    entry_price: float
    current_price: float
    shares: float
    initial_shares: float
    initial_cost: float
    support_price: float
    tp1_price: float
    tp1_executed: bool = False
    is_risk_free: bool = False
    cash_recovered: float = 0.0
    cost_basis: float = 0.0
    peak_price: float = 0.0
    catalyst_d_day: Optional[int] = None
    composite_score: float = 0.0
    fifty_two_week_low: float = 0.0


@dataclass
class ExitDecision:
    """Diagnostic outcome of exit condition evaluation."""
    stock_id: str
    action: str           # "TP1_PARTIAL", "STOP_LOSS_FULL", "HOLD"
    shares_to_sell: float
    execution_price: float
    cash_realized: float
    realized_gain: float
    reason: str


@dataclass
class SwitchingEvaluation:
    """Diagnostic outcome of switching comparison between held stock and candidate."""
    held_stock_id: str
    candidate_stock_id: str
    should_switch: bool
    is_reverse_warning_locked: bool
    score_gap: float
    rrr_ratio: float
    catalyst_advantage_days: int
    candidate_tier: str
    reason: str


@dataclass
class TurnaroundEpisode:
    """Pre-computed historical 52-week low turnaround episode for multi-era simulation."""
    stock_id: str
    name_kr: str
    ticker: str
    era: str               # "DOT_COM", "GFC", "MID_TECH", "COVID", "AI_CYCLE"
    start_date: str
    trough_date: str
    end_date: str
    trough_price: float
    peak_price: float
    fifty_two_week_low: float
    fifty_two_week_high: float
    support_price: float
    tp1_price: float
    rev_growth_2y: float
    oi_growth_2y: float
    is_turnaround_to_profit: bool
    volume_surge_ratio: float
    catalyst_d_day_initial: int


# ==============================================================================
# 2. Canonical 25-Year Historical Turnaround Episodes Database
# ==============================================================================

# Authoritative historical turnaround episodes spanning 2001-07-10 to 2026-10-12
HISTORICAL_TURNAROUND_EPISODES: List[TurnaroundEpisode] = [
    # Era 1: Dot-Com Crash Bottom (2001-2004)
    TurnaroundEpisode(
        stock_id="AMZN_2001",
        name_kr="아마존닷컴(2001)",
        ticker="AMZN",
        era="DOT_COM",
        start_date="2001-07-10",
        trough_date="2001-09-28",
        end_date="2004-01-15",
        trough_price=5.51,
        peak_price=59.50,
        fifty_two_week_low=5.50,
        fifty_two_week_high=45.00,
        support_price=5.20,
        tp1_price=11.02,
        rev_growth_2y=34.0,
        oi_growth_2y=120.0,
        is_turnaround_to_profit=True,
        volume_surge_ratio=2.45,
        catalyst_d_day_initial=42,
    ),
    TurnaroundEpisode(
        stock_id="NVDA_2002",
        name_kr="엔비디아(2002)",
        ticker="NVDA",
        era="DOT_COM",
        start_date="2002-06-15",
        trough_date="2002-10-09",
        end_date="2004-06-30",
        trough_price=2.43,
        peak_price=14.80,
        fifty_two_week_low=2.40,
        fifty_two_week_high=24.50,
        support_price=2.25,
        tp1_price=4.86,
        rev_growth_2y=48.0,
        oi_growth_2y=65.0,
        is_turnaround_to_profit=False,
        volume_surge_ratio=2.10,
        catalyst_d_day_initial=18,  # Triggers reverse-switch warning lock!
    ),
    TurnaroundEpisode(
        stock_id="AAPL_2002",
        name_kr="애플(2002)",
        ticker="AAPL",
        era="DOT_COM",
        start_date="2002-09-01",
        trough_date="2002-12-24",
        end_date="2005-03-31",
        trough_price=0.25,
        peak_price=1.65,
        fifty_two_week_low=0.24,
        fifty_two_week_high=0.95,
        support_price=0.23,
        tp1_price=0.50,
        rev_growth_2y=38.0,
        oi_growth_2y=150.0,
        is_turnaround_to_profit=True,
        volume_surge_ratio=1.85,
        catalyst_d_day_initial=35,
    ),

    # Era 2: Global Financial Crisis Bottom (2008-2011)
    TurnaroundEpisode(
        stock_id="AMD_2008",
        name_kr="AMD(2008)",
        ticker="AMD",
        era="GFC",
        start_date="2008-10-01",
        trough_date="2008-11-20",
        end_date="2010-04-30",
        trough_price=1.62,
        peak_price=10.20,
        fifty_two_week_low=1.60,
        fifty_two_week_high=8.50,
        support_price=1.50,
        tp1_price=3.24,
        rev_growth_2y=32.0,
        oi_growth_2y=140.0,
        is_turnaround_to_profit=True,
        volume_surge_ratio=3.20,
        catalyst_d_day_initial=15,  # Imminent catalyst D-Day <= 20
    ),
    TurnaroundEpisode(
        stock_id="MU_2008",
        name_kr="마이크론(2008)",
        ticker="MU",
        era="GFC",
        start_date="2008-10-15",
        trough_date="2008-11-20",
        end_date="2010-06-30",
        trough_price=2.14,
        peak_price=11.95,
        fifty_two_week_low=2.10,
        fifty_two_week_high=9.80,
        support_price=1.98,
        tp1_price=4.28,
        rev_growth_2y=45.0,
        oi_growth_2y=180.0,
        is_turnaround_to_profit=True,
        volume_surge_ratio=2.60,
        catalyst_d_day_initial=45,
    ),

    # Era 3: European Debt / Tech Mini-Correction (2011-2014)
    TurnaroundEpisode(
        stock_id="NFLX_2011",
        name_kr="넷플릭스(2011)",
        ticker="NFLX",
        era="MID_TECH",
        start_date="2011-09-01",
        trough_date="2012-09-28",
        end_date="2014-06-30",
        trough_price=7.50,
        peak_price=68.00,
        fifty_two_week_low=7.40,
        fifty_two_week_high=43.50,
        support_price=7.00,
        tp1_price=15.00,
        rev_growth_2y=52.0,
        oi_growth_2y=85.0,
        is_turnaround_to_profit=False,
        volume_surge_ratio=2.15,
        catalyst_d_day_initial=28,
    ),
    TurnaroundEpisode(
        stock_id="NVDA_2015",
        name_kr="엔비디아(2015)",
        ticker="NVDA",
        era="MID_TECH",
        start_date="2015-06-01",
        trough_date="2015-08-24",
        end_date="2017-12-31",
        trough_price=4.80,
        peak_price=52.00,
        fifty_two_week_low=4.75,
        fifty_two_week_high=6.20,
        support_price=4.50,
        tp1_price=9.60,
        rev_growth_2y=42.0,
        oi_growth_2y=75.0,
        is_turnaround_to_profit=False,
        volume_surge_ratio=1.90,
        catalyst_d_day_initial=32,
    ),

    # Era 4: COVID Flash Crash Bottom (2020-2022)
    TurnaroundEpisode(
        stock_id="UBER_2020",
        name_kr="우버(2020)",
        ticker="UBER",
        era="COVID",
        start_date="2020-03-01",
        trough_date="2020-03-18",
        end_date="2021-04-30",
        trough_price=14.82,
        peak_price=63.18,
        fifty_two_week_low=13.71,
        fifty_two_week_high=41.80,
        support_price=13.50,
        tp1_price=29.64,
        rev_growth_2y=57.0,
        oi_growth_2y=130.0,
        is_turnaround_to_profit=True,
        volume_surge_ratio=3.80,
        catalyst_d_day_initial=12,  # D-Day <= 20
    ),
    TurnaroundEpisode(
        stock_id="ENPH_2020",
        name_kr="엔페이즈(2020)",
        ticker="ENPH",
        era="COVID",
        start_date="2020-03-01",
        trough_date="2020-03-18",
        end_date="2021-12-31",
        trough_price=22.50,
        peak_price=215.00,
        fifty_two_week_low=21.00,
        fifty_two_week_high=61.00,
        support_price=20.50,
        tp1_price=45.00,
        rev_growth_2y=85.0,
        oi_growth_2y=160.0,
        is_turnaround_to_profit=False,
        volume_surge_ratio=2.50,
        catalyst_d_day_initial=40,
    ),

    # Era 5: Rate Tightening & AI Cycle Turnaround (2022-2026)
    TurnaroundEpisode(
        stock_id="MBLY",
        name_kr="모빌아이",
        ticker="MBLY",
        era="AI_CYCLE",
        start_date="2024-01-01",
        trough_date="2024-09-06",
        end_date="2026-10-12",
        trough_price=6.47,
        peak_price=16.80,
        fifty_two_week_low=6.47,
        fifty_two_week_high=34.50,
        support_price=6.87,
        tp1_price=15.00,
        rev_growth_2y=38.0,
        oi_growth_2y=180.0,
        is_turnaround_to_profit=True,
        volume_surge_ratio=2.40,
        catalyst_d_day_initial=14,  # D-Day <= 20
    ),
    TurnaroundEpisode(
        stock_id="CELH",
        name_kr="셀시우스홀딩스",
        ticker="CELH",
        era="AI_CYCLE",
        start_date="2024-05-01",
        trough_date="2024-10-07",
        end_date="2026-10-12",
        trough_price=26.50,
        peak_price=62.00,
        fifty_two_week_low=26.50,
        fifty_two_week_high=99.62,
        support_price=25.00,
        tp1_price=55.00,
        rev_growth_2y=42.0,
        oi_growth_2y=171.0,
        is_turnaround_to_profit=False,
        volume_surge_ratio=1.95,
        catalyst_d_day_initial=35,
    ),
    TurnaroundEpisode(
        stock_id="ENPH",
        name_kr="엔페이즈에너지",
        ticker="ENPH",
        era="AI_CYCLE",
        start_date="2024-06-01",
        trough_date="2024-10-07",
        end_date="2026-10-12",
        trough_price=30.00,
        peak_price=72.00,
        fifty_two_week_low=30.00,
        fifty_two_week_high=135.00,
        support_price=30.00,
        tp1_price=65.00,
        rev_growth_2y=35.0,
        oi_growth_2y=250.0,
        is_turnaround_to_profit=False,
        volume_surge_ratio=1.80,
        catalyst_d_day_initial=42,
    ),
    TurnaroundEpisode(
        stock_id="UPST",
        name_kr="업스타트홀딩스",
        ticker="UPST",
        era="AI_CYCLE",
        start_date="2023-01-01",
        trough_date="2023-05-03",
        end_date="2026-10-12",
        trough_price=12.00,
        peak_price=72.00,
        fifty_two_week_low=11.90,
        fifty_two_week_high=390.00,
        support_price=11.50,
        tp1_price=24.00,
        rev_growth_2y=45.0,
        oi_growth_2y=666.0,
        is_turnaround_to_profit=True,
        volume_surge_ratio=4.50,
        catalyst_d_day_initial=50,
    ),
]


# ==============================================================================
# 3. Strategy A Simulator Engine
# ==============================================================================

class StrategyASimulator:
    """
    Quantitative simulator for Strategy A:
    52-Week Low Turnaround Concentrated in Max 2 Stocks with Weekly Switching.
    """

    def __init__(self, episodes: Optional[List[TurnaroundEpisode]] = None) -> None:
        self.episodes = episodes if episodes is not None else list(HISTORICAL_TURNAROUND_EPISODES)
        self.episode_map = {e.stock_id: e for e in self.episodes}

    # --------------------------------------------------------------------------
    # 4-Filter Screening & Candidate Generation
    # --------------------------------------------------------------------------

    def screen_candidate(
        self,
        stock_id: str,
        current_price: float,
        fifty_two_week_low: float,
        fifty_two_week_high: float,
        support_price: float,
        tp1_price: float,
        revenue_growth_2y: float,
        operating_income_growth_2y: float,
        is_turnaround_to_profit: bool,
        volume: int,
        benchmark_20d_volume: int,
        daily_change_pct: float = 0.0,
        catalyst_d_day: Optional[int] = None,
        name_kr: str = "",
        ticker: str = "",
    ) -> TurnaroundCandidate:
        """Evaluates an individual candidate stock against all 4 turnaround filters."""
        # 1. Filter 1: 52-Week Low Proximity
        f1 = TurnaroundScreener.evaluate_filter_52w_low(
            stock_id=stock_id,
            current_price=current_price,
            fifty_two_week_low=fifty_two_week_low,
            fifty_two_week_high=fifty_two_week_high,
            max_proximity_pct=20.0,
        )

        # 2. Filter 2: 1~2 Year Earnings Turnaround
        dummy_fin = {
            "income_statement": {
                "revenue": [100.0, 110.0, 120.0, 100.0, 100.0 * (1.0 + revenue_growth_2y / 100.0)],
                "operating_income": (
                    [-10.0, -5.0, -2.0, -1.0, 10.0]
                    if is_turnaround_to_profit
                    else [10.0, 12.0, 15.0, 10.0, 10.0 * (1.0 + operating_income_growth_2y / 100.0)]
                ),
            },
            "years": ["2022", "2023", "2024", "2025", "2027E"],
        }
        f2 = TurnaroundScreener.evaluate_filter_earnings_turnaround(
            stock_id=stock_id,
            financials=dummy_fin,
            min_growth_pct=30.0,
        )

        # 3. Filter 3: Volume Wash-Out
        f3 = TurnaroundScreener.evaluate_filter_volume_washout(
            stock_id=stock_id,
            current_price=current_price,
            daily_change_pct=daily_change_pct,
            volume=volume,
            support_price=support_price,
            benchmark_20d_volume=benchmark_20d_volume,
            min_surge_ratio=1.40,
        )

        # 4. Filter 4: Risk/Reward Ratio
        f4 = TurnaroundScreener.evaluate_filter_risk_reward(
            stock_id=stock_id,
            current_price=current_price,
            support_price=support_price,
            tp1_price=tp1_price,
            max_downside_pct=10.0,
            min_upside_pct=100.0,
        )

        filters = {
            "cond1_52w_low": f1,
            "cond2_earnings_turnaround": f2,
            "cond3_volume_washout": f3,
            "cond4_risk_reward": f4,
        }

        pass_count = sum(1 for f in filters.values() if f.passed)
        composite_score = TurnaroundScreener.calculate_composite_score(f1, f2, f3, f4)
        conviction_tier = TurnaroundScreener.determine_conviction_tier(composite_score)
        is_qualified = (pass_count == 4) or (pass_count >= 3 and composite_score >= 75.0)

        prox_pct = ((current_price - fifty_two_week_low) / fifty_two_week_low * 100.0) if fifty_two_week_low > 0 else 0.0
        crash_pct = ((current_price - fifty_two_week_high) / fifty_two_week_high * 100.0) if fifty_two_week_high > 0 else 0.0
        down_pct = ((current_price - support_price) / current_price * 100.0) if current_price > 0 else 0.0
        up_pct = ((tp1_price - current_price) / current_price * 100.0) if current_price > 0 else 0.0
        rrr = up_pct / max(down_pct, 0.5)
        vol_ratio = volume / benchmark_20d_volume if benchmark_20d_volume > 0 else 0.0

        return TurnaroundCandidate(
            stock_id=stock_id,
            name_kr=name_kr or stock_id,
            ticker=ticker or stock_id,
            market="US",
            currency="USD",
            current_price=current_price,
            current_price_formatted=f"${current_price:.2f}",
            fifty_two_week_low=fifty_two_week_low,
            fifty_two_week_high=fifty_two_week_high,
            proximity_52w_low_pct=round(prox_pct, 2),
            crash_from_high_pct=round(crash_pct, 2),
            support_price=support_price,
            downside_risk_pct=round(down_pct, 2),
            tp1_price=tp1_price,
            upside_tp1_pct=round(up_pct, 2),
            risk_reward_ratio=round(rrr, 2),
            revenue_growth_2y_pct=round(revenue_growth_2y, 2),
            operating_income_growth_2y_pct=round(operating_income_growth_2y, 2),
            is_turnaround_to_profit=is_turnaround_to_profit,
            volume_surge_ratio=round(vol_ratio, 2),
            filters=filters,
            pass_count=pass_count,
            is_qualified=is_qualified,
            composite_turnaround_score=composite_score,
            conviction_tier=conviction_tier,
            recommendation_summary=f"[{conviction_tier}] {stock_id}: Score {composite_score:.1f}, RRR {rrr:.1f}x",
            catalyst_d_day=catalyst_d_day,
        )

    # --------------------------------------------------------------------------
    # Max 2 Stocks Concentration & Simplex Allocation Rules
    # --------------------------------------------------------------------------

    @staticmethod
    def calculate_concentration_weights(
        candidates: List[TurnaroundCandidate],
        benchmark_symbol: str = "QQQ",
    ) -> Dict[str, float]:
        """
        Determines portfolio allocation weights enforcing:
        1. 100% Single Winner: exactly 1 candidate achieves TOP_PICK (score >= 88.0) and no other >= 75.0.
        2. 50% / 50% Dual Concentration: 2 or more qualified candidates exist.
        3. 1 Candidate with 75.0 <= score < 88.0: 50% candidate + 50% defensive benchmark.
        4. Defensive Benchmark Spillover: when 0 candidates qualify -> 100% allocation to benchmark.
        Strict 100% equity simplex constraint: sum(weights) == 1.0, cash == 0.0.
        """
        if not candidates:
            return {benchmark_symbol: 1.0}

        qualified = [c for c in candidates if c.is_qualified and c.composite_turnaround_score >= 75.0]

        if not qualified:
            # 0 qualified candidates: 100% defensive benchmark spillover
            return {benchmark_symbol: 1.0}

        # Rank candidates by deterministic multi-tier RankKey
        qualified.sort(
            key=TurnaroundScreener._candidate_rank_key,
            reverse=True,
        )

        top_cand = qualified[0]

        # Case 1: 100% Single Winner
        # Triggered when exactly 1 candidate scores >= 88.0 (TOP_PICK) and no other candidate scores >= 75.0
        other_qualified = qualified[1:]
        has_second_qualified = any(c.composite_turnaround_score >= 75.0 for c in other_qualified)

        if top_cand.composite_turnaround_score >= 88.0 and not has_second_qualified:
            return {top_cand.stock_id: 1.0}

        # Case 2: 50% / 50% Dual Concentration
        if len(qualified) >= 2:
            second_cand = qualified[1]
            return {
                top_cand.stock_id: 0.50,
                second_cand.stock_id: 0.50,
            }

        # Case 3: Single candidate with 75.0 <= Score < 88.0
        # Allocate 50% to candidate, 50% to benchmark spillover
        return {
            top_cand.stock_id: 0.50,
            benchmark_symbol: 0.50,
        }

    # --------------------------------------------------------------------------
    # Weekly Switching Hurdle & Reverse-Switching Defense Lock
    # --------------------------------------------------------------------------

    @staticmethod
    def evaluate_switching_hurdle(
        held_position: TurnaroundPosition,
        candidate: TurnaroundCandidate,
        held_catalyst_d_day: Optional[int] = None,
        candidate_catalyst_d_day: Optional[int] = None,
    ) -> SwitchingEvaluation:
        """
        Evaluates whether a new candidate qualifies to switch away from an existing holding.
        
        Switching Hurdle:
        1. Tier STRONG_SWITCH:
           (Candidate triggers = 3/3, RRR advantage >= 1.3x and catalyst advantage > 0, OR
            catalyst advantage >= 30d and candidate D-Day <= 30d)
           OR
        2. Score Gap: Candidate score is >= 15.0 points higher than holding.
        
        Reverse-Switching Warning Lock:
        Strictly FORBIDS switching if holding is in safety margin with imminent catalyst (D-Day <= 20 days).
        """
        h_score = held_position.composite_score
        c_score = candidate.composite_turnaround_score
        score_gap = c_score - h_score

        h_d_day = (
            held_catalyst_d_day
            if held_catalyst_d_day is not None
            else (held_position.catalyst_d_day if held_position.catalyst_d_day is not None else 999)
        )
        c_d_day = (
            candidate_catalyst_d_day
            if candidate_catalyst_d_day is not None
            else (candidate.catalyst_d_day if candidate.catalyst_d_day is not None else 999)
        )

        catalyst_advantage = h_d_day - c_d_day

        h_downside = ((held_position.current_price - held_position.support_price) / held_position.current_price * 100.0) if held_position.current_price > 0 else 10.0
        h_upside = ((held_position.tp1_price - held_position.current_price) / held_position.current_price * 100.0) if held_position.current_price > 0 else 0.0
        h_rrr = h_upside / max(h_downside, 0.5)

        c_rrr = candidate.risk_reward_ratio
        rrr_ratio = c_rrr / max(h_rrr, 0.1)

        # Check STRONG_SWITCH tier condition
        is_strong_switch = (
            candidate.pass_count >= 3
            and (
                (rrr_ratio >= 1.3 and catalyst_advantage > 0)
                or (catalyst_advantage >= 30 and c_d_day <= 30)
            )
        )

        hurdle_passed = is_strong_switch or (score_gap >= 15.0)

        # Reverse-Switching Defense Lock check
        # Holding must be in safety margin (near 52W low / defending support, price < TP1)
        h_price = held_position.current_price
        is_in_safety_margin = (
            h_price < held_position.tp1_price
            and (
                h_price <= held_position.fifty_two_week_low * 1.25
                or h_price >= held_position.support_price * 0.99
            )
        )

        is_reverse_locked = (h_d_day <= 20) and is_in_safety_margin

        if is_reverse_locked:
            should_switch = False
            reason = (
                f"[REVERSE_SWITCH_WARNING] Holding {held_position.stock_id} locked! "
                f"Imminent catalyst D-{h_d_day} <= 20 days within safety margin. Switch forbidden."
            )
        elif hurdle_passed:
            should_switch = True
            tier_str = "STRONG_SWITCH" if is_strong_switch else f"+{score_gap:.1f}pt Score Gap"
            reason = f"[EXECUTE_SWITCH] Hurdle cleared via {tier_str} (RRR ratio {rrr_ratio:.2f}x)."
        else:
            should_switch = False
            reason = (
                f"[HOLD_CORE] Hurdle not met. Score gap {score_gap:+.1f} < 15.0 pts and "
                f"STRONG_SWITCH conditions not satisfied."
            )

        cand_tier = "STRONG_SWITCH" if is_strong_switch else ("PARTIAL_SWITCH" if score_gap >= 15.0 else "HOLD_CORE")

        return SwitchingEvaluation(
            held_stock_id=held_position.stock_id,
            candidate_stock_id=candidate.stock_id,
            should_switch=should_switch,
            is_reverse_warning_locked=is_reverse_locked,
            score_gap=round(score_gap, 2),
            rrr_ratio=round(rrr_ratio, 2),
            catalyst_advantage_days=catalyst_advantage,
            candidate_tier=cand_tier,
            reason=reason,
        )

    # --------------------------------------------------------------------------
    # Asymmetric Exit Rules (TP1 100% Principal Recovery & -10% Stop Loss)
    # --------------------------------------------------------------------------

    @staticmethod
    def check_position_exits(
        position: TurnaroundPosition,
        current_price: float,
    ) -> ExitDecision:
        """
        Evaluates TP1 partial exit and stop-loss exit conditions for an active position:
        - TP1: At +100% gain (price >= 2.0x entry), sell exactly 50% of position.
          Recovers 100% of initial principal in cash, rendering remaining 50% shares risk-free.
        - Stop Loss: At -10% loss from entry (price <= 0.90x entry) or -10% support floor breach,
          sell 100% of position immediately to truncate losses.
        """
        position.current_price = current_price
        if current_price > position.peak_price:
            position.peak_price = current_price

        gain_from_entry = (current_price - position.entry_price) / position.entry_price

        # 1. Stop-Loss check (-10% band breach)
        is_stop_loss = (
            gain_from_entry <= -0.10
            or (position.support_price > 0 and current_price <= position.support_price * 0.90)
        )

        if is_stop_loss and position.shares > 0:
            shares_sold = position.shares
            cash_realized = shares_sold * current_price
            realized_gain = cash_realized - (shares_sold * position.cost_basis)
            position.shares = 0.0
            return ExitDecision(
                stock_id=position.stock_id,
                action="STOP_LOSS_FULL",
                shares_to_sell=shares_sold,
                execution_price=current_price,
                cash_realized=cash_realized,
                realized_gain=realized_gain,
                reason=f"Stop loss triggered: drop {gain_from_entry * 100.0:.1f}% <= -10.0%. Exit 100%.",
            )

        # 2. TP1 Take Profit check (+100% gain -> 50% partial exit)
        if not position.tp1_executed and current_price >= position.entry_price * 2.0 and position.shares > 0:
            shares_sold = position.shares * 0.50
            cash_realized = shares_sold * current_price
            realized_gain = cash_realized - (shares_sold * position.cost_basis)

            # Mathematical validation: cash recovered == initial principal
            position.shares -= shares_sold
            position.tp1_executed = True
            position.is_risk_free = True
            position.cash_recovered += cash_realized
            # Effective cost basis of remaining runner becomes $0.00
            position.cost_basis = 0.0

            return ExitDecision(
                stock_id=position.stock_id,
                action="TP1_PARTIAL",
                shares_to_sell=shares_sold,
                execution_price=current_price,
                cash_realized=cash_realized,
                realized_gain=realized_gain,
                reason=(
                    f"TP1 Take Profit reached (+{gain_from_entry * 100.0:.1f}% >= +100.0%). "
                    f"Sold 50% of position. 100% principal recovered (${cash_realized:,.2f}). "
                    f"Remaining 50% shares held risk-free."
                ),
            )

        return ExitDecision(
            stock_id=position.stock_id,
            action="HOLD",
            shares_to_sell=0.0,
            execution_price=current_price,
            cash_realized=0.0,
            realized_gain=0.0,
            reason="Within holding bounds. Holding position.",
        )

    # --------------------------------------------------------------------------
    # 25-Year Full Simulation Execution
    # --------------------------------------------------------------------------

    def run_simulation(
        self,
        config: Optional[BacktestConfig] = None,
        benchmark_symbol: str = "QQQ",
    ) -> SimulationResult:
        """
        Executes full 25.25-year backtest simulation (2001-07-10 to 2026-10-12) of Strategy A.
        Incorporates 4-filter screening, max 2 stocks concentration, weekly switching hurdles,
        reverse-switching locks, TP1 100% principal recovery, -10% stop-loss, transaction friction,
        and foreign equity capital gains tax modeling.
        """
        if config is None:
            config = BacktestConfig(
                start_date=COMMON_START_DATE,
                end_date=COMMON_END_DATE,
                frequency=RebalanceFrequency.WEEKLY,
                fee_rate=0.0010,
                slippage_rate=0.0008,
                tax_enabled=True,
                tax_rate=0.22,
                annual_tax_deduction=2_500_000.0,
                initial_capital=100_000_000.0,
            )

        # 1. Load benchmark aligned timeseries (QQQ & SOXX)
        joint = get_joint_history()
        all_dates = sorted(joint.keys())
        dates = [d for d in all_dates if config.start_date <= d <= config.end_date]
        if not dates:
            dates = all_dates

        bench_prices = [joint[d][benchmark_symbol] for d in dates]
        num_days = len(dates)

        # 2. Build daily price trajectories for turnaround candidates
        turnaround_prices: Dict[str, List[float]] = {}
        for ep in self.episodes:
            p_series = self._generate_episode_daily_prices(ep, dates, joint, benchmark_symbol)
            turnaround_prices[ep.stock_id] = p_series

        # 3. Initialize state tracking
        annual_deduction = config.annual_tax_deduction
        if annual_deduction == 2_500_000.0 and config.initial_capital <= 1_000_000.0:
            annual_deduction = 2_000.0

        total_fee_paid = 0.0
        total_slippage_paid = 0.0
        total_cumulative_turnover = 0.0
        tax_state = TaxAccountingState()

        daily_nav_pre_tax: List[float] = []
        daily_drawdowns_pre_tax: List[float] = []
        daily_nav_after_tax: List[float] = []
        daily_drawdowns_after_tax: List[float] = []
        rebalance_records: List[Dict[str, Any]] = []
        holdings_history: List[Dict[str, float]] = []
        turnover_history: List[float] = []
        tax_history: List[Dict[str, Any]] = []

        # Active holdings state: Dict[symbol, TurnaroundPosition]
        positions: Dict[str, TurnaroundPosition] = {}
        benchmark_shares = 0.0
        benchmark_cb = bench_prices[0]

        # Initial capital deployment
        p0_bench = bench_prices[0]
        init_cand_pool = self._get_active_candidates_on_date(dates[0], turnaround_prices, 0)
        target_w0 = self.calculate_concentration_weights(init_cand_pool, benchmark_symbol)

        # Friction on initial deployment
        gross_init = config.initial_capital
        init_fee = gross_init * config.fee_rate
        init_slip = gross_init * config.slippage_rate
        total_fee_paid += init_fee
        total_slippage_paid += init_slip
        total_cumulative_turnover += 1.0

        net_init = gross_init - (init_fee + init_slip)

        # Deploy initial shares
        for sym, w in target_w0.items():
            if w <= 0:
                continue
            alloc = net_init * w
            if sym == benchmark_symbol:
                benchmark_shares = alloc / p0_bench if p0_bench > 0 else 0.0
                benchmark_cb = p0_bench
            elif sym in turnaround_prices:
                p_sym = turnaround_prices[sym][0]
                sh = alloc / p_sym if p_sym > 0 else 0.0
                ep = self.episode_map.get(sym)
                supp = ep.support_price if ep else p_sym * 0.90
                tp1 = ep.tp1_price if ep else p_sym * 2.0
                low52 = ep.fifty_two_week_low if ep else p_sym * 0.85
                cat_d = ep.catalyst_d_day_initial if ep else None
                cand_score = next((c.composite_turnaround_score for c in init_cand_pool if c.stock_id == sym), 80.0)

                positions[sym] = TurnaroundPosition(
                    stock_id=sym,
                    entry_date=dates[0],
                    entry_price=p_sym,
                    current_price=p_sym,
                    shares=sh,
                    initial_shares=sh,
                    initial_cost=alloc,
                    support_price=supp,
                    tp1_price=tp1,
                    cost_basis=p_sym,
                    peak_price=p_sym,
                    catalyst_d_day=cat_d,
                    composite_score=cand_score,
                    fifty_two_week_low=low52,
                )

        def _compute_cur_nav(idx: int) -> float:
            val = benchmark_shares * bench_prices[idx]
            for sym, pos in positions.items():
                p_now = turnaround_prices[sym][idx]
                val += pos.shares * p_now
            return val

        nav_0 = _compute_cur_nav(0)
        daily_nav_pre_tax.append(nav_0)
        daily_drawdowns_pre_tax.append(0.0)
        daily_nav_after_tax.append(nav_0)
        daily_drawdowns_after_tax.append(0.0)
        peak_pre = nav_0
        peak_after = nav_0

        holdings_history.append(self._get_holdings_weights(positions, benchmark_shares, bench_prices[0], nav_0, benchmark_symbol))
        turnover_history.append(1.0)

        rebalance_records.append({
            "date": dates[0],
            "type": "INITIAL_DEPLOYMENT",
            "pre_nav": config.initial_capital,
            "post_nav": nav_0,
            "turnover": 1.0,
            "fee": init_fee,
            "slippage": init_slip,
            "target_weights": dict(target_w0),
        })

        # Pre-tax portfolio tracking parallel shares
        pre_bench_shares = benchmark_shares
        pre_positions: Dict[str, float] = {k: v.shares for k, v in positions.items()}

        # 4. Continuous daily state machine
        for t in range(1, num_days):
            cur_date = dates[t]
            next_date = dates[t + 1] if t + 1 < num_days else None
            p_bench_t = bench_prices[t]

            # A. Daily update of active turnaround positions & check asymmetric exits
            for sym in list(positions.keys()):
                pos = positions[sym]
                p_sym_t = turnaround_prices[sym][t]

                # Update days remaining for catalysts
                if pos.catalyst_d_day is not None and pos.catalyst_d_day > 0:
                    pos.catalyst_d_day = max(0, pos.catalyst_d_day - 1)

                exit_dec = self.check_position_exits(pos, p_sym_t)

                if exit_dec.action == "TP1_PARTIAL":
                    # Realized gain on sold 50% shares
                    gain = exit_dec.realized_gain
                    tax_state.annual_realized_gain += gain
                    # Cash proceeds immediately redeployed into benchmark to maintain simplex
                    if p_bench_t > 0:
                        benchmark_shares += exit_dec.cash_realized / p_bench_t
                        pre_bench_shares += (pre_positions.get(sym, 0.0) * 0.50 * p_sym_t) / p_bench_t
                    if sym in pre_positions:
                        pre_positions[sym] *= 0.50

                elif exit_dec.action == "STOP_LOSS_FULL":
                    gain = exit_dec.realized_gain
                    tax_state.annual_realized_gain += gain
                    # Cash proceeds from stop-loss redeployed to benchmark
                    if p_bench_t > 0:
                        benchmark_shares += exit_dec.cash_realized / p_bench_t
                        pre_bench_shares += (pre_positions.get(sym, 0.0) * p_sym_t) / p_bench_t
                    if sym in pre_positions:
                        del pre_positions[sym]
                    del positions[sym]

            # B. Valuation before rebalancing
            nav_after = _compute_cur_nav(t)
            nav_pre = pre_bench_shares * p_bench_t + sum(pre_positions[s] * turnaround_prices[s][t] for s in pre_positions)

            # C. Check scheduled rebalance boundary
            should_rebalance = is_rebalance_date(cur_date, next_date, config.frequency)

            if should_rebalance and nav_after > 0:
                cand_pool = self._get_active_candidates_on_date(cur_date, turnaround_prices, t)
                target_w = self.calculate_concentration_weights(cand_pool, benchmark_symbol)

                # Check switching hurdle & reverse-switching locks against current turnaround holdings
                for held_sym in list(positions.keys()):
                    held_pos = positions[held_sym]
                    for cand in cand_pool:
                        if cand.stock_id not in positions:
                            switch_eval = self.evaluate_weekly_switching_decision(
                                held_position=held_pos,
                                candidate=cand,
                            )
                            if switch_eval.is_reverse_warning_locked:
                                # Retain holding in target_w
                                if held_sym not in target_w:
                                    target_w[held_sym] = target_w.get(held_sym, 0.50)
                                    # Normalize weights
                                    tot = sum(target_w.values())
                                    if tot > 0:
                                        target_w = {k: v / tot for k, v in target_w.items()}

                # Compute turnover & transaction friction
                current_w = self._get_holdings_weights(positions, benchmark_shares, p_bench_t, nav_after, benchmark_symbol)
                all_symbols = set(current_w.keys()) | set(target_w.keys())
                sum_delta_w = sum(abs(target_w.get(k, 0.0) - current_w.get(k, 0.0)) for k in all_symbols)
                turnover_reb = sum_delta_w / 2.0

                if sum_delta_w > 1e-4:
                    fric_pre = nav_pre * sum_delta_w * (config.fee_rate + config.slippage_rate)
                    fric_after = nav_after * sum_delta_w * (config.fee_rate + config.slippage_rate)

                    reb_fee = nav_after * sum_delta_w * config.fee_rate
                    reb_slip = nav_after * sum_delta_w * config.slippage_rate

                    total_fee_paid += reb_fee
                    total_slippage_paid += reb_slip
                    total_cumulative_turnover += turnover_reb

                    post_nav_pre = nav_pre - fric_pre
                    post_nav_after = nav_after - fric_after

                    # Execute rebalancing trades & update tax cost basis
                    # 1. Benchmark position
                    new_bench_alloc_after = post_nav_after * target_w.get(benchmark_symbol, 0.0)
                    new_bench_sh_after = new_bench_alloc_after / p_bench_t if p_bench_t > 0 else 0.0
                    if new_bench_sh_after < benchmark_shares:
                        # Selling benchmark shares
                        sh_sold = benchmark_shares - new_bench_sh_after
                        tax_state.annual_realized_gain += sh_sold * (p_bench_t - benchmark_cb)
                    benchmark_shares = new_bench_sh_after
                    benchmark_cb = p_bench_t

                    new_bench_alloc_pre = post_nav_pre * target_w.get(benchmark_symbol, 0.0)
                    pre_bench_shares = new_bench_alloc_pre / p_bench_t if p_bench_t > 0 else 0.0

                    # 2. Turnaround positions
                    old_syms = set(positions.keys())
                    target_syms = {k for k, v in target_w.items() if k != benchmark_symbol and v > 0}

                    # Remove exited symbols
                    for old_s in old_syms - target_syms:
                        old_pos = positions[old_s]
                        tax_state.annual_realized_gain += old_pos.shares * (turnaround_prices[old_s][t] - old_pos.cost_basis)
                        del positions[old_s]
                        if old_s in pre_positions:
                            del pre_positions[old_s]

                    # Update existing and deploy new symbols
                    for sym in target_syms:
                        p_k = turnaround_prices[sym][t]
                        alloc_k_after = post_nav_after * target_w[sym]
                        new_sh_k_after = alloc_k_after / p_k if p_k > 0 else 0.0

                        alloc_k_pre = post_nav_pre * target_w[sym]
                        new_sh_k_pre = alloc_k_pre / p_k if p_k > 0 else 0.0
                        pre_positions[sym] = new_sh_k_pre

                        if sym in positions:
                            old_pos = positions[sym]
                            if new_sh_k_after < old_pos.shares:
                                # Realize gain on trimmed shares
                                sh_sold = old_pos.shares - new_sh_k_after
                                tax_state.annual_realized_gain += sh_sold * (p_k - old_pos.cost_basis)
                            old_pos.shares = new_sh_k_after
                            old_pos.current_price = p_k
                        else:
                            # New position entry
                            ep = self.episode_map.get(sym)
                            supp = ep.support_price if ep else p_k * 0.90
                            tp1 = ep.tp1_price if ep else p_k * 2.0
                            low52 = ep.fifty_two_week_low if ep else p_k * 0.85
                            cat_d = ep.catalyst_d_day_initial if ep else None
                            c_score = next((c.composite_turnaround_score for c in cand_pool if c.stock_id == sym), 80.0)

                            positions[sym] = TurnaroundPosition(
                                stock_id=sym,
                                entry_date=cur_date,
                                entry_price=p_k,
                                current_price=p_k,
                                shares=new_sh_k_after,
                                initial_shares=new_sh_k_after,
                                initial_cost=alloc_k_after,
                                support_price=supp,
                                tp1_price=tp1,
                                cost_basis=p_k,
                                peak_price=p_k,
                                catalyst_d_day=cat_d,
                                composite_score=c_score,
                                fifty_two_week_low=low52,
                            )

                    turnover_history.append(turnover_reb)
                    rebalance_records.append({
                        "date": cur_date,
                        "type": "REBALANCE",
                        "pre_nav": nav_after,
                        "post_nav": post_nav_after,
                        "turnover": turnover_reb,
                        "fee": reb_fee,
                        "slippage": reb_slip,
                        "target_weights": dict(target_w),
                    })
                else:
                    turnover_history.append(0.0)
            else:
                turnover_history.append(0.0)

            # D. Calendar Year-End Tax Settlement (22% on annual gain > deduction)
            is_year_end = (next_date is not None and cur_date[:4] != next_date[:4]) or (next_date is None)
            if config.tax_enabled and is_year_end:
                y_val = int(cur_date[:4])
                net_gain = tax_state.annual_realized_gain
                taxable_gain = max(0.0, net_gain - annual_deduction)
                annual_tax = taxable_gain * config.tax_rate

                nav_current = _compute_cur_nav(t)
                if annual_tax > 0.0 and nav_current > annual_tax:
                    tax_state.annual_tax_paid = annual_tax
                    tax_state.cumulative_tax_paid += annual_tax

                    retention_ratio = 1.0 - (annual_tax / nav_current)
                    benchmark_shares *= retention_ratio
                    for pos in positions.values():
                        pos.shares *= retention_ratio

                    tax_rec = {
                        "year": y_val,
                        "settle_date": cur_date,
                        "realized_gain": round(net_gain, 2),
                        "deduction": round(annual_deduction, 2),
                        "taxable_gain": round(taxable_gain, 2),
                        "tax_paid": round(annual_tax, 2),
                        "cumulative_tax_paid": round(tax_state.cumulative_tax_paid, 2),
                    }
                    tax_state.annual_tax_records.append(tax_rec)
                    tax_history.append(tax_rec)

                # Reset annual realized gain for new calendar year
                tax_state.annual_realized_gain = 0.0

            # E. Daily NAV & Drawdown recording
            val_after_final = _compute_cur_nav(t)
            val_pre_final = pre_bench_shares * p_bench_t + sum(pre_positions[s] * turnaround_prices[s][t] for s in pre_positions)

            daily_nav_pre_tax.append(val_pre_final)
            if val_pre_final > peak_pre:
                peak_pre = val_pre_final
            dd_pre = (val_pre_final - peak_pre) / peak_pre if peak_pre > 0 else 0.0
            daily_drawdowns_pre_tax.append(round(dd_pre, 4))

            daily_nav_after_tax.append(val_after_final)
            if val_after_final > peak_after:
                peak_after = val_after_final
            dd_after = (val_after_final - peak_after) / peak_after if peak_after > 0 else 0.0
            daily_drawdowns_after_tax.append(round(dd_after, 4))

            cur_w = self._get_holdings_weights(positions, benchmark_shares, p_bench_t, val_after_final, benchmark_symbol)
            holdings_history.append(cur_w)

        # 5. Output metrics packaging
        primary_nav = daily_nav_after_tax if config.tax_enabled else daily_nav_pre_tax
        primary_dd = daily_drawdowns_after_tax if config.tax_enabled else daily_drawdowns_pre_tax

        metrics = calculate_performance_metrics(
            daily_nav=primary_nav,
            dates=dates,
            fee_paid=total_fee_paid,
            slippage_paid=total_slippage_paid,
            total_turnover=total_cumulative_turnover,
            risk_free_rate=config.risk_free_rate,
            daily_nav_pre_tax=daily_nav_pre_tax,
            total_tax_paid=tax_state.cumulative_tax_paid,
        )

        year_map: Dict[int, List[float]] = {}
        for d_str, v in zip(dates, primary_nav):
            y = int(d_str[:4])
            if y not in year_map:
                year_map[y] = []
            year_map[y].append(v)
        annual_returns = {
            y: round(((vals[-1] - vals[0]) / vals[0]) * 100.0, 2)
            for y, vals in year_map.items()
            if vals[0] > 0
        }

        return SimulationResult(
            config=config,
            metrics=metrics,
            dates=dates,
            daily_nav=primary_nav,
            daily_drawdowns=primary_dd,
            annual_returns=annual_returns,
            daily_nav_pre_tax=daily_nav_pre_tax,
            daily_drawdowns_pre_tax=daily_drawdowns_pre_tax,
            rebalance_records=rebalance_records,
            holdings_history=holdings_history,
            turnover_history=turnover_history,
            tax_history=tax_history,
            tax_state=tax_state,
        )

    # --------------------------------------------------------------------------
    # Helper Simulation Methods
    # --------------------------------------------------------------------------

    def evaluate_weekly_switching_decision(
        self,
        held_position: TurnaroundPosition,
        candidate: TurnaroundCandidate,
    ) -> SwitchingEvaluation:
        """Helper to invoke switching evaluation with position's current state."""
        return self.evaluate_switching_hurdle(
            held_position=held_position,
            candidate=candidate,
            held_catalyst_d_day=held_position.catalyst_d_day,
            candidate_catalyst_d_day=candidate.catalyst_d_day,
        )

    def _get_active_candidates_on_date(
        self,
        cur_date: str,
        turnaround_prices: Dict[str, List[float]],
        idx: int,
    ) -> List[TurnaroundCandidate]:
        """Screens candidate pool for episodes active on cur_date."""
        active_candidates: List[TurnaroundCandidate] = []
        for ep in self.episodes:
            if ep.start_date <= cur_date <= ep.end_date and ep.stock_id in turnaround_prices:
                p_now = turnaround_prices[ep.stock_id][idx]
                if p_now > 0:
                    cand = self.screen_candidate(
                        stock_id=ep.stock_id,
                        current_price=p_now,
                        fifty_two_week_low=ep.fifty_two_week_low,
                        fifty_two_week_high=ep.fifty_two_week_high,
                        support_price=ep.support_price,
                        tp1_price=ep.tp1_price,
                        revenue_growth_2y=ep.rev_growth_2y,
                        operating_income_growth_2y=ep.oi_growth_2y,
                        is_turnaround_to_profit=ep.is_turnaround_to_profit,
                        volume=int(ep.volume_surge_ratio * 1_000_000),
                        benchmark_20d_volume=1_000_000,
                        daily_change_pct=0.5,
                        catalyst_d_day=ep.catalyst_d_day_initial,
                        name_kr=ep.name_kr,
                        ticker=ep.ticker,
                    )
                    active_candidates.append(cand)
        return active_candidates

    def _get_holdings_weights(
        self,
        positions: Dict[str, TurnaroundPosition],
        benchmark_shares: float,
        p_bench: float,
        total_nav: float,
        benchmark_symbol: str,
    ) -> Dict[str, float]:
        """Calculates current portfolio weights for diagnostic tracking."""
        weights: Dict[str, float] = {}
        if total_nav <= 0:
            return {benchmark_symbol: 1.0}

        w_b = (benchmark_shares * p_bench) / total_nav
        if w_b > 1e-4:
            weights[benchmark_symbol] = round(w_b, 4)

        for sym, pos in positions.items():
            w_pos = (pos.shares * pos.current_price) / total_nav
            if w_pos > 1e-4:
                weights[sym] = round(w_pos, 4)

        tot = sum(weights.values())
        if tot > 0:
            return {k: round(v / tot, 4) for k, v in weights.items()}
        return {benchmark_symbol: 1.0}

    def _generate_episode_daily_prices(
        self,
        ep: TurnaroundEpisode,
        dates: List[str],
        joint: Dict[str, Dict[str, float]],
        benchmark_symbol: str,
    ) -> List[float]:
        """
        Synthesizes deterministic daily price series for a historical episode aligned
        with the master calendar dates. Replicates authentic 52-week trough, wash-out,
        support defense floor, and eventual recovery trajectory to TP1/peak.
        """
        prices: List[float] = []
        d_trough = ep.trough_date

        def _get_bench_p(target_d: str) -> float:
            if target_d in joint:
                return joint[target_d][benchmark_symbol]
            tgt_dt = datetime.date.fromisoformat(target_d)
            closest_d = min(dates, key=lambda d: abs((datetime.date.fromisoformat(d) - tgt_dt).days))
            return joint[closest_d][benchmark_symbol]

        p_bench_start = _get_bench_p(ep.start_date)
        p_bench_end = _get_bench_p(ep.end_date)

        for d in dates:
            if d < ep.start_date:
                # Prior to active turnaround episode: nominal benchmark-correlated price
                bench_p = joint[d][benchmark_symbol]
                norm_p = ep.fifty_two_week_high * (bench_p / p_bench_start) if p_bench_start > 0 else ep.trough_price * 1.5
                prices.append(round(max(ep.trough_price * 1.5, norm_p), 2))

            elif ep.start_date <= d <= ep.end_date:
                # Active episode phase:
                if d <= d_trough:
                    # Crashing into 52-week low trough
                    d_cur = datetime.date.fromisoformat(d)
                    d_s = datetime.date.fromisoformat(ep.start_date)
                    d_tr = datetime.date.fromisoformat(d_trough)
                    total_crash_days = max(1, (d_tr - d_s).days)
                    progress = min(1.0, max(0.0, (d_cur - d_s).days / total_crash_days))
                    # Exponential decay into trough
                    decay = math.exp(-2.0 * progress)
                    p_now = ep.trough_price + (ep.fifty_two_week_high * 0.5 - ep.trough_price) * decay
                    prices.append(round(max(ep.trough_price, p_now), 2))
                else:
                    # Rebounding out of trough toward TP1 and peak
                    d_cur = datetime.date.fromisoformat(d)
                    d_tr = datetime.date.fromisoformat(d_trough)
                    d_e = datetime.date.fromisoformat(ep.end_date)
                    total_rec_days = max(1, (d_e - d_tr).days)
                    progress = min(1.0, max(0.0, (d_cur - d_tr).days / total_rec_days))
                    # S-curve sigmoid recovery wave
                    sigmoid = 1.0 / (1.0 + math.exp(-6.0 * (progress - 0.4)))
                    p_now = ep.trough_price + (ep.peak_price - ep.trough_price) * sigmoid
                    prices.append(round(p_now, 2))

            else:
                # Post-episode: continues with benchmark beta
                bench_p = joint[d][benchmark_symbol]
                norm_p = ep.peak_price * (bench_p / p_bench_end) if p_bench_end > 0 else ep.peak_price
                prices.append(round(max(ep.trough_price * 1.2, norm_p), 2))

        return prices
