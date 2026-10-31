# TEST_INFRA.md: RightSideAlpha Full-Stack Web Service E2E Test Infrastructure

## 1. Test Philosophy & Quantitative Principles

The test suite for **RightSideAlpha** is designed and implemented as an **opaque-box, requirement-driven, deterministic end-to-end verification harness**. It treats the entire web application and API as an external system under test, evaluating behavior strictly against external HTTP contracts, quantitative ground truths, and business requirements defined in `ORIGINAL_REQUEST.md` and `PROJECT.md`.

### Core Testing Tenets:
1. **Opaque-Box Requirement Verification**: Tests interact solely via standard HTTP requests (`GET`, `POST`, `HEAD`, `OPTIONS`) and HTTP responses (status codes, JSON payloads, redirection headers), without inspecting internal database tables, private variables, or backend implementation mechanics.
2. **Deterministic Mathematical Ground Truth**: Expected values are directly derived from authoritative quantitative datasets:
   - `관심종목_백업_20261030/pw_rsi_2000_2026_backtest.json` (26.8-year backtest with 203.87x multiple, 21.97% CAGR, 84 trade records).
   - `관심종목_백업_20261030/all_100_stocks_screened.json` (100-ticker screened universe with moving averages, RSI14, 52W proximity, 10D volume surge).
   - `관심종목_백업_20261030/weekly_picks/` (Institutional 6-section research briefs for MBLY, CELH, etc.).
3. **Progressive Testability & Isolation**: Tests are self-contained and isolated. Each test sets up its own inputs, handles its own tokens/headers, does not depend on execution order, and operates reliably in both live server mode (`http://127.0.0.1:8000`) and in-process TestClient mode.
4. **Monetization & Security Hardening**: Validates that proprietary quantitative signals (MA60 trigger prices, stop-loss levels, 2x target prices, Position Doctor, and TradingView Pine Script v5) remain strictly masked for unauthenticated free visitors and unlock immediately upon valid license verification (specifically supporting demo bypass key `PRO-DEMO-2026`).
5. **Adversarial & Boundary Verification**: Rigorously probes edge conditions including empty queries, SQL/XSS special characters, malformed license keys, zero/negative pricing in financial calculators, and missing authentication headers.

---

## 2. 4-Tier Test Architecture

The E2E test suite is organized into four hierarchical verification tiers in `d:\투자홈페이지\tests_e2e\`:

```
┌────────────────────────────────────────────────────────────────────────┐
│               TIER 4: REAL-WORLD ACCEPTANCE SCENARIOS                  │
│  - Retail investor end-to-end onboarding and conversion workflow       │
│  - Public discovery -> Leaderboard search -> Backtest audit ->         │
│    PRO-DEMO-2026 license entry -> Underwater stock diagnosis via       │
│    Position Doctor -> TradingView referral click -> Pine Script copy   │
│  - Session downgrade & graceful recovery workflows                     │
├────────────────────────────────────────────────────────────────────────┤
│               TIER 3: CROSS-FEATURE INTERACTIONS                       │
│  - Pairwise: Unauthenticated masked -> License valid -> Unmasked data  │
│  - Pairwise: License validation -> Unlocks Pro Vault & Pine Script v5  │
│  - Pairwise: Stock price detail -> Feeds into Position Doctor calc     │
│  - Pairwise: Custom affiliate configuration -> Dynamic referral link   │
│  - Pairwise: Outbound redirect -> Click analytics tracking increment   │
│  - Pairwise: Research brief -> Matches live stock leaderboard ignition │
├────────────────────────────────────────────────────────────────────────┤
│               TIER 2: BOUNDARY & CORNER CASES                          │
│  - Empty & whitespace search strings (`?search=`, `?search=%20%20`)    │
│  - Non-existent ticker lookup (`/api/stocks/NONEXISTENT999` -> 404)    │
│  - Special characters, SQL/XSS injections (`' OR 1=1;--`, `<script>`)   │
│  - Invalid/empty/short/malformed license keys -> valid: false / 422    │
│  - Extreme Position Doctor inputs (zero/negative price, negative days) │
│  - Boundary condition cutoffs (-9.0% stop, 55D day cutoff, +100% TP1)  │
│  - Security headers: Missing or malformed `Authorization: Bearer`      │
│  - Invalid referral providers & parameter boundaries                   │
├────────────────────────────────────────────────────────────────────────┤
│               TIER 1: PRIMARY FEATURES (ISOLATED SPECIFICATIONS)       │
│  - F0: Server startup & health endpoints (`/health`, `/`, `/docs`)     │
│  - F1: Screened stocks API & public masking (100 stocks, masked rows)  │
│  - F2: Backtest & KPI data engine (203.87x multiple, 21.97% CAGR, logs)│
│  - F3: Turnaround research briefs API (`/api/research`, MBLY, CELH)    │
│  - F5: Lemon Squeezy license validation (`PRO-DEMO-2026` bypass)       │
│  - F9/F10: Referral link generation & tracking (TradingView, SA)       │
└────────────────────────────────────────────────────────────────────────┘
```

---

## 3. Feature Inventory & Coverage Matrix

Every feature defined in `PROJECT.md` is mapped to its test tier, test module, and specific test cases:

| Feature # | Feature Name | Test Module | Tier | Test Cases Included | Verification Objective |
|:---:|:---|:---|:---:|:---:|:---|
| **F0** | Server Startup & Health | `test_tier1_features.py` | Tier 1 | 5 | `/health` returns 200 `status: ok`, `/` responds, `/docs` schema accessible, HEAD method supported |
| **F1** | Screened Stocks API & Masking | `test_tier1_features.py`<br>`test_tier2_boundaries.py`<br>`test_tier3_interactions.py` | Tier 1-3 | 18+ | 100 stocks list, public masking for rows >= 4, zone filtering (`IGNITION_ZONE`), sorting, unmasked upon Pro auth |
| **F2** | Backtest & KPI Data Engine | `test_tier1_features.py` | Tier 1 | 6 | 26.8Y summary, 203.87x multiple, 21.97% CAGR, benchmark comparisons (QQQ/SPY), 84 trade logs |
| **F3** | Turnaround Research Briefs | `test_tier1_features.py`<br>`test_tier3_interactions.py` | Tier 1, 3 | 6 | `/api/research` list, MBLY and CELH briefs, structured 6 sections (1:11+ RRR, buy band, TP1 +100%) |
| **F5** | Lemon Squeezy License Validation | `test_tier1_features.py`<br>`test_tier2_boundaries.py` | Tier 1, 2 | 12+ | Demo key `PRO-DEMO-2026` validation, case insensitivity, reject empty/short/invalid keys |
| **F6/F8** | Server Pro Vault & Pine Script | `test_tier1_features.py`<br>`test_tier3_interactions.py` | Tier 1, 3 | 6 | Protected `/api/pro/vault` and `/api/pro/pinescript`, TradingView Pine Script v5 delivery |
| **F7** | Position Doctor Diagnostics | `test_tier2_boundaries.py`<br>`test_tier3_interactions.py`<br>`test_tier4_scenarios.py` | Tier 2-4 | 10+ | 4 exit rules: -9% hard stop, 55D time-stop (< +8%), +100% TP1 half exit, hold status |
| **F9/F10**| Referral Link Building & Clicks | `test_tier1_features.py`<br>`test_tier2_boundaries.py`<br>`test_tier3_interactions.py` | Tier 1-3 | 12+ | Configurable affiliate tags, dynamic link build (`TradingView`, `Seeking Alpha`), 307 redirect & click tracking |
| **F18** | End-to-End User Scenarios | `test_tier4_scenarios.py` | Tier 4 | 4 | Complete retail investor journey from landing to conversion, backtest check, diagnosis, and referral copy |

---

## 4. Directory Layout

```
d:\투자홈페이지\
├── tests_e2e\
│   ├── __init__.py
│   ├── conftest.py               # Shared test client fixture, base URL detection, oracle datasets
│   ├── test_tier1_features.py    # Tier 1: Primary isolated features (>= 5 cases per feature)
│   ├── test_tier2_boundaries.py  # Tier 2: Boundary conditions, empty queries, invalid keys, stress
│   ├── test_tier3_interactions.py# Tier 3: Pairwise cross-feature interactions (Auth->Masking, Config->Link)
│   ├── test_tier4_scenarios.py   # Tier 4: Complete retail investor journey & conversion flows
│   └── run_e2e_tests.py          # Unified CLI & programmatic test runner with formatted ASCII summary
├── TEST_INFRA.md                 # This test infrastructure document
└── TEST_READY.md                 # Test suite readiness & execution report
```

---

## 5. Invocation Commands & Execution Modes

The test suite can be executed in two ways:

### Mode 1: Unified Test Runner (Recommended)
```bash
# Run all tiers against running server (default http://127.0.0.1:8000) or in-process
python tests_e2e/run_e2e_tests.py

# Run specific tier
python tests_e2e/run_e2e_tests.py --tier 1
python tests_e2e/run_e2e_tests.py --tier 2
python tests_e2e/run_e2e_tests.py --tier 3
python tests_e2e/run_e2e_tests.py --tier 4

# Target custom server port or remote URL
python tests_e2e/run_e2e_tests.py --server-url http://127.0.0.1:8080

# Verbose output with detailed assertions
python tests_e2e/run_e2e_tests.py --verbose
```

### Mode 2: Standard Pytest Runner
```bash
# Run entire E2E test suite
pytest tests_e2e/ -v

# Run single tier file
pytest tests_e2e/test_tier1_features.py -v
pytest tests_e2e/test_tier2_boundaries.py -v
pytest tests_e2e/test_tier3_interactions.py -v
pytest tests_e2e/test_tier4_scenarios.py -v

# Run with custom server URL
set SERVER_URL=http://127.0.0.1:8000 && pytest tests_e2e/ -v
```

---

## 6. Expected Output Derivation & Authoritative Sources

All assertions in Tiers 1-4 are derived from explicit, authoritative primary sources:

| Verification Target | Authoritative Source File | Primary Key Assertions |
|:---|:---|:---|
| **Backtest KPIs** | `관심종목_백업_20261030/pw_rsi_2000_2026_backtest.json` | Final Multiple: `203.87x`<br>CAGR: `21.97%`<br>Max Drawdown: `-70.67%`<br>Total Trades: `84`<br>Period: `2000-01-03 ~ 2026-10-13` |
| **Screened Stocks** | `관심종목_백업_20261030/all_100_stocks_screened.json` | 100 stock records.<br>CELH close: `27.93`, low52: `23.56`, high52: `66.74`.<br>APP close: `272.28`, low52: `266.84`.<br>Columns include MA distances, RSI14, volume surges. |
| **Research Briefs** | `관심종목_백업_20261030/weekly_picks/*.md` | MBLY (`2026-10-13_MBLY.md`) & CELH (`2026-09-30_CELH.md`).<br>Required sections: Moat, Wash-out, Consensus, 1-2Y 2x Roadmap. |
| **License Bypass** | `ORIGINAL_REQUEST.md` & `PROJECT.md` | Demo key `PRO-DEMO-2026` must return `valid: True` and unmask Pro features. |
| **Position Doctor** | `ORIGINAL_REQUEST.md` & `PROJECT.md` | Rule 1: Return <= -9.0% -> Exit immediately.<br>Rule 2: Held >= 55 days & Return < +8.0% -> Dead money exit.<br>Rule 3: Return >= +100.0% -> Sell 50% TP1.<br>Rule 4: Normal hold status with dollar levels. |
| **Referral URLs** | `PROJECT.md` § Interface Contracts | TradingView format: `https://www.tradingview.com/symbols/{ticker}/?aff_id={aff_id}`.<br>Seeking Alpha format: `https://seekingalpha.com/symbol/{ticker}/earnings?source={source}`. |
