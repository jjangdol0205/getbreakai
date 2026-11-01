#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
daily_6am_shorts_sender.py — Daily 6:00 AM KST Telegram Video + YouTube/Instagram Copy Kit Dispatcher
====================================================================================================
Sends 1 mastered US Viral Short MP4 per day (EP01 -> EP10) to Telegram (`@RigjtsideAlphabot`) along with
1-tap mobile copy blocks (`<code>...</code>`) for:
  1) YouTube Shorts Title
  2) YouTube Shorts Description & Pinned Comment
  3) Instagram Reels Caption & Pinned Comment

Usage:
  python daily_6am_shorts_sender.py --next          # Sends next queued episode (1..10) and advances pointer
  python daily_6am_shorts_sender.py --ep 1          # Sends specific episode (1..10)
"""
import argparse
import json
import pathlib
import sys
from datetime import datetime, timezone
from typing import Any, Dict, List

import httpx

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

BASE_DIR = pathlib.Path(__file__).resolve().parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from backend.app.services.telegram_service import telegram_service

VIDEOS_DIR = BASE_DIR / "viral_shorts_10_output"
STATE_FILE = BASE_DIR / "data" / "daily_shorts_state.json"

EPISODE_COPY_KIT: List[Dict[str, Any]] = [
    {
        "num": 1,
        "id": "EP01",
        "topic_kr": "폭락장 물타기(-50% Dip Trap) vs 월가 우측 돌파(Right-Side Ignition)",
        "yt_title": 'Why "Buying the Dip" Destroys 90% of Retail Accounts (The Right-Side Rule) 📉📈 #stocks #trading #usstocks',
        "yt_desc": (
            "You bought a stock down 50% thinking it was cheap—and somehow it dropped another 40%.\n"
            "Wall Street quants never catch falling knives on the left side of a crash. They wait for Right-Side Ignition above the 60-day moving average (MA60) with institutional volume.\n\n"
            "🖥️ Scan 72+ US Tech & Growth Stocks Live: https://getbreakai.com\n"
            "🤖 Free Real-Time Telegram Breakout Bot: https://t.me/RigjtsideAlphabot\n\n"
            "#usstocks #stockmarket #swingtrading #daytrading #nvda #tsla #celh #quanttrading #technicalanalysis #wallstreet"
        ),
        "yt_pin": (
            "📌 Bagholding a crashed stock right now? Enter your ticker & avg price into our FREE Position Doctor (3s Stop-Loss & 2x Target diagnosis) 👉 https://getbreakai.com | Free Telegram Bot: https://t.me/RigjtsideAlphabot"
        ),
        "ig_caption": (
            'Comment "ALPHA" and I’ll DM you instant access to our Live US Quant Terminal & Free Telegram Breakout Bot 👇\n\n'
            "Stop catching falling knives on the left side of a crash.\n"
            "Our 26-year Right-Side Quant Engine tracks 72+ US market leaders in real time:\n\n"
            "🔥 IGNITION: Institutional breakout confirmed above 60-day trendline (MA60)\n"
            "⚠️ TRAP: Price below MA60 — high bull-trap risk\n"
            "🩺 POSITION DOCTOR: Enter your avg cost for exact -9% Stop-Loss & +100% Target levels in 3 seconds.\n\n"
            '💬 Drop "ALPHA" in the comments below and check your DMs!\n\n'
            "#usstocks #stockmarket #daytrading #swingtrading #nvda #tsla #pltr #quanttrading #tradingstrategy #wallstreet"
        ),
    },
    {
        "num": 2,
        "id": "EP02",
        "topic_kr": "비자발적 장기투자(Bagholding)를 막아주는 -9% 기계적 칼손절 법칙",
        "yt_title": "How One -9% Rule Saves You From a -70% Bagholder Wipeout 🛑📉 #tradingstrategy #stocks #investing",
        "yt_desc": (
            "Every massive -50% portfolio wipeout starts as a small dip that you refused to sell.\n"
            "Institutional quants survive every bear market using one ruthless rule: an automatic -9.0% hard stop loss.\n\n"
            "🩺 Diagnose Your Stock in 3 Seconds (Position Doctor): https://getbreakai.com\n"
            "🤖 Free Telegram Quant Alert Bot: https://t.me/RigjtsideAlphabot\n\n"
            "#stockmarket #usstocks #riskmanagement #swingtrading #daytrading #optionsflow #nvda #tsla #quanttrading"
        ),
        "yt_pin": (
            "🛑 Stuck bagholding a losing US stock? Type your ticker & entry price into our free Position Doctor at https://getbreakai.com to see your exact mathematical -9% Stop & +100% Target!"
        ),
        "ig_caption": (
            'Comment "ALPHA" and I’ll DM you our free 3-second Position Doctor & Telegram Alert Bot 👇\n\n'
            "Every -70% bagholder nightmare started as a small dip you refused to cut.\n"
            "Here is how our institutional Position Doctor protects your capital:\n\n"
            "🛑 RULE 1 (-9% Hard Stop): Automatic exit before a dip becomes a crash\n"
            "⏳ RULE 2 (55-Day Time Stop): Cut dead money that fails to gain +8%\n"
            "💰 RULE 3 (+100% TP1): Sell 50% at 2x to ride a risk-free runner\n\n"
            '💬 Comment "ALPHA" below to test your portfolio in 3 seconds!\n\n'
            "#usstocks #stockmarket #swingtrading #daytrading #riskmanagement #nvda #tsla #wallstreet #quanttrading"
        ),
    },
    {
        "num": 3,
        "id": "EP03",
        "topic_kr": "계좌 복리를 망치는 '횡보장 기회비용' — 월가의 55일 시간 손절(Time Stop) 법칙",
        "yt_title": "The 55-Day 'Dead Money' Rule Wall Street Quants Live By ⏱️📈 #stocks #swingtrading #wallstreet",
        "yt_desc": (
            "The biggest hidden killer of your trading account isn't a crash—it's dead money.\n"
            "When you hold a sideways stock for 6 months, you miss every real institutional breakout. Our 26-year quant engine enforces a strict 55-Day Time Stop.\n\n"
            "🖥️ Live 72-Stock Breakout Scanner & Position Doctor: https://getbreakai.com\n"
            "🤖 Free Telegram Breakout Bot: https://t.me/RigjtsideAlphabot\n\n"
            "#usstocks #stockmarket #tradingstrategy #quanttrading #daytrading #nvda #tsla #pltr #momentumtrading"
        ),
        "yt_pin": (
            "⏱️ Holding a stock that refuses to move? Run your ticker + days held through our free Position Doctor at https://getbreakai.com to see if it triggered the 55-Day Dead Money Exit!"
        ),
        "ig_caption": (
            'Comment "ALPHA" and I’ll send you direct access to our Live US Quant Terminal & Telegram Bot 👇\n\n'
            "Crashes aren't the only thing killing your returns—Dead Money is.\n"
            "If a stock fails to gain +8% within 55 trading days, institutional quants rotate out immediately into active Right-Side Ignitions.\n\n"
            '💬 Drop "ALPHA" in the comments to check which 5 US stocks are in the live Ignition Zone today!\n\n'
            "#usstocks #stockmarket #swingtrading #daytrading #quanttrading #tradingtips #nvda #tsla #wallstreet"
        ),
    },
    {
        "num": 4,
        "id": "EP04",
        "topic_kr": "반도체 공포·탐욕 지수 18 (Extreme Fear) 진입 — 80% SMH : 20% XLV 역발상 바벨",
        "yt_title": "Semiconductor Fear & Greed Just Hit 18 (Extreme Fear) — The 80/20 Secret 🚨 #semiconductors #nvda #smh",
        "yt_desc": (
            "Every time semiconductor stocks drop 20%, retail traders panic and sell at the exact bottom.\n"
            "Right now, our 7-Factor Semiconductor Fear & Greed Index plunged to 18.0 (Extreme Fear)—triggering the 80% $SMH : 20% $XLV Contrarian Barbell.\n\n"
            "🧭 Live Semi Fear & Greed Terminal: https://getbreakai.com\n"
            "🤖 Free Telegram /semi & /ignition Alerts: https://t.me/RigjtsideAlphabot\n\n"
            "#semiconductors #nvda #amd #mu #smh #soxx #etf #usstocks #stockmarket #quanttrading"
        ),
        "yt_pin": (
            "🧭 Check today's live Semiconductor 7-Factor Fear & Greed score (18.0 Extreme Fear) and exact $SMH : $XLV barbell weights at https://getbreakai.com | Free Telegram Bot: https://t.me/RigjtsideAlphabot"
        ),
        "ig_caption": (
            'Comment "ALPHA" to get our live Semiconductor Fear & Greed Index + Telegram Alert Bot 👇\n\n'
            "While 90% of retail traders panic during chip pullbacks, our 7-Factor Semiconductor Fear & Greed Index just hit 18.0 (EXTREME FEAR).\n\n"
            "⚡ Contrarian Barbell Directive: Shift from 70/30 to 80% $SMH (Semiconductors) : 20% $XLV (Healthcare Vault)\n"
            "📈 26-Year Backtest: 23.1% CAGR with significantly lower drawdown than holding 100% tech.\n\n"
            '💬 Comment "ALPHA" below and check your DMs for the live dashboard!\n\n'
            "#nvda #semiconductors #smh #soxx #amd #usstocks #stockmarket #etfinvesting #quanttrading #wallstreet"
        ),
    },
    {
        "num": 5,
        "id": "EP05",
        "topic_kr": "고점 대비 -71% 폭락한 $CELH, 데드캣 바운스인가 진짜 기관 수급 돌파인가?",
        "yt_title": "$CELH Crashed 71% — Bull Trap or Institutional Right-Side Breakout? 🔥📈 #celh #stocks #swingtrading",
        "yt_desc": (
            "When a growth stock like Celsius ($CELH) crashes 71% from its high, how do you know if the bounce is a fakeout or a real institutional turnaround?\n"
            "We check 4 mathematical conditions: C1 Deep DD Washout, C2 Off 52W Low, C3 MA20/MA60 Reclamation, and C4 1.95x Volume Surge.\n\n"
            "📑 Read the Full $CELH Institutional Quant Brief: https://getbreakai.com\n"
            "🤖 Free Telegram Bot (/stock CELH): https://t.me/RigjtsideAlphabot\n\n"
            "#celh #usstocks #growthstocks #stockmarket #breakoutstocks #swingtrading #quanttrading #technicalanalysis"
        ),
        "yt_pin": (
            "📈 See the exact $CELH Entry Trigger ($27.93), -9% Hard Stop ($25.42), and +100% Target ($55.86) on our live terminal 👉 https://getbreakai.com"
        ),
        "ig_caption": (
            'Comment "ALPHA" and I’ll DM you the full $CELH Institutional Research Brief & Live Scanner 👇\n\n'
            "How do you separate a dead-cat bounce from a real institutional turnaround?\n"
            "Look at $CELH on our Right-Side Engine:\n"
            "✅ C1: -71.6% deep washout complete\n"
            "✅ C2: +31.4% off 52-week low\n"
            "✅ C3: Reclaimed 20-day & 60-day moving averages\n"
            "✅ C4: 1.95x 10-day institutional volume surge\n\n"
            '💬 Comment "ALPHA" below to unlock all 5 active Ignition stocks!\n\n'
            "#celh #usstocks #growthstocks #swingtrading #daytrading #stockscanner #quanttrading #wallstreet"
        ),
    },
    {
        "num": 6,
        "id": "EP06",
        "topic_kr": "$TSLA · $NVDA 급등 직전에 개인투자자만 털리는 이유 (기관 Entry Trigger)",
        "yt_title": "Why $TSLA & $NVDA Always Shake You Out Right Before Ripping 20% ⚡📈 #tsla #nvda #daytrading",
        "yt_desc": (
            "Ever feel like market makers wait for you to sell $TSLA or $NVDA before ripping it 20% higher?\n"
            "That happens because retail traders buy inside the chop zone before price clears the institutional 60-day Entry Trigger (TRG).\n\n"
            "🎯 Check Exact TRG Levels for 72+ US Stocks: https://getbreakai.com\n"
            "🤖 Free Telegram Bot (/stock TSLA, /stock NVDA): https://t.me/RigjtsideAlphabot\n\n"
            "#tsla #nvda #usstocks #stockmarket #daytrading #swingtrading #breakouttrading #quanttrading"
        ),
        "yt_pin": (
            "🎯 Stop getting shaken out in the chop zone! Check live Entry Trigger (TRG) prices for $TSLA, $NVDA, $AMD, and 72 US leaders 👉 https://getbreakai.com"
        ),
        "ig_caption": (
            'Comment "ALPHA" to get instant Telegram alerts when $TSLA, $NVDA & 72 US leaders hit their Entry Trigger 👇\n\n'
            "Why do you always get shaken out right before the real move?\n"
            "Because buying below the 60-day moving average puts you inside institutional chop.\n"
            "Our terminal calculates the exact dollar Entry Trigger (TRG) so you only strike when momentum is confirmed.\n\n"
            '💬 Drop "ALPHA" in the comments and check your DMs!\n\n'
            "#tsla #nvda #usstocks #stockmarket #daytrading #swingtrading #optionsflow #quanttrading #wallstreet"
        ),
    },
    {
        "num": 7,
        "id": "EP07",
        "topic_kr": "+100% 수익(TP1)에서 원금 100% 회수하고 '무위험 공짜 주식'으로 끝까지 먹는 법",
        "yt_title": "The +100% 'Free-Ride' Rule: How Quants Trade With Zero Principal Risk 💰🚀 #trading #stocks #investing",
        "yt_desc": (
            "The worst feeling in trading is watching an +80% gain round-trip all the way back into a loss.\n"
            "Wall Street quants prevent this with Rule 3: at +100% (TP1), sell 50% to recover 100% of your initial capital, and trail the rest on the 60-day moving average.\n\n"
            "🖥️ Calculate Your Exact 2x Target & Stop Levels: https://getbreakai.com\n"
            "🤖 Free Telegram Quant Bot: https://t.me/RigjtsideAlphabot\n\n"
            "#usstocks #stockmarket #swingtrading #wealthbuilding #quanttrading #tradingpsychology #wallstreet"
        ),
        "yt_pin": (
            "💰 Never round-trip a winning trade again. Get exact -9% Stop & +100% TP1 levels for your portfolio at https://getbreakai.com"
        ),
        "ig_caption": (
            'Comment "ALPHA" and I’ll DM you our Position Doctor calculator & Telegram Quant Bot 👇\n\n'
            "How do institutional traders ride massive multi-baggers without stress?\n"
            "The +100% Free-Ride Rule (TP1):\n"
            "1️⃣ Enter on Right-Side Ignition with a strict -9% Hard Stop\n"
            "2️⃣ At +100% gain (2x), sell exactly 50% of your shares\n"
            "3️⃣ Your original cash is now 100% back in your pocket—the remaining shares are a mathematically risk-free runner.\n\n"
            '💬 Comment "ALPHA" below for instant access to the live terminal!\n\n'
            "#usstocks #stockmarket #swingtrading #daytrading #tradingpsychology #quanttrading #wallstreet"
        ),
    },
    {
        "num": 8,
        "id": "EP08",
        "topic_kr": "미국주식 126종목 26년 백테스트(2000~2026) — 나스닥 14배 vs 우측 돌파 349배의 비밀",
        "yt_title": "We Backtested 126 US Stocks Over 26 Years — Here’s What Crushed Wall Street 📊🏆 #backtest #quant #stocks",
        "yt_desc": (
            "We tested 126 US stocks across 26.78 years (2000 Dot-Com Crash, 2008 GFC, 2020 COVID, 2022 Bear Market).\n"
            "Blindly buying 52-week lows suffered -71% drawdowns. Waiting for Right-Side PW-RSI Ignition compounded at 24.48% CAGR (349.3x vs QQQ 14.3x).\n\n"
            "📊 Explore the Full 26-Year Backtest & Live Scanner: https://getbreakai.com\n"
            "🤖 Free Telegram Quant Bot: https://t.me/RigjtsideAlphabot\n\n"
            "#quanttrading #backtesting #usstocks #stockmarket #algotrading #qqq #spy #swingtrading #wallstreet"
        ),
        "yt_pin": (
            "📊 Verify every year of our 26-year backtest (2000–2026) and see today's 5 Ignition stocks live at https://getbreakai.com"
        ),
        "ig_caption": (
            'Comment "ALPHA" to explore our 26-Year Backtest & Live 72-Stock Scanner 👇\n\n'
            "Numbers don't lie. Across 26.78 years and 126 US stocks (including 2000, 2008, and 2022):\n"
            "📉 Naive 52-Week Low Dip Buying: Crushed by -71% max drawdowns\n"
            "📈 Right-Side PW-RSI Engine: 24.48% CAGR (349.3x cumulative return vs QQQ 14.3x)\n\n"
            '💬 Drop "ALPHA" in the comments and I’ll DM you the live terminal link!\n\n'
            "#quanttrading #algotrading #usstocks #stockmarket #swingtrading #investing #qqq #nvda #wallstreet"
        ),
    },
    {
        "num": 9,
        "id": "EP09",
        "topic_kr": "가짜 돌파(Bull Trap)에 속지 않는 단 하나의 지표 — 10일 거래량 1.8배 폭발(Vol Surge)",
        "yt_title": "Fake Breakout vs. Real Institutional Buying: The 1.8x Volume Tell 🔍📊 #technicalanalysis #trading #stocks",
        "yt_desc": (
            "90% of retail breakout trades fail because traders only watch price candles and ignore institutional volume.\n"
            "When price crosses the 60-day moving average on weak volume, it's a Bull Trap. True institutional accumulation surges 1.5x–2.0x above 10-day average volume.\n\n"
            "🔍 Scan Live Institutional Volume Surges: https://getbreakai.com\n"
            "🤖 Free Telegram Breakout Bot: https://t.me/RigjtsideAlphabot\n\n"
            "#volumeanalysis #technicalanalysis #breakouttrading #usstocks #stockmarket #daytrading #swingtrading #quant"
        ),
        "yt_pin": (
            "🔍 Filter out low-volume bull traps automatically with our live 72-stock institutional scanner 👉 https://getbreakai.com"
        ),
        "ig_caption": (
            'Comment "ALPHA" and I’ll DM you our Live Institutional Volume & Breakout Scanner 👇\n\n'
            "Price can be manipulated on low volume—institutional volume surge cannot hide.\n"
            "Before entering any breakout, verify:\n"
            "1️⃣ Price reclaimed both MA20 and MA60\n"
            "2️⃣ 10-Day Volume Surge is spiking 1.5x to 2.0x+ above normal\n\n"
            '💬 Comment "ALPHA" below to get the live scanner & Telegram bot in your DMs!\n\n'
            "#technicalanalysis #daytrading #swingtrading #usstocks #stockmarket #priceaction #quanttrading #wallstreet"
        ),
    },
    {
        "num": 10,
        "id": "EP10",
        "topic_kr": "매일 밤 9시 30분 미국장 개장 전 3초 포지션 닥터(Position Doctor) 점검 루틴",
        "yt_title": "Run This 3-Second Quant Check Before the 9:30 AM Market Open 🔔📈 #usstocks #daytrading #stockmarket",
        "yt_desc": (
            "Before the US market opens at 9:30 AM EST tomorrow, stop trading blind on social media hype.\n"
            "In 3 seconds, check whether any US stock is in an institutional Right-Side Ignition or a dangerous Trap—and audit your open positions with Position Doctor.\n\n"
            "🖥️ Open Live US Quant Terminal: https://getbreakai.com\n"
            "🤖 Free Morning Briefing Telegram Bot: https://t.me/RigjtsideAlphabot\n\n"
            "#premarket #usstocks #stockmarket #daytrading #swingtrading #nvda #tsla #pltr #quanttrading #wallstreet"
        ),
        "yt_pin": (
            "🔔 Bookmark https://getbreakai.com and join our free Telegram Bot (https://t.me/RigjtsideAlphabot) for daily pre-market Ignition & Semi Fear & Greed briefings!"
        ),
        "ig_caption": (
            'Comment "ALPHA" and I’ll DM you our Pre-Market Quant Terminal + Free Telegram Alert Bot 👇\n\n'
            "Your 30-second pre-market checklist before the 9:30 AM EST opening bell:\n"
            "✅ Check /ignition on Telegram for today's top 5 Right-Side breakouts\n"
            "✅ Check /semi for Semiconductor Fear & Greed barbell weights\n"
            "✅ Run your open positions through Position Doctor for exact -9% Stop & 2x Target levels\n\n"
            '💬 Drop "ALPHA" in the comments right now and check your DMs!\n\n'
            "#premarket #usstocks #stockmarket #daytrading #swingtrading #nvda #tsla #quanttrading #wallstreet"
        ),
    },
]


def load_daily_state() -> Dict[str, Any]:
    if STATE_FILE.exists():
        try:
            return json.loads(STATE_FILE.read_text(encoding="utf-8"))
        except Exception:
            pass
    return {"next_ep": 1, "last_sent_date": "", "history": []}


def save_daily_state(st: Dict[str, Any]) -> None:
    STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
    STATE_FILE.write_text(json.dumps(st, ensure_ascii=False, indent=2), encoding="utf-8")


def send_episode_package_to_telegram(ep_num: int, advance_state: bool = False) -> bool:
    ep_idx = ((ep_num - 1) % 10)
    kit = EPISODE_COPY_KIT[ep_idx]
    real_num = kit["num"]
    mp4_path = VIDEOS_DIR / f"EP{real_num:02d}_US_Viral_Shorts.mp4"

    token = telegram_service._resolve_token()
    chat_id = telegram_service._resolve_chat_id() or "755033799"
    base = f"https://api.telegram.org/bot{token}"

    timeout_cfg = httpx.Timeout(connect=20.0, read=240.0, write=240.0, pool=30.0)
    with httpx.Client(timeout=timeout_cfg) as client:
        # 1. Upload the mastered MP4 video so the user can save it directly on their phone
        if mp4_path.exists():
            upload_path = mp4_path
            if mp4_path.stat().st_size > 8 * 1024 * 1024:
                try:
                    import subprocess
                    import imageio_ffmpeg
                    slim_path = VIDEOS_DIR / f"EP{real_num:02d}_TG_Fast.mp4"
                    if not slim_path.exists():
                        subprocess.run(
                            [
                                imageio_ffmpeg.get_ffmpeg_exe(),
                                "-y",
                                "-i",
                                str(mp4_path),
                                "-c:v",
                                "libx264",
                                "-preset",
                                "veryfast",
                                "-crf",
                                "25",
                                "-c:a",
                                "copy",
                                "-movflags",
                                "+faststart",
                                str(slim_path),
                            ],
                            stdout=subprocess.DEVNULL,
                            stderr=subprocess.DEVNULL,
                            check=False,
                        )
                    if slim_path.exists() and slim_path.stat().st_size > 100_000:
                        upload_path = slim_path
                except Exception:
                    upload_path = mp4_path

            video_bytes = upload_path.read_bytes()
            caption = (
                f"🎬 <b>[Day {real_num}/10 모닝 쇼츠·릴스 배달] {kit['id']} 완성본 영상</b>\n"
                f"📌 주제: {kit['topic_kr']}\n\n"
                "👆 <b>영상을 터치한 뒤 우측 상단 [⋮] → [갤러리에 저장(비디오 저장)]</b>을 눌러 핸드폰에 저장하세요!\n"
                "👇 바로 아래 메시지의 파란 글씨 박스를 터치하면 유튜브 제목·설명·인스타 캡션이 1초 만에 복사됩니다."
            )
            try:
                r_vid = client.post(
                    f"{base}/sendVideo",
                    data={
                        "chat_id": chat_id,
                        "caption": caption,
                        "parse_mode": "HTML",
                        "supports_streaming": "true",
                    },
                    files={"video": (mp4_path.name, video_bytes, "video/mp4")},
                )
                print(f"[DailyShorts] sendVideo EP{real_num:02d}: HTTP {r_vid.status_code}")
            except Exception as vid_exc:
                print(f"[DailyShorts] sendVideo warning: {vid_exc}")

        # 2. Send 1-Tap Copy YouTube Title, Description, Pinned Comment & Instagram Caption
        import html
        yt_title_esc = html.escape(kit["yt_title"])
        yt_desc_esc = html.escape(kit["yt_desc"])
        yt_pin_esc = html.escape(kit["yt_pin"])
        ig_cap_esc = html.escape(kit["ig_caption"])

        copy_msg = (
            f"📋 <b>[{kit['id']} 업로드용 1클릭 복사 패키지] ({real_num}/10편)</b>\n"
            "━━━━━━━━━━━━━━━━━━━━\n"
            "💡 <i>아래 박스 글씨를 핸드폰에서 <b>한 번만 톡 터치하면</b> 자동 복사됩니다!</i>\n\n"
            "▶️ <b>1. 유튜브 쇼츠 제목 (Title 👇)</b>\n"
            f"<code>{yt_title_esc}</code>\n\n"
            "📝 <b>2. 유튜브 쇼츠 설명 (Description 👇)</b>\n"
            f"<code>{yt_desc_esc}</code>\n\n"
            "📌 <b>3. 유튜브 쇼츠 고정 댓글 (Pinned Comment 👇)</b>\n"
            f"<code>{yt_pin_esc}</code>\n\n"
            "━━━━━━━━━━━━━━━━━━━━\n"
            "📸 <b>4. 인스타그램 릴스 본문 캡션 (Reels Caption 👇)</b>\n"
            f"<code>{ig_cap_esc}</code>\n\n"
            "📌 <b>5. 인스타 릴스 내 고정 댓글 (Pinned Comment 👇)</b>\n"
            '<code>📌 Comment "ALPHA" right here and my bot will instantly DM you the direct link to the Live Terminal (getbreakai.com) + our Free Telegram Alert Bot! 🚀</code>'
        )
        r_txt = client.post(
            f"{base}/sendMessage",
            json={
                "chat_id": chat_id,
                "text": copy_msg,
                "parse_mode": "HTML",
                "disable_web_page_preview": True,
            },
        )
        ok = r_txt.status_code == 200 and r_txt.json().get("ok", False)
        print(f"[DailyShorts] sendMessage EP{real_num:02d}: ok={ok}")

    if advance_state and ok:
        st = load_daily_state()
        today_str = datetime.now().strftime("%Y-%m-%d")
        st["last_sent_date"] = today_str
        st["next_ep"] = (real_num % 10) + 1
        st.setdefault("history", []).append(
            {"ep": real_num, "sent_at": datetime.now(timezone.utc).isoformat()}
        )
        save_daily_state(st)

    return ok


def main() -> int:
    parser = argparse.ArgumentParser(description="Daily 6:00 AM Shorts & Reels Telegram Sender")
    parser.add_argument("--ep", type=int, default=0, help="Send specific episode (1..10)")
    parser.add_argument("--next", action="store_true", help="Send next queued episode and advance state")
    args = parser.parse_args()

    if args.ep > 0:
        ok = send_episode_package_to_telegram(args.ep, advance_state=False)
        return 0 if ok else 1

    st = load_daily_state()
    next_ep = int(st.get("next_ep", 1))
    ok = send_episode_package_to_telegram(next_ep, advance_state=True)
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
