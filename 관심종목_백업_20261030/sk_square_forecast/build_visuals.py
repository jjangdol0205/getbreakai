#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
build_visuals.py - Generates 100% Zero-CDN Offline Standalone Charts and Executive Visual Dashboard
for SK Square (402340) & SK Hynix (000660) Forecast Engine.

Outputs:
- charts/nav_discount_chart.html
- charts/beta_spread_chart.html
- charts/historical_analogs_chart.html
- charts/scenario_fan_chart.html
- dashboard.html

Zero-CDN Guarantee:
- Absolutely NO external libraries, stylesheets, or fonts.
- Pure inline CSS, vanilla JavaScript, and responsive SVG/Canvas.
"""

import os
import sys
import json

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8")

WORKSPACE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(WORKSPACE_DIR, "data")
CHARTS_DIR = os.path.join(WORKSPACE_DIR, "charts")

os.makedirs(CHARTS_DIR, exist_ok=True)

# ---------------------------------------------------------------------------
# 1. Load Data Files
# ---------------------------------------------------------------------------
print("Loading data files from:", DATA_DIR)
with open(os.path.join(DATA_DIR, "nav_discount_series.json"), "r", encoding="utf-8") as f:
    nav_data = json.load(f)

with open(os.path.join(DATA_DIR, "technical_indicators.json"), "r", encoding="utf-8") as f:
    tech_data = json.load(f)

with open(os.path.join(DATA_DIR, "supply_demand_short.json"), "r", encoding="utf-8") as f:
    sup_data = json.load(f)

with open(os.path.join(DATA_DIR, "historical_analogs.json"), "r", encoding="utf-8") as f:
    analogs_data = json.load(f)

with open(os.path.join(DATA_DIR, "scenario_matrix.json"), "r", encoding="utf-8") as f:
    scenario_data = json.load(f)

# Combine 260 trading days data
combined_series = []
for i in range(len(nav_data["series"])):
    n = nav_data["series"][i]
    t = tech_data["series"][i]
    s = sup_data["series"][i]
    combined_series.append({
        "d": n["date"],
        "sq_close": n["square_price"],
        "sq_unit": n["square_unit_price"],
        "hy_close": n["hynix_price"],
        "total_nav": n["total_nav"],
        "nav_per_share": n["nav_per_share"],
        "disc_pct": n["discount_rate_pct"],
        "accreted_nav": n["accreted_nav_per_share"],
        "sq_sma20": t["square_sma_20"],
        "sq_sma60": t["square_sma_60"],
        "sq_sma120": t["square_sma_120"],
        "sq_sma200": t["square_sma_200"],
        "sq_dist_200ma": t["square_dist_200ma_pct"],
        "sq_rsi14": t["square_rsi_14"],
        "sq_macd": t["square_macd"],
        "sq_macd_signal": t["square_macd_signal"],
        "sq_macd_hist": t["square_macd_hist"],
        "sq_bb_upper": t["square_bb_upper"],
        "sq_bb_mid": t["square_bb_mid"],
        "sq_bb_lower": t["square_bb_lower"],
        "poc": t["poc_price"],
        "vah": t["vah_price"],
        "val": t["val_price"],
        "fib_23_6": t["fib_23_6"],
        "fib_38_2": t["fib_38_2"],
        "fib_50_0": t["fib_50_0"],
        "fib_61_8": t["fib_61_8"],
        "fib_78_6": t["fib_78_6"],
        "vkospi": t["vkospi"],
        "foreign_net": s["square_foreign_net_shares"],
        "inst_net": s["square_inst_net_shares"],
        "retail_net": s["square_retail_net_shares"],
        "other_corp_net": s["square_other_corp_net_shares"],
        "sq_cum_foreign_20d": s["square_cum_foreign_20d"],
        "sq_cum_inst_20d": s["square_cum_inst_20d"],
        "sq_cum_retail_20d": s["square_cum_retail_20d"],
        "sq_foreign_hold_pct": s["square_foreign_hold_pct"],
        "hy_foreign_hold_pct": s["hynix_foreign_hold_pct"],
        "hy_foreign_floor_minus_1sigma": s["hynix_foreign_floor_minus_1sigma"],
        "basis": s["market_basis"],
        "basis_regime": s["basis_regime"],
        "foreign_futures_cum_3d": s["foreign_futures_cum_3d_contracts"],
        "rolling_beta_20d": s["square_hynix_rolling_beta_20d"],
        "rolling_beta_60d": s["square_hynix_rolling_beta_60d"],
        "rolling_beta_120d": s["square_hynix_rolling_beta_120d"],
        "downside_beta": s["square_hynix_downside_beta"],
        "upside_beta": s["square_hynix_upside_beta"],
        "asymmetry_ratio": s["square_asymmetry_ratio"],
        "cum_return_spread_pct": s["cum_return_spread_pct"],
        "sq_short_volume": s["square_short_volume"],
        "sq_short_ratio_pct": s["square_short_ratio_pct"],
        "sq_loan_balance_shares": s["square_loan_balance_shares"],
        "hy_loan_balance_shares": s["hynix_loan_balance_shares"],
        "hy_days_to_cover": s["hynix_days_to_cover"],
        "hy_short_squeeze_score": s["hynix_short_squeeze_score"],
        "margin_floor_1": s["square_margin_call_floor_1"],
        "margin_floor_2": s["square_margin_call_floor_2"],
        "margin_overhang": s["square_margin_liquidation_overhang_shares"]
    })

combined_json = json.dumps(combined_series, ensure_ascii=False)
analogs_json = json.dumps(analogs_data["cases"], ensure_ascii=False)
scenario_json = json.dumps(scenario_data, ensure_ascii=False)

# Common Design Tokens & CSS
COMMON_CSS = """
:root {
  --bg-main: #0b111e;
  --bg-card: #131c2e;
  --bg-card-hover: #19253d;
  --bg-input: #1a253c;
  --text-primary: #f8fafc;
  --text-secondary: #94a3b8;
  --text-muted: #64748b;
  --border: #233554;
  --border-focus: #38bdf8;
  --primary: #38bdf8;
  --primary-glow: rgba(56, 189, 248, 0.2);
  --success: #10b981;
  --success-glow: rgba(16, 185, 129, 0.2);
  --danger: #f43f5e;
  --danger-glow: rgba(244, 63, 94, 0.2);
  --warning: #f59e0b;
  --warning-glow: rgba(245, 158, 11, 0.2);
  --purple: #a855f7;
  --indigo: #6366f1;
  --font-sans: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Noto Sans KR", Helvetica, Arial, sans-serif;
  --font-mono: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;
  --radius-sm: 6px;
  --radius-md: 10px;
  --radius-lg: 16px;
  --shadow: 0 4px 24px -2px rgba(0, 0, 0, 0.5);
  --transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
}

[data-theme="light"] {
  --bg-main: #f1f5f9;
  --bg-card: #ffffff;
  --bg-card-hover: #f8fafc;
  --bg-input: #e2e8f0;
  --text-primary: #0f172a;
  --text-secondary: #475569;
  --text-muted: #94a3b8;
  --border: #cbd5e1;
  --border-focus: #0284c7;
  --primary: #0284c7;
  --primary-glow: rgba(2, 132, 199, 0.15);
  --success: #059669;
  --danger: #e11d48;
  --warning: #d97706;
  --purple: #9333ea;
  --indigo: #4f46e5;
  --shadow: 0 4px 18px -1px rgba(0, 0, 0, 0.08);
}

* { box-sizing: border-box; margin: 0; padding: 0; }
body {
  background-color: var(--bg-main);
  color: var(--text-primary);
  font-family: var(--font-sans);
  line-height: 1.5;
  padding: 24px;
}
.container { max-width: 1440px; margin: 0 auto; }
header.chart-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap;
  gap: 16px;
  margin-bottom: 24px;
  padding-bottom: 20px;
  border-bottom: 1px solid var(--border);
}
.chart-title h1 {
  font-size: 24px;
  font-weight: 700;
  letter-spacing: -0.02em;
  display: flex;
  align-items: center;
  gap: 10px;
}
.chart-title p {
  color: var(--text-secondary);
  font-size: 14px;
  margin-top: 4px;
}
.chart-actions {
  display: flex;
  align-items: center;
  gap: 12px;
}
.badge {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 4px 10px;
  border-radius: var(--radius-sm);
  font-size: 12px;
  font-weight: 600;
  background: var(--bg-card);
  border: 1px solid var(--border);
}
.badge.badge-primary { background: var(--primary-glow); border-color: var(--primary); color: var(--primary); }
.badge.badge-success { background: var(--success-glow); border-color: var(--success); color: var(--success); }
.badge.badge-danger { background: var(--danger-glow); border-color: var(--danger); color: var(--danger); }
.badge.badge-warning { background: var(--warning-glow); border-color: var(--warning); color: var(--warning); }

.btn {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 8px 16px;
  border-radius: var(--radius-sm);
  font-size: 13px;
  font-weight: 600;
  cursor: pointer;
  border: 1px solid var(--border);
  background: var(--bg-card);
  color: var(--text-primary);
  transition: var(--transition);
  text-decoration: none;
}
.btn:hover {
  background: var(--bg-card-hover);
  border-color: var(--border-focus);
}
.btn-primary {
  background: var(--primary);
  color: #000;
  border-color: var(--primary);
}
.btn-primary:hover {
  filter: brightness(1.1);
}

.kpi-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(210px, 1fr));
  gap: 16px;
  margin-bottom: 24px;
}
.kpi-card {
  background: var(--bg-card);
  border: 1px solid var(--border);
  border-radius: var(--radius-md);
  padding: 16px 20px;
  box-shadow: var(--shadow);
  transition: var(--transition);
}
.kpi-card:hover {
  border-color: var(--border-focus);
  transform: translateY(-2px);
}
.kpi-label {
  font-size: 12px;
  color: var(--text-secondary);
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  margin-bottom: 6px;
  display: flex;
  justify-content: space-between;
}
.kpi-value {
  font-size: 24px;
  font-weight: 700;
  font-family: var(--font-mono);
  color: var(--text-primary);
}
.kpi-sub {
  font-size: 12px;
  color: var(--text-secondary);
  margin-top: 6px;
  display: flex;
  align-items: center;
  gap: 6px;
}

.chart-panel {
  background: var(--bg-card);
  border: 1px solid var(--border);
  border-radius: var(--radius-lg);
  padding: 24px;
  box-shadow: var(--shadow);
  margin-bottom: 24px;
  position: relative;
}
.chart-panel-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap;
  gap: 12px;
  margin-bottom: 20px;
}
.chart-panel-title {
  font-size: 16px;
  font-weight: 700;
  display: flex;
  align-items: center;
  gap: 8px;
}
.chart-controls {
  display: flex;
  align-items: center;
  gap: 8px;
}
.range-btn-group {
  display: inline-flex;
  background: var(--bg-input);
  border-radius: var(--radius-sm);
  padding: 2px;
  border: 1px solid var(--border);
}
.range-btn {
  padding: 4px 12px;
  font-size: 12px;
  font-weight: 600;
  border: none;
  background: transparent;
  color: var(--text-secondary);
  border-radius: var(--radius-sm);
  cursor: pointer;
  transition: var(--transition);
}
.range-btn.active, .range-btn:hover {
  background: var(--bg-card);
  color: var(--primary);
}

.canvas-container {
  position: relative;
  width: 100%;
  height: 480px;
}
canvas {
  width: 100%;
  height: 100%;
  display: block;
}
.tooltip {
  position: absolute;
  pointer-events: none;
  background: rgba(15, 23, 42, 0.95);
  backdrop-filter: blur(8px);
  border: 1px solid var(--border-focus);
  color: #fff;
  border-radius: var(--radius-md);
  padding: 12px 16px;
  font-size: 12px;
  box-shadow: var(--shadow);
  z-index: 100;
  display: none;
  min-width: 220px;
  line-height: 1.6;
}
.tooltip-header {
  font-weight: 700;
  color: var(--primary);
  border-bottom: 1px solid rgba(255,255,255,0.1);
  padding-bottom: 4px;
  margin-bottom: 6px;
}
.tooltip-row {
  display: flex;
  justify-content: space-between;
  gap: 16px;
}
.tooltip-row span:first-child { color: var(--text-secondary); }
.tooltip-row span:last-child { font-weight: 600; font-family: var(--font-mono); }

.simulator-card {
  background: var(--bg-card);
  border: 1px solid var(--border);
  border-radius: var(--radius-lg);
  padding: 24px;
  margin-bottom: 24px;
  box-shadow: var(--shadow);
}
.sim-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 24px;
  margin-top: 20px;
}
.sim-control-group {
  display: flex;
  flex-direction: column;
  gap: 8px;
}
.sim-control-header {
  display: flex;
  justify-content: space-between;
  font-size: 13px;
  font-weight: 600;
}
.sim-slider {
  width: 100%;
  accent-color: var(--primary);
  cursor: pointer;
  height: 6px;
  background: var(--bg-input);
  border-radius: 3px;
}
.sim-result-box {
  background: var(--bg-input);
  border: 1px solid var(--border);
  border-radius: var(--radius-md);
  padding: 20px;
  display: flex;
  flex-direction: column;
  justify-content: center;
}
.sim-result-value {
  font-size: 32px;
  font-weight: 800;
  font-family: var(--font-mono);
  color: var(--primary);
}

.table-wrapper {
  overflow-x: auto;
  margin-top: 16px;
}
table.custom-table {
  width: 100%;
  border-collapse: collapse;
  font-size: 13px;
  text-align: left;
}
table.custom-table th {
  background: var(--bg-input);
  color: var(--text-secondary);
  font-weight: 600;
  padding: 12px 16px;
  border-bottom: 2px solid var(--border);
  white-space: nowrap;
}
table.custom-table td {
  padding: 12px 16px;
  border-bottom: 1px solid var(--border);
  white-space: nowrap;
  font-family: var(--font-mono);
}
table.custom-table tr:hover td {
  background: var(--bg-card-hover);
}
"""

COMMON_JS_HEADER = """
function toggleTheme() {
  const current = document.documentElement.getAttribute('data-theme') || 'dark';
  const target = current === 'dark' ? 'light' : 'dark';
  document.documentElement.setAttribute('data-theme', target);
  localStorage.setItem('theme', target);
}
const savedTheme = localStorage.getItem('theme');
if (savedTheme) {
  document.documentElement.setAttribute('data-theme', savedTheme);
}
"""

print("Writing standalone charts...")

# ---------------------------------------------------------------------------
# 2. Build charts/nav_discount_chart.html
# ---------------------------------------------------------------------------
nav_html = f"""<!DOCTYPE html>
<html lang="ko" data-theme="dark">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>SK Square (402340) NAV & Valuation Discount Channels | Standalone Interactive Chart</title>
  <style>
{COMMON_CSS}
  </style>
</head>
<body>
  <div class="container">
    <header class="chart-header">
      <div class="chart-title">
        <h1>🏛️ SK Square NAV & Valuation Discount Channels</h1>
        <p>SK하이닉스 지분가치, 비상장 자산, 순현금 연동 주당 NAV 대비 할인율 시계열 분석 (260 거래일)</p>
      </div>
      <div class="chart-actions">
        <span class="badge badge-primary">Zero-CDN Offline</span>
        <button class="btn" onclick="toggleTheme()">🌓 테마 전환</button>
        <a href="../dashboard.html" class="btn">📊 종합 대시보드</a>
      </div>
    </header>

    <div class="kpi-grid">
      <div class="kpi-card">
        <div class="kpi-label">SK스퀘어 현재가 (주당)</div>
        <div class="kpi-value" id="kpi-sq-price">85,700 원</div>
        <div class="kpi-sub"><span class="badge badge-warning">단위환산 85.7만 원</span> 고점 대비 -42.5%</div>
      </div>
      <div class="kpi-card">
        <div class="kpi-label">주당 순자산가치 (NAV)</div>
        <div class="kpi-value" id="kpi-nav-price">238,160 원</div>
        <div class="kpi-sub"><span class="badge badge-primary">총 NAV 32.08조 원</span> 소각후 244,958원</div>
      </div>
      <div class="kpi-card">
        <div class="kpi-label">NAV 할인율</div>
        <div class="kpi-value" id="kpi-discount-rate" style="color: var(--danger);">64.02%</div>
        <div class="kpi-sub"><span class="badge badge-danger">역사적 극단 저평가</span> 역대 평균 52.0%</div>
      </div>
      <div class="kpi-card">
        <div class="kpi-label">자사주 소각 액크리션</div>
        <div class="kpi-value" style="color: var(--success);">+3.42%</div>
        <div class="kpi-sub"><span class="badge badge-success">지분율 20.07% → 20.76%</span> 2,407만 주 소각</div>
      </div>
      <div class="kpi-card">
        <div class="kpi-label">비상장 자산 + 순현금</div>
        <div class="kpi-value">5.30조 원</div>
        <div class="kpi-sub"><span class="badge badge-primary">솔리다임 4.5조</span> 순현금 0.8조 원</div>
      </div>
    </div>

    <!-- Main Chart Panel -->
    <div class="chart-panel">
      <div class="chart-panel-header">
        <div class="chart-panel-title">
          <span>📈 SK스퀘어 주가 vs 주당 NAV 및 할인율 채널</span>
          <span class="badge badge-primary" id="hover-date-badge">2026-10-13 최신</span>
        </div>
        <div class="chart-controls">
          <div class="range-btn-group">
            <button class="range-btn" onclick="setRange(22)">1M</button>
            <button class="range-btn" onclick="setRange(65)">3M</button>
            <button class="range-btn" onclick="setRange(130)">6M</button>
            <button class="range-btn active" onclick="setRange(260)">전체 (1Y)</button>
          </div>
        </div>
      </div>

      <!-- Price vs NAV Canvas -->
      <div style="font-size: 13px; font-weight: 600; color: var(--text-secondary); margin-bottom: 8px;">
        [상단] 주가 및 주당 NAV 채널 (KRW)
      </div>
      <div class="canvas-container" style="height: 320px;" id="canvas-box-1">
        <canvas id="chart-canvas-1"></canvas>
      </div>

      <!-- Discount Rate Canvas -->
      <div style="font-size: 13px; font-weight: 600; color: var(--text-secondary); margin: 20px 0 8px 0;">
        [하단] NAV 할인율 밴드 (%) — 50%/55%/60%/65% 벤치마크
      </div>
      <div class="canvas-container" style="height: 180px;" id="canvas-box-2">
        <canvas id="chart-canvas-2"></canvas>
      </div>

      <div class="tooltip" id="chart-tooltip"></div>
    </div>

    <!-- Interactive NAV Sensitivity Simulator -->
    <div class="simulator-card">
      <div class="chart-panel-title">
        <span>🎛️ 실시간 NAV 할인율 & SK하이닉스 주가 시뮬레이터</span>
        <span class="badge badge-success">Interactive Valuation Engine</span>
      </div>
      <p style="font-size: 13px; color: var(--text-secondary); margin-top: 4px;">
        SK하이닉스 주가 및 목표 NAV 할인율을 조절하여 SK스퀘어의 적정 주가와 기대 수익률을 실시간 산출합니다.
      </p>

      <div class="sim-grid">
        <div class="sim-control-group">
          <div class="sim-control-header">
            <span>SK하이닉스 가정 주가</span>
            <span id="sim-hynix-display" style="color: var(--primary); font-family: var(--font-mono);">183,300 원</span>
          </div>
          <input type="range" class="sim-slider" id="sim-hynix" min="120000" max="320000" step="1000" value="183300" oninput="updateSim()">
          <div style="display: flex; justify-content: space-between; font-size: 11px; color: var(--text-muted);">
            <span>120,000원 (비관)</span>
            <span>183,300원 (현재)</span>
            <span>320,000원 (낙관)</span>
          </div>
        </div>

        <div class="sim-control-group">
          <div class="sim-control-header">
            <span>목표 NAV 할인율</span>
            <span id="sim-discount-display" style="color: var(--warning); font-family: var(--font-mono);">50.0%</span>
          </div>
          <input type="range" class="sim-slider" id="sim-discount" min="30" max="70" step="1" value="50" oninput="updateSim()">
          <div style="display: flex; justify-content: space-between; font-size: 11px; color: var(--text-muted);">
            <span>30% (지주사 최상단)</span>
            <span>50% (정상화)</span>
            <span>70% (극단 디스카운트)</span>
          </div>
        </div>

        <div class="sim-result-box">
          <div class="kpi-label">시뮬레이션 산출 SK스퀘어 주가</div>
          <div class="sim-result-value" id="sim-target-price">119,080 원</div>
          <div class="kpi-sub" id="sim-target-sub" style="color: var(--success); font-weight: 600;">
            현재가 대비 +38.95% 상승 여력 (주당 NAV: 238,160원)
          </div>
        </div>
      </div>
    </div>

    <!-- Accretion Infographic Card -->
    <div class="chart-panel">
      <div class="chart-panel-title">
        <span>💎 SK하이닉스 40조 자사주 소각(2,407만 주)에 따른 SK스퀘어 재무적 수혜</span>
        <span class="badge badge-primary">BPS/EPS +3.42% Accretion</span>
      </div>
      <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 16px; margin-top: 16px;">
        <div style="background: var(--bg-input); padding: 16px; border-radius: var(--radius-md); border: 1px solid var(--border);">
          <div style="font-weight: 700; color: var(--primary); margin-bottom: 4px;">1. 지분율 자동 확대</div>
          <div style="font-size: 13px; color: var(--text-secondary);">
            SK하이닉스 총 발행주식수가 728,002,365주에서 703,932,365주로 2,407만 주 감소함에 따라, SK스퀘어 보유 지분율이 기존 <strong>20.07%에서 20.76%로 +0.69%p 자동 상승</strong>합니다.
          </div>
        </div>
        <div style="background: var(--bg-input); padding: 16px; border-radius: var(--radius-md); border: 1px solid var(--border);">
          <div style="font-weight: 700; color: var(--success); margin-bottom: 4px;">2. 주당 가치 즉각적 영구 증대</div>
          <div style="font-size: 13px; color: var(--text-secondary);">
            액크리션 팩터(Accretion Factor) 1.03419가 영구 적용되어 주당 NAV가 <strong>+6,798원 즉각 상향(238,160원 → 244,958원)</strong>되며, 배당금 및 지분법 이익 귀속분이 3.42% 영구 증대됩니다.
          </div>
        </div>
        <div style="background: var(--bg-input); padding: 16px; border-radius: var(--radius-md); border: 1px solid var(--border);">
          <div style="font-weight: 700; color: var(--warning); margin-bottom: 4px;">3. 솔리다임 가치 재평가</div>
          <div style="font-size: 13px; color: var(--text-secondary);">
            솔리다임 AI eSSD 분기 매출 100억 달러 런레이트 달성 및 1,000억~1,500억 달러 가치 평가 시, SK스퀘어 지분가치는 추가 2.5조~4조 원 추가 리레이팅 여력을 보유합니다.
          </div>
        </div>
      </div>
    </div>
  </div>

  <script>
{COMMON_JS_HEADER}

  const rawData = {combined_json};
  let activeRange = 260;

  function setRange(n) {{
    activeRange = n;
    document.querySelectorAll('.range-btn').forEach(btn => btn.classList.remove('active'));
    if (event && event.target) event.target.classList.add('active');
    renderCharts();
  }}

  function updateSim() {{
    const hynixP = parseFloat(document.getElementById('sim-hynix').value);
    const disc = parseFloat(document.getElementById('sim-discount').value);

    document.getElementById('sim-hynix-display').innerText = Number(hynixP).toLocaleString('ko-KR') + ' 원';
    document.getElementById('sim-discount-display').innerText = disc.toFixed(1) + '%';

    // NAV = Hynix * 146.1M + 4.5T (Unlisted) - (-0.8T Net Cash)
    const grossVal = hynixP * 146100000;
    const totalNav = grossVal + 4500000000000 + 800000000000;
    const navPerShare = totalNav / 134700000;
    const targetPrice = navPerShare * (1 - disc / 100);
    const currentPrice = 85700;
    const upside = ((targetPrice - currentPrice) / currentPrice) * 100;

    document.getElementById('sim-target-price').innerText = Math.round(targetPrice).toLocaleString('ko-KR') + ' 원';
    const sub = document.getElementById('sim-target-sub');
    sub.innerText = `현재가 대비 ${{upside >= 0 ? '+' : ''}}${{upside.toFixed(2)}}% (주당 NAV: ${{Math.round(navPerShare).toLocaleString('ko-KR')}}원)`;
    sub.style.color = upside >= 0 ? 'var(--success)' : 'var(--danger)';
  }}

  // High-DPI Canvas Rendering
  function renderCharts() {{
    const data = rawData.slice(-activeRange);
    renderPriceNavChart(data);
    renderDiscountChart(data);
  }}

  function setupCanvas(canvasId, containerId) {{
    const canvas = document.getElementById(canvasId);
    const container = document.getElementById(containerId);
    const dpr = window.devicePixelRatio || 1;
    const rect = container.getBoundingClientRect();
    canvas.width = rect.width * dpr;
    canvas.height = rect.height * dpr;
    const ctx = canvas.getContext('2d');
    ctx.scale(dpr, dpr);
    return {{ canvas, ctx, width: rect.width, height: rect.height }};
  }}

  function renderPriceNavChart(data) {{
    const {{ canvas, ctx, width, height }} = setupCanvas('chart-canvas-1', 'canvas-box-1');
    const pad = {{ top: 20, right: 70, bottom: 30, left: 20 }};
    const cWidth = width - pad.left - pad.right;
    const cHeight = height - pad.top - pad.bottom;

    // Y scale: NAV and Square Price
    let minVal = Infinity, maxVal = -Infinity;
    data.forEach(d => {{
      minVal = Math.min(minVal, d.sq_close, d.nav_per_share);
      maxVal = Math.max(maxVal, d.sq_close, d.accreted_nav);
    }});
    minVal = Math.floor(minVal * 0.9 / 10000) * 10000;
    maxVal = Math.ceil(maxVal * 1.05 / 10000) * 10000;

    const getY = v => pad.top + cHeight - ((v - minVal) / (maxVal - minVal)) * cHeight;
    const getX = i => pad.left + (i / (data.length - 1)) * cWidth;

    // Gridlines
    ctx.strokeStyle = '#233554';
    ctx.lineWidth = 1;
    ctx.setLineDash([4, 4]);
    ctx.fillStyle = '#94a3b8';
    ctx.font = '11px sans-serif';

    const yTicks = 5;
    for (let i = 0; i <= yTicks; i++) {{
      const v = minVal + (i / yTicks) * (maxVal - minVal);
      const y = getY(v);
      ctx.beginPath();
      ctx.moveTo(pad.left, y);
      ctx.lineTo(pad.left + cWidth, y);
      ctx.stroke();
      ctx.fillText(Math.round(v).toLocaleString('ko-KR'), pad.left + cWidth + 8, y + 4);
    }}

    // X Date Ticks
    const xStep = Math.ceil(data.length / 6);
    for (let i = 0; i < data.length; i += xStep) {{
      const x = getX(i);
      ctx.beginPath();
      ctx.moveTo(x, pad.top);
      ctx.lineTo(x, pad.top + cHeight);
      ctx.stroke();
      ctx.fillText(data[i].d.substring(5), x - 15, pad.top + cHeight + 20);
    }}
    ctx.setLineDash([]);

    // NAV Area Fill
    ctx.beginPath();
    ctx.moveTo(getX(0), getY(data[0].nav_per_share));
    for (let i = 1; i < data.length; i++) {{
      ctx.lineTo(getX(i), getY(data[i].nav_per_share));
    }}
    ctx.lineTo(getX(data.length - 1), pad.top + cHeight);
    ctx.lineTo(getX(0), pad.top + cHeight);
    ctx.closePath();
    const navGrad = ctx.createLinearGradient(0, pad.top, 0, pad.top + cHeight);
    navGrad.addColorStop(0, 'rgba(56, 189, 248, 0.25)');
    navGrad.addColorStop(1, 'rgba(56, 189, 248, 0.0)');
    ctx.fillStyle = navGrad;
    ctx.fill();

    // NAV Line
    ctx.beginPath();
    ctx.strokeStyle = '#38bdf8';
    ctx.lineWidth = 2.5;
    data.forEach((d, i) => {{
      const x = getX(i);
      const y = getY(d.nav_per_share);
      if (i === 0) ctx.moveTo(x, y); else ctx.lineTo(x, y);
    }});
    ctx.stroke();

    // Accreted NAV Line (dashed gold)
    ctx.beginPath();
    ctx.strokeStyle = '#fbbf24';
    ctx.setLineDash([5, 3]);
    ctx.lineWidth = 2;
    data.forEach((d, i) => {{
      const x = getX(i);
      const y = getY(d.accreted_nav);
      if (i === 0) ctx.moveTo(x, y); else ctx.lineTo(x, y);
    }});
    ctx.stroke();
    ctx.setLineDash([]);

    // Square Price Line
    ctx.beginPath();
    ctx.strokeStyle = '#f43f5e';
    ctx.lineWidth = 2.5;
    data.forEach((d, i) => {{
      const x = getX(i);
      const y = getY(d.sq_close);
      if (i === 0) ctx.moveTo(x, y); else ctx.lineTo(x, y);
    }});
    ctx.stroke();

    // Legend
    ctx.fillStyle = '#f8fafc';
    ctx.font = '12px sans-serif';
    ctx.fillRect(pad.left + 10, pad.top + 10, 360, 26);
    ctx.strokeRect(pad.left + 10, pad.top + 10, 360, 26);

    ctx.fillStyle = '#38bdf8'; ctx.fillRect(pad.left + 20, pad.top + 21, 14, 4);
    ctx.fillStyle = '#f8fafc'; ctx.fillText('주당 NAV (기본)', pad.left + 40, pad.top + 26);

    ctx.fillStyle = '#fbbf24'; ctx.fillRect(pad.left + 140, pad.top + 21, 14, 4);
    ctx.fillStyle = '#f8fafc'; ctx.fillText('소각후 주당 NAV (+3.4%)', pad.left + 160, pad.top + 26);

    ctx.fillStyle = '#f43f5e'; ctx.fillRect(pad.left + 290, pad.top + 21, 14, 4);
    ctx.fillStyle = '#f8fafc'; ctx.fillText('스퀘어 주가', pad.left + 310, pad.top + 26);
  }}

  function renderDiscountChart(data) {{
    const {{ canvas, ctx, width, height }} = setupCanvas('chart-canvas-2', 'canvas-box-2');
    const pad = {{ top: 15, right: 70, bottom: 25, left: 20 }};
    const cWidth = width - pad.left - pad.right;
    const cHeight = height - pad.top - pad.bottom;

    const minDisc = 40, maxDisc = 75;
    const getY = v => pad.top + cHeight - ((v - minDisc) / (maxDisc - minDisc)) * cHeight;
    const getX = i => pad.left + (i / (data.length - 1)) * cWidth;

    // Benchmark zones
    const zones = [
      {{ from: 65, to: 75, color: 'rgba(244, 63, 94, 0.15)', label: '극단 저평가 (>65%)' }},
      {{ from: 55, to: 65, color: 'rgba(245, 158, 11, 0.12)', label: '가치 매수 구간 (55~65%)' }},
      {{ from: 45, to: 55, color: 'rgba(16, 185, 129, 0.10)', label: '정상 밴드 (45~55%)' }}
    ];
    zones.forEach(z => {{
      const yTop = getY(z.to);
      const yBot = getY(z.from);
      ctx.fillStyle = z.color;
      ctx.fillRect(pad.left, yTop, cWidth, yBot - yTop);
    }});

    // Gridlines & Labels
    ctx.strokeStyle = '#233554';
    ctx.lineWidth = 1;
    ctx.setLineDash([4, 4]);
    ctx.fillStyle = '#94a3b8';
    ctx.font = '11px sans-serif';

    [45, 50, 55, 60, 65, 70].forEach(v => {{
      const y = getY(v);
      ctx.beginPath();
      ctx.moveTo(pad.left, y);
      ctx.lineTo(pad.left + cWidth, y);
      ctx.stroke();
      ctx.fillText(v + '%', pad.left + cWidth + 8, y + 4);
    }});
    ctx.setLineDash([]);

    // Discount line
    ctx.beginPath();
    ctx.strokeStyle = '#f43f5e';
    ctx.lineWidth = 2.5;
    data.forEach((d, i) => {{
      const x = getX(i);
      const y = getY(d.disc_pct);
      if (i === 0) ctx.moveTo(x, y); else ctx.lineTo(x, y);
    }});
    ctx.stroke();

    // Latest point circle
    const lastX = getX(data.length - 1);
    const lastY = getY(data[data.length - 1].disc_pct);
    ctx.beginPath();
    ctx.arc(lastX, lastY, 5, 0, Math.PI * 2);
    ctx.fillStyle = '#f43f5e';
    ctx.fill();
    ctx.strokeStyle = '#fff';
    ctx.lineWidth = 2;
    ctx.stroke();
  }}

  // Hover Tooltip Implementation
  const tooltip = document.getElementById('chart-tooltip');
  const box1 = document.getElementById('canvas-box-1');

  box1.addEventListener('mousemove', e => {{
    const rect = box1.getBoundingClientRect();
    const mouseX = e.clientX - rect.left;
    const pad = {{ left: 20, right: 70 }};
    const cWidth = rect.width - pad.left - pad.right;

    if (mouseX < pad.left || mouseX > pad.left + cWidth) {{
      tooltip.style.display = 'none';
      return;
    }}

    const data = rawData.slice(-activeRange);
    const ratio = (mouseX - pad.left) / cWidth;
    const idx = Math.min(data.length - 1, Math.max(0, Math.round(ratio * (data.length - 1))));
    const d = data[idx];

    tooltip.style.display = 'block';
    tooltip.style.left = (e.clientX - rect.left + 15) + 'px';
    tooltip.style.top = (e.clientY - rect.top + 15) + 'px';

    tooltip.innerHTML = `
      <div class="tooltip-header">${{d.d}} 거래일 팩트</div>
      <div class="tooltip-row"><span>SK스퀘어 종가</span><span style="color: #f43f5e">${{d.sq_close.toLocaleString()}} 원</span></div>
      <div class="tooltip-row"><span>주당 NAV</span><span style="color: #38bdf8">${{Math.round(d.nav_per_share).toLocaleString()}} 원</span></div>
      <div class="tooltip-row"><span>소각후 주당 NAV</span><span style="color: #fbbf24">${{Math.round(d.accreted_nav).toLocaleString()}} 원</span></div>
      <div class="tooltip-row"><span>NAV 할인율</span><span style="color: ${{d.disc_pct >= 60 ? '#f43f5e' : '#10b981'}}">${{d.disc_pct.toFixed(2)}}%</span></div>
      <div class="tooltip-row"><span>SK하이닉스 주가</span><span>${{d.hy_close.toLocaleString()}} 원</span></div>
    `;
    document.getElementById('hover-date-badge').innerText = d.d + ' (할인율 ' + d.disc_pct.toFixed(2) + '%)';
  }});

  box1.addEventListener('mouseleave', () => {{
    tooltip.style.display = 'none';
  }});

  window.addEventListener('resize', renderCharts);
  window.addEventListener('DOMContentLoaded', () => {{
    renderCharts();
    updateSim();
  }});
  </script>
</body>
</html>
"""

with open(os.path.join(CHARTS_DIR, "nav_discount_chart.html"), "w", encoding="utf-8") as f:
    f.write(nav_html)
print("Saved charts/nav_discount_chart.html")

# ---------------------------------------------------------------------------
# 3. Build charts/beta_spread_chart.html
# ---------------------------------------------------------------------------
beta_html = f"""<!DOCTYPE html>
<html lang="ko" data-theme="dark">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>SK Square vs SK Hynix Beta & Spread Analyzer | Standalone Interactive Chart</title>
  <style>
{COMMON_CSS}
  </style>
</head>
<body>
  <div class="container">
    <header class="chart-header">
      <div class="chart-title">
        <h1>⚡ SK Square vs SK Hynix Beta & Spread Analyzer</h1>
        <p>선현물 베이시스, 외인 선물 수급, 롤링 베타 및 비대칭 하방 베타(Asymmetric Downside Beta) 구조적 추적</p>
      </div>
      <div class="chart-actions">
        <span class="badge badge-primary">Zero-CDN Offline</span>
        <button class="btn" onclick="toggleTheme()">🌓 테마 전환</button>
        <a href="../dashboard.html" class="btn">📊 종합 대시보드</a>
      </div>
    </header>

    <div class="kpi-grid">
      <div class="kpi-card">
        <div class="kpi-label">20일 롤링 베타 (Beta)</div>
        <div class="kpi-value" style="color: var(--primary);">2.39x</div>
        <div class="kpi-sub"><span class="badge badge-warning">고변동성 증폭</span> 60일 1.35x / 120일 0.93x</div>
      </div>
      <div class="kpi-card">
        <div class="kpi-label">비대칭 하방 베타 비율</div>
        <div class="kpi-value" style="color: var(--danger);">1.63x</div>
        <div class="kpi-sub"><span class="badge badge-danger">하방 민감도 과잉</span> 하방 1.84x vs 상방 1.13x</div>
      </div>
      <div class="kpi-card">
        <div class="kpi-label">KOSPI200 선·현물 베이시스</div>
        <div class="kpi-value" style="color: var(--warning);">-0.85 pt</div>
        <div class="kpi-sub"><span class="badge badge-warning">백워데이션 지속</span> 이론치 +0.45pt 대비 약세</div>
      </div>
      <div class="kpi-card">
        <div class="kpi-label">외국인 선물 3일 누적</div>
        <div class="kpi-value" style="color: var(--danger);">-7,878 계약</div>
        <div class="kpi-sub"><span class="badge badge-danger">프로그램 매도 압력</span> 당일 -4,250계약 순매도</div>
      </div>
      <div class="kpi-card">
        <div class="kpi-label">수익률 스프레드 (스퀘어-하이닉스)</div>
        <div class="kpi-value" style="color: var(--success);">+3.42%</div>
        <div class="kpi-sub"><span class="badge badge-success">단기 반등 스프레드</span> 일간 +6.18%p 아웃퍼폼</div>
      </div>
    </div>

    <!-- Main Multi-Panel Chart -->
    <div class="chart-panel">
      <div class="chart-panel-header">
        <div class="chart-panel-title">
          <span>📉 롤링 베타 & 수익률 스프레드 & 파생시장 메커니즘</span>
          <span class="badge badge-primary" id="hover-beta-badge">2026-10-13 기준</span>
        </div>
        <div class="chart-controls">
          <div class="range-btn-group">
            <button class="range-btn" onclick="setRange(22)">1M</button>
            <button class="range-btn" onclick="setRange(65)">3M</button>
            <button class="range-btn" onclick="setRange(130)">6M</button>
            <button class="range-btn active" onclick="setRange(260)">전체 (1Y)</button>
          </div>
        </div>
      </div>

      <!-- Panel 1: Rolling Betas -->
      <div style="font-size: 13px; font-weight: 600; color: var(--text-secondary); margin-bottom: 6px;">
        [패널 1] SK스퀘어의 SK하이닉스 대비 롤링 베타 (20일선 Cyan, 60일선 Indigo, 120일선 Amber / 기준선 1.0x)
      </div>
      <div class="canvas-container" style="height: 250px;" id="beta-box-1">
        <canvas id="beta-canvas-1"></canvas>
      </div>

      <!-- Panel 2: Cumulative Return Spread -->
      <div style="font-size: 13px; font-weight: 600; color: var(--text-secondary); margin: 18px 0 6px 0;">
        [패널 2] 누적 수익률 스프레드 (%) — 하이닉스 대비 스퀘어의 초과/열위 성과 추이
      </div>
      <div class="canvas-container" style="height: 160px;" id="beta-box-2">
        <canvas id="beta-canvas-2"></canvas>
      </div>

      <!-- Panel 3: Basis and Foreign Futures -->
      <div style="font-size: 13px; font-weight: 600; color: var(--text-secondary); margin: 18px 0 6px 0;">
        [패널 3] KOSPI200 시장 베이시스 (pt) 및 백워데이션/콘탱고 레짐
      </div>
      <div class="canvas-container" style="height: 140px;" id="beta-box-3">
        <canvas id="beta-canvas-3"></canvas>
      </div>

      <div class="tooltip" id="beta-tooltip"></div>
    </div>

    <!-- Asymmetric Beta Stress Simulator -->
    <div class="simulator-card">
      <div class="chart-panel-title">
        <span>⚙️ 비대칭 하방 베타(Asymmetric Downside Beta) 민감도 시뮬레이터</span>
        <span class="badge badge-danger">Downside Risk Engine</span>
      </div>
      <p style="font-size: 13px; color: var(--text-secondary); margin-top: 4px;">
        SK하이닉스 주가 변동에 따른 SK스퀘어의 비대칭적 주가 반응(상승 시 베타 1.54 vs 하락 시 베타 2.39)을 시뮬레이션합니다.
      </p>

      <div class="sim-grid">
        <div class="sim-control-group">
          <div class="sim-control-header">
            <span>SK하이닉스 일간 예상 변동률</span>
            <span id="sim-hy-delta" style="color: var(--primary); font-family: var(--font-mono);">-5.0%</span>
          </div>
          <input type="range" class="sim-slider" id="sim-hy-slider" min="-15" max="15" step="0.5" value="-5" oninput="updateBetaSim()">
          <div style="display: flex; justify-content: space-between; font-size: 11px; color: var(--text-muted);">
            <span>-15% (급락 쇼크)</span>
            <span>0% (보합)</span>
            <span>+15% (서프라이즈)</span>
          </div>
        </div>

        <div class="sim-result-box">
          <div class="kpi-label">적용 베타 계수</div>
          <div class="sim-result-value" id="sim-applied-beta" style="font-size: 26px; color: var(--danger);">2.39x (하방 증폭)</div>
          <div class="kpi-sub" style="color: var(--text-secondary);">
            하방 국면($R_{{hy}} < 0$)에서는 지주사 할인 확대와 ETF 환매로 인해 베타가 급증합니다.
          </div>
        </div>

        <div class="sim-result-box">
          <div class="kpi-label">SK스퀘어 예상 등락률 & 가격</div>
          <div class="sim-result-value" id="sim-sq-result" style="color: var(--danger);">-11.95%</div>
          <div class="kpi-sub" id="sim-sq-price-sub" style="color: var(--text-secondary); font-weight: 600;">
            예상 종가: 75,460 원 (-10,240원)
          </div>
        </div>
      </div>
    </div>

    <!-- Market Mechanism Analysis -->
    <div class="chart-panel">
      <div class="chart-panel-title">
        <span>🔬 왜 SK스퀘어는 하이닉스보다 하락폭이 더 큰가? (3대 구조적 원인)</span>
        <span class="badge badge-warning">Microstructure Mechanics</span>
      </div>
      <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 16px; margin-top: 16px;">
        <div style="background: var(--bg-input); padding: 16px; border-radius: var(--radius-md); border: 1px solid var(--border);">
          <div style="font-weight: 700; color: var(--danger); margin-bottom: 4px;">1. 지주사 디스카운트 탄력성</div>
          <div style="font-size: 13px; color: var(--text-secondary);">
            반도체 업황 침체 우려 발생 시, 시장 참여자들은 직상장 하이닉스보다 지주사 SK스퀘어에 대해 보수적인 할인율(50% → 65%+)을 적용하여 <strong>지분가치 하락폭 이상으로 주가를 할인</strong>시킵니다.
          </div>
        </div>
        <div style="background: var(--bg-input); padding: 16px; border-radius: var(--radius-md); border: 1px solid var(--border);">
          <div style="font-weight: 700; color: var(--warning); margin-bottom: 4px;">2. 패시브/ETF 바스켓 환매 충격</div>
          <div style="font-size: 13px; color: var(--text-secondary);">
            코스피200 및 반도체 테마 ETF 대량 환매 시, 유동성이 하이닉스(시총 133조) 대비 작은 SK스퀘어(시총 11조) 호가창에 프로그램 비차익 매도가 집중되며 <strong>가격 슬리피지(Slippage)가 2~3배 확대</strong>됩니다.
          </div>
        </div>
        <div style="background: var(--bg-input); padding: 16px; border-radius: var(--radius-md); border: 1px solid var(--border);">
          <div style="font-weight: 700; color: var(--primary); margin-bottom: 4px;">3. 선물 백워데이션과 차익거래 매도</div>
          <div style="font-size: 13px; color: var(--text-secondary);">
            외국인 선물 매도로 베이시스가 -0.85pt 이하 역전(백워데이션)될 때 금융투자 차익 매도 프로그램이 현물 바스켓을 기계적으로 투매하여 <strong>스퀘어의 하방 변동성을 구조적으로 심화</strong>시킵니다.
          </div>
        </div>
      </div>
    </div>
  </div>

  <script>
{COMMON_JS_HEADER}

  const rawData = {combined_json};
  let activeRange = 260;

  function setRange(n) {{
    activeRange = n;
    document.querySelectorAll('.range-btn').forEach(btn => btn.classList.remove('active'));
    if (event && event.target) event.target.classList.add('active');
    renderBetaCharts();
  }}

  function updateBetaSim() {{
    const hyDelta = parseFloat(document.getElementById('sim-hy-slider').value);
    document.getElementById('sim-hy-delta').innerText = (hyDelta >= 0 ? '+' : '') + hyDelta.toFixed(1) + '%';

    const beta = hyDelta < 0 ? 2.39 : (hyDelta > 0 ? 1.54 : 1.0);
    const sqDelta = hyDelta * beta;
    const currentP = 85700;
    const expP = Math.round(currentP * (1 + sqDelta / 100));
    const pDiff = expP - currentP;

    const betaElem = document.getElementById('sim-applied-beta');
    betaElem.innerText = beta.toFixed(2) + 'x ' + (hyDelta < 0 ? '(하방 증폭)' : (hyDelta > 0 ? '(상방 반응)' : '(중립)'));
    betaElem.style.color = hyDelta < 0 ? 'var(--danger)' : 'var(--success)';

    const resElem = document.getElementById('sim-sq-result');
    resElem.innerText = (sqDelta >= 0 ? '+' : '') + sqDelta.toFixed(2) + '%';
    resElem.style.color = sqDelta >= 0 ? 'var(--success)' : 'var(--danger)';

    const subElem = document.getElementById('sim-sq-price-sub');
    subElem.innerText = `예상 종가: ${{expP.toLocaleString()}} 원 (${{pDiff >= 0 ? '+' : ''}}${{pDiff.toLocaleString()}}원)`;
  }}

  function setupCanvas(canvasId, containerId) {{
    const canvas = document.getElementById(canvasId);
    const container = document.getElementById(containerId);
    const dpr = window.devicePixelRatio || 1;
    const rect = container.getBoundingClientRect();
    canvas.width = rect.width * dpr;
    canvas.height = rect.height * dpr;
    const ctx = canvas.getContext('2d');
    ctx.scale(dpr, dpr);
    return {{ canvas, ctx, width: rect.width, height: rect.height }};
  }}

  function renderBetaCharts() {{
    const data = rawData.slice(-activeRange);
    renderPanel1(data);
    renderPanel2(data);
    renderPanel3(data);
  }}

  function renderPanel1(data) {{
    const {{ canvas, ctx, width, height }} = setupCanvas('beta-canvas-1', 'beta-box-1');
    const pad = {{ top: 15, right: 60, bottom: 25, left: 20 }};
    const cWidth = width - pad.left - pad.right;
    const cHeight = height - pad.top - pad.bottom;

    const minBeta = 0.5, maxBeta = 3.5;
    const getY = v => pad.top + cHeight - ((v - minBeta) / (maxBeta - minBeta)) * cHeight;
    const getX = i => pad.left + (i / (data.length - 1)) * cWidth;

    // High beta warning zone (>1.5x)
    ctx.fillStyle = 'rgba(244, 63, 94, 0.08)';
    ctx.fillRect(pad.left, getY(3.5), cWidth, getY(1.5) - getY(3.5));

    // Parity line 1.0x
    ctx.strokeStyle = '#94a3b8';
    ctx.lineWidth = 1.5;
    ctx.setLineDash([4, 4]);
    ctx.beginPath();
    ctx.moveTo(pad.left, getY(1.0));
    ctx.lineTo(pad.left + cWidth, getY(1.0));
    ctx.stroke();
    ctx.fillStyle = '#94a3b8';
    ctx.fillText('1.0x (패리티)', pad.left + cWidth + 6, getY(1.0) + 4);

    // Gridlines
    ctx.strokeStyle = '#233554';
    ctx.lineWidth = 1;
    [1.5, 2.0, 2.5, 3.0].forEach(v => {{
      const y = getY(v);
      ctx.beginPath();
      ctx.moveTo(pad.left, y);
      ctx.lineTo(pad.left + cWidth, y);
      ctx.stroke();
      ctx.fillText(v.toFixed(1) + 'x', pad.left + cWidth + 6, y + 4);
    }});
    ctx.setLineDash([]);

    // 120D Beta Line (Amber)
    ctx.beginPath();
    ctx.strokeStyle = '#f59e0b';
    ctx.lineWidth = 1.5;
    data.forEach((d, i) => {{
      const x = getX(i); const y = getY(d.rolling_beta_120d);
      if (i === 0) ctx.moveTo(x, y); else ctx.lineTo(x, y);
    }});
    ctx.stroke();

    // 60D Beta Line (Indigo)
    ctx.beginPath();
    ctx.strokeStyle = '#818cf8';
    ctx.lineWidth = 2.0;
    data.forEach((d, i) => {{
      const x = getX(i); const y = getY(d.rolling_beta_60d);
      if (i === 0) ctx.moveTo(x, y); else ctx.lineTo(x, y);
    }});
    ctx.stroke();

    // 20D Beta Line (Cyan)
    ctx.beginPath();
    ctx.strokeStyle = '#38bdf8';
    ctx.lineWidth = 2.5;
    data.forEach((d, i) => {{
      const x = getX(i); const y = getY(d.rolling_beta_20d);
      if (i === 0) ctx.moveTo(x, y); else ctx.lineTo(x, y);
    }});
    ctx.stroke();

    // Legend
    ctx.fillStyle = '#f8fafc';
    ctx.font = '11px sans-serif';
    ctx.fillStyle = '#38bdf8'; ctx.fillText('■ 20일 롤링 베타', pad.left + 10, pad.top + 16);
    ctx.fillStyle = '#818cf8'; ctx.fillText('■ 60일', pad.left + 120, pad.top + 16);
    ctx.fillStyle = '#f59e0b'; ctx.fillText('■ 120일', pad.left + 180, pad.top + 16);
  }}

  function renderPanel2(data) {{
    const {{ canvas, ctx, width, height }} = setupCanvas('beta-canvas-2', 'beta-box-2');
    const pad = {{ top: 10, right: 60, bottom: 20, left: 20 }};
    const cWidth = width - pad.left - pad.right;
    const cHeight = height - pad.top - pad.bottom;

    let minS = -30, maxS = 40;
    const getY = v => pad.top + cHeight - ((v - minS) / (maxS - minS)) * cHeight;
    const getX = i => pad.left + (i / (data.length - 1)) * cWidth;

    // Zero baseline
    ctx.strokeStyle = '#64748b';
    ctx.lineWidth = 1;
    ctx.beginPath();
    ctx.moveTo(pad.left, getY(0));
    ctx.lineTo(pad.left + cWidth, getY(0));
    ctx.stroke();
    ctx.fillStyle = '#94a3b8';
    ctx.font = '10px sans-serif';
    ctx.fillText('0.0%', pad.left + cWidth + 6, getY(0) + 3);

    // Spread line
    ctx.beginPath();
    ctx.strokeStyle = '#10b981';
    ctx.lineWidth = 2.0;
    data.forEach((d, i) => {{
      const x = getX(i); const y = getY(d.cum_return_spread_pct);
      if (i === 0) ctx.moveTo(x, y); else ctx.lineTo(x, y);
    }});
    ctx.stroke();

    ctx.fillStyle = 'rgba(16, 185, 129, 0.12)';
    ctx.lineTo(getX(data.length - 1), getY(0));
    ctx.lineTo(getX(0), getY(0));
    ctx.closePath();
    ctx.fill();
  }}

  function renderPanel3(data) {{
    const {{ canvas, ctx, width, height }} = setupCanvas('beta-canvas-3', 'beta-box-3');
    const pad = {{ top: 10, right: 60, bottom: 20, left: 20 }};
    const cWidth = width - pad.left - pad.right;
    const cHeight = height - pad.top - pad.bottom;

    const minB = -3.0, maxB = 2.0;
    const getY = v => pad.top + cHeight - ((v - minB) / (maxB - minB)) * cHeight;
    const getX = i => pad.left + (i / (data.length - 1)) * cWidth;
    const barWidth = Math.max(1, (cWidth / data.length) * 0.8);

    ctx.strokeStyle = '#94a3b8';
    ctx.lineWidth = 1;
    ctx.beginPath();
    ctx.moveTo(pad.left, getY(0));
    ctx.lineTo(pad.left + cWidth, getY(0));
    ctx.stroke();

    const y0 = getY(0);
    data.forEach((d, i) => {{
      const x = getX(i) - barWidth / 2;
      const y = getY(d.basis);
      ctx.fillStyle = d.basis >= 0 ? '#10b981' : '#f43f5e';
      ctx.fillRect(x, Math.min(y0, y), barWidth, Math.abs(y - y0));
    }});
  }}

  const tooltip = document.getElementById('beta-tooltip');
  const box1 = document.getElementById('beta-box-1');

  box1.addEventListener('mousemove', e => {{
    const rect = box1.getBoundingClientRect();
    const mouseX = e.clientX - rect.left;
    const pad = {{ left: 20, right: 60 }};
    const cWidth = rect.width - pad.left - pad.right;

    if (mouseX < pad.left || mouseX > pad.left + cWidth) {{
      tooltip.style.display = 'none'; return;
    }}
    const data = rawData.slice(-activeRange);
    const ratio = (mouseX - pad.left) / cWidth;
    const idx = Math.min(data.length - 1, Math.max(0, Math.round(ratio * (data.length - 1))));
    const d = data[idx];

    tooltip.style.display = 'block';
    tooltip.style.left = (e.clientX - rect.left + 15) + 'px';
    tooltip.style.top = (e.clientY - rect.top + 15) + 'px';

    tooltip.innerHTML = `
      <div class="tooltip-header">${{d.d}} 파생/베타 지표</div>
      <div class="tooltip-row"><span>20일 롤링 베타</span><span style="color: #38bdf8">${{d.rolling_beta_20d.toFixed(2)}}x</span></div>
      <div class="tooltip-row"><span>60일 롤링 베타</span><span style="color: #818cf8">${{d.rolling_beta_60d.toFixed(2)}}x</span></div>
      <div class="tooltip-row"><span>시장 베이시스</span><span style="color: ${{d.basis >= 0 ? '#10b981' : '#f43f5e'}}">${{d.basis.toFixed(2)}} pt (${{d.basis_regime}})</span></div>
      <div class="tooltip-row"><span>외인 선물 3일누적</span><span>${{Math.round(d.foreign_futures_cum_3d).toLocaleString()}} 계약</span></div>
      <div class="tooltip-row"><span>누적 수익률 스프레드</span><span style="color: #10b981">${{d.cum_return_spread_pct.toFixed(2)}}%</span></div>
    `;
    document.getElementById('hover-beta-badge').innerText = d.d + ' (20D Beta: ' + d.rolling_beta_20d.toFixed(2) + 'x)';
  }});

  box1.addEventListener('mouseleave', () => {{ tooltip.style.display = 'none'; }});

  window.addEventListener('resize', renderBetaCharts);
  window.addEventListener('DOMContentLoaded', () => {{
    renderBetaCharts();
    updateBetaSim();
  }});
  </script>
</body>
</html>
"""

with open(os.path.join(CHARTS_DIR, "beta_spread_chart.html"), "w", encoding="utf-8") as f:
    f.write(beta_html)
print("Saved charts/beta_spread_chart.html")

# ---------------------------------------------------------------------------
# 4. Build charts/historical_analogs_chart.html
# ---------------------------------------------------------------------------
analogs_html = f"""<!DOCTYPE html>
<html lang="ko" data-theme="dark">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Historical Leading Stock Analogs & Trajectory Classifier | Standalone Interactive Chart</title>
  <style>
{COMMON_CSS}
    .filter-btn-group {{
      display: inline-flex;
      background: var(--bg-input);
      border-radius: var(--radius-sm);
      padding: 3px;
      gap: 4px;
      border: 1px solid var(--border);
    }}
    .filter-btn {{
      padding: 6px 14px;
      font-size: 12px;
      font-weight: 600;
      border: none;
      background: transparent;
      color: var(--text-secondary);
      border-radius: var(--radius-sm);
      cursor: pointer;
      transition: var(--transition);
    }}
    .filter-btn.active, .filter-btn:hover {{
      background: var(--bg-card);
      color: var(--primary);
    }}
    .traj-badge-v {{ background: var(--success-glow); color: var(--success); border: 1px solid var(--success); }}
    .traj-badge-w {{ background: var(--primary-glow); color: var(--primary); border: 1px solid var(--primary); }}
    .traj-badge-l {{ background: var(--danger-glow); color: var(--danger); border: 1px solid var(--danger); }}
  </style>
</head>
<body>
  <div class="container">
    <header class="chart-header">
      <div class="chart-title">
        <h1>📜 6대 주도주 50%+ 조정 복원 유사사례 (Historical Analogs)</h1>
        <p>과거 반도체/빅테크 사상 최대 실적 후 40~60% 폭락 유사사례와 V vs W vs L자 복원 경로 정량 분석</p>
      </div>
      <div class="chart-actions">
        <span class="badge badge-primary">Zero-CDN Offline</span>
        <button class="btn" onclick="toggleTheme()">🌓 테마 전환</button>
        <a href="../dashboard.html" class="btn">📊 종합 대시보드</a>
      </div>
    </header>

    <div class="kpi-grid">
      <div class="kpi-card">
        <div class="kpi-label">정량 분석 유사사례</div>
        <div class="kpi-value" style="color: var(--primary);">6 개 사례</div>
        <div class="kpi-sub"><span class="badge badge-primary">한·미 주도주 전수</span> Hynix, MU, TSM, NVDA, 삼전</div>
      </div>
      <div class="kpi-card">
        <div class="kpi-label">평균 최대 낙폭 (MDD)</div>
        <div class="kpi-value" style="color: var(--danger);">-53.20%</div>
        <div class="kpi-sub"><span class="badge badge-warning">스퀘어 현재 -42.5%</span> 바닥 임계 진입 구간</div>
      </div>
      <div class="kpi-card">
        <div class="kpi-label">바닥 형성 소요 일수</div>
        <div class="kpi-value">198 거래일</div>
        <div class="kpi-sub"><span class="badge badge-primary">중앙값 173일</span> 약 7~10개월 소요</div>
      </div>
      <div class="kpi-card">
        <div class="kpi-label">바닥 후 +12M 평균 수익률</div>
        <div class="kpi-value" style="color: var(--success);">+106.9%</div>
        <div class="kpi-sub"><span class="badge badge-success">V자 +181% / W자 +81%</span> L자 +36%</div>
      </div>
      <div class="kpi-card">
        <div class="kpi-label">스퀘어 현재 복원 가능성</div>
        <div class="kpi-value" style="color: var(--warning);">W자 유력 (60%)</div>
        <div class="kpi-sub"><span class="badge badge-warning">10/27 실적 전후</span> 이중바닥 테스트 국면</div>
      </div>
    </div>

    <!-- Trajectory Overlay Chart Panel -->
    <div class="chart-panel">
      <div class="chart-panel-header">
        <div class="chart-panel-title">
          <span>📈 바닥(Trough Day 0) 기준 정규화 주가 궤적 오버레이 (-60D ~ +250D)</span>
        </div>
        <div class="chart-controls">
          <div class="filter-btn-group">
            <button class="filter-btn active" onclick="setTrajFilter('ALL')">전체 (6건)</button>
            <button class="filter-btn" onclick="setTrajFilter('V_SHAPE')">V자 급반등 (2건)</button>
            <button class="filter-btn" onclick="setTrajFilter('W_SHAPE')">W자 기간조정 (3건)</button>
            <button class="filter-btn" onclick="setTrajFilter('L_SHAPE')">L자 장기소외 (1건)</button>
          </div>
        </div>
      </div>

      <div class="canvas-container" style="height: 420px;" id="analogs-box">
        <canvas id="analogs-canvas"></canvas>
      </div>

      <div class="tooltip" id="analogs-tooltip"></div>
    </div>

    <!-- Analog Cases Data Table -->
    <div class="chart-panel">
      <div class="chart-panel-title">
        <span>📋 6대 유사사례 정량 비교 매트릭스 & SK스퀘어 현재 국면 대조</span>
      </div>
      <div class="table-wrapper">
        <table class="custom-table" id="analogs-table">
          <thead>
            <tr>
              <th>사례 식별자</th>
              <th>종목명 및 국면</th>
              <th>조정 기간</th>
              <th>고점 / 저점</th>
              <th>최대낙폭 (MDD)</th>
              <th>바닥 소요</th>
              <th>궤적 유형</th>
              <th>+1M</th>
              <th>+3M</th>
              <th>+6M</th>
              <th>+12M</th>
              <th>핵심 하락 동인 & 반등 촉매</th>
            </tr>
          </thead>
          <tbody>
            <!-- Populated via JavaScript -->
          </tbody>
        </table>
      </div>
    </div>

    <!-- V vs W vs L Archetype Analysis -->
    <div class="chart-panel">
      <div class="chart-panel-title">
        <span>🎯 V자 vs W자 vs L자 궤적을 가른 4대 결정 변수 (Attribution Model)</span>
      </div>
      <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 16px; margin-top: 16px;">
        <div style="background: var(--bg-input); padding: 18px; border-radius: var(--radius-md); border: 1px solid var(--border);">
          <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
            <span style="font-weight: 700; color: var(--success); font-size: 15px;">V자 직행 급반등 (TSMC 2022, NVDA 2022)</span>
            <span class="badge traj-badge-v">V_SHAPE</span>
          </div>
          <p style="font-size: 13px; color: var(--text-secondary); line-height: 1.6;">
            <strong>결정 변수:</strong> 거시 매크로(연준 금리 인하 피벗)와 <strong>파괴적 신규 수요(ChatGPT AI 혁명, 버크셔 13F 매수)</strong>가 결합될 때 발생. 주가 하락은 가파르지만 실적 턴어라운드가 즉각 입증되며 전고점을 6~12개월 만에 돌파.
          </p>
        </div>

        <div style="background: var(--bg-input); padding: 18px; border-radius: var(--radius-md); border: 1px solid var(--border);">
          <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
            <span style="font-weight: 700; color: var(--primary); font-size: 15px;">W자 기간조정 후 반등 (Hynix 2018, MU 2018, NVDA 2018)</span>
            <span class="badge traj-badge-w">W_SHAPE</span>
          </div>
          <p style="font-size: 13px; color: var(--text-secondary); line-height: 1.6;">
            <strong>결정 변수:</strong> 1차 과매도 기술적 반등 후 <strong>실적 적자 전환/재고 소진 확인을 위한 2차 바닥 테스트(이중바닥)</strong>를 거침. 공급사들의 자율 감산 합의와 고객사 재고 소진이 완료되는 2개 분기 후 대세 상승 국면 재진입.
          </p>
        </div>

        <div style="background: var(--bg-input); padding: 18px; border-radius: var(--radius-md); border: 1px solid var(--border);">
          <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
            <span style="font-weight: 700; color: var(--danger); font-size: 15px;">L자 장기 침체 소외 (삼성전자 2021-2022)</span>
            <span class="badge traj-badge-l">L_SHAPE</span>
          </div>
          <p style="font-size: 13px; color: var(--text-secondary); line-height: 1.6;">
            <strong>결정 변수:</strong> 경영진의 <strong>인위적 감산 지연(시장점유율 확대 전략)</strong>으로 채널 재고 누증이 4분기 이상 장기화되고, 차세대 고수익 제품(HBM/DDR5) 경쟁에서 뒤처지며 2년 이상 장기 횡보 박스권에 갇힘.
          </p>
        </div>
      </div>
    </div>
  </div>

  <script>
{COMMON_JS_HEADER}

  const casesData = {analogs_json};
  let currentFilter = 'ALL';

  function setTrajFilter(f) {{
    currentFilter = f;
    document.querySelectorAll('.filter-btn').forEach(btn => btn.classList.remove('active'));
    if (event && event.target) event.target.classList.add('active');
    renderAnalogsChart();
    renderTable();
  }}

  // Synthetic normalized trajectory points (-60 to +250 days, Trough Day 0 = 100)
  function getTrajectoryPoints(c) {{
    const pts = [];
    const peakRet = 100 / (1 + c.mdd_pct / 100); // Peak normalized value
    // Pre-trough (-60 to 0)
    for (let day = -60; day <= 0; day += 5) {{
      const t = (day + 60) / 60;
      const val = peakRet - (peakRet - 100) * Math.pow(t, 1.4);
      pts.push({{ day, val }});
    }}
    // Post-trough (0 to +250)
    const m1 = 100 * (1 + c.return_1m / 100);
    const m3 = 100 * (1 + c.return_3m / 100);
    const m6 = 100 * (1 + c.return_6m / 100);
    const m12 = 100 * (1 + c.return_12m / 100);

    for (let day = 5; day <= 250; day += 5) {{
      let val = 100;
      if (day <= 22) {{
        val = 100 + (m1 - 100) * (day / 22);
      }} else if (day <= 65) {{
        // W-shape dip around day 40-50 if W
        if (c.trajectory_type === 'W_SHAPE') {{
          val = m1 + (m3 - m1) * ((day - 22) / 43) - 8 * Math.sin(Math.PI * (day - 22) / 43);
        }} else {{
          val = m1 + (m3 - m1) * ((day - 22) / 43);
        }}
      }} else if (day <= 130) {{
        val = m3 + (m6 - m3) * ((day - 65) / 65);
      }} else {{
        val = m6 + (m12 - m6) * ((day - 130) / 120);
      }}
      pts.push({{ day, val }});
    }}
    return pts;
  }}

  function setupCanvas(canvasId, containerId) {{
    const canvas = document.getElementById(canvasId);
    const container = document.getElementById(containerId);
    const dpr = window.devicePixelRatio || 1;
    const rect = container.getBoundingClientRect();
    canvas.width = rect.width * dpr;
    canvas.height = rect.height * dpr;
    const ctx = canvas.getContext('2d');
    ctx.scale(dpr, dpr);
    return {{ canvas, ctx, width: rect.width, height: rect.height }};
  }}

  function renderAnalogsChart() {{
    const {{ canvas, ctx, width, height }} = setupCanvas('analogs-canvas', 'analogs-box');
    const pad = {{ top: 20, right: 60, bottom: 35, left: 30 }};
    const cWidth = width - pad.left - pad.right;
    const cHeight = height - pad.top - pad.bottom;

    const minDay = -60, maxDay = 250;
    const minVal = 80, maxVal = 420; // 100 = bottom, 400 = 4x

    const getX = d => pad.left + ((d - minDay) / (maxDay - minDay)) * cWidth;
    const getY = v => pad.top + cHeight - ((v - minVal) / (maxVal - minVal)) * cHeight;

    // Trough baseline (100)
    ctx.strokeStyle = '#38bdf8';
    ctx.lineWidth = 1.5;
    ctx.setLineDash([4, 4]);
    ctx.beginPath();
    ctx.moveTo(pad.left, getY(100));
    ctx.lineTo(pad.left + cWidth, getY(100));
    ctx.stroke();
    ctx.fillStyle = '#38bdf8';
    ctx.font = '11px sans-serif';
    ctx.fillText('100.0 (바닥 Trough)', pad.left + cWidth + 6, getY(100) + 4);

    // Day 0 Vertical Line
    ctx.strokeStyle = '#64748b';
    ctx.beginPath();
    ctx.moveTo(getX(0), pad.top);
    ctx.lineTo(getX(0), pad.top + cHeight);
    ctx.stroke();
    ctx.fillStyle = '#64748b';
    ctx.fillText('Day 0 (저점)', getX(0) - 15, pad.top + cHeight + 20);

    // Gridlines
    ctx.strokeStyle = '#233554';
    ctx.lineWidth = 1;
    [150, 200, 250, 300, 350, 400].forEach(v => {{
      const y = getY(v);
      ctx.beginPath();
      ctx.moveTo(pad.left, y);
      ctx.lineTo(pad.left + cWidth, y);
      ctx.stroke();
      ctx.fillStyle = '#94a3b8';
      ctx.fillText('+' + (v - 100) + '%', pad.left + cWidth + 6, y + 4);
    }});

    [-40, -20, 20, 50, 100, 150, 200, 250].forEach(d => {{
      if (d === 0) return;
      const x = getX(d);
      ctx.beginPath();
      ctx.moveTo(x, pad.top);
      ctx.lineTo(x, pad.top + cHeight);
      ctx.stroke();
      ctx.fillStyle = '#94a3b8';
      ctx.fillText('D' + (d > 0 ? '+' : '') + d, x - 12, pad.top + cHeight + 20);
    }});
    ctx.setLineDash([]);

    // Plot Cases
    const colors = {{
      'ANALOG-01': '#38bdf8', // Hynix 2018 (W)
      'ANALOG-02': '#60a5fa', // Micron 2018 (W)
      'ANALOG-03': '#34d399', // TSMC 2022 (V)
      'ANALOG-04': '#818cf8', // NVDA 2018 (W)
      'ANALOG-05': '#10b981', // NVDA 2022 (V)
      'ANALOG-06': '#f43f5e', // Samsung 2021 (L)
    }};

    casesData.forEach(c => {{
      if (currentFilter !== 'ALL' && c.trajectory_type !== currentFilter) return;

      const pts = getTrajectoryPoints(c);
      ctx.beginPath();
      ctx.strokeStyle = colors[c.case_id] || '#fff';
      ctx.lineWidth = c.trajectory_type === 'V_SHAPE' ? 2.5 : 2.0;

      pts.forEach((p, i) => {{
        const x = getX(p.day);
        const y = getY(p.val);
        if (i === 0) ctx.moveTo(x, y); else ctx.lineTo(x, y);
      }});
      ctx.stroke();

      // Label at end
      const last = pts[pts.length - 1];
      ctx.fillStyle = colors[c.case_id];
      ctx.font = '10px sans-serif';
      ctx.fillText(c.name.split(' ')[0], getX(last.day) - 35, getY(last.val) - 6);
    }});
  }}

  function renderTable() {{
    const tbody = document.querySelector('#analogs-table tbody');
    tbody.innerHTML = '';

    casesData.forEach(c => {{
      if (currentFilter !== 'ALL' && c.trajectory_type !== currentFilter) return;

      const tr = document.createElement('tr');
      const badgeClass = c.trajectory_type === 'V_SHAPE' ? 'traj-badge-v' : (c.trajectory_type === 'W_SHAPE' ? 'traj-badge-w' : 'traj-badge-l');

      tr.innerHTML = `
        <td><span class="badge">${{c.case_id}}</span></td>
        <td style="font-weight: 600; color: var(--text-primary);">${{c.name}} (${{c.ticker}})</td>
        <td style="color: var(--text-secondary);">${{c.period}}</td>
        <td>${{c.peak_price.toLocaleString()}} / ${{c.trough_price.toLocaleString()}}</td>
        <td style="color: var(--danger); font-weight: 700;">${{c.mdd_pct.toFixed(2)}}%</td>
        <td>${{c.days_to_bottom_trade}} 일</td>
        <td><span class="badge ${{badgeClass}}">${{c.trajectory_type}}</span></td>
        <td style="color: var(--success);">+${{c.return_1m.toFixed(1)}}%</td>
        <td style="color: var(--success);">+${{c.return_3m.toFixed(1)}}%</td>
        <td style="color: var(--success); font-weight: 600;">+${{c.return_6m.toFixed(1)}}%</td>
        <td style="color: var(--success); font-weight: 700;">+${{c.return_12m.toFixed(1)}}%</td>
        <td style="font-size: 11px; max-width: 320px; white-space: normal; line-height: 1.4;">
          <strong>원인:</strong> ${{c.key_drivers}}<br>
          <strong style="color: var(--primary);">촉매:</strong> ${{c.recovery_catalyst}}
        </td>
      `;
      tbody.appendChild(tr);
    }});
  }}

  window.addEventListener('resize', renderAnalogsChart);
  window.addEventListener('DOMContentLoaded', () => {{
    renderAnalogsChart();
    renderTable();
  }});
  </script>
</body>
</html>
"""

with open(os.path.join(CHARTS_DIR, "historical_analogs_chart.html"), "w", encoding="utf-8") as f:
    f.write(analogs_html)
print("Saved charts/historical_analogs_chart.html")

# ---------------------------------------------------------------------------
# 5. Build charts/scenario_fan_chart.html
# ---------------------------------------------------------------------------
scenario_html = f"""<!DOCTYPE html>
<html lang="ko" data-theme="dark">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>SK Square 3x3 Scenario Fan Chart & 76-Share Position Roadmap | Standalone Chart</title>
  <style>
{COMMON_CSS}
    .gauge-container {{
      background: var(--bg-input);
      border-radius: var(--radius-md);
      padding: 20px;
      margin-top: 16px;
      border: 1px solid var(--border);
    }}
    .progress-track {{
      background: rgba(255, 255, 255, 0.08);
      height: 16px;
      border-radius: 8px;
      overflow: hidden;
      position: relative;
      margin: 12px 0;
    }}
    .progress-fill {{
      height: 100%;
      background: linear-gradient(90deg, #38bdf8, #10b981);
      border-radius: 8px;
      transition: width 0.5s ease;
    }}
    .trigger-item {{
      background: var(--bg-input);
      border: 1px solid var(--border);
      border-radius: var(--radius-md);
      padding: 14px 16px;
      margin-bottom: 10px;
      display: flex;
      justify-content: space-between;
      align-items: center;
      flex-wrap: wrap;
      gap: 12px;
    }}
    .trigger-info {{ flex: 1; min-width: 260px; }}
    .trigger-name {{ font-weight: 700; font-size: 14px; color: var(--text-primary); margin-bottom: 2px; }}
    .trigger-desc {{ font-size: 12px; color: var(--text-secondary); }}
  </style>
</head>
<body>
  <div class="container">
    <header class="chart-header">
      <div class="chart-title">
        <h1>🎯 SK Square 3x3 Scenario Fan Chart & 76-Share Roadmap</h1>
        <p>단기·중기·장기 확률 가중 시나리오 콘(Fan Chart) 및 투자자 76주 원금 100% 무위험 회수(TP1) 로드맵</p>
      </div>
      <div class="chart-actions">
        <span class="badge badge-primary">Zero-CDN Offline</span>
        <button class="btn" onclick="toggleTheme()">🌓 테마 전환</button>
        <a href="../dashboard.html" class="btn">📊 종합 대시보드</a>
      </div>
    </header>

    <div class="kpi-grid">
      <div class="kpi-card">
        <div class="kpi-label">보유 수량 및 평단가</div>
        <div class="kpi-value" style="color: var(--primary);">76 주 @ 109만 원</div>
        <div class="kpi-sub"><span class="badge badge-primary">원금 8,284만 원</span> 주당 109,000원 환산</div>
      </div>
      <div class="kpi-card">
        <div class="kpi-label">현재 평가액 (85.7만 원 기준)</div>
        <div class="kpi-value" style="color: var(--danger);">6,513.2 만 원</div>
        <div class="kpi-sub"><span class="badge badge-danger">수익률 -21.38%</span> 평가손실 -1,770.8만 원</div>
      </div>
      <div class="kpi-card">
        <div class="kpi-label">TP1 목표가 (원금 100% 회수선)</div>
        <div class="kpi-value" style="color: var(--success);">218.0 만 원</div>
        <div class="kpi-sub"><span class="badge badge-success">+100.0% 상승 목표</span> 38주 매도 시 8,284만 원 회수</div>
      </div>
      <div class="kpi-card">
        <div class="kpi-label">장기 기대값 (EV 6~12M)</div>
        <div class="kpi-value" style="color: var(--primary);">149.9 만 원</div>
        <div class="kpi-sub"><span class="badge badge-primary">+74.9% 기대수익</span> Bull 2.18M / Base 1.32M</div>
      </div>
      <div class="kpi-card">
        <div class="kpi-label">TP1 후 무위험 잔여 포지션</div>
        <div class="kpi-value" style="color: var(--success);">38 주 (Free-Carry)</div>
        <div class="kpi-sub"><span class="badge badge-success">투자원금 0원 상태</span> 잔여가치 8,284만 원 전액 이익</div>
      </div>
    </div>

    <!-- Multi-Horizon Fan Chart Canvas -->
    <div class="chart-panel">
      <div class="chart-panel-header">
        <div class="chart-panel-title">
          <span>📈 3대 구간별 시나리오 콘(Fan Chart) & 기대값 궤적</span>
          <span class="badge badge-primary">Bull / Base / Bear Bands</span>
        </div>
      </div>

      <div class="canvas-container" style="height: 440px;" id="fan-box">
        <canvas id="fan-canvas"></canvas>
      </div>

      <div class="tooltip" id="fan-tooltip"></div>
    </div>

    <!-- 76-Share Position Diagnostic & TP1 Progress Gauge -->
    <div class="simulator-card">
      <div class="chart-panel-title">
        <span>💼 투자자 76주 포지션 진단 및 1~2년 TP1 100% 무위험 회수 게이지</span>
        <span class="badge badge-success">Capital Protection Protocol</span>
      </div>

      <div class="gauge-container">
        <div style="display: flex; justify-content: space-between; align-items: center;">
          <span style="font-weight: 700; font-size: 15px;">TP1 (218만 원 도달 시 38주 매도 원금 100% 회수) 진행률</span>
          <span style="font-family: var(--font-mono); font-weight: 700; color: var(--primary); font-size: 16px;" id="tp1-progress-text">39.3% 달성</span>
        </div>
        <div class="progress-track">
          <div class="progress-fill" id="tp1-progress-bar" style="width: 39.3%;"></div>
        </div>
        <div style="display: flex; justify-content: space-between; font-size: 12px; color: var(--text-secondary);">
          <span>현재가: 85.7만 원 (평가액 6,513만 원)</span>
          <span>본전(평단): 109.0만 원 (원금 8,284만 원)</span>
          <span style="color: var(--success); font-weight: 700;">TP1: 218.0만 원 (38주 매도 = 8,284만 원 원금 전액 회수)</span>
        </div>
      </div>

      <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(260px, 1fr)); gap: 16px; margin-top: 20px;">
        <div style="background: var(--bg-input); padding: 16px; border-radius: var(--radius-md); border: 1px solid var(--border);">
          <div class="kpi-label">단계 1: 원금 100% 회수 (Risk-Free 전환)</div>
          <p style="font-size: 13px; color: var(--text-secondary); margin-top: 6px; line-height: 1.5;">
            주가가 218만 원(주당 218,000원)에 도달할 때, <strong>보유 76주 중 정확히 절반인 38주를 매도</strong>합니다. 회수 금액은 <strong>8,284만 원</strong>으로 최초 투입 원금의 100.0%를 계좌로 온전히 현금 회수합니다.
          </p>
        </div>
        <div style="background: var(--bg-input); padding: 16px; border-radius: var(--radius-md); border: 1px solid var(--border);">
          <div class="kpi-label">단계 2: 잔여 38주 무위험 보유 (Free Carry)</div>
          <p style="font-size: 13px; color: var(--text-secondary); margin-top: 6px; line-height: 1.5;">
            원금 회수 후 잔여 38주는 <strong>순투자원금이 0원인 '공짜 주식(Risk-Free Carry)'</strong> 상태가 됩니다. 향후 솔리다임 IPO 및 하이닉스 사이클 고점(TP2 300만~400만 원)까지 어떠한 시장 급락에도 심리적 흔들림 없이 편안하게 보유할 수 있습니다.
          </p>
        </div>
        <div style="background: var(--bg-input); padding: 16px; border-radius: var(--radius-md); border: 1px solid var(--border);">
          <div class="kpi-label">단계 3: 자금 정체(Dead Money) 회피</div>
          <p style="font-size: 13px; color: var(--text-secondary); margin-top: 6px; line-height: 1.5;">
            막연한 물타기 대신, 8대 객관적 트리거(외인 선물 1.5만 계약, 베이시스 콘탱고, 대차잔고 -5% 감소)가 충족되기 전까지는 불필요한 현금 소진을 금지하고 최적의 반등 타이밍을 엄격히 포착합니다.
          </p>
        </div>
      </div>
    </div>

    <!-- 3x3 Scenario Matrix Table -->
    <div class="chart-panel">
      <div class="chart-panel-title">
        <span>📊 3x3 Bull / Base / Bear 주가 시나리오 매트릭스 상세</span>
      </div>
      <div class="table-wrapper">
        <table class="custom-table" id="scenario-table">
          <thead>
            <tr>
              <th>시계열 구간</th>
              <th>시나리오</th>
              <th>확률 (%)</th>
              <th>SK하이닉스 타겟가</th>
              <th>목표 NAV 할인율</th>
              <th>SK스퀘어 타겟가 (주당)</th>
              <th>단위가 (KRW)</th>
              <th>기대 수익률</th>
              <th>핵심 촉매 및 발생 시나리오</th>
            </tr>
          </thead>
          <tbody>
            <!-- Populated via JS -->
          </tbody>
        </table>
      </div>
    </div>

    <!-- 8-Point Trigger Checklist Cockpit -->
    <div class="chart-panel">
      <div class="chart-panel-title">
        <span>🚦 실전 대응 8대 객관적 트리거 체크리스트 (Objective Trigger Checklist)</span>
        <span class="badge badge-danger" id="trigger-overall-badge">현재 레짐: BEARISH_STRESS (0/8)</span>
      </div>
      <p style="font-size: 13px; color: var(--text-secondary); margin-top: 4px; margin-bottom: 16px;">
        매일 장 마감 후 8개 선행·동행 지표를 객관적으로 판별하여 감정을 배제한 기계적 투자 행동을 실행합니다.
      </p>

      <div id="trigger-list-container">
        <!-- Populated via JS -->
      </div>
    </div>
  </div>

  <script>
{COMMON_JS_HEADER}

  const scenarioData = {scenario_json};
  const horizons = scenarioData.horizons;
  const triggers = scenarioData.trigger_checklist;

  function setupCanvas(canvasId, containerId) {{
    const canvas = document.getElementById(canvasId);
    const container = document.getElementById(containerId);
    const dpr = window.devicePixelRatio || 1;
    const rect = container.getBoundingClientRect();
    canvas.width = rect.width * dpr;
    canvas.height = rect.height * dpr;
    const ctx = canvas.getContext('2d');
    ctx.scale(dpr, dpr);
    return {{ canvas, ctx, width: rect.width, height: rect.height }};
  }}

  function renderFanChart() {{
    const {{ canvas, ctx, width, height }} = setupCanvas('fan-canvas', 'fan-box');
    const pad = {{ top: 30, right: 90, bottom: 40, left: 30 }};
    const cWidth = width - pad.left - pad.right;
    const cHeight = height - pad.top - pad.bottom;

    // Nodes: 0: Current, 1: Short (1~4W), 2: Mid (1~3M), 3: Long (6~12M)
    const nodes = [
      {{ label: '현재 (2026-10-13)', bull: 857000, base: 857000, bear: 857000, ev: 857000 }},
      {{ label: '단기 (1~4주)', bull: horizons.short_term_1_4w.bull.square_target_unit_krw, base: horizons.short_term_1_4w.base.square_target_unit_krw, bear: horizons.short_term_1_4w.bear.square_target_unit_krw, ev: horizons.short_term_1_4w.expected_value_unit_krw }},
      {{ label: '중기 (1~3개월)', bull: horizons.mid_term_1_3m.bull.square_target_unit_krw, base: horizons.mid_term_1_3m.base.square_target_unit_krw, bear: horizons.mid_term_1_3m.bear.square_target_unit_krw, ev: horizons.mid_term_1_3m.expected_value_unit_krw }},
      {{ label: '장기 (6~12개월)', bull: horizons.long_term_6_12m.bull.square_target_unit_krw, base: horizons.long_term_6_12m.base.square_target_unit_krw, bear: horizons.long_term_6_12m.bear.square_target_unit_krw, ev: horizons.long_term_6_12m.expected_value_unit_krw }},
    ];

    const minPrice = 600000, maxPrice = 2400000;
    const getX = i => pad.left + (i / (nodes.length - 1)) * cWidth;
    const getY = p => pad.top + cHeight - ((p - minPrice) / (maxPrice - minPrice)) * cHeight;

    // Breakeven reference line (1,090,000 KRW)
    const yCost = getY(1090000);
    ctx.strokeStyle = '#f59e0b';
    ctx.lineWidth = 1.5;
    ctx.setLineDash([5, 5]);
    ctx.beginPath();
    ctx.moveTo(pad.left, yCost);
    ctx.lineTo(pad.left + cWidth, yCost);
    ctx.stroke();
    ctx.fillStyle = '#f59e0b';
    ctx.font = '11px sans-serif';
    ctx.fillText('본전 평단가: 109만 원', pad.left + cWidth + 6, yCost + 4);

    // TP1 100% Recovery reference line (2,180,000 KRW)
    const yTp1 = getY(2180000);
    ctx.strokeStyle = '#10b981';
    ctx.lineWidth = 2.0;
    ctx.setLineDash([4, 4]);
    ctx.beginPath();
    ctx.moveTo(pad.left, yTp1);
    ctx.lineTo(pad.left + cWidth, yTp1);
    ctx.stroke();
    ctx.fillStyle = '#10b981';
    ctx.font = '11px sans-serif';
    ctx.fillText('TP1 목표선: 218만 원 (원금 100% 회수)', pad.left + cWidth + 6, yTp1 + 4);
    ctx.setLineDash([]);

    // Gridlines & Ticks
    ctx.strokeStyle = '#233554';
    ctx.lineWidth = 1;
    [800000, 1000000, 1200000, 1400000, 1600000, 1800000, 2000000, 2200000].forEach(p => {{
      const y = getY(p);
      ctx.beginPath();
      ctx.moveTo(pad.left, y);
      ctx.lineTo(pad.left + cWidth, y);
      ctx.stroke();
      ctx.fillStyle = '#94a3b8';
      ctx.fillText((p / 10000).toLocaleString() + '만', pad.left + cWidth + 6, y + 4);
    }});

    // Fan Shading: Bear to Base (Red tint)
    ctx.beginPath();
    ctx.moveTo(getX(0), getY(nodes[0].bear));
    for (let i = 1; i < nodes.length; i++) ctx.lineTo(getX(i), getY(nodes[i].bear));
    for (let i = nodes.length - 1; i >= 0; i--) ctx.lineTo(getX(i), getY(nodes[i].base));
    ctx.closePath();
    ctx.fillStyle = 'rgba(244, 63, 94, 0.12)';
    ctx.fill();

    // Fan Shading: Base to Bull (Green tint)
    ctx.beginPath();
    ctx.moveTo(getX(0), getY(nodes[0].base));
    for (let i = 1; i < nodes.length; i++) ctx.lineTo(getX(i), getY(nodes[i].bull));
    for (let i = nodes.length - 1; i >= 0; i--) ctx.lineTo(getX(i), getY(nodes[i].base));
    ctx.closePath();
    ctx.fillStyle = 'rgba(16, 185, 129, 0.15)';
    ctx.fill();

    // Boundary Lines: Bull (Green)
    ctx.beginPath();
    ctx.strokeStyle = '#10b981';
    ctx.lineWidth = 2.5;
    nodes.forEach((n, i) => {{
      const x = getX(i), y = getY(n.bull);
      if (i === 0) ctx.moveTo(x, y); else ctx.lineTo(x, y);
    }});
    ctx.stroke();

    // Boundary Lines: Bear (Red)
    ctx.beginPath();
    ctx.strokeStyle = '#f43f5e';
    ctx.lineWidth = 2.0;
    nodes.forEach((n, i) => {{
      const x = getX(i), y = getY(n.bear);
      if (i === 0) ctx.moveTo(x, y); else ctx.lineTo(x, y);
    }});
    ctx.stroke();

    // Base Line (Indigo)
    ctx.beginPath();
    ctx.strokeStyle = '#818cf8';
    ctx.lineWidth = 2.0;
    nodes.forEach((n, i) => {{
      const x = getX(i), y = getY(n.base);
      if (i === 0) ctx.moveTo(x, y); else ctx.lineTo(x, y);
    }});
    ctx.stroke();

    // Expected Value Trajectory (Cyan with Circles)
    ctx.beginPath();
    ctx.strokeStyle = '#38bdf8';
    ctx.lineWidth = 3.0;
    nodes.forEach((n, i) => {{
      const x = getX(i), y = getY(n.ev);
      if (i === 0) ctx.moveTo(x, y); else ctx.lineTo(x, y);
    }});
    ctx.stroke();

    // Draw node dots
    nodes.forEach((n, i) => {{
      const x = getX(i);
      // EV Dot
      ctx.beginPath();
      ctx.arc(x, getY(n.ev), 6, 0, Math.PI * 2);
      ctx.fillStyle = '#38bdf8';
      ctx.fill();
      ctx.strokeStyle = '#fff';
      ctx.lineWidth = 2;
      ctx.stroke();

      // Node label
      ctx.fillStyle = '#f8fafc';
      ctx.font = '12px sans-serif';
      ctx.textAlign = 'center';
      ctx.fillText(n.label, x, pad.top + cHeight + 24);

      // EV Value text
      ctx.fillStyle = '#38bdf8';
      ctx.font = 'bold 12px monospace';
      ctx.fillText((n.ev / 10000).toLocaleString() + '만', x, getY(n.ev) - 12);
    }});
    ctx.textAlign = 'left';
  }}

  function renderScenarioTable() {{
    const tbody = document.querySelector('#scenario-table tbody');
    tbody.innerHTML = '';

    const list = [
      {{ hName: '단기 (1~4주 / 실적 발표)', data: horizons.short_term_1_4w }},
      {{ hName: '중기 (1~3개월 / 연말 배당·랠리)', data: horizons.mid_term_1_3m }},
      {{ hName: '장기 (6~12개월 / HBM4·솔리다임 IPO)', data: horizons.long_term_6_12m }},
    ];

    list.forEach(item => {{
      ['bull', 'base', 'bear'].forEach(sKey => {{
        const s = item.data[sKey];
        const tr = document.createElement('tr');
        const sColor = sKey === 'bull' ? 'var(--success)' : (sKey === 'base' ? 'var(--primary)' : 'var(--danger)');
        const sLabel = sKey === 'bull' ? '강세 (Bull)' : (sKey === 'base' ? '기본 (Base)' : '약세 (Bear)');

        tr.innerHTML = `
          <td style="font-weight: 600;">${{item.hName}}</td>
          <td><span class="badge" style="color: ${{sColor}}; border-color: ${{sColor}};">${{sLabel}}</span></td>
          <td style="font-family: var(--font-mono); font-weight: 700;">${{s.probability_pct}}%</td>
          <td>${{s.hynix_target_krw.toLocaleString()}} 원</td>
          <td style="color: var(--warning);">${{s.target_discount_pct.toFixed(1)}}%</td>
          <td style="font-weight: 700;">${{s.square_target_share_krw.toLocaleString()}} 원</td>
          <td style="font-weight: 800; color: ${{sColor}};">${{s.square_target_unit_krw.toLocaleString()}} 원</td>
          <td style="font-weight: 700; color: ${{s.expected_return_pct >= 0 ? 'var(--success)' : 'var(--danger)'}};">
            ${{s.expected_return_pct >= 0 ? '+' : ''}}${{s.expected_return_pct.toFixed(2)}}%
          </td>
          <td style="font-size: 11px; max-width: 300px; white-space: normal; line-height: 1.4;">
            ${{s.catalyst}}
          </td>
        `;
        tbody.appendChild(tr);
      }});
    }});
  }}

  function renderTriggerChecklist() {{
    const container = document.getElementById('trigger-list-container');
    container.innerHTML = '';

    triggers.forEach(t => {{
      const div = document.createElement('div');
      div.className = 'trigger-item';

      let regimeBadge = 'badge-danger';
      if (t.regime.includes('BULLISH')) regimeBadge = 'badge-success';
      else if (t.regime.includes('NEUTRAL') || t.regime.includes('DEEP_VALUE') || t.regime.includes('PENDING')) regimeBadge = 'badge-warning';

      div.innerHTML = `
        <div class="trigger-info">
          <div class="trigger-name">
            <span class="badge badge-primary" style="margin-right: 6px;">${{t.trigger_id}}</span>
            ${{t.name}}
          </div>
          <div class="trigger-desc">
            <strong>발동 기준:</strong> ${{t.condition}} &nbsp;|&nbsp;
            <strong>행동 지침:</strong> ${{t.action_guideline}}
          </div>
        </div>
        <div style="display: flex; align-items: center; gap: 12px;">
          <div style="text-align: right;">
            <div style="font-size: 12px; color: var(--text-secondary);">현재 상태</div>
            <div style="font-size: 13px; font-weight: 700; color: var(--text-primary);">${{t.current_status}}</div>
          </div>
          <span class="badge ${{regimeBadge}}">${{t.regime}}</span>
        </div>
      `;
      container.appendChild(div);
    }});
  }}

  window.addEventListener('resize', renderFanChart);
  window.addEventListener('DOMContentLoaded', () => {{
    renderFanChart();
    renderScenarioTable();
    renderTriggerChecklist();
  }});
  </script>
</body>
</html>
"""

with open(os.path.join(CHARTS_DIR, "scenario_fan_chart.html"), "w", encoding="utf-8") as f:
    f.write(scenario_html)
print("Saved charts/scenario_fan_chart.html")

# ---------------------------------------------------------------------------
# 6. Build dashboard.html (The Master Executive Visual Dashboard)
# ---------------------------------------------------------------------------
dashboard_html = f"""<!DOCTYPE html>
<html lang="ko" data-theme="dark">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>SK Square (402340) & SK Hynix (000660) Forecast Engine | Executive Visual Dashboard</title>
  <style>
{COMMON_CSS}
    /* Dashboard Specific Styles */
    .nav-tabs {{
      display: flex;
      overflow-x: auto;
      gap: 8px;
      border-bottom: 2px solid var(--border);
      margin-bottom: 24px;
      padding-bottom: 2px;
    }}
    .nav-tab-btn {{
      padding: 10px 18px;
      font-size: 14px;
      font-weight: 700;
      color: var(--text-secondary);
      background: transparent;
      border: none;
      border-bottom: 3px solid transparent;
      cursor: pointer;
      display: inline-flex;
      align-items: center;
      gap: 8px;
      white-space: nowrap;
      transition: var(--transition);
    }}
    .nav-tab-btn:hover {{
      color: var(--primary);
    }}
    .nav-tab-btn.active {{
      color: var(--primary);
      border-bottom-color: var(--primary);
    }}
    .tab-content-panel {{
      display: none;
      animation: fadeIn 0.3s ease;
    }}
    .tab-content-panel.active {{
      display: block;
    }}
    @keyframes fadeIn {{
      from {{ opacity: 0; transform: translateY(6px); }}
      to {{ opacity: 1; transform: translateY(0); }}
    }}
    .metric-grid-2 {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
      gap: 20px;
      margin-bottom: 24px;
    }}
    .progress-track {{
      background: rgba(255, 255, 255, 0.08);
      height: 14px;
      border-radius: 7px;
      overflow: hidden;
      margin: 10px 0;
    }}
    .progress-fill {{
      height: 100%;
      background: linear-gradient(90deg, #38bdf8, #10b981);
      border-radius: 7px;
    }}
    .standalone-link-card {{
      background: linear-gradient(135deg, rgba(56, 189, 248, 0.1), rgba(99, 102, 241, 0.1));
      border: 1px solid var(--border-focus);
      border-radius: var(--radius-md);
      padding: 16px 20px;
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-top: 24px;
    }}
  </style>
</head>
<body>
  <div class="container">
    <!-- Executive Top Header -->
    <header class="chart-header">
      <div class="chart-title">
        <h1>🏛️ SK Square (402340) & SK Hynix (000660) Forecast Engine</h1>
        <p>전방위 6대 영역 정량 데이터 분석, 파생 메커니즘, 주도주 유사사례 및 투자자 76주 종합 대시보드</p>
      </div>
      <div class="chart-actions">
        <span class="badge badge-primary">100% Zero-CDN Offline</span>
        <span class="badge badge-success">기준일 2026-10-13</span>
        <button class="btn" onclick="toggleTheme()">🌓 테마 전환</button>
      </div>
    </header>

    <!-- Executive KPI Ribbon (6 Core Cards) -->
    <div class="kpi-grid">
      <div class="kpi-card">
        <div class="kpi-label">SK스퀘어 현재가 (주당/단위)</div>
        <div class="kpi-value" id="kpi-price">85,700 원</div>
        <div class="kpi-sub"><span class="badge badge-warning">단위환산 85.7만 원</span> 52주고점(14.9만) 대비 -42.5%</div>
      </div>
      <div class="kpi-card">
        <div class="kpi-label">주당 순자산가치 (NAV)</div>
        <div class="kpi-value" style="color: var(--primary);">238,160 원</div>
        <div class="kpi-sub"><span class="badge badge-primary">총 NAV 32.08조 원</span> 소각후 244,958원 (+3.4%)</div>
      </div>
      <div class="kpi-card">
        <div class="kpi-label">NAV 할인율 (Discount)</div>
        <div class="kpi-value" style="color: var(--danger);">64.02%</div>
        <div class="kpi-sub"><span class="badge badge-danger">역사적 극단 저평가</span> 정상 밴드 45~55% 괴리</div>
      </div>
      <div class="kpi-card">
        <div class="kpi-label">비대칭 하방 베타 비율</div>
        <div class="kpi-value" style="color: var(--warning);">1.63x</div>
        <div class="kpi-sub"><span class="badge badge-warning">하방 민감도 1.84x</span> 20일 롤링 베타 2.39x</div>
      </div>
      <div class="kpi-card">
        <div class="kpi-label">외국인 지분율 (스퀘어/하이닉스)</div>
        <div class="kpi-value">45.3% / 48.2%</div>
        <div class="kpi-sub"><span class="badge badge-danger">-1.32σ 침체</span> 하이닉스 -1σ 바닥(51.3%) 하회</div>
      </div>
      <div class="kpi-card">
        <div class="kpi-label">투자자 76주 포지션 평가</div>
        <div class="kpi-value" style="color: var(--danger);">6,513.2 만 원</div>
        <div class="kpi-sub"><span class="badge badge-danger">수익률 -21.38%</span> 원금 8,284만 / 본전갭 1,770만</div>
      </div>
    </div>

    <!-- Navigation Tabs (6 Domains) -->
    <div class="nav-tabs">
      <button class="nav-tab-btn active" onclick="switchTab('tab-nav')">🏛️ 1. NAV & 할인율 채널</button>
      <button class="nav-tab-btn" onclick="switchTab('tab-tech')">📈 2. 기술적 지표 & 매물대</button>
      <button class="nav-tab-btn" onclick="switchTab('tab-supply')">🌊 3. 수급 & 파생 메커니즘</button>
      <button class="nav-tab-btn" onclick="switchTab('tab-short')">⚠️ 4. 공매도 & 반대매매 위험선</button>
      <button class="nav-tab-btn" onclick="switchTab('tab-analogs')">📜 5. 6대 주도주 유사사례</button>
      <button class="nav-tab-btn" onclick="switchTab('tab-scenario')">🎯 6. 3x3 시나리오 & 76주 로드맵</button>
    </div>

    <!-- TAB 1: NAV & Valuation Discount Channels -->
    <div class="tab-content-panel active" id="tab-nav">
      <div class="chart-panel">
        <div class="chart-panel-header">
          <div class="chart-panel-title">
            <span>주가 및 주당 NAV(순자산가치) 260거래일 시계열 추이 (KRW)</span>
          </div>
          <a href="charts/nav_discount_chart.html" class="btn btn-primary" target="_blank">🔍 단독 전용 차트 열기</a>
        </div>
        <div class="canvas-container" style="height: 340px;" id="dash-nav-box">
          <canvas id="dash-nav-canvas"></canvas>
        </div>
      </div>

      <div class="metric-grid-2">
        <div class="kpi-card">
          <div class="chart-panel-title" style="margin-bottom: 12px;">
            <span>💎 40조 자사주 소각(2,407만 주) 액크리션</span>
            <span class="badge badge-success">+3.42% EPS/BPS Uplift</span>
          </div>
          <p style="font-size: 13px; color: var(--text-secondary); line-height: 1.6;">
            SK하이닉스 발행주식수가 728.0M주에서 703.9M주로 감소함에 따라 SK스퀘어의 보유 지분율이 <strong>20.07%에서 20.76%로 자동 상향</strong>됩니다. 이에 따라 스퀘어의 주당 NAV는 <strong>+6,798원 영구 상향(238,160원 → 244,958원)</strong>되는 재무적 가치 증대 효과를 발생시킵니다.
          </p>
        </div>

        <div class="kpi-card">
          <div class="chart-panel-title" style="margin-bottom: 12px;">
            <span>📦 비상장 자산 & 솔리다임 가치 재평가</span>
            <span class="badge badge-primary">총 5.3조 원 안전마진</span>
          </div>
          <p style="font-size: 13px; color: var(--text-secondary); line-height: 1.6;">
            지주사 순현금 +8,000억 원과 솔리다임, 티맵모빌리티, 11번가 등 <strong>비상장 자산 4.5조 원이 하방 지지선</strong>을 형성합니다. 마이크론 AI eSSD 분기 $10B 돌파에 발맞추어 솔리다임 나스닥 IPO($100B~$150B) 추진 시 스퀘어 주당 NAV는 추가 2만~3만 원 리레이팅 잠재력을 갖춥니다.
          </p>
        </div>
      </div>
    </div>

    <!-- TAB 2: Technical & Volume Profile -->
    <div class="tab-content-panel" id="tab-tech">
      <div class="chart-panel">
        <div class="chart-panel-header">
          <div class="chart-panel-title">
            <span>이동평균선(20/60/120/200 MA) 및 볼린저 밴드(20, 2) 추세</span>
          </div>
          <div style="font-size: 12px; color: var(--text-secondary);">
            200일선 이격도: <strong style="color: var(--danger);">-7.45%</strong> | RSI(14): <strong style="color: var(--primary);">77.67</strong>
          </div>
        </div>
        <div class="canvas-container" style="height: 320px;" id="dash-tech-box">
          <canvas id="dash-tech-canvas"></canvas>
        </div>
      </div>

      <div class="metric-grid-2">
        <div class="kpi-card">
          <div class="chart-panel-title" style="margin-bottom: 10px;">
            <span>📊 50-bin 매물대(Volume Profile) 핵심 레벨</span>
          </div>
          <table class="custom-table">
            <tr><th>지표</th><th>가격 (KRW)</th><th>의미</th></tr>
            <tr><td>최대 매물대 (POC)</td><td style="color: var(--primary); font-weight: 700;">118,281 원</td><td>대규모 기관·외인 매물 집중 저항대</td></tr>
            <tr><td>매물대 상단 (VAH)</td><td>118,900 원</td><td>상방 돌파 시 가속 구간</td></tr>
            <tr><td>매물대 하단 (VAL)</td><td style="color: var(--success); font-weight: 700;">81,760 원</td><td>1차 강력 하방 지지선 (최근 저점 방어선)</td></tr>
          </table>
        </div>

        <div class="kpi-card">
          <div class="chart-panel-title" style="margin-bottom: 10px;">
            <span>📐 사이클 피보나치 되돌림 (Fibonacci Retracement)</span>
          </div>
          <table class="custom-table">
            <tr><th>비율</th><th>가격 (KRW)</th><th>비고</th></tr>
            <tr><td>0.0% (사이클 저점)</td><td>57,000 원</td><td>2024년 연초 바닥</td></tr>
            <tr><td>23.6% 되돌림</td><td>71,608 원</td><td>패닉 셀링 극단 지지선</td></tr>
            <tr><td>38.2% 되돌림</td><td style="color: var(--warning); font-weight: 700;">80,646 원</td><td>현재가(85,700원) 직전 지지대</td></tr>
            <tr><td>50.0% 중심선</td><td style="color: var(--primary); font-weight: 700;">87,950 원</td><td>단기 1차 회복 목표선 (목전)</td></tr>
            <tr><td>61.8% 골든선</td><td>95,254 원</td><td>중기 추세 반전 확정선</td></tr>
          </table>
        </div>
      </div>
    </div>

    <!-- TAB 3: Supply, Demand & Derivatives -->
    <div class="tab-content-panel" id="tab-supply">
      <div class="chart-panel">
        <div class="chart-panel-header">
          <div class="chart-panel-title">
            <span>4대 주체별(외국인·기관·개인·기타법인) 20일 누적 순매수 및 베이시스</span>
          </div>
          <a href="charts/beta_spread_chart.html" class="btn btn-primary" target="_blank">⚡ 베타 & 파생 전용 차트 열기</a>
        </div>
        <div class="canvas-container" style="height: 320px;" id="dash-sup-box">
          <canvas id="dash-sup-canvas"></canvas>
        </div>
      </div>

      <div class="metric-grid-2">
        <div class="kpi-card">
          <div class="chart-panel-title" style="margin-bottom: 10px;">
            <span>🌍 외국인 지분율 Z-Score 및 -1σ 바닥 분석</span>
          </div>
          <p style="font-size: 13px; color: var(--text-secondary); line-height: 1.6;">
            현재 SK하이닉스 외인 지분율은 <strong>48.15%로 250일 평균(53.22%) 대비 -2.60σ, -1σ 바닥(51.27%)을 크게 하회</strong>하는 극단 과매도 영역에 있습니다. SK스퀘어 외인 지분율 역시 <strong>45.3%(-1.32σ)</strong>로 자사주 매입 종료 후 수급 공백(위험지수 85점)이 지속되고 있으나, 과거 패턴 상 -1σ~-2σ 구간은 외인 귀환 시 강력한 숏스퀴즈 반등이 출현했던 변곡점입니다.
          </p>
        </div>

        <div class="kpi-card">
          <div class="chart-panel-title" style="margin-bottom: 10px;">
            <span>📉 파생시장 베이시스와 비대칭 하방 베타(1.63x)</span>
          </div>
          <p style="font-size: 13px; color: var(--text-secondary); line-height: 1.6;">
            코스피200 선·현물 베이시스가 <strong>-0.85pt(백워데이션)</strong>를 유지하고 외인 선물이 3일간 -7,878계약 순매도됨에 따라 금융투자 프로그램 차익 매도가 지속 출회되고 있습니다. 이로 인해 스퀘어는 하이닉스 하락 시 <strong>하방 베타 1.84~2.39x</strong>로 하락폭이 증폭되는 비대칭성을 보였습니다.
          </p>
        </div>
      </div>
    </div>

    <!-- TAB 4: Short Selling & Margin Call Danger Zones -->
    <div class="tab-content-panel" id="tab-short">
      <div class="kpi-grid">
        <div class="kpi-card">
          <div class="kpi-label">SK스퀘어 공매도 거래비중</div>
          <div class="kpi-value" style="color: var(--warning);">7.91%</div>
          <div class="kpi-sub">일간 거래량 38,500 주</div>
        </div>
        <div class="kpi-card">
          <div class="kpi-label">SK스퀘어 대차잔고</div>
          <div class="kpi-value" style="color: var(--primary);">512 만 주</div>
          <div class="kpi-sub">순보유잔고 122.8만 주</div>
        </div>
        <div class="kpi-card">
          <div class="kpi-label">SK하이닉스 대차잔고 / DTC</div>
          <div class="kpi-value" style="color: var(--primary);">3,145 만 주 / 2.25일</div>
          <div class="kpi-sub">5일 증감률 +12.9% (공매도 누증)</div>
        </div>
        <div class="kpi-card">
          <div class="kpi-label">신용융자 140% 반대매매 위험선 1</div>
          <div class="kpi-value" style="color: var(--danger);">78,501 원</div>
          <div class="kpi-sub"><span class="badge badge-danger">1차 청산 트리거</span> 현재가 대비 -8.4%</div>
        </div>
        <div class="kpi-card">
          <div class="kpi-label">신용융자 140% 반대매매 위험선 2</div>
          <div class="kpi-value" style="color: var(--danger);">71,988 원</div>
          <div class="kpi-sub"><span class="badge badge-danger">2차 투매 클라이맥스</span> 청산 대기 16.5만 주</div>
        </div>
      </div>

      <div class="chart-panel">
        <div class="chart-panel-title" style="margin-bottom: 12px;">
          <span>🚨 신용융자 140% 담보유지비율 반대매매(Margin Call) 위험 구간 분석</span>
        </div>
        <p style="font-size: 13px; color: var(--text-secondary); line-height: 1.6;">
          SK스퀘어 신용잔고는 75만 주(신용비율 0.56%) 수준이며, 최근 1~2개월 고점(11만~13만 원)에서 매수된 개인 신용물량의 <strong>1차 반대매매 위험 가격은 78,501원</strong>, <strong>2차 집단 반대매매 가격은 71,988원</strong>으로 산출됩니다. 주가가 80,000원 선을 이탈할 경우 약 <strong>165,000주의 반대매매 청산 매물</strong>이 시초가 동시호가에 쏟아지며 단기 언더슈팅을 유발할 수 있으나, 이는 과거 사이클 상 항상 <strong>수급 워시아웃(Wash-out)의 최종 바닥</strong>으로 작용했습니다.
        </p>
      </div>
    </div>

    <!-- TAB 5: 6 Historical Analog Benchmarks -->
    <div class="tab-content-panel" id="tab-analogs">
      <div class="chart-panel">
        <div class="chart-panel-header">
          <div class="chart-panel-title">
            <span>6대 주도주 50%+ 급락 후 복원 경로 오버레이 (-60D ~ +250D)</span>
          </div>
          <a href="charts/historical_analogs_chart.html" class="btn btn-primary" target="_blank">📜 유사사례 전용 차트 열기</a>
        </div>
        <div class="canvas-container" style="height: 360px;" id="dash-ana-box">
          <canvas id="dash-ana-canvas"></canvas>
        </div>
      </div>

      <div class="kpi-card" style="margin-bottom: 24px;">
        <div class="chart-panel-title" style="margin-bottom: 10px;">
          <span>🔍 SK스퀘어 현재 국면 진단: W자 이중바닥형(Hynix 2018 / MU 2018)에 가장 근접</span>
        </div>
        <p style="font-size: 13px; color: var(--text-secondary); line-height: 1.6;">
          사상 최대 실적(2024~2025 HBM 슈퍼사이클) 달성 후 클라우드 Capex 피크아웃 공포로 40~55% 조정을 거치는 메커니즘은 <strong>2018년 SK하이닉스 및 마이크론 국면과 92% 이상의 상관계수</strong>를 보입니다. 1차 저점(81,600원) 확인 후 10월 27일 실적 발표 전후로 2차 바닥을 다지는 <strong>W자형 복원 경로(부여 확률 60%)</strong>를 추종할 가능성이 가장 높습니다.
        </p>
      </div>
    </div>

    <!-- TAB 6: 3x3 Scenario Bands & Investor 76-Share Roadmap -->
    <div class="tab-content-panel" id="tab-scenario">
      <div class="chart-panel">
        <div class="chart-panel-header">
          <div class="chart-panel-title">
            <span>단기·중기·장기 확률 가중 시나리오 콘(Fan Chart) & 기대값 궤적</span>
          </div>
          <a href="charts/scenario_fan_chart.html" class="btn btn-primary" target="_blank">🎯 시나리오 & 76주 전용 차트 열기</a>
        </div>
        <div class="canvas-container" style="height: 360px;" id="dash-fan-box">
          <canvas id="dash-fan-canvas"></canvas>
        </div>
      </div>

      <!-- 76-Share Diagnostic Gauge -->
      <div class="simulator-card">
        <div class="chart-panel-title">
          <span>💼 투자자 76주 포지션: 1~2년 TP1 (218만 원) 100% 원금 무위험 회수 로드맵</span>
          <span class="badge badge-success">Capital Recovery Protocol</span>
        </div>

        <div style="background: var(--bg-input); padding: 18px; border-radius: var(--radius-md); border: 1px solid var(--border); margin-top: 14px;">
          <div style="display: flex; justify-content: space-between; font-size: 14px; font-weight: 700;">
            <span>TP1 원금 회수선(218만 원) 진행률</span>
            <span style="color: var(--primary); font-family: var(--font-mono);">39.3%</span>
          </div>
          <div class="progress-track">
            <div class="progress-fill" style="width: 39.3%;"></div>
          </div>
          <div style="display: flex; justify-content: space-between; font-size: 12px; color: var(--text-secondary);">
            <span>현재가: 85.7만 원 (평가액 6,513만 원 / 손실률 -21.38%)</span>
            <span>본전 평단: 109만 원 (매수원금 8,284만 원)</span>
            <span style="color: var(--success); font-weight: 700;">TP1 목표: 218만 원 (38주 매도 = 8,284만 원 100% 회수)</span>
          </div>
        </div>

        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(260px, 1fr)); gap: 16px; margin-top: 16px;">
          <div style="background: var(--bg-card); padding: 14px; border-radius: var(--radius-md); border: 1px solid var(--border);">
            <div class="kpi-label">단계 1: TP1 도달 (218만 원)</div>
            <p style="font-size: 12px; color: var(--text-secondary); margin-top: 4px;">
              보유 76주 중 38주를 매도하여 <strong>8,284만 원 현금을 회수</strong>함으로써 최초 투자원금을 100% 완전히 보전합니다.
            </p>
          </div>
          <div style="background: var(--bg-card); padding: 14px; border-radius: var(--radius-md); border: 1px solid var(--border);">
            <div class="kpi-label">단계 2: 잔여 38주 무위험 보유</div>
            <p style="font-size: 12px; color: var(--text-secondary); margin-top: 4px;">
              잔여 38주는 <strong>투자원금 0원인 Free-Carry 포지션</strong>으로 전환되어 솔리다임 IPO 및 차기 사이클 정점까지 무위험 복리를 누립니다.
            </p>
          </div>
          <div style="background: var(--bg-card); padding: 14px; border-radius: var(--radius-md); border: 1px solid var(--border);">
            <div class="kpi-label">단계 3: 8대 트리거 기계적 점검</div>
            <p style="font-size: 12px; color: var(--text-secondary); margin-top: 4px;">
              외인 선물 1.5만 계약 순매수 전환, 베이시스 콘탱고 복귀, 대차잔고 -5% 감소 신호 전까지는 감정적 뇌동매매를 철저히 차단합니다.
            </p>
          </div>
        </div>
      </div>
    </div>

    <!-- Standalone Chart Quick Launch Bar -->
    <div class="standalone-link-card">
      <div>
        <div style="font-weight: 700; font-size: 15px; color: var(--text-primary); margin-bottom: 2px;">
          📊 4대 독립 실행형 고해상도 인터랙티브 차트 모음 (Standalone Charts)
        </div>
        <div style="font-size: 12px; color: var(--text-secondary);">
          외부 네트워크 없는 순수 100% 로컬 파일환경(file:///)에서 자유롭게 브라우저 단독 탭으로 열람할 수 있습니다.
        </div>
      </div>
      <div style="display: flex; gap: 10px; flex-wrap: wrap;">
        <a href="charts/nav_discount_chart.html" class="btn" target="_blank">🏛️ NAV 할인율</a>
        <a href="charts/beta_spread_chart.html" class="btn" target="_blank">⚡ 베타 & 스프레드</a>
        <a href="charts/historical_analogs_chart.html" class="btn" target="_blank">📜 유사사례 오버레이</a>
        <a href="charts/scenario_fan_chart.html" class="btn" target="_blank">🎯 시나리오 팬차트</a>
      </div>
    </div>
  </div>

  <script>
{COMMON_JS_HEADER}

  const rawData = {combined_json};
  const scenarioData = {scenario_json};
  const analogsData = {analogs_json};

  function switchTab(tabId) {{
    document.querySelectorAll('.nav-tab-btn').forEach(btn => btn.classList.remove('active'));
    document.querySelectorAll('.tab-content-panel').forEach(p => p.classList.remove('active'));

    if (event && event.target) event.target.classList.add('active');
    document.getElementById(tabId).classList.add('active');

    // Trigger canvas re-render on active tab
    setTimeout(() => {{
      if (tabId === 'tab-nav') renderDashNav();
      else if (tabId === 'tab-tech') renderDashTech();
      else if (tabId === 'tab-supply') renderDashSup();
      else if (tabId === 'tab-analogs') renderDashAna();
      else if (tabId === 'tab-scenario') renderDashFan();
    }}, 50);
  }}

  function setupCanvas(canvasId, containerId) {{
    const canvas = document.getElementById(canvasId);
    const container = document.getElementById(containerId);
    const dpr = window.devicePixelRatio || 1;
    const rect = container.getBoundingClientRect();
    canvas.width = rect.width * dpr;
    canvas.height = rect.height * dpr;
    const ctx = canvas.getContext('2d');
    ctx.scale(dpr, dpr);
    return {{ canvas, ctx, width: rect.width, height: rect.height }};
  }}

  function renderDashNav() {{
    const {{ canvas, ctx, width, height }} = setupCanvas('dash-nav-canvas', 'dash-nav-box');
    const pad = {{ top: 20, right: 60, bottom: 25, left: 20 }};
    const cWidth = width - pad.left - pad.right;
    const cHeight = height - pad.top - pad.bottom;

    const data = rawData;
    let minV = Infinity, maxV = -Infinity;
    data.forEach(d => {{
      minV = Math.min(minV, d.sq_close, d.nav_per_share);
      maxV = Math.max(maxV, d.sq_close, d.accreted_nav);
    }});
    minV = Math.floor(minV * 0.9 / 10000) * 10000;
    maxV = Math.ceil(maxV * 1.05 / 10000) * 10000;

    const getX = i => pad.left + (i / (data.length - 1)) * cWidth;
    const getY = v => pad.top + cHeight - ((v - minV) / (maxV - minV)) * cHeight;

    // Gridlines
    ctx.strokeStyle = '#233554';
    ctx.lineWidth = 1;
    ctx.setLineDash([4, 4]);
    [100000, 150000, 200000, 250000].forEach(v => {{
      if (v < minV || v > maxV) return;
      const y = getY(v);
      ctx.beginPath(); ctx.moveTo(pad.left, y); ctx.lineTo(pad.left + cWidth, y); ctx.stroke();
      ctx.fillStyle = '#94a3b8'; ctx.font = '10px sans-serif';
      ctx.fillText(v.toLocaleString(), pad.left + cWidth + 6, y + 4);
    }});
    ctx.setLineDash([]);

    // NAV Area Fill
    ctx.beginPath();
    ctx.moveTo(getX(0), getY(data[0].nav_per_share));
    for (let i = 1; i < data.length; i++) ctx.lineTo(getX(i), getY(data[i].nav_per_share));
    ctx.lineTo(getX(data.length - 1), pad.top + cHeight);
    ctx.lineTo(getX(0), pad.top + cHeight);
    ctx.closePath();
    ctx.fillStyle = 'rgba(56, 189, 248, 0.15)';
    ctx.fill();

    // NAV Line
    ctx.beginPath(); ctx.strokeStyle = '#38bdf8'; ctx.lineWidth = 2;
    data.forEach((d, i) => {{ const x = getX(i), y = getY(d.nav_per_share); if (i === 0) ctx.moveTo(x, y); else ctx.lineTo(x, y); }});
    ctx.stroke();

    // Accreted NAV Line
    ctx.beginPath(); ctx.strokeStyle = '#fbbf24'; ctx.setLineDash([4, 3]); ctx.lineWidth = 1.5;
    data.forEach((d, i) => {{ const x = getX(i), y = getY(d.accreted_nav); if (i === 0) ctx.moveTo(x, y); else ctx.lineTo(x, y); }});
    ctx.stroke();
    ctx.setLineDash([]);

    // Square Price Line
    ctx.beginPath(); ctx.strokeStyle = '#f43f5e'; ctx.lineWidth = 2.5;
    data.forEach((d, i) => {{ const x = getX(i), y = getY(d.sq_close); if (i === 0) ctx.moveTo(x, y); else ctx.lineTo(x, y); }});
    ctx.stroke();
  }}

  function renderDashTech() {{
    const {{ canvas, ctx, width, height }} = setupCanvas('dash-tech-canvas', 'dash-tech-box');
    const pad = {{ top: 15, right: 60, bottom: 25, left: 20 }};
    const cWidth = width - pad.left - pad.right;
    const cHeight = height - pad.top - pad.bottom;

    const data = rawData;
    let minV = 50000, maxV = 155000;
    const getX = i => pad.left + (i / (data.length - 1)) * cWidth;
    const getY = v => pad.top + cHeight - ((v - minV) / (maxV - minV)) * cHeight;

    // Gridlines
    ctx.strokeStyle = '#233554'; ctx.lineWidth = 1; ctx.setLineDash([4, 4]);
    [60000, 80000, 100000, 120000, 140000].forEach(v => {{
      const y = getY(v);
      ctx.beginPath(); ctx.moveTo(pad.left, y); ctx.lineTo(pad.left + cWidth, y); ctx.stroke();
      ctx.fillStyle = '#94a3b8'; ctx.font = '10px sans-serif';
      ctx.fillText(v.toLocaleString(), pad.left + cWidth + 6, y + 4);
    }});
    ctx.setLineDash([]);

    // 200MA Line (Gray)
    ctx.beginPath(); ctx.strokeStyle = '#64748b'; ctx.lineWidth = 2;
    data.forEach((d, i) => {{ const x = getX(i), y = getY(d.sq_sma200); if (i === 0) ctx.moveTo(x, y); else ctx.lineTo(x, y); }});
    ctx.stroke();

    // 60MA Line (Indigo)
    ctx.beginPath(); ctx.strokeStyle = '#818cf8'; ctx.lineWidth = 1.5;
    data.forEach((d, i) => {{ const x = getX(i), y = getY(d.sq_sma60); if (i === 0) ctx.moveTo(x, y); else ctx.lineTo(x, y); }});
    ctx.stroke();

    // 20MA Line (Cyan)
    ctx.beginPath(); ctx.strokeStyle = '#38bdf8'; ctx.lineWidth = 1.5;
    data.forEach((d, i) => {{ const x = getX(i), y = getY(d.sq_sma20); if (i === 0) ctx.moveTo(x, y); else ctx.lineTo(x, y); }});
    ctx.stroke();

    // Close Line (Red)
    ctx.beginPath(); ctx.strokeStyle = '#f43f5e'; ctx.lineWidth = 2.5;
    data.forEach((d, i) => {{ const x = getX(i), y = getY(d.sq_close); if (i === 0) ctx.moveTo(x, y); else ctx.lineTo(x, y); }});
    ctx.stroke();
  }}

  function renderDashSup() {{
    const {{ canvas, ctx, width, height }} = setupCanvas('dash-sup-canvas', 'dash-sup-box');
    const pad = {{ top: 15, right: 60, bottom: 25, left: 20 }};
    const cWidth = width - pad.left - pad.right;
    const cHeight = height - pad.top - pad.bottom;

    const data = rawData;
    let minV = -3000000, maxV = 2000000;
    const getX = i => pad.left + (i / (data.length - 1)) * cWidth;
    const getY = v => pad.top + cHeight - ((v - minV) / (maxV - minV)) * cHeight;

    // Zero line
    ctx.strokeStyle = '#64748b'; ctx.lineWidth = 1;
    ctx.beginPath(); ctx.moveTo(pad.left, getY(0)); ctx.lineTo(pad.left + cWidth, getY(0)); ctx.stroke();

    // Foreign cum 20D (Cyan)
    ctx.beginPath(); ctx.strokeStyle = '#38bdf8'; ctx.lineWidth = 2;
    data.forEach((d, i) => {{ const x = getX(i), y = getY(d.sq_cum_foreign_20d); if (i === 0) ctx.moveTo(x, y); else ctx.lineTo(x, y); }});
    ctx.stroke();

    // Retail cum 20D (Red)
    ctx.beginPath(); ctx.strokeStyle = '#f43f5e'; ctx.lineWidth = 2;
    data.forEach((d, i) => {{ const x = getX(i), y = getY(d.sq_cum_retail_20d); if (i === 0) ctx.moveTo(x, y); else ctx.lineTo(x, y); }});
    ctx.stroke();
  }}

  function renderDashAna() {{
    const {{ canvas, ctx, width, height }} = setupCanvas('dash-ana-canvas', 'dash-ana-box');
    const pad = {{ top: 20, right: 60, bottom: 30, left: 20 }};
    const cWidth = width - pad.left - pad.right;
    const cHeight = height - pad.top - pad.bottom;

    const minDay = -60, maxDay = 250;
    const minVal = 80, maxVal = 420;
    const getX = d => pad.left + ((d - minDay) / (maxDay - minDay)) * cWidth;
    const getY = v => pad.top + cHeight - ((v - minVal) / (maxVal - minVal)) * cHeight;

    // Baseline 100
    ctx.strokeStyle = '#38bdf8'; ctx.lineWidth = 1.5; ctx.setLineDash([4, 4]);
    ctx.beginPath(); ctx.moveTo(pad.left, getY(100)); ctx.lineTo(pad.left + cWidth, getY(100)); ctx.stroke();
    ctx.setLineDash([]);

    const colors = {{
      'ANALOG-01': '#38bdf8', 'ANALOG-02': '#60a5fa', 'ANALOG-03': '#34d399',
      'ANALOG-04': '#818cf8', 'ANALOG-05': '#10b981', 'ANALOG-06': '#f43f5e'
    }};

    analogsData.forEach(c => {{
      ctx.beginPath(); ctx.strokeStyle = colors[c.case_id] || '#fff'; ctx.lineWidth = 2;
      const pts = [];
      const m1 = 100 * (1 + c.return_1m / 100);
      const m3 = 100 * (1 + c.return_3m / 100);
      const m6 = 100 * (1 + c.return_6m / 100);
      const m12 = 100 * (1 + c.return_12m / 100);

      for (let day = 0; day <= 250; day += 10) {{
        let val = 100;
        if (day <= 22) val = 100 + (m1 - 100) * (day / 22);
        else if (day <= 65) val = m1 + (m3 - m1) * ((day - 22) / 43);
        else if (day <= 130) val = m3 + (m6 - m3) * ((day - 65) / 65);
        else val = m6 + (m12 - m6) * ((day - 130) / 120);
        pts.push({{ day, val }});
      }}

      pts.forEach((p, i) => {{
        const x = getX(p.day), y = getY(p.val);
        if (i === 0) ctx.moveTo(x, y); else ctx.lineTo(x, y);
      }});
      ctx.stroke();
    }});
  }}

  function renderDashFan() {{
    const {{ canvas, ctx, width, height }} = setupCanvas('dash-fan-canvas', 'dash-fan-box');
    const pad = {{ top: 20, right: 80, bottom: 30, left: 20 }};
    const cWidth = width - pad.left - pad.right;
    const cHeight = height - pad.top - pad.bottom;

    const horizons = scenarioData.horizons;
    const nodes = [
      {{ label: '현재', bull: 857000, base: 857000, bear: 857000, ev: 857000 }},
      {{ label: '단기 (1~4W)', bull: horizons.short_term_1_4w.bull.square_target_unit_krw, base: horizons.short_term_1_4w.base.square_target_unit_krw, bear: horizons.short_term_1_4w.bear.square_target_unit_krw, ev: horizons.short_term_1_4w.expected_value_unit_krw }},
      {{ label: '중기 (1~3M)', bull: horizons.mid_term_1_3m.bull.square_target_unit_krw, base: horizons.mid_term_1_3m.base.square_target_unit_krw, bear: horizons.mid_term_1_3m.bear.square_target_unit_krw, ev: horizons.mid_term_1_3m.expected_value_unit_krw }},
      {{ label: '장기 (6~12M)', bull: horizons.long_term_6_12m.bull.square_target_unit_krw, base: horizons.long_term_6_12m.base.square_target_unit_krw, bear: horizons.long_term_6_12m.bear.square_target_unit_krw, ev: horizons.long_term_6_12m.expected_value_unit_krw }},
    ];

    const minPrice = 600000, maxPrice = 2400000;
    const getX = i => pad.left + (i / (nodes.length - 1)) * cWidth;
    const getY = p => pad.top + cHeight - ((p - minPrice) / (maxPrice - minPrice)) * cHeight;

    // Breakeven 1.09M
    const yCost = getY(1090000);
    ctx.strokeStyle = '#f59e0b'; ctx.lineWidth = 1.5; ctx.setLineDash([4, 4]);
    ctx.beginPath(); ctx.moveTo(pad.left, yCost); ctx.lineTo(pad.left + cWidth, yCost); ctx.stroke();
    ctx.fillStyle = '#f59e0b'; ctx.font = '10px sans-serif'; ctx.fillText('본전 평단 (109만)', pad.left + cWidth + 6, yCost + 3);

    // TP1 2.18M
    const yTp1 = getY(2180000);
    ctx.strokeStyle = '#10b981'; ctx.lineWidth = 2.0; ctx.setLineDash([4, 4]);
    ctx.beginPath(); ctx.moveTo(pad.left, yTp1); ctx.lineTo(pad.left + cWidth, yTp1); ctx.stroke();
    ctx.fillStyle = '#10b981'; ctx.font = '10px sans-serif'; ctx.fillText('TP1 (218만)', pad.left + cWidth + 6, yTp1 + 3);
    ctx.setLineDash([]);

    // Bull / Bear Cones
    ctx.beginPath();
    ctx.moveTo(getX(0), getY(nodes[0].bear));
    for (let i = 1; i < nodes.length; i++) ctx.lineTo(getX(i), getY(nodes[i].bear));
    for (let i = nodes.length - 1; i >= 0; i--) ctx.lineTo(getX(i), getY(nodes[i].bull));
    ctx.closePath();
    ctx.fillStyle = 'rgba(56, 189, 248, 0.12)';
    ctx.fill();

    // EV Trajectory
    ctx.beginPath(); ctx.strokeStyle = '#38bdf8'; ctx.lineWidth = 3;
    nodes.forEach((n, i) => {{ const x = getX(i), y = getY(n.ev); if (i === 0) ctx.moveTo(x, y); else ctx.lineTo(x, y); }});
    ctx.stroke();

    nodes.forEach((n, i) => {{
      const x = getX(i);
      ctx.beginPath(); ctx.arc(x, getY(n.ev), 5, 0, Math.PI * 2);
      ctx.fillStyle = '#38bdf8'; ctx.fill(); ctx.strokeStyle = '#fff'; ctx.lineWidth = 2; ctx.stroke();
      ctx.fillStyle = '#f8fafc'; ctx.font = '11px sans-serif'; ctx.textAlign = 'center';
      ctx.fillText(n.label, x, pad.top + cHeight + 18);
    }});
    ctx.textAlign = 'left';
  }}

  window.addEventListener('resize', () => {{
    renderDashNav();
  }});

  window.addEventListener('DOMContentLoaded', () => {{
    renderDashNav();
  }});
  </script>
</body>
</html>
"""

with open(os.path.join(WORKSPACE_DIR, "dashboard.html"), "w", encoding="utf-8") as f:
    f.write(dashboard_html)
print("Saved dashboard.html")

print("All visual components built successfully!")
