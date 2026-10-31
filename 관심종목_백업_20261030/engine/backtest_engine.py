"""
Quantitative Backtesting Engine & Performance Evaluation Suite with Capital Gains Tax Modeling.
Part of the 25.25-Year Quantitative Backtesting & Strategy Suite.

100% Offline, Zero-CDN, Pure Python Standard Library.
No external network sockets, no pandas/numpy dependencies.
Memory footprint: <350 KB.
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Callable, Dict, List, Optional, Tuple, Union
import datetime
import math


class RebalanceFrequency(str, Enum):
    """Supported portfolio rebalancing frequencies."""
    WEEKLY = "WEEKLY"
    MONTHLY = "MONTHLY"
    QUARTERLY = "QUARTERLY"
    SEMI_ANNUALLY = "SEMI_ANNUALLY"
    ANNUALLY = "ANNUALLY"


@dataclass
class BacktestConfig:
    """Simulation configuration parameters with foreign equity tax modeling."""
    start_date: str = "2001-07-10"
    end_date: str = "2026-10-12"
    initial_capital: float = 100_000_000.0   # 100,000,000 KRW ($100k equivalent)
    fee_rate: float = 0.0010                 # 0.10% brokerage commission
    slippage_rate: float = 0.0008            # 0.08% execution slippage (0.05%~0.10%)
    frequency: RebalanceFrequency = RebalanceFrequency.MONTHLY
    target_weights: Optional[Dict[str, float]] = None
    risk_free_rate: float = 0.02             # 2.0% annualized risk-free rate
    tax_enabled: bool = True                 # Foreign equity capital gains tax enabled
    tax_rate: float = 0.22                   # 22.0% effective tax rate (20% national + 2% local)
    annual_tax_deduction: float = 2_500_000.0 # 2.5 million KRW (or $2,000.0 USD)


@dataclass
class TaxAccountingState:
    """State tracking for annual capital gains tax accounting."""
    annual_realized_gain: float = 0.0
    annual_tax_paid: float = 0.0
    cumulative_tax_paid: float = 0.0
    annual_tax_records: List[Dict[str, Any]] = field(default_factory=list)


@dataclass
class PerformanceMetrics:
    """Standardized quantitative financial metrics suite with pre/after-tax attribution."""
    cumulative_return_pct: float
    cagr_pct: float
    mdd_pct: float
    sharpe_ratio: float
    calmar_ratio: float
    worst_year: str
    worst_year_pct: float
    fee_paid: float = 0.0
    slippage_paid: float = 0.0
    total_turnover: float = 0.0
    positive_years_pct: float = 0.0
    # Pre-tax and after-tax dual analytics
    cagr_pre_tax: float = 0.0
    cagr_after_tax: float = 0.0
    mdd_pre_tax: float = 0.0
    mdd_after_tax: float = 0.0
    calmar_pre_tax: float = 0.0
    calmar_after_tax: float = 0.0
    sharpe_pre_tax: float = 0.0
    sharpe_after_tax: float = 0.0
    total_tax_paid: float = 0.0
    tax_drag_pct: float = 0.0
    cumulative_return_pre_tax_pct: float = 0.0
    cumulative_return_after_tax_pct: float = 0.0

    @property
    def cagr(self) -> float:
        """Alias for cagr_pct."""
        return self.cagr_pct

    @property
    def mdd(self) -> float:
        """Alias for mdd_pct."""
        return self.mdd_pct

    @property
    def cumulative_return(self) -> float:
        """Alias for cumulative_return_pct."""
        return self.cumulative_return_pct

    @property
    def worst_year_return_pct(self) -> float:
        """Alias for worst_year_pct."""
        return self.worst_year_pct


@dataclass
class SimulationResult:
    """Simulation output containing curves, metrics, and execution history."""
    config: BacktestConfig
    metrics: PerformanceMetrics
    dates: List[str]
    daily_nav: List[float]                  # After-tax NAV if tax enabled, else pre-tax
    daily_drawdowns: List[float]            # After-tax drawdown
    annual_returns: Dict[int, float]
    daily_nav_pre_tax: List[float] = field(default_factory=list)
    daily_drawdowns_pre_tax: List[float] = field(default_factory=list)
    rebalance_records: List[Dict[str, Any]] = field(default_factory=list)
    holdings_history: List[Dict[str, float]] = field(default_factory=list)
    turnover_history: List[float] = field(default_factory=list)
    tax_history: List[Dict[str, Any]] = field(default_factory=list)
    tax_state: Optional[TaxAccountingState] = None

    @property
    def equity_curve(self) -> List[float]:
        """Alias for daily_nav."""
        return self.daily_nav

    @property
    def equity_curve_pre_tax(self) -> List[float]:
        """Alias for daily_nav_pre_tax."""
        return self.daily_nav_pre_tax

    @property
    def drawdown_curve(self) -> List[float]:
        """Alias for daily_drawdowns."""
        return self.daily_drawdowns

    @property
    def drawdown_curve_pre_tax(self) -> List[float]:
        """Alias for daily_drawdowns_pre_tax."""
        return self.daily_drawdowns_pre_tax

    @property
    def rebalance_history(self) -> List[Dict[str, Any]]:
        """Alias for rebalance_records."""
        return self.rebalance_records


def is_rebalance_date(
    current_date_str: str,
    next_date_str: Optional[str],
    freq: RebalanceFrequency
) -> bool:
    """
    Determines whether current_date_str is a rebalancing date boundary for freq.
    Returns True when transitioning into the next calendar period.
    """
    if next_date_str is None:
        return False

    d1 = datetime.date.fromisoformat(current_date_str)
    d2 = datetime.date.fromisoformat(next_date_str)

    if freq == RebalanceFrequency.WEEKLY:
        return d1.isocalendar()[:2] != d2.isocalendar()[:2]
    elif freq == RebalanceFrequency.MONTHLY:
        return (d1.year, d1.month) != (d2.year, d2.month)
    elif freq == RebalanceFrequency.QUARTERLY:
        q1 = (d1.month - 1) // 3
        q2 = (d2.month - 1) // 3
        return (d1.year, q1) != (d2.year, q2)
    elif freq == RebalanceFrequency.SEMI_ANNUALLY:
        h1 = (d1.month - 1) // 6
        h2 = (d2.month - 1) // 6
        return (d1.year, h1) != (d2.year, h2)
    elif freq == RebalanceFrequency.ANNUALLY:
        return d1.year != d2.year

    return False


def _compute_core_metrics(
    daily_nav: List[float],
    dates: List[str],
    risk_free_rate: float
) -> Tuple[float, float, float, float, float, Dict[int, float], str, float, float]:
    """Helper to calculate (cum_ret_pct, cagr_pct, mdd_pct, sharpe, calmar, annual_returns, worst_year, worst_year_pct, pos_pct)."""
    v0 = daily_nav[0]
    vt = daily_nav[-1]
    cum_ret_pct = ((vt - v0) / v0) * 100.0 if v0 > 0 else 0.0

    d0 = datetime.date.fromisoformat(dates[0])
    dt = datetime.date.fromisoformat(dates[-1])
    years = (dt - d0).days / 365.25

    if years > 0 and v0 > 0 and vt > 0:
        cagr = (vt / v0) ** (1.0 / years) - 1.0
        cagr_pct = cagr * 100.0
    else:
        cagr_pct = 0.0

    peak = daily_nav[0]
    min_dd = 0.0
    for v in daily_nav:
        if v > peak:
            peak = v
        dd = (v - peak) / peak if peak > 0 else 0.0
        if dd < min_dd:
            min_dd = dd
    mdd_pct = min_dd * 100.0

    # Sharpe ratio
    if len(daily_nav) >= 2:
        returns = [(daily_nav[i] / daily_nav[i - 1]) - 1.0 for i in range(1, len(daily_nav))]
        n = len(returns)
        mean_r = sum(returns) / n
        var_r = sum((r - mean_r) ** 2 for r in returns) / (n - 1) if n > 1 else 0.0
        std_r = math.sqrt(var_r) if var_r > 0 else 0.0
        sharpe = (mean_r * 252.0 - risk_free_rate) / (std_r * math.sqrt(252.0)) if std_r > 1e-12 else 0.0
    else:
        sharpe = 0.0

    # Calmar ratio
    abs_mdd = abs(min_dd)
    cagr_dec = cagr_pct / 100.0
    calmar = cagr_dec / abs_mdd if abs_mdd > 1e-6 else (99.99 if cagr_dec > 0 else 0.0)

    # Annual returns
    year_map: Dict[int, List[float]] = {}
    for d_str, v in zip(dates, daily_nav):
        y = int(d_str[:4])
        if y not in year_map:
            year_map[y] = []
        year_map[y].append(v)

    annual_returns: Dict[int, float] = {}
    for y, vals in year_map.items():
        y_ret = ((vals[-1] - vals[0]) / vals[0]) * 100.0 if vals[0] > 0 else 0.0
        annual_returns[y] = round(y_ret, 2)

    if annual_returns:
        worst_y = min(annual_returns.keys(), key=lambda y: annual_returns[y])
        worst_year_str = str(worst_y)
        worst_year_pct = annual_returns[worst_y]
        pos_years = sum(1 for ret in annual_returns.values() if ret > 0)
        pos_pct = (pos_years / len(annual_returns)) * 100.0
    else:
        worst_year_str = "N/A"
        worst_year_pct = 0.0
        pos_pct = 0.0

    return (
        round(cum_ret_pct, 2),
        round(cagr_pct, 2),
        round(mdd_pct, 2),
        round(sharpe, 2),
        round(calmar, 2),
        annual_returns,
        worst_year_str,
        round(worst_year_pct, 2),
        round(pos_pct, 1),
    )


def calculate_performance_metrics(
    daily_nav: List[float],
    dates: List[str],
    fee_paid: float = 0.0,
    slippage_paid: float = 0.0,
    total_turnover: float = 0.0,
    risk_free_rate: float = 0.02,
    daily_nav_pre_tax: Optional[List[float]] = None,
    total_tax_paid: float = 0.0
) -> PerformanceMetrics:
    """
    Computes institutional quantitative financial performance metrics with dual pre/after-tax attribution.
    """
    if not daily_nav or len(daily_nav) != len(dates):
        raise ValueError("daily_nav and dates must be non-empty and of equal length.")

    (
        cum_ret_pct, cagr_pct, mdd_pct, sharpe, calmar,
        annual_returns, worst_year_str, worst_year_pct, pos_pct
    ) = _compute_core_metrics(daily_nav, dates, risk_free_rate)

    if daily_nav_pre_tax and len(daily_nav_pre_tax) == len(dates):
        (
            pre_cum_ret, pre_cagr, pre_mdd, pre_sharpe, pre_calmar,
            _, _, _, _
        ) = _compute_core_metrics(daily_nav_pre_tax, dates, risk_free_rate)
        after_cagr = cagr_pct
        after_mdd = mdd_pct
        after_calmar = calmar
        after_sharpe = sharpe
        tax_drag = round(pre_cagr - after_cagr, 2)
        after_cum_ret = cum_ret_pct
    else:
        pre_cum_ret = cum_ret_pct
        pre_cagr = cagr_pct
        pre_mdd = mdd_pct
        pre_sharpe = sharpe
        pre_calmar = calmar
        after_cagr = cagr_pct
        after_mdd = mdd_pct
        after_calmar = calmar
        after_sharpe = sharpe
        tax_drag = 0.0
        after_cum_ret = cum_ret_pct

    return PerformanceMetrics(
        cumulative_return_pct=cum_ret_pct,
        cagr_pct=cagr_pct,
        mdd_pct=mdd_pct,
        sharpe_ratio=sharpe,
        calmar_ratio=calmar,
        worst_year=worst_year_str,
        worst_year_pct=worst_year_pct,
        fee_paid=round(fee_paid, 2),
        slippage_paid=round(slippage_paid, 2),
        total_turnover=round(total_turnover, 4),
        positive_years_pct=pos_pct,
        cagr_pre_tax=pre_cagr,
        cagr_after_tax=after_cagr,
        mdd_pre_tax=pre_mdd,
        mdd_after_tax=after_mdd,
        calmar_pre_tax=pre_calmar,
        calmar_after_tax=after_calmar,
        sharpe_pre_tax=pre_sharpe,
        sharpe_after_tax=after_sharpe,
        total_tax_paid=round(total_tax_paid, 2),
        tax_drag_pct=tax_drag,
        cumulative_return_pre_tax_pct=pre_cum_ret,
        cumulative_return_after_tax_pct=after_cum_ret,
    )


def _resolve_target_weights(
    weights_func: Union[Callable[..., Dict[str, float]], Dict[str, float]],
    idx: int,
    date_str: str,
    prices_map: Dict[str, float],
    nav: float
) -> Dict[str, float]:
    """Helper to safely invoke weights_func across multiple call signatures."""
    if isinstance(weights_func, dict):
        raw_weights = weights_func
    elif callable(weights_func):
        try:
            raw_weights = weights_func(idx, date_str, prices_map, nav)
        except TypeError:
            try:
                raw_weights = weights_func(idx, date_str)
            except TypeError:
                try:
                    raw_weights = weights_func(date_str)
                except TypeError:
                    raw_weights = weights_func()
    else:
        raise ValueError("weights_func must be a callable or Dict[str, float].")

    total_w = sum(raw_weights.values())
    if total_w > 0:
        return {k: v / total_w for k, v in raw_weights.items()}
    return {k: 0.0 for k in raw_weights}


def simulate_portfolio(
    prices: Dict[str, List[float]],
    dates: List[str],
    weights_func: Union[Callable[..., Dict[str, float]], Dict[str, float]],
    config: Optional[BacktestConfig] = None
) -> SimulationResult:
    """
    Simulates multi-asset portfolio with continuous daily share drift,
    dynamic 2-way rebalance turnover friction, foreign equity capital gains tax,
    and exact pre/after-tax metric tracking.
    
    100% stock full-investment constraint: w_cash = 0.0.
    """
    if config is None:
        config = BacktestConfig()

    if not dates or not prices:
        raise ValueError("prices and dates must not be empty.")

    num_days = len(dates)
    for asset, p_list in prices.items():
        if len(p_list) != num_days:
            raise ValueError(f"Price series for {asset} length ({len(p_list)}) mismatch dates ({num_days}).")

    if config.initial_capital <= 0:
        raise ValueError("initial_capital must be greater than zero.")

    # Determine default annual tax deduction scale
    annual_deduction = config.annual_tax_deduction
    if annual_deduction == 2_500_000.0 and config.initial_capital <= 1_000_000.0:
        annual_deduction = 2_000.0

    # Tracking states
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

    # Share counts and average cost bases
    # Pre-tax portfolio shares:
    shares_pre: Dict[str, float] = {}
    # After-tax portfolio shares and cost bases:
    shares_after: Dict[str, float] = {}
    cost_basis: Dict[str, float] = {}

    p0_map = {k: prices[k][0] for k in prices}
    init_weights = _resolve_target_weights(
        weights_func, 0, dates[0], p0_map, config.initial_capital
    )

    init_alloc_sum = sum(init_weights.get(k, 0.0) for k in prices)
    gross_init_vol = config.initial_capital * init_alloc_sum
    init_fee = gross_init_vol * config.fee_rate
    init_slippage = gross_init_vol * config.slippage_rate
    init_friction = init_fee + init_slippage

    total_fee_paid += init_fee
    total_slippage_paid += init_slippage
    total_cumulative_turnover += init_alloc_sum

    invested_capital = config.initial_capital - init_friction

    for k in prices:
        w_k = init_weights.get(k, 0.0)
        p_k = p0_map[k]
        sh = (invested_capital * w_k) / p_k if p_k > 0 else 0.0
        shares_pre[k] = sh
        shares_after[k] = sh
        cost_basis[k] = p_k

    nav_pre_0 = sum(shares_pre[k] * p0_map[k] for k in prices)
    nav_after_0 = sum(shares_after[k] * p0_map[k] for k in prices)
    peak_pre = nav_pre_0
    peak_after = nav_after_0

    daily_nav_pre_tax.append(nav_pre_0)
    daily_drawdowns_pre_tax.append(0.0)
    daily_nav_after_tax.append(nav_after_0)
    daily_drawdowns_after_tax.append(0.0)
    holdings_history.append(dict(shares_after))
    turnover_history.append(init_alloc_sum)

    rebalance_records.append({
        "date": dates[0],
        "type": "INITIAL_DEPLOYMENT",
        "pre_nav": config.initial_capital,
        "post_nav": nav_after_0,
        "turnover": init_alloc_sum,
        "fee": init_fee,
        "slippage": init_slippage,
        "target_weights": dict(init_weights),
    })

    # Continuous simulation
    for t in range(1, num_days):
        cur_date = dates[t]
        next_date = dates[t + 1] if t + 1 < num_days else None
        p_t_map = {k: prices[k][t] for k in prices}

        # Valuations before today's trades
        val_pre = sum(shares_pre[k] * p_t_map[k] for k in prices)
        val_after = sum(shares_after[k] * p_t_map[k] for k in prices)

        # Drifted weights
        drift_w: Dict[str, float] = {}
        if val_after > 0:
            for k in prices:
                drift_w[k] = (shares_after[k] * p_t_map[k]) / val_after
        else:
            drift_w = {k: 0.0 for k in prices}

        should_rebalance = is_rebalance_date(cur_date, next_date, config.frequency)

        if should_rebalance and val_after > 0:
            target_w = _resolve_target_weights(weights_func, t, cur_date, p_t_map, val_after)

            sum_delta_w = sum(
                abs(target_w.get(k, 0.0) - drift_w.get(k, 0.0))
                for k in prices
            )
            two_way_turnover = sum_delta_w / 2.0

            if sum_delta_w > 1e-6:
                # Deduct transaction friction
                reb_pre_vol = val_pre * sum_delta_w
                reb_after_vol = val_after * sum_delta_w
                
                fric_pre = reb_pre_vol * (config.fee_rate + config.slippage_rate)
                fric_after = reb_after_vol * (config.fee_rate + config.slippage_rate)
                
                reb_fee = reb_after_vol * config.fee_rate
                reb_slip = reb_after_vol * config.slippage_rate

                total_fee_paid += reb_fee
                total_slippage_paid += reb_slip
                total_cumulative_turnover += two_way_turnover

                post_val_pre = val_pre - fric_pre
                post_val_after = val_after - fric_after

                # Execute trades & update cost basis / realized gains
                for k in prices:
                    p_k = p_t_map[k]
                    # Pre-tax portfolio
                    shares_pre[k] = (post_val_pre * target_w.get(k, 0.0)) / p_k if p_k > 0 else 0.0
                    
                    # After-tax portfolio
                    new_sh = (post_val_after * target_w.get(k, 0.0)) / p_k if p_k > 0 else 0.0
                    old_sh = shares_after[k]
                    cb_k = cost_basis.get(k, p_k)

                    if new_sh < old_sh:
                        # Selling shares: realize gain/loss
                        sh_sold = old_sh - new_sh
                        gain = sh_sold * (p_k - cb_k)
                        tax_state.annual_realized_gain += gain
                    elif new_sh > old_sh:
                        # Buying shares: update weighted average cost basis
                        sh_bought = new_sh - old_sh
                        if new_sh > 0:
                            cost_basis[k] = (old_sh * cb_k + sh_bought * p_k) / new_sh
                        else:
                            cost_basis[k] = p_k

                    shares_after[k] = new_sh

                val_pre = sum(shares_pre[k] * p_t_map[k] for k in prices)
                val_after = sum(shares_after[k] * p_t_map[k] for k in prices)
                turnover_history.append(two_way_turnover)

                rebalance_records.append({
                    "date": cur_date,
                    "type": "REBALANCE",
                    "pre_nav": val_after + fric_after,
                    "post_nav": val_after,
                    "turnover": two_way_turnover,
                    "fee": reb_fee,
                    "slippage": reb_slip,
                    "target_weights": dict(target_w),
                    "drift_weights": dict(drift_w),
                })
            else:
                turnover_history.append(0.0)
        else:
            turnover_history.append(0.0)

        # Calendar year-end tax settlement
        is_year_end = (next_date is not None and cur_date[:4] != next_date[:4]) or (next_date is None)
        if config.tax_enabled and is_year_end:
            year_val = int(cur_date[:4])
            net_gain = tax_state.annual_realized_gain
            taxable_gain = max(0.0, net_gain - annual_deduction)
            annual_tax = taxable_gain * config.tax_rate

            if annual_tax > 0.0 and val_after > annual_tax:
                # Deduct tax from after-tax portfolio
                tax_state.annual_tax_paid = annual_tax
                tax_state.cumulative_tax_paid += annual_tax

                retention_ratio = 1.0 - (annual_tax / val_after)
                for k in prices:
                    shares_after[k] *= retention_ratio
                val_after = sum(shares_after[k] * p_t_map[k] for k in prices)

                tax_rec = {
                    "year": year_val,
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

        # Record daily valuations
        daily_nav_pre_tax.append(val_pre)
        if val_pre > peak_pre:
            peak_pre = val_pre
        dd_pre = (val_pre - peak_pre) / peak_pre if peak_pre > 0 else 0.0
        daily_drawdowns_pre_tax.append(round(dd_pre, 4))

        daily_nav_after_tax.append(val_after)
        if val_after > peak_after:
            peak_after = val_after
        dd_after = (val_after - peak_after) / peak_after if peak_after > 0 else 0.0
        daily_drawdowns_after_tax.append(round(dd_after, 4))

        holdings_history.append(dict(shares_after))

    # Determine primary daily NAV (after-tax if tax enabled, else pre-tax)
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

    # Annual returns
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


def run_buy_and_hold(
    prices: List[float],
    dates: List[str],
    asset_name: str = "ASSET",
    config: Optional[BacktestConfig] = None
) -> SimulationResult:
    """Convenience runner for Buy & Hold benchmark on a single price timeseries."""
    if config is None:
        config = BacktestConfig(frequency=RebalanceFrequency.ANNUALLY)
    price_dict = {asset_name: prices}
    return simulate_portfolio(
        prices=price_dict,
        dates=dates,
        weights_func={asset_name: 1.0},
        config=config
    )
