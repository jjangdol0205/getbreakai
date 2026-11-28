/* Dream Company Conversion UX Add-ons v20261125 (Strict CSP — Zero Inline Handlers, Zero Raw Hangul)
 * Preserves existing layout, design, auth, and checkout 100%.
 * Includes:
 *  1) Bottom Floating Pill CTA Bar (Divisions 1-5, scroll > 360, auto-hides over forms/checkout/footer/audio)
 *  2) Concrete 3-Card Deliverables Spec + Pre-Purchase FAQ (4 Qs) + Transparent 3-Line Review Policy (>=3 auto-show)
 *     - Always visible right above paid CTAs (never buried inside collapsed <details> accordions)
 *     - Also surfaced cleanly on Screen 0 opening editorial spread for immediate visitor trust
 *  3) #3 1-Second Intuitive 3-Stage Status Badges (Divisions 2 KFG, 3 GBA, 5 KFK ONLY — excluded on Div 1 TOM)
 *  4) Lightweight 1-Line Protection Ribbon inside Paid Vaults (TOM, KFG, GBA, KFK)
 */
(function initDreamCompanyUxAddons() {
  'use strict';
  if (typeof window === 'undefined' || typeof document === 'undefined') return;
  if (window.__DC_UX_ADDONS_V2__) return;
  window.__DC_UX_ADDONS_V2__ = true;

  function isInternalOrBotTraffic() {
    try {
      if (typeof window.__dcIsInternalOrBot === 'function' && window.__dcIsInternalOrBot()) return true;
      var sp = new URLSearchParams((window.location && window.location.search) || '');
      var isHttps = !!(window.location && window.location.protocol === 'https:');
      var ic = sp.get('internal_check');
      var od = sp.get('owner_device');
      if (ic === '0' || od === '0') {
        try { window.localStorage && window.localStorage.removeItem('dc_internal_exclude'); } catch (_r1) {}
        try { document.cookie = 'dc_internal_exclude=; Max-Age=0; Path=/; SameSite=Lax' + (isHttps ? '; Secure' : ''); } catch (_r2) {}
      } else if (ic === '1' || od === '1') {
        try { window.localStorage && window.localStorage.setItem('dc_internal_exclude', '1'); } catch (_w1) {}
        try { document.cookie = 'dc_internal_exclude=1; Max-Age=31536000; Path=/; SameSite=Lax' + (isHttps ? '; Secure' : ''); } catch (_w2) {}
        return true;
      }
      try { if (window.localStorage && window.localStorage.getItem('dc_internal_exclude') === '1') return true; } catch (_l1) {}
      try { if (/(?:^|;\s*)dc_internal_exclude=1(?:;|$)/.test(document.cookie || '')) return true; } catch (_c1) {}
      if (sp.get('internal_test') === '1' || sp.get('smoke_test') === '1') {
        try { window.sessionStorage && window.sessionStorage.setItem('dc_internal_test', '1'); } catch (_s1) {}
        return true;
      }
      try { if (window.sessionStorage && window.sessionStorage.getItem('dc_internal_test') === '1') return true; } catch (_s2) {}
      if (window.navigator && window.navigator.webdriver === true) return true;
      if (/HeadlessChrome|Playwright|Puppeteer|Selenium|LiveAudit|Watchdog|GitHub-Actions/i.test(String((window.navigator && window.navigator.userAgent) || ''))) return true;
    } catch (_g) {}
    return false;
  }
  isInternalOrBotTraffic();


  function detectDiv() {
    var host = String((window.location && window.location.hostname) || '').toLowerCase();
    var path = String((window.location && window.location.pathname) || '').toLowerCase();
    if (host.indexOf('kisfitglobal') !== -1 || host.indexOf('kfg-pages') !== -1) return 'KFG';
    if (host.indexOf('getbreakai') !== -1 || host.indexOf('gba-pages') !== -1) return 'GBA';
    if (host.indexOf('paradise-hero') !== -1 || host.indexOf('hero-pages') !== -1) return 'HERO';
    if (host.indexOf('kidsfit.co.kr') !== -1 || host.indexOf('kfk-pages') !== -1) return 'KFK';
    if (path.indexOf('/jp') === 0) return 'GBA';
    return 'TOM';
  }

  var DIV = detectDiv();
  var PATH = String((window.location && window.location.pathname) || '/').toLowerCase();
  var IS_MAIN =
    PATH === '/' ||
    PATH === '/index.html' ||
    PATH === '/jp' ||
    PATH === '/jp/' ||
    PATH === '/jp/index.html';

  function esc(str) {
    return String(str == null ? '' : str)
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;');
  }

  function injectStyles() {
    if (document.getElementById('dcUxAddonsStyle')) return;
    var st = document.createElement('style');
    st.id = 'dcUxAddonsStyle';
    st.textContent =
      '.dc-pill-bar{position:fixed;left:50%;bottom:16px;transform:translateX(-50%) translateY(120px);z-index:8800;display:flex;align-items:center;gap:8px;padding:8px 10px;border-radius:999px;background:rgba(15,44,34,0.96);color:#FAF7F2;box-shadow:0 12px 32px rgba(15,44,34,0.28);border:1px solid rgba(250,247,242,0.22);transition:transform 0.28s ease,opacity 0.28s ease;opacity:0;pointer-events:none;max-width:calc(100vw - 24px);}' +
      '.dc-pill-bar.is-visible{transform:translateX(-50%) translateY(0);opacity:1;pointer-events:auto;}' +
      '.dc-pill-btn{display:inline-flex;align-items:center;justify-content:center;white-space:nowrap;padding:9px 15px;border-radius:999px;font-weight:700;font-size:0.86rem;text-decoration:none;cursor:pointer;border:none;font-family:inherit;}' +
      '.dc-pill-primary{background:#FAF7F2;color:#0F2C22;}' +
      '.dc-pill-secondary{background:transparent;color:#ECFDF5;border:1px solid rgba(236,253,245,0.45);}' +
      '.dc-pill-bar.is-hero{bottom:74px;padding:10px 14px;}' +
      '.dc-pill-bar.is-hero .dc-pill-btn{font-size:1.06rem;padding:12px 18px;min-height:48px;}' +
      '.dc-addon-box{background:#FFFFFF;border:1px solid #E5E0D5;border-radius:14px;padding:20px;margin:20px 0;color:#111827;text-align:left;}' +
      '.dc-addon-box.is-opening{margin-top:30px;background:#FFFEFC;}' +
      '.dc-addon-kicker{font-size:0.74rem;font-weight:800;letter-spacing:0.06em;text-transform:uppercase;color:#0F2C22;margin-bottom:6px;}' +
      '.dc-addon-title{font-size:1.08rem;font-weight:800;color:#0F2C22;margin:0 0 12px;line-height:1.4;}' +
      '.dc-deliv-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:12px;}' +
      '.dc-deliv-card{background:#FAF7F2;border:1px solid #E5E0D5;border-radius:10px;padding:13px 14px;}' +
      '.dc-deliv-num{display:inline-block;font-size:0.74rem;font-weight:800;color:#0F2C22;background:#DCFCE7;padding:2px 8px;border-radius:999px;margin-bottom:6px;}' +
      '.dc-deliv-h{font-size:0.93rem;font-weight:800;color:#111827;margin:0 0 4px;line-height:1.4;}' +
      '.dc-deliv-p{font-size:0.84rem;color:#4B5563;margin:0;line-height:1.55;}' +
      '.dc-faq-wrap{margin-top:18px;padding-top:16px;border-top:1px solid #ECE7DC;}' +
      '.dc-faq-item{border-top:1px solid #ECE7DC;padding:10px 0;}' +
      '.dc-faq-item:first-of-type{border-top:none;padding-top:2px;}' +
      '.dc-faq-item summary{cursor:pointer;font-weight:700;font-size:0.92rem;color:#0F2C22;list-style:none;display:flex;justify-content:space-between;align-items:center;gap:10px;}' +
      '.dc-faq-item summary::-webkit-details-marker{display:none;}' +
      '.dc-faq-item summary::after{content:"+";font-weight:800;font-size:1.1rem;color:#0F2C22;flex-shrink:0;}' +
      '.dc-faq-item[open] summary::after{content:"-";}' +
      '.dc-faq-a{font-size:0.86rem;color:#374151;margin:8px 0 2px;line-height:1.65;}' +
      '.dc-policy-box{margin-top:14px;padding:12px 14px;border-radius:10px;background:#F8FAFC;border:1px solid #E2E8F0;font-size:0.82rem;color:#334155;line-height:1.6;}' +
      '.dc-review-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:10px;margin-top:12px;}' +
      '.dc-review-card{background:#FAF7F2;border:1px solid #E5E0D5;border-radius:10px;padding:12px;font-size:0.86rem;color:#1F2937;}' +
      '.dc-vault-ribbon{background:#FEF3C7;border:1px solid #F59E0B;color:#78350F;border-radius:8px;padding:8px 14px;font-size:0.82rem;font-weight:700;margin-bottom:14px;display:flex;align-items:center;justify-content:center;text-align:center;}' +
      '.dc-stage3-badge{display:inline-flex;align-items:center;gap:6px;padding:6px 13px;border-radius:999px;font-size:0.84rem;font-weight:800;border:1.5px solid currentColor;margin:8px 0 6px;line-height:1.35;}' +
      '.dc-stage3-green{color:#065F46;background:#ECFDF5;}' +
      '.dc-stage3-amber{color:#92400E;background:#FFFBEB;}' +
      '.dc-stage3-terra{color:#9A3412;background:#FFF7ED;}' +
      '@media(max-width:560px){.dc-pill-btn{font-size:0.78rem;padding:8px 12px;}.dc-addon-box{padding:15px 14px;}}';
    document.head.appendChild(st);
  }

  /* =========================================================================
   * 1) Bottom Floating Pill CTA Bar (Divisions 1-5 ALL)
   * ========================================================================= */
  function mountFloatingPill() {
    if (!IS_MAIN) return;
    if (document.getElementById('dcFloatingPillBar')) return;
    var cfgMap = {
      TOM: {
        pLabel: 'SMH Fear & Greed Gauge',
        pHref: '/smh-fear-greed?utm_source=floating_pill&utm_medium=web',
        sLabel: 'Free 2p Sample PDF',
        sHref: '/assets/downloads/tom_sample_2p.pdf',
        sBlank: true
      },
      KFG: {
        pLabel: 'Free 60s US CDC Check',
        pHref: '#top',
        pScroll: true,
        sLabel: 'Free 2p Sample PDF',
        sHref: '/assets/downloads/kfg_sample_2p.pdf',
        sBlank: true
      },
      GBA: {
        pLabel: 'SMH恐怖と強欲指数',
        pHref: '/jp/smh-fear-greed?utm_source=floating_pill&utm_medium=web',
        sLabel: '無料2pサンプルPDF',
        sHref: '/jp/downloads/gba_jp_sample_2p.pdf',
        sBlank: true
      },
      HERO: {
        pLabel: '🎵 \ubc31\uc6b4\ud638 6\uace1 \ubb34\ub8cc \ub4e3\uae30',
        pHref: '/stream',
        sLabel: '💐 \uce74\ud1a1 \ubb34\ub8cc \uc548\ubd80\uce74\ub4dc',
        sHref: '/vip.html',
        sBlank: false
      },
      KFK: {
        pLabel: '\uac00\uc785 \uc5c6\ub294 60\ucd08 \ubb34\ub8cc \uc9c4\ub2e8',
        pHref: '#top',
        pScroll: true,
        sLabel: '2p \ubb34\ub8cc \uc0d8\ud50c PDF',
        sHref: '/assets/downloads/kfk_sample_2p.pdf',
        sBlank: true
      }
    };
    var cfg = cfgMap[DIV] || cfgMap.TOM;
    var bar = document.createElement('div');
    bar.id = 'dcFloatingPillBar';
    bar.className = 'dc-pill-bar' + (DIV === 'HERO' ? ' is-hero' : '');
    bar.setAttribute('role', 'region');
    bar.setAttribute('aria-label', 'Quick Action Bar');
    bar.innerHTML =
      '<a class="dc-pill-btn dc-pill-primary" id="dcPillPrimaryBtn" href="' + esc(cfg.pHref) + '">' + esc(cfg.pLabel) + '</a>' +
      '<a class="dc-pill-btn dc-pill-secondary" id="dcPillSecondaryBtn" href="' + esc(cfg.sHref) + '"' + (cfg.sBlank ? ' target="_blank" rel="noopener"' : '') + '>' + esc(cfg.sLabel) + '</a>';
    document.body.appendChild(bar);

    var pBtn = document.getElementById('dcPillPrimaryBtn');
    if (pBtn && cfg.pScroll) {
      pBtn.addEventListener('click', function (ev) {
        ev.preventDefault();
        window.scrollTo({ top: 0, behavior: 'smooth' });
        if (!isInternalOrBotTraffic() && window.DreamCompanyCRM && typeof window.DreamCompanyCRM.trackFunnelEvent === 'function') {
          window.DreamCompanyCRM.trackFunnelEvent(DIV, 'floating_cta_click');
        }
      });
    } else if (pBtn) {
      pBtn.addEventListener('click', function () {
        if (!isInternalOrBotTraffic() && window.DreamCompanyCRM && typeof window.DreamCompanyCRM.trackFunnelEvent === 'function') {
          window.DreamCompanyCRM.trackFunnelEvent(DIV, 'floating_cta_click');
        }
      });
    }

    function isAnyObstructedElementInView() {
      var ae = document.activeElement;
      if (ae && (ae.tagName === 'INPUT' || ae.tagName === 'TEXTAREA' || ae.tagName === 'SELECT')) return true;
      var vh = window.innerHeight || 800;
      var sel = 'footer, .whop-checkout-button, [data-tom-paid-plan], #btn-one-tap-premium-suite, #btn-one-tap-six-month-pass, a[href*="latpeed.com"], a[href*="buy.polar.sh"], a[href*="whop.com/checkout"], #sticky-radio-player.is-playing';
      var nodes = document.querySelectorAll(sel);
      for (var i = 0; i < nodes.length; i++) {
        var el = nodes[i];
        if (!el || el.offsetParent === null) continue;
        var r = el.getBoundingClientRect();
        if (r.height > 10 && r.bottom > vh - 96 && r.top < vh) {
          return true;
        }
      }
      return false;
    }

    function updateBarVisibility() {
      var y = window.pageYOffset || document.documentElement.scrollTop || 0;
      var show = y > 360 && !isAnyObstructedElementInView();
      bar.classList.toggle('is-visible', show);
    }

    window.addEventListener('scroll', updateBarVisibility, { passive: true });
    window.addEventListener('resize', updateBarVisibility, { passive: true });
    document.addEventListener('focusin', updateBarVisibility, true);
    document.addEventListener('focusout', updateBarVisibility, true);
    setTimeout(updateBarVisibility, 700);
  }

  /* =========================================================================
   * 2) Copy Table (Zero AI Clichés, Zero Forbidden Polar/Whop/KFK Terms)
   * ========================================================================= */
  var COPY = {
    TOM: {
      delivKicker: 'WHAT YOU RECEIVE IMMEDIATELY',
      delivTitle: '3 Concrete Reference Deliverables Included',
      deliv: [
        { n: '01', h: '14-Page 2000-2025 Crisis Workbook PDF', p: 'Verified historical drawdowns and recovery months across Dot-Com, 2008, and 2022 for SMH x XLV + SGOV.' },
        { n: '02', h: 'Self-Serve Custom Dollar Worksheet', p: 'Printable allocation sheet scaled to your chosen household dollar band and 24-month Treasury reserve.' },
        { n: '03', h: '401(k) / IRA Tax-Location Study Table', p: 'Plain-English educational reference comparing taxable and tax-deferred account placement (non-advisory).' }
      ],
      faqKicker: 'BEFORE YOU DECIDE',
      faqTitle: 'Quick Answers Before Continuing',
      faqs: [
        { q: 'Can I inspect the actual data quality before paying?', a: 'Yes. Open our free 2-page 2000-2025 Sample PDF right now with zero email wall or card required.' },
        { q: 'Is this investment advice or trade timing signals?', a: 'No. Truth of Market is strictly an independent educational research publisher presenting public historical ETF statistics.' },
        { q: 'How fast do I receive my PDF after checkout?', a: 'Right after Whop checkout, plus an automatic backup email with your verified 6-digit OTP restore access.' },
        { q: 'What is the refund and cancellation policy?', a: '7-day full refund if unopened/undownloaded; 100% refund for any file or billing issue; optional recurring passes cancel anytime in 1 click.' }
      ],
      policyTitle: 'Verified Reader Review Policy (Zero Fake or Incentivized Reviews)',
      policyLines: [
        '1. Only verified paying members who authenticated their purchase can leave 1 voluntary reflection.',
        '2. Zero beta giveaways, zero sponsored posts, and zero paid or edited testimonials.',
        '3. Verified reflections appear automatically once 3 or more genuine member notes accumulate.'
      ],
      vaultRibbon: 'Personal & Household Use Only · Unauthorized Redistribution or Public Sharing Prohibited'
    },
    KFG: {
      delivKicker: 'CONCRETE PARENT DELIVERABLES',
      delivTitle: '3 Printable Reference Artifacts You Hold in Hand',
      deliv: [
        { n: '01', h: '4-Page Personalized US CDC Reference PDF', p: 'Time-adjusted bone-age math, US ft/in and lbs growth curves, and estimated adult height band.' },
        { n: '02', h: '30-Day Printable Refrigerator Checklist', p: 'Calm bedtime, dinner protein, and posture habits designed for busy weeknights — zero supplement ads.' },
        { n: '03', h: 'Pediatrician Visit Prep Sheet & Sibling Archive', p: 'Structured checkup questions plus up to 4 sibling profiles and monthly velocity tracking (Pass/Suite).' }
      ],
      faqKicker: 'PARENT PEACE-OF-MIND FAQ',
      faqTitle: 'Questions Parents Ask Before Continuing',
      faqs: [
        { q: 'Can I preview the report before paying?', a: 'Yes. Open our free 2-page US CDC Sample PDF immediately — zero email wall, zero supplement pitches.' },
        { q: 'Is this medical advice or a doctor replacement?', a: 'No. KISFIT Studio is a 100% automated, non-medical educational reference tool for adult parents (18+) built on public US CDC 2000 tables.' },
        { q: 'Does one Pass cover multiple children?', a: 'Yes. Both the 6-Month Pass ($19.99) and 12-Month Suite ($49) support up to 4 siblings under one family account.' },
        { q: 'What is your refund policy?', a: '7-day full refund if unopened/undownloaded; 100% refund for any file error or duplicate charge; zero recurring auto-billing on one-time passes.' }
      ],
      policyTitle: 'Verified Parent Review Policy (Zero Sponsored or Beta Reviews)',
      policyLines: [
        '1. Only verified Polar.sh buyers who authenticated their pass can leave 1 voluntary reflection.',
        '2. Zero beta testers, zero affiliate sponsorships, and zero fabricated reviews.',
        '3. Public parent reflections display automatically once 3+ genuine verified notes are recorded.'
      ],
      vaultRibbon: 'Family & Household Use Only · Unauthorized Redistribution or Sharing Prohibited'
    },
    GBA: {
      delivKicker: 'お手元に届く3つの実物資料',
      delivTitle: 'ご購入前に確認できる3つの具体的な成果物',
      deliv: [
        { n: '01', h: '12p 新NISA・過去25年統計ワークブックPDF', p: '2000〜2025年（ITバブル・リーマン・2022年）のSMH×XLV＋個人向け国債の客観的比較データ。' },
        { n: '02', h: '円建てセルフサービス自動計算シート', p: '成長投資枠1,200万円上限・つみたて枠600万円・特定口座の整理表をご自身の資産額で印刷保存。' },
        { n: '03', h: '楽天・SBI証券 指値注文ステップ図解', p: '50〜70代の方でも落ち着いて確認できる口座設定・指値確認手順の教育ガイド（売買推奨なし）。' }
      ],
      faqKicker: 'ご購入前のよくあるご質問',
      faqTitle: '迷いを解消するための4つの確認事項',
      faqs: [
        { q: '購入前に中身を確認できますか？', a: 'はい。メール登録不要で「無料2pサンプルPDF」を今すぐご覧いただけます。' },
        { q: '個別銘柄の売買指示や投資助言は含まれますか？', a: '一切含まれません。公開ETFの過去統計と金融庁の新NISA制度枠を整理した独立系教育出版資料です。' },
        { q: '¥1,480の買い切り版は自動更新されますか？', a: 'いいえ、1回限りの買い切りで自動更新はありません。月額・年間パスもいつでも1クリックで解約できます。' },
        { q: '返金ポリシーはどうなっていますか？', a: '未閲覧・未ダウンロード時は決済後7日以内全額返金、ファイル不具合や重複決済時は100%返金いたします。' }
      ],
      policyTitle: '認証会員ご感想の公開ポリシー（サクラ・広告レビュー0件）',
      policyLines: [
        '1. 実際に決済・認証を完了された会員様のみ1回に限り任意でご感想を投稿できます。',
        '2. 体験団募集・報酬付きレビュー・やらせ投稿は一切行っておりません。',
        '3. 実際の認証会員様のご感想が3件以上集まり次第、この欄に自動で公開されます。'
      ],
      vaultRibbon: 'ご本人・ご家族専用資料 ／ 無断転載・第三者への配布・共有禁止'
    },
    KFK: {
      delivKicker: '\uc190\uc5d0 \ubc14\ub85c \uc950\ub294 \uc2e4\ubb3c \uacb0\uacfc\ubb3c 3\uc885',
      delivTitle: '\uacb0\uc81c \uc804 \ud655\uc778\ud558\ub294 3\uac00\uc9c0 \uad6c\uccb4\uc801 \uc0b0\ucd9c\ubb3c',
      deliv: [
        { n: '01', h: '\uc544\uc774 \uc774\ub984·\ubf08\ub098\uc774 \uc2dc\ucc28(Δt) \ubc18\uc601 4p \ub9de\ucda4 PDF', p: '\uc9c8\ubcd1\uad00\ub9ac\uccad(KDCA 2017) \uacf5\uc2dd \uc131\uc7a5\ub3c4\ud45c \uae30\uc900\uc73c\ub85c \ubcf4\uc815\ud55c \uc608\uc0c1\ud0a4·\uc131\uc7a5 \ubcd1\ubaa9 \uc815\ub9ac \ubcf4\uace0\uc11c.' },
        { n: '02', h: '\uc18c\uc544\uacfc \ubc29\ubb38 \uc9c8\ubb38\uc9c0 + 30\uc77c \ub0c9\uc7a5\uace0 \uc2e4\ucc9c \ub2ec\ub825', p: '\uc9c4\ub8cc\uc2e4\uc5d0\uc11c \ubc14\ub85c \ubb3c\uc5b4\ubcfc \ud575\uc2ec \uc9c8\ubb38\uacfc \ubc24 9\uc2dc \ubc18 \uc218\uba74·\ub2e8\ubc31\uc9c8 \uc2b5\uad00 \uccb4\ud06c\ud45c\ub97c \uc778\uc1c4\uc6a9\uc73c\ub85c \uc81c\uacf5.' },
        { n: '03', h: '\uace8\ub4e0\ud0c0\uc784 \ub9c8\uc2a4\ud130\ubd81 PDF & 6~12\uac1c\uc6d4 \ud2b8\ub798\ucee4', p: '17p/20p \uc2e4\uc804 \uac00\uc774\ub4dc\uc640 \ub9e4\uc6d4 30\ucd08 \uc131\uc7a5\uc18d\ub3c4(cm/\ub144) \uc790\ub3d9 \ud310\ub3c5(\ucd5c\ub300 4\uba85 \ud615\uc81c\uc790\ub9e4 \uc9c0\uc6d0).' }
      ],
      faqKicker: '\uacb0\uc81c \uc804 \ub9c8\uc9c0\ub9c9 \uc758\uc2ec \ud574\uc18c FAQ',
      faqTitle: '\ubd80\ubaa8\ub2d8\uc774 \uac00\uc7a5 \ub9ce\uc774 \ubb3c\uc5b4\ubcf4\uc2dc\ub294 4\uac00\uc9c0',
      faqs: [
        { q: '\uacb0\uc81c \uc804\uc5d0 \uc2e4\uc81c PDF \ud488\uc9c8\uc744 \ubbf8\ub9ac \ubcfc \uc218 \uc788\ub098\uc694?', a: '\ub124. \ud68c\uc6d0\uac00\uc785\uc774\ub098 \uc774\uba54\uc77c \uc785\ub825 \uc5c6\uc774 \ubc14\ub85c \uc0c1\ub2e8·\uacb0\uacfc \ud654\uba74\uc758 2p \ubb34\ub8cc \uc0d8\ud50c PDF\ub97c \uc5f4\uc5b4 \ubcf4\uc2e4 \uc218 \uc788\uc2b5\ub2c8\ub2e4.' },
        { q: '\uc601\uc591\uc81c \uad11\uace0\ub098 \uc0c1\uc5c5\uc131 \uc81c\ud734 \ucd94\ucc9c\uc774 \ub4e4\uc5b4 \uc788\ub098\uc694?', a: '\ub2e8 1\uac74\ub3c4 \uc5c6\uc2b5\ub2c8\ub2e4. \ud0a4\uc988\ud54f\uc740 \uc9c8\ubcd1\uad00\ub9ac\uccad \uacf5\uacf5 \ub370\uc774\ud130 \uae30\ubc18 \uc21c\uc218 \uc720\ub8cc \ub9ac\ud3ec\ud2b8 \ud50c\ub7ab\ud3fc\uc73c\ub85c \uc0c1\uc5c5\uc131 \uc81c\ud734\ub97c \uc804\uba74 \ubc30\uc81c\ud569\ub2c8\ub2e4.' },
        { q: '\ub798\ud53c\ub4dc \uacb0\uc81c \ud6c4 \ub9de\ucda4 PDF\ub294 \uc5b4\ub5bb\uac8c \ubc1b\ub098\uc694?', a: '\ub798\ud53c\ub4dc \uacb0\uc81c \uc9c1\ud6c4 kidsfit.co.kr\ub85c \ub3cc\uc544\uc640 \uacb0\uc81c \uc774\uba54\uc77c\uacfc 6\uc790\ub9ac \uc778\uc99d\ucf54\ub4dc(\ub610\ub294 \uc8fc\ubb38\ucf54\ub4dc)\ub97c \uc785\ub825\ud558\uba74 \uc989\uc2dc \ubc1c\uae09\ub429\ub2c8\ub2e4.' },
        { q: '\ud658\ubd88 \uae30\uc900\uc774 \uad81\uae08\ud569\ub2c8\ub2e4.', a: '\ubbf8\uc5f4\ub78c·\ubbf8\ub2e4\uc6b4\ub85c\ub4dc \uc2dc \uacb0\uc81c \ud6c4 7\uc77c \uc774\ub0b4 \uc804\uc561 \ud658\ubd88\ub418\uba70, \ud30c\uc77c \uc624\ub958·\uc911\ubcf5 \uacb0\uc81c \uc2dc 100% \uc2e0\uc18d \ud658\ubd88\ud574 \ub4dc\ub9bd\ub2c8\ub2e4.' }
      ],
      policyTitle: '\ud22c\uba85 \ud6c4\uae30 \uac80\uc99d \uc815\ucc45 (\uccb4\ud5d8\ub2e8·\uad11\uace0 \ud6c4\uae30 0\uac74)',
      policyLines: [
        '1. \uc2e4\uc81c \uacb0\uc81c·\uc778\uc99d \uc644\ub8cc \uace0\uac1d\ub9cc 1\ud68c \uc790\ubc1c\uc801\uc73c\ub85c \uc791\uc131\ud560 \uc218 \uc788\uc2b5\ub2c8\ub2e4.',
        '2. \uccb4\ud5d8\ub2e8 \ubaa8\uc9d1·\ud560\uc778 \uc870\uac74\ubd80 \ud6c4\uae30·\ub300\ud589 \uc791\uc131 \ud6c4\uae30\ub294 0\uac74\uc785\ub2c8\ub2e4.',
        '3. \uc2e4\uc81c \uc778\uc99d \ubd80\ubaa8\ub2d8 \uc18c\uac10\uc774 3\uac74 \uc774\uc0c1 \ubaa8\uc774\uba74 \uc774 \uc601\uc5ed\uc5d0 \uc790\ub3d9 \uacf5\uac1c\ub429\ub2c8\ub2e4.'
      ],
      vaultRibbon: '1\uc778·\uac00\uc871 \uc804\uc6a9 \uc790\ub8cc · \ubb34\ub2e8 \ubc30\ud3ec \ubc0f \uc81c3\uc790 \uacf5\uc720 \uae08\uc9c0'
    }
  };

  function buildDeliverablesAndFaqEl(c, id, extraClass) {
    var wrap = document.createElement('section');
    wrap.id = id;
    wrap.className = 'dc-addon-box' + (extraClass ? (' ' + extraClass) : '');
    wrap.setAttribute('aria-label', 'Deliverables and FAQ');

    var delivHtml =
      '<div class="dc-addon-kicker">' + esc(c.delivKicker) + '</div>' +
      '<h3 class="dc-addon-title">' + esc(c.delivTitle) + '</h3>' +
      '<div class="dc-deliv-grid">' +
      c.deliv.map(function (d) {
        return (
          '<div class="dc-deliv-card">' +
          '<span class="dc-deliv-num">' + esc(d.n) + '</span>' +
          '<h4 class="dc-deliv-h">' + esc(d.h) + '</h4>' +
          '<p class="dc-deliv-p">' + esc(d.p) + '</p>' +
          '</div>'
        );
      }).join('') +
      '</div>';

    var faqHtml =
      '<div class="dc-faq-wrap">' +
      '<div class="dc-addon-kicker">' + esc(c.faqKicker) + '</div>' +
      '<h3 class="dc-addon-title">' + esc(c.faqTitle) + '</h3>' +
      c.faqs.map(function (f) {
        return (
          '<details class="dc-faq-item"><summary>' + esc(f.q) + '</summary>' +
          '<p class="dc-faq-a">' + esc(f.a) + '</p></details>'
        );
      }).join('') +
      '</div>';

    var policyHtml =
      '<div class="dc-policy-box">' +
      '<strong>' + esc(c.policyTitle) + '</strong><br>' +
      c.policyLines.map(esc).join('<br>') +
      '<div class="dc-verified-reviews-mount" style="display:none;margin-top:10px;"></div>' +
      '</div>';

    wrap.innerHTML = delivHtml + faqHtml + policyHtml;

    var details = wrap.querySelectorAll('details');
    for (var i = 0; i < details.length; i++) {
      details[i].addEventListener('toggle', function () {
        if (this.open && !isInternalOrBotTraffic() && window.DreamCompanyCRM && typeof window.DreamCompanyCRM.trackFunnelEvent === 'function') {
          window.DreamCompanyCRM.trackFunnelEvent(DIV, 'faq_open');
        }
      });
    }
    return wrap;
  }

  var __reviewsFetched = false;
  var __cachedReviewsRes = null;

  function applyReviewsToMounts(res) {
    var mounts = document.querySelectorAll('.dc-verified-reviews-mount');
    for (var i = 0; i < mounts.length; i++) {
      var mount = mounts[i];
      if (!res || !res.visible || !Array.isArray(res.reviews) || res.reviews.length < 3) {
        mount.style.display = 'none';
        continue;
      }
      mount.style.display = 'block';
      mount.innerHTML =
        '<div class="dc-review-grid">' +
        res.reviews.slice(0, 6).map(function (rv) {
          return (
            '<div class="dc-review-card">' +
            '<div style="font-weight:700;color:#0F2C22;margin-bottom:4px;">&#10003; ' + esc(rv.display_name || 'Verified') + '</div>' +
            '<div>&ldquo;' + esc(rv.comment || '') + '&rdquo;</div>' +
            '</div>'
          );
        }).join('') +
        '</div>';
    }
  }

  function hydrateVerifiedReviews() {
    if (__reviewsFetched) {
      applyReviewsToMounts(__cachedReviewsRes);
      return;
    }
    if (!window.DreamCompanyCRM || typeof window.DreamCompanyCRM.fetchVerifiedReviews !== 'function') return;
    __reviewsFetched = true;
    window.DreamCompanyCRM.fetchVerifiedReviews(DIV).then(function (res) {
      __cachedReviewsRes = res;
      applyReviewsToMounts(res);
    }).catch(function () {});
  }

  function mountDiv1235Addons() {
    if (DIV === 'HERO' || !IS_MAIN) return;
    var c = COPY[DIV];
    if (!c) return;

    // A) Always-visible Deliverables + FAQ + Review Policy directly above Paid CTAs (NEVER inside collapsed <details>)
    function tryAttachPreCheckout() {
      if (document.getElementById('dcPreCheckoutAddons')) return true;
      var anchorSelectors = {
        TOM: ['#pricing .pw-tier-grid', '.pw-tier-grid'],
        KFG: ['#kfg-proactive-growth-edge .kfg-tier-grid', '.kfg-tier-grid'],
        GBA: ['#pricing .pw-tier-grid', '.pw-tier-grid'],
        KFK: ['#kfk-latpeed-ebook-slot .pass-grid-2col', '.pass-grid-2col']
      };
      var list = anchorSelectors[DIV] || [];
      for (var i = 0; i < list.length; i++) {
        var target = document.querySelector(list[i]);
        if (target && target.parentNode && !target.closest('details')) {
          var box = buildDeliverablesAndFaqEl(c, 'dcPreCheckoutAddons', '');
          target.parentNode.insertBefore(box, target);
          hydrateVerifiedReviews();
          return true;
        }
      }
      return false;
    }

    // B) Opening Screen 0 Deliverables + FAQ + Review Policy so fresh visitors immediately verify concrete value
    function tryAttachOpeningTrust() {
      if (document.getElementById('dcOpeningTrustAddons')) return true;
      var openingSelectors = {
        TOM: '#pwScreen0',
        KFG: '#kfg-screen-0-letter',
        GBA: '#pwScreen0Jp',
        KFK: '#kfk-peer-growth-editorial'
      };
      var hostEl = document.querySelector(openingSelectors[DIV]);
      if (hostEl) {
        var box = buildDeliverablesAndFaqEl(c, 'dcOpeningTrustAddons', 'is-opening');
        hostEl.appendChild(box);
        hydrateVerifiedReviews();
        return true;
      }
      return false;
    }

    // C) Lightweight 1-Line Protection Ribbon inside Paid Vault (EXACT live IDs!)
    function tryAttachVaultRibbon() {
      var vaultSelectors = {
        TOM: ['#tomPaidScreen4Vault'],
        KFG: ['#kfg-screen-3-unlocked-dossier', '#kfg-unlocked-dossier-content'],
        GBA: ['#gbaPaidScreen4VaultJp'],
        KFK: ['#kfk-full-unlocked-report']
      };
      var list = vaultSelectors[DIV] || [];
      for (var i = 0; i < list.length; i++) {
        var v = document.querySelector(list[i]);
        if (!v) continue;
        if (!v.querySelector('.dc-vault-ribbon')) {
          var rib = document.createElement('div');
          rib.className = 'dc-vault-ribbon';
          rib.textContent = c.vaultRibbon;
          v.insertBefore(rib, v.firstChild);
        }
        break;
      }
    }

    // D) #3 1-Second Intuitive 3-Stage Status Badges (KFG, GBA, KFK ONLY — strictly excluded on TOM!)
    function tryAttachStage3Badge() {
      if (DIV === 'TOM') return;

      if (DIV === 'KFG') {
        var partialWrap = document.getElementById('kfg-partial-baseline-summary');
        if (!partialWrap || String(partialWrap.textContent || '').trim().length < 20) return;
        var pctEl =
          document.getElementById('kfg-res-percentile') ||
          partialWrap.querySelector('[data-kfg-percentile]') ||
          partialWrap.querySelector('.kfg-baseline-metrics .kfg-metric-tile:nth-child(2) .kfg-metric-value');
        var rawAttr = pctEl && pctEl.getAttribute ? pctEl.getAttribute('data-kfg-percentile') : '';
        var rawTxt = rawAttr || (pctEl ? String(pctEl.textContent || '') : String(partialWrap.textContent || ''));
        var m = rawTxt.match(/(\d+(?:\.\d+)?)/);
        var pct = m ? parseFloat(m[1]) : 50;
        var cls = pct >= 40 ? 'dc-stage3-green' : pct >= 18 ? 'dc-stage3-amber' : 'dc-stage3-terra';
        var label =
          pct >= 40
            ? 'Steady Growth Track (US CDC Guide)'
            : pct >= 18
              ? 'Sleep & Routine Tune-Up Zone'
              : 'Pediatrician Visit Prep Recommended';
        var b = document.getElementById('dcKfgStage3Badge');
        if (!b) {
          b = document.createElement('div');
          b.id = 'dcKfgStage3Badge';
          var h3 = partialWrap.querySelector('h3');
          if (h3 && h3.parentNode) h3.parentNode.insertBefore(b, h3.nextSibling);
          else partialWrap.insertBefore(b, partialWrap.firstChild);
        }
        b.className = 'dc-stage3-badge ' + cls;
        b.textContent = label;
      } else if (DIV === 'KFK') {
        var kPctEl = document.getElementById('result-free-percentile') || document.getElementById('kfk-res-percentile');
        var kCard = document.getElementById('kfk-free-summary-card');
        if (!kPctEl || !kCard) return;
        var kTxt = String(kPctEl.textContent || '');
        var km = kTxt.match(/(\d+(?:\.\d+)?)/);
        var kPct = km ? parseFloat(km[1]) : 50;
        var kCls = kPct >= 40 ? 'dc-stage3-green' : kPct >= 18 ? 'dc-stage3-amber' : 'dc-stage3-terra';
        var kLabel =
          kPct >= 40
            ? '\uc548\uc2ec \uc21c\ud56d \uad6c\uac04'
            : kPct >= 18
              ? '\ubc24 9\uc2dc \ubc18 \uc218\uba74·\uc601\uc591 \ubcf4\uac15 \uad6c\uac04'
              : '\uc18c\uc544\uacfc \ubc29\ubb38 \uc9c8\ubb38\uc9c0 \uc9c0\ucc38 \uad8c\uc7a5 \uad6c\uac04';
        var kb = document.getElementById('dcKfkStage3Badge');
        if (!kb) {
          kb = document.createElement('div');
          kb.id = 'dcKfkStage3Badge';
          var kh2 = document.getElementById('result-child-headline') || kCard.querySelector('h2');
          if (kh2 && kh2.parentNode) kh2.parentNode.insertBefore(kb, kh2.nextSibling);
          else kPctEl.parentNode.appendChild(kb);
        }
        kb.className = 'dc-stage3-badge ' + kCls;
        kb.textContent = kLabel;
      } else if (DIV === 'GBA') {
        var gRes = document.getElementById('pwFreeBaselineSummaryJp') || document.getElementById('gbaMorningClubJp');
        if (!gRes) return;
        var scaleVal = 1800;
        try {
          var saved = JSON.parse(localStorage.getItem('gba_jp_stepup_answers_v1') || '{}');
          if (saved && saved.scale) scaleVal = Number(saved.scale) || 1800;
        } catch (_) {}
        var profEl = document.getElementById('pwProfileSummaryJp');
        if (profEl) {
          var pm = String(profEl.textContent || '').replace(/,/g, '').match(/(\d+)\s*万円/);
          if (pm) scaleVal = Number(pm[1]) || scaleVal;
        }
        var gCls = scaleVal <= 1200 ? 'dc-stage3-green' : scaleVal <= 1800 ? 'dc-stage3-amber' : 'dc-stage3-terra';
        var gLabel =
          scaleVal <= 1200
            ? '新NISA 1,800万円非課税枠 最適配分'
            : scaleVal <= 1800
              ? '米国配当10%源泉徴収 認知推奨'
              : '成長投資枠1,200万円超過分 特定口座分離必須';
        var gb = document.getElementById('dcGbaStage3Badge');
        if (!gb) {
          gb = document.createElement('div');
          gb.id = 'dcGbaStage3Badge';
          var hTarget = document.getElementById('pwUnlockedRatioHeadlineJp') || gRes.querySelector('h2');
          if (hTarget && hTarget.parentNode) {
            hTarget.parentNode.insertBefore(gb, hTarget.nextSibling);
          } else {
            gRes.insertBefore(gb, gRes.firstChild);
          }
        }
        gb.className = 'dc-stage3-badge ' + gCls;
        gb.textContent = gLabel;
      }
    }

    function runAll() {
      tryAttachOpeningTrust();
      tryAttachPreCheckout();
      tryAttachVaultRibbon();
      tryAttachStage3Badge();
      mountOneTouchShareCard();
    }

    runAll();
    var timer = null;
    var obs = new MutationObserver(function () {
      if (timer) return;
      timer = setTimeout(function () {
        timer = null;
        runAll();
      }, 180);
    });
    obs.observe(document.body, { childList: true, subtree: true, attributes: true, attributeFilter: ['style', 'class'] });
  }



  /* =========================================================================
   * 5) Universal Result-Screen Top 1-Touch Share OG Card (?ref= + strip owner flags + share_click)
   * ========================================================================= */
  function buildCleanShareUrl(rawUrl, extraParams) {
    try {
      var base = String(rawUrl || (window.location ? (window.location.origin + window.location.pathname) : '')).trim();
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
          vid = window.localStorage.getItem('dc_visitor_id') || '';
          if (!vid) {
            vid = 'v_' + Math.random().toString(36).slice(2, 10) + Date.now().toString(36).slice(-4);
            window.localStorage.setItem('dc_visitor_id', vid);
          }
        }
      } catch (_v) {}
      if (vid) u.searchParams.set('ref', vid);
      if (!u.searchParams.get('utm_source')) u.searchParams.set('utm_source', 'referral');
      if (!u.searchParams.get('utm_medium')) u.searchParams.set('utm_medium', 'share');
      return u.toString();
    } catch (_e) {
      return String(rawUrl || '');
    }
  }
  window.__dcBuildCleanShareUrl = buildCleanShareUrl;

  function mountOneTouchShareCard() {
    if (document.getElementById('dcOneTouchShareCard')) return;
    if (document.getElementById('dcSeasonalToolApp') || document.getElementById('dcWinterCardsApp')) return;

    var SHARE_CFG = {
      TOM: {
        anchors: ['#pwScreen3', '#smhFgApp .fg-hero-card'],
        title: "Share Today's SMH Fear & Greed Snapshot Card",
        sub: 'Send a clean 1-tap snapshot link to your spouse or family (zero login wall).',
        btn: 'Share Snapshot Card',
        copied: 'Snapshot referral link copied! Share via text or email.',
        url: 'https://truthofmarket.com/smh-fear-greed',
        shareTitle: 'SMH Fear & Greed Snapshot | Truth of Market',
        shareText: 'Check today\'s live SMH Semiconductor Fear & Greed Index and 24-month Treasury crash study:'
      },
      KFG: {
        anchors: ['#kfg-partial-baseline-summary', '#kfg-screen-3-result', '#kfg-result-screen'],
        title: 'Share Result Card with Partner',
        sub: 'Send our US CDC height percentile & bone-age summary link to your co-parent in 1 tap.',
        btn: 'Share Result Card with Partner',
        copied: 'Clean partner share link copied! Paste in Messages or email.',
        url: 'https://kisfitglobal.com/',
        shareTitle: 'US CDC Bone-Age & Adult Height Check | KISFIT Studio',
        shareText: 'Let\'s review our child\'s US CDC height percentile and growth window together:'
      },
      GBA: {
        anchors: ['#pwFreeBaselineSummaryJp', '#smhFgApp .fg-hero-card', '#gbaMorningClubJp'],
        title: '\u672c\u65e5\u306eSMH\u6050\u6016\u6307\u6570\u30b9\u30ca\u30c3\u30d7\u30b7\u30e7\u30c3\u30c8\u3092\u5171\u6709',
        sub: 'LINE\u3084\u30e1\u30fc\u30eb\u3067\u3054\u5bb6\u65cf\u306b1\u30bf\u30c3\u30d7\u5171\u6709\u3067\u304d\u307e\u3059\uff08\u767b\u9332\u4e0d\u8981\uff09\u3002',
        btn: 'SMH\u6050\u6016\u6307\u6570\u30ab\u30fc\u30c9\u3092\u5171\u6709',
        copied: '\u5171\u6709\u30ea\u30f3\u30af\u3092\u30b3\u30d4\u30fc\u3057\u307e\u3057\u305f\uff01LINE\u3084\u30e1\u30fc\u30eb\u306b\u8cbc\u308a\u4ed8\u3051\u3066\u9001\u308c\u307e\u3059\u3002',
        url: 'https://getbreakai.com/jp/smh-fear-greed',
        shareTitle: '\u7c73\u56fd\u534a\u5c0e\u4f53SMH \u6050\u6016\u3068\u5f37\u6b32\u6307\u6570 | GetBreakAI',
        shareText: '\u672c\u65e5\u306eSMH\u6050\u6016\u6307\u6570\u3068\u65b0NISA 25\u5e74\u7d71\u8a08\u3092\u3054\u78ba\u8a8d\u304f\u3060\u3055\u3044\uff1a'
      },
      HERO: {
        anchors: ['#hero-radio-section', '#main-content .highlight-card', '#main-content'],
        title: '\uce74\uce74\uc624\ud1a1\u00b7\ubb38\uc790\ub85c \ub178\ub798\uc640 \uaf43\uce74\ub4dc \ud568\uaed8 \ubcf4\ub0b4\uae30',
        sub: '\ubc1b\ub294 \ubd84\uc774 \ub9c1\ud06c\ub97c \ub204\ub974\uba74 \uac00\uc0c1 \ud2b8\ub85c\ud2b8 \uac00\uc218 \ubc31\uc6b4\ud638 \ub178\ub798 \ud50c\ub808\uc774\uc5b4\uc640 \uaca8\uc6b8 \uaf43\uce74\ub4dc\uac00 \ubc14\ub85c \uc5f4\ub9bd\ub2c8\ub2e4.',
        btn: '\uce74\uce74\uc624\ud1a1\u00b7\ubb38\uc790\ub85c \ub178\ub798\uc640 \uaf43\uce74\ub4dc \ud568\uaed8 \ubcf4\ub0b4\uae30',
        copied: '\ub178\ub798+\uaf43\uce74\ub4dc \ub9c1\ud06c\uac00 \ubcf5\uc0ac\ub418\uc5c8\uc2b5\ub2c8\ub2e4! \uce74\uce74\uc624\ud1a1\uc774\ub098 \ubb38\uc790\uc5d0 \ubd99\uc5ec\ub123\uc5b4 \ubcf4\ub0b4\uc138\uc694.',
        url: 'https://paradise-hero.com/winter-cards?card=dongji&play=1',
        shareTitle: '\ubc31\uc6b4\ud638 \ub178\ub798\uc640 \uaca8\uc6b8 \uc548\ubd80 \uaf43\uce74\ub4dc | \uae40\uc324\uc758\uc601\uc6c5\ub77c\ub514\uc624',
        shareText: '\ub530\ub73b\ud55c \uaca8\uc6b8 \uaf43\uce74\ub4dc\uc640 \ubc31\uc6b4\ud638 \ubb34\ub8cc \ub178\ub798\ub97c \ubcf4\ub0b4\ub4dc\ub9bd\ub2c8\ub2e4:',
        isHero: true
      },
      KFK: {
        anchors: ['#kfk-free-summary-card', '#kfk-result-screen', '#result-screen'],
        title: '\uc544\uc774 \uc544\ube60\u00b7\uc5c4\ub9c8\uc5d0\uac8c \uc608\uc0c1\ud0a4 \uacb0\uacfc \uce74\ub4dc \ubcf4\ub0b4\uae30',
        sub: '\ubf08\ub098\uc774 \uc2dc\ucc28(\u0394t) \ubcf4\uc815 \uacb0\uacfc\uc640 \ub610\ub798 \ubc31\ubd84\uc704 \ub9c1\ud06c\ub97c \ubc30\uc6b0\uc790\uc5d0\uac8c 1\ud130\uce58\ub85c \uacf5\uc720\ud558\uc138\uc694.',
        btn: '\uc544\ube60\u00b7\uc5c4\ub9c8\uc5d0\uac8c \uacb0\uacfc \uce74\ub4dc \ubcf4\ub0b4\uae30',
        copied: '\uc608\uc0c1\ud0a4 \uacb0\uacfc \uacf5\uc720 \ub9c1\ud06c\uac00 \ubcf5\uc0ac\ub418\uc5c8\uc2b5\ub2c8\ub2e4! \uce74\ud1a1\uc5d0 \ubc14\ub85c \ubd99\uc5ec\ub123\uc5b4 \ubcf4\ub0b4\uc138\uc694.',
        url: 'https://kidsfit.co.kr/',
        shareTitle: '\ud0a4\uc988\ud54f \uc608\uc0c1\ud0a4 \uacb0\uacfc \uce74\ub4dc | KDCA 2017 \uc18c\uc544\uc131\uc7a5',
        shareText: '\uc6b0\ub9ac \uc544\uc774 KDCA \ud0a4 \ubc31\ubd84\uc704\uc640 \ubf08\ub098\uc774 \uc2dc\ucc28 \uc810\uac80 \uacb0\uacfc\ub97c \ud568\uaed8 \ud655\uc778\ud574 \ubd10\uc694:'
      }
    };

    var sc = SHARE_CFG[DIV];
    if (!sc) return;
    var host = null;
    for (var i = 0; i < sc.anchors.length; i++) {
      var cand = document.querySelector(sc.anchors[i]);
      if (cand) { host = cand; break; }
    }
    if (!host) return;

    var card = document.createElement('div');
    card.id = 'dcOneTouchShareCard';
    card.style.cssText = sc.isHero
      ? 'background:#0E2820;color:#FFFFFF;border:3px solid #D4AF37;border-radius:16px;padding:18px 20px;margin:0 0 18px;text-align:left;'
      : 'background:#0F2C22;color:#FFFFFF;border:1px solid #1E4638;border-radius:14px;padding:16px 18px;margin:0 0 18px;display:flex;flex-wrap:wrap;align-items:center;justify-content:space-between;gap:12px;text-align:left;';

    var titleStyle = sc.isHero ? 'font-size:22px;font-weight:900;color:#FDE68A;margin:0 0 6px;' : 'font-size:1rem;font-weight:800;color:#FAF7F2;margin:0 0 4px;';
    var subStyle = sc.isHero ? 'font-size:19px;color:#ECFDF5;margin:0 0 14px;line-height:1.55;' : 'font-size:0.84rem;color:#D1FAE5;margin:0;';
    var btnStyle = sc.isHero
      ? 'width:100%;min-height:62px;font-size:21px;font-weight:900;background:#FDE68A;color:#0E2820;border:none;border-radius:12px;cursor:pointer;padding:12px 18px;'
      : 'min-height:46px;font-size:0.92rem;font-weight:800;background:#F59E0B;color:#111827;border:none;border-radius:10px;cursor:pointer;padding:10px 18px;white-space:nowrap;';

    card.innerHTML =
      '<div style="flex:1 1 240px;">' +
        '<div style="' + titleStyle + '">' + esc(sc.title) + '</div>' +
        '<p style="' + subStyle + '">' + esc(sc.sub) + '</p>' +
      '</div>' +
      '<button type="button" id="dcOneTouchShareBtn" style="' + btnStyle + '">' + esc(sc.btn) + '</button>' +
      '<div id="dcShareToast" role="status" aria-live="polite" style="display:none;width:100%;margin-top:8px;padding:10px 12px;border-radius:8px;background:#ECFDF5;color:#065F46;font-weight:700;font-size:' + (sc.isHero ? '19px' : '0.86rem') + ';"></div>';

    host.insertBefore(card, host.firstChild);

    var shareBtn = card.querySelector('#dcOneTouchShareBtn');
    var toastEl = card.querySelector('#dcShareToast');
    if (shareBtn) {
      shareBtn.addEventListener('click', function () {
        var cleanUrl = buildCleanShareUrl(sc.url);
        shareBtn.setAttribute('data-last-share-url', cleanUrl);
        if (!isInternalOrBotTraffic() && window.DreamCompanyCRM && typeof window.DreamCompanyCRM.trackFunnelEvent === 'function') {
          window.DreamCompanyCRM.trackFunnelEvent(DIV, 'share_click', { event_meta: 'result_og_share_card' });
        }
        function showToast(msg) {
          if (!toastEl) return;
          toastEl.textContent = msg;
          toastEl.style.display = 'block';
        }
        if (navigator.share) {
          navigator.share({ title: sc.shareTitle, text: sc.shareText, url: cleanUrl }).then(function () {
            showToast(sc.copied);
          }).catch(function () {
            if (navigator.clipboard && navigator.clipboard.writeText) {
              navigator.clipboard.writeText(cleanUrl).then(function () { showToast(sc.copied); }).catch(function () { showToast(cleanUrl); });
            } else {
              showToast(cleanUrl);
            }
          });
        } else if (navigator.clipboard && navigator.clipboard.writeText) {
          navigator.clipboard.writeText(cleanUrl).then(function () { showToast(sc.copied); }).catch(function () { showToast(cleanUrl); });
        } else {
          showToast(cleanUrl);
        }
      });
    }
  }

  function boot() {
    injectStyles();
    mountFloatingPill();
    mountDiv1235Addons();
    mountOneTouchShareCard();
    setTimeout(mountOneTouchShareCard, 900);
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', boot);
  } else {
    boot();
  }
})();
