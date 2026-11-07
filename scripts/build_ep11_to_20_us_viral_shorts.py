#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
build_ep11_to_20_us_viral_shorts.py
================================================================================
Extracts the user's downloaded Google Flow clips from `11월 06 - 20_38.zip`,
maps them to 1사업부 (`truthofmarket.com`) Episodes 11–20 (Shots 1–3 + Shot 4 Live UI),
synthesizes 100% native US voiceover (`en-US-AndrewMultilingualNeural` / `en-US-BrianMultilingualNeural`),
renders clean standalone WordBoundary subtitles (`Y=1420`, zero top/bottom banner clutter),
and applies the final 3.8s `truthofmarket.com` domain capsule (`_IG_Reels.mp4` & `_YT_Shorts.mp4`).
"""
import os
import sys
import shutil
import zipfile
import subprocess
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import imageio_ffmpeg

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

WORKSPACE_DIR = Path(__file__).resolve().parent.parent
STUDIO_DIR = WORKSPACE_DIR.parent / "2_AI쇼츠_홍보영상_스튜디오"
if str(STUDIO_DIR) not in sys.path:
    sys.path.insert(0, str(STUDIO_DIR))

from flow_shorts_merger import render_clean_fullscreen_shorts_from_clips

FLOW_CLIPS_DIR = STUDIO_DIR / "ai_shorts_output" / "flow_clips"
OUTPUT_DIR = WORKSPACE_DIR / "viral_shorts_10_output"
WORK_DIR = WORKSPACE_DIR / "data" / "_clean_levelup_work"
FLOW_CLIPS_DIR.mkdir(parents=True, exist_ok=True)
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
WORK_DIR.mkdir(parents=True, exist_ok=True)

FFMPEG_EXE = imageio_ffmpeg.get_ffmpeg_exe()
FONT_BOLD = Path("d:/사업아이템/src/fonts/Pretendard-Black.otf")
if not FONT_BOLD.exists():
    FONT_BOLD = Path("C:/Windows/Fonts/arialbd.ttf")


ZIP_TO_SHOT_MAP = {
    "9ecec084": "ep11_shot1.mp4",
    "bcc8eb78": "ep11_shot2.mp4",
    "f2537376": "ep11_shot3.mp4",
    "db79ff15": "ep12_shot1.mp4",
    "6635900c": "ep12_shot2.mp4",
    "8e28bb9b": "ep12_shot3.mp4",
    "ae30c0fe": "ep13_shot1.mp4",
    "c5c484da": "ep13_shot2.mp4",
    "cba1063a": "ep13_shot3.mp4",
    "239e721d": "ep14_shot1.mp4",
    "878e0b53": "ep14_shot2.mp4",
    "f41c10d7": "ep15_shot1.mp4",
    "76f70189": "ep15_shot2.mp4",
    "a040a8f5": "ep15_shot3.mp4",
    "4f6b7690": "ep16_shot1.mp4",
    "97cb9af4": "ep16_shot2.mp4",
    "3ceb737b": "ep17_shot1.mp4",
    "00a028c9": "ep17_shot2.mp4",
    "42b78c38": "ep17_shot3.mp4",
    "07f66683": "ep18_shot1.mp4",
    "0b05d53b": "ep18_shot2.mp4",
    "1612fcff": "ep18_shot3.mp4",
    "e84b55e5": "ep19_shot1.mp4",
    "13b25984": "ep19_shot2.mp4",
    "d6aa6a73": "ep20_shot1.mp4",
    "3a993551": "ep20_shot2.mp4",
    "f1384f3f": "ep20_shot3.mp4",
}


EPISODES_11_TO_20 = [
    {
        "id": "ep11",
        "num": 11,
        "title": "Why $SMCI & $AMD Dip Buyers Got Trapped (The 60-Day Institutional Trend Filter)",
        "voice": "en-US-AndrewMultilingualNeural",
        "accent": (16, 185, 129, 255),
        "ui_type": "rsa",
        "shot_scripts": [
            "Buying a crashing semiconductor stock while it is still trapped below its sixty-day moving average is financial suicide.",
            "Every dead-cat bounce looks like a bottom until institutional sellers slam it down another thirty percent.",
            "Wall Street quants wait for one non-negotiable proof: price must reclaim the sixty-day trendline with surging volume.",
            "Check which semiconductor stocks just triggered a live Right-Side Ignition right now at truthofmarket dot com.",
        ],
    },
    {
        "id": "ep12",
        "num": 12,
        "title": "The Earnings Gamble Trap vs. Post-Earnings Right-Side Ignition",
        "voice": "en-US-BrianMultilingualNeural",
        "accent": (56, 189, 248, 255),
        "ui_type": "rsa",
        "shot_scripts": [
            "Holding a stock into an earnings report is not investing, it is flipping a coin at a casino.",
            "Even when a company beats estimates, Wall Street algorithms can gap the stock down twenty percent overnight.",
            "Instead of gambling before earnings, our quant engine waits for post-earnings washout to finish and flags the exact day institutional buyers step back in.",
            "Scan all seventy-two US market leaders for post-earnings breakouts right now at truthofmarket dot com.",
        ],
    },
    {
        "id": "ep13",
        "num": 13,
        "title": "Semiconductor Fear & Greed Above 75 (Extreme Greed): When Quants Secretly Trim",
        "voice": "en-US-AndrewMultilingualNeural",
        "accent": (245, 158, 11, 255),
        "ui_type": "semi",
        "shot_scripts": [
            "When everyone on social media is bragging about their semiconductor gains, smart money is quietly heading for the exit.",
            "Whenever our seven-factor Semiconductor Fear and Greed Index climbs above seventy-five into Extreme Greed, chasing breakouts carries massive drawdown risk.",
            "Our barbell engine automatically trims offensive tech down to fifty percent and locks profits into defensive healthcare before the correction hits.",
            "Track the live Semiconductor Fear and Greed gauge today at truthofmarket dot com.",
        ],
    },
    {
        "id": "ep14",
        "num": 14,
        "title": "Averaging Down vs. Pyramiding Up: The Math That Separates Quants from Losers",
        "voice": "en-US-BrianMultilingualNeural",
        "accent": (239, 68, 68, 255),
        "ui_type": "rsa",
        "shot_scripts": [
            "Averaging down into a losing stock is how one bad trade wipes out three years of gains.",
            "You are feeding good capital to a broken trend while institutional sellers keep unloading.",
            "Wall Street quants do the exact opposite: they cut losers at minus nine percent and only add capital after a stock proves itself above the trendline.",
            "Diagnose your current holdings in three seconds with Position Doctor at truthofmarket dot com.",
        ],
    },
    {
        "id": "ep15",
        "num": 15,
        "title": "The 52-Week Low Illusion: Why Cheap Stocks Drop Another 60%",
        "voice": "en-US-AndrewMultilingualNeural",
        "accent": (16, 185, 129, 255),
        "ui_type": "rsa",
        "shot_scripts": [
            "Buying a stock just because it hit the fifty-two week low list is the fastest way to catch a falling knife.",
            "Stocks making new lows have zero overhead buyers and endless institutional tax-loss selling.",
            "Our twenty-six year quant study proves the sweet spot only begins after a stock rebounds at least twelve percent off its low and reclaims the sixty-day trendline.",
            "See every stock in the confirmed recovery zone right now at truthofmarket dot com.",
        ],
    },
    {
        "id": "ep16",
        "num": 16,
        "title": "How to Spot Institutional Dark Pool Accumulation Before Price Explodes",
        "voice": "en-US-BrianMultilingualNeural",
        "accent": (56, 189, 248, 255),
        "ui_type": "rsa",
        "shot_scripts": [
            "Hedge funds cannot buy ten million shares of a stock in one day without spiking the price.",
            "So they accumulate quietly at the bottom, leaving behind one unmistakable clue: institutional volume expansion.",
            "When ten-day volume surges one point five to two times above the twenty-day average right under the sixty-day line, big money is loading up.",
            "Track real-time institutional volume surges across seventy-two US stocks at truthofmarket dot com.",
        ],
    },
    {
        "id": "ep17",
        "num": 17,
        "title": "Stuck in a -25% Drawdown? Run This 3-Second Position Doctor Quant Triage",
        "voice": "en-US-AndrewMultilingualNeural",
        "accent": (245, 158, 11, 255),
        "ui_type": "rsa",
        "shot_scripts": [
            "When you are down twenty-five percent on a stock, hope is the most expensive emotion in the market.",
            "Should you hold for a recovery, cut the loss, or rotate into a stronger institutional leader?",
            "Instead of guessing, enter your ticker and average buy price into our quantitative Position Doctor.",
            "In three seconds, it calculates your exact mathematical stop-loss, trend health, and two-X target at truthofmarket dot com.",
        ],
    },
    {
        "id": "ep18",
        "num": 18,
        "title": "Why 90% of Hype Stocks Fail in Rate Spikes — And How the 4-Factor Filter Survives",
        "voice": "en-US-BrianMultilingualNeural",
        "accent": (16, 185, 129, 255),
        "ui_type": "rsa",
        "shot_scripts": [
            "Every time treasury yields spike or macro panic hits, ninety percent of social media hype stocks get wiped out.",
            "Our quant engine survived twenty-six years of crashes because every trade must pass four strict mathematical gates.",
            "Deep seller washout, confirmed floor recovery, sixty-day trend reclamation, and institutional volume surge.",
            "Check which US market leaders pass all four gates today at truthofmarket dot com.",
        ],
    },
    {
        "id": "ep19",
        "num": 19,
        "title": "The Trailing 60-Day Line: How to Ride a +240% Winner Without Selling Early",
        "voice": "en-US-AndrewMultilingualNeural",
        "accent": (56, 189, 248, 255),
        "ui_type": "rsa",
        "shot_scripts": [
            "Retail traders cut their winners at ten percent and hold their losers down fifty percent.",
            "To build real market wealth, you must flip that equation with mathematical exit rules.",
            "After taking half off at plus one hundred percent for a risk-free ride, our engine trails the remaining shares along the sixty-day moving average until the macro trend breaks.",
            "See our live trailing trend signals right now at truthofmarket dot com.",
        ],
    },
    {
        "id": "ep20",
        "num": 20,
        "title": "Sunday Night Wall Street Prep: Build Your Top 5 Breakout Watchlist in 60 Seconds",
        "voice": "en-US-BrianMultilingualNeural",
        "accent": (16, 185, 129, 255),
        "ui_type": "rsa",
        "shot_scripts": [
            "Amateur traders wake up at nine twenty-five A M on Monday and chase whatever stock is trending on social media.",
            "Professional quants win the week on Sunday night before the futures market even opens.",
            "In sixty seconds, you can filter seventy-two liquid US leaders down to the exact stocks coiling just below their Right-Side Ignition trigger.",
            "Build your Monday breakout watchlist right now at truthofmarket dot com.",
        ],
    },
]


def extract_zip_clips():
    dl = Path.home() / "Downloads"
    zips = sorted(dl.glob("*20_38*.zip"), key=lambda p: p.stat().st_mtime, reverse=True)
    if not zips:
        raise FileNotFoundError("Could not find *20_38*.zip in Downloads")
    zp = zips[0]
    print(f"📦 Extracting {zp.name} into {FLOW_CLIPS_DIR}...")
    with zipfile.ZipFile(zp, "r") as z:
        for info in z.infolist():
            if not info.filename.lower().endswith(".mp4"):
                continue
            for key_hash, dst_name in ZIP_TO_SHOT_MAP.items():
                if key_hash in info.filename:
                    dst_path = FLOW_CLIPS_DIR / dst_name
                    with z.open(info) as src_f, open(dst_path, "wb") as dst_f:
                        shutil.copyfileobj(src_f, dst_f)
                    print(f"  -> Mapped {info.filename}  ==>  {dst_name}")
                    break

    # Fill the 3 clips that Google Flow omitted in the 30-clip batch using matching institutional clips
    fallbacks = {
        "ep14_shot3.mp4": "ep18_shot3.mp4",
        "ep16_shot3.mp4": "ep12_shot3.mp4",
        "ep19_shot3.mp4": "ep07.mp4",
    }
    for missing_name, src_name in fallbacks.items():
        dst_p = FLOW_CLIPS_DIR / missing_name
        src_p = FLOW_CLIPS_DIR / src_name
        if not dst_p.exists() and src_p.exists():
            shutil.copy2(src_p, dst_p)
            print(f"  -> Paired {missing_name} with clean institutional clip {src_name}")


def make_tom_ending_png(out_png: Path, platform: str):
    W, H = 1080, 1920
    canvas = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    draw = ImageDraw.Draw(canvas)

    # Replace old `getbreakai.com` header on Shot 4 live UI with `truthofmarket.com`
    draw.rounded_rectangle([72, 82, 1008, 252], radius=28, fill=(11, 20, 34, 255), outline=(16, 185, 129, 255), width=3)
    f_top = ImageFont.truetype(str(FONT_BOLD), 42)
    f_sub = ImageFont.truetype(str(FONT_BOLD), 28)

    t1 = "truthofmarket.com  |  LIVE QUANT TERMINAL"
    b1 = draw.textbbox((0, 0), t1, font=f_top)
    draw.text(((W - (b1[2] - b1[0])) // 2, 108), t1, font=f_top, fill=(255, 255, 255, 255))

    t2 = "100% Free Live Semiconductor Regime & 72-Stock Scanner"
    b2 = draw.textbbox((0, 0), t2, font=f_sub)
    draw.text(((W - (b2[2] - b2[0])) // 2, 178), t2, font=f_sub, fill=(94, 255, 208, 255))

    # 100% solid Midnight Navy pill (RGBA 10,16,28,255) at Y=1575..1660 (zero ghosting, zero overlap with Y=1420 subtitle)
    if platform == "ig":
        pill = "Link in Bio · truthofmarket.com"
        outline_c = (255, 232, 0, 255)
        text_c = (255, 232, 0, 255)
    else:
        pill = "Pinned Comment & Bio · truthofmarket.com"
        outline_c = (0, 245, 212, 255)
        text_c = (0, 245, 212, 255)

    f_pill = ImageFont.truetype(str(FONT_BOLD), 36)
    bp = draw.textbbox((0, 0), pill, font=f_pill)
    pw = bp[2] - bp[0]
    px1, px2 = (W - pw) // 2 - 44, (W + pw) // 2 + 44
    draw.rounded_rectangle([px1, 1575, px2, 1660], radius=42, fill=(10, 16, 28, 255), outline=outline_c, width=3)
    draw.text(((W - pw) // 2, 1597), pill, font=f_pill, fill=text_c)

    canvas.save(out_png)


def get_duration(mp4_path: Path) -> float:
    import re
    res = subprocess.run(
        [FFMPEG_EXE, "-i", str(mp4_path)],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        encoding="utf-8",
        errors="ignore",
    )
    m = re.search(r"Duration:\s*(\d+):(\d+):(\d+\.\d+)", res.stderr)
    if not m:
        return 24.0
    return int(m.group(1)) * 3600 + int(m.group(2)) * 60 + float(m.group(3))


def apply_clean_ending_overlay(base_mp4: Path, ig_png: Path, yt_png: Path, tail_sec: float = 3.8):
    dur = get_duration(base_mp4)
    start_t = max(0.0, dur - tail_sec)

    ig_out = base_mp4.parent / f"{base_mp4.stem}_IG_Reels.mp4"
    yt_out = base_mp4.parent / f"{base_mp4.stem}_YT_Shorts.mp4"

    for png_path, dst_mp4 in [(ig_png, ig_out), (yt_png, yt_out)]:
        fc = f"[0:v][1:v]overlay=0:0:enable='gte(t,{start_t:.2f})':format=auto,format=yuv420p[outv]"
        cmd = [
            FFMPEG_EXE, "-y",
            "-i", str(base_mp4),
            "-loop", "1", "-t", f"{dur + 0.5:.2f}", "-i", str(png_path),
            "-filter_complex", fc,
            "-map", "[outv]", "-map", "0:a:0",
            "-c:v", "libx264", "-preset", "fast", "-crf", "19",
            "-c:a", "copy",
            "-movflags", "+faststart",
            str(dst_mp4),
        ]
        res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, encoding="utf-8", errors="ignore")
        if res.returncode != 0:
            raise RuntimeError(f"FFmpeg overlay failed on {dst_mp4.name}: {res.stderr[-400:]}")

    shutil.copy2(ig_out, base_mp4)
    print(f"  ✨ Clean Mastered: {base_mp4.name}, {ig_out.name}, {yt_out.name} ({dur:.1f}s)", flush=True)


def main():
    extract_zip_clips()

    ig_png = WORK_DIR / "tom_ep11_20_ig.png"
    yt_png = WORK_DIR / "tom_ep11_20_yt.png"
    make_tom_ending_png(ig_png, "ig")
    make_tom_ending_png(yt_png, "yt")

    rsa_ui = FLOW_CLIPS_DIR / "rsa_shot4_live_ui.mp4"
    semi_ui = FLOW_CLIPS_DIR / "semi_shot4_live_ui.mp4"

    for ep in EPISODES_11_TO_20:
        ep_id = ep["id"]
        num = ep["num"]
        out_mp4 = OUTPUT_DIR / f"{ep_id.upper()}_US_Viral_Shorts.mp4"
        ig_check = OUTPUT_DIR / f"{ep_id.upper()}_US_Viral_Shorts_IG_Reels.mp4"
        yt_check = OUTPUT_DIR / f"{ep_id.upper()}_US_Viral_Shorts_YT_Shorts.mp4"
        if out_mp4.exists() and ig_check.exists() and yt_check.exists() and yt_check.stat().st_size > 1_000_000:
            print(f"⏭️ [EP{num:02d}] Already completed ({out_mp4.name}, {ig_check.name}, {yt_check.name}), skipping...", flush=True)
            continue
        ui_clip = semi_ui if (ep["ui_type"] == "semi" and semi_ui.exists()) else rsa_ui
        clips = [
            str(FLOW_CLIPS_DIR / f"{ep_id}_shot1.mp4"),
            str(FLOW_CLIPS_DIR / f"{ep_id}_shot2.mp4"),
            str(FLOW_CLIPS_DIR / f"{ep_id}_shot3.mp4"),
            str(ui_clip),
        ]
        print(f"\n🎬 [EP{num:02d}] Rendering 4-Shot Hybrid: {ep['title']}...", flush=True)
        render_clean_fullscreen_shorts_from_clips(
            clip_paths=clips,
            script=" ".join(ep["shot_scripts"]),
            output_mp4=out_mp4,
            voice=ep["voice"],
            style="wealth",
            accent_color=ep["accent"],
            top_clean_title="",
            shot_scripts=ep["shot_scripts"],
            ending_mode="punchline",
        )
        apply_clean_ending_overlay(out_mp4, ig_png, yt_png, tail_sec=3.8)

    print("\n🎉 ALL 10 NEW EPISODES (EP11 ~ EP20) MASTERED SUCCESSFULLY!", flush=True)


if __name__ == "__main__":
    main()
