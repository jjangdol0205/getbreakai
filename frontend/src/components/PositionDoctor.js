export function renderPositionDoctorForm(state) {
  const t = state.t || {};
  const td = t.doctor || {};
  const stocks = state.stocks || [];
  const celh = stocks.find((s) => s.ticker === "CELH");
  const defaultClose = celh ? Number(celh.close).toFixed(2) : "27.93";
  const defaultDate = celh && celh.date ? celh.date : "2026-10-13";
  const tickerVal = state.docTicker || "CELH";
  const entryVal =
    state.docEntry !== undefined && state.docEntry !== null && state.docEntry !== ""
      ? state.docEntry
      : defaultClose;
  const daysVal =
    state.docDays !== undefined && state.docDays !== null && state.docDays !== ""
      ? state.docDays
      : 42;
  const initialDoc = state.docLastResult
    ? formatDoctorResult(state.docLastResult, state)
    : `<div style="color:var(--muted);">${td.emptyHint || "Enter US ticker, cost basis ($), and trading days held to evaluate asymmetric exit triggers against the latest closing price"} ($${defaultClose}).</div>`;

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
            <label style="font-size:0.68rem; color:var(--muted); font-family:var(--font-mono); text-transform:uppercase;">${td.tickerLabel || "US Ticker"}</label>
            <input type="text" id="docTicker" value="${tickerVal}" placeholder="CELH" style="padding:7px 9px; background:#05080f; border:1px solid var(--border); color:#fff; border-radius:3px; font-family:var(--font-mono); font-weight:700; width:100%; margin-top:3px;" />
          </div>
          <div>
            <label style="font-size:0.68rem; color:var(--muted); font-family:var(--font-mono); text-transform:uppercase;">${td.entryLabel || "Cost Basis ($)"}</label>
            <input type="number" id="docEntry" step="0.01" value="${entryVal}" placeholder="${defaultClose}" style="padding:7px 9px; background:#05080f; border:1px solid var(--border); color:#fff; border-radius:3px; font-family:var(--font-mono); width:100%; margin-top:3px;" />
          </div>
          <div>
            <label style="font-size:0.68rem; color:var(--muted); font-family:var(--font-mono); text-transform:uppercase;">${td.daysLabel || "Trading Days"}</label>
            <input type="number" id="docDays" value="${daysVal}" placeholder="42" style="padding:7px 9px; background:#05080f; border:1px solid var(--border); color:#fff; border-radius:3px; font-family:var(--font-mono); width:100%; margin-top:3px;" />
          </div>
        </div>

        <div style="display:flex; gap:5px; flex-wrap:wrap; align-items:center; margin-bottom:12px;">
          <span style="font-size:0.68rem; color:var(--muted); font-family:var(--font-mono);">${td.presetsLabel || "LATEST CLOSE PRESETS"} (${defaultDate}):</span>
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

export function formatDoctorResult(result, state = null) {
  const td = state?.t?.doctor || {};
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

  const rawEntry = result.entry_price ?? state?.docEntry;
  const entryVal =
    rawEntry !== undefined && rawEntry !== null && Number(rawEntry) > 0
      ? Number(rawEntry)
      : 27.93;
  const stockMatch = (state?.stocks || []).find((s) => s.ticker === (result.ticker || "CELH"));
  const rawCurr = result.current_price ?? stockMatch?.close;
  const currVal =
    rawCurr !== undefined && rawCurr !== null && Number(rawCurr) > 0
      ? Number(rawCurr)
      : Number((entryVal * (1.0 + retVal / 100.0)).toFixed(2));
  const stopVal =
    result.stop_price !== undefined && result.stop_price !== null && Number(result.stop_price) > 0
      ? Number(result.stop_price)
      : entryVal * 0.91;
  const tp1Val =
    result.tp1_price !== undefined && result.tp1_price !== null && Number(result.tp1_price) > 0
      ? Number(result.tp1_price)
      : entryVal * 2.0;

  const stopStr = `$${stopVal.toFixed(2)}`;
  const tp1Str = `$${tp1Val.toFixed(2)}`;
  const currStr = `$${currVal.toFixed(2)}`;
  const entryStr = `$${entryVal.toFixed(2)}`;
  const asOfStr = result.as_of_date || stockMatch?.date || "2026-10-13";

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
        $${result.ticker || "CELH"} ${td.latestClose || "Latest Close"} (${asOfStr}): <b style="color:#fff;">${currStr}</b> · ${td.costBasis || "Cost Basis"}: <b style="color:#fff;">${entryStr}</b>
      </div>
      <div style="font-weight:700; color:#ffffff; font-size:0.78rem; margin-bottom:4px;">
        ${td.ruleTriggered || "Rule Triggered"}: ${result.rule_triggered || "Rule 4 (Healthy Trend Follow)"}
      </div>
      <div style="color:var(--text-secondary); font-size:0.78rem; line-height:1.45; margin-bottom:8px;">
        <b>${td.directive || "Execution Directive"}:</b> ${result.action_plan || ""}
      </div>
      <div class="mono" style="display:flex; gap:14px; font-size:0.72rem; color:var(--muted); border-top:1px solid var(--border); padding-top:6px;">
        <span>${td.hardStop || "Hard Stop (-9%)"}: <b style="color:var(--fin-down);">${stopStr}</b></span>
        <span>${td.tp1Target || "TP1 Target (2x)"}: <b style="color:var(--fin-up);">${tp1Str}</b></span>
      </div>
      <button type="button" class="btn btn-sm" id="btnSendDoctorTelegram" style="margin-top:10px; border-color:rgba(96,165,250,0.4); color:#93c5fd;">📲 Send Diagnosis to Telegram</button>
    </div>
  `;
}
