"""
backend/tests/test_telegram.py - Unit & Integration Tests for Telegram Bot & Quant Alert Hub
"""
import pytest

from backend.app.services.quant_engine import quant_engine
from backend.app.services.semi_engine import semi_engine
from backend.app.services.telegram_service import telegram_service


@pytest.fixture(autouse=True)
def isolate_telegram_config(tmp_path):
    """Isolates telegram_service persistence to a temporary file during each test."""
    orig_path = telegram_service.config_path
    orig_state = dict(telegram_service._state)
    telegram_service.config_path = tmp_path / "telegram_config_test.json"
    telegram_service._state = telegram_service._default_state()
    yield
    telegram_service.config_path = orig_path
    telegram_service._state = orig_state


def test_telegram_status_default(client):
    """GET /api/telegram/status returns unconfigured status by default."""
    res = client.get("/api/telegram/status")
    assert res.status_code == 200
    data = res.json()
    assert data["configured"] is False
    assert data["bot_token_masked"] == ""
    assert data["chat_id"] == ""
    assert data["channel_url"] == "https://t.me/RightSideAlphaBot"
    assert data["auto_alert_ignition"] is True
    assert data["auto_alert_stop_loss"] is True
    assert data["auto_alert_semi_extreme"] is True


def test_telegram_config_update_and_masked_token_preservation(client):
    """POST /api/telegram/config saves token/chat_id and preserves token when masked string is resubmitted."""
    res = client.post(
        "/api/telegram/config",
        json={
            "bot_token": "123456789:ABCDEF_secret_token_9876",
            "chat_id": "-10099887766",
            "channel_url": "https://t.me/RightSideAlphaBot",
            "auto_alert_ignition": True,
            "auto_alert_stop_loss": False,
            "auto_alert_semi_extreme": True,
        },
    )
    assert res.status_code == 200
    data = res.json()
    assert data["configured"] is True
    assert data["bot_token_masked"] == "123456...9876"
    assert data["chat_id"] == "-10099887766"
    assert data["auto_alert_stop_loss"] is False

    # Re-saving with the masked token should NOT overwrite the underlying real token
    res2 = client.post(
        "/api/telegram/config",
        json={
            "bot_token": data["bot_token_masked"],
            "chat_id": "-10099887766",
            "auto_alert_ignition": True,
            "auto_alert_stop_loss": True,
            "auto_alert_semi_extreme": True,
        },
    )
    assert res2.status_code == 200
    assert telegram_service._resolve_token() == "123456789:ABCDEF_secret_token_9876"


def test_telegram_test_message_matches_engines(client):
    """POST /api/telegram/test returns simulated preview with accurate Ignition & Semi F&G numbers."""
    res = client.post("/api/telegram/test", json={"lang": "kr"})
    assert res.status_code == 200
    data = res.json()
    assert data["ok"] is True
    assert data["simulated"] is True
    assert data["delivered"] is False
    assert data["briefing_type"] == "test"

    preview = data["message_preview"]
    celh = quant_engine.get_stock("CELH", is_pro=True)
    tsla = quant_engine.get_stock("TSLA", is_pro=True)
    semi_ov = semi_engine.get_overview()

    assert f"${celh.close:.2f}" in preview
    assert f"${tsla.close:.2f}" in preview
    assert f"{semi_ov.fg_score:.1f}" in preview
    assert "EXTREME FEAR" in preview


def test_telegram_ignition_briefing_exact_prices(client):
    """POST /api/telegram/send-briefing (ignition) verifies all 5 Ignition stocks match quant_engine 100%."""
    res = client.post("/api/telegram/send-briefing", json={"briefing_type": "ignition", "lang": "kr"})
    assert res.status_code == 200
    data = res.json()
    assert data["ok"] is True
    assert data["briefing_type"] == "ignition"

    preview = data["message_preview"]
    ignition_stocks = quant_engine.get_stocks(is_pro=True, zone="IGNITION_ZONE")
    assert len(ignition_stocks) == 5

    for s in ignition_stocks:
        assert f"${s.ticker}" in preview
        assert f"${s.close:.2f}" in preview
        assert f"${s.entry_trigger_price:.2f}" in preview
        assert f"${s.stop_loss_price:.2f}" in preview
        assert f"${s.tp1_2x_price:.2f}" in preview


def test_telegram_semi_briefing_exact_metrics(client):
    """POST /api/telegram/send-briefing (semi) verifies Semi F&G score and ETF prices match semi_engine."""
    res = client.post("/api/telegram/send-briefing", json={"briefing_type": "semi", "lang": "kr"})
    assert res.status_code == 200
    data = res.json()
    assert data["ok"] is True
    assert data["briefing_type"] == "semi"

    preview = data["message_preview"]
    ov = semi_engine.get_overview()
    assert f"{ov.fg_score:.1f}" in preview
    assert f"${ov.smh_close:.2f}" in preview
    assert f"${ov.xlv_close:.2f}" in preview
    assert f"${ov.qqq_close:.2f}" in preview
    assert f"{ov.recommended_smh_weight}% $SMH : {ov.recommended_xlv_weight}% $XLV" in preview


def test_telegram_doctor_briefing_exact_diagnosis(client):
    """POST /api/telegram/send-briefing (doctor) matches quant_engine.diagnose_position."""
    res = client.post(
        "/api/telegram/send-briefing",
        json={
            "briefing_type": "doctor",
            "ticker": "CELH",
            "entry_price": 27.20,
            "days_held": 42,
            "lang": "kr",
        },
    )
    assert res.status_code == 200
    data = res.json()
    assert data["ok"] is True
    assert data["briefing_type"] == "doctor"

    diag = quant_engine.diagnose_position("CELH", 27.20, 42)
    preview = data["message_preview"]
    assert "$CELH" in preview
    assert f"${diag.current_price:.2f}" in preview
    assert f"${diag.entry_price:.2f}" in preview
    assert f"${diag.stop_price:.2f}" in preview
    assert f"${diag.tp1_price:.2f}" in preview
    assert diag.status_code in preview


def test_telegram_full_briefing_combines_all_sections(client):
    """POST /api/telegram/send-briefing (full) includes Ignition, Semi F&G, and Research Top Picks."""
    res = client.post("/api/telegram/send-briefing", json={"briefing_type": "full", "lang": "kr"})
    assert res.status_code == 200
    data = res.json()
    assert data["ok"] is True
    assert data["briefing_type"] == "full"

    preview = data["message_preview"]
    assert "$CELH" in preview
    assert "$MBLY" in preview
    assert "$SMH" in preview
    assert "18.0" in preview


def test_telegram_webhook_commands(client):
    """POST /api/telegram/webhook handles /start, /ignition, /semi, /doctor, and /stock commands."""
    # 1. /start
    r_start = client.post("/api/telegram/webhook", json={"message": {"text": "/start", "chat": {"id": 111}}})
    assert r_start.status_code == 200
    assert r_start.json()["ok"] is True
    assert "/ignition" in r_start.json()["reply"]

    # 2. /ignition
    r_ign = client.post("/api/telegram/webhook", json={"message": {"text": "/ignition", "chat": {"id": 111}}})
    assert r_ign.status_code == 200
    assert "$CELH" in r_ign.json()["reply"]
    assert "$TSLA" in r_ign.json()["reply"]

    # 3. /semi
    r_semi = client.post("/api/telegram/webhook", json={"message": {"text": "/semi", "chat": {"id": 111}}})
    assert r_semi.status_code == 200
    assert "18.0" in r_semi.json()["reply"]
    assert "80% $SMH : 20% $XLV" in r_semi.json()["reply"]

    # 4. /doctor CELH 27.20 42
    r_doc = client.post(
        "/api/telegram/webhook",
        json={"message": {"text": "/doctor CELH 27.20 42", "chat": {"id": 111}}},
    )
    assert r_doc.status_code == 200
    assert "$CELH" in r_doc.json()["reply"]
    assert "$27.93" in r_doc.json()["reply"]
    assert "$24.75" in r_doc.json()["reply"]

    # 5. /stock TSLA
    tsla = quant_engine.get_stock("TSLA", is_pro=True)
    r_stock = client.post(
        "/api/telegram/webhook",
        json={"message": {"text": "/stock TSLA", "chat": {"id": 111}}},
    )
    assert r_stock.status_code == 200
    reply_stock = r_stock.json()["reply"]
    assert "$TSLA" in reply_stock
    assert f"${tsla.close:.2f}" in reply_stock
    assert f"${tsla.entry_trigger_price:.2f}" in reply_stock
    assert f"${tsla.stop_loss_price:.2f}" in reply_stock
    assert f"${tsla.tp1_2x_price:.2f}" in reply_stock
