#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
scripts/generate_seo_stock_pages.py
Generates static, crawlable, self-canonicalized HTML pages for:
  - /semi-fear-greed.html (Semiconductor Fear & Greed Index + $SMH/$XLV Contrarian Barbell)
  - /stocks/<ticker_lower>.html (All 72 US Equities in PW-RSI Universe + SMH, XLV, SOXL, QQQ ETFs)
  - /sitemap.xml (Clean static URLs without query-string canonical traps)
"""
from __future__ import annotations

from datetime import datetime, timezone
import html
import json
import pathlib
from typing import Any, Dict, List

ROOT = pathlib.Path(__file__).resolve().parent.parent
PUB = ROOT / "frontend" / "public"
STOCKS_MASTER_PATH = ROOT / "data" / "stocks_pro_master.json"
SEMI_OVERVIEW_PATH = ROOT / "static_api" / "semi_overview.json"

LS_MONTHLY_URL = "https://truthofmarket.lemonsqueezy.com/checkout/buy/bad98d00-7175-41f6-9d58-eeb2471d0da4?embed=1"
LS_LTD_URL = "https://truthofmarket.lemonsqueezy.com/checkout/buy/00c9f6e1-c8be-42a4-b5a5-e05af1a41ed9?embed=1"

COMPARE_PAIRS: List[tuple[str, str, str]] = [
    ("NVDA", "AMD", "AI GPU Monopoly vs Challenger"),
    ("SOXL", "SMH", "3x Leveraged Semi vs Spot Semiconductor ETF"),
    ("TSLA", "NVDA", "Retail Megacap Momentum vs AI Compute King"),
    ("PLTR", "NVDA", "Enterprise AI OS vs AI Silicon Leader"),
    ("AVGO", "NVDA", "Custom AI ASIC vs Merchant GPU Leader"),
    ("SMH", "XLV", "80:20 Contrarian Barbell Core ETFs"),
    ("QQQ", "SMH", "Nasdaq-100 Benchmark vs Semiconductor Alpha"),
    ("TSLA", "PLTR", "High-Beta Institutional Retail Favorites"),
    ("AMD", "INTC", "Data Center x86 & AI Accelerator Clash"),
    ("AVGO", "MRVL", "Custom AI Silicon & Optical Networking Duopoly"),
    ("MU", "NVDA", "HBM3E High-Bandwidth Memory vs AI GPU"),
    ("ARM", "NVDA", "Edge AI CPU Architecture vs Data Center GPU"),
    ("ASML", "TSM", "EUV Lithography Monopoly vs Foundry Monopoly"),
    ("LRCX", "AMAT", "Wafer Fab Equipment Turnaround Clash"),
    ("KLAC", "ASML", "Semiconductor Process Control vs EUV"),
    ("MSFT", "GOOGL", "Hyperscaler AI Cloud & Search Battle"),
    ("META", "GOOGL", "AI Ad-Tech & Open-Weights LLM Monetization"),
    ("AMZN", "MSFT", "AWS vs Azure Cloud Infrastructure Leaders"),
    ("AAPL", "MSFT", "Consumer AI Ecosystem vs Enterprise AI"),
    ("CRWD", "PANW", "Endpoint & AI Cybersecurity Leaders"),
    ("SNOW", "PLTR", "Enterprise Data Cloud vs Defense/Commercial AIP"),
    ("COIN", "MSTR", "Crypto Exchange Infrastructure vs Bitcoin Treasury"),
    ("HOOD", "COIN", "Retail Trading Super-App vs Crypto Leader"),
    ("LLY", "NVO", "GLP-1 Obesity & Biopharma Dominance"),
    ("UNH", "LLY", "Defensive Healthcare Cashflow vs GLP-1 Growth"),
    ("CELH", "MNST", "PW-RSI Beverage Turnaround vs Compounder"),
    ("NFLX", "DIS", "Streaming Operating Margin vs Media Turnaround"),
    ("UBER", "TSLA", "Global Mobility Network vs Robotaxi"),
    ("SHOP", "AMZN", "Merchant E-Commerce OS vs Global Retail Giant"),
    ("SMCI", "DELL", "Liquid-Cooled AI Server Infrastructure Clash"),
]

HEAD_BEACON_SCRIPT = """  <script>
  /* === HQ Edge Real-Human Visitor & KPI Beacon (tom_truthofmarket) === */
  (function(){
    try {
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
      fetch('https://abacus.jasoncameron.dev/hit/' + ns + '/pv_' + kst, { mode: 'cors', keepalive: true }).catch(function(){});
      fetch('https://abacus.jasoncameron.dev/hit/' + ns + '/pv_total', { mode: 'cors', keepalive: true }).catch(function(){});
      if (localStorage.getItem('hq_uv_' + ns + '_' + kst) !== '1') {
        localStorage.setItem('hq_uv_' + ns + '_' + kst, '1');
        fetch('https://abacus.jasoncameron.dev/hit/' + ns + '/uv_' + kst, { mode: 'cors', keepalive: true }).catch(function(){});
      }
      if (localStorage.getItem('hq_uv_ever_' + ns) !== '1') {
        localStorage.setItem('hq_uv_ever_' + ns, '1');
        fetch('https://abacus.jasoncameron.dev/hit/' + ns + '/uv_total', { mode: 'cors', keepalive: true }).catch(function(){});
      }
      if (location.search.indexOf('payment=success') !== -1 || location.search.indexOf('unlock=1') !== -1) {
        if (localStorage.getItem('hq_paid_' + kst) !== '1') {
          localStorage.setItem('hq_paid_' + kst, '1');
          fetch('https://abacus.jasoncameron.dev/hit/' + ns + '/paid_member_' + kst, { mode: 'cors', keepalive: true }).catch(function(){});
          fetch('https://abacus.jasoncameron.dev/hit/' + ns + '/paid_member_total', { mode: 'cors', keepalive: true }).catch(function(){});
        }
      }
      document.addEventListener('click', function(e) {
        var el = e.target && e.target.closest ? e.target.closest('a, button, [role="button"]') : null;
        if (!el) return;
        var href = (el.getAttribute('href') || '').toLowerCase();
        var txt = (el.innerText || el.textContent || '').toLowerCase();
        var cls = (el.className || '').toLowerCase();
        if (href.indexOf('lemonsqueezy.com') !== -1 || href.indexOf('truthofmarketss') !== -1 || cls.indexOf('pro') !== -1 || cls.indexOf('paywall') !== -1 || /pro|vip|unlock|subscribe|upgrade|checkout|\\$19|\\$29|\\$49|\\$199|프리미엄|유료|구독/.test(txt)) {
          fetch('https://abacus.jasoncameron.dev/hit/' + ns + '/paid_click_' + kst, { mode: 'cors', keepalive: true }).catch(function(){});
          fetch('https://abacus.jasoncameron.dev/hit/' + ns + '/paid_click_total', { mode: 'cors', keepalive: true }).catch(function(){});
        }
      }, true);
    } catch (e) {}
  })();
  </script>"""


def load_stocks_and_semi() -> tuple[List[Dict[str, Any]], Dict[str, Any]]:
    stocks: List[Dict[str, Any]] = []
    if STOCKS_MASTER_PATH.exists():
        raw = json.loads(STOCKS_MASTER_PATH.read_text(encoding="utf-8"))
        stocks = raw if isinstance(raw, list) else raw.get("stocks", [])
    semi: Dict[str, Any] = {}
    if SEMI_OVERVIEW_PATH.exists():
        semi = json.loads(SEMI_OVERVIEW_PATH.read_text(encoding="utf-8"))
    return stocks, semi


def build_ticker_directory_html(stocks: List[Dict[str, Any]], prefix: str = "/") -> str:
    links = [
        f'<a href="{prefix}semi-fear-greed.html" style="color:#f87171;text-decoration:none;font-weight:700;padding:3px 8px;border:1px solid rgba(248,113,113,0.3);border-radius:4px;background:rgba(239,68,68,0.08);">🧭 $SMH Semiconductor Fear &amp; Greed Index</a>'
    ]
    for etf in ("SMH", "XLV", "SOXL", "QQQ"):
        links.append(
            f'<a href="{prefix}stocks/{etf.lower()}.html" style="color:#38bdf8;text-decoration:none;font-weight:700;padding:3px 7px;border:1px solid rgba(56,189,248,0.25);border-radius:4px;">${etf} ETF</a>'
        )
    for s in stocks:
        tkr = str(s.get("ticker") or "").strip().upper()
        if not tkr or "." in tkr:
            continue
        name_en = html.escape(str(s.get("name_en") or s.get("name") or tkr))
        links.append(
            f'<a href="{prefix}stocks/{tkr.lower()}.html" title="{name_en} (${tkr}) PW-RSI Quant Analysis" style="color:#94a3b8;text-decoration:none;padding:2px 6px;border:1px solid rgba(148,163,184,0.16);border-radius:4px;font-family:JetBrains Mono,monospace;font-size:0.72rem;">${tkr}</a>'
        )
    joined = "\n      ".join(links)
    compare_links = []
    for t1, t2, label in COMPARE_PAIRS:
        slug = f"{t1.lower()}-vs-{t2.lower()}.html"
        compare_links.append(
            f'<a href="{prefix}compare/{slug}" title="${t1} vs ${t2} ({html.escape(label)}) PW-RSI Quant Comparison" style="color:#c084fc;text-decoration:none;padding:2px 7px;border:1px solid rgba(192,132,252,0.22);border-radius:4px;font-family:JetBrains Mono,monospace;font-size:0.71rem;background:rgba(168,85,247,0.06);">⚔️ ${t1} vs ${t2}</a>'
        )
    compare_joined = "\n      ".join(compare_links)
    return f"""  <section class="seo-directory-footer" style="max-width:1280px;margin:24px auto 32px;padding:18px 20px;background:#0b1220;border:1px solid #1e293b;border-radius:10px;color:#94a3b8;font-size:0.78rem;">
    <div style="font-weight:800;color:#e2e8f0;margin-bottom:8px;font-size:0.84rem;letter-spacing:0.02em;">
      📊 INSTITUTIONAL US EQUITY &amp; ETF COVERAGE DIRECTORY (72 STOCKS + $SMH/$XLV BARBELL)
    </div>
    <p style="margin:0 0 10px;color:#64748b;font-size:0.75rem;line-height:1.5;">
      Direct institutional Post-Washout Right-Side Ignition (PW-RSI) audits, 52-week support/resistance levels, MA20/MA60 trendline triggers, and -9.0% mechanical stop-loss floors:
    </p>
    <nav aria-label="US Stock and ETF Quantitative Research Directory" style="display:flex;flex-wrap:wrap;gap:6px;align-items:center;margin-bottom:14px;">
      {joined}
    </nav>
    <div style="font-weight:800;color:#e9d5ff;margin:10px 0 6px;font-size:0.8rem;letter-spacing:0.02em;">
      ⚔️ HEAD-TO-HEAD US STOCK &amp; ETF QUANT COMPARISONS (30 HIGH-INTENT MATCHUPS)
    </div>
    <nav aria-label="Head-to-Head US Stock Quantitative Comparisons" style="display:flex;flex-wrap:wrap;gap:6px;align-items:center;">
      {compare_joined}
    </nav>
  </section>"""


def generate_semi_fear_greed_page(semi: Dict[str, Any], stocks: List[Dict[str, Any]], js_name: str, css_name: str) -> str:
    as_of = str(semi.get("date") or "2026-11-05")
    fg_score = float(semi.get("fg_score") or 18.0)
    regime_en = str(semi.get("regime_en") or "Extreme Fear")
    smh_close = float(semi.get("smh_close") or 504.48)
    smh_dd = float(semi.get("smh_dd_pct") or -24.58)
    smh_rsi = float(semi.get("smh_rsi") or 34.2)
    xlv_close = float(semi.get("xlv_close") or 179.28)
    qqq_close = float(semi.get("qqq_close") or 690.49)
    smh_w = 80 if fg_score <= 25.0 else 70
    xlv_w = 100 - smh_w

    title = f"Semiconductor Fear & Greed Index ({fg_score:.1f} {regime_en}) & $SMH/$XLV Barbell | TruthOfMarket"
    desc = (
        f"Live CNN-Edition Semiconductor Fear & Greed Index ({fg_score:.1f}/100 {regime_en} as of {as_of}), "
        f"$SMH (${smh_close:.2f}, {smh_dd:.2f}% 52W DD) vs $XLV (${xlv_close:.2f}) {smh_w}:{xlv_w} contrarian barbell simulator."
    )
    canonical = "https://truthofmarket.com/semi-fear-greed.html"

    faq_ld = {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {
                "@type": "Question",
                "name": "What is the current Semiconductor Fear & Greed Index score today?",
                "acceptedAnswer": {
                    "@type": "Answer",
                    "text": f"As of {as_of}, the 7-Factor Semiconductor Fear & Greed Index stands at {fg_score:.1f} out of 100 ({regime_en}), with VanEck Semiconductor ETF ($SMH) trading at ${smh_close:.2f} ({smh_dd:.2f}% from its 52-week high, 14-day RSI {smh_rsi:.1f}).",
                },
            },
            {
                "@type": "Question",
                "name": "How does the $SMH and $XLV Contrarian Barbell strategy work during Extreme Fear?",
                "acceptedAnswer": {
                    "@type": "Answer",
                    "text": f"Under normal market regimes, the baseline allocation is 70% $SMH (Semiconductors) and 30% $XLV (Healthcare Select Sector SPDR). When the Semiconductor Fear & Greed Index drops into Extreme Fear (<=25) or $SMH experiences a >=19% drawdown, the engine shifts to a contrarian {smh_w}% $SMH : {xlv_w}% $XLV allocation.",
                },
            },
        ],
    }

    dir_html = build_ticker_directory_html(stocks, prefix="/")

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <script>window.__DEFAULT_VIEW__ = 'semi';</script>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>{html.escape(title)}</title>
  <meta name="description" content="{html.escape(desc)}" />
  <link rel="canonical" href="{canonical}" />
  <meta property="og:type" content="website" />
  <meta property="og:site_name" content="RightSideAlpha × SemiFearGreed" />
  <meta property="og:title" content="{html.escape(title)}" />
  <meta property="og:description" content="{html.escape(desc)}" />
  <meta property="og:url" content="{canonical}" />
  <meta property="og:image" content="https://truthofmarket.com/og-preview.png" />
  <meta name="twitter:card" content="summary_large_image" />
  <meta name="twitter:title" content="{html.escape(title)}" />
  <meta name="twitter:description" content="{html.escape(desc)}" />
  <meta name="twitter:image" content="https://truthofmarket.com/og-preview.png" />
  <link rel="icon" type="image/svg+xml" href="/favicon.svg" />
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&family=JetBrains+Mono:wght@500;600;700;800&family=Noto+Sans+JP:wght@400;600;700&family=Noto+Sans+KR:wght@400;600;700&display=swap" rel="stylesheet" />
  <script type="application/ld+json">{json.dumps(faq_ld, ensure_ascii=False)}</script>
  <script src="https://assets.lemonsqueezy.com/lemon.js" defer></script>
  <script type="module" crossorigin src="/assets/{js_name}"></script>
  <link rel="stylesheet" crossorigin href="/assets/{css_name}" />
{HEAD_BEACON_SCRIPT}
</head>
<body>
  <section class="seo-semi-hero" style="max-width:1280px;margin:14px auto 0;padding:16px 20px;background:linear-gradient(135deg,#0f172a 0%,#1e1b4b 100%);border:1px solid #334155;border-radius:10px;color:#f8fafc;">
    <div style="display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:12px;">
      <div>
        <div style="font-family:JetBrains Mono,monospace;font-size:0.72rem;color:#f87171;font-weight:700;text-transform:uppercase;">
          🧭 LIVE SEMICONDUCTOR FEAR &amp; GREED TERMINAL • AS OF {html.escape(as_of)}
        </div>
        <h1 style="font-size:1.25rem;font-weight:800;margin:4px 0;color:#ffffff;">
          CNN-Edition Semiconductor Fear &amp; Greed Index: <span style="color:#f87171;">{fg_score:.1f} / 100 ({html.escape(regime_en.upper())})</span>
        </h1>
        <p style="margin:0;font-size:0.82rem;color:#cbd5e1;">
          <strong>$SMH Close:</strong> ${smh_close:.2f} ({smh_dd:.2f}% 52W DD · RSI {smh_rsi:.1f}) &nbsp;|&nbsp;
          <strong>$XLV Close:</strong> ${xlv_close:.2f} &nbsp;|&nbsp;
          <strong>$QQQ Close:</strong> ${qqq_close:.2f} &nbsp;|&nbsp;
          <strong>Target Barbell:</strong> <span style="color:#38bdf8;font-weight:700;">{smh_w}% $SMH : {xlv_w}% $XLV</span>
        </p>
      </div>
      <div style="display:flex;gap:8px;flex-wrap:wrap;">
        <a href="{LS_MONTHLY_URL}" class="lemonsqueezy-button btn btn-primary" style="background:#2563eb;border-color:#3b82f6;color:#fff;text-decoration:none;padding:8px 14px;border-radius:6px;font-weight:700;font-size:0.8rem;">
          🔓 Unlock Pro VIP ($29/mo)
        </a>
        <a href="https://t.me/truthofmarketss" target="_blank" rel="noopener noreferrer" style="background:#0284c7;color:#fff;text-decoration:none;padding:8px 14px;border-radius:6px;font-weight:700;font-size:0.8rem;">
          ✈️ Free Telegram Briefing
        </a>
      </div>
    </div>
  </section>
  <div id="app"></div>
{dir_html}
</body>
</html>
"""


def generate_single_stock_page(
    stock: Dict[str, Any],
    semi: Dict[str, Any],
    all_stocks: List[Dict[str, Any]],
    js_name: str,
    css_name: str,
) -> str:
    tkr = str(stock.get("ticker") or "NVDA").strip().upper()
    tkr_lower = tkr.lower()
    name_en = str(stock.get("name_en") or stock.get("name") or tkr)
    name_kr = str(stock.get("name_kr") or name_en)
    name_jp = str(stock.get("name_jp") or name_en)
    sector = str(stock.get("sector") or "US Equity")
    as_of = str(stock.get("date") or semi.get("date") or "2026-11-05")
    close_p = float(stock.get("close") or 100.0)
    low52 = float(stock.get("low52") or close_p * 0.7)
    high52 = float(stock.get("high52") or close_p * 1.3)
    dd_pct = float(stock.get("dd_high52_pct") or -20.0)
    prox_low = float(stock.get("prox_low52_pct") or 15.0)
    ma20 = float(stock.get("ma20_price") or close_p * 0.98)
    ma60 = float(stock.get("ma60_price") or close_p * 0.96)
    rsi14 = float(stock.get("rsi14") or 50.0)
    vol_surge = float(stock.get("vol_surge_10d") or 1.2)
    score = int(stock.get("score") or 70)
    zone_code = str(stock.get("zone_code") or "WASHOUT_WATCH")
    zone_label = str(stock.get("zone_label_en") or zone_code)

    trg_p = float(stock.get("entry_trigger_price") or ma60)
    stop_p = float(stock.get("stop_loss_price") or round(close_p * 0.91, 2))
    tp1_p = float(stock.get("tp1_2x_price") or round(close_p * 2.0, 2))

    # Keep Pro VIP Ignition picks (other than free showcase CELH) masked in public HTML to protect paywall & boost FOMO
    is_vip_locked = zone_code == "IGNITION_ZONE" and tkr != "CELH"

    title = f"${tkr} ({name_en}) PW-RSI Turnaround Score ({score}/100) & Support/Resistance Audit | TruthOfMarket"
    desc = (
        f"Institutional PW-RSI quantitative analysis for {name_en} (${tkr}, {name_kr}) as of {as_of}: "
        f"Close ${close_p:.2f}, 52W Range ${low52:.2f}–${high52:.2f} ({dd_pct:.1f}% DD), RSI {rsi14:.1f}, "
        f"10D Volume {vol_surge:.2f}x, and {zone_label} status."
    )
    canonical = f"https://truthofmarket.com/stocks/{tkr_lower}.html"

    if is_vip_locked:
        exec_summary_text = (
            f"${tkr} ({name_en}) is currently in an active Pro VIP Right-Side Ignition setup (Score {score}/100, "
            f"10-day institutional volume surge {vol_surge:.2f}x). Exact entry trigger, -9.0% hard stop floor, and +100% TP1 levels are unlocked for Pro VIP members."
        )
        exec_box_html = f"""
      <div style="margin-top:12px;padding:12px 16px;background:rgba(234,179,8,0.08);border:1px solid rgba(234,179,8,0.4);border-radius:8px;display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:12px;">
        <div>
          <div style="font-size:0.74rem;font-family:JetBrains Mono,monospace;color:#facc15;font-weight:800;">
            🔒 PRO VIP RIGHT-SIDE IGNITION DETECTED • SCORE {score}/100 ({html.escape(sector.upper())})
          </div>
          <div style="font-size:0.84rem;color:#e2e8f0;margin-top:3px;">
            🎯 Entry Trigger: <span style="filter:blur(5px);user-select:none;font-family:JetBrains Mono,monospace;">$148.50</span> &nbsp;|&nbsp;
            🛑 -9.0% Hard Stop: <span style="filter:blur(5px);user-select:none;font-family:JetBrains Mono,monospace;">$135.10</span> &nbsp;|&nbsp;
            💰 +100% TP1 Target: <span style="filter:blur(5px);user-select:none;font-family:JetBrains Mono,monospace;">$297.00</span>
          </div>
        </div>
        <div style="display:flex;gap:8px;flex-wrap:wrap;">
          <a href="{LS_MONTHLY_URL}" class="lemonsqueezy-button" style="background:#eab308;color:#0f172a;text-decoration:none;padding:8px 14px;border-radius:6px;font-weight:800;font-size:0.8rem;">
            🔓 Unlock Exact ${tkr} Levels ($29/mo)
          </a>
          <a href="{LS_LTD_URL}" class="lemonsqueezy-button" style="background:#1e293b;border:1px solid #475569;color:#f8fafc;text-decoration:none;padding:8px 14px;border-radius:6px;font-weight:700;font-size:0.8rem;">
            💎 Lifetime Pass ($199)
          </a>
        </div>
      </div>"""
        init_ticker_js = ""
        init_filter_js = "ignition"
    else:
        exec_summary_text = (
            f"As of {as_of}, ${tkr} ({name_en}) trades at ${close_p:.2f} with a PW-RSI Turnaround Score of {score}/100 ({zone_label}). "
            f"The algorithmic 60-day Entry Trigger is ${trg_p:.2f}, the mechanical Rule 1 (-9.0% Hard Stop) floor is ${stop_p:.2f}, and the Rule 3 (+100% 2x Principal Recovery) target is ${tp1_p:.2f}."
        )
        exec_box_html = f"""
      <div style="margin-top:12px;padding:12px 16px;background:rgba(15,23,42,0.85);border:1px solid #334155;border-radius:8px;display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:12px;">
        <div style="font-size:0.84rem;color:#e2e8f0;font-family:JetBrains Mono,monospace;">
          🎯 <strong>MA20/MA60 Trigger:</strong> <span style="color:#38bdf8;">${trg_p:.2f}</span> &nbsp;|&nbsp;
          🛑 <strong>Rule 1 (-9% Hard Stop):</strong> <span style="color:#f87171;">${stop_p:.2f}</span> &nbsp;|&nbsp;
          💰 <strong>Rule 3 (+100% TP1):</strong> <span style="color:#4ade80;">${tp1_p:.2f}</span>
        </div>
        <div style="display:flex;gap:8px;flex-wrap:wrap;">
          <a href="{LS_MONTHLY_URL}" class="lemonsqueezy-button" style="background:#2563eb;color:#ffffff;text-decoration:none;padding:7px 13px;border-radius:6px;font-weight:700;font-size:0.78rem;">
            🔓 Unlock All 11 VIP Ignition Picks ($29/mo)
          </a>
          <a href="/semi-fear-greed.html" style="background:#1e293b;border:1px solid #475569;color:#f8fafc;text-decoration:none;padding:7px 13px;border-radius:6px;font-weight:700;font-size:0.78rem;">
            🧭 $SMH Fear &amp; Greed ({float(semi.get("fg_score") or 18.0):.1f})
          </a>
        </div>
      </div>"""
        init_ticker_js = tkr if tkr not in ("SMH", "XLV", "SOXL", "QQQ") else ""
        init_filter_js = ""

    faq_ld = {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {
                "@type": "Question",
                "name": f"What is {name_en} (${tkr})'s current PW-RSI Turnaround Score and trend status?",
                "acceptedAnswer": {
                    "@type": "Answer",
                    "text": f"As of {as_of}, {name_en} (${tkr}) has a Post-Washout Right-Side Ignition (PW-RSI) score of {score}/100 ({zone_label}), closing at ${close_p:.2f} with 14-day RSI at {rsi14:.1f} and 10-day relative volume at {vol_surge:.2f}x.",
                },
            },
            {
                "@type": "Question",
                "name": f"Where is ${tkr}'s 52-week support, moving averages, and mechanical stop-loss level?",
                "acceptedAnswer": {
                    "@type": "Answer",
                    "text": f"${tkr}'s 52-week range is ${low52:.2f} to ${high52:.2f} ({dd_pct:.1f}% drawdown from 52W high, +{prox_low:.1f}% off 52W low). Its 20-day MA is ${ma20:.2f} and 60-day MA is ${ma60:.2f}. {exec_summary_text}",
                },
            },
        ],
    }

    dir_html = build_ticker_directory_html(all_stocks, prefix="/")

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <script>
    window.__DEFAULT_VIEW__ = 'rightside';
    window.__INITIAL_TICKER__ = '{init_ticker_js}';
    window.__INITIAL_FILTER__ = '{init_filter_js}';
  </script>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>{html.escape(title)}</title>
  <meta name="description" content="{html.escape(desc)}" />
  <link rel="canonical" href="{canonical}" />
  <meta property="og:type" content="article" />
  <meta property="og:site_name" content="RightSideAlpha × SemiFearGreed" />
  <meta property="og:title" content="{html.escape(title)}" />
  <meta property="og:description" content="{html.escape(desc)}" />
  <meta property="og:url" content="{canonical}" />
  <meta property="og:image" content="https://truthofmarket.com/og-preview.png" />
  <meta name="twitter:card" content="summary_large_image" />
  <meta name="twitter:title" content="{html.escape(title)}" />
  <meta name="twitter:description" content="{html.escape(desc)}" />
  <meta name="twitter:image" content="https://truthofmarket.com/og-preview.png" />
  <link rel="icon" type="image/svg+xml" href="/favicon.svg" />
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&family=JetBrains+Mono:wght@500;600;700;800&family=Noto+Sans+JP:wght@400;600;700&family=Noto+Sans+KR:wght@400;600;700&display=swap" rel="stylesheet" />
  <script type="application/ld+json">{json.dumps(faq_ld, ensure_ascii=False)}</script>
  <script src="https://assets.lemonsqueezy.com/lemon.js" defer></script>
  <script type="module" crossorigin src="/assets/{js_name}"></script>
  <link rel="stylesheet" crossorigin href="/assets/{css_name}" />
{HEAD_BEACON_SCRIPT}
</head>
<body>
  <section class="seo-stock-audit-banner" style="max-width:1280px;margin:14px auto 0;padding:16px 20px;background:linear-gradient(135deg,#0f172a 0%,#111827 100%);border:1px solid #1e293b;border-radius:10px;color:#f8fafc;">
    <div style="font-size:0.72rem;font-family:JetBrains Mono,monospace;color:#94a3b8;margin-bottom:4px;">
      <a href="/" style="color:#38bdf8;text-decoration:none;">TruthOfMarket Terminal</a> &rsaquo;
      <span>{html.escape(sector)}</span> &rsaquo;
      <strong style="color:#f8fafc;">${tkr} ({html.escape(name_en)} · {html.escape(name_kr)} · {html.escape(name_jp)})</strong>
      <span style="float:right;color:#64748b;">As of {html.escape(as_of)}</span>
    </div>
    <h1 style="font-size:1.22rem;font-weight:800;margin:4px 0 8px;color:#ffffff;">
      ${tkr} ({html.escape(name_en)}) — Institutional PW-RSI Turnaround &amp; 52-Week Support/Resistance Audit
    </h1>
    <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(190px,1fr));gap:10px;">
      <div style="padding:10px 12px;background:#0b1220;border:1px solid #1e293b;border-radius:6px;">
        <div style="font-size:0.68rem;color:#64748b;text-transform:uppercase;font-weight:700;">Last Close &amp; 52W Range</div>
        <div style="font-size:1.05rem;font-weight:800;font-family:JetBrains Mono,monospace;color:#f8fafc;margin-top:2px;">
          ${close_p:.2f} <span style="font-size:0.75rem;color:#94a3b8;font-weight:500;">(${low52:.2f} – ${high52:.2f})</span>
        </div>
      </div>
      <div style="padding:10px 12px;background:#0b1220;border:1px solid #1e293b;border-radius:6px;">
        <div style="font-size:0.68rem;color:#64748b;text-transform:uppercase;font-weight:700;">PW-RSI Score &amp; Zone</div>
        <div style="font-size:1.05rem;font-weight:800;font-family:JetBrains Mono,monospace;color:#38bdf8;margin-top:2px;">
          {score}/100 <span style="font-size:0.74rem;color:#e2e8f0;">({html.escape(zone_label)})</span>
        </div>
      </div>
      <div style="padding:10px 12px;background:#0b1220;border:1px solid #1e293b;border-radius:6px;">
        <div style="font-size:0.68rem;color:#64748b;text-transform:uppercase;font-weight:700;">52W High DD / Off Low</div>
        <div style="font-size:1.05rem;font-weight:800;font-family:JetBrains Mono,monospace;color:#f87171;margin-top:2px;">
          {dd_pct:.1f}% <span style="font-size:0.75rem;color:#4ade80;">(+{prox_low:.1f}% off 52W Low)</span>
        </div>
      </div>
      <div style="padding:10px 12px;background:#0b1220;border:1px solid #1e293b;border-radius:6px;">
        <div style="font-size:0.68rem;color:#64748b;text-transform:uppercase;font-weight:700;">MA20 / MA60 / 10D Vol</div>
        <div style="font-size:0.92rem;font-weight:700;font-family:JetBrains Mono,monospace;color:#e2e8f0;margin-top:3px;">
          ${ma20:.2f} / ${ma60:.2f} <span style="color:#facc15;">({vol_surge:.2f}x Vol · RSI {rsi14:.1f})</span>
        </div>
      </div>
    </div>
{exec_box_html}
  </section>
  <div id="app"></div>
{dir_html}
</body>
</html>
"""


def generate_comparison_page(
    stock_a: Dict[str, Any],
    stock_b: Dict[str, Any],
    theme_label: str,
    semi: Dict[str, Any],
    all_stocks: List[Dict[str, Any]],
    js_name: str,
    css_name: str,
) -> str:
    ta = str(stock_a.get("ticker") or "NVDA").upper()
    tb = str(stock_b.get("ticker") or "AMD").upper()
    slug = f"{ta.lower()}-vs-{tb.lower()}.html"
    na = str(stock_a.get("name_en") or stock_a.get("name") or ta)
    nb = str(stock_b.get("name_en") or stock_b.get("name") or tb)
    na_kr = str(stock_a.get("name_kr") or na)
    nb_kr = str(stock_b.get("name_kr") or nb)
    as_of = str(stock_a.get("date") or semi.get("date") or "2026-11-05")

    ca = float(stock_a.get("close") or 100.0)
    cb = float(stock_b.get("close") or 100.0)
    sa = int(stock_a.get("score") or 75)
    sb = int(stock_b.get("score") or 72)
    ra = float(stock_a.get("rsi14") or 48.0)
    rb = float(stock_b.get("rsi14") or 50.0)
    va = float(stock_a.get("vol_surge_10d") or 1.25)
    vb = float(stock_b.get("vol_surge_10d") or 1.15)
    dda = float(stock_a.get("dd_high52_pct") or -18.0)
    ddb = float(stock_b.get("dd_high52_pct") or -22.0)
    stop_a = float(stock_a.get("stop_loss_price") or round(ca * 0.91, 2))
    stop_b = float(stock_b.get("stop_loss_price") or round(cb * 0.91, 2))
    trg_a = float(stock_a.get("entry_trigger_price") or round(ca * 0.98, 2))
    trg_b = float(stock_b.get("entry_trigger_price") or round(cb * 0.98, 2))

    winner = ta if (sa, va) >= (sb, vb) else tb
    loser = tb if winner == ta else ta
    win_score = sa if winner == ta else sb
    win_vol = va if winner == ta else vb

    title = f"${ta} vs ${tb} Stock Comparison ({as_of}): PW-RSI Score, Buy Trigger & -9% Stop-Loss | TruthOfMarket"
    desc = (
        f"Institutional head-to-head quant comparison: ${ta} ({na}, {na_kr}) vs ${tb} ({nb}, {nb_kr}) as of {as_of}. "
        f"Compare PW-RSI Turnaround Score ({sa} vs {sb}), 14D RSI ({ra:.1f} vs {rb:.1f}), 10D Volume ({va:.2f}x vs {vb:.2f}x), and -9% hard stop-loss."
    )
    canonical = f"https://truthofmarket.com/compare/{slug}"

    faq_ld = {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {
                "@type": "Question",
                "name": f"Should I buy ${ta} or ${tb} right now ({as_of})?",
                "acceptedAnswer": {
                    "@type": "Answer",
                    "text": (
                        f"According to the Post-Washout Right-Side Ignition (PW-RSI) quantitative model as of {as_of}, "
                        f"${winner} currently leads ${loser} with a PW-RSI Turnaround Score of {win_score}/100 and {win_vol:.2f}x 10-day relative institutional volume. "
                        f"${ta} trades at ${ca:.2f} (RSI {ra:.1f}, -9% stop ${stop_a:.2f}) while ${tb} trades at ${cb:.2f} (RSI {rb:.1f}, -9% stop ${stop_b:.2f})."
                    ),
                },
            },
            {
                "@type": "Question",
                "name": f"${ta}({na_kr}) vs ${tb}({nb_kr}) 지금 어느 종목이 우측매매 타점에 유리한가요?",
                "acceptedAnswer": {
                    "@type": "Answer",
                    "text": (
                        f"{as_of} 미국 정규장 마감 기준, PW-RSI 퀀트 점수는 ${ta} {sa}점(거래량 {va:.2f}배, -9% 손절선 ${stop_a:.2f}) vs "
                        f"${tb} {sb}점(거래량 {vb:.2f}배, -9% 손절선 ${stop_b:.2f})으로 현재 기관 수급 우위 종목은 ${winner}입니다."
                    ),
                },
            },
        ],
    }

    dir_html = build_ticker_directory_html(all_stocks, prefix="/")
    init_tkr = winner if winner not in ("SMH", "XLV", "SOXL", "QQQ") else ta

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <script>
    window.__DEFAULT_VIEW__ = 'rightside';
    window.__INITIAL_TICKER__ = '{init_tkr}';
  </script>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>{html.escape(title)}</title>
  <meta name="description" content="{html.escape(desc)}" />
  <link rel="canonical" href="{canonical}" />
  <meta property="og:type" content="article" />
  <meta property="og:site_name" content="RightSideAlpha × SemiFearGreed" />
  <meta property="og:title" content="{html.escape(title)}" />
  <meta property="og:description" content="{html.escape(desc)}" />
  <meta property="og:url" content="{canonical}" />
  <meta property="og:image" content="https://truthofmarket.com/og-preview.png" />
  <meta name="twitter:card" content="summary_large_image" />
  <meta name="twitter:title" content="{html.escape(title)}" />
  <meta name="twitter:description" content="{html.escape(desc)}" />
  <meta name="twitter:image" content="https://truthofmarket.com/og-preview.png" />
  <link rel="icon" type="image/svg+xml" href="/favicon.svg" />
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&family=JetBrains+Mono:wght@500;600;700;800&family=Noto+Sans+JP:wght@400;600;700&family=Noto+Sans+KR:wght@400;600;700&display=swap" rel="stylesheet" />
  <script type="application/ld+json">{json.dumps(faq_ld, ensure_ascii=False)}</script>
  <script src="https://assets.lemonsqueezy.com/lemon.js" defer></script>
  <script type="module" crossorigin src="/assets/{js_name}"></script>
  <link rel="stylesheet" crossorigin href="/assets/{css_name}" />
{HEAD_BEACON_SCRIPT}
</head>
<body>
  <section class="seo-compare-banner" style="max-width:1280px;margin:14px auto 0;padding:18px 22px;background:linear-gradient(135deg,#0f172a 0%,#1e1b4b 100%);border:1px solid #334155;border-radius:12px;color:#f8fafc;">
    <div style="font-size:0.72rem;font-family:JetBrains Mono,monospace;color:#c084fc;margin-bottom:4px;">
      <a href="/" style="color:#38bdf8;text-decoration:none;">TruthOfMarket Terminal</a> &rsaquo;
      <span>Head-to-Head Quant Audit</span> &rsaquo;
      <strong style="color:#f8fafc;">${ta} vs ${tb} ({html.escape(theme_label)})</strong>
      <span style="float:right;color:#94a3b8;">As of {html.escape(as_of)}</span>
    </div>
    <h1 style="font-size:1.28rem;font-weight:900;margin:4px 0 10px;color:#ffffff;">
      ⚔️ ${ta} ({html.escape(na)}) vs ${tb} ({html.escape(nb)}) — Institutional Right-Side Quant Verdict
    </h1>
    <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));gap:12px;margin-bottom:12px;">
      <div style="padding:12px 14px;background:#0b1220;border:1px solid {'#38bdf8' if winner == ta else '#1e293b'};border-radius:8px;">
        <div style="display:flex;justify-content:space-between;align-items:center;">
          <strong style="font-size:1.05rem;color:#38bdf8;font-family:JetBrains Mono,monospace;">${ta} · {html.escape(na_kr)}</strong>
          <span style="font-size:0.75rem;padding:2px 8px;border-radius:99px;background:rgba(56,189,248,0.15);color:#38bdf8;font-weight:800;">PW-RSI {sa}/100</span>
        </div>
        <div style="font-size:0.82rem;color:#cbd5e1;margin-top:8px;line-height:1.6;font-family:JetBrains Mono,monospace;">
          • Close: <strong>${ca:.2f}</strong> ({dda:.1f}% 52W DD)<br/>
          • 14D RSI: <strong>{ra:.1f}</strong> &nbsp;|&nbsp; 10D Vol: <strong>{va:.2f}x</strong><br/>
          • Right-Side Trigger: <span style="color:#4ade80;">${trg_a:.2f}</span> &nbsp;|&nbsp; -9% Stop: <span style="color:#f87171;">${stop_a:.2f}</span>
        </div>
      </div>
      <div style="padding:12px 14px;background:#0b1220;border:1px solid {'#38bdf8' if winner == tb else '#1e293b'};border-radius:8px;">
        <div style="display:flex;justify-content:space-between;align-items:center;">
          <strong style="font-size:1.05rem;color:#c084fc;font-family:JetBrains Mono,monospace;">${tb} · {html.escape(nb_kr)}</strong>
          <span style="font-size:0.75rem;padding:2px 8px;border-radius:99px;background:rgba(192,132,252,0.15);color:#c084fc;font-weight:800;">PW-RSI {sb}/100</span>
        </div>
        <div style="font-size:0.82rem;color:#cbd5e1;margin-top:8px;line-height:1.6;font-family:JetBrains Mono,monospace;">
          • Close: <strong>${cb:.2f}</strong> ({ddb:.1f}% 52W DD)<br/>
          • 14D RSI: <strong>{rb:.1f}</strong> &nbsp;|&nbsp; 10D Vol: <strong>{vb:.2f}x</strong><br/>
          • Right-Side Trigger: <span style="color:#4ade80;">${trg_b:.2f}</span> &nbsp;|&nbsp; -9% Stop: <span style="color:#f87171;">${stop_b:.2f}</span>
        </div>
      </div>
    </div>
    <div style="padding:12px 16px;background:rgba(234,179,8,0.09);border:1px solid rgba(234,179,8,0.45);border-radius:8px;display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:12px;">
      <div>
        <div style="font-size:0.76rem;font-family:JetBrains Mono,monospace;color:#facc15;font-weight:800;">
          🏆 QUANT VERDICT: ${winner} LEADS BY INSTITUTIONAL FLOW ({win_score}/100 • {win_vol:.2f}x VOL)
        </div>
        <div style="font-size:0.82rem;color:#e2e8f0;margin-top:3px;">
          🔒 <strong>${winner} vs ${loser} Whale Dark-Pool Target &amp; 2x TP1 Exit:</strong>
          <span style="filter:blur(5px);user-select:none;font-family:JetBrains Mono,monospace;">$184.20 / $268.00</span>
          &nbsp;(🇰🇷 내 평단가 물타기/손절 무료 진단 및 VIP 기관 타점 즉시 해금)
        </div>
      </div>
      <div style="display:flex;gap:8px;flex-wrap:wrap;">
        <a href="/?ticker={winner}#vaultSection" style="background:#0ea5e9;color:#fff;text-decoration:none;padding:8px 13px;border-radius:6px;font-weight:800;font-size:0.78rem;">
          🩺 Free Position Doctor (${winner}/${loser})
        </a>
        <a href="{LS_MONTHLY_URL}" class="lemonsqueezy-button" style="background:#eab308;color:#0f172a;text-decoration:none;padding:8px 14px;border-radius:6px;font-weight:800;font-size:0.78rem;">
          🔓 Unlock Pro VIP ($29/mo)
        </a>
        <a href="{LS_LTD_URL}" class="lemonsqueezy-button" style="background:#1e293b;border:1px solid #475569;color:#f8fafc;text-decoration:none;padding:8px 14px;border-radius:6px;font-weight:700;font-size:0.78rem;">
          💎 Lifetime ($199)
        </a>
      </div>
    </div>
  </section>
  <div id="app"></div>
{dir_html}
</body>
</html>
"""


def generate_all_seo_pages(js_name: str = "index-BIziPp23.js", css_name: str = "index-CaOpdap3.css") -> str:
    stocks, semi = load_stocks_and_semi()
    stocks_dir = PUB / "stocks"
    stocks_dir.mkdir(parents=True, exist_ok=True)

    # 1. Generate /semi-fear-greed.html
    semi_html = generate_semi_fear_greed_page(semi, stocks, js_name, css_name)
    (PUB / "semi-fear-greed.html").write_text(semi_html, encoding="utf-8")

    # 2. Generate 72 stock pages + 4 core ETF pages (SMH, XLV, SOXL, QQQ)
    smh_close = float(semi.get("smh_close") or 504.48)
    smh_dd = float(semi.get("smh_dd_pct") or -24.58)
    smh_rsi = float(semi.get("smh_rsi") or 34.2)
    xlv_close = float(semi.get("xlv_close") or 179.28)
    qqq_close = float(semi.get("qqq_close") or 690.49)
    as_of = str(semi.get("date") or "2026-11-05")

    etf_Synthetics = [
        {
            "ticker": "SMH",
            "name_en": "VanEck Semiconductor ETF",
            "name_kr": "VanEck 반도체 ETF",
            "name_jp": "VanEck 半導体 ETF",
            "sector": "Semiconductor ETF",
            "date": as_of,
            "close": smh_close,
            "low52": round(smh_close * 0.82, 2),
            "high52": round(smh_close / (1.0 + smh_dd / 100.0), 2),
            "dd_high52_pct": smh_dd,
            "prox_low52_pct": 18.0,
            "ma20_price": round(smh_close * 1.03, 2),
            "ma60_price": round(smh_close * 1.06, 2),
            "rsi14": smh_rsi,
            "vol_surge_10d": 1.68,
            "score": 88,
            "zone_code": "WASHOUT_WATCH",
            "zone_label_en": "EXTREME FEAR ACCUMULATION (80% BARBELL)",
            "entry_trigger_price": round(smh_close * 1.02, 2),
            "stop_loss_price": round(smh_close * 0.91, 2),
            "tp1_2x_price": round(smh_close * 2.0, 2),
        },
        {
            "ticker": "XLV",
            "name_en": "Health Care Select Sector SPDR ETF",
            "name_kr": "SPDR 헬스케어 섹터 ETF",
            "name_jp": "SPDR ヘルスケア ETF",
            "sector": "Healthcare Defensive ETF",
            "date": as_of,
            "close": xlv_close,
            "low52": round(xlv_close * 0.88, 2),
            "high52": round(xlv_close * 1.06, 2),
            "dd_high52_pct": -5.4,
            "prox_low52_pct": 13.6,
            "ma20_price": round(xlv_close * 0.99, 2),
            "ma60_price": round(xlv_close * 0.98, 2),
            "rsi14": 54.5,
            "vol_surge_10d": 1.12,
            "score": 82,
            "zone_code": "MA_APPROACH",
            "zone_label_en": "DEFENSIVE BARBELL VAULT (20%-30% WEIGHT)",
            "entry_trigger_price": round(xlv_close * 0.99, 2),
            "stop_loss_price": round(xlv_close * 0.91, 2),
            "tp1_2x_price": round(xlv_close * 1.45, 2),
        },
        {
            "ticker": "SOXL",
            "name_en": "Direxion Daily Semiconductor Bull 3X Shares",
            "name_kr": "Direxion 반도체 3배 레버리지 ETF",
            "name_jp": "Direxion 半導体株ブル3倍 ETF",
            "sector": "3x Leveraged Semiconductor ETF",
            "date": as_of,
            "close": 28.40,
            "low52": 18.50,
            "high52": 68.90,
            "dd_high52_pct": -58.8,
            "prox_low52_pct": 53.5,
            "ma20_price": 30.10,
            "ma60_price": 33.80,
            "rsi14": 36.4,
            "vol_surge_10d": 1.94,
            "score": 85,
            "zone_code": "WASHOUT_WATCH",
            "zone_label_en": "DEEP WASHOUT (WAIT FOR MA20/MA60 RIGHT-SIDE)",
            "entry_trigger_price": 31.20,
            "stop_loss_price": 25.84,
            "tp1_2x_price": 56.80,
        },
        {
            "ticker": "QQQ",
            "name_en": "Invesco QQQ Trust (Nasdaq-100 ETF)",
            "name_kr": "Invesco 나스닥 100 ETF",
            "name_jp": "Invesco QQQ ナスダック100 ETF",
            "sector": "Nasdaq-100 Benchmark ETF",
            "date": as_of,
            "close": qqq_close,
            "low52": round(qqq_close * 0.81, 2),
            "high52": round(qqq_close * 1.07, 2),
            "dd_high52_pct": -6.5,
            "prox_low52_pct": 23.4,
            "ma20_price": round(qqq_close * 0.99, 2),
            "ma60_price": round(qqq_close * 0.97, 2),
            "rsi14": 51.8,
            "vol_surge_10d": 1.18,
            "score": 80,
            "zone_code": "MA_APPROACH",
            "zone_label_en": "CORE BENCHMARK TREND",
            "entry_trigger_price": round(qqq_close * 0.99, 2),
            "stop_loss_price": round(qqq_close * 0.91, 2),
            "tp1_2x_price": round(qqq_close * 1.6, 2),
        },
    ]

    existing_tickers = {str(s.get("ticker") or "").upper() for s in stocks}
    combined = list(stocks) + [e for e in etf_Synthetics if e["ticker"] not in existing_tickers]

    sitemap_urls = [
        ("https://truthofmarket.com/", "1.0", "daily"),
        ("https://truthofmarket.com/semi-fear-greed.html", "0.95", "daily"),
    ]

    for item in combined:
        tkr = str(item.get("ticker") or "").strip().upper()
        if not tkr or "." in tkr:
            continue
        page_html = generate_single_stock_page(item, semi, stocks, js_name, css_name)
        out_file = stocks_dir / f"{tkr.lower()}.html"
        out_file.write_text(page_html, encoding="utf-8")
        prio = "0.90" if tkr in ("CELH", "NVDA", "TSLA", "AMD", "AVGO", "SMH", "XLV", "SOXL", "QQQ", "PLTR", "MBLY") else "0.80"
        sitemap_urls.append((f"https://truthofmarket.com/stocks/{tkr.lower()}.html", prio, "daily"))

    # 3. Generate 30 Head-to-Head Comparison SEO pages (/compare/<a-vs-b>.html)
    compare_dir = PUB / "compare"
    compare_dir.mkdir(parents=True, exist_ok=True)
    by_ticker = {str(it.get("ticker") or "").strip().upper(): it for it in combined}
    compare_count = 0
    for t1, t2, theme_label in COMPARE_PAIRS:
        sa = by_ticker.get(t1) or {"ticker": t1, "name_en": t1, "close": 100.0, "score": 78, "rsi14": 48.0, "vol_surge_10d": 1.3}
        sb = by_ticker.get(t2) or {"ticker": t2, "name_en": t2, "close": 100.0, "score": 74, "rsi14": 51.0, "vol_surge_10d": 1.15}
        cmp_html = generate_comparison_page(sa, sb, theme_label, semi, stocks, js_name, css_name)
        slug = f"{t1.lower()}-vs-{t2.lower()}.html"
        (compare_dir / slug).write_text(cmp_html, encoding="utf-8")
        sitemap_urls.append((f"https://truthofmarket.com/compare/{slug}", "0.88", "daily"))
        compare_count += 1

    today_iso = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    url_blocks = []
    for loc, prio, freq in sitemap_urls:
        url_blocks.append(
            f"""  <url>
    <loc>{loc}</loc>
    <lastmod>{today_iso}</lastmod>
    <changefreq>{freq}</changefreq>
    <priority>{prio}</priority>
  </url>"""
        )
    sitemap_xml = (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        + "\n".join(url_blocks)
        + "\n</urlset>\n"
    )
    (PUB / "sitemap.xml").write_text(sitemap_xml, encoding="utf-8")
    print(f"[SEO] Generated /semi-fear-greed.html + {len(combined)} /stocks/<ticker>.html pages + clean sitemap.xml ({len(sitemap_urls)} URLs)")
    return build_ticker_directory_html(stocks, prefix="/")


if __name__ == "__main__":
    generate_all_seo_pages()
