#!/usr/bin/env python3
"""
telegram_bot_runner.py - Standalone CLI & Long-Polling Runner for RightSideAlpha × SemiFearGreed Telegram Bot

Usage examples:
  python telegram_bot_runner.py --setup --token "123456:ABC..." --chat-id "987654321"
  python telegram_bot_runner.py --detect-chat-id --token "123456:ABC..."
  python telegram_bot_runner.py --send-briefing full
  python telegram_bot_runner.py --send-briefing ignition
  python telegram_bot_runner.py --send-briefing semi
  python telegram_bot_runner.py --send-pdf
  python telegram_bot_runner.py --poll
"""
import argparse
import sys
import time
from pathlib import Path
from typing import Optional

import httpx

BASE_DIR = Path(__file__).resolve().parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

from backend.app.models.telegram import TelegramConfigRequest, TelegramSendRequest
from backend.app.services.quant_engine import quant_engine
from backend.app.services.semi_engine import semi_engine
from backend.app.services.telegram_service import telegram_service


def find_latest_pdf(explicit_path: Optional[str] = None) -> Optional[Path]:
    """Resolves explicit PDF path or locates the latest daily PDF from 5_퀀트백테스트_텔레그램PDF_엔진/daily_pdf/."""
    if explicit_path and explicit_path != "AUTO":
        p = Path(explicit_path).expanduser().resolve()
        return p if p.exists() else None

    candidate_dirs = [
        BASE_DIR.parent / "5_퀀트백테스트_텔레그램PDF_엔진" / "daily_pdf",
        BASE_DIR / "daily_pdf",
    ]
    for d in candidate_dirs:
        if d.exists() and d.is_dir():
            pdfs = sorted(d.glob("*.pdf"), key=lambda x: x.stat().st_mtime, reverse=True)
            if pdfs:
                return pdfs[0]
    return None


def run_long_polling(token_override: Optional[str] = None) -> int:
    """Runs interactive Telegram Bot long-polling loop."""
    if token_override:
        telegram_service.update_config(
            TelegramConfigRequest(
                bot_token=token_override,
                chat_id=telegram_service.get_status().chat_id,
            )
        )

    token = telegram_service._resolve_token(token_override)
    if not token:
        print("[TelegramBot] ERROR: No bot_token configured. Run with --setup --token <TOKEN> first.")
        return 1

    print("[TelegramBot] Starting long-polling loop... Press Ctrl+C to stop.")
    print("[TelegramBot] Supported commands: /start, /help, /ignition, /semi, /full, /stock <TICKER>, /doctor <TICKER> <ENTRY> <DAYS>")
    offset = 0
    base_url = f"https://api.telegram.org/bot{token}"

    try:
        with httpx.Client(timeout=35.0) as client:
            while True:
                try:
                    # Daily 06:00 AM KST Auto-Delivery Check (EP01..EP10)
                    now_dt = time.localtime()
                    if now_dt.tm_hour == 6 and now_dt.tm_min <= 2:
                        try:
                            from daily_6am_shorts_sender import (
                                load_daily_state,
                                send_episode_package_to_telegram,
                            )
                            st = load_daily_state()
                            today_str = time.strftime("%Y-%m-%d", now_dt)
                            if st.get("last_sent_date") != today_str:
                                next_ep = int(st.get("next_ep", 1))
                                print(f"[TelegramBot] 06:00 AM Trigger: Sending Episode {next_ep}...")
                                send_episode_package_to_telegram(next_ep, advance_state=True)
                        except Exception as sched_exc:
                            print(f"[TelegramBot] 06:00 AM Scheduler warning: {sched_exc}")

                    resp = client.get(
                        f"{base_url}/getUpdates",
                        params={"timeout": 25, "offset": offset},
                    )
                    data = resp.json() if resp.content else {}
                    if resp.status_code == 200 and data.get("ok"):
                        for upd in data.get("result", []):
                            upd_id = int(upd.get("update_id", 0))
                            offset = max(offset, upd_id + 1)
                            reply = telegram_service.handle_webhook_update(upd)
                            print(f"[TelegramBot] Processed update_id={upd_id} ({len(reply)} chars)")
                    else:
                        print(f"[TelegramBot] getUpdates warning: {data}")
                        time.sleep(3.0)
                except KeyboardInterrupt:
                    raise
                except Exception as exc:
                    print(f"[TelegramBot] Polling error: {exc}")
                    time.sleep(3.0)
    except KeyboardInterrupt:
        print("\n[TelegramBot] Long-polling stopped.")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(
        description="RightSideAlpha × SemiFearGreed Telegram Bot CLI & Runner"
    )
    parser.add_argument("--setup", action="store_true", help="Save token & chat-id configuration and send test message")
    parser.add_argument("--token", type=str, default=None, help="Telegram Bot Token from @BotFather")
    parser.add_argument("--chat-id", type=str, default=None, help="Target Telegram Chat ID or Channel ID")
    parser.add_argument("--detect-chat-id", action="store_true", help="Auto-detect latest chat_id via getUpdates")
    parser.add_argument(
        "--send-briefing",
        nargs="?",
        const="full",
        default=None,
        choices=["full", "ignition", "semi", "test", "doctor"],
        help="Send or preview quant briefing (full | ignition | semi | test | doctor)",
    )
    parser.add_argument(
        "--send-pdf",
        nargs="?",
        const="AUTO",
        default=None,
        help="Upload latest daily PDF report to Telegram via sendDocument",
    )
    parser.add_argument("--poll", action="store_true", help="Run interactive long-polling Telegram bot")
    parser.add_argument("--lang", type=str, default="kr", choices=["kr", "en"], help="Briefing language (kr | en)")

    args = parser.parse_args()

    quant_engine.initialize()
    semi_engine.initialize()

    if args.setup:
        status = telegram_service.update_config(
            TelegramConfigRequest(
                bot_token=args.token,
                chat_id=args.chat_id,
            )
        )
        print(f"[TelegramBot] Configuration saved: configured={status.configured}, token={status.bot_token_masked}, chat_id={status.chat_id}")
        res = telegram_service.dispatch_briefing(
            TelegramSendRequest(briefing_type="test", lang=args.lang)
        )
        print(f"[TelegramBot] Test dispatch: delivered={res.delivered}, simulated={res.simulated} — {res.detail}")
        print("\n" + res.message_preview)
        return 0

    if args.detect_chat_id:
        det = telegram_service.detect_chat_id(bot_token=args.token)
        print(f"[TelegramBot] detect_chat_id: ok={det.ok}, chat_id={det.chat_id}, title={det.chat_title} — {det.detail}")
        return 0 if det.ok else 1

    if args.send_briefing is not None:
        res = telegram_service.dispatch_briefing(
            TelegramSendRequest(
                briefing_type=args.send_briefing,
                bot_token=args.token,
                chat_id=args.chat_id,
                lang=args.lang,
            )
        )
        print(f"[TelegramBot] Briefing '{res.briefing_type}': delivered={res.delivered}, simulated={res.simulated}")
        print(f"[TelegramBot] Detail: {res.detail}\n")
        print(res.message_preview)
        return 0

    if args.send_pdf is not None:
        pdf_path = find_latest_pdf(args.send_pdf)
        if not pdf_path:
            print("[TelegramBot] No PDF file found to upload.")
            return 1
        semi_ov = semi_engine.get_overview()
        caption = (
            f"📄 <b>[RightSideAlpha × SemiFearGreed] Daily Quant PDF Report</b>\n"
            f"File: <code>{pdf_path.name}</code> | Semi F&G: <b>{semi_ov.fg_score:.1f}/100 ({semi_ov.regime_kr})</b>"
        )
        delivered, simulated, detail = telegram_service.send_document(
            file_path=pdf_path,
            caption=caption,
            override_token=args.token,
            override_chat_id=args.chat_id,
        )
        print(f"[TelegramBot] PDF upload ({pdf_path.name}): delivered={delivered}, simulated={simulated} — {detail}")
        return 0 if (delivered or simulated) else 1

    if args.poll:
        return run_long_polling(token_override=args.token)

    # Default action when invoked with no flags: print current status & full briefing preview
    st = telegram_service.get_status()
    print(f"[TelegramBot] Status: configured={st.configured}, chat_id='{st.chat_id}', channel={st.channel_url}")
    preview = telegram_service.build_full_morning_briefing(lang=args.lang)
    print("\n" + preview)
    return 0


if __name__ == "__main__":
    sys.exit(main())
