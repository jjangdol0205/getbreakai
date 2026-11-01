export function renderPositionDoctorForm(state) {
  const t = state.t;
  const stocks = state.stocks || [];
  const celh = stocks.find((s) => s.ticker === "CELH");
  const defaultClose = celh ? Number(celh.close).toFixed(2) : "27.93";
  const defaultDate = celh && celh.date ? celh.date : "2026-10-13";
  const initialDoc = state.docLastResult
    ? formatDoctorResult(state.docLastResult)
    : `<div style="color:var(--muted);">Enter US ticker, cost basis ($), and trading days held to evaluate asymmetric exit triggers against the latest closing price ($${defaultClose}).</div>`;

  return `
    <div style="background:#090d16; border:1px solid var(--border); border-top:2px solid var(--fin-up); border-radius:4px; padding:18px; display:flex; flex-direction:column; justify-content:space-between;">
      <div>
        <div style="font-size:0.7rem; font-family:var(--font-mono); font-weight:700; color:var(--fin-up); letter-spacing:0.05em; text-transform:uppercase;">
          ${t.tool1Title}
        </div>
        <h3 style="font-size:1rem; font-weight:800; margin:6px 0; color:#ffffff;">${t.tool1Sub}</h3>
        <p style="font-size:0.78rem; color:var(--muted); margin-bottom:14px; line-height:1.5;">${t.tool1Desc}</p>

        <div class="doctor-inputs-grid">
          <div>
            <label style="font-size:0.68rem; color:var(--muted); font-family:var(--font-mono); text-transform:uppercase;">US Ticker</label>
            <input type="text" id="docTicker" value="CELH" placeholder="CELH" style="padding:7px 9px; background:#05080f; border:1px solid var(--border); color:#fff; border-radius:3px; font-family:var(--font-mono); font-weight:700; width:100%; margin-top:3px;" />
          </div>
          <div>
            <label style="font-size:0.68rem; color:var(--muted); font-family:var(--font-mono); text-transform:uppercase;">Cost Basis ($)</label>
            <input type="number" id="docEntry" step="0.01" value="${defaultClose}" placeholder="${defaultClose}" style="padding:7px 9px; background:#05080f; border:1px solid var(--border); color:#fff; border-radius:3px; font-family:var(--font-mono); width:100%; margin-top:3px;" />
          </div>
          <div>
            <label style="font-size:0.68rem; color:var(--muted); font-family:var(--font-mono); text-transform:uppercase;">Trading Days</label>
            <input type="number" id="docDays" value="42" placeholder="42" style="padding:7px 9px; background:#05080f; border:1px solid var(--border); color:#fff; border-radius:3px; font-family:var(--font-mono); width:100%; margin-top:3px;" />
          </div>
        </div>

        <div style="display:flex; gap:5px; flex-wrap:wrap; align-items:center; margin-bottom:12px;">
          <span style="font-size:0.68rem; color:var(--muted); font-family:var(--font-mono);">LATEST CLOSE PRESETS (${defaultDate}):</span>
          ${["CELH", "MBLY", "APP", "UPST", "NVDA", "CCL"]
            .map((tick) => {
              const st = stocks.find((x) => x.ticker === tick);
              const pr = st ? ` $${Number(st.close).toFixed(2)}` : "";
              return `
                <button class="btn btn-sm btn-quick-doc mono" data-ticker="${tick}" style="padding:2px 6px; font-size:0.68rem;">${tick}${pr}</button>
              `;
            })
            .join("")}
        </div>
      </div>

      <div>
        <button class="btn btn-primary" id="btnRunPositionDoctor" style="width:100%; justify-content:center; padding:9px;">
          ${t.tool1Btn}
        </button>
        <div id="docOutput" style="margin-top:12px; font-size:0.8rem; background:#05080f; padding:12px; border-radius:4px; border:1px solid var(--border); border-left:3px solid var(--fin-blue);">
          ${initialDoc}
        </div>
      </div>
    </div>
  `;
}

export function formatDoctorResult(result) {
  let badgeColor = "var(--fin-up)";
  let borderLeftColor = "var(--fin-up)";

  if (result.status_code === "CRITICAL_STOP" || result.status_code === "HARD_STOP" || result.is_critical) {
    badgeColor = "var(--fin-down)";
    borderLeftColor = "var(--fin-down)";
  } else if (result.status_code === "DEAD_MONEY" || result.status_code === "TIME_STOP") {
    badgeColor = "var(--fin-amber)";
    borderLeftColor = "var(--fin-amber)";
  } else if (result.status_code === "TP1_REACHED" || result.status_code === "TP1_HARVEST") {
    badgeColor = "var(--fin-up)";
    borderLeftColor = "var(--fin-up)";
  }

  const cleanLabel = String(result.status_label || result.status_code || "ACTIVE_HOLD").replace(/^[🟢🚨🛑⏳🎯⏰🏆\s]+/, "");
  const retVal = Number(result.return_pct ?? 0);
  const retStr = `${retVal >= 0 ? "+" : ""}${retVal.toFixed(2)}%`;
  const fallbackEntry =
    result.stop_price !== undefined && result.stop_price !== null && Number(result.stop_price) > 0
      ? Number(result.stop_price) / 0.91
      : result.tp1_price !== undefined && result.tp1_price !== null && Number(result.tp1_price) > 0
      ? Number(result.tp1_price) / 2.0
      : 27.93;
  const entryVal =
    result.entry_price !== undefined && result.entry_price !== null && Number(result.entry_price) > 0
      ? Number(result.entry_price)
      : fallbackEntry;
  const currVal =
    result.current_price !== undefined && result.current_price !== null && Number(result.current_price) > 0
      ? Number(result.current_price)
      : entryVal * (1.0 + retVal / 100.0);
  const stopVal = result.stop_price !== undefined && result.stop_price !== null ? Number(result.stop_price) : entryVal * 0.91;
  const tp1Val = result.tp1_price !== undefined && result.tp1_price !== null ? Number(result.tp1_price) : entryVal * 2.0;
  const stopStr = stopVal > 0 ? `$${stopVal.toFixed(2)}` : "$0.00";
  const tp1Str = tp1Val > 0 ? `$${tp1Val.toFixed(2)}` : "$0.00";
  const currStr = currVal > 0 ? `$${currVal.toFixed(2)}` : "$0.00";
  const entryStr = entryVal > 0 ? `$${entryVal.toFixed(2)}` : "$0.00";

  return `
    <div style="border-left: 3px solid ${borderLeftColor}; padding-left: 10px;">
      <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:6px;">
        <span class="mono" style="font-weight:800; font-size:0.84rem; color:${badgeColor};">
          ${cleanLabel}
        </span>
        <span class="mono" style="font-weight:800; color:${retVal >= 0 ? "var(--fin-up)" : "var(--fin-down)"}; font-size:0.86rem;">
          P&L: ${retStr}
        </span>
      </div>
      <div class="mono" style="font-size:0.73rem; color:#93c5fd; margin-bottom:4px;">
        $${result.ticker || "CELH"} Latest Close: <b style="color:#fff;">${currStr}</b> · Cost Basis: <b style="color:#fff;">${entryStr}</b>
      </div>
      <div style="font-weight:700; color:#ffffff; font-size:0.78rem; margin-bottom:4px;">
        Rule Triggered: ${result.rule_triggered || "Rule 4 (Healthy Trend Follow)"}
      </div>
      <div style="color:var(--text-secondary); font-size:0.78rem; line-height:1.45; margin-bottom:8px;">
        <b>Execution Directive:</b> ${result.action_plan || ""}
      </div>
      <div class="mono" style="display:flex; gap:14px; font-size:0.72rem; color:var(--muted); border-top:1px solid var(--border); padding-top:6px;">
        <span>Hard Stop (-9%): <b style="color:var(--fin-down);">${stopStr}</b></span>
        <span>TP1 Target (2x): <b style="color:var(--fin-up);">${tp1Str}</b></span>
      </div>
    </div>
  `;
}
