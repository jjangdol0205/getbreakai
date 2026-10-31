export function renderModals(state) {
  const cfg = state.config || {};
  const tm = state.t?.modal || {};
  const ttg = state.t?.telegram || {};
  const tgSt = state.telegramStatus || {};
  const isPro = Boolean(state.isProUnlocked);
  const selectedPlan = state.selectedCheckoutPlan || "monthly";
  const planTitle =
    selectedPlan === "lifetime"
      ? "$199 Lifetime License (One-Time)"
      : "$29/mo Pro Quantitative Terminal";
  const planHref =
    selectedPlan === "lifetime"
      ? cfg.ls_site1_ltd_url || "https://rightsidealpha.lemonsqueezy.com/checkout/buy/lifetime-pass"
      : cfg.ls_site1_monthly_url || "https://rightsidealpha.lemonsqueezy.com/checkout/buy/pro-monthly";

  const tgConfigured = Boolean(
    tgSt.configured ||
      ((cfg.tg_bot_token || tgSt.has_bot_token) && (cfg.tg_chat_id || tgSt.chat_id || tgSt.has_chat_id))
  );
  const tgChannelHref = cfg.tg_channel_url || tgSt.channel_url || "https://t.me/RigjtsideAlphabot";
  const tgBotTokenVal = cfg.tg_bot_token || tgSt.bot_token_masked || "924555...d6gU";
  const tgChatIdVal = cfg.tg_chat_id || tgSt.chat_id || "";
  const autoIgnChecked = (cfg.tg_auto_ignition ?? tgSt.auto_alert_ignition ?? true) !== false;
  const autoStopChecked = (cfg.tg_auto_stop ?? tgSt.auto_alert_stop ?? true) !== false;
  const autoSemiChecked = (cfg.tg_auto_semi ?? tgSt.auto_alert_semi_regime ?? true) !== false;

  const topStock = (state.stocks || []).find((s) => s.ticker === "CELH") || (state.stocks || [])[0] || {};
  const topTicker = topStock.ticker || "CELH";
  const topClose = Number(topStock.close ?? 27.93).toFixed(2);
  const topTrg = Number(topStock.entry_trigger_price ?? 29.12).toFixed(2);
  const topStp = Number(topStock.stop_loss_price ?? 25.42).toFixed(2);
  const topTp1 = Number(topStock.tp1_2x_price ?? 55.86).toFixed(2);
  const ov = state.semiOverview || {};
  const fgScore = Number(ov.fg_score ?? 18.0).toFixed(1);
  const smhClose = Number(ov.smh_close ?? 541.62).toFixed(2);
  const xlvClose = Number(ov.xlv_close ?? 179.28).toFixed(2);
  const defaultPreview =
    state.telegramLastPreview ||
    [
      `🟢 RightSideAlpha × SemiFearGreed — Quant Signal Preview`,
      `• Top Ignition: $${topTicker} | Close $${topClose} | TRG $${topTrg} | STP (-9%) $${topStp} | TP1 (2x) $${topTp1}`,
      `• SemiFearGreed: ${fgScore}/100 (EXTREME FEAR) → 80% $SMH ($${smhClose}) : 20% $XLV ($${xlvClose})`,
      `• Click any button above to dispatch live to Telegram or generate a full preview.`,
    ].join("\n");

  return `
    <!-- LICENSE ACTIVATION MODAL -->
    <div class="modal-backdrop" id="licenseModal">
      <div class="modal">
        <div style="font-size:0.68rem; font-family:var(--font-mono); color:#93c5fd; text-transform:uppercase; letter-spacing:0.05em;">
          ${tm.licenseTag || "AUTHENTICATION · LEMON SQUEEZY MERCHANT OF RECORD"}
        </div>
        <h3 style="font-size:1.12rem; font-weight:800; margin-top:4px; color:#ffffff;">
          ${tm.licenseTitle || "Activate Pro Terminal License"}
        </h3>
        <p style="color:var(--muted); font-size:0.82rem; margin-top:6px; line-height:1.5;">
          ${tm.licenseDesc || "Enter the license key issued upon Lemon Squeezy checkout to unlock all 72 US equity target levels, Position Risk Diagnostics, and the 26-year Semiconductor CSV dataset."}<br/>
          <span style="color:var(--text-secondary);">${tm.evalKeyLabel || "Evaluation Key"}: <code class="mono" style="color:var(--fin-up); font-weight:700;">PRO-DEMO-2026</code></span>
        </p>

        <div id="checkoutPlanCallout" style="margin-top:10px; margin-bottom:10px; padding:10px 12px; background:#090d16; border:1px solid var(--border); border-left:3px solid var(--fin-blue); border-radius:4px; font-size:0.78rem;">
          <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:6px;">
            <span>Selected Tier: <b id="selectedPlanLabel" style="color:#ffffff;">${planTitle}</b></span>
            <a id="externalCheckoutLink" href="${planHref}" target="_blank" rel="noopener noreferrer" class="mono" style="color:#60a5fa; font-size:0.72rem; text-decoration:underline;">
              Open External Lemon Squeezy Checkout ↗
            </a>
          </div>
        </div>

        <div style="margin-bottom:8px;">
          <button type="button" class="btn btn-emerald btn-sm" id="btnFillDemoKey" style="width:100%; justify-content:center; padding:7px 10px;">
            ⚡ ${tm.applyDemoBtn || "Apply Evaluation Key (PRO-DEMO-2026)"}
          </button>
        </div>

        <input type="text" id="licenseInput" value="${state.licenseKey || ""}" placeholder="PRO-DEMO-2026 or RSA-PRO-2026-LIVE" autocomplete="off" />
        <div id="licenseMsg" style="font-size:0.8rem; margin-bottom:12px; min-height:1.2em;"></div>
        <div style="display:flex; gap:8px; justify-content:space-between; align-items:center; flex-wrap:wrap;">
          <div>
            ${
              isPro
                ? `<button type="button" class="btn btn-sm" id="btnDeactivateLicense" style="border-color:var(--fin-down); color:#f87171;">
                     ${tm.deactivateBtn || "Deactivate / Lock Pro License"}
                   </button>`
                : ""
            }
          </div>
          <div style="display:flex; gap:8px;">
            <button type="button" class="btn" id="btnCancelLicense">${tm.cancelBtn || "Cancel"}</button>
            <button type="button" class="btn btn-primary" id="btnVerifyLicense">${tm.verifyBtn || "Verify & Unlock Terminal"}</button>
          </div>
        </div>
      </div>
    </div>

    <!-- TERMINAL & AFFILIATE CONFIG MODAL -->
    <div class="modal-backdrop" id="configModal">
      <div class="modal">
        <div style="font-size:0.68rem; font-family:var(--font-mono); color:#93c5fd; text-transform:uppercase; letter-spacing:0.05em;">
          ${tm.configTag || "ADMINISTRATION · MONETIZATION & PARTNER ROUTING"}
        </div>
        <h3 style="font-size:1.12rem; font-weight:800; margin-top:4px; color:#ffffff;">
          ${tm.configTitle || "Checkout & Affiliate Parameter Configuration"}
        </h3>
        <p style="color:var(--muted); font-size:0.8rem; margin-top:4px; margin-bottom:12px;">
          ${tm.configDesc || "Update Lemon Squeezy checkout endpoints and affiliate attribution identifiers. Changes persist to the backend and browser storage."}
        </p>

        <label style="font-size:0.72rem; color:var(--muted); font-family:var(--font-mono);">PLATFORM DOMAIN (TEAR SHEET WATERMARK)</label>
        <input type="text" id="cfgSite1Url" value="${cfg.site1_url || "https://getbreakai.com"}" />

        <label style="font-size:0.72rem; color:var(--muted); font-family:var(--font-mono);">LEMON SQUEEZY MONTHLY CHECKOUT URL ($29/MO)</label>
        <input type="text" id="cfgLsMonthly" value="${cfg.ls_site1_monthly_url || "https://rightsidealpha.lemonsqueezy.com/checkout/buy/pro-monthly"}" />

        <label style="font-size:0.72rem; color:var(--muted); font-family:var(--font-mono);">LEMON SQUEEZY LIFETIME CHECKOUT URL ($199)</label>
        <input type="text" id="cfgLsLtd" value="${cfg.ls_site1_ltd_url || "https://rightsidealpha.lemonsqueezy.com/checkout/buy/lifetime-pass"}" />

        <label style="font-size:0.72rem; color:var(--muted); font-family:var(--font-mono);">TRADINGVIEW AFFILIATE ID</label>
        <input type="text" id="cfgAffTv" value="${cfg.tradingview_aff_id || "rightsidealpha"}" />

        <label style="font-size:0.72rem; color:var(--muted); font-family:var(--font-mono);">SEEKING ALPHA PARTNER SOURCE TAG</label>
        <input type="text" id="cfgAffSa" value="${cfg.seekingalpha_source || "affiliate_rightside"}" />

        <div id="configMsg" style="font-size:0.8rem; margin-bottom:12px; min-height:1.2em;"></div>

        <div style="display:flex; gap:8px; justify-content:flex-end;">
          <button type="button" class="btn" id="btnCancelConfig">${tm.closeBtn || "Close"}</button>
          <button type="button" class="btn btn-primary" id="btnSaveConfig">${tm.saveBtn || "Save Configuration"}</button>
        </div>
      </div>
    </div>

    <!-- INSTITUTIONAL RESEARCH BRIEF MODAL -->
    <div class="modal-backdrop" id="researchModal">
      <div class="modal" style="max-width:760px;">
        <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:8px; margin-bottom:12px;">
          <h3 style="font-size:1.05rem; font-weight:800; color:#ffffff;" id="researchModalTitle">
            ${tm.researchTitle || "SEC Primary Filing Turnaround Brief"}
          </h3>
          <div style="display:flex; gap:6px; align-items:center; flex-wrap:wrap;">
            <button type="button" class="btn btn-sm btn-switch-research" data-ticker="CELH" id="btnSwitchResearchCelh">$CELH Brief</button>
            <button type="button" class="btn btn-sm btn-switch-research" data-ticker="MBLY" id="btnSwitchResearchMbly">$MBLY Brief</button>
            <button type="button" class="btn btn-sm" id="btnCloseResearch">${tm.closeBtn || "Close"} ✕</button>
          </div>
        </div>
        <div id="researchModalBody" style="font-size:0.84rem; color:var(--text); line-height:1.65; max-height:62vh; overflow-y:auto; background:#05080f; padding:18px; border-radius:4px; border:1px solid var(--border);">
          ${tm.researchLoading || "Loading institutional brief..."}
        </div>
      </div>
    </div>

    <!-- TELEGRAM QUANT ALERT & MORNING BRIEF DISPATCH MODAL -->
    <div class="modal-backdrop" id="telegramModal">
      <div class="modal" style="max-width:660px; max-height:92vh; overflow-y:auto;">
        <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:8px;">
          <div style="font-size:0.68rem; font-family:var(--font-mono); color:#93c5fd; text-transform:uppercase; letter-spacing:0.05em;">
            ${ttg.tag || "REAL-TIME QUANT DISPATCH · TELEGRAM BOT & CHANNEL INTEGRATION"}
          </div>
          <div style="display:flex; align-items:center; gap:8px; flex-wrap:wrap;">
            <span
              id="tgModalStatusBadge"
              class="badge ${tgConfigured ? "badge-ignition" : "badge-watch"}"
            >
              ${tgConfigured ? ttg.statusConnected || "CONNECTED ✓" : ttg.statusPreview || "PREVIEW / SETUP MODE"}
            </span>
            <a
              id="tgChannelLink"
              href="${tgChannelHref}"
              target="_blank"
              rel="noopener noreferrer"
              class="mono"
              style="font-size:0.72rem; color:#60a5fa; text-decoration:underline;"
            >
              ${ttg.openChannelBtn || "Open Telegram Bot / Channel ↗"}
            </a>
          </div>
        </div>

        <h3 style="font-size:1.12rem; font-weight:800; margin-top:6px; color:#ffffff;">
          📲 ${ttg.title || "Telegram Quant Signal & Morning Brief Dispatch"}
        </h3>
        <p style="color:var(--muted); font-size:0.8rem; margin-top:4px; line-height:1.45;">
          ${ttg.desc || "Receive real-time Right-Side Ignition breakouts, Position Doctor -9% / 55D stop alerts, and Semiconductor Fear & Greed 80:20 contrarian signals directly on Telegram."}
        </p>

        <!-- Step-by-step Quick Setup Guide -->
        <div style="margin:10px 0 12px; padding:10px 12px; background:#090d16; border:1px solid var(--border); border-left:3px solid #60a5fa; border-radius:4px; font-size:0.74rem; color:var(--text-secondary); display:grid; grid-template-columns:repeat(auto-fit, minmax(180px, 1fr)); gap:6px;">
          <div><b style="color:#93c5fd;">${ttg.step1 || "1. Create bot via @BotFather -> Paste Token"}</b></div>
          <div><b style="color:#93c5fd;">${ttg.step2 || "2. Send /start to your bot -> Click 'Auto-Detect Chat ID'"}</b></div>
          <div><b style="color:#93c5fd;">${ttg.step3 || "3. Click 'Save & Send Test Ping'"}</b></div>
        </div>

        <div style="display:grid; grid-template-columns:repeat(auto-fit, minmax(240px, 1fr)); gap:10px;">
          <div>
            <label style="font-size:0.68rem; color:var(--muted); font-family:var(--font-mono);">
              ${ttg.botTokenLabel || "TELEGRAM BOT TOKEN (@BotFather)"}
            </label>
            <input
              type="password"
              id="tgBotTokenInput"
              value="${tgBotTokenVal}"
              placeholder="1234567890:AAH..."
              autocomplete="off"
              style="margin:4px 0 8px;"
            />
          </div>
          <div>
            <label style="font-size:0.68rem; color:var(--muted); font-family:var(--font-mono);">
              ${ttg.chatIdLabel || "TELEGRAM CHAT ID OR @CHANNEL"}
            </label>
            <div style="display:flex; gap:6px; align-items:center; margin:4px 0 8px;">
              <input
                type="text"
                id="tgChatIdInput"
                value="${tgChatIdVal}"
                placeholder="e.g. 123456789 or @channel"
                autocomplete="off"
                style="margin:0; flex:1;"
              />
              <button type="button" class="btn btn-sm" id="btnDetectTgChatId" style="white-space:nowrap; padding:8px 10px; border-color:rgba(96,165,250,0.45); color:#93c5fd;">
                ${ttg.detectChatIdBtn || "🔍 Auto-Detect Chat ID"}
              </button>
            </div>
          </div>
        </div>

        <label style="font-size:0.68rem; color:var(--muted); font-family:var(--font-mono);">
          ${ttg.channelUrlLabel || "TELEGRAM CHANNEL / BOT LINK URL"}
        </label>
        <input
          type="text"
          id="tgChannelUrlInput"
          value="${tgChannelHref}"
          placeholder="https://t.me/RightSideAlphaBot"
          style="margin:4px 0 10px;"
        />

        <!-- Checkboxes for Auto-Alerts -->
        <div style="margin-bottom:12px; padding:10px 12px; background:#080c15; border:1px solid var(--border); border-radius:4px;">
          <div style="font-size:0.68rem; font-family:var(--font-mono); color:var(--muted); margin-bottom:6px; text-transform:uppercase;">
            ${ttg.autoAlertsLabel || "AUTOMATED SIGNAL SUBSCRIPTIONS"}
          </div>
          <div style="display:flex; flex-direction:column; gap:6px; font-size:0.78rem; color:var(--text-secondary);">
            <label style="display:flex; align-items:center; gap:8px; cursor:pointer;">
              <input type="checkbox" id="tgAutoIgnition" ${autoIgnChecked ? "checked" : ""} style="width:15px; height:15px; margin:0; padding:0; accent-color:var(--fin-up);" />
              <span>${ttg.chkIgnition || "Right-Side 4-Factor Ignition Breakout Alerts"}</span>
            </label>
            <label style="display:flex; align-items:center; gap:8px; cursor:pointer;">
              <input type="checkbox" id="tgAutoStop" ${autoStopChecked ? "checked" : ""} style="width:15px; height:15px; margin:0; padding:0; accent-color:var(--fin-up);" />
              <span>${ttg.chkStop || "Position Doctor -9% Hard Stop & 55D Time-Stop Alerts"}</span>
            </label>
            <label style="display:flex; align-items:center; gap:8px; cursor:pointer;">
              <input type="checkbox" id="tgAutoSemi" ${autoSemiChecked ? "checked" : ""} style="width:15px; height:15px; margin:0; padding:0; accent-color:var(--fin-up);" />
              <span>${ttg.chkSemi || "Semiconductor Fear & Greed Extreme Regime (<25 / >75) Alerts"}</span>
            </label>
          </div>
        </div>

        <!-- Instant Dispatch Action Bar (4 buttons) -->
        <div style="margin-bottom:10px;">
          <div style="font-size:0.68rem; font-family:var(--font-mono); color:var(--muted); margin-bottom:6px; text-transform:uppercase;">
            ${ttg.dispatchBarLabel || "INSTANT 1-CLICK SIGNAL DISPATCH & PREVIEW"}
          </div>
          <div style="display:grid; grid-template-columns:repeat(auto-fit, minmax(140px, 1fr)); gap:6px;">
            <button type="button" class="btn btn-sm" id="btnTgSendTest" style="justify-content:center; padding:7px 8px; border-color:rgba(16,185,129,0.45); color:#34d399;">
              🚀 Test Ping
            </button>
            <button type="button" class="btn btn-sm" id="btnTgSendIgnition" style="justify-content:center; padding:7px 8px; border-color:rgba(96,165,250,0.45); color:#93c5fd;">
              📊 Ignition Top 5
            </button>
            <button type="button" class="btn btn-sm" id="btnTgSendSemi" style="justify-content:center; padding:7px 8px; border-color:rgba(248,113,113,0.45); color:#fca5a5;">
              🧭 Semi 80:20 Signal
            </button>
            <button type="button" class="btn btn-sm" id="btnTgSendFull" style="justify-content:center; padding:7px 8px; border-color:rgba(251,191,36,0.45); color:#fde68a;">
              📑 Full Morning Brief
            </button>
          </div>
        </div>

        <div id="tgModalMsg" style="font-size:0.78rem; margin-bottom:8px; min-height:1.2em; color:#93c5fd;"></div>

        <div style="margin-bottom:14px;">
          <div style="font-size:0.66rem; font-family:var(--font-mono); color:var(--muted); margin-bottom:4px; text-transform:uppercase;">
            ${ttg.previewLabel || "LIVE TELEGRAM MESSAGE PREVIEW"}
          </div>
          <pre
            id="tgPreviewBox"
            class="mono"
            style="background:#05080f; border:1px solid var(--border); border-left:3px solid var(--fin-up); border-radius:4px; padding:10px 12px; font-size:0.73rem; color:var(--text-secondary); white-space:pre-wrap; word-break:break-word; max-height:175px; overflow-y:auto; line-height:1.45;"
          >${defaultPreview}</pre>
        </div>

        <div style="display:flex; gap:8px; justify-content:flex-end; align-items:center;">
          <button type="button" class="btn" id="btnCloseTelegram">${ttg.closeBtn || tm.closeBtn || "Close"}</button>
          <button type="button" class="btn btn-primary" id="btnSaveTelegram">${ttg.saveBtn || "Save Telegram Settings"}</button>
        </div>
      </div>
    </div>

    <!-- TOAST NOTIFICATION -->
    <div class="toast" id="toastBox">Action completed</div>
  `;
}
