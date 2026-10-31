# TEST_INFRA.md: Daily 08:10 AM KST 3-Page A4 PDF Investment Monitoring Report System Test Infrastructure

## 1. Test Philosophy & Quantitative Principles

The test suite for the Daily 08:10 AM KST 3-Page A4 PDF Investment Monitoring Report System ("구성안 A: 행동 시간순 배치") is architected as an **opaque-box, requirement-driven, deterministic test suite**. It guarantees mathematical rigor, execution integrity, zero coupling to internal presentation code, 100% primary source purity (0% Korean domestic media), and strict 3-page A4 physical layout containment.

### Core Testing Tenets:
1. **Opaque-Box Requirement Verification**: Tests validate the behavioral contracts, mathematical ground truths, and physical PDF layout specified in `ORIGINAL_REQUEST.md`, `PROJECT.md`, `quant_specs.md`, and `pdf_automation_specs.md`, rather than asserting against private implementation internals.
2. **Deterministic Mathematical Ground Truth**: All financial calculations (Asymmetric Beta Open Gap $\beta_{\text{down}}=1.55 / \beta_{\text{up}}=0.95$, Simulated Daily RSI(14), SOTP NAV & Discount, 1억 Graduation Target, 1,360만 KRW Share Defense Table, $\pm 5.0\%p$ Tax-Saver Band, SMH -20% Contrarian Tilt, 4 PW-RSI Conditions + `MA20 5D Slope > 0`, Stage 2 4 Exit Rules) are evaluated against exact closed-form analytical formulas.
3. **100% US & China Source Purity / 0% Korean Media Blacklist**: Automated regex and domain audits verify that zero domestic Korean news portals, domestic news outlets, or Korean brokerage houses are referenced anywhere in the intelligence feeds or generated PDF reports.
4. **Physical PDF Geometry & Typography Discipline**: Direct PyMuPDF (`fitz`) inspection validates:
   - `len(doc) == 3` strictly (never 2, never 4+ pages).
   - Document size $> 50\text{ KB}$.
   - Exact A4 portrait dimensions: $595.28 \times 841.89\text{ pt}$ ($\pm 2.5\text{ pt}$).
   - Zero vertical clipping ($y_1 \le 838.0\text{ pt}$ for all text blocks) and zero unreadable text collisions.
5. **Progressive & Self-Contained Testability**: All tests set up their own fixtures, fallback safely to local CSV caches (`data_stocks/`, `data/`), operate offline with zero network flakiness, and provide clean test execution without modifying production code.

---

## 2. 4-Tier Test Architecture

The test suite (`tests/test_morning_pdf_report.py`) implements a structured 4-tier hierarchy:

```
┌────────────────────────────────────────────────────────────────────────┐
│               TIER 4: REAL-WORLD ACCEPTANCE SCENARIOS                  │
│  - Full execution of `generate_morning_pdf.py`                         │
│  - Dual output: `YYYY-MM-DD_Morning_Alpha_Briefing.pdf` & `Latest_...` │
│  - PyMuPDF strict 3-page validation: `len(doc) == 3` (never 2 or 4+)   │
│  - PDF file size threshold: `size > 50,000 bytes`                      │
│  - Text bounding box inspection: `y1 <= 838.0 pt` (zero clipping)      │
│  - Batch script inspection: `run_morning_pdf_0810.bat` (chcp 65001)    │
├────────────────────────────────────────────────────────────────────────┤
│               TIER 3: CROSS-FEATURE COMBINATIONS                       │
│  - Overnight USD/KRW spike + SMH market drop (natural FX cushion)      │
│  - SK Square price collapse + 1,360만 KRW cash share defense recalculation│
│  - PW-RSI 1_BUY_IGNITION emergence + Discipline banner disappearance   │
│  - SMH 52W DD <= -20% + weight drift < 55% (drawdown tilt priority)   │
│  - Stage 2 active position holding countdown + stop-loss/tax credit    │
├────────────────────────────────────────────────────────────────────────┤
│               TIER 2: BOUNDARY & CORNER CASES                          │
│  - Extreme gap drops (-10%, -15% circuit breaker) & 0.0% unchanged gap │
│  - RSI(14) 0-variance series ($U=0, D=0 \to 50.0$) and extreme crash   │
│  - Tax-Saver band exact boundaries ($w_{\text{SMH}} = 55.0\%, 65.0\%$)  │
│  - Contrarian tilt exact boundary ($\text{DD} = -20.0\% \to 75\%$)     │
│  - PW-RSI boundary values: Prox_low=10.0%, 40.0%; Slope=0.0% (strict)  │
│  - Value-Trap blacklist enforcement (INTC, PFE, BA, NKE, PARA, WBD, ALB)│
│  - Offline mode & empty network responses falling back to local CSVs   │
├────────────────────────────────────────────────────────────────────────┤
│               TIER 1: FEATURE COVERAGE (ISOLATED SPECIFICATIONS)       │
│  - T1.1: 100% US & China primary source badge & origin schema          │
│  - T1.2: 0% South Korean domestic media blacklist regex audit          │
│  - T1.3: Page 1 30-Second Executive Banner (3 traffic light cards)     │
│  - T1.4: Page 1 Asymmetric beta open gap math (1.55 vs 0.95) & RSI(14) │
│  - T1.5: Page 1 SOTP Dual-Target gauge & 1,360만 share defense math   │
│  - T1.6: Page 2 SMH(60%)+XLV(40%) FX cushion & zero ETF oscillators    │
│  - T1.7: Page 2 ±5.0%p Tax-Saver band & SMH -20% contrarian tilt       │
│  - T1.8: Page 3 State-Aware Discipline Banner (0 buy signals)          │
│  - T1.9: Page 3 Stage 2 Active Position 4 exit rules                   │
│  - T1.10: Page 3 Actionable Top 5 & 4 conditions (MA20 slope > 0)      │
│  - T1.11: Page 3 Top 2 Spotlight Deep-Dive cards & Value-Trap Firewall │
└────────────────────────────────────────────────────────────────────────┘
```

---

## 3. Feature Inventory & Coverage Matrix (Features 1 ~ 32)

Every feature defined in `PROJECT.md` is mapped to its test tier, test method in `tests/test_morning_pdf_report.py`, and verification objective:

| # | Feature Name | Test Method | Tier | Verification Objective |
|---|---|---|:---:|---|
| 1 | 100% US & China Tickers Fetch | `test_feature_01_market_tickers_and_proxies` | Tier 1 | Ingests MU, NVDA, AVGO, SMH, XLV, QQQ, EWY, KORU, 0981.HK, 002371.SZ, 2408.TW, USD/KRW |
| 2 | 2-Tier Offline CSV Fallback | `test_feature_02_offline_csv_fallback` | Tier 1 | Seamless fallback to `data_stocks/` and `data/` local CSVs on network timeout/offline |
| 3 | 100% US/CN Primary News Badging | `test_feature_03_source_origin_badging` | Tier 1 | Enforces `[🇺🇸 US \| Source]` and `[🇨🇳 CN/TW \| Source]` format, EN/CN headline, KR summary |
| 4 | 0% Korean Media Blacklist | `test_feature_04_korean_media_blacklist_firewall` | Tier 1 | Automated regex audit verifies 0 occurrences of Naver, Daum, Hankyung, MK, Sedaily, etc. |
| 5 | Top 30-Second Executive Banner | `test_feature_05_executive_banner_logic` | Tier 1 | 3 traffic light cards (`🟢/🟡/🔴`) for SK Square, SMH+XLV Barbell, and PW-RSI Alpha |
| 6 | Overnight US/CN Proxy Bridge | `test_feature_06_overnight_bridge_sentiment` | Tier 1 | Composite semi return: $0.40 \cdot r_{\text{MU}} + 0.35 \cdot r_{\text{NVDA}} + 0.25 \cdot r_{\text{SMH}}$ |
| 7 | Asymmetric Beta Gap Simulator | `test_feature_07_asymmetric_beta_simulator` | Tier 1 | SK Square beta: $\beta_{\text{down}}=1.55$ when $\Delta < 0$, $\beta_{\text{up}}=0.95$ when $\Delta \ge 0$ |
| 8 | Simulated Daily RSI(14) | `test_feature_08_simulated_rsi14_calculator` | Tier 1 | Wilder's exponential moving average RSI(14) with $\alpha = 1/14$ under projected gap drops |
| 9 | Intraday Timing Rules & Win Rate | `test_feature_09_intraday_timing_and_win_rate` | Tier 1 | 09:00~09:30 panic sell ban, 10:30~14:00 rebound rule, RSI <= 29.5 5D 90% rebound win-rate |
| 10 | Dual-Target Valuation SVG Gauge | `test_feature_10_dual_target_valuation_gauge` | Tier 1 | SOTP NAV (20.76% stake + 20조 other), Case B/C, 1억 target (131.6만/151.6만), TP1 (218만) |
| 11 | Share Defense Calculator | `test_feature_11_share_count_defense_table` | Tier 1 | $\lceil 13.6\text{M} / P \rceil$ consumed shares at current vs rebound prices (109만, 132만) |
| 12 | 8 US/China Quantitative Triggers | `test_feature_12_eight_triggers_grid` | Tier 1 | 2×4 grid (`TRIG-01`~`08`) with Day-over-Day $\Delta$ metrics and bullish/bearish thresholds |
| 13 | Top 3 News & 3 Kill-Switches | `test_feature_13_news_and_kill_switches` | Tier 1 | Industry, Governance, Dilution kill-switches monitoring + US/CN primary memory headlines |
| 14 | SMH+XLV Scorecard & FX Cushion | `test_feature_14_smh_xlv_scorecard_fx_cushion` | Tier 1 | Proof of $R_{\text{KRW}} > R_{\text{USD}}$ when $R_{\text{FX}} > 0$; 1D/5D/20D/YTD/52W High DD metrics |
| 15 | Zero ETF Oscillator Guarantee | `test_feature_15_zero_etf_oscillator_guarantee` | Tier 1 | Hard prohibition of daily RSI/MACD on SMH/XLV to eliminate 22% tax drag |
| 16 | $\pm 5.0\%p$ Tax-Saver Band | `test_feature_16_tax_saver_tolerance_band` | Tier 1 | $55.0\% \le w_{\text{SMH}} \le 65.0\%$ enforces HOLD (zero rebalancing, zero tax realization) |
| 17 | SMH -20% Contrarian Tilt Gauge | `test_feature_17_contrarian_drawdown_tilt` | Tier 1 | SMH 52W DD $\le -20.0\%$ tilts target to 75%; recovery $> -5.0\%$ harvests profit back to 60% |
| 18 | XLV Downside Cushion Scorecard | `test_feature_18_xlv_cushion_and_rolling_corr` | Tier 1 | 20D/60D rolling `Corr(SMH, XLV)` vs `Corr(SMH, QQQ)` and crash day ($\le -1.5\%$) defense |
| 19 | Top 3 Holdings Pulse | `test_feature_19_top_holdings_pulse` | Tier 1 | SMH Top 3 (NVDA, TSM, AVGO) + XLV Top 3 (LLY, UNH, JNJ) + US 10Y Yield + China bellwethers |
| 20 | Top 3 Curated Sector News | `test_feature_20_curated_sector_news` | Tier 1 | Primary US & China semiconductor/healthcare news items with badges and KR takeaways |
| 21 | State-Aware Discipline Banner | `test_feature_21_state_aware_discipline_banner` | Tier 1 | Active when `1_BUY_IGNITION` count is 0, reinforcing patience protecting 26.8Y 21.97% CAGR |
| 22 | Stage 2 Active Survival Monitor | `test_feature_22_stage2_active_survival_monitor` | Tier 1 | -9% hard stop, 55D time-stop (< +8%), weekly upgrade switch (+10pt), MA60 TP1 half-exit |
| 23 | Actionable Top 5 Leaderboard | `test_feature_23_actionable_top5_leaderboard` | Tier 1 | Ranks Top 5 (`1_BUY_IGNITION` & `2_READY_MA20` only), excludes Korean stocks & falling knives |
| 24 | 4 Explicit PW-RSI Conditions | `test_feature_24_four_pwrsi_conditions_math` | Tier 1 | DD $\le -38\%$, Prox 10%~40%, Close > MA20 & MA60 AND `MA20 Slope > 0`, Vol $\ge 1.35x$ / Ret $\ge +8\%$ |
| 25 | Spotlight Deep-Dive Cards | `test_feature_25_spotlight_deep_dive_cards` | Tier 1 | Rich cards for Top 2 (Washout Root Cause, 1~2Y Catalyst, 26.8Y Analog, Execution Plan) |
| 26 | Value-Trap Firewall Notice | `test_feature_26_value_trap_firewall` | Tier 1 | Blocks secularly impaired stocks (`INTC`, `PFE`, `BA`, `NKE`, `PARA`, `WBD`, `ALB`) |
| 27 | Unified CLI Entrypoint | `test_feature_27_cli_entrypoint_interface` | Tier 4 | `generate_morning_pdf.py` execution with optional `--open` and `--offline` flags |
| 28 | Strict 3-Page A4 PDF Output | `test_feature_28_strict_three_page_pdf_output` | Tier 4 | Produces dated PDF and `Latest_Morning_Alpha_Briefing.pdf` with `size > 50 KB` |
| 29 | PyMuPDF Geometry & Zero-Clipping | `test_feature_29_pymupdf_geometry_and_bounds` | Tier 4 | `len(doc) == 3`, dimensions $595 \times 842\text{ pt}$, text block $y_1 \le 838.0\text{ pt}$ |
| 30 | Daily 08:10 AM Batch Script | `test_feature_30_windows_batch_runner` | Tier 4 | `run_morning_pdf_0810.bat` with `chcp 65001`, logging, and `--open` invocation |
| 31 | Task Scheduler Registration | `test_feature_31_task_scheduler_command` | Tier 4 | Verifies `schtasks /create` syntax and 08:10 KST automated trigger command |
| 32 | Comprehensive 4-Tier Test Suite | `test_feature_32_full_test_suite_integrity` | Tier 4 | Entire test suite executes cleanly and reports clear pass/fail diagnostics |

---

## 4. Expected Output Derivation & Mathematical Ground Truth

Every test verifies calculations against authoritative formulas derived from financial theory and project specifications:

### 4.1 Asymmetric Beta Open Gap Simulation
$$\Delta_{\text{Square}} = \begin{cases} 1.55 \times \Delta_{\text{Hynix}}, & \text{if } \Delta_{\text{Hynix}} < 0 \\ 0.95 \times \Delta_{\text{Hynix}}, & \text{if } \Delta_{\text{Hynix}} \ge 0 \end{cases}$$
$$P_{\text{Square, projected}} = \text{round}\left(P_{\text{Square, close}} \times \left(1 + \frac{\Delta_{\text{Square}}}{100}\right), -3\right)$$
$$V_{76} = \frac{76 \times P_{\text{Square, projected}}}{10,000} \quad\text{(만 원)}$$
$$\text{Buffer}_{\text{floor}} = \left(\frac{P_{\text{Square, projected}}}{780,000} - 1.0\right) \times 100\%$$

### 4.2 Simulated Daily RSI(14)
$$\alpha = \frac{1}{14}, \quad \Delta P_t = P_t - P_{t-1}$$
$$U_t = \alpha \max(\Delta P_t, 0) + (1 - \alpha) U_{t-1}, \quad D_t = \alpha \max(-\Delta P_t, 0) + (1 - \alpha) D_{t-1}$$
$$\text{Simulated RSI}(14) = 100 - \frac{100}{1 + \frac{U_{N+1}}{D_{N+1} + 10^{-9}}}$$

### 4.3 SOTP Dual-Target Valuation & 1억 Graduation Target
- Stake in Hynix: $20.76\%$ ($0.2076$)
- Hynix shares: $706,420,000$; Square shares: $131,920,000$; Other NAV: $20.0\text{조 원}$
$$\text{NAV}_{\text{per share}} = \frac{(P_{\text{Hynix}} \times 706,420,000 \times 0.2076) + 20 \times 10^{12}}{131,920,000}$$
$$\text{NAV Discount } (\%) = \left(1 - \frac{P_{\text{Square}}}{\text{NAV}_{\text{per share}}}\right) \times 100\%$$
- 1억 Graduation Target (76 shares): $100,000,000 / 76 = \mathbf{1,316,000\text{ KRW}}$
- 1억 Graduation Target (66 shares): $100,000,000 / 66 = \mathbf{1,516,000\text{ KRW}}$
- Net USD Conversion Pool: $100,000,000 \times (1 - 0.0035 - 0.0012) / (\text{USD/KRW}) \approx \mathbf{\$74,000 \sim \$76,000}$
- TP1 Price: $2.0 \times 1,090,000 = \mathbf{2,180,000\text{ KRW}}$

### 4.4 Emergency Cash 1,360만 KRW Share Defense Calculator
$$\text{Shares to Sell} = \left\lceil \frac{13,600,000}{P_{\text{sale}}} \right\rceil, \quad \text{Remaining Shares} = 76 - \text{Shares to Sell}$$
$$\text{Shares Saved} = 16 - \text{Shares to Sell}, \quad \text{Target for 1억 원} = \frac{100,000,000}{\text{Remaining Shares}}$$

### 4.5 Natural FX Cushion & Barbell Return
$$R_{\text{KRW}} = (1 + R_{\text{USD}}) \times (1 + R_{\text{FX}}) - 1.0$$
$$R_{\text{Barbell, USD}} = 0.60 \times R_{\text{SMH, USD}} + 0.40 \times R_{\text{XLV, USD}}$$
$$R_{\text{Barbell, KRW}} = (1 + R_{\text{Barbell, USD}}) \times (1 + R_{\text{FX}}) - 1.0$$

### 4.6 $\pm 5.0\%p$ Tax-Saver Band & Contrarian Tilt
$$55.0\% \le w_{\text{SMH}} \le 65.0\% \implies \mathbf{HOLD} \text{ (Zero rebalance)}$$
$$\text{DD}_{\text{SMH, 52W}} \le -20.0\% \implies \text{Target } w_{\text{SMH}} = \mathbf{75.0\%}$$
$$\text{DD}_{\text{SMH, 52W}} > -5.0\% \land w_{\text{SMH}} > 65.0\% \implies \text{Reset to } \mathbf{60.0\%}$$

### 4.7 4 PW-RSI Conditions & `MA20 5D Slope > 0`
1. $\text{DD}_{\text{52W High}} \le -38.0\%$
2. $+10.0\% \le \text{Prox}_{\text{52W Low}} \le +40.0\%$
3. $P_{\text{current}} > \text{MA20} \land P_{\text{current}} > \text{MA60} \land \text{Slope}_{\text{MA20, 5D}} > 0$
4. $\max_{10\text{D}} (\text{Vol} / \text{MA20}_{\text{vol}}) \ge 1.35x \lor \text{Return}_{20\text{D}} \ge +8.0\%$
$$\text{Trigger Price } (\$) = \max(\text{MA20}, \text{MA60})$$
$$\text{Distance to Trigger } (\%) = \left(\frac{\text{Trigger Price}}{P_{\text{current}}} - 1.0\right) \times 100\%$$

### 4.8 Stage 2 Active Position 4 Exit Rules
1. Hard Stop-Loss: $P_{\text{stop}} = \text{round}(P_{\text{entry}} \times 0.91, 2)$ (-9.0% loss realization yields 22% tax-loss credit).
2. Time-Stop: $\text{HoldingDays} \ge 55 \land \text{Return} < +8.0\% \implies$ Dead money exit.
3. Weekly Upgrade Switch: $\text{HoldingDays} \ge 25 \land \text{Return} < +12.0\% \land P < \text{MA20} \land \text{Score}_{\text{new \#1}} \ge \text{Score}_{\text{current}} + 10.0\text{ pts}$.
4. Trailing Stop & TP1: $+40\% \le \text{Return} < +100\% \implies P < 0.97 \times \text{MA60}$; $\text{Return} \ge +100\% \implies 50\%$ half-exit to recover 100% capital.

---

## 5. Verification Commands

To execute the test suite independently:

```bash
# Run the entire test suite with verbose reporting
pytest tests/test_morning_pdf_report.py -v

# Run individual tiers
pytest tests/test_morning_pdf_report.py -k "TestTier1" -v
pytest tests/test_morning_pdf_report.py -k "TestTier2" -v
pytest tests/test_morning_pdf_report.py -k "TestTier3" -v
pytest tests/test_morning_pdf_report.py -k "TestTier4" -v

# Run with full traceback on failure
pytest tests/test_morning_pdf_report.py -v --tb=short
```
