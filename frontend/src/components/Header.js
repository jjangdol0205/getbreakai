import { formatCheckoutUrl } from "../services/api.js";

export function renderHeader(state) {
  const t = state.t;
  const lang = state.lang;
  const isPro = state.isProUnlocked;
  const activeView = state.activeView || "rightside";
  const ov = state.semiOverview;
  const semiScore = ov && ov.fg_score !== undefined ? Number(ov.fg_score).toFixed(1) : "18.0";
  const rawRegime = ov
    ? lang === "jp"
      ? ov.regime_jp
      : lang === "kr"
      ? ov.regime_kr
      : ov.regime_en
    : "EXTREME FEAR";
  const semiRegime = String(rawRegime || "EXTREME FEAR").toUpperCase();
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
  const xlv1d = xlvEtf && xlvEtf.ret_1d_pct !== undefined ? Number(xlvEtf.ret_1d_pct) : 0.0;
  const lsMonthlyHref = formatCheckoutUrl(
    state.config?.ls_site1_monthly_url,
    "https://truthofmarket.lemonsqueezy.com/checkout/buy/bad98d00-7175-41f6-9d58-eeb2471d0da4"
  );
  const ytUrl = state.config?.youtube_url || "https://youtube.com/@rightsidealpha";
  const igUrl = state.config?.instagram_url || "https://www.instagram.com/semifeargreed";
  const tgUrl = state.config?.telegram_channel_url || "https://t.me/truthofmarketss";

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
            <span class="${Number(semiScore) >= 55 ? "tape-up" : "tape-down"}" style="font-weight:700;">${semiScore} / 100 (${semiRegime})</span>
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

          <a
            class="btn"
            id="headerYoutubeLink"
            href="${ytUrl}"
            target="_blank"
            rel="noopener noreferrer"
            title="Official YouTube (@rightsidealpha)"
            style="border-color:rgba(239,68,68,0.4); color:#fca5a5;"
          >
            <svg width="13" height="13" viewBox="0 0 24 24" fill="currentColor">
              <path d="M23.5 6.2a3 3 0 0 0-2.1-2.1C19.5 3.5 12 3.5 12 3.5s-7.5 0-9.4.6A3 3 0 0 0 .5 6.2 31.4 31.4 0 0 0 0 12a31.4 31.4 0 0 0 .5 5.8 3 3 0 0 0 2.1 2.1c1.9.6 9.4.6 9.4.6s7.5 0 9.4-.6a3 3 0 0 0 2.1-2.1A31.4 31.4 0 0 0 24 12a31.4 31.4 0 0 0-.5-5.8zM9.6 15.6V8.4l6.3 3.6-6.3 3.6z"/>
            </svg>
            <span>YouTube</span>
          </a>

          <a
            class="btn"
            id="headerInstagramLink"
            href="${igUrl}"
            target="_blank"
            rel="noopener noreferrer"
            title="Official Instagram (@semifeargreed)"
            style="border-color:rgba(236,72,153,0.4); color:#f9a8d4;"
          >
            <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <rect x="2" y="2" width="20" height="20" rx="5" ry="5"></rect>
              <path d="M16 11.37A4 4 0 1 1 12.63 8 4 4 0 0 1 16 11.37z"></path>
              <line x1="17.5" y1="6.5" x2="17.51" y2="6.5"></line>
            </svg>
            <span>Instagram</span>
          </a>

          <a
            class="btn"
            id="headerTelegramLink"
            href="${tgUrl}"
            target="_blank"
            rel="noopener noreferrer"
            title="Official Telegram Channel (@truthofmarketss)"
            style="border-color:rgba(56,189,248,0.45); color:#38bdf8;"
          >
            <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="#38bdf8" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <line x1="22" y1="2" x2="11" y2="13"></line>
              <polygon points="22 2 15 22 11 13 2 9 22 2"></polygon>
            </svg>
            <span>Telegram</span>
            <span style="width:6px; height:6px; border-radius:50%; background:var(--fin-up); display:inline-block;"></span>
          </a>

          <button class="btn" id="btnOpenTelegram" title="Telegram Quant Briefing Preview">
            <span id="btnTelegramLabel">📡 Brief</span>
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
            href="${lsMonthlyHref}"
            target="_blank"
            rel="noopener noreferrer"
          >
            <span id="btnUnlockPro">${t.btnUnlockPro}</span>
          </a>
        </div>
      </div>
    </header>
  `;
}
