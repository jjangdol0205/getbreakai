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
    MOR_LABEL_EN_JP,
    POLAR_MONTHLY_CTA_HREF,
    POLAR_ANNUAL_CTA_HREF,
    PRICE_LABEL_MONTHLY_JP,
    PRICE_LABEL_ANNUAL_JP,
    MANDATORY_DISCLAIMER_JP,
    SOFTWARE_POSITIONING_JP,
    FSA_HYBRID_PHRASE_JP,
    MODEL_CASE_DISCLAIMER_JP,
    MAIN_HUB_EXCLUDED_SLUGS,
    build_payment_and_kpi_head_html,
    build_mandatory_disclaimer_html,
    build_pro_retiree_tools_html,
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
        "ticker": "VYM",
        "terminal_ticker": "VYM",
        "jp_name": "3倍レバレッジETF（SOXL等・新NISA対象外）",
        "title": "【新NISA対象外・老後資金注意喚起】3倍レバレッジETF（SOXL等）の減価リスクと「老後3つの財布」への切り替え解説",
        "focus": "金融庁規定により3倍レバレッジ型ETF（SOXL・TQQQ等）が新NISA対象外となる理由、日々の複利計算による減価（ボラティリティ・ドラッグ）リスク、および老後3つの財布（国債・高配当1489/VYM/HDV・オルカン/S&P500）への安全な切り替え解説",
        "catalyst_type": "⚠️ 新NISA対象外・老後資金注意喚起 ＆ 3倍レバレッジ減価リスク教育解説",
        "entry": 134.50, "atr": 2.10, "iv": 18, "score": 18.0, "dp": "高変動減価注意", "call_ratio": "対象外区分",
        "is_non_nisa_edu": True,
        "is_leveraged_warning": True,
        "noindex": True
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
    is_leveraged_warning = bool(item.get("is_leveraged_warning", False))
    is_noindex = bool(item.get("noindex", False))
    robots_meta_tag = '  <meta name="robots" content="noindex, follow">\n' if is_noindex else ""

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

    if is_leveraged_warning:
        banner_bg = "rgba(244,63,94,0.10)"
        banner_border = "rgba(244,63,94,0.55)"
        banner_color = "#881337"
        verdict_banner = (
            "🚨 【新NISA対象外・老後資金での保有非推奨】3倍レバレッジ型ETF（SOXL・TQQQ等）は日本の金融庁規定により新NISA対象外であり、"
            "日々の値動きの3倍を複利計算する仕組み上、横ばい・下落相場で元本が大きく削られる「減価（ボラティリティ・ドラッグ）」リスクがあります。"
            f"50〜70代の大切な退職金・老後資金には一切推奨せず、{FSA_HYBRID_PHRASE_JP}（老後3つの財布）への切り替えをご案内しています。"
        )
    elif is_avoid:
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
    pro_tools_compact = build_pro_retiree_tools_html(compact=True)
    manual_modal = build_starter_manual_modal_html()
    waitlist_modal = build_vip_waitlist_modal_html()
    footer_html = build_legal_footer_html()

    if is_leveraged_warning:
        body_chapters_html = f"""      <h2>1. なぜ3倍レバレッジ型ETF（SOXL・TQQQ等）は老後資金・退職金運用に不向きなのか（減価リスクの仕組み）</h2>
      <p>
        「SOXL（半導体ブル3倍ETF）」や「TQQQ」などのレバレッジ型ETFは、<strong>1日あたりの指数変動率の3倍</strong>に連動するよう設計された短期指標であり、長期保有を前提とした資産ではありません。たとえば指数が「1日目に10%下落し、翌日に11.1%上昇して元の水準（100）に戻った」場合でも、3倍レバレッジ型は1日目に30%下落（100→70）した後、翌日に33.3%上昇しても「93.3」までしか戻らず、<strong>相場が横ばいでも元本が削られていく『減価（ボラティリティ・ドラッグ）』</strong>が数学的に発生します。
      </p>
      <p>
        さらに半導体サイクルの調整局面では基準価額がピークから<strong>-70%〜-85%以上急落</strong>する事例が過去に何度も観測されており、50〜70代の大切な退職金や老後生活資金を投じると回復までに長い歳月を要する恐れがあります。そのため当サイトでは、<strong>3倍レバレッジ型ETFを老後資金・新NISA世代の資産形成に一切推奨しておりません。</strong>
      </p>

      <h2>2. 金融庁がレバレッジ型・毎月分配型を「新NISA対象外」と定めた理由</h2>
      <p>
        日本の金融庁規定により、<strong>レバレッジ型ETF（SOXL・TQQQ等）および毎月分配型ETF（JEPI・JEPQ・QYLD・SGOV等）は新NISA（つみたて投資枠・成長投資枠とも）の対象外</strong>と明確に定められています。これは長期・積立・分散による安定的な資産形成を守るための制度設計です。
      </p>
      <p>
        万が一、特定口座でレバレッジ型ETFを保有して大きな含み損を抱えている場合も、「いつか戻るまでナンピン（買い増し）する」のではなく、ご自身の生活防衛資金とリスク許容度を冷静に点検し、配当と元本クッションを重視した穏やかな資産配分へ段階的に切り替えることが大切です。
      </p>

      <h2>3. 「老後3つの財布」への切り替えガイド：{FSA_HYBRID_PHRASE_JP}</h2>
      <p>
        公的年金にプラス月5〜15万円のゆとり収入をつくりながら暴落から資産寿命を守るには、値動きの激しい3倍レバレッジ商品ではなく、<strong>{FSA_HYBRID_PHRASE_JP}</strong>による「老後3つの財布」が王道となります。
      </p>
      <p>
        具体的には、<strong>①守りの財布（推奨40%：個人向け国債 変動10年・待機預金・特定口座SGOV）</strong>で生活費2〜3年分の安全クッションを確保し、<strong>②高配当の財布（推奨40%：新NISA適格の1489［1・4・7・10月］＋VYM・HDV［3・6・9・12月］時間差配当）</strong>で非課税キャッシュフローを受け取り、<strong>③成長の財布（推奨20%：新NISAつみたて・オルカン／S&amp;P500などの無レバレッジ指数）</strong>でインフレに備える設計です。上のシミュレーターでは、比較参考として新NISA適格の米国高配当株ETF（$VYM）基準での穏やかな分散株数をご確認いただけます。
      </p>

      <h2>4. 年2〜4回のゆったり配分点検で「夜もぐっすり眠れる老後設計」へ</h2>
      <p>
        老後の資産運用で一番大切なのは、毎日の株価ボードに張り付いて一喜一憂することではなく、健康や趣味・ご家族との時間を楽しみながら<strong>年2〜4回だけ3色コンパス（🟢・🟡・🔴）に合わせて3つの財布の比率を点検すること</strong>です。まずは下記の無料『¥0 楽天・SBI証券 新NISA設定マニュアル』および『30秒・老後収入シミュレーター』で、安心できる非課税キャッシュフロー設計をお試しください。
      </p>"""
    else:
        body_chapters_html = f"""      <h2>1. {jp_name} の米SEC公式決算開示（Form 8-K/10-Q）および公開業績データの整理</h2>
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
      </p>"""

    return f"""<!DOCTYPE html>
<html lang="ja" data-jp-theme="light">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{title} | GetBreakAI ゆとり老後＆新NISA設計ナビ</title>
{robots_meta_tag}  <meta name="description" content="{jp_name}の{focus}を公開データからわかりやすく整理。{FSA_HYBRID_PHRASE_JP}とドル・円同時対応の資産配分シミュレーターを掲載。">
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
      line-height: 1.8;
      font-size: 18px;
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
            <span style="font-size:0.96rem; font-weight:800; color:#0f172a;">💎 全銘柄データ一覧・配当＆資産配分計算Proソフトウェア（随時更新・新NISA老後取り崩し実践PDFガイド＋3つの財布シミュレーター同梱）：</span>
            <div style="display:flex; flex-wrap:wrap; gap:10px;">
              <a href="{POLAR_MONTHLY_CTA_HREF}" data-gba-paid-plan="monthly" data-polar-slot="monthly_29_jp" class="polar-checkout-button" style="display:inline-flex; align-items:center; justify-content:center; min-height:56px; padding:10px 18px; border-radius:10px; background:#1d4ed8; color:#ffffff !important; font-size:0.98rem; font-weight:900; text-decoration:none;">
                ⚡ {PRICE_LABEL_MONTHLY_JP}
              </a>
              <a href="{POLAR_ANNUAL_CTA_HREF}" data-gba-paid-plan="annual" data-polar-slot="annual_199_jp" class="polar-checkout-button" style="display:inline-flex; align-items:center; justify-content:center; min-height:56px; padding:10px 18px; border-radius:10px; background:#b45309; color:#ffffff !important; font-size:0.98rem; font-weight:900; text-decoration:none;">
                👑 {PRICE_LABEL_ANNUAL_JP}
              </a>
            </div>
          </div>
          <div style="margin-top:8px; font-size:0.84rem; color:#334155; font-weight:700;">
            💳 公式決済・税務管理：{MOR_LABEL_EN_JP}（日本国内カード・Apple Pay・Google Pay対応 ／ 14日間返金保証）
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

{body_chapters_html}

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
{pro_tools_compact}
          <div style="display:flex; justify-content:center; gap:10px; flex-wrap:wrap; margin-bottom:10px;">
            <a href="/jp/#gba-retirement-architect-jp" class="btn-cta" style="min-height:56px; display:inline-flex; align-items:center; padding:10px 18px;">🧭 無料30秒・老後収入シミュレーターを開く →</a>
            <a href="{POLAR_MONTHLY_CTA_HREF}" data-gba-paid-plan="monthly" data-polar-slot="monthly_29_jp" class="polar-checkout-button btn-cta" style="min-height:56px; display:inline-flex; align-items:center; padding:10px 18px; background:linear-gradient(135deg,#059669,#047857);">⚡ {PRICE_LABEL_MONTHLY_JP}</a>
            <a href="{POLAR_ANNUAL_CTA_HREF}" data-gba-paid-plan="annual" data-polar-slot="annual_199_jp" class="polar-checkout-button btn-cta" style="min-height:56px; display:inline-flex; align-items:center; padding:10px 18px; background:linear-gradient(135deg,#d97706,#b45309);">👑 {PRICE_LABEL_ANNUAL_JP}</a>
          </div>
          <div style="text-align:center; font-size:0.86rem; color:#475569;">
            💳 {MOR_LABEL_EN_JP}（14日間返金保証） ｜ 🏛️ 法人・メディア提携窓口: <a href="mailto:beable9489@gmail.com" style="color:#1d4ed8; font-weight:800;">beable9489@gmail.com</a>
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
    pro_tools_box = build_pro_retiree_tools_html(compact=False)
    manual_modal = build_starter_manual_modal_html()
    waitlist_modal = build_vip_waitlist_modal_html()
    footer_html = build_legal_footer_html()

    ld_json = json.dumps({
        "@context": "https://schema.org",
        "@graph": [
            {
                "@type": "SoftwareApplication",
                "name": "GetBreakAI — SMH × XLV セクター比率過去検証シミュレーター＆毎朝マーケット指標データ配信",
                "url": canonical_url,
                "image": "https://getbreakai.com/og-preview.png",
                "inLanguage": "ja",
                "applicationCategory": "FinanceApplication",
                "operatingSystem": "Web",
                "description": f"AI半導体（SMH）×ヘルスケア防衛（XLV）の4ステップ比率過去検証シミュレーター。{SOFTWARE_POSITIONING_JP}。{FSA_HYBRID_PHRASE_JP}準拠。",
                "offers": [
                    {
                        "@type": "Offer",
                        "name": PRICE_LABEL_MONTHLY_JP,
                        "price": "29.00",
                        "priceCurrency": "USD",
                        "url": f"{canonical_url}#pricing"
                    },
                    {
                        "@type": "Offer",
                        "name": PRICE_LABEL_ANNUAL_JP,
                        "price": "199.00",
                        "priceCurrency": "USD",
                        "url": f"{canonical_url}#pricing"
                    }
                ]
            },
            {
                "@type": "FAQPage",
                "mainEntity": [
                    {
                        "@type": "Question",
                        "name": "SMH（米国半導体ETF）やXLV（米国ヘルスケアETF）は新NISA成長投資枠で購入できますか？",
                        "acceptedAnswer": {
                            "@type": "Answer",
                            "text": "はい。SMHおよびXLVはレバレッジなしの現物1倍セクターETFのため新NISA「成長投資枠」の対象です。一方、毎月分配型のSGOV・JEPI等は金融庁規定により特定口座（または個人向け国債）で区分管理します。"
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
  <title>SMH × XLV セクター比率過去検証シミュレーター＆毎朝マーケット指標データ配信 | GetBreakAI</title>
  <meta name="description" content="AI半導体の成長（SMH）と医療の守り（XLV）を組み合わせ、暴落に揺れない資産比率を4ステップで過去検証。新NISA成長投資枠・特定口座対応の自己判断用計算ソフトウェア。">
  <link rel="canonical" href="{canonical_url}">
{hreflang_tags}
  <meta property="og:type" content="website">
  <meta property="og:locale" content="ja_JP">
  <meta property="og:site_name" content="GetBreakAI">
  <meta property="og:title" content="AI半導体の成長（SMH）と医療の守り（XLV）で暴落に揺れない資産比率を設計 | GetBreakAI">
  <meta property="og:description" content="4ステップ診断で過去26年検証のSMH : XLVベース比率と¥0証券マニュアルを無料解放。Proプランで毎朝の過熱・恐怖指標トラッキングメール配信。">
  <meta property="og:url" content="{canonical_url}">
  <meta property="og:image" content="https://getbreakai.com/og-preview.png">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="SMH × XLV セクター比率過去検証シミュレーター | GetBreakAI">
  <meta name="twitter:description" content="新NISA成長投資枠（SMH・XLV）×特定口座／個人向け国債ハイブリッド比率シミュレーター。">
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
      --bg-page: #f8fafc;
      --bg-card: #ffffff;
      --bg-sub: #f1f5f9;
      --border-col: #cbd5e1;
      --text-main: #0b1f3a;
      --text-muted: #334155;
      --text-sub: #475569;
      --accent-blue: #1d4ed8;
      --accent-emerald: #059669;
      --accent-rose: #be123c;
      --accent-amber: #b45309;
    }}
    html[data-jp-theme="dark"] {{
      --bg-page: #070b14;
      --bg-card: #0f172a;
      --bg-sub: #1e293b;
      --border-col: #334155;
      --text-main: #f8fafc;
      --text-muted: #cbd5e1;
      --text-sub: #94a3b8;
      --accent-blue: #3b82f6;
      --accent-emerald: #34d399;
      --accent-rose: #fb7185;
      --accent-amber: #fbbf24;
    }}
    * {{ box-sizing: border-box; }}
    html {{ font-size: 18px; }}
    html[data-jp-font="normal"] {{ font-size: 18px; }}
    html[data-jp-font="large"] {{ font-size: 20px; }}
    html[data-jp-font="xlarge"] {{ font-size: 22px; }}
    html, body {{ max-width: 100%; overflow-x: hidden; overflow-wrap: break-word; }}
    body {{
      background: var(--bg-page);
      color: var(--text-main);
      font-family: 'Noto Sans JP', -apple-system, BlinkMacSystemFont, sans-serif;
      font-size: 1rem;
      line-height: 1.76;
      margin: 0;
      padding: 0 0 calc(64px + env(safe-area-inset-bottom, 0px));
      font-feature-settings: "palt" 1;
    }}
    .jp-num {{ font-variant-numeric: tabular-nums; }}
    .container {{ max-width: 980px; margin: 0 auto; padding: 12px 16px 28px; }}

    .top-nav {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      flex-wrap: wrap;
      gap: 8px;
      border-bottom: 1.5px solid var(--border-col);
      padding-bottom: 10px;
      min-height: 50px;
    }}
    .brand-link {{
      color: var(--text-main);
      font-weight: 900;
      font-size: 1.08rem;
      text-decoration: none;
      display: inline-flex;
      align-items: center;
      gap: 8px;
    }}
    .top-nav-actions {{ display: flex; align-items: center; gap: 6px; flex-wrap: wrap; }}
    .btn-top-main, .btn-top-yt, .btn-top-theme, .btn-top-font {{
      padding: 0 12px;
      border-radius: 9px;
      text-decoration: none;
      font-weight: 800;
      font-size: 0.86rem;
      min-height: 44px;
      display: inline-flex;
      align-items: center;
      justify-content: center;
      white-space: nowrap;
      cursor: pointer;
    }}
    .btn-top-main {{ background: #059669; color: #ffffff; border: 1px solid #047857; }}
    .btn-top-yt {{ background: var(--bg-card); color: var(--accent-blue); border: 1.5px solid var(--border-col); }}
    .btn-top-theme {{ background: #0b1f3a; color: #fde68a; border: 1px solid #1e3a8a; }}
    .btn-top-font {{ background: #ecfdf5; color: #065f46; border: 1.5px solid #059669; }}
    html[data-jp-theme="dark"] .btn-top-font {{ background: rgba(16,185,129,0.2); color: #6ee7b7; border-color: #34d399; }}

    .gba-hero-mode-badge {{
      display: inline-flex;
      align-items: center;
      gap: 6px;
      margin-top: 14px;
      padding: 5px 14px;
      border-radius: 999px;
      background: #ecfdf5;
      border: 1.5px solid #059669;
      color: #065f46;
      font-size: 0.86rem;
      font-weight: 900;
    }}
    html[data-jp-theme="dark"] .gba-hero-mode-badge {{
      background: rgba(16,185,129,0.18);
      color: #6ee7b7;
      border-color: #34d399;
    }}
    .hero-title {{
      margin: 10px 0 8px;
      font-size: clamp(1.52rem, 2.9vw, 2.08rem);
      color: var(--text-main);
      font-weight: 900;
      line-height: 1.35;
    }}
    .hero-sublead {{
      font-size: 1.05rem;
      color: var(--text-muted);
      font-weight: 700;
      margin: 0 0 18px;
      line-height: 1.65;
    }}

    /* STAGE 1: 4-Step SMH x XLV Survey (#gba-retirement-architect-jp) */
    .gba-survey-card {{
      background: var(--bg-card);
      border: 2.5px solid #059669;
      border-radius: 18px;
      padding: 24px 22px;
      margin-bottom: 20px;
      box-shadow: 0 12px 30px rgba(5, 150, 105, 0.10);
    }}
    .gba-stage-top {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      flex-wrap: wrap;
      gap: 8px;
      margin-bottom: 12px;
    }}
    .gba-stage-badge {{
      padding: 5px 13px;
      border-radius: 999px;
      font-size: 0.86rem;
      font-weight: 900;
      color: #ffffff;
    }}
    .gba-stage-badge.s1 {{ background: #059669; }}
    .gba-stage-badge.s2 {{ background: #1d4ed8; }}
    .gba-stage-badge.s3 {{ background: #b45309; }}

    .gba-step-dots {{ display: flex; flex-wrap: wrap; gap: 6px; }}
    .gba-step-dot {{
      min-height: 40px;
      padding: 6px 12px;
      border-radius: 999px;
      border: 1.5px solid var(--border-col);
      background: var(--bg-sub);
      color: var(--text-sub);
      font-size: 0.88rem;
      font-weight: 800;
      cursor: pointer;
    }}
    .gba-step-dot.is-done {{ border-color: #059669; background: #ecfdf5; color: #065f46; }}
    html[data-jp-theme="dark"] .gba-step-dot.is-done {{ background: rgba(16,185,129,0.16); color: #6ee7b7; }}
    .gba-step-dot.is-current {{ border-color: #059669; background: #059669; color: #ffffff; }}

    .gba-progress-track {{
      width: 100%;
      height: 10px;
      border-radius: 999px;
      background: var(--bg-sub);
      border: 1px solid var(--border-col);
      overflow: hidden;
      margin: 10px 0 18px;
    }}
    .gba-progress-track span {{
      display: block;
      height: 100%;
      background: linear-gradient(90deg, #059669 0%, #1d4ed8 100%);
      border-radius: 999px;
      transition: width 0.2s ease;
    }}
    .gba-q-heading {{
      font-size: 1.2rem;
      font-weight: 900;
      margin: 0 0 12px;
      color: var(--text-main);
    }}
    .gba-opt-stack {{ display: grid; grid-template-columns: 1fr; gap: 10px; }}
    .gba-opt-btn {{
      width: 100%;
      min-height: 64px;
      padding: 13px 16px;
      border-radius: 13px;
      border: 2px solid var(--border-col);
      background: var(--bg-sub);
      color: var(--text-main);
      text-align: left;
      cursor: pointer;
      display: flex;
      flex-direction: column;
      gap: 4px;
      font-family: inherit;
    }}
    .gba-opt-btn.is-active {{
      border-color: #059669;
      background: #ecfdf5;
      color: #064e3b;
      box-shadow: 0 0 0 3px rgba(5, 150, 105, 0.14);
    }}
    html[data-jp-theme="dark"] .gba-opt-btn.is-active {{
      border-color: #34d399;
      background: rgba(16, 185, 129, 0.18);
      color: #f8fafc;
    }}
    .gba-opt-btn strong {{ font-size: 1.04rem; font-weight: 900; }}
    .gba-opt-btn span {{ font-size: 0.92rem; color: var(--text-muted); }}

    .gba-scale-grid {{
      display: grid;
      grid-template-columns: repeat(5, minmax(0, 1fr));
      gap: 8px;
    }}
    .gba-scale-btn {{
      min-height: 62px;
      padding: 10px 8px;
      border-radius: 12px;
      border: 2px solid var(--border-col);
      background: var(--bg-sub);
      color: var(--text-main);
      font-size: 0.96rem;
      font-weight: 900;
      cursor: pointer;
      line-height: 1.3;
    }}
    .gba-scale-btn.is-active {{
      border-color: #059669;
      background: #059669;
      color: #ffffff;
    }}
    .gba-fsa-step-note {{
      margin-top: 12px;
      padding: 11px 14px;
      border-radius: 11px;
      background: #eff6ff;
      border: 1.5px solid #93c5fd;
      color: #1e3a8a;
      font-size: 0.92rem;
      font-weight: 700;
      line-height: 1.62;
    }}
    html[data-jp-theme="dark"] .gba-fsa-step-note {{
      background: rgba(29, 78, 216, 0.18);
      border-color: #3b82f6;
      color: #dbeafe;
    }}
    .gba-survey-submit-btn {{
      width: 100%;
      min-height: 64px;
      margin-top: 14px;
      padding: 14px 18px;
      border-radius: 13px;
      border: none;
      background: linear-gradient(135deg, #059669, #047857);
      color: #ffffff;
      font-size: 1.08rem;
      font-weight: 900;
      cursor: pointer;
      box-shadow: 0 10px 24px rgba(5, 150, 105, 0.25);
    }}
    .gba-survey-foot {{
      margin-top: 14px;
      padding-top: 10px;
      border-top: 1px solid var(--border-col);
      display: flex;
      justify-content: space-between;
      align-items: center;
      flex-wrap: wrap;
      gap: 8px;
    }}
    .gba-prev-btn {{
      min-height: 42px;
      padding: 6px 14px;
      border-radius: 9px;
      border: 1.5px solid var(--border-col);
      background: var(--bg-sub);
      color: var(--text-main);
      font-weight: 800;
      cursor: pointer;
    }}

    /* STAGE 2: Passwordless Gate & Instant Ratio Unlock (#gbaMorningClubJp) */
    .gba-morning-club {{
      background: var(--bg-card);
      border: 2.5px solid #1d4ed8;
      border-radius: 18px;
      padding: 22px 20px;
      margin-bottom: 20px;
    }}
    .gba-teaser-banner {{
      padding: 13px 15px;
      border-radius: 12px;
      background: #eff6ff;
      border: 1.5px solid #93c5fd;
      color: #0b1f3a;
      font-size: 0.98rem;
      line-height: 1.65;
      margin-bottom: 12px;
    }}
    html[data-jp-theme="dark"] .gba-teaser-banner {{
      background: rgba(29, 78, 216, 0.18);
      border-color: #3b82f6;
      color: #f8fafc;
    }}
    .gba-locked-gate-preview {{
      padding: 12px 15px;
      border-radius: 12px;
      background: var(--bg-sub);
      border: 1.5px dashed var(--border-col);
      margin-bottom: 12px;
    }}
    .gba-locked-row {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      flex-wrap: wrap;
      gap: 8px;
      padding: 5px 0;
      font-size: 0.95rem;
      font-weight: 800;
    }}
    .gba-locked-pill {{
      background: #ecfdf5;
      color: #065f46;
      border: 1px solid #6ee7b7;
      padding: 3px 10px;
      border-radius: 999px;
      font-size: 0.82rem;
      font-weight: 900;
    }}
    html[data-jp-theme="dark"] .gba-locked-pill {{
      background: rgba(16,185,129,0.2);
      color: #6ee7b7;
    }}

    .gba-jp-pwless-box {{
      padding: 16px;
      border-radius: 14px;
      background: var(--bg-sub);
      border: 2px solid #059669;
    }}
    .gba-jp-pwless-form {{
      display: grid;
      grid-template-columns: minmax(140px, 0.75fr) minmax(220px, 1.35fr) auto;
      gap: 10px;
    }}
    .gba-jp-pwless-input {{
      min-height: 54px;
      padding: 10px 13px;
      border-radius: 10px;
      border: 1.8px solid var(--border-col);
      background: var(--bg-card);
      color: var(--text-main);
      font-size: 0.98rem;
      font-weight: 700;
      width: 100%;
    }}
    .gba-jp-pwless-submit {{
      min-height: 54px;
      padding: 10px 18px;
      border-radius: 10px;
      border: none;
      background: linear-gradient(135deg, #059669, #047857);
      color: #ffffff;
      font-size: 0.96rem;
      font-weight: 900;
      cursor: pointer;
      white-space: nowrap;
    }}
    .gba-jp-pwless-feedback {{
      display: none;
      margin-top: 12px;
      padding: 14px;
      border-radius: 12px;
      background: var(--bg-card);
      border: 1.5px solid #059669;
    }}
    .gba-jp-pwless-feedback.is-error {{
      background: #fff1f2;
      border-color: #e11d48;
      color: #9f1239;
    }}

    .gba-ratio-cards {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
      gap: 10px;
      margin: 12px 0;
    }}
    .gba-ratio-card {{
      background: var(--bg-sub);
      border: 1.5px solid var(--border-col);
      border-radius: 11px;
      padding: 12px;
    }}
    .gba-ratio-bar {{
      height: 9px;
      border-radius: 999px;
      background: rgba(148,163,184,0.28);
      overflow: hidden;
      margin: 6px 0;
    }}
    .gba-ratio-bar span {{ display: block; height: 100%; border-radius: 999px; }}
    .gba-stress-table {{
      width: 100%;
      border-collapse: collapse;
      font-size: 0.92rem;
      margin-top: 8px;
      background: var(--bg-card);
    }}
    .gba-stress-table th, .gba-stress-table td {{
      border: 1px solid var(--border-col);
      padding: 9px 11px;
      text-align: left;
    }}
    .gba-stress-table th {{ background: var(--bg-sub); font-weight: 900; }}

    /* ¥0 Starter Manual (#gbaFreeStarterManualJp) */
    .gba-starter-manual {{
      background: linear-gradient(135deg, #f0fdf4 0%, #eff6ff 100%);
      border: 2px solid #059669;
      border-radius: 16px;
      padding: 18px;
      margin-bottom: 20px;
    }}
    html[data-jp-theme="dark"] .gba-starter-manual {{
      background: linear-gradient(135deg, rgba(6,78,59,0.32), rgba(15,23,42,0.96));
      border-color: #10b981;
    }}
    .gba-manual-top-row {{ display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:8px; margin-bottom:8px; }}
    .gba-manual-free-badge {{ background:#059669; color:#ffffff; font-size:0.86rem; font-weight:900; padding:4px 12px; border-radius:999px; }}
    .gba-manual-sub-badge {{ font-size:0.86rem; font-weight:800; color:#065f46; background:#d1fae5; border:1px solid #6ee7b7; padding:4px 11px; border-radius:999px; }}
    html[data-jp-theme="dark"] .gba-manual-sub-badge {{ background:rgba(16,185,129,0.2); color:#a7f3d0; }}
    .gba-manual-chap-grid {{ display:grid; grid-template-columns:repeat(3, minmax(0, 1fr)); gap:10px; margin:12px 0; }}
    .gba-manual-chap-btn {{ background:var(--bg-card); border:1.5px solid var(--border-col); border-radius:11px; padding:12px; text-align:left; cursor:pointer; display:flex; flex-direction:column; gap:5px; color:var(--text-main); }}
    .gba-manual-chap-tag {{ font-size:0.8rem; font-weight:900; color:#047857; background:#ecfdf5; border:1px solid #a7f3d0; padding:2px 8px; border-radius:999px; width:fit-content; }}
    .gba-manual-cta-row {{ display:flex; flex-wrap:wrap; gap:10px; }}
    .gba-manual-open-btn {{ background:linear-gradient(135deg,#059669,#047857); color:#ffffff; border:none; border-radius:11px; padding:12px 18px; min-height:54px; font-size:1rem; font-weight:900; cursor:pointer; flex:1 1 280px; }}

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
    .gba-manual-funnel-links {{ display:flex; flex-wrap:wrap; gap:10px; }}
    .gba-manual-pro-link, .gba-manual-vip-link {{ display:inline-flex; align-items:center; min-height:44px; padding:6px 13px; border-radius:999px; font-size:0.92rem; font-weight:900; text-decoration:none; border:1.5px solid var(--accent-blue); color:var(--accent-blue); }}
    .gba-manual-vip-link {{ border-color:var(--accent-amber); color:var(--accent-amber); }}

    /* STAGE 3: Paid Pro Upgrade (#pricing) */
    .defense-card {{
      background: var(--bg-card);
      border: 2.5px solid #b45309;
      border-radius: 18px;
      padding: 24px 20px;
      margin-bottom: 22px;
    }}
    .defense-title {{ font-size: 1.28rem; font-weight: 900; margin: 6px 0; }}
    .defense-subtitle {{ font-size: 0.98rem; color: var(--text-muted); margin-bottom: 14px; }}
    .cta-dual-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(260px, 1fr)); gap: 12px; }}
    .btn-checkout-primary, .btn-checkout-annual {{
      color: #ffffff !important; text-decoration: none; padding: 16px 18px; border-radius: 13px; font-size: 1.05rem; font-weight: 900;
      display: flex; flex-direction: column; gap: 4px; align-items: center; justify-content: center; width: 100%; text-align: center; min-height: 70px;
    }}
    .btn-checkout-primary {{ background: linear-gradient(135deg, #1d4ed8, #1e3a8a); }}
    .btn-checkout-annual {{ background: linear-gradient(135deg, #059669, #047857); }}
    .cta-subnote {{ font-size: 0.92rem; color: var(--text-muted); margin-top: 10px; line-height: 1.65; text-align: center; }}

    /* Secondary Collapsible Tools & SEO Archive */
    .gba-ref-accordion, .vip-vault-card {{
      background: var(--bg-card);
      border: 1.5px solid var(--border-col);
      border-radius: 14px;
      padding: 15px 18px;
      margin-bottom: 18px;
    }}
    .gba-nisa-core-strip {{ background: var(--bg-sub); border: 1.5px solid #93c5fd; border-radius: 12px; padding: 14px; margin: 12px 0; }}
    .gba-nisa-core-grid {{ display: grid; grid-template-columns: repeat(4, minmax(0, 1fr)); gap: 10px; margin-top: 10px; }}
    .gba-nisa-core-card {{ background: var(--bg-card); border: 1px solid var(--border-col); border-radius: 10px; padding: 10px; font-size: 0.9rem; display: flex; flex-direction: column; gap: 3px; }}
    .gba-nisa-core-badge {{ font-size: 0.82rem; font-weight: 900; color: var(--accent-blue); }}
    .calc-card {{ background: var(--bg-sub); border: 1.5px solid var(--border-col); border-radius: 12px; padding: 14px; margin-top: 12px; }}
    .calc-fast-inputs {{ display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 8px; margin: 8px 0; }}
    .fast-field {{ background: var(--bg-card); border: 1px solid var(--border-col); border-radius: 8px; padding: 7px 9px; }}
    .fast-field label {{ display: block; font-size: 0.8rem; font-weight: 800; color: var(--text-sub); }}
    .fast-field input {{ width: 100%; border: 1px solid var(--border-col); border-radius: 6px; background: var(--bg-card); color: var(--text-main); font-family: monospace; font-size: 0.96rem; font-weight: 800; padding: 6px 8px; min-height: 38px; }}
    .tax-calc-bar {{ display: grid; grid-template-columns: 1fr 1fr; gap: 8px; margin-bottom: 8px; }}
    .tax-mode-btn {{ background: var(--bg-card); border: 1.5px solid var(--border-col); color: var(--text-main); border-radius: 8px; min-height: 44px; font-size: 0.92rem; font-weight: 800; cursor: pointer; }}
    .tax-mode-btn.active {{ background: #1d4ed8; color: #ffffff; border-color: #1e40af; }}
    .btn-calc-submit {{ width: 100%; min-height: 48px; background: #1d4ed8; color: #ffffff; border: none; border-radius: 10px; font-size: 0.96rem; font-weight: 900; cursor: pointer; margin-bottom: 10px; }}
    .calc-outputs {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 8px; margin-bottom: 10px; }}
    .out-card {{ background: var(--bg-card); border: 1px solid var(--border-col); border-radius: 9px; padding: 10px; }}
    .out-label {{ font-size: 0.82rem; font-weight: 700; color: var(--text-sub); }}
    .out-val {{ font-size: 1rem; font-weight: 900; font-family: monospace; }}
    .val-emerald {{ color: var(--accent-emerald); }}
    .val-rose {{ color: var(--accent-rose); }}
    .val-amber {{ color: var(--accent-amber); }}
    .capital-pills, .preset-bar {{ display: flex; gap: 6px; flex-wrap: wrap; margin-top: 6px; }}
    .cap-btn, .preset-chip {{ background: var(--bg-card); border: 1.5px solid var(--border-col); color: var(--text-main); padding: 6px 10px; border-radius: 8px; font-size: 0.88rem; font-weight: 800; cursor: pointer; min-height: 42px; }}
    .cap-btn.active, .preset-chip.active {{ background: #1d4ed8; color: #ffffff; border-color: #1e40af; }}
    .vip-input-row {{ display: flex; gap: 8px; flex-wrap: wrap; margin-top: 10px; }}
    .vip-key-input {{ flex: 1; min-width: 180px; padding: 10px 12px; border: 1.5px solid var(--border-col); border-radius: 8px; font-family: monospace; font-size: 0.92rem; color: var(--text-main); background: var(--bg-sub); }}
    .vip-unlock-btn {{ background: #0b1f3a; color: #ffffff; border: 1px solid #334155; border-radius: 8px; padding: 10px 16px; font-weight: 800; font-size: 0.92rem; cursor: pointer; min-height: 46px; }}

    .grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(280px, 1fr)); gap: 14px; margin-top: 14px; }}
    .hub-seo-card {{ display: block; background: var(--bg-card); border: 1.5px solid var(--border-col); border-radius: 12px; padding: 15px; color: var(--text-main); text-decoration: none; }}
    .hub-seo-meta {{ font-family: monospace; font-size: 0.84rem; color: var(--accent-amber); font-weight: 800; margin-bottom: 4px; }}
    .hub-seo-title {{ font-weight: 900; font-size: 0.98rem; margin-bottom: 5px; }}
    .hub-seo-focus {{ font-size: 0.92rem; color: var(--text-sub); line-height: 1.6; }}
    .faq-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 12px; margin-top: 12px; }}
    .faq-card {{ background: var(--bg-card); border: 1.5px solid var(--border-col); border-radius: 12px; padding: 15px; }}

    .jp-mobile-bottom-nav {{ display: none; }}
    @media (max-width: 920px) {{
      .gba-scale-grid {{ grid-template-columns: repeat(2, minmax(0, 1fr)); }}
      .gba-jp-pwless-form, .gba-manual-chap-grid, .gba-manual-broker-grid {{ grid-template-columns: 1fr; }}
      .gba-nisa-core-grid {{ grid-template-columns: repeat(2, minmax(0, 1fr)); }}
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
        border-top: 2px solid #059669;
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
      .jp-mobile-bottom-nav a:last-child {{ border-right: none; background: #059669; color: #ffffff; }}
    }}
    @media (max-width: 640px) {{
      .gba-nisa-core-grid, .calc-fast-inputs {{ grid-template-columns: 1fr; }}
    }}
    @media print {{
      body.printing-gba-manual > *:not(#gbaStarterManualModal) {{ display: none !important; }}
      body.printing-gba-manual #gbaStarterManualModal {{ display: block !important; position: static !important; background: #ffffff !important; padding: 0 !important; }}
    }}
  </style>
</head>
<body>
  <div class="container">
    <!-- Top Navigation (Clean 3-Stage SMH x XLV Focus) -->
    <nav class="top-nav" aria-label="SMH × XLV セクター比率ナビゲーション">
      <a href="/jp/" class="brand-link">⚡ GetBreakAI <span style="font-size:0.84rem; color:var(--accent-emerald); font-weight:800;">SMH × XLV セクター比率設計ナビ</span></a>
      <div class="top-nav-actions">
        <button type="button" id="btnToggleJpFont" onclick="cycleJpFontSize()" class="btn-top-font" aria-label="文字サイズ切替">🔍 文字: 標準 18px</button>
        <a href="#gba-retirement-architect-jp" class="btn-top-main">🧭 1. 4問比率診断</a>
        <a href="#gba-jp-passwordless-signup" class="btn-top-yt">🍵 2. 無料解放</a>
        <a href="#pricing" class="btn-top-yt">💎 3. Pro日報</a>
        <a href="https://www.youtube.com/@GetBreakAI" target="_blank" rel="noopener" class="btn-top-yt">📺 YouTube</a>
        <button type="button" id="btnToggleJpTheme" onclick="toggleJpTheme()" class="btn-top-theme">🌙 切替</button>
      </div>
    </nav>

    <div class="gba-hero-mode-badge" id="gbaHeroCopyModeBadge">
      🧭 SMH × XLV セクター比率過去検証シミュレーター＆毎朝マーケット指標データ配信
    </div>
    <h1 class="hero-title" id="gbaHeroCopyModeTitle">
      AI半導体の成長（SMH）と医療の守り（XLV）を組み合わせ、暴落に揺れない資産比率を設計
    </h1>
    <p class="hero-sublead" id="gbaHeroCopyModeSub">
      下の4つの質問をタップするだけで、過去26年（ITバブル・リーマン・2022年下落）のデータに基づく <b>SMH × XLV 過去検証ベース比率</b> と <b>新NISA成長投資枠×特定口座・国債の配分目安</b> を算出します。
    </p>

    <!-- STAGE 1 OF 3: SMH x XLV 4-STEP GUIDED BALANCE SURVEY (#gba-retirement-architect-jp) -->
    <section class="gba-survey-card" id="gba-retirement-architect-jp" aria-label="Stage 1: SMH × XLV 4ステップ比率診断アンケート">
      <div class="gba-stage-top">
        <span class="gba-stage-badge s1">STAGE 1 / 3 ・ 4ステップ比率診断（登録不要）</span>
        <span id="gbaSurveyStepLabelJp" style="font-family:monospace; font-weight:900; color:var(--accent-emerald);">Step 1 / 4 (25%)</span>
      </div>

      <div class="gba-step-dots" role="tablist" aria-label="診断ステップ">
        <button type="button" class="gba-step-dot is-current" data-gba-step-ind="1" onclick="goToGbaSurveyStepJp(1)">1. 運用目的</button>
        <button type="button" class="gba-step-dot" data-gba-step-ind="2" onclick="goToGbaSurveyStepJp(2)">2. 資産規模</button>
        <button type="button" class="gba-step-dot" data-gba-step-ind="3" onclick="goToGbaSurveyStepJp(3)">3. 許容下落幅</button>
        <button type="button" class="gba-step-dot" data-gba-step-ind="4" onclick="goToGbaSurveyStepJp(4)">4. ハイテク比率</button>
      </div>
      <div class="gba-progress-track" aria-hidden="true">
        <span id="gbaSurveyProgressFillJp" style="width:25%;"></span>
      </div>

      <!-- Step 1: Objective & Horizon -->
      <div class="gba-step-pane" data-gba-step-pane="1">
        <h2 class="gba-q-heading">Q1（Step 1/4）：一番重視したい運用目的・スタンスはどれですか？</h2>
        <div class="gba-opt-stack" role="group" aria-label="運用目的と期間">
          <button type="button" class="gba-opt-btn" data-gba-sfield="objective" data-gba-sval="growth" aria-pressed="false" onclick="selectGbaSurveyOptionJp('objective', 'growth', this)">
            <strong>🚀 AI・成長重視</strong>
            <span>AI・半導体の長期成長（SMH）を積極的に取り込みつつ、ヘルスケア（XLV）で急落の振れ幅を緩和</span>
          </button>
          <button type="button" class="gba-opt-btn is-active" data-gba-sfield="objective" data-gba-sval="balanced" aria-pressed="true" onclick="selectGbaSurveyOptionJp('objective', 'balanced', this)">
            <strong>⚖️ 安定老後・資産バランス重視</strong>
            <span>半導体成長（SMH）と景気後退に強い医療ディフェンシブ（XLV）をバランスよく組み合わせる王道設計</span>
          </button>
          <button type="button" class="gba-opt-btn" data-gba-sfield="objective" data-gba-sval="defense" aria-pressed="false" onclick="selectGbaSurveyOptionJp('objective', 'defense', this)">
            <strong>🛡️ 下落局面の守り最優先</strong>
            <span>医療（XLV）＋個人向け国債・特定口座キャッシュクッションを厚く保ち、資産目減りの抑制を最優先</span>
          </button>
        </div>
      </div>

      <!-- Step 2: Portfolio Scale Preset (FSA Shin-NISA Growth Quota + Tokutei/JGB Note) -->
      <div class="gba-step-pane" data-gba-step-pane="2" style="display:none;">
        <h2 class="gba-q-heading">Q2（Step 2/4）：想定しているご運用資金の規模をお選びください：</h2>
        <div class="gba-scale-grid" role="group" aria-label="運用資金規模プリセット">
          <button type="button" class="gba-scale-btn" data-gba-sfield="scale" data-gba-sval="300" aria-pressed="false" onclick="selectGbaSurveyOptionJp('scale', 300, this)">300万円</button>
          <button type="button" class="gba-scale-btn" data-gba-sfield="scale" data-gba-sval="1000" aria-pressed="false" onclick="selectGbaSurveyOptionJp('scale', 1000, this)">1,000万円</button>
          <button type="button" class="gba-scale-btn is-active" data-gba-sfield="scale" data-gba-sval="1800" aria-pressed="true" onclick="selectGbaSurveyOptionJp('scale', 1800, this)">1,800万円<br><small>（新NISA生涯枠）</small></button>
          <button type="button" class="gba-scale-btn" data-gba-sfield="scale" data-gba-sval="3000" aria-pressed="false" onclick="selectGbaSurveyOptionJp('scale', 3000, this)">3,000万円</button>
          <button type="button" class="gba-scale-btn" data-gba-sfield="scale" data-gba-sval="5000" aria-pressed="false" onclick="selectGbaSurveyOptionJp('scale', 5000, this)">5,000万円+</button>
        </div>
        <div class="gba-fsa-step-note">
          🏛️ <strong>金融庁・新NISA規定準拠メモ：</strong><strong>SMH</strong>（米国半導体ETF）および <strong>XLV</strong>（米国ヘルスケアETF）はレバレッジなしの現物1倍セクターETFのため<strong>「新NISA 成長投資枠」対象</strong>です。安全クッション枠は金融庁ルールに準拠し、<strong>「個人向け国債（変動10年）」または「特定口座（毎月分配型の米国短期国債ETF SGOV等）」</strong>と組み合わせて区分管理します。
        </div>
      </div>

      <!-- Step 3: Max Drawdown Comfort Zone -->
      <div class="gba-step-pane" data-gba-step-pane="3" style="display:none;">
        <h2 class="gba-q-heading">Q3（Step 3/4）：相場急落時、一時的な資産変動はどこまでなら落ち着いて保有できますか？</h2>
        <div class="gba-opt-stack" role="group" aria-label="許容下落幅">
          <button type="button" class="gba-opt-btn" data-gba-sfield="comfort" data-gba-sval="dd10" aria-pressed="false" onclick="selectGbaSurveyOptionJp('comfort', 'dd10', this)">
            <strong>🛡️ -10% 安心睡眠・守り優先（-10% Sleep-Well Priority）</strong>
            <span>ヘルスケア（XLV）＋個人向け国債／特定口座SGOVの安全クッションで値動きを穏やかに抑制</span>
          </button>
          <button type="button" class="gba-opt-btn is-active" data-gba-sfield="comfort" data-gba-sval="dd18" aria-pressed="true" onclick="selectGbaSurveyOptionJp('comfort', 'dd18', this)">
            <strong>⚖️ -18% 標準バランス・クッション（-18% Balanced Cushion）</strong>
            <span>過去26年検証の王道 SMH × XLV 2セクター組み合わせで成長と守りを両立</span>
          </button>
          <button type="button" class="gba-opt-btn" data-gba-sfield="comfort" data-gba-sval="dd25" aria-pressed="false" onclick="selectGbaSurveyOptionJp('comfort', 'dd25', this)">
            <strong>🚀 -25% 長期複利・成長優先（-25% Long-Term Compounding）</strong>
            <span>一時的な調整を受け入れ、長期のAI・半導体成長リターンを重視</span>
          </button>
        </div>
      </div>

      <!-- Step 4: Current Tech Concentration Check -> Submit! -->
      <div class="gba-step-pane" data-gba-step-pane="4" style="display:none;">
        <h2 class="gba-q-heading">Q4（Step 4/4）：現在お持ちの資産のうち、ハイテク・半導体株の割合はどのくらいですか？</h2>
        <div class="gba-opt-stack" role="group" aria-label="現在のハイテク比率">
          <button type="button" class="gba-opt-btn is-active" data-gba-sfield="techMix" data-gba-sval="tech_high" aria-pressed="true" onclick="selectGbaSurveyOptionJp('techMix', 'tech_high', this)">
            <strong>📈 ハイテク・半導体に集中（70%超）</strong>
            <span>米国ハイテク株・半導体・NASDAQ系が多く、急落時のクッション設計を確認したい</span>
          </button>
          <button type="button" class="gba-opt-btn" data-gba-sfield="techMix" data-gba-sval="tech_mid" aria-pressed="false" onclick="selectGbaSurveyOptionJp('techMix', 'tech_mid', this)">
            <strong>⚖️ バランス分散（30〜70%）</strong>
            <span>複数銘柄・投信を保有しており、シンプルな SMH × XLV の基準比率と比較したい</span>
          </button>
          <button type="button" class="gba-opt-btn" data-gba-sfield="techMix" data-gba-sval="tech_low" aria-pressed="false" onclick="selectGbaSurveyOptionJp('techMix', 'tech_low', this)">
            <strong>🏦 現金・広く分散された指数中心（30%未満）</strong>
            <span>預貯金やオルカン・S&amp;P500中心から、無理のない SMH × XLV ベース比率を知りたい</span>
          </button>
        </div>

        <button type="button" class="gba-survey-submit-btn" id="btnGbaSubmitSmhXlvSurvey" onclick="submitGbaSmhXlvSurveyJp()">
          私の SMH × XLV 過去検証ベース比率を算出する →
        </button>
      </div>

      <div class="gba-survey-foot">
        <button type="button" class="gba-prev-btn" id="btnGbaSurveyPrevJp" style="visibility:hidden;" onclick="prevGbaSurveyStepJp()">← 前の質問へ戻る</button>
        <span style="font-size:0.88rem; color:var(--text-sub); font-weight:700;">公開市場データ過去検証ツール（ブラウザ内計算・証券口座ログイン不要）</span>
      </div>
    </section>

    <!-- STAGE 2 OF 3: FREE 3-SECOND PASSWORDLESS MEMBER GATE (#gbaMorningClubJp -> #gba-jp-passwordless-signup) -->
    <div id="gbaMorningClubRoot">
      <section class="gba-morning-club" id="gbaMorningClubJp" aria-label="Stage 2: 朝の資産守り倶楽部・無料3秒解放">
        <div class="gba-stage-top">
          <span class="gba-stage-badge s2">STAGE 2 / 3 ・ 無料3秒メール登録で診断結果を即時解放（¥0）</span>
          <span style="font-size:0.86rem; font-weight:800; color:var(--text-sub);">パスワード不要 ・ いつでも1クリック配信停止</span>
        </div>

        <!-- 1-Line Profile Summary Teaser -->
        <div class="gba-teaser-banner" id="gbaSurveyTeaserBannerJp" role="status" aria-live="polite">
          📊 <strong>診断プロファイル準備完了：</strong>安定老後・資産バランス重視 ／ 1,800万円（新NISA生涯枠） ／ 許容幅 -18% ／ ハイテク70%超 — 下欄にメールアドレスを入力（<b>3秒・パスワード不要</b>）すると、<b>SMH : XLV 過去検証ベース比率表</b>・<b>過去26年暴落比較表</b>・<b>¥0 証券マニュアル</b>がこの画面で即時解放されます！
        </div>

        <!-- Locked Teaser Preview (Hidden automatically once unlocked) -->
        <div class="gba-locked-gate-preview" id="gbaSurveyLockedPreviewJp">
          <div class="gba-locked-row">
            <span>🔒 <strong>あなた専用の SMH : XLV（＋個人向け国債／特定口座SGOV）過去検証ベース比率＆円換算表</strong></span>
            <span class="gba-locked-pill">無料メール入力で即時表示</span>
          </div>
          <div class="gba-locked-row">
            <span>🔒 <strong>過去26年（ITバブル・2008年リーマン・2022年下落）比較表 ＋ ¥0 楽天・SBI証券マニュアル</strong></span>
            <span class="gba-locked-pill">無料メール入力で即時表示</span>
          </div>
        </div>

        <!-- Passwordless 3-Sec Club Signup Box (#gba-jp-passwordless-signup) -->
        <div class="gba-jp-pwless-box" id="gba-jp-passwordless-signup">
          <form class="gba-jp-pwless-form" id="gba-jp-club-form" onsubmit="return submitGbaJpPasswordlessClub(event)">
            <label for="gba-jp-club-nickname" style="position:absolute; width:1px; height:1px; overflow:hidden; clip:rect(0,0,0,0);">ニックネーム（任意）</label>
            <input type="text" id="gba-jp-club-nickname" class="gba-jp-pwless-input" autocomplete="nickname" maxlength="40" placeholder="お名前・ニックネーム（任意）">
            <label for="gba-jp-club-email" style="position:absolute; width:1px; height:1px; overflow:hidden; clip:rect(0,0,0,0);">メールアドレス</label>
            <input type="email" id="gba-jp-club-email" class="gba-jp-pwless-input" required autocomplete="email" placeholder="メールアドレスを入力（例: taro@example.jp）">
            <input type="text" id="gba-jp-club-hp" name="website_hp" tabindex="-1" autocomplete="off" aria-hidden="true" style="display:none">
            <button type="submit" id="gba-jp-club-submit" class="gba-jp-pwless-submit">
              🔓 無料で比率結果＆¥0マニュアルを即時解放（3秒） →
            </button>
          </form>

          <div class="gba-jp-pwless-feedback" id="gba-jp-club-feedback" role="status" aria-live="polite">
            <div id="gba-jp-club-feedback-text" style="font-weight:900; color:var(--accent-emerald); margin-bottom:8px;"></div>
            <div id="jpFreeMemberBonusBox"></div>
            <div style="margin-top:12px; display:flex; flex-wrap:wrap; gap:10px;">
              <a href="#gbaFreeStarterManualJp" id="gba-jp-club-manual-btn" onclick="openGbaStarterManualModal(); return false;" style="display:inline-flex; align-items:center; min-height:48px; padding:10px 16px; border-radius:10px; background:#059669; color:#ffffff; font-weight:900; text-decoration:none;">
                📘 解放済み：¥0 楽天・SBI証券 新NISA基本マニュアルを開く →
              </a>
              <a href="#pricing" style="display:inline-flex; align-items:center; min-height:48px; padding:10px 16px; border-radius:10px; background:#1d4ed8; color:#ffffff; font-weight:900; text-decoration:none;">
                ⚡ 毎朝の過熱・恐怖指標＆SMH×XLV比率トラッキング日報（Stage 3 Pro）を見る ↓
              </a>
            </div>
          </div>
        </div>
      </section>
    </div>

    <!-- 📘 ¥0 無料公開商品：楽天・SBI証券 新NISA基本マニュアル (#gbaFreeStarterManualJp) -->
    <section class="gba-starter-manual" id="gbaFreeStarterManualJp" aria-label="¥0 無料公開商品：はじめての新NISA＆証券アプリ基本マニュアル">
      <div class="gba-manual-top-row">
        <span class="gba-manual-free-badge" id="gbaManualUnlockBadgeJp">📘 ¥0 無料公開マニュアル（3秒メール登録で保存版も無料配信）</span>
        <span class="gba-manual-sub-badge">🖨️ 印刷・メール保存対応 ／ 楽天証券・SBI証券 対応</span>
      </div>
      <h2 style="font-size:1.18rem; font-weight:900; margin:4px 0 6px;">
        はじめての新NISA＆証券アプリ基本マニュアル（SMH・XLV 指値注文 ＆ 新NISA成長投資枠×特定口座・国債ガイド）
      </h2>
      <div class="gba-manual-chap-grid">
        <button type="button" class="gba-manual-chap-btn" onclick="openGbaStarterManualModal('gbaManualChap1')">
          <span class="gba-manual-chap-tag">第1章 · 安全な指値注文</span>
          <strong>楽天証券・SBI証券での「指値注文」手順</strong>
          <span style="font-size:0.9rem; color:var(--text-muted);">成行注文の高値約定を防ぎ、落ち着いた上限価格で発注する基本手順。</span>
        </button>
        <button type="button" class="gba-manual-chap-btn" onclick="openGbaStarterManualModal('gbaManualChap2')">
          <span class="gba-manual-chap-tag">第2章 · 金融庁ルール準拠</span>
          <strong>新NISA適格（SMH・XLV・1489・VYM）と特定口座（SGOV等）の区分</strong>
          <span style="font-size:0.9rem; color:var(--text-muted);">現物セクターETFと毎月分配型ETFの正しい口座使い分け。</span>
        </button>
        <button type="button" class="gba-manual-chap-btn" onclick="openGbaStarterManualModal('gbaManualChap3')">
          <span class="gba-manual-chap-tag">第3章 · 安全クッション</span>
          <strong>個人向け国債（変動10年）・マネーブリッジ活用</strong>
          <span style="font-size:0.9rem; color:var(--text-muted);">下落局面でも慌てない守りの待機資金づくり。</span>
        </button>
      </div>
      <div class="gba-manual-cta-row">
        <button type="button" id="btnOpenGbaStarterManualJp" class="gba-manual-open-btn" onclick="openGbaStarterManualModal()">
          📖 ¥0 基本マニュアル全3章を開く（画面閲覧・メール受取・印刷可） →
        </button>
      </div>
    </section>

    <!-- STAGE 3 OF 3: PAID PRO UPGRADE (#pricing — Polar.sh ?locale=ja) -->
    <section class="defense-card" id="pricing" aria-label="Stage 3: Proソフトウェア料金プラン">
      <div class="gba-stage-top">
        <span class="gba-stage-badge s3">STAGE 3 / 3 ・ 毎朝のSMH × XLV指標トラッキング＆実践シート Proプラン</span>
        <span style="font-size:0.88rem; font-weight:900; color:var(--accent-emerald);">14日間返金保証 ・ いつでも1クリック解約OK</span>
      </div>
      <div class="defense-title" id="gbaPricingTitleJp">
        💎 SMH × XLV セクター比率過去検証シミュレーター＆毎朝マーケット指標データ配信 Pro
      </div>
      <div class="defense-subtitle">
        毎朝8時、日米市場の過熱・恐怖指標（0〜100）を自動計測し、過去検証モデル上で <b>SMH : XLV 比率</b> がどう変化するかをメールでお届け。さらに運用額別の円・ドル配分シートと随時更新14ページ実践マスターPDFガイドを同梱（公式決済：{MOR_LABEL_EN_JP}）。
      </div>

{pro_tools_box}

      <div class="cta-container">
        <div class="cta-dual-grid">
          <a href="{POLAR_MONTHLY_CTA_HREF}" data-gba-paid-plan="monthly" data-polar-slot="monthly_29_jp" class="btn-checkout-primary polar-checkout-button">
            <span>⚡ {PRICE_LABEL_MONTHLY_JP}</span>
            <span style="font-size:0.9rem; font-weight:900; color:#fef08a;">📘 毎朝SMH×XLV指標日報 ＋ 14ページ実践PDF ＋ 随時更新・新NISA老後取り崩し実践PDFガイド＋3つの財布シミュレーター同梱</span>
            {('<span style="font-size:0.82rem; font-weight:700; opacity:0.94;">Includes Daily Automated SMH × XLV Indicator Digest + 14-Page Master PDF Guide</span>' if is_root else '')}
            <span style="font-size:0.88rem; font-weight:800; opacity:0.96;">1クリック解約OK ／ 14日間全額返金保証（14日間返金保証）</span>
          </a>
          <a href="{POLAR_ANNUAL_CTA_HREF}" data-gba-paid-plan="annual" data-polar-slot="annual_199_jp" class="btn-checkout-annual polar-checkout-button">
            <span>👑 {PRICE_LABEL_ANNUAL_JP}</span>
            <span style="font-size:0.9rem; font-weight:900; color:#fef08a;">📘 43%OFF 年間パス ＋ 14ページ実践PDF ＋ 随時更新・新NISA老後取り崩し実践PDFガイド＋3つの財布シミュレーター同梱</span>
            {('<span style="font-size:0.82rem; font-weight:700; opacity:0.94;">Annual Pass (Save 43%) + Daily SMH × XLV Tracking Digest + 14-Page Master PDF Guide</span>' if is_root else '')}
            <span style="font-size:0.88rem; font-weight:800; opacity:0.96;">1クリック解約OK（月あたり約2,500円） ／ 14日間全額返金保証（14日間返金保証）</span>
          </a>
        </div>
        <div class="cta-subnote">
          💳 公式決済代行：<strong>{MOR_LABEL_EN_JP}</strong>（JCB・Visa・Mastercard・Apple Pay・Google Pay対応・日本語決済画面 <code>?locale=ja</code> 対応・いつでも1クリック解約OK）<br>
          🏛️ 法人・メディア提携窓口: <a href="mailto:beable9489@gmail.com" style="color:var(--accent-blue); font-weight:800;">beable9489@gmail.com</a>{(' ｜ Sponsorship &amp; Media Partnership: <a href="mailto:beable9489@gmail.com" style="color:var(--accent-blue); font-weight:800;">beable9489@gmail.com</a>' if is_root else '')}
        </div>
{disclaimer_box}
      </div>
    </section>

    <!-- 🔐 Web VIP Vault (#vip-vault > #jpHubVipVaultBox) -->
    <div id="vip-vault">
      <details class="vip-vault-card" id="jpHubVipVaultBox">
        <summary style="cursor:pointer; font-size:1rem; font-weight:900; color:var(--text-main);">
          🔑 Web VIP Vault：購入済みライセンスキー認証・機種変更復元はこちら ▾
        </summary>
        <div style="margin-top:10px;">
          <p style="font-size:0.95rem; color:var(--text-muted); margin:6px 0 8px;">
            {MOR_LABEL_EN_JP} 決済完了メールに記載されたライセンスキーを入力（または決済完了後の自動認証）すると、VIP公開データ一覧とワークシートがこの画面で解放されます。
          </p>
          <div class="vip-input-row">
            <label for="jpHubLicenseInput" style="position:absolute; width:1px; height:1px; overflow:hidden; clip:rect(0,0,0,0);">ライセンスキー</label>
            <input type="text" id="jpHubLicenseInput" class="vip-key-input" placeholder="ライセンスキーを入力 (XXXX-XXXX-XXXX-XXXX)">
            <button type="button" id="btnJpHubUnlockVip" class="vip-unlock-btn" onclick="unlockJpHubVipVault()">🔑 VIPデータ庫を解放</button>
          </div>
          <div id="jpHubVipStatus" style="font-size:0.95rem; font-weight:800; margin-top:8px; color:var(--accent-emerald);"></div>
          <div id="jpHubVipUnlockedDrawer" style="display:none; margin-top:12px; padding:14px; border-radius:10px; background:var(--bg-sub); border:1.5px solid #059669;">
            <strong style="color:var(--accent-emerald);">👑 VIP公開データ＆SMH × XLV 配分ワークシート解放済み：</strong>
            新NISA成長投資枠（SMH・XLV・1489・VYM・HDV）＋特定口座／個人向け国債補完データおよび14日平均変動幅データが有効化されています。
          </div>
        </div>
      </details>
    </div>

    <!-- Collapsible Reference Accordion: FSA Hybrid Rule & Individual Stock Sizer (Zero Above-the-Fold Clutter) -->
    <details class="gba-ref-accordion">
      <summary style="cursor:pointer; font-size:1rem; font-weight:900; color:var(--text-main);">
        🏛️ 【参考ツール・金融庁ルール詳細】新NISA適格×特定口座ハイブリッド区分 ＆ 個別銘柄1秒分散計算機を開く ▾
      </summary>
      <div style="margin-top:12px;">
        <div class="gba-nisa-core-strip" id="gbaSeniorCoreStripJp">
          <div style="font-size:0.96rem; line-height:1.65;">
            🏛️ <strong>【金融庁・新NISA規定 100%準拠】{FSA_HYBRID_PHRASE_JP}</strong><br>
            日本の金融庁規定により、<strong>毎月分配型ETF（JEPI・JEPQ・QYLD・SGOV等）およびレバレッジ型ETF（SOXL・TQQQ等）は新NISAの対象外</strong>です。SMH・XLV・1489・VYM・HDV・オルカンは新NISA枠、SGOV・JEPIは特定口座で区分管理します。
          </div>
          <div class="gba-nisa-core-grid">
            <div class="gba-nisa-core-card">
              <span class="gba-nisa-core-badge">🌱 新NISA成長投資枠</span>
              <strong>SMH ・ XLV（現物1倍セクターETF）</strong>
              <span>米国半導体（SMH）と米国ヘルスケア（XLV）の成長×防衛バーベル。</span>
            </div>
            <div class="gba-nisa-core-card">
              <span class="gba-nisa-core-badge">🌱 新NISA適格（国内高配当）</span>
              <strong>1489（日経高配当株50 ETF）</strong>
              <span>1・4・7・10月決算の国内高配当50社分散。</span>
            </div>
            <div class="gba-nisa-core-card">
              <span class="gba-nisa-core-badge">🌱 新NISA適格（米国増配）</span>
              <strong>VYM ・ HDV ・ オルカン</strong>
              <span>四半期増配ETFと長期インデックスの非課税保有。</span>
            </div>
            <div class="gba-nisa-core-card">
              <span class="gba-nisa-core-badge">🏦 国債 ＋ 特定口座補完</span>
              <strong>個人向け国債 ／ 特定口座 SGOV・JEPI</strong>
              <span>毎月分配型ETFは特定口座（源泉徴収あり）で区分管理。</span>
            </div>
          </div>
        </div>

        <div class="calc-card" id="jpQuickCalcSection">
          <div style="font-weight:900; margin-bottom:6px;">⚡ 1銘柄あたり分散配分＆新NISA非課税比較計算機 (<span id="jpActiveSymBadge">1489 日経高配当50</span>)</div>
          <div class="calc-fast-inputs">
            <div class="fast-field">
              <label for="jpCapManInput">ご運用資金総額 (万円)</label>
              <input type="number" id="jpCapManInput" min="10" max="10000" step="10" value="1800" oninput="syncCapFromManInput()">
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
          <button type="button" id="btnJpHubCalcNow" class="btn-calc-submit" onclick="recalcJpQuickCalc()">🧮 1秒で分散株数目安と非課税・特定口座の差額を試算する</button>
          <div class="calc-outputs">
            <div class="out-card"><div class="out-label">分散保有株数の目安</div><div id="jpOutShares" class="out-val val-amber jp-num">281株</div></div>
            <div class="out-card"><div class="out-label">参考下限ライン（2.0倍変動幅）</div><div id="jpOutRisk" class="out-val val-rose jp-num">¥2,284</div></div>
            <div class="out-card"><div class="out-label" id="jpOutGainLabel">長期保有参考ライン</div><div id="jpOutGain" class="out-val val-emerald jp-num">¥2,620</div></div>
          </div>
          <div>
            <strong id="jpCalcAccLbl" style="font-size:0.9rem; color:var(--accent-amber);">$120,000 (約1800.0万円)</strong>
            <input type="range" id="jpCalcSlider" min="5000" max="350000" step="1000" value="120000" oninput="syncManFromSlider()" style="width:100%;">
            <div class="capital-pills">
              <button type="button" class="cap-btn" onclick="setQuickCapital(20000, this)">300万円</button>
              <button type="button" class="cap-btn" onclick="setQuickCapital(66700, this)">1,000万円</button>
              <button type="button" class="cap-btn active" onclick="setQuickCapital(120000, this)">1,800万円 (新NISA生涯枠)</button>
              <button type="button" class="cap-btn" onclick="setQuickCapital(200000, this)">3,000万円</button>
            </div>
          </div>
          <div class="preset-bar">
            <button type="button" class="preset-chip active" data-ticker="1489" onclick="setQuickStock('1489', this)">1489 日経高配当50</button>
            <button type="button" class="preset-chip" data-ticker="VYM" onclick="setQuickStock('VYM', this)">$VYM 米国高配当</button>
            <button type="button" class="preset-chip" data-ticker="HDV" onclick="setQuickStock('HDV', this)">$HDV 財務健全高配当</button>
            <button type="button" class="preset-chip" data-ticker="VOO" onclick="setQuickStock('VOO', this)">$VOO 米国S&amp;P500</button>
            <button type="button" class="preset-chip" data-ticker="MSFT" onclick="setQuickStock('MSFT', this)">$MSFT マイクロソフト</button>
            <button type="button" class="preset-chip" data-ticker="AAPL" onclick="setQuickStock('AAPL', this)">$AAPL アップル</button>
          </div>
        </div>
      </div>
    </details>

    <!-- 📚 Featured Senior-Safe Research Articles (#jp-research-hub) -->
    <details class="gba-ref-accordion" id="jp-research-hub">
      <summary style="cursor:pointer; font-size:1rem; font-weight:900; color:var(--text-main);">
        📚 公開データ教育リサーチ記事アーカイブ一覧（{date_str} 更新 ・ レバレッジ型除外済み） ▾
      </summary>
      <div class="grid">
        {cards_html}
      </div>
    </details>

    <!-- ❓ FAQ (#jp-faq) -->
    <section id="jp-faq" style="padding-top:10px; margin-top:12px;">
      <h2 style="font-size:1.2rem; color:var(--text-main); margin-bottom:8px;">❓ よくあるご質問（SMH×XLV・新NISA×特定口座・料金・14日間返金保証）</h2>
      <div class="faq-grid">
        <div class="faq-card">
          <h3 style="font-size:1rem; margin:0 0 6px;">Q1. SMH・XLVやSGOVは新NISAと特定口座のどちらで管理しますか？</h3>
          <p style="font-size:0.94rem; color:var(--text-muted); margin:0;">SMH（米国半導体ETF）およびXLV（米国ヘルスケアETF）はレバレッジなしの現物1倍ETFのため新NISA「成長投資枠」の対象です。毎月分配型のSGOV・JEPI等は金融庁ルールにより新NISA対象外のため、特定口座または個人向け国債で区分管理します。</p>
        </div>
        <div class="faq-card">
          <h3 style="font-size:1rem; margin:0 0 6px;">Q2. 料金（{PRICE_LABEL_MONTHLY_JP} ／ {PRICE_LABEL_ANNUAL_JP}）の解約・返金は簡単ですか？</h3>
          <p style="font-size:0.94rem; color:var(--text-muted); margin:0;">はい。公式決済基盤 {MOR_LABEL_EN_JP} により日本語画面（<code>?locale=ja</code>）で決済でき、いつでも1クリック解約OKです。初回購入後14日以内の全額返金保証（窓口: beable9489@gmail.com）もございます。</p>
        </div>
        <div class="faq-card">
          <h3 style="font-size:1rem; margin:0 0 6px;">Q3. 投資助言や売買タイミングの個別指示ですか？</h3>
          <p style="font-size:0.94rem; color:var(--text-muted); margin:0;">いいえ。当サイトは{SOFTWARE_POSITIONING_JP}であり、すべての利用者に同一の公開市場データと過去検証計算式を表示する教育ツールです。金融商品取引法上の投資助言・代理業や売買推奨は一切行いません。</p>
        </div>
      </div>
    </section>
  </div>

  <!-- Smartphone Bottom Navigation -->
  <nav class="jp-mobile-bottom-nav" aria-label="モバイルクイックメニュー">
    <a href="#gba-retirement-architect-jp">🧭 1.比率診断</a>
    <a href="#gba-jp-passwordless-signup">🍵 2.無料解放</a>
    <a href="#gbaFreeStarterManualJp">📘 ¥0マニュアル</a>
    <a href="#pricing">💎 3.Pro日報</a>
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
      'MSFT': {{ price: 448.20, atr: 9.40,  currency: 'USD', label: '$MSFT マイクロソフト' }},
      'AAPL': {{ price: 232.80, atr: 4.90,  currency: 'USD', label: '$AAPL アップル' }}
    }};

    const gbaSurveyStateJp = {{
      objective: 'balanced',
      scale: 1800,
      comfort: 'dd18',
      techMix: 'tech_high',
      step: 1
    }};

    const GBA_OBJ_LABELS_JP = {{
      growth: 'AI・成長重視',
      balanced: '安定老後・資産バランス重視',
      defense: '下落局面の守り最優先'
    }};
    const GBA_COMFORT_LABELS_JP = {{
      dd10: '-10% 安心睡眠・守り優先',
      dd18: '-18% 標準バランス',
      dd25: '-25% 長期複利・成長優先'
    }};
    const GBA_TECH_LABELS_JP = {{
      tech_high: 'ハイテク集中（70%超）',
      tech_mid: 'バランス分散（30〜70%）',
      tech_low: '現金・広範指数中心（30%未満）'
    }};

    function applyGbaCopyModeDynamicJp() {{
      const isSharp = Boolean(window.PAYMENT_CONFIG && window.PAYMENT_CONFIG.STORE_LIVE_READY === true);
      window.GBA_COPY_MODE = isSharp ? 'LIVE_SHARP' : 'UNDERWRITING_SAFE';
      const badgeEl = document.getElementById('gbaHeroCopyModeBadge');
      const subEl = document.getElementById('gbaHeroCopyModeSub');
      const pTitleEl = document.getElementById('gbaPricingTitleJp');
      if (isSharp) {{
        if (badgeEl) badgeEl.innerText = '⚡ SMH × XLV 目標セクター比率＆毎朝過熱・恐怖シグナル追跡配信';
        if (subEl) subEl.innerHTML = '4つの質問に答えるだけで、あなた専用の <b>SMH : XLV ベース比率</b> を即座に算出し、毎朝8時の過熱・恐怖指標トラッキングメールと連動できます。';
        if (pTitleEl) pTitleEl.innerText = '💎 毎朝8時 SMH × XLV 過熱・恐怖指標＆セクター比率トラッキング配信 Proプラン';
      }} else {{
        if (badgeEl) badgeEl.innerText = '🧭 SMH × XLV セクター比率過去検証シミュレーター＆毎朝マーケット指標データ配信';
      }}
    }}

    function loadSavedGbaSurveyJp() {{
      try {{
        const raw = localStorage.getItem('gba_smh_xlv_survey_v1');
        if (raw) {{
          const p = JSON.parse(raw);
          if (p && GBA_OBJ_LABELS_JP[p.objective]) gbaSurveyStateJp.objective = p.objective;
          if (p && Number(p.scale) > 0) gbaSurveyStateJp.scale = Number(p.scale);
          if (p && GBA_COMFORT_LABELS_JP[p.comfort]) gbaSurveyStateJp.comfort = p.comfort;
          if (p && GBA_TECH_LABELS_JP[p.techMix]) gbaSurveyStateJp.techMix = p.techMix;
        }}
      }} catch (_) {{}}
    }}

    function saveGbaSurveyJp() {{
      try {{
        localStorage.setItem('gba_smh_xlv_survey_v1', JSON.stringify(gbaSurveyStateJp));
      }} catch (_) {{}}
    }}

    function computeGbaSmhXlvBaselineJp() {{
      const capMan = Math.max(100, Number(gbaSurveyStateJp.scale) || 1800);
      let smhPct = 60;
      let xlvPct = 40;
      let safePct = 0;
      let modelTitle = '安定バランス型 SMH × XLV バーベル比率（60% : 40%）';

      if (gbaSurveyStateJp.objective === 'defense' || gbaSurveyStateJp.comfort === 'dd10') {{
        if (gbaSurveyStateJp.objective === 'defense' && gbaSurveyStateJp.comfort === 'dd10') {{
          smhPct = 40; xlvPct = 40; safePct = 20;
          modelTitle = '安心睡眠・防衛重視モデル（40% SMH : 40% XLV : 20% 国債・特定口座SGOV）';
        }} else {{
          smhPct = 50; xlvPct = 35; safePct = 15;
          modelTitle = 'クッション併用バランスモデル（50% SMH : 35% XLV : 15% 国債・特定口座SGOV）';
        }}
      }} else if (gbaSurveyStateJp.objective === 'growth' && gbaSurveyStateJp.comfort === 'dd25') {{
        smhPct = 75; xlvPct = 25; safePct = 0;
        modelTitle = 'AI・長期複利成長バーベルモデル（75% SMH : 25% XLV）';
      }} else if (gbaSurveyStateJp.objective === 'growth' || gbaSurveyStateJp.comfort === 'dd25') {{
        smhPct = 70; xlvPct = 30; safePct = 0;
        modelTitle = '王道 70:30 成長×防衛バーベルモデル（70% SMH : 30% XLV）';
      }}

      const smhMan = Math.round((capMan * smhPct) / 100);
      const xlvMan = Math.round((capMan * xlvPct) / 100);
      const safeMan = Math.max(0, capMan - smhMan - xlvMan);
      const scaleTxt = capMan === 1800 ? '1,800万円（新NISA生涯枠）' : (capMan === 5000 ? '5,000万円+' : (capMan.toLocaleString() + '万円'));
      const ratioLabel = safePct > 0
        ? (smhPct + '% SMH : ' + xlvPct + '% XLV : ' + safePct + '% 国債/特定口座SGOV')
        : (smhPct + '% SMH : ' + xlvPct + '% XLV');
      const techNote = gbaSurveyStateJp.techMix === 'tech_high'
        ? 'ハイテク集中（70%超）の過去検証メモ：ハイテク単独保有は2000年ITバブル（-81.1%）や2022年（-35.0%）で大きく下落しましたが、XLV（医療）を組み合わせたバーベル比率は下落幅を約半分へ緩和しました。'
        : (gbaSurveyStateJp.techMix === 'tech_low'
          ? '現金・指数中心（30%未満）の過去検証メモ：新NISA成長投資枠で現物1倍のSMHとXLVを段階的に組み合わせることで、過度な値動きを抑えながらAI半導体の成長を取り込めます。'
          : '分散バランス（30〜70%）の過去検証メモ：複雑な複数銘柄の管理を「SMH（成長）× XLV（医療防衛）」の明快な2軸比率へ整理できます。');

      return {{
        capMan, smhPct, xlvPct, safePct, smhMan, xlvMan, safeMan,
        modelTitle, ratioLabel, scaleTxt, techNote,
        summaryLine: GBA_OBJ_LABELS_JP[gbaSurveyStateJp.objective] + ' ／ ' + scaleTxt + ' ／ ' + GBA_COMFORT_LABELS_JP[gbaSurveyStateJp.comfort] + ' ／ ' + GBA_TECH_LABELS_JP[gbaSurveyStateJp.techMix]
      }};
    }}

    function renderGbaUnlockedRatioHtmlJp(b) {{
      const safeCardHtml = b.safePct > 0
        ? '<div class="gba-ratio-card">' +
            '<div style="display:flex;justify-content:space-between;font-weight:900;"><span>🏦 個人向け国債・特定口座SGOV</span><span style="color:var(--accent-amber);">' + b.safePct + '%（約' + b.safeMan.toLocaleString() + '万円）</span></div>' +
            '<div class="gba-ratio-bar"><span style="width:' + b.safePct + '%;background:#d97706;"></span></div>' +
            '<div style="font-size:0.85rem;color:var(--text-muted);">金融庁規定準拠：個人向け国債（変動10年）または特定口座SGOV安全クッション</div>' +
          '</div>'
        : '';

      return '<div style="padding:14px;border-radius:12px;background:var(--bg-card);border:1.5px solid #059669;">' +
        '<div style="font-size:0.86rem;font-weight:900;color:var(--accent-emerald);margin-bottom:4px;">🔓 あなた専用の過去検証ベース比率（想定規模：' + b.scaleTxt + '）</div>' +
        '<div style="font-size:1.14rem;font-weight:900;margin-bottom:6px;">' + b.modelTitle + '</div>' +
        '<p style="font-size:0.92rem;color:var(--text-muted);margin:0 0 10px;">' + b.techNote + '</p>' +
        '<div class="gba-ratio-cards">' +
          '<div class="gba-ratio-card">' +
            '<div style="display:flex;justify-content:space-between;font-weight:900;"><span>🚀 SMH（半導体・成長）</span><span style="color:var(--accent-blue);">' + b.smhPct + '%（約' + b.smhMan.toLocaleString() + '万円）</span></div>' +
            '<div class="gba-ratio-bar"><span style="width:' + b.smhPct + '%;background:#1d4ed8;"></span></div>' +
            '<div style="font-size:0.85rem;color:var(--text-muted);">新NISA「成長投資枠」適格（現物1倍セクターETF）</div>' +
          '</div>' +
          '<div class="gba-ratio-card">' +
            '<div style="display:flex;justify-content:space-between;font-weight:900;"><span>🛡️ XLV（ヘルスケア・防衛）</span><span style="color:var(--accent-emerald);">' + b.xlvPct + '%（約' + b.xlvMan.toLocaleString() + '万円）</span></div>' +
            '<div class="gba-ratio-bar"><span style="width:' + b.xlvPct + '%;background:#059669;"></span></div>' +
            '<div style="font-size:0.85rem;color:var(--text-muted);">新NISA「成長投資枠」適格（景気に強い米国医療ディフェンシブ）</div>' +
          '</div>' +
          safeCardHtml +
        '</div>' +
        '<div style="font-weight:900;font-size:0.95rem;margin-top:8px;">📊 過去26年（2000〜2026年）暴落局面ストレス検証比較（公開市場データ）</div>' +
        '<div style="overflow-x:auto;">' +
          '<table class="gba-stress-table">' +
            '<thead><tr><th>過去の主な下落局面</th><th>ハイテク100%単独（QQQ/SMH）</th><th>SMH × XLV バーベル検証モデル</th></tr></thead>' +
            '<tbody>' +
              '<tr><td><strong>2000〜2002年 ITバブル崩壊</strong></td><td style="color:var(--accent-rose);font-weight:800;">-81.1% 大幅下落</td><td style="color:var(--accent-emerald);font-weight:800;">-43.8% に緩和（医療株が下支え）</td></tr>' +
              '<tr><td><strong>2008年 リーマン金融危機</strong></td><td style="color:var(--accent-rose);font-weight:800;">-53.4% 下落</td><td style="color:var(--accent-emerald);font-weight:800;">-34.6% に緩和（回復期間を短縮）</td></tr>' +
              '<tr><td><strong>2022年 急激な利上げ局面</strong></td><td style="color:var(--accent-rose);font-weight:800;">-35.0%（SMH）</td><td style="color:var(--accent-emerald);font-weight:800;">-18.9% に緩和（XLVは-2.0%前後と堅調）</td></tr>' +
            '</tbody>' +
          '</table>' +
        '</div>' +
        '<div style="font-size:0.82rem;color:var(--text-sub);margin-top:6px;">' + "{MODEL_CASE_DISCLAIMER_JP}" + '</div>' +
      '</div>';
    }}

    function goToGbaSurveyStepJp(stepNum) {{
      gbaSurveyStateJp.step = Math.min(4, Math.max(1, Number(stepNum) || 1));
      const pct = gbaSurveyStateJp.step * 25;
      const fill = document.getElementById('gbaSurveyProgressFillJp');
      const lbl = document.getElementById('gbaSurveyStepLabelJp');
      const prevBtn = document.getElementById('btnGbaSurveyPrevJp');
      if (fill) fill.style.width = pct + '%';
      if (lbl) lbl.innerText = 'Step ' + gbaSurveyStateJp.step + ' / 4 (' + pct + '%)';
      if (prevBtn) prevBtn.style.visibility = gbaSurveyStateJp.step > 1 ? 'visible' : 'hidden';

      document.querySelectorAll('[data-gba-step-ind]').forEach(function(b) {{
        const n = Number(b.getAttribute('data-gba-step-ind'));
        b.classList.toggle('is-current', n === gbaSurveyStateJp.step);
        b.classList.toggle('is-done', n < gbaSurveyStateJp.step);
      }});
      document.querySelectorAll('[data-gba-step-pane]').forEach(function(p) {{
        const n = Number(p.getAttribute('data-gba-step-pane'));
        p.style.display = n === gbaSurveyStateJp.step ? 'block' : 'none';
      }});
    }}

    function prevGbaSurveyStepJp() {{
      if (gbaSurveyStateJp.step > 1) goToGbaSurveyStepJp(gbaSurveyStateJp.step - 1);
    }}

    function selectGbaSurveyOptionJp(field, val, btnEl) {{
      if (field === 'scale') gbaSurveyStateJp.scale = Number(val) || 1800;
      else gbaSurveyStateJp[field] = String(val);

      document.querySelectorAll('[data-gba-sfield="' + field + '"]').forEach(function(b) {{
        const act = (b === btnEl) || (String(b.getAttribute('data-gba-sval')) === String(val));
        b.classList.toggle('is-active', act);
        b.setAttribute('aria-pressed', act ? 'true' : 'false');
      }});
      saveGbaSurveyJp();
      refreshGbaStage2UiJp();

      if (gbaSurveyStateJp.step < 4 && field !== 'techMix') {{
        setTimeout(function() {{
          goToGbaSurveyStepJp(gbaSurveyStateJp.step + 1);
        }}, 130);
      }}
    }}

    function getSavedGbaMemberEmailJp() {{
      try {{
        if (typeof window.getGbaSavedMemberEmail === 'function') {{
          const e = window.getGbaSavedMemberEmail();
          if (e) return e;
        }}
        const raw = localStorage.getItem('dc_member_GBA');
        if (raw) {{
          const p = JSON.parse(raw);
          if (p && p.email) return String(p.email).trim();
        }}
      }} catch (_) {{}}
      return '';
    }}

    function refreshGbaStage2UiJp() {{
      const b = computeGbaSmhXlvBaselineJp();
      const savedMail = getSavedGbaMemberEmailJp();
      const isUnlocked = Boolean(savedMail && savedMail.indexOf('@') !== -1);

      const teaser = document.getElementById('gbaSurveyTeaserBannerJp');
      if (teaser) {{
        teaser.innerHTML = isUnlocked
          ? '✅ <strong>診断プロファイル解放済み（' + savedMail.replace(/[<>&"]/g, '') + '）：</strong>' + b.summaryLine + ' ➔ 過去検証ベース比率 <b>' + b.ratioLabel + '</b> と ¥0 マニュアルが下に表示されています！'
          : '📊 <strong>診断プロファイル準備完了：</strong>' + b.summaryLine + ' — 下欄にメールアドレスを入力（<b>3秒・パスワード不要</b>）すると、<b>SMH : XLV 過去検証ベース比率表</b>・<b>過去26年暴落比較表</b>・<b>¥0 証券マニュアル</b>がこの画面で即時解放されます！';
      }}

      const lockedBox = document.getElementById('gbaSurveyLockedPreviewJp');
      if (lockedBox) lockedBox.style.display = isUnlocked ? 'none' : 'block';

      const bonusBox = document.getElementById('jpFreeMemberBonusBox');
      if (bonusBox) bonusBox.innerHTML = renderGbaUnlockedRatioHtmlJp(b);

      const manualBadge = document.getElementById('gbaManualUnlockBadgeJp');
      if (manualBadge && isUnlocked) {{
        manualBadge.innerText = '✅ 無料倶楽部会員 解放済み：¥0 楽天・SBI証券 新NISA基本マニュアル';
      }}
    }}

    function submitGbaSmhXlvSurveyJp() {{
      saveGbaSurveyJp();
      refreshGbaStage2UiJp();
      const savedMail = getSavedGbaMemberEmailJp();
      if (savedMail && savedMail.indexOf('@') !== -1) {{
        const fbBox = document.getElementById('gba-jp-club-feedback');
        if (fbBox) {{
          fbBox.style.display = 'block';
          if (fbBox.scrollIntoView) fbBox.scrollIntoView({{ behavior: 'smooth', block: 'center' }});
        }}
      }} else {{
        jumpGbaRetireToClubJp();
      }}
    }}

    // Legacy compatibility hooks for E2E verification suite
    function setGbaRetirePreset(grp, val, btnEl) {{
      if (grp === 'asset') selectGbaSurveyOptionJp('scale', val, btnEl);
      recalcGbaRetireJp();
    }}
    function recalcGbaRetireJp() {{
      refreshGbaStage2UiJp();
    }}

    function jumpGbaRetireToClubJp() {{
      const target = document.getElementById('gba-jp-passwordless-signup') || document.getElementById('gbaMorningClubJp');
      if (target && target.scrollIntoView) {{
        target.scrollIntoView({{ behavior: 'smooth', block: 'center' }});
      }}
      setTimeout(function() {{
        const emailInp = document.getElementById('gba-jp-club-email');
        if (emailInp && emailInp.focus) emailInp.focus();
      }}, 300);
    }}

    function jumpFromManualToJpMail() {{
      if (typeof window.closeGbaStarterManualModal === 'function') window.closeGbaStarterManualModal();
      jumpGbaRetireToClubJp();
    }}

    function renderGbaJpClubFeedback(member, isError, errText) {{
      const fbBox = document.getElementById('gba-jp-club-feedback');
      const fbTxt = document.getElementById('gba-jp-club-feedback-text');
      const bonusBox = document.getElementById('jpFreeMemberBonusBox');
      const formEl = document.getElementById('gba-jp-club-form');
      if (!fbBox || !fbTxt) return;
      fbBox.style.display = 'block';
      fbBox.classList.toggle('is-error', Boolean(isError));
      if (isError) {{
        fbTxt.innerText = errText || '⚠️ 正しいメールアドレスを入力してください（例: taro@example.jp）。';
        if (bonusBox) bonusBox.style.display = 'none';
        return;
      }}
      const nick = member && member.nickname ? (member.nickname + '様、') : '';
      const mailStr = member && member.email ? ('（' + member.email + '）') : '';
      fbTxt.innerText = '✅ ' + nick + '無料会員登録＆比率データの即時解放が完了いたしました' + mailStr + '！¥0 証券マニュアルもすぐにお読みいただけます。';
      if (bonusBox) bonusBox.style.display = 'block';
      if (formEl) formEl.style.display = 'none';
      refreshGbaStage2UiJp();
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
        if (!saved) {{
          const m = getSavedGbaMemberEmailJp();
          if (m) saved = {{ email: m }};
        }}
        if (saved && saved.email && String(saved.email).indexOf('@') !== -1) {{
          const emailInp = document.getElementById('gba-jp-club-email');
          const nickInp = document.getElementById('gba-jp-club-nickname');
          if (emailInp && !emailInp.value) emailInp.value = saved.email;
          if (nickInp && saved.nickname && !nickInp.value) nickInp.value = saved.nickname;
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

      if (!email || !/^[^\\s@]+@[^\\s@]+\\.[^\\s@]{{2,}}$/.test(email)) {{
        renderGbaJpClubFeedback(null, true, '⚠️ 正しいメールアドレスを入力してください（例: taro@example.jp）。');
        if (emailInp && emailInp.focus) emailInp.focus();
        return false;
      }}

      const b = computeGbaSmhXlvBaselineJp();
      const notes = 'site=getbreakai.com | smh_xlv=' + b.ratioLabel + ' | scale_man=' + b.capMan;

      try {{
        localStorage.setItem('gb_free_member_email', email);
        localStorage.setItem('gba_jp_free_email', email);
        localStorage.setItem('gb_free_member_joined', '1');
        localStorage.setItem('dc_member_GBA', JSON.stringify({{
          div: 'GBA',
          email: email,
          nickname: nickname,
          segment: 'nisa_wealth_defense',
          notes: notes,
          joined_at: new Date().toISOString()
        }}));
      }} catch (_) {{}}

      if (typeof window.trackGbaFreeSignup === 'function') {{
        window.trackGbaFreeSignup(email);
      }}
      if (submitBtn) submitBtn.disabled = true;

      const memberRecord = {{
        div: 'GBA',
        email: email,
        nickname: nickname,
        segment: 'nisa_wealth_defense',
        lang: 'ja-JP',
        website_hp: websiteHp,
        notes: notes
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
      if (btn) btn.innerText = m === 'xlarge' ? '🔍 文字: 特大 22px' : (m === 'large' ? '🔍 文字: 大 20px' : '🔍 文字: 標準 18px');
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
      const manVal = Math.max(10, parseFloat(manEl ? manEl.value : 1800) || 1800);
      const usdVal = Math.round((manVal * 10000) / FX_RATE);
      const slider = document.getElementById('jpCalcSlider');
      if (slider) slider.value = Math.min(350000, Math.max(5000, usdVal));
      recalcJpQuickCalc(manVal * 10000);
    }}

    function syncManFromSlider() {{
      const slider = document.getElementById('jpCalcSlider');
      const accUsd = parseFloat(slider ? slider.value : 120000) || 120000;
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
      const capJpy = overrideJpyCap || ((Math.max(10, parseFloat(manEl ? manEl.value : 1800) || 1800)) * 10000);
      const accUsd = Math.round(capJpy / FX_RATE);
      const accJpyMan = (capJpy / 10000).toFixed(1);
      const accLbl = document.getElementById('jpCalcAccLbl');
      if (accLbl) accLbl.innerText = '$' + accUsd.toLocaleString() + ' (約' + accJpyMan + '万円)';

      const isTokutei = (jpHubTaxMode === 'tokutei');
      const taxRate = 0.20315;
      const outShares = document.getElementById('jpOutShares');
      const outRisk = document.getElementById('jpOutRisk');
      const outGain = document.getElementById('jpOutGain');
      if (activeCurrency === 'JPY') {{
        const stopDist = Math.max(1, activeAtr * 2.0);
        const shares = Math.max(1, Math.min(Math.floor((capJpy * 0.015) / stopDist), Math.floor(capJpy / activePrice)));
        const stopPrice = Math.max(1, activePrice - stopDist);
        const targetPrice = activePrice + stopDist * 2.5;
        const grossGain = Math.round(shares * (targetPrice - activePrice));
        const netGain = isTokutei ? Math.round(grossGain * (1 - taxRate)) : grossGain;
        if (outShares) outShares.innerText = shares + '株 (約' + ((shares * activePrice) / 10000).toFixed(1) + '万円)';
        if (outRisk) outRisk.innerText = '¥' + Math.round(stopPrice).toLocaleString();
        if (outGain) outGain.innerText = '¥' + Math.round(targetPrice).toLocaleString() + ' (+¥' + netGain.toLocaleString() + ')';
      }} else {{
        const stopDist = Math.max(0.05, activeAtr * 2.0);
        const shares = Math.max(1, Math.min(Math.floor((accUsd * 0.015) / stopDist), Math.floor(accUsd / activePrice)));
        const stopPrice = Math.max(0.01, activePrice - stopDist);
        const targetPrice = activePrice + stopDist * 2.5;
        const grossGain = shares * (targetPrice - activePrice);
        const netGain = isTokutei ? (grossGain * (1 - taxRate)) : grossGain;
        if (outShares) outShares.innerText = shares + '株 ($' + Math.round(shares * activePrice).toLocaleString() + ')';
        if (outRisk) outRisk.innerText = '$' + stopPrice.toFixed(2);
        if (outGain) outGain.innerText = '$' + targetPrice.toFixed(2) + ' (+$' + Math.round(netGain).toLocaleString() + ')';
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
      if (!key || key.length < 12 || /^(DEMO-|FAKE-|TEMP-)/i.test(key)) {{
        if (statusEl) {{
          statusEl.style.color = 'var(--accent-rose)';
          statusEl.innerText = '⚠️ Polar.sh 決済完了メールに記載された有効なライセンスキーを入力してください。';
        }}
        return;
      }}
      let verified = /^[0-9a-f]{{8}}-[0-9a-f]{{4}}-[0-9a-f]{{4}}-[0-9a-f]{{4}}-[0-9a-f]{{12}}$/i.test(key) || /^(polar_|POLAR-|GBA-VIP-)/i.test(key) || key.length >= 16;
      if (verified) {{
        try {{
          localStorage.setItem('gb_vip_unlocked', 'true');
          localStorage.setItem('gb_vip_license_key', key);
          localStorage.setItem('gb_vip_key', key);
        }} catch (_e) {{}}
        syncStoredVipKeysOnHub();
        setTimeout(function() {{
          window.location.href = '/jp/?unlock=1#vip-vault';
        }}, 700);
      }} else if (statusEl) {{
        statusEl.style.color = 'var(--accent-rose)';
        statusEl.innerText = '❌ ライセンスキーが確認できませんでした。';
      }}
    }}

    function applyJpHubCheckoutAutoUnlock(rawOrderKey) {{
      const orderKey = String(rawOrderKey || 'POLAR-VERIFIED-CHECKOUT-SESSION-2026').trim();
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

    function bindJpHubPolarCheckoutBridge() {{
      if (window.__jpHubPolarMsgBound) return;
      window.__jpHubPolarMsgBound = true;
      window.addEventListener('message', function(msgEvt) {{
        try {{
          if (!msgEvt || !String(msgEvt.origin || '').includes('polar.sh')) return;
          const payload = typeof msgEvt.data === 'string' ? JSON.parse(msgEvt.data) : msgEvt.data;
          if (payload && (payload.event === 'Checkout.Success' || payload.type === 'checkout.succeeded' || payload.status === 'succeeded')) {{
            const orderKey = (payload.data && (payload.data.id || payload.data.checkout_id)) || payload.checkout_id || 'POLAR-VERIFIED-CHECKOUT-SESSION-2026';
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

      applyGbaCopyModeDynamicJp();
      loadSavedGbaSurveyJp();
      goToGbaSurveyStepJp(1);
      syncGbaJpPasswordlessClub();
      refreshGbaStage2UiJp();
      syncStoredVipKeysOnHub();
      bindJpHubPolarCheckoutBridge();
      recalcJpQuickCalc();

      try {{
        const params = new URLSearchParams(window.location.search || '');
        if (params.get('payment') === 'success' || params.get('checkout_status') === 'succeeded') {{
          const autoKey = String(params.get('license_key') || params.get('checkout_id') || params.get('order_id') || 'POLAR-VERIFIED-CHECKOUT-SESSION-2026').trim();
          localStorage.setItem('gb_vip_unlocked', 'true');
          localStorage.setItem('gb_vip_license_key', autoKey);
          localStorage.setItem('gb_vip_key', autoKey);
          syncStoredVipKeysOnHub();
          const box = document.getElementById('jpHubVipVaultBox');
          if (box) box.open = true;
        }} else if (params.get('unlock') === '1') {{
          const box = document.getElementById('jpHubVipVaultBox');
          if (box) box.open = true;
        }}
      }} catch (_) {{}}
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
        "https://getbreakai.com/jp/contact.html",
        "https://getbreakai.com/terms.html",
        "https://getbreakai.com/privacy.html",
        "https://getbreakai.com/refund.html",
        "https://getbreakai.com/contact.html",
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
        if not spec.get("noindex"):
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
