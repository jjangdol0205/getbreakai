export function renderProofCard(state) {
  const t = state.t;

  return `
    <section class="proof-card">
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
              <th>${t.th_2x}</th>
              <th>${t.th_med}</th>
              <th>${t.th_mdd}</th>
              <th>${t.th_dead}</th>
              <th>${t.th_trap}</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td style="font-family:var(--font-sans); color:var(--text-secondary);">0. Market Random Entry Baseline</td>
              <td>18.20%</td>
              <td>+13.24%</td>
              <td>-19.35%</td>
              <td>74.0d</td>
              <td>19.20%</td>
            </tr>
            <tr>
              <td style="font-family:var(--font-sans); color:var(--fin-down);">1. Blind 52-Week Low Dip Buy (+0–10% off low, below MA20)</td>
              <td>28.91%</td>
              <td>+20.56%</td>
              <td style="color:var(--fin-down);">-30.31%</td>
              <td style="color:var(--fin-down);">81.0d</td>
              <td style="color:var(--fin-down);">25.54%</td>
            </tr>
            <tr>
              <td style="font-family:var(--font-sans); color:var(--text-secondary);">2. 52-Week Low + Earnings Filter (Left-Side Entry)</td>
              <td>30.06%</td>
              <td>+24.28%</td>
              <td>-29.85%</td>
              <td>81.0d</td>
              <td>24.82%</td>
            </tr>
            <tr class="proof-highlight">
              <td style="font-family:var(--font-sans);">3. PW-RSI Right-Side Ignition (+14–35% off low + MA20/60 Breakout + 1.40x Vol + 55D Time-Stop)</td>
              <td style="color:var(--fin-up);">55.24%</td>
              <td style="color:var(--fin-up);">+80.47% (Mean +109.1%)</td>
              <td style="color:var(--fin-up);">-16.49%</td>
              <td style="color:var(--fin-up);">29.0d</td>
              <td style="color:var(--fin-up);">0.93%</td>
            </tr>
          </tbody>
        </table>
      </div>
    </section>
  `;
}
