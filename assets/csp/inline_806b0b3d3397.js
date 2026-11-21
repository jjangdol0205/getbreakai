function jumpFromManualToJpMail() {
      if (typeof window.closeGbaStarterManualModal === 'function') window.closeGbaStarterManualModal();
      const subBox = document.getElementById('gba-substack-subscribe');
      if (subBox && subBox.scrollIntoView) subBox.scrollIntoView({ behavior: 'smooth', block: 'center' });
      setTimeout(function() {
        const inp = subBox ? subBox.querySelector('input[type="email"]') : null;
        if (inp && inp.focus) inp.focus();
      }, 350);
    }

    window.addEventListener('DOMContentLoaded', function() {
      try {
        const saved = localStorage.getItem('gb_free_member_email') || localStorage.getItem('gba_jp_free_email');
        if (saved) {
          document.querySelectorAll('.substack-inline-form input[type="email"]').forEach(function(inp) { inp.value = saved; });
        }
      } catch (_e) {}
    });
