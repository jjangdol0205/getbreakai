#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
scripts/upgrade_jp_fintech_uiux.py
4사업부 (GetBreakAI — getbreakai.com)
일본 투자자(米国株・新NISA・株クラ)가 가장 신뢰하고 선호하는 '일본 증권사·카부탄(株探)·버핏코드(バフェット・コード) 스타일'
고신뢰·고밀도·일람성 UI/UX로 index.html 및 /jp/*.html 30종을 전면 업그레이드합니다.

핵심 일본형 UI/UX 반영 사항:
1. [신뢰감 1위 컬러 시스템] 일본 증권사 표준 '도쿄 파이낸셜 네이비(#0B1F3A) & 클린 화이트/아이보리(#F4F6FA / #FFFFFF)' 기본 테마 + 상단 원클릭 '🌙 プロダーク / 🌞 証券ライト' 테마 전환 스위치 제공
2. [일본어 조판 최적화] Noto Sans JP + Hiragino Kaku Gothic ProN + Yu Gothic + Meiryo, font-feature-settings: "palt", 숫자 tabular-nums 정렬, 꼼꼼한 테두리(罫線) 및 번호 배지(STEP 01~03, POINT 01~03)
3. [원터치 엔화(¥) 자금 프리셋 & 환율 버튼] 슬라이더뿐 아니라 일본인이 직관적으로 누르는 [100万円] [300万円] [500万円] [750万円] [1,000万円] [1,200万円(新NISA成長枠満額)] 원터치 버튼 및 [1ドル=145円 / 150円 / 155円 / 160円] 환율 전환 버튼 탑재
4. [시각적 주가 위치 온도계 바 (#gbVisualRangeBar)] 2.0x ATR 손절라인 ── 현재주가 ── 5일 Gamma Wall ── 2.5R 목표가의 위치 관계를 한눈에 보여주는 일본 증권사 스타일 시각 게이지 바 탑재
5. [오늘의 미국주 AI 시그널 조견표 (本日の米国株AIシグナル早見表)] 일본인이 가장 좋아하는 '한눈에 보는 표(一覧表)'를 상단에 배치해 행 클릭만으로 즉시 종목 전환
6. [일본인 안심 FAQ 섹션 & 모바일 하단 고정 퀵바] 결제 전 의구심을 없애는 일본어 Q&A 4문 4답 및 스마트폰 한 손 조작 하단 탭바 탑재
"""

import os
import re

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INDEX_PATH = os.path.join(ROOT_DIR, "index.html")
JP_DIR = os.path.join(ROOT_DIR, "jp")


def upgrade_main_index():
    with open(INDEX_PATH, "r", encoding="utf-8") as f:
        html = f.read()

    # 1. Inject Japanese Fintech Light/Dark Dual Theme CSS + Mobile Bottom Bar + Quick Matrix styles before </style>
    jp_fintech_css = """
    /* === 日本人投資家向け「大手ネット証券・株探スタイル」高信頼UI/UXテーマ === */
    html[data-jp-theme="light"] {
      --bg-dark: #f4f6fa;
      --bg-card: #ffffff;
      --bg-card-hover: #f8fafc;
      --border-color: #d8e0ed;
      --border-accent: #1d4ed8;
      --text-main: #0f172a;
      --text-muted: #334155;
      --text-sub: #64748b;
      --accent-violet: #1d4ed8;
      --accent-amber: #b45309;
      --accent-emerald: #047857;
      --accent-rose: #be123c;
      --accent-sky: #0369a1;
      --glow-violet: rgba(29, 78, 216, 0.12);
      --glow-amber: rgba(180, 83, 9, 0.12);
    }

    html[data-jp-theme="light"] body {
      background-color: #f4f6fa;
      background-image: linear-gradient(180deg, #eef2f9 0%, #f4f6fa 320px);
      color: #0f172a;
    }

    html[data-jp-theme="light"] header {
      background: #0b1f3a !important;
      border-bottom: 2px solid #1e3a8a !important;
    }

    html[data-jp-theme="light"] header .brand-logo,
    html[data-jp-theme="light"] header .nav-links a {
      color: #f8fafc !important;
    }

    html[data-jp-theme="light"] .catalyst-tape {
      background: #102a4c !important;
      color: #f1f5f9 !important;
      border-bottom: 1px solid #1e3a8a !important;
    }

    html[data-jp-theme="light"] .tape-item {
      color: #e2e8f0 !important;
    }

    html[data-jp-theme="light"] .hero-pill {
      background: #eff6ff !important;
      border: 1.5px solid #93c5fd !important;
      color: #1e40af !important;
    }

    html[data-jp-theme="light"] .grad-violet {
      background: linear-gradient(135deg, #1e3a8a 0%, #1d4ed8 55%, #b45309 100%);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
    }

    html[data-jp-theme="light"] #gbEasyPlaybookBanner {
      background: #ffffff !important;
      border: 1.5px solid #cbd5e1 !important;
      border-top: 4px solid #0b1f3a !important;
      border-left: 4px solid #047857 !important;
      box-shadow: 0 6px 20px rgba(15, 23, 42, 0.06) !important;
    }

    html[data-jp-theme="light"] #gbEasyPlaybookBanner strong {
      color: #0f172a !important;
    }

    html[data-jp-theme="light"] #gbEasyPlaybookBanner > div:last-child > div {
      background: #f8fafc !important;
      border: 1px solid #e2e8f0 !important;
    }

    html[data-jp-theme="light"] .terminal-shell {
      background: #ffffff !important;
      border: 2px solid #cbd5e1 !important;
      box-shadow: 0 12px 32px rgba(15, 23, 42, 0.08) !important;
    }

    html[data-jp-theme="light"] .terminal-topbar {
      background: #0b1f3a !important;
      color: #ffffff !important;
      border-bottom: 2px solid #1e3a8a !important;
    }

    html[data-jp-theme="light"] .terminal-dots {
      color: #e2e8f0 !important;
    }

    html[data-jp-theme="light"] .ticker-btn {
      background: #17325c !important;
      border: 1px solid #3b5998 !important;
      color: #e2e8f0 !important;
    }

    html[data-jp-theme="light"] .ticker-btn.active,
    html[data-jp-theme="light"] .ticker-btn:hover {
      background: #f59e0b !important;
      border-color: #fbbf24 !important;
      color: #0b1f3a !important;
      font-weight: 900 !important;
    }

    html[data-jp-theme="light"] .pane-left {
      background: #ffffff !important;
      border-right: 1px solid #e2e8f0 !important;
    }

    html[data-jp-theme="light"] .pane-right {
      background: #f8fafc !important;
    }

    html[data-jp-theme="light"] .catalyst-headline,
    html[data-jp-theme="light"] h1,
    html[data-jp-theme="light"] h2,
    html[data-jp-theme="light"] h3 {
      color: #0b1f3a !important;
    }

    html[data-jp-theme="light"] .catalyst-summary {
      background: #f1f5f9 !important;
      border-left: 4px solid #1d4ed8 !important;
      color: #1e293b !important;
    }

    html[data-jp-theme="light"] .metric-box,
    html[data-jp-theme="light"] .sizer-card {
      background: #ffffff !important;
      border: 1.5px solid #cbd5e1 !important;
      box-shadow: 0 2px 6px rgba(15, 23, 42, 0.03) !important;
    }

    html[data-jp-theme="light"] .val-violet { color: #1d4ed8 !important; }
    html[data-jp-theme="light"] .val-amber  { color: #b45309 !important; }
    html[data-jp-theme="light"] .val-emerald { color: #047857 !important; }
    html[data-jp-theme="light"] .val-rose   { color: #be123c !important; }
    html[data-jp-theme="light"] .val-sky    { color: #0369a1 !important; }

    html[data-jp-theme="light"] #lblEntry {
      color: #0f172a !important;
    }

    html[data-jp-theme="light"] #gbPlainEnglishActionBox {
      background: #ecfdf5 !important;
      border: 2px solid #10b981 !important;
    }

    html[data-jp-theme="light"] #gbPlainActionTitle {
      color: #065f46 !important;
    }

    html[data-jp-theme="light"] #gbPlainActionSteps {
      color: #0f172a !important;
    }

    html[data-jp-theme="light"] .feature-card,
    html[data-jp-theme="light"] .price-card,
    html[data-jp-theme="light"] .comp-table-wrap,
    html[data-jp-theme="light"] .seo-link-card {
      background: #ffffff !important;
      border: 1.5px solid #cbd5e1 !important;
      color: #0f172a !important;
      box-shadow: 0 4px 14px rgba(15, 23, 42, 0.04) !important;
    }

    html[data-jp-theme="light"] .price-card.featured {
      border: 2.5px solid #1d4ed8 !important;
      box-shadow: 0 12px 30px rgba(29, 78, 216, 0.14) !important;
    }

    html[data-jp-theme="light"] .btn-checkout-secondary,
    html[data-jp-theme="light"] .btn-secondary {
      background: #f1f5f9 !important;
      color: #0b1f3a !important;
      border: 1.5px solid #94a3b8 !important;
    }

    html[data-jp-theme="light"] #gbCrossPromoBanner {
      background: #eff6ff !important;
      border: 1.5px solid #93c5fd !important;
      border-left: 5px solid #1d4ed8 !important;
    }

    html[data-jp-theme="light"] #gbCrossPromoBanner div {
      color: #0f172a !important;
    }

    html[data-jp-theme="light"] #vipCatalystTableBody strong {
      color: #0b1f3a !important;
    }

    /* 日本語タイポグラフィ＆数値整列 */
    body {
      font-feature-settings: "palt" 1;
      letter-spacing: 0.01em;
    }
    .metric-val, .sizer-card strong, table.comp-table td, .jp-num {
      font-variant-numeric: tabular-nums;
    }

    /* ワンタッチ円資金プリセットボタン */
    .jp-preset-row {
      display: flex;
      flex-wrap: wrap;
      gap: 6px;
      margin: 8px 0 14px;
    }
    .jp-preset-btn {
      background: rgba(29, 78, 216, 0.10);
      border: 1px solid var(--border-color);
      color: var(--text-main);
      font-family: var(--font-sans);
      font-size: 0.74rem;
      font-weight: 700;
      padding: 5px 10px;
      border-radius: 6px;
      cursor: pointer;
      transition: all 0.15s ease;
    }
    .jp-preset-btn:hover, .jp-preset-btn.active {
      background: var(--accent-violet);
      border-color: var(--accent-violet);
      color: #ffffff !important;
    }

    /* 株価位置レンジ図解バー */
    .jp-range-box {
      margin-top: 14px;
      padding: 12px 14px;
      background: rgba(15, 23, 42, 0.04);
      border: 1px solid var(--border-color);
      border-radius: 10px;
    }
    .jp-range-track {
      position: relative;
      height: 12px;
      border-radius: 999px;
      background: linear-gradient(90deg, #f43f5e 0%, #f59e0b 35%, #38bdf8 68%, #10b981 100%);
      margin: 10px 0 8px;
    }
    .jp-range-labels {
      display: flex;
      justify-content: space-between;
      font-size: 0.72rem;
      font-family: var(--font-mono);
      font-weight: 700;
      flex-wrap: wrap;
      gap: 4px;
    }

    /* スマホ片手操作用・下部固定クイックナビ */
    .jp-mobile-bottom-nav {
      display: none;
    }
    @media (max-width: 768px) {
      body {
        padding-bottom: 68px;
      }
      .jp-mobile-bottom-nav {
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        position: fixed;
        bottom: 0;
        left: 0;
        right: 0;
        z-index: 999;
        background: #0b1f3a;
        border-top: 2px solid #f59e0b;
        box-shadow: 0 -6px 20px rgba(0,0,0,0.35);
      }
      .jp-mobile-bottom-nav a {
        color: #f8fafc;
        text-decoration: none;
        font-size: 0.7rem;
        font-weight: 800;
        text-align: center;
        padding: 9px 4px;
        border-right: 1px solid rgba(255,255,255,0.12);
      }
      .jp-mobile-bottom-nav a:last-child {
        border-right: none;
        background: #d97706;
        color: #ffffff;
      }
    }
"""

    # Default <html lang="ja" data-jp-theme="light"> so Japanese visitors immediately see the high-trust Securities Light/Navy theme!
    html = html.replace('<html lang="ja">', '<html lang="ja" data-jp-theme="light">')
    if "data-jp-theme" not in html.split("</style>")[0]:
        html = html.replace("</style>", jp_fintech_css + "\n  </style>")

    # 2. Add Theme Toggle button in Header navigation
    if "btnToggleJpTheme" not in html:
        html = html.replace(
            '<a href="#radar" class="mobile-nav-cta">ATR計算機 ↓</a>',
            '<div style="display:flex; align-items:center; gap:8px;">'
            '<button type="button" id="btnToggleJpTheme" onclick="toggleJpTheme()" style="background:#17325c; color:#fde68a; border:1px solid #3b5998; padding:6px 11px; border-radius:7px; font-size:0.75rem; font-weight:800; cursor:pointer;">🌙 ダーク切替</button>'
            '<a href="#radar" class="mobile-nav-cta">ATR計算 ↓</a>'
            '</div>'
        )

    # 3. Add Japanese Trust & Brokerage Compatibility Ribbon + Quick Comparison Matrix right above #gbEasyPlaybookBanner
    jp_trust_and_matrix_html = """
    <!-- 🇯🇵 日本の個人投資家向け「3大安心・証券口座対応バッジ」 -->
    <div style="display:grid; grid-template-columns:repeat(auto-fit, minmax(240px, 1fr)); gap:10px; margin-bottom:18px;">
      <div style="background:var(--bg-card); border:1.5px solid var(--border-color); border-top:3px solid #1d4ed8; border-radius:10px; padding:10px 14px; display:flex; align-items:center; gap:10px;">
        <span style="font-size:1.35rem;">🏦</span>
        <div style="font-size:0.8rem; line-height:1.4;">
          <strong style="display:block; color:var(--text-main);">SBI証券・楽天証券・マネックス対応</strong>
          <span style="color:var(--text-muted);">新NISA成長投資枠・特定口座の逆指値にそのまま使えるドル/円計算</span>
        </div>
      </div>
      <div style="background:var(--bg-card); border:1.5px solid var(--border-color); border-top:3px solid #047857; border-radius:10px; padding:10px 14px; display:flex; align-items:center; gap:10px;">
        <span style="font-size:1.35rem;">📑</span>
        <div style="font-size:0.8rem; line-height:1.4;">
          <strong style="display:block; color:var(--text-main);">米国SEC EDGAR公式開示を3秒で日本語化</strong>
          <span style="color:var(--text-muted);">英語の8-K決算・Form-4役員自社株買い・Gamma壁を図解で要約</span>
        </div>
      </div>
      <div style="background:var(--bg-card); border:1.5px solid var(--border-color); border-top:3px solid #b45309; border-radius:10px; padding:10px 14px; display:flex; align-items:center; gap:10px;">
        <span style="font-size:1.35rem;">🛡️</span>
        <div style="font-size:0.8rem; line-height:1.4;">
          <strong style="display:block; color:var(--text-main);">塩漬け・大損を防ぐ「2.0x ATR損切り」</strong>
          <span style="color:var(--text-muted);">1回の許容損失を口座資金の1.5%以内に自動ロックする機関投資家式</span>
        </div>
      </div>
    </div>

    <!-- 📊 本日の米国株AIシグナル早見表（株探・四季報スタイルの高一覧性テーブル） -->
    <div id="gbQuickMatrixSection" class="comp-table-wrap" style="margin-bottom:20px; padding:16px 18px;">
      <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:8px; margin-bottom:10px;">
        <div style="font-weight:900; font-size:0.96rem;">
          📊 本日の米国株 主要銘柄AIシグナル＆ATR損切りライン早見表 <span style="font-size:0.76rem; font-weight:700; color:var(--accent-amber);">（行をクリックすると下の計算機に自動反映されます）</span>
        </div>
        <span style="font-size:0.74rem; font-family:var(--font-mono); color:var(--text-sub);">※1ドル＝150円基準・リアルタイム連動</span>
      </div>
      <table class="comp-table" id="gbQuickMatrixTable" style="font-size:0.82rem;">
        <thead>
          <tr>
            <th>銘柄コード・日本名</th>
            <th>AI総合判定</th>
            <th>一次情報カタリスト要約</th>
            <th>現在株価</th>
            <th>2.0x ATR損切り</th>
            <th>2.5R 利確目標</th>
            <th>シミュレーター</th>
          </tr>
        </thead>
        <tbody>
          <tr style="cursor:pointer;" onclick="selectCatalyst('NVDA'); document.getElementById('radar').scrollIntoView({behavior:'smooth'});">
            <td><strong>$NVDA エヌビディア</strong></td>
            <td><span class="tape-badge bg-pead">🟢 強気 93.5点</span></td>
            <td>Blackwell増産8-K・Call 3.2倍GEX</td>
            <td class="jp-num">$186.64</td>
            <td class="val-rose jp-num">$170.60</td>
            <td class="val-emerald jp-num"><strong>$226.74</strong></td>
            <td><button type="button" class="ticker-btn active" style="padding:4px 9px; font-size:0.72rem;">計算機に反映 ↓</button></td>
          </tr>
          <tr style="cursor:pointer;" onclick="selectCatalyst('PLTR'); document.getElementById('radar').scrollIntoView({behavior:'smooth'});">
            <td><strong>$PLTR パランティア</strong></td>
            <td><span class="tape-badge bg-pead">🟢 強気 91.0点</span></td>
            <td>国防AI大型契約(8-K)・DP機関買い64%</td>
            <td class="jp-num">$160.38</td>
            <td class="val-rose jp-num">$140.48</td>
            <td class="val-emerald jp-num"><strong>$210.13</strong></td>
            <td><button type="button" class="ticker-btn" style="padding:4px 9px; font-size:0.72rem;">計算機に反映 ↓</button></td>
          </tr>
          <tr style="cursor:pointer;" onclick="selectCatalyst('LLY'); document.getElementById('radar').scrollIntoView({behavior:'smooth'});">
            <td><strong>$LLY イーライリリー</strong></td>
            <td><span class="tape-badge bg-whale">🐋 役員買い 89.8点</span></td>
            <td>CEO/CFOら3名が自腹$4.8M市場内買い</td>
            <td class="jp-num">$1,354.00</td>
            <td class="val-rose jp-num">$1,248.38</td>
            <td class="val-emerald jp-num"><strong>$1,618.05</strong></td>
            <td><button type="button" class="ticker-btn" style="padding:4px 9px; font-size:0.72rem;">計算機に反映 ↓</button></td>
          </tr>
          <tr style="cursor:pointer;" onclick="selectCatalyst('TSLA'); document.getElementById('radar').scrollIntoView({behavior:'smooth'});">
            <td><strong>$TSLA テスラ</strong></td>
            <td><span class="tape-badge bg-gamma">⚡ GEX 89.7点</span></td>
            <td>Call 3.6倍スイープ流入・踏み上げ点火</td>
            <td class="jp-num">$358.22</td>
            <td class="val-rose jp-num">$322.24</td>
            <td class="val-emerald jp-num"><strong>$448.17</strong></td>
            <td><button type="button" class="ticker-btn" style="padding:4px 9px; font-size:0.72rem;">計算機に反映 ↓</button></td>
          </tr>
          <tr style="cursor:pointer;" onclick="selectCatalyst('AVGO'); document.getElementById('radar').scrollIntoView({behavior:'smooth'});">
            <td><strong>$AVGO ブロードコム</strong></td>
            <td><span class="tape-badge bg-pead">🟢 強気 88.4点</span></td>
            <td>カスタムAI半導体(ASIC)受注・DP 59%</td>
            <td class="jp-num">$293.69</td>
            <td class="val-rose jp-num">$263.41</td>
            <td class="val-emerald jp-num"><strong>$369.39</strong></td>
            <td><button type="button" class="ticker-btn" style="padding:4px 9px; font-size:0.72rem;">計算機に反映 ↓</button></td>
          </tr>
          <tr style="cursor:pointer; background:rgba(244,63,94,0.06);" onclick="selectCatalyst('SMCI'); document.getElementById('radar').scrollIntoView({behavior:'smooth'});">
            <td><strong>$SMCI スーパーマイクロ</strong></td>
            <td><span class="tape-badge bg-risk">🔴 禁止 28.5点</span></td>
            <td>10-K会計監査リスク＆機関売り67%検知</td>
            <td class="jp-num">$28.76</td>
            <td class="val-rose jp-num">新規買い禁止</td>
            <td class="val-rose jp-num"><strong>見送り推奨</strong></td>
            <td><button type="button" class="ticker-btn" style="padding:4px 9px; font-size:0.72rem;">警告詳細 ↓</button></td>
          </tr>
        </tbody>
      </table>
    </div>
"""

    if "gbQuickMatrixSection" not in html:
        html = html.replace(
            '<div id="gbEasyPlaybookBanner"',
            jp_trust_and_matrix_html + '\n    <div id="gbEasyPlaybookBanner"'
        )

    # 4. Add 1-Tap Japanese Yen Capital Presets & FX Rate Buttons right below #sliderAccount, plus Visual Price Range Thermometer Bar below #gbPlainEnglishActionBox
    yen_presets_html = """
            <div class="jp-preset-row">
              <span style="font-size:0.72rem; color:var(--text-sub); align-self:center; font-weight:700;">ワンタッチ資金選択:</span>
              <button type="button" class="jp-preset-btn" onclick="setJpAccountPreset(6700)">100万円</button>
              <button type="button" class="jp-preset-btn" onclick="setJpAccountPreset(20000)">300万円</button>
              <button type="button" class="jp-preset-btn" onclick="setJpAccountPreset(33300)">500万円</button>
              <button type="button" class="jp-preset-btn active" onclick="setJpAccountPreset(50000)">750万円 ($5万)</button>
              <button type="button" class="jp-preset-btn" onclick="setJpAccountPreset(66700)">1,000万円</button>
              <button type="button" class="jp-preset-btn" onclick="setJpAccountPreset(80000)">1,200万円 (新NISA枠)</button>
            </div>
            <div class="jp-preset-row" style="margin-top:4px;">
              <span style="font-size:0.72rem; color:var(--text-sub); align-self:center; font-weight:700;">為替レート試算:</span>
              <button type="button" class="jp-preset-btn" onclick="setJpFxRate(145)">145円(円高)</button>
              <button type="button" class="jp-preset-btn active" onclick="setJpFxRate(150)">150円(標準)</button>
              <button type="button" class="jp-preset-btn" onclick="setJpFxRate(155)">155円(円安)</button>
              <button type="button" class="jp-preset-btn" onclick="setJpFxRate(160)">160円</button>
            </div>"""

    if "setJpAccountPreset" not in html:
        html = html.replace(
            '<input type="range" id="sliderAccount" min="5000" max="250000" step="5000" value="50000" oninput="recalcSizer()">',
            '<input type="range" id="sliderAccount" min="5000" max="250000" step="100" value="50000" oninput="recalcSizer()">' + yen_presets_html
        )

    visual_range_bar_html = """
          <!-- 📏 株価位置ビジュアル温度計（損切り ── 現在値 ── Gamma壁 ── 2.5R利確） -->
          <div id="gbVisualRangeBar" class="jp-range-box">
            <div style="font-size:0.76rem; font-weight:800; color:var(--text-main);">
              📏 価格帯ビジュアルマップ（逆指値・現在値・利確目標の位置関係）
            </div>
            <div class="jp-range-track"></div>
            <div class="jp-range-labels">
              <span style="color:var(--accent-rose);">🛑 2.0x ATR損切り: <b id="barStopVal">$170.60</b></span>
              <span style="color:var(--text-main);">📍 現在値: <b id="barEntryVal">$186.64</b></span>
              <span style="color:var(--accent-violet);">⚡ 5日Gamma壁: <b id="barWallVal">$204.52</b></span>
              <span style="color:var(--accent-emerald);">🎯 2.5R利確: <b id="barTargetVal">$226.74</b></span>
            </div>
          </div>"""

    if "gbVisualRangeBar" not in html:
        html = html.replace(
            '<!-- 🟢 AI日本語アクションプラン・適正株数＆損切りライン -->',
            visual_range_bar_html + '\n\n          <!-- 🟢 AI日本語アクションプラン・適正株数＆損切りライン -->'
        )

    # 5. Add Japanese FAQ Section (#jp-faq) & Mobile Sticky Bottom Bar before <footer>
    jp_faq_and_mobile_nav = """
  <!-- ❓ よくあるご質問（日本の個人投資家向けQ&A） -->
  <section id="jp-faq" class="section container" style="padding-top:10px; padding-bottom:60px;">
    <h2 class="section-title">❓ よくあるご質問（新NISA・米国株投資家向けQ&amp;A）</h2>
    <p class="section-subtitle">ご購入前やご利用中によくいただくご質問をまとめました。</p>
    <div style="display:grid; grid-template-columns:repeat(auto-fit, minmax(300px, 1fr)); gap:16px;">
      <div class="feature-card">
        <h3 class="card-title" style="font-size:1.02rem;">Q1. 英語が全く読めなくても米国株の一次情報を理解できますか？</h3>
        <p class="card-desc">はい。米国SECに提出される英語の8-K（重要契約・決算）やForm-4（役員の自社株買い）をAIが3秒で日本語の点数（0〜100点）と3ステップの具体的な行動プランに変換するため、英語力は一切不要です。</p>
      </div>
      <div class="feature-card">
        <h3 class="card-title" style="font-size:1.02rem;">Q2. 楽天証券やSBI証券の注文画面でどう使えばいいですか？</h3>
        <p class="card-desc">当サイトの計算機に表示される「推奨エントリー株数」を購入し、証券アプリの逆指値（ストップロス）注文に「2.0x ATR損切りライン（$○○）」をそのまま入力するだけで、機関投資家と同じリスク管理が完了します。</p>
      </div>
      <div class="feature-card">
        <h3 class="card-title" style="font-size:1.02rem;">Q3. 永久ライセンス買い切り（$199 / 約30,000円）は本当に追加費用0円ですか？</h3>
        <p class="card-desc">はい。1回のお支払いのみで、毎月のサブスク課金は一切発生しません。さらに姉妹サイト TruthOfMarket.com（半導体恐怖強欲指数＆72銘柄PW-RSI）の生涯VIP権も無料で付属します。</p>
      </div>
      <div class="feature-card">
        <h3 class="card-title" style="font-size:1.02rem;">Q4. JCBカードやApple Payでの決済、月額プランの1クリック解約は可能ですか？</h3>
        <p class="card-desc">はい。公式決済基盤 Lemon Squeezy / Stripe により、JCB・Visa・Mastercard・Apple Pay・Google Pay・PayPalすべてに対応しており、月額プランもマイページからいつでも1クリックで解約可能です。</p>
      </div>
    </div>
  </section>

  <!-- 📱 スマホ片手操作用・下部固定クイックバー -->
  <nav class="jp-mobile-bottom-nav" aria-label="モバイルクイックメニュー">
    <a href="#gbQuickMatrixSection">📊 銘柄早見表</a>
    <a href="#radar">🧮 ATR株数計算</a>
    <a href="#vip-vault">👑 VIPデータ庫</a>
    <a href="#pricing">💎 Pro購入</a>
  </nav>
"""

    if 'id="jp-faq"' not in html:
        html = html.replace('<!-- フッター -->', jp_faq_and_mobile_nav + '\n  <!-- フッター -->')

    # 6. Update JS to support dynamic USD_JPY_RATE (`let USD_JPY_RATE = 150.0;`), `setJpAccountPreset`, `setJpFxRate`, `toggleJpTheme`, and updating `#barStopVal` / `#barEntryVal` / `#barWallVal` / `#barTargetVal`
    html = html.replace("const USD_JPY_RATE = 150.0;", "let USD_JPY_RATE = 150.0;")

    # 6-B. Inject Japanese Tax Regime Switcher (新NISA vs 特定口座 20.315%) & Real-time Tax/Fee/FX Net Profit Box
    tax_mode_buttons_html = """
            <div class="jp-preset-row" style="margin-top:4px;">
              <span style="font-size:0.72rem; color:var(--text-sub); align-self:center; font-weight:700;">日本の税制・口座区分:</span>
              <button type="button" id="btnTaxNisa" class="jp-preset-btn active" onclick="setJpTaxMode('nisa')">🌱 新NISA (非課税0%・買付手数料0円)</button>
              <button type="button" id="btnTaxTokutei" class="jp-preset-btn" onclick="setJpTaxMode('tokutei')">🏦 特定口座 (源泉20.315%・損益通算可)</button>
            </div>"""

    if 'id="btnTaxNisa"' not in html:
        html = html.replace(
            '<button type="button" class="jp-preset-btn" onclick="setJpFxRate(160)">160円</button>\n            </div>',
            '<button type="button" class="jp-preset-btn" onclick="setJpFxRate(160)">160円</button>\n            </div>' + tax_mode_buttons_html
        )

    jp_tax_fx_box_html = """
          <!-- 🇯🇵 日本国内の米国株税制（新NISA 0% vs 特定口座 20.315%）・売買手数料（上限$22）・為替変動（円高/円安）手取り純利益シミュレーター -->
          <div id="gbJpTaxAndFxBox" style="margin-top:14px; background:var(--bg-card); border:1.5px solid var(--border-color); border-left:5px solid #1d4ed8; border-radius:12px; padding:14px 16px; font-size:0.8rem; line-height:1.6;">
            <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:6px; margin-bottom:8px;">
              <strong style="color:var(--text-main); font-size:0.84rem;">
                🇯🇵 日本の米国株 税制・売買手数料・為替変動（円高/円安）手取り純利益シミュレーション
              </strong>
              <span id="badgeJpTaxMode" class="tape-badge bg-pead" style="font-size:0.7rem;">🌱 新NISA（成長投資枠：非課税 0%）適用中</span>
            </div>
            <div style="display:grid; grid-template-columns:repeat(auto-fit, minmax(210px, 1fr)); gap:10px; margin-bottom:10px;">
              <div style="background:rgba(16,185,129,0.06); border:1px solid rgba(16,185,129,0.28); border-radius:8px; padding:9px 11px;">
                <span style="display:block; font-size:0.71rem; color:var(--text-muted); font-weight:700;">🎯 2.5R利確時の「税・手数料引後 手取り純利益」</span>
                <strong id="valNetProfitJpy" class="val-emerald jp-num" style="font-size:0.95rem;">+約27.4万円 (手取り +$1,829)</strong>
                <span id="valTaxSavedNote" style="display:block; font-size:0.71rem; color:var(--accent-emerald); margin-top:2px;">✨ 新NISA非課税メリット: +約5.6万円 節税！</span>
              </div>
              <div style="background:rgba(29,78,216,0.05); border:1px solid rgba(29,78,216,0.22); border-radius:8px; padding:9px 11px;">
                <span style="display:block; font-size:0.71rem; color:var(--text-muted); font-weight:700;">🏦 証券手数料(0.495%上限$22)＋為替スプレッド(25銭)</span>
                <strong id="valBrokerFeeJpy" class="jp-num" style="font-size:0.9rem; color:var(--text-main);">往復コスト 約¥4,596 ($30.64)</strong>
                <span style="display:block; font-size:0.71rem; color:var(--text-sub); margin-top:2px;">SBI・楽天・マネックス米国株標準コスト反映</span>
              </div>
            </div>
            <div id="valFxSensitivity" style="font-size:0.76rem; color:var(--text-muted); margin-bottom:6px;">
              💱 <b>為替変動シミュレーション（円換算課税対応）:</b> 利確時に<b>5円円安(155円)</b>なら手取り <b>+約28.3万円</b> ／ <b>5円円高(145円)</b>なら手取り <b>+約26.5万円</b>
            </div>
            <div id="valLossTaxNote" style="font-size:0.75rem; color:var(--text-sub); background:rgba(245,158,11,0.08); border:1px solid rgba(245,158,11,0.28); border-radius:7px; padding:7px 10px;">
              ⚠️ <b>新NISAの重要注意点（損益通算不可）:</b> 新NISA口座で発生した損失は特定口座の利益と<b>損益通算（相殺）できません</b>。含み損を塩漬けにすると非課税枠が死に金になるため、<b>2.0x ATR損切りラインでの機械的撤退</b>が新NISA資産防衛の鉄則です。
            </div>
          </div>"""

    if 'id="gbJpTaxAndFxBox"' not in html:
        html = html.replace(
            '<!-- 🟢 AI日本語アクションプラン・適正株数＆損切りライン -->',
            jp_tax_fx_box_html + '\n\n          <!-- 🟢 AI日本語アクションプラン・適正株数＆損切りライン -->'
        )

    helper_js = """
    let JP_TAX_MODE = 'nisa'; // 'nisa' (0% 非課税・買付手数料0円) or 'tokutei' (20.315% 源泉徴収・損益通算可)

    function setJpTaxMode(mode) {
      JP_TAX_MODE = mode === 'tokutei' ? 'tokutei' : 'nisa';
      const bNisa = document.getElementById('btnTaxNisa');
      const bTok = document.getElementById('btnTaxTokutei');
      if (bNisa) bNisa.classList.toggle('active', JP_TAX_MODE === 'nisa');
      if (bTok) bTok.classList.toggle('active', JP_TAX_MODE === 'tokutei');
      recalcSizer();
    }

    function setJpAccountPreset(usdVal) {
      const s = document.getElementById('sliderAccount');
      if (s) {
        s.value = usdVal;
        recalcSizer();
      }
    }

    function setJpFxRate(rate) {
      USD_JPY_RATE = Number(rate) || 150.0;
      const fxEl = document.getElementById('lblFxRate');
      if (fxEl) fxEl.innerText = String(USD_JPY_RATE);
      recalcSizer();
    }

    function toggleJpTheme() {
      const root = document.documentElement;
      const cur = root.getAttribute('data-jp-theme') || 'light';
      const next = cur === 'light' ? 'dark' : 'light';
      root.setAttribute('data-jp-theme', next);
      const btn = document.getElementById('btnToggleJpTheme');
      if (btn) {
        btn.innerText = next === 'light' ? '🌙 ダーク切替' : '🌞 証券ライト切替';
      }
    }
"""

    if "function setJpAccountPreset" not in html:
        html = html.replace("function formatJpyMan(usdVal)", helper_js + "\n    function formatJpyMan(usdVal)")
    elif "function setJpTaxMode" not in html:
        html = html.replace(
            "function setJpAccountPreset(usdVal)",
            "let JP_TAX_MODE = 'nisa';\n    function setJpTaxMode(mode) {\n      JP_TAX_MODE = mode === 'tokutei' ? 'tokutei' : 'nisa';\n      const bNisa = document.getElementById('btnTaxNisa');\n      const bTok = document.getElementById('btnTaxTokutei');\n      if (bNisa) bNisa.classList.toggle('active', JP_TAX_MODE === 'nisa');\n      if (bTok) bTok.classList.toggle('active', JP_TAX_MODE === 'tokutei');\n      recalcSizer();\n    }\n    function setJpAccountPreset(usdVal)"
        )

    # Update visual range bar values and Japanese Tax/Fee/FX simulator inside recalcSizer()
    bar_update_js = """
      const bStop = document.getElementById('barStopVal');
      const bEntry = document.getElementById('barEntryVal');
      const bWall = document.getElementById('barWallVal');
      const bTarget = document.getElementById('barTargetVal');
      if (bStop) bStop.innerText = '$' + stopPrice.toFixed(2);
      if (bEntry) bEntry.innerText = '$' + entry.toFixed(2);
      if (bWall) bWall.innerText = '$' + upperWall.toFixed(2);
      if (bTarget) bTarget.innerText = '$' + target25R.toFixed(2);

      // 🇯🇵 日本国内の米国株税制（新NISA 0% vs 特定口座 20.315%）・売買手数料（0.495%上限$22）・為替スプレッド（25銭）計算
      const buyCommUsd = (typeof JP_TAX_MODE !== 'undefined' && JP_TAX_MODE === 'nisa') ? 0 : Math.min(22.0, notional * 0.00495);
      const sellNotional = shares * target25R;
      const sellCommUsd = Math.min(22.0, sellNotional * 0.00495);
      const fxSpreadJpy = (notional + sellNotional) * 0.25; // 往復為替スプレッド（片道25銭基準）
      const totalFeeUsd = buyCommUsd + sellCommUsd + (fxSpreadJpy / USD_JPY_RATE);
      const totalFeeJpy = Math.round(totalFeeUsd * USD_JPY_RATE);

      const grossProfitUsd = Math.max(0, gainDollars - totalFeeUsd);
      const grossProfitJpy = grossProfitUsd * USD_JPY_RATE;
      const jpTaxRate = 0.20315; // 所得税15.315% + 住民税5%
      const taxSavedJpy = grossProfitJpy * jpTaxRate;
      const isTokutei = (typeof JP_TAX_MODE !== 'undefined' && JP_TAX_MODE === 'tokutei');
      const netProfitJpy = isTokutei ? (grossProfitJpy * (1 - jpTaxRate)) : grossProfitJpy;
      const netProfitUsd = netProfitJpy / USD_JPY_RATE;

      const elNetJpy = document.getElementById('valNetProfitJpy');
      const elTaxNote = document.getElementById('valTaxSavedNote');
      const elFeeJpy = document.getElementById('valBrokerFeeJpy');
      const elFxSens = document.getElementById('valFxSensitivity');
      const elLossNote = document.getElementById('valLossTaxNote');
      const elTaxBadge = document.getElementById('badgeJpTaxMode');

      if (elTaxBadge) {
        elTaxBadge.className = isTokutei ? 'tape-badge bg-whale' : 'tape-badge bg-pead';
        elTaxBadge.innerText = isTokutei ? '🏦 特定口座（源泉徴収 20.315%・損益通算可）適用中' : '🌱 新NISA（成長投資枠：非課税 0%）適用中';
      }
      if (elNetJpy) {
        elNetJpy.innerText = '+約' + (netProfitJpy / 10000).toFixed(1) + '万円 (手取り +$' + Math.round(netProfitUsd).toLocaleString() + ')';
      }
      if (elTaxNote) {
        elTaxNote.innerText = isTokutei
          ? ('🏦 譲渡益税(20.315%) 源泉徴収額: -約' + (taxSavedJpy / 10000).toFixed(1) + '万円（確定申告不要）')
          : ('✨ 新NISA非課税メリット: 特定口座より +約' + (taxSavedJpy / 10000).toFixed(1) + '万円 お得！');
      }
      if (elFeeJpy) {
        elFeeJpy.innerText = '往復コスト 約¥' + totalFeeJpy.toLocaleString() + ' ($' + totalFeeUsd.toFixed(2) + ')';
      }
      if (elFxSens) {
        const rateWeak = USD_JPY_RATE + 5;
        const rateStrong = Math.max(100, USD_JPY_RATE - 5);
        const netWeakMan = ((grossProfitUsd * rateWeak) * (isTokutei ? (1 - jpTaxRate) : 1) / 10000).toFixed(1);
        const netStrongMan = ((grossProfitUsd * rateStrong) * (isTokutei ? (1 - jpTaxRate) : 1) / 10000).toFixed(1);
        elFxSens.innerHTML = '💱 <b>為替変動シミュレーション（円換算課税対応）:</b> 利確時に<b>5円円安(' + rateWeak + '円)</b>なら手取り <b>+約' + netWeakMan + '万円</b> ／ <b>5円円高(' + rateStrong + '円)</b>なら手取り <b>+約' + netStrongMan + '万円</b>';
      }
      if (elLossNote) {
        const lossRefundMan = ((actualRiskUsd * USD_JPY_RATE * jpTaxRate) / 10000).toFixed(1);
        elLossNote.innerHTML = isTokutei
          ? ('💡 <b>特定口座の損益通算メリット:</b> 万が一 2.0x ATR（-$' + actualRiskUsd.toLocaleString() + '）で損切りとなっても、他銘柄の利益や配当と<b>損益通算（＋3年間繰越控除）</b>することで<b>約' + lossRefundMan + '万円（20.315%）の税金還付効果</b>があり、実質ダメージを軽減できます。')
          : ('⚠️ <b>新NISAの重要注意点（損益通算不可）:</b> 新NISA口座の損失は特定口座と<b>損益通算できません</b>。含み損を放置（塩漬け）すると貴重な非課税枠が死に金になるため、<b>2.0x ATR損切りライン（$' + stopPrice.toFixed(2) + '）での機械的撤退</b>が新NISA枠を守る鉄則です。');
      }
"""
    if "barStopVal" not in html.split("function recalcSizer()")[1]:
        html = html.replace(
            "document.getElementById('outTarget25R').innerText =",
            bar_update_js + "\n      document.getElementById('outTarget25R').innerText ="
        )
    # Clean up any accidental duplicate const bStop block if present
    dup_block = """      const bStop = document.getElementById('barStopVal');
      const bEntry = document.getElementById('barEntryVal');
      const bWall = document.getElementById('barWallVal');
      const bTarget = document.getElementById('barTargetVal');
      if (bStop) bStop.innerText = '$' + stopPrice.toFixed(2);
      if (bEntry) bEntry.innerText = '$' + entry.toFixed(2);
      if (bWall) bWall.innerText = '$' + upperWall.toFixed(2);
      const bStop = document.getElementById('barStopVal');"""
    html = html.replace(dup_block, "      const bStop = document.getElementById('barStopVal');")

    with open(INDEX_PATH, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"[OK] Upgraded {INDEX_PATH} to Japanese Securities (SBI/Kabutan/Buffett-Code) High-Trust UI/UX")


def upgrade_seo_pages():
    if not os.path.exists(JP_DIR):
        return
    light_override_css = """
    /* 日本証券ライト・高信頼テーマ (標準) */
    body { background: #f4f6fa !important; color: #0f172a !important; font-feature-settings: "palt" 1; }
    header { background: #0b1f3a !important; border-bottom: 2px solid #1e3a8a !important; }
    .article-box { background: #ffffff !important; border: 1.5px solid #cbd5e1 !important; box-shadow: 0 8px 24px rgba(15,23,42,0.06) !important; }
    h1 { color: #0b1f3a !important; }
    h2 { color: #1e3a8a !important; border-left: 5px solid #1d4ed8 !important; background: #eff6ff; padding: 8px 12px !important; border-radius: 0 8px 8px 0; }
    h3 { color: #b45309 !important; }
    p, li { color: #1e293b !important; }
    .kpi-card { background: #f8fafc !important; border: 1.5px solid #cbd5e1 !important; }
    .kpi-label { color: #475569 !important; font-weight: 700; }
    .kpi-val { color: #0b1f3a !important; }
    .widget-box { background: #f8fafc !important; border: 2px solid #1d4ed8 !important; }
    .widget-box h3 { color: #0b1f3a !important; }
    a { color: #1d4ed8; }
"""
    count = 0
    for fn in os.listdir(JP_DIR):
        if not fn.endswith(".html"):
            continue
        p = os.path.join(JP_DIR, fn)
        c = open(p, "r", encoding="utf-8").read()
        if "日本証券ライト・高信頼テーマ" not in c and "</style>" in c:
            c = c.replace("</style>", light_override_css + "\n  </style>")
            open(p, "w", encoding="utf-8").write(c)
            count += 1
    print(f"[OK] Upgraded {count} Japanese SEO pages in {JP_DIR} to Japanese Securities Light/Navy UI/UX")


if __name__ == "__main__":
    upgrade_main_index()
    upgrade_seo_pages()
