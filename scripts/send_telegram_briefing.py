#!/usr/bin/env python3
"""
Standalone CLI & Cron Automation Script for Telegram Quantitative Briefings.

Usage Examples:
  python scripts/send_telegram_briefing.py --type FULL_DAILY --lang kr --dry-run
  python scripts/send_telegram_briefing.py --type SEMI_BRIEFING --lang kr --token <BOT_TOKEN> --chat-id <CHAT_ID>
  python scripts/send_telegram_briefing.py --type POSITION_DOCTOR --ticker CELH --entry 27.20 --days 42 --lang kr
"""
import argparse
import json
import sys
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from backend.app.models.telegram import TelegramDispatchRequest
from backend.app.services.telegram_service import telegram_service


def _run_cli(args: argparse.Namespace) -> int:
    req = TelegramDispatchRequest(
        alert_type=args.type,
        lang=args.lang,
        bot_token=args.token,
        chat_id=args.chat_id,
        ticker=args.ticker,
        entry_price=args.entry,
        days_held=args.days,
        custom_message=args.note,
        dry_run=args.dry_run,
    )
    res = telegram_service.dispatch_alert(req)
    if args.json:
        print(json.dumps(res.model_dump(), ensure_ascii=False, indent=2))
    else:
        print(f"=== Telegram Dispatch [{res.mode}] | Delivered: {res.delivered} ===")
        print(f"Detail: {res.status_detail}")
        print("-" * 64)
        print(res.message_preview)
        print("-" * 64)
    return 0 if res.ok else 1


def main() -> int:
    parser = argparse.ArgumentParser(description="Send or preview Alpha Finder & Semi Fear/Greed Telegram briefings.")
    parser.add_argument(
        "--type",
        default="FULL_DAILY",
        choices=["SEMI_BRIEFING", "RSA_IGNITION", "POSITION_DOCTOR", "FULL_DAILY", "TEST_PING"],
        help="Briefing template type (default: FULL_DAILY)",
    )
    parser.add_argument("--lang", default="kr", choices=["kr", "en", "jp"], help="Language code (kr, en, jp)")
    parser.add_argument("--token", default=None, help="Override Telegram Bot Token")
    parser.add_argument("--chat-id", default=None, help="Override Telegram Chat ID or @channel")
    parser.add_argument("--ticker", default="CELH", help="Ticker for POSITION_DOCTOR briefing")
    parser.add_argument("--entry", type=float, default=27.20, help="Entry price for POSITION_DOCTOR briefing")
    parser.add_argument("--days", type=int, default=42, help="Days held for POSITION_DOCTOR briefing")
    parser.add_argument("--note", default=None, help="Optional operator note appended to briefing")
    parser.add_argument("--dry-run", action="store_true", help="Preview message only without sending to Telegram API")
    parser.add_argument("--json", action="store_true", help="Output full JSON response")
    args = parser.parse_args()
    return _run_cli(args)


if __name__ == "__main__":
    raise SystemExit(main())
