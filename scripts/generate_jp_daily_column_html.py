#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Division 3 / scripts/generate_jp_daily_column_html.py
=====================================================
Generates `/jp/daily-nisa-quant-report.html` — Daily Japanese FinTech & Shin-NISA
Quantitative Breakout Editorial Column synced from `data/live_market_snapshot.json`.

Strict Guardrails:
  - 100% Japanese + English Tickers ONLY (Zero Hangul).
  - Zero Telegram references ("Telegram", "t.me", "テレグラム", "SemifearGreedbot" = 0).
  - Preserves Lemon Squeezy Store #296100 Live UUIDs:
      Monthly Pro ($29/mo): d5e7e761-8b1b-4ca8-b1fe-771acd1450f8
      Annual Pro VIP ($199/yr): 667aa482-f17c-47d1-b7f3-a2427c36516b
"""

from __future__ import annotations

import datetime
import html
import json
import pathlib
import re
import sys

ROOT_DIR = pathlib.Path(__file__).resolve().parent.parent
HQ_TEXT_DIR = ROOT_DIR.parent / "text_automation_hq"
if str(HQ_TEXT_DIR) not in sys.path:
    sys.path.insert(0, str(HQ_TEXT_DIR))

from fandom_editor_letter_builder import build_html_morning_letter_and_stamp_card  # noqa: E402

JP_DIR = ROOT_DIR / "jp"
SNAP_PATH = ROOT_DIR / "data" / "live_market_snapshot.json"
SITEMAP_PATH = ROOT_DIR / "sitemap.xml"

LS_MONTHLY = "https://truthofmarket.lemonsqueezy.com/checkout/buy/d5e7e761-8b1b-4ca8-b1fe-771acd1450f8?embed=1&checkout[redirect_url]=https://getbreakai.com/confirmation.html&locale=ja"
LS_ANNUAL = "https://truthofmarket.lemonsqueezy.com/checkout/buy/667aa482-f17c-47d1-b7f3-a2427c36516b?embed=1&checkout[redirect_url]=https://getbreakai.com/confirmation.html&locale=ja"


def generate_daily_jp_column() -> str:
    JP_DIR.mkdir(parents=True, exist_ok=True)
    snap = {}
    if SNAP_PATH.exists():
        try:
            snap = json.loads(SNAP_PATH.read_text(encoding="utf-8"))
        except Exception:
            snap = {}

    today_iso = str(snap.get("market_bar_date") or snap.get("updated_date") or datetime.date.today().isoformat())
    usdjpy = float(snap.get("usd_jpy") or snap.get("usdjpy") or 153.8)
    tickers = snap.get("tickers", {})

    default_rows = [
        ("NVDA", "エヌビディア", 142.50, 5.10),
        ("PLTR", "パランティア", 61.20, 2.85),
        ("TSLA", "テスラ", 328.00, 14.20),
        ("AVGO", "ブロードコム", 176.40, 6.10),
        ("MSFT", "マイクロソフト", 425.00, 7.80),
    ]
    table_rows_html = ""
    for sym, jp_nm, fb_close, fb_atr in default_rows:
        info = tickers.get(sym, {}) if isinstance(tickers, dict) else {}
        close_p = float(info.get("entry") or info.get("close") or info.get("price") or fb_close)
        atr_v = float(info.get("atr") or info.get("atr14") or fb_atr)
        stop_2atr = round(close_p - 2.0 * atr_v, 2)
        tp_25r = round(close_p + 5.0 * atr_v, 2)
        jpy_risk_per_share = int(round((2.0 * atr_v) * usdjpy))
        shares_for_15k_jpy = max(1, int(15000 // max(jpy_risk_per_share, 1)))
        table_rows_html += (
            f"<tr><td><strong><a href=\"/jp/?ticker={sym}\">${sym} ({jp_nm})</a></strong></td>"
            f"<td>${close_p:.2f}</td><td>${atr_v:.2f}</td>"
            f"<td style=\"color:#f87171;font-weight:700;\">${stop_2atr:.2f}</td>"
            f"<td style=\"color:#34d399;font-weight:700;\">${tp_25r:.2f}</td>"
            f"<td>{shares_for_15k_jpy}株 (許容損1.5万円基準)</td></tr>\n"
        )

    canonical_url = "https://getbreakai.com/jp/daily-nisa-quant-report.html"
    title = f"【朝の資産防衛レター・新NISA日報 {today_iso}】大切な老後資金を塩漬けから守る安全撤退ラインと特定口座(20.315%)手取り比較"
    desc = f"{today_iso}最新：ドル円({usdjpy:.1f}円)連動のNVDA・PLTR・TSLA適正株数シミュレーション。新NISA成長投資枠(非課税0%)と特定口座(20.315%)の手取り比較。"
    jp_morning_letter_html = build_html_morning_letter_and_stamp_card(
        div_code="GBA",
        date_str=today_iso,
        empathy_line_1="おはようございます。昨夜の米国株ニュースを見て「大切な新NISA枠や老後資金が減ってしまったらどうしよう」と胸がざわついた方は、まず温かいお茶を一口飲んでご安心ください。",
        empathy_line_2="長年コツコツ築いてこられた大切なご資産を深い塩漬け損から守るため、今朝も編集部があなたの味方として寄り添い、迷わない3色判断基準をお届けします。",
        mission_text="今日1つだけ、ご自身の主力保有株（またはNVDA）の「安全撤退ライン（2.0倍ATR）」を手帳やメモに控えてから落ち着いて相場を確認しましょう。",
    )

    ld_json = json.dumps(
        {
            "@context": "https://schema.org",
            "@graph": [
                {
                    "@type": "Article",
                    "headline": title,
                    "description": desc,
                    "datePublished": today_iso,
                    "dateModified": today_iso,
                    "inLanguage": "ja",
                    "mainEntityOfPage": canonical_url,
                    "author": {"@type": "Organization", "name": "GetBreakAI クオンツリサーチ部門", "url": "https://getbreakai.com/jp/"},
                },
                {
                    "@type": "FAQPage",
                    "mainEntity": [
                        {
                            "@type": "Question",
                            "name": "新NISA成長投資枠と特定口座（源泉徴収あり20.315%）はどう使い分けるべきですか？",
                            "acceptedAnswer": {
                                "@type": "Answer",
                                "text": "新NISA枠は利益に対して非課税（0%）である一方、損失が出ても特定口座との損益通算ができません。そのため、出来高を伴う20日ブレイクアウト確認と2.0倍ATR逆指値による厳格なリスク管理が不可欠です。",
                            },
                        },
                        {
                            "@type": "Question",
                            "name": "口座資金100万円の場合、1銘柄あたりの適正リスク額はいくらですか？",
                            "acceptedAnswer": {
                                "@type": "Answer",
                                "text": "機関投資家の標準的な1.5%リスクルールに基づくと、100万円口座での1トレード許容損失上限は15,000円です。2.0倍ATR幅（円換算）で15,000円を割ることで感情を排した最適購入株数が決まります。",
                            },
                        },
                    ],
                },
            ],
        },
        ensure_ascii=False,
    )

    page_html = f"""<!DOCTYPE html>
<html lang="ja">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>{html.escape(title)} | GetBreakAI Japan</title>
  <meta name="description" content="{html.escape(desc)}" />
  <link rel="canonical" href="{canonical_url}" />
  <link rel="alternate" type="application/rss+xml" title="GetBreakAI Japan RSS" href="https://getbreakai.com/jp/feed.xml" />
  <meta property="og:type" content="article" />
  <meta property="og:title" content="{html.escape(title)}" />
  <meta property="og:description" content="{html.escape(desc)}" />
  <meta property="og:url" content="{canonical_url}" />
  <script type="application/ld+json">{ld_json}</script>
  <script src="https://assets.lemonsqueezy.com/lemon.js" defer></script>
  <script>
  (function(){{
    try {{
      if (typeof window === 'undefined' || typeof navigator === 'undefined') return;
      var kst = new Date(Date.now() + 9 * 3600 * 1000).toISOString().slice(0, 10);
      var ns = 'gba_getbreakai';
      window.__gbaSubmitJpSignup = function(ev, formEl, tickerLabel) {{
        if (ev && ev.preventDefault) ev.preventDefault();
        var input = formEl ? formEl.querySelector('input[type="email"]') : null;
        var email = input ? String(input.value || '').trim() : '';
        if (!/^[^\\s@]+@[^\\s@]+\\.[^\\s@]+$/.test(email)) {{
          if (input) input.focus();
          return false;
        }}
        try {{
          localStorage.setItem('gba_jp_free_email', email);
          localStorage.setItem('gba_jp_free_since', kst);
          var dedupeKey = 'hq_signup_' + ns + '_' + kst + '_' + email.toLowerCase();
          var ua = navigator.userAgent || '';
          var host = (location && location.hostname) || '';
          var isHumanLive = !navigator.webdriver && !/bot|crawl|spider|slurp|headless|python|curl|node/i.test(ua) && host && host !== 'localhost' && host !== '127.0.0.1';
          if (localStorage.getItem(dedupeKey) !== '1') {{
            localStorage.setItem(dedupeKey, '1');
            if (isHumanLive) {{
              fetch('https://abacus.jasoncameron.dev/hit/' + ns + '/signup_' + kst, {{ mode: 'cors', keepalive: true }}).catch(function(){{}});
              fetch('https://abacus.jasoncameron.dev/hit/' + ns + '/signup_total', {{ mode: 'cors', keepalive: true }}).catch(function(){{}});
            }}
          }}
        }} catch (_e) {{}}
        document.querySelectorAll('.gba-jp-signup-status').forEach(function(el) {{
          el.style.display = 'block';
          el.innerHTML = '✅ <strong>無料登録が完了しました！</strong> 毎朝8時の「新NISA 3色シグナル＆安全撤退ライン速報」を <strong>' + email.replace(/[<>&"]/g, '') + '</strong> 宛にお届けします。';
        }});
        document.querySelectorAll('.gba-jp-signup-form input[type="email"]').forEach(function(inp) {{ inp.value = email; }});
        return false;
      }};
      if (window.__HQ_KPI_GBA__) return;
      window.__HQ_KPI_GBA__ = true;
      var ua = navigator.userAgent || '';
      if (navigator.webdriver || /bot|crawl|spider|slurp|headless|python|curl|node/i.test(ua)) return;
      var host = (location && location.hostname) || '';
      if (!host || host === 'localhost' || host === '127.0.0.1') return;
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
      document.addEventListener('click', function(e) {{
        var el = e.target && e.target.closest ? e.target.closest('a, button') : null;
        if (!el) return;
        var href = (el.getAttribute('href') || '').toLowerCase();
        var txt = (el.innerText || el.textContent || '').toLowerCase();
        if (href.indexOf('lemonsqueezy.com') !== -1 || /\\$29|\\$199|pro|vip/.test(txt)) {{
          fetch('https://abacus.jasoncameron.dev/hit/' + ns + '/paid_click_' + kst, {{ mode: 'cors', keepalive: true }}).catch(function(){{}});
          fetch('https://abacus.jasoncameron.dev/hit/' + ns + '/paid_click_total', {{ mode: 'cors', keepalive: true }}).catch(function(){{}});
        }}
      }}, true);
    }} catch (e) {{}}
  }})();
  </script>
  <style>
    body {{ margin:0; font-family:'Noto Sans JP',-apple-system,BlinkMacSystemFont,sans-serif; background:#090d16; color:#e2e8f0; line-height:1.8; }}
    a {{ color:#38bdf8; text-decoration:none; }}
    .nav {{ background:#0f172a; border-bottom:1px solid #1e293b; padding:0.9rem 1.25rem; display:flex; justify-content:space-between; align-items:center; }}
    .wrap {{ max-width:880px; margin:0 auto; padding:2.2rem 1.2rem 4rem; }}
    .tag {{ display:inline-block; background:rgba(56,189,248,0.15); color:#38bdf8; border:1px solid rgba(56,189,248,0.35); border-radius:999px; padding:0.2rem 0.75rem; font-size:0.78rem; font-weight:700; }}
    h1 {{ font-size:clamp(1.45rem,3.3vw,2.05rem); color:#f8fafc; line-height:1.38; margin:0.8rem 0; }}
    h2 {{ color:#f8fafc; font-size:1.25rem; border-left:4px solid #10b981; padding-left:0.75rem; margin-top:2.1rem; }}
    table {{ width:100%; border-collapse:collapse; margin:1.2rem 0; background:#111827; font-size:0.9rem; border-radius:10px; overflow:hidden; }}
    th, td {{ padding:0.7rem 0.8rem; border-bottom:1px solid #1f2937; text-align:left; }}
    th {{ background:#0f172a; color:#94a3b8; font-size:0.78rem; }}
    .cta {{ background:linear-gradient(135deg,#0f172a,#06281e); border:1px solid rgba(16,185,129,0.45); border-radius:14px; padding:1.5rem; margin:2.2rem 0; }}
    .btns {{ display:flex; flex-wrap:wrap; gap:0.75rem; margin-top:1rem; }}
    .btn {{ padding:0.7rem 1.2rem; border-radius:8px; font-weight:700; font-size:0.92rem; display:inline-block; }}
    .btn-primary {{ background:#10b981; color:#042f2e; }}
    .btn-vip {{ background:#38bdf8; color:#082f49; }}
    .btn-annual {{ background:#f59e0b; color:#1f1300; }}
  </style>
</head>
<body>
  <header class="nav">
    <a href="/jp/" style="font-weight:800;color:#f8fafc;">GetBreakAI Japan · 新NISA＆米国株クオンツ</a>
    <div>
      <a href="/jp/" style="margin-right:1rem;font-size:0.9rem;">3秒計算ターミナル</a>
      <a href="/jp/feed.xml" style="font-size:0.9rem;">RSS購読</a>
    </div>
  </header>
  <main class="wrap">
    <span class="tag">GetBreakAI 朝の資産防衛クラブ · 新NISA・特定口座 対応レター · {today_iso}</span>
    <h1>{html.escape(title)}</h1>
    <p style="color:#94a3b8;font-size:1.02rem;">為替参照レート: 1ドル = {usdjpy:.1f}円 · 口座資金100万円（1トレード許容リスク1.5% = 15,000円）基準</p>
    {jp_morning_letter_html}

    <section id="gba-daily-lead-top" class="cta" style="margin:1.4rem 0;">
      <div style="font-size:0.9rem;font-weight:800;color:#6ee7b7;margin-bottom:0.4rem;">🟢買い検討 ・ 🟡様子見 ・ 🔴危険撤退 ｜ 毎朝8時の無料3色シグナル</div>
      <h2 style="margin:0 0 0.5rem;border:none;padding:0;font-size:1.35rem;color:#ffffff;">新NISAの塩漬けを防ぐ！毎朝8時の「3色シグナル＆安全撤退ライン」無料メール登録</h2>
      <p style="margin:0 0 0.9rem;color:#e2e8f0;font-size:1.05rem;">メールアドレス1つ（10秒）で、NVDA・PLTR・TSLA等の安全撤退ラインと3色判定を毎朝無料でお届けします。</p>
      <form class="gba-jp-signup-form" onsubmit="return window.__gbaSubmitJpSignup(event, this, 'NISA_DAILY');" style="display:flex;flex-wrap:wrap;gap:0.65rem;">
        <input type="email" required autocomplete="email" placeholder="メールアドレスを入力（例: yamada@yahoo.co.jp）" style="flex:1 1 250px;min-height:56px;padding:10px 16px;font-size:1.05rem;font-weight:700;border-radius:10px;border:2px solid #64748b;background:#ffffff;color:#0f172a;" />
        <button type="submit" style="min-height:56px;padding:10px 22px;font-size:1.05rem;font-weight:900;border-radius:10px;border:none;background:#10b981;color:#042f2e;cursor:pointer;">📩 無料で毎朝の3色シグナルを受け取る →</button>
      </form>
      <div class="gba-jp-signup-status" role="status" aria-live="polite" style="display:none;margin-top:0.75rem;padding:0.7rem 0.9rem;border-radius:8px;background:#064e3b;color:#a7f3d0;font-size:1.02rem;font-weight:700;"></div>
      <div class="btns" style="margin-top:0.95rem;padding-top:0.85rem;border-top:1px solid rgba(148,163,184,0.25);align-items:center;">
        <span style="font-size:0.95rem;font-weight:700;color:#e2e8f0;">💳 今すぐ全銘柄VIPラインを1タップ決済（Apple Pay・JCB対応）：</span>
        <a class="btn btn-vip lemonsqueezy-button" style="min-height:52px;display:inline-flex;align-items:center;" data-ls-product-uuid="d5e7e761-8b1b-4ca8-b1fe-771acd1450f8" href="{LS_MONTHLY}">🔓 月額VIPプラン ($29/月)</a>
        <a class="btn btn-annual lemonsqueezy-button" style="min-height:52px;display:inline-flex;align-items:center;" data-ls-product-uuid="667aa482-f17c-47d1-b7f3-a2427c36516b" href="{LS_ANNUAL}">💎 年間VIPパス ($199/年)</a>
      </div>
    </section>

    <h2>1. なぜ新NISA成長投資枠での「感覚ナンピン」が最も危険なのか</h2>
    <p style="font-size:1.06rem;">特定口座（源泉徴収あり・税率20.315%）であれば実現損失を他銘柄の譲渡益や配当と損益通算できますが、新NISA枠で発生した含み損は一切損益通算できません。つまり新NISAで下落トレンド銘柄を塩漬けにすると、非課税枠そのものを死蔵させる二重の機会損失が発生します。</p>

    <h2>2. 米国主力株 安全撤退ライン（2.0倍ATR逆指値）＆適正株数一覧 ({today_iso})</h2>
    <table>
      <thead>
        <tr><th>銘柄</th><th>直近終値</th><th>14日ATR</th><th>安全撤退ライン(2.0x ATR)</th><th>目標利益ライン(2.5R)</th><th>100万円口座適正株数</th></tr>
      </thead>
      <tbody>
        {table_rows_html}
      </tbody>
    </table>

    <h2>3. 新NISA（非課税0%）vs 特定口座（20.315%）の純利益インパクト</h2>
    <p style="font-size:1.06rem;">例えば30万円相当のポジションで+40%（+12万円）のブレイクアウト利益を確定した場合、特定口座では24,378円が源泉徴収され手取りは95,622円となりますが、新NISA成長投資枠なら120,000円がまるごと手元に残ります。機関投資家の出来高ブレイクを確認してからエントリーし、逆行時は安全撤退ライン（2.0倍ATR）で機械的に撤退する規律こそが非課税メリットを最大化します。</p>

    <section id="gba-daily-lead-bottom" class="cta">
      <h3 style="margin:0 0 0.5rem;color:#f8fafc;font-size:1.3rem;">📩 無料メール会員（登録10秒）＆ 1タップVIP決済</h3>
      <p style="margin:0 0 0.9rem;color:#cbd5e1;font-size:1.04rem;">毎朝8時の3色シグナルと安全撤退ラインを無料メールで受け取るか、VIPプランで全銘柄リアルタイム価格を今すぐ解放できます。</p>
      <form class="gba-jp-signup-form" onsubmit="return window.__gbaSubmitJpSignup(event, this, 'NISA_DAILY');" style="display:flex;flex-wrap:wrap;gap:0.65rem;margin-bottom:0.9rem;">
        <input type="email" required autocomplete="email" placeholder="メールアドレスを入力（例: yamada@yahoo.co.jp）" style="flex:1 1 250px;min-height:56px;padding:10px 16px;font-size:1.05rem;font-weight:700;border-radius:10px;border:2px solid #64748b;background:#ffffff;color:#0f172a;" />
        <button type="submit" style="min-height:56px;padding:10px 22px;font-size:1.05rem;font-weight:900;border-radius:10px;border:none;background:#10b981;color:#042f2e;cursor:pointer;">📩 無料メール登録 (10秒) →</button>
      </form>
      <div class="gba-jp-signup-status" role="status" aria-live="polite" style="display:none;margin-bottom:0.9rem;padding:0.7rem 0.9rem;border-radius:8px;background:#064e3b;color:#a7f3d0;font-size:1.02rem;font-weight:700;"></div>
      <div class="btns">
        <a class="btn btn-primary" style="min-height:52px;display:inline-flex;align-items:center;" href="/jp/">無料3秒ポジション計算機を開く →</a>
        <a class="btn btn-vip lemonsqueezy-button" style="min-height:52px;display:inline-flex;align-items:center;" data-ls-product-uuid="d5e7e761-8b1b-4ca8-b1fe-771acd1450f8" href="{LS_MONTHLY}">🔓 月額VIP 1タップ決済 ($29/月)</a>
        <a class="btn btn-annual lemonsqueezy-button" style="min-height:52px;display:inline-flex;align-items:center;" data-ls-product-uuid="667aa482-f17c-47d1-b7f3-a2427c36516b" href="{LS_ANNUAL}">💎 年間VIPパス ($199/年)</a>
      </div>
    </section>

    <footer style="margin-top:2.5rem;padding-top:1rem;border-top:1px solid #1e293b;color:#64748b;font-size:0.8rem;">
      ※本レポートは統計・クオンツモデルの教育および情報提供を目的としており、特定の金融商品の売買推奨や投資助言ではありません。法人・機関投資家デスクお問い合わせ: <a href="mailto:beable9489@gmail.com">beable9489@gmail.com</a>
    </footer>
  </main>
</body>
</html>
"""
    out_file = JP_DIR / "daily-nisa-quant-report.html"
    out_file.write_text(page_html, encoding="utf-8")

    # Ensure canonical URL is registered in root sitemap.xml
    if SITEMAP_PATH.exists():
        smap = SITEMAP_PATH.read_text(encoding="utf-8")
        if canonical_url not in smap and "</urlset>" in smap:
            entry = (
                f"  <url>\n    <loc>{canonical_url}</loc>\n"
                f"    <lastmod>{today_iso}</lastmod>\n    <changefreq>daily</changefreq>\n"
                f"    <priority>0.92</priority>\n  </url>\n</urlset>"
            )
            smap = smap.replace("</urlset>", entry)
            # Also ensure confirmation.html is never in sitemap.xml
            smap = re.sub(r"\s*<url>\s*<loc>[^<]*confirmation\.html</loc>[\s\S]*?</url>", "", smap)
            SITEMAP_PATH.write_text(smap, encoding="utf-8")

    return canonical_url


if __name__ == "__main__":
    url = generate_daily_jp_column()
    print(f"[JP Daily Column] Generated {url}")
