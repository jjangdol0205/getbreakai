"""
backend/app/api/pro.py - Gated Pro Subscriber Vault and Advanced Tools API
"""
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status

from backend.app.api.deps import require_pro, get_is_pro
from backend.app.models.auth import (
    ProVaultResponse,
    PineScriptResponse,
    ProPositionDoctorRequest,
    ProPositionDoctorResponse,
)
from backend.app.models.stock import StockResponse
from backend.app.services.quant_engine import quant_engine

router = APIRouter()

# Authoritative TradingView Pine Script v5 Code (from prototype specification lines 357-370)
PINE_SCRIPT_V5_CODE = (
    "//@version=5\n"
    "indicator(\"RightSideAlpha PW-RSI Ignition v2.6\", overlay=true)\n"
    "ma20 = ta.sma(close, 20)\n"
    "ma60 = ta.sma(close, 60)\n"
    "low52 = ta.lowest(low, 252)\n"
    "high52 = ta.highest(high, 252)\n"
    "volRatio = volume / ta.sma(volume, 20)\n"
    "washout10d = ta.highest(volRatio, 10) >= 1.40\n"
    "proxLow = (close - low52) / low52 * 100\n"
    "ddHigh = (close - high52) / high52 * 100\n"
    "ignition = ddHigh <= -35 and proxLow >= 10 and proxLow <= 40 and close > ma20 and close > ma60 and washout10d\n"
    "plot(ma20, \"MA20\", color=color.new(color.aqua, 0), linewidth=2)\n"
    "plot(ma60, \"MA60 Trigger\", color=color.new(color.orange, 0), linewidth=2)\n"
    "plotshape(ignition and not ignition[1], \"PW-RSI IGNITION\", shape.labelup, location.belowbar, color.green, text=\"🟢 IGNITION\", textcolor=color.white)\n"
)


@router.get("/vault", response_model=ProVaultResponse)
def get_pro_vault(_: bool = Depends(require_pro)):
    """
    Access gated Pro Subscriber Vault. Requires valid Pro subscription or demo key.
    """
    return ProVaultResponse(
        unlocked=True,
        tier="pro",
        pine_script_available=True,
        tools=["position_doctor", "morning_pdf", "pine_script_v5"],
    )


@router.get("/pine-script", response_model=PineScriptResponse)
@router.get("/pinescript", response_model=PineScriptResponse, include_in_schema=False)
def get_pine_script(_: bool = Depends(require_pro)):
    """
    Deliver proprietary TradingView Pine Script v5 indicator code to verified subscribers.
    """
    return PineScriptResponse(
        version="v5",
        name="RightSideAlpha PW-RSI",
        code=PINE_SCRIPT_V5_CODE,
    )


@router.get("/stocks-unmasked", response_model=List[StockResponse])
def get_unmasked_stocks(_: bool = Depends(require_pro)):
    """
    Returns full universe of screened equities with unblurred target prices
    (stop_loss_price, tp1_2x_price, ma60_price).
    """
    return quant_engine.get_stocks(is_pro=True)


@router.post("/position-doctor", response_model=ProPositionDoctorResponse)
def evaluate_position_doctor(payload: ProPositionDoctorRequest):
    """
    Position Doctor diagnostic engine running the 4 asymmetric exit rules:
    - Rule 1: Return <= -9% -> Hard Stop Loss immediate exit.
    - Rule 2: Days held >= 55 & Return < +8% -> Stagnant dead-money exit.
    - Rule 3: Return >= +100% -> Sell 50% to recover initial capital risk-free.
    - Rule 4: Normal holding status within profit/stop bounds.
    """
    t_clean = payload.ticker.strip().upper()

    cur_price = payload.current_price
    if cur_price is None:
        stock = quant_engine.stocks_by_ticker.get(t_clean)
        cur_price = stock.close if stock else payload.entry_price
    else:
        cur_price = float(cur_price)

    return_pct = round(((cur_price - payload.entry_price) / payload.entry_price) * 100.0, 2)
    stop_price = round(payload.entry_price * 0.91, 2)
    tp1_price = round(payload.entry_price * 2.0, 2)

    if return_pct <= -9.0:
        return ProPositionDoctorResponse(
            ticker=t_clean,
            status_code="HARD_STOP",
            status_label="손절(-9% 칼손절 방어)",
            return_pct=return_pct,
            rule_triggered="Rule 1 (-9% Hard Stop Loss)",
            action_plan=f"Triggered: Exit immediately at ${cur_price} to protect capital and harvest tax loss credit.",
            is_critical=True,
            stop_price=stop_price,
            tp1_price=tp1_price,
        )
    elif payload.days_held >= 55 and return_pct < 8.0:
        return ProPositionDoctorResponse(
            ticker=t_clean,
            status_code="TIME_STOP",
            status_label="55일 시간손절(데드머니 탈출)",
            return_pct=return_pct,
            rule_triggered="Rule 2 (55-Day Time-Stop)",
            action_plan=f"Stagnant performance (+{return_pct}% in {payload.days_held} days). Rotate into fresh Ignition setup.",
            is_critical=False,
            stop_price=stop_price,
            tp1_price=tp1_price,
        )
    elif return_pct >= 100.0:
        return ProPositionDoctorResponse(
            ticker=t_clean,
            status_code="TP1_HARVEST",
            status_label="2배+(TP1) 달성 후 트레일링 익절",
            return_pct=return_pct,
            rule_triggered="Rule 3 (+100% TP1 Principal Recovery)",
            action_plan=f"Sell 50% at ${cur_price} to recover 100% principal. Ride remaining 50% risk-free.",
            is_critical=False,
            stop_price=stop_price,
            tp1_price=tp1_price,
        )
    else:
        days_left = max(0, 55 - payload.days_held)
        return ProPositionDoctorResponse(
            ticker=t_clean,
            status_code="HOLD",
            status_label="정상 보유 (밴드 내 유지)",
            return_pct=return_pct,
            rule_triggered="Rule 4 (Ongoing Hold)",
            action_plan=f"Hold position. Stop: ${stop_price}, TP1: ${tp1_price}. {days_left} trading days until 55-day review.",
            is_critical=False,
            stop_price=stop_price,
            tp1_price=tp1_price,
        )
