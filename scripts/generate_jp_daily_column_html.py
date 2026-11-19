#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Division 3 / scripts/generate_jp_daily_column_html.py
=====================================================
Generates `/jp/daily-nisa-quant-report.html` — Daily Japanese Shin-NISA & Tokutei Hybrid
Public Market Data & Retirement Cashflow Editorial Column synced from `data/live_market_snapshot.json`.
Strictly Zero-Hangul, Zero-Chat-App, MoR/FIEA & Japanese FSA Shin-NISA Hybrid Compliant.
"""

from __future__ import annotations

import datetime
import html
import json
import pathlib
import re
import sys

SCRIPT_DIR = pathlib.Path(__file__).resolve().parent
ROOT_DIR = SCRIPT_DIR.parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from gba_mor_nisa_shared import (  # noqa: E402
    MOR_LABEL_EN_JP,
    WHOP_MONTHLY_CTA_HREF,
    WHOP_ANNUAL_CTA_HREF,
    PRICE_LABEL_MONTHLY_JP,
    PRICE_LABEL_ANNUAL_JP,
    MANDATORY_DISCLAIMER_JP,
    SOFTWARE_POSITIONING_JP,
    FSA_HYBRID_PHRASE_JP,
    build_payment_and_kpi_head_html,
    build_mandatory_disclaimer_html,
    build_pro_retiree_tools_html,
    build_starter_manual_modal_html,
    build_vip_waitlist_modal_html,
    build_legal_footer_html,
)

JP_DIR = ROOT_DIR / "jp"
SNAP_PATH = ROOT_DIR / "data" / "live_market_snapshot.json"
SITEMAP_PATH = ROOT_DIR / "sitemap.xml"


def _build_morning_empathy_card(today_iso: str) -> str:
    return f"""    <div style="background:#ffffff; border:1.5px solid #cbd5e1; border-left:5px solid #059669; border-radius:14px; padding:18px 20px; margin:1.2rem 0; color:#0f172a;">
      <div style="font-size:0.88rem; font-weight:900; color:#065f46; margin-bottom:6px;">🍵 朝のゆとり老後＆資産守りレター · {html.escape(today_iso)}</div>
      <p style="margin:0 0 8px; color:#1e293b; font-size:1.02rem;">おはようございます。昨夜の相場ニュースを見て「大切な新NISA枠や退職金が減ってしまったらどうしよう」と気になった方も、まずは温かいお茶を一口飲んで落ち着いてデータを確認しましょう。</p>
      <p style="margin:0; color:#334155; font-size:0.98rem;"><strong>本日の小さな確認ポイント：</strong>ご自身の保有資産が{FSA_HYBRID_PHRASE_JP}のバランスから大きく偏っていないか、年2〜4回の穏やかな視点で点検しましょう。</p>
    </div>"""


def generate_daily_jp_column() -> str:
    JP_DIR.mkdir(parents=True, exist_ok=True)
    snap = {}
    if SNAP_PATH.exists():
        try:
            snap = json.loads(SNAP_PATH.read_text(encoding="utf-8"))
        except Exception:
            snap = {}

    today_iso = str(snap.get("market_bar_date") or snap.get("updated_date") or datetime.date.today().isoformat())
    usdjpy = float(snap.get("usd_jpy") or snap.get("usdjpy") or 150.0)
    tickers = snap.get("tickers", {})

    default_rows = [
        ("SMH", "米国半導体ETF（新NISA成長投資枠適格・成長柱）", 258.40, 5.80, "/jp/#gba-retirement-architect-jp", "新NISA成長枠（成長コア）"),
        ("XLV", "米国ヘルスケアETF（新NISA成長投資枠適格・防衛柱）", 148.90, 2.40, "/jp/#gba-retirement-architect-jp", "新NISA成長枠（防衛コア）"),
        ("SGOV", "米国0-3ヶ月短期国債ETF（特定口座・安全資産区分）", 100.42, 0.08, "/jp/#gba-retirement-architect-jp", "特定口座（または個人向け国債 変動10年）"),
        ("MSFT", "マイクロソフト（個別研究参考・上限10%以内）", 448.20, 9.40, "/jp/msft-azure-ai-copilot-sec-8k.html", "個別補完（口座10%以内）"),
        ("LLY", "イーライリリー（ヘルスケア研究参考・上限10%以内）", 1354.00, 52.81, "/jp/lly-form4-insider-cluster-buy.html", "個別補完（口座10%以内）"),
    ]
    table_rows_html = ""
    for sym, jp_nm, fb_close, fb_atr, link_href, acct_role in default_rows:
        info = tickers.get(sym, {}) if isinstance(tickers, dict) else {}
        close_p = float(info.get("entry") or info.get("close") or info.get("price") or fb_close)
        atr_v = float(info.get("atr") or info.get("atr14") or fb_atr)
        jpy_price = int(round(close_p * usdjpy))
        table_rows_html += (
            f'<tr><td><strong><a href="{link_href}">${sym} ({jp_nm})</a></strong></td>'
            f"<td>${close_p:.2f} (約¥{jpy_price:,})</td><td>${atr_v:.2f}</td>"
            f'<td style="color:#047857;font-weight:700;">{acct_role}</td></tr>\n'
        )

    canonical_url = "https://getbreakai.com/jp/daily-nisa-quant-report.html"
    title = f"【朝の資産守り＆新NISA公開データ日報 {today_iso}】新NISA成長投資枠（SMH × XLV）＋個人向け国債（変動10年）2本柱配分ガイド"
    desc = f"{today_iso}更新：ドル円({usdjpy:.1f}円)参照の公開市場データと{FSA_HYBRID_PHRASE_JP}に基づく非課税(0%)・安全資産の区分整理。"

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
                    "author": {"@type": "Organization", "name": "GetBreakAI Public Market Data Research", "url": "https://getbreakai.com/jp/"},
                    "publisher": {
                        "@type": "Organization",
                        "name": "GetBreakAI Japan",
                        "url": "https://getbreakai.com/jp/",
                        "sameAs": [
                            "https://www.youtube.com/@GetBreakAI",
                            "https://www.instagram.com/getbreakai/",
                        ],
                    },
                },
                {
                    "@type": "FAQPage",
                    "mainEntity": [
                        {
                            "@type": "Question",
                            "name": "新NISA成長投資枠と個人向け国債・特定口座（源泉徴収あり20.315%）はどう使い分けるべきですか？",
                            "acceptedAnswer": {
                                "@type": "Answer",
                                "text": "日本の金融庁規定により、毎月分配型ETF（SGOV・JEPI等）やレバレッジ型ETF（SOXL等）は新NISA対象外です。新NISA成長投資枠では現物1倍の米国半導体ETF（SMH）と米国ヘルスケアETF（XLV）の2本柱を保有し、生活防衛クッションは日本の個人向け国債（変動10年）または特定口座のSGOVで区分管理する設計が制度に準拠しています。",
                            },
                        },
                        {
                            "@type": "Question",
                            "name": "当日報は投資助言や売買推奨ですか？",
                            "acceptedAnswer": {
                                "@type": "Answer",
                                "text": MANDATORY_DISCLAIMER_JP,
                            },
                        },
                    ],
                },
            ],
        },
        ensure_ascii=False,
    )

    head_scripts = build_payment_and_kpi_head_html()
    disclaimer_box = build_mandatory_disclaimer_html()
    pro_tools_compact = build_pro_retiree_tools_html(compact=True)
    manual_modal = build_starter_manual_modal_html()
    waitlist_modal = build_vip_waitlist_modal_html()
    footer_html = build_legal_footer_html()

    page_html = f"""<!DOCTYPE html>
<html lang="ja" data-jp-theme="light">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>{html.escape(title)} | GetBreakAI 朝刊ノート</title>
  <meta name="description" content="{html.escape(desc)}" />
  <link rel="canonical" href="{canonical_url}" />
  <link rel="alternate" type="application/rss+xml" title="GetBreakAI Japan RSS" href="https://getbreakai.com/jp/feed.xml" />
  <meta property="og:type" content="article" />
  <meta property="og:title" content="{html.escape(title)}" />
  <meta property="og:description" content="{html.escape(desc)}" />
  <meta property="og:url" content="{canonical_url}" />
  <link rel="icon" type="image/svg+xml" href="/favicon.svg" />
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <link href="https://fonts.googleapis.com/css2?family=Noto+Sans+JP:wght@400;500;700;800&family=Noto+Serif+JP:wght@500;700&display=swap" rel="stylesheet" />
  <script type="application/ld+json">{ld_json}</script>
{head_scripts}
  <style>
    body {{ margin:0; font-family:'Noto Sans JP',-apple-system,BlinkMacSystemFont,sans-serif; background:#fcfcfa; color:#1a1a1a; line-height:1.85; font-size:18.5px; font-feature-settings:"palt" 1; }}
    a {{ color:#1d4ed8; text-decoration:underline; text-underline-offset:3px; }}
    .sr-only {{ position:absolute; width:1px; height:1px; overflow:hidden; clip:rect(0,0,0,0); }}
    .essay-topbar {{ border-bottom:1px solid #e6e4dd; background:rgba(252,252,250,0.95); position:sticky; top:0; z-index:40; }}
    .essay-topbar-inner {{ max-width:680px; margin:0 auto; padding:14px 20px; display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:10px; }}
    .essay-pub-brand {{ font-weight:800; color:#1a1a1a; font-size:0.96rem; text-decoration:none; }}
    .essay-top-nav {{ display:flex; gap:12px; align-items:center; font-size:0.85rem; font-weight:700; }}
    .essay-top-nav a, .essay-top-nav button {{ color:#6b6b66; text-decoration:none; background:none; border:none; font:inherit; cursor:pointer; }}
    .reading-column {{ max-width:680px; margin:0 auto; padding:44px 20px 72px; }}
    .essay-kicker {{ font-size:0.78rem; font-weight:800; letter-spacing:0.06em; color:#059669; margin-bottom:10px; }}
    h1 {{ font-family:'Noto Serif JP',Georgia,serif; font-size:clamp(1.55rem,3.6vw,2.1rem); color:#1a1a1a; line-height:1.38; margin:0 0 14px; }}
    .byline-bar {{ display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:12px; padding:14px 0; border-top:1px solid #e6e4dd; border-bottom:1px solid #e6e4dd; margin-bottom:30px; }}
    .byline-author {{ display:flex; align-items:center; gap:10px; }}
    .byline-avatar {{ width:38px; height:38px; border-radius:50%; background:#e9ece6; color:#1f3a2e; font-weight:800; font-size:0.85rem; display:inline-flex; align-items:center; justify-content:center; }}
    .share-copy-btn {{ background:#ffffff; border:1px solid #e6e4dd; border-radius:999px; padding:7px 14px; font-size:0.82rem; font-weight:700; color:#3d3d3a; cursor:pointer; }}
    h2 {{ font-family:'Noto Serif JP',Georgia,serif; color:#1a1a1a; font-size:1.3rem; border-bottom:1px solid #e6e4dd; padding-bottom:6px; margin:2em 0 0.75em; }}
    p {{ margin:0 0 1.45em; }}
    .table-wrap {{ overflow-x:auto; }}
    table {{ width:100%; border-collapse:collapse; margin:1.4rem 0; background:#ffffff; font-size:0.9rem; border:1px solid #e6e4dd; }}
    th, td {{ padding:0.7rem 0.8rem; border-bottom:1px solid #e6e4dd; text-align:left; }}
    th {{ background:#f5f4ef; color:#6b6b66; font-size:0.78rem; }}
    .substack-subscribe-box {{ margin:44px 0 22px; padding:28px 24px; background:#ffffff; border:1px solid #e6e4dd; border-radius:12px; text-align:center; }}
    .substack-sub-title {{ font-family:'Noto Serif JP',Georgia,serif; font-size:1.34rem; font-weight:700; margin-bottom:8px; }}
    .substack-sub-desc {{ font-size:0.92rem; color:#6b6b66; max-width:500px; margin:0 auto 16px; line-height:1.68; }}
    .substack-inline-form {{ display:flex; max-width:460px; margin:0 auto; gap:8px; flex-wrap:wrap; }}
    .substack-inline-form input {{ flex:1 1 220px; min-height:48px; padding:10px 14px; border:1px solid #c9c6bc; border-radius:8px; font-size:0.96rem; }}
    .substack-inline-form button {{ min-height:48px; padding:10px 20px; border:none; border-radius:8px; background:#059669; color:#ffffff; font-weight:800; font-size:0.94rem; cursor:pointer; }}
    .editorial-postscript {{ padding:18px 20px; background:#f5f4ef; border:1px solid #e6e4dd; border-radius:10px; font-size:0.9rem; line-height:1.7; color:#3d3d3a; }}
    .gba-manual-free-badge {{ display:inline-flex; align-items:center; gap:6px; background:#059669; color:#ffffff; font-size:0.86rem; font-weight:900; padding:4px 12px; border-radius:999px; }}
    .gba-manual-modal-backdrop {{ display:none; position:fixed; inset:0; z-index:9999; background:rgba(15,23,42,0.76); backdrop-filter:blur(4px); padding:18px 12px; overflow-y:auto; align-items:flex-start; justify-content:center; }}
    .gba-manual-modal-backdrop.is-open {{ display:flex; }}
    .gba-manual-modal-dialog {{ background:#ffffff; color:#0b1f3a; border:2px solid #059669; border-radius:16px; width:100%; max-width:860px; margin:8px auto 32px; overflow:hidden; }}
    .gba-manual-modal-header {{ background:#ffffff; border-bottom:2px solid #cbd5e1; padding:14px 18px; display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:10px; }}
    .gba-manual-action-btn {{ min-height:44px; padding:8px 14px; border-radius:10px; font-weight:900; cursor:pointer; border:2px solid #cbd5e1; background:#f8fafc; }}
    .gba-manual-nav-pills {{ display:flex; flex-wrap:wrap; gap:8px; padding:12px 18px; background:#f8fafc; border-bottom:1px solid #cbd5e1; }}
    .gba-manual-jump-pill {{ min-height:42px; padding:6px 12px; border-radius:999px; border:1px solid #cbd5e1; background:#ffffff; font-weight:800; cursor:pointer; }}
    .gba-manual-modal-body {{ padding:20px; }}
    .gba-manual-chapter-box {{ background:#f8fafc; border:1px solid #cbd5e1; border-radius:12px; padding:16px; margin-bottom:14px; }}
    .gba-manual-broker-grid {{ display:grid; grid-template-columns:repeat(auto-fit,minmax(250px,1fr)); gap:12px; }}
    .gba-manual-broker-card {{ background:#ffffff; border:1px solid #cbd5e1; border-radius:10px; padding:14px; }}
    .gba-manual-tip-callout {{ margin-top:10px; padding:10px 12px; background:#ecfdf5; border-left:4px solid #059669; border-radius:8px; }}
    .gba-manual-modal-funnel {{ background:#eff6ff; border:2px solid #059669; border-radius:12px; padding:16px; }}
    .gba-manual-open-btn {{ background:#059669; color:#ffffff; border:none; border-radius:10px; padding:12px 18px; font-weight:900; cursor:pointer; }}
    .gba-manual-funnel-links {{ display:flex; flex-wrap:wrap; gap:10px; margin-top:10px; }}
    .gba-manual-pro-link, .gba-manual-vip-link {{ padding:8px 14px; border-radius:999px; border:1.5px solid #1d4ed8; font-weight:800; background:#ffffff; }}
  </style>
</head>
<body>
  <header class="essay-topbar">
    <div class="essay-topbar-inner">
      <a href="/jp/" class="essay-pub-brand">GetBreakAI ・ 朝刊データノート</a>
      <nav class="essay-top-nav">
        <a href="/jp/nisa-quiet-barbell-essay.html">代表エッセイ</a>
        <a href="/jp/#gba-retirement-architect-jp">セクター過去統計エクスプローラー</a>
        <button type="button" onclick="openGbaStarterManualModal()">¥0 基本マニュアル</button>
        <a href="/jp/feed.xml">RSS</a>
      </nav>
    </div>
  </header>
  <main class="reading-column">
    <div class="essay-kicker">公開市場データ朝刊ノート ・ 為替参照 1ドル = {usdjpy:.1f}円</div>
    <h1>{html.escape(title)}</h1>
    <div class="byline-bar">
      <div class="byline-author">
        <span class="byline-avatar" aria-hidden="true">佐藤</span>
        <div>
          <div style="font-size:0.92rem;font-weight:800;">佐藤 健一</div>
          <div style="font-size:0.8rem;color:#6b6b66;">資産設計エッセイ・公開データ研究 ・ {today_iso}</div>
        </div>
      </div>
      <button type="button" class="share-copy-btn" onclick="window.__gbaCopyEssayLink(this)">リンクをコピー</button>
    </div>

    <article>
      <p>おはようございます。昨夜の米国市場や為替ニュースを見て「大切な新NISA枠や老後資金が大きく揺れていないだろうか」と気になった朝も、まずは落ち着いた目で公開終値と資産全体の比率だけを確かめていきましょう。</p>

      <h2>新NISA成長投資枠（SMH × XLV）と安全資産（個人向け国債・SGOV）の金融庁準拠区分</h2>
      <p>日本の金融庁規定により、毎月分配型ETF（SGOV・JEPI・JEPQ・QYLD等）およびレバレッジ型ETF（SOXL・TQQQ等）は新NISAの対象外であり、特定口座（源泉徴収あり・税率20.315%）でのみ保有可能です。そのため老後の資産設計では、<strong>{FSA_HYBRID_PHRASE_JP}</strong>を採用し、新NISA成長投資枠では現物1倍の米国半導体ETF（SMH）と米国ヘルスケアETF（XLV）の2本柱で非課税メリットを活かしながら、生活防衛クッションは日本の個人向け国債（変動10年）または特定口座のSGOVで安全に別枠管理します。</p>

      <h2>公開市場データによる主要ETF・参考銘柄 基準一覧 ({today_iso})</h2>
      <div class="table-wrap">
        <table>
          <thead>
            <tr><th>銘柄・資産区分</th><th>直近終値（円換算目安）</th><th>14日平均変動幅</th><th>口座区分・位置づけ</th></tr>
          </thead>
          <tbody>
            {table_rows_html}
          </tbody>
        </table>
      </div>

      <h2>新NISA（非課税0%）と特定口座（20.315%）の穏やかな使い分け</h2>
      <p>新NISA成長投資枠（年間240万円・つみたて投資枠と合計360万円）では配当金および売却益に対する国内20.315%課税が非課税となる一方、特定口座と損益通算はできません。したがって短期的な売買で年間枠を消費するのではなく、ゆとりある長期比率を維持する設計が有効です。</p>
    </article>

    <section class="substack-subscribe-box" id="gba-substack-subscribe" aria-label="朝刊エッセイ無料メール購読">
      <div class="substack-sub-title">次の朝刊ノートをメールで受け取る</div>
      <p class="substack-sub-desc">パスワード不要・いつでも1クリック配信停止OK。毎朝の公開市場データ要約と資産設計エッセイを無料でお届けします。</p>
      <form class="substack-inline-form" onsubmit="return window.__gbaSubmitSubstackSubscribe(event, this, 'daily-nisa-quant-report.html');" novalidate>
        <label for="dailySubEmailJp" class="sr-only">メールアドレス</label>
        <input id="dailySubEmailJp" type="email" required autocomplete="email" placeholder="メールアドレスを入力..." />
        <button type="submit">無料で購読する</button>
      </form>
      <div class="substack-sub-status" role="status" aria-live="polite" style="display:none;margin-top:12px;font-weight:700;"></div>
    </section>

    <aside class="editorial-postscript">
      <div style="font-size:0.76rem;font-weight:800;color:#6b6b66;margin-bottom:6px;">編集後記 ・ 独立系教育リサーチ出版</div>
      <p style="margin:0 0 8px;">過去25年の統計比較は <a href="/jp/#gba-retirement-architect-jp"><strong>セクター過去統計エクスプローラー（2000–2025年統計比較）</strong></a> にて登録不要・無料でご確認いただけます。「{SOFTWARE_POSITIONING_JP}」の定期購読は <a class="whop-checkout-button" data-gba-paid-plan="monthly" href="{WHOP_MONTHLY_CTA_HREF}">{PRICE_LABEL_MONTHLY_JP}</a> ・ <a class="whop-checkout-button" data-gba-paid-plan="annual" href="{WHOP_ANNUAL_CTA_HREF}">{PRICE_LABEL_ANNUAL_JP}</a>（決済基盤：{MOR_LABEL_EN_JP}）にてご提供しています。</p>
{disclaimer_box}
    </aside>
  </main>

{footer_html}
{manual_modal}
{waitlist_modal}

  <script>
    function jumpFromManualToJpMail() {{
      if (typeof window.closeGbaStarterManualModal === 'function') window.closeGbaStarterManualModal();
      const lead = document.getElementById('gba-substack-subscribe');
      if (lead && lead.scrollIntoView) lead.scrollIntoView({{ behavior: 'smooth', block: 'center' }});
    }}
  </script>
</body>
</html>
"""
    out_file = JP_DIR / "daily-nisa-quant-report.html"
    out_file.write_text(page_html, encoding="utf-8")

    if SITEMAP_PATH.exists():
        smap = SITEMAP_PATH.read_text(encoding="utf-8")
        if canonical_url not in smap and "</urlset>" in smap:
            entry = (
                f"  <url>\n    <loc>{canonical_url}</loc>\n"
                f"    <lastmod>{today_iso}</lastmod>\n    <changefreq>daily</changefreq>\n"
                f"    <priority>0.92</priority>\n  </url>\n</urlset>"
            )
            smap = smap.replace("</urlset>", entry)
        smap = re.sub(r"\s*<url>\s*<loc>[^<]*(?:confirmation|soxl-smh-semiconductor-timing)\.html</loc>[\s\S]*?</url>", "", smap)
        SITEMAP_PATH.write_text(smap, encoding="utf-8")

    return canonical_url


if __name__ == "__main__":
    url = generate_daily_jp_column()
    print(f"[JP Daily Column] Generated {url}")
