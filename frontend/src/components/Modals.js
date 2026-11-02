export function renderModals(state) {
  const cfg = state.config || {};
  const tgChannelUrl = cfg.telegram_channel_url || "https://t.me/truthofmarketss";
  const ytUrl = cfg.youtube_url || "https://youtube.com/@rightsidealpha";
  const igUrl = cfg.instagram_url || "https://www.instagram.com/rightsidealpha";
  const tgChatId = state.telegramChatId || cfg.telegram_chat_id || "@truthofmarketss";
  const tgToken = state.telegramBotToken || "DEMO-BOT-TOKEN";
  const tgType = state.telegramAlertType || "SEMI_BRIEFING";
  const ov = state.semiOverview || {};
  const ovDate = ov.date || "2026-10-30";
  const ovScore = Number(ov.fg_score ?? 18.0).toFixed(1);
  const ovRegime = String(ov.regime_en || "EXTREME FEAR").toUpperCase();
  const ovSmh = Number(ov.smh_close ?? 522.49).toFixed(2);
  const ovDd = Number(ov.smh_dd_pct ?? -22.23).toFixed(2);
  const ovRsi = Number(ov.smh_rsi ?? 40.6).toFixed(1);
  const ovXlv = Number(ov.xlv_close ?? 184.87).toFixed(2);
  const ovQqq = Number(ov.qqq_close ?? 690.49).toFixed(2);
  const ovW1 = ov.recommended_smh_weight ?? 80;
  const ovW2 = ov.recommended_xlv_weight ?? 20;
  const tgPreview =
    state.telegramPreviewText ||
    `🧭 [SemiFearGreed] Daily Semiconductor & Barbell Briefing (${ovDate})\n• Fear & Greed Score: ${ovScore} / 100 (${ovRegime})\n• $SMH (Semiconductor): $${ovSmh} (${ovDd}% 52W DD | RSI ${ovRsi})\n• $XLV (Healthcare Vault): $${ovXlv} | $QQQ: $${ovQqq}\n• Active Signal: Target ${ovW1}% $SMH : ${ovW2}% $XLV Barbell Allocation`;

  return `
    <!-- LICENSE ACTIVATION MODAL -->
    <div class="modal-backdrop" id="licenseModal">
      <div class="modal">
        <div style="font-size:0.68rem; font-family:var(--font-mono); color:#93c5fd; text-transform:uppercase; letter-spacing:0.05em;">
          AUTHENTICATION · LEMON SQUEEZY MERCHANT OF RECORD
        </div>
        <h3 style="font-size:1.12rem; font-weight:800; margin-top:4px; color:#ffffff;">Activate Pro Terminal License</h3>
        <p style="color:var(--muted); font-size:0.82rem; margin-top:6px; line-height:1.5;">
          Enter the license key issued upon Lemon Squeezy checkout to unlock all 72 US equity target levels, Daily VIP Ignition Order Book, Position Sizing Calculator, Position Doctor, and the 26-year Semiconductor CSV dataset.
        </p>
        <div style="display:grid; grid-template-columns:1fr 1fr; gap:8px; margin:12px 0 10px;">
          <a class="btn btn-primary btn-sm lemonsqueezy-button" href="${cfg.ls_site1_monthly_url || "https://truthofmarket.lemonsqueezy.com/checkout/buy/bad98d00-7175-41f6-9d58-eeb2471d0da4"}?embed=1" target="_blank" rel="noopener noreferrer" style="justify-content:center; padding:8px 10px; font-weight:700;">
            🍋 Subscribe Pro ($29/mo) ↗
          </a>
          <a class="btn btn-emerald btn-sm lemonsqueezy-button" href="${cfg.ls_site1_ltd_url || "https://truthofmarket.lemonsqueezy.com/checkout/buy/00c9f6e1-c8be-42a4-b5a5-e05af1a41ed9"}?embed=1" target="_blank" rel="noopener noreferrer" style="justify-content:center; padding:8px 10px; font-weight:700;">
            🏆 Lifetime Pass ($199) ↗
          </a>
        </div>
        <input type="text" id="licenseInput" value="${state.licenseKey || ""}" placeholder="Enter Lemon Squeezy License Key (XXXX-XXXX-XXXX-XXXX)" autocomplete="off" />
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
            <a class="btn btn-sm" id="tgModalYtBtn" href="${ytUrl}" target="_blank" rel="noopener noreferrer" style="border-color:rgba(239,68,68,0.45); color:#fca5a5;">
              📺 YouTube ↗
            </a>
            <a class="btn btn-sm" id="tgModalIgBtn" href="${igUrl}" target="_blank" rel="noopener noreferrer" style="border-color:rgba(236,72,153,0.45); color:#f9a8d4;">
              📸 Instagram ↗
            </a>
            <a class="btn btn-sm" id="tgChannelLinkBtn" href="${tgChannelUrl}" target="_blank" rel="noopener noreferrer" style="border-color:rgba(56,189,248,0.45); color:#38bdf8;">
              ✈️ @truthofmarketss ↗
            </a>
          </div>
        </div>

        <p style="color:var(--muted); font-size:0.8rem; margin-top:6px; margin-bottom:12px; line-height:1.5;">
          Join our Official Broadcast Channel <a href="${tgChannelUrl}" target="_blank" rel="noopener noreferrer" style="color:#38bdf8; font-weight:700;">t.me/truthofmarketss</a> (<code class="mono" style="color:#93c5fd;">@truthofmarketss</code>) for automated daily US Market & Semiconductor briefings.
        </p>

        ${
          state.isAdminAuthenticated
            ? `<div class="semi-form-grid-2" style="margin-bottom:8px;">
          <div>
            <label style="font-size:0.68rem; color:var(--muted); font-family:var(--font-mono);">TELEGRAM BOT PROFILE (@BotFather)</label>
            <input type="text" id="tgBotTokenInput" value="${tgToken}" placeholder="DEMO-BOT-TOKEN" autocomplete="off" style="margin:4px 0 0; -webkit-text-security:disc;" />
          </div>
          <div>
            <label style="font-size:0.68rem; color:var(--muted); font-family:var(--font-mono);">CHAT ID OR @CHANNEL USERNAME</label>
            <input type="text" id="tgChatIdInput" value="${tgChatId}" placeholder="@truthofmarketss" autocomplete="off" style="margin:4px 0 0;" />
          </div>
        </div>`
            : ""
        }

        <div class="${state.isAdminAuthenticated ? "semi-form-grid-2" : ""}" style="margin-bottom:10px;">
          ${
            state.isAdminAuthenticated
              ? `<div>
            <label style="font-size:0.68rem; color:var(--muted); font-family:var(--font-mono);">PUBLIC CHANNEL URL (HEADER / FOOTER LINK)</label>
            <input type="text" id="tgChannelUrlInput" value="${tgChannelUrl}" placeholder="https://t.me/truthofmarketss" style="margin:4px 0 0;" />
          </div>`
              : ""
          }
          <div>
            <label style="font-size:0.68rem; color:var(--muted); font-family:var(--font-mono);">BRIEFING TEMPLATE</label>
            <select id="tgAlertTypeSelect" style="width:100%; padding:9px 10px; margin-top:4px; background:#060911; border:1px solid var(--border); color:#fff; border-radius:4px; font-family:var(--font-sans); font-size:0.82rem; font-weight:600;">
              <option value="SEMI_BRIEFING" ${tgType === "SEMI_BRIEFING" ? "selected" : ""}>1. SemiFearGreed Index & $SMH:$XLV Rebalance</option>
              <option value="RSA_IGNITION" ${tgType === "RSA_IGNITION" ? "selected" : ""}>2. RightSideAlpha US Top 5 Ignition Signals</option>
              <option value="FULL_DAILY" ${tgType === "FULL_DAILY" ? "selected" : ""}>3. Full Combined Daily Briefing (Semi + US Stocks)</option>
              <option value="POSITION_DOCTOR" ${tgType === "POSITION_DOCTOR" ? "selected" : ""}>4. Position Doctor Diagnostic ($CELH)</option>
              ${
                state.isAdminAuthenticated
                  ? `<option value="TEST_PING" ${tgType === "TEST_PING" ? "selected" : ""}>5. Bot Connection Verification Ping</option>`
                  : ""
              }
            </select>
          </div>
        </div>

        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:6px; flex-wrap:wrap; gap:6px;">
          <span style="font-size:0.68rem; font-family:var(--font-mono); color:#93c5fd;">
            LIVE BRIEFING PREVIEW (VERIFIED LATEST CLOSES)
          </span>
          <div style="display:flex; gap:6px;">
            ${
              state.isAdminAuthenticated
                ? `<button class="btn btn-sm" id="btnVerifyTelegram" title="Test Bot Token with Telegram API">Verify & Save Bot</button>`
                : ""
            }
            <button class="btn btn-sm" id="btnPreviewTelegram">Refresh Preview</button>
            <button class="btn btn-sm" id="btnCopyTelegramMsg">Copy Text</button>
          </div>
        </div>

        <pre id="telegramPreviewBox" style="background:#05080f; border:1px solid var(--border); border-left:3px solid #38bdf8; border-radius:4px; padding:12px; font-family:var(--font-mono); font-size:0.74rem; color:#e2e8f0; white-space:pre-wrap; max-height:210px; overflow-y:auto; line-height:1.5; margin-bottom:10px;">${tgPreview}</pre>

        <div id="telegramStatusMsg" style="font-size:0.78rem; margin-bottom:10px; min-height:1.2em; color:#93c5fd;"></div>

        <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:8px;">
          <span class="mono" style="font-size:0.68rem; color:var(--muted);">
            Official Channel: @truthofmarketss · Live Daily Briefings
          </span>
          <div style="display:flex; gap:8px;">
            <button class="btn" id="btnCloseTelegram">Close</button>
            <a class="btn btn-primary" href="${tgChannelUrl}" target="_blank" rel="noopener noreferrer" style="background:#0284c7; border-color:#38bdf8;">
              Join Telegram Channel ↗
            </a>
            ${
              state.isAdminAuthenticated
                ? `<button class="btn btn-primary" id="btnSendTelegramNow" style="background:#059669; border-color:#10b981;">
              Send Briefing to Telegram ↗
            </button>`
                : ""
            }
          </div>
        </div>
      </div>
    </div>

    <!-- ADMIN LOGIN MODAL (SHA-256 PROTECTED, NO PLAINTEXT IN GIT) -->
    <div class="modal-backdrop" id="adminLoginModal">
      <div class="modal" style="max-width:440px;">
        <div style="font-size:0.68rem; font-family:var(--font-mono); color:#f59e0b; text-transform:uppercase; letter-spacing:0.05em;">
          RESTRICTED ACCESS · ADMINISTRATOR AUTHENTICATION
        </div>
        <h3 style="font-size:1.12rem; font-weight:800; margin-top:4px; color:#ffffff;">
          🔒 Admin Terminal Login
        </h3>
        <p style="color:var(--muted); font-size:0.8rem; margin-top:6px; margin-bottom:12px; line-height:1.5;">
          Enter your Administrator ID and Password to unlock Terminal Configuration, Lemon Squeezy Checkout Setup, Affiliate Routing, and full Pro Terminal access.
        </p>

        <label style="font-size:0.72rem; color:var(--muted); font-family:var(--font-mono);">ADMIN ID</label>
        <input type="text" id="adminIdInput" placeholder="Enter Admin ID" autocomplete="off" />

        <label style="font-size:0.72rem; color:var(--muted); font-family:var(--font-mono);">ADMIN ACCESS KEY</label>
        <input type="text" id="adminPwInput" placeholder="Enter Admin Password" autocomplete="off" style="-webkit-text-security:disc;" />

        <div id="adminLoginMsg" style="font-size:0.8rem; margin-bottom:12px; min-height:1.2em;"></div>

        <div style="display:flex; gap:8px; justify-content:flex-end;">
          <button class="btn" id="btnCancelAdminLogin">Cancel</button>
          <button class="btn btn-primary" id="btnSubmitAdminLogin">Login as Admin</button>
        </div>
      </div>
    </div>

    <!-- TERMINAL & AFFILIATE CONFIG MODAL -->
    <div class="modal-backdrop" id="configModal">
      <div class="modal" style="max-width:640px;">
        <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:8px;">
          <div>
            <div style="font-size:0.68rem; font-family:var(--font-mono); color:#93c5fd; text-transform:uppercase; letter-spacing:0.05em;">
              ADMINISTRATION · MONETIZATION & PARTNER ROUTING
            </div>
            <h3 style="font-size:1.12rem; font-weight:800; margin-top:4px; color:#ffffff;">Checkout & Affiliate Parameter Configuration</h3>
          </div>
          <button class="btn btn-sm" id="btnAdminLogout" style="border-color:rgba(246,70,93,0.45); color:var(--fin-down);">
            🔒 Admin Logout
          </button>
        </div>
        <p style="color:var(--muted); font-size:0.8rem; margin-top:4px; margin-bottom:10px;">
          Update Lemon Squeezy checkout endpoints, Telegram channel link, and affiliate attribution identifiers. Changes persist to the backend and browser storage.
        </p>

        <div style="background:rgba(37,99,235,0.1); border:1px solid rgba(59,130,246,0.35); border-radius:4px; padding:10px 12px; margin-bottom:12px; display:flex; gap:6px; align-items:center; justify-content:space-between; flex-wrap:wrap;">
          <span class="mono" style="font-size:0.7rem; color:#93c5fd; font-weight:700;">⚡ QUICK PARTNER PORTALS:</span>
          <div style="display:flex; gap:6px; flex-wrap:wrap;">
            <a class="btn btn-sm" href="https://app.lemonsqueezy.com/products" target="_blank" rel="noopener noreferrer" style="font-size:0.7rem; padding:4px 8px;">🍋 Lemon Squeezy ↗</a>
            <a class="btn btn-sm" href="https://www.tradingview.com/partner-program/" target="_blank" rel="noopener noreferrer" style="font-size:0.7rem; padding:4px 8px;">📈 TradingView Aff ↗</a>
            <a class="btn btn-sm" href="https://www.interactivebrokers.com/en/general/refer-a-friend.php" target="_blank" rel="noopener noreferrer" style="font-size:0.7rem; padding:4px 8px;">🏦 IBKR Referral ↗</a>
            <a class="btn btn-sm" href="https://affiliates.seekingalpha.com/" target="_blank" rel="noopener noreferrer" style="font-size:0.7rem; padding:4px 8px;">📊 Seeking Alpha Aff ↗</a>
          </div>
        </div>

        <label style="font-size:0.72rem; color:var(--muted); font-family:var(--font-mono);">PLATFORM DOMAIN (TEAR SHEET WATERMARK)</label>
        <input type="text" id="cfgSite1Url" value="${cfg.site1_url || "https://truthofmarket.com"}" />

        <label style="font-size:0.72rem; color:var(--muted); font-family:var(--font-mono);">LEMON SQUEEZY MONTHLY CHECKOUT URL ($29/MO)</label>
        <input type="text" id="cfgLsMonthly" value="${cfg.ls_site1_monthly_url || "https://truthofmarket.lemonsqueezy.com/checkout/buy/bad98d00-7175-41f6-9d58-eeb2471d0da4"}" />

        <label style="font-size:0.72rem; color:var(--muted); font-family:var(--font-mono);">LEMON SQUEEZY LIFETIME CHECKOUT URL ($199)</label>
        <input type="text" id="cfgLsLtd" value="${cfg.ls_site1_ltd_url || "https://truthofmarket.lemonsqueezy.com/checkout/buy/00c9f6e1-c8be-42a4-b5a5-e05af1a41ed9"}" />

        <label style="font-size:0.72rem; color:var(--muted); font-family:var(--font-mono);">TELEGRAM OFFICIAL CHANNEL / BOT URL</label>
        <input type="text" id="cfgTgChannel" value="${tgChannelUrl}" />

        <label style="font-size:0.72rem; color:var(--muted); font-family:var(--font-mono);">OFFICIAL YOUTUBE CHANNEL URL (@rightsidealpha)</label>
        <input type="text" id="cfgYoutubeUrl" value="${ytUrl}" />

        <label style="font-size:0.72rem; color:var(--muted); font-family:var(--font-mono);">OFFICIAL INSTAGRAM PROFILE URL (@rightsidealpha)</label>
        <input type="text" id="cfgInstagramUrl" value="${igUrl}" />

        <label style="font-size:0.72rem; color:var(--muted); font-family:var(--font-mono);">TRADINGVIEW AFFILIATE ID</label>
        <input type="text" id="cfgAffTv" value="${cfg.tradingview_aff_id || "1173809"}" />

        <label style="font-size:0.72rem; color:var(--muted); font-family:var(--font-mono);">SEEKING ALPHA PARTNER SOURCE TAG</label>
        <input type="text" id="cfgAffSa" value="${cfg.seekingalpha_source || "better_life333"}" />

        <label style="font-size:0.72rem; color:var(--muted); font-family:var(--font-mono);">BROKER / EXCHANGE PARTNER LABEL (E.G. BITGET / IBKR)</label>
        <input type="text" id="cfgBrokerName" value="${cfg.broker_name || "Bitget (7nja)"}" />

        <label style="font-size:0.72rem; color:var(--muted); font-family:var(--font-mono);">BROKER / EXCHANGE REFERRAL URL</label>
        <input type="text" id="cfgBrokerUrl" value="${cfg.broker_referral_url || "https://www.bitget.com/referral/register?clacCode=7nja"}" />

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

    <!-- LEGAL, PRIVACY, REFUND POLICY & SUPPORT MODAL -->
    <div class="modal-backdrop" id="legalModal">
      <div class="modal" style="max-width:740px;">
        <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:8px; margin-bottom:12px;">
          <div>
            <div style="font-size:0.68rem; font-family:var(--font-mono); color:#93c5fd; text-transform:uppercase; letter-spacing:0.05em;">
              LEGAL & COMPLIANCE · MERCHANT OF RECORD: LEMON SQUEEZY
            </div>
            <h3 style="font-size:1.1rem; font-weight:800; color:#ffffff; margin-top:3px;" id="legalModalTitle">
              Terms of Service, Privacy Policy & Refund Policy
            </h3>
          </div>
          <div style="display:flex; gap:6px; flex-wrap:wrap;">
            <button type="button" class="btn btn-sm btn-legal-tab" data-legal-tab="terms">Terms of Service</button>
            <button type="button" class="btn btn-sm btn-legal-tab" data-legal-tab="privacy">Privacy Policy</button>
            <button type="button" class="btn btn-sm btn-legal-tab" data-legal-tab="refund">Refund Policy</button>
            <button type="button" class="btn btn-sm btn-legal-tab" data-legal-tab="support">Support Contact</button>
            <button type="button" class="btn btn-sm" id="btnCloseLegalModal">Close ✕</button>
          </div>
        </div>
        <div id="legalModalBody" style="font-size:0.82rem; color:var(--text); line-height:1.68; max-height:62vh; overflow-y:auto; background:#05080f; padding:18px; border-radius:4px; border:1px solid var(--border);">
          <div data-legal-section="terms">
            <h4 style="color:#ffffff; font-size:0.95rem; font-weight:800; margin-bottom:6px;">1. Terms of Service & Non-Advisory Disclosure</h4>
            <p style="color:var(--muted); margin-bottom:10px;">
              RightSideAlpha and SemiFearGreed (<code class="mono">truthofmarket.com</code>) provide quantitative financial data analytics, empirical backtesting outputs (2000–2026), and algorithmic screening tools for US-listed equities and ETFs. Nothing on this platform constitutes personalized investment advice, brokerage solicitation, legal advice, or tax counsel. Users are solely responsible for their own investment decisions and trade executions.
            </p>
            <p style="color:var(--muted); margin-bottom:12px;">
              Pro Terminal licenses grant single-user access to quantitative target levels, daily SEC primary-filing briefs, Position Doctor diagnostics, and Pine Script v5 indicators. Redistribution or unauthorized sharing of license keys or private VIP Telegram invite links is strictly prohibited.
            </p>
          </div>
          <div data-legal-section="privacy" style="border-top:1px solid var(--border); padding-top:12px; margin-top:12px;">
            <h4 style="color:#ffffff; font-size:0.95rem; font-weight:800; margin-bottom:6px;">2. Privacy Policy</h4>
            <p style="color:var(--muted); margin-bottom:10px;">
              We respect your financial privacy. Portfolio inputs entered into the Position Sizing Calculator, Position Doctor, or $SMH:$XLV Barbell Rebalancing Engine are processed locally in your browser and are never sold or shared with third parties. Payment processing and billing data are handled securely by our Merchant of Record, <b>Lemon Squeezy, LLC</b>, under PCI-DSS compliance.
            </p>
          </div>
          <div data-legal-section="refund" style="border-top:1px solid var(--border); padding-top:12px; margin-top:12px;">
            <h4 style="color:#ffffff; font-size:0.95rem; font-weight:800; margin-bottom:6px;">3. Subscription Cancellation & Refund Policy</h4>
            <p style="color:var(--muted); margin-bottom:10px;">
              Monthly Pro subscriptions ($29/mo) can be canceled at any time with one click via your Lemon Squeezy customer billing portal or by contacting support; access remains active through the end of the current billing period with zero cancellation fees. Because digital quantitative data, downloadable 26.8-year CSV datasets, and Pine Script v5 source code are delivered immediately upon activation, Lifetime Pass ($199) and activated digital licenses are non-refundable once accessed, except where required by applicable consumer protection law or in cases of duplicate billing.
            </p>
          </div>
          <div data-legal-section="support" style="border-top:1px solid var(--border); padding-top:12px; margin-top:12px;">
            <h4 style="color:#ffffff; font-size:0.95rem; font-weight:800; margin-bottom:6px;">4. Customer Support & Billing Inquiries</h4>
            <p style="color:var(--muted);">
              • <b>Official Support Email</b>: <a href="mailto:support@truthofmarket.com" style="color:#60a5fa; font-weight:700;">support@truthofmarket.com</a><br/>
              • <b>Merchant of Record</b>: Lemon Squeezy, LLC (<a href="https://app.lemonsqueezy.com/my-orders" target="_blank" rel="noopener noreferrer" style="color:#60a5fa;">Manage Orders & Receipts ↗</a>)<br/>
              • <b>Public Broadcast Desk</b>: <a href="https://t.me/truthofmarketss" target="_blank" rel="noopener noreferrer" style="color:#38bdf8;">t.me/truthofmarketss (@truthofmarketss) ↗</a>
            </p>
          </div>
        </div>
      </div>
    </div>

    <!-- TOAST NOTIFICATION -->
    <div class="toast" id="toastBox">Action completed</div>
  `;
}
