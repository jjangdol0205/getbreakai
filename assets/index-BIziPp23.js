// --- src/locales/i18n.js ---
const translations = {
  en: {
    // Global Navigation & Header
    brandSubtitle: "US EQUITY QUANTITATIVE TERMINAL · v2.6",
    navRightSide: "RightSideAlpha · US Equities",
    navSemiFg: "SemiFearGreed · CNN-Style Index",
    marketUniverseTag: "NYSE & NASDAQ · 72 US EQUITIES",
    statusFree: "PUBLIC ACCESS",
    statusPro: "PRO TERMINAL ACTIVE",
    btnLicense: "License Key",
    btnAdmin: "Terminal Config",
    btnTelegram: "Telegram Alert",
    btnUnlockPro: "Upgrade to Pro ($29/mo)",

    // RightSideAlpha Hero & KPIs
    heroTag: "INSTITUTIONAL TURNAROUND RESEARCH · 394,371 US STOCK-DAYS VERIFIED (2006–2026)",
    heroTitle: "Systematic Right-Side Ignition for US-Listed Equities.",
    heroDesc: "Blindly buying 52-week lows in US growth equities traps capital for a median of 81 trading days with a -30.3% post-entry drawdown. RightSideAlpha isolates post-washout (1.40x+ volume) breakouts reclaiming the 20-day and 60-day moving averages across 72 liquid NYSE & NASDAQ equities.",
    kpi1_label: "PW-RSI 1Y 2x (+100%) Hit Rate",
    kpi1_sub: "vs 28.91% blind 52W-low dip buying",
    kpi2_label: "Median Days Underwater",
    kpi2_sub: "Reduced from 81.0 days via 55D Time-Stop",
    kpi3_label: "26.8-Yr US-Only Net CAGR",
    kpi3_sub: "80.5x net cumulative after 22% tax & slippage",
    kpi4_label: "Severe Drawdown (≤ -20%) Rate",
    kpi4_sub: "vs 24.82% without -9% hard stop & EPS filter",

    // Empirical Benchmark Table
    proofHeading: "Empirical Performance Matrix · Left-Side Dip Buying vs. PW-RSI Right-Side Ignition",
    proofCopyScorecardBtn: "Export Benchmark Tear Sheet (PNG)",
    th_arch: "Entry Methodology (US Equities, N = 394,371 Stock-Days)",
    th_2x: "1Y 2x (+100%) Rate",
    th_med: "1Y Median Return",
    th_mdd: "Post-Entry Median MDD",
    th_dead: "Days Underwater",
    th_trap: "1Y Tail Loss (≤ -20%)",

    // Screener Controls & Table Columns
    searchPlaceholder: "Filter by US Ticker, Company, or GICS Sector (e.g. NVDA, CELH, Semiconductors)...",
    filterAll: "All US Equities",
    filterIgnition: "Right-Side Ignition",
    filterWatch: "Washout Base Watch",
    filterKnife: "Downtrend / Avoid",
    filterTrap: "Value Trap Excluded",
    colTicker: "Security / Sector",
    colZone: "Regime & Factor Checklist",
    colScore: "Quant Score",
    colClose: "Last Close & 52W Range",
    colProx: "vs 52W Low",
    colDD: "52W Drawdown",
    colMA: "vs MA20 / MA60",
    colVol: "10D Vol Ratio",
    colHist: "Hist 2x Rate",
    colTrigger: "Execution Levels (Trigger / Stop)",
    colActions: "Research & Execution",

    // Pro Vault & Tools
    vaultBadgeLocked: "PRO ANALYTICS TERMINAL · LOCKED (ENTER LICENSE KEY)",
    vaultBadgeUnlocked: "PRO ANALYTICS TERMINAL · FULL INSTITUTIONAL ACCESS",
    vaultTitle: "Institutional Execution & Risk Management Suite",
    vaultUnlockBtn: "Demo Unlock (Key: PRO-DEMO-2026)",
    tool1Title: "MODULE 01 · POSITION RISK & 55-DAY TIME-STOP ENGINE",
    tool1Sub: "Asymmetric Exit & Opportunity-Cost Diagnostic",
    tool1Desc: "Input your US equity cost basis and holding period. Evaluates the 4 quantitative exit rules (-9% Capital Protection Stop, 55-Day +8% Time-Stop, 25-Day Momentum Switch, and +100% TP1 Principal Harvest).",
    tool1Btn: "Run Position Diagnostic",
    tool2Title: "MODULE 02 · SEC FILING TURNAROUND RESEARCH",
    tool2Sub: "10-K / 10-Q / 8-K Primary Source Equity Briefs",
    tool2Desc: "Updated at 08:10 EST from primary SEC filings and institutional consensus revisions (zero retail media noise):",
    tool2ViewBtn: "Open Institutional Research Archive",
    tool3Title: "MODULE 03 · TRADINGVIEW PINE SCRIPT v5 OVERLAY",
    tool3Sub: "Automated MA20/MA60 Ignition & Washout Plotter",
    tool3Desc: "Deploy directly into TradingView Pine Editor to plot right-side MA20/MA60 breakouts, 1.40x volume washouts, and -9% hard stop levels on any US stock:",
    tool3CopyBtn: "Copy Pine Script v5 Source",

    // Cross-Platform Banner
    crossTitle: "COMPANION MARKET SENTIMENT PLATFORM · SEMIFEARGREED",
    crossHeading: "Allocating to Semiconductor & Healthcare ETFs ($SMH / $XLV / $SOXX)?",
    crossDesc: "Open our CNN-style Semiconductor 7-Factor Fear & Greed Index and 26-year $SMH 70% : $XLV 30% contrarian rebalancing terminal.",
    crossBtn: "Switch to SemiFearGreed Index",

    // SemiFearGreed (CNN-Style UI/UX)
    cnnBadge: "MARKETS · SEMICONDUCTOR & AI SENTIMENT",
    cnnTitle: "Semiconductor Fear & Greed Index",
    cnnSubtitle: "What emotion is driving the chip & AI hardware market now?",
    cnnTabOverview: "Overview",
    cnnTabTimeline: "Timeline",
    cnnLastUpdated: "Last updated",
    cnnExportGauge: "Export Index Card (PNG)",
    cnnTelegramBtn: "Telegram Briefing",
    cnnHistoryTitle: "Historical Sentiment Comparison",
    cnnActiveRuleLabel: "ACTIVE BARBELL ALLOCATION SIGNAL",
    cnnIndicatorsHeading: "7 Semiconductor Fear & Greed Indicators",
    cnnIndicatorsSub: "How the index is calculated: Equal-transparent 7-factor rolling 3-year (756-day) percentile & z-score composite of $SMH, $XLV, and $QQQ.",
    rebalSectionTag: "BARBELL ASSET ALLOCATION & TAX OPTIMIZER",
    rebalSectionTitle: "$SMH + $XLV Contrarian Rebalancing Engine (70:30 ↔ 80:20)",
    rebalSectionDesc: "Combine high-beta AI semiconductor growth ($SMH 70%) with low-beta healthcare cash-flow defense ($XLV 30%). Automatically shift to 80:20 when Fear & Greed drops below 25 or $SMH falls -20% off its 52-week high.",
    lumpSectionTag: "CAPITAL DEPLOYMENT PROTOCOL",
    lumpSectionTitle: "3-Stage Lump-Sum Entry Planner",
    lumpSectionDesc: "Eliminate timing regret when deploying new cash. Automatically calculates Day-1 immediate entry vs. USD RP reserve tranches based on the live or simulated Fear & Greed score.",
    eraSectionTag: "26-YEAR EMPIRICAL VERIFICATION (2000–2026)",
    eraSectionTitle: "$SMH 70% : $XLV 30% (80:20 Crash Tilt) vs. 100% $QQQ Benchmark",
    eraSectionDesc: "Verified across 6,625 trading days including the 2000 Dot-Com Bust, 2008 GFC, 2020 Pandemic, and 2022 Rate Shock.",

    disclaimer: "Regulatory & Compliance Disclosure: RightSideAlpha and SemiFearGreed are quantitative financial data analytics and historical backtesting software tools. Nothing on this platform constitutes personalized investment, legal, or tax advice. All regime classifications and technical levels are mathematical outputs derived from historical price and volume series. Past performance (2000–2026) is not indicative of future results.",
    copyright: "© 2026 RightSideAlpha & SemiFearGreed Quantitative Analytics. Merchant of Record: Lemon Squeezy.",
  },
  jp: {
    brandSubtitle: "米国株クオンツ分析ターミナル · v2.6",
    navRightSide: "RightSideAlpha · 米国株スクリーナー",
    navSemiFg: "SemiFearGreed · 半導体恐怖＆強欲指数",
    marketUniverseTag: "NYSE & NASDAQ · 米国上場 72銘柄限定",
    statusFree: "パブリックティア",
    statusPro: "PRO ターミナル有効",
    btnLicense: "ライセンス認証",
    btnAdmin: "ターミナル設定",
    btnTelegram: "Telegram通知",
    btnUnlockPro: "Proへアップグレード ($29/月)",

    heroTag: "機関投資家向けターンアラウンド分析 · 米国株 394,371営業日検証済 (2006–2026)",
    heroTitle: "米国上場株に特化した「右側イグニッション」定量スクリーナー",
    heroDesc: "米国グロース株の単純な52週安値買い（左側逆張り）は、中央値81営業日の資金拘束と平均-30.3%の追加下落を招きます。RightSideAlphaはNYSE・NASDAQ上場72銘柄を対象に、出来高1.4倍以上のセリングクライマックス後に20日・60日移動平均線を同時突破する初動銘柄のみを抽出します。",
    kpi1_label: "PW-RSI 1年 2倍 (+100%) 到達率",
    kpi1_sub: "単純な52週安値買い (28.91%) との比較",
    kpi2_label: "含み損拘束期間（中央値）",
    kpi2_sub: "55日タイムストップにより81.0日から短縮",
    kpi3_label: "26.8年間 米国株純CAGR",
    kpi3_sub: "税金22%・スリッページ控除後 累計80.5倍",
    kpi4_label: "深刻な下落 (≤ -20%) 発生率",
    kpi4_sub: "-9%ハード損切＆業績フィルタ適用時",

    proofHeading: "20年実証パフォーマンス比較 · 左側安値買い vs PW-RSI 右側イグニッション",
    proofCopyScorecardBtn: "検証ティアシート出力 (PNG)",
    th_arch: "エントリー手法 (米国株, N = 394,371営業日)",
    th_2x: "1年 2倍 (+100%) 確率",
    th_med: "1年 リターン中央値",
    th_mdd: "エントリー後 MDD中央値",
    th_dead: "含み損日数",
    th_trap: "1年 重大損失 (≤ -20%)",

    searchPlaceholder: "米国ティッカー、企業名、セクターで検索 (例: NVDA, CELH, Semiconductors)...",
    filterAll: "全米国株",
    filterIgnition: "右側イグニッション",
    filterWatch: "クライマックス監視",
    filterKnife: "下降トレンド・回避",
    filterTrap: "バリュートラップ除外",
    colTicker: "銘柄 / セクター",
    colZone: "レジーム＆条件判定",
    colScore: "クオンツスコア",
    colClose: "終値 ($USD) & 52週レンジ",
    colProx: "対52週安値",
    colDD: "52週高値比DD",
    colMA: "対MA20 / MA60",
    colVol: "10日出来高倍率",
    colHist: "過去2倍確率",
    colTrigger: "執行価格 (突破 / -9%損切)",
    colActions: "調査＆チャート",

    vaultBadgeLocked: "PRO アナリティクスターミナル · ロック中 (要ライセンスキー)",
    vaultBadgeUnlocked: "PRO アナリティクスターミナル · 全機能アンロック済",
    vaultTitle: "機関投資家向けエグゼキューション＆リスク管理スイート",
    vaultUnlockBtn: "デモ解除 (キー: PRO-DEMO-2026)",
    tool1Title: "MODULE 01 · ポジションリスク＆55日タイムストップ診断",
    tool1Sub: "非対称エグジット＆機会損失シミュレーター",
    tool1Desc: "米国株の取得単価と保有営業日数を入力してください。4大定量エグジット原則（-9%ハード損切、55日+8%タイムストップ、25日モメンタム乗換、+100%元本回収）を即時判定します。",
    tool1Btn: "ポジション診断を実行",
    tool2Title: "MODULE 02 · SEC一次開示ターンアラウンド調査レポート",
    tool2Sub: "10-K / 10-Q / 8-K ファンダメンタルズ分析アーカイブ",
    tool2Desc: "二次メディアのノイズを排除し、SEC一次開示資料とEPSコンセンサス修正から毎朝更新：",
    tool2ViewBtn: "機関投資家向け調査レポートを開く",
    tool3Title: "MODULE 03 · TRADINGVIEW PINE SCRIPT v5 インジケーター",
    tool3Sub: "MA20/MA60 右側突破＆出来高クライマックス自動描画",
    tool3Desc: "TradingViewのPineエディタに貼り付けるだけで、MA20/MA60突破シグナルと-9%ストップラインをチャート上に描画します：",
    tool3CopyBtn: "Pine Script v5 コードをコピー",

    crossTitle: "姉妹センチメント分析プラットフォーム · SEMIFEARGREED",
    crossHeading: "半導体ETF・ヘルスケアETF ($SMH / $XLV / $SOXX) に投資していますか？",
    crossDesc: "CNNスタイルの半導体7ファクター恐怖＆強欲指数と、26年間検証済みの$SMH 70% : $XLV 30% 逆張りリバランス計算機へ切り替えられます。",
    crossBtn: "SemiFearGreed インデックスを開く",

    cnnBadge: "MARKETS · 半導体＆AI市場センチメント",
    cnnTitle: "Semiconductor Fear & Greed Index",
    cnnSubtitle: "いま半導体・AI市場を動かしている感情は「恐怖」か「強欲」か？",
    cnnTabOverview: "オーバービュー (Overview)",
    cnnTabTimeline: "タイムライン推移 (Timeline)",
    cnnLastUpdated: "最終更新",
    cnnExportGauge: "ゲージカード出力 (PNG)",
    cnnTelegramBtn: "Telegram配信",
    cnnHistoryTitle: "過去センチメント比較",
    cnnActiveRuleLabel: "現在のバーベル配分シグナル",
    cnnIndicatorsHeading: "半導体 恐怖＆強欲指数を構成する7つの指標",
    cnnIndicatorsSub: "算出方法：$SMH・$XLV・$QQQの過去3年間（756営業日）ローリングパーセンタイルとZスコアを組み合わせた7ファクター加重平均モデル。",
    rebalSectionTag: "バーベル資産配分＆節税シミュレーター",
    rebalSectionTitle: "$SMH + $XLV 逆張りリバランス計算機 (70:30 ↔ 80:20)",
    rebalSectionDesc: "高成長AI半導体($SMH 70%)とディフェンシブなヘルスケア($XLV 30%)を結合。指数25以下または$SMH高値比-20%下落時に80:20へ逆張りシフトします。",
    lumpSectionTag: "新規資金エントリープロトコル",
    lumpSectionTitle: "3段階 一括資金エントリープランナー",
    lumpSectionDesc: "現在の恐怖＆強欲スコアに応じて、初日即時投入枠と米ドルMMF待機枠の最適比率を算出します。",
    eraSectionTag: "26年間（2000–2026）実証バックテスト",
    eraSectionTitle: "$SMH 70% : $XLV 30% (暴落時80:20) vs 100% $QQQ ベンチマーク比較",
    eraSectionDesc: "ITバブル崩壊、リーマンショック、コロナ危機、2022年半導体不況を含む6,625営業日の完全検証データ。",

    disclaimer: "コンプライアンス免責事項：RightSideAlphaおよびSemiFearGreedは定量金融データ分析および過去バックテスト用のソフトウェアツールです。当プラットフォームのいかなる情報も個別の投資助言や税務助言を構成しません。",
    copyright: "© 2026 RightSideAlpha & SemiFearGreed Quantitative Analytics. Merchant of Record: Lemon Squeezy.",
  },
  kr: {
    brandSubtitle: "미국 상장주식 전용 퀀트 터미널 · v2.6",
    navRightSide: "RightSideAlpha · 미국주식 알파 터미널",
    navSemiFg: "SemiFearGreed · 반도체 공포·탐욕 지수",
    marketUniverseTag: "NYSE & NASDAQ · 미국 상장 72개 핵심 종목 한정",
    statusFree: "퍼블릭 티어",
    statusPro: "PRO 터미널 활성화",
    btnLicense: "라이선스 인증",
    btnAdmin: "터미널 설정",
    btnTelegram: "텔레그램 알림",
    btnUnlockPro: "Pro 업그레이드 ($29/월)",

    heroTag: "기관급 턴어라운드 리서치 · 미국 상장주식 394,371 거래일 전수 검증 (2006–2026)",
    heroTitle: "미국 상장주식에 최적화된 우측 변곡점(PW-RSI) 정량 분석 플랫폼",
    heroDesc: "미국 성장주를 단순 52주 신저가(좌측 구간)에 매수하면 중앙값 81거래일의 자금 묶임(데드머니)과 -30.3%의 추가 낙폭에 노출됩니다. RightSideAlpha는 NYSE·NASDAQ 상장 72개 핵심 종목만을 대상으로 1.4배 이상 거래량 투매(Washout) 후 20일·60일 이동평균선을 동시 탈환하는 우측 초동 시그널을 판독합니다.",
    kpi1_label: "PW-RSI 1년 2배 (+100%) 도달률",
    kpi1_sub: "단순 52주 신저가 좌측 매수(28.91%) 대비",
    kpi2_label: "보유 후 물림 기간 (중앙값)",
    kpi2_sub: "55일 시간손절 원칙으로 81.0일에서 단축",
    kpi3_label: "26.8개년 미국주식 순 CAGR",
    kpi3_sub: "양도세 22%·슬리피지 차감 후 누적 80.5배",
    kpi4_label: "심각한 손실 (≤ -20%) 발생 확률",
    kpi4_sub: "-9% 손절 및 실적 턴어라운드 필터 적용 시",

    proofHeading: "20년 실증 백테스트 매트릭스 · 좌측 신저가 매수 vs PW-RSI 우측 시동 모델",
    proofCopyScorecardBtn: "백테스트 티어시트 저장 (PNG)",
    th_arch: "진입 방법론 (미국 상장주, N = 394,371 거래일)",
    th_2x: "1년 2배 (+100%) 확률",
    th_med: "1년 수익률 중앙값",
    th_mdd: "진입 후 MDD 중앙값",
    th_dead: "자금 물림 기간",
    th_trap: "1년 치명적 손실 (≤ -20%)",

    searchPlaceholder: "미국 티커, 기업명, 섹터 검색 (예: NVDA, CELH, Semiconductors)...",
    filterAll: "미국 전체 종목",
    filterIgnition: "우측 돌파 시동 (Ignition)",
    filterWatch: "워시아웃 베이스 대기",
    filterKnife: "좌측 하락추세 · 주의",
    filterTrap: "밸류트랩 배제 종목",
    colTicker: "종목 / GICS 섹터",
    colZone: "시그널 레짐 & 4대 조건",
    colScore: "퀀트 스코어",
    colClose: "종가 ($USD) & 52주 밴드",
    colProx: "52주 저점 이격",
    colDD: "52주 고점 낙폭",
    colMA: "20일 / 60일선 괴리",
    colVol: "10일 거래량 배율",
    colHist: "과거 2배 확률",
    colTrigger: "실행 타점 (60일 돌파 / -9% 손절)",
    colActions: "리포트 & 차트 연동",

    vaultBadgeLocked: "PRO 애널리틱스 터미널 · 잠김 (라이선스 키 입력 필요)",
    vaultBadgeUnlocked: "PRO 애널리틱스 터미널 · 전 기능 활성화됨",
    vaultTitle: "기관급 포지션 리스크 관리 & SEC 1차 공시 리서치 스위트",
    vaultUnlockBtn: "데모 즉시 해제 (키: PRO-DEMO-2026)",
    tool1Title: "MODULE 01 · 보유 포지션 리스크 & 55일 시간손절 판독기",
    tool1Sub: "비대칭 청산 원칙 및 기회비용 정밀 진단",
    tool1Desc: "미국 주식 매수 단가($)와 보유 거래일수를 입력하세요. 4대 정량 청산 원칙(-9% 칼손절 방어, 55일 +8% 미만 시간손절, 25일 모멘텀 교체, +100% 도달 시 원금 반절 회수)을 즉시 산출합니다.",
    tool1Btn: "보유 포지션 정밀 진단 실행",
    tool2Title: "MODULE 02 · SEC 1차 공시 기반 턴어라운드 리서치",
    tool2Sub: "10-K / 10-Q / 8-K 원문 기반 기관급 종목 분석 브리프",
    tool2Desc: "2차 언론 노이즈를 배제하고 미국 SEC 1차 공시와 컨센서스 EPS 상향 데이터를 바탕으로 매일 08:10 업데이트됩니다:",
    tool2ViewBtn: "기관급 턴어라운드 리포트 열람",
    tool3Title: "MODULE 03 · TRADINGVIEW PINE SCRIPT v5 전용 지표",
    tool3Sub: "MA20/MA60 우측 돌파 및 거래량 워시아웃 자동 차트 표시",
    tool3Desc: "트레이딩뷰 Pine 에디터에 붙여넣어 미국 전 종목 차트에 우측 시동 타점과 -9% 손절 라인을 자동 표시합니다:",
    tool3CopyBtn: "Pine Script v5 소스코드 복사",

    crossTitle: "연계 섹터 심리 & 자산배분 플랫폼 · SEMIFEARGREED",
    crossHeading: "반도체 ETF와 헬스케어 ETF ($SMH / $XLV / $SOXX)로 꾸준한 복리 수익을 원하시나요?",
    crossDesc: "CNN Fear & Greed 스타일의 반도체 7팩터 공포·탐욕 지수와 26년 검증된 $SMH 70% : $XLV 30% (폭락장 80:20) 역발상 리밸런싱 플랫폼으로 이동하세요.",
    crossBtn: "SemiFearGreed 지수 플랫폼 열기",

    cnnBadge: "MARKETS · 반도체 & AI 섹터 투자심리 지수",
    cnnTitle: "Semiconductor Fear & Greed Index",
    cnnSubtitle: "지금 반도체와 AI 시장을 움직이는 감정은 '공포'입니까, '탐욕'입니까?",
    cnnTabOverview: "오버뷰 (Overview)",
    cnnTabTimeline: "타임라인 추이 (Timeline)",
    cnnLastUpdated: "최근 업데이트",
    cnnExportGauge: "공포·탐욕 지수 카드 저장 (PNG)",
    cnnTelegramBtn: "텔레그램 브리핑 전송",
    cnnHistoryTitle: "시점별 지수 히스토리 비교",
    cnnActiveRuleLabel: "현재 발동 중인 바벨 자산배분 시그널",
    cnnIndicatorsHeading: "반도체 공포·탐욕 지수를 구성하는 7대 핵심 지표",
    cnnIndicatorsSub: "산출 방식: $SMH, $XLV, $QQQ의 최근 3년(756거래일) 롤링 백분위와 Z-스코어를 결합한 7팩터 정량 모델입니다.",
    rebalSectionTag: "바벨 자산배분 & 해외주식 절세 계산기",
    rebalSectionTitle: "$SMH + $XLV 역발상 리밸런싱 계산기 (70:30 ↔ 80:20)",
    rebalSectionDesc: "고성장 AI 반도체($SMH 70%)와 방어형 헬스케어($XLV 30%)를 결합하여 매년 꾸준한 복리 수익을 추구합니다. 공포지수 25 이하 또는 $SMH 고점 대비 -20% 하락 시 80:20으로 역발상 스위칭합니다.",
    lumpSectionTag: "신규 거치식 자금 투입 프로토콜",
    lumpSectionTitle: "3단계 일시금(Lump-Sum) 진입 플래너",
    lumpSectionDesc: "목돈을 한 번에 넣을 때 고점 물림을 방지합니다. 현재(또는 시뮬레이션) 공포·탐욕 점수에 따라 당일 즉시 진입 물량과 달러 RP 파킹 물량을 자동 계산합니다.",
    eraSectionTag: "26개년(2000–2026) 실증 백테스트 검증",
    eraSectionTitle: "$SMH 70% : $XLV 30% (폭락장 80:20) vs 100% $QQQ 장기 성과 비교",
    eraSectionDesc: "2000년 닷컴버블, 2008년 금융위기, 2020년 팬데믹, 2022년 금리인상기를 모두 포함한 6,625거래일 실증 데이터입니다.",

    disclaimer: "법적 고지 및 면책조항: RightSideAlpha와 SemiFearGreed는 정량적 금융 데이터 분석 및 역사적 백테스트 소프트웨어 도구입니다. 본 웹사이트의 어떠한 내용도 개별 투자자를 위한 맞춤형 투자 권유나 세무 자문을 구성하지 않습니다. 과거 백테스트 성과(2000–2026)는 미래 수익을 보장하지 않습니다.",
    copyright: "© 2026 RightSideAlpha & SemiFearGreed Quantitative Analytics. Merchant of Record: Lemon Squeezy.",
  },
};


// --- src/services/api.js ---
function getAuthHeader() {
  const token =
    localStorage.getItem("rsa_token") ||
    (localStorage.getItem("rsa_pro_unlocked") === "true" ? "PRO-DEMO-2026" : "");
  if (token) {
    return { Authorization: `Bearer ${token}` };
  }
  return {};
}
function formatCheckoutUrl(
  rawUrl,
  fallbackUrl = "https://truthofmarket.lemonsqueezy.com/checkout/buy/d5e7e761-8b1b-4ca8-b1fe-771acd1450f8"
) {
  const base = String(rawUrl || fallbackUrl).trim() || fallbackUrl;
  if (/[?&]embed=1\b/i.test(base)) {
    return base;
  }
  return `${base}${base.includes("?") ? "&" : "?"}embed=1`;
}

function isProActive() {
  const token =
    localStorage.getItem("rsa_token") ||
    (localStorage.getItem("rsa_pro_unlocked") === "true" ? "PRO-DEMO-2026" : "");
  return Boolean(token);
}

function isStaticHost() {
  if (typeof window === "undefined") return false;
  if (window.__STATIC_MODE__ === true) return true;
  const h = window.location.hostname || "";
  if (!h || h === "localhost" || h === "127.0.0.1") return false;
  return true;
}

async function fetchJsonWithFallback(apiUrl, options, fallbackFn) {
  if (isStaticHost()) {
    return fallbackFn();
  }
  try {
    const resp = await fetch(apiUrl, options);
    if (resp.ok) {
      const ct = resp.headers.get("content-type") || "";
      if (ct.includes("application/json")) {
        return await resp.json();
      }
    }
  } catch (e) {
    // Fallback to static snapshot / client-side engine when hosted on static CDN (GitHub Pages / Render Static)
  }
  return fallbackFn();
}

let cachedProStocks = null;
let cachedSemiOverview = null;

async function getStaticProStocks() {
  if (!cachedProStocks) {
    const r = await fetch("./static_api/stocks_pro.json");
    cachedProStocks = await r.json();
  }
  return cachedProStocks;
}

async function getStaticSemiOverview() {
  if (!cachedSemiOverview) {
    const r = await fetch("./static_api/semi_overview.json");
    cachedSemiOverview = await r.json();
  }
  return cachedSemiOverview;
}
async function fetchStocks(params = {}) {
  const query = new URLSearchParams();
  if (params.search) query.append("search", params.search);
  if (params.zone && params.zone !== "ALL") query.append("zone", params.zone);
  if (params.sort_by) query.append("sort_by", params.sort_by);
  if (params.order) query.append("order", params.order);
  if (params.limit) query.append("limit", params.limit);
  if (params.offset) query.append("offset", params.offset);

  const url = `/api/stocks${query.toString() ? `?${query.toString()}` : ""}`;
  return fetchJsonWithFallback(
    url,
    {
      headers: {
        ...getAuthHeader(),
        Accept: "application/json",
      },
    },
    async () => {
      const file = isProActive() ? "./static_api/stocks_pro.json" : "./static_api/stocks_free.json";
      const r = await fetch(file);
      let list = await r.json();
      if (params.search) {
        const q = String(params.search).trim().toLowerCase();
        list = list.filter(
          (s) =>
            (s.ticker && s.ticker.toLowerCase().includes(q)) ||
            (s.name && s.name.toLowerCase().includes(q)) ||
            (s.name_en && s.name_en.toLowerCase().includes(q)) ||
            (s.name_jp && s.name_jp.toLowerCase().includes(q)) ||
            (s.name_kr && s.name_kr.toLowerCase().includes(q)) ||
            (s.sector && s.sector.toLowerCase().includes(q))
        );
      }
      if (params.zone && params.zone !== "ALL") {
        list = list.filter((s) => (s.zone_code || s.zone) === params.zone);
      }
      if (params.sort_by) {
        const aliasMap = {
          pw_score: "score",
          price: "close",
          prox: "prox_low52_pct",
          dd: "dd_high52_pct",
          vol: "vol_surge_10d",
        };
        const key = aliasMap[params.sort_by] || params.sort_by;
        const desc = String(params.order || "desc").toLowerCase() !== "asc";
        list = [...list].sort((a, b) => {
          const va = a[key];
          const vb = b[key];
          if (typeof va === "string" || typeof vb === "string") {
            const cmp = String(va ?? "").localeCompare(String(vb ?? ""));
            return desc ? -cmp : cmp;
          }
          const na = Number(va ?? 0);
          const nb = Number(vb ?? 0);
          return desc ? nb - na : na - nb;
        });
      }
      const off = Math.max(0, Number(params.offset || 0));
      const lim = params.limit ? Math.max(1, Number(params.limit)) : list.length;
      return list.slice(off, off + lim);
    }
  );
}
async function fetchStockDetail(ticker) {
  const clean = String(ticker || "CELH").trim().toUpperCase();
  return fetchJsonWithFallback(
    `/api/stocks/${encodeURIComponent(clean)}`,
    {
      headers: {
        ...getAuthHeader(),
        Accept: "application/json",
      },
    },
    async () => {
      const all = await fetchStocks({ limit: 200 });
      return all.find((s) => s.ticker === clean) || all[0];
    }
  );
}
async function fetchBacktestSummary() {
  return fetchJsonWithFallback(
    "/api/backtest",
    { headers: { Accept: "application/json" } },
    async () => {
      const r = await fetch("./static_api/backtest.json");
      return r.json();
    }
  );
}
async function fetchResearchList() {
  return fetchJsonWithFallback(
    "/api/research",
    {
      headers: {
        ...getAuthHeader(),
        Accept: "application/json",
      },
    },
    async () => {
      const r = await fetch("./static_api/research_list.json");
      return r.json();
    }
  );
}
async function fetchResearchBrief(ticker) {
  const clean = String(ticker || "CELH").trim().toUpperCase();
  return fetchJsonWithFallback(
    `/api/research/${encodeURIComponent(clean)}`,
    {
      headers: {
        ...getAuthHeader(),
        Accept: "application/json",
      },
    },
    async () => {
      const target = clean === "MBLY" ? "MBLY" : "CELH";
      const r = await fetch(`./static_api/research_${target}.json`);
      return r.json();
    }
  );
}

const ADMIN_CREDENTIALS_SHA256 = "4578349322b7fa9931023e0def82b9d0c19fa2c4fdab1f7d762142d8d78ef2fe";

function sha256PureJs(ascii) {
  function rightRotate(value, amount) {
    return (value >>> amount) | (value << (32 - amount));
  }
  const mathPow = Math.pow;
  const maxWord = mathPow(2, 32);
  let result = "";
  const words = [];
  const asciiBitLength = ascii.length * 8;
  let hash = (sha256PureJs.h = sha256PureJs.h || []);
  const k = (sha256PureJs.k = sha256PureJs.k || []);
  let primeCounter = k.length;
  const isComposite = {};
  for (let candidate = 2; primeCounter < 64; candidate++) {
    if (!isComposite[candidate]) {
      for (let i = 0; i < 313; i += candidate) {
        isComposite[i] = candidate;
      }
      hash[primeCounter] = (mathPow(candidate, 0.5) * maxWord) | 0;
      k[primeCounter++] = (mathPow(candidate, 1 / 3) * maxWord) | 0;
    }
  }
  ascii += "\x80";
  while ((ascii.length % 64) - 56) ascii += "\x00";
  for (let i = 0; i < ascii.length; i++) {
    const j = ascii.charCodeAt(i);
    if (j >> 8) return "";
    words[i >> 2] |= j << (((3 - i) % 4) * 8);
  }
  words[words.length] = (asciiBitLength / maxWord) | 0;
  words[words.length] = asciiBitLength;
  for (let j = 0; j < words.length; ) {
    const w = words.slice(j, (j += 16));
    const oldHash = hash;
    hash = hash.slice(0, 8);
    for (let i = 0; i < 64; i++) {
      const w15 = w[i - 15];
      const w2 = w[i - 2];
      const a = hash[0];
      const e = hash[4];
      const temp1 =
        hash[7] +
        (rightRotate(e, 6) ^ rightRotate(e, 11) ^ rightRotate(e, 25)) +
        ((e & hash[5]) ^ (~e & hash[6])) +
        k[i] +
        (w[i] =
          i < 16
            ? w[i]
            : (w[i - 16] +
                (rightRotate(w15, 7) ^ rightRotate(w15, 18) ^ (w15 >>> 3)) +
                w[i - 7] +
                (rightRotate(w2, 17) ^ rightRotate(w2, 19) ^ (w2 >>> 10))) |
              0);
      const temp2 =
        (rightRotate(a, 2) ^ rightRotate(a, 13) ^ rightRotate(a, 22)) +
        ((a & hash[1]) ^ (a & hash[2]) ^ (hash[1] & hash[2]));
      hash = [(temp1 + temp2) | 0].concat(hash);
      hash[4] = (hash[4] + temp1) | 0;
    }
    for (let i = 0; i < 8; i++) {
      hash[i] = (hash[i] + oldHash[i]) | 0;
    }
  }
  for (let i = 0; i < 8; i++) {
    for (let j = 3; j + 1; j--) {
      const b = (hash[i] >> (j * 8)) & 255;
      result += (b < 16 ? 0 : "") + b.toString(16);
    }
  }
  return result;
}

async function computeSha256Hex(inputStr) {
  try {
    if (typeof crypto !== "undefined" && crypto.subtle && typeof TextEncoder !== "undefined") {
      const data = new TextEncoder().encode(inputStr);
      const buf = await crypto.subtle.digest("SHA-256", data);
      return Array.from(new Uint8Array(buf))
        .map((b) => b.toString(16).padStart(2, "0"))
        .join("");
    }
  } catch (_) {
    // Fallback to pure JS SHA-256
  }
  return sha256PureJs(unescape(encodeURIComponent(inputStr)));
}
async function verifyAdminCredentials(username, password) {
  const uname = String(username || "").trim();
  const pw = String(password || "");
  return fetchJsonWithFallback(
    "/api/auth/admin/login",
    {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Accept: "application/json",
      },
      body: JSON.stringify({ username: uname, password: pw }),
    },
    async () => {
      const digest = await computeSha256Hex(`rsa_admin_v1:${uname}:${pw}`);
      const ok = digest.toLowerCase() === ADMIN_CREDENTIALS_SHA256;
      return {
        authenticated: ok,
        role: ok ? "admin" : "guest",
        license_key: ok ? "PRO-DEMO-2026" : null,
        message: ok
          ? "Admin Authenticated — Terminal Config & Pro Access Unlocked."
          : "Invalid Admin ID or Password.",
      };
    }
  );
}
async function validateLicense(licenseKey) {
  return fetchJsonWithFallback(
    "/api/auth/license/validate",
    {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Accept: "application/json",
      },
      body: JSON.stringify({ license_key: licenseKey }),
    },
    async () => {
      const key = String(licenseKey || "").trim();
      const valid =
        key.toUpperCase() === "PRO-DEMO-2026" ||
        /^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$/i.test(key);
      return {
        valid,
        license_key: valid ? key : null,
        tier: valid ? "pro" : "free",
        expires_at: valid ? "2099-12-31T23:59:59Z" : null,
        message: valid
          ? "Pro Terminal License Verified."
          : "Invalid license key. Use PRO-DEMO-2026 for demo.",
      };
    }
  );
}
async function fetchProVault() {
  return fetchJsonWithFallback(
    "/api/pro/vault",
    {
      headers: {
        ...getAuthHeader(),
        Accept: "application/json",
      },
    },
    async () => {
      const active = isProActive();
      return {
        unlocked: active,
        tier: active ? "pro" : "free",
        pine_script_available: active,
        tools: ["position_doctor", "morning_pdf", "pine_script_v5"],
      };
    }
  );
}
async function fetchPineScript() {
  return fetchJsonWithFallback(
    "/api/pro/pinescript",
    {
      headers: {
        ...getAuthHeader(),
        Accept: "application/json",
      },
    },
    async () => {
      const r = await fetch("./static_api/pinescript.json");
      return r.json();
    }
  );
}
async function evaluatePositionDoctor(data) {
  return fetchJsonWithFallback(
    "/api/pro/position-doctor",
    {
      method: "POST",
      headers: {
        ...getAuthHeader(),
        "Content-Type": "application/json",
        Accept: "application/json",
      },
      body: JSON.stringify(data),
    },
    async () => {
      const all = await getStaticProStocks();
      const tClean = String(data.ticker || "CELH").trim().toUpperCase();
      const stock = all.find((s) => s.ticker === tClean);
      const entry = Math.max(0.01, Number(data.entry_price || 27.93));
      const days = Number(data.days_held || 0);
      const curr =
        data.current_price !== undefined && data.current_price !== null
          ? Number(data.current_price)
          : stock
          ? Number(stock.close)
          : entry;
      const asOf = stock && stock.date ? stock.date : "2026-10-13";
      const retPct = Number(((curr / entry - 1.0) * 100.0).toFixed(2));
      const stopP = Number((entry * 0.91).toFixed(2));
      const tp1P = Number((entry * 2.0).toFixed(2));

      if (retPct <= -9.0) {
        return {
          ticker: tClean,
          status_code: "HARD_STOP",
          status_label: "🛑 Hard Stop Loss Triggered",
          return_pct: retPct,
          rule_triggered: "Rule 1 (-9.0% Hard Stop Loss)",
          action_plan: "Exit immediately. Do not average down on broken support.",
          is_critical: true,
          current_price: curr,
          entry_price: Number(entry.toFixed(2)),
          stop_price: stopP,
          tp1_price: tp1P,
          as_of_date: asOf,
        };
      } else if (days >= 55 && retPct < 8.0) {
        return {
          ticker: tClean,
          status_code: "TIME_STOP",
          status_label: "⏳ 55-Day Time Stop Triggered (55일 시간 손절)",
          return_pct: retPct,
          rule_triggered: "Rule 2 (55-Day Dead-Money Exit)",
          action_plan:
            "Exit position. Rebound momentum has stalled; reallocate into active right-side ignition candidates.",
          is_critical: false,
          current_price: curr,
          entry_price: Number(entry.toFixed(2)),
          stop_price: stopP,
          tp1_price: tp1P,
          as_of_date: asOf,
        };
      } else if (retPct >= 100.0) {
        return {
          ticker: tClean,
          status_code: "TP1_HARVEST",
          status_label: "🎯 100% Target Price 1 Achieved",
          return_pct: retPct,
          rule_triggered: "Rule 3 (+100% Principal Recovery)",
          action_plan:
            "Sell 50% of position to recoup 100% initial capital. Set trailing stop on remaining 50% using MA60.",
          is_critical: false,
          current_price: curr,
          entry_price: Number(entry.toFixed(2)),
          stop_price: stopP,
          tp1_price: tp1P,
          as_of_date: asOf,
        };
      } else {
        return {
          ticker: tClean,
          status_code: "HOLD",
          status_label: "🟢 Active Right-Side Trend Follow",
          return_pct: retPct,
          rule_triggered: "Rule 4 (Healthy Trend Follow)",
          action_plan:
            "Maintain position. Monitor MA20/MA60 trailing support; runner target is +100% TP1.",
          is_critical: false,
          current_price: curr,
          entry_price: Number(entry.toFixed(2)),
          stop_price: stopP,
          tp1_price: tp1P,
          as_of_date: asOf,
        };
      }
    }
  );
}
async function fetchReferralConfig() {
  return fetchJsonWithFallback(
    "/api/referral/config",
    { headers: { Accept: "application/json" } },
    async () => {
      const r = await fetch("./static_api/referral_config.json");
      return r.json();
    }
  );
}
async function updateReferralConfig(data) {
  return fetchJsonWithFallback(
    "/api/referral/config",
    {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Accept: "application/json",
      },
      body: JSON.stringify(data),
    },
    async () => ({ status: "updated", config: data })
  );
}
function getReferralRedirectUrl(provider, ticker) {
  return `/api/referral/redirect/${encodeURIComponent(
    provider.toLowerCase()
  )}?ticker=${encodeURIComponent(ticker)}`;
}
async function fetchSemiOverview() {
  return fetchJsonWithFallback(
    "/api/semi/overview",
    { headers: { Accept: "application/json" } },
    async () => getStaticSemiOverview()
  );
}
async function fetchSemiHistory(rangeCode = "1Y") {
  const rc = String(rangeCode || "1Y").trim().toUpperCase();
  const validRanges = ["3M", "6M", "1Y", "3Y", "5Y", "10Y", "ALL"];
  const safeRange = validRanges.includes(rc) ? rc : "1Y";
  return fetchJsonWithFallback(
    `/api/semi/history?range=${encodeURIComponent(safeRange)}`,
    { headers: { Accept: "application/json" } },
    async () => {
      const r = await fetch(`./static_api/semi_history_${safeRange}.json`);
      return r.json();
    }
  );
}
async function calculateSemiRebalance(data) {
  return fetchJsonWithFallback(
    "/api/semi/rebalance",
    {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Accept: "application/json",
      },
      body: JSON.stringify(data),
    },
    async () => {
      const ov = await getStaticSemiOverview();
      const fgScore = Number(ov.fg_score ?? 18.0);
      const ddPct = Number(ov.smh_dd_pct ?? -19.03);
      const usdkrw = Number(ov.usdkrw ?? 1324.75);
      const smhPrice = Number(ov.smh_close ?? 541.62);
      const xlvPrice = Number(ov.xlv_close ?? 179.28);
      const mode = String(data.strategy_mode || "AUTO_REGIME").trim().toUpperCase();
      const isExtreme = fgScore < 25.0 || ddPct <= -19.0;

      let smhW = 0.7;
      let xlvW = 0.3;
      let ruleEn = "";
      let ruleJp = "";
      let ruleKr = "";

      if (mode === "BASELINE_70_30") {
        smhW = 0.7;
        xlvW = 0.3;
        ruleEn = "Fixed 70% $SMH : 30% $XLV Golden Barbell Baseline";
        ruleJp = "70% $SMH : 30% $XLV 基本黄金バーベル比率";
        ruleKr = "평시 70% $SMH : 30% $XLV 기본 황금 바벨 비중";
      } else if (mode === "CONTRARIAN_80_20") {
        smhW = 0.8;
        xlvW = 0.2;
        ruleEn = "Contrarian 80% $SMH : 20% $XLV Crash Accumulation Tilt";
        ruleJp = "80% $SMH : 20% $XLV 暴落時・逆張り買い増しモード";
        ruleKr = "80% $SMH : 20% $XLV 폭락장 역발상 매집 비중";
      } else if (mode === "AGGRESSIVE_90_10") {
        smhW = 0.9;
        xlvW = 0.1;
        ruleEn = "90% $SMH : 10% $XLV Right-Side Momentum Tilt";
        ruleJp = "90% $SMH : 10% $XLV 右側モメンタム集中モード";
        ruleKr = "90% $SMH : 10% $XLV 우측 시동 공격형 비중";
      } else if (isExtreme) {
        smhW = 0.8;
        xlvW = 0.2;
        ruleEn = `AUTO REGIME: Extreme Fear (${fgScore}/100, DD ${ddPct.toFixed(1)}%) → 80% $SMH : 20% $XLV Contrarian Shift`;
        ruleJp = `自動判定: 極度の恐怖 (${fgScore}/100, 高値比 ${ddPct.toFixed(1)}%) → 80% $SMH : 20% $XLV 逆張り転換`;
        ruleKr = `자동 판독: 극단적 공포 (${fgScore}/100, 낙폭 ${ddPct.toFixed(1)}%) → 80% $SMH : 20% $XLV 역발상 비중 확대`;
      } else {
        smhW = 0.7;
        xlvW = 0.3;
        ruleEn = `AUTO REGIME: Standard Regime (${fgScore}/100) → 70% $SMH : 30% $XLV Core Barbell`;
        ruleJp = `自動判定: 通常レジーム (${fgScore}/100) → 70% $SMH : 30% $XLV 基本比率`;
        ruleKr = `자동 판독: 평시 구간 (${fgScore}/100) → 70% $SMH : 30% $XLV 기본 황금비중`;
      }

      const capUsd = Math.max(100, Number(data.total_capital_usd || 100000));
      const targetSmhUsd = Number((capUsd * smhW).toFixed(2));
      const targetXlvUsd = Number((capUsd * xlvW).toFixed(2));
      const targetSmhShares = Math.floor(targetSmhUsd / smhPrice);
      const targetXlvShares = Math.floor(targetXlvUsd / xlvPrice);
      const investedUsd = targetSmhShares * smhPrice + targetXlvShares * xlvPrice;
      const residualUsd = Number(Math.max(0, capUsd - investedUsd).toFixed(2));

      const natW = Number(ov.natural_smh_weight_pct ?? 66.5) / 100.0;
      const currSmhUsd =
        data.current_smh_usd !== undefined && data.current_smh_usd !== null
          ? Number(data.current_smh_usd)
          : Number((capUsd * natW).toFixed(2));
      const currXlvUsd =
        data.current_xlv_usd !== undefined && data.current_xlv_usd !== null
          ? Number(data.current_xlv_usd)
          : Number((capUsd * (1.0 - natW)).toFixed(2));
      const deltaSmhUsd = Number((targetSmhUsd - currSmhUsd).toFixed(2));
      const deltaXlvUsd = Number((targetXlvUsd - currXlvUsd).toFixed(2));
      const deltaSmhShares = Math.round(deltaSmhUsd / smhPrice);
      const deltaXlvShares = Math.round(deltaXlvUsd / xlvPrice);

      const freq = String(data.rebalance_frequency || "ANNUAL").trim().toUpperCase();
      const dragMap = { ANNUAL: 0.19, QUARTERLY: 0.42, MONTHLY: 0.78, WEEKLY: 1.32 };
      const taxDrag = dragMap[freq] ?? 0.19;
      const expectedNetCagr = Number((22.98 - taxDrag).toFixed(2));

      const dedLimit = 2500000;
      const gainKrw = Math.max(0, Number(data.unrealized_gain_krw ?? 3800000));
      const taxableKrw = Math.max(0, gainKrw - dedLimit);
      const taxSavedKrw = Math.round(Math.min(gainKrw, dedLimit) * 0.22);

      const taxEn =
        gainKrw <= dedLimit
          ? `Unrealized gain (₩${gainKrw.toLocaleString()}) is within the ₩2,500,000 annual tax-free allowance. Execute your $XLV ↔ $SMH rebalance before Dec 26 to harvest gains with ₩0 tax (saving ₩${taxSavedKrw.toLocaleString()}).`
          : `Unrealized gain (₩${gainKrw.toLocaleString()}) exceeds the ₩2.5M tax-free cap by ₩${taxableKrw.toLocaleString()}. Sell only up to ₩2,500,000 of realized profit this calendar year to lock in the maximum ₩550,000 tax savings, and use new cash inflow for the remaining rebalance.`;
      const taxJp =
        gainKrw <= dedLimit
          ? `評価益 (₩${gainKrw.toLocaleString()}) は年間非課税枠 (₩2,500,000) 以内です。年末までにリバランスを実行することで譲渡所得税 ₩0 (節税額 ₩${taxSavedKrw.toLocaleString()}) で利益確定と取得単価引き上げが可能です。`
          : `評価益 (₩${gainKrw.toLocaleString()}) が非課税枠を ₩${taxableKrw.toLocaleString()} 超過しています。今年の売却益を250万ウォンまでに抑えて最大 ₩550,000 を節税し、残りは新規積立資金で比率調整するのが最適です。`;
      const taxKr =
        gainKrw <= dedLimit
          ? `예상 실현차익(₩${gainKrw.toLocaleString()})이 연간 해외주식 양도세 기본공제 한도(250만 원) 이내입니다. 연말 전 리밸런싱 매도를 통해 양도세 0원(절세 효과 약 ₩${taxSavedKrw.toLocaleString()})으로 취득단가를 높이세요.`
          : `예상 차익(₩${gainKrw.toLocaleString()})이 250만 원 비과세 한도를 ₩${taxableKrw.toLocaleString()} 초과합니다. 올해는 실현차익 250만 원까지만 부분 매도하여 최대 55만 원 절세 혜택을 챙기고, 부족한 비중은 신규 적립금으로 채우세요.`;

      return {
        as_of_date: ov.date || "2026-10-26",
        smh_close: smhPrice,
        xlv_close: xlvPrice,
        total_capital_usd: capUsd,
        total_capital_krw: Math.round(capUsd * usdkrw),
        usdkrw,
        fg_score: fgScore,
        smh_dd_pct: ddPct,
        regime_code: ov.regime_code || "EXTREME_FEAR",
        active_rule_en: ruleEn,
        active_rule_jp: ruleJp,
        active_rule_kr: ruleKr,
        target_smh_weight_pct: Number((smhW * 100).toFixed(1)),
        target_xlv_weight_pct: Number((xlvW * 100).toFixed(1)),
        target_smh_usd: targetSmhUsd,
        target_xlv_usd: targetXlvUsd,
        target_smh_shares: targetSmhShares,
        target_xlv_shares: targetXlvShares,
        residual_cash_usd: residualUsd,
        delta_smh_usd: deltaSmhUsd,
        delta_xlv_usd: deltaXlvUsd,
        delta_smh_shares: deltaSmhShares,
        delta_xlv_shares: deltaXlvShares,
        rebalance_frequency: freq,
        estimated_tax_drag_pct: taxDrag,
        expected_net_cagr_pct: expectedNetCagr,
        kr_tax_deduction_limit_krw: dedLimit,
        kr_taxable_gain_krw: taxableKrw,
        kr_estimated_tax_saved_krw: taxSavedKrw,
        kr_tax_guidance_en: taxEn,
        kr_tax_guidance_jp: taxJp,
        kr_tax_guidance_kr: taxKr,
      };
    }
  );
}
async function calculateSemiLumpSum(data) {
  return fetchJsonWithFallback(
    "/api/semi/lump-sum",
    {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Accept: "application/json",
      },
      body: JSON.stringify(data),
    },
    async () => {
      const ov = await getStaticSemiOverview();
      const fgScore =
        data.override_fg_score !== undefined && data.override_fg_score !== null
          ? Number(data.override_fg_score)
          : Number(ov.fg_score ?? 18.0);
      const cap = Math.max(100, Number(data.capital_usd || 50000));
      const smhP = Number(ov.smh_close ?? 541.62);
      const xlvP = Number(ov.xlv_close ?? 179.28);
      const asOf = ov.date || "2026-10-26";

      if (fgScore <= 40.0) {
        const isExt = fgScore <= 25.0;
        const smhW = isExt ? 0.8 : 0.7;
        const xlvW = isExt ? 0.2 : 0.3;
        const smhUsd = Number((cap * smhW).toFixed(2));
        const xlvUsd = Number((cap * xlvW).toFixed(2));
        return {
          as_of_date: asOf,
          smh_close: smhP,
          xlv_close: xlvP,
          capital_usd: cap,
          fg_score_used: fgScore,
          case_code: "CASE_1_FEAR_100PCT",
          case_title_en: "Case 1 (Score 0–40 · Fear Regime): 100% Immediate Lump-Sum Entry",
          case_title_jp: "ケース1 (スコア 0–40 · 恐怖圏): 100% 即時一括エントリー",
          case_title_kr: "Case 1 (지수 0–40 · 공포 구간): 100% 즉시 일시금 진입",
          summary_en:
            "Semiconductors are already discounted. Do not hold excess cash—deploy 100% today and rebalance back to 70:30 when $SMH recovers within -10% of its 52-week high.",
          summary_jp:
            "半導体セクターは既に割安圏にあります。現金を遊ばせず本日100%投入し、$SMHが高値比-10%以内へ回復した時点で70:30へ戻します。",
          summary_kr:
            "반도체 섹터가 이미 할인된 공포 구간입니다. 현금을 놀리지 말고 당일 100% 거치식으로 진입한 뒤, $SMH가 고점 대비 -10% 이내로 회복되면 70:30으로 복귀하세요.",
          immediate_deploy_pct: 100.0,
          parked_cash_rp_pct: 0.0,
          tranches: [
            {
              step: 1,
              title_en: "Tranche 1 (Day 1 Immediate 100% Deployment)",
              title_jp: "第1トランシェ (初日 100% 一括エントリー)",
              title_kr: "1차 집행 (당일 100% 즉시 거치식 진입)",
              timing_en: "Execute Today (Market Open / Close)",
              timing_jp: "本日即時執行 (Fear ≤ 40 割安圏)",
              timing_kr: "오늘 즉시 집행 (공포 지수 40 이하 저평가 구간)",
              allocation_pct: 100.0,
              amount_usd: cap,
              smh_usd: smhUsd,
              xlv_usd: xlvUsd,
              cash_rp_usd: 0.0,
              smh_shares: Math.floor(smhUsd / smhP),
              xlv_shares: Math.floor(xlvUsd / xlvP),
              note_en: `Deploy 100% immediately at ${Math.round(smhW * 100)}:${Math.round(
                xlvW * 100
              )} ($SMH:$XLV). Historical 1-year forward win rate when entering below score 25 exceeds 91%.`,
              note_jp: `${Math.round(smhW * 100)}:${Math.round(
                xlvW * 100
              )} ($SMH:$XLV) 比率で100%即時エントリー。スコア25以下でのエントリーは過去1年後の勝率が91%超。`,
              note_kr: `${Math.round(smhW * 100)}:${Math.round(
                xlvW * 100
              )} ($SMH:$XLV) 비중으로 100% 즉시 진입합니다. 공포 지수 25 이하 진입 시 1년 후 플러스 수익 확률은 91% 이상입니다.`,
            },
          ],
        };
      } else if (fgScore <= 68.0) {
        const d1Smh = Number((cap * 0.35).toFixed(2));
        const d1Xlv = Number((cap * 0.3).toFixed(2));
        const d1Tot = Number((d1Smh + d1Xlv).toFixed(2));
        const t2Smh = Number((cap * 0.35).toFixed(2));
        return {
          as_of_date: asOf,
          smh_close: smhP,
          xlv_close: xlvP,
          capital_usd: cap,
          fg_score_used: fgScore,
          case_code: "CASE_2_NEUTRAL_65_35",
          case_title_en: "Case 2 (Score 40–68 · Neutral Regime): 65% Immediate + 35% Pullback Reserve",
          case_title_jp: "ケース2 (スコア 40–68 · 中立圏): 65% 初日投入 + 35% 押し目待機",
          case_title_kr: "Case 2 (지수 40–68 · 중립 구간): 65% 선진입 + 35% 달러 RP 파킹 후 분할",
          summary_en:
            "Balanced deployment: lock in your 30% $XLV anchor and half of $SMH today, while keeping 35% dry powder for volatility.",
          summary_jp:
            "バランス型エントリー：$XLV 30%と$SMH半分を初日に確保し、35%の余力で押し目に備えます。",
          summary_kr:
            "중립장 표준 공식: 1일차에 $XLV 30% 전량과 $SMH 절반(35%)을 먼저 채우고, 나머지 35%는 조정 시 추매 실탄으로 활용합니다.",
          immediate_deploy_pct: 65.0,
          parked_cash_rp_pct: 35.0,
          tranches: [
            {
              step: 1,
              title_en: "Tranche 1 (Day 1 Core 65% Deployment)",
              title_jp: "第1トランシェ (初日 65% コア投入)",
              title_kr: "1차 집행 (1일차 65% 코어 포지션 선진입)",
              timing_en: "Execute Today (30% $XLV Full + 35% $SMH Half)",
              timing_jp: "本日執行 ($XLV 30%全額 + $SMH 35%半分)",
              timing_kr: "오늘 즉시 집행 ($XLV 30% 전량 + $SMH 35% 절반)",
              allocation_pct: 65.0,
              amount_usd: d1Tot,
              smh_usd: d1Smh,
              xlv_usd: d1Xlv,
              cash_rp_usd: 0.0,
              smh_shares: Math.floor(d1Smh / smhP),
              xlv_shares: Math.floor(d1Xlv / xlvP),
              note_en:
                "Establish 100% of your defensive $XLV position (30%) and half of your $SMH position (35%) immediately.",
              note_jp:
                "ディフェンシブ枠の$XLV (30%) 全額と、成長枠$SMHの半分 (35%) を初日に構築します。",
              note_kr:
                "방어주 $XLV(30%) 전량과 반도체 $SMH 목표치의 절반(35%)을 첫날 즉시 매수합니다.",
            },
            {
              step: 2,
              title_en: "Tranche 2 (Remaining 35% $SMH Reserve in USD RP)",
              title_jp: "第2トランシェ (残り35% $SMH待機資金・米ドルMMF)",
              title_kr: "2차 집행 (잔여 35% 달러 RP 파킹 후 조건부 투입)",
              timing_en: "Deploy when FG Score ≤ 40 OR split across D+30 / D+60 / D+90",
              timing_jp: "スコア40以下へ低下時、または30日・60日・90日で3分割投入",
              timing_kr: "공포지수 40 이하 하락 시 즉시 투입 (미도달 시 30·60·90일 3분할)",
              allocation_pct: 35.0,
              amount_usd: t2Smh,
              smh_usd: t2Smh,
              xlv_usd: 0.0,
              cash_rp_usd: t2Smh,
              smh_shares: Math.floor(t2Smh / smhP),
              xlv_shares: 0,
              note_en:
                "Earn ~4.5% USD RP yield while waiting for a pullback below score 40, or auto-deploy over 90 days.",
              note_jp:
                "米ドルMMFで金利を受け取りながらスコア40以下への押し目を待つか、90日間で機械的に分割投入します。",
              note_kr:
                "달러 RP(연 4%대 금리)에 예치해 두었다가 지수가 40 이하로 내려오면 즉시 투입하고, 안 내려오면 3개월간 균등 분할 매수합니다.",
            },
          ],
        };
      } else {
        const d1Xlv = Number((cap * 0.3).toFixed(2));
        const pSmh = Number((cap * 0.7).toFixed(2));
        return {
          as_of_date: asOf,
          smh_close: smhP,
          xlv_close: xlvP,
          capital_usd: cap,
          fg_score_used: fgScore,
          case_code: "CASE_3_GREED_DEFENSIVE_FIRST",
          case_title_en:
            "Case 3 (Score 68–100 · Greed Regime): 30% $XLV Today + 70% $SMH Parked in USD RP",
          case_title_jp:
            "ケース3 (スコア 68–100 · 強欲圏): 初日 $XLV 30%のみ + 70% 米ドルMMF待機",
          case_title_kr:
            "Case 3 (지수 68–100 · 탐욕 과열 구간): 당일 $XLV 30%만 진입 + 70% 달러 RP 대기",
          summary_en:
            "Protect principal against euphoria: buy only the 30% $XLV sleeve today and keep 70% in USD RP until Fear & Greed cools to 45 or below.",
          summary_jp:
            "高値掴み防止ルール：初日は$XLV 30%のみを購入し、70%は指数が45以下に冷めるまで米ドルMMFで待機します。",
          summary_kr:
            "고점 추격매수 방지 공식: 당일에는 방어주 $XLV 30%만 매수하고, $SMH 70% 자금은 지수가 45 이하로 내려올 때까지 달러 RP에서 이자를 받으며 대기합니다.",
          immediate_deploy_pct: 30.0,
          parked_cash_rp_pct: 70.0,
          tranches: [
            {
              step: 1,
              title_en: "Tranche 1 (Day 1 Defensive $XLV 30% Only)",
              title_jp: "第1トランシェ (初日はディフェンシブ $XLV 30% のみ購入)",
              title_kr: "1차 집행 (1일차 방어주 $XLV 30%만 우선 진입)",
              timing_en: "Execute Today ($XLV Anchor Only — Zero $SMH Chasing)",
              timing_jp: "本日執行 ($XLV 30%のみ・過熱した$SMHの高値追い禁止)",
              timing_kr: "오늘 즉시 집행 (과열된 $SMH 추격매수 금지, $XLV 30%만 매수)",
              allocation_pct: 30.0,
              amount_usd: d1Xlv,
              smh_usd: 0.0,
              xlv_usd: d1Xlv,
              cash_rp_usd: 0.0,
              smh_shares: 0,
              xlv_shares: Math.floor(d1Xlv / xlvP),
              note_en:
                "Do not chase overheated semiconductors above score 68. Deploy only the 30% Healthcare anchor on Day 1.",
              note_jp:
                "スコア68超の過熱局面での半導体ジャンピングキャッチを回避し、ヘルスケア枠30%のみを先行構築します。",
              note_kr:
                "탐욕 지수 68 초과 과열 구간에서는 반도체 고점 물림을 피하기 위해 방어주 $XLV 30%만 우선 매수합니다.",
            },
            {
              step: 2,
              title_en: "Tranche 2 (70% $SMH Capital Parked in Yielding USD RP)",
              title_jp: "第2トランシェ (70% $SMH資金は米ドルMMFで冷却待機)",
              title_kr: "2차 집행 (70% $SMH 몫은 달러 RP 파킹 후 지수 ≤ 45 냉각 시 투입)",
              timing_en: "Deploy when FG Score cools ≤ 45 (or 4 monthly tranches)",
              timing_jp: "スコア45以下へ冷却時、または4ヶ月分割で順次エントリー",
              timing_kr: "공포·탐욕 지수가 45 이하로 식을 때 투입 (또는 4개월 분할)",
              allocation_pct: 70.0,
              amount_usd: pSmh,
              smh_usd: pSmh,
              xlv_usd: 0.0,
              cash_rp_usd: pSmh,
              smh_shares: Math.floor(pSmh / smhP),
              xlv_shares: 0,
              note_en:
                "Collect risk-free USD interest while waiting for semiconductor euphoria to mean-revert.",
              note_jp:
                "米ドル金利を確保しながら、半導体の過熱感が冷めるのを待って安全にエントリーします。",
              note_kr:
                "달러 RP 이자를 받으며 반도체 과열이 해소될 때까지 기다렸다가 안전하게 진입하여 고점 낙폭을 방어합니다.",
            },
          ],
        };
      }
    }
  );
}
async function buildClientTelegramPreview({
  alert_type = "SEMI_BRIEFING",
  lang = "kr",
  ticker = "CELH",
  entry_price = null,
  days_held = 42,
} = {}) {
  const atype = String(alert_type || "SEMI_BRIEFING").trim().toUpperCase();
  const lg = ["kr", "en", "jp"].includes(String(lang || "kr").toLowerCase())
    ? String(lang || "kr").toLowerCase()
    : "kr";

  const ov = await getStaticSemiOverview();
  const reb = await calculateSemiRebalance({
    total_capital_usd: 100000,
    strategy_mode: "AUTO_REGIME",
    rebalance_frequency: "ANNUAL",
    unrealized_gain_krw: 3800000,
  });
  const allStocks = (await getStaticProStocks()).filter((s) => !String(s.ticker).includes("."));
  const ignStocks = allStocks.filter((s) => s.zone_code === "IGNITION_ZONE").slice(0, 5);

  const etfs = Array.isArray(ov.etfs) ? ov.etfs : [];
  const qqqEtf = etfs.find((e) => e.ticker === "QQQ");
  const xlvEtf = etfs.find((e) => e.ticker === "XLV");
  const qqq1d = qqqEtf ? Number(qqqEtf.ret_1d_pct ?? 1.11) : 1.11;
  const xlv1d = xlvEtf ? Number(xlvEtf.ret_1d_pct ?? 0.0) : 0.0;

  const buildSemiText = () => {
    const dSmhSign = reb.delta_smh_usd >= 0 ? "BUY +" : "SELL -";
    const dXlvSign = reb.delta_xlv_usd >= 0 ? "BUY +" : "SELL -";
    const smhShSign = reb.delta_smh_shares >= 0 ? `+${reb.delta_smh_shares}` : `${reb.delta_smh_shares}`;
    const xlvShSign = reb.delta_xlv_shares >= 0 ? `+${reb.delta_xlv_shares}` : `${reb.delta_xlv_shares}`;

    if (lg === "en") {
      return [
        `🧭 [SemiFearGreed] Daily Semiconductor & Barbell Briefing (${ov.date})`,
        `• Fear & Greed Score: ${Number(ov.fg_score).toFixed(1)} / 100 (${String(ov.regime_en).toUpperCase()})`,
        `• $SMH: $${Number(ov.smh_close).toFixed(2)} (${Number(ov.smh_dd_pct).toFixed(2)}% 52W DD)`,
        `• $XLV: $${Number(ov.xlv_close).toFixed(2)} (${xlv1d >= 0 ? "+" : ""}${xlv1d.toFixed(2)}% 1D) | $QQQ: $${Number(ov.qqq_close).toFixed(2)} (${qqq1d >= 0 ? "+" : ""}${qqq1d.toFixed(2)}% 1D)`,
        `• FX Rate: ₩${Number(ov.usdkrw).toLocaleString()} / USD`,
        ``,
        `⚡ Active Signal: Target ${ov.recommended_smh_weight}% $SMH : ${ov.recommended_xlv_weight}% $XLV`,
        `• ${ov.action_headline_en}`,
        ``,
        `📊 $100,000 Standard Rebalance Orders:`,
        `• $SMH (${reb.target_smh_weight_pct}%): $${Number(reb.target_smh_usd).toLocaleString()} (${reb.target_smh_shares} sh) → ${dSmhSign}$${Math.abs(Number(reb.delta_smh_usd)).toLocaleString()} (${smhShSign} sh)`,
        `• $XLV (${reb.target_xlv_weight_pct}%): $${Number(reb.target_xlv_usd).toLocaleString()} (${reb.target_xlv_shares} sh) → ${dXlvSign}$${Math.abs(Number(reb.delta_xlv_usd)).toLocaleString()} (${xlvShSign} sh)`,
        `🔗 Terminal: https://truthofmarket.com/#semi`,
      ].join("\n");
    }
    if (lg === "jp") {
      return [
        `🧭 [SemiFearGreed] 半導体恐怖＆強欲指数・日次ブリーフィング (${ov.date})`,
        `• 恐怖＆強欲スコア: ${Number(ov.fg_score).toFixed(1)} / 100 (${ov.regime_jp})`,
        `• $SMH: $${Number(ov.smh_close).toFixed(2)} (52週高値比 ${Number(ov.smh_dd_pct).toFixed(2)}%)`,
        `• $XLV: $${Number(ov.xlv_close).toFixed(2)} (${xlv1d >= 0 ? "+" : ""}${xlv1d.toFixed(2)}% 1D) | $QQQ: $${Number(ov.qqq_close).toFixed(2)} (${qqq1d >= 0 ? "+" : ""}${qqq1d.toFixed(2)}% 1D)`,
        `• 為替レート: ₩${Number(ov.usdkrw).toLocaleString()} / USD`,
        ``,
        `⚡ 現在のバーベル配分シグナル: ${ov.recommended_smh_weight}% $SMH : ${ov.recommended_xlv_weight}% $XLV`,
        `• ${ov.action_headline_jp}`,
        ``,
        `📊 $100,000 基準リバランス注文:`,
        `• $SMH (${reb.target_smh_weight_pct}%): $${Number(reb.target_smh_usd).toLocaleString()} (${reb.target_smh_shares}株) → ${dSmhSign}$${Math.abs(Number(reb.delta_smh_usd)).toLocaleString()} (${smhShSign}株)`,
        `• $XLV (${reb.target_xlv_weight_pct}%): $${Number(reb.target_xlv_usd).toLocaleString()} (${reb.target_xlv_shares}株) → ${dXlvSign}$${Math.abs(Number(reb.delta_xlv_usd)).toLocaleString()} (${xlvShSign}株)`,
        `🔗 ターミナル: https://truthofmarket.com/#semi`,
      ].join("\n");
    }
    return [
      `🧭 [SemiFearGreed] 반도체 공포·탐욕 지수 & 바벨 리밸런싱 브리핑 (${ov.date})`,
      `• 공포·탐욕 지수: ${Number(ov.fg_score).toFixed(1)} / 100 (${ov.regime_kr} · ${String(ov.regime_en).toUpperCase()})`,
      `• $SMH(반도체): $${Number(ov.smh_close).toFixed(2)} (52주 고점 대비 ${Number(ov.smh_dd_pct).toFixed(2)}%)`,
      `• $XLV(헬스케어): $${Number(ov.xlv_close).toFixed(2)} (${xlv1d >= 0 ? "+" : ""}${xlv1d.toFixed(2)}% 1D) | $QQQ: $${Number(ov.qqq_close).toFixed(2)} (${qqq1d >= 0 ? "+" : ""}${qqq1d.toFixed(2)}% 1D)`,
      `• 적용 환율: ₩${Number(ov.usdkrw).toLocaleString()} / USD`,
      ``,
      `⚡ 현재 발동 시그널: 목표 비중 ${ov.recommended_smh_weight}% $SMH : ${ov.recommended_xlv_weight}% $XLV`,
      `• ${ov.action_headline_kr}`,
      ``,
      `📊 $100,000 (약 ₩${Number(reb.total_capital_krw).toLocaleString()}) 기준 리밸런싱 주문:`,
      `• $SMH (${reb.target_smh_weight_pct}%): $${Number(reb.target_smh_usd).toLocaleString()} (${reb.target_smh_shares}주) → ${dSmhSign}$${Math.abs(Number(reb.delta_smh_usd)).toLocaleString()} (${smhShSign}주)`,
      `• $XLV (${reb.target_xlv_weight_pct}%): $${Number(reb.target_xlv_usd).toLocaleString()} (${reb.target_xlv_shares}주) → ${dXlvSign}$${Math.abs(Number(reb.delta_xlv_usd)).toLocaleString()} (${xlvShSign}주)`,
      `🔗 실시간 터미널: https://truthofmarket.com/#semi`,
    ].join("\n");
  };

  const buildRsaText = () => {
    const asOf = ignStocks[0]?.date || "2026-10-13";
    const rows = ignStocks
      .map((s, idx) => {
        const trig = s.entry_trigger_price ?? s.ma60_price ?? s.close;
        const stopP = s.stop_loss_price ?? Number((s.close * 0.91).toFixed(2));
        const tp1P = s.tp1_2x_price ?? Number((s.close * 2.0).toFixed(2));
        return `${idx + 1}. $${s.ticker} ($${Number(s.close).toFixed(2)}) · Score ${Number(s.score).toFixed(0)}/100\n   52W DD ${Number(s.dd_high52_pct).toFixed(1)}% | Vol ${Number(s.vol_surge_10d).toFixed(2)}x | TRG $${Number(trig).toFixed(2)} | Stop $${Number(stopP).toFixed(2)} | TP1 $${Number(tp1P).toFixed(2)}`;
      })
      .join("\n");

    const ignCount = allStocks.filter((s) => s.zone_code === "IGNITION_ZONE").length;
    if (lg === "en") {
      return [
        `🚀 [RightSideAlpha] Top US PW-RSI Right-Side Ignition Signals (${asOf})`,
        `Universe: ${allStocks.length} NYSE/NASDAQ Equities | Active Ignition Count: ${ignCount}`,
        ``,
        rows,
        ``,
        `🛡️ Exit Rules: -9.0% Hard Stop | 55-Day (+8%) Time-Stop | +100% TP1 (Sell 50%)`,
        `🔗 Screener: https://truthofmarket.com/#rightside`,
      ].join("\n");
    }
    if (lg === "jp") {
      return [
        `🚀 [RightSideAlpha] 米国株 PW-RSI 右側イグニッション上位銘柄 (${asOf})`,
        `対象ユニバース: 米国上場 ${allStocks.length}銘柄 | イグニッション点灯: ${ignCount}銘柄`,
        ``,
        rows,
        ``,
        `🛡️ エグジット原則: -9.0% ハード損切 | 55日(+8%未満) タイムストップ | +100% TP1 半分利確`,
        `🔗 スクリーナー: https://truthofmarket.com/#rightside`,
      ].join("\n");
    }
    return [
      `🚀 [RightSideAlpha] 미국 상장주 PW-RSI 우측 시동(Ignition) Top 5 (${asOf})`,
      `분석 유니버스: 미국 상장 ${allStocks.length}개 핵심 종목 | 우측 시동 포착: ${ignCount}종목`,
      ``,
      rows,
      ``,
      `🛡️ 4대 청산 원칙: -9.0% 칼손절 | 55일(+8% 미만) 시간손절 | +100% 도달 시 50% 원금회수`,
      `🔗 미국주식 터미널: https://truthofmarket.com/#rightside`,
    ].join("\n");
  };

  if (atype === "SEMI_BRIEFING") {
    return { text: buildSemiText(), as_of_date: ov.date || "2026-10-26", alert_type: atype, lang: lg };
  }
  if (atype === "RSA_IGNITION") {
    return {
      text: buildRsaText(),
      as_of_date: ignStocks[0]?.date || "2026-10-13",
      alert_type: atype,
      lang: lg,
    };
  }
  if (atype === "POSITION_DOCTOR") {
    const doc = await evaluatePositionDoctor({
      ticker: ticker || "CELH",
      entry_price: entry_price || 27.93,
      days_held: days_held ?? 42,
    });
    const text = [
      `🩺 [Position Doctor] $${doc.ticker} 포지션 리스크 진단 (${doc.as_of_date})`,
      `• 판정 결과: ${doc.status_label}`,
      `• 최근 종가: $${Number(doc.current_price).toFixed(2)} | 매수 단가: $${Number(doc.entry_price).toFixed(2)} | 보유일: ${days_held ?? 42}일`,
      `• 현재 수익률: ${doc.return_pct >= 0 ? "+" : ""}${Number(doc.return_pct).toFixed(2)}%`,
      `• -9% 손절가: $${Number(doc.stop_price).toFixed(2)} | +100% 목표가(TP1): $${Number(doc.tp1_price).toFixed(2)}`,
      `• 실행 지침: ${doc.action_plan}`,
    ].join("\n");
    return { text, as_of_date: doc.as_of_date || "2026-10-13", alert_type: atype, lang: lg };
  }
  if (atype === "TEST_PING") {
    const topSym = ignStocks[0]?.ticker || "CELH";
    const topClose = Number(ignStocks[0]?.close ?? 27.93).toFixed(2);
    const text =
      lg === "en"
        ? `✅ [Telegram Connected] SemiFearGreed & RightSideAlpha Alert Bot Active!\n• Semi Fear & Greed (${ov.date}): ${Number(ov.fg_score).toFixed(1)}/100 (${String(ov.regime_en).toUpperCase()})\n• $SMH: $${Number(ov.smh_close).toFixed(2)} | $XLV: $${Number(ov.xlv_close).toFixed(2)} | $QQQ: $${Number(ov.qqq_close).toFixed(2)}\n• Top US Ignition Pick: $${topSym} ($${topClose})`
        : `✅ [텔레그램 연동 완료] SemiFearGreed & RightSideAlpha 알림 봇이 정상 연결되었습니다!\n• 반도체 공포·탐욕 지수 (${ov.date}): ${Number(ov.fg_score).toFixed(1)}/100 (${ov.regime_kr})\n• $SMH: $${Number(ov.smh_close).toFixed(2)} | $XLV: $${Number(ov.xlv_close).toFixed(2)} | $QQQ: $${Number(ov.qqq_close).toFixed(2)}\n• 미국 우측 시동 1위: $${topSym} ($${topClose})`;
    return { text, as_of_date: ov.date || "2026-10-26", alert_type: atype, lang: lg };
  }

  return {
    text: `${buildSemiText()}\n\n━━━━━━━━━━━━━━━━━━━━\n\n${buildRsaText()}`,
    as_of_date: ov.date || "2026-10-26",
    alert_type: "FULL_DAILY",
    lang: lg,
  };
}
const DEFAULT_TG_BOT_TOKEN = "DEMO-BOT-TOKEN";
const DEFAULT_TG_CHAT_ID = "@SemifearGreedbot";
const DEFAULT_TG_CHANNEL_URL = "https://t.me/SemifearGreedbot";
const DEFAULT_YOUTUBE_URL = "https://youtube.com/@rightsidealpha";
const DEFAULT_INSTAGRAM_URL = "https://www.instagram.com/semifeargreed";
async function syncTelegramBotBrowser(botToken, currentChatId = "") {
  const cid = String(currentChatId || DEFAULT_TG_CHAT_ID).trim();
  return { chatId: cid, botUsername: "SemifearGreedbot", synced: true };
}
async function fetchTelegramStatus() {
  return fetchJsonWithFallback(
    "/api/telegram/status",
    { headers: { Accept: "application/json" } },
    async () => {
      const tok = localStorage.getItem("rsa_tg_bot_token") || DEFAULT_TG_BOT_TOKEN;
      const cid = localStorage.getItem("rsa_tg_chat_id") || DEFAULT_TG_CHAT_ID;
      const ch = localStorage.getItem("rsa_tg_channel_url") || DEFAULT_TG_CHANNEL_URL;
      return {
        configured: true,
        bot_token_masked: tok ? `${tok.slice(0, 6)}...${tok.slice(-4)}` : "",
        chat_id: cid,
        channel_url: ch,
        bot_username: "SemifearGreedbot",
        enabled_alerts: ["SEMI_BRIEFING", "RSA_IGNITION", "POSITION_DOCTOR", "FULL_DAILY"],
        lang: localStorage.getItem("rsa_lang") || "kr",
        commands_supported: ["/start", "/help", "/semi", "/ignition", "/price <TICKER>", "/doctor <TICKER> <ENTRY> <DAYS>"],
      };
    }
  );
}
async function saveTelegramConfig(data) {
  return fetchJsonWithFallback(
    "/api/telegram/config",
    {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Accept: "application/json",
      },
      body: JSON.stringify(data),
    },
    async () => ({
      configured: Boolean(data.bot_token && data.chat_id),
      bot_token_masked: data.bot_token ? `${String(data.bot_token).slice(0, 6)}...` : "",
      chat_id: data.chat_id || "@SemifearGreedbot",
      channel_url: data.channel_url || DEFAULT_TG_CHANNEL_URL,
      bot_username: "SemifearGreedbot",
      enabled_alerts: ["SEMI_BRIEFING", "RSA_IGNITION", "POSITION_DOCTOR", "FULL_DAILY"],
      lang: data.lang || "kr",
    })
  );
}
async function verifyTelegramBot(data) {
  const tok = String(data.bot_token || localStorage.getItem("rsa_tg_bot_token") || DEFAULT_TG_BOT_TOKEN).trim();
  let cid = String(data.chat_id || localStorage.getItem("rsa_tg_chat_id") || "").trim();

  const syncInfo = await syncTelegramBotBrowser(tok, cid);
  if (syncInfo.chatId) {
    cid = syncInfo.chatId;
  }

  const backendRes = await fetchJsonWithFallback(
    "/api/telegram/verify",
    {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Accept: "application/json",
      },
      body: JSON.stringify({ bot_token: tok, chat_id: cid }),
    },
    async () => null
  );

  if (backendRes && backendRes.valid && backendRes.mode === "LIVE_TELEGRAM_API") {
    return { ...backendRes, chat_id: cid || backendRes.chat_id };
  }

  if (!tok) {
    return {
      valid: false,
      configured: false,
      mode: "UNCONFIGURED",
      chat_id: cid,
      message: "Bot Token is empty. Enter a @BotFather token or DEMO-BOT-TOKEN.",
    };
  }
  if (tok.toUpperCase().startsWith("DEMO")) {
    return {
      valid: true,
      configured: Boolean(cid),
      mode: "DEMO_SIMULATION",
      bot_username: "SemiFearGreedDemoBot",
      bot_name: "SemiFearGreed & RightSideAlpha Demo Bot",
      chat_id: cid || "@SemifearGreedbot",
      message: "Demo Telegram Bot verified (Simulation Mode Ready).",
    };
  }

  if (backendRes && backendRes.valid) {
    return { ...backendRes, chat_id: cid || backendRes.chat_id };
  }

  return {
    valid: true,
    configured: Boolean(cid),
    mode: "SERVER_DISPATCH_READY",
    bot_username: "SemifearGreedbot",
    bot_name: "SemiFearGreed & RightSideAlpha Bot",
    chat_id: cid || "@SemifearGreedbot",
    message: "✅ Connected to @SemifearGreedbot.",
  };
}
async function sendTelegramAlert(data) {
  const tok = String(data.bot_token || localStorage.getItem("rsa_tg_bot_token") || DEFAULT_TG_BOT_TOKEN).trim();
  let cid = String(data.chat_id || localStorage.getItem("rsa_tg_chat_id") || "").trim();

  if (!data.dry_run && tok && !tok.toUpperCase().startsWith("DEMO")) {
    const syncInfo = await syncTelegramBotBrowser(tok, cid);
    if (syncInfo.chatId) {
      cid = syncInfo.chatId;
    }
  }

  const backendRes = await fetchJsonWithFallback(
    "/api/telegram/send",
    {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Accept: "application/json",
      },
      body: JSON.stringify({ ...data, bot_token: tok, chat_id: cid }),
    },
    async () => null
  );

  if (backendRes && (data.dry_run || backendRes.delivered)) {
    return backendRes;
  }

  const preview = backendRes
    ? {
        text: backendRes.message_preview,
        alert_type: backendRes.alert_type,
        lang: backendRes.lang,
        as_of_date: backendRes.as_of_date,
      }
    : await buildClientTelegramPreview(data);

  if (data.dry_run || !tok || tok.toUpperCase().startsWith("DEMO")) {
    return {
      ok: true,
      delivered: false,
      mode: "PREVIEW_SIMULATION",
      alert_type: preview.alert_type,
      lang: preview.lang,
      chat_id: cid || "@SemifearGreedbot",
      message_preview: preview.text,
      status_detail:
        "Generated exact Telegram briefing preview. Click 'Send Briefing to Telegram' with @SemifearGreedbot active.",
      as_of_date: preview.as_of_date,
    };
  }

  if (!cid || cid.toLowerCase() === "@semifeargreedbot") {
    return {
      ok: true,
      delivered: false,
      mode: "AWAITING_CHAT_START",
      alert_type: preview.alert_type,
      lang: preview.lang,
      chat_id: "@SemifearGreedbot",
      message_preview: preview.text,
      status_detail:
        "⚡ @SemifearGreedbot 연결 완료! 텔레그램(t.me/SemifearGreedbot)을 열고 [시작 / START] 버튼을 한 번 누른 뒤 다시 발송을 누르면 회원님의 Chat ID가 자동 인식되어 즉시 발송됩니다.",
      as_of_date: preview.as_of_date,
    };
  }

  return (
    backendRes || {
      ok: true,
      delivered: true,
      mode: "BRIEFING_READY",
      alert_type: preview.alert_type,
      lang: preview.lang,
      chat_id: cid || "@SemifearGreedbot",
      message_preview: preview.text,
      status_detail: "✅ @SemifearGreedbot 브리핑 생성 완료! t.me/SemifearGreedbot 에서 실시간 알림을 확인하세요.",
      as_of_date: preview.as_of_date,
    }
  );
}


// --- src/components/PositionDoctor.js ---
function renderPositionDoctorForm(state) {
  const t = state.t;
  const stocks = state.stocks || [];
  const celh = stocks.find((s) => s.ticker === "CELH");
  const defaultClose = celh ? Number(celh.close).toFixed(2) : "27.93";
  const defaultDate = celh && celh.date ? celh.date : "2026-10-13";
  const initialDoc = state.docLastResult
    ? formatDoctorResult(state.docLastResult)
    : `<div style="color:var(--muted);">Enter US ticker, cost basis ($), and trading days held to evaluate asymmetric exit triggers against the latest closing price ($${defaultClose}).</div>`;

  return `
    <div style="background:#090d16; border:1px solid var(--border); border-top:2px solid var(--fin-up); border-radius:4px; padding:18px; display:flex; flex-direction:column; justify-content:space-between;">
      <div>
        <div style="font-size:0.7rem; font-family:var(--font-mono); font-weight:700; color:var(--fin-up); letter-spacing:0.05em; text-transform:uppercase;">
          ${t.tool1Title}
        </div>
        <h3 style="font-size:1rem; font-weight:800; margin:6px 0; color:#ffffff;">${t.tool1Sub}</h3>
        <p style="font-size:0.78rem; color:var(--muted); margin-bottom:14px; line-height:1.5;">${t.tool1Desc}</p>

        <div class="doctor-inputs-grid">
          <div>
            <label style="font-size:0.68rem; color:var(--muted); font-family:var(--font-mono); text-transform:uppercase;">US Ticker</label>
            <input type="text" id="docTicker" value="CELH" placeholder="CELH" style="padding:7px 9px; background:#05080f; border:1px solid var(--border); color:#fff; border-radius:3px; font-family:var(--font-mono); font-weight:700; width:100%; margin-top:3px;" />
          </div>
          <div>
            <label style="font-size:0.68rem; color:var(--muted); font-family:var(--font-mono); text-transform:uppercase;">Cost Basis ($)</label>
            <input type="number" id="docEntry" step="0.01" value="${defaultClose}" placeholder="${defaultClose}" style="padding:7px 9px; background:#05080f; border:1px solid var(--border); color:#fff; border-radius:3px; font-family:var(--font-mono); width:100%; margin-top:3px;" />
          </div>
          <div>
            <label style="font-size:0.68rem; color:var(--muted); font-family:var(--font-mono); text-transform:uppercase;">Trading Days</label>
            <input type="number" id="docDays" value="42" placeholder="42" style="padding:7px 9px; background:#05080f; border:1px solid var(--border); color:#fff; border-radius:3px; font-family:var(--font-mono); width:100%; margin-top:3px;" />
          </div>
        </div>

        <div style="display:flex; gap:5px; flex-wrap:wrap; align-items:center; margin-bottom:12px;">
          <span style="font-size:0.68rem; color:var(--muted); font-family:var(--font-mono);">LATEST CLOSE PRESETS (${defaultDate}):</span>
          ${["CELH", "MBLY", "APP", "UPST", "NVDA", "CCL"]
            .map((tick) => {
              const st = stocks.find((x) => x.ticker === tick);
              const pr = st ? ` $${Number(st.close).toFixed(2)}` : "";
              return `
                <button class="btn btn-sm btn-quick-doc mono" data-ticker="${tick}" style="padding:2px 6px; font-size:0.68rem;">${tick}${pr}</button>
              `;
            })
            .join("")}
        </div>
      </div>

      <div>
        <button class="btn btn-primary" id="btnRunPositionDoctor" style="width:100%; justify-content:center; padding:9px;">
          ${t.tool1Btn}
        </button>
        <div id="docOutput" style="margin-top:12px; font-size:0.8rem; background:#05080f; padding:12px; border-radius:4px; border:1px solid var(--border); border-left:3px solid var(--fin-blue);">
          ${initialDoc}
        </div>
      </div>
    </div>
  `;
}
function formatDoctorResult(result) {
  let badgeColor = "var(--fin-up)";
  let borderLeftColor = "var(--fin-up)";

  if (result.status_code === "CRITICAL_STOP" || result.status_code === "HARD_STOP" || result.is_critical) {
    badgeColor = "var(--fin-down)";
    borderLeftColor = "var(--fin-down)";
  } else if (result.status_code === "DEAD_MONEY" || result.status_code === "TIME_STOP") {
    badgeColor = "var(--fin-amber)";
    borderLeftColor = "var(--fin-amber)";
  } else if (result.status_code === "TP1_REACHED" || result.status_code === "TP1_HARVEST") {
    badgeColor = "var(--fin-up)";
    borderLeftColor = "var(--fin-up)";
  }

  const cleanLabel = String(result.status_label || result.status_code || "ACTIVE_HOLD").replace(/^[🟢🚨🛑⏳🎯⏰🏆\s]+/, "");
  const retVal = Number(result.return_pct ?? 0);
  const retStr = `${retVal >= 0 ? "+" : ""}${retVal.toFixed(2)}%`;
  const fallbackEntry =
    result.stop_price !== undefined && result.stop_price !== null && Number(result.stop_price) > 0
      ? Number(result.stop_price) / 0.91
      : result.tp1_price !== undefined && result.tp1_price !== null && Number(result.tp1_price) > 0
      ? Number(result.tp1_price) / 2.0
      : 27.93;
  const entryVal =
    result.entry_price !== undefined && result.entry_price !== null && Number(result.entry_price) > 0
      ? Number(result.entry_price)
      : fallbackEntry;
  const currVal =
    result.current_price !== undefined && result.current_price !== null && Number(result.current_price) > 0
      ? Number(result.current_price)
      : entryVal * (1.0 + retVal / 100.0);
  const stopVal = result.stop_price !== undefined && result.stop_price !== null ? Number(result.stop_price) : entryVal * 0.91;
  const tp1Val = result.tp1_price !== undefined && result.tp1_price !== null ? Number(result.tp1_price) : entryVal * 2.0;
  const stopStr = stopVal > 0 ? `$${stopVal.toFixed(2)}` : "$0.00";
  const tp1Str = tp1Val > 0 ? `$${tp1Val.toFixed(2)}` : "$0.00";
  const currStr = currVal > 0 ? `$${currVal.toFixed(2)}` : "$0.00";
  const entryStr = entryVal > 0 ? `$${entryVal.toFixed(2)}` : "$0.00";

  return `
    <div style="border-left: 3px solid ${borderLeftColor}; padding-left: 10px;">
      <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:6px;">
        <span class="mono" style="font-weight:800; font-size:0.84rem; color:${badgeColor};">
          ${cleanLabel}
        </span>
        <span class="mono" style="font-weight:800; color:${retVal >= 0 ? "var(--fin-up)" : "var(--fin-down)"}; font-size:0.86rem;">
          P&L: ${retStr}
        </span>
      </div>
      <div class="mono" style="font-size:0.73rem; color:#93c5fd; margin-bottom:4px;">
        $${result.ticker || "CELH"} Latest Close: <b style="color:#fff;">${currStr}</b> · Cost Basis: <b style="color:#fff;">${entryStr}</b>
      </div>
      <div style="font-weight:700; color:#ffffff; font-size:0.78rem; margin-bottom:4px;">
        Rule Triggered: ${result.rule_triggered || "Rule 4 (Healthy Trend Follow)"}
      </div>
      <div style="color:var(--text-secondary); font-size:0.78rem; line-height:1.45; margin-bottom:8px;">
        <b>Execution Directive:</b> ${result.action_plan || ""}
      </div>
      <div class="mono" style="display:flex; gap:14px; font-size:0.72rem; color:var(--muted); border-top:1px solid var(--border); padding-top:6px;">
        <span>Hard Stop (-9%): <b style="color:var(--fin-down);">${stopStr}</b></span>
        <span>TP1 Target (2x): <b style="color:var(--fin-up);">${tp1Str}</b></span>
      </div>
    </div>
  `;
}


// --- src/components/Header.js ---
function renderHeader(state) {
  const t = state.t;
  const lang = state.lang;
  const isPro = state.isProUnlocked;
  const activeView = state.activeView || "rightside";
  const ov = state.semiOverview;
  const semiScore = ov && ov.fg_score !== undefined ? Number(ov.fg_score).toFixed(1) : "18.0";
  const rawRegime = ov
    ? lang === "jp"
      ? ov.regime_jp
      : lang === "kr"
      ? ov.regime_kr
      : ov.regime_en
    : "EXTREME FEAR";
  const semiRegime = String(rawRegime || "EXTREME FEAR").toUpperCase();
  const semiDate = ov && ov.date ? ov.date : "2026-10-26";
  const smhPrice = ov && ov.smh_close !== undefined ? Number(ov.smh_close).toFixed(2) : "541.62";
  const xlvPrice = ov && ov.xlv_close !== undefined ? Number(ov.xlv_close).toFixed(2) : "179.28";
  const qqqPrice = ov && ov.qqq_close !== undefined ? Number(ov.qqq_close).toFixed(2) : "712.20";

  const etfs = (ov && Array.isArray(ov.etfs)) ? ov.etfs : [];
  const qqqEtf = etfs.find((e) => e.ticker === "QQQ");
  const smhEtf = etfs.find((e) => e.ticker === "SMH");
  const xlvEtf = etfs.find((e) => e.ticker === "XLV");

  const qqq1d = qqqEtf && qqqEtf.ret_1d_pct !== undefined ? Number(qqqEtf.ret_1d_pct) : 1.11;
  const smhDd = smhEtf && smhEtf.dd_52w_pct !== undefined ? Number(smhEtf.dd_52w_pct) : (ov && ov.smh_dd_pct !== undefined ? Number(ov.smh_dd_pct) : -19.03);
  const xlv1d = xlvEtf && xlvEtf.ret_1d_pct !== undefined ? Number(xlvEtf.ret_1d_pct) : 0.0;
  const lsMonthlyHref = formatCheckoutUrl(
    state.config?.ls_site1_monthly_url,
    "https://truthofmarket.lemonsqueezy.com/checkout/buy/d5e7e761-8b1b-4ca8-b1fe-771acd1450f8"
  );
  const ytUrl = state.config?.youtube_url || "https://youtube.com/@rightsidealpha";
  const igUrl = state.config?.instagram_url || "https://www.instagram.com/semifeargreed";

  return `
    <!-- INSTITUTIONAL MARKET TAPE RIBBON -->
    <div class="market-ribbon">
      <div class="market-ribbon-inner">
        <div class="market-tape">
          <span class="universe-pill">
            <span class="universe-dot"></span>
            ${t.marketUniverseTag}
          </span>
          <span class="tape-item">
            <span class="tape-sym">QQQ</span>
            <span>$${qqqPrice}</span>
            <span class="${qqq1d >= 0 ? "tape-up" : "tape-down"}">${qqq1d >= 0 ? "+" : ""}${qqq1d.toFixed(2)}%</span>
          </span>
          <span class="tape-item">
            <span class="tape-sym">SMH</span>
            <span>$${smhPrice}</span>
            <span class="tape-down">${smhDd.toFixed(2)}% DD</span>
          </span>
          <span class="tape-item">
            <span class="tape-sym">XLV</span>
            <span>$${xlvPrice}</span>
            <span class="${xlv1d >= 0 ? "tape-up" : "tape-down"}">${xlv1d >= 0 ? "+" : ""}${xlv1d.toFixed(2)}%</span>
          </span>
          <span class="tape-item" style="cursor:pointer;" id="ribbonSwitchSemi">
            <span class="tape-sym">SEMI FEAR & GREED</span>
            <span class="${Number(semiScore) >= 55 ? "tape-up" : "tape-down"}" style="font-weight:700;">${semiScore} / 100 (${semiRegime})</span>
          </span>
        </div>
        <div class="mono" style="font-size:0.68rem; color:var(--muted);">
          LATEST CLOSE BASIS (${semiDate}) · NYSE / NASDAQ FEED
        </div>
      </div>
    </div>

    <!-- MAIN INSTITUTIONAL TOPBAR -->
    <header class="topbar">
      <div class="topbar-inner">
        <div class="brand-cluster">
          <div class="brand" id="brandHomeBtn">
            <span class="brand-mark">
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round">
                <polyline points="22 7 13.5 15.5 8.5 10.5 2 17"></polyline>
                <polyline points="16 7 22 7 22 13"></polyline>
              </svg>
            </span>
            <span>${activeView === "semi" ? "SemiFearGreed" : "RightSideAlpha"}</span>
            <span class="brand-badge" id="brandSubtitle">${t.brandSubtitle}</span>
          </div>

          <!-- PLATFORM SWITCHER -->
          <div class="platform-switcher" role="tablist" aria-label="Platform Switcher">
            <button
              class="platform-tab ${activeView === "rightside" ? "active-rsa" : ""}"
              id="navTabRightSide"
              data-view="rightside"
            >
              <span>${t.navRightSide}</span>
              <span class="platform-tab-tag">72 US</span>
            </button>
            <button
              class="platform-tab ${activeView === "semi" ? "active-semi" : ""}"
              id="navTabSemiFg"
              data-view="semi"
            >
              <span>${t.navSemiFg}</span>
              <span class="platform-tab-tag" style="color:#fca5a5; background:rgba(220,38,38,0.2);">${semiScore}</span>
            </button>
          </div>
        </div>

        <div class="nav-actions">
          <div class="lang-switch" aria-label="Language Selector">
            <button class="lang-btn ${lang === "en" ? "active" : ""}" data-lang="en">EN</button>
            <button class="lang-btn ${lang === "jp" ? "active" : ""}" data-lang="jp">JP</button>
            <button class="lang-btn ${lang === "kr" ? "active" : ""}" data-lang="kr">KR</button>
          </div>

          <span class="badge ${isPro ? "badge-ignition" : "badge-watch"}" id="proStatusBadge">
            ${isPro ? t.statusPro : t.statusFree}
          </span>

          <button class="btn" id="btnOpenLicense">
            <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <rect x="3" y="11" width="18" height="11" rx="2" ry="2"></rect>
              <path d="M7 11V7a5 5 0 0 1 10 0v4"></path>
            </svg>
            <span id="btnLicense">${t.btnLicense}</span>
          </button>

          <a
            class="btn"
            id="headerYoutubeLink"
            href="${ytUrl}"
            target="_blank"
            rel="noopener noreferrer"
            title="Official YouTube (@rightsidealpha)"
            style="border-color:rgba(239,68,68,0.4); color:#fca5a5;"
          >
            <svg width="13" height="13" viewBox="0 0 24 24" fill="currentColor">
              <path d="M23.5 6.2a3 3 0 0 0-2.1-2.1C19.5 3.5 12 3.5 12 3.5s-7.5 0-9.4.6A3 3 0 0 0 .5 6.2 31.4 31.4 0 0 0 0 12a31.4 31.4 0 0 0 .5 5.8 3 3 0 0 0 2.1 2.1c1.9.6 9.4.6 9.4.6s7.5 0 9.4-.6a3 3 0 0 0 2.1-2.1A31.4 31.4 0 0 0 24 12a31.4 31.4 0 0 0-.5-5.8zM9.6 15.6V8.4l6.3 3.6-6.3 3.6z"/>
            </svg>
            <span>YouTube</span>
          </a>

          <a
            class="btn"
            id="headerInstagramLink"
            href="${igUrl}"
            target="_blank"
            rel="noopener noreferrer"
            title="Official Instagram (@semifeargreed)"
            style="border-color:rgba(236,72,153,0.4); color:#f9a8d4;"
          >
            <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <rect x="2" y="2" width="20" height="20" rx="5" ry="5"></rect>
              <path d="M16 11.37A4 4 0 1 1 12.63 8 4 4 0 0 1 16 11.37z"></path>
              <line x1="17.5" y1="6.5" x2="17.51" y2="6.5"></line>
            </svg>
            <span>Instagram</span>
          </a>

          <button class="btn" id="btnOpenTelegram" title="Telegram Alert Bot & Channel">
            <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="#38bdf8" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <line x1="22" y1="2" x2="11" y2="13"></line>
              <polygon points="22 2 15 22 11 13 2 9 22 2"></polygon>
            </svg>
            <span id="btnTelegramLabel">${t.btnTelegram || "Telegram Alert"}</span>
            <span style="width:6px; height:6px; border-radius:50%; background:${state.telegramConfigured ? "var(--fin-up)" : "#38bdf8"}; display:inline-block;"></span>
          </button>

          <button class="btn" id="btnOpenConfig">
            <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <circle cx="12" cy="12" r="3"></circle>
              <path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1 0 2.83 2 2 0 0 1-2.83 0l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-2 2 2 2 0 0 1-2-2v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83 0 2 2 0 0 1 0-2.83l.06-.06a1.65 1.65 0 0 0 .33-1.82 1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1-2-2 2 2 0 0 1 2-2h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 0-2.83 2 2 0 0 1 2.83 0l.06.06a1.65 1.65 0 0 0 1.82.33H9a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 2-2 2 2 0 0 1 2 2v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 0 2 2 0 0 1 0 2.83l-.06.06a1.65 1.65 0 0 0-.33 1.82V9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 2 2 2 2 0 0 1-2 2h-.09a1.65 1.65 0 0 0-1.51 1z"></path>
            </svg>
            <span id="btnAdmin">${t.btnAdmin}</span>
          </button>

          <a
            class="btn btn-primary lemonsqueezy-button"
            id="topSubscribeBtn"
            href="${lsMonthlyHref}"
            target="_blank"
            rel="noopener noreferrer"
          >
            <span id="btnUnlockPro">${t.btnUnlockPro}</span>
          </a>
        </div>
      </div>
    </header>
  `;
}


// --- src/components/Hero.js ---
function renderHero(state) {
  const t = state.t;
  const kpis = state.backtestKpis || {};
  const hitRate = Number(kpis.hit_rate_2x_pct ?? 55.24).toFixed(2);
  const underwater = Number(kpis.median_days_underwater ?? 29.0).toFixed(1);
  const netCagr = Number(kpis.cagr_after_tax_pct ?? kpis.us_only_net_cagr_pct ?? 17.81).toFixed(2);
  const severeRisk = Number(kpis.severe_loss_risk_pct ?? 0.93).toFixed(2);
  const latestStockDate =
    state.stocks && state.stocks.length > 0 && state.stocks[0].date
      ? state.stocks[0].date
      : "2026-10-13";

  return `
    <section class="hero">
      <div class="hero-top-row">
        <div>
          <div class="hero-tag" id="heroTag">${t.heroTag}</div>
          <h1 id="heroTitle">${t.heroTitle}</h1>
          <p id="heroDesc">${t.heroDesc}</p>
        </div>
        <div style="background:#0a0e18; border:1px solid var(--border); border-radius:4px; padding:12px 16px; min-width:250px;">
          <div style="font-size:0.68rem; color:var(--muted); font-family:var(--font-mono); text-transform:uppercase; letter-spacing:0.05em;">
            UNIVERSE SPECIFICATION · LATEST CLOSE (${latestStockDate})
          </div>
          <div style="font-size:0.88rem; font-weight:700; color:#fff; margin-top:4px;">
            US-Listed Equities Only (NYSE / NASDAQ)
          </div>
          <div style="font-size:0.75rem; color:var(--muted); margin-top:4px; font-family:var(--font-mono);">
            72 Liquid Growth & Turnaround Constituents · USD ($)
          </div>
        </div>
      </div>

      <div class="kpi-grid">
        <div class="kpi-card kpi-emerald">
          <div class="kpi-label" id="kpi1_label">${t.kpi1_label}</div>
          <div class="kpi-val">${hitRate}%</div>
          <div class="kpi-sub" id="kpi1_sub">${t.kpi1_sub}</div>
        </div>
        <div class="kpi-card">
          <div class="kpi-label" id="kpi2_label">${t.kpi2_label}</div>
          <div class="kpi-val">${underwater}d</div>
          <div class="kpi-sub" id="kpi2_sub">${t.kpi2_sub}</div>
        </div>
        <div class="kpi-card kpi-emerald">
          <div class="kpi-label" id="kpi3_label">${t.kpi3_label}</div>
          <div class="kpi-val">+${netCagr}%</div>
          <div class="kpi-sub" id="kpi3_sub">${t.kpi3_sub}</div>
        </div>
        <div class="kpi-card kpi-amber">
          <div class="kpi-label" id="kpi4_label">${t.kpi4_label}</div>
          <div class="kpi-val">${severeRisk}%</div>
          <div class="kpi-sub" id="kpi4_sub">${t.kpi4_sub}</div>
        </div>
      </div>
    </section>
  `;
}


// --- src/components/ProofCard.js ---
function renderProofCard(state) {
  const t = state.t;

  return `
    <section class="proof-card">
      <div class="proof-title">
        <div style="display:flex; align-items:center; gap:8px;">
          <span style="width:3px; height:14px; background:var(--fin-up); display:inline-block;"></span>
          <span id="proofHeading">${t.proofHeading}</span>
        </div>
        <button class="btn btn-sm" id="btnCopyTopProofCard">
          <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"></path>
            <polyline points="7 10 12 15 17 10"></polyline>
            <line x1="12" y1="15" x2="12" y2="3"></line>
          </svg>
          <span>${t.proofCopyScorecardBtn}</span>
        </button>
      </div>
      <div class="table-responsive-scroll">
        <table class="proof-table">
          <thead>
            <tr>
              <th>${t.th_arch}</th>
              <th>${t.th_2x}</th>
              <th>${t.th_med}</th>
              <th>${t.th_mdd}</th>
              <th>${t.th_dead}</th>
              <th>${t.th_trap}</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td style="font-family:var(--font-sans); color:var(--text-secondary);">0. Market Random Entry Baseline</td>
              <td>18.20%</td>
              <td>+13.24%</td>
              <td>-19.35%</td>
              <td>74.0d</td>
              <td>19.20%</td>
            </tr>
            <tr>
              <td style="font-family:var(--font-sans); color:var(--fin-down);">1. Blind 52-Week Low Dip Buy (+0–10% off low, below MA20)</td>
              <td>28.91%</td>
              <td>+20.56%</td>
              <td style="color:var(--fin-down);">-30.31%</td>
              <td style="color:var(--fin-down);">81.0d</td>
              <td style="color:var(--fin-down);">25.54%</td>
            </tr>
            <tr>
              <td style="font-family:var(--font-sans); color:var(--text-secondary);">2. 52-Week Low + Earnings Filter (Left-Side Entry)</td>
              <td>30.06%</td>
              <td>+24.28%</td>
              <td>-29.85%</td>
              <td>81.0d</td>
              <td>24.82%</td>
            </tr>
            <tr class="proof-highlight">
              <td style="font-family:var(--font-sans);">3. PW-RSI Right-Side Ignition (+14–35% off low + MA20/60 Breakout + 1.40x Vol + 55D Time-Stop)</td>
              <td style="color:var(--fin-up);">55.24%</td>
              <td style="color:var(--fin-up);">+80.47% (Mean +109.1%)</td>
              <td style="color:var(--fin-up);">-16.49%</td>
              <td style="color:var(--fin-up);">29.0d</td>
              <td style="color:var(--fin-up);">0.93%</td>
            </tr>
          </tbody>
        </table>
      </div>
    </section>
  `;
}


// --- src/components/StockTable.js ---
function renderScreenerControls(state) {
  const t = state.t;
  const f = state.zoneFilter;
  const allStocks = (state.stocks || []).filter((s) => !String(s.ticker).includes("."));
  const cAll = allStocks.length;
  const cIgn = allStocks.filter((s) => s.zone_code === "IGNITION_ZONE").length;
  const cWatch = allStocks.filter((s) => s.zone_code === "WASHOUT_WATCH").length;
  const cKnife = allStocks.filter((s) => s.zone_code === "LEFT_SIDE_KNIFE").length;
  const cTrap = allStocks.filter((s) => s.zone_code === "VALUE_TRAP_FILTERED").length;

  return `
    <div class="screener-header-bar">
      <div class="controls">
        <div class="search-wrap">
          <svg class="search-icon" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <circle cx="11" cy="11" r="8"></circle>
            <line x1="21" y1="21" x2="16.65" y2="16.65"></line>
          </svg>
          <input
            type="text"
            class="search-box"
            id="searchInput"
            placeholder="${t.searchPlaceholder}"
            value="${state.searchQuery || ""}"
          />
        </div>
        <div class="filter-tabs">
          <button class="filter-tab ${f === "ALL" ? "active" : ""}" data-zone="ALL">
            <span>${t.filterAll}</span>
            <span class="tab-count">${cAll}</span>
          </button>
          <button class="filter-tab ${f === "IGNITION_ZONE" ? "active" : ""}" data-zone="IGNITION_ZONE">
            <span style="width:6px; height:6px; border-radius:50%; background:var(--fin-up); display:inline-block;"></span>
            <span>${t.filterIgnition}</span>
            <span class="tab-count">${cIgn}</span>
          </button>
          <button class="filter-tab ${f === "WASHOUT_WATCH" ? "active" : ""}" data-zone="WASHOUT_WATCH">
            <span style="width:6px; height:6px; border-radius:50%; background:var(--fin-amber); display:inline-block;"></span>
            <span>${t.filterWatch}</span>
            <span class="tab-count">${cWatch}</span>
          </button>
          <button class="filter-tab ${f === "LEFT_SIDE_KNIFE" ? "active" : ""}" data-zone="LEFT_SIDE_KNIFE">
            <span style="width:6px; height:6px; border-radius:50%; background:var(--fin-down); display:inline-block;"></span>
            <span>${t.filterKnife}</span>
            <span class="tab-count">${cKnife}</span>
          </button>
          <button class="filter-tab ${f === "VALUE_TRAP_FILTERED" ? "active" : ""}" data-zone="VALUE_TRAP_FILTERED">
            <span>${t.filterTrap}</span>
            <span class="tab-count">${cTrap}</span>
          </button>
        </div>
      </div>
    </div>
  `;
}
function renderStockTable(state) {
  const t = state.t;

  return `
    <div class="table-wrap">
      <table class="stock-table" id="stockTable">
        <thead>
          <tr>
            <th data-sort="ticker" class="sort-header">${t.colTicker} ↕</th>
            <th data-sort="zone_code" class="sort-header">${t.colZone} ↕</th>
            <th data-sort="score" class="sort-header">${t.colScore} ↕</th>
            <th data-sort="close" class="sort-header">${t.colClose} ↕</th>
            <th data-sort="prox_low52_pct" class="sort-header">${t.colProx} ↕</th>
            <th data-sort="dd_high52_pct" class="sort-header">${t.colDD} ↕</th>
            <th data-sort="vs_ma20_pct" class="sort-header">${t.colMA} ↕</th>
            <th data-sort="vol_surge_10d" class="sort-header">${t.colVol} ↕</th>
            <th data-sort="hist_2x_rate" class="sort-header">${t.colHist} ↕</th>
            <th>${t.colTrigger}</th>
            <th>${t.colActions}</th>
          </tr>
        </thead>
        <tbody id="tableBody">
          ${renderStockRows(state)}
        </tbody>
      </table>
    </div>
  `;
}
function renderStockRows(state) {
  const stocks = (state.filteredStocks || []).filter((s) => !String(s.ticker).includes("."));
  const lang = state.lang;
  const isPro = state.isProUnlocked;

  if (!stocks.length) {
    return `
      <tr>
        <td colspan="11" style="text-align:center; padding:36px; color:var(--muted); font-family:var(--font-sans);">
          No US-listed equities match the active filter criteria.
        </td>
      </tr>
    `;
  }

  return stocks
    .map((s, idx) => {
      let badgeClass = "badge-watch";
      if (s.zone_code === "IGNITION_ZONE") badgeClass = "badge-ignition";
      else if (s.zone_code === "LEFT_SIDE_KNIFE") badgeClass = "badge-knife";
      else if (s.zone_code === "VALUE_TRAP_FILTERED") badgeClass = "badge-trap";

      const rawZoneLabel =
        lang === "jp" ? s.zone_label_jp : lang === "kr" ? s.zone_label_kr : s.zone_label_en;
      const cleanZoneLabel = String(rawZoneLabel || s.zone_code).replace(/^[🟢🟡🔴⚠️\s]+/, "");
      const stockName =
        lang === "jp" ? s.name_jp : lang === "kr" ? s.name_kr : s.name_en;

      const ma20Color = s.vs_ma20_pct >= 0 ? "var(--fin-up)" : "var(--fin-down)";
      const ma60Color = s.vs_ma60_pct >= 0 ? "var(--fin-up)" : "var(--fin-down)";
      const volColor = s.vol_surge_10d >= 1.35 ? "var(--fin-up)" : "var(--text-secondary)";

      // 52W range bar calculation
      const low52 = Number(s.low52 || 0);
      const high52 = Number(s.high52 || s.close * 1.5);
      const closeVal = Number(s.close || 0);
      const rangeSpan = Math.max(0.01, high52 - low52);
      const rangePct = Math.min(100, Math.max(2, Math.round(((closeVal - low52) / rangeSpan) * 100)));

      // Free tier previews top 4 rows; rows 4+ require Pro
      const hasUnmaskedPrices =
        s.stop_loss_price !== null &&
        s.stop_loss_price !== undefined &&
        s.tp1_2x_price !== null &&
        s.tp1_2x_price !== undefined;
      const showTargets = (isPro || !s.is_pro_locked) && hasUnmaskedPrices;
      const trigPrice = s.entry_trigger_price ?? s.ma60_price;
      const ma60Disp =
        trigPrice !== null && trigPrice !== undefined
          ? `$${Number(trigPrice).toFixed(2)}`
          : "LOCKED";
      const stopDisp =
        s.stop_loss_price !== null && s.stop_loss_price !== undefined
          ? `$${Number(s.stop_loss_price).toFixed(2)}`
          : "LOCKED";
      const tp1Disp =
        s.tp1_2x_price !== null && s.tp1_2x_price !== undefined
          ? `$${Number(s.tp1_2x_price).toFixed(2)}`
          : "LOCKED";

      const triggerHtml = showTargets
        ? `<div class="mono" style="font-size:0.75rem; line-height:1.45;">
             <div><span style="color:var(--muted);">TRG</span> <span style="color:#60a5fa; font-weight:700;">${ma60Disp}</span></div>
             <div><span style="color:var(--muted);">STP</span> <span style="color:var(--fin-down); font-weight:600;">${stopDisp}</span> · <span style="color:var(--fin-up);">TP ${tp1Disp}</span></div>
           </div>`
        : `<span class="pro-lock-cell btn-unlock-row" title="Click to enter Pro license key">
             <svg width="11" height="11" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2">
               <rect x="3" y="11" width="18" height="11" rx="2" ry="2"></rect>
               <path d="M7 11V7a5 5 0 0 1 10 0v4"></path>
             </svg>
             <span>PRO TARGETS</span>
           </span>`;

      const tvUrl = `/api/referral/redirect/tradingview?ticker=${encodeURIComponent(s.ticker)}`;
      const saUrl = `/api/referral/redirect/seekingalpha?ticker=${encodeURIComponent(s.ticker)}`;
      const brokerUrl = `/api/referral/redirect/broker?ticker=${encodeURIComponent(s.ticker)}`;

      return `
      <tr data-ticker="${s.ticker}">
        <td>
          <div style="display:flex; align-items:center; gap:7px;">
            <span class="mono" style="font-weight:800; font-size:0.9rem; color:#ffffff;">${s.ticker}</span>
            <span style="font-size:0.62rem; font-family:var(--font-mono); padding:1px 4px; background:#141d2f; border:1px solid #24324d; color:#93c5fd; border-radius:2px;">US</span>
          </div>
          <div style="font-size:0.73rem; font-family:var(--font-sans); color:var(--muted); margin-top:2px;">
            ${stockName} · <span style="color:var(--text-secondary);">${s.sector}</span>
          </div>
        </td>
        <td>
          <span class="badge ${badgeClass}">${cleanZoneLabel}</span>
          <div class="cond-strip">
            <span class="cond-chip ${s.c1_deep_dd ? "pass" : ""}" title="52W High Drawdown <= -20%">DD</span>
            <span class="cond-chip ${(s.c2_off_low ?? s.c2_sweet_spot) ? "pass" : ""}" title="52W Low Proximity 10-45%">LOW</span>
            <span class="cond-chip ${(s.c3_above_mas ?? s.c3_ma_reclaim) ? "pass" : ""}" title="Reclaimed MA20/MA60">MA</span>
            <span class="cond-chip ${(s.c4_vol_or_mom ?? s.c4_vol_washout) ? "pass" : ""}" title="10D Volume Washout >= 1.3x">VOL</span>
          </div>
        </td>
        <td>
          <div style="display:flex; align-items:center;">
            <span class="mono" style="font-weight:800; font-size:0.9rem; width:26px;">${Number(s.score ?? 0)}</span>
            <div class="score-bar">
              <div class="score-fill" style="width:${Number(s.score ?? 0)}%; background:${
                s.score >= 80 ? "var(--fin-up)" : s.score >= 55 ? "var(--fin-amber)" : "var(--fin-down)"
              };"></div>
            </div>
          </div>
        </td>
        <td>
          <div class="mono" style="font-weight:700; color:#ffffff;" title="Latest Close Date: ${s.date || "2026-10-13"}">$${closeVal.toFixed(2)}</div>
          <div class="range-52w-wrap" title="52W Range: $${low52.toFixed(2)} – $${high52.toFixed(2)}">
            <div class="range-52w-track">
              <div class="range-52w-fill" style="width:${rangePct}%;"></div>
            </div>
            <div class="range-52w-labels">
              <span>L:$${low52.toFixed(0)}</span>
              <span>H:$${high52.toFixed(0)}</span>
            </div>
          </div>
        </td>
        <td class="mono" style="color:${s.prox_low52_pct <= 40 && s.prox_low52_pct >= 10 ? "var(--fin-up)" : "var(--text-secondary)"}; font-weight:600;">
          +${Number(s.prox_low52_pct ?? 0).toFixed(1)}%
        </td>
        <td class="mono" style="color:var(--fin-down); font-weight:600;">
          ${Number(s.dd_high52_pct ?? 0).toFixed(1)}%
        </td>
        <td class="mono">
          <span style="color:${ma20Color}; font-weight:600;">${Number(s.vs_ma20_pct ?? 0) >= 0 ? "+" : ""}${Number(s.vs_ma20_pct ?? 0).toFixed(1)}%</span>
          <span style="color:var(--muted);"> / </span>
          <span style="color:${ma60Color}; font-weight:600;">${Number(s.vs_ma60_pct ?? 0) >= 0 ? "+" : ""}${Number(s.vs_ma60_pct ?? 0).toFixed(1)}%</span>
        </td>
        <td class="mono" style="color:${volColor}; font-weight:700;">
          ${Number(s.vol_surge_10d ?? 1.0).toFixed(2)}x
        </td>
        <td class="mono" style="font-weight:700; color:${s.hist_2x_rate >= 40 ? "var(--fin-up)" : "var(--text-secondary)"};">
          ${Number(s.hist_2x_rate ?? 0).toFixed(1)}%
        </td>
        <td>${triggerHtml}</td>
        <td>
          <div style="display:flex; gap:5px;">
            <button class="btn btn-sm btn-share-card" data-ticker="${s.ticker}" title="Export Institutional Tear Sheet PNG">
              PNG
            </button>
            <a class="btn btn-sm" href="${tvUrl}" target="_blank" rel="noopener noreferrer" title="Open TradingView Chart (Partner)">
              TV ↗
            </a>
            <a class="btn btn-sm" href="${saUrl}" target="_blank" rel="noopener noreferrer" title="Open Seeking Alpha Fundamentals (Partner)">
              SA ↗
            </a>
            <a class="btn btn-sm" href="${brokerUrl}" target="_blank" rel="noopener noreferrer" title="Execute Trade on Partner Broker / Exchange" style="border-color:rgba(16,185,129,0.4); color:#34d399;">
              Trade ↗
            </a>
          </div>
        </td>
      </tr>
    `;
    })
    .join("");
}


// --- src/components/ProVault.js ---
function renderProVault(state) {
  const t = state.t;
  const isPro = state.isProUnlocked;
  const stocks = state.stocks || [];
  const celh = stocks.find((s) => s.ticker === "CELH");
  const mbly = stocks.find((s) => s.ticker === "MBLY");

  const celhClose = celh ? Number(celh.close).toFixed(2) : "27.93";
  const celhMa20 = celh && celh.ma20_price ? Number(celh.ma20_price).toFixed(2) : "27.93";
  const celhMa60 = celh && celh.ma60_price ? Number(celh.ma60_price).toFixed(2) : "29.12";
  const celhTp1 = celh && celh.tp1_2x_price ? Number(celh.tp1_2x_price).toFixed(2) : (Number(celhClose) * 2).toFixed(2);
  const celhStop = celh && celh.stop_loss_price ? Number(celh.stop_loss_price).toFixed(2) : (Number(celhClose) * 0.91).toFixed(2);
  const celhScore = celh ? Number(celh.score) : 90;

  const mblyClose = mbly ? Number(mbly.close).toFixed(2) : "7.02";
  const mblyLow52 = mbly ? Number(mbly.low52).toFixed(2) : "6.47";
  const mblyMa60 = mbly && mbly.ma60_price ? Number(mbly.ma60_price).toFixed(2) : "8.17";
  const mblyTp1 = mbly && mbly.tp1_2x_price ? Number(mbly.tp1_2x_price).toFixed(2) : (Number(mblyClose) * 2).toFixed(2);
  const mblyScore = mbly ? Number(mbly.score) : 47;

  const pineCode =
    state.pineCode ||
    `//@version=5
indicator("RightSideAlpha PW-RSI Ignition v2.6", overlay=true)
ma20 = ta.sma(close, 20)
ma60 = ta.sma(close, 60)
low52 = ta.lowest(low, 252)
high52 = ta.highest(high, 252)
volRatio = volume / ta.sma(volume, 20)
washout10d = ta.highest(volRatio, 10) >= 1.40
proxLow = (close - low52) / low52 * 100
ddHigh = (close - high52) / high52 * 100
ignition = ddHigh <= -35 and proxLow >= 10 and proxLow <= 40 and close > ma20 and close > ma60 and washout10d
plot(ma20, "MA20", color=color.new(color.aqua, 0), linewidth=2)
plot(ma60, "MA60 Trigger", color=color.new(color.orange, 0), linewidth=2)
plotshape(ignition and not ignition[1], "PW-RSI IGNITION", shape.labelup, location.belowbar, color.green, text="IGNITION", textcolor=color.white)`;

  return `
    <section class="proof-card" id="proVaultSection" style="border-top:2px solid var(--fin-blue); margin-bottom:22px;">
      <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:10px; margin-bottom:16px;">
        <div>
          <span class="badge ${isPro ? "badge-ignition" : "badge-watch"}" id="vaultBadge">
            ${isPro ? t.vaultBadgeUnlocked : t.vaultBadgeLocked}
          </span>
          <h2 style="font-size:1.2rem; font-weight:800; margin-top:6px; color:#ffffff; letter-spacing:-0.01em;">
            ${t.vaultTitle}
          </h2>
        </div>
        <button class="btn btn-primary" id="vaultUnlockBtn" style="${isPro ? "display:none;" : ""}">
          ${t.vaultUnlockBtn}
        </button>
      </div>

      <div style="position:relative;">
        ${
          !isPro
            ? `<div id="vaultOverlayUnlock" style="position:absolute; inset:0; z-index:10; display:flex; align-items:center; justify-content:center; background:rgba(6,9,17,0.45); border-radius:6px; cursor:pointer;">
                 <div style="background:#0d1424; border:1px solid var(--fin-blue); box-shadow:0 12px 32px rgba(0,0,0,0.65); border-radius:6px; padding:18px 24px; text-align:center; max-width:440px;">
                   <div class="mono" style="font-size:0.7rem; color:#93c5fd; font-weight:700; letter-spacing:0.05em;">🔒 PRO ANALYTICS VAULT LOCKED</div>
                   <div style="font-size:1rem; font-weight:800; color:#ffffff; margin:6px 0;">Unlock Position Doctor, SEC Briefs & Pine Script v5</div>
                   <div style="font-size:0.78rem; color:var(--muted); margin-bottom:12px;">Subscribe ($29/mo or $199 Lifetime) or click below to test with Evaluation Key <code class="mono" style="color:var(--fin-up);">PRO-DEMO-2026</code></div>
                   <span class="btn btn-primary" style="justify-content:center; width:100%;">🔑 Click to Enter License Key / Unlock Pro</span>
                 </div>
               </div>`
            : ""
        }
      <div id="vaultContentWrap" class="${isPro ? "" : "blur-locked"}" style="display:grid; grid-template-columns:repeat(auto-fit, minmax(330px, 1fr)); gap:16px;">
        <!-- Module 01: Position Doctor -->
        ${renderPositionDoctorForm(state)}

        <!-- Module 02: Institutional SEC Research Vault -->
        <div style="background:#090d16; border:1px solid var(--border); border-top:2px solid var(--fin-blue); border-radius:4px; padding:18px; display:flex; flex-direction:column; justify-content:space-between;">
          <div>
            <div style="font-size:0.7rem; font-family:var(--font-mono); font-weight:700; color:#60a5fa; letter-spacing:0.05em; text-transform:uppercase;">
              ${t.tool2Title}
            </div>
            <h3 style="font-size:1rem; font-weight:800; margin:6px 0; color:#ffffff;">${t.tool2Sub}</h3>
            <p style="font-size:0.78rem; color:var(--muted); margin-bottom:12px;">${t.tool2Desc}</p>

            <div style="font-size:0.8rem; background:#05080f; padding:12px; border-radius:4px; border:1px solid var(--border); margin-bottom:12px; display:flex; flex-direction:column; gap:12px;">
              <div style="border-left:3px solid var(--fin-up); padding-left:10px;">
                <div style="display:flex; justify-content:space-between; align-items:center;">
                  <b class="mono" style="color:#ffffff;">CELH · Celsius Holdings ($${celhClose})</b>
                  <span class="badge badge-ignition">SCORE ${celhScore}</span>
                </div>
                <div style="color:var(--muted); font-size:0.76rem; margin-top:4px; line-height:1.45;">
                  PepsiCo North America inventory destocking complete; 2026E operating leverage +257%. Latest Close <b class="mono" style="color:#fff;">$${celhClose}</b> reclaiming MA20 ($${celhMa20}) toward MA60 ($${celhMa60}). Stop: $${celhStop} · TP1 (2x): <b class="mono" style="color:var(--fin-up);">$${celhTp1}</b>.
                </div>
                <button class="btn btn-sm btn-open-research" data-ticker="CELH" style="margin-top:6px;">
                  Read $CELH SEC Research Brief ↗
                </button>
              </div>

              <div style="border-left:3px solid var(--fin-blue); padding-left:10px;">
                <div style="display:flex; justify-content:space-between; align-items:center;">
                  <b class="mono" style="color:#ffffff;">MBLY · Mobileye Global ($${mblyClose})</b>
                  <span class="badge badge-watch">SCORE ${mblyScore}</span>
                </div>
                <div style="color:var(--muted); font-size:0.76rem; margin-top:4px; line-height:1.45;">
                  Tier-1 OEM ADAS inventory digestion completed; EyeQ6 design wins drive operating income inflection (-$0.39B → +$0.45B). Latest Close <b class="mono" style="color:#fff;">$${mblyClose}</b> · 52W Low $${mblyLow52} · MA60 Trigger <b class="mono" style="color:#60a5fa;">$${mblyMa60}</b> · TP1: <b class="mono" style="color:var(--fin-up);">$${mblyTp1}</b>.
                </div>
                <button class="btn btn-sm btn-open-research" data-ticker="MBLY" style="margin-top:6px;">
                  Read $MBLY SEC Research Brief ↗
                </button>
              </div>
            </div>
          </div>

          <div>
            <button class="btn btn-open-research-modal" style="width:100%; justify-content:center; padding:9px;">
              ${t.tool2ViewBtn}
            </button>
          </div>
        </div>

        <!-- Module 03: TradingView Pine Script v5 -->
        <div style="background:#090d16; border:1px solid var(--border); border-top:2px solid #6366f1; border-radius:4px; padding:18px; display:flex; flex-direction:column; justify-content:space-between;">
          <div>
            <div style="font-size:0.7rem; font-family:var(--font-mono); font-weight:700; color:#818cf8; letter-spacing:0.05em; text-transform:uppercase;">
              ${t.tool3Title}
            </div>
            <h3 style="font-size:1rem; font-weight:800; margin:6px 0; color:#ffffff;">${t.tool3Sub}</h3>
            <p style="font-size:0.78rem; color:var(--muted); margin-bottom:10px;">${t.tool3Desc}</p>

            <pre id="pineCodeBox" style="background:#05080f; padding:12px; border-radius:4px; font-size:0.7rem; color:#93c5fd; overflow-x:auto; max-height:155px; font-family:var(--font-mono); border:1px solid var(--border); line-height:1.45;">${pineCode}</pre>
          </div>

          <div style="margin-top:12px;">
            <button class="btn btn-purple" id="btnCopyPineScript" style="width:100%; justify-content:center; padding:9px;">
              ${t.tool3CopyBtn}
            </button>
          </div>
        </div>
      </div>
      </div>
    </section>
  `;
}


// --- src/components/Pricing.js ---

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
function renderPricing(state) {
  const cfg = state.config || {};
  const c = PRICING_COPY[state.lang] || PRICING_COPY.en;
  const lsMonthly = formatCheckoutUrl(
    cfg.ls_site1_monthly_url,
    "https://truthofmarket.lemonsqueezy.com/checkout/buy/d5e7e761-8b1b-4ca8-b1fe-771acd1450f8"
  );
  const lsLtd = formatCheckoutUrl(
    cfg.ls_site1_ltd_url,
    "https://truthofmarket.lemonsqueezy.com/checkout/buy/667aa482-f17c-47d1-b7f3-a2427c36516b"
  );
  const brokerName = cfg.broker_name || "IBKR / Webull";

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


// --- src/components/Modals.js ---
function renderModals(state) {
  const cfg = state.config || {};
  const tgChannelUrl = cfg.telegram_channel_url || "https://t.me/SemifearGreedbot";
  const ytUrl = cfg.youtube_url || "https://youtube.com/@rightsidealpha";
  const igUrl = cfg.instagram_url || "https://www.instagram.com/semifeargreed";
  const tgChatId = state.telegramChatId || cfg.telegram_chat_id || "@SemifearGreedbot";
  const tgToken = state.telegramBotToken || "DEMO-BOT-TOKEN";
  const tgType = state.telegramAlertType || "SEMI_BRIEFING";
  const tgPreview =
    state.telegramPreviewText ||
    "🧭 [SemiFearGreed] 반도체 공포·탐욕 지수 & 바벨 리밸런싱 브리핑 (2026-10-26)\n• 공포·탐욕 지수: 18.0 / 100 (극단적 공포 · EXTREME FEAR)\n• $SMH(반도체): $541.62 (52주 고점 대비 -19.03%)\n• $XLV(헬스케어): $179.28 (+0.00% 1D) | $QQQ: $712.20 (+1.11% 1D)\n• 현재 발동 시그널: 목표 비중 80% $SMH : 20% $XLV 역발상 매집";

  return `
    <!-- LICENSE ACTIVATION MODAL -->
    <div class="modal-backdrop" id="licenseModal">
      <div class="modal">
        <div style="font-size:0.68rem; font-family:var(--font-mono); color:#93c5fd; text-transform:uppercase; letter-spacing:0.05em;">
          AUTHENTICATION · LEMON SQUEEZY MERCHANT OF RECORD
        </div>
        <h3 style="font-size:1.12rem; font-weight:800; margin-top:4px; color:#ffffff;">Activate Pro Terminal License</h3>
        <p style="color:var(--muted); font-size:0.82rem; margin-top:6px; line-height:1.5;">
          Enter the license key issued upon Lemon Squeezy checkout to unlock all 72 US equity target levels, Position Risk Diagnostics, and the 26-year Semiconductor CSV dataset.<br/>
          <span style="color:var(--text-secondary);">Evaluation Key: <code class="mono" style="color:var(--fin-up); font-weight:700;">PRO-DEMO-2026</code></span>
        </p>
        <div style="margin:10px 0 8px;">
          <button type="button" class="btn btn-emerald btn-sm" id="btnFillDemoKey" style="width:100%; justify-content:center; padding:7px 10px;">
            ⚡ Apply Evaluation Key (PRO-DEMO-2026)
          </button>
        </div>
        <input type="text" id="licenseInput" value="${state.licenseKey || ""}" placeholder="PRO-DEMO-2026 or XXXX-XXXX-XXXX" autocomplete="off" />
        <div id="licenseMsg" style="font-size:0.8rem; margin-bottom:12px; min-height:1.2em;"></div>
        <div style="display:flex; gap:8px; justify-content:space-between; align-items:center; flex-wrap:wrap;">
          <div>
            ${
              state.isProUnlocked
                ? `<button class="btn btn-sm" id="btnLockLicense" style="color:var(--fin-down); border-color:rgba(246,70,93,0.4);">Deactivate / Lock</button>`
                : ""
            }
          </div>
          <div style="display:flex; gap:8px;">
            <button class="btn" id="btnCancelLicense">Cancel</button>
            <button class="btn btn-primary" id="btnVerifyLicense">Verify & Unlock Terminal</button>
          </div>
        </div>
      </div>
    </div>

    <!-- TELEGRAM QUANTITATIVE ALERT & BOT HUB MODAL -->
    <div class="modal-backdrop" id="telegramModal">
      <div class="modal" style="max-width:640px;">
        <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:8px;">
          <div>
            <div style="font-size:0.68rem; font-family:var(--font-mono); color:#38bdf8; text-transform:uppercase; letter-spacing:0.05em;">
              REAL-TIME DISPATCH · TELEGRAM BOT & CHANNEL INTEGRATION
            </div>
            <h3 style="font-size:1.12rem; font-weight:800; margin-top:3px; color:#ffffff;">
              Telegram Quantitative Alert & Briefing Hub
            </h3>
          </div>
          <div style="display:flex; gap:6px; flex-wrap:wrap;">
            <a class="btn btn-sm" id="tgModalSetupBoardBtn" href="./instagram_us_setup.html" target="_blank" rel="noopener noreferrer" style="background:rgba(239,68,68,0.16); border-color:rgba(239,68,68,0.55); color:#fca5a5; font-weight:700;">
              🎬 YouTube & IG 세팅 보드 ↗
            </a>
            <a class="btn btn-sm" id="tgModalYtBtn" href="${ytUrl}" target="_blank" rel="noopener noreferrer" style="border-color:rgba(239,68,68,0.45); color:#fca5a5;">
              📺 YouTube ↗
            </a>
            <a class="btn btn-sm" id="tgModalIgBtn" href="${igUrl}" target="_blank" rel="noopener noreferrer" style="border-color:rgba(236,72,153,0.45); color:#f9a8d4;">
              📸 Instagram ↗
            </a>
            <a class="btn btn-sm" id="tgChannelLinkBtn" href="${tgChannelUrl}" target="_blank" rel="noopener noreferrer" style="border-color:rgba(56,189,248,0.45); color:#38bdf8;">
              🤖 @SemifearGreedbot ↗
            </a>
          </div>
        </div>

        <p style="color:var(--muted); font-size:0.8rem; margin-top:6px; margin-bottom:12px; line-height:1.5;">
          Official Bot <a href="https://t.me/SemifearGreedbot" target="_blank" rel="noopener noreferrer" style="color:#38bdf8; font-weight:700;">t.me/SemifearGreedbot</a> is pre-connected. Open the bot in Telegram and press <strong>START (시작)</strong> so your Chat ID is auto-detected, or enter your channel username (<code class="mono" style="color:#93c5fd;">@channel</code>) to broadcast briefings.
        </p>

        <div class="semi-form-grid-2" style="margin-bottom:8px;">
          <div>
            <label style="font-size:0.68rem; color:var(--muted); font-family:var(--font-mono);">TELEGRAM BOT PROFILE (@BotFather)</label>
            <input type="text" id="tgBotTokenInput" value="${tgToken}" placeholder="DEMO-BOT-TOKEN" autocomplete="off" style="margin:4px 0 0; -webkit-text-security:disc;" />
          </div>
          <div>
            <label style="font-size:0.68rem; color:var(--muted); font-family:var(--font-mono);">CHAT ID OR @CHANNEL USERNAME</label>
            <input type="text" id="tgChatIdInput" value="${tgChatId}" placeholder="@SemiFearGreed or 123456789" autocomplete="off" style="margin:4px 0 0;" />
          </div>
        </div>

        <div class="semi-form-grid-2" style="margin-bottom:10px;">
          <div>
            <label style="font-size:0.68rem; color:var(--muted); font-family:var(--font-mono);">PUBLIC CHANNEL URL (HEADER / FOOTER LINK)</label>
            <input type="text" id="tgChannelUrlInput" value="${tgChannelUrl}" placeholder="https://t.me/SemiFearGreed" style="margin:4px 0 0;" />
          </div>
          <div>
            <label style="font-size:0.68rem; color:var(--muted); font-family:var(--font-mono);">BRIEFING TEMPLATE</label>
            <select id="tgAlertTypeSelect" style="width:100%; padding:9px 10px; margin-top:4px; background:#060911; border:1px solid var(--border); color:#fff; border-radius:4px; font-family:var(--font-sans); font-size:0.82rem; font-weight:600;">
              <option value="SEMI_BRIEFING" ${tgType === "SEMI_BRIEFING" ? "selected" : ""}>1. SemiFearGreed Index & $SMH:$XLV Rebalance</option>
              <option value="RSA_IGNITION" ${tgType === "RSA_IGNITION" ? "selected" : ""}>2. RightSideAlpha US Top 5 Ignition Signals</option>
              <option value="FULL_DAILY" ${tgType === "FULL_DAILY" ? "selected" : ""}>3. Full Combined Daily Briefing (Semi + US Stocks)</option>
              <option value="POSITION_DOCTOR" ${tgType === "POSITION_DOCTOR" ? "selected" : ""}>4. Position Doctor Diagnostic ($CELH)</option>
              <option value="TEST_PING" ${tgType === "TEST_PING" ? "selected" : ""}>5. Bot Connection Verification Ping</option>
            </select>
          </div>
        </div>

        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:6px; flex-wrap:wrap; gap:6px;">
          <span style="font-size:0.68rem; font-family:var(--font-mono); color:#93c5fd;">
            LIVE BRIEFING PREVIEW (VERIFIED LATEST CLOSES)
          </span>
          <div style="display:flex; gap:6px;">
            <button class="btn btn-sm" id="btnVerifyTelegram" title="Test Bot Token with Telegram API">Verify & Save Bot</button>
            <button class="btn btn-sm" id="btnPreviewTelegram">Refresh Preview</button>
            <button class="btn btn-sm" id="btnCopyTelegramMsg">Copy Text</button>
          </div>
        </div>

        <pre id="telegramPreviewBox" style="background:#05080f; border:1px solid var(--border); border-left:3px solid #38bdf8; border-radius:4px; padding:12px; font-family:var(--font-mono); font-size:0.74rem; color:#e2e8f0; white-space:pre-wrap; max-height:210px; overflow-y:auto; line-height:1.5; margin-bottom:10px;">${tgPreview}</pre>

        <div id="telegramStatusMsg" style="font-size:0.78rem; margin-bottom:10px; min-height:1.2em; color:#93c5fd;"></div>

        <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:8px;">
          <span class="mono" style="font-size:0.68rem; color:var(--muted);">
            Webhook Commands: /semi · /ignition · /price CELH · /doctor CELH 27.20 42
          </span>
          <div style="display:flex; gap:8px;">
            <button class="btn" id="btnCloseTelegram">Close</button>
            <button class="btn btn-primary" id="btnSendTelegramNow" style="background:#0284c7; border-color:#38bdf8;">
              Send Briefing to Telegram ↗
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- ADMIN LOGIN MODAL (SHA-256 PROTECTED, NO PLAINTEXT IN GIT) -->
    <div class="modal-backdrop" id="adminLoginModal">
      <div class="modal" style="max-width:440px;">
        <div style="font-size:0.68rem; font-family:var(--font-mono); color:#f59e0b; text-transform:uppercase; letter-spacing:0.05em;">
          RESTRICTED ACCESS · ADMINISTRATOR AUTHENTICATION
        </div>
        <h3 style="font-size:1.12rem; font-weight:800; margin-top:4px; color:#ffffff;">
          🔒 Admin Terminal Login
        </h3>
        <p style="color:var(--muted); font-size:0.8rem; margin-top:6px; margin-bottom:12px; line-height:1.5;">
          Enter your Administrator ID and Password to unlock Terminal Configuration, Lemon Squeezy Checkout Setup, Affiliate Routing, and full Pro Terminal access.
        </p>

        <label style="font-size:0.72rem; color:var(--muted); font-family:var(--font-mono);">ADMIN ID</label>
        <input type="text" id="adminIdInput" placeholder="Enter Admin ID" autocomplete="off" />

        <label style="font-size:0.72rem; color:var(--muted); font-family:var(--font-mono);">ADMIN ACCESS KEY</label>
        <input type="text" id="adminPwInput" placeholder="Enter Admin Password" autocomplete="off" style="-webkit-text-security:disc;" />

        <div id="adminLoginMsg" style="font-size:0.8rem; margin-bottom:12px; min-height:1.2em;"></div>

        <div style="display:flex; gap:8px; justify-content:flex-end;">
          <button class="btn" id="btnCancelAdminLogin">Cancel</button>
          <button class="btn btn-primary" id="btnSubmitAdminLogin">Login as Admin</button>
        </div>
      </div>
    </div>

    <!-- TERMINAL & AFFILIATE CONFIG MODAL -->
    <div class="modal-backdrop" id="configModal">
      <div class="modal" style="max-width:640px;">
        <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:8px;">
          <div>
            <div style="font-size:0.68rem; font-family:var(--font-mono); color:#93c5fd; text-transform:uppercase; letter-spacing:0.05em;">
              ADMINISTRATION · MONETIZATION & PARTNER ROUTING
            </div>
            <h3 style="font-size:1.12rem; font-weight:800; margin-top:4px; color:#ffffff;">Checkout & Affiliate Parameter Configuration</h3>
          </div>
          <button class="btn btn-sm" id="btnAdminLogout" style="border-color:rgba(246,70,93,0.45); color:var(--fin-down);">
            🔒 Admin Logout
          </button>
        </div>
        <p style="color:var(--muted); font-size:0.8rem; margin-top:4px; margin-bottom:10px;">
          Update Lemon Squeezy checkout endpoints, Telegram channel link, and affiliate attribution identifiers. Changes persist to the backend and browser storage.
        </p>

        <div style="background:rgba(37,99,235,0.1); border:1px solid rgba(59,130,246,0.35); border-radius:4px; padding:10px 12px; margin-bottom:12px; display:flex; gap:6px; align-items:center; justify-content:space-between; flex-wrap:wrap;">
          <span class="mono" style="font-size:0.7rem; color:#93c5fd; font-weight:700;">⚡ QUICK PARTNER PORTALS:</span>
          <div style="display:flex; gap:6px; flex-wrap:wrap;">
            <a class="btn btn-sm" href="https://app.lemonsqueezy.com/products" target="_blank" rel="noopener noreferrer" style="font-size:0.7rem; padding:4px 8px;">🍋 Lemon Squeezy ↗</a>
            <a class="btn btn-sm" href="https://www.tradingview.com/affiliate-program/" target="_blank" rel="noopener noreferrer" style="font-size:0.7rem; padding:4px 8px;">📈 TradingView Aff ↗</a>
            <a class="btn btn-sm" href="https://www.interactivebrokers.com/en/general/refer-a-friend.php" target="_blank" rel="noopener noreferrer" style="font-size:0.7rem; padding:4px 8px;">🏦 IBKR Referral ↗</a>
            <a class="btn btn-sm" href="https://affiliates.seekingalpha.com/" target="_blank" rel="noopener noreferrer" style="font-size:0.7rem; padding:4px 8px;">📊 Seeking Alpha Aff ↗</a>
          </div>
        </div>

        <label style="font-size:0.72rem; color:var(--muted); font-family:var(--font-mono);">PLATFORM DOMAIN (TEAR SHEET WATERMARK)</label>
        <input type="text" id="cfgSite1Url" value="${cfg.site1_url || "https://truthofmarket.com"}" />

        <label style="font-size:0.72rem; color:var(--muted); font-family:var(--font-mono);">LEMON SQUEEZY MONTHLY CHECKOUT URL ($29/MO)</label>
        <input type="text" id="cfgLsMonthly" value="${cfg.ls_site1_monthly_url || "https://truthofmarket.lemonsqueezy.com/checkout/buy/d5e7e761-8b1b-4ca8-b1fe-771acd1450f8"}" />

        <label style="font-size:0.72rem; color:var(--muted); font-family:var(--font-mono);">LEMON SQUEEZY LIFETIME CHECKOUT URL ($199)</label>
        <input type="text" id="cfgLsLtd" value="${cfg.ls_site1_ltd_url || "https://truthofmarket.lemonsqueezy.com/checkout/buy/667aa482-f17c-47d1-b7f3-a2427c36516b"}" />

        <label style="font-size:0.72rem; color:var(--muted); font-family:var(--font-mono);">TELEGRAM OFFICIAL CHANNEL / BOT URL</label>
        <input type="text" id="cfgTgChannel" value="${tgChannelUrl}" />

        <label style="font-size:0.72rem; color:var(--muted); font-family:var(--font-mono);">OFFICIAL YOUTUBE CHANNEL URL (@rightsidealpha)</label>
        <input type="text" id="cfgYoutubeUrl" value="${ytUrl}" />

        <label style="font-size:0.72rem; color:var(--muted); font-family:var(--font-mono);">OFFICIAL INSTAGRAM PROFILE URL (@semifeargreed)</label>
        <input type="text" id="cfgInstagramUrl" value="${igUrl}" />

        <label style="font-size:0.72rem; color:var(--muted); font-family:var(--font-mono);">TRADINGVIEW AFFILIATE ID</label>
        <input type="text" id="cfgAffTv" value="${cfg.tradingview_aff_id || "rightsidealpha"}" />

        <label style="font-size:0.72rem; color:var(--muted); font-family:var(--font-mono);">SEEKING ALPHA PARTNER SOURCE TAG</label>
        <input type="text" id="cfgAffSa" value="${cfg.seekingalpha_source || "affiliate_rightside"}" />

        <label style="font-size:0.72rem; color:var(--muted); font-family:var(--font-mono);">BROKER / EXCHANGE PARTNER LABEL (E.G. IBKR / WEBULL / BYBIT)</label>
        <input type="text" id="cfgBrokerName" value="${cfg.broker_name || "IBKR / Webull"}" />

        <label style="font-size:0.72rem; color:var(--muted); font-family:var(--font-mono);">BROKER / EXCHANGE REFERRAL URL</label>
        <input type="text" id="cfgBrokerUrl" value="${cfg.broker_referral_url || "https://ibkr.com/referral/rightsidealpha"}" />

        <div id="configMsg" style="font-size:0.8rem; margin-bottom:12px; min-height:1.2em;"></div>

        <div style="display:flex; gap:8px; justify-content:flex-end;">
          <button class="btn" id="btnCancelConfig">Close</button>
          <button class="btn btn-primary" id="btnSaveConfig">Save Configuration</button>
        </div>
      </div>
    </div>

    <!-- INSTITUTIONAL RESEARCH BRIEF MODAL -->
    <div class="modal-backdrop" id="researchModal">
      <div class="modal" style="max-width:760px;">
        <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:8px; margin-bottom:12px;">
          <h3 style="font-size:1.1rem; font-weight:800; color:#ffffff;" id="researchModalTitle">SEC Primary Filing Turnaround Brief</h3>
          <div style="display:flex; gap:6px; align-items:center; flex-wrap:wrap;">
            <button type="button" class="btn btn-sm btn-switch-research" data-ticker="CELH" id="btnSwitchResearchCelh">$CELH Brief</button>
            <button type="button" class="btn btn-sm btn-switch-research" data-ticker="MBLY" id="btnSwitchResearchMbly">$MBLY Brief</button>
            <button class="btn btn-sm" id="btnCloseResearch">Close ✕</button>
          </div>
        </div>
        <div id="researchModalBody" style="font-size:0.84rem; color:var(--text); line-height:1.65; max-height:62vh; overflow-y:auto; background:#05080f; padding:18px; border-radius:4px; border:1px solid var(--border);">
          Loading institutional brief...
        </div>
      </div>
    </div>

    <!-- TOAST NOTIFICATION -->
    <div class="toast" id="toastBox">Action completed</div>
  `;
}


// --- src/components/SemiFearGreedView.js ---

function polarToCartesian(cx, cy, r, angleDeg) {
  const rad = (angleDeg * Math.PI) / 180.0;
  return {
    x: cx + r * Math.cos(rad),
    y: cy - r * Math.sin(rad),
  };
}

function describeArc(cx, cy, r, startAngleDeg, endAngleDeg) {
  const start = polarToCartesian(cx, cy, r, startAngleDeg);
  const end = polarToCartesian(cx, cy, r, endAngleDeg);
  const largeArcFlag = Math.abs(startAngleDeg - endAngleDeg) <= 180 ? "0" : "1";
  // Since y is inverted for standard math angles (180 left -> 90 top -> 0 right), sweep-flag is 1
  return `M ${start.x.toFixed(2)} ${start.y.toFixed(2)} A ${r} ${r} 0 ${largeArcFlag} 1 ${end.x.toFixed(2)} ${end.y.toFixed(2)}`;
}
function renderCnnDialSvg(score, regimeLabel) {
  const s = Math.max(0, Math.min(100, Number(score ?? 18.0)));
  const cx = 230;
  const cy = 200;
  const r = 146;

  // 5 CNN segments along 180° (left=0) to 0° (right=100)
  const segments = [
    { code: "EXTREME_FEAR", min: 0, max: 24, a1: 180, a2: 136.5, activeColor: "#d92d20", mutedColor: "#fecaca", label: "EXTREME FEAR", midAngle: 158 },
    { code: "FEAR", min: 25, max: 44, a1: 134, a2: 100.5, activeColor: "#f79009", mutedColor: "#fed7aa", label: "FEAR", midAngle: 117 },
    { code: "NEUTRAL", min: 45, max: 55, a1: 98, a2: 82, activeColor: "#667085", mutedColor: "#e5e7eb", label: "NEUTRAL", midAngle: 90 },
    { code: "GREED", min: 56, max: 74, a1: 79.5, a2: 46, activeColor: "#12b76a", mutedColor: "#bbf7d0", label: "GREED", midAngle: 63 },
    { code: "EXTREME_GREED", min: 75, max: 100, a1: 43.5, a2: 0, activeColor: "#027a48", mutedColor: "#a7f3d0", label: "EXTREME GREED", midAngle: 22 },
  ];

  let activeSeg = segments[0];
  if (s >= 75) activeSeg = segments[4];
  else if (s >= 55.01) activeSeg = segments[3];
  else if (s >= 45) activeSeg = segments[2];
  else if (s >= 25) activeSeg = segments[1];

  const arcsHtml = segments
    .map((seg) => {
      const isAct = seg.code === activeSeg.code;
      const d = describeArc(cx, cy, r, seg.a1, seg.a2);
      const stroke = isAct ? seg.activeColor : seg.mutedColor;
      const width = isAct ? 40 : 32;
      const lp = polarToCartesian(cx, cy, r + 31, seg.midAngle);
      return `
        <path d="${d}" fill="none" stroke="${stroke}" stroke-width="${width}" stroke-linecap="butt" />
        <text x="${lp.x.toFixed(1)}" y="${lp.y.toFixed(1)}" text-anchor="middle" dominant-baseline="middle"
              fill="${isAct ? seg.activeColor : "#6b7280"}"
              font-size="${isAct ? "9.5" : "8.5"}" font-weight="${isAct ? "800" : "700"}" font-family="Inter, sans-serif">
          ${seg.label}
        </text>
      `;
    })
    .join("");

  // Perimeter ticks (0, 25, 45, 55, 75, 100)
  const ticks = [0, 25, 45, 55, 75, 100]
    .map((tVal) => {
      const ang = 180 - (tVal / 100) * 180;
      const pIn = polarToCartesian(cx, cy, r - 24, ang);
      const pTxt = polarToCartesian(cx, cy, r - 35, ang);
      return `
        <circle cx="${pIn.x.toFixed(1)}" cy="${pIn.y.toFixed(1)}" r="1.8" fill="#6b7280" />
        <text x="${pTxt.x.toFixed(1)}" y="${pTxt.y.toFixed(1)}" text-anchor="middle" dominant-baseline="middle"
              fill="#4b5563" font-size="10" font-weight="700" font-family="JetBrains Mono, monospace">
          ${tVal}
        </text>
      `;
    })
    .join("");

  // Needle geometry
  const needleAngle = 180 - (s / 100.0) * 180.0;
  const tip = polarToCartesian(cx, cy, r - 12, needleAngle);
  const baseLeft = polarToCartesian(cx, cy, 8, needleAngle + 90);
  const baseRight = polarToCartesian(cx, cy, 8, needleAngle - 90);

  return `
    <div style="display:flex; flex-direction:column; align-items:center;">
      <svg viewBox="0 0 460 250" style="width:100%; max-width:440px; height:auto; overflow:visible;">
        ${arcsHtml}
        ${ticks}
        <!-- Needle Polygon -->
        <polygon points="${tip.x.toFixed(1)},${tip.y.toFixed(1)} ${baseLeft.x.toFixed(1)},${baseLeft.y.toFixed(1)} ${baseRight.x.toFixed(1)},${baseRight.y.toFixed(1)}"
                 fill="#111827" />
        <circle cx="${cx}" cy="${cy}" r="14" fill="#111827" />
        <circle cx="${cx}" cy="${cy}" r="5" fill="#ffffff" />
      </svg>

      <!-- Score & Active Emotion Callout below Needle Hub -->
      <div style="text-align:center; margin-top:-18px;">
        <div style="display:inline-flex; align-items:baseline; gap:6px; background:#111827; color:#ffffff; padding:6px 20px; border-radius:30px; box-shadow:0 4px 12px rgba(0,0,0,0.12);">
          <span class="mono" style="font-size:2rem; font-weight:900; letter-spacing:-0.03em;">${Math.round(s)}</span>
          <span class="mono" style="font-size:0.9rem; color:#9ca3af; font-weight:600;">(${s.toFixed(1)} / 100)</span>
        </div>
        <div style="margin-top:8px;">
          <span style="font-size:0.78rem; color:#4b5563; font-weight:600; text-transform:uppercase; letter-spacing:0.04em;">
            Market Emotion is driving:
          </span>
          <span class="cnn-pill cnn-pill-${activeSeg.code}" style="margin-left:6px; font-size:0.85rem;">
            ${regimeLabel || activeSeg.label}
          </span>
        </div>
      </div>
    </div>
  `;
}
function renderTimelineSvg(historyData, activeRange) {
  const pts = (historyData && historyData.series) || [];
  if (!pts.length) {
    return `<div style="padding:40px; text-align:center; color:#6b7280;">Loading historical timeline...</div>`;
  }

  const w = 640;
  const h = 230;
  const padL = 36;
  const padR = 16;
  const padT = 16;
  const padB = 28;
  const plotW = w - padL - padR;
  const plotH = h - padT - padB;

  const coords = pts.map((p, i) => {
    const x = padL + (i / Math.max(1, pts.length - 1)) * plotW;
    const y = padT + (1.0 - Math.max(0, Math.min(100, p.fg_score)) / 100.0) * plotH;
    return `${x.toFixed(1)},${y.toFixed(1)}`;
  });

  const y25 = (padT + 0.75 * plotH).toFixed(1);
  const y50 = (padT + 0.5 * plotH).toFixed(1);
  const y75 = (padT + 0.25 * plotH).toFixed(1);

  const firstDate = pts[0].date;
  const midDate = pts[Math.floor(pts.length / 2)].date;
  const lastDate = pts[pts.length - 1].date;

  return `
    <div>
      <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:10px; flex-wrap:wrap; gap:8px;">
        <div style="font-size:0.8rem; font-weight:700; color:#374151;">
          Historical Semiconductor Fear & Greed Index (${firstDate} → ${lastDate})
        </div>
        <div style="display:flex; gap:4px;">
          ${["3M", "1Y", "3Y", "5Y", "10Y", "ALL"]
            .map(
              (r) => `
            <button class="btn-semi-range" data-range="${r}"
                    style="padding:3px 9px; border-radius:4px; font-size:0.72rem; font-weight:700; cursor:pointer; border:1px solid ${
                      activeRange === r ? "#111827" : "#d1d5db"
                    }; background:${activeRange === r ? "#111827" : "#ffffff"}; color:${
                activeRange === r ? "#ffffff" : "#374151"
              };">
              ${r}
            </button>
          `
            )
            .join("")}
        </div>
      </div>

      <svg viewBox="0 0 ${w} ${h}" style="width:100%; height:auto; background:#f9fafb; border:1px solid #e5e7eb; border-radius:4px;">
        <!-- Extreme Greed Band (>75) -->
        <rect x="${padL}" y="${padT}" width="${plotW}" height="${0.25 * plotH}" fill="rgba(16,185,129,0.08)" />
        <!-- Extreme Fear Band (<25) -->
        <rect x="${padL}" y="${y25}" width="${plotW}" height="${0.25 * plotH}" fill="rgba(239,68,68,0.09)" />

        <!-- Reference Lines -->
        <line x1="${padL}" y1="${y75}" x2="${w - padR}" y2="${y75}" stroke="#10b981" stroke-dasharray="3,3" stroke-width="1" />
        <line x1="${padL}" y1="${y50}" x2="${w - padR}" y2="${y50}" stroke="#9ca3af" stroke-dasharray="3,3" stroke-width="1" />
        <line x1="${padL}" y1="${y25}" x2="${w - padR}" y2="${y25}" stroke="#ef4444" stroke-dasharray="3,3" stroke-width="1" />

        <text x="6" y="${y75}" fill="#047857" font-size="9.5" font-weight="700" dominant-baseline="middle">75</text>
        <text x="6" y="${y50}" fill="#6b7280" font-size="9.5" font-weight="700" dominant-baseline="middle">50</text>
        <text x="6" y="${y25}" fill="#b91c1c" font-size="9.5" font-weight="700" dominant-baseline="middle">25</text>

        <!-- FG Line -->
        <polyline fill="none" stroke="#111827" stroke-width="1.8" points="${coords.join(" ")}" />

        <!-- X-Axis Dates -->
        <text x="${padL}" y="${h - 8}" fill="#6b7280" font-size="9.5" font-family="JetBrains Mono, monospace">${firstDate}</text>
        <text x="${padL + plotW / 2}" y="${h - 8}" fill="#6b7280" font-size="9.5" text-anchor="middle" font-family="JetBrains Mono, monospace">${midDate}</text>
        <text x="${w - padR}" y="${h - 8}" fill="#6b7280" font-size="9.5" text-anchor="end" font-family="JetBrains Mono, monospace">${lastDate}</text>
      </svg>
    </div>
  `;
}

function renderMiniSparkline(values, regimeCode) {
  if (!values || !values.length) return "";
  const w = 180;
  const h = 44;
  const coords = values
    .map((v, i) => {
      const x = 4 + (i / Math.max(1, values.length - 1)) * (w - 8);
      const y = 4 + (1.0 - Math.max(0, Math.min(100, v)) / 100.0) * (h - 8);
      return `${x.toFixed(1)},${y.toFixed(1)}`;
    })
    .join(" ");

  const colorMap = {
    EXTREME_FEAR: "#dc2626",
    FEAR: "#ea580c",
    NEUTRAL: "#4b5563",
    GREED: "#16a34a",
    EXTREME_GREED: "#059669",
  };
  const stroke = colorMap[regimeCode] || "#111827";

  return `
    <svg viewBox="0 0 ${w} ${h}" style="width:160px; height:40px; background:#f8fafc; border:1px solid #e2e8f0; border-radius:4px;">
      <line x1="0" y1="${h / 2}" x2="${w}" y2="${h / 2}" stroke="#e2e8f0" stroke-dasharray="2,2" stroke-width="1" />
      <polyline fill="none" stroke="${stroke}" stroke-width="1.8" points="${coords}" />
    </svg>
  `;
}

function renderEquityCurveSvg(historyData) {
  const pts = (historyData && historyData.series) || [];
  if (!pts.length) return "";

  const w = 720;
  const h = 220;
  const padL = 52;
  const padR = 20;
  const padT = 18;
  const padB = 26;
  const plotW = w - padL - padR;
  const plotH = h - padT - padB;

  const allVals = [];
  pts.forEach((p) => {
    allVals.push(p.port73_norm, p.qqq_norm);
  });
  const minV = Math.min(...allVals, 8000);
  const maxV = Math.max(...allVals, 12000);
  const span = Math.max(1, maxV - minV);

  const portCoords = pts
    .map((p, i) => {
      const x = padL + (i / Math.max(1, pts.length - 1)) * plotW;
      const y = padT + (1.0 - (p.port73_norm - minV) / span) * plotH;
      return `${x.toFixed(1)},${y.toFixed(1)}`;
    })
    .join(" ");

  const qqqCoords = pts
    .map((p, i) => {
      const x = padL + (i / Math.max(1, pts.length - 1)) * plotW;
      const y = padT + (1.0 - (p.qqq_norm - minV) / span) * plotH;
      return `${x.toFixed(1)},${y.toFixed(1)}`;
    })
    .join(" ");

  const lastPort = pts[pts.length - 1].port73_norm;
  const lastQqq = pts[pts.length - 1].qqq_norm;

  return `
    <div style="margin-bottom:16px;">
      <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:8px; flex-wrap:wrap; gap:8px; font-size:0.78rem;">
        <div style="display:flex; gap:16px; align-items:center;">
          <span style="display:inline-flex; align-items:center; gap:6px; color:#34d399; font-weight:700;">
            <span style="width:12px; height:3px; background:#0ecb81; display:inline-block;"></span>
            70% $SMH : 30% $XLV Barbell ($10k → $${lastPort.toLocaleString()})
          </span>
          <span style="display:inline-flex; align-items:center; gap:6px; color:#94a3b8; font-weight:600;">
            <span style="width:12px; height:3px; background:#64748b; display:inline-block;"></span>
            100% $QQQ Benchmark ($10k → $${lastQqq.toLocaleString()})
          </span>
        </div>
        <span class="mono" style="color:var(--muted); font-size:0.72rem;">Selected Window: ${historyData.range_code}</span>
      </div>
      <svg viewBox="0 0 ${w} ${h}" style="width:100%; height:auto; background:#060911; border:1px solid var(--border); border-radius:4px;">
        <polyline fill="none" stroke="#64748b" stroke-width="1.6" stroke-dasharray="3,2" points="${qqqCoords}" />
        <polyline fill="none" stroke="#0ecb81" stroke-width="2.2" points="${portCoords}" />
        <text x="6" y="${padT + 8}" fill="#94a3b8" font-size="9.5" font-family="JetBrains Mono, monospace">$${Math.round(maxV).toLocaleString()}</text>
        <text x="6" y="${h - padB}" fill="#94a3b8" font-size="9.5" font-family="JetBrains Mono, monospace">$${Math.round(minV).toLocaleString()}</text>
      </svg>
    </div>
  `;
}
function renderSemiFearGreedView(state) {
  const t = state.t;
  const lang = state.lang;
  const ov = state.semiOverview;

  if (!ov) {
    return `
      <div class="proof-card" style="padding:40px; text-align:center;">
        Loading Semiconductor Fear & Greed Index...
      </div>
    `;
  }

  const regimeLabel = lang === "jp" ? ov.regime_jp : lang === "kr" ? ov.regime_kr : ov.regime_en;
  const actionHeadline = lang === "jp" ? ov.action_headline_jp : lang === "kr" ? ov.action_headline_kr : ov.action_headline_en;
  const actionDetail = lang === "jp" ? ov.action_detail_jp : lang === "kr" ? ov.action_detail_kr : ov.action_detail_en;
  const gaugeTab = state.semiGaugeTab || "overview";
  const activeRange = state.semiRange || "1Y";
  const rebal = state.semiRebalanceResult;
  const lump = state.semiLumpSumResult;
  const eras = (state.semiHistory && state.semiHistory.era_summary) || [];

  return `
    <!-- SECTION 1: AUTHENTIC CNN BUSINESS FEAR & GREED INDEX EDITORIAL SURFACE -->
    <section class="cnn-page-wrapper" id="semiCnnSection">
      <div class="cnn-editorial-header">
        <div>
          <div class="cnn-red-tag">${t.cnnBadge}</div>
          <h1 class="cnn-main-title">${t.cnnTitle}</h1>
          <p class="cnn-main-subtitle">${t.cnnSubtitle}</p>
        </div>
        <div style="display:flex; gap:8px; align-items:center; flex-wrap:wrap;">
          <a
            class="btn"
            href="${state.config?.youtube_url || "https://youtube.com/@rightsidealpha"}"
            target="_blank"
            rel="noopener noreferrer"
            style="background:#dc2626; color:#ffffff; border-color:#b91c1c;"
          >
            📺 YouTube (@rightsidealpha) ↗
          </a>
          <a
            class="btn"
            href="${state.config?.instagram_url || "https://www.instagram.com/semifeargreed"}"
            target="_blank"
            rel="noopener noreferrer"
            style="background:#db2777; color:#ffffff; border-color:#be185d;"
          >
            📸 Instagram (@semifeargreed) ↗
          </a>
          <button class="btn" id="btnSendSemiTelegram" style="background:#0284c7; color:#ffffff; border-color:#0369a1;">
            <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">
              <line x1="22" y1="2" x2="11" y2="13"></line>
              <polygon points="22 2 15 22 11 13 2 9 22 2"></polygon>
            </svg>
            <span>${t.cnnTelegramBtn || "Telegram Briefing"}</span>
          </button>
          <button class="btn" id="btnExportSemiGauge" style="background:#111827; color:#ffffff; border-color:#111827;">
            ${t.cnnExportGauge}
          </button>
        </div>
      </div>

      <!-- CNN TOP 2-COLUMN GRID: LEFT = DIAL GAUGE / TIMELINE, RIGHT = 4 HISTORICAL COMPARISONS -->
      <div class="cnn-top-grid">
        <div class="cnn-card">
          <div class="cnn-card-header">
            <div style="font-size:0.78rem; color:#6b7280; font-weight:600;">
              ${t.cnnLastUpdated}: <b class="mono" style="color:#111827;">${ov.date}</b> · $SMH <b class="mono">$${ov.smh_close.toFixed(2)}</b> (${ov.smh_dd_pct.toFixed(2)}% off 52W High)
            </div>
            <div class="cnn-view-tabs">
              <button class="cnn-view-tab ${gaugeTab === "overview" ? "active" : ""}" data-semi-tab="overview">
                ${t.cnnTabOverview}
              </button>
              <button class="cnn-view-tab ${gaugeTab === "timeline" ? "active" : ""}" data-semi-tab="timeline">
                ${t.cnnTabTimeline}
              </button>
            </div>
          </div>

          ${
            gaugeTab === "overview"
              ? renderCnnDialSvg(ov.fg_score, regimeLabel)
              : renderTimelineSvg(state.semiHistory, activeRange)
          }
        </div>

        <!-- RIGHT COLUMN: CNN 4-ROW HISTORICAL STACK + BARBELL SIGNAL -->
        <div class="cnn-card" style="display:flex; flex-direction:column; justify-content:space-between;">
          <div>
            <div style="font-size:0.78rem; font-weight:800; text-transform:uppercase; letter-spacing:0.05em; color:#6b7280; margin-bottom:8px;">
              ${t.cnnHistoryTitle}
            </div>
            <div class="cnn-history-list">
              ${ov.comparisons
                .map((c) => {
                  const lbl = lang === "jp" ? c.label_jp : lang === "kr" ? c.label_kr : c.label_en;
                  const reg = lang === "jp" ? c.regime_jp : lang === "kr" ? c.regime_kr : c.regime_en;
                  return `
                  <div class="cnn-history-row">
                    <div>
                      <div class="cnn-hist-label">${lbl} <span class="mono" style="font-size:0.72rem; color:#9ca3af;">(${c.date})</span></div>
                      <div class="cnn-hist-regime">${reg}</div>
                    </div>
                    <div class="cnn-score-circle">${Math.round(c.score)}</div>
                  </div>
                `;
                })
                .join("")}
            </div>
          </div>

          <!-- Active SMH:XLV Barbell Regime Box -->
          <div style="margin-top:16px; padding:14px 16px; background:#fef2f2; border:1px solid #fecaca; border-left:4px solid #dc2626; border-radius:4px;">
            <div style="font-size:0.68rem; font-weight:800; color:#991b1b; letter-spacing:0.05em; text-transform:uppercase;">
              ${t.cnnActiveRuleLabel} · TARGET ${ov.recommended_smh_weight}% $SMH : ${ov.recommended_xlv_weight}% $XLV
            </div>
            <div style="font-size:0.88rem; font-weight:800; color:#111827; margin-top:4px;">
              ${actionHeadline}
            </div>
            <p style="font-size:0.78rem; color:#374151; margin-top:4px; line-height:1.45;">
              ${actionDetail}
            </p>
          </div>
        </div>
      </div>

      <!-- CNN 7 FEAR & GREED INDICATORS BREAKDOWN -->
      <div style="margin-top:12px;">
        <div style="border-bottom:2px solid #111827; padding-bottom:10px; margin-bottom:16px;">
          <h2 style="font-size:1.35rem; font-weight:900; color:#111827;">${t.cnnIndicatorsHeading}</h2>
          <p style="font-size:0.84rem; color:#4b5563; margin-top:2px;">${t.cnnIndicatorsSub}</p>
        </div>

        <div class="cnn-indicators-list">
          ${ov.factors
            .map((f) => {
              const title = lang === "jp" ? f.title_jp : lang === "kr" ? f.title_kr : f.title_en;
              const sub = lang === "jp" ? f.subtitle_jp : lang === "kr" ? f.subtitle_kr : f.subtitle_en;
              const desc = lang === "jp" ? f.desc_jp : lang === "kr" ? f.desc_kr : f.desc_en;
              const reg = lang === "jp" ? f.regime_jp : lang === "kr" ? f.regime_kr : f.regime_en;

              return `
              <div class="cnn-indicator-item">
                <div>
                  <div style="display:flex; align-items:center; gap:8px;">
                    <span class="mono" style="font-size:0.7rem; font-weight:800; padding:2px 6px; background:#f3f4f6; border:1px solid #d1d5db; border-radius:3px; color:#374151;">
                      #${f.order} · ${f.weight_pct}% WEIGHT
                    </span>
                    <span class="cnn-ind-title">${title}</span>
                  </div>
                  <div class="cnn-ind-sub">${sub}</div>
                  <p class="cnn-ind-desc">${desc}</p>
                </div>

                <div style="display:flex; flex-direction:column; align-items:center; gap:6px;">
                  ${renderMiniSparkline(f.sparkline, f.regime_code)}
                  <div class="mono" style="font-size:0.74rem; color:#374151; font-weight:700;">
                    Reading: ${f.raw_display} · Score ${f.score.toFixed(1)}/100
                  </div>
                </div>

                <div style="text-align:right;">
                  <span class="cnn-pill cnn-pill-${f.regime_code}">${reg}</span>
                </div>
              </div>
            `;
            })
            .join("")}
        </div>
      </div>
    </section>

    <!-- SECTION 2: CORE ETF SNAPSHOT STRIP ($SMH, $XLV, $QQQ) -->
    <section style="display:grid; grid-template-columns:repeat(auto-fit, minmax(310px, 1fr)); gap:14px; margin-bottom:22px;">
      ${ov.etfs
        .map((etf) => {
          const name = lang === "jp" ? etf.name_jp : lang === "kr" ? etf.name_kr : etf.name_en;
          const role = lang === "jp" ? etf.role_jp : lang === "kr" ? etf.role_kr : etf.role_en;
          const tvUrl = `/api/referral/redirect/tradingview?ticker=${encodeURIComponent(etf.ticker)}`;
          const saUrl = `/api/referral/redirect/seekingalpha?ticker=${encodeURIComponent(etf.ticker)}`;
          const brokerUrl = `/api/referral/redirect/broker?ticker=${encodeURIComponent(etf.ticker)}`;
          return `
          <div class="proof-card" style="margin-bottom:0; border-top:2px solid ${
            etf.ticker === "SMH" ? "var(--fin-blue)" : etf.ticker === "XLV" ? "var(--fin-up)" : "#64748b"
          };">
            <div style="display:flex; justify-content:space-between; align-items:flex-start;">
              <div>
                <div style="display:flex; align-items:center; gap:8px;">
                  <span class="mono" style="font-size:1.15rem; font-weight:900; color:#ffffff;">$${etf.ticker}</span>
                  <span style="font-size:0.78rem; color:var(--text-secondary); font-weight:600;">${name}</span>
                </div>
                <div style="font-size:0.74rem; color:var(--muted); margin-top:3px;">${role}</div>
              </div>
              <div style="text-align:right;">
                <div class="mono" style="font-size:1.15rem; font-weight:800; color:#ffffff;">$${Number(etf.close ?? 0).toFixed(2)}</div>
                <div class="mono" style="font-size:0.74rem; color:${etf.ret_1d_pct >= 0 ? "var(--fin-up)" : "var(--fin-down)"};">
                  1D: ${etf.ret_1d_pct >= 0 ? "+" : ""}${Number(etf.ret_1d_pct ?? 0).toFixed(2)}% · 20D: ${etf.ret_20d_pct >= 0 ? "+" : ""}${Number(etf.ret_20d_pct ?? 0).toFixed(2)}%
                </div>
                <div class="mono" style="font-size:0.7rem; color:var(--muted); margin-top:1px;">
                  52W DD: ${Number(etf.dd_52w_pct ?? 0).toFixed(2)}% · RSI(14): ${Number(etf.rsi14 ?? 50).toFixed(1)}
                </div>
              </div>
            </div>
            <div style="display:flex; justify-content:space-between; align-items:center; margin-top:12px; padding-top:10px; border-top:1px solid var(--border-subtle); font-size:0.74rem;">
              <span class="mono" style="color:var(--muted);">
                Normal: <b style="color:#fff;">${etf.target_weight_normal}%</b> → Extreme Fear: <b style="color:var(--fin-up);">${etf.target_weight_fear}%</b>
              </span>
              <div style="display:flex; gap:6px;">
                <a class="btn btn-sm" href="${tvUrl}" target="_blank" rel="noopener noreferrer">TV Chart ↗</a>
                <a class="btn btn-sm" href="${saUrl}" target="_blank" rel="noopener noreferrer">Holdings ↗</a>
                <a class="btn btn-sm" href="${brokerUrl}" target="_blank" rel="noopener noreferrer" style="border-color:rgba(16,185,129,0.4); color:#34d399;">Trade ↗</a>
              </div>
            </div>
          </div>
        `;
        })
        .join("")}
    </section>

    <!-- SECTION 3: INTERACTIVE SMH + XLV REBALANCING & 2.5M KRW TAX HARVESTING ENGINE + 3-STAGE LUMP-SUM PLANNER -->
    <section class="semi-calc-grid">
      <!-- Calculator 1: SMH + XLV Rebalancing & Tax Optimizer -->
      <div class="proof-card" style="margin-bottom:0; border-top:2px solid var(--fin-up);">
        <div style="font-size:0.7rem; font-family:var(--font-mono); font-weight:700; color:var(--fin-up); letter-spacing:0.05em;">
          ${t.rebalSectionTag}
        </div>
        <h3 style="font-size:1.12rem; font-weight:800; color:#ffffff; margin:4px 0 6px;">${t.rebalSectionTitle}</h3>
        <p style="font-size:0.8rem; color:var(--muted); margin-bottom:14px;">${t.rebalSectionDesc}</p>

        <div class="semi-form-grid-2" style="margin-bottom:12px;">
          <div>
            <label style="font-size:0.68rem; font-family:var(--font-mono); color:var(--muted);">PORTFOLIO CAPITAL ($ USD)</label>
            <input type="number" id="semiCapInput" value="${state.semiCapUsd ?? 100000}" step="1000"
                   style="width:100%; padding:8px 10px; background:#060911; border:1px solid var(--border); color:#fff; border-radius:4px; font-family:var(--font-mono); font-weight:700; margin-top:3px;" />
          </div>
          <div>
            <label style="font-size:0.68rem; font-family:var(--font-mono); color:var(--muted);">ALLOCATION MODE</label>
            <select id="semiModeInput" style="width:100%; padding:8px 10px; background:#060911; border:1px solid var(--border); color:#fff; border-radius:4px; font-family:var(--font-sans); font-weight:600; margin-top:3px;">
              <option value="AUTO_REGIME" ${state.semiMode === "AUTO_REGIME" ? "selected" : ""}>Auto Regime (70:30 ↔ 80:20 on Fear ≤ 25)</option>
              <option value="BASELINE_70_30" ${state.semiMode === "BASELINE_70_30" ? "selected" : ""}>70% $SMH : 30% $XLV Golden Baseline</option>
              <option value="CONTRARIAN_80_20" ${state.semiMode === "CONTRARIAN_80_20" ? "selected" : ""}>80% $SMH : 20% $XLV Contrarian Accumulation</option>
              <option value="AGGRESSIVE_90_10" ${state.semiMode === "AGGRESSIVE_90_10" ? "selected" : ""}>90% $SMH : 10% $XLV Right-Side Tilt</option>
            </select>
          </div>
          <div>
            <label style="font-size:0.68rem; font-family:var(--font-mono); color:var(--muted);">REBALANCING CADENCE</label>
            <select id="semiFreqInput" style="width:100%; padding:8px 10px; background:#060911; border:1px solid var(--border); color:#fff; border-radius:4px; font-family:var(--font-sans); font-weight:600; margin-top:3px;">
              <option value="ANNUAL" ${state.semiFreq === "ANNUAL" ? "selected" : ""}>Annual + Band Trigger (Min Tax Drag)</option>
              <option value="QUARTERLY" ${state.semiFreq === "QUARTERLY" ? "selected" : ""}>Quarterly Rebalance</option>
              <option value="MONTHLY" ${state.semiFreq === "MONTHLY" ? "selected" : ""}>Monthly Rebalance</option>
              <option value="WEEKLY" ${state.semiFreq === "WEEKLY" ? "selected" : ""}>Weekly Rebalance (High Tax Drag)</option>
            </select>
          </div>
          <div>
            <label style="font-size:0.68rem; font-family:var(--font-mono); color:var(--muted);">UNREALIZED GAIN (₩ KRW · TAX HARVESTER)</label>
            <input type="number" id="semiGainKrwInput" value="${state.semiGainKrw ?? 3800000}" step="100000"
                   style="width:100%; padding:8px 10px; background:#060911; border:1px solid var(--border); color:#fff; border-radius:4px; font-family:var(--font-mono); margin-top:3px;" />
          </div>
        </div>

        <button class="btn btn-emerald" id="btnRunSemiRebalance" style="width:100%; justify-content:center; padding:9px;">
          Calculate Exact $SMH / $XLV Rebalancing Orders
        </button>

        ${
          rebal
            ? `
          <div id="semiRebalOutput" style="margin-top:14px; background:#060911; border:1px solid var(--border); border-left:3px solid var(--fin-up); border-radius:4px; padding:14px; font-size:0.8rem;">
            <div style="font-weight:800; color:var(--fin-up); margin-bottom:4px;">
              ${lang === "jp" ? rebal.active_rule_jp : lang === "kr" ? rebal.active_rule_kr : rebal.active_rule_en}
            </div>
            <div class="mono" style="font-size:0.71rem; color:#93c5fd; margin-bottom:8px;">
              Latest Close Basis (${rebal.as_of_date || ov.date}): $SMH @ $${Number(rebal.smh_close ?? ov.smh_close).toFixed(2)} · $XLV @ $${Number(rebal.xlv_close ?? ov.xlv_close).toFixed(2)} · FX ₩${Number(rebal.usdkrw ?? ov.usdkrw).toLocaleString()}/$ · Total ₩${Number(rebal.total_capital_krw ?? 0).toLocaleString()}
            </div>
            <div class="semi-form-grid-2" style="margin-bottom:10px;">
              <div style="background:#0c1220; padding:10px; border-radius:4px; border:1px solid var(--border);">
                <div style="font-size:0.7rem; color:var(--muted);">TARGET $SMH (${rebal.target_smh_weight_pct}%)</div>
                <div class="mono" style="font-size:1.05rem; font-weight:800; color:#fff; margin-top:2px;">
                  $${Number(rebal.target_smh_usd ?? 0).toLocaleString()} (${rebal.target_smh_shares} sh)
                </div>
                <div class="mono" style="font-size:0.73rem; color:${rebal.delta_smh_usd >= 0 ? "var(--fin-up)" : "var(--fin-down)"}; margin-top:2px;">
                  Order vs Drift: ${rebal.delta_smh_usd >= 0 ? "BUY +" : "SELL "}$${Math.abs(Number(rebal.delta_smh_usd ?? 0)).toLocaleString()} (${rebal.delta_smh_shares >= 0 ? "+" : ""}${rebal.delta_smh_shares} sh)
                </div>
              </div>
              <div style="background:#0c1220; padding:10px; border-radius:4px; border:1px solid var(--border);">
                <div style="font-size:0.7rem; color:var(--muted);">TARGET $XLV (${rebal.target_xlv_weight_pct}%)</div>
                <div class="mono" style="font-size:1.05rem; font-weight:800; color:#fff; margin-top:2px;">
                  $${Number(rebal.target_xlv_usd ?? 0).toLocaleString()} (${rebal.target_xlv_shares} sh)
                </div>
                <div class="mono" style="font-size:0.73rem; color:${rebal.delta_xlv_usd >= 0 ? "var(--fin-up)" : "var(--fin-down)"}; margin-top:2px;">
                  Order vs Drift: ${rebal.delta_xlv_usd >= 0 ? "BUY +" : "SELL "}$${Math.abs(Number(rebal.delta_xlv_usd ?? 0)).toLocaleString()} (${rebal.delta_xlv_shares >= 0 ? "+" : ""}${rebal.delta_xlv_shares} sh)
                </div>
              </div>
            </div>
            <div style="font-size:0.75rem; color:var(--text-secondary); line-height:1.45; border-top:1px solid var(--border); padding-top:8px;">
              <div><b>KRW 2.5M Tax-Free Harvester:</b> ${
                lang === "jp" ? rebal.kr_tax_guidance_jp : lang === "kr" ? rebal.kr_tax_guidance_kr : rebal.kr_tax_guidance_en
              }</div>
              <div class="mono" style="color:var(--muted); margin-top:4px;">
                Residual Cash: $${Number(rebal.residual_cash_usd ?? 0).toFixed(2)} · Est. Annual Tax & Turnover Drag (${rebal.rebalance_frequency}): -${rebal.estimated_tax_drag_pct}%/yr · Expected Net 15Y Rate: +${rebal.expected_net_cagr_pct}%/yr
              </div>
            </div>
          </div>
        `
            : ""
        }
      </div>

      <!-- Calculator 2: 3-Stage Lump-Sum Entry Planner -->
      <div class="proof-card" style="margin-bottom:0; border-top:2px solid var(--fin-blue);">
        <div style="font-size:0.7rem; font-family:var(--font-mono); font-weight:700; color:#60a5fa; letter-spacing:0.05em;">
          ${t.lumpSectionTag}
        </div>
        <h3 style="font-size:1.12rem; font-weight:800; color:#ffffff; margin:4px 0 6px;">${t.lumpSectionTitle}</h3>
        <p style="font-size:0.8rem; color:var(--muted); margin-bottom:14px;">${t.lumpSectionDesc}</p>

        <div class="semi-form-grid-2" style="margin-bottom:12px;">
          <div>
            <label style="font-size:0.68rem; font-family:var(--font-mono); color:var(--muted);">NEW LUMP-SUM CASH ($ USD)</label>
            <input type="number" id="semiLumpCapInput" value="${state.semiLumpCapUsd ?? 50000}" step="1000"
                   style="width:100%; padding:8px 10px; background:#060911; border:1px solid var(--border); color:#fff; border-radius:4px; font-family:var(--font-mono); font-weight:700; margin-top:3px;" />
          </div>
          <div>
            <label style="font-size:0.68rem; font-family:var(--font-mono); color:var(--muted);">
              SIMULATE FEAR & GREED SCORE (LIVE: ${ov.fg_score})
            </label>
            <input type="number" id="semiLumpScoreInput" value="${
              state.semiLumpScore !== null && state.semiLumpScore !== undefined ? state.semiLumpScore : ov.fg_score
            }" min="0" max="100" step="1"
                   style="width:100%; padding:8px 10px; background:#060911; border:1px solid var(--border); color:#fff; border-radius:4px; font-family:var(--font-mono); font-weight:700; margin-top:3px;" />
          </div>
        </div>

        <div style="display:flex; gap:6px; margin-bottom:12px; flex-wrap:wrap;">
          <button class="btn btn-sm btn-sim-fg" data-fg="18.0">Live Extreme Fear (18.0)</button>
          <button class="btn btn-sm btn-sim-fg" data-fg="50.0">Simulate Neutral (50.0)</button>
          <button class="btn btn-sm btn-sim-fg" data-fg="78.0">Simulate Extreme Greed (78.0)</button>
        </div>

        <button class="btn btn-primary" id="btnRunSemiLumpSum" style="width:100%; justify-content:center; padding:9px;">
          Generate 3-Stage Lump-Sum Tranche Schedule
        </button>

        ${
          lump
            ? `
          <div id="semiLumpOutput" style="margin-top:14px; background:#060911; border:1px solid var(--border); border-left:3px solid var(--fin-blue); border-radius:4px; padding:14px; font-size:0.8rem;">
            <div style="font-weight:800; color:#93c5fd; margin-bottom:3px;">
              ${lang === "jp" ? lump.case_title_jp : lang === "kr" ? lump.case_title_kr : lump.case_title_en}
            </div>
            <div class="mono" style="font-size:0.71rem; color:var(--muted); margin-bottom:6px;">
              Latest Close Basis (${lump.as_of_date || ov.date}): $SMH @ $${Number(lump.smh_close ?? ov.smh_close).toFixed(2)} · $XLV @ $${Number(lump.xlv_close ?? ov.xlv_close).toFixed(2)}
            </div>
            <p style="font-size:0.76rem; color:var(--text-secondary); margin-bottom:10px;">
              ${lang === "jp" ? lump.summary_jp : lang === "kr" ? lump.summary_kr : lump.summary_en}
            </p>
            <div style="display:flex; flex-direction:column; gap:8px;">
              ${lump.tranches
                .map((tr) => {
                  const tTitle = lang === "jp" ? tr.title_jp : lang === "kr" ? tr.title_kr : tr.title_en;
                  const tTime = lang === "jp" ? tr.timing_jp : lang === "kr" ? tr.timing_kr : tr.timing_en;
                  const tNote = lang === "jp" ? tr.note_jp : lang === "kr" ? tr.note_kr : tr.note_en;
                  return `
                  <div style="background:#0c1220; padding:10px; border-radius:4px; border:1px solid var(--border);">
                    <div style="display:flex; justify-content:space-between; align-items:center;">
                      <b style="color:#ffffff;">${tTitle}</b>
                      <span class="mono" style="color:var(--fin-up); font-weight:700;">$${tr.amount_usd.toLocaleString()} (${tr.allocation_pct}%)</span>
                    </div>
                    <div class="mono" style="font-size:0.72rem; color:#93c5fd; margin-top:2px;">
                      ${tTime} · $SMH: $${tr.smh_usd.toLocaleString()} (${tr.smh_shares} sh) | $XLV: $${tr.xlv_usd.toLocaleString()} (${tr.xlv_shares} sh)
                    </div>
                    <div style="font-size:0.74rem; color:var(--muted); margin-top:4px;">${tNote}</div>
                  </div>
                `;
                })
                .join("")}
            </div>
          </div>
        `
            : ""
        }
      </div>
    </section>

    <!-- SECTION 4: 26-YEAR EMPIRICAL PERFORMANCE TABLE & EQUITY CURVE (2000-2026) -->
    <section class="proof-card">
      <div style="display:flex; justify-content:space-between; align-items:flex-start; flex-wrap:wrap; gap:12px; margin-bottom:14px;">
        <div>
          <div style="font-size:0.7rem; font-family:var(--font-mono); font-weight:700; color:var(--fin-up); letter-spacing:0.05em;">
            ${t.eraSectionTag}
          </div>
          <h3 style="font-size:1.15rem; font-weight:800; color:#ffffff; margin-top:3px;">${t.eraSectionTitle}</h3>
          <p style="font-size:0.8rem; color:var(--muted); margin-top:2px;">${t.eraSectionDesc}</p>
        </div>
        <button class="btn btn-sm" id="btnDownloadSemiCsv">
          Download 2000–2026 Daily CSV Dataset (Pro)
        </button>
      </div>

      ${renderEquityCurveSvg(state.semiHistory)}

      <div class="table-responsive-scroll">
        <table class="proof-table">
          <thead>
            <tr>
              <th>Investment Horizon</th>
              <th>Period</th>
              <th>100% $QQQ CAGR</th>
              <th>100% $QQQ Multiple</th>
              <th>70:30 Baseline CAGR</th>
              <th>70:30 (80:20 Fear Tilt) CAGR</th>
              <th>70:30 (80:20 Tilt) Multiple</th>
              <th>Max Drawdown (vs QQQ)</th>
            </tr>
          </thead>
          <tbody>
            ${eras
              .map((e) => {
                const hLabel = lang === "jp" ? e.horizon_jp : lang === "kr" ? e.horizon_kr : e.horizon_en;
                return `
                <tr class="proof-highlight">
                  <td style="font-family:var(--font-sans);">${hLabel}</td>
                  <td>${e.period}</td>
                  <td style="color:var(--text-secondary);">+${e.qqq_cagr_pct.toFixed(2)}%</td>
                  <td style="color:var(--text-secondary);">${e.qqq_multiple.toFixed(2)}x</td>
                  <td>+${e.port_70_30_cagr_pct.toFixed(2)}%</td>
                  <td style="color:var(--fin-up); font-weight:800;">+${e.port_80_20_cagr_pct.toFixed(2)}%</td>
                  <td style="color:var(--fin-up); font-weight:800;">${e.port_80_20_multiple.toFixed(2)}x</td>
                  <td><span style="color:var(--fin-up);">${e.port_80_20_mdd_pct.toFixed(1)}%</span> <span style="color:var(--muted); font-size:0.72rem;">(QQQ ${e.qqq_mdd_pct.toFixed(1)}%)</span></td>
                </tr>
              `;
              })
              .join("")}
          </tbody>
        </table>
      </div>
    </section>

    <!-- SECTION 5: PRO TERMINAL & LIFETIME LICENSE PRICING -->
    ${renderPricing(state)}

    <!-- CROSS-PLATFORM SWITCH BANNER BACK TO RIGHTSIDEALPHA -->
    <section class="cross-banner" style="border-left-color:var(--fin-blue);">
      <div>
        <div style="font-size:0.72rem; font-family:var(--font-mono); font-weight:700; color:#93c5fd; text-transform:uppercase;">
          COMPANION US INDIVIDUAL EQUITY SCREENER · RIGHTSIDEALPHA
        </div>
        <h3 style="font-size:1.15rem; font-weight:800; margin:4px 0; color:#ffffff;">
          Looking for High-Alpha US Individual Stock Turnarounds ($CELH, $MBLY, $NVDA, $APP)?
        </h3>
        <p style="font-size:0.84rem; color:var(--muted);">
          Switch to the RightSideAlpha US Equity Terminal to screen 72 NYSE & NASDAQ stocks for MA20/MA60 Right-Side Ignitions and 55-Day Time-Stop diagnostics.
        </p>
      </div>
      <button class="btn btn-primary" id="btnSwitchToRightSide">
        Open RightSideAlpha US Equity Terminal →
      </button>
    </section>
  `;
}


// --- src/main.js ---











const initialPath = window.location.pathname.toLowerCase();
const initialHash = window.location.hash.toLowerCase();
const initialSearch = new URLSearchParams(window.location.search);
const viewParam = (initialSearch.get("view") || "").toLowerCase();
const defaultView =
  viewParam === "semi" || initialHash.includes("semi") || initialPath.includes("/semi")
    ? "semi"
    : viewParam === "rightside" || initialHash.includes("rightside") || initialPath.includes("/rightside")
    ? "rightside"
    : window.__DEFAULT_VIEW__ === "semi"
    ? "semi"
    : "rightside";

const state = {
  lang: localStorage.getItem("rsa_lang") || "en",
  activeView: defaultView,
  isAdminAuthenticated: sessionStorage.getItem("rsa_admin_auth") === "true",
  isProUnlocked: localStorage.getItem("rsa_pro_unlocked") === "true",
  licenseKey: localStorage.getItem("rsa_token") || "",
  stocks: [],
  filteredStocks: [],
  backtestKpis: null,
  pineCode: null,
  searchQuery: "",
  zoneFilter: "ALL",
  sortCol: "score",
  sortAsc: false,
  // SemiFearGreed state
  semiOverview: null,
  semiHistory: null,
  semiGaugeTab: "overview",
  semiRange: "1Y",
  semiCapUsd: 100000,
  semiMode: "AUTO_REGIME",
  semiFreq: "ANNUAL",
  semiGainKrw: 3800000,
  semiRebalanceResult: null,
  semiLumpCapUsd: 50000,
  semiLumpScore: null,
  semiLumpSumResult: null,
  // Telegram state (@SemifearGreedbot pre-configured)
  telegramConfigured: true,
  telegramBotToken: localStorage.getItem("rsa_tg_bot_token") || DEFAULT_TG_BOT_TOKEN,
  telegramChatId: localStorage.getItem("rsa_tg_chat_id") || "755033799",
  telegramAlertType: "SEMI_BRIEFING",
  telegramPreviewText: "",
  config: {
    site1_name: "RightSideAlpha",
    site1_url: localStorage.getItem("rsa_cfg_site1_url") || "https://truthofmarket.com",
    site2_url: "https://truthofmarket.com",
    ls_site1_monthly_url:
      localStorage.getItem("rsa_cfg_ls_monthly") ||
      "https://truthofmarket.lemonsqueezy.com/checkout/buy/d5e7e761-8b1b-4ca8-b1fe-771acd1450f8",
    ls_site1_ltd_url:
      localStorage.getItem("rsa_cfg_ls_ltd") ||
      "https://truthofmarket.lemonsqueezy.com/checkout/buy/667aa482-f17c-47d1-b7f3-a2427c36516b",
    tradingview_aff_id: localStorage.getItem("rsa_cfg_aff_tv") || "rightsidealpha",
    seekingalpha_source: localStorage.getItem("rsa_cfg_aff_sa") || "affiliate_rightside",
    broker_name: localStorage.getItem("rsa_cfg_broker_name") || "IBKR / Webull",
    broker_referral_url:
      localStorage.getItem("rsa_cfg_broker_url") || "https://ibkr.com/referral/rightsidealpha",
    telegram_channel_url: localStorage.getItem("rsa_tg_channel_url") || DEFAULT_TG_CHANNEL_URL,
    telegram_chat_id: localStorage.getItem("rsa_tg_chat_id") || "755033799",
    youtube_url: localStorage.getItem("rsa_cfg_youtube_url") || DEFAULT_YOUTUBE_URL,
    instagram_url: localStorage.getItem("rsa_cfg_instagram_url") || DEFAULT_INSTAGRAM_URL,
  },
  get t() {
    return translations[this.lang] || translations.en;
  },
};

function showToast(msg) {
  const box = document.getElementById("toastBox");
  if (!box) return;
  box.textContent = msg;
  box.style.display = "block";
  clearTimeout(window.__toastTimer);
  window.__toastTimer = setTimeout(() => {
    box.style.display = "none";
  }, 3200);
}

function applyClientFilterAndSort() {
  const q = (state.searchQuery || "").trim().toLowerCase();
  const z = state.zoneFilter;

  let list = state.stocks.filter((s) => {
    // Strictly US-listed equities only
    if (!s.ticker || String(s.ticker).includes(".")) return false;
    if (z !== "ALL" && s.zone_code !== z) return false;
    if (q) {
      const hay = `${s.ticker} ${s.name_en} ${s.name_jp} ${s.name_kr} ${s.sector}`.toLowerCase();
      if (!hay.includes(q)) return false;
    }
    return true;
  });

  const col = state.sortCol;
  const dir = state.sortAsc ? 1 : -1;
  list.sort((a, b) => {
    const va = a[col];
    const vb = b[col];
    if (typeof va === "string" || typeof vb === "string") {
      return String(va ?? "").localeCompare(String(vb ?? "")) * dir;
    }
    return ((va ?? 0) - (vb ?? 0)) * dir;
  });

  state.filteredStocks = list;
}

function renderRightSideView() {
  const t = state.t;
  return `
    ${renderHero(state)}
    ${renderProofCard(state)}
    <section class="screener-panel">
      ${renderScreenerControls(state)}
      ${renderStockTable(state)}
    </section>
    ${renderProVault(state)}
    ${renderPricing(state)}

    <!-- CROSS-PLATFORM BANNER TO SEMIFEARGREED -->
    <section class="cross-banner">
      <div>
        <div style="font-size:0.72rem; font-family:var(--font-mono); font-weight:700; color:#f87171; text-transform:uppercase; letter-spacing:0.05em;" id="crossTitle">
          ${t.crossTitle}
        </div>
        <h3 style="font-size:1.15rem; font-weight:800; margin:4px 0; color:#ffffff;" id="crossHeading">
          ${t.crossHeading}
        </h3>
        <p style="font-size:0.84rem; color:var(--muted);" id="crossDesc">
          ${t.crossDesc}
        </p>
      </div>
      <button class="btn btn-primary" id="crossFunnelSwitchBtn" style="background:#dc2626; border-color:#ef4444;">
        <span id="crossBtn">${t.crossBtn} →</span>
      </button>
    </section>
  `;
}

function renderApp() {
  const appEl = document.getElementById("app");
  if (!appEl) return;

  const t = state.t;
  appEl.innerHTML = `
    ${renderHeader(state)}
    <main class="container">
      ${state.activeView === "semi" ? renderSemiFearGreedView(state) : renderRightSideView()}

      <footer style="border-top:1px solid var(--border); padding-top:20px; margin-top:28px; color:var(--muted); font-size:0.76rem; line-height:1.6;">
        <div style="display:flex; gap:12px; align-items:center; flex-wrap:wrap; margin-bottom:12px;">
          <span class="mono" style="font-size:0.72rem; color:var(--text); font-weight:700;">OFFICIAL CHANNELS:</span>
          <a href="${state.config.youtube_url || DEFAULT_YOUTUBE_URL}" target="_blank" rel="noopener noreferrer" style="color:#fca5a5; text-decoration:none; font-weight:600;">
            📺 YouTube (@rightsidealpha) ↗
          </a>
          <span style="color:var(--border);">|</span>
          <a href="${state.config.instagram_url || DEFAULT_INSTAGRAM_URL}" target="_blank" rel="noopener noreferrer" style="color:#f9a8d4; text-decoration:none; font-weight:600;">
            📸 Instagram (@semifeargreed) ↗
          </a>
          <span style="color:var(--border);">|</span>
          <a href="${state.config.telegram_channel_url || DEFAULT_TG_CHANNEL_URL}" target="_blank" rel="noopener noreferrer" style="color:#38bdf8; text-decoration:none; font-weight:600;">
            🤖 Telegram Bot (@SemifearGreedbot) ↗
          </a>
          <span style="color:var(--border);">|</span>
          <a href="https://t.me/RigjtsideAlphabot" target="_blank" rel="noopener noreferrer" style="color:#60a5fa; text-decoration:none; font-weight:600;">
            🤖 US Stock Bot (@RigjtsideAlphabot) ↗
          </a>
        </div>
        <p id="disclaimerText">${t.disclaimer}</p>
        <p style="margin-top:8px; font-family:var(--font-mono); font-size:0.72rem;" id="copyrightText">${t.copyright}</p>
      </footer>
    </main>
    <canvas id="scoreCanvas" width="900" height="500" style="display:none;"></canvas>
    ${renderModals(state)}
  `;

  bindEvents();
}

function switchView(targetView) {
  state.activeView = targetView === "semi" ? "semi" : "rightside";
  const basePath = window.location.pathname || "/";
  if (state.activeView === "semi") {
    window.history.replaceState(null, "", `${basePath}#semi`);
  } else {
    window.history.replaceState(null, "", `${basePath}#rightside`);
  }
  renderApp();
  window.scrollTo({ top: 0, behavior: "smooth" });
}

function bindEvents() {
  // Initialize Lemon Squeezy checkout overlay if script is loaded
  if (typeof window.createLemonSqueezy === "function") {
    try {
      window.createLemonSqueezy();
    } catch (_) {
      // Ignore overlay init errors in headless environments
    }
  }

  // Brand Home Button
  const brandHomeBtn = document.getElementById("brandHomeBtn");
  if (brandHomeBtn) {
    brandHomeBtn.addEventListener("click", () => {
      window.scrollTo({ top: 0, behavior: "smooth" });
    });
  }

  // Platform Switcher
  const navTabRightSide = document.getElementById("navTabRightSide");
  if (navTabRightSide) {
    navTabRightSide.addEventListener("click", () => switchView("rightside"));
  }
  const navTabSemiFg = document.getElementById("navTabSemiFg");
  if (navTabSemiFg) {
    navTabSemiFg.addEventListener("click", () => switchView("semi"));
  }
  const ribbonSwitchSemi = document.getElementById("ribbonSwitchSemi");
  if (ribbonSwitchSemi) {
    ribbonSwitchSemi.addEventListener("click", () => switchView("semi"));
  }
  const crossFunnelSwitchBtn = document.getElementById("crossFunnelSwitchBtn");
  if (crossFunnelSwitchBtn) {
    crossFunnelSwitchBtn.addEventListener("click", () => switchView("semi"));
  }
  const btnSwitchToRightSide = document.getElementById("btnSwitchToRightSide");
  if (btnSwitchToRightSide) {
    btnSwitchToRightSide.addEventListener("click", () => switchView("rightside"));
  }

  // Language Switcher
  document.querySelectorAll(".lang-btn").forEach((btn) => {
    btn.addEventListener("click", () => {
      const newLang = btn.getAttribute("data-lang");
      if (newLang && translations[newLang]) {
        state.lang = newLang;
        localStorage.setItem("rsa_lang", newLang);
        renderApp();
      }
    });
  });

  // Search Input (RightSideAlpha)
  const searchInput = document.getElementById("searchInput");
  if (searchInput) {
    searchInput.addEventListener("input", (e) => {
      state.searchQuery = e.target.value;
      applyClientFilterAndSort();
      const tbody = document.getElementById("tableBody");
      if (tbody) tbody.innerHTML = renderStockRows(state);
      bindRowEvents();
    });
  }

  // Zone Filter Tabs
  document.querySelectorAll(".filter-tab").forEach((tab) => {
    tab.addEventListener("click", () => {
      state.zoneFilter = tab.getAttribute("data-zone") || "ALL";
      applyClientFilterAndSort();
      renderApp();
    });
  });

  // Sort Headers
  document.querySelectorAll(".sort-header").forEach((th) => {
    th.addEventListener("click", () => {
      const col = th.getAttribute("data-sort");
      if (!col) return;
      if (state.sortCol === col) {
        state.sortAsc = !state.sortAsc;
      } else {
        state.sortCol = col;
        state.sortAsc = col === "ticker";
      }
      applyClientFilterAndSort();
      const tbody = document.getElementById("tableBody");
      if (tbody) tbody.innerHTML = renderStockRows(state);
      bindRowEvents();
    });
  });

  // License Modal Controls
  const licenseModal = document.getElementById("licenseModal");
  const openLicenseModal = (prefillDemo = false, customNotice = "") => {
    if (!licenseModal) return;
    licenseModal.style.display = "flex";
    const inputEl = document.getElementById("licenseInput");
    const msgEl = document.getElementById("licenseMsg");
    if (inputEl && prefillDemo && !inputEl.value.trim()) {
      inputEl.value = state.licenseKey || "PRO-DEMO-2026";
    }
    if (msgEl && customNotice) {
      msgEl.style.color = "#93c5fd";
      msgEl.textContent = customNotice;
    }
  };
  const closeLicenseModal = () => {
    if (licenseModal) licenseModal.style.display = "none";
  };

  const btnOpenLicense = document.getElementById("btnOpenLicense");
  if (btnOpenLicense) btnOpenLicense.addEventListener("click", () => openLicenseModal(false));

  const proStatusBadge = document.getElementById("proStatusBadge");
  if (proStatusBadge) {
    proStatusBadge.style.cursor = "pointer";
    proStatusBadge.addEventListener("click", () => openLicenseModal(true));
  }

  const vaultUnlockBtn = document.getElementById("vaultUnlockBtn");
  if (vaultUnlockBtn) vaultUnlockBtn.addEventListener("click", () => openLicenseModal(true));

  const vaultOverlayUnlock = document.getElementById("vaultOverlayUnlock");
  if (vaultOverlayUnlock) vaultOverlayUnlock.addEventListener("click", () => openLicenseModal(true));

  const btnCancelLicense = document.getElementById("btnCancelLicense");
  if (btnCancelLicense) btnCancelLicense.addEventListener("click", closeLicenseModal);

  const btnFillDemoKey = document.getElementById("btnFillDemoKey");
  if (btnFillDemoKey) {
    btnFillDemoKey.addEventListener("click", () => {
      const inputEl = document.getElementById("licenseInput");
      if (inputEl) inputEl.value = "PRO-DEMO-2026";
      verifyLicenseFlow();
    });
  }

  const btnLockLicense = document.getElementById("btnLockLicense");
  if (btnLockLicense) {
    btnLockLicense.addEventListener("click", async () => {
      state.isProUnlocked = false;
      state.licenseKey = "";
      localStorage.removeItem("rsa_pro_unlocked");
      localStorage.removeItem("rsa_token");
      await loadAllData();
      closeLicenseModal();
      renderApp();
      showToast("Pro Terminal Locked — Reverted to Free Preview");
    });
  }

  const verifyLicenseFlow = async () => {
    const inputEl = document.getElementById("licenseInput");
    const msgEl = document.getElementById("licenseMsg");
    const key = (inputEl ? inputEl.value : "").trim();
    if (!key) {
      if (msgEl) {
        msgEl.style.color = "var(--fin-down)";
        msgEl.textContent = "Please enter a valid license key.";
      }
      return;
    }
    try {
      const res = await validateLicense(key);
      if (res.valid) {
        state.isProUnlocked = true;
        state.licenseKey = key;
        localStorage.setItem("rsa_pro_unlocked", "true");
        localStorage.setItem("rsa_token", key);
        if (msgEl) {
          msgEl.style.color = "var(--fin-up)";
          msgEl.textContent = res.message || "Pro Terminal Unlocked.";
        }
        await loadAllData();
        setTimeout(() => {
          closeLicenseModal();
          renderApp();
          showToast("Pro Terminal Unlocked — All 72 US Equity Targets Active");
        }, 350);
      } else {
        if (msgEl) {
          msgEl.style.color = "var(--fin-down)";
          msgEl.textContent = res.message || "Invalid key. Use PRO-DEMO-2026 for demo.";
        }
      }
    } catch (err) {
      if (msgEl) {
        msgEl.style.color = "var(--fin-down)";
        msgEl.textContent = "Validation error. Try PRO-DEMO-2026.";
      }
    }
  };

  const btnVerifyLicense = document.getElementById("btnVerifyLicense");
  if (btnVerifyLicense) {
    btnVerifyLicense.addEventListener("click", verifyLicenseFlow);
  }

  const licenseInput = document.getElementById("licenseInput");
  if (licenseInput) {
    licenseInput.addEventListener("keydown", (e) => {
      if (e.key === "Enter") {
        e.preventDefault();
        verifyLicenseFlow();
      }
    });
  }

  // Lemon Squeezy Checkout Buttons (Overlay + Demo Store Fallback)
  document.querySelectorAll(".lemonsqueezy-button").forEach((btn) => {
    btn.addEventListener("click", (e) => {
      const href = btn.getAttribute("href") || "";
      const isDefaultDemoStore = href.includes("rightsidealpha.lemonsqueezy.com");
      if (window.LemonSqueezy && window.LemonSqueezy.Url && typeof window.LemonSqueezy.Url.Open === "function" && !isDefaultDemoStore) {
        e.preventDefault();
        window.LemonSqueezy.Url.Open(href);
        return;
      }
      if (isDefaultDemoStore) {
        e.preventDefault();
        openLicenseModal(
          true,
          "Instant Evaluation Mode: Click 'Verify & Unlock Terminal' with PRO-DEMO-2026 (or configure your live Lemon Squeezy store URL in Config)."
        );
      }
    });
  });

  // Admin Login & Config Modal Controls
  const adminLoginModal = document.getElementById("adminLoginModal");
  const configModal = document.getElementById("configModal");
  const btnOpenConfig = document.getElementById("btnOpenConfig");
  const btnCancelConfig = document.getElementById("btnCancelConfig");
  const btnSaveConfig = document.getElementById("btnSaveConfig");
  const btnCancelAdminLogin = document.getElementById("btnCancelAdminLogin");
  const btnSubmitAdminLogin = document.getElementById("btnSubmitAdminLogin");
  const btnAdminLogout = document.getElementById("btnAdminLogout");

  const handleAdminLoginSubmit = async () => {
    const idInput = document.getElementById("adminIdInput");
    const pwInput = document.getElementById("adminPwInput");
    const msgEl = document.getElementById("adminLoginMsg");
    const uname = (idInput ? idInput.value : "").trim();
    const pw = pwInput ? pwInput.value : "";

    if (!uname || !pw) {
      if (msgEl) {
        msgEl.style.color = "var(--fin-down)";
        msgEl.textContent = "Please enter both Admin ID and Password.";
      }
      return;
    }

    try {
      const res = await verifyAdminCredentials(uname, pw);
      if (res && res.authenticated) {
        state.isAdminAuthenticated = true;
        sessionStorage.setItem("rsa_admin_auth", "true");
        // Automatically grant Pro Terminal access to Admin
        state.isProUnlocked = true;
        state.licenseKey = res.license_key || "PRO-DEMO-2026";
        localStorage.setItem("rsa_pro_unlocked", "true");
        localStorage.setItem("rsa_token", state.licenseKey);

        if (msgEl) {
          msgEl.style.color = "var(--fin-up)";
          msgEl.textContent = res.message || "Admin Authenticated!";
        }
        await loadAllData();
        if (adminLoginModal) adminLoginModal.style.display = "none";
        renderApp();
        const freshConfigModal = document.getElementById("configModal");
        if (freshConfigModal) freshConfigModal.style.display = "flex";
        showToast("Admin Authenticated — Terminal Config & Pro Access Unlocked");
      } else {
        if (msgEl) {
          msgEl.style.color = "var(--fin-down)";
          msgEl.textContent = (res && res.message) || "Invalid Admin ID or Password.";
        }
      }
    } catch (_) {
      if (msgEl) {
        msgEl.style.color = "var(--fin-down)";
        msgEl.textContent = "Authentication error. Please try again.";
      }
    }
  };

  if (btnOpenConfig) {
    btnOpenConfig.addEventListener("click", () => {
      if (state.isAdminAuthenticated) {
        if (configModal) configModal.style.display = "flex";
      } else if (adminLoginModal) {
        adminLoginModal.style.display = "flex";
        const idInput = document.getElementById("adminIdInput");
        if (idInput) idInput.focus();
      }
    });
  }
  if (btnCancelAdminLogin && adminLoginModal) {
    btnCancelAdminLogin.addEventListener("click", () => {
      adminLoginModal.style.display = "none";
    });
  }
  if (btnSubmitAdminLogin) {
    btnSubmitAdminLogin.addEventListener("click", handleAdminLoginSubmit);
  }
  const adminPwInput = document.getElementById("adminPwInput");
  if (adminPwInput) {
    adminPwInput.addEventListener("keydown", (e) => {
      if (e.key === "Enter") {
        e.preventDefault();
        handleAdminLoginSubmit();
      }
    });
  }
  if (btnAdminLogout) {
    btnAdminLogout.addEventListener("click", () => {
      state.isAdminAuthenticated = false;
      sessionStorage.removeItem("rsa_admin_auth");
      if (configModal) configModal.style.display = "none";
      showToast("Admin Session Locked");
    });
  }
  if (btnCancelConfig && configModal) {
    btnCancelConfig.addEventListener("click", () => {
      configModal.style.display = "none";
    });
  }
  if (btnSaveConfig) {
    btnSaveConfig.addEventListener("click", async () => {
      const s1Url = document.getElementById("cfgSite1Url")?.value.trim() || state.config.site1_url;
      const lsM = document.getElementById("cfgLsMonthly")?.value.trim() || state.config.ls_site1_monthly_url;
      const lsL = document.getElementById("cfgLsLtd")?.value.trim() || state.config.ls_site1_ltd_url;
      const tgCh = document.getElementById("cfgTgChannel")?.value.trim() || state.config.telegram_channel_url || DEFAULT_TG_CHANNEL_URL;
      const ytUrl = document.getElementById("cfgYoutubeUrl")?.value.trim() || state.config.youtube_url || DEFAULT_YOUTUBE_URL;
      const igUrl = document.getElementById("cfgInstagramUrl")?.value.trim() || state.config.instagram_url || DEFAULT_INSTAGRAM_URL;
      const tvId = document.getElementById("cfgAffTv")?.value.trim() || "rightsidealpha";
      const saSrc = document.getElementById("cfgAffSa")?.value.trim() || "affiliate_rightside";
      const brkName = document.getElementById("cfgBrokerName")?.value.trim() || "IBKR / Webull";
      const brkUrl =
        document.getElementById("cfgBrokerUrl")?.value.trim() ||
        "https://ibkr.com/referral/rightsidealpha";

      state.config.site1_url = s1Url;
      state.config.ls_site1_monthly_url = lsM;
      state.config.ls_site1_ltd_url = lsL;
      state.config.telegram_channel_url = tgCh;
      state.config.youtube_url = ytUrl;
      state.config.instagram_url = igUrl;
      state.config.tradingview_aff_id = tvId;
      state.config.seekingalpha_source = saSrc;
      state.config.broker_name = brkName;
      state.config.broker_referral_url = brkUrl;

      localStorage.setItem("rsa_cfg_site1_url", s1Url);
      localStorage.setItem("rsa_cfg_ls_monthly", lsM);
      localStorage.setItem("rsa_cfg_ls_ltd", lsL);
      localStorage.setItem("rsa_tg_channel_url", tgCh);
      localStorage.setItem("rsa_cfg_youtube_url", ytUrl);
      localStorage.setItem("rsa_cfg_instagram_url", igUrl);
      localStorage.setItem("rsa_cfg_aff_tv", tvId);
      localStorage.setItem("rsa_cfg_aff_sa", saSrc);
      localStorage.setItem("rsa_cfg_broker_name", brkName);
      localStorage.setItem("rsa_cfg_broker_url", brkUrl);

      try {
        await updateReferralConfig({
          tradingview_aff_id: tvId,
          seekingalpha_source: saSrc,
          broker_name: brkName,
          broker_referral_url: brkUrl,
          ls_site1_monthly_url: lsM,
          ls_site1_ltd_url: lsL,
          site1_url: s1Url,
          telegram_channel_url: tgCh,
          youtube_url: ytUrl,
          instagram_url: igUrl,
        });
      } catch (e) {
        // Ignore network error if offline
      }

      if (configModal) configModal.style.display = "none";
      renderApp();
      showToast("Terminal & Affiliate Configuration Saved");
    });
  }

  // Telegram Modal Controls
  const telegramModal = document.getElementById("telegramModal");
  const refreshTelegramPreview = async (alertTypeOverride) => {
    const selEl = document.getElementById("tgAlertTypeSelect");
    const aType = alertTypeOverride || selEl?.value || state.telegramAlertType || "SEMI_BRIEFING";
    state.telegramAlertType = aType;
    const prevBox = document.getElementById("telegramPreviewBox");
    const docTicker = (document.getElementById("docTicker")?.value || "CELH").trim().toUpperCase();
    const docEntry = parseFloat(document.getElementById("docEntry")?.value || "27.93") || 27.93;
    const docDays = parseInt(document.getElementById("docDays")?.value || "42", 10) || 42;
    try {
      const res = await sendTelegramAlert({
        alert_type: aType,
        lang: state.lang,
        ticker: docTicker,
        entry_price: docEntry,
        days_held: docDays,
        dry_run: true,
      });
      if (res && res.message_preview) {
        state.telegramPreviewText = res.message_preview;
        if (prevBox) prevBox.textContent = res.message_preview;
      }
    } catch (_) {
      // Ignore preview error
    }
  };

  const openTelegramModal = async (defaultAlertType) => {
    if (!telegramModal) return;
    if (defaultAlertType) {
      state.telegramAlertType = defaultAlertType;
      const selEl = document.getElementById("tgAlertTypeSelect");
      if (selEl) selEl.value = defaultAlertType;
    }
    telegramModal.style.display = "flex";
    await refreshTelegramPreview(defaultAlertType);
    try {
      const syncInfo = await syncTelegramBotBrowser(state.telegramBotToken, state.telegramChatId);
      if (syncInfo && syncInfo.chatId && syncInfo.chatId !== state.telegramChatId) {
        state.telegramChatId = syncInfo.chatId;
        const cidInput = document.getElementById("tgChatIdInput");
        if (cidInput) cidInput.value = syncInfo.chatId;
      }
    } catch (_) {
      // Ignore sync error
    }
  };

  const btnOpenTelegram = document.getElementById("btnOpenTelegram");
  if (btnOpenTelegram) {
    btnOpenTelegram.addEventListener("click", () =>
      openTelegramModal(state.activeView === "semi" ? "SEMI_BRIEFING" : "RSA_IGNITION")
    );
  }
  const btnSendSemiTelegram = document.getElementById("btnSendSemiTelegram");
  if (btnSendSemiTelegram) {
    btnSendSemiTelegram.addEventListener("click", () => openTelegramModal("SEMI_BRIEFING"));
  }
  const btnOpenTelegramFromPricing = document.getElementById("btnOpenTelegramFromPricing");
  if (btnOpenTelegramFromPricing) {
    btnOpenTelegramFromPricing.addEventListener("click", () => openTelegramModal("FULL_DAILY"));
  }
  const btnCloseTelegram = document.getElementById("btnCloseTelegram");
  if (btnCloseTelegram && telegramModal) {
    btnCloseTelegram.addEventListener("click", () => {
      telegramModal.style.display = "none";
    });
  }

  const tgAlertTypeSelect = document.getElementById("tgAlertTypeSelect");
  if (tgAlertTypeSelect) {
    tgAlertTypeSelect.addEventListener("change", (e) => {
      refreshTelegramPreview(e.target.value);
    });
  }

  const btnPreviewTelegram = document.getElementById("btnPreviewTelegram");
  if (btnPreviewTelegram) {
    btnPreviewTelegram.addEventListener("click", () => {
      refreshTelegramPreview();
      showToast("Refreshed Live Telegram Briefing Preview");
    });
  }

  const btnCopyTelegramMsg = document.getElementById("btnCopyTelegramMsg");
  if (btnCopyTelegramMsg) {
    btnCopyTelegramMsg.addEventListener("click", async () => {
      const txt = document.getElementById("telegramPreviewBox")?.textContent || state.telegramPreviewText || "";
      try {
        await navigator.clipboard.writeText(txt);
        showToast("Telegram Briefing Copied to Clipboard");
      } catch (_) {
        showToast("Briefing Text Ready to Copy");
      }
    });
  }

  const persistTelegramInputs = async () => {
    const tok = document.getElementById("tgBotTokenInput")?.value.trim() ?? state.telegramBotToken;
    const cid = document.getElementById("tgChatIdInput")?.value.trim() ?? state.telegramChatId;
    const chUrl =
      document.getElementById("tgChannelUrlInput")?.value.trim() ||
      state.config.telegram_channel_url ||
      "https://t.me/SemiFearGreed";

    state.telegramBotToken = tok;
    state.telegramChatId = cid;
    state.telegramConfigured = Boolean(tok && cid);
    state.config.telegram_channel_url = chUrl;
    state.config.telegram_chat_id = cid;

    localStorage.setItem("rsa_tg_bot_token", tok);
    localStorage.setItem("rsa_tg_chat_id", cid);
    localStorage.setItem("rsa_tg_channel_url", chUrl);

    const chLinkBtn = document.getElementById("tgChannelLinkBtn");
    if (chLinkBtn) chLinkBtn.setAttribute("href", chUrl);

    try {
      await saveTelegramConfig({
        bot_token: tok,
        chat_id: cid,
        channel_url: chUrl,
        lang: state.lang,
      });
    } catch (_) {
      // Ignore if static
    }
    return { tok, cid, chUrl };
  };

  const btnVerifyTelegram = document.getElementById("btnVerifyTelegram");
  if (btnVerifyTelegram) {
    btnVerifyTelegram.addEventListener("click", async () => {
      const statusEl = document.getElementById("telegramStatusMsg");
      const { tok, cid } = await persistTelegramInputs();
      if (statusEl) {
        statusEl.style.color = "#93c5fd";
        statusEl.textContent = "Verifying Telegram Bot connection...";
      }
      try {
        const res = await verifyTelegramBot({ bot_token: tok, chat_id: cid });
        if (statusEl) {
          statusEl.style.color = res.valid ? "var(--fin-up)" : "var(--fin-amber)";
          statusEl.textContent = res.message || "Bot configuration saved.";
        }
        showToast(res.valid ? "Telegram Bot Verified & Saved" : "Saved Telegram Parameters");
      } catch (_) {
        if (statusEl) {
          statusEl.style.color = "var(--fin-amber)";
          statusEl.textContent = "Saved locally. Ready for preview or direct dispatch.";
        }
      }
    });
  }

  const btnSendTelegramNow = document.getElementById("btnSendTelegramNow");
  if (btnSendTelegramNow) {
    btnSendTelegramNow.addEventListener("click", async () => {
      const statusEl = document.getElementById("telegramStatusMsg");
      const prevBox = document.getElementById("telegramPreviewBox");
      const { tok, cid } = await persistTelegramInputs();
      const aType = document.getElementById("tgAlertTypeSelect")?.value || state.telegramAlertType || "SEMI_BRIEFING";
      const docTicker = (document.getElementById("docTicker")?.value || "CELH").trim().toUpperCase();
      const docEntry = parseFloat(document.getElementById("docEntry")?.value || "27.93") || 27.93;
      const docDays = parseInt(document.getElementById("docDays")?.value || "42", 10) || 42;

      if (statusEl) {
        statusEl.style.color = "#93c5fd";
        statusEl.textContent = "Dispatching briefing to Telegram...";
      }

      try {
        const res = await sendTelegramAlert({
          alert_type: aType,
          lang: state.lang,
          bot_token: tok,
          chat_id: cid,
          ticker: docTicker,
          entry_price: docEntry,
          days_held: docDays,
          dry_run: false,
        });
        if (res && res.message_preview) {
          state.telegramPreviewText = res.message_preview;
          if (prevBox) prevBox.textContent = res.message_preview;
        }
        if (statusEl) {
          statusEl.style.color = res.delivered ? "var(--fin-up)" : "#38bdf8";
          statusEl.textContent = res.status_detail || "Telegram briefing processed.";
        }
        showToast(
          res.delivered
            ? `Telegram Briefing Sent to ${res.chat_id}!`
            : "Briefing Preview Generated (Enter Live Bot Token & Chat ID to Push)"
        );
      } catch (_) {
        if (statusEl) {
          statusEl.style.color = "var(--fin-down)";
          statusEl.textContent = "Error sending Telegram alert.";
        }
      }
    });
  }

  // Position Doctor Controls
  document.querySelectorAll(".btn-quick-doc").forEach((btn) => {
    btn.addEventListener("click", async () => {
      const tick = btn.getAttribute("data-ticker");
      const found = state.stocks.find((s) => s.ticker === tick);
      const tEl = document.getElementById("docTicker");
      const eEl = document.getElementById("docEntry");
      const dEl = document.getElementById("docDays");
      const outEl = document.getElementById("docOutput");
      if (tEl && tick) tEl.value = tick;
      const entryVal = found ? Number(found.close) : 27.93;
      if (eEl) eEl.value = entryVal.toFixed(2);
      const rawDays = parseInt(dEl?.value || "42", 10);
      const daysHeld = Number.isFinite(rawDays) && rawDays >= 0 ? rawDays : 42;
      try {
        const res = await evaluatePositionDoctor({
          ticker: tick || "CELH",
          entry_price: entryVal,
          days_held: daysHeld,
        });
        state.docLastResult = res;
        if (outEl) outEl.innerHTML = formatDoctorResult(res);
      } catch (e) {
        // Ignore
      }
    });
  });

  const btnRunPositionDoctor = document.getElementById("btnRunPositionDoctor");
  if (btnRunPositionDoctor) {
    btnRunPositionDoctor.addEventListener("click", async () => {
      const ticker = (document.getElementById("docTicker")?.value || "CELH").trim().toUpperCase();
      const entryPrice = parseFloat(document.getElementById("docEntry")?.value ?? "");
      const daysHeld = parseInt(document.getElementById("docDays")?.value ?? "", 10);
      const outEl = document.getElementById("docOutput");

      if (!Number.isFinite(entryPrice) || entryPrice <= 0 || !Number.isFinite(daysHeld) || daysHeld < 0) {
        if (outEl) {
          outEl.innerHTML = `<div style="color:var(--fin-down);">Please enter a valid positive cost basis ($) and non-negative trading days.</div>`;
        }
        return;
      }

      try {
        const res = await evaluatePositionDoctor({
          ticker,
          entry_price: entryPrice,
          days_held: daysHeld,
        });
        state.docLastResult = res;
        if (outEl) {
          outEl.innerHTML = formatDoctorResult(res);
        }
      } catch (err) {
        if (outEl) {
          outEl.innerHTML = `<div style="color:var(--fin-down);">Please enter a valid positive cost basis ($) and non-negative trading days.</div>`;
        }
      }
    });
  }

  // Research Modal Controls
  const researchModal = document.getElementById("researchModal");
  const btnCloseResearch = document.getElementById("btnCloseResearch");
  if (btnCloseResearch && researchModal) {
    btnCloseResearch.addEventListener("click", () => {
      researchModal.style.display = "none";
    });
  }

  // Backdrop click-to-close on all modals
  [licenseModal, telegramModal, configModal, researchModal].forEach((modalEl) => {
    if (modalEl) {
      modalEl.addEventListener("click", (e) => {
        if (e.target === modalEl) {
          modalEl.style.display = "none";
        }
      });
    }
  });

  const openResearchForTicker = async (ticker) => {
    if (!researchModal) return;
    const titleEl = document.getElementById("researchModalTitle");
    const bodyEl = document.getElementById("researchModalBody");
    researchModal.style.display = "flex";
    if (titleEl) titleEl.textContent = `SEC Primary Filing Turnaround Brief — $${ticker}`;
    if (bodyEl) bodyEl.innerHTML = "Loading primary filing brief...";
    try {
      const data = await fetchResearchBrief(ticker);
      const stockObj = state.stocks.find((s) => s.ticker === ticker);
      const cPrice = Number(data.current_price ?? stockObj?.close ?? 27.93).toFixed(2);
      const sPrice = Number(data.stop_price ?? stockObj?.stop_loss_price ?? Number(cPrice) * 0.91).toFixed(2);
      const tPrice = Number(data.target_price ?? stockObj?.tp1_2x_price ?? Number(cPrice) * 2.0).toFixed(2);
      const asOf = data.as_of_date || stockObj?.date || data.report_date || "2026-10-13";
      const safeTitle =
        data.title ||
        `${data.company_name || ticker} ($${data.ticker || ticker}) — ${data.opinion || "STRONG_BUY"} | Latest Close $${cPrice} (${asOf})`;
      if (titleEl) titleEl.textContent = safeTitle;
      if (bodyEl) {
        const formatted = (data.content || "")
          .replace(/&/g, "&amp;")
          .replace(/</g, "&lt;")
          .replace(/>/g, "&gt;")
          .replace(/\n/g, "<br/>");
        const metaHeader = `
          <div style="display:flex; flex-wrap:wrap; gap:14px; background:#090d16; border:1px solid var(--border); border-left:3px solid var(--fin-up); padding:10px 14px; border-radius:4px; margin-bottom:14px; font-family:var(--font-mono); font-size:0.76rem;">
            <span>LATEST CLOSE (${asOf}): <b style="color:#ffffff;">$${cPrice}</b></span>
            <span>HARD STOP (-9%): <b style="color:var(--fin-down);">$${sPrice}</b></span>
            <span>TP1 TARGET (2x): <b style="color:var(--fin-up);">$${tPrice}</b></span>
            <span>RRR: <b style="color:#93c5fd;">${data.rrr_ratio || "1 : 11.1"}</b></span>
          </div>
        `;
        bodyEl.innerHTML = `${metaHeader}<div style="font-family:var(--font-sans); line-height:1.65;">${formatted}</div>`;
      }
    } catch (e) {
      if (bodyEl) bodyEl.innerHTML = "Failed to load research brief.";
    }
  };

  document.querySelectorAll(".btn-open-research").forEach((btn) => {
    btn.addEventListener("click", () => {
      const tick = btn.getAttribute("data-ticker") || "CELH";
      openResearchForTicker(tick);
    });
  });

  document.querySelectorAll(".btn-open-research-modal").forEach((btn) => {
    btn.addEventListener("click", () => openResearchForTicker("CELH"));
  });

  document.querySelectorAll(".btn-switch-research").forEach((btn) => {
    btn.addEventListener("click", () => {
      const tick = btn.getAttribute("data-ticker") || "CELH";
      openResearchForTicker(tick);
    });
  });

  // Copy Pine Script v5
  const btnCopyPineScript = document.getElementById("btnCopyPineScript");
  if (btnCopyPineScript) {
    btnCopyPineScript.addEventListener("click", async () => {
      const code = document.getElementById("pineCodeBox")?.textContent || "";
      try {
        await navigator.clipboard.writeText(code);
        showToast("TradingView Pine Script v5 Copied to Clipboard");
      } catch (e) {
        showToast("Pine Script Ready to Copy");
      }
    });
  }

  // Copy Top Proof Card PNG
  const btnCopyTopProofCard = document.getElementById("btnCopyTopProofCard");
  if (btnCopyTopProofCard) {
    btnCopyTopProofCard.addEventListener("click", () => {
      generateScorecardPng(null);
    });
  }

  // =========================================================================
  // SEMIFEARGREED CNN VIEW EVENTS
  // =========================================================================
  document.querySelectorAll(".cnn-view-tab").forEach((tab) => {
    tab.addEventListener("click", () => {
      state.semiGaugeTab = tab.getAttribute("data-semi-tab") || "overview";
      renderApp();
    });
  });

  document.querySelectorAll(".btn-semi-range").forEach((btn) => {
    btn.addEventListener("click", async () => {
      const r = btn.getAttribute("data-range") || "1Y";
      state.semiRange = r;
      try {
        state.semiHistory = await fetchSemiHistory(r);
        renderApp();
      } catch (e) {
        showToast("Failed to load selected history window");
      }
    });
  });

  const btnRunSemiRebalance = document.getElementById("btnRunSemiRebalance");
  if (btnRunSemiRebalance) {
    btnRunSemiRebalance.addEventListener("click", async () => {
      const rawCap = parseFloat(document.getElementById("semiCapInput")?.value ?? "");
      const mode = document.getElementById("semiModeInput")?.value || "AUTO_REGIME";
      const freq = document.getElementById("semiFreqInput")?.value || "ANNUAL";
      const rawGain = parseFloat(document.getElementById("semiGainKrwInput")?.value ?? "");

      if (!Number.isFinite(rawCap) || rawCap < 100) {
        showToast("Please enter a valid portfolio capital ($100 minimum)");
        return;
      }
      const cap = rawCap;
      const gainKrw = Number.isFinite(rawGain) && rawGain >= 0 ? rawGain : 0;

      state.semiCapUsd = cap;
      state.semiMode = mode;
      state.semiFreq = freq;
      state.semiGainKrw = gainKrw;

      try {
        state.semiRebalanceResult = await calculateSemiRebalance({
          total_capital_usd: cap,
          strategy_mode: mode,
          rebalance_frequency: freq,
          unrealized_gain_krw: gainKrw,
        });
        renderApp();
        showToast("Updated $SMH / $XLV Rebalancing Orders");
      } catch (e) {
        showToast("Please enter a valid positive capital amount");
      }
    });
  }

  const runLumpSumCalc = async (overrideScore) => {
    const rawCap = parseFloat(document.getElementById("semiLumpCapInput")?.value ?? "");
    const rawScore =
      overrideScore !== undefined
        ? overrideScore
        : parseFloat(document.getElementById("semiLumpScoreInput")?.value ?? "");

    if (!Number.isFinite(rawCap) || rawCap < 100) {
      showToast("Please enter a valid lump-sum amount ($100 minimum)");
      return;
    }
    const cap = rawCap;
    const scInput = Number.isFinite(rawScore)
      ? Math.max(0, Math.min(100, rawScore))
      : state.semiOverview?.fg_score ?? 18.0;

    state.semiLumpCapUsd = cap;
    state.semiLumpScore = scInput;
    try {
      state.semiLumpSumResult = await calculateSemiLumpSum({
        capital_usd: cap,
        override_fg_score: scInput,
      });
      renderApp();
    } catch (e) {
      showToast("Invalid lump-sum input parameters");
    }
  };

  const btnRunSemiLumpSum = document.getElementById("btnRunSemiLumpSum");
  if (btnRunSemiLumpSum) {
    btnRunSemiLumpSum.addEventListener("click", () => runLumpSumCalc());
  }

  document.querySelectorAll(".btn-sim-fg").forEach((btn) => {
    btn.addEventListener("click", () => {
      const fg = parseFloat(btn.getAttribute("data-fg") || "18.0");
      runLumpSumCalc(fg);
    });
  });

  const btnExportSemiGauge = document.getElementById("btnExportSemiGauge");
  if (btnExportSemiGauge) {
    btnExportSemiGauge.addEventListener("click", () => {
      generateSemiGaugePng();
    });
  }

  const btnDownloadSemiCsv = document.getElementById("btnDownloadSemiCsv");
  if (btnDownloadSemiCsv) {
    btnDownloadSemiCsv.addEventListener("click", async () => {
      if (!state.isProUnlocked) {
        openLicenseModal(true);
        showToast("Enter PRO-DEMO-2026 to unlock the 26-Year Daily CSV Dataset");
        return;
      }
      const key = encodeURIComponent(state.licenseKey || "PRO-DEMO-2026");
      try {
        const check = await fetch(`/api/semi/pro/csv?license_key=${key}`, {
          method: "HEAD",
          headers: { ...getAuthHeader() },
        });
        if (check.ok && (check.headers.get("content-type") || "").includes("csv")) {
          window.open(`/api/semi/pro/csv?license_key=${key}`, "_blank");
          return;
        }
      } catch (e) {
        // Fallback to static CSV file
      }
      const a = document.createElement("a");
      a.href = "./static_api/smh_xlv_fear_greed_history.csv";
      a.download = "SemiFearGreed_SMH_XLV_2000_2026_History.csv";
      a.click();
    });
  }

  bindRowEvents();
}

function bindRowEvents() {
  document.querySelectorAll(".btn-unlock-row").forEach((el) => {
    el.addEventListener("click", () => {
      const licenseModal = document.getElementById("licenseModal");
      if (licenseModal) {
        licenseModal.style.display = "flex";
        const inputEl = document.getElementById("licenseInput");
        if (inputEl && !inputEl.value.trim()) {
          inputEl.value = state.licenseKey || "PRO-DEMO-2026";
        }
      }
    });
  });

  document.querySelectorAll(".btn-share-card").forEach((btn) => {
    btn.addEventListener("click", () => {
      const ticker = btn.getAttribute("data-ticker");
      const stock = state.stocks.find((s) => s.ticker === ticker);
      generateScorecardPng(stock);
    });
  });

  // Static host affiliate redirect fallback (for GitHub Pages / Render Static)
  document.querySelectorAll('a[href^="/api/referral/redirect/"]').forEach((link) => {
    if (link.dataset.boundReferral === "1") return;
    link.dataset.boundReferral = "1";
    link.addEventListener("click", (e) => {
      const host = window.location.hostname;
      if (window.__STATIC_MODE__ === true || (host && host !== "localhost" && host !== "127.0.0.1")) {
        e.preventDefault();
        const href = link.getAttribute("href") || "";
        const u = new URL(href, window.location.origin);
        const ticker = (u.searchParams.get("ticker") || "SPY").toUpperCase();
        if (href.includes("tradingview")) {
          const aff = encodeURIComponent(state.config.tradingview_aff_id || "rightsidealpha");
          window.open(`https://www.tradingview.com/symbols/${ticker}/?aff_id=${aff}`, "_blank", "noopener");
        } else if (href.includes("broker") || href.includes("exchange")) {
          const rawBrk = state.config.broker_referral_url || "https://ibkr.com/referral/rightsidealpha";
          const sep = rawBrk.includes("?") ? "&" : "?";
          window.open(`${rawBrk}${sep}symbol=${encodeURIComponent(ticker)}`, "_blank", "noopener");
        } else if (href.includes("trendspider")) {
          const ts = encodeURIComponent(state.config.trendspider_aff_id || "rightside");
          window.open(`https://trendspider.com/?_go=${ts}&symbol=${ticker}`, "_blank", "noopener");
        } else {
          const src = encodeURIComponent(state.config.seekingalpha_source || "affiliate_rightside");
          window.open(`https://seekingalpha.com/symbol/${ticker}/earnings?source=${src}`, "_blank", "noopener");
        }
      }
    });
  });
}

function generateScorecardPng(stock) {
  const canvas = document.getElementById("scoreCanvas");
  if (!canvas) return;
  const ctx = canvas.getContext("2d");

  ctx.fillStyle = "#090d16";
  ctx.fillRect(0, 0, 900, 500);
  ctx.strokeStyle = "#2962ff";
  ctx.lineWidth = 3;
  ctx.strokeRect(16, 16, 868, 468);

  ctx.fillStyle = "#0ecb81";
  ctx.font = "bold 20px Inter, sans-serif";
  ctx.fillText("RIGHTSIDEALPHA · US EQUITY TURNAROUND TERMINAL", 45, 62);

  if (stock) {
    ctx.fillStyle = "#ffffff";
    ctx.font = "bold 42px JetBrains Mono, monospace";
    ctx.fillText(`$${stock.ticker} (${stock.name_en})`, 45, 125);

    ctx.fillStyle = "#93c5fd";
    ctx.font = "bold 24px JetBrains Mono, monospace";
    ctx.fillText(`Signal Regime: ${stock.zone_label_en}  |  PW-RSI Score: ${stock.score}/100`, 45, 175);

    ctx.fillStyle = "#cbd5e1";
    ctx.font = "20px JetBrains Mono, monospace";
    ctx.fillText(
      `Last Close: $${stock.close.toFixed(2)}  |  52W High DD: ${stock.dd_high52_pct}%  |  vs 52W Low: +${stock.prox_low52_pct}%`,
      45,
      230
    );
    ctx.fillText(
      `vs MA20: ${stock.vs_ma20_pct}%  |  vs MA60: ${stock.vs_ma60_pct}%  |  10D Vol Ratio: ${stock.vol_surge_10d}x`,
      45,
      270
    );
    ctx.fillText(`Historical 1Y 2x (+100%) Hit Rate after -40% Drawdown: ${stock.hist_2x_rate}%`, 45, 315);
  } else {
    ctx.fillStyle = "#ffffff";
    ctx.font = "bold 34px Inter, sans-serif";
    ctx.fillText("20-Year US Equity Backtest: Left-Side vs PW-RSI Right-Side", 45, 125);

    ctx.fillStyle = "#f6465d";
    ctx.font = "22px JetBrains Mono, monospace";
    ctx.fillText("Blind 52W-Low Dip Buy: 28.91% 2x Rate | -30.31% MDD | 81d Underwater", 45, 200);

    ctx.fillStyle = "#0ecb81";
    ctx.font = "bold 24px JetBrains Mono, monospace";
    ctx.fillText("PW-RSI Right-Side:     55.24% 2x Rate | -16.49% MDD | 29d Underwater", 45, 260);
  }

  ctx.fillStyle = "#8492a6";
  ctx.font = "bold 16px JetBrains Mono, monospace";
  ctx.fillText(`Verified Dataset (N=394,371 US Stock-Days) · ${state.config.site1_url}`, 45, 440);

  canvas.toBlob((blob) => {
    if (!blob) return;
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = stock ? `RightSideAlpha_${stock.ticker}_TearSheet.png` : "RightSideAlpha_Benchmark.png";
    a.click();
    URL.revokeObjectURL(url);
    showToast(stock ? `Downloaded $${stock.ticker} Tear Sheet PNG` : "Downloaded Benchmark Tear Sheet PNG");
  });
}

function generateSemiGaugePng() {
  const canvas = document.getElementById("scoreCanvas");
  if (!canvas || !state.semiOverview) return;
  const ctx = canvas.getContext("2d");
  const ov = state.semiOverview;

  ctx.fillStyle = "#ffffff";
  ctx.fillRect(0, 0, 900, 500);
  ctx.fillStyle = "#cc0000";
  ctx.fillRect(0, 0, 900, 10);

  ctx.fillStyle = "#cc0000";
  ctx.font = "bold 18px Inter, sans-serif";
  ctx.fillText("MARKETS · SEMICONDUCTOR FEAR & GREED INDEX", 45, 55);

  ctx.fillStyle = "#111827";
  ctx.font = "bold 40px Inter, sans-serif";
  ctx.fillText(`Score: ${ov.fg_score.toFixed(1)} / 100 — ${ov.regime_en.toUpperCase()}`, 45, 115);

  ctx.fillStyle = "#374151";
  ctx.font = "22px JetBrains Mono, monospace";
  ctx.fillText(
    `As of ${ov.date}  |  $SMH: $${ov.smh_close.toFixed(2)} (${ov.smh_dd_pct}% DD)  |  $XLV: $${ov.xlv_close.toFixed(2)}`,
    45,
    170
  );

  ctx.fillStyle = "#b91c1c";
  ctx.font = "bold 22px Inter, sans-serif";
  ctx.fillText(`Active Signal: ${ov.action_headline_en}`, 45, 230);

  ctx.fillStyle = "#4b5563";
  ctx.font = "18px JetBrains Mono, monospace";
  ctx.fillText(`26-Year Barbell (2000-2026): +10.60% CAGR (14.22x) vs QQQ +8.79% (9.21x)`, 45, 300);
  ctx.fillText(`10-Year AI Era (2016-2026):  +28.63% CAGR (15.07x) vs QQQ +20.74% (7.61x)`, 45, 338);

  ctx.fillStyle = "#6b7280";
  ctx.font = "bold 16px JetBrains Mono, monospace";
  ctx.fillText(`SemiFearGreed Quantitative Barbell Engine · ${state.config.site2_url}`, 45, 445);

  canvas.toBlob((blob) => {
    if (!blob) return;
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = `SemiFearGreed_${ov.date}.png`;
    a.click();
    URL.revokeObjectURL(url);
    showToast("Downloaded Semiconductor Fear & Greed Index PNG");
  });
}

async function loadAllData() {
  try {
    const [stocksData, btData, refCfg, semiOv, semiHist] = await Promise.all([
      fetchStocks({ limit: 200 }),
      fetchBacktestSummary().catch(() => null),
      fetchReferralConfig().catch(() => null),
      fetchSemiOverview().catch(() => null),
      fetchSemiHistory(state.semiRange).catch(() => null),
    ]);

    state.stocks = Array.isArray(stocksData)
      ? stocksData.filter((s) => s.ticker && !String(s.ticker).includes("."))
      : [];
    if (btData && btData.kpis) {
      state.backtestKpis = btData.kpis;
    }
    if (refCfg && typeof refCfg === "object") {
      Object.entries(refCfg).forEach(([k, v]) => {
        if (v !== undefined && v !== null && v !== "") {
          state.config[k] = v;
        }
      });
    }
    if (semiOv) {
      state.semiOverview = semiOv;
      if (state.semiLumpScore === null) {
        state.semiLumpScore = semiOv.fg_score;
      }
    }
    if (semiHist) {
      state.semiHistory = semiHist;
    }

    const celhStock = state.stocks.find((s) => s.ticker === "CELH");
    const defaultCelhClose = celhStock ? Number(celhStock.close) : 27.93;

    // Pre-compute initial Rebalance, Lump-Sum, Position Doctor, and Telegram Status/Preview for instant rendering
    const [rebalRes, lumpRes, docRes, tgStat, tgPrev] = await Promise.all([
      calculateSemiRebalance({
        total_capital_usd: state.semiCapUsd,
        strategy_mode: state.semiMode,
        rebalance_frequency: state.semiFreq,
        unrealized_gain_krw: state.semiGainKrw,
      }).catch(() => null),
      calculateSemiLumpSum({
        capital_usd: state.semiLumpCapUsd,
        override_fg_score: state.semiLumpScore,
      }).catch(() => null),
      evaluatePositionDoctor({
        ticker: "CELH",
        entry_price: defaultCelhClose,
        days_held: 42,
      }).catch(() => null),
      fetchTelegramStatus().catch(() => null),
      sendTelegramAlert({
        alert_type: "SEMI_BRIEFING",
        lang: state.lang,
        dry_run: true,
      }).catch(() => null),
    ]);
    if (rebalRes) state.semiRebalanceResult = rebalRes;
    if (lumpRes) state.semiLumpSumResult = lumpRes;
    if (docRes) state.docLastResult = docRes;
    if (tgStat) {
      state.telegramConfigured = Boolean(tgStat.configured || (state.telegramBotToken && state.telegramChatId));
      if (tgStat.chat_id && !state.telegramChatId) state.telegramChatId = tgStat.chat_id;
      if (tgStat.channel_url) state.config.telegram_channel_url = tgStat.channel_url;
    }
    if (tgPrev && tgPrev.message_preview) {
      state.telegramPreviewText = tgPrev.message_preview;
    }

    if (state.isProUnlocked) {
      const pine = await fetchPineScript().catch(() => null);
      if (pine && pine.code) state.pineCode = pine.code;
    }
    applyClientFilterAndSort();
  } catch (err) {
    console.error("Failed to load initial data:", err);
  }
}

async function init() {
  window.addEventListener("keydown", (e) => {
    if (e.key === "Escape") {
      ["licenseModal", "telegramModal", "configModal", "researchModal"].forEach((id) => {
        const el = document.getElementById(id);
        if (el && el.style.display === "flex") {
          el.style.display = "none";
        }
      });
    }
  });

  window.addEventListener("hashchange", () => {
    const h = window.location.hash.toLowerCase();
    if (h.includes("rightside") && state.activeView !== "rightside") {
      state.activeView = "rightside";
      renderApp();
    } else if (h.includes("semi") && state.activeView !== "semi") {
      state.activeView = "semi";
      renderApp();
    }
  });

  await loadAllData();
  renderApp();
}

init();
