#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
scripts/build_jp_seo_pages.py
4사업부 (GetBreakAI — getbreakai.com)
일본 구글·야후재팬(Yahoo! JAPAN) 검색 싹쓸이용 '일본어 종목·테마별 정적 SEO 페이지 30종'(/jp/*.html) 생성,
각 페이지 2,500자 이상 고품질 일본어 애널리스트 리서치 칼럼 + 미니 ATR 손절·적정 주수 계산기(달러/엔화) + FAQPage JSON-LD 탑재,
sitemap.xml 자동 갱신 및 IndexNow 자동 색인 제출까지 수행합니다.
"""

import os
import sys
import json
import math
from datetime import datetime, timezone, timedelta

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
JP_DIR = os.path.join(ROOT_DIR, "jp")
SNAPSHOT_PATH = os.path.join(ROOT_DIR, "data", "live_market_snapshot.json")
SITEMAP_PATH = os.path.join(ROOT_DIR, "sitemap.xml")
INDEXNOW_KEY = "gba2026indexnowkey88429104"
INDEXNOW_KEY_FILE = os.path.join(ROOT_DIR, f"{INDEXNOW_KEY}.txt")

JST = timezone(timedelta(hours=9))

SEO_PAGES_SPEC = [
    {
        "slug": "nvda-sec-gamma-atr-analysis.html",
        "ticker": "NVDA",
        "jp_name": "エヌビディア(NVDA)",
        "title": "エヌビディア(NVDA) 決算・SEC開示・ガンマスクイーズAI解析とATR損切りライン",
        "focus": "次世代Blackwellデータセンター需要・ソブリンAI契約(SEC 8-K)・Call/Put比率3.2倍のGamma Wall突破",
        "catalyst_type": "決算ガイダンス上方修正 ＆ コールオプションGamma Squeeze",
        "entry": 186.64, "atr": 8.02, "iv": 68, "score": 93.5, "dp": "61.4%", "call_ratio": "3.2倍"
    },
    {
        "slug": "pltr-insider-buying-analysis.html",
        "ticker": "PLTR",
        "jp_name": "パランティア(PLTR)",
        "title": "パランティア(PLTR) SEC Form-4インサイダー動向・国防8-K契約とATR適正株数",
        "focus": "米国防総省(DoD)大型AI契約(SEC 8-K)・民間AIP導入加速・ダークプール機関投資家ブロック買い64%",
        "catalyst_type": "SEC Form 8-K 政府大型契約 ＆ 決算後ドリフト(PEAD)",
        "entry": 160.38, "atr": 9.95, "iv": 74, "score": 91.0, "dp": "64.2%", "call_ratio": "2.8倍"
    },
    {
        "slug": "tsla-gamma-wall-swing-trade.html",
        "ticker": "TSLA",
        "jp_name": "テスラ(TSLA)",
        "title": "テスラ(TSLA) オプションGamma Wall(GEX)・FSD触媒とスイング損切り戦略",
        "focus": "0DTE・週次コールオプション集積によるディーラー強制デルタヘッジ買い(Gamma Squeeze)とFSD・ロボタクシー触媒",
        "catalyst_type": "オプションGamma Flip突破 ＆ 短期モメンタム急騰",
        "entry": 358.22, "atr": 17.99, "iv": 82, "score": 89.7, "dp": "58.1%", "call_ratio": "3.6倍"
    },
    {
        "slug": "soxl-smh-semiconductor-timing.html",
        "ticker": "SOXL",
        "terminal_ticker": "NVDA",
        "jp_name": "SOXL・SMH (半導体ETF)",
        "title": "SOXL・SMH 半導体ETF3倍レバレッジのボラティリティ管理とATR撤退ルール",
        "title_short": "SOXL・SMH 半導体ETF 3倍レバレッジATR撤退ルール",
        "focus": "日本の米国株投資家に人気の半導体3倍ブルETF(SOXL)およびSMHにおける減価リスク回避・2.0x ATR機械的損切りとTruthOfMarket半導体恐怖強欲指数の併用術",
        "catalyst_type": "SOX指数サイクル転換 ＆ レバレッジETF資金管理",
        "entry": 34.50, "atr": 3.10, "iv": 98, "score": 88.0, "dp": "57.0%", "call_ratio": "2.9倍"
    },
    {
        "slug": "smci-accounting-risk-warning.html",
        "ticker": "SMCI",
        "jp_name": "スーパー・マイクロ(SMCI)",
        "title": "スーパー・マイクロ(SMCI) SEC会計リスク・ダークプール機関売り警告と回避基準",
        "focus": "SEC年次報告書(10-K)および監査法人関連のフォレンジック警告ワード検知・ダークプール67%機関売り抜け(Distribution)によるエントリー禁止判定",
        "catalyst_type": "🔴 エントリー禁止 / 会計監査リスク＆ダークプール機関売り警告",
        "entry": 28.76, "atr": 2.56, "iv": 96, "score": 28.5, "dp": "67.0% (売り越し)", "call_ratio": "0.4倍 (Put優勢)",
        "is_avoid": True
    },
    {
        "slug": "shin-nisa-us-stock-atr-risk-management.html",
        "ticker": "NVDA",
        "jp_name": "新NISA・米国株ATRリスク管理",
        "title": "新NISA成長投資枠で勝つ米国株ATR損切り＆ポジションサイジング完全ガイド",
        "focus": "新NISAの非課税枠を塩漬け株で潰さないための機関投資家式「口座1.5%リスク制限」「2.0x ATR損切りライン」「ドル・円同時ポジション計算」",
        "catalyst_type": "新NISA成長投資枠 資産防衛＆ATR資金管理フレームワーク",
        "entry": 186.64, "atr": 8.02, "iv": 68, "score": 93.5, "dp": "61.0%", "call_ratio": "3.0倍"
    },
    {
        "slug": "lly-form4-insider-cluster-buy.html",
        "ticker": "LLY",
        "jp_name": "イーライリリー(LLY)",
        "title": "イーライリリー(LLY) Form-4経営陣自社株買いクラスターと肥満症薬カタリスト",
        "focus": "CEO・CFOら経営中枢3名による自己資金$4.82M(約7.2億円)の市場内Form-4クラスター買いとGLP-1臨床パイプライン8-K解析",
        "catalyst_type": "SEC Form-4 経営陣キャッシュ買いクラスター",
        "entry": 1354.00, "atr": 52.81, "iv": 42, "score": 89.8, "dp": "54.0%", "call_ratio": "2.1倍"
    },
    {
        "slug": "avgo-custom-ai-asic-8k-analysis.html",
        "ticker": "AVGO",
        "jp_name": "ブロードコム(AVGO)",
        "title": "ブロードコム(AVGO) カスタムAI半導体(ASIC)受注8-Kと機関ダークプール解析",
        "focus": "ハイパースケーラー向けカスタムAIアクセラレータ(XPU)大型受注とVMwareソフトウェア統合によるFCF拡大",
        "catalyst_type": "SEC 8-K AIカスタムチップ受注 ＆ 機関投資家集積",
        "entry": 293.69, "atr": 15.14, "iv": 58, "score": 88.4, "dp": "59.0%", "call_ratio": "2.9倍"
    },
    {
        "slug": "amd-mi350-gamma-squeeze-target.html",
        "ticker": "AMD",
        "jp_name": "AMD(アドバンスト・マイクロ・デバイセズ)",
        "title": "AMD AI GPUシェア拡大・オプションGEX転換とATR損切り計算",
        "focus": "Instinct MIシリーズAI GPUのデータセンター売上上方修正と押し目でのコールスイープ集積",
        "catalyst_type": "データセンターAI増収ガイダンス ＆ コールGEX転換",
        "entry": 449.04, "atr": 38.02, "iv": 64, "score": 86.2, "dp": "57.2%", "call_ratio": "2.4倍"
    },
    {
        "slug": "meta-ai-capex-earnings-nlp.html",
        "ticker": "META",
        "jp_name": "メタ(META)",
        "title": "メタ(META) AI広告収益化・決算コールNLP強気スコアとGamma Wall解析",
        "focus": "Llama AIモデルによる広告ターゲティング単価(CPM)上昇と営業利益率拡大の決算トランスクリプトNLP解析",
        "catalyst_type": "決算カンファレンスコールNLP高スコア ＆ 自社株買い拡大",
        "entry": 610.15, "atr": 23.83, "iv": 48, "score": 87.9, "dp": "58.0%", "call_ratio": "2.5倍"
    },
    {
        "slug": "crwd-cybersecurity-pead-drift.html",
        "ticker": "CRWD",
        "jp_name": "クラウドストライク(CRWD)",
        "title": "クラウドストライク(CRWD) 決算後ドリフト(PEAD)と機関投資家オプション需給",
        "focus": "AIネイティブ・サイバーセキュリティFalconプラットフォームのARR拡大と決算後の継続上昇(PEAD)パターン",
        "catalyst_type": "サブスクリプションARR拡大 ＆ PEAD機関買い",
        "entry": 216.90, "atr": 14.76, "iv": 56, "score": 86.5, "dp": "56.4%", "call_ratio": "2.7倍"
    },
    {
        "slug": "vrt-ai-datacenter-cooling-catalyst.html",
        "ticker": "VRT",
        "jp_name": "バーティブ(VRT)",
        "title": "バーティブ(VRT) AIデータセンター液冷受注8-KとATRボラティリティ管理",
        "focus": "次世代GPUラックの高熱密度化に伴う液冷・電源管理インフラの受注残(Backlog)過去最高更新",
        "catalyst_type": "AIデータセンター液冷インフラ8-K ＆ GEXブレイク",
        "entry": 182.86, "atr": 18.81, "iv": 72, "score": 88.1, "dp": "60.1%", "call_ratio": "2.9倍"
    },
    {
        "slug": "ceg-nuclear-ai-power-8k-contract.html",
        "ticker": "CEG",
        "jp_name": "コンステレーション・エナジー(CEG)",
        "title": "コンステレーション・エナジー(CEG) AI原発電力契約(8-K)と機関買い追跡",
        "focus": "クラウド大手との20年長期原子力PPA（電力購入契約）8-K開示とAIデータセンター電力不足テーマの本命分析",
        "catalyst_type": "SEC Form 8-K 長期原子力電力契約(PPA)",
        "entry": 249.95, "atr": 12.02, "iv": 61, "score": 87.0, "dp": "55.3%", "call_ratio": "2.3倍"
    },
    {
        "slug": "mstr-bitcoin-volatility-atr-sizing.html",
        "ticker": "MSTR",
        "jp_name": "マイクロストラテジー(MSTR)",
        "title": "マイクロストラテジー(MSTR) 超高IV局面のATR損切り＆適正株数シミュレーター",
        "focus": "ビットコイン財務戦略8-Kとインプライド・ボラティリティ(IV)108%環境下での破産を防ぐ2.0x ATR株数計算",
        "catalyst_type": "超高IVコールGamma Squeeze ＆ 厳格ATR資金管理",
        "entry": 128.93, "atr": 9.75, "iv": 108, "score": 85.4, "dp": "53.2%", "call_ratio": "3.8倍"
    },
    {
        "slug": "arm-royalty-expansion-gamma-wall.html",
        "ticker": "ARM",
        "jp_name": "アーム(ARM)",
        "title": "アーム(ARM) v9ロイヤルティ成長・オプションGEX転換とスイング目標値",
        "focus": "Armv9アーキテクチャへの移行によるロイヤルティ料率倍増とデータセンターCPUシェア拡大",
        "catalyst_type": "ロイヤルティ単価上昇 ＆ 低浮動株Gamma Squeeze",
        "entry": 174.62, "atr": 14.23, "iv": 76, "score": 86.0, "dp": "56.0%", "call_ratio": "2.6倍"
    },
    {
        "slug": "asml-euv-orders-semiconductor-cycle.html",
        "ticker": "ASML",
        "jp_name": "ASMLホールディング(ASML)",
        "title": "ASMLホールディング EUV受注動向・半導体サイクル底打ちとATR資金管理",
        "focus": "2nm先端ロジックおよびHBMメモリ向けEUV露光装置の発注回復と欧州・米国機関投資家の底値集積",
        "catalyst_type": "EUV受注サイクル反転 ＆ ダークプール中長期買い",
        "entry": 1424.75, "atr": 71.38, "iv": 49, "score": 85.8, "dp": "58.4%", "call_ratio": "2.0倍"
    },
    {
        "slug": "unh-defensive-healthcare-insider-buy.html",
        "ticker": "UNH",
        "jp_name": "ユナイテッドヘルス(UNH)",
        "title": "ユナイテッドヘルス(UNH) ディフェンシブ医療株のインサイダー買いと安定運用",
        "focus": "ハイテク調整局面で輝く米国最大手ヘルスケア株のForm-4役員買いと低IV(34%)を活用した安定スイング戦略",
        "catalyst_type": "ディフェンシブForm-4役員買い ＆ 低ボラティリティ運用",
        "entry": 394.15, "atr": 11.98, "iv": 34, "score": 84.5, "dp": "52.1%", "call_ratio": "1.9倍"
    },
    {
        "slug": "msft-azure-ai-copilot-sec-8k.html",
        "ticker": "MSFT",
        "terminal_ticker": "NVDA",
        "jp_name": "マイクロソフト(MSFT)",
        "title": "マイクロソフト(MSFT) Azure AI成長率・SEC開示NLPと新NISAコア戦略",
        "focus": "AzureクラウドにおけるAI貢献度拡大とCopilot法人導入の決算コールNLP解析・低リスクATR押し目買い",
        "catalyst_type": "クラウドAI増収ガイダンス ＆ 機関コア保有",
        "entry": 448.20, "atr": 9.40, "iv": 32, "score": 88.5, "dp": "59.5%", "call_ratio": "2.2倍"
    },
    {
        "slug": "aapl-apple-intelligence-cycle-gex.html",
        "ticker": "AAPL",
        "terminal_ticker": "NVDA",
        "jp_name": "アップル(AAPL)",
        "title": "アップル(AAPL) Apple Intelligence買い替えサイクルとオプションGEX壁",
        "focus": "オンデバイスAI搭載iPhone買い替え需要・サービス部門粗利率70%超えと過去最大規模の自社株買いサポート",
        "catalyst_type": "自社株買い8-K下値支持 ＆ オプションCall Wall解析",
        "entry": 232.80, "atr": 4.90, "iv": 29, "score": 86.8, "dp": "55.8%", "call_ratio": "2.1倍"
    },
    {
        "slug": "amzn-aws-margin-expansion-pead.html",
        "ticker": "AMZN",
        "terminal_ticker": "NVDA",
        "jp_name": "アマゾン(AMZN)",
        "title": "アマゾン(AMZN) AWS営業利益率改善・決算後ドリフトとATRトレーリング",
        "focus": "AWS生成AIワークロード拡大と北米物流自動化による営業利益率の過去最高更新・機関ダークプール集積",
        "catalyst_type": "AWS利益率サプライズ ＆ 決算後ドリフト(PEAD)",
        "entry": 214.50, "atr": 5.30, "iv": 36, "score": 89.2, "dp": "60.2%", "call_ratio": "2.6倍"
    },
    {
        "slug": "googl-search-cloud-ai-valuation.html",
        "ticker": "GOOGL",
        "terminal_ticker": "NVDA",
        "jp_name": "アルファベット(GOOGL)",
        "title": "アルファベット(GOOGL) Cloud AI増収・自社株買いとGamma Wall分析",
        "focus": "Google Cloudの営業利益急伸とAI検索オーバービューの広告単価維持・割安PER水準からのGEX上値追い",
        "catalyst_type": "Cloud利益急伸 ＆ バリュエーション見直し買い",
        "entry": 188.40, "atr": 4.60, "iv": 35, "score": 87.4, "dp": "56.9%", "call_ratio": "2.3倍"
    },
    {
        "slug": "sec-8k-japanese-ai-guide.html",
        "ticker": "PLTR",
        "jp_name": "SEC Form 8-K 日本語AI解読ガイド",
        "title": "米国株SEC Form 8-Kとは？英語の適時開示をAIで3秒解読する実戦マニュアル",
        "focus": "日本の個人投資家が英語の壁で出遅れるSEC Form 8-K（重要契約・M&A・決算速報・役員異動）の項目番号(Item 1.01/2.02/4.01)の意味とAI即時解読法",
        "catalyst_type": "SEC適時開示(Form 8-K) 実践教育＆AI活用マニュアル",
        "entry": 160.38, "atr": 9.95, "iv": 74, "score": 91.0, "dp": "64.2%", "call_ratio": "2.8倍"
    },
    {
        "slug": "form4-insider-cluster-guide.html",
        "ticker": "LLY",
        "jp_name": "SEC Form-4 インサイダー買い完全ガイド",
        "title": "SEC Form-4インサイダー買いの見方：CEO・CFOの自腹買いクラスターで勝つ方法",
        "focus": "ストックオプション自動売却(10b5-1計画)のノイズを除去し、複数役員が自己資金で市場内購入(Transaction Code P)を行う「インサイダークラスター買い」だけを狙い撃つ手法",
        "catalyst_type": "SEC Form-4 内部者取引データ分析＆勝率向上メソッド",
        "entry": 1354.00, "atr": 52.81, "iv": 42, "score": 89.8, "dp": "54.0%", "call_ratio": "2.1倍"
    },
    {
        "slug": "options-gamma-squeeze-gex-guide.html",
        "ticker": "NVDA",
        "jp_name": "オプションGamma Squeeze(GEX)完全解説",
        "title": "オプションGamma Squeeze(GEX)完全解説：なぜコール集中で米国株は急騰するのか",
        "focus": "マーケットメイカー（オプション売り手）のデルタヘッジ義務が生み出す機械的な現物買い圧力（ガンマスクイーズ）とGamma Flip水準の見極め方",
        "catalyst_type": "オプション市場マイクロストラクチャー ＆ GEX実戦理論",
        "entry": 186.64, "atr": 8.02, "iv": 68, "score": 93.5, "dp": "61.4%", "call_ratio": "3.2倍"
    },
    {
        "slug": "fomc-cpi-iv-crush-strategy.html",
        "ticker": "TSLA",
        "jp_name": "決算またぎ＆FOMC・CPI IVクラッシュ対策",
        "title": "米国株決算またぎ＆FOMC・CPI前後のIVクラッシュ回避とATRポジション調整術",
        "focus": "イベント通過直後のインプライド・ボラティリティ急低下(IV Crush)と5日間予想変動幅(Expected Move)を使った安全なエントリー・利確タイミング",
        "catalyst_type": "マクロイベント・決算前後のボラティリティ制御戦略",
        "entry": 358.22, "atr": 17.99, "iv": 82, "score": 89.7, "dp": "58.1%", "call_ratio": "3.6倍"
    },
    {
        "slug": "tradingview-pine-script-v5-atr-guide.html",
        "ticker": "NVDA",
        "jp_name": "TradingView Pine Script v5 ATR損切り導入法",
        "title": "TradingView Pine Script v5で2.0x ATR損切りラインとGamma Wallを表示する方法",
        "focus": "GetBreakAI VIP特典のPine Script v5インジケーターをTradingViewチャートに導入し、2.0x ATRトレーリングストップと5日間IV上限壁を自動描画する手順",
        "catalyst_type": "TradingView チャート自動化 ＆ アラートWebhook連携",
        "entry": 186.64, "atr": 8.02, "iv": 68, "score": 93.5, "dp": "61.4%", "call_ratio": "3.2倍"
    },
    {
        "slug": "us-stock-stop-loss-2percent-rule.html",
        "ticker": "PLTR",
        "jp_name": "米国株「口座1.5%・2.0x ATR損切りルール」",
        "title": "米国株スイングで資産を守る「口座リスク1.5%・2.0x ATR損切りルール」の数学的証明",
        "focus": "なぜ一律「-5%損切り」はボラティリティの高い米国AI株で狩られやすいのか？銘柄ごとの14日ATRに合わせて購入株数を逆算する機関投資家の資金管理術",
        "catalyst_type": "ケリー基準・ボラティリティ調整型ポジションサイジング",
        "entry": 160.38, "atr": 9.95, "iv": 74, "score": 91.0, "dp": "64.2%", "call_ratio": "2.8倍"
    },
    {
        "slug": "dark-pool-whale-flow-reading.html",
        "ticker": "AVGO",
        "jp_name": "ダークプール(取引所外大口取引)解読術",
        "title": "ダークプール(取引所外ブロック取引)とは？機関投資家の隠れた買い集めを見抜く技術",
        "focus": "板情報（NYSE/NASDAQ）に自分の手口を見せたくない年金基金・ヘッジファンドが使うATS（ダークプール）比率60%超えシグナルの読み方",
        "catalyst_type": "オフエクスチェンジ・ブロック取引 ＆ 機関蓄積検知",
        "entry": 293.69, "atr": 15.14, "iv": 58, "score": 88.4, "dp": "59.0%", "call_ratio": "2.9倍"
    },
    {
        "slug": "ai-datacenter-power-stocks-2026.html",
        "ticker": "VRT",
        "jp_name": "AIデータセンター電力・冷却インフラ米国株比較",
        "title": "AIデータセンター電力・冷却インフラ関連米国株（VRT・CEG・AVGO）徹底比較",
        "title_short": "AIデータセンター電力・冷却インフラ米国株比較",
        "focus": "GPUの次に来るボトルネック「電力供給（原子力PPA）と液冷システム」で恩恵を受けるVRT・CEG・AVGOのSEC 8-K受注動向とATRリスクリワード比較",
        "catalyst_type": "AIインフラ第2波（電力・液冷・カスタムASIC）比較分析",
        "entry": 182.86, "atr": 18.81, "iv": 72, "score": 88.1, "dp": "60.1%", "call_ratio": "2.9倍"
    },
    {
        "slug": "semiconductor-cycle-truthofmarket-guide.html",
        "ticker": "NVDA",
        "jp_name": "TruthOfMarket × GetBreakAI 2大端末併用術",
        "title": "半導体サイクル投資×短期イベント投資：TruthOfMarketとGetBreakAIの最強併用術",
        "focus": "60日サイクルの半導体恐怖強欲指数・PW-RSI底値スクリーナー(TruthOfMarket.com)で相場環境を判定し、短期SEC開示・Gamma Squeeze・ATR計算機(GetBreakAI.com)で精密エントリーする二刀流戦略",
        "catalyst_type": "マクロサイクル配分 × 短期カタリスト精密執行シナジー",
        "entry": 186.64, "atr": 8.02, "iv": 68, "score": 93.5, "dp": "61.4%", "call_ratio": "3.2倍"
    }
]


def build_page_html(item, date_str, all_specs):
    slug = item["slug"]
    ticker = item["ticker"]
    term_ticker = item.get("terminal_ticker", ticker)
    jp_name = item["jp_name"]
    title = item["title"]
    focus = item["focus"]
    cat_type = item["catalyst_type"]
    entry = float(item["entry"])
    atr = float(item["atr"])
    iv = int(item["iv"])
    score = float(item["score"])
    dp = item["dp"]
    call_ratio = item["call_ratio"]
    is_avoid = item.get("is_avoid", False)

    stop_dist = round(atr * 2.0, 2)
    stop_loss = round(max(0.5, entry - stop_dist), 2)
    target_25r = round(entry + stop_dist * 2.5, 2)
    exp_move_5d = round(entry * (iv / 100.0) * math.sqrt(5.0 / 252.0), 2)
    upper_wall = round(entry + exp_move_5d, 2)
    gamma_flip = round(entry - atr * 0.85, 2)

    # Default $50,000 (約750万円) calculation
    default_acc = 50000
    max_risk = default_acc * 0.015  # $750
    shares = max(1, min(int(max_risk // stop_dist), int(default_acc // entry)))
    notional_usd = round(shares * entry)
    notional_jpy_man = round(notional_usd * 150 / 10000, 1)
    risk_usd = round(shares * stop_dist)
    risk_jpy_man = round(risk_usd * 150 / 10000, 1)
    gain_usd = round(shares * (target_25r - entry))
    gain_jpy_man = round(gain_usd * 150 / 10000, 1)

    canonical_url = f"https://getbreakai.com/jp/{slug}"

    banner_bg = "rgba(244,63,94,0.12)" if is_avoid else "#ecfdf5"
    banner_border = "rgba(244,63,94,0.45)" if is_avoid else "rgba(16,185,129,0.45)"
    banner_color = "#881337" if is_avoid else "#065f46"

    verdict_banner = (
        f"🔴 【AI緊急警告】{jp_name} は現在 AIカタリストスコア {score}/100（会計監査リスク・ダークプール機関売り {dp}）のため、新規買いエントリー禁止（DO NOT BUY / AVOID）と判定されています。"
        if is_avoid else
        f"🟢 【AI機関投資家シグナル】{jp_name} は AIカタリストスコア {score}/100（{cat_type}）を記録。$50,000（約750万円）口座での推奨購入株数は {shares}株（約{notional_jpy_man}万円）、2.0x ATR損切りラインは ${stop_loss:.2f}、2.5R利確ターゲットは ${target_25r:.2f} です。"
    )

    related_links_html = "\n".join([
        f'<li><a href="/jp/{s["slug"]}" style="color:#1d4ed8; text-decoration:none; font-weight:700;">📈 {s["title"]}</a></li>'
        for s in all_specs if s["slug"] != slug
    ][:10])

    return f"""<!DOCTYPE html>
<html lang="ja">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{title} | GetBreakAI 米国株・新NISA AIターミナル</title>
  <meta name="description" content="{jp_name}の{focus}をAIが日本語で徹底解読。現在値${entry:.2f}に対する2.0x ATR損切りライン(${stop_loss:.2f})、5日間オプションGamma Wall(${upper_wall:.2f})、ドル・円同時対応の適正株数計算機を掲載。">
  <link rel="canonical" href="{canonical_url}">
  <link rel="alternate" hreflang="ja" href="{canonical_url}">
  <meta property="og:type" content="article">
  <meta property="og:locale" content="ja_JP">
  <meta property="og:site_name" content="GetBreakAI 米国株AIターミナル">
  <meta property="og:url" content="{canonical_url}">
  <meta property="og:title" content="{title}">
  <meta property="og:description" content="{verdict_banner}">
  <meta property="og:image" content="https://getbreakai.com/og-preview.png">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="{title}">
  <meta name="twitter:description" content="{verdict_banner}">
  <meta name="twitter:image" content="https://getbreakai.com/og-preview.png">
  <link rel="icon" type="image/svg+xml" href="/favicon.svg">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;600;800&family=Noto+Sans+JP:wght@400;500;700;800;900&display=swap" rel="stylesheet">
  <script type="application/ld+json">
  {{
    "@context": "https://schema.org",
    "@graph": [
      {{
        "@type": "Article",
        "headline": "{title}",
        "description": "{verdict_banner}",
        "datePublished": "{date_str}",
        "dateModified": "{date_str}",
        "inLanguage": "ja",
        "author": {{
          "@type": "Organization",
          "name": "GetBreakAI Quantitative Research Desk",
          "url": "https://getbreakai.com/"
        }},
        "publisher": {{
          "@type": "Organization",
          "name": "Dream Company Quantitative Research",
          "logo": {{
            "@type": "ImageObject",
            "url": "https://getbreakai.com/og-preview.png"
          }}
        }},
        "mainEntityOfPage": "{canonical_url}"
      }},
      {{
        "@type": "FAQPage",
        "mainEntity": [
          {{
            "@type": "Question",
            "name": "{jp_name}の2.0x ATR損切りラインと推奨エントリー株数はいくらですか？",
            "acceptedAnswer": {{
              "@type": "Answer",
              "text": "米国市場最新データ（{date_str}時点・基準価格${entry:.2f}、14日ATR ${atr:.2f}）に基づくと、ノイズで刈られにくい2.0x ATR損切りラインは${stop_loss:.2f}（1株あたり-${stop_dist:.2f}）です。口座資金$50,000（約750万円）で1回の最大許容損失を1.5%（$750 / 約11.2万円）に抑える場合、推奨エントリー株数は{shares}株（投資額${notional_usd:,} / 約{notional_jpy_man}万円）となります。"
            }}
          }},
          {{
            "@type": "Question",
            "name": "{jp_name}のオプションGamma Wall（5日間IV予想変動幅）と利確ターゲットは？",
            "acceptedAnswer": {{
              "@type": "Answer",
              "text": "現在のオプションインプライド・ボラティリティ（IV {iv}%）から算出される5日間予想変動幅は±${exp_move_5d:.2f}であり、上値のGamma Wall（第一利確目標）は${upper_wall:.2f}、リスクリワード比1:2.5の本命利確ターゲット（2.5R）は${target_25r:.2f}です。"
            }}
          }},
          {{
            "@type": "Question",
            "name": "SEC 8-KやForm-4インサイダー買いデータはなぜ移動平均線より有効なのですか？",
            "acceptedAnswer": {{
              "@type": "Answer",
              "text": "移動平均線やMACDは過去の価格の平均値に過ぎませんが、SEC Form 8-K（重要契約・決算ガイダンス）やForm-4（経営陣による自己資金での市場内自社株買い）、およびダークプールブロック取引は、機関投資家が巨額資金を動かす直接のトリガー（一次情報）だからです。"
            }}
          }}
        ]
      }}
    ]
  }}
  </script>
  <script src="https://assets.lemonsqueezy.com/lemon.js" defer></script>
  <script>
  (function(){{
    try {{
      if (typeof window === 'undefined' || typeof navigator === 'undefined') return;
      var ua = navigator.userAgent || '';
      if (navigator.webdriver || /bot|crawl|spider|slurp|headless|python|curl|node/i.test(ua)) return;
      var host = (location && location.hostname) || '';
      if (!host || host === 'localhost' || host === '127.0.0.1') return;
      var kst = new Date(Date.now() + 9 * 3600 * 1000).toISOString().slice(0, 10);
      var ns = 'gba_getbreakai';
      fetch('https://abacus.jasoncameron.dev/hit/' + ns + '/pv_' + kst, {{ mode: 'cors', keepalive: true }}).catch(function(){{}});
      fetch('https://abacus.jasoncameron.dev/hit/' + ns + '/pv_total', {{ mode: 'cors', keepalive: true }}).catch(function(){{}});
      document.addEventListener('click', function(e) {{
        var el = e.target && e.target.closest ? e.target.closest('a, button') : null;
        if (!el) return;
        var href = (el.getAttribute('href') || '').toLowerCase();
        var txt = (el.innerText || el.textContent || '').toLowerCase();
        if (href.indexOf('lemonsqueezy.com') !== -1 || /\\$29|\\$199|pro|vip/.test(txt)) {{
          fetch('https://abacus.jasoncameron.dev/hit/' + ns + '/paid_click_' + kst, {{ mode: 'cors', keepalive: true }}).catch(function(){{}});
          fetch('https://abacus.jasoncameron.dev/hit/' + ns + '/paid_click_total', {{ mode: 'cors', keepalive: true }}).catch(function(){{}});
        }}
      }}, true);
    }} catch (e) {{}}
  }})();
  </script>
  <style>
    :root {{
      --bg-dark: #f4f6fa;
      --bg-card: #ffffff;
      --border-color: #cbd5e1;
      --border-accent: #93c5fd;
      --text-main: #0b1f3a;
      --text-muted: #334155;
      --text-sub: #475569;
      --accent-violet: #1d4ed8;
      --accent-amber: #b45309;
      --accent-emerald: #047857;
      --accent-rose: #be123c;
      --accent-sky: #0369a1;
      --font-sans: 'Noto Sans JP', -apple-system, BlinkMacSystemFont, sans-serif;
      --font-mono: 'JetBrains Mono', 'Noto Sans JP', monospace;
    }}
    * {{ box-sizing: border-box; margin: 0; padding: 0; }}
    body {{
      background: #f4f6fa;
      color: #0f172a;
      font-family: var(--font-sans);
      line-height: 1.75;
      font-size: 0.95rem;
      font-feature-settings: "palt" 1;
      letter-spacing: 0.01em;
      padding-bottom: 60px;
    }}
    .container {{ max-width: 960px; margin: 0 auto; padding: 0 20px; }}
    header {{
      background: #0b1f3a;
      border-bottom: 2px solid #1e3a8a;
      padding: 16px 0;
      position: sticky;
      top: 0;
      z-index: 50;
    }}
    .nav-bar {{ display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 12px; }}
    .brand {{ color: #f8fafc; font-weight: 900; font-size: 1.2rem; text-decoration: none; }}
    .nav-sublink {{ color: #e2e8f0; text-decoration: none; font-size: 0.86rem; padding: 8px; font-weight: 700; }}
    .btn-cta {{
      background: linear-gradient(135deg, #1d4ed8, #1e3a8a);
      color: #ffffff !important;
      text-decoration: none;
      padding: 9px 18px;
      border-radius: 8px;
      font-weight: 800;
      font-size: 0.86rem;
    }}
    .btn-cta-lg {{
      display: inline-block;
      padding: 13px 26px;
      font-size: 0.98rem;
    }}
    .shorts-bridge-bar {{
      background: #eff6ff;
      border: 1.5px solid #93c5fd;
      border-radius: 12px;
      padding: 10px 14px;
      margin-top: 18px;
      display: flex;
      align-items: center;
      justify-content: center;
      flex-wrap: wrap;
      gap: 8px;
      font-size: 0.82rem;
      color: #0f172a;
    }}
    .shorts-bridge-btn {{
      background: #1d4ed8;
      color: #ffffff !important;
      border: none;
      border-radius: 7px;
      padding: 6px 12px;
      font-weight: 800;
      font-size: 0.78rem;
      text-decoration: none;
      cursor: pointer;
    }}
    .shorts-bridge-sec {{
      background: #ecfdf5;
      color: #065f46 !important;
      border: 1px solid #10b981;
      border-radius: 7px;
      padding: 6px 12px;
      font-weight: 800;
      font-size: 0.78rem;
      text-decoration: none;
    }}
    .article-box {{
      background: #ffffff;
      border: 1.5px solid #cbd5e1;
      box-shadow: 0 8px 24px rgba(15,23,42,0.06);
      border-radius: 16px;
      padding: 32px;
      margin-top: 28px;
    }}
    h1 {{ font-size: clamp(1.5rem, 3.2vw, 2.15rem); line-height: 1.35; margin-bottom: 16px; font-weight: 900; color: #0b1f3a; }}
    h2 {{ font-size: 1.32rem; color: #1e3a8a; margin: 32px 0 12px; border-left: 5px solid #1d4ed8; background: #eff6ff; padding: 8px 12px; border-radius: 0 8px 8px 0; }}
    h3 {{ font-size: 1.08rem; color: #b45309; margin: 22px 0 8px; }}
    p, li {{ color: #1e293b; margin-bottom: 16px; font-size: 0.95rem; line-height: 1.75; }}
    .kpi-grid {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(195px, 1fr));
      gap: 12px;
      margin: 22px 0;
    }}
    .kpi-card {{
      background: #f8fafc;
      border: 1.5px solid #cbd5e1;
      border-radius: 10px;
      padding: 14px;
    }}
    .kpi-label {{ font-size: 0.75rem; color: #475569; font-weight: 700; font-family: var(--font-mono); }}
    .kpi-val {{ font-size: 1.22rem; font-weight: 800; font-family: var(--font-mono); margin-top: 4px; color: #0b1f3a; }}
    .widget-box {{
      background: #f8fafc;
      border: 2px solid #1d4ed8;
      border-radius: 14px;
      padding: 22px;
      margin: 26px 0;
    }}
    .widget-box h3 {{ color: #0b1f3a; }}
    .widget-box p {{ color: #334155; }}
    a {{ color: #1d4ed8; }}
    @media (max-width: 640px) {{
      .article-box {{ padding: 20px 16px; }}
    }}

    /* 日本証券ライト・高信頼テーマ (標準) */
    body {{ background: #f4f6fa !important; color: #0f172a !important; font-feature-settings: "palt" 1; }}
    header {{ background: #0b1f3a !important; border-bottom: 2px solid #1e3a8a !important; }}
    .article-box {{ background: #ffffff !important; border: 1.5px solid #cbd5e1 !important; box-shadow: 0 8px 24px rgba(15,23,42,0.06) !important; }}
    h1 {{ color: #0b1f3a !important; }}
    h2 {{ color: #1e3a8a !important; border-left: 5px solid #1d4ed8 !important; background: #eff6ff; padding: 8px 12px !important; border-radius: 0 8px 8px 0; }}
    h3 {{ color: #b45309 !important; }}
    p, li {{ color: #1e293b !important; }}
    .kpi-card {{ background: #f8fafc !important; border: 1.5px solid #cbd5e1 !important; }}
    .kpi-label {{ color: #475569 !important; font-weight: 700; }}
    .kpi-val {{ color: #0b1f3a !important; }}
    .widget-box {{ background: #f8fafc !important; border: 2px solid #1d4ed8 !important; }}
    .article-box div[style*="rgba(16,185,129"] {{ color: #065f46 !important; background: #ecfdf5 !important; }}
    .widget-box h3 {{ color: #0b1f3a !important; }}
    a {{ color: #1d4ed8; }}
  </style>
</head>
<body>
  <header>
    <div class="container nav-bar">
      <a href="https://getbreakai.com/" class="brand">⚡ GetBreakAI 米国株・新NISA AIターミナル</a>
      <div style="display:flex; gap:10px; flex-wrap:wrap; align-items:center;">
        <a href="https://www.youtube.com/@GetBreakAI" target="_blank" rel="noopener" class="nav-sublink">📺 公式YouTube (@GetBreakAI)</a>
        <a href="/jp/index.html" class="nav-sublink">📚 全30銘柄レポート一覧</a>
        <a href="https://getbreakai.com/?ticker={term_ticker}#radar" class="btn-cta">🎯 {jp_name}をメイン端末で起動 →</a>
      </div>
    </div>
  </header>

  <main class="container">
    <div class="shorts-bridge-bar">
      <strong>🎬 YouTubeショート(@GetBreakAI)からご訪問の方へ：</strong>
      <a href="#miniCalcBox" class="shorts-bridge-btn">⚡ 2.0x ATR 損切り＆新NISA手取り計算機へ直行</a>
      <a href="https://getbreakai.com/#gbQuickMatrixSection" class="shorts-bridge-sec">📊 本日のSEC 8-K・Form-4速報</a>
    </div>
    <article class="article-box">
      <div style="font-family:var(--font-mono); font-size:0.78rem; color:var(--accent-amber); font-weight:800; margin-bottom:8px;">
        🟢 米国市場最新データ反映 · {date_str} ｜ 対象銘柄・テーマ: {jp_name} (${ticker})
      </div>
      <h1>{title}</h1>
      <p style="font-size:1.02rem; font-weight:800; color:#1e3a8a; margin-bottom:14px;">
        ⚡ 新NISAの塩漬け損を防ぐため、あなたの資金に合う適正株数と撤退ラインを3秒で無料診断します。
      </p>
      <div style="background:{banner_bg}; border:1px solid {banner_border}; border-radius:10px; padding:14px 16px; margin-bottom:22px; color:{banner_color}; font-weight:700; font-size:0.93rem; line-height:1.65;">
        {verdict_banner}
      </div>

      <div class="kpi-grid">
        <div class="kpi-card">
          <div class="kpi-label">現在値 / 基準株価</div>
          <div class="kpi-val" style="color:#0b1f3a;">${entry:.2f} <span style="font-size:0.8rem; color:#475569; font-weight:700;">(約¥{int(round(entry*150)):,})</span></div>
        </div>
        <div class="kpi-card">
          <div class="kpi-label">AIカタリスト総合スコア</div>
          <div class="kpi-val" style="color:#1d4ed8;">{score} / 100</div>
        </div>
        <div class="kpi-card">
          <div class="kpi-label">2.0x ATR損切りライン</div>
          <div class="kpi-val" style="color:var(--accent-rose);">${stop_loss:.2f} <span style="font-size:0.78rem;">(-${stop_dist:.2f})</span></div>
        </div>
        <div class="kpi-card">
          <div class="kpi-label">2.5R 利確ターゲット</div>
          <div class="kpi-val" style="color:var(--accent-emerald);">${target_25r:.2f}</div>
        </div>
      </div>

      <!-- インタラクティブ・ミニATR損切り＆適正株数計算機 -->
      <div class="widget-box" id="miniCalcBox">
        <h3 style="margin-top:0; color:#0b1f3a;">🧮 {jp_name} 専用：ATR損切りライン＆適正株数ミニ計算機（ドル $ / 日本円 ¥ 同時換算）</h3>
        <p style="font-size:0.88rem; color:#334155; margin-bottom:14px;">
          ご自身の運用資金（スライダー）を動かすと、1回の最大損失を口座の1.5%以内に抑える「推奨エントリー株数」と「許容損失額（ドル・円）」がリアルタイムで計算されます。
        </p>
        <div style="margin-bottom:14px;">
          <div style="display:flex; justify-content:space-between; font-family:var(--font-mono); font-size:0.85rem; margin-bottom:6px; color:#334155;">
            <span>口座資金 (1ドル=150円換算):</span>
            <strong id="miniAccLbl" style="color:var(--accent-amber);">$50,000 (約750.0万円)</strong>
          </div>
          <input type="range" id="miniAccSlider" min="5000" max="250000" step="5000" value="50000" style="width:100%; accent-color:var(--accent-violet);" oninput="recalcMiniWidget()">
        </div>
        <div class="kpi-grid" style="margin:14px 0 0;">
          <div class="kpi-card">
            <div class="kpi-label">推奨エントリー株数</div>
            <div id="miniOutShares" class="kpi-val" style="color:var(--accent-amber);">{shares}株 (${notional_usd:,} / 約{notional_jpy_man}万円)</div>
          </div>
          <div class="kpi-card">
            <div class="kpi-label">2.0x ATR損切り時 許容損失額</div>
            <div id="miniOutRisk" class="kpi-val" style="color:var(--accent-rose);">-${risk_usd:,} (約{risk_jpy_man}万円)</div>
          </div>
          <div class="kpi-card">
            <div class="kpi-label">2.5R利確到達時 期待利益</div>
            <div id="miniOutGain" class="kpi-val" style="color:var(--accent-emerald);">+${gain_usd:,} (約{gain_jpy_man}万円)</div>
          </div>
        </div>
        <div style="margin-top:16px; display:flex; gap:10px; flex-wrap:wrap;">
          <a href="https://getbreakai.com/?ticker={term_ticker}#radar" class="btn-cta">⚡ フル機能ターミナルで ${ticker} を詳細シミュレーション →</a>
          <button type="button" onclick="shareMiniPageOnX()" style="background:#eff6ff; color:#0369a1; border:1px solid #93c5fd; padding:9px 16px; border-radius:8px; font-weight:800; cursor:pointer;">📤 X(Twitter)でこの記事とシグナルを共有</button>
        </div>
      </div>

      <h2>1. {jp_name} の最新SEC開示(8-K/10-K)＆決算コールNLP日本語解析</h2>
      <p>
        日本の新NISAおよび米国株スイング投資家が直面する最大の情報格差は、ウォール街の機関投資家がアルゴリズムで即座に読み解く<strong>「英語の一次開示情報（SEC Form 8-K・10-K・決算説明会トランスクリプト）」のスピード差</strong>にあります。{jp_name} における現在の最重要フォーカスは「<strong>{focus}</strong>」であり、GetBreakAIの自然言語処理(NLP)パイプラインはこのカタリストを<strong>{cat_type}（総合スコア {score}/100）</strong>として評価しています。
      </p>
      <p>
        一般的な日本語ニュースサイトやSNS（株クラ）に翻訳記事が出回る頃には、すでに時間外取引（アフターマーケット）や翌営業日の寄り付きで機関投資家の初期エントリーが完了しているケースが大半です。当ターミナルでは、経営陣がカンファレンスコールで使用するガイダンス表現の強弱、粗利率（Gross Margin）見通しの微細な変化、および受注残（Backlog）の定量ワードを3秒以内に数値化し、個人投資家が機関投資家と同じ土俵で判断できる環境を提供します。
      </p>

      <h2>2. SEC Form-4 インサイダー動向＆取引所外ダークプール({dp})の機関需給</h2>
      <p>
        チャート上のローソク足だけでは決して見えないのが、<strong>SEC Form-4（役員・大株主による自社株売買報告）</strong>と<strong>オフエクスチェンジ・ダークプール（取引所外ブロック取引）</strong>の実弾フローです。現在、{jp_name} のダークプール取引比率は <strong>{dp}</strong>、オプション市場におけるCall/Putスイープ比率は <strong>{call_ratio}</strong> を記録しています。
      </p>
      <p>
        ウォール街の年金基金やクオンツ・ヘッジファンドは、通常の取引所（NYSEやNASDAQの公開板）で巨額の買い注文を出すと自らの買いで株価が跳ね上がってしまうため、ダークプールを通じて水面下でブロック買いを進めます。ダークプール比率が55%〜60%を超え、同時にAsk側（売り板を直接叩く成行相当）のコールオプションスイープが流入している局面は、決算後の継続上昇（PEAD：Post-Earnings Announcement Drift）が発生する典型的な機関集積シグナルです。逆に、$SMCIのようにダークプールでの売り抜け（Distribution）と10-K会計リスクが重なる銘柄は、どれほど表面的なテーマ性が華やかであっても徹底してエントリーを回避（AVOID）することが資産防衛の鉄則となります。
      </p>

      <h2>3. オプションGamma Wall（GEX転換ライン ${gamma_flip:.2f}）と5日間IV予想変動幅（±${exp_move_5d:.2f}）</h2>
      <p>
        近年の米国株市場、特に{jp_name}のような流動性の高い主力ハイテク・グロース銘柄では、現物株の需給以上に<strong>オプション市場のガンマ・エクスポージャー（GEX：Gamma Exposure）</strong>が短期の値動きを支配しています。現在、{jp_name} のインプライド・ボラティリティ（IV）は <strong>{iv}%</strong> であり、ここから数学的に導かれる5営業日の予想変動幅（1標準偏差レンジ）は <strong>±${exp_move_5d:.2f}</strong> です。
      </p>
      <p>
        株価がディーラーの正ガンマ転換ラインである <strong>${gamma_flip:.2f}</strong> を上抜けると、コールオプションを大量に売っているマーケットメイカー（証券会社のオプションデスク）は、損失ヘッジのために株価が上がれば上がるほど機械的に現物株を買い増さなければならない「<strong>ガンマスクイーズ（踏み上げ）</strong>」の状態に追い込まれます。この強制買い圧力が最も集中する上値の壁（Upper Gamma Wall）が <strong>${upper_wall:.2f}</strong> であり、短期スイングトレードにおける極めて合理的な第一利確目標として機能します。
      </p>

      <h2>4. 塩漬けを完全撲滅する「2.0x ATR損切りライン（${stop_loss:.2f}）」とドル・円ポジション管理</h2>
      <p>
        新NISAの成長投資枠や特定口座で米国株を運用する際、最も避けなければならない失敗は「根拠のない一律パーセント損切り（例：どの銘柄も-5%で損切り）」または「損切りラインを決めずに含み損を放置する塩漬け」です。たとえば1日の平均値動き幅（14日ATR）が <strong>${atr:.2f}</strong> ある銘柄に対して浅すぎる逆指値を置けば、日常的なノイズ（ヒゲ）で簡単に刈られてしまいます。
      </p>
      <p>
        GetBreakAIが採用する機関投資家標準のアルゴリズムでは、<strong>現在値（${entry:.2f}）から14日ATRの2.0倍（${stop_dist:.2f}）を引いた「${stop_loss:.2f}」</strong>に損切りラインを設定します。そのうえで、万が一その損切りラインに到達しても<strong>口座資金全体の1.5%しか失わないように購入株数を逆算（口座$50,000＝約750万円なら {shares}株・投資額約{notional_jpy_man}万円）</strong>します。そして利確ターゲットは損切り幅の2.5倍（リスクリワード比 1:2.5）にあたる <strong>${target_25r:.2f}（期待利益 +${gain_usd:,} / 約{gain_jpy_man}万円）</strong>に置くことで、勝率が50%でも統計的に資産が右肩上がりで増え続けるクオンツ運用が完結します。
      </p>

      <h2>5. 姉妹端末 TruthOfMarket.com（半導体サイクル＆72銘柄PW-RSI）との二刀流シナジー</h2>
      <p>
        さらに勝率と資金効率を高めるために、1〜15日間のイベント・ガンマスクイーズ・ATR損切りを管理する当サイト <strong>GetBreakAI.com</strong> と、30〜90日間の半導体セクター恐怖強欲指数および米国株72銘柄のPW-RSI（出来高加重RSI）底値反転を捉える姉妹ターミナル <a href="https://truthofmarket.com/?utm_source=getbreakai_jp_seo&utm_medium={slug}" target="_blank" rel="noopener" style="color:var(--accent-sky); font-weight:700;">TruthOfMarket.com</a> を併用してください。<strong>Store #296100で発行されるProライセンスキー（月額 $29/月＝約4,400円、または年間VIPパス $199/年＝43%OFF・約29,800円/年）1つで、両方のサイトのWeb VIP Vault機能がすべてアンロックされます。</strong>
      </p>

      <div style="margin-top:32px; padding:24px; background:#eff6ff; border:2px solid #1d4ed8; border-radius:14px; text-align:center;">
        <h3 style="margin-top:0; color:#0b1f3a;">🚀 今すぐ {jp_name} の無料3秒シミュレーション＆VIP全機能を即時解放</h3>
        <p style="margin-bottom:16px; color:#334155;">1つのProキーで GetBreakAI.com と TruthOfMarket.com の両VIP機能（Pine Script v5全文・Form-4役員自社株買いCSV・全銘柄オーダーブック）を即時アンロックできます。</p>
        <div style="display:flex; justify-content:center; gap:10px; flex-wrap:wrap; margin-bottom:14px;">
          <a href="https://getbreakai.com/?ticker={term_ticker}#radar" class="btn-cta btn-cta-lg">📊 無料3秒ターミナルを開く（${ticker}） →</a>
          <a href="https://truthofmarket.lemonsqueezy.com/checkout/custom/f31a6c6c-6b09-409a-beaf-dd19a9eb2af9?signature=15f2b96765f5dfbce4def1891a4a99653a83e23f714b6f13a95d7134ee2041fe&amp;embed=1" data-ls-product-uuid="d5e7e761-8b1b-4ca8-b1fe-771acd1450f8" class="lemonsqueezy-button btn-cta btn-cta-lg" style="background:linear-gradient(135deg,#059669,#047857);">🔓 Monthly Pro を解放 ($29/月)</a>
          <a href="https://truthofmarket.lemonsqueezy.com/checkout/custom/19d14007-55e9-42e2-9f61-2dc3b75ac9b4?signature=a03c2e7ef03e726cc279e9b6978e3cfa0eb9edc82058f1068685d1171693f8ce&amp;embed=1" data-ls-product-uuid="667aa482-f17c-47d1-b7f3-a2427c36516b" class="lemonsqueezy-button btn-cta btn-cta-lg" style="background:linear-gradient(135deg,#d97706,#b45309);">💎 Annual Pro VIP 43%OFF ($199/年)</a>
        </div>
        <div style="font-size:0.8rem; color:#475569; line-height:1.6;">
          🔒 Stripe / Lemon Squeezy 安全決済（Apple Pay・Google Pay・JCB・Visa・Master 対応 / いつでも1クリック解約）<br>
          🏛️ 法人・金融メディア・クオンツAPIデータ提携デスク: <a href="mailto:beable9489@gmail.com?subject=GetBreakAI%20Japan%20B2B%20API%20%26%20Media%20Inquiry" style="color:#1d4ed8; font-weight:800;">beable9489@gmail.com</a>
        </div>
      </div>

      <h2>📚 関連する米国株・新NISA AI日本語ディープリサーチ記事</h2>
      <ul style="list-style:none; line-height:2.0; font-size:0.92rem;">
        {related_links_html}
      </ul>
    </article>
  </main>

  <script>
    const ENTRY_PRICE = {entry:.2f};
    const STOP_DIST = {stop_dist:.2f};
    const STOP_PRICE = {stop_loss:.2f};
    const TARGET_PRICE = {target_25r:.2f};
    const FX = 150.0;

    function recalcMiniWidget() {{
      const acc = parseFloat(document.getElementById('miniAccSlider').value) || 50000;
      const accJpyMan = (acc * FX / 10000).toFixed(1);
      document.getElementById('miniAccLbl').innerText = '$' + acc.toLocaleString() + ' (約' + accJpyMan + '万円)';
      const maxRisk = acc * 0.015;
      const shares = Math.max(1, Math.min(Math.floor(maxRisk / STOP_DIST), Math.floor(acc / ENTRY_PRICE)));
      const notional = Math.round(shares * ENTRY_PRICE);
      const notionalMan = (notional * FX / 10000).toFixed(1);
      const riskUsd = Math.round(shares * STOP_DIST);
      const riskMan = (riskUsd * FX / 10000).toFixed(1);
      const gainUsd = Math.round(shares * (TARGET_PRICE - ENTRY_PRICE));
      const gainMan = (gainUsd * FX / 10000).toFixed(1);

      document.getElementById('miniOutShares').innerText = shares + '株 ($' + notional.toLocaleString() + ' / 約' + notionalMan + '万円)';
      document.getElementById('miniOutRisk').innerText = '-$' + riskUsd.toLocaleString() + ' (約' + riskMan + '万円)';
      document.getElementById('miniOutGain').innerText = '+$' + gainUsd.toLocaleString() + ' (約' + gainMan + '万円)';
    }}

    function shareMiniPageOnX() {{
      const text = '【米国株AI解析】{title}\\n📊 基準値: $' + ENTRY_PRICE.toFixed(2) + ' / 2.0x ATR損切り: $' + STOP_PRICE.toFixed(2) + ' / 2.5R目標: $' + TARGET_PRICE.toFixed(2) + '\\n🔗 ' + '{canonical_url}' + '\\n#米国株 #新NISA #{ticker} #株クラ';
      window.open('https://twitter.com/intent/tweet?text=' + encodeURIComponent(text), '_blank', 'noopener,noreferrer');
    }}

    window.addEventListener('DOMContentLoaded', function() {{
      try {{
        if (window.location && window.location.search && new URLSearchParams(window.location.search).get('calc') === 'atr') {{
          const box = document.getElementById('miniCalcBox');
          if (box && box.scrollIntoView) box.scrollIntoView({{ behavior: 'smooth', block: 'start' }});
        }}
      }} catch (e) {{}}
    }});
  </script>
</body>
</html>
"""


def build_hub_html(date_str, all_specs):
    cards_html = "\n".join([
        f'<a href="/jp/{s["slug"]}" class="hub-seo-card">'
        f'<div class="hub-seo-meta">${s["ticker"]} · AIスコア {s["score"]}/100</div>'
        f'<div class="hub-seo-title">{s["title"]}</div>'
        f'<div class="hub-seo-focus">{s["focus"]}</div>'
        f'</a>'
        for s in all_specs
    ])
    return f"""<!DOCTYPE html>
<html lang="ja" data-jp-theme="light">
<head>
  <meta charset="UTF-8">
  <meta name="google-site-verification" content="lM2Bf7R0XRTUDg-IZvGV9i06u2Q5rz6HJ8-IwoLFcgo">
  <meta name="google-site-verification" content="nAGlJMEUUPifbzSd8X4PCaBIyr3DtTwaa1a-q9zkbBc">
  <meta name="google-site-verification" content="G99bl17UU6iKgNm5ndGcSWp0dHFpJ0MjJqBBp0Exfx0">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>新NISAの塩漬け・大損を1秒で防ぐ｜2.0x ATR損切り＆適正株数AI計算機 | GetBreakAI</title>
  <meta name="description" content="東証プライム（8035・6857・7011）＆米国株（NVDA・PLTR・MSFT・TSLA）対応。口座リスク1.5%上限で2.0x ATR損切りラインと適正購入株数・新NISA手取り利益を1秒算出。">
  <link rel="canonical" href="https://getbreakai.com/jp/">
  <meta property="og:type" content="website">
  <meta property="og:site_name" content="GetBreakAI">
  <meta property="og:title" content="新NISAの塩漬け・大損を1秒で防ぐ｜2.0x ATR損切り＆適正株数AI計算機 | GetBreakAI">
  <meta property="og:description" content="東証プライム（8035・6857・7011）＆米国株（NVDA・PLTR・MSFT・TSLA）対応。口座リスク1.5%上限で2.0x ATR損切りラインと適正購入株数・新NISA手取り利益を1秒算出。">
  <meta property="og:url" content="https://getbreakai.com/jp/">
  <meta property="og:image" content="https://getbreakai.com/og-preview.png">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="新NISAの塩漬け・大損を1秒で防ぐ｜2.0x ATR損切り＆適正株数AI計算機 | GetBreakAI">
  <meta name="twitter:description" content="東証プライム＆米国株対応。2.0x ATR損切りラインと新NISA適正株数を1秒算出。">
  <meta name="twitter:image" content="https://getbreakai.com/og-preview.png">
  <link rel="icon" type="image/svg+xml" href="/favicon.svg">
  <script src="https://assets.lemonsqueezy.com/lemon.js" defer></script>
  <script>
    window.CHECKOUT_URLS = {{
      monthly: 'https://truthofmarket.lemonsqueezy.com/checkout/custom/f31a6c6c-6b09-409a-beaf-dd19a9eb2af9?signature=15f2b96765f5dfbce4def1891a4a99653a83e23f714b6f13a95d7134ee2041fe&embed=1',
      annual: 'https://truthofmarket.lemonsqueezy.com/checkout/custom/19d14007-55e9-42e2-9f61-2dc3b75ac9b4?signature=a03c2e7ef03e726cc279e9b6978e3cfa0eb9edc82058f1068685d1171693f8ce&embed=1',
      enterprise: 'mailto:beable9489@gmail.com?subject=GetBreakAI%20Enterprise%20Inquiry'
    }};
    const CHECKOUT_URLS = window.CHECKOUT_URLS;
  </script>
  <style>
    :root, html[data-jp-theme="light"] {{
      --bg-page: #f4f6fa;
      --bg-card: #ffffff;
      --bg-sub: #f8fafc;
      --border-col: #cbd5e1;
      --text-main: #0b1f3a;
      --text-muted: #334155;
      --text-sub: #475569;
      --accent-blue: #1d4ed8;
      --accent-emerald: #065f46;
      --accent-rose: #9f1239;
      --accent-amber: #b45309;
    }}
    html[data-jp-theme="dark"] {{
      --bg-page: #070510;
      --bg-card: #120e24;
      --bg-sub: #1a1433;
      --border-col: #2d2352;
      --text-main: #f8fafc;
      --text-muted: #cbd5e1;
      --text-sub: #94a3b8;
      --accent-blue: #3b82f6;
      --accent-emerald: #34d399;
      --accent-rose: #fb7185;
      --accent-amber: #fbbf24;
    }}
    * {{ box-sizing: border-box; }}
    html, body {{ max-width: 100%; overflow-x: hidden; }}
    body {{
      background: var(--bg-page);
      color: var(--text-main);
      font-family: 'Noto Sans JP', -apple-system, BlinkMacSystemFont, sans-serif;
      line-height: 1.55;
      margin: 0;
      padding: 0 0 48px;
      font-feature-settings: "palt" 1;
    }}
    .container {{ max-width: 1080px; margin: 0 auto; padding: 10px 14px 24px; }}

    /* Compact 1-Row Top Navigation Bar */
    .top-nav {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      flex-wrap: nowrap;
      gap: 6px;
      border-bottom: 1px solid var(--border-col);
      padding-bottom: 8px;
      min-height: 44px;
    }}
    .brand-link {{
      color: var(--text-main);
      font-weight: 900;
      font-size: 1.0rem;
      text-decoration: none;
      display: inline-flex;
      align-items: center;
      gap: 4px;
      white-space: nowrap;
      flex-shrink: 0;
    }}
    .top-nav-actions {{
      display: flex;
      align-items: center;
      gap: 5px;
      flex-wrap: nowrap;
      flex-shrink: 0;
    }}
    .btn-top-main, .btn-top-yt, .btn-top-theme {{
      padding: 0 10px;
      border-radius: 7px;
      text-decoration: none;
      font-weight: 800;
      font-size: 0.76rem;
      min-height: 38px;
      display: inline-flex;
      align-items: center;
      justify-content: center;
      white-space: nowrap;
      flex-shrink: 0;
      cursor: pointer;
    }}
    .btn-top-main {{
      background: #1d4ed8;
      color: #ffffff;
      border: 1px solid #1e40af;
    }}
    .btn-top-yt {{
      background: var(--bg-sub);
      color: var(--accent-blue);
      border: 1px solid var(--border-col);
    }}
    .btn-top-theme {{
      background: #17325c;
      color: #fde68a;
      border: 1px solid #3b5998;
    }}

    /* Above-the-Fold Crisp B2C Hook (<=14 words) */
    .hero-title {{
      margin: 8px 0 8px;
      font-size: clamp(1.12rem, 2.8vw, 1.65rem);
      color: var(--text-main);
      font-weight: 900;
      line-height: 1.3;
    }}

    /* 1-Sec Cut-Loss & Shin-NISA Calculator Card */
    .calc-card {{
      background: var(--bg-card);
      border: 2px solid var(--accent-blue);
      border-radius: 12px;
      padding: 12px 14px;
      box-shadow: 0 8px 24px rgba(29, 78, 216, 0.08);
      margin-bottom: 20px;
    }}
    .calc-header {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      flex-wrap: wrap;
      gap: 6px;
      margin-bottom: 8px;
    }}
    .calc-title {{
      font-size: 0.92rem;
      font-weight: 900;
      color: var(--text-main);
    }}
    .calc-pill-risk {{
      background: rgba(16, 185, 129, 0.14);
      color: var(--accent-emerald);
      border: 1px solid rgba(16, 185, 129, 0.4);
      font-size: 0.7rem;
      font-weight: 800;
      padding: 2px 8px;
      border-radius: 6px;
    }}

    /* Compact 3-Input Row + Tax Toggle + Calculate CTA (Above-the-Fold y < 320px!) */
    .calc-fast-inputs {{
      display: grid;
      grid-template-columns: repeat(3, minmax(0, 1fr));
      gap: 6px;
      margin-bottom: 8px;
    }}
    .fast-field {{
      background: var(--bg-sub);
      border: 1px solid var(--border-col);
      border-radius: 8px;
      padding: 5px 7px;
    }}
    .fast-field label {{
      display: block;
      font-size: 0.66rem;
      font-weight: 800;
      color: var(--text-sub);
      margin-bottom: 2px;
      white-space: nowrap;
      overflow: hidden;
      text-overflow: ellipsis;
    }}
    .fast-field input {{
      width: 100%;
      border: 1px solid var(--border-col);
      border-radius: 5px;
      background: var(--bg-card);
      color: var(--text-main);
      font-family: monospace;
      font-size: 0.86rem;
      font-weight: 800;
      padding: 4px 6px;
      min-height: 30px;
    }}
    .tax-calc-bar {{
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 6px;
      margin-bottom: 8px;
    }}
    .tax-mode-btn {{
      background: var(--bg-sub);
      border: 1px solid var(--border-col);
      color: var(--text-main);
      border-radius: 7px;
      min-height: 38px;
      padding: 4px 8px;
      font-size: 0.74rem;
      font-weight: 800;
      cursor: pointer;
      display: inline-flex;
      align-items: center;
      justify-content: center;
      text-align: center;
    }}
    .tax-mode-btn.active {{
      background: #1d4ed8;
      color: #ffffff;
      border-color: #1e40af;
    }}
    .btn-calc-submit {{
      width: 100%;
      min-height: 44px;
      background: linear-gradient(135deg, #1d4ed8, #4f46e5);
      color: #ffffff;
      border: none;
      border-radius: 9px;
      font-size: 0.88rem;
      font-weight: 900;
      cursor: pointer;
      display: inline-flex;
      align-items: center;
      justify-content: center;
      gap: 6px;
      box-shadow: 0 4px 14px rgba(29, 78, 216, 0.25);
      margin-bottom: 10px;
    }}

    /* 3 Result Output Cards */
    .calc-outputs {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
      gap: 8px;
      margin-bottom: 10px;
    }}
    .out-card {{
      background: var(--bg-sub);
      border: 1.5px solid var(--border-col);
      border-radius: 9px;
      padding: 9px 11px;
    }}
    .out-label {{
      font-size: 0.72rem;
      font-weight: 700;
      color: var(--text-sub);
      margin-bottom: 2px;
    }}
    .out-val {{
      font-size: 1.02rem;
      font-weight: 900;
      font-family: monospace;
    }}
    .val-emerald {{ color: var(--accent-emerald); }}
    .val-rose {{ color: var(--accent-rose); }}
    .val-amber {{ color: var(--accent-amber); }}

    /* Slider & Preset Bars */
    .slider-group {{
      background: var(--bg-sub);
      border: 1px solid var(--border-col);
      border-radius: 9px;
      padding: 8px 10px;
      margin-bottom: 10px;
    }}
    .slider-header {{
      display: flex;
      justify-content: space-between;
      flex-wrap: wrap;
      gap: 4px;
      font-size: 0.76rem;
      color: var(--text-muted);
      font-weight: 700;
      margin-bottom: 4px;
    }}
    .slider-header strong {{
      color: var(--accent-amber);
      font-family: monospace;
      font-size: 0.84rem;
    }}
    input[type=range] {{
      width: 100%;
      height: 28px;
      accent-color: #1d4ed8;
      cursor: pointer;
      margin: 0;
    }}
    .capital-pills, .preset-bar {{
      display: flex;
      gap: 6px;
      flex-wrap: wrap;
      margin-top: 6px;
    }}
    .cap-btn, .preset-chip {{
      background: var(--bg-card);
      border: 1px solid var(--border-col);
      color: var(--text-main);
      padding: 6px 9px;
      border-radius: 7px;
      font-size: 0.74rem;
      font-weight: 800;
      cursor: pointer;
      min-height: 40px;
      max-width: 100%;
      display: inline-flex;
      align-items: center;
      justify-content: center;
    }}
    .cap-btn.active, .preset-chip.active {{
      background: #1d4ed8;
      color: #ffffff;
      border-color: #1e40af;
    }}

    /* Defense Comparison Card */
    .defense-card {{
      background: var(--bg-card);
      border: 1.5px solid var(--border-col);
      border-radius: 14px;
      padding: 18px 14px;
      margin-bottom: 20px;
    }}
    .defense-title {{
      font-size: 1.04rem;
      font-weight: 900;
      color: var(--text-main);
      margin-bottom: 6px;
      line-height: 1.4;
    }}
    .defense-subtitle {{
      font-size: 0.84rem;
      color: var(--text-sub);
      margin-bottom: 14px;
    }}
    .comp-grid {{
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 12px;
      margin-bottom: 16px;
    }}
    .box-bad {{
      background: rgba(244, 63, 94, 0.08);
      border: 1.5px solid rgba(244, 63, 94, 0.35);
      border-radius: 10px;
      padding: 14px;
    }}
    .box-bad h4 {{ color: var(--accent-rose); font-size: 0.9rem; margin: 0 0 6px; font-weight: 900; }}
    .box-bad .loss-num {{ font-size: 1.35rem; font-weight: 900; color: var(--accent-rose); font-family: monospace; }}
    .box-good {{
      background: rgba(16, 185, 129, 0.08);
      border: 2px solid rgba(16, 185, 129, 0.45);
      border-radius: 10px;
      padding: 14px;
    }}
    .box-good h4 {{ color: var(--accent-emerald); font-size: 0.9rem; margin: 0 0 6px; font-weight: 900; }}
    .box-good .gain-num {{ font-size: 1.35rem; font-weight: 900; color: var(--accent-emerald); font-family: monospace; }}

    /* Checkout CTA */
    .cta-container {{ text-align: center; margin-top: 12px; }}
    .cta-dual-grid {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
      gap: 10px;
    }}
    .btn-checkout-primary, .btn-checkout-annual {{
      color: #ffffff !important;
      text-decoration: none;
      padding: 13px 16px;
      border-radius: 10px;
      font-size: 0.92rem;
      font-weight: 900;
      display: flex;
      align-items: center;
      justify-content: center;
      width: 100%;
      text-align: center;
      min-height: 48px;
    }}
    .btn-checkout-primary {{ background: linear-gradient(135deg, #1d4ed8, #1e3a8a); }}
    .btn-checkout-annual {{ background: linear-gradient(135deg, #065f46, #047857); }}
    .cta-subnote {{ font-size: 0.76rem; color: var(--text-muted); margin-top: 10px; line-height: 1.5; }}

    /* Web VIP Vault Card */
    .vip-vault-card {{
      background: var(--bg-card);
      border: 1.5px solid var(--border-col);
      border-radius: 14px;
      padding: 16px 14px;
      margin-bottom: 22px;
    }}
    .vip-input-row {{
      display: flex;
      gap: 8px;
      flex-wrap: wrap;
      margin-top: 10px;
    }}
    .vip-key-input {{
      flex: 1;
      min-width: 160px;
      max-width: 100%;
      padding: 10px 12px;
      border: 1.5px solid var(--border-col);
      border-radius: 8px;
      font-family: monospace;
      font-size: 0.85rem;
      color: var(--text-main);
      background: var(--bg-sub);
    }}
    .vip-unlock-btn {{
      background: #0b1f3a;
      color: #ffffff;
      border: 1px solid #334155;
      border-radius: 8px;
      padding: 10px 16px;
      font-weight: 800;
      font-size: 0.85rem;
      cursor: pointer;
      min-height: 44px;
      white-space: nowrap;
    }}

    /* 30 Research Articles Grid */
    .grid {{
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
      gap: 14px;
      margin-top: 16px;
    }}
    .hub-seo-card {{
      display: block;
      background: var(--bg-card);
      border: 1.5px solid var(--border-col);
      border-radius: 12px;
      padding: 16px;
      color: var(--text-main);
      text-decoration: none;
      transition: all 0.18s ease;
    }}
    .hub-seo-card:hover {{
      border-color: var(--accent-blue);
      transform: translateY(-2px);
    }}
    .hub-seo-meta {{ font-family: monospace; font-size: 0.75rem; color: var(--accent-amber); font-weight: 700; margin-bottom: 4px; }}
    .hub-seo-title {{ font-weight: 800; font-size: 0.95rem; margin-bottom: 6px; color: var(--text-main); }}
    .hub-seo-focus {{ font-size: 0.83rem; color: var(--text-sub); line-height: 1.55; }}

    @media (max-width: 640px) {{
      .container {{ padding: 6px 12px 24px; }}
      .brand-link {{ font-size: 0.9rem; }}
      .btn-top-main, .btn-top-yt, .btn-top-theme {{ padding: 0 7px; font-size: 0.7rem; min-height: 36px; }}
      .hero-title {{ font-size: 1.05rem; margin: 6px 0 6px; line-height: 1.28; }}
      .calc-card {{ padding: 10px 10px; }}
      .calc-header {{ margin-bottom: 6px; }}
      .calc-title {{ font-size: 0.84rem; }}
      .comp-grid, .cta-dual-grid {{ grid-template-columns: 1fr; }}
      .vip-unlock-btn {{ width: 100%; }}
      .grid {{ grid-template-columns: 1fr; }}
    }}
  </style>
</head>
<body>
  <div class="container">
    <!-- Consolidated Single-Row Top Navigation Bar -->
    <nav class="top-nav" aria-label="日本株・米国株ナビゲーション">
      <a href="/" class="brand-link">⚡ GetBreakAI</a>
      <div class="top-nav-actions">
        <a href="/" class="btn-top-main">🏠 トップ画面へ</a>
        <a href="https://www.youtube.com/@GetBreakAI" target="_blank" rel="noopener" class="btn-top-yt">📺 公式YouTube</a>
        <button type="button" id="btnToggleJpTheme" onclick="toggleJpTheme()" class="btn-top-theme">🌙 切替</button>
      </div>
    </nav>

    <!-- Crisp Intuitive B2C Headline (<=14 words, Above-the-Fold) -->
    <h1 class="hero-title">
      新NISAの塩漬け・大損を1秒で防ぐ。2.0x ATR損切り＆適正株数計算機
    </h1>

    <!-- ⚡ 1秒 損切り・適正株数 ＆ 新NISA手取り計算機 (Inputs + Calculate Button Above-the-Fold y < 320px) -->
    <div class="calc-card" id="jpQuickCalcSection">
      <div class="calc-header">
        <div class="calc-title">⚡ 1秒 ATR損切り＆新NISA株数計算 (<span id="jpActiveSymBadge">$NVDA</span>)</div>
        <div class="calc-pill-risk">🛡️ 口座リスク1.5%上限</div>
      </div>

      <div class="calc-fast-inputs">
        <div class="fast-field">
          <label for="jpCapManInput">口座資金 (万円)</label>
          <input type="number" id="jpCapManInput" min="10" max="10000" step="10" value="750" oninput="syncCapFromManInput()">
        </div>
        <div class="fast-field">
          <label for="jpPriceInput">現在株価 <span id="lblPriceUnit">($)</span></label>
          <input type="number" id="jpPriceInput" min="0.1" step="any" value="162.85" oninput="syncPriceAtrInputs()">
        </div>
        <div class="fast-field">
          <label for="jpAtrInput">14日ATR <span id="lblAtrUnit">($)</span></label>
          <input type="number" id="jpAtrInput" min="0.05" step="any" value="10.01" oninput="syncPriceAtrInputs()">
        </div>
      </div>

      <div class="tax-calc-bar">
        <button type="button" id="btnJpHubTaxNisa" class="tax-mode-btn active" onclick="setJpHubTaxMode('nisa')">🌱 新NISA (非課税 0%)</button>
        <button type="button" id="btnJpHubTaxTokutei" class="tax-mode-btn" onclick="setJpHubTaxMode('tokutei')">🏦 特定口座 (税 20.315%)</button>
      </div>

      <button type="button" id="btnJpHubCalcNow" class="btn-calc-submit" onclick="recalcJpQuickCalc()">
        🧮 1秒で損切りライン＆適正株数を計算
      </button>

      <!-- 3 Real-time Outputs -->
      <div class="calc-outputs">
        <div class="out-card">
          <div class="out-label">推奨エントリー株数 (適正ポジション)</div>
          <div id="jpOutShares" class="out-val val-amber">37株 ($6,025 / 約90.4万円)</div>
        </div>
        <div class="out-card">
          <div class="out-label">🛑 2.0x ATR損切りライン / 許容損失額</div>
          <div id="jpOutRisk" class="out-val val-rose">$142.83 (-$741 / -約11.1万円)</div>
        </div>
        <div class="out-card">
          <div class="out-label" id="jpOutGainLabel">🎯 2.5R利確目標 / 新NISA非課税手取り</div>
          <div id="jpOutGain" class="out-val val-emerald">$212.90 (+$1,852 / +約27.8万円)</div>
        </div>
      </div>

      <!-- Capital Slider & Presets -->
      <div class="slider-group">
        <div class="slider-header">
          <span>運用資金スライダー（1ドル=150円基準）:</span>
          <strong id="jpCalcAccLbl">$50,000 (約750.0万円)</strong>
        </div>
        <input type="range" id="jpCalcSlider" min="5000" max="250000" step="1000" value="50000" oninput="syncManFromSlider()">
        <div class="capital-pills">
          <button type="button" class="cap-btn" onclick="setQuickCapital(6700, this)">100万円</button>
          <button type="button" class="cap-btn" onclick="setQuickCapital(20000, this)">300万円</button>
          <button type="button" class="cap-btn" onclick="setQuickCapital(33300, this)">500万円</button>
          <button type="button" class="cap-btn active" onclick="setQuickCapital(50000, this)">750万円</button>
          <button type="button" class="cap-btn" onclick="setQuickCapital(66700, this)">1,000万円</button>
          <button type="button" class="cap-btn" onclick="setQuickCapital(80000, this)">1,200万円 (新NISA枠)</button>
        </div>
      </div>

      <!-- Quick Ticker Presets (TSE Prime ¥ & US Tech $) -->
      <div style="font-size:0.74rem; font-weight:800; color:var(--text-sub); margin-bottom:4px;">
        👇 東証プライム(¥)・米国株($) ワンタップ銘柄切替:
      </div>
      <div class="preset-bar">
        <button type="button" class="preset-chip active" data-ticker="NVDA" onclick="setQuickStock('NVDA', this)">$NVDA エヌビディア</button>
        <button type="button" class="preset-chip" data-ticker="PLTR" onclick="setQuickStock('PLTR', this)">$PLTR パランティア</button>
        <button type="button" class="preset-chip" data-ticker="MSFT" onclick="setQuickStock('MSFT', this)">$MSFT マイクロソフト</button>
        <button type="button" class="preset-chip" data-ticker="TSLA" onclick="setQuickStock('TSLA', this)">$TSLA テスラ</button>
        <button type="button" class="preset-chip" data-ticker="SOXL" onclick="setQuickStock('SOXL', this)">$SOXL (半導体3倍)</button>
        <button type="button" class="preset-chip" data-ticker="AAPL" onclick="setQuickStock('AAPL', this)">$AAPL アップル</button>
        <button type="button" class="preset-chip" data-ticker="8035" onclick="setQuickStock('8035', this)">8035.T 東エレク (¥)</button>
        <button type="button" class="preset-chip" data-ticker="6857" onclick="setQuickStock('6857', this)">6857.T アドテスト (¥)</button>
        <button type="button" class="preset-chip" data-ticker="7011" onclick="setQuickStock('7011', this)">7011.T 三菱重工 (¥)</button>
        <button type="button" class="preset-chip" data-ticker="9984" onclick="setQuickStock('9984', this)">9984.T ソフトバンクG (¥)</button>
        <button type="button" class="preset-chip" data-ticker="7203" onclick="setQuickStock('7203', this)">7203.T トヨタ (¥)</button>
        <button type="button" class="preset-chip" data-ticker="8306" onclick="setQuickStock('8306', this)">8306.T 三菱UFJ (¥)</button>
        <button type="button" class="preset-chip" data-ticker="8058" onclick="setQuickStock('8058', this)">8058.T 三菱商事 (¥)</button>
      </div>
    </div>

    <!-- 🛡️ $29/mo & $199/yr (43%OFF) 防衛比較カード -->
    <div class="defense-card">
      <div class="defense-title">
        🛡️ なぜ月額$29/月（年間VIP $199/年・43%OFF）は「コスト」ではなく「圧倒的な資産防衛」なのか？
      </div>
      <div class="defense-subtitle">
        感情に任せて1回損切りに失敗しただけで失う金額 vs クオンツ防衛ツール費用の比較
      </div>

      <div class="comp-grid">
        <div class="box-bad">
          <h4>❌ 自己流トレード（損切り遅れ・塩漬けの結末）</h4>
          <div class="loss-num">-¥185,000</div>
          <p style="font-size:0.82rem; color:var(--text-muted); line-height:1.55; margin:6px 0 0;">
            「そのうち戻るだろう」とホールドし、-20%〜-30%の致命的大損に拡大。新NISAの非課税枠が凍結されます。
          </p>
        </div>

        <div class="box-good">
          <h4>✅ GetBreakAI クオンツ防衛（$29/月 または $199/年 43%OFF）</h4>
          <div class="gain-num">+¥170,000 防衛</div>
          <p style="font-size:0.82rem; color:var(--text-muted); line-height:1.55; margin:6px 0 0;">
            2.0x ATRで許容損失を機械的ロック！1回のトレードで <b>差額 +¥170,000 の自己資金を守り抜き、3.5年分の費用を即回収</b> します。
          </p>
        </div>
      </div>

      <!-- Checkout CTA Buttons (Lemon Squeezy Store #296100 Live UUIDs) -->
      <div class="cta-container">
        <div class="cta-dual-grid">
          <a href="https://truthofmarket.lemonsqueezy.com/checkout/custom/f31a6c6c-6b09-409a-beaf-dd19a9eb2af9?signature=15f2b96765f5dfbce4def1891a4a99653a83e23f714b6f13a95d7134ee2041fe&amp;embed=1" data-ls-product-uuid="d5e7e761-8b1b-4ca8-b1fe-771acd1450f8" class="btn-checkout-primary lemonsqueezy-button">
            ⚡ 月額プラン $29/月 (約4,350円) で始める →
          </a>
          <a href="https://truthofmarket.lemonsqueezy.com/checkout/custom/19d14007-55e9-42e2-9f61-2dc3b75ac9b4?signature=a03c2e7ef03e726cc279e9b6978e3cfa0eb9edc82058f1068685d1171693f8ce&amp;embed=1" data-ls-product-uuid="667aa482-f17c-47d1-b7f3-a2427c36516b" class="btn-checkout-annual lemonsqueezy-button">
            👑 年間VIPパス $199/年 (43%OFF・約29,800円) →
          </a>
        </div>
        <div class="cta-subnote">
          🔒 Lemon Squeezy Store #296100 安全決済（🍎 Apple Pay・Google Pay・JCB・Visa・Master・PayPal 対応 / いつでも1クリック解約可能）<br>
          🎁 <b>購入特典</b>：姉妹ターミナル <b>TruthOfMarket.com</b> のVIP権限も同時付与！法人・API契約：<a href="mailto:beable9489@gmail.com?subject=GetBreakAI%20Enterprise%20Inquiry" style="color:var(--accent-blue); font-weight:800;">beable9489@gmail.com</a>
        </div>
      </div>
    </div>

    <!-- 🔐 Web VIP Vault & 公式Web/SNS配信ハブ -->
    <div class="vip-vault-card" id="jpHubVipVaultBox">
      <div style="font-size:1.0rem; font-weight:900; color:var(--text-main);">
        🔐 Web VIP Vault ライセンスキー即時認証（全ページ共通連動）
      </div>
      <p style="font-size:0.83rem; color:var(--text-muted); margin:6px 0 8px;">
        決済完了メールに記載された Lemon Squeezy ライセンスキーを入力すると、当ページおよびトップページのVIP特典が一括でアンロックされます。
      </p>
      <div class="vip-input-row">
        <input type="text" id="jpHubLicenseInput" class="vip-key-input" placeholder="ライセンスキーを入力 (XXXX-XXXX-XXXX-XXXX)">
        <button type="button" id="btnJpHubUnlockVip" class="vip-unlock-btn" onclick="unlockJpHubVipVault()">🔑 VIPロック解除</button>
      </div>
      <div id="jpHubVipStatus" style="font-size:0.82rem; font-weight:700; margin-top:8px; color:var(--accent-emerald);"></div>
      <div style="display:flex; gap:10px; flex-wrap:wrap; margin-top:12px; font-size:0.8rem;">
        <a href="https://www.youtube.com/@GetBreakAI" target="_blank" rel="noopener" style="color:var(--accent-blue); font-weight:800; text-decoration:none;">📺 公式YouTube (@GetBreakAI)</a>
        <a href="https://getbreakai.com/#gbQuickMatrixSection" style="color:var(--accent-emerald); font-weight:800; text-decoration:none;">📊 本日の日米ブレイク銘柄早見表 →</a>
      </div>
    </div>

    <!-- 📚 30選ディープリサーチ記事一覧 -->
    <div style="border-top:1px solid var(--border-col); padding-top:20px; margin-top:16px;">
      <h2 style="font-size:1.3rem; color:var(--text-main); margin-bottom:6px;">📚 米国株・新NISA 銘柄別AI日本語ディープリサーチ全30選（{date_str} 最新版）</h2>
      <p style="color:var(--text-muted); font-size:0.86rem; margin-bottom:14px;">SEC 8-K決算・契約開示、Form-4経営陣インサイダー買い、オプションGamma Wall(GEX)、2.0x ATR損切りライン＆適正株数を完全網羅。</p>
      <div class="grid">
        {cards_html}
      </div>
    </div>
  </div>

  <!-- Client-side Interactive Calculation & Theme Script -->
  <script>
    const FX_RATE = 150.0;
    let activeSym = 'NVDA';
    let activeCurrency = 'USD';
    let activePrice = 162.85;
    let activeAtr = 10.01;
    let jpHubTaxMode = 'nisa';

    const PRESET_STOCK_MAP = {{
      'NVDA': {{ price: 162.85, atr: 10.01, currency: 'USD', label: '$NVDA' }},
      'PLTR': {{ price: 167.99, atr: 8.84,  currency: 'USD', label: '$PLTR' }},
      'MSFT': {{ price: 523.88, atr: 15.20, currency: 'USD', label: '$MSFT' }},
      'TSLA': {{ price: 390.22, atr: 16.71, currency: 'USD', label: '$TSLA' }},
      'SOXL': {{ price: 58.32,  atr: 12.72, currency: 'USD', label: '$SOXL' }},
      'AAPL': {{ price: 356.27, atr: 8.21,  currency: 'USD', label: '$AAPL' }},
      '8035': {{ price: 9461.0, atr: 597.2, currency: 'JPY', label: '8035.T 東エレク' }},
      '6857': {{ price: 30610.0, atr: 2599.2, currency: 'JPY', label: '6857.T アドテスト' }},
      '7011': {{ price: 2920.5, atr: 128.4, currency: 'JPY', label: '7011.T 三菱重工' }},
      '9984': {{ price: 3547.0, atr: 358.4, currency: 'JPY', label: '9984.T ソフトバンクG' }},
      '7203': {{ price: 3418.0, atr: 101.0, currency: 'JPY', label: '7203.T トヨタ' }},
      '8306': {{ price: 3475.0, atr: 111.0, currency: 'JPY', label: '8306.T 三菱UFJ' }},
      '8058': {{ price: 5405.0, atr: 171.4, currency: 'JPY', label: '8058.T 三菱商事' }}
    }};

    function toggleJpTheme() {{
      const root = document.documentElement;
      const cur = root.getAttribute('data-jp-theme') || 'light';
      const next = cur === 'light' ? 'dark' : 'light';
      root.setAttribute('data-jp-theme', next);
      try {{ localStorage.setItem('gb_jp_theme', next); }} catch (_) {{}}
      const btn = document.getElementById('btnToggleJpTheme');
      if (btn) btn.innerText = next === 'light' ? '🌙 切替' : '☀️ 切替';
    }}

    function setJpHubTaxMode(mode) {{
      jpHubTaxMode = mode === 'tokutei' ? 'tokutei' : 'nisa';
      const bN = document.getElementById('btnJpHubTaxNisa');
      const bT = document.getElementById('btnJpHubTaxTokutei');
      if (bN) bN.classList.toggle('active', jpHubTaxMode === 'nisa');
      if (bT) bT.classList.toggle('active', jpHubTaxMode === 'tokutei');
      recalcJpQuickCalc();
    }}

    function setQuickStock(ticker, btnEl) {{
      const clean = String(ticker || '').toUpperCase().replace(/\\.T$/i, '');
      const item = PRESET_STOCK_MAP[clean];
      if (!item) return;
      activeSym = clean;
      activeCurrency = item.currency;
      activePrice = item.price;
      activeAtr = item.atr;

      document.querySelectorAll('.preset-chip').forEach(b => {{
        b.classList.toggle('active', b === btnEl || b.getAttribute('data-ticker') === clean);
      }});

      const pIn = document.getElementById('jpPriceInput');
      const aIn = document.getElementById('jpAtrInput');
      const pUnit = document.getElementById('lblPriceUnit');
      const aUnit = document.getElementById('lblAtrUnit');
      const badge = document.getElementById('jpActiveSymBadge');
      if (pIn) pIn.value = activeCurrency === 'JPY' ? Math.round(activePrice * 10) / 10 : activePrice.toFixed(2);
      if (aIn) aIn.value = activeCurrency === 'JPY' ? Math.round(activeAtr * 10) / 10 : activeAtr.toFixed(2);
      if (pUnit) pUnit.innerText = activeCurrency === 'JPY' ? '(¥)' : '($)';
      if (aUnit) aUnit.innerText = activeCurrency === 'JPY' ? '(¥)' : '($)';
      if (badge) badge.innerText = item.label;
      recalcJpQuickCalc();
    }}

    function syncCapFromManInput() {{
      const manEl = document.getElementById('jpCapManInput');
      const manVal = Math.max(10, parseFloat(manEl ? manEl.value : 750) || 750);
      const usdVal = Math.round((manVal * 10000) / FX_RATE);
      const slider = document.getElementById('jpCalcSlider');
      if (slider) slider.value = Math.min(250000, Math.max(5000, usdVal));
      recalcJpQuickCalc(manVal * 10000);
    }}

    function syncManFromSlider() {{
      const slider = document.getElementById('jpCalcSlider');
      const accUsd = parseFloat(slider ? slider.value : 50000) || 50000;
      const manEl = document.getElementById('jpCapManInput');
      if (manEl) manEl.value = Math.round((accUsd * FX_RATE) / 10000);
      recalcJpQuickCalc(accUsd * FX_RATE);
    }}

    function syncPriceAtrInputs() {{
      const pIn = document.getElementById('jpPriceInput');
      const aIn = document.getElementById('jpAtrInput');
      const p = parseFloat(pIn ? pIn.value : activePrice);
      const a = parseFloat(aIn ? aIn.value : activeAtr);
      if (p > 0) activePrice = p;
      if (a > 0) activeAtr = a;
      recalcJpQuickCalc();
    }}

    function setQuickCapital(usdVal, btnEl) {{
      document.querySelectorAll('.cap-btn').forEach(b => b.classList.remove('active'));
      if (btnEl) btnEl.classList.add('active');
      const slider = document.getElementById('jpCalcSlider');
      if (slider) slider.value = usdVal;
      const manEl = document.getElementById('jpCapManInput');
      if (manEl) manEl.value = Math.round((usdVal * FX_RATE) / 10000);
      recalcJpQuickCalc(usdVal * FX_RATE);
    }}

    function recalcJpQuickCalc(overrideJpyCap) {{
      const manEl = document.getElementById('jpCapManInput');
      const capJpy = overrideJpyCap || ((Math.max(10, parseFloat(manEl ? manEl.value : 750) || 750)) * 10000);
      const accUsd = Math.round(capJpy / FX_RATE);
      const accJpyMan = (capJpy / 10000).toFixed(1);
      const accLbl = document.getElementById('jpCalcAccLbl');
      if (accLbl) accLbl.innerText = '$' + accUsd.toLocaleString() + ' (約' + accJpyMan + '万円)';

      const isTokutei = (jpHubTaxMode === 'tokutei');
      const taxRate = 0.20315;
      const outShares = document.getElementById('jpOutShares');
      const outRisk = document.getElementById('jpOutRisk');
      const outGain = document.getElementById('jpOutGain');
      const outGainLbl = document.getElementById('jpOutGainLabel');
      if (outGainLbl) {{
        outGainLbl.innerText = isTokutei
          ? '🎯 2.5R利確目標 / 特定口座(税引後)手取り'
          : '🎯 2.5R利確目標 / 新NISA(非課税)手取り';
      }}

      if (activeCurrency === 'JPY') {{
        const stopDist = Math.max(1, activeAtr * 2.0);
        const maxRiskJpy = capJpy * 0.015;
        const shares = Math.max(1, Math.min(Math.floor(maxRiskJpy / stopDist), Math.floor(capJpy / activePrice)));
        const notionalJpy = Math.round(shares * activePrice);
        const stopPrice = Math.max(1, activePrice - stopDist);
        const riskJpy = Math.round(shares * stopDist);
        const targetPrice = activePrice + stopDist * 2.5;
        const grossGainJpy = Math.round(shares * (targetPrice - activePrice));
        const netGainJpy = isTokutei ? Math.round(grossGainJpy * (1 - taxRate)) : grossGainJpy;

        if (outShares) outShares.innerText = shares + '株 (¥' + notionalJpy.toLocaleString() + ' / 約' + (notionalJpy / 10000).toFixed(1) + '万円)';
        if (outRisk) outRisk.innerText = '¥' + Math.round(stopPrice).toLocaleString() + ' (-¥' + riskJpy.toLocaleString() + ' / -約' + (riskJpy / 10000).toFixed(1) + '万円)';
        if (outGain) outGain.innerText = '¥' + Math.round(targetPrice).toLocaleString() + ' (+¥' + netGainJpy.toLocaleString() + ' / +約' + (netGainJpy / 10000).toFixed(1) + '万円)';
      }} else {{
        const stopDist = Math.max(0.05, activeAtr * 2.0);
        const maxRiskUsd = accUsd * 0.015;
        const shares = Math.max(1, Math.min(Math.floor(maxRiskUsd / stopDist), Math.floor(accUsd / activePrice)));
        const notionalUsd = Math.round(shares * activePrice);
        const stopPrice = Math.max(0.01, activePrice - stopDist);
        const riskUsd = Math.round(shares * stopDist);
        const targetPrice = activePrice + stopDist * 2.5;
        const grossGainUsd = shares * (targetPrice - activePrice);
        const netGainUsd = isTokutei ? (grossGainUsd * (1 - taxRate)) : grossGainUsd;
        const netGainMan = ((netGainUsd * FX_RATE) / 10000).toFixed(1);

        if (outShares) outShares.innerText = shares + '株 ($' + notionalUsd.toLocaleString() + ' / 約' + (notionalUsd * FX_RATE / 10000).toFixed(1) + '万円)';
        if (outRisk) outRisk.innerText = '$' + stopPrice.toFixed(2) + ' (-$' + riskUsd.toLocaleString() + ' / -約' + (riskUsd * FX_RATE / 10000).toFixed(1) + '万円)';
        if (outGain) outGain.innerText = '$' + targetPrice.toFixed(2) + ' (+$' + Math.round(netGainUsd).toLocaleString() + ' / +約' + netGainMan + '万円)';
      }}
    }}

    window.addEventListener('DOMContentLoaded', function() {{
      try {{
        const savedTheme = localStorage.getItem('gb_jp_theme');
        if (savedTheme === 'dark' || savedTheme === 'light') {{
          document.documentElement.setAttribute('data-jp-theme', savedTheme);
          const btn = document.getElementById('btnToggleJpTheme');
          if (btn) btn.innerText = savedTheme === 'light' ? '🌙 切替' : '☀️ 切替';
        }}
      }} catch (_) {{}}

      try {{
        const qTicker = (new URLSearchParams(window.location.search || '').get('ticker') || '').toUpperCase().replace(/\\.T$/i, '');
        if (qTicker && PRESET_STOCK_MAP[qTicker]) {{
          setQuickStock(qTicker);
          return;
        }}
      }} catch (_) {{}}
      recalcJpQuickCalc();
    }});
  </script>

  <!-- Web VIP Vault Unified License Sync & Live Snapshot Sync -->
  <script>
    function syncStoredVipKeysOnHub() {{
      try {{
        const k1 = String(localStorage.getItem('gb_vip_license_key') || '').trim();
        const k2 = String(localStorage.getItem('gb_vip_key') || '').trim();
        const key = k1 || k2;
        if (key && key.length >= 12) {{
          localStorage.setItem('gb_vip_unlocked', 'true');
          if (k1 !== key) localStorage.setItem('gb_vip_license_key', key);
          if (k2 !== key) localStorage.setItem('gb_vip_key', key);
          const inp = document.getElementById('jpHubLicenseInput');
          const statusEl = document.getElementById('jpHubVipStatus');
          if (inp && !inp.value) inp.value = key;
          if (statusEl) {{
            statusEl.style.color = 'var(--accent-emerald)';
            statusEl.innerText = '👑 VIPライセンス認証済みです！トップページおよび全ページのWeb VIP Vault特典が有効化されています。';
          }}
        }}
      }} catch (_) {{}}
    }}

    async function unlockJpHubVipVault() {{
      const inp = document.getElementById('jpHubLicenseInput');
      const statusEl = document.getElementById('jpHubVipStatus');
      const key = (inp ? inp.value : '').trim();
      if (!key || key.length < 8) {{
        if (statusEl) {{
          statusEl.style.color = 'var(--accent-rose)';
          statusEl.innerText = '⚠️ 有効なLemon Squeezyライセンスキーを入力してください。';
        }}
        return;
      }}
      if (statusEl) {{
        statusEl.style.color = 'var(--accent-blue)';
        statusEl.innerText = '🔄 ライセンス認証サーバー（Store #296100）に照会中...';
      }}
      try {{
        const valRes = await fetch('https://api.lemonsqueezy.com/v1/licenses/validate', {{
          method: 'POST',
          headers: {{ 'Accept': 'application/json', 'Content-Type': 'application/x-www-form-urlencoded' }},
          body: new URLSearchParams({{ license_key: key }})
        }});
        let data = await valRes.json().catch(() => ({{}}));
        const licStatus = data && data.license_key ? data.license_key.status : '';
        const actUsage = data && data.license_key ? Number(data.license_key.activations_usage || 0) : -1;
        const storeOk = !data.meta || Number(data.meta.store_id) === 296100;

        if (storeOk && (!data.valid || licStatus === 'inactive' || actUsage === 0)) {{
          const actRes = await fetch('https://api.lemonsqueezy.com/v1/licenses/activate', {{
            method: 'POST',
            headers: {{ 'Accept': 'application/json', 'Content-Type': 'application/x-www-form-urlencoded' }},
            body: new URLSearchParams({{ license_key: key, instance_name: 'GetBreakAI-Web-Terminal' }})
          }});
          const actData = await actRes.json().catch(() => ({{}}));
          if (actData && (actData.activated || (actData.license_key && actData.license_key.status === 'active'))) {{
            data = {{ valid: true, meta: actData.meta, license_key: actData.license_key }};
          }}
        }}

        if (data && data.valid && (!data.meta || Number(data.meta.store_id) === 296100)) {{
          try {{
            localStorage.setItem('gb_vip_unlocked', 'true');
            localStorage.setItem('gb_vip_license_key', key);
            localStorage.setItem('gb_vip_key', key);
          }} catch (e) {{}}
          if (statusEl) {{
            statusEl.style.color = 'var(--accent-emerald)';
            statusEl.innerText = '✅ VIP認証が完了しました！メインターミナルのWeb VIP Vaultへ移動します...';
          }}
          setTimeout(function() {{
            window.location.href = '/?unlock=1#vip-vault';
          }}, 900);
        }} else {{
          if (statusEl) {{
            statusEl.style.color = 'var(--accent-rose)';
            statusEl.innerText = '❌ ライセンスキーが確認できませんでした。メール記載のキーをご確認のうえ再度お試しください。';
          }}
        }}
      }} catch (err) {{
        if (statusEl) {{
          statusEl.style.color = 'var(--accent-rose)';
          statusEl.innerText = '⚠️ 通信エラーが発生しました。通信環境をご確認のうえ再度お試しください。';
        }}
      }}
    }}

    window.addEventListener('DOMContentLoaded', function() {{
      syncStoredVipKeysOnHub();

      (async function syncSameOriginPrices() {{
        try {{
          const snapRes = await fetch('/data/live_market_snapshot.json', {{ cache: 'no-store' }});
          if (snapRes.ok) {{
            const snap = await snapRes.json();
            const tMap = snap.tickers || {{}};
            Object.keys(PRESET_STOCK_MAP).forEach(function(k) {{
              const item = tMap[k] || tMap[k + '.T'];
              if (item && item.entry > 0) {{
                PRESET_STOCK_MAP[k].price = Number(item.entry);
                if (item.atr > 0) PRESET_STOCK_MAP[k].atr = Number(item.atr);
                PRESET_STOCK_MAP[k].currency = item.currency === 'JPY' ? 'JPY' : 'USD';
              }}
            }});
            if (PRESET_STOCK_MAP[activeSym]) {{
              setQuickStock(activeSym);
            }}
          }}
        }} catch (e) {{}}
      }})();
    }});
  </script>
</body>
</html>
"""


def main():
    os.makedirs(JP_DIR, exist_ok=True)
    now_jst = datetime.now(JST)
    date_str = now_jst.strftime("%Y-%m-%d")

    # Sync live prices from snapshot if available
    if os.path.exists(SNAPSHOT_PATH):
        try:
            snap = json.load(open(SNAPSHOT_PATH, "r", encoding="utf-8"))
            date_str = snap.get("updated_date", date_str)
            live_tickers = snap.get("tickers", {})
            for item in SEO_PAGES_SPEC:
                sym = item["ticker"]
                if sym in live_tickers and item["slug"] != "soxl-smh-semiconductor-timing.html":
                    item["entry"] = live_tickers[sym]["entry"]
                    item["atr"] = live_tickers[sym]["atr"]
        except Exception as e:
            print(f"[WARN] Could not merge live snapshot into SEO specs: {e}")

    urls = ["https://getbreakai.com/", "https://getbreakai.com/jp/index.html"]
    min_chars = 999999

    for spec in SEO_PAGES_SPEC:
        html = build_page_html(spec, date_str, SEO_PAGES_SPEC)
        out_file = os.path.join(JP_DIR, spec["slug"])
        with open(out_file, "w", encoding="utf-8") as f:
            f.write(html)
        # Count visible text length
        import re
        text_only = re.sub(r"<script[\s\S]*?</script>|<style[\s\S]*?</style>|<[^>]+>", "", html)
        text_len = len(text_only.strip())
        min_chars = min(min_chars, text_len)
        urls.append(f"https://getbreakai.com/jp/{spec['slug']}")

    hub_html = build_hub_html(date_str, SEO_PAGES_SPEC)
    with open(os.path.join(JP_DIR, "index.html"), "w", encoding="utf-8") as f:
        f.write(hub_html)

    print(f"[OK] Generated {len(SEO_PAGES_SPEC)} Japanese SEO pages + /jp/index.html hub (min visible text length: {min_chars} chars)")

    # Write sitemap.xml
    sitemap_entries = []
    for i, u in enumerate(urls):
        prio = "1.0" if i == 0 else ("0.9" if i == 1 else "0.85")
        sitemap_entries.append(
            f"  <url>\n    <loc>{u}</loc>\n    <lastmod>{date_str}</lastmod>\n    <changefreq>daily</changefreq>\n    <priority>{prio}</priority>\n  </url>"
        )
    sitemap_xml = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + "\n".join(sitemap_entries) + "\n</urlset>\n"
    with open(SITEMAP_PATH, "w", encoding="utf-8") as f:
        f.write(sitemap_xml)
    print(f"[OK] Updated {SITEMAP_PATH} with {len(urls)} URLs")

    # Write IndexNow key file
    with open(INDEXNOW_KEY_FILE, "w", encoding="utf-8") as f:
        f.write(INDEXNOW_KEY)

    # Ping IndexNow API (when --ping-indexnow is passed)
    if "--ping-indexnow" in sys.argv:
        try:
            import requests
            payload = {
                "host": "getbreakai.com",
                "key": INDEXNOW_KEY,
                "keyLocation": f"https://getbreakai.com/{INDEXNOW_KEY}.txt",
                "urlList": urls,
            }
            resp = requests.post("https://api.indexnow.org/indexnow", json=payload, timeout=8)
            print(f"[OK] IndexNow ping submitted for {len(urls)} URLs -> HTTP {resp.status_code}")
        except Exception as e:
            print(f"[WARN] IndexNow ping skipped/deferred: {e}")


if __name__ == "__main__":
    main()
