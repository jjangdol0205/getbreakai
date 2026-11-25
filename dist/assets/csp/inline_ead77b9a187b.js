(function() {
      var activeWhopPlan = 'monthly';

      function buildDirectGbaWhopUrl(planKey) {
        var pLow = String(planKey || 'monthly').toLowerCase();
        var norm = (pLow === 'starter' || pLow === 'annual') ? pLow : 'monthly';
        var planObj = (typeof window.resolveGbaWhopPlan === 'function')
          ? window.resolveGbaWhopPlan(norm)
          : {
              purchase_url: norm === 'starter'
                ? 'https://whop.com/checkout/plan_j2eaOW4jizw2M'
                : (norm === 'annual' ? 'https://whop.com/checkout/plan_ahYIXbLDE0CsQ' : 'https://whop.com/checkout/plan_UtG9mA9L5pZIS')
            };
        var baseUrl = (planObj && planObj.purchase_url) || 'https://whop.com/checkout/plan_UtG9mA9L5pZIS';
        try {
          var savedEmail = (typeof window.getGbaSavedMemberEmail === 'function') ? window.getGbaSavedMemberEmail() : '';
          if (savedEmail && savedEmail.indexOf('@') !== -1 && typeof URL === 'function') {
            var u = new URL(baseUrl);
            if (!u.searchParams.get('email')) u.searchParams.set('email', savedEmail);
            return u.toString();
          }
        } catch (_) {}
        return baseUrl;
      }

      window.selectGbaWhopPlan = function(plan) {
        var pLow = String(plan || '').toLowerCase();
        activeWhopPlan = (pLow === 'starter' || pLow === 'annual') ? pLow : 'monthly';
      };

      window.openGbaWhopCheckoutModal = function(plan) {
        var pLow = String(plan || activeWhopPlan || 'monthly').toLowerCase();
        activeWhopPlan = (pLow === 'starter' || pLow === 'annual') ? pLow : 'monthly';
        var targetUrl = buildDirectGbaWhopUrl(activeWhopPlan);
        try {
          var win = window.open(targetUrl, '_blank', 'noopener,noreferrer');
          if (!win) window.location.href = targetUrl;
        } catch (_) {
          window.location.href = targetUrl;
        }
      };

      window.closeGbaWhopCheckoutModal = function() {};
      window.openGbaVipWaitlistModal = window.openGbaWhopCheckoutModal;
      window.closeGbaVipWaitlistModal = window.closeGbaWhopCheckoutModal;
    })();
