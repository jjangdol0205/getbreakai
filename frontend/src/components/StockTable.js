export function renderScreenerControls(state) {
  const t = state.t;
  const f = state.zoneFilter;
  const allStocks = (state.stocks || []).filter((s) => !String(s.ticker).includes("."));
  const cAll = allStocks.length;
  const cIgn = allStocks.filter((s) => s.zone_code === "IGNITION_ZONE").length;
  const cWatch = allStocks.filter((s) => s.zone_code === "WASHOUT_WATCH").length;
  const cKnife = allStocks.filter((s) => s.zone_code === "LEFT_SIDE_KNIFE").length;
  const cTrap = allStocks.filter((s) => s.zone_code === "VALUE_TRAP_FILTERED").length;

  return `
    <div class="screener-header-bar">
      <div class="controls">
        <div class="search-wrap">
          <svg class="search-icon" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <circle cx="11" cy="11" r="8"></circle>
            <line x1="21" y1="21" x2="16.65" y2="16.65"></line>
          </svg>
          <input
            type="text"
            class="search-box"
            id="searchInput"
            placeholder="${t.searchPlaceholder}"
            value="${state.searchQuery || ""}"
          />
        </div>
        <div class="filter-tabs">
          <button class="filter-tab ${f === "ALL" ? "active" : ""}" data-zone="ALL">
            <span>${t.filterAll}</span>
            <span class="tab-count">${cAll}</span>
          </button>
          <button class="filter-tab ${f === "IGNITION_ZONE" ? "active" : ""}" data-zone="IGNITION_ZONE">
            <span style="width:6px; height:6px; border-radius:50%; background:var(--fin-up); display:inline-block;"></span>
            <span>${t.filterIgnition}</span>
            <span class="tab-count">${cIgn}</span>
          </button>
          <button class="filter-tab ${f === "WASHOUT_WATCH" ? "active" : ""}" data-zone="WASHOUT_WATCH">
            <span style="width:6px; height:6px; border-radius:50%; background:var(--fin-amber); display:inline-block;"></span>
            <span>${t.filterWatch}</span>
            <span class="tab-count">${cWatch}</span>
          </button>
          <button class="filter-tab ${f === "LEFT_SIDE_KNIFE" ? "active" : ""}" data-zone="LEFT_SIDE_KNIFE">
            <span style="width:6px; height:6px; border-radius:50%; background:var(--fin-down); display:inline-block;"></span>
            <span>${t.filterKnife}</span>
            <span class="tab-count">${cKnife}</span>
          </button>
          <button class="filter-tab ${f === "VALUE_TRAP_FILTERED" ? "active" : ""}" data-zone="VALUE_TRAP_FILTERED">
            <span>${t.filterTrap}</span>
            <span class="tab-count">${cTrap}</span>
          </button>
        </div>
      </div>
    </div>
  `;
}

export function renderStockTable(state) {
  const t = state.t;

  return `
    <div class="table-wrap">
      <table class="stock-table" id="stockTable">
        <thead>
          <tr>
            <th data-sort="ticker" class="sort-header">${t.colTicker} ↕</th>
            <th data-sort="zone_code" class="sort-header">${t.colZone} ↕</th>
            <th data-sort="score" class="sort-header">${t.colScore} ↕</th>
            <th data-sort="close" class="sort-header">${t.colClose} ↕</th>
            <th data-sort="prox_low52_pct" class="sort-header">${t.colProx} ↕</th>
            <th data-sort="dd_high52_pct" class="sort-header">${t.colDD} ↕</th>
            <th data-sort="vs_ma20_pct" class="sort-header">${t.colMA} ↕</th>
            <th data-sort="vol_surge_10d" class="sort-header">${t.colVol} ↕</th>
            <th data-sort="hist_2x_rate" class="sort-header">${t.colHist} ↕</th>
            <th>${t.colTrigger}</th>
            <th>${t.colActions}</th>
          </tr>
        </thead>
        <tbody id="tableBody">
          ${renderStockRows(state)}
        </tbody>
      </table>
    </div>
  `;
}

export function renderStockRows(state) {
  const stocks = (state.filteredStocks || []).filter((s) => !String(s.ticker).includes("."));
  const lang = state.lang;
  const isPro = state.isProUnlocked;

  if (!stocks.length) {
    return `
      <tr>
        <td colspan="11" style="text-align:center; padding:36px; color:var(--muted); font-family:var(--font-sans);">
          No US-listed equities match the active filter criteria.
        </td>
      </tr>
    `;
  }

  return stocks
    .map((s, idx) => {
      let badgeClass = "badge-watch";
      if (s.zone_code === "IGNITION_ZONE") badgeClass = "badge-ignition";
      else if (s.zone_code === "LEFT_SIDE_KNIFE") badgeClass = "badge-knife";
      else if (s.zone_code === "VALUE_TRAP_FILTERED") badgeClass = "badge-trap";

      const rawZoneLabel =
        lang === "jp" ? s.zone_label_jp : lang === "kr" ? s.zone_label_kr : s.zone_label_en;
      const cleanZoneLabel = String(rawZoneLabel || s.zone_code).replace(/^[🟢🟡🔴⚠️\s]+/, "");
      const stockName =
        lang === "jp" ? s.name_jp : lang === "kr" ? s.name_kr : s.name_en;

      const ma20Color = s.vs_ma20_pct >= 0 ? "var(--fin-up)" : "var(--fin-down)";
      const ma60Color = s.vs_ma60_pct >= 0 ? "var(--fin-up)" : "var(--fin-down)";
      const volColor = s.vol_surge_10d >= 1.35 ? "var(--fin-up)" : "var(--text-secondary)";

      // 52W range bar calculation
      const low52 = Number(s.low52 || 0);
      const high52 = Number(s.high52 || s.close * 1.5);
      const closeVal = Number(s.close || 0);
      const rangeSpan = Math.max(0.01, high52 - low52);
      const rangePct = Math.min(100, Math.max(2, Math.round(((closeVal - low52) / rangeSpan) * 100)));

      // Free tier previews top 4 rows; rows 4+ require Pro
      const hasUnmaskedPrices =
        s.stop_loss_price !== null &&
        s.stop_loss_price !== undefined &&
        s.tp1_2x_price !== null &&
        s.tp1_2x_price !== undefined;
      const showTargets = (isPro || !s.is_pro_locked) && hasUnmaskedPrices;
      const trigPrice = s.entry_trigger_price ?? s.ma60_price;
      const ma60Disp =
        trigPrice !== null && trigPrice !== undefined
          ? `$${Number(trigPrice).toFixed(2)}`
          : "LOCKED";
      const stopDisp =
        s.stop_loss_price !== null && s.stop_loss_price !== undefined
          ? `$${Number(s.stop_loss_price).toFixed(2)}`
          : "LOCKED";
      const tp1Disp =
        s.tp1_2x_price !== null && s.tp1_2x_price !== undefined
          ? `$${Number(s.tp1_2x_price).toFixed(2)}`
          : "LOCKED";

      const triggerHtml = showTargets
        ? `<div class="mono" style="font-size:0.75rem; line-height:1.45;">
             <div><span style="color:var(--muted);">TRG</span> <span style="color:#60a5fa; font-weight:700;">${ma60Disp}</span></div>
             <div><span style="color:var(--muted);">STP</span> <span style="color:var(--fin-down); font-weight:600;">${stopDisp}</span> · <span style="color:var(--fin-up);">TP ${tp1Disp}</span></div>
           </div>`
        : `<span class="pro-lock-cell btn-unlock-row" title="Click to enter Pro license key">
             <svg width="11" height="11" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2">
               <rect x="3" y="11" width="18" height="11" rx="2" ry="2"></rect>
               <path d="M7 11V7a5 5 0 0 1 10 0v4"></path>
             </svg>
             <span>PRO TARGETS</span>
           </span>`;

      const tvUrl = `/api/referral/redirect/tradingview?ticker=${encodeURIComponent(s.ticker)}`;
      const saUrl = `/api/referral/redirect/seekingalpha?ticker=${encodeURIComponent(s.ticker)}`;
      const brokerUrl = `/api/referral/redirect/broker?ticker=${encodeURIComponent(s.ticker)}`;

      return `
      <tr data-ticker="${s.ticker}">
        <td>
          <div style="display:flex; align-items:center; gap:7px;">
            <span class="mono" style="font-weight:800; font-size:0.9rem; color:#ffffff;">${s.ticker}</span>
            <span style="font-size:0.62rem; font-family:var(--font-mono); padding:1px 4px; background:#141d2f; border:1px solid #24324d; color:#93c5fd; border-radius:2px;">US</span>
          </div>
          <div style="font-size:0.73rem; font-family:var(--font-sans); color:var(--muted); margin-top:2px;">
            ${stockName} · <span style="color:var(--text-secondary);">${s.sector}</span>
          </div>
        </td>
        <td>
          <span class="badge ${badgeClass}">${cleanZoneLabel}</span>
          <div class="cond-strip">
            <span class="cond-chip ${s.c1_deep_dd ? "pass" : ""}" title="52W High Drawdown <= -20%">DD</span>
            <span class="cond-chip ${(s.c2_off_low ?? s.c2_sweet_spot) ? "pass" : ""}" title="52W Low Proximity 10-45%">LOW</span>
            <span class="cond-chip ${(s.c3_above_mas ?? s.c3_ma_reclaim) ? "pass" : ""}" title="Reclaimed MA20/MA60">MA</span>
            <span class="cond-chip ${(s.c4_vol_or_mom ?? s.c4_vol_washout) ? "pass" : ""}" title="10D Volume Washout >= 1.3x">VOL</span>
          </div>
        </td>
        <td>
          <div style="display:flex; align-items:center;">
            <span class="mono" style="font-weight:800; font-size:0.9rem; width:26px;">${Number(s.score ?? 0)}</span>
            <div class="score-bar">
              <div class="score-fill" style="width:${Number(s.score ?? 0)}%; background:${
                s.score >= 80 ? "var(--fin-up)" : s.score >= 55 ? "var(--fin-amber)" : "var(--fin-down)"
              };"></div>
            </div>
          </div>
        </td>
        <td>
          <div class="mono" style="font-weight:700; color:#ffffff;" title="Latest Close Date: ${s.date || "2026-10-13"}">$${closeVal.toFixed(2)}</div>
          <div class="range-52w-wrap" title="52W Range: $${low52.toFixed(2)} – $${high52.toFixed(2)}">
            <div class="range-52w-track">
              <div class="range-52w-fill" style="width:${rangePct}%;"></div>
            </div>
            <div class="range-52w-labels">
              <span>L:$${low52.toFixed(0)}</span>
              <span>H:$${high52.toFixed(0)}</span>
            </div>
          </div>
        </td>
        <td class="mono" style="color:${s.prox_low52_pct <= 40 && s.prox_low52_pct >= 10 ? "var(--fin-up)" : "var(--text-secondary)"}; font-weight:600;">
          +${Number(s.prox_low52_pct ?? 0).toFixed(1)}%
        </td>
        <td class="mono" style="color:var(--fin-down); font-weight:600;">
          ${Number(s.dd_high52_pct ?? 0).toFixed(1)}%
        </td>
        <td class="mono">
          <span style="color:${ma20Color}; font-weight:600;">${Number(s.vs_ma20_pct ?? 0) >= 0 ? "+" : ""}${Number(s.vs_ma20_pct ?? 0).toFixed(1)}%</span>
          <span style="color:var(--muted);"> / </span>
          <span style="color:${ma60Color}; font-weight:600;">${Number(s.vs_ma60_pct ?? 0) >= 0 ? "+" : ""}${Number(s.vs_ma60_pct ?? 0).toFixed(1)}%</span>
        </td>
        <td class="mono" style="color:${volColor}; font-weight:700;">
          ${Number(s.vol_surge_10d ?? 1.0).toFixed(2)}x
        </td>
        <td class="mono" style="font-weight:700; color:${s.hist_2x_rate >= 40 ? "var(--fin-up)" : "var(--text-secondary)"};">
          ${Number(s.hist_2x_rate ?? 0).toFixed(1)}%
        </td>
        <td>${triggerHtml}</td>
        <td>
          <div style="display:flex; gap:5px;">
            <button class="btn btn-sm btn-share-card" data-ticker="${s.ticker}" title="Export Institutional Tear Sheet PNG">
              PNG
            </button>
            <a class="btn btn-sm" href="${tvUrl}" target="_blank" rel="noopener noreferrer" title="Open TradingView Chart (Partner)">
              TV ↗
            </a>
            <a class="btn btn-sm" href="${saUrl}" target="_blank" rel="noopener noreferrer" title="Open Seeking Alpha Fundamentals (Partner)">
              SA ↗
            </a>
            <a class="btn btn-sm" href="${brokerUrl}" target="_blank" rel="noopener noreferrer" title="Execute Trade on Partner Broker / Exchange" style="border-color:rgba(16,185,129,0.4); color:#34d399;">
              Trade ↗
            </a>
          </div>
        </td>
      </tr>
    `;
    })
    .join("");
}
