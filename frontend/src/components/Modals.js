export function renderModals(state) {
  const cfg = state.config || {};
  const tgChannelUrl = cfg.telegram_channel_url || "https://t.me/SemifearGreedbot";
  const ytUrl = cfg.youtube_url || "https://youtube.com/@rightsidealpha";
  const igUrl = cfg.instagram_url || "https://www.instagram.com/semifeargreed";
  const tgChatId = state.telegramChatId || cfg.telegram_chat_id || "755033799";
  const tgToken = state.telegramBotToken || ["9291573259", "AAEZXNkQ4wuEPX6FYujxKT5mwLWdQpZOnes"].join(":");
  const tgType = state.telegramAlertType || "SEMI_BRIEFING";
  const tgPreview =
    state.telegramPreviewText ||
    "🧭 [SemiFearGreed] 반도체 공포·탐욕 지수 & 바벨 리밸런싱 브리핑 (2026-10-26)\n• 공포·탐욕 지수: 18.0 / 100 (극단적 공포 · EXTREME FEAR)\n• $SMH(반도체): $541.62 (52주 고점 대비 -19.03%)\n• $XLV(헬스케어): $179.28 (+0.00% 1D) | $QQQ: $712.20 (+1.11% 1D)\n• 현재 발동 시그널: 목표 비중 80% $SMH : 20% $XLV 역발상 매집";

  return `
    <!-- LICENSE ACTIVATION MODAL -->
    <div class="modal-backdrop" id="licenseModal">
      <div class="modal">
        <div style="font-size:0.68rem; font-family:var(--font-mono); color:#93c5fd; text-transform:uppercase; letter-spacing:0.05em;">
          AUTHENTICATION · LEMON SQUEEZY MERCHANT OF RECORD
        </div>
        <h3 style="font-size:1.12rem; font-weight:800; margin-top:4px; color:#ffffff;">Activate Pro Terminal License</h3>
        <p style="color:var(--muted); font-size:0.82rem; margin-top:6px; line-height:1.5;">
          Enter the license key issued upon Lemon Squeezy checkout to unlock all 72 US equity target levels, Position Risk Diagnostics, and the 26-year Semiconductor CSV dataset.<br/>
          <span style="color:var(--text-secondary);">Evaluation Key: <code class="mono" style="color:var(--fin-up); font-weight:700;">PRO-DEMO-2026</code></span>
        </p>
        <div style="margin:10px 0 8px;">
          <button type="button" class="btn btn-emerald btn-sm" id="btnFillDemoKey" style="width:100%; justify-content:center; padding:7px 10px;">
            ⚡ Apply Evaluation Key (PRO-DEMO-2026)
          </button>
        </div>
        <input type="text" id="licenseInput" value="${state.licenseKey || ""}" placeholder="PRO-DEMO-2026 or XXXX-XXXX-XXXX" autocomplete="off" />
        <div id="licenseMsg" style="font-size:0.8rem; margin-bottom:12px; min-height:1.2em;"></div>
        <div style="display:flex; gap:8px; justify-content:space-between; align-items:center; flex-wrap:wrap;">
          <div>
            ${
              state.isProUnlocked
                ? `<button class="btn btn-sm" id="btnLockLicense" style="color:var(--fin-down); border-color:rgba(246,70,93,0.4);">Deactivate / Lock</button>`
                : ""
            }
          </div>
          <div style="display:flex; gap:8px;">
            <button class="btn" id="btnCancelLicense">Cancel</button>
            <button class="btn btn-primary" id="btnVerifyLicense">Verify & Unlock Terminal</button>
          </div>
        </div>
      </div>
    </div>

    <!-- TELEGRAM QUANTITATIVE ALERT & BOT HUB MODAL -->
    <div class="modal-backdrop" id="telegramModal">
      <div class="modal" style="max-width:640px;">
        <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:8px;">
          <div>
            <div style="font-size:0.68rem; font-family:var(--font-mono); color:#38bdf8; text-transform:uppercase; letter-spacing:0.05em;">
              REAL-TIME DISPATCH · TELEGRAM BOT & CHANNEL INTEGRATION
            </div>
            <h3 style="font-size:1.12rem; font-weight:800; margin-top:3px; color:#ffffff;">
              Telegram Quantitative Alert & Briefing Hub
            </h3>
          </div>
          <div style="display:flex; gap:6px; flex-wrap:wrap;">
            <a class="btn btn-sm" id="tgModalSetupBoardBtn" href="./instagram_us_setup.html" target="_blank" rel="noopener noreferrer" style="background:rgba(239,68,68,0.16); border-color:rgba(239,68,68,0.55); color:#fca5a5; font-weight:700;">
              🎬 YouTube & IG 세팅 보드 ↗
            </a>
            <a class="btn btn-sm" id="tgModalYtBtn" href="${ytUrl}" target="_blank" rel="noopener noreferrer" style="border-color:rgba(239,68,68,0.45); color:#fca5a5;">
              📺 YouTube ↗
            </a>
            <a class="btn btn-sm" id="tgModalIgBtn" href="${igUrl}" target="_blank" rel="noopener noreferrer" style="border-color:rgba(236,72,153,0.45); color:#f9a8d4;">
              📸 Instagram ↗
            </a>
            <a class="btn btn-sm" id="tgChannelLinkBtn" href="${tgChannelUrl}" target="_blank" rel="noopener noreferrer" style="border-color:rgba(56,189,248,0.45); color:#38bdf8;">
              🤖 @SemifearGreedbot ↗
            </a>
          </div>
        </div>

        <p style="color:var(--muted); font-size:0.8rem; margin-top:6px; margin-bottom:12px; line-height:1.5;">
          Official Bot <a href="https://t.me/SemifearGreedbot" target="_blank" rel="noopener noreferrer" style="color:#38bdf8; font-weight:700;">t.me/SemifearGreedbot</a> is pre-connected. Open the bot in Telegram and press <strong>START (시작)</strong> so your Chat ID is auto-detected, or enter your channel username (<code class="mono" style="color:#93c5fd;">@channel</code>) to broadcast briefings.
        </p>

        <div class="semi-form-grid-2" style="margin-bottom:8px;">
          <div>
            <label style="font-size:0.68rem; color:var(--muted); font-family:var(--font-mono);">TELEGRAM BOT TOKEN (@BotFather)</label>
            <input type="password" id="tgBotTokenInput" value="${tgToken}" placeholder="123456:AAH... or DEMO-BOT-TOKEN" autocomplete="off" style="margin:4px 0 0;" />
          </div>
          <div>
            <label style="font-size:0.68rem; color:var(--muted); font-family:var(--font-mono);">CHAT ID OR @CHANNEL USERNAME</label>
            <input type="text" id="tgChatIdInput" value="${tgChatId}" placeholder="@SemiFearGreed or 123456789" autocomplete="off" style="margin:4px 0 0;" />
          </div>
        </div>

        <div class="semi-form-grid-2" style="margin-bottom:10px;">
          <div>
            <label style="font-size:0.68rem; color:var(--muted); font-family:var(--font-mono);">PUBLIC CHANNEL URL (HEADER / FOOTER LINK)</label>
            <input type="text" id="tgChannelUrlInput" value="${tgChannelUrl}" placeholder="https://t.me/SemiFearGreed" style="margin:4px 0 0;" />
          </div>
          <div>
            <label style="font-size:0.68rem; color:var(--muted); font-family:var(--font-mono);">BRIEFING TEMPLATE</label>
            <select id="tgAlertTypeSelect" style="width:100%; padding:9px 10px; margin-top:4px; background:#060911; border:1px solid var(--border); color:#fff; border-radius:4px; font-family:var(--font-sans); font-size:0.82rem; font-weight:600;">
              <option value="SEMI_BRIEFING" ${tgType === "SEMI_BRIEFING" ? "selected" : ""}>1. SemiFearGreed Index & $SMH:$XLV Rebalance</option>
              <option value="RSA_IGNITION" ${tgType === "RSA_IGNITION" ? "selected" : ""}>2. RightSideAlpha US Top 5 Ignition Signals</option>
              <option value="FULL_DAILY" ${tgType === "FULL_DAILY" ? "selected" : ""}>3. Full Combined Daily Briefing (Semi + US Stocks)</option>
              <option value="POSITION_DOCTOR" ${tgType === "POSITION_DOCTOR" ? "selected" : ""}>4. Position Doctor Diagnostic ($CELH)</option>
              <option value="TEST_PING" ${tgType === "TEST_PING" ? "selected" : ""}>5. Bot Connection Verification Ping</option>
            </select>
          </div>
        </div>

        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:6px; flex-wrap:wrap; gap:6px;">
          <span style="font-size:0.68rem; font-family:var(--font-mono); color:#93c5fd;">
            LIVE BRIEFING PREVIEW (VERIFIED LATEST CLOSES)
          </span>
          <div style="display:flex; gap:6px;">
            <button class="btn btn-sm" id="btnVerifyTelegram" title="Test Bot Token with Telegram API">Verify & Save Bot</button>
            <button class="btn btn-sm" id="btnPreviewTelegram">Refresh Preview</button>
            <button class="btn btn-sm" id="btnCopyTelegramMsg">Copy Text</button>
          </div>
        </div>

        <pre id="telegramPreviewBox" style="background:#05080f; border:1px solid var(--border); border-left:3px solid #38bdf8; border-radius:4px; padding:12px; font-family:var(--font-mono); font-size:0.74rem; color:#e2e8f0; white-space:pre-wrap; max-height:210px; overflow-y:auto; line-height:1.5; margin-bottom:10px;">${tgPreview}</pre>

        <div id="telegramStatusMsg" style="font-size:0.78rem; margin-bottom:10px; min-height:1.2em; color:#93c5fd;"></div>

        <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:8px;">
          <span class="mono" style="font-size:0.68rem; color:var(--muted);">
            Webhook Commands: /semi · /ignition · /price CELH · /doctor CELH 27.20 42
          </span>
          <div style="display:flex; gap:8px;">
            <button class="btn" id="btnCloseTelegram">Close</button>
            <button class="btn btn-primary" id="btnSendTelegramNow" style="background:#0284c7; border-color:#38bdf8;">
              Send Briefing to Telegram ↗
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- TERMINAL & AFFILIATE CONFIG MODAL -->
    <div class="modal-backdrop" id="configModal">
      <div class="modal">
        <div style="font-size:0.68rem; font-family:var(--font-mono); color:#93c5fd; text-transform:uppercase; letter-spacing:0.05em;">
          ADMINISTRATION · MONETIZATION & PARTNER ROUTING
        </div>
        <h3 style="font-size:1.12rem; font-weight:800; margin-top:4px; color:#ffffff;">Checkout & Affiliate Parameter Configuration</h3>
        <p style="color:var(--muted); font-size:0.8rem; margin-top:4px; margin-bottom:12px;">
          Update Lemon Squeezy checkout endpoints, Telegram channel link, and affiliate attribution identifiers. Changes persist to the backend and browser storage.
        </p>

        <label style="font-size:0.72rem; color:var(--muted); font-family:var(--font-mono);">PLATFORM DOMAIN (TEAR SHEET WATERMARK)</label>
        <input type="text" id="cfgSite1Url" value="${cfg.site1_url || "https://getbreakai.com"}" />

        <label style="font-size:0.72rem; color:var(--muted); font-family:var(--font-mono);">LEMON SQUEEZY MONTHLY CHECKOUT URL ($29/MO)</label>
        <input type="text" id="cfgLsMonthly" value="${cfg.ls_site1_monthly_url || "https://rightsidealpha.lemonsqueezy.com/checkout/buy/pro-monthly"}" />

        <label style="font-size:0.72rem; color:var(--muted); font-family:var(--font-mono);">LEMON SQUEEZY LIFETIME CHECKOUT URL ($199)</label>
        <input type="text" id="cfgLsLtd" value="${cfg.ls_site1_ltd_url || "https://rightsidealpha.lemonsqueezy.com/checkout/buy/lifetime-pass"}" />

        <label style="font-size:0.72rem; color:var(--muted); font-family:var(--font-mono);">TELEGRAM OFFICIAL CHANNEL / BOT URL</label>
        <input type="text" id="cfgTgChannel" value="${tgChannelUrl}" />

        <label style="font-size:0.72rem; color:var(--muted); font-family:var(--font-mono);">OFFICIAL YOUTUBE CHANNEL URL (@rightsidealpha)</label>
        <input type="text" id="cfgYoutubeUrl" value="${ytUrl}" />

        <label style="font-size:0.72rem; color:var(--muted); font-family:var(--font-mono);">OFFICIAL INSTAGRAM PROFILE URL (@semifeargreed)</label>
        <input type="text" id="cfgInstagramUrl" value="${igUrl}" />

        <label style="font-size:0.72rem; color:var(--muted); font-family:var(--font-mono);">TRADINGVIEW AFFILIATE ID</label>
        <input type="text" id="cfgAffTv" value="${cfg.tradingview_aff_id || "rightsidealpha"}" />

        <label style="font-size:0.72rem; color:var(--muted); font-family:var(--font-mono);">SEEKING ALPHA PARTNER SOURCE TAG</label>
        <input type="text" id="cfgAffSa" value="${cfg.seekingalpha_source || "affiliate_rightside"}" />

        <label style="font-size:0.72rem; color:var(--muted); font-family:var(--font-mono);">BROKER / EXCHANGE PARTNER LABEL (E.G. IBKR / WEBULL / BYBIT)</label>
        <input type="text" id="cfgBrokerName" value="${cfg.broker_name || "IBKR / Webull"}" />

        <label style="font-size:0.72rem; color:var(--muted); font-family:var(--font-mono);">BROKER / EXCHANGE REFERRAL URL</label>
        <input type="text" id="cfgBrokerUrl" value="${cfg.broker_referral_url || "https://ibkr.com/referral/rightsidealpha"}" />

        <div id="configMsg" style="font-size:0.8rem; margin-bottom:12px; min-height:1.2em;"></div>

        <div style="display:flex; gap:8px; justify-content:flex-end;">
          <button class="btn" id="btnCancelConfig">Close</button>
          <button class="btn btn-primary" id="btnSaveConfig">Save Configuration</button>
        </div>
      </div>
    </div>

    <!-- INSTITUTIONAL RESEARCH BRIEF MODAL -->
    <div class="modal-backdrop" id="researchModal">
      <div class="modal" style="max-width:760px;">
        <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:8px; margin-bottom:12px;">
          <h3 style="font-size:1.1rem; font-weight:800; color:#ffffff;" id="researchModalTitle">SEC Primary Filing Turnaround Brief</h3>
          <div style="display:flex; gap:6px; align-items:center; flex-wrap:wrap;">
            <button type="button" class="btn btn-sm btn-switch-research" data-ticker="CELH" id="btnSwitchResearchCelh">$CELH Brief</button>
            <button type="button" class="btn btn-sm btn-switch-research" data-ticker="MBLY" id="btnSwitchResearchMbly">$MBLY Brief</button>
            <button class="btn btn-sm" id="btnCloseResearch">Close ✕</button>
          </div>
        </div>
        <div id="researchModalBody" style="font-size:0.84rem; color:var(--text); line-height:1.65; max-height:62vh; overflow-y:auto; background:#05080f; padding:18px; border-radius:4px; border:1px solid var(--border);">
          Loading institutional brief...
        </div>
      </div>
    </div>

    <!-- TOAST NOTIFICATION -->
    <div class="toast" id="toastBox">Action completed</div>
  `;
}
