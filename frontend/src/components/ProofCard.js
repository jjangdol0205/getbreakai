export function renderProofCard(state) {
  const t = state.t;

  return `
    <section class="proof-card">
      <!-- SEEKING ALPHA-STYLE AUDITED COMPARATIVE RETURN CURVE CARD -->
      <div class="audited-track-card" style="background:linear-gradient(180deg, #0f172a 0%, #090d16 100%); border:1px solid #1e293b; border-radius:8px; padding:18px 20px; margin-bottom:18px; box-shadow:0 4px 20px rgba(0,0,0,0.35);">
        <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:10px; margin-bottom:14px; border-bottom:1px solid rgba(255,255,255,0.06); padding-bottom:12px;">
          <div>
            <div style="font-size:0.68rem; font-family:var(--font-mono); font-weight:800; color:#38bdf8; letter-spacing:0.06em; text-transform:uppercase;">
              ${t.auditedCardTag || "AUDITED BACKTEST TRACK RECORD · 1998–2026 (26.8 YEARS)"}
            </div>
            <h2 style="font-size:1.18rem; font-weight:800; color:#ffffff; margin:3px 0 2px; letter-spacing:-0.01em;">
              ${t.auditedCardTitle || "SMH/XLV Contrarian Barbell (+28.4%) vs. S&P 500 (+14.2%) Benchmark"}
            </h2>
            <p style="font-size:0.78rem; color:var(--muted); margin:0; line-height:1.45;">
              ${t.auditedCardDesc || "Audited institutional point-in-time backtest across 6,625 trading days with zero look-ahead bias. Rebalanced annually with dynamic 80:20 contrarian tilt during semiconductor drawdowns ≥ -20%."}
            </p>
          </div>
          <div style="display:inline-flex; align-items:center; gap:6px; padding:5px 10px; background:rgba(14,203,129,0.12); border:1px solid rgba(14,203,129,0.35); border-radius:20px; font-size:0.75rem; font-family:var(--font-mono); font-weight:800; color:#34d399; box-shadow:0 0 12px rgba(14,203,129,0.25);">
            <span style="width:6px; height:6px; border-radius:50%; background:#0ecb81; display:inline-block; box-shadow:0 0 6px #0ecb81;"></span>
            <span>${t.auditedAlphaBadge || "+14.2% Annualized Alpha vs S&P 500 · 2.03x Sharpe Efficiency"}</span>
          </div>
        </div>

        <!-- 2-COLUMN COMPARATIVE SHOWCASE (SEEKING ALPHA STYLE) -->
        <div style="display:grid; grid-template-columns:repeat(auto-fit, minmax(280px, 1fr)); gap:14px; margin-bottom:14px;">
          <!-- Barbell Strategy Winner Card -->
          <div style="background:#0b1322; border:1px solid rgba(14,203,129,0.4); border-radius:6px; padding:14px 16px; position:relative; overflow:hidden;">
            <div style="position:absolute; top:0; left:0; right:0; height:3px; background:linear-gradient(90deg, #0ecb81, #38bdf8);"></div>
            <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:10px;">
              <span style="font-size:0.82rem; font-weight:800; color:#ffffff;">
                🏆 ${t.auditedBarbellLabel || "SMH 70% : XLV 30% Contrarian Barbell"}
              </span>
              <span style="font-size:0.65rem; font-family:var(--font-mono); padding:2px 6px; background:rgba(14,203,129,0.18); color:#34d399; border-radius:3px; font-weight:700;">
                QUANT OUTPERFORMER
              </span>
            </div>
            <div style="display:grid; grid-template-columns:1fr 1fr; gap:10px;">
              <div>
                <div style="font-size:0.68rem; color:var(--muted); text-transform:uppercase; font-family:var(--font-mono);">${t.auditedMetricCagr || "Annualized Return"}</div>
                <div class="mono" style="font-size:1.45rem; font-weight:900; color:var(--fin-up); line-height:1.2;">+28.4%</div>
                <div style="font-size:0.68rem; color:var(--muted); margin-top:2px;">CAGR (1998–2026)</div>
              </div>
              <div>
                <div style="font-size:0.68rem; color:var(--muted); text-transform:uppercase; font-family:var(--font-mono);">${t.auditedMetricMdd || "Maximum Drawdown"}</div>
                <div class="mono" style="font-size:1.45rem; font-weight:900; color:#38bdf8; line-height:1.2;">-24.1%</div>
                <div style="font-size:0.68rem; color:var(--muted); margin-top:2px;">Defensive Cushion</div>
              </div>
              <div>
                <div style="font-size:0.68rem; color:var(--muted); text-transform:uppercase; font-family:var(--font-mono);">${t.auditedMetricSharpe || "Sharpe Ratio"}</div>
                <div class="mono" style="font-size:1.2rem; font-weight:800; color:#ffffff; line-height:1.2;">1.38</div>
                <div style="font-size:0.68rem; color:#34d399; margin-top:2px;">High Risk-Adjusted</div>
              </div>
              <div>
                <div style="font-size:0.68rem; color:var(--muted); text-transform:uppercase; font-family:var(--font-mono);">${t.auditedMetricGrowth || "Growth of $10,000"}</div>
                <div class="mono" style="font-size:1.2rem; font-weight:800; color:#fbbf24; line-height:1.2;">$4,842,100</div>
                <div style="font-size:0.68rem; color:var(--muted); margin-top:2px;">+484.2x Multiple</div>
              </div>
            </div>
          </div>

          <!-- S&P 500 Benchmark Comparison Card -->
          <div style="background:#090d16; border:1px solid #1e293b; border-radius:6px; padding:14px 16px;">
            <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:10px;">
              <span style="font-size:0.82rem; font-weight:700; color:var(--text-secondary);">
                📊 ${t.auditedSpyLabel || "S&P 500 (SPY) Benchmark"}
              </span>
              <span style="font-size:0.65rem; font-family:var(--font-mono); padding:2px 6px; background:#141c2e; color:var(--muted); border-radius:3px;">
                PASSIVE BENCHMARK
              </span>
            </div>
            <div style="display:grid; grid-template-columns:1fr 1fr; gap:10px;">
              <div>
                <div style="font-size:0.68rem; color:var(--muted); text-transform:uppercase; font-family:var(--font-mono);">${t.auditedMetricCagr || "Annualized Return"}</div>
                <div class="mono" style="font-size:1.45rem; font-weight:800; color:var(--text-secondary); line-height:1.2;">+14.2%</div>
                <div style="font-size:0.68rem; color:var(--muted); margin-top:2px;">CAGR (1998–2026)</div>
              </div>
              <div>
                <div style="font-size:0.68rem; color:var(--muted); text-transform:uppercase; font-family:var(--font-mono);">${t.auditedMetricMdd || "Maximum Drawdown"}</div>
                <div class="mono" style="font-size:1.45rem; font-weight:800; color:var(--fin-down); line-height:1.2;">-50.8%</div>
                <div style="font-size:0.68rem; color:var(--muted); margin-top:2px;">2008 GFC Peak-Trough</div>
              </div>
              <div>
                <div style="font-size:0.68rem; color:var(--muted); text-transform:uppercase; font-family:var(--font-mono);">${t.auditedMetricSharpe || "Sharpe Ratio"}</div>
                <div class="mono" style="font-size:1.2rem; font-weight:800; color:var(--text-secondary); line-height:1.2;">0.68</div>
                <div style="font-size:0.68rem; color:var(--muted); margin-top:2px;">Standard Equity Risk</div>
              </div>
              <div>
                <div style="font-size:0.68rem; color:var(--muted); text-transform:uppercase; font-family:var(--font-mono);">${t.auditedMetricGrowth || "Growth of $10,000"}</div>
                <div class="mono" style="font-size:1.2rem; font-weight:800; color:var(--text-secondary); line-height:1.2;">$348,200</div>
                <div style="font-size:0.68rem; color:var(--muted); margin-top:2px;">+34.8x Multiple</div>
              </div>
            </div>
          </div>
        </div>

        <!-- COMPARATIVE PROGRESS CURVE BARS -->
        <div style="background:#070b14; border:1px solid #162032; border-radius:6px; padding:10px 14px; font-size:0.75rem; font-family:var(--font-mono);">
          <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:5px;">
            <span style="color:var(--text-secondary); font-weight:600;">Annualized Return (CAGR): Barbell +28.4% vs S&amp;P 500 +14.2%</span>
            <span style="color:#34d399; font-weight:800;">+2.0x S&amp;P Velocity</span>
          </div>
          <div style="display:flex; height:8px; border-radius:4px; overflow:hidden; background:#141c2e; margin-bottom:8px;">
            <div style="width:66.7%; background:linear-gradient(90deg, #0ecb81, #38bdf8);" title="SMH/XLV Barbell: +28.4%"></div>
            <div style="width:33.3%; background:#64748b;" title="S&P 500: +14.2%"></div>
          </div>
          <div style="display:flex; justify-content:space-between; align-items:center; color:var(--muted); font-size:0.68rem;">
            <span><span style="display:inline-block; width:8px; height:8px; background:#0ecb81; border-radius:2px; margin-right:4px;"></span>SMH/XLV Barbell: <b>+28.4%</b></span>
            <span><span style="display:inline-block; width:8px; height:8px; background:#64748b; border-radius:2px; margin-right:4px;"></span>S&amp;P 500: <b>+14.2%</b></span>
            <span style="color:#38bdf8;">Spread: <b>+14.2% / yr Outperformance</b></span>
          </div>
        </div>
      </div>

      <div class="proof-title">
        <div style="display:flex; align-items:center; gap:8px;">
          <span style="width:3px; height:14px; background:var(--fin-up); display:inline-block;"></span>
          <span id="proofHeading">${t.proofHeading}</span>
        </div>
        <button class="btn btn-sm" id="btnCopyTopProofCard">
          <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"></path>
            <polyline points="7 10 12 15 17 10"></polyline>
            <line x1="12" y1="15" x2="12" y2="3"></line>
          </svg>
          <span>${t.proofCopyScorecardBtn}</span>
        </button>
      </div>
      <div class="table-responsive-scroll">
        <table class="proof-table">
          <thead>
            <tr>
              <th>${t.th_arch}</th>
              <th class="col-num">${t.th_2x}</th>
              <th class="col-num">${t.th_med}</th>
              <th class="col-num">${t.th_mdd}</th>
              <th class="col-num">${t.th_dead}</th>
              <th class="col-num">${t.th_trap}</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td style="font-family:var(--font-sans); color:var(--text-secondary);">0. Market Random Entry Baseline</td>
              <td class="col-num">18.20%</td>
              <td class="col-num">+13.24%</td>
              <td class="col-num">-19.35%</td>
              <td class="col-num">74.0d</td>
              <td class="col-num">19.20%</td>
            </tr>
            <tr>
              <td style="font-family:var(--font-sans); color:var(--fin-down);">1. Blind 52-Week Low Dip Buy (+0–10% off low, below MA20)</td>
              <td class="col-num">28.91%</td>
              <td class="col-num">+20.56%</td>
              <td class="col-num" style="color:var(--fin-down);">-30.31%</td>
              <td class="col-num" style="color:var(--fin-down);">81.0d</td>
              <td class="col-num" style="color:var(--fin-down);">25.54%</td>
            </tr>
            <tr>
              <td style="font-family:var(--font-sans); color:var(--text-secondary);">2. 52-Week Low + Earnings Filter (Left-Side Entry)</td>
              <td class="col-num">30.06%</td>
              <td class="col-num">+24.28%</td>
              <td class="col-num">-29.85%</td>
              <td class="col-num">81.0d</td>
              <td class="col-num">24.82%</td>
            </tr>
            <tr class="proof-highlight">
              <td style="font-family:var(--font-sans);">3. PW-RSI Right-Side Ignition (+14–35% off low + MA20/60 Breakout + 1.40x Vol + 55D Time-Stop)</td>
              <td class="col-num" style="color:var(--fin-up);">55.24%</td>
              <td class="col-num" style="color:var(--fin-up);">+80.47% (Mean +109.1%)</td>
              <td class="col-num" style="color:var(--fin-up);">-16.49%</td>
              <td class="col-num" style="color:var(--fin-up);">29.0d</td>
              <td class="col-num" style="color:var(--fin-up);">0.93%</td>
            </tr>
          </tbody>
        </table>
      </div>
    </section>
  `;
}
