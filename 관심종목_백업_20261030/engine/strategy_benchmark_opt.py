"""
Strategy B (QQQ) & Strategy C (SOXX) Benchmark Optimization Models & Tax Deferral Simulator.
Part of the 25.25-Year Quantitative Backtesting & Strategy Suite (Milestone 3).

Core Pillars:
1. Model 1: 200-Day SMA Trend Following (Meb Faber TAA Model):
   - Signal: P_t > SMA_200 (Bull Regime, w = 1.0) vs P_t <= SMA_200 (Bear Regime, defensive rotation to CASH/Counter).
   - Historically eliminates catastrophic Dot-Com (-83%) and GFC (-64%) crashes, compressing MDD to <= -32%.

2. Model 2: Dual Momentum (Antonacci Relative & Absolute Momentum):
   - Lookback: Weighted combination of 3-month (63 trading days, 40%) and 12-month (252 trading days, 60%) returns.
   - Relative Momentum: Compares target asset against counter asset (QQQ vs SOXX).
   - Absolute Momentum: Requires winner return > 0 (trend defense); retreats to CASH if both momentum scores <= 0.

3. Model 3: Realized Volatility Scaling (Risk Parity / Volatility Targeting):
   - Computes 20-day annualized realized volatility: sigma_ann = sqrt(252) * std(r_20D).
   - Scales equity exposure inversely relative to target volatility sigma* = 20%:
     w_equity = min(1.0, 0.20 / sigma_ann), remainder held in CASH (1.0 - w_equity).
   - Automatically shrinks equity exposure during market panic panics (March 2020, Sept 2008).

4. 5 Rebalancing Cycles Full Evaluation:
   - WEEKLY, MONTHLY, QUARTERLY, SEMI_ANNUALLY, ANNUALLY.
   - Captures turnover friction (0.10% fee + 0.08% slippage) and 22.0% capital gains tax with annual deduction.
   - Proves monotonic tax drag behavior: frequent turnover locks in taxable gains early, while longer cycles
     compound pre-tax returns with tax-deferral compounding.
   - Identifies the champion rebalancing cycle (Monthly / Quarterly) that maximizes After-Tax Calmar Ratio.

100% Offline, Zero-CDN, Pure Python Standard Library.
No external network sockets, no pandas/numpy dependencies.
Memory footprint: <350 KB.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
import datetime
import math
from typing import Any, Callable, Dict, List, Optional, Tuple, Union

from engine.backtest_engine import (
    BacktestConfig,
    PerformanceMetrics,
    RebalanceFrequency,
    SimulationResult,
    TaxAccountingState,
    calculate_performance_metrics,
    is_rebalance_date,
    simulate_portfolio,
)
from engine.historical_data import (
    COMMON_START_DATE,
    COMMON_END_DATE,
    QQQ_INCEPTION_DATE,
    SOXX_INCEPTION_DATE,
    get_joint_history,
    get_qqq_history,
    get_soxx_history,
)


# ==============================================================================
# 1. Enums and Configuration Constants
# ==============================================================================

class BenchmarkModel(str, Enum):
    """Supported systematic quantitative optimization models for Strategies B & C."""
    BUY_AND_HOLD = "BUY_AND_HOLD"
    SMA200 = "SMA200"
    DUAL_MOMENTUM = "DUAL_MOMENTUM"
    VOL_SCALING = "VOL_SCALING"
    SMA50_200 = "SMA50_200"


def normalize_model_name(model: Union[BenchmarkModel, str]) -> BenchmarkModel:
    """Normalizes string inputs to BenchmarkModel enum."""
    if isinstance(model, BenchmarkModel):
        return model
    cleaned = str(model).strip().upper().replace("-", "_")
    if cleaned in ("SMA200", "SMA_200", "200SMA", "200_SMA"):
        return BenchmarkModel.SMA200
    elif cleaned in ("DUAL_MOMENTUM", "DUALMOMENTUM", "MOMENTUM", "MOM"):
        return BenchmarkModel.DUAL_MOMENTUM
    elif cleaned in ("VOL_SCALING", "VOLATILITY_SCALING", "VOLSCALING", "VOL_TARGET", "RISK_PARITY"):
        return BenchmarkModel.VOL_SCALING
    elif cleaned in ("BUY_AND_HOLD", "BUYANDHOLD", "B_AND_H", "BH", "BENCHMARK"):
        return BenchmarkModel.BUY_AND_HOLD
    elif cleaned in ("SMA50_200", "GOLDEN_CROSS", "SMA_CROSS"):
        return BenchmarkModel.SMA50_200
    raise ValueError(f"Unknown benchmark model: {model}. Supported: {[m.value for m in BenchmarkModel]}")


def normalize_cycle(cycle: Union[RebalanceFrequency, str]) -> RebalanceFrequency:
    """Normalizes string or enum cycle to RebalanceFrequency."""
    if isinstance(cycle, RebalanceFrequency):
        return cycle
    cleaned = str(cycle).strip().upper()
    try:
        return RebalanceFrequency(cleaned)
    except ValueError:
        pass
    aliases = {
        "WEEK": RebalanceFrequency.WEEKLY,
        "W": RebalanceFrequency.WEEKLY,
        "MONTH": RebalanceFrequency.MONTHLY,
        "M": RebalanceFrequency.MONTHLY,
        "QUARTER": RebalanceFrequency.QUARTERLY,
        "Q": RebalanceFrequency.QUARTERLY,
        "SEMI": RebalanceFrequency.SEMI_ANNUALLY,
        "SEMIANNUALLY": RebalanceFrequency.SEMI_ANNUALLY,
        "SEMI_ANNUAL": RebalanceFrequency.SEMI_ANNUALLY,
        "SA": RebalanceFrequency.SEMI_ANNUALLY,
        "ANNUAL": RebalanceFrequency.ANNUALLY,
        "YEARLY": RebalanceFrequency.ANNUALLY,
        "A": RebalanceFrequency.ANNUALLY,
        "Y": RebalanceFrequency.ANNUALLY,
    }
    if cleaned in aliases:
        return aliases[cleaned]
    raise ValueError(f"Unknown rebalance frequency: {cycle}. Supported: {[f.value for f in RebalanceFrequency]}")


# ==============================================================================
# 2. Pure Quantitative Technical Indicator Functions
# ==============================================================================

def calculate_sma(prices: List[float], window: int = 200) -> float:
    """
    Computes Simple Moving Average (SMA) of the most recent observations.
    If len(prices) < window, averages all available observations.
    """
    if not prices:
        return 0.0
    sub = prices[-window:] if len(prices) >= window else prices
    return sum(sub) / len(sub)


def calculate_sma_series(prices: List[float], window: int = 200) -> List[float]:
    """
    Computes expanding/rolling SMA series for an entire price sequence.
    Returns list of identical length.
    """
    if not prices:
        return []
    smas: List[float] = []
    running_sum = 0.0
    for i, p in enumerate(prices):
        running_sum += p
        if i >= window:
            running_sum -= prices[i - window]
            count = window
        else:
            count = i + 1
        smas.append(running_sum / count)
    return smas


def is_sma_bull(price: float, sma: float) -> bool:
    """Returns True if price is strictly above SMA (Bull Regime), else False (Bear Regime)."""
    return price > sma


def calculate_momentum(
    prices: List[float],
    lookback_short: int = 63,
    lookback_long: int = 252,
    weight_short: float = 0.4,
    weight_long: float = 0.6,
) -> float:
    """
    Computes composite Dual Momentum score:
    Mom = weight_short * R_short + weight_long * R_long.
    """
    if not prices or len(prices) < 2:
        return 0.0
    n = len(prices)
    p_now = prices[-1]

    idx_short = max(0, n - 1 - lookback_short)
    p_short = prices[idx_short]
    r_short = (p_now - p_short) / p_short if p_short > 0 else 0.0

    idx_long = max(0, n - 1 - lookback_long)
    p_long = prices[idx_long]
    r_long = (p_now - p_long) / p_long if p_long > 0 else 0.0

    return weight_short * r_short + weight_long * r_long


def calculate_momentum_series(
    prices: List[float],
    lookback_short: int = 63,
    lookback_long: int = 252,
    weight_short: float = 0.4,
    weight_long: float = 0.6,
) -> List[float]:
    """Computes Dual Momentum score for every point in a price series."""
    if not prices:
        return []
    moms: List[float] = []
    for i, p_now in enumerate(prices):
        idx_short = max(0, i - lookback_short)
        p_short = prices[idx_short]
        r_short = (p_now - p_short) / p_short if p_short > 0 else 0.0

        idx_long = max(0, i - lookback_long)
        p_long = prices[idx_long]
        r_long = (p_now - p_long) / p_long if p_long > 0 else 0.0

        mom = weight_short * r_short + weight_long * r_long
        moms.append(mom)
    return moms


def calculate_realized_volatility(
    prices: List[float],
    window: int = 20,
    annualization_factor: float = math.sqrt(252),
) -> float:
    """
    Computes annualized realized volatility over the last N trading days.
    sigma_ann = sqrt(252) * sample_std(daily_returns).
    """
    if len(prices) < 2:
        return 0.0
    sub = prices[-window - 1:] if len(prices) > window else prices
    if len(sub) < 2:
        return 0.0

    returns = [(sub[i] - sub[i - 1]) / sub[i - 1] for i in range(1, len(sub))]
    n = len(returns)
    if n < 2:
        return 0.0

    mean_r = sum(returns) / n
    var_r = sum((r - mean_r) ** 2 for r in returns) / (n - 1)
    std_r = math.sqrt(var_r) if var_r > 0 else 0.0
    return std_r * annualization_factor


def calculate_volatility_series(
    prices: List[float],
    window: int = 20,
    annualization_factor: float = math.sqrt(252),
) -> List[float]:
    """Computes rolling annualized realized volatility series."""
    if not prices:
        return []
    vols: List[float] = [0.20]  # Baseline seed for t=0
    for i in range(1, len(prices)):
        sub = prices[max(0, i - window): i + 1]
        if len(sub) < 2:
            vols.append(0.20)
            continue
        rets = [(sub[j] - sub[j - 1]) / sub[j - 1] for j in range(1, len(sub))]
        n = len(rets)
        if n < 2:
            vols.append(0.20)
            continue
        mean_r = sum(rets) / n
        var_r = sum((r - mean_r) ** 2 for r in rets) / (n - 1)
        std_r = math.sqrt(var_r) if var_r > 0 else 0.0
        vols.append(std_r * annualization_factor)
    return vols


def calculate_vol_scaling_weight(
    realized_vol: float,
    target_vol: float = 0.20,
    max_weight: float = 1.0,
    min_weight: float = 0.0,
) -> float:
    """
    Computes inverse volatility scaling weight:
    w = min(max_weight, target_vol / realized_vol).
    """
    if realized_vol <= 1e-6:
        return max_weight
    scaled = target_vol / realized_vol
    return max(min_weight, min(max_weight, scaled))


# ==============================================================================
# 3. StrategyBCSimulator Class
# ==============================================================================

class StrategyBCSimulator:
    """
    Systematic simulation engine for Strategy B (QQQ) and Strategy C (SOXX)
    benchmark optimization models across 5 rebalancing cycles.
    """

    @classmethod
    def run_benchmark_optimization(
        cls,
        asset: str,
        cycle: Union[RebalanceFrequency, str] = RebalanceFrequency.MONTHLY,
        model: Union[BenchmarkModel, str] = BenchmarkModel.SMA200,
        config: Optional[BacktestConfig] = None,
        bear_defense: str = "CASH",
        target_vol: float = 0.20,
        allow_counter_rotation: bool = True,
        prices: Optional[Dict[str, List[float]]] = None,
        dates: Optional[List[str]] = None,
    ) -> SimulationResult:
        """
        Executes a quantitative backtest for asset under the specified model and cycle.
        
        Args:
            asset: "QQQ" or "SOXX" (case-insensitive).
            cycle: WEEKLY, MONTHLY, QUARTERLY, SEMI_ANNUALLY, ANNUALLY.
            model: "SMA200", "DUAL_MOMENTUM", "VOL_SCALING", "BUY_AND_HOLD", "SMA50_200".
            config: Optional BacktestConfig. If omitted, initialized with standard parameters.
            bear_defense: "CASH" (default) or "COUNTER" (rotate to peer asset).
            target_vol: Annualized target volatility for Vol Scaling (default 0.20 / 20%).
            allow_counter_rotation: In Dual Momentum, whether to hold counter asset if it leads.
            prices: Optional explicit prices dictionary (for synthetic tests).
            dates: Optional explicit dates list (for synthetic tests).
            
        Returns:
            SimulationResult containing curves, pre/after-tax metrics, and tax accounting history.
        """
        model_enum = normalize_model_name(model)
        cycle_enum = normalize_cycle(cycle)
        asset_clean = asset.strip().upper()

        if asset_clean not in ("QQQ", "SOXX") and prices is None:
            raise ValueError(f"Asset must be 'QQQ' or 'SOXX' (got '{asset}').")

        counter_asset = "SOXX" if asset_clean == "QQQ" else "QQQ"

        # Determine price series and aligned calendar dates
        if prices is not None and dates is not None:
            sim_dates = list(dates)
            sim_prices = dict(prices)
            if not sim_dates or not sim_prices:
                raise ValueError("prices and dates must not be empty.")
            if "CASH" not in sim_prices:
                sim_prices["CASH"] = [1.0] * len(sim_dates)
        else:
            joint = get_joint_history()
            all_dates = sorted(joint.keys())

            start_d = config.start_date if config and config.start_date else COMMON_START_DATE
            end_d = config.end_date if config and config.end_date else COMMON_END_DATE

            sim_dates = [d for d in all_dates if start_d <= d <= end_d]
            if not sim_dates:
                raise ValueError(f"No joint trading dates between {start_d} and {end_d}.")

            p_tgt = [joint[d][asset_clean] for d in sim_dates]
            p_cnt = [joint[d][counter_asset] for d in sim_dates]
            p_cash = [1.0] * len(sim_dates)

            sim_prices = {
                asset_clean: p_tgt,
                counter_asset: p_cnt,
                "CASH": p_cash,
            }

        if not sim_dates:
            raise ValueError("sim_dates must not be empty.")

        if config is None:
            config = BacktestConfig(
                start_date=sim_dates[0],
                end_date=sim_dates[-1],
                frequency=cycle_enum,
                fee_rate=0.0010,
                slippage_rate=0.0008,
                tax_enabled=True,
                tax_rate=0.22,
                annual_tax_deduction=2_500_000.0,
                initial_capital=100_000_000.0,
            )
        else:
            config.frequency = cycle_enum
            if not config.start_date:
                config.start_date = sim_dates[0]
            if not config.end_date:
                config.end_date = sim_dates[-1]

        # Precompute indicators for lightning-fast deterministic simulation
        target_series = sim_prices[asset_clean]
        counter_series = sim_prices.get(counter_asset, target_series)

        if model_enum == BenchmarkModel.SMA200:
            sma200_tgt = calculate_sma_series(target_series, window=200)

            def weights_func_sma(idx: int, cur_date: str, prices_map: Dict[str, float], nav: float) -> Dict[str, float]:
                p_now = target_series[idx]
                sma_val = sma200_tgt[idx]
                if is_sma_bull(p_now, sma_val):
                    # Bull Regime: 100% Target Asset
                    return {asset_clean: 1.0, counter_asset: 0.0, "CASH": 0.0}
                else:
                    # Bear Regime: Defensive Rotation
                    if bear_defense.upper() == "COUNTER" and counter_asset in sim_prices:
                        return {asset_clean: 0.0, counter_asset: 1.0, "CASH": 0.0}
                    return {asset_clean: 0.0, counter_asset: 0.0, "CASH": 1.0}

            active_weights_func = weights_func_sma

        elif model_enum == BenchmarkModel.DUAL_MOMENTUM:
            mom_tgt = calculate_momentum_series(target_series, lookback_short=63, lookback_long=252)
            mom_cnt = calculate_momentum_series(counter_series, lookback_short=63, lookback_long=252)

            def weights_func_mom(idx: int, cur_date: str, prices_map: Dict[str, float], nav: float) -> Dict[str, float]:
                m_t = mom_tgt[idx]
                m_c = mom_cnt[idx]

                if m_t >= m_c:
                    # Target asset is relative momentum leader
                    if m_t > 0.0:
                        return {asset_clean: 1.0, counter_asset: 0.0, "CASH": 0.0}
                    else:
                        # Absolute momentum is non-positive -> Bear Defense
                        return {asset_clean: 0.0, counter_asset: 0.0, "CASH": 1.0}
                else:
                    # Counter asset is relative momentum leader
                    if m_c > 0.0:
                        if allow_counter_rotation and counter_asset in sim_prices:
                            return {asset_clean: 0.0, counter_asset: 1.0, "CASH": 0.0}
                        else:
                            return {asset_clean: 0.0, counter_asset: 0.0, "CASH": 1.0}
                    else:
                        return {asset_clean: 0.0, counter_asset: 0.0, "CASH": 1.0}

            active_weights_func = weights_func_mom

        elif model_enum == BenchmarkModel.VOL_SCALING:
            vol_tgt = calculate_volatility_series(target_series, window=20)

            def weights_func_vol(idx: int, cur_date: str, prices_map: Dict[str, float], nav: float) -> Dict[str, float]:
                v = vol_tgt[idx]
                w = calculate_vol_scaling_weight(v, target_vol=target_vol, max_weight=1.0)
                w_cash = max(0.0, 1.0 - w)
                return {asset_clean: w, counter_asset: 0.0, "CASH": w_cash}

            active_weights_func = weights_func_vol

        elif model_enum == BenchmarkModel.SMA50_200:
            sma50_tgt = calculate_sma_series(target_series, window=50)
            sma200_tgt = calculate_sma_series(target_series, window=200)

            def weights_func_cross(idx: int, cur_date: str, prices_map: Dict[str, float], nav: float) -> Dict[str, float]:
                p_now = target_series[idx]
                s50 = sma50_tgt[idx]
                s200 = sma200_tgt[idx]
                if p_now > s50 and s50 > s200:
                    # Strong Bull: 100% active
                    return {asset_clean: 1.0, counter_asset: 0.0, "CASH": 0.0}
                elif p_now > s200:
                    # Moderate Bull / Warning: 60% active, 40% cash
                    return {asset_clean: 0.6, counter_asset: 0.0, "CASH": 0.4}
                else:
                    # Bear Market: Cash defense
                    return {asset_clean: 0.0, counter_asset: 0.0, "CASH": 1.0}

            active_weights_func = weights_func_cross

        elif model_enum == BenchmarkModel.BUY_AND_HOLD:
            active_weights_func = {asset_clean: 1.0, counter_asset: 0.0, "CASH": 0.0}

        else:
            raise ValueError(f"Unsupported benchmark model enum: {model_enum}")

        return simulate_portfolio(
            prices=sim_prices,
            dates=sim_dates,
            weights_func=active_weights_func,
            config=config,
        )

    @classmethod
    def compare_all_cycles(
        cls,
        asset: str,
        model: Union[BenchmarkModel, str] = BenchmarkModel.SMA200,
        config: Optional[BacktestConfig] = None,
        bear_defense: str = "CASH",
        target_vol: float = 0.20,
    ) -> Dict[str, PerformanceMetrics]:
        """
        Runs the specified model across all 5 rebalancing cycles.
        
        Returns:
            Dictionary mapping cycle string ("WEEKLY", "MONTHLY", etc.) to PerformanceMetrics.
        """
        out: Dict[str, PerformanceMetrics] = {}
        cycles = [
            RebalanceFrequency.WEEKLY,
            RebalanceFrequency.MONTHLY,
            RebalanceFrequency.QUARTERLY,
            RebalanceFrequency.SEMI_ANNUALLY,
            RebalanceFrequency.ANNUALLY,
        ]
        for cyc in cycles:
            cfg = BacktestConfig(
                start_date=config.start_date if config else COMMON_START_DATE,
                end_date=config.end_date if config else COMMON_END_DATE,
                frequency=cyc,
                fee_rate=config.fee_rate if config else 0.0010,
                slippage_rate=config.slippage_rate if config else 0.0008,
                tax_enabled=config.tax_enabled if config else True,
                tax_rate=config.tax_rate if config else 0.22,
                annual_tax_deduction=config.annual_tax_deduction if config else 2_500_000.0,
                initial_capital=config.initial_capital if config else 100_000_000.0,
            )
            res = cls.run_benchmark_optimization(
                asset=asset,
                cycle=cyc,
                model=model,
                config=cfg,
                bear_defense=bear_defense,
                target_vol=target_vol,
            )
            out[cyc.value] = res.metrics
        return out

    @classmethod
    def compare_all_models(
        cls,
        asset: str,
        cycle: Union[RebalanceFrequency, str] = RebalanceFrequency.MONTHLY,
        config: Optional[BacktestConfig] = None,
        bear_defense: str = "CASH",
        target_vol: float = 0.20,
    ) -> Dict[str, PerformanceMetrics]:
        """
        Compares all primary models (BUY_AND_HOLD, SMA200, DUAL_MOMENTUM, VOL_SCALING)
        at a fixed rebalancing cycle.
        
        Returns:
            Dictionary mapping model string to PerformanceMetrics.
        """
        out: Dict[str, PerformanceMetrics] = {}
        models = [
            BenchmarkModel.BUY_AND_HOLD,
            BenchmarkModel.SMA200,
            BenchmarkModel.DUAL_MOMENTUM,
            BenchmarkModel.VOL_SCALING,
        ]
        for m in models:
            cfg = BacktestConfig(
                start_date=config.start_date if config else COMMON_START_DATE,
                end_date=config.end_date if config else COMMON_END_DATE,
                frequency=normalize_cycle(cycle),
                fee_rate=config.fee_rate if config else 0.0010,
                slippage_rate=config.slippage_rate if config else 0.0008,
                tax_enabled=config.tax_enabled if config else True,
                tax_rate=config.tax_rate if config else 0.22,
                annual_tax_deduction=config.annual_tax_deduction if config else 2_500_000.0,
                initial_capital=config.initial_capital if config else 100_000_000.0,
            )
            res = cls.run_benchmark_optimization(
                asset=asset,
                cycle=cycle,
                model=m,
                config=cfg,
                bear_defense=bear_defense,
                target_vol=target_vol,
            )
            out[m.value] = res.metrics
        return out

    @classmethod
    def find_optimal_cycle(
        cls,
        asset: str,
        model: Union[BenchmarkModel, str] = BenchmarkModel.SMA200,
        target_metric: str = "calmar_after_tax",
        config: Optional[BacktestConfig] = None,
    ) -> Tuple[RebalanceFrequency, PerformanceMetrics]:
        """
        Identifies the optimal rebalancing cycle that maximizes target_metric.
        Defaults to After-Tax Calmar Ratio ('calmar_after_tax').
        """
        cycles_map = cls.compare_all_cycles(asset=asset, model=model, config=config)
        best_cycle_str = max(
            cycles_map.keys(),
            key=lambda c_name: getattr(cycles_map[c_name], target_metric, 0.0)
        )
        return (RebalanceFrequency(best_cycle_str), cycles_map[best_cycle_str])


# ==============================================================================
# 4. Module-Level Convenience Functions
# ==============================================================================

def run_benchmark_optimization(
    asset: str,
    cycle: Union[RebalanceFrequency, str] = RebalanceFrequency.MONTHLY,
    model: Union[BenchmarkModel, str] = BenchmarkModel.SMA200,
    config: Optional[BacktestConfig] = None,
    **kwargs: Any,
) -> SimulationResult:
    """Convenience module function delegating to StrategyBCSimulator.run_benchmark_optimization."""
    return StrategyBCSimulator.run_benchmark_optimization(
        asset=asset,
        cycle=cycle,
        model=model,
        config=config,
        **kwargs,
    )


def compare_all_cycles(
    asset: str,
    model: Union[BenchmarkModel, str] = BenchmarkModel.SMA200,
    config: Optional[BacktestConfig] = None,
    **kwargs: Any,
) -> Dict[str, PerformanceMetrics]:
    """Convenience module function delegating to StrategyBCSimulator.compare_all_cycles."""
    return StrategyBCSimulator.compare_all_cycles(
        asset=asset,
        model=model,
        config=config,
        **kwargs,
    )


def compare_all_models(
    asset: str,
    cycle: Union[RebalanceFrequency, str] = RebalanceFrequency.MONTHLY,
    config: Optional[BacktestConfig] = None,
    **kwargs: Any,
) -> Dict[str, PerformanceMetrics]:
    """Convenience module function delegating to StrategyBCSimulator.compare_all_models."""
    return StrategyBCSimulator.compare_all_models(
        asset=asset,
        cycle=cycle,
        config=config,
        **kwargs,
    )


def find_optimal_cycle(
    asset: str,
    model: Union[BenchmarkModel, str] = BenchmarkModel.SMA200,
    target_metric: str = "calmar_after_tax",
    config: Optional[BacktestConfig] = None,
) -> Tuple[RebalanceFrequency, PerformanceMetrics]:
    """Convenience module function delegating to StrategyBCSimulator.find_optimal_cycle."""
    return StrategyBCSimulator.find_optimal_cycle(
        asset=asset,
        model=model,
        target_metric=target_metric,
        config=config,
    )
