window.PAYMENT_CONFIG = {
      PROVIDER: 'whop',
      DIVISION: 'GBA',
      STORE_SLOT: 'FINANCE_STORE_SLOT',
      STORE_LIVE_READY: true,
      COMPANY_ID: 'biz_pZ7yTvBkO7QcZY',
      STORE_NAME: 'GetBreakAI Japan Research',
      WHOP_PLANS: {
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
            (function(){return Promise.resolve();})('https://abacus.disabled/hit/' + ns + '/signup', { mode: 'cors', keepalive: true }).catch(function(){});
            (function(){return Promise.resolve();})('https://abacus.disabled/hit/' + ns + '/signup_total', { mode: 'cors', keepalive: true }).catch(function(){});
            if (localStorage.getItem('hq_signup_' + ns + '_' + kst) !== '1') {
              localStorage.setItem('hq_signup_' + ns + '_' + kst, '1');
              (function(){return Promise.resolve();})('https://abacus.disabled/hit/' + ns + '/signup_' + kst, { mode: 'cors', keepalive: true }).catch(function(){});
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
              (function(){return Promise.resolve();})('https://abacus.disabled/hit/' + ns + '/paid_click_' + kst, { mode: 'cors', keepalive: true }).catch(function(){});
              (function(){return Promise.resolve();})('https://abacus.disabled/hit/' + ns + '/paid_click_total', { mode: 'cors', keepalive: true }).catch(function(){});
              return;
            }
            var href = String(btn.getAttribute('href') || '');
            var planAttr = String(btn.getAttribute('data-gba-paid-plan') || btn.getAttribute('data-whop-plan') || '').toLowerCase();
            var selectedPlan = (planAttr === 'annual' || href.indexOf('plan_ahYIXbLDE0CsQ') !== -1 || href.indexOf('annual') !== -1)
              ? 'annual'
              : 'monthly';

            (function(){return Promise.resolve();})('https://abacus.disabled/hit/' + ns + '/paid_click_' + kst, { mode: 'cors', keepalive: true }).catch(function(){});
            (function(){return Promise.resolve();})('https://abacus.disabled/hit/' + ns + '/paid_click_total', { mode: 'cors', keepalive: true }).catch(function(){});
            (function(){return Promise.resolve();})('https://abacus.disabled/hit/' + ns + '/paid_click', { mode: 'cors', keepalive: true }).catch(function(){});

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
              (function(){return Promise.resolve();})('https://abacus.disabled/hit/' + ns + '/read_complete', { mode: 'cors', keepalive: true }).catch(function(){});
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
            (function(){return Promise.resolve();})('https://abacus.disabled/hit/' + ns + '/pv_' + kst, { mode: 'cors', keepalive: true }).catch(function(){});
            (function(){return Promise.resolve();})('https://abacus.disabled/hit/' + ns + '/pv_total', { mode: 'cors', keepalive: true }).catch(function(){});
            if (localStorage.getItem('hq_uv_' + ns + '_' + kst) !== '1') {
              localStorage.setItem('hq_uv_' + ns + '_' + kst, '1');
              (function(){return Promise.resolve();})('https://abacus.disabled/hit/' + ns + '/uv_' + kst, { mode: 'cors', keepalive: true }).catch(function(){});
            }
            if (localStorage.getItem('hq_uv_ever_' + ns) !== '1') {
              localStorage.setItem('hq_uv_ever_' + ns, '1');
              (function(){return Promise.resolve();})('https://abacus.disabled/hit/' + ns + '/uv_total', { mode: 'cors', keepalive: true }).catch(function(){});
            }
          }
        }
      } catch (_err) {}
    })();
