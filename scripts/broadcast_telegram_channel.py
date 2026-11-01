#!/usr/bin/env python3
"""
scripts/broadcast_telegram_channel.py - 100% English Telegram Channel & Bot Setup + Daily Quant Broadcast
"""
import argparse
import json
import os
from pathlib import Path
import httpx

BASE_DIR = Path(__file__).resolve().parent.parent
TG_CONFIG_PATH = BASE_DIR / "data" / "telegram_config.json"
SEMI_JSON_PATH = BASE_DIR / "frontend" / "public" / "static_api" / "semi_overview.json"
STOCKS_PRO_PATH = BASE_DIR / "frontend" / "public" / "static_api" / "stocks_pro.json"


def load_tg_credentials():
    token = os.getenv("TELEGRAM_BOT_TOKEN", "").strip()
    chat_id = os.getenv("TELEGRAM_CHAT_ID", "").strip() or "@truthofmarketss"
    if TG_CONFIG_PATH.exists():
        try:
            cfg = json.loads(TG_CONFIG_PATH.read_text(encoding="utf-8"))
            if not token:
                token = str(cfg.get("bot_token") or "").strip()
            if not os.getenv("TELEGRAM_CHAT_ID") and cfg.get("chat_id"):
                chat_id = str(cfg.get("chat_id")).strip()
        except Exception:
            pass
    return token, chat_id


def setup_bot_and_channel_english(client: httpx.Client, base_url: str, chat_id: str) -> None:
    # 1. Bot Name, Short Description, Description, and Commands (100% US English)
    r_name = client.post(
        f"{base_url}/setMyName",
        json={"name": "TruthOfMarket | US Quant & Semi Bot"},
    ).json()
    print("setMyName:", r_name)

    r_short = client.post(
        f"{base_url}/setMyShortDescription",
        json={
            "short_description": (
                "Official US Stock (RightSideAlpha) & Semiconductor ($SMH/$XLV) Fear & Greed Quant Bot — https://truthofmarket.com"
            )
        },
    ).json()
    print("setMyShortDescription:", r_short)

    r_desc = client.post(
        f"{base_url}/setMyDescription",
        json={
            "description": (
                "Official Quantitative Dispatch Bot for TruthOfMarket (https://truthofmarket.com)\n\n"
                "📢 Official Broadcast Channel: https://t.me/truthofmarketss\n"
                "📈 72 US Equities Right-Side PW-RSI Breakout Screener\n"
                "🧭 Semiconductor 7-Factor Fear & Greed Index ($SMH / $XLV / $QQQ)\n"
                "👑 Pro VIP Command Center: Daily Top 5 Order Book & Position Sizing Calculator"
            )
        },
    ).json()
    print("setMyDescription:", r_desc)

    r_cmds = client.post(
        f"{base_url}/setMyCommands",
        json={
            "commands": [
                {"command": "start", "description": "Launch TruthOfMarket US Quant Bot & menu"},
                {"command": "semi", "description": "Semiconductor 7-Factor Fear & Greed + $SMH:$XLV Barbell"},
                {"command": "ignition", "description": "Top US Right-Side PW-RSI Breakout Signals"},
                {"command": "stock", "description": "Instant US Stock Quant Card (e.g. /stock NVDA)"},
                {"command": "doctor", "description": "Position Doctor 4-Rule Audit (e.g. /doctor CELH 27.20 42)"},
                {"command": "full", "description": "Full Daily US Market & Semiconductor Quant Briefing"},
            ]
        },
    ).json()
    print("setMyCommands:", r_cmds)

    # 2. Channel Title & Description (if bot has can_change_info permission)
    r_ctitle = client.post(
        f"{base_url}/setChatTitle",
        json={
            "chat_id": chat_id,
            "title": "TruthOfMarket | US Stock & Semi Quant",
        },
    ).json()
    print("setChatTitle:", r_ctitle)

    r_cdesc = client.post(
        f"{base_url}/setChatDescription",
        json={
            "chat_id": chat_id,
            "description": (
                "Daily US Market Close Quantitative Briefings • 72-Equity Right-Side PW-RSI Ignition Signals • "
                "Semiconductor ($SMH/$XLV) 7-Factor Fear & Greed Index.\n"
                "🖥️ Live Terminal & Pro VIP Order Book: https://truthofmarket.com"
            ),
        },
    ).json()
    print("setChatDescription:", r_cdesc)


def build_english_daily_briefing() -> str:
    semi = json.loads(SEMI_JSON_PATH.read_text(encoding="utf-8"))
    stocks_payload = json.loads(STOCKS_PRO_PATH.read_text(encoding="utf-8"))
    stocks = stocks_payload if isinstance(stocks_payload, list) else stocks_payload.get("stocks", [])
    ignition = [s for s in stocks if s.get("zone_code") == "IGNITION_ZONE"]
    if not ignition:
        ignition = stocks[:4]

    as_of = semi.get("date") or "2026-10-30"
    fg_score = float(semi.get("fg_score", 64.6))
    regime_en = str(semi.get("regime_en", "Greed")).upper()
    smh_w = int(semi.get("recommended_smh_weight", 50))
    xlv_w = int(semi.get("recommended_xlv_weight", 50))
    smh_close = float(semi.get("smh_close", 522.49))
    smh_dd = float(semi.get("smh_dd_pct", -5.24))
    smh_rsi = float(semi.get("smh_rsi", 61.9))
    xlv_close = float(semi.get("xlv_close", 184.87))
    qqq_close = float(semi.get("qqq_close", 690.49))

    # Showcase #1 (CELH if present in ignition, else first ignition pick)
    showcase = next((s for s in ignition if s.get("ticker") == "CELH"), ignition[0])
    vip_locked = [s for s in ignition if s.get("ticker") != showcase.get("ticker")][:3]

    lines = [
        f"🏛️ <b>[TRUTHOFMARKET] DAILY US QUANT &amp; SEMICONDUCTOR BRIEFING ({as_of})</b>",
        "━━━━━━━━━━━━━━━━━━━━",
        "🧭 <b>1. Semiconductor 7-Factor Fear &amp; Greed Index</b>",
        f"• <b>Composite Score</b>: <b>{fg_score:.1f} / 100 ({regime_en})</b>",
        f"• <b>Barbell Allocation Directive</b>: <b>{smh_w}% $SMH : {xlv_w}% $XLV</b>",
        f"• <b>$SMH (Semiconductor)</b>: <b>${smh_close:.2f}</b> ({smh_dd:.2f}% 52W DD | RSI {smh_rsi:.1f})",
        f"• <b>$XLV (Healthcare Vault)</b>: <b>${xlv_close:.2f}</b> | <b>$QQQ</b>: <b>${qqq_close:.2f}</b>",
        "",
        f"🚀 <b>2. RightSideAlpha US 72-Equity Ignition Screener ({len(ignition)} Active Signals)</b>",
        "<i>4-Condition Turnaround Filter: 52W DD ≤ -20% + Off Low + MA20/60 Reclaim + 10D Vol Surge</i>",
        "",
        f"✅ <b>[FREE SAMPLE PICK #1] ${showcase['ticker']} ({showcase.get('name_en', showcase['ticker'])})</b>",
        f"• <b>Latest Close</b>: <b>${float(showcase['close']):.2f}</b> | <b>PW-RSI Score</b>: <b>{int(showcase['score'])} / 100</b>",
        f"• <b>52W Drawdown</b>: {float(showcase['dd_high52_pct']):.1f}% | <b>10D Vol Surge</b>: {float(showcase['vol_surge_10d']):.2f}x",
        f"• 🎯 <b>Entry Trigger (TRG)</b>: <code>${float(showcase['entry_trigger_price']):.2f}</code>",
        f"• 🛑 <b>Hard Stop (-7% STP)</b>: <code>${float(showcase['stop_loss_price']):.2f}</code>",
        f"• 💰 <b>Target 1 (+5% TP1)</b>: <code>${float(showcase['tp1_2x_price']):.2f}</code>",
        "",
    ]

    for idx, s in enumerate(vip_locked, start=2):
        lines.extend([
            f"🔒 <b>[PRO VIP IGNITION PICK #{idx}] — TICKER LOCKED</b>",
            f"• <b>Sector</b>: {s.get('sector', 'US Equity')} | <b>PW-RSI Score</b>: <b>{int(s['score'])} / 100</b>",
            f"• <b>52W Drawdown</b>: {float(s['dd_high52_pct']):.1f}% | <b>Off 52W Low</b>: +{float(s['prox_low52_pct']):.1f}% | <b>Vol</b>: {float(s['vol_surge_10d']):.2f}x",
            "• 🎯 <b>Entry / Stop (-7%) / TP1 (+5%)</b>: <code>🔒 Unlock Pro VIP at truthofmarket.com</code>",
            "",
        ])

    lines.extend([
        "━━━━━━━━━━━━━━━━━━━━",
        "👑 <b>What Pro VIP Subscribers Unlock on TruthOfMarket.com:</b>",
        "1️⃣ <b>Daily Top 5 Ignition Order Book</b> (Unmasked Tickers + Exact Entry/Stop/TP1)",
        "2️⃣ <b>Account Position Sizing &amp; Share Calculator</b> (Exact shares to buy per 1.5% risk)",
        "3️⃣ <b>All 72 US Stocks Target Levels + Position Doctor + TradingView Pine Script v5</b>",
        "",
        "👇 <b>Launch the Live Terminal or Unlock Pro VIP Access below:</b>",
    ])
    return "\n".join(lines)


def build_inline_keyboard() -> dict:
    return {
        "inline_keyboard": [
            [
                {
                    "text": "🖥️ Open Live Terminal (truthofmarket.com)",
                    "url": "https://truthofmarket.com",
                }
            ],
            [
                {
                    "text": "👑 Unlock Pro Monthly ($29/mo)",
                    "url": "https://truthofmarket.lemonsqueezy.com/checkout/buy/bad98d00-7175-41f6-9d58-eeb2471d0da4",
                },
                {
                    "text": "🏆 Lifetime VIP Pass ($199)",
                    "url": "https://truthofmarket.lemonsqueezy.com/checkout/buy/00c9f6e1-c8be-42a4-b5a5-e05af1a41ed9",
                },
            ],
            [
                {
                    "text": "📈 TradingView Pro Chart",
                    "url": "https://www.tradingview.com/?aff_id=1173809",
                },
                {
                    "text": "⚡ Trade on Bitget (24/7)",
                    "url": "https://www.bitget.com/referral/register?clacCode=7nja",
                },
            ],
            [
                {
                    "text": "▶️ YouTube (@rightsidealpha)",
                    "url": "https://youtube.com/@rightsidealpha",
                },
                {
                    "text": "📸 Instagram (@semifeargreed)",
                    "url": "https://www.instagram.com/semifeargreed",
                },
            ],
        ]
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--setup", action="store_true", help="Configure Bot & Channel profile in English")
    parser.add_argument("--pin", action="store_true", help="Pin the broadcasted message in the channel")
    args = parser.parse_args()

    token, chat_id = load_tg_credentials()
    if not token:
        print("No TELEGRAM_BOT_TOKEN configured; skipping live Telegram broadcast.")
        return

    base_url = f"https://api.telegram.org/bot{token}"
    with httpx.Client(timeout=15.0) as client:
        if args.setup:
            setup_bot_and_channel_english(client, base_url, chat_id)

        msg_html = build_english_daily_briefing()
        resp = client.post(
            f"{base_url}/sendMessage",
            json={
                "chat_id": chat_id,
                "text": msg_html,
                "parse_mode": "HTML",
                "disable_web_page_preview": True,
                "reply_markup": build_inline_keyboard(),
            },
        ).json()
        print("sendMessage:", resp.get("ok"), "message_id:", resp.get("result", {}).get("message_id"))

        if args.pin and resp.get("ok"):
            msg_id = resp["result"]["message_id"]
            r_pin = client.post(
                f"{base_url}/pinChatMessage",
                json={"chat_id": chat_id, "message_id": msg_id, "disable_notification": False},
            ).json()
            print("pinChatMessage:", r_pin)


if __name__ == "__main__":
    main()
