import { formatCheckoutUrl } from "../services/api.js";

const PRICING_COPY = {
  en: {
    t1Badge: "INSTITUTIONAL PRO",
    t1Title: "Pro Quantitative Terminal & Daily SEC Brief",
    t1Period: "/ month",
    t1Items: [
      "Unmask all 72 US Equity PW-RSI Scores, MA60 Breakout Triggers & -9% Stop Levels",
      "Daily 08:10 EST Primary-Filing (10-K/10-Q/8-K) Turnaround Research Digest",
      "Position Risk & 55-Day Time-Stop Diagnostic Engine (Position Doctor)",
      "Full TradingView Pine Script v5 Indicator Source Code + SemiFearGreed 26Y CSV",
    ],
    t1Btn: "Subscribe via Lemon Squeezy ($29/mo)",
    t2Badge: "FOUNDER ALLOCATION",
    t2Title: "Lifetime Research & Terminal License",
    t2Period: "/ one-time",
    t2Items: [
      "Permanent License Key — Zero recurring monthly subscription charges",
      "Complete 26.8-Year (2000–2026) US Equity & Semiconductor ETF Backtest Datasets",
      "Multilingual Access (English, Japanese & Korean SEC Research Briefs)",
      "Full Access to both RightSideAlpha and SemiFearGreed Pro Features",
    ],
    t2Btn: "Acquire Lifetime License ($199)",
    t3Badge: "EXECUTION & CHARTING PARTNERS",
    t3Title: "Direct Charting, Consensus & Broker Execution",
    t3Desc: "Verify MA20/MA60 volume breakouts, EPS revisions, and execute US stock/ETF orders with fee rebates:",
    t3Items: [
      "<b>TradingView Pro</b> — Multi-timeframe MA20/MA60 & Pine Script v5 execution",
      "<b>Seeking Alpha Premium</b> — Quant Grades & 1-2Y consensus EPS revision tracking",
      "<b>US Brokerage & Global Exchange</b> — Low-spread NYSE/NASDAQ & 24/7 Perp execution",
    ],
    tvBtn: "📈 Launch TradingView Terminal ↗",
    saBtn: "📊 Open Seeking Alpha EPS Consensus ↗",
    brokerBtn: "🏦 Open US Broker / Exchange PartnerBonus ↗",
    tgBtn: "🤖 Connect Telegram Alert Bot (@SemifearGreedbot) ↗",
  },
  kr: {
    t1Badge: "PRO 퀀트 멤버십",
    t1Title: "프로 퀀트 터미널 & 일간 SEC 공시 리서치",
    t1Period: "/ 월 구독",
    t1Items: [
      "미국 상장 72개 전 종목 진입 트리거(TRG) · -9% 칼손절(STP) · +100% 목표가(TP1) 전면 공개",
      "매일 아침 SEC 원문(10-K/10-Q/8-K) 기반 우측 시동 턴어라운드 핵심 요약 브리프",
      "포지션 닥터(Position Doctor): 내 보유종목 -9% 손절 / 55일 시간손절 / 원금회수 실시간 판독",
      "TradingView Pine Script v5 전용 지표 원본 코드 + 반도체 공포·탐욕 26년치 CSV 다운로드",
    ],
    t1Btn: "Lemon Squeezy로 Pro 구독하기 ($29/월)",
    t2Badge: "파운더 평생 소장권",
    t2Title: "평생 리서치 & 터미널 무제한 라이선스",
    t2Period: "/ 1회 결제 (평생)",
    t2Items: [
      "영구 라이선스 키 즉시 발급 — 매월 나가는 정기 구독료 평생 0원",
      "26.8년(2000–2026) 미국 개별주 & 반도체($SMH:$XLV) 전체 백테스트 원본 데이터셋 제공",
      "한국어 · 영어 · 일본어 3개 국어 SEC 리서치 브리프 및 텔레그램 실시간 알림 연동",
      "RightSideAlpha(개별주) + SemiFearGreed(반도체 공포지수) 모든 Pro 기능 영구 잠금 해제",
    ],
    t2Btn: "평생 라이선스 소장하기 ($199)",
    t3Badge: "차트 · 분석 · 증권/거래소 제휴 혜택",
    t3Title: "실전 차트 검증 & 제휴 증권사/거래소 수수료 혜택",
    t3Desc: "MA20/MA60 거래량 돌파 차트 확인부터 EPS 컨센서스 점검, 실전 매매 수수료 리베이트까지 원클릭으로 연결됩니다:",
    t3Items: [
      "<b>TradingView Pro</b> — MA20/MA60 돌파 및 Pine Script v5 지표 자동 작도 (제휴 할인)",
      "<b>Seeking Alpha Premium</b> — 월가 애널리스트 1~2년 선행 EPS 상향 리비전 추적",
      "<b>제휴 증권사 & 글로벌 거래소</b> — 미국주식(IBKR/Webull) 및 24시간 지수/선물 수수료 우대",
    ],
    tvBtn: "📈 TradingView 차트 터미널 열기 ↗",
    saBtn: "📊 Seeking Alpha 실적 컨센서스 열기 ↗",
    brokerBtn: "🏦 제휴 증권사 / 거래소 수수료 혜택 받기 ↗",
    tgBtn: "🤖 텔레그램 실시간 알림 봇 연결 (@SemifearGreedbot) ↗",
  },
  jp: {
    t1Badge: "INSTITUTIONAL PRO",
    t1Title: "Pro クオンツターミナル＆日次SECリサーチ",
    t1Period: "/ 月額",
    t1Items: [
      "米国72銘柄すべてのMA60突破トリガー(TRG)・-9%損切(STP)・+100%目標値(TP1)を完全公開",
      "毎朝08:10 EST更新・SEC一次開示(10-K/10-Q/8-K)ターンアラウンド分析ブリーフ",
      "ポジションドクター：保有銘柄の-9%損切 / 55日タイムストップ / 元本回収を即時診断",
      "TradingView Pine Script v5 インジケーター完全ソース＋半導体指数26年分CSVダウンロード",
    ],
    t1Btn: "Lemon SqueezyでPro購読 ($29/月)",
    t2Badge: "FOUNDER LIFETIME",
    t2Title: "永久リサーチ＆ターミナルライセンス",
    t2Period: "/ 買い切り(永久)",
    t2Items: [
      "永久ライセンスキー発行 — 毎月のサブスクリプション費用ゼロ",
      "26.8年間(2000–2026)の米国株＆半導体ETF完全バックテストデータセット収録",
      "日本語・英語・韓国語対応のSECリサーチブリーフ＆Telegramアラート連携",
      "RightSideAlpha＋SemiFearGreedの全Pro機能を永久アンロック",
    ],
    t2Btn: "永久ライセンスを取得 ($199)",
    t3Badge: "EXECUTION & CHARTING PARTNERS",
    t3Title: "チャート検証・EPSコンセンサス・提携証券/取引所",
    t3Desc: "MA20/MA60出来高ブレイクの確認、EPSリビジョン検証、米国株・指数の執行パートナー特典：",
    t3Items: [
      "<b>TradingView Pro</b> — マルチタイムフレームMA20/MA60＆Pine Script v5実行",
      "<b>Seeking Alpha Premium</b> — クオンツ評価＆1〜2年先EPSコンセンサス推移",
      "<b>提携証券・取引所 (IBKR / Webull / Bybit)</b> — 米国株・24時間インデックス取引特典",
    ],
    tvBtn: "📈 TradingView チャートを開く ↗",
    saBtn: "📊 Seeking Alpha EPSコンセンサス ↗",
    brokerBtn: "🏦 提携証券・取引所の手数料特典を見る ↗",
    tgBtn: "🤖 TelegramアラートBot接続 (@SemifearGreedbot) ↗",
  },
};

export function renderPricing(state) {
  const cfg = state.config || {};
  const c = PRICING_COPY[state.lang] || PRICING_COPY.en;
  const lsMonthly = formatCheckoutUrl(
    cfg.ls_site1_monthly_url,
    "https://truthofmarket.lemonsqueezy.com/checkout/buy/bad98d00-7175-41f6-9d58-eeb2471d0da4"
  );
  const lsLtd = formatCheckoutUrl(
    cfg.ls_site1_ltd_url,
    "https://truthofmarket.lemonsqueezy.com/checkout/buy/00c9f6e1-c8be-42a4-b5a5-e05af1a41ed9"
  );
  const brokerName = cfg.broker_name || "Bitget (7nja)";

  return `
    <section class="pricing-grid" id="pricingSection">
      <!-- Tier 1: Pro Monthly -->
      <div class="price-card featured">
        <div>
          <span class="badge badge-ignition">${c.t1Badge}</span>
          <h3 style="font-size:1.12rem; font-weight:800; margin-top:10px; color:#ffffff;">
            ${c.t1Title}
          </h3>
          <div class="price-num">$29 <span style="font-size:0.82rem; color:var(--muted); font-family:var(--font-sans); font-weight:500;">${c.t1Period}</span></div>
          <ul class="price-list">
            ${c.t1Items.map((item) => `<li><span>—</span> <span>${item}</span></li>`).join("")}
          </ul>
        </div>
        <a class="btn btn-primary lemonsqueezy-button" id="cardMonthlyBtn" href="${lsMonthly}" target="_blank" rel="noopener noreferrer" style="justify-content:center; padding:10px;">
          ${c.t1Btn}
        </a>
      </div>

      <!-- Tier 2: Lifetime Pass -->
      <div class="price-card">
        <div>
          <span class="badge badge-watch">${c.t2Badge}</span>
          <h3 style="font-size:1.12rem; font-weight:800; margin-top:10px; color:#ffffff;">
            ${c.t2Title}
          </h3>
          <div class="price-num">$199 <span style="font-size:0.82rem; color:var(--muted); font-family:var(--font-sans); font-weight:500;">${c.t2Period}</span></div>
          <ul class="price-list">
            ${c.t2Items.map((item) => `<li><span>—</span> <span>${item}</span></li>`).join("")}
          </ul>
        </div>
        <a class="btn btn-emerald lemonsqueezy-button" id="cardLtdBtn" href="${lsLtd}" target="_blank" rel="noopener noreferrer" style="justify-content:center; padding:10px;">
          ${c.t2Btn}
        </a>
      </div>

      <!-- Tier 3: Institutional Charting, Consensus & Broker/Exchange Partners -->
      <div class="price-card">
        <div>
          <span class="badge" style="background:rgba(41,98,255,0.14); color:#93c5fd; border:1px solid rgba(41,98,255,0.3);">${c.t3Badge}</span>
          <h3 style="font-size:1.12rem; font-weight:800; margin-top:10px; color:#ffffff;">
            ${c.t3Title}
          </h3>
          <p style="color:var(--muted); font-size:0.8rem; margin-top:8px; line-height:1.5;">
            ${c.t3Desc}
          </p>
          <ul class="price-list">
            ${c.t3Items.map((item) => `<li><span>—</span> <span>${item}</span></li>`).join("")}
          </ul>
        </div>
        <div style="display:flex; flex-direction:column; gap:7px;">
          <a class="btn" id="affTvBtn" href="/api/referral/redirect/tradingview?ticker=SPY" target="_blank" rel="noopener noreferrer" style="justify-content:center;">
            ${c.tvBtn}
          </a>
          <a class="btn" id="affSaBtn" href="/api/referral/redirect/seekingalpha?ticker=SPY" target="_blank" rel="noopener noreferrer" style="justify-content:center;">
            ${c.saBtn}
          </a>
          <a class="btn" id="affBrokerBtn" href="/api/referral/redirect/broker?ticker=SPY" target="_blank" rel="noopener noreferrer" style="justify-content:center; border-color:rgba(16,185,129,0.45); color:#34d399; font-weight:700;">
            ${c.brokerBtn} (${brokerName})
          </a>
          <button class="btn" id="btnOpenTelegramFromPricing" style="justify-content:center; border-color:rgba(56,189,248,0.4); color:#38bdf8;">
            ${c.tgBtn}
          </button>
          <div style="display:grid; grid-template-columns:1fr 1fr; gap:8px;">
            <a class="btn" id="pricingYoutubeBtn" href="${cfg.youtube_url || "https://youtube.com/@rightsidealpha"}" target="_blank" rel="noopener noreferrer" style="justify-content:center; border-color:rgba(239,68,68,0.4); color:#fca5a5;">
              📺 YouTube (@rightsidealpha) ↗
            </a>
            <a class="btn" id="pricingInstagramBtn" href="${cfg.instagram_url || "https://www.instagram.com/semifeargreed"}" target="_blank" rel="noopener noreferrer" style="justify-content:center; border-color:rgba(236,72,153,0.4); color:#f9a8d4;">
              📸 Instagram (@semifeargreed) ↗
            </a>
          </div>
        </div>
      </div>
    </section>
  `;
}
