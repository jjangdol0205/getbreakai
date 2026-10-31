"""
backend/app/api/telegram.py - FastAPI Router for Telegram Bot Configuration, Briefings & Webhook
"""
from typing import Any, Dict, Optional
from fastapi import APIRouter, Body

from backend.app.models.telegram import (
    TelegramConfigRequest,
    TelegramDetectChatRequest,
    TelegramDetectChatResponse,
    TelegramSendRequest,
    TelegramSendResponse,
    TelegramStatusResponse,
)
from backend.app.services.telegram_service import telegram_service

router = APIRouter()


@router.get("/status", response_model=TelegramStatusResponse)
def get_telegram_status() -> TelegramStatusResponse:
    """Returns current Telegram Bot configuration status and alert preferences."""
    return telegram_service.get_status()


@router.post("/config", response_model=TelegramStatusResponse)
def update_telegram_config(payload: TelegramConfigRequest) -> TelegramStatusResponse:
    """Updates Telegram Bot token, chat_id, channel_url, and auto-alert toggles."""
    return telegram_service.update_config(payload)


@router.post("/detect-chat-id", response_model=TelegramDetectChatResponse)
def detect_telegram_chat_id(
    payload: Optional[TelegramDetectChatRequest] = Body(default=None),
) -> TelegramDetectChatResponse:
    """Auto-detects the latest chat_id from Telegram getUpdates API."""
    token = payload.bot_token if payload else None
    return telegram_service.detect_chat_id(bot_token=token)


@router.post("/test", response_model=TelegramSendResponse)
def send_telegram_test(
    payload: Optional[TelegramSendRequest] = Body(default=None),
) -> TelegramSendResponse:
    """Sends or previews a connection verification + Ignition/Semi summary message."""
    req = payload or TelegramSendRequest(briefing_type="test")
    req.briefing_type = "test"
    return telegram_service.dispatch_briefing(req)


@router.post("/send-briefing", response_model=TelegramSendResponse)
def send_telegram_briefing(
    payload: Optional[TelegramSendRequest] = Body(default=None),
) -> TelegramSendResponse:
    """Dispatches a formatted Quant/Semiconductor/Position Doctor briefing to Telegram."""
    req = payload or TelegramSendRequest(briefing_type="full")
    return telegram_service.dispatch_briefing(req)


@router.post("/webhook")
def telegram_webhook(update: Dict[str, Any] = Body(default_factory=dict)) -> Dict[str, Any]:
    """Processes incoming Telegram Bot webhook updates (/start, /ignition, /semi, /doctor, /stock)."""
    reply_text = telegram_service.handle_webhook_update(update)
    return {"ok": True, "reply": reply_text}
