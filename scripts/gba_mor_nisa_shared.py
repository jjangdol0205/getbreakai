#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Division 3 (GBA — getbreakai.com) Shared Polar.sh MoR, FIEA (Kinsho-ho), FSA Shin-NISA Hybrid,
PAYMENT_CONFIG, VIP Waitlist Modal, CRM & Read-Complete Runtime Generator.
Strictly Zero-Hangul, Zero-LemonSqueezy, and Zero-Chat-App references.
"""

from __future__ import annotations
import os

MOR_LABEL_EN_JP = "Polar.sh (Merchant of Record · Global Card / Apple Pay / Google Pay)"
POLAR_MONTHLY_CTA_HREF = "#gbaVipWaitlistModal"
POLAR_ANNUAL_CTA_HREF = "#gbaVipWaitlistModal"

PRICE_LABEL_MONTHLY_JP = "月額 $29 / 約4,400円（税込）"
PRICE_LABEL_ANNUAL_JP = "年額 $199（約30,000円・税込）"

MANDATORY_DISCLAIMER_JP = (
    "免責事項：当サイトは公開市場データの可視化および数学的シミュレーションツール（教育・情報提供目的）であり、"
    "金融商品取引法上の投資助言・代理業や個別銘柄の売買推奨を行うものではありません。"
)

SOFTWARE_POSITIONING_JP = (
    "公開市場データ可視化および配当・資産配分計算ソフトウェア（Self-Directed Educational Calculator Software）"
)

FSA_HYBRID_PHRASE_JP = (
    "『新NISA 適格（四半期配当 VYM・HDV・1489・オルカン・S&P500 時間差組み合わせ）＋ 特定口座（毎月分配 SGOV・JEPI）ハイブリッド設計』"
)

VIP_WAITLIST_MODAL_TITLE_JP = "VIP創設メンバー先行案内＆早期20%割引クーポン予約（1秒メール登録）"

MODEL_CASE_DISCLAIMER_JP = "※ 資産規模・配分条件別の試算モデルケース（個人の感想や将来の運用成果を保証するものではありません）"

PRO_RETIREE_TOOLS_JP = (
    (
        "『毎朝自動配信：SMH × XLV マーケット過熱・恐怖指標＆セクター比率トラッキング日報メール』",
        "毎朝8時、日米市場の過熱度・恐怖度データ（0〜100）を集計し、過去検証モデル上で SMH（半導体）: XLV（医療）比率がどう推移しているかをわかりやすくメール配信",
    ),
    (
        "『新NISA成長投資枠（SMH・XLV）× 特定口座／個人向け国債 運用額別の円・ドル配分計算シート』",
        "ご自身の資産規模（300万〜5,000万円+・新NISA生涯非課税枠1,800万円対応）を入力するだけで、現物1倍ETFと安全クッションの具体的な金額目安を自動算出",
    ),
    (
        "『随時更新・SMH × XLV セクターバランス実践 14ページ マスターPDFガイド（楽天・SBI証券 大文字操作図解同梱）』",
        "過去26年（2000年ITバブル・2008年リーマン・2022年利上げ下落）の検証データ＆迷わず設定できる大きな文字の証券画面ステップマニュアル",
    ),
)

MAIN_HUB_EXCLUDED_SLUGS = {
    "soxl-smh-semiconductor-timing.html",
    "mstr-bitcoin-volatility-atr-sizing.html",
    "tsla-gamma-wall-swing-trade.html",
    "options-gamma-squeeze-gex-guide.html",
    "fomc-cpi-iv-crush-strategy.html",
    "us-stock-stop-loss-2percent-rule.html",
}


def build_payment_and_kpi_head_html() -> str:
    """Returns global head scripts for Polar.sh PAYMENT_CONFIG, CRM client, single-fire paid_click, waitlist/checkout router, ?payment=success unlock, signup & read_complete."""
    return r"""  <script src="/hq_member_crm_client.js"></script>
  <script>
    window.PAYMENT_CONFIG = {
      PROVIDER: 'polar_sh',
      DIVISION: 'GBA',
      STORE_SLOT: 'FINANCE_STORE_SLOT',
      STORE_LIVE_READY: false,
      POLAR_CHECKOUT_URLS: {
        monthly_29_jp: 'https://buy.polar.sh/polar_cl_AlujTTQg7tQ9Vu2gKVCnWDf1VJBSobVQQc3zc0NROOv?locale=ja',
        annual_199_jp: 'https://buy.polar.sh/polar_cl_nwbfHWyPzzpSXfhO2jDzfKAFdou4n7F7is2Lx1JaNe2?locale=ja',
        monthly_29: 'https://buy.polar.sh/polar_cl_AlujTTQg7tQ9Vu2gKVCnWDf1VJBSobVQQc3zc0NROOv?locale=ja',
        annual_199: 'https://buy.polar.sh/polar_cl_nwbfHWyPzzpSXfhO2jDzfKAFdou4n7F7is2Lx1JaNe2?locale=ja'
      },
      POLAR_GBA_MONTHLY_URL: 'https://buy.polar.sh/polar_cl_AlujTTQg7tQ9Vu2gKVCnWDf1VJBSobVQQc3zc0NROOv?locale=ja',
      POLAR_GBA_ANNUAL_URL: 'https://buy.polar.sh/polar_cl_nwbfHWyPzzpSXfhO2jDzfKAFdou4n7F7is2Lx1JaNe2?locale=ja',
      SUPPORT_EMAIL: 'beable9489@gmail.com'
    };
    window.CHECKOUT_URLS = {
      monthly: window.PAYMENT_CONFIG.POLAR_CHECKOUT_URLS.monthly_29_jp || window.PAYMENT_CONFIG.POLAR_CHECKOUT_URLS.monthly_29 || window.PAYMENT_CONFIG.POLAR_GBA_MONTHLY_URL || '',
      annual: window.PAYMENT_CONFIG.POLAR_CHECKOUT_URLS.annual_199_jp || window.PAYMENT_CONFIG.POLAR_CHECKOUT_URLS.annual_199 || window.PAYMENT_CONFIG.POLAR_GBA_ANNUAL_URL || '',
      enterprise: 'mailto:beable9489@gmail.com'
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

        window.ensurePolarLocaleUrl = function(rawUrl, defaultLocale, emailOverride) {
          var url = String(rawUrl || '').trim();
          if (!url || !/^https:\/\/(buy\.)?polar\.sh\//i.test(url)) return '';
          var loc = String(defaultLocale || 'ja').trim() || 'ja';
          var memberEmail = String(emailOverride || '').trim().toLowerCase();
          var validEmail = (memberEmail && /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(memberEmail)) ? memberEmail : '';
          try {
            var u = new URL(url);
            u.searchParams.set('locale', loc);
            if (validEmail && !u.searchParams.get('customer_email')) {
              u.searchParams.set('customer_email', validEmail);
            }
            return u.toString();
          } catch (_ue) {
            var cleanBase = url.replace(/([?&])locale=[^&]*/gi, '$1').replace(/\?&/, '?').replace(/[?&]+$/, '');
            var sep = cleanBase.indexOf('?') === -1 ? '?' : '&';
            var out = cleanBase + sep + 'locale=' + encodeURIComponent(loc);
            if (validEmail && out.indexOf('customer_email=') === -1) {
              out += '&customer_email=' + encodeURIComponent(validEmail);
            }
            return out;
          }
        };

        window.resolveGbaPolarCheckoutUrl = function(plan) {
          var cfg = window.PAYMENT_CONFIG || {};
          var urls = cfg.POLAR_CHECKOUT_URLS || {};
          var raw = (plan === 'annual')
            ? String(urls.annual_199_jp || urls.annual_199 || cfg.POLAR_GBA_ANNUAL_URL || '').trim()
            : String(urls.monthly_29_jp || urls.monthly_29 || cfg.POLAR_GBA_MONTHLY_URL || '').trim();
          return window.ensurePolarLocaleUrl(raw, 'ja');
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

        window.trackGbaVipWaitlistBeacons = function() {
          try {
            fetch('https://abacus.jasoncameron.dev/hit/' + ns + '/vip_waitlist_' + kst, { mode: 'cors', keepalive: true }).catch(function(){});
            fetch('https://abacus.jasoncameron.dev/hit/' + ns + '/vip_waitlist_total', { mode: 'cors', keepalive: true }).catch(function(){});
            fetch('https://abacus.jasoncameron.dev/hit/' + ns + '/vip_waitlist', { mode: 'cors', keepalive: true }).catch(function(){});
            fetch('https://abacus.jasoncameron.dev/hit/' + ns + '/signup', { mode: 'cors', keepalive: true }).catch(function(){});
            fetch('https://abacus.jasoncameron.dev/hit/' + ns + '/signup_total', { mode: 'cors', keepalive: true }).catch(function(){});
            if (localStorage.getItem('hq_signup_' + ns + '_' + kst) !== '1') {
              localStorage.setItem('hq_signup_' + ns + '_' + kst, '1');
              fetch('https://abacus.jasoncameron.dev/hit/' + ns + '/signup_' + kst, { mode: 'cors', keepalive: true }).catch(function(){});
            }
          } catch (_e) {}
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
            el.innerHTML = '✅ <strong>無料倶楽部へのご登録が完了しました！</strong> 毎朝8時の「新NISA 3色バランス指標＆公開データ試算ブリーフ」を <strong>' + email.replace(/[<>&"]/g, '') + '</strong> 宛にお届けいたします。';
          });
          document.querySelectorAll('.gba-jp-signup-form input[type="email"]').forEach(function(inp) { inp.value = email; });
          return false;
        };

        // Support ?payment=success return from Polar.sh hosted checkout on any GBA page
        try {
          var qParams = new URLSearchParams((window.location && window.location.search) || '');
          if (qParams.get('payment') === 'success' || qParams.get('checkout_status') === 'succeeded') {
            var pKey = String(qParams.get('license_key') || qParams.get('checkout_id') || qParams.get('order_id') || ('POLAR-VERIFIED-SESSION-' + kst)).trim();
            var pEmail = String(qParams.get('customer_email') || qParams.get('email') || '').trim();
            localStorage.setItem('gb_vip_unlocked', 'true');
            localStorage.setItem('gb_vip_license_key', pKey);
            localStorage.setItem('gb_vip_key', pKey);
            if (pEmail && pEmail.indexOf('@') !== -1) {
              localStorage.setItem('gb_vip_customer_email', pEmail);
            }
            if (typeof sessionStorage !== 'undefined' && sessionStorage.getItem('gba_polar_paid_hit') !== '1') {
              sessionStorage.setItem('gba_polar_paid_hit', '1');
              fetch('https://abacus.jasoncameron.dev/hit/' + ns + '/paid_success_' + kst, { mode: 'cors', keepalive: true }).catch(function(){});
              fetch('https://abacus.jasoncameron.dev/hit/' + ns + '/paid_success_total', { mode: 'cors', keepalive: true }).catch(function(){});
            }
          }
        } catch (_pe) {}

        if (!window.__GBA_PAID_CLICK_BOUND_V1__) {
          window.__GBA_PAID_CLICK_BOUND_V1__ = true;
          window.addEventListener('click', function(e) {
            var btn = e.target && e.target.closest
              ? e.target.closest('[data-gba-paid-plan], .polar-checkout-button, a[href*="buy.polar.sh"], a[href*="polar.sh/checkout"]')
              : null;
            if (!btn) return;
            var href = String(btn.getAttribute('href') || '');
            var planAttr = String(btn.getAttribute('data-gba-paid-plan') || '').toLowerCase();
            var slotAttr = String(btn.getAttribute('data-polar-slot') || '').toLowerCase();
            var selectedPlan = (planAttr === 'annual' || slotAttr.indexOf('annual') !== -1 || href.indexOf('annual') !== -1)
              ? 'annual'
              : 'monthly';

            fetch('https://abacus.jasoncameron.dev/hit/' + ns + '/paid_click_' + kst, { mode: 'cors', keepalive: true }).catch(function(){});
            fetch('https://abacus.jasoncameron.dev/hit/' + ns + '/paid_click_total', { mode: 'cors', keepalive: true }).catch(function(){});
            fetch('https://abacus.jasoncameron.dev/hit/' + ns + '/paid_click', { mode: 'cors', keepalive: true }).catch(function(){});

            var cfg = window.PAYMENT_CONFIG || {};
            var resolvedUrl = window.resolveGbaPolarCheckoutUrl(selectedPlan);
            if (!resolvedUrl && /^https:\/\/buy\.polar\.sh\/.+/i.test(href)) {
              resolvedUrl = window.ensurePolarLocaleUrl(href, 'ja');
            }
            var isLiveReady = (cfg.STORE_LIVE_READY === true) && /^https:\/\/buy\.polar\.sh\/.+/i.test(resolvedUrl);

            if (!isLiveReady) {
              e.preventDefault();
              e.stopImmediatePropagation();
              if (typeof window.openGbaVipWaitlistModal === 'function') {
                window.openGbaVipWaitlistModal(selectedPlan);
              }
              return false;
            }

            var memberEmail = window.getGbaSavedMemberEmail();
            var checkoutUrl = window.ensurePolarLocaleUrl(resolvedUrl, 'ja', memberEmail);

            if (checkoutUrl && !e.ctrlKey && !e.shiftKey && !e.metaKey) {
              e.preventDefault();
              e.stopImmediatePropagation();
              if (window.isGbaInAppWebView()) {
                window.location.href = checkoutUrl;
                return false;
              }
              if (window.PolarEmbedCheckout && typeof window.PolarEmbedCheckout.create === 'function') {
                window.PolarEmbedCheckout.create(checkoutUrl, 'light').catch(function() {
                  window.location.href = checkoutUrl;
                });
              } else {
                window.location.href = checkoutUrl;
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
    """Returns the exact mandatory FIEA (Kinsho-ho) non-advisory software disclaimer directly below Pricing."""
    return f"""      <div class="gba-mandatory-fiea-disclaimer" role="note" style="margin-top:14px; padding:13px 16px; border-radius:10px; background:#fffbeb; border:1.5px solid #f59e0b; color:#78350f; font-size:0.94rem; font-weight:700; line-height:1.68; text-align:left;">
        {MANDATORY_DISCLAIMER_JP}
      </div>"""


def build_pro_retiree_tools_html(compact: bool = False) -> str:
    """Returns high-contrast 3-tool efficacy showcase for Paid Pro ($29/mo & $199/yr) Shin-NISA Retiree Software."""
    items_html = "\n".join(
        f"""          <li style="background:var(--bg-sub, #f8fafc); border:1.5px solid var(--border-col, #cbd5e1); border-left:5px solid #1d4ed8; border-radius:11px; padding:{'10px 12px' if compact else '13px 15px'}; list-style:none;">
            <div style="font-size:{'0.95rem' if compact else '1.02rem'}; font-weight:900; color:var(--text-main, #0b1f3a); line-height:1.48; margin-bottom:4px;">✅ {idx}. {title_str}</div>
            <div style="font-size:{'0.88rem' if compact else '0.95rem'}; font-weight:700; color:var(--text-muted, #334155); line-height:1.6;">{desc_str}</div>
          </li>"""
        for idx, (title_str, desc_str) in enumerate(PRO_RETIREE_TOOLS_JP, start=1)
    )
    return f"""      <div class="gba-pro-retiree-tools-box" style="margin:14px 0 16px; padding:{'12px 14px' if compact else '16px 18px'}; border-radius:14px; background:var(--bg-card, #ffffff); border:2px solid #93c5fd;">
        <div style="font-size:{'0.96rem' if compact else '1.05rem'}; font-weight:900; color:var(--accent-blue, #1d4ed8); margin-bottom:10px; line-height:1.45;">
          🛠️ Proプラン（{PRICE_LABEL_MONTHLY_JP} ・ 年額 $199 / 約30,000円（税込））で使える「新NISA・老後3大設計ソフトウェアツール」
        </div>
        <ul style="margin:0; padding:0; display:flex; flex-direction:column; gap:10px;">
{items_html}
        </ul>
      </div>"""


def build_vip_waitlist_modal_html() -> str:
    """Returns scoped CSS, HTML, and JS for the Japanese VIP Founders Waitlist & 20% Coupon Modal (Zero Hangul)."""
    return f"""
  <style>
    .gba-vip-waitlist-backdrop {{
      display: none;
      position: fixed;
      inset: 0;
      z-index: 10050;
      background: rgba(11, 31, 58, 0.78);
      backdrop-filter: blur(5px);
      padding: 18px 12px;
      overflow-y: auto;
      align-items: center;
      justify-content: center;
    }}
    .gba-vip-waitlist-backdrop.is-open {{
      display: flex;
    }}
    .gba-vip-waitlist-dialog {{
      background: #ffffff;
      color: #0b1f3a;
      border: 2.5px solid #1d4ed8;
      border-radius: 18px;
      width: 100%;
      max-width: 580px;
      padding: 24px 22px;
      box-shadow: 0 24px 56px rgba(11, 31, 58, 0.42);
      font-family: 'Noto Sans JP', -apple-system, BlinkMacSystemFont, sans-serif;
      line-height: 1.7;
    }}
    .gba-vip-wl-top {{
      display: flex;
      justify-content: space-between;
      align-items: flex-start;
      gap: 10px;
      margin-bottom: 10px;
    }}
    .gba-vip-wl-badge {{
      display: inline-block;
      background: #eff6ff;
      color: #1e40af;
      border: 1.5px solid #93c5fd;
      font-size: 0.84rem;
      font-weight: 900;
      padding: 4px 12px;
      border-radius: 999px;
    }}
    .gba-vip-wl-close {{
      appearance: none;
      background: #f1f5f9;
      color: #0b1f3a;
      border: 1.5px solid #cbd5e1;
      border-radius: 9px;
      min-height: 40px;
      padding: 4px 12px;
      font-size: 0.9rem;
      font-weight: 800;
      cursor: pointer;
    }}
    .gba-vip-wl-title {{
      font-size: 1.24rem;
      font-weight: 900;
      color: #0b1f3a !important;
      margin: 4px 0 8px !important;
      padding: 0 !important;
      border: none !important;
      background: transparent !important;
      line-height: 1.42;
    }}
    .gba-vip-wl-desc {{
      font-size: 0.98rem;
      color: #334155 !important;
      margin: 0 0 14px;
      line-height: 1.68;
    }}
    .gba-vip-wl-plans {{
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 8px;
      margin-bottom: 14px;
    }}
    .gba-vip-wl-pbtn {{
      appearance: none;
      min-height: 54px;
      padding: 8px 10px;
      border-radius: 11px;
      border: 2px solid #cbd5e1;
      background: #f8fafc;
      color: #0b1f3a;
      font-size: 0.92rem;
      font-weight: 800;
      cursor: pointer;
      text-align: center;
      line-height: 1.35;
    }}
    .gba-vip-wl-pbtn.is-active {{
      border-color: #1d4ed8;
      background: #eff6ff;
      color: #1e3a8a;
      box-shadow: 0 0 0 3px rgba(29, 78, 216, 0.16);
    }}
    .gba-vip-wl-form {{
      display: flex;
      flex-wrap: wrap;
      gap: 10px;
    }}
    .gba-vip-wl-input {{
      flex: 1 1 240px;
      min-height: 54px;
      padding: 10px 14px;
      border-radius: 11px;
      border: 2px solid #64748b;
      background: #ffffff;
      color: #0f172a;
      font-size: 1.02rem;
      font-weight: 700;
    }}
    .gba-vip-wl-submit {{
      flex: 1 1 200px;
      min-height: 54px;
      padding: 10px 18px;
      border-radius: 11px;
      border: none;
      background: linear-gradient(135deg, #1d4ed8, #1e3a8a);
      color: #ffffff;
      font-size: 1rem;
      font-weight: 900;
      cursor: pointer;
    }}
    .gba-vip-wl-status {{
      display: none;
      margin-top: 12px;
      padding: 12px 14px;
      border-radius: 10px;
      background: #ecfdf5;
      border: 1.5px solid #059669;
      color: #065f46;
      font-size: 0.96rem;
      font-weight: 800;
      line-height: 1.65;
    }}
    @media (max-width: 600px) {{
      .gba-vip-wl-plans {{ grid-template-columns: 1fr; }}
    }}
  </style>

  <div class="gba-vip-waitlist-backdrop" id="gbaVipWaitlistModal" role="dialog" aria-modal="true" aria-labelledby="gbaVipWaitlistModalTitle" aria-hidden="true">
    <div class="gba-vip-waitlist-dialog">
      <div class="gba-vip-wl-top">
        <span class="gba-vip-wl-badge">🎁 創設メンバー優先案内 ・ 早期20%割引特典</span>
        <button type="button" class="gba-vip-wl-close" onclick="window.closeGbaVipWaitlistModal()">✕ 閉じる</button>
      </div>
      <h2 class="gba-vip-wl-title" id="gbaVipWaitlistModalTitle">{VIP_WAITLIST_MODAL_TITLE_JP}</h2>
      <p class="gba-vip-wl-desc">
        現在、公式グローバル決済基盤 <strong>{MOR_LABEL_EN_JP}</strong>（日本国内クレジットカード JCB・Visa・Mastercard・Apple Pay・Google Pay対応）の決済窓口最終確認を実施しております。メールアドレスをご登録いただくと、受付開始と同時に<strong>【創設メンバー限定・早期20%割引クーポン】</strong>を最優先でお届けいたします（本日の課金は一切発生いたしません）。
      </p>

      <div class="gba-vip-wl-plans" role="group" aria-label="ご希望プラン選択">
        <button type="button" class="gba-vip-wl-pbtn is-active" data-gba-wl-plan="monthly" onclick="window.selectGbaVipWaitlistPlan('monthly')">
          ⚡ {PRICE_LABEL_MONTHLY_JP}<br><small style="font-weight:700; color:#475569;">クーポン適用時 さらに20%OFF ／ 随時更新・新NISA老後取り崩し実践PDFガイド＋3つの財布シミュレーター同梱</small>
        </button>
        <button type="button" class="gba-vip-wl-pbtn" data-gba-wl-plan="annual" onclick="window.selectGbaVipWaitlistPlan('annual')">
          👑 {PRICE_LABEL_ANNUAL_JP}<br><small style="font-weight:700; color:#b45309;">一番人気・43%OFF＋早期20%割引 ／ 随時更新・新NISA老後取り崩し実践PDFガイド＋3つの財布シミュレーター同梱</small>
        </button>
      </div>
{build_pro_retiree_tools_html(compact=True)}

      <form class="gba-vip-wl-form" id="gbaVipWaitlistForm" onsubmit="return window.submitGbaVipWaitlist(event);">
        <label for="gbaVipWaitlistEmail" style="position:absolute; width:1px; height:1px; overflow:hidden; clip:rect(0,0,0,0);">メールアドレス</label>
        <input type="email" id="gbaVipWaitlistEmail" class="gba-vip-wl-input" required autocomplete="email" placeholder="メールアドレスを入力（例: yamada@example.jp）">
        <button type="submit" id="gbaVipWaitlistSubmitBtn" class="gba-vip-wl-submit">🎁 先行案内＆20%割引クーポンを予約する →</button>
      </form>

      <div class="gba-vip-wl-status" id="gbaVipWaitlistStatus" role="status" aria-live="polite"></div>

      <div style="margin-top:12px; font-size:0.84rem; color:#475569; line-height:1.58;">
        💳 決済・税務管理：{MOR_LABEL_EN_JP}（14日間返金保証・いつでも1クリック解約）<br>
        🔒 パスワード登録不要・いつでも1クリック配信停止可能 ｜ お問い合わせ窓口: <a href="mailto:beable9489@gmail.com" style="color:#1d4ed8; font-weight:800;">beable9489@gmail.com</a>
      </div>
    </div>
  </div>

  <script>
    (function() {{
      var activeWaitlistPlan = 'monthly';

      window.selectGbaVipWaitlistPlan = function(plan) {{
        activeWaitlistPlan = (plan === 'annual') ? 'annual' : 'monthly';
        document.querySelectorAll('[data-gba-wl-plan]').forEach(function(btn) {{
          var isAct = btn.getAttribute('data-gba-wl-plan') === activeWaitlistPlan;
          btn.classList.toggle('is-active', isAct);
          btn.setAttribute('aria-pressed', isAct ? 'true' : 'false');
        }});
      }};

      window.openGbaVipWaitlistModal = function(plan) {{
        window.selectGbaVipWaitlistPlan(plan || 'monthly');
        var modal = document.getElementById('gbaVipWaitlistModal');
        if (!modal) return;
        modal.classList.add('is-open');
        modal.setAttribute('aria-hidden', 'false');
        try {{
          var saved = localStorage.getItem('gb_free_member_email') || localStorage.getItem('gba_jp_free_email') || '';
          var inp = document.getElementById('gbaVipWaitlistEmail');
          if (inp && saved && !inp.value) inp.value = saved;
          setTimeout(function() {{ if (inp && inp.focus) inp.focus(); }}, 80);
        }} catch (_e) {{}}
      }};

      window.closeGbaVipWaitlistModal = function() {{
        var modal = document.getElementById('gbaVipWaitlistModal');
        if (!modal) return;
        modal.classList.remove('is-open');
        modal.setAttribute('aria-hidden', 'true');
      }};

      window.submitGbaVipWaitlist = function(ev) {{
        if (ev && ev.preventDefault) ev.preventDefault();
        var inp = document.getElementById('gbaVipWaitlistEmail');
        var statusEl = document.getElementById('gbaVipWaitlistStatus');
        var btn = document.getElementById('gbaVipWaitlistSubmitBtn');
        var email = String(inp ? inp.value : '').trim().toLowerCase();
        if (!/^[^\\s@]+@[^\\s@]+\\.[^\\s@]{{2,}}$/.test(email)) {{
          if (statusEl) {{
            statusEl.style.display = 'block';
            statusEl.innerText = '⚠️ 正しいメールアドレスを入力してください（例: yamada@example.jp）。';
          }}
          if (inp && inp.focus) inp.focus();
          return false;
        }}
        var selectedPlan = activeWaitlistPlan || 'monthly';
        if (btn) btn.disabled = true;

        var kstDay = new Date(Date.now() + 9 * 3600 * 1000).toISOString().slice(0, 10);
        if (typeof window.trackGbaVipWaitlistBeacons === 'function') {{
          window.trackGbaVipWaitlistBeacons();
        }} else {{
          fetch('https://abacus.jasoncameron.dev/hit/gba_getbreakai/vip_waitlist_' + kstDay, {{ mode: 'cors', keepalive: true }}).catch(function(){{}});
          fetch('https://abacus.jasoncameron.dev/hit/gba_getbreakai/vip_waitlist_total', {{ mode: 'cors', keepalive: true }}).catch(function(){{}});
          fetch('https://abacus.jasoncameron.dev/hit/gba_getbreakai/vip_waitlist', {{ mode: 'cors', keepalive: true }}).catch(function(){{}});
        }}

        var finishUi = function() {{
          if (btn) btn.disabled = false;
          if (statusEl) {{
            var planLabel = selectedPlan === 'annual' ? '{PRICE_LABEL_ANNUAL_JP}' : '{PRICE_LABEL_MONTHLY_JP}';
            statusEl.style.display = 'block';
            statusEl.innerHTML = '✅ <strong>VIP創設メンバー先行案内＆早期20%割引クーポンのご予約が完了いたしました！</strong>（' + email.replace(/[<>&"]/g, '') + ' ／ 選択プラン: ' + planLabel + '）<br>Polar.sh 公式決済受付の開始と同時に優先ご案内メールをお送りいたします。また毎朝8時の無料「3色バランス指標ブリーフ」も本日よりお届けいたします。';
          }}
        }};

        try {{
          localStorage.setItem('gb_free_member_email', email);
          localStorage.setItem('gba_jp_free_email', email);
        }} catch (_e) {{}}

        if (window.DreamCompanyCRM && typeof window.DreamCompanyCRM.registerMember === 'function') {{
          window.DreamCompanyCRM.registerMember({{
            div: 'GBA',
            email: email,
            segment: 'vip_waitlist',
            lang: 'ja-JP',
            notes: 'site=getbreakai.com | provider=polar_sh | plan=' + selectedPlan
          }}).then(finishUi).catch(finishUi);
        }} else {{
          finishUi();
        }}
        return false;
      }};

      document.addEventListener('click', function(ev) {{
        var modal = document.getElementById('gbaVipWaitlistModal');
        if (modal && modal.classList.contains('is-open') && ev.target === modal) {{
          window.closeGbaVipWaitlistModal();
        }}
      }});
      document.addEventListener('keydown', function(ev) {{
        if (ev.key === 'Escape') {{
          window.closeGbaVipWaitlistModal();
        }}
      }});
    }})();
  </script>"""


def build_starter_manual_modal_html() -> str:
    """Returns the In-App WebView guarded ¥0 Shin-NISA Starter Manual Modal + Email Delivery UI."""
    return f"""
  <!-- 📘 Interactive Modal: ¥0 無料公開商品 はじめての新NISA＆証券アプリ基本マニュアル (#gbaStarterManualModal) -->
  <div class="gba-manual-modal-backdrop" id="gbaStarterManualModal" role="dialog" aria-modal="true" aria-labelledby="gbaStarterManualModalTitle" aria-hidden="true">
    <div class="gba-manual-modal-dialog">
      <div class="gba-manual-modal-header">
        <div>
          <span class="gba-manual-free-badge" style="font-size:0.84rem;">📘 ¥0 無料公開マニュアル（保存版・登録不要）</span>
          <h2 class="gba-manual-modal-title" id="gbaStarterManualModalTitle">はじめての新NISA＆証券アプリ基本マニュアル</h2>
        </div>
        <div class="gba-manual-modal-actions">
          <button type="button" class="gba-manual-action-btn btn-print" id="btnPrintOrMailGbaManual" onclick="printGbaStarterManual()">🖨️ 印刷・PDF保存</button>
          <button type="button" class="gba-manual-action-btn" id="btnCloseGbaStarterManual" onclick="closeGbaStarterManualModal()">✕ 閉じる</button>
        </div>
      </div>

      <!-- In-App WebView Safe Email Delivery Strip ("このマニュアルをメールで受け取る（無料倶楽部登録）") -->
      <div id="gbaManualWebViewMailBox" style="padding:14px 18px; background:linear-gradient(135deg, #ecfdf5 0%, #eff6ff 100%); border-bottom:2px solid #059669;">
        <div id="gbaManualWebViewNotice" style="display:none; font-size:0.9rem; font-weight:900; color:#065f46; margin-bottom:6px;">
          📱 アプリ内ブラウザ（Instagram・Facebook・LINE等）では印刷機能が制限されるため、全章をこのまま画面でお読みいただくか、下記よりメールで保存版をお受け取りいただけます。
        </div>
        <div style="font-size:1rem; font-weight:900; color:#0b1f3a; margin-bottom:8px;">
          📩 このマニュアルをメールで受け取る（無料倶楽部登録）
        </div>
        <form id="gbaManualEmailDeliveryForm" onsubmit="return window.submitGbaManualEmailDelivery(event);" style="display:flex; flex-wrap:wrap; gap:8px;">
          <label for="gbaManualDeliveryEmail" style="position:absolute; width:1px; height:1px; overflow:hidden; clip:rect(0,0,0,0);">メールアドレス</label>
          <input type="email" id="gbaManualDeliveryEmail" required autocomplete="email" placeholder="メールアドレスを入力（例: taro@example.jp）" style="flex:1 1 230px; min-height:48px; padding:8px 13px; border-radius:10px; border:2px solid #64748b; background:#ffffff; color:#0f172a; font-size:0.98rem; font-weight:700;">
          <button type="submit" id="btnSubmitGbaManualMail" style="min-height:48px; padding:8px 18px; border-radius:10px; border:none; background:#059669; color:#ffffff; font-size:0.95rem; font-weight:900; cursor:pointer;">📩 このマニュアルをメールで受け取る（無料倶楽部登録） →</button>
        </form>
        <div id="gbaManualDeliveryStatus" role="status" aria-live="polite" style="display:none; margin-top:8px; padding:9px 12px; border-radius:8px; background:#d1fae5; color:#065f46; font-size:0.94rem; font-weight:800;"></div>
      </div>

      <nav class="gba-manual-nav-pills" aria-label="マニュアル目次">
        <button type="button" class="gba-manual-jump-pill" onclick="scrollToGbaManualChapter('gbaManualChap1')">第1章：指値注文の買い方</button>
        <button type="button" class="gba-manual-jump-pill" onclick="scrollToGbaManualChapter('gbaManualChap2')">第2章：新NISA適格×特定口座の使い分け</button>
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
              <strong class="broker-name">📱 楽天証券（スマホアプリ「iSPEED」・Web）の操作手順</strong>
              <ol>
                <li>銘柄名を検索し、右上の<strong>「注文」→「現物買い」</strong>をタップします。</li>
                <li>口座区分で対象銘柄に応じた区分（<strong>「NISA成長投資枠」</strong>または<strong>「特定口座」</strong>）を選びます。</li>
                <li>価格欄で<strong>「指値」</strong>を選択し、希望上限価格と株数を入力して確認画面へ進みます。</li>
              </ol>
            </div>
            <div class="gba-manual-broker-card">
              <strong class="broker-name">📱 SBI証券（「SBI証券 株」／「米国株」アプリ）の操作手順</strong>
              <ol>
                <li>銘柄画面から<strong>「取引」→「現物買」</strong>をタップします。</li>
                <li>預り区分で<strong>「NISA預り（成長）」</strong>または<strong>「特定預り」</strong>にチェックを入れます。</li>
                <li>価格指定で<strong>「指値」</strong>を選び、上限金額と株数を確認してから発注します。</li>
              </ol>
            </div>
          </div>
          <div class="gba-manual-tip-callout">
            ✅ <strong>安心のポイント：</strong>指値まで価格が下がらなければ約定せず現金がそのまま残るため、意図しない高値購入を防げます。
          </div>
        </article>

        <article class="gba-manual-chapter-box" id="gbaManualChap2">
          <h3>第2章 — 金融庁ルール準拠：新NISA適格銘柄と特定口座（毎月分配型）の正しいハイブリッド区分＆年2〜4回配分点検</h3>
          <p>
            日本の金融庁規定により、<strong>毎月分配型ETF（JEPI・JEPQ・QYLD・SGOV等）およびレバレッジ型ETF（SOXL・TQQQ等）は新NISAの対象外</strong>です。そのため老後の毎月キャッシュフロー設計では、{FSA_HYBRID_PHRASE_JP}で口座を正しく使い分け、頻繁な売買を避けて<strong>年2〜4回の穏やかな資産配分（リバランス）点検</strong>で年間360万円の非課税枠を大切に守ります。
          </p>
          <div class="gba-manual-broker-grid">
            <div class="gba-manual-broker-card">
              <strong class="broker-name">🌱 新NISA口座（非課税 0%）で保有できる適格コア資産</strong>
              <ol>
                <li><strong>1489（日経高配当株50 ETF）：</strong> 1・4・7・10月決算の国内高配当50社分散。</li>
                <li><strong>VYM・HDV（米国高配当株ETF）：</strong> 3・6・9・12月分配の米国優良増配株分散（1489と時間差組み合わせ）。</li>
                <li><strong>オルカン・S&amp;P500投信：</strong> つみたて投資枠・成長投資枠双方で長期インフレ対策に対応。</li>
              </ol>
            </div>
            <div class="gba-manual-broker-card">
              <strong class="broker-name">🏦 特定口座（源泉徴収あり 20.315%）で区分管理する資産</strong>
              <ol>
                <li><strong>SGOV（米国短期国債ETF）・JEPI（米国カバードコール毎月分配ETF）：</strong> 毎月分配型のため金融庁規定により新NISA対象外です。必ず<strong>特定口座</strong>で管理します。</li>
                <li><strong>損益通算の活用：</strong> 特定口座内の配当と譲渡損益は自動計算・損益通算されます。</li>
              </ol>
            </div>
          </div>
          <div class="gba-manual-tip-callout">
            ✅ <strong>安心のポイント：</strong>四半期配当の新NISA適格ETF（1・4・7・10月＋3・6・9・12月）と個人向け国債（半年利払い）・特定口座の毎月分配資産を組み合わせることで、金融庁ルールに100%準拠しながら年間を通じた穏やかなキャッシュフローを設計できます。
          </div>
        </article>

        <article class="gba-manual-chapter-box" id="gbaManualChap3">
          <h3>第3章 — 守りの財布を整える「個人向け国債（変動10年）・楽天マネーブリッジ・SBIハイブリッド預金」の活用法</h3>
          <p>
            相場変動が大きい<strong>🔴 現金・国債防衛モード</strong>の時期は、無理に株式比率を増やす必要はありません。生活費2〜3年分の安全クッションを国債や証券連携預金に置いておくことで、株価下落時にも慌てず配当と年金をゆったり受け取ることができます。
          </p>
          <div class="gba-manual-broker-grid">
            <div class="gba-manual-broker-card">
              <strong class="broker-name">🏦 楽天証券：「マネーブリッジ」＆個人向け国債</strong>
              <ol>
                <li>楽天証券と楽天銀行を連携する<strong>「マネーブリッジ（無料）」</strong>を設定し、普通預金優遇金利と預金保険で待機資金を保護します。</li>
                <li>生活防衛資金の一部を<strong>「個人向け国債（変動10年）」</strong>に配分すると、半年ごとに適用利率が見直され元本割れなく保有できます。</li>
              </ol>
            </div>
            <div class="gba-manual-broker-card">
              <strong class="broker-name">🏦 SBI証券：「SBIハイブリッド預金」＆外貨建MMF</strong>
              <ol>
                <li>住信SBIネット銀行と連携し<strong>「SBIハイブリッド預金」</strong>を有効にすると、待機円資金に毎月利子がつきながら買付余力へ自動反映されます。</li>
                <li>米ドル待機資金は特定口座の「外貨建MMF」や「SGOV（特定口座）」で区分管理できます。</li>
              </ol>
            </div>
          </div>
        </article>

        <div class="gba-manual-modal-funnel">
          <h4>🌅 基本設定を確認したら、毎朝8時の「3色バランス指標ブリーフ」をご活用ください</h4>
          <p>
            当サイトの数学的シミュレーターと毎朝の公開市場データ要約を活用し、ご自身のペースで年2〜4回の穏やかな資産配分点検にお役立てください。
          </p>
          <div class="gba-manual-cta-row" style="margin-bottom:10px;">
            <button type="button" class="gba-manual-open-btn" onclick="jumpFromManualToJpMail()">
              📧 無料倶楽部に登録して毎朝8時の「3色バランス指標」を受け取る
            </button>
          </div>
          <div class="gba-manual-funnel-links">
            <a href="{POLAR_MONTHLY_CTA_HREF}" data-gba-paid-plan="monthly" data-polar-slot="monthly_29_jp" class="gba-manual-pro-link polar-checkout-button">⚡ {PRICE_LABEL_MONTHLY_JP}</a>
            <a href="{POLAR_ANNUAL_CTA_HREF}" data-gba-paid-plan="annual" data-polar-slot="annual_199_jp" class="gba-manual-vip-link polar-checkout-button">👑 {PRICE_LABEL_ANNUAL_JP}</a>
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
          if (pBtn) pBtn.innerText = '📩 このマニュアルをメールで受け取る';
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
          st.innerHTML = '✅ <strong>ご登録ありがとうございます！</strong> 保存版マニュアルと毎朝8時の「新NISA 3色バランス指標ブリーフ」を <strong>' + email.replace(/[<>&"]/g, '') + '</strong> 宛にお届けいたします。';
        }}
        return false;
      }};

      window.addEventListener('DOMContentLoaded', function() {{
        if (typeof window.isGbaInAppWebView === 'function' && window.isGbaInAppWebView()) {{
          var pBtn = document.getElementById('btnPrintOrMailGbaManual');
          var notice = document.getElementById('gbaManualWebViewNotice');
          if (pBtn) pBtn.innerText = '📩 このマニュアルをメールで受け取る';
          if (notice) notice.style.display = 'block';
          document.querySelectorAll('.gba-manual-sub-badge').forEach(function(b) {{
            b.innerText = '📩 メール保存・画面閲覧対応 ／ 楽天証券・SBI証券 対応';
          }});
        }}
      }});
    }})();
  </script>"""


def build_legal_footer_html() -> str:
    """Returns prominent Polar.sh MoR & FIEA compliant footer legal bar linking both /jp/*.html and root /*.html legal pages."""
    return f"""
  <footer class="gba-fixed-legal-footer" style="margin-top:32px; padding:24px 16px 36px; border-top:2px solid #cbd5e1; background:rgba(15,23,42,0.03); font-size:0.9rem; line-height:1.72; color:var(--text-muted, #334155);">
    <div style="max-width:1040px; margin:0 auto;">
      <div style="display:flex; flex-wrap:wrap; align-items:center; justify-content:center; gap:10px 18px; margin-bottom:14px; font-weight:800;">
        <a href="/jp/terms.html" style="color:var(--accent-blue, #1d4ed8); text-decoration:underline;">利用規約</a>
        <span aria-hidden="true">·</span>
        <a href="/jp/privacy.html" style="color:var(--accent-blue, #1d4ed8); text-decoration:underline;">プライバシーポリシー</a>
        <span aria-hidden="true">·</span>
        <a href="/jp/refund.html" style="color:var(--accent-blue, #1d4ed8); text-decoration:underline;">14日間返金ポリシー</a>
        <span aria-hidden="true">·</span>
        <a href="/jp/contact.html" style="color:var(--accent-blue, #1d4ed8); text-decoration:underline;">特定商取引法に基づく表記</a>
        <span aria-hidden="true">·</span>
        <a href="https://www.youtube.com/@GetBreakAI" target="_blank" rel="noopener" style="color:var(--accent-blue, #1d4ed8); text-decoration:underline;">📺 公式YouTube (@GetBreakAI)</a>
        <span aria-hidden="true">·</span>
        <span>カスタマーサポート: <a href="mailto:beable9489@gmail.com" style="color:var(--accent-blue, #1d4ed8); font-weight:900; text-decoration:underline;">beable9489@gmail.com</a></span>
        <span aria-hidden="true">·</span>
        <span>法人・メディア提携窓口: <a href="mailto:beable9489@gmail.com?subject=GetBreakAI%20Media%20%26%20Corporate%20Partnership" style="color:var(--accent-blue, #1d4ed8); font-weight:900; text-decoration:underline;">beable9489@gmail.com</a></span>
      </div>
      <div style="text-align:center; font-size:0.82rem; color:var(--text-sub, #475569); margin-bottom:10px;">
        英語版・共通法務リンク:
        <a href="/terms.html" style="color:inherit; text-decoration:underline;">Terms (/terms.html)</a> ·
        <a href="/privacy.html" style="color:inherit; text-decoration:underline;">Privacy (/privacy.html)</a> ·
        <a href="/refund.html" style="color:inherit; text-decoration:underline;">14-Day Refund (/refund.html)</a> ·
        <a href="/contact.html" style="color:inherit; text-decoration:underline;">Commercial Disclosure (/contact.html)</a> ·
        <span>Sponsorship &amp; Media Partnership: <a href="mailto:beable9489@gmail.com" style="color:inherit; text-decoration:underline;">beable9489@gmail.com</a></span>
      </div>
      <div style="max-width:920px; margin:0 auto; padding:12px 15px; border-radius:10px; background:var(--bg-card, #ffffff); border:1px solid var(--border-col, #cbd5e1); font-size:0.84rem; color:var(--text-sub, #475569);">
        <strong>【{SOFTWARE_POSITIONING_JP}】</strong><br>
        {MANDATORY_DISCLAIMER_JP}<br>
        公式決済・税務管理基盤：<strong>{MOR_LABEL_EN_JP}</strong>（日本国内発行クレジットカード・Apple Pay・Google Pay対応 ／ 14日間返金保証）<br>
        Operated by Yoonju Lee · KIDS-FIT Global Studio &amp; GetBreakAI · Official Billing via {MOR_LABEL_EN_JP}. Support Desk: <a href="mailto:beable9489@gmail.com" style="color:var(--accent-blue, #1d4ed8); font-weight:800;">beable9489@gmail.com</a>
      </div>
    </div>
  </footer>"""


def _render_legal_doc(slug: str, title_jp: str, badge_text: str, body_html: str, is_jp_dir: bool) -> str:
    canonical = f"https://getbreakai.com/jp/{slug}" if is_jp_dir else f"https://getbreakai.com/{slug}"
    home_href = "/jp/"
    head_scripts = build_payment_and_kpi_head_html()
    waitlist_modal = build_vip_waitlist_modal_html()
    footer_html = build_legal_footer_html()
    return f"""<!DOCTYPE html>
<html lang="ja" data-jp-theme="light">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{title_jp} ｜ GetBreakAI</title>
  <meta name="description" content="GetBreakAI ({canonical}) — {title_jp}・{SOFTWARE_POSITIONING_JP}・{MOR_LABEL_EN_JP}。サポート窓口: beable9489@gmail.com">
  <link rel="canonical" href="{canonical}">
  <link rel="icon" type="image/svg+xml" href="/favicon.svg">
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
    .brand {{ color: #ffffff; text-decoration: none; font-weight: 900; font-size: 1.12rem; }}
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
      <a href="{home_href}" class="brand">⚡ GetBreakAI ゆとり老後＆新NISA設計ナビ</a>
      <a href="{home_href}" class="back-link">← 新NISA老後設計ナビへ戻る</a>
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
{waitlist_modal}
</body>
</html>
"""


def build_all_legal_pages(root_dir: str, jp_dir: str) -> None:
    """Generates and synchronizes terms.html, privacy.html, refund.html, and contact.html in both root and /jp/."""
    os.makedirs(jp_dir, exist_ok=True)

    terms_body = f"""      <p>
        本利用規約（以下「本規約」）は、<strong>Yoonju Lee · KIDS-FIT Global Studio</strong>（以下「当スタジオ」）が提供する<strong>{SOFTWARE_POSITIONING_JP}</strong>「<strong>GetBreakAI</strong>」（<a href="https://getbreakai.com/jp/">https://getbreakai.com/jp/</a>）のご利用条件を定めるものです。
      </p>
      <div class="disclaimer-box">
        {MANDATORY_DISCLAIMER_JP}
      </div>
      <h2>第1条（提供ソフトウェアの内容・自己判断ツールとしての性質）</h2>
      <ul>
        <li>公的年金と新NISA・特定口座を組み合わせた老後キャッシュフローおよび非課税節税額の数学的シミュレーション機能</li>
        <li>日本の金融庁規定に準拠した{FSA_HYBRID_PHRASE_JP}の資産配分比率計算機能</li>
        <li>Proプラン同梱ツール：①『新NISA 生涯非課税枠1,800万円（成長投資枠1,200万＋つみたて枠600万）退職金・年次別最適配分シート』、②『1489（1・4・7・10月）＋VYM/HDV（3・6・9・12月）＋国債でつくる 年12回・毎月配当カレンダー設計ツール』、③『楽天証券・SBI証券 スマホ／PC画面そのまま操作・大文字図解＆ステップガイド』</li>
        <li>米国SEC公開財務開示（Form 8-K / 10-Q / Form 4）および日米公開市場データの統計的可視化ダッシュボード（全利用者へ同一の計算式を表示する汎用教育ソフトウェア）</li>
      </ul>
      <h2>第2条（決済管理・ライセンス利用権）</h2>
      <p>
        有料ソフトウェアプラン（{PRICE_LABEL_MONTHLY_JP} ／ {PRICE_LABEL_ANNUAL_JP}）の決済処理・消費税等を含む税務管理・領収書発行は、公式決済代行基盤 <strong>{MOR_LABEL_EN_JP}</strong>（Stripe提携・日本国内発行クレジットカード／Apple Pay／Google Pay対応の公式 Merchant of Record）によって安全に処理されます。発行されたライセンスはご購入者様ご本人の個人利用に限り有効であり、第三者への転売・再配布は禁止されます。
      </p>
      <h2>第3条（無保証および免責事項）</h2>
      <p>
        当サイトに表示される公開市場データ・配当利回り試算・過去統計シミュレーションは教育および情報提供のみを目的としており、将来の運用成果や元本を保証するものではありません。最終的な資産配分および投資判断はお客様ご自身の責任において行ってください。
      </p>
      <h2>English Summary — Self-Directed Educational Calculator Software Terms</h2>
      <p>
        <strong>GetBreakAI</strong> is a self-directed public market data visualization and mathematical dividend/asset-allocation calculator software operated by <strong>Yoonju Lee · KIDS-FIT Global Studio</strong>, with global checkout, tax compliance, and invoicing handled by <strong>{MOR_LABEL_EN_JP}</strong>. GetBreakAI is NOT an investment advisor, broker-dealer, or financial instruments business operator under Japan&apos;s Financial Instruments and Exchange Act or U.S. law. Support: <a href="mailto:beable9489@gmail.com">beable9489@gmail.com</a>.
      </p>"""

    privacy_body = f"""      <p>
        <strong>GetBreakAI</strong>（運営：Yoonju Lee · KIDS-FIT Global Studio ／ 公式決済基盤：{MOR_LABEL_EN_JP}）は、お客様の個人情報およびプライバシー保護を最優先事項として管理いたします。
      </p>
      <h2>1. 取得する情報と決済セキュリティ</h2>
      <ul>
        <li><strong>クレジットカード・決済情報：</strong> 決済処理はすべて PCI-DSS Level 1 準拠の公式決済代行基盤 <strong>{MOR_LABEL_EN_JP}</strong>（Stripe決済インフラ提携）により暗号化処理され、当サイトのサーバーがカード番号を保持・閲覧することは一切ありません。</li>
        <li><strong>メール倶楽部・先行案内登録情報：</strong> ご登録いただいたメールアドレスおよび任意のニックネームは、毎朝の公開市場ブリーフィング配信・先行割引クーポンのご案内・カスタマーサポートの目的でのみ利用し、メール下部の解除リンクからいつでも1クリックで配信停止できます。</li>
        <li><strong>ブラウザ内計算データ（localStorage）：</strong> 老後キャッシュフローシミュレーターの試算条件や文字サイズ・テーマ設定はお使いのブラウザ内にのみ保存され、第三者へ販売・提供されることはありません。</li>
      </ul>
      <h2>2. 第三者提供の禁止および開示・削除請求</h2>
      <p>
        法令に基づく場合または公式決済代行事業者（{MOR_LABEL_EN_JP}）の決済・領収書発行処理に必要な範囲を除き、個人情報を第三者へ提供することはありません。登録情報の照会・訂正・削除のご請求は <a href="mailto:beable9489@gmail.com">beable9489@gmail.com</a> までご連絡ください。原則1営業日（24時間）以内に対応いたします。
      </p>
      <h2>English Summary — Privacy Policy (APPI &amp; GDPR Compliant)</h2>
      <p>
        Payment credentials are processed exclusively by <strong>{MOR_LABEL_EN_JP}</strong> and are never stored on GetBreakAI servers. Email addresses submitted for morning market summaries or VIP waitlist coupons include 1-click unsubscribe links and are never sold or rented. Contact <a href="mailto:beable9489@gmail.com">beable9489@gmail.com</a> for data deletion requests.
      </p>"""

    refund_body = f"""      <p>
        <strong>GetBreakAI</strong>（公式決済基盤：<strong>{MOR_LABEL_EN_JP}</strong>）では、シニア・個人投資家の皆さまに安心してご利用いただけるよう、<strong>いつでも可能な1クリック解約</strong>と<strong>初回ご購入後14日間の全額返金保証（14日間返金保証）</strong>を設けています。
      </p>
      <div class="disclaimer-box">
        ✅ <strong>14日間返金ポリシー（初回14日間返金保証）＆ いつでも1クリック自動更新停止（違約金0円）</strong><br>
        ご購入から14日以内に <a href="mailto:beable9489@gmail.com">beable9489@gmail.com</a> までご連絡いただければ、理由を問わず迅速に100%全額返金いたします。
      </div>
      <h2>1. サブスクリプションの1クリック解約手順</h2>
      <p>
        月額プラン（{PRICE_LABEL_MONTHLY_JP}）および年間プラン（{PRICE_LABEL_ANNUAL_JP}）は、ご購入時の領収書メール内の「Manage Subscription / Customer Portal」リンク、または <a href="https://polar.sh" target="_blank" rel="noopener noreferrer">Polar.sh Customer Portal</a>、もしくは <a href="mailto:beable9489@gmail.com">beable9489@gmail.com</a> へのメール連絡により24時間いつでも解約できます。
      </p>
      <h2>2. 14日間返金保証の申請方法と返金時期</h2>
      <ul>
        <li><strong>初回14日間返金保証：</strong> ご購入後14日以内に決済時のメールアドレスまたは注文番号（Order ID）を添えて <a href="mailto:beable9489@gmail.com">beable9489@gmail.com</a> 宛にご連絡ください。</li>
        <li><strong>重複課金・技術的不具合：</strong> 万が一の重複決済やライセンス未着時は即時100%返金または再発行いたします。</li>
        <li><strong>処理日数：</strong> ご連絡から原則1営業日（24時間）以内に <strong>{MOR_LABEL_EN_JP}</strong> 経由でお支払い元のカード・Apple Pay・Google Pay等へ返金手続きを実行いたします（明細反映はカード会社により通常3〜5営業日）。</li>
      </ul>
      <h2>English Summary — 14-Day Money-Back Guarantee &amp; 1-Click Cancellation</h2>
      <p>
        All billing and refunds are processed via <strong>{MOR_LABEL_EN_JP}</strong>. Cancel anytime in 1 click via the Polar.sh Customer Portal or receipt email with zero penalties. If you are not satisfied within 14 calendar days of your initial purchase, email <a href="mailto:beable9489@gmail.com">beable9489@gmail.com</a> with your checkout email or Order ID for a 100% full refund processed within 1 business day.
      </p>"""

    contact_body = f"""      <p>
        <strong>特定商取引法に基づく表記およびカスタマーサポート窓口（Commercial Disclosure &amp; Support Desk）</strong>
      </p>
      <table>
        <tbody>
          <tr>
            <th>販売事業者・運営スタジオ</th>
            <td>Yoonju Lee · KIDS-FIT Global Studio / Dream Company Quantitative Research (GetBreakAI Desk)</td>
          </tr>
          <tr>
            <th>公式決済代行 (MoR)</th>
            <td><strong>{MOR_LABEL_EN_JP}</strong> — Stripe提携・PCI-DSS Level 1準拠グローバル決済・税務管理基盤（JCB・Visa・Mastercard・Apple Pay・Google Pay対応）</td>
          </tr>
          <tr>
            <th>カスタマーサポート窓口</th>
            <td><a href="mailto:beable9489@gmail.com">beable9489@gmail.com</a>（24時間メール受付・原則1営業日以内に日本語または英語でご返信）</td>
          </tr>
          <tr>
            <th>法人・メディア提携窓口</th>
            <td>法人・メディア提携窓口: <a href="mailto:beable9489@gmail.com">beable9489@gmail.com</a></td>
          </tr>
          <tr>
            <th>提供ソフトウェア区分</th>
            <td>{SOFTWARE_POSITIONING_JP}</td>
          </tr>
          <tr>
            <th>販売価格（税込目安）</th>
            <td>
              ・月額Proプラン：{PRICE_LABEL_MONTHLY_JP}（随時更新・新NISA老後取り崩し実践PDFガイド＋3つの財布シミュレーター同梱）<br>
              ・年間Pro VIPプラン：{PRICE_LABEL_ANNUAL_JP}（随時更新・新NISA老後取り崩し実践PDFガイド＋3つの財布シミュレーター同梱）<br>
              ・法人・データ提携デスク：個別お見積り（<a href="mailto:beable9489@gmail.com">beable9489@gmail.com</a>）
            </td>
          </tr>
          <tr>
            <th>解約・14日間返金ポリシー</th>
            <td>いつでも1クリックで次回更新停止可能。初回購入後14日間返金保証あり（詳細は <a href="/jp/refund.html">14日間返金ポリシー</a> をご参照ください）。</td>
          </tr>
        </tbody>
      </table>"""

    specs = [
        ("terms.html", "利用規約 (Terms of Service)", "TERMS OF SERVICE · POLAR.SH MERCHANT OF RECORD", terms_body),
        ("privacy.html", "プライバシーポリシー (Privacy Policy)", "PRIVACY POLICY · APPI & GDPR COMPLIANT", privacy_body),
        ("refund.html", "14日間返金ポリシー・解約規約 (14-Day Refund Policy)", "14-DAY REFUND POLICY · 1-CLICK CANCELLATION", refund_body),
        ("contact.html", "特定商取引法に基づく表記・お問い合わせ (Contact)", "COMMERCIAL DISCLOSURE & SUPPORT DESK", contact_body),
    ]

    for slug, title_jp, badge_text, body_html in specs:
        root_html = _render_legal_doc(slug, title_jp, badge_text, body_html, is_jp_dir=False)
        jp_html = _render_legal_doc(slug, title_jp, badge_text, body_html, is_jp_dir=True)
        with open(os.path.join(root_dir, slug), "w", encoding="utf-8") as f:
            f.write(root_html)
        with open(os.path.join(jp_dir, slug), "w", encoding="utf-8") as f:
            f.write(jp_html)
