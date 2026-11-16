#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
scripts/build_jp_seo_pages.py
Division 3 (GBA — getbreakai.com) Upstream Static Site & 30-Page SEO Builder.
Generates:
  1. Root /index.html & /jp/index.html (Unified Japanese 50-70s Shin-NISA & Tokutei Hybrid Cashflow Edition)
  2. All 30 /jp/*.html Public Market Data & Asset-Allocation Educational Research Pages
  3. Legal Pages (/terms.html, /jp/terms.html, /privacy.html, /jp/privacy.html, /refund.html, /jp/refund.html, /contact.html, /jp/contact.html)
  4. sitemap.xml & IndexNow key file
Strictly Zero-Hangul, Zero-Chat-App, MoR/FIEA & Japanese FSA Shin-NISA Compliant.
"""

import os
import re
import sys
import json
import math
import shutil
from datetime import datetime, timezone, timedelta

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
if SCRIPT_DIR not in sys.path:
    sys.path.insert(0, SCRIPT_DIR)

from gba_mor_nisa_shared import (  # noqa: E402
    LS_MONTHLY_UUID,
    LS_ANNUAL_UUID,
    LS_MONTHLY_URL_HTML,
    LS_ANNUAL_URL_HTML,
    PRICE_LABEL_MONTHLY_JP,
    PRICE_LABEL_ANNUAL_JP,
    MANDATORY_DISCLAIMER_JP,
    SOFTWARE_POSITIONING_JP,
    FSA_HYBRID_PHRASE_JP,
    MAIN_HUB_EXCLUDED_SLUGS,
    build_payment_and_kpi_head_html,
    build_mandatory_disclaimer_html,
    build_starter_manual_modal_html,
    build_vip_waitlist_modal_html,
    build_legal_footer_html,
    build_all_legal_pages,
)

ROOT_DIR = os.path.dirname(SCRIPT_DIR)
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
        "title": "エヌビディア(NVDA) 米SEC公式決算開示（Form 8-K/10-Q）と資産配分・変動幅データ解析",
        "focus": "次世代AIデータセンター需要に関する米SEC公式決算開示（Form 8-K/10-Q）の要約と、大口機関投資家の安定買い越し比率61%および1銘柄集中を防ぐ資産配分シミュレーション",
        "catalyst_type": "米SEC公式決算開示（Form 8-K）＆ 機関投資家の需給改善",
        "entry": 186.64, "atr": 8.02, "iv": 68, "score": 93.5, "dp": "61.4%", "call_ratio": "3.2倍"
    },
    {
        "slug": "pltr-insider-buying-analysis.html",
        "ticker": "PLTR",
        "jp_name": "パランティア(PLTR)",
        "title": "パランティア(PLTR) SEC Form-4公開データ・長期契約開示と適正配分比率の試算",
        "focus": "米国公共・民間向けAI基盤契約の米SEC公式決算開示（Form 8-K/10-Q）と、大口機関投資家の安定買い越し比率64%に基づく長期ポートフォリオ配分目安",
        "catalyst_type": "米SEC公式適時開示（Form 8-K）＆ 機関投資家の長期保有動向",
        "entry": 160.38, "atr": 9.95, "iv": 74, "score": 91.0, "dp": "64.2%", "call_ratio": "2.8倍"
    },
    {
        "slug": "tsla-gamma-wall-swing-trade.html",
        "ticker": "TSLA",
        "jp_name": "テスラ(TSLA)",
        "title": "テスラ(TSLA) 米SEC事業開示データと公開オプション統計による予想変動幅の可視化",
        "focus": "自動運転・エネルギー貯蔵部門の米SEC公式決算開示（Form 8-K/10-Q）と、インプライド・ボラティリティ統計から算出される価格変動レンジの自己学習ガイド",
        "catalyst_type": "事業セグメント決算開示 ＆ ボラティリティ統計レンジ可視化",
        "entry": 358.22, "atr": 17.99, "iv": 82, "score": 89.7, "dp": "58.1%", "call_ratio": "3.6倍"
    },
    {
        "slug": "soxl-smh-semiconductor-timing.html",
        "ticker": "SOXL",
        "terminal_ticker": "NVDA",
        "jp_name": "半導体ETF（SMH・SOXL制度比較）",
        "title": "半導体ETF（SMH・SOXL）の公開変動幅データ比較と金融庁・新NISA対象外（特定口座）ルール解説",
        "focus": "金融庁規定により3倍レバレッジ型ETF（SOXL・TQQQ）および毎月分配型ETF（JEPI・SGOV）が新NISA対象外（特定口座のみ）となる法的区分と、新NISA適格コア資産（1489・VYM・HDV・オルカン・S&P500）との変動率比較",
        "catalyst_type": "金融庁・新NISA対象外（特定口座区分）制度解説 ＆ 変動統計比較",
        "entry": 34.50, "atr": 3.10, "iv": 98, "score": 72.0, "dp": "57.0%", "call_ratio": "1.4倍",
        "is_non_nisa_edu": True
    },
    {
        "slug": "smci-accounting-risk-warning.html",
        "ticker": "SMCI",
        "jp_name": "スーパー・マイクロ(SMCI)",
        "title": "スーパー・マイクロ(SMCI) 米SEC年次報告書（Form 10-K）公開リスク注記と機関需給データの読み方",
        "focus": "米SEC年次報告書（Form 10-K）における監査・内部統制関連の公開注記確認ポイントと、大口機関投資家の売り越し比率67%データの客観的リサーチ解説",
        "catalyst_type": "⚠️ 公開財務開示（Form 10-K）高変動リスク指標の確認ケーススタディ",
        "entry": 28.76, "atr": 2.56, "iv": 96, "score": 28.5, "dp": "67.0%（売り越し比率）", "call_ratio": "0.4倍",
        "is_avoid": True
    },
    {
        "slug": "shin-nisa-us-stock-atr-risk-management.html",
        "ticker": "VYM",
        "terminal_ticker": "VYM",
        "jp_name": "新NISA×特定口座ハイブリッド配分設計",
        "title": "新NISA適格（VYM・HDV・1489・オルカン・S&P500）＋特定口座（SGOV・JEPI）ハイブリッド資産配分ガイド",
        "focus": "年間360万円の非課税枠を大切にする年2〜4回の穏やかな資産配分点検と、金融庁規定に準拠した新NISA口座（四半期配当・長期インデックス）×特定口座（毎月分配型）のハイブリッド設計",
        "catalyst_type": "金融庁ルール準拠 新NISA×特定口座ハイブリッド老後資産設計",
        "entry": 134.50, "atr": 2.10, "iv": 18, "score": 95.5, "dp": "62.0%", "call_ratio": "2.1倍"
    },
    {
        "slug": "lly-form4-insider-cluster-buy.html",
        "ticker": "LLY",
        "jp_name": "イーライリリー(LLY)",
        "title": "イーライリリー(LLY) SEC Form-4経営陣の市場内自社株取得データと医薬品研究開発開示",
        "focus": "経営陣複数名による市場内自社株取得（SEC Form-4公開記録）と、代謝・ヘルスケア分野の米SEC公式決算開示（Form 8-K/10-Q）の読み解き方",
        "catalyst_type": "SEC Form-4 公開自社株取得記録 ＆ ヘルスケア業績開示",
        "entry": 1354.00, "atr": 52.81, "iv": 42, "score": 89.8, "dp": "54.0%", "call_ratio": "2.1倍"
    },
    {
        "slug": "avgo-custom-ai-asic-8k-analysis.html",
        "ticker": "AVGO",
        "jp_name": "ブロードコム(AVGO)",
        "title": "ブロードコム(AVGO) カスタムAI半導体・フリーキャッシュフロー開示と増配実績データ解析",
        "focus": "クラウド大手向けカスタム半導体とソフトウェア統合によるフリーキャッシュフロー成長・連続増配履歴に関する米SEC公開財務データの可視化",
        "catalyst_type": "米SEC公式決算開示（Form 8-K/10-Q）＆ 増配キャッシュフロー分析",
        "entry": 293.69, "atr": 15.14, "iv": 58, "score": 88.4, "dp": "59.0%", "call_ratio": "2.9倍"
    },
    {
        "slug": "amd-mi350-gamma-squeeze-target.html",
        "ticker": "AMD",
        "jp_name": "AMD(アドバンスト・マイクロ・デバイセズ)",
        "title": "AMD データセンター部門の米SEC売上開示と半導体セクター分散配分シミュレーション",
        "focus": "エンタープライズ・クラウド向けAI半導体部門の売上推移データと、ポートフォリオ全体の変動を抑える1銘柄あたり配分比率計算",
        "catalyst_type": "データセンター売上開示（Form 10-Q）＆ 機関投資家の需給改善",
        "entry": 449.04, "atr": 38.02, "iv": 64, "score": 86.2, "dp": "57.2%", "call_ratio": "2.4倍"
    },
    {
        "slug": "meta-ai-capex-earnings-nlp.html",
        "ticker": "META",
        "jp_name": "メタ(META)",
        "title": "メタ(META) 広告収益・株主還元（自社株買い・配当）に関する米SEC公式決算データ解析",
        "focus": "AI推薦基盤による営業利益率推移と株主還元枠（自社株買い・四半期配当）の米SEC公式決算開示（Form 8-K/10-Q）要約",
        "catalyst_type": "決算説明会公開テキスト解析 ＆ 株主還元（配当・自社株買い）開示",
        "entry": 610.15, "atr": 23.83, "iv": 48, "score": 87.9, "dp": "58.0%", "call_ratio": "2.5倍"
    },
    {
        "slug": "crwd-cybersecurity-pead-drift.html",
        "ticker": "CRWD",
        "jp_name": "クラウドストライク(CRWD)",
        "title": "クラウドストライク(CRWD) 年間経常収益（ARR）公開データと情報セキュリティ需要分析",
        "focus": "法人向けサイバーセキュリティのサブスクリプションARR（年間経常収益）とフリーキャッシュフロー推移に関する米SEC公開データ解説",
        "catalyst_type": "サブスクリプションARR公開統計 ＆ 機関投資家の保有比率推移",
        "entry": 216.90, "atr": 14.76, "iv": 56, "score": 86.5, "dp": "56.4%", "call_ratio": "2.7倍"
    },
    {
        "slug": "vrt-ai-datacenter-cooling-catalyst.html",
        "ticker": "VRT",
        "jp_name": "バーティブ(VRT)",
        "title": "バーティブ(VRT) データセンター電源・冷却設備の受注残（Backlog）公開データと変動幅試算",
        "focus": "データセンター向け熱管理・電源設備の受注残（Backlog）に関する米SEC公式決算開示（Form 8-K/10-Q）と適正分散比率シミュレーション",
        "catalyst_type": "データセンター設備受注開示 ＆ ボラティリティ配分計算",
        "entry": 182.86, "atr": 18.81, "iv": 72, "score": 88.1, "dp": "60.1%", "call_ratio": "2.9倍"
    },
    {
        "slug": "ceg-nuclear-ai-power-8k-contract.html",
        "ticker": "CEG",
        "jp_name": "コンステレーション・エナジー(CEG)",
        "title": "コンステレーション・エナジー(CEG) 長期電力供給契約（SEC Form 8-K）と公益インフラ収益構造",
        "focus": "データセンター向け長期クリーン電力購入契約（PPA）の米SEC公式適時開示（Form 8-K）と公益・インフラ企業の安定収益構造データ",
        "catalyst_type": "米SEC公式適時開示（Form 8-K 長期電力契約）＆ インフラ収益分析",
        "entry": 249.95, "atr": 12.02, "iv": 61, "score": 87.0, "dp": "55.3%", "call_ratio": "2.3倍"
    },
    {
        "slug": "mstr-bitcoin-volatility-atr-sizing.html",
        "ticker": "MSTR",
        "jp_name": "マイクロストラテジー(MSTR・高変動統計)",
        "title": "マイクロストラテジー(MSTR) 超高ボラティリティ銘柄の公開変動幅データと老後コア資産との区分解説",
        "focus": "暗号資産関連の財務開示（Form 8-K）に伴う年率100%超の価格変動リスク統計と、50〜70代の老後コア資産（国債・高配当・オルカン）から厳格に分離すべき数学的理由",
        "catalyst_type": "高ボラティリティ統計ケーススタディ ＆ 資産保全リスク教育",
        "entry": 128.93, "atr": 9.75, "iv": 108, "score": 65.0, "dp": "53.2%", "call_ratio": "1.8倍",
        "is_non_nisa_edu": True
    },
    {
        "slug": "arm-royalty-expansion-gamma-wall.html",
        "ticker": "ARM",
        "jp_name": "アーム(ARM)",
        "title": "アーム(ARM) 半導体設計ロイヤルティ収入の公開決算データとバリュエーション変動分析",
        "focus": "Armv9世代への移行に伴うロイヤルティ収入・ライセンス売上の米SEC公開決算データと、浮動株比率を踏まえた分散配分シミュレーション",
        "catalyst_type": "ロイヤルティ収益開示データ ＆ 公開市場需給バランス分析",
        "entry": 174.62, "atr": 14.23, "iv": 76, "score": 86.0, "dp": "56.0%", "call_ratio": "2.6倍"
    },
    {
        "slug": "asml-euv-orders-semiconductor-cycle.html",
        "ticker": "ASML",
        "jp_name": "ASMLホールディング(ASML)",
        "title": "ASMLホールディング EUV露光装置の受注統計・配当履歴と長期半導体サイクル解説",
        "focus": "先端半導体製造に不可欠なEUV露光装置の四半期受注統計と、欧米機関投資家の長期保有動向・配当推移データの可視化",
        "catalyst_type": "半導体製造装置サイクル統計 ＆ 長期機関投資家保有データ",
        "entry": 1424.75, "atr": 71.38, "iv": 49, "score": 85.8, "dp": "58.4%", "call_ratio": "2.0倍"
    },
    {
        "slug": "unh-defensive-healthcare-insider-buy.html",
        "ticker": "UNH",
        "jp_name": "ユナイテッドヘルス(UNH)",
        "title": "ユナイテッドヘルス(UNH) ディフェンシブ医療株の連続増配データとSEC Form-4公開記録",
        "focus": "景気変動に強い米国最大級ヘルスケア企業の連続増配実績・キャッシュフロー推移と、経営陣の市場内自社株取得（Form-4）データの解説",
        "catalyst_type": "ディフェンシブ増配実績データ ＆ SEC Form-4 公開記録",
        "entry": 394.15, "atr": 11.98, "iv": 34, "score": 88.5, "dp": "52.1%", "call_ratio": "1.9倍"
    },
    {
        "slug": "msft-azure-ai-copilot-sec-8k.html",
        "ticker": "MSFT",
        "terminal_ticker": "MSFT",
        "jp_name": "マイクロソフト(MSFT)",
        "title": "マイクロソフト(MSFT) クラウド収益・連続増配データと新NISA長期コア保有シミュレーション",
        "focus": "Azureクラウドおよび法人向けソフトウェアの安定キャッシュフロー・連続増配実績と、新NISA成長投資枠における長期資産配分試算",
        "catalyst_type": "クラウド収益開示（Form 10-Q）＆ 長期増配コア統計",
        "entry": 448.20, "atr": 9.40, "iv": 32, "score": 91.5, "dp": "59.5%", "call_ratio": "2.2倍"
    },
    {
        "slug": "aapl-apple-intelligence-cycle-gex.html",
        "ticker": "AAPL",
        "terminal_ticker": "AAPL",
        "jp_name": "アップル(AAPL)",
        "title": "アップル(AAPL) サービス部門利益率・自社株買い開示（SEC Form 10-Q）と長期保有データ",
        "focus": "世界中の稼働端末基盤が生み出すサービス部門の高粗利率と、大規模な自社株買い・安定配当に関する米SEC公開財務データの解説",
        "catalyst_type": "株主還元（自社株買い・配当）開示 ＆ 長期財務安定度分析",
        "entry": 232.80, "atr": 4.90, "iv": 29, "score": 90.2, "dp": "55.8%", "call_ratio": "2.1倍"
    },
    {
        "slug": "amzn-aws-margin-expansion-pead.html",
        "ticker": "AMZN",
        "terminal_ticker": "NVDA",
        "jp_name": "アマゾン(AMZN)",
        "title": "アマゾン(AMZN) AWS営業利益率と北米物流キャッシュフローに関する米SEC決算開示解析",
        "focus": "AWSクラウド部門の営業利益成長と物流効率化によるフリーキャッシュフロー拡大を米SEC公開決算データ（Form 10-Q）から読み解くガイド",
        "catalyst_type": "AWS営業利益率推移 ＆ 機関投資家の大口保有データ",
        "entry": 214.50, "atr": 5.30, "iv": 36, "score": 89.2, "dp": "60.2%", "call_ratio": "2.6倍"
    },
    {
        "slug": "googl-search-cloud-ai-valuation.html",
        "ticker": "GOOGL",
        "terminal_ticker": "NVDA",
        "jp_name": "アルファベット(GOOGL)",
        "title": "アルファベット(GOOGL) Google Cloud収益化・配当開始および自社株買い公開データ分析",
        "focus": "Google Cloudの営業利益拡大・検索広告キャッシュフローと、四半期配当および自社株買いに関する米SEC公式決算開示の要約",
        "catalyst_type": "Cloud収益成長 ＆ 株主還元・バリュエーション公開統計",
        "entry": 188.40, "atr": 4.60, "iv": 35, "score": 87.4, "dp": "56.9%", "call_ratio": "2.3倍"
    },
    {
        "slug": "sec-8k-japanese-ai-guide.html",
        "ticker": "MSFT",
        "terminal_ticker": "MSFT",
        "jp_name": "米SEC公式決算開示（Form 8-K）日本語ガイド",
        "title": "米SEC公式適時開示（Form 8-K/10-Q）とは？英語の一次財務情報をやさしく読み解く基礎マニュアル",
        "focus": "日本の個人投資家が知っておきたい米SEC EDGAR公式開示（重要契約Item 1.01・決算発表Item 2.02等）の基本構造と公開データの確認手順",
        "catalyst_type": "米SEC公開財務データ（EDGAR）基礎教育マニュアル",
        "entry": 448.20, "atr": 9.40, "iv": 32, "score": 91.5, "dp": "59.5%", "call_ratio": "2.2倍"
    },
    {
        "slug": "form4-insider-cluster-guide.html",
        "ticker": "LLY",
        "jp_name": "SEC Form-4 公開自社株取得データの読み方",
        "title": "米国株SEC Form-4（役員の自社株取得開示）とは？公開データの見方と注意点をやさしく解説",
        "focus": "ストックオプション自動売却（10b5-1計画）と純粋な市場内自社株取得（Code P）の違いを客観的に整理する米SEC公開データ教育ガイド",
        "catalyst_type": "SEC Form-4 公開内部者取引統計の基礎知識",
        "entry": 1354.00, "atr": 52.81, "iv": 42, "score": 89.8, "dp": "54.0%", "call_ratio": "2.1倍"
    },
    {
        "slug": "options-gamma-squeeze-gex-guide.html",
        "ticker": "NVDA",
        "jp_name": "オプション市場の予想変動幅（IV）基礎解説",
        "title": "米国株オプション市場の予想変動幅（インプライド・ボラティリティ）と機関需給の基礎知識",
        "focus": "公開オプション統計から算出される予想変動レンジ（Expected Move）の意味と、長期投資家が決算前後の値動きに慌てないための基礎教養",
        "catalyst_type": "公開市場マイクロストラクチャー ＆ ボラティリティ統計教育",
        "entry": 186.64, "atr": 8.02, "iv": 68, "score": 90.0, "dp": "61.4%", "call_ratio": "2.2倍"
    },
    {
        "slug": "fomc-cpi-iv-crush-strategy.html",
        "ticker": "VYM",
        "terminal_ticker": "VYM",
        "jp_name": "FOMC・米CPI発表と日米金利・為替の基礎知識",
        "title": "FOMC政策金利・米CPI発表がドル円為替と新NISA資産配分に与える影響の基礎ガイド",
        "focus": "米国連邦準備制度（FRB）の金利決定やインフレ統計（CPI）の公開日程と、年2〜4回の穏やかな資産配分点検における確認ポイント",
        "catalyst_type": "日米マクロ金利・為替統計 ＆ 老後資産配分教育ガイド",
        "entry": 134.50, "atr": 2.10, "iv": 18, "score": 92.0, "dp": "60.0%", "call_ratio": "2.0倍"
    },
    {
        "slug": "tradingview-pine-script-v5-atr-guide.html",
        "ticker": "MSFT",
        "terminal_ticker": "MSFT",
        "jp_name": "TradingView公開データ可視化スクリプト導入ガイド",
        "title": "TradingView Pine Script v5で平均変動幅（ATR統計帯）と長期トレンド帯を表示する設定手順",
        "focus": "自己判断のチャート学習ツールとしてTradingViewに14日平均変動幅バンドと長期移動平均線を表示する具体的な設定ステップ",
        "catalyst_type": "TradingView チャート可視化設定 ＆ 自己学習ツールガイド",
        "entry": 448.20, "atr": 9.40, "iv": 32, "score": 90.5, "dp": "59.5%", "call_ratio": "2.2倍"
    },
    {
        "slug": "us-stock-stop-loss-2percent-rule.html",
        "ticker": "VYM",
        "terminal_ticker": "VYM",
        "jp_name": "1銘柄集中を防ぐ分散配分比率（1.5%変動基準）の数学",
        "title": "老後資金・新NISAで1銘柄への買いすぎを防ぐ「許容変動幅1.5%基準・株数計算式」の数学的解説",
        "focus": "銘柄ごとの1日あたり平均値動き幅（ATR統計値）に応じて保有株数の上限を計算し、ポートフォリオ全体の安定性を保つ分散数理モデル",
        "catalyst_type": "ボラティリティ調整型・資産配分計算式の数学的基礎",
        "entry": 134.50, "atr": 2.10, "iv": 18, "score": 93.0, "dp": "61.0%", "call_ratio": "2.0倍"
    },
    {
        "slug": "dark-pool-whale-flow-reading.html",
        "ticker": "AVGO",
        "jp_name": "機関投資家の取引所外ブロック取引（ATS）公開統計とは",
        "title": "米国の取引所外大口取引（ATS公開統計）とは？年金基金・機関投資家の大口執行データの基礎知識",
        "focus": "米国FINRA等で公開される取引所外ブロック取引（ATS）比率の意味と、年金基金や長期機関投資家が市場インパクトを抑えて執行する仕組みの解説",
        "catalyst_type": "FINRA公開ATS統計データ ＆ 機関投資家執行インフラ解説",
        "entry": 293.69, "atr": 15.14, "iv": 58, "score": 88.4, "dp": "59.0%", "call_ratio": "2.1倍"
    },
    {
        "slug": "ai-datacenter-power-stocks-2026.html",
        "ticker": "CEG",
        "jp_name": "AIデータセンター電力・冷却インフラ公開財務データ比較",
        "title": "AIデータセンター電力・冷却インフラ関連米国株（CEG・VRT・AVGO）の公開決算データ比較",
        "focus": "電力供給契約（PPA）と冷却設備・半導体インフラを担う主要3社の米SEC公式決算開示（売上成長率・営業利益率・配当利回り）の客観比較",
        "catalyst_type": "電力・インフラ関連3社の公開財務指標・変動幅比較",
        "entry": 249.95, "atr": 12.02, "iv": 61, "score": 88.0, "dp": "57.5%", "call_ratio": "2.3倍"
    },
    {
        "slug": "semiconductor-cycle-truthofmarket-guide.html",
        "ticker": "VYM",
        "terminal_ticker": "VYM",
        "jp_name": "日米マクロ＆老後3つの財布 資産配分フレームワーク",
        "title": "日米マクロ金利・半導体サイクル統計と「老後3つの財布（国債・高配当・インデックス）」連携ガイド",
        "focus": "個人向け国債・新NISA適格の四半期高配当ETF（1489・VYM・HDV）・オルカン/S&P500に特定口座（SGOV・JEPI）を組み合わせる長期キャッシュフロー設計",
        "catalyst_type": "マクロサイクル公開統計 × 老後キャッシュフロー資産配分設計",
        "entry": 134.50, "atr": 2.10, "iv": 18, "score": 94.0, "dp": "61.4%", "call_ratio": "2.1倍"
    }
]


def _senior_clean_hub_text(text: str) -> str:
    """Ensures natural Japanese retirement & public data phrasing with zero awkward machine-replaced artifacts."""
    cleaned = str(text or "")
    fixes = [
        ("大口機関投資家機関投資家", "大口機関投資家"),
        ("機関大口機関投資家", "大口機関投資家"),
        ("大口機関実需機関", "大口機関投資家"),
        ("公式決算開示開示", "公式決算開示"),
        ("米国株米国公式", "米国SEC公式"),
        ("機関需給 Squeeze", "機関投資家の需給改善"),
        ("機関需給 Wall", "機関投資家の需給節目"),
        ("SEC Form 公式業績発表", "米SEC公式決算開示（Form 8-K/10-Q）"),
    ]
    for bad, good in fixes:
        cleaned = cleaned.replace(bad, good)
    return cleaned


def build_page_html(item, date_str, all_specs):
    slug = item["slug"]
    ticker = item["ticker"]
    term_ticker = item.get("terminal_ticker", ticker)
    jp_name = _senior_clean_hub_text(item["jp_name"])
    title = _senior_clean_hub_text(item["title"])
    focus = _senior_clean_hub_text(item["focus"])
    cat_type = _senior_clean_hub_text(item["catalyst_type"])
    entry = float(item["entry"])
    atr = float(item["atr"])
    iv = int(item["iv"])
    score = float(item["score"])
    dp = _senior_clean_hub_text(item["dp"])
    call_ratio = _senior_clean_hub_text(item["call_ratio"])
    is_avoid = bool(item.get("is_avoid", False))
    is_non_nisa_edu = bool(item.get("is_non_nisa_edu", False))

    stop_dist = round(atr * 2.0, 2)
    stop_loss = round(max(0.5, entry - stop_dist), 2)
    target_25r = round(entry + stop_dist * 2.5, 2)
    exp_move_5d = round(entry * (iv / 100.0) * math.sqrt(5.0 / 252.0), 2)

    default_acc = 50000
    max_risk = default_acc * 0.015
    shares = max(1, min(int(max_risk // max(stop_dist, 0.05)), int(default_acc // max(entry, 0.5))))
    notional_usd = round(shares * entry)
    notional_jpy_man = round(notional_usd * 150 / 10000, 1)
    risk_usd = round(shares * stop_dist)
    risk_jpy_man = round(risk_usd * 150 / 10000, 1)
    gain_usd = round(shares * (target_25r - entry))
    gain_jpy_man = round(gain_usd * 150 / 10000, 1)

    canonical_url = f"https://getbreakai.com/jp/{slug}"

    if is_avoid:
        banner_bg = "rgba(244,63,94,0.10)"
        banner_border = "rgba(244,63,94,0.45)"
        banner_color = "#881337"
        verdict_banner = (
            f"⚠️ 【公開財務リスク指標の確認】{jp_name} は公開データ安定度スコア {score}/100（{cat_type}・取引所外データ {dp}）のため、"
            f"1銘柄への偏重を避け公的開示（Form 10-K/8-K）を慎重に確認すべき高変動区分として表示されています。"
        )
    elif is_non_nisa_edu:
        banner_bg = "#fffbeb"
        banner_border = "#f59e0b"
        banner_color = "#78350f"
        verdict_banner = (
            f"🏛️ 【金融庁・新NISA制度区分のご注意】レバレッジ型ETF（SOXL・TQQQ）および毎月分配型ETF（JEPI・JEPQ・QYLD・SGOV）は"
            f"日本の金融庁規定により【新NISA対象外（特定口座のみ保有可）】です。50〜70代の老後資産形成には{FSA_HYBRID_PHRASE_JP}をご活用ください。"
        )
    else:
        banner_bg = "#ecfdf5"
        banner_border = "rgba(16,185,129,0.45)"
        banner_color = "#064e3b"
        verdict_banner = (
            f"📊 【公開市場データ要約】{jp_name} の公開財務・需給スコアは {score}/100（{cat_type}）です。"
            f"想定運用資金 $50,000（約750万円）における1銘柄分散目安は {shares}株（約{notional_jpy_man}万円）、"
            f"2.0倍ATR変動幅の参考下限値は ${stop_loss:.2f}、長期目標参考値は ${target_25r:.2f} です。"
        )

    related_candidates = [
        s for s in all_specs
        if s["slug"] != slug and s["slug"] not in MAIN_HUB_EXCLUDED_SLUGS
    ]
    related_links_html = "\n".join([
        f'<li><a href="/jp/{s["slug"]}" style="color:#1d4ed8; text-decoration:none; font-weight:700;">📘 {_senior_clean_hub_text(s["title"])}</a></li>'
        for s in related_candidates[:10]
    ])

    ld_graph = {
        "@context": "https://schema.org",
        "@graph": [
            {
                "@type": "Article",
                "headline": title,
                "description": verdict_banner,
                "datePublished": date_str,
                "dateModified": date_str,
                "inLanguage": "ja",
                "author": {
                    "@type": "Organization",
                    "name": "GetBreakAI Public Market Data Research",
                    "url": "https://getbreakai.com/jp/"
                },
                "publisher": {
                    "@type": "Organization",
                    "name": "GetBreakAI Educational Software",
                    "logo": {
                        "@type": "ImageObject",
                        "url": "https://getbreakai.com/og-preview.png"
                    }
                },
                "mainEntityOfPage": canonical_url
            },
            {
                "@type": "FAQPage",
                "mainEntity": [
                    {
                        "@type": "Question",
                        "name": f"{jp_name}の1銘柄あたり分散配分目安と平均変動幅（ATR統計値）はどのように計算しますか？",
                        "acceptedAnswer": {
                            "@type": "Answer",
                            "text": f"公開市場データ（{date_str}時点・基準価格${entry:.2f}、14日平均変動幅ATR ${atr:.2f}）に基づき、2.0倍変動幅（${stop_dist:.2f}）が運用資金全体の1.5%以内に収まるよう逆算すると、$50,000（約750万円）口座での分散目安は{shares}株（約{notional_jpy_man}万円）となります。"
                        }
                    },
                    {
                        "@type": "Question",
                        "name": "毎月分配型ETF（JEPI・SGOV等）やレバレッジ型ETF（SOXL等）は新NISAで買えますか？",
                        "acceptedAnswer": {
                            "@type": "Answer",
                            "text": "いいえ。日本の金融庁ルールにより、毎月分配型ETF（JEPI・JEPQ・QYLD・SGOV等）およびレバレッジ型ETF（SOXL・TQQQ等）は新NISAの対象外であり、特定口座でのみ保有可能です。新NISA枠では四半期配当のVYM・HDV・1489およびオルカン・S&P500を組み合わせるハイブリッド設計が適しています。"
                        }
                    },
                    {
                        "@type": "Question",
                        "name": "当サイトの計算ツールは投資助言ですか？",
                        "acceptedAnswer": {
                            "@type": "Answer",
                            "text": MANDATORY_DISCLAIMER_JP
                        }
                    }
                ]
            }
        ]
    }
    ld_json_str = json.dumps(ld_graph, ensure_ascii=False, indent=2)

    head_scripts = build_payment_and_kpi_head_html()
    disclaimer_box = build_mandatory_disclaimer_html()
    manual_modal = build_starter_manual_modal_html()
    waitlist_modal = build_vip_waitlist_modal_html()
    footer_html = build_legal_footer_html()

    return f"""<!DOCTYPE html>
<html lang="ja" data-jp-theme="light">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{title} | GetBreakAI ゆとり老後＆新NISA設計ナビ</title>
  <meta name="description" content="{jp_name}の{focus}を公開データからわかりやすく整理。{FSA_HYBRID_PHRASE_JP}とドル・円同時対応の資産配分シミュレーターを掲載。">
  <link rel="canonical" href="{canonical_url}">
  <link rel="alternate" hreflang="ja" href="{canonical_url}">
  <meta property="og:type" content="article">
  <meta property="og:locale" content="ja_JP">
  <meta property="og:site_name" content="GetBreakAI ゆとり老後＆新NISA設計ナビ">
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
{ld_json_str}
  </script>
{head_scripts}
  <style>
    :root {{
      --bg-page: #f4f6fa;
      --bg-card: #ffffff;
      --bg-sub: #f8fafc;
      --border-col: #cbd5e1;
      --text-main: #0b1f3a;
      --text-muted: #334155;
      --text-sub: #475569;
      --accent-blue: #1d4ed8;
      --accent-amber: #b45309;
      --accent-emerald: #047857;
      --accent-rose: #be123c;
      --font-sans: 'Noto Sans JP', -apple-system, BlinkMacSystemFont, sans-serif;
      --font-mono: 'JetBrains Mono', 'Noto Sans JP', monospace;
    }}
    * {{ box-sizing: border-box; margin: 0; padding: 0; }}
    body {{
      background: #f4f6fa !important;
      color: #0f172a !important;
      font-family: var(--font-sans);
      line-height: 1.78;
      font-size: 17px;
      font-feature-settings: "palt" 1;
      letter-spacing: 0.01em;
    }}
    .container {{ max-width: 960px; margin: 0 auto; padding: 0 20px; }}
    header {{
      background: #0b1f3a !important;
      border-bottom: 2px solid #1e3a8a !important;
      padding: 15px 0;
      position: sticky;
      top: 0;
      z-index: 50;
    }}
    .nav-bar {{ display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 10px; }}
    .brand {{ color: #f8fafc !important; font-weight: 900; font-size: 1.15rem; text-decoration: none; }}
    .nav-sublink {{ color: #e2e8f0 !important; text-decoration: none; font-size: 0.9rem; padding: 6px 8px; font-weight: 700; }}
    .btn-cta {{
      background: linear-gradient(135deg, #1d4ed8, #1e3a8a);
      color: #ffffff !important;
      text-decoration: none;
      padding: 9px 16px;
      border-radius: 9px;
      font-weight: 800;
      font-size: 0.9rem;
      border: none;
      cursor: pointer;
    }}
    .shorts-bridge-bar {{
      background: #eff6ff;
      border: 1.5px solid #93c5fd;
      border-radius: 12px;
      padding: 11px 14px;
      margin-top: 18px;
      display: flex;
      align-items: center;
      justify-content: center;
      flex-wrap: wrap;
      gap: 10px;
      font-size: 0.92rem;
      color: #0f172a;
    }}
    .article-box {{
      background: #ffffff !important;
      border: 1.5px solid #cbd5e1 !important;
      box-shadow: 0 8px 24px rgba(15,23,42,0.06) !important;
      border-radius: 16px;
      padding: 30px 28px;
      margin-top: 22px;
    }}
    h1 {{ font-size: clamp(1.48rem, 3vw, 2.05rem); line-height: 1.38; margin-bottom: 14px; font-weight: 900; color: #0b1f3a !important; }}
    h2 {{ font-size: 1.28rem; color: #1e3a8a !important; margin: 30px 0 12px; border-left: 5px solid #1d4ed8 !important; background: #eff6ff; padding: 8px 12px !important; border-radius: 0 8px 8px 0; }}
    h3 {{ font-size: 1.08rem; color: #0b1f3a !important; margin: 18px 0 8px; }}
    p, li {{ color: #1e293b !important; margin-bottom: 14px; font-size: 1rem; line-height: 1.78; }}
    .kpi-grid {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(195px, 1fr));
      gap: 12px;
      margin: 20px 0;
    }}
    .kpi-card {{
      background: #f8fafc !important;
      border: 1.5px solid #cbd5e1 !important;
      border-radius: 10px;
      padding: 14px;
    }}
    .kpi-label {{ font-size: 0.82rem; color: #475569 !important; font-weight: 700; }}
    .kpi-val {{ font-size: 1.18rem; font-weight: 800; font-family: var(--font-mono); margin-top: 4px; color: #0b1f3a !important; }}
    .widget-box {{
      background: #f8fafc !important;
      border: 2px solid #1d4ed8 !important;
      border-radius: 14px;
      padding: 22px;
      margin: 24px 0;
    }}
    /* Shared ¥0 Manual Modal styles */
    .gba-manual-free-badge {{ display:inline-flex; align-items:center; gap:6px; background:#059669; color:#ffffff; font-size:0.86rem; font-weight:900; padding:4px 12px; border-radius:999px; }}
    .gba-manual-modal-backdrop {{ display:none; position:fixed; inset:0; z-index:9999; background:rgba(15,23,42,0.76); backdrop-filter:blur(4px); padding:18px 12px; overflow-y:auto; align-items:flex-start; justify-content:center; }}
    .gba-manual-modal-backdrop.is-open {{ display:flex; }}
    .gba-manual-modal-dialog {{ background:#ffffff; color:#0b1f3a; border:2px solid #059669; border-radius:16px; width:100%; max-width:860px; margin:8px auto 32px; box-shadow:0 22px 50px rgba(0,0,0,0.45); overflow:hidden; }}
    .gba-manual-modal-header {{ position:sticky; top:0; z-index:5; background:#ffffff; border-bottom:2px solid #cbd5e1; padding:14px 18px; display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:10px; }}
    .gba-manual-modal-title {{ font-size:1.18rem; font-weight:900; color:#0b1f3a; margin:4px 0 0; }}
    .gba-manual-modal-actions {{ display:flex; gap:8px; flex-wrap:wrap; }}
    .gba-manual-action-btn {{ appearance:none; min-height:46px; padding:8px 14px; border-radius:10px; font-size:0.96rem; font-weight:900; cursor:pointer; border:2px solid #cbd5e1; background:#f8fafc; color:#0b1f3a; }}
    .gba-manual-action-btn.btn-print {{ border-color:#059669; background:#ecfdf5; color:#065f46; }}
    .gba-manual-nav-pills {{ display:flex; flex-wrap:wrap; gap:8px; padding:12px 18px; background:#f8fafc; border-bottom:1px solid #cbd5e1; }}
    .gba-manual-jump-pill {{ appearance:none; min-height:44px; padding:7px 13px; border-radius:999px; border:1.5px solid #cbd5e1; background:#ffffff; color:#0b1f3a; font-size:0.94rem; font-weight:800; cursor:pointer; }}
    .gba-manual-modal-body {{ padding:20px; font-size:1.05rem; line-height:1.8; }}
    .gba-manual-chapter-box {{ background:#f8fafc; border:1.5px solid #cbd5e1; border-radius:14px; padding:18px; margin-bottom:16px; }}
    .gba-manual-broker-grid {{ display:grid; grid-template-columns:repeat(auto-fit, minmax(260px, 1fr)); gap:12px; margin-top:10px; }}
    .gba-manual-broker-card {{ background:#ffffff; border:1.5px solid #cbd5e1; border-radius:12px; padding:14px; }}
    .gba-manual-tip-callout {{ margin-top:12px; padding:12px 14px; border-radius:10px; background:#ecfdf5; border-left:4px solid #059669; font-weight:700; }}
    .gba-manual-modal-funnel {{ background:#eff6ff; border:2px solid #059669; border-radius:14px; padding:18px; margin-top:10px; }}
    .gba-manual-open-btn {{ appearance:none; background:linear-gradient(135deg,#059669,#047857); color:#ffffff; border:none; border-radius:11px; padding:12px 18px; min-height:52px; font-size:1rem; font-weight:900; cursor:pointer; }}
    .gba-manual-funnel-links {{ display:flex; flex-wrap:wrap; gap:10px; margin-top:10px; }}
    .gba-manual-pro-link, .gba-manual-vip-link {{ display:inline-flex; align-items:center; min-height:46px; padding:8px 14px; border-radius:999px; font-size:0.95rem; font-weight:900; text-decoration:none; background:#ffffff; border:1.5px solid #1d4ed8; color:#1d4ed8; }}
    @media (max-width: 640px) {{
      .article-box {{ padding: 20px 15px; }}
    }}
    @media print {{
      body.printing-gba-manual > *:not(#gbaStarterManualModal) {{ display: none !important; }}
      body.printing-gba-manual #gbaStarterManualModal {{ display: block !important; position: static !important; background: #ffffff !important; padding: 0 !important; }}
    }}
  </style>
</head>
<body>
  <header>
    <div class="container nav-bar">
      <a href="/jp/" class="brand">⚡ GetBreakAI ゆとり老後＆新NISA設計ナビ</a>
      <div style="display:flex; gap:8px; flex-wrap:wrap; align-items:center;">
        <a href="https://www.youtube.com/@GetBreakAI" target="_blank" rel="noopener" class="nav-sublink">📺 公式YouTube</a>
        <button type="button" onclick="openGbaStarterManualModal()" class="nav-sublink" style="background:#065f46; border:1px solid #10b981; border-radius:7px; cursor:pointer;">📘 ¥0 基本マニュアル</button>
        <a href="/jp/#gba-retirement-architect-jp" class="btn-cta">🧭 30秒・老後収入シミュレーター →</a>
      </div>
    </div>
  </header>

  <main class="container">
    <div class="shorts-bridge-bar">
      <strong>🧭 50〜70代のゆとり老後＆新NISAキャッシュフロー設計：</strong>
      <a href="#miniCalcBox" class="btn-cta" style="padding:6px 12px; font-size:0.84rem;">🧮 1銘柄分散比率シミュレーターへ</a>
      <button type="button" onclick="openGbaStarterManualModal()" style="background:#ecfdf5; color:#065f46; border:1.5px solid #059669; border-radius:8px; padding:6px 12px; font-weight:800; font-size:0.84rem; cursor:pointer;">📘 ¥0 楽天・SBI証券 新NISA設定マニュアル</button>
    </div>

    <article class="article-box">
      <div style="font-family:var(--font-mono); font-size:0.84rem; color:var(--accent-amber); font-weight:800; margin-bottom:8px;">
        📊 公開市場データ更新日: {date_str} ｜ 対象データ: {jp_name} (${ticker})
      </div>
      <h1>{title}</h1>
      <p style="font-size:1.05rem; font-weight:800; color:#1e3a8a !important; margin-bottom:14px;">
        🧭 大切な退職金と新NISA非課税枠を1銘柄への偏重から守るため、ご資金に対する穏やかな資産配分目安を3秒で試算できます。
      </p>
      <div style="background:{banner_bg}; border:1.5px solid {banner_border}; border-radius:10px; padding:14px 16px; margin-bottom:22px; color:{banner_color}; font-weight:700; font-size:1.02rem; line-height:1.68;">
        {verdict_banner}
      </div>

      <!-- 上部：無料倶楽部メール登録 ＆ Proソフトウェア案内 -->
      <section id="gba-jp-lead-top" style="margin:20px 0 26px; padding:22px; background:linear-gradient(135deg,#ecfdf5 0%,#eff6ff 100%); border:2.5px solid #059669; border-radius:16px;">
        <div style="display:inline-block; background:#065f46; color:#ffffff; font-size:0.88rem; font-weight:800; padding:4px 13px; border-radius:999px; margin-bottom:10px;">
          🍵 朝のゆとり老後＆日米マクロ倶楽部（無料・パスワード不要）
        </div>
        <h2 style="margin:0 0 8px !important; background:transparent !important; border:none !important; padding:0 !important; font-size:1.32rem; line-height:1.42; color:#0b1f3a !important;">
          毎朝8時「日米マクロ・新NISA 3色バランス指標ブリーフ」無料メール登録
        </h2>
        <p style="margin:0 0 14px; font-size:1.02rem; line-height:1.68; color:#1e293b !important;">
          メールアドレス1つ（3秒）で、毎朝の金利・ドル円為替・老後3つの財布の公開データ要約と『¥0 新NISA基本設定マニュアル』を無料でお届けします。
        </p>
        <form class="gba-jp-signup-form" onsubmit="return window.__gbaSubmitJpSignup(event, this, '{ticker}');" style="display:flex; flex-wrap:wrap; gap:10px; align-items:stretch;">
          <label for="gbaTopEmail_{ticker}" style="position:absolute; width:1px; height:1px; overflow:hidden; clip:rect(0,0,0,0);">メールアドレス</label>
          <input id="gbaTopEmail_{ticker}" type="email" required autocomplete="email" placeholder="メールアドレスを入力（例: yamada@yahoo.co.jp）" style="flex:1 1 260px; min-height:56px; padding:12px 16px; font-size:1.04rem; font-weight:700; border-radius:12px; border:2px solid #64748b; background:#ffffff; color:#0f172a;">
          <button type="submit" style="min-height:56px; padding:12px 22px; font-size:1.02rem; font-weight:900; border-radius:12px; border:none; background:#059669; color:#ffffff; cursor:pointer;">
            📩 無料で毎朝の3色バランス指標を受け取る →
          </button>
        </form>
        <div class="gba-jp-signup-status" role="status" aria-live="polite" style="display:none; margin-top:12px; padding:12px 14px; border-radius:10px; background:#d1fae5; color:#065f46; font-size:1rem; font-weight:800;"></div>

        <div style="margin-top:16px; padding-top:14px; border-top:1px solid #a7f3d0;">
          <div style="display:flex; flex-wrap:wrap; align-items:center; justify-content:space-between; gap:10px;">
            <span style="font-size:0.96rem; font-weight:800; color:#0f172a;">💎 全銘柄データ一覧・配当＆資産配分計算Proソフトウェア：</span>
            <div style="display:flex; flex-wrap:wrap; gap:10px;">
              <a href="{LS_MONTHLY_URL_HTML}" data-gba-paid-plan="monthly" data-ls-product-uuid="{LS_MONTHLY_UUID}" class="lemonsqueezy-button" style="display:inline-flex; align-items:center; justify-content:center; min-height:56px; padding:10px 18px; border-radius:10px; background:#1d4ed8; color:#ffffff !important; font-size:0.98rem; font-weight:900; text-decoration:none;">
                ⚡ {PRICE_LABEL_MONTHLY_JP}
              </a>
              <a href="{LS_ANNUAL_URL_HTML}" data-gba-paid-plan="annual" data-ls-product-uuid="{LS_ANNUAL_UUID}" class="lemonsqueezy-button" style="display:inline-flex; align-items:center; justify-content:center; min-height:56px; padding:10px 18px; border-radius:10px; background:#b45309; color:#ffffff !important; font-size:0.98rem; font-weight:900; text-decoration:none;">
                👑 {PRICE_LABEL_ANNUAL_JP}
              </a>
            </div>
          </div>
{disclaimer_box}
        </div>
      </section>

      <div class="kpi-grid">
        <div class="kpi-card">
          <div class="kpi-label">直近基準株価（公開終値）</div>
          <div class="kpi-val">${entry:.2f} <span style="font-size:0.8rem; color:#475569; font-weight:700;">(約¥{int(round(entry*150)):,})</span></div>
        </div>
        <div class="kpi-card">
          <div class="kpi-label">公開データ安定度スコア</div>
          <div class="kpi-val" style="color:#1d4ed8 !important;">{score} / 100</div>
        </div>
        <div class="kpi-card">
          <div class="kpi-label">2.0倍ATR 変動幅参考値</div>
          <div class="kpi-val" style="color:#be123c !important;">${stop_loss:.2f} <span style="font-size:0.78rem;">(幅 ${stop_dist:.2f})</span></div>
        </div>
        <div class="kpi-card">
          <div class="kpi-label">長期リスクリワード参考値</div>
          <div class="kpi-val" style="color:#047857 !important;">${target_25r:.2f}</div>
        </div>
      </div>

      <!-- 自己判断用・資産配分＆変動幅シミュレーター -->
      <div class="widget-box" id="miniCalcBox">
        <h3 style="margin-top:0;">🧮 {jp_name}：1銘柄集中を防ぐ資産配分＆許容変動幅シミュレーター（ドル $ / 日本円 ¥ 同時換算）</h3>
        <p style="font-size:0.95rem; color:#334155 !important; margin-bottom:14px;">
          ご自身の運用資産総額に合わせてスライダーを動かすと、1銘柄あたりの価格変動（14日ATR×2.0倍）を資産全体の1.5%以内に抑える「分散保有株数の目安」を自動計算します。
        </p>
        <div style="margin-bottom:14px;">
          <div style="display:flex; justify-content:space-between; font-family:var(--font-mono); font-size:0.92rem; margin-bottom:6px; color:#334155;">
            <span>想定ご運用資産 (1ドル=150円基準):</span>
            <strong id="miniAccLbl" style="color:#b45309;">$50,000 (約750.0万円)</strong>
          </div>
          <input type="range" id="miniAccSlider" min="5000" max="250000" step="5000" value="50000" style="width:100%; accent-color:#1d4ed8;" oninput="recalcMiniWidget()">
        </div>
        <div class="kpi-grid" style="margin:14px 0 0;">
          <div class="kpi-card">
            <div class="kpi-label">分散保有株数の目安</div>
            <div id="miniOutShares" class="kpi-val" style="color:#b45309 !important;">{shares}株 (${notional_usd:,} / 約{notional_jpy_man}万円)</div>
          </div>
          <div class="kpi-card">
            <div class="kpi-label">2.0倍ATR変動時の想定振れ幅</div>
            <div id="miniOutRisk" class="kpi-val" style="color:#be123c !important;">-${risk_usd:,} (約{risk_jpy_man}万円)</div>
          </div>
          <div class="kpi-card">
            <div class="kpi-label">長期2.5倍目標時の試算差額</div>
            <div id="miniOutGain" class="kpi-val" style="color:#047857 !important;">+${gain_usd:,} (約{gain_jpy_man}万円)</div>
          </div>
        </div>
        <div style="margin-top:16px; display:flex; gap:10px; flex-wrap:wrap;">
          <a href="/jp/?ticker={term_ticker}#jpQuickCalcSection" class="btn-cta">🧭 新NISA・老後3つの財布シミュレーターで全体配分を確認 →</a>
        </div>
      </div>

      <h2>1. {jp_name} の米SEC公式決算開示（Form 8-K/10-Q）および公開業績データの整理</h2>
      <p>
        50〜70代の個人投資家が新NISAや退職金運用で最も大切にしたいのは、SNSの噂や一時的なブームに惑わされず、<strong>企業が規制当局へ提出した一次公開情報（米SEC Form 8-K・Form 10-Q・年次報告書Form 10-K）</strong>を落ち着いた視点で確認することです。{jp_name} に関する現在の主要確認テーマは「<strong>{focus}</strong>」であり、公開データ可視化スコアは <strong>{score}/100（区分：{cat_type}）</strong> となっています。
      </p>
      <p>
        英語で公開される決算発表や設備投資計画・配当方針の開示も、売上成長率・営業利益率・フリーキャッシュフローの3点に絞って整理すれば決して難しくありません。当ページではすべての利用者に同一の客観的統計データを表示し、ご自身のペースで資産配分を点検するための基礎資料を提供しています。
      </p>

      <h2>2. SEC Form-4（役員自社株取得記録）および大口機関投資家の公開需給統計（{dp}）</h2>
      <p>
        日々の株価変動の背景にある中長期の資金動向を知るうえで参考になるのが、<strong>SEC Form-4（経営陣による市場内での自社株取得開示）</strong>と、米国FINRA等で集計される<strong>取引所外の大口機関投資家取引比率（現在 {dp}、オプション需給倍率 {call_ratio}）</strong>です。
      </p>
      <p>
        年金基金や長期運用の機関投資家は、一度に大量の注文を出して市場価格を乱高下させないよう、複数日に分けて穏やかにポジションを構築します。同様に個人の老後資産づくりにおいても、一度に全額を1銘柄へ投じるのではなく、時間と資産クラスを分けて穏やかに保有比率を整えることが長期の安心につながります。
      </p>

      <h2>3. 【重要・金融庁規定準拠】新NISA適格銘柄と特定口座（毎月分配型）のハイブリッド設計</h2>
      <p>
        日本の金融庁ルールにより、米国ETFや国内ETFを老後の毎月キャッシュフローづくりに活用する際は<strong>「新NISA口座で保有できる銘柄」と「特定口座でのみ保有できる銘柄」の法的な違い</strong>を正確に把握しておく必要があります。具体的には、<strong>毎月分配型ETF（JEPI・JEPQ・QYLD・SGOV等）およびレバレッジ型ETF（SOXL・TQQQ等）は金融庁規定により新NISA（つみたて投資枠・成長投資枠とも）の対象外</strong>です。
      </p>
      <p>
        そのため、年金にプラスする安定したキャッシュフローを設計する際は、<strong>{FSA_HYBRID_PHRASE_JP}</strong>が王道となります。新NISA枠内では四半期配当の<strong>1489（1・4・7・10月決算）</strong>と<strong>VYM・HDV（3・6・9・12月分配）</strong>、および長期成長の<strong>オルカン・S&amp;P500</strong>を組み合わせて20.315%非課税メリットを活かし、毎月分配の<strong>SGOV（米国短期国債ETF）やJEPI</strong>を組み入れる場合は必ず<strong>特定口座（源泉徴収あり）</strong>で区分管理してください。
      </p>

      <h2>4. 年2〜4回の穏やかな資産配分点検と1銘柄あたりの買いすぎ防止計算</h2>
      <p>
        新NISA口座では頻繁に売却を繰り返すと年間360万円の非課税投資枠を消化してしまうほか、万が一含み損が生じても特定口座と損益通算ができない仕組みになっています。したがって、短期的な値動きを追いかけるのではなく、<strong>「①守りの財布（個人向け国債・待機預金）」「②収入の財布（高配当ETF）」「③成長の財布（オルカン・S&amp;P500・優良大型株）」の比率を年2〜4回だけゆったり見直す運用</strong>がシニア世代の資産寿命を大きく延ばします。
      </p>
      <p>
        個別銘柄である {jp_name}（基準値 ${entry:.2f}、14日平均変動幅 ${atr:.2f}）を一部組み入れる場合も、2.0倍変動幅（${stop_dist:.2f}）の振れが口座全体の1.5%以内に収まる株数（$50,000＝約750万円口座で {shares}株・約{notional_jpy_man}万円）にとどめることで、夜もぐっすり眠れる健全な分散バランスを維持できます。
      </p>

      <!-- 下部：無料倶楽部登録 ＆ Proソフトウェア案内 -->
      <section id="gba-jp-lead-bottom" style="margin-top:32px; padding:24px; background:linear-gradient(135deg,#ecfdf5 0%,#eff6ff 100%); border:2.5px solid #059669; border-radius:16px;">
        <h3 style="margin-top:0; font-size:1.28rem;">🍵 無料正会員登録（パスワード不要・3秒）：毎朝8時の「新NISA 3色バランス指標ブリーフ」</h3>
        <p style="margin-bottom:14px; font-size:1.02rem;">クレジットカード不要・いつでも1クリック配信停止可能。毎朝の日米マクロ市場と老後3つの財布バランス指標を無料でお届けします。</p>
        <form class="gba-jp-signup-form" onsubmit="return window.__gbaSubmitJpSignup(event, this, '{ticker}');" style="display:flex; flex-wrap:wrap; gap:10px; margin-bottom:14px;">
          <label for="gbaBotEmail_{ticker}" style="position:absolute; width:1px; height:1px; overflow:hidden; clip:rect(0,0,0,0);">メールアドレス</label>
          <input id="gbaBotEmail_{ticker}" type="email" required autocomplete="email" placeholder="メールアドレスを入力（例: yamada@yahoo.co.jp）" style="flex:1 1 260px; min-height:56px; padding:12px 16px; font-size:1.04rem; font-weight:700; border-radius:12px; border:2px solid #64748b; background:#ffffff; color:#0f172a;">
          <button type="submit" style="min-height:56px; padding:12px 22px; font-size:1.02rem; font-weight:900; border-radius:12px; border:none; background:#059669; color:#ffffff; cursor:pointer;">
            📩 無料メール倶楽部に参加する →
          </button>
        </form>
        <div class="gba-jp-signup-status" role="status" aria-live="polite" style="display:none; margin-bottom:14px; padding:12px 14px; border-radius:10px; background:#d1fae5; color:#065f46; font-size:1rem; font-weight:800;"></div>

        <div style="padding-top:14px; border-top:1px solid #93c5fd;">
          <div style="font-size:1rem; font-weight:900; color:#0b1f3a; margin-bottom:10px; text-align:center;">💎 全銘柄の公開データ一覧・配当＆資産配分計算Proソフトウェア：</div>
          <div style="display:flex; justify-content:center; gap:10px; flex-wrap:wrap; margin-bottom:10px;">
            <a href="/jp/#gba-retirement-architect-jp" class="btn-cta" style="min-height:56px; display:inline-flex; align-items:center; padding:10px 18px;">🧭 無料30秒・老後収入シミュレーターを開く →</a>
            <a href="{LS_MONTHLY_URL_HTML}" data-gba-paid-plan="monthly" data-ls-product-uuid="{LS_MONTHLY_UUID}" class="lemonsqueezy-button btn-cta" style="min-height:56px; display:inline-flex; align-items:center; padding:10px 18px; background:linear-gradient(135deg,#059669,#047857);">⚡ {PRICE_LABEL_MONTHLY_JP}</a>
            <a href="{LS_ANNUAL_URL_HTML}" data-gba-paid-plan="annual" data-ls-product-uuid="{LS_ANNUAL_UUID}" class="lemonsqueezy-button btn-cta" style="min-height:56px; display:inline-flex; align-items:center; padding:10px 18px; background:linear-gradient(135deg,#d97706,#b45309);">👑 {PRICE_LABEL_ANNUAL_JP}</a>
          </div>
          <div style="text-align:center; font-size:0.86rem; color:#475569;">
            🏛️ 法人・金融メディア・データ連携窓口: <a href="mailto:beable9489@gmail.com" style="color:#1d4ed8; font-weight:800;">beable9489@gmail.com</a>
          </div>
{disclaimer_box}
        </div>
      </section>

      <h2>📚 関連する新NISA・日米優良株 公開データ教育リサーチ記事</h2>
      <ul style="list-style:none; line-height:2.0; font-size:0.96rem;">
        {related_links_html}
      </ul>
    </article>
  </main>

{footer_html}
{manual_modal}
{waitlist_modal}

  <script>
    const ENTRY_PRICE = {entry:.2f};
    const STOP_DIST = {stop_dist:.2f};
    const TARGET_PRICE = {target_25r:.2f};
    const FX = 150.0;

    function recalcMiniWidget() {{
      const slider = document.getElementById('miniAccSlider');
      const acc = parseFloat(slider ? slider.value : 50000) || 50000;
      const accJpyMan = (acc * FX / 10000).toFixed(1);
      const lbl = document.getElementById('miniAccLbl');
      if (lbl) lbl.innerText = '$' + acc.toLocaleString() + ' (約' + accJpyMan + '万円)';
      const maxRisk = acc * 0.015;
      const shares = Math.max(1, Math.min(Math.floor(maxRisk / Math.max(STOP_DIST, 0.05)), Math.floor(acc / Math.max(ENTRY_PRICE, 0.5))));
      const notional = Math.round(shares * ENTRY_PRICE);
      const notionalMan = (notional * FX / 10000).toFixed(1);
      const riskUsd = Math.round(shares * STOP_DIST);
      const riskMan = (riskUsd * FX / 10000).toFixed(1);
      const gainUsd = Math.round(shares * (TARGET_PRICE - ENTRY_PRICE));
      const gainMan = (gainUsd * FX / 10000).toFixed(1);

      const elS = document.getElementById('miniOutShares');
      const elR = document.getElementById('miniOutRisk');
      const elG = document.getElementById('miniOutGain');
      if (elS) elS.innerText = shares + '株 ($' + notional.toLocaleString() + ' / 約' + notionalMan + '万円)';
      if (elR) elR.innerText = '-$' + riskUsd.toLocaleString() + ' (約' + riskMan + '万円)';
      if (elG) elG.innerText = '+$' + gainUsd.toLocaleString() + ' (約' + gainMan + '万円)';
    }}

    function jumpFromManualToJpMail() {{
      if (typeof window.closeGbaStarterManualModal === 'function') window.closeGbaStarterManualModal();
      const topLead = document.getElementById('gba-jp-lead-top');
      if (topLead && topLead.scrollIntoView) topLead.scrollIntoView({{ behavior: 'smooth', block: 'center' }});
      setTimeout(function() {{
        const inp = topLead ? topLead.querySelector('input[type="email"]') : null;
        if (inp && inp.focus) inp.focus();
      }}, 350);
    }}

    window.addEventListener('DOMContentLoaded', function() {{
      try {{
        const saved = localStorage.getItem('gb_free_member_email') || localStorage.getItem('gba_jp_free_email');
        if (saved) {{
          document.querySelectorAll('.gba-jp-signup-form input[type="email"]').forEach(function(inp) {{ inp.value = saved; }});
        }}
      }} catch (_e) {{}}
    }});
  </script>
</body>
</html>
"""


def build_hub_html(date_str: str, all_specs: list, is_root: bool = False) -> str:
    canonical_url = "https://getbreakai.com/" if is_root else "https://getbreakai.com/jp/"
    hreflang_tags = (
        '  <link rel="alternate" hreflang="ja" href="https://getbreakai.com/">\n'
        '  <link rel="alternate" hreflang="x-default" href="https://getbreakai.com/">'
        if is_root else
        '  <link rel="alternate" hreflang="ja" href="https://getbreakai.com/jp/">'
    )

    senior_specs = [
        s for s in all_specs
        if s["slug"] not in MAIN_HUB_EXCLUDED_SLUGS
        and s["ticker"] not in ("SOXL", "TQQQ", "COIN", "MSTR")
    ]
    cards_html = "\n".join([
        f'<a href="/jp/{s["slug"]}" class="hub-seo-card">'
        f'<div class="hub-seo-meta">${s["ticker"]} · 公開データ安定度 {s["score"]}/100</div>'
        f'<div class="hub-seo-title">{_senior_clean_hub_text(s["title"])}</div>'
        f'<div class="hub-seo-focus">{_senior_clean_hub_text(s["focus"])}</div>'
        f'</a>'
        for s in senior_specs
    ])

    head_scripts = build_payment_and_kpi_head_html()
    disclaimer_box = build_mandatory_disclaimer_html()
    manual_modal = build_starter_manual_modal_html()
    waitlist_modal = build_vip_waitlist_modal_html()
    footer_html = build_legal_footer_html()

    ld_json = json.dumps({
        "@context": "https://schema.org",
        "@graph": [
            {
                "@type": "SoftwareApplication",
                "name": "GetBreakAI — 年金＋新NISA ゆとり老後＆配当・資産配分計算ソフトウェア",
                "url": canonical_url,
                "image": "https://getbreakai.com/og-preview.png",
                "inLanguage": "ja",
                "applicationCategory": "FinanceApplication",
                "operatingSystem": "Web",
                "description": f"50〜70代の日本の個人投資家向け{SOFTWARE_POSITIONING_JP}。{FSA_HYBRID_PHRASE_JP}に基づく老後キャッシュフロー試算を提供。",
                "offers": [
                    {
                        "@type": "Offer",
                        "name": PRICE_LABEL_MONTHLY_JP,
                        "price": "29.00",
                        "priceCurrency": "USD",
                        "url": f"https://truthofmarket.lemonsqueezy.com/checkout/buy/{LS_MONTHLY_UUID}?embed=1&locale=ja"
                    },
                    {
                        "@type": "Offer",
                        "name": PRICE_LABEL_ANNUAL_JP,
                        "price": "199.00",
                        "priceCurrency": "USD",
                        "url": f"https://truthofmarket.lemonsqueezy.com/checkout/buy/{LS_ANNUAL_UUID}?embed=1&locale=ja"
                    }
                ]
            },
            {
                "@type": "FAQPage",
                "mainEntity": [
                    {
                        "@type": "Question",
                        "name": "JEPIやSGOVなどの毎月分配型ETFやSOXLは新NISA口座で購入できますか？",
                        "acceptedAnswer": {
                            "@type": "Answer",
                            "text": "いいえ。日本の金融庁規定により、毎月分配型ETF（JEPI・JEPQ・QYLD・SGOV等）およびレバレッジ型ETF（SOXL・TQQQ等）は新NISAの対象外です。当サイトでは『新NISA 適格（四半期配当 VYM・HDV・1489・オルカン・S&P500 時間差組み合わせ）＋ 特定口座（毎月分配 SGOV・JEPI）ハイブリッド設計』をご案内しています。"
                        }
                    },
                    {
                        "@type": "Question",
                        "name": "当サイトは投資助言や個別銘柄の推奨を行うサービスですか？",
                        "acceptedAnswer": {
                            "@type": "Answer",
                            "text": MANDATORY_DISCLAIMER_JP
                        }
                    }
                ]
            }
        ]
    }, ensure_ascii=False, indent=2)

    return f"""<!DOCTYPE html>
<html lang="ja" data-jp-theme="light">
<head>
  <meta charset="UTF-8">
  <meta name="google-site-verification" content="lM2Bf7R0XRTUDg-IZvGV9i06u2Q5rz6HJ8-IwoLFcgo">
  <meta name="google-site-verification" content="nAGlJMEUUPifbzSd8X4PCaBIyr3DtTwaa1a-q9zkbBc">
  <meta name="google-site-verification" content="G99bl17UU6iKgNm5ndGcSWp0dHFpJ0MjJqBBp0Exfx0">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>年金＋新NISAで『毎月ゆとりある老後収入』を設計し、資産寿命を守る羅針盤 | GetBreakAI</title>
  <meta name="description" content="50〜70代のための30秒・ゆとり老後＆新NISA毎月キャッシュフロー設計シミュレーター。{FSA_HYBRID_PHRASE_JP}を3色バランス指標で年2〜4回ゆったり配分点検。">
  <link rel="canonical" href="{canonical_url}">
{hreflang_tags}
  <meta property="og:type" content="website">
  <meta property="og:locale" content="ja_JP">
  <meta property="og:site_name" content="GetBreakAI">
  <meta property="og:title" content="年金＋新NISAで『毎月ゆとりある老後収入』を設計し、資産寿命を守る羅針盤 | GetBreakAI">
  <meta property="og:description" content="30秒で年金＋月いくらの非課税ゆとり収入が作れるか試算。{FSA_HYBRID_PHRASE_JP}対応。">
  <meta property="og:url" content="{canonical_url}">
  <meta property="og:image" content="https://getbreakai.com/og-preview.png">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="年金＋新NISAで『毎月ゆとりある老後収入』を設計し、資産寿命を守る羅針盤 | GetBreakAI">
  <meta name="twitter:description" content="50〜70代のための新NISA×特定口座ハイブリッド老後キャッシュフロー計算ソフトウェア。">
  <meta name="twitter:image" content="https://getbreakai.com/og-preview.png">
  <link rel="icon" type="image/svg+xml" href="/favicon.svg">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;600;800&family=Noto+Sans+JP:wght@400;500;700;800;900&display=swap" rel="stylesheet">
  <script type="application/ld+json">
{ld_json}
  </script>
{head_scripts}
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
    html {{ font-size: 17px; }}
    html[data-jp-font="large"] {{ font-size: 19px; }}
    html[data-jp-font="xlarge"] {{ font-size: 20.8px; }}
    html, body {{ max-width: 100%; overflow-x: hidden; overflow-wrap: break-word; }}
    body {{
      background: var(--bg-page);
      color: var(--text-main);
      font-family: 'Noto Sans JP', -apple-system, BlinkMacSystemFont, sans-serif;
      line-height: 1.75;
      margin: 0;
      padding: 0 0 calc(64px + env(safe-area-inset-bottom, 0px));
      font-feature-settings: "palt" 1;
      letter-spacing: 0.01em;
    }}
    .jp-num {{ font-variant-numeric: tabular-nums; }}
    .comp-table-wrap {{ overflow-x: auto; max-width: 100%; }}
    .container {{ max-width: 1080px; margin: 0 auto; padding: 10px 14px 24px; }}

    .top-nav {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      flex-wrap: wrap;
      gap: 8px;
      border-bottom: 1.5px solid var(--border-col);
      padding-bottom: 10px;
      min-height: 48px;
    }}
    .brand-link {{
      color: var(--text-main);
      font-weight: 900;
      font-size: 1.08rem;
      text-decoration: none;
      display: inline-flex;
      align-items: center;
      gap: 6px;
    }}
    .top-nav-actions {{
      display: flex;
      align-items: center;
      gap: 6px;
      flex-wrap: wrap;
    }}
    .btn-top-main, .btn-top-yt, .btn-top-theme, .btn-top-font {{
      padding: 0 11px;
      border-radius: 8px;
      text-decoration: none;
      font-weight: 800;
      font-size: 0.84rem;
      min-height: 42px;
      display: inline-flex;
      align-items: center;
      justify-content: center;
      white-space: nowrap;
      cursor: pointer;
    }}
    .btn-top-main {{ background: #1d4ed8; color: #ffffff; border: 1px solid #1e40af; }}
    .btn-top-yt {{ background: var(--bg-sub); color: var(--accent-blue); border: 1px solid var(--border-col); }}
    .btn-top-theme {{ background: #17325c; color: #fde68a; border: 1px solid #3b5998; }}
    .btn-top-font {{ background: #ecfdf5; color: #065f46; border: 1.5px solid #10b981; }}
    html[data-jp-theme="dark"] .btn-top-font {{ background: #064e3b; color: #ecfdf5; border-color: #34d399; }}

    .hero-title {{
      margin: 12px 0 8px;
      font-size: clamp(1.52rem, 3vw, 2.15rem);
      color: var(--text-main);
      font-weight: 900;
      line-height: 1.35;
    }}
    .hero-sublead {{
      font-size: 1.08rem;
      color: var(--text-muted);
      font-weight: 700;
      margin: 0 0 14px;
      line-height: 1.72;
    }}

    /* 3-Color Balance Quick Cards */
    .signal-light-section {{
      background: var(--bg-card);
      border: 1.5px solid var(--border-col);
      border-radius: 14px;
      padding: 15px;
      margin-bottom: 18px;
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
      display: flex;
      flex-direction: column;
      gap: 5px;
      min-height: 112px;
    }}
    .signal-light-card.sig-buy {{ border-top: 5px solid #10b981; }}
    .signal-light-card.sig-watch {{ border-top: 5px solid #f59e0b; }}
    .sig-pill {{
      display: inline-flex;
      align-items: center;
      gap: 4px;
      font-size: 0.86rem;
      font-weight: 900;
      padding: 3px 9px;
      border-radius: 999px;
      width: fit-content;
    }}
    .sig-pill-buy {{ background: rgba(16, 185, 129, 0.16); color: var(--accent-emerald); }}
    .sig-pill-watch {{ background: rgba(245, 158, 11, 0.18); color: var(--accent-amber); }}

    /* #gba-retirement-architect-jp */
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
    }}
    .gba-retire-top {{ display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:8px; margin-bottom:10px; }}
    .gba-retire-kicker {{ background:#dcfce7; color:#065f46; border:1.5px solid #059669; border-radius:999px; padding:5px 14px; font-size:0.92rem; font-weight:900; }}
    html[data-jp-theme="dark"] .gba-retire-kicker {{ background:rgba(16,185,129,0.2); color:#6ee7b7; border-color:#34d399; }}
    .gba-retire-subtag {{ background:#fef3c7; color:#92400e; border:1px solid #d97706; border-radius:999px; padding:5px 13px; font-size:0.9rem; font-weight:800; }}
    html[data-jp-theme="dark"] .gba-retire-subtag {{ background:rgba(245,158,11,0.18); color:#fde68a; }}
    .gba-retire-heading {{ font-size:clamp(1.32rem, 2.2vw, 1.65rem); font-weight:900; color:var(--text-main); margin:4px 0 8px; line-height:1.38; }}
    .gba-retire-lead {{ font-size:1.06rem; line-height:1.74; color:var(--text-muted); margin:0 0 16px; }}
    .gba-retire-presets {{ display:grid; grid-template-columns:repeat(3, minmax(0, 1fr)); gap:12px; margin-bottom:18px; }}
    .gba-retire-pgroup {{ background:var(--bg-card); border:1.5px solid var(--border-col); border-radius:12px; padding:13px; }}
    .gba-retire-plabel {{ display:block; font-size:0.98rem; font-weight:900; color:var(--text-main); margin-bottom:9px; }}
    .gba-retire-pgrid {{ display:grid; grid-template-columns:repeat(2, minmax(0, 1fr)); gap:8px; }}
    .gba-retire-pbtn {{ min-height:48px; padding:8px; border-radius:10px; border:1.5px solid var(--border-col); background:var(--bg-page); color:var(--text-main); font-size:0.98rem; font-weight:800; cursor:pointer; }}
    .gba-retire-pbtn.is-active {{ background:linear-gradient(135deg, #059669, #047857); border-color:#10b981; color:#ffffff !important; }}
    .gba-retire-res-grid {{ display:grid; grid-template-columns:repeat(2, minmax(0, 1fr)); gap:15px; margin-bottom:16px; }}
    .gba-retire-rcard {{ background:var(--bg-card); border:1.5px solid var(--border-col); border-radius:14px; padding:16px; display:flex; flex-direction:column; gap:11px; }}
    .gba-retire-rkicker {{ font-size:0.94rem; font-weight:900; color:var(--accent-blue); }}
    .gba-retire-proj {{ font-size:1.06rem; color:var(--text-main); }}
    .gba-retire-proj strong {{ font-size:1.3rem; color:var(--accent-emerald); }}
    .gba-retire-cgrid {{ display:grid; grid-template-columns:repeat(2, minmax(0, 1fr)); gap:10px; }}
    .gba-retire-cbox {{ border-radius:12px; padding:12px; border:1.5px solid var(--border-col); }}
    .gba-retire-cbox.is-safe {{ background:rgba(16, 185, 129, 0.1); border-color:#059669; }}
    .gba-retire-cbox.is-crash {{ background:rgba(239, 68, 68, 0.08); border-color:rgba(239, 68, 68, 0.5); }}
    .gba-retire-ctag {{ display:block; font-size:0.92rem; font-weight:900; color:var(--text-main); margin-bottom:5px; }}
    .gba-retire-cnum {{ font-size:clamp(1.45rem, 2.2vw, 1.9rem); font-weight:900; color:#047857; line-height:1.2; margin-bottom:5px; }}
    html[data-jp-theme="dark"] .gba-retire-cnum {{ color:#34d399; }}
    .gba-retire-cnum.is-muted {{ color:#b91c1c; }}
    html[data-jp-theme="dark"] .gba-retire-cnum.is-muted {{ color:#fca5a5; }}
    .gba-retire-csub {{ font-size:0.94rem; line-height:1.58; color:var(--text-muted); }}
    .gba-retire-callout {{ background:rgba(16,185,129,0.14); border:1.5px solid #059669; border-radius:10px; padding:11px 13px; font-size:1rem; line-height:1.65; }}
    .gba-retire-taxbox {{ background:rgba(37,99,235,0.09); border:1.5px solid rgba(37,99,235,0.42); border-radius:10px; padding:11px 13px; font-size:0.98rem; line-height:1.62; }}
    .gba-retire-wtabs {{ display:grid; grid-template-columns:repeat(3, minmax(0, 1fr)); gap:8px; }}
    .gba-retire-wtab {{ min-height:46px; padding:7px 8px; border-radius:9px; border:1.5px solid var(--border-col); background:var(--bg-page); color:var(--text-main); font-size:0.92rem; font-weight:800; cursor:pointer; }}
    .gba-retire-wtab.is-active {{ background:#1d4ed8; border-color:#2563eb; color:#ffffff !important; }}
    .gba-retire-wdesc {{ font-size:0.98rem; line-height:1.62; color:var(--text-muted); }}
    .gba-wallet-list {{ display:flex; flex-direction:column; gap:10px; }}
    .gba-wallet-item {{ background:var(--bg-page); border:1px solid var(--border-col); border-radius:10px; padding:10px 12px; }}
    .gba-wallet-head {{ display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:6px; font-size:0.98rem; font-weight:800; margin-bottom:5px; }}
    .gba-wallet-stat {{ font-weight:900; color:var(--accent-emerald); }}
    .gba-wallet-bar {{ height:9px; border-radius:999px; background:rgba(148,163,184,0.28); overflow:hidden; margin-bottom:5px; }}
    .gba-wallet-bar span {{ display:block; height:100%; border-radius:999px; }}
    .gba-wallet-item.w1 .gba-wallet-bar span {{ background:#0284c7; }}
    .gba-wallet-item.w2 .gba-wallet-bar span {{ background:#059669; }}
    .gba-wallet-item.w3 .gba-wallet-bar span {{ background:#d97706; }}
    .gba-wallet-note {{ font-size:0.93rem; line-height:1.56; color:var(--text-muted); }}

    .gba-nisa-core-strip {{ background:var(--bg-card); border:2px solid #1d4ed8; border-radius:13px; padding:15px; margin-bottom:15px; }}
    .gba-nisa-core-title {{ font-size:1.02rem; line-height:1.68; color:var(--text-main); margin-bottom:10px; }}
    .gba-nisa-core-grid {{ display:grid; grid-template-columns:repeat(4, minmax(0, 1fr)); gap:10px; }}
    .gba-nisa-core-card {{ background:var(--bg-page); border:1px solid var(--border-col); border-radius:10px; padding:11px; display:flex; flex-direction:column; gap:4px; }}
    .gba-nisa-core-badge {{ font-size:0.88rem; font-weight:900; color:var(--accent-blue); }}
    .gba-retire-ladder {{ display:grid; grid-template-columns:repeat(2, minmax(0, 1fr)); gap:10px; }}
    .gba-retire-cta {{ min-height:58px; padding:12px 15px; border-radius:11px; font-size:0.98rem; font-weight:900; cursor:pointer; display:flex; flex-direction:column; align-items:center; justify-content:center; text-align:center; text-decoration:none; line-height:1.38; }}
    .gba-retire-cta.c-manual {{ background:#e0f2fe; border:2px solid #0284c7; color:#075985; }}
    html[data-jp-theme="dark"] .gba-retire-cta.c-manual {{ background:rgba(14,165,233,0.18); border-color:#38bdf8; color:#e0f2fe; }}
    .gba-retire-cta.c-club {{ background:linear-gradient(135deg, #059669, #047857); border:none; color:#ffffff !important; }}
    .gba-retire-cta.c-pro {{ background:#1d4ed8; border:none; color:#ffffff !important; }}
    .gba-retire-cta.c-vip {{ background:linear-gradient(135deg, #d97706, #b45309); border:none; color:#ffffff !important; }}
    .gba-retire-cta small {{ font-size:0.86rem; font-weight:800; opacity:0.95; margin-top:2px; }}

    /* Unified Morning Club & Passwordless Signup (#gbaMorningClubJp + #gba-jp-passwordless-signup) */
    .gba-morning-club {{
      background: linear-gradient(135deg, #fffbeb 0%, #f8fafc 100%);
      border: 2px solid #d97706;
      border-radius: 14px;
      padding: 18px 16px;
      margin-bottom: 18px;
    }}
    html[data-jp-theme="dark"] .gba-morning-club {{
      background: linear-gradient(135deg, rgba(30,27,75,0.92), rgba(15,23,42,0.95));
      border-color: rgba(251,191,36,0.55);
    }}
    .gba-club-header {{ display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:8px; margin-bottom:10px; }}
    .gba-club-title-group {{ display:flex; align-items:center; flex-wrap:wrap; gap:8px; }}
    .gba-club-badge {{ background:#fef3c7; color:#92400e; border:1.5px solid #d97706; font-size:0.88rem; font-weight:900; padding:3px 10px; border-radius:999px; }}
    html[data-jp-theme="dark"] .gba-club-badge {{ background:rgba(245,158,11,0.18); color:#fde68a; }}
    .gba-club-title {{ font-size:1.02rem; font-weight:900; }}
    .gba-club-streak {{ background:#ecfdf5; color:#065f46; border:1.5px solid #059669; font-size:0.86rem; font-weight:900; padding:4px 11px; border-radius:999px; }}
    html[data-jp-theme="dark"] .gba-club-streak {{ background:rgba(16,185,129,0.18); color:#6ee7b7; }}
    .gba-club-greeting {{ background:var(--bg-card); border:1px solid var(--border-col); border-left:4px solid #d97706; border-radius:10px; padding:11px 13px; margin-bottom:12px; font-weight:700; }}
    .gba-club-poll-header {{ display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:6px; margin-bottom:8px; }}
    .gba-club-poll-grid {{ display:grid; grid-template-columns:repeat(3, minmax(0, 1fr)); gap:10px; }}
    .gba-club-poll-btn {{ min-height:56px; padding:10px 13px; border-radius:11px; border:2px solid var(--border-col); background:var(--bg-card); color:var(--text-main); cursor:pointer; display:flex; flex-direction:column; gap:6px; text-align:left; }}
    .gba-club-poll-btn.is-active {{ border-color:#059669; background:#ecfdf5; }}
    html[data-jp-theme="dark"] .gba-club-poll-btn.is-active {{ border-color:#34d399; background:rgba(16,185,129,0.18); }}
    .gba-poll-row-top {{ display:flex; justify-content:space-between; align-items:center; gap:8px; width:100%; font-weight:900; }}
    .gba-poll-bar-bg {{ display:block; width:100%; height:8px; border-radius:999px; background:rgba(148,163,184,0.25); overflow:hidden; }}
    .gba-poll-bar-fill {{ display:block; height:100%; border-radius:999px; }}
    .gba-poll-bar-fill.fill-dip {{ background:#10b981; }}
    .gba-poll-bar-fill.fill-watch {{ background:#f59e0b; }}
    .gba-poll-bar-fill.fill-cash {{ background:#2563eb; }}
    .gba-club-companion {{ margin-top:10px; padding:10px 12px; border-radius:10px; background:var(--bg-card); border:1.5px dashed var(--border-col); font-weight:800; color:var(--text-muted); }}
    .gba-club-companion.is-voted {{ background:#ecfdf5; border:1.5px solid #059669; color:#065f46; }}

    .gba-jp-pwless-box {{ margin-top:14px; padding:18px 16px; border-radius:12px; background:var(--bg-card); border:2px solid #059669; }}
    .gba-jp-pwless-top {{ display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:8px; margin-bottom:8px; }}
    .gba-jp-pwless-badge {{ background:#059669; color:#ffffff; font-size:0.86rem; font-weight:900; padding:4px 12px; border-radius:999px; }}
    .gba-jp-pwless-heading {{ font-size:1.12rem; font-weight:900; margin:0 0 6px; }}
    .gba-jp-pwless-sub {{ font-size:0.98rem; color:var(--text-muted); margin:0 0 12px; }}
    .gba-jp-seg-grid {{ display:grid; grid-template-columns:repeat(3, minmax(0, 1fr)); gap:8px; margin-bottom:12px; }}
    .gba-jp-seg-btn {{ min-height:48px; padding:8px 10px; border-radius:10px; border:1.8px solid var(--border-col); background:var(--bg-sub); color:var(--text-main); font-size:0.92rem; font-weight:800; cursor:pointer; }}
    .gba-jp-seg-btn.is-active {{ background:#ecfdf5; border-color:#059669; color:#065f46; }}
    html[data-jp-theme="dark"] .gba-jp-seg-btn.is-active {{ background:rgba(16,185,129,0.2); border-color:#34d399; color:#a7f3d0; }}
    .gba-jp-pwless-form {{ display:grid; grid-template-columns:minmax(150px, 0.8fr) minmax(230px, 1.4fr) auto; gap:10px; }}
    .gba-jp-pwless-input {{ min-height:52px; padding:10px 13px; border-radius:10px; border:1.8px solid var(--border-col); background:var(--bg-card); color:var(--text-main); font-size:0.98rem; font-weight:700; width:100%; }}
    .gba-jp-pwless-submit {{ min-height:52px; padding:10px 18px; border-radius:10px; border:none; background:linear-gradient(135deg,#059669,#047857); color:#ffffff; font-size:0.96rem; font-weight:900; cursor:pointer; white-space:nowrap; }}
    .gba-jp-pwless-feedback {{ display:none; margin-top:12px; padding:12px 14px; border-radius:10px; background:#ecfdf5; border:1.5px solid #059669; color:#065f46; font-weight:800; }}
    .gba-jp-pwless-feedback.is-error {{ background:#fff1f2; border-color:#e11d48; color:#9f1239; }}
    .gba-jp-club-manual-cta {{ display:inline-flex; align-items:center; margin-top:8px; min-height:46px; padding:8px 16px; border-radius:10px; background:#059669; color:#ffffff !important; font-weight:900; text-decoration:none; }}

    /* ¥0 Starter Manual Card & Modal */
    .gba-starter-manual {{ background:linear-gradient(135deg, #f0fdf4 0%, #eff6ff 100%); border:2px solid #059669; border-radius:14px; padding:18px; margin-bottom:18px; }}
    html[data-jp-theme="dark"] .gba-starter-manual {{ background:linear-gradient(135deg, rgba(6,78,59,0.34), rgba(15,23,42,0.96)); border-color:#10b981; }}
    .gba-manual-top-row {{ display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:8px; margin-bottom:10px; }}
    .gba-manual-free-badge {{ display:inline-flex; align-items:center; gap:6px; background:#059669; color:#ffffff; font-size:0.9rem; font-weight:900; padding:5px 12px; border-radius:999px; }}
    .gba-manual-sub-badge {{ font-size:0.88rem; font-weight:800; color:#065f46; background:#d1fae5; border:1px solid #6ee7b7; padding:4px 11px; border-radius:999px; }}
    html[data-jp-theme="dark"] .gba-manual-sub-badge {{ background:rgba(16,185,129,0.18); color:#a7f3d0; }}
    .gba-manual-heading {{ font-size:1.22rem; font-weight:900; margin:0 0 8px; line-height:1.45; }}
    .gba-manual-lead {{ font-size:1.04rem; color:var(--text-muted); margin:0 0 14px; }}
    .gba-manual-chap-grid {{ display:grid; grid-template-columns:repeat(3, minmax(0, 1fr)); gap:12px; margin-bottom:14px; }}
    .gba-manual-chap-btn {{ background:var(--bg-card); border:2px solid var(--border-col); border-radius:12px; padding:14px; text-align:left; cursor:pointer; display:flex; flex-direction:column; justify-content:space-between; gap:8px; color:var(--text-main); }}
    .gba-manual-chap-tag {{ font-size:0.84rem; font-weight:900; color:#047857; background:#ecfdf5; border:1px solid #a7f3d0; padding:3px 9px; border-radius:999px; width:fit-content; }}
    .gba-manual-chap-title {{ font-size:1.04rem; font-weight:900; }}
    .gba-manual-chap-desc {{ font-size:0.95rem; color:var(--text-muted); }}
    .gba-manual-chap-more {{ font-size:0.92rem; font-weight:900; color:var(--accent-blue); }}
    .gba-manual-cta-row {{ display:flex; flex-wrap:wrap; gap:10px; margin-bottom:12px; }}
    .gba-manual-open-btn {{ background:linear-gradient(135deg,#059669,#047857); color:#ffffff; border:none; border-radius:12px; padding:13px 18px; min-height:54px; font-size:1.04rem; font-weight:900; cursor:pointer; flex:1 1 300px; }}
    .gba-manual-signal-btn {{ background:var(--bg-card); color:var(--text-main); border:2px solid var(--accent-blue); border-radius:12px; padding:12px 16px; min-height:54px; font-size:1rem; font-weight:900; cursor:pointer; flex:1 1 260px; }}
    .gba-manual-funnel-strip {{ display:flex; flex-wrap:wrap; align-items:center; justify-content:space-between; gap:10px; padding-top:10px; border-top:1px dashed var(--border-col); font-size:0.95rem; color:var(--text-muted); }}
    .gba-manual-funnel-links {{ display:flex; flex-wrap:wrap; gap:10px; }}
    .gba-manual-pro-link, .gba-manual-vip-link {{ display:inline-flex; align-items:center; min-height:44px; padding:6px 13px; border-radius:999px; font-size:0.92rem; font-weight:900; text-decoration:none; border:1.5px solid var(--accent-blue); color:var(--accent-blue); }}
    .gba-manual-vip-link {{ border-color:var(--accent-amber); color:var(--accent-amber); }}

    .gba-manual-modal-backdrop {{ display:none; position:fixed; inset:0; z-index:9999; background:rgba(15,23,42,0.76); backdrop-filter:blur(4px); padding:18px 12px; overflow-y:auto; align-items:flex-start; justify-content:center; }}
    .gba-manual-modal-backdrop.is-open {{ display:flex; }}
    .gba-manual-modal-dialog {{ background:var(--bg-card); color:var(--text-main); border:2px solid #059669; border-radius:16px; width:100%; max-width:860px; margin:8px auto 32px; box-shadow:0 22px 50px rgba(0,0,0,0.45); overflow:hidden; }}
    .gba-manual-modal-header {{ position:sticky; top:0; z-index:5; background:var(--bg-card); border-bottom:2px solid var(--border-col); padding:14px 18px; display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:10px; }}
    .gba-manual-modal-title {{ font-size:1.18rem; font-weight:900; margin:4px 0 0; }}
    .gba-manual-modal-actions {{ display:flex; gap:8px; flex-wrap:wrap; }}
    .gba-manual-action-btn {{ min-height:46px; padding:8px 14px; border-radius:10px; font-size:0.96rem; font-weight:900; cursor:pointer; border:2px solid var(--border-col); background:var(--bg-sub); color:var(--text-main); }}
    .gba-manual-action-btn.btn-print {{ border-color:#059669; background:#ecfdf5; color:#065f46; }}
    .gba-manual-nav-pills {{ display:flex; flex-wrap:wrap; gap:8px; padding:12px 18px; background:var(--bg-sub); border-bottom:1px solid var(--border-col); }}
    .gba-manual-jump-pill {{ min-height:44px; padding:7px 13px; border-radius:999px; border:1.5px solid var(--border-col); background:var(--bg-card); color:var(--text-main); font-size:0.94rem; font-weight:800; cursor:pointer; }}
    .gba-manual-modal-body {{ padding:20px; font-size:1.05rem; line-height:1.8; }}
    .gba-manual-chapter-box {{ background:var(--bg-sub); border:1.5px solid var(--border-col); border-radius:14px; padding:18px; margin-bottom:16px; }}
    .gba-manual-broker-grid {{ display:grid; grid-template-columns:repeat(2, minmax(0, 1fr)); gap:12px; margin-top:10px; }}
    .gba-manual-broker-card {{ background:var(--bg-card); border:1.5px solid var(--border-col); border-radius:12px; padding:14px; }}
    .gba-manual-tip-callout {{ margin-top:12px; padding:12px 14px; border-radius:10px; background:rgba(16,185,129,0.11); border-left:4px solid #059669; }}
    .gba-manual-modal-funnel {{ background:linear-gradient(135deg, rgba(16,185,129,0.12), rgba(37,99,235,0.10)); border:2px solid #059669; border-radius:14px; padding:18px; margin-top:8px; }}

    /* Quick 1-Sec Allocation Calculator (#jpQuickCalcSection) */
    .calc-card {{ background:var(--bg-card); border:2px solid var(--accent-blue); border-radius:14px; padding:16px; margin-bottom:20px; }}
    .calc-header {{ display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:6px; margin-bottom:10px; }}
    .calc-title {{ font-size:1.02rem; font-weight:900; }}
    .calc-pill-risk {{ background:rgba(16,185,129,0.14); color:var(--accent-emerald); border:1px solid rgba(16,185,129,0.4); font-size:0.86rem; font-weight:800; padding:3px 9px; border-radius:6px; }}
    .calc-fast-inputs {{ display:grid; grid-template-columns:repeat(3, minmax(0, 1fr)); gap:8px; margin-bottom:8px; }}
    .fast-field {{ background:var(--bg-sub); border:1px solid var(--border-col); border-radius:8px; padding:7px 9px; }}
    .fast-field label {{ display:block; font-size:0.8rem; font-weight:800; color:var(--text-sub); margin-bottom:3px; }}
    .fast-field input {{ width:100%; border:1px solid var(--border-col); border-radius:6px; background:var(--bg-card); color:var(--text-main); font-family:monospace; font-size:0.98rem; font-weight:800; padding:6px 8px; min-height:38px; }}
    .tax-calc-bar {{ display:grid; grid-template-columns:1fr 1fr; gap:8px; margin-bottom:8px; }}
    .tax-mode-btn {{ background:var(--bg-sub); border:1.5px solid var(--border-col); color:var(--text-main); border-radius:8px; min-height:46px; font-size:0.94rem; font-weight:800; cursor:pointer; }}
    .tax-mode-btn.active {{ background:#1d4ed8; color:#ffffff; border-color:#1e40af; }}
    .btn-calc-submit {{ width:100%; min-height:52px; background:linear-gradient(135deg,#1d4ed8,#4f46e5); color:#ffffff; border:none; border-radius:10px; font-size:1rem; font-weight:900; cursor:pointer; margin-bottom:10px; }}
    .calc-outputs {{ display:grid; grid-template-columns:repeat(auto-fit, minmax(210px, 1fr)); gap:10px; margin-bottom:10px; }}
    .out-card {{ background:var(--bg-sub); border:1.5px solid var(--border-col); border-radius:10px; padding:11px; }}
    .out-label {{ font-size:0.84rem; font-weight:700; color:var(--text-sub); margin-bottom:3px; }}
    .out-val {{ font-size:1.05rem; font-weight:900; font-family:monospace; }}
    .val-emerald {{ color:var(--accent-emerald); }}
    .val-rose {{ color:var(--accent-rose); }}
    .val-amber {{ color:var(--accent-amber); }}
    .slider-group {{ background:var(--bg-sub); border:1px solid var(--border-col); border-radius:10px; padding:10px; margin-bottom:10px; }}
    .slider-header {{ display:flex; justify-content:space-between; flex-wrap:wrap; font-size:0.9rem; font-weight:700; margin-bottom:4px; }}
    input[type=range] {{ width:100%; height:28px; accent-color:#1d4ed8; cursor:pointer; }}
    .capital-pills, .preset-bar {{ display:flex; gap:6px; flex-wrap:wrap; margin-top:6px; }}
    .cap-btn, .preset-chip {{ background:var(--bg-card); border:1.5px solid var(--border-col); color:var(--text-main); padding:6px 11px; border-radius:8px; font-size:0.9rem; font-weight:800; cursor:pointer; min-height:46px; }}
    .cap-btn.active, .preset-chip.active {{ background:#1d4ed8; color:#ffffff; border-color:#1e40af; }}

    /* Pricing & Defense Card (#pricing) */
    .defense-card {{ background:var(--bg-card); border:2px solid var(--border-col); border-radius:16px; padding:22px 18px; margin-bottom:22px; }}
    .defense-title {{ font-size:1.22rem; font-weight:900; margin-bottom:6px; }}
    .defense-subtitle {{ font-size:0.98rem; color:var(--text-sub); margin-bottom:14px; }}
    .comp-grid {{ display:grid; grid-template-columns:1fr 1fr; gap:12px; margin-bottom:16px; }}
    .box-bad {{ background:rgba(244,63,94,0.08); border:1.5px solid rgba(244,63,94,0.35); border-radius:12px; padding:14px; }}
    .box-bad h4 {{ color:var(--accent-rose); font-size:0.98rem; margin:0 0 6px; font-weight:900; }}
    .box-bad .loss-num {{ font-size:1.35rem; font-weight:900; color:var(--accent-rose); font-family:monospace; }}
    .box-good {{ background:rgba(16,185,129,0.08); border:2px solid rgba(16,185,129,0.45); border-radius:12px; padding:14px; }}
    .box-good h4 {{ color:var(--accent-emerald); font-size:0.98rem; margin:0 0 6px; font-weight:900; }}
    .box-good .gain-num {{ font-size:1.35rem; font-weight:900; color:var(--accent-emerald); font-family:monospace; }}
    .cta-dual-grid {{ display:grid; grid-template-columns:repeat(auto-fit, minmax(260px, 1fr)); gap:12px; }}
    .btn-checkout-primary, .btn-checkout-annual {{
      color:#ffffff !important; text-decoration:none; padding:15px 18px; border-radius:12px; font-size:1.05rem; font-weight:900;
      display:flex; flex-direction:column; gap:4px; align-items:center; justify-content:center; width:100%; text-align:center; min-height:68px;
    }}
    .btn-checkout-primary {{ background:linear-gradient(135deg, #1d4ed8, #1e3a8a); }}
    .btn-checkout-annual {{ background:linear-gradient(135deg, #065f46, #047857); }}
    .cta-subnote {{ font-size:0.92rem; color:var(--text-muted); margin-top:10px; line-height:1.65; text-align:center; }}

    /* VIP Vault (#vip-vault & #jpHubVipVaultBox) */
    .vip-vault-card {{ background:var(--bg-card); border:1.5px solid var(--border-col); border-radius:14px; padding:16px; margin-bottom:22px; }}
    .vip-input-row {{ display:flex; gap:8px; flex-wrap:wrap; margin-top:10px; }}
    .vip-key-input {{ flex:1; min-width:180px; padding:10px 12px; border:1.5px solid var(--border-col); border-radius:8px; font-family:monospace; font-size:0.92rem; color:var(--text-main); background:var(--bg-sub); }}
    .vip-unlock-btn {{ background:#0b1f3a; color:#ffffff; border:1px solid #334155; border-radius:8px; padding:10px 16px; font-weight:800; font-size:0.92rem; cursor:pointer; min-height:46px; }}

    /* Research Grid & FAQ */
    .grid {{ display:grid; grid-template-columns:repeat(auto-fill, minmax(280px, 1fr)); gap:14px; margin-top:14px; }}
    .hub-seo-card {{ display:block; background:var(--bg-card); border:1.5px solid var(--border-col); border-radius:12px; padding:16px; color:var(--text-main); text-decoration:none; }}
    .hub-seo-card:hover {{ border-color:var(--accent-blue); }}
    .hub-seo-meta {{ font-family:monospace; font-size:0.86rem; color:var(--accent-amber); font-weight:800; margin-bottom:4px; }}
    .hub-seo-title {{ font-weight:900; font-size:1rem; margin-bottom:6px; }}
    .hub-seo-focus {{ font-size:0.94rem; color:var(--text-sub); line-height:1.62; }}
    .faq-grid {{ display:grid; grid-template-columns:repeat(auto-fit, minmax(280px, 1fr)); gap:14px; margin-top:12px; }}
    .faq-card {{ background:var(--bg-card); border:1.5px solid var(--border-col); border-radius:12px; padding:16px; }}

    /* Mobile Bottom Quick Bar */
    .jp-mobile-bottom-nav {{ display:none; }}
    @media (max-width: 920px) {{
      .gba-retire-presets, .gba-retire-res-grid, .gba-jp-pwless-form, .gba-manual-chap-grid, .gba-manual-broker-grid {{ grid-template-columns: 1fr; }}
      .gba-nisa-core-grid, .signal-light-grid {{ grid-template-columns: repeat(2, minmax(0, 1fr)); }}
    }}
    @media (max-width: 768px) {{
      .jp-mobile-bottom-nav {{
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        position: fixed;
        bottom: 0;
        left: 0;
        right: 0;
        z-index: 999;
        background: #0b1f3a;
        border-top: 2px solid #f59e0b;
        padding-bottom: env(safe-area-inset-bottom, 0px);
      }}
      .jp-mobile-bottom-nav a {{
        color: #f8fafc;
        text-decoration: none;
        font-size: 0.76rem;
        font-weight: 800;
        text-align: center;
        padding: 10px 4px;
        border-right: 1px solid rgba(255,255,255,0.14);
      }}
      .jp-mobile-bottom-nav a:last-child {{ border-right: none; background: #d97706; color: #ffffff; }}
    }}
    @media (max-width: 640px) {{
      .gba-retire-cgrid, .gba-nisa-core-grid, .gba-retire-wtabs, .gba-retire-ladder, .comp-grid, .gba-club-poll-grid, .gba-jp-seg-grid, .calc-fast-inputs {{ grid-template-columns: 1fr; }}
    }}
    @media print {{
      body.printing-gba-manual > *:not(#gbaStarterManualModal) {{ display: none !important; }}
      body.printing-gba-manual #gbaStarterManualModal {{ display: block !important; position: static !important; background: #ffffff !important; padding: 0 !important; }}
    }}
  </style>
</head>
<body>
  <div class="container">
    <!-- Top Navigation (Strictly /jp/ Unified) -->
    <nav class="top-nav" aria-label="ゆとり老後＆新NISAナビゲーション">
      <a href="/jp/" class="brand-link">⚡ GetBreakAI <span style="font-size:0.84rem; color:var(--accent-emerald); font-weight:800;">ゆとり老後＆新NISA設計ナビ</span></a>
      <div class="top-nav-actions">
        <button type="button" id="btnToggleJpFont" onclick="cycleJpFontSize()" class="btn-top-font" aria-label="文字サイズ切替">🔍 文字: 標準</button>
        <a href="#gba-retirement-architect-jp" class="btn-top-main">🧭 30秒老後試算</a>
        <a href="#pricing" class="btn-top-yt">💎 Pro料金</a>
        <a href="https://www.youtube.com/@GetBreakAI" target="_blank" rel="noopener" class="btn-top-yt">📺 YouTube</a>
        <button type="button" id="btnToggleJpTheme" onclick="toggleJpTheme()" class="btn-top-theme">🌙 切替</button>
      </div>
    </nav>

    <!-- Crisp Intuitive Senior B2C Headline -->
    <h1 class="hero-title">
      年金＋新NISAで『毎月ゆとりある老後収入』を設計し、暴落から資産寿命を守る羅針盤
    </h1>
    <p class="hero-sublead">
      難しい専門用語や忙しい頻繁な取引は不要です。金融庁ルールに完全準拠した<b>{FSA_HYBRID_PHRASE_JP}</b>と個人向け国債を組み合わせ、3色バランス指標（🟢・🟡・🔴）に合わせて<b>年2〜4回ゆったり配分を見直す</b>だけで、非課税枠360万円を守りながら心穏やかな老後キャッシュフローを設計できます。
    </p>

    <!-- 🚦 3-Color Balance Quick Cards -->
    <section class="signal-light-section" id="jpSignalTrafficLightHub" aria-label="本日の老後ハイブリッド資産・3色バランス早見カード">
      <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:8px;">
        <div style="font-weight:900; font-size:1.05rem;">🚦 本日の「新NISA適格コア × 特定口座ハイブリッド」3色バランス早見カード <span style="font-size:0.92rem; color:var(--accent-blue);">（公開市場データ連動）</span></div>
        <a href="#gba-jp-passwordless-signup" style="font-size:0.95rem; font-weight:900; color:var(--accent-emerald); text-decoration:underline;">📧 毎朝8時の無料3色ブリーフ登録 ↓</a>
      </div>
      <div class="signal-light-grid">
        <button type="button" class="signal-light-card sig-buy" onclick="setQuickStock('1489'); document.getElementById('jpQuickCalcSection').scrollIntoView({{behavior:'smooth'}});">
          <span class="sig-pill sig-pill-buy">🟢 新NISA適格（1・4・7・10月）</span>
          <strong style="font-size:1.02rem; color:var(--text-main);">1489 日経高配当株50 ETF</strong>
          <span style="font-size:0.92rem; color:var(--text-muted);">日本優良50社・新NISA成長投資枠で非課税配当</span>
        </button>
        <button type="button" class="signal-light-card sig-buy" onclick="setQuickStock('VYM'); document.getElementById('jpQuickCalcSection').scrollIntoView({{behavior:'smooth'}});">
          <span class="sig-pill sig-pill-buy">🟢 新NISA適格（3・6・9・12月）</span>
          <strong style="font-size:1.02rem; color:var(--text-main);">VYM・HDV 米国高配当株ETF</strong>
          <span style="font-size:0.92rem; color:var(--text-muted);">1489と時間差組み合わせで年間配当を平準化</span>
        </button>
        <button type="button" class="signal-light-card sig-buy" onclick="document.getElementById('gba-retirement-architect-jp').scrollIntoView({{behavior:'smooth'}});">
          <span class="sig-pill sig-pill-buy">🟢 新NISA適格（長期成長枠）</span>
          <strong style="font-size:1.02rem; color:var(--text-main);">オルカン ＆ 米国株式（S&amp;P500）</strong>
          <span style="font-size:0.92rem; color:var(--text-muted);">物価上昇（インフレ）から老後資産の実質価値を保護</span>
        </button>
        <button type="button" class="signal-light-card sig-watch" onclick="document.getElementById('gbaSeniorCoreStripJp').scrollIntoView({{behavior:'smooth'}});">
          <span class="sig-pill sig-pill-watch">🛡️ 国債 ＋ 特定口座（SGOV・JEPI）</span>
          <strong style="font-size:1.02rem; color:var(--text-main);">個人向け国債 ＆ 特定口座毎月分配</strong>
          <span style="font-size:0.92rem; color:var(--text-muted);">※毎月分配型（SGOV・JEPI）は特定口座で区分管理</span>
        </button>
      </div>
    </section>

    <!-- 🧭 30秒・ゆとり老後＆新NISA毎月キャッシュフロー設計シミュレーター (#gba-retirement-architect-jp) -->
    <section class="gba-retire-arch" id="gba-retirement-architect-jp" aria-label="30秒・ゆとり老後＆新NISA毎月キャッシュフロー設計シミュレーター">
      <div class="gba-retire-top">
        <span class="gba-retire-kicker">🧭 無料公開・登録不要｜30秒 ゆとり老後設計ナビ</span>
        <span class="gba-retire-subtag">🏛️ 金融庁ルール準拠：新NISA適格 × 特定口座ハイブリッド対応</span>
      </div>
      <h2 class="gba-retire-heading">
        30秒・ゆとり老後＆新NISA「毎月キャッシュフロー」設計シミュレーター
      </h2>
      <p class="gba-retire-lead">
        下の3つの条件をタップするだけで、<b>公的年金に毎月プラスできる「ゆとり老後収入」</b>、暴落・塩漬け回避で守られる毎月差額、および3色バランス指標に連動した<b>「老後3つの財布」最適配分</b>がその場で試算されます。
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
        <div class="gba-retire-rcard">
          <div class="gba-retire-rkicker">計算結果 ① · 年金に毎月プラスできる「ゆとり老後キャッシュフロー」</div>
          <div class="gba-retire-proj">
            受取開始時の想定老後資産：<strong id="gbaRetireProjMan">約2,318万円</strong>
          </div>
          <div class="gba-retire-cgrid">
            <div class="gba-retire-cbox is-safe">
              <span class="gba-retire-ctag">🛡️ 3つの財布・年2〜4回配分ルート</span>
              <div class="gba-retire-cnum" id="gbaRetireSafeMo">月 +8.7万円</div>
              <div class="gba-retire-csub" id="gbaRetireSafeSub">年間 約104.3万円（年4.5%配当＆計画取り崩し）· <b>資産寿命 32年以上</b></div>
            </div>
            <div class="gba-retire-cbox is-crash">
              <span class="gba-retire-ctag">⚠️ 1銘柄集中・暴落塩漬けルート（-35%下落時）</span>
              <div class="gba-retire-cnum is-muted" id="gbaRetireCrashMo">月 +4.8万円</div>
              <div class="gba-retire-csub" id="gbaRetireCrashSub">退職前後の下落で資産約1,507万円へ縮小 · <b>約19年で枯渇懸念</b></div>
            </div>
          </div>
          <div class="gba-retire-callout" id="gbaRetireGapBanner">
            ✅ 分散配分点検で <strong>毎月 +3.9万円（年間 +47.0万円）のゆとり収入</strong> を守り、資産寿命を <strong>+13年以上延長</strong> する試算です。
          </div>
          <div class="gba-retire-taxbox" id="gbaRetireTaxBanner">
            🌱 <strong>新NISA 20.315% 非課税節税メリット：</strong>特定口座と比べ <strong>年間 約2.1万円 ／ 20年累計 約148万円</strong> の税金が手元に残ります。
          </div>
        </div>

        <div class="gba-retire-rcard">
          <div class="gba-retire-rkicker">計算結果 ② · 公開市場データ連動「老後3つの財布」最適配分ガイド</div>
          <div class="gba-retire-wtabs" role="group" aria-label="相場天気モード切替">
            <button type="button" class="gba-retire-wtab" data-gba-wmode="green" aria-pressed="false" onclick="setGbaRetireWeather('green', this)">🟢 安定環境</button>
            <button type="button" class="gba-retire-wtab is-active" data-gba-wmode="yellow" aria-pressed="true" onclick="setGbaRetireWeather('yellow', this)">🟡 標準・配当重視</button>
            <button type="button" class="gba-retire-wtab" data-gba-wmode="red" aria-pressed="false" onclick="setGbaRetireWeather('red', this)">🔴 国債・現金防衛</button>
          </div>
          <div class="gba-retire-wdesc" id="gbaRetireWeatherDesc">
            🟡 本日は「標準・配当重視バランス」：新NISA年間360万円枠を大切に温存しながら、国債クッション30%と高配当40%で穏やかに受け取る配分です。
          </div>
          <div class="gba-wallet-list">
            <div class="gba-wallet-item w1">
              <div class="gba-wallet-head">
                <span>① 守りの財布（個人向け国債 変動10年・待機預金 ／ 特定口座 SGOV）</span>
                <span class="gba-wallet-stat" id="gbaWallet1Stat">30% · 約695万円</span>
              </div>
              <div class="gba-wallet-bar"><span id="gbaWallet1Bar" style="width:30%;"></span></div>
              <div class="gba-wallet-note">生活費2〜3年分を安全確保（※毎月分配の米国短期国債ETF SGOVは特定口座で区分管理）。</div>
            </div>
            <div class="gba-wallet-item w2">
              <div class="gba-wallet-head">
                <span>② 収入の財布（新NISA：1489・VYM・HDV ＋ 特定口座：JEPI）</span>
                <span class="gba-wallet-stat" id="gbaWallet2Stat">40% · 約927万円</span>
              </div>
              <div class="gba-wallet-bar"><span id="gbaWallet2Bar" style="width:40%;"></span></div>
              <div class="gba-wallet-note">新NISA適格の四半期配当（1・4・7・10月 1489 × 3・6・9・12月 VYM/HDV）に特定口座の毎月分配JEPIをハイブリッド補完。</div>
            </div>
            <div class="gba-wallet-item w3">
              <div class="gba-wallet-head">
                <span>③ 成長の財布（新NISA適格：オルカン・S&amp;P500）</span>
                <span class="gba-wallet-stat" id="gbaWallet3Stat">30% · 約695万円</span>
              </div>
              <div class="gba-wallet-bar"><span id="gbaWallet3Bar" style="width:30%;"></span></div>
              <div class="gba-wallet-note">インフレに負けない長期成長枠。年2〜4回だけ穏やかに比率を点検します。</div>
            </div>
          </div>
        </div>
      </div>

      <!-- 🏛️ Mandatory Japanese FSA (金融庁) Shin-NISA Hybrid Compliance Strip -->
      <div class="gba-nisa-core-strip" id="gbaSeniorCoreStripJp">
        <div class="gba-nisa-core-title">
          🏛️ <strong>【金融庁・新NISA規定 100%準拠】{FSA_HYBRID_PHRASE_JP}</strong><br>
          日本の金融庁規定により、<strong>毎月分配型ETF（JEPI・JEPQ・QYLD・SGOV等）およびレバレッジ型ETF（SOXL・TQQQ等）は新NISAの対象外</strong>です。当ソフトウェアでは、新NISA非課税枠と特定口座を法規通り正確に区分したハイブリッド設計を採用しています：
        </div>
        <div class="gba-nisa-core-grid">
          <div class="gba-nisa-core-card">
            <span class="gba-nisa-core-badge">🌱 新NISA適格 ①（国内高配当）</span>
            <strong>1489（日経高配当株50 ETF）</strong>
            <span>1・4・7・10月決算。新NISA成長投資枠で国内優良50社の分配金を非課税受取。</span>
          </div>
          <div class="gba-nisa-core-card">
            <span class="gba-nisa-core-badge">🌱 新NISA適格 ②（米国四半期増配）</span>
            <strong>VYM ・ HDV（米国高配当株ETF）</strong>
            <span>3・6・9・12月分配。1489と時間差で組み合わせることで新NISA枠内の配当受取月を分散。</span>
          </div>
          <div class="gba-nisa-core-card">
            <span class="gba-nisa-core-badge">🌱 新NISA適格 ③（長期インデックス）</span>
            <strong>オルカン ・ S&amp;P500</strong>
            <span>つみたて投資枠・成長投資枠100%適格。超低コストでインフレ対策の柱を構築。</span>
          </div>
          <div class="gba-nisa-core-card">
            <span class="gba-nisa-core-badge">🏦 国債 ＋ 特定口座（毎月分配補完）</span>
            <strong>個人向け国債 ／ 特定口座 SGOV・JEPI</strong>
            <span>毎月分配型のSGOV・JEPIは新NISA対象外のため、必ず特定口座（源泉徴収あり）で区分保有。</span>
          </div>
        </div>
      </div>

      <!-- 3-Step Value Ladder CTA Bar -->
      <div class="gba-retire-ladder">
        <button type="button" class="gba-retire-cta c-manual" onclick="var el=document.getElementById('gbaFreeStarterManualJp'); if(el&&el.scrollIntoView){{el.scrollIntoView({{behavior:'smooth',block:'start'}});}}">
          <span>📘 Step 1（¥0 無料）：楽天・SBI証券＆新NISAハイブリッド設定マニュアル</span>
          <small>登録不要・今すぐ全3章を読めます（画面閲覧・メール保存対応）</small>
        </button>
        <button type="button" class="gba-retire-cta c-club" onclick="jumpGbaRetireToClubJp()">
          <span>🍵 Step 2（3秒無料登録）：朝のゆとり老後＆日米マクロ倶楽部</span>
          <small>パスワード不要・毎朝8時に3色バランス指標ブリーフをお届け</small>
        </button>
        <a href="{LS_MONTHLY_URL_HTML}" data-gba-paid-plan="monthly" data-ls-product-uuid="{LS_MONTHLY_UUID}" class="gba-retire-cta c-pro lemonsqueezy-button">
          <span>⚡ Step 3：{PRICE_LABEL_MONTHLY_JP}</span>
          <small>いつでも1クリック解約OK・14日間返金保証・全データ計算機能</small>
        </a>
        <a href="{LS_ANNUAL_URL_HTML}" data-gba-paid-plan="annual" data-ls-product-uuid="{LS_ANNUAL_UUID}" class="gba-retire-cta c-vip lemonsqueezy-button">
          <span>👑 年間Pro VIP：{PRICE_LABEL_ANNUAL_JP}</span>
          <small>43%OFF 一番人気・月あたり約2,500円・14日間返金保証</small>
        </a>
      </div>
    </section>

    <!-- 🍵 Unified Single Email Club Card (#gbaMorningClubRoot > #gbaMorningClubJp > #gba-jp-passwordless-signup) -->
    <div id="gbaMorningClubRoot">
      <section class="gba-morning-club" id="gbaMorningClubJp" aria-label="朝のゆとり老後＆資産守り倶楽部">
        <div class="gba-club-header">
          <div class="gba-club-title-group">
            <span class="gba-club-badge">🍵 朝のゆとり老後＆資産守り倶楽部</span>
            <strong class="gba-club-title">年金＋新NISA・老後資金をご一緒に守る朝の習慣</strong>
          </div>
          <span class="gba-club-streak" id="gbaJpClubStreakBadge">🏅 倶楽部会員・連続訪問 1日目</span>
        </div>

        <div class="gba-club-greeting">
          <span style="color:var(--accent-amber); font-weight:900; margin-right:6px;">編集部の今朝のご挨拶：</span>
          <span id="gbaJpClubGreetingText">「おはようございます。大切な新NISAと老後資金は、焦らず年2〜4回の穏やかなペースで育てていきましょう。」</span>
        </div>

        <div class="gba-club-poll-header">
          <span style="font-weight:900;">🗳️ 本日の個人投資家スタンス集計（1タップ・登録不要）</span>
          <span style="font-size:0.88rem; font-weight:800; color:var(--text-sub);" id="gbaJpClubPollTotal">本日 482名の個人投資家が参加中</span>
        </div>

        <div class="gba-club-poll-grid" role="group" aria-label="本日の個人投資家アンケート">
          <button type="button" class="gba-club-poll-btn" data-gba-poll="buy_dip" aria-pressed="false" onclick="voteGbaMorningClubJp('buy_dip')">
            <span class="gba-poll-row-top">
              <span>🟢 新NISA積立・配当継続</span>
              <strong data-gba-pct="buy_dip">34%</strong>
            </span>
            <span class="gba-poll-bar-bg"><span class="gba-poll-bar-fill fill-dip" data-gba-bar="buy_dip" style="width:34%;"></span></span>
          </button>
          <button type="button" class="gba-club-poll-btn" data-gba-poll="watch" aria-pressed="false" onclick="voteGbaMorningClubJp('watch')">
            <span class="gba-poll-row-top">
              <span>🟡 現状配分を穏やかに維持</span>
              <strong data-gba-pct="watch">41%</strong>
            </span>
            <span class="gba-poll-bar-bg"><span class="gba-poll-bar-fill fill-watch" data-gba-bar="watch" style="width:41%;"></span></span>
          </button>
          <button type="button" class="gba-club-poll-btn" data-gba-poll="cash" aria-pressed="false" onclick="voteGbaMorningClubJp('cash')">
            <span class="gba-poll-row-top">
              <span>🛡️ 国債・待機資金を重視</span>
              <strong data-gba-pct="cash">25%</strong>
            </span>
            <span class="gba-poll-bar-bg"><span class="gba-poll-bar-fill fill-cash" data-gba-bar="cash" style="width:25%;"></span></span>
          </button>
        </div>

        <div class="gba-club-companion" id="gbaJpClubCompanionMsg" role="status" aria-live="polite">
          今朝のスタンスを1タップでお選びいただくと、全国の倶楽部会員の皆さまの集計結果が表示されます。
        </div>

        <!-- Unified Single Passwordless 3-Sec Club Signup Box (#gba-jp-passwordless-signup) -->
        <div class="gba-jp-pwless-box" id="gba-jp-passwordless-signup">
          <div class="gba-jp-pwless-top">
            <span class="gba-jp-pwless-badge">📧 無料正会員・パスワード不要（3秒完了）</span>
            <span style="font-size:0.86rem; font-weight:800; color:var(--text-muted);">毎朝8:00配信 ・ クレジットカード不要 ・ いつでも1クリック配信停止</span>
          </div>
          <h3 class="gba-jp-pwless-heading">毎朝8時の「ゆとり老後・新NISA×特定口座 3色バランス指標ブリーフ」を無料メールでお届け</h3>
          <p class="gba-jp-pwless-sub">パスワード登録は一切不要です。ご関心テーマを選んでメールアドレスを入力するだけで、本日の無料ブリーフが即時表示され、毎朝の金利・為替・配当資産データがメールで届きます。</p>

          <div class="gba-jp-seg-grid" role="group" aria-label="関心テーマ選択">
            <button type="button" class="gba-jp-seg-btn is-active" data-gba-seg="nisa_wealth_defense" aria-pressed="true" onclick="selectGbaJpClubSegment('nisa_wealth_defense')">
              🌱 新NISA・老後資金の保全設計
            </button>
            <button type="button" class="gba-jp-seg-btn" data-gba-seg="jp_us_macro_fx" aria-pressed="false" onclick="selectGbaJpClubSegment('jp_us_macro_fx')">
              💱 日米マクロ金利・ドル円為替統計
            </button>
            <button type="button" class="gba-jp-seg-btn" data-gba-seg="semis_high_dividend" aria-pressed="false" onclick="selectGbaJpClubSegment('semis_high_dividend')">
              💴 日米高配当ETF（1489・VYM・HDV）
            </button>
          </div>

          <form class="gba-jp-pwless-form" id="gba-jp-club-form" onsubmit="return submitGbaJpPasswordlessClub(event)">
            <label for="gba-jp-club-nickname" style="position:absolute; width:1px; height:1px; overflow:hidden; clip:rect(0,0,0,0);">ニックネーム（任意）</label>
            <input type="text" id="gba-jp-club-nickname" class="gba-jp-pwless-input" autocomplete="nickname" maxlength="40" placeholder="ニックネーム（任意）">
            <label for="gba-jp-club-email" style="position:absolute; width:1px; height:1px; overflow:hidden; clip:rect(0,0,0,0);">メールアドレス</label>
            <input type="email" id="gba-jp-club-email" class="gba-jp-pwless-input" required autocomplete="email" placeholder="メールアドレスを入力（例: taro@example.jp）">
            <input type="text" id="gba-jp-club-hp" name="website_hp" tabindex="-1" autocomplete="off" aria-hidden="true" style="display:none">
            <button type="submit" id="gba-jp-club-submit" class="gba-jp-pwless-submit">
              📩 無料で朝の資産守り倶楽部に参加する（3秒完了） →
            </button>
          </form>

          <div class="gba-jp-pwless-feedback" id="gba-jp-club-feedback" role="status" aria-live="polite">
            <div id="gba-jp-club-feedback-text"></div>
            <div id="jpFreeMemberBonusBox" style="margin-top:10px; padding:12px 14px; border-radius:9px; background:var(--bg-card); border:1px solid #10b981; color:var(--text-main); font-size:0.95rem; line-height:1.68;">
              <div style="font-weight:900; color:var(--accent-emerald); margin-bottom:4px;">🎁 無料会員限定サマリー：本日の「新NISA適格 × 特定口座ハイブリッド」3つの財布ガイド</div>
              <div>・<b>🛡️ 守りの財布（30%）：</b>個人向け国債（変動10年）・待機預金（＋米ドル待機は特定口座SGOV）</div>
              <div>・<b>💴 収入の財布（40%）：</b>新NISA成長投資枠の1489・VYM・HDV時間差配当（＋毎月分配JEPIは特定口座）</div>
              <div>・<b>🌍 成長の財布（30%）：</b>新NISAオルカン・S&amp;P500を年2〜4回の穏やかな配分点検で長期保有</div>
            </div>
            <a href="#gbaFreeStarterManualJp" class="gba-jp-club-manual-cta" id="gba-jp-club-manual-btn" onclick="openGbaStarterManualModal(); return false;">
              📘 ¥0 無料・楽天／SBI証券 新NISAハイブリッド設定マニュアルを開く →
            </a>
          </div>
        </div>
      </section>
    </div>

    <!-- 📘 ¥0 無料公開商品：はじめての新NISA＆証券アプリ基本マニュアル (#gbaFreeStarterManualJp) -->
    <section class="gba-starter-manual" id="gbaFreeStarterManualJp" aria-label="¥0 無料公開商品：はじめての新NISA＆証券アプリ基本マニュアル">
      <div class="gba-manual-top-row">
        <span class="gba-manual-free-badge">📘 ¥0 無料公開商品（登録不要・全ページ即時公開）</span>
        <span class="gba-manual-sub-badge">🖨️ 印刷・メール保存対応 ／ 楽天証券・SBI証券 対応</span>
      </div>
      <h2 class="gba-manual-heading">
        はじめての新NISA＆証券アプリ基本マニュアル（指値注文・新NISA適格×特定口座ハイブリッド区分・待機資金ガイド）
      </h2>
      <p class="gba-manual-lead">
        「アプリの注文画面でどの区分を選べばよいか迷う…」という50〜70代の皆さまへ。金融庁ルールに準拠した口座の使い分けと落ち着いた基本操作を、専門用語を使わずやさしい日本語でまとめました。
      </p>

      <div class="gba-manual-chap-grid">
        <button type="button" class="gba-manual-chap-btn" onclick="openGbaStarterManualModal('gbaManualChap1')">
          <span class="gba-manual-chap-tag">第1章 · 落ち着いた買い方</span>
          <strong class="gba-manual-chap-title">楽天証券（iSPEED）・SBI証券での「指値注文」手順</strong>
          <span class="gba-manual-chap-desc">寄り付き直後の思わぬ高値約定を防ぎ、納得できる上限価格で落ち着いて注文する基本操作です。</span>
          <span class="gba-manual-chap-more">第1章を詳しく読む →</span>
        </button>

        <button type="button" class="gba-manual-chap-btn" onclick="openGbaStarterManualModal('gbaManualChap2')">
          <span class="gba-manual-chap-tag">第2章 · 金融庁ルール準拠</span>
          <strong class="gba-manual-chap-title">新NISA適格（VYM・HDV・1489）と特定口座（SGOV・JEPI）の区分</strong>
          <span class="gba-manual-chap-desc">毎月分配型ETFが特定口座専用となる理由と、年2〜4回の穏やかな資産配分点検の手順です。</span>
          <span class="gba-manual-chap-more">第2章を詳しく読む →</span>
        </button>

        <button type="button" class="gba-manual-chap-btn" onclick="openGbaStarterManualModal('gbaManualChap3')">
          <span class="gba-manual-chap-tag">第3章 · 守りの待機資金</span>
          <strong class="gba-manual-chap-title">個人向け国債・楽天マネーブリッジ・SBIハイブリッド預金</strong>
          <span class="gba-manual-chap-desc">生活費2〜3年分の安全クッションを元本保護・優遇金利で整える具体的な設定方法です。</span>
          <span class="gba-manual-chap-more">第3章を詳しく読む →</span>
        </button>
      </div>

      <div class="gba-manual-cta-row">
        <button type="button" id="btnOpenGbaStarterManualJp" class="gba-manual-open-btn" onclick="openGbaStarterManualModal()">
          📖 ¥0 基本マニュアル全3章を開く（画面閲覧・メール受取・印刷可）
        </button>
        <button type="button" class="gba-manual-signal-btn" onclick="jumpGbaRetireToClubJp()">
          📧 毎朝8時の無料「3色バランス指標」を受け取る ↑
        </button>
      </div>

      <div class="gba-manual-funnel-strip">
        <span>💡 <strong>Proソフトウェアプラン：</strong>全銘柄の公開財務データ・配当＆資産配分シミュレーター機能</span>
        <div class="gba-manual-funnel-links">
          <a href="{LS_MONTHLY_URL_HTML}" data-gba-paid-plan="monthly" data-ls-product-uuid="{LS_MONTHLY_UUID}" class="gba-manual-pro-link lemonsqueezy-button">⚡ {PRICE_LABEL_MONTHLY_JP}</a>
          <a href="{LS_ANNUAL_URL_HTML}" data-gba-paid-plan="annual" data-ls-product-uuid="{LS_ANNUAL_UUID}" class="gba-manual-vip-link lemonsqueezy-button">👑 {PRICE_LABEL_ANNUAL_JP}</a>
        </div>
      </div>
    </section>

    <!-- ⚡ 1秒 新NISA×特定口座 1銘柄あたり安心配分額シミュレーター (#jpQuickCalcSection) -->
    <div class="calc-card" id="jpQuickCalcSection">
      <div class="calc-header">
        <div class="calc-title">⚡ 1秒 1銘柄あたり分散配分＆新NISA非課税比較シミュレーター (<span id="jpActiveSymBadge">1489 日経高配当50</span>)</div>
        <div class="calc-pill-risk">🛡️ 1銘柄への過度な集中を防ぐ自己判断用計算ツール</div>
      </div>

      <div class="calc-fast-inputs">
        <div class="fast-field">
          <label for="jpCapManInput">ご運用資金総額 (万円)</label>
          <input type="number" id="jpCapManInput" min="10" max="10000" step="10" value="1500" oninput="syncCapFromManInput()">
        </div>
        <div class="fast-field">
          <label for="jpPriceInput">現在基準価格 <span id="lblPriceUnit">(¥)</span></label>
          <input type="number" id="jpPriceInput" min="0.1" step="any" value="2380" oninput="syncPriceAtrInputs()">
        </div>
        <div class="fast-field">
          <label for="jpAtrInput">14日平均変動幅 <span id="lblAtrUnit">(¥)</span></label>
          <input type="number" id="jpAtrInput" min="0.05" step="any" value="48" oninput="syncPriceAtrInputs()">
        </div>
      </div>

      <div class="tax-calc-bar">
        <button type="button" id="btnJpHubTaxNisa" class="tax-mode-btn active" onclick="setJpHubTaxMode('nisa')">🌱 新NISA適格枠 (非課税 0%)</button>
        <button type="button" id="btnJpHubTaxTokutei" class="tax-mode-btn" onclick="setJpHubTaxMode('tokutei')">🏦 特定口座 (税 20.315%・SGOV/JEPI等)</button>
      </div>

      <button type="button" id="btnJpHubCalcNow" class="btn-calc-submit" onclick="recalcJpQuickCalc()">
        🧮 1秒で「1銘柄分散株数目安」と「非課税・特定口座の手取り差額」を試算する
      </button>

      <div class="calc-outputs">
        <div class="out-card">
          <div class="out-label">分散保有株数の目安（1銘柄集中防止）</div>
          <div id="jpOutShares" class="out-val val-amber jp-num">234株 (¥556,920 / 約55.7万円)</div>
        </div>
        <div class="out-card">
          <div class="out-label">🛡️ 年2〜4回配分点検の参考下限値（2.0倍変動幅）</div>
          <div id="jpOutRisk" class="out-val val-rose jp-num">¥2,284 (-¥22,464 / -約2.2万円)</div>
        </div>
        <div class="out-card">
          <div class="out-label" id="jpOutGainLabel">🎯 長期保有参考ライン（新NISA非課税試算）</div>
          <div id="jpOutGain" class="out-val val-emerald jp-num">¥2,620 (+¥56,160 / +約5.6万円)</div>
        </div>
      </div>

      <div class="slider-group">
        <div class="slider-header">
          <span>ご運用資産スライダー（1ドル=150円基準）:</span>
          <strong id="jpCalcAccLbl" style="color:var(--accent-amber);">$100,000 (約1500.0万円)</strong>
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

      <div style="font-size:0.95rem; font-weight:800; color:var(--text-sub); margin-bottom:6px;">
        👇 新NISA適格コアETF（1489・VYM・HDV・VOO）＆ 日米優良大型株 ワンタップ試算切替：
      </div>
      <div class="preset-bar">
        <button type="button" class="preset-chip active" data-ticker="1489" onclick="setQuickStock('1489', this)">1489 日経高配当50 (新NISA)</button>
        <button type="button" class="preset-chip" data-ticker="VYM" onclick="setQuickStock('VYM', this)">$VYM 米国高配当 (新NISA)</button>
        <button type="button" class="preset-chip" data-ticker="HDV" onclick="setQuickStock('HDV', this)">$HDV 財務健全高配当 (新NISA)</button>
        <button type="button" class="preset-chip" data-ticker="VOO" onclick="setQuickStock('VOO', this)">$VOO 米国S&amp;P500 (新NISA)</button>
        <button type="button" class="preset-chip" data-ticker="8306" onclick="setQuickStock('8306', this)">8306.T 三菱UFJ (¥)</button>
        <button type="button" class="preset-chip" data-ticker="8058" onclick="setQuickStock('8058', this)">8058.T 三菱商事 (¥)</button>
        <button type="button" class="preset-chip" data-ticker="7203" onclick="setQuickStock('7203', this)">7203.T トヨタ (¥)</button>
        <button type="button" class="preset-chip" data-ticker="MSFT" onclick="setQuickStock('MSFT', this)">$MSFT マイクロソフト</button>
        <button type="button" class="preset-chip" data-ticker="AAPL" onclick="setQuickStock('AAPL', this)">$AAPL アップル</button>
      </div>
    </div>

    <!-- 💎 Pricing Section (#pricing) + Mandatory FIEA Disclaimer Directly Below -->
    <section class="defense-card" id="pricing" aria-label="Proソフトウェア料金プラン">
      <div class="defense-title">
        💎 公開市場データ可視化・配当＆資産配分計算ソフトウェア Proプラン
      </div>
      <div class="defense-subtitle">
        1銘柄集中や感情的な売買を避け、新NISA適格資産と特定口座ハイブリッド配分をデータで落ち着いて試算する自己判断用計算ソフトウェア（Lemon Squeezy Store #296100）
      </div>

      <div class="comp-grid">
        <div class="box-bad">
          <h4>❌ 自己流の1銘柄集中・口座区分の誤認</h4>
          <div class="loss-num">-¥525万円 相当の資産目減り懸念</div>
          <p style="font-size:0.98rem; color:var(--text-muted); line-height:1.68; margin:6px 0 0;">
            退職金を一度に高変動銘柄へ集中させたり、新NISA非課税枠を頻繁な売買で消費してしまうケース。
          </p>
        </div>

        <div class="box-good">
          <h4>✅ GetBreakAI 老後キャッシュフロー計算Pro</h4>
          <div class="gain-num">毎月 +3.9万円 ゆとり試算設計</div>
          <p style="font-size:0.98rem; color:var(--text-muted); line-height:1.68; margin:6px 0 0;">
            {FSA_HYBRID_PHRASE_JP}と公開SEC財務データ一覧（CSV出力対応）で、年2〜4回の穏やかな配分点検を支援します。
          </p>
        </div>
      </div>

      <div class="cta-container">
        <div class="cta-dual-grid">
          <a href="{LS_MONTHLY_URL_HTML}" data-gba-paid-plan="monthly" data-ls-product-uuid="{LS_MONTHLY_UUID}" class="btn-checkout-primary lemonsqueezy-button">
            <span>⚡ {PRICE_LABEL_MONTHLY_JP}</span>
            <span style="font-size:0.9rem; font-weight:800; opacity:0.96;">いつでも1クリック解約OK ／ 14日間全額返金保証</span>
          </a>
          <a href="{LS_ANNUAL_URL_HTML}" data-gba-paid-plan="annual" data-ls-product-uuid="{LS_ANNUAL_UUID}" class="btn-checkout-annual lemonsqueezy-button">
            <span>👑 {PRICE_LABEL_ANNUAL_JP}</span>
            <span style="font-size:0.9rem; font-weight:800; opacity:0.96;">43%OFF 一番人気（月あたり約2,500円） ／ 14日間全額返金保証</span>
          </a>
        </div>
        <div class="cta-subnote">
          💳 JCB・Visa・Mastercard・Apple Pay・Google Pay対応（カード会社にて自動円換算）｜ いつでも1クリック解約可能<br>
          🏛️ 法人・金融メディア・APIデータ窓口：<a href="mailto:beable9489@gmail.com" style="color:var(--accent-blue); font-weight:800;">beable9489@gmail.com</a>
        </div>
{disclaimer_box}
      </div>
    </section>

    <!-- 🔐 Web VIP Vault (#vip-vault > #jpHubVipVaultBox — Stays 100% Inside /jp/) -->
    <div id="vip-vault">
      <details class="vip-vault-card" id="jpHubVipVaultBox">
        <summary style="cursor:pointer; font-size:1.02rem; font-weight:900; color:var(--text-main);">
          🔑 Web VIP Vault：購入済みライセンスキー認証・機種変更復元はこちら ▾
        </summary>
        <div style="margin-top:10px;">
          <p style="font-size:0.96rem; color:var(--text-muted); margin:6px 0 8px;">
            Lemon Squeezy（Store #296100）決済完了メールに記載されたライセンスキーを入力すると、日米高配当・優良株の公開データ一覧とCSV出力機能がこの画面で解放されます。
          </p>
          <div class="vip-input-row">
            <label for="jpHubLicenseInput" style="position:absolute; width:1px; height:1px; overflow:hidden; clip:rect(0,0,0,0);">ライセンスキー</label>
            <input type="text" id="jpHubLicenseInput" class="vip-key-input" placeholder="ライセンスキーを入力 (XXXX-XXXX-XXXX-XXXX)">
            <button type="button" id="btnJpHubUnlockVip" class="vip-unlock-btn" onclick="unlockJpHubVipVault()">🔑 VIPデータ庫を解放</button>
          </div>
          <div id="jpHubVipStatus" style="font-size:0.96rem; font-weight:800; margin-top:8px; color:var(--accent-emerald);"></div>
          <div id="jpHubVipUnlockedDrawer" style="display:none; margin-top:12px; padding:14px; border-radius:10px; background:var(--bg-sub); border:1.5px solid #059669;">
            <strong style="color:var(--accent-emerald);">👑 VIP公開データ一覧解放済み：</strong>
            新NISA適格コア（1489・VYM・HDV・オルカン・S&amp;P500）＋特定口座補完（SGOV・JEPI）および日米主要企業の米SEC開示・配当利回り・14日平均変動幅データが有効化されています。
          </div>
        </div>
      </details>
    </div>

    <!-- 📚 Featured Senior-Safe Research Articles (#jp-research-hub — 3x Leverage & Options Swing Excluded) -->
    <section id="jp-research-hub" style="border-top:1px solid var(--border-col); padding-top:20px; margin-top:16px;">
      <h2 style="font-size:1.32rem; color:var(--text-main); margin-bottom:6px;">📚 新NISA・日米優良株 公開データ教育リサーチ一覧（{date_str} 更新）</h2>
      <p style="color:var(--text-muted); font-size:1.02rem; line-height:1.7; margin-bottom:14px;">
        米SEC公式決算開示（Form 8-K/10-Q）、連続増配実績、機関投資家の長期保有統計、および金融庁・新NISA口座区分ルールをやさしく解説しています（レバレッジ型・短期オプション記事は除外済み）。
      </p>
      <div class="grid">
        {cards_html}
      </div>
    </section>

    <!-- ❓ Senior Reassurance FAQ (#jp-faq) -->
    <section id="jp-faq" style="border-top:1px solid var(--border-col); padding-top:20px; margin-top:24px;">
      <h2 style="font-size:1.32rem; color:var(--text-main); margin-bottom:6px;">❓ よくあるご質問（新NISA×特定口座・料金・解約・免責について）</h2>
      <div class="faq-grid">
        <div class="faq-card">
          <h3 style="font-size:1.02rem; margin:0 0 6px;">Q1. 毎月分配型のJEPIやSGOV、3倍レバレッジのSOXLは新NISAで買えますか？</h3>
          <p style="font-size:0.95rem; color:var(--text-muted); margin:0;">いいえ。日本の金融庁ルールにより毎月分配型ETF（JEPI・JEPQ・QYLD・SGOV等）およびレバレッジ型（SOXL・TQQQ）は新NISA対象外です。新NISAでは四半期配当の1489・VYM・HDVやオルカン・S&amp;P500を保有し、SGOV・JEPIは特定口座で組み合わせるハイブリッド設計をご活用ください。</p>
        </div>
        <div class="faq-card">
          <h3 style="font-size:1.02rem; margin:0 0 6px;">Q2. 料金表記（{PRICE_LABEL_MONTHLY_JP} ／ {PRICE_LABEL_ANNUAL_JP}）の支払いと解約・返金は簡単ですか？</h3>
          <p style="font-size:0.95rem; color:var(--text-muted); margin:0;">はい。公式決済基盤 Lemon Squeezy（Store #296100）によりJCB・Visa・Mastercard・Apple Payに対応し、いつでも1クリックで解約可能です。また初回購入から14日以内の全額返金保証（窓口: beable9489@gmail.com）を設けています。</p>
        </div>
        <div class="faq-card">
          <h3 style="font-size:1.02rem; margin:0 0 6px;">Q3. 当サイトは投資助言や個別株の売買指示を行うサービスですか？</h3>
          <p style="font-size:0.95rem; color:var(--text-muted); margin:0;">いいえ。当サイトは{SOFTWARE_POSITIONING_JP}であり、すべての利用者に同一の公開市場データと数学的計算式を表示する教育・情報提供ツールです。金融商品取引法上の投資助言・代理業や売買推奨は一切行いません。</p>
        </div>
      </div>
    </section>
  </div>

  <!-- Smartphone Bottom Navigation -->
  <nav class="jp-mobile-bottom-nav" aria-label="モバイルクイックメニュー">
    <a href="#gba-retirement-architect-jp">🧭 老後試算</a>
    <a href="#gba-jp-passwordless-signup">🍵 無料倶楽部</a>
    <a href="#gbaFreeStarterManualJp">📘 ¥0マニュアル</a>
    <a href="#pricing">💎 Pro料金</a>
  </nav>

{footer_html}
{manual_modal}
{waitlist_modal}

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
      'HDV':  {{ price: 118.40, atr: 1.85,  currency: 'USD', label: '$HDV 財務健全高配当ETF' }},
      'VOO':  {{ price: 548.60, atr: 8.40,  currency: 'USD', label: '$VOO 米国S&P500' }},
      'NVDA': {{ price: 186.64, atr: 8.02,  currency: 'USD', label: '$NVDA エヌビディア' }},
      'PLTR': {{ price: 160.38, atr: 9.95,  currency: 'USD', label: '$PLTR パランティア' }},
      'MSFT': {{ price: 448.20, atr: 9.40,  currency: 'USD', label: '$MSFT マイクロソフト' }},
      'AAPL': {{ price: 232.80, atr: 4.90,  currency: 'USD', label: '$AAPL アップル' }},
      '8035': {{ price: 26800.0, atr: 780.0, currency: 'JPY', label: '8035.T 東エレク' }},
      '7203': {{ price: 2780.0, atr: 68.0,  currency: 'JPY', label: '7203.T トヨタ' }},
      '8306': {{ price: 1850.0, atr: 48.0,  currency: 'JPY', label: '8306.T 三菱UFJ' }},
      '8058': {{ price: 2680.0, atr: 64.0,  currency: 'JPY', label: '8058.T 三菱商事' }}
    }};

    const gbaRetireState = {{ asset: 1500, years: 5, monthly: 5, weather: 'yellow' }};
    const GBA_RETIRE_WEATHER_MAP = {{
      green: {{
        weights: [20, 40, 40],
        desc: '🟢 安定環境バランス：生活費2年分の国債クッションを確保しつつ、新NISA適格の四半期配当（1489・VYM・HDV）＋オルカン・S&P500でゆとり収入と長期成長を両立します。'
      }},
      yellow: {{
        weights: [30, 40, 30],
        desc: '🟡 標準・配当重視バランス：新NISA年間360万円枠を大切に温存しながら、国債クッション30%と高配当40%（新NISA 1489/VYM/HDV＋特定口座 JEPI）を受け取る配分です。'
      }},
      red: {{
        weights: [45, 35, 20],
        desc: '🔴 国債・現金防衛バランス：相場変動の大きい局面では、年2〜4回の定期点検で個人向け国債・待機預金（特定口座SGOV含む）を45%へ厚くし資産寿命を守ります。'
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
      if (safeSubEl) safeSubEl.innerHTML = '年間 約' + safeAnnualMan.toFixed(1) + '万円（年4.5%配当＆計画取り崩し）· <b>資産寿命 32年以上</b>';
      const crashMoEl = document.getElementById('gbaRetireCrashMo');
      if (crashMoEl) crashMoEl.innerText = '月 +' + crashMoMan.toFixed(1) + '万円';
      const crashSubEl = document.getElementById('gbaRetireCrashSub');
      if (crashSubEl) crashSubEl.innerHTML = '退職前後の下落で資産約' + crashProjMan.toLocaleString() + '万円へ縮小 · <b>約19年で枯渇懸念</b>';
      const gapEl = document.getElementById('gbaRetireGapBanner');
      if (gapEl) gapEl.innerHTML = '✅ 分散配分点検で <strong>毎月 +' + gapMoMan.toFixed(1) + '万円（年間 +' + gapYrMan.toFixed(1) + '万円）のゆとり収入</strong> を守り、資産寿命を <strong>+13年以上延長</strong> する試算です。';
      const taxEl = document.getElementById('gbaRetireTaxBanner');
      if (taxEl) taxEl.innerHTML = '🌱 <strong>新NISA 20.315% 非課税節税メリット：</strong>特定口座と比べ <strong>年間 約' + annualDivTaxSaved.toFixed(1) + '万円 ／ 20年累計 約' + cum20YrTaxSaved.toLocaleString() + '万円</strong> の税金が手元に残ります。';

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
        const emailInp = document.getElementById('gba-jp-club-email');
        if (emailInp && emailInp.focus) emailInp.focus();
      }}, 380);
    }}

    function jumpFromManualToJpMail() {{
      if (typeof window.closeGbaStarterManualModal === 'function') window.closeGbaStarterManualModal();
      jumpGbaRetireToClubJp();
    }}

    const GBA_CLUB_GREETINGS_JP = [
      '「おはようございます。大切な新NISAと老後資金は、焦らず年2〜4回の穏やかなペースで育てていきましょう。」',
      '「おはようございます。相場が揺れる日こそ、個人向け国債と高配当クッションで心穏やかに見守りましょう。」',
      '「今朝もご訪問ありがとうございます。退職金や老後の備えは、1銘柄に偏らない分散配分が一番の守りになります。」',
      '「おはようございます。周囲のニュースに急かされず、ご自身のライフプランに合う配分を大切にしましょう。」'
    ];
    const GBA_CLUB_COMPANION_JP = {{
      buy_dip: '🟢 落ち着いた長期視点ですね。新NISA適格の四半期配当ETFと積立枠を焦らずコツコツ育てることが将来のゆとりにつながります。',
      watch: '🟡 とても賢明なご判断です。無理に売買せず現在の3つの財布バランスを静かに保つことで、年間360万円の非課税枠を大切に温存できます。',
      cash: '🛡️ 堅実な資産管理ですね。個人向け国債や待機預金をしっかり確保しておけば、どのような市場環境でも安心してお過ごしいただけます。'
    }};

    function getGbaJstDateKey() {{
      return new Date(Date.now() + 9 * 3600 * 1000).toISOString().slice(0, 10);
    }}

    function getGbaDateSeed(dateStr) {{
      let h = 2166136261;
      const s = String(dateStr || '2026-11-16');
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
            if (pl && pl.date === todayKey && GBA_CLUB_COMPANION_JP[pl.choice]) activeChoice = pl.choice;
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
        if (localStorage.getItem(hitFlag) !== '1') {{
          localStorage.setItem(hitFlag, '1');
          fetch('https://abacus.jasoncameron.dev/hit/gba_getbreakai/poll_' + choice + '_' + todayKey, {{ mode: 'cors', keepalive: true }}).catch(function(){{}});
        }}
      }} catch (_) {{}}
    }}

    const GBA_JP_CLUB_SEGMENT_LABELS = {{
      nisa_wealth_defense: '新NISA・老後資金の保全設計',
      jp_us_macro_fx: '日米マクロ金利・ドル円為替統計',
      semis_high_dividend: '日米高配当ETF（1489・VYM・HDV）'
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
      const bonusBox = document.getElementById('jpFreeMemberBonusBox');
      const manualBtn = document.getElementById('gba-jp-club-manual-btn');
      if (!fbBox || !fbTxt) return;
      fbBox.style.display = 'block';
      fbBox.classList.toggle('is-error', Boolean(isError));
      if (isError) {{
        fbTxt.innerText = errText || '⚠️ 正しいメールアドレスを入力してください（例: taro@example.jp）。';
        if (bonusBox) bonusBox.style.display = 'none';
        if (manualBtn) manualBtn.style.display = 'none';
        return;
      }}
      const nick = member && member.nickname ? (member.nickname + '様、') : '';
      const segKey = (member && member.segment && GBA_JP_CLUB_SEGMENT_LABELS[member.segment]) ? member.segment : 'nisa_wealth_defense';
      const segLabel = GBA_JP_CLUB_SEGMENT_LABELS[segKey];
      const mailStr = member && member.email ? ('（' + member.email + '）') : '';
      fbTxt.innerText = '✅ ' + nick + '朝のゆとり老後＆資産守り倶楽部への無料正会員登録が完了いたしました' + mailStr + '。毎朝8時に「' + segLabel + '」重視の公開市場ブリーフをお届けいたします。';
      if (bonusBox) bonusBox.style.display = 'block';
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
        if (emailInp && emailInp.focus) emailInp.focus();
        return false;
      }}

      try {{
        localStorage.setItem('gb_free_member_email', email);
        localStorage.setItem('gba_jp_free_email', email);
        localStorage.setItem('gb_free_member_joined', '1');
      }} catch (_) {{}}

      if (typeof window.trackGbaFreeSignup === 'function') {{
        window.trackGbaFreeSignup(email);
      }}
      if (submitBtn) submitBtn.disabled = true;

      const memberRecord = {{
        div: 'GBA',
        email: email,
        nickname: nickname,
        segment: segment,
        lang: 'ja-JP',
        website_hp: websiteHp,
        notes: 'site=getbreakai.com | club_signup'
      }};
      if (window.DreamCompanyCRM && typeof window.DreamCompanyCRM.registerMember === 'function') {{
        window.DreamCompanyCRM.registerMember(memberRecord)
          .then(function(res) {{
            if (submitBtn) submitBtn.disabled = false;
            if (res && res.ok === false) {{
              renderGbaJpClubFeedback(null, true, '⚠️ 正しいメールアドレスを入力してください（例: taro@example.jp）。');
              return;
            }}
            renderGbaJpClubFeedback(memberRecord, false, '');
          }})
          .catch(function() {{
            if (submitBtn) submitBtn.disabled = false;
            renderGbaJpClubFeedback(memberRecord, false, '');
          }});
      }} else {{
        if (submitBtn) submitBtn.disabled = false;
        renderGbaJpClubFeedback(memberRecord, false, '');
      }}
      return false;
    }}

    function applyJpFontSize(mode) {{
      const m = (mode === 'large' || mode === 'xlarge') ? mode : 'normal';
      document.documentElement.setAttribute('data-jp-font', m);
      try {{ localStorage.setItem('gb_jp_fontsize', m); }} catch (_) {{}}
      const btn = document.getElementById('btnToggleJpFont');
      if (btn) btn.innerText = m === 'xlarge' ? '🔍 文字: 特大' : (m === 'large' ? '🔍 文字: 大' : '🔍 文字: 標準');
    }}

    function cycleJpFontSize() {{
      const cur = document.documentElement.getAttribute('data-jp-font') || 'normal';
      const next = cur === 'normal' ? 'large' : (cur === 'large' ? 'xlarge' : 'normal');
      applyJpFontSize(next);
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
      document.querySelectorAll('.preset-chip').forEach(function(b) {{
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
      const manVal = Math.max(10, parseFloat(manEl ? manEl.value : 1500) || 1500);
      const usdVal = Math.round((manVal * 10000) / FX_RATE);
      const slider = document.getElementById('jpCalcSlider');
      if (slider) slider.value = Math.min(250000, Math.max(5000, usdVal));
      recalcJpQuickCalc(manVal * 10000);
    }}

    function syncManFromSlider() {{
      const slider = document.getElementById('jpCalcSlider');
      const accUsd = parseFloat(slider ? slider.value : 100000) || 100000;
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
      document.querySelectorAll('.cap-btn').forEach(function(b) {{ b.classList.remove('active'); }});
      if (btnEl) btnEl.classList.add('active');
      const slider = document.getElementById('jpCalcSlider');
      if (slider) slider.value = usdVal;
      const manEl = document.getElementById('jpCapManInput');
      if (manEl) manEl.value = Math.round((usdVal * FX_RATE) / 10000);
      recalcJpQuickCalc(usdVal * FX_RATE);
    }}

    function recalcJpQuickCalc(overrideJpyCap) {{
      const manEl = document.getElementById('jpCapManInput');
      const capJpy = overrideJpyCap || ((Math.max(10, parseFloat(manEl ? manEl.value : 1500) || 1500)) * 10000);
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
          ? '🎯 長期保有参考ライン（特定口座・税20.315%控除後試算）'
          : '🎯 長期保有参考ライン（新NISA非課税0%試算）';
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
          const drawer = document.getElementById('jpHubVipUnlockedDrawer');
          if (inp && !inp.value) inp.value = key;
          if (statusEl) statusEl.innerText = '👑 VIPライセンス認証済みです！公開データ一覧が解放されています。';
          if (drawer) drawer.style.display = 'block';
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
          }} catch (_e) {{}}
          syncStoredVipKeysOnHub();
          setTimeout(function() {{
            window.location.href = '/jp/?unlock=1#vip-vault';
          }}, 700);
        }} else {{
          if (statusEl) {{
            statusEl.style.color = 'var(--accent-rose)';
            statusEl.innerText = '❌ ライセンスキーが確認できませんでした。メール記載のキーをご確認のうえ再度お試しください。';
          }}
        }}
      }} catch (_err) {{
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
      setTimeout(function() {{ window.location.href = '/jp/?unlock=1#vip-vault'; }}, 900);
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

    if (!window.__jpHubLsMsgBound) {{
      window.__jpHubLsMsgBound = true;
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
    }}

    window.addEventListener('DOMContentLoaded', function() {{
      try {{
        const savedTheme = localStorage.getItem('gb_jp_theme');
        if (savedTheme === 'dark' || savedTheme === 'light') {{
          document.documentElement.setAttribute('data-jp-theme', savedTheme);
          const btn = document.getElementById('btnToggleJpTheme');
          if (btn) btn.innerText = savedTheme === 'light' ? '🌙 切替' : '☀️ 切替';
        }}
        const savedFont = localStorage.getItem('gb_jp_fontsize');
        if (savedFont) applyJpFontSize(savedFont);
      }} catch (_) {{}}

      syncGbaMorningClubJp();
      syncGbaJpPasswordlessClub();
      recalcGbaRetireJp();
      syncStoredVipKeysOnHub();
      bindJpHubLemonSqueezyOverlay();

      try {{
        const params = new URLSearchParams(window.location.search || '');
        if (params.get('unlock') === '1') {{
          const box = document.getElementById('jpHubVipVaultBox');
          if (box) box.open = true;
        }}
        const qTicker = (params.get('ticker') || '').toUpperCase().replace(/\\.T$/i, '');
        if (qTicker && PRESET_STOCK_MAP[qTicker]) {{
          setQuickStock(qTicker);
        }} else {{
          recalcJpQuickCalc();
        }}
      }} catch (_) {{
        recalcJpQuickCalc();
      }}

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
            if (PRESET_STOCK_MAP[activeSym]) setQuickStock(activeSym);
          }}
        }} catch (_e) {{}}
      }})();
    }});
  </script>
</body>
</html>
"""


def main():
    os.makedirs(JP_DIR, exist_ok=True)
    for crm_asset in ("hq-mailing-endpoint.json", "hq_member_crm_client.js"):
        crm_src = os.path.join(ROOT_DIR, crm_asset)
        if os.path.isfile(crm_src):
            shutil.copyfile(crm_src, os.path.join(JP_DIR, crm_asset))

    # Build and sync all 8 legal pages (/terms.html, /jp/terms.html, /privacy.html, /jp/privacy.html, /refund.html, /jp/refund.html, /contact.html, /jp/contact.html)
    build_all_legal_pages(ROOT_DIR, JP_DIR)

    # Sync jp/confirmation.html from root confirmation.html with /jp/confirmation.html canonical
    conf_src = os.path.join(ROOT_DIR, "confirmation.html")
    if os.path.isfile(conf_src):
        with open(conf_src, "r", encoding="utf-8") as cf:
            conf_html = cf.read()
        jp_conf_html = conf_html.replace(
            "https://getbreakai.com/confirmation.html",
            "https://getbreakai.com/jp/confirmation.html",
        )
        with open(os.path.join(JP_DIR, "confirmation.html"), "w", encoding="utf-8") as jcf:
            jcf.write(jp_conf_html)

    now_jst = datetime.now(JST)
    date_str = now_jst.strftime("%Y-%m-%d")

    if os.path.exists(SNAPSHOT_PATH):
        try:
            with open(SNAPSHOT_PATH, "r", encoding="utf-8") as sf:
                snap = json.load(sf)
            date_str = snap.get("updated_date", date_str)
            live_tickers = snap.get("tickers", {})
            for item in SEO_PAGES_SPEC:
                sym = item["ticker"]
                if sym in live_tickers and item["slug"] != "soxl-smh-semiconductor-timing.html":
                    item["entry"] = live_tickers[sym]["entry"]
                    item["atr"] = live_tickers[sym]["atr"]
        except Exception as e:
            print(f"[WARN] Could not merge live snapshot into SEO specs: {e}")

    urls = [
        "https://getbreakai.com/",
        "https://getbreakai.com/jp/",
        "https://getbreakai.com/jp/daily-nisa-quant-report.html",
        "https://getbreakai.com/jp/terms.html",
        "https://getbreakai.com/jp/privacy.html",
        "https://getbreakai.com/jp/refund.html",
        "https://getbreakai.com/terms.html",
        "https://getbreakai.com/privacy.html",
        "https://getbreakai.com/refund.html",
    ]
    min_chars = 999999

    for spec in SEO_PAGES_SPEC:
        html = build_page_html(spec, date_str, SEO_PAGES_SPEC)
        out_file = os.path.join(JP_DIR, spec["slug"])
        with open(out_file, "w", encoding="utf-8") as f:
            f.write(html)
        text_only = re.sub(r"<script[\s\S]*?</script>|<style[\s\S]*?</style>|<[^>]+>", "", html)
        text_len = len(text_only.strip())
        min_chars = min(min_chars, text_len)
        urls.append(f"https://getbreakai.com/jp/{spec['slug']}")

    if "--detail-only" not in sys.argv:
        jp_hub_html = build_hub_html(date_str, SEO_PAGES_SPEC, is_root=False)
        with open(os.path.join(JP_DIR, "index.html"), "w", encoding="utf-8") as f:
            f.write(jp_hub_html)

        root_hub_html = build_hub_html(date_str, SEO_PAGES_SPEC, is_root=True)
        with open(os.path.join(ROOT_DIR, "index.html"), "w", encoding="utf-8") as f:
            f.write(root_hub_html)

    print(f"[OK] Generated {len(SEO_PAGES_SPEC)} Japanese SEO pages + unified /index.html & /jp/index.html + 8 legal pages (min visible text length: {min_chars} chars)")

    sitemap_entries = []
    for i, u in enumerate(urls):
        prio = "1.0" if i == 0 else ("0.95" if i == 1 else "0.85")
        sitemap_entries.append(
            f"  <url>\n    <loc>{u}</loc>\n    <lastmod>{date_str}</lastmod>\n    <changefreq>daily</changefreq>\n    <priority>{prio}</priority>\n  </url>"
        )
    sitemap_xml = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + "\n".join(sitemap_entries) + "\n</urlset>\n"
    with open(SITEMAP_PATH, "w", encoding="utf-8") as f:
        f.write(sitemap_xml)
    print(f"[OK] Updated {SITEMAP_PATH} with {len(urls)} URLs")

    with open(INDEXNOW_KEY_FILE, "w", encoding="utf-8") as f:
        f.write(INDEXNOW_KEY)

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
