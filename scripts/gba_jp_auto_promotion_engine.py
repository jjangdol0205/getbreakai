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

from fandom_editor_letter_builder import (  # noqa: E402
    compose_fandom_editor_letter_md,
    validate_fandom_editor_letter,
)
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
        "title_prefix": "新NISA成長投資枠と特定口座(20.315%)：大切な老後資金を「塩漬け損」から守る朝の3色シグナル",
        "hook": "新NISAで一番怖い「塩漬け損」を防ぐ適正株数を、3秒で無料診断できます。\n\n損益通算ができない新NISAこそ、感覚ナンピンを卒業し「青・黄・赤」の明確な撤退ルールで非課税枠を守りましょう。 #新NISA #米国株",
    },
    {
        "slug": "shin-nisa-us-stock-atr-risk-management.html",
        "title_prefix": "資金100万円なら許容損失は1.5万円まで：夜ぐっすり眠れる新NISA適正株数の決め方",
        "hook": "米国株で資産を減らす原因の9割は「1銘柄への買いすぎ」にあります。\n\n資金100万円なら1回の許容損失は15,000円まで。値動きに合わせて夜ぐっすり眠れる購入株数を3秒で無料計算します。 #新NISA #資産運用",
    },
    {
        "slug": "nvda-sec-gamma-atr-analysis.html",
        "title_prefix": "エヌビディア・半導体株の急落で慌てない！高値掴みと塩漬けを防ぐ3色売買ルール",
        "hook": "半導体株の急落で「なんとなく安いから」と買うと資金が何年も眠ります。\n\n底値を当てにいかず、大口資金の買い集めと「青シグナル（順張り転換）」を確認してから落ち着いて検討するのが鉄則です。 #米国株 #半導体株",
    },
    {
        "slug": "us-stock-stop-loss-2percent-rule.html",
        "title_prefix": "「いつか戻る」が一番危険？退職金・老後資金を減らさない米国株の安全撤退ライン入門",
        "hook": "「いつか戻る」と待つうちに、大切な老後資金が半分になることがあります。\n\n株価が50%下がると元に戻すには+100%の上昇が必要です。浅い傷のうちに守る「赤シグナル撤退線」を無料確認できます。 #新NISA #老後資金",
    },
    {
        "slug": "unh-defensive-healthcare-insider-buy.html",
        "title_prefix": "ハイテク株だけに偏っていませんか？守りのヘルスケア株を添える大人の新NISA資産防衛術",
        "hook": "ハイテク株だけに偏らず、守りの銘柄を添えると新NISAはぐっと安定します。\n\n値動きの大きい半導体株と堅実なヘルスケア株を組み合わせ、急落時も慌てない資産配分と適正株数を無料診断しましょう。 #新NISA #資産防衛",
    },
]


def load_live_usd_jpy() -> float:
    snap_path = DATA_DIR / "live_market_snapshot.json"
    try:
        if snap_path.exists():
            snap = json.loads(snap_path.read_text(encoding="utf-8"))
            rate = float(snap.get("usd_jpy") or 0)
            if rate > 80.0:
                return round(rate, 2)
    except Exception:
        pass
    return 155.0


def update_dual_llms_txt() -> str:
    today_str = datetime.datetime.now(JST).strftime("%Y-%m-%d")
    seo_pages = sorted(
        p.name
        for p in JP_DIR.glob("*.html")
        if p.name not in ("index.html", "confirmation.html") and not p.name.startswith("google")
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

    # 2. Dedicated Japanese /jp/llms.txt (Zero confirmation.html & Zero Hangul!)
    jp_lines = [
        "# GetBreakAI Japan (https://getbreakai.com/jp/)",
        "",
        "> 日本の40代〜70代個人投資家・新NISA運用層のための「毎朝の3色売買シグナル（青＝順張り維持・黄＝様子見・赤＝安全撤退ライン）」＆3秒適正株数シミュレーター（新NISA成長投資枠 0%非課税 vs 特定口座 20.315% 手取り純利益比較対応）。",
        f"> 最終更新日: {today_str} (JST)",
        "",
        "## 1. コア機能（メール1つで毎朝の無料3色シグナル受信＆3秒計算機）",
        "- **毎朝の無料3色売買シグナル配信**: メールアドレス1つで、米国主力株・日本半導体株の「青・黄・赤」安全判定を毎朝無料でお届けします。",
        "- **ドル($)・日本円(¥)同時対応 3秒適正株数シミュレーター**: ご資金（例：100万円・300万円）と許容リスク（1.5%ルール）から、夜ぐっすり眠れる購入株数と撤退ラインを3秒で算出。",
        "- **新NISA（非課税 0%）vs 特定口座（源泉徴収 20.315%）手取り比較**: 利確時の税引後手取り額と損益通算の違いを分かりやすく比較。",
        "",
        "## 2. 主要日本語コラム・解析ページ一覧",
        "- 日本語メインターミナル: https://getbreakai.com/jp/",
        "- 本日の新NISA・老後資金3色シグナル日報: https://getbreakai.com/jp/daily-nisa-quant-report.html",
        "- 日本語RSSフィード (Blog/note連携): https://getbreakai.com/jp/feed.xml",
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
        if p.name in ("index.html", "confirmation.html") or p.name.startswith("google"):
            continue
        mapping[f"https://getbreakai.com/jp/{p.name}"] = p
    return mapping


def main() -> int:
    dry_run = "--dry-run" in sys.argv
    no_deploy = "--no-deploy" in sys.argv
    if not no_deploy:
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
    if no_deploy:
        dist_jp = ROOT_DIR / "dist" / "jp"
        if dist_jp.exists() and (JP_DIR / "daily-nisa-quant-report.html").exists():
            (dist_jp / "daily-nisa-quant-report.html").write_text(
                (JP_DIR / "daily-nisa-quant-report.html").read_text(encoding="utf-8"),
                encoding="utf-8",
            )
    elif build_dist_js.exists():
        subprocess.run(["node", str(build_dist_js)], cwd=str(ROOT_DIR), check=False, capture_output=True)

    deploy_res = {"status": "SKIPPED_NO_DEPLOY"} if no_deploy else deploy_division_live("GBA", dry_run=dry_run)

    # 3. Rotate daily theme & run 1x/day Telegraph + Zero-Ban Syndication
    usd_jpy = load_live_usd_jpy()
    day_ord = datetime.date.today().toordinal()
    theme = JP_DAILY_THEMES[day_ord % len(JP_DAILY_THEMES)]
    target_slug = theme["slug"] if (JP_DIR / theme["slug"]).exists() else "daily-nisa-quant-report.html"
    canonical_url = f"https://getbreakai.com/jp/{target_slug}"
    title = f"【朝の資産防衛レター {as_of}】{theme['title_prefix']}"

    nodes = [
        {
            "tag": "blockquote",
            "children": [
                f"☀️ GetBreakAI 朝の資産防衛クラブ ({as_of} / 実勢レート 1ドル＝約{usd_jpy:.1f}円): おはようございます。昨夜の相場ニュースで新NISA枠や老後資金が不安になった方も、まずは温かいお茶を飲んでご安心ください。今朝も編集部があなたの味方として寄り添います。"
            ],
        },
        {
            "tag": "p",
            "children": [
                "新NISA成長投資枠は利益が非課税（0%）になる心強い制度ですが、特定口座（20.315%）と異なり他の利益と損益通算ができません。だからこそ「なんとなく安そうだから」と下落中の株をナンピンして何年も塩漬けにしないことが、大切な老後資金を守る一番の近道です。"
            ],
        },
        {
            "tag": "p",
            "children": [
                "今日1分の小さな安心ミッション：買う前にまず3秒シミュレーターでご資金に合う適正株数を確認してみましょう（無料メール1つで毎朝の3色シグナルも受け取れます）：",
                {"tag": "a", "attrs": {"href": canonical_url}, "children": [canonical_url]},
            ],
        },
    ]

    tg_res = publish_daily_unique_telegraph_summary(
        div_code="GBA",
        account_file=TELEGRAPH_ACCT_PATH,
        short_name="GetBreakAI_JP",
        author_name="GetBreakAI 朝の資産防衛パートナー",
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
        f"☀️ 今朝の資産防衛レター全文＆無料の3秒適正株数シミュレーターはこちら：\n"
        f"{canonical_url}?utm_source=social_thread&utm_medium=organic"
    )

    note_md = compose_fandom_editor_letter_md(
        div_code="GBA",
        title=title,
        canonical_url=canonical_url,
        empathy_two_lines=[
            "おはようございます。昨夜の米国株ニュースを見て「せっかく積み立てた新NISA枠や大切な老後資金が減ってしまったらどうしよう」と不安を感じた方は、まず深呼吸して温かい飲み物を一口どうぞ。",
            "50代・60代からの資産運用で一番大切なのは、無理に大勝ちを狙うことではなく、長年働いて築いたご資産を深い塩漬け損から穏やかに守り抜くことです。",
        ],
        three_insights=[
            "**新NISA（非課税0%）と特定口座（20.315%）のやさしい使い分け**: 特定口座は利益に20.315%課税される代わりに損切り額を損益通算できますが、新NISA枠は利益がまるごと非課税（0%）になる反面、損失の損益通算ができないため早めの安全撤退ルールが命綱になります。",
            "**迷わない毎朝の3色シグナル（Donchian 20日高値＆2.0倍ATR基準）**: 🔵青シグナル（上昇トレンド維持）・🟡黄シグナル（様子見・待機）・🔴赤シグナル（2.0倍ATR安全撤退ライン）の3色だけで落ち着いて手取りを守れます。",
            f"**実勢レート（1ドル＝約{usd_jpy:.1f}円）連動の適正株数ルール**: 例えば口座資金100万円なら1回の許容損失を1.5%（15,000円）以内に抑える株数だけを持つことで、夜ぐっすり眠れる運用が続けられます。",
        ],
        daily_mission=(
            "今日1分だけ、気になっている米国株1銘柄（NVDA・MSFT・AVGOなど）の「安全撤退ライン（2.0倍ATR）」を手帳やスマホのメモに書き留めてから相場を眺めてみましょう。"
        ),
        gentle_bridge_lines=[
            f"**今朝の資産防衛レター全文＆日課スタンプを押す**: {canonical_url}",
            f"**無料の3秒適正株数シミュレーター＆毎朝8時の無料3色シグナル配信（メール1つで開始）**: https://getbreakai.com/jp/ （まずは無料ツールだけで十分お役立ていただけます）",
            "**さらに詳しく見たい方へ（任意・Pro VIP）**: 全72銘柄のリアルタイム価格とTradingView自動描画をご希望の方には、月額 $29/月・年間パス $199/年プランもご用意しております。",
        ],
        footer_disclaimer="※本レターはGetBreakAI 朝の資産防衛クラブによる統計・教育目的の情報提供であり、個別銘柄の売買推奨や投資助言ではありません。",
    )
    gba_letter_check = validate_fandom_editor_letter("GBA", note_md)
    if not gba_letter_check["passed"]:
        raise RuntimeError(f"GBA Fandom Editor Letter validation failed: {gba_letter_check}")

    zenn_md = (
        f"---\ntitle: \"{title}\"\nemoji: \"📊\"\ntype: \"idea\"\ntopics: [\"nisa\", \"finance\", \"usstocks\", \"assetmanagement\"]\npublished: true\n---\n\n"
        + note_md
    )

    note_paid_funnel_md = (
        f"# 【無料公開＋Pro実践ガイド】{title}\n\n"
        f"> 大切な新NISA非課税枠と老後資金を「高値掴み・塩漬け損」から守る朝の3色シグナル日報（{as_of}）\n\n"
        + note_md
        + "\n---\n"
        + "## 🔒 GetBreakAI Pro VIP メンバーシップのご案内\n"
        + "- **毎朝の無料3色シグナル登録**: `https://getbreakai.com/jp/` からメールアドレス1つで無料スタート\n"
        + "- **全72銘柄アンロック＆TradingView自動描画インジケーター（Pro VIP）**: 月額 $29/月（年間パス $199/年・43%割引）1つで `https://getbreakai.com/jp/` と姉妹端末 `https://truthofmarket.com/` の両方を即時解放。\n"
        + "- **法人・メディア提携窓口**: `beable9489@gmail.com`\n"
    )

    yahoo_bbs_txt = (
        f"【新NISA・老後資金の守り方メモ {as_of}】\n"
        f"新NISA枠は特定口座（20.315%）と違って損益通算ができないため、値動きの大きい半導体株ほど買う前に「資金100万円なら許容損失1.5万円まで」と株数を決めておくと安心ですね。\n"
        f"実勢レート（1ドル＝約{usd_jpy:.1f}円）連動の3秒適正株数計算機と毎朝の無料3色シグナルは GetBreakAI Japan（getbreakai.com/jp/）で確認できます。\n"
    )

    syn_res = dispatch_zero_ban_text_bundle(
        div_code="GBA",
        canonical_domain=HOST,
        canonical_url=canonical_url,
        title=title,
        summary=f"新NISA(非課税0%)・特定口座(20.315%)対応：大切な老後資金を塩漬け損から守る毎朝の3色売買シグナル日報（1ドル＝約{usd_jpy:.1f}円）",
        main_social_hook=theme["hook"],
        reply_social_link=reply_post,
        longform_markdown=note_md,
        tags=["nisa", "finance", "japan", "stocks"],
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
