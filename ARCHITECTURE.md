# GetBreakAI Architecture & Engineering Specification

- **System Name**: GetBreakAI (`getbreakai.com`)
- **Version**: 1.0.0-PROD-SPEC
- **Document Status**: Authoritative Engineering Design
- **Target Market**: Global Institutional & Retail Momentum Traders (USD SaaS)
- **Store / Merchant of Record**: Lemon Squeezy Store ID `#296100` (`KIDS-FIT Global Studio` / `TruthOfMarket Analytics` / `GetBreakAI`)
- **Official Contact**: `beable9489@gmail.com`

---

## 1. Executive Summary & Value Proposition

GetBreakAI (`getbreakai.com`) is an institutional-grade, AI-driven quantitative market breakout detection and risk management SaaS platform. 

### 1.1 The Retail Trader Failure Loop
Over 90% of retail equity and crypto traders consistently lose capital due to three cognitive flaws:
1. **Left-Side Knife Catching**: Buying into steep downtrends under the illusion that "it cannot fall further", suffering massive tail drawdowns (-70% to -90%).
2. **The Disposition Effect**: Selling winners prematurely at +5% to feel good, while bag-holding losing positions down to -40%, destroying risk-adjusted returns.
3. **Subjective Emotion & Absence of Fixed Stops**: Lacking algorithmic discipline, refusing to accept losses until margin calls occur.

### 1.2 The GetBreakAI Algorithmic Solution
GetBreakAI completely removes human emotion from trade execution:
- **Price-Weighted RSI (PW-RSI) & MA60 Right Ignition**: Signals trigger ONLY when a stock reclaims its 60-day moving average on institutional volume expansion (>1.5x 20-day average volume).
- **Mandatory Non-Negotiable -9.0% Hard Stop**: Maximum downside is strictly capped at -9.0% from entry. Zero exceptions.
- **Dynamic 2x Take-Profit Target (18% - 100%)**: Enforces a minimum 2:1 Reward-to-Risk ratio (R:R), with trailing breakeven activation once gain exceeds +15.0%.

---

## 2. Quantitative Engine Specifications

```
                     ┌──────────────────────────────────────┐
                     │ Raw Market Feed (Polygon / Alpaca)    │
                     │ High-frequency Daily/Hourly OHLCV    │
                     └──────────────────┬───────────────────┘
                                        │
                                        ▼
                     ┌──────────────────────────────────────┐
                     │ Breakout Detection & Filter Engine   │
                     │ • Donchian 20/55 Channel Highs       │
                     │ • ATR Volatility Expansion Ratio     │
                     │ • Volume Multiplier >= 1.5x MA20_Vol │
                     └──────────────────┬───────────────────┘
                                        │
                                        ▼
                     ┌──────────────────────────────────────┐
                     │ PW-RSI Ignition Scorer               │
                     │ • PW_RSI = RSI * (Vol / MA20_Vol)    │
                     │ • MA60 Slope > 0 & Close > MA60      │
                     └──────────────────┬───────────────────┘
                                        │
                                        ▼
                     ┌──────────────────────────────────────┐
                     │ Risk & Execution State Machine       │
                     │ • Entry: Confirmed Breakout Close    │
                     │ • Hard Stop: Entry * 0.910 (-9.0%)   │
                     │ • Trailing BE: Triggered at +15.0%   │
                     │ • 2x Target: Minimum +18.0% (2:1 R:R)│
                     └──────────────────┬───────────────────┘
                                        │
                         ┌──────────────┴──────────────┐
                         ▼                             ▼
              [Live Webhook / Telegram]     [Interactive Terminal]
```

### 2.1 Mathematical Formulas & Algorithmic Definitions

#### A. Donchian 20/55 Channel Breakout
A breakout signal candidate occurs when the current price exceeds the upper Donchian channel:
$$\text{UpperChannel}_{N}(t) = \max_{1 \le i \le N} (\text{High}_{t-i})$$
A primary trigger requires:
$$\text{Close}_{t} > \text{UpperChannel}_{20}(t) \quad \text{and} \quad \text{Close}_{t} > \text{SMA}_{60}(t)$$

#### B. Volume-Weighted Ignition & PW-RSI
Standard RSI measures only price velocity. **PW-RSI (Price-Weighted RSI)** multiplies directional momentum by institutional volume accumulation:
$$\text{VolFactor}(t) = \frac{\text{Volume}_{t}}{\frac{1}{20} \sum_{k=0}^{19} \text{Volume}_{t-k}}$$
$$\text{PW-RSI}_{14}(t) = \text{RSI}_{14}(t) \times \min(\text{VolFactor}(t), 3.0)$$
- **Ignition Threshold**: A breakout is deemed an **Institutional Ignition** when $\text{PW-RSI}_{14} \ge 90.0$ and $\text{VolFactor} \ge 1.5$.
- **False-Breakout Filter**: If $\text{Close}_{t} > \text{UpperChannel}$ but $\text{VolFactor} < 1.0$, the breakout is flagged as *Low-Volume Bull Trap* and suppressed.

#### C. Asymmetric Risk Formulation (-9% Stop / 2x Take-Profit)
1. **Initial Stop-Loss**:
   $$\text{StopLoss}_{\text{initial}} = \text{EntryPrice} \times (1 - 0.090) = \text{EntryPrice} \times 0.910$$
2. **Initial Minimum Take-Profit (2:1 R:R)**:
   $$\text{RiskAmount} = \text{EntryPrice} - \text{StopLoss}_{\text{initial}} = 0.090 \times \text{EntryPrice}$$
   $$\text{TargetPrice}_{\text{min}} = \text{EntryPrice} + (2.0 \times \text{RiskAmount}) = \text{EntryPrice} \times 1.180 \ (+18.0\%)$$
3. **Dynamic Breakeven & Trailing Escalation**:
   - When $\text{High}_{t} \ge \text{EntryPrice} \times 1.150$ (+15% gain): Stop-loss escalates to $\text{EntryPrice} \times 1.010$ (guaranteed +1.0% net profit covering trading fees).
   - When $\text{High}_{t} \ge \text{TargetPrice}_{\text{min}}$: Half position (50%) is liquidated to lock in 2x profit, and remainder trails $\text{SMA}_{20}$ until closed.

---

## 3. Lemon Squeezy USD SaaS Subscription Integration

GetBreakAI operates as a high-margin digital SaaS using Lemon Squeezy as Merchant of Record (MoR), completely abstracting global sales tax, VAT/GST, chargebacks, and multi-currency conversion.

### 3.1 Store & Product Architecture
- **Lemon Squeezy Store ID**: `#296100` (`KIDS-FIT Global Studio` / `TruthOfMarket Analytics` / `GetBreakAI`)
- **Checkout Host**: `https://truthofmarket.lemonsqueezy.com` (or custom domain `https://billing.getbreakai.com`)

| Plan Tier | Price (USD) | Billing Interval | Target Audience | Key Features Included |
| :--- | :--- | :--- | :--- | :--- |
| **Starter Scanner** | **$29 / mo** | Monthly Recurring | Retail Part-Time Traders | • Daily Top 10 Breakout Scanner<br>• -9% Stop-Loss Calculator<br>• EOD Watchlist CSV Download |
| **Pro Breakout** | **$49 / mo** | Monthly Recurring (or $399/yr, 32% off) | Active Momentum Traders | • Real-time Intraday Ignition Alerts<br>• PW-RSI Volume Accumulation Engine<br>• Direct Telegram VIP Signal Webhook<br>• Pine Script v5 Indicator Source Code |
| **Institutional Alpha** | **$199 / mo** | Monthly Recurring (or $1,499/yr) | Family Offices / Quant Funds | • Full REST/WebSocket API Access<br>• SEC 10-K Forensic Risk NLP Feed<br>• Dark-Pool Flow Order Imbalance Metrics<br>• Dedicated Priority Slack/Telegram Room |

### 3.2 Secure Webhook Architecture
All subscription events are validated using HMAC-SHA256 signature verification.

```javascript
// Webhook Signature Verification Spec
const crypto = require('crypto');

function verifyLemonSqueezySignature(rawBody, signatureHeader, secret) {
  const hmac = crypto.createHmac('sha256', secret);
  const digest = Buffer.from(hmac.update(rawBody).digest('hex'), 'utf8');
  const signature = Buffer.from(signatureHeader || '', 'utf8');
  
  if (digest.length !== signature.length) return false;
  return crypto.timingSafeEqual(digest, signature);
}
```

#### Monitored Webhook Events:
1. `subscription_created`: Provision user account, generate API keys, grant VIP Telegram access.
2. `subscription_updated`: Handle plan upgrades/downgrades dynamically.
3. `subscription_cancelled`: Set grace period until end of billing cycle.
4. `subscription_payment_failed`: Send automated dunning email and warning via Telegram.

---

## 4. Technical Stack & System Architecture

```
┌────────────────────────────────────────────────────────┐
│ Frontend: Cloudflare Pages / Static Edge CDN           │
│ • Pure HTML5 / Modern ES6 Modules / Tailwind CSS       │
│ • TradingView Lightweight Charts (v4.1)                │
│ • Lemon Squeezy Checkout.js Overlay Integration        │
└──────────────────────────┬─────────────────────────────┘
                           │ HTTPS / WSS
                           ▼
┌────────────────────────────────────────────────────────┐
│ Edge API & Backend: Node.js / Cloudflare Workers       │
│ • Fastify / Express / Worker microservices             │
│ • JWT Authentication & Subscription Entitlement Check   │
│ • Rate Limiting & Cloudflare Turnstile bot protection   │
└──────────────────────────┬─────────────────────────────┘
                           │
             ┌─────────────┴─────────────┐
             ▼                           ▼
┌──────────────────────────┐┌──────────────────────────┐
│ Data & Quant Workers     ││ Storage & Cache          │
│ • Polygon/Alpaca Feeds   ││ • PostgreSQL (Supabase)  │
│ • Breakout Math Engine   ││ • Cloudflare D1 / KV     │
│ • PW-RSI Calculation     ││ • Redis Real-time PubSub │
└──────────────────────────┘└──────────────────────────┘
```

### 4.1 Frontend Architecture
- **Zero Heavy Framework Lock-In**: Built with lightweight, deterministic Vanilla JS / Vite to achieve a Google PageSpeed score of 98+ and sub-200ms First Contentful Paint (FCP).
- **Interactive Charting**: TradingView Lightweight Charts (`lightweight-charts`) provides ultra-responsive, mobile-friendly 60fps candlestick charting with custom overlays for the -9% stop band and 2x profit target box.
- **Brand Aesthetic**: High-contrast, dark-mode institutional aesthetic (#0a0e17 background, cyan/emerald signals, crimson risk stops) matching Bloomberg/Refinitiv ergonomics.

### 4.2 Backend & Data Pipelines
- **Data Ingestion**: Scheduled daily and intraday batch ingestion of S&P 500, Nasdaq 100, and high-beta momentum equities (e.g., SMH, NVDA, PLTR, TSM).
- **Quant Calculation Worker**: Distributed calculation of Donchian bands, ATR(14), RSI(14), and PW-RSI. Signals are cached in Redis and pushed via SSE (Server-Sent Events) or WebSockets to active clients.

---

## 5. Deployment, Security & Monitoring Architecture

### 5.1 Infrastructure Layout
- **Domain**: `getbreakai.com` managed via Cloudflare DNS with Full (Strict) SSL/TLS.
- **Hosting**: Cloudflare Pages for the static front-end; Cloudflare Workers / Fly.io for the API backend.
- **Global Latency**: Average API response < 45ms across North America, Europe, and Asia-Pacific.

### 5.2 Security & Compliance Guardrails
- **No Financial Advice Disclaimer**: Explicit FTC / SEC / FINRA safe-harbor legal notices rendered on every page:
  > *"GetBreakAI is an automated financial technology software and analytical tool, not a registered investment advisor, broker, or financial planner. Past breakout performance does not guarantee future results."*
- **Contact Desk Unification**: Official support desk unified to `beable9489@gmail.com`.
- **Payment Security**: PCI-DSS Level 1 compliance completely offloaded to Lemon Squeezy. No credit card or billing credentials ever touch GetBreakAI infrastructure.

### 5.3 Automated Heartbeat & Telegram Alerting
- Edge synthetic monitor probes `/api/health` every 60 seconds.
- Any downtime or API failure triggers immediate notification to the headquarters Telegram bot (`@SemifearGreedbot`) and Dream Company master room (`-1003834697086`).
