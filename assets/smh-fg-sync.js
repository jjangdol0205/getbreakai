/* Live SMH Fear & Greed Sync Helper (Strict CSP, Same-Origin JSON, Zero Hangul) */
(function () {
  'use strict';
  if (typeof window === 'undefined' || typeof document === 'undefined' || typeof fetch !== 'function') return;
  function hydrate() {
    var tomEl = document.getElementById('tomLiveTempText');
    var gbaEl = document.getElementById('gbaLiveTempTextJp');
    if (!tomEl && !gbaEl) return;
    fetch('/data/smh_fg_latest.json?v=' + Math.floor(Date.now() / 300000), { cache: 'no-cache' })
      .then(function (r) { return r && r.ok ? r.json() : null; })
      .then(function (d) {
        if (!d || typeof d.score !== 'number' || !d.as_of_date) return;
        var sc = Number(d.score).toFixed(1);
        if (tomEl) {
          var regEn = String(d.label_en || 'Extreme Fear');
          tomEl.textContent = 'Data As Of: ' + d.as_of_date + ' \u00b7 SMH Fear & Greed: ' + sc + ' / 100 (' + regEn + ') \u2192';
        }
        if (gbaEl) {
          var regJa = String(d.label_ja || '\u6975\u5ea6\u306e\u6050\u6016');
          gbaEl.textContent = '\u6700\u65b0\u30c7\u30fc\u30bf\u57fa\u6e96\u65e5\uff1a' + d.as_of_date + ' \u30fb SMH\u6050\u6016\u3068\u5f37\u6b32\u6307\u6570\uff1a' + sc + ' / 100\uff08' + regJa + '\u570f\uff09 \u2192';
        }
      })
      .catch(function () {});
  }
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', hydrate);
  } else {
    hydrate();
  }
})();
