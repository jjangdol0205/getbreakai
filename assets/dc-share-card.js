/* Dream Company Client-Side Canvas Summary Share Card (1080x1080 PNG, Zero Server Cost, Zero PII, Strict CSP) */
(function initDreamCompanyShareCard() {
  'use strict';
  if (typeof window === 'undefined' || typeof document === 'undefined') return;
  if (window.__DC_SHARE_CARD_V1__) return;
  window.__DC_SHARE_CARD_V1__ = true;

  function detectDiv() {
    var host = String((window.location && window.location.hostname) || '').toLowerCase();
    var path = String((window.location && window.location.pathname) || '').toLowerCase();
    if (host.indexOf('kisfitglobal') !== -1 || host.indexOf('kfg-pages') !== -1) return 'KFG';
    if (host.indexOf('getbreakai') !== -1 || host.indexOf('gba-pages') !== -1) return 'GBA';
    if (host.indexOf('kidsfit.co.kr') !== -1 || host.indexOf('kfk-pages') !== -1) return 'KFK';
    if (path.indexOf('/jp') === 0) return 'GBA';
    return 'TOM';
  }

  var DIV = detectDiv();
  var PATH = String((window.location && window.location.pathname) || '/').toLowerCase();
  var IS_FG = PATH.indexOf('smh-fear-greed') !== -1;

  function injectStyle() {
    if (document.getElementById('dcShareCardStyle')) return;
    var st = document.createElement('style');
    st.id = 'dcShareCardStyle';
    st.textContent =
      '.dc-share-card-btn{display:inline-flex;align-items:center;justify-content:center;gap:6px;padding:9px 15px;min-height:40px;border-radius:8px;border:1.5px solid #0F2C22;background:#0F2C22;color:#FAF7F2;font-family:inherit;font-size:0.84rem;font-weight:700;cursor:pointer;text-decoration:none;transition:opacity 0.16s ease;}' +
      '.dc-share-card-btn:hover{opacity:0.9;}' +
      '.dc-share-card-wrap{display:flex;flex-wrap:wrap;align-items:center;justify-content:center;gap:10px;margin-top:14px;}' +
      '.dc-share-card-toast{font-size:0.8rem;font-weight:700;color:#065F46;}';
    document.head.appendChild(st);
  }

  function wrapLines(ctx, text, maxW) {
    var words = String(text || '').split(/\s+/);
    var lines = [];
    var cur = '';
    for (var i = 0; i < words.length; i++) {
      var test = cur ? (cur + ' ' + words[i]) : words[i];
      if (ctx.measureText(test).width > maxW && cur) {
        lines.push(cur);
        cur = words[i];
      } else {
        cur = test;
      }
    }
    if (cur) lines.push(cur);
    return lines;
  }

  function drawRoundedRect(ctx, x, y, w, h, r) {
    ctx.beginPath();
    ctx.moveTo(x + r, y);
    ctx.lineTo(x + w - r, y);
    ctx.quadraticCurveTo(x + w, y, x + w, y + r);
    ctx.lineTo(x + w, y + h - r);
    ctx.quadraticCurveTo(x + w, y + h, x + w - r, y + h);
    ctx.lineTo(x + r, y + h);
    ctx.quadraticCurveTo(x, y + h, x, y + h - r);
    ctx.lineTo(x, y + r);
    ctx.quadraticCurveTo(x, y, x + r, y);
    ctx.closePath();
  }

  function readLiveCardState() {
    if (DIV === 'TOM' || DIV === 'GBA') {
      var isJa = DIV === 'GBA';
      var score = 3.8;
      var asOf = '2026-11-24';
      var zoneLabel = isJa ? '極度の恐怖' : 'Extreme Fear';
      var ratioLine = '';

      var fgBadge = document.getElementById('smhFgZoneBadge');
      var fgAsOf = document.getElementById('smhFgAsOf');
      if (fgBadge) {
        var bm = String(fgBadge.textContent || '').match(/(\d+(?:\.\d+)?)/);
        if (bm) score = parseFloat(bm[1]);
        var parts = String(fgBadge.textContent || '').split(/·|—|-|\|/);
        if (parts.length > 1) zoneLabel = parts[parts.length - 1].trim();
      }
      if (fgAsOf) {
        var dm = String(fgAsOf.textContent || '').match(/(\d{4}-\d{2}-\d{2})/);
        if (dm) asOf = dm[1];
      }
      var tempEl = document.getElementById(isJa ? 'gbaLiveTempTextJp' : 'tomLiveTempText');
      if (!fgBadge && tempEl) {
        var tt = String(tempEl.textContent || '');
        var tm = tt.match(/(\d+(?:\.\d+)?)\s*\/\s*100/);
        if (tm) score = parseFloat(tm[1]);
        var td = tt.match(/(\d{4}-\d{2}-\d{2})/);
        if (td) asOf = td[1];
      }
      var ratioEl = document.getElementById(isJa ? 'pwUnlockedRatioHeadlineJp' : 'pwUnlockedRatioHeadline');
      if (ratioEl && ratioEl.offsetParent !== null) {
        ratioLine = String(ratioEl.textContent || '').trim();
      }
      var badge3 = document.getElementById('dcGbaStage3Badge');
      return {
        kind: 'finance',
        brand: isJa ? 'GETBREAK AI JAPAN' : 'TRUTH OF MARKET',
        kicker: isJa ? '米国半導体（SMH）恐怖と強欲指数 ・ 過去統計' : 'SMH SEMICONDUCTOR FEAR & GREED INDEX',
        title: ratioLine || (isJa ? '本日のSMH市場温度スコア' : "Today's SMH Market Structure Score"),
        score: Math.max(0, Math.min(100, Number(score) || 0)),
        zoneLabel: zoneLabel,
        badgeLine: (badge3 && badge3.textContent) ? badge3.textContent.trim() : (isJa ? '2000–2025年 公開ETF統計（教育参考）' : '2000-2025 Public ETF Historical Statistics'),
        asOf: asOf,
        domain: isJa ? 'getbreakai.com/jp/smh-fear-greed' : 'truthofmarket.com/smh-fear-greed',
        filename: isJa ? 'getbreakai-smh-summary.png' : 'truthofmarket-smh-summary.png',
        footerNote: isJa ? '投資助言・売買推奨なし ／ 公開ETF統計の教育参考カード' : 'Independent Educational Research · Zero Trade Signals'
      };
    }

    // KFG or KFK — ZERO PII (NO child name, NO DOB!)
    var isKo = DIV === 'KFK';
    var pct = 50;
    var ageBand = isKo ? '\ucd08\ub4f1·\uccad\uc18c\ub144 \uc131\uc7a5 \uad6c\uac04' : 'Childhood Growth Band';
    if (isKo) {
      var kp = document.getElementById('result-free-percentile');
      if (kp) {
        var km = String(kp.textContent || '').match(/(\d+(?:\.\d+)?)/);
        if (km) pct = parseFloat(km[1]);
      }
      var ageInp = document.getElementById('kfk-vip-age');
      var headEl = document.getElementById('result-child-headline');
      var hTxt = headEl ? String(headEl.textContent || '') : '';
      var am = hTxt.match(/\ub9cc\s*(\d+)\s*\uc138/);
      if (am) ageBand = '\ub9cc ' + am[1] + '\uc138 \ub610\ub798 \uae30\uc900 (\uac1c\uc778\uc815\ubcf4 \ube44\ud3ec\ud568)';
      else if (ageInp && ageInp.value) ageBand = '\ub9cc ' + ageInp.value + '\uc138 \ub610\ub798 \uae30\uc900';
    } else {
      var ep = document.getElementById('kfg-res-percentile') || document.querySelector('#kfg-partial-baseline-summary [data-kfg-percentile]');
      if (ep) {
        var rawAttr = ep.getAttribute('data-kfg-percentile') || ep.textContent || '';
        var em = String(rawAttr).match(/(\d+(?:\.\d+)?)/);
        if (em) pct = parseFloat(em[1]);
      }
      var ageNote = document.getElementById('kfg-live-age-note');
      if (ageNote) {
        var ym = String(ageNote.textContent || '').match(/(\d+)\s*year/i);
        if (ym) ageBand = 'Age ' + ym[1] + ' Peer Band (Zero PII)';
      }
    }

    var stageEl = document.getElementById(isKo ? 'dcKfkStage3Badge' : 'dcKfgStage3Badge');
    var stageLabel = stageEl && stageEl.textContent
      ? stageEl.textContent.trim()
      : (isKo
        ? (pct >= 40 ? '\uc548\uc2ec \uc21c\ud56d \uad6c\uac04' : pct >= 18 ? '\ubc24 9\uc2dc \ubc18 \uc218\uba74·\uc601\uc591 \ubcf4\uac15 \uad6c\uac04' : '\uc18c\uc544\uacfc \ubc29\ubb38 \uc9c8\ubb38\uc9c0 \uc9c0\ucc38 \uad8c\uc7a5 \uad6c\uac04')
        : (pct >= 40 ? 'Steady Growth Track (US CDC Guide)' : pct >= 18 ? 'Sleep & Routine Tune-Up Zone' : 'Pediatrician Visit Prep Recommended'));

    return {
      kind: 'growth',
      brand: isKo ? '\ud0a4\uc988\ud54f \uc131\uc7a5 \uc5f0\uad6c\uc18c' : 'KISFIT STUDIO',
      kicker: isKo ? '\uc9c8\ubcd1\uad00\ub9ac\uccad(KDCA 2017) \uacf5\uc2dd \uc131\uc7a5\ub3c4\ud45c \uc694\uc57d \uce74\ub4dc' : 'US CDC 2000 GROWTH PERCENTILE SUMMARY',
      title: ageBand,
      score: Math.max(1, Math.min(99, Number(pct) || 50)),
      zoneLabel: isKo ? (pct.toFixed(1) + ' \ubc31\ubd84\uc704') : (Math.round(pct) + 'th Percentile'),
      badgeLine: stageLabel,
      asOf: new Date().toISOString().slice(0, 10),
      domain: isKo ? 'kidsfit.co.kr' : 'kisfitglobal.com',
      filename: isKo ? 'kidsfit-growth-summary.png' : 'kisfit-growth-summary.png',
      footerNote: isKo ? '\uc544\uc774 \uc774\ub984·\uc0dd\ub144\uc6d4\uc77c \ubbf8\ud3ec\ud568 · \uc9c8\ubcd1\uad00\ub9ac\uccad \uacf5\uacf5 \ub370\uc774\ud130 \uae30\uc900 \uac00\uc815\uc6a9 \ucc38\uace0 \uce74\ub4dc' : 'Zero Child Name or DOB Included · Public US CDC Educational Reference'
    };
  }

  function renderCanvas(data) {
    var c = document.createElement('canvas');
    c.width = 1080;
    c.height = 1080;
    var ctx = c.getContext('2d');

    // Warm editorial ivory canvas
    ctx.fillStyle = '#FAF7F2';
    ctx.fillRect(0, 0, 1080, 1080);

    // Subtle double frame
    ctx.strokeStyle = '#DFD7CC';
    ctx.lineWidth = 4;
    drawRoundedRect(ctx, 40, 40, 1000, 1000, 28);
    ctx.stroke();

    // Top forest green editorial ribbon
    ctx.fillStyle = '#0F2C22';
    drawRoundedRect(ctx, 64, 64, 952, 130, 20);
    ctx.fill();

    ctx.fillStyle = '#A7F3D0';
    ctx.font = '700 24px Inter, "Noto Sans JP", "Malgun Gothic", sans-serif';
    ctx.textAlign = 'center';
    ctx.fillText(data.brand, 540, 118);

    ctx.fillStyle = '#FAF7F2';
    ctx.font = '600 22px Inter, "Noto Sans JP", "Malgun Gothic", sans-serif';
    ctx.fillText(data.kicker, 540, 162);

    // Title
    ctx.fillStyle = '#111827';
    ctx.font = '700 40px Georgia, "Noto Serif JP", "Malgun Gothic", serif';
    var titleLines = wrapLines(ctx, data.title, 860);
    var ty = 270;
    for (var i = 0; i < Math.min(2, titleLines.length); i++) {
      ctx.fillText(titleLines[i], 540, ty);
      ty += 52;
    }

    // Center Visual: Semicircular Gauge (Finance) or Horizontal Percentile Track (Growth)
    if (data.kind === 'finance') {
      var cx = 540;
      var cy = 540;
      var rad = 185;
      // Background arc
      ctx.lineWidth = 34;
      ctx.lineCap = 'round';
      ctx.strokeStyle = '#E5E0D5';
      ctx.beginPath();
      ctx.arc(cx, cy, rad, Math.PI, 2 * Math.PI, false);
      ctx.stroke();

      // Colored active arc
      var endAng = Math.PI + (Math.PI * (data.score / 100));
      ctx.strokeStyle = data.score < 25 ? '#B91C1C' : data.score < 45 ? '#D97706' : data.score <= 55 ? '#475569' : '#059669';
      ctx.beginPath();
      ctx.arc(cx, cy, rad, Math.PI, Math.max(Math.PI + 0.08, endAng), false);
      ctx.stroke();

      // Big score number
      ctx.fillStyle = '#0F2C22';
      ctx.font = '800 96px Inter, sans-serif';
      ctx.fillText(data.score.toFixed(1), cx, cy - 22);

      ctx.fillStyle = '#6B7280';
      ctx.font = '700 26px Inter, sans-serif';
      ctx.fillText('/ 100', cx, cy + 20);

      // Zone pill
      ctx.fillStyle = '#ECFDF5';
      drawRoundedRect(ctx, 290, 590, 500, 68, 34);
      ctx.fill();
      ctx.strokeStyle = '#0F2C22';
      ctx.lineWidth = 3;
      ctx.stroke();
      ctx.fillStyle = '#0F2C22';
      ctx.font = '800 32px Inter, "Noto Sans JP", sans-serif';
      ctx.fillText(data.zoneLabel + '  ·  ' + data.asOf, 540, 636);
    } else {
      // Big Percentile Score Card
      ctx.fillStyle = '#FFFFFF';
      drawRoundedRect(ctx, 130, 360, 820, 290, 24);
      ctx.fill();
      ctx.strokeStyle = '#D6CEC3';
      ctx.lineWidth = 3;
      ctx.stroke();

      ctx.fillStyle = '#0F2C22';
      ctx.font = '800 88px Inter, "Malgun Gothic", sans-serif';
      ctx.fillText(data.zoneLabel, 540, 480);

      // Percentile track
      var tx = 200;
      var tw = 680;
      var py = 545;
      ctx.fillStyle = '#EDE8DD';
      drawRoundedRect(ctx, tx, py, tw, 24, 12);
      ctx.fill();
      var fillW = Math.max(24, Math.round(tw * (data.score / 100)));
      ctx.fillStyle = '#2F5241';
      drawRoundedRect(ctx, tx, py, fillW, 24, 12);
      ctx.fill();
      // Pin circle
      ctx.fillStyle = '#B45309';
      ctx.beginPath();
      ctx.arc(tx + fillW, py + 12, 18, 0, Math.PI * 2);
      ctx.fill();

      ctx.fillStyle = '#6B635B';
      ctx.font = '600 22px Inter, "Malgun Gothic", sans-serif';
      ctx.textAlign = 'left';
      ctx.fillText('3%', tx, py + 58);
      ctx.textAlign = 'center';
      ctx.fillText('50%', tx + tw / 2, py + 58);
      ctx.textAlign = 'right';
      ctx.fillText('97%', tx + tw, py + 58);
      ctx.textAlign = 'center';
    }

    // 3-Stage Status / Highlight Pill
    ctx.fillStyle = '#FFFBEB';
    drawRoundedRect(ctx, 130, 710, 820, 86, 18);
    ctx.fill();
    ctx.strokeStyle = '#D97706';
    ctx.lineWidth = 2.5;
    ctx.stroke();
    ctx.fillStyle = '#78350F';
    ctx.font = '800 30px Inter, "Noto Sans JP", "Malgun Gothic", sans-serif';
    ctx.fillText(data.badgeLine, 540, 764);

    // Bottom Brand URL Watermark Bar
    ctx.fillStyle = '#0F2C22';
    drawRoundedRect(ctx, 130, 845, 820, 86, 16);
    ctx.fill();
    ctx.fillStyle = '#FAF7F2';
    ctx.font = '700 32px Inter, sans-serif';
    ctx.fillText(data.domain, 540, 900);

    // Subtle disclaimer footer
    ctx.fillStyle = '#6B7280';
    ctx.font = '500 20px Inter, "Noto Sans JP", "Malgun Gothic", sans-serif';
    ctx.fillText(data.footerNote, 540, 990);

    return c;
  }

  function triggerDownloadOrShare(toastEl) {
    var data = readLiveCardState();
    var canvas = renderCanvas(data);
    if (window.DreamCompanyCRM && typeof window.DreamCompanyCRM.trackFunnelEvent === 'function') {
      try { window.DreamCompanyCRM.trackFunnelEvent(DIV, 'share_card_png'); } catch (_) {}
    }
    function setToast(msg) {
      if (!toastEl) return;
      toastEl.textContent = msg;
      setTimeout(function () { if (toastEl.textContent === msg) toastEl.textContent = ''; }, 3200);
    }
    var doneLabel = DIV === 'KFK' ? '\uc694\uc57d \uce74\ub4dc PNG \uc800\uc7a5 \uc644\ub8cc ✓' : (DIV === 'GBA' ? '要約カードPNGを保存しました ✓' : 'Summary Card PNG Saved ✓');

    if (canvas.toBlob) {
      canvas.toBlob(function (blob) {
        if (!blob) return;
        try {
          var file = new File([blob], data.filename, { type: 'image/png' });
          if (navigator.canShare && navigator.share && navigator.canShare({ files: [file] })) {
            navigator.share({ files: [file], title: data.brand, text: data.domain }).then(function () {
              setToast(doneLabel);
            }).catch(function () {
              var u = URL.createObjectURL(blob);
              var a = document.createElement('a');
              a.href = u;
              a.download = data.filename;
              document.body.appendChild(a);
              a.click();
              document.body.removeChild(a);
              setTimeout(function () { URL.revokeObjectURL(u); }, 2500);
              setToast(doneLabel);
            });
            return;
          }
        } catch (_) {}
        var url = URL.createObjectURL(blob);
        var a2 = document.createElement('a');
        a2.href = url;
        a2.download = data.filename;
        document.body.appendChild(a2);
        a2.click();
        document.body.removeChild(a2);
        setTimeout(function () { URL.revokeObjectURL(url); }, 2500);
        setToast(doneLabel);
      }, 'image/png');
    } else {
      var a3 = document.createElement('a');
      a3.href = canvas.toDataURL('image/png');
      a3.download = data.filename;
      document.body.appendChild(a3);
      a3.click();
      document.body.removeChild(a3);
      setToast(doneLabel);
    }
  }

  function createShareButton(btnId) {
    var label = DIV === 'KFK'
      ? '\uc694\uc57d \uce74\ub4dc \uc774\ubbf8\uc9c0 \uc800\uc7a5 (PNG)'
      : (DIV === 'GBA'
        ? (IS_FG ? '本日のSMH指数カードを画像保存（PNG）' : '要約カードを画像保存（PNG）')
        : (IS_FG ? "Save / Share Today's SMH Card (PNG)" : 'Save Summary Card (PNG)'));
    var wrap = document.createElement('div');
    wrap.className = 'dc-share-card-wrap';
    var btn = document.createElement('button');
    btn.type = 'button';
    btn.id = btnId;
    btn.className = 'dc-share-card-btn';
    btn.textContent = label;
    var toast = document.createElement('span');
    toast.className = 'dc-share-card-toast';
    toast.setAttribute('role', 'status');
    toast.setAttribute('aria-live', 'polite');
    btn.addEventListener('click', function () {
      triggerDownloadOrShare(toast);
    });
    wrap.appendChild(btn);
    wrap.appendChild(toast);
    return wrap;
  }

  function tryMount() {
    if (document.getElementById('btn-dc-share-card')) return;
    var target = null;
    if (IS_FG) {
      target = document.querySelector('.fg-hero-card');
    } else if (DIV === 'TOM') {
      target = document.getElementById('pwFreeBaselineSummaryView');
    } else if (DIV === 'GBA') {
      target = document.getElementById('gba-top-share-bar-jp') || document.getElementById('pwFreeBaselineSummaryJp');
    } else if (DIV === 'KFG') {
      target = document.getElementById('kfg-top-share-bar') || document.getElementById('kfg-partial-baseline-summary');
    } else if (DIV === 'KFK') {
      target = document.getElementById('kfk-top-share-bar') || document.getElementById('kfk-free-summary-card');
    }
    if (target) {
      target.appendChild(createShareButton('btn-dc-share-card'));
    }
  }

  function boot() {
    injectStyle();
    tryMount();
    var obs = new MutationObserver(function () { tryMount(); });
    obs.observe(document.body, { childList: true, subtree: true });
  }

  window.DreamCompanyShareCard = {
    renderDataUrl: function () {
      var data = readLiveCardState();
      return renderCanvas(data).toDataURL('image/png');
    },
    readState: readLiveCardState
  };

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', boot);
  } else {
    boot();
  }
})();
