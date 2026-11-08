# GetBreakAI (`getbreakai.com`)

> Institutional-Grade AI Quantitative Breakout Detection & Asymmetric Risk Management SaaS.

[![Node.js CI](https://img.shields.io/badge/Node.js-18%2B-brightgreen)](https://nodejs.org/)
[![License](https://img.shields.io/badge/License-Proprietary-red)]()
[![Store](https://img.shields.io/badge/LemonSqueezy-Store%20%23296100-blue)](https://lemonsqueezy.com)
[![Support](https://img.shields.io/badge/Support-beable9489%40gmail.com-orange)](mailto:beable9489@gmail.com)

---

## 1. Overview

GetBreakAI is an institutional SaaS platform designed to eliminate the retail trader failure loop (left-side knife catching, emotional holding of losing trades, and premature selling of winners) by automating asymmetric risk rules and high-volume breakout detection.

### Core Mathematical Disciplines
- **PW-RSI (Price-Weighted RSI)**: Multiplies RSI momentum by institutional volume accumulation to detect true right-side market breakouts.
- **Strict -9.0% Hard Stop-Loss**: Every position is mechanically exited at -9.0% from entry price. Zero discretionary exceptions.
- **Dynamic 2x Take-Profit (Minimum 2:1 R:R)**: Targets at least +18.0% before initial profit taking, with trailing stops moving to breakeven after +15.0%.

---

## 2. Directory Layout

```
getbreakai/
├── ARCHITECTURE.md          # Complete quant & engineering specifications
├── README.md                # Project quick-start & overview
├── package.json             # Scripts & metadata
├── index.html               # Landing wireframe & live interactive breakout simulator
├── src/
│   ├── engine/
│   │   └── breakout_engine.js   # Genuine quant math engine (PW-RSI, Stop/TP, Breakouts)
│   └── services/
│       └── lemonsqueezy.js      # Checkout generator & HMAC webhook verification
└── tests/
    └── breakout_engine.test.js  # Mathematical unit & stress test suite
```

---

## 3. Quick Start

### Run Unit Tests
Verify mathematical calculations, risk triggers, and signal detection (15 tests):
```bash
npm test
```

### Run Adversarial HMAC Security Tests
Verify Lemon Squeezy webhook signature verification under adversarial attacks (12 tests):
```bash
npm run test:adversarial
# Or: node tests/adversarial_lemonsqueezy_hmac.test.js
```

### Run All Test Suites (27/27 Total)
```bash
npm run test:all
```

### Run Synthetic Engine Benchmark
```bash
npm start
```

---

## 4. Monetization & Checkout Integration
Operates under Lemon Squeezy Store `#296100` (`KIDS-FIT Global Studio` / `TruthOfMarket Analytics` / `GetBreakAI`):
- **Starter Scanner**: `$29 / mo`
- **Pro Breakout**: `$49 / mo` (or `$399 / yr`)
- **Institutional Alpha**: `$199 / mo` (or `$1,499 / yr`)

For billing inquiries, contact the unified desk at `beable9489@gmail.com`.

---

## 5. Safe Harbor Legal Notice
GetBreakAI is automated financial technology software and an analytical tool, not a registered investment advisor, broker, or financial planner. Past breakout performance does not guarantee future results.
