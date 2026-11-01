#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
================================================================================
🎬 10-Episode US Viral Promo Shorts Merger & Subtitle Mastering Engine
================================================================================
- Supports all 10 US Viral Promo Episodes (EP01 ~ EP10) for:
  * SemiFearGreed (https://truthofmarket.com)
  * RightSideAlpha (https://getbreakai.com)
  * Telegram Bot (@SemifearGreedbot)
- Automatically picks up downloaded Google Flow (.mp4) clips from:
  1) `d:/투자홈페이지/3_AI영상_홍보_스튜디오/ai_shorts_output/flow_clips/epXX_shot1.mp4` (or `epXX.mp4`)
  2) User's Windows `Downloads` folder (most recent `.mp4` files downloaded from Google Flow)
- Appends the 1080x1920 Live Website UI recording as the final CTA shot (Shot 4),
  synthesizes native US voiceover (`en-US-AndrewMultilingualNeural`),
  burns 0.01s-synced Word-by-Word Active Pop-up Subtitles, and adds cinematic sub-bass boom!

Usage:
  python scripts/merge_10_promo_shorts.py --ep 1
  python scripts/merge_10_promo_shorts.py --all
  python scripts/merge_10_promo_shorts.py --from-downloads --ep 1
"""
import argparse
import shutil
import sys
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

ROOT_DIR = Path(__file__).resolve().parents[1]
STUDIO_DIR = next(ROOT_DIR.parent.glob("3_*"), ROOT_DIR.parent / "3_AI영상_홍보_스튜디오")
if str(STUDIO_DIR) not in sys.path:
    sys.path.insert(0, str(STUDIO_DIR))

OUTPUT_DIR = STUDIO_DIR / "ai_shorts_output"
FLOW_CLIPS_DIR = OUTPUT_DIR / "flow_clips"
LOCAL_OUT_DIR = ROOT_DIR / "promo_shorts_output"
LOCAL_OUT_DIR.mkdir(parents=True, exist_ok=True)


# ==============================================================================
# 10 US VIRAL PROMO SHORTS EPISODES (PROMPTS + VOICEOVER SCRIPTS + CTA CONFIG)
# ==============================================================================
EPISODES = {
    1: {
        "code": "ep01",
        "title": "EP01_Semi_2AM_Panic_Extreme_Fear",
        "platform": "semi",
        "style_tag": "Dark Fincher Psychological Hook",
        "accent_color": (239, 68, 68, 255),  # Crimson Red
        "ending_mode": "punchline",
        "flow_prompts": [
            # Shot 1 (Main Hook / Fast 1-Clip Mode)
            "Vertical 9:16 cinematic close-up shot, 4k photorealistic. A stressed 32-year-old American male trader sitting on the edge of his bed at 2 AM in a dark bedroom. Intense crimson red light from his smartphone screen illuminates the sweat and exhaustion on his face as semiconductor stocks crash. Moody David Fincher style dark teal and red lighting, shallow depth of field, slow push-in.",
            # Shot 2 (Visual Metaphor / Fear Gauge)
            "Vertical 9:16 cinematic macro shot, 4k photorealistic. A sleek glass speedometer-style financial Fear and Greed dial on a dark institutional trading terminal slamming violently to the left into glowing red Extreme Fear at number 18. Crisp reflections on dark glass, dramatic cinematic lighting.",
            # Shot 3 (Quant Awakening)
            "Vertical 9:16 cinematic medium shot, 4k photorealistic. A calm, razor-sharp Wall Street quantitative portfolio manager in a dark glass Manhattan office at dawn, executing an automated rebalance order as emerald green buy blocks light up his ultrawide screen. Smooth tracking shot.",
        ],
        "shot_scripts": [
            "Every single time semiconductor stocks drop twenty percent, retail traders panic and sell at the exact bottom.",
            "Right now, our seven-factor Semiconductor Fear and Greed Index just plunged to eighteen, Extreme Fear.",
            "Over twenty-six years of market data, shifting from a seventy-thirty baseline to eighty percent SMH and twenty percent Healthcare XLV during Extreme Fear crushed the Nasdaq.",
            "Check today's live Fear and Greed score and exact rebalance shares free at truthofmarket dot com.",
        ],
    },
    2: {
        "code": "ep02",
        "title": "EP02_RSA_Falling_Knife_Trap",
        "platform": "rsa",
        "style_tag": "Brutal Truth / Wall Street Wake-Up",
        "accent_color": (16, 185, 129, 255),  # Emerald Green
        "ending_mode": "punchline",
        "flow_prompts": [
            # Shot 1
            "Vertical 9:16 cinematic over-the-shoulder shot, 4k photorealistic. A frustrated retail investor at a dimly lit home desk staring at a glowing red stock chart plunging down a steep cliff on his monitor, holding his head in his hands. Dark moody atmosphere, realistic screen reflections, slow zoom in.",
            # Shot 2
            "Vertical 9:16 cinematic slow-motion macro shot, 4k photorealistic. A gleaming steel dagger falling vertically through dark smoky air, reflecting crimson stock ticker numbers on its blade. High-contrast dramatic studio lighting, ultra-detailed.",
            # Shot 3
            "Vertical 9:16 cinematic shot, 4k photorealistic. A high-tech dark quantitative trading monitor showing a stock chart rounding out a flat bottom base and erupting upward through a glowing golden 60-day moving average line with massive green volume bars.",
        ],
        "shot_scripts": [
            "You bought a famous stock down fifty percent thinking it was cheap, and then it dropped another forty percent.",
            "Buying the left side of a crash is called catching a falling knife, and it traps retail capital for years.",
            "Institutional quants never guess the bottom. They wait for Right-Side Ignition, when price reclaims the sixty-day moving average on surging volume.",
            "Scan all seventy-two US momentum leaders and test your portfolio free at getbreakai dot com.",
        ],
    },
    3: {
        "code": "ep03",
        "title": "EP03_Semi_80_20_Barbell_Secret",
        "platform": "semi",
        "style_tag": "Dark Luxury / Hedge Fund Playbook",
        "accent_color": (245, 158, 11, 255),  # Gold Amber
        "ending_mode": "punchline",
        "flow_prompts": [
            # Shot 1
            "Vertical 9:16 cinematic shot, 4k photorealistic. Nighttime view from inside a sleek black Porsche driving through rain-slicked Manhattan streets, neon stock market tickers reflecting off the wet windshield. Dark luxury aesthetic, shallow depth of field.",
            # Shot 2
            "Vertical 9:16 cinematic close-up shot, 4k photorealistic. A balanced precision brass scale on a dark marble desk in a private wealth office, one side holding a glowing silicon semiconductor wafer and the other side holding a defensive medical shield emblem. Moody warm gold lighting.",
            # Shot 3
            "Vertical 9:16 cinematic shot, 4k photorealistic. A wealthy quantitative strategist in a tailored dark suit reviewing a glowing 26-year compounding equity curve climbing steadily on a sleek MacBook Pro in a dark penthouse study.",
        ],
        "shot_scripts": [
            "Going one hundred percent into semiconductor ETFs feels genius in a bull run, until a thirty-five percent drawdown wipes out your nerve.",
            "That is why institutional money uses the Golden Barbell: seventy percent SMH semiconductors paired with thirty percent XLV defensive healthcare.",
            "When chip stocks crash into Extreme Fear below twenty-five, you sell defensive XLV at the top and rotate into eighty percent SMH at dirt-cheap prices.",
            "Calculate your exact dollar and share rebalance in three seconds at truthofmarket dot com.",
        ],
    },
    4: {
        "code": "ep04",
        "title": "EP04_RSA_Position_Doctor_Bagholder_Audit",
        "platform": "rsa",
        "style_tag": "Interactive Diagnostic / Pain Relief Hook",
        "accent_color": (56, 189, 248, 255),  # Cyan Blue
        "ending_mode": "punchline",
        "flow_prompts": [
            # Shot 1
            "Vertical 9:16 cinematic close-up shot, 4k photorealistic. A conflicted investor staring at a red minus-twenty-two percent portfolio screen on his phone at night, thumb hovering nervously between a red Sell button and a gray Hold button. Tense cinematic lighting.",
            # Shot 2
            "Vertical 9:16 cinematic shot, 4k photorealistic. A futuristic medical diagnostic scanner beam sweeping across a 3D holographic stock candlestick chart in a dark lab, highlighting a broken support line in bright warning red.",
            # Shot 3
            "Vertical 9:16 cinematic medium shot, 4k photorealistic. A relieved trader nodding with clarity as a clean quantitative risk dashboard displays an exact nine-percent stop-loss level and a two-x profit target on his dark monitor.",
        ],
        "shot_scripts": [
            "Be honest. How many red stocks are sitting in your brokerage account right now because you hope they will bounce back?",
            "Hope is not a risk management strategy. Every institutional trade needs a hard nine-percent stop loss and a fifty-five day time stop.",
            "Instead of guessing whether to hold or cut, run your ticker, entry price, and holding days through our algorithmic Position Doctor.",
            "Get an instant mathematical verdict on your stock right now at getbreakai dot com or on our free Telegram bot.",
        ],
    },
    5: {
        "code": "ep05",
        "title": "EP05_RSA_Institutional_Breakout_Footprints",
        "platform": "rsa",
        "style_tag": "'Feels Illegal to Know' Insider Quant Style",
        "accent_color": (16, 185, 129, 255),  # Emerald Green
        "ending_mode": "punchline",
        "flow_prompts": [
            # Shot 1
            "Vertical 9:16 cinematic shot, 4k photorealistic. A shadowy view of the New York Stock Exchange facade at dusk as institutional server racks pulse with high-frequency fiber-optic light behind glass windows. Thriller movie atmosphere, slow push-in.",
            # Shot 2
            "Vertical 9:16 cinematic macro shot, 4k photorealistic. An extreme close-up of a dark trading terminal where ten-day institutional volume bars suddenly spike one-point-five times higher in glowing neon green while price crosses an orange moving average.",
            # Shot 3
            "Vertical 9:16 cinematic shot, 4k photorealistic. A focused young quant analyst in a dark room smiling subtlely as five US stock tickers lock into an emerald Ignition Zone on his multi-screen setup.",
        ],
        "shot_scripts": [
            "Wall Street hedge funds cannot hide when they accumulate millions of shares in a turnaround stock.",
            "Before a stock doubles, it leaves four mathematical footprints: seller washout, higher lows, reclaiming the sixty-day moving average, and a ten-day volume surge.",
            "Our PW-RSI engine scans seventy-two US market leaders daily to catch that exact Right-Side Ignition before financial television even notices.",
            "See today's top five US Ignition stocks unlocked right now at getbreakai dot com.",
        ],
    },
    6: {
        "code": "ep06",
        "title": "EP06_Semi_SOXL_Wipeout_vs_Smart_Barbell",
        "platform": "semi",
        "style_tag": "3D Stress-Test / Volatility Reality Check",
        "accent_color": (239, 68, 68, 255),  # Crimson Red
        "ending_mode": "punchline",
        "flow_prompts": [
            # Shot 1
            "Vertical 9:16 cinematic shot, 4k photorealistic. A dramatic rollercoaster track plunging straight down into dark storm clouds with glowing red stock market numbers flying past the camera. Intense visceral motion, 4k cinema quality.",
            # Shot 2
            "Vertical 9:16 cinematic close-up shot, 4k photorealistic. A silicon wafer inside a high-tech cleanroom glowing under ultraviolet lithography lasers, reflecting sharp geometric patterns on dark glass.",
            # Shot 3
            "Vertical 9:16 cinematic shot, 4k photorealistic. A calm institutional trading desk overlooking a city skyline at night, displaying a green portfolio curve outperforming a crashing red benchmark.",
        ],
        "shot_scripts": [
            "Everyone loves semiconductor stocks when Nvidia and SMH are hitting all-time highs, but a twenty percent pullback destroys over-leveraged accounts.",
            "In our twenty-six year backtest from two thousand to twenty twenty-six, the semiconductor cycle suffered brutal drawdowns every few years.",
            "Yet investors who systematically rebalanced between SMH semiconductors and XLV healthcare turned ten thousand dollars into over two million dollars with lower stress.",
            "Download the full twenty-six year dataset and check today's regime signal at truthofmarket dot com.",
        ],
    },
    7: {
        "code": "ep07",
        "title": "EP07_RSA_55_Day_Dead_Money_Rule",
        "platform": "rsa",
        "style_tag": "Opportunity Cost / Time-Stop Secret",
        "accent_color": (245, 158, 11, 255),  # Amber
        "ending_mode": "punchline",
        "flow_prompts": [
            # Shot 1
            "Vertical 9:16 cinematic macro shot, 4k photorealistic. An antique glass hourglass on a dark trading desk with golden sand running out, while a flat sideways stock chart glows faintly in the background. Moody cinematic lighting.",
            # Shot 2
            "Vertical 9:16 cinematic shot, 4k photorealistic. A split-focus shot in a dark room: in the foreground a stagnant gray stock ticker barely moving, while in the background emerald green breakout stocks rocket upward on a wall screen.",
            # Shot 3
            "Vertical 9:16 cinematic shot, 4k photorealistic. A decisive trader pressing a clean keyboard key to rotate capital out of a dead position into a surging right-side momentum leader.",
        ],
        "shot_scripts": [
            "The biggest silent killer of your stock portfolio is not a sudden crash. It is dead money.",
            "When you hold a stagnant stock for months waiting for a bounce, you miss every real institutional breakout happening across the market.",
            "That is why our quantitative engine enforces Rule Two: if a position fails to gain eight percent within fifty-five trading days, you cut it and rotate into active Right-Side leaders.",
            "Test if your stocks have triggered the fifty-five day time stop right now at getbreakai dot com.",
        ],
    },
    8: {
        "code": "ep08",
        "title": "EP08_RSA_100_Percent_TP1_Free_Runner",
        "platform": "rsa",
        "style_tag": "Asymmetric Wealth / House Money Rule",
        "accent_color": (16, 185, 129, 255),  # Emerald
        "ending_mode": "punchline",
        "flow_prompts": [
            # Shot 1
            "Vertical 9:16 cinematic close-up shot, 4k photorealistic. A retail trader celebrating a big paper gain on his phone, followed by a sudden flash of red as the stock reverses and wipes out his unbooked profits. Dramatic lighting shift.",
            # Shot 2
            "Vertical 9:16 cinematic shot, 4k photorealistic. A sleek digital vault door locking in glowing gold bars on the left while a green rocket trajectory continues climbing on a transparent HUD glass screen on the right.",
            # Shot 3
            "Vertical 9:16 cinematic medium shot, 4k photorealistic. A relaxed investor sipping espresso on a high-rise balcony at sunset while his tablet trails a winning stock along a smooth 60-day moving average line.",
        ],
        "shot_scripts": [
            "Have you ever watched a winning stock double in your account, only to hold too long and watch the entire profit vanish?",
            "Professional momentum traders never ride a full position back down. At plus one hundred percent gain, you sell exactly half.",
            "That single move locks in one hundred percent of your original cash into your pocket, turning the remaining half into a stress-free runner trailed by the sixty-day moving average.",
            "Get exact two-x target prices and trailing stop levels for seventy-two US stocks at getbreakai dot com.",
        ],
    },
    9: {
        "code": "ep09",
        "title": "EP09_Telegram_Quant_Bot_Instant_Alerts",
        "platform": "semi",
        "style_tag": "Speed & Automation / Telegram Bot Hook",
        "accent_color": (56, 189, 248, 255),  # Telegram Sky Blue
        "ending_mode": "punchline",
        "flow_prompts": [
            # Shot 1
            "Vertical 9:16 cinematic shot, 4k photorealistic. A noisy wall of television screens broadcasting financial news anchors talking over late market headlines, slightly blurred in the background while a trader checks a sleek smartphone in the foreground.",
            # Shot 2
            "Vertical 9:16 cinematic macro shot, 4k photorealistic. A smartphone resting on a dark carbon-fiber desk lighting up with an instant glowing blue Telegram quantitative alert notification showing semiconductor Fear and Greed at 18 and top stock triggers.",
            # Shot 3
            "Vertical 9:16 cinematic shot, 4k photorealistic. A modern commuter on a sleek evening train tapping a single button on his phone to view institutional stop-loss and target levels in one second.",
        ],
        "shot_scripts": [
            "By the time financial news anchors tell you semiconductor stocks are a buy, institutional money is already up forty percent.",
            "You do not have time to stare at charts for six hours a day. You need real-time quantitative signals delivered straight to your phone.",
            "Our free Telegram bot gives you the live Semiconductor Fear and Greed score, top five US Right-Side Ignition stocks, and instant price diagnostics with one tap.",
            "Search SemifearGreedbot on Telegram or tap the link at truthofmarket dot com to connect in ten seconds.",
        ],
    },
    10: {
        "code": "ep10",
        "title": "EP10_Semi_3_Tranche_Crash_Deployment",
        "platform": "semi",
        "style_tag": "Master Blueprint / $100K Crash Calculator",
        "accent_color": (16, 185, 129, 255),  # Emerald Green
        "ending_mode": "punchline",
        "flow_prompts": [
            # Shot 1
            "Vertical 9:16 cinematic shot, 4k photorealistic. A retail trader shoving all his chips into the center of a dark table as a market chart dips ten percent, only for the chart in the background to plunge much deeper into red.",
            # Shot 2
            "Vertical 9:16 cinematic close-up shot, 4k photorealistic. Three glowing emerald capital vaults unlocking sequentially one by one as a digital Fear and Greed counter drops from 35 to 25 to 18 on a dark glass screen.",
            # Shot 3
            "Vertical 9:16 cinematic shot, 4k photorealistic. A confident institutional investor reviewing a 3-tranche capital deployment schedule on a wide dark monitor as semiconductor stocks begin a massive recovery.",
        ],
        "shot_scripts": [
            "The worst mistake investors make in a tech sell-off is firing all their cash on the very first five percent dip.",
            "When semiconductors enter a real correction, smart money deploys cash in three mathematical tranches: thirty percent in Fear, forty percent in Extreme Fear, and thirty percent on the right-side rebound.",
            "With the Semiconductor Fear and Greed Index sitting at eighteen right now, our Lump-Sum Tranche Calculator shows you the exact dollar amounts to deploy today.",
            "Run your own cash deployment blueprint free right now at truthofmarket dot com.",
        ],
    },
}


def find_clips_for_episode(ep_num: int, use_downloads: bool = False) -> list[str]:
    """
    Resolves clips for an episode:
    1) Checks `flow_clips/ep{02d}_shot1.mp4`, `ep{02d}_shot2.mp4`, `ep{02d}_shot3.mp4`
    2) Checks `flow_clips/ep{02d}.mp4` (if user generated 1 clip for the episode, repeats/splits across Shots 1-3)
    3) If --from-downloads is set (or no epXX files found), checks recent `.mp4` files in ~/Downloads
    4) Appends the live website UI recording (`semi_shot4_live_ui.mp4` or `rsa_shot4_live_ui.mp4`) as Shot 4!
    """
    ep = EPISODES[ep_num]
    code = ep["code"]
    platform = ep["platform"]

    shot4_ui = FLOW_CLIPS_DIR / ("semi_shot4_live_ui.mp4" if platform == "semi" else "rsa_shot4_live_ui.mp4")
    if not shot4_ui.exists():
        # Fallback if Shot 4 UI hasn't been captured yet
        alt = sorted(FLOW_CLIPS_DIR.glob("*shot4*.mp4"))
        if alt:
            shot4_ui = alt[0]

    # 1. Check dedicated 3-shot files: ep01_shot1.mp4, ep01_shot2.mp4, ep01_shot3.mp4
    three_shots = [FLOW_CLIPS_DIR / f"{code}_shot{i}.mp4" for i in range(1, 4)]
    if all(p.exists() for p in three_shots):
        print(f"✅ [{code.upper()}] Found dedicated 3 Flow clips: {[p.name for p in three_shots]}")
        return [str(p) for p in three_shots] + [str(shot4_ui)]

    # 2. Check single clip for the episode: ep01.mp4 or ep1.mp4
    for single_name in [f"{code}.mp4", f"ep{ep_num}.mp4", f"ep{ep_num:02d}_flow.mp4"]:
        sp = FLOW_CLIPS_DIR / single_name
        if sp.exists():
            print(f"✅ [{code.upper()}] Found single Flow clip {sp.name} -> pairing with Live UI Shot 4")
            return [str(sp), str(sp), str(sp), str(shot4_ui)]

    # 3. Check user's Windows Downloads folder if requested
    dl_dir = Path.home() / "Downloads"
    if use_downloads and dl_dir.exists():
        recent_mp4s = sorted(
            [p for p in dl_dir.glob("*.mp4") if p.stat().st_size > 30_000],
            key=lambda p: p.stat().st_mtime,
            reverse=True,
        )
        if len(recent_mp4s) >= 3:
            chosen = list(reversed(recent_mp4s[:3]))
            for idx, src in enumerate(chosen, start=1):
                dst = FLOW_CLIPS_DIR / f"{code}_shot{idx}.mp4"
                shutil.copy2(src, dst)
            print(f"✅ [{code.upper()}] Imported 3 latest MP4s from Downloads: {[p.name for p in chosen]}")
            return [str(FLOW_CLIPS_DIR / f"{code}_shot{i}.mp4") for i in range(1, 4)] + [str(shot4_ui)]
        elif len(recent_mp4s) >= 1:
            src = recent_mp4s[0]
            dst = FLOW_CLIPS_DIR / f"{code}.mp4"
            shutil.copy2(src, dst)
            print(f"✅ [{code.upper()}] Imported latest MP4 from Downloads: {src.name}")
            return [str(dst), str(dst), str(dst), str(shot4_ui)]

    # 4. Fallback to existing Flow clips in flow_clips so preview works out of the box
    fallback = [FLOW_CLIPS_DIR / f"shot{i}_flow.mp4" for i in range(1, 4)]
    if all(p.exists() for p in fallback):
        print(f"ℹ️ [{code.upper()}] Using existing studio Flow clips for preview.")
        return [str(p) for p in fallback] + [str(shot4_ui)]

    any_mp4s = sorted(FLOW_CLIPS_DIR.glob("*.mp4"))[:3]
    return [str(p) for p in any_mp4s] + [str(shot4_ui)]


def build_episode(ep_num: int, use_downloads: bool = False) -> Path:
    from flow_shorts_merger import render_clean_fullscreen_shorts_from_clips

    ep = EPISODES[ep_num]
    clips = find_clips_for_episode(ep_num, use_downloads=use_downloads)
    out_mp4 = LOCAL_OUT_DIR / f"{ep['title']}.mp4"

    print(f"\n🎬 Rendering {ep['title']} ({ep['style_tag']})...")
    render_clean_fullscreen_shorts_from_clips(
        clip_paths=clips,
        script=" ".join(ep["shot_scripts"]),
        output_mp4=out_mp4,
        voice="en-US-AndrewMultilingualNeural",
        style="wealth",
        accent_color=ep["accent_color"],
        top_clean_title="",
        shot_scripts=ep["shot_scripts"],
        ending_mode=ep["ending_mode"],
    )
    # Also copy to 3_AI영상_홍보_스튜디오/ai_shorts_output
    try:
        shutil.copy2(out_mp4, OUTPUT_DIR / out_mp4.name)
    except Exception:
        pass
    print(f"🎉 Completed: {out_mp4}")
    return out_mp4


def main() -> int:
    parser = argparse.ArgumentParser(description="Merge Google Flow clips + Live UI + Native US Subtitles for 10 Promo Shorts")
    parser.add_argument("--ep", type=int, default=1, choices=range(1, 11), help="Episode number (1 to 10)")
    parser.add_argument("--all", action="store_true", help="Render all 10 episodes")
    parser.add_argument("--from-downloads", action="store_true", help="Automatically import latest MP4s from ~/Downloads")
    args = parser.parse_args()

    if args.all:
        for e in range(1, 11):
            build_episode(e, use_downloads=False)
    else:
        build_episode(args.ep, use_downloads=args.from_downloads)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
