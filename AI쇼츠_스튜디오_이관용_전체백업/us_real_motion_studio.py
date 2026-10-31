# -*- coding: utf-8 -*-
"""
================================================================================
🎬 US Real-Motion & 3D Animation Studio Engine (100% Moving Video Edition)
================================================================================
정지 사진을 줌인/패닝하던 기존 방식을 완전히 폐기하고,
모든 프레임이 '실제 움직이는 원본 영상(Real Moving Footage) + 3D 애니메이션 영상 +
실시간 30fps 모션 그래픽(EEG 뇌파 오실로스코프, 신경 시냅스 펄스, 실시간 게이지,
화염 불티 물리 시뮬레이션)'으로 구동되는 프로덕션 엔진입니다.
================================================================================
"""

import os
import sys
import math
import wave
import asyncio
import subprocess
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageEnhance
import edge_tts
import edge_tts.communicate as _edge_comm
import imageio_ffmpeg

try:
    _edge_comm._SSL_CTX.load_default_certs()
except Exception:
    pass

BASE_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = BASE_DIR / "ai_shorts_output"
REAL_DIR = OUTPUT_DIR / "real_footage"
TEMP_DIR = OUTPUT_DIR / "temp_motion"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
REAL_DIR.mkdir(parents=True, exist_ok=True)
TEMP_DIR.mkdir(parents=True, exist_ok=True)

FFMPEG_EXE = imageio_ffmpeg.get_ffmpeg_exe()

WIDTH = 1080
HEIGHT = 1920
FPS = 30

FONT_ARIAL_BOLD = r"C:\Windows\Fonts\arialbd.ttf"
FONT_SEGOE_BOLD = r"C:\Windows\Fonts\segoeuib.ttf"
FONT_SEGOE_REG = r"C:\Windows\Fonts\segoeui.ttf"
FONT_CONSOLAS = r"C:\Windows\Fonts\consolab.ttf"

# 기존 스튜디오 오디오/자막 유틸리티 재사용
from us_viral_studio import (
    load_font,
    synthesize_natural_voice_with_words,
    group_words_into_phrases,
    build_studio_soundtrack,
    draw_active_word_captions,
)


# ==============================================================================
# 1. 실제 비디오 클립을 30fps 프레임 배열로 디코딩하는 고속 로더
# ==============================================================================
def load_video_clip_frames(
    video_path: Path,
    num_frames: int,
    start_sec: float = 0.0,
    target_w: int = WIDTH,
    target_h: int = HEIGHT,
    fit_mode: str = "cover",
    speed: float = 1.0,
) -> list:
    """
    실제 동영상(.webm, .ogv, .mpg, .mp4)에서 지정된 구간의 프레임을 추출합니다.
    원본 길이가 짧으면 자연스럽게 앞뒤 왕복(Ping-Pong) 또는 루프하여 끊김 없이 실제 움직임을 유지합니다.
    """
    pts_expr = f"{1.0 / speed:.3f}*PTS"
    if fit_mode == "cover":
        vf = (
            f"setpts={pts_expr},"
            f"fps={FPS},"
            f"scale={target_w}:{target_h}:force_original_aspect_ratio=increase,"
            f"crop={target_w}:{target_h}"
        )
    else:
        # contain_center: 과학 3D 뇌 영상 등이 잘리지 않고 중앙에 온전히 보이도록 처리
        vf = (
            f"setpts={pts_expr},"
            f"fps={FPS},"
            f"scale={target_w}:{target_h}:force_original_aspect_ratio=decrease,"
            f"pad={target_w}:{target_h}:(ow-iw)/2:(oh-ih)/2:black"
        )

    cmd = [
        FFMPEG_EXE,
        "-ss", f"{start_sec:.2f}",
        "-i", str(video_path),
        "-vf", vf,
        "-vframes", str(num_frames),
        "-f", "rawvideo",
        "-pix_fmt", "rgb24",
        "-",
    ]
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
    raw_bytes, _ = proc.communicate()

    frame_size = target_w * target_h * 3
    extracted = []
    for i in range(0, len(raw_bytes) - frame_size + 1, frame_size):
        chunk = raw_bytes[i:i + frame_size]
        arr = np.frombuffer(chunk, dtype=np.uint8).reshape((target_h, target_w, 3))
        extracted.append(Image.fromarray(arr, mode="RGB"))

    if not extracted:
        extracted = [Image.new("RGB", (target_w, target_h), (8, 12, 18))]

    # 만약 필요한 프레임 수보다 원본 클립이 짧으면 Ping-Pong(정방향 -> 역방향) 연속 재생으로 끊김 없는 모션 생성
    if len(extracted) < num_frames:
        ping_pong = extracted + list(reversed(extracted[1:-1] if len(extracted) > 2 else extracted))
        full_frames = []
        while len(full_frames) < num_frames:
            full_frames.extend(ping_pong)
        return full_frames[:num_frames]

    return extracted[:num_frames]


# ==============================================================================
# 2. 실시간 30fps 애니메이션 그래픽 오버레이 (뇌파 EEG, 신경 시냅스 발화, 화염 불티)
# ==============================================================================
class LiveNeuralMotionGraphics:
    """
    영상 1(3D 뇌과학)에서 실제 움직이는 3D 뇌 영상 위/아래에
    실시간으로 파동치는 뇌파(EEG) 오실로스코프, 시냅스 전기 신호 발화 애니메이션,
    실시간 독소/기억력 게이지를 매 프레임 그리는 모션 그래픽 엔진
    """
    def __init__(self):
        rng = np.random.default_rng(77)
        # 신경망 노드 좌표 (상단/하단 배경에서 실시간 연결 및 전기 펄스 이동)
        self.nodes_x = rng.uniform(80, WIDTH - 80, 26)
        self.nodes_y = rng.uniform(220, 1280, 26)
        self.nodes_vx = rng.uniform(-22, 22, 26)
        self.nodes_vy = rng.uniform(-22, 22, 26)
        self.edges = []
        for i in range(26):
            for j in range(i + 1, 26):
                dist = math.hypot(self.nodes_x[i] - self.nodes_x[j], self.nodes_y[i] - self.nodes_y[j])
                if dist < 310:
                    self.edges.append((i, j))

    def draw_hud_and_animation(
        self,
        odraw: ImageDraw.ImageDraw,
        t: float,
        global_prog: float,
        shot_idx: int,
        title_top: str,
        title_main: str,
        font_mono: ImageFont.FreeTypeFont,
        font_sm: ImageFont.FreeTypeFont,
        font_lg: ImageFont.FreeTypeFont,
    ):
        # 1) 실시간 움직이는 신경 시냅스 노드 & 광자(Action Potential) 이동 애니메이션
        cur_x = []
        cur_y = []
        for i in range(len(self.nodes_x)):
            nx = self.nodes_x[i] + math.sin(t * 1.4 + i) * 35.0
            ny = self.nodes_y[i] + math.cos(t * 1.1 + i * 0.7) * 35.0
            cur_x.append(nx)
            cur_y.append(ny)

        is_toxin_phase = (shot_idx in (1, 2))
        node_col = (255, 75, 95, 110) if is_toxin_phase else (0, 245, 212, 110)
        pulse_col = (255, 90, 110, 230) if is_toxin_phase else (0, 255, 225, 230)

        for e_idx, (i, j) in enumerate(self.edges):
            x1, y1 = cur_x[i], cur_y[i]
            x2, y2 = cur_x[j], cur_y[j]
            odraw.line((x1, y1, x2, y2), fill=(node_col[0], node_col[1], node_col[2], 45), width=2)
            # 시냅스 축삭을 따라 실제로 날아가는 전기 신호 점(Moving Action Potential)
            p_pos = ((t * 1.6 + e_idx * 0.23) % 1.0)
            px = x1 + (x2 - x1) * p_pos
            py = y1 + (y2 - y1) * p_pos
            odraw.ellipse((px - 5, py - 5, px + 5, py + 5), fill=pulse_col)

        for nx, ny in zip(cur_x, cur_y):
            odraw.ellipse((nx - 6, ny - 6, nx + 6, ny + 6), fill=node_col)

        # 2) 상단 실시간 EEG 뇌파 오실로스코프 & 생체 시계 대시보드
        odraw.rounded_rectangle(
            (56, 82, WIDTH - 56, 268),
            radius=20,
            fill=(8, 14, 24, 205),
            outline=(0, 245, 212, 130),
            width=2,
        )
        # 깜빡이는 LIVE 레코딩 인디케이터
        blink_alpha = 255 if int(t * 4) % 2 == 0 else 70
        odraw.ellipse((86, 108, 104, 126), fill=(255, 55, 75, blink_alpha))
        odraw.text((118, 101), title_top, font=font_sm, fill=(0, 245, 212, 240))
        odraw.text((86, 138), title_main, font=font_lg, fill=(255, 255, 255, 255))

        # 오른쪽 상단 실시간 EEG 뇌파 파형(Scrolling Live Waveform)
        wave_pts = []
        wx_start, wx_end = 650, WIDTH - 84
        wy_mid = 142
        for x_step in range(wx_start, wx_end, 4):
            phase = (x_step - wx_start) * 0.045 - t * 9.5
            amp = (
                18.0 * math.sin(phase)
                + 11.0 * math.cos(phase * 2.3)
                + 7.0 * math.sin(phase * 5.1)
            )
            wave_pts.append((x_step, wy_mid + amp))
        if len(wave_pts) > 1:
            odraw.line(wave_pts, fill=(0, 245, 212, 235), width=3)

        # 하단 게이지 바 (실시간 독소 축적률 & 기억력 감소율 애니메이션)
        toxin_pct = min(96, int(18 + global_prog * 78))
        mem_pct = max(60, int(100 - global_prog * 40))
        bar_y = 212
        odraw.text((86, bar_y - 4), f"NEURAL TOXIN LOAD: {toxin_pct}%", font=font_mono, fill=(255, 105, 115, 245))
        odraw.rounded_rectangle((415, bar_y + 2, 680, bar_y + 22), radius=8, fill=(30, 38, 50, 220))
        fill_w = int(265 * (toxin_pct / 100.0))
        odraw.rounded_rectangle((415, bar_y + 2, 415 + fill_w, bar_y + 22), radius=8, fill=(255, 65, 85, 255))

        odraw.text((710, bar_y - 4), f"MEMORY: {mem_pct}%", font=font_mono, fill=(0, 245, 212, 245))


class FireAndDustPhysics:
    """
    고대 로마 영상(영상 3)에서 화면 위로 실제로 피어오르는 횃불 불티(Embers)와
    햇살 속 먼지 입자(Volumetric Dust)를 물리 시뮬레이션으로 렌더링합니다.
    """
    def __init__(self, count: int = 55):
        rng = np.random.default_rng(303)
        self.x = rng.uniform(0, WIDTH, count)
        self.y = rng.uniform(0, HEIGHT, count)
        self.vx = rng.uniform(-35, 35, count)
        self.vy = rng.uniform(-160, -55, count)
        self.size = rng.uniform(2.5, 6.5, count)
        self.phase = rng.uniform(0, 6.28, count)

    def draw(self, odraw: ImageDraw.ImageDraw, t: float, fiery: bool = False):
        for i in range(len(self.x)):
            px = (self.x[i] + self.vx[i] * t + 28.0 * math.sin(t * 2.4 + self.phase[i])) % WIDTH
            py = (self.y[i] + self.vy[i] * (t * (1.6 if fiery else 0.6))) % HEIGHT
            r = self.size[i] * (1.25 if fiery else 0.9)
            alpha = int(175 * (0.5 + 0.5 * math.sin(t * 5.0 + self.phase[i])))
            if fiery:
                col = (255, int(110 + 90 * math.sin(i)), 30, alpha)
            else:
                col = (255, 235, 190, int(alpha * 0.55))
            odraw.ellipse((px - r, py - r, px + r, py + r), fill=col)


# ==============================================================================
# 3. [영상 1] 실제 움직이는 3D 뇌 영상 4종 + 실시간 EEG/시냅스 애니메이션 쇼츠
# ==============================================================================
def build_real_motion_video_1():
    print("\n============================================================")
    print("🧠 [1/3] 실제 3D 뇌 회전·MRI 단층·커넥톰 비행 영상 + 실시간 뇌파 애니메이션 렌더링")
    print("============================================================")

    script = (
        "If you sleep less than six hours tonight, your brain literally begins to eat itself. "
        "While you are awake, your neurons produce toxic metabolic waste every single second. "
        "Normally, during deep sleep, spinal fluid flushes those toxins right out. "
        "But when you skip sleep, microglial cells go into overdrive and start destroying healthy synapses. "
        "Even worse, just five nights of poor sleep drops your memory retention by forty percent."
    )

    mp3_path = TEMP_DIR / "v1_voice.mp3"
    wav_path = TEMP_DIR / "v1_voice.wav"
    words, total_dur = asyncio.run(
        synthesize_natural_voice_with_words(
            full_script=script,
            voice="en-US-AndrewMultilingualNeural",
            out_mp3=mp3_path,
            out_wav=wav_path,
            rate="+6%",
        )
    )
    phrases = group_words_into_phrases(words, max_words_per_group=3, max_chars=18)

    total_frames = int(total_dur * FPS)
    shot_frames = total_frames // 4
    rem_frames = total_frames - shot_frames * 3
    counts = [shot_frames, shot_frames, shot_frames, rem_frames]

    # 4개의 실제 움직이는 3D 뇌/MRI/신경망 영상 클립 디코딩 (1080x1080 영역으로 선명하게 추출)
    print("  -> 실제 3D 뇌 애니메이션 및 MRI 비디오 프레임 디코딩 중...")
    clip1 = load_video_clip_frames(
        REAL_DIR / "v1_brain_3d_rotate.mpg", counts[0], start_sec=0.0,
        target_w=1080, target_h=1080, fit_mode="cover", speed=0.75,
    )
    clip2 = load_video_clip_frames(
        REAL_DIR / "v1_brain_connectome.ogv", counts[1], start_sec=6.0,
        target_w=1080, target_h=1080, fit_mode="cover", speed=1.1,
    )
    clip3 = load_video_clip_frames(
        REAL_DIR / "v1_brain_neural_map.ogv", counts[2], start_sec=9.0,
        target_w=1080, target_h=1080, fit_mode="cover", speed=1.15,
    )
    clip4 = load_video_clip_frames(
        REAL_DIR / "v1_brain_mri_axial.webm", counts[3], start_sec=0.0,
        target_w=1080, target_h=1080, fit_mode="contain_center", speed=0.55,
    )
    all_clips = clip1 + clip2 + clip3 + clip4

    shot_dur = total_dur / 4.0
    cut_times = [shot_dur * 1, shot_dur * 2, shot_dur * 3]
    final_audio = TEMP_DIR / "v1_master.wav"
    build_studio_soundtrack(wav_path, cut_times, total_dur, style="science", final_wav=final_audio)

    out_mp4 = OUTPUT_DIR / "US_1_BodyScience_BrainSleep_Shorts.mp4"
    cmd = [
        FFMPEG_EXE, "-y",
        "-f", "rawvideo", "-vcodec", "rawvideo",
        "-s", f"{WIDTH}x{HEIGHT}", "-pix_fmt", "rgb24", "-r", str(FPS),
        "-i", "-", "-i", str(final_audio),
        "-c:v", "libx264", "-preset", "fast", "-crf", "21",
        "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k",
        "-shortest", "-movflags", "+faststart", str(out_mp4),
    ]
    proc = subprocess.Popen(cmd, stdin=subprocess.PIPE, stderr=subprocess.DEVNULL)

    motion_gfx = LiveNeuralMotionGraphics()
    font_mono = load_font(FONT_CONSOLAS, 24)
    font_sm = load_font(FONT_SEGOE_BOLD, 24)
    font_lg = load_font(FONT_SEGOE_BOLD, 34)

    shot_labels = [
        ("LIVE 3D CORTEX TELEMETRY", "360° BRAIN ROTATION SCAN"),
        ("WHITE MATTER CONNECTOME", "METABOLIC TOXIN ACCUMULATION"),
        ("FLUORESCENT AXON MICROSCOPY", "SYNAPTIC PHAGOCYTOSIS ACTIVE"),
        ("AXIAL MRI SLICE SEQUENCE", "-40% HIPPOCAMPAL RETENTION"),
    ]

    for f_idx in range(total_frames):
        t = f_idx / float(FPS)
        global_prog = f_idx / float(max(1, total_frames - 1))
        shot_idx = min(3, int(t / shot_dur))

        # 다크 클리니컬 캔버스 위에 실제 움직이는 3D 뇌 영상을 중앙(y=275~1355)에 배치
        canvas = Image.new("RGB", (WIDTH, HEIGHT), (5, 8, 15))
        vid_frame = all_clips[f_idx]
        # 대비와 선명도 강화
        vid_frame = ImageEnhance.Contrast(vid_frame).enhance(1.22)
        canvas.paste(vid_frame, (0, 275))

        overlay = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
        odraw = ImageDraw.Draw(overlay)

        # 상·하단 경계 부드러운 페이드 처리
        for fade_i in range(45):
            alpha_f = int(255 * (1.0 - fade_i / 45.0))
            odraw.line((0, 275 + fade_i, WIDTH, 275 + fade_i), fill=(5, 8, 15, alpha_f))
            odraw.line((0, 1354 - fade_i, WIDTH, 1354 - fade_i), fill=(5, 8, 15, alpha_f))

        # 실시간 30fps 뇌파 & 시냅스 발화 모션 그래픽 렌더링
        t_top, t_main = shot_labels[shot_idx]
        motion_gfx.draw_hud_and_animation(
            odraw, t, global_prog, shot_idx, t_top, t_main, font_mono, font_sm, font_lg
        )

        # 단어별 Active-Word Kinetic Captions
        draw_active_word_captions(
            odraw, phrases, t, accent_color=(0, 245, 212, 255), y_pos=1430
        )

        prog_w = int(WIDTH * global_prog)
        odraw.rectangle((0, HEIGHT - 8, prog_w, HEIGHT), fill=(0, 245, 212, 240))

        comp = Image.alpha_composite(canvas.convert("RGBA"), overlay).convert("RGB")
        proc.stdin.write(comp.tobytes())

    proc.stdin.close()
    proc.wait()
    print(f"✅ [완료] {out_mp4} (100% 실제 3D 뇌 영상 + 실시간 모션 그래픽)")


# ==============================================================================
# 4. [영상 2] 실제 빗방울 창문 & 야간 도시 교통 실사 비디오 + 인스타 릴스 리스트
# ==============================================================================
def build_real_motion_video_2():
    print("\n============================================================")
    print("📸 [2/3] 실제 야간 빗방울 창문 & 도심 차량 주행 실사 영상 릴스 렌더링")
    print("============================================================")

    hook_script = (
        "Save this before you scroll. "
        "Here are five websites so powerful, they actually feel illegal to know in twenty twenty-six."
    )
    mp3_path = TEMP_DIR / "v2_voice.mp3"
    wav_path = TEMP_DIR / "v2_voice.wav"
    words, voice_dur = asyncio.run(
        synthesize_natural_voice_with_words(
            full_script=hook_script,
            voice="en-US-AndrewMultilingualNeural",
            out_mp3=mp3_path,
            out_wav=wav_path,
            rate="+2%",
        )
    )
    total_dur = max(11.5, voice_dur + 4.0)
    total_frames = int(total_dur * FPS)
    f_cut1 = int(total_frames * 0.36)
    f_cut2 = int(total_frames * 0.70)
    f_rem = total_frames - f_cut1 - f_cut2

    padded_wav = TEMP_DIR / "v2_voice_padded.wav"
    subprocess.run(
        [
            FFMPEG_EXE, "-y", "-i", str(wav_path),
            "-af", f"apad=whole_dur={total_dur}",
            "-ar", "44100", "-ac", "2", str(padded_wav),
        ],
        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True,
    )

    cut_times = [f_cut1 / float(FPS), (f_cut1 + f_cut2) / float(FPS)]
    final_audio = TEMP_DIR / "v2_master.wav"
    build_studio_soundtrack(padded_wav, cut_times, total_dur, style="reels_luxury", final_wav=final_audio)

    print("  -> 실제 야간 빗방울 유리창 & 도심 야간 통행 비디오 프레임 디코딩 중...")
    clip_rain = load_video_clip_frames(
        REAL_DIR / "v2_rain_window_night.webm", f_cut1, start_sec=1.0,
        target_w=WIDTH, target_h=HEIGHT, fit_mode="cover", speed=1.0,
    )
    clip_traffic = load_video_clip_frames(
        REAL_DIR / "v2_night_traffic.webm", f_cut2, start_sec=3.0,
        target_w=WIDTH, target_h=HEIGHT, fit_mode="cover", speed=1.15,
    )
    clip_tokyo = load_video_clip_frames(
        REAL_DIR / "v2_tokyo_rain_night.webm", f_rem, start_sec=1.0,
        target_w=WIDTH, target_h=HEIGHT, fit_mode="cover", speed=1.0,
    )
    all_clips = clip_rain + clip_traffic + clip_tokyo

    list_items = [
        ("01", "Perplexity.ai", "Replaces hours of Google research in 5 seconds"),
        ("02", "Gamma.app", "Turns a single text prompt into a full deck or site"),
        ("03", "TinyWow.com", "100+ free PDF, video & file tools with zero sign-up"),
        ("04", "Scribehow.com", "Auto-generates step-by-step guides while you work"),
        ("05", "NotebookLM.google", "Turns any document into an interactive AI podcast"),
    ]

    font_header_tag = load_font(FONT_SEGOE_BOLD, 25)
    font_title = load_font(FONT_SEGOE_BOLD, 46)
    font_num = load_font(FONT_SEGOE_BOLD, 32)
    font_site = load_font(FONT_SEGOE_BOLD, 36)
    font_desc = load_font(FONT_SEGOE_REG, 27)
    font_cta = load_font(FONT_SEGOE_BOLD, 31)

    out_mp4 = OUTPUT_DIR / "US_2_InstaReels_DarkLuxury_Listicle.mp4"
    cmd = [
        FFMPEG_EXE, "-y",
        "-f", "rawvideo", "-vcodec", "rawvideo",
        "-s", f"{WIDTH}x{HEIGHT}", "-pix_fmt", "rgb24", "-r", str(FPS),
        "-i", "-", "-i", str(final_audio),
        "-c:v", "libx264", "-preset", "fast", "-crf", "21",
        "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k",
        "-shortest", "-movflags", "+faststart", str(out_mp4),
    ]
    proc = subprocess.Popen(cmd, stdin=subprocess.PIPE, stderr=subprocess.DEVNULL)

    for f_idx in range(total_frames):
        t = f_idx / float(FPS)
        bg = ImageEnhance.Brightness(all_clips[f_idx]).enhance(0.68)
        bg = ImageEnhance.Contrast(bg).enhance(1.15)

        overlay = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
        odraw = ImageDraw.Draw(overlay)

        odraw.rounded_rectangle((90, 220, 465, 274), radius=27, fill=(15, 20, 28, 175), outline=(255, 255, 255, 110), width=1)
        odraw.ellipse((114, 239, 130, 255), fill=(0, 245, 212, 255))
        odraw.text((144, 232), "BOOKMARK THIS FOR LATER", font=font_header_tag, fill=(240, 245, 250, 255))

        odraw.text((92, 305), "5 Websites So Powerful They", font=font_title, fill=(255, 255, 255, 255), stroke_width=2, stroke_fill=(0, 0, 0, 200))
        odraw.text((92, 365), "Feel Illegal to Know (2026)", font=font_title, fill=(255, 218, 120, 255), stroke_width=2, stroke_fill=(0, 0, 0, 200))

        card_start_y = 480
        card_h = 162
        card_gap = 22

        # 현재 하이라이트 중인 카드 인덱스 (시간에 따라 01 -> 05 순차 네온 글로우 이동!)
        active_card_idx = int((t * 1.1) % 5)

        for idx, (num_str, site_name, site_desc) in enumerate(list_items):
            appear_t = 0.15 + idx * 0.35
            if t < appear_t:
                continue
            item_prog = min(1.0, (t - appear_t) / 0.25)
            ease = 1.0 - (1.0 - item_prog) ** 3
            slide_dy = int((1.0 - ease) * 35)
            alpha_card = int(205 * ease)
            alpha_txt = int(255 * ease)

            cy1 = card_start_y + idx * (card_h + card_gap) + slide_dy
            cy2 = cy1 + card_h

            is_glow = (idx == active_card_idx and t > 2.2)
            border_col = (255, 218, 120, 220) if is_glow else (255, 255, 255, int(75 * ease))
            border_w = 3 if is_glow else 2

            odraw.rounded_rectangle(
                (84, cy1, WIDTH - 84, cy2),
                radius=24,
                fill=(12, 16, 24, alpha_card),
                outline=border_col,
                width=border_w,
            )
            odraw.rounded_rectangle(
                (112, cy1 + 32, 176, cy1 + 92),
                radius=16,
                fill=(255, 215, 110, int(55 if is_glow else 35 * ease)),
                outline=(255, 215, 110, int(180 * ease)),
                width=1,
            )
            odraw.text((126, cy1 + 44), num_str, font=font_num, fill=(255, 220, 130, alpha_txt))
            odraw.text((202, cy1 + 28), site_name, font=font_site, fill=(255, 255, 255, alpha_txt))
            odraw.text((202, cy1 + 84), site_desc, font=font_desc, fill=(205, 215, 228, alpha_txt))

        # 하단 CTA 버튼 (살짝 맥동하는 애니메이션)
        pulse_pad = int(4 * math.sin(t * 5.0))
        cta_box_y = 1490
        odraw.rounded_rectangle(
            (84 - pulse_pad, cta_box_y - pulse_pad // 2, WIDTH - 84 + pulse_pad, cta_box_y + 104 + pulse_pad // 2),
            radius=52,
            fill=(255, 255, 255, 242),
        )
        cta_txt = 'Comment "LIST" & I\'ll DM you all 5 links'
        cb = odraw.textbbox((0, 0), cta_txt, font=font_cta)
        cw = cb[2] - cb[0]
        odraw.text(((WIDTH - cw) // 2, cta_box_y + 32), cta_txt, font=font_cta, fill=(12, 14, 18, 255))

        comp = Image.alpha_composite(bg.convert("RGBA"), overlay).convert("RGB")
        proc.stdin.write(comp.tobytes())

    proc.stdin.close()
    proc.wait()
    print(f"✅ [완료] {out_mp4} (100% 실제 야간 빗방울 & 도심 주행 실사 영상)")


# ==============================================================================
# 5. [영상 3] 실제 3D 고대 로마 복원 애니메이션 비행 + 실제 4K 콜로세움/판테온 영상
# ==============================================================================
def build_real_motion_video_3():
    print("\n============================================================")
    print("🏛️ [3/3] 실제 3D 고대 로마 시가지 복원 영상 + 4K 콜로세움/판테온 실사 영상 렌더링")
    print("============================================================")

    script = (
        "Could you actually survive twenty-four hours in Ancient Rome? "
        "First, forget sleeping in. By dawn, a million people pack into muddy streets narrower than your hallway. "
        "If you get sick, doctors might prescribe crushed gladiator sweat as medicine. "
        "Need to brush your teeth? Romans used aged human urine to whiten their smiles. "
        "And if your apartment catches fire at night, there is no public fire department, unless you pay them on the spot."
    )

    mp3_path = TEMP_DIR / "v3_voice.mp3"
    wav_path = TEMP_DIR / "v3_voice.wav"
    words, total_dur = asyncio.run(
        synthesize_natural_voice_with_words(
            full_script=script,
            voice="en-US-BrianMultilingualNeural",
            out_mp3=mp3_path,
            out_wav=wav_path,
            rate="+5%",
        )
    )
    phrases = group_words_into_phrases(words, max_words_per_group=3, max_chars=19)

    total_frames = int(total_dur * FPS)
    shot_frames = total_frames // 4
    rem_frames = total_frames - shot_frames * 3
    counts = [shot_frames, shot_frames, shot_frames, rem_frames]

    print("  -> 실제 3D 고대 로마 복원 비디오 & 4K 로마 실사 영상 디코딩 중...")
    # Cut 1: 고대 로마 수부라(Subura) 및 시가지 3D 항공 애니메이션
    clip1 = load_video_clip_frames(
        REAL_DIR / "v3_ancient_rome_3d.webm", counts[0], start_sec=5.0,
        target_w=WIDTH, target_h=HEIGHT, fit_mode="cover", speed=1.0,
    )
    # Cut 2: 실제 콜로세움 내부 아치 & 경기장 카메라 패닝 영상
    clip2 = load_video_clip_frames(
        REAL_DIR / "v3_inside_colosseum.webm", counts[1], start_sec=2.0,
        target_w=WIDTH, target_h=HEIGHT, fit_mode="cover", speed=1.1,
    )
    # Cut 3: 실제 로마 판테온 신전 & 기둥 카메라 무빙 영상
    clip3 = load_video_clip_frames(
        REAL_DIR / "v3_pantheon_rome.webm", counts[2], start_sec=3.0,
        target_w=WIDTH, target_h=HEIGHT, fit_mode="cover", speed=1.1,
    )
    # Cut 4: 고대 로마 콜로세움 야간/황혼 3D 복원 회전 영상 + 실시간 화재 불티 시뮬레이션
    clip4 = load_video_clip_frames(
        REAL_DIR / "v3_colosseum_3d.webm", counts[3], start_sec=10.0,
        target_w=WIDTH, target_h=HEIGHT, fit_mode="cover", speed=1.15,
    )
    all_clips = clip1 + clip2 + clip3 + clip4

    shot_dur = total_dur / 4.0
    cut_times = [shot_dur * 1, shot_dur * 2, shot_dur * 3]
    final_audio = TEMP_DIR / "v3_master.wav"
    build_studio_soundtrack(wav_path, cut_times, total_dur, style="history", final_wav=final_audio)

    out_mp4 = OUTPUT_DIR / "US_3_History_SurviveAncientRome_Shorts.mp4"
    cmd = [
        FFMPEG_EXE, "-y",
        "-f", "rawvideo", "-vcodec", "rawvideo",
        "-s", f"{WIDTH}x{HEIGHT}", "-pix_fmt", "rgb24", "-r", str(FPS),
        "-i", "-", "-i", str(final_audio),
        "-c:v", "libx264", "-preset", "fast", "-crf", "21",
        "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k",
        "-shortest", "-movflags", "+faststart", str(out_mp4),
    ]
    proc = subprocess.Popen(cmd, stdin=subprocess.PIPE, stderr=subprocess.DEVNULL)

    fire_fx = FireAndDustPhysics(count=60)
    font_ch_sm = load_font(FONT_SEGOE_BOLD, 25)
    font_ch_lg = load_font(FONT_SEGOE_BOLD, 33)

    chapter_titles = [
        ("06:00 AM // 3D SUBURA DISTRICT", "1,000,000 CITIZENS AWAKEN"),
        ("11:00 AM // COLOSSEUM ARENA", "THE GLADIATOR SWEAT CURE"),
        ("03:00 PM // IMPERIAL PANTHEON", "ANCIENT ROMAN HYGIENE"),
        ("11:00 PM // NIGHT FIRE IN ROME", "PRIVATE FIRE BRIGADES"),
    ]

    for f_idx in range(total_frames):
        t = f_idx / float(FPS)
        global_prog = f_idx / float(max(1, total_frames - 1))
        shot_idx = min(3, int(t / shot_dur))

        frame = all_clips[f_idx]
        # 마지막 4번째 챕터("if your apartment catches fire at night")에서는 붉은 화염 조명 그레이딩 추가
        if shot_idx == 3:
            arr = np.asarray(frame, dtype=np.float32)
            flicker = 1.0 + 0.14 * math.sin(t * 14.0)
            arr[..., 0] = np.clip(arr[..., 0] * 1.35 * flicker + 28, 0, 255)
            arr[..., 1] = np.clip(arr[..., 1] * 0.95, 0, 255)
            arr[..., 2] = np.clip(arr[..., 2] * 0.75, 0, 255)
            frame = Image.fromarray(arr.astype(np.uint8), mode="RGB")

        overlay = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
        odraw = ImageDraw.Draw(overlay)

        # 하단 자막 가독성을 위한 자연스러운 그라데이션 셰이드
        for s_y in range(1180, HEIGHT, 4):
            s_alpha = int(170 * ((s_y - 1180) / float(HEIGHT - 1180)))
            odraw.rectangle((0, s_y, WIDTH, s_y + 4), fill=(8, 6, 4, s_alpha))

        # 햇살 속 먼지 또는 야간 화재 불티 물리 애니메이션
        fire_fx.draw(odraw, t, fiery=(shot_idx == 3))

        c_top, c_main = chapter_titles[shot_idx]
        odraw.rounded_rectangle((64, 96, 610, 198), radius=14, fill=(18, 14, 10, 185), outline=(255, 200, 110, 140), width=2)
        odraw.text((92, 109), c_top, font=font_ch_sm, fill=(255, 205, 115, 240))
        odraw.text((92, 144), c_main, font=font_ch_lg, fill=(255, 250, 240, 255))

        draw_active_word_captions(
            odraw, phrases, t, accent_color=(255, 214, 60, 255), y_pos=1390
        )

        prog_w = int(WIDTH * global_prog)
        odraw.rectangle((0, HEIGHT - 8, prog_w, HEIGHT), fill=(255, 205, 90, 240))

        comp = Image.alpha_composite(frame.convert("RGBA"), overlay).convert("RGB")
        proc.stdin.write(comp.tobytes())

    proc.stdin.close()
    proc.wait()
    print(f"✅ [완료] {out_mp4} (100% 실제 3D 고대 로마 애니메이션 & 4K 실사 영상)")


if __name__ == "__main__":
    build_real_motion_video_1()
    build_real_motion_video_2()
    build_real_motion_video_3()
