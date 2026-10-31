# Project: 미국 52주 신저가 턴어라운드 정밀 스크리닝 및 주간 Top-Pick 심층 분석/아카이빙 시스템 (Weekly Turnaround Screener System)

## Architecture
A 100% offline, zero-external-dependency financial architecture extending the personal investment processing hub with:
1. **US 52-Week Low Turnaround Screener Engine** (`engine/turnaround_screener.py`):
   - Quantitative evaluation of 4 cross-validated turnaround conditions:
     (1) **52-Week Low Proximity**: Price within 10%~20% of 52-week low ($P \le L_{52} \times 1.20$, deep-value safety margin).
     (2) **1~2 Year Earnings Turnaround Visibility**: Consensus/guidance showing Revenue or Operating Income growing $\ge 30\%$ over 1~2 years or swinging from loss to substantial profit (흑자 전환).
     (3) **Volume Wash-Out & Support Rebound**: Panic selling volume surge $\ge 1.4\text{x}$ benchmark, defense of key support floor, and green rebound candle ($\Delta P \ge 0.0\%$).
     (4) **Asymmetric Risk/Reward Ratio**: Downside risk to support floor $\le 10\%$ vs 1~2 year TP1 2x upside $\ge +100\%$ ($RRR \ge 10.0\text{x}$).
   - Multi-factor composite scoring model (0~100 pts) evaluating conviction tiers: `TOP_PICK`, `STRONG_CANDIDATE`, `WATCHLIST`, `DISQUALIFIED`.
2. **Weekly Top-Pick Selection & Deep-Dive Report Engine** (`engine/turnaround_screener.py`, `engine/sync_dashboard.py`, `engine/cli.py`):
   - Objective selection of the single #1 Top-Pick winner based on composite score, RRR, catalyst urgency, and market cap.
   - Institutional-grade deep-dive report generator creating `weekly_picks/YYYY-MM-DD_<ticker>.md`:
     * Section 1: 비즈니스 모델 및 시장 지배력 (Business Model & Moat)
     * Section 2: 52주 신저가 추락 원인 정밀 해부 (Root Cause of 52-Week Low Fall)
     * Section 3: 1~2년 실적 턴어라운드 핵심 동인 (1~2Y Turnaround Drivers & Catalysts)
     * Section 4: 타점 진단 & 1~2년 2배(+100%) 로드맵 (Valuation, Timing & 2x Roadmap)
     * Section 5: 기존 보유 포트폴리오(SK스퀘어 76주)와의 전술적 스위칭 적합도 평가 (Tactical Switching Suitability)
     * Section 6: 주간 모니터링 체크리스트 및 결론 (Weekly Checklist & Conclusion)
   - Idempotent archiving into `data.js` under `window.WATCHLIST_DATA.weeklyScreener` (`currentPick`, `candidates`, `history`).
   - Unified CLI command: `python -m engine.cli weekly_pick` and automatic hook inside `python -m engine.cli sync`.
3. **Dedicated Offline Dashboard View 6 & Archive UI** (`index.html`):
   - Navigation button `btnViewTurnaround`: `<span>💎</span> 금주의 턴어라운드 Pick`.
   - Dedicated View 6 container (`viewTurnaroundSection`) with 32 contracted DOM IDs:
     * Top Turnaround 4-Tile KPI Ribbon (`#turnaroundKpiRibbon`)
     * Top-Pick Showcase Hero Card (`#turnaroundShowcaseCard`)
     * 52-Week Position SVG Gauge with 10%~20% Sweet Spot zone and dynamic pointer pin
     * Asymmetric Risk/Reward Profile Split Bar (-10% downside vs +100% TP1 upside)
     * Catalyst D-Day Countdown and Volume Wash-Out Badges
     * Candidates Comparison Matrix Card (`#turnaroundCandidatesCard`)
     * Historical Weekly Recommendations Archive Table (`#turnaroundArchiveCard`) with real-time return tracking
   - 100% Zero-CDN offline self-containment (`file:///` compatible, 0 remote scripts/fonts/icons/urls).
4. **Comprehensive 4-Tier + DOM Audit Test Suite** (`tests/test_weekly_turnaround_screener.py`):
   - Tier 1 Feature Coverage (16 tests), Tier 2 Boundary Value Analysis (18 tests), Tier 3 Cross-Feature (10 tests), Tier 4 Real-World Workloads (8 tests), Tier 5 DOM Contracts & Offline Audit (8 tests). Total 60 new tests + existing 689 tests = ~749 tests, 100% PASS.

## Feature Inventory
| # | Feature | Description | Milestone | Source |
|---|---------|-------------|-----------|--------|
| 1 | 52-Week Low Proximity Filter (C1) | Quantitative filter verifying current price is within 10%~20% from 52-week low | M1 | Survey (R1) |
| 2 | 1~2 Year Earnings Turnaround Filter (C2) | Multi-year consensus growth evaluation verifying Revenue/Operating Income $\ge 30\%$ or loss-to-profit inflection | M1 | Survey (R1) |
| 3 | Volume Wash-Out & Support Rebound Filter (C3) | Evaluates volume surge $\ge 1.4\text{x}$ benchmark, defense of key support floor, and green rebound candle | M1 | Survey (R1) |
| 4 | Asymmetric Risk/Reward Ratio Filter (C4) | Evaluates downside risk $\le 10\%$ vs 1~2 year TP1 upside $\ge +100\%$ ($RRR \ge 10.0\text{x}$) | M1 | Survey (R1) |
| 5 | Multi-Factor Composite Scoring & Ranking | 100-point composite scoring formula and conviction tiers (`TOP_PICK`, `STRONG_CANDIDATE`, `WATCHLIST`) | M1 | Survey (R1, R2) |
| 6 | Objective Top-Pick Single Winner Selection | Deterministic selection algorithm picking the #1 single best turnaround stock | M2 | Survey (R2) |
| 7 | Institutional Deep-Dive Report Generator | Generates 6-section research report saved to `weekly_picks/YYYY-MM-DD_<ticker>.md` | M2 | Survey (R2) |
| 8 | SK Square 76 Shares Switching Suitability | Evaluates tactical switching vs user's core holding (8,284만 원, 109만 원 평단) and enforces reverse-switching defense | M2 | Survey (R2) |
| 9 | `data.js` `weeklyScreener` Store Persistence | Idempotent serialization into `window.WATCHLIST_DATA.weeklyScreener` (`currentPick`, `candidates`, `history`) | M2 | Survey (R2) |
| 10 | CLI Subcommand & Automated Sync Pipeline Hook | Adds `weekly_pick` subcommand to `engine/cli.py` and auto-evaluates during `sync` | M2 | Survey (R2) |
| 11 | Dashboard Dedicated View 6 & Nav Switcher | Adds `btnViewTurnaround` and `viewTurnaroundSection` with 32 contracted DOM IDs | M3 | Survey (R3) |
| 12 | 52-Week Range SVG Gauge & Sweet Spot Visualizer | Inline SVG gauge highlighting 10%~20% sweet spot with dynamic pointer pin | M3 | Survey (R3) |
| 13 | Asymmetric Risk/Reward Split Visual Bar | Dual-split horizontal bar displaying -10% downside vs +100% TP1 upside | M3 | Survey (R3) |
| 14 | Historical Recommendations Return Tracking Archive | Chronological table tracking recommendation price vs current price, return %, and status | M3 | Survey (R3) |
| 15 | Comprehensive 5-Tier E2E Test Suite | 60 new tests in `tests/test_weekly_turnaround_screener.py` covering Tiers 1-5 | M4 | Survey (AC) |
| 16 | Zero-CDN Offline & Full Regression Integrity | 0 CDN dependencies, 100% pass across all 749+ test cases | M4 | Survey (AC) |

## Milestones
| # | Name | Scope | Dependencies | Status |
|---|------|-------|-------------|--------|
| Phase 0 | Survey & Architecture Specification | Codebase inspection, 4-condition math formulation, data store schema, DOM ID contract, 3 Explorer reports | none | DONE |
| M1 | US 52-Week Low Turnaround Screener Engine (R1) | `engine/turnaround_screener.py`, `tests/test_turnaround_screener.py` (Filters C1~C4, Candidate scoring, Universe screening) | Phase 0 | DONE |
| M2 | Weekly Top-Pick Deep-Dive Report & Data Archiving (R2) | `engine/turnaround_screener.py`, `engine/sync_dashboard.py`, `engine/cli.py`, `weekly_picks/`, `data.js` | M1 | DONE |
| M3 | Dashboard Dedicated View 6 UI & Historical Archive (R3) | `index.html` (View 6, 32 DOM IDs, 52W SVG gauge, RRR bar, Archive table, Zero-CDN) | M2 | DONE |
| M4 | Final Milestone: Comprehensive Test Suite & Adversarial Audit (AC) | `tests/test_weekly_turnaround_screener.py`, full regression pass (835 tests), Forensic Integrity Audit | M1, M2, M3 | DONE |

## Interface Contracts
### Turnaround Screener -> Sync Module & data.js
- Function: `TurnaroundScreener.run_weekly_screener(date: str = "YYYY-MM-DD", universe: Optional[List[str]] = None) -> WeeklyScreenerSnapshot`
- Output Schema in `data.js` (`window.WATCHLIST_DATA.weeklyScreener`):
  ```javascript
  {
    "lastEvaluated": "YYYY-MM-DD",
    "status": "ACTIVE",
    "currentPick": {
      "stockId": "MBLY",
      "ticker": "MBLY",
      "nameKr": "모빌아이",
      "currentPrice": 7.47,
      "fiftyTwoWeekLow": 6.47,
      "fiftyTwoWeekHigh": 34.50,
      "proximityTo52wLowPct": 15.46,
      "supportPrice": 6.87,
      "downsideRiskPct": -8.03,
      "tp1Price": 15.00,
      "upsideTp1Pct": 100.80,
      "riskRewardRatio": 12.55,
      "compositeScore": 90.0,
      "convictionLevel": "TOP_PICK",
      "primaryCatalyst": { "name": "...", "dDay": 21 },
      "volumeWashoutConfirmed": true,
      "switchingEvaluation": { "action": "HOLD_CORE_AND_BUY_SEPARATE", ... },
      "markdownPath": "weekly_picks/YYYY-MM-DD_MBLY.md"
    },
    "candidates": [ ... ],
    "history": [ ... ]
  }
  ```

### CLI -> Turnaround Screener
- Command: `python -m engine.cli weekly_pick [-i <dump.txt>] [-d <YYYY-MM-DD>] [--sync] [--json]`
- Hook in `cmd_sync`: Automatically executes `run_weekly_screener()` and passes payload into `sync_to_dashboard()`.

## Code Layout
- `engine/`:
  - `turnaround_screener.py` (NEW in M1/M2: Screener filters, candidate scoring, Top-Pick selection, deep-dive report generator)
  - `models.py` (stock models & masters)
  - `finance_feed.py` (verified 52-week ranges & quotes)
  - `timing_engine.py` (support floors, valuation bands, TP1 rules)
  - `sync_dashboard.py` (updates `data.js` with `weeklyScreener`)
  - `cli.py` (CLI subcommands & unified pipeline)
- `weekly_picks/`:
  - `YYYY-MM-DD_<ticker>.md` (NEW in M2: institutional-grade markdown reports)
- `tests/`:
  - `test_turnaround_screener.py` (NEW in M1: unit tests for 4 filters & scoring)
  - `test_weekly_turnaround_screener.py` (NEW in M4: 60-test E2E test suite across Tiers 1-5)
  - 40 existing test modules (689 tests baseline)
- `index.html`: Dedicated View 6 (`viewTurnaroundSection`, 32 DOM IDs, Zero-CDN)
- `data.js`: `weeklyScreener` store
