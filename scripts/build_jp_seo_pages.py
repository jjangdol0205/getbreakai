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
    WHOP_MONTHLY_CTA_HREF,
    WHOP_ANNUAL_CTA_HREF,
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
        "title": "エヌビディア(NVDA) 米SEC公式決算開示（Form 8-K/10-Q）と半導体セクター分散データ解析",
        "focus": "次世代AIデータセンター需要に関する米SEC公式決算開示（Form 8-K/10-Q）の要約と、1銘柄集中を避けSMH×XLVセクター分散で保有するリスク管理視点",
        "catalyst_type": "米SEC公式決算開示（Form 8-K）＆ 機関投資家の長期保有動向",
        "entry": 186.64, "atr": 8.02, "iv": 68, "score": 93.5, "dp": "61.4%", "call_ratio": "安定推移",
        "noindex": True
    },
    {
        "slug": "pltr-insider-buying-analysis.html",
        "ticker": "PLTR",
        "jp_name": "パランティア(PLTR)",
        "title": "パランティア(PLTR) SEC Form-4公開データ・長期契約開示とセクター分散比率の整理",
        "focus": "米国公共・民間向けAI基盤契約の米SEC公式決算開示（Form 8-K/10-Q）と、大口機関投資家の保有比率64%に基づく長期ポートフォリオ比較",
        "catalyst_type": "米SEC公式適時開示（Form 8-K）＆ 機関投資家の長期保有動向",
        "entry": 160.38, "atr": 9.95, "iv": 74, "score": 91.0, "dp": "64.2%", "call_ratio": "安定推移"
    },
    {
        "slug": "tsla-gamma-wall-swing-trade.html",
        "ticker": "TSLA",
        "jp_name": "テスラ(TSLA)",
        "title": "テスラ(TSLA) 米SEC事業開示データと高変動個別株のリスク比較ガイド",
        "focus": "自動運転・エネルギー貯蔵部門の米SEC公式決算開示（Form 8-K/10-Q）と、老後コア資産（SMH×XLV＋個人向け国債）と高変動個別株を区別する基礎知識",
        "catalyst_type": "事業セグメント決算開示 ＆ 価格変動幅リスク比較",
        "entry": 358.22, "atr": 17.99, "iv": 82, "score": 89.7, "dp": "58.1%", "call_ratio": "高変動注意",
        "noindex": True
    },
    {
        "slug": "soxl-smh-semiconductor-timing.html",
        "ticker": "SMH",
        "terminal_ticker": "SMH",
        "jp_name": "3倍レバレッジETF（SOXL等・新NISA対象外）",
        "title": "【新NISA対象外・老後資金注意喚起】3倍レバレッジETF（SOXL等）の減価リスクと「SMH × XLV 2本柱」への切り替え解説",
        "focus": "金融庁規定により3倍レバレッジ型ETF（SOXL・TQQQ等）が新NISA対象外となる理由、日々の複利計算による減価リスク、および新NISA成長投資枠の現物1倍2本柱（SMH × XLV）＋個人向け国債（変動10年）への安全な切り替え解説",
        "catalyst_type": "新NISA対象外・老後資金注意喚起 ＆ 3倍レバレッジ減価リスク教育解説",
        "entry": 258.40, "atr": 5.80, "iv": 24, "score": 18.0, "dp": "高変動減価注意", "call_ratio": "対象外区分",
        "is_non_nisa_edu": True,
        "is_leveraged_warning": True,
        "noindex": True
    },
    {
        "slug": "smci-accounting-risk-warning.html",
        "ticker": "SMCI",
        "jp_name": "スーパー・マイクロ(SMCI)",
        "title": "スーパー・マイクロ(SMCI) 米SEC年次報告書（Form 10-K）公開リスク注記とセクターETF分散の重要性",
        "focus": "米SEC年次報告書（Form 10-K）における監査・内部統制関連の公開注記確認ポイントと、個別株リスクを避け現物セクターETF（SMH）で分散する客観的リサーチ解説",
        "catalyst_type": "公開財務開示（Form 10-K）高変動リスク指標の確認ケーススタディ",
        "entry": 28.76, "atr": 2.56, "iv": 96, "score": 28.5, "dp": "67.0%（売り越し比率）", "call_ratio": "高変動注意",
        "is_avoid": True
    },
    {
        "slug": "shin-nisa-us-stock-atr-risk-management.html",
        "ticker": "SMH",
        "terminal_ticker": "SMH",
        "jp_name": "新NISA成長投資枠（SMH × XLV）＋個人向け国債 2本柱配分設計",
        "title": "新NISA成長投資枠「米国半導体（SMH）×米国医療（XLV）」＋個人向け国債（変動10年）2本柱・老後資産配分ガイド",
        "focus": "年間360万円・生涯1,800万円の非課税枠を大切にする年2回の穏やかな比率点検と、金融庁規定に準拠した新NISA成長投資枠（SMH × XLV 現物1倍2本柱）＋個人向け国債（変動10年）／特定口座SGOVの安全資産設計",
        "catalyst_type": "金融庁ルール準拠 新NISA（SMH × XLV）＋個人向け国債 2本柱設計",
        "entry": 258.40, "atr": 5.80, "iv": 24, "score": 96.0, "dp": "26年検証済", "call_ratio": "現物1倍",
        "is_guide": True,
        "is_flagship_nisa_guide": True
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
        "title": "AMD データセンター部門の米SEC売上開示と半導体ETF（SMH）分散比較",
        "focus": "エンタープライズ・クラウド向けAI半導体部門の売上推移データと、1銘柄集中を避け半導体ETF（SMH）と医療ETF（XLV）で分散する意義",
        "catalyst_type": "データセンター売上開示（Form 10-Q）＆ セクター分散研究",
        "entry": 449.04, "atr": 38.02, "iv": 64, "score": 86.2, "dp": "57.2%", "call_ratio": "安定推移",
        "noindex": True
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
        "focus": "暗号資産関連の財務開示（Form 8-K）に伴う年率100%超の価格変動リスク統計と、50〜70代の老後コア資産（SMH × XLV ＋ 個人向け国債）から厳格に分離すべき数学的理由",
        "catalyst_type": "高ボラティリティ統計ケーススタディ ＆ 資産保全リスク教育",
        "entry": 128.93, "atr": 9.75, "iv": 108, "score": 65.0, "dp": "53.2%", "call_ratio": "高変動注意",
        "is_non_nisa_edu": True,
        "noindex": True
    },
    {
        "slug": "arm-royalty-expansion-gamma-wall.html",
        "ticker": "ARM",
        "jp_name": "アーム(ARM)",
        "title": "アーム(ARM) 半導体設計ロイヤルティ収入の公開決算データとセクター分散分析",
        "focus": "Armv9世代への移行に伴うロイヤルティ収入・ライセンス売上の米SEC公開決算データと、半導体セクターETF（SMH）との比較",
        "catalyst_type": "ロイヤルティ収益開示データ ＆ 公開市場統計分析",
        "entry": 174.62, "atr": 14.23, "iv": 76, "score": 86.0, "dp": "56.0%", "call_ratio": "安定推移",
        "noindex": True
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
        "ticker": "SMH",
        "terminal_ticker": "SMH",
        "jp_name": "米SEC公式決算開示（Form 8-K）日本語基礎ガイド",
        "title": "米SEC公式適時開示（Form 8-K/10-Q）とは？英語の一次財務情報をやさしく読み解く基礎マニュアル",
        "focus": "日本の個人投資家が知っておきたい米SEC EDGAR公式開示（重要契約Item 1.01・決算発表Item 2.02等）の基本構造と公開データの確認手順",
        "catalyst_type": "米SEC公開財務データ（EDGAR）基礎教育マニュアル",
        "entry": 258.40, "atr": 5.80, "iv": 24, "score": 91.5, "dp": "EDGAR一次開示", "call_ratio": "基礎教養",
        "is_guide": True
    },
    {
        "slug": "form4-insider-cluster-guide.html",
        "ticker": "XLV",
        "jp_name": "SEC Form-4 公開自社株取得データの読み方",
        "title": "米国株SEC Form-4（役員の自社株取得開示）とは？公開データの見方と注意点をやさしく解説",
        "focus": "ストックオプション自動売却（10b5-1計画）と純粋な市場内自社株取得（Code P）の違いを客観的に整理する米SEC公開データ教育ガイド",
        "catalyst_type": "SEC Form-4 公開内部者取引統計の基礎知識",
        "entry": 148.90, "atr": 2.40, "iv": 18, "score": 89.8, "dp": "Form-4公開統計", "call_ratio": "基礎教養",
        "is_guide": True
    },
    {
        "slug": "options-gamma-squeeze-gex-guide.html",
        "ticker": "SMH",
        "jp_name": "公開市場の予想変動幅（IV統計）基礎解説",
        "title": "米国株市場の予想変動幅（インプライド・ボラティリティ統計）と長期保有の基礎知識",
        "focus": "公開市場統計から算出される予想変動レンジの意味と、新NISA長期投資家が決算前後の短期値動きに慌てないための基礎教養",
        "catalyst_type": "公開市場ボラティリティ統計 ＆ 長期保有基礎教育",
        "entry": 258.40, "atr": 5.80, "iv": 24, "score": 90.0, "dp": "公開変動統計", "call_ratio": "基礎教養",
        "is_guide": True,
        "noindex": True
    },
    {
        "slug": "fomc-cpi-iv-crush-strategy.html",
        "ticker": "SMH",
        "terminal_ticker": "SMH",
        "jp_name": "FOMC・米CPI発表と日米金利・為替の基礎知識",
        "title": "FOMC政策金利・米CPI発表がドル円為替と新NISA（SMH × XLV）資産配分に与える影響の基礎ガイド",
        "focus": "米国連邦準備制度（FRB）の金利決定やインフレ統計（CPI）の公開日程と、年2回の穏やかな SMH × XLV ＋ 個人向け国債比率点検における確認ポイント",
        "catalyst_type": "日米マクロ金利・為替統計 ＆ 老後資産配分教育ガイド",
        "entry": 258.40, "atr": 5.80, "iv": 24, "score": 92.0, "dp": "日米マクロ統計", "call_ratio": "年2回点検",
        "is_guide": True,
        "noindex": True
    },
    {
        "slug": "tradingview-pine-script-v5-atr-guide.html",
        "ticker": "SMH",
        "terminal_ticker": "SMH",
        "jp_name": "TradingView移動平均線・セクター比較チャート導入ガイド",
        "title": "TradingViewで長期移動平均線と SMH × XLV セクター比較チャートを表示する設定手順",
        "focus": "自己判断のチャート学習ツールとしてTradingViewに長期移動平均線および半導体（SMH）・ヘルスケア（XLV）の相対推移を表示する設定ステップ",
        "catalyst_type": "TradingView チャート可視化設定 ＆ 自己学習ツールガイド",
        "entry": 258.40, "atr": 5.80, "iv": 24, "score": 90.5, "dp": "チャート可視化", "call_ratio": "自己学習",
        "is_guide": True,
        "noindex": True
    },
    {
        "slug": "us-stock-stop-loss-2percent-rule.html",
        "ticker": "SMH",
        "terminal_ticker": "SMH",
        "jp_name": "下落の非対称性と安全資産クッションの数学",
        "title": "老後資金・新NISAで深い下落を避ける「ドローダウン回復の数学」と個人向け国債クッション解説",
        "focus": "-50%の下落を取り戻すには+100%の上昇が必要となる複利の非対称性と、SMH × XLV に個人向け国債（変動10年）を添えて資産寿命を守る数理モデル",
        "catalyst_type": "ドローダウン非対称性の数学 ＆ 安全資産クッション解説",
        "entry": 258.40, "atr": 5.80, "iv": 24, "score": 93.0, "dp": "26年複利検証", "call_ratio": "資産防衛",
        "is_guide": True,
        "noindex": True
    },
    {
        "slug": "dark-pool-whale-flow-reading.html",
        "ticker": "XLV",
        "jp_name": "機関投資家の取引所外ブロック取引（ATS）公開統計とは",
        "title": "米国の取引所外大口取引（ATS公開統計）とは？年金基金・機関投資家の長期執行データの基礎知識",
        "focus": "米国FINRA等で公開される取引所外ブロック取引（ATS）比率の意味と、年金基金や長期機関投資家が市場インパクトを抑えて執行する仕組みの解説",
        "catalyst_type": "FINRA公開ATS統計データ ＆ 機関投資家執行インフラ解説",
        "entry": 148.90, "atr": 2.40, "iv": 18, "score": 88.4, "dp": "FINRA公開統計", "call_ratio": "基礎教養",
        "is_guide": True,
        "noindex": True
    },
    {
        "slug": "ai-datacenter-power-stocks-2026.html",
        "ticker": "CEG",
        "jp_name": "AIデータセンター電力・冷却インフラ公開財務データ比較",
        "title": "AIデータセンター電力・冷却インフラ関連米国株（CEG・VRT・AVGO）の公開決算データ比較",
        "focus": "電力供給契約（PPA）と冷却設備・半導体インフラを担う主要3社の米SEC公式決算開示（売上成長率・営業利益率・配当利回り）の客観比較",
        "catalyst_type": "電力・インフラ関連3社の公開財務指標比較",
        "entry": 249.95, "atr": 12.02, "iv": 61, "score": 88.0, "dp": "3社比較統計", "call_ratio": "セクター研究",
        "is_guide": True
    },
    {
        "slug": "semiconductor-cycle-truthofmarket-guide.html",
        "ticker": "SMH",
        "terminal_ticker": "SMH",
        "jp_name": "日米マクロ＆ SMH × XLV 2本柱 資産配分フレームワーク",
        "title": "半導体サイクル26年統計と「新NISA（SMH × XLV）＋個人向け国債（変動10年）」2本柱連携ガイド",
        "focus": "新NISA成長投資枠で保有できる米国半導体（SMH）と米国ヘルスケア（XLV）に、個人向け国債（変動10年）や特定口座（SGOV）の安全資産を組み合わせる長期資産配分設計",
        "catalyst_type": "26年セクター統計 × 新NISA老後資産配分設計",
        "entry": 258.40, "atr": 5.80, "iv": 24, "score": 94.0, "dp": "2000-2025検証", "call_ratio": "現物1倍",
        "is_guide": True
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
    jp_name = _senior_clean_hub_text(item["jp_name"])
    title = _senior_clean_hub_text(item["title"])
    focus = _senior_clean_hub_text(item["focus"])
    cat_type = _senior_clean_hub_text(item["catalyst_type"])
    entry = float(item["entry"])
    atr = float(item["atr"])
    score = float(item["score"])
    dp = _senior_clean_hub_text(item["dp"])
    call_ratio = _senior_clean_hub_text(item["call_ratio"])
    is_avoid = bool(item.get("is_avoid", False))
    is_non_nisa_edu = bool(item.get("is_non_nisa_edu", False))
    is_leveraged_warning = bool(item.get("is_leveraged_warning", False))
    is_guide = bool(item.get("is_guide", False))
    is_flagship_nisa_guide = bool(item.get("is_flagship_nisa_guide", False))
    is_noindex = bool(item.get("noindex", False))
    robots_meta_tag = '  <meta name="robots" content="noindex, follow">\n' if is_noindex else ""

    default_acc = 50000
    alloc_cap_usd = default_acc * 0.10
    shares = max(1, int(alloc_cap_usd // max(entry, 0.5)))
    notional_usd = round(shares * entry)
    notional_jpy_man = round(notional_usd * 150 / 10000, 1)

    clean_slug = slug[:-5] if slug.endswith(".html") else slug
    canonical_url = f"https://getbreakai.com/jp/{clean_slug}"

    if is_leveraged_warning:
        verdict_banner = (
            "【新NISA対象外・老後資金での保有非推奨】3倍レバレッジ型ETF（SOXL・TQQQ等）は日本の金融庁規定により新NISA対象外であり、"
            "日々の値動きの3倍を複利計算する仕組み上、横ばい・下落相場で元本が大きく削られる「減価（ボラティリティ・ドラッグ）」リスクがあります。"
            f"50〜70代の大切な退職金・老後資金には一切推奨せず、{FSA_HYBRID_PHRASE_JP}への切り替えをご案内しています。"
        )
    elif is_flagship_nisa_guide:
        verdict_banner = (
            "【新NISA・老後資産配分 基礎ガイド】年間360万円・生涯1,800万円の非課税枠を長期で守り抜く鍵は、短期の売買ではなく"
            "「新NISA成長投資枠の現物1倍2本柱（米国半導体 SMH × 米国ヘルスケア XLV）」と"
            "「生活防衛クッション（個人向け国債 変動10年 ／ 特定口座 SGOV）」を組み合わせ、年2回だけ静かに比率を点検する設計にあります。"
        )
    elif is_guide:
        verdict_banner = (
            f"【公開市場データ・基礎解説】{focus}。"
            f"50〜70代の老後資産設計における基本原則（{FSA_HYBRID_PHRASE_JP}）に沿ってわかりやすく整理しています。"
        )
    elif is_avoid:
        verdict_banner = (
            f"【公開財務リスク指標の確認】{jp_name} は公開データ安定度スコア {score}/100（{cat_type}・取引所外データ {dp}）のため、"
            "1銘柄への偏重を避け、コア資産は新NISA成長投資枠の現物セクターETF（SMH × XLV）で分散すべき高変動区分として整理しています。"
        )
    elif is_non_nisa_edu:
        verdict_banner = (
            f"【金融庁・新NISA制度区分のご注意】レバレッジ型ETF（SOXL・TQQQ）および毎月分配型ETF（JEPI・JEPQ・QYLD・SGOV）は"
            f"日本の金融庁規定により【新NISA対象外（特定口座のみ保有可）】です。50〜70代の老後資産形成には{FSA_HYBRID_PHRASE_JP}をご活用ください。"
        )
    else:
        verdict_banner = (
            f"【公開市場データ要約】{jp_name}（直近公開終値 ${entry:.2f}）の公開財務・需給スコアは {score}/100（{cat_type}）です。"
            f"想定運用資金 $50,000（約750万円）口座において1銘柄上限10%以内に抑える分散目安は {shares}株（約{notional_jpy_man}万円）であり、"
            "老後コア資産は新NISA成長投資枠の SMH × XLV ＋ 個人向け国債（変動10年）で安定させる設計が基本となります。"
        )

    if is_flagship_nisa_guide:
        related_links_html = "\n".join([
            '<li><a href="/jp/nisa-quiet-barbell-essay.html" style="color:#1d4ed8; text-decoration:none; font-weight:700;">火曜の夜に証券アプリを閉じる理由 — 半導体（SMH）と医療（XLV）という2つの時計</a></li>',
            '<li><a href="/jp/semiconductor-cycle-truthofmarket-guide.html" style="color:#1d4ed8; text-decoration:none; font-weight:700;">半導体サイクル26年統計と「新NISA（SMH × XLV）＋個人向け国債（変動10年）」2本柱連携ガイド</a></li>',
            '<li><a href="/jp/daily-nisa-quant-report.html" style="color:#1d4ed8; text-decoration:none; font-weight:700;">朝の資産守り＆新NISA公開データ日報（SMH × XLV ＋ 個人向け国債 2本柱）</a></li>',
            '<li><a href="/jp/unh-defensive-healthcare-insider-buy.html" style="color:#1d4ed8; text-decoration:none; font-weight:700;">ユナイテッドヘルス(UNH) ディフェンシブ医療株の連続増配データとSEC Form-4公開記録</a></li>',
            '<li><a href="/jp/lly-form4-insider-cluster-buy.html" style="color:#1d4ed8; text-decoration:none; font-weight:700;">イーライリリー(LLY) SEC Form-4経営陣の市場内自社株取得データと医薬品研究開発開示</a></li>',
            '<li><a href="/jp/msft-azure-ai-copilot-sec-8k.html" style="color:#1d4ed8; text-decoration:none; font-weight:700;">マイクロソフト(MSFT) クラウド収益・連続増配データと新NISA長期コア保有シミュレーション</a></li>',
        ])
    else:
        related_candidates = [
            s for s in all_specs
            if s["slug"] != slug and s["slug"] not in MAIN_HUB_EXCLUDED_SLUGS and not s.get("noindex")
        ]
        related_links_html = "\n".join([
            f'<li><a href="/jp/{s["slug"]}" style="color:#1d4ed8; text-decoration:none; font-weight:700;">{_senior_clean_hub_text(s["title"])}</a></li>'
            for s in related_candidates[:8]
        ])

    if is_guide or is_leveraged_warning:
        faq_q1_name = "新NISA成長投資枠における「SMH × XLV」と「個人向け国債（変動10年）」の2本柱配分とはどのような設計ですか？"
        faq_q1_text = (
            "新NISA成長投資枠ではレバレッジのない現物1倍の米国半導体ETF（SMH）と米国ヘルスケアETF（XLV）を組み合わせて構造的な成長と下落耐性を両立させ、"
            "今後2〜3年以内に使う生活防衛資金は日本の個人向け国債（変動10年）または特定口座の米国短期国債ETF（SGOV）で区分管理する長期資産配分フレームワークです。"
        )
    else:
        faq_q1_name = f"{jp_name}の公開財務データを確認する際、新NISA口座ではどのように分散比率を管理すべきですか？"
        faq_q1_text = (
            f"公開市場データ（{date_str}時点・基準終値${entry:.2f}、14日平均変動幅${atr:.2f}）上も個別株は決算ごとに固有の価格変動を伴います。"
            f"そのため老後コア資産は新NISA成長投資枠の SMH × XLV および個人向け国債（変動10年）に置き、個別株は口座全体の10%以内（$50,000＝約750万円口座で{shares}株・約{notional_jpy_man}万円目安）にとどめる設計が有効です。"
        )

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
                    "url": "https://getbreakai.com/jp/",
                    "sameAs": [
                        "https://www.youtube.com/@GetBreakAI",
                        "https://www.instagram.com/getbreakai/"
                    ],
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
                        "name": faq_q1_name,
                        "acceptedAnswer": {
                            "@type": "Answer",
                            "text": faq_q1_text
                        }
                    },
                    {
                        "@type": "Question",
                        "name": "毎月分配型ETF（SGOV・JEPI等）やレバレッジ型ETF（SOXL等）は新NISAで買えますか？",
                        "acceptedAnswer": {
                            "@type": "Answer",
                            "text": "いいえ。日本の金融庁ルールにより、毎月分配型ETF（SGOV・JEPI・JEPQ・QYLD等）およびレバレッジ型ETF（SOXL・TQQQ等）は新NISAの対象外であり、特定口座でのみ保有可能です。新NISA成長投資枠では現物1倍の米国半導体ETF（SMH）と米国ヘルスケアETF（XLV）を保有し、安全資産クッションは日本の個人向け国債（変動10年）または特定口座のSGOVで区分管理する設計が適しています。"
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

    kicker_html = (
        "新NISA・老後資産配分 基礎ガイド ・ SMH × XLV ＋ 個人向け国債（変動10年）"
        if (is_guide or is_leveraged_warning)
        else f"米国企業 公開財務データ研究ノート ・ 対象銘柄: {jp_name} (${ticker})"
    )

    if is_flagship_nisa_guide:
        body_chapters_html = f"""      <h2>1. 新NISA（年間360万円・生涯1,800万円）で最も避けたい「単一テーマ集中」と深い下落の数学</h2>
      <p>
        新NISA口座は配当金や譲渡益に対する20.315%の課税が非課税になる非常に心強い制度ですが、特定口座とは異なり<strong>「万が一損失が出ても他の口座の利益と損益通算ができない」</strong>という制度上の特徴があります。また、短期的な売買を繰り返すと年間360万円（成長投資枠240万円）の非課税投資枠をその年のうちに消化してしまいます。
      </p>
      <p>
        さらに重要なのが「下落の非対称性」です。資産が一度 <strong>-50% 下落すると、元の水準を取り戻すためには +100% の上昇</strong>が必要になります。50〜70代の退職金や老後資金において、単一のハイテク株や値動きの激しいテーマ株だけに集中投資してしまうと、相場調整が長引いた際に生活費の取り崩しと重なり、資産寿命を大きく縮める原因となります。
      </p>

      <h2>2. なぜ「米国半導体（SMH）× 米国ヘルスケア（XLV）」の現物1倍2本柱なのか（2000〜2025年検証）</h2>
      <p>
        そこで当プラットフォームが2000年〜2025年（26年間・ITバブル崩壊、リーマン危機、2022年急速利上げを含む）の公開データから検証しているのが、<strong>新NISA成長投資枠で保有できる現物1倍ETF「米国半導体（SMH）」と「米国ヘルスケア（XLV）」を組み合わせる2本柱設計</strong>です。
      </p>
      <p>
        AI・データセンター・産業インフラの設備投資サイクルを牽引する半導体（SMH）の隣に、景気後退や金利変動に左右されにくい医薬品・医療機器・ヘルスケアサービス（XLV）を並べることで、2022年のハイテク調整局面（SMH 約-35%に対し XLV は約-2%で推移）のように異なる値動きのリズムが互いを支え合い、単独保有に比べて最大ドローダウンと回復期間を大きく抑えることができます。
      </p>

      <h2>3. 生活防衛クッション：「個人向け国債（変動10年）」と特定口座（SGOV）の金融庁準拠区分</h2>
      <p>
        日本の金融庁規定により、<strong>毎月分配型ETF（SGOV・JEPI等）およびレバレッジ型ETF（SOXL・TQQQ等）は新NISAの対象外</strong>です。そのため、今後2〜3年以内に使う予定の生活防衛資金や医療・住宅予備費は、株式市場から切り離して安全資産クッションとして確保します。
      </p>
      <p>
        日本居住のシニア世帯にとって最もわかりやすい選択肢は、財務省が発行する<strong>「個人向け国債（変動10年）」</strong>（元本割れなし・1万円から購入可・半年ごとに実勢金利に合わせて適用利率が見直し）です。米ドル建ての待機資金を運用する場合は、<strong>特定口座（源泉徴収あり）で米国短期国債0-3ヶ月ETF（SGOV）</strong>を区分管理する<strong>{FSA_HYBRID_PHRASE_JP}</strong>が制度に完全準拠した形となります。
      </p>

      <h2>4. 毎日の株価ボードから離れる「年2回の穏やかな比率点検」ルール</h2>
      <p>
        老後の資産設計で本当に大切なのは、毎日のニュースや分刻みのチャートを追いかけることではなく、あらかじめ決めた<strong>「SMH : XLV : 安全資産（個人向け国債・SGOV）」の基準比率を年2回（半年ごと）だけ静かに点検すること</strong>です。半導体が大きく上昇して比率が膨らみすぎたときは一部をヘルスケアや安全資産へ戻し、市場が極端な悲観に沈んだときだけ落ち着いた目で公開データを確認する——その規律が夜の安心と長期の複利を守ります。
      </p>"""
    elif is_leveraged_warning:
        body_chapters_html = f"""      <h2>1. なぜ3倍レバレッジ型ETF（SOXL・TQQQ等）は老後資金・退職金運用に不向きなのか（減価リスクの仕組み）</h2>
      <p>
        「SOXL（半導体ブル3倍ETF）」や「TQQQ」などのレバレッジ型ETFは、<strong>1日あたりの指数変動率の3倍</strong>に連動するよう設計された短期指標であり、長期保有を前提とした資産ではありません。たとえば指数が「1日目に10%下落し、翌日に11.1%上昇して元の水準（100）に戻った」場合でも、3倍レバレッジ型は1日目に30%下落（100→70）した後、翌日に33.3%上昇しても「93.3」までしか戻らず、<strong>相場が横ばいでも元本が削られていく『減価（ボラティリティ・ドラッグ）』</strong>が数学的に発生します。
      </p>
      <p>
        さらに半導体サイクルの調整局面では基準価額がピークから<strong>-70%〜-85%以上急落</strong>する事例が過去に何度も観測されており、50〜70代の大切な退職金や老後生活資金を投じると回復までに長い歳月を要する恐れがあります。そのため当サイトでは、<strong>3倍レバレッジ型ETFを老後資金・新NISA世代の資産形成に一切推奨しておりません。</strong>
      </p>

      <h2>2. 金融庁がレバレッジ型・毎月分配型を「新NISA対象外」と定めた理由</h2>
      <p>
        日本の金融庁規定により、<strong>レバレッジ型ETF（SOXL・TQQQ等）および毎月分配型ETF（SGOV・JEPI・JEPQ・QYLD等）は新NISA（つみたて投資枠・成長投資枠とも）の対象外</strong>と明確に定められています。これは長期・分散による安定的な資産形成を守るための制度設計です。
      </p>
      <p>
        万が一、特定口座でレバレッジ型ETFを保有して大きな含み損を抱えている場合も、「いつか戻るまでナンピン（買い増し）する」のではなく、ご自身の生活防衛資金とリスク許容度を冷静に点検し、現物1倍のセクター分散と安全資産クッションへ段階的に切り替えることが大切です。
      </p>

      <h2>3. 現物1倍の2本柱への切り替え：{FSA_HYBRID_PHRASE_JP}</h2>
      <p>
        半導体の長期成長を取り込みながら深い下落から資産寿命を守るには、減価リスクのある3倍レバレッジ商品ではなく、<strong>{FSA_HYBRID_PHRASE_JP}</strong>が王道となります。
      </p>
      <p>
        具体的には、新NISA成長投資枠で保有できる現物1倍の<strong>米国半導体ETF（SMH）</strong>と、景気後退局面でも底堅い<strong>米国ヘルスケアETF（XLV）</strong>を組み合わせ、さらに生活費2〜3年分の安全クッションを<strong>個人向け国債（変動10年）または特定口座の米国短期国債ETF（SGOV）</strong>で確保する設計です。
      </p>

      <h2>4. 年2回のゆったり比率点検で「夜もぐっすり眠れる老後設計」へ</h2>
      <p>
        老後の資産運用で一番大切なのは、毎日の株価ボードに張り付いて一喜一憂することではなく、健康や趣味・ご家族との時間を楽しみながら<strong>年2回だけ SMH × XLV と安全資産の比率を穏やかに点検すること</strong>です。下記の4ステップ比率シミュレーターにて、ご自身の資産規模に合った初期ベース比率を無料でご確認いただけます。
      </p>"""
    elif is_guide:
        body_chapters_html = f"""      <h2>1. 基礎解説：{jp_name} の公開データ構造と確認ポイント</h2>
      <p>
        50〜70代の個人投資家が新NISAや退職金運用で最も大切にしたいのは、SNSの噂や短期的な値動きの見出しに振り回されず、<strong>公的機関・規制当局・取引所が公表する一次統計データ（{cat_type}）</strong>を落ち着いた視点で読み解くことです。本ガイドの主要テーマは「<strong>{focus}</strong>」です。
      </p>
      <p>
        専門用語が多く見える米国の公開市場データも、「長期の収益基盤が維持されているか」「市場全体の過熱・悲観が極端な水準にないか」「ご自身の資産配分が単一テーマに偏っていないか」の3点に絞って確認すれば、日々のニュースに慌てる必要はなくなります。
      </p>

      <h2>2. 短期売買ではなく「長期セクター分散」に公開データを活かす視点</h2>
      <p>
        公開市場の統計データ（区分：{dp} ・ 点検目安：{call_ratio}）は、明日の株価を当てて頻繁に売買するためにあるのではありません。むしろ「市場が熱狂しているときに高値で買いすぎない」「一時的な悲観局面で大切な長期資産を狼狽売りしない」ための<strong>心の温度計</strong>として活用することに本来の価値があります。
      </p>
      <p>
        新NISA口座では短期売買を繰り返すと年間非課税枠を消費してしまうため、公開データは年2回の定期点検の参考指標として静かに役立てるのが賢明です。
      </p>

      <h2>3. 【金融庁規定準拠】新NISA成長投資枠（SMH × XLV）と個人向け国債の2本柱設計</h2>
      <p>
        日本の金融庁ルールにより、<strong>毎月分配型ETF（SGOV・JEPI等）およびレバレッジ型ETF（SOXL・TQQQ等）は新NISAの対象外</strong>であり、特定口座でのみ保有可能です。制度に正しく準拠しながらインフレ対応の成長と下値防衛を両立させるには、<strong>{FSA_HYBRID_PHRASE_JP}</strong>が明快な基準となります。
      </p>
      <p>
        新NISA成長投資枠では現物1倍の<strong>米国半導体ETF（SMH）</strong>と<strong>米国ヘルスケアETF（XLV）</strong>という異なる景気サイクルで動く2本柱を保有し、生活防衛クッションは<strong>日本の個人向け国債（変動10年）または特定口座のSGOV</strong>で別枠管理することで、嵐の相場でも取り崩しに困らない土台が整います。
      </p>

      <h2>4. セクター過去統計エクスプローラー（2000–2025年統計比較）による歴史的ケース確認</h2>
      <p>
        どれほど優れた制度や公開データがあっても、ご自身の睡眠を妨げるような高い変動幅では長期保有を続けることはできません。下の検証サマリーおよび<strong>「セクター過去統計エクスプローラー（2000–2025年統計比較）」</strong>を使って、過去25年間の下落局面における歴史的統計比率を確かめてみてください。
      </p>"""
    else:
        body_chapters_html = f"""      <h2>1. {jp_name} の米SEC公式決算開示（Form 8-K/10-Q）および公開業績データの整理</h2>
      <p>
        50〜70代の個人投資家が新NISAや老後資金の運用で大切にしたいのは、一時的な話題性に流されず、<strong>企業が米国証券取引委員会（SEC）へ提出した一次公開情報（Form 8-K・Form 10-Q・年次報告書Form 10-K）</strong>を客観的に確認することです。{jp_name} に関する現在の主要確認テーマは「<strong>{focus}</strong>」であり、公開データ安定度スコアは <strong>{score}/100（区分：{cat_type}）</strong> となっています。
      </p>
      <p>
        英語で公開される決算発表や設備投資・株主還元方針の開示も、「売上と営業キャッシュフローの持続性」「バランスシートの健全性」「配当・自社株買いの実績」の3点に絞って整理すれば、落ち着いた長期視点で評価することができます。
      </p>

      <h2>2. SEC Form-4（役員自社株取得記録）および機関投資家の公開需給統計（{dp}）</h2>
      <p>
        中長期の資金動向を読み解く補助資料となるのが、<strong>SEC Form-4（経営陣による市場内での自社株取得開示）</strong>および米国FINRA等で集計される<strong>取引所外の大口機関投資家取引統計（現在 {dp} ・ 需給区分 {call_ratio}）</strong>です。
      </p>
      <p>
        年金基金や長期運用の機関投資家は、単一銘柄に過度の資金を集中させることなく、セクター全体の枠組みのなかで慎重にウェイトを管理します。個人の新NISA・老後資産づくりにおいても、個別企業の研究はあくまで全体のバランスを補う視点として位置づけることが長期の安心につながります。
      </p>

      <h2>3. 個別株集中リスクを避ける「SMH × XLV ＋ 個人向け国債（変動10年）」2本柱コア設計</h2>
      <p>
        どれほど優良に見える個別企業であっても、単独銘柄では決算発表や規制変更による1日10%〜20%超の価格変動を避けられません。そのため50〜70代のコア資産には<strong>{FSA_HYBRID_PHRASE_JP}</strong>を据える設計を基本とします。
      </p>
      <p>
        日本の金融庁規定により毎月分配型ETF（SGOV・JEPI等）やレバレッジ型ETF（SOXL等）は新NISA対象外となるため、新NISA成長投資枠では現物1倍の<strong>米国半導体ETF（SMH）× 米国ヘルスケアETF（XLV）</strong>でセクター分散を図り、2〜3年分の生活防衛クッションを<strong>日本の個人向け国債（変動10年）または特定口座のSGOV</strong>で確保します。
      </p>

      <h2>4. 1銘柄あたり口座上限10%ルールの目安と年2回の穏やかな比率点検</h2>
      <p>
        新NISA口座では損失が出ても特定口座と損益通算ができず、頻繁な売却は年間非課税枠を消化してしまいます。仮に研究対象として {jp_name}（直近基準終値 ${entry:.2f}、14日平均変動幅 ${atr:.2f}）を一部組み入れる場合でも、<strong>1銘柄あたりの保有額は運用資産全体の10%以内（想定 $50,000＝約750万円口座で上限 {shares}株・約{notional_jpy_man}万円目安）</strong>にとどめ、資産の大半は年2回だけ比率を見直す SMH × XLV ＋ 安全資産の2本柱で守る運用が堅実です。
      </p>"""

    if is_guide or is_leveraged_warning:
        summary_cards_html = """      <div class="kpi-grid">
        <div class="kpi-card">
          <div class="kpi-label">SMH × XLV 過去26年 年率複利（2000-2025）</div>
          <div class="kpi-val" style="color:#059669 !important;">約 11.4%</div>
        </div>
        <div class="kpi-card">
          <div class="kpi-label">SMH × XLV 最大下落幅（S&amp;P500単独 -50.9%）</div>
          <div class="kpi-val" style="color:#1d4ed8 !important;">-27.8%</div>
        </div>
        <div class="kpi-card">
          <div class="kpi-label">新NISA成長投資枠 区分</div>
          <div class="kpi-val">現物1倍 適格（SMH・XLV）</div>
        </div>
        <div class="kpi-card">
          <div class="kpi-label">生活防衛クッション（日本居住者）</div>
          <div class="kpi-val" style="color:#b45309 !important;">個人向け国債（変動10年）／SGOV</div>
        </div>
      </div>

      <div class="widget-box">
        <h3 style="margin-top:0;">過去25年の統計を確認する「セクター過去統計エクスプローラー（2000–2025年統計比較）」</h3>
        <p style="font-size:0.94rem; color:#3d3d3a !important; margin-bottom:14px;">
          4つの条件（重視する視点・想定規模・許容下落幅・ハイテク集中度）を選ぶだけで、新NISA成長投資枠（SMH・XLV）と安全資産クッション（個人向け国債 変動10年 ／ 特定口座 SGOV）の2000–2025年過去統計比率を登録不要・無料で確認できます。
        </p>
        <a href="/jp/#gba-retirement-architect-jp" style="display:inline-flex; align-items:center; justify-content:center; min-height:48px; padding:12px 22px; background:#059669; color:#ffffff; text-decoration:none; border-radius:8px; font-weight:800; font-size:0.95rem;">
          セクター過去統計エクスプローラー（2000–2025年統計比較）を開く &rarr;
        </a>
      </div>"""
    else:
        summary_cards_html = f"""      <div class="kpi-grid">
        <div class="kpi-card">
          <div class="kpi-label">直近基準株価（公開終値）</div>
          <div class="kpi-val">${entry:.2f} <span style="font-size:0.78rem; color:#6b6b66; font-weight:700;">(約¥{int(round(entry*150)):,})</span></div>
        </div>
        <div class="kpi-card">
          <div class="kpi-label">公開データ安定度スコア</div>
          <div class="kpi-val" style="color:#1d4ed8 !important;">{score} / 100</div>
        </div>
        <div class="kpi-card">
          <div class="kpi-label">14日平均変動幅（公開統計）</div>
          <div class="kpi-val">${atr:.2f}</div>
        </div>
        <div class="kpi-card">
          <div class="kpi-label">1銘柄上限10% 分散目安（750万円口座）</div>
          <div class="kpi-val" style="color:#059669 !important;">{shares}株（約{notional_jpy_man}万円）</div>
        </div>
      </div>

      <div class="widget-box">
        <h3 style="margin-top:0;">個別株の集中リスクを比較する「セクター過去統計エクスプローラー（2000–2025年統計比較）」</h3>
        <p style="font-size:0.94rem; color:#3d3d3a !important; margin-bottom:14px;">
          1銘柄への偏重を避け、新NISA成長投資枠の米国半導体（SMH）× 米国ヘルスケア（XLV）と安全資産クッション（個人向け国債 変動10年 ／ 特定口座 SGOV）の2000–2025年歴史的統計比率を登録不要・無料で確認できます。
        </p>
        <a href="/jp/#gba-retirement-architect-jp" style="display:inline-flex; align-items:center; justify-content:center; min-height:48px; padding:12px 22px; background:#059669; color:#ffffff; text-decoration:none; border-radius:8px; font-weight:800; font-size:0.95rem;">
          セクター過去統計エクスプローラー（2000–2025年統計比較）を開く &rarr;
        </a>
      </div>"""

    substack_end_html = _build_substack_end_box_jp(slug, disclaimer_box)

    return f"""<!DOCTYPE html>
<html lang="ja" data-jp-theme="light">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{title} | GetBreakAI 朝刊エッセイ＆公開データ研究</title>
{robots_meta_tag}  <meta name="description" content="{jp_name}の{focus}を公開データからわかりやすく整理。{FSA_HYBRID_PHRASE_JP}に基づく長期資産配分ガイドを掲載。">
  <link rel="canonical" href="{canonical_url}">
  <link rel="alternate" hreflang="ja" href="{canonical_url}">
  <meta property="og:type" content="article">
  <meta property="og:locale" content="ja_JP">
  <meta property="og:site_name" content="GetBreakAI 朝刊エッセイ＆公開データ研究">
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
  <link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;600;800&family=Noto+Sans+JP:wght@400;500;700;800&family=Noto+Serif+JP:wght@500;700&display=swap" rel="stylesheet">
  <script type="application/ld+json">
{ld_json_str}
  </script>
{head_scripts}
  <style>{SUBSTACK_PAPER_CSS_JP}</style>
</head>
<body>
  <header class="essay-topbar">
    <div class="essay-topbar-inner">
      <a href="/jp/" class="essay-pub-brand">GetBreakAI ・ 朝刊エッセイ＆公開データ研究</a>
      <nav class="essay-top-nav" aria-label="記事ナビゲーション">
        <a href="/jp/nisa-quiet-barbell-essay.html">代表エッセイ</a>
        <a href="/jp/#gba-retirement-architect-jp">セクター過去統計エクスプローラー</a>
        <button type="button" onclick="openGbaStarterManualModal()">¥0 基本マニュアル</button>
      </nav>
    </div>
  </header>

  <main class="reading-column">
    <div class="essay-kicker">{kicker_html}</div>
    <h1>{title}</h1>
    <p class="essay-subtitle">{verdict_banner}</p>

    <div class="byline-bar">
      <div class="byline-author">
        <span class="byline-avatar" aria-hidden="true">佐藤</span>
        <div>
          <div class="byline-name">佐藤 健一</div>
          <div class="byline-meta">資産設計エッセイ・公開データ研究 ・ {date_str}</div>
        </div>
      </div>
      <button type="button" class="share-copy-btn" onclick="window.__gbaCopyEssayLink(this)">リンクをコピー</button>
    </div>

    <article>
{body_chapters_html}

{summary_cards_html}

      <h2>関連する新NISA・米国セクター＆優良株 公開データ研究ノート</h2>
      <ul style="list-style:none; line-height:2.0; font-size:0.95rem;">
        {related_links_html}
      </ul>
    </article>

{substack_end_html}
  </main>

{footer_html}
{manual_modal}
{waitlist_modal}

  <script>
    function jumpFromManualToJpMail() {{
      if (typeof window.closeGbaStarterManualModal === 'function') window.closeGbaStarterManualModal();
      const subBox = document.getElementById('gba-substack-subscribe');
      if (subBox && subBox.scrollIntoView) subBox.scrollIntoView({{ behavior: 'smooth', block: 'center' }});
      setTimeout(function() {{
        const inp = subBox ? subBox.querySelector('input[type="email"]') : null;
        if (inp && inp.focus) inp.focus();
      }}, 350);
    }}

    window.addEventListener('DOMContentLoaded', function() {{
      try {{
        const saved = localStorage.getItem('gb_free_member_email') || localStorage.getItem('gba_jp_free_email');
        if (saved) {{
          document.querySelectorAll('.substack-inline-form input[type="email"]').forEach(function(inp) {{ inp.value = saved; }});
        }}
      }} catch (_e) {{}}
    }});
  </script>
</body>
</html>
"""

SUBSTACK_PAPER_CSS_JP = """
    :root {
      --paper-bg: #fcfcfa;
      --card-bg: #ffffff;
      --ink: #1a1a1a;
      --ink-soft: #3d3d3a;
      --ink-muted: #6b6b66;
      --rule: #e6e4dd;
      --accent-emerald: #059669;
      --accent-blue: #1d4ed8;
      --accent-amber: #b45309;
      --accent-rose: #be123c;
      --font-serif: 'Noto Serif JP', 'Hiragino Mincho ProN', 'Yu Mincho', Georgia, serif;
      --font-sans: 'Noto Sans JP', -apple-system, BlinkMacSystemFont, sans-serif;
      --font-mono: 'JetBrains Mono', 'Noto Sans JP', monospace;
    }
    * { box-sizing: border-box; margin: 0; padding: 0; }
    .sr-only { position: absolute; width: 1px; height: 1px; padding: 0; margin: -1px; overflow: hidden; clip: rect(0,0,0,0); border: 0; }
    body {
      background: var(--paper-bg) !important;
      color: var(--ink) !important;
      font-family: var(--font-sans);
      font-size: 18.5px;
      line-height: 1.85;
      font-feature-settings: "palt" 1;
      letter-spacing: 0.015em;
      -webkit-font-smoothing: antialiased;
    }
    a { color: var(--accent-blue); text-decoration: underline; text-underline-offset: 3px; }
    .essay-topbar {
      border-bottom: 1px solid var(--rule);
      background: rgba(252, 252, 250, 0.95);
      backdrop-filter: blur(6px);
      position: sticky;
      top: 0;
      z-index: 40;
    }
    .essay-topbar-inner {
      max-width: 680px;
      margin: 0 auto;
      padding: 14px 20px;
      display: flex;
      justify-content: space-between;
      align-items: center;
      flex-wrap: wrap;
      gap: 10px;
    }
    .essay-pub-brand {
      color: var(--ink) !important;
      font-weight: 800;
      font-size: 0.96rem;
      text-decoration: none;
      letter-spacing: -0.01em;
    }
    .essay-top-nav {
      display: flex;
      gap: 12px;
      flex-wrap: wrap;
      align-items: center;
      font-size: 0.85rem;
      font-weight: 700;
    }
    .essay-top-nav a, .essay-top-nav button {
      color: var(--ink-muted) !important;
      text-decoration: none;
      background: transparent;
      border: none;
      font-family: inherit;
      font-size: 0.85rem;
      font-weight: 700;
      cursor: pointer;
      padding: 4px 2px;
    }
    .essay-top-nav a:hover, .essay-top-nav button:hover { color: var(--ink) !important; }
    .reading-column {
      max-width: 680px;
      margin: 0 auto;
      padding: 44px 20px 72px;
    }
    .essay-kicker {
      font-size: 0.78rem;
      font-weight: 800;
      letter-spacing: 0.06em;
      color: var(--accent-emerald);
      margin-bottom: 10px;
    }
    h1 {
      font-family: var(--font-serif);
      font-size: clamp(1.62rem, 3.8vw, 2.22rem);
      line-height: 1.36;
      margin-bottom: 14px;
      font-weight: 700;
      color: var(--ink) !important;
      letter-spacing: -0.01em;
    }
    .essay-subtitle {
      font-size: 1.06rem;
      line-height: 1.7;
      color: var(--ink-muted) !important;
      margin-bottom: 22px;
      font-weight: 400;
    }
    .byline-bar {
      display: flex;
      justify-content: space-between;
      align-items: center;
      gap: 12px;
      flex-wrap: wrap;
      padding: 14px 0;
      border-top: 1px solid var(--rule);
      border-bottom: 1px solid var(--rule);
      margin-bottom: 32px;
    }
    .byline-author { display: flex; align-items: center; gap: 11px; }
    .byline-avatar {
      width: 38px;
      height: 38px;
      border-radius: 50%;
      background: #e9ece6;
      color: #1f3a2e;
      font-weight: 800;
      font-size: 0.86rem;
      display: inline-flex;
      align-items: center;
      justify-content: center;
    }
    .byline-name { font-size: 0.92rem; font-weight: 800; color: var(--ink); line-height: 1.3; }
    .byline-meta { font-size: 0.8rem; color: var(--ink-muted); }
    .share-copy-btn {
      appearance: none;
      background: var(--card-bg);
      border: 1px solid var(--rule);
      border-radius: 999px;
      padding: 7px 14px;
      min-height: 38px;
      font-family: var(--font-sans);
      font-size: 0.82rem;
      font-weight: 700;
      color: var(--ink-soft);
      cursor: pointer;
    }
    .share-copy-btn:hover { border-color: #b8b5aa; color: var(--ink); }
    article p, article li {
      color: var(--ink) !important;
      margin-bottom: 1.5em;
      font-size: 18.5px;
      line-height: 1.88;
    }
    article h2 {
      font-family: var(--font-serif);
      font-size: 1.34rem;
      line-height: 1.42;
      color: var(--ink) !important;
      margin: 2.1em 0 0.75em;
      padding-bottom: 6px;
      border-bottom: 1px solid var(--rule);
      font-weight: 700;
    }
    article h3 {
      font-size: 1.08rem;
      color: var(--ink) !important;
      margin: 1.4em 0 0.5em;
      font-weight: 800;
    }
    .kpi-grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
      gap: 10px;
      margin: 22px 0;
    }
    .kpi-card {
      background: var(--card-bg) !important;
      border: 1px solid var(--rule) !important;
      border-radius: 10px;
      padding: 12px 14px;
    }
    .kpi-label { font-size: 0.78rem; color: var(--ink-muted) !important; font-weight: 700; }
    .kpi-val { font-size: 1.08rem; font-weight: 800; font-family: var(--font-mono); margin-top: 4px; color: var(--ink) !important; }
    .widget-box {
      background: var(--card-bg) !important;
      border: 1px solid var(--rule) !important;
      border-radius: 12px;
      padding: 20px;
      margin: 28px 0;
    }
    .substack-subscribe-box {
      margin: 44px 0 22px;
      padding: 28px 24px;
      background: var(--card-bg);
      border: 1px solid var(--rule);
      border-radius: 12px;
      text-align: center;
    }
    .substack-sub-title {
      font-family: var(--font-serif);
      font-size: 1.36rem;
      font-weight: 700;
      color: var(--ink);
      margin-bottom: 8px;
    }
    .substack-sub-desc {
      font-size: 0.92rem;
      line-height: 1.68;
      color: var(--ink-muted) !important;
      max-width: 520px;
      margin: 0 auto 16px;
    }
    .substack-inline-form {
      display: flex;
      max-width: 470px;
      margin: 0 auto;
      gap: 8px;
      flex-wrap: wrap;
    }
    .substack-inline-form input[type="email"] {
      flex: 1 1 220px;
      min-height: 48px;
      padding: 10px 14px;
      border: 1px solid #c9c6bc;
      border-radius: 8px;
      font-size: 0.96rem;
      background: #ffffff;
      color: var(--ink);
    }
    .substack-inline-form button {
      min-height: 48px;
      padding: 10px 20px;
      border: none;
      border-radius: 8px;
      background: #059669;
      color: #ffffff;
      font-size: 0.94rem;
      font-weight: 800;
      cursor: pointer;
    }
    .substack-sub-status {
      margin-top: 12px;
      font-size: 0.92rem;
      line-height: 1.6;
      font-weight: 700;
    }
    .editorial-postscript {
      padding: 18px 20px;
      background: #f5f4ef;
      border: 1px solid var(--rule);
      border-radius: 10px;
      font-size: 0.9rem;
      line-height: 1.72;
      color: var(--ink-soft);
      margin-bottom: 32px;
    }
    .editorial-postscript p {
      margin: 0 0 8px;
      font-size: 0.9rem;
      line-height: 1.72;
      color: var(--ink-soft) !important;
    }
    .ps-label {
      font-size: 0.76rem;
      font-weight: 800;
      letter-spacing: 0.05em;
      color: var(--ink-muted);
      margin-bottom: 6px;
    }
    /* Shared ¥0 Manual Modal styles */
    .gba-manual-free-badge { display:inline-flex; align-items:center; gap:6px; background:#059669; color:#ffffff; font-size:0.86rem; font-weight:900; padding:4px 12px; border-radius:999px; }
    .gba-manual-modal-backdrop { display:none; position:fixed; inset:0; z-index:9999; background:rgba(15,23,42,0.76); backdrop-filter:blur(4px); padding:18px 12px; overflow-y:auto; align-items:flex-start; justify-content:center; }
    .gba-manual-modal-backdrop.is-open { display:flex; }
    .gba-manual-modal-dialog { background:#ffffff; color:#0b1f3a; border:2px solid #059669; border-radius:16px; width:100%; max-width:860px; margin:8px auto 32px; box-shadow:0 22px 50px rgba(0,0,0,0.45); overflow:hidden; }
    .gba-manual-modal-header { position:sticky; top:0; z-index:5; background:#ffffff; border-bottom:2px solid #cbd5e1; padding:14px 18px; display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:10px; }
    .gba-manual-modal-title { font-size:1.18rem; font-weight:900; color:#0b1f3a; margin:4px 0 0; }
    .gba-manual-modal-actions { display:flex; gap:8px; flex-wrap:wrap; }
    .gba-manual-action-btn { appearance:none; min-height:46px; padding:8px 14px; border-radius:10px; font-size:0.96rem; font-weight:900; cursor:pointer; border:2px solid #cbd5e1; background:#f8fafc; color:#0b1f3a; }
    .gba-manual-action-btn.btn-print { border-color:#059669; background:#ecfdf5; color:#065f46; }
    .gba-manual-nav-pills { display:flex; flex-wrap:wrap; gap:8px; padding:12px 18px; background:#f8fafc; border-bottom:1px solid #cbd5e1; }
    .gba-manual-jump-pill { appearance:none; min-height:44px; padding:7px 13px; border-radius:999px; border:1.5px solid #cbd5e1; background:#ffffff; color:#0b1f3a; font-size:0.94rem; font-weight:800; cursor:pointer; }
    .gba-manual-modal-body { padding:20px; font-size:1.05rem; line-height:1.8; }
    .gba-manual-chapter-box { background:#f8fafc; border:1.5px solid #cbd5e1; border-radius:14px; padding:18px; margin-bottom:16px; }
    .gba-manual-broker-grid { display:grid; grid-template-columns:repeat(auto-fit, minmax(260px, 1fr)); gap:12px; margin-top:10px; }
    .gba-manual-broker-card { background:#ffffff; border:1.5px solid #cbd5e1; border-radius:12px; padding:14px; }
    .gba-manual-tip-callout { margin-top:12px; padding:12px 14px; border-radius:10px; background:#ecfdf5; border-left:4px solid #059669; font-weight:700; }
    .gba-manual-modal-funnel { background:#eff6ff; border:2px solid #059669; border-radius:14px; padding:18px; margin-top:10px; }
    .gba-manual-open-btn { appearance:none; background:linear-gradient(135deg,#059669,#047857); color:#ffffff; border:none; border-radius:11px; padding:12px 18px; min-height:52px; font-size:1rem; font-weight:900; cursor:pointer; }
    .gba-manual-funnel-links { display:flex; flex-wrap:wrap; gap:10px; margin-top:10px; }
    .gba-manual-pro-link, .gba-manual-vip-link { display:inline-flex; align-items:center; min-height:46px; padding:8px 14px; border-radius:999px; font-size:0.95rem; font-weight:900; text-decoration:none; background:#ffffff; border:1.5px solid #1d4ed8; color:#1d4ed8; }
    @media (max-width: 560px) {
      .reading-column { padding: 28px 18px 56px; }
      .substack-inline-form button { width: 100%; }
    }
    @media print {
      body.printing-gba-manual > *:not(#gbaStarterManualModal) { display: none !important; }
      body.printing-gba-manual #gbaStarterManualModal { display: block !important; position: static !important; background: #ffffff !important; padding: 0 !important; }
    }
"""


def _build_substack_end_box_jp(slug: str, disclaimer_box: str) -> str:
    return f"""
    <section class="substack-subscribe-box" id="gba-substack-subscribe" aria-label="朝刊エッセイ無料メール購読">
      <div class="substack-sub-title">次の朝刊エッセイをメールで受け取る</div>
      <p class="substack-sub-desc">
        AI半導体の成長（SMH）と医療の守り（XLV）、そして新NISAと老後資産の穏やかな設計について、広告のない静かな朝刊ノートをお届けします（無料・パスワード不要・1クリック解除OK）。
      </p>
      <form class="substack-inline-form" onsubmit="return window.__gbaSubmitSubstackSubscribe(event, this, '{slug}');" novalidate>
        <label for="substackEmailJp_{slug[:16]}" class="sr-only">メールアドレス</label>
        <input id="substackEmailJp_{slug[:16]}" type="email" required autocomplete="email" placeholder="メールアドレスを入力..." />
        <button type="submit">無料で購読する</button>
      </form>
      <div class="substack-sub-status" role="status" aria-live="polite" style="display:none;"></div>
    </section>

    <aside class="editorial-postscript" aria-label="編集後記・独立系教育リサーチ出版">
      <div class="ps-label">編集後記 ・ 新NISA・資産リサーチ研究室（教育目的）</div>
      <p>
        <strong>SMH × XLV</strong> の過去26年間（2000–2025年）の統計推移は、<a href="/jp/#gba-retirement-architect-jp"><strong>セクター過去統計エクスプローラー（2000–2025年統計比較）</strong></a>（<button type="button" onclick="openGbaStarterManualModal()" style="background:none;border:none;color:#1d4ed8;text-decoration:underline;font-weight:700;cursor:pointer;font-size:inherit;padding:0;">¥0 楽天・SBI証券 新NISA口座区分マニュアル</button> 同梱）で登録不要・無料でお確かめいただけます。「{SOFTWARE_POSITIONING_JP}」の購読パスは <a href="{WHOP_MONTHLY_CTA_HREF}" data-gba-paid-plan="monthly" class="whop-checkout-button">{PRICE_LABEL_MONTHLY_JP}</a> ・ <a href="{WHOP_ANNUAL_CTA_HREF}" data-gba-paid-plan="annual" class="whop-checkout-button">{PRICE_LABEL_ANNUAL_JP}</a>（決済管理：{MOR_LABEL_EN_JP}）にてご提供しています。
      </p>
{disclaimer_box}
    </aside>"""


def build_flagship_essay_jp_html(date_str: str) -> str:
    slug = "nisa-quiet-barbell-essay.html"
    clean_slug = slug[:-5] if slug.endswith(".html") else slug
    canonical_url = f"https://getbreakai.com/jp/{clean_slug}"
    title = "騒がしい強気相場よりも、静かな「2つの柱」が最後まで残る理由"
    subtitle = "夜の食卓で証券アプリを開くとき、100%ハイテク集中が奪う「眠りの質」と、半導体（SMH）×医療（XLV）が26年間の嵐をどう乗り越えたか。"
    desc = "佐藤健一による資産設計エッセイ。新NISA成長投資枠で保有できる半導体（SMH）とヘルスケア（XLV）、個人向け国債・特定口座クッションを組み合わせた穏やかな長期資産設計を26年の公開データから紐解きます。"

    head_scripts = build_payment_and_kpi_head_html()
    disclaimer_box = build_mandatory_disclaimer_html()
    manual_modal = build_starter_manual_modal_html()
    waitlist_modal = build_vip_waitlist_modal_html()
    footer_html = build_legal_footer_html()
    substack_end_html = _build_substack_end_box_jp(slug, disclaimer_box)

    ld_json = json.dumps(
        {
            "@context": "https://schema.org",
            "@graph": [
                {
                    "@type": "Article",
                    "headline": title,
                    "description": desc,
                    "datePublished": date_str,
                    "dateModified": date_str,
                    "inLanguage": "ja",
                    "mainEntityOfPage": canonical_url,
                    "author": {
                        "@type": "Person",
                        "name": "佐藤 健一",
                        "jobTitle": "資産設計エッセイ",
                    },
                    "publisher": {
                        "@type": "Organization",
                        "name": "GetBreakAI",
                        "url": "https://getbreakai.com/jp/",
                        "sameAs": [
                            "https://www.youtube.com/@GetBreakAI",
                            "https://www.instagram.com/getbreakai/",
                        ],
                    },
                },
                {
                    "@type": "FAQPage",
                    "mainEntity": [
                        {
                            "@type": "Question",
                            "name": "SMH（半導体ETF）とXLV（ヘルスケアETF）は新NISA成長投資枠の対象ですか？",
                            "acceptedAnswer": {
                                "@type": "Answer",
                                "text": "はい。SMHおよびXLVはレバレッジのない現物1倍の米国セクターETFであり、新NISAの成長投資枠で保有可能です。一方、毎月分配型の米国短期国債ETF（SGOV等）は金融庁規定により特定口座（または個人向け国債）で区分管理します。",
                            },
                        },
                        {
                            "@type": "Question",
                            "name": "当エッセイは特定の売買タイミングを助言するものですか？",
                            "acceptedAnswer": {
                                "@type": "Answer",
                                "text": MANDATORY_DISCLAIMER_JP,
                            },
                        },
                    ],
                },
            ],
        },
        ensure_ascii=False,
    )

    return f"""<!DOCTYPE html>
<html lang="ja" data-jp-theme="light">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{title} | GetBreakAI 朝刊エッセイ</title>
  <meta name="description" content="{desc}">
  <link rel="canonical" href="{canonical_url}">
  <link rel="alternate" hreflang="ja" href="{canonical_url}">
  <meta property="og:type" content="article">
  <meta property="og:locale" content="ja_JP">
  <meta property="og:site_name" content="GetBreakAI 朝刊エッセイ">
  <meta property="og:url" content="{canonical_url}">
  <meta property="og:title" content="{title}">
  <meta property="og:description" content="{subtitle}">
  <meta property="og:image" content="https://getbreakai.com/og-preview.png">
  <meta name="twitter:card" content="summary_large_image">
  <link rel="icon" type="image/svg+xml" href="/favicon.svg">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Noto+Sans+JP:wght@400;500;700;800&family=Noto+Serif+JP:wght@500;700&display=swap" rel="stylesheet">
  <script type="application/ld+json">{ld_json}</script>
{head_scripts}
  <style>{SUBSTACK_PAPER_CSS_JP}</style>
</head>
<body>
  <header class="essay-topbar">
    <div class="essay-topbar-inner">
      <a href="/jp/" class="essay-pub-brand">GetBreakAI ・ 朝刊エッセイ</a>
      <nav class="essay-top-nav" aria-label="記事ナビゲーション">
        <a href="/jp/#gba-retirement-architect-jp">セクター過去統計エクスプローラー</a>
        <button type="button" onclick="openGbaStarterManualModal()">¥0 基本マニュアル</button>
        <a href="/jp/#pricing">リサーチパス案内</a>
      </nav>
    </div>
  </header>

  <main class="reading-column">
    <div class="essay-kicker">資産設計エッセイ ・ 代表コラム</div>
    <h1>{title}</h1>
    <p class="essay-subtitle">{subtitle}</p>

    <div class="byline-bar">
      <div class="byline-author">
        <span class="byline-avatar" aria-hidden="true">佐藤</span>
        <div>
          <div class="byline-name">佐藤 健一</div>
          <div class="byline-meta">資産設計エッセイ ・ {date_str} ・ 読了目安 6分</div>
        </div>
      </div>
      <button type="button" class="share-copy-btn" onclick="window.__gbaCopyEssayLink(this)">リンクをコピー</button>
    </div>

    <article>
      <p>
        火曜日の夜遅く、米国のナスダック市場が3%以上急落したというニュースを目にしたあと、キッチンの明かりを落としてスマートフォンの証券アプリを開くとき、私たちは「今後20年間の美しい複利グラフ」を眺めるために画面を開くわけではありません。ただ静かに、これまで20年、30年と働いて少しずつ積み上げてきた老後の蓄えが無事だろうか、ひとつの人気テーマに偏りすぎてはいなかっただろうかと、胸の奥の小さな不安を確かめるために画面を開きます。
      </p>

      <p>
        強い技術革新の波が訪れるたび、投資家の周囲にはいつも似たような空気が流れます。半導体やAI関連の銘柄が連日のように高値を更新していると、値動きの穏やかな資産を持っていることが、まるで時代の変化に乗り遅れているかのように感じられてしまうのです。知人との何気ない会話や経済ニュースの見出しに触れるうち、最初は老後の安心のために始めたはずの新NISA口座が、いつの間にか資産の7割、8割まで単一のハイテク・サイクルと同じ方向に揺れ動く形へと傾いていきます。
      </p>

      <p>
        ひとつの産業だけに資産を預ける危うさは、上昇相場の計算表には決して現れません。それが顔を出すのは、下落が始まってから1年半が過ぎた頃の「暮らしの予定表」のなかです。2000年から2002年にかけてのITバブル崩壊では、ハイテク中心の指数が底を打つまでに8割を超える下落を記録しました。そこまで極端ではない2022年の利上げ局面でさえ、米国半導体ETF（SMH）は高値から約35%後退しています。頭の中では「長期投資だから下がっても持ち続ければいい」とわかっていても、現実の人生では定年退職の時期も、自宅の修繕も、家族の節目も、半導体サイクルの回復を待ってはくれません。
      </p>

      <p>
        だからこそ、長期の成長エンジンである米国半導体（SMH）の隣に、米国ヘルスケア（XLV）というまったく別の時計で動く柱を並べておくことに深い意味が生まれます。どちらもレバレッジのかからない現物1倍のETFであり、新NISAの成長投資枠で静かに保有できる資産です。半導体がデータセンターや産業インフラの設備投資サイクルに乗って大きく前進する一方で、医薬品や医療機器、ヘルスケアサービスに対する需要は、中央銀行の金利政策や景気の良し悪しに左右されにくいという性質を持っています。病院の診察室や日々の処方箋は、株式市場の流行とは無関係に今日も動いているからです。
      </p>

      <p>
        2022年の相場をもう一度振り返ってみると、その違いは驚くほど穏やかに表れています。SMHが秋にかけて約35%下落するなか、XLVは年間を通じてほとんど崩れず、マイナス2%前後の水準にとどまりました。2つの柱を組み合わせていた世帯の資産が無傷だったわけではありません。けれども、口座の半分近くが嵐のなかでも静かに踏みとどまってくれたおかげで、多くの人が一番底で慌てて手放すことなく眠りにつき、結果として2023年以降の半導体回復の果実をそのまま受け取ることができたのです。
      </p>

      <p>
        さらに50代・60代からの資産設計であれば、今後2〜3年以内に使う予定の生活防衛資金を、日本の個人向け国債（変動10年）や特定口座で区分管理する米国短期国債ETF（SGOVなど、金融庁規定に合わせたハイブリッド設計）として手元に置いておくことで、心の余裕はもう一段深まります。3倍レバレッジ商品や分刻みのチャートを追いかける必要はありません。ご自身が夜ぐっすり眠れる比率をあらかじめ決めておき、市場の過熱や恐怖が極端に振れたときだけ落ち着いた目で公開データを確かめる。騒がしい相場を最後まで歩き通すのは、いつもそうした静かな設計なのだと感じています。
      </p>
    </article>

{substack_end_html}
  </main>

{footer_html}
{manual_modal}
{waitlist_modal}
</body>
</html>
"""

def _load_live_temp_badge_jp(fallback_date: str) -> str:
    semi_path = os.path.join(ROOT_DIR, "data", "semi_overview.json")
    as_of = fallback_date or "2026-11-19"
    score_int = 52
    regime_lbl = "中立圏"
    if os.path.isfile(semi_path):
        try:
            with open(semi_path, "r", encoding="utf-8") as sf:
                ov = json.load(sf)
            if ov.get("date"):
                as_of = str(ov["date"]).strip()
            raw_sc = ov.get("fg_score", ov.get("fear_greed_score", ov.get("score", 52)))
            score_int = int(round(float(raw_sc)))
            if score_int <= 25:
                regime_lbl = "極度の恐怖圏"
            elif score_int <= 44:
                regime_lbl = "慎重・警戒圏"
            elif score_int <= 55:
                regime_lbl = "中立圏"
            elif score_int <= 75:
                regime_lbl = "強気圏"
            else:
                regime_lbl = "過熱注意圏"
        except Exception:
            pass
    return f"最新データ基準日：{as_of} ・ 市場温度指数：{score_int} / 100（{regime_lbl}）"


def build_hub_html(date_str: str, all_specs: list, is_root: bool = False) -> str:
    canonical_url = "https://getbreakai.com/" if is_root else "https://getbreakai.com/jp/"
    hreflang_tags = (
        '  <link rel="alternate" hreflang="ja" href="https://getbreakai.com/">\n'
        '  <link rel="alternate" hreflang="x-default" href="https://getbreakai.com/">'
        if is_root else
        '  <link rel="alternate" hreflang="ja" href="https://getbreakai.com/jp/">'
    )

    head_scripts = build_payment_and_kpi_head_html()
    manual_modal = build_starter_manual_modal_html()
    waitlist_modal = build_vip_waitlist_modal_html()
    live_temp_text_jp = _load_live_temp_badge_jp(date_str)

    ld_json = json.dumps({
        "@context": "https://schema.org",
        "@graph": [
            {
                "@type": "Organization",
                "name": "GetBreakAI Japan Research",
                "url": canonical_url,
                "logo": "https://getbreakai.com/og-preview.png",
                "email": "support@getbreakai.com",
                "sameAs": [
                    "https://www.youtube.com/@GetBreakAI",
                    "https://www.instagram.com/getbreakai/"
                ]
            },
            {
                "@type": "SoftwareApplication",
                "name": "GetBreakAI — 新NISA・資産リサーチ研究室（教育目的）｜セクター過去統計エクスプローラー（2000–2025年統計比較）",
                "url": canonical_url,
                "image": "https://getbreakai.com/og-preview.png",
                "inLanguage": "ja",
                "applicationCategory": "EducationalApplication",
                "operatingSystem": "Web",
                "description": f"「{SOFTWARE_POSITIONING_JP}」。{FSA_HYBRID_PHRASE_JP}対応。",
                "offers": [
                    {
                        "@type": "Offer",
                        "name": PRICE_LABEL_MONTHLY_JP,
                        "price": "4400",
                        "priceCurrency": "JPY",
                        "url": WHOP_MONTHLY_CTA_HREF
                    },
                    {
                        "@type": "Offer",
                        "name": PRICE_LABEL_ANNUAL_JP,
                        "price": "29800",
                        "priceCurrency": "JPY",
                        "url": WHOP_ANNUAL_CTA_HREF
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
  <meta name="naver-site-verification" content="3427958718d8f3404b04d803e4b60e773ef4e2df" data-slot="naver-search-advisor">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>GetBreakAI Japan — 新NISA・資産リサーチ研究室（教育目的）｜SMH × XLV 過去25年統計比較</title>
  <meta name="description" content="騒がしい銘柄探しを手放し、二つの柱で老後資産を守り抜くために。教育目的の市場データニュースレター ＋ 2000–2025年 過去統計ワークブック（投資助言・個別推奨は一切行わない独立系リサーチ出版）。">
  <link rel="canonical" href="{canonical_url}">
{hreflang_tags}
  <meta property="og:type" content="website">
  <meta property="og:locale" content="ja_JP">
  <meta property="og:site_name" content="GetBreakAI Japan Research">
  <meta property="og:title" content="GetBreakAI Japan — 新NISA・資産リサーチ研究室（教育目的）">
  <meta property="og:description" content="セクター過去統計エクスプローラー（2000–2025年統計比較）＆ 教育目的の市場データニュースレター ＋ 2000–2025年 過去統計ワークブック。">
  <meta property="og:url" content="{canonical_url}">
  <meta property="og:image" content="https://getbreakai.com/og-preview.png">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="GetBreakAI Japan — 新NISA・資産リサーチ研究室（教育目的）">
  <meta name="twitter:description" content="セクター過去統計エクスプローラー（2000–2025年統計比較）＆ 朝刊リサーチノート。">
  <meta name="twitter:image" content="https://getbreakai.com/og-preview.png">
  <link rel="icon" type="image/svg+xml" href="/favicon.svg">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Noto+Sans+JP:wght@400;500;600;700&family=Shippori+Mincho:wght@500;600;700&display=swap" rel="stylesheet">
  <script type="application/ld+json">
{ld_json}
  </script>
{head_scripts}
  <style>
    :root, html[data-jp-theme="light"] {{
      --pw-bg: #FBFBF9;
      --pw-surface: #FFFFFF;
      --pw-sub: #F3F8F5;
      --pw-border: #E2E8F0;
      --pw-border-strong: #CBD5E1;
      --pw-ink: #0F172A;
      --pw-body: #334155;
      --pw-muted: #64748B;
      --pw-emerald: #065F46;
      --pw-navy: #1E3A8A;
    }}
    html[data-jp-theme="dark"] {{
      --pw-bg: #0B1120;
      --pw-surface: #111827;
      --pw-sub: #0F2922;
      --pw-border: #1E293B;
      --pw-border-strong: #334155;
      --pw-ink: #F8FAFC;
      --pw-body: #CBD5E1;
      --pw-muted: #94A3B8;
      --pw-emerald: #10B981;
      --pw-navy: #60A5FA;
    }}
    * {{ box-sizing: border-box; }}
    html {{ font-size: 18px; }}
    body {{
      margin: 0;
      background: var(--pw-bg);
      color: var(--pw-ink);
      font-family: 'Noto Sans JP', 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
      font-size: 18px;
      line-height: 1.78;
      font-feature-settings: "palt" 1;
      -webkit-font-smoothing: antialiased;
    }}
    .pw-shell {{
      max-width: 820px;
      margin: 0 auto;
      padding: 36px 24px 48px;
    }}
    .pw-masthead {{
      display: flex;
      justify-content: space-between;
      align-items: baseline;
      gap: 16px;
      flex-wrap: wrap;
      padding-bottom: 20px;
      margin-bottom: 40px;
      border-bottom: 1px solid var(--pw-border);
    }}
    .pw-brand-btn {{
      appearance: none;
      background: none;
      border: none;
      padding: 0;
      cursor: pointer;
      text-align: left;
      color: var(--pw-ink);
      display: inline-flex;
      align-items: baseline;
      gap: 12px;
      flex-wrap: wrap;
    }}
    .pw-wordmark {{
      font-family: 'Inter', 'Noto Sans JP', sans-serif;
      font-size: 0.86rem;
      font-weight: 700;
      letter-spacing: 0.14em;
      text-transform: uppercase;
      color: var(--pw-ink);
    }}
    .pw-submark {{
      font-size: 0.78rem;
      font-weight: 500;
      color: var(--pw-muted);
    }}
    .pw-signin-link {{
      appearance: none;
      background: none;
      border: none;
      padding: 4px 0;
      font-family: inherit;
      font-size: 0.85rem;
      font-weight: 500;
      color: var(--pw-body);
      cursor: pointer;
      border-bottom: 1px solid transparent;
    }}
    .pw-signin-link:hover {{
      color: var(--pw-ink);
      border-bottom-color: var(--pw-ink);
    }}
    .pw-kicker {{
      font-family: 'Inter', 'Noto Sans JP', sans-serif;
      font-size: 0.75rem;
      font-weight: 600;
      letter-spacing: 0.1em;
      text-transform: uppercase;
      color: var(--pw-emerald);
      margin: 0 0 14px;
    }}
    .pw-serif-h1 {{
      font-family: 'Shippori Mincho', 'Noto Serif JP', 'Yu Mincho', Georgia, serif;
      font-weight: 600;
      font-size: clamp(1.7rem, 3.8vw, 2.55rem);
      line-height: 1.36;
      letter-spacing: -0.01em;
      word-break: auto-phrase;
      color: var(--pw-ink);
      margin: 0 0 22px;
    }}
    .pw-editorial-figure {{
      margin: 0 0 30px;
      padding: 0;
    }}
    .pw-editorial-plate {{
      width: 100%;
      background: #FBFBF9;
      border-radius: 6px;
      overflow: hidden;
    }}
    html[data-jp-theme="dark"] .pw-editorial-plate {{
      padding: 6px;
      border: 1px solid var(--pw-border-strong);
    }}
    .pw-editorial-plate img {{
      display: block;
      width: 100%;
      max-height: 390px;
      height: auto;
      object-fit: contain;
      margin: 0 auto;
    }}
    .pw-editorial-caption {{
      margin: 8px 0 0;
      font-family: 'Shippori Mincho', 'Noto Serif JP', Georgia, serif;
      font-size: 0.88rem;
      line-height: 1.65;
      color: var(--pw-muted);
      text-align: center;
    }}
    .pw-serif-h2 {{
      font-family: 'Shippori Mincho', 'Noto Serif JP', 'Yu Mincho', Georgia, serif;
      font-weight: 600;
      font-size: clamp(1.45rem, 3vw, 1.95rem);
      line-height: 1.38;
      color: var(--pw-ink);
      margin: 0 0 14px;
    }}
    .pw-manifesto {{
      margin: 0 0 36px;
    }}
    .pw-manifesto p {{
      margin: 0 0 18px;
      font-size: 1rem;
      line-height: 1.85;
      color: var(--pw-body);
    }}
    .pw-manifesto p:last-child {{
      margin-bottom: 0;
    }}
    .pw-manifesto strong {{
      color: var(--pw-ink);
      font-weight: 600;
    }}
    .pw-table-card {{
      background: var(--pw-surface);
      border: 1px solid var(--pw-border);
      border-radius: 6px;
      padding: 24px 24px 18px;
      margin: 0 0 34px;
    }}
    .pw-table-header {{
      display: flex;
      justify-content: space-between;
      align-items: baseline;
      flex-wrap: wrap;
      gap: 8px;
      margin-bottom: 14px;
    }}
    .pw-table-title {{
      font-family: 'Inter', 'Noto Sans JP', sans-serif;
      font-size: 0.76rem;
      font-weight: 600;
      letter-spacing: 0.08em;
      color: var(--pw-body);
    }}
    .pw-table-meta {{
      font-size: 0.78rem;
      color: var(--pw-muted);
    }}
    .pw-table-scroll {{
      overflow-x: auto;
      -webkit-overflow-scrolling: touch;
    }}
    .pw-sim-table {{
      width: 100%;
      border-collapse: collapse;
      font-variant-numeric: tabular-nums;
      font-size: 0.88rem;
    }}
    .pw-sim-table th {{
      text-align: right;
      font-size: 0.72rem;
      font-weight: 600;
      letter-spacing: 0.02em;
      color: var(--pw-muted);
      padding: 10px 8px;
      border-top: 1px solid var(--pw-border);
      border-bottom: 1px solid var(--pw-border-strong);
      white-space: nowrap;
    }}
    .pw-sim-table th:first-child {{
      text-align: left;
      padding-left: 8px;
    }}
    .pw-sim-table td {{
      text-align: right;
      padding: 12px 8px;
      border-bottom: 1px solid var(--pw-border);
      color: var(--pw-body);
      white-space: nowrap;
    }}
    .pw-sim-table td:first-child {{
      text-align: left;
      padding-left: 10px;
      color: var(--pw-ink);
      font-weight: 500;
    }}
    .pw-sim-table tr.is-featured td {{
      background: var(--pw-sub);
      color: var(--pw-ink);
      font-weight: 600;
      border-bottom-color: #A7F3D0;
    }}
    .pw-sim-table tr.is-featured td:first-child {{
      border-left: 3px solid var(--pw-emerald);
      padding-left: 11px;
      color: var(--pw-emerald);
      font-weight: 700;
    }}
    .pw-sim-table tr.is-featured .pw-dd-neg,
    .pw-sim-table tr.is-featured .pw-eff-pos {{
      color: var(--pw-emerald);
    }}
    .pw-table-note {{
      margin: 12px 0 0;
      font-size: 0.79rem;
      line-height: 1.62;
      color: var(--pw-muted);
    }}
    .pw-primary-cta-wrap {{
      display: flex;
      flex-direction: column;
      align-items: flex-start;
      gap: 10px;
    }}
    .pw-btn-primary {{
      appearance: none;
      display: inline-flex;
      align-items: center;
      justify-content: center;
      gap: 10px;
      min-height: 56px;
      padding: 14px 28px;
      background: #0F172A;
      color: #FFFFFF !important;
      border: 1px solid #0F172A;
      border-radius: 4px;
      font-family: inherit;
      font-size: 1rem;
      font-weight: 600;
      text-decoration: none !important;
      cursor: pointer;
      transition: background 0.16s ease;
    }}
    .pw-btn-primary:hover {{
      background: #1E293B;
    }}
    .pw-btn-emerald {{
      background: #065F46;
      border-color: #065F46;
    }}
    .pw-btn-emerald:hover {{
      background: #047857;
    }}
    .pw-cta-caption {{
      font-size: 0.82rem;
      color: var(--pw-muted);
    }}
    .pw-live-temp-pill {{
      display: inline-flex;
      align-items: center;
      gap: 9px;
      padding: 8px 14px;
      margin: 0 0 16px;
      background: var(--pw-surface);
      border: 1px solid var(--pw-border-strong);
      border-radius: 999px;
      font-size: 0.82rem;
      font-weight: 600;
      font-variant-numeric: tabular-nums;
      color: var(--pw-body);
    }}
    .pw-live-dot {{
      width: 8px;
      height: 8px;
      border-radius: 50%;
      background: var(--pw-emerald);
      flex-shrink: 0;
    }}
    .pw-above-fold-cta {{
      margin: 0 0 28px;
    }}

    /* Screen 1: Step-Up Assessment */
    .pw-step-card {{
      background: var(--pw-surface);
      border: 1px solid var(--pw-border);
      border-radius: 6px;
      padding: 32px 30px;
    }}
    .pw-step-top {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 12px;
    }}
    .pw-back-btn {{
      appearance: none;
      background: none;
      border: none;
      padding: 4px 0;
      font-family: inherit;
      font-size: 0.86rem;
      font-weight: 500;
      color: var(--pw-body);
      cursor: pointer;
    }}
    .pw-step-counter {{
      font-family: 'Inter', sans-serif;
      font-size: 0.76rem;
      font-weight: 600;
      letter-spacing: 0.12em;
      color: var(--pw-muted);
      font-variant-numeric: tabular-nums;
    }}
    .pw-progress-line {{
      width: 100%;
      height: 2px;
      background: var(--pw-border);
      margin-bottom: 28px;
      overflow: hidden;
    }}
    .pw-progress-fill {{
      display: block;
      height: 100%;
      background: var(--pw-emerald);
      transition: width 0.22s ease;
    }}
    .pw-q-title {{
      font-family: 'Shippori Mincho', 'Noto Serif JP', Georgia, serif;
      font-weight: 600;
      font-size: clamp(1.35rem, 2.8vw, 1.75rem);
      line-height: 1.4;
      color: var(--pw-ink);
      margin: 0 0 8px;
    }}
    .pw-q-sub {{
      margin: 0 0 22px;
      font-size: 0.92rem;
      color: var(--pw-muted);
    }}
    .pw-option-list {{
      display: flex;
      flex-direction: column;
      gap: 10px;
    }}
    .pw-opt-btn {{
      appearance: none;
      width: 100%;
      text-align: left;
      background: var(--pw-bg);
      border: 1px solid var(--pw-border-strong);
      border-radius: 4px;
      padding: 16px 18px;
      cursor: pointer;
      display: flex;
      flex-direction: column;
      gap: 4px;
      font-family: inherit;
    }}
    .pw-opt-btn:hover {{
      border-color: var(--pw-ink);
      background: var(--pw-surface);
    }}
    .pw-opt-btn.is-selected {{
      border-color: var(--pw-emerald);
      border-width: 1.5px;
      background: var(--pw-sub);
    }}
    .pw-opt-head {{
      display: flex;
      justify-content: space-between;
      align-items: baseline;
      gap: 12px;
    }}
    .pw-opt-num {{
      font-family: 'Inter', sans-serif;
      font-size: 0.75rem;
      font-weight: 600;
      letter-spacing: 0.08em;
      color: var(--pw-muted);
      margin-right: 8px;
    }}
    .pw-opt-title {{
      font-size: 1rem;
      font-weight: 600;
      color: var(--pw-ink);
    }}
    .pw-opt-desc {{
      font-size: 0.88rem;
      line-height: 1.6;
      color: var(--pw-body);
    }}
    .pw-scale-grid {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(145px, 1fr));
      gap: 10px;
    }}
    .pw-scale-btn {{
      appearance: none;
      min-height: 64px;
      padding: 12px 10px;
      background: var(--pw-bg);
      border: 1px solid var(--pw-border-strong);
      border-radius: 4px;
      font-family: inherit;
      font-variant-numeric: tabular-nums;
      font-size: 0.98rem;
      font-weight: 600;
      color: var(--pw-ink);
      cursor: pointer;
      line-height: 1.35;
    }}
    .pw-scale-btn.is-selected {{
      border-color: var(--pw-emerald);
      border-width: 1.5px;
      background: var(--pw-sub);
      color: var(--pw-emerald);
    }}

    /* Screen 2: Partial Baseline Gate */
    .pw-gate-card {{
      background: var(--pw-surface);
      border: 1px solid var(--pw-border);
      border-radius: 6px;
      padding: 30px 28px;
      margin-bottom: 28px;
    }}
    .pw-profile-strip {{
      display: flex;
      justify-content: space-between;
      align-items: baseline;
      flex-wrap: wrap;
      gap: 10px;
      padding: 10px 14px;
      background: var(--pw-bg);
      border: 1px solid var(--pw-border);
      border-radius: 4px;
      font-size: 0.85rem;
      color: var(--pw-body);
      margin-bottom: 20px;
    }}
    .pw-inline-link {{
      appearance: none;
      background: none;
      border: none;
      padding: 0;
      font-family: inherit;
      font-size: 0.85rem;
      font-weight: 600;
      color: var(--pw-navy);
      text-decoration: underline;
      text-underline-offset: 3px;
      cursor: pointer;
    }}
    .pw-email-form {{
      display: flex;
      flex-wrap: wrap;
      gap: 10px;
      margin-top: 16px;
    }}
    .pw-email-input {{
      flex: 1 1 250px;
      width: 100%;
      min-width: 180px;
      box-sizing: border-box;
      min-height: 52px;
      padding: 12px 16px;
      background: var(--pw-surface);
      border: 1px solid #94A3B8;
      border-radius: 4px;
      font-family: inherit;
      font-size: 1rem;
      color: var(--pw-ink);
    }}
    #pwRestoreModalJp .pw-email-input {{
      flex: 0 0 auto;
    }}
    .pw-ratio-bar {{
      display: flex;
      width: 100%;
      height: 12px;
      border-radius: 2px;
      overflow: hidden;
      margin: 18px 0 16px;
      background: var(--pw-border);
    }}
    .pw-ratio-grid {{
      display: grid;
      grid-template-columns: repeat(3, 1fr);
      gap: 12px;
      margin-bottom: 18px;
      font-variant-numeric: tabular-nums;
    }}
    .pw-ratio-cell {{
      padding: 14px;
      background: var(--pw-bg);
      border: 1px solid var(--pw-border);
      border-radius: 4px;
    }}
    .pw-ratio-ticker {{
      font-family: 'Inter', 'Noto Sans JP', sans-serif;
      font-size: 0.74rem;
      font-weight: 600;
      letter-spacing: 0.06em;
      color: var(--pw-muted);
    }}
    .pw-ratio-pct {{
      font-family: 'Inter', sans-serif;
      font-size: 1.55rem;
      font-weight: 700;
      color: var(--pw-ink);
      margin: 2px 0;
    }}
    .pw-ratio-name {{
      font-size: 0.82rem;
      color: var(--pw-body);
    }}
    .pw-gated-preview-list {{
      margin-top: 18px;
      padding-top: 16px;
      border-top: 1px solid var(--pw-border);
      display: flex;
      flex-direction: column;
      gap: 8px;
    }}
    .pw-gated-row {{
      display: flex;
      justify-content: space-between;
      align-items: baseline;
      flex-wrap: wrap;
      gap: 8px;
      padding: 10px 12px;
      background: var(--pw-bg);
      border: 1px solid var(--pw-border);
      border-radius: 4px;
      font-size: 0.88rem;
      color: var(--pw-body);
    }}
    .pw-gated-badge {{
      font-family: 'Inter', 'Noto Sans JP', sans-serif;
      font-size: 0.74rem;
      font-weight: 600;
      letter-spacing: 0.06em;
      color: var(--pw-navy);
    }}

    /* Screen 3: 2-Tier Differentiated Paid Membership */
    .pw-tiers-section {{
      padding-top: 8px;
    }}
    .pw-tier-grid {{
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 18px;
      margin-top: 18px;
    }}
    .pw-tier-card {{
      background: var(--pw-surface);
      border: 1px solid var(--pw-border);
      border-radius: 6px;
      padding: 26px 24px;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
    }}
    .pw-tier-card.is-annual {{
      border-color: var(--pw-emerald);
      border-width: 1.5px;
    }}
    .pw-tier-kicker {{
      font-family: 'Inter', 'Noto Sans JP', sans-serif;
      font-size: 0.73rem;
      font-weight: 600;
      letter-spacing: 0.08em;
      color: var(--pw-muted);
      margin-bottom: 6px;
    }}
    .pw-tier-card.is-annual .pw-tier-kicker {{
      color: var(--pw-emerald);
    }}
    .pw-tier-name {{
      font-family: 'Shippori Mincho', 'Noto Serif JP', Georgia, serif;
      font-size: 1.32rem;
      font-weight: 600;
      color: var(--pw-ink);
      margin: 0 0 8px;
    }}
    .pw-tier-price {{
      font-variant-numeric: tabular-nums;
      font-size: 1.28rem;
      font-weight: 700;
      color: var(--pw-ink);
      margin-bottom: 4px;
    }}
    .pw-tier-saving {{
      font-size: 0.82rem;
      font-weight: 600;
      color: var(--pw-emerald);
      margin-bottom: 16px;
    }}
    .pw-tier-list {{
      list-style: none;
      padding: 16px 0 0;
      margin: 0 0 22px;
      border-top: 1px solid var(--pw-border);
      display: flex;
      flex-direction: column;
      gap: 10px;
      font-size: 0.9rem;
      line-height: 1.65;
      color: var(--pw-body);
    }}
    .pw-tier-list li {{
      position: relative;
      padding-left: 16px;
    }}
    .pw-tier-list li::before {{
      content: "—";
      position: absolute;
      left: 0;
      color: var(--pw-emerald);
      font-weight: 600;
    }}
    .pw-mor-note {{
      margin-top: 16px;
      font-size: 0.8rem;
      color: var(--pw-muted);
      line-height: 1.6;
    }}

    /* Quiet 1-Line Legal Footer */
    .pw-legal-footer {{
      max-width: 820px;
      margin: 0 auto;
      padding: 20px 24px 40px;
      border-top: 1px solid var(--pw-border);
      font-size: 0.8rem;
      line-height: 1.65;
      color: var(--pw-muted);
    }}
    .pw-legal-links {{
      display: flex;
      flex-wrap: wrap;
      gap: 8px 14px;
      margin-bottom: 6px;
    }}
    .pw-legal-links a {{
      color: var(--pw-body);
      text-decoration: none;
    }}
    .pw-legal-links a:hover {{
      color: var(--pw-ink);
      text-decoration: underline;
    }}
    .pw-legal-disclaimer {{
      margin: 0;
      font-size: 0.77rem;
      color: var(--pw-muted);
    }}

    /* Shared Modal Rules */
    .pw-modal-backdrop, .pw-modal-backdrop * {{
      box-sizing: border-box;
    }}
    .pw-modal-backdrop {{
      display: none;
      position: fixed;
      inset: 0;
      z-index: 10040;
      background: rgba(15, 23, 42, 0.58);
      backdrop-filter: blur(3px);
      padding: 20px 14px;
      align-items: center;
      justify-content: center;
      overflow-y: auto;
    }}
    .pw-modal-backdrop.is-open {{ display: flex; }}
    .pw-modal-dialog {{
      width: 100%;
      max-width: 560px;
      background: #FFFFFF;
      border: 1px solid #CBD5E1;
      border-radius: 6px;
      padding: 26px 22px;
      color: #0F172A;
      max-height: calc(100vh - 32px);
      overflow-x: hidden;
      overflow-y: auto;
    }}
    .gba-manual-free-badge {{ display:inline-flex; align-items:center; gap:6px; background:#065F46; color:#FFFFFF; font-size:0.78rem; font-weight:600; padding:4px 10px; border-radius:4px; }}
    .gba-manual-modal-backdrop {{ display:none; position:fixed; inset:0; z-index:9999; background:rgba(15,23,42,0.65); backdrop-filter:blur(3px); padding:18px 12px; overflow-y:auto; align-items:flex-start; justify-content:center; }}
    .gba-manual-modal-backdrop.is-open {{ display:flex; }}
    .gba-manual-modal-dialog {{ background:#FFFFFF; color:#0F172A; border:1px solid #CBD5E1; border-radius:6px; width:100%; max-width:820px; margin:12px auto 32px; overflow:hidden; }}
    .gba-manual-modal-header {{ position:sticky; top:0; z-index:5; background:#FFFFFF; border-bottom:1px solid #E2E8F0; padding:16px 20px; display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:10px; }}
    .gba-manual-modal-title {{ font-size:1.15rem; font-weight:700; color:#0F172A; margin:4px 0 0; }}
    .gba-manual-modal-actions {{ display:flex; gap:8px; flex-wrap:wrap; }}
    .gba-manual-action-btn {{ appearance:none; min-height:42px; padding:8px 14px; border-radius:4px; font-size:0.88rem; font-weight:600; cursor:pointer; border:1px solid #CBD5E1; background:#FBFBF9; color:#0F172A; }}
    .gba-manual-nav-pills {{ display:flex; flex-wrap:wrap; gap:8px; padding:12px 20px; background:#FBFBF9; border-bottom:1px solid #E2E8F0; }}
    .gba-manual-jump-pill {{ appearance:none; min-height:38px; padding:6px 12px; border-radius:4px; border:1px solid #CBD5E1; background:#FFFFFF; color:#0F172A; font-size:0.85rem; font-weight:600; cursor:pointer; }}
    .gba-manual-modal-body {{ padding:22px 20px; font-size:0.96rem; line-height:1.78; }}
    .gba-manual-chapter-box {{ background:#FBFBF9; border:1px solid #E2E8F0; border-radius:6px; padding:18px; margin-bottom:16px; }}
    .gba-manual-broker-grid {{ display:grid; grid-template-columns:repeat(auto-fit, minmax(250px, 1fr)); gap:12px; margin-top:10px; }}
    .gba-manual-broker-card {{ background:#FFFFFF; border:1px solid #E2E8F0; border-radius:4px; padding:14px; }}
    .gba-manual-tip-callout {{ margin-top:12px; padding:12px 14px; border-radius:4px; background:#F3F8F5; border-left:3px solid #065F46; font-weight:500; }}
    .gba-manual-modal-funnel {{ background:#FBFBF9; border:1px solid #E2E8F0; border-radius:6px; padding:18px; margin-top:10px; }}
    .gba-manual-open-btn {{ appearance:none; background:#065F46; color:#FFFFFF; border:none; border-radius:4px; padding:12px 18px; min-height:48px; font-size:0.94rem; font-weight:600; cursor:pointer; }}
    .gba-manual-funnel-links {{ display:flex; flex-wrap:wrap; gap:10px; margin-top:10px; }}
    .gba-manual-pro-link, .gba-manual-vip-link {{ display:inline-flex; align-items:center; min-height:42px; padding:8px 14px; border-radius:4px; font-size:0.88rem; font-weight:600; text-decoration:none; background:#FFFFFF; border:1px solid #1E3A8A; color:#1E3A8A; }}

    @media (max-width: 768px) {{
      .pw-shell {{ padding: 24px 18px 36px; }}
      .pw-step-card, .pw-gate-card {{ padding: 22px 18px; }}
      .pw-table-card {{ padding: 18px 14px 14px; }}
      .pw-tier-grid, .pw-ratio-grid {{ grid-template-columns: 1fr; }}
      .pw-btn-primary {{ width: 100%; }}
    }}
    @media print {{
      body.printing-gba-manual > *:not(#gbaStarterManualModal) {{ display: none !important; }}
      body.printing-gba-manual #gbaStarterManualModal {{ display: block !important; position: static !important; background: #ffffff !important; padding: 0 !important; }}
    }}
    body[data-cro-density="cro-pad-compact"] .pw-shell {{ padding: 24px 20px 36px; }}
    body[data-cro-density="cro-pad-compact"] .pw-masthead {{ margin-bottom: 24px; padding-bottom: 14px; }}
    body[data-cro-density="cro-pad-airy"] .pw-shell {{ padding: 48px 28px 60px; }}
    body[data-cro-density="cro-pad-airy"] .pw-masthead {{ margin-bottom: 52px; padding-bottom: 24px; }}
  </style>
</head>
<body>
  <main id="gba-retirement-architect-jp" class="pw-shell">
    <header class="pw-masthead">
      <button type="button" class="pw-brand-btn" onclick="showPwScreenJp(0)">
        <span class="pw-wordmark">GETBREAK AI &middot; JAPAN</span>
        <span class="pw-submark">新NISA・資産リサーチ研究室（教育目的）</span>
      </button>
      <button type="button" class="pw-signin-link" id="btnOpenPwRestoreJp" onclick="openPwRestoreModalJp()">保存済みデータの復元</button>
    </header>

    <!-- Screen 0: Above-the-Fold Instant Start CTA + Live Market Temperature + Founding Note & 2000-2025 Statistical Case Study Table -->
    <section id="pwScreen0Jp" data-pw-screen="0">
      <div class="pw-kicker">新NISA・資産リサーチ研究室（教育目的） &middot; セクター過去統計エクスプローラー（2000–2025年統計比較）</div>
      <h1 class="pw-serif-h1">騒がしい銘柄探しを手放し、二つの柱で老後資産を守り抜くために。</h1>

      <a href="/jp/smh-fear-greed" class="pw-live-temp-pill" id="gbaLiveTempBadgeJp" role="status" aria-live="polite" style="text-decoration:none;cursor:pointer;">
        <span class="pw-live-dot" aria-hidden="true"></span>
        <span id="gbaLiveTempTextJp">{live_temp_text_jp}</span>
      </a>

      <div class="pw-primary-cta-wrap pw-above-fold-cta">
        <button type="button" class="pw-btn-primary pw-btn-emerald" id="btnStartPwStepUpJp" onclick="startPwStepUpJp()">
          新NISA 米国配当10%課税・暴落耐性を30秒無料確認 &rarr;
        </button>
        <span class="pw-cta-caption">日本語・証券口座ログイン不要 ・ 2000–2025年統計比較をメール壁なしで即時開示</span>
      </div>

      <figure class="pw-editorial-figure">
        <div class="pw-editorial-plate">
          <img src="/assets/gba-private-wealth-engawa.jpg" alt="静かな朝の光が差し込む書斎と縁側の水彩画" width="1200" height="675" loading="eager" decoding="async">
        </div>
        <figcaption class="pw-editorial-caption">日々の相場ノイズから離れ、公開統計データとともに新NISAと老後資産の歴史的回復力を静かに学ぶ研究室。</figcaption>
      </figure>

      <div class="pw-manifesto">
        <p>
          退職前後や50〜70代のご世帯が大切な老後資金や新NISA枠で眠れぬ夜を過ごす理由は、知識や努力が足りないからではありません。日々あふれ返る個別株の話題や短期ブームを追いかけるうちに、知らぬ間に資産の大半が単一のハイテク銘柄へと偏り、数年に一度の深い調整局面を無防備なまま迎えてしまうことにあります。
        </p>
        <p>
          私たちが <strong>GetBreakAI（新NISA・資産リサーチ研究室）</strong> を立ち上げた理由は明快です。投資助言や個別銘柄の売買推奨を一切行わず、<strong>「米国半導体の構造的成長（SMH）」</strong>と、景気や金利に左右されにくい<strong>「米国ヘルスケアの生活必需キャッシュフロー（XLV）」</strong>という二つの現物1倍ETF（ともに<strong>新NISA 成長投資枠</strong>対象）に、個人向け国債や<strong>特定口座</strong>（毎月分配型米国短期国債ETF SGOV等）の安全クッションを添えた歴史的データが、過去25年間の暴落局面をどう通過したかを客観的に記録・教育するためです。
        </p>
        <p>
          当研究室は<strong>「{SOFTWARE_POSITIONING_JP}」</strong>として運営されています。まずは無料の4問エクスプローラーにて、2000〜2025年の統計比較比率をメール登録なしで今すぐお確かめください。
        </p>
      </div>

      <div class="pw-table-card" role="region" aria-label="2000〜2025年 ヒストリカル統計比較表">
        <div class="pw-table-header">
          <span class="pw-table-title">TABLE I &mdash; 2000〜2025年 セクター過去統計ケーススタディ比較</span>
          <span class="pw-table-meta">レバレッジなし現物1倍指数・ETF基準</span>
        </div>
        <div class="pw-table-scroll">
          <table class="pw-sim-table">
            <thead>
              <tr>
                <th>過去統計ケーススタディ</th>
                <th>年率複利 (CAGR)</th>
                <th>最大下落率 (Max DD)</th>
                <th>高値回復期間</th>
                <th>効率比 (CAGR/|DD|)</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td>S&amp;P 500 単独</td>
                <td>~7.9%</td>
                <td class="pw-dd-neg">-50.9%</td>
                <td>56ヶ月</td>
                <td>0.16x</td>
              </tr>
              <tr>
                <td>伝統的 60/40 分散</td>
                <td>~6.4%</td>
                <td class="pw-dd-neg">-32.3%</td>
                <td>31ヶ月</td>
                <td>0.20x</td>
              </tr>
              <tr>
                <td>SMH 100% 単独</td>
                <td>~11.8%</td>
                <td class="pw-dd-neg">-74.6%</td>
                <td>89ヶ月</td>
                <td>0.16x</td>
              </tr>
              <tr class="is-featured">
                <td>SMH &times; XLV バランス統計ケース</td>
                <td>~11.4%</td>
                <td class="pw-dd-neg">-27.8%</td>
                <td>19ヶ月</td>
                <td class="pw-eff-pos">0.41x</td>
              </tr>
            </tbody>
          </table>
        </div>
        <p class="pw-table-note">
          公開指数・現物ETF終値（2000〜2025年、年2回の定率比率比較モデル）に基づく教育・情報提供目的の過去統計比較であり、投資助言や将来の運用成果の保証ではありません（SMH・XLVは新NISA成長投資枠対象、毎月分配型SGOV等は金融庁規定により{FSA_HYBRID_PHRASE_JP}に準拠し特定口座で区分管理）。
        </p>
      </div>

      <div class="pw-primary-cta-wrap">
        <button type="button" class="pw-btn-primary pw-btn-emerald" id="btnPwStartStepUpJp" onclick="startPwStepUpJp()">
          新NISA 米国配当10%課税・暴落耐性を30秒無料確認 &rarr;
        </button>
        <span class="pw-cta-caption">全4問（1問ずつ進行） ・ 登録不要で即時表示 ・ 証券口座ログイン不要</span>
      </div>
    </section>

    <!-- Screen 1: Focused 1-Question-at-a-Time Step-Up Explorer (Step 1 of 4 -> Step 4 of 4) -->
    <section id="pwScreen1Jp" data-pw-screen="1" style="display:none;">
      <div class="pw-step-card">
        <div class="pw-step-top">
          <button type="button" class="pw-back-btn" id="btnPwStepBackJp" onclick="prevPwStepJp()">&larr; 戻る</button>
          <span class="pw-step-counter" id="pwStepCounterJp">STEP 01 OF 04</span>
        </div>
        <div class="pw-progress-line" aria-hidden="true">
          <span class="pw-progress-fill" id="pwStepProgressFillJp" style="width:25%;"></span>
        </div>

        <div data-pw-qpane-jp="1">
          <h2 class="pw-q-title">2000〜2025年の過去統計で、最も比較したい視点はどれですか？</h2>
          <p class="pw-q-sub">学習・比較したい歴史的セクター統計ケースをひとつお選びください。</p>
          <div class="pw-option-list" role="radiogroup" aria-label="過去統計の比較視点">
            <button type="button" class="pw-opt-btn" data-pw-jfield="objective" data-pw-jval="growth" onclick="selectPwOptionJp('objective', 'growth')">
              <div class="pw-opt-head"><span><span class="pw-opt-num">I</span><span class="pw-opt-title">半導体成長（SMH）主軸の長期統計ケース</span></span><span>&rarr;</span></div>
              <span class="pw-opt-desc">半導体（SMH）比率を高めに置きつつ、ヘルスケア（XLV）が過去の下落幅をどう緩和したかを比較します。</span>
            </button>
            <button type="button" class="pw-opt-btn is-selected" data-pw-jfield="objective" data-pw-jval="balanced" onclick="selectPwOptionJp('objective', 'balanced')">
              <div class="pw-opt-head"><span><span class="pw-opt-num">II</span><span class="pw-opt-title">成長と下落耐性を均衡させた標準統計ケース</span></span><span>&rarr;</span></div>
              <span class="pw-opt-desc">SMHの成長力とXLVのディフェンシブ性を均衡させた25年間の標準バランス統計を確認します。</span>
            </button>
            <button type="button" class="pw-opt-btn" data-pw-jfield="objective" data-pw-jval="preservation" onclick="selectPwOptionJp('objective', 'preservation')">
              <div class="pw-opt-head"><span><span class="pw-opt-num">III</span><span class="pw-opt-title">下落抑制・安全クッション重視の統計ケース</span></span><span>&rarr;</span></div>
              <span class="pw-opt-desc">医療（XLV）と個人向け国債・特定口座SGOVの安全クッションを厚くした過去推移を確認します。</span>
            </button>
          </div>
        </div>

        <div data-pw-qpane-jp="2" style="display:none;">
          <h2 class="pw-q-title">試算モデルとして参照したい想定規模をお選びください。</h2>
          <p class="pw-q-sub">新NISA成長投資枠（SMH・XLV）と個人向け国債・特定口座クッションの統計金額換算にのみ使用されます。</p>
          <div class="pw-scale-grid" role="radiogroup" aria-label="想定規模">
            <button type="button" class="pw-scale-btn" data-pw-jfield="scale" data-pw-jval="300" onclick="selectPwOptionJp('scale', 300)">300万円</button>
            <button type="button" class="pw-scale-btn" data-pw-jfield="scale" data-pw-jval="1000" onclick="selectPwOptionJp('scale', 1000)">1,000万円</button>
            <button type="button" class="pw-scale-btn is-selected" data-pw-jfield="scale" data-pw-jval="1800" onclick="selectPwOptionJp('scale', 1800)">1,800万円<br><small style="font-weight:500;font-size:0.78rem;">新NISA生涯枠</small></button>
            <button type="button" class="pw-scale-btn" data-pw-jfield="scale" data-pw-jval="3000" onclick="selectPwOptionJp('scale', 3000)">3,000万円</button>
            <button type="button" class="pw-scale-btn" data-pw-jfield="scale" data-pw-jval="5000" onclick="selectPwOptionJp('scale', 5000)">5,000万円+</button>
          </div>
        </div>

        <div data-pw-qpane-jp="3" style="display:none;">
          <h2 class="pw-q-title">過去の暴落局面における、比較したい最大下落幅レンジはどれですか？</h2>
          <p class="pw-q-sub">2000年ITバブル・2008年リーマン危機・2022年利上げ局面での統計レンジを選択します。</p>
          <div class="pw-option-list" role="radiogroup" aria-label="過去下落幅レンジ">
            <button type="button" class="pw-opt-btn" data-pw-jfield="comfort" data-pw-jval="dd10" onclick="selectPwOptionJp('comfort', 'dd10')">
              <div class="pw-opt-head"><span><span class="pw-opt-num">I</span><span class="pw-opt-title">穏やかな変動レンジ（安全クッション厚め）</span></span><span>&rarr;</span></div>
              <span class="pw-opt-desc">XLVに加え、個人向け国債・特定口座SGOVの比率を高めた低変動統計ケースを参照します。</span>
            </button>
            <button type="button" class="pw-opt-btn is-selected" data-pw-jfield="comfort" data-pw-jval="dd18" onclick="selectPwOptionJp('comfort', 'dd18')">
              <div class="pw-opt-head"><span><span class="pw-opt-num">II</span><span class="pw-opt-title">標準2本柱レンジ（2000–2025年 基本ケース）</span></span><span>&rarr;</span></div>
              <span class="pw-opt-desc">過去25年統計の標準的な SMH &times; XLV バランスケースを参照します。</span>
            </button>
            <button type="button" class="pw-opt-btn" data-pw-jfield="comfort" data-pw-jval="dd25" onclick="selectPwOptionJp('comfort', 'dd25')">
              <div class="pw-opt-head"><span><span class="pw-opt-num">III</span><span class="pw-opt-title">長期成長重視レンジ（半導体比率高め）</span></span><span>&rarr;</span></div>
              <span class="pw-opt-desc">中間調整の振れ幅を許容し、長期の半導体セクター統計比率を高めたケースを参照します。</span>
            </button>
          </div>
        </div>

        <div data-pw-qpane-jp="4" style="display:none;">
          <h2 class="pw-q-title">比較対象とする現在のハイテク・半導体比率はどの程度ですか？</h2>
          <p class="pw-q-sub">単一セクター集中ケースと2本柱過去統計ケースの差分を整理します。</p>
          <div class="pw-option-list" role="radiogroup" aria-label="比較対象のハイテク比率">
            <button type="button" class="pw-opt-btn is-selected" data-pw-jfield="techMix" data-pw-jval="tech_high" onclick="selectPwOptionJp('techMix', 'tech_high')">
              <div class="pw-opt-head"><span><span class="pw-opt-num">I</span><span class="pw-opt-title">70%超（ハイテク・半導体株中心）</span></span></div>
              <span class="pw-opt-desc">単一セクターの設備投資サイクルと、医療ディフェンシブ柱を組み合わせた過去統計を比較。</span>
            </button>
            <button type="button" class="pw-opt-btn" data-pw-jfield="techMix" data-pw-jval="tech_mid" onclick="selectPwOptionJp('techMix', 'tech_mid')">
              <div class="pw-opt-head"><span><span class="pw-opt-num">II</span><span class="pw-opt-title">30〜70%（複数セクター・投信に分散）</span></span></div>
              <span class="pw-opt-desc">既存の分散構成を、明快な2セクター過去統計モデルと比較したい方向け。</span>
            </button>
            <button type="button" class="pw-opt-btn" data-pw-jfield="techMix" data-pw-jval="tech_low" onclick="selectPwOptionJp('techMix', 'tech_low')">
              <div class="pw-opt-head"><span><span class="pw-opt-num">III</span><span class="pw-opt-title">30%未満（預貯金・広く分散された指数中心）</span></span></div>
              <span class="pw-opt-desc">待機資金やインデックス中心と、2本柱＋国債クッションの歴史的推移を比較したい方向け。</span>
            </button>
          </div>
          <div style="margin-top:24px;">
            <button type="button" class="pw-btn-primary pw-btn-emerald" id="btnSubmitPwAssessmentJp" style="width:100%;" onclick="submitPwAssessmentJp()">
              過去25年の統計比較要約を表示する（無料） &rarr;
            </button>
          </div>
        </div>
      </div>
    </section>

    <!-- Screen 2: Immediate Free Historical Baseline Study Summary (ZERO Email Wall!) + Optional 1-Line Passwordless Save Box -->
    <section id="gbaMorningClubJp" data-pw-screen="2" style="display:none;">
      <div class="pw-gate-card">
        <div class="pw-profile-strip">
          <span id="pwProfileSummaryJp">比較条件：標準統計ケース ・ 1,800万円（新NISA生涯枠） ・ 標準2本柱レンジ</span>
          <button type="button" class="pw-inline-link" onclick="editPwInputsJp()">比較条件を変更する</button>
        </div>

        <!-- Immediately Revealed Free Historical Baseline Study Summary -->
        <div id="pwFreeBaselineSummaryJp">
          <div class="pw-kicker">FREE HISTORICAL STUDY SUMMARY &middot; セクター過去統計エクスプローラー（2000–2025年統計比較）</div>
          <h2 class="pw-serif-h2" id="pwUnlockedRatioHeadlineJp">SMH 55% &middot; XLV 35% &middot; 個人向け国債／SGOV 10%</h2>
          <p style="margin:0;color:var(--pw-body);font-size:0.93rem;">
            2000〜2025年の現物ETF公開データにおける過去統計比較比率です（SMH・XLV＝新NISA成長投資枠対象、安全資産クッション＝個人向け国債 変動10年 または特定口座SGOV ／ 個別の投資助言ではありません）。証券アプリの口座区分・基本設定は <button type="button" class="pw-inline-link" id="gbaFreeStarterManualJp" onclick="openGbaStarterManualModal()">無料（¥0）楽天・SBI証券 新NISA口座区分ガイド</button> をご参照ください。
          </p>

          <div class="pw-ratio-bar" id="pwRatioVisualBarJp" aria-hidden="true">
            <span style="width:55%;background:#0F172A;"></span>
            <span style="width:35%;background:#065F46;"></span>
            <span style="width:10%;background:#94A3B8;"></span>
          </div>

          <div class="pw-ratio-grid">
            <div class="pw-ratio-cell">
              <div class="pw-ratio-ticker">SMH &middot; 成長柱（新NISA成長枠）</div>
              <div class="pw-ratio-pct" id="pwPctSmhJp">55%</div>
              <div class="pw-ratio-name" id="pwAmtSmhJp">米国半導体現物ETF（約990万円）</div>
            </div>
            <div class="pw-ratio-cell">
              <div class="pw-ratio-ticker">XLV &middot; 防衛柱（新NISA成長枠）</div>
              <div class="pw-ratio-pct" id="pwPctXlvJp">35%</div>
              <div class="pw-ratio-name" id="pwAmtXlvJp">米国ヘルスケア現物ETF（約630万円）</div>
            </div>
            <div class="pw-ratio-cell">
              <div class="pw-ratio-ticker">CUSHION &middot; 安全資産クッション</div>
              <div class="pw-ratio-pct" id="pwPctCushionJp">10%</div>
              <div class="pw-ratio-name" id="pwAmtCushionJp">個人向け国債／特定口座SGOV（約180万円）</div>
            </div>
          </div>

          <div class="pw-gated-preview-list">
            <div class="pw-gated-row">
              <span>2000–2025年 最大下落幅比較：SMH単独 <strong>-74.6%</strong> ・ S&amp;P500単独 <strong>-50.9%</strong> に対し、2本柱バランス統計は <strong id="pwHistDdCompareJp">-24.5%（回復目安 約18ヶ月）</strong></span>
              <span class="pw-gated-badge">過去統計検証値</span>
            </div>
          </div>
        </div>

        <!-- Screen 2 無料2pサンプルPDF（無料統計結果の直下に上方配置・Screen 0離脱防止） -->
        <div id="gbaScreen2SamplePdfBox" style="margin-top:18px;padding:14px 16px;background:#F3F8F5;border:1.5px solid #065F46;border-radius:8px;display:flex;flex-wrap:wrap;align-items:center;justify-content:space-between;gap:12px;">
          <div style="font-size:0.88rem;color:#0F172A;line-height:1.55;max-width:490px;">
            <strong>無料2ページ・サンプルPDFを先に確認：</strong> 2000&ndash;2025年危機別比較表と楽天・SBI証券の口座区分ダイジェスト（登録不要・無料）
          </div>
          <a href="/jp/downloads/gba_jp_sample_2p.pdf" target="_blank" rel="noopener" id="btnGbaScreen2SamplePdf" class="pw-btn-primary" style="background:#FFFFFF;color:#065F46;border:1.5px solid #065F46;padding:10px 16px;min-height:46px;font-size:0.88rem;text-decoration:none;">
            無料2pサンプルPDFを見る &rarr;
          </a>
        </div>

        <!-- Frictionless 1-Line Passwordless Email Box Directly Below Free Summary -->
        <div id="gba-jp-passwordless-signup" style="margin-top:24px; padding-top:20px; border-top:1px solid var(--pw-border);">
          <div class="pw-kicker" style="margin-bottom:6px;">FREE MORNING RESEARCH NOTES &middot; パスワード不要・1クリック解除OK</div>
          <h3 class="pw-serif-h2" style="font-size:1.25rem; margin-bottom:6px;">この統計要約を保存し、朝刊リサーチノートを受け取る（無料）</h3>
          <p style="margin:0;color:var(--pw-body);font-size:0.9rem;">
            メールアドレスを入力すると、上の過去統計比較要約をいつでも再表示でき、教育目的の朝刊市場データノートを無料でお届けします。
          </p>
          <form class="pw-email-form gba-jp-signup-form" id="gba-jp-club-form" onsubmit="return submitPwFreeGateJp(event)" novalidate>
            <input type="text" id="gba-jp-club-hp" name="website_hp" tabindex="-1" autocomplete="off" aria-hidden="true" style="display:none;">
            <input type="email" id="gba-jp-club-email" class="pw-email-input" required autocomplete="email" placeholder="メールアドレスを入力（例: yamada@example.jp）" aria-label="メールアドレス">
            <button type="submit" id="gba-jp-club-submit" class="pw-btn-primary pw-btn-emerald">
              無料で保存・購読する &rarr;
            </button>
          </form>
          <div id="pwGateStatusJp" role="status" aria-live="polite" style="display:none;margin-top:10px;font-size:0.88rem;color:#065F46;font-weight:600;"></div>
        </div>
      </div>
    </section>

    <!-- Screen 3: 2-Tier Whop Research Pass (#pricing — @whop/checkout Modal + Direct Tab Fallback) -->
    <section id="pricing" class="pw-tiers-section" data-pw-screen="3" style="display:none;">
      <span id="vip-vault" style="display:block;height:0;overflow:hidden;" aria-hidden="true"></span>
      <div class="pw-kicker">INDEPENDENT RESEARCH PASS &middot; 新NISA・資産リサーチ研究室（教育目的）</div>
      <h2 class="pw-serif-h2" id="pwPricingHeadlineJp">教育目的の市場データニュースレター ＋ 2000–2025年 過去統計ワークブック</h2>
      <p style="margin:0;color:var(--pw-body);font-size:0.92rem;">
        投資助言・個別推奨は一切行わない独立系リサーチ出版として、毎朝の公開市場温度データニュースレターと過去26年間の統計ワークブックをお届けします。
      </p>

      <div class="pw-tier-grid">
        <div class="pw-tier-card">
          <div>
            <div class="pw-tier-kicker">TIER I &middot; MONTHLY RESEARCH PASS</div>
            <h3 class="pw-tier-name">{PRICE_LABEL_MONTHLY_JP}</h3>
            <div class="pw-tier-price">¥4,400 <span style="font-size:0.86rem;font-weight:500;color:var(--pw-muted);">/ 月（税込）</span></div>
            <div class="pw-tier-saving">1ヶ月単位でいつでも1クリック解約可能</div>
            <ul class="pw-tier-list">
              <li><strong>教育目的の市場データニュースレター（毎朝8時配信）</strong>：日米市場温度指数（0〜100）と SMH &times; XLV 過去統計比率の推移記録</li>
              <li><strong>局面別セクター過去統計リファレンス表</strong>（2000〜2025年の過熱・中立・恐怖局面ごとの歴史的統計ウェイト）</li>
              <li><strong>新NISA成長投資枠・個人向け国債／特定口座 制度区分データノート</strong></li>
            </ul>
          </div>
          <a href="{WHOP_MONTHLY_CTA_HREF}" data-gba-paid-plan="monthly" data-whop-plan="monthly" class="pw-btn-primary whop-checkout-button" style="width:100%;">
            {PRICE_LABEL_MONTHLY_JP} を購読する &rarr;
          </a>
        </div>

        <div class="pw-tier-card is-annual">
          <div>
            <div class="pw-tier-kicker">TIER II &middot; ANNUAL RESEARCH PASS &middot; 44% OFF</div>
            <h3 class="pw-tier-name">{PRICE_LABEL_ANNUAL_JP}</h3>
            <div class="pw-tier-price">¥29,800 <span style="font-size:0.86rem;font-weight:500;color:var(--pw-muted);">/ 年（税込）</span></div>
            <div class="pw-tier-saving">月額換算 約2,483円（月額比 約44%割引）</div>
            <ul class="pw-tier-list">
              <li><strong>月額リサーチパスの全内容（12ヶ月間の毎朝市場データニュースレター配信）</strong></li>
              <li><strong>2000–2025年 過去統計ワークブック完全版（随時更新PDF）</strong>：ITバブル・リーマン危機・2022年利上げ局面の SMH &times; XLV ＋ 安全資産 統計比較集</li>
              <li><strong>新NISA成長投資枠・個人向け国債（変動10年）・特定口座SGOV 長期管理ガイドブック</strong></li>
            </ul>
          </div>
          <a href="{WHOP_ANNUAL_CTA_HREF}" data-gba-paid-plan="annual" data-whop-plan="annual" class="pw-btn-primary pw-btn-emerald whop-checkout-button" style="width:100%;">
            {PRICE_LABEL_ANNUAL_JP} を購読する &rarr;
          </a>
        </div>
      </div>

      <div style="margin-top:18px;padding:16px 18px;background:#F8FAFC;border:1px solid #CBD5E1;border-radius:10px;display:flex;flex-wrap:wrap;align-items:center;justify-content:space-between;gap:12px;">
        <div style="font-size:0.9rem;color:#334155;max-width:600px;line-height:1.65;">
          <strong style="color:#0F172A;">ご購入前の事前確認：</strong> 2000&ndash;2025年危機別比較表と楽天iSPEED・SBI証券の買い付け手順ダイジェストを収めた無料2ページ・サンプルPDFを先にご確認いただけます。
        </div>
        <a href="/jp/downloads/gba_jp_sample_2p.pdf" target="_blank" rel="noopener" class="pw-btn-primary" style="background:#FFFFFF;color:#0F2C22;border:1.5px solid #0F2C22;padding:10px 18px;font-size:0.92rem;text-decoration:none;">
          無料2pサンプルPDFを見る &rarr;
        </a>
      </div>
      <p class="pw-mor-note" style="line-height:1.72;">
        <strong>デジタルコンテンツ標準返金・解約ポリシー：</strong> ①未閲覧・未ダウンロード時は決済後7日以内100%全額返金 ②デジタルPDF・コンテンツ閲覧／ダウンロード開始後の自己都合返金不可（上記無料2pサンプルを必ず事前にご確認ください） ③ファイル不具合・システム障害・重複決済時は100%返金 ④定期購読は違約金なし・いつでも1クリックで次回決済停止可能。<br>
        公式決済基盤：{MOR_LABEL_EN_JP}（日本円 JPY 建て請求：月額 ¥4,400 / 年額 ¥29,800） ・ お問い合わせ：<a href="mailto:support@getbreakai.com" style="color:inherit;text-decoration:underline;">support@getbreakai.com</a> ・ <a href="/jp/archive.html" style="color:inherit;text-decoration:underline;">月次あんしんレポート・アーカイブ</a><br>
        提供区分：「{SOFTWARE_POSITIONING_JP}」
      </p>
      <div style="margin-top:18px;padding:16px 18px;background:#FFFFFF;border:1px solid #E2E8F0;border-radius:10px;font-size:0.88rem;color:#475569;">
        <strong style="color:#0F172A;">初期読者レビュー募集：</strong> 無料サンプルPDFや新NISA 1,800万円ワークブックをご覧になったご感想をぜひお寄せください。<a href="mailto:support@getbreakai.com?subject=GetBreakAI%20Reader%20Review" style="color:#065F46;font-weight:700;text-decoration:underline;margin-left:6px;">2行レビューを送る &rarr;</a>
      </div>
    </section>

    <!-- Screen 4: Paid Research Vault JP (円建て SMH x XLV + 個人向け国債/SGOV PDF・-35%ストレステスト・新NISA 1,800万円非課税ロードマップ・楽天/SBI 5分図解・月次あんしん成績表) -->
    <section id="gbaPaidScreen4VaultJp" class="pw-tiers-section" data-pw-screen="4" style="display:none;margin-top:28px;">
      <div class="pw-gate-card" style="border:1.5px solid #065F46;background:#FFFFFF;">
        <div class="pw-kicker" style="color:#065F46;">PAID RESEARCH VAULT &middot; スマホ・PC共通 永久復元エディション</div>
        <h2 class="pw-serif-h2" id="gbaScreen4HeadlineJp">円建て SMH &times; XLV ＋ 個人向け国債／SGOV セルフサービス自動計算統計ワークブック</h2>
        <p style="margin:0 0 16px;color:#475569;font-size:0.95rem;">
          ご自身の世帯想定規模（万円）を入力すると、円建て金額シミュレーション、-35%暴落耐性ストレステスト、新NISA 1,800万円（成長240万＋つみたて120万）非課税ロードマップ、楽天証券・SBI証券の大きな文字5分注文図解、毎月1日の『月次あんしん成績表』が即座に更新されます。
        </p>

        <div style="display:flex;flex-wrap:wrap;align-items:center;gap:12px;padding:14px 16px;background:#F8FAFC;border:1px solid #CBD5E1;border-radius:8px;margin-bottom:18px;">
          <label for="gbaCustomManYenInput" style="font-weight:700;font-size:0.98rem;color:#0F172A;">世帯想定規模（単位：万円）：</label>
          <input type="number" id="gbaCustomManYenInput" min="100" max="100000" step="100" value="1800" oninput="onGbaManYenInput()" style="padding:10px 14px;border:1px solid #94A3B8;border-radius:6px;font-size:1.05rem;font-weight:700;width:160px;font-variant-numeric:tabular-nums;">
          <button type="button" class="pw-btn-primary pw-btn-emerald" id="btnDownloadGbaMaster12pPdf" onclick="downloadProtectedGbaPdfJp()">
            12p 新NISA完全版ワークブックPDFをダウンロード &rarr;
          </button>
          <button type="button" class="pw-btn-primary" id="btnDownloadGbaCustomPdf" onclick="openGbaCustomPdfWindowJp()" style="background:#FFFFFF;color:#0F2C22;border:1.5px solid #0F2C22;">
            カスタム金額シートを印刷 &rarr;
          </button>
          <a href="/jp/archive.html" style="font-weight:700;color:#065F46;text-decoration:underline;font-size:0.9rem;">月次あんしんレポート・Q&amp;Aアーカイブ &rarr;</a>
        </div>

        <div id="gbaScreen4YenTable" class="pw-table-card" style="margin-bottom:18px;"></div>
        <div id="gbaScreen4StressTest" class="pw-table-card" style="margin-bottom:18px;"></div>
        <div id="gbaScreen4NisaRoadmap" class="pw-table-card" style="margin-bottom:18px;padding:18px;"></div>
        <div id="gbaScreen4BrokerGuide" class="pw-table-card" style="margin-bottom:18px;padding:18px;"></div>
        <div id="gbaScreen4MonthlyCard" class="pw-table-card" style="margin-bottom:18px;padding:18px;"></div>

        <div style="padding:16px;background:#ECFDF5;border:1px solid #6EE7B7;border-radius:8px;margin-bottom:14px;">
          <div class="pw-kicker" style="color:#065F46;margin-bottom:6px;">永久復元マジックリンク ＆ デジタルサポート・標準返金窓口</div>
          <p style="margin:0 0 10px;font-size:0.92rem;color:#064E3B;">
            機種変更後や別端末（スマホ・タブレット・PC）からも1クリックで本画面とPDFを復元できる専用リンクをメール宛にお送りします：
          </p>
          <form onsubmit="return submitGbaPaidMagicEmailJp(event)" class="pw-email-form" novalidate>
            <input type="email" id="gbaPaidMagicEmailInput" class="pw-email-input" placeholder="ご登録メールアドレスを入力" autocomplete="email">
            <button type="submit" class="pw-btn-primary pw-btn-emerald">永久復元リンクをメール送信 &rarr;</button>
          </form>
          <div id="gbaPaidMagicStatus" role="status" aria-live="polite" style="display:none;margin-top:8px;font-size:0.88rem;font-weight:600;color:#065F46;"></div>
          <div style="margin-top:10px;font-size:0.86rem;color:#334155;">
            標準デジタル返金・1クリックサポート：<a id="gbaOneClickRefundLink" href="mailto:support@getbreakai.com?subject=GetBreakAI%20Support%20or%20Refund" style="color:#065F46;font-weight:700;text-decoration:underline;">1クリック返金・お問い合わせ申請（support@getbreakai.com）</a>
          </div>
        </div>

        <div id="gbaSatisfactionMount"></div>
      </div>
    </section>
  </main>

  <footer class="pw-legal-footer">
    <div class="pw-legal-links">
      <span>GetBreakAI Japan Research</span>
      <span>&middot;</span>
      <a href="/jp/terms.html">利用規約</a>
      <span>&middot;</span>
      <a href="/jp/privacy.html">プライバシーポリシー</a>
      <span>&middot;</span>
      <a href="/jp/refund.html">返金・解約ポリシー</a>
      <span>&middot;</span>
      <a href="/jp/tokushoho.html">特定商取引法に基づく表記</a>
      <span>&middot;</span>
      <a href="/jp/contact.html">お問い合わせ</a>
      <span>&middot;</span>
      <a href="https://www.youtube.com/@GetBreakAI" target="_blank" rel="noopener">公式YouTube @GetBreakAI</a>
      <span>&middot;</span>
      <a href="https://www.instagram.com/getbreakai/" target="_blank" rel="noopener">公式Instagram @getbreakai</a>
      <span>&middot;</span>
      <a href="mailto:support@getbreakai.com">support@getbreakai.com</a>
    </div>
    <p class="pw-legal-disclaimer">{MANDATORY_DISCLAIMER_JP}</p>
  </footer>

  <!-- Member Sign-In / Restore Modal (0 Emojis) -->
  <div class="pw-modal-backdrop" id="pwRestoreModalJp" role="dialog" aria-modal="true" aria-labelledby="pwRestoreTitleJp">
    <div class="pw-modal-dialog">
      <div style="display:flex;justify-content:space-between;align-items:center;gap:12px;margin-bottom:14px;">
        <span class="pw-kicker" style="margin:0;">MEMBER ACCESS &amp; RESTORE</span>
        <button type="button" class="pw-back-btn" style="min-height:44px;min-width:72px;padding:8px 14px;border:1px solid #CBD5E1;border-radius:4px;background:#F8FAFC;text-decoration:none;flex-shrink:0;" onclick="closePwRestoreModalJp()">閉じる</button>
      </div>
      <h3 class="pw-serif-h2" id="pwRestoreTitleJp" style="font-size:1.45rem;">保存済み統計要約・購読パスの復元</h3>
      <p style="margin:0 0 16px;font-size:0.9rem;color:#475569;">
        ご登録メールアドレスを入力して保存済みの過去統計比較要約を再表示するか、Whop.com 決済完了メール記載の領収書番号をご入力ください。
      </p>
      <form onsubmit="return submitPwRestoreJp(event)" novalidate style="display:flex;flex-direction:column;gap:12px;">
        <input type="email" id="pwRestoreEmailJp" class="pw-email-input" placeholder="Whop決済時のメールアドレス" autocomplete="email">
        <input type="text" id="jpHubLicenseInput" class="pw-email-input" placeholder="アクセスコード・領収書ID・または6桁認証コード" autocomplete="one-time-code">
        <div style="display:flex;gap:8px;flex-wrap:wrap;">
          <button type="submit" class="pw-btn-primary pw-btn-emerald" style="flex:1;min-width:170px;">認証して開く &rarr;</button>
          <button type="button" onclick="requestGbaOtpJp()" class="pw-btn-primary" style="background:#FFFFFF;color:#0F2C22;border:1.5px solid #0F2C22;">6桁コードを送信</button>
        </div>
      </form>
      <div id="jpHubVipStatus" role="status" aria-live="polite" style="display:none;margin-top:12px;font-size:0.88rem;color:#065F46;"></div>
    </div>
  </div>

{manual_modal}
{waitlist_modal}

  <script>
    let pwCurrentScreenJp = 0;
    let pwCurrentStepJp = 1;
    let pwAnswersJp = {{
      objective: 'balanced',
      scale: 1800,
      comfort: 'dd18',
      techMix: 'tech_high'
    }};

    function toggleJpTheme() {{
      const cur = document.documentElement.getAttribute('data-jp-theme') || 'light';
      const next = cur === 'light' ? 'dark' : 'light';
      document.documentElement.setAttribute('data-jp-theme', next);
      try {{ localStorage.setItem('gb_jp_theme', next); }} catch (_) {{}}
    }}

    let gbaLiveTempScoreJp = 11;
    let gbaLiveTempDateJp = '2026-11-18';

    function hydrateGbaLiveTempBadgeJp() {{
      const txtEl = document.getElementById('gbaLiveTempTextJp');
      if (!txtEl || typeof fetch !== 'function') return;
      const applyData = function(ov) {{
        if (!ov || typeof ov !== 'object') return;
        const dt = String(ov.date || ov.as_of_date || '').trim();
        const rawSc = (ov.fg_score !== undefined) ? ov.fg_score : ((ov.fear_greed_score !== undefined) ? ov.fear_greed_score : ov.score);
        const numSc = Number(rawSc);
        if (!dt || isNaN(numSc)) return;
        const sc = Math.round(numSc);
        gbaLiveTempScoreJp = sc;
        gbaLiveTempDateJp = dt;
        let reg = '中立圏';
        if (sc <= 25) reg = '極度の恐怖圏';
        else if (sc <= 44) reg = '慎重・警戒圏';
        else if (sc <= 55) reg = '中立圏';
        else if (sc <= 75) reg = '強気圏';
        else reg = '過熱注意圏';
        txtEl.textContent = '最新データ基準日：' + dt + ' ・ 市場温度指数：' + sc + ' / 100（' + reg + '）';
        renderGbaScreen4VaultJp();
      }};
      fetch('/data/semi_overview.json', {{ cache: 'no-cache' }})
        .then(function(r) {{ return r.ok ? r.json() : Promise.reject(); }})
        .then(applyData)
        .catch(function() {{
          fetch('/static_api/semi_overview.json', {{ cache: 'no-cache' }})
            .then(function(r2) {{ return r2.ok ? r2.json() : null; }})
            .then(applyData)
            .catch(function() {{}});
        }});
    }}

    function loadPwSavedAnswersJp() {{
      try {{
        const raw = localStorage.getItem('gba_pw_stepup_answers_v1');
        if (raw) {{
          const parsed = JSON.parse(raw);
          if (parsed && typeof parsed === 'object') {{
            pwAnswersJp = Object.assign(pwAnswersJp, parsed);
          }}
        }}
      }} catch (_) {{}}
    }}

    function computePwBaselineJp() {{
      const obj = pwAnswersJp.objective || 'balanced';
      const comfort = pwAnswersJp.comfort || 'dd18';
      const scale = Number(pwAnswersJp.scale) || 1800;

      let smh = 55;
      let xlv = 35;
      let cushion = 10;

      if (obj === 'growth') {{
        smh = 68; xlv = 27; cushion = 5;
      }} else if (obj === 'preservation') {{
        smh = 35; xlv = 45; cushion = 20;
      }}

      if (comfort === 'dd10') {{
        smh = Math.max(25, smh - 12);
        xlv = xlv + 5;
        cushion = 100 - smh - xlv;
      }} else if (comfort === 'dd25') {{
        cushion = Math.max(0, cushion - 5);
        smh = smh + 8;
        xlv = 100 - smh - cushion;
      }}

      const objLbl = obj === 'growth' ? '半導体成長統計ケース' : (obj === 'preservation' ? '安全クッション重視ケース' : '標準統計ケース');
      const scaleLbl = scale >= 5000 ? '5,000万円+' : (scale === 1800 ? '1,800万円（新NISA生涯枠）' : scale.toLocaleString() + '万円');
      const ddLbl = comfort === 'dd10' ? '穏やか変動レンジ' : (comfort === 'dd25' ? '長期成長レンジ' : '標準2本柱レンジ');

      const smhMan = Math.round(scale * smh / 100);
      const xlvMan = Math.round(scale * xlv / 100);
      const cushMan = Math.max(0, scale - smhMan - xlvMan);
      const estDd = comfort === 'dd10' ? '-17.8%（回復目安 約13ヶ月）' : (comfort === 'dd25' ? '-31.2%（回復目安 約22ヶ月）' : '-24.5%（回復目安 約18ヶ月）');

      return {{
        smh: smh,
        xlv: xlv,
        cushion: cushion,
        smhMan: smhMan,
        xlvMan: xlvMan,
        cushMan: cushMan,
        estDd: estDd,
        headline: 'SMH ' + smh + '% ・ XLV ' + xlv + '% ・ 個人向け国債／SGOV ' + cushion + '%',
        summary: '比較条件：' + objLbl + ' ・ ' + scaleLbl + ' ・ ' + ddLbl
      }};
    }}

    function getSavedGbaEmailJp() {{
      try {{
        if (window.DreamCompanyCRM && typeof window.DreamCompanyCRM.getLocalMember === 'function') {{
          const m = window.DreamCompanyCRM.getLocalMember('GBA');
          if (m && m.email) return String(m.email).trim().toLowerCase();
        }}
        return String(localStorage.getItem('gba_jp_free_email') || localStorage.getItem('gb_free_member_email') || '').trim().toLowerCase();
      }} catch (_) {{
        return '';
      }}
    }}

    function syncPwStage2UiJp() {{
      const b = computePwBaselineJp();
      const sumEl = document.getElementById('pwProfileSummaryJp');
      if (sumEl) sumEl.textContent = b.summary;
      const hlEl = document.getElementById('pwUnlockedRatioHeadlineJp');
      if (hlEl) hlEl.textContent = b.headline;

      const pSmh = document.getElementById('pwPctSmhJp');
      const pXlv = document.getElementById('pwPctXlvJp');
      const pCush = document.getElementById('pwPctCushionJp');
      if (pSmh) pSmh.textContent = b.smh + '%';
      if (pXlv) pXlv.textContent = b.xlv + '%';
      if (pCush) pCush.textContent = b.cushion + '%';

      const aSmh = document.getElementById('pwAmtSmhJp');
      const aXlv = document.getElementById('pwAmtXlvJp');
      const aCush = document.getElementById('pwAmtCushionJp');
      if (aSmh) aSmh.textContent = '米国半導体現物ETF（約' + b.smhMan.toLocaleString() + '万円）';
      if (aXlv) aXlv.textContent = '米国ヘルスケア現物ETF（約' + b.xlvMan.toLocaleString() + '万円）';
      if (aCush) aCush.textContent = '個人向け国債／特定口座SGOV（約' + b.cushMan.toLocaleString() + '万円）';

      const ddCmp = document.getElementById('pwHistDdCompareJp');
      if (ddCmp) ddCmp.textContent = b.estDd;

      const bar = document.getElementById('pwRatioVisualBarJp');
      if (bar) {{
        bar.innerHTML =
          '<span style="width:' + b.smh + '%;background:#0F172A;"></span>' +
          '<span style="width:' + b.xlv + '%;background:#065F46;"></span>' +
          '<span style="width:' + b.cushion + '%;background:#94A3B8;"></span>';
      }}

      const em = getSavedGbaEmailJp();
      const inp = document.getElementById('gba-jp-club-email');
      if (inp && em && !inp.value) inp.value = em;
    }}

    function fmtManYenJp(n) {{
      return Math.round(Number(n) || 0).toLocaleString('ja-JP') + '万円';
    }}

    function renderGbaScreen4VaultJp() {{
      const b = computePwBaselineJp();
      const inp = document.getElementById('gbaCustomManYenInput');
      const totalMan = Math.max(100, Number(inp && inp.value ? inp.value : pwAnswersJp.scale) || 1800);
      if (inp && Number(inp.value) !== totalMan) inp.value = String(totalMan);

      const smhMan = Math.round(totalMan * b.smh / 100);
      const xlvMan = Math.round(totalMan * b.xlv / 100);
      const cushMan = Math.max(0, totalMan - smhMan - xlvMan);

      const yenTbl = document.getElementById('gbaScreen4YenTable');
      if (yenTbl) {{
        yenTbl.innerHTML =
          '<div class="pw-table-header"><span class="pw-table-title">第1章 — 円建て世帯規模ワークシート（想定総額：' + fmtManYenJp(totalMan) + '）</span><span class="pw-table-meta">現物1倍ETF・国債過去統計</span></div>' +
          '<div class="pw-table-scroll"><table class="pw-sim-table"><thead><tr><th>構成区分</th><th>過去統計比率</th><th>円建て目安金額</th><th>2000〜2025年統計における役割</th></tr></thead><tbody>' +
          '<tr><td><strong>SMH</strong>（米国半導体現物ETF）</td><td>' + b.smh + '%</td><td style="font-variant-numeric:tabular-nums;font-weight:700;">' + fmtManYenJp(smhMan) + '</td><td>AI・半導体技術革新による長期成長エンジン</td></tr>' +
          '<tr><td><strong>XLV</strong>（米国ヘルスケア現物ETF）</td><td>' + b.xlv + '%</td><td style="font-variant-numeric:tabular-nums;font-weight:700;">' + fmtManYenJp(xlvMan) + '</td><td>景気後退局面でも底堅い生活必須医療キャッシュフロー</td></tr>' +
          '<tr class="is-featured"><td><strong>個人向け国債（変動10年）／SGOV</strong></td><td>' + b.cushion + '%</td><td style="font-variant-numeric:tabular-nums;font-weight:700;">' + fmtManYenJp(cushMan) + '</td><td>暴落時に株式を売却せず生活費を守る安全クッション</td></tr>' +
          '</tbody></table></div>';
      }}

      const tech49 = Math.round(totalMan * 0.49);
      const sp35 = Math.round(totalMan * 0.35);
      const studyPct = Math.round((0.46 * (b.smh / 100) + 0.16 * (b.xlv / 100)) * 1000) / 10;
      const studyLoss = Math.round(totalMan * (studyPct / 100));
      const stressEl = document.getElementById('gbaScreen4StressTest');
      if (stressEl) {{
        stressEl.innerHTML =
          '<div class="pw-table-header"><span class="pw-table-title">第2章 — -35%暴落局面ストレステスト（' + fmtManYenJp(totalMan) + ' 基準）</span><span class="pw-table-meta">下落耐性比較</span></div>' +
          '<div class="pw-table-scroll"><table class="pw-sim-table"><thead><tr><th>比較ケース</th><th>想定下落幅</th><th>評価変動額</th><th>残存評価額＆安全資産クッション</th></tr></thead><tbody>' +
          '<tr><td>半導体単独（SMH 100%）</td><td class="pw-dd-neg">-49.0%</td><td class="pw-dd-neg">-' + fmtManYenJp(tech49) + '</td><td>' + fmtManYenJp(totalMan - tech49) + '（国債バッファ 0円）</td></tr>' +
          '<tr><td>S&amp;P 500単独</td><td class="pw-dd-neg">-35.0%</td><td class="pw-dd-neg">-' + fmtManYenJp(sp35) + '</td><td>' + fmtManYenJp(totalMan - sp35) + '（国債バッファ 0円）</td></tr>' +
          '<tr class="is-featured"><td><strong>選択中の SMH &times; XLV ＋ 安全資産ケース</strong></td><td class="pw-eff-pos">-' + studyPct.toFixed(1) + '%</td><td class="pw-eff-pos">-' + fmtManYenJp(studyLoss) + '</td><td><strong>' + fmtManYenJp(totalMan - studyLoss) + '（安全資産 ' + fmtManYenJp(cushMan) + ' 無傷）</strong></td></tr>' +
          '</tbody></table></div>' +
          '<p class="pw-table-note">※教育目的の過去統計シミュレーションです。個人向け国債（変動10年）や短期米国債ETF（SGOV）を別枠で確保しておくことで、市場回復までの約18ヶ月間も落ち着いて保有を継続しやすくなります。</p>';
      }}

      const equityTotalMan = smhMan + xlvMan;
      const nisaGrowthSlot = Math.min(1200, equityTotalMan);
      const equityOverflowAfterGrowth = Math.max(0, equityTotalMan - nisaGrowthSlot);
      const nisaTsumitateSlot = Math.min(600, equityOverflowAfterGrowth);
      const overflowTaxableEquityMan = Math.max(0, equityOverflowAfterGrowth - nisaTsumitateSlot);
      const totalOverflowAndSafetyMan = cushMan + overflowTaxableEquityMan;
      const nisaEl = document.getElementById('gbaScreen4NisaRoadmap');
      if (nisaEl) {{
        nisaEl.innerHTML =
          '<div class="pw-kicker" style="margin-bottom:6px;">第3章 — 新NISA 1,800万円法定上限完全準拠（合計一致検証：' + fmtManYenJp(nisaGrowthSlot + nisaTsumitateSlot + totalOverflowAndSafetyMan) + ' / ' + fmtManYenJp(totalMan) + '）</div>' +
          '<h3 style="margin:0 0 10px;font-size:1.15rem;color:#0F172A;">成長投資枠1,200万円＋つみたて枠600万円＋超過分の安全配置（1円も消失しない完全配分）</h3>' +
          '<div style="display:grid;gap:10px;font-size:0.94rem;color:#334155;">' +
          '<div style="padding:12px;background:#F8FAFC;border-left:3px solid #0F172A;border-radius:6px;"><strong>1. 新NISA 成長投資枠（年間上限240万円・生涯上限1,200万円 ／ 配置額：' + fmtManYenJp(nisaGrowthSlot) + '）：</strong> 現物1倍ETFである <strong>SMH × XLV</strong> を法定上限1,200万円まで優先配置します（3倍レバレッジETF・短期債SGOVは新NISA枠を使いません）。</div>' +
          '<div style="padding:12px;background:#F8FAFC;border-left:3px solid #065F46;border-radius:6px;"><strong>2. 新NISA つみたて投資枠（年間上限120万円・生涯上限600万円 ／ 配置額：' + fmtManYenJp(nisaTsumitateSlot) + '）：</strong> 成長枠1,200万円を超える長期株式分は、金融庁届出済みの低コスト広範インデックス投信で最大600万円の生涯非課税枠を5年計画で活用します。</div>' +
          '<div style="padding:12px;background:#F8FAFC;border-left:3px solid #64748B;border-radius:6px;"><strong>3. 生涯非課税枠超過分 ＆ 安全クッション（合計配置額：' + fmtManYenJp(totalOverflowAndSafetyMan) + ' ＝ 安全資産 ' + fmtManYenJp(cushMan) + ' ＋ 非課税枠超過分 ' + fmtManYenJp(overflowTaxableEquityMan) + '）：</strong> 新NISA対象外の安全バッファおよび1,800万円超過分は、<strong>個人向け国債（変動10年・元本割れなし）</strong>または<strong>特定口座（源泉徴収あり）内の SGOV・現物ETF</strong> に明確に分離配置します（米国ETF配当には米国10%源泉徴収＋日本課税の外国税額控除対象ルールを適用）。</div>' +
          '</div>';
      }}

      const brokerEl = document.getElementById('gbaScreen4BrokerGuide');
      if (brokerEl) {{
        brokerEl.innerHTML =
          '<div class="pw-kicker" style="margin-bottom:6px;">第4章 — 楽天証券・SBI証券 大きな文字（18px+）5分安全注文図解ガイド</div>' +
          '<h3 style="margin:0 0 10px;font-size:1.15rem;color:#0F172A;">見間違い・高値掴みを防ぐ4ステップ確認手順</h3>' +
          '<ol style="margin:0;padding-left:22px;font-size:1.02rem;line-height:1.85;color:#1E293B;">' +
          '<li><strong>注文時間帯の確認：</strong> 米国市場オープン直後15分間（日本時間23:30〜23:45／冬時間0:30〜0:45）のスプレッド拡大を避け、落ち着いた時間帯または事前の指値予約を利用します。</li>' +
          '<li><strong>ティッカーと現物1倍の確認：</strong> 楽天証券（iSPEED）またはSBI証券（米国株アプリ）で <strong>SMH</strong>・<strong>XLV</strong>・<strong>SGOV</strong> を検索し、レバレッジ型ではない現物ETFであることを確認します。</li>' +
          '<li><strong>「成行」ではなく必ず「指値（Limit）」を選択：</strong> 口座区分（「NISA成長投資枠」または「特定預り」）を確認のうえ、現在値付近の指値注文で安全に発注します。</li>' +
          '<li><strong>点検は年2回（1月・7月）のみ：</strong> 毎日の株価ニュースに振り回されず、半年ごとの比率確認だけで穏やかな老後時間を守ります。</li>' +
          '</ol>';
      }}

      const rebalDue = (gbaLiveTempScoreJp >= 78 || gbaLiveTempScoreJp <= 22);
      const verdictTxt = rebalDue
        ? '【今月の1秒判定：過去データ比率の定期点検タイミング】'
        : '【今月の1秒判定：維持して安心してお休みください】';
      const monthlyEl = document.getElementById('gbaScreen4MonthlyCard');
      if (monthlyEl) {{
        monthlyEl.innerHTML =
          '<div class="pw-kicker" style="margin-bottom:6px;">第5章 — 毎月1日『月次あんしん成績表』＆ 月1回『会員匿名Q&amp;A回報』</div>' +
          '<div style="padding:12px 16px;border-radius:8px;background:' + (rebalDue ? '#FEF3C7' : '#ECFDF5') + ';color:' + (rebalDue ? '#92400E' : '#065F46') + ';font-weight:800;font-size:1.02rem;margin-bottom:10px;">' + verdictTxt + ' ・ 市場温度 ' + gbaLiveTempScoreJp + ' / 100（' + gbaLiveTempDateJp + ' 基準）</div>' +
          '<p style="margin:0 0 8px;font-size:0.96rem;color:#334155;"><strong>先月の変動クッション要約：</strong> 半導体現物（SMH）にヘルスケア（XLV）と安全資産（' + fmtManYenJp(cushMan) + '）を組み合わせた2本柱ケースは、ハイテク単独保有と比べて穏やかな値動きを維持しました。</p>' +
          '<p style="margin:0;font-size:0.94rem;color:#475569;"><strong>今月の匿名Q&amp;A抜粋：</strong>「Q. 為替（円高・円安）が気になるときはどう考えればよいですか？」→「A. 米国株ETF（ドル資産）と日本円建ての個人向け国債（変動10年）を併用することで、通貨面でも自然な分散クッションが働きます（※教育目的の一般解説）。」</p>';
      }}

      const satEl = document.getElementById('gbaSatisfactionMount');
      if (satEl && !satEl.__mounted && window.DreamCompanyCRM && typeof window.DreamCompanyCRM.mountSatisfactionBar === 'function') {{
        satEl.__mounted = true;
        window.DreamCompanyCRM.mountSatisfactionBar(satEl, {{ div: 'GBA', context: 'screen4_paid_vault_jp', email: getSavedGbaEmailJp() }});
      }}
    }}

    function onGbaManYenInput() {{
      const inp = document.getElementById('gbaCustomManYenInput');
      pwAnswersJp.scale = Math.max(100, Number(inp ? inp.value : 1800) || 1800);
      renderGbaScreen4VaultJp();
    }}

    function openGbaCustomPdfWindowJp() {{
      renderGbaScreen4VaultJp();
      const s1 = (document.getElementById('gbaScreen4YenTable') || {{}}).innerHTML || '';
      const s2 = (document.getElementById('gbaScreen4StressTest') || {{}}).innerHTML || '';
      const s3 = (document.getElementById('gbaScreen4NisaRoadmap') || {{}}).innerHTML || '';
      const s4 = (document.getElementById('gbaScreen4BrokerGuide') || {{}}).innerHTML || '';
      const s5 = (document.getElementById('gbaScreen4MonthlyCard') || {{}}).innerHTML || '';
      const w = window.open('', '_blank');
      if (!w) {{ window.print(); return; }}
      w.document.write(
        '<!DOCTYPE html><html lang="ja"><head><meta charset="UTF-8"><title>GetBreakAI セルフサービス自動計算統計ワークブックPDF</title>' +
        '<style>body{{font-family:"Hiragino Kaku Gothic ProN",Meiryo,sans-serif;max-width:780px;margin:24px auto;padding:0 20px;color:#0f172a;font-size:16px;line-height:1.72;}}table{{width:100%;border-collapse:collapse;margin:12px 0;font-size:14px;}}th,td{{border:1px solid #cbd5e1;padding:9px 10px;text-align:left;}}th{{background:#f1f5f9;}}.page-break{{page-break-before:always;margin-top:26px;padding-top:18px;border-top:2px solid #0f172a;}}@media print{{.no-print{{display:none;}}}}</style></head><body>' +
        '<div class="no-print" style="padding:12px;background:#ecfdf5;border:1px solid #059669;border-radius:8px;margin-bottom:18px;"><strong>PDF保存の準備が完了しました：</strong> 印刷画面で「PDFに保存」を選択してください。 <button onclick="window.print()" style="margin-left:12px;padding:8px 16px;background:#065f46;color:#fff;border:none;border-radius:6px;font-weight:700;cursor:pointer;">PDFとして保存・印刷</button></div>' +
        '<h1>GetBreakAI — 新NISA・SMH &times; XLV ＋ 安全資産 セルフサービス自動計算統計ワークブック</h1>' +
        '<p style="font-size:13px;color:#475569;">独立系リサーチ出版（教育目的データ・投資助言非該当 ・ お問い合わせ: support@getbreakai.com）</p>' +
        '<div>' + s1 + '</div><div style="margin-top:18px;">' + s2 + '</div>' +
        '<div class="page-break">' + s3 + '</div><div class="page-break">' + s4 + '</div><div class="page-break">' + s5 + '</div>' +
        '</body></html>'
      );
      w.document.close();
      setTimeout(function() {{ try {{ w.print(); }} catch (_) {{}} }}, 350);
    }}

    function submitGbaPaidMagicEmailJp(ev) {{
      if (ev && ev.preventDefault) ev.preventDefault();
      const inp = document.getElementById('gbaPaidMagicEmailInput');
      const st = document.getElementById('gbaPaidMagicStatus');
      const em = String(inp && inp.value ? inp.value : getSavedGbaEmailJp()).trim().toLowerCase();
      if (!/^[^\\s@]+@[^\\s@]+\\.[^\\s@]{{2,}}$/.test(em)) {{
        if (st) {{
          st.style.display = 'block';
          st.style.color = '#991B1B';
          st.textContent = '正しいメールアドレスをご入力ください。';
        }}
        return false;
      }}
      if (window.DreamCompanyCRM && typeof window.DreamCompanyCRM.deliverPaidMagicPack === 'function') {{
        window.DreamCompanyCRM.deliverPaidMagicPack({{
          div: 'GBA',
          email: em,
          plan_tier: (localStorage.getItem('gb_vip_plan') === 'annual') ? '年間リサーチパス（¥29,800/年）' : '月額リサーチパス（¥4,400/月）',
          order_ref: localStorage.getItem('gb_vip_license_key') || 'GBA-MAGIC-LINK',
          base_url: 'https://getbreakai.com/jp/',
          hash_anchor: 'gbaPaidScreen4VaultJp',
          profile_state: pwAnswersJp
        }}).then(function(res) {{
          if (st) {{
            st.style.display = 'block';
            st.style.color = '#065F46';
            st.textContent = em + ' 宛に永久復元マジックリンク（未閲覧7日返金・1クリック解約案内付き）を送信しました。';
          }}
          const rf = document.getElementById('gbaOneClickRefundLink');
          if (rf && res && res.refund_support_url) rf.href = res.refund_support_url;
        }});
      }}
      return false;
    }}

    function showPwScreenJp(screenNum) {{
      pwCurrentScreenJp = screenNum;
      let isVipUnlocked = (screenNum === 4);
      try {{
        if (localStorage.getItem('gb_vip_unlocked') === 'true') isVipUnlocked = true;
      }} catch (_) {{}}
      const s0 = document.getElementById('pwScreen0Jp');
      const s1 = document.getElementById('pwScreen1Jp');
      const s2 = document.getElementById('gbaMorningClubJp');
      const s3 = document.getElementById('pricing');
      const s4 = document.getElementById('gbaPaidScreen4VaultJp');
      if (s0) s0.style.display = (screenNum === 0) ? 'block' : 'none';
      if (s1) s1.style.display = (screenNum === 1) ? 'block' : 'none';
      if (s2) s2.style.display = (screenNum >= 2) ? 'block' : 'none';
      if (s3) s3.style.display = (screenNum >= 2) ? 'block' : 'none';
      if (s4) s4.style.display = (screenNum === 4 || (screenNum >= 2 && isVipUnlocked)) ? 'block' : 'none';
      if (screenNum >= 2) {{
        syncPwStage2UiJp();
        if (s4 && s4.style.display === 'block') renderGbaScreen4VaultJp();
      }}
      window.scrollTo({{ top: 0, behavior: 'smooth' }});
    }}

    function showPwQuestionStepJp(stepNum) {{
      pwCurrentStepJp = Math.max(1, Math.min(4, stepNum));
      document.querySelectorAll('[data-pw-qpane-jp]').forEach(function(el) {{
        el.style.display = (Number(el.getAttribute('data-pw-qpane-jp')) === pwCurrentStepJp) ? 'block' : 'none';
      }});
      const cLbl = document.getElementById('pwStepCounterJp');
      if (cLbl) cLbl.textContent = 'STEP 0' + pwCurrentStepJp + ' OF 04';
      const fill = document.getElementById('pwStepProgressFillJp');
      if (fill) fill.style.width = (pwCurrentStepJp * 25) + '%';
      document.querySelectorAll('[data-pw-jfield]').forEach(function(btn) {{
        const f = btn.getAttribute('data-pw-jfield');
        const v = btn.getAttribute('data-pw-jval');
        const act = String(pwAnswersJp[f]) === String(v);
        btn.classList.toggle('is-selected', act);
      }});
    }}

    function startPwStepUpJp() {{
      showPwQuestionStepJp(1);
      showPwScreenJp(1);
    }}

    function prevPwStepJp() {{
      if (pwCurrentStepJp > 1) {{
        showPwQuestionStepJp(pwCurrentStepJp - 1);
      }} else {{
        showPwScreenJp(0);
      }}
    }}

    function selectPwOptionJp(field, val) {{
      pwAnswersJp[field] = val;
      try {{ localStorage.setItem('gba_pw_stepup_answers_v1', JSON.stringify(pwAnswersJp)); }} catch (_) {{}}
      showPwQuestionStepJp(pwCurrentStepJp);
      if (pwCurrentStepJp < 4) {{
        setTimeout(function() {{ showPwQuestionStepJp(pwCurrentStepJp + 1); }}, 150);
      }}
    }}

    function submitPwAssessmentJp() {{
      if (window.DreamCompanyCRM && typeof window.DreamCompanyCRM.trackFunnelEvent === 'function') {{
        window.DreamCompanyCRM.trackFunnelEvent('GBA', 'quiz_complete');
      }}
      showPwScreenJp(2);
    }}

    function editPwInputsJp() {{
      showPwQuestionStepJp(1);
      showPwScreenJp(1);
    }}

    function submitPwFreeGateJp(ev) {{
      if (ev && ev.preventDefault) ev.preventDefault();
      const hp = document.getElementById('gba-jp-club-hp');
      if (hp && hp.value) return false;
      const inp = document.getElementById('gba-jp-club-email');
      const st = document.getElementById('pwGateStatusJp');
      const btn = document.getElementById('gba-jp-club-submit');
      const email = String(inp ? inp.value : '').trim().toLowerCase();
      if (!/^[^\\s@]+@[^\\s@]+\\.[^\\s@]{{2,}}$/.test(email)) {{
        if (st) {{
          st.style.display = 'block';
          st.style.color = '#991B1B';
          st.textContent = '正しいメールアドレスをご入力ください。';
        }}
        if (inp && inp.focus) inp.focus();
        return false;
      }}
      if (btn) {{ btn.disabled = true; btn.textContent = '登録中...'; }}

      const b = computePwBaselineJp();
      const noteStr = 'site=getbreakai.com/jp/ | study_ratio=' + b.headline + ' | ' + b.summary;
      try {{
        const kst = new Date(Date.now() + 9 * 3600 * 1000).toISOString().slice(0, 10);
        localStorage.setItem('gba_jp_free_email', email);
        localStorage.setItem('gb_free_member_email', email);
        localStorage.setItem('gba_jp_free_since', kst);
        localStorage.setItem('dc_member_GBA', JSON.stringify({{
          div: 'GBA', email: email, nickname: '', segment: 'nisa_wealth_defense', notes: noteStr, joined_at: new Date().toISOString()
        }}));
        if (typeof window.trackGbaFreeSignup === 'function') window.trackGbaFreeSignup(email);
      }} catch (_) {{}}

      const done = function(res) {{
        if (btn) {{ btn.disabled = false; btn.innerHTML = (res && res.ok) ? '保存・購読登録済み' : '再試行する'; }}
        if (st) {{
          st.style.display = 'block';
          if (res && res.ok) {{
            st.style.color = '#065F46';
            st.textContent = 'サーバー登録完了：毎朝の朝刊リサーチノートを ' + email + ' 宛にお届けします（いつでも1クリック解除OK）。';
          }} else {{
            st.style.color = '#991B1B';
            st.textContent = '一時的な通信エラーが発生しました。少し時間をおいて再度お試しください。';
          }}
        }}
        syncPwStage2UiJp();
      }};

      if (window.DreamCompanyCRM && typeof window.DreamCompanyCRM.registerMember === 'function') {{
        window.DreamCompanyCRM.registerMember({{
          div: 'GBA', email: email, nickname: '', segment: 'nisa_wealth_defense', lang: 'ja-JP', notes: noteStr, message: noteStr
        }}).then(done).catch(function() {{ done({{ ok: false }}); }});
      }} else {{
        done({{ ok: false }});
      }}
      return false;
    }}

    function jumpFromManualToJpMail() {{
      if (typeof window.closeGbaStarterManualModal === 'function') window.closeGbaStarterManualModal();
      showPwScreenJp(2);
    }}

    function openPwRestoreModalJp() {{
      const m = document.getElementById('pwRestoreModalJp');
      if (!m) return;
      const saved = getSavedGbaEmailJp();
      const inp = document.getElementById('pwRestoreEmailJp');
      if (inp && saved && !inp.value) inp.value = saved;
      m.classList.add('is-open');
    }}

    function closePwRestoreModalJp() {{
      const m = document.getElementById('pwRestoreModalJp');
      if (m) m.classList.remove('is-open');
    }}

    function downloadProtectedGbaPdfJp() {{
      if (window.DreamCompanyCRM && typeof window.DreamCompanyCRM.openProtectedPdfDownload === 'function') {{
        return window.DreamCompanyCRM.openProtectedPdfDownload('GBA', 'gba_jp_nisa_12p', function() {{
          openPwRestoreModalJp();
        }});
      }}
      openPwRestoreModalJp();
      return false;
    }}

    function requestGbaOtpJp() {{
      const emInp = document.getElementById('pwRestoreEmailJp');
      const st = document.getElementById('jpHubVipStatus');
      const em = String(emInp ? emInp.value : '').trim().toLowerCase();
      if (!/^[^\\s@]+@[^\\s@]+\\.[^\\s@]{{2,}}$/.test(em)) {{
        if (st) {{
          st.style.display = 'block';
          st.style.color = '#991B1B';
          st.textContent = '先にWhop決済時のメールアドレスをご入力ください。';
        }}
        return false;
      }}
      if (st) {{
        st.style.display = 'block';
        st.style.color = '#334155';
        st.textContent = '6桁ワンタイム認証コードを送信しています...';
      }}
      if (window.DreamCompanyCRM && typeof window.DreamCompanyCRM.requestAuthOtp === 'function') {{
        window.DreamCompanyCRM.requestAuthOtp({{ div: 'GBA', email: em }}).then(function() {{
          if (st) {{
            st.style.display = 'block';
            st.style.color = '#065F46';
            st.textContent = '有効なご購入履歴が確認された場合、6桁認証コードをメール送信しました（10分間有効）。上の欄へ入力して認証してください。';
          }}
        }});
      }}
      return false;
    }}

    function syncStoredVipKeysOnHub() {{
      // Client-only key length checks disabled for Zero-Bypass security; active sessions verify server-side.
      return;
    }}

    function submitPwRestoreJp(ev) {{
      if (ev && ev.preventDefault) ev.preventDefault();
      const emInp = document.getElementById('pwRestoreEmailJp');
      const licInp = document.getElementById('jpHubLicenseInput');
      const st = document.getElementById('jpHubVipStatus');
      const em = String(emInp ? emInp.value : '').trim().toLowerCase();
      const lic = String(licInp ? licInp.value : '').trim();

      if (!/^[^\\s@]+@[^\\s@]+\\.[^\\s@]{{2,}}$/.test(em)) {{
        if (st) {{
          st.style.display = 'block';
          st.style.color = '#991B1B';
          st.textContent = 'Whop決済時にご使用されたメールアドレスをご入力ください。';
        }}
        return false;
      }}
      const isSixDigitOtp = /^\\d{{6}}$/.test(lic);
      if (!lic || (!isSixDigitOtp && lic.length < 6)) {{
        if (st) {{
          st.style.display = 'block';
          st.style.color = '#991B1B';
          st.textContent = 'アクセスコード・領収書IDを入力するか、「6桁コードを送信」ボタンを押してください。';
        }}
        return false;
      }}
      if (st) {{
        st.style.display = 'block';
        st.style.color = '#334155';
        st.textContent = 'サーバーでWhop会員権限を照合しています...';
      }}
      const reqPayload = isSixDigitOtp
        ? {{ div: 'GBA', email: em, otp: lic }}
        : {{ div: 'GBA', email: em, access_code: lic }};
      const vp = (window.DreamCompanyCRM && typeof window.DreamCompanyCRM.verifyEntitlement === 'function')
        ? window.DreamCompanyCRM.verifyEntitlement(reqPayload)
        : Promise.resolve({{ authorized: false }});
      vp.then(function(vres) {{
        try {{
          localStorage.setItem('gba_jp_free_email', em);
          localStorage.setItem('gb_free_member_email', em);
        }} catch (_) {{}}
        if (vres && vres.authorized) {{
          try {{
            localStorage.setItem('gb_vip_unlocked', 'true');
            localStorage.setItem('gb_vip_license_key', isSixDigitOtp ? 'OTP-VERIFIED' : lic);
            localStorage.setItem('gb_vip_key', isSixDigitOtp ? 'OTP-VERIFIED' : lic);
          }} catch (_) {{}}
          if (st) {{
            st.style.display = 'block';
            st.style.color = '#065F46';
            st.textContent = '有料会員パスが確認されました。12p完全版ワークブック画面を開きます。';
          }}
          setTimeout(function() {{ closePwRestoreModalJp(); showPwScreenJp(4); }}, 450);
        }} else {{
          try {{ localStorage.removeItem('gb_vip_unlocked'); }} catch (_) {{}}
          if (st) {{
            st.style.display = 'block';
            st.style.color = '#991B1B';
            st.textContent = '有効なWhop決済履歴が確認できませんでした。「6桁コードを送信」をお試しいただくか support@getbreakai.com へご連絡ください。';
          }}
        }}
      }});
      return false;
    }}

    function bindJpHubWhopCheckoutBridge() {{
      if (window.__jpHubWhopMsgBound) return;
      window.__jpHubWhopMsgBound = true;
      window.addEventListener('message', function(msgEvt) {{
        try {{
          if (!msgEvt || !msgEvt.origin) return;
          const origHost = new URL(String(msgEvt.origin)).hostname.toLowerCase();
          if (origHost !== 'whop.com' && !origHost.endsWith('.whop.com')) return;
          const payload = typeof msgEvt.data === 'string' ? JSON.parse(msgEvt.data) : msgEvt.data;
          if (payload && (payload.event === 'checkout.complete' || payload.type === 'checkout.succeeded' || payload.status === 'succeeded')) {{
            if (typeof window.closeGbaWhopCheckoutModal === 'function') window.closeGbaWhopCheckoutModal();
            openPwRestoreModalJp();
          }}
        }} catch (_) {{}}
      }});
    }}

    window.addEventListener('DOMContentLoaded', function() {{
      try {{
        const savedTheme = localStorage.getItem('gb_jp_theme');
        if (savedTheme === 'dark' || savedTheme === 'light') {{
          document.documentElement.setAttribute('data-jp-theme', savedTheme);
        }}
      }} catch (_) {{}}

      window.GBA_COPY_MODE = (window.PAYMENT_CONFIG && window.PAYMENT_CONFIG.STORE_LIVE_READY) ? 'LIVE_SHARP' : 'UNDERWRITING_SAFE';
      loadPwSavedAnswersJp();
      showPwQuestionStepJp(1);
      syncStoredVipKeysOnHub();
      bindJpHubWhopCheckoutBridge();
      hydrateGbaLiveTempBadgeJp();

      try {{
        if (window.DreamCompanyCRM && typeof window.DreamCompanyCRM.decodeMagicRestoreParam === 'function') {{
          const mObj = window.DreamCompanyCRM.decodeMagicRestoreParam(window.location.search || '');
          if (mObj && typeof mObj === 'object' && mObj.email && mObj.access_code && typeof window.DreamCompanyCRM.verifyEntitlement === 'function') {{
            if (mObj.objective) pwAnswersJp.objective = mObj.objective;
            if (mObj.scale) pwAnswersJp.scale = Number(mObj.scale) || 1800;
            if (mObj.comfort) pwAnswersJp.comfort = mObj.comfort;
            if (mObj.techMix) pwAnswersJp.techMix = mObj.techMix;
            localStorage.setItem('gba_pw_stepup_answers_v1', JSON.stringify(pwAnswersJp));
            localStorage.setItem('gba_jp_free_email', String(mObj.email).toLowerCase());
            window.DreamCompanyCRM.verifyEntitlement({{
              div: 'GBA',
              email: mObj.email,
              access_code: mObj.access_code,
              magic_restore: true
            }}).then(function(vr) {{
              if (vr && vr.authorized) {{
                localStorage.setItem('gb_vip_unlocked', 'true');
                showPwScreenJp(4);
              }} else {{
                openPwRestoreModalJp();
              }}
            }});
            return;
          }}
        }}
        const params = new URLSearchParams(window.location.search || '');
        const h = (window.location.hash || '').toLowerCase();
        if (params.get('payment') === 'success' || params.get('checkout_status') === 'succeeded') {{
          openPwRestoreModalJp();
        }} else if (h === '#pricing' || h === '#gbamorningclubjp') {{
          showPwScreenJp(2);
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
                if sym in live_tickers and not item.get("is_guide") and item["slug"] != "soxl-smh-semiconductor-timing.html":
                    item["entry"] = live_tickers[sym]["entry"]
                    item["atr"] = live_tickers[sym]["atr"]
        except Exception as e:
            print(f"[WARN] Could not merge live snapshot into SEO specs: {e}")

    urls = [
        "https://getbreakai.com/jp/",
        "https://getbreakai.com/jp/smh-fear-greed",
        "https://getbreakai.com/jp/nisa-quiet-barbell-essay",
        "https://getbreakai.com/jp/daily-nisa-quant-report",
        "https://getbreakai.com/jp/terms",
        "https://getbreakai.com/jp/privacy",
        "https://getbreakai.com/jp/refund",
        "https://getbreakai.com/jp/tokushoho",
        "https://getbreakai.com/jp/contact",
        "https://getbreakai.com/terms",
        "https://getbreakai.com/privacy",
        "https://getbreakai.com/refund",
        "https://getbreakai.com/tokushoho",
        "https://getbreakai.com/contact",
    ]
    jp_guides_dir = os.path.join(JP_DIR, "guides")
    if os.path.isdir(jp_guides_dir):
        urls.append("https://getbreakai.com/jp/guides/")
        for fn in sorted(os.listdir(jp_guides_dir)):
            if fn.endswith(".html") and fn != "index.html":
                urls.append(f"https://getbreakai.com/jp/guides/{fn[:-5]}")
    flagship_html = build_flagship_essay_jp_html(date_str)
    with open(os.path.join(JP_DIR, "nisa-quiet-barbell-essay.html"), "w", encoding="utf-8") as ef:
        ef.write(flagship_html)

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
            clean_s = spec["slug"][:-5] if spec["slug"].endswith(".html") else spec["slug"]
            urls.append(f"https://getbreakai.com/jp/{clean_s}")

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
