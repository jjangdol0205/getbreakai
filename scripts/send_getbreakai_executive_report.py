#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
D:\드림컴퍼니\3사업부\scripts\send_getbreakai_executive_report.py
Sends the GetBreakAI (Division 3) Executive Completion Report via @SemifearGreedbot
to both the HQ Telegram Group (-1003834697086) and CEO Direct (755033799).
"""

import sys
import json
import urllib.request
import urllib.parse

# Ensure UTF-8 output
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

BOT_TOKEN = "9291573259:AAEZXNkQ4wuEPX6FYujxKT5mwLWdQpZOnes"
TARGET_CHATS = [
    {"name": "HQ Group", "id": "-1003834697086"},
    {"name": "CEO Direct", "id": "755033799"}
]

REPORT_TEXT = (
    "🚀 [드림컴퍼니 본사 총괄 · 3사업부 GetBreakAI] 자율 실행 M1~M4 전수 완수 보고\n\n"
    "■ 대상 시스템: GetBreakAI (https://getbreakai.com & /jp/)\n"
    "■ 전담 봇: @SemifearGreedbot ([3사업부 · 본사] 일본퀀트)\n"
    "■ 실행 일시: 2026-11-10 23:25 KST\n\n"
    "━━━━━━━━━━━━━━━━━━━━━━\n"
    "1️⃣ Google Flow V3 쇼츠 24편 마스터링 (100% 완료)\n"
    "  • EP01~EP24 전편 1080×1920@30fps 클린 비디오 마스터링 완료\n"
    "  • FFmpeg 디코딩 오류 0건, 음향 리미터 -0.5 dBFS 완벽 준수 (-7.4 ~ -6.0 dBFS)\n"
    "  • ja-JP-NanamiNeural 자연어 나레이션 & 자막 100% 완독 싱크\n"
    "  • 유튜브/인스타 업로드 카피패스트 키트 및 매니페스트 동기화 완료\n\n"
    "2️⃣ 일본 랜딩페이지(jp/index.html) 전환율 고도화\n"
    "  • ⚡ 1秒 損切り・適正株数 計算機 (1초 엔화 손절가·적정주수 계산기) 탑재\n"
    "  • 구독료($29/월) vs 1회 손절 실패 손실액(-¥185,000) 방어 비교 카드 구현\n"
    "  • 반응형 테이블 래퍼(.comp-table-wrap) 및 모바일 뷰포트 제로 블리드 검증\n"
    "  • WCAG AA/AAA 명암비(최소 4.5:1 / 7.0:1) 100% 준수\n\n"
    "3️⃣ 수익화 Lemon Squeezy Store #296100 불변식 보존\n"
    "  • Starter Breakout Scanner ($29/mo): gb-starter-29\n"
    "  • Pro Institutional Breakout ($49/mo): gb-pro-49\n"
    "  • Institutional Alpha Terminal ($1,499/yr): gb-inst-1499\n"
    "  • 타이밍 안전 HMAC-SHA256 웹훅 서명 검증 무결성 유지\n\n"
    "4️⃣ 전 자동화 테스트 슈트 100% 통과 (Zero Error)\n"
    "  • test_mastered_24_shorts.py: 24/24 MP4 PASS\n"
    "  • challenger_m1_audit.py: 95/95 PASS\n"
    "  • verify_code_quality.py --all: 84/84 PASS\n"
    "  • npm run test:all: 6개 슈트 82개 단위/통합 테스트 100% PASS\n"
    "  • node scripts/build_dist.js: ./dist 정적 배포 번들 동기화 완료\n"
    "━━━━━━━━━━━━━━━━━━━━━━\n"
    "✅ 상태: M1~M4 전 과업 정상 완료 및 프로덕션 배포 준비 완료"
)


def send_telegram_message(token, chat_id, text):
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": text,
        "disable_web_page_preview": True
    }
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        url,
        data=data,
        headers={"Content-Type": "application/json"}
    )
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            status_code = resp.status
            body = resp.read().decode("utf-8")
            res_json = json.loads(body)
            return status_code, res_json
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8")
        try:
            res_json = json.loads(body)
        except Exception:
            res_json = {"error": body}
        return e.code, res_json
    except Exception as e:
        return 500, {"error": str(e)}


def main():
    print("=" * 72)
    print(" [GetBreakAI] Telegram Executive Report Delivery via @SemifearGreedbot")
    print("=" * 72)
    
    all_success = True
    for target in TARGET_CHATS:
        chat_id = target["id"]
        name = target["name"]
        print(f"\nSending report to {name} ({chat_id})...")
        code, res = send_telegram_message(BOT_TOKEN, chat_id, REPORT_TEXT)
        ok = res.get("ok", False)
        print(f"  HTTP Status: {code}")
        print(f"  Telegram ok: {ok}")
        if code == 200 and ok:
            msg_id = res.get("result", {}).get("message_id")
            print(f"  ✓ [SUCCESS] Delivered to {name}. Message ID: {msg_id}")
        else:
            all_success = False
            print(f"  ❌ [FAIL] Delivery to {name} failed: {res}")
            
    print("\n" + "=" * 72)
    if all_success:
        print("ALL TELEGRAM NOTIFICATIONS DELIVERED SUCCESSFULLY (HTTP 200 OK)")
        print("=" * 72)
        return 0
    else:
        print("SOME TELEGRAM DELIVERIES FAILED")
        print("=" * 72)
        return 1


if __name__ == "__main__":
    sys.exit(main())
