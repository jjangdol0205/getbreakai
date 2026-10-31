(function(){const t=document.createElement("link").relList;if(t&&t.supports&&t.supports("modulepreload"))return;for(const i of document.querySelectorAll('link[rel="modulepreload"]'))n(i);new MutationObserver(i=>{for(const a of i)if(a.type==="childList")for(const l of a.addedNodes)l.tagName==="LINK"&&l.rel==="modulepreload"&&n(l)}).observe(document,{childList:!0,subtree:!0});function o(i){const a={};return i.integrity&&(a.integrity=i.integrity),i.referrerPolicy&&(a.referrerPolicy=i.referrerPolicy),i.crossOrigin==="use-credentials"?a.credentials="include":i.crossOrigin==="anonymous"?a.credentials="omit":a.credentials="same-origin",a}function n(i){if(i.ep)return;i.ep=!0;const a=o(i);fetch(i.href,a)}})();const W={en:{brandSubtitle:"US EQUITY QUANTITATIVE TERMINAL · v2.6",navRightSide:"RightSideAlpha · US Equities",navSemiFg:"SemiFearGreed · CNN-Style Index",marketUniverseTag:"NYSE & NASDAQ · 72 US EQUITIES",statusFree:"PUBLIC ACCESS",statusPro:"PRO TERMINAL ACTIVE",btnLicense:"License Key",btnAdmin:"Terminal Config",btnUnlockPro:"Upgrade to Pro ($29/mo)",heroTag:"INSTITUTIONAL TURNAROUND RESEARCH · 394,371 US STOCK-DAYS VERIFIED (2006–2026)",heroTitle:"Systematic Right-Side Ignition for US-Listed Equities.",heroDesc:"Blindly buying 52-week lows in US growth equities traps capital for a median of 81 trading days with a -30.3% post-entry drawdown. RightSideAlpha isolates post-washout (1.40x+ volume) breakouts reclaiming the 20-day and 60-day moving averages across 72 liquid NYSE & NASDAQ equities.",kpi1_label:"PW-RSI 1Y 2x (+100%) Hit Rate",kpi1_sub:"vs 28.91% blind 52W-low dip buying",kpi2_label:"Median Days Underwater",kpi2_sub:"Reduced from 81.0 days via 55D Time-Stop",kpi3_label:"26.8-Yr US-Only Net CAGR",kpi3_sub:"80.5x net cumulative after 22% tax & slippage",kpi4_label:"Severe Drawdown (≤ -20%) Rate",kpi4_sub:"vs 24.82% without -9% hard stop & EPS filter",proofHeading:"Empirical Performance Matrix · Left-Side Dip Buying vs. PW-RSI Right-Side Ignition",proofCopyScorecardBtn:"Export Benchmark Tear Sheet (PNG)",th_arch:"Entry Methodology (US Equities, N = 394,371 Stock-Days)",th_2x:"1Y 2x (+100%) Rate",th_med:"1Y Median Return",th_mdd:"Post-Entry Median MDD",th_dead:"Days Underwater",th_trap:"1Y Tail Loss (≤ -20%)",searchPlaceholder:"Filter by US Ticker, Company, or GICS Sector (e.g. NVDA, CELH, Semiconductors)...",filterAll:"All US Equities",filterIgnition:"Right-Side Ignition",filterWatch:"Washout Base Watch",filterKnife:"Downtrend / Avoid",filterTrap:"Value Trap Excluded",colTicker:"Security / Sector",colZone:"Regime & Factor Checklist",colScore:"Quant Score",colClose:"Last Close & 52W Range",colProx:"vs 52W Low",colDD:"52W Drawdown",colMA:"vs MA20 / MA60",colVol:"10D Vol Ratio",colHist:"Hist 2x Rate",colTrigger:"Execution Levels (Trigger / Stop)",colActions:"Research & Execution",vaultBadgeLocked:"PRO ANALYTICS TERMINAL · LOCKED (ENTER LICENSE KEY)",vaultBadgeUnlocked:"PRO ANALYTICS TERMINAL · FULL INSTITUTIONAL ACCESS",vaultTitle:"Institutional Execution & Risk Management Suite",vaultUnlockBtn:"Demo Unlock (Key: PRO-DEMO-2026)",tool1Title:"MODULE 01 · POSITION RISK & 55-DAY TIME-STOP ENGINE",tool1Sub:"Asymmetric Exit & Opportunity-Cost Diagnostic",tool1Desc:"Input your US equity cost basis and holding period. Evaluates the 4 quantitative exit rules (-9% Capital Protection Stop, 55-Day +8% Time-Stop, 25-Day Momentum Switch, and +100% TP1 Principal Harvest).",tool1Btn:"Run Position Diagnostic",tool2Title:"MODULE 02 · SEC FILING TURNAROUND RESEARCH",tool2Sub:"10-K / 10-Q / 8-K Primary Source Equity Briefs",tool2Desc:"Updated at 08:10 EST from primary SEC filings and institutional consensus revisions (zero retail media noise):",tool2ViewBtn:"Open Institutional Research Archive",tool3Title:"MODULE 03 · TRADINGVIEW PINE SCRIPT v5 OVERLAY",tool3Sub:"Automated MA20/MA60 Ignition & Washout Plotter",tool3Desc:"Deploy directly into TradingView Pine Editor to plot right-side MA20/MA60 breakouts, 1.40x volume washouts, and -9% hard stop levels on any US stock:",tool3CopyBtn:"Copy Pine Script v5 Source",crossTitle:"COMPANION MARKET SENTIMENT PLATFORM · SEMIFEARGREED",crossHeading:"Allocating to Semiconductor & Healthcare ETFs ($SMH / $XLV / $SOXX)?",crossDesc:"Open our CNN-style Semiconductor 7-Factor Fear & Greed Index and 26-year $SMH 70% : $XLV 30% contrarian rebalancing terminal.",crossBtn:"Switch to SemiFearGreed Index",cnnBadge:"MARKETS · SEMICONDUCTOR & AI SENTIMENT",cnnTitle:"Semiconductor Fear & Greed Index",cnnSubtitle:"What emotion is driving the chip & AI hardware market now?",cnnTabOverview:"Overview",cnnTabTimeline:"Timeline",cnnLastUpdated:"Last updated",cnnExportGauge:"Export Index Card (PNG)",cnnHistoryTitle:"Historical Sentiment Comparison",cnnActiveRuleLabel:"ACTIVE BARBELL ALLOCATION SIGNAL",cnnIndicatorsHeading:"7 Semiconductor Fear & Greed Indicators",cnnIndicatorsSub:"How the index is calculated: Equal-transparent 7-factor rolling 3-year (756-day) percentile & z-score composite of $SMH, $XLV, and $QQQ.",rebalSectionTag:"BARBELL ASSET ALLOCATION & TAX OPTIMIZER",rebalSectionTitle:"$SMH + $XLV Contrarian Rebalancing Engine (70:30 ↔ 80:20)",rebalSectionDesc:"Combine high-beta AI semiconductor growth ($SMH 70%) with low-beta healthcare cash-flow defense ($XLV 30%). Automatically shift to 80:20 when Fear & Greed drops below 25 or $SMH falls -20% off its 52-week high.",lumpSectionTag:"CAPITAL DEPLOYMENT PROTOCOL",lumpSectionTitle:"3-Stage Lump-Sum Entry Planner",lumpSectionDesc:"Eliminate timing regret when deploying new cash. Automatically calculates Day-1 immediate entry vs. USD RP reserve tranches based on the live or simulated Fear & Greed score.",eraSectionTag:"26-YEAR EMPIRICAL VERIFICATION (2000–2026)",eraSectionTitle:"$SMH 70% : $XLV 30% (80:20 Crash Tilt) vs. 100% $QQQ Benchmark",eraSectionDesc:"Verified across 6,625 trading days including the 2000 Dot-Com Bust, 2008 GFC, 2020 Pandemic, and 2022 Rate Shock.",disclaimer:"Regulatory & Compliance Disclosure: RightSideAlpha and SemiFearGreed are quantitative financial data analytics and historical backtesting software tools. Nothing on this platform constitutes personalized investment, legal, or tax advice. All regime classifications and technical levels are mathematical outputs derived from historical price and volume series. Past performance (2000–2026) is not indicative of future results.",copyright:"© 2026 RightSideAlpha & SemiFearGreed Quantitative Analytics. Merchant of Record: Lemon Squeezy."},jp:{brandSubtitle:"米国株クオンツ分析ターミナル · v2.6",navRightSide:"RightSideAlpha · 米国株スクリーナー",navSemiFg:"SemiFearGreed · 半導体恐怖＆強欲指数",marketUniverseTag:"NYSE & NASDAQ · 米国上場 72銘柄限定",statusFree:"パブリックティア",statusPro:"PRO ターミナル有効",btnLicense:"ライセンス認証",btnAdmin:"ターミナル設定",btnUnlockPro:"Proへアップグレード ($29/月)",heroTag:"機関投資家向けターンアラウンド分析 · 米国株 394,371営業日検証済 (2006–2026)",heroTitle:"米国上場株に特化した「右側イグニッション」定量スクリーナー",heroDesc:"米国グロース株の単純な52週安値買い（左側逆張り）は、中央値81営業日の資金拘束と平均-30.3%の追加下落を招きます。RightSideAlphaはNYSE・NASDAQ上場72銘柄を対象に、出来高1.4倍以上のセリングクライマックス後に20日・60日移動平均線を同時突破する初動銘柄のみを抽出します。",kpi1_label:"PW-RSI 1年 2倍 (+100%) 到達率",kpi1_sub:"単純な52週安値買い (28.91%) との比較",kpi2_label:"含み損拘束期間（中央値）",kpi2_sub:"55日タイムストップにより81.0日から短縮",kpi3_label:"26.8年間 米国株純CAGR",kpi3_sub:"税金22%・スリッページ控除後 累計80.5倍",kpi4_label:"深刻な下落 (≤ -20%) 発生率",kpi4_sub:"-9%ハード損切＆業績フィルタ適用時",proofHeading:"20年実証パフォーマンス比較 · 左側安値買い vs PW-RSI 右側イグニッション",proofCopyScorecardBtn:"検証ティアシート出力 (PNG)",th_arch:"エントリー手法 (米国株, N = 394,371営業日)",th_2x:"1年 2倍 (+100%) 確率",th_med:"1年 リターン中央値",th_mdd:"エントリー後 MDD中央値",th_dead:"含み損日数",th_trap:"1年 重大損失 (≤ -20%)",searchPlaceholder:"米国ティッカー、企業名、セクターで検索 (例: NVDA, CELH, Semiconductors)...",filterAll:"全米国株",filterIgnition:"右側イグニッション",filterWatch:"クライマックス監視",filterKnife:"下降トレンド・回避",filterTrap:"バリュートラップ除外",colTicker:"銘柄 / セクター",colZone:"レジーム＆条件判定",colScore:"クオンツスコア",colClose:"終値 ($USD) & 52週レンジ",colProx:"対52週安値",colDD:"52週高値比DD",colMA:"対MA20 / MA60",colVol:"10日出来高倍率",colHist:"過去2倍確率",colTrigger:"執行価格 (突破 / -9%損切)",colActions:"調査＆チャート",vaultBadgeLocked:"PRO アナリティクスターミナル · ロック中 (要ライセンスキー)",vaultBadgeUnlocked:"PRO アナリティクスターミナル · 全機能アンロック済",vaultTitle:"機関投資家向けエグゼキューション＆リスク管理スイート",vaultUnlockBtn:"デモ解除 (キー: PRO-DEMO-2026)",tool1Title:"MODULE 01 · ポジションリスク＆55日タイムストップ診断",tool1Sub:"非対称エグジット＆機会損失シミュレーター",tool1Desc:"米国株の取得単価と保有営業日数を入力してください。4大定量エグジット原則（-9%ハード損切、55日+8%タイムストップ、25日モメンタム乗換、+100%元本回収）を即時判定します。",tool1Btn:"ポジション診断を実行",tool2Title:"MODULE 02 · SEC一次開示ターンアラウンド調査レポート",tool2Sub:"10-K / 10-Q / 8-K ファンダメンタルズ分析アーカイブ",tool2Desc:"二次メディアのノイズを排除し、SEC一次開示資料とEPSコンセンサス修正から毎朝更新：",tool2ViewBtn:"機関投資家向け調査レポートを開く",tool3Title:"MODULE 03 · TRADINGVIEW PINE SCRIPT v5 インジケーター",tool3Sub:"MA20/MA60 右側突破＆出来高クライマックス自動描画",tool3Desc:"TradingViewのPineエディタに貼り付けるだけで、MA20/MA60突破シグナルと-9%ストップラインをチャート上に描画します：",tool3CopyBtn:"Pine Script v5 コードをコピー",crossTitle:"姉妹センチメント分析プラットフォーム · SEMIFEARGREED",crossHeading:"半導体ETF・ヘルスケアETF ($SMH / $XLV / $SOXX) に投資していますか？",crossDesc:"CNNスタイルの半導体7ファクター恐怖＆強欲指数と、26年間検証済みの$SMH 70% : $XLV 30% 逆張りリバランス計算機へ切り替えられます。",crossBtn:"SemiFearGreed インデックスを開く",cnnBadge:"MARKETS · 半導体＆AI市場センチメント",cnnTitle:"Semiconductor Fear & Greed Index",cnnSubtitle:"いま半導体・AI市場を動かしている感情は「恐怖」か「強欲」か？",cnnTabOverview:"オーバービュー (Overview)",cnnTabTimeline:"タイムライン推移 (Timeline)",cnnLastUpdated:"最終更新",cnnExportGauge:"ゲージカード出力 (PNG)",cnnHistoryTitle:"過去センチメント比較",cnnActiveRuleLabel:"現在のバーベル配分シグナル",cnnIndicatorsHeading:"半導体 恐怖＆強欲指数を構成する7つの指標",cnnIndicatorsSub:"算出方法：$SMH・$XLV・$QQQの過去3年間（756営業日）ローリングパーセンタイルとZスコアを組み合わせた7ファクター加重平均モデル。",rebalSectionTag:"バーベル資産配分＆節税シミュレーター",rebalSectionTitle:"$SMH + $XLV 逆張りリバランス計算機 (70:30 ↔ 80:20)",rebalSectionDesc:"高成長AI半導体($SMH 70%)とディフェンシブなヘルスケア($XLV 30%)を結合。指数25以下または$SMH高値比-20%下落時に80:20へ逆張りシフトします。",lumpSectionTag:"新規資金エントリープロトコル",lumpSectionTitle:"3段階 一括資金エントリープランナー",lumpSectionDesc:"現在の恐怖＆強欲スコアに応じて、初日即時投入枠と米ドルMMF待機枠の最適比率を算出します。",eraSectionTag:"26年間（2000–2026）実証バックテスト",eraSectionTitle:"$SMH 70% : $XLV 30% (暴落時80:20) vs 100% $QQQ ベンチマーク比較",eraSectionDesc:"ITバブル崩壊、リーマンショック、コロナ危機、2022年半導体不況を含む6,625営業日の完全検証データ。",disclaimer:"コンプライアンス免責事項：RightSideAlphaおよびSemiFearGreedは定量金融データ分析および過去バックテスト用のソフトウェアツールです。当プラットフォームのいかなる情報も個別の投資助言や税務助言を構成しません。",copyright:"© 2026 RightSideAlpha & SemiFearGreed Quantitative Analytics. Merchant of Record: Lemon Squeezy."},kr:{brandSubtitle:"미국 상장주식 전용 퀀트 터미널 · v2.6",navRightSide:"RightSideAlpha · 미국주식 알파 터미널",navSemiFg:"SemiFearGreed · 반도체 공포·탐욕 지수",marketUniverseTag:"NYSE & NASDAQ · 미국 상장 72개 핵심 종목 한정",statusFree:"퍼블릭 티어",statusPro:"PRO 터미널 활성화",btnLicense:"라이선스 인증",btnAdmin:"터미널 설정",btnUnlockPro:"Pro 업그레이드 ($29/월)",heroTag:"기관급 턴어라운드 리서치 · 미국 상장주식 394,371 거래일 전수 검증 (2006–2026)",heroTitle:"미국 상장주식에 최적화된 우측 변곡점(PW-RSI) 정량 분석 플랫폼",heroDesc:"미국 성장주를 단순 52주 신저가(좌측 구간)에 매수하면 중앙값 81거래일의 자금 묶임(데드머니)과 -30.3%의 추가 낙폭에 노출됩니다. RightSideAlpha는 NYSE·NASDAQ 상장 72개 핵심 종목만을 대상으로 1.4배 이상 거래량 투매(Washout) 후 20일·60일 이동평균선을 동시 탈환하는 우측 초동 시그널을 판독합니다.",kpi1_label:"PW-RSI 1년 2배 (+100%) 도달률",kpi1_sub:"단순 52주 신저가 좌측 매수(28.91%) 대비",kpi2_label:"보유 후 물림 기간 (중앙값)",kpi2_sub:"55일 시간손절 원칙으로 81.0일에서 단축",kpi3_label:"26.8개년 미국주식 순 CAGR",kpi3_sub:"양도세 22%·슬리피지 차감 후 누적 80.5배",kpi4_label:"심각한 손실 (≤ -20%) 발생 확률",kpi4_sub:"-9% 손절 및 실적 턴어라운드 필터 적용 시",proofHeading:"20년 실증 백테스트 매트릭스 · 좌측 신저가 매수 vs PW-RSI 우측 시동 모델",proofCopyScorecardBtn:"백테스트 티어시트 저장 (PNG)",th_arch:"진입 방법론 (미국 상장주, N = 394,371 거래일)",th_2x:"1년 2배 (+100%) 확률",th_med:"1년 수익률 중앙값",th_mdd:"진입 후 MDD 중앙값",th_dead:"자금 물림 기간",th_trap:"1년 치명적 손실 (≤ -20%)",searchPlaceholder:"미국 티커, 기업명, 섹터 검색 (예: NVDA, CELH, Semiconductors)...",filterAll:"미국 전체 종목",filterIgnition:"우측 돌파 시동 (Ignition)",filterWatch:"워시아웃 베이스 대기",filterKnife:"좌측 하락추세 · 주의",filterTrap:"밸류트랩 배제 종목",colTicker:"종목 / GICS 섹터",colZone:"시그널 레짐 & 4대 조건",colScore:"퀀트 스코어",colClose:"종가 ($USD) & 52주 밴드",colProx:"52주 저점 이격",colDD:"52주 고점 낙폭",colMA:"20일 / 60일선 괴리",colVol:"10일 거래량 배율",colHist:"과거 2배 확률",colTrigger:"실행 타점 (60일 돌파 / -9% 손절)",colActions:"리포트 & 차트 연동",vaultBadgeLocked:"PRO 애널리틱스 터미널 · 잠김 (라이선스 키 입력 필요)",vaultBadgeUnlocked:"PRO 애널리틱스 터미널 · 전 기능 활성화됨",vaultTitle:"기관급 포지션 리스크 관리 & SEC 1차 공시 리서치 스위트",vaultUnlockBtn:"데모 즉시 해제 (키: PRO-DEMO-2026)",tool1Title:"MODULE 01 · 보유 포지션 리스크 & 55일 시간손절 판독기",tool1Sub:"비대칭 청산 원칙 및 기회비용 정밀 진단",tool1Desc:"미국 주식 매수 단가($)와 보유 거래일수를 입력하세요. 4대 정량 청산 원칙(-9% 칼손절 방어, 55일 +8% 미만 시간손절, 25일 모멘텀 교체, +100% 도달 시 원금 반절 회수)을 즉시 산출합니다.",tool1Btn:"보유 포지션 정밀 진단 실행",tool2Title:"MODULE 02 · SEC 1차 공시 기반 턴어라운드 리서치",tool2Sub:"10-K / 10-Q / 8-K 원문 기반 기관급 종목 분석 브리프",tool2Desc:"2차 언론 노이즈를 배제하고 미국 SEC 1차 공시와 컨센서스 EPS 상향 데이터를 바탕으로 매일 08:10 업데이트됩니다:",tool2ViewBtn:"기관급 턴어라운드 리포트 열람",tool3Title:"MODULE 03 · TRADINGVIEW PINE SCRIPT v5 전용 지표",tool3Sub:"MA20/MA60 우측 돌파 및 거래량 워시아웃 자동 차트 표시",tool3Desc:"트레이딩뷰 Pine 에디터에 붙여넣어 미국 전 종목 차트에 우측 시동 타점과 -9% 손절 라인을 자동 표시합니다:",tool3CopyBtn:"Pine Script v5 소스코드 복사",crossTitle:"연계 섹터 심리 & 자산배분 플랫폼 · SEMIFEARGREED",crossHeading:"반도체 ETF와 헬스케어 ETF ($SMH / $XLV / $SOXX)로 꾸준한 복리 수익을 원하시나요?",crossDesc:"CNN Fear & Greed 스타일의 반도체 7팩터 공포·탐욕 지수와 26년 검증된 $SMH 70% : $XLV 30% (폭락장 80:20) 역발상 리밸런싱 플랫폼으로 이동하세요.",crossBtn:"SemiFearGreed 지수 플랫폼 열기",cnnBadge:"MARKETS · 반도체 & AI 섹터 투자심리 지수",cnnTitle:"Semiconductor Fear & Greed Index",cnnSubtitle:"지금 반도체와 AI 시장을 움직이는 감정은 '공포'입니까, '탐욕'입니까?",cnnTabOverview:"오버뷰 (Overview)",cnnTabTimeline:"타임라인 추이 (Timeline)",cnnLastUpdated:"최근 업데이트",cnnExportGauge:"공포·탐욕 지수 카드 저장 (PNG)",cnnHistoryTitle:"시점별 지수 히스토리 비교",cnnActiveRuleLabel:"현재 발동 중인 바벨 자산배분 시그널",cnnIndicatorsHeading:"반도체 공포·탐욕 지수를 구성하는 7대 핵심 지표",cnnIndicatorsSub:"산출 방식: $SMH, $XLV, $QQQ의 최근 3년(756거래일) 롤링 백분위와 Z-스코어를 결합한 7팩터 정량 모델입니다.",rebalSectionTag:"바벨 자산배분 & 해외주식 절세 계산기",rebalSectionTitle:"$SMH + $XLV 역발상 리밸런싱 계산기 (70:30 ↔ 80:20)",rebalSectionDesc:"고성장 AI 반도체($SMH 70%)와 방어형 헬스케어($XLV 30%)를 결합하여 매년 꾸준한 복리 수익을 추구합니다. 공포지수 25 이하 또는 $SMH 고점 대비 -20% 하락 시 80:20으로 역발상 스위칭합니다.",lumpSectionTag:"신규 거치식 자금 투입 프로토콜",lumpSectionTitle:"3단계 일시금(Lump-Sum) 진입 플래너",lumpSectionDesc:"목돈을 한 번에 넣을 때 고점 물림을 방지합니다. 현재(또는 시뮬레이션) 공포·탐욕 점수에 따라 당일 즉시 진입 물량과 달러 RP 파킹 물량을 자동 계산합니다.",eraSectionTag:"26개년(2000–2026) 실증 백테스트 검증",eraSectionTitle:"$SMH 70% : $XLV 30% (폭락장 80:20) vs 100% $QQQ 장기 성과 비교",eraSectionDesc:"2000년 닷컴버블, 2008년 금융위기, 2020년 팬데믹, 2022년 금리인상기를 모두 포함한 6,625거래일 실증 데이터입니다.",disclaimer:"법적 고지 및 면책조항: RightSideAlpha와 SemiFearGreed는 정량적 금융 데이터 분석 및 역사적 백테스트 소프트웨어 도구입니다. 본 웹사이트의 어떠한 내용도 개별 투자자를 위한 맞춤형 투자 권유나 세무 자문을 구성하지 않습니다. 과거 백테스트 성과(2000–2026)는 미래 수익을 보장하지 않습니다.",copyright:"© 2026 RightSideAlpha & SemiFearGreed Quantitative Analytics. Merchant of Record: Lemon Squeezy."}};function X(){const e=localStorage.getItem("rsa_token")||(localStorage.getItem("rsa_pro_unlocked")==="true"?"PRO-DEMO-2026":"");return e?{Authorization:`Bearer ${e}`}:{}}function se(){return!!(localStorage.getItem("rsa_token")||(localStorage.getItem("rsa_pro_unlocked")==="true"?"PRO-DEMO-2026":""))}function le(){if(typeof window>"u")return!1;if(window.__STATIC_MODE__===!0)return!0;const e=window.location.hostname||"";return!(!e||e==="localhost"||e==="127.0.0.1")}async function M(e,t,o){if(le())return o();try{const n=await fetch(e,t);if(n.ok&&(n.headers.get("content-type")||"").includes("application/json"))return await n.json()}catch{}return o()}let q=null,Q=null;async function ce(){return q||(q=await(await fetch("./static_api/stocks_pro.json")).json()),q}async function ee(){return Q||(Q=await(await fetch("./static_api/semi_overview.json")).json()),Q}async function de(e={}){const t=new URLSearchParams;e.search&&t.append("search",e.search),e.zone&&e.zone!=="ALL"&&t.append("zone",e.zone),e.sort_by&&t.append("sort_by",e.sort_by),e.order&&t.append("order",e.order),e.limit&&t.append("limit",e.limit),e.offset&&t.append("offset",e.offset);const o=`/api/stocks${t.toString()?`?${t.toString()}`:""}`;return M(o,{headers:{...X(),Accept:"application/json"}},async()=>{const n=se()?"./static_api/stocks_pro.json":"./static_api/stocks_free.json";let a=await(await fetch(n)).json();if(e.search){const l=String(e.search).trim().toLowerCase();a=a.filter(c=>c.ticker&&c.ticker.toLowerCase().includes(l)||c.name&&c.name.toLowerCase().includes(l)||c.sector&&c.sector.toLowerCase().includes(l))}if(e.zone&&e.zone!=="ALL"&&(a=a.filter(l=>l.zone===e.zone)),e.sort_by){const l=e.sort_by,c=String(e.order||"desc").toLowerCase()!=="asc";a=[...a].sort((f,s)=>{const p=Number(f[l]??0),h=Number(s[l]??0);return c?h-p:p-h})}return a})}async function pe(){return M("/api/backtest",{headers:{Accept:"application/json"}},async()=>(await fetch("./static_api/backtest.json")).json())}async function me(e){const t=String(e||"CELH").trim().toUpperCase();return M(`/api/research/${encodeURIComponent(t)}`,{headers:{...X(),Accept:"application/json"}},async()=>(await fetch(`./static_api/research_${t==="MBLY"?"MBLY":"CELH"}.json`)).json())}async function fe(e){return M("/api/auth/license/validate",{method:"POST",headers:{"Content-Type":"application/json",Accept:"application/json"},body:JSON.stringify({license_key:e})},async()=>{const t=String(e||"").trim(),o=t.toUpperCase()==="PRO-DEMO-2026"||t.length>=10&&t.includes("-");return{valid:o,tier:o?"pro":"free",message:o?"Pro Terminal License Verified.":"Invalid license key. Use PRO-DEMO-2026 for demo."}})}async function ue(){return M("/api/pro/pinescript",{headers:{...X(),Accept:"application/json"}},async()=>(await fetch("./static_api/pinescript.json")).json())}async function K(e){return M("/api/pro/position-doctor",{method:"POST",headers:{...X(),"Content-Type":"application/json",Accept:"application/json"},body:JSON.stringify(e)},async()=>{const t=await ce(),o=String(e.ticker||"CELH").trim().toUpperCase(),n=t.find(h=>h.ticker===o),i=Math.max(.01,Number(e.entry_price||27.93)),a=Number(e.days_held||0),l=n?Number(n.close):i,c=n&&n.date?n.date:"2026-10-13",f=Number(((l/i-1)*100).toFixed(2)),s=Number((i*.91).toFixed(2)),p=Number((i*2).toFixed(2));return f<=-9?{ticker:o,status_code:"CRITICAL_STOP",status_label:"🛑 Hard Stop Loss Triggered",return_pct:f,rule_triggered:"Rule 1 (-9.0% Hard Stop Loss)",action_plan:"Execute immediate market exit. Do not average down on broken support.",is_critical:!0,current_price:l,entry_price:Number(i.toFixed(2)),stop_price:s,tp1_price:p,as_of_date:c}:a>=55&&f<8?{ticker:o,status_code:"DEAD_MONEY",status_label:"⏳ 55-Day Time Stop Triggered",return_pct:f,rule_triggered:"Rule 2 (55-Day Dead-Money Exit)",action_plan:"Exit position. Rebound momentum has stalled; reallocate into active right-side ignition candidates.",is_critical:!1,current_price:l,entry_price:Number(i.toFixed(2)),stop_price:s,tp1_price:p,as_of_date:c}:f>=100?{ticker:o,status_code:"TP1_REACHED",status_label:"🎯 100% Target Price 1 Achieved",return_pct:f,rule_triggered:"Rule 3 (+100% Principal Recovery)",action_plan:"Sell 50% of position to recoup 100% initial capital. Set trailing stop on remaining 50% using MA60.",is_critical:!1,current_price:l,entry_price:Number(i.toFixed(2)),stop_price:s,tp1_price:p,as_of_date:c}:{ticker:o,status_code:"ACTIVE_HOLD",status_label:"🟢 Active Right-Side Trend Follow",return_pct:f,rule_triggered:"Rule 4 (Healthy Trend Follow)",action_plan:"Maintain position. Monitor MA20/MA60 trailing support; runner target is +100% TP1.",is_critical:!1,current_price:l,entry_price:Number(i.toFixed(2)),stop_price:s,tp1_price:p,as_of_date:c}})}async function ge(){return M("/api/referral/config",{headers:{Accept:"application/json"}},async()=>(await fetch("./static_api/referral_config.json")).json())}async function ve(e){return M("/api/referral/config",{method:"POST",headers:{"Content-Type":"application/json",Accept:"application/json"},body:JSON.stringify(e)},async()=>({status:"updated",config:e}))}async function he(){return M("/api/semi/overview",{headers:{Accept:"application/json"}},async()=>ee())}async function te(e="1Y"){const t=String(e||"1Y").trim().toUpperCase(),n=["3M","6M","1Y","3Y","5Y","10Y","ALL"].includes(t)?t:"1Y";return M(`/api/semi/history?range=${encodeURIComponent(n)}`,{headers:{Accept:"application/json"}},async()=>(await fetch(`./static_api/semi_history_${n}.json`)).json())}async function oe(e){return M("/api/semi/rebalance",{method:"POST",headers:{"Content-Type":"application/json",Accept:"application/json"},body:JSON.stringify(e)},async()=>{const t=await ee(),o=Number(t.fg_score??18),n=Number(t.smh_dd_pct??-19.03),i=Number(t.usdkrw??1324.75),a=Number(t.smh_close??541.62),l=Number(t.xlv_close??179.28),c=String(e.strategy_mode||"AUTO_REGIME").trim().toUpperCase(),f=o<25||n<=-19;let s=.7,p=.3,h="",r="",v="";c==="BASELINE_70_30"?(s=.7,p=.3,h="Fixed 70% $SMH : 30% $XLV Golden Barbell Baseline",r="70% $SMH : 30% $XLV 基本黄金バーベル比率",v="평시 70% $SMH : 30% $XLV 기본 황금 바벨 비중"):c==="CONTRARIAN_80_20"?(s=.8,p=.2,h="Contrarian 80% $SMH : 20% $XLV Crash Accumulation Tilt",r="80% $SMH : 20% $XLV 暴落時・逆張り買い増しモード",v="80% $SMH : 20% $XLV 폭락장 역발상 매집 비중"):c==="AGGRESSIVE_90_10"?(s=.9,p=.1,h="90% $SMH : 10% $XLV Right-Side Momentum Tilt",r="90% $SMH : 10% $XLV 右側モメンタム集中モード",v="90% $SMH : 10% $XLV 우측 시동 공격형 비중"):f?(s=.8,p=.2,h=`AUTO REGIME: Extreme Fear (${o}/100, DD ${n.toFixed(1)}%) → 80% $SMH : 20% $XLV Contrarian Shift`,r=`自動判定: 極度の恐怖 (${o}/100, 高値比 ${n.toFixed(1)}%) → 80% $SMH : 20% $XLV 逆張り転換`,v=`자동 판독: 극단적 공포 (${o}/100, 낙폭 ${n.toFixed(1)}%) → 80% $SMH : 20% $XLV 역발상 비중 확대`):(s=.7,p=.3,h=`AUTO REGIME: Standard Regime (${o}/100) → 70% $SMH : 30% $XLV Core Barbell`,r=`自動判定: 通常レジーム (${o}/100) → 70% $SMH : 30% $XLV 基本比率`,v=`자동 판독: 평시 구간 (${o}/100) → 70% $SMH : 30% $XLV 기본 황금비중`);const g=Math.max(100,Number(e.total_capital_usd||1e5)),x=Number((g*s).toFixed(2)),E=Number((g*p).toFixed(2)),k=Math.floor(x/a),S=Math.floor(E/l),T=k*a+S*l,R=Number(Math.max(0,g-T).toFixed(2)),A=Number(t.natural_smh_weight_pct??64.9)/100,O=Number((g*A).toFixed(2)),H=Number((g*(1-A)).toFixed(2)),P=Number((x-O).toFixed(2)),B=Number((E-H).toFixed(2)),V=Math.round(P/a),G=Math.round(B/l),u=String(e.rebalance_frequency||"ANNUAL").trim().toUpperCase(),b={ANNUAL:.19,QUARTERLY:.42,MONTHLY:.78,WEEKLY:1.32}[u]??.19,y=Number((22.98-b).toFixed(2)),_=25e5,$=Math.max(0,Number(e.unrealized_gain_krw??38e5)),w=Math.max(0,$-_),L=Math.round(Math.min($,_)*.22),N=$<=_?`Unrealized gain (₩${$.toLocaleString()}) is within the ₩2,500,000 annual tax-free allowance. Execute your $XLV ↔ $SMH rebalance before Dec 26 to harvest gains with ₩0 tax (saving ₩${L.toLocaleString()}).`:`Unrealized gain (₩${$.toLocaleString()}) exceeds the ₩2.5M tax-free cap by ₩${w.toLocaleString()}. Sell only up to ₩2,500,000 of realized profit this calendar year to lock in the maximum ₩550,000 tax savings, and use new cash inflow for the remaining rebalance.`,I=$<=_?`評価益 (₩${$.toLocaleString()}) は年間非課税枠 (₩2,500,000) 以内です。年末までにリバランスを実行することで譲渡所得税 ₩0 (節税額 ₩${L.toLocaleString()}) で利益確定と取得単価引き上げが可能です。`:`評価益 (₩${$.toLocaleString()}) が非課税枠を ₩${w.toLocaleString()} 超過しています。今年の売却益を250万ウォンまでに抑えて最大 ₩550,000 を節税し、残りは新規積立資金で比率調整するのが最適です。`,U=$<=_?`예상 실현차익(₩${$.toLocaleString()})이 연간 해외주식 양도세 기본공제 한도(250만 원) 이내입니다. 연말 전 리밸런싱 매도를 통해 양도세 0원(절세 효과 약 ₩${L.toLocaleString()})으로 취득단가를 높이세요.`:`예상 차익(₩${$.toLocaleString()})이 250만 원 비과세 한도를 ₩${w.toLocaleString()} 초과합니다. 올해는 실현차익 250만 원까지만 부분 매도하여 최대 55만 원 절세 혜택을 챙기고, 부족한 비중은 신규 적립금으로 채우세요.`;return{as_of_date:t.date||"2026-10-26",smh_close:a,xlv_close:l,total_capital_usd:g,total_capital_krw:Math.round(g*i),usdkrw:i,fg_score:o,smh_dd_pct:n,regime_code:t.regime_code||"EXTREME_FEAR",active_rule_en:h,active_rule_jp:r,active_rule_kr:v,target_smh_weight_pct:Number((s*100).toFixed(1)),target_xlv_weight_pct:Number((p*100).toFixed(1)),target_smh_usd:x,target_xlv_usd:E,target_smh_shares:k,target_xlv_shares:S,residual_cash_usd:R,delta_smh_usd:P,delta_xlv_usd:B,delta_smh_shares:V,delta_xlv_shares:G,rebalance_frequency:u,estimated_tax_drag_pct:b,expected_net_cagr_pct:y,kr_tax_deduction_limit_krw:_,kr_taxable_gain_krw:w,kr_estimated_tax_saved_krw:L,kr_tax_guidance_en:N,kr_tax_guidance_jp:I,kr_tax_guidance_kr:U}})}async function ie(e){return M("/api/semi/lump-sum",{method:"POST",headers:{"Content-Type":"application/json",Accept:"application/json"},body:JSON.stringify(e)},async()=>{const t=await ee(),o=e.override_fg_score!==void 0&&e.override_fg_score!==null?Number(e.override_fg_score):Number(t.fg_score??18),n=Math.max(100,Number(e.capital_usd||5e4)),i=Number(t.smh_close??541.62),a=Number(t.xlv_close??179.28),l=t.date||"2026-10-26";if(o<=40){const c=o<=25,f=c?.8:.7,s=c?.2:.3,p=Number((n*f).toFixed(2)),h=Number((n*s).toFixed(2));return{as_of_date:l,smh_close:i,xlv_close:a,capital_usd:n,fg_score_used:o,case_code:"CASE_1_FEAR_100PCT",case_title_en:"Case 1 (Score 0–40 · Fear Regime): 100% Immediate Lump-Sum Entry",case_title_jp:"ケース1 (スコア 0–40 · 恐怖圏): 100% 即時一括エントリー",case_title_kr:"Case 1 (지수 0–40 · 공포 구간): 100% 즉시 일시금 진입",summary_en:"Semiconductors are already discounted. Do not hold excess cash—deploy 100% today and rebalance back to 70:30 when $SMH recovers within -10% of its 52-week high.",summary_jp:"半導体セクターは既に割安圏にあります。現金を遊ばせず本日100%投入し、$SMHが高値比-10%以内へ回復した時点で70:30へ戻します。",summary_kr:"반도체 섹터가 이미 할인된 공포 구간입니다. 현금을 놀리지 말고 당일 100% 거치식으로 진입한 뒤, $SMH가 고점 대비 -10% 이내로 회복되면 70:30으로 복귀하세요.",immediate_deploy_pct:100,parked_cash_rp_pct:0,tranches:[{step:1,title_en:"Tranche 1 (Day 1 Immediate 100% Deployment)",title_jp:"第1トランシェ (初日 100% 一括エントリー)",title_kr:"1차 집행 (당일 100% 즉시 거치식 진입)",timing_en:"Execute Today (Market Open / Close)",timing_jp:"本日即時執行 (Fear ≤ 40 割安圏)",timing_kr:"오늘 즉시 집행 (공포 지수 40 이하 저평가 구간)",allocation_pct:100,amount_usd:n,smh_usd:p,xlv_usd:h,cash_rp_usd:0,smh_shares:Math.floor(p/i),xlv_shares:Math.floor(h/a),note_en:`Deploy 100% immediately at ${Math.round(f*100)}:${Math.round(s*100)} ($SMH:$XLV). Historical 1-year forward win rate when entering below score 25 exceeds 91%.`,note_jp:`${Math.round(f*100)}:${Math.round(s*100)} ($SMH:$XLV) 比率で100%即時エントリー。スコア25以下でのエントリーは過去1年後の勝率が91%超。`,note_kr:`${Math.round(f*100)}:${Math.round(s*100)} ($SMH:$XLV) 비중으로 100% 즉시 진입합니다. 공포 지수 25 이하 진입 시 1년 후 플러스 수익 확률은 91% 이상입니다.`}]}}else if(o<=68){const c=Number((n*.35).toFixed(2)),f=Number((n*.3).toFixed(2)),s=Number((c+f).toFixed(2)),p=Number((n*.35).toFixed(2));return{as_of_date:l,smh_close:i,xlv_close:a,capital_usd:n,fg_score_used:o,case_code:"CASE_2_NEUTRAL_65_35",case_title_en:"Case 2 (Score 40–68 · Neutral Regime): 65% Immediate + 35% Pullback Reserve",case_title_jp:"ケース2 (スコア 40–68 · 中立圏): 65% 初日投入 + 35% 押し目待機",case_title_kr:"Case 2 (지수 40–68 · 중립 구간): 65% 선진입 + 35% 달러 RP 파킹 후 분할",summary_en:"Balanced deployment: lock in your 30% $XLV anchor and half of $SMH today, while keeping 35% dry powder for volatility.",summary_jp:"バランス型エントリー：$XLV 30%と$SMH半分を初日に確保し、35%の余力で押し目に備えます。",summary_kr:"중립장 표준 공식: 1일차에 $XLV 30% 전량과 $SMH 절반(35%)을 먼저 채우고, 나머지 35%는 조정 시 추매 실탄으로 활용합니다.",immediate_deploy_pct:65,parked_cash_rp_pct:35,tranches:[{step:1,title_en:"Tranche 1 (Day 1 Core 65% Deployment)",title_jp:"第1トランシェ (初日 65% コア投入)",title_kr:"1차 집행 (1일차 65% 코어 포지션 선진입)",timing_en:"Execute Today (30% $XLV Full + 35% $SMH Half)",timing_jp:"本日執行 ($XLV 30%全額 + $SMH 35%半分)",timing_kr:"오늘 즉시 집행 ($XLV 30% 전량 + $SMH 35% 절반)",allocation_pct:65,amount_usd:s,smh_usd:c,xlv_usd:f,cash_rp_usd:0,smh_shares:Math.floor(c/i),xlv_shares:Math.floor(f/a),note_en:"Establish 100% of your defensive $XLV position (30%) and half of your $SMH position (35%) immediately.",note_jp:"ディフェンシブ枠の$XLV (30%) 全額と、成長枠$SMHの半分 (35%) を初日に構築します。",note_kr:"방어주 $XLV(30%) 전량과 반도체 $SMH 목표치의 절반(35%)을 첫날 즉시 매수합니다."},{step:2,title_en:"Tranche 2 (Remaining 35% $SMH Reserve in USD RP)",title_jp:"第2トランシェ (残り35% $SMH待機資金・米ドルMMF)",title_kr:"2차 집행 (잔여 35% 달러 RP 파킹 후 조건부 투입)",timing_en:"Deploy when FG Score ≤ 40 OR split across D+30 / D+60 / D+90",timing_jp:"スコア40以下へ低下時、または30日・60日・90日で3分割投入",timing_kr:"공포지수 40 이하 하락 시 즉시 투입 (미도달 시 30·60·90일 3분할)",allocation_pct:35,amount_usd:p,smh_usd:p,xlv_usd:0,cash_rp_usd:p,smh_shares:Math.floor(p/i),xlv_shares:0,note_en:"Earn ~4.5% USD RP yield while waiting for a pullback below score 40, or auto-deploy over 90 days.",note_jp:"米ドルMMFで金利を受け取りながらスコア40以下への押し目を待つか、90日間で機械的に分割投入します。",note_kr:"달러 RP(연 4%대 금리)에 예치해 두었다가 지수가 40 이하로 내려오면 즉시 투입하고, 안 내려오면 3개월간 균등 분할 매수합니다."}]}}else{const c=Number((n*.3).toFixed(2)),f=Number((n*.7).toFixed(2));return{as_of_date:l,smh_close:i,xlv_close:a,capital_usd:n,fg_score_used:o,case_code:"CASE_3_GREED_DEFENSIVE_FIRST",case_title_en:"Case 3 (Score 68–100 · Greed Regime): 30% $XLV Today + 70% $SMH Parked in USD RP",case_title_jp:"ケース3 (スコア 68–100 · 強欲圏): 初日 $XLV 30%のみ + 70% 米ドルMMF待機",case_title_kr:"Case 3 (지수 68–100 · 탐욕 과열 구간): 당일 $XLV 30%만 진입 + 70% 달러 RP 대기",summary_en:"Protect principal against euphoria: buy only the 30% $XLV sleeve today and keep 70% in USD RP until Fear & Greed cools to 45 or below.",summary_jp:"高値掴み防止ルール：初日は$XLV 30%のみを購入し、70%は指数が45以下に冷めるまで米ドルMMFで待機します。",summary_kr:"고점 추격매수 방지 공식: 당일에는 방어주 $XLV 30%만 매수하고, $SMH 70% 자금은 지수가 45 이하로 내려올 때까지 달러 RP에서 이자를 받으며 대기합니다.",immediate_deploy_pct:30,parked_cash_rp_pct:70,tranches:[{step:1,title_en:"Tranche 1 (Day 1 Defensive $XLV 30% Only)",title_jp:"第1トランシェ (初日はディフェンシブ $XLV 30% のみ購入)",title_kr:"1차 집행 (1일차 방어주 $XLV 30%만 우선 진입)",timing_en:"Execute Today ($XLV Anchor Only — Zero $SMH Chasing)",timing_jp:"本日執行 ($XLV 30%のみ・過熱した$SMHの高値追い禁止)",timing_kr:"오늘 즉시 집행 (과열된 $SMH 추격매수 금지, $XLV 30%만 매수)",allocation_pct:30,amount_usd:c,smh_usd:0,xlv_usd:c,cash_rp_usd:0,smh_shares:0,xlv_shares:Math.floor(c/a),note_en:"Do not chase overheated semiconductors above score 68. Deploy only the 30% Healthcare anchor on Day 1.",note_jp:"スコア68超の過熱局面での半導体ジャンピングキャッチを回避し、ヘルスケア枠30%のみを先行構築します。",note_kr:"탐욕 지수 68 초과 과열 구간에서는 반도체 고점 물림을 피하기 위해 방어주 $XLV 30%만 우선 매수합니다."},{step:2,title_en:"Tranche 2 (70% $SMH Capital Parked in Yielding USD RP)",title_jp:"第2トランシェ (70% $SMH資金は米ドルMMFで冷却待機)",title_kr:"2차 집행 (70% $SMH 몫은 달러 RP 파킹 후 지수 ≤ 45 냉각 시 투입)",timing_en:"Deploy when FG Score cools ≤ 45 (or 4 monthly tranches)",timing_jp:"スコア45以下へ冷却時、または4ヶ月分割で順次エントリー",timing_kr:"공포·탐욕 지수가 45 이하로 식을 때 투입 (또는 4개월 분할)",allocation_pct:70,amount_usd:f,smh_usd:f,xlv_usd:0,cash_rp_usd:f,smh_shares:Math.floor(f/i),xlv_shares:0,note_en:"Collect risk-free USD interest while waiting for semiconductor euphoria to mean-revert.",note_jp:"米ドル金利を確保しながら、半導体の過熱感が冷めるのを待って安全にエントリーします。",note_kr:"달러 RP 이자를 받으며 반도체 과열이 해소될 때까지 기다렸다가 안전하게 진입하여 고점 낙폭을 방어합니다."}]}}})}function be(e){const t=e.t,o=e.lang,n=e.isProUnlocked,i=e.activeView||"rightside",a=e.semiOverview,l=a&&a.fg_score!==void 0?Number(a.fg_score).toFixed(1):"18.0",c=a&&a.regime_en?String(a.regime_en).toUpperCase():"EXTREME FEAR",f=a&&a.date?a.date:"2026-10-26",s=a&&a.smh_close!==void 0?Number(a.smh_close).toFixed(2):"541.62",p=a&&a.xlv_close!==void 0?Number(a.xlv_close).toFixed(2):"179.28",h=a&&a.qqq_close!==void 0?Number(a.qqq_close).toFixed(2):"712.20",r=a&&Array.isArray(a.etfs)?a.etfs:[],v=r.find(T=>T.ticker==="QQQ"),g=r.find(T=>T.ticker==="SMH"),x=r.find(T=>T.ticker==="XLV"),E=v&&v.ret_1d_pct!==void 0?Number(v.ret_1d_pct):1.11,k=g&&g.dd_52w_pct!==void 0?Number(g.dd_52w_pct):a&&a.smh_dd_pct!==void 0?Number(a.smh_dd_pct):-19.03,S=x&&x.ret_1d_pct!==void 0?Number(x.ret_1d_pct):.84;return`
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
            <span class="${E>=0?"tape-up":"tape-down"}">${E>=0?"+":""}${E.toFixed(2)}%</span>
          </span>
          <span class="tape-item">
            <span class="tape-sym">SMH</span>
            <span>$${s}</span>
            <span class="tape-down">${k.toFixed(2)}% DD</span>
          </span>
          <span class="tape-item">
            <span class="tape-sym">XLV</span>
            <span>$${p}</span>
            <span class="${S>=0?"tape-up":"tape-down"}">${S>=0?"+":""}${S.toFixed(2)}%</span>
          </span>
          <span class="tape-item" style="cursor:pointer;" id="ribbonSwitchSemi">
            <span class="tape-sym">SEMI FEAR & GREED</span>
            <span class="tape-down" style="font-weight:700;">${l} / 100 (${c})</span>
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
            <span>${i==="semi"?"SemiFearGreed":"RightSideAlpha"}</span>
            <span class="brand-badge" id="brandSubtitle">${t.brandSubtitle}</span>
          </div>

          <!-- PLATFORM SWITCHER -->
          <div class="platform-switcher" role="tablist" aria-label="Platform Switcher">
            <button
              class="platform-tab ${i==="rightside"?"active-rsa":""}"
              id="navTabRightSide"
              data-view="rightside"
            >
              <span>${t.navRightSide}</span>
              <span class="platform-tab-tag">72 US</span>
            </button>
            <button
              class="platform-tab ${i==="semi"?"active-semi":""}"
              id="navTabSemiFg"
              data-view="semi"
            >
              <span>${t.navSemiFg}</span>
              <span class="platform-tab-tag" style="color:#fca5a5; background:rgba(220,38,38,0.2);">${l}</span>
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
            href="${e.config.ls_site1_monthly_url}?embed=1"
          >
            <span id="btnUnlockPro">${t.btnUnlockPro}</span>
          </a>
        </div>
      </div>
    </header>
  `}function ye(e){const t=e.t,o=e.backtestKpis||{},n=Number(o.hit_rate_2x_pct??55.24).toFixed(2),i=Number(o.median_days_underwater??29).toFixed(1),a=Number(o.cagr_after_tax_pct??o.us_only_net_cagr_pct??17.81).toFixed(2),l=Number(o.severe_loss_risk_pct??.93).toFixed(2),c=e.stocks&&e.stocks.length>0&&e.stocks[0].date?e.stocks[0].date:"2026-10-13";return`
    <section class="hero">
      <div class="hero-top-row">
        <div>
          <div class="hero-tag" id="heroTag">${t.heroTag}</div>
          <h1 id="heroTitle">${t.heroTitle}</h1>
          <p id="heroDesc">${t.heroDesc}</p>
        </div>
        <div style="background:#0a0e18; border:1px solid var(--border); border-radius:4px; padding:12px 16px; min-width:250px;">
          <div style="font-size:0.68rem; color:var(--muted); font-family:var(--font-mono); text-transform:uppercase; letter-spacing:0.05em;">
            UNIVERSE SPECIFICATION · LATEST CLOSE (${c})
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
          <div class="kpi-val">${i}d</div>
          <div class="kpi-sub" id="kpi2_sub">${t.kpi2_sub}</div>
        </div>
        <div class="kpi-card kpi-emerald">
          <div class="kpi-label" id="kpi3_label">${t.kpi3_label}</div>
          <div class="kpi-val">+${a}%</div>
          <div class="kpi-sub" id="kpi3_sub">${t.kpi3_sub}</div>
        </div>
        <div class="kpi-card kpi-amber">
          <div class="kpi-label" id="kpi4_label">${t.kpi4_label}</div>
          <div class="kpi-val">${l}%</div>
          <div class="kpi-sub" id="kpi4_sub">${t.kpi4_sub}</div>
        </div>
      </div>
    </section>
  `}function _e(e){const t=e.t;return`
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
  `}function xe(e){const t=e.t,o=e.zoneFilter,n=(e.stocks||[]).filter(s=>!String(s.ticker).includes(".")),i=n.length,a=n.filter(s=>s.zone_code==="IGNITION_ZONE").length,l=n.filter(s=>s.zone_code==="WASHOUT_WATCH").length,c=n.filter(s=>s.zone_code==="LEFT_SIDE_KNIFE").length,f=n.filter(s=>s.zone_code==="VALUE_TRAP_FILTERED").length;return`
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
            <span class="tab-count">${i}</span>
          </button>
          <button class="filter-tab ${o==="IGNITION_ZONE"?"active":""}" data-zone="IGNITION_ZONE">
            <span style="width:6px; height:6px; border-radius:50%; background:var(--fin-up); display:inline-block;"></span>
            <span>${t.filterIgnition}</span>
            <span class="tab-count">${a}</span>
          </button>
          <button class="filter-tab ${o==="WASHOUT_WATCH"?"active":""}" data-zone="WASHOUT_WATCH">
            <span style="width:6px; height:6px; border-radius:50%; background:var(--fin-amber); display:inline-block;"></span>
            <span>${t.filterWatch}</span>
            <span class="tab-count">${l}</span>
          </button>
          <button class="filter-tab ${o==="LEFT_SIDE_KNIFE"?"active":""}" data-zone="LEFT_SIDE_KNIFE">
            <span style="width:6px; height:6px; border-radius:50%; background:var(--fin-down); display:inline-block;"></span>
            <span>${t.filterKnife}</span>
            <span class="tab-count">${c}</span>
          </button>
          <button class="filter-tab ${o==="VALUE_TRAP_FILTERED"?"active":""}" data-zone="VALUE_TRAP_FILTERED">
            <span>${t.filterTrap}</span>
            <span class="tab-count">${f}</span>
          </button>
        </div>
      </div>
    </div>
  `}function Se(e){const t=e.t;return`
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
          ${J(e)}
        </tbody>
      </table>
    </div>
  `}function J(e){const t=(e.filteredStocks||[]).filter(i=>!String(i.ticker).includes(".")),o=e.lang,n=e.isProUnlocked;return t.length?t.map((i,a)=>{let l="badge-watch";i.zone_code==="IGNITION_ZONE"?l="badge-ignition":i.zone_code==="LEFT_SIDE_KNIFE"?l="badge-knife":i.zone_code==="VALUE_TRAP_FILTERED"&&(l="badge-trap");const c=o==="jp"?i.zone_label_jp:o==="kr"?i.zone_label_kr:i.zone_label_en,f=String(c||i.zone_code).replace(/^[🟢🟡🔴⚠️\s]+/,""),s=o==="jp"?i.name_jp:o==="kr"?i.name_kr:i.name_en,p=i.vs_ma20_pct>=0?"var(--fin-up)":"var(--fin-down)",h=i.vs_ma60_pct>=0?"var(--fin-up)":"var(--fin-down)",r=i.vol_surge_10d>=1.35?"var(--fin-up)":"var(--text-secondary)",v=Number(i.low52||0),g=Number(i.high52||i.close*1.5),x=Number(i.close||0),E=Math.max(.01,g-v),k=Math.min(100,Math.max(2,Math.round((x-v)/E*100))),S=n||a<4||!i.is_pro_locked,T=i.ma60_price!==null&&i.ma60_price!==void 0?`$${Number(i.ma60_price).toFixed(2)}`:"LOCKED",R=i.stop_loss_price!==null&&i.stop_loss_price!==void 0?`$${Number(i.stop_loss_price).toFixed(2)}`:"LOCKED",A=i.tp1_2x_price!==null&&i.tp1_2x_price!==void 0?`$${Number(i.tp1_2x_price).toFixed(2)}`:"LOCKED",O=S?`<div class="mono" style="font-size:0.75rem; line-height:1.45;">
             <div><span style="color:var(--muted);">TRG</span> <span style="color:#60a5fa; font-weight:700;">${T}</span></div>
             <div><span style="color:var(--muted);">STP</span> <span style="color:var(--fin-down); font-weight:600;">${R}</span> · <span style="color:var(--fin-up);">TP ${A}</span></div>
           </div>`:`<span class="pro-lock-cell btn-unlock-row" title="Click to enter Pro license key">
             <svg width="11" height="11" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2">
               <rect x="3" y="11" width="18" height="11" rx="2" ry="2"></rect>
               <path d="M7 11V7a5 5 0 0 1 10 0v4"></path>
             </svg>
             <span>PRO TARGETS</span>
           </span>`,H=`/api/referral/redirect/tradingview?ticker=${encodeURIComponent(i.ticker)}`,P=`/api/referral/redirect/seekingalpha?ticker=${encodeURIComponent(i.ticker)}`;return`
      <tr data-ticker="${i.ticker}">
        <td>
          <div style="display:flex; align-items:center; gap:7px;">
            <span class="mono" style="font-weight:800; font-size:0.9rem; color:#ffffff;">${i.ticker}</span>
            <span style="font-size:0.62rem; font-family:var(--font-mono); padding:1px 4px; background:#141d2f; border:1px solid #24324d; color:#93c5fd; border-radius:2px;">US</span>
          </div>
          <div style="font-size:0.73rem; font-family:var(--font-sans); color:var(--muted); margin-top:2px;">
            ${s} · <span style="color:var(--text-secondary);">${i.sector}</span>
          </div>
        </td>
        <td>
          <span class="badge ${l}">${f}</span>
          <div class="cond-strip">
            <span class="cond-chip ${i.c1_deep_dd?"pass":""}" title="52W High Drawdown <= -20%">DD</span>
            <span class="cond-chip ${i.c2_off_low??i.c2_sweet_spot?"pass":""}" title="52W Low Proximity 10-45%">LOW</span>
            <span class="cond-chip ${i.c3_above_mas??i.c3_ma_reclaim?"pass":""}" title="Reclaimed MA20/MA60">MA</span>
            <span class="cond-chip ${i.c4_vol_or_mom??i.c4_vol_washout?"pass":""}" title="10D Volume Washout >= 1.3x">VOL</span>
          </div>
        </td>
        <td>
          <div style="display:flex; align-items:center;">
            <span class="mono" style="font-weight:800; font-size:0.9rem; width:26px;">${Number(i.score??0)}</span>
            <div class="score-bar">
              <div class="score-fill" style="width:${Number(i.score??0)}%; background:${i.score>=80?"var(--fin-up)":i.score>=55?"var(--fin-amber)":"var(--fin-down)"};"></div>
            </div>
          </div>
        </td>
        <td>
          <div class="mono" style="font-weight:700; color:#ffffff;" title="Latest Close Date: ${i.date||"2026-10-13"}">$${x.toFixed(2)}</div>
          <div class="range-52w-wrap" title="52W Range: $${v.toFixed(2)} – $${g.toFixed(2)}">
            <div class="range-52w-track">
              <div class="range-52w-fill" style="width:${k}%;"></div>
            </div>
            <div class="range-52w-labels">
              <span>L:$${v.toFixed(0)}</span>
              <span>H:$${g.toFixed(0)}</span>
            </div>
          </div>
        </td>
        <td class="mono" style="color:${i.prox_low52_pct<=40&&i.prox_low52_pct>=10?"var(--fin-up)":"var(--text-secondary)"}; font-weight:600;">
          +${Number(i.prox_low52_pct??0).toFixed(1)}%
        </td>
        <td class="mono" style="color:var(--fin-down); font-weight:600;">
          ${Number(i.dd_high52_pct??0).toFixed(1)}%
        </td>
        <td class="mono">
          <span style="color:${p}; font-weight:600;">${Number(i.vs_ma20_pct??0)>=0?"+":""}${Number(i.vs_ma20_pct??0).toFixed(1)}%</span>
          <span style="color:var(--muted);"> / </span>
          <span style="color:${h}; font-weight:600;">${Number(i.vs_ma60_pct??0)>=0?"+":""}${Number(i.vs_ma60_pct??0).toFixed(1)}%</span>
        </td>
        <td class="mono" style="color:${r}; font-weight:700;">
          ${Number(i.vol_surge_10d??1).toFixed(2)}x
        </td>
        <td class="mono" style="font-weight:700; color:${i.hist_2x_rate>=40?"var(--fin-up)":"var(--text-secondary)"};">
          ${Number(i.hist_2x_rate??0).toFixed(1)}%
        </td>
        <td>${O}</td>
        <td>
          <div style="display:flex; gap:5px;">
            <button class="btn btn-sm btn-share-card" data-ticker="${i.ticker}" title="Export Institutional Tear Sheet PNG">
              PNG
            </button>
            <a class="btn btn-sm" href="${H}" target="_blank" rel="noopener noreferrer" title="Open TradingView Chart">
              TV ↗
            </a>
            <a class="btn btn-sm" href="${P}" target="_blank" rel="noopener noreferrer" title="Open Seeking Alpha Fundamentals">
              SA ↗
            </a>
          </div>
        </td>
      </tr>
    `}).join(""):`
      <tr>
        <td colspan="11" style="text-align:center; padding:36px; color:var(--muted); font-family:var(--font-sans);">
          No US-listed equities match the active filter criteria.
        </td>
      </tr>
    `}function $e(e){const t=e.t,o=e.stocks||[],n=o.find(c=>c.ticker==="CELH"),i=n?Number(n.close).toFixed(2):"27.93",a=n&&n.date?n.date:"2026-10-13",l=e.docLastResult?Z(e.docLastResult):`<div style="color:var(--muted);">Enter US ticker, cost basis ($), and trading days held to evaluate asymmetric exit triggers against the latest closing price ($${i}).</div>`;return`
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
            <input type="number" id="docEntry" step="0.01" value="${i}" placeholder="${i}" style="padding:7px 9px; background:#05080f; border:1px solid var(--border); color:#fff; border-radius:3px; font-family:var(--font-mono); width:100%; margin-top:3px;" />
          </div>
          <div>
            <label style="font-size:0.68rem; color:var(--muted); font-family:var(--font-mono); text-transform:uppercase;">Trading Days</label>
            <input type="number" id="docDays" value="42" placeholder="42" style="padding:7px 9px; background:#05080f; border:1px solid var(--border); color:#fff; border-radius:3px; font-family:var(--font-mono); width:100%; margin-top:3px;" />
          </div>
        </div>

        <div style="display:flex; gap:5px; flex-wrap:wrap; align-items:center; margin-bottom:12px;">
          <span style="font-size:0.68rem; color:var(--muted); font-family:var(--font-mono);">LATEST CLOSE PRESETS (${a}):</span>
          ${["CELH","MBLY","APP","UPST","NVDA","CCL"].map(c=>{const f=o.find(p=>p.ticker===c),s=f?` $${Number(f.close).toFixed(2)}`:"";return`
                <button class="btn btn-sm btn-quick-doc mono" data-ticker="${c}" style="padding:2px 6px; font-size:0.68rem;">${c}${s}</button>
              `}).join("")}
        </div>
      </div>

      <div>
        <button class="btn btn-primary" id="btnRunPositionDoctor" style="width:100%; justify-content:center; padding:9px;">
          ${t.tool1Btn}
        </button>
        <div id="docOutput" style="margin-top:12px; font-size:0.8rem; background:#05080f; padding:12px; border-radius:4px; border:1px solid var(--border); border-left:3px solid var(--fin-blue);">
          ${l}
        </div>
      </div>
    </div>
  `}function Z(e){let t="var(--fin-up)",o="var(--fin-up)";e.status_code==="CRITICAL_STOP"||e.status_code==="HARD_STOP"||e.is_critical?(t="var(--fin-down)",o="var(--fin-down)"):e.status_code==="DEAD_MONEY"||e.status_code==="TIME_STOP"?(t="var(--fin-amber)",o="var(--fin-amber)"):(e.status_code==="TP1_REACHED"||e.status_code==="TP1_HARVEST")&&(t="var(--fin-up)",o="var(--fin-up)");const n=String(e.status_label||e.status_code||"ACTIVE_HOLD").replace(/^[🟢🚨🛑⏳🎯⏰🏆\s]+/,""),i=Number(e.return_pct??0),a=`${i>=0?"+":""}${i.toFixed(2)}%`,l=e.entry_price!==void 0&&e.entry_price!==null?Number(e.entry_price):0,c=e.current_price!==void 0&&e.current_price!==null?Number(e.current_price):l,f=e.stop_price!==void 0&&e.stop_price!==null?Number(e.stop_price):l*.91,s=e.tp1_price!==void 0&&e.tp1_price!==null?Number(e.tp1_price):l*2,p=f>0?`$${f.toFixed(2)}`:"$0.00",h=s>0?`$${s.toFixed(2)}`:"$0.00",r=c>0?`$${c.toFixed(2)}`:"$0.00",v=l>0?`$${l.toFixed(2)}`:"$0.00";return`
    <div style="border-left: 3px solid ${o}; padding-left: 10px;">
      <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:6px;">
        <span class="mono" style="font-weight:800; font-size:0.84rem; color:${t};">
          ${n}
        </span>
        <span class="mono" style="font-weight:800; color:${i>=0?"var(--fin-up)":"var(--fin-down)"}; font-size:0.86rem;">
          P&L: ${a}
        </span>
      </div>
      <div class="mono" style="font-size:0.73rem; color:#93c5fd; margin-bottom:4px;">
        $${e.ticker||"CELH"} Latest Close: <b style="color:#fff;">${r}</b> · Cost Basis: <b style="color:#fff;">${v}</b>
      </div>
      <div style="font-weight:700; color:#ffffff; font-size:0.78rem; margin-bottom:4px;">
        Rule Triggered: ${e.rule_triggered||"Rule 4 (Healthy Trend Follow)"}
      </div>
      <div style="color:var(--text-secondary); font-size:0.78rem; line-height:1.45; margin-bottom:8px;">
        <b>Execution Directive:</b> ${e.action_plan||""}
      </div>
      <div class="mono" style="display:flex; gap:14px; font-size:0.72rem; color:var(--muted); border-top:1px solid var(--border); padding-top:6px;">
        <span>Hard Stop (-9%): <b style="color:var(--fin-down);">${p}</b></span>
        <span>TP1 Target (2x): <b style="color:var(--fin-up);">${h}</b></span>
      </div>
    </div>
  `}function Ee(e){const t=e.t,o=e.isProUnlocked,n=e.stocks||[],i=n.find(S=>S.ticker==="CELH"),a=n.find(S=>S.ticker==="MBLY"),l=i?Number(i.close).toFixed(2):"27.93",c=i&&i.ma20_price?Number(i.ma20_price).toFixed(2):"27.93",f=i&&i.ma60_price?Number(i.ma60_price).toFixed(2):"29.12",s=i&&i.tp1_2x_price?Number(i.tp1_2x_price).toFixed(2):(Number(l)*2).toFixed(2),p=i&&i.stop_loss_price?Number(i.stop_loss_price).toFixed(2):(Number(l)*.91).toFixed(2),h=i?Number(i.score):85,r=a?Number(a.close).toFixed(2):"7.02",v=a?Number(a.low52).toFixed(2):"6.47",g=a&&a.ma60_price?Number(a.ma60_price).toFixed(2):"8.17",x=a&&a.tp1_2x_price?Number(a.tp1_2x_price).toFixed(2):(Number(r)*2).toFixed(2),E=a?Number(a.score):62,k=e.pineCode||`//@version=5
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

      <div id="vaultContentWrap" class="${o?"":"blur-locked"}" style="display:grid; grid-template-columns:repeat(auto-fit, minmax(330px, 1fr)); gap:16px;">
        <!-- Module 01: Position Doctor -->
        ${$e(e)}

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
                  <b class="mono" style="color:#ffffff;">CELH · Celsius Holdings ($${l})</b>
                  <span class="badge badge-ignition">SCORE ${h}</span>
                </div>
                <div style="color:var(--muted); font-size:0.76rem; margin-top:4px; line-height:1.45;">
                  PepsiCo North America inventory destocking complete; 2026E operating leverage +257%. Latest Close <b class="mono" style="color:#fff;">$${l}</b> reclaiming MA20 ($${c}) toward MA60 ($${f}). Stop: $${p} · TP1 (2x): <b class="mono" style="color:var(--fin-up);">$${s}</b>.
                </div>
                <button class="btn btn-sm btn-open-research" data-ticker="CELH" style="margin-top:6px;">
                  Read $CELH SEC Research Brief ↗
                </button>
              </div>

              <div style="border-left:3px solid var(--fin-blue); padding-left:10px;">
                <div style="display:flex; justify-content:space-between; align-items:center;">
                  <b class="mono" style="color:#ffffff;">MBLY · Mobileye Global ($${r})</b>
                  <span class="badge badge-watch">SCORE ${E}</span>
                </div>
                <div style="color:var(--muted); font-size:0.76rem; margin-top:4px; line-height:1.45;">
                  Tier-1 OEM ADAS inventory digestion completed; EyeQ6 design wins drive operating income inflection (-$0.39B → +$0.45B). Latest Close <b class="mono" style="color:#fff;">$${r}</b> · 52W Low $${v} · MA60 Trigger <b class="mono" style="color:#60a5fa;">$${g}</b> · TP1: <b class="mono" style="color:var(--fin-up);">$${x}</b>.
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

            <pre id="pineCodeBox" style="background:#05080f; padding:12px; border-radius:4px; font-size:0.7rem; color:#93c5fd; overflow-x:auto; max-height:155px; font-family:var(--font-mono); border:1px solid var(--border); line-height:1.45;">${k}</pre>
          </div>

          <div style="margin-top:12px;">
            <button class="btn btn-purple" id="btnCopyPineScript" style="width:100%; justify-content:center; padding:9px;">
              ${t.tool3CopyBtn}
            </button>
          </div>
        </div>
      </div>
    </section>
  `}function we(e){const t=e.config||{},o=t.ls_site1_monthly_url||"https://rightsidealpha.lemonsqueezy.com/checkout/buy/pro-monthly",n=t.ls_site1_ltd_url||"https://rightsidealpha.lemonsqueezy.com/checkout/buy/lifetime-pass";return`
    <section class="pricing-grid" id="pricingSection">
      <!-- Tier 1: Pro Monthly -->
      <div class="price-card featured">
        <div>
          <span class="badge badge-ignition">INSTITUTIONAL PRO</span>
          <h3 style="font-size:1.12rem; font-weight:800; margin-top:10px; color:#ffffff;">
            Pro Quantitative Terminal & Daily SEC Brief
          </h3>
          <div class="price-num">$29 <span style="font-size:0.82rem; color:var(--muted); font-family:var(--font-sans); font-weight:500;">/ month</span></div>
          <ul class="price-list">
            <li><span>—</span> <span>Unmask all 72 US Equity PW-RSI Scores, MA60 Breakout Triggers & -9% Stop Levels</span></li>
            <li><span>—</span> <span>Daily 08:10 EST Primary-Filing (10-K/10-Q/8-K) Turnaround Research Digest</span></li>
            <li><span>—</span> <span>Position Risk & 55-Day Time-Stop Diagnostic Engine</span></li>
            <li><span>—</span> <span>Full TradingView Pine Script v5 Indicator Source Code + SemiFearGreed 26Y CSV</span></li>
          </ul>
        </div>
        <a class="btn btn-primary lemonsqueezy-button" id="cardMonthlyBtn" href="${o}?embed=1" style="justify-content:center; padding:10px;">
          Subscribe via Lemon Squeezy ($29/mo)
        </a>
      </div>

      <!-- Tier 2: Lifetime Pass -->
      <div class="price-card">
        <div>
          <span class="badge badge-watch">FOUNDER ALLOCATION</span>
          <h3 style="font-size:1.12rem; font-weight:800; margin-top:10px; color:#ffffff;">
            Lifetime Research & Terminal License
          </h3>
          <div class="price-num">$199 <span style="font-size:0.82rem; color:var(--muted); font-family:var(--font-sans); font-weight:500;">/ one-time</span></div>
          <ul class="price-list">
            <li><span>—</span> <span>Permanent License Key — Zero recurring monthly subscription charges</span></li>
            <li><span>—</span> <span>Complete 26.8-Year (2000–2026) US Equity & Semiconductor ETF Backtest Datasets</span></li>
            <li><span>—</span> <span>Multilingual Access (English, Japanese & Korean SEC Research Briefs)</span></li>
            <li><span>—</span> <span>Full Access to both RightSideAlpha and SemiFearGreed Pro Features</span></li>
          </ul>
        </div>
        <a class="btn btn-emerald lemonsqueezy-button" id="cardLtdBtn" href="${n}?embed=1" style="justify-content:center; padding:10px;">
          Acquire Lifetime License ($199)
        </a>
      </div>

      <!-- Tier 3: Institutional Charting & Fundamental Partners -->
      <div class="price-card">
        <div>
          <span class="badge" style="background:rgba(41,98,255,0.14); color:#93c5fd; border:1px solid rgba(41,98,255,0.3);">EXECUTION & DATA PARTNERS</span>
          <h3 style="font-size:1.12rem; font-weight:800; margin-top:10px; color:#ffffff;">
            Direct Charting & Consensus EPS Verification
          </h3>
          <p style="color:var(--muted); font-size:0.8rem; margin-top:8px; line-height:1.5;">
            Verify MA20/MA60 volume breakouts and forward EPS revisions on institutional charting and consensus platforms:
          </p>
          <ul class="price-list">
            <li><span>—</span> <span><b>TradingView Pro</b> — Multi-timeframe MA20/MA60 & Pine Script v5 execution</span></li>
            <li><span>—</span> <span><b>Seeking Alpha Premium</b> — Quant Grades & 1-2Y consensus EPS revision tracking</span></li>
            <li><span>—</span> <span><b>Interactive Brokers (IBKR)</b> — Direct NYSE/NASDAQ routing & institutional FX rates</span></li>
          </ul>
        </div>
        <div style="display:flex; flex-direction:column; gap:8px;">
          <a class="btn" id="affTvBtn" href="/api/referral/redirect/tradingview?ticker=SPY" target="_blank" rel="noopener noreferrer" style="justify-content:center;">
            Launch TradingView Terminal ↗
          </a>
          <a class="btn" id="affSaBtn" href="/api/referral/redirect/seekingalpha?ticker=SPY" target="_blank" rel="noopener noreferrer" style="justify-content:center;">
            Open Seeking Alpha EPS Consensus ↗
          </a>
        </div>
      </div>
    </section>
  `}function ke(e){const t=e.config;return`
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
        <input type="text" id="licenseInput" placeholder="PRO-DEMO-2026 or XXXX-XXXX-XXXX" autocomplete="off" />
        <div id="licenseMsg" style="font-size:0.8rem; margin-bottom:12px; min-height:1.2em;"></div>
        <div style="display:flex; gap:8px; justify-content:flex-end;">
          <button class="btn" id="btnCancelLicense">Cancel</button>
          <button class="btn btn-primary" id="btnVerifyLicense">Verify & Unlock Terminal</button>
        </div>
      </div>
    </div>

    <!-- TERMINAL & AFFILIATE CONFIG MODAL -->
    <div class="modal-backdrop" id="configModal">
      <div class="modal">
        <div style="font-size:0.68rem; font-family:var(--font-mono); color:#93c5fd; text-transform:uppercase; letter-spacing:0.05em;">
          ADMINISTRATION · MONETIZATION & PARTNER ROUTING
        </div>
        <h3 style="font-size:1.12rem; font-weight:800; margin-top:4px; color:#ffffff;">Checkout & Affiliate Parameter Configuration</h3>
        <p style="color:var(--muted); font-size:0.8rem; margin-top:4px; margin-bottom:12px;">
          Update Lemon Squeezy checkout endpoints and affiliate attribution identifiers. Changes persist to the backend and browser storage.
        </p>

        <label style="font-size:0.72rem; color:var(--muted); font-family:var(--font-mono);">PLATFORM DOMAIN (TEAR SHEET WATERMARK)</label>
        <input type="text" id="cfgSite1Url" value="${t.site1_url||"https://getbreakai.com"}" />

        <label style="font-size:0.72rem; color:var(--muted); font-family:var(--font-mono);">LEMON SQUEEZY MONTHLY CHECKOUT URL ($29/MO)</label>
        <input type="text" id="cfgLsMonthly" value="${t.ls_site1_monthly_url||"https://rightsidealpha.lemonsqueezy.com/checkout/buy/pro-monthly"}" />

        <label style="font-size:0.72rem; color:var(--muted); font-family:var(--font-mono);">LEMON SQUEEZY LIFETIME CHECKOUT URL ($199)</label>
        <input type="text" id="cfgLsLtd" value="${t.ls_site1_ltd_url||"https://rightsidealpha.lemonsqueezy.com/checkout/buy/lifetime-pass"}" />

        <label style="font-size:0.72rem; color:var(--muted); font-family:var(--font-mono);">TRADINGVIEW AFFILIATE ID</label>
        <input type="text" id="cfgAffTv" value="${t.tradingview_aff_id||"rightsidealpha"}" />

        <label style="font-size:0.72rem; color:var(--muted); font-family:var(--font-mono);">SEEKING ALPHA PARTNER SOURCE TAG</label>
        <input type="text" id="cfgAffSa" value="${t.seekingalpha_source||"affiliate_rightside"}" />

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
        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:12px;">
          <h3 style="font-size:1.1rem; font-weight:800; color:#ffffff;" id="researchModalTitle">SEC Primary Filing Turnaround Brief</h3>
          <button class="btn btn-sm" id="btnCloseResearch">Close ✕</button>
        </div>
        <div id="researchModalBody" style="font-size:0.84rem; color:var(--text); line-height:1.65; max-height:62vh; overflow-y:auto; background:#05080f; padding:18px; border-radius:4px; border:1px solid var(--border);">
          Loading institutional brief...
        </div>
      </div>
    </div>

    <!-- TOAST NOTIFICATION -->
    <div class="toast" id="toastBox">Action completed</div>
  `}function D(e,t,o,n){const i=n*Math.PI/180;return{x:e+o*Math.cos(i),y:t-o*Math.sin(i)}}function Te(e,t,o,n,i){const a=D(e,t,o,n),l=D(e,t,o,i),c=Math.abs(n-i)<=180?"0":"1";return`M ${a.x.toFixed(2)} ${a.y.toFixed(2)} A ${o} ${o} 0 ${c} 1 ${l.x.toFixed(2)} ${l.y.toFixed(2)}`}function Le(e,t){const o=Math.max(0,Math.min(100,Number(e||18))),n=230,i=200,a=146,l=[{code:"EXTREME_FEAR",min:0,max:24,a1:180,a2:136.5,activeColor:"#d92d20",mutedColor:"#fecaca",label:"EXTREME FEAR",midAngle:158},{code:"FEAR",min:25,max:44,a1:134,a2:100.5,activeColor:"#f79009",mutedColor:"#fed7aa",label:"FEAR",midAngle:117},{code:"NEUTRAL",min:45,max:55,a1:98,a2:82,activeColor:"#667085",mutedColor:"#e5e7eb",label:"NEUTRAL",midAngle:90},{code:"GREED",min:56,max:74,a1:79.5,a2:46,activeColor:"#12b76a",mutedColor:"#bbf7d0",label:"GREED",midAngle:63},{code:"EXTREME_GREED",min:75,max:100,a1:43.5,a2:0,activeColor:"#027a48",mutedColor:"#a7f3d0",label:"EXTREME GREED",midAngle:22}];let c=l[0];o>=75?c=l[4]:o>=55.01?c=l[3]:o>=45?c=l[2]:o>=25&&(c=l[1]);const f=l.map(g=>{const x=g.code===c.code,E=Te(n,i,a,g.a1,g.a2),k=x?g.activeColor:g.mutedColor,S=x?40:32,T=D(n,i,a+31,g.midAngle);return`
        <path d="${E}" fill="none" stroke="${k}" stroke-width="${S}" stroke-linecap="butt" />
        <text x="${T.x.toFixed(1)}" y="${T.y.toFixed(1)}" text-anchor="middle" dominant-baseline="middle"
              fill="${x?g.activeColor:"#6b7280"}"
              font-size="${x?"9.5":"8.5"}" font-weight="${x?"800":"700"}" font-family="Inter, sans-serif">
          ${g.label}
        </text>
      `}).join(""),s=[0,25,45,55,75,100].map(g=>{const x=180-g/100*180,E=D(n,i,a-24,x),k=D(n,i,a-35,x);return`
        <circle cx="${E.x.toFixed(1)}" cy="${E.y.toFixed(1)}" r="1.8" fill="#6b7280" />
        <text x="${k.x.toFixed(1)}" y="${k.y.toFixed(1)}" text-anchor="middle" dominant-baseline="middle"
              fill="#4b5563" font-size="10" font-weight="700" font-family="JetBrains Mono, monospace">
          ${g}
        </text>
      `}).join(""),p=180-o/100*180,h=D(n,i,a-12,p),r=D(n,i,8,p+90),v=D(n,i,8,p-90);return`
    <div style="display:flex; flex-direction:column; align-items:center;">
      <svg viewBox="0 0 460 250" style="width:100%; max-width:440px; height:auto; overflow:visible;">
        ${f}
        ${s}
        <!-- Needle Polygon -->
        <polygon points="${h.x.toFixed(1)},${h.y.toFixed(1)} ${r.x.toFixed(1)},${r.y.toFixed(1)} ${v.x.toFixed(1)},${v.y.toFixed(1)}"
                 fill="#111827" />
        <circle cx="${n}" cy="${i}" r="14" fill="#111827" />
        <circle cx="${n}" cy="${i}" r="5" fill="#ffffff" />
      </svg>

      <!-- Score & Active Emotion Callout below Needle Hub -->
      <div style="text-align:center; margin-top:-18px;">
        <div style="display:inline-flex; align-items:baseline; gap:6px; background:#111827; color:#ffffff; padding:6px 20px; border-radius:30px; box-shadow:0 4px 12px rgba(0,0,0,0.12);">
          <span class="mono" style="font-size:2rem; font-weight:900; letter-spacing:-0.03em;">${Math.round(o)}</span>
          <span class="mono" style="font-size:0.9rem; color:#9ca3af; font-weight:600;">(${o.toFixed(1)} / 100)</span>
        </div>
        <div style="margin-top:8px;">
          <span style="font-size:0.78rem; color:#4b5563; font-weight:600; text-transform:uppercase; letter-spacing:0.04em;">
            Market Emotion is driving:
          </span>
          <span class="cnn-pill cnn-pill-${c.code}" style="margin-left:6px; font-size:0.85rem;">
            ${t||c.label}
          </span>
        </div>
      </div>
    </div>
  `}function Ae(e,t){const o=e&&e.series||[];if(!o.length)return'<div style="padding:40px; text-align:center; color:#6b7280;">Loading historical timeline...</div>';const n=640,i=230,a=36,l=16,c=16,f=28,s=n-a-l,p=i-c-f,h=o.map((S,T)=>{const R=a+T/Math.max(1,o.length-1)*s,A=c+(1-Math.max(0,Math.min(100,S.fg_score))/100)*p;return`${R.toFixed(1)},${A.toFixed(1)}`}),r=(c+.75*p).toFixed(1),v=(c+.5*p).toFixed(1),g=(c+.25*p).toFixed(1),x=o[0].date,E=o[Math.floor(o.length/2)].date,k=o[o.length-1].date;return`
    <div>
      <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:10px; flex-wrap:wrap; gap:8px;">
        <div style="font-size:0.8rem; font-weight:700; color:#374151;">
          Historical Semiconductor Fear & Greed Index (${x} → ${k})
        </div>
        <div style="display:flex; gap:4px;">
          ${["3M","1Y","3Y","5Y","10Y","ALL"].map(S=>`
            <button class="btn-semi-range" data-range="${S}"
                    style="padding:3px 9px; border-radius:4px; font-size:0.72rem; font-weight:700; cursor:pointer; border:1px solid ${t===S?"#111827":"#d1d5db"}; background:${t===S?"#111827":"#ffffff"}; color:${t===S?"#ffffff":"#374151"};">
              ${S}
            </button>
          `).join("")}
        </div>
      </div>

      <svg viewBox="0 0 ${n} ${i}" style="width:100%; height:auto; background:#f9fafb; border:1px solid #e5e7eb; border-radius:4px;">
        <!-- Extreme Greed Band (>75) -->
        <rect x="${a}" y="${c}" width="${s}" height="${.25*p}" fill="rgba(16,185,129,0.08)" />
        <!-- Extreme Fear Band (<25) -->
        <rect x="${a}" y="${r}" width="${s}" height="${.25*p}" fill="rgba(239,68,68,0.09)" />

        <!-- Reference Lines -->
        <line x1="${a}" y1="${g}" x2="${n-l}" y2="${g}" stroke="#10b981" stroke-dasharray="3,3" stroke-width="1" />
        <line x1="${a}" y1="${v}" x2="${n-l}" y2="${v}" stroke="#9ca3af" stroke-dasharray="3,3" stroke-width="1" />
        <line x1="${a}" y1="${r}" x2="${n-l}" y2="${r}" stroke="#ef4444" stroke-dasharray="3,3" stroke-width="1" />

        <text x="6" y="${g}" fill="#047857" font-size="9.5" font-weight="700" dominant-baseline="middle">75</text>
        <text x="6" y="${v}" fill="#6b7280" font-size="9.5" font-weight="700" dominant-baseline="middle">50</text>
        <text x="6" y="${r}" fill="#b91c1c" font-size="9.5" font-weight="700" dominant-baseline="middle">25</text>

        <!-- FG Line -->
        <polyline fill="none" stroke="#111827" stroke-width="1.8" points="${h.join(" ")}" />

        <!-- X-Axis Dates -->
        <text x="${a}" y="${i-8}" fill="#6b7280" font-size="9.5" font-family="JetBrains Mono, monospace">${x}</text>
        <text x="${a+s/2}" y="${i-8}" fill="#6b7280" font-size="9.5" text-anchor="middle" font-family="JetBrains Mono, monospace">${E}</text>
        <text x="${n-l}" y="${i-8}" fill="#6b7280" font-size="9.5" text-anchor="end" font-family="JetBrains Mono, monospace">${k}</text>
      </svg>
    </div>
  `}function Re(e,t){if(!e||!e.length)return"";const o=180,n=44,i=e.map((c,f)=>{const s=4+f/Math.max(1,e.length-1)*(o-8),p=4+(1-Math.max(0,Math.min(100,c))/100)*(n-8);return`${s.toFixed(1)},${p.toFixed(1)}`}).join(" "),l={EXTREME_FEAR:"#dc2626",FEAR:"#ea580c",NEUTRAL:"#4b5563",GREED:"#16a34a",EXTREME_GREED:"#059669"}[t]||"#111827";return`
    <svg viewBox="0 0 ${o} ${n}" style="width:160px; height:40px; background:#f8fafc; border:1px solid #e2e8f0; border-radius:4px;">
      <line x1="0" y1="${n/2}" x2="${o}" y2="${n/2}" stroke="#e2e8f0" stroke-dasharray="2,2" stroke-width="1" />
      <polyline fill="none" stroke="${l}" stroke-width="1.8" points="${i}" />
    </svg>
  `}function Ie(e){const t=e&&e.series||[];if(!t.length)return"";const o=720,n=220,i=52,a=20,l=18,c=26,f=o-i-a,s=n-l-c,p=[];t.forEach(S=>{p.push(S.port73_norm,S.qqq_norm)});const h=Math.min(...p,8e3),r=Math.max(...p,12e3),v=Math.max(1,r-h),g=t.map((S,T)=>{const R=i+T/Math.max(1,t.length-1)*f,A=l+(1-(S.port73_norm-h)/v)*s;return`${R.toFixed(1)},${A.toFixed(1)}`}).join(" "),x=t.map((S,T)=>{const R=i+T/Math.max(1,t.length-1)*f,A=l+(1-(S.qqq_norm-h)/v)*s;return`${R.toFixed(1)},${A.toFixed(1)}`}).join(" "),E=t[t.length-1].port73_norm,k=t[t.length-1].qqq_norm;return`
    <div style="margin-bottom:16px;">
      <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:8px; flex-wrap:wrap; gap:8px; font-size:0.78rem;">
        <div style="display:flex; gap:16px; align-items:center;">
          <span style="display:inline-flex; align-items:center; gap:6px; color:#34d399; font-weight:700;">
            <span style="width:12px; height:3px; background:#0ecb81; display:inline-block;"></span>
            70% $SMH : 30% $XLV Barbell ($10k → $${E.toLocaleString()})
          </span>
          <span style="display:inline-flex; align-items:center; gap:6px; color:#94a3b8; font-weight:600;">
            <span style="width:12px; height:3px; background:#64748b; display:inline-block;"></span>
            100% $QQQ Benchmark ($10k → $${k.toLocaleString()})
          </span>
        </div>
        <span class="mono" style="color:var(--muted); font-size:0.72rem;">Selected Window: ${e.range_code}</span>
      </div>
      <svg viewBox="0 0 ${o} ${n}" style="width:100%; height:auto; background:#060911; border:1px solid var(--border); border-radius:4px;">
        <polyline fill="none" stroke="#64748b" stroke-width="1.6" stroke-dasharray="3,2" points="${x}" />
        <polyline fill="none" stroke="#0ecb81" stroke-width="2.2" points="${g}" />
        <text x="6" y="${l+8}" fill="#94a3b8" font-size="9.5" font-family="JetBrains Mono, monospace">$${Math.round(r).toLocaleString()}</text>
        <text x="6" y="${n-c}" fill="#94a3b8" font-size="9.5" font-family="JetBrains Mono, monospace">$${Math.round(h).toLocaleString()}</text>
      </svg>
    </div>
  `}function Me(e){const t=e.t,o=e.lang,n=e.semiOverview;if(!n)return`
      <div class="proof-card" style="padding:40px; text-align:center;">
        Loading Semiconductor Fear & Greed Index...
      </div>
    `;const i=o==="jp"?n.regime_jp:o==="kr"?n.regime_kr:n.regime_en,a=o==="jp"?n.action_headline_jp:o==="kr"?n.action_headline_kr:n.action_headline_en,l=o==="jp"?n.action_detail_jp:o==="kr"?n.action_detail_kr:n.action_detail_en,c=e.semiGaugeTab||"overview",f=e.semiRange||"1Y",s=e.semiRebalanceResult,p=e.semiLumpSumResult,h=e.semiHistory&&e.semiHistory.era_summary||[];return`
    <!-- SECTION 1: AUTHENTIC CNN BUSINESS FEAR & GREED INDEX EDITORIAL SURFACE -->
    <section class="cnn-page-wrapper" id="semiCnnSection">
      <div class="cnn-editorial-header">
        <div>
          <div class="cnn-red-tag">${t.cnnBadge}</div>
          <h1 class="cnn-main-title">${t.cnnTitle}</h1>
          <p class="cnn-main-subtitle">${t.cnnSubtitle}</p>
        </div>
        <div style="display:flex; gap:8px; align-items:center;">
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
              <button class="cnn-view-tab ${c==="overview"?"active":""}" data-semi-tab="overview">
                ${t.cnnTabOverview}
              </button>
              <button class="cnn-view-tab ${c==="timeline"?"active":""}" data-semi-tab="timeline">
                ${t.cnnTabTimeline}
              </button>
            </div>
          </div>

          ${c==="overview"?Le(n.fg_score,i):Ae(e.semiHistory,f)}
        </div>

        <!-- RIGHT COLUMN: CNN 4-ROW HISTORICAL STACK + BARBELL SIGNAL -->
        <div class="cnn-card" style="display:flex; flex-direction:column; justify-content:space-between;">
          <div>
            <div style="font-size:0.78rem; font-weight:800; text-transform:uppercase; letter-spacing:0.05em; color:#6b7280; margin-bottom:8px;">
              ${t.cnnHistoryTitle}
            </div>
            <div class="cnn-history-list">
              ${n.comparisons.map(r=>{const v=o==="jp"?r.label_jp:o==="kr"?r.label_kr:r.label_en,g=o==="jp"?r.regime_jp:o==="kr"?r.regime_kr:r.regime_en;return`
                  <div class="cnn-history-row">
                    <div>
                      <div class="cnn-hist-label">${v} <span class="mono" style="font-size:0.72rem; color:#9ca3af;">(${r.date})</span></div>
                      <div class="cnn-hist-regime">${g}</div>
                    </div>
                    <div class="cnn-score-circle">${Math.round(r.score)}</div>
                  </div>
                `}).join("")}
            </div>
          </div>

          <!-- Active SMH:XLV Barbell Regime Box -->
          <div style="margin-top:16px; padding:14px 16px; background:#fef2f2; border:1px solid #fecaca; border-left:4px solid #dc2626; border-radius:4px;">
            <div style="font-size:0.68rem; font-weight:800; color:#991b1b; letter-spacing:0.05em; text-transform:uppercase;">
              ${t.cnnActiveRuleLabel} · TARGET ${n.recommended_smh_weight}% $SMH : ${n.recommended_xlv_weight}% $XLV
            </div>
            <div style="font-size:0.88rem; font-weight:800; color:#111827; margin-top:4px;">
              ${a}
            </div>
            <p style="font-size:0.78rem; color:#374151; margin-top:4px; line-height:1.45;">
              ${l}
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
          ${n.factors.map(r=>{const v=o==="jp"?r.title_jp:o==="kr"?r.title_kr:r.title_en,g=o==="jp"?r.subtitle_jp:o==="kr"?r.subtitle_kr:r.subtitle_en,x=o==="jp"?r.desc_jp:o==="kr"?r.desc_kr:r.desc_en,E=o==="jp"?r.regime_jp:o==="kr"?r.regime_kr:r.regime_en;return`
              <div class="cnn-indicator-item">
                <div>
                  <div style="display:flex; align-items:center; gap:8px;">
                    <span class="mono" style="font-size:0.7rem; font-weight:800; padding:2px 6px; background:#f3f4f6; border:1px solid #d1d5db; border-radius:3px; color:#374151;">
                      #${r.order} · ${r.weight_pct}% WEIGHT
                    </span>
                    <span class="cnn-ind-title">${v}</span>
                  </div>
                  <div class="cnn-ind-sub">${g}</div>
                  <p class="cnn-ind-desc">${x}</p>
                </div>

                <div style="display:flex; flex-direction:column; align-items:center; gap:6px;">
                  ${Re(r.sparkline,r.regime_code)}
                  <div class="mono" style="font-size:0.74rem; color:#374151; font-weight:700;">
                    Reading: ${r.raw_display} · Score ${r.score.toFixed(1)}/100
                  </div>
                </div>

                <div style="text-align:right;">
                  <span class="cnn-pill cnn-pill-${r.regime_code}">${E}</span>
                </div>
              </div>
            `}).join("")}
        </div>
      </div>
    </section>

    <!-- SECTION 2: CORE ETF SNAPSHOT STRIP ($SMH, $XLV, $QQQ) -->
    <section style="display:grid; grid-template-columns:repeat(auto-fit, minmax(310px, 1fr)); gap:14px; margin-bottom:22px;">
      ${n.etfs.map(r=>{const v=o==="jp"?r.name_jp:o==="kr"?r.name_kr:r.name_en,g=o==="jp"?r.role_jp:o==="kr"?r.role_kr:r.role_en,x=`/api/referral/redirect/tradingview?ticker=${encodeURIComponent(r.ticker)}`,E=`/api/referral/redirect/seekingalpha?ticker=${encodeURIComponent(r.ticker)}`;return`
          <div class="proof-card" style="margin-bottom:0; border-top:2px solid ${r.ticker==="SMH"?"var(--fin-blue)":r.ticker==="XLV"?"var(--fin-up)":"#64748b"};">
            <div style="display:flex; justify-content:space-between; align-items:flex-start;">
              <div>
                <div style="display:flex; align-items:center; gap:8px;">
                  <span class="mono" style="font-size:1.15rem; font-weight:900; color:#ffffff;">$${r.ticker}</span>
                  <span style="font-size:0.78rem; color:var(--text-secondary); font-weight:600;">${v}</span>
                </div>
                <div style="font-size:0.74rem; color:var(--muted); margin-top:3px;">${g}</div>
              </div>
              <div style="text-align:right;">
                <div class="mono" style="font-size:1.15rem; font-weight:800; color:#ffffff;">$${Number(r.close??0).toFixed(2)}</div>
                <div class="mono" style="font-size:0.74rem; color:${r.ret_1d_pct>=0?"var(--fin-up)":"var(--fin-down)"};">
                  1D: ${r.ret_1d_pct>=0?"+":""}${Number(r.ret_1d_pct??0).toFixed(2)}% · 20D: ${r.ret_20d_pct>=0?"+":""}${Number(r.ret_20d_pct??0).toFixed(2)}%
                </div>
                <div class="mono" style="font-size:0.7rem; color:var(--muted); margin-top:1px;">
                  52W DD: ${Number(r.dd_52w_pct??0).toFixed(2)}% · RSI(14): ${Number(r.rsi14??50).toFixed(1)}
                </div>
              </div>
            </div>
            <div style="display:flex; justify-content:space-between; align-items:center; margin-top:12px; padding-top:10px; border-top:1px solid var(--border-subtle); font-size:0.74rem;">
              <span class="mono" style="color:var(--muted);">
                Normal: <b style="color:#fff;">${r.target_weight_normal}%</b> → Extreme Fear: <b style="color:var(--fin-up);">${r.target_weight_fear}%</b>
              </span>
              <div style="display:flex; gap:6px;">
                <a class="btn btn-sm" href="${x}" target="_blank" rel="noopener noreferrer">TV Chart ↗</a>
                <a class="btn btn-sm" href="${E}" target="_blank" rel="noopener noreferrer">Holdings ↗</a>
              </div>
            </div>
          </div>
        `}).join("")}
    </section>

    <!-- SECTION 3: INTERACTIVE SMH + XLV REBALANCING & 2.5M KRW TAX HARVESTING ENGINE + 3-STAGE LUMP-SUM PLANNER -->
    <section style="display:grid; grid-template-columns:repeat(auto-fit, minmax(440px, 1fr)); gap:18px; margin-bottom:22px;">
      <!-- Calculator 1: SMH + XLV Rebalancing & Tax Optimizer -->
      <div class="proof-card" style="margin-bottom:0; border-top:2px solid var(--fin-up);">
        <div style="font-size:0.7rem; font-family:var(--font-mono); font-weight:700; color:var(--fin-up); letter-spacing:0.05em;">
          ${t.rebalSectionTag}
        </div>
        <h3 style="font-size:1.12rem; font-weight:800; color:#ffffff; margin:4px 0 6px;">${t.rebalSectionTitle}</h3>
        <p style="font-size:0.8rem; color:var(--muted); margin-bottom:14px;">${t.rebalSectionDesc}</p>

        <div style="display:grid; grid-template-columns:repeat(2, 1fr); gap:10px; margin-bottom:12px;">
          <div>
            <label style="font-size:0.68rem; font-family:var(--font-mono); color:var(--muted);">PORTFOLIO CAPITAL ($ USD)</label>
            <input type="number" id="semiCapInput" value="${e.semiCapUsd||1e5}" step="1000"
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
          <div>
            <label style="font-size:0.68rem; font-family:var(--font-mono); color:var(--muted);">UNREALIZED GAIN (₩ KRW · TAX HARVESTER)</label>
            <input type="number" id="semiGainKrwInput" value="${e.semiGainKrw||38e5}" step="100000"
                   style="width:100%; padding:8px 10px; background:#060911; border:1px solid var(--border); color:#fff; border-radius:4px; font-family:var(--font-mono); margin-top:3px;" />
          </div>
        </div>

        <button class="btn btn-emerald" id="btnRunSemiRebalance" style="width:100%; justify-content:center; padding:9px;">
          Calculate Exact $SMH / $XLV Rebalancing Orders
        </button>

        ${s?`
          <div id="semiRebalOutput" style="margin-top:14px; background:#060911; border:1px solid var(--border); border-left:3px solid var(--fin-up); border-radius:4px; padding:14px; font-size:0.8rem;">
            <div style="font-weight:800; color:var(--fin-up); margin-bottom:4px;">
              ${o==="jp"?s.active_rule_jp:o==="kr"?s.active_rule_kr:s.active_rule_en}
            </div>
            <div class="mono" style="font-size:0.71rem; color:#93c5fd; margin-bottom:8px;">
              Latest Close Basis (${s.as_of_date||n.date}): $SMH @ $${Number(s.smh_close??n.smh_close).toFixed(2)} · $XLV @ $${Number(s.xlv_close??n.xlv_close).toFixed(2)} · FX ₩${Number(s.usdkrw??n.usdkrw).toLocaleString()}/$ · Total ₩${Number(s.total_capital_krw??0).toLocaleString()}
            </div>
            <div style="display:grid; grid-template-columns:1fr 1fr; gap:10px; margin-bottom:10px;">
              <div style="background:#0c1220; padding:10px; border-radius:4px; border:1px solid var(--border);">
                <div style="font-size:0.7rem; color:var(--muted);">TARGET $SMH (${s.target_smh_weight_pct}%)</div>
                <div class="mono" style="font-size:1.05rem; font-weight:800; color:#fff; margin-top:2px;">
                  $${Number(s.target_smh_usd??0).toLocaleString()} (${s.target_smh_shares} sh)
                </div>
                <div class="mono" style="font-size:0.73rem; color:${s.delta_smh_usd>=0?"var(--fin-up)":"var(--fin-down)"}; margin-top:2px;">
                  Order vs Drift: ${s.delta_smh_usd>=0?"BUY +":"SELL "}$${Math.abs(Number(s.delta_smh_usd??0)).toLocaleString()} (${s.delta_smh_shares>=0?"+":""}${s.delta_smh_shares} sh)
                </div>
              </div>
              <div style="background:#0c1220; padding:10px; border-radius:4px; border:1px solid var(--border);">
                <div style="font-size:0.7rem; color:var(--muted);">TARGET $XLV (${s.target_xlv_weight_pct}%)</div>
                <div class="mono" style="font-size:1.05rem; font-weight:800; color:#fff; margin-top:2px;">
                  $${Number(s.target_xlv_usd??0).toLocaleString()} (${s.target_xlv_shares} sh)
                </div>
                <div class="mono" style="font-size:0.73rem; color:${s.delta_xlv_usd>=0?"var(--fin-up)":"var(--fin-down)"}; margin-top:2px;">
                  Order vs Drift: ${s.delta_xlv_usd>=0?"BUY +":"SELL "}$${Math.abs(Number(s.delta_xlv_usd??0)).toLocaleString()} (${s.delta_xlv_shares>=0?"+":""}${s.delta_xlv_shares} sh)
                </div>
              </div>
            </div>
            <div style="font-size:0.75rem; color:var(--text-secondary); line-height:1.45; border-top:1px solid var(--border); padding-top:8px;">
              <div><b>KRW 2.5M Tax-Free Harvester:</b> ${o==="jp"?s.kr_tax_guidance_jp:o==="kr"?s.kr_tax_guidance_kr:s.kr_tax_guidance_en}</div>
              <div class="mono" style="color:var(--muted); margin-top:4px;">
                Residual Cash: $${Number(s.residual_cash_usd??0).toFixed(2)} · Est. Annual Tax & Turnover Drag (${s.rebalance_frequency}): -${s.estimated_tax_drag_pct}%/yr · Expected Net 15Y Rate: +${s.expected_net_cagr_pct}%/yr
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

        <div style="display:grid; grid-template-columns:1fr 1fr; gap:10px; margin-bottom:12px;">
          <div>
            <label style="font-size:0.68rem; font-family:var(--font-mono); color:var(--muted);">NEW LUMP-SUM CASH ($ USD)</label>
            <input type="number" id="semiLumpCapInput" value="${e.semiLumpCapUsd||5e4}" step="1000"
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

        ${p?`
          <div id="semiLumpOutput" style="margin-top:14px; background:#060911; border:1px solid var(--border); border-left:3px solid var(--fin-blue); border-radius:4px; padding:14px; font-size:0.8rem;">
            <div style="font-weight:800; color:#93c5fd; margin-bottom:3px;">
              ${o==="jp"?p.case_title_jp:o==="kr"?p.case_title_kr:p.case_title_en}
            </div>
            <div class="mono" style="font-size:0.71rem; color:var(--muted); margin-bottom:6px;">
              Latest Close Basis (${p.as_of_date||n.date}): $SMH @ $${Number(p.smh_close??n.smh_close).toFixed(2)} · $XLV @ $${Number(p.xlv_close??n.xlv_close).toFixed(2)}
            </div>
            <p style="font-size:0.76rem; color:var(--text-secondary); margin-bottom:10px;">
              ${o==="jp"?p.summary_jp:o==="kr"?p.summary_kr:p.summary_en}
            </p>
            <div style="display:flex; flex-direction:column; gap:8px;">
              ${p.tranches.map(r=>{const v=o==="jp"?r.title_jp:o==="kr"?r.title_kr:r.title_en,g=o==="jp"?r.timing_jp:o==="kr"?r.timing_kr:r.timing_en,x=o==="jp"?r.note_jp:o==="kr"?r.note_kr:r.note_en;return`
                  <div style="background:#0c1220; padding:10px; border-radius:4px; border:1px solid var(--border);">
                    <div style="display:flex; justify-content:space-between; align-items:center;">
                      <b style="color:#ffffff;">${v}</b>
                      <span class="mono" style="color:var(--fin-up); font-weight:700;">$${r.amount_usd.toLocaleString()} (${r.allocation_pct}%)</span>
                    </div>
                    <div class="mono" style="font-size:0.72rem; color:#93c5fd; margin-top:2px;">
                      ${g} · $SMH: $${r.smh_usd.toLocaleString()} (${r.smh_shares} sh) | $XLV: $${r.xlv_usd.toLocaleString()} (${r.xlv_shares} sh)
                    </div>
                    <div style="font-size:0.74rem; color:var(--muted); margin-top:4px;">${x}</div>
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

      ${Ie(e.semiHistory)}

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
            ${h.map(r=>`
                <tr class="proof-highlight">
                  <td style="font-family:var(--font-sans);">${o==="jp"?r.horizon_jp:o==="kr"?r.horizon_kr:r.horizon_en}</td>
                  <td>${r.period}</td>
                  <td style="color:var(--text-secondary);">+${r.qqq_cagr_pct.toFixed(2)}%</td>
                  <td style="color:var(--text-secondary);">${r.qqq_multiple.toFixed(2)}x</td>
                  <td>+${r.port_70_30_cagr_pct.toFixed(2)}%</td>
                  <td style="color:var(--fin-up); font-weight:800;">+${r.port_80_20_cagr_pct.toFixed(2)}%</td>
                  <td style="color:var(--fin-up); font-weight:800;">${r.port_80_20_multiple.toFixed(2)}x</td>
                  <td><span style="color:var(--fin-up);">${r.port_80_20_mdd_pct.toFixed(1)}%</span> <span style="color:var(--muted); font-size:0.72rem;">(QQQ ${r.qqq_mdd_pct.toFixed(1)}%)</span></td>
                </tr>
              `).join("")}
          </tbody>
        </table>
      </div>
    </section>

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
  `}const Ce=window.location.pathname.toLowerCase(),Ne=window.location.hash.toLowerCase(),Fe=window.location.hostname.toLowerCase(),De=window.__DEFAULT_VIEW__==="semi"||Fe.includes("truthofmarket")||Ce.includes("/semi")||Ne.includes("semi")?"semi":"rightside",d={lang:localStorage.getItem("rsa_lang")||"en",activeView:De,isProUnlocked:localStorage.getItem("rsa_pro_unlocked")==="true",licenseKey:localStorage.getItem("rsa_token")||"",stocks:[],filteredStocks:[],backtestKpis:null,pineCode:null,searchQuery:"",zoneFilter:"ALL",sortCol:"score",sortAsc:!1,semiOverview:null,semiHistory:null,semiGaugeTab:"overview",semiRange:"1Y",semiCapUsd:1e5,semiMode:"AUTO_REGIME",semiFreq:"ANNUAL",semiGainKrw:38e5,semiRebalanceResult:null,semiLumpCapUsd:5e4,semiLumpScore:null,semiLumpSumResult:null,config:{site1_name:"RightSideAlpha",site1_url:localStorage.getItem("rsa_cfg_site1_url")||"https://getbreakai.com",site2_url:"https://truthofmarket.com",ls_site1_monthly_url:localStorage.getItem("rsa_cfg_ls_monthly")||"https://rightsidealpha.lemonsqueezy.com/checkout/buy/pro-monthly",ls_site1_ltd_url:localStorage.getItem("rsa_cfg_ls_ltd")||"https://rightsidealpha.lemonsqueezy.com/checkout/buy/lifetime-pass",tradingview_aff_id:localStorage.getItem("rsa_cfg_aff_tv")||"rightsidealpha",seekingalpha_source:localStorage.getItem("rsa_cfg_aff_sa")||"affiliate_rightside"},get t(){return W[this.lang]||W.en}};function C(e){const t=document.getElementById("toastBox");t&&(t.textContent=e,t.style.display="block",clearTimeout(window.__toastTimer),window.__toastTimer=setTimeout(()=>{t.style.display="none"},3200))}function j(){const e=(d.searchQuery||"").trim().toLowerCase(),t=d.zoneFilter;let o=d.stocks.filter(a=>!(!a.ticker||String(a.ticker).includes(".")||t!=="ALL"&&a.zone_code!==t||e&&!`${a.ticker} ${a.name_en} ${a.name_jp} ${a.name_kr} ${a.sector}`.toLowerCase().includes(e)));const n=d.sortCol,i=d.sortAsc?1:-1;o.sort((a,l)=>{const c=a[n],f=l[n];return typeof c=="string"?c.localeCompare(f)*i:((c||0)-(f||0))*i}),d.filteredStocks=o}function Pe(){const e=d.t;return`
    ${ye(d)}
    ${_e(d)}
    <section class="screener-panel">
      ${xe(d)}
      ${Se(d)}
    </section>
    ${Ee(d)}
    ${we(d)}

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
  `}function F(){const e=document.getElementById("app");if(!e)return;const t=d.t;e.innerHTML=`
    ${be(d)}
    <main class="container">
      ${d.activeView==="semi"?Me(d):Pe()}

      <footer style="border-top:1px solid var(--border); padding-top:20px; margin-top:28px; color:var(--muted); font-size:0.76rem; line-height:1.6;">
        <p id="disclaimerText">${t.disclaimer}</p>
        <p style="margin-top:8px; font-family:var(--font-mono); font-size:0.72rem;" id="copyrightText">${t.copyright}</p>
      </footer>
    </main>
    <canvas id="scoreCanvas" width="900" height="500" style="display:none;"></canvas>
    ${ke(d)}
  `,Oe()}function z(e){d.activeView=e==="semi"?"semi":"rightside",d.activeView==="semi"?window.history.replaceState(null,"","#semi"):window.history.replaceState(null,"","#rightside"),F(),window.scrollTo({top:0,behavior:"smooth"})}function Oe(){const e=document.getElementById("navTabRightSide");e&&e.addEventListener("click",()=>z("rightside"));const t=document.getElementById("navTabSemiFg");t&&t.addEventListener("click",()=>z("semi"));const o=document.getElementById("ribbonSwitchSemi");o&&o.addEventListener("click",()=>z("semi"));const n=document.getElementById("crossFunnelSwitchBtn");n&&n.addEventListener("click",()=>z("semi"));const i=document.getElementById("btnSwitchToRightSide");i&&i.addEventListener("click",()=>z("rightside")),document.querySelectorAll(".lang-btn").forEach(u=>{u.addEventListener("click",()=>{const m=u.getAttribute("data-lang");m&&W[m]&&(d.lang=m,localStorage.setItem("rsa_lang",m),F())})});const a=document.getElementById("searchInput");a&&a.addEventListener("input",u=>{d.searchQuery=u.target.value,j();const m=document.getElementById("tableBody");m&&(m.innerHTML=J(d)),Y()}),document.querySelectorAll(".filter-tab").forEach(u=>{u.addEventListener("click",()=>{d.zoneFilter=u.getAttribute("data-zone")||"ALL",j(),F()})}),document.querySelectorAll(".sort-header").forEach(u=>{u.addEventListener("click",()=>{const m=u.getAttribute("data-sort");if(!m)return;d.sortCol===m?d.sortAsc=!d.sortAsc:(d.sortCol=m,d.sortAsc=m==="ticker"),j();const b=document.getElementById("tableBody");b&&(b.innerHTML=J(d)),Y()})});const l=document.getElementById("licenseModal"),c=()=>{l&&(l.style.display="flex")},f=()=>{l&&(l.style.display="none")},s=document.getElementById("btnOpenLicense");s&&s.addEventListener("click",c);const p=document.getElementById("vaultUnlockBtn");p&&p.addEventListener("click",c);const h=document.getElementById("btnCancelLicense");h&&h.addEventListener("click",f);const r=document.getElementById("btnVerifyLicense");r&&r.addEventListener("click",async()=>{const u=document.getElementById("licenseInput"),m=document.getElementById("licenseMsg"),b=(u?u.value:"").trim();if(!b){m&&(m.style.color="var(--fin-down)",m.textContent="Please enter a valid license key.");return}try{const y=await fe(b);y.valid?(d.isProUnlocked=!0,d.licenseKey=b,localStorage.setItem("rsa_pro_unlocked","true"),localStorage.setItem("rsa_token",b),m&&(m.style.color="var(--fin-up)",m.textContent=y.message||"Pro Terminal Unlocked."),await ae(),setTimeout(()=>{f(),F(),C("Pro Terminal Unlocked — All 72 US Equity Targets Active")},350)):m&&(m.style.color="var(--fin-down)",m.textContent=y.message||"Invalid key. Use PRO-DEMO-2026 for demo.")}catch{m&&(m.style.color="var(--fin-down)",m.textContent="Validation error. Try PRO-DEMO-2026.")}});const v=document.getElementById("configModal"),g=document.getElementById("btnOpenConfig"),x=document.getElementById("btnCancelConfig"),E=document.getElementById("btnSaveConfig");g&&v&&g.addEventListener("click",()=>{v.style.display="flex"}),x&&v&&x.addEventListener("click",()=>{v.style.display="none"}),E&&E.addEventListener("click",async()=>{var $,w,L,N,I;const u=(($=document.getElementById("cfgSite1Url"))==null?void 0:$.value.trim())||d.config.site1_url,m=((w=document.getElementById("cfgLsMonthly"))==null?void 0:w.value.trim())||d.config.ls_site1_monthly_url,b=((L=document.getElementById("cfgLsLtd"))==null?void 0:L.value.trim())||d.config.ls_site1_ltd_url,y=((N=document.getElementById("cfgAffTv"))==null?void 0:N.value.trim())||"rightsidealpha",_=((I=document.getElementById("cfgAffSa"))==null?void 0:I.value.trim())||"affiliate_rightside";d.config.site1_url=u,d.config.ls_site1_monthly_url=m,d.config.ls_site1_ltd_url=b,d.config.tradingview_aff_id=y,d.config.seekingalpha_source=_,localStorage.setItem("rsa_cfg_site1_url",u),localStorage.setItem("rsa_cfg_ls_monthly",m),localStorage.setItem("rsa_cfg_ls_ltd",b),localStorage.setItem("rsa_cfg_aff_tv",y),localStorage.setItem("rsa_cfg_aff_sa",_);try{await ve({tradingview_aff_id:y,seekingalpha_source:_,ls_site1_monthly_url:m,ls_site1_ltd_url:b,site1_url:u})}catch{}v&&(v.style.display="none"),F(),C("Terminal & Affiliate Configuration Saved")}),document.querySelectorAll(".btn-quick-doc").forEach(u=>{u.addEventListener("click",async()=>{const m=u.getAttribute("data-ticker"),b=d.stocks.find(I=>I.ticker===m),y=document.getElementById("docTicker"),_=document.getElementById("docEntry"),$=document.getElementById("docDays"),w=document.getElementById("docOutput");y&&m&&(y.value=m);const L=b?Number(b.close):27.93;_&&(_.value=L.toFixed(2));const N=parseInt(($==null?void 0:$.value)||"42",10);try{const I=await K({ticker:m||"CELH",entry_price:L,days_held:N});d.docLastResult=I,w&&(w.innerHTML=Z(I))}catch{}})});const k=document.getElementById("btnRunPositionDoctor");k&&k.addEventListener("click",async()=>{var _,$,w;const u=(((_=document.getElementById("docTicker"))==null?void 0:_.value)||"CELH").trim().toUpperCase(),m=parseFloat((($=document.getElementById("docEntry"))==null?void 0:$.value)||"27.93"),b=parseInt(((w=document.getElementById("docDays"))==null?void 0:w.value)||"42",10),y=document.getElementById("docOutput");try{const L=await K({ticker:u,entry_price:m,days_held:b});d.docLastResult=L,y&&(y.innerHTML=Z(L))}catch{y&&(y.innerHTML='<div style="color:var(--fin-down);">Please enter a valid positive cost basis ($) and non-negative trading days.</div>')}});const S=document.getElementById("researchModal"),T=document.getElementById("btnCloseResearch");T&&S&&T.addEventListener("click",()=>{S.style.display="none"});const R=async u=>{if(!S)return;const m=document.getElementById("researchModalTitle"),b=document.getElementById("researchModalBody");S.style.display="flex",m&&(m.textContent=`SEC Primary Filing Turnaround Brief — $${u}`),b&&(b.innerHTML="Loading primary filing brief...");try{const y=await me(u),_=d.stocks.find(U=>U.ticker===u),$=Number(y.current_price??(_==null?void 0:_.close)??27.93).toFixed(2),w=Number(y.stop_price??(_==null?void 0:_.stop_loss_price)??Number($)*.91).toFixed(2),L=Number(y.target_price??(_==null?void 0:_.tp1_2x_price)??Number($)*2).toFixed(2),N=y.as_of_date||(_==null?void 0:_.date)||y.report_date||"2026-10-13",I=y.title||`${y.company_name||u} ($${y.ticker||u}) — ${y.opinion||"STRONG_BUY"} | Latest Close $${$} (${N})`;if(m&&(m.textContent=I),b){const U=(y.content||"").replace(/&/g,"&amp;").replace(/</g,"&lt;").replace(/>/g,"&gt;").replace(/\n/g,"<br/>"),re=`
          <div style="display:flex; flex-wrap:wrap; gap:14px; background:#090d16; border:1px solid var(--border); border-left:3px solid var(--fin-up); padding:10px 14px; border-radius:4px; margin-bottom:14px; font-family:var(--font-mono); font-size:0.76rem;">
            <span>LATEST CLOSE (${N}): <b style="color:#ffffff;">$${$}</b></span>
            <span>HARD STOP (-9%): <b style="color:var(--fin-down);">$${w}</b></span>
            <span>TP1 TARGET (2x): <b style="color:var(--fin-up);">$${L}</b></span>
            <span>RRR: <b style="color:#93c5fd;">${y.rrr_ratio||"1 : 11.1"}</b></span>
          </div>
        `;b.innerHTML=`${re}<div style="font-family:var(--font-sans); line-height:1.65;">${U}</div>`}}catch{b&&(b.innerHTML="Failed to load research brief.")}};document.querySelectorAll(".btn-open-research").forEach(u=>{u.addEventListener("click",()=>{const m=u.getAttribute("data-ticker")||"CELH";R(m)})}),document.querySelectorAll(".btn-open-research-modal").forEach(u=>{u.addEventListener("click",()=>R("CELH"))});const A=document.getElementById("btnCopyPineScript");A&&A.addEventListener("click",async()=>{var m;const u=((m=document.getElementById("pineCodeBox"))==null?void 0:m.textContent)||"";try{await navigator.clipboard.writeText(u),C("TradingView Pine Script v5 Copied to Clipboard")}catch{C("Pine Script Ready to Copy")}});const O=document.getElementById("btnCopyTopProofCard");O&&O.addEventListener("click",()=>{ne(null)}),document.querySelectorAll(".cnn-view-tab").forEach(u=>{u.addEventListener("click",()=>{d.semiGaugeTab=u.getAttribute("data-semi-tab")||"overview",F()})}),document.querySelectorAll(".btn-semi-range").forEach(u=>{u.addEventListener("click",async()=>{const m=u.getAttribute("data-range")||"1Y";d.semiRange=m;try{d.semiHistory=await te(m),F()}catch{C("Failed to load selected history window")}})});const H=document.getElementById("btnRunSemiRebalance");H&&H.addEventListener("click",async()=>{var _,$,w,L;const u=parseFloat(((_=document.getElementById("semiCapInput"))==null?void 0:_.value)||"100000"),m=(($=document.getElementById("semiModeInput"))==null?void 0:$.value)||"AUTO_REGIME",b=((w=document.getElementById("semiFreqInput"))==null?void 0:w.value)||"ANNUAL",y=parseFloat(((L=document.getElementById("semiGainKrwInput"))==null?void 0:L.value)||"3800000");d.semiCapUsd=u,d.semiMode=m,d.semiFreq=b,d.semiGainKrw=y;try{d.semiRebalanceResult=await oe({total_capital_usd:u,strategy_mode:m,rebalance_frequency:b,unrealized_gain_krw:y}),F(),C("Updated $SMH / $XLV Rebalancing Orders")}catch{C("Please enter a valid positive capital amount")}});const P=async u=>{var y,_;const m=parseFloat(((y=document.getElementById("semiLumpCapInput"))==null?void 0:y.value)||"50000"),b=u!==void 0?u:parseFloat(((_=document.getElementById("semiLumpScoreInput"))==null?void 0:_.value)||"18.0");d.semiLumpCapUsd=m,d.semiLumpScore=b;try{d.semiLumpSumResult=await ie({capital_usd:m,override_fg_score:b}),F()}catch{C("Invalid lump-sum input parameters")}},B=document.getElementById("btnRunSemiLumpSum");B&&B.addEventListener("click",()=>P()),document.querySelectorAll(".btn-sim-fg").forEach(u=>{u.addEventListener("click",()=>{const m=parseFloat(u.getAttribute("data-fg")||"18.0");P(m)})});const V=document.getElementById("btnExportSemiGauge");V&&V.addEventListener("click",()=>{He()});const G=document.getElementById("btnDownloadSemiCsv");G&&G.addEventListener("click",async()=>{if(!d.isProUnlocked){c(),C("Enter PRO-DEMO-2026 to unlock the 26-Year Daily CSV Dataset");return}const u=encodeURIComponent(d.licenseKey||"PRO-DEMO-2026");try{const b=await fetch(`/api/semi/pro/csv?license_key=${u}`,{method:"HEAD"});if(b.ok&&(b.headers.get("content-type")||"").includes("csv")){window.open(`/api/semi/pro/csv?license_key=${u}`,"_blank");return}}catch{}const m=document.createElement("a");m.href="./static_api/smh_xlv_fear_greed_history.csv",m.download="SemiFearGreed_SMH_XLV_2000_2026_History.csv",m.click()}),Y(),document.querySelectorAll('a[href^="/api/referral/redirect/"]').forEach(u=>{u.addEventListener("click",m=>{const b=window.location.hostname;if(b&&b!=="localhost"&&b!=="127.0.0.1"){m.preventDefault();const y=u.getAttribute("href")||"",$=(new URL(y,window.location.origin).searchParams.get("ticker")||"SPY").toUpperCase();if(y.includes("tradingview")){const w=encodeURIComponent(d.config.tradingview_aff_id||"rightsidealpha");window.open(`https://www.tradingview.com/symbols/${$}/?aff_id=${w}`,"_blank","noopener")}else{const w=encodeURIComponent(d.config.seekingalpha_source||"affiliate_rightside");window.open(`https://seekingalpha.com/symbol/${$}/earnings?source=${w}`,"_blank","noopener")}}})})}function Y(){document.querySelectorAll(".btn-unlock-row").forEach(e=>{e.addEventListener("click",()=>{const t=document.getElementById("licenseModal");t&&(t.style.display="flex")})}),document.querySelectorAll(".btn-share-card").forEach(e=>{e.addEventListener("click",()=>{const t=e.getAttribute("data-ticker"),o=d.stocks.find(n=>n.ticker===t);ne(o)})})}function ne(e){const t=document.getElementById("scoreCanvas");if(!t)return;const o=t.getContext("2d");o.fillStyle="#090d16",o.fillRect(0,0,900,500),o.strokeStyle="#2962ff",o.lineWidth=3,o.strokeRect(16,16,868,468),o.fillStyle="#0ecb81",o.font="bold 20px Inter, sans-serif",o.fillText("RIGHTSIDEALPHA · US EQUITY TURNAROUND TERMINAL",45,62),e?(o.fillStyle="#ffffff",o.font="bold 42px JetBrains Mono, monospace",o.fillText(`$${e.ticker} (${e.name_en})`,45,125),o.fillStyle="#93c5fd",o.font="bold 24px JetBrains Mono, monospace",o.fillText(`Signal Regime: ${e.zone_label_en}  |  PW-RSI Score: ${e.score}/100`,45,175),o.fillStyle="#cbd5e1",o.font="20px JetBrains Mono, monospace",o.fillText(`Last Close: $${e.close.toFixed(2)}  |  52W High DD: ${e.dd_high52_pct}%  |  vs 52W Low: +${e.prox_low52_pct}%`,45,230),o.fillText(`vs MA20: ${e.vs_ma20_pct}%  |  vs MA60: ${e.vs_ma60_pct}%  |  10D Vol Ratio: ${e.vol_surge_10d}x`,45,270),o.fillText(`Historical 1Y 2x (+100%) Hit Rate after -40% Drawdown: ${e.hist_2x_rate}%`,45,315)):(o.fillStyle="#ffffff",o.font="bold 34px Inter, sans-serif",o.fillText("20-Year US Equity Backtest: Left-Side vs PW-RSI Right-Side",45,125),o.fillStyle="#f6465d",o.font="22px JetBrains Mono, monospace",o.fillText("Blind 52W-Low Dip Buy: 28.91% 2x Rate | -30.31% MDD | 81d Underwater",45,200),o.fillStyle="#0ecb81",o.font="bold 24px JetBrains Mono, monospace",o.fillText("PW-RSI Right-Side:     55.24% 2x Rate | -16.49% MDD | 29d Underwater",45,260)),o.fillStyle="#8492a6",o.font="bold 16px JetBrains Mono, monospace",o.fillText(`Verified Dataset (N=394,371 US Stock-Days) · ${d.config.site1_url}`,45,440),t.toBlob(n=>{if(!n)return;const i=URL.createObjectURL(n),a=document.createElement("a");a.href=i,a.download=e?`RightSideAlpha_${e.ticker}_TearSheet.png`:"RightSideAlpha_Benchmark.png",a.click(),URL.revokeObjectURL(i),C(e?`Downloaded $${e.ticker} Tear Sheet PNG`:"Downloaded Benchmark Tear Sheet PNG")})}function He(){const e=document.getElementById("scoreCanvas");if(!e||!d.semiOverview)return;const t=e.getContext("2d"),o=d.semiOverview;t.fillStyle="#ffffff",t.fillRect(0,0,900,500),t.fillStyle="#cc0000",t.fillRect(0,0,900,10),t.fillStyle="#cc0000",t.font="bold 18px Inter, sans-serif",t.fillText("MARKETS · SEMICONDUCTOR FEAR & GREED INDEX",45,55),t.fillStyle="#111827",t.font="bold 40px Inter, sans-serif",t.fillText(`Score: ${o.fg_score.toFixed(1)} / 100 — ${o.regime_en.toUpperCase()}`,45,115),t.fillStyle="#374151",t.font="22px JetBrains Mono, monospace",t.fillText(`As of ${o.date}  |  $SMH: $${o.smh_close.toFixed(2)} (${o.smh_dd_pct}% DD)  |  $XLV: $${o.xlv_close.toFixed(2)}`,45,170),t.fillStyle="#b91c1c",t.font="bold 22px Inter, sans-serif",t.fillText(`Active Signal: ${o.action_headline_en}`,45,230),t.fillStyle="#4b5563",t.font="18px JetBrains Mono, monospace",t.fillText("26-Year Barbell (2000-2026): +10.60% CAGR (14.22x) vs QQQ +8.79% (9.21x)",45,300),t.fillText("10-Year AI Era (2016-2026):  +28.63% CAGR (15.07x) vs QQQ +20.74% (7.61x)",45,338),t.fillStyle="#6b7280",t.font="bold 16px JetBrains Mono, monospace",t.fillText(`SemiFearGreed Quantitative Barbell Engine · ${d.config.site2_url}`,45,445),e.toBlob(n=>{if(!n)return;const i=URL.createObjectURL(n),a=document.createElement("a");a.href=i,a.download=`SemiFearGreed_${o.date}.png`,a.click(),URL.revokeObjectURL(i),C("Downloaded Semiconductor Fear & Greed Index PNG")})}async function ae(){try{const[e,t,o,n,i]=await Promise.all([de({limit:200}),pe().catch(()=>null),ge().catch(()=>null),he().catch(()=>null),te(d.semiRange).catch(()=>null)]);d.stocks=Array.isArray(e)?e.filter(p=>p.ticker&&!String(p.ticker).includes(".")):[],t&&t.kpis&&(d.backtestKpis=t.kpis),o&&typeof o=="object"&&Object.entries(o).forEach(([p,h])=>{h!=null&&h!==""&&(d.config[p]=h)}),n&&(d.semiOverview=n,d.semiLumpScore===null&&(d.semiLumpScore=n.fg_score)),i&&(d.semiHistory=i);const a=d.stocks.find(p=>p.ticker==="CELH"),l=a?Number(a.close):27.93,[c,f,s]=await Promise.all([oe({total_capital_usd:d.semiCapUsd,strategy_mode:d.semiMode,rebalance_frequency:d.semiFreq,unrealized_gain_krw:d.semiGainKrw}).catch(()=>null),ie({capital_usd:d.semiLumpCapUsd,override_fg_score:d.semiLumpScore}).catch(()=>null),K({ticker:"CELH",entry_price:l,days_held:42}).catch(()=>null)]);if(c&&(d.semiRebalanceResult=c),f&&(d.semiLumpSumResult=f),s&&(d.docLastResult=s),d.isProUnlocked){const p=await ue().catch(()=>null);p&&p.code&&(d.pineCode=p.code)}j()}catch(e){console.error("Failed to load initial data:",e)}}async function Ue(){await ae(),F()}Ue();
