"""
backend/app/models/telegram.py - Pydantic schemas for Telegram Bot & Alert Hub
"""
from typing import Optional
from pydantic import BaseModel, Field


class TelegramConfigRequest(BaseModel):
    bot_token: Optional[str] = None
    chat_id: Optional[str] = None
    channel_url: Optional[str] = "https://t.me/RightSideAlphaBot"
    auto_alert_ignition: bool = True
    auto_alert_stop_loss: bool = True
    auto_alert_semi_extreme: bool = True


class TelegramStatusResponse(BaseModel):
    configured: bool
    bot_token_masked: str
    bot_username: Optional[str] = None
    chat_id: str
    channel_url: str
    auto_alert_ignition: bool
    auto_alert_stop_loss: bool
    auto_alert_semi_extreme: bool
    last_sent_at: Optional[str] = None
    messages_sent_count: int = 0


class TelegramSendRequest(BaseModel):
    briefing_type: str = Field(default="full", description="test | ignition | semi | doctor | full")
    custom_message: Optional[str] = None
    ticker: Optional[str] = None
    entry_price: Optional[float] = None
    days_held: Optional[int] = None
    bot_token: Optional[str] = None
    chat_id: Optional[str] = None
    lang: str = "kr"


class TelegramSendResponse(BaseModel):
    ok: bool
    delivered: bool
    simulated: bool
    briefing_type: str
    chat_id: str
    message_preview: str
    timestamp: str
    detail: str


class TelegramDetectChatRequest(BaseModel):
    bot_token: Optional[str] = None


class TelegramDetectChatResponse(BaseModel):
    ok: bool
    chat_id: Optional[str] = None
    chat_title: Optional[str] = None
    username: Optional[str] = None
    detail: str
