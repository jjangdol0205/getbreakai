# -*- coding: utf-8 -*-
"""
================================================================================
🎬 Google Flow (Veo) 클립 자동 합본 & 클린 풀스크린 쇼츠 마스터링 엔진 (V2)
================================================================================
- 상단 인위적인 상태창(HUD) 100% 제거, 1080x1920 풀스크린 모션 비디오
- 단순 N등분이 아닌 '대사 문장 시작 타이밍(WordBoundary 호흡 구간)'에 0.01초 단위로 칼같이 맞춘 컷 전환
- 미국 상위 1% 쇼츠의 2대 엔딩 공식 지원:
  1) punchline: 묵직한 한 줄 결론(Takeaway) + 시네마틱 서브베이스 드롭(Outro Boom) + 여운 페이드아웃
  2) loop: 끝문장이 0초의 첫 문장으로 자연스럽게 이어지는 무한 루프(Seamless Loop) 편집
================================================================================
"""

import os
import sys
import re
import wave
import asyncio
import argparse
import subprocess
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageEnhance
import edge_tts
import edge_tts.communicate as _edge_comm
import imageio_ffmpeg

try:
    _edge_comm._SSL_CTX.load_default_certs()
except Exception:
    pass

from us_viral_studio import (
    WIDTH,
    HEIGHT,
    FPS,
    load_font,
    FONT_SEGOE_BOLD,
    synthesize_natural_voice_with_words,
    group_words_into_phrases,
    build_studio_soundtrack,
    draw_active_word_captions,
)
from us_real_motion_studio import load_video_clip_frames

BASE_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = BASE_DIR / "ai_shorts_output"
FLOW_CLIPS_DIR = OUTPUT_DIR / "flow_clips"
TEMP_DIR = OUTPUT_DIR / "temp_flow"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
FLOW_CLIPS_DIR.mkdir(parents=True, exist_ok=True)
TEMP_DIR.mkdir(parents=True, exist_ok=True)

FFMPEG_EXE = imageio_ffmpeg.get_ffmpeg_exe()


def _count_clean_words(text: str) -> int:
    tokens = re.findall(r"[A-Za-z0-9']+", text)
    return len(tokens)


def compute_sentence_synced_cut_times(words: list, shot_scripts: list, total_dur: float) -> list:
    """
    각 컷의 대사(shot_scripts) 단어 수를 기반으로,
    이전 문장이 끝나고 다음 문장이 시작되는 정확한 호흡 지점(초)을 계산합니다.
    """
    n_shots = len(shot_scripts)
    if n_shots <= 1 or not words:
        return []

    word_counts = [_count_clean_words(s) for s in shot_scripts]
    total_expected = sum(word_counts)
    actual_total = len(words)

    cut_times = []
    cum_expected = 0
    for i in range(n_shots - 1):
        cum_expected += word_counts[i]
        # 실제 TTS 단어 인덱스로 매핑
        w_idx = int(round(cum_expected * actual_total / max(1, total_expected)))
        w_idx = max(1, min(actual_total - 1, w_idx))
        prev_end = words[w_idx - 1]["end"]
        next_start = words[w_idx]["start"]
        cut_t = (prev_end + next_start) * 0.5
        cut_times.append(cut_t)

    return cut_times


def add_outro_cinematic_boom(wav_path: Path, boom_time: float, ending_mode: str = "punchline"):
    """
    엔딩 모드에 따라 시네마틱 서브베이스 임팩트(Punchline) 또는 루프 브릿지 사운드를 추가합니다.
    """
    with wave.open(str(wav_path), "rb") as wf:
        sr = wf.getframerate()
        n_ch = wf.getnchannels()
        sampwidth = wf.getsampwidth()
        raw = wf.readframes(wf.getnframes())

    audio = np.frombuffer(raw, dtype=np.int16).astype(np.float32) / 32768.0
    if n_ch == 2:
        audio = audio.reshape(-1, 2)
    else:
        audio = np.column_stack([audio, audio])

    n_samples = audio.shape[0]
    start_idx = int(max(0.0, boom_time - 0.05) * sr)

    if ending_mode == "punchline" and start_idx < n_samples:
        # 묵직한 극장판 서브베이스 드롭 (65Hz -> 28Hz) + 따뜻한 앰비언트 잔향
        boom_len = min(int(1.25 * sr), n_samples - start_idx)
        if boom_len > 0:
            t_arr = np.linspace(0.0, boom_len / sr, boom_len, dtype=np.float32)
            freq = 62.0 * np.exp(-1.5 * t_arr) + 26.0
            phase = 2.0 * np.pi * np.cumsum(freq) / sr
            env = np.exp(-2.6 * t_arr) * np.minimum(1.0, t_arr / 0.02)
            sub_boom = (0.42 * np.sin(phase) + 0.15 * np.sin(2.0 * phase)) * env
            audio[start_idx:start_idx + boom_len, 0] += sub_boom
            audio[start_idx:start_idx + boom_len, 1] += sub_boom

        # 마지막 0.35초 부드러운 오디오 페이드아웃
        fade_len = min(int(0.35 * sr), n_samples)
        fade_curve = np.linspace(1.0, 0.0, fade_len, dtype=np.float32)[:, None]
        audio[-fade_len:] *= fade_curve

    elif ending_mode == "loop":
        # 루프 엔딩: 마지막 0.18초에 첫 문장으로 빨려 들어가는 라이저(Riser Whoosh) 삽입
        riser_len = min(int(0.22 * sr), n_samples)
        if riser_len > 0:
            t_arr = np.linspace(0.0, 1.0, riser_len, dtype=np.float32)
            freq = 90.0 + 220.0 * (t_arr ** 2)
            phase = 2.0 * np.pi * np.cumsum(freq) / sr
            riser = 0.18 * np.sin(phase) * (t_arr ** 1.5)
            audio[-riser_len:, 0] += riser
            audio[-riser_len:, 1] += riser

    audio = np.clip(audio, -0.98, 0.98)
    out_int16 = (audio * 32767.0).astype(np.int16)

    with wave.open(str(wav_path), "wb") as wf:
        wf.setnchannels(2)
        wf.setsampwidth(2)
        wf.setframerate(sr)
        wf.writeframes(out_int16.tobytes())


def render_clean_fullscreen_shorts_from_clips(
    clip_paths: list,
    script: str,
    output_mp4: Path,
    voice: str = "en-US-AndrewMultilingualNeural",
    style: str = "science",
    accent_color: tuple = (0, 245, 212, 255),
    top_clean_title: str = "",
    shot_scripts: list = None,
    ending_mode: str = "punchline",
):
    """
    상단 HUD/상태창 없이 100% 깔끔한 풀스크린 비디오 + 문장 호흡 동기화 컷 편집 +
    미국 쇼츠 엔딩 공식(punchline / loop)을 적용하여 렌더링합니다.
    """
    if shot_scripts and len(shot_scripts) == len(clip_paths):
        full_script = " ".join(s.strip() for s in shot_scripts)
    else:
        full_script = script

    tag = output_mp4.stem
    mp3_path = TEMP_DIR / f"{tag}_voice.mp3"
    wav_path = TEMP_DIR / f"{tag}_voice.wav"

    words, raw_dur = asyncio.run(
        synthesize_natural_voice_with_words(
            full_script=full_script,
            voice=voice,
            out_mp3=mp3_path,
            out_wav=wav_path,
            rate="+5%",
        )
    )
    phrases = group_words_into_phrases(words, max_words_per_group=3, max_chars=18)

    last_word_end = words[-1]["end"] if words else raw_dur
    if ending_mode == "punchline":
        # 마지막 단어 후 1.05초의 시네마틱 여운(Sub-Bass Boom + 페이드아웃) 부여
        total_dur = max(raw_dur, last_word_end + 1.05)
    elif ending_mode == "loop":
        # 무한 루프: 마지막 단어가 끝나자마자 0.06초 뒤 바로 0초 첫 문장으로 이어지도록 칼컷
        total_dur = min(raw_dur, last_word_end + 0.06)
    else:
        total_dur = raw_dur

    total_frames = int(round(total_dur * FPS))
    n_clips = len(clip_paths)

    # 문장 시작 타이밍에 맞춘 컷 전환 시간 계산
    if shot_scripts and len(shot_scripts) == n_clips:
        cut_times = compute_sentence_synced_cut_times(words, shot_scripts, total_dur)
    else:
        cut_times = [(i * total_dur / n_clips) for i in range(1, n_clips)]

    # 각 클립이 담당할 프레임 수 계산
    boundaries = [0.0] + cut_times + [total_dur]
    clip_frame_counts = []
    accum_f = 0
    for i in range(n_clips):
        if i == n_clips - 1:
            cnt = max(1, total_frames - accum_f)
        else:
            target_end_f = int(round(boundaries[i + 1] * FPS))
            cnt = max(1, target_end_f - accum_f)
        clip_frame_counts.append(cnt)
        accum_f += cnt

    all_frames = []
    for idx, (cp, cnt) in enumerate(zip(clip_paths, clip_frame_counts)):
        frames = load_video_clip_frames(
            Path(cp),
            num_frames=cnt,
            start_sec=0.0,
            target_w=WIDTH,
            target_h=HEIGHT,
            fit_mode="cover",
            speed=1.0,
        )
        all_frames.extend(frames)

    # 루프 엔딩일 때: 마지막 4프레임(0.13초)을 첫 번째 클립 시작 프레임과 살짝 블렌딩하여 시각적 점프 제거
    if ending_mode == "loop" and len(all_frames) > 8:
        first_frame = all_frames[0].convert("RGBA")
        for b_idx in range(1, 5):
            alpha = b_idx / 5.0
            cur = all_frames[-5 + b_idx].convert("RGBA")
            all_frames[-5 + b_idx] = Image.blend(cur, first_frame, alpha * 0.55).convert("RGB")

    final_audio = TEMP_DIR / f"{tag}_master.wav"
    build_studio_soundtrack(wav_path, cut_times, total_dur, style=style, final_wav=final_audio)
    add_outro_cinematic_boom(final_audio, boom_time=last_word_end, ending_mode=ending_mode)

    cmd = [
        FFMPEG_EXE, "-y",
        "-f", "rawvideo", "-vcodec", "rawvideo",
        "-s", f"{WIDTH}x{HEIGHT}", "-pix_fmt", "rgb24", "-r", str(FPS),
        "-i", "-", "-i", str(final_audio),
        "-c:v", "libx264", "-preset", "fast", "-crf", "20",
        "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k",
        "-shortest", "-movflags", "+faststart", str(output_mp4),
    ]
    proc = subprocess.Popen(cmd, stdin=subprocess.PIPE, stderr=subprocess.DEVNULL)

    font_title = load_font(FONT_SEGOE_BOLD, 48)

    for f_idx in range(total_frames):
        t = f_idx / float(FPS)
        frame = all_frames[min(f_idx, len(all_frames) - 1)]

        # punchline 엔딩 모드: 마지막 0.55초 동안 시네마틱 페이드아웃(서서히 암전)
        if ending_mode == "punchline" and (total_dur - t) < 0.55:
            rem_ratio = max(0.0, (total_dur - t) / 0.55)
            brightness = 0.15 + 0.85 * (rem_ratio ** 1.4)
            frame = ImageEnhance.Brightness(frame).enhance(brightness)

        overlay = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
        odraw = ImageDraw.Draw(overlay)

        if top_clean_title:
            tb = odraw.textbbox((0, 0), top_clean_title, font=font_title)
            tw = tb[2] - tb[0]
            odraw.text(
                ((WIDTH - tw) // 2, 140),
                top_clean_title,
                font=font_title,
                fill=(255, 255, 255, 255),
                stroke_width=6,
                stroke_fill=(0, 0, 0, 230),
            )

        draw_active_word_captions(
            odraw,
            phrases,
            t,
            accent_color=accent_color,
            y_pos=1420,
        )

        comp = Image.alpha_composite(frame.convert("RGBA"), overlay).convert("RGB")
        proc.stdin.write(comp.tobytes())

    proc.stdin.close()
    proc.wait()
    print(f"✅ [{ending_mode.upper()} 엔딩] 클린 풀스크린 쇼츠 완성: {output_mp4} (컷 전환: {[round(c, 2) for c in cut_times]}초)")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Google Flow (Veo) 클립 자동 합본 & 미국식 엔딩 마스터링 엔진")
    parser.add_argument("--ending", choices=["punchline", "loop", "both"], default="both", help="엔딩 스타일 선택 (기본: both)")
    parser.add_argument("--out", type=str, default="", help="단일 출력 파일 경로 (선택)")
    args = parser.parse_args()

    default_clips = [FLOW_CLIPS_DIR / f"shot{i}_flow.mp4" for i in range(1, 5)]
    if all(p.exists() for p in default_clips):
        clips = [str(p) for p in default_clips]
    else:
        clips = [str(p) for p in sorted(FLOW_CLIPS_DIR.glob("*.mp4"))[:4]]

    if not clips:
        dl_dir = Path.home() / "Downloads"
        if dl_dir.exists():
            import time
            now = time.time()
            recent_mp4s = [p for p in dl_dir.glob("*.mp4") if (now - p.stat().st_mtime) < 7200]
            recent_mp4s.sort(key=lambda p: p.stat().st_mtime)
            if recent_mp4s:
                print(f"✨ 다운로드 폴더에서 최근 Flow 영상 {len(recent_mp4s)}개를 자동으로 찾았습니다!")
                clips = [str(p) for p in recent_mp4s[-4:]]

    if not clips:
        print(f"💡 [{FLOW_CLIPS_DIR}] 또는 [다운로드] 폴더에 Google Flow에서 다운받은 mp4 클립들을 넣어주세요!")
        sys.exit(1)

    shots_punchline = [
        "If you sleep less than six hours tonight, your brain literally begins to eat itself.",
        "While you are awake, your neurons produce toxic metabolic waste every single second, and only deep sleep can flush those toxins out.",
        "When you skip sleep, your brain cleaning cells go into overdrive and start destroying healthy synapses.",
        "Just five nights of poor sleep drops your memory by forty percent. So put your phone down tonight, because eight hours of sleep is not a luxury, it is survival.",
    ]

    shots_loop = [
        "If you sleep less than six hours tonight, your brain literally begins to eat itself.",
        "While you are awake, your neurons produce toxic metabolic waste every single second, and only deep sleep can flush those toxins out.",
        "When you skip sleep, your brain cleaning cells go into overdrive and start destroying healthy synapses.",
        "Just five nights of poor sleep drops your memory by forty percent. So put your phone down right now, because that is exactly what happens",
    ]

    if args.ending in ("punchline", "both"):
        out_a = Path(args.out) if (args.out and args.ending == "punchline") else (OUTPUT_DIR / "US_1A_Punchline_Ending_Shorts.mp4")
        render_clean_fullscreen_shorts_from_clips(
            clip_paths=clips,
            script=" ".join(shots_punchline),
            output_mp4=out_a,
            shot_scripts=shots_punchline,
            ending_mode="punchline",
        )

    if args.ending in ("loop", "both"):
        out_b = Path(args.out) if (args.out and args.ending == "loop") else (OUTPUT_DIR / "US_1B_Seamless_Loop_Shorts.mp4")
        render_clean_fullscreen_shorts_from_clips(
            clip_paths=clips,
            script=" ".join(shots_loop),
            output_mp4=out_b,
            shot_scripts=shots_loop,
            ending_mode="loop",
        )

