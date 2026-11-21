function copyText(id) {
      const text = document.getElementById(id).innerText;
      navigator.clipboard.writeText(text).then(() => {
        const t = document.getElementById('toast');
        t.style.display = 'block';
        setTimeout(() => { t.style.display = 'none'; }, 1800);
      });
    }
