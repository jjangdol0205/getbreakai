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
    POLAR_MONTHLY_CTA_HREF,
    POLAR_ANNUAL_CTA_HREF,
    PRICE_LABEL_MONTHLY_JP,
    PRICE_LABEL_ANNUAL_JP,
    MANDATORY_DISCLAIMER_JP,
    FSA_HYBRID_PHRASE_JP,
    build_payment_and_kpi_head_html,
    build_mandatory_disclaimer_html,
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
        ("VYM", "バンガード米国高配当株ETF（新NISA適格・四半期）", 134.50, 2.10),
        ("MSFT", "マイクロソフト（新NISA成長枠・連続増配）", 448.20, 9.40),
        ("AAPL", "アップル（新NISA成長枠・株主還元）", 232.80, 4.90),
        ("NVDA", "エヌビディア（公開決算データ参考）", 186.64, 8.02),
        ("AVGO", "ブロードコム（半導体・増配実績参考）", 293.69, 15.14),
    ]
    table_rows_html = ""
    for sym, jp_nm, fb_close, fb_atr in default_rows:
        info = tickers.get(sym, {}) if isinstance(tickers, dict) else {}
        close_p = float(info.get("entry") or info.get("close") or info.get("price") or fb_close)
        atr_v = float(info.get("atr") or info.get("atr14") or fb_atr)
        band_low = round(max(0.5, close_p - 2.0 * atr_v), 2)
        band_high = round(close_p + 5.0 * atr_v, 2)
        jpy_band_per_share = int(round((2.0 * atr_v) * usdjpy))
        shares_for_15k_jpy = max(1, int(15000 // max(jpy_band_per_share, 1)))
        table_rows_html += (
            f'<tr><td><strong><a href="/jp/?ticker={sym}#jpQuickCalcSection">${sym} ({jp_nm})</a></strong></td>'
            f"<td>${close_p:.2f}</td><td>${atr_v:.2f}</td>"
            f'<td style="color:#be123c;font-weight:700;">${band_low:.2f}</td>'
            f'<td style="color:#047857;font-weight:700;">${band_high:.2f}</td>'
            f"<td>{shares_for_15k_jpy}株 (100万円あたり分散目安)</td></tr>\n"
        )

    canonical_url = "https://getbreakai.com/jp/daily-nisa-quant-report.html"
    title = f"【朝のゆとり老後＆新NISA公開データ日報 {today_iso}】新NISA適格（VYM・HDV・1489）＋特定口座（SGOV・JEPI）ハイブリッド配分と手取り比較"
    desc = f"{today_iso}更新：ドル円({usdjpy:.1f}円)連動の公開市場データと{FSA_HYBRID_PHRASE_JP}の非課税(0%) vs 特定口座(20.315%)比較。"
    empathy_html = _build_morning_empathy_card(today_iso)

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
                },
                {
                    "@type": "FAQPage",
                    "mainEntity": [
                        {
                            "@type": "Question",
                            "name": "新NISA成長投資枠と特定口座（源泉徴収あり20.315%）はどう使い分けるべきですか？",
                            "acceptedAnswer": {
                                "@type": "Answer",
                                "text": "日本の金融庁規定により、毎月分配型ETF（JEPI・SGOV等）やレバレッジ型ETF（SOXL等）は新NISA対象外です。新NISA枠では四半期配当の1489・VYM・HDVやオルカン・S&P500を保有し、毎月分配のSGOV・JEPIは特定口座で管理するハイブリッド設計が準拠しています。",
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
    manual_modal = build_starter_manual_modal_html()
    waitlist_modal = build_vip_waitlist_modal_html()
    footer_html = build_legal_footer_html()

    page_html = f"""<!DOCTYPE html>
<html lang="ja" data-jp-theme="light">
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
  <link rel="icon" type="image/svg+xml" href="/favicon.svg" />
  <script type="application/ld+json">{ld_json}</script>
{head_scripts}
  <style>
    body {{ margin:0; font-family:'Noto Sans JP',-apple-system,BlinkMacSystemFont,sans-serif; background:#f4f6fa; color:#0f172a; line-height:1.8; font-size:17px; font-feature-settings:"palt" 1; }}
    a {{ color:#1d4ed8; text-decoration:none; }}
    .nav {{ background:#0b1f3a; border-bottom:2px solid #1e3a8a; padding:0.95rem 1.25rem; display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:10px; }}
    .wrap {{ max-width:920px; margin:0 auto; padding:2rem 1.2rem 3rem; }}
    .tag {{ display:inline-block; background:#eff6ff; color:#1e40af; border:1px solid #93c5fd; border-radius:999px; padding:0.25rem 0.85rem; font-size:0.84rem; font-weight:800; }}
    h1 {{ font-size:clamp(1.45rem,3vw,2rem); color:#0b1f3a; line-height:1.38; margin:0.8rem 0; }}
    h2 {{ color:#1e3a8a; font-size:1.25rem; border-left:5px solid #1d4ed8; background:#eff6ff; padding:0.45rem 0.75rem; border-radius:0 8px 8px 0; margin-top:2rem; }}
    .table-wrap {{ overflow-x:auto; }}
    table {{ width:100%; border-collapse:collapse; margin:1.1rem 0; background:#ffffff; font-size:0.94rem; border:1px solid #cbd5e1; border-radius:10px; overflow:hidden; }}
    th, td {{ padding:0.75rem 0.85rem; border-bottom:1px solid #e2e8f0; text-align:left; }}
    th {{ background:#0b1f3a; color:#ffffff; font-size:0.84rem; }}
    .cta {{ background:linear-gradient(135deg,#ecfdf5,#eff6ff); border:2px solid #059669; border-radius:14px; padding:1.5rem; margin:2rem 0; }}
    .btns {{ display:flex; flex-wrap:wrap; gap:0.75rem; margin-top:1rem; }}
    .btn {{ padding:0.75rem 1.2rem; border-radius:10px; font-weight:900; font-size:0.96rem; display:inline-flex; align-items:center; min-height:54px; }}
    .btn-primary {{ background:#059669; color:#ffffff !important; }}
    .btn-vip {{ background:#1d4ed8; color:#ffffff !important; }}
    .btn-annual {{ background:#b45309; color:#ffffff !important; }}
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
  <header class="nav">
    <a href="/jp/" style="font-weight:900;color:#ffffff;font-size:1.1rem;">⚡ GetBreakAI ゆとり老後＆新NISA設計ナビ</a>
    <div style="display:flex;gap:12px;align-items:center;flex-wrap:wrap;">
      <button type="button" onclick="openGbaStarterManualModal()" style="background:#065f46;color:#ffffff;border:1px solid #10b981;border-radius:8px;padding:6px 12px;font-weight:800;cursor:pointer;">📘 ¥0 基本マニュアル</button>
      <a href="/jp/#gba-retirement-architect-jp" style="color:#93c5fd;font-weight:800;">🧭 30秒・老後収入シミュレーター</a>
      <a href="/jp/feed.xml" style="color:#e2e8f0;font-size:0.9rem;">RSS</a>
    </div>
  </header>
  <main class="wrap">
    <span class="tag">GetBreakAI 朝のゆとり老後＆資産守り倶楽部 · 公開市場データ日報 · {today_iso}</span>
    <h1>{html.escape(title)}</h1>
    <p style="color:#475569;font-size:1rem;font-weight:700;">為替参照レート: 1ドル = {usdjpy:.1f}円 · 金融庁・新NISA規定準拠ハイブリッド設計対応</p>
{empathy_html}

    <section id="gba-daily-lead-top" class="cta">
      <div style="font-size:0.92rem;font-weight:900;color:#065f46;margin-bottom:0.4rem;">🍵 毎朝8時の無料3色バランス指標ブリーフ（パスワード不要）</div>
      <h2 style="margin:0 0 0.5rem;border:none;background:transparent;padding:0;font-size:1.3rem;color:#0b1f3a;">毎朝8時の「新NISA×特定口座 3色バランス指標」無料メール登録</h2>
      <p style="margin:0 0 0.9rem;color:#334155;font-size:1rem;">メールアドレス1つ（3秒）で、日米金利・為替と老後3つの財布の公開データ要約を毎朝無料でお届けします。</p>
      <form class="gba-jp-signup-form" onsubmit="return window.__gbaSubmitJpSignup(event, this, 'NISA_DAILY');" style="display:flex;flex-wrap:wrap;gap:0.65rem;">
        <input type="email" required autocomplete="email" placeholder="メールアドレスを入力（例: yamada@yahoo.co.jp）" style="flex:1 1 250px;min-height:54px;padding:10px 16px;font-size:1.02rem;font-weight:700;border-radius:10px;border:2px solid #64748b;background:#ffffff;color:#0f172a;" />
        <button type="submit" style="min-height:54px;padding:10px 22px;font-size:1.02rem;font-weight:900;border-radius:10px;border:none;background:#059669;color:#ffffff;cursor:pointer;">📩 無料で毎朝の3色ブリーフを受け取る →</button>
      </form>
      <div class="gba-jp-signup-status" role="status" aria-live="polite" style="display:none;margin-top:0.75rem;padding:0.75rem 0.95rem;border-radius:8px;background:#d1fae5;color:#065f46;font-size:1rem;font-weight:800;"></div>
      <div class="btns" style="margin-top:1rem;padding-top:0.9rem;border-top:1px solid #a7f3d0;align-items:center;">
        <span style="font-size:0.95rem;font-weight:800;color:#0f172a;">💎 配当・資産配分計算Proソフトウェア（随時更新・新NISA老後取り崩し実践PDFガイド＋3つの財布シミュレーター同梱）：</span>
        <a class="btn btn-vip polar-checkout-button" data-gba-paid-plan="monthly" data-polar-slot="monthly_29_jp" href="{POLAR_MONTHLY_CTA_HREF}">⚡ {PRICE_LABEL_MONTHLY_JP}</a>
        <a class="btn btn-annual polar-checkout-button" data-gba-paid-plan="annual" data-polar-slot="annual_199_jp" href="{POLAR_ANNUAL_CTA_HREF}">👑 {PRICE_LABEL_ANNUAL_JP}</a>
      </div>
      <div style="margin-top:0.5rem;font-size:0.84rem;color:#334155;font-weight:700;">💳 公式決済・税務管理：{MOR_LABEL_EN_JP}（14日間返金保証）</div>
{disclaimer_box}
    </section>

    <h2>1. 【金融庁規定準拠】新NISA適格銘柄と特定口座（毎月分配型）のハイブリッド設計</h2>
    <p>日本の金融庁規定により、<strong>毎月分配型ETF（JEPI・JEPQ・QYLD・SGOV等）およびレバレッジ型ETF（SOXL・TQQQ等）は新NISAの対象外</strong>であり、特定口座（源泉徴収あり・税率20.315%）でのみ保有可能です。そのため老後の毎月キャッシュフロー設計では、<strong>{FSA_HYBRID_PHRASE_JP}</strong>を採用し、新NISA枠内では四半期配当ETFの時間差組み合わせ（1・4・7・10月の1489 × 3・6・9・12月のVYM・HDV）とオルカン・S&amp;P500で非課税メリットを最大化します。</p>

    <h2>2. 公開市場データによる1銘柄あたり分散配分目安一覧 ({today_iso})</h2>
    <div class="table-wrap">
      <table>
        <thead>
          <tr><th>銘柄</th><th>直近終値</th><th>14日平均変動幅</th><th>2.0倍変動参考下限</th><th>長期参考上限</th><th>100万円口座 分散株数目安</th></tr>
        </thead>
        <tbody>
          {table_rows_html}
        </tbody>
      </table>
    </div>

    <h2>3. 新NISA（非課税0%）vs 特定口座（20.315%）の手取り比較</h2>
    <p>新NISA成長投資枠（年間240万円・つみたて投資枠と合計360万円）では配当金および売却益に対する国内20.315%課税が非課税となる一方、特定口座と損益通算はできません。したがって頻繁な売買で年間枠を消費するのではなく、年2〜4回の穏やかな資産配分点検で長期保有を続ける設計が有効です。</p>

    <section id="gba-daily-lead-bottom" class="cta">
      <h3 style="margin:0 0 0.5rem;color:#0b1f3a;font-size:1.25rem;">🍵 無料メール倶楽部（登録3秒）＆ Pro計算ソフトウェア</h3>
      <form class="gba-jp-signup-form" onsubmit="return window.__gbaSubmitJpSignup(event, this, 'NISA_DAILY');" style="display:flex;flex-wrap:wrap;gap:0.65rem;margin-bottom:0.9rem;">
        <input type="email" required autocomplete="email" placeholder="メールアドレスを入力（例: yamada@yahoo.co.jp）" style="flex:1 1 250px;min-height:54px;padding:10px 16px;font-size:1.02rem;font-weight:700;border-radius:10px;border:2px solid #64748b;background:#ffffff;color:#0f172a;" />
        <button type="submit" style="min-height:54px;padding:10px 22px;font-size:1.02rem;font-weight:900;border-radius:10px;border:none;background:#059669;color:#ffffff;cursor:pointer;">📩 無料倶楽部に参加する →</button>
      </form>
      <div class="gba-jp-signup-status" role="status" aria-live="polite" style="display:none;margin-bottom:0.9rem;padding:0.75rem 0.95rem;border-radius:8px;background:#d1fae5;color:#065f46;font-size:1rem;font-weight:800;"></div>
      <div class="btns">
        <a class="btn btn-primary" href="/jp/#gba-retirement-architect-jp">🧭 30秒・老後キャッシュフローシミュレーターを開く →</a>
        <a class="btn btn-vip polar-checkout-button" data-gba-paid-plan="monthly" data-polar-slot="monthly_29_jp" href="{POLAR_MONTHLY_CTA_HREF}">⚡ {PRICE_LABEL_MONTHLY_JP}</a>
        <a class="btn btn-annual polar-checkout-button" data-gba-paid-plan="annual" data-polar-slot="annual_199_jp" href="{POLAR_ANNUAL_CTA_HREF}">👑 {PRICE_LABEL_ANNUAL_JP}</a>
      </div>
      <div style="margin-top:0.6rem;font-size:0.84rem;color:#334155;font-weight:700;">💳 {MOR_LABEL_EN_JP} ｜ 🏛️ 法人・メディア提携窓口: <a href="mailto:beable9489@gmail.com" style="font-weight:800;">beable9489@gmail.com</a></div>
{disclaimer_box}
    </section>
  </main>

{footer_html}
{manual_modal}
{waitlist_modal}

  <script>
    function jumpFromManualToJpMail() {{
      if (typeof window.closeGbaStarterManualModal === 'function') window.closeGbaStarterManualModal();
      const lead = document.getElementById('gba-daily-lead-top');
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
        smap = re.sub(r"\s*<url>\s*<loc>[^<]*confirmation\.html</loc>[\s\S]*?</url>", "", smap)
        SITEMAP_PATH.write_text(smap, encoding="utf-8")

    return canonical_url


if __name__ == "__main__":
    url = generate_daily_jp_column()
    print(f"[JP Daily Column] Generated {url}")
