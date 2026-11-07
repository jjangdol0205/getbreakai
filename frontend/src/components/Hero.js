export function renderHero(state) {
  const t = state.t;
  const kpis = state.backtestKpis || {};
  const hitRate = Number(kpis.hit_rate_2x_pct ?? 55.24).toFixed(2);
  const underwater = Number(kpis.median_days_underwater ?? 29.0).toFixed(1);
  const netCagr = Number(kpis.cagr_after_tax_pct ?? kpis.us_only_net_cagr_pct ?? 17.81).toFixed(2);
  const severeRisk = Number(kpis.severe_loss_risk_pct ?? 0.93).toFixed(2);
  const latestStockDate =
    state.stocks && state.stocks.length > 0 && state.stocks[0].date
      ? state.stocks[0].date
      : "2026-10-30";

  return `
    <section class="hero">
      <div class="hero-top-row">
        <div>
          <div style="display:flex; align-items:center; gap:10px; flex-wrap:wrap; margin-bottom:8px;">
            <div class="hero-tag" id="heroTag" style="margin-bottom:0;">${t.heroTag}</div>
            <button type="button" class="btn btn-sm" id="btnOpenPwRsiExplainer" style="padding:2px 8px; font-size:0.68rem; font-family:var(--font-mono); border-color:rgba(56,189,248,0.4); color:#38bdf8; background:rgba(56,189,248,0.08); display:inline-flex; align-items:center; gap:4px; cursor:pointer;" title="Click to view full PW-RSI methodology">
              <span>💡</span>
              <span>${t.pwRsiExplainerBtn || "What is PW-RSI?"}</span>
            </button>
          </div>
          <h1 id="heroTitle">${t.heroTitle}</h1>
          <p id="heroDesc">${t.heroDesc}</p>
        </div>
        <div style="background:#0a0e18; border:1px solid var(--border); border-radius:4px; padding:12px 16px; min-width:250px;">
          <div style="font-size:0.68rem; color:var(--muted); font-family:var(--font-mono); text-transform:uppercase; letter-spacing:0.05em;">
            UNIVERSE SPECIFICATION · LATEST CLOSE (${latestStockDate})
          </div>
          <div style="font-size:0.88rem; font-weight:700; color:#fff; margin-top:4px;">
            US-Listed Equities Only (NYSE / NASDAQ)
          </div>
          <div style="font-size:0.75rem; color:var(--muted); margin-top:4px; font-family:var(--font-mono);">
            72 Liquid Growth & Turnaround Constituents · USD ($)
          </div>
        </div>
      </div>

      <div class="hero-onboarding-strip" style="display:flex; align-items:center; justify-content:space-between; flex-wrap:wrap; gap:10px; background:rgba(13,19,34,0.85); border:1px solid rgba(56,189,248,0.22); border-left:3px solid #10b981; border-radius:6px; padding:10px 14px; margin-bottom:14px;">
        <div style="display:flex; align-items:center; flex-wrap:wrap; gap:12px; font-size:0.76rem; color:#cbd5e1;">
          <span class="mono" style="font-size:0.68rem; font-weight:800; color:#34d399; background:rgba(16,185,129,0.12); padding:2px 7px; border-radius:3px;">15s QUICK START</span>
          <span><b>1. Ignition:</b> Price &gt; MA20/MA60 + 1.4x Vol</span>
          <span style="color:var(--muted);">·</span>
          <span><b>2. Risk Guard:</b> -9.0% Hard Stop / 55d Time Stop</span>
          <span style="color:var(--muted);">·</span>
          <span><b>3. Harvest:</b> Sell 50% at +100% (2x Target)</span>
        </div>
        <div style="display:flex; align-items:center; gap:8px; flex-wrap:wrap;">
          <a href="#proVaultSection" class="btn btn-sm" id="btnHeroJumpPositionDoctor" style="background:rgba(16,185,129,0.14); border-color:rgba(16,185,129,0.45); color:#34d399; font-weight:800; padding:5px 10px; font-size:0.73rem; text-decoration:none;">
            🩺 Free 3-Second Position Doctor ↓
          </a>
          <a href="#stockTable" class="btn btn-sm" id="btnHeroJumpFreeSample" style="background:rgba(56,189,248,0.1); border-color:rgba(56,189,248,0.35); color:#38bdf8; font-weight:700; padding:5px 10px; font-size:0.73rem; text-decoration:none;">
            🔥 #1 Free Sample ($CELH) ↓
          </a>
        </div>
      </div>

      <div class="kpi-grid">
        <div class="kpi-card kpi-emerald">
          <div class="kpi-label" id="kpi1_label">${t.kpi1_label}</div>
          <div class="kpi-val">${hitRate}%</div>
          <div class="kpi-sub" id="kpi1_sub">${t.kpi1_sub}</div>
        </div>
        <div class="kpi-card">
          <div class="kpi-label" id="kpi2_label">${t.kpi2_label}</div>
          <div class="kpi-val">${underwater}d</div>
          <div class="kpi-sub" id="kpi2_sub">${t.kpi2_sub}</div>
        </div>
        <div class="kpi-card kpi-emerald">
          <div class="kpi-label" id="kpi3_label">${t.kpi3_label}</div>
          <div class="kpi-val">+${netCagr}%</div>
          <div class="kpi-sub" id="kpi3_sub">${t.kpi3_sub}</div>
        </div>
        <div class="kpi-card kpi-amber">
          <div class="kpi-label" id="kpi4_label">${t.kpi4_label}</div>
          <div class="kpi-val">${severeRisk}%</div>
          <div class="kpi-sub" id="kpi4_sub">${t.kpi4_sub}</div>
        </div>
      </div>
    </section>
  `;
}
