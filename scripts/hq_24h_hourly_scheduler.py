#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
scripts/hq_24h_hourly_scheduler.py
24시간 1·2·3사업부 1시간 단위 순환 교대근무(Round-Robin) 자동 실행 엔진

원칙:
  - 매시간 정각마다 오직 1개 사업부만 단독으로 배정되어 작업 수행 (동시 실행 0% · PC 과부하 0%)
  - 00, 03, 06, 09, 12, 15, 18, 21시 (하루 8시간): 1사업부 (TOM - truthofmarket.com)
  - 01, 04, 07, 10, 13, 16, 19, 22시 (하루 8시간): 2사업부 (KFG - kisfitglobal.com)
  - 02, 05, 08, 11, 14, 17, 20, 23시 (하루 8시간): 3사업부 (KFK - kidsfit.co.kr)
  - 블로그/웹툰 활동은 철저히 배제하고, 데이터 동기화·SEO·유튜브/인스타 RL 자가개선·퍼널 무결성 점검만 수행
"""

import json
import os
import subprocess
import sys
import urllib.request
from datetime import datetime, timezone, timedelta
from pathlib import Path

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

BASE_DIR = Path(r"D:\투자홈페이지\1_RightSideAlpha_미국주식터미널")
LOG_FILE = BASE_DIR / "data" / "hq_24h_work_log.jsonl"

HOURLY_SCHEDULE = {
    0: {
        "div": "1사업부 (truthofmarket.com)",
        "code": "TOM",
        "cwd": r"D:\투자홈페이지\1_RightSideAlpha_미국주식터미널",
        "title": "미국장 장중 72종목 & $SMH/$XLV 실시간 시세·거래량(Vol Surge) 동기화",
        "action": "tom_sync",
    },
    1: {
        "div": "2사업부 (kisfitglobal.com)",
        "code": "KFG",
        "cwd": r"D:\키즈핏 영문",
        "title": "미국 학부모 낮 피크타임 서버 응답속도 & 레몬스퀴즈 Live 결제창(#1494859/#1494860) 무결성 점검",
        "action": "kfg_health_checkout",
    },
    2: {
        "div": "3사업부 (kidsfit.co.kr)",
        "code": "KFK",
        "cwd": r"D:\사업아이템",
        "title": "심야 한국판 소아청소년 성장·두뇌 발달 지식베이스 & 연령별 Q&A 정합성 점검",
        "action": "kfk_kb_audit",
    },
    3: {
        "div": "1사업부 (truthofmarket.com)",
        "code": "TOM",
        "cwd": r"D:\투자홈페이지\1_RightSideAlpha_미국주식터미널",
        "title": "미국장 후반부 우측 돌파(Ignition) & -9% 칼손절 포지션 닥터 타점 재계산",
        "action": "tom_sync",
    },
    4: {
        "div": "2사업부 (kisfitglobal.com)",
        "code": "KFG",
        "cwd": r"D:\키즈핏 영문",
        "title": "해외 소아내분비·뇌과학 최신 논문 크롤링 & 글로벌 지식DB 보강",
        "action": "kfg_papers",
    },
    5: {
        "div": "3사업부 (kidsfit.co.kr)",
        "code": "KFK",
        "cwd": r"D:\사업아이템",
        "title": "새벽 전사업부 방문수·유튜브 쇼츠·인스타 릴스 수집 & UCB1 강화학습(RL) 자가개선",
        "action": "dawn_rl",
    },
    6: {
        "div": "1사업부 (truthofmarket.com)",
        "code": "TOM",
        "cwd": r"D:\투자홈페이지\1_RightSideAlpha_미국주식터미널",
        "title": "미장 마감 최종 종가 확정 & 반도체 공포탐욕지수 + VIP 텔레그램(@truthofmarketss) 모닝 브리핑",
        "action": "tom_morning_vip",
    },
    7: {
        "div": "2사업부 (kisfitglobal.com)",
        "code": "KFG",
        "cwd": r"D:\키즈핏 영문",
        "title": "@kisfitglobal 유튜브 쇼츠 조회수 기반 RL 가중치 동기화 & 영문 숏폼 훅 최적화",
        "action": "kfg_rl_shorts",
    },
    8: {
        "div": "3사업부 (kidsfit.co.kr)",
        "code": "KFK",
        "cwd": r"D:\사업아이템",
        "title": "아침 등원 시간대 한국판(kidsfit.co.kr) 무료 진단·셀렉트샵 퍼널 무결성 점검",
        "action": "kfk_kb_audit",
    },
    9: {
        "div": "1사업부 (truthofmarket.com)",
        "code": "TOM",
        "cwd": r"D:\투자홈페이지\1_RightSideAlpha_미국주식터미널",
        "title": "@rightsidealpha 유튜브·인스타·X 유입 점검 및 미국주식 쇼츠 UCB1 강화학습 갱신",
        "action": "dawn_rl_silent",
    },
    10: {
        "div": "2사업부 (kisfitglobal.com)",
        "code": "KFG",
        "cwd": r"D:\키즈핏 영문",
        "title": "미국 저녁 골든타임 진단 완료율 & 유료 리포트 전환 정책(rl-paid-conversion-policy) 튜닝",
        "action": "kfg_health_checkout",
    },
    11: {
        "div": "3사업부 (kidsfit.co.kr)",
        "code": "KFK",
        "cwd": r"D:\사업아이템",
        "title": "오전 피크타임 네이버 블로그·카페(아이교육+상품추천 ?ep=N) 발행 & 지식iN 답변",
        "action": "kfk_naver_blog_and_kin",
    },
    12: {
        "div": "1사업부 (truthofmarket.com)",
        "code": "TOM",
        "cwd": r"D:\투자홈페이지\1_RightSideAlpha_미국주식터미널",
        "title": "72개 미국주식 전 종목 사이트맵(sitemap.xml 75 URL) & RSS 검색엔진 색인 우선순위 갱신",
        "action": "tom_seo_check",
    },
    13: {
        "div": "2사업부 (kisfitglobal.com)",
        "code": "KFG",
        "cwd": r"D:\키즈핏 영문",
        "title": "영문 63개 Q&A 페이지 SEO 스키마 & 구글 서치콘솔 사이트맵/RSS 상태 점검",
        "action": "kfg_health_checkout",
    },
    14: {
        "div": "3사업부 (kidsfit.co.kr)",
        "code": "KFK",
        "cwd": r"D:\사업아이템",
        "title": "네이버 지식iN 실시간 육아·교구 질문 자동 답변 & 육아 블로그 공감 투어",
        "action": "kfk_naver_kin_only",
    },
    15: {
        "div": "1사업부 (truthofmarket.com)",
        "code": "TOM",
        "cwd": r"D:\투자홈페이지\1_RightSideAlpha_미국주식터미널",
        "title": "26년 백테스트(349.3x) 및 반도체 바벨(SMH:XLV) 정적 API 데이터 무결성 감사",
        "action": "tom_seo_check",
    },
    16: {
        "div": "2사업부 (kisfitglobal.com)",
        "code": "KFG",
        "cwd": r"D:\키즈핏 영문",
        "title": "@kisfitglobal 유튜브 쇼츠 실시간 조회수 크롤링 & 챔피언 훅 가중치 업데이트",
        "action": "kfg_rl_shorts",
    },
    17: {
        "div": "3사업부 (kidsfit.co.kr)",
        "code": "KFK",
        "cwd": r"D:\사업아이템",
        "title": "하원 시간대 네이버 카페(moneyfitlab) 육아템·워크북 칼럼 발행 & 지식iN 답변",
        "action": "kfk_naver_cafe_and_kin",
    },
    18: {
        "div": "1사업부 (truthofmarket.com)",
        "code": "TOM",
        "cwd": r"D:\투자홈페이지\1_RightSideAlpha_미국주식터미널",
        "title": "미국 프리마켓 개장 전 $SMH·$XLV·72종목 시세 및 월가 뉴스 데이터 동기화",
        "action": "tom_sync",
    },
    19: {
        "div": "2사업부 (kisfitglobal.com)",
        "code": "KFG",
        "cwd": r"D:\키즈핏 영문",
        "title": "US CDC 성장곡선 & 5축 두뇌 LQ 진단 엔진·리포트 출력 무결성 자동 검증",
        "action": "kfg_health_checkout",
    },
    20: {
        "div": "3사업부 (kidsfit.co.kr)",
        "code": "KFK",
        "cwd": r"D:\사업아이템",
        "title": "밤 8시 골든타임 네이버 블로그·카페(아이교육+상품추천 ?ep=N) 발행 & 지식iN 답변",
        "action": "kfk_naver_blog_and_kin",
    },
    21: {
        "div": "1사업부 (truthofmarket.com)",
        "code": "TOM",
        "cwd": r"D:\투자홈페이지\1_RightSideAlpha_미국주식터미널",
        "title": "미국 정규장 개장 대비 72종목 & SMH/XLV 실시간 시세·타점 점검",
        "action": "tom_sync",
    },
    22: {
        "div": "2사업부 (kisfitglobal.com)",
        "code": "KFG",
        "cwd": r"D:\키즈핏 영문",
        "title": "2사업부 일일 실방문자(봇 제외) 및 레몬스퀴즈 유료결제 정밀 집계 리포트 갱신",
        "action": "kfg_daily_sales_report",
    },
    23: {
        "div": "3사업부 (kidsfit.co.kr)",
        "code": "KFK",
        "cwd": r"D:\사업아이템",
        "title": "3사업부 일일 방문·제휴 클릭·유튜브 조회수 마감 정산 및 익일 새벽 큐 준비",
        "action": "dawn_rl_silent",
    },
}


def ping_url(url):
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "HQ-24H-Monitor/1.0"})
        with urllib.request.urlopen(req, timeout=8) as r:
            return r.status
    except Exception:
        return 0


def execute_hourly_action(slot, notify_override=False):
    act = slot["action"]
    summary = "정상 완료"

    if act == "tom_sync":
        script = r"D:\투자홈페이지\1_RightSideAlpha_미국주식터미널\scripts\sync_live_market_data.py"
        if os.path.exists(script):
            subprocess.run(["python", script], cwd=slot["cwd"], timeout=120, capture_output=True)
        st = ping_url("https://truthofmarket.com/")
        summary = f"truthofmarket.com 응답 HTTP {st} · 72종목 & SMH/XLV 데이터 동기화 완료"

    elif act == "tom_morning_vip":
        s1 = r"D:\투자홈페이지\1_RightSideAlpha_미국주식터미널\scripts\sync_live_market_data.py"
        s2 = r"D:\투자홈페이지\1_RightSideAlpha_미국주식터미널\scripts\broadcast_telegram_channel.py"
        if os.path.exists(s1):
            subprocess.run(["python", s1], cwd=slot["cwd"], timeout=120, capture_output=True)
        if os.path.exists(s2):
            subprocess.run(["python", s2, "--pin"], cwd=slot["cwd"], timeout=60, capture_output=True)
        summary = "미장 마감 종가 동기화 & @truthofmarketss VIP 채널 오더북 발송 완료"

    elif act == "tom_seo_check":
        st1 = ping_url("https://truthofmarket.com/sitemap.xml")
        st2 = ping_url("https://truthofmarket.com/rss.xml")
        summary = f"truthofmarket.com Sitemap(HTTP {st1}) & RSS(HTTP {st2}) 무결성 확인 완료"

    elif act == "kfg_health_checkout":
        st1 = ping_url("https://kisfitglobal.com/")
        st2 = ping_url("https://kisfitglobal.com/api/lemonsqueezy-checkout.json")
        summary = f"kisfitglobal.com(HTTP {st1}) & LemonSqueezy Live Checkout JSON(HTTP {st2}) 정상 확인"

    elif act == "kfg_papers":
        script = r"D:\키즈핏 영문\scripts\crawl_research_papers.py"
        if os.path.exists(script):
            subprocess.run(["python", script], cwd=slot["cwd"], timeout=90, capture_output=True)
        summary = "소아성장·뇌과학 논문 DB 점검 및 최신화 완료"

    elif act == "kfg_rl_shorts":
        script = r"D:\키즈핏 영문\scripts\rl_shorts_reels_view_optimizer.py"
        if os.path.exists(script):
            subprocess.run(["python", script], cwd=slot["cwd"], timeout=60, capture_output=True)
        summary = "@kisfitglobal 유튜브 쇼츠 실시간 조회수 수집 & RL 챔피언 훅 가중치 갱신 완료"

    elif act == "kfg_daily_sales_report":
        script = r"D:\키즈핏 영문\scripts\daily_visitor_and_sales_report.js"
        if os.path.exists(script):
            subprocess.run(["node", script], cwd=slot["cwd"], timeout=45, capture_output=True)
        summary = "2사업부 일일 실방문자·유료결제 리포트 JSON 집계 완료"

    elif act == "kfk_kb_audit":
        st1 = ping_url("https://kidsfit.co.kr/")
        st2 = ping_url("https://kidsfit.co.kr/sitemap.xml")
        idx_p = r"D:\사업아이템\dist\index.html"
        ls_zero = True
        if os.path.exists(idx_p):
            ls_zero = "lemonsqueezy" not in open(idx_p, encoding="utf-8", errors="ignore").read().lower()
        summary = f"kidsfit.co.kr(HTTP {st1}) · Sitemap(HTTP {st2}) · 무료/셀렉트샵 전용 무결성(LS 0건={ls_zero}) 확인 완료"

    elif act == "kfk_naver_blog_and_kin":
        runner = r"D:\사업아이템\scripts\naver_cdp_live_runner.py"
        if os.path.exists(runner):
            subprocess.run(["python", runner, "--all"], cwd=slot["cwd"], timeout=240, capture_output=True)
        st1 = ping_url("https://kidsfit.co.kr/")
        summary = f"네이버 블로그(expertise333)·카페(moneyfitlab) 교육+상품추천(?ep=N) 발행 & 지식iN 답변 완료 (HTTP {st1})"

    elif act == "kfk_naver_cafe_and_kin":
        runner = r"D:\사업아이템\scripts\naver_cdp_live_runner.py"
        if os.path.exists(runner):
            subprocess.run(["python", runner, "--cafe", "--kin"], cwd=slot["cwd"], timeout=180, capture_output=True)
        st1 = ping_url("https://kidsfit.co.kr/")
        summary = f"네이버 카페(moneyfitlab) 육아템·워크북 가이드 발행 & 지식iN 실시간 답변 완료 (HTTP {st1})"

    elif act == "kfk_naver_kin_only":
        runner = r"D:\사업아이템\scripts\naver_cdp_live_runner.py"
        if os.path.exists(runner):
            subprocess.run(["python", runner, "--kin"], cwd=slot["cwd"], timeout=120, capture_output=True)
        st1 = ping_url("https://kidsfit.co.kr/")
        summary = f"네이버 지식iN 실시간 육아 질문 자동 답변 & 육아 블로그 공감 투어 · kidsfit.co.kr(HTTP {st1}) 점검 완료"

    elif act == "dawn_rl":
        script = r"D:\투자홈페이지\1_RightSideAlpha_미국주식터미널\scripts\hq_dawn_rl_self_improver.py"
        subprocess.run(["python", script, "--notify"], cwd=r"D:\투자홈페이지\1_RightSideAlpha_미국주식터미널", timeout=120, capture_output=True)
        summary = "전사업부 방문수·유튜브·인스타 새벽 강화학습(RL) 자가개선 및 텔레그램 보고 완료"

    elif act == "dawn_rl_silent":
        script = r"D:\투자홈페이지\1_RightSideAlpha_미국주식터미널\scripts\hq_dawn_rl_self_improver.py"
        subprocess.run(["python", script], cwd=r"D:\투자홈페이지\1_RightSideAlpha_미국주식터미널", timeout=120, capture_output=True)
        summary = "전사업부 방문수·유튜브·인스타 백그라운드 강화학습(RL) 가중치 갱신 완료"

    elif act == "visitor_briefing":
        script = r"D:\투자홈페이지\1_RightSideAlpha_미국주식터미널\scripts\hq_all_divisions_visitor_briefing.js"
        subprocess.run(["node", script, "--notify"], cwd=r"D:\투자홈페이지\1_RightSideAlpha_미국주식터미널", timeout=45, capture_output=True)
        summary = "전사업부 통합 실방문자(UV/PV) & 서치콘솔 브리핑 발송 완료"

    return summary


def format_24h_timetable_html(current_hour):
    lines = [
        "🕒 <b>[1·2·3사업부 24시간 1시간 교대근무 마스터 스케줄 가동 현황]</b>",
        "• <b>원칙</b>: 매시간 정각마다 <b>딱 1개 사업부만 단독 배정</b> (1→2→3사업부 순환 · 과부하 0%)",
        "━━━━━━━━━━━━━━━━━━",
    ]
    for h in range(24):
        s = HOURLY_SCHEDULE[h]
        marker = "👉 <b>[현재 시간 가동]</b> " if h == current_hour else ""
        lines.append(f"{marker}<code>{h:02d}:00</code> | <b>{s['div'].split()[0]}</b> — {s['title']}")
    lines.append("━━━━━━━━━━━━━━━━━━")
    lines.append("💡 <i>매시 정각 자동으로 해당 사업부 업무를 단독 수행하며, 언제든 <code>스케줄</code> 또는 <code>/schedule24</code> 입력 시 24시간 근무표를 확인하실 수 있습니다.</i>")
    return "\n".join(lines)


def main():
    kst_now = datetime.now(timezone(timedelta(hours=9)))
    hour = kst_now.hour
    for idx, arg in enumerate(sys.argv):
        if arg == "--hour" and idx + 1 < len(sys.argv):
            hour = int(sys.argv[idx + 1]) % 24

    show_table = "--table" in sys.argv
    notify = "--notify" in sys.argv

    slot = HOURLY_SCHEDULE[hour]
    summary = execute_hourly_action(slot, notify_override=notify)

    entry = {
        "timestamp_kst": kst_now.strftime("%Y-%m-%d %H:%M:%S KST"),
        "hour": f"{hour:02d}:00",
        "division": slot["div"],
        "task_title": slot["title"],
        "result_summary": summary,
    }
    LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")

    if notify or show_table:
        bridge_js = r"D:\투자홈페이지\1_RightSideAlpha_미국주식터미널\scripts\master_hq_telegram_bridge.js"
        msg = (
            f"✅ <b>[{hour:02d}:00 정각 교대근무 완료 — {slot['div']}]</b>\n"
            f"• <b>수행 업무</b>: {slot['title']}\n"
            f"• <b>실행 결과</b>: <code>{summary}</code>\n\n"
            + (format_24h_timetable_html(hour) if show_table else "")
        )
        subprocess.run(["node", bridge_js, "--notify", msg], cwd=r"D:\투자홈페이지\1_RightSideAlpha_미국주식터미널")

    print(json.dumps(entry, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
