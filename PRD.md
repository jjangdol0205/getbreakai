# PRD.md — 1사업부 RightSideAlpha × SemiFearGreed (`truthofmarket.com`) 앱 설계도 및 명세서

이 문서는 AI가 전체 코드베이스를 매번 뒤지지 않고도 **1) 핵심기능·화면흐름(User Flow), 2) 데이터 스키마(Data Schema), 3) 가드레일(Guardrails), 4) 모듈화 파일 역할 지도**를 즉시 파악하도록 돕는 기준 설계도입니다.

---

## 1. 핵심 기능 및 화면 흐름 (User Flow)

사용자가 `https://truthofmarket.com`에 접속하여 무료 진단을 체험하고 유료 Pro/Lifetime 멤버십으로 전환하기까지의 화면 이동 순서입니다:

1. **[화면 1] 상단 헤더 메뉴바 (`Header & Regime Banner`)**
   - 담당 파일: `frontend/src/main.js`, `semi-fear-greed.html`
   - 실시간 `$SMH` 반도체 공포·탐욕 지수(7-Factor Regime Score) 요약 배지, 터미널 탭 전환(`72-Stock Scanner` ↔ `$SMH Fear & Greed`), `Unlock Pro ($29/mo)` 결제 모달 호출 버튼 배치.
2. **[화면 2] 72개 미국 주도주 퀀트 스캐너 & 차트 (`Main Scanner & Chart`)**
   - 담당 파일: `frontend/src/main.js`, `frontend/src/components/StockTable.js`, `frontend/src/components/ChartPanel.js`
   - 6-Factor Right-Side Ignition 시그널(`IGNITION`, `WASHOUT BASE`, `TRAP`) 필터링 및 종목 클릭 시 60일 이동평균선(MA60)·거래량 돌파 차트 표시.
   - 무료 사용자는 상위 시그널 일부 열람 가능, VIP 잠금 종목 클릭 시 결제 모달(`#licenseModal`) 오픈.
3. **[화면 3] 포지션 닥터 (`Position Doctor — 3초 손절·목표가 진단기`)**
   - 담당 파일: `frontend/src/components/Modals.js`, `frontend/src/main.js`
   - 사용자가 보유 티커(예: `NVDA`, `TSLA`)와 평단가를 입력하면 기계적 `-9.0%` 칼손절가, `55일` 타임스탑, `+100%` 1차 익절 목표가를 3초 만에 계산.
4. **[화면 4] 로그인·라이선스 키 인증 및 레몬스퀴지 결제창 (`Login & Paywall Box`)**
   - 담당 파일: `frontend/src/components/Modals.js` (`#licenseModal`)
   - **Pro Monthly (`$29/mo`)** 및 **Lifetime Pass (`$199`)** 원클릭 레몬스퀴지 결제 버튼 + 구매 후 발급받은 라이선스 키(`TOM-...` / Lemon Squeezy License Key) 입력·활성화 창.
5. **[화면 5] 하단 푸터 & 법적 고지 (`Footer`)**
   - 담당 파일: `frontend/src/main.js`, `terms.html`, `privacy.html`, `refund.html`
   - 공식 스토어 운영자 표기(`Operated by Yoonju Lee · KIDS-FIT Global Studio (Lemon Squeezy Store #296100)`), 이용약관·개인정보처리방침·환불정책 링크.

---

## 2. 데이터 스키마 (Data Schema — 저장소별 열 이름 정의)

### A. 브라우저 임시저장소 (`localStorage` — 클라이언트 상태)
| Key 이름 | 저장되는 정보 (엑셀 열 구조) | 담당 파일 |
| :--- | :--- | :--- |
| `rsa_pro_license_key` | 사용자가 입력해 인증 완료된 유료 라이선스 키 문자열 | `frontend/src/components/Modals.js` |
| `rsa_pro_unlocked` | `'true'` 또는 `'false'` (VIP 잠금 해제 여부) | `frontend/src/main.js` |
| `rsa_watchlist` | 사용자가 즐겨찾기한 미국 주식 티커 배열 (예: `["NVDA","AVGO"]`) | `frontend/src/main.js` |

### B. 정적 마켓 데이터 DB (`static_api/` & `data/`)
| 파일 경로 | 주요 열(필드) 구조 | 역할 |
| :--- | :--- | :--- |
| `static_api/semi_overview.json` | `score`(0~100), `regime`(`Extreme Fear` 등), `smh_price`, `xlv_price`, `target_smh_weight`(70%~80%) | `$SMH × $XLV` 바벨 리밸런싱 및 공포·탐욕 지수 |
| `data/stocks_pro_master.json` | `ticker`, `name`, `sector`, `price`, `ma60`, `vol_ratio`, `pw_rsi_stage`, `stop_loss_pct` | 72개 미국 주도주 6-Factor 시그널 테이블 |

### C. 외부 클라우드 / 결제 및 텔레그램 API
- **Lemon Squeezy API (`Store #296100`)**: 유료 결제 및 라이선스 키 검증, 3분 주기 실시간 본심사 승인·매출 감시(`scripts/master_hq_telegram_bridge.js` 내 `checkLemonSqueezyLiveStatus`).
- **Master HQ Telegram Bridge (`scripts/master_hq_telegram_bridge.js`)**: 사장님 텔레그램(`Chat ID 755033799`)과 연결되어 1·2·3사업부 원격 명령 수신 및 완료 보고(`--notify`) 전송.

---

## 3. 가드레일 (Guardrails — 절대 깨뜨리면 안 되는 약속)
1. **레몬스퀴지 Live UUID 고정**: `bad98d00-7175-41f6-9d58-eeb2471d0da4` (`$29/mo`), `00c9f6e1-c8be-42a4-b5a5-e05af1a41ed9` (`$199`) 절대 변경 금지.
2. **원본 수정 후 빌드 필수**: `frontend/` 또는 루트 HTML 수정 후 반드시 `python scripts/build_static_bundle.py` 실행하여 `dist/` 갱신.
3. **모듈별 단일 파일 수정**: 상단 메뉴바를 고칠 때 로그인/결제 모달이나 차트 계산 로직을 건드리지 말 것.

---

## 4. 모듈화 파일 역할 지도 (어디를 고쳐야 하는가?)

| 수정하고 싶은 화면 / 기능 | 지정할 파일 (`@파일명`) | 비고 (주의사항) |
| :--- | :--- | :--- |
| **상단 메뉴바(Header) / 메인 레이아웃 / 하단 푸터(Footer)** | `@frontend/src/main.js`, `@index.html` | 푸터 사업자 표기(`Store #296100`) 유지 필수 |
| **로그인·라이선스 인증창 / 유료 결제창(Login & Paywall Box)** | `@frontend/src/components/Modals.js` | `#licenseModal` 내 Live UUID 2종 절대 유지 |
| **반도체 공포·탐욕 터미널 화면 (`$SMH × $XLV`)** | `@semi-fear-greed.html` | 70:30 / 80:20 바벨 계산기 로직 보호 |
| **쇼츠·릴스 영상 클린 마스터링** | `@scripts/levelup_clean_shorts_tom_kfg.py` | 자막만 깔끔하게 배치, 도메인 유도는 마지막 3초만 |
| **3대 사업부 텔레그램 원격 제어 & 레몬스퀴지 감시** | `@scripts/master_hq_telegram_bridge.js` | 단일 프로세스 순차 큐(`taskQueue`) 유지 |
