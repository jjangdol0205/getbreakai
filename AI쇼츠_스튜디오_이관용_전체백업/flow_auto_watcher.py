# -*- coding: utf-8 -*-
"""
================================================================================
⚡ Google Flow × Antigravity 2분 컷 반자동 코파일럿 감시기 (flow_auto_watcher.py)
================================================================================
크롬 원격 디버깅(Allow 팝업) 없이 가장 빠르고 쾌적하게 협업하는 시스템입니다.

작동 순서:
1. 실행 즉시 Google Flow용 4컷 통합 프롬프트를 윈도우 클립보드에 자동 복사합니다.
   -> 사용자는 Google Flow 채팅창에서 [Ctrl + V] -> [Enter]만 누르면 됩니다!
2. 동시에 내 PC의 `다운로드(Downloads)` 폴더를 실시간 감시합니다.
3. 사용자가 Google Flow에서 생성된 영상 4개의 [다운로드(↓)] 버튼을 누르면,
   `Downloads` 폴더에 .mp4 파일 4개가 들어오는 즉시 자동으로 감지하여
   상단 상태창 없는 100% 클린 풀스크린 + 원테이크 성우 + 단어별(Word-by-Word) 자막을 입혀
   최종 완성본 쇼츠(.mp4)를 자동 생성하고 폴더를 열어줍니다!
================================================================================
"""

import os
import sys
import time
import shutil
import argparse
import subprocess
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

from flow_shorts_merger import render_clean_fullscreen_shorts_from_clips

BASE_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = BASE_DIR / "ai_shorts_output"
FLOW_CLIPS_DIR = OUTPUT_DIR / "flow_clips"
DOWNLOADS_DIR = Path.home() / "Downloads"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
FLOW_CLIPS_DIR.mkdir(parents=True, exist_ok=True)

PRESETS = {
    "1_brain": {
        "name": "US_1_BrainScience_Flow_Clean_Shorts.mp4",
        "voice": "en-US-AndrewMultilingualNeural",
        "style": "science",
        "accent": (0, 245, 212, 255),
        "script": (
            "If you sleep less than six hours tonight, your brain literally begins to eat itself. "
            "While you are awake, your neurons produce toxic metabolic waste every single second. "
            "Normally, during deep sleep, spinal fluid flushes those toxins right out. "
            "But when you skip sleep, microglial cells go into overdrive and start destroying healthy synapses. "
            "Even worse, just five nights of poor sleep drops your memory retention by forty percent."
        ),
        "flow_prompt": (
            "Generate 4 separate 9:16 vertical cinematic videos (no text on screen):\n"
            "1) Extreme macro cinematic shot: A tired human eye slowly blinks and the pupil dilates as blue smartphone light flickers across the iris in a dark room at 3 AM, 85mm macro lens.\n"
            "2) 3D medical documentary animation: Camera slowly orbits a translucent human head while glowing cyan and amber neural pathways pulse and fire across the cerebral cortex.\n"
            "3) Microscopic 3D scientific CGI: Camera pushes forward through brain neurons as bright bio-electrical signals shoot along axons and red particles accumulate around synapses.\n"
            "4) Handheld documentary shot inside a dark hospital neurology lab: A doctor points at a glowing brain MRI scan on a diagnostic monitor as scan slices animate."
        ),
    },
    "2_reels": {
        "name": "US_2_DarkLuxury_Flow_Clean_Reels.mp4",
        "voice": "en-US-AndrewMultilingualNeural",
        "style": "reels_luxury",
        "accent": (255, 218, 120, 255),
        "script": (
            "Save this before you scroll. "
            "Here are five websites so powerful, they actually feel illegal to know in twenty twenty-six. "
            "Perplexity replaces hours of research in five seconds. "
            "Gamma turns one prompt into a full presentation. "
            "And Notebook L M turns any PDF into an interactive podcast."
        ),
        "flow_prompt": (
            "Generate 4 separate 9:16 vertical cinematic 35mm film videos (no text on screen):\n"
            "1) Driver POV inside a luxury sports car driving smoothly through rainy Manhattan streets at night, raindrops streaking across the windshield with warm city bokeh.\n"
            "2) Slow dolly-in toward a sleek silver laptop on a dark walnut desk in a minimalist penthouse at night while rain streams down the floor-to-ceiling window.\n"
            "3) Cinematic close-up of hands typing on a backlit mechanical keyboard in a moody dark studio lit by a warm brass desk lamp.\n"
            "4) Aerial night helicopter shot gliding smoothly between glowing Manhattan skyscrapers in light rain, Kodak Portra 800 film look."
        ),
    },
    "3_rome": {
        "name": "US_3_AncientRome_Flow_Clean_Shorts.mp4",
        "voice": "en-US-BrianMultilingualNeural",
        "style": "history",
        "accent": (255, 214, 60, 255),
        "script": (
            "Could you actually survive twenty-four hours in Ancient Rome? "
            "First, forget sleeping in. By dawn, a million people pack into muddy streets narrower than your hallway. "
            "If you get sick, doctors might prescribe crushed gladiator sweat as medicine. "
            "Need to brush your teeth? Romans used aged human urine to whiten their smiles. "
            "And if your apartment catches fire at night, there is no public fire department, unless you pay them on the spot."
        ),
        "flow_prompt": (
            "Generate 4 separate 9:16 vertical live-action historical cinema videos (Ridley Scott ARRI Alexa style, no text on screen):\n"
            "1) Camera tracks forward through a crowded, muddy street in Ancient Rome at dawn as citizens in worn linen tunics walk past and golden sunlight pierces through dust.\n"
            "2) Macro cinema close-up of weathered hands pouring ancient silver Roman coins onto a rough wooden tavern table lit by flickering oil lamps.\n"
            "3) Slow cinematic pan across an ancient Roman marble bathhouse with thick steam rising off the water and sunbeams shining through stone arches.\n"
            "4) Dramatic night cinema shot in Ancient Rome as burning torches and fire flames flicker against stone apartment buildings while crowds gather in the street."
        ),
    },
}


def copy_to_clipboard(text: str):
    p = subprocess.Popen(["powershell", "-NoProfile", "-Command", "Set-Clipboard -Value $input"], stdin=subprocess.PIPE)
    p.communicate(input=text.encode("utf-8"))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--preset", choices=["1_brain", "2_reels", "3_rome"], default="1_brain")
    parser.add_argument("--count", type=int, default=4, help="Number of downloaded MP4 clips to wait for")
    args = parser.parse_args()

    cfg = PRESETS[args.preset]
    copy_to_clipboard(cfg["flow_prompt"])

    print("======================================================================")
    print(f"📋 [STEP 1 완료] '{args.preset}' 프롬프트가 클립보드에 자동 복사되었습니다!")
    print("👉 지금 Google Flow 채팅창에서 [Ctrl + V] -> [Enter]를 눌러주세요.")
    print(f"👉 영상 {args.count}개가 생성되면 각 영상의 [다운로드(↓)] 버튼만 눌러주세요!")
    print("======================================================================", flush=True)

    # 현재 시점 이후에 Downloads 폴더에 새로 들어오는 .mp4 파일 감시
    start_ts = time.time() - 5.0
    seen_files = set()
    collected = []

    print(f"👀 [{DOWNLOADS_DIR}] 폴더에서 새 .mp4 파일 {args.count}개 다운로드 대기 중...", flush=True)
    while len(collected) < args.count:
        if DOWNLOADS_DIR.exists():
            mp4s = [
                p for p in DOWNLOADS_DIR.glob("*.mp4")
                if p.stat().st_mtime > start_ts and p not in seen_files and not p.name.endswith(".crdownload")
            ]
            mp4s.sort(key=lambda p: p.stat().st_mtime)
            for p in mp4s:
                # 파일 쓰기가 완전히 끝났는지 확인 (크기 안정성 체크)
                s1 = p.stat().st_size
                time.sleep(0.6)
                s2 = p.stat().st_size
                if s1 == s2 and s2 > 30000:
                    seen_files.add(p)
                    idx = len(collected) + 1
                    dst = FLOW_CLIPS_DIR / f"{args.preset}_clip_{idx:02d}.mp4"
                    shutil.copy2(p, dst)
                    collected.append(dst)
                    print(f"  ✅ [{idx}/{args.count}] 다운로드 감지 및 수집 완료: {p.name} ({round(s2/1024/1024, 2)} MB)", flush=True)
                    if len(collected) >= args.count:
                        break
        time.sleep(1.5)

    print("\n🎬 4개 클립 수집 완료! 상단 상태창 없는 100% 클린 풀스크린 쇼츠 자동 합본 시작...", flush=True)
    out_mp4 = OUTPUT_DIR / cfg["name"]
    render_clean_fullscreen_shorts_from_clips(
        clip_paths=collected,
        script=cfg["script"],
        output_mp4=out_mp4,
        voice=cfg["voice"],
        style=cfg["style"],
        accent_color=cfg["accent"],
    )
    print(f"\n🎉 최종 완성본 생성 완료: {out_mp4}", flush=True)


if __name__ == "__main__":
    main()
