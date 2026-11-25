/* Live SMH Fear & Greed Sync Helper v2 (Strict CSP, Same-Origin JSON, Overwrite-Proof) */
(function () {
  'use strict';
  if (typeof window === 'undefined' || typeof document === 'undefined' || typeof fetch !== 'function') return;
  var canonicalTom = '';
  var canonicalGba = '';

  function enforceText() {
    var tomEl = document.getElementById('tomLiveTempText');
    if (tomEl && canonicalTom && tomEl.textContent !== canonicalTom) {
      tomEl.textContent = canonicalTom;
    }
    var gbaEl = document.getElementById('gbaLiveTempTextJp');
    if (gbaEl && canonicalGba && gbaEl.textContent !== canonicalGba) {
      gbaEl.textContent = canonicalGba;
    }
  }

  function hydrate() {
    var tomEl = document.getElementById('tomLiveTempText');
    var gbaEl = document.getElementById('gbaLiveTempTextJp');
    if (!tomEl && !gbaEl) return;
    fetch('/data/smh_fg_latest.json?v=' + Math.floor(Date.now() / 300000), { cache: 'no-cache' })
      .then(function (r) { return r && r.ok ? r.json() : null; })
      .then(function (d) {
        if (!d || typeof d.score !== 'number' || !d.as_of_date) return;
        var sc = Number(d.score).toFixed(1);
        canonicalTom = 'Data As Of: ' + d.as_of_date + ' \u00b7 SMH Fear & Greed: ' + sc + ' / 100 (' + String(d.label_en || 'Extreme Fear') + ') \u2192';
        canonicalGba = '\u6700\u65b0\u30c7\u30fc\u30bf\u57fa\u6e96\u65e5\uff1a' + d.as_of_date + ' \u30fb SMH\u6050\u6016\u3068\u5f37\u6b32\u6307\u6570\uff1a' + sc + ' / 100\uff08' + String(d.label_ja || '\u6975\u5ea6\u306e\u6050\u6016') + '\u570f\uff09 \u2192';
        enforceText();
        [tomEl, gbaEl].forEach(function (el) {
          if (!el || el._smhFgObs) return;
          el._smhFgObs = true;
          var mo = new MutationObserver(enforceText);
          mo.observe(el, { childList: true, characterData: true, subtree: true });
        });
        setTimeout(enforceText, 450);
        setTimeout(enforceText, 1200);
      })
      .catch(function () {});
  }
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', hydrate);
  } else {
    hydrate();
  }
  window.addEventListener('load', enforceText);
})();
