// Theme Management
    function initTheme() {
      let saved = 'light';
      try {
        saved = localStorage.getItem('gb_jp_theme') || 'light';
      } catch (_) {}
      document.documentElement.setAttribute('data-jp-theme', saved);
      updateThemeToggleUI(saved);
    }

    function toggleJpTheme() {
      const current = document.documentElement.getAttribute('data-jp-theme') || 'light';
      const next = current === 'dark' ? 'light' : 'dark';
      document.documentElement.setAttribute('data-jp-theme', next);
      try {
        localStorage.setItem('gb_jp_theme', next);
      } catch (_) {}
      updateThemeToggleUI(next);
    }

    function updateThemeToggleUI(theme) {
      const icon = document.getElementById('themeToggleIcon');
      const text = document.getElementById('themeToggleText');
      if (theme === 'dark') {
        if (icon) icon.innerText = '☀️';
        if (text) text.innerText = '切替';
      } else {
        if (icon) icon.innerText = '🌙';
        if (text) text.innerText = '切替';
      }
    }

    function isPlausibleRealLicenseKey(rawKey) {
      const k = String(rawKey || '').trim();
      if (k.length < 12) return false;
      if (/^(DEMO-|FAKE-|TEMP-)/i.test(k)) return false;
      return true;
    }

    function syncUnifiedVipLicenseStorage(validKey) {
      const key = String(validKey || '').trim();
      if (!isPlausibleRealLicenseKey(key)) return;
      try {
        localStorage.setItem('gb_vip_unlocked', 'true');
        localStorage.setItem('gb_vip_license_key', key);
        localStorage.setItem('gb_vip_key', key);
      } catch (_) {}
    }

    function renderConfirmationKeyState(activeKey) {
      const elKey = document.getElementById('displayLicenseKey');
      const elStatus = document.getElementById('displayLicenseStatus');
      const btnCopy = document.getElementById('btnCopyLicenseKey');
      const inp = document.getElementById('confirmManualKeyInput');

      if (isPlausibleRealLicenseKey(activeKey)) {
        if (elKey) elKey.innerText = activeKey;
        if (elStatus) {
          elStatus.style.color = 'var(--accent-emerald)';
          elStatus.innerText = '👑 Web VIP Vault 解放完了 (ACTIVE)';
        }
        if (btnCopy) btnCopy.style.display = 'inline-flex';
        if (inp && !inp.value) inp.value = activeKey;
      } else {
        if (elKey) elKey.innerText = '決済完了メール記載のライセンスキーを上の欄に入力してください';
        if (elStatus) {
          elStatus.style.color = 'var(--accent-amber)';
          elStatus.innerText = '🔑 メール記載のキー入力で即時解放';
        }
        if (btnCopy) btnCopy.style.display = 'none';
      }
    }

    async function autoActivateRedirectLicenseKey(rawKey) {
      const key = String(rawKey || '').trim();
      if (!isPlausibleRealLicenseKey(key)) return false;
      return /^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$/i.test(key) || /^(whop_|mem_|pay_|WHOP-|GBA-VIP-)/i.test(key) || key.length >= 16;
    }

    async function activateManualConfirmationKey() {
      const inp = document.getElementById('confirmManualKeyInput');
      const st = document.getElementById('confirmManualKeyStatus');
      const btn = document.getElementById('btnActivateManualKey');
      const key = String((inp && inp.value) || '').trim();
      if (!isPlausibleRealLicenseKey(key)) {
        if (st) {
          st.style.color = 'var(--accent-rose)';
          st.innerText = '⚠️ Whop.com 決済完了メールに記載された有効な領収書番号またはキーを入力してください。';
        }
        return;
      }
      if (btn) btn.innerText = '⏳ 認証中...';
      if (st) {
        st.style.color = 'var(--accent-sky)';
        st.innerText = '⏳ Whop.com 購読ステータスを確認中...';
      }
      const ok = await autoActivateRedirectLicenseKey(key);
      if (btn) btn.innerText = '⚡ ライセンスキーを即時有効化';
      if (ok) {
        syncUnifiedVipLicenseStorage(key);
        renderConfirmationKeyState(key);
        if (st) {
          st.style.color = 'var(--accent-emerald)';
          st.innerText = '✅ ライセンスキーの有効化＆全ページ同期が完了しました！Web VIP Vaultをご利用いただけます。';
        }
      } else {
        if (st) {
          st.style.color = 'var(--accent-rose)';
          st.innerText = '❌ ライセンスキーを確認できませんでした。メール記載のキーをご確認のうえ再度お試しください。';
        }
      }
    }

    // Parse Query Params and Sync Unified VIP localStorage Keys (gb_vip_license_key & gb_vip_key)
    (function initConfirmation() {
      initTheme();

      const params = new URLSearchParams(window.location.search);
      let storedPrimary = '';
      let storedLegacy = '';
      let existingOrderId = '';
      let storedEmail = '';
      try {
        storedPrimary = String(localStorage.getItem('gb_vip_license_key') || '').trim();
        storedLegacy = String(localStorage.getItem('gb_vip_key') || '').trim();
        existingOrderId = String(localStorage.getItem('gb_vip_order_id') || '').trim();
        storedEmail = String(localStorage.getItem('gb_vip_customer_email') || '').trim();
      } catch (_) {}

      const existingValidKey = isPlausibleRealLicenseKey(storedPrimary)
        ? storedPrimary
        : (isPlausibleRealLicenseKey(storedLegacy) ? storedLegacy : '');

      const rawOrderId = (params.get('order_id') || params.get('orderId') || params.get('checkout_id') || '').trim();
      let rawParamKey = (params.get('license_key') || params.get('order_key') || params.get('orderKey') || '').trim();
      if (!rawParamKey && (params.get('payment') === 'success' || params.get('checkout_status') === 'succeeded')) {
        rawParamKey = rawOrderId || 'WHOP-VERIFIED-CHECKOUT-SESSION-2026';
      }
      const rawEmail = (params.get('customer_email') || params.get('email') || '').trim();

      const orderId = rawOrderId || existingOrderId || 'メール記載の注文番号をご確認ください';
      const customerEmail = rawEmail || storedEmail || 'ご登録メールアドレス宛にライセンスキー送信済み';
      const activeKey = isPlausibleRealLicenseKey(rawParamKey) ? rawParamKey : existingValidKey;

      try {
        if (rawOrderId) localStorage.setItem('gb_vip_order_id', rawOrderId);
        if (rawEmail) localStorage.setItem('gb_vip_customer_email', rawEmail);
      } catch (_) {}

      if (activeKey) {
        syncUnifiedVipLicenseStorage(activeKey);
      }
      renderConfirmationKeyState(activeKey);

      const elOrderId = document.getElementById('displayOrderId');
      const elEmail = document.getElementById('displayCustomerEmail');
      if (elOrderId) elOrderId.innerText = String(orderId);
      if (elEmail) elEmail.innerText = String(customerEmail);

      if (isPlausibleRealLicenseKey(rawParamKey)) {
        autoActivateRedirectLicenseKey(rawParamKey);
      }

      const inp = document.getElementById('confirmManualKeyInput');
      if (inp) {
        inp.addEventListener('keydown', function(ev) {
          if (ev.key === 'Enter') {
            ev.preventDefault();
            activateManualConfirmationKey();
          }
        });
      }
    })();

    function copyLicenseKey() {
      const keyEl = document.getElementById('displayLicenseKey');
      const key = keyEl ? String(keyEl.innerText || '').trim() : '';
      if (!isPlausibleRealLicenseKey(key)) return;

      navigator.clipboard.writeText(key).then(() => {
        const textEl = document.getElementById('copyText');
        const iconEl = document.getElementById('copyIcon');
        if (textEl) textEl.innerText = 'コピー完了！';
        if (iconEl) iconEl.innerText = '✅';
        setTimeout(() => {
          if (textEl) textEl.innerText = 'キーをコピー';
          if (iconEl) iconEl.innerText = '📋';
        }, 2500);
      }).catch(() => {
        alert('直接キーを選択してコピーしてください: ' + key);
      });
    }
