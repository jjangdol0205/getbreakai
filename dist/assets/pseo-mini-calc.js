/* Dream Company pSEO Embedded Interactive Mini-Calculator (Strict CSP, Zero Inline Handlers) */
(function () {
  'use strict';
  if (typeof window === 'undefined' || typeof document === 'undefined') return;

  function fmtNum(n) {
    return Math.round(n).toLocaleString('en-US');
  }

  function initTomCalc(root) {
    var inp = root.querySelector('[data-calc-input="usd"]');
    var btn = root.querySelector('[data-calc-run="1"]');
    var out = root.querySelector('[data-calc-out="1"]');
    if (!inp || !btn || !out) return;
    var smhDd = parseFloat(root.getAttribute('data-smh-dd') || '74.6');
    var mixDd = parseFloat(root.getAttribute('data-mix-dd') || '27.8');
    function run() {
      var amt = Math.max(10000, Math.min(20000000, parseFloat(inp.value) || 500000));
      var lossSmh = amt * (smhDd / 100);
      var lossMix = amt * (mixDd / 100);
      var saved = Math.max(0, lossSmh - lossMix);
      var reserve24 = amt * 0.15;
      out.innerHTML =
        '<strong>Sample Scale: $' + fmtNum(amt) + '</strong><br>' +
        '100% SMH Peak Historical Drawdown (-' + smhDd.toFixed(1) + '%): <strong>-$' + fmtNum(lossSmh) + '</strong><br>' +
        'Balanced SMH x XLV + SGOV Study (-' + mixDd.toFixed(1) + '%): <strong>-$' + fmtNum(lossMix) + '</strong> (historical cushion diff: <strong>+$' + fmtNum(saved) + '</strong>)<br>' +
        'Illustrative 15% Treasury Reserve (SGOV): <strong>$' + fmtNum(reserve24) + '</strong> (educational math only).';
      out.style.display = 'block';
    }
    btn.addEventListener('click', run);
    inp.addEventListener('change', run);
    run();
  }

  function initGbaCalc(root) {
    var inp = root.querySelector('[data-calc-input="manyen"]');
    var btn = root.querySelector('[data-calc-run="1"]');
    var out = root.querySelector('[data-calc-out="1"]');
    if (!inp || !btn || !out) return;
    function run() {
      var man = Math.max(100, Math.min(50000, parseFloat(inp.value) || 1800));
      var nisaGrowth = Math.min(1200, Math.round(man * 0.65));
      var cushion = Math.max(100, Math.round(man * 0.20));
      var overflow = Math.max(0, man - nisaGrowth - cushion);
      var ddSmh = Math.round(man * 0.746);
      var ddMix = Math.round(man * 0.278);
      out.innerHTML =
        '<strong>\u60f3\u5b9a\u898f\u6a21\uff1a' + fmtNum(man) + '\u4e07\u5186</strong><br>' +
        '\u65b0NISA \u6210\u9577\u6295\u8cc7\u67a0\u76ee\u5b89\uff08\u4e0a\u96501,200\u4e07\u5186\uff09\uff1a<strong>' + fmtNum(nisaGrowth) + '\u4e07\u5186</strong> \uff0f \u5b89\u5168\u30af\u30c3\u30b7\u30e7\u30f3\uff08\u500b\u4eba\u5411\u3051\u56fd\u50b5\u7b49\uff09\uff1a<strong>' + fmtNum(cushion) + '\u4e07\u5186</strong>' +
        (overflow > 0 ? (' \uff0f \u3064\u307f\u305f\u3066\u67a0\u30fb\u7279\u5b9a\u53e3\u5ea7\u533a\u5206\uff1a<strong>' + fmtNum(overflow) + '\u4e07\u5186</strong>') : '') + '<br>' +
        '2000\u20132025\u5e74\u6700\u5927\u4e0b\u843d\u7d71\u8a08\u6bd4\u8f03\uff1aSMH\u5358\u72ec <strong>-' + fmtNum(ddSmh) + '\u4e07\u5186</strong> vs 2\u672c\u67f1\u5747\u8861 <strong>-' + fmtNum(ddMix) + '\u4e07\u5186</strong>\uff08\u6559\u80b2\u53c2\u8003\uff09\u3002';
      out.style.display = 'block';
    }
    btn.addEventListener('click', run);
    inp.addEventListener('change', run);
    run();
  }

  function normPct(z) {
    var t = 1 / (1 + 0.2316419 * Math.abs(z));
    var d = 0.3989423 * Math.exp(-z * z / 2);
    var prob = d * t * (0.3193815 + t * (-0.3565638 + t * (1.781478 + t * (-1.821256 + t * 1.330274))));
    var p = z > 0 ? 1 - prob : prob;
    return Math.max(0.5, Math.min(99.5, p * 100));
  }

  function initGrowthCalc(root, lang) {
    var inp = root.querySelector('[data-calc-input="cm"]');
    var btn = root.querySelector('[data-calc-run="1"]');
    var out = root.querySelector('[data-calc-out="1"]');
    if (!inp || !btn || !out) return;
    var p50 = parseFloat(root.getAttribute('data-p50') || '138.8');
    var sd = parseFloat(root.getAttribute('data-sd') || '6.1');
    function run() {
      var cm = Math.max(70, Math.min(205, parseFloat(inp.value) || p50));
      var z = (cm - p50) / Math.max(2.0, sd);
      var pct = normPct(z);
      var diff = cm - p50;
      var sign = diff >= 0 ? '+' : '';
      var totalIn = cm / 2.54;
      var ft = Math.floor(totalIn / 12);
      var remIn = (totalIn - ft * 12).toFixed(1);
      if (lang === 'ko') {
        var zoneKo = pct >= 40
          ? '\uc548\uc2ec \uc21c\ud56d \uad6c\uac04'
          : (pct >= 18 ? '\ubc24 9\uc2dc \ubc18 \uc218\uba74\u00b7\uc601\uc591 \ubcf4\uac15 \uad6c\uac04' : '\uc18c\uc544\uacfc \ubc29\ubb38 \uc9c8\ubb38\uc9c0 \uc9c0\ucc38 \uad8c\uc7a5 \uad6c\uac04');
        out.innerHTML =
          '<strong>\uc785\ub825 \ud0a4 ' + cm.toFixed(1) + ' cm</strong> \u2192 \ub610\ub798 \uc57d <strong>' + pct.toFixed(1) + ' \ubc31\ubd84\uc704</strong> (\uc911\uac04\uac12 ' + p50.toFixed(1) + ' cm \ub300\ube44 <strong>' + sign + diff.toFixed(1) + ' cm</strong>)<br>' +
          '\ud604\uc7ac \uc0dd\ud65c \ud750\ub984 \uad6c\uac04: <strong>' + zoneKo + '</strong> \u2014 \uc544\ub798 1\ubd84 \ubb34\ub8cc \uacc4\uc0b0\uae30\uc5d0\uc11c \ubd80\ubaa8 \ud0a4\uc640 \ubf08\ub098\uc774 \uc2dc\ucc28(\u0394t)\uae4c\uc9c0 \ud568\uaed8 \ud655\uc778\ud574 \ubcf4\uc138\uc694.';
      } else {
        var zoneEn = pct >= 40
          ? 'Steady Growth Track'
          : (pct >= 18 ? 'Sleep & Routine Tune-Up Zone' : 'Pediatrician Visit Prep Recommended');
        out.innerHTML =
          '<strong>Entered Height: ' + ft + ' ft ' + remIn + ' in (' + cm.toFixed(1) + ' cm)</strong> &rarr; Approx. <strong>' + Math.round(pct) + 'th Percentile</strong> (' + sign + diff.toFixed(1) + ' cm vs. median ' + p50.toFixed(1) + ' cm)<br>' +
          'Status Band: <strong>' + zoneEn + '</strong> &mdash; Use the full 60-second check below to include both parents\' heights and any past wrist bone-age X-ray.';
      }
      out.style.display = 'block';
    }
    btn.addEventListener('click', run);
    inp.addEventListener('change', run);
    run();
  }

  function boot() {
    var boxes = document.querySelectorAll('[data-pseo-calc]');
    for (var i = 0; i < boxes.length; i++) {
      var kind = boxes[i].getAttribute('data-pseo-calc');
      if (kind === 'tom') initTomCalc(boxes[i]);
      else if (kind === 'gba') initGbaCalc(boxes[i]);
      else if (kind === 'kfg') initGrowthCalc(boxes[i], 'en');
      else if (kind === 'kfk') initGrowthCalc(boxes[i], 'ko');
    }
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', boot);
  } else {
    boot();
  }
})();
