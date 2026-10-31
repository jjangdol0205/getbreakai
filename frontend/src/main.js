import "./styles/theme.css";
import { translations } from "./locales/i18n.js";
import {
  fetchStocks,
  fetchBacktestSummary,
  fetchResearchBrief,
  validateLicense,
  fetchPineScript,
  evaluatePositionDoctor,
  fetchReferralConfig,
  updateReferralConfig,
  fetchSemiOverview,
  fetchSemiHistory,
  calculateSemiRebalance,
  calculateSemiLumpSum,
  fetchTelegramStatus,
  saveTelegramConfig,
  detectTelegramChatId,
  sendTelegramBriefing,
  sendTelegramTest,
} from "./services/api.js";
import { renderHeader } from "./components/Header.js";
import { renderHero } from "./components/Hero.js";
import { renderProofCard } from "./components/ProofCard.js";
import { renderScreenerControls, renderStockTable, renderStockRows } from "./components/StockTable.js";
import { renderProVault } from "./components/ProVault.js";
import { formatDoctorResult } from "./components/PositionDoctor.js";
import { renderPricing } from "./components/Pricing.js";
import { renderModals } from "./components/Modals.js";
import { renderSemiFearGreedView } from "./components/SemiFearGreedView.js";

const initialPath = window.location.pathname.toLowerCase();
const initialHash = window.location.hash.toLowerCase();
const initialHost = window.location.hostname.toLowerCase();
const defaultView =
  window.__DEFAULT_VIEW__ === "semi" ||
  initialHost.includes("truthofmarket") ||
  initialPath.includes("/semi") ||
  initialHash.includes("semi")
    ? "semi"
    : "rightside";

const state = {
  lang: localStorage.getItem("rsa_lang") || "en",
  activeView: defaultView,
  isProUnlocked: localStorage.getItem("rsa_pro_unlocked") === "true",
  licenseKey: localStorage.getItem("rsa_token") || "",
  selectedCheckoutPlan: "monthly",
  stocks: [],
  filteredStocks: [],
  backtestKpis: null,
  pineCode: null,
  searchQuery: "",
  zoneFilter: "ALL",
  sortCol: "score",
  sortAsc: false,
  // Position Doctor state
  docTicker: "CELH",
  docEntry: null,
  docDays: 42,
  docLastResult: null,
  // SemiFearGreed state
  semiOverview: null,
  semiHistory: null,
  semiGaugeTab: "overview",
  semiRange: "1Y",
  semiCapUsd: 100000,
  semiMode: "AUTO_REGIME",
  semiFreq: "ANNUAL",
  semiGainKrw: 3800000,
  semiRebalanceResult: null,
  semiLumpCapUsd: 50000,
  semiLumpScore: null,
  semiLumpSumResult: null,
  config: {
    site1_name: "RightSideAlpha",
    site1_url: localStorage.getItem("rsa_cfg_site1_url") || "https://getbreakai.com",
    site2_url: "https://truthofmarket.com",
    ls_site1_monthly_url:
      localStorage.getItem("rsa_cfg_ls_monthly") ||
      "https://rightsidealpha.lemonsqueezy.com/checkout/buy/pro-monthly",
    ls_site1_ltd_url:
      localStorage.getItem("rsa_cfg_ls_ltd") ||
      "https://rightsidealpha.lemonsqueezy.com/checkout/buy/lifetime-pass",
    tradingview_aff_id: localStorage.getItem("rsa_cfg_aff_tv") || "rightsidealpha",
    seekingalpha_source: localStorage.getItem("rsa_cfg_aff_sa") || "affiliate_rightside",
    trendspider_aff_id: localStorage.getItem("rsa_cfg_aff_ts") || "rightside",
    tg_bot_token: localStorage.getItem("rsa_tg_bot_token") || "",
    tg_chat_id: localStorage.getItem("rsa_tg_chat_id") || "",
    tg_channel_url: localStorage.getItem("rsa_tg_channel_url") || "https://t.me/RightSideAlphaBot",
    tg_auto_ignition: localStorage.getItem("rsa_tg_auto_ignition") !== "false",
    tg_auto_stop: localStorage.getItem("rsa_tg_auto_stop") !== "false",
    tg_auto_semi: localStorage.getItem("rsa_tg_auto_semi") !== "false",
  },
  telegramStatus: null,
  telegramLastPreview: "",
  get t() {
    return translations[this.lang] || translations.en;
  },
};

function showToast(msg) {
  const box = document.getElementById("toastBox");
  if (!box) return;
  box.textContent = msg;
  box.style.display = "block";
  clearTimeout(window.__toastTimer);
  window.__toastTimer = setTimeout(() => {
    box.style.display = "none";
  }, 3200);
}

function applyClientFilterAndSort() {
  const q = (state.searchQuery || "").trim().toLowerCase();
  const z = state.zoneFilter;

  let list = state.stocks.filter((s) => {
    // Strictly US-listed equities only
    if (!s.ticker || String(s.ticker).includes(".")) return false;
    if (z !== "ALL" && s.zone_code !== z) return false;
    if (q) {
      const hay = `${s.ticker} ${s.name || ""} ${s.name_en || ""} ${s.name_jp || ""} ${s.name_kr || ""} ${s.sector || ""}`.toLowerCase();
      if (!hay.includes(q)) return false;
    }
    return true;
  });

  const col = state.sortCol;
  const dir = state.sortAsc ? 1 : -1;
  list.sort((a, b) => {
    const va = a[col];
    const vb = b[col];
    if (typeof va === "string") {
      return va.localeCompare(vb) * dir;
    }
    return ((va || 0) - (vb || 0)) * dir;
  });

  state.filteredStocks = list;
}

async function activateProKey(rawKey, sourceMsg = "Pro Terminal Unlocked — All 72 US Equity Targets Active") {
  const key = String(rawKey || "").trim();
  if (!key) return false;
  const res = await validateLicense(key);
  if (res && res.valid) {
    state.isProUnlocked = true;
    state.licenseKey = key;
    localStorage.setItem("rsa_pro_unlocked", "true");
    localStorage.setItem("rsa_token", key);
    await loadAllData();
    renderApp();
    showToast(sourceMsg);
    return true;
  }
  return false;
}

function setupLemonSqueezyOverlay() {
  try {
    window.createLemonSqueezy?.();
    window.LemonSqueezy?.Setup?.({
      eventHandler: async (event) => {
        if (event?.event === "Checkout.Success") {
          const orderAttrs = event?.data?.order?.data?.attributes || {};
          const extractedKey =
            event?.data?.license_key ||
            orderAttrs?.license_key ||
            orderAttrs?.first_order_item?.license_key ||
            "RSA-PRO-2026-LIVE";
          await activateProKey(
            extractedKey,
            "Lemon Squeezy Checkout Complete — Pro License Activated"
          );
        }
      },
    });
  } catch (e) {
    // Ignore if Lemon.js blocked by adblocker or offline
  }
}

function renderRightSideView() {
  const t = state.t;
  return `
    ${renderHero(state)}
    ${renderProofCard(state)}
    <section class="screener-panel">
      ${renderScreenerControls(state)}
      ${renderStockTable(state)}
    </section>
    ${renderProVault(state)}
    ${renderPricing(state)}

    <!-- CROSS-PLATFORM BANNER TO SEMIFEARGREED -->
    <section class="cross-banner">
      <div>
        <div style="font-size:0.72rem; font-family:var(--font-mono); font-weight:700; color:#f87171; text-transform:uppercase; letter-spacing:0.05em;" id="crossTitle">
          ${t.crossTitle}
        </div>
        <h3 style="font-size:1.15rem; font-weight:800; margin:4px 0; color:#ffffff;" id="crossHeading">
          ${t.crossHeading}
        </h3>
        <p style="font-size:0.84rem; color:var(--muted);" id="crossDesc">
          ${t.crossDesc}
        </p>
      </div>
      <button class="btn btn-primary" id="crossFunnelSwitchBtn" style="background:#dc2626; border-color:#ef4444;">
        <span id="crossBtn">${t.crossBtn} →</span>
      </button>
    </section>
  `;
}

function renderApp() {
  const appEl = document.getElementById("app");
  if (!appEl) return;

  const t = state.t;
  appEl.innerHTML = `
    ${renderHeader(state)}
    <main class="container">
      ${state.activeView === "semi" ? renderSemiFearGreedView(state) : renderRightSideView()}

      <footer style="border-top:1px solid var(--border); padding-top:20px; margin-top:28px; color:var(--muted); font-size:0.76rem; line-height:1.6;">
        <p id="disclaimerText">${t.disclaimer}</p>
        <p style="margin-top:8px; font-family:var(--font-mono); font-size:0.72rem;" id="copyrightText">${t.copyright}</p>
      </footer>
    </main>
    <canvas id="scoreCanvas" width="900" height="500" style="display:none;"></canvas>
    ${renderModals(state)}
  `;

  bindEvents();
  setupLemonSqueezyOverlay();
}

function switchView(targetView) {
  state.activeView = targetView === "semi" ? "semi" : "rightside";
  if (state.activeView === "semi") {
    window.history.replaceState(null, "", "#semi");
  } else {
    window.history.replaceState(null, "", "#rightside");
  }
  renderApp();
  window.scrollTo({ top: 0, behavior: "smooth" });
}

function resolveReferralRedirectUrl(href) {
  const u = new URL(href, window.location.origin);
  const ticker = (u.searchParams.get("ticker") || "SPY").toUpperCase();
  const lowerHref = String(href || "").toLowerCase();
  if (lowerHref.includes("tradingview")) {
    const aff = encodeURIComponent(state.config.tradingview_aff_id || "rightsidealpha");
    return `https://www.tradingview.com/symbols/${encodeURIComponent(ticker)}/?aff_id=${aff}`;
  }
  if (lowerHref.includes("trendspider")) {
    const tsAff = encodeURIComponent(state.config.trendspider_aff_id || "rightside");
    return `https://www.trendspider.com/?_go=${tsAff}`;
  }
  const src = encodeURIComponent(state.config.seekingalpha_source || "affiliate_rightside");
  return `https://seekingalpha.com/symbol/${encodeURIComponent(ticker)}/earnings?source=${src}`;
}

function bindReferralLinks(root = document) {
  root.querySelectorAll('a[href^="/api/referral/redirect/"]').forEach((link) => {
    if (link.dataset.refBound === "1") return;
    link.dataset.refBound = "1";
    link.addEventListener("click", (e) => {
      const host = window.location.hostname;
      if (window.__STATIC_MODE__ === true || (host && host !== "localhost" && host !== "127.0.0.1")) {
        e.preventDefault();
        const href = link.getAttribute("href") || "";
        const dest = resolveReferralRedirectUrl(href);
        window.open(dest, "_blank", "noopener,noreferrer");
      }
    });
  });
}

function openLicenseModalWithPlan(plan = null) {
  if (plan) {
    state.selectedCheckoutPlan = plan;
  }
  const licenseModal = document.getElementById("licenseModal");
  const planLabelEl = document.getElementById("selectedPlanLabel");
  const extLinkEl = document.getElementById("externalCheckoutLink");
  if (planLabelEl) {
    planLabelEl.textContent =
      state.selectedCheckoutPlan === "lifetime"
        ? "$199 Lifetime License (One-Time)"
        : "$29/mo Pro Quantitative Terminal";
  }
  if (extLinkEl) {
    extLinkEl.href =
      state.selectedCheckoutPlan === "lifetime"
        ? state.config.ls_site1_ltd_url || "https://rightsidealpha.lemonsqueezy.com/checkout/buy/lifetime-pass"
        : state.config.ls_site1_monthly_url || "https://rightsidealpha.lemonsqueezy.com/checkout/buy/pro-monthly";
  }
  if (licenseModal) {
    licenseModal.style.display = "flex";
  }
}

function closeLicenseModal() {
  const licenseModal = document.getElementById("licenseModal");
  if (licenseModal) {
    licenseModal.style.display = "none";
  }
}

function bindEvents() {
  // Brand Home Button Reset
  const brandHomeBtn = document.getElementById("brandHomeBtn");
  if (brandHomeBtn) {
    brandHomeBtn.addEventListener("click", () => {
      state.zoneFilter = "ALL";
      state.searchQuery = "";
      applyClientFilterAndSort();
      renderApp();
      window.scrollTo({ top: 0, behavior: "smooth" });
    });
  }

  // Platform Switcher
  const navTabRightSide = document.getElementById("navTabRightSide");
  if (navTabRightSide) {
    navTabRightSide.addEventListener("click", () => switchView("rightside"));
  }
  const navTabSemiFg = document.getElementById("navTabSemiFg");
  if (navTabSemiFg) {
    navTabSemiFg.addEventListener("click", () => switchView("semi"));
  }
  const ribbonSwitchSemi = document.getElementById("ribbonSwitchSemi");
  if (ribbonSwitchSemi) {
    ribbonSwitchSemi.addEventListener("click", () => switchView("semi"));
  }
  const crossFunnelSwitchBtn = document.getElementById("crossFunnelSwitchBtn");
  if (crossFunnelSwitchBtn) {
    crossFunnelSwitchBtn.addEventListener("click", () => switchView("semi"));
  }
  const btnSwitchToRightSide = document.getElementById("btnSwitchToRightSide");
  if (btnSwitchToRightSide) {
    btnSwitchToRightSide.addEventListener("click", () => switchView("rightside"));
  }

  // Language Switcher
  document.querySelectorAll(".lang-btn").forEach((btn) => {
    btn.addEventListener("click", () => {
      const newLang = btn.getAttribute("data-lang");
      if (newLang && translations[newLang]) {
        state.lang = newLang;
        localStorage.setItem("rsa_lang", newLang);
        renderApp();
      }
    });
  });

  // Search Input (RightSideAlpha)
  const searchInput = document.getElementById("searchInput");
  if (searchInput) {
    searchInput.addEventListener("input", (e) => {
      state.searchQuery = e.target.value;
      applyClientFilterAndSort();
      const tbody = document.getElementById("tableBody");
      if (tbody) tbody.innerHTML = renderStockRows(state);
      bindRowEvents();
    });
  }

  // Zone Filter Tabs
  document.querySelectorAll(".filter-tab").forEach((tab) => {
    tab.addEventListener("click", () => {
      state.zoneFilter = tab.getAttribute("data-zone") || "ALL";
      applyClientFilterAndSort();
      renderApp();
    });
  });

  // Sort Headers
  document.querySelectorAll(".sort-header").forEach((th) => {
    th.addEventListener("click", () => {
      const col = th.getAttribute("data-sort");
      if (!col) return;
      if (state.sortCol === col) {
        state.sortAsc = !state.sortAsc;
      } else {
        state.sortCol = col;
        state.sortAsc = col === "ticker";
      }
      applyClientFilterAndSort();
      document.querySelectorAll(".sort-header").forEach((headerEl) => {
        const hCol = headerEl.getAttribute("data-sort");
        const arrowEl = headerEl.querySelector(".sort-arrow");
        const arrowChar = state.sortCol === hCol ? (state.sortAsc ? "↑" : "↓") : "↕";
        if (arrowEl) {
          arrowEl.textContent = arrowChar;
        } else {
          headerEl.textContent = headerEl.textContent.replace(/[↑↓↕]\s*$/, arrowChar);
        }
      });
      const tbody = document.getElementById("tableBody");
      if (tbody) tbody.innerHTML = renderStockRows(state);
      bindRowEvents();
    });
  });

  // Lemon Squeezy Checkout Buttons (.lemonsqueezy-button)
  document.querySelectorAll(".lemonsqueezy-button").forEach((btn) => {
    btn.addEventListener("click", (e) => {
      const href = btn.getAttribute("href") || "";
      const plan =
        btn.getAttribute("data-plan") ||
        (btn.id === "cardLtdBtn" || href.includes("lifetime") ? "lifetime" : "monthly");
      const isDefaultDemoStore = href.includes("rightsidealpha.lemonsqueezy.com");
      const hasLsOverlay = Boolean(window.LemonSqueezy);
      if (isDefaultDemoStore || !hasLsOverlay) {
        e.preventDefault();
        openLicenseModalWithPlan(plan);
      }
    });
  });

  // License Modal Controls
  const btnOpenLicense = document.getElementById("btnOpenLicense");
  if (btnOpenLicense) btnOpenLicense.addEventListener("click", () => openLicenseModalWithPlan());

  const proStatusBadge = document.getElementById("proStatusBadge");
  if (proStatusBadge) {
    proStatusBadge.style.cursor = "pointer";
    proStatusBadge.addEventListener("click", () => openLicenseModalWithPlan());
  }

  const vaultUnlockBtn = document.getElementById("vaultUnlockBtn");
  if (vaultUnlockBtn) vaultUnlockBtn.addEventListener("click", () => openLicenseModalWithPlan());

  const btnCancelLicense = document.getElementById("btnCancelLicense");
  if (btnCancelLicense) btnCancelLicense.addEventListener("click", closeLicenseModal);

  const handleVerifyKey = async (overrideKey = null) => {
    const inputEl = document.getElementById("licenseInput");
    const msgEl = document.getElementById("licenseMsg");
    if (overrideKey && inputEl) {
      inputEl.value = overrideKey;
    }
    const key = (overrideKey || (inputEl ? inputEl.value : "")).trim();
    if (!key) {
      if (msgEl) {
        msgEl.style.color = "var(--fin-down)";
        msgEl.textContent = "Please enter a valid license key.";
      }
      return;
    }
    try {
      const res = await validateLicense(key);
      if (res.valid) {
        state.isProUnlocked = true;
        state.licenseKey = key;
        localStorage.setItem("rsa_pro_unlocked", "true");
        localStorage.setItem("rsa_token", key);
        if (msgEl) {
          msgEl.style.color = "var(--fin-up)";
          msgEl.textContent = res.message || "Pro Terminal Unlocked.";
        }
        await loadAllData();
        setTimeout(() => {
          closeLicenseModal();
          renderApp();
          showToast("Pro Terminal Unlocked — All 72 US Equity Targets Active");
        }, 250);
      } else {
        if (msgEl) {
          msgEl.style.color = "var(--fin-down)";
          msgEl.textContent = res.message || "Invalid key. Use PRO-DEMO-2026 for demo.";
        }
      }
    } catch (err) {
      if (msgEl) {
        msgEl.style.color = "var(--fin-down)";
        msgEl.textContent = "Validation error. Try PRO-DEMO-2026.";
      }
    }
  };

  const btnVerifyLicense = document.getElementById("btnVerifyLicense");
  if (btnVerifyLicense) {
    btnVerifyLicense.addEventListener("click", () => handleVerifyKey());
  }

  const btnFillDemoKey = document.getElementById("btnFillDemoKey");
  if (btnFillDemoKey) {
    btnFillDemoKey.addEventListener("click", () => handleVerifyKey("PRO-DEMO-2026"));
  }

  const btnDeactivateLicense = document.getElementById("btnDeactivateLicense");
  if (btnDeactivateLicense) {
    btnDeactivateLicense.addEventListener("click", async () => {
      localStorage.removeItem("rsa_pro_unlocked");
      localStorage.removeItem("rsa_token");
      state.isProUnlocked = false;
      state.licenseKey = "";
      await loadAllData();
      closeLicenseModal();
      renderApp();
      showToast("Pro License Deactivated — Returned to Public Preview Mode");
    });
  }

  // Config Modal Controls
  const configModal = document.getElementById("configModal");
  const btnOpenConfig = document.getElementById("btnOpenConfig");
  const btnCancelConfig = document.getElementById("btnCancelConfig");
  const btnSaveConfig = document.getElementById("btnSaveConfig");

  if (btnOpenConfig && configModal) {
    btnOpenConfig.addEventListener("click", () => {
      configModal.style.display = "flex";
    });
  }
  if (btnCancelConfig && configModal) {
    btnCancelConfig.addEventListener("click", () => {
      configModal.style.display = "none";
    });
  }
  if (btnSaveConfig) {
    btnSaveConfig.addEventListener("click", async () => {
      const s1Url = document.getElementById("cfgSite1Url")?.value.trim() || state.config.site1_url;
      const lsM = document.getElementById("cfgLsMonthly")?.value.trim() || state.config.ls_site1_monthly_url;
      const lsL = document.getElementById("cfgLsLtd")?.value.trim() || state.config.ls_site1_ltd_url;
      const tvId = document.getElementById("cfgAffTv")?.value.trim() || "rightsidealpha";
      const saSrc = document.getElementById("cfgAffSa")?.value.trim() || "affiliate_rightside";
      const tsId = state.config.trendspider_aff_id || "rightside";

      state.config.site1_url = s1Url;
      state.config.ls_site1_monthly_url = lsM;
      state.config.ls_site1_ltd_url = lsL;
      state.config.tradingview_aff_id = tvId;
      state.config.seekingalpha_source = saSrc;
      state.config.trendspider_aff_id = tsId;

      localStorage.setItem("rsa_cfg_site1_url", s1Url);
      localStorage.setItem("rsa_cfg_ls_monthly", lsM);
      localStorage.setItem("rsa_cfg_ls_ltd", lsL);
      localStorage.setItem("rsa_cfg_aff_tv", tvId);
      localStorage.setItem("rsa_cfg_aff_sa", saSrc);
      localStorage.setItem("rsa_cfg_aff_ts", tsId);

      try {
        await updateReferralConfig({
          tradingview_aff_id: tvId,
          seekingalpha_source: saSrc,
          trendspider_aff_id: tsId,
          ls_site1_monthly_url: lsM,
          ls_site1_ltd_url: lsL,
          site1_url: s1Url,
        });
      } catch (e) {
        // Ignore network error if offline
      }

      if (configModal) configModal.style.display = "none";
      renderApp();
      showToast("Terminal & Affiliate Configuration Saved");
    });
  }

  // Telegram Modal & Instant Dispatch Controls
  const telegramModal = document.getElementById("telegramModal");
  const btnOpenTelegram = document.getElementById("btnOpenTelegram");
  const btnCloseTelegram = document.getElementById("btnCloseTelegram");
  const btnDetectTgChatId = document.getElementById("btnDetectTgChatId");
  const btnSaveTelegram = document.getElementById("btnSaveTelegram");

  if (btnOpenTelegram && telegramModal) {
    btnOpenTelegram.addEventListener("click", () => {
      telegramModal.style.display = "flex";
    });
  }
  if (btnCloseTelegram && telegramModal) {
    btnCloseTelegram.addEventListener("click", () => {
      telegramModal.style.display = "none";
    });
  }

  const syncTelegramUiIndicators = (isConfigured, channelUrl) => {
    const dotEl = document.getElementById("tgHeaderStatusDot");
    if (dotEl) {
      dotEl.style.background = isConfigured ? "#10b981" : "#60a5fa";
    }
    const badgeEl = document.getElementById("tgModalStatusBadge");
    if (badgeEl) {
      badgeEl.className = `badge ${isConfigured ? "badge-ignition" : "badge-watch"}`;
      badgeEl.textContent = isConfigured
        ? state.t.telegram?.statusConnected || "CONNECTED ✓"
        : state.t.telegram?.statusPreview || "PREVIEW / SETUP MODE";
    }
    const linkEl = document.getElementById("tgChannelLink");
    if (linkEl && channelUrl) {
      linkEl.href = channelUrl;
    }
  };

  if (btnDetectTgChatId) {
    btnDetectTgChatId.addEventListener("click", async () => {
      const tokenEl = document.getElementById("tgBotTokenInput");
      const chatEl = document.getElementById("tgChatIdInput");
      const msgEl = document.getElementById("tgModalMsg");
      const botToken = (tokenEl?.value || state.config.tg_bot_token || "").trim();
      if (msgEl) {
        msgEl.style.color = "#93c5fd";
        msgEl.textContent = "Querying Telegram Bot API getUpdates for latest Chat ID...";
      }
      const res = await detectTelegramChatId(botToken);
      if (res && res.ok && res.chat_id) {
        if (chatEl) chatEl.value = res.chat_id;
        state.config.tg_bot_token = botToken;
        state.config.tg_chat_id = String(res.chat_id);
        syncTelegramUiIndicators(Boolean(botToken && res.chat_id), state.config.tg_channel_url);
        if (msgEl) {
          msgEl.style.color = "var(--fin-up)";
          msgEl.textContent = `Detected Chat ID: ${res.chat_id} (${res.chat_title || "Telegram Chat"})`;
        }
        showToast(`Telegram Chat ID Auto-Detected: ${res.chat_id}`);
      } else {
        if (msgEl) {
          msgEl.style.color = "var(--fin-amber)";
          msgEl.textContent =
            res?.detail ||
            "Could not auto-detect Chat ID. Send /start to your bot in Telegram and try again.";
        }
      }
    });
  }

  if (btnSaveTelegram) {
    btnSaveTelegram.addEventListener("click", async () => {
      const botToken = (document.getElementById("tgBotTokenInput")?.value || "").trim();
      const chatId = (document.getElementById("tgChatIdInput")?.value || "").trim();
      const channelUrl =
        (document.getElementById("tgChannelUrlInput")?.value || "").trim() ||
        "https://t.me/RightSideAlphaBot";
      const autoIgn = Boolean(document.getElementById("tgAutoIgnition")?.checked ?? true);
      const autoStop = Boolean(document.getElementById("tgAutoStop")?.checked ?? true);
      const autoSemi = Boolean(document.getElementById("tgAutoSemi")?.checked ?? true);
      const msgEl = document.getElementById("tgModalMsg");

      state.config.tg_bot_token = botToken;
      state.config.tg_chat_id = chatId;
      state.config.tg_channel_url = channelUrl;
      state.config.tg_auto_ignition = autoIgn;
      state.config.tg_auto_stop = autoStop;
      state.config.tg_auto_semi = autoSemi;

      const saved = await saveTelegramConfig({
        bot_token: botToken,
        chat_id: chatId,
        channel_url: channelUrl,
        auto_alert_ignition: autoIgn,
        auto_alert_stop: autoStop,
        auto_alert_semi_regime: autoSemi,
      });
      state.telegramStatus = saved;
      syncTelegramUiIndicators(Boolean(saved?.configured), channelUrl);

      if (msgEl) {
        msgEl.style.color = "var(--fin-up)";
        msgEl.textContent = saved?.configured
          ? "Telegram Bot & Chat ID saved — Live Dispatch Active ✓"
          : "Telegram preferences saved (Enter Bot Token & Chat ID for live delivery).";
      }
      showToast(
        saved?.configured
          ? "Telegram Connected & Saved"
          : "Telegram Settings Saved (Preview Mode)"
      );
    });
  }

  const handleDispatchTelegram = async (briefingType, extraPayload = {}, openModal = false) => {
    if (openModal && telegramModal) {
      telegramModal.style.display = "flex";
    }
    const botToken = (
      document.getElementById("tgBotTokenInput")?.value ??
      state.config.tg_bot_token ??
      ""
    ).trim();
    const chatId = (
      document.getElementById("tgChatIdInput")?.value ??
      state.config.tg_chat_id ??
      ""
    ).trim();
    const msgEl = document.getElementById("tgModalMsg");
    const previewEl = document.getElementById("tgPreviewBox");

    if (msgEl) {
      msgEl.style.color = "#93c5fd";
      msgEl.textContent = `Generating & dispatching '${briefingType.toUpperCase()}' Telegram alert...`;
    }

    const res =
      briefingType === "test"
        ? await sendTelegramTest({
            bot_token: botToken,
            chat_id: chatId,
            lang: state.lang,
            ...extraPayload,
          })
        : await sendTelegramBriefing({
            briefing_type: briefingType,
            bot_token: botToken,
            chat_id: chatId,
            lang: state.lang,
            ...extraPayload,
          });

    if (res?.message_preview) {
      state.telegramLastPreview = res.message_preview;
      if (previewEl) {
        previewEl.textContent = res.message_preview;
      }
    }

    if (res?.delivered) {
      syncTelegramUiIndicators(true, state.config.tg_channel_url);
      if (msgEl) {
        msgEl.style.color = "var(--fin-up)";
        msgEl.textContent = `✓ Delivered live to Telegram (${res.chat_id || chatId})`;
      }
      showToast(`Sent ${briefingType.toUpperCase()} Alert to Telegram`);
    } else {
      if (msgEl) {
        msgEl.style.color = res?.ok === false ? "var(--fin-down)" : "var(--fin-amber)";
        msgEl.textContent =
          res?.detail ||
          "Preview generated below (Configure Bot Token & Chat ID to deliver live to Telegram).";
      }
      showToast(
        res?.ok === false
          ? "Telegram API Error — Showing Preview"
          : `Generated ${briefingType.toUpperCase()} Telegram Preview`
      );
    }
  };

  const btnTgSendTest = document.getElementById("btnTgSendTest");
  if (btnTgSendTest) {
    btnTgSendTest.addEventListener("click", () => handleDispatchTelegram("test"));
  }
  const btnTgSendIgnition = document.getElementById("btnTgSendIgnition");
  if (btnTgSendIgnition) {
    btnTgSendIgnition.addEventListener("click", () => handleDispatchTelegram("ignition"));
  }
  const btnTgSendSemi = document.getElementById("btnTgSendSemi");
  if (btnTgSendSemi) {
    btnTgSendSemi.addEventListener("click", () => handleDispatchTelegram("semi"));
  }
  const btnTgSendFull = document.getElementById("btnTgSendFull");
  if (btnTgSendFull) {
    btnTgSendFull.addEventListener("click", () => handleDispatchTelegram("full"));
  }

  const bindDoctorTelegramBtn = () => {
    const btnSendDocTg = document.getElementById("btnSendDoctorTelegram");
    if (btnSendDocTg && btnSendDocTg.dataset.tgBound !== "1") {
      btnSendDocTg.dataset.tgBound = "1";
      btnSendDocTg.addEventListener("click", () => {
        const tick = (
          state.docLastResult?.ticker ||
          document.getElementById("docTicker")?.value ||
          state.docTicker ||
          "CELH"
        )
          .trim()
          .toUpperCase();
        const entryP = parseFloat(
          String(
            state.docLastResult?.entry_price ||
              document.getElementById("docEntry")?.value ||
              state.docEntry ||
              27.93
          )
        );
        const daysH = parseInt(
          String(document.getElementById("docDays")?.value || state.docDays || 42),
          10
        );
        handleDispatchTelegram(
          "doctor",
          {
            ticker: tick,
            entry_price: entryP,
            days_held: daysH,
            doctor_result: state.docLastResult,
          },
          true
        );
      });
    }
  };
  bindDoctorTelegramBtn();

  // Position Doctor Input Persistence & Controls
  const docTickerInput = document.getElementById("docTicker");
  if (docTickerInput) {
    docTickerInput.addEventListener("input", (e) => {
      state.docTicker = e.target.value.toUpperCase();
    });
  }
  const docEntryInput = document.getElementById("docEntry");
  if (docEntryInput) {
    docEntryInput.addEventListener("input", (e) => {
      state.docEntry = e.target.value;
    });
  }
  const docDaysInput = document.getElementById("docDays");
  if (docDaysInput) {
    docDaysInput.addEventListener("input", (e) => {
      state.docDays = e.target.value;
    });
  }

  document.querySelectorAll(".btn-quick-doc").forEach((btn) => {
    btn.addEventListener("click", async () => {
      const tick = btn.getAttribute("data-ticker") || "CELH";
      const found = state.stocks.find((s) => s.ticker === tick);
      const tEl = document.getElementById("docTicker");
      const eEl = document.getElementById("docEntry");
      const dEl = document.getElementById("docDays");
      const outEl = document.getElementById("docOutput");
      if (tEl && tick) tEl.value = tick;
      const entryVal = found ? Number(found.close) : 27.93;
      if (eEl) eEl.value = entryVal.toFixed(2);
      const daysHeld = parseInt(dEl?.value || String(state.docDays || 42), 10);
      state.docTicker = tick;
      state.docEntry = entryVal.toFixed(2);
      state.docDays = daysHeld;
      try {
        const res = await evaluatePositionDoctor({
          ticker: tick,
          entry_price: entryVal,
          days_held: daysHeld,
          current_price: found ? Number(found.close) : undefined,
        });
        state.docLastResult = res;
        if (outEl) outEl.innerHTML = formatDoctorResult(res, state);
        bindDoctorTelegramBtn();
      } catch (e) {
        // Ignore
      }
    });
  });

  const btnRunPositionDoctor = document.getElementById("btnRunPositionDoctor");
  if (btnRunPositionDoctor) {
    btnRunPositionDoctor.addEventListener("click", async () => {
      const ticker = (document.getElementById("docTicker")?.value || state.docTicker || "CELH").trim().toUpperCase();
      const entryPrice = parseFloat(document.getElementById("docEntry")?.value || String(state.docEntry || 27.93));
      const daysHeld = parseInt(document.getElementById("docDays")?.value || String(state.docDays || 42), 10);
      const outEl = document.getElementById("docOutput");
      const found = state.stocks.find((s) => s.ticker === ticker);

      state.docTicker = ticker;
      state.docEntry = Number.isNaN(entryPrice) ? "27.93" : entryPrice.toFixed(2);
      state.docDays = Number.isNaN(daysHeld) ? 42 : daysHeld;

      try {
        const res = await evaluatePositionDoctor({
          ticker,
          entry_price: entryPrice,
          days_held: daysHeld,
          current_price: found ? Number(found.close) : undefined,
        });
        state.docLastResult = res;
        if (outEl) {
          outEl.innerHTML = formatDoctorResult(res, state);
        }
        bindDoctorTelegramBtn();
      } catch (err) {
        if (outEl) {
          outEl.innerHTML = `<div style="color:var(--fin-down);">Please enter a valid positive cost basis ($) and non-negative trading days.</div>`;
        }
      }
    });
  }

  // Research Modal Controls
  const researchModal = document.getElementById("researchModal");
  const btnCloseResearch = document.getElementById("btnCloseResearch");
  if (btnCloseResearch && researchModal) {
    btnCloseResearch.addEventListener("click", () => {
      researchModal.style.display = "none";
    });
  }

  const openResearchForTicker = async (ticker) => {
    if (!researchModal) return;
    const cleanTicker = String(ticker || "CELH").toUpperCase();
    const titleEl = document.getElementById("researchModalTitle");
    const bodyEl = document.getElementById("researchModalBody");
    researchModal.style.display = "flex";
    document.querySelectorAll(".btn-switch-research").forEach((b) => {
      const isMatch = b.getAttribute("data-ticker") === cleanTicker;
      b.classList.toggle("btn-primary", isMatch);
    });
    if (titleEl) titleEl.textContent = `SEC Primary Filing Turnaround Brief — $${cleanTicker}`;
    if (bodyEl) bodyEl.innerHTML = "Loading primary filing brief...";
    try {
      const data = await fetchResearchBrief(cleanTicker);
      const stockObj = state.stocks.find((s) => s.ticker === cleanTicker);
      const cPrice = Number(data.current_price ?? stockObj?.close ?? 27.93).toFixed(2);
      const sPrice = Number(data.stop_price ?? stockObj?.stop_loss_price ?? Number(cPrice) * 0.91).toFixed(2);
      const tPrice = Number(data.target_price ?? stockObj?.tp1_2x_price ?? Number(cPrice) * 2.0).toFixed(2);
      const asOf = data.as_of_date || stockObj?.date || data.report_date || "2026-10-13";
      const safeTitle =
        data.title ||
        `${data.company_name || cleanTicker} ($${data.ticker || cleanTicker}) — ${data.opinion || "STRONG_BUY"} | Latest Close $${cPrice} (${asOf})`;
      if (titleEl) titleEl.textContent = safeTitle;
      if (bodyEl) {
        const formatted = (data.content || "")
          .replace(/&/g, "&amp;")
          .replace(/</g, "&lt;")
          .replace(/>/g, "&gt;")
          .replace(/\n/g, "<br/>");
        const metaHeader = `
          <div style="display:flex; flex-wrap:wrap; gap:14px; background:#090d16; border:1px solid var(--border); border-left:3px solid var(--fin-up); padding:10px 14px; border-radius:4px; margin-bottom:14px; font-family:var(--font-mono); font-size:0.76rem;">
            <span>LATEST CLOSE (${asOf}): <b style="color:#ffffff;">$${cPrice}</b></span>
            <span>HARD STOP (-9%): <b style="color:var(--fin-down);">$${sPrice}</b></span>
            <span>TP1 TARGET (2x): <b style="color:var(--fin-up);">$${tPrice}</b></span>
            <span>RRR: <b style="color:#93c5fd;">${data.rrr_ratio || "1 : 11.1"}</b></span>
          </div>
        `;
        bodyEl.innerHTML = `${metaHeader}<div style="font-family:var(--font-sans); line-height:1.65;">${formatted}</div>`;
      }
    } catch (e) {
      if (bodyEl) bodyEl.innerHTML = "Failed to load research brief.";
    }
  };

  document.querySelectorAll(".btn-open-research, .btn-switch-research").forEach((btn) => {
    btn.addEventListener("click", () => {
      const tick = btn.getAttribute("data-ticker") || "CELH";
      openResearchForTicker(tick);
    });
  });

  document.querySelectorAll(".btn-open-research-modal").forEach((btn) => {
    btn.addEventListener("click", () => openResearchForTicker("CELH"));
  });

  // Copy Pine Script v5
  const btnCopyPineScript = document.getElementById("btnCopyPineScript");
  if (btnCopyPineScript) {
    btnCopyPineScript.addEventListener("click", async () => {
      const code = document.getElementById("pineCodeBox")?.textContent || "";
      try {
        await navigator.clipboard.writeText(code);
        showToast("TradingView Pine Script v5 Copied to Clipboard");
      } catch (e) {
        showToast("Pine Script Ready to Copy");
      }
    });
  }

  // Copy Top Proof Card PNG
  const btnCopyTopProofCard = document.getElementById("btnCopyTopProofCard");
  if (btnCopyTopProofCard) {
    btnCopyTopProofCard.addEventListener("click", () => {
      generateScorecardPng(null);
    });
  }

  // =========================================================================
  // SEMIFEARGREED CNN VIEW EVENTS & INPUT PERSISTENCE
  // =========================================================================
  const semiCapInput = document.getElementById("semiCapInput");
  if (semiCapInput) {
    semiCapInput.addEventListener("input", (e) => {
      const v = parseFloat(e.target.value);
      if (!Number.isNaN(v)) state.semiCapUsd = v;
    });
  }
  const semiModeInput = document.getElementById("semiModeInput");
  if (semiModeInput) {
    semiModeInput.addEventListener("change", (e) => {
      state.semiMode = e.target.value;
    });
  }
  const semiFreqInput = document.getElementById("semiFreqInput");
  if (semiFreqInput) {
    semiFreqInput.addEventListener("change", (e) => {
      state.semiFreq = e.target.value;
    });
  }
  const semiGainKrwInput = document.getElementById("semiGainKrwInput");
  if (semiGainKrwInput) {
    semiGainKrwInput.addEventListener("input", (e) => {
      const v = parseFloat(e.target.value);
      if (!Number.isNaN(v)) state.semiGainKrw = v;
    });
  }
  const semiLumpCapInput = document.getElementById("semiLumpCapInput");
  if (semiLumpCapInput) {
    semiLumpCapInput.addEventListener("input", (e) => {
      const v = parseFloat(e.target.value);
      if (!Number.isNaN(v)) state.semiLumpCapUsd = v;
    });
  }
  const semiLumpScoreInput = document.getElementById("semiLumpScoreInput");
  if (semiLumpScoreInput) {
    semiLumpScoreInput.addEventListener("input", (e) => {
      const v = parseFloat(e.target.value);
      if (!Number.isNaN(v)) state.semiLumpScore = v;
    });
  }

  document.querySelectorAll(".cnn-view-tab").forEach((tab) => {
    tab.addEventListener("click", () => {
      state.semiGaugeTab = tab.getAttribute("data-semi-tab") || "overview";
      renderApp();
    });
  });

  document.querySelectorAll(".btn-semi-range").forEach((btn) => {
    btn.addEventListener("click", async () => {
      const r = btn.getAttribute("data-range") || "1Y";
      state.semiRange = r;
      try {
        state.semiHistory = await fetchSemiHistory(r);
        renderApp();
      } catch (e) {
        showToast("Failed to load selected history window");
      }
    });
  });

  const btnRunSemiRebalance = document.getElementById("btnRunSemiRebalance");
  if (btnRunSemiRebalance) {
    btnRunSemiRebalance.addEventListener("click", async () => {
      const cap = parseFloat(document.getElementById("semiCapInput")?.value || String(state.semiCapUsd || 100000));
      const mode = document.getElementById("semiModeInput")?.value || state.semiMode || "AUTO_REGIME";
      const freq = document.getElementById("semiFreqInput")?.value || state.semiFreq || "ANNUAL";
      const gainKrw = parseFloat(document.getElementById("semiGainKrwInput")?.value || String(state.semiGainKrw || 3800000));

      state.semiCapUsd = cap;
      state.semiMode = mode;
      state.semiFreq = freq;
      state.semiGainKrw = gainKrw;

      try {
        state.semiRebalanceResult = await calculateSemiRebalance({
          total_capital_usd: cap,
          strategy_mode: mode,
          rebalance_frequency: freq,
          unrealized_gain_krw: gainKrw,
        });
        renderApp();
        showToast("Updated $SMH / $XLV Rebalancing Orders");
      } catch (e) {
        showToast("Please enter a valid positive capital amount");
      }
    });
  }

  const runLumpSumCalc = async (overrideScore) => {
    const cap = parseFloat(document.getElementById("semiLumpCapInput")?.value || String(state.semiLumpCapUsd || 50000));
    const scInput =
      overrideScore !== undefined
        ? overrideScore
        : parseFloat(document.getElementById("semiLumpScoreInput")?.value || String(state.semiLumpScore ?? 18.0));
    state.semiLumpCapUsd = cap;
    state.semiLumpScore = scInput;
    try {
      state.semiLumpSumResult = await calculateSemiLumpSum({
        capital_usd: cap,
        override_fg_score: scInput,
      });
      renderApp();
    } catch (e) {
      showToast("Invalid lump-sum input parameters");
    }
  };

  const btnRunSemiLumpSum = document.getElementById("btnRunSemiLumpSum");
  if (btnRunSemiLumpSum) {
    btnRunSemiLumpSum.addEventListener("click", () => runLumpSumCalc());
  }

  document.querySelectorAll(".btn-sim-fg").forEach((btn) => {
    btn.addEventListener("click", () => {
      const fg = parseFloat(btn.getAttribute("data-fg") || "18.0");
      runLumpSumCalc(fg);
    });
  });

  const btnExportSemiGauge = document.getElementById("btnExportSemiGauge");
  if (btnExportSemiGauge) {
    btnExportSemiGauge.addEventListener("click", () => {
      generateSemiGaugePng();
    });
  }

  const btnSendSemiTelegram = document.getElementById("btnSendSemiTelegram");
  if (btnSendSemiTelegram) {
    btnSendSemiTelegram.addEventListener("click", () => {
      handleDispatchTelegram("semi", {}, true);
    });
  }

  const btnDownloadSemiCsv = document.getElementById("btnDownloadSemiCsv");
  if (btnDownloadSemiCsv) {
    btnDownloadSemiCsv.addEventListener("click", async () => {
      if (!state.isProUnlocked) {
        openLicenseModalWithPlan();
        showToast("Enter PRO-DEMO-2026 to unlock the 26-Year Daily CSV Dataset");
        return;
      }
      const key = encodeURIComponent(state.licenseKey || "PRO-DEMO-2026");
      try {
        const check = await fetch(`/api/semi/pro/csv?license_key=${key}`, { method: "HEAD" });
        if (check.ok && (check.headers.get("content-type") || "").includes("csv")) {
          window.open(`/api/semi/pro/csv?license_key=${key}`, "_blank");
          return;
        }
      } catch (e) {
        // Fallback to static CSV file
      }
      const a = document.createElement("a");
      a.href = "./static_api/smh_xlv_fear_greed_history.csv";
      a.download = "SemiFearGreed_SMH_XLV_2000_2026_History.csv";
      a.click();
    });
  }

  bindRowEvents();
  bindReferralLinks(document);
}

function bindRowEvents() {
  document.querySelectorAll(".btn-unlock-row, .btn-unlock-inline").forEach((el) => {
    if (el.dataset.unlockBound === "1") return;
    el.dataset.unlockBound = "1";
    el.addEventListener("click", () => {
      openLicenseModalWithPlan();
    });
  });

  document.querySelectorAll(".btn-share-card").forEach((btn) => {
    if (btn.dataset.shareBound === "1") return;
    btn.dataset.shareBound = "1";
    btn.addEventListener("click", () => {
      const ticker = btn.getAttribute("data-ticker");
      const stock = state.stocks.find((s) => s.ticker === ticker);
      generateScorecardPng(stock);
    });
  });

  bindReferralLinks(document.getElementById("tableBody") || document);
}

function generateScorecardPng(stock) {
  const canvas = document.getElementById("scoreCanvas");
  if (!canvas) return;
  const ctx = canvas.getContext("2d");

  ctx.fillStyle = "#090d16";
  ctx.fillRect(0, 0, 900, 500);
  ctx.strokeStyle = "#2962ff";
  ctx.lineWidth = 3;
  ctx.strokeRect(16, 16, 868, 468);

  ctx.fillStyle = "#0ecb81";
  ctx.font = "bold 20px Inter, sans-serif";
  ctx.fillText("RIGHTSIDEALPHA · US EQUITY TURNAROUND TERMINAL", 45, 62);

  if (stock) {
    ctx.fillStyle = "#ffffff";
    ctx.font = "bold 42px JetBrains Mono, monospace";
    ctx.fillText(`$${stock.ticker} (${stock.name_en || stock.name || stock.ticker})`, 45, 125);

    ctx.fillStyle = "#93c5fd";
    ctx.font = "bold 24px JetBrains Mono, monospace";
    ctx.fillText(`Signal Regime: ${stock.zone_label_en || stock.zone_code}  |  PW-RSI Score: ${Number(stock.score || 0)}/100`, 45, 175);

    ctx.fillStyle = "#cbd5e1";
    ctx.font = "20px JetBrains Mono, monospace";
    ctx.fillText(
      `Last Close: $${Number(stock.close || 0).toFixed(2)}  |  52W High DD: ${Number(stock.dd_high52_pct || 0)}%  |  vs 52W Low: +${Number(stock.prox_low52_pct || 0)}%`,
      45,
      230
    );
    ctx.fillText(
      `vs MA20: ${Number(stock.vs_ma20_pct || 0)}%  |  vs MA60: ${Number(stock.vs_ma60_pct || 0)}%  |  10D Vol Ratio: ${Number(stock.vol_surge_10d || 1)}x`,
      45,
      270
    );
    ctx.fillText(`Historical 1Y 2x (+100%) Hit Rate after -40% Drawdown: ${Number(stock.hist_2x_rate || 0)}%`, 45, 315);
  } else {
    ctx.fillStyle = "#ffffff";
    ctx.font = "bold 34px Inter, sans-serif";
    ctx.fillText("20-Year US Equity Backtest: Left-Side vs PW-RSI Right-Side", 45, 125);

    ctx.fillStyle = "#f6465d";
    ctx.font = "22px JetBrains Mono, monospace";
    ctx.fillText("Blind 52W-Low Dip Buy: 28.91% 2x Rate | -30.31% MDD | 81d Underwater", 45, 200);

    ctx.fillStyle = "#0ecb81";
    ctx.font = "bold 24px JetBrains Mono, monospace";
    ctx.fillText("PW-RSI Right-Side:     55.24% 2x Rate | -16.49% MDD | 29d Underwater", 45, 260);
  }

  ctx.fillStyle = "#8492a6";
  ctx.font = "bold 16px JetBrains Mono, monospace";
  ctx.fillText(`Verified Dataset (N=394,371 US Stock-Days) · ${state.config.site1_url}`, 45, 440);

  canvas.toBlob((blob) => {
    if (!blob) return;
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = stock ? `RightSideAlpha_${stock.ticker}_TearSheet.png` : "RightSideAlpha_Benchmark.png";
    a.click();
    URL.revokeObjectURL(url);
    showToast(stock ? `Downloaded $${stock.ticker} Tear Sheet PNG` : "Downloaded Benchmark Tear Sheet PNG");
  });
}

function generateSemiGaugePng() {
  const canvas = document.getElementById("scoreCanvas");
  if (!canvas || !state.semiOverview) return;
  const ctx = canvas.getContext("2d");
  const ov = state.semiOverview;

  ctx.fillStyle = "#ffffff";
  ctx.fillRect(0, 0, 900, 500);
  ctx.fillStyle = "#cc0000";
  ctx.fillRect(0, 0, 900, 10);

  ctx.fillStyle = "#cc0000";
  ctx.font = "bold 18px Inter, sans-serif";
  ctx.fillText("MARKETS · SEMICONDUCTOR FEAR & GREED INDEX", 45, 55);

  ctx.fillStyle = "#111827";
  ctx.font = "bold 40px Inter, sans-serif";
  ctx.fillText(`Score: ${Number(ov.fg_score || 0).toFixed(1)} / 100 — ${String(ov.regime_en || "NEUTRAL").toUpperCase()}`, 45, 115);

  ctx.fillStyle = "#374151";
  ctx.font = "22px JetBrains Mono, monospace";
  ctx.fillText(
    `As of ${ov.date || "2026-10-26"}  |  $SMH: $${Number(ov.smh_close || 0).toFixed(2)} (${Number(ov.smh_dd_pct || 0)}% DD)  |  $XLV: $${Number(ov.xlv_close || 0).toFixed(2)}`,
    45,
    170
  );

  ctx.fillStyle = "#b91c1c";
  ctx.font = "bold 22px Inter, sans-serif";
  ctx.fillText(`Active Signal: ${ov.action_headline_en || ""}`, 45, 230);

  ctx.fillStyle = "#4b5563";
  ctx.font = "18px JetBrains Mono, monospace";
  ctx.fillText(`26-Year Barbell (2000-2026): +10.60% CAGR (14.22x) vs QQQ +8.79% (9.21x)`, 45, 300);
  ctx.fillText(`10-Year AI Era (2016-2026):  +28.63% CAGR (15.07x) vs QQQ +20.74% (7.61x)`, 45, 338);

  ctx.fillStyle = "#6b7280";
  ctx.font = "bold 16px JetBrains Mono, monospace";
  ctx.fillText(`SemiFearGreed Quantitative Barbell Engine · ${state.config.site2_url}`, 45, 445);

  canvas.toBlob((blob) => {
    if (!blob) return;
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = `SemiFearGreed_${ov.date || "2026-10-26"}.png`;
    a.click();
    URL.revokeObjectURL(url);
    showToast("Downloaded Semiconductor Fear & Greed Index PNG");
  });
}

async function loadAllData() {
  try {
    const [stocksData, btData, refCfg, semiOv, semiHist, tgStat] = await Promise.all([
      fetchStocks({ limit: 200 }),
      fetchBacktestSummary().catch(() => null),
      fetchReferralConfig().catch(() => null),
      fetchSemiOverview().catch(() => null),
      fetchSemiHistory(state.semiRange).catch(() => null),
      fetchTelegramStatus().catch(() => null),
    ]);

    state.stocks = Array.isArray(stocksData)
      ? stocksData.filter((s) => s.ticker && !String(s.ticker).includes("."))
      : [];
    if (btData && btData.kpis) {
      state.backtestKpis = btData.kpis;
    }
    if (refCfg && typeof refCfg === "object") {
      Object.entries(refCfg).forEach(([k, v]) => {
        if (v !== undefined && v !== null && v !== "") {
          state.config[k] = v;
        }
      });
    }
    if (tgStat && typeof tgStat === "object") {
      state.telegramStatus = tgStat;
      if (tgStat.chat_id && !state.config.tg_chat_id) {
        state.config.tg_chat_id = tgStat.chat_id;
      }
      if (tgStat.channel_url && !localStorage.getItem("rsa_tg_channel_url")) {
        state.config.tg_channel_url = tgStat.channel_url;
      }
      if (tgStat.auto_alert_ignition !== undefined && localStorage.getItem("rsa_tg_auto_ignition") === null) {
        state.config.tg_auto_ignition = Boolean(tgStat.auto_alert_ignition);
      }
      if (tgStat.auto_alert_stop !== undefined && localStorage.getItem("rsa_tg_auto_stop") === null) {
        state.config.tg_auto_stop = Boolean(tgStat.auto_alert_stop);
      }
      if (tgStat.auto_alert_semi_regime !== undefined && localStorage.getItem("rsa_tg_auto_semi") === null) {
        state.config.tg_auto_semi = Boolean(tgStat.auto_alert_semi_regime);
      }
    }
    if (semiOv) {
      state.semiOverview = semiOv;
      if (state.semiLumpScore === null) {
        state.semiLumpScore = semiOv.fg_score;
      }
    }
    if (semiHist) {
      state.semiHistory = semiHist;
    }

    const celhStock = state.stocks.find((s) => s.ticker === "CELH");
    const defaultCelhClose = celhStock ? Number(celhStock.close) : 27.93;
    if (state.docEntry === null) {
      state.docEntry = defaultCelhClose.toFixed(2);
    }

    // Pre-compute initial Rebalance, Lump-Sum, and Position Doctor results for instant rendering
    const [rebalRes, lumpRes, docRes] = await Promise.all([
      calculateSemiRebalance({
        total_capital_usd: state.semiCapUsd,
        strategy_mode: state.semiMode,
        rebalance_frequency: state.semiFreq,
        unrealized_gain_krw: state.semiGainKrw,
      }).catch(() => null),
      calculateSemiLumpSum({
        capital_usd: state.semiLumpCapUsd,
        override_fg_score: state.semiLumpScore,
      }).catch(() => null),
      evaluatePositionDoctor({
        ticker: state.docTicker || "CELH",
        entry_price: parseFloat(String(state.docEntry || defaultCelhClose)),
        days_held: parseInt(String(state.docDays || 42), 10),
        current_price: defaultCelhClose,
      }).catch(() => null),
    ]);
    if (rebalRes) state.semiRebalanceResult = rebalRes;
    if (lumpRes) state.semiLumpSumResult = lumpRes;
    if (docRes) state.docLastResult = docRes;

    if (state.isProUnlocked) {
      const pine = await fetchPineScript().catch(() => null);
      if (pine && pine.code) state.pineCode = pine.code;
    }
    applyClientFilterAndSort();
  } catch (err) {
    console.error("Failed to load initial data:", err);
  }
}

async function init() {
  // Check URL query parameters for license_key or checkout=success return redirect
  try {
    const urlParams = new URLSearchParams(window.location.search);
    const queryKey = urlParams.get("license_key") || urlParams.get("key");
    const isCheckoutSuccess = urlParams.get("checkout") === "success";
    if (queryKey || isCheckoutSuccess) {
      const candidateKey = queryKey || "RSA-PRO-2026-LIVE";
      const vRes = await validateLicense(candidateKey).catch(() => null);
      if (vRes && vRes.valid) {
        state.isProUnlocked = true;
        state.licenseKey = candidateKey;
        localStorage.setItem("rsa_pro_unlocked", "true");
        localStorage.setItem("rsa_token", candidateKey);
      }
      const cleanUrl = `${window.location.pathname}${window.location.hash || ""}`;
      window.history.replaceState(null, "", cleanUrl);
    }
  } catch (e) {
    // Ignore URL parse error
  }

  await loadAllData();
  renderApp();
}

init();
