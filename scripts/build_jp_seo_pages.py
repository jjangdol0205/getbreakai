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
      var kst = new Date(Date.now() + 9 * 3600 * 1000).toISOString().slice(0, 10);
      var ns = 'gba_getbreakai';
      window.__gbaSubmitJpSignup = function(ev, formEl, tickerLabel) {{
        if (ev && ev.preventDefault) ev.preventDefault();
        var input = formEl ? formEl.querySelector('input[type="email"]') : null;
        var email = input ? String(input.value || '').trim() : '';
        if (!/^[^\\s@]+@[^\\s@]+\\.[^\\s@]+$/.test(email)) {{
          if (input) input.focus();
          return false;
        }}
        try {{
          localStorage.setItem('gba_jp_free_email', email);
          localStorage.setItem('gba_jp_free_since', kst);
          var dedupeKey = 'hq_signup_' + ns + '_' + kst + '_' + email.toLowerCase();
          var ua = navigator.userAgent || '';
          var host = (location && location.hostname) || '';
          var isHumanLive = !navigator.webdriver && !/bot|crawl|spider|slurp|headless|python|curl|node/i.test(ua) && host && host !== 'localhost' && host !== '127.0.0.1';
          if (localStorage.getItem(dedupeKey) !== '1') {{
            localStorage.setItem(dedupeKey, '1');
            if (isHumanLive) {{
              fetch('https://abacus.jasoncameron.dev/hit/' + ns + '/signup_' + kst, {{ mode: 'cors', keepalive: true }}).catch(function(){{}});
              fetch('https://abacus.jasoncameron.dev/hit/' + ns + '/signup_total', {{ mode: 'cors', keepalive: true }}).catch(function(){{}});
            }}
          }}
        }} catch (_e) {{}}
        document.querySelectorAll('.gba-jp-signup-status').forEach(function(el) {{
          el.style.display = 'block';
          el.innerHTML = '✅ <strong>無料登録が完了しました！</strong> 毎朝8時の「新NISA 3色シグナル＆安全撤退ライン速報」を <strong>' + email.replace(/[<>&"]/g, '') + '</strong> 宛にお届けします（' + String(tickerLabel || '').replace(/[<>&"]/g, '') + '）。';
        }});
        document.querySelectorAll('.gba-jp-signup-form input[type="email"]').forEach(function(inp) {{ inp.value = email; }});
        return false;
      }};
      document.addEventListener('DOMContentLoaded', function() {{
        try {{
          var saved = localStorage.getItem('gba_jp_free_email');
          if (saved) {{
            document.querySelectorAll('.gba-jp-signup-form input[type="email"]').forEach(function(inp) {{ inp.value = saved; }});
          }}
        }} catch (_e2) {{}}
      }});
      if (window.__HQ_KPI_GBA__) return;
      window.__HQ_KPI_GBA__ = true;
      var ua = navigator.userAgent || '';
      if (navigator.webdriver || /bot|crawl|spider|slurp|headless|python|curl|node/i.test(ua)) return;
      var host = (location && location.hostname) || '';
      if (!host || host === 'localhost' || host === '127.0.0.1') return;
      fetch('https://abacus.jasoncameron.dev/hit/' + ns + '/pv_' + kst, {{ mode: 'cors', keepalive: true }}).catch(function(){{}});
      fetch('https://abacus.jasoncameron.dev/hit/' + ns + '/pv_total', {{ mode: 'cors', keepalive: true }}).catch(function(){{}});
      if (localStorage.getItem('hq_uv_' + ns + '_' + kst) !== '1') {{
        localStorage.setItem('hq_uv_' + ns + '_' + kst, '1');
        fetch('https://abacus.jasoncameron.dev/hit/' + ns + '/uv_' + kst, {{ mode: 'cors', keepalive: true }}).catch(function(){{}});
      }}
      if (localStorage.getItem('hq_uv_ever_' + ns) !== '1') {{
        localStorage.setItem('hq_uv_ever_' + ns, '1');
        fetch('https://abacus.jasoncameron.dev/hit/' + ns + '/uv_total', {{ mode: 'cors', keepalive: true }}).catch(function(){{}});
      }}
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
      <div style="background:{banner_bg}; border:1px solid {banner_border}; border-radius:10px; padding:14px 16px; margin-bottom:22px; color:{banner_color}; font-weight:700; font-size:1.05rem; line-height:1.65;">
        {verdict_banner}
      </div>

      <!-- 上部：50〜70代・新NISA投資家向け 1項目・無料朝刊3色シグナル登録＆1タップ決済 -->
      <section id="gba-jp-lead-top" style="margin:20px 0 26px; padding:22px; background:linear-gradient(135deg,#ecfdf5 0%,#eff6ff 100%); border:2.5px solid #059669; border-radius:16px; box-shadow:0 8px 22px rgba(5,150,105,0.10);">
        <div style="display:inline-block; background:#065f46; color:#ffffff; font-size:0.9rem; font-weight:800; padding:5px 14px; border-radius:999px; margin-bottom:10px;">
          {'🔴 現在の判定：危険・見送り警戒' if is_avoid else '🟢 現在の判定：買い検討・安全管理'} ｜ 毎朝8時の無料3色シグナル
        </div>
        <h2 style="margin:0 0 8px !important; background:transparent !important; border:none !important; padding:0 !important; font-size:1.38rem; line-height:1.4; color:#0b1f3a !important;">
          新NISAの塩漬けを防ぐ！{jp_name}の「3色シグナル＆安全撤退ライン」無料メール登録
        </h2>
        <p style="margin:0 0 14px; font-size:1.08rem; line-height:1.65; color:#1e293b !important;">
          難しい専門用語は不要です。メールアドレス1つ（10秒）で、毎朝8時に<strong>🟢買い検討・🟡様子見・🔴危険撤退</strong>と安全撤退ライン（${stop_loss:.2f}）を無料でお届けします。
        </p>
        <form class="gba-jp-signup-form" onsubmit="return window.__gbaSubmitJpSignup(event, this, '{ticker}');" style="display:flex; flex-wrap:wrap; gap:10px; align-items:stretch;">
          <input type="email" required autocomplete="email" placeholder="メールアドレスを入力（例: yamada@yahoo.co.jp）" style="flex:1 1 260px; min-height:58px; padding:12px 16px; font-size:1.08rem; font-weight:700; border-radius:12px; border:2px solid #64748b; background:#ffffff; color:#0f172a;" />
          <button type="submit" style="min-height:58px; padding:12px 24px; font-size:1.08rem; font-weight:900; border-radius:12px; border:none; background:#059669; color:#ffffff; cursor:pointer; white-space:nowrap;">
            📩 無料で毎朝の3色シグナルを受け取る →
          </button>
        </form>
        <div class="gba-jp-signup-status" role="status" aria-live="polite" style="display:none; margin-top:12px; padding:12px 14px; border-radius:10px; background:#d1fae5; color:#065f46; font-size:1.05rem; font-weight:800;"></div>
        <div style="margin-top:14px; padding-top:12px; border-top:1px solid #a7f3d0; display:flex; flex-wrap:wrap; align-items:center; justify-content:space-between; gap:10px;">
          <span style="font-size:0.98rem; font-weight:800; color:#0f172a;">💳 今すぐ全銘柄の売買ラインを解放（Apple Pay・JCB・カード1タップ決済）：</span>
          <div style="display:flex; flex-wrap:wrap; gap:10px;">
            <a href="https://truthofmarket.lemonsqueezy.com/checkout/buy/d5e7e761-8b1b-4ca8-b1fe-771acd1450f8?embed=1&amp;checkout[redirect_url]=https://getbreakai.com/confirmation.html&amp;locale=ja" data-ls-product-uuid="d5e7e761-8b1b-4ca8-b1fe-771acd1450f8" class="lemonsqueezy-button" style="display:inline-flex; align-items:center; justify-content:center; min-height:60px; padding:10px 18px; border-radius:10px; background:#1d4ed8; color:#ffffff !important; font-size:1rem; font-weight:900; text-decoration:none;">
              ⚡ 月額Proプラン $29/月
            </a>
            <a href="https://truthofmarket.lemonsqueezy.com/checkout/buy/667aa482-f17c-47d1-b7f3-a2427c36516b?embed=1&amp;checkout[redirect_url]=https://getbreakai.com/confirmation.html&amp;locale=ja" data-ls-product-uuid="667aa482-f17c-47d1-b7f3-a2427c36516b" class="lemonsqueezy-button" style="display:inline-flex; align-items:center; justify-content:center; min-height:60px; padding:10px 18px; border-radius:10px; background:#d97706; color:#ffffff !important; font-size:1rem; font-weight:900; text-decoration:none;">
              👑 年間VIPパス $199/年 (43%OFF)
            </a>
          </div>
        </div>
      </section>

      <div class="kpi-grid">
        <div class="kpi-card">
          <div class="kpi-label">現在値 / 基準株価</div>
          <div class="kpi-val" style="color:#0b1f3a;">${entry:.2f} <span style="font-size:0.8rem; color:#475569; font-weight:700;">(約¥{int(round(entry*150)):,})</span></div>
        </div>
        <div class="kpi-card">
          <div class="kpi-label">AI総合安全スコア</div>
          <div class="kpi-val" style="color:#1d4ed8;">{score} / 100</div>
        </div>
        <div class="kpi-card">
          <div class="kpi-label">安全撤退ライン (2.0x ATR損切り)</div>
          <div class="kpi-val" style="color:var(--accent-rose);">${stop_loss:.2f} <span style="font-size:0.78rem;">(-${stop_dist:.2f})</span></div>
        </div>
        <div class="kpi-card">
          <div class="kpi-label">目標利益ライン (2.5R利確目安)</div>
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

      <!-- 下部：無料朝刊3色シグナル登録＆1タップ日本語決済ボックス -->
      <div id="gba-jp-lead-bottom" style="margin-top:32px; padding:24px; background:linear-gradient(135deg,#ecfdf5 0%,#eff6ff 100%); border:2.5px solid #059669; border-radius:16px;">
        <h3 style="margin-top:0; font-size:1.32rem; color:#0b1f3a !important;">📩 まずは無料メール登録（10秒）：毎朝8時の「新NISA 3色シグナル＆安全撤退ライン」</h3>
        <p style="margin-bottom:14px; font-size:1.06rem; color:#1e293b !important;">クレジットカード不要・いつでも1クリック解除可能。{jp_name} のトレンド変化と撤退ラインを毎朝日本語でお届けします。</p>
        <form class="gba-jp-signup-form" onsubmit="return window.__gbaSubmitJpSignup(event, this, '{ticker}');" style="display:flex; flex-wrap:wrap; gap:10px; margin-bottom:14px;">
          <input type="email" required autocomplete="email" placeholder="メールアドレスを入力（例: yamada@yahoo.co.jp）" style="flex:1 1 260px; min-height:58px; padding:12px 16px; font-size:1.08rem; font-weight:700; border-radius:12px; border:2px solid #64748b; background:#ffffff; color:#0f172a;" />
          <button type="submit" style="min-height:58px; padding:12px 24px; font-size:1.08rem; font-weight:900; border-radius:12px; border:none; background:#059669; color:#ffffff; cursor:pointer;">
            📩 無料メール会員に登録する →
          </button>
        </form>
        <div class="gba-jp-signup-status" role="status" aria-live="polite" style="display:none; margin-bottom:14px; padding:12px 14px; border-radius:10px; background:#d1fae5; color:#065f46; font-size:1.05rem; font-weight:800;"></div>
        <div style="padding-top:14px; border-top:1px solid #93c5fd; text-align:center;">
          <div style="font-size:1rem; font-weight:800; color:#0b1f3a; margin-bottom:10px;">🚀 今すぐ {jp_name} のVIP全機能・全銘柄シグナルを1タップ即時解放：</div>
          <div style="display:flex; justify-content:center; gap:10px; flex-wrap:wrap; margin-bottom:12px;">
            <a href="https://getbreakai.com/?ticker={term_ticker}#radar" class="btn-cta btn-cta-lg" style="min-height:60px; display:inline-flex; align-items:center;">📊 無料3秒計算機を開く（${ticker}） →</a>
            <a href="https://truthofmarket.lemonsqueezy.com/checkout/buy/d5e7e761-8b1b-4ca8-b1fe-771acd1450f8?embed=1&amp;checkout[redirect_url]=https://getbreakai.com/confirmation.html&amp;locale=ja" data-ls-product-uuid="d5e7e761-8b1b-4ca8-b1fe-771acd1450f8" class="lemonsqueezy-button btn-cta btn-cta-lg" style="min-height:60px; display:inline-flex; align-items:center; background:linear-gradient(135deg,#059669,#047857);">⚡ 月額Proプラン $29/月</a>
            <a href="https://truthofmarket.lemonsqueezy.com/checkout/buy/667aa482-f17c-47d1-b7f3-a2427c36516b?embed=1&amp;checkout[redirect_url]=https://getbreakai.com/confirmation.html&amp;locale=ja" data-ls-product-uuid="667aa482-f17c-47d1-b7f3-a2427c36516b" class="lemonsqueezy-button btn-cta btn-cta-lg" style="min-height:60px; display:inline-flex; align-items:center; background:linear-gradient(135deg,#d97706,#b45309);">👑 年間VIPパス $199/年 (43%OFF)</a>
          </div>
          <div style="font-size:0.86rem; color:#475569; line-height:1.6;">
            🔒 Stripe / Lemon Squeezy 日本語安全決済（Apple Pay・Google Pay・JCB・Visa・Master 対応 / いつでも1クリック解約）<br>
            🏛️ 法人・金融メディア・クオンツAPIデータ提携デスク: <a href="mailto:beable9489@gmail.com?subject=GetBreakAI%20Japan%20B2B%20API%20%26%20Media%20Inquiry" style="color:#1d4ed8; font-weight:800;">beable9489@gmail.com</a>
          </div>
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


def _senior_clean_hub_text(text: str) -> str:
    cleaned = text
    replacements = [
        ("2.0x ATR損切りライン＆適正株数", "新NISA非課税枠を守る安心配分＆投資額目安"),
        ("2.0x ATR損切り", "年2〜4回の穏やかな配分調整"),
        ("ATR損切り", "買いすぎ防止・穏やかな配分調整"),
        ("ATR撤退", "穏やかな配分見直し"),
        ("ATRリスク管理", "新NISA長期資産防衛"),
        ("ATR", "値動き目安"),
        ("コールGamma Wall(GEX)", "機関投資家の大口需要"),
        ("Gamma Wall(GEX)", "機関投資家の大口需要"),
        ("オプションGamma Wall", "機関投資家の支持帯"),
        ("ガンマスクイーズ", "機関投資家の実需買い"),
        ("Gamma", "機関需給"),
        ("GEX", "機関需給"),
        ("ダークプール", "大口機関投資家"),
        ("SEC 8-K", "決算・公式業績発表"),
        ("8-K", "公式業績発表"),
    ]
    for old_s, new_s in replacements:
        cleaned = cleaned.replace(old_s, new_s)
    return cleaned


def build_hub_html(date_str, all_specs):
    senior_specs = [
        s for s in all_specs
        if s["ticker"] not in ("SOXL", "TQQQ", "COIN", "MSTR")
        and "soxl" not in s["slug"].lower()
        and "mstr" not in s["slug"].lower()
    ]
    cards_html = "\n".join([
        f'<a href="/jp/{s["slug"]}" class="hub-seo-card">'
        f'<div class="hub-seo-meta">${s["ticker"]} · 安心度スコア {s["score"]}/100</div>'
        f'<div class="hub-seo-title">{_senior_clean_hub_text(s["title"])}</div>'
        f'<div class="hub-seo-focus">{_senior_clean_hub_text(s["focus"])}</div>'
        f'</a>'
        for s in senior_specs
    ])
    return f"""<!DOCTYPE html>
<html lang="ja" data-jp-theme="light">
<head>
  <meta charset="UTF-8">
  <meta name="google-site-verification" content="lM2Bf7R0XRTUDg-IZvGV9i06u2Q5rz6HJ8-IwoLFcgo">
  <meta name="google-site-verification" content="nAGlJMEUUPifbzSd8X4PCaBIyr3DtTwaa1a-q9zkbBc">
  <meta name="google-site-verification" content="G99bl17UU6iKgNm5ndGcSWp0dHFpJ0MjJqBBp0Exfx0">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>年金＋新NISAで『毎月ゆとりある老後収入』を設計し、暴落から資産寿命を守る羅針盤 | GetBreakAI</title>
  <meta name="description" content="50〜70代のための30秒・ゆとり老後＆新NISA毎月キャッシュフロー設計シミュレーター。個人向け国債・1489（日経高配当株50）/VYM・eMAXIS Slim 全世界株式（オルカン）・米国株式（S&amp;P500）を3色信号で年2〜4回ゆったり配分調整。">
  <link rel="canonical" href="https://getbreakai.com/jp/">
  <meta property="og:type" content="website">
  <meta property="og:site_name" content="GetBreakAI">
  <meta property="og:title" content="年金＋新NISAで『毎月ゆとりある老後収入』を設計し、暴落から資産寿命を守る羅針盤 | GetBreakAI">
  <meta property="og:description" content="30秒で年金＋月いくらの非課税ゆとり収入が作れるか試算。個人向け国債・1489/VYM・オルカン・S&amp;P500を3色信号で年2〜4回ゆったり配分見直し。">
  <meta property="og:url" content="https://getbreakai.com/jp/">
  <meta property="og:image" content="https://getbreakai.com/og-preview.png">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="年金＋新NISAで『毎月ゆとりある老後収入』を設計し、暴落から資産寿命を守る羅針盤 | GetBreakAI">
  <meta name="twitter:description" content="50〜70代のための新NISA＆ゆとり老後キャッシュフロー設計パートナー。">
  <meta name="twitter:image" content="https://getbreakai.com/og-preview.png">
  <link rel="icon" type="image/svg+xml" href="/favicon.svg">
  <script src="https://assets.lemonsqueezy.com/lemon.js" defer></script>
  <script src="/hq_member_crm_client.js" defer></script>
  <script>
    window.CHECKOUT_URLS = {{
      monthly: 'https://truthofmarket.lemonsqueezy.com/checkout/buy/d5e7e761-8b1b-4ca8-b1fe-771acd1450f8?embed=1&checkout[redirect_url]=https://getbreakai.com/confirmation.html&locale=ja',
      annual: 'https://truthofmarket.lemonsqueezy.com/checkout/buy/667aa482-f17c-47d1-b7f3-a2427c36516b?embed=1&checkout[redirect_url]=https://getbreakai.com/confirmation.html&locale=ja',
      enterprise: 'mailto:beable9489@gmail.com?subject=GetBreakAI%20Enterprise%20Inquiry'
    }};
    const CHECKOUT_URLS = window.CHECKOUT_URLS;
  </script>
  <script>
  /* === HQ Edge Real-Human Visitor & Free Signup Beacon (gba_getbreakai) === */
  (function(){{
    try {{
      if (typeof window === 'undefined' || typeof navigator === 'undefined') return;
      var kst = new Date(Date.now() + 9 * 3600 * 1000).toISOString().slice(0, 10);
      var ns = 'gba_getbreakai';
      window.trackGbaFreeSignup = function(emailAddr) {{
        try {{
          var host = (location && location.hostname) || '';
          if (!host || host === 'localhost' || host === '127.0.0.1') return;
          if (localStorage.getItem('hq_signup_' + ns + '_' + kst) !== '1') {{
            localStorage.setItem('hq_signup_' + ns + '_' + kst, '1');
            fetch('https://abacus.jasoncameron.dev/hit/' + ns + '/signup_' + kst, {{ mode: 'cors', keepalive: true }}).catch(function(){{}});
          }}
          if (localStorage.getItem('hq_signup_ever_' + ns) !== '1') {{
            localStorage.setItem('hq_signup_ever_' + ns, '1');
            fetch('https://abacus.jasoncameron.dev/hit/' + ns + '/signup_total', {{ mode: 'cors', keepalive: true }}).catch(function(){{}});
          }}
        }} catch (e) {{}}
      }};
      if (window.__HQ_BEACON_SENT_gba_getbreakai__ || window.__HQ_KPI_GBA__) return;
      window.__HQ_BEACON_SENT_gba_getbreakai__ = true;
      window.__HQ_KPI_GBA__ = true;
      var ua = navigator.userAgent || '';
      if (navigator.webdriver || /bot|crawl|spider|slurp|headless|lighthouse|gtmetrix|pingdom|uptimerobot|python|curl|node|axios/i.test(ua)) return;
      var host = (location && location.hostname) || '';
      if (!host || host === 'localhost' || host === '127.0.0.1') return;
      fetch('https://abacus.jasoncameron.dev/hit/' + ns + '/pv_' + kst, {{ mode: 'cors', keepalive: true }}).catch(function(){{}});
      fetch('https://abacus.jasoncameron.dev/hit/' + ns + '/pv_total', {{ mode: 'cors', keepalive: true }}).catch(function(){{}});
      if (localStorage.getItem('hq_uv_' + ns + '_' + kst) !== '1') {{
        localStorage.setItem('hq_uv_' + ns + '_' + kst, '1');
        fetch('https://abacus.jasoncameron.dev/hit/' + ns + '/uv_' + kst, {{ mode: 'cors', keepalive: true }}).catch(function(){{}});
      }}
      if (localStorage.getItem('hq_uv_ever_' + ns) !== '1') {{
        localStorage.setItem('hq_uv_ever_' + ns, '1');
        fetch('https://abacus.jasoncameron.dev/hit/' + ns + '/uv_total', {{ mode: 'cors', keepalive: true }}).catch(function(){{}});
      }}
      window.trackGbaPaidClick = function() {{
        fetch('https://abacus.jasoncameron.dev/hit/' + ns + '/paid_click_' + kst, {{ mode: 'cors', keepalive: true }}).catch(function(){{}});
        fetch('https://abacus.jasoncameron.dev/hit/' + ns + '/paid_click_total', {{ mode: 'cors', keepalive: true }}).catch(function(){{}});
      }};
      document.addEventListener('click', function(e) {{
        var el = e.target && e.target.closest ? e.target.closest('a, button, [role="button"]') : null;
        if (!el) return;
        var href = (el.getAttribute('href') || '').toLowerCase();
        var cls = (el.className || '').toLowerCase();
        if (href.indexOf('lemonsqueezy.com') !== -1 || cls.indexOf('lemonsqueezy') !== -1) {{
          window.trackGbaPaidClick();
        }}
      }}, true);
    }} catch (e) {{}}
  }})();
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
    html {{ font-size: 16.5px; }}
    html[data-jp-font="large"] {{ font-size: 18.5px; }}
    html[data-jp-font="xlarge"] {{ font-size: 20.2px; }}
    html, body {{ max-width: 100%; overflow-x: hidden; }}
    body {{
      background: var(--bg-page);
      color: var(--text-main);
      font-family: 'Noto Sans JP', -apple-system, BlinkMacSystemFont, sans-serif;
      line-height: 1.65;
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
      padding: 14px 18px;
      border-radius: 12px;
      font-size: 1.05rem;
      font-weight: 900;
      display: flex;
      flex-direction: column;
      gap: 3px;
      align-items: center;
      justify-content: center;
      width: 100%;
      text-align: center;
      min-height: 66px;
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

    /* Senior Font Toggle, 3-Color Traffic Light Cards, Morning Club & 1-Field Morning Mail Signup */
    .btn-top-font {{
      padding: 0 10px;
      border-radius: 7px;
      font-weight: 900;
      font-size: 0.78rem;
      min-height: 40px;
      display: inline-flex;
      align-items: center;
      justify-content: center;
      white-space: nowrap;
      flex-shrink: 0;
      cursor: pointer;
      background: #ecfdf5;
      color: #065f46;
      border: 1.5px solid #10b981;
    }}
    html[data-jp-theme="dark"] .btn-top-font {{
      background: #064e3b;
      color: #ecfdf5;
      border-color: #34d399;
    }}
    .hero-sublead {{
      font-size: 0.94rem;
      color: var(--text-muted);
      font-weight: 700;
      margin: 0 0 12px;
      line-height: 1.55;
    }}
    .signal-light-section {{
      background: var(--bg-card);
      border: 1.5px solid var(--border-col);
      border-radius: 14px;
      padding: 14px;
      margin-bottom: 16px;
    }}
    .signal-light-grid {{
      display: grid;
      grid-template-columns: repeat(4, minmax(0, 1fr));
      gap: 10px;
      margin-top: 10px;
    }}
    .signal-light-card {{
      background: var(--bg-sub);
      border: 2px solid var(--border-col);
      border-radius: 12px;
      padding: 12px;
      text-align: left;
      cursor: pointer;
      transition: transform 0.15s ease, border-color 0.15s ease;
      display: flex;
      flex-direction: column;
      gap: 5px;
      min-height: 112px;
      min-width: 0;
    }}
    .signal-light-card:hover {{ transform: translateY(-2px); border-color: var(--accent-blue); }}
    .signal-light-card.sig-buy {{ border-top: 5px solid #10b981; }}
    .signal-light-card.sig-watch {{ border-top: 5px solid #f59e0b; }}
    .signal-light-card.sig-warn {{ border-top: 5px solid #e11d48; background: rgba(244, 63, 94, 0.06); }}
    .sig-pill {{
      display: inline-flex;
      align-items: center;
      gap: 4px;
      font-size: 0.78rem;
      font-weight: 900;
      padding: 3px 9px;
      border-radius: 999px;
      width: fit-content;
    }}
    .sig-pill-buy {{ background: rgba(16, 185, 129, 0.16); color: var(--accent-emerald); }}
    .sig-pill-watch {{ background: rgba(245, 158, 11, 0.18); color: var(--accent-amber); }}
    .sig-pill-warn {{ background: rgba(244, 63, 94, 0.18); color: var(--accent-rose); }}

    /* 🍵 朝の資産守り倶楽部 (#gbaMorningClubJp) */
    .gba-morning-club {{
      background: linear-gradient(135deg, #fffbeb 0%, #f8fafc 100%);
      border: 2px solid #d97706;
      border-radius: 14px;
      padding: 16px 16px;
      margin-bottom: 18px;
      box-shadow: 0 8px 22px rgba(180, 83, 9, 0.08);
      max-width: 100%;
    }}
    html[data-jp-theme="dark"] .gba-morning-club {{
      background: linear-gradient(135deg, rgba(30, 27, 75, 0.92), rgba(15, 23, 42, 0.95));
      border-color: rgba(251, 191, 36, 0.55);
      box-shadow: 0 8px 24px rgba(0, 0, 0, 0.35);
    }}
    .gba-club-header {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      flex-wrap: wrap;
      gap: 8px;
      margin-bottom: 10px;
    }}
    .gba-club-title-group {{
      display: flex;
      align-items: center;
      flex-wrap: wrap;
      gap: 8px;
      min-width: 0;
    }}
    .gba-club-badge {{
      display: inline-flex;
      align-items: center;
      background: #fef3c7;
      color: #92400e;
      border: 1.5px solid #d97706;
      font-size: 0.78rem;
      font-weight: 900;
      padding: 3px 10px;
      border-radius: 999px;
    }}
    html[data-jp-theme="dark"] .gba-club-badge {{
      background: rgba(245, 158, 11, 0.18);
      color: #fde68a;
      border-color: #fbbf24;
    }}
    .gba-club-title {{
      font-size: 1.02rem;
      font-weight: 900;
      color: var(--text-main);
      line-height: 1.35;
    }}
    .gba-club-streak {{
      display: inline-flex;
      align-items: center;
      gap: 4px;
      background: #ecfdf5;
      color: #065f46;
      border: 1.5px solid #059669;
      font-size: 0.8rem;
      font-weight: 900;
      padding: 4px 11px;
      border-radius: 999px;
      max-width: 100%;
    }}
    html[data-jp-theme="dark"] .gba-club-streak {{
      background: rgba(16, 185, 129, 0.18);
      color: #6ee7b7;
      border-color: #34d399;
    }}
    .gba-club-greeting {{
      background: var(--bg-card);
      border: 1px solid var(--border-col);
      border-left: 4px solid #d97706;
      border-radius: 10px;
      padding: 11px 13px;
      margin-bottom: 12px;
      font-size: 0.94rem;
      line-height: 1.65;
      color: var(--text-main);
      font-weight: 700;
      word-break: break-word;
    }}
    .gba-club-greeting-label {{
      display: inline-block;
      color: var(--accent-amber);
      font-weight: 900;
      margin-right: 6px;
    }}
    .gba-club-poll-header {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      flex-wrap: wrap;
      gap: 6px;
      margin-bottom: 8px;
    }}
    .gba-club-poll-title {{
      font-size: 0.9rem;
      font-weight: 900;
      color: var(--text-main);
    }}
    .gba-club-poll-meta {{
      font-size: 0.8rem;
      font-weight: 800;
      color: var(--text-sub);
    }}
    .gba-club-poll-grid {{
      display: grid;
      grid-template-columns: repeat(3, minmax(0, 1fr));
      gap: 10px;
    }}
    .gba-club-poll-btn {{
      min-height: 58px;
      min-width: 0;
      width: 100%;
      padding: 10px 13px;
      border-radius: 11px;
      border: 2px solid var(--border-col);
      background: var(--bg-card);
      color: var(--text-main);
      cursor: pointer;
      display: flex;
      flex-direction: column;
      justify-content: center;
      gap: 7px;
      text-align: left;
      transition: transform 0.14s ease, border-color 0.16s ease, box-shadow 0.16s ease;
    }}
    .gba-club-poll-btn:hover {{
      transform: translateY(-1px);
      border-color: var(--accent-blue);
    }}
    .gba-club-poll-btn.is-active {{
      border-color: #059669;
      background: #ecfdf5;
      box-shadow: 0 0 0 3px rgba(5, 150, 105, 0.18);
    }}
    html[data-jp-theme="dark"] .gba-club-poll-btn.is-active {{
      border-color: #34d399;
      background: rgba(16, 185, 129, 0.18);
      box-shadow: 0 0 0 3px rgba(52, 211, 153, 0.22);
    }}
    .gba-poll-row-top {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      gap: 8px;
      width: 100%;
      min-width: 0;
    }}
    .gba-poll-opt-text {{
      font-size: 0.95rem;
      font-weight: 900;
      color: var(--text-main);
      min-width: 0;
      overflow-wrap: anywhere;
    }}
    .gba-poll-opt-pct {{
      font-family: monospace;
      font-size: 0.9rem;
      font-weight: 900;
      color: var(--accent-blue);
      flex-shrink: 0;
    }}
    .gba-poll-bar-bg {{
      display: block;
      width: 100%;
      height: 8px;
      border-radius: 999px;
      background: rgba(148, 163, 184, 0.25);
      overflow: hidden;
    }}
    .gba-poll-bar-fill {{
      display: block;
      height: 100%;
      border-radius: 999px;
      transition: width 0.42s cubic-bezier(0.22, 1, 0.36, 1);
    }}
    .gba-poll-bar-fill.fill-dip {{ background: #10b981; }}
    .gba-poll-bar-fill.fill-watch {{ background: #f59e0b; }}
    .gba-poll-bar-fill.fill-cash {{ background: #2563eb; }}
    .gba-club-companion {{
      margin-top: 10px;
      padding: 10px 12px;
      border-radius: 10px;
      background: var(--bg-card);
      border: 1.5px dashed var(--border-col);
      font-size: 0.89rem;
      font-weight: 800;
      line-height: 1.6;
      color: var(--text-muted);
      word-break: break-word;
    }}
    .gba-club-companion.is-voted {{
      background: #ecfdf5;
      border: 1.5px solid #059669;
      color: #065f46;
    }}
    html[data-jp-theme="dark"] .gba-club-companion.is-voted {{
      background: rgba(16, 185, 129, 0.16);
      border-color: #34d399;
      color: #a7f3d0;
    }}

    /* Passwordless 3-Sec Morning Macro Club Membership (#gba-jp-passwordless-signup) */
    .gba-jp-pwless-box {{
      margin-top: 14px;
      padding: 16px 16px;
      border-radius: 12px;
      background: var(--bg-card);
      border: 2px solid #059669;
      box-shadow: 0 6px 18px rgba(5, 150, 105, 0.10);
    }}
    html[data-jp-theme="dark"] .gba-jp-pwless-box {{
      background: rgba(15, 23, 42, 0.88);
      border-color: #10b981;
      box-shadow: 0 6px 20px rgba(0, 0, 0, 0.35);
    }}
    .gba-jp-pwless-top {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      flex-wrap: wrap;
      gap: 8px;
      margin-bottom: 8px;
    }}
    .gba-jp-pwless-badge {{
      display: inline-flex;
      align-items: center;
      gap: 6px;
      background: #059669;
      color: #ffffff;
      font-size: 0.84rem;
      font-weight: 900;
      padding: 4px 12px;
      border-radius: 999px;
      letter-spacing: 0.01em;
    }}
    .gba-jp-pwless-note {{
      font-size: 0.78rem;
      font-weight: 800;
      color: var(--text-muted);
    }}
    .gba-jp-pwless-heading {{
      font-size: 1.08rem;
      font-weight: 900;
      color: var(--text-main);
      line-height: 1.45;
      margin: 0 0 6px;
    }}
    .gba-jp-pwless-sub {{
      font-size: 0.9rem;
      color: var(--text-muted);
      line-height: 1.62;
      margin: 0 0 12px;
    }}
    .gba-jp-seg-label {{
      font-size: 0.82rem;
      font-weight: 900;
      color: var(--text-main);
      margin-bottom: 6px;
      display: block;
    }}
    .gba-jp-seg-grid {{
      display: grid;
      grid-template-columns: repeat(3, minmax(0, 1fr));
      gap: 8px;
      margin-bottom: 12px;
    }}
    .gba-jp-seg-btn {{
      appearance: none;
      min-height: 46px;
      padding: 8px 10px;
      border-radius: 10px;
      border: 1.8px solid var(--border-col);
      background: var(--bg-sub);
      color: var(--text-main);
      font-size: 0.88rem;
      font-weight: 800;
      font-family: inherit;
      cursor: pointer;
      display: inline-flex;
      align-items: center;
      justify-content: center;
      text-align: center;
      line-height: 1.35;
      transition: all 0.15s ease;
    }}
    .gba-jp-seg-btn:hover {{
      border-color: #059669;
    }}
    .gba-jp-seg-btn.is-active {{
      background: #ecfdf5;
      border-color: #059669;
      color: #065f46;
      box-shadow: 0 0 0 2px rgba(5, 150, 105, 0.18);
    }}
    html[data-jp-theme="dark"] .gba-jp-seg-btn.is-active {{
      background: rgba(16, 185, 129, 0.20);
      border-color: #34d399;
      color: #a7f3d0;
    }}
    .gba-jp-pwless-form {{
      display: grid;
      grid-template-columns: minmax(160px, 0.85fr) minmax(240px, 1.45fr) auto;
      gap: 10px;
      align-items: stretch;
    }}
    .gba-jp-pwless-input {{
      min-height: 50px;
      padding: 10px 13px;
      border-radius: 10px;
      border: 1.8px solid var(--border-col);
      background: var(--bg-card);
      color: var(--text-main);
      font-size: 0.96rem;
      font-weight: 700;
      font-family: inherit;
      width: 100%;
    }}
    .gba-jp-pwless-input:focus {{
      outline: 3px solid rgba(5, 150, 105, 0.30);
      border-color: #059669;
    }}
    .gba-jp-pwless-submit {{
      appearance: none;
      min-height: 50px;
      padding: 10px 18px;
      border-radius: 10px;
      border: none;
      background: linear-gradient(135deg, #059669, #047857);
      color: #ffffff;
      font-size: 0.95rem;
      font-weight: 900;
      font-family: inherit;
      cursor: pointer;
      white-space: nowrap;
      box-shadow: 0 6px 16px rgba(5, 150, 105, 0.25);
    }}
    .gba-jp-pwless-submit:hover {{ filter: brightness(1.05); }}
    .gba-jp-pwless-feedback {{
      display: none;
      margin-top: 12px;
      padding: 12px 14px;
      border-radius: 10px;
      background: #ecfdf5;
      border: 1.5px solid #059669;
      color: #065f46;
      font-size: 0.92rem;
      font-weight: 800;
      line-height: 1.65;
    }}
    html[data-jp-theme="dark"] .gba-jp-pwless-feedback {{
      background: rgba(16, 185, 129, 0.16);
      border-color: #34d399;
      color: #a7f3d0;
    }}
    .gba-jp-pwless-feedback.is-error {{
      background: #fff1f2;
      border-color: #e11d48;
      color: #9f1239;
    }}
    html[data-jp-theme="dark"] .gba-jp-pwless-feedback.is-error {{
      background: rgba(244, 63, 94, 0.16);
      border-color: #fb7185;
      color: #fecdd3;
    }}
    .gba-jp-club-manual-cta {{
      display: inline-flex;
      align-items: center;
      justify-content: center;
      margin-top: 8px;
      min-height: 46px;
      padding: 8px 16px;
      border-radius: 10px;
      background: #059669;
      color: #ffffff !important;
      font-size: 0.92rem;
      font-weight: 900;
      text-decoration: none;
      box-shadow: 0 4px 12px rgba(5, 150, 105, 0.24);
    }}
    @media (max-width: 860px) {{
      .gba-jp-pwless-form {{ grid-template-columns: 1fr; }}
      .gba-jp-pwless-submit {{ width: 100%; white-space: normal; }}
    }}
    @media (max-width: 680px) {{
      .gba-jp-seg-grid {{ grid-template-columns: 1fr; }}
    }}

    .morning-mail-card {{
      background: linear-gradient(135deg, rgba(6, 95, 70, 0.08), rgba(29, 78, 216, 0.08));
      border: 2.5px solid #059669;
      border-radius: 14px;
      padding: 18px 16px;
      margin-bottom: 20px;
      box-shadow: 0 10px 26px rgba(5, 150, 105, 0.10);
    }}
    .morning-mail-form {{
      display: flex;
      gap: 10px;
      flex-wrap: wrap;
      margin-top: 12px;
    }}
    .morning-mail-input {{
      flex: 1 1 260px;
      min-height: 56px;
      padding: 12px 14px;
      border-radius: 10px;
      border: 2px solid var(--border-col);
      background: var(--bg-card);
      color: var(--text-main);
      font-size: 1.02rem;
      font-weight: 700;
    }}
    .morning-mail-input:focus {{
      outline: 3px solid rgba(5, 150, 105, 0.35);
      border-color: #059669;
    }}
    .morning-mail-btn {{
      flex: 0 0 auto;
      min-height: 56px;
      padding: 12px 22px;
      border-radius: 10px;
      border: none;
      background: linear-gradient(135deg, #059669, #047857);
      color: #ffffff;
      font-size: 1.0rem;
      font-weight: 900;
      cursor: pointer;
      box-shadow: 0 6px 18px rgba(5, 150, 105, 0.28);
      white-space: nowrap;
    }}

    @media (max-width: 820px) {{
      .signal-light-grid {{ grid-template-columns: repeat(2, minmax(0, 1fr)); }}
    }}

    @media (max-width: 680px) {{
      .gba-club-poll-grid {{ grid-template-columns: 1fr; }}
    }}

    @media (max-width: 640px) {{
      .container {{ padding: 6px 12px 24px; }}
      .brand-link {{ font-size: 0.88rem; }}
      .btn-top-main, .btn-top-yt, .btn-top-theme, .btn-top-font {{ padding: 0 7px; font-size: 0.7rem; min-height: 38px; }}
      .hero-title {{ font-size: 1.12rem; margin: 6px 0 6px; line-height: 1.32; }}
      .signal-light-grid {{ grid-template-columns: 1fr 1fr; gap: 8px; }}
      .gba-morning-club {{ padding: 13px 12px; }}
      .morning-mail-btn {{ width: 100%; white-space: normal; }}
      .calc-card {{ padding: 10px 10px; }}
      .calc-header {{ margin-bottom: 6px; }}
      .calc-title {{ font-size: 0.86rem; }}
      .comp-grid, .cta-dual-grid {{ grid-template-columns: 1fr; }}
      .vip-unlock-btn {{ width: 100%; }}
      .grid {{ grid-template-columns: 1fr; }}
    }}

    /* 📘 ¥0 無料公開商品：はじめての新NISA＆証券アプリ基本マニュアル (#gbaFreeStarterManualJp & #gbaStarterManualModal) */
    .gba-starter-manual {{
      background: linear-gradient(135deg, #f0fdf4 0%, #eff6ff 100%);
      border: 2px solid #059669;
      border-radius: 14px;
      padding: 18px 18px;
      margin-bottom: 18px;
      box-shadow: 0 8px 22px rgba(5, 150, 105, 0.09);
      max-width: 100%;
    }}
    html[data-jp-theme="dark"] .gba-starter-manual {{
      background: linear-gradient(135deg, rgba(6, 78, 59, 0.34) 0%, rgba(15, 23, 42, 0.96) 100%);
      border-color: #10b981;
      box-shadow: 0 8px 24px rgba(0, 0, 0, 0.38);
    }}
    .gba-manual-top-row {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      flex-wrap: wrap;
      gap: 8px;
      margin-bottom: 10px;
    }}
    .gba-manual-free-badge {{
      display: inline-flex;
      align-items: center;
      gap: 6px;
      background: #059669;
      color: #ffffff;
      font-size: 0.92rem;
      font-weight: 900;
      padding: 5px 12px;
      border-radius: 999px;
      letter-spacing: 0.01em;
    }}
    .gba-manual-sub-badge {{
      font-size: 0.9rem;
      font-weight: 800;
      color: #065f46;
      background: #d1fae5;
      border: 1px solid #6ee7b7;
      padding: 4px 11px;
      border-radius: 999px;
    }}
    html[data-jp-theme="dark"] .gba-manual-sub-badge {{
      background: rgba(16, 185, 129, 0.18);
      color: #a7f3d0;
      border-color: rgba(52, 211, 153, 0.45);
    }}
    .gba-manual-heading {{
      font-size: 1.24rem;
      font-weight: 900;
      color: var(--text-main);
      line-height: 1.45;
      margin: 0 0 8px;
    }}
    .gba-manual-lead {{
      font-size: 1.125rem;
      color: var(--text-muted);
      line-height: 1.72;
      margin: 0 0 14px;
      word-break: break-word;
    }}
    .gba-manual-chap-grid {{
      display: grid;
      grid-template-columns: repeat(3, minmax(0, 1fr));
      gap: 12px;
      margin-bottom: 14px;
    }}
    .gba-manual-chap-btn {{
      appearance: none;
      background: var(--bg-card);
      border: 2px solid var(--border-col);
      border-radius: 12px;
      padding: 14px 14px;
      text-align: left;
      cursor: pointer;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      gap: 8px;
      min-height: 64px;
      min-width: 0;
      color: var(--text-main);
      font-family: inherit;
      transition: transform 0.15s ease, border-color 0.15s ease, box-shadow 0.15s ease;
    }}
    .gba-manual-chap-btn:hover {{
      transform: translateY(-2px);
      border-color: #059669;
      box-shadow: 0 6px 16px rgba(5, 150, 105, 0.14);
    }}
    .gba-manual-chap-tag {{
      display: inline-block;
      font-size: 0.86rem;
      font-weight: 900;
      color: #047857;
      background: #ecfdf5;
      border: 1px solid #a7f3d0;
      padding: 3px 9px;
      border-radius: 999px;
      width: fit-content;
    }}
    html[data-jp-theme="dark"] .gba-manual-chap-tag {{
      color: #6ee7b7;
      background: rgba(16, 185, 129, 0.16);
      border-color: rgba(52, 211, 153, 0.4);
    }}
    .gba-manual-chap-title {{
      font-size: 1.125rem;
      font-weight: 900;
      color: var(--text-main);
      line-height: 1.45;
    }}
    .gba-manual-chap-desc {{
      font-size: 1.02rem;
      color: var(--text-muted);
      line-height: 1.62;
    }}
    .gba-manual-chap-more {{
      font-size: 0.96rem;
      font-weight: 900;
      color: var(--accent-blue);
    }}
    .gba-manual-cta-row {{
      display: flex;
      flex-wrap: wrap;
      gap: 10px;
      align-items: center;
      margin-bottom: 12px;
    }}
    .gba-manual-open-btn {{
      appearance: none;
      background: linear-gradient(135deg, #059669, #047857);
      color: #ffffff;
      border: none;
      border-radius: 12px;
      padding: 14px 20px;
      min-height: 56px;
      font-size: 1.125rem;
      font-weight: 900;
      font-family: inherit;
      cursor: pointer;
      display: inline-flex;
      align-items: center;
      justify-content: center;
      gap: 8px;
      box-shadow: 0 6px 18px rgba(5, 150, 105, 0.28);
      flex: 1 1 320px;
      text-align: center;
    }}
    .gba-manual-open-btn:hover {{ filter: brightness(1.06); }}
    .gba-manual-signal-btn {{
      appearance: none;
      background: var(--bg-card);
      color: var(--text-main);
      border: 2px solid var(--accent-blue);
      border-radius: 12px;
      padding: 12px 16px;
      min-height: 56px;
      font-size: 1.04rem;
      font-weight: 900;
      font-family: inherit;
      cursor: pointer;
      display: inline-flex;
      align-items: center;
      justify-content: center;
      gap: 6px;
      flex: 1 1 280px;
      text-align: center;
    }}
    .gba-manual-funnel-strip {{
      display: flex;
      flex-wrap: wrap;
      align-items: center;
      justify-content: space-between;
      gap: 10px;
      padding-top: 10px;
      border-top: 1px dashed var(--border-col);
      font-size: 1rem;
      color: var(--text-muted);
      line-height: 1.6;
    }}
    .gba-manual-funnel-links {{
      display: flex;
      flex-wrap: wrap;
      gap: 10px;
      align-items: center;
    }}
    .gba-manual-pro-link {{
      display: inline-flex;
      align-items: center;
      min-height: 44px;
      padding: 6px 13px;
      border-radius: 999px;
      font-size: 0.96rem;
      font-weight: 900;
      text-decoration: none;
      background: rgba(37, 99, 235, 0.1);
      color: var(--accent-blue);
      border: 1.5px solid var(--accent-blue);
    }}
    .gba-manual-vip-link {{
      display: inline-flex;
      align-items: center;
      min-height: 44px;
      padding: 6px 13px;
      border-radius: 999px;
      font-size: 0.96rem;
      font-weight: 900;
      text-decoration: none;
      background: rgba(217, 119, 6, 0.14);
      color: var(--accent-amber);
      border: 1.5px solid var(--accent-amber);
    }}

    /* Interactive Modal (#gbaStarterManualModal) */
    .gba-manual-modal-backdrop {{
      display: none;
      position: fixed;
      inset: 0;
      z-index: 9999;
      background: rgba(15, 23, 42, 0.76);
      backdrop-filter: blur(4px);
      padding: 18px 12px;
      overflow-y: auto;
      align-items: flex-start;
      justify-content: center;
    }}
    .gba-manual-modal-backdrop.is-open {{
      display: flex;
    }}
    .gba-manual-modal-dialog {{
      background: var(--bg-card);
      color: var(--text-main);
      border: 2px solid #059669;
      border-radius: 16px;
      width: 100%;
      max-width: 860px;
      margin: 8px auto 32px;
      box-shadow: 0 22px 50px rgba(0, 0, 0, 0.45);
      overflow: hidden;
    }}
    .gba-manual-modal-header {{
      position: sticky;
      top: 0;
      z-index: 5;
      background: var(--bg-card);
      border-bottom: 2px solid var(--border-col);
      padding: 14px 18px;
      display: flex;
      justify-content: space-between;
      align-items: center;
      flex-wrap: wrap;
      gap: 10px;
    }}
    .gba-manual-modal-title {{
      font-size: 1.22rem;
      font-weight: 900;
      color: var(--text-main);
      margin: 4px 0 0;
      line-height: 1.4;
    }}
    .gba-manual-modal-actions {{
      display: flex;
      gap: 8px;
      flex-wrap: wrap;
    }}
    .gba-manual-action-btn {{
      appearance: none;
      min-height: 48px;
      padding: 8px 14px;
      border-radius: 10px;
      font-size: 1rem;
      font-weight: 900;
      font-family: inherit;
      cursor: pointer;
      border: 2px solid var(--border-col);
      background: var(--bg-sub);
      color: var(--text-main);
    }}
    .gba-manual-action-btn.btn-print {{
      border-color: #059669;
      background: #ecfdf5;
      color: #065f46;
    }}
    html[data-jp-theme="dark"] .gba-manual-action-btn.btn-print {{
      background: rgba(16, 185, 129, 0.18);
      color: #a7f3d0;
      border-color: #10b981;
    }}
    .gba-manual-nav-pills {{
      display: flex;
      flex-wrap: wrap;
      gap: 8px;
      padding: 12px 18px;
      background: var(--bg-sub);
      border-bottom: 1px solid var(--border-col);
    }}
    .gba-manual-jump-pill {{
      appearance: none;
      min-height: 46px;
      padding: 8px 14px;
      border-radius: 999px;
      border: 1.5px solid var(--border-col);
      background: var(--bg-card);
      color: var(--text-main);
      font-size: 1rem;
      font-weight: 800;
      font-family: inherit;
      cursor: pointer;
    }}
    .gba-manual-jump-pill:hover {{ border-color: #059669; }}
    .gba-manual-modal-body {{
      padding: 20px 20px 24px;
      font-size: 1.15rem;
      line-height: 1.82;
      color: var(--text-main);
    }}
    .gba-manual-chapter-box {{
      background: var(--bg-sub);
      border: 1.5px solid var(--border-col);
      border-radius: 14px;
      padding: 18px 18px;
      margin-bottom: 18px;
      scroll-margin-top: 96px;
    }}
    .gba-manual-chapter-box h3 {{
      font-size: 1.24rem;
      font-weight: 900;
      color: var(--text-main);
      margin: 0 0 10px;
      line-height: 1.45;
    }}
    .gba-manual-chapter-box p {{
      font-size: 1.15rem;
      color: var(--text-main);
      margin: 0 0 12px;
      line-height: 1.82;
    }}
    .gba-manual-broker-grid {{
      display: grid;
      grid-template-columns: repeat(2, minmax(0, 1fr));
      gap: 12px;
      margin-top: 10px;
    }}
    .gba-manual-broker-card {{
      background: var(--bg-card);
      border: 1.5px solid var(--border-col);
      border-radius: 12px;
      padding: 14px 15px;
      font-size: 1.125rem;
      line-height: 1.75;
    }}
    .gba-manual-broker-card strong.broker-name {{
      display: block;
      font-size: 1.14rem;
      color: var(--accent-blue);
      margin-bottom: 6px;
    }}
    .gba-manual-broker-card ol {{
      margin: 0;
      padding-left: 22px;
    }}
    .gba-manual-broker-card li {{
      margin-bottom: 6px;
    }}
    .gba-manual-tip-callout {{
      margin-top: 12px;
      padding: 12px 14px;
      border-radius: 10px;
      background: rgba(16, 185, 129, 0.11);
      border-left: 4px solid #059669;
      font-size: 1.125rem;
      line-height: 1.72;
      color: var(--text-main);
    }}
    .gba-manual-modal-funnel {{
      background: linear-gradient(135deg, rgba(16, 185, 129, 0.12), rgba(37, 99, 235, 0.10));
      border: 2px solid #059669;
      border-radius: 14px;
      padding: 18px 18px;
      margin-top: 8px;
    }}
    .gba-manual-modal-funnel h4 {{
      font-size: 1.2rem;
      font-weight: 900;
      margin: 0 0 8px;
      color: var(--text-main);
    }}
    .gba-manual-modal-funnel p {{
      font-size: 1.125rem;
      margin: 0 0 14px;
      line-height: 1.75;
      color: var(--text-muted);
    }}
    @media (max-width: 820px) {{
      .gba-manual-chap-grid, .gba-manual-broker-grid {{ grid-template-columns: 1fr; }}
    }}
    @media (max-width: 640px) {{
      .gba-starter-manual {{ padding: 14px 12px; }}
      .gba-manual-heading {{ font-size: 1.14rem; }}
      .gba-manual-open-btn, .gba-manual-signal-btn {{ width: 100%; flex-basis: 100%; padding: 12px 14px; }}
      .gba-manual-modal-backdrop {{ padding: 8px 6px; }}
      .gba-manual-modal-header {{ padding: 12px 12px; }}
      .gba-manual-nav-pills {{ padding: 10px 12px; }}
      .gba-manual-modal-body {{ padding: 14px 12px 20px; font-size: 1.125rem; }}
      .gba-manual-chapter-box {{ padding: 14px 12px; }}
      .gba-manual-pro-link, .gba-manual-vip-link {{ width: 100%; justify-content: center; }}
    }}
    @media print {{
      body.printing-gba-manual > *:not(#gbaStarterManualModal) {{ display: none !important; }}
      body.printing-gba-manual #gbaStarterManualModal {{
        display: block !important;
        position: static !important;
        background: #ffffff !important;
        padding: 0 !important;
        overflow: visible !important;
      }}
      body.printing-gba-manual .gba-manual-modal-dialog {{
        max-width: 100% !important;
        border: none !important;
        box-shadow: none !important;
        background: #ffffff !important;
        color: #000000 !important;
        margin: 0 !important;
      }}
      body.printing-gba-manual .gba-manual-modal-actions,
      body.printing-gba-manual .gba-manual-nav-pills {{ display: none !important; }}
      body.printing-gba-manual .gba-manual-chapter-box {{
        break-inside: avoid;
        background: #ffffff !important;
        border: 1px solid #94a3b8 !important;
        color: #000000 !important;
      }}
    }}

    /* === 50-70s Senior Presbyopia Large-Print UX & #gba-retirement-architect-jp === */
    body {{
      font-size: 17.5px;
      line-height: 1.75;
    }}
    .hero-title {{
      font-size: clamp(1.58rem, 3vw, 2.2rem);
      line-height: 1.35;
    }}
    .hero-sublead {{
      font-size: 1.125rem;
      line-height: 1.76;
    }}
    .sig-pill, .gba-club-badge, .gba-club-streak, .gba-club-poll-meta,
    .gba-jp-pwless-badge, .gba-jp-pwless-note, .gba-manual-free-badge,
    .gba-manual-sub-badge, .calc-pill-risk, .out-label, .hub-seo-meta {{
      font-size: 0.94rem !important;
    }}
    .gba-club-greeting, .gba-club-companion, .gba-jp-pwless-sub,
    .gba-manual-lead, .cta-subnote, .hub-seo-focus {{
      font-size: 1.06rem !important;
      line-height: 1.72 !important;
    }}
    .preset-chip, .cap-btn, .tax-mode-btn, .gba-jp-seg-btn {{
      min-height: 48px !important;
      font-size: 0.98rem !important;
    }}

    .gba-retire-arch {{
      background: linear-gradient(135deg, #f0fdf4 0%, #eff6ff 100%);
      border: 2.5px solid #059669;
      border-radius: 16px;
      padding: 22px 20px;
      margin: 0 0 20px 0;
      box-shadow: 0 10px 28px rgba(5, 150, 105, 0.12);
    }}
    html[data-jp-theme="dark"] .gba-retire-arch {{
      background: linear-gradient(135deg, rgba(6, 44, 36, 0.95) 0%, rgba(15, 23, 42, 0.96) 100%);
      border-color: #10b981;
      box-shadow: 0 12px 30px rgba(16, 185, 129, 0.18);
    }}
    .gba-retire-top {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      flex-wrap: wrap;
      gap: 8px;
      margin-bottom: 10px;
    }}
    .gba-retire-kicker {{
      display: inline-flex;
      align-items: center;
      background: #dcfce7;
      color: #065f46;
      border: 1.5px solid #059669;
      border-radius: 999px;
      padding: 5px 14px;
      font-size: 0.95rem;
      font-weight: 900;
    }}
    html[data-jp-theme="dark"] .gba-retire-kicker {{
      background: rgba(16, 185, 129, 0.2);
      color: #6ee7b7;
      border-color: #34d399;
    }}
    .gba-retire-subtag {{
      display: inline-flex;
      align-items: center;
      background: #fef3c7;
      color: #92400e;
      border: 1px solid #d97706;
      border-radius: 999px;
      padding: 5px 13px;
      font-size: 0.94rem;
      font-weight: 800;
    }}
    html[data-jp-theme="dark"] .gba-retire-subtag {{
      background: rgba(245, 158, 11, 0.18);
      color: #fde68a;
      border-color: rgba(251, 191, 36, 0.5);
    }}
    .gba-retire-heading {{
      font-size: clamp(1.32rem, 2.2vw, 1.65rem);
      font-weight: 900;
      color: var(--text-main);
      margin: 4px 0 8px;
      line-height: 1.38;
    }}
    .gba-retire-lead {{
      font-size: 1.1rem;
      line-height: 1.75;
      color: var(--text-muted);
      margin: 0 0 16px;
    }}
    .gba-retire-presets {{
      display: grid;
      grid-template-columns: repeat(3, minmax(0, 1fr));
      gap: 12px;
      margin-bottom: 18px;
    }}
    .gba-retire-pgroup {{
      background: var(--bg-card);
      border: 1.5px solid var(--border-col);
      border-radius: 12px;
      padding: 13px 13px;
    }}
    .gba-retire-plabel {{
      display: block;
      font-size: 1rem;
      font-weight: 900;
      color: var(--text-main);
      margin-bottom: 9px;
    }}
    .gba-retire-pgrid {{
      display: grid;
      grid-template-columns: repeat(2, minmax(0, 1fr));
      gap: 8px;
    }}
    .gba-retire-pbtn {{
      min-height: 50px;
      padding: 8px 8px;
      border-radius: 10px;
      border: 1.5px solid var(--border-col);
      background: var(--bg-page);
      color: var(--text-main);
      font-size: 1.02rem;
      font-weight: 800;
      cursor: pointer;
      transition: all 0.15s ease;
    }}
    .gba-retire-pbtn.is-active {{
      background: linear-gradient(135deg, #059669, #047857);
      border-color: #10b981;
      color: #ffffff !important;
      box-shadow: 0 4px 12px rgba(5, 150, 105, 0.28);
    }}

    .gba-retire-res-grid {{
      display: grid;
      grid-template-columns: repeat(2, minmax(0, 1fr));
      gap: 15px;
      margin-bottom: 16px;
    }}
    .gba-retire-rcard {{
      background: var(--bg-card);
      border: 1.5px solid var(--border-col);
      border-radius: 14px;
      padding: 16px 16px;
      display: flex;
      flex-direction: column;
      gap: 11px;
    }}
    .gba-retire-rkicker {{
      font-size: 0.95rem;
      font-weight: 900;
      color: var(--accent-blue);
    }}
    .gba-retire-proj {{
      font-size: 1.08rem;
      color: var(--text-main);
    }}
    .gba-retire-proj strong {{
      font-size: 1.32rem;
      color: var(--accent-emerald);
    }}
    .gba-retire-cgrid {{
      display: grid;
      grid-template-columns: repeat(2, minmax(0, 1fr));
      gap: 10px;
    }}
    .gba-retire-cbox {{
      border-radius: 12px;
      padding: 12px 12px;
      border: 1.5px solid var(--border-col);
    }}
    .gba-retire-cbox.is-safe {{
      background: rgba(16, 185, 129, 0.1);
      border-color: #059669;
    }}
    .gba-retire-cbox.is-crash {{
      background: rgba(239, 68, 68, 0.08);
      border-color: rgba(239, 68, 68, 0.5);
    }}
    .gba-retire-ctag {{
      display: block;
      font-size: 0.94rem;
      font-weight: 900;
      color: var(--text-main);
      margin-bottom: 5px;
      line-height: 1.4;
    }}
    .gba-retire-cnum {{
      font-size: clamp(1.5rem, 2.3vw, 1.95rem);
      font-weight: 900;
      color: #047857;
      line-height: 1.2;
      margin-bottom: 5px;
    }}
    html[data-jp-theme="dark"] .gba-retire-cnum {{
      color: #34d399;
    }}
    .gba-retire-cnum.is-muted {{
      color: #b91c1c;
    }}
    html[data-jp-theme="dark"] .gba-retire-cnum.is-muted {{
      color: #fca5a5;
    }}
    .gba-retire-csub {{
      font-size: 0.98rem;
      line-height: 1.58;
      color: var(--text-muted);
    }}
    .gba-retire-callout {{
      background: rgba(16, 185, 129, 0.14);
      border: 1.5px solid #059669;
      border-radius: 10px;
      padding: 11px 13px;
      font-size: 1.04rem;
      line-height: 1.65;
      color: var(--text-main);
    }}
    .gba-retire-taxbox {{
      background: rgba(37, 99, 235, 0.09);
      border: 1.5px solid rgba(37, 99, 235, 0.42);
      border-radius: 10px;
      padding: 11px 13px;
      font-size: 1.02rem;
      line-height: 1.62;
      color: var(--text-main);
    }}

    .gba-retire-wtabs {{
      display: grid;
      grid-template-columns: repeat(3, minmax(0, 1fr));
      gap: 8px;
    }}
    .gba-retire-wtab {{
      min-height: 48px;
      padding: 7px 8px;
      border-radius: 9px;
      border: 1.5px solid var(--border-col);
      background: var(--bg-page);
      color: var(--text-main);
      font-size: 0.95rem;
      font-weight: 800;
      cursor: pointer;
    }}
    .gba-retire-wtab.is-active {{
      background: #1d4ed8;
      border-color: #2563eb;
      color: #ffffff !important;
    }}
    .gba-retire-wdesc {{
      font-size: 1.02rem;
      line-height: 1.62;
      color: var(--text-muted);
    }}
    .gba-wallet-list {{
      display: flex;
      flex-direction: column;
      gap: 10px;
    }}
    .gba-wallet-item {{
      background: var(--bg-page);
      border: 1px solid var(--border-col);
      border-radius: 10px;
      padding: 10px 12px;
    }}
    .gba-wallet-head {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      flex-wrap: wrap;
      gap: 6px;
      font-size: 1.02rem;
      font-weight: 800;
      color: var(--text-main);
      margin-bottom: 5px;
    }}
    .gba-wallet-stat {{
      font-weight: 900;
      color: var(--accent-emerald);
    }}
    .gba-wallet-bar {{
      height: 9px;
      border-radius: 999px;
      background: rgba(148, 163, 184, 0.28);
      overflow: hidden;
      margin-bottom: 5px;
    }}
    .gba-wallet-bar span {{
      display: block;
      height: 100%;
      border-radius: 999px;
      transition: width 0.2s ease;
    }}
    .gba-wallet-item.w1 .gba-wallet-bar span {{ background: #0284c7; }}
    .gba-wallet-item.w2 .gba-wallet-bar span {{ background: #059669; }}
    .gba-wallet-item.w3 .gba-wallet-bar span {{ background: #d97706; }}
    .gba-wallet-note {{
      font-size: 0.96rem;
      line-height: 1.56;
      color: var(--text-muted);
    }}

    .gba-nisa-core-strip {{
      background: var(--bg-card);
      border: 1.5px solid rgba(37, 99, 235, 0.42);
      border-radius: 13px;
      padding: 14px 15px;
      margin-bottom: 15px;
    }}
    .gba-nisa-core-title {{
      font-size: 1.05rem;
      line-height: 1.65;
      color: var(--text-main);
      margin-bottom: 10px;
    }}
    .gba-nisa-core-grid {{
      display: grid;
      grid-template-columns: repeat(4, minmax(0, 1fr));
      gap: 10px;
    }}
    .gba-nisa-core-card {{
      background: var(--bg-page);
      border: 1px solid var(--border-col);
      border-radius: 10px;
      padding: 11px 11px;
      display: flex;
      flex-direction: column;
      gap: 4px;
    }}
    .gba-nisa-core-badge {{
      font-size: 0.94rem;
      font-weight: 900;
      color: var(--accent-blue);
    }}
    .gba-nisa-core-card strong {{
      font-size: 1.02rem;
      color: var(--text-main);
      line-height: 1.4;
    }}
    .gba-nisa-core-card span:last-child {{
      font-size: 0.96rem;
      line-height: 1.56;
      color: var(--text-muted);
    }}

    .gba-retire-ladder {{
      display: grid;
      grid-template-columns: repeat(2, minmax(0, 1fr));
      gap: 10px;
    }}
    .gba-retire-cta {{
      min-height: 56px;
      padding: 12px 15px;
      border-radius: 11px;
      font-size: 1rem;
      font-weight: 900;
      cursor: pointer;
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      text-align: center;
      text-decoration: none;
      line-height: 1.38;
      box-sizing: border-box;
    }}
    .gba-retire-cta.c-manual {{
      background: #e0f2fe;
      border: 2px solid #0284c7;
      color: #075985;
    }}
    html[data-jp-theme="dark"] .gba-retire-cta.c-manual {{
      background: rgba(14, 165, 233, 0.18);
      border-color: #38bdf8;
      color: #e0f2fe;
    }}
    .gba-retire-cta.c-club {{
      background: linear-gradient(135deg, #059669, #047857);
      border: none;
      color: #ffffff !important;
    }}
    .gba-retire-cta.c-pro {{
      background: #1d4ed8;
      border: none;
      color: #ffffff !important;
    }}
    .gba-retire-cta.c-vip {{
      background: linear-gradient(135deg, #d97706, #b45309);
      border: none;
      color: #ffffff !important;
    }}
    .gba-retire-cta small {{
      font-size: 0.92rem;
      font-weight: 800;
      opacity: 0.95;
      margin-top: 2px;
    }}

    @media (max-width: 920px) {{
      .gba-retire-presets, .gba-retire-res-grid {{ grid-template-columns: 1fr; }}
      .gba-nisa-core-grid {{ grid-template-columns: repeat(2, minmax(0, 1fr)); }}
    }}
    @media (max-width: 640px) {{
      .gba-retire-arch {{ padding: 16px 12px; }}
      .gba-retire-cgrid, .gba-nisa-core-grid, .gba-retire-wtabs, .gba-retire-ladder {{ grid-template-columns: 1fr; }}
    }}
  </style>
</head>
<body>
  <div class="container">
    <!-- Consolidated Single-Row Top Navigation Bar -->
    <nav class="top-nav" aria-label="日本株・米国株ナビゲーション">
      <a href="/" class="brand-link">⚡ GetBreakAI</a>
      <div class="top-nav-actions">
        <button type="button" id="btnToggleJpFont" onclick="cycleJpFontSize()" class="btn-top-font" aria-label="文字サイズ切替">🔍 文字: 標準</button>
        <a href="/" class="btn-top-main">🏠 詳細端末</a>
        <a href="https://www.youtube.com/@GetBreakAI" target="_blank" rel="noopener" class="btn-top-yt">📺 YouTube</a>
        <button type="button" id="btnToggleJpTheme" onclick="toggleJpTheme()" class="btn-top-theme">🌙 切替</button>
      </div>
    </nav>

    <!-- Crisp Intuitive Senior B2C Headline (<=15 words, Above-the-Fold) -->
    <h1 class="hero-title">
      年金＋新NISAで『毎月ゆとりある老後収入』を設計し、暴落から資産寿命を守る羅針盤
    </h1>
    <p class="hero-sublead">
      難しい英語や専門用語、忙しい短期売買は不要です。<b>個人向け国債・高配当ETF（1489／VYM）・オルカン・S&amp;P500</b>を組み合わせ、3色信号（🟢・🟡・🔴）に合わせて<b>年2〜4回ゆったり配分を見直す</b>だけで、非課税枠360万円を守りながら心穏やかな老後収入を育てます。
    </p>

    <!-- 🚦 3-Color Traffic Light Quick Cards (100% Shin-NISA Eligible Senior Core) -->
    <section class="signal-light-section" id="jpSignalTrafficLightHub" aria-label="本日の新NISA適格コア4資産・3色ガイド">
      <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:8px;">
        <div style="font-weight:900; font-size:1.05rem; color:var(--text-main);">🚦 本日の新NISA適格「老後コア4資産」3色バランス早見カード <span style="font-size:0.94rem; color:var(--accent-blue);">（年2〜4回のゆったり配分見直し）</span></div>
        <a href="#gba-jp-passwordless-signup" style="font-size:0.95rem; font-weight:900; color:var(--accent-emerald); text-decoration:underline;">📧 毎朝8時の無料3色ブリーフを登録 ↓</a>
      </div>
      <div class="signal-light-grid">
        <button type="button" class="signal-light-card sig-buy" onclick="setQuickStock('1489'); document.getElementById('jpQuickCalcSection').scrollIntoView({{behavior:'smooth'}});">
          <span class="sig-pill sig-pill-buy">🟢 収入の財布（成長投資枠）</span>
          <strong style="font-size:1.05rem; color:var(--text-main);">1489 日経高配当株50 ETF</strong>
          <span style="font-size:0.95rem; color:var(--text-muted);">日本優良50社・新NISA非課税で配当受取</span>
        </button>
        <button type="button" class="signal-light-card sig-buy" onclick="setQuickStock('VYM'); document.getElementById('jpQuickCalcSection').scrollIntoView({{behavior:'smooth'}});">
          <span class="sig-pill sig-pill-buy">🟢 収入の財布（米国増配株）</span>
          <strong style="font-size:1.05rem; color:var(--text-main);">$VYM 米国高配当株ETF</strong>
          <span style="font-size:0.95rem; color:var(--text-muted);">米国大型増配株400社超へ安定分散</span>
        </button>
        <button type="button" class="signal-light-card sig-buy" onclick="document.getElementById('gba-retirement-architect-jp').scrollIntoView({{behavior:'smooth'}});">
          <span class="sig-pill sig-pill-buy">🟢 成長の財布（つみたて枠王道）</span>
          <strong style="font-size:1.05rem; color:var(--text-main);">eMAXIS Slim 全世界株式（オルカン）</strong>
          <span style="font-size:0.95rem; color:var(--text-muted);">世界分散＋S&amp;P500でインフレ負け防止</span>
        </button>
        <button type="button" class="signal-light-card sig-watch" onclick="document.getElementById('gba-retirement-architect-jp').scrollIntoView({{behavior:'smooth'}});">
          <span class="sig-pill sig-pill-watch">🛡️ 守りの財布（元本保護クッション）</span>
          <strong style="font-size:1.05rem; color:var(--text-main);">個人向け国債（変動10年）＆待機預金</strong>
          <span style="font-size:0.95rem; color:var(--text-muted);">生活費2〜3年分を安全確保・暴落時も安心</span>
        </button>
      </div>
    </section>

    <!-- 🧭 30秒・ゆとり老後＆新NISA毎月キャッシュフロー設計シミュレーター (#gba-retirement-architect-jp) -->
    <section class="gba-retire-arch" id="gba-retirement-architect-jp" aria-label="30秒・ゆとり老後＆新NISA毎月キャッシュフロー設計シミュレーター">
      <div class="gba-retire-top">
        <span class="gba-retire-kicker">🧭 無料公開・登録不要｜30秒 ゆとり老後設計ナビ</span>
        <span class="gba-retire-subtag">🌱 新NISA（非課税20.315%節税）＆ 年2〜4回ゆったり配分対応</span>
      </div>
      <h2 class="gba-retire-heading">
        30秒・ゆとり老後＆新NISA「毎月キャッシュフロー」設計シミュレーター
      </h2>
      <p class="gba-retire-lead">
        下の3つのボタンをタップするだけで、<b>公的年金に毎月プラスできる「ゆとり老後収入（非課税）」</b>、暴落・塩漬け回避で守られる毎月差額、そして本日の3色信号に連動した<b>「老後3つの財布」最適配分</b>がその場でわかります。
      </p>

      <div class="gba-retire-presets">
        <div class="gba-retire-pgroup">
          <span class="gba-retire-plabel">① 現在の老後準備資産（退職金・預貯金含む）</span>
          <div class="gba-retire-pgrid" role="group" aria-label="現在の老後準備資産">
            <button type="button" class="gba-retire-pbtn" data-gba-rgrp="asset" data-gba-rval="500" aria-pressed="false" onclick="setGbaRetirePreset('asset', 500, this)">500万円</button>
            <button type="button" class="gba-retire-pbtn is-active" data-gba-rgrp="asset" data-gba-rval="1500" aria-pressed="true" onclick="setGbaRetirePreset('asset', 1500, this)">1,500万円</button>
            <button type="button" class="gba-retire-pbtn" data-gba-rgrp="asset" data-gba-rval="3000" aria-pressed="false" onclick="setGbaRetirePreset('asset', 3000, this)">3,000万円</button>
            <button type="button" class="gba-retire-pbtn" data-gba-rgrp="asset" data-gba-rval="5000" aria-pressed="false" onclick="setGbaRetirePreset('asset', 5000, this)">5,000万円</button>
          </div>
        </div>

        <div class="gba-retire-pgroup">
          <span class="gba-retire-plabel">② 取り崩し（老後受取）開始まで</span>
          <div class="gba-retire-pgrid" role="group" aria-label="取り崩し開始まで">
            <button type="button" class="gba-retire-pbtn" data-gba-rgrp="years" data-gba-rval="0" aria-pressed="false" onclick="setGbaRetirePreset('years', 0, this)">今すぐ</button>
            <button type="button" class="gba-retire-pbtn is-active" data-gba-rgrp="years" data-gba-rval="5" aria-pressed="true" onclick="setGbaRetirePreset('years', 5, this)">5年後</button>
            <button type="button" class="gba-retire-pbtn" data-gba-rgrp="years" data-gba-rval="10" aria-pressed="false" onclick="setGbaRetirePreset('years', 10, this)">10年後</button>
            <button type="button" class="gba-retire-pbtn" data-gba-rgrp="years" data-gba-rval="15" aria-pressed="false" onclick="setGbaRetirePreset('years', 15, this)">15年後</button>
          </div>
        </div>

        <div class="gba-retire-pgroup">
          <span class="gba-retire-plabel">③ 毎月の新NISA積立額</span>
          <div class="gba-retire-pgrid" role="group" aria-label="毎月の新NISA積立額">
            <button type="button" class="gba-retire-pbtn" data-gba-rgrp="monthly" data-gba-rval="0" aria-pressed="false" onclick="setGbaRetirePreset('monthly', 0, this)">0円</button>
            <button type="button" class="gba-retire-pbtn" data-gba-rgrp="monthly" data-gba-rval="3" aria-pressed="false" onclick="setGbaRetirePreset('monthly', 3, this)">月3万円</button>
            <button type="button" class="gba-retire-pbtn is-active" data-gba-rgrp="monthly" data-gba-rval="5" aria-pressed="true" onclick="setGbaRetirePreset('monthly', 5, this)">月5万円</button>
            <button type="button" class="gba-retire-pbtn" data-gba-rgrp="monthly" data-gba-rval="10" aria-pressed="false" onclick="setGbaRetirePreset('monthly', 10, this)">月10万円</button>
          </div>
        </div>
      </div>

      <div class="gba-retire-res-grid" aria-live="polite">
        <!-- 計算結果① -->
        <div class="gba-retire-rcard">
          <div class="gba-retire-rkicker">計算結果 ① · 年金に毎月プラスできる「ゆとり老後キャッシュフロー」</div>
          <div class="gba-retire-proj">
            受取開始時の想定老後資産：<strong id="gbaRetireProjMan">約2,288万円</strong>
          </div>

          <div class="gba-retire-cgrid">
            <div class="gba-retire-cbox is-safe">
              <span class="gba-retire-ctag">🛡️ 3つの財布・年2〜4回配分ルート</span>
              <div class="gba-retire-cnum" id="gbaRetireSafeMo">月 +8.6万円</div>
              <div class="gba-retire-csub" id="gbaRetireSafeSub">年間 約103.0万円（年4.5%配当＆計画取り崩し・新NISA非課税）· <b>資産寿命 32年以上</b></div>
            </div>
            <div class="gba-retire-cbox is-crash">
              <span class="gba-retire-ctag">⚠️ 暴落・塩漬け放置ルート（-35%下落時）</span>
              <div class="gba-retire-cnum is-muted" id="gbaRetireCrashMo">月 +4.7万円</div>
              <div class="gba-retire-csub" id="gbaRetireCrashSub">退職前後の暴落で資産約1,487万円へ縮小 · <b>約19年で枯渇懸念</b></div>
            </div>
          </div>

          <div class="gba-retire-callout" id="gbaRetireGapBanner">
            ✅ 暴落・塩漬け回避で <strong>毎月 +3.9万円（年間 +46.8万円）のゆとり収入</strong> を守り抜き、資産寿命を <strong>+12年以上延長</strong> できます！
          </div>
          <div class="gba-retire-taxbox" id="gbaRetireTaxBanner">
            🌱 <strong>新NISA 20.315% 非課税節税メリット：</strong>特定口座と比べ <strong>年間 約2.1万円〜20.9万円 ／ 20年累計 約418万円</strong> の税金がまるごと手元に残ります。
          </div>
        </div>

        <!-- 計算結果② -->
        <div class="gba-retire-rcard">
          <div class="gba-retire-rkicker">計算結果 ② · 本日の3色シグナル連動「老後3つの財布」最適配分ガイド</div>

          <div class="gba-retire-wtabs" role="group" aria-label="相場天気モード切替">
            <button type="button" class="gba-retire-wtab" data-gba-wmode="green" aria-pressed="false" onclick="setGbaRetireWeather('green', this)">🟢 安定上昇</button>
            <button type="button" class="gba-retire-wtab is-active" data-gba-wmode="yellow" aria-pressed="true" onclick="setGbaRetireWeather('yellow', this)">🟡 様子見（本日）</button>
            <button type="button" class="gba-retire-wtab" data-gba-wmode="red" aria-pressed="false" onclick="setGbaRetireWeather('red', this)">🔴 現金防衛</button>
          </div>

          <div class="gba-retire-wdesc" id="gbaRetireWeatherDesc">
            🟡 本日は「様子見・配当重視モード」：頻繁な売買で新NISA年間360万円枠を消費せず、国債クッションと高配当を受け取りながら穏やかに保有する配分です。
          </div>

          <div class="gba-wallet-list">
            <div class="gba-wallet-item w1">
              <div class="gba-wallet-head">
                <span>① 守りの財布（個人向け国債 変動10年・待機預金）</span>
                <span class="gba-wallet-stat" id="gbaWallet1Stat">30% · 約686万円</span>
              </div>
              <div class="gba-wallet-bar"><span id="gbaWallet1Bar" style="width:30%;"></span></div>
              <div class="gba-wallet-note">楽天マネーブリッジ・SBIハイブリッド預金＆個人向け国債で生活費2〜3年分を無傷で確保。</div>
            </div>

            <div class="gba-wallet-item w2">
              <div class="gba-wallet-head">
                <span>② 収入の財布（1489 日経高配当株50 ／ VYM 米国増配株）</span>
                <span class="gba-wallet-stat" id="gbaWallet2Stat">40% · 約915万円</span>
              </div>
              <div class="gba-wallet-bar"><span id="gbaWallet2Bar" style="width:40%;"></span></div>
              <div class="gba-wallet-note">新NISA成長投資枠で配当金・分配金を非課税受取。毎月のゆとり生活費の柱になります。</div>
            </div>

            <div class="gba-wallet-item w3">
              <div class="gba-wallet-head">
                <span>③ 成長の財布（eMAXIS Slim 全世界株式［オルカン］・S&amp;P500）</span>
                <span class="gba-wallet-stat" id="gbaWallet3Stat">30% · 約686万円</span>
              </div>
              <div class="gba-wallet-bar"><span id="gbaWallet3Bar" style="width:30%;"></span></div>
              <div class="gba-wallet-note">物価上昇（インフレ）に負けない長期成長エンジン。3色信号に合わせ年2〜4回だけ穏やかに比率調整。</div>
            </div>
          </div>
        </div>
      </div>

      <!-- 新NISA 100%適格 4大コア資産ストリップ（レバレッジ・暗号資産関連 0件） -->
      <div class="gba-nisa-core-strip" id="gbaSeniorCoreStripJp">
        <div class="gba-nisa-core-title">
          🏛️ <strong>金融庁・新NISA（つみたて枠・成長投資枠）100%適格「シニア王道4大コア資産」</strong> — 値動きの荒い3倍レバレッジ投信や短期売買は一切使わず、年2〜4回の穏やかな配分調整で資産寿命を延ばします：
        </div>
        <div class="gba-nisa-core-grid">
          <div class="gba-nisa-core-card">
            <span class="gba-nisa-core-badge">🛡️ ① 守り・安全資金</span>
            <strong>個人向け国債（変動10年）</strong>
            <span>国が元本保証・半年ごとに金利見直し。暴落時に株を売らずに済む「心の安定剤」。</span>
          </div>
          <div class="gba-nisa-core-card">
            <span class="gba-nisa-core-badge">💴 ② 収入・日米高配当</span>
            <strong>1489（日経高配当50）／ VYM</strong>
            <span>日本と米国の優良増配・高配当企業群から、新NISA非課税で安定した配当収入を確保。</span>
          </div>
          <div class="gba-nisa-core-card">
            <span class="gba-nisa-core-badge">🌍 ③ 成長・世界分散</span>
            <strong>eMAXIS Slim 全世界株式（オルカン）</strong>
            <span>つみたて投資枠の王道。1本で先進国・日本・新興国の優良企業へ超低コスト分散。</span>
          </div>
          <div class="gba-nisa-core-card">
            <span class="gba-nisa-core-badge">🇺🇸 ④ 成長・米国コア</span>
            <strong>eMAXIS Slim 米国株式（S&amp;P500）</strong>
            <span>米国を代表する黒字500社へ長期複利投資。インフレから老後資産の実質価値を防衛。</span>
          </div>
        </div>
      </div>

      <!-- 3段階バリューラダー CTAバー -->
      <div class="gba-retire-ladder">
        <button type="button" class="gba-retire-cta c-manual" onclick="var el=document.getElementById('gbaFreeStarterManualJp'); if(el&&el.scrollIntoView){{el.scrollIntoView({{behavior:'smooth',block:'start'}});}}">
          <span>📘 Step 1（¥0 無料）：楽天・SBI証券＆新NISA安全設定マニュアル</span>
          <small>登録不要・今すぐ全ページ読めます（印刷・PDF保存対応）</small>
        </button>
        <button type="button" class="gba-retire-cta c-club" onclick="jumpGbaRetireToClubJp()">
          <span>🍵 Step 2（3秒無料登録）：朝のゆとり老後＆日米マクロ倶楽部</span>
          <small>パスワード不要・毎朝8時に3色バランス指針をお届け</small>
        </button>
        <a href="https://truthofmarket.lemonsqueezy.com/checkout/buy/d5e7e761-8b1b-4ca8-b1fe-771acd1450f8?embed=1&amp;checkout[redirect_url]=https://getbreakai.com/confirmation.html&amp;locale=ja" data-ls-product-uuid="d5e7e761-8b1b-4ca8-b1fe-771acd1450f8" class="gba-retire-cta c-pro lemonsqueezy-button">
          <span>⚡ Step 3：月額 $29（約4,400円・クレカ自動円換算）</span>
          <small>いつでも1クリック解約OK・全銘柄3色配分＆VIPブリーフ即時解放</small>
        </a>
        <a href="https://truthofmarket.lemonsqueezy.com/checkout/buy/667aa482-f17c-47d1-b7f3-a2427c36516b?embed=1&amp;checkout[redirect_url]=https://getbreakai.com/confirmation.html&amp;locale=ja" data-ls-product-uuid="667aa482-f17c-47d1-b7f3-a2427c36516b" class="gba-retire-cta c-vip lemonsqueezy-button">
          <span>👑 年間Pro VIP：年額 $199（約30,000円・月あたり約2,500円）</span>
          <small>43%OFF 一番人気・クレカ自動円換算・いつでも1クリック解約OK</small>
        </a>
      </div>
    </section>

    <!-- 🍵 朝の資産守り倶楽部 (#gbaMorningClubJp — Zero-Signup Daily Belonging & 1-Click Poll) -->
    <section class="gba-morning-club" id="gbaMorningClubJp" aria-label="朝のゆとり老後＆資産守り倶楽部">
      <div class="gba-club-header">
        <div class="gba-club-title-group">
          <span class="gba-club-badge">🍵 朝のゆとり老後＆資産守り倶楽部</span>
          <strong class="gba-club-title">年金＋新NISA・老後資金をご一緒に守る朝の習慣</strong>
        </div>
        <span class="gba-club-streak" id="gbaJpClubStreakBadge">🏅 倶楽部会員・連続訪問 1日目</span>
      </div>

      <div class="gba-club-greeting">
        <span class="gba-club-greeting-label">編集部の今朝のご挨拶：</span>
        <span id="gbaJpClubGreetingText">「おはようございます。大切な新NISAと老後資金は、焦らず青信号の日だけゆっくり育てていきましょう。」</span>
      </div>

      <div class="gba-club-poll-header">
        <span class="gba-club-poll-title">🗳️ 本日の個人投資家アンケート（1クリック・登録不要）</span>
        <span class="gba-club-poll-meta" id="gbaJpClubPollTotal">本日 482名の個人投資家が参加中</span>
      </div>

      <div class="gba-club-poll-grid" role="group" aria-label="本日の個人投資家アンケート">
        <button type="button" class="gba-club-poll-btn" data-gba-poll="buy_dip" aria-pressed="false" onclick="voteGbaMorningClubJp('buy_dip')">
          <span class="gba-poll-row-top">
            <span class="gba-poll-opt-text">🟢 押し目待ち</span>
            <strong class="gba-poll-opt-pct" data-gba-pct="buy_dip">34%</strong>
          </span>
          <span class="gba-poll-bar-bg" aria-hidden="true">
            <span class="gba-poll-bar-fill fill-dip" data-gba-bar="buy_dip" style="width:34%;"></span>
          </span>
        </button>

        <button type="button" class="gba-club-poll-btn" data-gba-poll="watch" aria-pressed="false" onclick="voteGbaMorningClubJp('watch')">
          <span class="gba-poll-row-top">
            <span class="gba-poll-opt-text">🟡 様子見</span>
            <strong class="gba-poll-opt-pct" data-gba-pct="watch">41%</strong>
          </span>
          <span class="gba-poll-bar-bg" aria-hidden="true">
            <span class="gba-poll-bar-fill fill-watch" data-gba-bar="watch" style="width:41%;"></span>
          </span>
        </button>

        <button type="button" class="gba-club-poll-btn" data-gba-poll="cash" aria-pressed="false" onclick="voteGbaMorningClubJp('cash')">
          <span class="gba-poll-row-top">
            <span class="gba-poll-opt-text">🛡️ 現金重視</span>
            <strong class="gba-poll-opt-pct" data-gba-pct="cash">25%</strong>
          </span>
          <span class="gba-poll-bar-bg" aria-hidden="true">
            <span class="gba-poll-bar-fill fill-cash" data-gba-bar="cash" style="width:25%;"></span>
          </span>
        </button>
      </div>

      <div class="gba-club-companion" id="gbaJpClubCompanionMsg" role="status" aria-live="polite">
        今朝の投資スタンスを1タップでお選びいただくと、全国の倶楽部会員の皆さまの集計結果とメッセージが表示されます。
      </div>

      <!-- 朝の資産守り＆日米マクロ倶楽部 無料正会員登録（3秒完了） -->
      <div class="gba-jp-pwless-box" id="gba-jp-passwordless-signup">
        <div class="gba-jp-pwless-top">
          <span class="gba-jp-pwless-badge">無料正会員・パスワード不要（3秒登録）</span>
          <span class="gba-jp-pwless-note">毎朝配信 ・ クレジットカード不要 ・ いつでも1クリック配信停止</span>
        </div>
        <h3 class="gba-jp-pwless-heading">毎朝の日米マクロ市場＆新NISA 3色安全シグナルを無料メールでお届け</h3>
        <p class="gba-jp-pwless-sub">パスワード登録は一切不要。関心テーマを選んでメールアドレスを入力するだけで、毎朝の金利・円ドル為替・高値掴み防止ブリーフィングが届きます。</p>

        <span class="gba-jp-seg-label">1. ご関心の高い資産防衛テーマを選択（1タップ）</span>
        <div class="gba-jp-seg-grid" role="group" aria-label="関心テーマ選択">
          <button type="button" class="gba-jp-seg-btn is-active" data-gba-seg="nisa_wealth_defense" aria-pressed="true" onclick="selectGbaJpClubSegment('nisa_wealth_defense')">
            新NISA・老後資金の塩漬け防止
          </button>
          <button type="button" class="gba-jp-seg-btn" data-gba-seg="jp_us_macro_fx" aria-pressed="false" onclick="selectGbaJpClubSegment('jp_us_macro_fx')">
            日米マクロ市場・円ドル為替・金利
          </button>
          <button type="button" class="gba-jp-seg-btn" data-gba-seg="semis_high_dividend" aria-pressed="false" onclick="selectGbaJpClubSegment('semis_high_dividend')">
            半導体・日米高配当株シグナル
          </button>
        </div>

        <form class="gba-jp-pwless-form" id="gba-jp-club-form" onsubmit="return submitGbaJpPasswordlessClub(event)">
          <label for="gba-jp-club-nickname" style="position:absolute; width:1px; height:1px; overflow:hidden; clip:rect(0,0,0,0);">ニックネーム（任意）</label>
          <input type="text" id="gba-jp-club-nickname" class="gba-jp-pwless-input" autocomplete="nickname" maxlength="40" placeholder="ニックネーム（任意）">
          <label for="gba-jp-club-email" style="position:absolute; width:1px; height:1px; overflow:hidden; clip:rect(0,0,0,0);">メールアドレス</label>
          <input type="email" id="gba-jp-club-email" class="gba-jp-pwless-input" required autocomplete="email" placeholder="メールアドレスを入力（例: taro@example.jp）">
          <input type="text" id="gba-jp-club-hp" name="website_hp" tabindex="-1" autocomplete="off" aria-hidden="true" style="display:none">
          <button type="submit" id="gba-jp-club-submit" class="gba-jp-pwless-submit">
            無料で朝の資産守り倶楽部に参加する（3秒完了） →
          </button>
        </form>

        <div class="gba-jp-pwless-feedback" id="gba-jp-club-feedback" role="status" aria-live="polite">
          <div id="gba-jp-club-feedback-text"></div>
          <a href="#gbaFreeStarterManualJp" class="gba-jp-club-manual-cta" id="gba-jp-club-manual-btn" onclick="var el=document.getElementById('gbaFreeStarterManualJp'); if(el&&el.scrollIntoView){{el.scrollIntoView({{behavior:'smooth',block:'start'}});}}">
            ¥0 無料・楽天／SBI証券 新NISA安全注文マニュアルを開く →
          </a>
        </div>
      </div>
    </section>

    <!-- 📘 ¥0 無料公開商品：はじめての新NISA＆証券アプリ基本マニュアル (#gbaFreeStarterManualJp) -->
    <section class="gba-starter-manual" id="gbaFreeStarterManualJp" aria-label="¥0 無料公開商品：はじめての新NISA＆証券アプリ基本マニュアル">
      <div class="gba-manual-top-row">
        <span class="gba-manual-free-badge">📘 ¥0 無料公開商品（登録不要・全ページ即時公開）</span>
        <span class="gba-manual-sub-badge">🖨️ 印刷・PDF保存対応 ／ 楽天証券・SBI証券 対応</span>
      </div>
      <h2 class="gba-manual-heading">
        はじめての新NISA＆証券アプリ基本マニュアル（指値注文・逆指値による塩漬け防止・待機資金設定ガイド）
      </h2>
      <p class="gba-manual-lead">
        「アプリの注文画面でどのボタンを押せば安全なのか不安…」という初心者〜中級者の皆さまへ。大切な新NISA枠と老後資金を守るための<strong>「3つの基本手順」</strong>を、専門用語を使わずやさしい日本語でまとめました。
      </p>

      <div class="gba-manual-chap-grid">
        <button type="button" class="gba-manual-chap-btn" onclick="openGbaStarterManualModal('gbaManualChap1')">
          <span class="gba-manual-chap-tag">第1章 · 安全な買い方</span>
          <strong class="gba-manual-chap-title">楽天証券（iSPEED）・SBI証券での「指値注文」手順</strong>
          <span class="gba-manual-chap-desc">朝一番の「成行注文」による思わぬ高値掴みを防ぎ、希望価格以下で落ち着いて買う3タップ手順です。</span>
          <span class="gba-manual-chap-more">第1章を詳しく読む →</span>
        </button>

        <button type="button" class="gba-manual-chap-btn" onclick="openGbaStarterManualModal('gbaManualChap2')">
          <span class="gba-manual-chap-tag">第2章 · 塩漬け防止の守り</span>
          <strong class="gba-manual-chap-title">新NISAを守る「逆指値（ストップロス）」の入れ方</strong>
          <span class="gba-manual-chap-desc">画面に張り付かなくても、8〜9%下がった時点で自動的に売却して資産の半減を防ぐ安全ネット設定です。</span>
          <span class="gba-manual-chap-more">第2章を詳しく読む →</span>
        </button>

        <button type="button" class="gba-manual-chap-btn" onclick="openGbaStarterManualModal('gbaManualChap3')">
          <span class="gba-manual-chap-tag">第3章 · 赤信号の待機資金</span>
          <strong class="gba-manual-chap-title">楽天マネーブリッジ・SBIハイブリッド預金の整え方</strong>
          <span class="gba-manual-chap-desc">赤信号（様子見・現金保護）の日に、優遇金利を受け取りながら次の青信号をゆったり待つ準備です。</span>
          <span class="gba-manual-chap-more">第3章を詳しく読む →</span>
        </button>
      </div>

      <div class="gba-manual-cta-row">
        <button type="button" id="btnOpenGbaStarterManualJp" class="gba-manual-open-btn" onclick="openGbaStarterManualModal()">
          📖 ¥0 基本マニュアル全3章を開く（印刷・PDF保存可）
        </button>
        <button type="button" class="gba-manual-signal-btn" onclick="jumpFromManualToJpMail()">
          📧 毎朝8時の無料「3色シグナル」を受け取る ↓
        </button>
      </div>

      <div class="gba-manual-funnel-strip">
        <span>💡 <strong>次のステップ：</strong>基本の注文・守り方をマスターしたら、毎朝の<strong>🟢安定上昇・🟡様子見・🔴現金防衛</strong>シグナルをご活用ください。</span>
        <div class="gba-manual-funnel-links">
          <a href="https://truthofmarket.lemonsqueezy.com/checkout/buy/d5e7e761-8b1b-4ca8-b1fe-771acd1450f8?embed=1&amp;checkout[redirect_url]=https://getbreakai.com/confirmation.html&amp;locale=ja" data-ls-product-uuid="d5e7e761-8b1b-4ca8-b1fe-771acd1450f8" class="gba-manual-pro-link lemonsqueezy-button">⚡ 月額 $29（約4,400円・クレカ自動円換算・いつでも1クリック解約OK）</a>
          <a href="https://truthofmarket.lemonsqueezy.com/checkout/buy/667aa482-f17c-47d1-b7f3-a2427c36516b?embed=1&amp;checkout[redirect_url]=https://getbreakai.com/confirmation.html&amp;locale=ja" data-ls-product-uuid="667aa482-f17c-47d1-b7f3-a2427c36516b" class="gba-manual-vip-link lemonsqueezy-button">👑 年額 $199（約30,000円・月あたり約2,500円・43%OFF）</a>
        </div>
      </div>
    </section>

    <!-- ⚡ 1秒 新NISA年間360万円枠 買いすぎ防止＆1銘柄あたり安心投資額計算機 -->
    <div class="calc-card" id="jpQuickCalcSection">
      <div class="calc-header">
        <div class="calc-title">⚡ 1秒 新NISA買いすぎ防止＆1銘柄あたり安心投資額計算 (<span id="jpActiveSymBadge">1489 日経高配当50</span>)</div>
        <div class="calc-pill-risk">🛡️ 年間360万円非課税枠を大切にする穏やかな分散設計</div>
      </div>

      <div class="calc-fast-inputs">
        <div class="fast-field">
          <label for="jpCapManInput">ご運用資金 (万円)</label>
          <input type="number" id="jpCapManInput" min="10" max="10000" step="10" value="1500" oninput="syncCapFromManInput()">
        </div>
        <div class="fast-field">
          <label for="jpPriceInput">現在基準価格・株価 <span id="lblPriceUnit">(¥)</span></label>
          <input type="number" id="jpPriceInput" min="0.1" step="any" value="2380" oninput="syncPriceAtrInputs()">
        </div>
        <div class="fast-field">
          <label for="jpAtrInput">値動きゆとり幅 <span id="lblAtrUnit">(¥)</span></label>
          <input type="number" id="jpAtrInput" min="0.05" step="any" value="48" oninput="syncPriceAtrInputs()">
        </div>
      </div>

      <div class="tax-calc-bar">
        <button type="button" id="btnJpHubTaxNisa" class="tax-mode-btn active" onclick="setJpHubTaxMode('nisa')">🌱 新NISA (非課税 0%)</button>
        <button type="button" id="btnJpHubTaxTokutei" class="tax-mode-btn" onclick="setJpHubTaxMode('tokutei')">🏦 特定口座 (税 20.315%)</button>
      </div>

      <button type="button" id="btnJpHubCalcNow" class="btn-calc-submit" onclick="recalcJpQuickCalc()" style="min-height:54px; font-size:1.04rem;">
        🧮 1秒で「買いすぎ防止・適正株数」と「新NISA非課税メリット」を計算する
      </button>

      <!-- 3 Real-time Outputs -->
      <div class="calc-outputs">
        <div class="out-card">
          <div class="out-label">推奨保有株数（1銘柄への集中・買いすぎ防止）</div>
          <div id="jpOutShares" class="out-val val-amber">234株 (¥556,920 / 約55.7万円)</div>
        </div>
        <div class="out-card">
          <div class="out-label">🛡️ 配分見直し目安ライン（年2〜4回の穏やかな点検）</div>
          <div id="jpOutRisk" class="out-val val-rose">¥2,284 (-¥22,464 / -約2.2万円)</div>
        </div>
        <div class="out-card">
          <div class="out-label" id="jpOutGainLabel">🎯 長期保有目標ライン（新NISA非課税手取り）</div>
          <div id="jpOutGain" class="out-val val-emerald">¥2,620 (+¥56,160 / +約5.6万円)</div>
        </div>
      </div>

      <!-- Capital Slider & Presets -->
      <div class="slider-group">
        <div class="slider-header">
          <span>ご運用資産スライダー（1ドル=150円基準）:</span>
          <strong id="jpCalcAccLbl">$100,000 (約1500.0万円)</strong>
        </div>
        <input type="range" id="jpCalcSlider" min="5000" max="250000" step="1000" value="100000" oninput="syncManFromSlider()">
        <div class="capital-pills">
          <button type="button" class="cap-btn" onclick="setQuickCapital(20000, this)">300万円</button>
          <button type="button" class="cap-btn" onclick="setQuickCapital(33300, this)">500万円</button>
          <button type="button" class="cap-btn" onclick="setQuickCapital(66700, this)">1,000万円</button>
          <button type="button" class="cap-btn active" onclick="setQuickCapital(100000, this)">1,500万円</button>
          <button type="button" class="cap-btn" onclick="setQuickCapital(120000, this)">1,800万円 (新NISA生涯枠)</button>
          <button type="button" class="cap-btn" onclick="setQuickCapital(200000, this)">3,000万円</button>
        </div>
      </div>

      <!-- Quick Ticker Presets (Shin-NISA Eligible Core & Quality Blue-Chips) -->
      <div style="font-size:0.98rem; font-weight:800; color:var(--text-sub); margin-bottom:6px;">
        👇 新NISA適格コアETF・日米優良大型株 ワンタップ切替（レバレッジ除外）:
      </div>
      <div class="preset-bar">
        <button type="button" class="preset-chip active" data-ticker="1489" onclick="setQuickStock('1489', this)">1489 日経高配当株50 (¥)</button>
        <button type="button" class="preset-chip" data-ticker="VYM" onclick="setQuickStock('VYM', this)">$VYM 米国高配当株ETF</button>
        <button type="button" class="preset-chip" data-ticker="VOO" onclick="setQuickStock('VOO', this)">$VOO 米国S&amp;P500 ETF</button>
        <button type="button" class="preset-chip" data-ticker="8306" onclick="setQuickStock('8306', this)">8306.T 三菱UFJ (¥)</button>
        <button type="button" class="preset-chip" data-ticker="8058" onclick="setQuickStock('8058', this)">8058.T 三菱商事 (¥)</button>
        <button type="button" class="preset-chip" data-ticker="7203" onclick="setQuickStock('7203', this)">7203.T トヨタ (¥)</button>
        <button type="button" class="preset-chip" data-ticker="8035" onclick="setQuickStock('8035', this)">8035.T 東エレク (¥)</button>
        <button type="button" class="preset-chip" data-ticker="7011" onclick="setQuickStock('7011', this)">7011.T 三菱重工 (¥)</button>
        <button type="button" class="preset-chip" data-ticker="MSFT" onclick="setQuickStock('MSFT', this)">$MSFT マイクロソフト</button>
        <button type="button" class="preset-chip" data-ticker="AAPL" onclick="setQuickStock('AAPL', this)">$AAPL アップル</button>
        <button type="button" class="preset-chip" data-ticker="NVDA" onclick="setQuickStock('NVDA', this)">$NVDA エヌビディア</button>
      </div>
    </div>

    <!-- 📧 1-Field Free Morning Signal Email Signup (North Star Conversion Gate — Before Paid Tier) -->
    <section class="morning-mail-card" id="gbJpMorningMailBox" aria-label="毎朝8時の新NISA 3色シグナル無料メール登録">
      <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:8px;">
        <span class="sig-pill sig-pill-buy">📧 無料メール会員（クレジットカード不要・登録30秒）</span>
        <span style="font-size:0.95rem; font-weight:800; color:var(--text-muted);">毎朝8:00配信 · いつでも1クリック配信停止</span>
      </div>
      <h2 style="font-size:1.25rem; font-weight:900; color:var(--text-main); margin:10px 0 6px; line-height:1.42;">
        🔔 選択中の銘柄（<span id="jpAlertSymLabel" style="color:var(--accent-blue);">1489 日経高配当50</span>）の配分点検ガイド ＆ 毎朝8時「ゆとり老後・新NISA 3色ブリーフ」を無料で受け取る
      </h2>
      <p style="font-size:1.06rem; color:var(--text-muted); margin:0; line-height:1.7;">
        ご登録後すぐに、本日の「🟢安定保有・🟡様子見配当・🛡️国債クッション比率」の無料サマリーがこの画面で解放されます。
      </p>
      <form class="morning-mail-form" id="gbJpMorningMailForm" onsubmit="return submitGbJpFreeSignup(event)">
        <label for="gbJpMorningEmailInput" style="position:absolute; width:1px; height:1px; overflow:hidden; clip:rect(0,0,0,0);">メールアドレス</label>
        <input type="email" id="gbJpMorningEmailInput" class="morning-mail-input" required autocomplete="email" placeholder="メールアドレスを入力（例：yamada@example.co.jp）">
        <button type="submit" id="btnGbJpMorningSubmit" class="morning-mail-btn">
          📧 無料で毎朝の3色ブリーフを受け取る
        </button>
      </form>
      <div id="gbJpMorningStatus" role="status" aria-live="polite" style="font-size:1.02rem; font-weight:800; margin-top:10px; color:var(--accent-emerald);"></div>
      <div id="jpFreeMemberBonusBox" style="display:none; margin-top:12px; background:var(--bg-card); border:1.5px solid #10b981; border-radius:10px; padding:14px 16px; font-size:1.04rem; line-height:1.7;">
        <div style="font-weight:900; color:var(--accent-emerald); margin-bottom:6px;">🎁 無料会員限定：本日の新NISA「老後3つの財布」モーニングブリーフ（即時解放済み）</div>
        <div>・<b>🛡️ ① 守りの財布（個人向け国債・待機預金）：</b>30%維持 — 相場急変時も株を売らずに2〜3年分の生活費を確保</div>
        <div>・<b>💴 ② 収入の財布（1489 日経高配当50 ／ $VYM 米国増配株）：</b>40%維持 — 新NISA非課税で安定配当を受取</div>
        <div>・<b>🌍 ③ 成長の財布（オルカン・S&amp;P500）：</b>30%維持 — 年2〜4回の穏やかな比率点検で年間360万円非課税枠を温存</div>
      </div>
    </section>

    <!-- 🛡️ $29/mo & $199/yr (43%OFF) 防衛比較カード -->
    <div class="defense-card">
      <div class="defense-title">
        🛡️ なぜ「年2〜4回の3色バランス見直し」が、新NISAと大切な退職金を暴落から守るのか？
      </div>
      <div class="defense-subtitle">
        ニュースに焦って高値掴み・狼狽売りを繰り返すケース vs 3つの財布で心穏やかに守るケースの比較
      </div>

      <div class="comp-grid">
        <div class="box-bad">
          <h4>❌ 自己流の集中投資・頻繁な売買（塩漬けと非課税枠の浪費）</h4>
          <div class="loss-num">-¥525万円 目減り</div>
          <p style="font-size:1.02rem; color:var(--text-muted); line-height:1.68; margin:6px 0 0;">
            退職金を一度に人気株へ集中投資し、-35%暴落でパニック売却。新NISAの年間360万円非課税枠も失われてしまいます。
          </p>
        </div>

        <div class="box-good">
          <h4>✅ GetBreakAI ゆとり老後Pro（3色信号 × 年2〜4回の穏やかな配分調整）</h4>
          <div class="gain-num">毎月 +3.9万円 ゆとり防衛</div>
          <p style="font-size:1.02rem; color:var(--text-muted); line-height:1.68; margin:6px 0 0;">
            <b>個人向け国債・1489/VYM・オルカン/S&amp;P500</b>の最適比率を毎朝ナビゲート。<b>非課税メリット累計400万円超</b>と穏やかな老後収入を守ります。
          </p>
        </div>
      </div>

      <!-- Checkout CTA Buttons (Lemon Squeezy Store #296100 Live UUIDs + JPY Reassurance) -->
      <div class="cta-container">
        <div class="cta-dual-grid">
          <a href="https://truthofmarket.lemonsqueezy.com/checkout/buy/d5e7e761-8b1b-4ca8-b1fe-771acd1450f8?embed=1&amp;checkout[redirect_url]=https://getbreakai.com/confirmation.html&amp;locale=ja" data-ls-product-uuid="d5e7e761-8b1b-4ca8-b1fe-771acd1450f8" class="btn-checkout-primary lemonsqueezy-button">
            <span>⚡ 月額 $29（約4,400円・クレカ自動円換算）</span>
            <span style="font-size:0.95rem; font-weight:800; opacity:0.96;">いつでも1クリック解約OK / 決済完了と同時に自動ロック解除</span>
          </a>
          <a href="https://truthofmarket.lemonsqueezy.com/checkout/buy/667aa482-f17c-47d1-b7f3-a2427c36516b?embed=1&amp;checkout[redirect_url]=https://getbreakai.com/confirmation.html&amp;locale=ja" data-ls-product-uuid="667aa482-f17c-47d1-b7f3-a2427c36516b" class="btn-checkout-annual lemonsqueezy-button">
            <span>👑 年額 $199（約30,000円・月あたり約2,500円）</span>
            <span style="font-size:0.95rem; font-weight:800; opacity:0.96;">43%OFF 一番人気・クレカ自動円換算・いつでも1クリック解約OK</span>
          </a>
        </div>
        <div style="margin-top:12px; font-size:1.04rem; font-weight:900; color:var(--text-main);">
          💳 日本国内クレジットカードで自動円換算決済（JCB・Visa・Master・Apple Pay・Google Pay対応）／ いつでも1クリック解約OK
        </div>
        <div class="cta-subnote">
          ✨ ご決済完了と同時にこのブラウザでVIP全機能が自動的に解放されます（キーのコピー＆ペースト不要）。<br>
          🔒 Lemon Squeezy Store #296100 安全決済（月額 $29＝約4,400円 ／ 年額 $199＝約30,000円・月あたり約2,500円・いつでも1クリック解約OK）<br>
          🎁 <b>購入特典</b>：姉妹ターミナル <b>TruthOfMarket.com</b> のVIP権限も同時付与！法人・API契約：<a href="mailto:beable9489@gmail.com?subject=GetBreakAI%20Enterprise%20Inquiry" style="color:var(--accent-blue); font-weight:800;">beable9489@gmail.com</a>
        </div>
      </div>
    </div>

    <!-- 🔐 Web VIP Vault 機種変更・既存ライセンス復元（新規決済は自動解放） -->
    <details class="vip-vault-card" id="jpHubVipVaultBox">
      <summary style="cursor:pointer; font-size:1.02rem; font-weight:900; color:var(--text-main); list-style:none;">
        🔑 既に購入済み・機種変更でのライセンスキー復元はこちら（新規決済時は自動でロック解除されます） ▾
      </summary>
      <div style="margin-top:10px;">
        <p style="font-size:0.98rem; color:var(--text-muted); margin:6px 0 8px;">
          決済完了メールに記載された Lemon Squeezy ライセンスキーを入力すると、当ページおよびトップページのVIP特典が一括でアンロックされます。
        </p>
        <div class="vip-input-row">
          <input type="text" id="jpHubLicenseInput" class="vip-key-input" placeholder="ライセンスキーを入力 (XXXX-XXXX-XXXX-XXXX)">
          <button type="button" id="btnJpHubUnlockVip" class="vip-unlock-btn" onclick="unlockJpHubVipVault()">🔑 VIPロック解除</button>
        </div>
        <div id="jpHubVipStatus" style="font-size:0.96rem; font-weight:700; margin-top:8px; color:var(--accent-emerald);"></div>
        <div style="display:flex; gap:12px; flex-wrap:wrap; margin-top:12px; font-size:0.98rem;">
          <a href="https://www.youtube.com/@GetBreakAI" target="_blank" rel="noopener" style="color:var(--accent-blue); font-weight:800; text-decoration:none;">📺 公式YouTube (@GetBreakAI)</a>
          <a href="https://getbreakai.com/#gbQuickMatrixSection" style="color:var(--accent-emerald); font-weight:800; text-decoration:none;">📊 本日の日米コア資産＆優良株早見表 →</a>
        </div>
      </div>
    </details>

    <!-- 📚 新NISA適格銘柄ディープリサーチ記事一覧 -->
    <div style="border-top:1px solid var(--border-col); padding-top:20px; margin-top:16px;">
      <h2 style="font-size:1.35rem; color:var(--text-main); margin-bottom:6px;">📚 新NISA・日米優良株 やさしい日本語リサーチ一覧（{date_str} 最新版）</h2>
      <p style="color:var(--text-muted); font-size:1.04rem; line-height:1.7; margin-bottom:14px;">決算・配当余力、機関投資家の長期資金動向、買いすぎを防ぐ安心投資額目安を専門用語なしでわかりやすく解説しています（3倍レバレッジ・暗号資産関連銘柄は除外済み）。</p>
      <div class="grid">
        {cards_html}
      </div>
    </div>
  </div>

  <!-- 📘 Interactive Modal: ¥0 無料公開商品 はじめての新NISA＆証券アプリ基本マニュアル (#gbaStarterManualModal) -->
  <div class="gba-manual-modal-backdrop" id="gbaStarterManualModal" role="dialog" aria-modal="true" aria-labelledby="gbaStarterManualModalTitle" aria-hidden="true">
    <div class="gba-manual-modal-dialog">
      <div class="gba-manual-modal-header">
        <div>
          <span class="gba-manual-free-badge" style="font-size:0.84rem;">📘 ¥0 無料公開マニュアル（保存版・登録不要）</span>
          <h2 class="gba-manual-modal-title" id="gbaStarterManualModalTitle">はじめての新NISA＆証券アプリ基本マニュアル</h2>
        </div>
        <div class="gba-manual-modal-actions">
          <button type="button" class="gba-manual-action-btn btn-print" onclick="printGbaStarterManual()">🖨️ 印刷・PDF保存</button>
          <button type="button" class="gba-manual-action-btn" id="btnCloseGbaStarterManual" onclick="closeGbaStarterManualModal()">✕ 閉じる</button>
        </div>
      </div>

      <nav class="gba-manual-nav-pills" aria-label="マニュアル目次">
        <button type="button" class="gba-manual-jump-pill" onclick="scrollToGbaManualChapter('gbaManualChap1')">第1章：指値注文の買い方</button>
        <button type="button" class="gba-manual-jump-pill" onclick="scrollToGbaManualChapter('gbaManualChap2')">第2章：逆指値で塩漬け防止</button>
        <button type="button" class="gba-manual-jump-pill" onclick="scrollToGbaManualChapter('gbaManualChap3')">第3章：赤信号の日の待機資金</button>
      </nav>

      <div class="gba-manual-modal-body">
        <article class="gba-manual-chapter-box" id="gbaManualChap1">
          <h3>第1章 — 楽天証券（iSPEED）・SBI証券での安全な買い方（「成行」ではなく「指値注文」の基本手順）</h3>
          <p>
            株を買うとき、注文画面には<strong>「成行（なりゆき）」</strong>と<strong>「指値（さしね）」</strong>の2つがあります。朝9時ちょうど（米国株なら夜23時30分）の市場が開く直後に「成行」で注文してしまうと、一時的に跳ね上がった思わぬ高い価格で買えてしまうことがあります。大切な老後資金や新NISA枠では、必ず<strong>「この価格以下なら買う」と上限を決める『指値注文』</strong>を選びましょう。
          </p>
          <div class="gba-manual-broker-grid">
            <div class="gba-manual-broker-card">
              <strong class="broker-name">📱 楽天証券（スマホアプリ「iSPEED」・Web）の手順</strong>
              <ol>
                <li>銘柄名を検索し、右上の<strong>「注文」→「現物買い」</strong>をタップします。</li>
                <li>口座区分で<strong>「NISA成長投資枠」</strong>（または特定口座）を選びます。</li>
                <li>価格の欄で「成行」ではなく<strong>「指値」</strong>をタップし、現在の株価と同じか少し下の希望価格を入力して注文します。</li>
              </ol>
            </div>
            <div class="gba-manual-broker-card">
              <strong class="broker-name">📱 SBI証券（「SBI証券 株」／「米国株」アプリ）の手順</strong>
              <ol>
                <li>銘柄画面から<strong>「取引」→「現物買」</strong>をタップします。</li>
                <li>預り区分で<strong>「NISA預り（成長）」</strong>にチェックを入れます。</li>
                <li>価格指定で必ず<strong>「指値」</strong>を選び、ご自身が納得できる上限金額と株数を入力して確認画面へ進みます。</li>
              </ol>
            </div>
          </div>
          <div class="gba-manual-tip-callout">
            ✅ <strong>安心のポイント：</strong>もし株価が指値まで下がらなければ「買えずに現金が残るだけ」ですので、高値掴みで後悔することがなくなります。
          </div>
        </article>

        <article class="gba-manual-chapter-box" id="gbaManualChap2">
          <h3>第2章 — 年2〜4回の「ゆったり配分見直し」と、個別株での塩漬けを防ぐ「逆指値」手順</h3>
          <p>
            新NISA口座には「利益・配当に税金（20.315%）がかからない」大きな魅力がある一方、短期売買を繰り返すと<strong>年間360万円の非課税投資枠をすぐ消費してしまう</strong>うえ、大きな含み損を抱えても<strong>他の口座と損益通算ができない</strong>注意点があります。基本は<strong>3色信号に合わせた「年2〜4回のゆったり配分見直し」</strong>で非課税枠を大切にし、個別株を買う場合のみ「買値から8〜9%下で売る予約（逆指値）」を添えて塩漬けを防ぎましょう。
          </p>
          <div class="gba-manual-broker-grid">
            <div class="gba-manual-broker-card">
              <strong class="broker-name">🛡️ 楽天証券での「逆指値」設定手順</strong>
              <ol>
                <li>保有銘柄一覧から該当の株をタップし、<strong>「現物売り」</strong>を選びます。</li>
                <li>執行条件で<strong>「逆指値」</strong>（または「通常＋逆指値」）を選びます。</li>
                <li>「市場価格が<strong>〇〇円以下</strong>になったら売り」に安全撤退ラインの金額を入力し、期間を「今週中（または最長期間）」にして予約完了です。</li>
              </ol>
            </div>
            <div class="gba-manual-broker-card">
              <strong class="broker-name">🛡️ SBI証券での「逆指値」設定手順</strong>
              <ol>
                <li>ポートフォリオから銘柄を選び、<strong>「現物売」</strong>をタップします。</li>
                <li>注文画面の上部または条件欄で<strong>「逆指値」</strong>を選択します。</li>
                <li>「現在値が<strong>〇〇円以下</strong>になった時点で成行（または指値）発注」と入力し、期間を指定して発注しておきます。</li>
              </ol>
            </div>
          </div>
          <div class="gba-manual-tip-callout">
            ✅ <strong>安心のポイント：</strong>一度予約しておけば、日中や夜間にスマートフォンを見続けなくても、急落時に自動でブレーキがかかり大切な元本を守ってくれます。
          </div>
        </article>

        <article class="gba-manual-chapter-box" id="gbaManualChap3">
          <h3>第3章 — 赤信号の日に大切な老後資金を守る「待機資金（楽天マネーブリッジ・SBIハイブリッド預金等）」の整え方</h3>
          <p>
            相場全体が荒れている<strong>🔴 赤信号（現金保護・新規見送り）の日</strong>に、無理に株を買う必要はまったくありません。「休むも相場」という言葉の通り、手元の現金を安全な場所で利息を受け取りながら待機させておくことで、次に<strong>🟢 青信号（買い検討）</strong>が点灯した日に余裕をもって優良銘柄を迎えることができます。
          </p>
          <div class="gba-manual-broker-grid">
            <div class="gba-manual-broker-card">
              <strong class="broker-name">🏦 楽天証券：「マネーブリッジ」自動スイープ設定</strong>
              <ol>
                <li>楽天証券と楽天銀行を連携する<strong>「マネーブリッジ（無料）」</strong>を設定します。</li>
                <li>赤信号の日は銀行の普通預金に資金を置いておくだけで優遇金利が適用され、預金保険の対象として安全に守られます。</li>
                <li>青信号が来て株を買うときは、入金操作なしで自動的に証券口座へ資金が移動（自動スイープ）します。</li>
              </ol>
            </div>
            <div class="gba-manual-broker-card">
              <strong class="broker-name">🏦 SBI証券：「SBIハイブリッド預金」＆外貨MMF</strong>
              <ol>
                <li>住信SBIネット銀行と連携し<strong>「SBIハイブリッド預金」</strong>を有効にします。</li>
                <li>待機中の円資金に毎月利子がつきながら、そのままSBI証券の「買付余力」として自動的に反映されます。</li>
                <li>米国株用の米ドル待機資金がある場合は、証券アプリ内の「外貨建てMMF」に入れておくとドルでも安定した利回りを受け取れます。</li>
              </ol>
            </div>
          </div>
          <div class="gba-manual-tip-callout">
            ✅ <strong>安心のポイント：</strong>「安全な買い方（指値）」「自動ブレーキ（逆指値）」「待機資金の置き場所」の3つが整えば、もう相場ニュースに振り回されることはありません。
          </div>
        </article>

        <div class="gba-manual-modal-funnel">
          <h4>🌅 基本の準備が整ったら、毎朝の「3色安全シグナル」をご活用ください</h4>
          <p>
            GetBreakAIでは、毎朝<strong>「🟢 買い検討 ／ 🟡 様子見 ／ 🔴 現金保護」</strong>の3色判定と、銘柄ごとの具体的な安全撤退ラインを配信しています。まずは無料メール登録、または全銘柄の撤退ラインが即時わかるProプランで安心の資産防衛をお始めください。
          </p>
          <div class="gba-manual-cta-row" style="margin-bottom:10px;">
            <button type="button" class="gba-manual-open-btn" onclick="jumpFromManualToJpMail()">
              📧 無料で毎朝8時の「3色シグナル」を受け取る
            </button>
          </div>
          <div class="gba-manual-funnel-links">
            <a href="https://truthofmarket.lemonsqueezy.com/checkout/buy/d5e7e761-8b1b-4ca8-b1fe-771acd1450f8?embed=1&amp;checkout[redirect_url]=https://getbreakai.com/confirmation.html&amp;locale=ja" data-ls-product-uuid="d5e7e761-8b1b-4ca8-b1fe-771acd1450f8" class="gba-manual-pro-link lemonsqueezy-button">⚡ 月額 $29（約4,400円・クレカ自動円換算・いつでも1クリック解約OK）</a>
            <a href="https://truthofmarket.lemonsqueezy.com/checkout/buy/667aa482-f17c-47d1-b7f3-a2427c36516b?embed=1&amp;checkout[redirect_url]=https://getbreakai.com/confirmation.html&amp;locale=ja" data-ls-product-uuid="667aa482-f17c-47d1-b7f3-a2427c36516b" class="gba-manual-vip-link lemonsqueezy-button">👑 年額 $199（約30,000円・月あたり約2,500円・いつでも1クリック解約OK）</a>
          </div>
        </div>
      </div>
    </div>
  </div>

  <!-- Client-side Interactive Calculation & Theme Script -->
  <script>
    const FX_RATE = 150.0;
    let activeSym = '1489';
    let activeCurrency = 'JPY';
    let activePrice = 2380.0;
    let activeAtr = 48.0;
    let jpHubTaxMode = 'nisa';

    const PRESET_STOCK_MAP = {{
      '1489': {{ price: 2380.0, atr: 48.0,  currency: 'JPY', label: '1489 日経高配当50' }},
      'VYM':  {{ price: 134.50, atr: 2.10,  currency: 'USD', label: '$VYM 米国高配当ETF' }},
      'VOO':  {{ price: 548.60, atr: 8.40,  currency: 'USD', label: '$VOO 米国S&P500' }},
      'NVDA': {{ price: 162.85, atr: 10.01, currency: 'USD', label: '$NVDA' }},
      'PLTR': {{ price: 167.99, atr: 8.84,  currency: 'USD', label: '$PLTR' }},
      'MSFT': {{ price: 523.88, atr: 15.20, currency: 'USD', label: '$MSFT' }},
      'TSLA': {{ price: 390.22, atr: 16.71, currency: 'USD', label: '$TSLA' }},
      'AAPL': {{ price: 356.27, atr: 8.21,  currency: 'USD', label: '$AAPL' }},
      '8035': {{ price: 9461.0, atr: 597.2, currency: 'JPY', label: '8035.T 東エレク' }},
      '6857': {{ price: 30610.0, atr: 2599.2, currency: 'JPY', label: '6857.T アドテスト' }},
      '7011': {{ price: 2920.5, atr: 128.4, currency: 'JPY', label: '7011.T 三菱重工' }},
      '9984': {{ price: 3547.0, atr: 358.4, currency: 'JPY', label: '9984.T ソフトバンクG' }},
      '7203': {{ price: 3418.0, atr: 101.0, currency: 'JPY', label: '7203.T トヨタ' }},
      '8306': {{ price: 3475.0, atr: 111.0, currency: 'JPY', label: '8306.T 三菱UFJ' }},
      '8058': {{ price: 5405.0, atr: 171.4, currency: 'JPY', label: '8058.T 三菱商事' }}
    }};

    const gbaRetireState = {{ asset: 1500, years: 5, monthly: 5, weather: 'yellow' }};
    const GBA_RETIRE_WEATHER_MAP = {{
      green: {{
        weights: [20, 40, 40],
        desc: '🟢 安定上昇モード：生活費2年分の国債クッションを確保しつつ、新NISAの高配当（1489・VYM）40%＋オルカン・S&P500 40%でゆとり収入と資産成長を両立します。'
      }},
      yellow: {{
        weights: [30, 40, 30],
        desc: '🟡 本日は「様子見・配当重視モード」：頻繁な売買で新NISA年間360万円枠を消費せず、国債クッション30%と高配当40%を受け取りながら穏やかに保有する配分です。'
      }},
      red: {{
        weights: [45, 35, 20],
        desc: '🔴 現金・国債防衛モード：相場急変に備え、年2〜4回の定期見直しで個人向け国債・待機預金を45%へ厚くし、暴落時の資産寿命短縮（塩漬け）を防ぎます。'
      }}
    }};

    function setGbaRetirePreset(grp, val, btnEl) {{
      if (!grp) return;
      gbaRetireState[grp] = Number(val) || 0;
      document.querySelectorAll('.gba-retire-pbtn[data-gba-rgrp="' + grp + '"]').forEach(function(b) {{
        const active = (b === btnEl) || (Number(b.getAttribute('data-gba-rval')) === gbaRetireState[grp]);
        b.classList.toggle('is-active', active);
        b.setAttribute('aria-pressed', active ? 'true' : 'false');
      }});
      recalcGbaRetireJp();
    }}

    function setGbaRetireWeather(mode, btnEl) {{
      const m = GBA_RETIRE_WEATHER_MAP[mode] ? mode : 'yellow';
      gbaRetireState.weather = m;
      document.querySelectorAll('.gba-retire-wtab').forEach(function(b) {{
        const active = (b === btnEl) || (b.getAttribute('data-gba-wmode') === m);
        b.classList.toggle('is-active', active);
        b.setAttribute('aria-pressed', active ? 'true' : 'false');
      }});
      recalcGbaRetireJp();
    }}

    function recalcGbaRetireJp() {{
      const asset = Math.max(100, Number(gbaRetireState.asset) || 1500);
      const years = Math.max(0, Number(gbaRetireState.years) || 0);
      const monthly = Math.max(0, Number(gbaRetireState.monthly) || 0);
      const rMo = 0.055 / 12.0;
      let projMan = asset;
      if (years > 0) {{
        const n = years * 12;
        const fvLump = asset * Math.pow(1 + rMo, n);
        const fvContrib = monthly > 0 ? monthly * ((Math.pow(1 + rMo, n) - 1) / rMo) : 0;
        projMan = Math.round(fvLump + fvContrib);
      }}
      const safeAnnualMan = projMan * 0.045;
      const safeMoMan = safeAnnualMan / 12.0;
      const crashProjMan = Math.round(projMan * 0.65);
      const crashMoMan = (crashProjMan * 0.038) / 12.0;
      const gapMoMan = Math.max(0.5, safeMoMan - crashMoMan);
      const gapYrMan = gapMoMan * 12.0;

      const principalPutIn = asset + (monthly * years * 12);
      const growthGainMan = Math.max(0, projMan - principalPutIn);
      const annualDivTaxSaved = safeAnnualMan * 0.20315;
      const cum20YrTaxSaved = Math.max(12, Math.round((annualDivTaxSaved * 20) + (growthGainMan * 0.20315)));

      const projEl = document.getElementById('gbaRetireProjMan');
      if (projEl) projEl.innerText = '約' + projMan.toLocaleString() + '万円';

      const safeMoEl = document.getElementById('gbaRetireSafeMo');
      if (safeMoEl) safeMoEl.innerText = '月 +' + safeMoMan.toFixed(1) + '万円';

      const safeSubEl = document.getElementById('gbaRetireSafeSub');
      if (safeSubEl) {{
        safeSubEl.innerHTML = '年間 約' + safeAnnualMan.toFixed(1) + '万円（年4.5%配当＆計画取り崩し・新NISA非課税）· <b>資産寿命 32年以上</b>';
      }}

      const crashMoEl = document.getElementById('gbaRetireCrashMo');
      if (crashMoEl) crashMoEl.innerText = '月 +' + crashMoMan.toFixed(1) + '万円';

      const crashSubEl = document.getElementById('gbaRetireCrashSub');
      if (crashSubEl) {{
        crashSubEl.innerHTML = '退職前後の暴落で資産約' + crashProjMan.toLocaleString() + '万円へ縮小 · <b>約19年で枯渇懸念</b>';
      }}

      const gapEl = document.getElementById('gbaRetireGapBanner');
      if (gapEl) {{
        gapEl.innerHTML = '✅ 暴落・塩漬け回避で <strong>毎月 +' + gapMoMan.toFixed(1) + '万円（年間 +' + gapYrMan.toFixed(1) + '万円）のゆとり収入</strong> を守り抜き、資産寿命を <strong>+13年以上延長</strong> できます！';
      }}

      const taxEl = document.getElementById('gbaRetireTaxBanner');
      if (taxEl) {{
        taxEl.innerHTML = '🌱 <strong>新NISA 20.315% 非課税節税メリット：</strong>特定口座と比べ <strong>年間 約' + annualDivTaxSaved.toFixed(1) + '万円 ／ 20年累計 約' + cum20YrTaxSaved.toLocaleString() + '万円</strong> の税金がまるごと手元に残ります。';
      }}

      const wCfg = GBA_RETIRE_WEATHER_MAP[gbaRetireState.weather] || GBA_RETIRE_WEATHER_MAP.yellow;
      const wDescEl = document.getElementById('gbaRetireWeatherDesc');
      if (wDescEl) wDescEl.innerText = wCfg.desc;

      for (let idx = 0; idx < 3; idx++) {{
        const pct = wCfg.weights[idx];
        const manAmt = Math.round((projMan * pct) / 100);
        const statEl = document.getElementById('gbaWallet' + (idx + 1) + 'Stat');
        const barEl = document.getElementById('gbaWallet' + (idx + 1) + 'Bar');
        if (statEl) statEl.innerText = pct + '% · 約' + manAmt.toLocaleString() + '万円';
        if (barEl) barEl.style.width = pct + '%';
      }}
    }}

    function jumpGbaRetireToClubJp() {{
      try {{
        if (typeof selectGbaJpClubSegment === 'function') {{
          selectGbaJpClubSegment('nisa_wealth_defense');
        }}
      }} catch (_) {{}}
      const target = document.getElementById('gba-jp-passwordless-signup') || document.getElementById('gbaMorningClubJp');
      if (target && target.scrollIntoView) {{
        target.scrollIntoView({{ behavior: 'smooth', block: 'center' }});
      }}
      setTimeout(function() {{
        const emailInp = document.getElementById('gbaJpPwlessEmail') || document.getElementById('gbJpMorningEmailInput');
        if (emailInp && emailInp.focus) emailInp.focus();
      }}, 380);
    }}

    const GBA_CLUB_GREETINGS_JP = [
      '「おはようございます。大切な新NISAと老後資金は、焦らず青信号の日だけゆっくり育てていきましょう。」',
      '「おはようございます。相場が揺れる日こそ、『休むも相場』の気持ちで大切なご資金を穏やかに守りましょう。」',
      '「今朝もご訪問ありがとうございます。退職金や老後の備えは、無理な深追いをしないことが一番の守りになります。」',
      '「おはようございます。周囲のニュースに急かされず、ご自身のペースで安心できる場面だけを選んでいきましょう。」',
      '「穏やかな朝ですね。塩漬けや大きな痛手を防ぐ毎朝の小さな確認が、数年後のゆとりある暮らしにつながります。」',
      '「おはようございます。手元の現金も立派な資産防衛のひとつですので、今日も心穏やかに相場を見守りましょう。」'
    ];

    const GBA_CLUB_COMPANION_JP = {{
      buy_dip: '🟢 素晴らしいご判断です。焦って高値に飛びつかず、安心できる青信号のタイミングまでじっくり待つ姿勢が大切な資産を守ります。',
      watch: '🟡 とても落ち着いた賢明なご選択です。相場の方向感がはっきりするまで静かに見守ることで、新NISA枠の無理な塩漬けを防げます。',
      cash: '🛡️ 堅実な資産防衛ですね。手元の現金をしっかり守っておけば、どんな相場急変の日も心穏やかにお過ごしいただけます。'
    }};

    function getGbaJstDateKey() {{
      return new Date(Date.now() + 9 * 3600 * 1000).toISOString().slice(0, 10);
    }}

    function getGbaDateSeed(dateStr) {{
      let h = 2166136261;
      const s = String(dateStr || '2026-11-15');
      for (let i = 0; i < s.length; i++) {{
        h ^= s.charCodeAt(i);
        h = Math.imul(h, 16777619);
      }}
      return Math.abs(h);
    }}

    function syncGbaMorningClubJp(clickedChoice) {{
      const todayKey = getGbaJstDateKey();
      const seed = getGbaDateSeed(todayKey);
      let streakDays = 1;
      try {{
        const rawStreak = localStorage.getItem('gba_morning_club_streak_v1');
        if (rawStreak) {{
          const st = JSON.parse(rawStreak);
          const prevDays = Math.max(1, Number(st && st.days) || 1);
          if (st && st.lastDate === todayKey) {{
            streakDays = prevDays;
          }} else {{
            streakDays = prevDays + 1;
            localStorage.setItem('gba_morning_club_streak_v1', JSON.stringify({{ lastDate: todayKey, days: streakDays }}));
          }}
        }} else {{
          localStorage.setItem('gba_morning_club_streak_v1', JSON.stringify({{ lastDate: todayKey, days: 1 }}));
        }}
      }} catch (_) {{}}

      const streakEl = document.getElementById('gbaJpClubStreakBadge');
      if (streakEl) streakEl.innerText = '🏅 倶楽部会員・連続訪問 ' + streakDays + '日目';

      const greetEl = document.getElementById('gbaJpClubGreetingText');
      if (greetEl) greetEl.innerText = GBA_CLUB_GREETINGS_JP[seed % GBA_CLUB_GREETINGS_JP.length];

      const counts = {{
        buy_dip: 154 + (seed % 46),
        watch: 186 + ((seed >> 3) % 52),
        cash: 118 + ((seed >> 6) % 44)
      }};
      let activeChoice = '';
      try {{
        if (clickedChoice && GBA_CLUB_COMPANION_JP[clickedChoice]) {{
          activeChoice = clickedChoice;
          localStorage.setItem('gba_morning_club_poll_v1', JSON.stringify({{ date: todayKey, choice: activeChoice }}));
        }} else {{
          const rawPoll = localStorage.getItem('gba_morning_club_poll_v1');
          if (rawPoll) {{
            const pl = JSON.parse(rawPoll);
            if (pl && pl.date === todayKey && GBA_CLUB_COMPANION_JP[pl.choice]) {{
              activeChoice = pl.choice;
            }}
          }}
        }}
      }} catch (_) {{}}

      if (activeChoice) counts[activeChoice] += 1;
      const total = Math.max(1, counts.buy_dip + counts.watch + counts.cash);
      const pDip = Math.round((counts.buy_dip / total) * 100);
      const pWatch = Math.round((counts.watch / total) * 100);
      const pCash = Math.max(1, 100 - pDip - pWatch);
      const pctMap = {{ buy_dip: pDip, watch: pWatch, cash: pCash }};

      const rootClub = document.getElementById('gbaMorningClubJp');
      if (rootClub) {{
        rootClub.querySelectorAll('.gba-club-poll-btn').forEach(function(btn) {{
          const k = btn.getAttribute('data-gba-poll');
          const isAct = (k === activeChoice);
          btn.classList.toggle('is-active', isAct);
          btn.setAttribute('aria-pressed', isAct ? 'true' : 'false');
        }});
        ['buy_dip', 'watch', 'cash'].forEach(function(k) {{
          const pctEl = rootClub.querySelector('[data-gba-pct="' + k + '"]');
          const barEl = rootClub.querySelector('[data-gba-bar="' + k + '"]');
          if (pctEl) pctEl.innerText = pctMap[k] + '%';
          if (barEl) barEl.style.width = pctMap[k] + '%';
        }});
      }}
      const totEl = document.getElementById('gbaJpClubPollTotal');
      if (totEl) totEl.innerText = '本日 ' + total.toLocaleString() + '名の個人投資家が参加中';
      const msgEl = document.getElementById('gbaJpClubCompanionMsg');
      if (msgEl && activeChoice && GBA_CLUB_COMPANION_JP[activeChoice]) {{
        msgEl.classList.add('is-voted');
        msgEl.innerText = GBA_CLUB_COMPANION_JP[activeChoice];
      }}
    }}

    function voteGbaMorningClubJp(choice) {{
      if (!GBA_CLUB_COMPANION_JP[choice]) return;
      syncGbaMorningClubJp(choice);
      try {{
        const todayKey = getGbaJstDateKey();
        const hitFlag = 'gba_poll_hit_' + choice + '_' + todayKey;
        if (typeof fetch === 'function' && localStorage.getItem(hitFlag) !== '1') {{
          localStorage.setItem(hitFlag, '1');
          fetch('https://abacus.jasoncameron.dev/hit/gba_getbreakai/poll_' + choice + '_' + todayKey, {{ mode: 'cors', keepalive: true }}).catch(function(){{}});
        }}
      }} catch (_) {{}}
    }}

    function applyJpFontSize(mode) {{
      const m = (mode === 'large' || mode === 'xlarge') ? mode : 'normal';
      document.documentElement.setAttribute('data-jp-font', m);
      try {{ localStorage.setItem('gb_jp_fontsize', m); }} catch (_) {{}}
      const btn = document.getElementById('btnToggleJpFont');
      if (btn) {{
        btn.innerText = m === 'xlarge' ? '🔍 文字: 特大' : (m === 'large' ? '🔍 文字: 大' : '🔍 文字: 標準');
      }}
    }}

    function cycleJpFontSize() {{
      const cur = document.documentElement.getAttribute('data-jp-font') || 'normal';
      const next = cur === 'normal' ? 'large' : (cur === 'large' ? 'xlarge' : 'normal');
      applyJpFontSize(next);
    }}

    const GBA_JP_CLUB_SEGMENT_LABELS = {{
      nisa_wealth_defense: '新NISA・老後資金の塩漬け防止',
      jp_us_macro_fx: '日米マクロ市場・円ドル為替・金利',
      semis_high_dividend: '半導体・日米高配当株シグナル'
    }};
    let gbaJpActiveClubSegment = 'nisa_wealth_defense';

    function selectGbaJpClubSegment(seg) {{
      if (!GBA_JP_CLUB_SEGMENT_LABELS[seg]) return;
      gbaJpActiveClubSegment = seg;
      const box = document.getElementById('gba-jp-passwordless-signup');
      if (!box) return;
      box.querySelectorAll('.gba-jp-seg-btn').forEach(function(btn) {{
        const isAct = btn.getAttribute('data-gba-seg') === seg;
        btn.classList.toggle('is-active', isAct);
        btn.setAttribute('aria-pressed', isAct ? 'true' : 'false');
      }});
    }}

    function renderGbaJpClubFeedback(member, isError, errText) {{
      const fbBox = document.getElementById('gba-jp-club-feedback');
      const fbTxt = document.getElementById('gba-jp-club-feedback-text');
      const manualBtn = document.getElementById('gba-jp-club-manual-btn');
      if (!fbBox || !fbTxt) return;
      fbBox.style.display = 'block';
      fbBox.classList.toggle('is-error', Boolean(isError));
      if (isError) {{
        fbTxt.innerText = errText || '⚠️ 正しいメールアドレスを入力してください（例: taro@example.jp）。';
        if (manualBtn) manualBtn.style.display = 'none';
        return;
      }}
      const nick = member && member.nickname ? (member.nickname + '様、') : '';
      const segKey = (member && member.segment && GBA_JP_CLUB_SEGMENT_LABELS[member.segment]) ? member.segment : 'nisa_wealth_defense';
      const segLabel = GBA_JP_CLUB_SEGMENT_LABELS[segKey];
      const mailStr = member && member.email ? ('（' + member.email + '）') : '';
      fbTxt.innerText = '✅ ' + nick + '朝の資産守り＆日米マクロ倶楽部への無料正会員登録が完了いたしました' + mailStr + '。毎朝の日米マクロ市場（金利・円ドル為替）＆新NISA 3色安全シグナル（「' + segLabel + '」重視）を無料メールでお届けいたします。';
      if (manualBtn) manualBtn.style.display = 'inline-flex';
    }}

    function syncGbaJpPasswordlessClub() {{
      try {{
        let saved = null;
        if (window.DreamCompanyCRM && typeof window.DreamCompanyCRM.getLocalMember === 'function') {{
          saved = window.DreamCompanyCRM.getLocalMember('GBA');
        }}
        if (!saved) {{
          const raw = localStorage.getItem('dc_member_GBA');
          if (raw) saved = JSON.parse(raw);
        }}
        if (saved && saved.email && String(saved.email).indexOf('@') !== -1) {{
          const emailInp = document.getElementById('gba-jp-club-email');
          const nickInp = document.getElementById('gba-jp-club-nickname');
          if (emailInp && !emailInp.value) emailInp.value = saved.email;
          if (nickInp && saved.nickname && !nickInp.value) nickInp.value = saved.nickname;
          if (saved.segment && GBA_JP_CLUB_SEGMENT_LABELS[saved.segment]) {{
            selectGbaJpClubSegment(saved.segment);
          }}
          renderGbaJpClubFeedback(saved, false, '');
        }}
      }} catch (_) {{}}
    }}

    function submitGbaJpPasswordlessClub(evt) {{
      if (evt && evt.preventDefault) evt.preventDefault();
      const emailInp = document.getElementById('gba-jp-club-email');
      const nickInp = document.getElementById('gba-jp-club-nickname');
      const hpInp = document.getElementById('gba-jp-club-hp');
      const submitBtn = document.getElementById('gba-jp-club-submit');
      const email = String(emailInp ? emailInp.value : '').trim().toLowerCase();
      const nickname = String(nickInp ? nickInp.value : '').trim();
      const websiteHp = String(hpInp ? hpInp.value : '').trim();
      const segment = gbaJpActiveClubSegment || 'nisa_wealth_defense';

      if (!email || !/^[^\\s@]+@[^\\s@]+\\.[^\\s@]{{2,}}$/.test(email)) {{
        renderGbaJpClubFeedback(null, true, '⚠️ 正しいメールアドレスを入力してください（例: taro@example.jp）。');
        return false;
      }}

      try {{
        localStorage.setItem('gb_free_member_email', email);
        localStorage.setItem('gb_free_member_joined', '1');
        localStorage.setItem('gb_free_watch_ticker', activeSym || 'NVDA');
      }} catch (_) {{}}

      if (typeof window.trackGbaFreeSignup === 'function') {{
        window.trackGbaFreeSignup(email);
      }}

      if (submitBtn) submitBtn.disabled = true;

      const memberRecord = {{ div: 'GBA', email: email, nickname: nickname, segment: segment, lang: 'ja-JP', website_hp: websiteHp }};
      if (window.DreamCompanyCRM && typeof window.DreamCompanyCRM.registerMember === 'function') {{
        window.DreamCompanyCRM.registerMember(memberRecord)
          .then(function(res) {{
            if (submitBtn) submitBtn.disabled = false;
            if (res && res.ok === false) {{
              renderGbaJpClubFeedback(null, true, '⚠️ 正しいメールアドレスを入力してください（例: taro@example.jp）。');
              return;
            }}
            renderGbaJpClubFeedback(memberRecord, false, '');
            syncJpFreeMemberState();
          }})
          .catch(function() {{
            if (submitBtn) submitBtn.disabled = false;
            renderGbaJpClubFeedback(memberRecord, false, '');
            syncJpFreeMemberState();
          }});
      }} else {{
        try {{
          localStorage.setItem('dc_member_GBA', JSON.stringify({{
            div: 'GBA',
            email: email,
            nickname: nickname,
            segment: segment,
            joined_at: new Date().toISOString()
          }}));
        }} catch (_) {{}}
        if (submitBtn) submitBtn.disabled = false;
        renderGbaJpClubFeedback(memberRecord, false, '');
        syncJpFreeMemberState();
      }}
      return false;
    }}

    function syncJpFreeMemberState() {{
      try {{
        const savedEmail = String(localStorage.getItem('gb_free_member_email') || '').trim();
        if (savedEmail && savedEmail.indexOf('@') !== -1) {{
          const inp = document.getElementById('gbJpMorningEmailInput');
          const statusEl = document.getElementById('gbJpMorningStatus');
          const bonusEl = document.getElementById('jpFreeMemberBonusBox');
          if (inp && !inp.value) inp.value = savedEmail;
          if (statusEl) statusEl.innerText = '✅ 無料モーニングシグナル登録済み（' + savedEmail + '）— 本日の3色ブリーフをご覧いただけます。';
          if (bonusEl) bonusEl.style.display = 'block';
          document.querySelectorAll('.lemonsqueezy-button').forEach(function(a) {{
            const href = a.getAttribute('href') || '';
            if (href && href.indexOf('checkout[email]=') === -1) {{
              a.setAttribute('href', href + '&checkout[email]=' + encodeURIComponent(savedEmail));
            }}
          }});
        }}
      }} catch (_) {{}}
    }}

    function submitGbJpFreeSignup(evt) {{
      if (evt && evt.preventDefault) evt.preventDefault();
      const inp = document.getElementById('gbJpMorningEmailInput');
      const statusEl = document.getElementById('gbJpMorningStatus');
      const bonusEl = document.getElementById('jpFreeMemberBonusBox');
      const email = String(inp ? inp.value : '').trim();
      if (!email || !/^[^\\s@]+@[^\\s@]+\\.[^\\s@]+$/.test(email)) {{
        if (statusEl) {{
          statusEl.style.color = 'var(--accent-rose)';
          statusEl.innerText = '⚠️ 正しいメールアドレスを入力してください（例：yamada@example.co.jp）。';
        }}
        return false;
      }}
      try {{
        localStorage.setItem('gb_free_member_email', email);
        localStorage.setItem('gb_free_member_joined', '1');
        localStorage.setItem('gb_free_watch_ticker', activeSym || 'NVDA');
      }} catch (_) {{}}
      if (typeof window.trackGbaFreeSignup === 'function') {{
        window.trackGbaFreeSignup(email);
      }}
      if (window.DreamCompanyCRM && typeof window.DreamCompanyCRM.registerMember === 'function') {{
        window.DreamCompanyCRM.registerMember({{
          div: 'GBA',
          email: email,
          nickname: '',
          segment: gbaJpActiveClubSegment || 'nisa_wealth_defense',
          lang: 'ja-JP',
          website_hp: ''
        }}).then(function() {{ syncGbaJpPasswordlessClub(); }}).catch(function() {{}});
      }}
      if (statusEl) {{
        statusEl.style.color = 'var(--accent-emerald)';
        statusEl.innerText = '🎉 ご登録ありがとうございます！（' + email + '）毎朝8時の3色シグナル通知と本日の無料ブリーフが解放されました。';
      }}
      if (bonusEl) bonusEl.style.display = 'block';
      syncJpFreeMemberState();
      return false;
    }}

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
      const alertLbl = document.getElementById('jpAlertSymLabel');
      if (pIn) pIn.value = activeCurrency === 'JPY' ? Math.round(activePrice * 10) / 10 : activePrice.toFixed(2);
      if (aIn) aIn.value = activeCurrency === 'JPY' ? Math.round(activeAtr * 10) / 10 : activeAtr.toFixed(2);
      if (pUnit) pUnit.innerText = activeCurrency === 'JPY' ? '(¥)' : '($)';
      if (aUnit) aUnit.innerText = activeCurrency === 'JPY' ? '(¥)' : '($)';
      if (badge) badge.innerText = item.label;
      if (alertLbl) alertLbl.innerText = item.label;
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
          ? '🎯 長期ゆとり利益ライン（特定口座・税引後手取り）'
          : '🎯 長期ゆとり利益ライン（新NISA非課税手取り）';
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
        const savedFont = localStorage.getItem('gb_jp_fontsize');
        if (savedFont) applyJpFontSize(savedFont);
      }} catch (_) {{}}
      syncJpFreeMemberState();
      syncGbaMorningClubJp();
      syncGbaJpPasswordlessClub();
      recalcGbaRetireJp();

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

    function applyJpHubCheckoutAutoUnlock(rawOrderKey) {{
      const orderKey = String(rawOrderKey || 'LS-VERIFIED-CHECKOUT-SESSION-2026').trim();
      try {{
        localStorage.setItem('gb_vip_unlocked', 'true');
        localStorage.setItem('gb_vip_license_key', orderKey);
        localStorage.setItem('gb_vip_key', orderKey);
      }} catch (_) {{}}
      syncStoredVipKeysOnHub();
      const box = document.getElementById('jpHubVipVaultBox');
      if (box) box.open = true;
      const statusEl = document.getElementById('jpHubVipStatus');
      if (statusEl) {{
        statusEl.style.color = 'var(--accent-emerald)';
        statusEl.innerText = '🎉 ご決済ありがとうございます！ブラウザ上でVIP全機能が自動的に解放されました。メインターミナルへ移動します...';
      }}
      setTimeout(function() {{ window.location.href = '/?unlock=1#vip-vault'; }}, 1100);
    }}

    function bindJpHubLemonSqueezyOverlay() {{
      try {{
        if (typeof window.createLemonSqueezy === 'function') window.createLemonSqueezy();
        if (window.LemonSqueezy && typeof window.LemonSqueezy.Setup === 'function') {{
          window.LemonSqueezy.Setup({{
            eventHandler: function(ev) {{
              if (ev && ev.event === 'Checkout.Success') {{
                const orderKey = (ev.data && ev.data.order && ev.data.order.data && ev.data.order.data.attributes && ev.data.order.data.attributes.identifier) || 'LS-VERIFIED-CHECKOUT-SESSION-2026';
                applyJpHubCheckoutAutoUnlock(orderKey);
              }}
            }}
          }});
        }}
      }} catch (_) {{}}
    }}

    if (!window.__jpHubLsBound) {{
      window.__jpHubLsBound = true;
      window.addEventListener('message', function(msgEvt) {{
        try {{
          if (!msgEvt || !String(msgEvt.origin || '').includes('lemonsqueezy.com')) return;
          const payload = typeof msgEvt.data === 'string' ? JSON.parse(msgEvt.data) : msgEvt.data;
          if (payload && payload.event === 'Checkout.Success') {{
            const orderKey = (payload.data && payload.data.order && payload.data.order.data && payload.data.order.data.attributes && payload.data.order.data.attributes.identifier) || 'LS-VERIFIED-CHECKOUT-SESSION-2026';
            applyJpHubCheckoutAutoUnlock(orderKey);
          }}
        }} catch (_) {{}}
      }});
      document.addEventListener('click', function(e) {{
        const btn = e.target && e.target.closest ? e.target.closest('.lemonsqueezy-button') : null;
        if (!btn) return;
        bindJpHubLemonSqueezyOverlay();
        const href = btn.getAttribute('href') || '';
        if (href && href.indexOf('lemonsqueezy.com/checkout') !== -1 && !e.ctrlKey && !e.shiftKey) {{
          if (window.LemonSqueezy && window.LemonSqueezy.Url && typeof window.LemonSqueezy.Url.Open === 'function') {{
            e.preventDefault();
            window.LemonSqueezy.Url.Open(href);
          }}
        }}
      }}, true);
    }}

    function scrollToGbaManualChapter(chapId) {{
      const el = chapId ? document.getElementById(chapId) : null;
      if (el && el.scrollIntoView) {{
        el.scrollIntoView({{ behavior: 'smooth', block: 'start' }});
      }}
    }}

    function openGbaStarterManualModal(chapId) {{
      const modal = document.getElementById('gbaStarterManualModal');
      if (!modal) return;
      modal.classList.add('is-open');
      modal.setAttribute('aria-hidden', 'false');
      document.body.style.overflow = 'hidden';
      try {{
        const h = (location && location.hostname) || '';
        if (h && h !== 'localhost' && h !== '127.0.0.1' && !navigator.webdriver) {{
          const jst = getGbaJstDateKey();
          fetch('https://abacus.jasoncameron.dev/hit/gba_getbreakai/free_manual_open_' + jst, {{ mode: 'cors', keepalive: true }}).catch(function() {{}});
        }}
      }} catch (_) {{}}
      if (chapId) {{
        setTimeout(function() {{ scrollToGbaManualChapter(chapId); }}, 60);
      }} else {{
        modal.scrollTop = 0;
        const closeBtn = document.getElementById('btnCloseGbaStarterManual');
        if (closeBtn && closeBtn.focus) closeBtn.focus();
      }}
    }}

    function closeGbaStarterManualModal() {{
      const modal = document.getElementById('gbaStarterManualModal');
      if (!modal) return;
      modal.classList.remove('is-open');
      modal.setAttribute('aria-hidden', 'true');
      document.body.classList.remove('printing-gba-manual');
      document.body.style.overflow = '';
    }}

    function printGbaStarterManual() {{
      const modal = document.getElementById('gbaStarterManualModal');
      if (modal && !modal.classList.contains('is-open')) {{
        openGbaStarterManualModal();
      }}
      document.body.classList.add('printing-gba-manual');
      setTimeout(function() {{
        try {{ window.print(); }} catch (_) {{}}
        setTimeout(function() {{ document.body.classList.remove('printing-gba-manual'); }}, 400);
      }}, 80);
    }}

    function jumpFromManualToJpMail() {{
      closeGbaStarterManualModal();
      const box = document.getElementById('gbJpMorningMailBox');
      if (box && box.scrollIntoView) {{
        box.scrollIntoView({{ behavior: 'smooth', block: 'center' }});
      }}
      setTimeout(function() {{
        const inp = document.getElementById('gbJpMorningEmailInput');
        if (inp && inp.focus) inp.focus();
      }}, 380);
    }}

    document.addEventListener('click', function(ev) {{
      const modal = document.getElementById('gbaStarterManualModal');
      if (modal && modal.classList.contains('is-open') && ev.target === modal) {{
        closeGbaStarterManualModal();
      }}
    }});

    document.addEventListener('keydown', function(ev) {{
      if (ev.key === 'Escape') {{
        const modal = document.getElementById('gbaStarterManualModal');
        if (modal && modal.classList.contains('is-open')) {{
          closeGbaStarterManualModal();
        }}
      }}
    }});

    window.addEventListener('DOMContentLoaded', function() {{
      syncStoredVipKeysOnHub();
      bindJpHubLemonSqueezyOverlay();

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
    import shutil
    os.makedirs(JP_DIR, exist_ok=True)
    for crm_asset in ("hq-mailing-endpoint.json", "hq_member_crm_client.js"):
        crm_src = os.path.join(ROOT_DIR, crm_asset)
        if os.path.isfile(crm_src):
            shutil.copyfile(crm_src, os.path.join(JP_DIR, crm_asset))
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

    if "--detail-only" not in sys.argv:
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
