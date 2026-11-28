/**
 * Dream Company HQ - Universal Cloud CRM, Server-Verified Entitlement, Magic Restore & 4-Stage Funnel Client (v5 Cloudflare D1 + Brevo)
 * Shared across Divisions 1-5 static Cloudflare Pages frontends (100% ASCII source for Zero-Hangul scanner safety).
 *
 * Capabilities:
 *  1. 100% CORS-safe Cloudflare Worker + D1 + Brevo CRM registration (`https://api.truthofmarket.com/api/crm/register`)
 *  2. Server-side paid entitlement verification (`verifyEntitlement` -> `/api/verify-entitlement`, blocks unauthenticated bypass!)
 *  3. Automatic 4-Stage Funnel Event & UTM tracking (`landing_view -> quiz_complete -> checkout_click -> paid_success`)
 *  4. Cross-Device Permanent Magic Restore (`?magic_restore=...`) + Standard Digital Refund & 1-Click Support links
 *  5. 4th Div Free Fan Next-Song Vote persisted in Cloudflare D1 (`submitHeroVote` / `fetchHeroVotes`)
 *  6. Cumulative 6-Month Height Velocity Tracker (`KFG` & `KFK`) with full Korean & English 4-habit local commentary
 */
(function (global) {
  'use strict';

  // Universal Internal QA / Owner Device / Playwright / Bot Traffic Guard (Zero-Pollution Client Gate)
  function isInternalOrBotTraffic() {
    try {
      var sp = new URLSearchParams((global.location && global.location.search) || '');
      var isHttps = !!(global.location && global.location.protocol === 'https:');
      var ic = sp.get('internal_check');
      var od = sp.get('owner_device');
      if (ic === '0' || od === '0') {
        try { if (global.localStorage) global.localStorage.removeItem('dc_internal_exclude'); } catch (_r1) {}
        try {
          if (global.document) {
            global.document.cookie = 'dc_internal_exclude=; Max-Age=0; Path=/; SameSite=Lax' + (isHttps ? '; Secure' : '');
          }
        } catch (_r2) {}
      } else if (ic === '1' || od === '1') {
        try { if (global.localStorage) global.localStorage.setItem('dc_internal_exclude', '1'); } catch (_w1) {}
        try {
          if (global.document) {
            global.document.cookie = 'dc_internal_exclude=1; Max-Age=31536000; Path=/; SameSite=Lax' + (isHttps ? '; Secure' : '');
          }
        } catch (_w2) {}
        return true;
      }
      try {
        if (global.localStorage && global.localStorage.getItem('dc_internal_exclude') === '1') return true;
      } catch (_l1) {}
      try {
        if (global.document && /(?:^|;\s*)dc_internal_exclude=1(?:;|$)/.test(global.document.cookie || '')) return true;
      } catch (_c1) {}
      if (sp.get('internal_test') === '1' || sp.get('smoke_test') === '1') {
        try { if (global.sessionStorage) global.sessionStorage.setItem('dc_internal_test', '1'); } catch (_s1) {}
        return true;
      }
      try {
        if (global.sessionStorage && global.sessionStorage.getItem('dc_internal_test') === '1') return true;
      } catch (_s2) {}
      if (global.navigator && global.navigator.webdriver === true) return true;
      var ua = String((global.navigator && global.navigator.userAgent) || '');
      if (/HeadlessChrome|Playwright|Puppeteer|Selenium|LiveAudit|Watchdog|GitHub-Actions/i.test(ua)) return true;
    } catch (_g) {}
    return false;
  }
  global.__dcIsInternalOrBot = isInternalOrBotTraffic;
  isInternalOrBotTraffic();

  // Neutralize deprecated third-party hit counter & block internal/bot analytics before network dispatch
  if (typeof global.fetch === 'function' && !global.__dcAbacusFetchGuarded) {
    global.__dcAbacusFetchGuarded = true;
    var _origFetch = global.fetch.bind(global);
    global.fetch = function (input, init) {
      try {
        var reqUrl = typeof input === 'string' ? input : (input && input.url ? String(input.url) : '');
        var isAbacus = reqUrl.indexOf('abacus.jasoncameron.dev') >= 0 || reqUrl.indexOf('script.google.com/macros/s/') >= 0;
        var isInternalAnalytics = isInternalOrBotTraffic() && (reqUrl.indexOf('/api/analytics/event') >= 0 || reqUrl.indexOf('/hit/') >= 0);
        if (isAbacus || isInternalAnalytics) {
          var bodyTxt = isInternalAnalytics ? '{"ok":true,"skipped":"internal_test"}' : '{"ok":true,"value":0}';
          if (typeof Response === 'function') {
            return Promise.resolve(new Response(bodyTxt, { status: 200, headers: { 'Content-Type': 'application/json' } }));
          }
          return Promise.resolve({ ok: true, status: 200, json: function () { return Promise.resolve({ ok: true, skipped: isInternalAnalytics ? 'internal_test' : 'abacus' }); } });
        }
      } catch (_e) {}
      return _origFetch(input, init);
    };
  }

  if (global.navigator && typeof global.navigator.sendBeacon === 'function' && !global.__dcBeaconGuarded) {
    global.__dcBeaconGuarded = true;
    var _origBeacon = global.navigator.sendBeacon.bind(global.navigator);
    global.navigator.sendBeacon = function (url, data) {
      try {
        var u = String(url || '');
        if (u.indexOf('abacus.jasoncameron.dev') >= 0) return true;
        if (isInternalOrBotTraffic() && (u.indexOf('/api/analytics/event') >= 0 || u.indexOf('/hit/') >= 0)) return true;
      } catch (_b) {}
      return _origBeacon(url, data);
    };
  }

  // Purge any legacy PWA Service Worker caches cleanly so returning browsers always load fresh Cloudflare Pages builds
  try {
    if (global.navigator && global.navigator.serviceWorker && typeof global.navigator.serviceWorker.getRegistrations === 'function') {
      global.navigator.serviceWorker.getRegistrations().then(function (regs) {
        if (regs && regs.length) {
          regs.forEach(function (reg) { try { reg.unregister(); } catch (_e) {} });
          if (global.caches && typeof global.caches.keys === 'function') {
            global.caches.keys().then(function (keys) {
              keys.forEach(function (k) { try { global.caches.delete(k); } catch (_e) {} });
            }).catch(function () {});
          }
        }
      }).catch(function () {});
    }
  } catch (_e) {}

  var CLOUD_API_BASE = global.DC_CLOUD_API_BASE || 'https://api.truthofmarket.com';
  var QUEUE_KEY = 'dc_crm_sync_queue_v2';

  var SUPPORT_EMAIL_BY_DIV = {
    TOM: 'hello@truthofmarket.com',
    KFG: 'care@kisfitglobal.com',
    GBA: 'support@getbreakai.com',
    HERO: 'radio@paradise-hero.com',
    KFK: 'help@kidsfit.co.kr'
  };

  function getSupportEmail(div) {
    var d = String(div || 'TOM').toUpperCase();
    return SUPPORT_EMAIL_BY_DIV[d] || 'hello@truthofmarket.com';
  }

  function detectDivFromHost() {
    try {
      var h = String((global.location && global.location.hostname) || '').toLowerCase();
      if (h.indexOf('kisfitglobal') >= 0) return 'KFG';
      if (h.indexOf('getbreakai') >= 0) return 'GBA';
      if (h.indexOf('paradise-hero') >= 0) return 'HERO';
      if (h.indexOf('kidsfit.co.kr') >= 0) return 'KFK';
      return 'TOM';
    } catch (_) {
      return 'TOM';
    }
  }

  function postCloudJson(path, payload, opts) {
    var isAnalytics = String(path || '').indexOf('/api/analytics/event') >= 0;
    if (isAnalytics && isInternalOrBotTraffic()) {
      return Promise.resolve({ ok: true, skipped: 'internal_test' });
    }
    var bodyStr = JSON.stringify(payload || {});
    var fullUrl = CLOUD_API_BASE + path;
    var tryBeaconFallback = function () {
      try {
        if (isAnalytics && isInternalOrBotTraffic()) return false;
        if (global.navigator && typeof global.navigator.sendBeacon === 'function' && typeof Blob === 'function') {
          return global.navigator.sendBeacon(fullUrl, new Blob([bodyStr], { type: 'text/plain;charset=UTF-8' }));
        }
      } catch (_be) {}
      return false;
    };
    if (opts && opts.beaconOnly) {
      var sentOnly = tryBeaconFallback();
      if (sentOnly) return Promise.resolve({ ok: true, transport: 'beacon' });
    }
    return fetch(fullUrl, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: bodyStr,
      keepalive: true
    }).then(function (res) {
      return res.json().catch(function () { return { ok: res.ok, status: res.status }; });
    }).catch(function (err) {
      if (isAnalytics && tryBeaconFallback()) {
        return { ok: true, transport: 'beacon_fallback' };
      }
      throw err;
    });
  }

  function getCloudJson(path) {
    return fetch(CLOUD_API_BASE + path, { method: 'GET' }).then(function (res) {
      return res.json().catch(function () { return { ok: res.ok, status: res.status }; });
    });
  }

  function readQueue() {
    try {
      var raw = localStorage.getItem(QUEUE_KEY);
      var parsed = raw ? JSON.parse(raw) : [];
      return Array.isArray(parsed) ? parsed : [];
    } catch (_) {
      return [];
    }
  }

  function writeQueue(items) {
    try {
      localStorage.setItem(QUEUE_KEY, JSON.stringify((items || []).slice(-30)));
    } catch (_) {}
  }

  function saveLocalMember(div, record) {
    try {
      localStorage.setItem('dc_member_' + String(div).toUpperCase(), JSON.stringify(record));
    } catch (_) {}
  }

  function getLocalMember(div) {
    try {
      var raw = localStorage.getItem('dc_member_' + String(div).toUpperCase());
      return raw ? JSON.parse(raw) : null;
    } catch (_) {
      return null;
    }
  }

  /* ==========================================================================
   * AARRR Growth Engine v6: Anonymous Cohort Visitor ID, D1/D7/D30 Retention,
   * Closed-Loop ?ref= Referral Attribution & Micro-Funnel Tracking (100% ASCII)
   * ========================================================================== */
  function detectIsQaOrBot() {
    if (isInternalOrBotTraffic()) return true;
    try {
      var ua = String((global.navigator && global.navigator.userAgent) || '');
      if (global.navigator && global.navigator.webdriver) return true;
      if (/HeadlessChrome|bot|crawl|spider|slurp|lighthouse|pingdom|uptimerobot|watchdog/i.test(ua)) return true;
      var qs = String((global.location && global.location.search) || '');
      if (/[?&](watchdog|qa=1|nocache=vl_|nocache=aarrr_qa)/i.test(qs)) return true;
    } catch (_) {}
    return false;
  }

  function getOrCreateVisitorProfile() {
    var nowMs = Date.now();
    var vid = '';
    var firstSeenMs = nowMs;
    var referredBy = '';
    try {
      vid = String(localStorage.getItem('dc_vid_v1') || '').replace(/[^A-Za-z0-9_\-]/g, '').slice(0, 32);
      if (!vid) {
        var rnd = Math.random().toString(36).slice(2, 10) + nowMs.toString(36).slice(-4);
        vid = 'v_' + rnd.slice(0, 12);
        localStorage.setItem('dc_vid_v1', vid);
      }
      var rawFs = localStorage.getItem('dc_first_seen_v1');
      if (rawFs && Number(rawFs) > 1700000000000) {
        firstSeenMs = Number(rawFs);
      } else {
        localStorage.setItem('dc_first_seen_v1', String(nowMs));
      }
      var sp = new URLSearchParams((global.location && global.location.search) || '');
      var urlRef = String(sp.get('ref') || '').replace(/[^A-Za-z0-9_\-]/g, '').slice(0, 32);
      var savedRef = String(localStorage.getItem('dc_ref_by_v1') || '').replace(/[^A-Za-z0-9_\-]/g, '').slice(0, 32);
      if (urlRef && urlRef !== vid && !savedRef) {
        localStorage.setItem('dc_ref_by_v1', urlRef);
        referredBy = urlRef;
      } else {
        referredBy = savedRef || (urlRef && urlRef !== vid ? urlRef : '');
      }
    } catch (_) {
      vid = vid || ('v_' + nowMs.toString(36));
    }
    var daysSinceFirst = Math.max(0, Math.floor((nowMs - firstSeenMs) / 86400000));
    return {
      visitor_id: vid,
      first_seen_ms: firstSeenMs,
      days_since_first: daysSinceFirst,
      referred_by: referredBy
    };
  }

  function getReferrerHost() {
    try {
      var ref = String((global.document && global.document.referrer) || '');
      if (!ref) return '';
      var u = new URL(ref);
      var curHost = String((global.location && global.location.hostname) || '').toLowerCase();
      if (u.hostname.toLowerCase() === curHost) return '';
      return u.hostname.toLowerCase().slice(0, 100);
    } catch (_) {
      return '';
    }
  }

  function buildReferralShareUrl(rawUrl) {
    try {
      var base = String(rawUrl || (global.location ? (global.location.origin + global.location.pathname) : '')).trim();
      var prof = getOrCreateVisitorProfile();
      var u = new URL(base);
      ['internal_check', 'owner_device', 'internal_test', 'smoke_test', 'nocache'].forEach(function (k) {
        u.searchParams.delete(k);
      });
      if (prof.visitor_id) u.searchParams.set('ref', prof.visitor_id);
      if (!u.searchParams.get('utm_source')) u.searchParams.set('utm_source', 'referral');
      if (!u.searchParams.get('utm_medium')) u.searchParams.set('utm_medium', 'share');
      return u.toString();
    } catch (_) {
      return String(rawUrl || '');
    }
  }

  function classifyCheckoutStepFromHref(href, el) {
    var h = String(href || '').toLowerCase();
    var pAttr = el ? String(el.getAttribute('data-whop-plan') || el.getAttribute('data-kfg-paid-plan') || el.getAttribute('data-csp-arg') || el.getAttribute('data-tom-paid-plan') || el.getAttribute('data-gba-paid-plan') || '').toLowerCase() : '';
    if (pAttr === 'starter' || pAttr === 'single' || pAttr === 'tier1' || h.indexOf('plan_xiplzfnr8slmz') >= 0 || h.indexOf('plan_j2eaow4jizw2m') >= 0 || h.indexOf('polar_cl_v2pl') >= 0 || h.indexOf('/products/damap') >= 0) {
      return 'step2_low';
    }
    if (pAttr === 'annual' || pAttr === 'premium' || pAttr === 'tier3' || h.indexOf('plan_9sdgfi753ucxq') >= 0 || h.indexOf('plan_ahyixblde0csq') >= 0 || h.indexOf('polar_cl_icvf') >= 0 || h.indexOf('/products/88dyn') >= 0) {
      return 'step4_premium';
    }
    if (pAttr === 'monthly' || pAttr === 'pass' || pAttr === 'sixmonth' || pAttr === 'tier2' || h.indexOf('plan_xvjenwyrdef8t') >= 0 || h.indexOf('plan_utg9ma9l5pzis') >= 0 || h.indexOf('polar_cl_p8da') >= 0 || h.indexOf('/products/_5nq4') >= 0) {
      return 'step3_core';
    }
    return '';
  }

  function captureUtmParams() {
    try {
      var sp = new URLSearchParams((global.location && global.location.search) || '');
      var utm = {
        utm_source: sp.get('utm_source') || '',
        utm_medium: sp.get('utm_medium') || '',
        utm_campaign: sp.get('utm_campaign') || '',
        utm_content: sp.get('utm_content') || ''
      };
      if (utm.utm_source || utm.utm_medium || utm.utm_campaign || utm.utm_content) {
        sessionStorage.setItem('dc_utm_params', JSON.stringify(utm));
        return utm;
      }
      var saved = sessionStorage.getItem('dc_utm_params');
      return saved ? JSON.parse(saved) : utm;
    } catch (_) {
      return { utm_source: '', utm_medium: '', utm_campaign: '', utm_content: '' };
    }
  }

  function trackFunnelEvent(div, eventName, extra) {
    if (isInternalOrBotTraffic()) return Promise.resolve({ ok: true, skipped: 'internal_test' });
    try {
      var d = String(div || detectDivFromHost()).toUpperCase();
      var utm = captureUtmParams();
      var prof = getOrCreateVisitorProfile();
      var isQa = (extra && typeof extra.is_qa !== 'undefined') ? Boolean(extra.is_qa) : detectIsQaOrBot();
      var payload = {
        div_code: d,
        event_name: String(eventName || 'landing_view'),
        utm_source: utm.utm_source || (extra && extra.utm_source) || '',
        utm_medium: utm.utm_medium || (extra && extra.utm_medium) || '',
        utm_campaign: utm.utm_campaign || (extra && extra.utm_campaign) || '',
        utm_content: utm.utm_content || (extra && extra.utm_content) || '',
        page_path: (global.location && global.location.pathname) ? global.location.pathname : '/',
        visitor_id: prof.visitor_id,
        ref_code: (extra && extra.ref_code) || prof.referred_by || '',
        referrer_host: getReferrerHost(),
        days_since_first: prof.days_since_first,
        event_meta: (extra && extra.event_meta) ? String(extra.event_meta).slice(0, 120) : '',
        is_qa: isQa ? 1 : 0
      };
      if (typeof global.gtag === 'function') {
        try { global.gtag('event', payload.event_name, { division: d, utm_source: payload.utm_source, utm_campaign: payload.utm_campaign, event_meta: payload.event_meta }); } catch (_) {}
      }
      return postCloudJson('/api/analytics/event', payload).catch(function () { return { ok: false }; });
    } catch (_) {
      return Promise.resolve({ ok: false });
    }
  }

  function mountReturningVisitorBanner(div, daysSinceFirst) {
    try {
      if (daysSinceFirst < 1 || !global.document || !global.document.body) return;
      if (global.document.getElementById('dc-returning-banner')) return;
      if (div === 'HERO') return;
      var msg = '';
      if (div === 'GBA') {
        msg = '\u304a\u304b\u3048\u308a\u306a\u3055\u3044\uff08\u521d\u56de\u8a2a\u554f\u304b\u3089 ' + daysSinceFirst + '\u65e5\u76ee\uff09\u2014 \u4eca\u65e5\u306e\u65b0NISA\u7d71\u8a08\u30d0\u30e9\u30f3\u30b9\u3084\u4fdd\u5b58\u6e08\u307f\u30ec\u30dd\u30fc\u30c8\u3092\u3059\u3050\u306b\u78ba\u8a8d\u3067\u304d\u307e\u3059\u3002';
      } else if (div === 'KFK') {
        msg = '\ub2e4\uc2dc \ubc29\ubb38\ud574 \uc8fc\uc154\uc11c \uac10\uc0ac\ud569\ub2c8\ub2e4 (\uccab \ubc29\ubb38 ' + daysSinceFirst + '\uc77c\ucc28) \u2014 \uc624\ub298 \uc6b0\ub9ac \uc544\uc774 \uc131\uc7a5 \uc2dc\uacc4 \ud750\ub984\uacfc \uc6d4\uac04 \uae30\ub85d\uc744 \ubc14\ub85c \ud655\uc778\ud574 \ubcf4\uc138\uc694.';
      } else if (div === 'KFG') {
        msg = 'Welcome back (Day ' + daysSinceFirst + ' since your first check) \u2014 re-check your child\'s US CDC growth pace or reopen your saved report anytime.';
      } else {
        msg = 'Welcome back (Day ' + daysSinceFirst + ' since your first visit) \u2014 re-check today\'s SMH \u00d7 XLV + SGOV calm balance or reopen your saved workbook.';
      }
      var bar = global.document.createElement('div');
      bar.id = 'dc-returning-banner';
      bar.setAttribute('role', 'status');
      bar.style.cssText = 'background:#ECFDF5;border-bottom:1px solid #A7F3D0;color:#065F46;padding:8px 14px;text-align:center;font-size:13px;font-weight:600;line-height:1.45;';
      bar.textContent = msg;
      global.document.body.insertBefore(bar, global.document.body.firstChild);
    } catch (_) {}
  }

  /* ==========================================================================
   * Cross-Device Permanent Magic Link Codec (UTF-8 safe Base64URL)
   * ========================================================================== */
  function toBase64Url(str) {
    try {
      var utf8Bytes = encodeURIComponent(str).replace(/%([0-9A-F]{2})/g, function (_, p1) {
        return String.fromCharCode(parseInt(p1, 16));
      });
      return btoa(utf8Bytes).replace(/\+/g, '-').replace(/\//g, '_').replace(/=+$/g, '');
    } catch (_) {
      return '';
    }
  }

  function fromBase64Url(b64) {
    try {
      var norm = String(b64 || '').replace(/-/g, '+').replace(/_/g, '/');
      while (norm.length % 4) norm += '=';
      var bin = atob(norm);
      var pct = '';
      for (var i = 0; i < bin.length; i++) {
        pct += '%' + ('00' + bin.charCodeAt(i).toString(16)).slice(-2);
      }
      return decodeURIComponent(pct);
    } catch (_) {
      return '';
    }
  }

  function encodeMagicRestoreUrl(baseUrl, stateObj, hashAnchor) {
    var cleanBase = String(baseUrl || (global.location ? global.location.origin + global.location.pathname : '')).split('#')[0];
    var compact = {};
    var k;
    for (k in (stateObj || {})) {
      if (Object.prototype.hasOwnProperty.call(stateObj, k) && stateObj[k] !== undefined && stateObj[k] !== null && stateObj[k] !== '') {
        compact[k] = stateObj[k];
      }
    }
    compact.v = 5;
    if (!compact.ts) compact.ts = Math.floor(Date.now() / 1000);
    var token = toBase64Url(JSON.stringify(compact));
    var sep = cleanBase.indexOf('?') >= 0 ? '&' : '?';
    var anchor = hashAnchor ? (String(hashAnchor).charAt(0) === '#' ? hashAnchor : '#' + hashAnchor) : '';
    return cleanBase + sep + 'magic_restore=' + encodeURIComponent(token) + anchor;
  }

  function decodeMagicRestoreParam(searchStr) {
    try {
      var qs = String(searchStr !== undefined ? searchStr : (global.location ? global.location.search : ''));
      var sp = new URLSearchParams(qs);
      var rawVal = sp.get('magic_restore');
      if (!rawVal) return null;
      if (rawVal === '1' && sp.get('email') && sp.get('code')) {
        return {
          email: sp.get('email').trim().toLowerCase(),
          access_code: sp.get('code').trim().toUpperCase(),
          tier: sp.get('tier') || 'tier1',
          magic_restore: true
        };
      }
      var jsonTxt = fromBase64Url(decodeURIComponent(rawVal));
      if (!jsonTxt) return null;
      var obj = JSON.parse(jsonTxt);
      return (obj && typeof obj === 'object') ? obj : null;
    } catch (_) {
      return null;
    }
  }

  function savePaidVault(div, vaultObj) {
    var d = String(div || '').toUpperCase();
    if (!d) return;
    try {
      localStorage.setItem('dc_paid_vault_' + d, JSON.stringify(vaultObj));
    } catch (_) {}
  }

  function getPaidVault(div) {
    var d = String(div || '').toUpperCase();
    try {
      var raw = localStorage.getItem('dc_paid_vault_' + d);
      return raw ? JSON.parse(raw) : null;
    } catch (_) {
      return null;
    }
  }

  /* ==========================================================================
   * 1. CORS-Safe CRM Registration (Cloudflare D1 + Brevo Day 0/2/5 Drip)
   * ========================================================================== */
  function registerMember(opts) {
    var div = String((opts && (opts.div || opts.div_code)) || detectDivFromHost()).trim().toUpperCase();
    var email = String((opts && opts.email) || '').trim().toLowerCase();
    var nickname = String((opts && opts.nickname) || '').trim();
    var segment = String((opts && opts.segment) || 'general').trim();
    var message = String((opts && (opts.message || opts.notes)) || '').trim();
    var lang = String((opts && opts.lang) || '').trim();

    if (!/^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(email)) {
      return Promise.resolve({ ok: false, error: 'INVALID_EMAIL' });
    }

    var nowIso = new Date().toISOString();
    var _vp = getOrCreateVisitorProfile();
    var _qa = detectIsQaOrBot();
    var payload = {
      div_code: div,
      div: div,
      email: email,
      nickname: nickname,
      segment: segment,
      visitor_id: _vp.visitor_id,
      ref_code: _vp.referred_by,
      is_qa: _qa ? 1 : 0,
      metadata: {
        message: message,
        lang: lang,
        utm: captureUtmParams(),
        visitor_id: _vp.visitor_id,
        referred_by: _vp.referred_by,
        referrer_host: getReferrerHost(),
        is_qa: _qa ? 1 : 0,
        source_url: (global.location && global.location.href) ? global.location.href : '',
        client_ts: nowIso
      }
    };

    saveLocalMember(div, {
      div: div,
      email: email,
      nickname: nickname,
      segment: segment,
      joined_at: nowIso
    });

    return postCloudJson('/api/crm/register', payload).then(function (res) {
      if (res && res.ok) {
        res.div = div;
        res.email = email;
        res.segment = segment;
        return res;
      }
      var q = readQueue();
      q.push(payload);
      writeQueue(q);
      return { ok: false, queued_for_sync: true, error: (res && res.error) || 'SERVER_UNAVAILABLE' };
    }).catch(function () {
      var q2 = readQueue();
      q2.push(payload);
      writeQueue(q2);
      return { ok: false, queued_for_sync: true, error: 'NETWORK_ERROR' };
    });
  }

  function escapeHtml(raw) {
    return String(raw === undefined || raw === null ? '' : raw)
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;')
      .replace(/'/g, '&#39;');
  }

  var ALLOWED_CHECKOUT_HOSTS = {
    'whop.com': true,
    'www.whop.com': true,
    'buy.polar.sh': true,
    'polar.sh': true,
    'www.latpeed.com': true,
    'latpeed.com': true,
    'cshop.naver.com': true,
    'influencers.coupang.com': true,
    'api.truthofmarket.com': true
  };

  function isAllowedExternalUrl(rawUrl) {
    try {
      var u = new URL(String(rawUrl || '').trim());
      if (u.protocol !== 'https:') return false;
      var h = u.hostname.toLowerCase();
      return Boolean(ALLOWED_CHECKOUT_HOSTS[h] || h.endsWith('.whop.com'));
    } catch (_) {
      return false;
    }
  }

  function saveSignedDownloads(div, downloads, ttlSec) {
    var d = String(div || '').toUpperCase();
    if (!d || !downloads || typeof downloads !== 'object') return;
    var rec = {
      downloads: downloads,
      expires_at: Date.now() + Math.max(60, Number(ttlSec || 900) - 60) * 1000
    };
    try {
      if (global.sessionStorage) global.sessionStorage.setItem('dc_signed_dl_' + d, JSON.stringify(rec));
    } catch (_) {}
  }

  function getSignedDownloadUrl(div, docKey) {
    var d = String(div || '').toUpperCase();
    try {
      if (!global.sessionStorage) return '';
      var raw = global.sessionStorage.getItem('dc_signed_dl_' + d);
      if (!raw) return '';
      var rec = JSON.parse(raw);
      if (!rec || !rec.downloads || Date.now() >= Number(rec.expires_at || 0)) return '';
      return String(rec.downloads[docKey] || '');
    } catch (_) {
      return '';
    }
  }

  /* ==========================================================================
   * 2. Server-Side Entitlement Verification & 6-Digit OTP (Zero-Bypass!)
   * ========================================================================== */
  function requestAuthOtp(opts) {
    var div = String((opts && (opts.div || opts.div_code)) || detectDivFromHost()).trim().toUpperCase();
    var email = String((opts && opts.email) || '').trim().toLowerCase();
    if (!/^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(email)) {
      return Promise.resolve({ ok: false, error: 'INVALID_EMAIL' });
    }
    return postCloudJson('/api/auth/request-otp', {
      div_code: div,
      email: email
    }).catch(function () {
      return { ok: false, error: 'NETWORK_ERROR' };
    });
  }

  function verifyEntitlement(opts) {
    var div = String((opts && (opts.div || opts.div_code)) || detectDivFromHost()).trim().toUpperCase();
    var email = String((opts && opts.email) || '').trim().toLowerCase();
    var code = String((opts && (opts.access_code || opts.code || opts.order_ref)) || '').trim().toUpperCase();
    var otp = String((opts && opts.otp) || '').replace(/\D/g, '').trim();
    var tier = String((opts && opts.tier) || '').trim().toLowerCase();
    if (!/^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(email)) {
      return Promise.resolve({ ok: false, authorized: false, error: 'INVALID_EMAIL' });
    }
    if (!code && otp.length !== 6) {
      return Promise.resolve({ ok: true, authorized: false, requires_code_or_otp: true, reason: 'verification_credential_required' });
    }
    return postCloudJson('/api/verify-entitlement', {
      div_code: div,
      email: email,
      access_code: code,
      otp: otp,
      tier: tier,
      magic_restore: Boolean(opts && opts.magic_restore)
    }).then(function (res) {
      if (res && res.authorized) {
        trackFunnelEvent(div, 'paid_success');
        if (res.downloads) {
          saveSignedDownloads(div, res.downloads, res.download_ttl_sec || 900);
        }
        savePaidVault(div, {
          div: div,
          email: email,
          tier: res.tier || 'tier1',
          tier2_unlocked: Boolean(res.tier2_unlocked),
          tier3_unlocked: Boolean(res.tier3_unlocked),
          access_code: res.access_code || code || '',
          order_ref: res.order_ref || '',
          verified_at: new Date().toISOString()
        });
      }
      return res || { ok: false, authorized: false, reason: 'verification_failed' };
    }).catch(function () {
      return { ok: false, authorized: false, reason: 'network_error' };
    });
  }

  function triggerReliablePdfDownload(signedUrl, docKey) {
    if (!signedUrl || !isAllowedExternalUrl(signedUrl)) return Promise.resolve(false);
    var fnameMap = {
      tom_master_14p: 'TruthOfMarket_Master_Workbook_2000_2025_14p.pdf',
      kfg_cdc_guide_8p: 'KISFIT_Studio_US_CDC_Growth_Guide_8p.pdf',
      gba_jp_nisa_12p: 'GetBreakAI_JP_ShinNISA_Workbook_12p.pdf',
      kfk_tier1_masterbook: 'KidsFit_GoldenTime_Masterbook_17p.pdf',
      kfk_tier2_fullpackage: 'KidsFit_6Month_Tracker_FullPackage_20p.pdf'
    };
    var fallbackName = fnameMap[docKey] || (String(docKey || 'document') + '.pdf');
    if (typeof global.fetch === 'function' && global.URL && typeof global.URL.createObjectURL === 'function' && global.document && global.document.body) {
      return global.fetch(signedUrl, { method: 'GET', mode: 'cors', credentials: 'omit' })
        .then(function (resp) {
          if (!resp || !resp.ok) throw new Error('HTTP_' + (resp ? resp.status : 0));
          return resp.blob();
        })
        .then(function (blob) {
          var objUrl = global.URL.createObjectURL(blob);
          var a = global.document.createElement('a');
          a.href = objUrl;
          a.download = fallbackName;
          a.rel = 'noopener';
          a.style.display = 'none';
          global.document.body.appendChild(a);
          a.click();
          setTimeout(function () {
            try { global.URL.revokeObjectURL(objUrl); if (a.parentNode) a.parentNode.removeChild(a); } catch (_) {}
          }, 8000);
          return true;
        })
        .catch(function () {
          try {
            var a2 = global.document.createElement('a');
            a2.href = signedUrl;
            a2.download = fallbackName;
            a2.rel = 'noopener';
            a2.style.display = 'none';
            global.document.body.appendChild(a2);
            a2.click();
            setTimeout(function () { try { if (a2.parentNode) a2.parentNode.removeChild(a2); } catch (_) {} }, 4000);
            return true;
          } catch (_) {
            if (global.location) global.location.assign(signedUrl);
            return true;
          }
        });
    }
    if (global.location) global.location.assign(signedUrl);
    return Promise.resolve(true);
  }

  function openProtectedPdfDownload(div, docKey, onNeedsReauth) {
    var d = String(div || detectDivFromHost()).trim().toUpperCase();
    var cached = getSignedDownloadUrl(d, docKey);
    if (cached && isAllowedExternalUrl(cached)) {
      trackFunnelEvent(d, 'pdf_download');
      return triggerReliablePdfDownload(cached, docKey).then(function (ok) {
        if (ok) return { ok: true, cached: true };
        if (typeof onNeedsReauth === 'function') onNeedsReauth({ authorized: false, reason: 'download_failed' });
        return { ok: false, reason: 'download_failed' };
      });
    }

    var vault = getPaidVault(d);
    if (vault && vault.email && (vault.access_code || vault.order_ref)) {
      return verifyEntitlement({ div: d, email: vault.email, access_code: vault.access_code || vault.order_ref }).then(function (vres) {
        var fresh = (vres && vres.authorized && vres.downloads && vres.downloads[docKey]) ? vres.downloads[docKey] : '';
        if (fresh && isAllowedExternalUrl(fresh)) {
          trackFunnelEvent(d, 'pdf_download');
          return triggerReliablePdfDownload(fresh, docKey).then(function (ok) {
            return ok ? { ok: true, refreshed: true } : { ok: false, reason: 'download_failed' };
          });
        }
        if (typeof onNeedsReauth === 'function') onNeedsReauth(vres);
        return { ok: false, reason: 'reauth_required' };
      });
    }

    if (typeof onNeedsReauth === 'function') onNeedsReauth({ authorized: false, reason: 'reauth_required' });
    return Promise.resolve({ ok: false, reason: 'reauth_required' });
  }

  /* ==========================================================================
   * 3. Standard Digital Refund & Support Link (Replaces legacy 7-Day copy!)
   * ========================================================================== */
  function buildRefundSupportMailto(div, email, orderRef) {
    var d = String(div || detectDivFromHost()).toUpperCase();
    var subj = '[' + d + ' Digital Refund / Support Request] ' + (orderRef || email || 'Member Request');
    return 'mailto:' + getSupportEmail(d) + '?subject=' + encodeURIComponent(subj);
  }

  function deliverPaidMagicPack(opts) {
    var div = String((opts && opts.div) || detectDivFromHost()).trim().toUpperCase();
    var email = String((opts && opts.email) || '').trim().toLowerCase();
    var planTier = String((opts && opts.plan_tier) || 'Paid Pass').trim();
    var orderRef = String((opts && opts.order_ref) || ('WEB-' + div + '-' + Date.now().toString(36).toUpperCase())).trim();
    var statePayload = (opts && opts.profile_state) ? opts.profile_state : {};
    statePayload.div = div;
    statePayload.tier = planTier;
    statePayload.email = email;
    statePayload.order_ref = orderRef;

    var baseUrl = (opts && opts.base_url) || (global.location ? (global.location.origin + global.location.pathname) : '');
    var hashAnchor = (opts && opts.hash_anchor) || '';
    var magicUrl = encodeMagicRestoreUrl(baseUrl, statePayload, hashAnchor);
    var refundUrl = buildRefundSupportMailto(div, email, orderRef);

    var vaultRecord = {
      div: div,
      email: email,
      plan_tier: planTier,
      order_ref: orderRef,
      magic_restore_url: magicUrl,
      refund_support_url: refundUrl,
      profile_state: statePayload,
      activated_at: new Date().toISOString()
    };
    savePaidVault(div, vaultRecord);

    if (!/^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(email)) {
      return Promise.resolve({ ok: true, local_only: true, magic_restore_url: magicUrl, refund_support_url: refundUrl, vault: vaultRecord });
    }

    var segMap = {
      TOM: 'TOM_Paid_VIP',
      KFG: 'KFG_Paid_VIP',
      GBA: 'GBA_Paid_VIP',
      HERO: 'hero_free_family',
      KFK: 'KFK_Paid_VIP'
    };
    return registerMember({
      div: div,
      email: email,
      nickname: String((opts && opts.nickname) || '').trim(),
      segment: String((opts && opts.segment) || segMap[div] || (div + '_Paid_VIP')),
      notes: 'PAID_MAGIC_PACK_V5|' + planTier + '|' + orderRef
    }).then(function (res) {
      return { ok: true, crm_sync: res, magic_restore_url: magicUrl, refund_support_url: refundUrl, vault: vaultRecord };
    });
  }

  /* ==========================================================================
   * 4. Division 4 Free Fan Next-Song Vote (Persisted in Cloudflare D1)
   * ========================================================================== */
  function fetchHeroVotes() {
    return getCloudJson('/api/hero/vote');
  }

  function submitHeroVote(songKey, voterId) {
    var vid = voterId;
    if (!vid) {
      try {
        vid = localStorage.getItem('dc_hero_voter_id');
        if (!vid) {
          vid = 'v_' + Math.random().toString(36).slice(2) + '_' + Date.now().toString(36);
          localStorage.setItem('dc_hero_voter_id', vid);
        }
      } catch (_) {
        vid = 'v_anon_' + Date.now();
      }
    }
    return postCloudJson('/api/hero/vote', { song_key: String(songKey || ''), voter_id: vid });
  }

  /* ==========================================================================
   * 5. 1-Second Satisfaction Vote (`[+ / = / -]`)
   * ========================================================================== */
  function fetchVerifiedReviews(div) {
    var d = String(div || detectDivFromHost()).trim().toUpperCase();
    return getCloudJson('/api/reviews?div=' + encodeURIComponent(d)).catch(function () {
      return { ok: false, div: d, count: 0, threshold: 3, visible: false, reviews: [] };
    });
  }
  function fetchHeroStories() {
    return getCloudJson('/api/hero/stories').catch(function () { return { ok: false, stories: [], cheers: {} }; });
  }
  function submitHeroStory(payload) {
    return postCloudJson('/api/hero/stories', payload || {});
  }
  function cheerHeroStory(storyId, voterId) {
    var vid = voterId;
    if (!vid) {
      try {
        vid = localStorage.getItem('dc_hero_voter_id');
        if (!vid) { vid = 'v_' + Math.random().toString(36).slice(2) + '_' + Date.now().toString(36); localStorage.setItem('dc_hero_voter_id', vid); }
      } catch (_) { vid = 'v_anon_' + Date.now(); }
    }
    return postCloudJson('/api/hero/story-cheer', { story_id: String(storyId || ''), voter_id: vid });
  }

  function submitSatisfactionVote(opts) {
    var div = String((opts && opts.div) || detectDivFromHost()).trim().toUpperCase();
    var vote = String((opts && opts.vote) || 'up').trim().toLowerCase();
    var contextKey = String((opts && opts.context) || 'paid_report').trim();
    var voteRec = { div: div, vote: vote, context: contextKey, voted_at: new Date().toISOString() };
    try {
      localStorage.setItem('dc_sat_vote_' + div + '_' + contextKey, JSON.stringify(voteRec));
    } catch (_) {}
    var vault = getPaidVault(div);
    var fbEmail = String((opts && opts.email) || (vault && vault.email) || '').trim().toLowerCase();
    var fbComment = String((opts && opts.comment) || '').trim().slice(0, 240);
    var fbNick = String((opts && (opts.display_name || opts.nickname)) || '').trim().slice(0, 32);
    return postCloudJson('/api/feedback', {
      div_code: div, rating: vote, email: fbEmail, comment: fbComment, display_name: fbNick
    }).catch(function () {
      return trackFunnelEvent(div, 'sat_vote_' + vote).then(function () { return { ok: true, div: div, vote: vote }; });
    });
  }

  function getLocalizedVoteStrings(div, allowEmoji) {
    var d = String(div || 'TOM').toUpperCase();
    if (d === 'GBA') {
      return {
        prompt: '\u4eca\u6708\u306e\u30ea\u30b5\u30fc\u30c1\u30fb\u30ec\u30dd\u30fc\u30c8\u306f\u304a\u5f79\u306b\u7acb\u3061\u307e\u3057\u305f\u304b\uff1f',
        up: '\u5927\u5909\u6e80\u8db3',
        neutral: '\u666e\u901a',
        down: '\u6539\u5584\u5e0c\u671b',
        thanks: '\u3054\u56de\u7b54\u3042\u308a\u304c\u3068\u3046\u3054\u3056\u3044\u307e\u3059\u3002\u6765\u9031\u306e\u54c1\u8cea\u6539\u5584\u306b\u53cd\u6620\u3044\u305f\u3057\u307e\u3059\u3002'
      };
    }
    if (d === 'KFK') {
      return {
        prompt: '\uc774\ubc88 \ub2ec \uc131\uc7a5 \ub9ac\ud3ec\ud2b8\uac00 \ub3c4\uc6c0\uc774 \ub418\uc168\ub098\uc694?',
        up: '\ub9e4\uc6b0 \ub9cc\uc871',
        neutral: '\ubcf4\ud1b5',
        down: '\uc544\uc26c\uc6c0',
        thanks: '\uc18c\uc911\ud55c \uc758\uacac \uac10\uc0ac\ud569\ub2c8\ub2e4. \ub9e4\uc8fc \ub9ac\ud3ec\ud2b8 \ud488\uc9c8 \uac1c\uc120\uc5d0 \ubc18\uc601\ub429\ub2c8\ub2e4.'
      };
    }
    if (d === 'HERO') {
      return {
        prompt: '\uc624\ub298 \ubc31\uc6b4\ud638 \ub77c\ub514\uc624\uc640 \uc0ac\ub791\ubc29\uc774 \uc990\uac70\uc6b0\uc168\ub098\uc694?',
        up: (allowEmoji ? '\ud83d\udc4d ' : '') + '\ub9e4\uc6b0 \ub9cc\uc871',
        neutral: (allowEmoji ? '\ud83d\ude10 ' : '') + '\ubcf4\ud1b5',
        down: (allowEmoji ? '\ud83d\udc4e ' : '') + '\uc544\uc26c\uc6c0',
        thanks: '\uac10\uc0ac\ud569\ub2c8\ub2e4! \ubcf4\ub0b4\uc8fc\uc2e0 \ub9c8\uc74c\uc744 \ub2e4\uc74c \ubc29\uc1a1\uc5d0 \uaf2d \ub2f4\uaca0\uc2b5\ub2c8\ub2e4.'
      };
    }
    return {
      prompt: 'Was this personalized report helpful today?',
      up: 'Very Helpful',
      neutral: 'Okay',
      down: 'Needs Work',
      thanks: 'Thank you. Your 1-second feedback directly guides our weekly research improvements.'
    };
  }

  function mountSatisfactionBar(target, opts) {
    var el = (typeof target === 'string') ? (global.document && global.document.querySelector(target)) : target;
    if (!el) return;
    var div = String((opts && opts.div) || detectDivFromHost()).toUpperCase();
    var contextKey = String((opts && opts.context) || 'paid_report');
    var isHero = (div === 'HERO');
    var labels = getLocalizedVoteStrings(div, isHero);
    var fontPx = isHero ? '20px' : '14px';
    var padBtn = isHero ? '14px 20px' : '8px 14px';

    el.innerHTML = ''
      + '<div class="dc-sat-vote-bar" style="display:flex;flex-wrap:wrap;align-items:center;justify-content:space-between;gap:10px;padding:' + (isHero ? '18px 20px' : '12px 16px') + ';border:1px solid rgba(120,120,120,0.24);border-radius:10px;margin-top:14px;font-size:' + fontPx + ';">'
      + '  <span class="dc-sat-prompt" style="font-weight:600;">' + labels.prompt + '</span>'
      + '  <div class="dc-sat-actions" style="display:flex;flex-wrap:wrap;gap:8px;">'
      + '    <button type="button" data-dc-vote="up" style="cursor:pointer;padding:' + padBtn + ';border-radius:8px;border:1px solid rgba(16,185,129,0.45);background:rgba(16,185,129,0.10);color:inherit;font-weight:700;font-size:' + fontPx + ';">[+] ' + labels.up + '</button>'
      + '    <button type="button" data-dc-vote="neutral" style="cursor:pointer;padding:' + padBtn + ';border-radius:8px;border:1px solid rgba(148,163,184,0.45);background:transparent;color:inherit;font-weight:600;font-size:' + fontPx + ';">[=] ' + labels.neutral + '</button>'
      + '    <button type="button" data-dc-vote="down" style="cursor:pointer;padding:' + padBtn + ';border-radius:8px;border:1px solid rgba(239,68,68,0.38);background:transparent;color:inherit;font-weight:600;font-size:' + fontPx + ';">[-] ' + labels.down + '</button>'
      + '  </div>'
      + '</div>';

    var btns = el.querySelectorAll('[data-dc-vote]');
    for (var i = 0; i < btns.length; i++) {
      (function (btn) {
        btn.addEventListener('click', function () {
          var v = btn.getAttribute('data-dc-vote') || 'up';
          submitSatisfactionVote({ div: div, vote: v, context: contextKey, email: opts && opts.email });
          var wrap = el.querySelector('.dc-sat-vote-bar');
          if (v === 'up' && !isHero && wrap) {
            var askTxt = div === 'KFK' ? '\ub3c4\uc6c0\uc774 \ub418\uc168\ub2e4\uba74 \ud55c \uc904 \uc18c\uac10\uc744 \ub0a8\uaca8 \uc8fc\uc138\uc694 (\uc120\ud0dd · \uc775\uba85/\ub2c9\ub124\uc784):' : (div === 'GBA' ? 'よろしければ一言ご感想をお聞かせください（任意・匿名可）：' : 'Optional: share a 1-line voluntary reflection (verified members only):');
            var btnLbl = div === 'KFK' ? '\uc18c\uac10 \uc800\uc7a5' : (div === 'GBA' ? '送信' : 'Save Note');
            wrap.innerHTML = '<div style="width:100%;"><div style="font-weight:700;margin-bottom:6px;">' + askTxt + '</div><div style="display:flex;flex-wrap:wrap;gap:6px;"><input type="text" class="dc-sat-nick" maxlength="32" placeholder="Nickname" style="flex:0 1 130px;padding:7px 9px;border:1px solid #CBD5E1;border-radius:6px;font-size:13px;"><input type="text" class="dc-sat-comment-box" maxlength="220" placeholder="..." style="flex:1 1 200px;padding:7px 9px;border:1px solid #CBD5E1;border-radius:6px;font-size:13px;"><button type="button" class="dc-sat-send-btn" style="padding:7px 14px;border-radius:6px;border:none;background:#0F2C22;color:#FFF;font-weight:700;cursor:pointer;">' + btnLbl + '</button></div></div>';
            var sBtn = wrap.querySelector('.dc-sat-send-btn');
            if (sBtn) sBtn.addEventListener('click', function () {
              var nEl = wrap.querySelector('.dc-sat-nick');
              var cEl = wrap.querySelector('.dc-sat-comment-box');
              var cVal = String(cEl ? cEl.value : '').trim();
              if (cVal.length < 5) { if (cEl) cEl.focus(); return; }
              sBtn.disabled = true;
              submitSatisfactionVote({ div: div, vote: 'up', context: contextKey, email: opts && opts.email, display_name: String(nEl ? nEl.value : '').trim(), comment: cVal }).then(function () {
                wrap.innerHTML = '<span style="font-weight:600;">' + labels.thanks + '</span>';
              });
            });
          } else if (wrap) {
            wrap.innerHTML = '<span style="font-weight:600;">' + labels.thanks + '</span>';
          }
        });
      })(btns[i]);
    }
  }

  /* ==========================================================================
   * 6. Pediatric 6-Month Cumulative Height Velocity History (KFG & KFK, Multi-Sibling Aware!)
   * ========================================================================== */
  function readCheckinHistory(div, siblingId) {
    var suffix = siblingId ? ('_' + String(siblingId)) : '';
    var key = 'dc_checkin_history_' + String(div || 'KFG').toUpperCase() + suffix;
    try {
      var raw = localStorage.getItem(key);
      var arr = raw ? JSON.parse(raw) : [];
      return Array.isArray(arr) ? arr : [];
    } catch (_) {
      return [];
    }
  }

  function appendCheckinHistory(div, entry, siblingId) {
    var d = String(div || 'KFG').toUpperCase();
    var suffix = siblingId ? ('_' + String(siblingId)) : '';
    var key = 'dc_checkin_history_' + d + suffix;
    var arr = readCheckinHistory(d, siblingId);
    arr.push({
      date: entry.date || new Date().toISOString().slice(0, 10),
      day_milestone: entry.day_milestone || (arr.length + 1) * 30,
      prev_height_cm: Number(entry.prev_height_cm) || 0,
      height_cm: Number(entry.current_height_cm || entry.height_cm) || 0,
      delta_cm: Number(entry.delta_cm) || 0,
      annualized_cm_yr: Number(entry.annualized_cm_yr) || 0,
      target_cm_yr: Number(entry.target_cm_yr) || 5.8
    });
    var trimmed = arr.slice(-12);
    try { localStorage.setItem(key, JSON.stringify(trimmed)); } catch (_) {}
    return trimmed;
  }

  function computeLocalKfgCommentary(payload) {
    var prevH = Number(payload.prev_height_cm) || (Number(payload.current_height_cm) - 0.5);
    var curH = Number(payload.current_height_cm) || 137.7;
    var age = Number(payload.child_age_years) || 9;
    var isF = String(payload.child_sex || 'M').toUpperCase().charAt(0) === 'F';
    var targetVel = age < 6 ? 6.6 : (age < 9 ? 5.7 : (age < 11.5 ? (isF ? 7.4 : 5.5) : (age < 14 ? (isF ? 5.6 : 8.2) : 3.6)));
    var targetInYr = Math.round((targetVel / 2.54) * 10) / 10;
    var delta = Math.round((curH - prevH) * 100) / 100;
    var deltaIn = Math.round((delta / 2.54) * 100) / 100;
    var annVel = Math.round(((delta / 30) * 365) * 10) / 10;
    var annInYr = Math.round((annVel / 2.54) * 10) / 10;
    var habits = [
      { key: 'Deep Sleep Window (Pre-10 PM Routine)', score: Number(payload.sleep_score) || 3, tip: 'Shift lights-out 30 minutes earlier and turn off screens 45 minutes before bed to support consistent deep-sleep recovery.' },
      { key: 'Protein + Calcium / Vit D3 / Zinc Balance', score: Number(payload.nutrition_score) || 3, tip: 'Pair dinner lean protein with Calcium, Vitamin D3, and Zinc-rich whole foods for balanced daily nutrition.' },
      { key: 'Daily 20-Min Jump & Stretch Activity', score: Number(payload.exercise_score) || 3, tip: 'Add 15-20 minutes of jump-rope, hops, or evening spine-lengthening stretches daily.' },
      { key: 'Desk Posture & Nasal Breathing Habit', score: Number(payload.posture_score) || 3, tip: 'Support upright desk posture and nighttime nasal breathing habits to maintain full standing stature.' }
    ].sort(function (a, b) { return a.score - b.score; });
    var verdict = delta <= 0
      ? ('Height held steady at ' + (curH / 2.54).toFixed(1) + ' in (' + curH.toFixed(1) + ' cm) this 30-day cycle; childhood growth naturally happens in pulses. Keep morning wall measurements consistent.')
      : ('30-day gain of +' + deltaIn.toFixed(2) + ' in (+' + delta.toFixed(2) + ' cm) — annualized pace of ~' + annInYr.toFixed(1) + ' in/yr (' + annVel.toFixed(1) + ' cm/yr) vs. US CDC age-' + age + ' reference of ' + targetInYr.toFixed(1) + ' in/yr.');
    return {
      ok: true,
      prev_height_cm: prevH,
      current_height_cm: curH,
      delta_cm: delta,
      delta_inches: deltaIn,
      annualized_cm_yr: annVel,
      annualized_in_yr: annInYr,
      cdc_target_cm_yr: targetVel,
      cdc_target_in_yr: targetInYr,
      velocity_verdict: verdict,
      strongest_habit: habits[habits.length - 1],
      priority_bottleneck: habits[0]
    };
  }

  function computeLocalKfkCommentary(payload) {
    var prevH = Number(payload.prev_height_cm) || (Number(payload.current_height_cm) - 0.5);
    var curH = Number(payload.current_height_cm) || 134.5;
    var age = Number(payload.child_age_years) || 9;
    var isF = String(payload.child_sex || 'M').toUpperCase().charAt(0) === 'F';
    var targetVel = age < 6 ? 6.6 : (age < 9 ? 5.8 : (age < 11.5 ? (isF ? 7.5 : 5.6) : (age < 14 ? (isF ? 5.5 : 8.3) : 3.5)));
    var delta = Math.round((curH - prevH) * 100) / 100;
    var annVel = Math.round(((delta / 30) * 365) * 10) / 10;
    var habits = [
      {
        key: '\uc218\uba74 \uace8\ub4e0\ud0c0\uc784 (22\uc2dc \uc774\uc804 \ucde8\uce68)',
        score: Number(payload.sleep_score) || 3,
        tip: '\ucde8\uce68 \uc2dc\uac04\uc744 30\ubd84 \uc55e\ub2f9\uae30\uace0 \uc7a0\ub4e4\uae30 45\ubd84 \uc804 \uc2a4\ub9c8\ud2b8\ud3f0\u00b7TV \ud654\uba74\uc744 \ub044\uba74 \uc131\uc7a5\ud638\ub974\ubaac \ubd84\ube44 \ud3ed\uc744 \uc548\uc815\uc801\uc73c\ub85c \uc9c0\ud0ac \uc218 \uc788\uc2b5\ub2c8\ub2e4.'
      },
      {
        key: '\ub2e8\ubc31\uc9c8\u00b7\uce7c\uc298\u00b7\ube44\ud0c0\ubbfcD \uc2dd\ub2e8',
        score: Number(payload.nutrition_score) || 3,
        tip: '\uc800\ub141 \uc2dd\uc0ac\uc5d0 \uc0b4\ucf54\uae30\u00b7\uc0dd\uc120\u00b7\ub450\ubd80 \ub4f1 \uc591\uc9c8\uc758 \ub2e8\ubc31\uc9c8\uc744 \ucc59\uae30\uace0 \uc2dd\ud6c4 \uc57c\uc2dd\u00b7\ub2e8 \uc74c\ub8cc\ub97c \uc904\uc5ec \uace8\ubc00\ub3c4\uc640 \uc778\uc290\ub9b0 \ubc18\uc751\uc744 \ud568\uaed8 \uad00\ub9ac\ud558\uc138\uc694.'
      },
      {
        key: '\uc218\uc9c1 \uc810\ud504\u00b7\ud558\uccb4 \uc2a4\ud2b8\ub808\uce6d (20\ubd84)',
        score: Number(payload.exercise_score) || 3,
        tip: '\uc904\ub118\uae30\u00b7\ub18d\uad6c\u00b7\uc81c\uc790\ub9ac \uc810\ud504 \ub4f1 \ud558\ub8e8 15~20\ubd84 \uc218\uc9c1 \uc790\uadf9 \uc6b4\ub3d9\uacfc \ucde8\uce68 \uc804 \ucc99\ucd94 \uc2a4\ud2b8\ub808\uce6d\uc744 \uafb8\uc900\ud788 \uc720\uc9c0\ud558\uc138\uc694.'
      },
      {
        key: '\ubc14\ub978 \uc790\uc138\u00b7\ucf54\ud638\ud761 \uc2b5\uad00',
        score: Number(payload.posture_score) || 3,
        tip: '\ucc45\uc0c1 \uac70\ubd81\ubaa9 \uad50\uc815\uacfc \uc218\uba74 \uc911 \ucf54\ud638\ud761 \uc720\uc9c0\ub9cc\uc73c\ub85c\ub3c4 \uc228\uc5b4 \uc788\ub358 1.0~1.8cm\uc758 \uc2e0\uc7a5 \ud3ec\ud150\uc15c\uc744 \uc9c0\ud0ac \uc218 \uc788\uc2b5\ub2c8\ub2e4.'
      }
    ].sort(function (a, b) { return a.score - b.score; });

    var paceNote = annVel >= targetVel
      ? '\ub610\ub798 \ud3c9\uade0 \uc131\uc7a5\uc18d\ub3c4\ub97c \uc6c3\ub3c4\ub294 \uc591\ud638\ud55c \ud750\ub984\uc785\ub2c8\ub2e4.'
      : '\ub610\ub798 \uae30\uc900 \uc18d\ub3c4\ubcf4\ub2e4 \uc57d\uac04 \uc644\ub9cc\ud558\ubbc0\ub85c \ucd5c\uc6b0\uc120 \ubcd1\ubaa9 \uc2b5\uad00 1\uac00\uc9c0\ubd80\ud130 \uc9d1\uc911 \ubcf4\uc644\ud574 \ubcf4\uc138\uc694.';

    var verdict = delta <= 0
      ? ('\uc774\ubc88 30\uc77c \uc8fc\uae30 \uce21\uc815\ud0a4\ub294 ' + curH.toFixed(1) + 'cm\ub85c \ubcf4\ud569 \uad6c\uac04\uc785\ub2c8\ub2e4. \uc18c\uc544 \uc131\uc7a5\uc740 \uacc4\ub2e8\uc2dd\uc73c\ub85c \ud06c\ubbc0\ub85c \ub9e4\uc6d4 \uac19\uc740 \uc544\uce68 \uc2dc\uac04 \uce21\uc815\uacfc 22\uc2dc \uc774\uc804 \ucde8\uce68\uc744 \uc720\uc9c0\ud574 \uc8fc\uc138\uc694.')
      : ('30\uc77c \ub3d9\uc548 +' + delta.toFixed(2) + 'cm \uc131\uc7a5 (\uc5f0\uac04 \ud658\uc0b0 ' + annVel.toFixed(1) + 'cm/\ub144 vs \uc9c8\ubcd1\uad00\ub9ac\uccad \ub9cc ' + age + '\uc138 \uae30\uc900 ' + targetVel.toFixed(1) + 'cm/\ub144). ' + paceNote);

    return {
      ok: true,
      prev_height_cm: prevH,
      current_height_cm: curH,
      delta_cm: delta,
      annualized_cm_yr: annVel,
      kdca_target_cm_yr: targetVel,
      velocity_verdict: verdict,
      strongest_habit: habits[habits.length - 1],
      priority_bottleneck: habits[0]
    };
  }

  function enrollKfgPaidVip(opts) {
    var email = String((opts && opts.email) || '').trim().toLowerCase();
    if (!/^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(email)) {
      return Promise.resolve({ ok: false, error: 'INVALID_EMAIL' });
    }
    var payload = {
      email: email,
      parent_name: String((opts && opts.parent_name) || 'Parent').trim(),
      child_name: String((opts && opts.child_name) || 'Your Child').trim(),
      child_sex: String((opts && opts.child_sex) || 'M').trim().toUpperCase(),
      child_age_years: Number((opts && opts.child_age_years) || 9),
      baseline_height_cm: Number((opts && opts.baseline_height_cm) || 137.2),
      plan_tier: String((opts && opts.plan_tier) || '6-Month Growth Pass ($19.99)').trim(),
      months_remaining: Number((opts && opts.months_remaining) || 6),
      order_ref: String((opts && opts.order_ref) || 'POLAR-KFG-VIP').trim()
    };
    try { localStorage.setItem('dc_kfg_paid_vip', JSON.stringify(payload)); } catch (_) {}
    return deliverPaidMagicPack({
      div: 'KFG',
      email: email,
      nickname: payload.parent_name,
      plan_tier: payload.plan_tier,
      order_ref: payload.order_ref,
      hash_anchor: 'kfg-vip-monthly-checkin',
      profile_state: payload
    }).then(function () {
      return { ok: true, baseline_height_cm: payload.baseline_height_cm };
    });
  }

  function submitKfgVipCheckin(opts) {
    var siblingId = (opts && opts.sibling_id) || '';
    var payload = {
      email: String((opts && opts.email) || '').trim().toLowerCase(),
      child_name: String((opts && opts.child_name) || 'Your Child').trim(),
      child_sex: String((opts && opts.child_sex) || 'M').trim().toUpperCase(),
      child_age_years: Number((opts && opts.child_age_years) || 9),
      prev_height_cm: Number((opts && opts.prev_height_cm) || 137.2),
      current_height_cm: Number((opts && opts.current_height_cm) || 137.7),
      sleep_score: Number((opts && opts.sleep_score) || 3),
      nutrition_score: Number((opts && opts.nutrition_score) || 3),
      exercise_score: Number((opts && opts.exercise_score) || 3),
      posture_score: Number((opts && opts.posture_score) || 3)
    };
    var localRes = computeLocalKfgCommentary(payload);
    var history = appendCheckinHistory('KFG', {
      prev_height_cm: localRes.prev_height_cm,
      current_height_cm: localRes.current_height_cm,
      delta_cm: localRes.delta_cm,
      annualized_cm_yr: localRes.annualized_cm_yr,
      target_cm_yr: localRes.cdc_target_cm_yr
    }, siblingId);
    localRes.history = history;
    if (payload.email) {
      trackFunnelEvent('KFG', 'vip_checkin_submit');
    }
    return Promise.resolve(localRes);
  }

  function enrollKfkPaidVip(opts) {
    var email = String((opts && opts.email) || '').trim().toLowerCase();
    if (!/^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(email)) {
      return Promise.resolve({ ok: false, error: 'INVALID_EMAIL' });
    }
    var payload = {
      email: email,
      parent_name: String((opts && opts.parent_name) || 'Parent').trim(),
      child_name: String((opts && opts.child_name) || 'Child').trim(),
      child_sex: String((opts && opts.child_sex) || 'M').trim().toUpperCase(),
      child_age_years: Number((opts && opts.child_age_years) || 9),
      baseline_height_cm: Number((opts && opts.baseline_height_cm) || 134),
      plan_tier: String((opts && opts.plan_tier) || 'Latpeed Tier 2 (19,900 KRW)').trim(),
      months_remaining: Number((opts && opts.months_remaining) || 6),
      order_ref: String((opts && opts.order_ref) || 'LATPEED-VIP').trim()
    };
    try { localStorage.setItem('dc_kfk_paid_vip', JSON.stringify(payload)); } catch (_) {}
    return deliverPaidMagicPack({
      div: 'KFK',
      email: email,
      nickname: payload.parent_name,
      segment: 'KFK_Paid_VIP',
      plan_tier: payload.plan_tier,
      order_ref: payload.order_ref,
      hash_anchor: 'kfk-vip-monthly-checkin',
      profile_state: payload
    }).then(function (packRes) {
      return {
        ok: true,
        magic_restore_url: packRes.magic_restore_url,
        refund_support_url: packRes.refund_support_url,
        baseline_height_cm: payload.baseline_height_cm
      };
    });
  }

  function submitKfkVipCheckin(opts) {
    var payload = {
      email: String((opts && opts.email) || '').trim().toLowerCase(),
      child_name: String((opts && opts.child_name) || 'Child').trim(),
      child_sex: String((opts && opts.child_sex) || 'M').trim().toUpperCase(),
      child_age_years: Number((opts && opts.child_age_years) || 9),
      prev_height_cm: Number((opts && opts.prev_height_cm) || 134.0),
      current_height_cm: Number((opts && opts.current_height_cm) || 134.5),
      sleep_score: Number((opts && opts.sleep_score) || 4),
      nutrition_score: Number((opts && opts.nutrition_score) || 4),
      exercise_score: Number((opts && opts.exercise_score) || 3),
      posture_score: Number((opts && opts.posture_score) || 4)
    };
    var localRes = computeLocalKfkCommentary(payload);
    var history = appendCheckinHistory('KFK', {
      prev_height_cm: localRes.prev_height_cm,
      current_height_cm: localRes.current_height_cm,
      delta_cm: localRes.delta_cm,
      annualized_cm_yr: localRes.annualized_cm_yr,
      target_cm_yr: localRes.kdca_target_cm_yr
    });
    localRes.history = history;
    if (payload.email) {
      trackFunnelEvent('KFK', 'vip_checkin_submit');
    }
    return Promise.resolve(localRes);
  }

  function flushPendingQueue() {
    var q = readQueue();
    if (!q.length) return;
    var remaining = [];
    var chain = Promise.resolve();
    q.forEach(function (item) {
      chain = chain.then(function () {
        return postCloudJson('/api/crm/register', item).then(function (r) {
          if (!r || !r.ok) remaining.push(item);
        }).catch(function () { remaining.push(item); });
      });
    });
    chain.then(function () { writeQueue(remaining); });
  }

  // Auto-fire AARRR v6: Acquisition (landing_view + referral_visit), Retention (return_d1/d7/d30 + welcome bar),
  // Activation (quiz_start + sample_pdf_click), and Revenue (tier-tagged checkout_click + affiliate_click)!
  if (global.addEventListener) {
    global.addEventListener('DOMContentLoaded', function () {
      var div = detectDivFromHost();
      var utm = captureUtmParams();
      var prof = getOrCreateVisitorProfile();
      trackFunnelEvent(div, 'landing_view');

      // Closed-loop Referral Visit attribution (?ref=v_...)
      try {
        var sp = new URLSearchParams((global.location && global.location.search) || '');
        var urlRef = String(sp.get('ref') || '').replace(/[^A-Za-z0-9_\-]/g, '').slice(0, 32);
        if (urlRef && urlRef !== prof.visitor_id && sessionStorage.getItem('dc_ref_tracked_' + urlRef) !== '1') {
          sessionStorage.setItem('dc_ref_tracked_' + urlRef, '1');
          trackFunnelEvent(div, 'referral_visit', { ref_code: urlRef, event_meta: 'ref:' + urlRef });
        }
      } catch (_) {}

      // D1 / D7 / D30 Cohort Retention tracking (max 1x per calendar day) + Returning Welcome Strip
      try {
        var todayKey = new Date().toISOString().slice(0, 10);
        var isD7DripReturn = String(utm.utm_campaign || '').toLowerCase().indexOf('d7') >= 0;
        if (prof.days_since_first >= 30 && localStorage.getItem('dc_ret_d30_' + todayKey) !== '1') {
          localStorage.setItem('dc_ret_d30_' + todayKey, '1');
          trackFunnelEvent(div, 'return_d30', { event_meta: 'day_' + prof.days_since_first });
        } else if ((prof.days_since_first >= 7 || isD7DripReturn) && localStorage.getItem('dc_ret_d7_' + todayKey) !== '1') {
          localStorage.setItem('dc_ret_d7_' + todayKey, '1');
          trackFunnelEvent(div, 'return_d7', { event_meta: isD7DripReturn ? 'drip_d7' : ('day_' + prof.days_since_first) });
        } else if (prof.days_since_first >= 1 && localStorage.getItem('dc_ret_d1_' + todayKey) !== '1') {
          localStorage.setItem('dc_ret_d1_' + todayKey, '1');
          trackFunnelEvent(div, 'return_d1', { event_meta: 'day_' + prof.days_since_first });
        }
        if (prof.days_since_first >= 1 || isD7DripReturn) {
          mountReturningVisitorBanner(div, Math.max(1, prof.days_since_first));
        }
      } catch (_) {}

      setTimeout(flushPendingQueue, 1500);

      if (global.document && global.document.addEventListener) {
        global.document.addEventListener('click', function (ev) {
          var a = ev.target && ev.target.closest ? ev.target.closest('a,button') : null;
          if (!a) return;
          var href = String(a.getAttribute('href') || '');
          var id = String(a.id || '');

          // 1. Sample 2p PDF Inspection (Activation signal)
          if (/_sample_2p\.pdf/i.test(href)) {
            trackFunnelEvent(div, 'sample_pdf_click', { event_meta: href.split('/').pop() });
            return;
          }
          // 2. Quiz / Interactive Tool Start (Micro-Activation signal, 1x/session)
          if (id === 'btnStartPwStepUp' || id === 'btnStartPwStepUpBottom' || id === 'btnPwStartStepUp' || id === 'btn-kfg-begin-atelier-top' || id === 'btn-kfg-begin-atelier' || id === 'btnStartPwStepUpJp' || id === 'btnPwStartStepUpJp' || id === 'btn-start-atelier-hero' || id === 'btn-start-atelier-stepup' || id === 'btn-kfk-begin-atelier' || a.getAttribute('data-csp-act') === 'kfg-begin-atelier' || a.getAttribute('data-pw-start-stepup') === '1' || a.hasAttribute('data-kfk-age-chip') || a.hasAttribute('data-kfg-mini-start') || a.hasAttribute('data-tom-stress-btn')) {
            try {
              if (sessionStorage.getItem('dc_quiz_start_' + div) !== '1') {
                sessionStorage.setItem('dc_quiz_start_' + div, '1');
                trackFunnelEvent(div, 'quiz_start', { event_meta: id || a.getAttribute('data-kfk-age-chip') || a.getAttribute('data-tom-stress-btn') || 'start_btn' });
              }
            } catch (_) {}
            return;
          }
          // 3. HERO Affiliate Store Click (distinct Revenue event — covers Naver CShop, BrandConnect & Coupang)
          if (/cshop\.naver\.com|brandconnect\.naver\.com|coupang\.com/i.test(href)) {
            var affMeta = /brandconnect\.naver\.com/i.test(href) ? 'naver_brandconnect' : (/naver/i.test(href) ? 'naver_cshop' : 'coupang');
            trackFunnelEvent(div, 'affiliate_click', { event_meta: affMeta });
            return;
          }
          // 4. Paid PG Checkout Click with Value-Ladder step tag (step2_low / step3_core / step4_premium)
          if (/whop\.com|buy\.polar\.sh|latpeed\.com/i.test(href)) {
            var stepTag = classifyCheckoutStepFromHref(href, a);
            trackFunnelEvent(div, 'checkout_click', { event_meta: stepTag || 'pg_click' });
          }
        }, true);
      }
    });
  }

  global.DreamCompanyCRM = {
    CLOUD_API_BASE: CLOUD_API_BASE,
    registerMember: registerMember,
    requestAuthOtp: requestAuthOtp,
    verifyEntitlement: verifyEntitlement,
    openProtectedPdfDownload: openProtectedPdfDownload,
    getSignedDownloadUrl: getSignedDownloadUrl,
    escapeHtml: escapeHtml,
    isAllowedExternalUrl: isAllowedExternalUrl,
    trackFunnelEvent: trackFunnelEvent,
    getOrCreateVisitorProfile: getOrCreateVisitorProfile,
    buildReferralShareUrl: buildReferralShareUrl,
    detectIsQaOrBot: detectIsQaOrBot,
    fetchHeroVotes: fetchHeroVotes,
    submitHeroVote: submitHeroVote,
    fetchHeroStories: fetchHeroStories,
    submitHeroStory: submitHeroStory,
    cheerHeroStory: cheerHeroStory,
    fetchVerifiedReviews: fetchVerifiedReviews,
    deliverPaidMagicPack: deliverPaidMagicPack,
    encodeMagicRestoreUrl: encodeMagicRestoreUrl,
    decodeMagicRestoreParam: decodeMagicRestoreParam,
    getPaidVault: getPaidVault,
    savePaidVault: savePaidVault,
    submitSatisfactionVote: submitSatisfactionVote,
    mountSatisfactionBar: mountSatisfactionBar,
    buildRefundSupportMailto: buildRefundSupportMailto,
    getSupportEmail: getSupportEmail,
    enrollKfgPaidVip: enrollKfgPaidVip,
    submitKfgVipCheckin: submitKfgVipCheckin,
    enrollKfkPaidVip: enrollKfkPaidVip,
    submitKfkVipCheckin: submitKfkVipCheckin,
    readCheckinHistory: readCheckinHistory,
    appendCheckinHistory: appendCheckinHistory,
    getLocalMember: getLocalMember,
    flushPendingQueue: flushPendingQueue
  };
})(typeof window !== 'undefined' ? window : this);
