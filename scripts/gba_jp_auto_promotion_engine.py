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
        "title_prefix": "新NISA成長投資枠（SMH × XLV）＋個人向け国債（変動10年）2本柱・老後資産配分設計",
        "hook": "新NISA成長投資枠の現物1倍2本柱（SMH × XLV）と個人向け国債（変動10年）の初期比率を4ステップで無料試算できます。\n\n金融庁ルールに準拠した静かな2本柱設計で大切な老後資金を守りましょう。 #新NISA #老後資金",
    },
    {
        "slug": "shin-nisa-us-stock-atr-risk-management.html",
        "title_prefix": "単一テーマ集中を防ぐ2本柱設計：夜ぐっすり眠れる新NISA資産配分の決め方",
        "hook": "老後資産運用で大切なのは単一セクターに偏らない穏やかな分散配分です。\n\n米国半導体（SMH）×米国医療（XLV）と個人向け国債（変動10年）のバランスを年2回ゆったり点検しましょう。 #新NISA #資産運用",
    },
    {
        "slug": "msft-azure-ai-copilot-sec-8k.html",
        "title_prefix": "米SEC公式決算開示（Form 8-K/10-Q）と連続増配データの落ち着いた読み方",
        "hook": "ニュースの騒音に振り回されず、企業の一次公開データとセクター全体のバランスを落ち着いて確認する習慣が長期の安心につながります。 #米国株 #新NISA",
    },
    {
        "slug": "unh-defensive-healthcare-insider-buy.html",
        "title_prefix": "ハイテク株だけに偏っていませんか？守りのヘルスケア（XLV）を添える新NISA配分",
        "hook": "成長セクター（SMH）だけでなく、ディフェンシブな医療セクター（XLV）や個人向け国債（変動10年）を組み合わせることで資産寿命は大きく安定します。 #新NISA #資産配分",
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
    return 150.0


def update_dual_llms_txt() -> str:
    today_str = datetime.datetime.now(JST).strftime("%Y-%m-%d")
    excluded_names = {
        "index.html", "confirmation.html", "terms.html", "privacy.html", "refund.html", "contact.html",
        "soxl-smh-semiconductor-timing.html", "mstr-bitcoin-volatility-atr-sizing.html",
        "nvda-sec-gamma-atr-analysis.html", "tsla-gamma-wall-swing-trade.html",
        "amd-mi350-gamma-squeeze-target.html", "arm-royalty-expansion-gamma-wall.html",
        "options-gamma-squeeze-gex-guide.html", "fomc-cpi-iv-crush-strategy.html",
        "tradingview-pine-script-v5-atr-guide.html", "us-stock-stop-loss-2percent-rule.html",
        "dark-pool-whale-flow-reading.html",
    }
    seo_pages = sorted(
        p.name
        for p in JP_DIR.glob("*.html")
        if p.name not in excluded_names and not p.name.startswith("google")
    )

    en_lines = [
        "# GetBreakAI — Japanese 50-70s Shin-NISA SMH × XLV + JGB Asset-Allocation Platform (https://getbreakai.com/jp/)",
        "",
        f"> Updated: {today_str} | Self-Directed Public Market Data Visualization & 2-Pillar Asset-Allocation Simulator (FSA Shin-NISA Growth Quota Eligible Spot 1x SMH × XLV + Japanese Retail Government Bonds Variable 10-Year / Tokutei Account SGOV Cushion).",
        "> Official Channels: https://www.youtube.com/@GetBreakAI | https://www.instagram.com/getbreakai/",
        "",
        "## 1. Core Japanese Calculators & Legal Pages",
        "- Main Retirement & Shin-NISA Hub: https://getbreakai.com/jp/",
        "- Root Canonical Mirror: https://getbreakai.com/",
        "- Flagship Editorial Essay: https://getbreakai.com/jp/nisa-quiet-barbell-essay.html",
        "- Daily Public Market Data Report: https://getbreakai.com/jp/daily-nisa-quant-report.html",
        "- Terms of Service: https://getbreakai.com/jp/terms.html",
        "- Privacy Policy: https://getbreakai.com/jp/privacy.html",
        "- 14-Day Refund Policy: https://getbreakai.com/jp/refund.html",
        "- Japanese Research RSS Feed: https://getbreakai.com/jp/feed.xml",
        "",
        "## 2. Featured Japanese Public Market Data & Shin-NISA Guides (/jp/)",
    ]
    for fn in seo_pages[:31]:
        en_lines.append(f"- https://getbreakai.com/jp/{fn}")
    (ROOT_DIR / "llms.txt").write_text("\n".join(en_lines) + "\n", encoding="utf-8")

    jp_lines = [
        "# GetBreakAI Japan (https://getbreakai.com/jp/)",
        "",
        "> 日本の50代〜70代個人投資家・新NISA運用層のための公開市場データ可視化および資産配分計算ソフトウェア（Self-Directed Educational Calculator Software）。金融庁規定準拠『新NISA成長投資枠 適格（米国半導体 SMH × 米国ヘルスケア XLV 現物1倍2本柱）＋ 安全資産クッション（個人向け国債 変動10年 ／ 特定口座 SGOV）』対応。",
        "> 公式チャンネル: https://www.youtube.com/@GetBreakAI | https://www.instagram.com/getbreakai/",
        f"> 最終更新日: {today_str} (JST)",
        "",
        "## 1. コア計算ツール（投資助言・売買推奨を行わない自己判断用教育計算ソフトウェア）",
        "- **4ステップ SMH × XLV ＋ 個人向け国債 比率設計シミュレーター**: 新NISA成長投資枠と安全資産クッションの初期ベース比率試算。",
        "- **代表エッセイ・朝刊データノート**: 2000〜2025年（26年間）の公開セクター検証に基づく長期資産設計コラム。",
        "- **法務・サポート窓口**: 利用規約 https://getbreakai.com/jp/terms.html / プライバシーポリシー https://getbreakai.com/jp/privacy.html / 14日間返金ポリシー https://getbreakai.com/jp/refund.html / サポート beable9489@gmail.com",
        "",
        "## 2. 主要日本語リサーチ・公開データ解説ページ一覧",
        "- 日本語メインハブ: https://getbreakai.com/jp/",
        "- 代表エッセイ: https://getbreakai.com/jp/nisa-quiet-barbell-essay.html",
        "- 本日の新NISA・公開市場データ日報: https://getbreakai.com/jp/daily-nisa-quant-report.html",
        "- 日本語RSSフィード: https://getbreakai.com/jp/feed.xml",
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
            "**新NISA（非課税0%）と個人向け国債・特定口座のやさしい使い分け**: 新NISA枠は利益がまるごと非課税（0%）になる反面、損失の損益通算ができないため、単一株集中を避け現物1倍セクターETF（SMH × XLV）で分散することが命綱になります。",
            "**年2回の穏やかな市場温度（0〜100）点検**: 半導体の成長力（SMH）とヘルスケアの下落耐性（XLV）を組み合わせ、市場の過熱・悲観に合わせて年2回だけ比率を静かに点検します。",
            f"**実勢レート（1ドル＝約{usd_jpy:.1f}円）と生活防衛クッション**: 今後2〜3年分の生活予備費は個人向け国債（変動10年）または特定口座のSGOVで別枠確保することで、夜ぐっすり眠れる運用が続けられます。",
        ],
        daily_mission=(
            "今日1分だけ、ご自身の新NISA口座が単一のハイテクテーマだけに偏っていないか、SMH × XLV ＋ 個人向け国債の基準比率と照らし合わせてみましょう。"
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
        summary=f"新NISA成長投資枠（米国半導体 SMH × 米国ヘルスケア XLV）＋個人向け国債（変動10年）／特定口座（SGOV）2本柱対応：大切な老後資金を守る朝の公開データ日報（1ドル＝約{usd_jpy:.1f}円）",
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
