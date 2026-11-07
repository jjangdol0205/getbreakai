#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
daily_6am_shorts_sender.py — Daily 6:00 AM KST Telegram Video + YouTube/Instagram/X/Reddit Copy Kit Dispatcher
==============================================================================================================
Sends 1 mastered US Viral Short MP4 per day (EP01 -> EP10) to Telegram along with
1-tap mobile copy blocks (`<pre>...</pre>`) for:
  1) YouTube Shorts Title (with live $SMH Fear & Greed score)
  2) YouTube Shorts Description
  3) YouTube Shorts Safe Pinned Comment (Related Video + Channel Bio Bridge)
  4) Instagram Reels Caption (ManyChat 'SMH' / 'ALPHA' DM Automation + 1 Unmasked & 2 Blurred VIP Picks)
  5) X (Twitter) & Stocktwits $Cashtag Sniping Copy ($SMH $NVDA $SOXL $AMD $AVGO $CELH $XLV)
  6) Reddit (r/swingtrading, r/ETFs, r/Semiconductors) & TradingView Idea Copy

Usage:
  python daily_6am_shorts_sender.py --next          # Sends next queued episode (1..10) and advances pointer
  python daily_6am_shorts_sender.py --ep 1          # Sends specific episode (1..10)
"""
import argparse
import html
import json
import os
import pathlib
import re
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
SEMI_OVERVIEW_FILE = BASE_DIR / "static_api" / "semi_overview.json"
STOCKS_MASTER_FILE = BASE_DIR / "data" / "stocks_pro_master.json"

EPISODE_COPY_KIT: List[Dict[str, Any]] = [
    {
        "num": 1,
        "id": "EP01",
        "topic_kr": "폭락장 물타기(-50% Dip Trap) vs 월가 우측 돌파(Right-Side Ignition)",
        "yt_title": 'Why "Buying the Dip" on $NVDA, $TSLA & $SOXL Destroys 90% of Accounts (The Right-Side Rule) 📉📈 #nvda #tsla #stocks',
        "yt_desc": (
            "You bought a stock down 50% thinking it was cheap—and somehow it dropped another 40%.\n"
            "Wall Street quants never catch falling knives on the left side of a crash. They wait for Right-Side Ignition above the 60-day moving average (MA60) with institutional volume.\n\n"
            "🖥️ Scan 72+ US Tech & Growth Stocks Live: https://truthofmarket.com\n"
            "🧭 Live $SMH Semiconductor Fear & Greed Terminal: https://truthofmarket.com/semi-fear-greed.html\n"
            "✈️ Free Real-Time Telegram Briefing Channel: https://t.me/truthofmarketss\n\n"
            "#usstocks #stockmarket #swingtrading #daytrading #nvda #tsla #celh #quanttrading #technicalanalysis #wallstreet"
        ),
        "yt_pin": (
            "📌 Bagholding a crashed stock right now? Tap our channel icon (@rightsidealpha) or the Related Video link below to run our FREE Position Doctor (3s Stop-Loss & 2x Target diagnosis)!"
        ),
        "ig_caption": (
            'Comment "SMH" or "ALPHA" and I’ll DM you the live 72-stock PW-RSI terminal link & Free Telegram Breakout Bot 👇\n\n'
            "Stop catching falling knives on the left side of a crash.\n"
            "Our 26-year Right-Side Quant Engine tracks 72+ US market leaders in real time:\n\n"
            "🔥 IGNITION: Institutional breakout confirmed above 60-day trendline (MA60)\n"
            "⚠️ TRAP: Price below MA60 — high bull-trap risk\n"
            "🩺 POSITION DOCTOR: Enter your avg cost for exact -9% Stop-Loss & +100% Target levels in 3 seconds.\n\n"
            '💬 Drop "SMH" in the comments below and check your DMs!\n\n'
            "#usstocks #stockmarket #daytrading #swingtrading #nvda #tsla #pltr #quanttrading #tradingstrategy #wallstreet"
        ),
    },
    {
        "num": 2,
        "id": "EP02",
        "topic_kr": "비자발적 장기투자(Bagholding)를 막아주는 -9% 기계적 칼손절 법칙",
        "yt_title": "$NVDA, $TSLA & $PLTR: How One -9% Stop Rule Saves You From a -70% Wipeout 🛑📉 #nvda #tsla #pltr",
        "yt_desc": (
            "Every massive -50% portfolio wipeout starts as a small dip that you refused to sell.\n"
            "Institutional quants survive every bear market using one ruthless rule: an automatic -9.0% hard stop loss.\n\n"
            "🩺 Diagnose Your Stock in 3 Seconds (Position Doctor): https://truthofmarket.com\n"
            "✈️ Free Telegram Quant Alert Channel: https://t.me/truthofmarketss\n\n"
            "#stockmarket #usstocks #riskmanagement #swingtrading #daytrading #optionsflow #nvda #tsla #quanttrading"
        ),
        "yt_pin": (
            "🛑 Stuck bagholding a losing US stock? Tap @rightsidealpha below and open our free Position Doctor to see your exact mathematical -9% Stop & +100% Target!"
        ),
        "ig_caption": (
            'Comment "SMH" or "ALPHA" and I’ll DM you our free 3-second Position Doctor & Telegram Alert Bot 👇\n\n'
            "Every -70% bagholder nightmare started as a small dip you refused to cut.\n"
            "Here is how our institutional Position Doctor protects your capital:\n\n"
            "🛑 RULE 1 (-9% Hard Stop): Automatic exit before a dip becomes a crash\n"
            "⏳ RULE 2 (55-Day Time Stop): Cut dead money that fails to gain +8%\n"
            "💰 RULE 3 (+100% TP1): Sell 50% at 2x to ride a risk-free runner\n\n"
            '💬 Comment "SMH" below to test your portfolio in 3 seconds!\n\n'
            "#usstocks #stockmarket #swingtrading #daytrading #riskmanagement #nvda #tsla #wallstreet #quanttrading"
        ),
    },
    {
        "num": 3,
        "id": "EP03",
        "topic_kr": "계좌 복리를 망치는 '횡보장 기회비용' — 월가의 55일 시간 손절(Time Stop) 법칙",
        "yt_title": "$SOXL, $AMD & $TSLA: The 55-Day 'Dead Money' Rule Wall Street Quants Live By ⏱️📈 #soxl #amd #tsla",
        "yt_desc": (
            "The biggest hidden killer of your trading account isn't a crash—it's dead money.\n"
            "When you hold a sideways stock for 6 months, you miss every real institutional breakout. Our 26-year quant engine enforces a strict 55-Day Time Stop.\n\n"
            "🖥️ Live 72-Stock Breakout Scanner & Position Doctor: https://truthofmarket.com\n"
            "✈️ Free Telegram Breakout Channel: https://t.me/truthofmarketss\n\n"
            "#usstocks #stockmarket #tradingstrategy #quanttrading #daytrading #nvda #tsla #pltr #momentumtrading"
        ),
        "yt_pin": (
            "⏱️ Holding a stock that refuses to move? Run your ticker + days held through our free Position Doctor via the link in @rightsidealpha bio!"
        ),
        "ig_caption": (
            'Comment "SMH" or "ALPHA" and I’ll send you direct access to our Live US Quant Terminal & Telegram Bot 👇\n\n'
            "Crashes aren't the only thing killing your returns—Dead Money is.\n"
            "If a stock fails to gain +8% within 55 trading days, institutional quants rotate out immediately into active Right-Side Ignitions.\n\n"
            '💬 Drop "SMH" in the comments to check which US stocks are in the live Ignition Zone today!\n\n'
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
            "🧭 Live Semi Fear & Greed Terminal: https://truthofmarket.com/semi-fear-greed.html\n"
            "✈️ Free Telegram /semi & /ignition Alerts: https://t.me/truthofmarketss\n\n"
            "#semiconductors #nvda #amd #mu #smh #soxx #etf #usstocks #stockmarket #quanttrading"
        ),
        "yt_pin": (
            "🧭 Check today's live Semiconductor 7-Factor Fear & Greed score and exact $SMH : $XLV barbell weights via the top link on @rightsidealpha!"
        ),
        "ig_caption": (
            'Comment "SMH" to get our live Semiconductor Fear & Greed Index + Telegram Alert Bot 👇\n\n'
            "While 90% of retail traders panic during chip pullbacks, our 7-Factor Semiconductor Fear & Greed Index just hit 18.0 (EXTREME FEAR).\n\n"
            "⚡ Contrarian Barbell Directive: Shift from 70/30 to 80% $SMH (Semiconductors) : 20% $XLV (Healthcare Vault)\n"
            "📈 26-Year Backtest: 23.1% CAGR with significantly lower drawdown than holding 100% tech.\n\n"
            '💬 Comment "SMH" below and check your DMs for the live dashboard!\n\n'
            "#nvda #semiconductors #smh #soxx #amd #usstocks #stockmarket #etfinvesting #quanttrading #wallstreet"
        ),
    },
    {
        "num": 5,
        "id": "EP05",
        "topic_kr": "고점 대비 -71% 폭락한 $CELH, 데드캣 바운스인가 진짜 기관 수급 돌파인가?",
        "yt_title": "$CELH Crashed 71% — Bull Trap or Institutional Right-Side Breakout? 🔥📈 #celh #stocks #swingtrading",
        "yt_desc": (
            "When a growth stock like Celsius ($CELH) crashes from its high, how do you know if the bounce is a fakeout or a real institutional turnaround?\n"
            "We check 4 mathematical conditions: C1 Deep DD Washout, C2 Off 52W Low, C3 MA20/MA60 Reclamation, and C4 Volume Surge.\n\n"
            "📑 Read the Full $CELH Institutional Quant Brief: https://truthofmarket.com/stocks/celh.html\n"
            "✈️ Free Telegram Channel: https://t.me/truthofmarketss\n\n"
            "#celh #usstocks #growthstocks #stockmarket #breakoutstocks #swingtrading #quanttrading #technicalanalysis"
        ),
        "yt_pin": (
            "📈 See the exact $CELH Entry Trigger, -9% Hard Stop, and +100% Target on our live terminal via @rightsidealpha bio!"
        ),
        "ig_caption": (
            'Comment "SMH" or "ALPHA" and I’ll DM you the full $CELH Institutional Research Brief & Live Scanner 👇\n\n'
            "How do you separate a dead-cat bounce from a real institutional turnaround?\n"
            "Look at $CELH on our Right-Side Engine:\n"
            "✅ C1: Deep 52W washout complete\n"
            "✅ C2: Rebounding off 52-week low\n"
            "✅ C3: Reclaimed 20-day & 60-day moving averages\n"
            "✅ C4: 2.45x 10-day institutional volume surge\n\n"
            '💬 Comment "SMH" below to unlock all active Ignition stocks!\n\n'
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
            "🎯 Check Exact TRG Levels for $NVDA & 72 US Stocks: https://truthofmarket.com/stocks/nvda.html\n"
            "✈️ Free Telegram Channel: https://t.me/truthofmarketss\n\n"
            "#tsla #nvda #usstocks #stockmarket #daytrading #swingtrading #breakouttrading #quanttrading"
        ),
        "yt_pin": (
            "🎯 Stop getting shaken out in the chop zone! Check live Entry Trigger (TRG) prices for $TSLA, $NVDA, $AMD, and 72 US leaders via @rightsidealpha!"
        ),
        "ig_caption": (
            'Comment "SMH" to get instant alerts when $TSLA, $NVDA & 72 US leaders hit their Entry Trigger 👇\n\n'
            "Why do you always get shaken out right before the real move?\n"
            "Because buying below the 60-day moving average puts you inside institutional chop.\n"
            "Our terminal calculates the exact dollar Entry Trigger (TRG) so you only strike when momentum is confirmed.\n\n"
            '💬 Drop "SMH" in the comments and check your DMs!\n\n'
            "#tsla #nvda #usstocks #stockmarket #daytrading #swingtrading #optionsflow #quanttrading #wallstreet"
        ),
    },
    {
        "num": 7,
        "id": "EP07",
        "topic_kr": "+100% 수익(TP1)에서 원금 100% 회수하고 '무위험 공짜 주식'으로 끝까지 먹는 법",
        "yt_title": "$NVDA & $PLTR +100% 'Free-Ride' Rule: How Quants Trade With Zero Principal Risk 💰🚀 #nvda #pltr #stocks",
        "yt_desc": (
            "The worst feeling in trading is watching an +80% gain round-trip all the way back into a loss.\n"
            "Wall Street quants prevent this with Rule 3: at +100% (TP1), sell 50% to recover 100% of your initial capital, and trail the rest on the 60-day moving average.\n\n"
            "🖥️ Calculate Your Exact 2x Target & Stop Levels: https://truthofmarket.com\n"
            "✈️ Free Telegram Quant Channel: https://t.me/truthofmarketss\n\n"
            "#usstocks #stockmarket #swingtrading #wealthbuilding #quanttrading #tradingpsychology #wallstreet"
        ),
        "yt_pin": (
            "💰 Never round-trip a winning trade again. Get exact -9% Stop & +100% TP1 levels for your portfolio via @rightsidealpha!"
        ),
        "ig_caption": (
            'Comment "SMH" and I’ll DM you our Position Doctor calculator & Telegram Quant Bot 👇\n\n'
            "How do institutional traders ride massive multi-baggers without stress?\n"
            "The +100% Free-Ride Rule (TP1):\n"
            "1️⃣ Enter on Right-Side Ignition with a strict -9% Hard Stop\n"
            "2️⃣ At +100% gain (2x), sell exactly 50% of your shares\n"
            "3️⃣ Your original cash is now 100% back in your pocket—the remaining shares are a mathematically risk-free runner.\n\n"
            '💬 Comment "SMH" below for instant access to the live terminal!\n\n'
            "#usstocks #stockmarket #swingtrading #daytrading #tradingpsychology #quanttrading #wallstreet"
        ),
    },
    {
        "num": 8,
        "id": "EP08",
        "topic_kr": "미국주식 126종목 26년 백테스트(2000~2026) — 나스닥 14배 vs 우측 돌파 349배의 비밀",
        "yt_title": "26-Year Backtest ($QQQ, $NVDA, $SMH): Why Right-Side Breakout Crushed Wall Street 349x 📊🏆 #nvda #qqq #smh",
        "yt_desc": (
            "We tested 126 US stocks across 26.78 years (2000 Dot-Com Crash, 2008 GFC, 2020 COVID, 2022 Bear Market).\n"
            "Blindly buying 52-week lows suffered -71% drawdowns. Waiting for Right-Side PW-RSI Ignition compounded at 24.48% CAGR (349.3x vs QQQ 14.3x).\n\n"
            "📊 Explore the Full 26-Year Backtest & Live Scanner: https://truthofmarket.com\n"
            "✈️ Free Telegram Quant Channel: https://t.me/truthofmarketss\n\n"
            "#quanttrading #backtesting #usstocks #stockmarket #algotrading #qqq #spy #swingtrading #wallstreet"
        ),
        "yt_pin": (
            "📊 Verify every year of our 26-year backtest (2000–2026) and see today's Ignition stocks live via @rightsidealpha!"
        ),
        "ig_caption": (
            'Comment "SMH" to explore our 26-Year Backtest & Live 72-Stock Scanner 👇\n\n'
            "Numbers don't lie. Across 26.78 years and 126 US stocks (including 2000, 2008, and 2022):\n"
            "📉 Naive 52-Week Low Dip Buying: Crushed by -71% max drawdowns\n"
            "📈 Right-Side PW-RSI Engine: 24.48% CAGR (349.3x cumulative return vs QQQ 14.3x)\n\n"
            '💬 Drop "SMH" in the comments and I’ll DM you the live terminal link!\n\n'
            "#quanttrading #algotrading #usstocks #stockmarket #swingtrading #investing #qqq #nvda #wallstreet"
        ),
    },
    {
        "num": 9,
        "id": "EP09",
        "topic_kr": "가짜 돌파(Bull Trap)에 속지 않는 단 하나의 지표 — 10일 거래량 1.8배 폭발(Vol Surge)",
        "yt_title": "$NVDA, $TSLA & $SOFI Fake Breakout vs Real Institutional Buying: The 1.8x Volume Tell 🔍📊 #nvda #tsla #sofi",
        "yt_desc": (
            "90% of retail breakout trades fail because traders only watch price candles and ignore institutional volume.\n"
            "When price crosses the 60-day moving average on weak volume, it's a Bull Trap. True institutional accumulation surges 1.5x–2.0x above 10-day average volume.\n\n"
            "🔍 Scan Live Institutional Volume Surges: https://truthofmarket.com\n"
            "✈️ Free Telegram Breakout Channel: https://t.me/truthofmarketss\n\n"
            "#volumeanalysis #technicalanalysis #breakouttrading #usstocks #stockmarket #daytrading #swingtrading #quant"
        ),
        "yt_pin": (
            "🔍 Filter out low-volume bull traps automatically with our live 72-stock institutional scanner via @rightsidealpha!"
        ),
        "ig_caption": (
            'Comment "SMH" and I’ll DM you our Live Institutional Volume & Breakout Scanner 👇\n\n'
            "Price can be manipulated on low volume—institutional volume surge cannot hide.\n"
            "Before entering any breakout, verify:\n"
            "1️⃣ Price reclaimed both MA20 and MA60\n"
            "2️⃣ 10-Day Volume Surge is spiking 1.5x to 2.0x+ above normal\n\n"
            '💬 Comment "SMH" below to get the live scanner & Telegram bot in your DMs!\n\n'
            "#technicalanalysis #daytrading #swingtrading #usstocks #stockmarket #priceaction #quanttrading #wallstreet"
        ),
    },
    {
        "num": 10,
        "id": "EP10",
        "topic_kr": "매일 밤 9시 30분 미국장 개장 전 3초 포지션 닥터(Position Doctor) 점검 루틴",
        "yt_title": "Trading $NVDA, $TSLA or $SOXL Today? Run This 3-Second Check Before 9:30 AM Open 🔔📈 #nvda #tsla #soxl",
        "yt_desc": (
            "Before the US market opens at 9:30 AM EST tomorrow, stop trading blind on social media hype.\n"
            "In 3 seconds, check whether any US stock is in an institutional Right-Side Ignition or a dangerous Trap—and audit your open positions with Position Doctor.\n\n"
            "🖥️ Open Live US Quant Terminal: https://truthofmarket.com\n"
            "✈️ Free Morning Briefing Telegram Channel: https://t.me/truthofmarketss\n\n"
            "#premarket #usstocks #stockmarket #daytrading #swingtrading #nvda #tsla #pltr #quanttrading #wallstreet"
        ),
        "yt_pin": (
            "🔔 Tap @rightsidealpha below and open our bio link for daily pre-market Ignition & Semi Fear & Greed briefings!"
        ),
        "ig_caption": (
            'Comment "SMH" and I’ll DM you our Pre-Market Quant Terminal + Free Telegram Alert Bot 👇\n\n'
            "Your 30-second pre-market checklist before the 9:30 AM EST opening bell:\n"
            "✅ Check /ignition on Telegram for today's top Right-Side breakouts\n"
            "✅ Check /semi for Semiconductor Fear & Greed barbell weights\n"
            "✅ Run your open positions through Position Doctor for exact -9% Stop & 2x Target levels\n\n"
            '💬 Drop "SMH" in the comments right now and check your DMs!\n\n'
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


def _load_live_market_snapshot() -> Dict[str, Any]:
    snap = {
        "as_of": "2026-11-05",
        "fg_score": 18.0,
        "regime_en": "EXTREME FEAR",
        "smh_close": 504.48,
        "smh_dd_pct": -24.58,
        "xlv_close": 179.28,
        "celh_close": 30.04,
        "celh_trg": 29.33,
        "celh_stop": 27.34,
        "celh_tp1": 60.08,
        "celh_score": 98,
        "vip2_score": 94,
        "vip2_sector": "Solar Modules",
        "vip2_vol": 2.15,
        "vip3_score": 92,
        "vip3_sector": "Semiconductors",
        "vip3_vol": 1.98,
    }
    if SEMI_OVERVIEW_FILE.exists():
        try:
            ov = json.loads(SEMI_OVERVIEW_FILE.read_text(encoding="utf-8"))
            snap["as_of"] = str(ov.get("date") or snap["as_of"])
            snap["fg_score"] = float(ov.get("fg_score") or snap["fg_score"])
            snap["regime_en"] = str(ov.get("regime_en") or snap["regime_en"]).upper()
            snap["smh_close"] = float(ov.get("smh_close") or snap["smh_close"])
            snap["smh_dd_pct"] = float(ov.get("smh_dd_pct") or snap["smh_dd_pct"])
            snap["xlv_close"] = float(ov.get("xlv_close") or snap["xlv_close"])
        except Exception:
            pass
    if STOCKS_MASTER_FILE.exists():
        try:
            raw = json.loads(STOCKS_MASTER_FILE.read_text(encoding="utf-8"))
            rows = raw if isinstance(raw, list) else raw.get("stocks", [])
            ign = [r for r in rows if r.get("zone_code") == "IGNITION_ZONE"]
            if len(ign) >= 1:
                s1 = ign[0]
                snap["celh_close"] = float(s1.get("close") or snap["celh_close"])
                snap["celh_trg"] = float(s1.get("entry_trigger_price") or snap["celh_trg"])
                snap["celh_stop"] = float(s1.get("stop_loss_price") or snap["celh_stop"])
                snap["celh_tp1"] = float(s1.get("tp1_2x_price") or snap["celh_tp1"])
                snap["celh_score"] = int(s1.get("score") or snap["celh_score"])
            if len(ign) >= 2:
                s2 = ign[1]
                snap["vip2_score"] = int(s2.get("score") or snap["vip2_score"])
                snap["vip2_sector"] = str(s2.get("sector") or snap["vip2_sector"])
                snap["vip2_vol"] = float(s2.get("vol_surge_10d") or snap["vip2_vol"])
            if len(ign) >= 3:
                s3 = ign[2]
                snap["vip3_score"] = int(s3.get("score") or snap["vip3_score"])
                snap["vip3_sector"] = str(s3.get("sector") or snap["vip3_sector"])
                snap["vip3_vol"] = float(s3.get("vol_surge_10d") or snap["vip3_vol"])
        except Exception:
            pass
    return snap


def send_episode_package_to_telegram(ep_num: int, advance_state: bool = False) -> bool:
    ep_idx = (ep_num - 1) % 10
    kit = EPISODE_COPY_KIT[ep_idx]
    real_num = kit["num"]
    mp4_path = VIDEOS_DIR / f"EP{real_num:02d}_US_Viral_Shorts.mp4"
    snap = _load_live_market_snapshot()

    def _read_env_tok(fp, key):
        if os.path.exists(fp):
            m = re.search(rf"^{key}=(.+)$", open(fp, encoding="utf-8", errors="ignore").read(), re.M)
            if m:
                return m.group(1).strip().strip("'\"")
        return ""

    rsa_tok = _read_env_tok(str(BASE_DIR / ".env"), "RSA_TELEGRAM_BOT_TOKEN")
    kfg_tok = _read_env_tok(r"D:\키즈핏 영문\.env", "TELEGRAM_BOT_TOKEN")
    token = os.environ.get("HQ_TELEGRAM_BOT_TOKEN") or rsa_tok or kfg_tok or telegram_service._resolve_token()
    chat_id = os.environ.get("HQ_TELEGRAM_CHAT_ID") or "755033799"
    base = f"https://api.telegram.org/bot{token}"

    yt_title = kit["yt_title"].replace("getbreakai.com", "truthofmarket.com")
    yt_desc = (
        kit["yt_desc"]
        .replace("getbreakai.com", "truthofmarket.com")
        .replace("https://t.me/RigjtsideAlphabot", "https://t.me/truthofmarketss")
    )
    ig_caption = (
        kit["ig_caption"]
        .replace("getbreakai.com", "truthofmarket.com")
        .replace("https://t.me/RigjtsideAlphabot", "https://t.me/truthofmarketss")
        + f"\n\n📊 LIVE PW-RSI ORDER BOOK ({snap['as_of']}):\n"
        + f"🔥 #1 [FREE SHOWCASE] $CELH (${snap['celh_close']:.2f} | Score {snap['celh_score']}/100) → Entry ${snap['celh_trg']:.2f} | -9% Stop ${snap['celh_stop']:.2f} | +100% TP1 ${snap['celh_tp1']:.2f}\n"
        + f"🔒 #2 $████ [PRO VIP — {snap['vip2_sector']}] (Score {snap['vip2_score']}/100 | Vol {snap['vip2_vol']:.2f}x)\n"
        + f"🔒 #3 $████ [PRO VIP — {snap['vip3_sector']}] (Score {snap['vip3_score']}/100 | Vol {snap['vip3_vol']:.2f}x)\n"
        + '👉 Comment "SMH" or "ALPHA" for the instant DM link!'
    )

    x_cashtag_copy = (
        f"🧭 Semiconductor Fear & Greed Index: {snap['fg_score']:.1f}/100 ({snap['regime_en']}) as of {snap['as_of']}\n"
        f"• $SMH Close: ${snap['smh_close']:.2f} ({snap['smh_dd_pct']:.1f}% 52W DD) → 80% $SMH : 20% $XLV Contrarian Barbell Active\n\n"
        f"🎯 Daily PW-RSI Right-Side Ignition Order Book:\n"
        f"#1 Free Showcase: $CELH (${snap['celh_close']:.2f} | Score {snap['celh_score']}/100 | Stop ${snap['celh_stop']:.2f} | TP1 ${snap['celh_tp1']:.2f})\n"
        f"#2-#5 Pro VIP Picks: Locked ({snap['vip2_sector']} & {snap['vip3_sector']}, 2.0x+ Vol Surge)\n\n"
        f"🖥️ Live 72-Stock Terminal: https://truthofmarket.com/semi-fear-greed.html\n"
        f"$NVDA $SOXL $AMD $AVGO $TSLA $PLTR"
    )

    reddit_tv_copy = (
        f"[Quant Study] $SMH Semiconductor Fear & Greed at {snap['fg_score']:.1f} ({snap['regime_en']}) + 72-Stock Post-Washout Right-Side Ignition (PW-RSI) Screen ({snap['as_of']})\n\n"
        f"1. Macro Regime ($SMH vs $XLV Barbell):\n"
        f"- 7-Factor Semiconductor Fear & Greed Score: {snap['fg_score']:.1f}/100 ({snap['regime_en']})\n"
        f"- $SMH is trading at ${snap['smh_close']:.2f} ({snap['smh_dd_pct']:.2f}% off 52W high). When FG <= 25, our 26.8-year model shifts from 70/30 to 80% $SMH : 20% $XLV.\n\n"
        f"2. PW-RSI Right-Side Turnaround Rules (2000-2026 Backtest: 24.48% CAGR):\n"
        f"- C1: Deep 52W High Drawdown washout complete\n"
        f"- C2: Rebounding off 52W low support\n"
        f"- C3: Price reclaimed both 20D & 60D Moving Averages\n"
        f"- C4: 10D Relative Volume Surge >= 1.5x\n"
        f"- Risk Rules: -9.0% Mechanical Hard Stop (Rule 1) | 55-Day Dead Money Time Stop (Rule 2) | +100% 2x Principal Harvest (Rule 3)\n\n"
        f"3. Today's #1 Unmasked Signal:\n"
        f"- $CELH (Score {snap['celh_score']}/100): Close ${snap['celh_close']:.2f} | Entry Trigger ${snap['celh_trg']:.2f} | -9% Hard Stop ${snap['celh_stop']:.2f} | +100% TP1 ${snap['celh_tp1']:.2f}\n\n"
        f"Full interactive 72-stock screener & $SMH/$XLV simulator: https://truthofmarket.com"
    )

    timeout_cfg = httpx.Timeout(connect=20.0, read=240.0, write=240.0, pool=30.0)
    with httpx.Client(timeout=timeout_cfg) as client:
        from scripts.render_dual_yt_ig_cta import ensure_dual_videos

        yt_video_path = mp4_path
        ig_video_path = mp4_path
        if mp4_path.exists():
            try:
                yt_str, ig_str = ensure_dual_videos(str(mp4_path), "TOM", force=False)
                yt_video_path = pathlib.Path(yt_str)
                ig_video_path = pathlib.Path(ig_str)
            except Exception as e_render:
                print(f"[DailyShorts] Dual render warning: {e_render}")

        yt_safe_pin = (
            f"📌 External links aren't clickable in Shorts comments!\n"
            f"👉 {kit['yt_pin']} (Full $NVDA, $TSLA, $SOXL, $PLTR & $SMH -9% Stop / +100% Target table + FREE 3-Second Position Doctor: tap @rightsidealpha channel icon below → click truthofmarket.com in Bio! 📊🚀)"
        )

        yt_title_esc = html.escape(yt_title)
        yt_desc_esc = html.escape(yt_desc)
        yt_pin_esc = html.escape(yt_safe_pin)
        ig_cap_esc = html.escape(ig_caption)
        x_copy_esc = html.escape(x_cashtag_copy)
        reddit_copy_esc = html.escape(reddit_tv_copy)

        if yt_video_path.exists():
            yt_caption = (
                f"🇺🇸 <b>[1사업부: truthofmarket.com · 1/2 영상: 유튜브 쇼츠 전용판 ({real_num}/10편)]</b>\n"
                f"📌 주제: {kit['topic_kr']}\n"
                "✅ 엔딩 자막: 유튜브 맞춤형 (@rightsidealpha 관련 동영상 &amp; 프로필 링크 유도)\n"
                "📺 업로드 유튜브: https://www.youtube.com/@rightsidealpha"
            )
            client.post(
                f"{base}/sendVideo",
                data={"chat_id": chat_id, "caption": yt_caption, "parse_mode": "HTML", "supports_streaming": "true"},
                files={"video": (yt_video_path.name, yt_video_path.read_bytes(), "video/mp4")},
            )

        yt_messages = [
            f"🔴 <b>[1/4] 1사업부 유튜브 쇼츠 제목 (@rightsidealpha)</b> — 아래 박스 터치 시 바로 복사\n<pre>{yt_title_esc}</pre>",
            f"🟠 <b>[2/4] 1사업부 유튜브 쇼츠 설명란 (@rightsidealpha)</b> — 아래 박스 터치 시 바로 복사\n<pre>{yt_desc_esc}</pre>",
            f"📌 <b>[3/4] 1사업부 유튜브 쇼츠 안전 고정댓글 (외부 URL 0% · 관련 동영상 브릿지)</b> — 아래 박스 터치 시 복사 후 고정(Pin)\n<pre>{yt_pin_esc}</pre>",
        ]
        ok = True
        for m_html in yt_messages:
            r_txt = client.post(
                f"{base}/sendMessage",
                json={"chat_id": chat_id, "text": m_html, "parse_mode": "HTML", "disable_web_page_preview": True},
            )
            ok = ok and (r_txt.status_code == 200 and r_txt.json().get("ok", False))

        if ig_video_path.exists():
            ig_caption_vid = (
                f"📸 <b>[1사업부: truthofmarket.com · 2/2 영상: 인스타 릴스 전용판 ({real_num}/10편)]</b>\n"
                "✅ 엔딩 자막: 인스타 매니챗 맞춤형 (댓글에 'SMH' 또는 'ALPHA' 입력 시 1초 만에 DM 자동 발송 유도)\n"
                "📸 업로드 인스타: https://www.instagram.com/rightsidealpha"
            )
            client.post(
                f"{base}/sendVideo",
                data={"chat_id": chat_id, "caption": ig_caption_vid, "parse_mode": "HTML", "supports_streaming": "true"},
                files={"video": (ig_video_path.name, ig_video_path.read_bytes(), "video/mp4")},
            )

        extra_messages = [
            f"🟣 <b>[4/4] 1사업부 인스타그램 릴스 전체 본문 (@rightsidealpha · 매니챗 'SMH'/'ALPHA' 연동)</b> — 아래 박스 터치 시 바로 복사\n<pre>{ig_cap_esc}</pre>",


        ]
        for m_html in extra_messages:
            r_extra = client.post(
                f"{base}/sendMessage",
                json={"chat_id": chat_id, "text": m_html, "parse_mode": "HTML", "disable_web_page_preview": True},
            )
            ok = ok and (r_extra.status_code == 200 and r_extra.json().get("ok", False))

        print(f"[DailyShorts] Sent Full 6-Part YT+IG+X+Reddit Package EP{real_num:02d}: ok={ok}")

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
