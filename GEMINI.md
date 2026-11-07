# GEMINI.md — 1사업부 RightSideAlpha × SemiFearGreed (`truthofmarket.com`) 절대 규칙 (Ground Rules)

이 파일은 AI 에이전트가 매 작업마다 최우선으로 준수해야 하는 핵심 규칙(Always-On Ground Rules)입니다.

---

## 1. 작업 전 필수 습관 (3줄 브리핑 원칙)
- **코드 수정 전 3줄 브리핑**: 사용자가 지시한 파일을 수정하기 전에 **어느 파일의 어느 영역(컴포넌트/함수/섹션)을 어떻게 바꿀지 3줄 이내로 먼저 브리핑**한 뒤 작업할 것.
- **단일 범위 집중**: 사용자가 지시한 파일(`@파일명`)과 `TODO.md`의 현재 체크리스트 항목만 수정하고, 요청하지 않은 주변 기능이나 레이아웃을 임의로 리팩토링하지 말 것.
- **참고 문서 우선 확인**: 화면 흐름이나 데이터 구조가 헷갈릴 때는 전체 코드를 다 뒤지지 말고 루트의 `PRD.md`와 `TODO.md`를 먼저 읽을 것.

---

## 2. 토큰 폭탄 방지 (절대 직접 열람/수정 금지 파일)
다음 대용량·자동생성 파일들은 컨텍스트(토큰) 낭비를 막기 위해 **직접 `read_file`로 전체 열람하거나 수동 편집하지 말 것**:
- `dist/` 폴더 내부 파일 (직접 수정 금지 — 반드시 `frontend/` 및 원본 수정 후 `python scripts/build_static_bundle.py`로 생성)
- `data/stocks_pro_master.json`, `static_api/*.json` 등 대용량 시계열 데이터 파일 (전체를 읽지 말고 필요한 키 구조만 확인)
- `.mp4`, `.wav`, `.png` 등 바이너리 미디어 자산

---

## 3. 절대 깨뜨리면 안 되는 가드레일 (Guardrails)

### ① 레몬스퀴지(Lemon Squeezy Store `#296100`) 실결제(Live Mode) UUID 보호
- `frontend/src/components/Modals.js` 및 `frontend/src/main.js`에 설정된 **Live Mode 체크아웃 URL**을 절대 Test Mode UUID로 되돌리거나 훼손하지 말 것:
  - **Pro Monthly (`$29/mo`, Product `#1491944`)**: `https://truthofmarket.lemonsqueezy.com/checkout/buy/bad98d00-7175-41f6-9d58-eeb2471d0da4`
  - **Lifetime Pass (`$199`, Product `#1491942`)**: `https://truthofmarket.lemonsqueezy.com/checkout/buy/00c9f6e1-c8be-42a4-b5a5-e05af1a41ed9`
- 라이선스 모달(`#licenseModal`)과 하단 푸터의 공식 사업자 표기(`Operated by Yoonju Lee · KIDS-FIT Global Studio (Lemon Squeezy Store #296100)`)를 절대 삭제하지 말 것.

### ② 3대 사업부 통합 마스터 텔레그램 브릿지 보호
- `scripts/master_hq_telegram_bridge.js`는 1·2·3사업부 전체 원격 제어 및 레몬스퀴지 실시간 승인·결제 감시 데몬이므로, 기존 명령어 라우팅과 순차 큐(`taskQueue`) 로직을 절대 훼손하지 말 것.
- 과부하 방지를 위해 모든 무거운 작업은 **한 번에 한 사업부씩 순차 실행**할 것.

### ③ 쇼츠·릴스 영상 클린 마스터링 원칙
- 영상 제작·편집 시 **화면 상·하단에 조잡한 배너/박스를 상시 띄우지 말 것**.
- 본론 구간에는 **깔끔한 자막만 단독 배치**하고, **홈페이지 도메인(`truthofmarket.com`) 유도는 마지막 2~3초 엔딩 컷에만** 깔끔하게 노출할 것.

### ④ 빌드 및 멀티 리모트 배포 규칙
- 프론트엔드 수정 후에는 반드시 `python scripts/build_static_bundle.py`를 실행하여 `dist/`에 반영할 것.
- Git 배포 시에는 `truthofmarket` (`truthofmarket.com`)과 `origin` (`getbreakai.git`) 리모트 정합성을 유지할 것.
