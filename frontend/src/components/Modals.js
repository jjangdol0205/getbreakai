export function renderModals(state) {
  const cfg = state.config;

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
        <input type="text" id="licenseInput" placeholder="PRO-DEMO-2026 or XXXX-XXXX-XXXX" autocomplete="off" />
        <div id="licenseMsg" style="font-size:0.8rem; margin-bottom:12px; min-height:1.2em;"></div>
        <div style="display:flex; gap:8px; justify-content:flex-end;">
          <button class="btn" id="btnCancelLicense">Cancel</button>
          <button class="btn btn-primary" id="btnVerifyLicense">Verify & Unlock Terminal</button>
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
          Update Lemon Squeezy checkout endpoints and affiliate attribution identifiers. Changes persist to the backend and browser storage.
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
          <button class="btn" id="btnCancelConfig">Close</button>
          <button class="btn btn-primary" id="btnSaveConfig">Save Configuration</button>
        </div>
      </div>
    </div>

    <!-- INSTITUTIONAL RESEARCH BRIEF MODAL -->
    <div class="modal-backdrop" id="researchModal">
      <div class="modal" style="max-width:760px;">
        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:12px;">
          <h3 style="font-size:1.1rem; font-weight:800; color:#ffffff;" id="researchModalTitle">SEC Primary Filing Turnaround Brief</h3>
          <button class="btn btn-sm" id="btnCloseResearch">Close ✕</button>
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
