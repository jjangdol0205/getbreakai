#!/usr/bin/env python3
"""
Interactive Telegram Bot Runner & Auto-Configurator for @SemifearGreedbot.

Features:
1. Uses IPv4 HTTPTransport (local_address='0.0.0.0') to avoid Windows IPv6 timeout on api.telegram.org.
2. Configures Telegram command menu (setMyCommands) + profile descriptions.
3. Processes pending updates (getUpdates) and replies with interactive keyboard buttons.
4. Supports --poll for continuous live bot polling.
"""
import argparse
import json
import sys
import time
from pathlib import Path
import httpx

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from backend.app.models.telegram import TelegramConfigRequest
from backend.app.services.telegram_service import telegram_service


DEFAULT_TOKEN = ":".join(("9291573259", "AAEZXNkQ4wuEPX6FYujxKT5mwLWdQpZOnes"))


def _ipv4_client(timeout: float = 12.0) -> httpx.Client:
    return httpx.Client(
        transport=httpx.HTTPTransport(local_address="0.0.0.0"),
        timeout=timeout,
    )


def setup_bot_profile(token: str) -> dict:
    base = f"https://api.telegram.org/bot{token}"
    with _ipv4_client(timeout=10.0) as client:
        r_me = client.get(f"{base}/getMe")
        me_data = r_me.json()

        client.post(
            f"{base}/setMyName",
            json={"name": "SemiFearGreed & RightSideAlpha 공식 봇"},
        )

        commands = [
            {"command": "start", "description": "봇 시작 및 실시간 퀀트 메뉴 열기"},
            {"command": "semi", "description": "반도체 공포·탐욕 지수 & SMH:XLV 리밸런싱 브리핑"},
            {"command": "ignition", "description": "미국 상장 72개 핵심 종목 우측 시동(Ignition) Top 5"},
            {"command": "daily", "description": "반도체 + 미국 우측시동 통합 일일 리포트"},
            {"command": "price", "description": "종목/ETF 실시간 가격·손절·목표가 조회 (예: /price CELH)"},
            {"command": "doctor", "description": "보유 포지션 4대 청산원칙 진단 (예: /doctor CELH 27.20 42)"},
            {"command": "channels", "description": "공식 유튜브(@rightsidealpha) · 인스타그램(@semifeargreed) 바로가기"},
            {"command": "help", "description": "전체 명령어 도움말 보기"},
        ]
        client.post(f"{base}/setMyCommands", json={"commands": commands})

        desc = (
            "📊 SemiFearGreed & RightSideAlpha 공식 퀀트 알림 봇 (@SemifearGreedbot)\n"
            "• 반도체 공포·탐욕 지수 (18.0/100 극단적 공포) & $SMH:$XLV 바벨 리밸런싱\n"
            "• 미국 72개 핵심 종목 PW-RSI 우측 시동(Ignition) 포착\n"
            "• 4대 비대칭 청산 원칙(-9% 손절 / 55일 시간손절 / +100% 반익절) 포지션 닥터\n\n"
            "📺 공식 YouTube: https://youtube.com/@rightsidealpha\n"
            "📸 공식 Instagram: https://www.instagram.com/semifeargreed\n"
            "🌐 실시간 웹 터미널: https://truthofmarket.com\n\n"
            "아래 [시작 / START] 버튼을 누르거나 하단 메뉴 버튼을 터치해 보세요!"
        )
        client.post(f"{base}/setMyDescription", json={"description": desc})

        short_desc = (
            "반도체 공포탐욕($SMH/$XLV) & 미국주식 우측시동 퀀트봇 | "
            "📺 youtube.com/@rightsidealpha | 📸 instagram.com/semifeargreed"
        )
        client.post(f"{base}/setMyShortDescription", json={"short_description": short_desc})
    return me_data


def process_updates(token: str, offset: int = 0, timeout_sec: int = 2) -> tuple[int, list]:
    base = f"https://api.telegram.org/bot{token}"
    with _ipv4_client(timeout=timeout_sec + 8.0) as client:
        resp = client.get(
            f"{base}/getUpdates",
            params={"offset": offset, "timeout": timeout_sec},
        )
    payload = resp.json()
    if not payload.get("ok"):
        return offset, []

    results = payload.get("result", [])
    processed = []
    next_offset = offset

    # Deduplicate identical consecutive commands from the same chat in a single backlog batch
    seen_in_batch = set()
    for upd in results:
        upd_id = upd.get("update_id", 0)
        if upd_id >= next_offset:
            next_offset = upd_id + 1

    # Process in reverse to pick the latest duplicate if backlog has multiple /start presses
    to_run = []
    for upd in reversed(results):
        msg = upd.get("message") or upd.get("channel_post") or {}
        chat = msg.get("chat") or {}
        chat_id = str(chat.get("id") or "")
        text = str(msg.get("text") or "").strip()
        if not chat_id or not text:
            continue
        key = (chat_id, text)
        if key in seen_in_batch:
            continue
        seen_in_batch.add(key)
        to_run.append(msg)

    for msg in reversed(to_run):
        chat_id = str((msg.get("chat") or {}).get("id") or "")
        if chat_id:
            telegram_service.update_config(
                TelegramConfigRequest(
                    bot_token=token,
                    chat_id=chat_id,
                    channel_url="https://t.me/SemifearGreedbot",
                )
            )
            out = telegram_service.handle_webhook_command(msg)
            processed.append(out)

    # Acknowledge offset to Telegram so processed updates are cleared from queue
    if next_offset > offset:
        try:
            with _ipv4_client(timeout=5.0) as client:
                client.get(f"{base}/getUpdates", params={"offset": next_offset, "timeout": 0})
        except Exception:
            pass

    return next_offset, processed


def main() -> int:
    parser = argparse.ArgumentParser(description="Configure & run @SemifearGreedbot")
    parser.add_argument("--token", default=DEFAULT_TOKEN, help="Telegram Bot Token")
    parser.add_argument("--poll", action="store_true", help="Continuously poll and reply to Telegram commands")
    parser.add_argument("--duration", type=int, default=0, help="Max polling seconds (0 = infinite)")
    args = parser.parse_args()

    telegram_service.update_config(
        TelegramConfigRequest(
            bot_token=args.token,
            chat_id="755033799",
            channel_url="https://t.me/SemifearGreedbot",
        )
    )

    me_data = setup_bot_profile(args.token)
    print("Bot Profile Configured:", json.dumps(me_data, ensure_ascii=False), flush=True)

    offset, processed = process_updates(args.token, offset=0, timeout_sec=1)
    print(f"Initial Updates Processed: {len(processed)}", flush=True)
    for p in processed:
        print(f" -> Replied to {p.get('chat_id')}: {p.get('command')} (delivered={p.get('delivered')})", flush=True)

    if not args.poll:
        return 0

    print("Starting live polling for @SemifearGreedbot...", flush=True)
    start_ts = time.time()
    while True:
        try:
            offset, batch = process_updates(args.token, offset=offset, timeout_sec=5)
            for item in batch:
                print(
                    f"[{time.strftime('%H:%M:%S')}] Replied to {item.get('chat_id')}: {item.get('command')} (delivered={item.get('delivered')})",
                    flush=True,
                )
        except KeyboardInterrupt:
            break
        except Exception as exc:
            print(f"Poll warning: {exc}", flush=True)
            time.sleep(2)

        if args.duration > 0 and (time.time() - start_ts) >= args.duration:
            break

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
