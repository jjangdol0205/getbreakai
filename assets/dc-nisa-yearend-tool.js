(function () {
  'use strict';

  function buildCleanShareUrl(rawUrl, extraParams) {
    var base = String(rawUrl || (window.location.origin + window.location.pathname));
    var u = new URL(base);
    ['internal_check', 'owner_device', 'internal_test', 'smoke_test', 'nocache'].forEach(function (k) {
      u.searchParams.delete(k);
    });
    if (extraParams && typeof extraParams === 'object') {
      Object.keys(extraParams).forEach(function (k) {
        if (extraParams[k] !== undefined && extraParams[k] !== null && extraParams[k] !== '') {
          u.searchParams.set(k, String(extraParams[k]));
        }
      });
    }
    var vid = '';
    try {
      if (window.DreamCompanyCRM && typeof window.DreamCompanyCRM.getOrCreateVisitorProfile === 'function') {
        vid = window.DreamCompanyCRM.getOrCreateVisitorProfile().visitor_id || '';
      } else {
        vid = localStorage.getItem('dc_visitor_id') || '';
        if (!vid) {
          vid = 'v_' + Math.random().toString(36).slice(2, 10) + Date.now().toString(36).slice(-4);
          localStorage.setItem('dc_visitor_id', vid);
        }
      }
    } catch (_) {}
    if (vid) u.searchParams.set('ref', vid);
    if (!u.searchParams.get('utm_source')) u.searchParams.set('utm_source', 'referral');
    if (!u.searchParams.get('utm_medium')) u.searchParams.set('utm_medium', 'share');
    return u.toString();
  }
  window.__dcBuildCleanShareUrl = buildCleanShareUrl;

  function triggerOneTouchShare(div, title, text, shareUrl, toastEl, copiedMsg) {
    var cleanUrl = buildCleanShareUrl(shareUrl);
    if (window.DreamCompanyCRM && typeof window.DreamCompanyCRM.trackFunnelEvent === 'function') {
      window.DreamCompanyCRM.trackFunnelEvent(div, 'share_click', { event_meta: 'seasonal_share_card' });
    }
    function showToast(msg) {
      if (!toastEl) return;
      toastEl.textContent = msg;
      toastEl.style.display = 'block';
    }
    if (navigator.share) {
      navigator.share({ title: title, text: text, url: cleanUrl }).then(function () {
        showToast(copiedMsg);
      }).catch(function () {
        if (navigator.clipboard && navigator.clipboard.writeText) {
          navigator.clipboard.writeText(cleanUrl).then(function () { showToast(copiedMsg); }).catch(function () { showToast(cleanUrl); });
        } else {
          showToast(cleanUrl);
        }
      });
    } else if (navigator.clipboard && navigator.clipboard.writeText) {
      navigator.clipboard.writeText(cleanUrl).then(function () { showToast(copiedMsg); }).catch(function () { showToast(cleanUrl); });
    } else {
      showToast(cleanUrl);
    }
    return cleanUrl;
  }

  function fmtMan(n) {
    return Math.max(0, Math.round(n * 10) / 10).toLocaleString('ja-JP') + '万円';
  }

  function calc() {
    var tsuUsed = Math.max(0, Math.min(120, parseFloat(document.getElementById('nisaTsuUsed').value) || 0));
    var groUsed = Math.max(0, Math.min(240, parseFloat(document.getElementById('nisaGroUsed').value) || 0));
    var lifeUsed = Math.max(0, Math.min(1800, parseFloat(document.getElementById('nisaLifeUsed').value) || 0));
    var sellCost = Math.max(0, Math.min(lifeUsed, parseFloat(document.getElementById('nisaSellCost').value) || 0));
    var sellMkt = Math.max(0, parseFloat(document.getElementById('nisaSellMkt').value) || 0);

    var remTsu = Math.max(0, 120 - tsuUsed);
    var remGro = Math.max(0, 240 - groUsed);
    var remLifeNow = Math.max(0, 1800 - lifeUsed);
    var rem2026Total = Math.min(remTsu + remGro, remLifeNow);

    // 金融庁ルール: 売却した商品の「簿価(取得原価)」分のみ翌年1月1日に生涯枠が復活（時価ではない）
    var revive2027 = sellCost;
    var lifeAfterRevive = Math.min(1800, remLifeNow + revive2027);
    var nextYearCap = Math.min(360, lifeAfterRevive);
    var mktDiff = sellMkt - sellCost;

    document.getElementById('gbaOutRemTsu').textContent = fmtMan(remTsu);
    document.getElementById('gbaOutRemGro').textContent = fmtMan(remGro);
    document.getElementById('gbaOutRemTotal').textContent = fmtMan(rem2026Total);
    document.getElementById('gbaOutRevive').textContent = fmtMan(revive2027) + '（簿価ベース）';
    document.getElementById('gbaOutLife2027').textContent = fmtMan(lifeAfterRevive) + ' / 1,800万円';
    document.getElementById('gbaOutNextCap').textContent = fmtMan(nextYearCap) + '（年間上限360万円）';
    document.getElementById('gbaOutNote').textContent = sellCost > 0
      ? ('売却時価 ' + fmtMan(sellMkt) + '（評価損益 ' + (mktDiff >= 0 ? '+' : '') + Math.round(mktDiff) + '万円）のうち、2027年1月1日に復活するのは取得原価（簿価）の ' + fmtMan(revive2027) + ' です。年間上限360万円は変わりません。')
      : '2026年内の残余非課税枠は年末の受渡日基準で締切となります。無理に一括消費せず、翌年枠（360万円）と分散設計を落ち着いて比較してください。';
  }

  document.addEventListener('DOMContentLoaded', function () {
    ['nisaTsuUsed', 'nisaGroUsed', 'nisaLifeUsed', 'nisaSellCost', 'nisaSellMkt'].forEach(function (id) {
      document.getElementById(id).addEventListener('input', calc);
    });
    var btn = document.getElementById('btnGbaSeasonalShare');
    if (btn) {
      btn.addEventListener('click', function () {
        var remTxt = (document.getElementById('gbaOutRemTotal') || {}).textContent || '';
        triggerOneTouchShare(
          'GBA',
          '2026年 新NISA 年末残余枠＆2027年簿価復活計算機 | GetBreakAI',
          '今年の残余非課税枠（' + remTxt + '）と翌年1月の簿価枠復活を10秒確認：',
          'https://getbreakai.com/jp/tools/nisa-year-end',
          document.getElementById('gbaSeasonalShareToast'),
          '共有リンクをコピーしました（ご家族・ご友人へそのまま送れます）'
        );
      });
    }
    calc();
  });
})();
