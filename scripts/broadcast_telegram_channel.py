#!/usr/bin/env python3
"""
scripts/broadcast_telegram_channel.py - Pro VIP Exclusive Telegram Channel Setup,
Unmasked Ignition Order Book & Real-Time $SMH/$XLV + 72-Stock News Broadcast (100% English)
"""
import argparse
import html
import json
import os
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Dict, List
import httpx

BASE_DIR = Path(__file__).resolve().parent.parent
TG_CONFIG_PATH = BASE_DIR / "data" / "telegram_config.json"
SEMI_JSON_PATH = BASE_DIR / "frontend" / "public" / "static_api" / "semi_overview.json"
STOCKS_PRO_PATH = BASE_DIR / "frontend" / "public" / "static_api" / "stocks_pro.json"


def load_tg_credentials():
    token = os.getenv("TELEGRAM_BOT_TOKEN", "").strip()
    chat_id = os.getenv("TELEGRAM_CHAT_ID", "").strip() or "-1004248811575"
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


def fetch_ticker_news(client: httpx.Client, symbol: str, max_items: int = 2) -> List[Dict[str, str]]:
    """Fetches real-time English Wall Street news headlines for a ticker via Yahoo Finance RSS."""
    url = f"https://feeds.finance.yahoo.com/rss/2.0/headline?s={symbol}&region=US&lang=en-US"
    results: List[Dict[str, str]] = []
    try:
        r = client.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=8.0)
        if r.status_code == 200 and r.text:
            root = ET.fromstring(r.text)
            for item in root.findall("./channel/item")[:max_items]:
                title = (item.findtext("title") or "").strip()
                link = (item.findtext("link") or "").strip()
                if title and link:
                    results.append({"symbol": symbol, "title": title, "link": link})
    except Exception:
        pass
    return results


def setup_bot_and_channel_english(client: httpx.Client, base_url: str, chat_id: str) -> None:
    client.post(
        f"{base_url}/setMyName",
        json={"name": "TruthOfMarket | Pro VIP Quant & News Bot"},
    )
    client.post(
        f"{base_url}/setMyShortDescription",
        json={
            "short_description": (
                "Pro VIP Exclusive $SMH/$XLV & 72-Equity Breaking News + Ignition Order Book Bot — https://truthofmarket.com"
            )
        },
    )
    client.post(
        f"{base_url}/setMyDescription",
        json={
            "description": (
                "Official Pro VIP Quantitative & Breaking News Bot for TruthOfMarket (https://truthofmarket.com)\n\n"
                "👑 Pro VIP Exclusive Channel (Subscribers Only)\n"
                "📰 Real-Time $SMH, $XLV & 72 US Equity Breaking News\n"
                "🎯 Daily Unmasked Right-Side PW-RSI Ignition Order Book\n"
                "🧭 Semiconductor 7-Factor Fear & Greed Index"
            )
        },
    )
    client.post(
        f"{base_url}/setChatTitle",
        json={
            "chat_id": chat_id,
            "title": "TruthOfMarket VIP | $SMH·$XLV & 72 US Stock News",
        },
    )
    client.post(
        f"{base_url}/setChatDescription",
        json={
            "chat_id": chat_id,
            "description": (
                "👑 PRO VIP SUBSCRIBERS ONLY • Real-Time $SMH/$XLV & 72-Equity Breaking News • "
                "Unmasked Daily Right-Side PW-RSI Ignition Order Book.\n"
                "🖥️ Terminal & License Verification: https://truthofmarket.com"
            ),
        },
    )


def build_vip_briefing_with_news(client: httpx.Client) -> str:
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

    lines = [
        f"👑 <b>[TRUTHOFMARKET PRO VIP] DAILY ORDER BOOK &amp; BREAKING NEWS ({as_of})</b>",
        "━━━━━━━━━━━━━━━━━━━━",
        "🧭 <b>1. Semiconductor ($SMH) &amp; Healthcare ($XLV) Barbell Desk</b>",
        f"• <b>Fear &amp; Greed Score</b>: <b>{fg_score:.1f} / 100 ({regime_en})</b>",
        f"• <b>Target Barbell Allocation</b>: <b>{smh_w}% $SMH : {xlv_w}% $XLV</b>",
        f"• <b>$SMH</b>: <b>${smh_close:.2f}</b> ({smh_dd:.2f}% 52W DD | RSI {smh_rsi:.1f}) | <b>$XLV</b>: <b>${xlv_close:.2f}</b> | <b>$QQQ</b>: <b>${qqq_close:.2f}</b>",
        "",
        f"🎯 <b>2. Unmasked Pro VIP Ignition Order Book ({len(ignition)} Active Signals)</b>",
    ]

    for idx, s in enumerate(ignition[:5], start=1):
        close_p = float(s["close"])
        trg_p = float(s.get("entry_trigger_price") or close_p)
        stp_p = float(s.get("stop_loss_price") or close_p * 0.93)
        tp1_p = float(s.get("tp1_2x_price") or close_p * 1.05)
        shares_10k = max(1, int(4500 // close_p))
        lines.append(
            f"<b>#{idx} ${s['ticker']}</b> ({html.escape(s.get('name_en', s['ticker']))}) — <b>${close_p:.2f}</b> | Score <b>{int(s['score'])}/100</b>\n"
            f"   └ 🎯 Entry: <code>${trg_p:.2f}</code> | 🛑 Stop(-7%): <code>${stp_p:.2f}</code> | 💰 TP1(+5%): <code>${tp1_p:.2f}</code> | 🧮 Ref Size: <code>{shares_10k} sh</code>"
        )

    # Fetch live news for SMH, XLV, and active Ignition stocks + top movers from the 72 universe
    lines.extend([
        "",
        "📰 <b>3. Live Wall Street News Radar ($SMH · $XLV · 72-Equity Universe)</b>",
    ])

    etf_news = fetch_ticker_news(client, "SMH", max_items=1) + fetch_ticker_news(client, "XLV", max_items=1)
    for n in etf_news:
        safe_title = html.escape(n["title"])
        safe_link = html.escape(n["link"], quote=True)
        lines.append(f"• <b>[${n['symbol']} ETF]</b> <a href=\"{safe_link}\">{safe_title}</a>")

    stock_Watch = [s["ticker"] for s in ignition[:4]]
    for extra in ("NVDA", "TSLA", "AMD", "PLTR"):
        if extra not in stock_Watch and len(stock_Watch) < 6:
            stock_Watch.append(extra)

    seen_titles = set()
    for sym in stock_Watch:
        items = fetch_ticker_news(client, sym, max_items=1)
        for n in items:
            if n["title"] in seen_titles:
                continue
            seen_titles.add(n["title"])
            safe_title = html.escape(n["title"])
            safe_link = html.escape(n["link"], quote=True)
            lines.append(f"• <b>[${sym}]</b> <a href=\"{safe_link}\">{safe_title}</a>")

    lines.extend([
        "━━━━━━━━━━━━━━━━━━━━",
        "🔒 <i>Strictly Confidential — For TruthOfMarket Pro VIP Subscribers Only.</i>",
    ])
    return "\n".join(lines)


def build_inline_keyboard() -> dict:
    return {
        "inline_keyboard": [
            [
                {
                    "text": "🖥️ Open Pro VIP Terminal (truthofmarket.com)",
                    "url": "https://truthofmarket.com",
                }
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
    parser.add_argument("--setup", action="store_true", help="Configure Bot & VIP Channel profile in English")
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

        msg_html = build_vip_briefing_with_news(client)
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
