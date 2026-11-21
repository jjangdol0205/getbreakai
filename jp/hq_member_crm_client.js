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

  function postCloudJson(path, payload) {
    return fetch(CLOUD_API_BASE + path, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload || {})
    }).then(function (res) {
      return res.json().catch(function () { return { ok: res.ok, status: res.status }; });
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
   * UTM Capture & 4-Stage Funnel Analytics (`landing_view -> quiz_complete -> checkout_click -> paid_success`)
   * ========================================================================== */
  function captureUtmParams() {
    try {
      var sp = new URLSearchParams((global.location && global.location.search) || '');
      var utm = {
        utm_source: sp.get('utm_source') || '',
        utm_medium: sp.get('utm_medium') || '',
        utm_campaign: sp.get('utm_campaign') || ''
      };
      if (utm.utm_source || utm.utm_medium || utm.utm_campaign) {
        sessionStorage.setItem('dc_utm_params', JSON.stringify(utm));
        return utm;
      }
      var saved = sessionStorage.getItem('dc_utm_params');
      return saved ? JSON.parse(saved) : utm;
    } catch (_) {
      return { utm_source: '', utm_medium: '', utm_campaign: '' };
    }
  }

  function trackFunnelEvent(div, eventName, extra) {
    try {
      var d = String(div || detectDivFromHost()).toUpperCase();
      var utm = captureUtmParams();
      var payload = {
        div_code: d,
        event_name: String(eventName || 'landing_view'),
        utm_source: utm.utm_source || (extra && extra.utm_source) || '',
        utm_medium: utm.utm_medium || (extra && extra.utm_medium) || '',
        utm_campaign: utm.utm_campaign || (extra && extra.utm_campaign) || '',
        page_path: (global.location && global.location.pathname) ? global.location.pathname : '/'
      };
      if (typeof global.gtag === 'function') {
        try { global.gtag('event', payload.event_name, { division: d, utm_source: payload.utm_source, utm_campaign: payload.utm_campaign }); } catch (_) {}
      }
      return postCloudJson('/api/analytics/event', payload).catch(function () { return { ok: false }; });
    } catch (_) {
      return Promise.resolve({ ok: false });
    }
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
    var payload = {
      div_code: div,
      div: div,
      email: email,
      nickname: nickname,
      segment: segment,
      metadata: {
        message: message,
        lang: lang,
        utm: captureUtmParams(),
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
          access_code: code || '',
          verified_at: new Date().toISOString()
        });
      }
      return res || { ok: false, authorized: false, reason: 'verification_failed' };
    }).catch(function () {
      return { ok: false, authorized: false, reason: 'network_error' };
    });
  }

  function openProtectedPdfDownload(div, docKey, onNeedsReauth) {
    var d = String(div || detectDivFromHost()).trim().toUpperCase();
    var triggerNav = function (signedUrl) {
      if (!signedUrl || !isAllowedExternalUrl(signedUrl)) return false;
      trackFunnelEvent(d, 'pdf_download');
      var w = null;
      try { w = global.open(signedUrl, '_blank', 'noopener,noreferrer'); } catch (_) {}
      if (!w && global.location) global.location.href = signedUrl;
      return true;
    };

    var cached = getSignedDownloadUrl(d, docKey);
    if (cached && triggerNav(cached)) {
      return Promise.resolve({ ok: true, cached: true });
    }

    var vault = getPaidVault(d);
    if (vault && vault.email && vault.access_code) {
      return verifyEntitlement({ div: d, email: vault.email, access_code: vault.access_code }).then(function (vres) {
        var fresh = (vres && vres.authorized && vres.downloads && vres.downloads[docKey]) ? vres.downloads[docKey] : '';
        if (fresh && triggerNav(fresh)) {
          return { ok: true, refreshed: true };
        }
        if (typeof onNeedsReauth === 'function') onNeedsReauth(vres);
        return { ok: false, reason: 'reauth_required' };
      });
    }

    if (typeof onNeedsReauth === 'function') onNeedsReauth({ authorized: false, reason: 'reauth_required' });
    return Promise.resolve({ ok: false, reason: 'reauth_required' });
  }

  /* ==========================================================================
   * 3. Standard Digital Refund & Support Link (Replaces legacy 14-Day copy!)
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
  function submitSatisfactionVote(opts) {
    var div = String((opts && opts.div) || detectDivFromHost()).trim().toUpperCase();
    var vote = String((opts && opts.vote) || 'up').trim().toLowerCase();
    var contextKey = String((opts && opts.context) || 'paid_report').trim();
    var voteRec = { div: div, vote: vote, context: contextKey, voted_at: new Date().toISOString() };
    try {
      localStorage.setItem('dc_sat_vote_' + div + '_' + contextKey, JSON.stringify(voteRec));
    } catch (_) {}
    return trackFunnelEvent(div, 'sat_vote_' + vote).then(function () {
      return { ok: true, div: div, vote: vote };
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
          if (wrap) wrap.innerHTML = '<span style="font-weight:600;">' + labels.thanks + '</span>';
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

  // Auto-fire Stage 1 funnel `landing_view` + flush queue + auto-wire checkout_click on Whop/Polar/Latpeed links!
  if (global.addEventListener) {
    global.addEventListener('DOMContentLoaded', function () {
      var div = detectDivFromHost();
      captureUtmParams();
      trackFunnelEvent(div, 'landing_view');
      setTimeout(flushPendingQueue, 1500);
      if (global.document && global.document.addEventListener) {
        global.document.addEventListener('click', function (ev) {
          var a = ev.target && ev.target.closest ? ev.target.closest('a,button') : null;
          if (!a) return;
          var href = String(a.getAttribute('href') || '');
          if (/whop\.com|buy\.polar\.sh|latpeed\.com|cshop\.naver\.com|influencers\.coupang\.com/i.test(href)) {
            trackFunnelEvent(div, 'checkout_click');
          }
        });
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
    fetchHeroVotes: fetchHeroVotes,
    submitHeroVote: submitHeroVote,
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
