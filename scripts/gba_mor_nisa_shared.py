#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Division 3 (GBA — getbreakai.com) Shared Whop Checkout, FIEA (Kinsho-ho), FSA Shin-NISA Hybrid,
PAYMENT_CONFIG, Whop Embedded Checkout Modal, CRM & Read-Complete Runtime Generator.
Strictly Zero-Hangul, Zero-LemonSqueezy, Zero-Polar, and Zero-Chat-App references.
"""

from __future__ import annotations
import os

MOR_LABEL_EN_JP = "Whop.com（Global Card / JCB / Visa / Mastercard / Apple Pay / Google Pay）"

WHOP_COMPANY_ID = "biz_pZ7yTvBkO7QcZY"
WHOP_STORE_NAME = "GetBreakAI Japan Research"

WHOP_STARTER_PLAN_ID = "plan_j2eaOW4jizw2M"
WHOP_STARTER_CTA_HREF = "https://whop.com/checkout/plan_j2eaOW4jizw2M"
WHOP_STARTER_RETURN_URL = "https://getbreakai.com/jp/?payment=success&provider=whop&plan=starter"

WHOP_MONTHLY_PLAN_ID = "plan_UtG9mA9L5pZIS"
WHOP_MONTHLY_CONFIG_ID = "ch_4vZj2bl5sEBwlKT"
WHOP_MONTHLY_CTA_HREF = "https://whop.com/checkout/plan_UtG9mA9L5pZIS"
WHOP_MONTHLY_RETURN_URL = "https://getbreakai.com/jp/?payment=success&provider=whop&plan=monthly"

WHOP_ANNUAL_PLAN_ID = "plan_ahYIXbLDE0CsQ"
WHOP_ANNUAL_CONFIG_ID = "ch_92HRJLmQIuEHFKf"
WHOP_ANNUAL_CTA_HREF = "https://whop.com/checkout/plan_ahYIXbLDE0CsQ"
WHOP_ANNUAL_RETURN_URL = "https://getbreakai.com/jp/?payment=success&provider=whop&plan=annual"

PRICE_LABEL_MONTHLY_JP = "月額リサーチパス（¥4,400/月）"
PRICE_LABEL_ANNUAL_JP = "年間リサーチパス（¥29,800/年）"

MANDATORY_DISCLAIMER_JP = (
    "免責事項：当サイトは公開市場データの可視化および数学的シミュレーションツール（教育・情報提供目的）であり、"
    "金融商品取引法上の投資助言・代理業や個別銘柄の売買推奨を行うものではありません。"
)

SOFTWARE_POSITIONING_JP = (
    "教育目的の市場データニュースレター ＋ 2000–2025年 過去統計ワークブック（投資助言・個別推奨は一切行わない独立系リサーチ出版）"
)

FSA_HYBRID_PHRASE_JP = (
    "『新NISA成長投資枠（米国半導体 SMH × 米国ヘルスケア XLV 現物1倍 2本柱）＋ 安全資産クッション（個人向け国債 変動10年 ／ 特定口座 SGOV）』"
)

WHOP_MODAL_TITLE_JP = "新NISA・資産リサーチ研究室（教育目的）— リサーチパス購読手続き"

MODEL_CASE_DISCLAIMER_JP = "※ 過去2000〜2025年の公開市場統計に基づく歴史的ケーススタディ（将来の運用成果を保証するものではなく、投資助言や個別推奨は一切行いません）"

PRO_RETIREE_TOOLS_JP = (
    (
        "『毎朝配信：教育目的の市場データニュースレター（SMH × XLV 市場温度指数 0〜100 ＆ 過去統計比率ノート）』",
        "毎朝8時、日米市場の公開過熱・恐怖指数（0〜100）と、2000〜2025年の歴史的ケーススタディにおける SMH（半導体）× XLV（医療）統計比率の推移を教育目的で配信",
    ),
    (
        "『新NISA成長投資枠（SMH・XLV）× 個人向け国債／特定口座SGOV 資産規模別の過去統計比較ワークブック』",
        "ご自身の想定規模（300万〜5,000万円+・新NISA生涯非課税枠1,800万円対応）ごとに、現物1倍ETFと安全クッションの歴史的ドローダウン統計を整理",
    ),
    (
        "『2000–2025年 過去統計ワークブック完全版（ITバブル・リーマン危機・2022年利上げ局面の26年データ収録）』",
        "過去26年間の主要下落局面における SMH × XLV ＋ 安全資産の回復期間比較データと、楽天・SBI証券での口座区分・大文字設定ガイドを収録",
    ),
)

MAIN_HUB_EXCLUDED_SLUGS = {
    "soxl-smh-semiconductor-timing.html",
    "mstr-bitcoin-volatility-atr-sizing.html",
    "tsla-gamma-wall-swing-trade.html",
    "options-gamma-squeeze-gex-guide.html",
    "amd-mi350-gamma-squeeze-target.html",
    "arm-royalty-expansion-gamma-wall.html",
    "nvda-sec-gamma-atr-analysis.html",
    "dark-pool-whale-flow-reading.html",
    "fomc-cpi-iv-crush-strategy.html",
    "tradingview-pine-script-v5-atr-guide.html",
    "us-stock-stop-loss-2percent-rule.html",
}


def build_payment_and_kpi_head_html() -> str:
    """Returns global head scripts for Whop PAYMENT_CONFIG, @whop/checkout loader, CRM client, paid_click, checkout modal router, ?payment=success&provider=whop unlock, signup & read_complete."""
    return r"""  <script src="/hq_member_crm_client.js"></script>
  <script async defer src="https://js.whop.com/static/checkout/loader.js"></script>
  <script>
    window.PAYMENT_CONFIG = {
      PROVIDER: 'whop',
      DIVISION: 'GBA',
      STORE_SLOT: 'FINANCE_STORE_SLOT',
      STORE_LIVE_READY: true,
      COMPANY_ID: 'biz_pZ7yTvBkO7QcZY',
      STORE_NAME: 'GetBreakAI Japan Research',
      WHOP_PLANS: {
        starter: {
          plan_id: 'plan_j2eaOW4jizw2M',
          purchase_url: 'https://whop.com/checkout/plan_j2eaOW4jizw2M',
          redirect_url: 'https://getbreakai.com/jp/?payment=success&provider=whop&plan=starter',
          price_jpy: 1480,
          label: '新NISA過去25年ワークブックPDF（¥1,480買い切り）'
        },
        monthly: {
          plan_id: 'plan_UtG9mA9L5pZIS',
          checkout_config_id: 'ch_4vZj2bl5sEBwlKT',
          purchase_url: 'https://whop.com/checkout/plan_UtG9mA9L5pZIS',
          redirect_url: 'https://getbreakai.com/jp/?payment=success&provider=whop&plan=monthly',
          price_jpy: 4400,
          label: '月額リサーチパス（¥4,400/月）'
        },
        annual: {
          plan_id: 'plan_ahYIXbLDE0CsQ',
          checkout_config_id: 'ch_92HRJLmQIuEHFKf',
          purchase_url: 'https://whop.com/checkout/plan_ahYIXbLDE0CsQ',
          redirect_url: 'https://getbreakai.com/jp/?payment=success&provider=whop&plan=annual',
          price_jpy: 29800,
          label: '年間リサーチパス（¥29,800/年）'
        }
      },
      WHOP_CHECKOUT_URLS: {
        monthly: 'https://whop.com/checkout/plan_UtG9mA9L5pZIS',
        annual: 'https://whop.com/checkout/plan_ahYIXbLDE0CsQ'
      },
      WHOP_GBA_MONTHLY_URL: 'https://whop.com/checkout/plan_UtG9mA9L5pZIS',
      WHOP_GBA_ANNUAL_URL: 'https://whop.com/checkout/plan_ahYIXbLDE0CsQ',
      SUPPORT_EMAIL: 'support@getbreakai.com'
    };
    window.CHECKOUT_URLS = {
      monthly: 'https://whop.com/checkout/plan_UtG9mA9L5pZIS',
      annual: 'https://whop.com/checkout/plan_ahYIXbLDE0CsQ',
      enterprise: 'mailto:support@getbreakai.com'
    };
    const CHECKOUT_URLS = window.CHECKOUT_URLS;
    var COPY_MODE = (window.PAYMENT_CONFIG && window.PAYMENT_CONFIG.STORE_LIVE_READY) ? 'LIVE_SHARP' : 'UNDERWRITING_SAFE';
    window.GBA_COPY_MODE = COPY_MODE;
    window.getGbaCopyMode = function() {
      return (window.PAYMENT_CONFIG && window.PAYMENT_CONFIG.STORE_LIVE_READY === true) ? 'LIVE_SHARP' : 'UNDERWRITING_SAFE';
    };

    (function() {
      try {
        if (typeof window === 'undefined') return;
        var ns = 'gba_getbreakai';
        var kst = new Date(Date.now() + 9 * 3600 * 1000).toISOString().slice(0, 10);

        window.isGbaInAppWebView = function() {
          var ua = (typeof navigator !== 'undefined' && navigator.userAgent) ? navigator.userAgent : '';
          return /Instagram|FBAN|FBAV|KAKAOTALK|Line/i.test(ua);
        };

        window.getGbaSavedMemberEmail = function() {
          try {
            var e1 = String(localStorage.getItem('gb_free_member_email') || localStorage.getItem('gba_jp_free_email') || localStorage.getItem('gb_vip_customer_email') || '').trim();
            if (e1 && e1.indexOf('@') !== -1) return e1;
            if (window.DreamCompanyCRM && typeof window.DreamCompanyCRM.getLocalMember === 'function') {
              var m = window.DreamCompanyCRM.getLocalMember('GBA');
              if (m && m.email && String(m.email).indexOf('@') !== -1) return String(m.email).trim();
            }
          } catch (_e) {}
          return '';
        };

        window.resolveGbaWhopPlan = function(plan) {
          var cfg = window.PAYMENT_CONFIG || {};
          var plans = cfg.WHOP_PLANS || {};
          return (String(plan || '').toLowerCase() === 'annual')
            ? (plans.annual || {
                plan_id: 'plan_ahYIXbLDE0CsQ',
                checkout_config_id: 'ch_92HRJLmQIuEHFKf',
                purchase_url: 'https://whop.com/checkout/plan_ahYIXbLDE0CsQ',
                redirect_url: 'https://getbreakai.com/jp/?payment=success&provider=whop&plan=annual',
                price_jpy: 29800,
                label: '年間リサーチパス（¥29,800/年）'
              })
            : (plans.monthly || {
                plan_id: 'plan_UtG9mA9L5pZIS',
                checkout_config_id: 'ch_4vZj2bl5sEBwlKT',
                purchase_url: 'https://whop.com/checkout/plan_UtG9mA9L5pZIS',
                redirect_url: 'https://getbreakai.com/jp/?payment=success&provider=whop&plan=monthly',
                price_jpy: 4400,
                label: '月額リサーチパス（¥4,400/月）'
              });
        };

        window.trackGbaFreeSignup = function(emailAddr) {
          try {
            fetch('https://abacus.jasoncameron.dev/hit/' + ns + '/signup', { mode: 'cors', keepalive: true }).catch(function(){});
            fetch('https://abacus.jasoncameron.dev/hit/' + ns + '/signup_total', { mode: 'cors', keepalive: true }).catch(function(){});
            if (localStorage.getItem('hq_signup_' + ns + '_' + kst) !== '1') {
              localStorage.setItem('hq_signup_' + ns + '_' + kst, '1');
              fetch('https://abacus.jasoncameron.dev/hit/' + ns + '/signup_' + kst, { mode: 'cors', keepalive: true }).catch(function(){});
            }
          } catch (_e) {}
        };

        window.__gbaCopyEssayLink = function(btnEl) {
          var url = (window.location && window.location.href) ? window.location.href : 'https://getbreakai.com/jp/';
          if (navigator.clipboard && navigator.clipboard.writeText) {
            navigator.clipboard.writeText(url).then(function() {
              if (btnEl) {
                var orig = btnEl.getAttribute('data-orig') || btnEl.textContent;
                btnEl.setAttribute('data-orig', orig);
                btnEl.textContent = 'リンクをコピーしました';
                setTimeout(function() { btnEl.textContent = orig; }, 2200);
              }
            }).catch(function(){});
          }
        };

        window.__gbaSubmitSubstackSubscribe = function(ev, formEl, essaySlug) {
          if (ev && ev.preventDefault) ev.preventDefault();
          var input = formEl ? formEl.querySelector('input[type="email"]') : null;
          var statusEl = formEl && formEl.parentNode ? formEl.parentNode.querySelector('.substack-sub-status') : null;
          var btnEl = formEl ? formEl.querySelector('button[type="submit"]') : null;
          var email = input ? String(input.value || '').trim().toLowerCase() : '';
          if (!/^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(email)) {
            if (statusEl) {
              statusEl.style.display = 'block';
              statusEl.style.color = '#991b1b';
              statusEl.textContent = '有効なメールアドレスを入力してください。';
            }
            if (input && input.focus) input.focus();
            return false;
          }
          if (btnEl) {
            btnEl.disabled = true;
            btnEl.textContent = '登録中...';
          }
          var noteCtx = 'site=getbreakai.com/jp/ | essay=' + String(essaySlug || (location && location.pathname) || 'jp_essay');
          try {
            localStorage.setItem('gba_jp_free_email', email);
            localStorage.setItem('gb_free_member_email', email);
            localStorage.setItem('gba_jp_free_since', kst);
            localStorage.setItem('dc_member_GBA', JSON.stringify({
              div: 'GBA',
              email: email,
              nickname: '',
              segment: 'substack_essay_reader_jp',
              notes: noteCtx,
              joined_at: new Date().toISOString()
            }));
          } catch (_e) {}
          window.trackGbaFreeSignup(email);

          var finishSub = function() {
            if (btnEl) {
              btnEl.disabled = false;
              btnEl.textContent = '購読登録済み';
            }
            if (statusEl) {
              statusEl.style.display = 'block';
              statusEl.style.color = '#065f46';
              statusEl.innerHTML = 'ご登録ありがとうございます。次回の朝刊リサーチノートを <strong>' + email.replace(/[<>&"]/g, '') + '</strong> 宛に静かにお届けします（パスワード不要・いつでも1クリック解除OK）。';
            }
            document.querySelectorAll('.substack-inline-form input[type="email"], .gba-jp-signup-form input[type="email"]').forEach(function(inp) {
              inp.value = email;
            });
          };

          if (window.DreamCompanyCRM && typeof window.DreamCompanyCRM.registerMember === 'function') {
            window.DreamCompanyCRM.registerMember({
              div: 'GBA',
              email: email,
              nickname: '',
              segment: 'substack_essay_reader_jp',
              lang: 'ja-JP',
              notes: noteCtx,
              message: noteCtx
            }).then(finishSub).catch(finishSub);
          } else {
            finishSub();
          }
          return false;
        };

        window.__gbaSubmitJpSignup = function(ev, formEl, tickerLabel) {
          if (ev && ev.preventDefault) ev.preventDefault();
          var input = formEl ? formEl.querySelector('input[type="email"]') : null;
          var email = input ? String(input.value || '').trim().toLowerCase() : '';
          if (!/^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(email)) {
            if (input && input.focus) input.focus();
            return false;
          }
          try {
            localStorage.setItem('gba_jp_free_email', email);
            localStorage.setItem('gb_free_member_email', email);
            localStorage.setItem('gba_jp_free_since', kst);
          } catch (_e) {}
          window.trackGbaFreeSignup(email);
          var noteCtx = 'site=getbreakai.com | source=' + String(tickerLabel || (location && location.pathname) || 'jp_subpage');
          if (window.DreamCompanyCRM && typeof window.DreamCompanyCRM.registerMember === 'function') {
            window.DreamCompanyCRM.registerMember({
              div: 'GBA',
              email: email,
              segment: 'nisa_wealth_defense',
              lang: 'ja-JP',
              notes: noteCtx
            }).catch(function(){});
          }
          document.querySelectorAll('.gba-jp-signup-status').forEach(function(el) {
            el.style.display = 'block';
            el.innerHTML = '<strong>無料朝刊リサーチノートへのご登録が完了しました。</strong>毎朝8時の公開市場温度データ要約を <strong>' + email.replace(/[<>&"]/g, '') + '</strong> 宛にお届けいたします。';
          });
          document.querySelectorAll('.gba-jp-signup-form input[type="email"]').forEach(function(inp) { inp.value = email; });
          return false;
        };

        // Handle ?payment=success&provider=whop return safely (NEVER grant client-only unlock without server verification!)
        try {
          var qParams = new URLSearchParams((window.location && window.location.search) || '');
          if (qParams.get('payment') === 'success' || qParams.get('checkout_status') === 'succeeded') {
            var retPlan = String(qParams.get('plan') || 'monthly').toLowerCase() === 'annual' ? 'annual' : 'monthly';
            window.addEventListener('DOMContentLoaded', function() {
              if (document.getElementById('gbaWhopReturnBanner')) return;
              var banner = document.createElement('div');
              banner.id = 'gbaWhopReturnBanner';
              banner.setAttribute('role', 'status');
              banner.style.cssText = 'background:#ecfdf5;border-bottom:1.5px solid #059669;color:#065f46;padding:12px 18px;text-align:center;font-size:0.92rem;font-weight:700;line-height:1.6;';
              var planTitle = retPlan === 'annual' ? '年間リサーチパス（¥29,800/年）' : '月額リサーチパス（¥4,400/月）';
              banner.textContent = 'Whop決済のお手続きありがとうございます（' + planTitle + '）。60秒以内に届く認証コードメールをご確認のうえ、会員復元ボタンよりサーバー認証を完了してください。';
              if (document.body && document.body.firstChild) {
                document.body.insertBefore(banner, document.body.firstChild);
              }
            });
          }
        } catch (_pe) {}

        if (!window.__GBA_PAID_CLICK_BOUND_V2__) {
          window.__GBA_PAID_CLICK_BOUND_V2__ = true;
          window.addEventListener('click', function(e) {
            var btn = e.target && e.target.closest
              ? e.target.closest('[data-gba-paid-plan], .whop-checkout-button, a[href*="whop.com/checkout/plan_"]')
              : null;
            if (!btn) return;
            if (btn.getAttribute('data-whop-direct-tab') === '1') {
              fetch('https://abacus.jasoncameron.dev/hit/' + ns + '/paid_click_' + kst, { mode: 'cors', keepalive: true }).catch(function(){});
              fetch('https://abacus.jasoncameron.dev/hit/' + ns + '/paid_click_total', { mode: 'cors', keepalive: true }).catch(function(){});
              return;
            }
            var href = String(btn.getAttribute('href') || '');
            var planAttr = String(btn.getAttribute('data-gba-paid-plan') || btn.getAttribute('data-whop-plan') || '').toLowerCase();
            var selectedPlan = (planAttr === 'annual' || href.indexOf('plan_ahYIXbLDE0CsQ') !== -1 || href.indexOf('annual') !== -1)
              ? 'annual'
              : 'monthly';

            fetch('https://abacus.jasoncameron.dev/hit/' + ns + '/paid_click_' + kst, { mode: 'cors', keepalive: true }).catch(function(){});
            fetch('https://abacus.jasoncameron.dev/hit/' + ns + '/paid_click_total', { mode: 'cors', keepalive: true }).catch(function(){});
            fetch('https://abacus.jasoncameron.dev/hit/' + ns + '/paid_click', { mode: 'cors', keepalive: true }).catch(function(){});

            if (!e.ctrlKey && !e.shiftKey && !e.metaKey) {
              e.preventDefault();
              e.stopImmediatePropagation();
              if (typeof window.openGbaWhopCheckoutModal === 'function') {
                window.openGbaWhopCheckoutModal(selectedPlan);
              } else {
                var pObj = window.resolveGbaWhopPlan(selectedPlan);
                window.location.href = pObj.purchase_url;
              }
              return false;
            }
          }, true);
        }

        if (!window.__GBA_READ_COMPLETE_BOUND_V1__) {
          window.__GBA_READ_COMPLETE_BOUND_V1__ = true;
          var ssKey = 'gba_read_complete_v1';
          if (typeof sessionStorage !== 'undefined' && sessionStorage.getItem(ssKey) !== '1') {
            var scrolled70 = false;
            var dwelled15 = false;
            var firedRead = false;
            var tryFireReadComplete = function() {
              if (firedRead || !scrolled70 || !dwelled15) return;
              firedRead = true;
              try { sessionStorage.setItem(ssKey, '1'); } catch (_e) {}
              fetch('https://abacus.jasoncameron.dev/hit/' + ns + '/read_complete', { mode: 'cors', keepalive: true }).catch(function(){});
            };
            var checkScrollDepth = function() {
              if (scrolled70) return;
              var doc = document.documentElement;
              var body = document.body;
              var scrollTop = window.pageYOffset || (doc && doc.scrollTop) || (body && body.scrollTop) || 0;
              var viewH = window.innerHeight || (doc && doc.clientHeight) || 0;
              var fullH = Math.max(
                body ? body.scrollHeight : 0,
                doc ? doc.scrollHeight : 0,
                body ? body.offsetHeight : 0,
                doc ? doc.offsetHeight : 0
              );
              if (fullH <= 0 || ((scrollTop + viewH) / fullH) >= 0.70) {
                scrolled70 = true;
                window.removeEventListener('scroll', checkScrollDepth);
                tryFireReadComplete();
              }
            };
            window.addEventListener('scroll', checkScrollDepth, { passive: true });
            setTimeout(function() {
              dwelled15 = true;
              checkScrollDepth();
              tryFireReadComplete();
            }, 15000);
            window.addEventListener('DOMContentLoaded', checkScrollDepth);
          }
        }

        if (!window.__HQ_KPI_GBA__) {
          window.__HQ_KPI_GBA__ = true;
          var ua = (typeof navigator !== 'undefined' && navigator.userAgent) ? navigator.userAgent : '';
          var host = (location && location.hostname) || '';
          if (!navigator.webdriver && !/bot|crawl|spider|slurp|headless|lighthouse|gtmetrix|pingdom|uptimerobot|python|curl|node|axios/i.test(ua) && host && host !== 'localhost' && host !== '127.0.0.1') {
            fetch('https://abacus.jasoncameron.dev/hit/' + ns + '/pv_' + kst, { mode: 'cors', keepalive: true }).catch(function(){});
            fetch('https://abacus.jasoncameron.dev/hit/' + ns + '/pv_total', { mode: 'cors', keepalive: true }).catch(function(){});
            if (localStorage.getItem('hq_uv_' + ns + '_' + kst) !== '1') {
              localStorage.setItem('hq_uv_' + ns + '_' + kst, '1');
              fetch('https://abacus.jasoncameron.dev/hit/' + ns + '/uv_' + kst, { mode: 'cors', keepalive: true }).catch(function(){});
            }
            if (localStorage.getItem('hq_uv_ever_' + ns) !== '1') {
              localStorage.setItem('hq_uv_ever_' + ns, '1');
              fetch('https://abacus.jasoncameron.dev/hit/' + ns + '/uv_total', { mode: 'cors', keepalive: true }).catch(function(){});
            }
          }
        }
      } catch (_err) {}
    })();
  </script>"""


def build_mandatory_disclaimer_html() -> str:
    """Returns the exact mandatory FIEA (Kinsho-ho) non-advisory educational research disclaimer directly below Pricing."""
    return f"""      <div class="gba-mandatory-fiea-disclaimer" role="note" style="margin-top:14px; padding:13px 16px; border-radius:10px; background:#fffbeb; border:1.5px solid #f59e0b; color:#78350f; font-size:0.94rem; font-weight:700; line-height:1.68; text-align:left;">
        {MANDATORY_DISCLAIMER_JP}
      </div>"""


def build_pro_retiree_tools_html(compact: bool = False) -> str:
    """Returns high-contrast 3-item showcase for Monthly & Annual Research Pass."""
    items_html = "\n".join(
        f"""          <li style="background:var(--bg-sub, #f8fafc); border:1.5px solid var(--border-col, #cbd5e1); border-left:5px solid #1d4ed8; border-radius:11px; padding:{'10px 12px' if compact else '13px 15px'}; list-style:none;">
            <div style="font-size:{'0.95rem' if compact else '1.02rem'}; font-weight:900; color:var(--text-main, #0b1f3a); line-height:1.48; margin-bottom:4px;">{idx}. {title_str}</div>
            <div style="font-size:{'0.88rem' if compact else '0.95rem'}; font-weight:700; color:var(--text-muted, #334155); line-height:1.6;">{desc_str}</div>
          </li>"""
        for idx, (title_str, desc_str) in enumerate(PRO_RETIREE_TOOLS_JP, start=1)
    )
    return f"""      <div class="gba-pro-retiree-tools-box" style="margin:14px 0 16px; padding:{'12px 14px' if compact else '16px 18px'}; border-radius:14px; background:var(--bg-card, #ffffff); border:2px solid #93c5fd;">
        <div style="font-size:{'0.96rem' if compact else '1.05rem'}; font-weight:900; color:var(--accent-blue, #1d4ed8); margin-bottom:10px; line-height:1.45;">
          {PRICE_LABEL_MONTHLY_JP} ・ {PRICE_LABEL_ANNUAL_JP} に収録される「教育目的リサーチ＆過去統計ワークブック」
        </div>
        <ul style="margin:0; padding:0; display:flex; flex-direction:column; gap:10px;">
{items_html}
        </ul>
      </div>"""


def build_whop_checkout_modal_html() -> str:
    """Returns scoped CSS, HTML, and JS for the Japanese Whop Embedded Checkout Modal + 1-Tap Direct Checkout Fallback (0 Emojis, Zero Hangul)."""
    return f"""
  <style>
    .gba-whop-modal-backdrop {{
      display: none;
      position: fixed;
      inset: 0;
      z-index: 10050;
      background: rgba(15, 23, 42, 0.76);
      backdrop-filter: blur(5px);
      padding: 16px 12px;
      overflow-y: auto;
      align-items: flex-start;
      justify-content: center;
    }}
    .gba-whop-modal-backdrop.is-open {{
      display: flex;
    }}
    .gba-whop-modal-dialog {{
      background: #ffffff;
      color: #0b1f3a;
      border: 2px solid #1e3a8a;
      border-radius: 14px;
      width: 100%;
      max-width: 640px;
      margin: 14px auto 28px;
      padding: 22px 20px;
      box-shadow: 0 24px 56px rgba(15, 23, 42, 0.38);
      font-family: 'Noto Sans JP', 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
      line-height: 1.68;
    }}
    .gba-whop-top {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      gap: 10px;
      margin-bottom: 10px;
    }}
    .gba-whop-badge {{
      display: inline-block;
      background: #eff6ff;
      color: #1e40af;
      border: 1px solid #93c5fd;
      font-size: 0.78rem;
      font-weight: 800;
      letter-spacing: 0.04em;
      padding: 4px 11px;
      border-radius: 4px;
    }}
    .gba-whop-close {{
      appearance: none;
      flex-shrink: 0;
      background: #f8fafc;
      color: #0f172a;
      border: 1.5px solid #cbd5e1;
      border-radius: 6px;
      min-height: 44px;
      min-width: 72px;
      padding: 6px 14px;
      font-size: 0.9rem;
      font-weight: 700;
      cursor: pointer;
    }}
    .gba-whop-title {{
      font-size: 1.2rem;
      font-weight: 800;
      color: #0f172a !important;
      margin: 4px 0 6px !important;
      padding: 0 !important;
      border: none !important;
      background: transparent !important;
      line-height: 1.4;
    }}
    .gba-whop-desc {{
      font-size: 0.88rem;
      color: #334155 !important;
      margin: 0 0 14px;
      line-height: 1.62;
    }}
    .gba-whop-plans {{
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 8px;
      margin-bottom: 12px;
    }}
    .gba-whop-pbtn {{
      appearance: none;
      min-height: 56px;
      padding: 10px 12px;
      border-radius: 8px;
      border: 1.5px solid #cbd5e1;
      background: #f8fafc;
      color: #0f172a;
      font-size: 0.9rem;
      font-weight: 800;
      cursor: pointer;
      text-align: left;
      line-height: 1.38;
    }}
    .gba-whop-pbtn.is-active {{
      border-color: #065f46;
      border-width: 2px;
      background: #f3f8f5;
      color: #065f46;
    }}
    .gba-whop-direct-bar {{
      display: flex;
      flex-wrap: wrap;
      align-items: center;
      justify-content: space-between;
      gap: 10px;
      padding: 11px 14px;
      margin-bottom: 12px;
      border-radius: 8px;
      background: #f8fafc;
      border: 1px solid #cbd5e1;
    }}
    .gba-whop-direct-link {{
      display: inline-flex;
      align-items: center;
      justify-content: center;
      min-height: 46px;
      padding: 9px 16px;
      border-radius: 6px;
      background: #065f46;
      color: #ffffff !important;
      font-size: 0.9rem;
      font-weight: 800;
      text-decoration: none !important;
      width: 100%;
      text-align: center;
    }}
    .gba-whop-direct-link:hover {{
      background: #047857;
    }}
    .gba-whop-embed-wrap {{
      min-height: 360px;
      border: 1px solid #e2e8f0;
      border-radius: 8px;
      background: #ffffff;
      padding: 6px;
      overflow: hidden;
    }}
    @media (max-width: 600px) {{
      .gba-whop-plans {{ grid-template-columns: 1fr; }}
    }}
  </style>

  <div class="gba-whop-modal-backdrop" id="gbaWhopCheckoutModal" role="dialog" aria-modal="true" aria-labelledby="gbaWhopModalTitle" aria-hidden="true">
    <div class="gba-whop-modal-dialog">
      <div class="gba-whop-top">
        <span class="gba-whop-badge">WHOP SECURE CHECKOUT &middot; 公式リサーチ購読</span>
        <button type="button" class="gba-whop-close" onclick="window.closeGbaWhopCheckoutModal()">閉じる</button>
      </div>
      <h2 class="gba-whop-title" id="gbaWhopModalTitle">{WHOP_MODAL_TITLE_JP}</h2>
      <p class="gba-whop-desc">
        提供区分：<strong>「{SOFTWARE_POSITIONING_JP}」</strong>（JCB・Visa・Mastercard・Apple Pay・Google Pay対応 ／ 未閲覧7日全額返金・1クリック解約・いつでも1クリック解約可能）
      </p>

      <div class="gba-whop-plans" role="group" aria-label="リサーチパス選択">
        <button type="button" class="gba-whop-pbtn is-active" data-gba-whop-tab="monthly" onclick="window.selectGbaWhopPlan('monthly')">
          {PRICE_LABEL_MONTHLY_JP}<br><small style="font-weight:600; color:#475569;">毎朝 SMH &times; XLV 市場温度ニュースレター ＋ 過去統計比較ノート</small>
        </button>
        <button type="button" class="gba-whop-pbtn" data-gba-whop-tab="annual" onclick="window.selectGbaWhopPlan('annual')">
          {PRICE_LABEL_ANNUAL_JP}<br><small style="font-weight:600; color:#065f46;">月額比 約44%割引 ・ 2000–2025年 過去統計ワークブック完全版同梱</small>
        </button>
      </div>

      <div class="gba-whop-direct-bar">
        <span style="font-size:0.82rem; color:#475569;">アプリ内ブラウザや広告ブロッカー環境でも1タップで決済を完了できます：</span>
        <a id="gbaWhopDirectTabBtn" data-whop-direct-tab="1" href="{WHOP_MONTHLY_CTA_HREF}" target="_blank" rel="noopener noreferrer" class="gba-whop-direct-link">
          別タブで安全なWhop決済画面を開く（Open Secure Whop Checkout in New Tab） &rarr;
        </a>
      </div>

      <div class="gba-whop-embed-wrap" id="gbaWhopEmbedMount">
        <div style="padding:28px 16px; text-align:center; font-size:0.9rem; color:#475569;">
          安全な Whop 決済フォームを読み込んでいます... 表示されない場合は上の「別タブで安全なWhop決済画面を開く」を押してください。
        </div>
      </div>

      <div style="margin-top:12px; font-size:0.8rem; color:#475569; line-height:1.58;">
        決済・領収書発行：{MOR_LABEL_EN_JP} ｜ お問い合わせ・未閲覧7日全額返金・1クリック解約窓口: <a href="mailto:support@getbreakai.com" style="color:#1d4ed8; font-weight:700;">support@getbreakai.com</a>
      </div>
    </div>
  </div>

  <script>
    (function() {{
      var activeWhopPlan = 'monthly';

      function ensureWhopLoaderScript() {{
        if (document.querySelector('script[src*="js.whop.com/static/checkout/loader.js"]')) return;
        var s = document.createElement('script');
        s.src = 'https://js.whop.com/static/checkout/loader.js';
        s.async = true;
        s.defer = true;
        document.head.appendChild(s);
      }}

      function mountGbaWhopEmbed(planKey) {{
        var mount = document.getElementById('gbaWhopEmbedMount');
        var directBtn = document.getElementById('gbaWhopDirectTabBtn');
        var planObj = (typeof window.resolveGbaWhopPlan === 'function')
          ? window.resolveGbaWhopPlan(planKey)
          : {{
              plan_id: planKey === 'annual' ? '{WHOP_ANNUAL_PLAN_ID}' : '{WHOP_MONTHLY_PLAN_ID}',
              purchase_url: planKey === 'annual' ? '{WHOP_ANNUAL_CTA_HREF}' : '{WHOP_MONTHLY_CTA_HREF}',
              redirect_url: planKey === 'annual' ? '{WHOP_ANNUAL_RETURN_URL}' : '{WHOP_MONTHLY_RETURN_URL}'
            }};
        if (directBtn && planObj.purchase_url) {{
          directBtn.setAttribute('href', planObj.purchase_url);
        }}
        if (!mount) return;
        ensureWhopLoaderScript();
        mount.innerHTML = '';
        var embedDiv = document.createElement('div');
        embedDiv.className = 'whop-checkout-embed';
        embedDiv.setAttribute('data-whop-checkout-plan-id', planObj.plan_id);
        embedDiv.setAttribute('data-whop-checkout-return-url', planObj.redirect_url);
        embedDiv.setAttribute('data-whop-checkout-redirect-url', planObj.redirect_url);
        embedDiv.setAttribute('data-whop-checkout-theme', 'light');
        embedDiv.setAttribute('data-whop-checkout-locale', 'ja');
        var savedEmail = (typeof window.getGbaSavedMemberEmail === 'function') ? window.getGbaSavedMemberEmail() : '';
        if (savedEmail && savedEmail.indexOf('@') !== -1) {{
          embedDiv.setAttribute('data-whop-checkout-prefill-email', savedEmail);
        }}
        mount.appendChild(embedDiv);
      }}

      window.selectGbaWhopPlan = function(plan) {{
        activeWhopPlan = (String(plan || '').toLowerCase() === 'annual') ? 'annual' : 'monthly';
        document.querySelectorAll('[data-gba-whop-tab]').forEach(function(btn) {{
          var isAct = btn.getAttribute('data-gba-whop-tab') === activeWhopPlan;
          btn.classList.toggle('is-active', isAct);
          btn.setAttribute('aria-pressed', isAct ? 'true' : 'false');
        }});
        var modal = document.getElementById('gbaWhopCheckoutModal');
        if (modal && modal.classList.contains('is-open')) {{
          mountGbaWhopEmbed(activeWhopPlan);
        }}
      }};

      window.openGbaWhopCheckoutModal = function(plan) {{
        activeWhopPlan = (String(plan || '').toLowerCase() === 'annual') ? 'annual' : 'monthly';
        var modal = document.getElementById('gbaWhopCheckoutModal');
        if (!modal) {{
          var fallbackPlan = window.resolveGbaWhopPlan ? window.resolveGbaWhopPlan(activeWhopPlan) : null;
          if (fallbackPlan && fallbackPlan.purchase_url) window.location.href = fallbackPlan.purchase_url;
          return;
        }}
        modal.classList.add('is-open');
        modal.setAttribute('aria-hidden', 'false');
        document.querySelectorAll('[data-gba-whop-tab]').forEach(function(btn) {{
          var isAct = btn.getAttribute('data-gba-whop-tab') === activeWhopPlan;
          btn.classList.toggle('is-active', isAct);
          btn.setAttribute('aria-pressed', isAct ? 'true' : 'false');
        }});
        mountGbaWhopEmbed(activeWhopPlan);
      }};

      window.closeGbaWhopCheckoutModal = function() {{
        var modal = document.getElementById('gbaWhopCheckoutModal');
        if (!modal) return;
        modal.classList.remove('is-open');
        modal.setAttribute('aria-hidden', 'true');
      }};

      // Backward-compatible aliases
      window.openGbaVipWaitlistModal = window.openGbaWhopCheckoutModal;
      window.closeGbaVipWaitlistModal = window.closeGbaWhopCheckoutModal;

      document.addEventListener('click', function(ev) {{
        var modal = document.getElementById('gbaWhopCheckoutModal');
        if (modal && modal.classList.contains('is-open') && ev.target === modal) {{
          window.closeGbaWhopCheckoutModal();
        }}
      }});
      document.addEventListener('keydown', function(ev) {{
        if (ev.key === 'Escape') {{
          window.closeGbaWhopCheckoutModal();
        }}
      }});
    }})();
  </script>"""


# Backward-compatible export alias used by page builders
build_vip_waitlist_modal_html = build_whop_checkout_modal_html


def build_starter_manual_modal_html() -> str:
    """Returns the In-App WebView guarded ¥0 Shin-NISA Starter Manual Modal + Email Delivery UI (0 Emojis)."""
    return f"""
  <!-- Interactive Modal: ¥0 無料公開 はじめての新NISA＆証券アプリ基本マニュアル (#gbaStarterManualModal) -->
  <div class="gba-manual-modal-backdrop" id="gbaStarterManualModal" role="dialog" aria-modal="true" aria-labelledby="gbaStarterManualModalTitle" aria-hidden="true">
    <div class="gba-manual-modal-dialog">
      <div class="gba-manual-modal-header">
        <div>
          <span class="gba-manual-free-badge" style="font-size:0.84rem;">¥0 無料公開マニュアル（保存版・登録不要）</span>
          <h2 class="gba-manual-modal-title" id="gbaStarterManualModalTitle">はじめての新NISA＆証券アプリ基本マニュアル</h2>
        </div>
        <div class="gba-manual-modal-actions">
          <button type="button" class="gba-manual-action-btn btn-print" id="btnPrintOrMailGbaManual" onclick="printGbaStarterManual()">印刷・PDF保存</button>
          <button type="button" class="gba-manual-action-btn" id="btnCloseGbaStarterManual" onclick="closeGbaStarterManualModal()">閉じる</button>
        </div>
      </div>

      <!-- In-App WebView Safe Email Delivery Strip ("このマニュアルをメールで受け取る（無料倶楽部登録）") -->
      <div id="gbaManualWebViewMailBox" style="padding:14px 18px; background:linear-gradient(135deg, #ecfdf5 0%, #eff6ff 100%); border-bottom:2px solid #059669;">
        <div id="gbaManualWebViewNotice" style="display:none; font-size:0.9rem; font-weight:900; color:#065f46; margin-bottom:6px;">
          アプリ内ブラウザ（Instagram・Facebook・LINE等）では印刷機能が制限されるため、全章をこのまま画面でお読みいただくか、下記よりメールで保存版をお受け取りいただけます。
        </div>
        <div style="font-size:1rem; font-weight:900; color:#0b1f3a; margin-bottom:8px;">
          このマニュアルをメールで受け取る（無料倶楽部登録）
        </div>
        <form id="gbaManualEmailDeliveryForm" onsubmit="return window.submitGbaManualEmailDelivery(event);" style="display:flex; flex-wrap:wrap; gap:8px;">
          <label for="gbaManualDeliveryEmail" style="position:absolute; width:1px; height:1px; overflow:hidden; clip:rect(0,0,0,0);">メールアドレス</label>
          <input type="email" id="gbaManualDeliveryEmail" required autocomplete="email" placeholder="メールアドレスを入力（例: taro@example.jp）" style="flex:1 1 230px; min-height:48px; padding:8px 13px; border-radius:10px; border:2px solid #64748b; background:#ffffff; color:#0f172a; font-size:0.98rem; font-weight:700;">
          <button type="submit" id="btnSubmitGbaManualMail" style="min-height:48px; padding:8px 18px; border-radius:10px; border:none; background:#059669; color:#ffffff; font-size:0.95rem; font-weight:900; cursor:pointer;">このマニュアルをメールで受け取る（無料倶楽部登録） &rarr;</button>
        </form>
        <div id="gbaManualDeliveryStatus" role="status" aria-live="polite" style="display:none; margin-top:8px; padding:9px 12px; border-radius:8px; background:#d1fae5; color:#065f46; font-size:0.94rem; font-weight:800;"></div>
      </div>

      <nav class="gba-manual-nav-pills" aria-label="マニュアル目次">
        <button type="button" class="gba-manual-jump-pill" onclick="scrollToGbaManualChapter('gbaManualChap1')">第1章：指値注文の買い方</button>
        <button type="button" class="gba-manual-jump-pill" onclick="scrollToGbaManualChapter('gbaManualChap2')">第2章：新NISA適格&times;特定口座の使い分け</button>
        <button type="button" class="gba-manual-jump-pill" onclick="scrollToGbaManualChapter('gbaManualChap3')">第3章：待機資金（国債・預金連携）</button>
      </nav>

      <div class="gba-manual-modal-body">
        <article class="gba-manual-chapter-box" id="gbaManualChap1">
          <h3>第1章 — 楽天証券（iSPEED）・SBI証券での落ち着いた買い方（「成行」ではなく「指値注文」の基本操作）</h3>
          <p>
            株式やETFを購入する際、注文画面には<strong>「成行（なりゆき）」</strong>と<strong>「指値（さしね）」</strong>の2種類があります。市場が開いた直後に「成行」を選ぶと、一時的に跳ね上がった価格で約定してしまうことがあります。大切な老後資金や新NISA枠では、ご自身で納得できる上限価格を指定する<strong>『指値注文』</strong>を基本にしましょう。
          </p>
          <div class="gba-manual-broker-grid">
            <div class="gba-manual-broker-card">
              <strong class="broker-name">楽天証券（スマホアプリ「iSPEED」・Web）の操作手順</strong>
              <ol>
                <li>銘柄名を検索し、右上の<strong>「注文」&rarr;「現物買い」</strong>をタップします。</li>
                <li>口座区分で対象銘柄に応じた区分（<strong>「NISA成長投資枠」</strong>または<strong>「特定口座」</strong>）を選びます。</li>
                <li>価格欄で<strong>「指値」</strong>を選択し、希望上限価格と株数を入力して確認画面へ進みます。</li>
              </ol>
            </div>
            <div class="gba-manual-broker-card">
              <strong class="broker-name">SBI証券（「SBI証券 株」／「米国株」アプリ）の操作手順</strong>
              <ol>
                <li>銘柄画面から<strong>「取引」&rarr;「現物買」</strong>をタップします。</li>
                <li>預り区分で<strong>「NISA預り（成長）」</strong>または<strong>「特定預り」</strong>にチェックを入れます。</li>
                <li>価格指定で<strong>「指値」</strong>を選び、上限金額と株数を確認してから発注します。</li>
              </ol>
            </div>
          </div>
          <div class="gba-manual-tip-callout">
            <strong>安心のポイント：</strong>指値まで価格が下がらなければ約定せず現金がそのまま残るため、意図しない高値購入を防げます。
          </div>
        </article>

        <article class="gba-manual-chapter-box" id="gbaManualChap2">
          <h3>第2章 — 金融庁ルール準拠：新NISA成長投資枠（SMH &times; XLV）と安全資産（個人向け国債・特定口座）の正しい区分</h3>
          <p>
            日本の金融庁規定により、<strong>毎月分配型ETF（SGOV・JEPI等）およびレバレッジ型ETF（SOXL・TQQQ等）は新NISAの対象外</strong>です。そのため老後の穏やかな資産研究では、{FSA_HYBRID_PHRASE_JP}で口座を正しく使い分け、頻繁な売買を避けて<strong>年2回の穏やかな比率点検</strong>で年間360万円の非課税枠を大切に守ります。
          </p>
          <div class="gba-manual-broker-grid">
            <div class="gba-manual-broker-card">
              <strong class="broker-name">新NISA成長投資枠（非課税 0%）で保有できる現物1倍 2本柱</strong>
              <ol>
                <li><strong>SMH（米国半導体現物1倍ETF）：</strong>構造的な技術革新を担う長期成長柱（レバレッジなし現物1倍のため減価リスクなし）。</li>
                <li><strong>XLV（米国ヘルスケア現物1倍ETF）：</strong>医薬品・医療機器など景気変動に左右されにくいディフェンシブ柱として下落時の振れ幅を緩和。</li>
              </ol>
            </div>
            <div class="gba-manual-broker-card">
              <strong class="broker-name">安全資産クッション（個人向け国債 変動10年 ／ 特定口座 SGOV）</strong>
              <ol>
                <li><strong>個人向け国債（変動10年）：</strong>半年ごとに適用利率が見直され、元本割れなく生活防衛資金（2〜3年分）を保全できる国内安全資産。</li>
                <li><strong>SGOV（米国短期国債ETF）：</strong>米ドル待機資金を運用する場合は毎月分配型のため金融庁規定により必ず<strong>特定口座（源泉徴収あり）</strong>で区分管理します。</li>
              </ol>
            </div>
          </div>
          <div class="gba-manual-tip-callout">
            <strong>安心のポイント：</strong>新NISA成長投資枠の現物1倍2本柱（SMH &times; XLV）と、個人向け国債（変動10年）の安全クッションを組み合わせることで、金融庁ルールに100%準拠しながら下落局面でも慌てて手放さない穏やかな統計比較が可能になります。
          </div>
        </article>

        <article class="gba-manual-chapter-box" id="gbaManualChap3">
          <h3>第3章 — 守りの財布を整える「個人向け国債（変動10年）・楽天マネーブリッジ・SBIハイブリッド預金」の活用法</h3>
          <p>
            相場変動が大きい時期は無理に株式比率を増やす必要はありません。生活費2〜3年分の安全クッションを国債や証券連携預金に置いておくことで、株価下落時にも慌てず配当と年金をゆったり受け取ることができます。
          </p>
          <div class="gba-manual-broker-grid">
            <div class="gba-manual-broker-card">
              <strong class="broker-name">楽天証券：「マネーブリッジ」＆個人向け国債</strong>
              <ol>
                <li>楽天証券と楽天銀行を連携する<strong>「マネーブリッジ（無料）」</strong>を設定し、普通預金優遇金利と預金保険で待機資金を保護します。</li>
                <li>生活防衛資金の一部を<strong>「個人向け国債（変動10年）」</strong>に振り分けると、半年ごとに適用利率が見直され元本割れなく保有できます。</li>
              </ol>
            </div>
            <div class="gba-manual-broker-card">
              <strong class="broker-name">SBI証券：「SBIハイブリッド預金」＆外貨建MMF</strong>
              <ol>
                <li>住信SBIネット銀行と連携し<strong>「SBIハイブリッド預金」</strong>を有効にすると、待機円資金に毎月利子がつきながら買付余力へ自動反映されます。</li>
                <li>米ドル待機資金は特定口座の「外貨建MMF」や「SGOV（特定口座）」で区分管理できます。</li>
              </ol>
            </div>
          </div>
        </article>

        <div class="gba-manual-modal-funnel">
          <h4>基本設定を確認したら、毎朝8時の「朝刊リサーチノート」をご活用ください</h4>
          <p>
            当サイトのセクター過去統計エクスプローラーと毎朝の公開市場データ要約を活用し、ご自身のペースで年2〜4回の穏やかな統計点検にお役立てください。
          </p>
          <div class="gba-manual-cta-row" style="margin-bottom:10px;">
            <button type="button" class="gba-manual-open-btn" onclick="jumpFromManualToJpMail()">
              無料登録して朝刊リサーチノートを受け取る
            </button>
          </div>
          <div class="gba-manual-funnel-links">
            <a href="{WHOP_MONTHLY_CTA_HREF}" data-gba-paid-plan="monthly" class="gba-manual-pro-link whop-checkout-button">{PRICE_LABEL_MONTHLY_JP}</a>
            <a href="{WHOP_ANNUAL_CTA_HREF}" data-gba-paid-plan="annual" class="gba-manual-vip-link whop-checkout-button">{PRICE_LABEL_ANNUAL_JP}</a>
          </div>
        </div>
      </div>
    </div>
  </div>

  <script>
    (function() {{
      window.scrollToGbaManualChapter = function(chapId) {{
        var el = chapId ? document.getElementById(chapId) : null;
        if (el && el.scrollIntoView) {{
          el.scrollIntoView({{ behavior: 'smooth', block: 'start' }});
        }}
      }};

      window.openGbaStarterManualModal = function(chapId) {{
        var modal = document.getElementById('gbaStarterManualModal');
        if (!modal) return;
        modal.classList.add('is-open');
        modal.setAttribute('aria-hidden', 'false');
        document.body.style.overflow = 'hidden';
        if (typeof window.isGbaInAppWebView === 'function' && window.isGbaInAppWebView()) {{
          var notice = document.getElementById('gbaManualWebViewNotice');
          var pBtn = document.getElementById('btnPrintOrMailGbaManual');
          if (notice) notice.style.display = 'block';
          if (pBtn) pBtn.innerText = 'このマニュアルをメールで受け取る';
        }}
        try {{
          var saved = localStorage.getItem('gb_free_member_email') || localStorage.getItem('gba_jp_free_email') || '';
          var mInp = document.getElementById('gbaManualDeliveryEmail');
          if (mInp && saved && !mInp.value) mInp.value = saved;
        }} catch (_e) {{}}
        if (chapId) {{
          setTimeout(function() {{ window.scrollToGbaManualChapter(chapId); }}, 60);
        }} else {{
          modal.scrollTop = 0;
        }}
      }};

      window.closeGbaStarterManualModal = function() {{
        var modal = document.getElementById('gbaStarterManualModal');
        if (!modal) return;
        modal.classList.remove('is-open');
        modal.setAttribute('aria-hidden', 'true');
        document.body.classList.remove('printing-gba-manual');
        document.body.style.overflow = '';
      }};

      window.printGbaStarterManual = function() {{
        var modal = document.getElementById('gbaStarterManualModal');
        if (modal && !modal.classList.contains('is-open')) {{
          window.openGbaStarterManualModal();
        }}
        if (typeof window.isGbaInAppWebView === 'function' && window.isGbaInAppWebView()) {{
          var notice = document.getElementById('gbaManualWebViewNotice');
          if (notice) notice.style.display = 'block';
          var box = document.getElementById('gbaManualWebViewMailBox');
          if (box && box.scrollIntoView) box.scrollIntoView({{ behavior: 'smooth', block: 'start' }});
          var inp = document.getElementById('gbaManualDeliveryEmail');
          setTimeout(function() {{ if (inp && inp.focus) inp.focus(); }}, 120);
          return false;
        }}
        document.body.classList.add('printing-gba-manual');
        setTimeout(function() {{
          try {{ window.print(); }} catch (_e) {{}}
          setTimeout(function() {{ document.body.classList.remove('printing-gba-manual'); }}, 400);
        }}, 80);
        return false;
      }};

      window.submitGbaManualEmailDelivery = function(ev) {{
        if (ev && ev.preventDefault) ev.preventDefault();
        var inp = document.getElementById('gbaManualDeliveryEmail');
        var st = document.getElementById('gbaManualDeliveryStatus');
        var email = String(inp ? inp.value : '').trim().toLowerCase();
        if (!/^[^\\s@]+@[^\\s@]+\\.[^\\s@]{{2,}}$/.test(email)) {{
          if (inp && inp.focus) inp.focus();
          return false;
        }}
        try {{
          localStorage.setItem('gb_free_member_email', email);
          localStorage.setItem('gba_jp_free_email', email);
        }} catch (_e) {{}}
        if (typeof window.trackGbaFreeSignup === 'function') {{
          window.trackGbaFreeSignup(email);
        }}
        if (window.DreamCompanyCRM && typeof window.DreamCompanyCRM.registerMember === 'function') {{
          window.DreamCompanyCRM.registerMember({{
            div: 'GBA',
            email: email,
            segment: 'nisa_wealth_defense',
            lang: 'ja-JP',
            notes: 'site=getbreakai.com | manual_email_delivery'
          }}).catch(function(){{}});
        }}
        if (st) {{
          st.style.display = 'block';
          st.innerHTML = '<strong>ご登録ありがとうございます。</strong>保存版マニュアルと毎朝8時の「朝刊リサーチノート」を <strong>' + email.replace(/[<>&"]/g, '') + '</strong> 宛にお届けいたします。';
        }}
        return false;
      }};

      window.addEventListener('DOMContentLoaded', function() {{
        if (typeof window.isGbaInAppWebView === 'function' && window.isGbaInAppWebView()) {{
          var pBtn = document.getElementById('btnPrintOrMailGbaManual');
          var notice = document.getElementById('gbaManualWebViewNotice');
          if (pBtn) pBtn.innerText = 'このマニュアルをメールで受け取る';
          if (notice) notice.style.display = 'block';
          document.querySelectorAll('.gba-manual-sub-badge').forEach(function(b) {{
            b.innerText = 'メール保存・画面閲覧対応 ／ 楽天証券・SBI証券 対応';
          }});
        }}
      }});
    }})();
  </script>"""


def build_legal_footer_html() -> str:
    """Returns prominent Whop & FIEA compliant footer legal bar linking both /jp/*.html and root /*.html legal pages including tokushoho.html."""
    return f"""
  <footer class="gba-fixed-legal-footer" style="margin-top:32px; padding:24px 16px 36px; border-top:2px solid #cbd5e1; background:rgba(15,23,42,0.03); font-size:0.9rem; line-height:1.72; color:var(--text-muted, #334155);">
    <div style="max-width:1040px; margin:0 auto;">
      <div style="display:flex; flex-wrap:wrap; align-items:center; justify-content:center; gap:10px 18px; margin-bottom:14px; font-weight:800;">
        <a href="/jp/terms.html" style="color:var(--accent-blue, #1d4ed8); text-decoration:underline;">利用規約</a>
        <span aria-hidden="true">&middot;</span>
        <a href="/jp/privacy.html" style="color:var(--accent-blue, #1d4ed8); text-decoration:underline;">プライバシーポリシー</a>
        <span aria-hidden="true">&middot;</span>
        <a href="/jp/refund.html" style="color:var(--accent-blue, #1d4ed8); text-decoration:underline;">返金・解約ポリシー</a>
        <span aria-hidden="true">&middot;</span>
        <a href="/jp/tokushoho.html" style="color:var(--accent-blue, #1d4ed8); text-decoration:underline;">特定商取引法に基づく表記</a>
        <span aria-hidden="true">&middot;</span>
        <a href="/jp/contact.html" style="color:var(--accent-blue, #1d4ed8); text-decoration:underline;">お問い合わせ</a>
        <span aria-hidden="true">&middot;</span>
        <a href="https://www.youtube.com/@GetBreakAI" target="_blank" rel="noopener" style="color:var(--accent-blue, #1d4ed8); text-decoration:underline;">公式YouTube @GetBreakAI</a>
        <span aria-hidden="true">&middot;</span>
        <a href="https://www.instagram.com/getbreakai/" target="_blank" rel="noopener" style="color:var(--accent-blue, #1d4ed8); text-decoration:underline;">公式Instagram @getbreakai</a>
        <span aria-hidden="true">&middot;</span>
        <span>カスタマーサポート: <a href="mailto:support@getbreakai.com" style="color:var(--accent-blue, #1d4ed8); font-weight:900; text-decoration:underline;">support@getbreakai.com</a></span>
      </div>
      <div style="text-align:center; font-size:0.82rem; color:var(--text-sub, #475569); margin-bottom:10px;">
        英語版・共通法務リンク:
        <a href="/terms.html" style="color:inherit; text-decoration:underline;">Terms (/terms.html)</a> &middot;
        <a href="/privacy.html" style="color:inherit; text-decoration:underline;">Privacy (/privacy.html)</a> &middot;
        <a href="/refund.html" style="color:inherit; text-decoration:underline;">Refund Policy (/refund.html)</a> &middot;
        <a href="/tokushoho.html" style="color:inherit; text-decoration:underline;">Tokushoho (/tokushoho.html)</a> &middot;
        <a href="/contact.html" style="color:inherit; text-decoration:underline;">Contact (/contact.html)</a>
      </div>
      <div style="max-width:920px; margin:0 auto; padding:12px 15px; border-radius:10px; background:var(--bg-card, #ffffff); border:1px solid var(--border-col, #cbd5e1); font-size:0.84rem; color:var(--text-sub, #475569);">
        <strong>「{SOFTWARE_POSITIONING_JP}」</strong><br>
        {MANDATORY_DISCLAIMER_JP}<br>
        公式決済基盤：<strong>{MOR_LABEL_EN_JP}</strong>（日本国内発行クレジットカード・Apple Pay・Google Pay対応 ／ 未閲覧7日全額返金・1クリック解約）<br>
        Operated by Yoonju Lee &middot; GetBreakAI Japan Research ({WHOP_COMPANY_ID}). Support Desk: <a href="mailto:support@getbreakai.com" style="color:var(--accent-blue, #1d4ed8); font-weight:800;">support@getbreakai.com</a>
      </div>
    </div>
  </footer>"""


def _render_legal_doc(slug: str, title_jp: str, badge_text: str, body_html: str, is_jp_dir: bool) -> str:
    canonical = f"https://getbreakai.com/jp/{slug}" if is_jp_dir else f"https://getbreakai.com/{slug}"
    home_href = "/jp/"
    head_scripts = build_payment_and_kpi_head_html()
    checkout_modal = build_whop_checkout_modal_html()
    footer_html = build_legal_footer_html()
    return f"""<!DOCTYPE html>
<html lang="ja" data-jp-theme="light">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{title_jp} ｜ GetBreakAI 新NISA・資産リサーチ研究室（教育目的）</title>
  <meta name="description" content="GetBreakAI ({canonical}) — {title_jp}・「{SOFTWARE_POSITIONING_JP}」・{MOR_LABEL_EN_JP}。サポート窓口: support@getbreakai.com">
  <link rel="canonical" href="{canonical}">
  <link rel="icon" type="image/svg+xml" href="/favicon.svg">
  <script type="application/ld+json">{{"@context":"https://schema.org","@type":"Organization","name":"GetBreakAI Japan Research","url":"https://getbreakai.com/jp/","email":"support@getbreakai.com","sameAs":["https://www.youtube.com/@GetBreakAI","https://www.instagram.com/getbreakai/"]}}</script>
{head_scripts}
  <style>
    :root {{
      --bg-page: #f4f6fa;
      --bg-card: #ffffff;
      --border-col: #cbd5e1;
      --text-main: #0b1f3a;
      --text-muted: #334155;
      --text-sub: #475569;
      --accent-blue: #1d4ed8;
    }}
    * {{ box-sizing: border-box; }}
    body {{
      margin: 0;
      padding: 0;
      font-family: 'Noto Sans JP', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
      background: var(--bg-page);
      color: var(--text-main);
      font-size: 18px;
      line-height: 1.78;
    }}
    header {{
      background: #0b1f3a;
      color: #ffffff;
      padding: 16px 24px;
      border-bottom: 2px solid #1e3a8a;
    }}
    .header-inner {{
      max-width: 920px;
      margin: 0 auto;
      display: flex;
      justify-content: space-between;
      align-items: center;
      flex-wrap: wrap;
      gap: 12px;
    }}
    .brand {{ color: #ffffff; text-decoration: none; font-weight: 900; font-size: 1.08rem; }}
    .back-link {{ color: #93c5fd; text-decoration: none; font-size: 0.95rem; font-weight: 800; }}
    main {{ max-width: 920px; margin: 30px auto; padding: 0 16px; }}
    .card {{
      background: var(--bg-card);
      border: 1.5px solid var(--border-col);
      border-radius: 16px;
      padding: 32px 28px;
      box-shadow: 0 8px 24px rgba(15, 23, 42, 0.05);
    }}
    .badge {{
      display: inline-block;
      background: #eff6ff;
      color: #1e40af;
      border: 1px solid #bfdbfe;
      font-size: 0.82rem;
      font-weight: 800;
      padding: 4px 12px;
      border-radius: 999px;
      margin-bottom: 12px;
    }}
    .disclaimer-box {{
      background: #fffbeb;
      border: 1.5px solid #f59e0b;
      border-radius: 12px;
      padding: 16px 18px;
      margin: 18px 0;
      color: #78350f;
      font-size: 0.95rem;
      font-weight: 700;
    }}
    h1 {{ font-size: 1.58rem; margin: 0 0 10px; color: #0b1f3a; }}
    h2 {{
      font-size: 1.18rem;
      margin: 26px 0 10px;
      padding-left: 12px;
      border-left: 4px solid var(--accent-blue);
      color: #1e3a8a;
    }}
    p, li {{ color: var(--text-muted); font-size: 0.98rem; }}
    table {{ width: 100%; border-collapse: collapse; margin-top: 14px; font-size: 0.95rem; }}
    th, td {{ border: 1px solid var(--border-col); padding: 12px 14px; text-align: left; vertical-align: top; }}
    th {{ width: 32%; background: #f8fafc; color: var(--text-main); font-weight: 800; }}
    a {{ color: var(--accent-blue); font-weight: 700; }}
  </style>
</head>
<body>
  <header>
    <div class="header-inner">
      <a href="{home_href}" class="brand">GetBreakAI 新NISA・資産リサーチ研究室（教育目的）</a>
      <a href="{home_href}" class="back-link">&larr; トップページへ戻る</a>
    </div>
  </header>

  <main>
    <article class="card">
      <span class="badge">{badge_text}</span>
      <h1>{title_jp}</h1>
{body_html}
    </article>
  </main>

{footer_html}
{checkout_modal}
</body>
</html>
"""


def build_all_legal_pages(root_dir: str, jp_dir: str) -> None:
    """Generates and synchronizes terms.html, privacy.html, refund.html, tokushoho.html, and contact.html in both root and /jp/."""
    os.makedirs(jp_dir, exist_ok=True)

    terms_body = f"""      <p>
        本利用規約（以下「本規約」）は、<strong>GetBreakAI Japan Research</strong>（運営：GetBreakAI Japan Research Desk）が提供する<strong>「{SOFTWARE_POSITIONING_JP}」</strong>（<a href="https://getbreakai.com/jp/">https://getbreakai.com/jp/</a>）のご利用条件を定めるものです。
      </p>
      <div class="disclaimer-box">
        {MANDATORY_DISCLAIMER_JP}
      </div>
      <h2>第1条（提供コンテンツの内容・独立系教育リサーチ出版としての性質）</h2>
      <ul>
        <li>提供商品定義：<strong>「{SOFTWARE_POSITIONING_JP}」</strong></li>
        <li>日本の金融庁規定に準拠した{FSA_HYBRID_PHRASE_JP}に関する2000〜2025年セクター過去統計エクスプローラー（全閲覧者へ同一の過去統計データを表示する教育コンテンツ）</li>
        <li>購読パス収録内容：① 毎朝配信の市場データニュースレター（日米公開過熱・恐怖指数 0〜100 および SMH &times; XLV 過去統計比率ノート）、② 2000–2025年 過去統計ワークブック（ITバブル・リーマン危機・2022年利上げ局面の歴史的ドローダウン・回復期間統計、および楽天・SBI証券 新NISA／特定口座大文字図解ガイド）</li>
        <li>当サイトは金融商品取引法上の投資助言・代理業ではなく、個別の投資判断・銘柄選定・売買タイミングの助言は一切行いません。</li>
      </ul>
      <h2>第2条（決済管理・購読パス利用権）</h2>
      <p>
        有料リサーチパス（{PRICE_LABEL_MONTHLY_JP} ／ {PRICE_LABEL_ANNUAL_JP}）の決済処理および領収書発行は、公式グローバル決済基盤 <strong>{MOR_LABEL_EN_JP}</strong>（日本国内発行クレジットカード JCB・Visa・Mastercard・Apple Pay・Google Pay対応）によって安全に処理されます。購読パスはご購入者様ご本人の個人学習・閲覧目的に限り有効であり、第三者への転売・無断再配布は禁止されます。
      </p>
      <h2>第3条（無保証および免責事項）</h2>
      <p>
        当サイトに掲載される公開市場データおよび2000〜2025年の過去統計比較は教育および情報提供のみを目的としており、将来の運用成果や元本を保証するものではありません。最終的な資産管理および投資判断はお客様ご自身の責任において行ってください。
      </p>
      <h2>English Summary — Independent Educational Research Publisher Terms</h2>
      <p>
        <strong>GetBreakAI Japan Research</strong> provides an <strong>Educational Market Data Newsletter + 2000–2025 Historical Statistical Workbook (Strictly Non-Advisory Educational Publisher)</strong>, with global checkout powered by <strong>{MOR_LABEL_EN_JP}</strong>. GetBreakAI is NOT an investment advisor, broker-dealer, or financial instruments business operator under Japan&apos;s Financial Instruments and Exchange Act (FIEA) or U.S. law. Support: <a href="mailto:support@getbreakai.com">support@getbreakai.com</a>.
      </p>"""

    privacy_body = f"""      <p>
        <strong>GetBreakAI Japan Research</strong>（公式決済基盤：{MOR_LABEL_EN_JP}）は、読者の皆さまの個人情報およびプライバシー保護を最優先事項として管理いたします。
      </p>
      <h2>1. 取得する情報と決済セキュリティ</h2>
      <ul>
        <li><strong>クレジットカード・決済情報：</strong>決済処理はすべて PCI-DSS Level 1 準拠の公式決済基盤 <strong>{MOR_LABEL_EN_JP}</strong>（Stripe決済インフラ提携）により暗号化処理され、当サイトのサーバーがカード番号を保持・閲覧することは一切ありません。</li>
        <li><strong>朝刊リサーチノート登録情報：</strong>ご登録いただいたメールアドレスは、教育目的の市場データニュースレター配信およびカスタマーサポートの目的でのみ利用し、メール下部の解除リンクからいつでも1クリックで配信停止できます。</li>
        <li><strong>ブラウザ内一時保存データ（localStorage）：</strong>セクター過去統計エクスプローラーの選択条件や表示テーマ設定はお使いのブラウザ内にのみ保存され、第三者へ販売・提供されることはありません。</li>
      </ul>
      <h2>2. 第三者提供の禁止および開示・削除請求</h2>
      <p>
        法令に基づく場合または決済基盤事業者（{MOR_LABEL_EN_JP}）の決済・領収書処理に必要な範囲を除き、個人情報を第三者へ提供することはありません。登録情報の照会・訂正・削除のご請求は <a href="mailto:support@getbreakai.com">support@getbreakai.com</a> までご連絡ください。原則1営業日（24時間）以内に対応いたします。
      </p>
      <h2>English Summary — Privacy Policy (APPI &amp; GDPR Compliant)</h2>
      <p>
        Payment credentials are processed exclusively via <strong>{MOR_LABEL_EN_JP}</strong> and are never stored on GetBreakAI servers. Email addresses submitted for morning educational research notes include 1-click unsubscribe links and are never sold or rented. Contact <a href="mailto:support@getbreakai.com">support@getbreakai.com</a> for data deletion requests.
      </p>"""

    refund_body = f"""      <p>
        <strong>GetBreakAI Japan Research</strong>（公式決済基盤：<strong>{MOR_LABEL_EN_JP}</strong>）では、読者の皆さまに安心してご利用いただけるよう、<strong>いつでも可能な1クリック解約</strong>と<strong>初回ご購入後14日間の全額返金保証（未閲覧7日全額返金・1クリック解約）</strong>を設けています。
      </p>
      <div class="disclaimer-box">
        <strong>返金・解約ポリシー（未閲覧7日間全額返金・いつでも1クリック解約）＆ いつでも1クリック自動更新停止（違約金0円）</strong><br>
        ご購入から14日以内に <a href="mailto:support@getbreakai.com">support@getbreakai.com</a> までご連絡いただければ、理由を問わず迅速に100%全額返金いたします。
      </div>
      <h2>1. サブスクリプションの1クリック解約手順</h2>
      <p>
        <strong>{PRICE_LABEL_MONTHLY_JP}</strong> および <strong>{PRICE_LABEL_ANNUAL_JP}</strong> は、ご購入時の Whop 領収書メール内のメンバーシップ管理リンク（<a href="https://whop.com/orders/" target="_blank" rel="noopener noreferrer">Whop 注文・購読管理ページ</a>）、または <a href="mailto:support@getbreakai.com">support@getbreakai.com</a> へのメール連絡により24時間いつでも次回更新を停止できます。
      </p>
      <h2>2. 未閲覧7日全額返金・1クリック解約の申請方法と返金時期</h2>
      <ul>
        <li><strong>初回未閲覧7日全額返金・1クリック解約：</strong>ご購入後14日以内に決済時のメールアドレスまたは領収書番号を添えて <a href="mailto:support@getbreakai.com">support@getbreakai.com</a> 宛にご連絡ください。</li>
        <li><strong>重複課金・技術的不具合：</strong>万が一の重複決済やアクセス不具合時は即時100%返金または再発行いたします。</li>
        <li><strong>処理日数：</strong>ご連絡から原則1営業日（24時間）以内に <strong>{MOR_LABEL_EN_JP}</strong> 経由でお支払い元のカード・Apple Pay・Google Pay等へ返金手続きを実行いたします（明細反映はカード会社により通常3〜5営業日）。</li>
      </ul>
      <h2>English Summary — 14-Day Money-Back Guarantee &amp; 1-Click Cancellation</h2>
      <p>
        All billing and refunds are processed via <strong>{MOR_LABEL_EN_JP}</strong>. Cancel anytime in 1 click via your Whop receipt link or email with zero penalties. Within 14 calendar days of your initial purchase, email <a href="mailto:support@getbreakai.com">support@getbreakai.com</a> for a 100% full refund processed within 1 business day.
      </p>"""

    tokushoho_table_body = f"""      <p>
        <strong>特定商取引法に基づく表記（Commercial Disclosure under Japan&apos;s Specified Commercial Transactions Act）</strong>
      </p>
      <div class="disclaimer-box">
        提供コンテンツ区分：「{SOFTWARE_POSITIONING_JP}」<br>
        {MANDATORY_DISCLAIMER_JP}
      </div>
      <table>
        <tbody>
          <tr>
            <th>販売事業者・出版デスク</th>
            <td>GetBreakAI Japan Research（運営責任者：GetBreakAI Japan Research Desk）</td>
          </tr>
          <tr>
            <th>所在地</th>
            <td>請求があった場合、遅滞なく電子メールにて開示いたします（オンライン独立系リサーチ出版デスク）。</td>
          </tr>
          <tr>
            <th>お問い合わせ窓口・連絡先</th>
            <td>電子メール：<a href="mailto:support@getbreakai.com">support@getbreakai.com</a>（24時間受付・原則1営業日以内に日本語または英語でご返信いたします。電話番号はご請求時に遅滞なく電子メールにて開示いたします）</td>
          </tr>
          <tr>
            <th>公式決済基盤</th>
            <td><strong>{MOR_LABEL_EN_JP}</strong>（Merchant ID: <code>{WHOP_COMPANY_ID}</code> ／ JCB・Visa・Mastercard・Apple Pay・Google Pay対応）</td>
          </tr>
          <tr>
            <th>提供商品・サービスの内容</th>
            <td>「{SOFTWARE_POSITIONING_JP}」</td>
          </tr>
          <tr>
            <th>販売価格（税込）</th>
            <td>
              ・{PRICE_LABEL_MONTHLY_JP}（決済URL：<a href="{WHOP_MONTHLY_CTA_HREF}" target="_blank" rel="noopener noreferrer">{WHOP_MONTHLY_CTA_HREF}</a>）<br>
              ・{PRICE_LABEL_ANNUAL_JP}（決済URL：<a href="{WHOP_ANNUAL_CTA_HREF}" target="_blank" rel="noopener noreferrer">{WHOP_ANNUAL_CTA_HREF}</a>）<br>
              ※商品価格以外にお客様にご負担いただく追加手数料はありません（インターネット接続料金・通信料はお客様のご負担となります）。
            </td>
          </tr>
          <tr>
            <th>代金の支払時期・支払方法</th>
            <td>クレジットカード決済（JCB・Visa・Mastercard・American Express）、Apple Pay、Google Pay。初回お申し込み時に即時決済され、以後選択プランに応じて1ヶ月ごとまたは1年ごとに自動更新されます。</td>
          </tr>
          <tr>
            <th>商品の引渡時期</th>
            <td>決済完了後、ただちにオンライン画面およびご登録メールアドレス宛にリサーチパス・過去統計ワークブックへのアクセスが有効化されます。</td>
          </tr>
          <tr>
            <th>解約・返品・デジタルコンテンツ標準返金規約</th>
            <td>①未閲覧・未ダウンロード時は決済後7日以内100%全額返金 ②デジタルPDF・コンテンツのダウンロード／閲覧開始後の自己都合返金不可（決済ボタン横に無料2pサンプルPDFを常設） ③ファイル不具合・重複決済時は100%返金 ④定期購読はいつでも1クリックで次回更新停止可能（違約金0円）。詳細は <a href="/jp/refund.html">返金・解約ポリシー</a> をご参照ください。</td>
          </tr>
        </tbody>
      </table>"""

    contact_body = f"""      <p>
        <strong>カスタマーサポート・法人メディア窓口および特定商取引法に基づく表記</strong>
      </p>
      <p>
        ご購読に関するご質問、メールアドレス変更、未閲覧7日全額返金・1クリック解約のご申請、ならびにメディア取材・法人データ提携のお問い合わせは、<a href="mailto:support@getbreakai.com">support@getbreakai.com</a> までお気軽にご連絡ください（原則24時間以内にご返信いたします）。特定商取引法に基づく法定記載事項の専用ページは <a href="/jp/tokushoho.html">特定商取引法に基づく表記 (/jp/tokushoho.html)</a> でもご確認いただけます。
      </p>
{tokushoho_table_body}"""

    specs = [
        ("terms.html", "利用規約 (Terms of Service)", "TERMS OF SERVICE · INDEPENDENT EDUCATIONAL RESEARCH", terms_body),
        ("privacy.html", "プライバシーポリシー (Privacy Policy)", "PRIVACY POLICY · APPI & GDPR COMPLIANT", privacy_body),
        ("refund.html", "デジタルコンテンツ標準返金・解約ポリシー (Standard Digital Refund Policy)", "STANDARD DIGITAL REFUND & 1-CLICK CANCELLATION", refund_body),
        ("tokushoho.html", "特定商取引法に基づく表記 (Specified Commercial Transactions Act)", "SPECIFIED COMMERCIAL TRANSACTIONS ACT DISCLOSURE", tokushoho_table_body),
        ("contact.html", "お問い合わせ・特定商取引法表記 (Contact & Disclosure)", "SUPPORT DESK & COMMERCIAL DISCLOSURE", contact_body),
    ]

    for slug, title_jp, badge_text, body_html in specs:
        root_html = _render_legal_doc(slug, title_jp, badge_text, body_html, is_jp_dir=False)
        jp_html = _render_legal_doc(slug, title_jp, badge_text, body_html, is_jp_dir=True)
        with open(os.path.join(root_dir, slug), "w", encoding="utf-8") as f:
            f.write(root_html)
        with open(os.path.join(jp_dir, slug), "w", encoding="utf-8") as f:
            f.write(jp_html)
