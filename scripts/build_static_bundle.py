"""
scripts/build_static_bundle.py
Builds the production frontend bundle from frontend/src/* and frontend/public/*
and synchronizes identical outputs to:
  1. frontend/dist/
  2. dist/
  3. ./ (repo root static files)
"""
from datetime import datetime, timezone
from email.utils import format_datetime
import json
import pathlib
import re
import shutil
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.generate_seo_stock_pages import generate_all_seo_pages

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


def refresh_health_and_rss() -> tuple[str, str]:
    now_utc = datetime.now(timezone.utc)
    iso_now = now_utc.strftime("%Y-%m-%dT%H:%M:%SZ")
    rfc_now = format_datetime(now_utc)

    semi_path = ROOT / "static_api" / "semi_overview.json"
    stocks_path = ROOT / "static_api" / "stocks_free.json"
    as_of_date = "2026-11-05"
    fg_score = 18.0
    regime_code = "EXTREME_FEAR"
    smh_close = 504.48
    smh_dd_pct = -24.58
    celh_close = 30.04
    celh_stop = 27.34
    celh_tp1 = 60.08

    if semi_path.exists():
        try:
            ov = json.loads(semi_path.read_text(encoding="utf-8"))
            as_of_date = str(ov.get("date") or as_of_date)
            fg_score = float(ov.get("fg_score") or fg_score)
            regime_code = str(ov.get("regime_code") or regime_code)
            smh_close = float(ov.get("smh_close") or smh_close)
            smh_dd_pct = float(ov.get("smh_dd_pct") or smh_dd_pct)
        except Exception:
            pass

    if stocks_path.exists():
        try:
            st = json.loads(stocks_path.read_text(encoding="utf-8"))
            for row in st:
                if row.get("ticker") == "CELH":
                    celh_close = float(row.get("close") or celh_close)
                    celh_stop = round(celh_close * 0.91, 2)
                    celh_tp1 = round(celh_close * 2.0, 2)
                    break
        except Exception:
            pass

    health_obj = {
        "status": "ok",
        "mode": "static",
        "as_of_date": as_of_date,
        "updated_at": iso_now,
        "services": ["RightSideAlpha", "SemiFearGreed"],
    }
    health_json = json.dumps(health_obj, indent=2) + "\n"

    rss_xml = f"""<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom">
  <channel>
    <title>RightSideAlpha x SemiFearGreed | US Equity Quant Terminal &amp; Semiconductor Fear &amp; Greed Index</title>
    <link>https://truthofmarket.com/</link>
    <atom:link href="https://truthofmarket.com/rss.xml" rel="self" type="application/rss+xml" />
    <atom:link href="https://pubsubhubbub.appspot.com/" rel="hub" />
    <description>Institutional US Equity Post-Washout Right-Side Ignition (PW-RSI) Quant Terminal covering 72 US equities, daily $SMH Semiconductor Fear &amp; Greed Index (0-100), and $SMH/$XLV contrarian barbell allocation.</description>
    <language>en-US</language>
    <lastBuildDate>{rfc_now}</lastBuildDate>
    <item>
      <title><![CDATA[RightSideAlpha x SemiFearGreed — 72 US Equity PW-RSI Turnaround Terminal & 26.8-Year Backtest (As of {as_of_date})]]></title>
      <link>https://truthofmarket.com/</link>
      <guid isPermaLink="true">https://truthofmarket.com/</guid>
      <pubDate>{rfc_now}</pubDate>
      <description><![CDATA[Live institutional US equity quant screener (as of {as_of_date}) tracking 72 liquid US stocks across 52-week washout bottoms, right-side SMA20/SMA60 turnaround ignition triggers, -9.0% mechanical hard-stop protection, and 2x (TP1 +100%) asymmetric profit targets.]]></description>
    </item>
    <item>
      <title><![CDATA[CNN-Edition Semiconductor Fear & Greed Index ($SMH {fg_score:.1f} {regime_code}) & $SMH/$XLV 80:20 Contrarian Barbell Engine]]></title>
      <link>https://truthofmarket.com/semi-fear-greed.html</link>
      <guid isPermaLink="true">https://truthofmarket.com/semi-fear-greed.html</guid>
      <pubDate>{rfc_now}</pubDate>
      <description><![CDATA[Real-time 5-factor Semiconductor Fear & Greed Index ($SMH Close ${smh_close:.2f}, {smh_dd_pct:.2f}% from 52W High as of {as_of_date}) and regime-based $SMH (VanEck Semiconductor ETF) vs. $XLV (Health Care Select Sector SPDR) contrarian barbell rebalancing simulator.]]></description>
    </item>
    <item>
      <title><![CDATA[Celsius Holdings ($CELH) Institutional Deep-Dive: 52W Bottom Re-Accumulation & PW-RSI Turnaround Analysis (${celh_close:.2f})]]></title>
      <link>https://truthofmarket.com/stocks/celh.html</link>
      <guid isPermaLink="true">https://truthofmarket.com/stocks/celh.html</guid>
      <pubDate>{rfc_now}</pubDate>
      <description><![CDATA[Comprehensive institutional audit of Celsius Holdings ($CELH, Close ${celh_close:.2f} as of {as_of_date}) following its PepsiCo inventory destocking washout: gross margin defense, international expansion catalysts, ${celh_stop:.2f} (-9.0%) hard stop floor, and ${celh_tp1:.2f} (+100% 2x) TP1 target.]]></description>
    </item>
    <item>
      <title><![CDATA[Mobileye Global ($MBLY) Post-Mortem Risk Audit: Rule 1 (-9.0% Hard Stop @ $6.39) Execution & Capital Preservation]]></title>
      <link>https://truthofmarket.com/stocks/mbly.html</link>
      <guid isPermaLink="true">https://truthofmarket.com/stocks/mbly.html</guid>
      <pubDate>{rfc_now}</pubDate>
      <description><![CDATA[Transparent institutional post-mortem on Mobileye Global ($MBLY): how mechanical execution of Rule 1 (-9.0% Hard Stop at $6.39) prevented deeper drawdown after support breakdown and redeployed capital into confirmed right-side leaders.]]></description>
    </item>
    <item>
      <title><![CDATA[NVIDIA ($NVDA) & VanEck Semiconductor ETF ($SMH) Institutional PW-RSI Support/Resistance Audit ({as_of_date})]]></title>
      <link>https://truthofmarket.com/stocks/nvda.html</link>
      <guid isPermaLink="true">https://truthofmarket.com/stocks/nvda.html</guid>
      <pubDate>{rfc_now}</pubDate>
      <description><![CDATA[Daily quantitative screening ({as_of_date}) of NVIDIA ($NVDA), $SMH, $SOXL, $AMD, and $AVGO across 52-week support/resistance levels, 20-day/60-day moving average reclaim triggers, and -9.0% hard-stop risk floors.]]></description>
    </item>
  </channel>
</rss>
"""
    return health_json, rss_xml


def main() -> None:
    chunks = []
    for rel in MODULE_ORDER:
        raw = (FE / rel).read_text(encoding="utf-8")
        chunks.append(f"// --- {rel} ---\n{strip_imports_and_exports(raw)}")
    bundled_js = "\n\n".join(chunks)
    css_raw = (FE / "src/styles/theme.css").read_text(encoding="utf-8")

    js_name = "index-BIziPp23.js"
    css_name = "index-CaOpdap3.css"

    # Generate all 76 static /stocks/<ticker>.html pages, /semi-fear-greed.html, and clean sitemap.xml
    seo_dir_html = generate_all_seo_pages(js_name=js_name, css_name=css_name)

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
      if (window.__HQ_BEACON_SENT_tom_truthofmarket__ || window.__HQ_KPI_TOM__) return;
      window.__HQ_BEACON_SENT_tom_truthofmarket__ = true;
      window.__HQ_KPI_TOM__ = true;
      var ua = navigator.userAgent || '';
      if (navigator.webdriver || /bot|crawl|spider|slurp|headless|lighthouse|gtmetrix|pingdom|uptimerobot|python|curl|node|axios/i.test(ua)) return;
      var host = (location && location.hostname) || '';
      if (!host || host === 'localhost' || host === '127.0.0.1') return;
      var kst = new Date(Date.now() + 9 * 3600 * 1000).toISOString().slice(0, 10);
      var ns = 'tom_truthofmarket';
      fetch('https://abacus.jasoncameron.dev/hit/' + ns + '/pv_' + kst, {{ mode: 'cors', keepalive: true }}).catch(function(){{}});
      fetch('https://abacus.jasoncameron.dev/hit/' + ns + '/pv_total', {{ mode: 'cors', keepalive: true }}).catch(function(){{}});
      if (localStorage.getItem('hq_uv_' + ns + '_' + kst) !== '1') {{
        localStorage.setItem('hq_uv_' + ns + '_' + kst, '1');
        fetch('https://abacus.jasoncameron.dev/hit/' + ns + '/uv_' + kst, {{ mode: 'cors', keepalive: true }}).catch(function(){{}});
      }}
      if (localStorage.getItem('hq_uv_ever_' + ns) !== '1') {{
        localStorage.setItem('hq_uv_ever_' + ns, '1');
        fetch('https://abacus.jasoncameron.dev/hit/' + ns + '/uv_total', {{ mode: 'cors', keepalive: true }}).catch(function(){{}});
      }}
      if (location.search.indexOf('payment=success') !== -1 || location.search.indexOf('unlock=1') !== -1) {{
        if (localStorage.getItem('hq_paid_' + kst) !== '1') {{
          localStorage.setItem('hq_paid_' + kst, '1');
          fetch('https://abacus.jasoncameron.dev/hit/' + ns + '/paid_member_' + kst, {{ mode: 'cors', keepalive: true }}).catch(function(){{}});
          fetch('https://abacus.jasoncameron.dev/hit/' + ns + '/paid_member_total', {{ mode: 'cors', keepalive: true }}).catch(function(){{}});
        }}
      }}
      document.addEventListener('click', function(e) {{
        var el = e.target && e.target.closest ? e.target.closest('a, button, [role="button"]') : null;
        if (!el) return;
        var href = (el.getAttribute('href') || '').toLowerCase();
        var txt = (el.innerText || el.textContent || '').toLowerCase();
        var cls = (el.className || '').toLowerCase();
        if (href.indexOf('lemonsqueezy.com') !== -1 || href.indexOf('truthofmarketss') !== -1 || cls.indexOf('pro') !== -1 || cls.indexOf('paywall') !== -1 || /pro|vip|unlock|subscribe|upgrade|checkout|\\$19|\\$29|\\$49|\\$199|프리미엄|유료|구독/.test(txt)) {{
          fetch('https://abacus.jasoncameron.dev/hit/' + ns + '/paid_click_' + kst, {{ mode: 'cors', keepalive: true }}).catch(function(){{}});
          fetch('https://abacus.jasoncameron.dev/hit/' + ns + '/paid_click_total', {{ mode: 'cors', keepalive: true }}).catch(function(){{}});
        }}
      }}, true);
    }} catch (e) {{}}
  }})();
  </script>
</head>
<body>
  <div id="app"></div>
{seo_dir_html}
</body>
</html>
"""

    health_json, rss_xml = refresh_health_and_rss()

    # Keep frontend/public/index.html, rss.xml, and health.json in sync
    (PUB / "index.html").write_text(index_html, encoding="utf-8")
    (PUB / "rss.xml").write_text(rss_xml, encoding="utf-8")
    (PUB / "static_api").mkdir(parents=True, exist_ok=True)
    (PUB / "static_api" / "health.json").write_text(health_json, encoding="utf-8")
    (ROOT / "static_api" / "health.json").write_text(health_json, encoding="utf-8")

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
        # Write index.html, rss.xml, and static_api/health.json AFTER copying public files
        (target_dir / "index.html").write_text(index_html, encoding="utf-8")
        (target_dir / "rss.xml").write_text(rss_xml, encoding="utf-8")
        (target_dir / "static_api").mkdir(parents=True, exist_ok=True)
        (target_dir / "static_api" / "health.json").write_text(health_json, encoding="utf-8")
        for stale_rel in ["instagram_us_setup.html", "static_api/stocks_pro.json", "static_api/smh_xlv_fear_greed_history.csv"]:
            tp = target_dir / stale_rel
            if tp.exists():
                tp.unlink()

    print(f"Built & synced frontend/dist, ./dist, and root static bundle ({js_name}, {css_name})")


if __name__ == "__main__":
    main()
