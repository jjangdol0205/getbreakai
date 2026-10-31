# TEST_INFRA — Test Infrastructure Architecture

## 1. Overview & Purpose
This document specifies the architecture, execution model, mathematical oracles, and acceptance gates of the **4-Tier E2E Opaque-Box Test Suite** (`test_forecast_suite.py`) for the **SK Square (402340) & SK Hynix (000660) Forecast Engine**.

The test infrastructure is designed under strict opaque-box principles:
- **Authoritative Specifications**: All expectations are derived directly from `ORIGINAL_REQUEST.md` (section `## 2026-10-13T23:02:36Z`), `reference_user_notes.md`, `PROJECT.md`, and `spec_report.md`.
- **Zero-Facade Guarantee**: Tests verify real mathematical calculations, boundary conditions, data schemas, and actual artifact files on disk. No mock facades that unconditionally pass.
- **Progressive Testability**: The test suite gracefully detects milestone progress. Mathematical oracles, schemas, boundary cases, and existing milestone artifacts execute immediately, while pending milestone deliverables (e.g. M2 dashboard, M4 report) are transparently resolved via structured skipping until their respective milestones complete.

---

## 2. 4-Tier Test Suite Architecture

```
                    ┌────────────────────────────────────────────────────────┐
                    │      4-Tier E2E Opaque-Box Test Architecture           │
                    └────────────────────────────────────────────────────────┘
                                                │
         ┌──────────────────┬───────────────────┴───────────────────┬──────────────────┐
         ▼                  ▼                                       ▼                  ▼
   ┌───────────┐      ┌───────────┐                           ┌───────────┐      ┌───────────┐
   │  Tier 1   │      │  Tier 2   │                           │  Tier 3   │      │  Tier 4   │
   │  Feature  │      │ Boundary  │                           │   Math    │      │Real-World │
   │ Coverage  │      │ & Corner  │                           │Consistency│      │ Scenarios │
   └───────────┘      └───────────┘                           └───────────┘      └───────────┘
         │                  │                                       │                  │
   • 6 Domains        • Strict 0 NaN                          • NAV Identity     • Analogs (>=5)
   • F1 ~ F18         • Zero-Division                         • Accretion Math   • 76-Share TP1
   • CLI & Files      • Premium Regime                        • Asymmetric β     • 8 Triggers
                      • Stress Bounds                         • Scenario EVs     • Report Rubric
```

### Tier 1: Feature Coverage (Features 1 to 27)
- **Domain 1 (Fundamental)**: Gross Asset Value, Net Asset Value, Per-Share NAV, Discount Rate, 40T Buyback Accretion (20.07% -> 20.76%), Solidigm $100B~$150B fair valuation sensitivity, Dell/Chey 544B KRW block deal impact.
- **Domain 2 (Technical)**: Multi-timeframe Moving Averages (20/60/120/200 MAs), 200MA distance (%), 50-bin Volume Profile (POC/VAH/VAL), Fibonacci cycle retracements (23.6%, 38.2%, 50.0%, 61.8%, 78.6%), RSI(14), MACD(12,26,9), Bollinger Bands(20,2), P/B channels (0.4x~0.9x).
- **Domain 3 (Supply & Demand)**: 4 participant flow tracking (Foreigner, Institution, Retail, Other Corp), Foreign ownership Z-Score and -1σ (47.2%) floor, Treasury buyback completion demand vacuum.
- **Domain 4 (Derivatives & Market Mechanics)**: Futures-Spot Basis ($F - S$), Contango vs Backwardation, Foreign futures contracts, Asymmetric downside beta ($\beta_{down} > \beta_{up}$) and return spread.
- **Domain 5 (Short Selling & Margin)**: Short volume ratio (%), Loan balance (대차잔고), Short covering / squeeze threshold triggers (-5% 5D), Margin call 140% danger zone price.
- **Domain 6 (Historical Analogs & Classifier)**: Backtest parameters of 6 analog cases, Trajectory classification (`V_SHAPE`, `W_SHAPE`, `L_SHAPE`).
- **CLI & Output Pipeline**: Executable verification of `run_forecast.py` / `forecast_engine.py` with exit code 0.

### Tier 2: Boundary & Corner Cases
- **Strict Zero-NaN Policy**: Automated recursive inspection across all JSON and CSV datasets in `data/`. Every float must be finite; zero `NaN`, `null`, `undefined`, `inf`, or `-inf` tolerated.
- **Negative Discount (Premium Regime)**: Correctly models situations where $P_{sq} > NAV_{per\_share}$, resulting in negative discount rates without clipping or runtime crashes.
- **Zero-Division Guards**:
  * Peak equals Trough in Fibonacci: clamps levels to current price without zero division.
  * Flat price series in RSI: returns neutral 50.0.
  * Monotonic rising price series in RSI: returns 100.0 without divide-by-zero on average loss.
  * Hynix daily return equals 0.0%: rolling variance and beta calculation remains robust.
  * Zero margin borrowing: danger price returns 0.0.
- **Adversarial & Stress Bounds**:
  * Korean UTF-8 character encoding roundtrip fidelity.
  * Invalid input combinations (negative shares, non-positive NAV in discount formula, mismatched series lengths) raise explicit `ValueError`.
  * Hyper-bull stress test (Hynix at 1,000,000 KRW): NAV scales without numeric overflow.
  * Extreme panic stress test (VKOSPI at 65.0): correctly flags regime as `BEARISH_STRESS`.

### Tier 3: Mathematical Consistency & Exact Interface Formulas
- **NAV Formulation**:
  $$NAV_{total} = P_{hynix} \times 146,100,000 + V_{unlisted} - NetDebt_{holding}$$
  $$NAV_{per\_share} = \frac{NAV_{total}}{134,700,000}$$
  $$Discount = \frac{NAV_{per\_share} - P_{square}}{NAV_{per\_share}} \times 100\%$$
- **Buyback Accretion Math**:
  $$\text{Post Shares} = 728,002,365 - 24,070,000 = 703,932,365$$
  $$\text{Ownership Ratio} = \frac{146,100,000}{703,932,365} = 20.7548\% \approx 20.76\% \quad (\text{from } 20.0686\% \approx 20.07\%)$$
  $$\text{Accretion Factor} = \frac{728,002,365}{703,932,365} = 1.03419 \quad (+3.42\% \text{ EPS/BPS uplift})$$
- **Asymmetric Beta Formulation**:
  $$\beta_{down} = \frac{\text{Cov}(R_{sq}, R_{hy} \mid R_{hy} < 0)}{\text{Var}(R_{hy} \mid R_{hy} < 0)}, \quad \beta_{up} = \frac{\text{Cov}(R_{sq}, R_{hy} \mid R_{hy} > 0)}{\text{Var}(R_{hy} \mid R_{hy} > 0)}$$
  $$\text{Asymmetry Ratio} = \frac{\beta_{down}}{\beta_{up}} > 1.0$$
- **Multi-Horizon Scenario Probability & Expected Value Integrity**:
  * Probabilities sum to 1.0 across Short, Mid, and Long horizons.
  * Short-term EV: $0.25 \times 1,060,000 + 0.50 \times 910,000 + 0.25 \times 760,000 = \mathbf{910,000\text{ KRW}}$
  * Mid-term EV: $0.30 \times 1,300,000 + 0.45 \times 1,050,000 + 0.25 \times 730,000 = \mathbf{1,045,000\text{ KRW}}$
  * Long-term EV: $0.35 \times 2,180,000 + 0.45 \times 1,320,000 + 0.20 \times 710,000 = \mathbf{1,499,000\text{ KRW}}$

### Tier 4: Real-World Scenarios
- **Historical Analogs Table ($\ge 5$ cases)**:
  1. SK Hynix 2018-2019: Peak 95.3k, Trough 57.7k, MDD -39.45% / -42.0%, Days ~150-180, `W_SHAPE`
  2. SK Hynix 2021-2022: Peak 150.5k, Trough 78.5k, MDD -47.8%, Days ~330, `W_SHAPE`
  3. Micron MU 2018: Peak $62.62, Trough $29.02, MDD -53.66%, Days ~145-185, `W_SHAPE`
  4. TSMC TSM 2022: Peak $140.66, Trough $60.28, MDD -57.14%, Days ~202-280, `V_SHAPE`
  5. Nvidia NVDA 2021-2022: Peak $34.60, Trough $10.81, MDD -68.8%, Days ~340, `V_SHAPE`
  6. Samsung Electronics 2021-2022: Peak 96.8k, Trough 51.8k, MDD -46.5%, Days ~390, `L_SHAPE`
- **Investor 76-Share Position Diagnostic & TP1 Plan**:
  * 76 physical shares @ 1,090,000 KRW avg cost = 82,840,000 KRW invested principal.
  * Baseline market value @ 857,000 KRW = 65,132,000 KRW (-21.38% unrealized return).
  * TP1 Milestone: Target price 2,180,000 KRW (+100.0% vs cost basis).
  * TP1 Execution: Sell exactly 38 shares (50%) = 82,840,000 KRW cash recovered (100% of original principal).
  * Post-TP1 State: 38 shares retained at 0 KRW net cost (100% Risk-Free carry).
- **Objective 8-Point Trigger Checklist**:
  * 8 quantitative signals (Foreign futures 3D > 15k, Basis > 0.50pt, Loan balance -5% 5D, 200MA defense 3D, NAV discount <= 52%, Buyback filing confirmed, VKOSPI < 18, Dual net buying > 10B KRW).
  * Regime scores: 0~2 (BEARISH_STRESS), 3~5 (NEUTRAL_CONSOLIDATION), 6~8 (BULLISH_REVERSAL).
- **Deep Research Report & Dashboard Offline Rubric**:
  * Audits report structure (6 domains, Red Team, Fact-Check, 3-Month strategist tracking).
  * Enforces 100% Zero-CDN offline self-containment (zero external network URLs in HTML files).

---

## 3. Test Execution Commands

### Standard Runner
```bash
python test_forecast_suite.py
```

### Unittest Module Discovery
```bash
python -m unittest test_forecast_suite.py -v
```

### Target Exit Code
- Exit Code: `0`
- Minimum Passing Tests: `44+`
- Failures / Errors: `0`

---

## 4. Progressive Milestone Integration Matrix

| Milestone | Deliverables | Test Coverage Status in `test_forecast_suite.py` |
|---|---|---|
| **M-TEST** | `test_forecast_suite.py`, `TEST_INFRA.md`, `TEST_READY.md` | Complete suite operational with canonical math oracle and schema verifiers |
| **M1** | Data Pipeline, `forecast_engine.py`, `data/*.csv`, `data/*.json` | `test_f25_cli_execution_and_artifacts`, `test_strict_zero_nan_in_data_records`, all `test_generated_*_file_integrity` PASS |
| **M2** | `dashboard.html`, `charts/*.html` | `test_offline_dashboard_and_chart_contracts` verifies Zero-CDN compliance |
| **M3** | Fact-Check, Strategist Tracking, Red Team analysis | Verified via math oracle and deep research content validators |
| **M4** | Master Report `sk_square_forecast_deep_dive_report.md` | `test_deep_dive_report_institutional_rubric` verifies all mandatory sections |
| **M5** | Final E2E Audit & Certification | Full 46-test suite executes with 0 skips, 0 errors, 0 failures |

---

## 5. Artifact & Directory Inventory
```
d:\관심종목\sk_square_forecast\
├── test_forecast_suite.py                    # Master 4-tier E2E test runner (46 test cases)
├── TEST_INFRA.md                             # Test infrastructure architecture specification
├── TEST_READY.md                             # Test readiness attestation & inventory
├── forecast_engine.py                        # Master quantitative engine
├── run_forecast.py                           # CLI entry point wrapper
├── reference_user_notes.md                   # Authoritative user inputs
├── sk_square_forecast_deep_dive_report.md   # Final deep research report (M4)
├── dashboard.html                            # Offline executive dashboard (M2)
├── charts/                                   # Standalone interactive charts (M2)
└── data/                                     # Output datasets with 0 NaN guarantee (M1)
    ├── seed_market_data.json
    ├── nav_discount_series.csv & .json
    ├── technical_indicators.csv & .json
    ├── supply_demand_short.csv & .json
    ├── historical_analogs.csv & .json
    └── scenario_matrix.json
```
