import { renderPricing } from "./Pricing.js";

function polarToCartesian(cx, cy, r, angleDeg) {
  const rad = (angleDeg * Math.PI) / 180.0;
  return {
    x: cx + r * Math.cos(rad),
    y: cy - r * Math.sin(rad),
  };
}

function describeArc(cx, cy, r, startAngleDeg, endAngleDeg) {
  const start = polarToCartesian(cx, cy, r, startAngleDeg);
  const end = polarToCartesian(cx, cy, r, endAngleDeg);
  const largeArcFlag = Math.abs(startAngleDeg - endAngleDeg) <= 180 ? "0" : "1";
  // Since y is inverted for standard math angles (180 left -> 90 top -> 0 right), sweep-flag is 1
  return `M ${start.x.toFixed(2)} ${start.y.toFixed(2)} A ${r} ${r} 0 ${largeArcFlag} 1 ${end.x.toFixed(2)} ${end.y.toFixed(2)}`;
}

export function renderCnnDialSvg(score, regimeLabel) {
  const s = Math.max(0, Math.min(100, Number(score ?? 18.0)));
  const cx = 230;
  const cy = 200;
  const r = 146;

  // 5 CNN segments along 180° (left=0) to 0° (right=100)
  const segments = [
    { code: "EXTREME_FEAR", min: 0, max: 24, a1: 180, a2: 136.5, activeColor: "#d92d20", mutedColor: "#fecaca", label: "EXTREME FEAR", midAngle: 158 },
    { code: "FEAR", min: 25, max: 44, a1: 134, a2: 100.5, activeColor: "#f79009", mutedColor: "#fed7aa", label: "FEAR", midAngle: 117 },
    { code: "NEUTRAL", min: 45, max: 55, a1: 98, a2: 82, activeColor: "#667085", mutedColor: "#e5e7eb", label: "NEUTRAL", midAngle: 90 },
    { code: "GREED", min: 56, max: 74, a1: 79.5, a2: 46, activeColor: "#12b76a", mutedColor: "#bbf7d0", label: "GREED", midAngle: 63 },
    { code: "EXTREME_GREED", min: 75, max: 100, a1: 43.5, a2: 0, activeColor: "#027a48", mutedColor: "#a7f3d0", label: "EXTREME GREED", midAngle: 22 },
  ];

  let activeSeg = segments[0];
  if (s >= 75) activeSeg = segments[4];
  else if (s >= 55.01) activeSeg = segments[3];
  else if (s >= 45) activeSeg = segments[2];
  else if (s >= 25) activeSeg = segments[1];

  const arcsHtml = segments
    .map((seg) => {
      const isAct = seg.code === activeSeg.code;
      const d = describeArc(cx, cy, r, seg.a1, seg.a2);
      const stroke = isAct ? seg.activeColor : seg.mutedColor;
      const width = isAct ? 40 : 32;
      const lp = polarToCartesian(cx, cy, r + 31, seg.midAngle);
      return `
        <path d="${d}" fill="none" stroke="${stroke}" stroke-width="${width}" stroke-linecap="butt" />
        <text x="${lp.x.toFixed(1)}" y="${lp.y.toFixed(1)}" text-anchor="middle" dominant-baseline="middle"
              fill="${isAct ? seg.activeColor : "#6b7280"}"
              font-size="${isAct ? "9.5" : "8.5"}" font-weight="${isAct ? "800" : "700"}" font-family="Inter, sans-serif">
          ${seg.label}
        </text>
      `;
    })
    .join("");

  // Perimeter ticks (0, 25, 45, 55, 75, 100)
  const ticks = [0, 25, 45, 55, 75, 100]
    .map((tVal) => {
      const ang = 180 - (tVal / 100) * 180;
      const pIn = polarToCartesian(cx, cy, r - 24, ang);
      const pTxt = polarToCartesian(cx, cy, r - 35, ang);
      return `
        <circle cx="${pIn.x.toFixed(1)}" cy="${pIn.y.toFixed(1)}" r="1.8" fill="#6b7280" />
        <text x="${pTxt.x.toFixed(1)}" y="${pTxt.y.toFixed(1)}" text-anchor="middle" dominant-baseline="middle"
              fill="#4b5563" font-size="10" font-weight="700" font-family="JetBrains Mono, monospace">
          ${tVal}
        </text>
      `;
    })
    .join("");

  // Needle geometry
  const needleAngle = 180 - (s / 100.0) * 180.0;
  const tip = polarToCartesian(cx, cy, r - 12, needleAngle);
  const baseLeft = polarToCartesian(cx, cy, 8, needleAngle + 90);
  const baseRight = polarToCartesian(cx, cy, 8, needleAngle - 90);

  return `
    <div style="display:flex; flex-direction:column; align-items:center;">
      <svg viewBox="0 0 460 250" style="width:100%; max-width:440px; height:auto; overflow:visible;">
        ${arcsHtml}
        ${ticks}
        <!-- Needle Polygon -->
        <polygon points="${tip.x.toFixed(1)},${tip.y.toFixed(1)} ${baseLeft.x.toFixed(1)},${baseLeft.y.toFixed(1)} ${baseRight.x.toFixed(1)},${baseRight.y.toFixed(1)}"
                 fill="#111827" />
        <circle cx="${cx}" cy="${cy}" r="14" fill="#111827" />
        <circle cx="${cx}" cy="${cy}" r="5" fill="#ffffff" />
      </svg>

      <!-- Score & Active Emotion Callout below Needle Hub -->
      <div style="text-align:center; margin-top:-18px;">
        <div style="display:inline-flex; align-items:baseline; gap:6px; background:#111827; color:#ffffff; padding:6px 20px; border-radius:30px; box-shadow:0 4px 12px rgba(0,0,0,0.12);">
          <span class="mono" style="font-size:2rem; font-weight:900; letter-spacing:-0.03em;">${Math.round(s)}</span>
          <span class="mono" style="font-size:0.9rem; color:#9ca3af; font-weight:600;">(${s.toFixed(1)} / 100)</span>
        </div>
        <div style="margin-top:8px;">
          <span style="font-size:0.78rem; color:#4b5563; font-weight:600; text-transform:uppercase; letter-spacing:0.04em;">
            Market Emotion is driving:
          </span>
          <span class="cnn-pill cnn-pill-${activeSeg.code}" style="margin-left:6px; font-size:0.85rem;">
            ${regimeLabel || activeSeg.label}
          </span>
        </div>
      </div>
    </div>
  `;
}

export function renderTimelineSvg(historyData, activeRange) {
  const pts = (historyData && historyData.series) || [];
  if (!pts.length) {
    return `<div style="padding:40px; text-align:center; color:#6b7280;">Loading historical timeline...</div>`;
  }

  const w = 640;
  const h = 230;
  const padL = 36;
  const padR = 16;
  const padT = 16;
  const padB = 28;
  const plotW = w - padL - padR;
  const plotH = h - padT - padB;

  const coords = pts.map((p, i) => {
    const x = padL + (i / Math.max(1, pts.length - 1)) * plotW;
    const y = padT + (1.0 - Math.max(0, Math.min(100, p.fg_score)) / 100.0) * plotH;
    return `${x.toFixed(1)},${y.toFixed(1)}`;
  });

  const y25 = (padT + 0.75 * plotH).toFixed(1);
  const y50 = (padT + 0.5 * plotH).toFixed(1);
  const y75 = (padT + 0.25 * plotH).toFixed(1);

  const firstDate = pts[0].date;
  const midDate = pts[Math.floor(pts.length / 2)].date;
  const lastDate = pts[pts.length - 1].date;

  return `
    <div>
      <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:10px; flex-wrap:wrap; gap:8px;">
        <div style="font-size:0.8rem; font-weight:700; color:#374151;">
          Historical Semiconductor Fear & Greed Index (${firstDate} → ${lastDate})
        </div>
        <div style="display:flex; gap:4px;">
          ${["3M", "1Y", "3Y", "5Y", "10Y", "ALL"]
            .map(
              (r) => `
            <button class="btn-semi-range" data-range="${r}"
                    style="padding:3px 9px; border-radius:4px; font-size:0.72rem; font-weight:700; cursor:pointer; border:1px solid ${
                      activeRange === r ? "#111827" : "#d1d5db"
                    }; background:${activeRange === r ? "#111827" : "#ffffff"}; color:${
                activeRange === r ? "#ffffff" : "#374151"
              };">
              ${r}
            </button>
          `
            )
            .join("")}
        </div>
      </div>

      <svg viewBox="0 0 ${w} ${h}" style="width:100%; height:auto; background:#f9fafb; border:1px solid #e5e7eb; border-radius:4px;">
        <!-- Extreme Greed Band (>75) -->
        <rect x="${padL}" y="${padT}" width="${plotW}" height="${0.25 * plotH}" fill="rgba(16,185,129,0.08)" />
        <!-- Extreme Fear Band (<25) -->
        <rect x="${padL}" y="${y25}" width="${plotW}" height="${0.25 * plotH}" fill="rgba(239,68,68,0.09)" />

        <!-- Reference Lines -->
        <line x1="${padL}" y1="${y75}" x2="${w - padR}" y2="${y75}" stroke="#10b981" stroke-dasharray="3,3" stroke-width="1" />
        <line x1="${padL}" y1="${y50}" x2="${w - padR}" y2="${y50}" stroke="#9ca3af" stroke-dasharray="3,3" stroke-width="1" />
        <line x1="${padL}" y1="${y25}" x2="${w - padR}" y2="${y25}" stroke="#ef4444" stroke-dasharray="3,3" stroke-width="1" />

        <text x="6" y="${y75}" fill="#047857" font-size="9.5" font-weight="700" dominant-baseline="middle">75</text>
        <text x="6" y="${y50}" fill="#6b7280" font-size="9.5" font-weight="700" dominant-baseline="middle">50</text>
        <text x="6" y="${y25}" fill="#b91c1c" font-size="9.5" font-weight="700" dominant-baseline="middle">25</text>

        <!-- FG Line -->
        <polyline fill="none" stroke="#111827" stroke-width="1.8" points="${coords.join(" ")}" />

        <!-- X-Axis Dates -->
        <text x="${padL}" y="${h - 8}" fill="#6b7280" font-size="9.5" font-family="JetBrains Mono, monospace">${firstDate}</text>
        <text x="${padL + plotW / 2}" y="${h - 8}" fill="#6b7280" font-size="9.5" text-anchor="middle" font-family="JetBrains Mono, monospace">${midDate}</text>
        <text x="${w - padR}" y="${h - 8}" fill="#6b7280" font-size="9.5" text-anchor="end" font-family="JetBrains Mono, monospace">${lastDate}</text>
      </svg>
    </div>
  `;
}

function renderMiniSparkline(values, regimeCode) {
  if (!values || !values.length) return "";
  const w = 180;
  const h = 44;
  const coords = values
    .map((v, i) => {
      const x = 4 + (i / Math.max(1, values.length - 1)) * (w - 8);
      const y = 4 + (1.0 - Math.max(0, Math.min(100, v)) / 100.0) * (h - 8);
      return `${x.toFixed(1)},${y.toFixed(1)}`;
    })
    .join(" ");

  const colorMap = {
    EXTREME_FEAR: "#dc2626",
    FEAR: "#ea580c",
    NEUTRAL: "#4b5563",
    GREED: "#16a34a",
    EXTREME_GREED: "#059669",
  };
  const stroke = colorMap[regimeCode] || "#111827";

  return `
    <svg viewBox="0 0 ${w} ${h}" style="width:160px; height:40px; background:#f8fafc; border:1px solid #e2e8f0; border-radius:4px;">
      <line x1="0" y1="${h / 2}" x2="${w}" y2="${h / 2}" stroke="#e2e8f0" stroke-dasharray="2,2" stroke-width="1" />
      <polyline fill="none" stroke="${stroke}" stroke-width="1.8" points="${coords}" />
    </svg>
  `;
}

function renderEquityCurveSvg(historyData) {
  const pts = (historyData && historyData.series) || [];
  if (!pts.length) return "";

  const w = 720;
  const h = 220;
  const padL = 52;
  const padR = 20;
  const padT = 18;
  const padB = 26;
  const plotW = w - padL - padR;
  const plotH = h - padT - padB;

  const allVals = [];
  pts.forEach((p) => {
    allVals.push(p.port73_norm, p.qqq_norm);
  });
  const minV = Math.min(...allVals, 8000);
  const maxV = Math.max(...allVals, 12000);
  const span = Math.max(1, maxV - minV);

  const portCoords = pts
    .map((p, i) => {
      const x = padL + (i / Math.max(1, pts.length - 1)) * plotW;
      const y = padT + (1.0 - (p.port73_norm - minV) / span) * plotH;
      return `${x.toFixed(1)},${y.toFixed(1)}`;
    })
    .join(" ");

  const qqqCoords = pts
    .map((p, i) => {
      const x = padL + (i / Math.max(1, pts.length - 1)) * plotW;
      const y = padT + (1.0 - (p.qqq_norm - minV) / span) * plotH;
      return `${x.toFixed(1)},${y.toFixed(1)}`;
    })
    .join(" ");

  const lastPort = pts[pts.length - 1].port73_norm;
  const lastQqq = pts[pts.length - 1].qqq_norm;

  return `
    <div style="margin-bottom:16px;">
      <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:8px; flex-wrap:wrap; gap:8px; font-size:0.78rem;">
        <div style="display:flex; gap:16px; align-items:center;">
          <span style="display:inline-flex; align-items:center; gap:6px; color:#34d399; font-weight:700;">
            <span style="width:12px; height:3px; background:#0ecb81; display:inline-block;"></span>
            70% $SMH : 30% $XLV Barbell ($10k → $${lastPort.toLocaleString()})
          </span>
          <span style="display:inline-flex; align-items:center; gap:6px; color:#94a3b8; font-weight:600;">
            <span style="width:12px; height:3px; background:#64748b; display:inline-block;"></span>
            100% $QQQ Benchmark ($10k → $${lastQqq.toLocaleString()})
          </span>
        </div>
        <span class="mono" style="color:var(--muted); font-size:0.72rem;">Selected Window: ${historyData.range_code}</span>
      </div>
      <svg viewBox="0 0 ${w} ${h}" style="width:100%; height:auto; background:#060911; border:1px solid var(--border); border-radius:4px;">
        <polyline fill="none" stroke="#64748b" stroke-width="1.6" stroke-dasharray="3,2" points="${qqqCoords}" />
        <polyline fill="none" stroke="#0ecb81" stroke-width="2.2" points="${portCoords}" />
        <text x="6" y="${padT + 8}" fill="#94a3b8" font-size="9.5" font-family="JetBrains Mono, monospace">$${Math.round(maxV).toLocaleString()}</text>
        <text x="6" y="${h - padB}" fill="#94a3b8" font-size="9.5" font-family="JetBrains Mono, monospace">$${Math.round(minV).toLocaleString()}</text>
      </svg>
    </div>
  `;
}

export function renderSemiFearGreedView(state) {
  const t = state.t;
  const lang = state.lang;
  const ov = state.semiOverview;

  if (!ov) {
    return `
      <div class="proof-card" style="padding:40px; text-align:center;">
        Loading Semiconductor Fear & Greed Index...
      </div>
    `;
  }

  const regimeLabel = lang === "jp" ? ov.regime_jp : lang === "kr" ? ov.regime_kr : ov.regime_en;
  const actionHeadline = lang === "jp" ? ov.action_headline_jp : lang === "kr" ? ov.action_headline_kr : ov.action_headline_en;
  const actionDetail = lang === "jp" ? ov.action_detail_jp : lang === "kr" ? ov.action_detail_kr : ov.action_detail_en;
  const gaugeTab = state.semiGaugeTab || "overview";
  const activeRange = state.semiRange || "1Y";
  const rebal = state.semiRebalanceResult;
  const lump = state.semiLumpSumResult;
  const eras = (state.semiHistory && state.semiHistory.era_summary) || [];

  return `
    <!-- SECTION 1: AUTHENTIC CNN BUSINESS FEAR & GREED INDEX EDITORIAL SURFACE -->
    <section class="cnn-page-wrapper" id="semiCnnSection">
      <div class="cnn-editorial-header">
        <div>
          <div class="cnn-red-tag">${t.cnnBadge}</div>
          <h1 class="cnn-main-title">${t.cnnTitle}</h1>
          <p class="cnn-main-subtitle">${t.cnnSubtitle}</p>
        </div>
        <div style="display:flex; gap:8px; align-items:center; flex-wrap:wrap;">
          <a
            class="btn"
            href="${state.config?.youtube_url || "https://youtube.com/@rightsidealpha"}"
            target="_blank"
            rel="noopener noreferrer"
            style="background:#dc2626; color:#ffffff; border-color:#b91c1c;"
          >
            📺 YouTube (@rightsidealpha) ↗
          </a>
          <a
            class="btn"
            href="${state.config?.instagram_url || "https://www.instagram.com/semifeargreed"}"
            target="_blank"
            rel="noopener noreferrer"
            style="background:#db2777; color:#ffffff; border-color:#be185d;"
          >
            📸 Instagram (@semifeargreed) ↗
          </a>
          <a
            class="btn ${state.isProUnlocked ? "" : "btn-gated-vip-tg"}"
            href="${state.isProUnlocked ? (state.config?.telegram_vip_channel_url || "https://t.me/+a6Sl2yLirbwyODQ1") : "#pro-vip-telegram"}"
            ${state.isProUnlocked ? 'target="_blank" rel="noopener noreferrer"' : ""}
            style="background:#0284c7; color:#ffffff; border-color:#0369a1;"
          >
            ${state.isProUnlocked ? "👑 VIP Telegram News ↗" : "🔒 VIP Telegram ($SMH/$XLV News)"}
          </a>
          <button class="btn" id="btnExportSemiGauge" style="background:#111827; color:#ffffff; border-color:#111827;">
            ${t.cnnExportGauge}
          </button>
        </div>
      </div>

      <!-- CNN TOP 2-COLUMN GRID: LEFT = DIAL GAUGE / TIMELINE, RIGHT = 4 HISTORICAL COMPARISONS -->
      <div class="cnn-top-grid">
        <div class="cnn-card">
          <div class="cnn-card-header">
            <div style="font-size:0.78rem; color:#6b7280; font-weight:600;">
              ${t.cnnLastUpdated}: <b class="mono" style="color:#111827;">${ov.date}</b> · $SMH <b class="mono">$${ov.smh_close.toFixed(2)}</b> (${ov.smh_dd_pct.toFixed(2)}% off 52W High)
            </div>
            <div class="cnn-view-tabs">
              <button class="cnn-view-tab ${gaugeTab === "overview" ? "active" : ""}" data-semi-tab="overview">
                ${t.cnnTabOverview}
              </button>
              <button class="cnn-view-tab ${gaugeTab === "timeline" ? "active" : ""}" data-semi-tab="timeline">
                ${t.cnnTabTimeline}
              </button>
            </div>
          </div>

          ${
            gaugeTab === "overview"
              ? renderCnnDialSvg(ov.fg_score, regimeLabel)
              : renderTimelineSvg(state.semiHistory, activeRange)
          }
        </div>

        <!-- RIGHT COLUMN: CNN 4-ROW HISTORICAL STACK + BARBELL SIGNAL -->
        <div class="cnn-card" style="display:flex; flex-direction:column; justify-content:space-between;">
          <div>
            <div style="font-size:0.78rem; font-weight:800; text-transform:uppercase; letter-spacing:0.05em; color:#6b7280; margin-bottom:8px;">
              ${t.cnnHistoryTitle}
            </div>
            <div class="cnn-history-list">
              ${ov.comparisons
                .map((c) => {
                  const lbl = lang === "jp" ? c.label_jp : lang === "kr" ? c.label_kr : c.label_en;
                  const reg = lang === "jp" ? c.regime_jp : lang === "kr" ? c.regime_kr : c.regime_en;
                  return `
                  <div class="cnn-history-row">
                    <div>
                      <div class="cnn-hist-label">${lbl} <span class="mono" style="font-size:0.72rem; color:#9ca3af;">(${c.date})</span></div>
                      <div class="cnn-hist-regime">${reg}</div>
                    </div>
                    <div class="cnn-score-circle">${Math.round(c.score)}</div>
                  </div>
                `;
                })
                .join("")}
            </div>
          </div>

          <!-- Active SMH:XLV Barbell Regime Box -->
          <div style="margin-top:16px; padding:14px 16px; background:#fef2f2; border:1px solid #fecaca; border-left:4px solid #dc2626; border-radius:4px;">
            <div style="font-size:0.68rem; font-weight:800; color:#991b1b; letter-spacing:0.05em; text-transform:uppercase;">
              ${t.cnnActiveRuleLabel} · TARGET ${ov.recommended_smh_weight}% $SMH : ${ov.recommended_xlv_weight}% $XLV
            </div>
            <div style="font-size:0.88rem; font-weight:800; color:#111827; margin-top:4px;">
              ${actionHeadline}
            </div>
            <p style="font-size:0.78rem; color:#374151; margin-top:4px; line-height:1.45;">
              ${actionDetail}
            </p>
          </div>
        </div>
      </div>

      <!-- CNN 7 FEAR & GREED INDICATORS BREAKDOWN -->
      <div style="margin-top:12px;">
        <div style="border-bottom:2px solid #111827; padding-bottom:10px; margin-bottom:16px;">
          <h2 style="font-size:1.35rem; font-weight:900; color:#111827;">${t.cnnIndicatorsHeading}</h2>
          <p style="font-size:0.84rem; color:#4b5563; margin-top:2px;">${t.cnnIndicatorsSub}</p>
        </div>

        <div class="cnn-indicators-list">
          ${ov.factors
            .map((f) => {
              const title = lang === "jp" ? f.title_jp : lang === "kr" ? f.title_kr : f.title_en;
              const sub = lang === "jp" ? f.subtitle_jp : lang === "kr" ? f.subtitle_kr : f.subtitle_en;
              const desc = lang === "jp" ? f.desc_jp : lang === "kr" ? f.desc_kr : f.desc_en;
              const reg = lang === "jp" ? f.regime_jp : lang === "kr" ? f.regime_kr : f.regime_en;

              return `
              <div class="cnn-indicator-item">
                <div>
                  <div style="display:flex; align-items:center; gap:8px;">
                    <span class="mono" style="font-size:0.7rem; font-weight:800; padding:2px 6px; background:#f3f4f6; border:1px solid #d1d5db; border-radius:3px; color:#374151;">
                      #${f.order} · ${f.weight_pct}% WEIGHT
                    </span>
                    <span class="cnn-ind-title">${title}</span>
                  </div>
                  <div class="cnn-ind-sub">${sub}</div>
                  <p class="cnn-ind-desc">${desc}</p>
                </div>

                <div style="display:flex; flex-direction:column; align-items:center; gap:6px;">
                  ${renderMiniSparkline(f.sparkline, f.regime_code)}
                  <div class="mono" style="font-size:0.74rem; color:#374151; font-weight:700;">
                    Reading: ${f.raw_display} · Score ${f.score.toFixed(1)}/100
                  </div>
                </div>

                <div style="text-align:right;">
                  <span class="cnn-pill cnn-pill-${f.regime_code}">${reg}</span>
                </div>
              </div>
            `;
            })
            .join("")}
        </div>
      </div>
    </section>

    <!-- SECTION 2: CORE ETF SNAPSHOT STRIP ($SMH, $XLV, $QQQ) -->
    <section style="display:grid; grid-template-columns:repeat(auto-fit, minmax(310px, 1fr)); gap:14px; margin-bottom:22px;">
      ${ov.etfs
        .map((etf) => {
          const name = lang === "jp" ? etf.name_jp : lang === "kr" ? etf.name_kr : etf.name_en;
          const role = lang === "jp" ? etf.role_jp : lang === "kr" ? etf.role_kr : etf.role_en;
          const cfg = state.config || {};
          const tvAffId = encodeURIComponent(cfg.tradingview_aff_id || "1173809");
          const saSource = encodeURIComponent(cfg.seekingalpha_source || "better_life333");
          const rawBrk = cfg.broker_referral_url || "https://www.bitget.com/referral/register?clacCode=7nja";
          const brkSep = rawBrk.includes("?") ? "&" : "?";
          const tvUrl = `https://www.tradingview.com/symbols/${encodeURIComponent(etf.ticker)}/?aff_id=${tvAffId}`;
          const saUrl = `https://seekingalpha.com/symbol/${encodeURIComponent(etf.ticker)}/earnings?source=${saSource}`;
          const brokerUrl = `${rawBrk}${brkSep}symbol=${encodeURIComponent(etf.ticker)}`;
          return `
          <div class="proof-card" style="margin-bottom:0; border-top:2px solid ${
            etf.ticker === "SMH" ? "var(--fin-blue)" : etf.ticker === "XLV" ? "var(--fin-up)" : "#64748b"
          };">
            <div style="display:flex; justify-content:space-between; align-items:flex-start;">
              <div>
                <div style="display:flex; align-items:center; gap:8px;">
                  <span class="mono" style="font-size:1.15rem; font-weight:900; color:#ffffff;">$${etf.ticker}</span>
                  <span style="font-size:0.78rem; color:var(--text-secondary); font-weight:600;">${name}</span>
                </div>
                <div style="font-size:0.74rem; color:var(--muted); margin-top:3px;">${role}</div>
              </div>
              <div style="text-align:right;">
                <div class="mono" style="font-size:1.15rem; font-weight:800; color:#ffffff;">$${Number(etf.close ?? 0).toFixed(2)}</div>
                <div class="mono" style="font-size:0.74rem; color:${etf.ret_1d_pct >= 0 ? "var(--fin-up)" : "var(--fin-down)"};">
                  1D: ${etf.ret_1d_pct >= 0 ? "+" : ""}${Number(etf.ret_1d_pct ?? 0).toFixed(2)}% · 20D: ${etf.ret_20d_pct >= 0 ? "+" : ""}${Number(etf.ret_20d_pct ?? 0).toFixed(2)}%
                </div>
                <div class="mono" style="font-size:0.7rem; color:var(--muted); margin-top:1px;">
                  52W DD: ${Number(etf.dd_52w_pct ?? 0).toFixed(2)}% · RSI(14): ${Number(etf.rsi14 ?? 50).toFixed(1)}
                </div>
              </div>
            </div>
            <div style="display:flex; justify-content:space-between; align-items:center; margin-top:12px; padding-top:10px; border-top:1px solid var(--border-subtle); font-size:0.74rem;">
              <span class="mono" style="color:var(--muted);">
                Normal: <b style="color:#fff;">${etf.target_weight_normal}%</b> → Extreme Fear: <b style="color:var(--fin-up);">${etf.target_weight_fear}%</b>
              </span>
              <div style="display:flex; gap:6px;">
                <a class="btn btn-sm" href="${tvUrl}" target="_blank" rel="noopener noreferrer">TV Chart ↗</a>
                <a class="btn btn-sm" href="${saUrl}" target="_blank" rel="noopener noreferrer">Holdings ↗</a>
                <a class="btn btn-sm" href="${brokerUrl}" target="_blank" rel="noopener noreferrer" style="border-color:rgba(16,185,129,0.4); color:#34d399;">Trade ↗</a>
              </div>
            </div>
          </div>
        `;
        })
        .join("")}
    </section>

    <!-- SECTION 3: INTERACTIVE SMH + XLV REBALANCING & 2.5M KRW TAX HARVESTING ENGINE + 3-STAGE LUMP-SUM PLANNER -->
    <section class="semi-calc-grid">
      <!-- Calculator 1: SMH + XLV Rebalancing & Tax Optimizer -->
      <div class="proof-card" style="margin-bottom:0; border-top:2px solid var(--fin-up);">
        <div style="font-size:0.7rem; font-family:var(--font-mono); font-weight:700; color:var(--fin-up); letter-spacing:0.05em;">
          ${t.rebalSectionTag}
        </div>
        <h3 style="font-size:1.12rem; font-weight:800; color:#ffffff; margin:4px 0 6px;">${t.rebalSectionTitle}</h3>
        <p style="font-size:0.8rem; color:var(--muted); margin-bottom:14px;">${t.rebalSectionDesc}</p>

        <div class="semi-form-grid-2" style="margin-bottom:12px;">
          <div>
            <label style="font-size:0.68rem; font-family:var(--font-mono); color:var(--muted);">PORTFOLIO CAPITAL ($ USD)</label>
            <input type="number" id="semiCapInput" value="${state.semiCapUsd ?? 100000}" step="1000"
                   style="width:100%; padding:8px 10px; background:#060911; border:1px solid var(--border); color:#fff; border-radius:4px; font-family:var(--font-mono); font-weight:700; margin-top:3px;" />
          </div>
          <div>
            <label style="font-size:0.68rem; font-family:var(--font-mono); color:var(--muted);">ALLOCATION MODE</label>
            <select id="semiModeInput" style="width:100%; padding:8px 10px; background:#060911; border:1px solid var(--border); color:#fff; border-radius:4px; font-family:var(--font-sans); font-weight:600; margin-top:3px;">
              <option value="AUTO_REGIME" ${state.semiMode === "AUTO_REGIME" ? "selected" : ""}>Auto Regime (70:30 ↔ 80:20 on Fear ≤ 25)</option>
              <option value="BASELINE_70_30" ${state.semiMode === "BASELINE_70_30" ? "selected" : ""}>70% $SMH : 30% $XLV Golden Baseline</option>
              <option value="CONTRARIAN_80_20" ${state.semiMode === "CONTRARIAN_80_20" ? "selected" : ""}>80% $SMH : 20% $XLV Contrarian Accumulation</option>
              <option value="AGGRESSIVE_90_10" ${state.semiMode === "AGGRESSIVE_90_10" ? "selected" : ""}>90% $SMH : 10% $XLV Right-Side Tilt</option>
            </select>
          </div>
          <div>
            <label style="font-size:0.68rem; font-family:var(--font-mono); color:var(--muted);">REBALANCING CADENCE</label>
            <select id="semiFreqInput" style="width:100%; padding:8px 10px; background:#060911; border:1px solid var(--border); color:#fff; border-radius:4px; font-family:var(--font-sans); font-weight:600; margin-top:3px;">
              <option value="ANNUAL" ${state.semiFreq === "ANNUAL" ? "selected" : ""}>Annual + Band Trigger (Min Tax Drag)</option>
              <option value="QUARTERLY" ${state.semiFreq === "QUARTERLY" ? "selected" : ""}>Quarterly Rebalance</option>
              <option value="MONTHLY" ${state.semiFreq === "MONTHLY" ? "selected" : ""}>Monthly Rebalance</option>
              <option value="WEEKLY" ${state.semiFreq === "WEEKLY" ? "selected" : ""}>Weekly Rebalance (High Tax Drag)</option>
            </select>
          </div>
          ${
            lang === "kr"
              ? `<div>
            <label style="font-size:0.68rem; font-family:var(--font-mono); color:var(--muted);">UNREALIZED GAIN (₩ KRW · TAX HARVESTER)</label>
            <input type="number" id="semiGainKrwInput" value="${state.semiGainKrw ?? 3800000}" step="100000"
                   style="width:100%; padding:8px 10px; background:#060911; border:1px solid var(--border); color:#fff; border-radius:4px; font-family:var(--font-mono); margin-top:3px;" />
          </div>`
              : ""
          }
        </div>

        <button class="btn btn-emerald" id="btnRunSemiRebalance" style="width:100%; justify-content:center; padding:9px;">
          Calculate Exact $SMH / $XLV Rebalancing Orders
        </button>

        ${
          rebal
            ? `
          <div id="semiRebalOutput" style="margin-top:14px; background:#060911; border:1px solid var(--border); border-left:3px solid var(--fin-up); border-radius:4px; padding:14px; font-size:0.8rem;">
            <div style="font-weight:800; color:var(--fin-up); margin-bottom:4px;">
              ${lang === "jp" ? rebal.active_rule_jp : lang === "kr" ? rebal.active_rule_kr : rebal.active_rule_en}
            </div>
            <div class="mono" style="font-size:0.71rem; color:#93c5fd; margin-bottom:8px;">
              Latest Close Basis (${rebal.as_of_date || ov.date}): $SMH @ $${Number(rebal.smh_close ?? ov.smh_close).toFixed(2)} · $XLV @ $${Number(rebal.xlv_close ?? ov.xlv_close).toFixed(2)}${
                lang === "kr"
                  ? ` · FX ₩${Number(rebal.usdkrw ?? ov.usdkrw).toLocaleString()}/$ · Total ₩${Number(rebal.total_capital_krw ?? 0).toLocaleString()}`
                  : ` · Total Capital $${Number(rebal.total_capital_usd ?? state.semiCapUsd ?? 100000).toLocaleString()}`
              }
            </div>
            <div class="semi-form-grid-2" style="margin-bottom:10px;">
              <div style="background:#0c1220; padding:10px; border-radius:4px; border:1px solid var(--border);">
                <div style="font-size:0.7rem; color:var(--muted);">TARGET $SMH (${rebal.target_smh_weight_pct}%)</div>
                <div class="mono" style="font-size:1.05rem; font-weight:800; color:#fff; margin-top:2px;">
                  $${Number(rebal.target_smh_usd ?? 0).toLocaleString()} (${rebal.target_smh_shares} sh)
                </div>
                <div class="mono" style="font-size:0.73rem; color:${rebal.delta_smh_usd >= 0 ? "var(--fin-up)" : "var(--fin-down)"}; margin-top:2px;">
                  Order vs Drift: ${rebal.delta_smh_usd >= 0 ? "BUY +" : "SELL "}$${Math.abs(Number(rebal.delta_smh_usd ?? 0)).toLocaleString()} (${rebal.delta_smh_shares >= 0 ? "+" : ""}${rebal.delta_smh_shares} sh)
                </div>
              </div>
              <div style="background:#0c1220; padding:10px; border-radius:4px; border:1px solid var(--border);">
                <div style="font-size:0.7rem; color:var(--muted);">TARGET $XLV (${rebal.target_xlv_weight_pct}%)</div>
                <div class="mono" style="font-size:1.05rem; font-weight:800; color:#fff; margin-top:2px;">
                  $${Number(rebal.target_xlv_usd ?? 0).toLocaleString()} (${rebal.target_xlv_shares} sh)
                </div>
                <div class="mono" style="font-size:0.73rem; color:${rebal.delta_xlv_usd >= 0 ? "var(--fin-up)" : "var(--fin-down)"}; margin-top:2px;">
                  Order vs Drift: ${rebal.delta_xlv_usd >= 0 ? "BUY +" : "SELL "}$${Math.abs(Number(rebal.delta_xlv_usd ?? 0)).toLocaleString()} (${rebal.delta_xlv_shares >= 0 ? "+" : ""}${rebal.delta_xlv_shares} sh)
                </div>
              </div>
            </div>
            <div style="font-size:0.75rem; color:var(--text-secondary); line-height:1.45; border-top:1px solid var(--border); padding-top:8px;">
              ${
                lang === "kr"
                  ? `<div style="margin-bottom:4px;"><b>KRW 2.5M Tax-Free Harvester:</b> ${rebal.kr_tax_guidance_kr}</div>`
                  : ""
              }
              <div class="mono" style="color:var(--muted);">
                Residual Cash: $${Number(rebal.residual_cash_usd ?? 0).toFixed(2)} · Est. Annual Tax & Turnover Drag (${rebal.rebalance_frequency}): -${rebal.estimated_tax_drag_pct}%/yr · Expected Net 15Y Rate: +${rebal.expected_net_cagr_pct}%/yr
              </div>
            </div>
          </div>
        `
            : ""
        }
      </div>

      <!-- Calculator 2: 3-Stage Lump-Sum Entry Planner -->
      <div class="proof-card" style="margin-bottom:0; border-top:2px solid var(--fin-blue);">
        <div style="font-size:0.7rem; font-family:var(--font-mono); font-weight:700; color:#60a5fa; letter-spacing:0.05em;">
          ${t.lumpSectionTag}
        </div>
        <h3 style="font-size:1.12rem; font-weight:800; color:#ffffff; margin:4px 0 6px;">${t.lumpSectionTitle}</h3>
        <p style="font-size:0.8rem; color:var(--muted); margin-bottom:14px;">${t.lumpSectionDesc}</p>

        <div class="semi-form-grid-2" style="margin-bottom:12px;">
          <div>
            <label style="font-size:0.68rem; font-family:var(--font-mono); color:var(--muted);">NEW LUMP-SUM CASH ($ USD)</label>
            <input type="number" id="semiLumpCapInput" value="${state.semiLumpCapUsd ?? 50000}" step="1000"
                   style="width:100%; padding:8px 10px; background:#060911; border:1px solid var(--border); color:#fff; border-radius:4px; font-family:var(--font-mono); font-weight:700; margin-top:3px;" />
          </div>
          <div>
            <label style="font-size:0.68rem; font-family:var(--font-mono); color:var(--muted);">
              SIMULATE FEAR & GREED SCORE (LIVE: ${ov.fg_score})
            </label>
            <input type="number" id="semiLumpScoreInput" value="${
              state.semiLumpScore !== null && state.semiLumpScore !== undefined ? state.semiLumpScore : ov.fg_score
            }" min="0" max="100" step="1"
                   style="width:100%; padding:8px 10px; background:#060911; border:1px solid var(--border); color:#fff; border-radius:4px; font-family:var(--font-mono); font-weight:700; margin-top:3px;" />
          </div>
        </div>

        <div style="display:flex; gap:6px; margin-bottom:12px; flex-wrap:wrap;">
          <button class="btn btn-sm btn-sim-fg" data-fg="18.0">Live Extreme Fear (18.0)</button>
          <button class="btn btn-sm btn-sim-fg" data-fg="50.0">Simulate Neutral (50.0)</button>
          <button class="btn btn-sm btn-sim-fg" data-fg="78.0">Simulate Extreme Greed (78.0)</button>
        </div>

        <button class="btn btn-primary" id="btnRunSemiLumpSum" style="width:100%; justify-content:center; padding:9px;">
          Generate 3-Stage Lump-Sum Tranche Schedule
        </button>

        ${
          lump
            ? `
          <div id="semiLumpOutput" style="margin-top:14px; background:#060911; border:1px solid var(--border); border-left:3px solid var(--fin-blue); border-radius:4px; padding:14px; font-size:0.8rem;">
            <div style="font-weight:800; color:#93c5fd; margin-bottom:3px;">
              ${lang === "jp" ? lump.case_title_jp : lang === "kr" ? lump.case_title_kr : lump.case_title_en}
            </div>
            <div class="mono" style="font-size:0.71rem; color:var(--muted); margin-bottom:6px;">
              Latest Close Basis (${lump.as_of_date || ov.date}): $SMH @ $${Number(lump.smh_close ?? ov.smh_close).toFixed(2)} · $XLV @ $${Number(lump.xlv_close ?? ov.xlv_close).toFixed(2)}
            </div>
            <p style="font-size:0.76rem; color:var(--text-secondary); margin-bottom:10px;">
              ${lang === "jp" ? lump.summary_jp : lang === "kr" ? lump.summary_kr : lump.summary_en}
            </p>
            <div style="display:flex; flex-direction:column; gap:8px;">
              ${lump.tranches
                .map((tr) => {
                  const tTitle = lang === "jp" ? tr.title_jp : lang === "kr" ? tr.title_kr : tr.title_en;
                  const tTime = lang === "jp" ? tr.timing_jp : lang === "kr" ? tr.timing_kr : tr.timing_en;
                  const tNote = lang === "jp" ? tr.note_jp : lang === "kr" ? tr.note_kr : tr.note_en;
                  return `
                  <div style="background:#0c1220; padding:10px; border-radius:4px; border:1px solid var(--border);">
                    <div style="display:flex; justify-content:space-between; align-items:center;">
                      <b style="color:#ffffff;">${tTitle}</b>
                      <span class="mono" style="color:var(--fin-up); font-weight:700;">$${tr.amount_usd.toLocaleString()} (${tr.allocation_pct}%)</span>
                    </div>
                    <div class="mono" style="font-size:0.72rem; color:#93c5fd; margin-top:2px;">
                      ${tTime} · $SMH: $${tr.smh_usd.toLocaleString()} (${tr.smh_shares} sh) | $XLV: $${tr.xlv_usd.toLocaleString()} (${tr.xlv_shares} sh)
                    </div>
                    <div style="font-size:0.74rem; color:var(--muted); margin-top:4px;">${tNote}</div>
                  </div>
                `;
                })
                .join("")}
            </div>
          </div>
        `
            : ""
        }
      </div>
    </section>

    <!-- SECTION 4: 26-YEAR EMPIRICAL PERFORMANCE TABLE & EQUITY CURVE (2000-2026) -->
    <section class="proof-card">
      <div style="display:flex; justify-content:space-between; align-items:flex-start; flex-wrap:wrap; gap:12px; margin-bottom:14px;">
        <div>
          <div style="font-size:0.7rem; font-family:var(--font-mono); font-weight:700; color:var(--fin-up); letter-spacing:0.05em;">
            ${t.eraSectionTag}
          </div>
          <h3 style="font-size:1.15rem; font-weight:800; color:#ffffff; margin-top:3px;">${t.eraSectionTitle}</h3>
          <p style="font-size:0.8rem; color:var(--muted); margin-top:2px;">${t.eraSectionDesc}</p>
        </div>
        <button class="btn btn-sm" id="btnDownloadSemiCsv">
          Download 2000–2026 Daily CSV Dataset (Pro)
        </button>
      </div>

      ${renderEquityCurveSvg(state.semiHistory)}

      <div class="table-responsive-scroll">
        <table class="proof-table">
          <thead>
            <tr>
              <th>Investment Horizon</th>
              <th>Period</th>
              <th>100% $QQQ CAGR</th>
              <th>100% $QQQ Multiple</th>
              <th>70:30 Baseline CAGR</th>
              <th>70:30 (80:20 Fear Tilt) CAGR</th>
              <th>70:30 (80:20 Tilt) Multiple</th>
              <th>Max Drawdown (vs QQQ)</th>
            </tr>
          </thead>
          <tbody>
            ${eras
              .map((e) => {
                const hLabel = lang === "jp" ? e.horizon_jp : lang === "kr" ? e.horizon_kr : e.horizon_en;
                return `
                <tr class="proof-highlight">
                  <td style="font-family:var(--font-sans);">${hLabel}</td>
                  <td>${e.period}</td>
                  <td style="color:var(--text-secondary);">+${e.qqq_cagr_pct.toFixed(2)}%</td>
                  <td style="color:var(--text-secondary);">${e.qqq_multiple.toFixed(2)}x</td>
                  <td>+${e.port_70_30_cagr_pct.toFixed(2)}%</td>
                  <td style="color:var(--fin-up); font-weight:800;">+${e.port_80_20_cagr_pct.toFixed(2)}%</td>
                  <td style="color:var(--fin-up); font-weight:800;">${e.port_80_20_multiple.toFixed(2)}x</td>
                  <td><span style="color:var(--fin-up);">${e.port_80_20_mdd_pct.toFixed(1)}%</span> <span style="color:var(--muted); font-size:0.72rem;">(QQQ ${e.qqq_mdd_pct.toFixed(1)}%)</span></td>
                </tr>
              `;
              })
              .join("")}
          </tbody>
        </table>
      </div>
    </section>

    <!-- SECTION 5: PRO TERMINAL & LIFETIME LICENSE PRICING -->
    ${renderPricing(state)}

    <!-- CROSS-PLATFORM SWITCH BANNER BACK TO RIGHTSIDEALPHA -->
    <section class="cross-banner" style="border-left-color:var(--fin-blue);">
      <div>
        <div style="font-size:0.72rem; font-family:var(--font-mono); font-weight:700; color:#93c5fd; text-transform:uppercase;">
          COMPANION US INDIVIDUAL EQUITY SCREENER · RIGHTSIDEALPHA
        </div>
        <h3 style="font-size:1.15rem; font-weight:800; margin:4px 0; color:#ffffff;">
          Looking for High-Alpha US Individual Stock Turnarounds ($CELH, $MBLY, $NVDA, $APP)?
        </h3>
        <p style="font-size:0.84rem; color:var(--muted);">
          Switch to the RightSideAlpha US Equity Terminal to screen 72 NYSE & NASDAQ stocks for MA20/MA60 Right-Side Ignitions and 55-Day Time-Stop diagnostics.
        </p>
      </div>
      <button class="btn btn-primary" id="btnSwitchToRightSide">
        Open RightSideAlpha US Equity Terminal →
      </button>
    </section>
  `;
}
