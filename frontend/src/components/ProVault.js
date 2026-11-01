import { renderPositionDoctorForm } from "./PositionDoctor.js";

export function renderProVault(state) {
  const t = state.t;
  const isPro = state.isProUnlocked;
  const stocks = state.stocks || [];
  const topIgnitions = stocks
    .filter((s) => s.zone_code === "IGNITION_ZONE" || Number(s.score) >= 75)
    .slice(0, 5);
  const proCapUsd = Number(state.proPortfolioUsd || 30000);
  const perSlotUsd = Math.round(proCapUsd * 0.15); // 15% slot -> 9% stop = 1.35% total account risk
  const celh = stocks.find((s) => s.ticker === "CELH");
  const mbly = stocks.find((s) => s.ticker === "MBLY");

  const celhClose = celh ? Number(celh.close).toFixed(2) : "27.93";
  const celhMa20 = celh && celh.ma20_price ? Number(celh.ma20_price).toFixed(2) : "27.93";
  const celhMa60 = celh && celh.ma60_price ? Number(celh.ma60_price).toFixed(2) : "29.12";
  const celhTp1 = celh && celh.tp1_2x_price ? Number(celh.tp1_2x_price).toFixed(2) : (Number(celhClose) * 2).toFixed(2);
  const celhStop = celh && celh.stop_loss_price ? Number(celh.stop_loss_price).toFixed(2) : (Number(celhClose) * 0.91).toFixed(2);
  const celhScore = celh ? Number(celh.score) : 90;

  const mblyClose = mbly ? Number(mbly.close).toFixed(2) : "7.02";
  const mblyLow52 = mbly ? Number(mbly.low52).toFixed(2) : "6.47";
  const mblyMa60 = mbly && mbly.ma60_price ? Number(mbly.ma60_price).toFixed(2) : "8.17";
  const mblyTp1 = mbly && mbly.tp1_2x_price ? Number(mbly.tp1_2x_price).toFixed(2) : (Number(mblyClose) * 2).toFixed(2);
  const mblyScore = mbly ? Number(mbly.score) : 47;

  const pineCode =
    state.pineCode ||
    `//@version=5
indicator("RightSideAlpha PW-RSI Ignition v2.6", overlay=true)
ma20 = ta.sma(close, 20)
ma60 = ta.sma(close, 60)
low52 = ta.lowest(low, 252)
high52 = ta.highest(high, 252)
volRatio = volume / ta.sma(volume, 20)
washout10d = ta.highest(volRatio, 10) >= 1.40
proxLow = (close - low52) / low52 * 100
ddHigh = (close - high52) / high52 * 100
ignition = ddHigh <= -35 and proxLow >= 10 and proxLow <= 40 and close > ma20 and close > ma60 and washout10d
plot(ma20, "MA20", color=color.new(color.aqua, 0), linewidth=2)
plot(ma60, "MA60 Trigger", color=color.new(color.orange, 0), linewidth=2)
plotshape(ignition and not ignition[1], "PW-RSI IGNITION", shape.labelup, location.belowbar, color.green, text="IGNITION", textcolor=color.white)`;

  return `
    <section class="proof-card" id="proVaultSection" style="border-top:2px solid var(--fin-blue); margin-bottom:22px;">
      <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:10px; margin-bottom:16px;">
        <div>
          <span class="badge ${isPro ? "badge-ignition" : "badge-watch"}" id="vaultBadge">
            ${isPro ? t.vaultBadgeUnlocked : t.vaultBadgeLocked}
          </span>
          <h2 style="font-size:1.2rem; font-weight:800; margin-top:6px; color:#ffffff; letter-spacing:-0.01em;">
            ${t.vaultTitle}
          </h2>
        </div>
        <button class="btn btn-primary" id="vaultUnlockBtn" style="${isPro ? "display:none;" : ""}">
          ${t.vaultUnlockBtn}
        </button>
      </div>

      <div style="position:relative;">
        ${
          !isPro
            ? `<div id="vaultOverlayUnlock" style="position:absolute; inset:0; z-index:10; display:flex; align-items:center; justify-content:center; background:rgba(6,9,17,0.58); border-radius:6px; cursor:pointer;">
                 <div style="background:#0d1424; border:1px solid var(--fin-blue); box-shadow:0 12px 32px rgba(0,0,0,0.75); border-radius:6px; padding:22px 26px; text-align:center; max-width:500px;">
                   <div class="mono" style="font-size:0.72rem; color:#fbbf24; font-weight:800; letter-spacing:0.05em;">👑 PRO VIP ALPHA COMMAND CENTER LOCKED</div>
                   <div style="font-size:1.05rem; font-weight:800; color:#ffffff; margin:8px 0;">
                     Unlock All 72 Stock Targets, Daily Ignition Order Book, Position Sizing Calculator & Pine Script v5
                   </div>
                   <div style="font-size:0.8rem; color:var(--muted); margin-bottom:14px; line-height:1.5;">
                     Free users see only 1 sample stock ($CELH). Upgrade to Pro ($29/mo or $199 Lifetime) to reveal all hidden VIP Ignition picks, exact share-sizing orders, Position Doctor diagnostics, and the 26-Year Semiconductor CSV.
                   </div>
                   <span class="btn btn-primary" style="justify-content:center; width:100%; padding:10px; font-weight:800;">
                     🔑 Enter Pro License Key / Subscribe Now →
                   </span>
                 </div>
               </div>`
            : ""
        }

      <!-- PRO VIP MODULE 00: TODAY'S IGNITION ORDER BOOK & ACCOUNT POSITION SIZING ENGINE -->
      <div class="${isPro ? "" : "blur-locked"}" style="background:#090d16; border:1px solid rgba(16,185,129,0.35); border-left:4px solid var(--fin-up); border-radius:4px; padding:16px 18px; margin-bottom:16px;">
        <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:10px; margin-bottom:12px;">
          <div>
            <div class="mono" style="font-size:0.7rem; color:var(--fin-up); font-weight:800; letter-spacing:0.05em;">
              👑 PRO VIP EXCLUSIVE · DAILY RIGHT-SIDE IGNITION ORDER BOOK & POSITION SIZING
            </div>
            <h3 style="font-size:1.02rem; font-weight:800; color:#ffffff; margin-top:3px;">
              Today's Top Turnaround Action Sheet (1.35% Max Account Risk per Position)
            </h3>
          </div>
          <div style="display:flex; align-items:center; gap:8px;">
            <label class="mono" style="font-size:0.72rem; color:var(--muted);">MY ACCOUNT ($ USD):</label>
            <input type="number" id="proCapitalInput" value="${proCapUsd}" step="5000" min="1000" style="width:120px; padding:6px 8px; background:#05080f; border:1px solid var(--border); color:#fff; border-radius:4px; font-family:var(--font-mono); font-weight:700; margin:0;" />
            <button type="button" class="btn btn-emerald btn-sm" id="btnCalcProSizing">Update Shares</button>
          </div>
        </div>
        <div class="table-responsive-scroll">
          <table class="stock-table" style="font-size:0.78rem;">
            <thead>
              <tr>
                <th>VIP Pick</th>
                <th>PW Score</th>
                <th>Latest Close</th>
                <th>Entry Trigger (MA20/60)</th>
                <th>-9.0% Hard Stop</th>
                <th>+100% TP1 Target</th>
                <th>15% Slot Allocation ($${perSlotUsd.toLocaleString()})</th>
                <th>Max Loss Impact</th>
              </tr>
            </thead>
            <tbody>
              ${topIgnitions
                .map((s, idx) => {
                  const c = Number(s.close || 25);
                  const trig = Number(s.entry_trigger_price ?? s.ma60_price ?? c).toFixed(2);
                  const stp = Number(s.stop_loss_price ?? c * 0.91).toFixed(2);
                  const tp1 = Number(s.tp1_2x_price ?? c * 2.0).toFixed(2);
                  const sh = Math.max(1, Math.floor(perSlotUsd / c));
                  const maxLossUsd = Math.round(sh * c * 0.09);
                  return `
                    <tr>
                      <td class="mono" style="font-weight:800; color:#ffffff;">#${idx + 1} $${s.ticker} <span style="color:var(--muted); font-weight:500;">(${s.sector})</span></td>
                      <td class="mono" style="color:var(--fin-up); font-weight:800;">${s.score}/100</td>
                      <td class="mono">$${c.toFixed(2)}</td>
                      <td class="mono" style="color:#60a5fa; font-weight:700;">$${trig}</td>
                      <td class="mono" style="color:var(--fin-down); font-weight:700;">$${stp}</td>
                      <td class="mono" style="color:var(--fin-up); font-weight:700;">$${tp1}</td>
                      <td class="mono" style="color:#ffffff; font-weight:800;">Buy ${sh} shares ($${Math.round(sh * c).toLocaleString()})</td>
                      <td class="mono" style="color:var(--fin-amber);">-$${maxLossUsd.toLocaleString()} (-1.35% Eq)</td>
                    </tr>
                  `;
                })
                .join("")}
            </tbody>
          </table>
        </div>
      </div>

      <div id="vaultContentWrap" class="${isPro ? "" : "blur-locked"}" style="display:grid; grid-template-columns:repeat(auto-fit, minmax(330px, 1fr)); gap:16px;">
        <!-- Module 01: Position Doctor -->
        ${renderPositionDoctorForm(state)}

        <!-- Module 02: Institutional SEC Research Vault -->
        <div style="background:#090d16; border:1px solid var(--border); border-top:2px solid var(--fin-blue); border-radius:4px; padding:18px; display:flex; flex-direction:column; justify-content:space-between;">
          <div>
            <div style="font-size:0.7rem; font-family:var(--font-mono); font-weight:700; color:#60a5fa; letter-spacing:0.05em; text-transform:uppercase;">
              ${t.tool2Title}
            </div>
            <h3 style="font-size:1rem; font-weight:800; margin:6px 0; color:#ffffff;">${t.tool2Sub}</h3>
            <p style="font-size:0.78rem; color:var(--muted); margin-bottom:12px;">${t.tool2Desc}</p>

            <div style="font-size:0.8rem; background:#05080f; padding:12px; border-radius:4px; border:1px solid var(--border); margin-bottom:12px; display:flex; flex-direction:column; gap:12px;">
              <div style="border-left:3px solid var(--fin-up); padding-left:10px;">
                <div style="display:flex; justify-content:space-between; align-items:center;">
                  <b class="mono" style="color:#ffffff;">CELH · Celsius Holdings ($${celhClose})</b>
                  <span class="badge badge-ignition">SCORE ${celhScore}</span>
                </div>
                <div style="color:var(--muted); font-size:0.76rem; margin-top:4px; line-height:1.45;">
                  PepsiCo North America inventory destocking complete; 2026E operating leverage +257%. Latest Close <b class="mono" style="color:#fff;">$${celhClose}</b> reclaiming MA20 ($${celhMa20}) toward MA60 ($${celhMa60}). Stop: $${celhStop} · TP1 (2x): <b class="mono" style="color:var(--fin-up);">$${celhTp1}</b>.
                </div>
                <button class="btn btn-sm btn-open-research" data-ticker="CELH" style="margin-top:6px;">
                  Read $CELH SEC Research Brief ↗
                </button>
              </div>

              <div style="border-left:3px solid var(--fin-blue); padding-left:10px;">
                <div style="display:flex; justify-content:space-between; align-items:center;">
                  <b class="mono" style="color:#ffffff;">MBLY · Mobileye Global ($${mblyClose})</b>
                  <span class="badge badge-watch">SCORE ${mblyScore}</span>
                </div>
                <div style="color:var(--muted); font-size:0.76rem; margin-top:4px; line-height:1.45;">
                  Tier-1 OEM ADAS inventory digestion completed; EyeQ6 design wins drive operating income inflection (-$0.39B → +$0.45B). Latest Close <b class="mono" style="color:#fff;">$${mblyClose}</b> · 52W Low $${mblyLow52} · MA60 Trigger <b class="mono" style="color:#60a5fa;">$${mblyMa60}</b> · TP1: <b class="mono" style="color:var(--fin-up);">$${mblyTp1}</b>.
                </div>
                <button class="btn btn-sm btn-open-research" data-ticker="MBLY" style="margin-top:6px;">
                  Read $MBLY SEC Research Brief ↗
                </button>
              </div>
            </div>
          </div>

          <div>
            <button class="btn btn-open-research-modal" style="width:100%; justify-content:center; padding:9px;">
              ${t.tool2ViewBtn}
            </button>
          </div>
        </div>

        <!-- Module 03: TradingView Pine Script v5 -->
        <div style="background:#090d16; border:1px solid var(--border); border-top:2px solid #6366f1; border-radius:4px; padding:18px; display:flex; flex-direction:column; justify-content:space-between;">
          <div>
            <div style="font-size:0.7rem; font-family:var(--font-mono); font-weight:700; color:#818cf8; letter-spacing:0.05em; text-transform:uppercase;">
              ${t.tool3Title}
            </div>
            <h3 style="font-size:1rem; font-weight:800; margin:6px 0; color:#ffffff;">${t.tool3Sub}</h3>
            <p style="font-size:0.78rem; color:var(--muted); margin-bottom:10px;">${t.tool3Desc}</p>

            <pre id="pineCodeBox" style="background:#05080f; padding:12px; border-radius:4px; font-size:0.7rem; color:#93c5fd; overflow-x:auto; max-height:155px; font-family:var(--font-mono); border:1px solid var(--border); line-height:1.45;">${pineCode}</pre>
          </div>

          <div style="margin-top:12px;">
            <button class="btn btn-purple" id="btnCopyPineScript" style="width:100%; justify-content:center; padding:9px;">
              ${t.tool3CopyBtn}
            </button>
          </div>
        </div>
      </div>
      </div>
    </section>
  `;
}
