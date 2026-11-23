/* SMH Fear & Greed Index — Calm Light Editorial Renderer (Strict CSP, Zero Inline Scripts) */
(function initSmhFearGreedPage() {
  'use strict';

  var root = document.getElementById('smhFgApp');
  if (!root) return;
  var lang = (root.getAttribute('data-lang') || 'en').toLowerCase() === 'ja' ? 'ja' : 'en';
  var divCode = lang === 'ja' ? 'GBA' : 'TOM';
  var dataUrl = root.getAttribute('data-json') || '/data/smh_fg_latest.json';

  function esc(str) {
    return String(str == null ? '' : str)
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;');
  }

  function zoneColor(score) {
    if (score < 25) return '#B91C1C';
    if (score < 45) return '#C2410C';
    if (score <= 55) return '#475569';
    if (score <= 75) return '#15803D';
    return '#0F2C22';
  }

  function zoneBg(score) {
    if (score < 25) return '#FEF2F2';
    if (score < 45) return '#FFF7ED';
    if (score <= 55) return '#F1F5F9';
    if (score <= 75) return '#F0FDF4';
    return '#ECFDF5';
  }

  function renderGaugeSvg(score) {
    var s = Math.max(0, Math.min(100, Number(score) || 0));
    var angleRad = Math.PI * (1 - s / 100);
    var cx = 160;
    var cy = 152;
    var r = 112;
    var nx = (cx + (r - 14) * Math.cos(angleRad)).toFixed(1);
    var ny = (cy - (r - 14) * Math.sin(angleRad)).toFixed(1);
    var col = zoneColor(s);

    return (
      '<svg viewBox="0 0 320 185" role="img" aria-label="SMH Fear and Greed Gauge ' +
      s.toFixed(1) +
      ' out of 100" style="width:100%;max-width:340px;height:auto;display:block;margin:0 auto;">' +
      '<defs>' +
      '<linearGradient id="smhFgGrad" x1="0%" y1="0%" x2="100%" y2="0%">' +
      '<stop offset="0%" stop-color="#B91C1C"/>' +
      '<stop offset="30%" stop-color="#EA580C"/>' +
      '<stop offset="50%" stop-color="#64748B"/>' +
      '<stop offset="75%" stop-color="#16A34A"/>' +
      '<stop offset="100%" stop-color="#0F2C22"/>' +
      '</linearGradient>' +
      '</defs>' +
      '<path d="M 48 152 A 112 112 0 0 1 272 152" fill="none" stroke="#E5E0D5" stroke-width="20" stroke-linecap="round"/>' +
      '<path d="M 48 152 A 112 112 0 0 1 272 152" fill="none" stroke="url(#smhFgGrad)" stroke-width="20" stroke-linecap="round" opacity="0.92"/>' +
      '<line x1="160" y1="152" x2="' + nx + '" y2="' + ny + '" stroke="#111827" stroke-width="4" stroke-linecap="round"/>' +
      '<circle cx="160" cy="152" r="9" fill="#0F2C22" stroke="#FAF7F2" stroke-width="3"/>' +
      '<text x="38" y="176" font-size="11" fill="#64748B" font-weight="600">0</text>' +
      '<text x="152" y="28" font-size="11" fill="#64748B" font-weight="600">50</text>' +
      '<text x="266" y="176" font-size="11" fill="#64748B" font-weight="600">100</text>' +
      '<text x="160" y="128" text-anchor="middle" font-size="38" font-weight="800" fill="' + col + '" style="font-variant-numeric:tabular-nums;">' + s.toFixed(1) + '</text>' +
      '</svg>'
    );
  }

  function renderHistorySvg(history) {
    if (!Array.isArray(history) || history.length < 2) return '';
    var w = 720;
    var h = 210;
    var padL = 38;
    var padR = 16;
    var padT = 16;
    var padB = 28;
    var innerW = w - padL - padR;
    var innerH = h - padT - padB;
    var pts = [];
    for (var i = 0; i < history.length; i++) {
      var x = padL + (i / (history.length - 1)) * innerW;
      var sc = Math.max(0, Math.min(100, Number(history[i].score) || 0));
      var y = padT + ((100 - sc) / 100) * innerH;
      pts.push(x.toFixed(1) + ',' + y.toFixed(1));
    }
    var y25 = (padT + 0.75 * innerH).toFixed(1);
    var y50 = (padT + 0.5 * innerH).toFixed(1);
    var y75 = (padT + 0.25 * innerH).toFixed(1);
    var firstDate = esc(history[0].date || '');
    var midDate = esc(history[Math.floor(history.length / 2)].date || '');
    var lastDate = esc(history[history.length - 1].date || '');
    var lastPt = pts[pts.length - 1].split(',');
    return (
      '<svg viewBox="0 0 ' + w + ' ' + h + '" role="img" aria-label="180-Day SMH Fear and Greed History" style="width:100%;height:auto;display:block;">' +
      '<rect x="' + padL + '" y="' + y25 + '" width="' + innerW + '" height="' + (innerH * 0.25).toFixed(1) + '" fill="#FEF2F2" opacity="0.65"/>' +
      '<rect x="' + padL + '" y="' + padT + '" width="' + innerW + '" height="' + (innerH * 0.25).toFixed(1) + '" fill="#ECFDF5" opacity="0.65"/>' +
      '<line x1="' + padL + '" y1="' + y75 + '" x2="' + (w - padR) + '" y2="' + y75 + '" stroke="#CBD5E1" stroke-dasharray="4 4"/>' +
      '<line x1="' + padL + '" y1="' + y50 + '" x2="' + (w - padR) + '" y2="' + y50 + '" stroke="#94A3B8" stroke-dasharray="4 4"/>' +
      '<line x1="' + padL + '" y1="' + y25 + '" x2="' + (w - padR) + '" y2="' + y25 + '" stroke="#FCA5A5" stroke-dasharray="4 4"/>' +
      '<text x="6" y="' + (Number(y75) + 4) + '" font-size="11" fill="#475569">75</text>' +
      '<text x="6" y="' + (Number(y50) + 4) + '" font-size="11" fill="#475569">50</text>' +
      '<text x="6" y="' + (Number(y25) + 4) + '" font-size="11" fill="#B91C1C">25</text>' +
      '<polyline fill="none" stroke="#0F2C22" stroke-width="2.5" stroke-linejoin="round" points="' + pts.join(' ') + '"/>' +
      '<circle cx="' + lastPt[0] + '" cy="' + lastPt[1] + '" r="5" fill="#B91C1C" stroke="#FFFFFF" stroke-width="2"/>' +
      '<text x="' + padL + '" y="' + (h - 6) + '" font-size="11" fill="#64748B">' + firstDate + '</text>' +
      '<text x="' + (padL + innerW / 2 - 28).toFixed(0) + '" y="' + (h - 6) + '" font-size="11" fill="#64748B">' + midDate + '</text>' +
      '<text x="' + (w - padR - 66) + '" y="' + (h - 6) + '" font-size="11" fill="#0F2C22" font-weight="700">' + lastDate + '</text>' +
      '</svg>'
    );
  }

  function renderData(d) {
    var score = Number(d.score || 0);
    var label = lang === 'ja' ? (d.label_ja || d.label_en) : d.label_en;
    var col = zoneColor(score);
    var bg = zoneBg(score);

    var gaugeEl = document.getElementById('smhFgGaugeMount');
    if (gaugeEl) gaugeEl.innerHTML = renderGaugeSvg(score);

    var badgeEl = document.getElementById('smhFgZoneBadge');
    if (badgeEl) {
      badgeEl.textContent = label + ' (' + score.toFixed(1) + ' / 100)';
      badgeEl.style.color = col;
      badgeEl.style.background = bg;
      badgeEl.style.borderColor = col;
    }

    var dateEl = document.getElementById('smhFgAsOf');
    if (dateEl) {
      dateEl.textContent = (lang === 'ja' ? '米国市場終値基準：' : 'As of US market close: ') + (d.as_of_date || '--');
    }

    var cmp = d.comparisons || {};
    var prices = d.prices || {};
    var statsEl = document.getElementById('smhFgCompareRow');
    if (statsEl) {
      var items = [
        { k: lang === 'ja' ? '前営業日' : 'Previous Close', v: Number(cmp.prev_1d || 0).toFixed(1) },
        { k: lang === 'ja' ? '1週間前' : '1 Week Ago', v: Number(cmp.prev_1w || 0).toFixed(1) },
        { k: lang === 'ja' ? '1ヶ月前' : '1 Month Ago', v: Number(cmp.prev_1m || 0).toFixed(1) },
        { k: 'SMH / XLV', v: '$' + Number(prices.SMH || 0).toFixed(2) + ' / $' + Number(prices.XLV || 0).toFixed(2) }
      ];
      statsEl.innerHTML = items
        .map(function (it) {
          return (
            '<div class="fg-stat-pill"><span class="fg-stat-k">' +
            esc(it.k) +
            '</span><strong class="fg-stat-v">' +
            esc(it.v) +
            '</strong></div>'
          );
        })
        .join('');
    }

    var facEl = document.getElementById('smhFgFactorsGrid');
    if (facEl && Array.isArray(d.factors)) {
      facEl.innerHTML = d.factors
        .map(function (f, i) {
          var sc = Number(f.score || 0);
          var fCol = zoneColor(sc);
          var fName = lang === 'ja' ? f.name_ja : f.name_en;
          var fRaw = lang === 'ja' ? f.raw_display_ja : f.raw_display;
          var fDesc = lang === 'ja' ? f.desc_ja : f.desc_en;
          return (
            '<article class="fg-factor-card">' +
            '<div class="fg-factor-head"><span class="fg-factor-num">' + (i + 1) + '</span>' +
            '<h3>' + esc(fName) + '</h3>' +
            '<span class="fg-factor-score" style="color:' + fCol + ';background:' + zoneBg(sc) + ';">' + sc.toFixed(1) + '</span></div>' +
            '<div class="fg-bar-track"><div class="fg-bar-fill" style="width:' + Math.max(3, Math.min(100, sc)).toFixed(0) + '%;background:' + fCol + ';"></div></div>' +
            '<div class="fg-factor-raw">' + esc(fRaw) + '</div>' +
            '<p class="fg-factor-desc">' + esc(fDesc) + '</p>' +
            '</article>'
          );
        })
        .join('');
    }

    var histEl = document.getElementById('smhFgHistoryMount');
    if (histEl) histEl.innerHTML = renderHistorySvg(d.history || []);

    var tblBody = document.getElementById('smhFgRegimeTableBody');
    if (tblBody && Array.isArray(d.historical_regimes)) {
      tblBody.innerHTML = d.historical_regimes
        .map(function (r) {
          return (
            '<tr>' +
            '<td><strong>' + esc(lang === 'ja' ? r.zone_ja : r.zone_en) + '</strong></td>' +
            '<td class="num">' + esc(r.share_pct) + '</td>' +
            '<td class="num">' + esc(r.smh_dd_median) + '</td>' +
            '<td class="num">' + esc(r.mix_dd_median) + '</td>' +
            '<td>' + esc(lang === 'ja' ? r.note_ja : r.note_en) + '</td>' +
            '</tr>'
          );
        })
        .join('');
    }
  }

  // Bind Extreme Fear/Greed Free Email Alert Form
  var alertForm = document.getElementById('smhFgAlertForm');
  if (alertForm) {
    alertForm.addEventListener('submit', function (ev) {
      ev.preventDefault();
      var emInp = document.getElementById('smhFgAlertEmail');
      var stEl = document.getElementById('smhFgAlertStatus');
      var btn = alertForm.querySelector('button[type="submit"]');
      var email = String(emInp ? emInp.value : '').trim().toLowerCase();
      if (!/^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(email)) {
        if (stEl) {
          stEl.style.display = 'block';
          stEl.style.color = '#991B1B';
          stEl.textContent = lang === 'ja'
            ? '有効なメールアドレスをご入力ください。'
            : 'Please enter a valid email address.';
        }
        return;
      }
      if (btn) btn.disabled = true;
      var done = function () {
        if (btn) btn.disabled = false;
        if (stEl) {
          stEl.style.display = 'block';
          stEl.style.color = '#065F46';
          stEl.textContent = lang === 'ja'
            ? '登録が完了しました。極度の恐怖（20以下）または極度の強欲（80以上）到達時に無料メールでお知らせします。'
            : 'Subscribed. We will email you automatically whenever the SMH Fear & Greed Index enters Extreme Fear (<=20) or Extreme Greed (>=80).';
        }
      };
      if (window.DreamCompanyCRM && typeof window.DreamCompanyCRM.registerMember === 'function') {
        window.DreamCompanyCRM.trackFunnelEvent(divCode, 'fg_alert_signup');
        window.DreamCompanyCRM.registerMember({
          div: divCode,
          email: email,
          segment: 'smh_fg_extreme_alert',
          lang: lang === 'ja' ? 'ja-JP' : 'en-US',
          notes: 'smh_fear_greed_extreme_alert'
        }).then(done).catch(done);
      } else {
        done();
      }
    });
  }

  if (window.DreamCompanyCRM && typeof window.DreamCompanyCRM.trackFunnelEvent === 'function') {
    window.DreamCompanyCRM.trackFunnelEvent(divCode, 'fg_view');
  }

  fetch(dataUrl + '?t=' + Math.floor(Date.now() / 300000), { cache: 'no-store' })
    .then(function (r) {
      if (!r.ok) throw new Error('HTTP ' + r.status);
      return r.json();
    })
    .then(renderData)
    .catch(function () {
      var badgeEl = document.getElementById('smhFgZoneBadge');
      if (badgeEl) {
        badgeEl.textContent = lang === 'ja' ? '最新データを読み込み中...' : 'Refreshing latest US close data...';
      }
    });
})();
