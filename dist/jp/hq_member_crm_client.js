/**
 * Dream Company HQ - Universal Passwordless Club, Cross-Device Magic Restore & Retention Client (v4 Phase 3)
 * Shared across Divisions 1-5 static GitHub Pages frontends (100% ASCII source for Zero-Hangul scanner safety).
 *
 * Capabilities:
 *  1. Passwordless 3-second club registration (`dc_member_<DIV>`) + offline retry queue (`dc_crm_sync_queue_v1`)
 *  2. Cross-Device Permanent Magic Restore (`?magic_restore=<base64url>`) - zero localStorage dependency across phones/PCs
 *  3. 60-Second Paid Delivery Trigger (`deliverPaidMagicPack`) with dual GAS v4 + v1 (`register_member` notes) compatibility
 *  4. 1-Second Satisfaction Vote (`submitSatisfactionVote` & `mountSatisfactionBar`) + 14-Day Refund / 1-Click Support link
 *  5. Cumulative 6-Month Height Velocity Tracker (`KFG` & `KFK`) with pre-filled 30s check-in & Day-165 Graduation Album state
 */
(function (global) {
  'use strict';

  var ENDPOINT_CACHE = null;
  var QUEUE_KEY = 'dc_crm_sync_queue_v1';
  var SUPPORT_EMAIL = 'beable9489@gmail.com';

  function resolveEndpointUrl() {
    if (ENDPOINT_CACHE) return Promise.resolve(ENDPOINT_CACHE);
    if (global.HQ_MAILING_ENDPOINT && String(global.HQ_MAILING_ENDPOINT).indexOf('https://script.google.com/macros/s/') === 0) {
      ENDPOINT_CACHE = String(global.HQ_MAILING_ENDPOINT).trim();
      return Promise.resolve(ENDPOINT_CACHE);
    }
    var jsonPath = global.HQ_MAILING_CONFIG_PATH || '/hq-mailing-endpoint.json';
    return fetch(jsonPath + '?v=' + Math.floor(Date.now() / 300000), { cache: 'no-store' })
      .then(function (res) { return res.ok ? res.json() : null; })
      .then(function (cfg) {
        if (cfg && cfg.webapp_exec_url && String(cfg.webapp_exec_url).indexOf('https://script.google.com/macros/s/') === 0) {
          ENDPOINT_CACHE = String(cfg.webapp_exec_url).trim();
          return ENDPOINT_CACHE;
        }
        return '';
      })
      .catch(function () { return ''; });
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
      localStorage.setItem(QUEUE_KEY, JSON.stringify(items.slice(-30)));
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
    compact.v = 4;
    if (!compact.ts) compact.ts = Math.floor(Date.now() / 1000);
    var token = toBase64Url(JSON.stringify(compact));
    var sep = cleanBase.indexOf('?') >= 0 ? '&' : '?';
    var anchor = hashAnchor ? (String(hashAnchor).charAt(0) === '#' ? hashAnchor : '#' + hashAnchor) : '';
    return cleanBase + sep + 'magic_restore=' + encodeURIComponent(token) + anchor;
  }

  function decodeMagicRestoreParam(searchStr) {
    try {
      var qs = String(searchStr !== undefined ? searchStr : (global.location ? global.location.search : ''));
      var m = qs.match(/[?&]magic_restore=([^&#]+)/);
      if (!m || !m[1]) return null;
      var jsonTxt = fromBase64Url(decodeURIComponent(m[1]));
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
      var restored = decodeMagicRestoreParam();
      if (restored && (!restored.div || String(restored.div).toUpperCase() === d)) {
        savePaidVault(d, restored);
        return restored;
      }
      var raw = localStorage.getItem('dc_paid_vault_' + d);
      return raw ? JSON.parse(raw) : null;
    } catch (_) {
      return null;
    }
  }

  /* ==========================================================================
   * Apps Script Transport with Automatic GAS v1 Fallback (`register_member`)
   * ========================================================================== */
  function postToAppsScript(execUrl, payload) {
    return fetch(execUrl, {
      method: 'POST',
      headers: { 'Content-Type': 'text/plain;charset=utf-8' },
      body: JSON.stringify(payload),
      redirect: 'follow'
    }).then(function (res) {
      return res.text().then(function (txt) {
        try { return JSON.parse(txt); } catch (_) { return { ok: res.ok }; }
      });
    });
  }

  function postWithLegacyFallback(payload, fallbackMemberPayload) {
    return resolveEndpointUrl().then(function (execUrl) {
      if (!execUrl) {
        var q = readQueue();
        q.push(fallbackMemberPayload || payload);
        writeQueue(q);
        return { ok: true, queued_for_sync: true };
      }
      return postToAppsScript(execUrl, payload).then(function (res) {
        if (res && res.ok === false && /UNAUTHORIZED|UNKNOWN_ACTION/i.test(String(res.error || '')) && fallbackMemberPayload) {
          return postToAppsScript(execUrl, fallbackMemberPayload);
        }
        return res;
      }).catch(function () {
        var q2 = readQueue();
        q2.push(fallbackMemberPayload || payload);
        writeQueue(q2);
        return { ok: true, queued_for_sync: true };
      });
    });
  }

  function registerMember(opts) {
    var div = String((opts && opts.div) || '').trim().toUpperCase();
    var email = String((opts && opts.email) || '').trim().toLowerCase();
    var nickname = String((opts && opts.nickname) || '').trim();
    var segment = String((opts && opts.segment) || 'general').trim();
    var message = String((opts && (opts.message || opts.notes)) || '').trim();
    var lang = String((opts && opts.lang) || '').trim();
    var websiteHp = String((opts && opts.website_hp) || '').trim();

    if (!/^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(email)) {
      return Promise.resolve({ ok: false, error: 'INVALID_EMAIL' });
    }

    var payload = {
      action: 'register_member',
      div: div,
      email: email,
      nickname: nickname,
      segment: segment,
      message: message,
      notes: message,
      lang: lang,
      website_hp: websiteHp,
      source_url: (global.location && global.location.href) ? global.location.href : '',
      client_ts: new Date().toISOString()
    };

    saveLocalMember(div, {
      div: div,
      email: email,
      nickname: nickname,
      segment: segment,
      joined_at: payload.client_ts
    });

    return postWithLegacyFallback(payload, null).then(function (res) {
      if (res && typeof res === 'object') {
        res.div = res.div || div;
        res.email = email;
        res.segment = segment;
      }
      return res;
    });
  }

  /* ==========================================================================
   * 60-Second Cross-Device Paid Magic Pack Delivery (Divisions 1-5)
   * ========================================================================== */
  function buildRefundSupportMailto(div, email, orderRef) {
    var d = String(div || 'HQ').toUpperCase();
    var subj = '[' + d + ' 14-Day Refund / Priority Support] ' + (orderRef || email || 'Member Request');
    return 'mailto:' + SUPPORT_EMAIL + '?subject=' + encodeURIComponent(subj);
  }

  function deliverPaidMagicPack(opts) {
    var div = String((opts && opts.div) || 'TOM').trim().toUpperCase();
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
      return Promise.resolve({
        ok: true,
        local_only: true,
        magic_restore_url: magicUrl,
        refund_support_url: refundUrl,
        vault: vaultRecord
      });
    }

    var segMap = {
      TOM: 'TOM_Paid_VIP',
      KFG: 'KFG_Paid_VIP',
      GBA: 'GBA_Paid_VIP',
      HERO: 'hero_honor_9900',
      KFK: 'KFK_Paid_VIP'
    };
    var seg = String((opts && opts.segment) || segMap[div] || (div + '_Paid_VIP'));
    var primaryPayload = {
      action: 'deliver_paid_magic_pack',
      div: div,
      email: email,
      nickname: String((opts && opts.nickname) || '').trim(),
      segment: seg,
      plan_tier: planTier,
      order_ref: orderRef,
      magic_restore_url: magicUrl,
      refund_support_url: refundUrl,
      profile_state: statePayload,
      client_ts: vaultRecord.activated_at
    };
    var compactNote = 'PAID_MAGIC_PACK_V4|' + JSON.stringify({
      tier: planTier,
      ref: orderRef,
      magic: magicUrl.slice(0, 950),
      ts: vaultRecord.activated_at
    });
    var fallbackPayload = {
      action: 'register_member',
      div: div,
      email: email,
      nickname: primaryPayload.nickname,
      segment: seg,
      notes: compactNote,
      message: compactNote,
      source_url: magicUrl.slice(0, 245)
    };

    return postWithLegacyFallback(primaryPayload, fallbackPayload).then(function (res) {
      return {
        ok: true,
        crm_sync: res,
        magic_restore_url: magicUrl,
        refund_support_url: refundUrl,
        vault: vaultRecord
      };
    });
  }

  /* ==========================================================================
   * 1-Second Satisfaction Vote (`[+ / = / -]` & Weekly Feedback Sync)
   * ========================================================================== */
  function submitSatisfactionVote(opts) {
    var div = String((opts && opts.div) || 'TOM').trim().toUpperCase();
    var vote = String((opts && opts.vote) || 'up').trim().toLowerCase(); // up | neutral | down
    var contextKey = String((opts && opts.context) || 'paid_report').trim();
    var localMem = getLocalMember(div);
    var paidVault = getPaidVault(div);
    var email = String((opts && opts.email) || (paidVault && paidVault.email) || (localMem && localMem.email) || '').trim().toLowerCase();

    var voteRec = {
      div: div,
      vote: vote,
      context: contextKey,
      voted_at: new Date().toISOString()
    };
    try {
      localStorage.setItem('dc_sat_vote_' + div + '_' + contextKey, JSON.stringify(voteRec));
    } catch (_) {}

    var v4Payload = {
      action: 'submit_satisfaction_vote',
      div: div,
      email: email || ('anon-' + div.toLowerCase() + '@dreamcompany.local'),
      vote: vote,
      context: contextKey,
      source_url: (global.location && global.location.href) ? global.location.href : '',
      client_ts: voteRec.voted_at
    };
    var noteStr = 'SAT_VOTE_V4|' + vote.toUpperCase() + '|' + contextKey + '|' + voteRec.voted_at;
    var fallback = email ? {
      action: 'register_member',
      div: div,
      email: email,
      segment: (paidVault && paidVault.plan_tier) ? (div + '_Paid_VIP') : 'general',
      notes: noteStr,
      message: noteStr
    } : null;

    return postWithLegacyFallback(v4Payload, fallback).then(function () {
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
    var div = String((opts && opts.div) || 'TOM').toUpperCase();
    var contextKey = String((opts && opts.context) || 'paid_report');
    var allowEmoji = (div === 'HERO');
    var labels = getLocalizedVoteStrings(div, allowEmoji);
    var isHero = (div === 'HERO');
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
          if (wrap) {
            wrap.innerHTML = '<span style="font-weight:600;">' + labels.thanks + '</span>';
          }
        });
      })(btns[i]);
    }
  }

  /* ==========================================================================
   * Pediatric 6-Month Cumulative Height Velocity History (KFG & KFK)
   * ========================================================================== */
  function readCheckinHistory(div) {
    var key = 'dc_checkin_history_' + String(div || 'KFG').toUpperCase();
    try {
      var raw = localStorage.getItem(key);
      var arr = raw ? JSON.parse(raw) : [];
      return Array.isArray(arr) ? arr : [];
    } catch (_) {
      return [];
    }
  }

  function appendCheckinHistory(div, entry) {
    var d = String(div || 'KFG').toUpperCase();
    var key = 'dc_checkin_history_' + d;
    var arr = readCheckinHistory(d);
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
    try {
      localStorage.setItem(key, JSON.stringify(trimmed));
    } catch (_) {}
    return trimmed;
  }

  function enrollKfgPaidVip(opts) {
    var email = String((opts && opts.email) || '').trim().toLowerCase();
    if (!/^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(email)) {
      return Promise.resolve({ ok: false, error: 'INVALID_EMAIL' });
    }
    var payload = {
      action: 'enroll_kfg_paid_vip',
      email: email,
      parent_name: String((opts && opts.parent_name) || 'Parent').trim(),
      child_name: String((opts && opts.child_name) || 'Your Child').trim(),
      child_sex: String((opts && opts.child_sex) || 'M').trim().toUpperCase(),
      child_age_years: Number((opts && opts.child_age_years) || 9),
      baseline_height_cm: Number((opts && opts.baseline_height_cm) || 134),
      plan_tier: String((opts && opts.plan_tier) || '6-Month Growth Pass ($19.99)').trim(),
      months_remaining: Number((opts && opts.months_remaining) || 6),
      order_ref: String((opts && opts.order_ref) || 'POLAR-KFG-VIP').trim()
    };
    try {
      localStorage.setItem('dc_kfg_paid_vip', JSON.stringify(payload));
    } catch (_) {}

    deliverPaidMagicPack({
      div: 'KFG',
      email: email,
      nickname: payload.parent_name,
      plan_tier: payload.plan_tier,
      order_ref: payload.order_ref,
      hash_anchor: 'kfg-vip-monthly-checkin',
      profile_state: payload
    });

    return postWithLegacyFallback(payload, null).then(function (res) {
      return res || { ok: true, baseline_height_cm: payload.baseline_height_cm };
    });
  }

  function computeLocalKfgCommentary(payload) {
    var prevH = Number(payload.prev_height_cm) || (Number(payload.current_height_cm) - 0.5);
    var curH = Number(payload.current_height_cm) || 134.5;
    var age = Number(payload.child_age_years) || 9;
    var isF = String(payload.child_sex || 'M').toUpperCase().charAt(0) === 'F';
    var targetVel = age < 6 ? 6.6 : (age < 9 ? 5.7 : (age < 11.5 ? (isF ? 7.4 : 5.5) : (age < 14 ? (isF ? 5.6 : 8.2) : 3.6)));
    var delta = Math.round((curH - prevH) * 100) / 100;
    var annVel = Math.round(((delta / 30) * 365) * 10) / 10;
    var habits = [
      { key: 'Deep Sleep Window (Pre-10 PM GH Pulse)', score: Number(payload.sleep_score) || 3, tip: 'Shift lights-out 30 minutes earlier and turn off screens 45 minutes before bed to protect peak Growth Hormone release.' },
      { key: 'Protein + Calcium / Vit D3 / Zinc Intake', score: Number(payload.nutrition_score) || 3, tip: 'Pair dinner lean protein with bioavailable Calcium, Vitamin D3, and Zinc for healthy bone-plate mineralization.' },
      { key: 'Daily 20-Min Vertical Impact & Stretch', score: Number(payload.exercise_score) || 3, tip: 'Add 15-20 minutes of jump-rope, hops, or evening spinal decompression stretches daily.' },
      { key: 'Spinal Posture & Nasal Breathing', score: Number(payload.posture_score) || 3, tip: 'Correct forward-head desk posture and check nighttime nasal breathing to protect 1.0-1.8 cm of standing stature.' }
    ].sort(function (a, b) { return a.score - b.score; });
    var verdict = delta <= 0
      ? ('Height held steady at ' + curH.toFixed(1) + ' cm this 30-day cycle; linear growth occurs in saltatory pulses - protect morning measurement consistency and pre-10 PM sleep.')
      : ('30-day gain of +' + delta.toFixed(2) + ' cm (~' + annVel.toFixed(1) + ' cm/yr annualized pace vs. US CDC age-' + age + ' reference of ' + targetVel.toFixed(1) + ' cm/yr).');
    return {
      ok: true,
      prev_height_cm: prevH,
      current_height_cm: curH,
      delta_cm: delta,
      delta_inches: Math.round((delta / 2.54) * 100) / 100,
      annualized_cm_yr: annVel,
      annualized_in_yr: Math.round((annVel / 2.54) * 100) / 100,
      cdc_target_cm_yr: targetVel,
      velocity_verdict: verdict,
      strongest_habit: habits[habits.length - 1],
      priority_bottleneck: habits[0]
    };
  }

  function submitKfgVipCheckin(opts) {
    var payload = {
      action: 'submit_kfg_vip_checkin',
      email: String((opts && opts.email) || '').trim().toLowerCase(),
      vip_token: String((opts && opts.vip_token) || '').trim(),
      paid_verified: Boolean(opts && opts.paid_verified),
      order_ref: String((opts && opts.order_ref) || '').trim(),
      child_name: String((opts && opts.child_name) || 'Your Child').trim(),
      child_sex: String((opts && opts.child_sex) || 'M').trim().toUpperCase(),
      child_age_years: Number((opts && opts.child_age_years) || 9),
      prev_height_cm: Number((opts && opts.prev_height_cm) || 0),
      current_height_cm: Number((opts && opts.current_height_cm) || 0),
      sleep_score: Number((opts && opts.sleep_score) || 3),
      nutrition_score: Number((opts && opts.nutrition_score) || 3),
      exercise_score: Number((opts && opts.exercise_score) || 3),
      posture_score: Number((opts && opts.posture_score) || 3)
    };
    var localFallback = computeLocalKfgCommentary(payload);
    var history = appendCheckinHistory('KFG', {
      prev_height_cm: localFallback.prev_height_cm,
      current_height_cm: localFallback.current_height_cm,
      delta_cm: localFallback.delta_cm,
      annualized_cm_yr: localFallback.annualized_cm_yr,
      target_cm_yr: localFallback.cdc_target_cm_yr
    });
    localFallback.history = history;

    return postWithLegacyFallback(payload, null).then(function (res) {
      if (res && typeof res === 'object') {
        var merged = {};
        var k;
        for (k in localFallback) { if (Object.prototype.hasOwnProperty.call(localFallback, k)) merged[k] = localFallback[k]; }
        for (k in res) { if (Object.prototype.hasOwnProperty.call(res, k) && res[k] !== undefined && res[k] !== null) merged[k] = res[k]; }
        merged.history = history;
        return merged;
      }
      return localFallback;
    });
  }

  function enrollKfkPaidVip(opts) {
    var email = String((opts && opts.email) || '').trim().toLowerCase();
    if (!/^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(email)) {
      return Promise.resolve({ ok: false, error: 'INVALID_EMAIL' });
    }
    var payload = {
      action: 'enroll_kfk_paid_vip',
      email: email,
      parent_name: String((opts && opts.parent_name) || 'Parent').trim(),
      child_name: String((opts && opts.child_name) || 'Child').trim(),
      child_sex: String((opts && opts.child_sex) || 'M').trim().toUpperCase(),
      child_age_years: Number((opts && opts.child_age_years) || 9),
      baseline_height_cm: Number((opts && opts.baseline_height_cm) || 134),
      plan_tier: String((opts && opts.plan_tier) || 'Latpeed Tier 2 (19,900 KRW)').trim(),
      months_remaining: Number((opts && opts.months_remaining) || 6),
      order_ref: String((opts && opts.order_ref) || 'LATPEED-EMAIL-PASS').trim()
    };
    try {
      localStorage.setItem('dc_kfk_paid_vip', JSON.stringify(payload));
    } catch (_) {}

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
      var fallback = {
        action: 'register_member',
        div: 'KFK',
        email: email,
        nickname: payload.parent_name,
        segment: 'KFK_Paid_VIP',
        notes: 'KFK_PAID_VIP|' + JSON.stringify({
          child: payload.child_name,
          sex: payload.child_sex,
          age: payload.child_age_years,
          h0: payload.baseline_height_cm,
          tier: payload.plan_tier,
          ref: payload.order_ref
        })
      };
      return postWithLegacyFallback(payload, fallback).then(function (res) {
        return {
          ok: true,
          crm: res,
          magic_restore_url: packRes.magic_restore_url,
          refund_support_url: packRes.refund_support_url,
          baseline_height_cm: payload.baseline_height_cm
        };
      });
    });
  }

  function submitKfkVipCheckin(opts) {
    var curH = Number((opts && opts.current_height_cm) || 134.5);
    var prevH = Number((opts && opts.prev_height_cm) || (curH - 0.5));
    var age = Number((opts && opts.child_age_years) || 9);
    var isF = String((opts && opts.child_sex) || 'M').toUpperCase().charAt(0) === 'F';
    var targetVel = age < 6 ? 6.6 : (age < 9 ? 5.8 : (age < 11.5 ? (isF ? 7.5 : 5.6) : (age < 14 ? (isF ? 5.5 : 8.3) : 3.5)));
    var delta = Math.round((curH - prevH) * 100) / 100;
    var annVel = Math.round(((delta / 30) * 365) * 10) / 10;
    var history = appendCheckinHistory('KFK', {
      prev_height_cm: prevH,
      current_height_cm: curH,
      delta_cm: delta,
      annualized_cm_yr: annVel,
      target_cm_yr: targetVel
    });

    var payload = {
      action: 'submit_kfk_vip_checkin',
      email: String((opts && opts.email) || '').trim().toLowerCase(),
      paid_verified: true,
      order_ref: String((opts && opts.order_ref) || 'LATPEED-VIP').trim(),
      child_name: String((opts && opts.child_name) || 'Child').trim(),
      child_sex: isF ? 'F' : 'M',
      child_age_years: age,
      prev_height_cm: prevH,
      current_height_cm: curH,
      sleep_score: Number((opts && opts.sleep_score) || 4),
      nutrition_score: Number((opts && opts.nutrition_score) || 4),
      exercise_score: Number((opts && opts.exercise_score) || 3),
      posture_score: Number((opts && opts.posture_score) || 4)
    };
    var fallback = payload.email ? {
      action: 'register_member',
      div: 'KFK',
      email: payload.email,
      segment: 'KFK_Paid_VIP',
      notes: 'KFK_CHECKIN|' + prevH + '->' + curH + '|vel=' + annVel + 'cm/yr'
    } : null;

    return postWithLegacyFallback(payload, fallback).then(function (res) {
      return {
        ok: true,
        crm: res,
        prev_height_cm: prevH,
        current_height_cm: curH,
        delta_cm: delta,
        annualized_cm_yr: annVel,
        kdca_target_cm_yr: targetVel,
        history: history
      };
    });
  }

  function flushPendingQueue() {
    var q = readQueue();
    if (!q.length) return;
    resolveEndpointUrl().then(function (execUrl) {
      if (!execUrl) return;
      var remaining = [];
      var chain = Promise.resolve();
      q.forEach(function (item) {
        chain = chain.then(function () {
          return postToAppsScript(execUrl, item).catch(function () {
            remaining.push(item);
          });
        });
      });
      chain.then(function () { writeQueue(remaining); });
    });
  }

  if (global.addEventListener) {
    global.addEventListener('DOMContentLoaded', function () {
      setTimeout(flushPendingQueue, 1800);
    });
  }

  global.DreamCompanyCRM = {
    registerMember: registerMember,
    deliverPaidMagicPack: deliverPaidMagicPack,
    encodeMagicRestoreUrl: encodeMagicRestoreUrl,
    decodeMagicRestoreParam: decodeMagicRestoreParam,
    getPaidVault: getPaidVault,
    savePaidVault: savePaidVault,
    submitSatisfactionVote: submitSatisfactionVote,
    mountSatisfactionBar: mountSatisfactionBar,
    buildRefundSupportMailto: buildRefundSupportMailto,
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
