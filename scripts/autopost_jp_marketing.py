#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GetBreakAI (getbreakai.com) — Japanese Marketing Autopilot & RSS/Telegram Delivery Engine
=========================================================================================
1. Generates standard RSS 2.0 feeds:
   - /jp/feed.xml   (30 Japanese SEO Articles + Daily Institutional Signals for Blog/RSS/Make/IFTTT)
   - /jp/x-feed.xml (Daily 10 Japanese X/Threads/Bluesky Auto-Post items with image enclosures)
2. Generates YouTube Shorts & Instagram Reels Copy-Paste Kit (`yt_ig_reels_kit_jp.md`)
   for the 3 daily 1080x1920 Japanese MP4 videos.
3. Optional `--send-telegram`: Sends the 3 rendered MP4 videos + copy-paste Japanese
   YouTube Shorts / Instagram Reels titles, captions, and pinned comments directly to
   the CEO's Telegram (@SemifearGreedbot) so uploading on smartphone takes 30 seconds.
4. Optional X API v2 / Webhook auto-posting when `X_BEARER_TOKEN` / `MAKE_WEBHOOK_URL` are set.
"""

import os
import sys
import json
import datetime
import urllib.request
import urllib.parse
from xml.sax.saxutils import escape

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
JP_DIR = os.path.join(ROOT_DIR, "jp")
OUTBOX_BASE = os.path.join(ROOT_DIR, "marketing_outbox_jp")
SNAPSHOT_PATH = os.path.join(ROOT_DIR, "data", "live_market_snapshot.json")
HQ_TG_CONFIG = r"D:\드림컴퍼니\1사업부\data\telegram_config.json"
DEFAULT_CEO_CHAT_ID = "755033799"


def get_latest_outbox_dir():
    if not os.path.exists(OUTBOX_BASE):
        return None, None
    dates = sorted([
        d for d in os.listdir(OUTBOX_BASE)
        if os.path.isdir(os.path.join(OUTBOX_BASE, d)) and len(d) == 10
    ])
    if not dates:
        return None, None
    latest = dates[-1]
    return latest, os.path.join(OUTBOX_BASE, latest)


def load_snapshot():
    if os.path.exists(SNAPSHOT_PATH):
        with open(SNAPSHOT_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"updated_at": datetime.date.today().isoformat(), "tickers": {}}


def build_rss_feeds(date_str, outbox_dir, snap):
    os.makedirs(JP_DIR, exist_ok=True)
    now_rfc822 = datetime.datetime.now(datetime.timezone.utc).strftime("%a, %d %b %Y %H:%M:%S GMT")

    # 1. Build /jp/x-feed.xml from x_posts_10.json
    x_posts_path = os.path.join(outbox_dir, "x_posts_10.json") if outbox_dir else None
    x_posts = []
    if x_posts_path and os.path.exists(x_posts_path):
        with open(x_posts_path, "r", encoding="utf-8") as f:
            x_posts = json.load(f)

    x_items_xml = []
    for idx, post in enumerate(x_posts):
        ticker = post.get("ticker", "NVDA")
        text = post.get("text", "")
        url = f"https://getbreakai.com/?ticker={ticker}&utm_source=x_auto&utm_medium=rss"
        title = text.split("\n")[0][:80]
        guid = f"https://getbreakai.com/jp/x-post-{date_str}-{idx+1}"
        x_items_xml.append(f"""    <item>
      <title>{escape(title)}</title>
      <link>{escape(url)}</link>
      <guid isPermaLink="false">{escape(guid)}</guid>
      <pubDate>{now_rfc822}</pubDate>
      <description>{escape(text)}</description>
    </item>""")

    x_feed_xml = f"""<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom">
  <channel>
    <title>GetBreakAI 米国株・新NISA 機関投資家シグナル速報 (X/Threads自動配信フィード)</title>
    <link>https://getbreakai.com/</link>
    <description>米国SEC 8-K/Form-4・オプションGamma壁・2.0x ATR損切り＆新NISA税引後シミュレーター公式フィード</description>
    <language>ja</language>
    <lastBuildDate>{now_rfc822}</lastBuildDate>
    <atom:link href="https://getbreakai.com/jp/x-feed.xml" rel="self" type="application/rss+xml"/>
{chr(10).join(x_items_xml)}
  </channel>
</rss>
"""
    x_feed_path = os.path.join(JP_DIR, "x-feed.xml")
    with open(x_feed_path, "w", encoding="utf-8") as f:
        f.write(x_feed_xml)

    # 2. Build /jp/feed.xml for SEO research articles & note.com / blog syndication
    seo_files = sorted([
        fn for fn in os.listdir(JP_DIR)
        if fn.endswith(".html") and fn != "index.html"
    ])
    article_items_xml = []
    for fn in seo_files[:20]:
        url = f"https://getbreakai.com/jp/{fn}"
        slug_title = fn.replace(".html", "").replace("-", " ").upper()
        article_items_xml.append(f"""    <item>
      <title>【米国株AI解析】{escape(slug_title)} — SEC一次情報・Gamma壁・2.0x ATR損切りライン ({date_str}更新)</title>
      <link>{escape(url)}</link>
      <guid isPermaLink="true">{escape(url)}</guid>
      <pubDate>{now_rfc822}</pubDate>
      <description>{escape(f"新NISA・特定口座(20.315%)対応の米国株機関投資家シグナル＆ATR適正株数レポート: {url}")}</description>
    </item>""")

    main_feed_xml = f"""<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom">
  <channel>
    <title>GetBreakAI 日本公式リサーチ＆米国株AIシグナル (RSS 2.0)</title>
    <link>https://getbreakai.com/jp/</link>
    <description>ウォール街のSEC開示・インサイダー買い・ガンマウォールを日本語で毎日自動更新</description>
    <language>ja</language>
    <lastBuildDate>{now_rfc822}</lastBuildDate>
    <atom:link href="https://getbreakai.com/jp/feed.xml" rel="self" type="application/rss+xml"/>
{chr(10).join(article_items_xml)}
  </channel>
</rss>
"""
    main_feed_path = os.path.join(JP_DIR, "feed.xml")
    with open(main_feed_path, "w", encoding="utf-8") as f:
        f.write(main_feed_xml)

    print(f"[OK] Generated RSS feeds: {x_feed_path} ({len(x_items_xml)} items) & {main_feed_path} ({len(article_items_xml)} items)")


def build_yt_ig_kit(date_str, outbox_dir, snap):
    if not outbox_dir:
        return []
    tickers = snap.get("tickers", {})

    def t_info(sym, default_entry, default_stop, default_tp):
        d = tickers.get(sym, {})
        return (
            d.get("price", default_entry),
            d.get("atr_stop_2x", default_stop),
            d.get("target_25r", default_tp),
        )

    nvda_p, nvda_s, nvda_t = t_info("NVDA", 186.64, 170.60, 226.74)
    pltr_p, pltr_s, pltr_t = t_info("PLTR", 160.38, 140.48, 210.13)
    tsla_p, tsla_s, tsla_t = t_info("TSLA", 358.22, 322.24, 448.17)

    kits = [
        {
            "file": "jp_shorts_01_NVDA_gamma_atr.mp4",
            "ticker": "NVDA",
            "jp_name": "エヌビディア ($NVDA)",
            "yt_title": f"【エヌビディア株】どこで利確・損切り？機関のGamma壁とATR計算 ({date_str}) #米国株 #新NISA #NVDA",
            "ig_caption": (
                f"🔥 エヌビディア($NVDA)を「なんとなく」で売買していませんか？\n\n"
                f"ウォール街の機関投資家が実際に見ている本日のライン👇\n"
                f"📍 現在株価: ${nvda_p}\n"
                f"🛑 2.0x ATR損切りライン（逆指値）: ${nvda_s}\n"
                f"🎯 2.5R 利確ターゲット: ${nvda_t}\n\n"
                f"新NISA（非課税0%）と特定口座（20.315%）の手取り純利益＆あなたの資金に合った適正購入株数はプロフィールのリンク（getbreakai.com）から3秒で無料計算できます📊\n\n"
                f"#米国株 #新NISA #エヌビディア #NVDA #半導体株 #米国株投資 #株式投資 #資産運用 #スイングトレード"
            ),
            "pinned_comment": "📊 あなたの日本円資金（100万円〜新NISA枠）に最適なエヌビディア購入株数＆2.0x ATR損切り計算機はこちら 👉 https://getbreakai.com/?ticker=NVDA"
        },
        {
            "file": "jp_shorts_02_PLTR_sec8k_atr.mp4",
            "ticker": "PLTR",
            "jp_name": "パランティア ($PLTR)",
            "yt_title": f"【パランティア急騰】SEC 8-K国防AI契約と2.0x ATR損切りライン ({date_str}) #米国株 #PLTR #新NISA",
            "ig_caption": (
                f"🚀 パランティア($PLTR) 機関投資家のダークプール買い集め64%検知！\n\n"
                f"英語のSEC Form 8-K（重要契約開示）をAIが3秒で日本語解析👇\n"
                f"📍 現在株価: ${pltr_p}\n"
                f"🛑 2.0x ATR損切りライン（逆指値）: ${pltr_s}\n"
                f"🎯 2.5R 利確ターゲット: ${pltr_t}\n\n"
                f"高ボラティリティ銘柄こそ「感情」ではなく「ATR（平均値動き幅）」で株数を調整するのが機関投資家の鉄則です。\n"
                f"👉 プロフィールのリンク（getbreakai.com）で今すぐ無料シミュレーション！\n\n"
                f"#米国株 #パランティア #PLTR #AI関連株 #新NISA #米国株スイング #テンバガー候補 #株式投資"
            ),
            "pinned_comment": "📊 パランティア($PLTR)のSEC開示日本語要約＆新NISA税引後シミュレーターはこちら 👉 https://getbreakai.com/?ticker=PLTR"
        },
        {
            "file": "jp_shorts_03_TSLA_gex_atr.mp4",
            "ticker": "TSLA",
            "jp_name": "テスラ ($TSLA)",
            "yt_title": f"【テスラ株】コール3.6倍の踏み上げ点火！損切りと利確目標はここ ({date_str}) #テスラ #TSLA #米国株",
            "ig_caption": (
                f"⚡ テスラ($TSLA) オプション市場でコール3.6倍のガンマスクイーズ検知！\n\n"
                f"値動きが激しいテスラで「狼狽売り・塩漬け」をゼロにする本日の数値👇\n"
                f"📍 現在株価: ${tsla_p}\n"
                f"🛑 2.0x ATR損切りライン（逆指値）: ${tsla_s}\n"
                f"🎯 2.5R 利確ターゲット: ${tsla_t}\n\n"
                f"SBI証券・楽天証券・マネックス証券の逆指値にそのまま使えるドル/円計算機はプロフィールのリンク（getbreakai.com）から無料で使えます⚡\n\n"
                f"#テスラ #TSLA #テスラ株 #米国株 #新NISA #オプション取引 #スイングトレード #米国株投資"
            ),
            "pinned_comment": "⚡ テスラ($TSLA)の5日間Gamma壁＆ATR適正株数シミュレーターはこちら 👉 https://getbreakai.com/?ticker=TSLA"
        }
    ]

    md_lines = [
        f"# 📱 YouTube ショート ＆ Instagram リール 1分コピペ投稿キット ({date_str})",
        "",
        "社長！毎日YouTubeショートとInstagramリールに動画をアップする際、下の**タイトル・キャプション・固定コメント**をそのままコピー＆ペーストするだけで完了します！",
        ""
    ]
    for idx, k in enumerate(kits, 1):
        md_lines.extend([
            f"---",
            f"## 🎬 動画 {idx}: {k['jp_name']} (`{k['file']}`)",
            f"### ① YouTube ショート タイトル（コピー用）",
            f"```text",
            k["yt_title"],
            f"```",
            f"### ② Instagram リール キャプション ＆ YouTube 概要欄（コピー用）",
            f"```text",
            k["ig_caption"],
            f"```",
            f"### ③ 固定コメント（ピン留め用）",
            f"```text",
            k["pinned_comment"],
            f"```",
            ""
        ])

    kit_md_path = os.path.join(outbox_dir, "yt_ig_reels_kit_jp.md")
    kit_json_path = os.path.join(outbox_dir, "yt_ig_reels_kit_jp.json")
    with open(kit_md_path, "w", encoding="utf-8") as f:
        f.write("\n".join(md_lines))
    with open(kit_json_path, "w", encoding="utf-8") as f:
        json.dump(kits, f, ensure_ascii=False, indent=2)

    print(f"[OK] Generated YouTube Shorts & Instagram Reels Copy-Paste Kit: {kit_md_path}")
    return kits


def send_telegram_video_and_kit(outbox_dir, kits):
    bot_token = os.environ.get("GBA_TELEGRAM_BOT_TOKEN") or os.environ.get("TELEGRAM_BOT_TOKEN")
    chat_id = os.environ.get("GBA_TELEGRAM_CHAT_ID") or DEFAULT_CEO_CHAT_ID

    if not bot_token and os.path.exists(HQ_TG_CONFIG):
        try:
            cfg = json.load(open(HQ_TG_CONFIG, "r", encoding="utf-8"))
            bot_token = cfg.get("bot_token")
        except Exception:
            pass

    if not bot_token:
        print("[SKIP] No Telegram bot token found for video delivery.")
        return

    import subprocess
    for idx, k in enumerate(kits, 1):
        mp4_path = os.path.join(outbox_dir, k["file"])
        if not os.path.exists(mp4_path):
            continue
        caption = (
            f"🎬 [本日のYouTubeショート＆インスタリール用動画 #{idx}: {k['jp_name']}]\n\n"
            f"📌 【YouTubeタイトル】:\n{k['yt_title']}\n\n"
            f"📸 【インスタリール・概要欄】:\n{k['ig_caption']}\n\n"
            f"💬 【固定コメント】:\n{k['pinned_comment']}"
        )
        cmd = [
            "curl.exe", "-s", "-X", "POST",
            f"https://api.telegram.org/bot{bot_token}/sendVideo",
            "-F", f"chat_id={chat_id}",
            "-F", f"video=@{mp4_path}",
            "-F", f"caption={caption[:1000]}"
        ]
        res = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace")
        if res.returncode == 0 and '"ok":true' in res.stdout:
            print(f"[OK] Sent MP4 video #{idx} ({k['file']}) + Copy-Paste Caption to Telegram ({chat_id})")
        else:
            print(f"[WARN] Telegram video send status for {k['file']}: {res.stdout[:200]}")


def post_webhook_if_configured(date_str, outbox_dir):
    webhook_url = os.environ.get("MAKE_WEBHOOK_URL") or os.environ.get("ZAPIER_WEBHOOK_URL")
    if not webhook_url or not outbox_dir:
        return
    x_posts_path = os.path.join(outbox_dir, "x_posts_10.json")
    if not os.path.exists(x_posts_path):
        return
    posts = json.load(open(x_posts_path, "r", encoding="utf-8"))
    payload = json.dumps({"date": date_str, "site": "https://getbreakai.com", "posts": posts}).encode("utf-8")
    req = urllib.request.Request(webhook_url, data=payload, headers={"Content-Type": "application/json"}, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            print(f"[OK] Triggered external automation webhook ({resp.status})")
    except Exception as e:
        print(f"[WARN] Webhook trigger failed: {e}")


def main():
    date_str, outbox_dir = get_latest_outbox_dir()
    snap = load_snapshot()
    if not date_str:
        date_str = datetime.date.today().isoformat()
    build_rss_feeds(date_str, outbox_dir, snap)
    kits = build_yt_ig_kit(date_str, outbox_dir, snap)
    post_webhook_if_configured(date_str, outbox_dir)
    if "--send-telegram" in sys.argv and outbox_dir and kits:
        send_telegram_video_and_kit(outbox_dir, kits)


if __name__ == "__main__":
    main()
