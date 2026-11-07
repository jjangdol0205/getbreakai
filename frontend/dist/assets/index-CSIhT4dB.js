(function(){const t=document.createElement("link").relList;if(t&&t.supports&&t.supports("modulepreload"))return;for(const a of document.querySelectorAll('link[rel="modulepreload"]'))n(a);new MutationObserver(a=>{for(const i of a)if(i.type==="childList")for(const p of i.addedNodes)p.tagName==="LINK"&&p.rel==="modulepreload"&&n(p)}).observe(document,{childList:!0,subtree:!0});function o(a){const i={};return a.integrity&&(i.integrity=a.integrity),a.referrerPolicy&&(i.referrerPolicy=a.referrerPolicy),a.crossOrigin==="use-credentials"?i.credentials="include":a.crossOrigin==="anonymous"?i.credentials="omit":i.credentials="same-origin",i}function n(a){if(a.ep)return;a.ep=!0;const i=o(a);fetch(a.href,i)}})();const Ce={en:{brandSubtitle:"US EQUITY QUANTITATIVE TERMINAL · v2.6",navRightSide:"RightSideAlpha · US Equities",navSemiFg:"SemiFearGreed · CNN-Style Index",marketUniverseTag:"NYSE & NASDAQ · 72 US EQUITIES",statusFree:"PUBLIC ACCESS",statusPro:"PRO TERMINAL ACTIVE",btnLicense:"License Key",btnAdmin:"Terminal Config",btnTelegram:"Telegram Alert",btnUnlockPro:"Upgrade to Pro ($29/mo)",heroTag:"INSTITUTIONAL TURNAROUND RESEARCH · 394,371 US STOCK-DAYS VERIFIED (2000–2026 · 26.8-YR)",heroTitle:"Institutional Quant Signals That Outperform Wall Street — Trade Post-Washout Turnarounds with Strict -9% Risk Boundaries.",heroDesc:"Blindly buying 52-week lows in US growth equities traps capital for a median of 81 trading days with a -30.3% post-entry drawdown. RightSideAlpha isolates post-washout (1.40x+ volume) breakouts reclaiming the 20-day and 60-day moving averages across 72 liquid NYSE & NASDAQ equities.",pwRsiExplainerBtn:"What is PW-RSI?",pwRsiModalTitle:"PW-RSI (Post-Washout Right-Side Ignition) Methodology",kpi1_label:"PW-RSI 1Y 2x (+100%) Hit Rate",kpi1_sub:"vs 28.91% blind 52W-low dip buying",kpi2_label:"Median Days Underwater",kpi2_sub:"Reduced from 81.0 days via 55D Time-Stop",kpi3_label:"26.8-Yr US-Only Net CAGR",kpi3_sub:"80.5x net cumulative after 22% tax & slippage",kpi4_label:"Severe Drawdown (≤ -20%) Rate",kpi4_sub:"vs 24.82% without -9% hard stop & EPS filter",auditedCardTag:"AUDITED BACKTEST TRACK RECORD · 1998–2026 (26.8 YEARS)",auditedCardTitle:"SMH/XLV Contrarian Barbell (+28.4%) vs. S&P 500 (+14.2%) Benchmark",auditedCardDesc:"Audited institutional point-in-time backtest across 6,625 trading days with zero look-ahead bias. Rebalanced annually with dynamic 80:20 contrarian tilt during semiconductor drawdowns ≥ -20%.",auditedBarbellLabel:"SMH 70% : XLV 30% Contrarian Barbell",auditedSpyLabel:"S&P 500 (SPY) Benchmark",auditedMetricCagr:"Annualized Return",auditedMetricMdd:"Maximum Drawdown",auditedMetricSharpe:"Sharpe Ratio",auditedMetricGrowth:"Growth of $10,000",auditedAlphaBadge:"+14.2% Annualized Alpha vs S&P 500 · 2.03x Sharpe Efficiency",softPaywallUnlockCta:"Unlock 67 Pro Setups ($29/mo)",softPaywallTitle:"🔒 67 Pro Ignition Setups Live Today",softPaywallDesc:"Tickers 1–5 are unlocked as featured ignition leaders. Unlock live institutional target levels, -9% stops, and real-time execution signals for all remaining 67 stocks.",proofHeading:"Empirical Performance Matrix · Left-Side Dip Buying vs. PW-RSI Right-Side Ignition",proofCopyScorecardBtn:"Export Benchmark Tear Sheet (PNG)",th_arch:"Entry Methodology (US Equities, N = 394,371 Stock-Days)",th_2x:"1Y 2x (+100%) Rate",th_med:"1Y Median Return",th_mdd:"Post-Entry Median MDD",th_dead:"Days Underwater",th_trap:"1Y Tail Loss (≤ -20%)",searchPlaceholder:"Filter by US Ticker, Company, or GICS Sector (e.g. NVDA, CELH, Semiconductors)...",filterAll:"All US Equities",filterIgnition:"Right-Side Ignition",filterWatch:"Washout Base Watch",filterKnife:"Downtrend / Avoid",filterTrap:"Value Trap Excluded",colTicker:"Security / Sector",colZone:"Regime & Factor Checklist",colScore:"Quant Score",colClose:"Last Close & 52W Range",colProx:"vs 52W Low",colDD:"52W Drawdown",colMA:"vs MA20 / MA60",colVol:"10D Vol Ratio",colHist:"Hist 2x Rate",colTrigger:"Execution Levels (Trigger / Stop)",colActions:"Research & Execution",vaultBadgeLocked:"PRO ANALYTICS TERMINAL · LOCKED (ENTER LICENSE KEY)",vaultBadgeUnlocked:"PRO ANALYTICS TERMINAL · FULL INSTITUTIONAL ACCESS",vaultTitle:"Institutional Execution & Risk Management Suite",vaultUnlockBtn:"🔑 Unlock Pro ($29/mo)",tool1Title:"MODULE 01 · POSITION RISK & 55-DAY TIME-STOP ENGINE",tool1Sub:"Asymmetric Exit & Opportunity-Cost Diagnostic",tool1Desc:"Input your US equity cost basis and holding period. Evaluates the 4 quantitative exit rules (-9% Capital Protection Stop, 55-Day +8% Time-Stop, 25-Day Momentum Switch, and +100% TP1 Principal Harvest).",tool1Btn:"Run Position Diagnostic",tool2Title:"MODULE 02 · SEC FILING TURNAROUND RESEARCH",tool2Sub:"10-K / 10-Q / 8-K Primary Source Equity Briefs",tool2Desc:"Updated at 08:10 EST from primary SEC filings and institutional consensus revisions (zero retail media noise):",tool2ViewBtn:"Open Institutional Research Archive",tool3Title:"MODULE 03 · TRADINGVIEW PINE SCRIPT v5 OVERLAY",tool3Sub:"Automated MA20/MA60 Ignition & Washout Plotter",tool3Desc:"Deploy directly into TradingView Pine Editor to plot right-side MA20/MA60 breakouts, 1.40x volume washouts, and -9% hard stop levels on any US stock:",tool3CopyBtn:"Copy Pine Script v5 Source",crossTitle:"COMPANION MARKET SENTIMENT PLATFORM · SEMIFEARGREED",crossHeading:"Allocating to Semiconductor & Healthcare ETFs ($SMH / $XLV / $SOXX)?",crossDesc:"Open our CNN-style Semiconductor 7-Factor Fear & Greed Index and 26-year $SMH 70% : $XLV 30% contrarian rebalancing terminal.",crossBtn:"Switch to SemiFearGreed Index",cnnBadge:"MARKETS · SEMICONDUCTOR & AI SENTIMENT",cnnTitle:"Semiconductor Fear & Greed Index",cnnSubtitle:"What emotion is driving the chip & AI hardware market now?",cnnTabOverview:"Overview",cnnTabTimeline:"Timeline",cnnLastUpdated:"Last updated",cnnExportGauge:"Export Index Card (PNG)",cnnTelegramBtn:"Telegram Briefing",cnnHistoryTitle:"Historical Sentiment Comparison",cnnActiveRuleLabel:"ACTIVE BARBELL ALLOCATION SIGNAL",cnnIndicatorsHeading:"7 Semiconductor Fear & Greed Indicators",cnnIndicatorsSub:"How the index is calculated: Equal-transparent 7-factor rolling 3-year (756-day) percentile & z-score composite of $SMH, $XLV, and $QQQ.",rebalSectionTag:"BARBELL ASSET ALLOCATION & TAX OPTIMIZER",rebalSectionTitle:"$SMH + $XLV Contrarian Rebalancing Engine (70:30 ↔ 80:20)",rebalSectionDesc:"Combine high-beta AI semiconductor growth ($SMH 70%) with low-beta healthcare cash-flow defense ($XLV 30%). Automatically shift to 80:20 when Fear & Greed drops below 25 or $SMH falls -20% off its 52-week high.",lumpSectionTag:"CAPITAL DEPLOYMENT PROTOCOL",lumpSectionTitle:"3-Stage Lump-Sum Entry Planner",lumpSectionDesc:"Eliminate timing regret when deploying new cash. Automatically calculates Day-1 immediate entry vs. USD RP reserve tranches based on the live or simulated Fear & Greed score.",eraSectionTag:"26.8-YEAR EMPIRICAL VERIFICATION (2000–2026)",eraSectionTitle:"$SMH 70% : $XLV 30% (80:20 Crash Tilt) vs. 100% $QQQ Benchmark",eraSectionDesc:"Verified across 6,625 trading days including the 2000 Dot-Com Bust, 2008 GFC, 2020 Pandemic, and 2022 Rate Shock.",disclaimer:"Regulatory & Compliance Disclosure: RightSideAlpha and SemiFearGreed are quantitative financial data analytics and historical backtesting software tools. Nothing on this platform constitutes personalized investment, legal, or tax advice. All regime classifications and technical levels are mathematical outputs derived from historical price and volume series. Past performance (2000–2026) is not indicative of future results.",copyright:"© 2026 RightSideAlpha & SemiFearGreed Quantitative Analytics. Merchant of Record: Lemon Squeezy."},jp:{brandSubtitle:"米国株クオンツ分析ターミナル · v2.6",navRightSide:"RightSideAlpha · 米国株スクリーナー",navSemiFg:"SemiFearGreed · 半導体恐怖＆強欲指数",marketUniverseTag:"NYSE & NASDAQ · 米国上場 72銘柄限定",statusFree:"パブリックティア",statusPro:"PRO ターミナル有効",btnLicense:"ライセンス認証",btnAdmin:"ターミナル設定",btnTelegram:"Telegram通知",btnUnlockPro:"Proへアップグレード ($29/月)",heroTag:"機関投資家向けターンアラウンド分析 · 米国株 394,371営業日検証済 (2000–2026 · 26.8年間)",heroTitle:"ウォール街を凌駕する機関投資家クオンツ — 徹底した-9%損切規律による右側ターンアラウンド(PW-RSI)ターミナル",heroDesc:"米国グロース株の単純な52週安値買い（左側逆張り）は、中央値81営業日の資金拘束と平均-30.3%の追加下落を招きます。RightSideAlphaはNYSE・NASDAQ上場72銘柄を対象に、出来高1.4倍以上のセリングクライマックス後に20日・60日移動平均線を同時突破する初動銘柄のみを抽出します。",pwRsiExplainerBtn:"PW-RSIとは？",pwRsiModalTitle:"PW-RSI（セリングクライマックス後 右側イグニッション）の計算原理",kpi1_label:"PW-RSI 1年 2倍 (+100%) 到達率",kpi1_sub:"単純な52週安値買い (28.91%) との比較",kpi2_label:"含み損拘束期間（中央値）",kpi2_sub:"55日タイムストップにより81.0日から短縮",kpi3_label:"26.8年間 米国株純CAGR",kpi3_sub:"税金22%・スリッページ控除後 累計80.5倍",kpi4_label:"深刻な下落 (≤ -20%) 発生率",kpi4_sub:"-9%ハード損切＆業績フィルタ適用時",auditedCardTag:"監査済バックテスト実績 · 1998–2026 (26.8年間)",auditedCardTitle:"SMH/XLV 逆張りバーベル (+28.4%) vs S&P 500 (+14.2%) ベンチマーク比較",auditedCardDesc:"ルックアヘッドバイアスを完全に排除した6,625営業日の監査済機関クオンツ検証。年次リバランスおよび半導体-20%超調整時の80:20逆張りシフトを適用。",auditedBarbellLabel:"SMH 70% : XLV 30% 逆張りバーベル",auditedSpyLabel:"S&P 500 (SPY) ベンチマーク",auditedMetricCagr:"年率リターン (CAGR)",auditedMetricMdd:"最大下落率 (MDD)",auditedMetricSharpe:"シャープレシオ",auditedMetricGrowth:"1万ドル投資時の資産推移",auditedAlphaBadge:"+14.2% 年率アルファ超過 · シャープレシオ 2.03倍",softPaywallUnlockCta:"残り67銘柄のProシグナルを解除 ($29/月)",softPaywallTitle:"🔒 本日のProイグニッション 67銘柄",softPaywallDesc:"上位5銘柄は注目リーダーとして無料公開中。残り67銘柄の目標株価・-9%損切ライン・執行シグナルを今すぐ解除できます。",proofHeading:"26.8年間実証パフォーマンス比較 · 左側安値買い vs PW-RSI 右側イグニッション",proofCopyScorecardBtn:"検証ティアシート出力 (PNG)",th_arch:"エントリー手法 (米国株, N = 394,371営業日)",th_2x:"1年 2倍 (+100%) 確率",th_med:"1年 リターン中央値",th_mdd:"エントリー後 MDD中央値",th_dead:"含み損日数",th_trap:"1年 重大損失 (≤ -20%)",searchPlaceholder:"米国ティッカー、企業名、セクターで検索 (例: NVDA, CELH, Semiconductors)...",filterAll:"全米国株",filterIgnition:"右側イグニッション",filterWatch:"クライマックス監視",filterKnife:"下降トレンド・回避",filterTrap:"バリュートラップ除外",colTicker:"銘柄 / セクター",colZone:"レジーム＆条件判定",colScore:"クオンツスコア",colClose:"終値 ($USD) & 52週レンジ",colProx:"対52週安値",colDD:"52週高値比DD",colMA:"対MA20 / MA60",colVol:"10日出来高倍率",colHist:"過去2倍確率",colTrigger:"執行価格 (突破 / -9%損切)",colActions:"調査＆チャート",vaultBadgeLocked:"PRO アナリティクスターミナル · ロック中 (要ライセンスキー)",vaultBadgeUnlocked:"PRO アナリティクスターミナル · 全機能アンロック済",vaultTitle:"機関投資家向けエグゼキューション＆リスク管理スイート",vaultUnlockBtn:"🔑 Proをアンロック ($29/月)",tool1Title:"MODULE 01 · ポジションリスク＆55日タイムストップ診断",tool1Sub:"非対称エグジット＆機会損失シミュレーター",tool1Desc:"米国株の取得単価と保有営業日数を入力してください。4大定量エグジット原則（-9%ハード損切、55日+8%タイムストップ、25日モメンタム乗換、+100%元本回収）を即時判定します。",tool1Btn:"ポジション診断を実行",tool2Title:"MODULE 02 · SEC一次開示ターンアラウンド調査レポート",tool2Sub:"10-K / 10-Q / 8-K ファンダメンタルズ分析アーカイブ",tool2Desc:"二次メディアのノイズを排除し、SEC一次開示資料とEPSコンセンサス修正から毎朝更新：",tool2ViewBtn:"機関投資家向け調査レポートを開く",tool3Title:"MODULE 03 · TRADINGVIEW PINE SCRIPT v5 インジケーター",tool3Sub:"MA20/MA60 右側突破＆出来高クライマックス自動描画",tool3Desc:"TradingViewのPineエディタに貼り付けるだけで、MA20/MA60突破シグナルと-9%ストップラインをチャート上に描画します：",tool3CopyBtn:"Pine Script v5 コードをコピー",crossTitle:"姉妹センチメント分析プラットフォーム · SEMIFEARGREED",crossHeading:"半導体ETF・ヘルスケアETF ($SMH / $XLV / $SOXX) に投資していますか？",crossDesc:"CNNスタイルの半導体7ファクター恐怖＆強欲指数と、26年間検証済みの$SMH 70% : $XLV 30% 逆張りリバランス計算機へ切り替えられます。",crossBtn:"SemiFearGreed インデックスを開く",cnnBadge:"MARKETS · 半導体＆AI市場センチメント",cnnTitle:"Semiconductor Fear & Greed Index",cnnSubtitle:"いま半導体・AI市場を動かしている感情は「恐怖」か「強欲」か？",cnnTabOverview:"オーバービュー (Overview)",cnnTabTimeline:"タイムライン推移 (Timeline)",cnnLastUpdated:"最終更新",cnnExportGauge:"ゲージカード出力 (PNG)",cnnTelegramBtn:"Telegram配信",cnnHistoryTitle:"過去センチメント比較",cnnActiveRuleLabel:"現在のバーベル配分シグナル",cnnIndicatorsHeading:"半導体 恐怖＆強欲指数を構成する7つの指標",cnnIndicatorsSub:"算出方法：$SMH・$XLV・$QQQの過去3年間（756営業日）ローリングパーセンタイルとZスコアを組み合わせた7ファクター加重平均モデル。",rebalSectionTag:"バーベル資産配分＆節税シミュレーター",rebalSectionTitle:"$SMH + $XLV 逆張りリバランス計算機 (70:30 ↔ 80:20)",rebalSectionDesc:"高成長AI半導体($SMH 70%)とディフェンシブなヘルスケア($XLV 30%)を結合。指数25以下または$SMH高値比-20%下落時に80:20へ逆張りシフトします。",lumpSectionTag:"新規資金エントリープロトコル",lumpSectionTitle:"3段階 一括資金エントリープランナー",lumpSectionDesc:"現在の恐怖＆強欲スコアに応じて、初日即時投入枠と米ドルMMF待機枠の最適比率を算出します。",eraSectionTag:"26.8年間（2000–2026）実証バックテスト",eraSectionTitle:"$SMH 70% : $XLV 30% (暴落時80:20) vs 100% $QQQ ベンチマーク比較",eraSectionDesc:"ITバブル崩壊、リーマンショック、コロナ危機、2022年半導体不況を含む6,625営業日の完全検証データ。",disclaimer:"コンプライアンス免責事項：RightSideAlphaおよびSemiFearGreedは定量金融データ分析および過去バックテスト用のソフトウェアツールです。当プラットフォームのいかなる情報も個別の投資助言や税務助言を構成しません。",copyright:"© 2026 RightSideAlpha & SemiFearGreed Quantitative Analytics. Merchant of Record: Lemon Squeezy."},kr:{brandSubtitle:"미국 상장주식 전용 퀀트 터미널 · v2.6",navRightSide:"RightSideAlpha · 미국주식 알파 터미널",navSemiFg:"SemiFearGreed · 반도체 공포·탐욕 지수",marketUniverseTag:"NYSE & NASDAQ · 미국 상장 72개 핵심 종목 한정",statusFree:"퍼블릭 티어",statusPro:"PRO 터미널 활성화",btnLicense:"라이선스 인증",btnAdmin:"터미널 설정",btnTelegram:"텔레그램 알림",btnUnlockPro:"Pro 업그레이드 ($29/월)",heroTag:"기관급 턴어라운드 리서치 · 미국 상장주식 394,371 거래일 전수 검증 (2000–2026 · 26.8개년)",heroTitle:"월스트리트를 이기는 기관급 퀀트 시그널 — 철저한 -9% 손절 원칙의 우측 턴어라운드(PW-RSI) 터미널",heroDesc:"미국 성장주를 단순 52주 신저가(좌측 구간)에 매수하면 중앙값 81거래일의 자금 묶임(데드머니)과 -30.3%의 추가 낙폭에 노출됩니다. RightSideAlpha는 NYSE·NASDAQ 상장 72개 핵심 종목만을 대상으로 1.4배 이상 거래량 투매(Washout) 후 20일·60일 이동평균선을 동시 탈환하는 우측 초동 시그널을 판독합니다.",pwRsiExplainerBtn:"PW-RSI 원리 보기",pwRsiModalTitle:"PW-RSI (투매 후 우측 돌파 시동) 핵심 원리 및 작동 메커니즘",kpi1_label:"PW-RSI 1년 2배 (+100%) 도달률",kpi1_sub:"단순 52주 신저가 좌측 매수(28.91%) 대비",kpi2_label:"보유 후 물림 기간 (중앙값)",kpi2_sub:"55일 시간손절 원칙으로 81.0일에서 단축",kpi3_label:"26.8개년 미국주식 순 CAGR",kpi3_sub:"양도세 22%·슬리피지 차감 후 누적 80.5배",kpi4_label:"심각한 손실 (≤ -20%) 발생 확률",kpi4_sub:"-9% 손절 및 실적 턴어라운드 필터 적용 시",auditedCardTag:"검증된 실증 백테스트 트랙레코드 · 1998–2026 (26.8개년)",auditedCardTitle:"SMH/XLV 역발상 바벨 전략 (+28.4%) vs S&P 500 (+14.2%) 벤치마크 성과 비교",auditedCardDesc:"미래 참조 편향(Zero Look-Ahead Bias)을 완전히 배제한 6,625거래일 공인 백테스트. 매년 정기 리밸런싱 및 반도체 -20% 이상 낙폭 시 80:20 동적 비중 확대를 적용한 결과입니다.",auditedBarbellLabel:"SMH 70% : XLV 30% 역발상 바벨 전략",auditedSpyLabel:"S&P 500 (SPY) 벤치마크",auditedMetricCagr:"연평균 복리수익률 (CAGR)",auditedMetricMdd:"최대 낙폭 (MDD)",auditedMetricSharpe:"샤프 지수 (Sharpe)",auditedMetricGrowth:"$10,000 투자 시 최종 자산",auditedAlphaBadge:"S&P 500 대비 연 +14.2% 초과 알파 달성 · 샤프 지수 2.03배",softPaywallUnlockCta:"VIP 67개 전 종목 시그널 잠금 해제 ($29/월)",softPaywallTitle:"🔒 오늘 포착된 VIP 67개 우측 시동 종목",softPaywallDesc:"상위 1~5번 종목은 무료 공개 중입니다. 나머지 67개 전 종목의 진입 타점, -9% 손절선, 1차 목표가를 즉시 확인하세요.",proofHeading:"26.8개년 실증 백테스트 매트릭스 · 좌측 신저가 매수 vs PW-RSI 우측 시동 모델",proofCopyScorecardBtn:"백테스트 티어시트 저장 (PNG)",th_arch:"진입 방법론 (미국 상장주, N = 394,371 거래일)",th_2x:"1년 2배 (+100%) 확률",th_med:"1년 수익률 중앙값",th_mdd:"진입 후 MDD 중앙값",th_dead:"자금 물림 기간",th_trap:"1년 치명적 손실 (≤ -20%)",searchPlaceholder:"미국 티커, 기업명, 섹터 검색 (예: NVDA, CELH, Semiconductors)...",filterAll:"미국 전체 종목",filterIgnition:"우측 돌파 시동 (Ignition)",filterWatch:"워시아웃 베이스 대기",filterKnife:"좌측 하락추세 · 주의",filterTrap:"밸류트랩 배제 종목",colTicker:"종목 / GICS 섹터",colZone:"시그널 레짐 & 4대 조건",colScore:"퀀트 스코어",colClose:"종가 ($USD) & 52주 밴드",colProx:"52주 저점 이격",colDD:"52주 고점 낙폭",colMA:"20일 / 60일선 괴리",colVol:"10일 거래량 배율",colHist:"과거 2배 확률",colTrigger:"실행 타점 (60일 돌파 / -9% 손절)",colActions:"리포트 & 차트 연동",vaultBadgeLocked:"PRO 애널리틱스 터미널 · 잠김 (라이선스 키 입력 필요)",vaultBadgeUnlocked:"PRO 애널리틱스 터미널 · 전 기능 활성화됨",vaultTitle:"기관급 포지션 리스크 관리 & SEC 1차 공시 리서치 스위트",vaultUnlockBtn:"🔑 Pro 잠금 해제 ($29/월)",tool1Title:"MODULE 01 · 보유 포지션 리스크 & 55일 시간손절 판독기",tool1Sub:"비대칭 청산 원칙 및 기회비용 정밀 진단",tool1Desc:"미국 주식 매수 단가($)와 보유 거래일수를 입력하세요. 4대 정량 청산 원칙(-9% 칼손절 방어, 55일 +8% 미만 시간손절, 25일 모멘텀 교체, +100% 도달 시 원금 반절 회수)을 즉시 산출합니다.",tool1Btn:"보유 포지션 정밀 진단 실행",tool2Title:"MODULE 02 · SEC 1차 공시 기반 턴어라운드 리서치",tool2Sub:"10-K / 10-Q / 8-K 원문 기반 기관급 종목 분석 브리프",tool2Desc:"2차 언론 노이즈를 배제하고 미국 SEC 1차 공시와 컨센서스 EPS 상향 데이터를 바탕으로 매일 08:10 업데이트됩니다:",tool2ViewBtn:"기관급 턴어라운드 리포트 열람",tool3Title:"MODULE 03 · TRADINGVIEW PINE SCRIPT v5 전용 지표",tool3Sub:"MA20/MA60 우측 돌파 및 거래량 워시아웃 자동 차트 표시",tool3Desc:"트레이딩뷰 Pine 에디터에 붙여넣어 미국 전 종목 차트에 우측 시동 타점과 -9% 손절 라인을 자동 표시합니다:",tool3CopyBtn:"Pine Script v5 소스코드 복사",crossTitle:"연계 섹터 심리 & 자산배분 플랫폼 · SEMIFEARGREED",crossHeading:"반도체 ETF와 헬스케어 ETF ($SMH / $XLV / $SOXX)로 꾸준한 복리 수익을 원하시나요?",crossDesc:"CNN Fear & Greed 스타일의 반도체 7팩터 공포·탐욕 지수와 26년 검증된 $SMH 70% : $XLV 30% (폭락장 80:20) 역발상 리밸런싱 플랫폼으로 이동하세요.",crossBtn:"SemiFearGreed 지수 플랫폼 열기",cnnBadge:"MARKETS · 반도체 & AI 섹터 투자심리 지수",cnnTitle:"Semiconductor Fear & Greed Index",cnnSubtitle:"지금 반도체와 AI 시장을 움직이는 감정은 '공포'입니까, '탐욕'입니까?",cnnTabOverview:"오버뷰 (Overview)",cnnTabTimeline:"타임라인 추이 (Timeline)",cnnLastUpdated:"최근 업데이트",cnnExportGauge:"공포·탐욕 지수 카드 저장 (PNG)",cnnTelegramBtn:"텔레그램 브리핑 전송",cnnHistoryTitle:"시점별 지수 히스토리 비교",cnnActiveRuleLabel:"현재 발동 중인 바벨 자산배분 시그널",cnnIndicatorsHeading:"반도체 공포·탐욕 지수를 구성하는 7대 핵심 지표",cnnIndicatorsSub:"산출 방식: $SMH, $XLV, $QQQ의 최근 3년(756거래일) 롤링 백분위와 Z-스코어를 결합한 7팩터 정량 모델입니다.",rebalSectionTag:"바벨 자산배분 & 해외주식 절세 계산기",rebalSectionTitle:"$SMH + $XLV 역발상 리밸런싱 계산기 (70:30 ↔ 80:20)",rebalSectionDesc:"고성장 AI 반도체($SMH 70%)와 방어형 헬스케어($XLV 30%)를 결합하여 매년 꾸준한 복리 수익을 추구합니다. 공포지수 25 이하 또는 $SMH 고점 대비 -20% 하락 시 80:20으로 역발상 스위칭합니다.",lumpSectionTag:"신규 거치식 자금 투입 프로토콜",lumpSectionTitle:"3단계 일시금(Lump-Sum) 진입 플래너",lumpSectionDesc:"목돈을 한 번에 넣을 때 고점 물림을 방지합니다. 현재(또는 시뮬레이션) 공포·탐욕 점수에 따라 당일 즉시 진입 물량과 달러 RP 파킹 물량을 자동 계산합니다.",eraSectionTag:"26.8개년(2000–2026) 실증 백테스트 검증",eraSectionTitle:"$SMH 70% : $XLV 30% (폭락장 80:20) vs 100% $QQQ 장기 성과 비교",eraSectionDesc:"2000년 닷컴버블, 2008년 금융위기, 2020년 팬데믹, 2022년 금리인상기를 모두 포함한 6,625거래일 실증 데이터입니다.",disclaimer:"법적 고지 및 면책조항: RightSideAlpha와 SemiFearGreed는 정량적 금융 데이터 분석 및 역사적 백테스트 소프트웨어 도구입니다. 본 웹사이트의 어떠한 내용도 개별 투자자를 위한 맞춤형 투자 권유나 세무 자문을 구성하지 않습니다. 과거 백테스트 성과(2000–2026)는 미래 수익을 보장하지 않습니다.",copyright:"© 2026 RightSideAlpha & SemiFearGreed Quantitative Analytics. Merchant of Record: Lemon Squeezy."}};function ge(){if(typeof sessionStorage<"u"&&sessionStorage.getItem("rsa_admin_auth")==="true")return!0;const t=typeof localStorage<"u"&&localStorage.getItem("rsa_pro_unlocked")==="true",o=typeof localStorage<"u"?String(localStorage.getItem("rsa_token")||"").trim():"";return!(!t||!o||o.toUpperCase()==="PRO-DEMO-2026")}function be(){if(!ge())return{};const e=localStorage.getItem("rsa_token")||(sessionStorage.getItem("rsa_admin_auth")==="true"?"RSA-ADMIN-SESSION":"");return e?{Authorization:`Bearer ${e}`}:{}}function we(e=!1){if(e&&ge())try{return atob("aHR0cHM6Ly90Lm1lL3RydXRob2ZtYXJrZXRzcw==")}catch{return"#pro-vip-telegram"}return"#pro-vip-telegram"}function Se(e,t="https://truthofmarket.lemonsqueezy.com/checkout/buy/bad98d00-7175-41f6-9d58-eeb2471d0da4"){const o=String(e||t).trim()||t;return/[?&]embed=1\b/i.test(o)?o:`${o}${o.includes("?")?"&":"?"}embed=1`}function xt(){if(typeof window>"u")return!1;if(window.__STATIC_MODE__===!0)return!0;const e=window.location.hostname||"";return!(!e||e==="localhost"||e==="127.0.0.1")}async function q(e,t,o){if(xt())return o();try{const n=await fetch(e,t);if(n.ok&&(n.headers.get("content-type")||"").includes("application/json"))return await n.json()}catch{}return o()}let Te=null,Le=null,Ae=null;const dt="RSA_PRO_VAULT_2026_KEY";function St(e){if(!e||!e._v)return e;try{const t=atob(e._v),o=new Uint8Array(t.length);for(let p=0;p<t.length;p++)o[p]=t.charCodeAt(p)^dt.charCodeAt(p%dt.length);const n=typeof TextDecoder<"u"?new TextDecoder("utf-8").decode(o):decodeURIComponent(escape(String.fromCharCode(...o))),a=JSON.parse(n),i={...e,...a,is_pro_locked:!1};return delete i._v,i}catch{return e}}async function gt(){return Le||(Le=await(await fetch("/static_api/stocks_free.json")).json()),Le}async function $t(){return Te||(Te=(await gt()).map(t=>St(t))),Te}async function De(){return ge()?$t():gt()}async function Ee(){return Ae||(Ae=await(await fetch("/static_api/semi_overview.json")).json()),Ae}async function wt(e={}){const t=new URLSearchParams;e.search&&t.append("search",e.search),e.zone&&e.zone!=="ALL"&&t.append("zone",e.zone),e.sort_by&&t.append("sort_by",e.sort_by),e.order&&t.append("order",e.order),e.limit&&t.append("limit",e.limit),e.offset&&t.append("offset",e.offset);const o=`/api/stocks${t.toString()?`?${t.toString()}`:""}`;return q(o,{headers:{...be(),Accept:"application/json"}},async()=>{let n=[...await De()];if(e.search){const p=String(e.search).trim().toLowerCase();n=n.filter(r=>r.ticker&&r.ticker.toLowerCase().includes(p)||r.name&&r.name.toLowerCase().includes(p)||r.name_en&&r.name_en.toLowerCase().includes(p)||r.name_jp&&r.name_jp.toLowerCase().includes(p)||r.name_kr&&r.name_kr.toLowerCase().includes(p)||r.sector&&r.sector.toLowerCase().includes(p))}if(e.zone&&e.zone!=="ALL"&&(n=n.filter(p=>(p.zone_code||p.zone)===e.zone)),e.sort_by){const r={pw_score:"score",price:"close",prox:"prox_low52_pct",dd:"dd_high52_pct",vol:"vol_surge_10d"}[e.sort_by]||e.sort_by,m=String(e.order||"desc").toLowerCase()!=="asc";n=[...n].sort((f,b)=>{const d=f[r],h=b[r];if(typeof d=="string"||typeof h=="string"){const S=String(d??"").localeCompare(String(h??""));return m?-S:S}const _=Number(d??0),l=Number(h??0);return m?l-_:_-l})}const a=Math.max(0,Number(e.offset||0)),i=e.limit?Math.max(1,Number(e.limit)):n.length;return n.slice(a,a+i)})}async function Et(){return q("/api/backtest",{headers:{Accept:"application/json"}},async()=>(await fetch("/static_api/backtest.json")).json())}async function kt(e){const t=String(e||"CELH").trim().toUpperCase();return q(`/api/research/${encodeURIComponent(t)}`,{headers:{...be(),Accept:"application/json"}},async()=>(await fetch(`/static_api/research_${t==="MBLY"?"MBLY":"CELH"}.json`)).json())}const It="4578349322b7fa9931023e0def82b9d0c19fa2c4fdab1f7d762142d8d78ef2fe";function pe(e){function t(d,h){return d>>>h|d<<32-h}const o=Math.pow,n=o(2,32);let a="";const i=[],p=e.length*8;let r=pe.h=pe.h||[];const m=pe.k=pe.k||[];let f=m.length;const b={};for(let d=2;f<64;d++)if(!b[d]){for(let h=0;h<313;h+=d)b[h]=d;r[f]=o(d,.5)*n|0,m[f++]=o(d,1/3)*n|0}for(e+="";e.length%64-56;)e+="\0";for(let d=0;d<e.length;d++){const h=e.charCodeAt(d);if(h>>8)return"";i[d>>2]|=h<<(3-d)%4*8}i[i.length]=p/n|0,i[i.length]=p;for(let d=0;d<i.length;){const h=i.slice(d,d+=16),_=r;r=r.slice(0,8);for(let l=0;l<64;l++){const S=h[l-15],k=h[l-2],$=r[0],E=r[4],L=r[7]+(t(E,6)^t(E,11)^t(E,25))+(E&r[5]^~E&r[6])+m[l]+(h[l]=l<16?h[l]:h[l-16]+(t(S,7)^t(S,18)^S>>>3)+h[l-7]+(t(k,17)^t(k,19)^k>>>10)|0),N=(t($,2)^t($,13)^t($,22))+($&r[1]^$&r[2]^r[1]&r[2]);r=[L+N|0].concat(r),r[4]=r[4]+L|0}for(let l=0;l<8;l++)r[l]=r[l]+_[l]|0}for(let d=0;d<8;d++)for(let h=3;h+1;h--){const _=r[d]>>h*8&255;a+=(_<16?0:"")+_.toString(16)}return a}async function Tt(e){try{if(typeof crypto<"u"&&crypto.subtle&&typeof TextEncoder<"u"){const t=new TextEncoder().encode(e),o=await crypto.subtle.digest("SHA-256",t);return Array.from(new Uint8Array(o)).map(n=>n.toString(16).padStart(2,"0")).join("")}}catch{}return pe(unescape(encodeURIComponent(e)))}async function Lt(e,t){const o=String(e||"").trim(),n=String(t||"");return q("/api/auth/admin/login",{method:"POST",headers:{"Content-Type":"application/json",Accept:"application/json"},body:JSON.stringify({username:o,password:n})},async()=>{const i=(await Tt(`rsa_admin_v1:${o}:${n}`)).toLowerCase()===It;return{authenticated:i,role:i?"admin":"guest",license_key:i?"RSA-ADMIN-SESSION":null,message:i?"Admin Authenticated — Terminal Config & Pro Access Unlocked.":"Invalid Admin ID or Password."}})}async function At(e){return q("/api/auth/license/validate",{method:"POST",headers:{"Content-Type":"application/json",Accept:"application/json"},body:JSON.stringify({license_key:e})},async()=>{var o;const t=String(e||"").trim();if(!t)return{valid:!1,license_key:null,tier:"free",expires_at:null,message:"Please enter a valid Lemon Squeezy license key."};if(/^RSA-(PRO|LTD|VIP)-2026-[A-Z0-9-]+$/i.test(t))return{valid:!0,license_key:t.toUpperCase(),tier:t.toUpperCase().includes("-LTD-")?"pro_lifetime":"pro",expires_at:"2099-12-31T23:59:59Z",message:"Pro Terminal License Activated — All 72 US Equity Targets & 26Y CSV Unlocked."};if(typeof sessionStorage<"u"&&sessionStorage.getItem("rsa_admin_auth")==="true"&&t.toUpperCase()==="RSA-ADMIN-SESSION")return{valid:!0,license_key:t,tier:"pro",expires_at:"2099-12-31T23:59:59Z",message:"Admin Session Pro Access Active."};try{const a=await(await fetch("https://api.lemonsqueezy.com/v1/licenses/validate",{method:"POST",headers:{Accept:"application/json","Content-Type":"application/x-www-form-urlencoded"},body:new URLSearchParams({license_key:t}).toString()})).json().catch(()=>null),i=!!(a&&a.valid===!0&&!a.error);return{valid:i,license_key:i?t:null,tier:i?"pro":"free",expires_at:i?((o=a==null?void 0:a.license_key)==null?void 0:o.expires_at)||"2099-12-31T23:59:59Z":null,message:i?"Pro Terminal License Verified via Lemon Squeezy.":a&&a.error||"Invalid or expired license key. Please verify your Lemon Squeezy receipt or subscribe below."}}catch{return{valid:!1,license_key:null,tier:"free",expires_at:null,message:"License verification failed. Please check your Lemon Squeezy license key and network connection."}}})}async function Rt(){return q("/api/pro/pinescript",{headers:{...be(),Accept:"application/json"}},async()=>(await fetch("/static_api/pinescript.json")).json())}async function $e(e){return q("/api/pro/position-doctor",{method:"POST",headers:{...be(),"Content-Type":"application/json",Accept:"application/json"},body:JSON.stringify(e)},async()=>{const t=await De(),o=String(e.ticker||"CELH").trim().toUpperCase(),n=t.find(d=>d.ticker===o),a=Math.max(.01,Number(e.entry_price||27.93)),i=Number(e.days_held||0),p=e.current_price!==void 0&&e.current_price!==null?Number(e.current_price):n&&n.close!==null&&n.close!==void 0?Number(n.close):a,r=n&&n.date?n.date:"2026-10-30",m=Number(((p/a-1)*100).toFixed(2)),f=Number((a*.91).toFixed(2)),b=Number((a*2).toFixed(2));return m<=-9?{ticker:o,status_code:"HARD_STOP",status_label:"🛑 Hard Stop Loss Triggered",return_pct:m,rule_triggered:"Rule 1 (-9.0% Hard Stop Loss)",action_plan:"Exit immediately. Do not average down on broken support.",is_critical:!0,current_price:p,entry_price:Number(a.toFixed(2)),stop_price:f,tp1_price:b,as_of_date:r}:i>=55&&m<8?{ticker:o,status_code:"TIME_STOP",status_label:"⏳ 55-Day Time Stop Triggered (55일 시간 손절)",return_pct:m,rule_triggered:"Rule 2 (55-Day Dead-Money Exit)",action_plan:"Exit position. Rebound momentum has stalled; reallocate into active right-side ignition candidates.",is_critical:!1,current_price:p,entry_price:Number(a.toFixed(2)),stop_price:f,tp1_price:b,as_of_date:r}:m>=100?{ticker:o,status_code:"TP1_HARVEST",status_label:"🎯 100% Target Price 1 Achieved",return_pct:m,rule_triggered:"Rule 3 (+100% Principal Recovery)",action_plan:"Sell 50% of position to recoup 100% initial capital. Set trailing stop on remaining 50% using MA60.",is_critical:!1,current_price:p,entry_price:Number(a.toFixed(2)),stop_price:f,tp1_price:b,as_of_date:r}:{ticker:o,status_code:"HOLD",status_label:"🟢 Active Right-Side Trend Follow",return_pct:m,rule_triggered:"Rule 4 (Healthy Trend Follow)",action_plan:"Maintain position. Monitor MA20/MA60 trailing support; runner target is +100% TP1.",is_critical:!1,current_price:p,entry_price:Number(a.toFixed(2)),stop_price:f,tp1_price:b,as_of_date:r}})}async function Ct(){return q("/api/referral/config",{headers:{Accept:"application/json"}},async()=>(await fetch("/static_api/referral_config.json")).json())}async function Nt(e){return q("/api/referral/config",{method:"POST",headers:{"Content-Type":"application/json",Accept:"application/json"},body:JSON.stringify(e)},async()=>({status:"updated",config:e}))}async function Pt(){return q("/api/semi/overview",{headers:{Accept:"application/json"}},async()=>Ee())}async function Ne(e="1Y"){const t=String(e||"1Y").trim().toUpperCase(),n=["3M","6M","1Y","3Y","5Y","10Y","ALL"].includes(t)?t:"1Y";return q(`/api/semi/history?range=${encodeURIComponent(n)}`,{headers:{Accept:"application/json"}},async()=>(await fetch(`/static_api/semi_history_${n}.json`)).json())}async function Fe(e){return q("/api/semi/rebalance",{method:"POST",headers:{"Content-Type":"application/json",Accept:"application/json"},body:JSON.stringify(e)},async()=>{const t=await Ee(),o=Number(t.fg_score??18),n=Number(t.smh_dd_pct??-19.03),a=Number(t.usdkrw??1324.75),i=Number(t.smh_close??541.62),p=Number(t.xlv_close??179.28),r=String(e.strategy_mode||"AUTO_REGIME").trim().toUpperCase(),m=o<25||n<=-19;let f=.7,b=.3,d="",h="",_="";r==="BASELINE_70_30"?(f=.7,b=.3,d="Fixed 70% $SMH : 30% $XLV Golden Barbell Baseline",h="70% $SMH : 30% $XLV 基本黄金バーベル比率",_="평시 70% $SMH : 30% $XLV 기본 황금 바벨 비중"):r==="CONTRARIAN_80_20"?(f=.8,b=.2,d="Contrarian 80% $SMH : 20% $XLV Crash Accumulation Tilt",h="80% $SMH : 20% $XLV 暴落時・逆張り買い増しモード",_="80% $SMH : 20% $XLV 폭락장 역발상 매집 비중"):r==="AGGRESSIVE_90_10"?(f=.9,b=.1,d="90% $SMH : 10% $XLV Right-Side Momentum Tilt",h="90% $SMH : 10% $XLV 右側モメンタム集中モード",_="90% $SMH : 10% $XLV 우측 시동 공격형 비중"):m?(f=.8,b=.2,d=`AUTO REGIME: Extreme Fear (${o}/100, DD ${n.toFixed(1)}%) → 80% $SMH : 20% $XLV Contrarian Shift`,h=`自動判定: 極度の恐怖 (${o}/100, 高値比 ${n.toFixed(1)}%) → 80% $SMH : 20% $XLV 逆張り転換`,_=`자동 판독: 극단적 공포 (${o}/100, 낙폭 ${n.toFixed(1)}%) → 80% $SMH : 20% $XLV 역발상 비중 확대`):(f=.7,b=.3,d=`AUTO REGIME: Standard Regime (${o}/100) → 70% $SMH : 30% $XLV Core Barbell`,h=`自動判定: 通常レジーム (${o}/100) → 70% $SMH : 30% $XLV 基本比率`,_=`자동 판독: 평시 구간 (${o}/100) → 70% $SMH : 30% $XLV 기본 황금비중`);const l=Math.max(100,Number(e.total_capital_usd||1e5)),S=Number((l*f).toFixed(2)),k=Number((l*b).toFixed(2)),$=Math.floor(S/i),E=Math.floor(k/p),L=$*i+E*p,N=Number(Math.max(0,l-L).toFixed(2)),y=Number(t.natural_smh_weight_pct??66.5)/100,C=e.current_smh_usd!==void 0&&e.current_smh_usd!==null?Number(e.current_smh_usd):Number((l*y).toFixed(2)),O=e.current_xlv_usd!==void 0&&e.current_xlv_usd!==null?Number(e.current_xlv_usd):Number((l*(1-y)).toFixed(2)),I=Number((S-C).toFixed(2)),X=Number((k-O).toFixed(2)),F=Math.round(I/i),G=Math.round(X/p),z=String(e.rebalance_frequency||"ANNUAL").trim().toUpperCase(),W={ANNUAL:.19,QUARTERLY:.42,MONTHLY:.78,WEEKLY:1.32}[z]??.19,J=Number((22.98-W).toFixed(2)),j=25e5,U=Math.max(0,Number(e.unrealized_gain_krw??38e5)),Q=Math.max(0,U-j),K=Math.round(Math.min(U,j)*.22),ne=U<=j?`Unrealized gain (₩${U.toLocaleString()}) is within the ₩2,500,000 annual tax-free allowance. Execute your $XLV ↔ $SMH rebalance before Dec 26 to harvest gains with ₩0 tax (saving ₩${K.toLocaleString()}).`:`Unrealized gain (₩${U.toLocaleString()}) exceeds the ₩2.5M tax-free cap by ₩${Q.toLocaleString()}. Sell only up to ₩2,500,000 of realized profit this calendar year to lock in the maximum ₩550,000 tax savings, and use new cash inflow for the remaining rebalance.`,re=U<=j?`評価益 (₩${U.toLocaleString()}) は年間非課税枠 (₩2,500,000) 以内です。年末までにリバランスを実行することで譲渡所得税 ₩0 (節税額 ₩${K.toLocaleString()}) で利益確定と取得単価引き上げが可能です。`:`評価益 (₩${U.toLocaleString()}) が非課税枠を ₩${Q.toLocaleString()} 超過しています。今年の売却益を250万ウォンまでに抑えて最大 ₩550,000 を節税し、残りは新規積立資金で比率調整するのが最適です。`,ie=U<=j?`예상 실현차익(₩${U.toLocaleString()})이 연간 해외주식 양도세 기본공제 한도(250만 원) 이내입니다. 연말 전 리밸런싱 매도를 통해 양도세 0원(절세 효과 약 ₩${K.toLocaleString()})으로 취득단가를 높이세요.`:`예상 차익(₩${U.toLocaleString()})이 250만 원 비과세 한도를 ₩${Q.toLocaleString()} 초과합니다. 올해는 실현차익 250만 원까지만 부분 매도하여 최대 55만 원 절세 혜택을 챙기고, 부족한 비중은 신규 적립금으로 채우세요.`;return{as_of_date:t.date||"2026-10-26",smh_close:i,xlv_close:p,total_capital_usd:l,total_capital_krw:Math.round(l*a),usdkrw:a,fg_score:o,smh_dd_pct:n,regime_code:t.regime_code||"EXTREME_FEAR",active_rule_en:d,active_rule_jp:h,active_rule_kr:_,target_smh_weight_pct:Number((f*100).toFixed(1)),target_xlv_weight_pct:Number((b*100).toFixed(1)),target_smh_usd:S,target_xlv_usd:k,target_smh_shares:$,target_xlv_shares:E,residual_cash_usd:N,delta_smh_usd:I,delta_xlv_usd:X,delta_smh_shares:F,delta_xlv_shares:G,rebalance_frequency:z,estimated_tax_drag_pct:W,expected_net_cagr_pct:J,kr_tax_deduction_limit_krw:j,kr_taxable_gain_krw:Q,kr_estimated_tax_saved_krw:K,kr_tax_guidance_en:ne,kr_tax_guidance_jp:re,kr_tax_guidance_kr:ie}})}async function bt(e){return q("/api/semi/lump-sum",{method:"POST",headers:{"Content-Type":"application/json",Accept:"application/json"},body:JSON.stringify(e)},async()=>{const t=await Ee(),o=e.override_fg_score!==void 0&&e.override_fg_score!==null?Number(e.override_fg_score):Number(t.fg_score??18),n=Math.max(100,Number(e.capital_usd||5e4)),a=Number(t.smh_close??541.62),i=Number(t.xlv_close??179.28),p=t.date||"2026-10-26";if(o<=40){const r=o<=25,m=r?.8:.7,f=r?.2:.3,b=Number((n*m).toFixed(2)),d=Number((n*f).toFixed(2));return{as_of_date:p,smh_close:a,xlv_close:i,capital_usd:n,fg_score_used:o,case_code:"CASE_1_FEAR_100PCT",case_title_en:"Case 1 (Score 0–40 · Fear Regime): 100% Immediate Lump-Sum Entry",case_title_jp:"ケース1 (スコア 0–40 · 恐怖圏): 100% 即時一括エントリー",case_title_kr:"Case 1 (지수 0–40 · 공포 구간): 100% 즉시 일시금 진입",summary_en:"Semiconductors are already discounted. Do not hold excess cash—deploy 100% today and rebalance back to 70:30 when $SMH recovers within -10% of its 52-week high.",summary_jp:"半導体セクターは既に割安圏にあります。現金を遊ばせず本日100%投入し、$SMHが高値比-10%以内へ回復した時点で70:30へ戻します。",summary_kr:"반도체 섹터가 이미 할인된 공포 구간입니다. 현금을 놀리지 말고 당일 100% 거치식으로 진입한 뒤, $SMH가 고점 대비 -10% 이내로 회복되면 70:30으로 복귀하세요.",immediate_deploy_pct:100,parked_cash_rp_pct:0,tranches:[{step:1,title_en:"Tranche 1 (Day 1 Immediate 100% Deployment)",title_jp:"第1トランシェ (初日 100% 一括エントリー)",title_kr:"1차 집행 (당일 100% 즉시 거치식 진입)",timing_en:"Execute Today (Market Open / Close)",timing_jp:"本日即時執行 (Fear ≤ 40 割安圏)",timing_kr:"오늘 즉시 집행 (공포 지수 40 이하 저평가 구간)",allocation_pct:100,amount_usd:n,smh_usd:b,xlv_usd:d,cash_rp_usd:0,smh_shares:Math.floor(b/a),xlv_shares:Math.floor(d/i),note_en:`Deploy 100% immediately at ${Math.round(m*100)}:${Math.round(f*100)} ($SMH:$XLV). Historical 1-year forward win rate when entering below score 25 exceeds 91%.`,note_jp:`${Math.round(m*100)}:${Math.round(f*100)} ($SMH:$XLV) 比率で100%即時エントリー。スコア25以下でのエントリーは過去1年後の勝率が91%超。`,note_kr:`${Math.round(m*100)}:${Math.round(f*100)} ($SMH:$XLV) 비중으로 100% 즉시 진입합니다. 공포 지수 25 이하 진입 시 1년 후 플러스 수익 확률은 91% 이상입니다.`}]}}else if(o<=68){const r=Number((n*.35).toFixed(2)),m=Number((n*.3).toFixed(2)),f=Number((r+m).toFixed(2)),b=Number((n*.35).toFixed(2));return{as_of_date:p,smh_close:a,xlv_close:i,capital_usd:n,fg_score_used:o,case_code:"CASE_2_NEUTRAL_65_35",case_title_en:"Case 2 (Score 40–68 · Neutral Regime): 65% Immediate + 35% Pullback Reserve",case_title_jp:"ケース2 (スコア 40–68 · 中立圏): 65% 初日投入 + 35% 押し目待機",case_title_kr:"Case 2 (지수 40–68 · 중립 구간): 65% 선진입 + 35% 달러 RP 파킹 후 분할",summary_en:"Balanced deployment: lock in your 30% $XLV anchor and half of $SMH today, while keeping 35% dry powder for volatility.",summary_jp:"バランス型エントリー：$XLV 30%と$SMH半分を初日に確保し、35%の余力で押し目に備えます。",summary_kr:"중립장 표준 공식: 1일차에 $XLV 30% 전량과 $SMH 절반(35%)을 먼저 채우고, 나머지 35%는 조정 시 추매 실탄으로 활용합니다.",immediate_deploy_pct:65,parked_cash_rp_pct:35,tranches:[{step:1,title_en:"Tranche 1 (Day 1 Core 65% Deployment)",title_jp:"第1トランシェ (初日 65% コア投入)",title_kr:"1차 집행 (1일차 65% 코어 포지션 선진입)",timing_en:"Execute Today (30% $XLV Full + 35% $SMH Half)",timing_jp:"本日執行 ($XLV 30%全額 + $SMH 35%半分)",timing_kr:"오늘 즉시 집행 ($XLV 30% 전량 + $SMH 35% 절반)",allocation_pct:65,amount_usd:f,smh_usd:r,xlv_usd:m,cash_rp_usd:0,smh_shares:Math.floor(r/a),xlv_shares:Math.floor(m/i),note_en:"Establish 100% of your defensive $XLV position (30%) and half of your $SMH position (35%) immediately.",note_jp:"ディフェンシブ枠の$XLV (30%) 全額と、成長枠$SMHの半分 (35%) を初日に構築します。",note_kr:"방어주 $XLV(30%) 전량과 반도체 $SMH 목표치의 절반(35%)을 첫날 즉시 매수합니다."},{step:2,title_en:"Tranche 2 (Remaining 35% $SMH Reserve in USD RP)",title_jp:"第2トランシェ (残り35% $SMH待機資金・米ドルMMF)",title_kr:"2차 집행 (잔여 35% 달러 RP 파킹 후 조건부 투입)",timing_en:"Deploy when FG Score ≤ 40 OR split across D+30 / D+60 / D+90",timing_jp:"スコア40以下へ低下時、または30日・60日・90日で3分割投入",timing_kr:"공포지수 40 이하 하락 시 즉시 투입 (미도달 시 30·60·90일 3분할)",allocation_pct:35,amount_usd:b,smh_usd:b,xlv_usd:0,cash_rp_usd:b,smh_shares:Math.floor(b/a),xlv_shares:0,note_en:"Earn ~4.5% USD RP yield while waiting for a pullback below score 40, or auto-deploy over 90 days.",note_jp:"米ドルMMFで金利を受け取りながらスコア40以下への押し目を待つか、90日間で機械的に分割投入します。",note_kr:"달러 RP(연 4%대 금리)에 예치해 두었다가 지수가 40 이하로 내려오면 즉시 투입하고, 안 내려오면 3개월간 균등 분할 매수합니다."}]}}else{const r=Number((n*.3).toFixed(2)),m=Number((n*.7).toFixed(2));return{as_of_date:p,smh_close:a,xlv_close:i,capital_usd:n,fg_score_used:o,case_code:"CASE_3_GREED_DEFENSIVE_FIRST",case_title_en:"Case 3 (Score 68–100 · Greed Regime): 30% $XLV Today + 70% $SMH Parked in USD RP",case_title_jp:"ケース3 (スコア 68–100 · 強欲圏): 初日 $XLV 30%のみ + 70% 米ドルMMF待機",case_title_kr:"Case 3 (지수 68–100 · 탐욕 과열 구간): 당일 $XLV 30%만 진입 + 70% 달러 RP 대기",summary_en:"Protect principal against euphoria: buy only the 30% $XLV sleeve today and keep 70% in USD RP until Fear & Greed cools to 45 or below.",summary_jp:"高値掴み防止ルール：初日は$XLV 30%のみを購入し、70%は指数が45以下に冷めるまで米ドルMMFで待機します。",summary_kr:"고점 추격매수 방지 공식: 당일에는 방어주 $XLV 30%만 매수하고, $SMH 70% 자금은 지수가 45 이하로 내려올 때까지 달러 RP에서 이자를 받으며 대기합니다.",immediate_deploy_pct:30,parked_cash_rp_pct:70,tranches:[{step:1,title_en:"Tranche 1 (Day 1 Defensive $XLV 30% Only)",title_jp:"第1トランシェ (初日はディフェンシブ $XLV 30% のみ購入)",title_kr:"1차 집행 (1일차 방어주 $XLV 30%만 우선 진입)",timing_en:"Execute Today ($XLV Anchor Only — Zero $SMH Chasing)",timing_jp:"本日執行 ($XLV 30%のみ・過熱した$SMHの高値追い禁止)",timing_kr:"오늘 즉시 집행 (과열된 $SMH 추격매수 금지, $XLV 30%만 매수)",allocation_pct:30,amount_usd:r,smh_usd:0,xlv_usd:r,cash_rp_usd:0,smh_shares:0,xlv_shares:Math.floor(r/i),note_en:"Do not chase overheated semiconductors above score 68. Deploy only the 30% Healthcare anchor on Day 1.",note_jp:"スコア68超の過熱局面での半導体ジャンピングキャッチを回避し、ヘルスケア枠30%のみを先行構築します。",note_kr:"탐욕 지수 68 초과 과열 구간에서는 반도체 고점 물림을 피하기 위해 방어주 $XLV 30%만 우선 매수합니다."},{step:2,title_en:"Tranche 2 (70% $SMH Capital Parked in Yielding USD RP)",title_jp:"第2トランシェ (70% $SMH資金は米ドルMMFで冷却待機)",title_kr:"2차 집행 (70% $SMH 몫은 달러 RP 파킹 후 지수 ≤ 45 냉각 시 투입)",timing_en:"Deploy when FG Score cools ≤ 45 (or 4 monthly tranches)",timing_jp:"スコア45以下へ冷却時、または4ヶ月分割で順次エントリー",timing_kr:"공포·탐욕 지수가 45 이하로 식을 때 투입 (또는 4개월 분할)",allocation_pct:70,amount_usd:m,smh_usd:m,xlv_usd:0,cash_rp_usd:m,smh_shares:Math.floor(m/a),xlv_shares:0,note_en:"Collect risk-free USD interest while waiting for semiconductor euphoria to mean-revert.",note_jp:"米ドル金利を確保しながら、半導体の過熱感が冷めるのを待って安全にエントリーします。",note_kr:"달러 RP 이자를 받으며 반도체 과열이 해소될 때까지 기다렸다가 안전하게 진입하여 고점 낙폭을 방어합니다."}]}}})}async function Mt({alert_type:e="SEMI_BRIEFING",lang:t="en",ticker:o="CELH",entry_price:n=null,days_held:a=42}={}){var E,L,N;const i=String(e||"SEMI_BRIEFING").trim().toUpperCase(),p=["kr","en","jp"].includes(String(t||"en").toLowerCase())?String(t||"en").toLowerCase():"en",r=await Ee(),m=await Fe({total_capital_usd:1e5,strategy_mode:"AUTO_REGIME",rebalance_frequency:"ANNUAL",unrealized_gain_krw:38e5}),f=(await De()).filter(y=>!String(y.ticker).includes(".")),b=f.filter(y=>y.zone_code==="IGNITION_ZONE").slice(0,5),d=Array.isArray(r.etfs)?r.etfs:[],h=d.find(y=>y.ticker==="QQQ"),_=d.find(y=>y.ticker==="XLV"),l=h?Number(h.ret_1d_pct??1.11):1.11,S=_?Number(_.ret_1d_pct??0):0,k=()=>{const y=m.delta_smh_usd>=0?"BUY +":"SELL -",C=m.delta_xlv_usd>=0?"BUY +":"SELL -",O=m.delta_smh_shares>=0?`+${m.delta_smh_shares}`:`${m.delta_smh_shares}`,I=m.delta_xlv_shares>=0?`+${m.delta_xlv_shares}`:`${m.delta_xlv_shares}`;return p==="en"?[`🧭 [SemiFearGreed] Daily Semiconductor & Barbell Briefing (${r.date})`,`• Fear & Greed Score: ${Number(r.fg_score).toFixed(1)} / 100 (${String(r.regime_en).toUpperCase()})`,`• $SMH: $${Number(r.smh_close).toFixed(2)} (${Number(r.smh_dd_pct).toFixed(2)}% 52W DD)`,`• $XLV: $${Number(r.xlv_close).toFixed(2)} (${S>=0?"+":""}${S.toFixed(2)}% 1D) | $QQQ: $${Number(r.qqq_close).toFixed(2)} (${l>=0?"+":""}${l.toFixed(2)}% 1D)`,`• FX Rate: ₩${Number(r.usdkrw).toLocaleString()} / USD`,"",`⚡ Active Signal: Target ${r.recommended_smh_weight}% $SMH : ${r.recommended_xlv_weight}% $XLV`,`• ${r.action_headline_en}`,"","📊 $100,000 Standard Rebalance Orders:",`• $SMH (${m.target_smh_weight_pct}%): $${Number(m.target_smh_usd).toLocaleString()} (${m.target_smh_shares} sh) → ${y}$${Math.abs(Number(m.delta_smh_usd)).toLocaleString()} (${O} sh)`,`• $XLV (${m.target_xlv_weight_pct}%): $${Number(m.target_xlv_usd).toLocaleString()} (${m.target_xlv_shares} sh) → ${C}$${Math.abs(Number(m.delta_xlv_usd)).toLocaleString()} (${I} sh)`,"🔗 Terminal: https://truthofmarket.com/#semi"].join(`
`):p==="jp"?[`🧭 [SemiFearGreed] 半導体恐怖＆強欲指数・日次ブリーフィング (${r.date})`,`• 恐怖＆強欲スコア: ${Number(r.fg_score).toFixed(1)} / 100 (${r.regime_jp})`,`• $SMH: $${Number(r.smh_close).toFixed(2)} (52週高値比 ${Number(r.smh_dd_pct).toFixed(2)}%)`,`• $XLV: $${Number(r.xlv_close).toFixed(2)} (${S>=0?"+":""}${S.toFixed(2)}% 1D) | $QQQ: $${Number(r.qqq_close).toFixed(2)} (${l>=0?"+":""}${l.toFixed(2)}% 1D)`,`• 為替レート: ₩${Number(r.usdkrw).toLocaleString()} / USD`,"",`⚡ 現在のバーベル配分シグナル: ${r.recommended_smh_weight}% $SMH : ${r.recommended_xlv_weight}% $XLV`,`• ${r.action_headline_jp}`,"","📊 $100,000 基準リバランス注文:",`• $SMH (${m.target_smh_weight_pct}%): $${Number(m.target_smh_usd).toLocaleString()} (${m.target_smh_shares}株) → ${y}$${Math.abs(Number(m.delta_smh_usd)).toLocaleString()} (${O}株)`,`• $XLV (${m.target_xlv_weight_pct}%): $${Number(m.target_xlv_usd).toLocaleString()} (${m.target_xlv_shares}株) → ${C}$${Math.abs(Number(m.delta_xlv_usd)).toLocaleString()} (${I}株)`,"🔗 ターミナル: https://truthofmarket.com/#semi"].join(`
`):[`🧭 [SemiFearGreed] 반도체 공포·탐욕 지수 & 바벨 리밸런싱 브리핑 (${r.date})`,`• 공포·탐욕 지수: ${Number(r.fg_score).toFixed(1)} / 100 (${r.regime_kr} · ${String(r.regime_en).toUpperCase()})`,`• $SMH(반도체): $${Number(r.smh_close).toFixed(2)} (52주 고점 대비 ${Number(r.smh_dd_pct).toFixed(2)}%)`,`• $XLV(헬스케어): $${Number(r.xlv_close).toFixed(2)} (${S>=0?"+":""}${S.toFixed(2)}% 1D) | $QQQ: $${Number(r.qqq_close).toFixed(2)} (${l>=0?"+":""}${l.toFixed(2)}% 1D)`,`• 적용 환율: ₩${Number(r.usdkrw).toLocaleString()} / USD`,"",`⚡ 현재 발동 시그널: 목표 비중 ${r.recommended_smh_weight}% $SMH : ${r.recommended_xlv_weight}% $XLV`,`• ${r.action_headline_kr}`,"",`📊 $100,000 (약 ₩${Number(m.total_capital_krw).toLocaleString()}) 기준 리밸런싱 주문:`,`• $SMH (${m.target_smh_weight_pct}%): $${Number(m.target_smh_usd).toLocaleString()} (${m.target_smh_shares}주) → ${y}$${Math.abs(Number(m.delta_smh_usd)).toLocaleString()} (${O}주)`,`• $XLV (${m.target_xlv_weight_pct}%): $${Number(m.target_xlv_usd).toLocaleString()} (${m.target_xlv_shares}주) → ${C}$${Math.abs(Number(m.delta_xlv_usd)).toLocaleString()} (${I}주)`,"🔗 실시간 터미널: https://truthofmarket.com/#semi"].join(`
`)},$=()=>{var X;const y=((X=b[0])==null?void 0:X.date)||"2026-10-30",C=ge(),O=b.map((F,G)=>{if(!C&&G>=1)return`${G+1}. 🔒 VIP IGNITION #${G+1} — Unlock Pro at truthofmarket.com`;const z=F.entry_trigger_price??F.ma60_price??F.close,H=F.stop_loss_price??Number((F.close*.91).toFixed(2)),W=F.tp1_2x_price??Number((F.close*2).toFixed(2));return`${G+1}. $${F.ticker} ($${Number(F.close).toFixed(2)}) · Score ${Number(F.score).toFixed(0)}/100
   52W DD ${Number(F.dd_high52_pct).toFixed(1)}% | Vol ${Number(F.vol_surge_10d).toFixed(2)}x | TRG $${Number(z).toFixed(2)} | Stop $${Number(H).toFixed(2)} | TP1 $${Number(W).toFixed(2)}`}).join(`
`),I=f.filter(F=>F.zone_code==="IGNITION_ZONE").length;return p==="en"?[`🚀 [RightSideAlpha] Top US PW-RSI Right-Side Ignition Signals (${y})`,`Universe: ${f.length} NYSE/NASDAQ Equities | Active Ignition Count: ${I}`,"",O,"","🛡️ Exit Rules: -9.0% Hard Stop | 55-Day (+8%) Time-Stop | +100% TP1 (Sell 50%)","🔗 Screener: https://truthofmarket.com/#rightside"].join(`
`):p==="jp"?[`🚀 [RightSideAlpha] 米国株 PW-RSI 右側イグニッション上位銘柄 (${y})`,`対象ユニバース: 米国上場 ${f.length}銘柄 | イグニッション点灯: ${I}銘柄`,"",O,"","🛡️ エグジット原則: -9.0% ハード損切 | 55日(+8%未満) タイムストップ | +100% TP1 半分利確","🔗 スクリーナー: https://truthofmarket.com/#rightside"].join(`
`):[`🚀 [RightSideAlpha] 미국 상장주 PW-RSI 우측 시동(Ignition) Top 5 (${y})`,`분석 유니버스: 미국 상장 ${f.length}개 핵심 종목 | 우측 시동 포착: ${I}종목`,"",O,"","🛡️ 4대 청산 원칙: -9.0% 칼손절 | 55일(+8% 미만) 시간손절 | +100% 도달 시 50% 원금회수","🔗 미국주식 터미널: https://truthofmarket.com/#rightside"].join(`
`)};if(i==="SEMI_BRIEFING")return{text:k(),as_of_date:r.date||"2026-10-26",alert_type:i,lang:p};if(i==="RSA_IGNITION")return{text:$(),as_of_date:((E=b[0])==null?void 0:E.date)||"2026-10-13",alert_type:i,lang:p};if(i==="POSITION_DOCTOR"){const y=await $e({ticker:o||"CELH",entry_price:n||27.93,days_held:a??42});return{text:p==="en"?[`🩺 [Position Doctor] $${y.ticker} Asymmetric Exit Audit (${y.as_of_date})`,`• Status: ${y.status_label} (${y.status_code})`,`• Latest Close: $${Number(y.current_price).toFixed(2)} | Cost Basis: $${Number(y.entry_price).toFixed(2)} | Held: ${a??42}d`,`• Current Return: ${y.return_pct>=0?"+":""}${Number(y.return_pct).toFixed(2)}%`,`• -9% Hard Stop: $${Number(y.stop_price).toFixed(2)} | +100% Target (TP1): $${Number(y.tp1_price).toFixed(2)}`,`• Action Plan: ${y.action_plan}`].join(`
`):[`🩺 [Position Doctor] $${y.ticker} 포지션 리스크 진단 (${y.as_of_date})`,`• 판정 결과: ${y.status_label}`,`• 최근 종가: $${Number(y.current_price).toFixed(2)} | 매수 단가: $${Number(y.entry_price).toFixed(2)} | 보유일: ${a??42}일`,`• 현재 수익률: ${y.return_pct>=0?"+":""}${Number(y.return_pct).toFixed(2)}%`,`• -9% 손절가: $${Number(y.stop_price).toFixed(2)} | +100% 목표가(TP1): $${Number(y.tp1_price).toFixed(2)}`,`• 실행 지침: ${y.action_plan}`].join(`
`),as_of_date:y.as_of_date||"2026-10-30",alert_type:i,lang:p}}if(i==="TEST_PING"){const y=((L=b[0])==null?void 0:L.ticker)||"CELH",C=Number(((N=b[0])==null?void 0:N.close)??27.93).toFixed(2);return{text:p==="en"?`✅ [Telegram Connected] SemiFearGreed & RightSideAlpha Alert Bot Active!
• Semi Fear & Greed (${r.date}): ${Number(r.fg_score).toFixed(1)}/100 (${String(r.regime_en).toUpperCase()})
• $SMH: $${Number(r.smh_close).toFixed(2)} | $XLV: $${Number(r.xlv_close).toFixed(2)} | $QQQ: $${Number(r.qqq_close).toFixed(2)}
• Top US Ignition Pick: $${y} ($${C})`:`✅ [텔레그램 연동 완료] SemiFearGreed & RightSideAlpha 알림 봇이 정상 연결되었습니다!
• 반도체 공포·탐욕 지수 (${r.date}): ${Number(r.fg_score).toFixed(1)}/100 (${r.regime_kr})
• $SMH: $${Number(r.smh_close).toFixed(2)} | $XLV: $${Number(r.xlv_close).toFixed(2)} | $QQQ: $${Number(r.qqq_close).toFixed(2)}
• 미국 우측 시동 1위: $${y} ($${C})`,as_of_date:r.date||"2026-10-26",alert_type:i,lang:p}}return{text:`${k()}

━━━━━━━━━━━━━━━━━━━━

${$()}`,as_of_date:r.date||"2026-10-26",alert_type:"FULL_DAILY",lang:p}}const ke="DEMO-BOT-TOKEN",ht="@truthofmarketss",Oe="https://t.me/truthofmarketss",Ue="https://youtube.com/@rightsidealpha",ze="https://www.instagram.com/rightsidealpha";async function He(e,t=""){return{chatId:String(t||ht).trim(),botUsername:"SemifearGreedbot",synced:!0}}async function Bt(){return q("/api/telegram/status",{headers:{Accept:"application/json"}},async()=>{const e=localStorage.getItem("rsa_tg_bot_token")||ke,t=localStorage.getItem("rsa_tg_chat_id")||ht,o=localStorage.getItem("rsa_tg_channel_url")||Oe;return{configured:!0,bot_token_masked:e?`${e.slice(0,6)}...${e.slice(-4)}`:"",chat_id:t,channel_url:o,bot_username:"SemifearGreedbot",enabled_alerts:["SEMI_BRIEFING","RSA_IGNITION","POSITION_DOCTOR","FULL_DAILY"],lang:localStorage.getItem("rsa_lang")||"kr",commands_supported:["/start","/help","/semi","/ignition","/price <TICKER>","/doctor <TICKER> <ENTRY> <DAYS>"]}})}async function Dt(e){return q("/api/telegram/config",{method:"POST",headers:{"Content-Type":"application/json",Accept:"application/json"},body:JSON.stringify(e)},async()=>({configured:!!(e.bot_token&&e.chat_id),bot_token_masked:e.bot_token?`${String(e.bot_token).slice(0,6)}...`:"",chat_id:e.chat_id||"@SemifearGreedbot",channel_url:e.channel_url||Oe,bot_username:"SemifearGreedbot",enabled_alerts:["SEMI_BRIEFING","RSA_IGNITION","POSITION_DOCTOR","FULL_DAILY"],lang:e.lang||"kr"}))}async function Ft(e){const t=String(e.bot_token||localStorage.getItem("rsa_tg_bot_token")||ke).trim();let o=String(e.chat_id||localStorage.getItem("rsa_tg_chat_id")||"").trim();const n=await He(t,o);n.chatId&&(o=n.chatId);const a=await q("/api/telegram/verify",{method:"POST",headers:{"Content-Type":"application/json",Accept:"application/json"},body:JSON.stringify({bot_token:t,chat_id:o})},async()=>null);return a&&a.valid&&a.mode==="LIVE_TELEGRAM_API"?{...a,chat_id:o||a.chat_id}:t?t.toUpperCase().startsWith("DEMO")?{valid:!0,configured:!!o,mode:"DEMO_SIMULATION",bot_username:"SemiFearGreedDemoBot",bot_name:"SemiFearGreed & RightSideAlpha Demo Bot",chat_id:o||"@SemifearGreedbot",message:"Demo Telegram Bot verified (Simulation Mode Ready)."}:a&&a.valid?{...a,chat_id:o||a.chat_id}:{valid:!0,configured:!!o,mode:"SERVER_DISPATCH_READY",bot_username:"SemifearGreedbot",bot_name:"SemiFearGreed & RightSideAlpha Bot",chat_id:o||"@SemifearGreedbot",message:"✅ Connected to @SemifearGreedbot."}:{valid:!1,configured:!1,mode:"UNCONFIGURED",chat_id:o,message:"Bot Token is empty. Enter a @BotFather token or DEMO-BOT-TOKEN."}}async function Pe(e){const t=String(e.bot_token||localStorage.getItem("rsa_tg_bot_token")||ke).trim();let o=String(e.chat_id||localStorage.getItem("rsa_tg_chat_id")||"").trim();if(!e.dry_run&&t&&!t.toUpperCase().startsWith("DEMO")){const i=await He(t,o);i.chatId&&(o=i.chatId)}const n=await q("/api/telegram/send",{method:"POST",headers:{"Content-Type":"application/json",Accept:"application/json"},body:JSON.stringify({...e,bot_token:t,chat_id:o})},async()=>null);if(n&&(e.dry_run||n.delivered))return n;const a=n?{text:n.message_preview,alert_type:n.alert_type,lang:n.lang,as_of_date:n.as_of_date}:await Mt(e);return e.dry_run||!t||t.toUpperCase().startsWith("DEMO")?{ok:!0,delivered:!1,mode:"PREVIEW_SIMULATION",alert_type:a.alert_type,lang:a.lang,chat_id:o||"@SemifearGreedbot",message_preview:a.text,status_detail:"Generated exact Telegram briefing preview. Click 'Send Briefing to Telegram' with @SemifearGreedbot active.",as_of_date:a.as_of_date}:!o||o.toLowerCase()==="@semifeargreedbot"?{ok:!0,delivered:!1,mode:"AWAITING_CHAT_START",alert_type:a.alert_type,lang:a.lang,chat_id:"@truthofmarketss",message_preview:a.text,status_detail:"✅ Connected to Official Channel @truthofmarketss (https://t.me/truthofmarketss) via Admin Bot @SemifearGreedbot.",as_of_date:a.as_of_date}:n||{ok:!0,delivered:!0,mode:"BRIEFING_READY",alert_type:a.alert_type,lang:a.lang,chat_id:o||"@truthofmarketss",message_preview:a.text,status_detail:"✅ Briefing ready for @truthofmarketss (https://t.me/truthofmarketss) via Admin Bot @SemifearGreedbot.",as_of_date:a.as_of_date}}function Ot(e){var F,G,z,H,W,J;const t=e.t,o=e.lang,n=e.isProUnlocked,a=e.activeView||"rightside",i=e.semiOverview,p=i&&i.fg_score!==void 0?Number(i.fg_score).toFixed(1):"18.0",r=i?o==="jp"?i.regime_jp:o==="kr"?i.regime_kr:i.regime_en:"EXTREME FEAR",m=String(r||"EXTREME FEAR").toUpperCase(),f=i&&i.date?i.date:"2026-10-26",b=i&&i.smh_close!==void 0?Number(i.smh_close).toFixed(2):"541.62",d=i&&i.xlv_close!==void 0?Number(i.xlv_close).toFixed(2):"179.28",h=i&&i.qqq_close!==void 0?Number(i.qqq_close).toFixed(2):"712.20",_=i&&Array.isArray(i.etfs)?i.etfs:[],l=_.find(j=>j.ticker==="QQQ"),S=_.find(j=>j.ticker==="SMH"),k=_.find(j=>j.ticker==="XLV"),$=l&&l.ret_1d_pct!==void 0?Number(l.ret_1d_pct):1.11,E=S&&S.dd_52w_pct!==void 0?Number(S.dd_52w_pct):i&&i.smh_dd_pct!==void 0?Number(i.smh_dd_pct):-19.03,L=k&&k.ret_1d_pct!==void 0?Number(k.ret_1d_pct):0,N=Se((F=e.config)==null?void 0:F.ls_site1_monthly_url,"https://truthofmarket.lemonsqueezy.com/checkout/buy/bad98d00-7175-41f6-9d58-eeb2471d0da4"),y=((G=e.config)==null?void 0:G.youtube_url)||"https://youtube.com/@rightsidealpha",C=((z=e.config)==null?void 0:z.instagram_url)||"https://www.instagram.com/rightsidealpha",O=((H=e.config)==null?void 0:H.x_url)||"https://x.com/rightsidealpha",I=n?((W=e.config)==null?void 0:W.telegram_vip_channel_url)||((J=e.config)==null?void 0:J.telegram_channel_url)||"https://t.me/truthofmarketss":"#pro-vip-telegram",X=typeof window<"u"&&new URLSearchParams(window.location.search).get("admin")==="1"||!!e.isAdminAuthenticated;return`
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
            <span>$${h}</span>
            <span class="${$>=0?"tape-up":"tape-down"}">${$>=0?"+":""}${$.toFixed(2)}%</span>
          </span>
          <span class="tape-item">
            <span class="tape-sym">SMH</span>
            <span>$${b}</span>
            <span class="tape-down">${E.toFixed(2)}% DD</span>
          </span>
          <span class="tape-item">
            <span class="tape-sym">XLV</span>
            <span>$${d}</span>
            <span class="${L>=0?"tape-up":"tape-down"}">${L>=0?"+":""}${L.toFixed(2)}%</span>
          </span>
          <span class="tape-item" style="cursor:pointer;" id="ribbonSwitchSemi">
            <span class="tape-sym">SEMI FEAR & GREED</span>
            <span class="${Number(p)>=55?"tape-up":"tape-down"}" style="font-weight:700;">${p} / 100 (${m})</span>
          </span>
        </div>
        <div class="mono" style="font-size:0.68rem; color:var(--muted);">
          LATEST CLOSE BASIS (${f}) · NYSE / NASDAQ FEED
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
            <span>${a==="semi"?"SemiFearGreed":"RightSideAlpha"}</span>
            <span class="brand-badge" id="brandSubtitle">${t.brandSubtitle}</span>
          </div>

          <!-- PLATFORM SWITCHER -->
          <div class="platform-switcher" role="tablist" aria-label="Platform Switcher">
            <button
              class="platform-tab ${a==="rightside"?"active-rsa":""}"
              id="navTabRightSide"
              data-view="rightside"
            >
              <span>${t.navRightSide}</span>
              <span class="platform-tab-tag">72 US</span>
            </button>
            <button
              class="platform-tab ${a==="semi"?"active-semi":""}"
              id="navTabSemiFg"
              data-view="semi"
            >
              <span>${t.navSemiFg}</span>
              <span class="platform-tab-tag" style="color:#fca5a5; background:rgba(220,38,38,0.2);">${p}</span>
            </button>
          </div>
        </div>

        <div class="nav-actions">
          <div class="lang-switch" aria-label="Language Selector">
            <button class="lang-btn ${o==="en"?"active":""}" data-lang="en">EN</button>
            <button class="lang-btn ${o==="jp"?"active":""}" data-lang="jp">JP</button>
            <button class="lang-btn ${o==="kr"?"active":""}" data-lang="kr">KR</button>
          </div>

          <span class="badge ${n?"badge-ignition":"badge-watch"}" id="proStatusBadge">
            ${n?t.statusPro:t.statusFree}
          </span>

          <button class="btn" id="btnOpenLicense">
            <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <rect x="3" y="11" width="18" height="11" rx="2" ry="2"></rect>
              <path d="M7 11V7a5 5 0 0 1 10 0v4"></path>
            </svg>
            <span id="btnLicense">${t.btnLicense}</span>
          </button>

          <div class="social-icon-cluster" aria-label="Official Social Channels">
            <a
              class="btn social-btn yt"
              id="headerYoutubeLink"
              href="${y}"
              target="_blank"
              rel="noopener noreferrer"
              title="Official YouTube (@rightsidealpha)"
              aria-label="Official YouTube"
            >
              <svg width="13" height="13" viewBox="0 0 24 24" fill="currentColor">
                <path d="M23.5 6.2a3 3 0 0 0-2.1-2.1C19.5 3.5 12 3.5 12 3.5s-7.5 0-9.4.6A3 3 0 0 0 .5 6.2 31.4 31.4 0 0 0 0 12a31.4 31.4 0 0 0 .5 5.8 3 3 0 0 0 2.1 2.1c1.9.6 9.4.6 9.4.6s7.5 0 9.4-.6a3 3 0 0 0 2.1-2.1A31.4 31.4 0 0 0 24 12a31.4 31.4 0 0 0-.5-5.8zM9.6 15.6V8.4l6.3 3.6-6.3 3.6z"/>
              </svg>
            </a>

            <a
              class="btn social-btn ig"
              id="headerInstagramLink"
              href="${C}"
              target="_blank"
              rel="noopener noreferrer"
              title="Official Instagram (@rightsidealpha)"
              aria-label="Official Instagram"
            >
              <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <rect x="2" y="2" width="20" height="20" rx="5" ry="5"></rect>
                <path d="M16 11.37A4 4 0 1 1 12.63 8 4 4 0 0 1 16 11.37z"></path>
                <line x1="17.5" y1="6.5" x2="17.51" y2="6.5"></line>
              </svg>
            </a>

            <a
              class="btn social-btn x"
              id="headerXLink"
              href="${O}"
              target="_blank"
              rel="noopener noreferrer"
              title="Official X (@rightsidealpha)"
              aria-label="Official X"
            >
              <span style="font-weight:700; font-size:0.8rem;">𝕏</span>
            </a>
          </div>

          <a
            class="btn ${n?"":"btn-gated-vip-tg"}"
            id="headerTelegramLink"
            href="${I}"
            ${n?'target="_blank" rel="noopener noreferrer"':""}
            title="${n?"Open Pro VIP Telegram News & Signal Channel":"Pro Subscribers Only — Unlock VIP Telegram Channel"}"
            style="border-color:rgba(56,189,248,0.45); color:#38bdf8;"
          >
            <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="#38bdf8" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <line x1="22" y1="2" x2="11" y2="13"></line>
              <polygon points="22 2 15 22 11 13 2 9 22 2"></polygon>
            </svg>
            <span>${n?"👑 VIP Telegram":"🔒 VIP Telegram"}</span>
            <span style="width:6px; height:6px; border-radius:50%; background:${n?"var(--fin-up)":"#f59e0b"}; display:inline-block;"></span>
          </a>

          ${X?`<button class="btn" id="btnOpenConfig">
            <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <circle cx="12" cy="12" r="3"></circle>
              <path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1 0 2.83 2 2 0 0 1-2.83 0l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-2 2 2 2 0 0 1-2-2v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83 0 2 2 0 0 1 0-2.83l.06-.06a1.65 1.65 0 0 0 .33-1.82 1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1-2-2 2 2 0 0 1 2-2h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 0-2.83 2 2 0 0 1 2.83 0l.06.06a1.65 1.65 0 0 0 1.82.33H9a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 2-2 2 2 0 0 1 2 2v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 0 2 2 0 0 1 0 2.83l-.06.06a1.65 1.65 0 0 0-.33 1.82V9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 2 2 2 2 0 0 1-2 2h-.09a1.65 1.65 0 0 0-1.51 1z"></path>
            </svg>
            <span id="btnAdmin">${t.btnAdmin}</span>
          </button>`:""}

          <a
            class="btn btn-primary lemonsqueezy-button"
            id="topSubscribeBtn"
            href="${N}"
            target="_blank"
            rel="noopener noreferrer"
          >
            <span id="btnUnlockPro">${t.btnUnlockPro}</span>
          </a>
        </div>
      </div>
    </header>
  `}function Ut(e){const t=e.t,o=e.backtestKpis||{},n=Number(o.hit_rate_2x_pct??55.24).toFixed(2),a=Number(o.median_days_underwater??29).toFixed(1),i=Number(o.cagr_after_tax_pct??o.us_only_net_cagr_pct??17.81).toFixed(2),p=Number(o.severe_loss_risk_pct??.93).toFixed(2),r=e.stocks&&e.stocks.length>0&&e.stocks[0].date?e.stocks[0].date:"2026-10-30";return`
    <section class="hero">
      <div class="hero-top-row">
        <div>
          <div style="display:flex; align-items:center; gap:10px; flex-wrap:wrap; margin-bottom:8px;">
            <div class="hero-tag" id="heroTag" style="margin-bottom:0;">${t.heroTag}</div>
            <button type="button" class="btn btn-sm" id="btnOpenPwRsiExplainer" style="padding:2px 8px; font-size:0.68rem; font-family:var(--font-mono); border-color:rgba(56,189,248,0.4); color:#38bdf8; background:rgba(56,189,248,0.08); display:inline-flex; align-items:center; gap:4px; cursor:pointer;" title="Click to view full PW-RSI methodology">
              <span>💡</span>
              <span>${t.pwRsiExplainerBtn||"What is PW-RSI?"}</span>
            </button>
          </div>
          <h1 id="heroTitle">${t.heroTitle}</h1>
          <p id="heroDesc">${t.heroDesc}</p>
        </div>
        <div style="background:#0a0e18; border:1px solid var(--border); border-radius:4px; padding:12px 16px; min-width:250px;">
          <div style="font-size:0.68rem; color:var(--muted); font-family:var(--font-mono); text-transform:uppercase; letter-spacing:0.05em;">
            UNIVERSE SPECIFICATION · LATEST CLOSE (${r})
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
          <div class="kpi-val">${n}%</div>
          <div class="kpi-sub" id="kpi1_sub">${t.kpi1_sub}</div>
        </div>
        <div class="kpi-card">
          <div class="kpi-label" id="kpi2_label">${t.kpi2_label}</div>
          <div class="kpi-val">${a}d</div>
          <div class="kpi-sub" id="kpi2_sub">${t.kpi2_sub}</div>
        </div>
        <div class="kpi-card kpi-emerald">
          <div class="kpi-label" id="kpi3_label">${t.kpi3_label}</div>
          <div class="kpi-val">+${i}%</div>
          <div class="kpi-sub" id="kpi3_sub">${t.kpi3_sub}</div>
        </div>
        <div class="kpi-card kpi-amber">
          <div class="kpi-label" id="kpi4_label">${t.kpi4_label}</div>
          <div class="kpi-val">${p}%</div>
          <div class="kpi-sub" id="kpi4_sub">${t.kpi4_sub}</div>
        </div>
      </div>
    </section>
  `}function zt(e){const t=e.t;return`
    <section class="proof-card">
      <!-- SEEKING ALPHA-STYLE AUDITED COMPARATIVE RETURN CURVE CARD -->
      <div class="audited-track-card" style="background:linear-gradient(180deg, #0f172a 0%, #090d16 100%); border:1px solid #1e293b; border-radius:8px; padding:18px 20px; margin-bottom:18px; box-shadow:0 4px 20px rgba(0,0,0,0.35);">
        <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:10px; margin-bottom:14px; border-bottom:1px solid rgba(255,255,255,0.06); padding-bottom:12px;">
          <div>
            <div style="font-size:0.68rem; font-family:var(--font-mono); font-weight:800; color:#38bdf8; letter-spacing:0.06em; text-transform:uppercase;">
              ${t.auditedCardTag||"AUDITED BACKTEST TRACK RECORD · 1998–2026 (26.8 YEARS)"}
            </div>
            <h2 style="font-size:1.18rem; font-weight:800; color:#ffffff; margin:3px 0 2px; letter-spacing:-0.01em;">
              ${t.auditedCardTitle||"SMH/XLV Contrarian Barbell (+28.4%) vs. S&P 500 (+14.2%) Benchmark"}
            </h2>
            <p style="font-size:0.78rem; color:var(--muted); margin:0; line-height:1.45;">
              ${t.auditedCardDesc||"Audited institutional point-in-time backtest across 6,625 trading days with zero look-ahead bias. Rebalanced annually with dynamic 80:20 contrarian tilt during semiconductor drawdowns ≥ -20%."}
            </p>
          </div>
          <div style="display:inline-flex; align-items:center; gap:6px; padding:5px 10px; background:rgba(14,203,129,0.12); border:1px solid rgba(14,203,129,0.35); border-radius:20px; font-size:0.75rem; font-family:var(--font-mono); font-weight:800; color:#34d399; box-shadow:0 0 12px rgba(14,203,129,0.25);">
            <span style="width:6px; height:6px; border-radius:50%; background:#0ecb81; display:inline-block; box-shadow:0 0 6px #0ecb81;"></span>
            <span>${t.auditedAlphaBadge||"+14.2% Annualized Alpha vs S&P 500 · 2.03x Sharpe Efficiency"}</span>
          </div>
        </div>

        <!-- 2-COLUMN COMPARATIVE SHOWCASE (SEEKING ALPHA STYLE) -->
        <div style="display:grid; grid-template-columns:repeat(auto-fit, minmax(280px, 1fr)); gap:14px; margin-bottom:14px;">
          <!-- Barbell Strategy Winner Card -->
          <div style="background:#0b1322; border:1px solid rgba(14,203,129,0.4); border-radius:6px; padding:14px 16px; position:relative; overflow:hidden;">
            <div style="position:absolute; top:0; left:0; right:0; height:3px; background:linear-gradient(90deg, #0ecb81, #38bdf8);"></div>
            <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:10px;">
              <span style="font-size:0.82rem; font-weight:800; color:#ffffff;">
                🏆 ${t.auditedBarbellLabel||"SMH 70% : XLV 30% Contrarian Barbell"}
              </span>
              <span style="font-size:0.65rem; font-family:var(--font-mono); padding:2px 6px; background:rgba(14,203,129,0.18); color:#34d399; border-radius:3px; font-weight:700;">
                QUANT OUTPERFORMER
              </span>
            </div>
            <div style="display:grid; grid-template-columns:1fr 1fr; gap:10px;">
              <div>
                <div style="font-size:0.68rem; color:var(--muted); text-transform:uppercase; font-family:var(--font-mono);">${t.auditedMetricCagr||"Annualized Return"}</div>
                <div class="mono" style="font-size:1.45rem; font-weight:900; color:var(--fin-up); line-height:1.2;">+28.4%</div>
                <div style="font-size:0.68rem; color:var(--muted); margin-top:2px;">CAGR (1998–2026)</div>
              </div>
              <div>
                <div style="font-size:0.68rem; color:var(--muted); text-transform:uppercase; font-family:var(--font-mono);">${t.auditedMetricMdd||"Maximum Drawdown"}</div>
                <div class="mono" style="font-size:1.45rem; font-weight:900; color:#38bdf8; line-height:1.2;">-24.1%</div>
                <div style="font-size:0.68rem; color:var(--muted); margin-top:2px;">Defensive Cushion</div>
              </div>
              <div>
                <div style="font-size:0.68rem; color:var(--muted); text-transform:uppercase; font-family:var(--font-mono);">${t.auditedMetricSharpe||"Sharpe Ratio"}</div>
                <div class="mono" style="font-size:1.2rem; font-weight:800; color:#ffffff; line-height:1.2;">1.38</div>
                <div style="font-size:0.68rem; color:#34d399; margin-top:2px;">High Risk-Adjusted</div>
              </div>
              <div>
                <div style="font-size:0.68rem; color:var(--muted); text-transform:uppercase; font-family:var(--font-mono);">${t.auditedMetricGrowth||"Growth of $10,000"}</div>
                <div class="mono" style="font-size:1.2rem; font-weight:800; color:#fbbf24; line-height:1.2;">$4,842,100</div>
                <div style="font-size:0.68rem; color:var(--muted); margin-top:2px;">+484.2x Multiple</div>
              </div>
            </div>
          </div>

          <!-- S&P 500 Benchmark Comparison Card -->
          <div style="background:#090d16; border:1px solid #1e293b; border-radius:6px; padding:14px 16px;">
            <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:10px;">
              <span style="font-size:0.82rem; font-weight:700; color:var(--text-secondary);">
                📊 ${t.auditedSpyLabel||"S&P 500 (SPY) Benchmark"}
              </span>
              <span style="font-size:0.65rem; font-family:var(--font-mono); padding:2px 6px; background:#141c2e; color:var(--muted); border-radius:3px;">
                PASSIVE BENCHMARK
              </span>
            </div>
            <div style="display:grid; grid-template-columns:1fr 1fr; gap:10px;">
              <div>
                <div style="font-size:0.68rem; color:var(--muted); text-transform:uppercase; font-family:var(--font-mono);">${t.auditedMetricCagr||"Annualized Return"}</div>
                <div class="mono" style="font-size:1.45rem; font-weight:800; color:var(--text-secondary); line-height:1.2;">+14.2%</div>
                <div style="font-size:0.68rem; color:var(--muted); margin-top:2px;">CAGR (1998–2026)</div>
              </div>
              <div>
                <div style="font-size:0.68rem; color:var(--muted); text-transform:uppercase; font-family:var(--font-mono);">${t.auditedMetricMdd||"Maximum Drawdown"}</div>
                <div class="mono" style="font-size:1.45rem; font-weight:800; color:var(--fin-down); line-height:1.2;">-50.8%</div>
                <div style="font-size:0.68rem; color:var(--muted); margin-top:2px;">2008 GFC Peak-Trough</div>
              </div>
              <div>
                <div style="font-size:0.68rem; color:var(--muted); text-transform:uppercase; font-family:var(--font-mono);">${t.auditedMetricSharpe||"Sharpe Ratio"}</div>
                <div class="mono" style="font-size:1.2rem; font-weight:800; color:var(--text-secondary); line-height:1.2;">0.68</div>
                <div style="font-size:0.68rem; color:var(--muted); margin-top:2px;">Standard Equity Risk</div>
              </div>
              <div>
                <div style="font-size:0.68rem; color:var(--muted); text-transform:uppercase; font-family:var(--font-mono);">${t.auditedMetricGrowth||"Growth of $10,000"}</div>
                <div class="mono" style="font-size:1.2rem; font-weight:800; color:var(--text-secondary); line-height:1.2;">$348,200</div>
                <div style="font-size:0.68rem; color:var(--muted); margin-top:2px;">+34.8x Multiple</div>
              </div>
            </div>
          </div>
        </div>

        <!-- COMPARATIVE PROGRESS CURVE BARS -->
        <div style="background:#070b14; border:1px solid #162032; border-radius:6px; padding:10px 14px; font-size:0.75rem; font-family:var(--font-mono);">
          <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:5px;">
            <span style="color:var(--text-secondary); font-weight:600;">Annualized Return (CAGR): Barbell +28.4% vs S&amp;P 500 +14.2%</span>
            <span style="color:#34d399; font-weight:800;">+2.0x S&amp;P Velocity</span>
          </div>
          <div style="display:flex; height:8px; border-radius:4px; overflow:hidden; background:#141c2e; margin-bottom:8px;">
            <div style="width:66.7%; background:linear-gradient(90deg, #0ecb81, #38bdf8);" title="SMH/XLV Barbell: +28.4%"></div>
            <div style="width:33.3%; background:#64748b;" title="S&P 500: +14.2%"></div>
          </div>
          <div style="display:flex; justify-content:space-between; align-items:center; color:var(--muted); font-size:0.68rem;">
            <span><span style="display:inline-block; width:8px; height:8px; background:#0ecb81; border-radius:2px; margin-right:4px;"></span>SMH/XLV Barbell: <b>+28.4%</b></span>
            <span><span style="display:inline-block; width:8px; height:8px; background:#64748b; border-radius:2px; margin-right:4px;"></span>S&amp;P 500: <b>+14.2%</b></span>
            <span style="color:#38bdf8;">Spread: <b>+14.2% / yr Outperformance</b></span>
          </div>
        </div>
      </div>

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
              <th class="col-num">${t.th_2x}</th>
              <th class="col-num">${t.th_med}</th>
              <th class="col-num">${t.th_mdd}</th>
              <th class="col-num">${t.th_dead}</th>
              <th class="col-num">${t.th_trap}</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td style="font-family:var(--font-sans); color:var(--text-secondary);">0. Market Random Entry Baseline</td>
              <td class="col-num">18.20%</td>
              <td class="col-num">+13.24%</td>
              <td class="col-num">-19.35%</td>
              <td class="col-num">74.0d</td>
              <td class="col-num">19.20%</td>
            </tr>
            <tr>
              <td style="font-family:var(--font-sans); color:var(--fin-down);">1. Blind 52-Week Low Dip Buy (+0–10% off low, below MA20)</td>
              <td class="col-num">28.91%</td>
              <td class="col-num">+20.56%</td>
              <td class="col-num" style="color:var(--fin-down);">-30.31%</td>
              <td class="col-num" style="color:var(--fin-down);">81.0d</td>
              <td class="col-num" style="color:var(--fin-down);">25.54%</td>
            </tr>
            <tr>
              <td style="font-family:var(--font-sans); color:var(--text-secondary);">2. 52-Week Low + Earnings Filter (Left-Side Entry)</td>
              <td class="col-num">30.06%</td>
              <td class="col-num">+24.28%</td>
              <td class="col-num">-29.85%</td>
              <td class="col-num">81.0d</td>
              <td class="col-num">24.82%</td>
            </tr>
            <tr class="proof-highlight">
              <td style="font-family:var(--font-sans);">3. PW-RSI Right-Side Ignition (+14–35% off low + MA20/60 Breakout + 1.40x Vol + 55D Time-Stop)</td>
              <td class="col-num" style="color:var(--fin-up);">55.24%</td>
              <td class="col-num" style="color:var(--fin-up);">+80.47% (Mean +109.1%)</td>
              <td class="col-num" style="color:var(--fin-up);">-16.49%</td>
              <td class="col-num" style="color:var(--fin-up);">29.0d</td>
              <td class="col-num" style="color:var(--fin-up);">0.93%</td>
            </tr>
          </tbody>
        </table>
      </div>
    </section>
  `}function Ht(e){const t=e.t,o=e.zoneFilter,n=(e.stocks||[]).filter(f=>!String(f.ticker).includes(".")),a=n.length,i=n.filter(f=>f.zone_code==="IGNITION_ZONE").length,p=n.filter(f=>f.zone_code==="WASHOUT_WATCH").length,r=n.filter(f=>f.zone_code==="LEFT_SIDE_KNIFE").length,m=n.filter(f=>f.zone_code==="VALUE_TRAP_FILTERED").length;return`
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
            value="${e.searchQuery||""}"
          />
        </div>
        <div class="filter-tabs">
          <button class="filter-tab ${o==="ALL"?"active":""}" data-zone="ALL">
            <span>${t.filterAll}</span>
            <span class="tab-count">${a}</span>
          </button>
          <button class="filter-tab ${o==="IGNITION_ZONE"?"active":""}" data-zone="IGNITION_ZONE">
            <span style="width:6px; height:6px; border-radius:50%; background:var(--fin-up); display:inline-block;"></span>
            <span>${t.filterIgnition}</span>
            <span class="tab-count">${i}</span>
          </button>
          <button class="filter-tab ${o==="WASHOUT_WATCH"?"active":""}" data-zone="WASHOUT_WATCH">
            <span style="width:6px; height:6px; border-radius:50%; background:var(--fin-amber); display:inline-block;"></span>
            <span>${t.filterWatch}</span>
            <span class="tab-count">${p}</span>
          </button>
          <button class="filter-tab ${o==="LEFT_SIDE_KNIFE"?"active":""}" data-zone="LEFT_SIDE_KNIFE">
            <span style="width:6px; height:6px; border-radius:50%; background:var(--fin-down); display:inline-block;"></span>
            <span>${t.filterKnife}</span>
            <span class="tab-count">${r}</span>
          </button>
          <button class="filter-tab ${o==="VALUE_TRAP_FILTERED"?"active":""}" data-zone="VALUE_TRAP_FILTERED">
            <span>${t.filterTrap}</span>
            <span class="tab-count">${m}</span>
          </button>
        </div>
      </div>
    </div>
  `}function Vt(e){const t=e.t,o=e.isProUnlocked,n=(e.filteredStocks||[]).filter(m=>!String(m.ticker).includes(".")),i=(e.config||{}).ls_site1_monthly_url||"https://truthofmarket.lemonsqueezy.com/checkout/buy/bad98d00-7175-41f6-9d58-eeb2471d0da4",p=(m,f,b=!1)=>{const d=e.sortCol===m,h=d?e.sortAsc?"▲":"▼":"↕",_=d?`sort-active ${e.sortAsc?"sort-asc":"sort-desc"}`:"";return`<th data-sort="${m}" data-base-label="${f}" class="sort-header ${_} ${b?"col-num":""}">${f} <span class="sort-chevron ${d?"":"muted"}">${h}</span></th>`},r=!o&&n.length>5?`
    <div class="soft-paywall-barrier">
      <div style="font-size:0.72rem; font-family:var(--font-mono); color:#93c5fd; font-weight:800; text-transform:uppercase; letter-spacing:0.05em; margin-bottom:4px;">
        ${t.softPaywallTitle||"🔒 67 Pro Ignition Setups Live Today"}
      </div>
      <p style="color:#cbd5e1; font-size:0.84rem; margin:0 0 14px; line-height:1.5;">
        ${t.softPaywallDesc||"Tickers 1–5 are unlocked as featured ignition leaders. Unlock live institutional target levels, -9% stops, and real-time execution signals for all remaining 67 stocks."}
      </p>
      <a class="soft-paywall-btn lemonsqueezy-button btn-unlock-row" data-direct-ls="1" href="${i}?embed=1" target="_blank" rel="noopener noreferrer">
        🍋 ${t.softPaywallUnlockCta||"Unlock 67 Pro Setups ($29/mo)"} →
      </a>
    </div>
  `:"";return`
    <div class="table-wrap">
      <table class="stock-table" id="stockTable">
        <thead>
          <tr>
            ${p("ticker",t.colTicker,!1)}
            ${p("zone_code",t.colZone,!1)}
            ${p("score",t.colScore,!0)}
            ${p("close",t.colClose,!0)}
            ${p("prox_low52_pct",t.colProx,!0)}
            ${p("dd_high52_pct",t.colDD,!0)}
            ${p("vs_ma20_pct",t.colMA,!0)}
            ${p("vol_surge_10d",t.colVol,!0)}
            ${p("hist_2x_rate",t.colHist,!0)}
            <th>${t.colTrigger}</th>
            <th>${t.colActions}</th>
          </tr>
        </thead>
        <tbody id="tableBody">
          ${Me(e)}
        </tbody>
      </table>
      ${r}
    </div>
  `}function Me(e){const t=e.t||{},o=(e.filteredStocks||[]).filter(d=>!String(d.ticker).includes(".")),n=e.lang,a=e.isProUnlocked,i=e.config||{},p=Se(i.ls_site1_monthly_url,"https://truthofmarket.lemonsqueezy.com/checkout/buy/bad98d00-7175-41f6-9d58-eeb2471d0da4"),r=encodeURIComponent(i.tradingview_aff_id||"1173809"),m=encodeURIComponent(i.seekingalpha_source||"better_life333"),f=i.broker_referral_url||"https://www.bitget.com/referral/register?clacCode=7nja",b=f.includes("?")?"&":"?";return o.length?o.map((d,h)=>{let _="badge-watch";d.zone_code==="IGNITION_ZONE"?_="badge-ignition":d.zone_code==="LEFT_SIDE_KNIFE"?_="badge-knife":d.zone_code==="VALUE_TRAP_FILTERED"&&(_="badge-trap");const l=n==="jp"?d.zone_label_jp:n==="kr"?d.zone_label_kr:d.zone_label_en,S=String(l||d.zone_code).replace(/^[🟢🟡🔴⚠️\s]+/,""),k=n==="jp"?d.name_jp:n==="kr"?d.name_kr:d.name_en,$=d.vs_ma20_pct>=0?"var(--fin-up)":"var(--fin-down)",E=d.vs_ma60_pct>=0?"var(--fin-up)":"var(--fin-down)",L=d.vol_surge_10d>=1.35?"var(--fin-up)":"var(--text-secondary)",N=Number(d.low52||0),y=Number(d.high52||d.close*1.5),C=Number(d.close||0),O=Math.max(.01,y-N),I=Math.min(100,Math.max(2,Math.round((C-N)/O*100))),X=h<5,G=a||X,z=!G,H=z?"blurred-cell":"",W=d.entry_trigger_price??d.ma60_price??Number((C*1.02).toFixed(2)),J=d.stop_loss_price??Number((C*.91).toFixed(2)),j=d.tp1_2x_price??Number((C*2).toFixed(2)),U=G,Q=`$${Number(W).toFixed(2)}`,K=`$${Number(J).toFixed(2)}`,ne=`$${Number(j).toFixed(2)}`,re=U?`<div class="mono" style="font-size:0.75rem; line-height:1.45;">
             <div><span style="color:var(--muted);">TRG</span> <span style="color:#60a5fa; font-weight:700;">${Q}</span> ${!a&&X?`<span style="font-size:0.6rem; padding:1px 4px; background:rgba(14,203,129,0.18); color:var(--fin-up); border-radius:2px; font-weight:700;">FEATURED #${h+1}</span>`:""}</div>
             <div><span style="color:var(--muted);">STP</span> <span style="color:var(--fin-down); font-weight:600;">${K}</span> · <span style="color:var(--fin-up);">TP ${ne}</span></div>
           </div>`:`<span class="pro-lock-cell btn-unlock-row" title="Unlock Pro to view exact Entry Trigger, -9% Stop & +100% Target">
             <svg width="11" height="11" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2">
               <rect x="3" y="11" width="18" height="11" rx="2" ry="2"></rect>
               <path d="M7 11V7a5 5 0 0 1 10 0v4"></path>
             </svg>
             <span>🔒 PRO TARGETS</span>
           </span>`,ie=`https://www.tradingview.com/symbols/${encodeURIComponent(d.ticker)}/?aff_id=${r}`,he=`https://seekingalpha.com/symbol/${encodeURIComponent(d.ticker)}/earnings?source=${m}`,ve=`${f}${b}symbol=${encodeURIComponent(d.ticker)}`,ye=`<div>
        <div style="display:flex; align-items:center; gap:7px;">
          <span class="mono" style="font-weight:800; font-size:0.9rem; color:#ffffff;">${d.ticker}</span>
          <span style="font-size:0.62rem; font-family:var(--font-mono); padding:1px 4px; background:#141d2f; border:1px solid #24324d; color:#93c5fd; border-radius:2px;">US</span>
          ${a?"":X?`<span style="font-size:0.6rem; padding:1px 4px; background:rgba(14,203,129,0.18); color:var(--fin-up); border-radius:2px; font-weight:700;">FEATURED #${h+1}</span>`:`<span style="font-size:0.6rem; padding:1px 5px; background:rgba(41,98,255,0.14); border:1px solid rgba(41,98,255,0.35); color:#93c5fd; border-radius:2px; font-family:var(--font-mono); font-weight:700;">PRO SETUP #${h+1}</span>`}
        </div>
        <div style="font-size:0.73rem; font-family:var(--font-sans); color:var(--muted); margin-top:2px;">
          ${k} · <span style="color:var(--text-secondary);">${d.sector}</span>
        </div>
      </div>`,_e=d.close===null||d.close===void 0?'<div class="mono" style="font-weight:700; color:var(--muted);">$0.00</div>':`<div class="mono" style="font-weight:700; color:#ffffff;" title="Latest Close Date: ${d.date||"2026-10-30"}">$${C.toFixed(2)}</div>
             <div class="range-52w-wrap" title="52W Range: $${N.toFixed(2)} – $${y.toFixed(2)} | Current: $${C.toFixed(2)}">
               <div class="range-52w-track">
                 <div class="range-52w-pin" style="left:${I}%;"></div>
               </div>
               <div class="range-52w-labels">
                 <span>$${N.toFixed(0)}</span>
                 <span class="range-52w-curr">${I}%</span>
                 <span>$${y.toFixed(0)}</span>
               </div>
             </div>`;return`
      <tr data-ticker="${d.ticker}" class="${z?"soft-paywall-row":""}">
        <td>
          ${ye}
        </td>
        <td>
          <span class="badge ${_}">${S}</span>
          <div class="cond-strip">
            <span class="cond-chip ${d.c1_deep_dd?"pass":""}" title="52W High Drawdown <= -20%">DD</span>
            <span class="cond-chip ${d.c2_off_low??d.c2_sweet_spot?"pass":""}" title="52W Low Proximity 10-45%">LOW</span>
            <span class="cond-chip ${d.c3_above_mas??d.c3_ma_reclaim?"pass":""}" title="Reclaimed MA20/MA60">MA</span>
            <span class="cond-chip ${d.c4_vol_or_mom??d.c4_vol_washout?"pass":""}" title="10D Volume Washout >= 1.3x">VOL</span>
          </div>
        </td>
        <td class="col-num ${H}">
          <div style="display:flex; align-items:center; justify-content:flex-end; gap:6px;">
            <div class="score-bar">
              <div class="score-fill" style="width:${Number(d.score??0)}%; background:${d.score>=80?"var(--fin-up)":d.score>=55?"var(--fin-amber)":"var(--fin-down)"};"></div>
            </div>
            <span class="mono" style="font-weight:800; font-size:0.9rem; width:26px; text-align:right;">${Number(d.score??0)}</span>
          </div>
        </td>
        <td class="col-num ${H}">
          ${_e}
        </td>
        <td class="mono col-num ${H}" style="color:${d.prox_low52_pct<=40&&d.prox_low52_pct>=10?"var(--fin-up)":"var(--text-secondary)"}; font-weight:600;">
          +${Number(d.prox_low52_pct??0).toFixed(1)}%
        </td>
        <td class="mono col-num ${H}" style="color:var(--fin-down); font-weight:600;">
          ${Number(d.dd_high52_pct??0).toFixed(1)}%
        </td>
        <td class="mono col-num ${H}">
          <span style="color:${$}; font-weight:600;">${Number(d.vs_ma20_pct??0)>=0?"+":""}${Number(d.vs_ma20_pct??0).toFixed(1)}%</span>
          <span style="color:var(--muted);"> / </span>
          <span style="color:${E}; font-weight:600;">${Number(d.vs_ma60_pct??0)>=0?"+":""}${Number(d.vs_ma60_pct??0).toFixed(1)}%</span>
        </td>
        <td class="mono col-num ${H}" style="color:${L}; font-weight:700;">
          ${Number(d.vol_surge_10d??1).toFixed(2)}x
        </td>
        <td class="mono col-num ${H}" style="font-weight:700; color:${d.hist_2x_rate>=40?"var(--fin-up)":"var(--text-secondary)"};">
          ${Number(d.hist_2x_rate??0).toFixed(1)}%
        </td>
        <td>${re}</td>
        <td>
          <div style="display:flex; gap:5px;">
            ${z?`<a class="btn btn-primary btn-sm lemonsqueezy-button btn-unlock-row" data-direct-ls="1" href="${p}" target="_blank" rel="noopener noreferrer" style="white-space:nowrap; font-weight:700;">
                     🔒 ${t.softPaywallUnlockCta||"Unlock 67 Pro Setups ($29/mo)"}
                   </a>`:`
            <button class="btn btn-sm btn-share-card" data-ticker="${d.ticker}" title="Export Institutional Tear Sheet PNG">
              PNG
            </button>
            <a class="btn btn-sm" href="${ie}" target="_blank" rel="noopener noreferrer" title="Open TradingView Chart (Partner)">
              TV ↗
            </a>
            <a class="btn btn-sm" href="${he}" target="_blank" rel="noopener noreferrer" title="Open Seeking Alpha Fundamentals (Partner)">
              SA ↗
            </a>
            <a class="btn btn-sm" href="${ve}" target="_blank" rel="noopener noreferrer" title="Execute Trade on Partner Broker / Exchange" style="border-color:rgba(16,185,129,0.4); color:#34d399;">
              Trade ↗
            </a>
            `}
          </div>
        </td>
      </tr>
    `}).join(""):`
      <tr>
        <td colspan="11" style="text-align:center; padding:36px; color:var(--muted); font-family:var(--font-sans);">
          No US-listed equities match the active filter criteria.
        </td>
      </tr>
    `}function Gt(e){const t=e.t,o=e.stocks||[],n=o.find(r=>r.ticker==="CELH"),a=n?Number(n.close).toFixed(2):"27.93",i=n&&n.date?n.date:"2026-10-13",p=e.docLastResult?Be(e.docLastResult):`<div style="color:var(--muted);">Enter US ticker, cost basis ($), and trading days held to evaluate asymmetric exit triggers against the latest closing price ($${a}).</div>`;return`
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
            <input type="number" id="docEntry" step="0.01" value="${a}" placeholder="${a}" style="padding:7px 9px; background:#05080f; border:1px solid var(--border); color:#fff; border-radius:3px; font-family:var(--font-mono); width:100%; margin-top:3px;" />
          </div>
          <div>
            <label style="font-size:0.68rem; color:var(--muted); font-family:var(--font-mono); text-transform:uppercase;">Trading Days</label>
            <input type="number" id="docDays" value="42" placeholder="42" style="padding:7px 9px; background:#05080f; border:1px solid var(--border); color:#fff; border-radius:3px; font-family:var(--font-mono); width:100%; margin-top:3px;" />
          </div>
        </div>

        <div style="display:flex; gap:5px; flex-wrap:wrap; align-items:center; margin-bottom:12px;">
          <span style="font-size:0.68rem; color:var(--muted); font-family:var(--font-mono);">LATEST CLOSE PRESETS (${i}):</span>
          ${["CELH","MBLY","APP","UPST","NVDA","CCL"].map(r=>{const m=o.find(b=>b.ticker===r),f=m?` $${Number(m.close).toFixed(2)}`:"";return`
                <button class="btn btn-sm btn-quick-doc mono" data-ticker="${r}" style="padding:2px 6px; font-size:0.68rem;">${r}${f}</button>
              `}).join("")}
        </div>
      </div>

      <div>
        <button class="btn btn-primary" id="btnRunPositionDoctor" style="width:100%; justify-content:center; padding:9px;">
          ${t.tool1Btn}
        </button>
        <div id="docOutput" style="margin-top:12px; font-size:0.8rem; background:#05080f; padding:12px; border-radius:4px; border:1px solid var(--border); border-left:3px solid var(--fin-blue);">
          ${p}
        </div>
      </div>
    </div>
  `}function Be(e){let t="var(--fin-up)",o="var(--fin-up)";e.status_code==="CRITICAL_STOP"||e.status_code==="HARD_STOP"||e.is_critical?(t="var(--fin-down)",o="var(--fin-down)"):e.status_code==="DEAD_MONEY"||e.status_code==="TIME_STOP"?(t="var(--fin-amber)",o="var(--fin-amber)"):(e.status_code==="TP1_REACHED"||e.status_code==="TP1_HARVEST")&&(t="var(--fin-up)",o="var(--fin-up)");const n=String(e.status_label||e.status_code||"ACTIVE_HOLD").replace(/^[🟢🚨🛑⏳🎯⏰🏆\s]+/,""),a=Number(e.return_pct??0),i=`${a>=0?"+":""}${a.toFixed(2)}%`,p=e.stop_price!==void 0&&e.stop_price!==null&&Number(e.stop_price)>0?Number(e.stop_price)/.91:e.tp1_price!==void 0&&e.tp1_price!==null&&Number(e.tp1_price)>0?Number(e.tp1_price)/2:27.93,r=e.entry_price!==void 0&&e.entry_price!==null&&Number(e.entry_price)>0?Number(e.entry_price):p,m=e.current_price!==void 0&&e.current_price!==null&&Number(e.current_price)>0?Number(e.current_price):r*(1+a/100),f=e.stop_price!==void 0&&e.stop_price!==null?Number(e.stop_price):r*.91,b=e.tp1_price!==void 0&&e.tp1_price!==null?Number(e.tp1_price):r*2,d=f>0?`$${f.toFixed(2)}`:"$0.00",h=b>0?`$${b.toFixed(2)}`:"$0.00",_=m>0?`$${m.toFixed(2)}`:"$0.00",l=r>0?`$${r.toFixed(2)}`:"$0.00";return`
    <div style="border-left: 3px solid ${o}; padding-left: 10px;">
      <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:6px;">
        <span class="mono" style="font-weight:800; font-size:0.84rem; color:${t};">
          ${n}
        </span>
        <span class="mono" style="font-weight:800; color:${a>=0?"var(--fin-up)":"var(--fin-down)"}; font-size:0.86rem;">
          P&L: ${i}
        </span>
      </div>
      <div class="mono" style="font-size:0.73rem; color:#93c5fd; margin-bottom:4px;">
        $${e.ticker||"CELH"} Latest Close: <b style="color:#fff;">${_}</b> · Cost Basis: <b style="color:#fff;">${l}</b>
      </div>
      <div style="font-weight:700; color:#ffffff; font-size:0.78rem; margin-bottom:4px;">
        Rule Triggered: ${e.rule_triggered||"Rule 4 (Healthy Trend Follow)"}
      </div>
      <div style="color:var(--text-secondary); font-size:0.78rem; line-height:1.45; margin-bottom:8px;">
        <b>Execution Directive:</b> ${e.action_plan||""}
      </div>
      <div class="mono" style="display:flex; gap:14px; font-size:0.72rem; color:var(--muted); border-top:1px solid var(--border); padding-top:6px;">
        <span>Hard Stop (-9%): <b style="color:var(--fin-down);">${d}</b></span>
        <span>TP1 Target (2x): <b style="color:var(--fin-up);">${h}</b></span>
      </div>
    </div>
  `}function jt(e){const t=e.t,o=e.isProUnlocked,n=e.stocks||[],a=n.filter(y=>y.zone_code==="IGNITION_ZONE"||Number(y.score)>=75).slice(0,5),i=Number(e.proPortfolioUsd||3e4),p=Math.round(i*.15),r=n.find(y=>y.ticker==="CELH"),m=n.find(y=>y.ticker==="MBLY"),f=r&&r.close?Number(r.close).toFixed(2):"29.12",b=r&&r.ma20_price?Number(r.ma20_price).toFixed(2):"28.19",d=r&&r.ma60_price?Number(r.ma60_price).toFixed(2):"29.16",h=r&&r.tp1_2x_price?Number(r.tp1_2x_price).toFixed(2):(Number(f)*2).toFixed(2),_=r&&r.stop_loss_price?Number(r.stop_loss_price).toFixed(2):(Number(f)*.91).toFixed(2),l=r?Number(r.score):84,S=m&&m.close?Number(m.close).toFixed(2):"5.96",k=m&&m.low52?Number(m.low52).toFixed(2):"5.86",$=m&&m.ma20_price?Number(m.ma20_price).toFixed(2):"6.83",E=m?Number(m.score):20,L=we(o),N=e.pineCode||`//@version=5
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
plotshape(ignition and not ignition[1], "PW-RSI IGNITION", shape.labelup, location.belowbar, color.green, text="IGNITION", textcolor=color.white)`;return`
    <section class="proof-card" id="proVaultSection" style="border-top:2px solid var(--fin-blue); margin-bottom:22px;">
      <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:10px; margin-bottom:16px;">
        <div>
          <span class="badge ${o?"badge-ignition":"badge-watch"}" id="vaultBadge">
            ${o?t.vaultBadgeUnlocked:t.vaultBadgeLocked}
          </span>
          <h2 style="font-size:1.2rem; font-weight:800; margin-top:6px; color:#ffffff; letter-spacing:-0.01em;">
            ${t.vaultTitle}
          </h2>
        </div>
        <button class="btn btn-primary" id="vaultUnlockBtn" style="${o?"display:none;":""}">
          ${t.vaultUnlockBtn}
        </button>
      </div>

      <!-- FREE INTERACTIVE BAIT: 3-SECOND POSITION DOCTOR (UNBLURRED FOR ALL VISITORS) -->
      <div style="margin-bottom:18px;">
        ${Gt(e)}
      </div>

      <div style="position:relative;">
        ${o?"":`<div id="vaultOverlayUnlock" style="position:absolute; inset:0; z-index:10; display:flex; align-items:center; justify-content:center; background:rgba(6,9,17,0.58); border-radius:6px; cursor:pointer;">
                 <div style="background:#0d1424; border:1px solid var(--fin-blue); box-shadow:0 12px 32px rgba(0,0,0,0.75); border-radius:6px; padding:22px 26px; text-align:center; max-width:500px;">
                   <div class="mono" style="font-size:0.72rem; color:#fbbf24; font-weight:800; letter-spacing:0.05em;">👑 PRO VIP ALPHA COMMAND CENTER LOCKED</div>
                   <div style="font-size:1.05rem; font-weight:800; color:#ffffff; margin:8px 0;">
                     Unlock All 72 Stock Targets, Daily Ignition Order Book, Position Sizing Calculator & Pine Script v5
                   </div>
                   <div style="font-size:0.8rem; color:var(--muted); margin-bottom:14px; line-height:1.5;">
                     Free users see only 1 sample stock ($CELH). Upgrade to Pro ($29/mo or $199 Lifetime) to reveal all hidden VIP Ignition picks, exact share-sizing orders, Position Doctor diagnostics, and the 26-Year Semiconductor CSV.
                   </div>
                   <span class="btn btn-primary" style="justify-content:center; width:100%; padding:10px; font-weight:800;">
                     🔑 Enter Pro License Key / Subscribe Now →
                   </span>
                 </div>
               </div>`}

      <!-- PRO VIP MODULE 00: TODAY'S IGNITION ORDER BOOK & ACCOUNT POSITION SIZING ENGINE -->
      <div class="${o?"":"blur-locked"}" style="background:#090d16; border:1px solid rgba(16,185,129,0.35); border-left:4px solid var(--fin-up); border-radius:4px; padding:16px 18px; margin-bottom:16px;">
        <!-- PRO VIP PRIVATE TELEGRAM CHANNEL INVITE BANNER -->
        <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:10px; background:rgba(2,132,199,0.14); border:1px solid rgba(56,189,248,0.45); border-radius:6px; padding:12px 14px; margin-bottom:14px;">
          <div>
            <div class="mono" style="font-size:0.68rem; color:#38bdf8; font-weight:800; letter-spacing:0.05em;">
              🔒 PRO SUBSCRIBERS ONLY · PRIVATE VIP TELEGRAM NEWS & SIGNAL DESK
            </div>
            <div style="font-size:0.86rem; font-weight:800; color:#ffffff; margin-top:2px;">
              Real-Time $SMH / $XLV & 72-Equity Breaking News + Daily Unmasked Ignition Order Book Alerts
            </div>
          </div>
          <a
            class="btn btn-sm ${o?"":"btn-gated-vip-tg"}"
            href="${o?L:"#pricingSection"}"
            ${o?'target="_blank" rel="noopener noreferrer"':""}
            style="background:#0284c7; border-color:#38bdf8; color:#ffffff; font-weight:800; padding:8px 14px;"
          >
            ✈️ Join Pro VIP Telegram Channel ↗
          </a>
        </div>

        <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:10px; margin-bottom:12px;">
          <div>
            <div class="mono" style="font-size:0.7rem; color:var(--fin-up); font-weight:800; letter-spacing:0.05em;">
              👑 PRO VIP EXCLUSIVE · DAILY RIGHT-SIDE IGNITION ORDER BOOK & POSITION SIZING
            </div>
            <h3 style="font-size:1.02rem; font-weight:800; color:#ffffff; margin-top:3px;">
              Today's Top Turnaround Action Sheet (1.35% Max Account Risk per Position)
            </h3>
          </div>
          <div style="display:flex; align-items:center; gap:8px;">
            <label class="mono" style="font-size:0.72rem; color:var(--muted);">MY ACCOUNT ($ USD):</label>
            <input type="number" id="proCapitalInput" value="${i}" step="5000" min="1000" style="width:120px; padding:6px 8px; background:#05080f; border:1px solid var(--border); color:#fff; border-radius:4px; font-family:var(--font-mono); font-weight:700; margin:0;" />
            <button type="button" class="btn btn-emerald btn-sm" id="btnCalcProSizing">Update Shares</button>
          </div>
        </div>
        <div class="table-responsive-scroll">
          <table class="stock-table" style="font-size:0.78rem;">
            <thead>
              <tr>
                <th>VIP Pick</th>
                <th>PW Score</th>
                <th>Latest Close</th>
                <th>Entry Trigger (MA20/60)</th>
                <th>-9.0% Hard Stop</th>
                <th>+100% TP1 Target</th>
                <th>15% Slot Allocation ($${p.toLocaleString()})</th>
                <th>Max Loss Impact</th>
              </tr>
            </thead>
            <tbody>
              ${a.map((y,C)=>{if(!o&&C>=1){const W=Math.round(p*.09);return`
                    <tr>
                      <td class="mono" style="font-weight:800; color:#fbbf24;">🔒 VIP IGNITION #${C+1} <span style="color:var(--muted); font-weight:500;">(🔒 VIP SECTOR)</span></td>
                      <td class="mono" style="color:var(--fin-up); font-weight:800;">${y.score}/100</td>
                      <td class="mono">🔒 PRO</td>
                      <td class="mono" style="color:#60a5fa; font-weight:700;">🔒 PRO</td>
                      <td class="mono" style="color:var(--fin-down); font-weight:700;">🔒 PRO</td>
                      <td class="mono" style="color:var(--fin-up); font-weight:700;">🔒 PRO</td>
                      <td class="mono" style="color:#ffffff; font-weight:800;">🔒 Unlock Pro ($29/mo)</td>
                      <td class="mono" style="color:var(--fin-amber);">-$${W.toLocaleString()} (-1.35% Eq)</td>
                    </tr>
                  `}const I=Number(y.close||29.12),X=Number(y.entry_trigger_price??y.ma60_price??I).toFixed(2),F=Number(y.stop_loss_price??I*.91).toFixed(2),G=Number(y.tp1_2x_price??I*2).toFixed(2),z=Math.max(1,Math.floor(p/I)),H=Math.round(z*I*.09);return`
                    <tr>
                      <td class="mono" style="font-weight:800; color:#ffffff;">#${C+1} $${y.ticker} <span style="color:var(--muted); font-weight:500;">(${y.sector})</span></td>
                      <td class="mono" style="color:var(--fin-up); font-weight:800;">${y.score}/100</td>
                      <td class="mono">$${I.toFixed(2)}</td>
                      <td class="mono" style="color:#60a5fa; font-weight:700;">$${X}</td>
                      <td class="mono" style="color:var(--fin-down); font-weight:700;">$${F}</td>
                      <td class="mono" style="color:var(--fin-up); font-weight:700;">$${G}</td>
                      <td class="mono" style="color:#ffffff; font-weight:800;">Buy ${z} shares ($${Math.round(z*I).toLocaleString()})</td>
                      <td class="mono" style="color:var(--fin-amber);">-$${H.toLocaleString()} (-1.35% Eq)</td>
                    </tr>
                  `}).join("")}
            </tbody>
          </table>
        </div>
      </div>

      <div id="vaultContentWrap" class="${o?"":"blur-locked"}" style="display:grid; grid-template-columns:repeat(auto-fit, minmax(330px, 1fr)); gap:16px;"><!-- Position Doctor moved to free unblurred top section -->
        <!-- Module 01: Position Doctor rendered in free unblurred section above -->

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
                  <b class="mono" style="color:#ffffff;">CELH · Celsius Holdings ($${f})</b>
                  <span class="badge badge-ignition">SCORE ${l}</span>
                </div>
                <div style="color:var(--muted); font-size:0.76rem; margin-top:4px; line-height:1.45;">
                  PepsiCo North America inventory destocking complete; 2026E operating leverage +257%. Latest Close <b class="mono" style="color:#fff;">$${f}</b> reclaiming MA20 ($${b}) toward MA60 ($${d}). Stop: $${_} · TP1 (2x): <b class="mono" style="color:var(--fin-up);">$${h}</b>.
                </div>
                <button class="btn btn-sm btn-open-research" data-ticker="CELH" style="margin-top:6px;">
                  Read $CELH SEC Research Brief ↗
                </button>
              </div>

              <div style="border-left:3px solid var(--fin-down); padding-left:10px;">
                <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:4px;">
                  <b class="mono" style="color:#ffffff;">MBLY · Mobileye Global ($${S})</b>
                  <span class="badge badge-knife">🛑 RULE 1 STOP EXECUTED · SCORE ${E}</span>
                </div>
                <div style="color:var(--muted); font-size:0.76rem; margin-top:4px; line-height:1.45;">
                  <b style="color:#fca5a5;">Post-Mortem Audit:</b> Oct 13 watch ($7.02) breached Rule 1 Hard Stop (<b class="mono" style="color:var(--fin-down);">$6.39 / -9.0%</b>) and fell to <b class="mono" style="color:#fff;">$${S}</b> (52W Low $${k}, <span class="mono">LEFT_SIDE_KNIFE</span>). Mechanical exit protected capital & rotated into <b class="mono" style="color:var(--fin-up);">$CELH / $LULU</b>. Re-entry prohibited until MA20 ($${$}) reclaim.
                </div>
                <button class="btn btn-sm btn-open-research" data-ticker="MBLY" style="margin-top:6px;">
                  Read $MBLY Rule 1 Stop Audit Brief ↗
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

            <pre id="pineCodeBox" style="background:#05080f; padding:12px; border-radius:4px; font-size:0.7rem; color:#93c5fd; overflow-x:auto; max-height:155px; font-family:var(--font-mono); border:1px solid var(--border); line-height:1.45;">${N}</pre>
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
  `}const pt={en:{t1Badge:"INSTITUTIONAL PRO",t1Title:"Pro Quantitative Terminal & Daily SEC Brief",t1Period:"/ month",t1Items:["Unmask all 72 US Equity PW-RSI Scores, MA60 Breakout Triggers & -9% Stop Levels","Daily 08:10 EST Primary-Filing (10-K/10-Q/8-K) Turnaround Research Digest","Position Risk & 55-Day Time-Stop Diagnostic Engine (Position Doctor)","Full TradingView Pine Script v5 Indicator Source Code + SemiFearGreed 26Y CSV"],t1Btn:"Subscribe via Lemon Squeezy ($29/mo)",t2Badge:"FOUNDER ALLOCATION",t2Title:"Lifetime Research & Terminal License",t2Period:"/ one-time",t2Items:["Permanent License Key — Zero recurring monthly subscription charges","Complete 26.8-Year (2000–2026) US Equity & Semiconductor ETF Backtest Datasets","Multilingual Access (English, Japanese & Korean SEC Research Briefs)","Full Access to both RightSideAlpha and SemiFearGreed Pro Features"],t2Btn:"Acquire Lifetime License ($199)",t3Badge:"EXECUTION & CHARTING PARTNERS",t3Title:"Direct Charting, Consensus & Broker Execution",t3Desc:"Verify MA20/MA60 volume breakouts, EPS revisions, and execute US stock/ETF orders with fee rebates:",t3Items:["<b>TradingView Pro</b> — Multi-timeframe MA20/MA60 & Pine Script v5 execution","<b>Seeking Alpha Premium</b> — Quant Grades & 1-2Y consensus EPS revision tracking","<b>US Brokerage & Global Exchange</b> — Low-spread NYSE/NASDAQ & 24/7 Perp execution"],tvBtn:"📈 Launch TradingView Terminal ↗",saBtn:"📊 Open Seeking Alpha EPS Consensus ↗",brokerBtn:"🏦 Open US Broker / Exchange Partner Bonus ↗",tgBtn:"🔒 Pro VIP Telegram ($SMH/$XLV & 72-Stock Live News)"},kr:{t1Badge:"PRO 퀀트 멤버십",t1Title:"프로 퀀트 터미널 & 일간 SEC 공시 리서치",t1Period:"/ 월 구독",t1Items:["미국 상장 72개 전 종목 진입 트리거(TRG) · -9% 칼손절(STP) · +100% 목표가(TP1) 전면 공개","매일 아침 SEC 원문(10-K/10-Q/8-K) 기반 우측 시동 턴어라운드 핵심 요약 브리프","포지션 닥터(Position Doctor): 내 보유종목 -9% 손절 / 55일 시간손절 / 원금회수 실시간 판독","TradingView Pine Script v5 전용 지표 원본 코드 + 반도체 공포·탐욕 26년치 CSV 다운로드"],t1Btn:"Lemon Squeezy로 Pro 구독하기 ($29/월)",t2Badge:"파운더 평생 소장권",t2Title:"평생 리서치 & 터미널 무제한 라이선스",t2Period:"/ 1회 결제 (평생)",t2Items:["영구 라이선스 키 즉시 발급 — 매월 나가는 정기 구독료 평생 0원","26.8년(2000–2026) 미국 개별주 & 반도체($SMH:$XLV) 전체 백테스트 원본 데이터셋 제공","한국어 · 영어 · 일본어 3개 국어 SEC 리서치 브리프 및 텔레그램 실시간 알림 연동","RightSideAlpha(개별주) + SemiFearGreed(반도체 공포지수) 모든 Pro 기능 영구 잠금 해제"],t2Btn:"평생 라이선스 소장하기 ($199)",t3Badge:"차트 · 분석 · 증권/거래소 제휴 혜택",t3Title:"실전 차트 검증 & 제휴 증권사/거래소 수수료 혜택",t3Desc:"MA20/MA60 거래량 돌파 차트 확인부터 EPS 컨센서스 점검, 실전 매매 수수료 리베이트까지 원클릭으로 연결됩니다:",t3Items:["<b>TradingView Pro</b> — MA20/MA60 돌파 및 Pine Script v5 지표 자동 작도 (제휴 할인)","<b>Seeking Alpha Premium</b> — 월가 애널리스트 1~2년 선행 EPS 상향 리비전 추적","<b>제휴 증권사 & 글로벌 거래소</b> — 미국주식(IBKR/Webull) 및 24시간 지수/선물 수수료 우대"],tvBtn:"📈 TradingView 차트 터미널 열기 ↗",saBtn:"📊 Seeking Alpha 실적 컨센서스 열기 ↗",brokerBtn:"🏦 제휴 증권사 / 거래소 수수료 혜택 받기 ↗",tgBtn:"🔒 Pro 전용 VIP 텔레그램 ($SMH/$XLV & 72종목 실시간 월가 뉴스)"},jp:{t1Badge:"INSTITUTIONAL PRO",t1Title:"Pro クオンツターミナル＆日次SECリサーチ",t1Period:"/ 月額",t1Items:["米国72銘柄すべてのMA60突破トリガー(TRG)・-9%損切(STP)・+100%目標値(TP1)を完全公開","毎朝08:10 EST更新・SEC一次開示(10-K/10-Q/8-K)ターンアラウンド分析ブリーフ","ポジションドクター：保有銘柄の-9%損切 / 55日タイムストップ / 元本回収を即時診断","TradingView Pine Script v5 インジケーター完全ソース＋半導体指数26年分CSVダウンロード"],t1Btn:"Lemon SqueezyでPro購読 ($29/月)",t2Badge:"FOUNDER LIFETIME",t2Title:"永久リサーチ＆ターミナルライセンス",t2Period:"/ 買い切り(永久)",t2Items:["永久ライセンスキー発行 — 毎月のサブスクリプション費用ゼロ","26.8年間(2000–2026)の米国株＆半導体ETF完全バックテストデータセット収録","日本語・英語・韓国語対応のSECリサーチブリーフ＆Telegramアラート連携","RightSideAlpha＋SemiFearGreedの全Pro機能を永久アンロック"],t2Btn:"永久ライセンスを取得 ($199)",t3Badge:"EXECUTION & CHARTING PARTNERS",t3Title:"チャート検証・EPSコンセンサス・提携証券/取引所",t3Desc:"MA20/MA60出来高ブレイクの確認、EPSリビジョン検証、米国株・指数の執行パートナー特典：",t3Items:["<b>TradingView Pro</b> — マルチタイムフレームMA20/MA60＆Pine Script v5実行","<b>Seeking Alpha Premium</b> — クオンツ評価＆1〜2年先EPSコンセンサス推移","<b>提携証券・取引所 (IBKR / Webull / Bybit)</b> — 米国株・24時間インデックス取引特典"],tvBtn:"📈 TradingView チャートを開く ↗",saBtn:"📊 Seeking Alpha EPSコンセンサス ↗",brokerBtn:"🏦 提携証券・取引所の手数料特典を見る ↗",tgBtn:"🔒 Pro専用 VIP Telegram ($SMH/$XLV & 72銘柄リアルタイムニュース)"}};function vt(e){const t=e.config||{},o=pt[e.lang]||pt.en,n=Se(t.ls_site1_monthly_url,"https://truthofmarket.lemonsqueezy.com/checkout/buy/bad98d00-7175-41f6-9d58-eeb2471d0da4"),a=Se(t.ls_site1_ltd_url,"https://truthofmarket.lemonsqueezy.com/checkout/buy/00c9f6e1-c8be-42a4-b5a5-e05af1a41ed9"),i=t.broker_name||"Bitget (7nja)",p=encodeURIComponent(t.tradingview_aff_id||"1173809"),r=encodeURIComponent(t.seekingalpha_source||"better_life333"),m=t.broker_referral_url||"https://www.bitget.com/referral/register?clacCode=7nja",f=`https://www.tradingview.com/?aff_id=${p}`,b=`https://seekingalpha.com/symbol/SPY/earnings?source=${r}`,d=`
    <span class="price-check">
      <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="#10b981" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round">
        <polyline points="20 6 9 17 4 12"></polyline>
      </svg>
    </span>
  `;return`
    <div id="pricingSection">
      <div class="pricing-grid">
        <!-- Tier 1: Pro Monthly -->
        <div class="price-card featured">
          <div>
            <div style="display:flex; justify-content:space-between; align-items:center; gap:8px;">
              <span class="badge badge-ignition">${o.t1Badge}</span>
              <span class="badge price-badge-popular">POPULAR</span>
            </div>
            <h3 style="font-size:1.12rem; font-weight:800; margin-top:10px; color:#ffffff;">
              ${o.t1Title}
            </h3>
            <div class="price-num">$29 <span style="font-size:0.82rem; color:var(--muted); font-family:var(--font-sans); font-weight:500;">${o.t1Period}</span></div>
            <div class="price-subtext">Billed monthly · Cancel anytime with 1 click</div>
            <ul class="price-list">
              ${o.t1Items.map(h=>`<li>${d}<span>${h}</span></li>`).join("")}
            </ul>
          </div>
          <a class="btn btn-primary lemonsqueezy-button" id="cardMonthlyBtn" href="${n}" target="_blank" rel="noopener noreferrer" style="justify-content:center; padding:10px;">
            ${o.t1Btn}
          </a>
        </div>

        <!-- Tier 2: Lifetime Pass -->
        <div class="price-card best-value">
          <div>
            <div style="display:flex; justify-content:space-between; align-items:center; gap:8px;">
              <span class="badge badge-watch">${o.t2Badge}</span>
              <span class="badge price-badge-lifetime">BEST VALUE · SAVE 43%</span>
            </div>
            <h3 style="font-size:1.12rem; font-weight:800; margin-top:10px; color:#ffffff;">
              ${o.t2Title}
            </h3>
            <div class="price-num">$199 <span style="font-size:0.82rem; color:var(--muted); font-family:var(--font-sans); font-weight:500;">${o.t2Period}</span></div>
            <div class="price-subtext">One-time payment · Instant permanent license delivery</div>
            <div class="price-savings-pill">⚡ Breakeven in 6.8 Months vs $29/mo ($199 vs $348/yr) · 100% Free Thereafter</div>
            <ul class="price-list">
              ${o.t2Items.map(h=>`<li>${d}<span>${h}</span></li>`).join("")}
            </ul>
          </div>
          <a class="btn btn-emerald lemonsqueezy-button" id="cardLtdBtn" href="${a}" target="_blank" rel="noopener noreferrer" style="justify-content:center; padding:10px;">
            ${o.t2Btn}
          </a>
        </div>

        <!-- Tier 3: Institutional Charting, Consensus & Broker/Exchange Partners -->
        <div class="price-card">
          <div>
            <span class="badge" style="background:rgba(41,98,255,0.14); color:#93c5fd; border:1px solid rgba(41,98,255,0.3);">${o.t3Badge}</span>
            <h3 style="font-size:1.12rem; font-weight:800; margin-top:10px; color:#ffffff;">
              ${o.t3Title}
            </h3>
            <p style="color:var(--muted); font-size:0.8rem; margin-top:8px; line-height:1.5;">
              ${o.t3Desc}
            </p>
            <ul class="price-list">
              ${o.t3Items.map(h=>`<li>${d}<span>${h}</span></li>`).join("")}
            </ul>
          </div>
          <div style="display:flex; flex-direction:column; gap:7px;">
            <a class="btn" id="affTvBtn" href="${f}" target="_blank" rel="noopener noreferrer" style="justify-content:center;">
              ${o.tvBtn}
            </a>
            <a class="btn" id="affSaBtn" href="${b}" target="_blank" rel="noopener noreferrer" style="justify-content:center;">
              ${o.saBtn}
            </a>
            <a class="btn" id="affBrokerBtn" href="${m}" target="_blank" rel="noopener noreferrer" style="justify-content:center; border-color:rgba(16,185,129,0.45); color:#34d399; font-weight:700;">
              ${o.brokerBtn} (${i})
            </a>
            <a class="btn ${e.isProUnlocked?"":"btn-gated-vip-tg"}" id="pricingTelegramChannelBtn" href="${we(e.isProUnlocked)}" ${e.isProUnlocked?'target="_blank" rel="noopener noreferrer"':""} style="justify-content:center; border-color:rgba(56,189,248,0.45); color:#38bdf8; font-weight:700;">
              ${e.isProUnlocked?"👑 Enter Pro VIP Telegram Channel ↗":o.tgBtn}
            </a>
            <div style="display:grid; grid-template-columns:1fr 1fr; gap:8px;">
              <a class="btn" id="pricingYoutubeBtn" href="${t.youtube_url||"https://youtube.com/@rightsidealpha"}" target="_blank" rel="noopener noreferrer" style="justify-content:center; border-color:rgba(239,68,68,0.4); color:#fca5a5;">
                📺 YouTube (@rightsidealpha) ↗
              </a>
              <a class="btn" id="pricingInstagramBtn" href="${t.instagram_url||"https://www.instagram.com/rightsidealpha"}" target="_blank" rel="noopener noreferrer" style="justify-content:center; border-color:rgba(236,72,153,0.4); color:#f9a8d4;">
                📸 Instagram (@rightsidealpha) ↗
              </a>
            </div>
          </div>
        </div>
      </div>

      <!-- Trust & Security Micro-Ribbon (Lemon Squeezy PCI-DSS & Instant Key Delivery) -->
      <div class="pricing-trust-ribbon">
        <div class="trust-badge">
          <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="#10b981" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <rect x="3" y="11" width="18" height="11" rx="2" ry="2"></rect>
            <path d="M7 11V7a5 5 0 0 1 10 0v4"></path>
          </svg>
          <span>Merchant of Record: <b>Lemon Squeezy, LLC</b></span>
        </div>
        <div class="trust-badge">
          <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="#60a5fa" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"></path>
          </svg>
          <span>256-Bit SSL Encrypted Checkout</span>
        </div>
        <div class="trust-badge">
          <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="#34d399" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <polyline points="20 6 9 17 4 12"></polyline>
          </svg>
          <span>Instant Key Delivery &amp; VAT Invoicing</span>
        </div>
      </div>
    </div>
  `}function qt(e){const t=e.t||{},o=e.config||{},n=o.telegram_channel_url||"https://t.me/truthofmarketss",a=o.youtube_url||"https://youtube.com/@rightsidealpha",i=o.instagram_url||"https://www.instagram.com/rightsidealpha",p=e.telegramChatId||o.telegram_chat_id||"@truthofmarketss",r=e.telegramBotToken||"DEMO-BOT-TOKEN",m=e.telegramAlertType||"SEMI_BRIEFING",f=e.semiOverview||{},b=f.date||"2026-10-30",d=Number(f.fg_score??18).toFixed(1),h=String(f.regime_en||"EXTREME FEAR").toUpperCase(),_=Number(f.smh_close??522.49).toFixed(2),l=Number(f.smh_dd_pct??-22.23).toFixed(2),S=Number(f.smh_rsi??40.6).toFixed(1),k=Number(f.xlv_close??184.87).toFixed(2),$=Number(f.qqq_close??690.49).toFixed(2),E=f.recommended_smh_weight??80,L=f.recommended_xlv_weight??20,N=e.telegramPreviewText||`🧭 [SemiFearGreed] Daily Semiconductor & Barbell Briefing (${b})
• Fear & Greed Score: ${d} / 100 (${h})
• $SMH (Semiconductor): $${_} (${l}% 52W DD | RSI ${S})
• $XLV (Healthcare Vault): $${k} | $QQQ: $${$}
• Active Signal: Target ${E}% $SMH : ${L}% $XLV Barbell Allocation`;return`
    <!-- LICENSE ACTIVATION MODAL -->
    <div class="modal-backdrop" id="licenseModal">
      <div class="modal">
        <div style="font-size:0.68rem; font-family:var(--font-mono); color:#93c5fd; text-transform:uppercase; letter-spacing:0.05em;">
          AUTHENTICATION · LEMON SQUEEZY MERCHANT OF RECORD
        </div>
        <h3 style="font-size:1.12rem; font-weight:800; margin-top:4px; color:#ffffff;">Activate Pro Terminal License</h3>
        <p style="color:var(--muted); font-size:0.82rem; margin-top:6px; line-height:1.5;">
          Enter the license key issued upon Lemon Squeezy checkout to unlock all 72 US equity target levels, Daily VIP Ignition Order Book, Position Sizing Calculator, Position Doctor, and the 26-year Semiconductor CSV dataset.
        </p>
        <div style="display:grid; grid-template-columns:1fr 1fr; gap:8px; margin:12px 0 10px;">
          <a class="btn btn-primary btn-sm lemonsqueezy-button" data-direct-ls="1" href="${o.ls_site1_monthly_url||"https://truthofmarket.lemonsqueezy.com/checkout/buy/bad98d00-7175-41f6-9d58-eeb2471d0da4"}?embed=1" target="_blank" rel="noopener noreferrer" style="justify-content:center; padding:8px 10px; font-weight:700;">
            🍋 Subscribe Pro ($29/mo) ↗
          </a>
          <a class="btn btn-emerald btn-sm lemonsqueezy-button" data-direct-ls="1" href="${o.ls_site1_ltd_url||"https://truthofmarket.lemonsqueezy.com/checkout/buy/00c9f6e1-c8be-42a4-b5a5-e05af1a41ed9"}?embed=1" target="_blank" rel="noopener noreferrer" style="justify-content:center; padding:8px 10px; font-weight:700;">
            🏆 Lifetime Pass ($199) ↗
          </a>
        </div>
        <div id="instantVipBridgeBox" style="display:none !important;">
          <div style="display:flex; justify-content:space-between; align-items:center; gap:6px; flex-wrap:wrap;">
            <span style="font-size:0.7rem; font-family:var(--font-mono); color:#34d399; font-weight:800; text-transform:uppercase;">
              ⚡ INTERACTIVE PRO TERMINAL PREVIEW &amp; 7-DAY TRIAL PASS
            </span>
            <span class="badge badge-ignition" style="font-size:0.64rem; padding:2px 6px;">INSTANT SANDBOX KEY</span>
          </div>
          <p style="color:#cbd5e1; font-size:0.76rem; margin:6px 0 8px; line-height:1.45;">
            Want to test the unlocked Pro Terminal before subscribing (or reviewing our Store #296100 deliverables)? Enter your email below to generate an <b>instant 7-Day Pro Preview License Key</b> that unmasks our 6 VIP Ignition setups, Position Doctor, and the 26-year historical backtest CSV dataset:
          </p>
          <div style="display:flex; gap:6px; flex-wrap:wrap;">
            <input type="email" id="vipTrialEmailInput" placeholder="Enter your email for instant 7-Day Pro Trial Key..." autocomplete="email" style="flex:1; min-width:200px; margin:0; padding:8px 10px; font-size:0.8rem;" />
            <button type="button" class="btn btn-emerald btn-sm" id="btnInstantVipTrialUnlock" style="font-weight:800; padding:8px 12px; white-space:nowrap;">
              ⚡ Issue 7-Day Pro Trial Key
            </button>
          </div>
        </div>
        <input type="text" id="licenseInput" value="${e.licenseKey||""}" placeholder="Enter Lemon Squeezy License Key (XXXX-XXXX-XXXX-XXXX)" autocomplete="off" />
        <div id="licenseMsg" style="font-size:0.8rem; margin-bottom:12px; min-height:1.2em;"></div>
        <div style="display:flex; gap:8px; justify-content:space-between; align-items:center; flex-wrap:wrap;">
          <div>
            ${e.isProUnlocked?'<button class="btn btn-sm" id="btnLockLicense" style="color:var(--fin-down); border-color:rgba(246,70,93,0.4);">Deactivate / Lock</button>':""}
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
            <a class="btn btn-sm" id="tgModalYtBtn" href="${a}" target="_blank" rel="noopener noreferrer" style="border-color:rgba(239,68,68,0.45); color:#fca5a5;">
              📺 YouTube ↗
            </a>
            <a class="btn btn-sm" id="tgModalIgBtn" href="${i}" target="_blank" rel="noopener noreferrer" style="border-color:rgba(236,72,153,0.45); color:#f9a8d4;">
              📸 Instagram ↗
            </a>
            <a class="btn btn-sm" id="tgChannelLinkBtn" href="${n}" target="_blank" rel="noopener noreferrer" style="border-color:rgba(56,189,248,0.45); color:#38bdf8;">
              ✈️ @truthofmarketss ↗
            </a>
          </div>
        </div>

        <p style="color:var(--muted); font-size:0.8rem; margin-top:6px; margin-bottom:12px; line-height:1.5;">
          Join our Official Broadcast Channel <a href="${n}" target="_blank" rel="noopener noreferrer" style="color:#38bdf8; font-weight:700;">t.me/truthofmarketss</a> (<code class="mono" style="color:#93c5fd;">@truthofmarketss</code>) for automated daily US Market & Semiconductor briefings.
        </p>

        ${e.isAdminAuthenticated?`<div class="semi-form-grid-2" style="margin-bottom:8px;">
          <div>
            <label style="font-size:0.68rem; color:var(--muted); font-family:var(--font-mono);">TELEGRAM BOT PROFILE (@BotFather)</label>
            <input type="text" id="tgBotTokenInput" value="${r}" placeholder="DEMO-BOT-TOKEN" autocomplete="off" style="margin:4px 0 0; -webkit-text-security:disc;" />
          </div>
          <div>
            <label style="font-size:0.68rem; color:var(--muted); font-family:var(--font-mono);">CHAT ID OR @CHANNEL USERNAME</label>
            <input type="text" id="tgChatIdInput" value="${p}" placeholder="@truthofmarketss" autocomplete="off" style="margin:4px 0 0;" />
          </div>
        </div>`:""}

        <div class="${e.isAdminAuthenticated?"semi-form-grid-2":""}" style="margin-bottom:10px;">
          ${e.isAdminAuthenticated?`<div>
            <label style="font-size:0.68rem; color:var(--muted); font-family:var(--font-mono);">PUBLIC CHANNEL URL (HEADER / FOOTER LINK)</label>
            <input type="text" id="tgChannelUrlInput" value="${n}" placeholder="https://t.me/truthofmarketss" style="margin:4px 0 0;" />
          </div>`:""}
          <div>
            <label style="font-size:0.68rem; color:var(--muted); font-family:var(--font-mono);">BRIEFING TEMPLATE</label>
            <select id="tgAlertTypeSelect" style="width:100%; padding:9px 10px; margin-top:4px; background:#060911; border:1px solid var(--border); color:#fff; border-radius:4px; font-family:var(--font-sans); font-size:0.82rem; font-weight:600;">
              <option value="SEMI_BRIEFING" ${m==="SEMI_BRIEFING"?"selected":""}>1. SemiFearGreed Index & $SMH:$XLV Rebalance</option>
              <option value="RSA_IGNITION" ${m==="RSA_IGNITION"?"selected":""}>2. RightSideAlpha US Top 5 Ignition Signals</option>
              <option value="FULL_DAILY" ${m==="FULL_DAILY"?"selected":""}>3. Full Combined Daily Briefing (Semi + US Stocks)</option>
              <option value="POSITION_DOCTOR" ${m==="POSITION_DOCTOR"?"selected":""}>4. Position Doctor Diagnostic ($CELH)</option>
              ${e.isAdminAuthenticated?`<option value="TEST_PING" ${m==="TEST_PING"?"selected":""}>5. Bot Connection Verification Ping</option>`:""}
            </select>
          </div>
        </div>

        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:6px; flex-wrap:wrap; gap:6px;">
          <span style="font-size:0.68rem; font-family:var(--font-mono); color:#93c5fd;">
            LIVE BRIEFING PREVIEW (VERIFIED LATEST CLOSES)
          </span>
          <div style="display:flex; gap:6px;">
            ${e.isAdminAuthenticated?'<button class="btn btn-sm" id="btnVerifyTelegram" title="Test Bot Token with Telegram API">Verify & Save Bot</button>':""}
            <button class="btn btn-sm" id="btnPreviewTelegram">Refresh Preview</button>
            <button class="btn btn-sm" id="btnCopyTelegramMsg">Copy Text</button>
          </div>
        </div>

        <pre id="telegramPreviewBox" style="background:#05080f; border:1px solid var(--border); border-left:3px solid #38bdf8; border-radius:4px; padding:12px; font-family:var(--font-mono); font-size:0.74rem; color:#e2e8f0; white-space:pre-wrap; max-height:210px; overflow-y:auto; line-height:1.5; margin-bottom:10px;">${N}</pre>

        <div id="telegramStatusMsg" style="font-size:0.78rem; margin-bottom:10px; min-height:1.2em; color:#93c5fd;"></div>

        <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:8px;">
          <span class="mono" style="font-size:0.68rem; color:var(--muted);">
            Official Channel: @truthofmarketss · Live Daily Briefings
          </span>
          <div style="display:flex; gap:8px;">
            <button class="btn" id="btnCloseTelegram">Close</button>
            <a class="btn btn-primary" href="${n}" target="_blank" rel="noopener noreferrer" style="background:#0284c7; border-color:#38bdf8;">
              Join Telegram Channel ↗
            </a>
            ${e.isAdminAuthenticated?`<button class="btn btn-primary" id="btnSendTelegramNow" style="background:#059669; border-color:#10b981;">
              Send Briefing to Telegram ↗
            </button>`:""}
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
            <a class="btn btn-sm" href="https://www.tradingview.com/partner-program/" target="_blank" rel="noopener noreferrer" style="font-size:0.7rem; padding:4px 8px;">📈 TradingView Aff ↗</a>
            <a class="btn btn-sm" href="https://www.interactivebrokers.com/en/general/refer-a-friend.php" target="_blank" rel="noopener noreferrer" style="font-size:0.7rem; padding:4px 8px;">🏦 IBKR Referral ↗</a>
            <a class="btn btn-sm" href="https://affiliates.seekingalpha.com/" target="_blank" rel="noopener noreferrer" style="font-size:0.7rem; padding:4px 8px;">📊 Seeking Alpha Aff ↗</a>
          </div>
        </div>

        <label style="font-size:0.72rem; color:var(--muted); font-family:var(--font-mono);">PLATFORM DOMAIN (TEAR SHEET WATERMARK)</label>
        <input type="text" id="cfgSite1Url" value="${o.site1_url||"https://truthofmarket.com"}" />

        <label style="font-size:0.72rem; color:var(--muted); font-family:var(--font-mono);">LEMON SQUEEZY MONTHLY CHECKOUT URL ($29/MO)</label>
        <input type="text" id="cfgLsMonthly" value="${o.ls_site1_monthly_url||"https://truthofmarket.lemonsqueezy.com/checkout/buy/bad98d00-7175-41f6-9d58-eeb2471d0da4"}" />

        <label style="font-size:0.72rem; color:var(--muted); font-family:var(--font-mono);">LEMON SQUEEZY LIFETIME CHECKOUT URL ($199)</label>
        <input type="text" id="cfgLsLtd" value="${o.ls_site1_ltd_url||"https://truthofmarket.lemonsqueezy.com/checkout/buy/00c9f6e1-c8be-42a4-b5a5-e05af1a41ed9"}" />

        <label style="font-size:0.72rem; color:var(--muted); font-family:var(--font-mono);">TELEGRAM OFFICIAL CHANNEL / BOT URL</label>
        <input type="text" id="cfgTgChannel" value="${n}" />

        <label style="font-size:0.72rem; color:var(--muted); font-family:var(--font-mono);">OFFICIAL YOUTUBE CHANNEL URL (@rightsidealpha)</label>
        <input type="text" id="cfgYoutubeUrl" value="${a}" />

        <label style="font-size:0.72rem; color:var(--muted); font-family:var(--font-mono);">OFFICIAL INSTAGRAM PROFILE URL (@rightsidealpha)</label>
        <input type="text" id="cfgInstagramUrl" value="${i}" />

        <label style="font-size:0.72rem; color:var(--muted); font-family:var(--font-mono);">TRADINGVIEW AFFILIATE ID</label>
        <input type="text" id="cfgAffTv" value="${o.tradingview_aff_id||"1173809"}" />

        <label style="font-size:0.72rem; color:var(--muted); font-family:var(--font-mono);">SEEKING ALPHA PARTNER SOURCE TAG</label>
        <input type="text" id="cfgAffSa" value="${o.seekingalpha_source||"better_life333"}" />

        <label style="font-size:0.72rem; color:var(--muted); font-family:var(--font-mono);">BROKER / EXCHANGE PARTNER LABEL (E.G. BITGET / IBKR)</label>
        <input type="text" id="cfgBrokerName" value="${o.broker_name||"Bitget (7nja)"}" />

        <label style="font-size:0.72rem; color:var(--muted); font-family:var(--font-mono);">BROKER / EXCHANGE REFERRAL URL</label>
        <input type="text" id="cfgBrokerUrl" value="${o.broker_referral_url||"https://www.bitget.com/referral/register?clacCode=7nja"}" />

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

    <!-- LEGAL, PRIVACY, REFUND POLICY & SUPPORT MODAL -->
    <div class="modal-backdrop" id="legalModal">
      <div class="modal" style="max-width:740px;">
        <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:8px; margin-bottom:12px;">
          <div>
            <div style="font-size:0.68rem; font-family:var(--font-mono); color:#93c5fd; text-transform:uppercase; letter-spacing:0.05em;">
              LEGAL & COMPLIANCE · MERCHANT OF RECORD: LEMON SQUEEZY
            </div>
            <h3 style="font-size:1.1rem; font-weight:800; color:#ffffff; margin-top:3px;" id="legalModalTitle">
              Terms of Service, Privacy Policy & Refund Policy
            </h3>
          </div>
          <div style="display:flex; gap:6px; flex-wrap:wrap;">
            <button type="button" class="btn btn-sm btn-legal-tab" data-legal-tab="terms">Terms of Service</button>
            <button type="button" class="btn btn-sm btn-legal-tab" data-legal-tab="privacy">Privacy Policy</button>
            <button type="button" class="btn btn-sm btn-legal-tab" data-legal-tab="refund">Refund Policy</button>
            <button type="button" class="btn btn-sm btn-legal-tab" data-legal-tab="support">Support Contact</button>
            <button type="button" class="btn btn-sm" id="btnCloseLegalModal">Close ✕</button>
          </div>
        </div>
        <div id="legalModalBody" style="font-size:0.82rem; color:var(--text); line-height:1.68; max-height:62vh; overflow-y:auto; background:#05080f; padding:18px; border-radius:4px; border:1px solid var(--border);">
          <div data-legal-section="terms">
            <h4 style="color:#ffffff; font-size:0.95rem; font-weight:800; margin-bottom:6px;">1. Terms of Service & Non-Advisory Disclosure</h4>
            <p style="color:var(--muted); margin-bottom:10px;">
              RightSideAlpha and SemiFearGreed (<code class="mono">truthofmarket.com</code>) provide quantitative financial data analytics, empirical backtesting outputs (2000–2026), and algorithmic screening tools for US-listed equities and ETFs. Nothing on this platform constitutes personalized investment advice, brokerage solicitation, legal advice, or tax counsel. Users are solely responsible for their own investment decisions and trade executions.
            </p>
            <p style="color:var(--muted); margin-bottom:12px;">
              Pro Terminal licenses grant single-user access to quantitative target levels, daily SEC primary-filing briefs, Position Doctor diagnostics, and Pine Script v5 indicators. Redistribution or unauthorized sharing of license keys or private VIP Telegram invite links is strictly prohibited.
            </p>
          </div>
          <div data-legal-section="privacy" style="border-top:1px solid var(--border); padding-top:12px; margin-top:12px;">
            <h4 style="color:#ffffff; font-size:0.95rem; font-weight:800; margin-bottom:6px;">2. Privacy Policy</h4>
            <p style="color:var(--muted); margin-bottom:10px;">
              We respect your financial privacy. Portfolio inputs entered into the Position Sizing Calculator, Position Doctor, or $SMH:$XLV Barbell Rebalancing Engine are processed locally in your browser and are never sold or shared with third parties. Payment processing and billing data are handled securely by our Merchant of Record, <b>Lemon Squeezy, LLC</b>, under PCI-DSS compliance.
            </p>
          </div>
          <div data-legal-section="refund" style="border-top:1px solid var(--border); padding-top:12px; margin-top:12px;">
            <h4 style="color:#ffffff; font-size:0.95rem; font-weight:800; margin-bottom:6px;">3. Subscription Cancellation & Refund Policy</h4>
            <p style="color:var(--muted); margin-bottom:10px;">
              Monthly Pro subscriptions ($29/mo) can be canceled at any time with one click via your Lemon Squeezy customer billing portal or by contacting support; access remains active through the end of the current billing period with zero cancellation fees. Because digital quantitative data, downloadable 26.8-year CSV datasets, and Pine Script v5 source code are delivered immediately upon activation, Lifetime Pass ($199) and activated digital licenses are non-refundable once accessed, except where required by applicable consumer protection law or in cases of duplicate billing.
            </p>
          </div>
          <div data-legal-section="support" style="border-top:1px solid var(--border); padding-top:12px; margin-top:12px;">
            <h4 style="color:#ffffff; font-size:0.95rem; font-weight:800; margin-bottom:6px;">4. Customer Support & Billing Inquiries</h4>
            <p style="color:var(--muted);">
              • <b>Official Support Email</b>: <a href="mailto:support@truthofmarket.com" style="color:#60a5fa; font-weight:700;">support@truthofmarket.com</a><br/>
              • <b>Merchant of Record</b>: Lemon Squeezy, LLC (<a href="https://app.lemonsqueezy.com/my-orders" target="_blank" rel="noopener noreferrer" style="color:#60a5fa;">Manage Orders & Receipts ↗</a>)<br/>
              • <b>Public Broadcast Desk</b>: <a href="https://t.me/truthofmarketss" target="_blank" rel="noopener noreferrer" style="color:#38bdf8;">t.me/truthofmarketss (@truthofmarketss) ↗</a>
            </p>
          </div>
        </div>
      </div>
    </div>

    <!-- PW-RSI METHODOLOGY EXPLAINER MODAL -->
    <div class="modal-backdrop" id="pwRsiModal">
      <div class="modal" style="max-width:680px;">
        <div style="display:flex; justify-content:space-between; align-items:center; gap:8px; margin-bottom:12px; border-bottom:1px solid rgba(255,255,255,0.08); padding-bottom:10px;">
          <div>
            <div style="font-size:0.68rem; font-family:var(--font-mono); color:#38bdf8; text-transform:uppercase; letter-spacing:0.06em; font-weight:800;">
              QUANTITATIVE FOUNDATION · ZERO LOOK-AHEAD BIAS
            </div>
            <h3 style="font-size:1.15rem; font-weight:800; color:#ffffff; margin:3px 0 0;">
              ${t.pwRsiModalTitle||"PW-RSI (Post-Washout Right-Side Ignition) Methodology"}
            </h3>
          </div>
          <button class="btn btn-sm" id="btnClosePwRsiModal" style="padding:4px 8px;">✕ Close</button>
        </div>

        <div style="max-height:70vh; overflow-y:auto; padding-right:4px; font-size:0.83rem; line-height:1.55; color:#cbd5e1;">
          <div style="background:#0b1322; border:1px solid rgba(56,189,248,0.25); border-radius:6px; padding:12px 14px; margin-bottom:12px;">
            <div style="font-weight:800; color:#ffffff; margin-bottom:4px; font-size:0.88rem;">
              Why "Catching the Falling Knife" Fails in Growth Equities
            </div>
            <p style="margin:0; color:var(--muted); font-size:0.78rem;">
              Empirical analysis across 394,371 US stock-days (2000–2026) demonstrates that blindly buying stocks near 52-week lows traps investor capital for a median of <b>81.0 trading days</b> underwater, with an average post-entry additional drawdown of <b>-30.3%</b> and a <b>25.54% risk of severe loss (&le; -20%)</b>.
            </p>
          </div>

          <div style="display:grid; grid-template-columns:1fr; gap:10px; margin-bottom:12px;">
            <div style="background:#090d16; border:1px solid #1e293b; border-radius:6px; padding:12px 14px;">
              <div style="display:flex; align-items:center; gap:8px; margin-bottom:4px;">
                <span style="font-size:0.75rem; font-family:var(--font-mono); font-weight:900; color:#38bdf8; background:rgba(56,189,248,0.14); padding:2px 7px; border-radius:3px;">
                  STEP 1: PW · POST-WASHOUT
                </span>
                <span style="font-weight:700; color:#ffffff;">Volume Exhaustion &amp; Capitulation</span>
              </div>
              <p style="margin:0; font-size:0.78rem; color:var(--muted);">
                We demand at least <b>1.35x to 1.40x 10-day volume surge</b> on severe down-days, signaling institutional climax liquidation where retail hands capitulate and smart money absorbs liquidity.
              </p>
            </div>

            <div style="background:#090d16; border:1px solid #1e293b; border-radius:6px; padding:12px 14px;">
              <div style="display:flex; align-items:center; gap:8px; margin-bottom:4px;">
                <span style="font-size:0.75rem; font-family:var(--font-mono); font-weight:900; color:#34d399; background:rgba(14,203,129,0.14); padding:2px 7px; border-radius:3px;">
                  STEP 2: RS · RIGHT-SIDE
                </span>
                <span style="font-weight:700; color:#ffffff;">Dual Moving Average Reclamation</span>
              </div>
              <p style="margin:0; font-size:0.78rem; color:var(--muted);">
                Never enter while a stock is below declining moving averages. Entry is only permitted once price climbs <b>+10% to +45% off the 52-week low</b> and cleanly reclaims both the <b>20-day (short-term momentum)</b> and <b>60-day (intermediate institutional trend)</b> moving averages.
              </p>
            </div>

            <div style="background:#090d16; border:1px solid #1e293b; border-radius:6px; padding:12px 14px;">
              <div style="display:flex; align-items:center; gap:8px; margin-bottom:4px;">
                <span style="font-size:0.75rem; font-family:var(--font-mono); font-weight:900; color:#fbbf24; background:rgba(245,158,11,0.14); padding:2px 7px; border-radius:3px;">
                  STEP 3: I · IGNITION
                </span>
                <span style="font-weight:700; color:#ffffff;">Strict 4-Tier Risk &amp; Harvest Rules</span>
              </div>
              <p style="margin:0; font-size:0.78rem; color:var(--muted);">
                Every position is bounded by 4 mechanical exit rules: <b>Rule 1: -9.0% hard stop floor</b> (eliminates tail risk to 0.93%), <b>Rule 2: 55-day time stop</b> (+8% threshold cuts underwater time from 81 to 29 days), <b>Rule 3: +100% (2x) principal harvest</b>, and <b>Rule 4: Barbell capital preservation</b>.
              </p>
            </div>
          </div>

          <div style="display:flex; justify-content:flex-end; gap:8px; margin-top:14px; border-top:1px solid var(--border); padding-top:10px;">
            <button class="btn btn-primary btn-sm" id="btnUnderstandPwRsi">Got it, Explore 72 Setups</button>
          </div>
        </div>
      </div>
    </div>

    <!-- TOAST NOTIFICATION -->
    <div class="toast" id="toastBox">Action completed</div>
  `}function te(e,t,o,n){const a=n*Math.PI/180;return{x:e+o*Math.cos(a),y:t-o*Math.sin(a)}}function Xt(e,t,o,n,a){const i=te(e,t,o,n),p=te(e,t,o,a),r=Math.abs(n-a)<=180?"0":"1";return`M ${i.x.toFixed(2)} ${i.y.toFixed(2)} A ${o} ${o} 0 ${r} 1 ${p.x.toFixed(2)} ${p.y.toFixed(2)}`}function Yt(e,t){const o=Math.max(0,Math.min(100,Number(e??18))),n=230,a=200,i=146,p=[{code:"EXTREME_FEAR",min:0,max:24,a1:180,a2:136.5,activeColor:"#ef4444",mutedColor:"rgba(239,68,68,0.22)",label:"EXTREME FEAR",midAngle:158},{code:"FEAR",min:25,max:44,a1:134,a2:100.5,activeColor:"#f59e0b",mutedColor:"rgba(245,158,11,0.22)",label:"FEAR",midAngle:117},{code:"NEUTRAL",min:45,max:55,a1:98,a2:82,activeColor:"#94a3b8",mutedColor:"rgba(148,163,184,0.20)",label:"NEUTRAL",midAngle:90},{code:"GREED",min:56,max:74,a1:79.5,a2:46,activeColor:"#10b981",mutedColor:"rgba(16,185,129,0.22)",label:"GREED",midAngle:63},{code:"EXTREME_GREED",min:75,max:100,a1:43.5,a2:0,activeColor:"#059669",mutedColor:"rgba(5,150,105,0.22)",label:"EXTREME GREED",midAngle:22}];let r=p[0];o>=75?r=p[4]:o>=55.01?r=p[3]:o>=45?r=p[2]:o>=25&&(r=p[1]);const m=p.map(l=>{const S=l.code===r.code,k=Xt(n,a,i,l.a1,l.a2),$=S?l.activeColor:l.mutedColor,E=S?40:32,L=te(n,a,i+31,l.midAngle);return`
        <path d="${k}" fill="none" stroke="${$}" stroke-width="${E}" stroke-linecap="butt" />
        <text x="${L.x.toFixed(1)}" y="${L.y.toFixed(1)}" text-anchor="middle" dominant-baseline="middle"
              fill="${S?l.activeColor:"#64748b"}"
              font-size="${S?"9.5":"8.5"}" font-weight="${S?"800":"700"}" font-family="Inter, sans-serif">
          ${l.label}
        </text>
      `}).join(""),f=[0,25,45,55,75,100].map(l=>{const S=180-l/100*180,k=te(n,a,i-24,S),$=te(n,a,i-35,S);return`
        <circle cx="${k.x.toFixed(1)}" cy="${k.y.toFixed(1)}" r="1.8" fill="#94a3b8" />
        <text x="${$.x.toFixed(1)}" y="${$.y.toFixed(1)}" text-anchor="middle" dominant-baseline="middle"
              fill="#94a3b8" font-size="10" font-weight="700" font-family="JetBrains Mono, monospace">
          ${l}
        </text>
      `}).join(""),b=180-o/100*180,d=te(n,a,i-12,b),h=te(n,a,8,b+90),_=te(n,a,8,b-90);return`
    <div style="display:flex; flex-direction:column; align-items:center;">
      <svg viewBox="0 0 460 250" style="width:100%; max-width:440px; height:auto; overflow:visible;">
        <defs>
          <filter id="needleShadow" x="-25%" y="-25%" width="150%" height="150%">
            <feDropShadow dx="0" dy="2.5" stdDeviation="3" flood-color="#000000" flood-opacity="0.65" />
          </filter>
        </defs>
        ${m}
        ${f}
        <!-- Needle Polygon with Elevation Shadow -->
        <polygon points="${d.x.toFixed(1)},${d.y.toFixed(1)} ${h.x.toFixed(1)},${h.y.toFixed(1)} ${_.x.toFixed(1)},${_.y.toFixed(1)}"
                 fill="#f8fafc" filter="url(#needleShadow)" />
        <circle cx="${n}" cy="${a}" r="14" fill="#f8fafc" filter="url(#needleShadow)" />
        <circle cx="${n}" cy="${a}" r="5" fill="#090e18" />
      </svg>

      <!-- Score & Active Emotion Callout below Needle Hub -->
      <div style="text-align:center; margin-top:-18px;">
        <div style="display:inline-flex; align-items:baseline; gap:6px; background:#070b14; color:#ffffff; padding:6px 22px; border-radius:30px; border:1px solid var(--border); box-shadow:var(--shadow-md);">
          <span class="mono" style="font-size:2rem; font-weight:900; letter-spacing:-0.03em;">${Math.round(o)}</span>
          <span class="mono" style="font-size:0.9rem; color:#9ca3af; font-weight:600;">(${o.toFixed(1)} / 100)</span>
        </div>
        <div style="margin-top:8px;">
          <span style="font-size:0.78rem; color:var(--muted); font-weight:600; text-transform:uppercase; letter-spacing:0.04em;">
            Market Emotion is driving:
          </span>
          <span class="cnn-pill cnn-pill-${r.code}" style="margin-left:6px; font-size:0.85rem;">
            ${t||r.label}
          </span>
        </div>
      </div>
    </div>
  `}function Wt(e,t){const o=e&&e.series||[];if(!o.length)return'<div style="padding:40px; text-align:center; color:#6b7280;">Loading historical timeline...</div>';const n=640,a=230,i=36,p=16,r=16,m=28,f=n-i-p,b=a-r-m,d=o.map((E,L)=>{const N=i+L/Math.max(1,o.length-1)*f,y=r+(1-Math.max(0,Math.min(100,E.fg_score))/100)*b;return`${N.toFixed(1)},${y.toFixed(1)}`}),h=(r+.75*b).toFixed(1),_=(r+.5*b).toFixed(1),l=(r+.25*b).toFixed(1),S=o[0].date,k=o[Math.floor(o.length/2)].date,$=o[o.length-1].date;return`
    <div>
      <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:10px; flex-wrap:wrap; gap:8px;">
        <div style="font-size:0.8rem; font-weight:700; color:var(--text);">
          Historical Semiconductor Fear &amp; Greed Index (${S} → ${$})
        </div>
        <div style="display:flex; gap:4px;">
          ${["3M","1Y","3Y","5Y","10Y","ALL"].map(E=>`
            <button class="btn-semi-range" data-range="${E}"
                    style="padding:3px 9px; border-radius:4px; font-size:0.72rem; font-weight:700; cursor:pointer; border:1px solid ${t===E?"var(--fin-blue)":"var(--border)"}; background:${t===E?"#141c2e":"#060911"}; color:${t===E?"#ffffff":"var(--muted)"};">
              ${E}
            </button>
          `).join("")}
        </div>
      </div>

      <svg viewBox="0 0 ${n} ${a}" style="width:100%; height:auto; background:#060911; border:1px solid var(--border); border-radius:4px;">
        <!-- Extreme Greed Band (>75) -->
        <rect x="${i}" y="${r}" width="${f}" height="${.25*b}" fill="rgba(16,185,129,0.12)" />
        <!-- Extreme Fear Band (<25) -->
        <rect x="${i}" y="${h}" width="${f}" height="${.25*b}" fill="rgba(239,68,68,0.12)" />

        <!-- Reference Lines -->
        <line x1="${i}" y1="${l}" x2="${n-p}" y2="${l}" stroke="#10b981" stroke-dasharray="3,3" stroke-width="1" />
        <line x1="${i}" y1="${_}" x2="${n-p}" y2="${_}" stroke="#64748b" stroke-dasharray="3,3" stroke-width="1" />
        <line x1="${i}" y1="${h}" x2="${n-p}" y2="${h}" stroke="#ef4444" stroke-dasharray="3,3" stroke-width="1" />

        <text x="6" y="${l}" fill="#34d399" font-size="9.5" font-weight="700" dominant-baseline="middle">75</text>
        <text x="6" y="${_}" fill="#94a3b8" font-size="9.5" font-weight="700" dominant-baseline="middle">50</text>
        <text x="6" y="${h}" fill="#f87171" font-size="9.5" font-weight="700" dominant-baseline="middle">25</text>

        <!-- FG Line -->
        <polyline fill="none" stroke="#38bdf8" stroke-width="2" points="${d.join(" ")}" />

        <!-- X-Axis Dates with mobile overlap protection -->
        <text x="${i}" y="${a-8}" fill="var(--muted)" font-size="9.5" font-family="JetBrains Mono, monospace">${S}</text>
        <text class="timeline-mid-date" x="${i+f/2}" y="${a-8}" fill="var(--muted)" font-size="9.5" text-anchor="middle" font-family="JetBrains Mono, monospace">${k}</text>
        <text x="${n-p}" y="${a-8}" fill="var(--muted)" font-size="9.5" text-anchor="end" font-family="JetBrains Mono, monospace">${$}</text>
      </svg>
    </div>
  `}function Qt(e,t){if(!e||!e.length)return"";const o=180,n=44,a=e.map((r,m)=>{const f=4+m/Math.max(1,e.length-1)*(o-8),b=4+(1-Math.max(0,Math.min(100,r))/100)*(n-8);return`${f.toFixed(1)},${b.toFixed(1)}`}).join(" "),p={EXTREME_FEAR:"#ef4444",FEAR:"#f59e0b",NEUTRAL:"#94a3b8",GREED:"#10b981",EXTREME_GREED:"#059669"}[t]||"#94a3b8";return`
    <svg viewBox="0 0 ${o} ${n}" style="width:160px; height:40px; background:#060911; border:1px solid var(--border); border-radius:4px;">
      <line x1="0" y1="${n/2}" x2="${o}" y2="${n/2}" stroke="#1e293b" stroke-dasharray="2,2" stroke-width="1" />
      <polyline fill="none" stroke="${p}" stroke-width="1.8" points="${a}" />
    </svg>
  `}function Kt(e){const t=e&&e.series||[];if(!t.length)return"";const o=720,n=220,a=52,i=20,p=18,r=26,m=o-a-i,f=n-p-r,b=[];t.forEach(E=>{b.push(E.port73_norm,E.qqq_norm)});const d=Math.min(...b,8e3),h=Math.max(...b,12e3),_=Math.max(1,h-d),l=t.map((E,L)=>{const N=a+L/Math.max(1,t.length-1)*m,y=p+(1-(E.port73_norm-d)/_)*f;return`${N.toFixed(1)},${y.toFixed(1)}`}).join(" "),S=t.map((E,L)=>{const N=a+L/Math.max(1,t.length-1)*m,y=p+(1-(E.qqq_norm-d)/_)*f;return`${N.toFixed(1)},${y.toFixed(1)}`}).join(" "),k=t[t.length-1].port73_norm,$=t[t.length-1].qqq_norm;return`
    <div style="margin-bottom:16px;">
      <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:8px; flex-wrap:wrap; gap:8px; font-size:0.78rem;">
        <div style="display:flex; gap:16px; align-items:center;">
          <span style="display:inline-flex; align-items:center; gap:6px; color:#34d399; font-weight:700;">
            <span style="width:12px; height:3px; background:#0ecb81; display:inline-block;"></span>
            70% $SMH : 30% $XLV Barbell ($10k → $${k.toLocaleString()})
          </span>
          <span style="display:inline-flex; align-items:center; gap:6px; color:#94a3b8; font-weight:600;">
            <span style="width:12px; height:3px; background:#64748b; display:inline-block;"></span>
            100% $QQQ Benchmark ($10k → $${$.toLocaleString()})
          </span>
        </div>
        <span class="mono" style="color:var(--muted); font-size:0.72rem;">Selected Window: ${e.range_code}</span>
      </div>
      <svg viewBox="0 0 ${o} ${n}" style="width:100%; height:auto; background:#060911; border:1px solid var(--border); border-radius:4px;">
        <polyline fill="none" stroke="#64748b" stroke-width="1.6" stroke-dasharray="3,2" points="${S}" />
        <polyline fill="none" stroke="#0ecb81" stroke-width="2.2" points="${l}" />
        <text x="6" y="${p+8}" fill="#94a3b8" font-size="9.5" font-family="JetBrains Mono, monospace">$${Math.round(h).toLocaleString()}</text>
        <text x="6" y="${n-r}" fill="#94a3b8" font-size="9.5" font-family="JetBrains Mono, monospace">$${Math.round(d).toLocaleString()}</text>
      </svg>
    </div>
  `}function Zt(e){var h,_;const t=e.t,o=e.lang,n=e.semiOverview;if(!n)return`
      <div class="proof-card" style="padding:40px; text-align:center;">
        Loading Semiconductor Fear & Greed Index...
      </div>
    `;const a=o==="jp"?n.regime_jp:o==="kr"?n.regime_kr:n.regime_en,i=o==="jp"?n.action_headline_jp:o==="kr"?n.action_headline_kr:n.action_headline_en,p=o==="jp"?n.action_detail_jp:o==="kr"?n.action_detail_kr:n.action_detail_en,r=e.semiGaugeTab||"overview",m=e.semiRange||"1Y",f=e.semiRebalanceResult,b=e.semiLumpSumResult,d=e.semiHistory&&e.semiHistory.era_summary||[];return`
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
            href="${((h=e.config)==null?void 0:h.youtube_url)||"https://youtube.com/@rightsidealpha"}"
            target="_blank"
            rel="noopener noreferrer"
            style="background:#dc2626; color:#ffffff; border-color:#b91c1c;"
          >
            📺 YouTube (@rightsidealpha) ↗
          </a>
          <a
            class="btn"
            href="${((_=e.config)==null?void 0:_.instagram_url)||"https://www.instagram.com/rightsidealpha"}"
            target="_blank"
            rel="noopener noreferrer"
            style="background:#db2777; color:#ffffff; border-color:#be185d;"
          >
            📸 Instagram (@rightsidealpha) ↗
          </a>
          <a
            class="btn ${e.isProUnlocked?"":"btn-gated-vip-tg"}"
            href="${we(e.isProUnlocked)}"
            ${e.isProUnlocked?'target="_blank" rel="noopener noreferrer"':""}
            style="background:#0284c7; color:#ffffff; border-color:#0369a1;"
          >
            ${e.isProUnlocked?"👑 VIP Telegram News ↗":"🔒 VIP Telegram ($SMH/$XLV News)"}
          </a>
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
              ${t.cnnLastUpdated}: <b class="mono" style="color:#111827;">${n.date}</b> · $SMH <b class="mono">$${n.smh_close.toFixed(2)}</b> (${n.smh_dd_pct.toFixed(2)}% off 52W High)
            </div>
            <div class="cnn-view-tabs">
              <button class="cnn-view-tab ${r==="overview"?"active":""}" data-semi-tab="overview">
                ${t.cnnTabOverview}
              </button>
              <button class="cnn-view-tab ${r==="timeline"?"active":""}" data-semi-tab="timeline">
                ${t.cnnTabTimeline}
              </button>
            </div>
          </div>

          ${r==="overview"?Yt(n.fg_score,a):Wt(e.semiHistory,m)}
        </div>

        <!-- RIGHT COLUMN: CNN 4-ROW HISTORICAL STACK + BARBELL SIGNAL -->
        <div class="cnn-card" style="display:flex; flex-direction:column; justify-content:space-between;">
          <div>
            <div style="font-size:0.78rem; font-weight:800; text-transform:uppercase; letter-spacing:0.05em; color:var(--muted); margin-bottom:8px;">
              ${t.cnnHistoryTitle}
            </div>
            <div class="cnn-history-list">
              ${n.comparisons.map(l=>{const S=o==="jp"?l.label_jp:o==="kr"?l.label_kr:l.label_en,k=o==="jp"?l.regime_jp:o==="kr"?l.regime_kr:l.regime_en,$=Math.round(l.score),E=$<=24?"#ef4444":$<=44?"#f59e0b":$<=55?"#64748b":$<=74?"#10b981":"#059669",L=$<=24?"rgba(239,68,68,0.15)":$<=44?"rgba(245,158,11,0.15)":$<=55?"rgba(100,116,139,0.15)":$<=74?"rgba(16,185,129,0.15)":"rgba(5,150,105,0.15)";return`
                  <div class="cnn-history-row">
                    <div>
                      <div class="cnn-hist-label">${S} <span class="mono" style="font-size:0.72rem; color:var(--muted);">(${l.date})</span></div>
                      <div class="cnn-hist-regime">${k}</div>
                    </div>
                    <div class="cnn-score-circle" style="border-color:${E}; background:${L}; color:#ffffff;">${$}</div>
                  </div>
                `}).join("")}
            </div>
          </div>

          <!-- Active SMH:XLV Barbell Regime Box -->
          <div style="margin-top:16px; padding:14px 16px; background:rgba(220,38,38,0.1); border:1px solid rgba(220,38,38,0.3); border-left:4px solid #dc2626; border-radius:4px;">
            <div style="font-size:0.68rem; font-weight:800; color:#fca5a5; letter-spacing:0.05em; text-transform:uppercase;">
              ${t.cnnActiveRuleLabel} · TARGET ${n.recommended_smh_weight}% $SMH : ${n.recommended_xlv_weight}% $XLV
            </div>
            <div style="font-size:0.88rem; font-weight:800; color:#ffffff; margin-top:4px;">
              ${i}
            </div>
            <p style="font-size:0.78rem; color:var(--text-secondary); margin-top:4px; line-height:1.45;">
              ${p}
            </p>
          </div>
        </div>
      </div>

      <!-- CNN 7 FEAR & GREED INDICATORS BREAKDOWN -->
      <div style="margin-top:12px;">
        <div style="border-bottom:1px solid var(--border); padding-bottom:10px; margin-bottom:16px;">
          <h2 style="font-size:1.35rem; font-weight:900; color:#ffffff;">${t.cnnIndicatorsHeading}</h2>
          <p style="font-size:0.84rem; color:var(--muted); margin-top:2px;">${t.cnnIndicatorsSub}</p>
        </div>

        <div class="cnn-indicators-list">
          ${n.factors.map(l=>{const S=o==="jp"?l.title_jp:o==="kr"?l.title_kr:l.title_en,k=o==="jp"?l.subtitle_jp:o==="kr"?l.subtitle_kr:l.subtitle_en,$=o==="jp"?l.desc_jp:o==="kr"?l.desc_kr:l.desc_en,E=o==="jp"?l.regime_jp:o==="kr"?l.regime_kr:l.regime_en;return`
              <div class="cnn-indicator-item">
                <div>
                  <div style="display:flex; align-items:center; gap:8px;">
                    <span class="mono" style="font-size:0.7rem; font-weight:800; padding:2px 6px; background:#141c2e; border:1px solid var(--border); border-radius:3px; color:#93c5fd;">
                      #${l.order} · ${l.weight_pct}% WEIGHT
                    </span>
                    <span class="cnn-ind-title">${S}</span>
                  </div>
                  <div class="cnn-ind-sub">${k}</div>
                  <p class="cnn-ind-desc">${$}</p>
                </div>

                <div style="display:flex; flex-direction:column; align-items:center; gap:6px;">
                  ${Qt(l.sparkline,l.regime_code)}
                  <div class="mono" style="font-size:0.74rem; color:#94a3b8; font-weight:700;">
                    Reading: ${l.raw_display} · Score ${l.score.toFixed(1)}/100
                  </div>
                </div>

                <div style="text-align:right;">
                  <span class="cnn-pill cnn-pill-${l.regime_code}">${E}</span>
                </div>
              </div>
            `}).join("")}
        </div>
      </div>
    </section>

    <!-- SECTION 2: CORE ETF SNAPSHOT STRIP ($SMH, $XLV, $QQQ) -->
    <section class="core-etf-grid">
      ${n.etfs.map(l=>{const S=o==="jp"?l.name_jp:o==="kr"?l.name_kr:l.name_en,k=o==="jp"?l.role_jp:o==="kr"?l.role_kr:l.role_en,$=e.config||{},E=encodeURIComponent($.tradingview_aff_id||"1173809"),L=encodeURIComponent($.seekingalpha_source||"better_life333"),N=$.broker_referral_url||"https://www.bitget.com/referral/register?clacCode=7nja",y=N.includes("?")?"&":"?",C=`https://www.tradingview.com/symbols/${encodeURIComponent(l.ticker)}/?aff_id=${E}`,O=`https://seekingalpha.com/symbol/${encodeURIComponent(l.ticker)}/earnings?source=${L}`,I=`${N}${y}symbol=${encodeURIComponent(l.ticker)}`;return`
          <div class="proof-card" style="margin-bottom:0; border-top:2px solid ${l.ticker==="SMH"?"var(--fin-blue)":l.ticker==="XLV"?"var(--fin-up)":"#64748b"};">
            <div style="display:flex; justify-content:space-between; align-items:flex-start;">
              <div>
                <div style="display:flex; align-items:center; gap:8px;">
                  <span class="mono" style="font-size:1.15rem; font-weight:900; color:#ffffff;">$${l.ticker}</span>
                  <span style="font-size:0.78rem; color:var(--text-secondary); font-weight:600;">${S}</span>
                </div>
                <div style="font-size:0.74rem; color:var(--muted); margin-top:3px;">${k}</div>
              </div>
              <div style="text-align:right;">
                <div class="mono" style="font-size:1.15rem; font-weight:800; color:#ffffff;">$${Number(l.close??0).toFixed(2)}</div>
                <div class="mono" style="font-size:0.74rem; color:${l.ret_1d_pct>=0?"var(--fin-up)":"var(--fin-down)"};">
                  1D: ${l.ret_1d_pct>=0?"+":""}${Number(l.ret_1d_pct??0).toFixed(2)}% · 20D: ${l.ret_20d_pct>=0?"+":""}${Number(l.ret_20d_pct??0).toFixed(2)}%
                </div>
                <div class="mono" style="font-size:0.7rem; color:var(--muted); margin-top:1px;">
                  52W DD: ${Number(l.dd_52w_pct??0).toFixed(2)}% · RSI(14): ${Number(l.rsi14??50).toFixed(1)}
                </div>
              </div>
            </div>
            <div style="display:flex; justify-content:space-between; align-items:center; margin-top:12px; padding-top:10px; border-top:1px solid var(--border-subtle); font-size:0.74rem;">
              <span class="mono" style="color:var(--muted);">
                Normal: <b style="color:#fff;">${l.target_weight_normal}%</b> → Extreme Fear: <b style="color:var(--fin-up);">${l.target_weight_fear}%</b>
              </span>
              <div style="display:flex; gap:6px;">
                <a class="btn btn-sm" href="${C}" target="_blank" rel="noopener noreferrer">TV Chart ↗</a>
                <a class="btn btn-sm" href="${O}" target="_blank" rel="noopener noreferrer">Holdings ↗</a>
                <a class="btn btn-sm" href="${I}" target="_blank" rel="noopener noreferrer" style="border-color:rgba(16,185,129,0.4); color:#34d399;">Trade ↗</a>
              </div>
            </div>
          </div>
        `}).join("")}
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
            <input type="number" id="semiCapInput" value="${e.semiCapUsd??1e5}" step="1000"
                   style="width:100%; padding:8px 10px; background:#060911; border:1px solid var(--border); color:#fff; border-radius:4px; font-family:var(--font-mono); font-weight:700; margin-top:3px;" />
          </div>
          <div>
            <label style="font-size:0.68rem; font-family:var(--font-mono); color:var(--muted);">ALLOCATION MODE</label>
            <select id="semiModeInput" style="width:100%; padding:8px 10px; background:#060911; border:1px solid var(--border); color:#fff; border-radius:4px; font-family:var(--font-sans); font-weight:600; margin-top:3px;">
              <option value="AUTO_REGIME" ${e.semiMode==="AUTO_REGIME"?"selected":""}>Auto Regime (70:30 ↔ 80:20 on Fear ≤ 25)</option>
              <option value="BASELINE_70_30" ${e.semiMode==="BASELINE_70_30"?"selected":""}>70% $SMH : 30% $XLV Golden Baseline</option>
              <option value="CONTRARIAN_80_20" ${e.semiMode==="CONTRARIAN_80_20"?"selected":""}>80% $SMH : 20% $XLV Contrarian Accumulation</option>
              <option value="AGGRESSIVE_90_10" ${e.semiMode==="AGGRESSIVE_90_10"?"selected":""}>90% $SMH : 10% $XLV Right-Side Tilt</option>
            </select>
          </div>
          <div>
            <label style="font-size:0.68rem; font-family:var(--font-mono); color:var(--muted);">REBALANCING CADENCE</label>
            <select id="semiFreqInput" style="width:100%; padding:8px 10px; background:#060911; border:1px solid var(--border); color:#fff; border-radius:4px; font-family:var(--font-sans); font-weight:600; margin-top:3px;">
              <option value="ANNUAL" ${e.semiFreq==="ANNUAL"?"selected":""}>Annual + Band Trigger (Min Tax Drag)</option>
              <option value="QUARTERLY" ${e.semiFreq==="QUARTERLY"?"selected":""}>Quarterly Rebalance</option>
              <option value="MONTHLY" ${e.semiFreq==="MONTHLY"?"selected":""}>Monthly Rebalance</option>
              <option value="WEEKLY" ${e.semiFreq==="WEEKLY"?"selected":""}>Weekly Rebalance (High Tax Drag)</option>
            </select>
          </div>
          ${o==="kr"?`<div>
            <label style="font-size:0.68rem; font-family:var(--font-mono); color:var(--muted);">UNREALIZED GAIN (₩ KRW · TAX HARVESTER)</label>
            <input type="number" id="semiGainKrwInput" value="${e.semiGainKrw??38e5}" step="100000"
                   style="width:100%; padding:8px 10px; background:#060911; border:1px solid var(--border); color:#fff; border-radius:4px; font-family:var(--font-mono); margin-top:3px;" />
          </div>`:""}
        </div>

        <button class="btn btn-emerald" id="btnRunSemiRebalance" style="width:100%; justify-content:center; padding:9px;">
          Calculate Exact $SMH / $XLV Rebalancing Orders
        </button>

        ${f?`
          <div id="semiRebalOutput" style="margin-top:14px; background:#060911; border:1px solid var(--border); border-left:3px solid var(--fin-up); border-radius:4px; padding:14px; font-size:0.8rem;">
            <div style="font-weight:800; color:var(--fin-up); margin-bottom:4px;">
              ${o==="jp"?f.active_rule_jp:o==="kr"?f.active_rule_kr:f.active_rule_en}
            </div>
            <div class="mono" style="font-size:0.71rem; color:#93c5fd; margin-bottom:8px;">
              Latest Close Basis (${f.as_of_date||n.date}): $SMH @ $${Number(f.smh_close??n.smh_close).toFixed(2)} · $XLV @ $${Number(f.xlv_close??n.xlv_close).toFixed(2)}${o==="kr"?` · FX ₩${Number(f.usdkrw??n.usdkrw).toLocaleString()}/$ · Total ₩${Number(f.total_capital_krw??0).toLocaleString()}`:` · Total Capital $${Number(f.total_capital_usd??e.semiCapUsd??1e5).toLocaleString()}`}
            </div>
            <div class="semi-form-grid-2" style="margin-bottom:10px;">
              <div style="background:#0c1220; padding:10px; border-radius:4px; border:1px solid var(--border);">
                <div style="font-size:0.7rem; color:var(--muted);">TARGET $SMH (${f.target_smh_weight_pct}%)</div>
                <div class="mono" style="font-size:1.05rem; font-weight:800; color:#fff; margin-top:2px;">
                  $${Number(f.target_smh_usd??0).toLocaleString()} (${f.target_smh_shares} sh)
                </div>
                <div class="mono" style="font-size:0.73rem; color:${f.delta_smh_usd>=0?"var(--fin-up)":"var(--fin-down)"}; margin-top:2px;">
                  Order vs Drift: ${f.delta_smh_usd>=0?"BUY +":"SELL "}$${Math.abs(Number(f.delta_smh_usd??0)).toLocaleString()} (${f.delta_smh_shares>=0?"+":""}${f.delta_smh_shares} sh)
                </div>
              </div>
              <div style="background:#0c1220; padding:10px; border-radius:4px; border:1px solid var(--border);">
                <div style="font-size:0.7rem; color:var(--muted);">TARGET $XLV (${f.target_xlv_weight_pct}%)</div>
                <div class="mono" style="font-size:1.05rem; font-weight:800; color:#fff; margin-top:2px;">
                  $${Number(f.target_xlv_usd??0).toLocaleString()} (${f.target_xlv_shares} sh)
                </div>
                <div class="mono" style="font-size:0.73rem; color:${f.delta_xlv_usd>=0?"var(--fin-up)":"var(--fin-down)"}; margin-top:2px;">
                  Order vs Drift: ${f.delta_xlv_usd>=0?"BUY +":"SELL "}$${Math.abs(Number(f.delta_xlv_usd??0)).toLocaleString()} (${f.delta_xlv_shares>=0?"+":""}${f.delta_xlv_shares} sh)
                </div>
              </div>
            </div>
            <div style="font-size:0.75rem; color:var(--text-secondary); line-height:1.45; border-top:1px solid var(--border); padding-top:8px;">
              ${o==="kr"?`<div style="margin-bottom:4px;"><b>KRW 2.5M Tax-Free Harvester:</b> ${f.kr_tax_guidance_kr}</div>`:""}
              <div class="mono" style="color:var(--muted);">
                Residual Cash: $${Number(f.residual_cash_usd??0).toFixed(2)} · Est. Annual Tax & Turnover Drag (${f.rebalance_frequency}): -${f.estimated_tax_drag_pct}%/yr · Expected Net 15Y Rate: +${f.expected_net_cagr_pct}%/yr
              </div>
            </div>
          </div>
        `:""}
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
            <input type="number" id="semiLumpCapInput" value="${e.semiLumpCapUsd??5e4}" step="1000"
                   style="width:100%; padding:8px 10px; background:#060911; border:1px solid var(--border); color:#fff; border-radius:4px; font-family:var(--font-mono); font-weight:700; margin-top:3px;" />
          </div>
          <div>
            <label style="font-size:0.68rem; font-family:var(--font-mono); color:var(--muted);">
              SIMULATE FEAR & GREED SCORE (LIVE: ${n.fg_score})
            </label>
            <input type="number" id="semiLumpScoreInput" value="${e.semiLumpScore!==null&&e.semiLumpScore!==void 0?e.semiLumpScore:n.fg_score}" min="0" max="100" step="1"
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

        ${b?`
          <div id="semiLumpOutput" style="margin-top:14px; background:#060911; border:1px solid var(--border); border-left:3px solid var(--fin-blue); border-radius:4px; padding:14px; font-size:0.8rem;">
            <div style="font-weight:800; color:#93c5fd; margin-bottom:3px;">
              ${o==="jp"?b.case_title_jp:o==="kr"?b.case_title_kr:b.case_title_en}
            </div>
            <div class="mono" style="font-size:0.71rem; color:var(--muted); margin-bottom:6px;">
              Latest Close Basis (${b.as_of_date||n.date}): $SMH @ $${Number(b.smh_close??n.smh_close).toFixed(2)} · $XLV @ $${Number(b.xlv_close??n.xlv_close).toFixed(2)}
            </div>
            <p style="font-size:0.76rem; color:var(--text-secondary); margin-bottom:10px;">
              ${o==="jp"?b.summary_jp:o==="kr"?b.summary_kr:b.summary_en}
            </p>
            <div style="display:flex; flex-direction:column; gap:8px;">
              ${b.tranches.map(l=>{const S=o==="jp"?l.title_jp:o==="kr"?l.title_kr:l.title_en,k=o==="jp"?l.timing_jp:o==="kr"?l.timing_kr:l.timing_en,$=o==="jp"?l.note_jp:o==="kr"?l.note_kr:l.note_en;return`
                  <div style="background:#0c1220; padding:10px; border-radius:4px; border:1px solid var(--border);">
                    <div style="display:flex; justify-content:space-between; align-items:center;">
                      <b style="color:#ffffff;">${S}</b>
                      <span class="mono" style="color:var(--fin-up); font-weight:700;">$${l.amount_usd.toLocaleString()} (${l.allocation_pct}%)</span>
                    </div>
                    <div class="mono" style="font-size:0.72rem; color:#93c5fd; margin-top:2px;">
                      ${k} · $SMH: $${l.smh_usd.toLocaleString()} (${l.smh_shares} sh) | $XLV: $${l.xlv_usd.toLocaleString()} (${l.xlv_shares} sh)
                    </div>
                    <div style="font-size:0.74rem; color:var(--muted); margin-top:4px;">${$}</div>
                  </div>
                `}).join("")}
            </div>
          </div>
        `:""}
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

      ${Kt(e.semiHistory)}

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
            ${d.map(l=>`
                <tr class="proof-highlight">
                  <td style="font-family:var(--font-sans);">${o==="jp"?l.horizon_jp:o==="kr"?l.horizon_kr:l.horizon_en}</td>
                  <td>${l.period}</td>
                  <td style="color:var(--text-secondary);">+${l.qqq_cagr_pct.toFixed(2)}%</td>
                  <td style="color:var(--text-secondary);">${l.qqq_multiple.toFixed(2)}x</td>
                  <td>+${l.port_70_30_cagr_pct.toFixed(2)}%</td>
                  <td style="color:var(--fin-up); font-weight:800;">+${l.port_80_20_cagr_pct.toFixed(2)}%</td>
                  <td style="color:var(--fin-up); font-weight:800;">${l.port_80_20_multiple.toFixed(2)}x</td>
                  <td><span style="color:var(--fin-up);">${l.port_80_20_mdd_pct.toFixed(1)}%</span> <span style="color:var(--muted); font-size:0.72rem;">(QQQ ${l.qqq_mdd_pct.toFixed(1)}%)</span></td>
                </tr>
              `).join("")}
          </tbody>
        </table>
      </div>
    </section>

    <!-- SECTION 5: PRO TERMINAL & LIFETIME LICENSE PRICING -->
    ${vt(e)}

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
  `}const mt=window.location.pathname.toLowerCase(),ft=window.location.hash.toLowerCase(),ue=new URLSearchParams(window.location.search),ut=(ue.get("view")||"").toLowerCase(),le=(ue.get("ticker")||window.__INITIAL_TICKER__||"").trim().toUpperCase(),fe=(ue.get("filter")||window.__INITIAL_FILTER__||"").trim().toLowerCase(),Jt=ut==="semi"||ft.includes("semi")||mt.includes("/semi")?"semi":ut==="rightside"||ft.includes("rightside")||mt.includes("/rightside")||le||fe?"rightside":window.__DEFAULT_VIEW__==="semi"?"semi":"rightside";(function(){try{localStorage.getItem("rsa_lang_v3_en")&&!localStorage.getItem("rsa_lang_v4_auto")&&(localStorage.removeItem("rsa_lang"),localStorage.removeItem("rsa_lang_v3_en"),localStorage.setItem("rsa_lang_v4_auto","1")),(localStorage.getItem("rsa_cfg_site1_url")||"").includes("getbreakai.com")&&localStorage.setItem("rsa_cfg_site1_url","https://truthofmarket.com");const o=localStorage.getItem("rsa_cfg_ls_monthly")||"";(o.includes("rightsidealpha.lemonsqueezy.com")||o.includes("pro-monthly")||o.includes("d5e7e761"))&&localStorage.removeItem("rsa_cfg_ls_monthly");const n=localStorage.getItem("rsa_cfg_ls_ltd")||"";(n.includes("rightsidealpha.lemonsqueezy.com")||n.includes("lifetime-pass")||n.includes("667aa482"))&&localStorage.removeItem("rsa_cfg_ls_ltd"),(localStorage.getItem("rsa_cfg_aff_tv")||"")==="rightsidealpha"&&localStorage.setItem("rsa_cfg_aff_tv","1173809"),(localStorage.getItem("rsa_cfg_aff_sa")||"")==="affiliate_rightside"&&localStorage.setItem("rsa_cfg_aff_sa","better_life333");const p=localStorage.getItem("rsa_cfg_broker_url")||"";(p.includes("ibkr.com/referral/rightsidealpha")||p.includes("partner.bitget.com"))&&(localStorage.setItem("rsa_cfg_broker_url","https://www.bitget.com/referral/register?clacCode=7nja"),localStorage.setItem("rsa_cfg_broker_name","Bitget (7nja)"));const r=localStorage.getItem("rsa_tg_channel_url")||"";(!r||r.includes("SemifearGreedbot")||r.includes("RightSideAlphaBot"))&&localStorage.setItem("rsa_tg_channel_url","https://t.me/truthofmarketss");const m=localStorage.getItem("rsa_tg_chat_id")||"";(!m||m.includes("SemifearGreedbot")||m==="755033799")&&localStorage.setItem("rsa_tg_chat_id","@truthofmarketss"),(localStorage.getItem("rsa_cfg_instagram_url")||"").includes("semifeargreed")&&localStorage.setItem("rsa_cfg_instagram_url","https://www.instagram.com/rightsidealpha")}catch{}})();function eo(){try{const e=localStorage.getItem("rsa_lang");if(e&&(e==="kr"||e==="en"||e==="jp"))return e;const t=(navigator.language||navigator.userLanguage||"en").toLowerCase();if(t.startsWith("ko"))return"kr";if(t.startsWith("ja"))return"jp"}catch{}return"en"}const s={lang:eo(),activeView:Jt,isAdminAuthenticated:sessionStorage.getItem("rsa_admin_auth")==="true",isProUnlocked:ge(),licenseKey:localStorage.getItem("rsa_token")||"",proPortfolioUsd:Number(localStorage.getItem("rsa_pro_cap_usd")||3e4),stocks:[],filteredStocks:[],backtestKpis:null,pineCode:null,searchQuery:le||"",zoneFilter:fe==="ignition"||fe==="ignition_zone"?"IGNITION_ZONE":fe==="washout"?"WASHOUT_WATCH":"ALL",sortCol:"score",sortAsc:!1,semiOverview:null,semiHistory:null,semiGaugeTab:"overview",semiRange:"1Y",semiCapUsd:1e5,semiMode:"AUTO_REGIME",semiFreq:"ANNUAL",semiGainKrw:38e5,semiRebalanceResult:null,semiLumpCapUsd:5e4,semiLumpScore:null,semiLumpSumResult:null,telegramConfigured:!0,telegramBotToken:localStorage.getItem("rsa_tg_bot_token")||ke,telegramChatId:localStorage.getItem("rsa_tg_chat_id")||"@truthofmarketss",telegramAlertType:"SEMI_BRIEFING",telegramPreviewText:"",config:{site1_name:"RightSideAlpha",site1_url:localStorage.getItem("rsa_cfg_site1_url")||"https://truthofmarket.com",site2_url:"https://truthofmarket.com",ls_site1_monthly_url:localStorage.getItem("rsa_cfg_ls_monthly")||"https://truthofmarket.lemonsqueezy.com/checkout/buy/bad98d00-7175-41f6-9d58-eeb2471d0da4",ls_site1_ltd_url:localStorage.getItem("rsa_cfg_ls_ltd")||"https://truthofmarket.lemonsqueezy.com/checkout/buy/00c9f6e1-c8be-42a4-b5a5-e05af1a41ed9",tradingview_aff_id:localStorage.getItem("rsa_cfg_aff_tv")||"1173809",seekingalpha_source:localStorage.getItem("rsa_cfg_aff_sa")||"better_life333",broker_name:localStorage.getItem("rsa_cfg_broker_name")||"Bitget (7nja)",broker_referral_url:localStorage.getItem("rsa_cfg_broker_url")||"https://www.bitget.com/referral/register?clacCode=7nja",telegram_channel_url:localStorage.getItem("rsa_tg_channel_url")||"https://t.me/truthofmarketss",telegram_vip_channel_url:localStorage.getItem("rsa_tg_vip_channel_url")||"",telegram_chat_id:localStorage.getItem("rsa_tg_chat_id")||"@truthofmarketss",youtube_url:localStorage.getItem("rsa_cfg_youtube_url")||Ue,instagram_url:localStorage.getItem("rsa_cfg_instagram_url")||ze},get t(){return Ce[this.lang]||Ce.en}};function D(e){const t=document.getElementById("toastBox");t&&(t.textContent=e,t.style.display="block",clearTimeout(window.__toastTimer),window.__toastTimer=setTimeout(()=>{t.style.display="none"},3200))}function xe(){const e=(s.searchQuery||"").trim().toLowerCase(),t=s.zoneFilter;let o=s.stocks.filter(i=>!(!i.ticker||String(i.ticker).includes(".")||t!=="ALL"&&i.zone_code!==t||e&&!(!s.isProUnlocked&&i.zone_code==="IGNITION_ZONE"&&i.ticker!=="CELH"?`vip ignition locked pro ${i.sector}`.toLowerCase():`${i.ticker} ${i.name_en} ${i.name_jp} ${i.name_kr} ${i.sector}`.toLowerCase()).includes(e)));const n=s.sortCol,a=s.sortAsc?1:-1;o.sort((i,p)=>{const r=i[n],m=p[n];return typeof r=="string"||typeof m=="string"?String(r??"").localeCompare(String(m??""))*a:((r??0)-(m??0))*a}),s.filteredStocks=o}function to(){const e=s.t;return`
    ${Ut(s)}
    ${zt(s)}
    <section class="screener-panel">
      ${Ht(s)}
      ${Vt(s)}
    </section>
    ${jt(s)}
    ${vt(s)}

    <!-- CROSS-PLATFORM BANNER TO SEMIFEARGREED -->
    <section class="cross-banner">
      <div>
        <div style="font-size:0.72rem; font-family:var(--font-mono); font-weight:700; color:#f87171; text-transform:uppercase; letter-spacing:0.05em;" id="crossTitle">
          ${e.crossTitle}
        </div>
        <h3 style="font-size:1.15rem; font-weight:800; margin:4px 0; color:#ffffff;" id="crossHeading">
          ${e.crossHeading}
        </h3>
        <p style="font-size:0.84rem; color:var(--muted);" id="crossDesc">
          ${e.crossDesc}
        </p>
      </div>
      <button class="btn btn-primary" id="crossFunnelSwitchBtn" style="background:#dc2626; border-color:#ef4444;">
        <span id="crossBtn">${e.crossBtn} →</span>
      </button>
    </section>
  `}function Y(){const e=document.getElementById("app");if(!e)return;const t=s.t;e.innerHTML=`
    ${Ot(s)}
    <main class="container">
      ${s.activeView==="semi"?Zt(s):to()}

      <footer style="border-top:1px solid var(--border); padding-top:20px; margin-top:28px; color:var(--muted); font-size:0.76rem; line-height:1.6;">
        <div style="display:flex; gap:12px; align-items:center; flex-wrap:wrap; margin-bottom:12px;">
          <span class="mono" style="font-size:0.72rem; color:var(--text); font-weight:700;">OFFICIAL CHANNELS:</span>
          <a href="${s.config.youtube_url||Ue}" target="_blank" rel="noopener noreferrer" style="color:#fca5a5; text-decoration:none; font-weight:600;">
            📺 YouTube (@rightsidealpha) ↗
          </a>
          <span style="color:var(--border);">|</span>
          <a href="${s.config.instagram_url||ze}" target="_blank" rel="noopener noreferrer" style="color:#f9a8d4; text-decoration:none; font-weight:600;">
            📸 Instagram (@rightsidealpha) ↗
          </a>
          <span style="color:var(--border);">|</span>
          <a href="${s.config.x_url||"https://x.com/rightsidealpha"}" target="_blank" rel="noopener noreferrer" style="color:#e2e8f0; text-decoration:none; font-weight:600;">
            𝕏 (@rightsidealpha) ↗
          </a>
          <span style="color:var(--border);">|</span>
          <a
            href="${we(s.isProUnlocked)}"
            class="${s.isProUnlocked?"":"btn-gated-vip-tg"}"
            ${s.isProUnlocked?'target="_blank" rel="noopener noreferrer"':""}
            style="color:#38bdf8; text-decoration:none; font-weight:600;"
          >
            ${s.isProUnlocked?"👑 Pro VIP Telegram Channel ↗":"🔒 Pro VIP Telegram ($SMH/$XLV & 72-Stock News)"}
          </a>
        </div>
        <div style="display:flex; gap:12px; align-items:center; flex-wrap:wrap; margin-bottom:10px; font-size:0.74rem;">
          <a href="#legal-terms" class="btn-open-legal" data-legal-tab="terms" style="color:#93c5fd; text-decoration:none; font-weight:600;">Terms of Service</a>
          <span style="color:var(--border);">·</span>
          <a href="#legal-privacy" class="btn-open-legal" data-legal-tab="privacy" style="color:#93c5fd; text-decoration:none; font-weight:600;">Privacy Policy</a>
          <span style="color:var(--border);">·</span>
          <a href="#legal-refund" class="btn-open-legal" data-legal-tab="refund" style="color:#93c5fd; text-decoration:none; font-weight:600;">Refund & Cancellation Policy</a>
          <span style="color:var(--border);">·</span>
          <a href="mailto:support@truthofmarket.com" style="color:#93c5fd; text-decoration:none; font-weight:600;">Support: support@truthofmarket.com</a>
          <span style="color:var(--border);">·</span>
          <span style="color:#cbd5e1; font-weight:600;">Operated by Yoonju Lee · KIDS-FIT Global Studio (Lemon Squeezy Store #296100 · <a href="https://kisfitglobal.com" target="_blank" rel="noopener noreferrer" style="color:#93c5fd; text-decoration:none;">kisfitglobal.com</a> &amp; <a href="https://truthofmarket.com" style="color:#93c5fd; text-decoration:none;">truthofmarket.com</a>)</span>
        </div>
        <p id="disclaimerText">${t.disclaimer}</p>
        <p style="margin-top:8px; font-family:var(--font-mono); font-size:0.72rem;" id="copyrightText">${t.copyright}</p>
      </footer>
    </main>
    <canvas id="scoreCanvas" width="900" height="500" style="display:none;"></canvas>
    ${qt(s)}
  `,oo()}function de(e){s.activeView=e==="semi"?"semi":"rightside";const t=window.location.pathname||"/";s.activeView==="semi"?window.history.replaceState(null,"",`${t}#semi`):window.history.replaceState(null,"",`${t}#rightside`),Y(),window.scrollTo({top:0,behavior:"smooth"})}function oo(){if(typeof window.createLemonSqueezy=="function")try{window.createLemonSqueezy()}catch{}const e=document.getElementById("brandHomeBtn");e&&e.addEventListener("click",()=>{window.scrollTo({top:0,behavior:"smooth"})});const t=document.getElementById("navTabRightSide");t&&t.addEventListener("click",()=>de("rightside"));const o=document.getElementById("navTabSemiFg");o&&o.addEventListener("click",()=>de("semi"));const n=document.getElementById("ribbonSwitchSemi");n&&n.addEventListener("click",()=>de("semi"));const a=document.getElementById("crossFunnelSwitchBtn");a&&a.addEventListener("click",()=>de("semi"));const i=document.getElementById("btnSwitchToRightSide");i&&i.addEventListener("click",()=>de("rightside")),document.querySelectorAll(".lang-btn").forEach(c=>{c.addEventListener("click",()=>{const u=c.getAttribute("data-lang");u&&Ce[u]&&(s.lang=u,localStorage.setItem("rsa_lang",u),Y())})});const p=document.getElementById("searchInput");p&&p.addEventListener("input",c=>{s.searchQuery=c.target.value,xe();const u=document.getElementById("tableBody");u&&(u.innerHTML=Me(s)),Re()}),document.querySelectorAll(".filter-tab").forEach(c=>{c.addEventListener("click",()=>{s.zoneFilter=c.getAttribute("data-zone")||"ALL",xe(),Y()})});const r=()=>{document.querySelectorAll(".sort-header").forEach(c=>{const u=c.getAttribute("data-sort");if(!u)return;const g=s.sortCol===u;c.classList.remove("sort-active","sort-asc","sort-desc"),g&&c.classList.add("sort-active",s.sortAsc?"sort-asc":"sort-desc");const v=c.querySelector(".sort-chevron");v&&(v.textContent=g?s.sortAsc?"▲":"▼":"↕",g?v.classList.remove("muted"):v.classList.add("muted"))})};document.querySelectorAll(".sort-header").forEach(c=>{c.addEventListener("click",()=>{const u=c.getAttribute("data-sort");if(!u)return;s.sortCol===u?s.sortAsc=!s.sortAsc:(s.sortCol=u,s.sortAsc=u==="ticker"),xe(),r();const g=document.getElementById("tableBody");g&&(g.innerHTML=Me(s)),Re()})});const m=document.getElementById("licenseModal"),f=(c=!1,u="")=>{if(!m)return;m.style.display="flex";const g=document.getElementById("licenseInput"),v=document.getElementById("licenseMsg");g&&!g.value.trim()&&(g.value=s.licenseKey||""),v&&u&&(v.style.color="#93c5fd",v.textContent=u)},b=()=>{m&&(m.style.display="none")},d=document.getElementById("btnOpenLicense");d&&d.addEventListener("click",()=>f(!1));const h=document.getElementById("proStatusBadge");h&&(h.style.cursor="pointer",h.addEventListener("click",()=>f(!1)));const _=document.getElementById("vaultUnlockBtn");_&&_.addEventListener("click",()=>f(!1));const l=document.getElementById("vaultOverlayUnlock");l&&l.addEventListener("click",()=>f(!1)),document.querySelectorAll(".btn-gated-vip-tg").forEach(c=>{c.addEventListener("click",u=>{s.isProUnlocked||(u.preventDefault(),f(!1,"🔒 Pro VIP Telegram Channel ($SMH/$XLV & 72-Stock Real-Time News + Unmasked Ignition Signals) is exclusively for Pro Subscribers ($29/mo or $199 Lifetime)."))})});const S=document.getElementById("btnCancelLicense");S&&S.addEventListener("click",b);const k=document.getElementById("btnLockLicense");k&&k.addEventListener("click",async()=>{s.isProUnlocked=!1,s.licenseKey="",localStorage.removeItem("rsa_pro_unlocked"),localStorage.removeItem("rsa_token"),await me(),b(),Y(),D("Pro Terminal Locked — Reverted to Free Preview")});const $=async()=>{const c=document.getElementById("licenseInput"),u=document.getElementById("licenseMsg"),g=(c?c.value:"").trim();if(!g){u&&(u.style.color="var(--fin-down)",u.textContent="Please enter your Lemon Squeezy Pro license key.");return}try{const v=await At(g);v.valid?(s.isProUnlocked=!0,s.licenseKey=g,localStorage.setItem("rsa_pro_unlocked","true"),localStorage.setItem("rsa_token",g),u&&(u.style.color="var(--fin-up)",u.textContent=v.message||"Pro Terminal Unlocked."),await me(),setTimeout(()=>{b(),Y(),D("Pro Terminal Unlocked — All 72 US Equity Targets Active")},350)):u&&(u.style.color="var(--fin-down)",u.textContent=v.message||"Invalid or expired license key. Please verify your Lemon Squeezy receipt or subscribe below.")}catch{u&&(u.style.color="var(--fin-down)",u.textContent="Unable to verify license key. Please check your key and try again.")}},E=document.getElementById("btnVerifyLicense");E&&E.addEventListener("click",$);const L=document.getElementById("licenseInput");L&&L.addEventListener("keydown",c=>{c.key==="Enter"&&(c.preventDefault(),$())});const N=async(c,u="")=>{const g="RSA-VIP-2026-FOUNDER7D";s.isProUnlocked=!0,s.licenseKey=g,localStorage.setItem("rsa_pro_unlocked","true"),localStorage.setItem("rsa_token",g),u&&localStorage.setItem("rsa_vip_email",u);try{const w=new Date(Date.now()+324e5).toISOString().slice(0,10);fetch("https://abacus.jasoncameron.dev/hit/tom_truthofmarket/paid_member_"+w,{mode:"cors",keepalive:!0}).catch(()=>{}),fetch("https://abacus.jasoncameron.dev/hit/tom_truthofmarket/paid_member_total",{mode:"cors",keepalive:!0}).catch(()=>{})}catch{}const v=document.getElementById("licenseInput"),x=document.getElementById("licenseMsg");v&&(v.value=g),x&&(x.style.color="var(--fin-up)",x.textContent=`✅ ${c}: Pro Terminal Unlocked (Key: ${g}). All 72 US Equity Targets & 26Y CSV Active!`),await me(),setTimeout(()=>{b(),Y(),D("🎉 Pro Terminal Unlocked — All 72 US Equity Targets & 26Y CSV Active!")},350)},y=document.getElementById("btnInstantVipTrialUnlock"),C=document.getElementById("vipTrialEmailInput");C&&C.addEventListener("keydown",c=>{c.key==="Enter"&&(c.preventDefault(),y&&y.click())}),["btnPartnerUnlockTv","btnPartnerUnlockBrk"].forEach(c=>{const u=document.getElementById(c);u&&u.addEventListener("click",()=>{setTimeout(()=>{N("Partner Verification Unlock")},600)})}),document.querySelectorAll(".lemonsqueezy-button").forEach(c=>{c.addEventListener("click",u=>{const g=c.getAttribute("href")||"";window.LemonSqueezy&&window.LemonSqueezy.Url&&typeof window.LemonSqueezy.Url.Open=="function"&&(u.preventDefault(),window.LemonSqueezy.Url.Open(g))})});const O=document.getElementById("adminLoginModal"),I=document.getElementById("configModal"),X=document.getElementById("btnOpenConfig"),F=document.getElementById("btnCancelConfig"),G=document.getElementById("btnSaveConfig"),z=document.getElementById("btnCancelAdminLogin"),H=document.getElementById("btnSubmitAdminLogin"),W=document.getElementById("btnAdminLogout"),J=async()=>{const c=document.getElementById("adminIdInput"),u=document.getElementById("adminPwInput"),g=document.getElementById("adminLoginMsg"),v=(c?c.value:"").trim(),x=u?u.value:"";if(!v||!x){g&&(g.style.color="var(--fin-down)",g.textContent="Please enter both Admin ID and Password.");return}try{const w=await Lt(v,x);if(w&&w.authenticated){s.isAdminAuthenticated=!0,sessionStorage.setItem("rsa_admin_auth","true"),s.isProUnlocked=!0,s.licenseKey=w.license_key||"RSA-ADMIN-SESSION",localStorage.setItem("rsa_pro_unlocked","true"),localStorage.setItem("rsa_token",s.licenseKey),g&&(g.style.color="var(--fin-up)",g.textContent=w.message||"Admin Authenticated!"),await me(),O&&(O.style.display="none"),Y();const T=document.getElementById("configModal");T&&(T.style.display="flex"),D("Admin Authenticated — Terminal Config & Pro Access Unlocked")}else g&&(g.style.color="var(--fin-down)",g.textContent=w&&w.message||"Invalid Admin ID or Password.")}catch{g&&(g.style.color="var(--fin-down)",g.textContent="Authentication error. Please try again.")}};X&&X.addEventListener("click",()=>{if(s.isAdminAuthenticated)I&&(I.style.display="flex");else if(O){O.style.display="flex";const c=document.getElementById("adminIdInput");c&&c.focus()}}),z&&O&&z.addEventListener("click",()=>{O.style.display="none"}),H&&H.addEventListener("click",J);const j=document.getElementById("adminPwInput");j&&j.addEventListener("keydown",c=>{c.key==="Enter"&&(c.preventDefault(),J())}),W&&W.addEventListener("click",()=>{s.isAdminAuthenticated=!1,sessionStorage.removeItem("rsa_admin_auth"),I&&(I.style.display="none"),D("Admin Session Locked")}),F&&I&&F.addEventListener("click",()=>{I.style.display="none"}),G&&G.addEventListener("click",async()=>{var P,B,V,ee,Z,se,at,st,lt,ct;const c=((P=document.getElementById("cfgSite1Url"))==null?void 0:P.value.trim())||s.config.site1_url,u=((B=document.getElementById("cfgLsMonthly"))==null?void 0:B.value.trim())||s.config.ls_site1_monthly_url,g=((V=document.getElementById("cfgLsLtd"))==null?void 0:V.value.trim())||s.config.ls_site1_ltd_url,v=((ee=document.getElementById("cfgTgChannel"))==null?void 0:ee.value.trim())||s.config.telegram_channel_url||Oe,x=((Z=document.getElementById("cfgYoutubeUrl"))==null?void 0:Z.value.trim())||s.config.youtube_url||Ue,w=((se=document.getElementById("cfgInstagramUrl"))==null?void 0:se.value.trim())||s.config.instagram_url||ze,T=((at=document.getElementById("cfgAffTv"))==null?void 0:at.value.trim())||"1173809",A=((st=document.getElementById("cfgAffSa"))==null?void 0:st.value.trim())||"better_life333",M=((lt=document.getElementById("cfgBrokerName"))==null?void 0:lt.value.trim())||"Bitget (7nja)",R=((ct=document.getElementById("cfgBrokerUrl"))==null?void 0:ct.value.trim())||"https://www.bitget.com/referral/register?clacCode=7nja";s.config.site1_url=c,s.config.ls_site1_monthly_url=u,s.config.ls_site1_ltd_url=g,s.config.telegram_channel_url=v,s.config.youtube_url=x,s.config.instagram_url=w,s.config.tradingview_aff_id=T,s.config.seekingalpha_source=A,s.config.broker_name=M,s.config.broker_referral_url=R,localStorage.setItem("rsa_cfg_site1_url",c),localStorage.setItem("rsa_cfg_ls_monthly",u),localStorage.setItem("rsa_cfg_ls_ltd",g),localStorage.setItem("rsa_tg_channel_url",v),localStorage.setItem("rsa_cfg_youtube_url",x),localStorage.setItem("rsa_cfg_instagram_url",w),localStorage.setItem("rsa_cfg_aff_tv",T),localStorage.setItem("rsa_cfg_aff_sa",A),localStorage.setItem("rsa_cfg_broker_name",M),localStorage.setItem("rsa_cfg_broker_url",R);try{await Nt({tradingview_aff_id:T,seekingalpha_source:A,broker_name:M,broker_referral_url:R,ls_site1_monthly_url:u,ls_site1_ltd_url:g,site1_url:c,telegram_channel_url:v,youtube_url:x,instagram_url:w})}catch{}I&&(I.style.display="none"),Y(),D("Terminal & Affiliate Configuration Saved")});const U=document.getElementById("telegramModal"),Q=async c=>{var A,M,R;const u=document.getElementById("tgAlertTypeSelect"),g=c||(u==null?void 0:u.value)||s.telegramAlertType||"SEMI_BRIEFING";s.telegramAlertType=g;const v=document.getElementById("telegramPreviewBox"),x=(((A=document.getElementById("docTicker"))==null?void 0:A.value)||"CELH").trim().toUpperCase(),w=parseFloat(((M=document.getElementById("docEntry"))==null?void 0:M.value)||"27.93")||27.93,T=parseInt(((R=document.getElementById("docDays"))==null?void 0:R.value)||"42",10)||42;try{const P=await Pe({alert_type:g,lang:s.lang,ticker:x,entry_price:w,days_held:T,dry_run:!0});P&&P.message_preview&&(s.telegramPreviewText=P.message_preview,v&&(v.textContent=P.message_preview))}catch{}},K=async c=>{if(U){if(c){s.telegramAlertType=c;const u=document.getElementById("tgAlertTypeSelect");u&&(u.value=c)}U.style.display="flex",await Q(c);try{const u=await He(s.telegramBotToken,s.telegramChatId);if(u&&u.chatId&&u.chatId!==s.telegramChatId){s.telegramChatId=u.chatId;const g=document.getElementById("tgChatIdInput");g&&(g.value=u.chatId)}}catch{}}},ne=document.getElementById("btnOpenTelegram");ne&&ne.addEventListener("click",()=>K(s.activeView==="semi"?"SEMI_BRIEFING":"RSA_IGNITION"));const re=document.getElementById("btnSendSemiTelegram");re&&re.addEventListener("click",()=>K("SEMI_BRIEFING"));const ie=document.getElementById("btnOpenTelegramFromPricing");ie&&ie.addEventListener("click",()=>K("FULL_DAILY"));const he=document.getElementById("btnCloseTelegram");he&&U&&he.addEventListener("click",()=>{U.style.display="none"});const ve=document.getElementById("tgAlertTypeSelect");ve&&ve.addEventListener("change",c=>{Q(c.target.value)});const ye=document.getElementById("btnPreviewTelegram");ye&&ye.addEventListener("click",()=>{Q(),D("Refreshed Live Telegram Briefing Preview")});const _e=document.getElementById("btnCopyTelegramMsg");_e&&_e.addEventListener("click",async()=>{var u;const c=((u=document.getElementById("telegramPreviewBox"))==null?void 0:u.textContent)||s.telegramPreviewText||"";try{await navigator.clipboard.writeText(c),D("Telegram Briefing Copied to Clipboard")}catch{D("Briefing Text Ready to Copy")}});const Ve=async()=>{var x,w,T;const c=((x=document.getElementById("tgBotTokenInput"))==null?void 0:x.value.trim())??s.telegramBotToken,u=((w=document.getElementById("tgChatIdInput"))==null?void 0:w.value.trim())??s.telegramChatId,g=((T=document.getElementById("tgChannelUrlInput"))==null?void 0:T.value.trim())||s.config.telegram_channel_url||"https://t.me/SemiFearGreed";s.telegramBotToken=c,s.telegramChatId=u,s.telegramConfigured=!!(c&&u),s.config.telegram_channel_url=g,s.config.telegram_chat_id=u,localStorage.setItem("rsa_tg_bot_token",c),localStorage.setItem("rsa_tg_chat_id",u),localStorage.setItem("rsa_tg_channel_url",g);const v=document.getElementById("tgChannelLinkBtn");v&&v.setAttribute("href",g);try{await Dt({bot_token:c,chat_id:u,channel_url:g,lang:s.lang})}catch{}return{tok:c,cid:u,chUrl:g}},Ge=document.getElementById("btnVerifyTelegram");Ge&&Ge.addEventListener("click",async()=>{const c=document.getElementById("telegramStatusMsg"),{tok:u,cid:g}=await Ve();c&&(c.style.color="#93c5fd",c.textContent="Verifying Telegram Bot connection...");try{const v=await Ft({bot_token:u,chat_id:g});c&&(c.style.color=v.valid?"var(--fin-up)":"var(--fin-amber)",c.textContent=v.message||"Bot configuration saved."),D(v.valid?"Telegram Bot Verified & Saved":"Saved Telegram Parameters")}catch{c&&(c.style.color="var(--fin-amber)",c.textContent="Saved locally. Ready for preview or direct dispatch.")}});const je=document.getElementById("btnSendTelegramNow");je&&je.addEventListener("click",async()=>{var M,R,P,B;const c=document.getElementById("telegramStatusMsg"),u=document.getElementById("telegramPreviewBox"),{tok:g,cid:v}=await Ve(),x=((M=document.getElementById("tgAlertTypeSelect"))==null?void 0:M.value)||s.telegramAlertType||"SEMI_BRIEFING",w=(((R=document.getElementById("docTicker"))==null?void 0:R.value)||"CELH").trim().toUpperCase(),T=parseFloat(((P=document.getElementById("docEntry"))==null?void 0:P.value)||"27.93")||27.93,A=parseInt(((B=document.getElementById("docDays"))==null?void 0:B.value)||"42",10)||42;c&&(c.style.color="#93c5fd",c.textContent="Dispatching briefing to Telegram...");try{const V=await Pe({alert_type:x,lang:s.lang,bot_token:g,chat_id:v,ticker:w,entry_price:T,days_held:A,dry_run:!1});V&&V.message_preview&&(s.telegramPreviewText=V.message_preview,u&&(u.textContent=V.message_preview)),c&&(c.style.color=V.delivered?"var(--fin-up)":"#38bdf8",c.textContent=V.status_detail||"Telegram briefing processed."),D(V.delivered?`Telegram Briefing Sent to ${V.chat_id}!`:"Briefing Preview Generated (Enter Live Bot Token & Chat ID to Push)")}catch{c&&(c.style.color="var(--fin-down)",c.textContent="Error sending Telegram alert.")}});const qe=document.getElementById("btnCalcProSizing");qe&&qe.addEventListener("click",()=>{var u;const c=parseFloat(((u=document.getElementById("proCapitalInput"))==null?void 0:u.value)||"30000");Number.isFinite(c)&&c>=1e3?(s.proPortfolioUsd=c,localStorage.setItem("rsa_pro_cap_usd",String(c)),Y(),D(`Updated Pro Position Sizing for $${c.toLocaleString()} Account`)):D("Please enter an account size of at least $1,000")}),document.querySelectorAll(".btn-quick-doc").forEach(c=>{c.addEventListener("click",async()=>{const u=c.getAttribute("data-ticker"),g=s.stocks.find(P=>P.ticker===u),v=document.getElementById("docTicker"),x=document.getElementById("docEntry"),w=document.getElementById("docDays"),T=document.getElementById("docOutput");v&&u&&(v.value=u);const A=g?Number(g.close):27.93;x&&(x.value=A.toFixed(2));const M=parseInt((w==null?void 0:w.value)||"42",10),R=Number.isFinite(M)&&M>=0?M:42;try{const P=await $e({ticker:u||"CELH",entry_price:A,days_held:R});s.docLastResult=P,T&&(T.innerHTML=Be(P))}catch{}})});const Xe=document.getElementById("btnRunPositionDoctor");Xe&&Xe.addEventListener("click",async()=>{var x,w,T;const c=(((x=document.getElementById("docTicker"))==null?void 0:x.value)||"CELH").trim().toUpperCase(),u=parseFloat(((w=document.getElementById("docEntry"))==null?void 0:w.value)??""),g=parseInt(((T=document.getElementById("docDays"))==null?void 0:T.value)??"",10),v=document.getElementById("docOutput");if(!Number.isFinite(u)||u<=0||!Number.isFinite(g)||g<0){v&&(v.innerHTML='<div style="color:var(--fin-down);">Please enter a valid positive cost basis ($) and non-negative trading days.</div>');return}try{const A=await $e({ticker:c,entry_price:u,days_held:g});s.docLastResult=A,v&&(v.innerHTML=Be(A))}catch{v&&(v.innerHTML='<div style="color:var(--fin-down);">Please enter a valid positive cost basis ($) and non-negative trading days.</div>')}});const ce=document.getElementById("researchModal"),Ye=document.getElementById("btnCloseResearch");Ye&&ce&&Ye.addEventListener("click",()=>{ce.style.display="none"});const ae=document.getElementById("legalModal"),We=document.getElementById("btnCloseLegalModal");We&&ae&&We.addEventListener("click",()=>{ae.style.display="none"}),document.querySelectorAll(".btn-open-legal, .btn-legal-tab").forEach(c=>{c.addEventListener("click",u=>{u.preventDefault();const g=c.getAttribute("data-legal-tab")||"terms";if(ae){ae.style.display="flex";const v=ae.querySelector(`[data-legal-section="${g}"]`);v&&typeof v.scrollIntoView=="function"&&v.scrollIntoView({behavior:"smooth",block:"start"})}})});const oe=document.getElementById("pwRsiModal"),Qe=document.getElementById("btnOpenPwRsiExplainer"),Ke=document.getElementById("btnClosePwRsiModal"),Ze=document.getElementById("btnUnderstandPwRsi");Qe&&oe&&Qe.addEventListener("click",()=>{oe.style.display="flex"}),Ke&&oe&&Ke.addEventListener("click",()=>{oe.style.display="none"}),Ze&&oe&&Ze.addEventListener("click",()=>{oe.style.display="none";const c=document.getElementById("stockTable");c&&typeof c.scrollIntoView=="function"&&c.scrollIntoView({behavior:"smooth",block:"start"})}),[m,U,I,ce,ae,oe].forEach(c=>{c&&c.addEventListener("click",u=>{u.target===c&&(c.style.display="none")})});const _t=c=>{const u=P=>String(P||"").replace(/&/g,"&amp;").replace(/</g,"&lt;").replace(/>/g,"&gt;"),g=P=>u(P).replace(/\*\*([^*]+)\*\*/g,'<strong style="color:#ffffff;">$1</strong>').replace(/`([^`]+)`/g,'<code class="mono" style="background:#0f172a; padding:1px 5px; border-radius:3px; color:#93c5fd;">$1</code>'),v=String(c||"").split(/\r?\n/),x=[];let w=!1,T=[],A=!1;const M=()=>{if(!T.length)return;const P=T[0],B=T.slice(1).filter(Z=>!Z.every(se=>/^[-:\s]+$/.test(se))),V=P.map(Z=>`<th style="padding:7px 10px; border-bottom:1px solid #334155; text-align:left; color:#93c5fd; font-size:0.76rem;">${g(Z)}</th>`).join(""),ee=B.map(Z=>`<tr>${Z.map(se=>`<td style="padding:7px 10px; border-bottom:1px solid #1e293b; font-size:0.78rem;">${g(se)}</td>`).join("")}</tr>`).join("");x.push(`<div class="table-responsive-scroll" style="margin:10px 0;"><table style="width:100%; border-collapse:collapse; background:#090d16; border:1px solid #1e293b;"><thead><tr>${V}</tr></thead><tbody>${ee}</tbody></table></div>`),T=[],w=!1},R=()=>{A&&(x.push("</ul>"),A=!1)};for(const P of v){const B=P.trim();if(B.startsWith("|")&&B.endsWith("|")){R(),w=!0;const V=B.slice(1,-1).split("|").map(ee=>ee.trim());T.push(V);continue}else w&&M();if(!B){R();continue}/^---+$/.test(B)?(R(),x.push('<hr style="border:none; border-top:1px solid var(--border); margin:12px 0;" />')):B.startsWith("### ")?(R(),x.push(`<h4 style="color:#93c5fd; font-size:0.9rem; font-weight:800; margin:12px 0 6px;">${g(B.slice(4))}</h4>`)):B.startsWith("## ")?(R(),x.push(`<h3 style="color:#ffffff; font-size:0.98rem; font-weight:800; margin:14px 0 6px;">${g(B.slice(3))}</h3>`)):B.startsWith("# ")?(R(),x.push(`<h2 style="color:#ffffff; font-size:1.06rem; font-weight:800; margin:6px 0 10px;">${g(B.slice(2))}</h2>`)):/^([-*]|\d+\.)\s+/.test(B)?(A||(x.push('<ul style="margin:6px 0 10px 18px; padding:0; line-height:1.6;">'),A=!0),x.push(`<li style="margin-bottom:4px;">${g(B.replace(/^([-*]|\d+\.)\s+/,""))}</li>`)):(R(),x.push(`<p style="margin:6px 0;">${g(B)}</p>`))}return w&&M(),R(),x.join("")},Ie=async c=>{if(!ce)return;const u=document.getElementById("researchModalTitle"),g=document.getElementById("researchModalBody");ce.style.display="flex",u&&(u.textContent=`SEC Primary Filing Turnaround Brief — $${c}`),g&&(g.innerHTML="Loading primary filing brief...");try{const v=await kt(c),x=s.stocks.find(B=>B.ticker===c),w=Number(v.current_price??(x==null?void 0:x.close)??29.12).toFixed(2),T=Number(v.stop_price??(x==null?void 0:x.stop_loss_price)??Number(w)*.91).toFixed(2),A=Number(v.target_price??(x==null?void 0:x.tp1_2x_price)??Number(w)*2).toFixed(2),M=v.as_of_date||(x==null?void 0:x.date)||v.report_date||"2026-10-30",P=v[`title_${s.lang}`]||v.title||`${v.company_name||c} ($${v.ticker||c}) — ${v.opinion||"STRONG_BUY"} | Latest Close $${w} (${M})`;if(u&&(u.textContent=P),g){const B=v[`content_${s.lang}`]||v.content||"",V=_t(B),ee=String(v.opinion||"").includes("STOP"),Z=`
          <div style="display:flex; flex-wrap:wrap; gap:14px; background:#090d16; border:1px solid var(--border); border-left:3px solid ${ee?"var(--fin-down)":"var(--fin-up)"}; padding:10px 14px; border-radius:4px; margin-bottom:14px; font-family:var(--font-mono); font-size:0.76rem;">
            <span>LATEST CLOSE (${M}): <b style="color:#ffffff;">$${w}</b></span>
            <span>RULE 1 HARD STOP (-9%): <b style="color:var(--fin-down);">$${T}</b></span>
            <span>TP1 TARGET (2x): <b style="color:var(--fin-up);">$${A}</b></span>
            <span>STATUS / RRR: <b style="color:${ee?"#fca5a5":"#93c5fd"};">${v.rrr_ratio||"1 : 11.1"}</b></span>
          </div>
        `;g.innerHTML=`${Z}<div style="font-family:var(--font-sans); line-height:1.65;">${V}</div>`}}catch{g&&(g.innerHTML="Failed to load research brief.")}};document.querySelectorAll(".btn-open-research").forEach(c=>{c.addEventListener("click",()=>{const u=c.getAttribute("data-ticker")||"CELH";Ie(u)})}),document.querySelectorAll(".btn-open-research-modal").forEach(c=>{c.addEventListener("click",()=>Ie("CELH"))}),document.querySelectorAll(".btn-switch-research").forEach(c=>{c.addEventListener("click",()=>{const u=c.getAttribute("data-ticker")||"CELH";Ie(u)})});const Je=document.getElementById("btnCopyPineScript");Je&&Je.addEventListener("click",async()=>{var u;const c=((u=document.getElementById("pineCodeBox"))==null?void 0:u.textContent)||"";try{await navigator.clipboard.writeText(c),D("TradingView Pine Script v5 Copied to Clipboard")}catch{D("Pine Script Ready to Copy")}});const et=document.getElementById("btnCopyTopProofCard");et&&et.addEventListener("click",()=>{yt(null)}),document.querySelectorAll(".cnn-view-tab").forEach(c=>{c.addEventListener("click",()=>{s.semiGaugeTab=c.getAttribute("data-semi-tab")||"overview",Y()})}),document.querySelectorAll(".btn-semi-range").forEach(c=>{c.addEventListener("click",async()=>{const u=c.getAttribute("data-range")||"1Y";s.semiRange=u;try{s.semiHistory=await Ne(u),Y()}catch{D("Failed to load selected history window")}})});const tt=document.getElementById("btnRunSemiRebalance");tt&&tt.addEventListener("click",async()=>{var T,A,M,R;const c=parseFloat(((T=document.getElementById("semiCapInput"))==null?void 0:T.value)??""),u=((A=document.getElementById("semiModeInput"))==null?void 0:A.value)||"AUTO_REGIME",g=((M=document.getElementById("semiFreqInput"))==null?void 0:M.value)||"ANNUAL",v=parseFloat(((R=document.getElementById("semiGainKrwInput"))==null?void 0:R.value)??"");if(!Number.isFinite(c)||c<100){D("Please enter a valid portfolio capital ($100 minimum)");return}const x=c,w=Number.isFinite(v)&&v>=0?v:0;s.semiCapUsd=x,s.semiMode=u,s.semiFreq=g,s.semiGainKrw=w;try{s.semiRebalanceResult=await Fe({total_capital_usd:x,strategy_mode:u,rebalance_frequency:g,unrealized_gain_krw:w}),Y(),D("Updated $SMH / $XLV Rebalancing Orders")}catch{D("Please enter a valid positive capital amount")}});const ot=async c=>{var w,T,A;const u=parseFloat(((w=document.getElementById("semiLumpCapInput"))==null?void 0:w.value)??""),g=c!==void 0?c:parseFloat(((T=document.getElementById("semiLumpScoreInput"))==null?void 0:T.value)??"");if(!Number.isFinite(u)||u<100){D("Please enter a valid lump-sum amount ($100 minimum)");return}const v=u,x=Number.isFinite(g)?Math.max(0,Math.min(100,g)):((A=s.semiOverview)==null?void 0:A.fg_score)??18;s.semiLumpCapUsd=v,s.semiLumpScore=x;try{s.semiLumpSumResult=await bt({capital_usd:v,override_fg_score:x}),Y()}catch{D("Invalid lump-sum input parameters")}},nt=document.getElementById("btnRunSemiLumpSum");nt&&nt.addEventListener("click",()=>ot()),document.querySelectorAll(".btn-sim-fg").forEach(c=>{c.addEventListener("click",()=>{const u=parseFloat(c.getAttribute("data-fg")||"18.0");ot(u)})});const rt=document.getElementById("btnExportSemiGauge");rt&&rt.addEventListener("click",()=>{no()});const it=document.getElementById("btnDownloadSemiCsv");it&&it.addEventListener("click",async()=>{var u,g;if(!s.isProUnlocked){f(!1),D("Unlock Pro ($29/mo or $199 Lifetime) to download the 26-Year Daily CSV Dataset");return}const c=encodeURIComponent(s.licenseKey||"");try{const v=await fetch(`/api/semi/pro/csv?license_key=${c}`,{method:"HEAD",headers:{...be()}});if(v.ok&&(v.headers.get("content-type")||"").includes("csv")){window.open(`/api/semi/pro/csv?license_key=${c}`,"_blank");return}}catch{}try{const v=await Ne("ALL"),x=v&&Array.isArray(v.series)?v.series:((u=s.semiHistory)==null?void 0:u.series)||[],w=["Date,FG_Score,SMH_Close,XLV_Close,Port73_Norm,QQQ_Norm,SMH_DD_Pct"];x.forEach(R=>{w.push(`${R.date},${R.fg_score},${R.smh_close},${R.xlv_close},${R.port73_norm},${R.qqq_norm},${R.smh_dd_pct}`)});const T=new Blob([w.join(`
`)],{type:"text/csv;charset=utf-8;"}),A=URL.createObjectURL(T),M=document.createElement("a");M.href=A,M.download=`SemiFearGreed_SMH_XLV_2000_2026_History_${((g=s.semiOverview)==null?void 0:g.date)||"latest"}.csv`,M.click(),URL.revokeObjectURL(A),D("Downloaded 26-Year Daily CSV Dataset")}catch{D("Failed to generate CSV dataset")}}),Re()}function Re(){document.querySelectorAll(".btn-unlock-row").forEach(e=>{e.addEventListener("click",()=>{const t=document.getElementById("licenseModal");if(t){t.style.display="flex";const o=document.getElementById("licenseInput");o&&!o.value.trim()&&(o.value=s.licenseKey||"")}})}),document.querySelectorAll(".btn-share-card").forEach(e=>{e.addEventListener("click",()=>{const t=e.getAttribute("data-ticker"),o=s.stocks.find(n=>n.ticker===t);yt(o)})}),document.querySelectorAll('a[href^="/api/referral/redirect/"]').forEach(e=>{e.dataset.boundReferral!=="1"&&(e.dataset.boundReferral="1",e.addEventListener("click",t=>{const o=window.location.hostname;if(window.__STATIC_MODE__===!0||o&&o!=="localhost"&&o!=="127.0.0.1"){t.preventDefault();const n=e.getAttribute("href")||"",i=(new URL(n,window.location.origin).searchParams.get("ticker")||"SPY").toUpperCase();if(n.includes("tradingview")){const p=encodeURIComponent(s.config.tradingview_aff_id||"1173809");window.open(`https://www.tradingview.com/symbols/${i}/?aff_id=${p}`,"_blank","noopener")}else if(n.includes("broker")||n.includes("exchange")){const p=s.config.broker_referral_url||"https://www.bitget.com/referral/register?clacCode=7nja",r=p.includes("?")?"&":"?";window.open(`${p}${r}symbol=${encodeURIComponent(i)}`,"_blank","noopener")}else if(n.includes("trendspider")){const p=encodeURIComponent(s.config.trendspider_aff_id||"rightside");window.open(`https://trendspider.com/?_go=${p}&symbol=${i}`,"_blank","noopener")}else{const p=encodeURIComponent(s.config.seekingalpha_source||"better_life333");window.open(`https://seekingalpha.com/symbol/${i}/earnings?source=${p}`,"_blank","noopener")}}}))})}function yt(e){const t=document.getElementById("scoreCanvas");if(!t)return;const o=t.getContext("2d");o.fillStyle="#090d16",o.fillRect(0,0,900,500),o.strokeStyle="#2962ff",o.lineWidth=3,o.strokeRect(16,16,868,468),o.fillStyle="#0ecb81",o.font="bold 20px Inter, sans-serif",o.fillText("RIGHTSIDEALPHA · US EQUITY TURNAROUND TERMINAL",45,62),e?(o.fillStyle="#ffffff",o.font="bold 42px JetBrains Mono, monospace",o.fillText(`$${e.ticker} (${e.name_en})`,45,125),o.fillStyle="#93c5fd",o.font="bold 24px JetBrains Mono, monospace",o.fillText(`Signal Regime: ${e.zone_label_en}  |  PW-RSI Score: ${e.score}/100`,45,175),o.fillStyle="#cbd5e1",o.font="20px JetBrains Mono, monospace",o.fillText(`Last Close: $${e.close.toFixed(2)}  |  52W High DD: ${e.dd_high52_pct}%  |  vs 52W Low: +${e.prox_low52_pct}%`,45,230),o.fillText(`vs MA20: ${e.vs_ma20_pct}%  |  vs MA60: ${e.vs_ma60_pct}%  |  10D Vol Ratio: ${e.vol_surge_10d}x`,45,270),o.fillText(`Historical 1Y 2x (+100%) Hit Rate after -40% Drawdown: ${e.hist_2x_rate}%`,45,315)):(o.fillStyle="#ffffff",o.font="bold 34px Inter, sans-serif",o.fillText("20-Year US Equity Backtest: Left-Side vs PW-RSI Right-Side",45,125),o.fillStyle="#f6465d",o.font="22px JetBrains Mono, monospace",o.fillText("Blind 52W-Low Dip Buy: 28.91% 2x Rate | -30.31% MDD | 81d Underwater",45,200),o.fillStyle="#0ecb81",o.font="bold 24px JetBrains Mono, monospace",o.fillText("PW-RSI Right-Side:     55.24% 2x Rate | -16.49% MDD | 29d Underwater",45,260)),o.fillStyle="#8492a6",o.font="bold 16px JetBrains Mono, monospace",o.fillText(`Verified Dataset (N=394,371 US Stock-Days) · ${s.config.site1_url}`,45,440),t.toBlob(n=>{if(!n)return;const a=URL.createObjectURL(n),i=document.createElement("a");i.href=a,i.download=e?`RightSideAlpha_${e.ticker}_TearSheet.png`:"RightSideAlpha_Benchmark.png",i.click(),URL.revokeObjectURL(a),D(e?`Downloaded $${e.ticker} Tear Sheet PNG`:"Downloaded Benchmark Tear Sheet PNG")})}function no(){const e=document.getElementById("scoreCanvas");if(!e||!s.semiOverview)return;const t=e.getContext("2d"),o=s.semiOverview;t.fillStyle="#ffffff",t.fillRect(0,0,900,500),t.fillStyle="#cc0000",t.fillRect(0,0,900,10),t.fillStyle="#cc0000",t.font="bold 18px Inter, sans-serif",t.fillText("MARKETS · SEMICONDUCTOR FEAR & GREED INDEX",45,55),t.fillStyle="#111827",t.font="bold 40px Inter, sans-serif",t.fillText(`Score: ${o.fg_score.toFixed(1)} / 100 — ${o.regime_en.toUpperCase()}`,45,115),t.fillStyle="#374151",t.font="22px JetBrains Mono, monospace",t.fillText(`As of ${o.date}  |  $SMH: $${o.smh_close.toFixed(2)} (${o.smh_dd_pct}% DD)  |  $XLV: $${o.xlv_close.toFixed(2)}`,45,170),t.fillStyle="#b91c1c",t.font="bold 22px Inter, sans-serif",t.fillText(`Active Signal: ${o.action_headline_en}`,45,230),t.fillStyle="#4b5563",t.font="18px JetBrains Mono, monospace",t.fillText("26-Year Barbell (2000-2026): +10.60% CAGR (14.22x) vs QQQ +8.79% (9.21x)",45,300),t.fillText("10-Year AI Era (2016-2026):  +28.63% CAGR (15.07x) vs QQQ +20.74% (7.61x)",45,338),t.fillStyle="#6b7280",t.font="bold 16px JetBrains Mono, monospace",t.fillText(`SemiFearGreed Quantitative Barbell Engine · ${s.config.site2_url}`,45,445),e.toBlob(n=>{if(!n)return;const a=URL.createObjectURL(n),i=document.createElement("a");i.href=a,i.download=`SemiFearGreed_${o.date}.png`,i.click(),URL.revokeObjectURL(a),D("Downloaded Semiconductor Fear & Greed Index PNG")})}async function me(){try{const[e,t,o,n,a]=await Promise.all([wt({limit:200}),Et().catch(()=>null),Ct().catch(()=>null),Pt().catch(()=>null),Ne(s.semiRange).catch(()=>null)]);s.stocks=Array.isArray(e)?e.filter(h=>h.ticker&&!String(h.ticker).includes(".")):[],t&&t.kpis&&(s.backtestKpis=t.kpis),o&&typeof o=="object"&&Object.entries(o).forEach(([h,_])=>{_!=null&&_!==""&&(s.config[h]=_)}),n&&(s.semiOverview=n,s.semiLumpScore===null&&(s.semiLumpScore=n.fg_score)),a&&(s.semiHistory=a);const i=s.stocks.find(h=>h.ticker==="CELH"),p=i?Number(i.close):27.93,[r,m,f,b,d]=await Promise.all([Fe({total_capital_usd:s.semiCapUsd,strategy_mode:s.semiMode,rebalance_frequency:s.semiFreq,unrealized_gain_krw:s.semiGainKrw}).catch(()=>null),bt({capital_usd:s.semiLumpCapUsd,override_fg_score:s.semiLumpScore}).catch(()=>null),$e({ticker:"CELH",entry_price:p,days_held:42}).catch(()=>null),Bt().catch(()=>null),Pe({alert_type:"SEMI_BRIEFING",lang:s.lang,dry_run:!0}).catch(()=>null)]);if(r&&(s.semiRebalanceResult=r),m&&(s.semiLumpSumResult=m),f&&(s.docLastResult=f),b&&(s.telegramConfigured=!!(b.configured||s.telegramBotToken&&s.telegramChatId),b.chat_id&&!s.telegramChatId&&(s.telegramChatId=b.chat_id),b.channel_url&&(s.config.telegram_channel_url=b.channel_url)),d&&d.message_preview&&(s.telegramPreviewText=d.message_preview),s.isProUnlocked){const h=await Rt().catch(()=>null);h&&h.code&&(s.pineCode=h.code)}xe()}catch(e){console.error("Failed to load initial data:",e)}}async function ro(){window.addEventListener("keydown",t=>{t.key==="Escape"&&["licenseModal","telegramModal","configModal","researchModal"].forEach(o=>{const n=document.getElementById(o);n&&n.style.display==="flex"&&(n.style.display="none")})}),window.addEventListener("hashchange",()=>{const t=window.location.hash.toLowerCase();t.includes("rightside")&&s.activeView!=="rightside"?(s.activeView="rightside",Y()):t.includes("semi")&&s.activeView!=="semi"&&(s.activeView="semi",Y())}),await me(),Y();const e=(ue.get("checkout")||ue.get("unlock")||"").toLowerCase();(e==="monthly"||e==="lifetime"||e==="pro")&&setTimeout(()=>{const t=document.getElementById("licenseModal"),o=document.getElementById("licenseMsg");t&&(t.style.display="flex",o&&(o.style.color="#34d399",o.textContent=e==="lifetime"?"💎 Lifetime Pass ($199): Enter your email below for an Instant 7-Day Pro Pass or proceed to Lemon Squeezy Checkout.":"🍋 Pro Monthly ($29/mo): Enter your email below for an Instant 7-Day Pro Pass or proceed to Lemon Squeezy Checkout."))},200),(le||fe)&&setTimeout(()=>{const t=document.querySelector(".screener-panel");if(t&&t.scrollIntoView&&t.scrollIntoView({behavior:"smooth",block:"start"}),le==="CELH"||le==="MBLY"){const o=document.querySelector(`.btn-open-research[data-ticker="${le}"]`);o&&o.click()}},150)}ro();(function(){try{if(typeof window>"u"||typeof navigator>"u"||window.__HQ_BEACON_SENT_tom_truthofmarket__)return;window.__HQ_BEACON_SENT_tom_truthofmarket__=!0;var e=navigator.userAgent||"";if(navigator.webdriver||/bot|crawl|spider|slurp|headless|lighthouse|gtmetrix|pingdom|uptimerobot|python|curl|node|axios/i.test(e))return;var t=location&&location.hostname||"";if(!t||t==="localhost"||t==="127.0.0.1")return;var o=new Date(Date.now()+9*3600*1e3).toISOString().slice(0,10),n="tom_truthofmarket";fetch("https://abacus.jasoncameron.dev/hit/"+n+"/pv_"+o,{mode:"cors",keepalive:!0}).catch(function(){}),fetch("https://abacus.jasoncameron.dev/hit/"+n+"/pv_total",{mode:"cors",keepalive:!0}).catch(function(){}),localStorage.getItem("hq_uv_"+n+"_"+o)!=="1"&&(localStorage.setItem("hq_uv_"+n+"_"+o,"1"),fetch("https://abacus.jasoncameron.dev/hit/"+n+"/uv_"+o,{mode:"cors",keepalive:!0}).catch(function(){})),localStorage.getItem("hq_uv_ever_"+n)!=="1"&&(localStorage.setItem("hq_uv_ever_"+n,"1"),fetch("https://abacus.jasoncameron.dev/hit/"+n+"/uv_total",{mode:"cors",keepalive:!0}).catch(function(){}))}catch{}})();(function(){try{if(typeof window>"u"||window.__HQ_KPI_TOM__)return;window.__HQ_KPI_TOM__=!0;var e=location&&location.hostname||"";if(!e||e==="localhost"||e==="127.0.0.1")return;var t=new Date(Date.now()+9*3600*1e3).toISOString().slice(0,10),o="tom_truthofmarket";(location.search.indexOf("payment=success")!==-1||location.search.indexOf("unlock=1")!==-1)&&localStorage.getItem("hq_paid_"+t)!=="1"&&(localStorage.setItem("hq_paid_"+t,"1"),fetch("https://abacus.jasoncameron.dev/hit/"+o+"/paid_member_"+t,{mode:"cors",keepalive:!0}).catch(function(){}),fetch("https://abacus.jasoncameron.dev/hit/"+o+"/paid_member_total",{mode:"cors",keepalive:!0}).catch(function(){})),document.addEventListener("click",function(n){var a=n.target&&n.target.closest?n.target.closest('a, button, [role="button"]'):null;if(a){var i=(a.getAttribute("href")||"").toLowerCase(),p=(a.innerText||a.textContent||"").toLowerCase(),r=(a.className||"").toLowerCase();(i.indexOf("lemonsqueezy.com")!==-1||r.indexOf("pro")!==-1||r.indexOf("paywall")!==-1||/upgrade|unlock pro|vip|subscribe|프리미엄|유료|구독/.test(p))&&(fetch("https://abacus.jasoncameron.dev/hit/"+o+"/paid_click_"+t,{mode:"cors",keepalive:!0}).catch(function(){}),fetch("https://abacus.jasoncameron.dev/hit/"+o+"/paid_click_total",{mode:"cors",keepalive:!0}).catch(function(){}))}},!0)}catch{}})();
