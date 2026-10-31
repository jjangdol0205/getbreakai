export function renderHeader(state) {
  const t = state.t;
  const lang = state.lang;
  const isPro = state.isProUnlocked;
  const activeView = state.activeView || "rightside";
  const ov = state.semiOverview;
  const semiScore = ov && ov.fg_score !== undefined ? Number(ov.fg_score).toFixed(1) : "18.0";
  const semiRegime = ov && ov.regime_en ? String(ov.regime_en).toUpperCase() : "EXTREME FEAR";
  const semiDate = ov && ov.date ? ov.date : "2026-10-26";
  const smhPrice = ov && ov.smh_close !== undefined ? Number(ov.smh_close).toFixed(2) : "541.62";
  const xlvPrice = ov && ov.xlv_close !== undefined ? Number(ov.xlv_close).toFixed(2) : "179.28";
  const qqqPrice = ov && ov.qqq_close !== undefined ? Number(ov.qqq_close).toFixed(2) : "712.20";

  const etfs = (ov && Array.isArray(ov.etfs)) ? ov.etfs : [];
  const qqqEtf = etfs.find((e) => e.ticker === "QQQ");
  const smhEtf = etfs.find((e) => e.ticker === "SMH");
  const xlvEtf = etfs.find((e) => e.ticker === "XLV");

  const qqq1d = qqqEtf && qqqEtf.ret_1d_pct !== undefined ? Number(qqqEtf.ret_1d_pct) : 1.11;
  const smhDd = smhEtf && smhEtf.dd_52w_pct !== undefined ? Number(smhEtf.dd_52w_pct) : (ov && ov.smh_dd_pct !== undefined ? Number(ov.smh_dd_pct) : -19.03);
  const xlv1d = xlvEtf && xlvEtf.ret_1d_pct !== undefined ? Number(xlvEtf.ret_1d_pct) : 0.84;

  return `
    <!-- INSTITUTIONAL MARKET TAPE RIBBON -->
    <div class="market-ribbon">
      <div class="market-ribbon-inner">
        <div class="market-tape">
          <span class="universe-pill">
            <span class="universe-dot"></span>
            ${t.marketUniverseTag}
          </span>
          <span class="tape-item">
            <span class="tape-sym">QQQ</span>
            <span>$${qqqPrice}</span>
            <span class="${qqq1d >= 0 ? "tape-up" : "tape-down"}">${qqq1d >= 0 ? "+" : ""}${qqq1d.toFixed(2)}%</span>
          </span>
          <span class="tape-item">
            <span class="tape-sym">SMH</span>
            <span>$${smhPrice}</span>
            <span class="tape-down">${smhDd.toFixed(2)}% DD</span>
          </span>
          <span class="tape-item">
            <span class="tape-sym">XLV</span>
            <span>$${xlvPrice}</span>
            <span class="${xlv1d >= 0 ? "tape-up" : "tape-down"}">${xlv1d >= 0 ? "+" : ""}${xlv1d.toFixed(2)}%</span>
          </span>
          <span class="tape-item" style="cursor:pointer;" id="ribbonSwitchSemi">
            <span class="tape-sym">SEMI FEAR & GREED</span>
            <span class="tape-down" style="font-weight:700;">${semiScore} / 100 (${semiRegime})</span>
          </span>
        </div>
        <div class="mono" style="font-size:0.68rem; color:var(--muted);">
          LATEST CLOSE BASIS (${semiDate}) · NYSE / NASDAQ FEED
        </div>
      </div>
    </div>

    <!-- MAIN INSTITUTIONAL TOPBAR -->
    <header class="topbar">
      <div class="topbar-inner">
        <div class="brand-cluster">
          <div class="brand" id="brandHomeBtn">
            <span class="brand-mark">
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round">
                <polyline points="22 7 13.5 15.5 8.5 10.5 2 17"></polyline>
                <polyline points="16 7 22 7 22 13"></polyline>
              </svg>
            </span>
            <span>${activeView === "semi" ? "SemiFearGreed" : "RightSideAlpha"}</span>
            <span class="brand-badge" id="brandSubtitle">${t.brandSubtitle}</span>
          </div>

          <!-- PLATFORM SWITCHER -->
          <div class="platform-switcher" role="tablist" aria-label="Platform Switcher">
            <button
              class="platform-tab ${activeView === "rightside" ? "active-rsa" : ""}"
              id="navTabRightSide"
              data-view="rightside"
            >
              <span>${t.navRightSide}</span>
              <span class="platform-tab-tag">72 US</span>
            </button>
            <button
              class="platform-tab ${activeView === "semi" ? "active-semi" : ""}"
              id="navTabSemiFg"
              data-view="semi"
            >
              <span>${t.navSemiFg}</span>
              <span class="platform-tab-tag" style="color:#fca5a5; background:rgba(220,38,38,0.2);">${semiScore}</span>
            </button>
          </div>
        </div>

        <div class="nav-actions">
          <div class="lang-switch" aria-label="Language Selector">
            <button class="lang-btn ${lang === "en" ? "active" : ""}" data-lang="en">EN</button>
            <button class="lang-btn ${lang === "jp" ? "active" : ""}" data-lang="jp">JP</button>
            <button class="lang-btn ${lang === "kr" ? "active" : ""}" data-lang="kr">KR</button>
          </div>

          <span class="badge ${isPro ? "badge-ignition" : "badge-watch"}" id="proStatusBadge">
            ${isPro ? t.statusPro : t.statusFree}
          </span>

          <button class="btn" id="btnOpenLicense">
            <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <rect x="3" y="11" width="18" height="11" rx="2" ry="2"></rect>
              <path d="M7 11V7a5 5 0 0 1 10 0v4"></path>
            </svg>
            <span id="btnLicense">${t.btnLicense}</span>
          </button>

          <button class="btn" id="btnOpenConfig">
            <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <circle cx="12" cy="12" r="3"></circle>
              <path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1 0 2.83 2 2 0 0 1-2.83 0l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-2 2 2 2 0 0 1-2-2v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83 0 2 2 0 0 1 0-2.83l.06-.06a1.65 1.65 0 0 0 .33-1.82 1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1-2-2 2 2 0 0 1 2-2h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 0-2.83 2 2 0 0 1 2.83 0l.06.06a1.65 1.65 0 0 0 1.82.33H9a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 2-2 2 2 0 0 1 2 2v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 0 2 2 0 0 1 0 2.83l-.06.06a1.65 1.65 0 0 0-.33 1.82V9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 2 2 2 2 0 0 1-2 2h-.09a1.65 1.65 0 0 0-1.51 1z"></path>
            </svg>
            <span id="btnAdmin">${t.btnAdmin}</span>
          </button>

          <a
            class="btn btn-primary lemonsqueezy-button"
            id="topSubscribeBtn"
            href="${state.config.ls_site1_monthly_url}?embed=1"
          >
            <span id="btnUnlockPro">${t.btnUnlockPro}</span>
          </a>
        </div>
      </div>
    </header>
  `;
}
