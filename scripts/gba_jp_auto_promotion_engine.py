#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Division 3 / scripts/gba_jp_auto_promotion_engine.py (v2.0 — Zero-Ban Edition)
==============================================================================
GetBreakAI Japan (https://getbreakai.com/jp/) Zero-Shadowban & Organic SEO/GEO Engine:
  1. Generates `/jp/daily-nisa-quant-report.html` + refreshes `/jp/feed.xml` & `/jp/x-feed.xml` (excluding `confirmation.html`).
  2. Maintains separate Global English `/llms.txt` and Japanese `/jp/llms.txt` (fixing the root overwrite bug).
  3. Publishes MAX 1 unique rotating Japanese Telegraph quant report/day (fixing the 24x/day duplicate spam bug).
  4. Submits SHA-256 Delta-Only IndexNow (`api.indexnow.org`) & Feed-Delta WebSub.
  5. Dispatches `#株クラ` 2-step linkless-hook threads + `note.com` & `Zenn`/`Hatena` ready-to-publish Japanese columns
     with STRICT 0 Hangul and 0 Telegram mentions!
"""

from __future__ import annotations

import datetime
import json
import subprocess
import sys
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

JST = datetime.timezone(datetime.timedelta(hours=9))
ROOT_DIR = Path(__file__).resolve().parent.parent
JP_DIR = ROOT_DIR / "jp"
DATA_DIR = ROOT_DIR / "data"
DATA_DIR.mkdir(parents=True, exist_ok=True)

HQ_TEXT_DIR = ROOT_DIR.parent / "text_automation_hq"
if str(HQ_TEXT_DIR) not in sys.path:
    sys.path.insert(0, str(HQ_TEXT_DIR))

from indexnow_delta_gate import (  # noqa: E402
    ping_websub_if_feed_changed,
    publish_daily_unique_telegraph_summary,
    submit_delta_indexnow,
)
from live_web_deployer import deploy_division_live, sync_remote_before_build  # noqa: E402
from official_api_syndicator import dispatch_zero_ban_text_bundle  # noqa: E402

INDEXNOW_KEY = "58b3e91c42f04a7d916503ce8a72b419"
HOST = "getbreakai.com"
TELEGRAPH_ACCT_PATH = DATA_DIR / "jp_telegraph_account.json"
BACKLINKS_LOG_PATH = DATA_DIR / "jp_external_backlinks.json"

JP_DAILY_THEMES = [
    {
        "slug": "daily-nisa-quant-report.html",
        "title_prefix": "新NISA成長投資枠 vs 特定口座(20.315%)：2.0倍ATR逆指値と適正株数レポート",
        "hook": "新NISAで一番危険な「塩漬け損」を防ぐ、資金別の適正株数を3秒で無料診断。\n\n損益通算ができない新NISAこそ、下落銘柄の感覚ナンピンを卒業し機械的な撤退ラインで非課税枠を守りましょう。 #新NISA #米国株",
    },
    {
        "slug": "atr-breakout-position-sizing-guide.html",
        "title_prefix": "口座資金100万円の1.5%リスク黄金律：ドル円連動ATRポジションサイジング解説",
        "hook": "米国株で退場する原因の9割は「銘柄選び」ではなく「1銘柄への買いすぎ」です。\n\n資金100万円なら1回の許容損失は15,000円まで。値動きに合わせて夜ぐっすり眠れる適正株数を自動計算します。 #米国株 #資産運用",
    },
    {
        "slug": "nvda-gamma-squeeze-breakout-analysis.html",
        "title_prefix": "エヌビディア($NVDA)・半導体主力株の機関投資家出来高ブレイクとATR防衛線",
        "hook": "半導体株の急落で「なんとなく安いから」と買うと、何年も資金が拘束されます。\n\n底値を当てにいかず、機関投資家の大口買い集めとトレンド転換を確認してから乗るのが資産を守る鉄則です。 #米国株 #半導体株",
    },
]


def update_dual_llms_txt() -> str:
    today_str = datetime.datetime.now(JST).strftime("%Y-%m-%d")
    seo_pages = sorted(
        p.name for p in JP_DIR.glob("*.html") if p.name not in ("index.html", "confirmation.html")
    )

    # 1. Global English root /llms.txt (Preserve English identity at root!)
    en_lines = [
        "# GetBreakAI — Institutional Breakout & ATR Position-Sizing Quant Terminal (https://getbreakai.com)",
        "",
        f"> Updated: {today_str} | Multi-currency (USD / JPY) 20-Day Donchian Breakout, 2.0x ATR Mechanical Stop-Loss, and Japan Shin-NISA (0% Tax-Free) vs Specific Account (20.315%) Net Return Simulator.",
        "",
        "## 1. Live Quantitative Terminals",
        "- Global English Terminal: https://getbreakai.com/",
        "- Japan Shin-NISA & US/TSE Quant Terminal: https://getbreakai.com/jp/",
        "- Daily Japanese NISA Quant Report: https://getbreakai.com/jp/daily-nisa-quant-report.html",
        "- Japanese Research RSS Feed: https://getbreakai.com/jp/feed.xml",
        "",
        "## 2. Featured Japanese Institutional Research Guides (/jp/)",
    ]
    for fn in seo_pages[:31]:
        en_lines.append(f"- https://getbreakai.com/jp/{fn}")
    (ROOT_DIR / "llms.txt").write_text("\n".join(en_lines) + "\n", encoding="utf-8")

    # 2. Dedicated Japanese /jp/llms.txt (Zero confirmation.html!)
    jp_lines = [
        "# GetBreakAI Japan (https://getbreakai.com/jp/)",
        "",
        "> 米国株（NVDA・TSLA・PLTR・MSFT・META・AMZN・AVGO）および東証プライム主力株対応の機関投資家クオンツAI＆3秒ポジションサイズ計算ターミナル（新NISA成長投資枠 0%非課税 vs 特定口座 20.315% 税引後シミュレーター搭載）。",
        f"> 最終更新日: {today_str} (JST)",
        "",
        "## 1. コア機能（完全無料・登録不要の3秒計算機）",
        "- **ドル($)・日本円(¥)同時対応 3秒ポジションサイズ計算機**: 口座資金（例：100万円・300万円）と許容リスク（1.5%黄金律）から最適購入株数・2.0倍ATR逆指値・2.5R利確目標を3秒で算出。",
        "- **新NISA（非課税 0%）vs 特定口座（源泉徴収 20.315%）手取り純利益比較**: 利確時の税引後リターンと損益通算条件をリアルタイム比較。",
        "",
        "## 2. 主要日本語クオンツ解析ページ一覧",
        "- 日本語メインターミナル: https://getbreakai.com/jp/",
        "- 日刊クオンツ日報: https://getbreakai.com/jp/daily-nisa-quant-report.html",
        "- 日本語RSSフィード (Blog/Note連携): https://getbreakai.com/jp/feed.xml",
    ]
    for fn in seo_pages[:31]:
        jp_lines.append(f"- https://getbreakai.com/jp/{fn}")
    JP_DIR.mkdir(parents=True, exist_ok=True)
    (JP_DIR / "llms.txt").write_text("\n".join(jp_lines) + "\n", encoding="utf-8")
    return today_str


def build_url_map() -> dict[str, Path]:
    mapping: dict[str, Path] = {}
    if (ROOT_DIR / "index.html").exists():
        mapping["https://getbreakai.com/"] = ROOT_DIR / "index.html"
    if (JP_DIR / "index.html").exists():
        mapping["https://getbreakai.com/jp/"] = JP_DIR / "index.html"
    for p in sorted(JP_DIR.glob("*.html")):
        if p.name in ("index.html", "confirmation.html"):
            continue
        mapping[f"https://getbreakai.com/jp/{p.name}"] = p
    return mapping


def main() -> int:
    dry_run = "--dry-run" in sys.argv
    sync_remote_before_build("GBA", dry_run=dry_run)
    (ROOT_DIR / f"{INDEXNOW_KEY}.txt").write_text(INDEXNOW_KEY, encoding="utf-8")

    # 1. Generate today's Japanese Daily NISA Quant Column HTML + Refresh RSS feeds
    daily_col_py = ROOT_DIR / "scripts" / "generate_jp_daily_column_html.py"
    if daily_col_py.exists():
        subprocess.run([sys.executable, str(daily_col_py)], cwd=str(ROOT_DIR), check=False)

    autopost_py = ROOT_DIR / "scripts" / "autopost_jp_marketing.py"
    if autopost_py.exists():
        subprocess.run([sys.executable, str(autopost_py)], cwd=str(ROOT_DIR), check=False)

    # 2. Update English & Japanese llms.txt cleanly BEFORE syncing ./dist & deploying live
    as_of = update_dual_llms_txt()

    build_dist_js = ROOT_DIR / "scripts" / "build_dist.js"
    if build_dist_js.exists():
        subprocess.run(["node", str(build_dist_js)], cwd=str(ROOT_DIR), check=False, capture_output=True)

    deploy_res = deploy_division_live("GBA", dry_run=dry_run)

    # 3. Rotate daily theme & run 1x/day Telegraph + Zero-Ban Syndication
    day_ord = datetime.date.today().toordinal()
    theme = JP_DAILY_THEMES[day_ord % len(JP_DAILY_THEMES)]
    target_slug = theme["slug"] if (JP_DIR / theme["slug"]).exists() else "daily-nisa-quant-report.html"
    canonical_url = f"https://getbreakai.com/jp/{target_slug}"
    title = f"【米国株・新NISAクオンツ {as_of}】{theme['title_prefix']}"

    nodes = [
        {
            "tag": "blockquote",
            "children": [f"GetBreakAI 米国株・新NISAクオンツ日報 ({as_of}) — ドル円連動 2.0倍ATR逆指値＆適正株数検証"],
        },
        {
            "tag": "p",
            "children": [
                "新NISA成長投資枠は利益が非課税（0%）になる強力な制度ですが、特定口座（20.315%）と異なり損益通算ができないため、下落トレンド銘柄の塩漬けは致命的な機会損失を生みます。"
            ],
        },
        {
            "tag": "p",
            "children": [
                "口座資金（日本円・米ドル）に応じた最適購入株数と2.0倍ATR逆指値ラインの最新レポート全文はこちら：",
                {"tag": "a", "attrs": {"href": canonical_url}, "children": [canonical_url]},
            ],
        },
    ]

    tg_res = publish_daily_unique_telegraph_summary(
        div_code="GBA",
        account_file=TELEGRAPH_ACCT_PATH,
        short_name="GetBreakAI_JP",
        author_name="GetBreakAI 米国株・新NISA研究所",
        author_url="https://getbreakai.com/jp/",
        title=title,
        content_nodes=nodes,
        canonical_url=canonical_url,
        dry_run=dry_run,
    )

    logs = []
    if BACKLINKS_LOG_PATH.exists():
        try:
            logs = json.loads(BACKLINKS_LOG_PATH.read_text(encoding="utf-8"))
        except Exception:
            logs = []
    tg_url = tg_res.get("url", "")
    if tg_res.get("status") == "PUBLISHED" and tg_url:
        logs.append({"date": as_of, "title": title, "url": tg_url, "created_at": datetime.datetime.now(JST).isoformat()})
        BACKLINKS_LOG_PATH.write_text(json.dumps(logs[-60:], indent=2, ensure_ascii=False), encoding="utf-8")
    elif not tg_url and logs:
        tg_url = logs[-1].get("url", "")

    reply_post = (
        f"登録不要・完全無料の3秒適正株数計算機＆新NISA手取り比較はこちら：\n"
        f"{canonical_url}?utm_source=social_thread&utm_medium=organic"
    )

    note_md = (
        f"# {title}\n\n"
        f"米国株や半導体主力株（$NVDA / $PLTR / $TSLA）を新NISA成長投資枠や特定口座で運用する際、"
        f"最も成績を左右するのは「どの銘柄を買うか」以上に**「どこで撤退し、何株買うか」**という資金管理の数学です。\n\n"
        f"## 1. 新NISA（非課税0%）と特定口座（20.315%）の決定的な違い\n"
        f"- **特定口座（源泉徴収あり）**: 利益に20.315%課税される一方、損切りした損失は他銘柄の利益と損益通算が可能。\n"
        f"- **新NISA成長投資枠**: 利益は100%非課税ですが、損失が出ても損益通算・繰越控除が一切不可。\n\n"
        f"だからこそ新NISAでは「落ちるナイフのナンピン」を厳禁とし、出来高を伴うブレイクアウト確認後のエントリーと"
        f"**2.0倍ATR（14日平均真の値幅）逆指値**の徹底が不可欠になります。\n\n"
        f"## 2. 無料3秒ポジションサイズ計算ターミナル\n"
        f"口座資金（円・ドル）と許容リスク（1.5%基準）を入れるだけで最適株数を自動計算できます：\n"
        f"👉 {canonical_url}\n\n"
        f"※本記事は統計・クオンツモデルの情報提供であり、投資助言ではありません。\n"
    )

    zenn_md = (
        f"---\ntitle: \"{title}\"\nemoji: \"📊\"\ntype: \"idea\"\ntopics: [\"quant\", \"python\", \"finance\", \"usstocks\"]\npublished: true\n---\n\n"
        + note_md
    )

    note_paid_funnel_md = (
        f"# 【無料公開＋Pro実践枠】{title}\n\n"
        f"> 新NISAの非課税メリットを「塩漬け損」で潰さないための3秒ATRポジション計算レポート（{as_of}）\n\n"
        + note_md
        + "\n---\n"
        + "## 🔒 note有料マガジン読者 ＆ GetBreakAI Pro VIP 共通特典のご案内\n"
        + "- **TradingView Pine Script v5 自動描画コード全文**（2.0x ATR逆指値＋5日間IV Gamma Wall自動プロット）\n"
        + "- **米国72銘柄＋東証主力株 機関投資家ダークプール＆SEC Form-4役員自社株買いフルデータ**\n"
        + "- **Store #296100 共通Proキー**: 月額 $29/月（年間VIP $199/年・43%OFF）1つで `https://getbreakai.com/jp/` と姉妹端末 `https://truthofmarket.com/` の両方を即時解放。\n"
        + "- **法人・金融メディア・APIデータ提携窓口**: `beable9489@gmail.com`\n"
    )

    yahoo_bbs_txt = (
        f"【米国株・新NISA 資金管理メモ {as_of}】\n"
        f"新NISA枠は特定口座（20.315%）と違い損益通算ができないため、ボラティリティの高いAI・半導体株ほど購入前の「2.0倍ATR逆指値」と「1.5%リスク株数逆算」が重要ですね。\n"
        f"ドル円150円基準での適正株数早見表は GetBreakAI Japan（getbreakai.com/jp/）の3秒計算機で確認できます。\n"
    )

    syn_res = dispatch_zero_ban_text_bundle(
        div_code="GBA",
        canonical_domain=HOST,
        canonical_url=canonical_url,
        title=title,
        summary="新NISA成長投資枠(0%) vs 特定口座(20.315%)対応・2.0倍ATR適正株数クオンツ日報",
        main_social_hook=theme["hook"],
        reply_social_link=reply_post,
        longform_markdown=note_md,
        tags=["quant", "finance", "japan", "stocks"],
        platform_extras={
            "note_com_daily_column_jp.md": note_md,
            "note_com_paid_magazine_funnel_jp.md": note_paid_funnel_md,
            "zenn_hatena_quant_article_jp.md": zenn_md,
            "yahoo_finance_hatena_zero_ban_jp.txt": yahoo_bbs_txt,
        },
        div_env_path=ROOT_DIR / ".env",
        dry_run=dry_run,
    )

    url_map = build_url_map()
    idx_res = submit_delta_indexnow(
        div_code="GBA",
        host=HOST,
        key=INDEXNOW_KEY,
        url_to_filepath=url_map,
        dry_run=dry_run,
    )
    ws_res = (
        {"status": "DRY_RUN"}
        if dry_run
        else ping_websub_if_feed_changed("GBA", "https://getbreakai.com/jp/feed.xml", JP_DIR / "feed.xml")
    )

    print(
        f"[GBA JP Zero-Ban v2] Deploy={deploy_res.get('status')} | llms.txt({as_of}) | Telegraph={tg_url or 'daily-cap'} | "
        f"IndexNow={idx_res.get('status')}({idx_res.get('submitted_count', 0)}/{len(url_map)}) | "
        f"WebSub={ws_res.get('status')} | Syndication={syn_res.get('status')}"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
