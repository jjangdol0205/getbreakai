function copyById(id, label) {
      const text = document.getElementById(id).innerText;
      navigator.clipboard.writeText(text).then(() => {
        const t = document.getElementById('toast');
        t.innerText = '✅ ' + label + ' — all 24 prompts copied!';
        t.style.display = 'block';
        setTimeout(() => { t.style.display = 'none'; }, 2200);
      });
    }
