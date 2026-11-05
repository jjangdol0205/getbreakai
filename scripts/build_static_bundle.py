"""
scripts/build_static_bundle.py
Builds the production frontend bundle from frontend/src/* and frontend/public/*
and synchronizes identical outputs to:
  1. frontend/dist/
  2. dist/
  3. ./ (repo root static files)
"""
import pathlib
import re
import shutil

ROOT = pathlib.Path(__file__).resolve().parent.parent
FE = ROOT / "frontend"
DIST = FE / "dist"
ROOT_DIST = ROOT / "dist"
PUB = FE / "public"

MODULE_ORDER = [
    "src/locales/i18n.js",
    "src/services/api.js",
    "src/components/PositionDoctor.js",
    "src/components/Header.js",
    "src/components/Hero.js",
    "src/components/ProofCard.js",
    "src/components/StockTable.js",
    "src/components/ProVault.js",
    "src/components/Pricing.js",
    "src/components/Modals.js",
    "src/components/SemiFearGreedView.js",
    "src/main.js",
]


def strip_imports_and_exports(code: str) -> str:
    code = re.sub(r"^\s*import\s+[\s\S]*?from\s+[\"'][^\"']+[\"'];?\s*$", "", code, flags=re.M)
    code = re.sub(r"^\s*import\s+[\"'][^\"']+[\"'];?\s*$", "", code, flags=re.M)
    code = re.sub(r"^\s*export\s+(async\s+function|function|const|let|var)\s+", r"\1 ", code, flags=re.M)
    return code


def main() -> None:
    chunks = []
    for rel in MODULE_ORDER:
        raw = (FE / rel).read_text(encoding="utf-8")
        chunks.append(f"// --- {rel} ---\n{strip_imports_and_exports(raw)}")
    bundled_js = "\n\n".join(chunks)
    css_raw = (FE / "src/styles/theme.css").read_text(encoding="utf-8")

    js_name = "index-BIziPp23.js"
    css_name = "index-CaOpdap3.css"

    index_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <script>window.__DEFAULT_VIEW__ = 'rightside';</script>
  <meta charset="UTF-8" />
  <meta name="google-site-verification" content="nAGlJMEUUPifbzSd8X4PCaBIyr3DtTwaa1a-q9zkbBc" />
  <meta name="google-site-verification" content="G99bl17UU6iKgNm5ndGcSWp0dHFpJ0MjJqBBp0Exfx0" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>RightSideAlpha × SemiFearGreed | 72 US Equity PW-RSI Turnaround Terminal & Semiconductor Fear & Greed Index</title>
  <meta name="description" content="Real-time CNN-Edition Semiconductor Fear & Greed Index (0-100), $SMH/$XLV 70:30 & 80:20 Contrarian Barbell Rebalancing Engine, and 72 US Equity Post-Washout Right-Side Ignition (PW-RSI) Terminal." />
  <link rel="canonical" href="https://truthofmarket.com/" />
  <link rel="alternate" type="application/rss+xml" title="RightSideAlpha × SemiFearGreed RSS Feed" href="https://truthofmarket.com/rss.xml" />
  <meta property="og:type" content="website" />
  <meta property="og:site_name" content="RightSideAlpha × SemiFearGreed" />
  <meta property="og:title" content="RightSideAlpha × SemiFearGreed | 72 US Equity PW-RSI & Semiconductor Fear & Greed Index" />
  <meta property="og:description" content="Real-time CNN-Edition Semiconductor Fear & Greed Index (0-100), $SMH/$XLV 70:30 & 80:20 Contrarian Barbell Rebalancing Engine, and 72 US Equity Post-Washout Right-Side Ignition (PW-RSI) Terminal." />
  <meta property="og:url" content="https://truthofmarket.com/" />
  <meta property="og:image" content="https://truthofmarket.com/og-preview.png" />
  <meta name="twitter:card" content="summary_large_image" />
  <meta name="twitter:title" content="RightSideAlpha × SemiFearGreed | 72 US Equity PW-RSI & Semiconductor Fear & Greed Index" />
  <meta name="twitter:description" content="Real-time CNN-Edition Semiconductor Fear & Greed Index (0-100), $SMH/$XLV 70:30 & 80:20 Contrarian Barbell Rebalancing Engine, and 72 US Equity Post-Washout Right-Side Ignition (PW-RSI) Terminal." />
  <meta name="twitter:image" content="https://truthofmarket.com/og-preview.png" />
  <link rel="icon" type="image/svg+xml" href="./favicon.svg" />
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&family=JetBrains+Mono:wght@500;600;700;800&family=Noto+Sans+JP:wght@400;600;700&family=Noto+Sans+KR:wght@400;600;700&display=swap" rel="stylesheet" />
  <script src="https://assets.lemonsqueezy.com/lemon.js" defer></script>
  <script type="module" crossorigin src="./assets/{js_name}"></script>
  <link rel="stylesheet" crossorigin href="./assets/{css_name}" />
  <script>
  /* === HQ Edge Real-Human Visitor & KPI Beacon (tom_truthofmarket) === */
  (function(){{
    try {{
      if (typeof window === 'undefined' || typeof navigator === 'undefined') return;
      if (window.__HQ_BEACON_SENT_tom_truthofmarket__) return;
      window.__HQ_BEACON_SENT_tom_truthofmarket__ = true;
      var ua = navigator.userAgent || '';
      if (navigator.webdriver || /bot|crawl|spider|slurp|headless|lighthouse|gtmetrix|pingdom|uptimerobot|python|curl|node|axios/i.test(ua)) return;
      var host = (location && location.hostname) || '';
      if (!host || host === 'localhost' || host === '127.0.0.1') return;
      var kst = new Date(Date.now() + 9 * 3600 * 1000).toISOString().slice(0, 10);
      var ns = 'tom_truthofmarket';
      fetch('https://abacus.jasoncameron.dev/hit/' + ns + '/pv_' + kst, {{ mode: 'cors', keepalive: true }}).catch(function(){{}});
      if (localStorage.getItem('hq_uv_' + ns + '_' + kst) !== '1') {{
        localStorage.setItem('hq_uv_' + ns + '_' + kst, '1');
        fetch('https://abacus.jasoncameron.dev/hit/' + ns + '/uv_' + kst, {{ mode: 'cors', keepalive: true }}).catch(function(){{}});
      }}
      document.addEventListener('click', function(e) {{
        var el = e.target && e.target.closest ? e.target.closest('a, button, [role="button"]') : null;
        if (!el) return;
        var href = (el.getAttribute('href') || '').toLowerCase();
        var txt = (el.innerText || el.textContent || '').toLowerCase();
        if (href.indexOf('lemonsqueezy.com') !== -1 || href.indexOf('truthofmarketss') !== -1 || /pro|vip|unlock|subscribe|upgrade|checkout|\$19|\$29|\$49/.test(txt)) {{
          fetch('https://abacus.jasoncameron.dev/hit/' + ns + '/paid_click_' + kst, {{ mode: 'cors', keepalive: true }}).catch(function(){{}});
        }}
      }}, true);
    }} catch (e) {{}}
  }})();
  </script>
</head>
<body>
  <div id="app"></div>
</body>
</html>
"""

    # Keep frontend/public/index.html in sync so it can never overwrite with stale tags
    (PUB / "index.html").write_text(index_html, encoding="utf-8")

    # Remove deprecated/leak files from public source before copying
    for stale_rel in ["instagram_us_setup.html", "static_api/stocks_pro.json", "static_api/smh_xlv_fear_greed_history.csv"]:
        sp = PUB / stale_rel
        if sp.exists():
            sp.unlink()

    for target_dir in [DIST, ROOT_DIST, ROOT]:
        assets_d = target_dir / "assets"
        assets_d.mkdir(parents=True, exist_ok=True)
        (assets_d / js_name).write_text(bundled_js, encoding="utf-8")
        (assets_d / css_name).write_text(css_raw, encoding="utf-8")
        for item in PUB.iterdir():
            if item.name in ("index.html", "instagram_us_setup.html"):
                continue
            dest = target_dir / item.name
            if item.is_dir():
                shutil.copytree(item, dest, dirs_exist_ok=True)
            else:
                shutil.copy2(item, dest)
        # Write index.html AFTER copying public files so it is never overwritten
        (target_dir / "index.html").write_text(index_html, encoding="utf-8")
        for stale_rel in ["instagram_us_setup.html", "static_api/stocks_pro.json", "static_api/smh_xlv_fear_greed_history.csv"]:
            tp = target_dir / stale_rel
            if tp.exists():
                tp.unlink()

    print(f"Built & synced frontend/dist, ./dist, and root static bundle ({js_name}, {css_name})")


if __name__ == "__main__":
    main()
