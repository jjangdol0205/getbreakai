# GEMINI.md — 3사업부 GetBreakAI Japan (`getbreakai.com`) 절대 규칙 (Ground Rules)

이 문서는 `D:\드림컴퍼니\3사업부` 작업 시 루트 `D:\드림컴퍼니\GEMINI.md`와 100% 일관되게 적용되는 하위 규칙입니다. 모든 대화방(`텔레그램`, `hq_main`, `sns_video`, `seo_monetize`, `payment_pg`)은 반드시 루트 `D:\드림컴퍼니\GEMINI.md` 및 `D:\드림컴퍼니\data\hq_ssot_state.json`과 동일한 기준만 답변·수행합니다.

---

## 1. 법인 정체성 · 전담 CEO 봇 · 호스팅 (SSOT)
- **법인명 / 도메인**: 3사업부 (`GBA` 법인) — **`https://getbreakai.com`** (주력 일본어 랜딩 **`https://getbreakai.com/jp/`** 및 루트 `/` 동기화, **GitHub Pages**, 원격 저장소 `jjangdol0205/getbreakai.git` `main` 브랜치)
- **전담 CEO 봇**: **`@SemifearGreedbot`** (`3사업부/.env`의 `TELEGRAM_BOT_TOKEN`, 3사업부 일본법인 전담 CEO — 그룹 비서실장·감사관은 **`@Allcompany1_bot`**)
- **일본 시니어(50~70대) 8대 웹사이트 원칙 & 직관 가독성**:
  - 상단 부제목을 **2줄 이내 쉬운 노후 현금흐름 문장**으로 압축(티커 과밀 나열 금지), 초기 기본 본문 `18px+`, `本日の3色バランス早見カード`에 실시간 기준일·신호등 판정·권장 비중(%)·예상 배당률(%)을 명확히 표기합니다 (`SOXL` 등 레버리지 문서는 `noindex` 격리, `t.me` 링크 `0건`, 한글 `[가-힣]` `0건`).
- **핵심 가치 사다리 (Value Ladder)**:
  1. **무료 입문 (`¥0`)**: 30초 新NISA 노후 시뮬레이터(`#gba-retirement-architect-jp`) + 『はじめての新NISA＆楽天・SBI証券アプリ基本マニュアル』 (`#gbaFreeStarterManualJp`) + 『朝の資産守り倶楽部』 (`#gbaMorningClubJp` / `#gba-jp-passwordless-signup`, 1클릭 설문 + Substack형 일본어 에디터 레터)
  2. **유료 전환 (`Polar.sh` 글로벌 MoR — `window.PAYMENT_CONFIG`, `PROVIDER: 'polar_sh'`, `lemonsqueezy` `0건`)**:
     - Monthly Pro (`$29/mo` · `約4,400円/月` · `いつでも1クリック解約OK`) / Annual Pro VIP (`$199/yr` · `約30,000円/年`), 개통 전 `vip_waitlist` 20% 얼리버드 모달 방어.
     - **체감형 3대 新NISA Pro 효능감**: ① 新NISA 생애 한도 1,800만 엔 연차별 퇴직금 배분 설계표 · ② `1489 + VYM/HDV + 個人向け国債` 시차 조합 12개월 매월 배당 캘린더 · ③ 라쿠텐·SBI증권 스마트폰/PC 큰글씨 화면 매뉴얼 + 14p 일본어 PDF 마스터북 번들 (`Institutional Desk`: `mailto:beable9489@gmail.com`).

---

## 2. 빌드 영속성 및 잠근 기능(Locked DOM) 보호
- `/jp/index.html`은 **`scripts/build_jp_seo_pages.py`** 실행 시 재생성되므로, `/jp/` 화면 수정 시 반드시 **`scripts/build_jp_seo_pages.py` 템플릿 원본**에 영구 반영한 뒤 빌드를 실행하십시오.
- 잠근 DOM(`#gba-retirement-architect-jp`, `#gbaMorningClubJp`, `#gba-jp-passwordless-signup`, `#gbaFreeStarterManualJp`, `#gbaStarterManualModal`) 및 푸터 3대 약관을 절대 훼손하지 마십시오.

---

## 3. 실서버 배포 및 `/live-audit` 출구 잠금
- 웹 수정 시 반드시 빌드 스크립트 실행 ➜ `git commit & push` (`jjangdol0205/getbreakai.git` `main`) ➜ CDN 전파 대기 후 `python "C:\Users\jjang\.gemini\config\skills\live-audit\run_live_audit.py" getbreakai.com` `ALL PASS` 확인 후 보고합니다.
