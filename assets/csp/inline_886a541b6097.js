function jumpFromManualToJpMail() {
      if (typeof window.closeGbaStarterManualModal === 'function') window.closeGbaStarterManualModal();
      const lead = document.getElementById('gba-substack-subscribe');
      if (lead && lead.scrollIntoView) lead.scrollIntoView({ behavior: 'smooth', block: 'center' });
    }
