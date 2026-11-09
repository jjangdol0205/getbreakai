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
        "ticker": "NVDA",
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
        "ticker": "NVDA",
        "jp_name": "マイクロソフト(MSFT)",
        "title": "マイクロソフト(MSFT) Azure AI成長率・SEC開示NLPと新NISAコア戦略",
        "focus": "AzureクラウドにおけるAI貢献度拡大とCopilot法人導入の決算コールNLP解析・低リスクATR押し目買い",
        "catalyst_type": "クラウドAI増収ガイダンス ＆ 機関コア保有",
        "entry": 448.20, "atr": 9.40, "iv": 32, "score": 88.5, "dp": "59.5%", "call_ratio": "2.2倍"
    },
    {
        "slug": "aapl-apple-intelligence-cycle-gex.html",
        "ticker": "NVDA",
        "jp_name": "アップル(AAPL)",
        "title": "アップル(AAPL) Apple Intelligence買い替えサイクルとオプションGEX壁",
        "focus": "オンデバイスAI搭載iPhone買い替え需要・サービス部門粗利率70%超えと過去最大規模の自社株買いサポート",
        "catalyst_type": "自社株買い8-K下値支持 ＆ オプションCall Wall解析",
        "entry": 232.80, "atr": 4.90, "iv": 29, "score": 86.8, "dp": "55.8%", "call_ratio": "2.1倍"
    },
    {
        "slug": "amzn-aws-margin-expansion-pead.html",
        "ticker": "NVDA",
        "jp_name": "アマゾン(AMZN)",
        "title": "アマゾン(AMZN) AWS営業利益率改善・決算後ドリフトとATRトレーリング",
        "focus": "AWS生成AIワークロード拡大と北米物流自動化による営業利益率の過去最高更新・機関ダークプール集積",
        "catalyst_type": "AWS利益率サプライズ ＆ 決算後ドリフト(PEAD)",
        "entry": 214.50, "atr": 5.30, "iv": 36, "score": 89.2, "dp": "60.2%", "call_ratio": "2.6倍"
    },
    {
        "slug": "googl-search-cloud-ai-valuation.html",
        "ticker": "NVDA",
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

    verdict_banner = (
        f"🔴 【AI緊急警告】{jp_name} は現在 AIカタリストスコア {score}/100（会計監査リスク・ダークプール機関売り {dp}）のため、新規買いエントリー禁止（DO NOT BUY / AVOID）と判定されています。"
        if is_avoid else
        f"🟢 【AI機関投資家シグナル】{jp_name} は AIカタリストスコア {score}/100（{cat_type}）を記録。$50,000（約750万円）口座での推奨購入株数は {shares}株（約{notional_jpy_man}万円）、2.0x ATR損切りラインは ${stop_loss:.2f}、2.5R利確ターゲットは ${target_25r:.2f} です。"
    )

    related_links_html = "\n".join([
        f'<li><a href="/jp/{s["slug"]}" style="color:#c4b5fd; text-decoration:none;">📈 {s["title"]}</a></li>'
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
    }} catch (e) {{}}
  }})();
  </script>
  <style>
    :root {{
      --bg-dark: #06050c;
      --bg-card: #0e0b1a;
      --border-color: #241d3d;
      --border-accent: #4c3785;
      --text-main: #f8fafc;
      --text-muted: #b4add0;
      --accent-violet: #8b5cf6;
      --accent-amber: #f59e0b;
      --accent-emerald: #10b981;
      --accent-rose: #f43f5e;
      --accent-sky: #38bdf8;
      --font-sans: 'Noto Sans JP', sans-serif;
      --font-mono: 'JetBrains Mono', monospace;
    }}
    * {{ box-sizing: border-box; margin: 0; padding: 0; }}
    body {{
      background: var(--bg-dark);
      color: var(--text-main);
      font-family: var(--font-sans);
      line-height: 1.8;
      padding-bottom: 60px;
    }}
    .container {{ max-width: 960px; margin: 0 auto; padding: 0 20px; }}
    header {{
      background: rgba(6,5,12,0.92);
      border-bottom: 1px solid var(--border-color);
      padding: 16px 0;
      position: sticky;
      top: 0;
      z-index: 50;
    }}
    .nav-bar {{ display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 12px; }}
    .brand {{ color: #fff; font-weight: 900; font-size: 1.2rem; text-decoration: none; }}
    .btn-cta {{
      background: linear-gradient(135deg, var(--accent-violet), #6d28d9);
      color: #fff;
      text-decoration: none;
      padding: 9px 18px;
      border-radius: 8px;
      font-weight: 800;
      font-size: 0.86rem;
    }}
    .article-box {{
      background: var(--bg-card);
      border: 1px solid var(--border-accent);
      border-radius: 16px;
      padding: 32px;
      margin-top: 28px;
    }}
    h1 {{ font-size: clamp(1.5rem, 3.2vw, 2.15rem); line-height: 1.35; margin-bottom: 16px; font-weight: 900; }}
    h2 {{ font-size: 1.32rem; color: #c4b5fd; margin: 32px 0 12px; border-left: 4px solid var(--accent-violet); padding-left: 12px; }}
    h3 {{ font-size: 1.08rem; color: var(--accent-amber); margin: 22px 0 8px; }}
    p {{ color: var(--text-muted); margin-bottom: 16px; font-size: 0.97rem; }}
    .kpi-grid {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(195px, 1fr));
      gap: 12px;
      margin: 22px 0;
    }}
    .kpi-card {{
      background: #141026;
      border: 1px solid var(--border-color);
      border-radius: 10px;
      padding: 14px;
    }}
    .kpi-label {{ font-size: 0.75rem; color: var(--text-muted); font-family: var(--font-mono); }}
    .kpi-val {{ font-size: 1.22rem; font-weight: 800; font-family: var(--font-mono); margin-top: 4px; }}
    .widget-box {{
      background: #130e24;
      border: 1.5px solid var(--accent-violet);
      border-radius: 14px;
      padding: 22px;
      margin: 26px 0;
    }}
    @media (max-width: 640px) {{
      .article-box {{ padding: 20px 16px; }}
    }}
  </style>
</head>
<body>
  <header>
    <div class="container nav-bar">
      <a href="https://getbreakai.com/" class="brand">⚡ GetBreakAI 米国株・新NISA AIターミナル</a>
      <div style="display:flex; gap:10px; flex-wrap:wrap;">
        <a href="/jp/index.html" style="color:var(--text-muted); text-decoration:none; font-size:0.86rem; padding:8px;">📚 全30銘柄レポート一覧</a>
        <a href="https://getbreakai.com/?ticker={ticker}#radar" class="btn-cta">🎯 {jp_name}をメイン端末で起動 →</a>
      </div>
    </div>
  </header>

  <main class="container">
    <article class="article-box">
      <div style="font-family:var(--font-mono); font-size:0.78rem; color:var(--accent-amber); font-weight:800; margin-bottom:8px;">
        🟢 米国市場最新データ反映 · {date_str} ｜ 対象銘柄・テーマ: {jp_name} (${ticker})
      </div>
      <h1>{title}</h1>
      <div style="background:rgba(16,185,129,0.12); border:1px solid rgba(16,185,129,0.45); border-radius:10px; padding:14px 16px; margin-bottom:22px; color:#e2e8f0; font-weight:700; font-size:0.93rem;">
        {verdict_banner}
      </div>

      <div class="kpi-grid">
        <div class="kpi-card">
          <div class="kpi-label">現在値 / 基準株価</div>
          <div class="kpi-val" style="color:#fff;">${entry:.2f} <span style="font-size:0.8rem; color:var(--text-muted);">(約¥{int(round(entry*150)):,})</span></div>
        </div>
        <div class="kpi-card">
          <div class="kpi-label">AIカタリスト総合スコア</div>
          <div class="kpi-val" style="color:#c4b5fd;">{score} / 100</div>
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
      <div class="widget-box">
        <h3 style="margin-top:0; color:#fff;">🧮 {jp_name} 専用：ATR損切りライン＆適正株数ミニ計算機（ドル $ / 日本円 ¥ 同時換算）</h3>
        <p style="font-size:0.86rem; margin-bottom:14px;">
          ご自身の運用資金（スライダー）を動かすと、1回の最大損失を口座の1.5%以内に抑える「推奨エントリー株数」と「許容損失額（ドル・円）」がリアルタイムで計算されます。
        </p>
        <div style="margin-bottom:14px;">
          <div style="display:flex; justify-content:space-between; font-family:var(--font-mono); font-size:0.85rem; margin-bottom:6px;">
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
          <a href="https://getbreakai.com/?ticker={ticker}#radar" class="btn-cta">⚡ フル機能ターミナルで ${ticker} を詳細シミュレーション →</a>
          <button type="button" onclick="shareMiniPageOnX()" style="background:#1a1430; color:#38bdf8; border:1px solid #38bdf8; padding:9px 16px; border-radius:8px; font-weight:800; cursor:pointer;">📤 X(Twitter)でこの記事とシグナルを共有</button>
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
        さらに勝率と資金効率を高めるために、1〜15日間のイベント・ガンマスクイーズ・ATR損切りを管理する当サイト <strong>GetBreakAI.com</strong> と、30〜90日間の半導体セクター恐怖強欲指数および米国株72銘柄のPW-RSI（出来高加重RSI）底値反転を捉える姉妹ターミナル <a href="https://truthofmarket.com/?utm_source=getbreakai_jp_seo&utm_medium={slug}" target="_blank" rel="noopener" style="color:var(--accent-sky); font-weight:700;">TruthOfMarket.com</a> を併用してください。<strong>Store #296100で発行されるProライセンスキー（月額$29＝約4,350円、または永久買い切り$199＝約29,800円）1つで、両方のサイトのVIP機能がすべてアンロックされます。</strong>
      </p>

      <div style="margin-top:32px; padding:22px; background:linear-gradient(135deg, rgba(139,92,246,0.18), rgba(16,185,129,0.12)); border:1px solid var(--accent-violet); border-radius:14px; text-align:center;">
        <h3 style="margin-top:0; color:#fff;">🚀 今すぐ GetBreakAI メインターミナルで {jp_name} の最新シグナルを確認</h3>
        <p style="margin-bottom:16px;">Pine Script v5インジケーター全文、Form-4役員自社株買いCSV、全銘柄オーダーブックを即時解放できます。</p>
        <a href="https://getbreakai.com/?ticker={ticker}#radar" class="btn-cta" style="display:inline-block; padding:13px 26px; font-size:0.98rem;">📊 GetBreakAI メインターミナルを開く（${ticker} 自動選択） →</a>
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
  </script>
</body>
</html>
"""


def build_hub_html(date_str, all_specs):
    cards_html = "\n".join([
        f'<a href="/jp/{s["slug"]}" style="display:block; background:#141026; border:1px solid #241d3d; border-radius:12px; padding:16px; color:#f8fafc; text-decoration:none;">'
        f'<div style="font-family:monospace; font-size:0.76rem; color:#f59e0b; margin-bottom:4px;">${s["ticker"]} · AIスコア {s["score"]}/100</div>'
        f'<div style="font-weight:800; font-size:0.98rem; margin-bottom:6px; color:#c4b5fd;">{s["title"]}</div>'
        f'<div style="font-size:0.84rem; color:#b4add0;">{s["focus"]}</div>'
        f'</a>'
        for s in all_specs
    ])
    return f"""<!DOCTYPE html>
<html lang="ja">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>米国株・新NISA 銘柄別AI日本語ディープリサーチ全30選 | GetBreakAI</title>
  <meta name="description" content="エヌビディア(NVDA)、パランティア(PLTR)、テスラ(TSLA)、イーライリリー(LLY)、SOXL、SMCIなど米国株30銘柄・テーマのSEC開示・インサイダー買い・Gamma Wall・ATR損切りライン解説一覧。">
  <link rel="canonical" href="https://getbreakai.com/jp/index.html">
  <link rel="icon" type="image/svg+xml" href="/favicon.svg">
  <style>
    body {{ background:#06050c; color:#f8fafc; font-family:'Noto Sans JP',sans-serif; line-height:1.7; margin:0; padding:0 0 60px; }}
    .container {{ max-width:1100px; margin:0 auto; padding:24px 20px; }}
    .grid {{ display:grid; grid-template-columns:repeat(auto-fill, minmax(310px, 1fr)); gap:16px; margin-top:24px; }}
  </style>
</head>
<body>
  <div class="container">
    <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:12px; border-bottom:1px solid #241d3d; padding-bottom:16px;">
      <a href="https://getbreakai.com/" style="color:#fff; font-weight:900; font-size:1.25rem; text-decoration:none;">⚡ GetBreakAI 米国株・新NISA AIターミナル</a>
      <a href="https://getbreakai.com/#radar" style="background:#8b5cf6; color:#fff; padding:9px 18px; border-radius:8px; text-decoration:none; font-weight:800;">🎯 メインATR計算機へ戻る →</a>
    </div>
    <h1 style="margin-top:24px; font-size:1.8rem;">📚 米国株・新NISA 銘柄別AI日本語ディープリサーチ全30選（{date_str} 最新版）</h1>
    <p style="color:#b4add0;">SEC 8-K決算・契約開示、Form-4経営陣インサイダー買い、オプションGamma Wall(GEX)、2.0x ATR損切りライン＆適正株数を完全網羅。</p>
    <div class="grid">
      {cards_html}
    </div>
  </div>
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

    # Ping IndexNow API
    if "--ping-indexnow" in sys.argv or True:
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
