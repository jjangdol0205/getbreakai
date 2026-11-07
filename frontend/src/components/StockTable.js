import { formatCheckoutUrl } from "../services/api.js";

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
  const isPro = state.isProUnlocked;
  const stocks = (state.filteredStocks || []).filter((s) => !String(s.ticker).includes("."));
  const cfg = state.config || {};
  const monthlyUrl = cfg.ls_site1_monthly_url || "https://truthofmarket.lemonsqueezy.com/checkout/buy/bad98d00-7175-41f6-9d58-eeb2471d0da4";

  const renderSortTh = (col, label, isNum = false) => {
    const isAct = state.sortCol === col;
    const chevron = isAct ? (state.sortAsc ? "▲" : "▼") : "↕";
    const actClass = isAct ? `sort-active ${state.sortAsc ? "sort-asc" : "sort-desc"}` : "";
    const numClass = isNum ? "col-num" : "";
    return `<th data-sort="${col}" data-base-label="${label}" class="sort-header ${actClass} ${numClass}">${label} <span class="sort-chevron ${isAct ? "" : "muted"}">${chevron}</span></th>`;
  };

  const softPaywallBanner =
    !isPro && stocks.length > 5
      ? `
    <div class="soft-paywall-barrier">
      <div style="font-size:0.72rem; font-family:var(--font-mono); color:#93c5fd; font-weight:800; text-transform:uppercase; letter-spacing:0.05em; margin-bottom:4px;">
        ${t.softPaywallTitle || "🔒 67 Pro Ignition Setups Live Today"}
      </div>
      <p style="color:#cbd5e1; font-size:0.84rem; margin:0 0 14px; line-height:1.5;">
        ${t.softPaywallDesc || "Tickers 1–5 are unlocked as featured ignition leaders. Unlock live institutional target levels, -9% stops, and real-time execution signals for all remaining 67 stocks."}
      </p>
      <a class="soft-paywall-btn lemonsqueezy-button btn-unlock-row" data-direct-ls="1" href="${monthlyUrl}?embed=1" target="_blank" rel="noopener noreferrer">
        🍋 ${t.softPaywallUnlockCta || "Unlock 67 Pro Setups ($29/mo)"} →
      </a>
    </div>
  `
      : "";

  return `
    <div class="table-wrap">
      <table class="stock-table" id="stockTable">
        <thead>
          <tr>
            ${renderSortTh("ticker", t.colTicker, false)}
            ${renderSortTh("zone_code", t.colZone, false)}
            ${renderSortTh("score", t.colScore, true)}
            ${renderSortTh("close", t.colClose, true)}
            ${renderSortTh("prox_low52_pct", t.colProx, true)}
            ${renderSortTh("dd_high52_pct", t.colDD, true)}
            ${renderSortTh("vs_ma20_pct", t.colMA, true)}
            ${renderSortTh("vol_surge_10d", t.colVol, true)}
            ${renderSortTh("hist_2x_rate", t.colHist, true)}
            <th>${t.colTrigger}</th>
            <th>${t.colActions}</th>
          </tr>
        </thead>
        <tbody id="tableBody">
          ${renderStockRows(state)}
        </tbody>
      </table>
      ${softPaywallBanner}
    </div>
  `;
}

export function renderStockRows(state) {
  const t = state.t || {};
  const stocks = (state.filteredStocks || []).filter((s) => !String(s.ticker).includes("."));
  const lang = state.lang;
  const isPro = state.isProUnlocked;
  const cfg = state.config || {};
  const lsMonthlyUrl = formatCheckoutUrl(
    cfg.ls_site1_monthly_url,
    "https://truthofmarket.lemonsqueezy.com/checkout/buy/bad98d00-7175-41f6-9d58-eeb2471d0da4"
  );
  const tvAffId = encodeURIComponent(cfg.tradingview_aff_id || "1173809");
  const saSource = encodeURIComponent(cfg.seekingalpha_source || "better_life333");
  const rawBrokerUrl = cfg.broker_referral_url || "https://www.bitget.com/referral/register?clacCode=7nja";
  const brokerSep = rawBrokerUrl.includes("?") ? "&" : "?";

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

      // Soft paywall rule:
      // Tickers 1–5 (idx < 5) are featured free sample leaders and fully readable/interactive.
      // Tickers 6–72 (idx >= 5) are softly blurred when user is not Pro.
      const isFeaturedLeader = idx < 5;
      const isFreeSample = isFeaturedLeader; // Free sample rows (1-5 open) for non-Pro users
      const isReadable = isPro || isFreeSample;
      const isSoftBlurred = !isReadable;
      const blurClass = isSoftBlurred ? "blurred-cell" : "";

      const calcTrig = s.entry_trigger_price ?? s.ma60_price ?? Number((closeVal * 1.02).toFixed(2));
      const calcStop = s.stop_loss_price ?? Number((closeVal * 0.91).toFixed(2));
      const calcTp1 = s.tp1_2x_price ?? Number((closeVal * 2.0).toFixed(2));
      const showTargets = isReadable;

      const ma60Disp = `$${Number(calcTrig).toFixed(2)}`;
      const stopDisp = `$${Number(calcStop).toFixed(2)}`;
      const tp1Disp = `$${Number(calcTp1).toFixed(2)}`;

      const triggerHtml = showTargets
        ? `<div class="mono" style="font-size:0.75rem; line-height:1.45;">
             <div><span style="color:var(--muted);">TRG</span> <span style="color:#60a5fa; font-weight:700;">${ma60Disp}</span> ${
               !isPro && isFeaturedLeader
                 ? `<span style="font-size:0.6rem; padding:1px 4px; background:rgba(14,203,129,0.18); color:var(--fin-up); border-radius:2px; font-weight:700;">FEATURED #${idx + 1}</span>`
                 : ""
             }</div>
             <div><span style="color:var(--muted);">STP</span> <span style="color:var(--fin-down); font-weight:600;">${stopDisp}</span> · <span style="color:var(--fin-up);">TP ${tp1Disp}</span></div>
           </div>`
        : `<span class="pro-lock-cell btn-unlock-row" title="Unlock Pro to view exact Entry Trigger, -9% Stop & +100% Target">
             <svg width="11" height="11" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2">
               <rect x="3" y="11" width="18" height="11" rx="2" ry="2"></rect>
               <path d="M7 11V7a5 5 0 0 1 10 0v4"></path>
             </svg>
             <span>🔒 PRO TARGETS</span>
           </span>`;

      const tvUrl = `https://www.tradingview.com/symbols/${encodeURIComponent(s.ticker)}/?aff_id=${tvAffId}`;
      const saUrl = `https://seekingalpha.com/symbol/${encodeURIComponent(s.ticker)}/earnings?source=${saSource}`;
      const brokerUrl = `${rawBrokerUrl}${brokerSep}symbol=${encodeURIComponent(s.ticker)}`;

      const tickerCellHtml = `<div>
        <div style="display:flex; align-items:center; gap:7px;">
          <span class="mono" style="font-weight:800; font-size:0.9rem; color:#ffffff;">${s.ticker}</span>
          <span style="font-size:0.62rem; font-family:var(--font-mono); padding:1px 4px; background:#141d2f; border:1px solid #24324d; color:#93c5fd; border-radius:2px;">US</span>
          ${
            !isPro
              ? isFeaturedLeader
                ? `<span style="font-size:0.6rem; padding:1px 4px; background:rgba(14,203,129,0.18); color:var(--fin-up); border-radius:2px; font-weight:700;">${idx === 0 || s.ticker === "CELH" ? "FREE SAMPLE #1 · FEATURED #1" : `FEATURED #${idx + 1}`}</span>`
                : `<span style="font-size:0.6rem; padding:1px 5px; background:rgba(41,98,255,0.14); border:1px solid rgba(41,98,255,0.35); color:#93c5fd; border-radius:2px; font-family:var(--font-mono); font-weight:700;">PRO SETUP #${idx + 1}</span>`
              : ""
          }
        </div>
        <div style="font-size:0.73rem; font-family:var(--font-sans); color:var(--muted); margin-top:2px;">
          ${stockName} · <span style="color:var(--text-secondary);">${s.sector}</span>
        </div>
      </div>`;

      const closeCellHtml =
        s.close === null || s.close === undefined
          ? `<div class="mono" style="font-weight:700; color:var(--muted);">$0.00</div>`
          : `<div class="mono" style="font-weight:700; color:#ffffff;" title="Latest Close Date: ${s.date || "2026-10-30"}">$${closeVal.toFixed(2)}</div>
             <div class="range-52w-wrap" title="52W Range: $${low52.toFixed(2)} – $${high52.toFixed(2)} | Current: $${closeVal.toFixed(2)}">
               <div class="range-52w-track">
                 <div class="range-52w-pin" style="left:${rangePct}%;"></div>
               </div>
               <div class="range-52w-labels">
                 <span>$${low52.toFixed(0)}</span>
                 <span class="range-52w-curr">${rangePct}%</span>
                 <span>$${high52.toFixed(0)}</span>
               </div>
             </div>`;

      return `
      <tr data-ticker="${s.ticker}" class="${isSoftBlurred ? "soft-paywall-row" : ""}">
        <td>
          ${tickerCellHtml}
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
        <td class="col-num ${blurClass}">
          <div style="display:flex; align-items:center; justify-content:flex-end; gap:6px;">
            <div class="score-bar">
              <div class="score-fill" style="width:${Number(s.score ?? 0)}%; background:${
                s.score >= 80 ? "var(--fin-up)" : s.score >= 55 ? "var(--fin-amber)" : "var(--fin-down)"
              };"></div>
            </div>
            <span class="mono" style="font-weight:800; font-size:0.9rem; width:26px; text-align:right;">${Number(s.score ?? 0)}</span>
          </div>
        </td>
        <td class="col-num ${blurClass}">
          ${closeCellHtml}
        </td>
        <td class="mono col-num ${blurClass}" style="color:${s.prox_low52_pct <= 40 && s.prox_low52_pct >= 10 ? "var(--fin-up)" : "var(--text-secondary)"}; font-weight:600;">
          +${Number(s.prox_low52_pct ?? 0).toFixed(1)}%
        </td>
        <td class="mono col-num ${blurClass}" style="color:var(--fin-down); font-weight:600;">
          ${Number(s.dd_high52_pct ?? 0).toFixed(1)}%
        </td>
        <td class="mono col-num ${blurClass}">
          <span style="color:${ma20Color}; font-weight:600;">${Number(s.vs_ma20_pct ?? 0) >= 0 ? "+" : ""}${Number(s.vs_ma20_pct ?? 0).toFixed(1)}%</span>
          <span style="color:var(--muted);"> / </span>
          <span style="color:${ma60Color}; font-weight:600;">${Number(s.vs_ma60_pct ?? 0) >= 0 ? "+" : ""}${Number(s.vs_ma60_pct ?? 0).toFixed(1)}%</span>
        </td>
        <td class="mono col-num ${blurClass}" style="color:${volColor}; font-weight:700;">
          ${Number(s.vol_surge_10d ?? 1.0).toFixed(2)}x
        </td>
        <td class="mono col-num ${blurClass}" style="font-weight:700; color:${s.hist_2x_rate >= 40 ? "var(--fin-up)" : "var(--text-secondary)"};">
          ${Number(s.hist_2x_rate ?? 0).toFixed(1)}%
        </td>
        <td>${triggerHtml}</td>
        <td>
          <div style="display:flex; gap:5px;">
            ${
              isSoftBlurred
                ? `<a class="btn btn-primary btn-sm lemonsqueezy-button btn-unlock-row" data-direct-ls="1" href="${lsMonthlyUrl}" target="_blank" rel="noopener noreferrer" style="white-space:nowrap; font-weight:700;">
                     🔒 ${t.softPaywallUnlockCta || "Unlock 67 Pro Setups ($29/mo)"}
                   </a>`
                : `
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
            `
            }
          </div>
        </td>
      </tr>
    `;
    })
    .join("");
}
