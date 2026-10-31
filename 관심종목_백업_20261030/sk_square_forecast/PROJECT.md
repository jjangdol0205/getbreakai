# Project: SK Square (402340) & SK Hynix (000660) Forecast Engine & Deep Research

## Architecture
- **Data & Ingestion Layer**: Dual-track engine combining live market scraping with robust, offline static seed snapshots in `sk_square_forecast/data/` (guaranteeing 100% offline self-containment with zero external network or third-party dependency crash).
- **Quantitative Engine Layer (`forecast_engine.py`)**: Computes 6 core domains:
  1. Fundamental (NAV, discount rate, buyback cancellation equity accretion).
  2. Technical (20/60/120/200 MAs, Volume Profile POC/VAH/VAL, Fibonacci retracements, RSI, MACD, Bollinger Bands, PB/PE bands).
  3. Supply & Demand (4 participant categories, foreign ownership z-score floor, buyback vacuum).
  4. Futures & Derivatives (Basis, foreign futures, program trading, asymmetric downside beta).
  5. Short & Margin (Short volume ratio, loan balance, squeeze triggers, margin call liquidation floors).
  6. Historical Analogs (6 cases table: peak/trough dates, MDD, bottom days, +1M/+3M/+6M/+12M returns, V/W/L classification).
- **Visualization Layer (`charts/` & `dashboard.html`)**: Standalone, Zero-CDN offline interactive/SVG charts and executive dashboard.
- **Reporting Layer (`sk_square_forecast_deep_dive_report.md`)**: Full institutional-grade Korean Markdown report with all 6 domains, Fact-Check, 3-Month Analyst Tracking, Red Team, Scenario Price Bands, and 76-Share Position Trigger Checklist.
- **Verification & Audit Layer**: Automated test suite (`test_forecast_suite.py`) validating exit code 0, 0 NaN values, complete analog metrics, and forensic audit verifying authentic implementation.

## Feature Inventory
| # | Feature | Description | Milestone | Source | Status |
|---|---------|-------------|-----------|--------|--------|
| F1 | NAV & Discount Rate Engine | Gross asset value, net debt, NAV, per-share NAV, and historical discount rate series | M1 | Survey (F1) | DONE |
| F2 | Buyback Accretion Model | 40T KRW / 24.07M share cancellation effect on Square stake (20.07% -> 20.76%) and BPS/EPS (+3.42%) | M1 | Survey (F2) | DONE |
| F3 | Solidigm Valuation & IPO | $100B~$150B fair value, AI eSSD $10B run-rate, double-listing discount vs re-rating | M1, M3 | Survey (F3) | DONE |
| F4 | Dell/Chey Governance Model | 544B KRW block deal analysis, AI server synergy vs holdco cash flow reality | M1, M3 | Survey (F4) | DONE |
| F5 | Multi-Timeframe MAs | 20, 60, 120, 200 daily/weekly MAs, slope, distance from 200MA | M1 | Survey (F5) | DONE |
| F6 | Volume Profile & Fibonacci | 50-bin Volume Profile (POC, VAH, VAL) and cycle Fibonacci retracements | M1 | Survey (F6) | DONE |
| F7 | Momentum & Volatility | RSI(14), MACD(12,26,9), Bollinger Bands(20,2), VKOSPI volatility proxy | M1 | Survey (F7) | DONE |
| F8 | PB/PE Valuation Bands | Historical P/B (0.4x~0.9x) and P/E valuation channel projections | M1 | Survey (F8) | DONE |
| F9 | Multi-Investor Flow Tracker | Cumulative net purchases: Foreign, Institution, Retail, Other Corp | M1 | Survey (F9) | DONE |
| F10 | Foreign Ownership Z-Score | Foreign holding %, mean, standard deviation bands, -1σ (47.2%) floor test | M1 | Survey (F10) | DONE |
| F11 | Buyback Vacuum Analyzer | Treasury share program completion demand vacuum & pension rebalancing risk | M1 | Survey (F11) | DONE |
| F12 | Futures Basis & Program Trading | KOSPI200 Basis (F-S), contango/backwardation, foreign futures, program trading | M1 | Survey (F12) | DONE |
| F13 | Asymmetric Beta Modeling | Rolling beta, downside beta, upside beta, asymmetry ratio (β_down > β_up) | M1 | Survey (F13) | DONE |
| F14 | Short Selling & Loan Balance | Short volume ratio, loan balance (shares/value), short interest % | M1 | Survey (F14) | DONE |
| F15 | Short Squeeze Threshold | Mathematical triggers for short covering (loan balance -5%, 20MA cross) | M1 | Survey (F15) | DONE |
| F16 | Margin Call Zone Detector | 140% broker collateral liquidation danger price zones and overhang volume | M1 | Survey (F16) | DONE |
| F17 | Historical Analogs Simulator | 6 cases: Hynix 2018, Micron 2018, TSMC 2022, NVDA 2018, NVDA 2022, Samsung 2021 | M1 | Survey (F17) | DONE |
| F18 | Trajectory Classifier | V-shape vs W-shape vs L-shape attribution (Earnings, Multiple, Rates, Flow) | M1 | Survey (F18) | DONE |
| F19 | User Notes Fact-Check | Empirical verification of 6 claims in reference_user_notes.md | M3 | Survey (F19) | DONE |
| F20 | 3-Month Analyst Tracking | Sentiment evolution of Park Se-ik, Kim Jang-yeol, Lee Dae-ho, Wall St | M3 | Survey (F20) | DONE |
| F21 | Adversarial Red Team | 5 structural risk theses (holdco discount, HBM peak-out, Oct 27 sell-on, etc.) | M3 | Survey (F21) | DONE |
| F22 | Multi-Horizon Scenario Matrix | 3x3 Bull/Base/Bear price bands across 1~4W, 1~3M, 6~12M with exact formulas | M4 | Survey (F22) | DONE |
| F23 | 76-Share Position Diagnostic | Portfolio roadmap for 76 shares (82.84M principal, avg 1.09M, TP1 2.18M recovery) | M4 | Survey (F23) | DONE |
| F24 | Objective Trigger Checklist | 8 daily/weekly quantitative trigger indicators and decision rules | M4 | Survey (F24) | DONE |
| F25 | Forecasting CLI Engine | CLI tool (`run_forecast.py`) outputting 0 NaN CSV/JSON with exit code 0 | M1 | Survey (F25) | DONE |
| F26 | Deep Research Report Generator | Institutional-grade Markdown research report (`sk_square_forecast_deep_dive_report.md`)| M4 | Survey (F26) | DONE |
| F27 | Offline Chart & Dashboard Suite | Zero-CDN, 100% offline interactive/SVG charts and executive HTML dashboard | M2 | Survey (F27) | DONE |

## Milestones
| # | Name | Scope | Dependencies | Status |
|---|------|-------|-------------|--------|
| M-TEST | E2E Test Suite & Test Infra | Develop comprehensive opaque-box test suite (`test_forecast_suite.py`, `TEST_INFRA.md`, `TEST_READY.md`) covering Tiers 1-4 | none | DONE |
| M1 | Quantitative Data Pipeline & Engine | Build dual-track data seed, `forecast_engine.py`, compute all 6 domains, output clean CSV/JSON (0 NaN) | none | DONE |
| M2 | Visualization Charts & Dashboard | Build 100% offline Zero-CDN SVG/HTML charts and `dashboard.html` | M1 | DONE |
| M3 | Fact-Check, Analyst Tracking & Red Team | Author empirical fact-check matrix, 3-month strategist tracker, and Red Team risk analysis | M1 | DONE |
| M4 | Scenario Bands, Trigger Checklist & Master Report | Implement 3x3 scenario matrix, 76-share position guide, 8-point trigger checklist, and master Markdown research report | M1, M2, M3 | DONE |
| M5 | Final E2E Verification & Forensic Integrity Audit | Run 100% E2E tests, challenger stress testing, and forensic auditor certification | M-TEST, M4 | DONE |

## Interface Contracts
### `forecast_engine.py` ↔ Data Artifacts
- **Inputs**: Offline seed data in `data/seed_market_data.json` and optional live fetch fallback.
- **Outputs**:
  * `data/nav_discount_series.csv` & `data/nav_discount_series.json`
  * `data/technical_indicators.csv` & `data/technical_indicators.json`
  * `data/supply_demand_short.csv` & `data/supply_demand_short.json`
  * `data/historical_analogs.csv` & `data/historical_analogs.json`
  * `data/scenario_matrix.json`
- **Integrity Guarantee**: All generated CSV/JSON contain 0 `NaN` values, with programmatic exit code 0.

### Quantitative Engine ↔ Visual Dashboard (`dashboard.html`)
- **Data Ingestion**: Embedded JSON and pure local SVG/Canvas rendering.
- **Zero-CDN Compliance**: 100% verified, 0 external script/font/stylesheet tags.

### Analytical Outputs ↔ Deep Research Report (`sk_square_forecast_deep_dive_report.md`)
- **Sections**: All 11 sections verified with 100% numerical parity against generated datasets.
