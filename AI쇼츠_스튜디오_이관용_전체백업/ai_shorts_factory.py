# -*- coding: utf-8 -*-
"""
================================================================================
🎬 AI 바이럴 쇼츠 자동 제작 엔진 (AI Shorts Auto-Factory v1.0)
================================================================================
머니멘터리 영상("프롬프트 하나로 매달 수천만원 버는 남자의 역대급 부업") 속
1억 뷰 스타일 AI 쇼츠를 내 PC에서 무제한 무료로 생성하는 올인원 파이프라인입니다.

지원 모드:
1. [Global Split-Screen Mode] 썸네일 속 노트북 화면 그대로 재현!
   - 상단(천사/하늘 시네마틱 모션) + 하단(예수님/인물 시네마틱 포트레이트 + 오라 효과)
   - 중앙 라벤더/네온 캡션 박스 ("Do you love Jesus?" 스타일) + 동적 강조 자막
   - 영문 신경망 AI 성우(edge-tts) + 천상의 앰비언트 패드 BGM 자동 합성

2. [Korea Viral Full-Screen Mode] 국내 조회수 폭발형 명언·부의 법칙·심리 쇼츠
   - 풀스크린 1080x1920 줌인/패닝(Ken Burns) + 황금 파티클 이펙트
   - 한국어 신경망 AI 성우 + 노란색/민트색 핵심 키워드 하이라이트 팝업 자막
   - 다크 시네마틱 BGM + 상단 후킹 배지 & 하단 진행바

3. [Custom Prompt Mode] 원하는 주제 한 줄만 입력하면 대본 -> 음성 -> 영상(.mp4) 자동 완성!
================================================================================
"""

import os
import sys
import math
import time
import json
import wave
import struct
import asyncio
import argparse
import subprocess
import urllib.request
import urllib.parse
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance
import edge_tts
import edge_tts.communicate as _edge_comm
import imageio_ffmpeg

# Windows OS 시스템 루트 인증서 저장소 로드
try:
    _edge_comm._SSL_CTX.load_default_certs()
except Exception:
    pass

# 기본 경로 설정
BASE_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = BASE_DIR / "ai_shorts_output"
ASSETS_DIR = OUTPUT_DIR / "assets"
TEMP_DIR = OUTPUT_DIR / "temp"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
ASSETS_DIR.mkdir(parents=True, exist_ok=True)
TEMP_DIR.mkdir(parents=True, exist_ok=True)

FFMPEG_EXE = imageio_ffmpeg.get_ffmpeg_exe()

# 해상도 및 프레임 설정 (유튜브 쇼츠 / 릴스 / 틱톡 표준 9:16 Full HD)
WIDTH = 1080
HEIGHT = 1920
FPS = 30

# 폰트 경로 (Windows 기본 탑재 고딕/볼드 폰트)
FONT_KO_BOLD = r"C:\Windows\Fonts\malgunbd.ttf"
FONT_KO_REG = r"C:\Windows\Fonts\malgun.ttf"
FONT_EN_BOLD = r"C:\Windows\Fonts\arialbd.ttf"
FONT_EN_IMPACT = r"C:\Windows\Fonts\impact.ttf"


def get_font(font_path: str, size: int) -> ImageFont.FreeTypeFont:
    if os.path.exists(font_path):
        return ImageFont.truetype(font_path, size)
    return ImageFont.truetype(FONT_KO_BOLD, size)


# ==============================================================================
# 1. 저작권 걱정 없는 시네마틱 앰비언트 BGM 합성기 (Numpy Wave Synthesizer)
# ==============================================================================
def generate_cinematic_bgm(
    wav_path: Path,
    duration_sec: float,
    mood: str = "heavenly",
    sample_rate: int = 44100,
):
    """
    유튜브 저작권 위반(음원 수익 정지)이 0%인 자체 합성 시네마틱 스테레오 BGM 생성
    - heavenly: 따뜻하고 웅장한 천상의 코드 패드 + 쉬머 하모닉스 (글로벌 축복/감동 쇼츠용)
    - dark_wealth: 묵직하고 몰입감 넘치는 다크 시네마틱 드론 + 펄스 (국내 동기부여/부자법칙 쇼츠용)
    """
    total_samples = int(duration_sec * sample_rate)
    t = np.linspace(0, duration_sec, total_samples, endpoint=False)

    if mood == "heavenly":
        # Fmaj7 -> Cmaj7 -> Dm7 -> Bbmaj7 천상의 감동 코드 진행
        chord_freqs = [
            [174.61, 220.00, 261.63, 329.63, 523.25],  # Fmaj7
            [130.81, 196.00, 246.94, 329.63, 392.00],  # Cmaj7
            [146.83, 220.00, 261.63, 349.23, 440.00],  # Dm7
            [116.54, 174.61, 220.00, 293.66, 440.00],  # Bbmaj9
        ]
    else:
        # C minor -> Ab major -> Fm -> G7 다크 시네마틱 몰입 코드 진행
        chord_freqs = [
            [130.81, 155.56, 196.00, 261.63, 311.13],  # Cm
            [103.83, 155.56, 207.65, 261.63, 311.13],  # Ab
            [87.31, 130.81, 174.61, 207.65, 261.63],   # Fm
            [98.00, 146.83, 196.00, 246.94, 293.66],   # G
        ]

    left = np.zeros(total_samples, dtype=np.float64)
    right = np.zeros(total_samples, dtype=np.float64)

    chord_len = duration_sec / len(chord_freqs)
    for idx, freqs in enumerate(chord_freqs):
        start_t = idx * chord_len
        end_t = (idx + 1) * chord_len
        # 부드러운 크로스페이드 엔벨로프
        env = np.clip((t - start_t) / 1.2, 0, 1) * np.clip((end_t - t) / 1.2, 0, 1)
        mask = (t >= max(0, start_t - 1.2)) & (t <= min(duration_sec, end_t + 1.2))
        tm = t[mask]
        em = env[mask]

        for f_i, f in enumerate(freqs):
            # 스테레오 디튜닝 및 따뜻한 배음(Harmonics) 합성
            detune = 0.35 * (f_i - 2)
            l_wave = (
                0.6 * np.sin(2 * np.pi * (f - detune) * tm)
                + 0.25 * np.sin(2 * np.pi * (f * 2.0) * tm + 0.3)
                + 0.10 * np.sin(2 * np.pi * (f * 0.5) * tm)
            )
            r_wave = (
                0.6 * np.sin(2 * np.pi * (f + detune) * tm + 0.4)
                + 0.25 * np.sin(2 * np.pi * (f * 2.0) * tm + 0.9)
                + 0.10 * np.sin(2 * np.pi * (f * 0.5) * tm + 0.2)
            )
            weight = 0.22 / (1 + 0.25 * f_i)
            left[mask] += weight * l_wave * em
            right[mask] += weight * r_wave * em

    # 은은한 저음 심장박동/리듬 펄스 추가
    if mood != "heavenly":
        pulse = (0.5 + 0.5 * np.sin(2 * np.pi * 1.5 * t)) ** 3
        sub_bass = 0.15 * np.sin(2 * np.pi * 65.41 * t) * pulse
        left += sub_bass
        right += sub_bass
    else:
        # 천상의 반짝이는 벨(Bell Shimmer) 배음
        shimmer = 0.04 * np.sin(2 * np.pi * 1046.5 * t) * (0.5 + 0.5 * np.sin(2 * np.pi * 0.8 * t))
        left += shimmer
        right += shimmer * 0.9

    # 전체 페이드 인 / 아웃
    global_env = np.clip(t / 0.8, 0, 1) * np.clip((duration_sec - t) / 1.5, 0, 1)
    left *= global_env * 0.35   # 성우 목소리가 잘 들리도록 BGM 볼륨 최적화
    right *= global_env * 0.35

    # 16-bit PCM 스테레오 WAV 저장
    stereo = np.vstack((left, right)).T
    stereo = np.clip(stereo, -0.98, 0.98)
    pcm = (stereo * 32767).astype(np.int16)

    with wave.open(str(wav_path), "wb") as wf:
        wf.setnchannels(2)
        wf.setsampwidth(2)
        wf.setframerate(sample_rate)
        wf.writeframes(pcm.tobytes())


# ==============================================================================
# 2. 문장별 신경망 AI 성우(TTS) 생성 및 정확한 길이 측정
# ==============================================================================
async def synthesize_segments_tts(segments: list, voice: str, rate: str = "+0%", pitch: str = "+0Hz"):
    """
    각 대본 문장을 edge-tts로 개별 MP3 생성 후 WAV로 변환하여 정확한 프레임/초 길이를 측정합니다.
    """
    results = []
    for idx, seg in enumerate(segments):
        mp3_path = TEMP_DIR / f"tts_seg_{idx:02d}.mp3"
        wav_path = TEMP_DIR / f"tts_seg_{idx:02d}.wav"

        communicate = edge_tts.Communicate(
            text=seg["tts_text"],
            voice=voice,
            rate=rate,
            pitch=pitch,
        )
        await communicate.save(str(mp3_path))

        # ffmpeg로 44.1kHz 스테레오 WAV 변환 + 앞뒤 미세 무음 정리 및 0.25초 자연스러운 호흡 여백 추가
        cmd = [
            FFMPEG_EXE, "-y",
            "-i", str(mp3_path),
            "-af", "apad=pad_dur=0.28",
            "-ar", "44100",
            "-ac", "2",
            str(wav_path),
        ]
        subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)

        with wave.open(str(wav_path), "rb") as wf:
            frames = wf.getnframes()
            sr = wf.getframerate()
            dur = frames / float(sr)

        seg_copy = dict(seg)
        seg_copy["wav_path"] = wav_path
        seg_copy["duration"] = max(dur, 1.8)
        results.append(seg_copy)

    return results


def merge_audio_with_bgm(segments_with_audio: list, mood: str, final_audio_path: Path) -> float:
    """
    문장별 음성 WAV들을 하나로 이어붙이고, 배경음악(BGM)과 믹싱하여 최종 오디오 트랙을 생성합니다.
    """
    sample_rate = 44100
    voice_chunks = []

    current_time = 0.0
    for seg in segments_with_audio:
        with wave.open(str(seg["wav_path"]), "rb") as wf:
            raw = wf.readframes(wf.getnframes())
            arr = np.frombuffer(raw, dtype=np.int16).reshape(-1, 2).astype(np.float64) / 32768.0
        seg_dur = len(arr) / float(sample_rate)
        seg["start_time"] = current_time
        seg["end_time"] = current_time + seg_dur
        seg["duration"] = seg_dur
        # 프레임 시점의 음성 에너지(하단 인물 오라/호흡 반응용) 계산
        rms_window = int(sample_rate / FPS)
        energies = []
        for f_idx in range(0, len(arr), rms_window):
            chunk = arr[f_idx:f_idx + rms_window]
            energies.append(float(np.sqrt(np.mean(chunk ** 2))) if len(chunk) > 0 else 0.0)
        seg["energies"] = energies
        voice_chunks.append(arr)
        current_time += seg_dur

    # 엔딩 여운 0.8초 추가
    tail_samples = int(0.8 * sample_rate)
    voice_chunks.append(np.zeros((tail_samples, 2), dtype=np.float64))
    total_duration = current_time + 0.8

    full_voice = np.vstack(voice_chunks)

    # BGM 생성 및 로드
    bgm_path = TEMP_DIR / "bgm_track.wav"
    generate_cinematic_bgm(bgm_path, total_duration, mood=mood, sample_rate=sample_rate)
    with wave.open(str(bgm_path), "rb") as wf:
        bgm_raw = wf.readframes(wf.getnframes())
        bgm_arr = np.frombuffer(bgm_raw, dtype=np.int16).reshape(-1, 2).astype(np.float64) / 32768.0

    min_len = min(len(full_voice), len(bgm_arr))
    mixed = full_voice[:min_len] * 1.15 + bgm_arr[:min_len] * 0.75
    mixed = np.clip(mixed, -0.98, 0.98)
    pcm = (mixed * 32767).astype(np.int16)

    with wave.open(str(final_audio_path), "wb") as wf:
        wf.setnchannels(2)
        wf.setsampwidth(2)
        wf.setframerate(sample_rate)
        wf.writeframes(pcm.tobytes())

    return total_duration


# ==============================================================================
# 3. 고화질 아트워크 로드 및 자동 생성기 (로컬 에셋 + AI API + 프로시저럴 아트)
# ==============================================================================
def create_fallback_artwork(path: Path, theme: str, w: int = 1080, h: int = 1080):
    """
    네트워크 제한 시에도 즉시 고품질 시네마틱 아트워크를 생성하는 폴백 렌더러
    """
    y, x = np.ogrid[:h, :w]
    cx, cy = w / 2.0, h / 2.0
    dist = np.sqrt((x - cx) ** 2 + (y - cy) ** 2) / (max(w, h) * 0.7)

    if "angel" in theme or "heaven" in theme:
        # 황금빛 태양 광선과 신비로운 구름 그라데이션
        angle = np.arctan2(y - cy * 0.7, x - cx)
        rays = 0.5 + 0.5 * np.cos(angle * 16)
        r = np.clip(255 * (1.0 - dist * 0.55) + 45 * rays, 30, 255)
        g = np.clip(210 * (1.0 - dist * 0.65) + 35 * rays, 20, 245)
        b = np.clip(135 * (1.0 - dist * 0.75) + 20 * rays, 15, 210)
    elif "jesus" in theme:
        # 따뜻한 렘브란트 조명 포트레이트 배경
        r = np.clip(180 * (1.0 - dist * 0.8), 20, 220)
        g = np.clip(135 * (1.0 - dist * 0.85), 15, 175)
        b = np.clip(90 * (1.0 - dist * 0.9), 10, 120)
    else:
        # 서울 펜트하우스 다크 골드 & 네온 블루 야경 분위기
        r = np.clip(45 + 160 * np.exp(-dist * 2.2), 12, 230)
        g = np.clip(55 + 125 * np.exp(-dist * 2.5), 18, 195)
        b = np.clip(95 + 90 * (1.0 - y / float(h)), 30, 210)

    arr = np.stack([r, g, b], axis=-1).astype(np.uint8)
    img = Image.fromarray(arr, mode="RGB")
    img.save(path)


def ensure_scene_image(filename: str, prompt: str, target_w: int = 1080, target_h: int = 1080) -> Image.Image:
    """
    1순위: assets 폴더에 이미 생성된 고해상도 AI 이미지 사용
    2순위: Pollinations Flux 무료 AI 이미지 생성 API 호출
    3순위: 프로시저럴 시네마틱 배경 생성
    """
    asset_path = ASSETS_DIR / filename
    if not asset_path.exists() or asset_path.stat().st_size < 5000:
        try:
            encoded = urllib.parse.quote(prompt)
            url = f"https://image.pollinations.ai/prompt/{encoded}?width={target_w}&height={target_h}&nologo=true&seed=42"
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
            with urllib.request.urlopen(req, timeout=12) as resp:
                data = resp.read()
                if len(data) > 10000:
                    asset_path.write_bytes(data)
        except Exception:
            pass

    if not asset_path.exists() or asset_path.stat().st_size < 5000:
        create_fallback_artwork(asset_path, filename.lower(), target_w, target_h)

    return Image.open(asset_path).convert("RGB")


# ==============================================================================
# 4. 시각 효과 유틸리티 (Ken Burns 줌/패닝, 황금 파티클, 둥근 캡션 박스, 외곽선 자막)
# ==============================================================================
def crop_ken_burns(img: Image.Image, target_w: int, target_h: int, progress: float, zoom_start: float = 1.0, zoom_end: float = 1.16, pan_x: float = 0.0, pan_y: float = 0.0) -> Image.Image:
    """
    정지된 이미지를 실제 카메라가 무빙하는 것처럼 부드럽게 줌인/패닝(Ken Burns 효과)합니다.
    """
    # 부드러운 S-커브 보간 (Smoothstep)
    p = progress * progress * (3.0 - 2.0 * progress)
    zoom = zoom_start + (zoom_end - zoom_start) * p

    src_w, src_h = img.size
    aspect_target = target_w / float(target_h)
    aspect_src = src_w / float(src_h)

    if aspect_src > aspect_target:
        base_h = src_h
        base_w = int(src_h * aspect_target)
    else:
        base_w = src_w
        base_h = int(src_w / aspect_target)

    crop_w = base_w / zoom
    crop_h = base_h / zoom

    max_dx = (src_w - crop_w) * 0.35
    max_dy = (src_h - crop_h) * 0.35

    cx = (src_w / 2.0) + max_dx * pan_x * (p - 0.5) * 2.0
    cy = (src_h / 2.0) + max_dy * pan_y * (p - 0.5) * 2.0

    x1 = max(0.0, min(src_w - crop_w, cx - crop_w / 2.0))
    y1 = max(0.0, min(src_h - crop_h, cy - crop_h / 2.0))

    return img.crop((x1, y1, x1 + crop_w, y1 + crop_h)).resize((target_w, target_h), Image.Resampling.BICUBIC)


class GoldenParticleSystem:
    """
    화면에 입체감과 생명력을 불어넣는 시네마틱 황금 빛 입자(Light Particles) 시스템
    """
    def __init__(self, count: int = 38, seed: int = 777):
        rng = np.random.default_rng(seed)
        self.x = rng.uniform(0, WIDTH, count)
        self.y = rng.uniform(0, HEIGHT, count)
        self.vx = rng.uniform(-18, 18, count)
        self.vy = rng.uniform(-55, -20, count)
        self.radius = rng.uniform(2.5, 7.5, count)
        self.phase = rng.uniform(0, 2 * np.pi, count)
        self.color_type = rng.integers(0, 2, count)

    def draw(self, overlay_draw: ImageDraw.ImageDraw, t: float):
        for i in range(len(self.x)):
            px = (self.x[i] + self.vx[i] * t + 15.0 * math.sin(t * 1.5 + self.phase[i])) % WIDTH
            py = (self.y[i] + self.vy[i] * t) % HEIGHT
            alpha = int(115 * (0.5 + 0.5 * math.sin(t * 3.2 + self.phase[i])))
            r = self.radius[i]
            if self.color_type[i] == 0:
                col = (255, 230, 140, alpha)
            else:
                col = (255, 250, 220, alpha)
            overlay_draw.ellipse((px - r, py - r, px + r, py + r), fill=col)


def draw_text_with_outline(
    draw: ImageDraw.ImageDraw,
    pos: tuple,
    text: str,
    font: ImageFont.FreeTypeFont,
    fill: tuple = (255, 255, 255, 255),
    outline_color: tuple = (0, 0, 0, 255),
    stroke_width: int = 6,
    shadow_offset: int = 4,
):
    x, y = pos
    if shadow_offset > 0:
        draw.text(
            (x + shadow_offset, y + shadow_offset),
            text,
            font=font,
            fill=(0, 0, 0, 180),
            stroke_width=stroke_width,
            stroke_fill=(0, 0, 0, 180),
        )
    draw.text(
        (x, y),
        text,
        font=font,
        fill=fill,
        stroke_width=stroke_width,
        stroke_fill=outline_color,
    )


# ==============================================================================
# 5. [모드 1] 썸네일 속 1억 뷰 스타일 — 상·하단 2분할 글로벌 AI 쇼츠 렌더러
# ==============================================================================
def render_split_screen_viral_shorts(
    output_mp4: Path,
    segments: list,
    center_pill_text: str = "Do you love Jesus?",
    voice: str = "en-US-ChristopherNeural",
):
    """
    머니멘터리 썸네일 속 노트북 화면을 100% 재현하고 업그레이드한 상·하단 2분할 바이럴 쇼츠 생성기
    - 상단(1080x960): 장엄한 천사 / 황금빛 하늘 구름 모션 씬 전환
    - 하단(1080x960): 시네마틱 예수님 포트레이트 (음성 에너지에 반응하는 성스러운 빛 효과 + 부드러운 줌)
    - 중앙(y=960): 썸네일과 동일한 라벤더/퍼플 알약 배너 ("Do you love Jesus?")
    - 하단부(y=1380~1680): 팝업 애니메이션 자막 + 조회수 1억 뷰급 리텐션 진행바
    """
    print(f"[1/4] AI 성우 음성 합성 중 ({voice})...")
    segs_audio = asyncio.run(synthesize_segments_tts(segments, voice=voice, rate="-5%", pitch="-2Hz"))

    final_wav = TEMP_DIR / "split_final_audio.wav"
    print("[2/4] 저작권 프리 천상의 앰비언트 BGM 생성 및 오디오 마스터링 중...")
    total_duration = merge_audio_with_bgm(segs_audio, mood="heavenly", final_audio_path=final_wav)
    total_frames = int(total_duration * FPS)

    print("[3/4] 고화질 AI 아트워크 로드 중...")
    img_angel = ensure_scene_image(
        "angel_top.png",
        "majestic angel with huge golden white feathered wings walking in desert mountain landscape at golden hour, 8k cinematic",
    )
    img_heaven = ensure_scene_image(
        "heaven_rays.png",
        "heavenly golden clouds parting with dramatic sunbeams god rays shining over valley, 8k cinematic",
    )
    img_jesus = ensure_scene_image(
        "jesus_bottom.png",
        "hyper-realistic compassionate portrait of Jesus looking at viewer, warm golden rim light, 8k",
    )

    top_images = [img_angel, img_heaven]
    particles = GoldenParticleSystem(count=42, seed=101)

    font_pill = get_font(FONT_KO_BOLD, 50)
    font_sub = get_font(FONT_KO_BOLD, 56)
    font_sub_hi = get_font(FONT_KO_BOLD, 62)
    font_badge = get_font(FONT_KO_BOLD, 30)

    print(f"[4/4] 1080x1920 Full HD 영상 프레임 렌더링 중 (총 {total_frames} 프레임, {total_duration:.1f}초)...")
    cmd = [
        FFMPEG_EXE, "-y",
        "-f", "rawvideo",
        "-vcodec", "rawvideo",
        "-s", f"{WIDTH}x{HEIGHT}",
        "-pix_fmt", "rgb24",
        "-r", str(FPS),
        "-i", "-",
        "-i", str(final_wav),
        "-c:v", "libx264",
        "-preset", "fast",
        "-crf", "18",
        "-pix_fmt", "yuv420p",
        "-c:a", "aac",
        "-b:a", "192k",
        "-shortest",
        "-movflags", "+faststart",
        str(output_mp4),
    ]
    proc = subprocess.Popen(cmd, stdin=subprocess.PIPE, stderr=subprocess.DEVNULL)

    half_h = HEIGHT // 2  # 960

    for frame_idx in range(total_frames):
        t = frame_idx / float(FPS)
        global_prog = frame_idx / float(max(1, total_frames - 1))

        # 현재 시간(t)에 해당하는 대본 세그먼트 찾기
        active_seg = segs_audio[-1]
        active_idx = len(segs_audio) - 1
        for s_i, seg in enumerate(segs_audio):
            if seg["start_time"] <= t <= seg["end_time"]:
                active_seg = seg
                active_idx = s_i
                break

        seg_prog = np.clip(
            (t - active_seg["start_time"]) / max(0.01, active_seg["duration"]),
            0.0,
            1.0,
        )

        # 음성 에너지 추출 (하단 인물 빛 오라 반응용)
        e_idx = min(int((t - active_seg["start_time"]) * FPS), len(active_seg["energies"]) - 1)
        voice_energy = active_seg["energies"][max(0, e_idx)] if active_seg["energies"] else 0.0

        # 1) 상단 프레임 (천사 / 천국 구름 교차 + Ken Burns 무빙)
        top_src = top_images[active_idx % len(top_images)]
        pan_dir = 1.0 if (active_idx % 2 == 0) else -1.0
        top_crop = crop_ken_burns(
            top_src,
            WIDTH,
            half_h,
            seg_prog,
            zoom_start=1.02,
            zoom_end=1.18,
            pan_x=0.4 * pan_dir,
            pan_y=-0.25,
        )

        # 2) 하단 프레임 (예수님 포트레이트 + 호흡 줌 + 음성 반응형 황금빛 밝기 강조)
        bot_zoom = 1.03 + 0.06 * math.sin(t * 0.9) + min(0.025, voice_energy * 0.12)
        bot_crop = crop_ken_burns(
            img_jesus,
            WIDTH,
            half_h,
            0.5,
            zoom_start=bot_zoom,
            zoom_end=bot_zoom,
            pan_x=0.0,
            pan_y=0.0,
        )
        if voice_energy > 0.02:
            enhancer = ImageEnhance.Brightness(bot_crop)
            bot_crop = enhancer.enhance(1.0 + min(0.18, voice_energy * 0.85))

        # 캔버스 병합
        canvas = Image.new("RGB", (WIDTH, HEIGHT))
        canvas.paste(top_crop, (0, 0))
        canvas.paste(bot_crop, (0, half_h))

        # 오버레이 레이어 (파티클, 구분선, 알약 배너, 자막)
        overlay = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
        odraw = ImageDraw.Draw(overlay)

        # 상·하단 경계 그라데이션 & 황금 파티클
        particles.draw(odraw, t)
        odraw.rectangle((0, half_h - 6, WIDTH, half_h + 6), fill=(255, 225, 160, 210))

        # 3) 썸네일 속 핵심 포인트: 중앙 라벤더/퍼플 알약 캡션 박스 ("Do you love Jesus?")
        pill_text = active_seg.get("pill_text", center_pill_text)
        bbox = odraw.textbbox((0, 0), pill_text, font=font_pill)
        tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
        pad_x, pad_y = 44, 20
        rx1 = (WIDTH - tw) // 2 - pad_x
        ry1 = half_h - (th // 2) - pad_y
        rx2 = (WIDTH + tw) // 2 + pad_x
        ry2 = half_h + (th // 2) + pad_y

        # 알약 그림자 + 라벤더 배경 (썸네일 속 #B39DDB 톤 재현)
        odraw.rounded_rectangle(
            (rx1 + 4, ry1 + 6, rx2 + 4, ry2 + 6),
            radius=28,
            fill=(0, 0, 0, 140),
        )
        odraw.rounded_rectangle(
            (rx1, ry1, rx2, ry2),
            radius=28,
            fill=(178, 152, 220, 245),
            outline=(255, 255, 255, 220),
            width=3,
        )
        draw_text_with_outline(
            odraw,
            ((WIDTH - tw) // 2, ry1 + pad_y - 4),
            pill_text,
            font_pill,
            fill=(255, 255, 255, 255),
            outline_color=(20, 10, 35, 255),
            stroke_width=5,
            shadow_offset=2,
        )

        # 4) 하단 팝업 애니메이션 자막 (문장 등장 시 통통 튀는 Pop-in 스케일 효과)
        pop_offset = int(max(0.0, (0.12 - seg_prog) / 0.12) * 28)
        sub_lines = active_seg["caption_lines"]
        base_y = 1490 + pop_offset

        # 자막 가독성을 위한 반투명 다크 백플레이트
        odraw.rounded_rectangle(
            (60, base_y - 30, WIDTH - 60, base_y + len(sub_lines) * 82 + 25),
            radius=24,
            fill=(10, 10, 18, 155),
        )

        for l_idx, line_info in enumerate(sub_lines):
            line_text = line_info["text"]
            is_highlight = line_info.get("highlight", False)
            f_use = font_sub_hi if is_highlight else font_sub
            col_use = (255, 230, 80, 255) if is_highlight else (255, 255, 255, 255)

            lb = odraw.textbbox((0, 0), line_text, font=f_use)
            lw = lb[2] - lb[0]
            lx = (WIDTH - lw) // 2
            ly = base_y + l_idx * 82

            draw_text_with_outline(
                odraw,
                (lx, ly),
                line_text,
                f_use,
                fill=col_use,
                outline_color=(0, 0, 0, 255),
                stroke_width=6,
                shadow_offset=4,
            )

        # 5) 상단 후킹 배지 & 하단 리텐션 진행바
        badge_txt = "★ WAIT TILL THE END (99% SCROLL PAST)"
        bb = odraw.textbbox((0, 0), badge_txt, font=font_badge)
        bw = bb[2] - bb[0]
        odraw.rounded_rectangle(
            ((WIDTH - bw) // 2 - 24, 58, (WIDTH + bw) // 2 + 24, 118),
            radius=20,
            fill=(0, 0, 0, 165),
            outline=(255, 215, 100, 200),
            width=2,
        )
        odraw.text(((WIDTH - bw) // 2, 70), badge_txt, font=font_badge, fill=(255, 235, 150, 255))

        # 하단 진행바
        bar_w = int(WIDTH * global_prog)
        odraw.rectangle((0, HEIGHT - 14, WIDTH, HEIGHT), fill=(255, 255, 255, 60))
        odraw.rectangle((0, HEIGHT - 14, bar_w, HEIGHT), fill=(255, 215, 60, 255))

        final_frame = Image.alpha_composite(canvas.convert("RGBA"), overlay).convert("RGB")
        proc.stdin.write(final_frame.tobytes())

    proc.stdin.close()
    proc.wait()
    print(f"✅ 글로벌 1억 뷰 스타일 쇼츠 생성 완료: {output_mp4}")


# ==============================================================================
# 6. [모드 2] 한국어 조회수 폭발 스타일 — 풀스크린 시네마틱 AI 쇼츠 렌더러
# ==============================================================================
def render_korea_viral_shorts(
    output_mp4: Path,
    segments: list,
    top_hook_title: str = "부자들이 절대 말 안 해주는 돈의 비밀",
    category_tag: str = "🔥 알고리즘 떡상 명언 · 부의 법칙",
    voice: str = "ko-KR-InJoonNeural",
):
    """
    국내 유튜브 쇼츠/인스타 릴스에서 조회수 수백만 회를 뽑는
    '다크 골드 시네마틱 + 굵은 핵심어 강조 자막 + 묵직한 AI 보이스' 쇼츠 생성기
    """
    print(f"[1/4] 한국어 신경망 AI 성우 음성 합성 중 ({voice})...")
    segs_audio = asyncio.run(synthesize_segments_tts(segments, voice=voice, rate="+8%", pitch="-3Hz"))

    final_wav = TEMP_DIR / "korea_final_audio.wav"
    print("[2/4] 다크 시네마틱 BGM 합성 및 오디오 마스터링 중...")
    total_duration = merge_audio_with_bgm(segs_audio, mood="dark_wealth", final_audio_path=final_wav)
    total_frames = int(total_duration * FPS)

    print("[3/4] 시네마틱 배경 아트워크 로드 중...")
    img_penthouse = ensure_scene_image(
        "seoul_penthouse.png",
        "mysterious successful figure in dark suit standing before floor-to-ceiling window overlooking rainy Seoul night skyline, 8k",
        1080, 1920,
    )
    img_heaven = ensure_scene_image(
        "heaven_rays.png",
        "dramatic golden sunbeams breaking through dark storm clouds over city skyline, cinematic 8k",
        1080, 1920,
    )
    img_angel = ensure_scene_image(
        "angel_top.png",
        "majestic golden figure standing on mountain peak at sunrise, epic cinematic 8k",
        1080, 1920,
    )
    bg_pool = [img_penthouse, img_heaven, img_angel]

    particles = GoldenParticleSystem(count=45, seed=2026)

    font_tag = get_font(FONT_KO_BOLD, 32)
    font_hook = get_font(FONT_KO_BOLD, 52)
    font_sub = get_font(FONT_KO_BOLD, 60)
    font_sub_hi = get_font(FONT_KO_BOLD, 68)

    print(f"[4/4] 1080x1920 한국어 바이럴 쇼츠 렌더링 중 (총 {total_frames} 프레임, {total_duration:.1f}초)...")
    cmd = [
        FFMPEG_EXE, "-y",
        "-f", "rawvideo",
        "-vcodec", "rawvideo",
        "-s", f"{WIDTH}x{HEIGHT}",
        "-pix_fmt", "rgb24",
        "-r", str(FPS),
        "-i", "-",
        "-i", str(final_wav),
        "-c:v", "libx264",
        "-preset", "fast",
        "-crf", "18",
        "-pix_fmt", "yuv420p",
        "-c:a", "aac",
        "-b:a", "192k",
        "-shortest",
        "-movflags", "+faststart",
        str(output_mp4),
    ]
    proc = subprocess.Popen(cmd, stdin=subprocess.PIPE, stderr=subprocess.DEVNULL)

    # 상단/하단 시네마틱 비네팅 마스크 미리 생성
    y_grid = np.linspace(0, 1, HEIGHT)[:, None]
    vignette_alpha = np.clip(
        np.where(y_grid < 0.25, (0.25 - y_grid) * 3.2, 0.0)
        + np.where(y_grid > 0.52, (y_grid - 0.52) * 1.65, 0.0),
        0.18,
        0.82,
    )
    vignette_arr = np.zeros((HEIGHT, WIDTH, 4), dtype=np.uint8)
    vignette_arr[..., 3] = (vignette_alpha * 255).astype(np.uint8)
    vignette_img = Image.fromarray(vignette_arr, mode="RGBA")

    for frame_idx in range(total_frames):
        t = frame_idx / float(FPS)
        global_prog = frame_idx / float(max(1, total_frames - 1))

        active_seg = segs_audio[-1]
        active_idx = len(segs_audio) - 1
        for s_i, seg in enumerate(segs_audio):
            if seg["start_time"] <= t <= seg["end_time"]:
                active_seg = seg
                active_idx = s_i
                break

        seg_prog = np.clip(
            (t - active_seg["start_time"]) / max(0.01, active_seg["duration"]),
            0.0,
            1.0,
        )

        src_bg = bg_pool[active_idx % len(bg_pool)]
        pan_dir = 1.0 if (active_idx % 2 == 0) else -1.0
        bg_frame = crop_ken_burns(
            src_bg,
            WIDTH,
            HEIGHT,
            seg_prog,
            zoom_start=1.03,
            zoom_end=1.20,
            pan_x=0.35 * pan_dir,
            pan_y=-0.20,
        )

        overlay = vignette_img.copy()
        odraw = ImageDraw.Draw(overlay)
        particles.draw(odraw, t)

        # 1) 상단 고정 후킹 헤더 (한국 쇼츠 특유의 상단 네온 제목 박스)
        tb = odraw.textbbox((0, 0), category_tag, font=font_tag)
        tw = tb[2] - tb[0]
        odraw.rounded_rectangle(
            ((WIDTH - tw) // 2 - 28, 110, (WIDTH + tw) // 2 + 28, 172),
            radius=30,
            fill=(255, 195, 0, 240),
        )
        odraw.text(((WIDTH - tw) // 2, 121), category_tag, font=font_tag, fill=(15, 15, 20, 255))

        hb = odraw.textbbox((0, 0), top_hook_title, font=font_hook)
        hw = hb[2] - hb[0]
        draw_text_with_outline(
            odraw,
            ((WIDTH - hw) // 2, 198),
            top_hook_title,
            font_hook,
            fill=(255, 255, 255, 255),
            outline_color=(0, 0, 0, 255),
            stroke_width=6,
            shadow_offset=4,
        )

        # 2) 중앙~하단 임팩트 팝업 자막
        pop_dy = int(max(0.0, (0.14 - seg_prog) / 0.14) * 32)
        sub_lines = active_seg["caption_lines"]
        center_y = 1180 + pop_dy

        odraw.rounded_rectangle(
            (55, center_y - 40, WIDTH - 55, center_y + len(sub_lines) * 98 + 35),
            radius=28,
            fill=(8, 10, 18, 175),
            outline=(255, 205, 70, 140),
            width=2,
        )

        for l_idx, line_info in enumerate(sub_lines):
            txt = line_info["text"]
            is_hi = line_info.get("highlight", False)
            f_use = font_sub_hi if is_hi else font_sub
            col = (255, 225, 45, 255) if is_hi else (255, 255, 255, 255)

            lb = odraw.textbbox((0, 0), txt, font=f_use)
            lw = lb[2] - lb[0]
            lx = (WIDTH - lw) // 2
            ly = center_y + l_idx * 96

            draw_text_with_outline(
                odraw,
                (lx, ly),
                txt,
                f_use,
                fill=col,
                outline_color=(0, 0, 0, 255),
                stroke_width=7,
                shadow_offset=5,
            )

        # 3) 장면 번호 인디케이터 & 하단 진행바
        step_txt = f"SCENE 0{active_idx + 1} / 0{len(segs_audio)}"
        sb = odraw.textbbox((0, 0), step_txt, font=font_tag)
        sw = sb[2] - sb[0]
        odraw.text(((WIDTH - sw) // 2, HEIGHT - 120), step_txt, font=font_tag, fill=(200, 205, 220, 200))

        bar_w = int(WIDTH * global_prog)
        odraw.rectangle((0, HEIGHT - 16, WIDTH, HEIGHT), fill=(255, 255, 255, 50))
        odraw.rectangle((0, HEIGHT - 16, bar_w, HEIGHT), fill=(255, 205, 0, 255))

        final_frame = Image.alpha_composite(bg_frame.convert("RGBA"), overlay).convert("RGB")
        proc.stdin.write(final_frame.tobytes())

    proc.stdin.close()
    proc.wait()
    print(f"✅ 한국어 조회수 폭발 스타일 쇼츠 생성 완료: {output_mp4}")


# ==============================================================================
# 7. 기본 내장 프리셋 시나리오 2종 (글로벌 1억 뷰 분할 쇼츠 + 한국형 부의 법칙 쇼츠)
# ==============================================================================
GLOBAL_SPLIT_PRESET = [
    {
        "tts_text": "Stop scrolling for just five seconds, my child.",
        "pill_text": "Do you love Jesus?",
        "caption_lines": [
            {"text": "STOP SCROLLING", "highlight": True},
            {"text": "FOR JUST 5 SECONDS...", "highlight": False},
        ],
    },
    {
        "tts_text": "This video did not find you by accident today.",
        "pill_text": "Do you love Jesus?",
        "caption_lines": [
            {"text": "THIS WAS NOT", "highlight": False},
            {"text": "AN ACCIDENT TODAY.", "highlight": True},
        ],
    },
    {
        "tts_text": "Every silent tear and heavy burden you carried is finally turning into a miracle.",
        "pill_text": "Type AMEN to claim ★",
        "caption_lines": [
            {"text": "EVERY SILENT TEAR", "highlight": False},
            {"text": "IS BECOMING A MIRACLE ★", "highlight": True},
        ],
    },
    {
        "tts_text": "Before midnight tonight, unexpected peace and blessings will knock on your door.",
        "pill_text": "Don't ignore this sign",
        "caption_lines": [
            {"text": "UNEXPECTED BLESSINGS", "highlight": True},
            {"text": "ARE AT YOUR DOOR.", "highlight": False},
        ],
    },
    {
        "tts_text": "If you believe and receive this blessing, share this with someone you love.",
        "pill_text": "Share & Be Blessed ♥",
        "caption_lines": [
            {"text": "CLAIM THIS BLESSING", "highlight": True},
            {"text": "& SHARE WITH LOVED ONES", "highlight": False},
        ],
    },
]

KOREA_VIRAL_PRESET = [
    {
        "tts_text": "프롬프트 단 한 줄로 매달 수천만 원을 버는 사람들이 절대 안 알려주는 비밀이 있습니다.",
        "caption_lines": [
            {"text": "프롬프트 단 한 줄로", "highlight": False},
            {"text": "월 수천만 원 버는 비밀", "highlight": True},
        ],
    },
    {
        "tts_text": "그들은 카메라를 들고 밖으로 나가 촬영하거나 밤새워 편집하지 않습니다.",
        "caption_lines": [
            {"text": "직접 촬영하지도 않고", "highlight": False},
            {"text": "밤새 편집하지도 않습니다", "highlight": True},
        ],
    },
    {
        "tts_text": "초반 3초 동안 시선을 멈추게 하는 강렬한 질문 하나와 AI 시각 효과만 결합했을 뿐입니다.",
        "caption_lines": [
            {"text": "초반 3초 시선 강탈 질문과", "highlight": True},
            {"text": "AI 시각 효과의 완벽한 결합", "highlight": False},
        ],
    },
    {
        "tts_text": "남들이 비싼 강의료를 내고 배울 때, 당신은 이 자동화 엔진으로 오늘 바로 시작할 수 있습니다.",
        "caption_lines": [
            {"text": "비싼 강의료 낼 필요 없이", "highlight": False},
            {"text": "지금 바로 자동화로 시작하세요!", "highlight": True},
        ],
    },
]


def build_custom_segments_from_topic(topic: str, lang: str = "ko") -> list:
    """
    사용자가 원하는 주제를 한 줄로 입력하면 즉시 4컷 쇼츠 대본과 자막 구조로 변환합니다.
    """
    if lang == "en":
        return [
            {
                "tts_text": f"Wait! Do not scroll past if you want to know the truth about {topic}.",
                "pill_text": topic[:26],
                "caption_lines": [
                    {"text": "DO NOT SCROLL PAST!", "highlight": True},
                    {"text": topic.upper()[:24], "highlight": False},
                ],
            },
            {
                "tts_text": f"99 percent of people completely miss this hidden secret about {topic}.",
                "pill_text": "99% Miss This Secret",
                "caption_lines": [
                    {"text": "99% OF PEOPLE MISS", "highlight": False},
                    {"text": "THIS HIDDEN SECRET", "highlight": True},
                ],
            },
            {
                "tts_text": "Once you apply this simple shift today, everything changes faster than you think.",
                "pill_text": "Watch What Happens ★",
                "caption_lines": [
                    {"text": "APPLY THIS TODAY", "highlight": True},
                    {"text": "& WATCH EVERYTHING CHANGE", "highlight": False},
                ],
            },
            {
                "tts_text": "Save this video right now so you never lose this powerful reminder.",
                "pill_text": "Save & Share ★",
                "caption_lines": [
                    {"text": "SAVE THIS VIDEO NOW", "highlight": True},
                    {"text": "BEFORE IT DISAPPEARS", "highlight": False},
                ],
            },
        ]
    else:
        return [
            {
                "tts_text": f"잠깐만요! {topic}, 아직도 남들 하는 대로 똑같이 하고 계신가요?",
                "caption_lines": [
                    {"text": f"★ {topic}", "highlight": True},
                    {"text": "아직도 모르고 계셨나요?", "highlight": False},
                ],
            },
            {
                "tts_text": f"상위 1퍼센트는 {topic}에서 가장 중요한 핵심 한 가지만 집중적으로 공략합니다.",
                "caption_lines": [
                    {"text": "상위 1%가 집중하는", "highlight": False},
                    {"text": "단 하나의 결정적 차이!", "highlight": True},
                ],
            },
            {
                "tts_text": "복잡한 과정은 전부 걷어내고 시스템이 알아서 일하게 만드는 것이 핵심입니다.",
                "caption_lines": [
                    {"text": "복잡한 노가다는 끝!", "highlight": True},
                    {"text": "시스템이 일하게 만드세요", "highlight": False},
                ],
            },
            {
                "tts_text": "나중에 다시 찾으려면 없으니 지금 바로 저장해 두고 오늘부터 실행해 보세요!",
                "caption_lines": [
                    {"text": "잊어버리기 전에 지금 바로", "highlight": False},
                    {"text": "저장 & 구독해 두세요 ★", "highlight": True},
                ],
            },
        ]


def main():
    parser = argparse.ArgumentParser(description="AI Viral Shorts Auto-Factory")
    parser.add_argument("--mode", choices=["all", "split", "korea", "custom"], default="all")
    parser.add_argument("--topic", type=str, default="")
    parser.add_argument("--lang", choices=["ko", "en"], default="ko")
    parser.add_argument("--layout", choices=["split", "full"], default="full")
    parser.add_argument("--out", type=str, default="")
    args = parser.parse_args()

    if args.mode in ("all", "split"):
        out_split = OUTPUT_DIR / "1_썸네일재현_글로벌1억뷰_분할쇼츠.mp4"
        render_split_screen_viral_shorts(
            output_mp4=out_split,
            segments=GLOBAL_SPLIT_PRESET,
            center_pill_text="Do you love Jesus?",
            voice="en-US-ChristopherNeural",
        )

    if args.mode in ("all", "korea"):
        out_korea = OUTPUT_DIR / "2_국내떡상스타일_부의법칙_AI쇼츠.mp4"
        render_korea_viral_shorts(
            output_mp4=out_korea,
            segments=KOREA_VIRAL_PRESET,
            top_hook_title="프롬프트 1줄로 월 수천 버는 법",
            category_tag="★ 머니멘터리 화제의 AI 쇼츠 재현",
            voice="ko-KR-InJoonNeural",
        )

    if args.mode == "custom" and args.topic:
        safe_name = "".join(c if c.isalnum() else "_" for c in args.topic)[:25]
        out_custom = Path(args.out) if args.out else (OUTPUT_DIR / f"custom_{safe_name}.mp4")
        segs = build_custom_segments_from_topic(args.topic, lang=args.lang)
        if args.layout == "split":
            voice = "en-US-ChristopherNeural" if args.lang == "en" else "ko-KR-InJoonNeural"
            render_split_screen_viral_shorts(
                output_mp4=out_custom,
                segments=segs,
                center_pill_text=args.topic[:24],
                voice=voice,
            )
        else:
            voice = "ko-KR-InJoonNeural" if args.lang == "ko" else "en-US-ChristopherNeural"
            render_korea_viral_shorts(
                output_mp4=out_custom,
                segments=segs,
                top_hook_title=args.topic[:18],
                category_tag="★ AI 원클릭 자동 생성 쇼츠",
                voice=voice,
            )


if __name__ == "__main__":
    main()
