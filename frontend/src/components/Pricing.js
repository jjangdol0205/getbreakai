const formatLsUrl = (u) =>
  !u ? "#" : u.includes("?") ? (u.includes("embed=1") ? u : `${u}&embed=1`) : `${u}?embed=1`;

export function renderPricing(state) {
  const cfg = state.config || {};
  const tp = state.t?.pricing || {};
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
          <span class="badge badge-ignition">${tp.t1Badge || "INSTITUTIONAL PRO"}</span>
          <h3 style="font-size:1.12rem; font-weight:800; margin-top:10px; color:#ffffff;">
            ${tp.t1Title || "Pro Quantitative Terminal & Daily SEC Brief"}
          </h3>
          <div class="price-num">$29 <span style="font-size:0.82rem; color:var(--muted); font-family:var(--font-sans); font-weight:500;">${tp.t1Period || "/ month"}</span></div>
          <ul class="price-list">
            <li><span>—</span> <span>${tp.t1Feat1 || "Unmask all 72 US Equity PW-RSI Scores, MA20/60 Breakout Triggers & -9% Stop Levels"}</span></li>
            <li><span>—</span> <span>${tp.t1Feat2 || "Daily 08:10 EST Primary-Filing (10-K/10-Q/8-K) Turnaround Research Digest"}</span></li>
            <li><span>—</span> <span>${tp.t1Feat3 || "Position Risk & 55-Day Time-Stop Diagnostic Engine"}</span></li>
            <li><span>—</span> <span>${tp.t1Feat4 || "Full TradingView Pine Script v5 Indicator Source Code + SemiFearGreed 26Y CSV"}</span></li>
          </ul>
        </div>
        <a class="btn btn-primary lemonsqueezy-button" id="cardMonthlyBtn" data-plan="monthly" href="${formatLsUrl(lsMonthly)}" style="justify-content:center; padding:10px;">
          ${tp.t1Btn || "Subscribe via Lemon Squeezy ($29/mo)"}
        </a>
      </div>

      <!-- Tier 2: Lifetime Pass -->
      <div class="price-card">
        <div>
          <span class="badge badge-watch">${tp.t2Badge || "FOUNDER ALLOCATION"}</span>
          <h3 style="font-size:1.12rem; font-weight:800; margin-top:10px; color:#ffffff;">
            ${tp.t2Title || "Lifetime Research & Terminal License"}
          </h3>
          <div class="price-num">$199 <span style="font-size:0.82rem; color:var(--muted); font-family:var(--font-sans); font-weight:500;">${tp.t2Period || "/ one-time"}</span></div>
          <ul class="price-list">
            <li><span>—</span> <span>${tp.t2Feat1 || "Permanent License Key — Zero recurring monthly subscription charges"}</span></li>
            <li><span>—</span> <span>${tp.t2Feat2 || "Complete 26.8-Year (2000–2026) US Equity & Semiconductor ETF Backtest Datasets"}</span></li>
            <li><span>—</span> <span>${tp.t2Feat3 || "Multilingual Access (English, Japanese & Korean SEC Research Briefs)"}</span></li>
            <li><span>—</span> <span>${tp.t2Feat4 || "Full Access to both RightSideAlpha and SemiFearGreed Pro Features"}</span></li>
          </ul>
        </div>
        <a class="btn btn-emerald lemonsqueezy-button" id="cardLtdBtn" data-plan="lifetime" href="${formatLsUrl(lsLtd)}" style="justify-content:center; padding:10px;">
          ${tp.t2Btn || "Acquire Lifetime License ($199)"}
        </a>
      </div>

      <!-- Tier 3: Institutional Charting & Fundamental Partners -->
      <div class="price-card">
        <div>
          <span class="badge" style="background:rgba(41,98,255,0.14); color:#93c5fd; border:1px solid rgba(41,98,255,0.3);">${tp.t3Badge || "EXECUTION & DATA PARTNERS"}</span>
          <h3 style="font-size:1.12rem; font-weight:800; margin-top:10px; color:#ffffff;">
            ${tp.t3Title || "Direct Charting & Consensus EPS Verification"}
          </h3>
          <p style="color:var(--muted); font-size:0.8rem; margin-top:8px; line-height:1.5;">
            ${tp.t3Desc || "Verify MA20/MA60 volume breakouts and forward EPS revisions on institutional charting and consensus platforms:"}
          </p>
          <ul class="price-list">
            <li><span>—</span> <span><b>TradingView Pro</b> — Multi-timeframe MA20/MA60 & Pine Script v5 execution</span></li>
            <li><span>—</span> <span><b>Seeking Alpha Premium</b> — Quant Grades & 1-2Y consensus EPS revision tracking</span></li>
            <li><span>—</span> <span><b>Interactive Brokers (IBKR)</b> — Direct NYSE/NASDAQ routing & institutional FX rates</span></li>
          </ul>
        </div>
        <div style="display:flex; flex-direction:column; gap:8px;">
          <a class="btn" id="affTvBtn" href="/api/referral/redirect/tradingview?ticker=SPY" target="_blank" rel="noopener noreferrer" style="justify-content:center;">
            ${tp.t3TvBtn || "Launch TradingView Terminal ↗"}
          </a>
          <a class="btn" id="affSaBtn" href="/api/referral/redirect/seekingalpha?ticker=SPY" target="_blank" rel="noopener noreferrer" style="justify-content:center;">
            ${tp.t3SaBtn || "Open Seeking Alpha EPS Consensus ↗"}
          </a>
        </div>
      </div>
    </section>
  `;
}
