# 🇯🇵 GetBreakAI (`getbreakai.com`) — 오늘 바로 끝내는 일본 무인 자동 홍보 세팅 가이드 & Flow 영상 제작 프롬프트

사장님께서 직접 하시는 **Flow 기반 유튜브 쇼츠 & 인스타 릴스** 외에, 나머지 모든 일본 마케팅 채널(X/트위터 · 스레드 · 구글/야후 재팬 SEO · 텔레그램 알림)을 **오늘 딱 10분 투자해서 평생 100% 무인으로 돌아가게 만드는 단계별 매뉴얼**입니다.

---

## ✅ 1단계: 일본 X(트위터) & 스레드(Threads) 100% 무인 자동 포스팅 세팅 (소요시간: 5분 · 무료)

현재 우리 서버(`https://getbreakai.com`)에는 매일 아침 06:00 미국장 마감 직후 자동으로 최신 시세와 일본어 분석글이 업데이트되는 **자동 배포용 RSS 피드 주소 2개**가 이미 개통되어 있습니다:
- **일본 X / 스레드 자동 트윗용 RSS 주소**: `https://getbreakai.com/jp/x-feed.xml`
- **일본 블로그 / 칼럼용 RSS 주소**: `https://getbreakai.com/jp/feed.xml`

### 👉 오늘 바로 세팅하는 순서 (`dlvr.it` 무료 버전 추천)
1. 인터넷 브라우저에서 **[https://dlvrit.com](https://dlvrit.com)** 접속 후 무료 회원가입(Sign Up Free)을 합니다.
2. 첫 화면의 **`1. Auto Post from Feeds` (피드에서 자동 포스팅)** 입력창에 아래 주소를 복사해서 붙여넣고 돋보기(검색) 버튼을 누릅니다:
   ```text
   https://getbreakai.com/jp/x-feed.xml
   ```
3. 검색된 피드 옆의 **`[+]` 버튼**을 누르고 **`Next: Connect Social`**을 클릭합니다.
4. 연결할 SNS 아이콘 중에서 **X (Twitter)** 또는 **Threads (스레드)** 아이콘을 눌러 일본 홍보용 계정으로 로그인(권한 허용)합니다.
5. **`Start Posting`**을 누르면 세팅 끝!
   - **작동 방식**: 매일 아침 06:00에 우리 GitHub 서버가 미국장 종가와 ATR 손절 라인을 계산해 `x-feed.xml`을 업데이트하면, `dlvr.it`이 이를 감지하여 **일본어 분석 트윗 + `#米国株 #新NISA #エヌビディア` 해시태그 + `https://getbreakai.com/?ticker=NVDA` 링크**를 사장님 X/스레드 계정에 자동으로 올립니다!

---

## ✅ 2단계: 구글 재팬(Google.co.jp) & 야후 재팬(Yahoo! JAPAN) 검색 노출 등록 (소요시간: 3분 · 1회만 등록)

현재 `https://getbreakai.com/jp/` 산하에 일본인들이 가장 많이 검색하는 미국주식 30개 핵심 키워드 페이지가 생성되어 있고, 매일 아침 자동으로 갱신됩니다. 구글 재팬 검색 결과에 빠르게 상단 노출되도록 오늘 딱 한 번만 사이트맵을 제출해 주세요.

1. **[Google Search Console](https://search.google.com/search-console)** 접속 후 `getbreakai.com` 도메인 선택
2. 왼쪽 메뉴에서 **`Sitemaps (사이트맵)`** 클릭
3. `'새 사이트맵 추가'` 입력칸에 아래 글자를 입력하고 **`제출`** 클릭:
   ```text
   sitemap.xml
   ```
4. 끝! 이후에는 매일 아침 06:00마다 우리 무인 스케줄러(`getbreakai_jp_autopilot.yml`)가 자동으로 구글·야후·빙(IndexNow)에 최신 페이지를 핑(Ping)하여 검색 유입을 모아옵니다.

---

## ✅ 3단계: Google Flow로 영상 만드실 때 바로 복붙하는 4컷 프롬프트 (인물 홍보형: 미녀 아나운서 / 미남 퀀트)

일본·미국 주식 쇼츠/릴스에서는 **첫 2초에 매력적인 인물(TV도쿄 경제 아나운서 스타일의 미녀 또는 마루노우치 수트핏 미남 펀드매니저)**이 등장해 시선을 사로잡고, 중간에 차트·터미널 데이터를 보여준 뒤 인물로 마무리하는 구조가 **스크롤 멈춤률(Thumb-stop rate)과 유료 전환율이 가장 높습니다!**

### 👩 컨셉 A: 지적인 도쿄 금융 미녀 애널리스트 / 경제 캐스터 버전 (남성 30~50대 투자자 타깃 압도적 1위)
- **Cut 1 (0~3초 · 시선 강탈 훅)**:
  ```text
  Vertical 9:16 medium close-up of a stunningly beautiful young Japanese female financial anchor in a tailored navy blazer, standing in a sleek Tokyo skyscraper office at night with glowing stock monitors blurred in the background, looking directly into the camera with a confident intelligent smile, cinematic lighting, 8k photorealistic
  ```
- **Cut 2 (3~7초 · 손실 공감 & 경고)**:
  ```text
  Vertical 9:16 cinematic shot of the same beautiful Japanese female financial analyst looking concerned as she points at a red plunging stock candlestick chart on a glass tablet, dramatic rim lighting, shallow depth of field, 8k photorealistic
  ```
- **Cut 3 (7~12초 · AI 시그널 & 2.0x ATR 해법 제시)**:
  ```text
  Vertical 9:16 shot of the beautiful Japanese female analyst tapping a futuristic glowing screen showing NVIDIA stock chart locking in a green 2.5R profit target and a sharp blue 2.0x ATR stop-loss line, high-trust fintech commercial vibe
  ```
- **Cut 4 (12~16초 · 엔딩 미소 & 스마트폰 터미널 제시)**:
  ```text
  Vertical 9:16 close-up of the beautiful Japanese female financial anchor smiling warmly at the camera while holding up a sleek smartphone displaying a clean navy-and-white stock calculator app, golden bokeh background, ultra-realistic 8k
  ```

### 👨 컨셉 B: 멋있는 월가/도쿄 수트핏 남성 퀀트 트레이더 버전 (전문성·신뢰감 극대화)
- **Cut 1 (0~3초 · 카리스마 훅)**:
  ```text
  Vertical 9:16 medium close-up of a handsome charismatic Japanese male hedge fund manager in a sharp bespoke charcoal suit and luxury watch, standing in front of a multi-monitor Wall Street quant trading desk at night, looking intensely at the camera, cinematic moody lighting, 8k photorealistic
  ```
- **Cut 2 (3~7초 · 개미들의 뇌동매매 지적)**:
  ```text
  Vertical 9:16 over-the-shoulder shot of the handsome male quant trader calmly analyzing a volatile US stock chart while red retail panic alerts flash on a secondary screen, ultra-sharp focus, financial thriller aesthetic
  ```
- **Cut 3 (7~12초 · 기관 수급 & 2.0x ATR 정밀 타점)**:
  ```text
  Vertical 9:16 shot of the handsome male trader gesturing toward a crisp holographic display of SEC 8-K data and a 2.0x ATR risk shield locking in exact share counts in USD and Yen, 8k photorealistic
  ```
- **Cut 4 (12~16초 · 여유로운 성공 엔딩)**:
  ```text
  Vertical 9:16 shot of the handsome Japanese male quant trader leaning back with a confident nod, holding a smartphone showing a clean financial terminal interface, warm luxury office lighting, 8k
  ```

### 🎙️ [일본어 나레이션 대본 (TTS 또는 Flow 자막용)]
> 「新NISAでエヌビディアやパランティアを『なんとなく』で買っていませんか？個人投資家が大損する最大の原因は、損切りラインを決めずに塩漬けにすることです。ウォール街のクオンツAI『GetBreakAI』なら、英語のSEC開示とオプションのガンマ需給を3秒で日本語化。さらに14日間の平均値動き幅・ATRから、口座資金の1.5%以内に損失を抑える『適正購入株数』と『逆指値ライン』をドルと日本円で自動計算します。プロフィールのリンク、getbreakai.comで今すぐ無料計算してみてください。」

### 📋 [유튜브 쇼츠 / 인스타 릴스 업로드 시 복붙용 캡션 & 해시태그]
- **제목**:
  `【米国株・新NISA】エヌビディア＆パランティア、どこで損切り・利確する？機関のATR株数計算機 #米国株 #新NISA #NVDA`
- **본문 / 캡션**:
  ```text
  🔥 米国株を「感覚」で売買して含み損を塩漬けにしていませんか？

  ウォール街の機関投資家が使う「3大一次情報＋2.0x ATR資金管理」を完全日本語化📊
  ✅ 英語のSEC 8-K（決算・重要契約）＆Form-4（役員の自社株買い）を3秒で点数化
  ✅ SBI証券・楽天証券・マネックス証券の逆指値にそのまま使えるドル/円同時計算
  ✅ 新NISA（非課税0%）と特定口座（20.315%）の手取り純利益をワンタッチ比較！

  👉 プロフィールのリンク（ https://getbreakai.com ）から登録不要・無料で今すぐ計算できます！

  #米国株 #新NISA #エヌビディア #パランティア #テスラ #SOXL #半導体株 #米国株投資 #株式投資 #スイングトレード #資産運用
  ```
