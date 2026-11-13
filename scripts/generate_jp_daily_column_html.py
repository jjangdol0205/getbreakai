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

ROOT_DIR = pathlib.Path(__file__).resolve().parent.parent
JP_DIR = ROOT_DIR / "jp"
SNAP_PATH = ROOT_DIR / "data" / "live_market_snapshot.json"
SITEMAP_PATH = ROOT_DIR / "sitemap.xml"

LS_MONTHLY = "https://truthofmarket.lemonsqueezy.com/checkout/buy/d5e7e761-8b1b-4ca8-b1fe-771acd1450f8?embed=1"
LS_ANNUAL = "https://truthofmarket.lemonsqueezy.com/checkout/buy/667aa482-f17c-47d1-b7f3-a2427c36516b?embed=1"


def generate_daily_jp_column() -> str:
    JP_DIR.mkdir(parents=True, exist_ok=True)
    snap = {}
    if SNAP_PATH.exists():
        try:
            snap = json.loads(SNAP_PATH.read_text(encoding="utf-8"))
        except Exception:
            snap = {}

    today_iso = datetime.date.today().isoformat()
    usdjpy = float(snap.get("usdjpy") or 153.8)
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
        close_p = float(info.get("close") or info.get("price") or fb_close)
        atr_v = float(info.get("atr14") or info.get("atr") or fb_atr)
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
    title = f"【米国株・新NISAクオンツ日報 {today_iso}】2.0倍ATR逆指値と特定口座(20.315%)税引後リターン検証"
    desc = f"{today_iso}最新：ドル円({usdjpy:.1f}円)連動のNVDA・PLTR・TSLA適正株数シミュレーション。新NISA成長投資枠(非課税0%)と特定口座(20.315%)の手取り比較。"

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
    <span class="tag">新NISA・特定口座 対応クオンツ日報 · {today_iso}</span>
    <h1>{html.escape(title)}</h1>
    <p style="color:#94a3b8;font-size:0.9rem;">為替参照レート: 1ドル = {usdjpy:.1f}円 · 口座資金100万円（1トレード許容リスク1.5% = 15,000円）基準</p>

    <h2>1. なぜ新NISA成長投資枠での「感覚ナンピン」が最も危険なのか</h2>
    <p>特定口座（源泉徴収あり・税率20.315%）であれば実現損失を他銘柄の譲渡益や配当と損益通算できますが、新NISA枠で発生した含み損は一切損益通算できません。つまり新NISAで下落トレンド銘柄を塩漬けにすると、非課税枠そのものを死蔵させる二重の機会損失が発生します。</p>

    <h2>2. 米国主力株 2.0倍ATR防衛ライン＆適正株数一覧 ({today_iso})</h2>
    <table>
      <thead>
        <tr><th>銘柄</th><th>直近終値</th><th>14日ATR</th><th>2.0x ATR逆指値</th><th>2.5R利確目安</th><th>100万円口座適正株数</th></tr>
      </thead>
      <tbody>
        {table_rows_html}
      </tbody>
    </table>

    <h2>3. 新NISA（非課税0%）vs 特定口座（20.315%）の純利益インパクト</h2>
    <p>例えば30万円相当のポジションで+40%（+12万円）のブレイクアウト利益を確定した場合、特定口座では24,378円が源泉徴収され手取りは95,622円となりますが、新NISA成長投資枠なら120,000円がまるごと手元に残ります。機関投資家の出来高ブレイクを確認してからエントリーし、逆行時は2.0倍ATRで機械的に撤退する規律こそが非課税メリットを最大化します。</p>

    <section class="cta">
      <h3 style="margin:0 0 0.4rem;color:#f8fafc;">あなたの口座資金（円・ドル）で今すぐ3秒無料診断</h3>
      <p style="margin:0;color:#cbd5e1;font-size:0.95rem;">登録不要で主要銘柄の最適購入株数・2.0倍ATR逆指値・新NISA税引後手取り額をリアルタイム計算できます。</p>
      <div class="btns">
        <a class="btn btn-primary" href="/jp/">無料3秒ポジション計算機を開く →</a>
        <a class="btn btn-vip lemonsqueezy-button" href="{LS_MONTHLY}">Monthly Pro ($29/mo)</a>
        <a class="btn btn-annual lemonsqueezy-button" href="{LS_ANNUAL}">Annual Pro VIP ($199/yr)</a>
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
