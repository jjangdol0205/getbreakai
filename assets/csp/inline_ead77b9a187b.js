(function() {
      var activeWhopPlan = 'monthly';

      function ensureWhopLoaderScript() {
        if (document.querySelector('script[src*="js.whop.com/static/checkout/loader.js"]')) return;
        var s = document.createElement('script');
        s.src = 'https://js.whop.com/static/checkout/loader.js';
        s.async = true;
        s.defer = true;
        document.head.appendChild(s);
      }

      function mountGbaWhopEmbed(planKey) {
        var mount = document.getElementById('gbaWhopEmbedMount');
        var directBtn = document.getElementById('gbaWhopDirectTabBtn');
        var planObj = (typeof window.resolveGbaWhopPlan === 'function')
          ? window.resolveGbaWhopPlan(planKey)
          : {
              plan_id: planKey === 'annual' ? 'plan_ahYIXbLDE0CsQ' : 'plan_UtG9mA9L5pZIS',
              purchase_url: planKey === 'annual' ? 'https://whop.com/checkout/plan_ahYIXbLDE0CsQ' : 'https://whop.com/checkout/plan_UtG9mA9L5pZIS',
              redirect_url: planKey === 'annual' ? 'https://getbreakai.com/jp/?payment=success&provider=whop&plan=annual' : 'https://getbreakai.com/jp/?payment=success&provider=whop&plan=monthly'
            };
        if (directBtn && planObj.purchase_url) {
          directBtn.setAttribute('href', planObj.purchase_url);
        }
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
        if (savedEmail && savedEmail.indexOf('@') !== -1) {
          embedDiv.setAttribute('data-whop-checkout-prefill-email', savedEmail);
        }
        mount.appendChild(embedDiv);
      }

      window.selectGbaWhopPlan = function(plan) {
        activeWhopPlan = (String(plan || '').toLowerCase() === 'annual') ? 'annual' : 'monthly';
        document.querySelectorAll('[data-gba-whop-tab]').forEach(function(btn) {
          var isAct = btn.getAttribute('data-gba-whop-tab') === activeWhopPlan;
          btn.classList.toggle('is-active', isAct);
          btn.setAttribute('aria-pressed', isAct ? 'true' : 'false');
        });
        var modal = document.getElementById('gbaWhopCheckoutModal');
        if (modal && modal.classList.contains('is-open')) {
          mountGbaWhopEmbed(activeWhopPlan);
        }
      };

      window.openGbaWhopCheckoutModal = function(plan) {
        activeWhopPlan = (String(plan || '').toLowerCase() === 'annual') ? 'annual' : 'monthly';
        var modal = document.getElementById('gbaWhopCheckoutModal');
        if (!modal) {
          var fallbackPlan = window.resolveGbaWhopPlan ? window.resolveGbaWhopPlan(activeWhopPlan) : null;
          if (fallbackPlan && fallbackPlan.purchase_url) window.location.href = fallbackPlan.purchase_url;
          return;
        }
        modal.classList.add('is-open');
        modal.setAttribute('aria-hidden', 'false');
        document.querySelectorAll('[data-gba-whop-tab]').forEach(function(btn) {
          var isAct = btn.getAttribute('data-gba-whop-tab') === activeWhopPlan;
          btn.classList.toggle('is-active', isAct);
          btn.setAttribute('aria-pressed', isAct ? 'true' : 'false');
        });
        mountGbaWhopEmbed(activeWhopPlan);
      };

      window.closeGbaWhopCheckoutModal = function() {
        var modal = document.getElementById('gbaWhopCheckoutModal');
        if (!modal) return;
        modal.classList.remove('is-open');
        modal.setAttribute('aria-hidden', 'true');
      };

      // Backward-compatible aliases
      window.openGbaVipWaitlistModal = window.openGbaWhopCheckoutModal;
      window.closeGbaVipWaitlistModal = window.closeGbaWhopCheckoutModal;

      document.addEventListener('click', function(ev) {
        var modal = document.getElementById('gbaWhopCheckoutModal');
        if (modal && modal.classList.contains('is-open') && ev.target === modal) {
          window.closeGbaWhopCheckoutModal();
        }
      });
      document.addEventListener('keydown', function(ev) {
        if (ev.key === 'Escape') {
          window.closeGbaWhopCheckoutModal();
        }
      });
    })();
