"""
[1년 2배(2x) 2단계 복리 릴레이 & 전 종목 동적 PW-RSI 자동 발굴 레이더]
실행 방법: python check_my_plan.py

핵심 기능:
1. [STEP 1] 보유 중인 SK스퀘어(402340.KS) 76주의 종가, 평가금액, 손익률, 200일선 지지 여부,
   RSI(14), 1단계 목표 구간(120만~132만 원) 도달률을 자동 진단합니다.
2. [STEP 2] 고정된 몇 개 종목만 보는 것이 아니라, 매 실행 시마다 한·미 핵심 유니버스 100개 종목 전체의
   최신 시세를 병렬(Multi-thread)로 실시간 업데이트하여:
   - (조건 1) 52주 고점 대비 -40% 이상 낙폭 (밸류에이션 압축)
   - (조건 2) 향후 1~2년 매출·영업이익 다이나믹 성장/흑자전환 모멘텀 (구조적 사양산업/밸류트랩 제외)
   - (조건 3) 바닥권 거래량 워시아웃(1.4x+) 및 52주 신저가 대비 +12%~+38% 반등
   - (조건 4) 20일선 & 60일선 동시 돌파 (우측 시동 PW-RSI)
   위 조건을 만족하는 종목을 매주 동적으로 새로 발굴·랭킹하여 브리핑합니다.
"""

import os
import sys
import concurrent.futures
from datetime import datetime
import urllib3
import requests
import pandas as pd
import numpy as np

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data_stocks")
os.makedirs(DATA_DIR, exist_ok=True)

# 1. 사용자 보유 포지션 설정 (72주 보유 - 생활자금 4주(~300만 원) 인출 반영)
MY_PORTFOLIO = {
    "stage": 1,
    "ticker": "402340.KS",
    "name": "SK스퀘어",
    "shares": 72,
    "avg_cost": 1_090_000.0,
    "target_asset_krw": 100_000_000.0,       # 총 자산 1억 원 목표
    "stage1_switch_zone_min": 1_389_000.0,   # 72주 * 1,389,000원 = 100,008,000원 (1억 원 돌파 기준가)
    "stage1_switch_zone_max": 1_420_000.0,   # Case C 적정가 상단 (72주 = 1억 224만 원)
    "tp1_price": 2_180_000.0,
    "hard_support_floor": 780_000.0,
}

# 2. 한·미 100대 동적 스캔 유니버스 및 1~2년 실적 성장성/밸류트랩 메타데이터
# (향후 1~2년 매출/영업이익 고성장·턴어라운드 적격 유니버스 vs 구조적 저성장/밸류트랩 구분)
UNIVERSE_META = {
    # Core Stage-2 ETF Portfolio (SMH 70% + XLV 30%)
    "SMH": {"name": "미국 반도체 ETF(VanEck)", "growth_tier": "CORE", "growth_desc": "글로벌 AI·반도체 대장주(NVDA·TSM·AVGO 등) 70% 메인 코어"},
    "XLV": {"name": "미국 헬스케어 ETF(SPDR)", "growth_tier": "CORE", "growth_desc": "미국 대표 헬스케어·비만치료제(LLY·UNH·ABBV 등) 30% 방어 코어"},
    # Watchlist & High-Conviction Turnaround Growth
    "CELH": {"name": "셀시우스 홀딩스", "growth_tier": "A+", "growth_desc": "매출+36%/OP+81% (펩시 재고조정 종료·글로벌 확장)"},
    "MBLY": {"name": "모빌아이", "growth_tier": "A+", "growth_desc": "매출+37%/영업익 흑자대전환 (EyeQ6·SuperVision 양산)"},
    "UPST": {"name": "업스타트 홀딩스", "growth_tier": "A+", "growth_desc": "매출+61%/흑자전환 (금리인하 AI 대출 레버리지)"},
    "APP": {"name": "앱러빈(AppLovin)", "growth_tier": "A+", "growth_desc": "AI 광고엔진 AXON 매출+35%+/OPM 50%+"},
    "ENPH": {"name": "엔페이즈 에너지", "growth_tier": "A", "growth_desc": "매출+49%/OP+200%+ (IQ9 인버터·유럽/미국 회복)"},
    "FLNC": {"name": "플루언스 에너지", "growth_tier": "A", "growth_desc": "AI 데이터센터 BESS 수주 $4.5B·흑자전환"},
    "UBER": {"name": "우버 테크놀로지", "growth_tier": "A", "growth_desc": "로보택시 플랫폼 해자·FCF 연 +40% 성장"},
    # US Semiconductors & AI Infrastructure
    "NVDA": {"name": "엔비디아", "growth_tier": "A+", "growth_desc": "블랙웰/루빈 AI 슈퍼사이클 독점"},
    "AMD": {"name": "AMD", "growth_tier": "A+", "growth_desc": "MI350 AI 가속기 및 서버 CPU 점유율 확대"},
    "MU": {"name": "마이크론", "growth_tier": "A+", "growth_desc": "HBM3E/HBM4 및 데이터센터 D램 이익 폭증"},
    "AVGO": {"name": "브로드컴", "growth_tier": "A+", "growth_desc": "맞춤형 AI ASIC(XPU) 및 네트워킹 독점"},
    "MRVL": {"name": "마벨 테크놀로지", "growth_tier": "A", "growth_desc": "클라우드 광통신 DSP 및 커스텀 AI 칩 성장"},
    "AMAT": {"name": "어플라이드 머티어리얼즈", "growth_tier": "A", "growth_desc": "HBM 패키징·GAA 전공정 장비 수혜"},
    "LRCX": {"name": "램리서치", "growth_tier": "A", "growth_desc": "3D 낸드·HBM 식각 장비 턴어라운드"},
    "KLAC": {"name": "KLA", "growth_tier": "A", "growth_desc": "첨단 공정 수율 계측 장비 독점"},
    "QCOM": {"name": "퀄컴", "growth_tier": "B+", "growth_desc": "온디바이스 AI 스냅드래곤 및 차량용 반도체"},
    "ON": {"name": "온세미컨덕터", "growth_tier": "A", "growth_desc": "전기차·전력반도체(SiC) 재고소진 후 턴어라운드"},
    "MPWR": {"name": "모놀리식 파워", "growth_tier": "A+", "growth_desc": "AI 서버 전력관리칩(PMIC) 고성장"},
    "SMCI": {"name": "슈퍼마이크로", "growth_tier": "B+", "growth_desc": "수랭식 AI 서버 매출 성장 (마진 변동성 유의)"},
    "ARM": {"name": "ARM 홀딩스", "growth_tier": "A+", "growth_desc": "v9 아키텍처 로열티율 2배 상승·데이터센터 침투"},
    "TSM": {"name": "TSMC", "growth_tier": "A+", "growth_desc": "AI 칩 파운드리 및 CoWoS 패키징 독점"},
    "ASML": {"name": "ASML", "growth_tier": "A", "growth_desc": "High-NA EUV 독점 및 2027 팹 투자 수혜"},
    # US High-Beta Growth / Software / Platform
    "META": {"name": "메타 플랫폼스", "growth_tier": "A+", "growth_desc": "AI 광고 추천 고도화 및 영업이익 고성장"},
    "NFLX": {"name": "넷플릭스", "growth_tier": "A+", "growth_desc": "광고 요금제 및 글로벌 가입자 영업레버리지"},
    "AMZN": {"name": "아마존", "growth_tier": "A+", "growth_desc": "AWS AI 클라우드 가속 및 북미 물류 마진 개선"},
    "TSLA": {"name": "테슬라", "growth_tier": "A", "growth_desc": "FSD 자율주행·로보택시 및 메가팩(ESS) 이익 급증"},
    "PLTR": {"name": "팔란티어", "growth_tier": "A+", "growth_desc": "AIP 엔터프라이즈·국방 AI 소프트웨어 폭발적 성장"},
    "CVNA": {"name": "카바나", "growth_tier": "A", "growth_desc": "대당 매출총이익(GPU) 구조적 혁신 및 흑자 확대"},
    "COIN": {"name": "코인베이스", "growth_tier": "A", "growth_desc": "크립토 거래량 및 스테이블코인/파생 수익 레버리지"},
    "SHOP": {"name": "쇼피파이", "growth_tier": "A+", "growth_desc": "글로벌 이커머스 GMV 성장 및 FCF 마진 레벨업"},
    "PYPL": {"name": "페이팔", "growth_tier": "B+", "growth_desc": "Fastlane 체크아웃 개선 및 자사주 소각 턴어라운드"},
    "ROKU": {"name": "로쿠", "growth_tier": "B+", "growth_desc": "커넥티드 TV 광고 플랫폼 흑자 전환"},
    "SNOW": {"name": "스노우플레이크", "growth_tier": "A", "growth_desc": "엔터프라이즈 데이터 클라우드·AI 신제품 채택"},
    "CRWD": {"name": "크라우드스트라이크", "growth_tier": "A+", "growth_desc": "사이버보안 플랫폼 통합 및 ARR 고성장"},
    "PANW": {"name": "팔로알토 네트웍스", "growth_tier": "A", "growth_desc": "차세대 보안 플랫폼화 및 고마진 성장"},
    "NET": {"name": "클라우드플레어", "growth_tier": "A+", "growth_desc": "엣지 AI 추론(Workers AI) 및 제로트러스트 고성장"},
    "DDOG": {"name": "데이터독", "growth_tier": "A+", "growth_desc": "클라우드·AI 인프라 모니터링 수요 가속"},
    "ZS": {"name": "지스케일러", "growth_tier": "A", "growth_desc": "제로트러스트 클라우드 보안 영업이익 급증"},
    "MDB": {"name": "몽고DB", "growth_tier": "A", "growth_desc": "Atlas 클라우드 DB 소비 회복 및 AI 앱 수혜"},
    "U": {"name": "유니티 소프트웨어", "growth_tier": "B+", "growth_desc": "구조조정 완료 후 광고/엔진 턴어라운드"},
    "PINS": {"name": "핀터레스트", "growth_tier": "A", "growth_desc": "아마존 제휴 쇼핑 광고 및 ARPU 상승"},
    "SPOT": {"name": "스포티파이", "growth_tier": "A+", "growth_desc": "구독료 인상 및 오디오북·비용 통제로 영업이익 폭증"},
    "DUOL": {"name": "듀오링고", "growth_tier": "A+", "growth_desc": "Duolingo Max(AI) 유료전환율 및 FCF 급증"},
    "HOOD": {"name": "로빈후드", "growth_tier": "A", "growth_desc": "골드 구독자·옵션/크립토 점유율 확대 흑자 폭발"},
    "AFRM": {"name": "어펌 홀딩스", "growth_tier": "A", "growth_desc": "금리 인하 조달비용 감소 및 애플페이 탑재 GMV 급증"},
    "SOFI": {"name": "소파이 테크놀로지", "growth_tier": "A", "growth_desc": "금융서비스 부문 흑자 폭증 및 GAAP 순이익 고성장"},
    # US Clean Energy / Biotech / Consumer Growth
    "FSLR": {"name": "퍼스트솔라", "growth_tier": "A", "growth_desc": "미국 데이터센터 태양광 수주잔고 및 IRA 세액공제"},
    "SEDG": {"name": "솔라엣지", "growth_tier": "B+", "growth_desc": "유럽 인버터 재고 소진 후 적자 축소 턴어라운드"},
    "LLY": {"name": "일라이 릴리", "growth_tier": "A+", "growth_desc": "비만치료제(젭바운드/마운자로) 및 경구용 신약 독점"},
    "VRTX": {"name": "버텍스 파마슈티컬", "growth_tier": "A", "growth_desc": "비마약성 진통제 신약 및 낭포성섬유증 독점"},
    "REGN": {"name": "리제네론", "growth_tier": "A", "growth_desc": "듀피젠트 적응증 확대 및 항암 파이프라인"},
    "DECK": {"name": "데커스 아웃도어", "growth_tier": "A", "growth_desc": "HOKA 및 UGG 글로벌 고성장"},
    "CROX": {"name": "크록스", "growth_tier": "B+", "growth_desc": "초저평가 PER 및 잉여현금흐름 자사주 소각"},
    "LULU": {"name": "룰루레몬", "growth_tier": "B+", "growth_desc": "중국/글로벌 매장 확장 및 고마진 유지"},
    "GE": {"name": "GE 에어로스페이스", "growth_tier": "A", "growth_desc": "항공기 엔진 애프터마켓 고마진 슈퍼사이클"},
    # KR Leading Turnaround & Super-Cycle Growth Universe
    "402340.KS": {"name": "SK스퀘어", "growth_tier": "A+", "growth_desc": "하이닉스 지분 21%+·솔리다임 흑자·NAV 할인율 축소"},
    "000660.KS": {"name": "SK하이닉스", "growth_tier": "A+", "growth_desc": "HBM4/SOCAM 독점, 영업이익 396~454조 전망"},
    "005930.KS": {"name": "삼성전자", "growth_tier": "A", "growth_desc": "메모리 판가 상승 및 HBM3E/HBM4 진입 턴어라운드"},
    "042700.KS": {"name": "한미반도체", "growth_tier": "A+", "growth_desc": "HBM TC본더 글로벌 독점 및 고마진 수주 확대"},
    "007660.KS": {"name": "이수페타시스", "growth_tier": "A+", "growth_desc": "AI 가속기용 초다층 MLB 기판 증설 및 이익 급증"},
    "267260.KS": {"name": "HD현대일렉트릭", "growth_tier": "A+", "growth_desc": "북미 AI 전력망 초고압 변압기 3년치 완판·OPM 20%+"},
    "003230.KS": {"name": "삼양식품", "growth_tier": "A+", "growth_desc": "불닭 글로벌 수출 및 밀양 2공장 증설 영업이익 급증"},
    "259960.KS": {"name": "크래프톤", "growth_tier": "A", "growth_desc": "배틀그라운드 역대 최고 매출 및 신작 파이프라인"},
    "034020.KS": {"name": "두산에너빌리티", "growth_tier": "A", "growth_desc": "체코 원전·미국 SMR 수주 및 가스터빈 이익 성장"},
    "012450.KS": {"name": "한화에어로스페이스", "growth_tier": "A+", "growth_desc": "K9·천무 글로벌 방산 수출로 영업이익 폭발"},
    "064350.KS": {"name": "현대로템", "growth_tier": "A+", "growth_desc": "K2 전차 폴란드/루마니아 추가 수출 이익 급증"},
    "329180.KS": {"name": "HD현대중공업", "growth_tier": "A", "growth_desc": "고가 LNG선 건조 비중 확대 및 특수선(MRO) 수혜"},
    "010140.KS": {"name": "삼성중공업", "growth_tier": "A", "growth_desc": "FLNG 독점 수주 및 고선가 물량 매출 인식 흑자 확대"},
    "196170.KQ": {"name": "알테오젠", "growth_tier": "A+", "growth_desc": "키트루다 SC 제형 변경 로열티 유입 본격화"},
    "207940.KS": {"name": "삼성바이오로직스", "growth_tier": "A+", "growth_desc": "5공장 가동 및 미 생물보안법 반사이익 수주 독식"},
    "068270.KS": {"name": "셀트리온", "growth_tier": "A", "growth_desc": "짐펜트라 미국 처방 확대 및 합병 원가율 개선"},
    "005380.KS": {"name": "현대차", "growth_tier": "A", "growth_desc": "하이브리드 고수익성 및 인도 IPO·자사주 소각 밸류업"},
    "000270.KS": {"name": "기아", "growth_tier": "A", "growth_desc": "글로벌 완성차 최고 영업이익률 및 주주환원 확대"},
    "035420.KS": {"name": "NAVER", "growth_tier": "B+", "growth_desc": "홈피드·클립 광고 회복 및 AI 커머스 수익화"},
    "035720.KS": {"name": "카카오", "growth_tier": "B", "growth_desc": "비핵심 계열사 정리 및 비용 효율화 턴어라운드"},
    "086520.KQ": {"name": "에코프로", "growth_tier": "B", "growth_desc": "전방 전기차 캐즘 통과 후 양극재 출하 회복 대기"},
    "247540.KQ": {"name": "에코프로비엠", "growth_tier": "B", "growth_desc": "유럽/북미 OEM 신차 출시 시 양극재 가동률 회복"},
    # Value Traps / Secular Headwinds (Flagged to avoid false 52W-low traps!)
    "INTC": {"name": "인텔", "growth_tier": "TRAP", "growth_desc": "[주의] 파운드리 대규모 적자 및 점유율 하락"},
    "PARA": {"name": "파라마운트", "growth_tier": "TRAP", "growth_desc": "[주의] 레거시 케이블TV 구조적 사양화"},
    "WBD": {"name": "워너브라더스", "growth_tier": "TRAP", "growth_desc": "[주의] 막대한 부채 및 레거시 미디어 역성장"},
    "PFE": {"name": "화이자", "growth_tier": "TRAP", "growth_desc": "[주의] 특허절벽 및 코로나 매출 공백 장기화"},
    "BA": {"name": "보잉", "growth_tier": "TRAP", "growth_desc": "[주의] 품질 이슈·파업 및 대규모 유상증자 희석"},
    "NKE": {"name": "나이키", "growth_tier": "TRAP", "growth_desc": "[주의] 러닝화 점유율 잠식 및 매출 역성장"},
    "ALB": {"name": "앨버말", "growth_tier": "WAIT_CYCLE", "growth_desc": "[주의] 리튬 판가 반등 전까지 데드머니 위험"},
}

HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}


def fetch_or_update_ticker(ticker: str) -> tuple[str, pd.DataFrame | None]:
    """Fetches latest 2Y daily data from Yahoo Finance (with local CSV fallback)."""
    safe_name = ticker.replace(".", "_")
    csv_path = os.path.join(DATA_DIR, f"{safe_name}.csv")
    try:
        url = f"https://query1.finance.yahoo.com/v8/finance/chart/{ticker}?range=2y&interval=1d"
        r = requests.get(url, headers=HEADERS, verify=False, timeout=8)
        if r.status_code == 200:
            res = r.json()["chart"]["result"][0]
            meta_info = res.get("meta", {})
            ts = res["timestamp"]
            q = res["indicators"]["quote"][0]
            closes = list(q["close"])
            highs = list(q["high"])
            lows = list(q["low"])
            if closes and closes[-1] is None and meta_info.get("regularMarketPrice") is not None:
                closes[-1] = meta_info.get("regularMarketPrice")
                highs[-1] = meta_info.get("regularMarketDayHigh") or closes[-1]
                lows[-1] = meta_info.get("regularMarketDayLow") or closes[-1]
            df = pd.DataFrame({
                "Date": [datetime.fromtimestamp(t).strftime("%Y-%m-%d") for t in ts],
                "Close": closes,
                "High": highs,
                "Low": lows,
                "Volume": q["volume"],
            }).dropna(subset=["Close"])
            df["High"] = df["High"].fillna(df["Close"])
            df["Low"] = df["Low"].fillna(df["Close"])
            df["Volume"] = df["Volume"].fillna(0)
            if len(df) >= 200:
                return ticker, df
    except Exception:
        pass

    # Fallback to local cached CSV if offline or rate-limited
    if os.path.exists(csv_path):
        try:
            df = pd.read_csv(csv_path).dropna(subset=["Close"])
            df["High"] = df["High"].fillna(df["Close"])
            df["Low"] = df["Low"].fillna(df["Close"])
            df["Volume"] = df["Volume"].fillna(0)
            if len(df) >= 200:
                return ticker, df.tail(504).reset_index(drop=True)
        except Exception:
            pass
    return ticker, None


def calc_stock_signal(ticker: str, df: pd.DataFrame) -> dict:
    c = df["Close"].astype(float)
    h = df["High"].astype(float)
    lo = df["Low"].astype(float)
    v = df["Volume"].astype(float)

    cur = float(c.iloc[-1])
    dt = str(df["Date"].iloc[-1])
    lo52 = float(lo.tail(252).min())
    hi52 = float(h.tail(252).max())
    ma20 = float(c.tail(20).mean())
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
    vs_ma200 = (cur / ma200 - 1.0) * 100.0

    meta = UNIVERSE_META.get(ticker, {"name": ticker, "growth_tier": "B", "growth_desc": "일반 섹터"})
    tier = meta["growth_tier"]
    is_growth_qualified = tier in ("A+", "A", "B+")

    # PW-RSI (Post-Washout Right-Side Ignition) Scoring (0 ~ 100 pts)
    # 1) Deep Drawdown Reset (Max 25 pts): DD <= -40%
    score_dd = min(25.0, max(0.0, (abs(min(0.0, dd_high)) - 25.0) * 0.7)) if dd_high <= -35.0 else 0.0
    # 2) Proximity to 52W Low Sweet Spot +12% ~ +38% (Max 25 pts)
    if 12.0 <= prox_low <= 38.0:
        score_prox = 25.0
    elif 0.0 <= prox_low < 12.0:
        score_prox = 15.0  # Still very close to bottom
    elif 38.0 < prox_low <= 55.0:
        score_prox = 12.0
    else:
        score_prox = 0.0

    # 3) Right-Side Moving Average Breakout (Max 30 pts)
    if cur > ma20 and cur > ma60:
        score_ma = 30.0
    elif cur >= ma20 * 0.995:
        score_ma = 20.0
    elif vs_ma20 >= -5.0:
        score_ma = 10.0
    else:
        score_ma = 3.0

    # 4) Volume Wash-Out & Earnings Growth Tier (Max 20 pts)
    score_vol = min(10.0, max(0.0, (max_vol_10d - 1.0) * 10.0))
    score_growth = 10.0 if tier == "A+" else (8.0 if tier == "A" else (5.0 if tier == "B+" else -30.0))

    total_score = round(score_dd + score_prox + score_ma + score_vol + score_growth, 1)

    # Determine Signal Stage
    c1_deep_dd = dd_high <= -38.0
    c2_off_low = 10.0 <= prox_low <= 42.0
    c3_above_mas = (cur > ma20) and (cur > ma60)
    c4_vol_or_mom = (max_vol_10d >= 1.35) or (ret20d >= 6.0)

    if not is_growth_qualified:
        signal_stage = "TRAP_EXCLUDED"
    elif c1_deep_dd and c2_off_low and c3_above_mas and c4_vol_or_mom:
        signal_stage = "1_BUY_IGNITION"
    elif c1_deep_dd and (prox_low <= 40.0) and (cur >= ma20 * 0.99 or vs_ma20 >= -2.0):
        signal_stage = "2_READY_MA20"
    elif c1_deep_dd and (prox_low <= 30.0):
        signal_stage = "3_WATCH_BOTTOM"
    else:
        signal_stage = "4_OTHER"

    is_kr = ticker.endswith(".KS") or ticker.endswith(".KQ")
    return {
        "ticker": ticker,
        "name": meta["name"],
        "is_kr": is_kr,
        "growth_tier": tier,
        "growth_desc": meta["growth_desc"],
        "date": dt,
        "close": cur,
        "lo52": lo52,
        "hi52": hi52,
        "prox_low": prox_low,
        "dd_high": dd_high,
        "ma20": ma20,
        "ma60": ma60,
        "ma200": ma200,
        "vs_ma20": vs_ma20,
        "vs_ma60": vs_ma60,
        "vs_ma200": vs_ma200,
        "rsi14": rsi14,
        "vol_surge": max_vol_10d,
        "ret20d": ret20d,
        "score": total_score,
        "signal_stage": signal_stage,
    }


def get_latest_usdkrw() -> float:
    try:
        url = "https://query1.finance.yahoo.com/v8/finance/chart/KRW=X?range=5d&interval=1d"
        r = requests.get(url, headers=HEADERS, verify=False, timeout=5)
        if r.status_code == 200:
            closes = [x for x in r.json()["chart"]["result"][0]["indicators"]["quote"][0]["close"] if x is not None]
            if closes:
                return float(closes[-1])
    except Exception:
        pass
    fx_csv = os.path.join(BASE_DIR, "data", "USDKRW.csv")
    if os.path.exists(fx_csv):
        try:
            df = pd.read_csv(fx_csv).dropna()
            if len(df) > 0:
                return float(df["Close"].iloc[-1])
        except Exception:
            pass
    return 1334.0


def main():
    print("=" * 110)
    print(" [마스터 플랜 레이더] 1단계 SK스퀘어(72주 비과세 1억 졸업) -> 달러 1회 환전 -> 2단계 미국 [SMH 70% + XLV 30%] 코어 시스템")
    print("=" * 110)

    all_tickers = list(UNIVERSE_META.keys())
    results = {}
    usdkrw = get_latest_usdkrw()

    with concurrent.futures.ThreadPoolExecutor(max_workers=16) as executor:
        futs = {executor.submit(fetch_or_update_ticker, t): t for t in all_tickers}
        for fut in concurrent.futures.as_completed(futs):
            t, df = fut.result()
            if df is not None:
                results[t] = calc_stock_signal(t, df)

    # 1. SK스퀘어 72주 및 달러 환전 시뮬레이션 진단
    sk = results.get(MY_PORTFOLIO["ticker"])
    hy = results.get("000660.KS")

    net_factor = (1.0 - 0.0035) * (1.0 - 0.0012)
    target_usd_1eok = (100_000_000.0 * net_factor) / usdkrw
    cur_net_usd = 0.0

    if sk:
        shares = MY_PORTFOLIO["shares"]
        principal = shares * MY_PORTFOLIO["avg_cost"]
        cur_val = shares * sk["close"]
        pnl_krw = cur_val - principal
        pnl_pct = (cur_val / principal - 1.0) * 100.0
        hy_p = f"{hy['close']:,.0f}원" if hy else "N/A"

        target_1eok_72 = 100_000_000.0 / shares   # 72주 단독 1억 돌파가 (1,388,889원)
        target_tot1eok_72 = 97_000_000.0 / shares # 기인출 300만 포함 총자산 1억 돌파가 (1,347,222원)
        target_83m_72 = 79_840_000.0 / shares     # 총 투입원금(8,284만) 100% 복구가 (1,108,889원)
        cur_net_usd = (cur_val * net_factor) / usdkrw

        print(f"\n[STEP 1] 1단계 한국 코어 진단: {MY_PORTFOLIO['name']} ({MY_PORTFOLIO['ticker']}) {shares}주 (기준일: {sk['date']} | 환율: {usdkrw:,.1f}원/$)")
        print("-" * 110)
        print(f" * 현재 주가 / 평단가 : {sk['close']:,.0f}원 / {MY_PORTFOLIO['avg_cost']:,.0f}원 (SK하이닉스 현재가: {hy_p})")
        print(f" * 잔여 원금 / 평가액 : {principal/10000:,.1f}만 원 -> {cur_val/10000:,.1f}만 원 (손익: {pnl_krw/10000:+,.1f}만 원 / {pnl_pct:+.2f}%, 기인출 4주 ~300만 원 별도)")
        print(f" * 기술적 위치 진단   : RSI(14) = {sk['rsi14']:.1f} | 200일선({sk['ma200']:,.0f}원) 대비 {sk['vs_ma200']:+.1f}% | 20일선({sk['ma20']:,.0f}원) 대비 {sk['vs_ma20']:+.1f}%")
        print(f" * [원금복구·1억 목표]: 총원금 복구가 {target_83m_72:,.0f}원 | 총자산 1억 돌파가 {target_tot1eok_72:,.0f}원~{target_1eok_72:,.0f}원 (1억 환전 시 약 ${target_usd_1eok:,.0f})")

        if cur_val >= 97_000_000.0:
            stage1_verdict = "[ACTION: 5단계 1억 원 졸업 구간 도달!] 전량 매도 및 달러(USD) 환전 -> 아래 [STEP 2] SMH 70% + XLV 30% 즉시 구축!"
        elif sk["close"] >= 1_090_000.0:
            stage1_verdict = "[ACTION: 4단계 평단·총원금 복구 구간!] 절반(36주) 선매도 후 달러 전환하여 SMH 70% + XLV 30% 1차 진입 고려!"
        elif sk["close"] >= 950_000.0:
            stage1_verdict = "[HOLD/WATCH: 3단계 MA200 회복 구간] 1억 목표가까지 홀딩 유지 (현금 필요시 최소 주수만 인출)"
        elif sk["close"] < 740_000.0:
            stage1_verdict = "[ALERT: 1단계 킬스위치 점검] 주간 종가 기준 74만 원 이탈 시 50%(36주) 축소 및 달러 방어 점검!"
        elif sk["rsi14"] <= 35.0:
            stage1_verdict = "[HOLD: 2단계 과매도 바닥 구간] 바닥 패닉셀 엄금! 기술적 반등 및 20일선 회복 대기"
        else:
            stage1_verdict = "[HOLD: 2단계 보유 구간] 20일선·200일선 회복 및 1억 졸업 목표가까지 차분히 보유 유지"
        print(f" >> [1단계 행동 지침] : {stage1_verdict}")

    # 2. [STEP 2] 2단계 미국 코어 포트폴리오 (SMH 70% + XLV 30%) & 우측 시동 틸트(90:10) 진단
    smh = results.get("SMH")
    xlv = results.get("XLV")
    print(f"\n[STEP 2] 2단계 미국 코어 포트폴리오 [SMH 70% + XLV 30%] 실시간 진단 (최근 7년 세후 연복리 +30.8% · MDD -28.3% · 샤프 0.88)")
    print("-" * 110)
    if smh and xlv:
        print(f"{'ETF 종목명(티커)':26s} | {'목표비중':>6s} | {'현재가($)':>9s} | {'고점낙폭':>7s} | {'신저가대비':>8s} | {'20일선':>7s} | {'60일선':>7s} | {'RSI(14)':>7s} | {'역할 및 시계열 핵심 기능'}")
        print("-" * 110)
        for t_code, w_str, role_str in [
            ("SMH", "70.0%", "AI·반도체 1등주(NVDA·TSM·AVGO) 성장 엔진"),
            ("XLV", "30.0%", "헬스케어(LLY·UNH·ABBV) 하락 방패 & 리밸런싱 재원"),
        ]:
            m = results[t_code]
            label = f"{m['name'][:14]}({t_code})"
            print(
                f"{label:26s} | {w_str:>6s} | ${m['close']:8,.2f} | {m['dd_high']:+6.1f}% | +{m['prox_low']:6.1f}% | "
                f"{m['vs_ma20']:+6.1f}% | {m['vs_ma60']:+6.1f}% | {m['rsi14']:6.1f}  | {role_str}"
            )

        # SMH 우측 시동 비중 확대(90:10 Dynamic Tilt) 조건 체크
        is_smh_tilt_buy = (smh["dd_high"] <= -22.0) and (8.0 <= smh["prox_low"] <= 40.0) and (smh["close"] > smh["ma20"]) and (smh["close"] > smh["ma60"])
        if is_smh_tilt_buy:
            tilt_verdict = "[🔥 TILT BUY 점등: SMH 90% : XLV 10% 비중 확대!] SMH가 -22%+ 조정 후 20·60일선을 동시 돌파했습니다! (+45% 반등 시까지 90:10 승부)"
            w_smh_rec, w_xlv_rec = 0.90, 0.10
        elif smh["dd_high"] <= -22.0:
            tilt_verdict = f"[⏳ TILT 대기: 기본 70:30 유지] SMH가 고점 대비 {smh['dd_high']:.1f}% 조정 중입니다. 20일선(${smh['ma20']:.2f})·60일선(${smh['ma60']:.2f}) 동시 돌파 시 90:10 확대!"
            w_smh_rec, w_xlv_rec = 0.70, 0.30
        else:
            tilt_verdict = "[✅ CORE HOLD: 정석 70:30 비율 유지] SMH 상승 추세 순항 중 -> SMH 70% + XLV 30% 보유 및 연말 250만 원 비과세 한도 내 리밸런싱"
            w_smh_rec, w_xlv_rec = 0.70, 0.30

        # 1억 원 환전 시($target_usd_1eok) 및 현재 평가액 환전 시($cur_net_usd) 매수 주수 시뮬레이션
        smh_usd_1eok = target_usd_1eok * w_smh_rec
        xlv_usd_1eok = target_usd_1eok * w_xlv_rec
        smh_sh_1eok = smh_usd_1eok / smh["close"]
        xlv_sh_1eok = xlv_usd_1eok / xlv["close"]

        print("-" * 110)
        print(f" * [우측 시동 틸트 판정] : {tilt_verdict}")
        print(
            f" * [1억 졸업 환전 시(${target_usd_1eok:,.0f}) 주문 가이드] : "
            f"SMH({int(w_smh_rec*100)}%) ${smh_usd_1eok:,.0f} (약 {smh_sh_1eok:.1f}주) + "
            f"XLV({int(w_xlv_rec*100)}%) ${xlv_usd_1eok:,.0f} (약 {xlv_sh_1eok:.1f}주)"
        )
        if cur_net_usd > 0:
            smh_sh_cur = (cur_net_usd * w_smh_rec) / smh["close"]
            xlv_sh_cur = (cur_net_usd * w_xlv_rec) / xlv["close"]
            print(
                f" * [현재 평가액 환전 시(${cur_net_usd:,.0f}) 참고 수량] : "
                f"SMH 약 {smh_sh_cur:.1f}주 (${cur_net_usd*w_smh_rec:,.0f}) + "
                f"XLV 약 {xlv_sh_cur:.1f}주 (${cur_net_usd*w_xlv_rec:,.0f})"
            )

    # 3. [STEP 3] (참고용 부록) 미국 개별주 PW-RSI 순환매 레이더 Top 5
    us_candidates = [
        v for k, v in results.items()
        if (not v["is_kr"]) and (k not in ("SMH", "XLV")) and v["signal_stage"] in ("1_BUY_IGNITION", "2_READY_MA20", "3_WATCH_BOTTOM")
    ]
    us_candidates.sort(key=lambda x: (x["signal_stage"], -x["score"]))

    print(f"\n[STEP 3] (참고용 시장 온도계) 미국 개별 성장주 PW-RSI 우측 시동 레이더 Top 5")
    print("-" * 110)
    print(f"{'순위/미국종목명(티커)':24s} | {'현재가($)':>9s} | {'고점낙폭':>7s} | {'신저가대비':>8s} | {'20일선':>7s} | {'60일선':>7s} | {'거래량':>5s} | {'점수':>4s} | {'개별주 우측 시동 상태'}")
    print("-" * 110)

    for idx, m in enumerate(us_candidates[:5], 1):
        cur_str = f"${m['close']:,.2f}"
        trig60_str = f"${m['ma60']:,.2f}"
        trig20_str = f"${m['ma20']:,.2f}"

        if m["signal_stage"] == "1_BUY_IGNITION":
            status = f"[BUY: 우측 시동 켜짐!] 20/60일선 동시 돌파! ({m['growth_desc'][:20]})"
        elif m["signal_stage"] == "2_READY_MA20":
            status = f"[READY: 예비 시동] 20일선 근접/회복 -> 60일선({trig60_str}) 돌파 대기"
        else:
            status = f"[WAIT: 좌측 바닥] 20일선({trig20_str}) 회복 대기 ({m['growth_desc'][:18]})"

        label = f"{idx:2d}. {m['name'][:8]}({m['ticker']})"
        print(
            f"{label:24s} | {cur_str:>9s} | {m['dd_high']:+6.1f}% | +{m['prox_low']:6.1f}% | "
            f"{m['vs_ma20']:+6.1f}% | {m['vs_ma60']:+6.1f}% | {m['vol_surge']:4.2f}x | {m['score']:4.1f} | {status}"
        )

    print("-" * 110)
    print(" * [2단계 코어 3대 원칙] 1) SMH 70% + XLV 30% 기본 보유(과세이연 복리) | 2) 연말 250만 원 공제 내 비과세 리밸런싱 | 3) SMH -22% 조정 후 우측 시동 시 90:10 확대")
    print("=" * 110)


if __name__ == "__main__":
    main()

