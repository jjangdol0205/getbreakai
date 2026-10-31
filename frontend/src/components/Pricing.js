export function renderPricing(state) {
  const cfg = state.config || {};
  const lsMonthly =
    cfg.ls_site1_monthly_url ||
    "https://rightsidealpha.lemonsqueezy.com/checkout/buy/pro-monthly";
  const lsLtd =
    cfg.ls_site1_ltd_url ||
    "https://rightsidealpha.lemonsqueezy.com/checkout/buy/lifetime-pass";

  return `
    <section class="pricing-grid" id="pricingSection">
      <!-- Tier 1: Pro Monthly -->
      <div class="price-card featured">
        <div>
          <span class="badge badge-ignition">INSTITUTIONAL PRO</span>
          <h3 style="font-size:1.12rem; font-weight:800; margin-top:10px; color:#ffffff;">
            Pro Quantitative Terminal & Daily SEC Brief
          </h3>
          <div class="price-num">$29 <span style="font-size:0.82rem; color:var(--muted); font-family:var(--font-sans); font-weight:500;">/ month</span></div>
          <ul class="price-list">
            <li><span>—</span> <span>Unmask all 72 US Equity PW-RSI Scores, MA60 Breakout Triggers & -9% Stop Levels</span></li>
            <li><span>—</span> <span>Daily 08:10 EST Primary-Filing (10-K/10-Q/8-K) Turnaround Research Digest</span></li>
            <li><span>—</span> <span>Position Risk & 55-Day Time-Stop Diagnostic Engine</span></li>
            <li><span>—</span> <span>Full TradingView Pine Script v5 Indicator Source Code + SemiFearGreed 26Y CSV</span></li>
          </ul>
        </div>
        <a class="btn btn-primary lemonsqueezy-button" id="cardMonthlyBtn" href="${lsMonthly}?embed=1" style="justify-content:center; padding:10px;">
          Subscribe via Lemon Squeezy ($29/mo)
        </a>
      </div>

      <!-- Tier 2: Lifetime Pass -->
      <div class="price-card">
        <div>
          <span class="badge badge-watch">FOUNDER ALLOCATION</span>
          <h3 style="font-size:1.12rem; font-weight:800; margin-top:10px; color:#ffffff;">
            Lifetime Research & Terminal License
          </h3>
          <div class="price-num">$199 <span style="font-size:0.82rem; color:var(--muted); font-family:var(--font-sans); font-weight:500;">/ one-time</span></div>
          <ul class="price-list">
            <li><span>—</span> <span>Permanent License Key — Zero recurring monthly subscription charges</span></li>
            <li><span>—</span> <span>Complete 26.8-Year (2000–2026) US Equity & Semiconductor ETF Backtest Datasets</span></li>
            <li><span>—</span> <span>Multilingual Access (English, Japanese & Korean SEC Research Briefs)</span></li>
            <li><span>—</span> <span>Full Access to both RightSideAlpha and SemiFearGreed Pro Features</span></li>
          </ul>
        </div>
        <a class="btn btn-emerald lemonsqueezy-button" id="cardLtdBtn" href="${lsLtd}?embed=1" style="justify-content:center; padding:10px;">
          Acquire Lifetime License ($199)
        </a>
      </div>

      <!-- Tier 3: Institutional Charting & Fundamental Partners -->
      <div class="price-card">
        <div>
          <span class="badge" style="background:rgba(41,98,255,0.14); color:#93c5fd; border:1px solid rgba(41,98,255,0.3);">EXECUTION & DATA PARTNERS</span>
          <h3 style="font-size:1.12rem; font-weight:800; margin-top:10px; color:#ffffff;">
            Direct Charting & Consensus EPS Verification
          </h3>
          <p style="color:var(--muted); font-size:0.8rem; margin-top:8px; line-height:1.5;">
            Verify MA20/MA60 volume breakouts and forward EPS revisions on institutional charting and consensus platforms:
          </p>
          <ul class="price-list">
            <li><span>—</span> <span><b>TradingView Pro</b> — Multi-timeframe MA20/MA60 & Pine Script v5 execution</span></li>
            <li><span>—</span> <span><b>Seeking Alpha Premium</b> — Quant Grades & 1-2Y consensus EPS revision tracking</span></li>
            <li><span>—</span> <span><b>Interactive Brokers (IBKR)</b> — Direct NYSE/NASDAQ routing & institutional FX rates</span></li>
          </ul>
        </div>
        <div style="display:flex; flex-direction:column; gap:8px;">
          <a class="btn" id="affTvBtn" href="/api/referral/redirect/tradingview?ticker=SPY" target="_blank" rel="noopener noreferrer" style="justify-content:center;">
            Launch TradingView Terminal ↗
          </a>
          <a class="btn" id="affSaBtn" href="/api/referral/redirect/seekingalpha?ticker=SPY" target="_blank" rel="noopener noreferrer" style="justify-content:center;">
            Open Seeking Alpha EPS Consensus ↗
          </a>
        </div>
      </div>
    </section>
  `;
}
