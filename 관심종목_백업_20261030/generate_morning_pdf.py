"""
[08:10 KST 모닝 알파 & 코어 포트폴리오 3페이지 PDF 자동 생성 엔진 (100% US & China Primary Sources)]
실행 방법:
  python "D:\\투자홈페이지\\관심종목_백업_20261030\\generate_morning_pdf.py"
  python "D:\\투자홈페이지\\관심종목_백업_20261030\\generate_morning_pdf.py" --open   # 생성 후 PDF 즉시 열기

특징:
  1. 대한민국 국내 언론/증권사 리포트 100% 배제 -> 오직 미국(US) 및 중국/중화권(CN/TW/HK) 1차 데이터·외신만 사용
  2. 구성안 A (행동 시간순 3페이지 고정 레이아웃):
     - Page 1: [오늘 아침 30초 통합 결론 배너] + [보유 코어 SK스퀘어(76주) 장전 시초가 브릿지 · 1억 졸업/주수 방어 · 미/중 8대 트리거 · 미/중 핵심 외신 Top 3]
     - Page 2: [미국 코어 ETF 바벨: SMH(60%) + XLV(40%)] 간밤 성적표(환쿠션 반영) · ±5%p 세금방어 밴드 & SMH -20% 역발상 틸트 · XLV 하방 쿠션 · Top 3 동인 및 미/중 산업 외신
     - Page 3: [미국 전용(US-Only) 동적 PW-RSI 알파 레이더] Actionable Top 5 (전일비 Δ, 4대 조건 체크, 달러 돌파 트리거 가격 $) · Today's Spotlight 딥다이브 카드(2종목) · 2단계 손절(-9%)/시간손절(55일) 트래커
"""

import os
import sys
import json
import subprocess
import concurrent.futures
import xml.etree.ElementTree as ET
from datetime import datetime
from typing import Optional, Tuple, Dict, Any, List
import urllib3
import requests
import pandas as pd
import numpy as np
import argparse
import shutil

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

from engine.primary_feed_us_cn import (
    assert_zero_korean_media,
    fetch_market_snapshot,
    fetch_proxy_quotes,
    build_primary_news_feed,
    PROXIES_META,
    SYMBOL_ALIASES,
    fetch_ticker_df as fetch_primary_ticker_df,
    compute_quote_metrics,
    find_blacklisted_media,
)
from engine.report_page1 import render_page1_html
from engine.report_page2 import render_page2_html
from engine.report_page3 import render_page3_html
from engine.pdf_compiler import (
    build_full_html_report,
    compile_html_to_pdf,
    verify_pdf_with_pymupdf,
)

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data_stocks")
ETF_DATA_DIR = os.path.join(BASE_DIR, "data")
OUT_DIR = os.path.join(BASE_DIR, "daily_pdf")
os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(OUT_DIR, exist_ok=True)

HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}

# 1. 코어 보유 포지션 설정 (1단계: SK스퀘어 76주 비과세 1억 졸업 -> 달러 1회 환전 -> 2단계 US-Only PW-RSI)
MY_PORTFOLIO = {
    "stage": 1,  # 1: SK스퀘어 보유기, 2: 달러 환전 후 미국 PW-RSI 실전 운용기
    "ticker": "402340.KS",
    "name": "SK스퀘어",
    "shares": 72,
    "avg_cost": 1_090_000.0,
    "target_asset_krw": 100_000_000.0,
    "cash_need_krw": 10_480_000.0,
    "hard_support_floor": 780_000.0,
    "case_b_fair_low": 869_000.0,
    "case_b_fair_high": 1_002_000.0,
    "case_c_fair": 1_419_000.0,
    "tp1_price": 2_180_000.0,
    "smh_target_weight": 0.70,
    "xlv_target_weight": 0.30,
    "smh_current_weight": 0.70,
    "contrarian_tilt_weight": 0.80,
    # 2단계 진입 시 추적할 미국 알파 보유 포지션 예시/슬롯
    "stage2_active_pos": None,
}

PORTFOLIO_CONFIG_PATH = os.path.join(BASE_DIR, "portfolio_config.json")


def load_portfolio_config() -> dict:
    """Loads dynamic user portfolio configuration from portfolio_config.json if available."""
    cfg = dict(MY_PORTFOLIO)
    if os.path.exists(PORTFOLIO_CONFIG_PATH):
        try:
            with open(PORTFOLIO_CONFIG_PATH, "r", encoding="utf-8") as f:
                data = json.load(f)
            kr = data.get("kr_core", {})
            etf = data.get("etf_barbell", {})
            cfg["stage"] = data.get("stage", cfg["stage"])
            cfg["shares"] = kr.get("shares", cfg["shares"])
            cfg["avg_cost"] = kr.get("avg_cost_krw", cfg["avg_cost"])
            cfg["cash_need_krw"] = kr.get("cash_need_krw", cfg["cash_need_krw"])
            cfg["smh_target_weight"] = etf.get("smh_target_weight", cfg["smh_target_weight"])
            cfg["xlv_target_weight"] = etf.get("xlv_target_weight", cfg["xlv_target_weight"])
            cfg["smh_current_weight"] = etf.get("smh_current_weight", cfg["smh_current_weight"])
            cfg["contrarian_tilt_weight"] = etf.get("contrarian_tilt_weight", cfg["contrarian_tilt_weight"])
            cfg["us_alpha_positions"] = data.get("us_alpha_positions", [])
            if cfg["us_alpha_positions"]:
                cfg["stage2_active_pos"] = cfg["us_alpha_positions"][0]
        except Exception:
            pass
    return cfg


# 2. 미국 전용(US-Only) 동적 스캔 유니버스 (한국 주식 100% 배제 -> T+3 결제시차 0일 & 양도세 22% 손익통산 100%)
US_UNIVERSE_META = {
    "CELH": {
        "name": "셀시우스 홀딩스",
        "sector": "Consumer Growth",
        "growth_tier": "A+",
        "tag": "북미 점유율 15%·펩시 재고조정 종료·해외 확장",
        "washout_why": "펩시코(PepsiCo) 북미 유통망 재고 조정 우려로 밸류에이션 과매도 세척 완료",
        "turnaround_catalyst": "2026~2027 매출 +36%·영업이익 +81% 컨센서스 및 영국/호주/프랑스 글로벌 매출 가속",
        "hist_analog": "2025.02 PW-RSI 우측 시동 포착 당시 144거래일 보유 +91.0% 수익 달성 종목",
    },
    "NFLX": {
        "name": "넷플릭스",
        "sector": "Global Platform",
        "growth_tier": "A+",
        "tag": "광고 요금제 MAU 폭발·스포츠 라이브·영업레버리지",
        "washout_why": "밸류에이션 멀티플 숨고르기 및 단기 가이던스 보수성으로 과매도 조정",
        "turnaround_catalyst": "광고 요금제 ARPU 상승 및 라이브 이벤트(NFL/WWE) 광고 단가 인상으로 FCF 마진 레벨업",
        "hist_analog": "2005년(+100.8%), 2012~2014년(+476.5%) PW-RSI 역대 최고 멀티배거 족보 보유",
    },
    "LULU": {
        "name": "룰루레몬",
        "sector": "Global Consumer",
        "growth_tier": "B+",
        "tag": "중국 본토 매출 +30% 고성장·고마진·자사주 매입",
        "washout_why": "북미 소비 둔화 우려 및 신제품 라인업 교체기 노이즈로 역사적 최저 PER 구간까지 압축",
        "turnaround_catalyst": "중국 시장 매장 확대(+30% YoY) 및 남성복/액세서리 비중 확대로 영업이익률 22%+ 방어",
        "hist_analog": "2014.11 PW-RSI 우측 시동 진입 후 93거래일 만에 +39.3% 중기 추세 수익 기록",
    },
    "FSLR": {
        "name": "퍼스트솔라",
        "sector": "Clean Energy / AI Power",
        "growth_tier": "A",
        "tag": "미국 AI 데이터센터 태양광 수주잔고 80GW·IRA 수혜",
        "washout_why": "금리 변동성 및 정책 불확실성 노이즈로 밸류에이션 멀티플 압축",
        "turnaround_catalyst": "미국 빅테크 AI 데이터센터 전력 PPA 장기계약 독식 및 중국산 태양광 관세 장벽 반사이익",
        "hist_analog": "2019.01 PW-RSI 우측 시동 포착 후 149거래일 보유 +31.8% 추세 수익 달성",
    },
    "ENPH": {
        "name": "엔페이즈 에너지",
        "sector": "Clean Tech / Power",
        "growth_tier": "A",
        "tag": "IQ9 마이크로인버터·AI 데이터센터 800V DC 진출",
        "washout_why": "유럽/캘리포니아 주택용 태양광 채널 재고 조정으로 밸류에이션 과매도 조정",
        "turnaround_catalyst": "차세대 GaN 기반 IQ9 출시 및 AI 데이터센터 전력변환(800V DC) 신시장 진출로 영업익 +200% 턴어라운드",
        "hist_analog": "채널 재고 소진 완료 후 20일·60일선 동시 돌파 시 가장 탄력적인 베타를 보이는 대표 종목",
    },
    "MBLY": {
        "name": "모빌아이",
        "sector": "Autonomous AI",
        "growth_tier": "A+",
        "tag": "EyeQ6 양산·SuperVision 수주·영업익 흑자대전환",
        "washout_why": "Tier-1 고객사 EyeQ 칩 재고 소진 이슈로 과매도 하락 후 바닥 다지기",
        "turnaround_catalyst": "재고 정상화 완료 + 폭스바겐/글로벌 OEM SuperVision·Chauffeur 양산으로 매출 +37% 반등",
        "hist_analog": "거래량 워시아웃(1.46x) 출현 완료, 20일선/60일선 순차 돌파 대기 중인 핵심 후보",
    },
    "UPST": {"name": "업스타트 홀딩스", "sector": "AI Fintech", "growth_tier": "A+", "tag": "금리인하 AI 대출 승인율 점프·매출+61% 흑자전환", "washout_why": "고금리 장기화 우려로 고점 대비 -58% 조정", "turnaround_catalyst": "연준 금리 인하 사이클 + 기관 자금 파트너십 확대로 대출 취급고 급증", "hist_analog": "금리 안정기 20·60일선 돌파 시 단기 2배 폭발력을 가진 고베타 AI 핀테크"},
    "APP": {"name": "앱러빈(AppLovin)", "sector": "AI AdTech", "growth_tier": "A+", "tag": "AXON 2.0 AI 광고엔진 매출+35%·OPM 50%+", "washout_why": "단기 급등 후 차익실현 매물로 -64% 조정", "turnaround_catalyst": "이커머스 웹 광고 확장 및 AXON AI 타겟팅 효율 고도화", "hist_analog": "고마진 AI 소프트웨어 대장주"},
    "FLNC": {"name": "플루언스 에너지", "sector": "AI Grid BESS", "growth_tier": "A", "tag": "AI 데이터센터 BESS 수주잔고 $4.5B·흑자전환", "washout_why": "프로젝트 매출 인식 시점 이연으로 단기 조정", "turnaround_catalyst": "북미 AI 전력망 배터리 저장장치(BESS) 수주 폭발", "hist_analog": "전력망 병목 해결 핵심 수혜주"},
    "UBER": {"name": "우버 테크놀로지", "sector": "Mobility Platform", "growth_tier": "A", "tag": "로보택시 애그리게이터 해자·FCF 연+40% 성장", "washout_why": "자율주행 단독 경쟁 우려 과대반영으로 조정", "turnaround_catalyst": "웨이모(Waymo)·위라이드 등 글로벌 자율주행 플릿 독점 파트너십 확대 및 대규모 자사주 매입", "hist_analog": "대형 플랫폼 중 가장 견고한 잉여현금흐름(FCF) 성장주"},
    "NVDA": {"name": "엔비디아", "sector": "AI Semi", "growth_tier": "A+", "tag": "블랙웰/루빈 AI 가속기 독점", "washout_why": "단기 AI 설비투자 호흡조절 우려", "turnaround_catalyst": "하이퍼스케일러 차세대 AI 클러스터 증설", "hist_analog": "2010.09 PW-RSI +98.4%"},
    "AMD": {"name": "AMD", "sector": "AI Semi", "growth_tier": "A+", "tag": "MI350/MI400 AI 가속기 및 서버 CPU 점유율 확대", "washout_why": "AI GPU 점유율 격차 우려로 밸류 압축", "turnaround_catalyst": "엔터프라이즈 AI 추론 칩 채택 가속", "hist_analog": "2011.12 PW-RSI +35.9%"},
    "MU": {"name": "마이크론", "sector": "AI Memory", "growth_tier": "A+", "tag": "HBM3E/HBM4 및 데이터센터 D램 이익 성장", "washout_why": "중국 CXMT 범용 DDR5 추격 우려로 조정", "turnaround_catalyst": "미국 빅테크향 HBM 완판 및 고부가 eSSD 비중 확대", "hist_analog": "2016.05 PW-RSI +244.0%"},
    "AVGO": {"name": "브로드컴", "sector": "AI Semi", "growth_tier": "A+", "tag": "빅테크 커스텀 AI ASIC(XPU) 및 네트워킹 독점", "washout_why": "단기 멀티플 조정", "turnaround_catalyst": "구글·메타·바이트댄스 맞춤형 AI 칩 양산 확대", "hist_analog": "AI 인프라 핵심 벨웨더"},
    "MRVL": {"name": "마벨 테크놀로지", "sector": "AI Semi", "growth_tier": "A", "tag": "클라우드 광통신 DSP 및 커스텀 AI 칩 성장", "washout_why": "레거시 통신장비 재고 조정", "turnaround_catalyst": "AI 데이터센터 800G/1.6T 광인터커넥트 수요 폭발", "hist_analog": "AI 네트워킹 턴어라운드"},
    "AMAT": {"name": "어플라이드 머티어리얼즈", "sector": "Semi Equip", "growth_tier": "A", "tag": "HBM 패키징·GAA 전공정 장비 수혜", "washout_why": "중국 수출 통제 우려", "turnaround_catalyst": "선단 파운드리 GAA 및 HBM 어드밴스드 패키징 매출 급증", "hist_analog": "반도체 장비 대장"},
    "LRCX": {"name": "램리서치", "sector": "Semi Equip", "growth_tier": "A", "tag": "3D 낸드·HBM TSV 식각 장비 턴어라운드", "washout_why": "메모리 설비투자 지연 우려", "turnaround_catalyst": "HBM4 TSV 식각 및 낸드 단수 고도화 교체 수요", "hist_analog": "식각 장비 독점"},
    "KLAC": {"name": "KLA", "sector": "Semi Equip", "growth_tier": "A", "tag": "첨단 공정 수율 계측/검사 장비 독점", "washout_why": "반도체 섹터 동반 조정", "turnaround_catalyst": "2나노 및 HBM 적층 공정 복잡도 증가로 계측 장비 필수화", "hist_analog": "2015.10 PW-RSI +31.3%"},
    "ON": {"name": "온세미컨덕터", "sector": "Power Semi", "growth_tier": "A", "tag": "전기차·AI 서버 전력반도체(SiC) 턴어라운드", "washout_why": "글로벌 전기차 재고 조정", "turnaround_catalyst": "산업용·자동차 재고 바닥 통과 및 AI 데이터센터 전력칩 공급", "hist_analog": "전력반도체 핵심주"},
    "MPWR": {"name": "모놀리식 파워", "sector": "Power Semi", "growth_tier": "A+", "tag": "AI 서버 전력관리칩(PMIC) 고성장", "washout_why": "고객사 점유율 배분 루머로 과매도", "turnaround_catalyst": "차세대 AI 가속기 및 자동차용 전력모듈 채택 확대", "hist_analog": "고수익 아날로그 반도체"},
    "ARM": {"name": "ARM 홀딩스", "sector": "AI Semi IP", "growth_tier": "A+", "tag": "v9 아키텍처 로열티율 2배 상승·데이터센터 침투", "washout_why": "고밸류 멀티플 압축", "turnaround_catalyst": "AWS Graviton·NVIDIA Grace 등 AI 서버용 ARM CPU 점유율 급증", "hist_analog": "반도체 IP 독점"},
    "TSM": {"name": "TSMC", "sector": "AI Foundry", "growth_tier": "A+", "tag": "AI 칩 파운드리 및 CoWoS 패키징 글로벌 독점", "washout_why": "지정학 및 단기 차익실현", "turnaround_catalyst": "3Q 역대 최대 순이익 경신 및 2나노/CoWoS 증설 가속", "hist_analog": "글로벌 AI 파운드리 절대 강자"},
    "ASML": {"name": "ASML", "sector": "Semi Equip", "growth_tier": "A", "tag": "High-NA EUV 독점 및 2027 팹 투자 수혜", "washout_why": "중국 매출 비중 정상화 및 고객사 수주 이연", "turnaround_catalyst": "TSMC·인텔·하이닉스 2027 선단 공정용 EUV 출하 재개", "hist_analog": "EUV 리소그래피 독점"},
    "META": {"name": "메타 플랫폼스", "sector": "Big Tech", "growth_tier": "A+", "tag": "AI 광고 추천 고도화 및 영업이익 고성장", "washout_why": "AI CapEx 증가 우려", "turnaround_catalyst": "Llama 기반 광고 전환율 상승", "hist_analog": "빅테크 핵심주"},
    "AMZN": {"name": "아마존", "sector": "Big Tech", "growth_tier": "A+", "tag": "AWS AI 클라우드 가속 및 북미 물류 마진 개선", "washout_why": "클라우드 CapEx 부담", "turnaround_catalyst": "AWS 생성형 AI 워크로드 매출 폭발", "hist_analog": "클라우드/커머스 1위"},
    "TSLA": {"name": "테슬라", "sector": "Autonomous / ESS", "growth_tier": "A", "tag": "FSD 자율주행·로보택시 및 메가팩(ESS) 이익 급증", "washout_why": "전기차 마진 압축", "turnaround_catalyst": "메가팩 에너지 저장장치 고마진 성장 및 로보택시 상용화", "hist_analog": "고베타 모멘텀 대장"},
    "PLTR": {"name": "팔란티어", "sector": "AI Software", "growth_tier": "A+", "tag": "AIP 엔터프라이즈·국방 AI 소프트웨어 폭발적 성장", "washout_why": "단기 밸류에이션 부담", "turnaround_catalyst": "미국 상업용 AIP 부트캠프 전환율 폭발", "hist_analog": "AI 소프트웨어 대장"},
    "COIN": {"name": "코인베이스", "sector": "FinTech / Crypto", "growth_tier": "A", "tag": "크립토 현물 ETF 수탁 및 스테이블코인/파생 레버리지", "washout_why": "가상자산 단기 박스권 조정으로 고점 대비 -53% 하락", "turnaround_catalyst": "글로벌 유동성 확대기 거래대금 폭발 및 Base 체인 수수료 성장", "hist_analog": "고베타 턴어라운드"},
    "SHOP": {"name": "쇼피파이", "sector": "E-Commerce", "growth_tier": "A+", "tag": "글로벌 이커머스 GMV 성장 및 FCF 마진 레벨업", "washout_why": "소비 둔화 우려", "turnaround_catalyst": "엔터프라이즈 화주 영입 및 물류 매각 후 FCF 마진 급증", "hist_analog": "이커머스 솔루션 1위"},
    "SNOW": {"name": "스노우플레이크", "sector": "Cloud Data", "growth_tier": "A", "tag": "엔터프라이즈 데이터 클라우드·AI 신제품 채택", "washout_why": "클라우드 소비 최적화 우려", "turnaround_catalyst": "Cortex AI 및 Iceberg 테이블 채택 가속", "hist_analog": "2024.11 PW-RSI +30.4%"},
    "CRWD": {"name": "크라우드스트라이크", "sector": "Cybersecurity", "growth_tier": "A+", "tag": "사이버보안 플랫폼 통합 및 ARR 고성장", "washout_why": "일시적 IT 업데이트 장애 여파 해소", "turnaround_catalyst": "Falcon Flex 모듈 채택 확대로 순매출유지율(DBNRR) 회복", "hist_analog": "사이버보안 1위"},
    "PANW": {"name": "팔로알토 네트웍스", "sector": "Cybersecurity", "growth_tier": "A", "tag": "차세대 보안 플랫폼화 및 고마진 성장", "washout_why": "플랫폼화 전환기 단기 빌링 노이즈", "turnaround_catalyst": "대형 엔터프라이즈 보안 통합 계약 급증", "hist_analog": "보안 플랫폼 대장"},
    "NET": {"name": "클라우드플레어", "sector": "Edge AI / Cloud", "growth_tier": "A+", "tag": "엣지 AI 추론(Workers AI) 및 제로트러스트 고성장", "washout_why": "고멀티플 성장주 조정", "turnaround_catalyst": "글로벌 엣지 네트워크 기반 AI 추론 수요 확대", "hist_analog": "엣지 클라우드 리더"},
    "DDOG": {"name": "데이터독", "sector": "Cloud Monitoring", "growth_tier": "A+", "tag": "클라우드·AI 인프라 모니터링 수요 가속", "washout_why": "클라우드 지출 효율화 우려", "turnaround_catalyst": "AI 네이티브 고객사 모니터링 ARR 비중 급증", "hist_analog": "2023.05 PW-RSI +15.0%"},
    "PINS": {"name": "핀터레스트", "sector": "Social Commerce", "growth_tier": "A", "tag": "아마존/구글 제휴 쇼핑 광고 및 ARPU 상승", "washout_why": "광고주 단기 예산 변동", "turnaround_catalyst": "퍼포먼스 광고 솔루션(Performance+) 도입으로 전환율 급증", "hist_analog": "소셜 커머스 턴어라운드"},
    "SPOT": {"name": "스포티파이", "sector": "Audio Platform", "growth_tier": "A+", "tag": "구독료 인상 및 비용 통제로 영업이익/FCF 폭증", "washout_why": "단기 차익실현", "turnaround_catalyst": "유료 구독자 증가 및 총마진율 30%+ 돌파", "hist_analog": "플랫폼 흑자전환 모범사례"},
    "DUOL": {"name": "듀오링고", "sector": "AI EdTech", "growth_tier": "A+", "tag": "Duolingo Max(AI) 유료전환율 및 FCF 급증", "washout_why": "단기 멀티플 조정", "turnaround_catalyst": "AI 영상통화(Lily) 탑재 Max 티어 구독 확산", "hist_analog": "2026.05 PW-RSI +18.6%"},
    "HOOD": {"name": "로빈후드", "sector": "FinTech", "growth_tier": "A", "tag": "골드 구독자·옵션/크립토 점유율 확대 흑자 폭발", "washout_why": "단기 금리/거래대금 노이즈", "turnaround_catalyst": "연금 매칭·골드 유료구독자 200만 돌파 및 유럽 확장", "hist_analog": "핀테크 영업레버리지"},
    "AFRM": {"name": "어펌 홀딩스", "sector": "FinTech BNPL", "growth_tier": "A", "tag": "금리 인하 조달비용 감소 및 애플페이 탑재 GMV 급증", "washout_why": "소비자 연체율 우려(실제 연체율은 안정적)", "turnaround_catalyst": "기준금리 인하에 따른 자금조달 마진 확대 및 Apple Pay 통합", "hist_analog": "금리 인하 최대 수혜"},
    "SOFI": {"name": "소파이 테크놀로지", "sector": "FinTech Bank", "growth_tier": "A", "tag": "금융서비스 부문 흑자 폭증 및 GAAP 순이익 고성장", "washout_why": "보수적 대출 가이던스 및 전환사채 차익거래 매물(-56%)", "turnaround_catalyst": "비이자 수수료(Loan Platform Business) 매출 폭발 및 예금 기반 확대", "hist_analog": "거래량 1.89x 폭발, 20일선 회복 대기"},
    "LLY": {"name": "일라이 릴리", "sector": "Biopharma", "growth_tier": "A+", "tag": "비만치료제(젭바운드/마운자로) 및 경구용 오포글리프론 독점", "washout_why": "단기 밸류 숨고르기", "turnaround_catalyst": "글로벌 비만/대사질환 적응증 확장 및 생산설비 증설 완료", "hist_analog": "XLV 핵심 성장 엔진"},
    "VRTX": {"name": "버텍스 파마슈티컬", "sector": "Biotech", "growth_tier": "A", "tag": "비마약성 진통제(Suzetrigine) 신약 및 낭포성섬유증 독점", "washout_why": "임상 파이프라인 단기 노이즈", "turnaround_catalyst": "FDA 승인 비마약성 급성 통증 치료제 상업화 본격화", "hist_analog": "바이오 캐시카우"},
    "REGN": {"name": "리제네론", "sector": "Biotech", "growth_tier": "A", "tag": "듀피젠트 COPD 적응증 확대 및 항암 파이프라인", "washout_why": "아일리아 바이오시밀러 경쟁 우려", "turnaround_catalyst": "듀피젠트 매출 고성장 및 고용량 아일리아 전환 방어", "hist_analog": "2025.10 PW-RSI 포착"},
    "DECK": {"name": "데커스 아웃도어", "sector": "Consumer", "growth_tier": "A", "tag": "HOKA 러닝화 및 UGG 글로벌 고성장", "washout_why": "소비재 섹터 동반 조정", "turnaround_catalyst": "HOKA 글로벌 매장 침투율 확대", "hist_analog": "나이키 점유율 흡수 대장"},
    "GE": {"name": "GE 에어로스페이스", "sector": "Aerospace", "growth_tier": "A", "tag": "항공기 엔진 애프터마켓(MRO) 고마진 슈퍼사이클", "washout_why": "단기 차익실현", "turnaround_catalyst": "글로벌 여객기 운항 증가 및 LEAP 엔진 정비 마진 확대", "hist_analog": "2020.10 PW-RSI +74.8%"},
    # Value Traps (Automatically Flagged)
    "INTC": {"name": "인텔", "sector": "Legacy Semi", "growth_tier": "TRAP", "tag": "[밸류트랩] 파운드리 대규모 적자 및 서버 CPU 점유율 상실", "washout_why": "구조적 경쟁력 약화", "turnaround_catalyst": "역성장", "hist_analog": "매수 배제"},
    "PARA": {"name": "파라마운트", "sector": "Legacy Media", "growth_tier": "TRAP", "tag": "[밸류트랩] 레거시 케이블TV 구조적 사양화", "washout_why": "코드커팅 가속", "turnaround_catalyst": "역성장", "hist_analog": "매수 배제"},
    "WBD": {"name": "워너브라더스", "sector": "Legacy Media", "growth_tier": "TRAP", "tag": "[밸류트랩] 막대한 부채 및 레거시 미디어 역성장", "washout_why": "선형 TV 광고 감소", "turnaround_catalyst": "역성장", "hist_analog": "매수 배제"},
    "PFE": {"name": "화이자", "sector": "Legacy Pharma", "growth_tier": "TRAP", "tag": "[밸류트랩] 특허절벽 및 코로나 매출 공백 장기화", "washout_why": "주요 블록버스터 특허 만료", "turnaround_catalyst": "역성장", "hist_analog": "매수 배제"},
    "BA": {"name": "보잉", "sector": "Aerospace", "growth_tier": "TRAP", "tag": "[밸류트랩] 품질 이슈·파업 및 대규모 유상증자 희석", "washout_why": "재무구조 악화", "turnaround_catalyst": "역성장", "hist_analog": "매수 배제"},
    "NKE": {"name": "나이키", "sector": "Apparel", "growth_tier": "TRAP", "tag": "[밸류트랩] HOKA/On에 러닝화 점유율 잠식 및 매출 둔화", "washout_why": "브랜드 모멘텀 약화", "turnaround_catalyst": "역성장", "hist_analog": "매수 배제"},
    "ALB": {"name": "앨버말", "sector": "Lithium", "growth_tier": "WAIT_CYCLE", "tag": "[사이클대기] 리튬 스팟 판가 추세 반등 전까지 데드머니 위험", "washout_why": "리튬 공급과잉", "turnaround_catalyst": "판가 회복 대기", "hist_analog": "매수 배제"},
}


def fetch_ticker_df(ticker: str) -> tuple[str, pd.DataFrame | None]:
    """Fetches 2Y daily OHLCV with 2-tier Yahoo Finance US & local CSV fallback."""
    return fetch_primary_ticker_df(ticker)


def compute_basic_quote(df: pd.DataFrame) -> dict:
    c = df["Close"].astype(float)
    h = df["High"].astype(float)
    lo = df["Low"].astype(float)
    v = df["Volume"].astype(float)
    cur = float(c.iloc[-1])
    prev = float(c.iloc[-2]) if len(c) >= 2 else cur
    chg1d = (cur / prev - 1.0) * 100.0
    chg5d = (cur / float(c.iloc[-6]) - 1.0) * 100.0 if len(c) >= 6 else 0.0
    chg20d = (cur / float(c.iloc[-21]) - 1.0) * 100.0 if len(c) >= 21 else 0.0
    hi52 = float(h.tail(252).max())
    lo52 = float(lo.tail(252).min())
    dd52 = (cur / hi52 - 1.0) * 100.0
    prox52 = (cur / lo52 - 1.0) * 100.0
    ma20 = float(c.tail(20).mean())
    ma60 = float(c.tail(60).mean())
    ma200 = float(c.tail(200).mean())
    delta = c.diff()
    up = delta.clip(lower=0).ewm(com=13, adjust=True, min_periods=14).mean()
    dn = (-delta.clip(upper=0)).ewm(com=13, adjust=True, min_periods=14).mean()
    rsi14 = float((100.0 - 100.0 / (1.0 + up / (dn + 1e-9))).iloc[-1])
    vol20 = float(v.tail(20).mean()) + 1.0
    vol_ratio = float(v.iloc[-1] / vol20)
    return {
        "date": str(df["Date"].iloc[-1]),
        "close": cur,
        "high_today": float(h.iloc[-1]),
        "low_today": float(lo.iloc[-1]),
        "chg1d": chg1d,
        "chg5d": chg5d,
        "chg20d": chg20d,
        "hi52": hi52,
        "lo52": lo52,
        "dd52": dd52,
        "prox52": prox52,
        "ma20": ma20,
        "ma60": ma60,
        "ma200": ma200,
        "vs_ma20": (cur / ma20 - 1.0) * 100.0,
        "vs_ma60": (cur / ma60 - 1.0) * 100.0,
        "vs_ma200": (cur / ma200 - 1.0) * 100.0,
        "rsi14": rsi14,
        "vol_ratio": vol_ratio,
    }


def calc_pw_rsi_signal(ticker: str, df: pd.DataFrame, prev_scores: dict, _calc_prev_day: bool = True) -> dict:
    c = df["Close"].astype(float)
    h = df["High"].astype(float)
    lo = df["Low"].astype(float)
    v = df["Volume"].astype(float)

    cur = float(c.iloc[-1])
    prev = float(c.iloc[-2]) if len(c) >= 2 else cur
    chg1d = (cur / prev - 1.0) * 100.0
    dt = str(df["Date"].iloc[-1])
    lo52 = float(lo.tail(252).min())
    hi52 = float(h.tail(252).max())
    ma20_series = c.rolling(20).mean()
    ma20 = float(ma20_series.iloc[-1])
    ma20_prev5 = float(ma20_series.iloc[-6]) if len(ma20_series) >= 26 else ma20
    ma20_slope_pct = (ma20 / ma20_prev5 - 1.0) * 100.0 if ma20_prev5 > 0 else 0.0
    ma60 = float(c.tail(60).mean())
    ma200 = float(c.tail(200).mean())

    delta = c.diff()
    up = delta.clip(lower=0).ewm(com=13, adjust=True, min_periods=14).mean()
    dn = (-delta.clip(upper=0)).ewm(com=13, adjust=True, min_periods=14).mean()
    rsi14 = float((100.0 - 100.0 / (1.0 + up / (dn + 1e-9))).iloc[-1])

    vol20 = float(v.tail(20).mean()) + 1.0
    max_vol_10d = float(v.tail(10).max() / vol20)
    ret20d = (cur / float(c.iloc[-21]) - 1.0) * 100.0 if len(c) >= 21 else 0.0
    prox_low = (cur / lo52 - 1.0) * 100.0
    dd_high = (cur / hi52 - 1.0) * 100.0
    vs_ma20 = (cur / ma20 - 1.0) * 100.0
    vs_ma60 = (cur / ma60 - 1.0) * 100.0

    meta = US_UNIVERSE_META[ticker]
    tier = meta["growth_tier"]
    is_growth_qualified = tier in ("A+", "A", "B+")

    # Scoring (0 ~ 100 pts) — round each component to 0.1 so component sum == total_score exactly
    score_dd = round(min(25.0, max(0.0, (abs(min(0.0, dd_high)) - 25.0) * 0.7)) if dd_high <= -35.0 else 0.0, 1)
    if 10.0 <= prox_low <= 40.0:
        score_prox = 25.0
    elif 0.0 <= prox_low < 10.0:
        score_prox = 14.0
    elif 40.0 < prox_low <= 55.0:
        score_prox = 12.0
    else:
        score_prox = 0.0

    if cur > ma20 and cur > ma60 and ma20_slope_pct > 0:
        score_ma = 30.0
    elif cur > ma20 and cur > ma60:
        score_ma = 25.0
    elif cur >= ma20 * 0.995:
        score_ma = 20.0
    elif vs_ma20 >= -5.0:
        score_ma = 10.0
    else:
        score_ma = 3.0

    score_vol = round(min(10.0, max(0.0, (max_vol_10d - 1.0) * 10.0)), 1)
    score_growth = 10.0 if tier == "A+" else (8.0 if tier == "A" else (5.0 if tier == "B+" else -30.0))
    total_score = round(score_dd + score_prox + score_ma + score_vol + score_growth, 1)

    # 4 Exact Conditions (Restoring MA20_Slope > 0 from empirical backtest)
    c1_deep_dd = dd_high <= -38.0
    c2_off_low = 10.0 <= prox_low <= 40.0
    c3_price_ok = (cur > ma20) and (cur > ma60)
    c3_slope_ok = ma20_slope_pct > 0.0
    c3_above_mas = c3_price_ok and c3_slope_ok
    c4_vol_or_mom = (max_vol_10d >= 1.35) or (ret20d >= 8.0)

    if not is_growth_qualified:
        signal_stage = "TRAP_EXCLUDED"
    elif c1_deep_dd and c2_off_low and c3_above_mas and c4_vol_or_mom:
        signal_stage = "1_BUY_IGNITION"
    elif c1_deep_dd and (prox_low <= 42.0) and (cur >= ma20 * 0.98 or vs_ma20 >= -3.0):
        signal_stage = "2_READY_MA20"
    elif c1_deep_dd and (prox_low <= 30.0):
        signal_stage = "3_WATCH_BOTTOM"
    else:
        signal_stage = "4_OTHER"

    # Trigger dollar price needed for full 1_BUY_IGNITION
    trigger_price = max(ma20, ma60)
    pct_to_trigger = (trigger_price / cur - 1.0) * 100.0

    prev_info = prev_scores.get(ticker) if prev_scores else None
    if prev_info is None and _calc_prev_day and len(df) >= 31:
        try:
            prev_day_res = calc_pw_rsi_signal(ticker, df.iloc[:-1], {}, _calc_prev_day=False)
            prev_sc = prev_day_res["score"]
            prev_st = prev_day_res["signal_stage"]
        except Exception:
            prev_sc = total_score
            prev_st = signal_stage
    else:
        prev_info = prev_info or {}
        prev_sc = prev_info.get("score", total_score)
        prev_st = prev_info.get("stage", signal_stage)
    score_delta = round(total_score - prev_sc, 1)

    return {
        "ticker": ticker,
        "name": meta["name"],
        "sector": meta["sector"],
        "growth_tier": tier,
        "tag": meta["tag"],
        "washout_why": meta["washout_why"],
        "turnaround_catalyst": meta["turnaround_catalyst"],
        "hist_analog": meta["hist_analog"],
        "date": dt,
        "close": cur,
        "chg1d": chg1d,
        "lo52": lo52,
        "hi52": hi52,
        "prox_low": prox_low,
        "dd_high": dd_high,
        "ma20": ma20,
        "ma60": ma60,
        "ma200": ma200,
        "ma20_slope_pct": ma20_slope_pct,
        "vs_ma20": vs_ma20,
        "vs_ma60": vs_ma60,
        "rsi14": rsi14,
        "vol_surge": max_vol_10d,
        "ret20d": ret20d,
        "score": total_score,
        "score_dd": score_dd,
        "score_prox": score_prox,
        "score_ma": score_ma,
        "score_vol": score_vol,
        "score_growth": score_growth,
        "score_delta": score_delta,
        "prev_stage": prev_st,
        "signal_stage": signal_stage,
        "c1": c1_deep_dd,
        "c2": c2_off_low,
        "c3": c3_above_mas,
        "c3_price_ok": c3_price_ok,
        "c3_slope_ok": c3_slope_ok,
        "c4": c4_vol_or_mom,
        "trigger_price": trigger_price,
        "pct_to_trigger": pct_to_trigger,
        "stop_loss_price": round(cur * 0.91, 2),
        "tp1_price": round(cur * 2.00, 2),
    }


def fetch_rss_headlines(query: str, lang_params: str, max_items: int = 5) -> list[dict]:
    """Fetches primary US (en-US) or China/Greater China (zh-CN/zh-TW) RSS headlines."""
    items = []
    try:
        url = f"https://news.google.com/rss/search?q={requests.utils.quote(query)}&{lang_params}"
        r = requests.get(url, headers=HEADERS, verify=False, timeout=6)
        if r.status_code == 200:
            root = ET.fromstring(r.content)
            for it in root.findall(".//item")[:max_items]:
                title = (it.find("title").text or "").strip()
                pub = (it.find("pubDate").text or "")[:16]
                src_el = it.find("source")
                src = src_el.text.strip() if (src_el is not None and src_el.text) else "Global Wire"
                if " - " in title and src == "Global Wire":
                    parts = title.rsplit(" - ", 1)
                    title, src = parts[0].strip(), parts[1].strip()
                items.append({"title": title, "source": src, "pub": pub})
    except Exception:
        pass
    return items


def build_us_cn_curated_intelligence(live_rss: dict = None) -> dict:
    """
    Combines live-fetched US (en-US) & China (zh-CN/zh-TW) RSS headlines with
    rigorous Korean translation & portfolio impact commentary (0% South Korean domestic media).
    """
    live_rss = live_rss or {}
    base_news = build_primary_news_feed()
    sk_news = base_news["sk_news"]
    etf_news = base_news["etf_news"]

    # Provide backward-compatible field aliases alongside standard schema
    for item in sk_news + etf_news:
        item.setdefault("origin", item.get("origin_badge", ""))
        item.setdefault("badge", item.get("category_badge", ""))
        item.setdefault("badge_cls", item.get("badge_class", ""))
        item.setdefault("orig_title", item.get("orig_headline", ""))

    # Append fresh live US RSS headline if available and clean
    if live_rss.get("us_semi_mem"):
        top_us = live_rss["us_semi_mem"][0]
        title_with_src = f"{top_us['title']} ({top_us['source']})"
        if not find_blacklisted_media(title_with_src):
            sk_news[1]["orig_headline"] = title_with_src
            sk_news[1]["orig_title"] = title_with_src

    res = {
        "sk_news": sk_news,
        "etf_news": etf_news,
        "page1_news": sk_news,
        "page2_news": etf_news,
    }
    assert_zero_korean_media(res)
    return res


def generate_morning_briefing(
    target_date: Optional[str] = None,
    force_offline: bool = False,
    open_pdf: bool = False,
) -> Tuple[int, str]:
    """
    Complete end-to-end Daily 08:10 AM KST Morning Alpha Briefing PDF pipeline:
      1. Ingests quotes & curated intelligence (100% US & CN/TW primary sources)
      2. Computes quantitative metrics for Page 1, Page 2, Page 3
      3. Scans 100% US-only PW-RSI universe (actionable Top 5)
      4. Renders strict 3-page A4 HTML report
      5. Compiles print-ready vector PDF via headless Microsoft Edge/Chrome
      6. Verifies PDF with PyMuPDF (len(doc) == 3, size > 50KB, y1 <= 838.0 pt)
      7. Copies to Latest_Morning_Alpha_Briefing.pdf and opens on screen if requested
    """
    print("=== [08:10 KST Morning Alpha Briefing 3-Page PDF Generation Engine] ===")

    # 1. Fetch Market Snapshot & News (100% US & CN/TW Primary Feeds)
    snapshot = fetch_market_snapshot(date=target_date, force_offline=force_offline)
    ref_date = snapshot.get("date") or datetime.now().strftime("%Y-%m-%d")
    print(f"[Engine] Market Snapshot Loaded: Date = {ref_date}, Proxies = {len(snapshot['quotes'])}")

    # 2. Compute Calculations for Page 1, Page 2, Page 3
    # Scan US Alpha Universe for PW-RSI Candidates
    print("[Engine] Scanning 100% US-Only PW-RSI Universe...")
    def scan_one(tk):
        try:
            t, df = fetch_primary_ticker_df(tk, force_offline=force_offline)
            if df is not None and len(df) >= 30:
                return calc_pw_rsi_signal(tk, df, {})
        except Exception:
            pass
        return None

    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as ex:
        scan_results = [r for r in ex.map(scan_one, US_UNIVERSE_META.keys()) if r is not None]

    # Filter Actionable (1_BUY_IGNITION and 2_READY_MA20 only, strictly US-only)
    actionable = [
        c for c in scan_results
        if c["signal_stage"] in ("1_BUY_IGNITION", "2_READY_MA20")
        and not c["ticker"].endswith((".KS", ".KQ"))
    ]
    actionable.sort(key=lambda x: (-x["score"], -x["vol_surge"], x["ticker"]))
    buy_count = sum(1 for c in scan_results if c["signal_stage"] == "1_BUY_IGNITION")
    ready_count = sum(1 for c in scan_results if c["signal_stage"] == "2_READY_MA20")
    print(f"[Engine] US Candidates Scanned: Total = {len(scan_results)}, Actionable = {len(actionable)} (Buy: {buy_count}, Ready: {ready_count})")

    # Barbell & ETF calculations
    smh_q = snapshot["quotes"].get("SMH", {})
    pf_cfg = load_portfolio_config()
    calc_data = {
        "pwrsi_buy_count": buy_count,
        "pwrsi_ready_count": ready_count,
        "actionable_top5": actionable[:5],
        "smh_weight": float(pf_cfg.get("smh_current_weight", 0.70)),
        "smh_target_weight": float(pf_cfg.get("smh_target_weight", 0.70)),
        "xlv_target_weight": float(pf_cfg.get("xlv_target_weight", 0.30)),
        "smh_dd52": smh_q.get("dd52", -6.8),
        "portfolio_config": pf_cfg,
    }

    # 3. Render HTML for all 3 Pages
    print("[Engine] Rendering Page 1, Page 2, Page 3 HTML...")
    p1_html = render_page1_html(snapshot, calc_data)
    p2_html = render_page2_html(snapshot, calc_data)
    p3_html = render_page3_html(snapshot, calc_data)
    full_html = build_full_html_report(p1_html, p2_html, p3_html, report_date=ref_date)

    # 4. Save HTML to daily_pdf
    html_filename = f"{ref_date}_Morning_Alpha_Briefing.html"
    html_path = os.path.join(OUT_DIR, html_filename)
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(full_html)
    print(f"[Engine] HTML Saved: {html_filename}")

    # 5. Compile PDF via Headless Microsoft Edge/Chrome
    pdf_filename = f"{ref_date}_Morning_Alpha_Briefing.pdf"
    dated_pdf_path = os.path.join(OUT_DIR, pdf_filename)
    latest_pdf_path = os.path.join(OUT_DIR, "Latest_Morning_Alpha_Briefing.pdf")

    print("[Engine] Compiling Strict 3-Page A4 PDF via Headless Browser...")
    success = compile_html_to_pdf(html_path, dated_pdf_path)
    if not success or not os.path.exists(dated_pdf_path):
        print("[Engine] ERROR: PDF compilation failed.")
        return 1, "PDF compilation failed"

    # Copy to Latest_Morning_Alpha_Briefing.pdf
    try:
        shutil.copyfile(dated_pdf_path, latest_pdf_path)
    except Exception as e:
        print(f"[Engine] Warning: copy to Latest failed: {e}")

    # 6. Verify with PyMuPDF
    print("[Engine] Verifying PDF with PyMuPDF (len(doc) == 3, size > 50KB, y1 <= 838.0 pt)...")
    valid, msg = verify_pdf_with_pymupdf(latest_pdf_path)
    if not valid:
        print(f"[Engine] Verification ERROR: {msg}")
        return 1, msg
    print(f"[Engine] {msg}")

    # 7. Auto-Popup on Screen if requested
    if open_pdf:
        print(f"[Engine] Auto-Opening PDF on user desktop: {os.path.basename(dated_pdf_path)}")
        if sys.platform == "win32" and hasattr(os, "startfile"):
            try:
                os.startfile(dated_pdf_path)
            except Exception as e:
                print(f"[Engine] Could not open PDF via os.startfile: {e}")

    print("=== [SUCCESS: Morning Alpha Briefing PDF Ready] ===")
    return 0, dated_pdf_path


def main():
    parser = argparse.ArgumentParser(description="Daily 08:10 AM KST Morning Alpha Briefing PDF Engine")
    parser.add_argument("--open", action="store_true", help="Automatically open generated PDF on screen")
    parser.add_argument("--date", type=str, default=None, help="Target reference date (YYYY-MM-DD)")
    parser.add_argument("--offline", action="store_true", help="Force offline mode using local CSV caches")
    args = parser.parse_args()

    exit_code, out_msg = generate_morning_briefing(
        target_date=args.date,
        force_offline=args.offline,
        open_pdf=args.open,
    )
    sys.exit(exit_code)


if __name__ == "__main__":
    main()


