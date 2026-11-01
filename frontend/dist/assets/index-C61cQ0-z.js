(function(){const t=document.createElement("link").relList;if(t&&t.supports&&t.supports("modulepreload"))return;for(const a of document.querySelectorAll('link[rel="modulepreload"]'))n(a);new MutationObserver(a=>{for(const i of a)if(i.type==="childList")for(const r of i.addedNodes)r.tagName==="LINK"&&r.rel==="modulepreload"&&n(r)}).observe(document,{childList:!0,subtree:!0});function o(a){const i={};return a.integrity&&(i.integrity=a.integrity),a.referrerPolicy&&(i.referrerPolicy=a.referrerPolicy),a.crossOrigin==="use-credentials"?i.credentials="include":a.crossOrigin==="anonymous"?i.credentials="omit":i.credentials="same-origin",i}function n(a){if(a.ep)return;a.ep=!0;const i=o(a);fetch(a.href,i)}})();const be={en:{brandSubtitle:"US EQUITY QUANTITATIVE TERMINAL · v2.6",navRightSide:"RightSideAlpha · US Equities",navSemiFg:"SemiFearGreed · CNN-Style Index",marketUniverseTag:"NYSE & NASDAQ · 72 US EQUITIES",statusFree:"PUBLIC ACCESS",statusPro:"PRO TERMINAL ACTIVE",btnLicense:"License Key",btnAdmin:"Terminal Config",btnUnlockPro:"Upgrade to Pro ($29/mo)",heroTag:"INSTITUTIONAL TURNAROUND RESEARCH · 394,371 US STOCK-DAYS VERIFIED (2006–2026)",heroTitle:"Systematic Right-Side Ignition for US-Listed Equities.",heroDesc:"Blindly buying 52-week lows in US growth equities traps capital for a median of 81 trading days with a -30.3% post-entry drawdown. RightSideAlpha isolates post-washout (1.40x+ volume) breakouts reclaiming the 20-day and 60-day moving averages across 72 liquid NYSE & NASDAQ equities.",kpi1_label:"PW-RSI 1Y 2x (+100%) Hit Rate",kpi1_sub:"vs 28.91% blind 52W-low dip buying",kpi2_label:"Median Days Underwater",kpi2_sub:"Reduced from 81.0 days via 55D Time-Stop",kpi3_label:"26.8-Yr US-Only Net CAGR",kpi3_sub:"80.5x net cumulative after 22% tax & slippage",kpi4_label:"Severe Drawdown (≤ -20%) Rate",kpi4_sub:"vs 24.82% without -9% hard stop & EPS filter",proofHeading:"Empirical Performance Matrix · Left-Side Dip Buying vs. PW-RSI Right-Side Ignition",proofCopyScorecardBtn:"Export Benchmark Tear Sheet (PNG)",th_arch:"Entry Methodology (US Equities, N = 394,371 Stock-Days)",th_2x:"1Y 2x (+100%) Rate",th_med:"1Y Median Return",th_mdd:"Post-Entry Median MDD",th_dead:"Days Underwater",th_trap:"1Y Tail Loss (≤ -20%)",searchPlaceholder:"Filter by US Ticker, Company, or GICS Sector (e.g. NVDA, CELH, Semiconductors)...",filterAll:"All US Equities",filterIgnition:"Right-Side Ignition",filterWatch:"Washout Base Watch",filterKnife:"Downtrend / Avoid",filterTrap:"Value Trap Excluded",colTicker:"Security / Sector",colZone:"Regime & Factor Checklist",colScore:"Quant Score",colClose:"Last Close & 52W Range",colProx:"vs 52W Low",colDD:"52W Drawdown",colMA:"vs MA20 / MA60",colVol:"10D Vol Ratio",colHist:"Hist 2x Rate",colTrigger:"Execution Levels (Trigger / Stop)",colActions:"Research & Execution",vaultBadgeLocked:"PRO ANALYTICS TERMINAL · LOCKED (ENTER LICENSE KEY)",vaultBadgeUnlocked:"PRO ANALYTICS TERMINAL · FULL INSTITUTIONAL ACCESS",vaultTitle:"Institutional Execution & Risk Management Suite",vaultUnlockBtn:"Demo Unlock (Key: PRO-DEMO-2026)",tool1Title:"MODULE 01 · POSITION RISK & 55-DAY TIME-STOP ENGINE",tool1Sub:"Asymmetric Exit & Opportunity-Cost Diagnostic",tool1Desc:"Input your US equity cost basis and holding period. Evaluates the 4 quantitative exit rules (-9% Hard Stop, 55-Day +8% Time-Stop, +100% TP1 Principal Harvest, and Active Band Hold).",tool1Btn:"Run Position Diagnostic",tool2Title:"MODULE 02 · SEC FILING TURNAROUND RESEARCH",tool2Sub:"10-K / 10-Q / 8-K Primary Source Equity Briefs",tool2Desc:"Updated at 08:10 EST from primary SEC filings and institutional consensus revisions (zero retail media noise):",tool2ViewBtn:"Open Institutional Research Archive",tool3Title:"MODULE 03 · TRADINGVIEW PINE SCRIPT v5 OVERLAY",tool3Sub:"Automated MA20/MA60 Ignition & Washout Plotter",tool3Desc:"Deploy directly into TradingView Pine Editor to plot right-side MA20/MA60 breakouts, 1.40x volume washouts, and -9% hard stop levels on any US stock:",tool3CopyBtn:"Copy Pine Script v5 Source",crossTitle:"COMPANION MARKET SENTIMENT PLATFORM · SEMIFEARGREED",crossHeading:"Allocating to Semiconductor & Healthcare ETFs ($SMH / $XLV / $SOXX)?",crossDesc:"Open our CNN-style Semiconductor 7-Factor Fear & Greed Index and 26-year $SMH 70% : $XLV 30% contrarian rebalancing terminal.",crossBtn:"Switch to SemiFearGreed Index",cnnBadge:"MARKETS · SEMICONDUCTOR & AI SENTIMENT",cnnTitle:"Semiconductor Fear & Greed Index",cnnSubtitle:"What emotion is driving the chip & AI hardware market now?",cnnTabOverview:"Overview",cnnTabTimeline:"Timeline",cnnLastUpdated:"Last updated",cnnExportGauge:"Export Index Card (PNG)",cnnHistoryTitle:"Historical Sentiment Comparison",cnnActiveRuleLabel:"ACTIVE BARBELL ALLOCATION SIGNAL",cnnIndicatorsHeading:"7 Semiconductor Fear & Greed Indicators",cnnIndicatorsSub:"How the index is calculated: Equal-transparent 7-factor rolling 3-year (756-day) percentile & z-score composite of $SMH, $XLV, and $QQQ.",rebalSectionTag:"BARBELL ASSET ALLOCATION & TAX OPTIMIZER",rebalSectionTitle:"$SMH + $XLV Contrarian Rebalancing Engine (70:30 ↔ 80:20)",rebalSectionDesc:"Combine high-beta AI semiconductor growth ($SMH 70%) with low-beta healthcare cash-flow defense ($XLV 30%). Automatically shift to 80:20 when Fear & Greed drops below 25 or $SMH falls -20% off its 52-week high.",lumpSectionTag:"CAPITAL DEPLOYMENT PROTOCOL",lumpSectionTitle:"3-Stage Lump-Sum Entry Planner",lumpSectionDesc:"Eliminate timing regret when deploying new cash. Automatically calculates Day-1 immediate entry vs. USD RP reserve tranches based on the live or simulated Fear & Greed score.",eraSectionTag:"26-YEAR EMPIRICAL VERIFICATION (2000–2026)",eraSectionTitle:"$SMH 70% : $XLV 30% (80:20 Crash Tilt) vs. 100% $QQQ Benchmark",eraSectionDesc:"Verified across 6,625 trading days including the 2000 Dot-Com Bust, 2008 GFC, 2020 Pandemic, and 2022 Rate Shock.",disclaimer:"Regulatory & Compliance Disclosure: RightSideAlpha and SemiFearGreed are quantitative financial data analytics and historical backtesting software tools. Nothing on this platform constitutes personalized investment, legal, or tax advice. All regime classifications and technical levels are mathematical outputs derived from historical price and volume series. Past performance (2000–2026) is not indicative of future results.",copyright:"© 2026 RightSideAlpha & SemiFearGreed Quantitative Analytics. Merchant of Record: Lemon Squeezy.",table:{locked:"PRO TARGETS",empty:"No US-listed equities match the active filter criteria."},doctor:{tickerLabel:"US Ticker",entryLabel:"Cost Basis ($)",daysLabel:"Trading Days",presetsLabel:"LATEST CLOSE PRESETS",emptyHint:"Enter US ticker, cost basis ($), and trading days held to evaluate asymmetric exit triggers against the latest closing price",latestClose:"Latest Close",costBasis:"Cost Basis",ruleTriggered:"Rule Triggered",directive:"Execution Directive",hardStop:"Hard Stop (-9%)",tp1Target:"TP1 Target (2x)"},pricing:{t1Badge:"INSTITUTIONAL PRO",t1Title:"Pro Quantitative Terminal & Daily SEC Brief",t1Period:"/ month",t1Feat1:"Unmask all 72 US Equity PW-RSI Scores, MA20/60 Breakout Triggers & -9% Stop Levels",t1Feat2:"Daily 08:10 EST Primary-Filing (10-K/10-Q/8-K) Turnaround Research Digest",t1Feat3:"Position Risk & 55-Day Time-Stop Diagnostic Engine",t1Feat4:"Full TradingView Pine Script v5 Indicator Source Code + SemiFearGreed 26Y CSV",t1Btn:"Subscribe via Lemon Squeezy ($29/mo)",t2Badge:"FOUNDER ALLOCATION",t2Title:"Lifetime Research & Terminal License",t2Period:"/ one-time",t2Feat1:"Permanent License Key — Zero recurring monthly subscription charges",t2Feat2:"Complete 26.8-Year (2000–2026) US Equity & Semiconductor ETF Backtest Datasets",t2Feat3:"Multilingual Access (English, Japanese & Korean SEC Research Briefs)",t2Feat4:"Full Access to both RightSideAlpha and SemiFearGreed Pro Features",t2Btn:"Acquire Lifetime License ($199)",t3Badge:"EXECUTION & DATA PARTNERS",t3Title:"Direct Charting & Consensus EPS Verification",t3Desc:"Verify MA20/MA60 volume breakouts and forward EPS revisions on institutional charting and consensus platforms:",t3TvBtn:"Launch TradingView Terminal ↗",t3SaBtn:"Open Seeking Alpha EPS Consensus ↗"},modal:{licenseTag:"AUTHENTICATION · LEMON SQUEEZY MERCHANT OF RECORD",licenseTitle:"Activate Pro Terminal License",licenseDesc:"Enter the license key issued upon Lemon Squeezy checkout to unlock all 72 US equity target levels, Position Risk Diagnostics, and the 26-year Semiconductor CSV dataset.",evalKeyLabel:"Evaluation Key",applyDemoBtn:"Apply Evaluation Key (PRO-DEMO-2026)",deactivateBtn:"Deactivate / Lock Pro License",cancelBtn:"Cancel",verifyBtn:"Verify & Unlock Terminal",configTag:"ADMINISTRATION · MONETIZATION & PARTNER ROUTING",configTitle:"Checkout & Affiliate Parameter Configuration",configDesc:"Update Lemon Squeezy checkout endpoints and affiliate attribution identifiers. Changes persist to the backend and browser storage.",closeBtn:"Close",saveBtn:"Save Configuration",researchTitle:"SEC Primary Filing Turnaround Brief",researchLoading:"Loading institutional brief..."},telegram:{btnTelegram:"Telegram Alerts",tag:"REAL-TIME QUANT DISPATCH · TELEGRAM BOT & CHANNEL INTEGRATION",title:"Telegram Quant Signal & Morning Brief Dispatch",desc:"Receive real-time Right-Side Ignition breakouts, Position Doctor -9% / 55D stop alerts, and Semiconductor Fear & Greed 80:20 contrarian signals directly on Telegram.",statusConnected:"CONNECTED ✓",statusPreview:"PREVIEW / SETUP MODE",openChannelBtn:"Open Telegram Bot / Channel ↗",step1:"1. Create bot via @BotFather -> Paste Token",step2:"2. Send /start to your bot -> Click 'Auto-Detect Chat ID'",step3:"3. Click 'Save & Send Test Ping'",botTokenLabel:"TELEGRAM BOT TOKEN (@BotFather)",chatIdLabel:"TELEGRAM CHAT ID OR @CHANNEL",detectChatIdBtn:"🔍 Auto-Detect Chat ID",channelUrlLabel:"TELEGRAM CHANNEL / BOT LINK URL",autoAlertsLabel:"AUTOMATED SIGNAL SUBSCRIPTIONS",chkIgnition:"Right-Side 4-Factor Ignition Breakout Alerts",chkStop:"Position Doctor -9% Hard Stop & 55D Time-Stop Alerts",chkSemi:"Semiconductor Fear & Greed Extreme Regime (<25 / >75) Alerts",dispatchBarLabel:"INSTANT 1-CLICK SIGNAL DISPATCH & PREVIEW",btnSendTest:"🚀 Send Test Ping",btnSendIgnition:"📊 Send Ignition Top-Picks",btnSendSemi:"🧭 Send Semi 80:20 Signal",btnSendFull:"📑 Send Full Morning Brief",previewLabel:"LIVE TELEGRAM MESSAGE PREVIEW",closeBtn:"Close",saveBtn:"Save Telegram Settings",btnSendDoctor:"📲 Send Diagnosis to Telegram",btnSendSemiView:"📲 Send 80:20 Signal to Telegram"}},jp:{brandSubtitle:"米国株クオンツ分析ターミナル · v2.6",navRightSide:"RightSideAlpha · 米国株スクリーナー",navSemiFg:"SemiFearGreed · 半導体恐怖＆強欲指数",marketUniverseTag:"NYSE & NASDAQ · 米国上場 72銘柄限定",statusFree:"パブリックティア",statusPro:"PRO ターミナル有効",btnLicense:"ライセンス認証",btnAdmin:"ターミナル設定",btnUnlockPro:"Proへアップグレード ($29/月)",heroTag:"機関投資家向けターンアラウンド分析 · 米国株 394,371営業日検証済 (2006–2026)",heroTitle:"米国上場株に特化した「右側イグニッション」定量スクリーナー",heroDesc:"米国グロース株の単純な52週安値買い（左側逆張り）は、中央値81営業日の資金拘束と平均-30.3%の追加下落を招きます。RightSideAlphaはNYSE・NASDAQ上場72銘柄を対象に、出来高1.4倍以上のセリングクライマックス後に20日・60日移動平均線を同時突破する初動銘柄のみを抽出します。",kpi1_label:"PW-RSI 1年 2倍 (+100%) 到達率",kpi1_sub:"単純な52週安値買い (28.91%) との比較",kpi2_label:"含み損拘束期間（中央値）",kpi2_sub:"55日タイムストップにより81.0日から短縮",kpi3_label:"26.8年間 米国株純CAGR",kpi3_sub:"税金22%・スリッページ控除後 累計80.5倍",kpi4_label:"深刻な下落 (≤ -20%) 発生率",kpi4_sub:"-9%ハード損切＆業績フィルタ適用時",proofHeading:"20年実証パフォーマンス比較 · 左側安値買い vs PW-RSI 右側イグニッション",proofCopyScorecardBtn:"検証ティアシート出力 (PNG)",th_arch:"エントリー手法 (米国株, N = 394,371営業日)",th_2x:"1年 2倍 (+100%) 確率",th_med:"1年 リターン中央値",th_mdd:"エントリー後 MDD中央値",th_dead:"含み損日数",th_trap:"1年 重大損失 (≤ -20%)",searchPlaceholder:"米国ティッカー、企業名、セクターで検索 (例: NVDA, CELH, Semiconductors)...",filterAll:"全米国株",filterIgnition:"右側イグニッション",filterWatch:"クライマックス監視",filterKnife:"下降トレンド・回避",filterTrap:"バリュートラップ除外",colTicker:"銘柄 / セクター",colZone:"レジーム＆条件判定",colScore:"クオンツスコア",colClose:"終値 ($USD) & 52週レンジ",colProx:"対52週安値",colDD:"52週高値比DD",colMA:"対MA20 / MA60",colVol:"10日出来高倍率",colHist:"過去2倍確率",colTrigger:"執行価格 (突破 / -9%損切)",colActions:"調査＆チャート",vaultBadgeLocked:"PRO アナリティクスターミナル · ロック中 (要ライセンスキー)",vaultBadgeUnlocked:"PRO アナリティクスターミナル · 全機能アンロック済",vaultTitle:"機関投資家向けエグゼキューション＆リスク管理スイート",vaultUnlockBtn:"デモ解除 (キー: PRO-DEMO-2026)",tool1Title:"MODULE 01 · ポジションリスク＆55日タイムストップ診断",tool1Sub:"非対称エグジット＆機会損失シミュレーター",tool1Desc:"米国株の取得単価と保有営業日数を入力してください。4大定量エグジット原則（-9%ハード損切、55日+8%タイムストップ、+100% TP1元本回収、アクティブバンド保有）を即時判定します。",tool1Btn:"ポジション診断を実行",tool2Title:"MODULE 02 · SEC一次開示ターンアラウンド調査レポート",tool2Sub:"10-K / 10-Q / 8-K ファンダメンタルズ分析アーカイブ",tool2Desc:"二次メディアのノイズを排除し、SEC一次開示資料とEPSコンセンサス修正から毎朝更新：",tool2ViewBtn:"機関投資家向け調査レポートを開く",tool3Title:"MODULE 03 · TRADINGVIEW PINE SCRIPT v5 インジケーター",tool3Sub:"MA20/MA60 右側突破＆出来高クライマックス自動描画",tool3Desc:"TradingViewのPineエディタに貼り付けるだけで、MA20/MA60突破シグナルと-9%ストップラインをチャート上に描画します：",tool3CopyBtn:"Pine Script v5 コードをコピー",crossTitle:"姉妹センチメント分析プラットフォーム · SEMIFEARGREED",crossHeading:"半導体ETF・ヘルスケアETF ($SMH / $XLV / $SOXX) に投資していますか？",crossDesc:"CNNスタイルの半導体7ファクター恐怖＆強欲指数と、26年間検証済みの$SMH 70% : $XLV 30% 逆張りリバランス計算機へ切り替えられます。",crossBtn:"SemiFearGreed インデックスを開く",cnnBadge:"MARKETS · 半導体＆AI市場センチメント",cnnTitle:"Semiconductor Fear & Greed Index",cnnSubtitle:"いま半導体・AI市場を動かしている感情は「恐怖」か「強欲」か？",cnnTabOverview:"オーバービュー (Overview)",cnnTabTimeline:"タイムライン推移 (Timeline)",cnnLastUpdated:"最終更新",cnnExportGauge:"ゲージカード出力 (PNG)",cnnHistoryTitle:"過去センチメント比較",cnnActiveRuleLabel:"現在のバーベル配分シグナル",cnnIndicatorsHeading:"半導体 恐怖＆強欲指数を構成する7つの指標",cnnIndicatorsSub:"算出方法：$SMH・$XLV・$QQQの過去3年間（756営業日）ローリングパーセンタイルとZスコアを組み合わせた7ファクター加重平均モデル。",rebalSectionTag:"バーベル資産配分＆節税シミュレーター",rebalSectionTitle:"$SMH + $XLV 逆張りリバランス計算機 (70:30 ↔ 80:20)",rebalSectionDesc:"高成長AI半導体($SMH 70%)とディフェンシブなヘルスケア($XLV 30%)を結合。指数25以下または$SMH高値比-20%下落時に80:20へ逆張りシフトします。",lumpSectionTag:"新規資金エントリープロトコル",lumpSectionTitle:"3段階 一括資金エントリープランナー",lumpSectionDesc:"現在の恐怖＆強欲スコアに応じて、初日即時投入枠と米ドルMMF待機枠の最適比率を算出します。",eraSectionTag:"26年間（2000–2026）実証バックテスト",eraSectionTitle:"$SMH 70% : $XLV 30% (暴落時80:20) vs 100% $QQQ ベンチマーク比較",eraSectionDesc:"ITバブル崩壊、リーマンショック、コロナ危機、2022年半導体不況を含む6,625営業日の完全検証データ。",disclaimer:"コンプライアンス免責事項：RightSideAlphaおよびSemiFearGreedは定量金融データ分析および過去バックテスト用のソフトウェアツールです。当プラットフォームのいかなる情報も個別の投資助言や税務助言を構成しません。",copyright:"© 2026 RightSideAlpha & SemiFearGreed Quantitative Analytics. Merchant of Record: Lemon Squeezy.",table:{locked:"PRO TARGETS",empty:"条件に一致する米国上場銘柄がありません。"},doctor:{tickerLabel:"米国ティッカー",entryLabel:"取得単価 ($)",daysLabel:"保有営業日数",presetsLabel:"最新終値プリセット",emptyHint:"米国ティッカー、取得単価($)、保有営業日数を入力し、最新終値に対する非対称エグジット判定を実行します",latestClose:"最新終値",costBasis:"取得単価",ruleTriggered:"発動ルール",directive:"執行ディレクティブ",hardStop:"ハード損切 (-9%)",tp1Target:"TP1 目標 (2x)"},pricing:{t1Badge:"INSTITUTIONAL PRO",t1Title:"Pro クオンツターミナル＆日次SEC調査レポート",t1Period:"/ 月",t1Feat1:"全72米国株のPW-RSIスコア・MA20/60突破トリガー・-9%損切ラインを完全公開",t1Feat2:"毎日08:10 EST更新のSEC一次開示 (10-K/10-Q/8-K) ターンアラウンド調査レポート",t1Feat3:"ポジションリスク＆55日タイムストップ診断エンジン",t1Feat4:"TradingView Pine Script v5 完全ソースコード + SemiFearGreed 26年日次CSV",t1Btn:"Lemon Squeezyで購読 ($29/月)",t2Badge:"FOUNDER ALLOCATION",t2Title:"ライフタイム（永久）ターミナルライセンス",t2Period:"/ 一括払い",t2Feat1:"永久ライセンスキー発行 — 毎月のサブスクリプション課金なし",t2Feat2:"26.8年間 (2000–2026) 米国株＆半導体ETF完全バックテストデータセット",t2Feat3:"日・英・韓 3ヶ国語対応のSEC一次開示リサーチアーカイブ",t2Feat4:"RightSideAlphaおよびSemiFearGreed両プラットフォームのPro機能を永久開放",t2Btn:"ライフタイムパスを取得 ($199)",t3Badge:"EXECUTION & DATA PARTNERS",t3Title:"機関投資家向けチャート＆EPSコンセンサス検証",t3Desc:"MA20/MA60出来高ブレイクとEPSコンセンサス修正を機関投資家向けプラットフォームで直接検証：",t3TvBtn:"TradingView チャートを起動 ↗",t3SaBtn:"Seeking Alpha EPSコンセンサスを開く ↗"},modal:{licenseTag:"AUTHENTICATION · LEMON SQUEEZY MERCHANT OF RECORD",licenseTitle:"Pro ターミナル ライセンス認証",licenseDesc:"Lemon Squeezy決済後に発行されたライセンスキーを入力すると、全72米国株の目標株価、ポジション診断、26年半導体CSVデータがアンロックされます。",evalKeyLabel:"評価用デモキー",applyDemoBtn:"デモキーを即時適用 (PRO-DEMO-2026)",deactivateBtn:"Proライセンスを解除・ロック",cancelBtn:"キャンセル",verifyBtn:"認証してアンロック",configTag:"ADMINISTRATION · MONETIZATION & PARTNER ROUTING",configTitle:"決済URL＆アフィリエイトパラメータ設定",configDesc:"Lemon Squeezy決済エンドポイントとアフィリエイトIDを更新します。変更はバックエンドとブラウザに保存されます。",closeBtn:"閉じる",saveBtn:"設定を保存",researchTitle:"SEC一次開示 ターンアラウンド調査レポート",researchLoading:"調査レポートを読み込み中..."},telegram:{btnTelegram:"Telegram通知",tag:"REAL-TIME QUANT DISPATCH · TELEGRAM BOT & CHANNEL INTEGRATION",title:"Telegram クオンツシグナル＆モーニングブリーフ配信",desc:"右側イグニッション初動ブレイク、ポジションドクターの-9%損切・55日タイムストップ警告、半導体恐怖＆強欲指数80:20逆張りシグナルをTelegramへリアルタイム配信します。",statusConnected:"CONNECTED ✓",statusPreview:"PREVIEW / SETUP MODE",openChannelBtn:"Telegram ボット / チャンネルを開く ↗",step1:"1. @BotFatherでボット作成 -> トークンを貼り付け",step2:"2. ボットへ /start を送信 -> 「チャットID自動検出」をクリック",step3:"3. 設定を保存してテストPingを送信",botTokenLabel:"TELEGRAM ボットトークン (@BotFather)",chatIdLabel:"TELEGRAM チャットID または @CHANNEL",detectChatIdBtn:"🔍 チャットID自動検出",channelUrlLabel:"TELEGRAM チャンネル / ボットURL",autoAlertsLabel:"自動アラート配信トリガー設定",chkIgnition:"右側4条件イグニッション突破シグナル通知",chkStop:"ポジション診断 -9%ハード損切＆55日タイムストップ通知",chkSemi:"半導体 恐怖＆強欲指数 極端レジーム (<25 / >75) 通知",dispatchBarLabel:"ワンクリック即時シグナル配信＆プレビュー",btnSendTest:"🚀 Send Test Ping",btnSendIgnition:"📊 Send Ignition Top-Picks",btnSendSemi:"🧭 Send Semi 80:20 Signal",btnSendFull:"📑 Send Full Morning Brief",previewLabel:"LIVE TELEGRAM MESSAGE PREVIEW",closeBtn:"閉じる",saveBtn:"Save Telegram Settings",btnSendDoctor:"📲 診断結果をTelegramへ送信",btnSendSemiView:"📲 80:20シグナルをTelegramへ送信"}},kr:{brandSubtitle:"미국 상장주식 전용 퀀트 터미널 · v2.6",navRightSide:"RightSideAlpha · 미국주식 알파 터미널",navSemiFg:"SemiFearGreed · 반도체 공포·탐욕 지수",marketUniverseTag:"NYSE & NASDAQ · 미국 상장 72개 핵심 종목 한정",statusFree:"퍼블릭 티어",statusPro:"PRO 터미널 활성화",btnLicense:"라이선스 인증",btnAdmin:"터미널 설정",btnUnlockPro:"Pro 업그레이드 ($29/월)",heroTag:"기관급 턴어라운드 리서치 · 미국 상장주식 394,371 거래일 전수 검증 (2006–2026)",heroTitle:"미국 상장주식에 최적화된 우측 변곡점(PW-RSI) 정량 분석 플랫폼",heroDesc:"미국 성장주를 단순 52주 신저가(좌측 구간)에 매수하면 중앙값 81거래일의 자금 묶임(데드머니)과 -30.3%의 추가 낙폭에 노출됩니다. RightSideAlpha는 NYSE·NASDAQ 상장 72개 핵심 종목만을 대상으로 1.4배 이상 거래량 투매(Washout) 후 20일·60일 이동평균선을 동시 탈환하는 우측 초동 시그널을 판독합니다.",kpi1_label:"PW-RSI 1년 2배 (+100%) 도달률",kpi1_sub:"단순 52주 신저가 좌측 매수(28.91%) 대비",kpi2_label:"보유 후 물림 기간 (중앙값)",kpi2_sub:"55일 시간손절 원칙으로 81.0일에서 단축",kpi3_label:"26.8개년 미국주식 순 CAGR",kpi3_sub:"양도세 22%·슬리피지 차감 후 누적 80.5배",kpi4_label:"심각한 손실 (≤ -20%) 발생 확률",kpi4_sub:"-9% 손절 및 실적 턴어라운드 필터 적용 시",proofHeading:"20년 실증 백테스트 매트릭스 · 좌측 신저가 매수 vs PW-RSI 우측 시동 모델",proofCopyScorecardBtn:"백테스트 티어시트 저장 (PNG)",th_arch:"진입 방법론 (미국 상장주, N = 394,371 거래일)",th_2x:"1년 2배 (+100%) 확률",th_med:"1년 수익률 중앙값",th_mdd:"진입 후 MDD 중앙값",th_dead:"자금 물림 기간",th_trap:"1년 치명적 손실 (≤ -20%)",searchPlaceholder:"미국 티커, 기업명, 섹터 검색 (예: NVDA, CELH, Semiconductors)...",filterAll:"미국 전체 종목",filterIgnition:"우측 돌파 시동 (Ignition)",filterWatch:"워시아웃 베이스 대기",filterKnife:"좌측 하락추세 · 주의",filterTrap:"밸류트랩 배제 종목",colTicker:"종목 / GICS 섹터",colZone:"시그널 레짐 & 4대 조건",colScore:"퀀트 스코어",colClose:"종가 ($USD) & 52주 밴드",colProx:"52주 저점 이격",colDD:"52주 고점 낙폭",colMA:"20일 / 60일선 괴리",colVol:"10일 거래량 배율",colHist:"과거 2배 확률",colTrigger:"실행 타점 (60일 돌파 / -9% 손절)",colActions:"리포트 & 차트 연동",vaultBadgeLocked:"PRO 애널리틱스 터미널 · 잠김 (라이선스 키 입력 필요)",vaultBadgeUnlocked:"PRO 애널리틱스 터미널 · 전 기능 활성화됨",vaultTitle:"기관급 포지션 리스크 관리 & SEC 1차 공시 리서치 스위트",vaultUnlockBtn:"데모 즉시 해제 (키: PRO-DEMO-2026)",tool1Title:"MODULE 01 · 보유 포지션 리스크 & 55일 시간손절 판독기",tool1Sub:"비대칭 청산 원칙 및 기회비용 정밀 진단",tool1Desc:"미국 주식 매수 단가($)와 보유 거래일수를 입력하세요. 4대 정량 청산 원칙(-9% 칼손절 방어, 55일 +8% 미만 시간손절, +100% TP1 원금 반절 회수, 정상 밴드 보유)을 즉시 산출합니다.",tool1Btn:"보유 포지션 정밀 진단 실행",tool2Title:"MODULE 02 · SEC 1차 공시 기반 턴어라운드 리서치",tool2Sub:"10-K / 10-Q / 8-K 원문 기반 기관급 종목 분석 브리프",tool2Desc:"2차 언론 노이즈를 배제하고 미국 SEC 1차 공시와 컨센서스 EPS 상향 데이터를 바탕으로 매일 08:10 업데이트됩니다:",tool2ViewBtn:"기관급 턴어라운드 리포트 열람",tool3Title:"MODULE 03 · TRADINGVIEW PINE SCRIPT v5 전용 지표",tool3Sub:"MA20/MA60 우측 돌파 및 거래량 워시아웃 자동 차트 표시",tool3Desc:"트레이딩뷰 Pine 에디터에 붙여넣어 미국 전 종목 차트에 우측 시동 타점과 -9% 손절 라인을 자동 표시합니다:",tool3CopyBtn:"Pine Script v5 소스코드 복사",crossTitle:"연계 섹터 심리 & 자산배분 플랫폼 · SEMIFEARGREED",crossHeading:"반도체 ETF와 헬스케어 ETF ($SMH / $XLV / $SOXX)로 꾸준한 복리 수익을 원하시나요?",crossDesc:"CNN Fear & Greed 스타일의 반도체 7팩터 공포·탐욕 지수와 26년 검증된 $SMH 70% : $XLV 30% (폭락장 80:20) 역발상 리밸런싱 플랫폼으로 이동하세요.",crossBtn:"SemiFearGreed 지수 플랫폼 열기",cnnBadge:"MARKETS · 반도체 & AI 섹터 투자심리 지수",cnnTitle:"Semiconductor Fear & Greed Index",cnnSubtitle:"지금 반도체와 AI 시장을 움직이는 감정은 '공포'입니까, '탐욕'입니까?",cnnTabOverview:"오버뷰 (Overview)",cnnTabTimeline:"타임라인 추이 (Timeline)",cnnLastUpdated:"최근 업데이트",cnnExportGauge:"공포·탐욕 지수 카드 저장 (PNG)",cnnHistoryTitle:"시점별 지수 히스토리 비교",cnnActiveRuleLabel:"현재 발동 중인 바벨 자산배분 시그널",cnnIndicatorsHeading:"반도체 공포·탐욕 지수를 구성하는 7대 핵심 지표",cnnIndicatorsSub:"산출 방식: $SMH, $XLV, $QQQ의 최근 3년(756거래일) 롤링 백분위와 Z-스코어를 결합한 7팩터 정량 모델입니다.",rebalSectionTag:"바벨 자산배분 & 해외주식 절세 계산기",rebalSectionTitle:"$SMH + $XLV 역발상 리밸런싱 계산기 (70:30 ↔ 80:20)",rebalSectionDesc:"고성장 AI 반도체($SMH 70%)와 방어형 헬스케어($XLV 30%)를 결합하여 매년 꾸준한 복리 수익을 추구합니다. 공포지수 25 이하 또는 $SMH 고점 대비 -20% 하락 시 80:20으로 역발상 스위칭합니다.",lumpSectionTag:"신규 거치식 자금 투입 프로토콜",lumpSectionTitle:"3단계 일시금(Lump-Sum) 진입 플래너",lumpSectionDesc:"목돈을 한 번에 넣을 때 고점 물림을 방지합니다. 현재(또는 시뮬레이션) 공포·탐욕 점수에 따라 당일 즉시 진입 물량과 달러 RP 파킹 물량을 자동 계산합니다.",eraSectionTag:"26개년(2000–2026) 실증 백테스트 검증",eraSectionTitle:"$SMH 70% : $XLV 30% (폭락장 80:20) vs 100% $QQQ 장기 성과 비교",eraSectionDesc:"2000년 닷컴버블, 2008년 금융위기, 2020년 팬데믹, 2022년 금리인상기를 모두 포함한 6,625거래일 실증 데이터입니다.",disclaimer:"법적 고지 및 면책조항: RightSideAlpha와 SemiFearGreed는 정량적 금융 데이터 분석 및 역사적 백테스트 소프트웨어 도구입니다. 본 웹사이트의 어떠한 내용도 개별 투자자를 위한 맞춤형 투자 권유나 세무 자문을 구성하지 않습니다. 과거 백테스트 성과(2000–2026)는 미래 수익을 보장하지 않습니다.",copyright:"© 2026 RightSideAlpha & SemiFearGreed Quantitative Analytics. Merchant of Record: Lemon Squeezy.",table:{locked:"PRO TARGETS",empty:"선택한 필터 조건에 부합하는 미국 상장 종목이 없습니다."},doctor:{tickerLabel:"미국 티커",entryLabel:"매수 단가 ($)",daysLabel:"보유 거래일수",presetsLabel:"최근 종가 프리셋",emptyHint:"미국 티커, 매수 단가($), 보유 거래일수를 입력하여 최근 종가 기준 비대칭 청산 시그널을 진단하세요",latestClose:"최근 종가",costBasis:"매수 단가",ruleTriggered:"발동 원칙",directive:"실행 지침",hardStop:"칼손절 라인 (-9%)",tp1Target:"TP1 목표가 (2x)"},pricing:{t1Badge:"INSTITUTIONAL PRO",t1Title:"Pro 퀀트 터미널 & 일간 SEC 1차 공시 브리프",t1Period:"/ 월",t1Feat1:"미국 72개 핵심 종목 PW-RSI 스코어, MA20/60 돌파 타점 및 -9% 손절가 전수 공개",t1Feat2:"매일 08:10 EST 미국 SEC 1차 공시(10-K/10-Q/8-K) 턴어라운드 리서치 다이제스트",t1Feat3:"보유 포지션 리스크 & 55일 시간손절 정밀 진단 엔진",t1Feat4:"TradingView Pine Script v5 전용 지표 소스코드 + SemiFearGreed 26년 일간 CSV",t1Btn:"Lemon Squeezy 정기 구독 ($29/월)",t2Badge:"FOUNDER ALLOCATION",t2Title:"평생 소장(Lifetime) 리서치 & 터미널 라이선스",t2Period:"/ 평생 1회 결제",t2Feat1:"영구 라이선스 키 발급 — 매월 반복되는 구독료 영구 면제",t2Feat2:"26.8개년(2000–2026) 미국 주식 & 반도체 ETF 백테스트 전체 데이터셋",t2Feat3:"한·미·일 3개 국어 SEC 1차 공시 리서치 브리프 무제한 열람",t2Feat4:"RightSideAlpha 및 SemiFearGreed 양대 플랫폼 Pro 기능 평생 잠금 해제",t2Btn:"평생 라이선스 구매 ($199)",t3Badge:"EXECUTION & DATA PARTNERS",t3Title:"기관급 차트 연동 & 컨센서스 EPS 교차 검증",t3Desc:"MA20/MA60 거래량 돌파와 선행 EPS 상향 추이를 글로벌 차트 및 컨센서스 플랫폼에서 직접 검증하세요:",t3TvBtn:"TradingView 차트 터미널 실행 ↗",t3SaBtn:"Seeking Alpha EPS 컨센서스 열기 ↗"},modal:{licenseTag:"AUTHENTICATION · LEMON SQUEEZY MERCHANT OF RECORD",licenseTitle:"Pro 터미널 라이선스 활성화",licenseDesc:"Lemon Squeezy 결제 후 발급된 라이선스 키를 입력하면 미국 72개 전 종목 타점, 포지션 진단기, 26년 반도체 CSV 데이터셋이 즉시 잠금 해제됩니다.",evalKeyLabel:"즉시 평가용 데모 키",applyDemoBtn:"데모 키 1초 자동 적용 (PRO-DEMO-2026)",deactivateBtn:"Pro 라이선스 비활성화 (잠금 복귀)",cancelBtn:"취소",verifyBtn:"라이선스 인증 및 잠금 해제",configTag:"ADMINISTRATION · MONETIZATION & PARTNER ROUTING",configTitle:"결제 체크아웃 & 어필리에이트 파라미터 설정",configDesc:"Lemon Squeezy 결제 링크와 파트너 어필리에이트 ID를 설정합니다. 변경사항은 서버 및 브라우저에 즉시 저장됩니다.",closeBtn:"닫기",saveBtn:"설정 저장",researchTitle:"SEC 1차 공시 기반 턴어라운드 리서치 브리프",researchLoading:"기관급 리서치 브리프를 불러오는 중..."},telegram:{btnTelegram:"텔레그램 알림",tag:"REAL-TIME QUANT DISPATCH · TELEGRAM BOT & CHANNEL INTEGRATION",title:"텔레그램 퀀트 시그널 & 모닝 브리핑 실시간 연동",desc:"우측 시동(PW-RSI) 돌파 종목, 보유 포지션 -9% 칼손절·55일 시간손절 경고, 반도체 공포·탐욕 80:20 역발상 리밸런싱 시그널을 텔레그램으로 즉시 수신하세요.",statusConnected:"CONNECTED ✓",statusPreview:"PREVIEW / SETUP MODE",openChannelBtn:"텔레그램 봇 / 채널 열기 ↗",step1:"1. @BotFather에서 봇 생성 후 Bot Token 붙여넣기",step2:"2. 생성한 봇에게 /start 메시지 전송 후 '채팅 ID 자동 찾기' 클릭",step3:"3. 설정 저장 및 테스트 핑 발송 클릭",botTokenLabel:"TELEGRAM 봇 토큰 (@BotFather)",chatIdLabel:"TELEGRAM 채팅 ID 또는 @채널명",detectChatIdBtn:"🔍 채팅 ID 자동 찾기",channelUrlLabel:"TELEGRAM 채널 / 봇 링크 URL",autoAlertsLabel:"실시간 자동 알림 수신 항목",chkIgnition:"우측 4대 조건 시동(Ignition) 돌파 알림",chkStop:"포지션 닥터 -9% 칼손절 및 55일 시간손절 경보",chkSemi:"반도체 공포·탐욕 지수 극단 구간 (<25 / >75) 알림",dispatchBarLabel:"원클릭 즉시 브리핑 발송 & 미리보기",btnSendTest:"🚀 Send Test Ping",btnSendIgnition:"📊 Send Ignition Top-Picks",btnSendSemi:"🧭 Send Semi 80:20 Signal",btnSendFull:"📑 Send Full Morning Brief",previewLabel:"LIVE TELEGRAM MESSAGE PREVIEW",closeBtn:"닫기",saveBtn:"Save Telegram Settings",btnSendDoctor:"📲 진단 결과 텔레그램 전송",btnSendSemiView:"📲 80:20 시그널 텔레그램 전송"}}};function Ue(){return typeof localStorage>"u"?!1:!!(localStorage.getItem("rsa_token")||(localStorage.getItem("rsa_pro_unlocked")==="true"?"PRO-DEMO-2026":""))&&localStorage.getItem("rsa_pro_unlocked")==="true"}function de(){return Ue()?{Authorization:`Bearer ${localStorage.getItem("rsa_token")||"PRO-DEMO-2026"}`}:{}}function ye(){return typeof window>"u"?!1:window.__STATIC_MODE__===!0}async function P(e,t,o){if(ye())return o();try{const n=await fetch(e,t);if(n.ok&&(n.headers.get("content-type")||"").includes("application/json"))return await n.json()}catch{}return o()}let te=null,ue=null;async function He(){return te||(te=await(await fetch("./static_api/stocks_pro.json")).json()),te}async function pe(){return ue||(ue=await(await fetch("./static_api/semi_overview.json")).json()),ue}async function Ke(e={}){const t=new URLSearchParams;e.search&&t.append("search",e.search),e.zone&&e.zone!=="ALL"&&t.append("zone",e.zone),e.sort_by&&t.append("sort_by",e.sort_by),e.order&&t.append("order",e.order),e.limit&&t.append("limit",e.limit),e.offset&&t.append("offset",e.offset);const o=`/api/stocks${t.toString()?`?${t.toString()}`:""}`;return P(o,{headers:{...de(),Accept:"application/json"}},async()=>{const n=Ue()?"./static_api/stocks_pro.json":"./static_api/stocks_free.json";let i=await(await fetch(n)).json();if(e.search){const r=String(e.search).trim().toLowerCase();i=i.filter(d=>{const g=(d.name||d.name_en||d.name_kr||d.name_jp||"").toLowerCase(),c=`${d.name||""} ${d.name_en||""} ${d.name_kr||""} ${d.name_jp||""}`.toLowerCase();return d.ticker&&d.ticker.toLowerCase().includes(r)||g.includes(r)||c.includes(r)||d.sector&&d.sector.toLowerCase().includes(r)})}if(e.zone&&e.zone!=="ALL"&&(i=i.filter(r=>r.zone_code===e.zone)),e.sort_by){const r=e.sort_by,d=String(e.order||"desc").toLowerCase()!=="asc";i=[...i].sort((g,c)=>{const p=Number(g[r]??0),f=Number(c[r]??0);return d?f-p:p-f})}return i})}async function We(){return P("/api/backtest",{headers:{Accept:"application/json"}},async()=>(await fetch("./static_api/backtest.json")).json())}async function Ye(e){const t=String(e||"CELH").trim().toUpperCase();return P(`/api/research/${encodeURIComponent(t)}`,{headers:{...de(),Accept:"application/json"}},async()=>(await fetch(`./static_api/research_${t==="MBLY"?"MBLY":"CELH"}.json`)).json())}function Ze(e){const t=String(e||"").trim();return t?t.toUpperCase()==="PRO-DEMO-2026"||/^RSA-(PRO|LTD)-2026-[A-Z0-9]{4,12}$/i.test(t)||/^[0-9A-F]{8}-[0-9A-F]{4}-[0-9A-F]{4}-[0-9A-F]{4}-[0-9A-F]{12}$/i.test(t):!1}async function ve(e){return P("/api/auth/license/validate",{method:"POST",headers:{"Content-Type":"application/json",Accept:"application/json"},body:JSON.stringify({license_key:e})},async()=>{const t=String(e||"").trim(),o=Ze(t);return{valid:o,license_key:o?t.toUpperCase():t,tier:o?"pro":"free",message:o?"Pro Terminal License Verified.":"Invalid license key. Use PRO-DEMO-2026 for demo."}})}async function Je(){return P("/api/pro/pinescript",{headers:{...de(),Accept:"application/json"}},async()=>(await fetch("./static_api/pinescript.json")).json())}async function se(e){const t=String(e.ticker||"CELH").trim().toUpperCase(),o=Math.max(.01,Number(e.entry_price||27.93)),n=Number(e.days_held||0),a=await P("/api/pro/position-doctor",{method:"POST",headers:{...de(),"Content-Type":"application/json",Accept:"application/json"},body:JSON.stringify(e)},async()=>{const r=(await He()).find(l=>l.ticker===t),d=r?Number(r.close):o,g=r&&r.date?r.date:"2026-10-13",c=Number(((d/o-1)*100).toFixed(2)),p=Number((o*.91).toFixed(2)),f=Number((o*2).toFixed(2));return c<=-9?{ticker:t,status_code:"CRITICAL_STOP",status_label:"🛑 Hard Stop Loss Triggered",return_pct:c,rule_triggered:"Rule 1 (-9.0% Hard Stop Loss)",action_plan:"Execute immediate market exit. Do not average down on broken support.",is_critical:!0,current_price:d,entry_price:Number(o.toFixed(2)),stop_price:p,tp1_price:f,as_of_date:g}:n>=55&&c<8?{ticker:t,status_code:"DEAD_MONEY",status_label:"⏳ 55-Day Time Stop Triggered",return_pct:c,rule_triggered:"Rule 2 (55-Day Dead-Money Exit)",action_plan:"Exit position. Rebound momentum has stalled; reallocate into active right-side ignition candidates.",is_critical:!1,current_price:d,entry_price:Number(o.toFixed(2)),stop_price:p,tp1_price:f,as_of_date:g}:c>=100?{ticker:t,status_code:"TP1_REACHED",status_label:"🎯 100% Target Price 1 Achieved",return_pct:c,rule_triggered:"Rule 3 (+100% Principal Recovery)",action_plan:"Sell 50% of position to recoup 100% initial capital. Set trailing stop on remaining 50% using MA60.",is_critical:!1,current_price:d,entry_price:Number(o.toFixed(2)),stop_price:p,tp1_price:f,as_of_date:g}:{ticker:t,status_code:"ACTIVE_HOLD",status_label:"🟢 Active Right-Side Trend Follow",return_pct:c,rule_triggered:"Rule 4 (Healthy Trend Follow)",action_plan:"Maintain position. Monitor MA20/MA60 trailing support; runner target is +100% TP1.",is_critical:!1,current_price:d,entry_price:Number(o.toFixed(2)),stop_price:p,tp1_price:f,as_of_date:g}});if(a&&typeof a=="object"){if((a.entry_price===void 0||a.entry_price===null||!(a.entry_price>0))&&(a.entry_price=Number(o.toFixed(2))),a.current_price===void 0||a.current_price===null||!(a.current_price>0)){let i=e.current_price?Number(e.current_price):null;if(!i&&te){const r=te.find(d=>d.ticker===t);r&&(i=Number(r.close))}!i&&a.return_pct!==void 0&&(i=Number((a.entry_price*(1+Number(a.return_pct)/100)).toFixed(2))),a.current_price=i||a.entry_price}(a.stop_price===void 0||a.stop_price===null)&&(a.stop_price=Number((a.entry_price*.91).toFixed(2))),(a.tp1_price===void 0||a.tp1_price===null)&&(a.tp1_price=Number((a.entry_price*2).toFixed(2))),a.as_of_date||(a.as_of_date="2026-10-13")}return a}async function et(){return P("/api/referral/config",{headers:{Accept:"application/json"}},async()=>(await fetch("./static_api/referral_config.json")).json())}async function tt(e){return P("/api/referral/config",{method:"POST",headers:{"Content-Type":"application/json",Accept:"application/json"},body:JSON.stringify(e)},async()=>({status:"updated",config:e}))}async function ot(){return P("/api/semi/overview",{headers:{Accept:"application/json"}},async()=>pe())}async function ze(e="1Y"){const t=String(e||"1Y").trim().toUpperCase(),n=["3M","6M","1Y","3Y","5Y","10Y","ALL"].includes(t)?t:"1Y",a=async()=>(await fetch(`./static_api/semi_history_${n}.json`)).json(),i=await P(`/api/semi/history?range=${encodeURIComponent(n)}`,{headers:{Accept:"application/json"}},a);if(i&&i.range_code&&String(i.range_code).toUpperCase()!==n)try{return await a()}catch{return i}return i}async function Ve(e){return P("/api/semi/rebalance",{method:"POST",headers:{"Content-Type":"application/json",Accept:"application/json"},body:JSON.stringify(e)},async()=>{const t=await pe(),o=Number(t.fg_score??18),n=Number(t.smh_dd_pct??-19.03),a=Number(t.usdkrw??1324.75),i=Number(t.smh_close??541.62),r=Number(t.xlv_close??179.28),d=String(e.strategy_mode||"AUTO_REGIME").trim().toUpperCase(),g=o<25||n<=-19;let c=.7,p=.3,f="",l="",v="";d==="BASELINE_70_30"?(c=.7,p=.3,f="Fixed 70% $SMH : 30% $XLV Golden Barbell Baseline",l="70% $SMH : 30% $XLV 基本黄金バーベル比率",v="평시 70% $SMH : 30% $XLV 기본 황금 바벨 비중"):d==="CONTRARIAN_80_20"?(c=.8,p=.2,f="Contrarian 80% $SMH : 20% $XLV Crash Accumulation Tilt",l="80% $SMH : 20% $XLV 暴落時・逆張り買い増しモード",v="80% $SMH : 20% $XLV 폭락장 역발상 매집 비중"):d==="AGGRESSIVE_90_10"?(c=.9,p=.1,f="90% $SMH : 10% $XLV Right-Side Momentum Tilt",l="90% $SMH : 10% $XLV 右側モメンタム集中モード",v="90% $SMH : 10% $XLV 우측 시동 공격형 비중"):g?(c=.8,p=.2,f=`AUTO REGIME: Extreme Fear (${o}/100, DD ${n.toFixed(1)}%) → 80% $SMH : 20% $XLV Contrarian Shift`,l=`自動判定: 極度の恐怖 (${o}/100, 高値比 ${n.toFixed(1)}%) → 80% $SMH : 20% $XLV 逆張り転換`,v=`자동 판독: 극단적 공포 (${o}/100, 낙폭 ${n.toFixed(1)}%) → 80% $SMH : 20% $XLV 역발상 비중 확대`):(c=.7,p=.3,f=`AUTO REGIME: Standard Regime (${o}/100) → 70% $SMH : 30% $XLV Core Barbell`,l=`自動判定: 通常レジーム (${o}/100) → 70% $SMH : 30% $XLV 基本比率`,v=`자동 판독: 평시 구간 (${o}/100) → 70% $SMH : 30% $XLV 기본 황금비중`);const h=Math.max(100,Number(e.total_capital_usd||1e5)),E=Number((h*c).toFixed(2)),k=Number((h*p).toFixed(2)),y=Math.floor(E/i),$=Math.floor(k/r),L=y*i+$*r,w=Number(Math.max(0,h-L).toFixed(2)),A=Number(t.natural_smh_weight_pct??66.5)/100,R=Number((h*A).toFixed(2)),F=Number((h*(1-A)).toFixed(2)),N=Number((E-R).toFixed(2)),O=Number((k-F).toFixed(2)),j=Math.round(N/i),z=Math.round(O/r),H=String(e.rebalance_frequency||"ANNUAL").trim().toUpperCase(),W={ANNUAL:.19,QUARTERLY:.42,MONTHLY:.78,WEEKLY:1.32}[H]??.19,oe=Number((22.98-W).toFixed(2)),V=25e5,B=Math.max(0,Number(e.unrealized_gain_krw??38e5)),X=Math.max(0,B-V),G=Math.round(Math.min(B,V)*.22),ne=B<=V?`Unrealized gain (₩${B.toLocaleString()}) is within the ₩2,500,000 annual tax-free allowance. Execute your $XLV ↔ $SMH rebalance before Dec 26 to harvest gains with ₩0 tax (saving ₩${G.toLocaleString()}).`:`Unrealized gain (₩${B.toLocaleString()}) exceeds the ₩2.5M tax-free cap by ₩${X.toLocaleString()}. Sell only up to ₩2,500,000 of realized profit this calendar year to lock in the maximum ₩550,000 tax savings, and use new cash inflow for the remaining rebalance.`,ie=B<=V?`評価益 (₩${B.toLocaleString()}) は年間非課税枠 (₩2,500,000) 以内です。年末までにリバランスを実行することで譲渡所得税 ₩0 (節税額 ₩${G.toLocaleString()}) で利益確定と取得単価引き上げが可能です。`:`評価益 (₩${B.toLocaleString()}) が非課税枠を ₩${X.toLocaleString()} 超過しています。今年の売却益を250万ウォンまでに抑えて最大 ₩550,000 を節税し、残りは新規積立資金で比率調整するのが最適です。`,ae=B<=V?`예상 실현차익(₩${B.toLocaleString()})이 연간 해외주식 양도세 기본공제 한도(250만 원) 이내입니다. 연말 전 리밸런싱 매도를 통해 양도세 0원(절세 효과 약 ₩${G.toLocaleString()})으로 취득단가를 높이세요.`:`예상 차익(₩${B.toLocaleString()})이 250만 원 비과세 한도를 ₩${X.toLocaleString()} 초과합니다. 올해는 실현차익 250만 원까지만 부분 매도하여 최대 55만 원 절세 혜택을 챙기고, 부족한 비중은 신규 적립금으로 채우세요.`;return{as_of_date:t.date||"2026-10-26",smh_close:i,xlv_close:r,total_capital_usd:h,total_capital_krw:Math.round(h*a),usdkrw:a,fg_score:o,smh_dd_pct:n,regime_code:t.regime_code||"EXTREME_FEAR",active_rule_en:f,active_rule_jp:l,active_rule_kr:v,target_smh_weight_pct:Number((c*100).toFixed(1)),target_xlv_weight_pct:Number((p*100).toFixed(1)),target_smh_usd:E,target_xlv_usd:k,target_smh_shares:y,target_xlv_shares:$,residual_cash_usd:w,delta_smh_usd:N,delta_xlv_usd:O,delta_smh_shares:j,delta_xlv_shares:z,rebalance_frequency:H,estimated_tax_drag_pct:W,expected_net_cagr_pct:oe,kr_tax_deduction_limit_krw:V,kr_taxable_gain_krw:X,kr_estimated_tax_saved_krw:G,kr_tax_guidance_en:ne,kr_tax_guidance_jp:ie,kr_tax_guidance_kr:ae}})}async function Ge(e){return P("/api/semi/lump-sum",{method:"POST",headers:{"Content-Type":"application/json",Accept:"application/json"},body:JSON.stringify(e)},async()=>{const t=await pe(),o=e.override_fg_score!==void 0&&e.override_fg_score!==null?Number(e.override_fg_score):Number(t.fg_score??18),n=Math.max(100,Number(e.capital_usd||5e4)),a=Number(t.smh_close??541.62),i=Number(t.xlv_close??179.28),r=t.date||"2026-10-26";if(o<=40){const d=o<=25,g=d?.8:.7,c=d?.2:.3,p=Number((n*g).toFixed(2)),f=Number((n*c).toFixed(2));return{as_of_date:r,smh_close:a,xlv_close:i,capital_usd:n,fg_score_used:o,case_code:"CASE_1_FEAR_100PCT",case_title_en:"Case 1 (Score 0–40 · Fear Regime): 100% Immediate Lump-Sum Entry",case_title_jp:"ケース1 (スコア 0–40 · 恐怖圏): 100% 即時一括エントリー",case_title_kr:"Case 1 (지수 0–40 · 공포 구간): 100% 즉시 일시금 진입",summary_en:"Semiconductors are already discounted. Do not hold excess cash—deploy 100% today and rebalance back to 70:30 when $SMH recovers within -10% of its 52-week high.",summary_jp:"半導体セクターは既に割安圏にあります。現金を遊ばせず本日100%投入し、$SMHが高値比-10%以内へ回復した時点で70:30へ戻します。",summary_kr:"반도체 섹터가 이미 할인된 공포 구간입니다. 현금을 놀리지 말고 당일 100% 거치식으로 진입한 뒤, $SMH가 고점 대비 -10% 이내로 회복되면 70:30으로 복귀하세요.",immediate_deploy_pct:100,parked_cash_rp_pct:0,tranches:[{step:1,title_en:"Tranche 1 (Day 1 Immediate 100% Deployment)",title_jp:"第1トランシェ (初日 100% 一括エントリー)",title_kr:"1차 집행 (당일 100% 즉시 거치식 진입)",timing_en:"Execute Today (Market Open / Close)",timing_jp:"本日即時執行 (Fear ≤ 40 割安圏)",timing_kr:"오늘 즉시 집행 (공포 지수 40 이하 저평가 구간)",allocation_pct:100,amount_usd:n,smh_usd:p,xlv_usd:f,cash_rp_usd:0,smh_shares:Math.floor(p/a),xlv_shares:Math.floor(f/i),note_en:`Deploy 100% immediately at ${Math.round(g*100)}:${Math.round(c*100)} ($SMH:$XLV). Historical 1-year forward win rate when entering below score 25 exceeds 91%.`,note_jp:`${Math.round(g*100)}:${Math.round(c*100)} ($SMH:$XLV) 比率で100%即時エントリー。スコア25以下でのエントリーは過去1年後の勝率が91%超。`,note_kr:`${Math.round(g*100)}:${Math.round(c*100)} ($SMH:$XLV) 비중으로 100% 즉시 진입합니다. 공포 지수 25 이하 진입 시 1년 후 플러스 수익 확률은 91% 이상입니다.`}]}}else if(o<=68){const d=Number((n*.35).toFixed(2)),g=Number((n*.3).toFixed(2)),c=Number((d+g).toFixed(2)),p=Number((n*.35).toFixed(2));return{as_of_date:r,smh_close:a,xlv_close:i,capital_usd:n,fg_score_used:o,case_code:"CASE_2_NEUTRAL_65_35",case_title_en:"Case 2 (Score 40–68 · Neutral Regime): 65% Immediate + 35% Pullback Reserve",case_title_jp:"ケース2 (スコア 40–68 · 中立圏): 65% 初日投入 + 35% 押し目待機",case_title_kr:"Case 2 (지수 40–68 · 중립 구간): 65% 선진입 + 35% 달러 RP 파킹 후 분할",summary_en:"Balanced deployment: lock in your 30% $XLV anchor and half of $SMH today, while keeping 35% dry powder for volatility.",summary_jp:"バランス型エントリー：$XLV 30%と$SMH半分を初日に確保し、35%の余力で押し目に備えます。",summary_kr:"중립장 표준 공식: 1일차에 $XLV 30% 전량과 $SMH 절반(35%)을 먼저 채우고, 나머지 35%는 조정 시 추매 실탄으로 활용합니다.",immediate_deploy_pct:65,parked_cash_rp_pct:35,tranches:[{step:1,title_en:"Tranche 1 (Day 1 Core 65% Deployment)",title_jp:"第1トランシェ (初日 65% コア投入)",title_kr:"1차 집행 (1일차 65% 코어 포지션 선진입)",timing_en:"Execute Today (30% $XLV Full + 35% $SMH Half)",timing_jp:"本日執行 ($XLV 30%全額 + $SMH 35%半分)",timing_kr:"오늘 즉시 집행 ($XLV 30% 전량 + $SMH 35% 절반)",allocation_pct:65,amount_usd:c,smh_usd:d,xlv_usd:g,cash_rp_usd:0,smh_shares:Math.floor(d/a),xlv_shares:Math.floor(g/i),note_en:"Establish 100% of your defensive $XLV position (30%) and half of your $SMH position (35%) immediately.",note_jp:"ディフェンシブ枠の$XLV (30%) 全額と、成長枠$SMHの半分 (35%) を初日に構築します。",note_kr:"방어주 $XLV(30%) 전량과 반도체 $SMH 목표치의 절반(35%)을 첫날 즉시 매수합니다."},{step:2,title_en:"Tranche 2 (Remaining 35% $SMH Reserve in USD RP)",title_jp:"第2トランシェ (残り35% $SMH待機資金・米ドルMMF)",title_kr:"2차 집행 (잔여 35% 달러 RP 파킹 후 조건부 투입)",timing_en:"Deploy when FG Score ≤ 40 OR split across D+30 / D+60 / D+90",timing_jp:"スコア40以下へ低下時、または30日・60日・90日で3分割投入",timing_kr:"공포지수 40 이하 하락 시 즉시 투입 (미도달 시 30·60·90일 3분할)",allocation_pct:35,amount_usd:p,smh_usd:p,xlv_usd:0,cash_rp_usd:p,smh_shares:Math.floor(p/a),xlv_shares:0,note_en:"Earn ~4.5% USD RP yield while waiting for a pullback below score 40, or auto-deploy over 90 days.",note_jp:"米ドルMMFで金利を受け取りながらスコア40以下への押し目を待つか、90日間で機械的に分割投入します。",note_kr:"달러 RP(연 4%대 금리)에 예치해 두었다가 지수가 40 이하로 내려오면 즉시 투입하고, 안 내려오면 3개월간 균등 분할 매수합니다."}]}}else{const d=Number((n*.3).toFixed(2)),g=Number((n*.7).toFixed(2));return{as_of_date:r,smh_close:a,xlv_close:i,capital_usd:n,fg_score_used:o,case_code:"CASE_3_GREED_DEFENSIVE_FIRST",case_title_en:"Case 3 (Score 68–100 · Greed Regime): 30% $XLV Today + 70% $SMH Parked in USD RP",case_title_jp:"ケース3 (スコア 68–100 · 強欲圏): 初日 $XLV 30%のみ + 70% 米ドルMMF待機",case_title_kr:"Case 3 (지수 68–100 · 탐욕 과열 구간): 당일 $XLV 30%만 진입 + 70% 달러 RP 대기",summary_en:"Protect principal against euphoria: buy only the 30% $XLV sleeve today and keep 70% in USD RP until Fear & Greed cools to 45 or below.",summary_jp:"高値掴み防止ルール：初日は$XLV 30%のみを購入し、70%は指数が45以下に冷めるまで米ドルMMFで待機します。",summary_kr:"고점 추격매수 방지 공식: 당일에는 방어주 $XLV 30%만 매수하고, $SMH 70% 자금은 지수가 45 이하로 내려올 때까지 달러 RP에서 이자를 받으며 대기합니다.",immediate_deploy_pct:30,parked_cash_rp_pct:70,tranches:[{step:1,title_en:"Tranche 1 (Day 1 Defensive $XLV 30% Only)",title_jp:"第1トランシェ (初日はディフェンシブ $XLV 30% のみ購入)",title_kr:"1차 집행 (1일차 방어주 $XLV 30%만 우선 진입)",timing_en:"Execute Today ($XLV Anchor Only — Zero $SMH Chasing)",timing_jp:"本日執行 ($XLV 30%のみ・過熱した$SMHの高値追い禁止)",timing_kr:"오늘 즉시 집행 (과열된 $SMH 추격매수 금지, $XLV 30%만 매수)",allocation_pct:30,amount_usd:d,smh_usd:0,xlv_usd:d,cash_rp_usd:0,smh_shares:0,xlv_shares:Math.floor(d/i),note_en:"Do not chase overheated semiconductors above score 68. Deploy only the 30% Healthcare anchor on Day 1.",note_jp:"スコア68超の過熱局面での半導体ジャンピングキャッチを回避し、ヘルスケア枠30%のみを先行構築します。",note_kr:"탐욕 지수 68 초과 과열 구간에서는 반도체 고점 물림을 피하기 위해 방어주 $XLV 30%만 우선 매수합니다."},{step:2,title_en:"Tranche 2 (70% $SMH Capital Parked in Yielding USD RP)",title_jp:"第2トランシェ (70% $SMH資金は米ドルMMFで冷却待機)",title_kr:"2차 집행 (70% $SMH 몫은 달러 RP 파킹 후 지수 ≤ 45 냉각 시 투입)",timing_en:"Deploy when FG Score cools ≤ 45 (or 4 monthly tranches)",timing_jp:"スコア45以下へ冷却時、または4ヶ月分割で順次エントリー",timing_kr:"공포·탐욕 지수가 45 이하로 식을 때 투입 (또는 4개월 분할)",allocation_pct:70,amount_usd:g,smh_usd:g,xlv_usd:0,cash_rp_usd:g,smh_shares:Math.floor(g/a),xlv_shares:0,note_en:"Collect risk-free USD interest while waiting for semiconductor euphoria to mean-revert.",note_jp:"米ドル金利を確保しながら、半導体の過熱感が冷めるのを待って安全にエントリーします。",note_kr:"달러 RP 이자를 받으며 반도체 과열이 해소될 때까지 기다렸다가 안전하게 진입하여 고점 낙폭을 방어합니다."}]}}})}const De="9245553889:AAGCiCKCDeHZGNfY85iHxm6azY72bmad6gU",le="https://t.me/RigjtsideAlphabot";function me(){if(typeof localStorage>"u")return{bot_token:De,chat_id:"",channel_url:le,auto_alert_ignition:!0,auto_alert_stop:!0,auto_alert_semi_regime:!0,has_local_ignition:!1,has_local_stop:!1,has_local_semi:!1};const e=localStorage.getItem("rsa_tg_auto_ignition"),t=localStorage.getItem("rsa_tg_auto_stop"),o=localStorage.getItem("rsa_tg_auto_semi"),n=(localStorage.getItem("rsa_tg_bot_token")||"").trim();return{bot_token:n&&!n.includes("...")?n:De,chat_id:(localStorage.getItem("rsa_tg_chat_id")||"").trim(),channel_url:(localStorage.getItem("rsa_tg_channel_url")||le).trim(),auto_alert_ignition:e!==null?e!=="false":!0,auto_alert_stop:t!==null?t!=="false":!0,auto_alert_semi_regime:o!==null?o!=="false":!0,has_local_ignition:e!==null,has_local_stop:t!==null,has_local_semi:o!==null}}async function nt(){const e=me(),t=await P("/api/telegram/status",{headers:{Accept:"application/json"}},async()=>{try{const i=await fetch("./static_api/telegram_status.json");if(i.ok)return await i.json()}catch{}return{}}),o=!!(e.bot_token&&e.chat_id),n=!!(t!=null&&t.configured||o),a=e.bot_token?`${e.bot_token.slice(0,6)}...${e.bot_token.slice(-4)}`:(t==null?void 0:t.bot_token_masked)||"";return{...t,configured:n,has_bot_token:!!(t!=null&&t.has_bot_token||e.bot_token),has_chat_id:!!(t!=null&&t.has_chat_id||e.chat_id),bot_token_masked:a,chat_id:e.chat_id||(t==null?void 0:t.chat_id)||"",channel_url:e.channel_url||(t==null?void 0:t.channel_url)||"https://t.me/RightSideAlphaBot",auto_alert_ignition:e.has_local_ignition?e.auto_alert_ignition:(t==null?void 0:t.auto_alert_ignition)??!0,auto_alert_stop:e.has_local_stop?e.auto_alert_stop:(t==null?void 0:t.auto_alert_stop)??!0,auto_alert_semi_regime:e.has_local_semi?e.auto_alert_semi_regime:(t==null?void 0:t.auto_alert_semi_regime)??!0}}async function it(e={}){const t=me(),o=e.bot_token!==void 0?String(e.bot_token).trim():"",n=o&&!o.includes("...")?o:t.bot_token,a=e.chat_id!==void 0?String(e.chat_id).trim():t.chat_id,i=e.channel_url!==void 0?String(e.channel_url).trim()||le:t.channel_url||le,r=e.auto_alert_ignition!==void 0?!!e.auto_alert_ignition:t.auto_alert_ignition,d=e.auto_alert_stop!==void 0?!!e.auto_alert_stop:t.auto_alert_stop,g=e.auto_alert_semi_regime!==void 0?!!e.auto_alert_semi_regime:t.auto_alert_semi_regime;typeof localStorage<"u"&&(localStorage.setItem("rsa_tg_bot_token",n),localStorage.setItem("rsa_tg_chat_id",a),localStorage.setItem("rsa_tg_channel_url",i),localStorage.setItem("rsa_tg_auto_ignition",String(r)),localStorage.setItem("rsa_tg_auto_stop",String(d)),localStorage.setItem("rsa_tg_auto_semi",String(g)));const p=await P("/api/telegram/config",{method:"POST",headers:{"Content-Type":"application/json",Accept:"application/json"},body:JSON.stringify({bot_token:n,chat_id:a,channel_url:i,auto_alert_ignition:r,auto_alert_stop:d,auto_alert_semi_regime:g})},async()=>({ok:!0,status:"updated",configured:!!(n&&a),chat_id:a,channel_url:i,auto_alert_ignition:r,auto_alert_stop:d,auto_alert_semi_regime:g}));return{...p,ok:!0,configured:!!(p!=null&&p.configured||n&&a),has_bot_token:!!(n||p!=null&&p.has_bot_token),has_chat_id:!!(a||p!=null&&p.has_chat_id),chat_id:a||(p==null?void 0:p.chat_id)||"",channel_url:i,auto_alert_ignition:r,auto_alert_stop:d,auto_alert_semi_regime:g}}async function je(e){var a,i,r,d;const t=me(),o=String(e||"").trim(),n=(o&&!o.includes("...")?o:t.bot_token).trim();if(n&&!n.includes("...")&&typeof localStorage<"u"&&localStorage.setItem("rsa_tg_bot_token",n),!ye())try{const g=await fetch("/api/telegram/detect-chat-id",{method:"POST",headers:{"Content-Type":"application/json",Accept:"application/json"},body:JSON.stringify({bot_token:n||void 0})});if(g.ok){const c=await g.json();if(c&&c.ok&&c.chat_id&&!c.simulated)return typeof localStorage<"u"&&localStorage.setItem("rsa_tg_chat_id",String(c.chat_id)),c}}catch{}if(!n)return{ok:!1,chat_id:"",detail:"Please enter your Telegram Bot Token from @BotFather first."};try{const g=await fetch(`https://api.telegram.org/bot${n}/getUpdates?limit=25`),c=await g.json();if(!g.ok||!c.ok)return{ok:!1,chat_id:"",detail:(c==null?void 0:c.description)||"Telegram Bot API rejected the token. Verify your @BotFather token."};const p=Array.isArray(c.result)?c.result:[];for(let f=p.length-1;f>=0;f--){const l=p[f]||{},v=((a=l.message)==null?void 0:a.chat)||((i=l.channel_post)==null?void 0:i.chat)||((r=l.edited_message)==null?void 0:r.chat)||((d=l.my_chat_member)==null?void 0:d.chat);if(v&&v.id!==void 0){const h=String(v.id);return typeof localStorage<"u"&&localStorage.setItem("rsa_tg_chat_id",h),{ok:!0,chat_id:h,chat_title:v.title||v.first_name||v.username||"Telegram Chat",username:v.username||""}}}return{ok:!1,chat_id:"",detail:"No recent messages found. Open your bot in Telegram, send /start, and click Auto-Detect again."}}catch{return{ok:!1,chat_id:"",detail:"Could not reach api.telegram.org. Enter your Chat ID manually or verify network access."}}}async function at(e={}){const t=String(e.briefing_type||"test").trim().toLowerCase(),[o,n]=await Promise.all([He().catch(()=>[]),pe().catch(()=>null)]),a=[...o||[]].filter(y=>y.zone_code==="IGNITION_ZONE").sort((y,$)=>Number($.score||0)-Number(y.score||0)),i=(a.length?a:o||[]).slice(0,5),r=i[0]||{ticker:"CELH",score:90,close:27.93,entry_trigger_price:29.12,stop_loss_price:25.42,tp1_2x_price:55.86,date:"2026-10-13"},d=Number((n==null?void 0:n.fg_score)??18).toFixed(1),g=String((n==null?void 0:n.regime_en)||"EXTREME FEAR").toUpperCase(),c=Number((n==null?void 0:n.smh_close)??541.62).toFixed(2),p=Number((n==null?void 0:n.smh_dd_pct)??-19.03).toFixed(2),f=Number((n==null?void 0:n.xlv_close)??179.28).toFixed(2),l=Number((n==null?void 0:n.qqq_close)??712.2).toFixed(2),v=(n==null?void 0:n.date)||"2026-10-26",h=(n==null?void 0:n.recommended_smh_weight)??80,E=(n==null?void 0:n.recommended_xlv_weight)??20;if(t==="test")return["🟢 <b>RightSideAlpha × SemiFearGreed — Telegram Quant Alert Connected</b>","","• <b>Universe:</b> 72 Liquid NYSE & NASDAQ Equities (N = 394,371 Stock-Days)",`• <b>Top Right-Side Ignition:</b> <code>$${r.ticker}</code> (Score ${r.score}/100) | Close <b>$${Number(r.close).toFixed(2)}</b>`,`  ↳ TRG: <b>$${Number(r.entry_trigger_price).toFixed(2)}</b> | STP (-9%): <b>$${Number(r.stop_loss_price).toFixed(2)}</b> | TP1 (2x): <b>$${Number(r.tp1_2x_price).toFixed(2)}</b>`,`• <b>SemiFearGreed Index (${v}):</b> <b>${d} / 100 (${g})</b>`,`  ↳ Active Barbell Signal: <b>${h}% $SMH ($${c}) : ${E}% $XLV ($${f})</b>`,"","✅ Real-time Ignition Breakouts, Position Doctor -9% / 55D Stops & 80:20 Contrarian Signals are active."].join(`
`);if(t==="ignition"){const y=["📊 <b>RightSideAlpha — Top 5 Right-Side Ignition Breakouts</b>",`<i>Post-Washout (1.40x+ Vol) + MA20/MA60 Simultaneous Reclaim (${r.date||"2026-10-13"})</i>`,""];return i.forEach(($,L)=>{const w=Number($.close||0).toFixed(2),A=Number($.entry_trigger_price??$.close??0).toFixed(2),R=Number($.stop_loss_price??Number(w)*.91).toFixed(2),F=Number($.tp1_2x_price??Number(w)*2).toFixed(2),N=Number($.vol_surge_10d??1.4).toFixed(2);y.push(`<b>${L+1}. $${$.ticker}</b> (${$.name_en||$.name||$.ticker}) — Score <b>${$.score}/100</b>`,`   Close: <b>$${w}</b> | TRG: <b>$${A}</b> | STP (-9%): <b>$${R}</b> | TP1 (2x): <b>$${F}</b> | Vol: ${N}x`)}),y.push("","📌 <b>Execution Rule:</b> Hard Stop at -9.0% below entry; 55-Day Time-Stop if gain &lt; +8.0%."),y.join(`
`)}if(t==="semi")return["🧭 <b>SemiFearGreed — CNN-Style 7-Factor Index &amp; 80:20 Barbell Signal</b>",`<i>As of Latest Close (${v}) · 26-Year Verified Barbell Engine</i>`,"",`• <b>Fear &amp; Greed Score:</b> <b>${d} / 100 (${g})</b>`,`• <b>$SMH (AI Semiconductor):</b> <b>$${c}</b> (${p}% off 52W High) → Target <b>${h}%</b>`,`• <b>$XLV (Healthcare Defense):</b> <b>$${f}</b> → Target <b>${E}%</b>`,`• <b>$QQQ (Nasdaq-100 Bench):</b> <b>$${l}</b>`,"",`⚡ <b>Active Directive:</b> ${(n==null?void 0:n.action_headline_en)||"80% $SMH : 20% $XLV Contrarian Accumulation Triggered"}`,"📈 <b>26Y Track Record:</b> +10.60% CAGR (14.22x) vs $QQQ +8.79% (9.21x) | 10Y AI Era: +28.63% CAGR."].join(`
`);if(t==="doctor"){const y=e.doctor_result||await se({ticker:e.ticker||"CELH",entry_price:e.entry_price||27.93,days_held:e.days_held??42}),$=Number((y==null?void 0:y.return_pct)??0),L=`${$>=0?"+":""}${$.toFixed(2)}%`;return["🩺 <b>RightSideAlpha — Position Doctor Risk &amp; 55-Day Time-Stop Diagnostic</b>","",`• <b>Security:</b> <code>$${y.ticker||"CELH"}</code> (As of ${y.as_of_date||"2026-10-13"})`,`• <b>Status:</b> <b>${y.status_label||y.status_code||"ACTIVE_HOLD"}</b>`,`• <b>Latest Close:</b> <b>$${Number(y.current_price||27.93).toFixed(2)}</b> | <b>Cost Basis:</b> <b>$${Number(y.entry_price||27.93).toFixed(2)}</b> (P&amp;L: <b>${L}</b>)`,`• <b>Rule Triggered:</b> ${y.rule_triggered||"Rule 4 (Healthy Trend Follow)"}`,`• <b>Hard Stop (-9%):</b> <b>$${Number(y.stop_price||25.42).toFixed(2)}</b> | <b>TP1 Target (2x):</b> <b>$${Number(y.tp1_price||55.86).toFixed(2)}</b>`,"",`📋 <b>Execution Directive:</b> ${y.action_plan||"Maintain position and monitor MA20/MA60 trailing support."}`].join(`
`)}const k=i.slice(0,5).map((y,$)=>`  ${$+1}. <b>$${y.ticker}</b> (Score ${y.score}) — Close $${Number(y.close).toFixed(2)} | TRG $${Number(y.entry_trigger_price).toFixed(2)} | STP $${Number(y.stop_loss_price).toFixed(2)} | TP1 $${Number(y.tp1_2x_price).toFixed(2)}`).join(`
`);return["📑 <b>RightSideAlpha × SemiFearGreed — Institutional Morning Executive Brief</b>","<i>US Equity Right-Side Ignition &amp; Semiconductor 80:20 Barbell Terminal</i>","",`<b>1️⃣ TOP 5 RIGHT-SIDE IGNITION BREAKOUTS (${r.date||"2026-10-13"})</b>`,k,"",`<b>2️⃣ SEMICONDUCTOR FEAR &amp; GREED INDEX (${v})</b>`,`  • Score: <b>${d} / 100 (${g})</b>`,`  • $SMH: <b>$${c}</b> (${p}% DD) | $XLV: <b>$${f}</b> | $QQQ: <b>$${l}</b>`,`  • Allocation Signal: <b>${h}% $SMH : ${E}% $XLV</b> (${(n==null?void 0:n.action_headline_en)||"Contrarian Accumulation"})`,"","<b>3️⃣ ASYMMETRIC RISK PROTOCOL</b>","  • Rule 1: <b>-9.0% Hard Stop Loss</b> (Zero averaging down on broken support)","  • Rule 2: <b>55-Day Time-Stop</b> if position return &lt; +8.0%","  • Rule 3: <b>+100% TP1 Principal Harvest</b> (Sell 50%, trail remaining 50% on MA60)"].join(`
`)}async function qe(e={}){var g;const t=me(),o=String(e.bot_token??"").trim(),n=o&&!o.includes("...")?o:t.bot_token;let a=String(e.chat_id??t.chat_id??"").trim();const i=String(e.briefing_type||"test").trim().toLowerCase();if(n&&!a){const c=await je(n).catch(()=>null);c&&c.ok&&c.chat_id&&(a=String(c.chat_id))}let r=null;if(!ye())try{const c=await fetch("/api/telegram/send-briefing",{method:"POST",headers:{"Content-Type":"application/json",Accept:"application/json"},body:JSON.stringify({...e,briefing_type:i,bot_token:n||void 0,chat_id:a||void 0})});if(c.ok&&(r=await c.json(),r&&r.delivered))return r}catch{}const d=(r==null?void 0:r.message_preview)||await at(e);if(n&&a)try{const c=await fetch(`https://api.telegram.org/bot${n}/sendMessage`,{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({chat_id:a,text:d,parse_mode:"HTML",disable_web_page_preview:!0})}),p=await c.json();return c.ok&&p.ok?{ok:!0,delivered:!0,simulated:!1,briefing_type:i,chat_id:a,message_id:(g=p.result)==null?void 0:g.message_id,message_preview:d,detail:`Delivered live to Telegram (${a})`}:{ok:!1,delivered:!1,simulated:!0,briefing_type:i,message_preview:d,detail:(p==null?void 0:p.description)||"Telegram API rejected dispatch — showing preview below."}}catch{return{ok:!0,delivered:!1,simulated:!0,briefing_type:i,message_preview:d,detail:"Preview generated (Direct Telegram API call blocked or offline)"}}return{ok:!0,delivered:!1,simulated:!0,briefing_type:i,message_preview:d,detail:(r==null?void 0:r.detail)||"Preview generated (Enter Bot Token & Chat ID to deliver live to Telegram)"}}async function rt(e={}){return qe({...e,briefing_type:"test"})}const st=e=>e?e.includes("?")?e.includes("embed=1")?e:`${e}&embed=1`:`${e}?embed=1`:"#";function lt(e){var w,A,R,F;const t=e.t,o=e.lang,n=e.isProUnlocked,a=e.activeView||"rightside",i=e.semiOverview,r=i&&i.fg_score!==void 0?Number(i.fg_score).toFixed(1):"18.0",d=i?e.lang==="kr"?i.regime_kr||i.regime_en:e.lang==="jp"?i.regime_jp||i.regime_en:i.regime_en||"NEUTRAL":"NEUTRAL",g=String(d||"NEUTRAL").toUpperCase(),c=i&&i.date?i.date:"2026-10-26",p=i&&i.smh_close!==void 0?Number(i.smh_close).toFixed(2):"541.62",f=i&&i.xlv_close!==void 0?Number(i.xlv_close).toFixed(2):"179.28",l=i&&i.qqq_close!==void 0?Number(i.qqq_close).toFixed(2):"712.20",v=i&&Array.isArray(i.etfs)?i.etfs:[],h=v.find(N=>N.ticker==="QQQ"),E=v.find(N=>N.ticker==="SMH"),k=v.find(N=>N.ticker==="XLV"),y=h&&h.ret_1d_pct!==void 0?Number(h.ret_1d_pct):1.11,$=E&&E.dd_52w_pct!==void 0?Number(E.dd_52w_pct):i&&i.smh_dd_pct!==void 0?Number(i.smh_dd_pct):-19.03,L=k&&k.ret_1d_pct!==void 0?Number(k.ret_1d_pct):Number((i==null?void 0:i.xlv_1d_pct)??0);return`
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
            <span>$${l}</span>
            <span class="${y>=0?"tape-up":"tape-down"}">${y>=0?"+":""}${y.toFixed(2)}%</span>
          </span>
          <span class="tape-item">
            <span class="tape-sym">SMH</span>
            <span>$${p}</span>
            <span class="tape-down">${$.toFixed(2)}% DD</span>
          </span>
          <span class="tape-item">
            <span class="tape-sym">XLV</span>
            <span>$${f}</span>
            <span class="${L>=0?"tape-up":"tape-down"}">${L>=0?"+":""}${L.toFixed(2)}%</span>
          </span>
          <span class="tape-item" style="cursor:pointer;" id="ribbonSwitchSemi">
            <span class="tape-sym">SEMI FEAR & GREED</span>
            <span class="tape-down" style="font-weight:700;">${r} / 100 (${g})</span>
          </span>
        </div>
        <div class="mono" style="font-size:0.68rem; color:var(--muted);">
          LATEST CLOSE BASIS (${c}) · NYSE / NASDAQ FEED
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
              <span class="platform-tab-tag" style="color:#fca5a5; background:rgba(220,38,38,0.2);">${r}</span>
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

          <button class="btn" id="btnOpenTelegram" style="border-color:rgba(96,165,250,0.4);">
            <span
              id="tgHeaderStatusDot"
              style="width:7px; height:7px; border-radius:50%; display:inline-block; background:${(w=e.telegramStatus)!=null&&w.configured||(A=e.config)!=null&&A.tg_chat_id?"#10b981":"#60a5fa"};"
            ></span>
            <span id="btnTelegramLabel">📲 ${((R=t.telegram)==null?void 0:R.btnTelegram)||"Telegram"}</span>
          </button>

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
            data-plan="monthly"
            href="${st((F=e.config)==null?void 0:F.ls_site1_monthly_url)}"
            style="${n?"display:none;":""}"
          >
            <span id="btnUnlockPro">${t.btnUnlockPro}</span>
          </a>
        </div>
      </div>
    </header>
  `}function ct(e){const t=e.t,o=e.backtestKpis||{},n=Number(o.hit_rate_2x_pct??55.24).toFixed(2),a=Number(o.median_days_underwater??29).toFixed(1),i=Number(o.cagr_after_tax_pct??o.us_only_net_cagr_pct??17.81).toFixed(2),r=Number(o.severe_loss_risk_pct??.93).toFixed(2),d=e.stocks&&e.stocks.length>0&&e.stocks[0].date?e.stocks[0].date:"2026-10-13";return`
    <section class="hero">
      <div class="hero-top-row">
        <div>
          <div class="hero-tag" id="heroTag">${t.heroTag}</div>
          <h1 id="heroTitle">${t.heroTitle}</h1>
          <p id="heroDesc">${t.heroDesc}</p>
        </div>
        <div style="background:#0a0e18; border:1px solid var(--border); border-radius:4px; padding:12px 16px; min-width:250px;">
          <div style="font-size:0.68rem; color:var(--muted); font-family:var(--font-mono); text-transform:uppercase; letter-spacing:0.05em;">
            UNIVERSE SPECIFICATION · LATEST CLOSE (${d})
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
          <div class="kpi-val">${r}%</div>
          <div class="kpi-sub" id="kpi4_sub">${t.kpi4_sub}</div>
        </div>
      </div>
    </section>
  `}function dt(e){const t=e.t;return`
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
  `}function pt(e){const t=e.t,o=e.zoneFilter,n=(e.stocks||[]).filter(c=>!String(c.ticker).includes(".")),a=n.length,i=n.filter(c=>c.zone_code==="IGNITION_ZONE").length,r=n.filter(c=>c.zone_code==="WASHOUT_WATCH").length,d=n.filter(c=>c.zone_code==="LEFT_SIDE_KNIFE").length,g=n.filter(c=>c.zone_code==="VALUE_TRAP_FILTERED").length;return`
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
            <span class="tab-count">${r}</span>
          </button>
          <button class="filter-tab ${o==="LEFT_SIDE_KNIFE"?"active":""}" data-zone="LEFT_SIDE_KNIFE">
            <span style="width:6px; height:6px; border-radius:50%; background:var(--fin-down); display:inline-block;"></span>
            <span>${t.filterKnife}</span>
            <span class="tab-count">${d}</span>
          </button>
          <button class="filter-tab ${o==="VALUE_TRAP_FILTERED"?"active":""}" data-zone="VALUE_TRAP_FILTERED">
            <span>${t.filterTrap}</span>
            <span class="tab-count">${g}</span>
          </button>
        </div>
      </div>
    </div>
  `}function mt(e){const t=e.t,o=e.sortCol||"score",n=!!e.sortAsc,a=i=>o===i?n?"↑":"↓":"↕";return`
    <div class="table-wrap">
      <table class="stock-table" id="stockTable">
        <thead>
          <tr>
            <th data-sort="ticker" class="sort-header">${t.colTicker} <span class="sort-arrow">${a("ticker")}</span></th>
            <th data-sort="zone_code" class="sort-header">${t.colZone} <span class="sort-arrow">${a("zone_code")}</span></th>
            <th data-sort="score" class="sort-header">${t.colScore} <span class="sort-arrow">${a("score")}</span></th>
            <th data-sort="close" class="sort-header">${t.colClose} <span class="sort-arrow">${a("close")}</span></th>
            <th data-sort="prox_low52_pct" class="sort-header">${t.colProx} <span class="sort-arrow">${a("prox_low52_pct")}</span></th>
            <th data-sort="dd_high52_pct" class="sort-header">${t.colDD} <span class="sort-arrow">${a("dd_high52_pct")}</span></th>
            <th data-sort="vs_ma20_pct" class="sort-header">${t.colMA} <span class="sort-arrow">${a("vs_ma20_pct")}</span></th>
            <th data-sort="vol_surge_10d" class="sort-header">${t.colVol} <span class="sort-arrow">${a("vol_surge_10d")}</span></th>
            <th data-sort="hist_2x_rate" class="sort-header">${t.colHist} <span class="sort-arrow">${a("hist_2x_rate")}</span></th>
            <th>${t.colTrigger}</th>
            <th>${t.colActions}</th>
          </tr>
        </thead>
        <tbody id="tableBody">
          ${_e(e)}
        </tbody>
      </table>
    </div>
  `}function _e(e){var i;const t=e.t||{},o=(e.filteredStocks||[]).filter(r=>!String(r.ticker).includes(".")),n=e.lang,a=e.isProUnlocked;return o.length?o.map(r=>{var H;let d="badge-watch";r.zone_code==="IGNITION_ZONE"?d="badge-ignition":r.zone_code==="LEFT_SIDE_KNIFE"?d="badge-knife":r.zone_code==="VALUE_TRAP_FILTERED"&&(d="badge-trap");const g=n==="jp"?r.zone_label_jp:n==="kr"?r.zone_label_kr:r.zone_label_en,c=String(g||r.zone_code).replace(/^[🟢🟡🔴⚠️\s]+/,""),p=n==="jp"?r.name_jp:n==="kr"?r.name_kr:r.name_en,f=r.vs_ma20_pct>=0?"var(--fin-up)":"var(--fin-down)",l=r.vs_ma60_pct>=0?"var(--fin-up)":"var(--fin-down)",v=r.vol_surge_10d>=1.35?"var(--fin-up)":"var(--text-secondary)";let h="";r.vs_ma20_pct>=0&&r.vs_ma60_pct>=0?h='<div style="margin-top:2px;"><span class="ma-badge pass">MA20·60 ↑</span></div>':(r.c3_above_mas||r.c3_ma_reclaim)&&(h='<div style="margin-top:2px;"><span class="ma-badge pass">MA20↑·60 RECLAIM</span></div>');const E=Number(r.low52||0),k=Number(r.high52||r.close*1.5),y=Number(r.close||0),$=Math.max(.01,k-E),L=Math.min(100,Math.max(2,Math.round((y-E)/$*100))),w=a||!r.is_pro_locked&&r.stop_loss_price!==null&&r.stop_loss_price!==void 0,A=r.entry_trigger_price??r.ma60_price,R=A!=null?`$${Number(A).toFixed(2)}`:"LOCKED",F=r.stop_loss_price!==null&&r.stop_loss_price!==void 0?`$${Number(r.stop_loss_price).toFixed(2)}`:"LOCKED",N=r.tp1_2x_price!==null&&r.tp1_2x_price!==void 0?`$${Number(r.tp1_2x_price).toFixed(2)}`:"LOCKED",O=w?`<div class="mono" style="font-size:0.75rem; line-height:1.45;">
             <div><span style="color:var(--muted);">TRG</span> <span style="color:#60a5fa; font-weight:700;">${R}</span></div>
             <div><span style="color:var(--muted);">STP</span> <span style="color:var(--fin-down); font-weight:600;">${F}</span> · <span style="color:var(--fin-up);">TP ${N}</span></div>
           </div>`:`<button type="button" class="pro-lock-cell btn-unlock-row btn-unlock-inline" title="Click to enter Pro license key">🔒 ${((H=t.table)==null?void 0:H.locked)||"PRO TARGETS"}</button>`,j=`/api/referral/redirect/tradingview?ticker=${encodeURIComponent(r.ticker)}`,z=`/api/referral/redirect/seekingalpha?ticker=${encodeURIComponent(r.ticker)}`;return`
      <tr data-ticker="${r.ticker}">
        <td>
          <div style="display:flex; align-items:center; gap:7px;">
            <span class="mono" style="font-weight:800; font-size:0.9rem; color:#ffffff;">${r.ticker}</span>
            <span style="font-size:0.62rem; font-family:var(--font-mono); padding:1px 4px; background:#141d2f; border:1px solid #24324d; color:#93c5fd; border-radius:2px;">US</span>
          </div>
          <div style="font-size:0.73rem; font-family:var(--font-sans); color:var(--muted); margin-top:2px;">
            ${p} · <span style="color:var(--text-secondary);">${r.sector}</span>
          </div>
        </td>
        <td>
          <span class="badge ${d}">${c}</span>
          <div class="cond-strip">
            <span class="cond-chip ${r.c1_deep_dd?"pass":""}" title="52W High Drawdown <= -20%">DD</span>
            <span class="cond-chip ${r.c2_off_low??r.c2_sweet_spot?"pass":""}" title="52W Low Proximity 10-45%">LOW</span>
            <span class="cond-chip ${r.c3_above_mas??r.c3_ma_reclaim?"pass":""}" title="Reclaimed MA20/MA60">MA</span>
            <span class="cond-chip ${r.c4_vol_or_mom??r.c4_vol_washout?"pass":""}" title="10D Volume Washout >= 1.3x">VOL</span>
          </div>
        </td>
        <td>
          <div style="display:flex; align-items:center;">
            <span class="mono" style="font-weight:800; font-size:0.9rem; width:26px;">${Number(r.score??0)}</span>
            <div class="score-bar">
              <div class="score-fill" style="width:${Number(r.score??0)}%; background:${r.score>=80?"var(--fin-up)":r.score>=55?"var(--fin-amber)":"var(--fin-down)"};"></div>
            </div>
          </div>
        </td>
        <td>
          <div class="mono" style="font-weight:700; color:#ffffff;" title="Latest Close Date: ${r.date||"2026-10-13"}">$${y.toFixed(2)}</div>
          <div class="range-52w-wrap" title="52W Range: $${E.toFixed(2)} – $${k.toFixed(2)}">
            <div class="range-52w-track">
              <div class="range-52w-fill" style="width:${L}%;"></div>
            </div>
            <div class="range-52w-labels">
              <span>L:$${E.toFixed(0)}</span>
              <span>H:$${k.toFixed(0)}</span>
            </div>
          </div>
        </td>
        <td class="mono" style="color:${r.prox_low52_pct<=40&&r.prox_low52_pct>=10?"var(--fin-up)":"var(--text-secondary)"}; font-weight:600;">
          +${Number(r.prox_low52_pct??0).toFixed(1)}%
        </td>
        <td class="mono" style="color:var(--fin-down); font-weight:600;">
          ${Number(r.dd_high52_pct??0).toFixed(1)}%
        </td>
        <td class="mono">
          <div>
            <span style="color:${f}; font-weight:600;">${Number(r.vs_ma20_pct??0)>=0?"+":""}${Number(r.vs_ma20_pct??0).toFixed(1)}%</span>
            <span style="color:var(--muted);"> / </span>
            <span style="color:${l}; font-weight:600;">${Number(r.vs_ma60_pct??0)>=0?"+":""}${Number(r.vs_ma60_pct??0).toFixed(1)}%</span>
          </div>
          ${h}
        </td>
        <td class="mono" style="color:${v}; font-weight:700;">
          ${Number(r.vol_surge_10d??1).toFixed(2)}x
        </td>
        <td class="mono" style="font-weight:700; color:${r.hist_2x_rate>=40?"var(--fin-up)":"var(--text-secondary)"};">
          ${Number(r.hist_2x_rate??0).toFixed(1)}%
        </td>
        <td>${O}</td>
        <td>
          <div style="display:flex; gap:5px;">
            <button class="btn btn-sm btn-share-card" data-ticker="${r.ticker}" title="Export Institutional Tear Sheet PNG">
              PNG
            </button>
            <a class="btn btn-sm" href="${j}" target="_blank" rel="noopener noreferrer" title="Open TradingView Chart">
              TV ↗
            </a>
            <a class="btn btn-sm" href="${z}" target="_blank" rel="noopener noreferrer" title="Open Seeking Alpha Fundamentals">
              SA ↗
            </a>
          </div>
        </td>
      </tr>
    `}).join(""):`
      <tr>
        <td colspan="11" style="text-align:center; padding:36px; color:var(--muted); font-family:var(--font-sans);">
          ${((i=t.table)==null?void 0:i.empty)||"No US-listed equities match the active filter criteria."}
        </td>
      </tr>
    `}function ut(e){const t=e.t||{},o=t.doctor||{},n=e.stocks||[],a=n.find(f=>f.ticker==="CELH"),i=a?Number(a.close).toFixed(2):"27.93",r=a&&a.date?a.date:"2026-10-13",d=e.docTicker||"CELH",g=e.docEntry!==void 0&&e.docEntry!==null&&e.docEntry!==""?e.docEntry:i,c=e.docDays!==void 0&&e.docDays!==null&&e.docDays!==""?e.docDays:42,p=e.docLastResult?he(e.docLastResult,e):`<div style="color:var(--muted);">${o.emptyHint||"Enter US ticker, cost basis ($), and trading days held to evaluate asymmetric exit triggers against the latest closing price"} ($${i}).</div>`;return`
    <div style="background:#090d16; border:1px solid var(--border); border-top:2px solid var(--fin-up); border-radius:4px; padding:18px; display:flex; flex-direction:column; justify-content:space-between;">
      <div>
        <div style="font-size:0.7rem; font-family:var(--font-mono); font-weight:700; color:var(--fin-up); letter-spacing:0.05em; text-transform:uppercase;">
          ${t.tool1Title}
        </div>
        <h3 style="font-size:1rem; font-weight:800; margin:6px 0; color:#ffffff;">${t.tool1Sub}</h3>
        <p style="font-size:0.78rem; color:var(--muted); margin-bottom:14px; line-height:1.5;">${t.tool1Desc}</p>

        <div class="doctor-inputs-grid">
          <div>
            <label style="font-size:0.68rem; color:var(--muted); font-family:var(--font-mono); text-transform:uppercase;">${o.tickerLabel||"US Ticker"}</label>
            <input type="text" id="docTicker" value="${d}" placeholder="CELH" style="padding:7px 9px; background:#05080f; border:1px solid var(--border); color:#fff; border-radius:3px; font-family:var(--font-mono); font-weight:700; width:100%; margin-top:3px;" />
          </div>
          <div>
            <label style="font-size:0.68rem; color:var(--muted); font-family:var(--font-mono); text-transform:uppercase;">${o.entryLabel||"Cost Basis ($)"}</label>
            <input type="number" id="docEntry" step="0.01" value="${g}" placeholder="${i}" style="padding:7px 9px; background:#05080f; border:1px solid var(--border); color:#fff; border-radius:3px; font-family:var(--font-mono); width:100%; margin-top:3px;" />
          </div>
          <div>
            <label style="font-size:0.68rem; color:var(--muted); font-family:var(--font-mono); text-transform:uppercase;">${o.daysLabel||"Trading Days"}</label>
            <input type="number" id="docDays" value="${c}" placeholder="42" style="padding:7px 9px; background:#05080f; border:1px solid var(--border); color:#fff; border-radius:3px; font-family:var(--font-mono); width:100%; margin-top:3px;" />
          </div>
        </div>

        <div style="display:flex; gap:5px; flex-wrap:wrap; align-items:center; margin-bottom:12px;">
          <span style="font-size:0.68rem; color:var(--muted); font-family:var(--font-mono);">${o.presetsLabel||"LATEST CLOSE PRESETS"} (${r}):</span>
          ${["CELH","MBLY","APP","UPST","NVDA","CCL"].map(f=>{const l=n.find(h=>h.ticker===f),v=l?` $${Number(l.close).toFixed(2)}`:"";return`
                <button class="btn btn-sm btn-quick-doc mono" data-ticker="${f}" style="padding:2px 6px; font-size:0.68rem;">${f}${v}</button>
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
  `}function he(e,t=null){var w;const o=((w=t==null?void 0:t.t)==null?void 0:w.doctor)||{};let n="var(--fin-up)",a="var(--fin-up)";e.status_code==="CRITICAL_STOP"||e.status_code==="HARD_STOP"||e.is_critical?(n="var(--fin-down)",a="var(--fin-down)"):e.status_code==="DEAD_MONEY"||e.status_code==="TIME_STOP"?(n="var(--fin-amber)",a="var(--fin-amber)"):(e.status_code==="TP1_REACHED"||e.status_code==="TP1_HARVEST")&&(n="var(--fin-up)",a="var(--fin-up)");const i=String(e.status_label||e.status_code||"ACTIVE_HOLD").replace(/^[🟢🚨🛑⏳🎯⏰🏆\s]+/,""),r=Number(e.return_pct??0),d=`${r>=0?"+":""}${r.toFixed(2)}%`,g=e.entry_price??(t==null?void 0:t.docEntry),c=g!=null&&Number(g)>0?Number(g):27.93,p=((t==null?void 0:t.stocks)||[]).find(A=>A.ticker===(e.ticker||"CELH")),f=e.current_price??(p==null?void 0:p.close),l=f!=null&&Number(f)>0?Number(f):Number((c*(1+r/100)).toFixed(2)),v=e.stop_price!==void 0&&e.stop_price!==null&&Number(e.stop_price)>0?Number(e.stop_price):c*.91,h=e.tp1_price!==void 0&&e.tp1_price!==null&&Number(e.tp1_price)>0?Number(e.tp1_price):c*2,E=`$${v.toFixed(2)}`,k=`$${h.toFixed(2)}`,y=`$${l.toFixed(2)}`,$=`$${c.toFixed(2)}`,L=e.as_of_date||(p==null?void 0:p.date)||"2026-10-13";return`
    <div style="border-left: 3px solid ${a}; padding-left: 10px;">
      <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:6px;">
        <span class="mono" style="font-weight:800; font-size:0.84rem; color:${n};">
          ${i}
        </span>
        <span class="mono" style="font-weight:800; color:${r>=0?"var(--fin-up)":"var(--fin-down)"}; font-size:0.86rem;">
          P&L: ${d}
        </span>
      </div>
      <div class="mono" style="font-size:0.73rem; color:#93c5fd; margin-bottom:4px;">
        $${e.ticker||"CELH"} ${o.latestClose||"Latest Close"} (${L}): <b style="color:#fff;">${y}</b> · ${o.costBasis||"Cost Basis"}: <b style="color:#fff;">${$}</b>
      </div>
      <div style="font-weight:700; color:#ffffff; font-size:0.78rem; margin-bottom:4px;">
        ${o.ruleTriggered||"Rule Triggered"}: ${e.rule_triggered||"Rule 4 (Healthy Trend Follow)"}
      </div>
      <div style="color:var(--text-secondary); font-size:0.78rem; line-height:1.45; margin-bottom:8px;">
        <b>${o.directive||"Execution Directive"}:</b> ${e.action_plan||""}
      </div>
      <div class="mono" style="display:flex; gap:14px; font-size:0.72rem; color:var(--muted); border-top:1px solid var(--border); padding-top:6px;">
        <span>${o.hardStop||"Hard Stop (-9%)"}: <b style="color:var(--fin-down);">${E}</b></span>
        <span>${o.tp1Target||"TP1 Target (2x)"}: <b style="color:var(--fin-up);">${k}</b></span>
      </div>
      <button type="button" class="btn btn-sm" id="btnSendDoctorTelegram" style="margin-top:10px; border-color:rgba(96,165,250,0.4); color:#93c5fd;">📲 Send Diagnosis to Telegram</button>
    </div>
  `}function gt(e){const t=e.t,o=e.isProUnlocked,n=e.stocks||[],a=n.find(R=>R.ticker==="CELH"),i=n.find(R=>R.ticker==="MBLY"),r=a?Number(a.close).toFixed(2):"27.93",d=a&&a.ma20_price?Number(a.ma20_price).toFixed(2):"27.93",g=a&&a.ma60_price?Number(a.ma60_price).toFixed(2):"29.12",c=a&&a.tp1_2x_price?Number(a.tp1_2x_price).toFixed(2):(Number(r)*2).toFixed(2),p=a&&a.stop_loss_price?Number(a.stop_loss_price).toFixed(2):(Number(r)*.91).toFixed(2),f=a?Number(a.score):85,l=i,v=i?Number(i.close).toFixed(2):"7.02",h=i?Number(i.low52).toFixed(2):"6.47",E=i&&i.ma60_price?Number(i.ma60_price).toFixed(2):"8.17",k=i&&i.tp1_2x_price?Number(i.tp1_2x_price).toFixed(2):(Number(v)*2).toFixed(2),y=i?Number(i.score):62,$=(l==null?void 0:l.zone_code)==="LEFT_SIDE_KNIFE"?"badge-knife":(l==null?void 0:l.zone_code)==="IGNITION_ZONE"?"badge-ignition":"badge-watch",L=e.lang==="jp"?l==null?void 0:l.zone_label_jp:e.lang==="kr"?l==null?void 0:l.zone_label_kr:l==null?void 0:l.zone_label_en,w=String(L||((l==null?void 0:l.zone_code)==="LEFT_SIDE_KNIFE"?"LEFT-SIDE KNIFE":"WASHOUT WATCH")).replace(/^[🟢🟡🔴⚠️\s]+/,""),A=e.pineCode||`//@version=5
// RightSideAlpha PW-RSI Ignition Engine (ddHigh <= -20, proxLow <= 45, volRatio >= 1.30)
indicator("RightSideAlpha PW-RSI Ignition v2.6", overlay=true)
ma20 = ta.sma(close, 20)
ma60 = ta.sma(close, 60)
low52 = ta.lowest(low, 252)
high52 = ta.highest(high, 252)
volRatio = volume / ta.sma(volume, 20)
washout10d = ta.highest(volRatio, 10) >= 1.30
proxLow = (close - low52) / low52 * 100
ddHigh = (close - high52) / high52 * 100
ignition = ddHigh <= -20 and proxLow >= 10 and proxLow <= 45 and close > ma20 and close > ma60 and washout10d
plot(ma20, "MA20", color=color.new(color.aqua, 0), linewidth=2)
plot(ma60, "MA60 Trigger", color=color.new(color.orange, 0), linewidth=2)
plotshape(ignition and not ignition[1], "PW-RSI IGNITION", shape.labelup, location.belowbar, color.green, text="🟢 IGNITION", textcolor=color.white)`;return`
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

      <div id="vaultContentWrap" class="${o?"":"blur-locked"}" style="display:grid; grid-template-columns:repeat(auto-fit, minmax(min(100%, 320px), 1fr)); gap:16px;">
        <!-- Module 01: Position Doctor -->
        ${ut(e)}

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
                <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:4px;">
                  <b class="mono" style="color:#ffffff;">CELH · Celsius Holdings ($${r})</b>
                  <span class="badge badge-ignition">SCORE ${f}</span>
                </div>
                <div style="color:var(--muted); font-size:0.76rem; margin-top:4px; line-height:1.45;">
                  PepsiCo North America inventory destocking complete; 2026E operating leverage +257%. Latest Close <b class="mono" style="color:#fff;">$${r}</b> reclaiming MA20 ($${d}) toward MA60 ($${g}). Stop: $${p} · TP1 (2x): <b class="mono" style="color:var(--fin-up);">$${c}</b>.
                </div>
                <button class="btn btn-sm btn-open-research" data-ticker="CELH" style="margin-top:6px;">
                  Read $CELH SEC Research Brief ↗
                </button>
              </div>

              <div style="border-left:3px solid var(--fin-blue); padding-left:10px;">
                <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:4px;">
                  <b class="mono" style="color:#ffffff;">MBLY · Mobileye Global ($${v})</b>
                  <span class="badge ${$}">${w} · SCORE ${y}</span>
                </div>
                <div style="color:var(--muted); font-size:0.76rem; margin-top:4px; line-height:1.45;">
                  Tier-1 OEM ADAS inventory digestion completed; EyeQ6 design wins drive operating income inflection (-$0.39B → +$0.45B). Latest Close <b class="mono" style="color:#fff;">$${v}</b> · 52W Low $${h} · MA60 Trigger <b class="mono" style="color:#60a5fa;">$${E}</b> · TP1: <b class="mono" style="color:var(--fin-up);">$${k}</b>.
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

            <pre id="pineCodeBox" style="background:#05080f; padding:12px; border-radius:4px; font-size:0.7rem; color:#93c5fd; overflow-x:auto; max-height:155px; font-family:var(--font-mono); border:1px solid var(--border); line-height:1.45;">${A}</pre>
          </div>

          <div style="margin-top:12px;">
            <button class="btn btn-purple" id="btnCopyPineScript" style="width:100%; justify-content:center; padding:9px;">
              ${t.tool3CopyBtn}
            </button>
          </div>
        </div>
      </div>
    </section>
  `}const Be=e=>e?e.includes("?")?e.includes("embed=1")?e:`${e}&embed=1`:`${e}?embed=1`:"#";function ft(e){var i;const t=e.config||{},o=((i=e.t)==null?void 0:i.pricing)||{},n=t.ls_site1_monthly_url||"https://rightsidealpha.lemonsqueezy.com/checkout/buy/pro-monthly",a=t.ls_site1_ltd_url||"https://rightsidealpha.lemonsqueezy.com/checkout/buy/lifetime-pass";return`
    <section class="pricing-grid" id="pricingSection">
      <!-- Tier 1: Pro Monthly -->
      <div class="price-card featured">
        <div>
          <span class="badge badge-ignition">${o.t1Badge||"INSTITUTIONAL PRO"}</span>
          <h3 style="font-size:1.12rem; font-weight:800; margin-top:10px; color:#ffffff;">
            ${o.t1Title||"Pro Quantitative Terminal & Daily SEC Brief"}
          </h3>
          <div class="price-num">$29 <span style="font-size:0.82rem; color:var(--muted); font-family:var(--font-sans); font-weight:500;">${o.t1Period||"/ month"}</span></div>
          <ul class="price-list">
            <li><span>—</span> <span>${o.t1Feat1||"Unmask all 72 US Equity PW-RSI Scores, MA20/60 Breakout Triggers & -9% Stop Levels"}</span></li>
            <li><span>—</span> <span>${o.t1Feat2||"Daily 08:10 EST Primary-Filing (10-K/10-Q/8-K) Turnaround Research Digest"}</span></li>
            <li><span>—</span> <span>${o.t1Feat3||"Position Risk & 55-Day Time-Stop Diagnostic Engine"}</span></li>
            <li><span>—</span> <span>${o.t1Feat4||"Full TradingView Pine Script v5 Indicator Source Code + SemiFearGreed 26Y CSV"}</span></li>
          </ul>
        </div>
        <a class="btn btn-primary lemonsqueezy-button" id="cardMonthlyBtn" data-plan="monthly" href="${Be(n)}" style="justify-content:center; padding:10px;">
          ${o.t1Btn||"Subscribe via Lemon Squeezy ($29/mo)"}
        </a>
      </div>

      <!-- Tier 2: Lifetime Pass -->
      <div class="price-card">
        <div>
          <span class="badge badge-watch">${o.t2Badge||"FOUNDER ALLOCATION"}</span>
          <h3 style="font-size:1.12rem; font-weight:800; margin-top:10px; color:#ffffff;">
            ${o.t2Title||"Lifetime Research & Terminal License"}
          </h3>
          <div class="price-num">$199 <span style="font-size:0.82rem; color:var(--muted); font-family:var(--font-sans); font-weight:500;">${o.t2Period||"/ one-time"}</span></div>
          <ul class="price-list">
            <li><span>—</span> <span>${o.t2Feat1||"Permanent License Key — Zero recurring monthly subscription charges"}</span></li>
            <li><span>—</span> <span>${o.t2Feat2||"Complete 26.8-Year (2000–2026) US Equity & Semiconductor ETF Backtest Datasets"}</span></li>
            <li><span>—</span> <span>${o.t2Feat3||"Multilingual Access (English, Japanese & Korean SEC Research Briefs)"}</span></li>
            <li><span>—</span> <span>${o.t2Feat4||"Full Access to both RightSideAlpha and SemiFearGreed Pro Features"}</span></li>
          </ul>
        </div>
        <a class="btn btn-emerald lemonsqueezy-button" id="cardLtdBtn" data-plan="lifetime" href="${Be(a)}" style="justify-content:center; padding:10px;">
          ${o.t2Btn||"Acquire Lifetime License ($199)"}
        </a>
      </div>

      <!-- Tier 3: Institutional Charting & Fundamental Partners -->
      <div class="price-card">
        <div>
          <span class="badge" style="background:rgba(41,98,255,0.14); color:#93c5fd; border:1px solid rgba(41,98,255,0.3);">${o.t3Badge||"EXECUTION & DATA PARTNERS"}</span>
          <h3 style="font-size:1.12rem; font-weight:800; margin-top:10px; color:#ffffff;">
            ${o.t3Title||"Direct Charting & Consensus EPS Verification"}
          </h3>
          <p style="color:var(--muted); font-size:0.8rem; margin-top:8px; line-height:1.5;">
            ${o.t3Desc||"Verify MA20/MA60 volume breakouts and forward EPS revisions on institutional charting and consensus platforms:"}
          </p>
          <ul class="price-list">
            <li><span>—</span> <span><b>TradingView Pro</b> — Multi-timeframe MA20/MA60 & Pine Script v5 execution</span></li>
            <li><span>—</span> <span><b>Seeking Alpha Premium</b> — Quant Grades & 1-2Y consensus EPS revision tracking</span></li>
            <li><span>—</span> <span><b>Interactive Brokers (IBKR)</b> — Direct NYSE/NASDAQ routing & institutional FX rates</span></li>
          </ul>
        </div>
        <div style="display:flex; flex-direction:column; gap:8px;">
          <a class="btn" id="affTvBtn" href="/api/referral/redirect/tradingview?ticker=SPY" target="_blank" rel="noopener noreferrer" style="justify-content:center;">
            ${o.t3TvBtn||"Launch TradingView Terminal ↗"}
          </a>
          <a class="btn" id="affSaBtn" href="/api/referral/redirect/seekingalpha?ticker=SPY" target="_blank" rel="noopener noreferrer" style="justify-content:center;">
            ${o.t3SaBtn||"Open Seeking Alpha EPS Consensus ↗"}
          </a>
        </div>
      </div>
    </section>
  `}function bt(e){var z,H;const t=e.config||{},o=((z=e.t)==null?void 0:z.modal)||{},n=((H=e.t)==null?void 0:H.telegram)||{},a=e.telegramStatus||{},i=!!e.isProUnlocked,r=e.selectedCheckoutPlan||"monthly",d=r==="lifetime"?"$199 Lifetime License (One-Time)":"$29/mo Pro Quantitative Terminal",g=r==="lifetime"?t.ls_site1_ltd_url||"https://rightsidealpha.lemonsqueezy.com/checkout/buy/lifetime-pass":t.ls_site1_monthly_url||"https://rightsidealpha.lemonsqueezy.com/checkout/buy/pro-monthly",c=!!(a.configured||(t.tg_bot_token||a.has_bot_token)&&(t.tg_chat_id||a.chat_id||a.has_chat_id)),p=t.tg_channel_url||a.channel_url||"https://t.me/RigjtsideAlphabot",f=t.tg_bot_token||a.bot_token_masked||"924555...d6gU",l=t.tg_chat_id||a.chat_id||"",v=(t.tg_auto_ignition??a.auto_alert_ignition??!0)!==!1,h=(t.tg_auto_stop??a.auto_alert_stop??!0)!==!1,E=(t.tg_auto_semi??a.auto_alert_semi_regime??!0)!==!1,k=(e.stocks||[]).find(Z=>Z.ticker==="CELH")||(e.stocks||[])[0]||{},y=k.ticker||"CELH",$=Number(k.close??27.93).toFixed(2),L=Number(k.entry_trigger_price??29.12).toFixed(2),w=Number(k.stop_loss_price??25.42).toFixed(2),A=Number(k.tp1_2x_price??55.86).toFixed(2),R=e.semiOverview||{},F=Number(R.fg_score??18).toFixed(1),N=Number(R.smh_close??541.62).toFixed(2),O=Number(R.xlv_close??179.28).toFixed(2),j=e.telegramLastPreview||["🟢 RightSideAlpha × SemiFearGreed — Quant Signal Preview",`• Top Ignition: $${y} | Close $${$} | TRG $${L} | STP (-9%) $${w} | TP1 (2x) $${A}`,`• SemiFearGreed: ${F}/100 (EXTREME FEAR) → 80% $SMH ($${N}) : 20% $XLV ($${O})`,"• Click any button above to dispatch live to Telegram or generate a full preview."].join(`
`);return`
    <!-- LICENSE ACTIVATION MODAL -->
    <div class="modal-backdrop" id="licenseModal">
      <div class="modal">
        <div style="font-size:0.68rem; font-family:var(--font-mono); color:#93c5fd; text-transform:uppercase; letter-spacing:0.05em;">
          ${o.licenseTag||"AUTHENTICATION · LEMON SQUEEZY MERCHANT OF RECORD"}
        </div>
        <h3 style="font-size:1.12rem; font-weight:800; margin-top:4px; color:#ffffff;">
          ${o.licenseTitle||"Activate Pro Terminal License"}
        </h3>
        <p style="color:var(--muted); font-size:0.82rem; margin-top:6px; line-height:1.5;">
          ${o.licenseDesc||"Enter the license key issued upon Lemon Squeezy checkout to unlock all 72 US equity target levels, Position Risk Diagnostics, and the 26-year Semiconductor CSV dataset."}<br/>
          <span style="color:var(--text-secondary);">${o.evalKeyLabel||"Evaluation Key"}: <code class="mono" style="color:var(--fin-up); font-weight:700;">PRO-DEMO-2026</code></span>
        </p>

        <div id="checkoutPlanCallout" style="margin-top:10px; margin-bottom:10px; padding:10px 12px; background:#090d16; border:1px solid var(--border); border-left:3px solid var(--fin-blue); border-radius:4px; font-size:0.78rem;">
          <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:6px;">
            <span>Selected Tier: <b id="selectedPlanLabel" style="color:#ffffff;">${d}</b></span>
            <a id="externalCheckoutLink" href="${g}" target="_blank" rel="noopener noreferrer" class="mono" style="color:#60a5fa; font-size:0.72rem; text-decoration:underline;">
              Open External Lemon Squeezy Checkout ↗
            </a>
          </div>
        </div>

        <div style="margin-bottom:8px;">
          <button type="button" class="btn btn-emerald btn-sm" id="btnFillDemoKey" style="width:100%; justify-content:center; padding:7px 10px;">
            ⚡ ${o.applyDemoBtn||"Apply Evaluation Key (PRO-DEMO-2026)"}
          </button>
        </div>

        <input type="text" id="licenseInput" value="${e.licenseKey||""}" placeholder="PRO-DEMO-2026 or RSA-PRO-2026-LIVE" autocomplete="off" />
        <div id="licenseMsg" style="font-size:0.8rem; margin-bottom:12px; min-height:1.2em;"></div>
        <div style="display:flex; gap:8px; justify-content:space-between; align-items:center; flex-wrap:wrap;">
          <div>
            ${i?`<button type="button" class="btn btn-sm" id="btnDeactivateLicense" style="border-color:var(--fin-down); color:#f87171;">
                     ${o.deactivateBtn||"Deactivate / Lock Pro License"}
                   </button>`:""}
          </div>
          <div style="display:flex; gap:8px;">
            <button type="button" class="btn" id="btnCancelLicense">${o.cancelBtn||"Cancel"}</button>
            <button type="button" class="btn btn-primary" id="btnVerifyLicense">${o.verifyBtn||"Verify & Unlock Terminal"}</button>
          </div>
        </div>
      </div>
    </div>

    <!-- TERMINAL & AFFILIATE CONFIG MODAL -->
    <div class="modal-backdrop" id="configModal">
      <div class="modal">
        <div style="font-size:0.68rem; font-family:var(--font-mono); color:#93c5fd; text-transform:uppercase; letter-spacing:0.05em;">
          ${o.configTag||"ADMINISTRATION · MONETIZATION & PARTNER ROUTING"}
        </div>
        <h3 style="font-size:1.12rem; font-weight:800; margin-top:4px; color:#ffffff;">
          ${o.configTitle||"Checkout & Affiliate Parameter Configuration"}
        </h3>
        <p style="color:var(--muted); font-size:0.8rem; margin-top:4px; margin-bottom:12px;">
          ${o.configDesc||"Update Lemon Squeezy checkout endpoints and affiliate attribution identifiers. Changes persist to the backend and browser storage."}
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
          <button type="button" class="btn" id="btnCancelConfig">${o.closeBtn||"Close"}</button>
          <button type="button" class="btn btn-primary" id="btnSaveConfig">${o.saveBtn||"Save Configuration"}</button>
        </div>
      </div>
    </div>

    <!-- INSTITUTIONAL RESEARCH BRIEF MODAL -->
    <div class="modal-backdrop" id="researchModal">
      <div class="modal" style="max-width:760px;">
        <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:8px; margin-bottom:12px;">
          <h3 style="font-size:1.05rem; font-weight:800; color:#ffffff;" id="researchModalTitle">
            ${o.researchTitle||"SEC Primary Filing Turnaround Brief"}
          </h3>
          <div style="display:flex; gap:6px; align-items:center; flex-wrap:wrap;">
            <button type="button" class="btn btn-sm btn-switch-research" data-ticker="CELH" id="btnSwitchResearchCelh">$CELH Brief</button>
            <button type="button" class="btn btn-sm btn-switch-research" data-ticker="MBLY" id="btnSwitchResearchMbly">$MBLY Brief</button>
            <button type="button" class="btn btn-sm" id="btnCloseResearch">${o.closeBtn||"Close"} ✕</button>
          </div>
        </div>
        <div id="researchModalBody" style="font-size:0.84rem; color:var(--text); line-height:1.65; max-height:62vh; overflow-y:auto; background:#05080f; padding:18px; border-radius:4px; border:1px solid var(--border);">
          ${o.researchLoading||"Loading institutional brief..."}
        </div>
      </div>
    </div>

    <!-- TELEGRAM QUANT ALERT & MORNING BRIEF DISPATCH MODAL -->
    <div class="modal-backdrop" id="telegramModal">
      <div class="modal" style="max-width:660px; max-height:92vh; overflow-y:auto;">
        <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:8px;">
          <div style="font-size:0.68rem; font-family:var(--font-mono); color:#93c5fd; text-transform:uppercase; letter-spacing:0.05em;">
            ${n.tag||"REAL-TIME QUANT DISPATCH · TELEGRAM BOT & CHANNEL INTEGRATION"}
          </div>
          <div style="display:flex; align-items:center; gap:8px; flex-wrap:wrap;">
            <span
              id="tgModalStatusBadge"
              class="badge ${c?"badge-ignition":"badge-watch"}"
            >
              ${c?n.statusConnected||"CONNECTED ✓":n.statusPreview||"PREVIEW / SETUP MODE"}
            </span>
            <a
              id="tgChannelLink"
              href="${p}"
              target="_blank"
              rel="noopener noreferrer"
              class="mono"
              style="font-size:0.72rem; color:#60a5fa; text-decoration:underline;"
            >
              ${n.openChannelBtn||"Open Telegram Bot / Channel ↗"}
            </a>
          </div>
        </div>

        <h3 style="font-size:1.12rem; font-weight:800; margin-top:6px; color:#ffffff;">
          📲 ${n.title||"Telegram Quant Signal & Morning Brief Dispatch"}
        </h3>
        <p style="color:var(--muted); font-size:0.8rem; margin-top:4px; line-height:1.45;">
          ${n.desc||"Receive real-time Right-Side Ignition breakouts, Position Doctor -9% / 55D stop alerts, and Semiconductor Fear & Greed 80:20 contrarian signals directly on Telegram."}
        </p>

        <!-- Step-by-step Quick Setup Guide -->
        <div style="margin:10px 0 12px; padding:10px 12px; background:#090d16; border:1px solid var(--border); border-left:3px solid #60a5fa; border-radius:4px; font-size:0.74rem; color:var(--text-secondary); display:grid; grid-template-columns:repeat(auto-fit, minmax(180px, 1fr)); gap:6px;">
          <div><b style="color:#93c5fd;">${n.step1||"1. Create bot via @BotFather -> Paste Token"}</b></div>
          <div><b style="color:#93c5fd;">${n.step2||"2. Send /start to your bot -> Click 'Auto-Detect Chat ID'"}</b></div>
          <div><b style="color:#93c5fd;">${n.step3||"3. Click 'Save & Send Test Ping'"}</b></div>
        </div>

        <div style="display:grid; grid-template-columns:repeat(auto-fit, minmax(240px, 1fr)); gap:10px;">
          <div>
            <label style="font-size:0.68rem; color:var(--muted); font-family:var(--font-mono);">
              ${n.botTokenLabel||"TELEGRAM BOT TOKEN (@BotFather)"}
            </label>
            <input
              type="password"
              id="tgBotTokenInput"
              value="${f}"
              placeholder="1234567890:AAH..."
              autocomplete="off"
              style="margin:4px 0 8px;"
            />
          </div>
          <div>
            <label style="font-size:0.68rem; color:var(--muted); font-family:var(--font-mono);">
              ${n.chatIdLabel||"TELEGRAM CHAT ID OR @CHANNEL"}
            </label>
            <div style="display:flex; gap:6px; align-items:center; margin:4px 0 8px;">
              <input
                type="text"
                id="tgChatIdInput"
                value="${l}"
                placeholder="e.g. 123456789 or @channel"
                autocomplete="off"
                style="margin:0; flex:1;"
              />
              <button type="button" class="btn btn-sm" id="btnDetectTgChatId" style="white-space:nowrap; padding:8px 10px; border-color:rgba(96,165,250,0.45); color:#93c5fd;">
                ${n.detectChatIdBtn||"🔍 Auto-Detect Chat ID"}
              </button>
            </div>
          </div>
        </div>

        <label style="font-size:0.68rem; color:var(--muted); font-family:var(--font-mono);">
          ${n.channelUrlLabel||"TELEGRAM CHANNEL / BOT LINK URL"}
        </label>
        <input
          type="text"
          id="tgChannelUrlInput"
          value="${p}"
          placeholder="https://t.me/RightSideAlphaBot"
          style="margin:4px 0 10px;"
        />

        <!-- Checkboxes for Auto-Alerts -->
        <div style="margin-bottom:12px; padding:10px 12px; background:#080c15; border:1px solid var(--border); border-radius:4px;">
          <div style="font-size:0.68rem; font-family:var(--font-mono); color:var(--muted); margin-bottom:6px; text-transform:uppercase;">
            ${n.autoAlertsLabel||"AUTOMATED SIGNAL SUBSCRIPTIONS"}
          </div>
          <div style="display:flex; flex-direction:column; gap:6px; font-size:0.78rem; color:var(--text-secondary);">
            <label style="display:flex; align-items:center; gap:8px; cursor:pointer;">
              <input type="checkbox" id="tgAutoIgnition" ${v?"checked":""} style="width:15px; height:15px; margin:0; padding:0; accent-color:var(--fin-up);" />
              <span>${n.chkIgnition||"Right-Side 4-Factor Ignition Breakout Alerts"}</span>
            </label>
            <label style="display:flex; align-items:center; gap:8px; cursor:pointer;">
              <input type="checkbox" id="tgAutoStop" ${h?"checked":""} style="width:15px; height:15px; margin:0; padding:0; accent-color:var(--fin-up);" />
              <span>${n.chkStop||"Position Doctor -9% Hard Stop & 55D Time-Stop Alerts"}</span>
            </label>
            <label style="display:flex; align-items:center; gap:8px; cursor:pointer;">
              <input type="checkbox" id="tgAutoSemi" ${E?"checked":""} style="width:15px; height:15px; margin:0; padding:0; accent-color:var(--fin-up);" />
              <span>${n.chkSemi||"Semiconductor Fear & Greed Extreme Regime (<25 / >75) Alerts"}</span>
            </label>
          </div>
        </div>

        <!-- Instant Dispatch Action Bar (4 buttons) -->
        <div style="margin-bottom:10px;">
          <div style="font-size:0.68rem; font-family:var(--font-mono); color:var(--muted); margin-bottom:6px; text-transform:uppercase;">
            ${n.dispatchBarLabel||"INSTANT 1-CLICK SIGNAL DISPATCH & PREVIEW"}
          </div>
          <div style="display:grid; grid-template-columns:repeat(auto-fit, minmax(140px, 1fr)); gap:6px;">
            <button type="button" class="btn btn-sm" id="btnTgSendTest" style="justify-content:center; padding:7px 8px; border-color:rgba(16,185,129,0.45); color:#34d399;">
              🚀 Test Ping
            </button>
            <button type="button" class="btn btn-sm" id="btnTgSendIgnition" style="justify-content:center; padding:7px 8px; border-color:rgba(96,165,250,0.45); color:#93c5fd;">
              📊 Ignition Top 5
            </button>
            <button type="button" class="btn btn-sm" id="btnTgSendSemi" style="justify-content:center; padding:7px 8px; border-color:rgba(248,113,113,0.45); color:#fca5a5;">
              🧭 Semi 80:20 Signal
            </button>
            <button type="button" class="btn btn-sm" id="btnTgSendFull" style="justify-content:center; padding:7px 8px; border-color:rgba(251,191,36,0.45); color:#fde68a;">
              📑 Full Morning Brief
            </button>
          </div>
        </div>

        <div id="tgModalMsg" style="font-size:0.78rem; margin-bottom:8px; min-height:1.2em; color:#93c5fd;"></div>

        <div style="margin-bottom:14px;">
          <div style="font-size:0.66rem; font-family:var(--font-mono); color:var(--muted); margin-bottom:4px; text-transform:uppercase;">
            ${n.previewLabel||"LIVE TELEGRAM MESSAGE PREVIEW"}
          </div>
          <pre
            id="tgPreviewBox"
            class="mono"
            style="background:#05080f; border:1px solid var(--border); border-left:3px solid var(--fin-up); border-radius:4px; padding:10px 12px; font-size:0.73rem; color:var(--text-secondary); white-space:pre-wrap; word-break:break-word; max-height:175px; overflow-y:auto; line-height:1.45;"
          >${j}</pre>
        </div>

        <div style="display:flex; gap:8px; justify-content:flex-end; align-items:center;">
          <button type="button" class="btn" id="btnCloseTelegram">${n.closeBtn||o.closeBtn||"Close"}</button>
          <button type="button" class="btn btn-primary" id="btnSaveTelegram">${n.saveBtn||"Save Telegram Settings"}</button>
        </div>
      </div>
    </div>

    <!-- TOAST NOTIFICATION -->
    <div class="toast" id="toastBox">Action completed</div>
  `}function q(e,t,o,n){const a=n*Math.PI/180;return{x:e+o*Math.cos(a),y:t-o*Math.sin(a)}}function _t(e,t,o,n,a){const i=q(e,t,o,n),r=q(e,t,o,a),d=Math.abs(n-a)<=180?"0":"1";return`M ${i.x.toFixed(2)} ${i.y.toFixed(2)} A ${o} ${o} 0 ${d} 1 ${r.x.toFixed(2)} ${r.y.toFixed(2)}`}function ht(e,t){const o=Math.max(0,Math.min(100,Number(e||18))),n=230,a=200,i=146,r=[{code:"EXTREME_FEAR",min:0,max:24,a1:180,a2:136.5,activeColor:"#d92d20",mutedColor:"#fecaca",label:"EXTREME FEAR",midAngle:158},{code:"FEAR",min:25,max:44,a1:134,a2:100.5,activeColor:"#f79009",mutedColor:"#fed7aa",label:"FEAR",midAngle:117},{code:"NEUTRAL",min:45,max:55,a1:98,a2:82,activeColor:"#667085",mutedColor:"#e5e7eb",label:"NEUTRAL",midAngle:90},{code:"GREED",min:56,max:74,a1:79.5,a2:46,activeColor:"#12b76a",mutedColor:"#bbf7d0",label:"GREED",midAngle:63},{code:"EXTREME_GREED",min:75,max:100,a1:43.5,a2:0,activeColor:"#027a48",mutedColor:"#a7f3d0",label:"EXTREME GREED",midAngle:22}];let d=r[0];o>=75?d=r[4]:o>=55.01?d=r[3]:o>=45?d=r[2]:o>=25&&(d=r[1]);const g=r.map(h=>{const E=h.code===d.code,k=_t(n,a,i,h.a1,h.a2),y=E?h.activeColor:h.mutedColor,$=E?40:32,L=q(n,a,i+31,h.midAngle);return`
        <path d="${k}" fill="none" stroke="${y}" stroke-width="${$}" stroke-linecap="butt" />
        <text x="${L.x.toFixed(1)}" y="${L.y.toFixed(1)}" text-anchor="middle" dominant-baseline="middle"
              fill="${E?h.activeColor:"#6b7280"}"
              font-size="${E?"9.5":"8.5"}" font-weight="${E?"800":"700"}" font-family="Inter, sans-serif">
          ${h.label}
        </text>
      `}).join(""),c=[0,25,45,55,75,100].map(h=>{const E=180-h/100*180,k=q(n,a,i-24,E),y=q(n,a,i-35,E);return`
        <circle cx="${k.x.toFixed(1)}" cy="${k.y.toFixed(1)}" r="1.8" fill="#6b7280" />
        <text x="${y.x.toFixed(1)}" y="${y.y.toFixed(1)}" text-anchor="middle" dominant-baseline="middle"
              fill="#4b5563" font-size="10" font-weight="700" font-family="JetBrains Mono, monospace">
          ${h}
        </text>
      `}).join(""),p=180-o/100*180,f=q(n,a,i-12,p),l=q(n,a,8,p+90),v=q(n,a,8,p-90);return`
    <div style="display:flex; flex-direction:column; align-items:center;">
      <svg viewBox="0 0 460 250" style="width:100%; max-width:440px; height:auto; overflow:visible;">
        ${g}
        ${c}
        <!-- Needle Polygon -->
        <polygon points="${f.x.toFixed(1)},${f.y.toFixed(1)} ${l.x.toFixed(1)},${l.y.toFixed(1)} ${v.x.toFixed(1)},${v.y.toFixed(1)}"
                 fill="#111827" />
        <circle cx="${n}" cy="${a}" r="14" fill="#111827" />
        <circle cx="${n}" cy="${a}" r="5" fill="#ffffff" />
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
          <span class="cnn-pill cnn-pill-${d.code}" style="margin-left:6px; font-size:0.85rem;">
            ${t||d.label}
          </span>
        </div>
      </div>
    </div>
  `}function yt(e,t){const o=e&&e.series||[];if(!o.length)return'<div style="padding:40px; text-align:center; color:#6b7280;">Loading historical timeline...</div>';const n=640,a=230,i=36,r=16,d=16,g=28,c=n-i-r,p=a-d-g,f=o.map(($,L)=>{const w=i+L/Math.max(1,o.length-1)*c,A=d+(1-Math.max(0,Math.min(100,$.fg_score))/100)*p;return`${w.toFixed(1)},${A.toFixed(1)}`}),l=(d+.75*p).toFixed(1),v=(d+.5*p).toFixed(1),h=(d+.25*p).toFixed(1),E=o[0].date,k=o[Math.floor(o.length/2)].date,y=o[o.length-1].date;return`
    <div>
      <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:10px; flex-wrap:wrap; gap:8px;">
        <div style="font-size:0.8rem; font-weight:700; color:#374151;">
          Historical Semiconductor Fear & Greed Index (${E} → ${y})
        </div>
        <div style="display:flex; gap:4px; flex-wrap:wrap;">
          ${["3M","6M","1Y","3Y","5Y","10Y","ALL"].map($=>`
            <button class="btn-semi-range" data-range="${$}"
                    style="padding:3px 9px; border-radius:4px; font-size:0.72rem; font-weight:700; cursor:pointer; border:1px solid ${t===$?"#111827":"#d1d5db"}; background:${t===$?"#111827":"#ffffff"}; color:${t===$?"#ffffff":"#374151"};">
              ${$}
            </button>
          `).join("")}
        </div>
      </div>

      <svg viewBox="0 0 ${n} ${a}" style="width:100%; height:auto; background:#f9fafb; border:1px solid #e5e7eb; border-radius:4px;">
        <!-- Extreme Greed Band (>75) -->
        <rect x="${i}" y="${d}" width="${c}" height="${.25*p}" fill="rgba(16,185,129,0.08)" />
        <!-- Extreme Fear Band (<25) -->
        <rect x="${i}" y="${l}" width="${c}" height="${.25*p}" fill="rgba(239,68,68,0.09)" />

        <!-- Reference Lines -->
        <line x1="${i}" y1="${h}" x2="${n-r}" y2="${h}" stroke="#10b981" stroke-dasharray="3,3" stroke-width="1" />
        <line x1="${i}" y1="${v}" x2="${n-r}" y2="${v}" stroke="#9ca3af" stroke-dasharray="3,3" stroke-width="1" />
        <line x1="${i}" y1="${l}" x2="${n-r}" y2="${l}" stroke="#ef4444" stroke-dasharray="3,3" stroke-width="1" />

        <text x="6" y="${h}" fill="#047857" font-size="9.5" font-weight="700" dominant-baseline="middle">75</text>
        <text x="6" y="${v}" fill="#6b7280" font-size="9.5" font-weight="700" dominant-baseline="middle">50</text>
        <text x="6" y="${l}" fill="#b91c1c" font-size="9.5" font-weight="700" dominant-baseline="middle">25</text>

        <!-- FG Line -->
        <polyline fill="none" stroke="#111827" stroke-width="1.8" points="${f.join(" ")}" />

        <!-- X-Axis Dates -->
        <text x="${i}" y="${a-8}" fill="#6b7280" font-size="9.5" font-family="JetBrains Mono, monospace">${E}</text>
        <text x="${i+c/2}" y="${a-8}" fill="#6b7280" font-size="9.5" text-anchor="middle" font-family="JetBrains Mono, monospace">${k}</text>
        <text x="${n-r}" y="${a-8}" fill="#6b7280" font-size="9.5" text-anchor="end" font-family="JetBrains Mono, monospace">${y}</text>
      </svg>
    </div>
  `}function vt(e,t){if(!e||!e.length)return"";const o=180,n=44,a=e.map((d,g)=>{const c=4+g/Math.max(1,e.length-1)*(o-8),p=4+(1-Math.max(0,Math.min(100,d))/100)*(n-8);return`${c.toFixed(1)},${p.toFixed(1)}`}).join(" "),r={EXTREME_FEAR:"#dc2626",FEAR:"#ea580c",NEUTRAL:"#4b5563",GREED:"#16a34a",EXTREME_GREED:"#059669"}[t]||"#111827";return`
    <svg viewBox="0 0 ${o} ${n}" style="width:160px; height:40px; background:#f8fafc; border:1px solid #e2e8f0; border-radius:4px;">
      <line x1="0" y1="${n/2}" x2="${o}" y2="${n/2}" stroke="#e2e8f0" stroke-dasharray="2,2" stroke-width="1" />
      <polyline fill="none" stroke="${r}" stroke-width="1.8" points="${a}" />
    </svg>
  `}function St(e){const t=e&&e.series||[];if(!t.length)return"";const o=720,n=220,a=52,i=20,r=18,d=26,g=o-a-i,c=n-r-d,p=[];t.forEach($=>{p.push($.port73_norm,$.qqq_norm)});const f=Math.min(...p,8e3),l=Math.max(...p,12e3),v=Math.max(1,l-f),h=t.map(($,L)=>{const w=a+L/Math.max(1,t.length-1)*g,A=r+(1-($.port73_norm-f)/v)*c;return`${w.toFixed(1)},${A.toFixed(1)}`}).join(" "),E=t.map(($,L)=>{const w=a+L/Math.max(1,t.length-1)*g,A=r+(1-($.qqq_norm-f)/v)*c;return`${w.toFixed(1)},${A.toFixed(1)}`}).join(" "),k=t[t.length-1].port73_norm,y=t[t.length-1].qqq_norm;return`
    <div style="margin-bottom:16px;">
      <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:8px; flex-wrap:wrap; gap:8px; font-size:0.78rem;">
        <div style="display:flex; gap:16px; align-items:center;">
          <span style="display:inline-flex; align-items:center; gap:6px; color:#34d399; font-weight:700;">
            <span style="width:12px; height:3px; background:#0ecb81; display:inline-block;"></span>
            70% $SMH : 30% $XLV Barbell ($10k → $${k.toLocaleString()})
          </span>
          <span style="display:inline-flex; align-items:center; gap:6px; color:#94a3b8; font-weight:600;">
            <span style="width:12px; height:3px; background:#64748b; display:inline-block;"></span>
            100% $QQQ Benchmark ($10k → $${y.toLocaleString()})
          </span>
        </div>
        <span class="mono" style="color:var(--muted); font-size:0.72rem;">Selected Window: ${e.range_code}</span>
      </div>
      <svg viewBox="0 0 ${o} ${n}" style="width:100%; height:auto; background:#060911; border:1px solid var(--border); border-radius:4px;">
        <polyline fill="none" stroke="#64748b" stroke-width="1.6" stroke-dasharray="3,2" points="${E}" />
        <polyline fill="none" stroke="#0ecb81" stroke-width="2.2" points="${h}" />
        <text x="6" y="${r+8}" fill="#94a3b8" font-size="9.5" font-family="JetBrains Mono, monospace">$${Math.round(l).toLocaleString()}</text>
        <text x="6" y="${n-d}" fill="#94a3b8" font-size="9.5" font-family="JetBrains Mono, monospace">$${Math.round(f).toLocaleString()}</text>
      </svg>
    </div>
  `}function xt(e){const t=e.t,o=e.lang,n=e.semiOverview;if(!n)return`
      <div class="proof-card" style="padding:40px; text-align:center;">
        Loading Semiconductor Fear & Greed Index...
      </div>
    `;const a=o==="jp"?n.regime_jp:o==="kr"?n.regime_kr:n.regime_en,i=o==="jp"?n.action_headline_jp:o==="kr"?n.action_headline_kr:n.action_headline_en,r=o==="jp"?n.action_detail_jp:o==="kr"?n.action_detail_kr:n.action_detail_en,d=e.semiGaugeTab||"overview",g=e.semiRange||"1Y",c=e.semiRebalanceResult,p=e.semiLumpSumResult,f=e.semiHistory&&e.semiHistory.era_summary||[];return`
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
              <button class="cnn-view-tab ${d==="overview"?"active":""}" data-semi-tab="overview">
                ${t.cnnTabOverview}
              </button>
              <button class="cnn-view-tab ${d==="timeline"?"active":""}" data-semi-tab="timeline">
                ${t.cnnTabTimeline}
              </button>
            </div>
          </div>

          ${d==="overview"?ht(n.fg_score,a):yt(e.semiHistory,g)}
        </div>

        <!-- RIGHT COLUMN: CNN 4-ROW HISTORICAL STACK + BARBELL SIGNAL -->
        <div class="cnn-card" style="display:flex; flex-direction:column; justify-content:space-between;">
          <div>
            <div style="font-size:0.78rem; font-weight:800; text-transform:uppercase; letter-spacing:0.05em; color:#6b7280; margin-bottom:8px;">
              ${t.cnnHistoryTitle}
            </div>
            <div class="cnn-history-list">
              ${n.comparisons.map(l=>{const v=o==="jp"?l.label_jp:o==="kr"?l.label_kr:l.label_en,h=o==="jp"?l.regime_jp:o==="kr"?l.regime_kr:l.regime_en;return`
                  <div class="cnn-history-row">
                    <div>
                      <div class="cnn-hist-label">${v} <span class="mono" style="font-size:0.72rem; color:#9ca3af;">(${l.date})</span></div>
                      <div class="cnn-hist-regime">${h}</div>
                    </div>
                    <div class="cnn-score-circle">${Math.round(l.score)}</div>
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
              ${i}
            </div>
            <p style="font-size:0.78rem; color:#374151; margin-top:4px; line-height:1.45;">
              ${r}
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
          ${n.factors.map(l=>{const v=o==="jp"?l.title_jp:o==="kr"?l.title_kr:l.title_en,h=o==="jp"?l.subtitle_jp:o==="kr"?l.subtitle_kr:l.subtitle_en,E=o==="jp"?l.desc_jp:o==="kr"?l.desc_kr:l.desc_en,k=o==="jp"?l.regime_jp:o==="kr"?l.regime_kr:l.regime_en;return`
              <div class="cnn-indicator-item">
                <div>
                  <div style="display:flex; align-items:center; gap:8px;">
                    <span class="mono" style="font-size:0.7rem; font-weight:800; padding:2px 6px; background:#f3f4f6; border:1px solid #d1d5db; border-radius:3px; color:#374151;">
                      #${l.order} · ${l.weight_pct}% WEIGHT
                    </span>
                    <span class="cnn-ind-title">${v}</span>
                  </div>
                  <div class="cnn-ind-sub">${h}</div>
                  <p class="cnn-ind-desc">${E}</p>
                </div>

                <div style="display:flex; flex-direction:column; align-items:center; gap:6px;">
                  ${vt(l.sparkline,l.regime_code)}
                  <div class="mono" style="font-size:0.74rem; color:#374151; font-weight:700;">
                    Reading: ${l.raw_display} · Score ${l.score.toFixed(1)}/100
                  </div>
                </div>

                <div style="text-align:right;">
                  <span class="cnn-pill cnn-pill-${l.regime_code}">${k}</span>
                </div>
              </div>
            `}).join("")}
        </div>
      </div>
    </section>

    <!-- SECTION 2: CORE ETF SNAPSHOT STRIP ($SMH, $XLV, $QQQ) -->
    <section style="display:grid; grid-template-columns:repeat(auto-fit, minmax(min(100%, 280px), 1fr)); gap:14px; margin-bottom:22px;">
      ${n.etfs.map(l=>{const v=o==="jp"?l.name_jp:o==="kr"?l.name_kr:l.name_en,h=o==="jp"?l.role_jp:o==="kr"?l.role_kr:l.role_en,E=`/api/referral/redirect/tradingview?ticker=${encodeURIComponent(l.ticker)}`,k=`/api/referral/redirect/seekingalpha?ticker=${encodeURIComponent(l.ticker)}`;return`
          <div class="proof-card" style="margin-bottom:0; border-top:2px solid ${l.ticker==="SMH"?"var(--fin-blue)":l.ticker==="XLV"?"var(--fin-up)":"#64748b"};">
            <div style="display:flex; justify-content:space-between; align-items:flex-start;">
              <div>
                <div style="display:flex; align-items:center; gap:8px;">
                  <span class="mono" style="font-size:1.15rem; font-weight:900; color:#ffffff;">$${l.ticker}</span>
                  <span style="font-size:0.78rem; color:var(--text-secondary); font-weight:600;">${v}</span>
                </div>
                <div style="font-size:0.74rem; color:var(--muted); margin-top:3px;">${h}</div>
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
                <a class="btn btn-sm" href="${E}" target="_blank" rel="noopener noreferrer">TV Chart ↗</a>
                <a class="btn btn-sm" href="${k}" target="_blank" rel="noopener noreferrer">Holdings ↗</a>
              </div>
            </div>
          </div>
        `}).join("")}
    </section>

    <!-- SECTION 3: INTERACTIVE SMH + XLV REBALANCING & 2.5M KRW TAX HARVESTING ENGINE + 3-STAGE LUMP-SUM PLANNER -->
    <section class="semi-calc-grid" style="display:grid; grid-template-columns:repeat(auto-fit, minmax(min(100%, 380px), 1fr)); gap:18px; margin-bottom:22px;">
      <!-- Calculator 1: SMH + XLV Rebalancing & Tax Optimizer -->
      <div class="proof-card" style="margin-bottom:0; border-top:2px solid var(--fin-up);">
        <div style="font-size:0.7rem; font-family:var(--font-mono); font-weight:700; color:var(--fin-up); letter-spacing:0.05em;">
          ${t.rebalSectionTag}
        </div>
        <h3 style="font-size:1.12rem; font-weight:800; color:#ffffff; margin:4px 0 6px;">${t.rebalSectionTitle}</h3>
        <p style="font-size:0.8rem; color:var(--muted); margin-bottom:14px;">${t.rebalSectionDesc}</p>

        <div class="semi-form-two-col" style="display:grid; grid-template-columns:repeat(2, 1fr); gap:10px; margin-bottom:12px;">
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

        ${c?`
          <div id="semiRebalOutput" style="margin-top:14px; background:#060911; border:1px solid var(--border); border-left:3px solid var(--fin-up); border-radius:4px; padding:14px; font-size:0.8rem;">
            <div style="font-weight:800; color:var(--fin-up); margin-bottom:4px;">
              ${o==="jp"?c.active_rule_jp:o==="kr"?c.active_rule_kr:c.active_rule_en}
            </div>
            <div class="mono" style="font-size:0.71rem; color:#93c5fd; margin-bottom:8px;">
              Latest Close Basis (${c.as_of_date||n.date}): $SMH @ $${Number(c.smh_close??n.smh_close).toFixed(2)} · $XLV @ $${Number(c.xlv_close??n.xlv_close).toFixed(2)} · FX ₩${Number(c.usdkrw??n.usdkrw).toLocaleString()}/$ · Total ₩${Number(c.total_capital_krw??0).toLocaleString()}
            </div>
            <div class="semi-form-two-col" style="display:grid; grid-template-columns:1fr 1fr; gap:10px; margin-bottom:10px;">
              <div style="background:#0c1220; padding:10px; border-radius:4px; border:1px solid var(--border);">
                <div style="font-size:0.7rem; color:var(--muted);">TARGET $SMH (${c.target_smh_weight_pct}%)</div>
                <div class="mono" style="font-size:1.05rem; font-weight:800; color:#fff; margin-top:2px;">
                  $${Number(c.target_smh_usd??0).toLocaleString()} (${c.target_smh_shares} sh)
                </div>
                <div class="mono" style="font-size:0.73rem; color:${c.delta_smh_usd>=0?"var(--fin-up)":"var(--fin-down)"}; margin-top:2px;">
                  Order vs Drift: ${c.delta_smh_usd>=0?"BUY +":"SELL "}$${Math.abs(Number(c.delta_smh_usd??0)).toLocaleString()} (${c.delta_smh_shares>=0?"+":""}${c.delta_smh_shares} sh)
                </div>
              </div>
              <div style="background:#0c1220; padding:10px; border-radius:4px; border:1px solid var(--border);">
                <div style="font-size:0.7rem; color:var(--muted);">TARGET $XLV (${c.target_xlv_weight_pct}%)</div>
                <div class="mono" style="font-size:1.05rem; font-weight:800; color:#fff; margin-top:2px;">
                  $${Number(c.target_xlv_usd??0).toLocaleString()} (${c.target_xlv_shares} sh)
                </div>
                <div class="mono" style="font-size:0.73rem; color:${c.delta_xlv_usd>=0?"var(--fin-up)":"var(--fin-down)"}; margin-top:2px;">
                  Order vs Drift: ${c.delta_xlv_usd>=0?"BUY +":"SELL "}$${Math.abs(Number(c.delta_xlv_usd??0)).toLocaleString()} (${c.delta_xlv_shares>=0?"+":""}${c.delta_xlv_shares} sh)
                </div>
              </div>
            </div>
            <div style="font-size:0.75rem; color:var(--text-secondary); line-height:1.45; border-top:1px solid var(--border); padding-top:8px;">
              <div><b>KRW 2.5M Tax-Free Harvester:</b> ${o==="jp"?c.kr_tax_guidance_jp:o==="kr"?c.kr_tax_guidance_kr:c.kr_tax_guidance_en}</div>
              <div class="mono" style="color:var(--muted); margin-top:4px;">
                Residual Cash: $${Number(c.residual_cash_usd??0).toFixed(2)} · Est. Annual Tax & Turnover Drag (${c.rebalance_frequency}): -${c.estimated_tax_drag_pct}%/yr · Expected Net 15Y Rate: +${c.expected_net_cagr_pct}%/yr
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

        <div class="semi-form-two-col" style="display:grid; grid-template-columns:1fr 1fr; gap:10px; margin-bottom:12px;">
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
              ${p.tranches.map(l=>{const v=o==="jp"?l.title_jp:o==="kr"?l.title_kr:l.title_en,h=o==="jp"?l.timing_jp:o==="kr"?l.timing_kr:l.timing_en,E=o==="jp"?l.note_jp:o==="kr"?l.note_kr:l.note_en;return`
                  <div style="background:#0c1220; padding:10px; border-radius:4px; border:1px solid var(--border);">
                    <div style="display:flex; justify-content:space-between; align-items:center;">
                      <b style="color:#ffffff;">${v}</b>
                      <span class="mono" style="color:var(--fin-up); font-weight:700;">$${l.amount_usd.toLocaleString()} (${l.allocation_pct}%)</span>
                    </div>
                    <div class="mono" style="font-size:0.72rem; color:#93c5fd; margin-top:2px;">
                      ${h} · $SMH: $${l.smh_usd.toLocaleString()} (${l.smh_shares} sh) | $XLV: $${l.xlv_usd.toLocaleString()} (${l.xlv_shares} sh)
                    </div>
                    <div style="font-size:0.74rem; color:var(--muted); margin-top:4px;">${E}</div>
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
        <div style="display:flex; gap:8px; align-items:center; flex-wrap:wrap;">
          <button type="button" class="btn" id="btnSendSemiTelegram" style="border-color:rgba(96,165,250,0.4); color:#93c5fd;">📲 Send 80:20 Signal to Telegram</button>
          <button class="btn btn-sm" id="btnDownloadSemiCsv">
            Download 2000–2026 Daily CSV Dataset (Pro)
          </button>
        </div>
      </div>

      ${St(e.semiHistory)}

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
            ${f.map(l=>`
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
  `}const Pe=window.location.pathname.toLowerCase(),Fe=window.location.hash.toLowerCase(),$t=new URLSearchParams(window.location.search),Oe=($t.get("view")||"").toLowerCase(),Et=Oe==="semi"||Fe.includes("semi")||Pe.includes("/semi")?"semi":Oe==="rightside"||Fe.includes("rightside")||Pe.includes("/rightside")?"rightside":window.__DEFAULT_VIEW__==="semi"?"semi":"rightside",s={lang:localStorage.getItem("rsa_lang")||"en",activeView:Et,isProUnlocked:localStorage.getItem("rsa_pro_unlocked")==="true",licenseKey:localStorage.getItem("rsa_token")||"",selectedCheckoutPlan:"monthly",stocks:[],filteredStocks:[],backtestKpis:null,pineCode:null,searchQuery:"",zoneFilter:"ALL",sortCol:"score",sortAsc:!1,docTicker:"CELH",docEntry:null,docDays:42,docLastResult:null,semiOverview:null,semiHistory:null,semiGaugeTab:"overview",semiRange:"1Y",semiCapUsd:1e5,semiMode:"AUTO_REGIME",semiFreq:"ANNUAL",semiGainKrw:38e5,semiRebalanceResult:null,semiLumpCapUsd:5e4,semiLumpScore:null,semiLumpSumResult:null,config:{site1_name:"RightSideAlpha",site1_url:localStorage.getItem("rsa_cfg_site1_url")||"https://getbreakai.com",site2_url:"https://truthofmarket.com",ls_site1_monthly_url:localStorage.getItem("rsa_cfg_ls_monthly")||"https://rightsidealpha.lemonsqueezy.com/checkout/buy/pro-monthly",ls_site1_ltd_url:localStorage.getItem("rsa_cfg_ls_ltd")||"https://rightsidealpha.lemonsqueezy.com/checkout/buy/lifetime-pass",tradingview_aff_id:localStorage.getItem("rsa_cfg_aff_tv")||"rightsidealpha",seekingalpha_source:localStorage.getItem("rsa_cfg_aff_sa")||"affiliate_rightside",trendspider_aff_id:localStorage.getItem("rsa_cfg_aff_ts")||"rightside",tg_bot_token:localStorage.getItem("rsa_tg_bot_token")||"",tg_chat_id:localStorage.getItem("rsa_tg_chat_id")||"",tg_channel_url:localStorage.getItem("rsa_tg_channel_url")||"https://t.me/RightSideAlphaBot",tg_auto_ignition:localStorage.getItem("rsa_tg_auto_ignition")!=="false",tg_auto_stop:localStorage.getItem("rsa_tg_auto_stop")!=="false",tg_auto_semi:localStorage.getItem("rsa_tg_auto_semi")!=="false"},telegramStatus:null,telegramLastPreview:"",get t(){return be[this.lang]||be.en}};function D(e){const t=document.getElementById("toastBox");t&&(t.textContent=e,t.style.display="block",clearTimeout(window.__toastTimer),window.__toastTimer=setTimeout(()=>{t.style.display="none"},3200))}function ee(){const e=(s.searchQuery||"").trim().toLowerCase(),t=s.zoneFilter;let o=s.stocks.filter(i=>!(!i.ticker||String(i.ticker).includes(".")||t!=="ALL"&&i.zone_code!==t||e&&!`${i.ticker} ${i.name||""} ${i.name_en||""} ${i.name_jp||""} ${i.name_kr||""} ${i.sector||""}`.toLowerCase().includes(e)));const n=s.sortCol,a=s.sortAsc?1:-1;o.sort((i,r)=>{const d=i[n],g=r[n];return typeof d=="string"?d.localeCompare(g)*a:((d||0)-(g||0))*a}),s.filteredStocks=o}async function Tt(e,t="Pro Terminal Unlocked — All 72 US Equity Targets Active"){const o=String(e).trim();if(!o)return!1;const n=await ve(o);return n&&n.valid?(s.isProUnlocked=!0,s.licenseKey=o,localStorage.setItem("rsa_pro_unlocked","true"),localStorage.setItem("rsa_token",o),await ce(),U(),D(t),!0):!1}function kt(){var e,t,o;try{(e=window.createLemonSqueezy)==null||e.call(window),(o=(t=window.LemonSqueezy)==null?void 0:t.Setup)==null||o.call(t,{eventHandler:async n=>{var a,i,r,d,g;if((n==null?void 0:n.event)==="Checkout.Success"){const c=((r=(i=(a=n==null?void 0:n.data)==null?void 0:a.order)==null?void 0:i.data)==null?void 0:r.attributes)||{},p=((d=n==null?void 0:n.data)==null?void 0:d.license_key)||(c==null?void 0:c.license_key)||((g=c==null?void 0:c.first_order_item)==null?void 0:g.license_key)||"RSA-PRO-2026-LIVE";await Tt(p,"Lemon Squeezy Checkout Complete — Pro License Activated")}}})}catch{}}function Lt(){const e=s.t;return`
    ${ct(s)}
    ${dt(s)}
    <section class="screener-panel">
      ${pt(s)}
      ${mt(s)}
    </section>
    ${gt(s)}
    ${ft(s)}

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
  `}function U(){const e=document.getElementById("app");if(!e)return;const t=s.t;e.innerHTML=`
    ${lt(s)}
    <main class="container">
      ${s.activeView==="semi"?xt(s):Lt()}

      <footer style="border-top:1px solid var(--border); padding-top:20px; margin-top:28px; color:var(--muted); font-size:0.76rem; line-height:1.6;">
        <p id="disclaimerText">${t.disclaimer}</p>
        <p style="margin-top:8px; font-family:var(--font-mono); font-size:0.72rem;" id="copyrightText">${t.copyright}</p>
      </footer>
    </main>
    <canvas id="scoreCanvas" width="900" height="500" style="display:none;"></canvas>
    ${bt(s)}
  `,wt(),kt()}function J(e){s.activeView=e==="semi"?"semi":"rightside",s.activeView==="semi"?window.history.replaceState(null,"","#semi"):window.history.replaceState(null,"","#rightside"),U(),window.scrollTo({top:0,behavior:"smooth"})}function It(e){const o=(new URL(e,window.location.origin).searchParams.get("ticker")||"SPY").toUpperCase(),n=String(e||"").toLowerCase();if(n.includes("tradingview")){const i=encodeURIComponent(s.config.tradingview_aff_id||"rightsidealpha");return`https://www.tradingview.com/symbols/${encodeURIComponent(o)}/?aff_id=${i}`}if(n.includes("trendspider"))return`https://www.trendspider.com/?_go=${encodeURIComponent(s.config.trendspider_aff_id||"rightside")}`;const a=encodeURIComponent(s.config.seekingalpha_source||"affiliate_rightside");return`https://seekingalpha.com/symbol/${encodeURIComponent(o)}/earnings?source=${a}`}function Xe(e=document){e.querySelectorAll('a[href^="/api/referral/redirect/"]').forEach(t=>{t.dataset.refBound!=="1"&&(t.dataset.refBound="1",t.addEventListener("click",o=>{const n=window.location.hostname;if(window.__STATIC_MODE__===!0||n&&n!=="localhost"&&n!=="127.0.0.1"){o.preventDefault();const a=t.getAttribute("href")||"",i=It(a);window.open(i,"_blank","noopener,noreferrer")}}))})}function Y(e=null){e&&(s.selectedCheckoutPlan=e);const t=document.getElementById("licenseModal"),o=document.getElementById("selectedPlanLabel"),n=document.getElementById("externalCheckoutLink");o&&(o.textContent=s.selectedCheckoutPlan==="lifetime"?"$199 Lifetime License (One-Time)":"$29/mo Pro Quantitative Terminal"),n&&(n.href=s.selectedCheckoutPlan==="lifetime"?s.config.ls_site1_ltd_url||"https://rightsidealpha.lemonsqueezy.com/checkout/buy/lifetime-pass":s.config.ls_site1_monthly_url||"https://rightsidealpha.lemonsqueezy.com/checkout/buy/pro-monthly"),t&&(t.style.display="flex")}function ge(){const e=document.getElementById("licenseModal");e&&(e.style.display="none")}function wt(){const e=document.getElementById("brandHomeBtn");e&&e.addEventListener("click",()=>{s.zoneFilter="ALL",s.searchQuery="",ee(),U(),window.scrollTo({top:0,behavior:"smooth"})});const t=document.getElementById("navTabRightSide");t&&t.addEventListener("click",()=>J("rightside"));const o=document.getElementById("navTabSemiFg");o&&o.addEventListener("click",()=>J("semi"));const n=document.getElementById("ribbonSwitchSemi");n&&n.addEventListener("click",()=>J("semi"));const a=document.getElementById("crossFunnelSwitchBtn");a&&a.addEventListener("click",()=>J("semi"));const i=document.getElementById("btnSwitchToRightSide");i&&i.addEventListener("click",()=>J("rightside")),document.querySelectorAll(".lang-btn").forEach(m=>{m.addEventListener("click",()=>{const u=m.getAttribute("data-lang");u&&be[u]&&(s.lang=u,localStorage.setItem("rsa_lang",u),U())})});const r=document.getElementById("searchInput");r&&r.addEventListener("input",m=>{s.searchQuery=m.target.value,ee();const u=document.getElementById("tableBody");u&&(u.innerHTML=_e(s)),fe()}),document.querySelectorAll(".filter-tab").forEach(m=>{m.addEventListener("click",()=>{s.zoneFilter=m.getAttribute("data-zone")||"ALL",ee(),U()})}),document.querySelectorAll(".sort-header").forEach(m=>{m.addEventListener("click",()=>{const u=m.getAttribute("data-sort");if(!u)return;s.sortCol===u?s.sortAsc=!s.sortAsc:(s.sortCol=u,s.sortAsc=u==="ticker"),ee(),document.querySelectorAll(".sort-header").forEach(x=>{const _=x.getAttribute("data-sort"),S=x.querySelector(".sort-arrow"),I=s.sortCol===_?s.sortAsc?"↑":"↓":"↕";S?S.textContent=I:x.textContent=x.textContent.replace(/[↑↓↕]\s*$/,I)});const b=document.getElementById("tableBody");b&&(b.innerHTML=_e(s)),fe()})}),document.querySelectorAll(".lemonsqueezy-button").forEach(m=>{m.addEventListener("click",u=>{const b=m.getAttribute("href")||"",x=m.getAttribute("data-plan")||(m.id==="cardLtdBtn"||b.includes("lifetime")?"lifetime":"monthly"),_=b.includes("rightsidealpha.lemonsqueezy.com"),S=!!window.LemonSqueezy;(_||!S)&&(u.preventDefault(),Y(x))})});const d=document.getElementById("btnOpenLicense");d&&d.addEventListener("click",()=>Y());const g=document.getElementById("proStatusBadge");g&&(g.style.cursor="pointer",g.addEventListener("click",()=>Y()));const c=document.getElementById("vaultUnlockBtn");c&&c.addEventListener("click",()=>Y());const p=document.getElementById("btnCancelLicense");p&&p.addEventListener("click",ge);const f=async(m=null)=>{const u=document.getElementById("licenseInput"),b=document.getElementById("licenseMsg");m&&u&&(u.value=m);const x=(m||(u?u.value:"")).trim();if(!x){b&&(b.style.color="var(--fin-down)",b.textContent="Please enter a valid license key.");return}try{const _=await ve(x);_.valid?(s.isProUnlocked=!0,s.licenseKey=x,localStorage.setItem("rsa_pro_unlocked","true"),localStorage.setItem("rsa_token",x),b&&(b.style.color="var(--fin-up)",b.textContent=_.message||"Pro Terminal Unlocked."),await ce(),setTimeout(()=>{ge(),U(),D("Pro Terminal Unlocked — All 72 US Equity Targets Active")},250)):b&&(b.style.color="var(--fin-down)",b.textContent=_.message||"Invalid key. Use PRO-DEMO-2026 for demo.")}catch{b&&(b.style.color="var(--fin-down)",b.textContent="Validation error. Try PRO-DEMO-2026.")}},l=document.getElementById("btnVerifyLicense");l&&l.addEventListener("click",()=>f());const v=document.getElementById("btnFillDemoKey");v&&v.addEventListener("click",()=>f("PRO-DEMO-2026"));const h=document.getElementById("btnDeactivateLicense");h&&h.addEventListener("click",async()=>{localStorage.removeItem("rsa_pro_unlocked"),localStorage.removeItem("rsa_token"),s.isProUnlocked=!1,s.licenseKey="",await ce(),ge(),U(),D("Pro License Deactivated — Returned to Public Preview Mode")});const E=document.getElementById("configModal"),k=document.getElementById("btnOpenConfig"),y=document.getElementById("btnCancelConfig"),$=document.getElementById("btnSaveConfig");k&&E&&k.addEventListener("click",()=>{E.style.display="flex"}),y&&E&&y.addEventListener("click",()=>{E.style.display="none"}),$&&$.addEventListener("click",async()=>{var I,T,C,M,Q;const m=((I=document.getElementById("cfgSite1Url"))==null?void 0:I.value.trim())||s.config.site1_url,u=((T=document.getElementById("cfgLsMonthly"))==null?void 0:T.value.trim())||s.config.ls_site1_monthly_url,b=((C=document.getElementById("cfgLsLtd"))==null?void 0:C.value.trim())||s.config.ls_site1_ltd_url,x=((M=document.getElementById("cfgAffTv"))==null?void 0:M.value.trim())||"rightsidealpha",_=((Q=document.getElementById("cfgAffSa"))==null?void 0:Q.value.trim())||"affiliate_rightside",S=s.config.trendspider_aff_id||"rightside";s.config.site1_url=m,s.config.ls_site1_monthly_url=u,s.config.ls_site1_ltd_url=b,s.config.tradingview_aff_id=x,s.config.seekingalpha_source=_,s.config.trendspider_aff_id=S,localStorage.setItem("rsa_cfg_site1_url",m),localStorage.setItem("rsa_cfg_ls_monthly",u),localStorage.setItem("rsa_cfg_ls_ltd",b),localStorage.setItem("rsa_cfg_aff_tv",x),localStorage.setItem("rsa_cfg_aff_sa",_),localStorage.setItem("rsa_cfg_aff_ts",S);try{await tt({tradingview_aff_id:x,seekingalpha_source:_,trendspider_aff_id:S,ls_site1_monthly_url:u,ls_site1_ltd_url:b,site1_url:m})}catch{}E&&(E.style.display="none"),U(),D("Terminal & Affiliate Configuration Saved")});const L=document.getElementById("telegramModal"),w=document.getElementById("btnOpenTelegram"),A=document.getElementById("btnCloseTelegram"),R=document.getElementById("btnDetectTgChatId"),F=document.getElementById("btnSaveTelegram");w&&L&&w.addEventListener("click",()=>{L.style.display="flex"}),A&&L&&A.addEventListener("click",()=>{L.style.display="none"});const N=(m,u)=>{var S,I;const b=document.getElementById("tgHeaderStatusDot");b&&(b.style.background=m?"#10b981":"#60a5fa");const x=document.getElementById("tgModalStatusBadge");x&&(x.className=`badge ${m?"badge-ignition":"badge-watch"}`,x.textContent=m?((S=s.t.telegram)==null?void 0:S.statusConnected)||"CONNECTED ✓":((I=s.t.telegram)==null?void 0:I.statusPreview)||"PREVIEW / SETUP MODE");const _=document.getElementById("tgChannelLink");_&&u&&(_.href=u)};R&&R.addEventListener("click",async()=>{const m=document.getElementById("tgBotTokenInput"),u=document.getElementById("tgChatIdInput"),b=document.getElementById("tgModalMsg"),x=((m==null?void 0:m.value)||s.config.tg_bot_token||"").trim();b&&(b.style.color="#93c5fd",b.textContent="Querying Telegram Bot API getUpdates for latest Chat ID...");const _=await je(x);_&&_.ok&&_.chat_id?(u&&(u.value=_.chat_id),s.config.tg_bot_token=x,s.config.tg_chat_id=String(_.chat_id),N(!!(x&&_.chat_id),s.config.tg_channel_url),b&&(b.style.color="var(--fin-up)",b.textContent=`Detected Chat ID: ${_.chat_id} (${_.chat_title||"Telegram Chat"})`),D(`Telegram Chat ID Auto-Detected: ${_.chat_id}`)):b&&(b.style.color="var(--fin-amber)",b.textContent=(_==null?void 0:_.detail)||"Could not auto-detect Chat ID. Send /start to your bot in Telegram and try again.")}),F&&F.addEventListener("click",async()=>{var C,M,Q,K,re,Me;const m=(((C=document.getElementById("tgBotTokenInput"))==null?void 0:C.value)||"").trim(),u=(((M=document.getElementById("tgChatIdInput"))==null?void 0:M.value)||"").trim(),b=(((Q=document.getElementById("tgChannelUrlInput"))==null?void 0:Q.value)||"").trim()||"https://t.me/RightSideAlphaBot",x=!!(((K=document.getElementById("tgAutoIgnition"))==null?void 0:K.checked)??!0),_=!!(((re=document.getElementById("tgAutoStop"))==null?void 0:re.checked)??!0),S=!!(((Me=document.getElementById("tgAutoSemi"))==null?void 0:Me.checked)??!0),I=document.getElementById("tgModalMsg");s.config.tg_bot_token=m,s.config.tg_chat_id=u,s.config.tg_channel_url=b,s.config.tg_auto_ignition=x,s.config.tg_auto_stop=_,s.config.tg_auto_semi=S;const T=await it({bot_token:m,chat_id:u,channel_url:b,auto_alert_ignition:x,auto_alert_stop:_,auto_alert_semi_regime:S});s.telegramStatus=T,N(!!(T!=null&&T.configured),b),I&&(I.style.color="var(--fin-up)",I.textContent=T!=null&&T.configured?"Telegram Bot & Chat ID saved — Live Dispatch Active ✓":"Telegram preferences saved (Enter Bot Token & Chat ID for live delivery)."),D(T!=null&&T.configured?"Telegram Connected & Saved":"Telegram Settings Saved (Preview Mode)")});const O=async(m,u={},b=!1)=>{var C,M;b&&L&&(L.style.display="flex");const x=(((C=document.getElementById("tgBotTokenInput"))==null?void 0:C.value)??s.config.tg_bot_token??"").trim(),_=(((M=document.getElementById("tgChatIdInput"))==null?void 0:M.value)??s.config.tg_chat_id??"").trim(),S=document.getElementById("tgModalMsg"),I=document.getElementById("tgPreviewBox");S&&(S.style.color="#93c5fd",S.textContent=`Generating & dispatching '${m.toUpperCase()}' Telegram alert...`);const T=m==="test"?await rt({bot_token:x,chat_id:_,lang:s.lang,...u}):await qe({briefing_type:m,bot_token:x,chat_id:_,lang:s.lang,...u});T!=null&&T.message_preview&&(s.telegramLastPreview=T.message_preview,I&&(I.textContent=T.message_preview)),T!=null&&T.delivered?(N(!0,s.config.tg_channel_url),S&&(S.style.color="var(--fin-up)",S.textContent=`✓ Delivered live to Telegram (${T.chat_id||_})`),D(`Sent ${m.toUpperCase()} Alert to Telegram`)):(S&&(S.style.color=(T==null?void 0:T.ok)===!1?"var(--fin-down)":"var(--fin-amber)",S.textContent=(T==null?void 0:T.detail)||"Preview generated below (Configure Bot Token & Chat ID to deliver live to Telegram)."),D((T==null?void 0:T.ok)===!1?"Telegram API Error — Showing Preview":`Generated ${m.toUpperCase()} Telegram Preview`))},j=document.getElementById("btnTgSendTest");j&&j.addEventListener("click",()=>O("test"));const z=document.getElementById("btnTgSendIgnition");z&&z.addEventListener("click",()=>O("ignition"));const H=document.getElementById("btnTgSendSemi");H&&H.addEventListener("click",()=>O("semi"));const Z=document.getElementById("btnTgSendFull");Z&&Z.addEventListener("click",()=>O("full"));const W=()=>{const m=document.getElementById("btnSendDoctorTelegram");m&&m.dataset.tgBound!=="1"&&(m.dataset.tgBound="1",m.addEventListener("click",()=>{var _,S,I,T,C;const u=(((_=s.docLastResult)==null?void 0:_.ticker)||((S=document.getElementById("docTicker"))==null?void 0:S.value)||s.docTicker||"CELH").trim().toUpperCase(),b=parseFloat(String(((I=s.docLastResult)==null?void 0:I.entry_price)||((T=document.getElementById("docEntry"))==null?void 0:T.value)||s.docEntry||27.93)),x=parseInt(String(((C=document.getElementById("docDays"))==null?void 0:C.value)||s.docDays||42),10);O("doctor",{ticker:u,entry_price:b,days_held:x,doctor_result:s.docLastResult},!0)}))};W();const oe=document.getElementById("docTicker");oe&&oe.addEventListener("input",m=>{s.docTicker=m.target.value.toUpperCase()});const V=document.getElementById("docEntry");V&&V.addEventListener("input",m=>{s.docEntry=m.target.value});const B=document.getElementById("docDays");B&&B.addEventListener("input",m=>{s.docDays=m.target.value}),document.querySelectorAll(".btn-quick-doc").forEach(m=>{m.addEventListener("click",async()=>{const u=m.getAttribute("data-ticker")||"CELH",b=s.stocks.find(M=>M.ticker===u),x=document.getElementById("docTicker"),_=document.getElementById("docEntry"),S=document.getElementById("docDays"),I=document.getElementById("docOutput");x&&u&&(x.value=u);const T=b?Number(b.close):27.93;_&&(_.value=T.toFixed(2));const C=parseInt((S==null?void 0:S.value)||String(s.docDays||42),10);s.docTicker=u,s.docEntry=T.toFixed(2),s.docDays=C;try{const M=await se({ticker:u,entry_price:T,days_held:C,current_price:b?Number(b.close):void 0});s.docLastResult=M,I&&(I.innerHTML=he(M,s)),W()}catch{}})});const X=document.getElementById("btnRunPositionDoctor");X&&X.addEventListener("click",async()=>{var S,I,T;const m=(((S=document.getElementById("docTicker"))==null?void 0:S.value)||s.docTicker||"CELH").trim().toUpperCase(),u=parseFloat(((I=document.getElementById("docEntry"))==null?void 0:I.value)||String(s.docEntry||27.93)),b=parseInt(((T=document.getElementById("docDays"))==null?void 0:T.value)||String(s.docDays||42),10),x=document.getElementById("docOutput"),_=s.stocks.find(C=>C.ticker===m);s.docTicker=m,s.docEntry=Number.isNaN(u)?"27.93":u.toFixed(2),s.docDays=Number.isNaN(b)?42:b;try{const C=await se({ticker:m,entry_price:u,days_held:b,current_price:_?Number(_.close):void 0});s.docLastResult=C,x&&(x.innerHTML=he(C,s)),W()}catch{x&&(x.innerHTML='<div style="color:var(--fin-down);">Please enter a valid positive cost basis ($) and non-negative trading days.</div>')}});const G=document.getElementById("researchModal"),ne=document.getElementById("btnCloseResearch");ne&&G&&ne.addEventListener("click",()=>{G.style.display="none"});const ie=async m=>{if(!G)return;const u=String(m||"CELH").toUpperCase(),b=document.getElementById("researchModalTitle"),x=document.getElementById("researchModalBody");G.style.display="flex",document.querySelectorAll(".btn-switch-research").forEach(_=>{const S=_.getAttribute("data-ticker")===u;_.classList.toggle("btn-primary",S)}),b&&(b.textContent=`SEC Primary Filing Turnaround Brief — $${u}`),x&&(x.innerHTML="Loading primary filing brief...");try{const _=await Ye(u),S=s.stocks.find(K=>K.ticker===u),I=Number(_.current_price??(S==null?void 0:S.close)??27.93).toFixed(2),T=Number(_.stop_price??(S==null?void 0:S.stop_loss_price)??Number(I)*.91).toFixed(2),C=Number(_.target_price??(S==null?void 0:S.tp1_2x_price)??Number(I)*2).toFixed(2),M=_.as_of_date||(S==null?void 0:S.date)||_.report_date||"2026-10-13",Q=_.title||`${_.company_name||u} ($${_.ticker||u}) — ${_.opinion||"STRONG_BUY"} | Latest Close $${I} (${M})`;if(b&&(b.textContent=Q),x){const K=(_.content||"").replace(/&/g,"&amp;").replace(/</g,"&lt;").replace(/>/g,"&gt;").replace(/\n/g,"<br/>"),re=`
          <div style="display:flex; flex-wrap:wrap; gap:14px; background:#090d16; border:1px solid var(--border); border-left:3px solid var(--fin-up); padding:10px 14px; border-radius:4px; margin-bottom:14px; font-family:var(--font-mono); font-size:0.76rem;">
            <span>LATEST CLOSE (${M}): <b style="color:#ffffff;">$${I}</b></span>
            <span>HARD STOP (-9%): <b style="color:var(--fin-down);">$${T}</b></span>
            <span>TP1 TARGET (2x): <b style="color:var(--fin-up);">$${C}</b></span>
            <span>RRR: <b style="color:#93c5fd;">${_.rrr_ratio||"1 : 11.1"}</b></span>
          </div>
        `;x.innerHTML=`${re}<div style="font-family:var(--font-sans); line-height:1.65;">${K}</div>`}}catch{x&&(x.innerHTML="Failed to load research brief.")}};document.querySelectorAll(".btn-open-research, .btn-switch-research").forEach(m=>{m.addEventListener("click",()=>{const u=m.getAttribute("data-ticker")||"CELH";ie(u)})}),document.querySelectorAll(".btn-open-research-modal").forEach(m=>{m.addEventListener("click",()=>ie("CELH"))});const ae=document.getElementById("btnCopyPineScript");ae&&ae.addEventListener("click",async()=>{var u;const m=((u=document.getElementById("pineCodeBox"))==null?void 0:u.textContent)||"";try{await navigator.clipboard.writeText(m),D("TradingView Pine Script v5 Copied to Clipboard")}catch{D("Pine Script Ready to Copy")}});const Se=document.getElementById("btnCopyTopProofCard");Se&&Se.addEventListener("click",()=>{Qe(null)});const xe=document.getElementById("semiCapInput");xe&&xe.addEventListener("input",m=>{const u=parseFloat(m.target.value);Number.isNaN(u)||(s.semiCapUsd=u)});const $e=document.getElementById("semiModeInput");$e&&$e.addEventListener("change",m=>{s.semiMode=m.target.value});const Ee=document.getElementById("semiFreqInput");Ee&&Ee.addEventListener("change",m=>{s.semiFreq=m.target.value});const Te=document.getElementById("semiGainKrwInput");Te&&Te.addEventListener("input",m=>{const u=parseFloat(m.target.value);Number.isNaN(u)||(s.semiGainKrw=u)});const ke=document.getElementById("semiLumpCapInput");ke&&ke.addEventListener("input",m=>{const u=parseFloat(m.target.value);Number.isNaN(u)||(s.semiLumpCapUsd=u)});const Le=document.getElementById("semiLumpScoreInput");Le&&Le.addEventListener("input",m=>{const u=parseFloat(m.target.value);Number.isNaN(u)||(s.semiLumpScore=u)}),document.querySelectorAll(".cnn-view-tab").forEach(m=>{m.addEventListener("click",()=>{s.semiGaugeTab=m.getAttribute("data-semi-tab")||"overview",U()})}),document.querySelectorAll(".btn-semi-range").forEach(m=>{m.addEventListener("click",async()=>{const u=m.getAttribute("data-range")||"1Y";s.semiRange=u;try{s.semiHistory=await ze(u),U()}catch{D("Failed to load selected history window")}})});const Ie=document.getElementById("btnRunSemiRebalance");Ie&&Ie.addEventListener("click",async()=>{var _,S,I,T;const m=parseFloat(((_=document.getElementById("semiCapInput"))==null?void 0:_.value)||String(s.semiCapUsd||1e5)),u=((S=document.getElementById("semiModeInput"))==null?void 0:S.value)||s.semiMode||"AUTO_REGIME",b=((I=document.getElementById("semiFreqInput"))==null?void 0:I.value)||s.semiFreq||"ANNUAL",x=parseFloat(((T=document.getElementById("semiGainKrwInput"))==null?void 0:T.value)||String(s.semiGainKrw||38e5));s.semiCapUsd=m,s.semiMode=u,s.semiFreq=b,s.semiGainKrw=x;try{s.semiRebalanceResult=await Ve({total_capital_usd:m,strategy_mode:u,rebalance_frequency:b,unrealized_gain_krw:x}),U(),D("Updated $SMH / $XLV Rebalancing Orders")}catch{D("Please enter a valid positive capital amount")}});const we=async m=>{var x,_;const u=parseFloat(((x=document.getElementById("semiLumpCapInput"))==null?void 0:x.value)||String(s.semiLumpCapUsd||5e4)),b=m!==void 0?m:parseFloat(((_=document.getElementById("semiLumpScoreInput"))==null?void 0:_.value)||String(s.semiLumpScore??18));s.semiLumpCapUsd=u,s.semiLumpScore=b;try{s.semiLumpSumResult=await Ge({capital_usd:u,override_fg_score:b}),U()}catch{D("Invalid lump-sum input parameters")}},Ae=document.getElementById("btnRunSemiLumpSum");Ae&&Ae.addEventListener("click",()=>we()),document.querySelectorAll(".btn-sim-fg").forEach(m=>{m.addEventListener("click",()=>{const u=parseFloat(m.getAttribute("data-fg")||"18.0");we(u)})});const Ce=document.getElementById("btnExportSemiGauge");Ce&&Ce.addEventListener("click",()=>{At()});const Re=document.getElementById("btnSendSemiTelegram");Re&&Re.addEventListener("click",()=>{O("semi",{},!0)});const Ne=document.getElementById("btnDownloadSemiCsv");Ne&&Ne.addEventListener("click",async()=>{if(!s.isProUnlocked){Y(),D("Enter PRO-DEMO-2026 to unlock the 26-Year Daily CSV Dataset");return}const m=encodeURIComponent(s.licenseKey||"PRO-DEMO-2026");try{const b=await fetch(`/api/semi/pro/csv?license_key=${m}`,{method:"HEAD"});if(b.ok&&(b.headers.get("content-type")||"").includes("csv")){window.open(`/api/semi/pro/csv?license_key=${m}`,"_blank");return}}catch{}const u=document.createElement("a");u.href="./static_api/smh_xlv_fear_greed_history.csv",u.download="SemiFearGreed_SMH_XLV_2000_2026_History.csv",u.click()}),fe(),Xe(document)}function fe(){document.querySelectorAll(".btn-unlock-row, .btn-unlock-inline").forEach(e=>{e.dataset.unlockBound!=="1"&&(e.dataset.unlockBound="1",e.addEventListener("click",()=>{Y()}))}),document.querySelectorAll(".btn-share-card").forEach(e=>{e.dataset.shareBound!=="1"&&(e.dataset.shareBound="1",e.addEventListener("click",()=>{const t=e.getAttribute("data-ticker"),o=s.stocks.find(n=>n.ticker===t);Qe(o)}))}),Xe(document.getElementById("tableBody")||document)}function Qe(e){const t=document.getElementById("scoreCanvas");if(!t)return;const o=t.getContext("2d");o.fillStyle="#090d16",o.fillRect(0,0,900,500),o.strokeStyle="#2962ff",o.lineWidth=3,o.strokeRect(16,16,868,468),o.fillStyle="#0ecb81",o.font="bold 20px Inter, sans-serif",o.fillText("RIGHTSIDEALPHA · US EQUITY TURNAROUND TERMINAL",45,62),e?(o.fillStyle="#ffffff",o.font="bold 42px JetBrains Mono, monospace",o.fillText(`$${e.ticker} (${e.name_en||e.name||e.ticker})`,45,125),o.fillStyle="#93c5fd",o.font="bold 24px JetBrains Mono, monospace",o.fillText(`Signal Regime: ${e.zone_label_en||e.zone_code}  |  PW-RSI Score: ${Number(e.score||0)}/100`,45,175),o.fillStyle="#cbd5e1",o.font="20px JetBrains Mono, monospace",o.fillText(`Last Close: $${Number(e.close||0).toFixed(2)}  |  52W High DD: ${Number(e.dd_high52_pct||0)}%  |  vs 52W Low: +${Number(e.prox_low52_pct||0)}%`,45,230),o.fillText(`vs MA20: ${Number(e.vs_ma20_pct||0)}%  |  vs MA60: ${Number(e.vs_ma60_pct||0)}%  |  10D Vol Ratio: ${Number(e.vol_surge_10d||1)}x`,45,270),o.fillText(`Historical 1Y 2x (+100%) Hit Rate after -40% Drawdown: ${Number(e.hist_2x_rate||0)}%`,45,315)):(o.fillStyle="#ffffff",o.font="bold 34px Inter, sans-serif",o.fillText("20-Year US Equity Backtest: Left-Side vs PW-RSI Right-Side",45,125),o.fillStyle="#f6465d",o.font="22px JetBrains Mono, monospace",o.fillText("Blind 52W-Low Dip Buy: 28.91% 2x Rate | -30.31% MDD | 81d Underwater",45,200),o.fillStyle="#0ecb81",o.font="bold 24px JetBrains Mono, monospace",o.fillText("PW-RSI Right-Side:     55.24% 2x Rate | -16.49% MDD | 29d Underwater",45,260)),o.fillStyle="#8492a6",o.font="bold 16px JetBrains Mono, monospace",o.fillText(`Verified Dataset (N=394,371 US Stock-Days) · ${s.config.site1_url}`,45,440),t.toBlob(n=>{if(!n)return;const a=URL.createObjectURL(n),i=document.createElement("a");i.href=a,i.download=e?`RightSideAlpha_${e.ticker}_TearSheet.png`:"RightSideAlpha_Benchmark.png",i.click(),URL.revokeObjectURL(a),D(e?`Downloaded $${e.ticker} Tear Sheet PNG`:"Downloaded Benchmark Tear Sheet PNG")})}function At(){const e=document.getElementById("scoreCanvas");if(!e||!s.semiOverview)return;const t=e.getContext("2d"),o=s.semiOverview;t.fillStyle="#ffffff",t.fillRect(0,0,900,500),t.fillStyle="#cc0000",t.fillRect(0,0,900,10),t.fillStyle="#cc0000",t.font="bold 18px Inter, sans-serif",t.fillText("MARKETS · SEMICONDUCTOR FEAR & GREED INDEX",45,55),t.fillStyle="#111827",t.font="bold 40px Inter, sans-serif",t.fillText(`Score: ${Number(o.fg_score||0).toFixed(1)} / 100 — ${String(o.regime_en||"NEUTRAL").toUpperCase()}`,45,115),t.fillStyle="#374151",t.font="22px JetBrains Mono, monospace",t.fillText(`As of ${o.date||"2026-10-26"}  |  $SMH: $${Number(o.smh_close||0).toFixed(2)} (${Number(o.smh_dd_pct||0)}% DD)  |  $XLV: $${Number(o.xlv_close||0).toFixed(2)}`,45,170),t.fillStyle="#b91c1c",t.font="bold 22px Inter, sans-serif",t.fillText(`Active Signal: ${o.action_headline_en||""}`,45,230),t.fillStyle="#4b5563",t.font="18px JetBrains Mono, monospace",t.fillText("26-Year Barbell (2000-2026): +10.60% CAGR (14.22x) vs QQQ +8.79% (9.21x)",45,300),t.fillText("10-Year AI Era (2016-2026):  +28.63% CAGR (15.07x) vs QQQ +20.74% (7.61x)",45,338),t.fillStyle="#6b7280",t.font="bold 16px JetBrains Mono, monospace",t.fillText(`SemiFearGreed Quantitative Barbell Engine · ${s.config.site2_url}`,45,445),e.toBlob(n=>{if(!n)return;const a=URL.createObjectURL(n),i=document.createElement("a");i.href=a,i.download=`SemiFearGreed_${o.date||"2026-10-26"}.png`,i.click(),URL.revokeObjectURL(a),D("Downloaded Semiconductor Fear & Greed Index PNG")})}async function ce(){try{const[e,t,o,n,a,i]=await Promise.all([Ke({limit:200}),We().catch(()=>null),et().catch(()=>null),ot().catch(()=>null),ze(s.semiRange).catch(()=>null),nt().catch(()=>null)]);s.stocks=Array.isArray(e)?e.filter(f=>f.ticker&&!String(f.ticker).includes(".")):[],t&&t.kpis&&(s.backtestKpis=t.kpis),o&&typeof o=="object"&&Object.entries(o).forEach(([f,l])=>{l!=null&&l!==""&&(s.config[f]=l)}),i&&typeof i=="object"&&(s.telegramStatus=i,i.chat_id&&!s.config.tg_chat_id&&(s.config.tg_chat_id=i.chat_id),i.channel_url&&!localStorage.getItem("rsa_tg_channel_url")&&(s.config.tg_channel_url=i.channel_url),i.auto_alert_ignition!==void 0&&localStorage.getItem("rsa_tg_auto_ignition")===null&&(s.config.tg_auto_ignition=!!i.auto_alert_ignition),i.auto_alert_stop!==void 0&&localStorage.getItem("rsa_tg_auto_stop")===null&&(s.config.tg_auto_stop=!!i.auto_alert_stop),i.auto_alert_semi_regime!==void 0&&localStorage.getItem("rsa_tg_auto_semi")===null&&(s.config.tg_auto_semi=!!i.auto_alert_semi_regime)),n&&(s.semiOverview=n,s.semiLumpScore===null&&(s.semiLumpScore=n.fg_score)),a&&(s.semiHistory=a);const r=s.stocks.find(f=>f.ticker==="CELH"),d=r?Number(r.close):27.93;s.docEntry===null&&(s.docEntry=d.toFixed(2));const[g,c,p]=await Promise.all([Ve({total_capital_usd:s.semiCapUsd,strategy_mode:s.semiMode,rebalance_frequency:s.semiFreq,unrealized_gain_krw:s.semiGainKrw}).catch(()=>null),Ge({capital_usd:s.semiLumpCapUsd,override_fg_score:s.semiLumpScore}).catch(()=>null),se({ticker:s.docTicker||"CELH",entry_price:parseFloat(String(s.docEntry||d)),days_held:parseInt(String(s.docDays||42),10),current_price:d}).catch(()=>null)]);if(g&&(s.semiRebalanceResult=g),c&&(s.semiLumpSumResult=c),p&&(s.docLastResult=p),s.isProUnlocked){const f=await Je().catch(()=>null);f&&f.code&&(s.pineCode=f.code)}ee()}catch(e){console.error("Failed to load initial data:",e)}}async function Ct(){try{const e=new URLSearchParams(window.location.search),t=e.get("license_key")||e.get("key"),o=e.get("checkout")==="success";if(t||o){const n=t||"RSA-PRO-2026-LIVE",a=await ve(n).catch(()=>null);a&&a.valid&&(s.isProUnlocked=!0,s.licenseKey=n,localStorage.setItem("rsa_pro_unlocked","true"),localStorage.setItem("rsa_token",n));const i=`${window.location.pathname}${window.location.hash||""}`;window.history.replaceState(null,"",i)}}catch{}await ce(),U()}Ct();
