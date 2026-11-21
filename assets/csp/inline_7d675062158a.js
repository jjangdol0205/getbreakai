(function() {
      window.scrollToGbaManualChapter = function(chapId) {
        var el = chapId ? document.getElementById(chapId) : null;
        if (el && el.scrollIntoView) {
          el.scrollIntoView({ behavior: 'smooth', block: 'start' });
        }
      };

      window.openGbaStarterManualModal = function(chapId) {
        var modal = document.getElementById('gbaStarterManualModal');
        if (!modal) return;
        modal.classList.add('is-open');
        modal.setAttribute('aria-hidden', 'false');
        document.body.style.overflow = 'hidden';
        if (typeof window.isGbaInAppWebView === 'function' && window.isGbaInAppWebView()) {
          var notice = document.getElementById('gbaManualWebViewNotice');
          var pBtn = document.getElementById('btnPrintOrMailGbaManual');
          if (notice) notice.style.display = 'block';
          if (pBtn) pBtn.innerText = 'このマニュアルをメールで受け取る';
        }
        try {
          var saved = localStorage.getItem('gb_free_member_email') || localStorage.getItem('gba_jp_free_email') || '';
          var mInp = document.getElementById('gbaManualDeliveryEmail');
          if (mInp && saved && !mInp.value) mInp.value = saved;
        } catch (_e) {}
        if (chapId) {
          setTimeout(function() { window.scrollToGbaManualChapter(chapId); }, 60);
        } else {
          modal.scrollTop = 0;
        }
      };

      window.closeGbaStarterManualModal = function() {
        var modal = document.getElementById('gbaStarterManualModal');
        if (!modal) return;
        modal.classList.remove('is-open');
        modal.setAttribute('aria-hidden', 'true');
        document.body.classList.remove('printing-gba-manual');
        document.body.style.overflow = '';
      };

      window.printGbaStarterManual = function() {
        var modal = document.getElementById('gbaStarterManualModal');
        if (modal && !modal.classList.contains('is-open')) {
          window.openGbaStarterManualModal();
        }
        if (typeof window.isGbaInAppWebView === 'function' && window.isGbaInAppWebView()) {
          var notice = document.getElementById('gbaManualWebViewNotice');
          if (notice) notice.style.display = 'block';
          var box = document.getElementById('gbaManualWebViewMailBox');
          if (box && box.scrollIntoView) box.scrollIntoView({ behavior: 'smooth', block: 'start' });
          var inp = document.getElementById('gbaManualDeliveryEmail');
          setTimeout(function() { if (inp && inp.focus) inp.focus(); }, 120);
          return false;
        }
        document.body.classList.add('printing-gba-manual');
        setTimeout(function() {
          try { window.print(); } catch (_e) {}
          setTimeout(function() { document.body.classList.remove('printing-gba-manual'); }, 400);
        }, 80);
        return false;
      };

      window.submitGbaManualEmailDelivery = function(ev) {
        if (ev && ev.preventDefault) ev.preventDefault();
        var inp = document.getElementById('gbaManualDeliveryEmail');
        var st = document.getElementById('gbaManualDeliveryStatus');
        var email = String(inp ? inp.value : '').trim().toLowerCase();
        if (!/^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(email)) {
          if (inp && inp.focus) inp.focus();
          return false;
        }
        try {
          localStorage.setItem('gb_free_member_email', email);
          localStorage.setItem('gba_jp_free_email', email);
        } catch (_e) {}
        if (typeof window.trackGbaFreeSignup === 'function') {
          window.trackGbaFreeSignup(email);
        }
        if (window.DreamCompanyCRM && typeof window.DreamCompanyCRM.registerMember === 'function') {
          window.DreamCompanyCRM.registerMember({
            div: 'GBA',
            email: email,
            segment: 'nisa_wealth_defense',
            lang: 'ja-JP',
            notes: 'site=getbreakai.com | manual_email_delivery'
          }).catch(function(){});
        }
        if (st) {
          st.style.display = 'block';
          st.innerHTML = '<strong>ご登録ありがとうございます。</strong>保存版マニュアルと毎朝8時の「朝刊リサーチノート」を <strong>' + email.replace(/[<>&"]/g, '') + '</strong> 宛にお届けいたします。';
        }
        return false;
      };

      window.addEventListener('DOMContentLoaded', function() {
        if (typeof window.isGbaInAppWebView === 'function' && window.isGbaInAppWebView()) {
          var pBtn = document.getElementById('btnPrintOrMailGbaManual');
          var notice = document.getElementById('gbaManualWebViewNotice');
          if (pBtn) pBtn.innerText = 'このマニュアルをメールで受け取る';
          if (notice) notice.style.display = 'block';
          document.querySelectorAll('.gba-manual-sub-badge').forEach(function(b) {
            b.innerText = 'メール保存・画面閲覧対応 ／ 楽天証券・SBI証券 対応';
          });
        }
      });
    })();
