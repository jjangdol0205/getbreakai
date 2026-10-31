# -*- coding: utf-8 -*-
"""
================================================================================
🎬 US Viral Shorts & Reels Pro Studio Engine (No-AI-Slop Edition)
================================================================================
미국 유튜브 쇼츠 & 인스타 릴스 인기 채널(Zack D. Films, Vox, MagnatesMedia,
Dark Luxury Listicle)의 실제 프리미어 프로 / 애프터이펙트 편집 기법을 구현한 스튜디오 엔진.

핵심 차별점 (왜 '싼티 나는 AI 느낌'이 전혀 없는가?):
1. [원테이크 자연 호흡 성우 + 단어 단위(WordBoundary) 0.01초 싱크]
   - 문장을 쪼개서 녹음하지 않고 전체 대본을 한 번의 호흡으로 녹음해 실제 다큐멘터리 내레이터 억양 구현
   - edge-tts의 WordBoundary 타임스탬프를 추출해 현재 발음 중인 단어만 색상이 바뀌며 커지는
     실제 미국 쇼츠 표준 'Active-Word Kinetic Caption' 구현 (촌스러운 반투명 자막 박스 제거)
2. [멀티 앵글 4컷 전환 + 핸드헬드 짐벌 흔들림 + 35mm 필름 그레인]
   - 사진 1장으로 버티지 않고 이야기 흐름에 맞춰 2.5~3.5초마다 4개의 카메라 샷 전환
   - 컷 전환 시 4프레임 휩(Whip) 줌 + 노출 플래시(Flash) + 컷 전환 효과음(Whoosh & Sub-Thud SFX) 동기화
   - 미세한 핸드헬드 카메라 호흡과 아날로그 35mm 필름 그레인을 입혀 인위적인 AI 광택 제거
3. [프로 사운드 디자인 (SFX + 로우패스 필터 스튜디오 BGM)]
   - 컷 전환마다 들어가는 시네마틱 우쉬(Whoosh), 심장박동 서브베이스(Heartbeat Sub),
     카메라 셔터/틱(Tick) 효과음과 로우패스 필터링된 다크 앰비언트 트랙 믹싱
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
from PIL import Image, ImageDraw, ImageFont, ImageEnhance, ImageFilter
import edge_tts
import edge_tts.communicate as _edge_comm
import imageio_ffmpeg

# Windows 시스템 루트 인증서 로드
try:
    _edge_comm._SSL_CTX.load_default_certs()
except Exception:
    pass

BASE_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = BASE_DIR / "ai_shorts_output"
ASSETS_DIR = OUTPUT_DIR / "assets"
TEMP_DIR = OUTPUT_DIR / "temp_us"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
ASSETS_DIR.mkdir(parents=True, exist_ok=True)
TEMP_DIR.mkdir(parents=True, exist_ok=True)

FFMPEG_EXE = imageio_ffmpeg.get_ffmpeg_exe()

WIDTH = 1080
HEIGHT = 1920
FPS = 30

FONT_IMPACT = r"C:\Windows\Fonts\impact.ttf"
FONT_ARIAL_BOLD = r"C:\Windows\Fonts\arialbd.ttf"
FONT_ARIAL_REG = r"C:\Windows\Fonts\arial.ttf"
FONT_SEGOE_BOLD = r"C:\Windows\Fonts\segoeuib.ttf"
FONT_SEGOE_REG = r"C:\Windows\Fonts\segoeui.ttf"


def load_font(path: str, size: int) -> ImageFont.FreeTypeFont:
    for candidate in [path, FONT_SEGOE_BOLD, FONT_ARIAL_BOLD]:
        if os.path.exists(candidate):
            return ImageFont.truetype(candidate, size)
    return ImageFont.load_default()


# ==============================================================================
# 1. 원테이크 자연 성우 합성 + 단어별(WordBoundary) 정밀 타임스탬프 추출
# ==============================================================================
async def synthesize_natural_voice_with_words(
    full_script: str,
    voice: str,
    out_mp3: Path,
    out_wav: Path,
    rate: str = "+4%",
    pitch: str = "+0Hz",
):
    """
    전체 스크립트를 끊지 않고 한 번에 합성하여 실제 사람처럼 자연스러운 억양을 만들고,
    동시에 모든 단어의 정확한 시작/종료 초(sec)를 추출합니다.
    """
    comm = edge_tts.Communicate(
        text=full_script,
        voice=voice,
        rate=rate,
        pitch=pitch,
        boundary="WordBoundary",
    )
    words = []
    with open(out_mp3, "wb") as audio_file:
        async for chunk in comm.stream():
            if chunk["type"] == "audio":
                audio_file.write(chunk["data"])
            elif chunk["type"] == "WordBoundary":
                w_text = chunk["text"].strip()
                start_s = chunk["offset"] / 1e7
                dur_s = max(0.08, chunk["duration"] / 1e7)
                if w_text:
                    words.append({
                        "word": w_text,
                        "start": start_s,
                        "end": start_s + dur_s,
                        "duration": dur_s,
                    })

    # 44.1kHz 스테레오 WAV 변환 + 끝에 0.45초 자연스러운 루프 여운 추가
    cmd = [
        FFMPEG_EXE, "-y",
        "-i", str(out_mp3),
        "-af", "apad=pad_dur=0.45",
        "-ar", "44100",
        "-ac", "2",
        str(out_wav),
    ]
    subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)

    with wave.open(str(out_wav), "rb") as wf:
        total_dur = wf.getnframes() / float(wf.getframerate())

    return words, total_dur


def group_words_into_phrases(words: list, max_words_per_group: int = 3, max_chars: int = 20) -> list:
    """
    단어 타임스탬프 리스트를 미국 쇼츠 표준인 2~3단어 묶음(Phrase Chunk)으로 그룹화합니다.
    구두점(., ?, !, —)이 나오면 즉시 구절을 끊어 호흡과 시각적 리듬을 일치시킵니다.
    """
    groups = []
    cur = []
    cur_chars = 0

    for w in words:
        token = w["word"]
        if cur and (len(cur) >= max_words_per_group or (cur_chars + len(token) > max_chars)):
            groups.append({
                "start": cur[0]["start"],
                "end": cur[-1]["end"],
                "words": cur,
            })
            cur = []
            cur_chars = 0

        cur.append(w)
        cur_chars += len(token) + 1

        if any(token.endswith(p) for p in [".", "?", "!", ",", ";", ":"]):
            groups.append({
                "start": cur[0]["start"],
                "end": cur[-1]["end"],
                "words": cur,
            })
            cur = []
            cur_chars = 0

    if cur:
        groups.append({
            "start": cur[0]["start"],
            "end": cur[-1]["end"],
            "words": cur,
        })

    # 구절 간 빈틈을 부드럽게 메워 자막이 깜빡거리지 않게 보정
    for i in range(len(groups) - 1):
        gap = groups[i + 1]["start"] - groups[i]["end"]
        if 0 < gap < 0.35:
            groups[i]["end"] = groups[i + 1]["start"]

    return groups


# ==============================================================================
# 2. 스튜디오 사운드 디자인 엔진 (컷 전환 SFX + 서브베이스 붐 + 다크 로파이 BGM)
# ==============================================================================
def build_studio_soundtrack(
    voice_wav: Path,
    cut_times: list,
    total_duration: float,
    style: str,
    final_wav: Path,
):
    """
    단순 전자음이 아닌, 로우패스 필터링된 따뜻한 다크 앰비언트 스튜디오 트랙과
    컷 전환 시점(cut_times)마다 정확히 터지는 시네마틱 우쉬(Whoosh) + 서브베이스 쿵(Thud) 효과음을 합성합니다.
    """
    sr = 44100
    total_samples = int(total_duration * sr)
    t = np.linspace(0, total_duration, total_samples, endpoint=False)
    rng = np.random.default_rng(42)

    left = np.zeros(total_samples, dtype=np.float64)
    right = np.zeros(total_samples, dtype=np.float64)

    if style == "science":
        # Zack D. Films / Vox 스타일: 긴장감 있는 펄스 베이스 + 미니멀 시네마틱 틱(Tick) 리듬
        notes = [110.0, 130.81, 98.0, 123.47]  # A2 -> C3 -> G2 -> B2
        beat_hz = 2.0  # 120 BPM
    elif style == "reels_luxury":
        # 미국 다크 럭셔리 인스타 릴스: 묵직하고 몽환적인 슬로우 드레이크/위켄드 스타일 R&B 패드 + 서브베이스
        notes = [92.50, 110.0, 73.42, 82.41]  # F#2 -> A2 -> D2 -> E2
        beat_hz = 1.4
    else:
        # 넷플릭스/리들리 스콧 역사 다큐: 웅장한 저음 첼로/호른 드론 + 북소리 울림
        notes = [73.42, 87.31, 65.41, 82.41]  # D2 -> F2 -> C2 -> E2
        beat_hz = 1.25

    sec_per_note = total_duration / len(notes)
    for idx, f0 in enumerate(notes):
        s_t = idx * sec_per_note
        e_t = (idx + 1) * sec_per_note
        env = np.clip((t - s_t) / 0.8, 0, 1) * np.clip((e_t - t) / 0.8, 0, 1)
        # 따뜻한 아날로그 패드 (기본음 + 5도 + 옥타브)
        pad_l = (
            0.55 * np.sin(2 * np.pi * f0 * t)
            + 0.30 * np.sin(2 * np.pi * (f0 * 1.498) * t + 0.3)
            + 0.15 * np.sin(2 * np.pi * (f0 * 2.0) * t + 0.7)
        )
        pad_r = (
            0.55 * np.sin(2 * np.pi * (f0 * 1.002) * t + 0.5)
            + 0.30 * np.sin(2 * np.pi * (f0 * 1.501) * t + 1.1)
            + 0.15 * np.sin(2 * np.pi * (f0 * 2.0) * t + 0.2)
        )
        left += 0.24 * pad_l * env
        right += 0.24 * pad_r * env

    # 부드러운 심장박동 서브베이스 펄스 (60Hz~80Hz)
    beat_phase = (t * beat_hz) % 1.0
    kick_env = np.exp(-beat_phase * 7.5)
    kick_freq = 55.0 + 35.0 * np.exp(-beat_phase * 18.0)
    kick = 0.22 * np.sin(2 * np.pi * kick_freq * t) * kick_env
    left += kick
    right += kick

    # 과학 다큐용 정밀 시계 초침 Tick 사운드 (집중력 상승 효과)
    if style == "science":
        tick_phase = (t * 2.0) % 1.0
        tick_env = np.exp(-tick_phase * 65.0)
        noise_tick = rng.normal(0, 1, total_samples) * tick_env * 0.045
        left += noise_tick * 0.8
        right += noise_tick * 1.0

    # --- 컷 전환 시점(cut_times)마다 시네마틱 Whoosh + Sub-Impact 효과음 삽입 ---
    # 0.0초 시작 훅(Hook) 임팩트 포함
    all_impacts = [0.02] + list(cut_times)
    for c_t in all_impacts:
        idx_center = int(c_t * sr)
        win = int(0.38 * sr)
        i_start = max(0, idx_center - win // 2)
        i_end = min(total_samples, idx_center + win // 2)
        if i_end <= i_start:
            continue
        local_t = np.linspace(-0.19, 0.19, i_end - i_start)
        # 가우시안 엔벨로프 우쉬(Filtered Noise Sweep) + 저음 쿵(Sub Thump)
        w_env = np.exp(-(local_t / 0.075) ** 2)
        sub_thump = 0.38 * np.sin(2 * np.pi * (85.0 - 140.0 * local_t) * (local_t + 0.2)) * w_env
        whoosh_noise = rng.normal(0, 1, i_end - i_start) * w_env * 0.12
        # 간단한 이동평균 로우패스 필터로 부드러운 바람 소리로 변환
        kernel = np.ones(18) / 18.0
        whoosh_smooth = np.convolve(whoosh_noise, kernel, mode="same")
        # 좌->우 패닝 효과
        pan = np.linspace(0.2, 0.8, i_end - i_start)
        left[i_start:i_end] += sub_thump + whoosh_smooth * (1.0 - pan)
        right[i_start:i_end] += sub_thump + whoosh_smooth * pan

    # 전체 페이드 인/아웃
    fade = np.clip(t / 0.25, 0, 1) * np.clip((total_duration - t) / 0.65, 0, 1)
    left *= fade
    right *= fade

    # 성우 음성과 믹싱 (성우가 말할 때 BGM이 자연스럽게 깔리는 스튜디오 밸런스)
    if voice_wav and voice_wav.exists():
        with wave.open(str(voice_wav), "rb") as wf:
            v_raw = wf.readframes(wf.getnframes())
            v_arr = np.frombuffer(v_raw, dtype=np.int16).reshape(-1, 2).astype(np.float64) / 32768.0
        m_len = min(total_samples, len(v_arr))
        # 성우 에너지가 높은 구간에서 BGM 자동 덕킹(Sidechain Ducking)
        v_mono = np.abs(v_arr[:m_len, 0])
        duck_kernel = np.ones(int(sr * 0.15)) / float(int(sr * 0.15))
        v_env = np.convolve(v_mono, duck_kernel, mode="same")
        bgm_gain = np.clip(0.68 - v_env * 1.4, 0.32, 0.68)

        final_l = v_arr[:m_len, 0] * 1.18 + left[:m_len] * bgm_gain
        final_r = v_arr[:m_len, 1] * 1.18 + right[:m_len] * bgm_gain
    else:
        final_l = left * 0.85
        final_r = right * 0.85

    stereo = np.vstack((final_l, final_r)).T
    stereo = np.clip(stereo, -0.98, 0.98)
    pcm = (stereo * 32767).astype(np.int16)

    with wave.open(str(final_wav), "wb") as wf:
        wf.setnchannels(2)
        wf.setsampwidth(2)
        wf.setframerate(sr)
        wf.writeframes(pcm.tobytes())


# ==============================================================================
# 3. 프로 카메라 워크 (핸드헬드 짐벌 무빙 + 컷 전환 휩/플래시 + 35mm 필름 그레인)
# ==============================================================================
def render_camera_motion(
    img: Image.Image,
    t_local: float,
    shot_dur: float,
    shot_idx: int,
    whip_intensity: float = 0.0,
) -> Image.Image:
    """
    단순 직선 줌이 아니라 실제 카메라맨이 짐벌을 들고 찍은 듯한 미세한 핸드헬드 호흡과
    컷 전환 직후 0.12초간의 광학 휩(Whip Zoom) 효과를 적용합니다.
    """
    prog = np.clip(t_local / max(0.01, shot_dur), 0.0, 1.0)
    # 샷마다 줌인 / 줌아웃 교차로 역동성 부여
    if shot_idx % 2 == 0:
        base_zoom = 1.04 + 0.11 * (prog * prog * (3 - 2 * prog))
    else:
        base_zoom = 1.15 - 0.10 * (prog * prog * (3 - 2 * prog))

    # 컷 전환 순간의 빠른 카메라 휩(Whip) 줌인 보정
    zoom = base_zoom + whip_intensity * 0.09

    src_w, src_h = img.size
    aspect_target = WIDTH / float(HEIGHT)
    aspect_src = src_w / float(src_h)

    if aspect_src > aspect_target:
        base_h = src_h
        base_w = int(src_h * aspect_target)
    else:
        base_w = src_w
        base_h = int(src_w / aspect_target)

    crop_w = base_w / zoom
    crop_h = base_h / zoom

    # 유기적인 핸드헬드 카메라 드리프트 (사인파 합성)
    sway_x = math.sin(t_local * 1.8 + shot_idx * 1.7) * 18.0 + math.cos(t_local * 0.9) * 10.0
    sway_y = math.cos(t_local * 1.4 + shot_idx * 2.3) * 14.0

    cx = (src_w / 2.0) + sway_x
    cy = (src_h / 2.0) + sway_y

    x1 = max(0.0, min(src_w - crop_w, cx - crop_w / 2.0))
    y1 = max(0.0, min(src_h - crop_h, cy - crop_h / 2.0))

    frame = img.crop((x1, y1, x1 + crop_w, y1 + crop_h)).resize((WIDTH, HEIGHT), Image.Resampling.BICUBIC)

    # 컷 전환 순간(whip_intensity > 0) 미세한 시네마틱 노출 플래시 효과
    if whip_intensity > 0.05:
        enhancer = ImageEnhance.Brightness(frame)
        frame = enhancer.enhance(1.0 + whip_intensity * 0.28)

    return frame


# 미리 생성해 두는 35mm 아날로그 필름 그레인 & 광학 비네팅 텍스처 (AI 플라스틱 느낌 제거용)
_GRAIN_FRAMES = []


def init_film_grain_cache(num_frames: int = 12):
    global _GRAIN_FRAMES
    if _GRAIN_FRAMES:
        return
    rng = np.random.default_rng(1999)
    y_g = np.linspace(-1, 1, HEIGHT)[:, None]
    x_g = np.linspace(-1, 1, WIDTH)[None, :]
    rad = np.sqrt(x_g ** 2 + y_g ** 2)
    vig = np.clip(1.0 - 0.32 * (rad ** 2.2), 0.55, 1.0)
    # 하단 자막 영역(y > 0.45) 자연스러운 다크 그라데이션
    bottom_shade = np.where(y_g > 0.25, np.clip(1.0 - (y_g - 0.25) * 0.55, 0.42, 1.0), 1.0)
    combined_mask = (vig * bottom_shade)[..., None]

    for _ in range(num_frames):
        noise = rng.normal(0.0, 5.5, (HEIGHT // 2, WIDTH // 2, 1)).astype(np.float32)
        noise_full = np.repeat(np.repeat(noise, 2, axis=0), 2, axis=1)
        _GRAIN_FRAMES.append((combined_mask, noise_full))


def apply_film_look(frame_rgb: Image.Image, frame_idx: int) -> Image.Image:
    init_film_grain_cache()
    mask, grain = _GRAIN_FRAMES[frame_idx % len(_GRAIN_FRAMES)]
    arr = np.asarray(frame_rgb, dtype=np.float32)
    arr = arr * mask + grain
    arr = np.clip(arr, 0, 255).astype(np.uint8)
    return Image.fromarray(arr, mode="RGB")


# ==============================================================================
# 4. 미국 쇼츠 표준 'Active-Word Kinetic Caption' 렌더러 (박스 없는 단어별 팝업 자막)
# ==============================================================================
def draw_active_word_captions(
    overlay_draw: ImageDraw.ImageDraw,
    phrase_groups: list,
    t: float,
    accent_color: tuple = (0, 245, 212, 255),
    danger_words: set = None,
    y_pos: int = 1380,
):
    """
    현재 시점(t)에 발화 중인 2~3단어 구절을 화면 중앙 하단에 표시하되,
    지금 이 순간 발음되고 있는 '단어(Active Word)'만 색상이 켜지고 살짝 위로 팝업되도록 렌더링합니다.
    """
    if danger_words is None:
        danger_words = {"toxic", "shrinks", "plaque", "damage", "deadly", "die", "stop", "never", "illegal", "survive", "blood", "poison"}

    active_group = None
    for g in phrase_groups:
        if g["start"] - 0.06 <= t <= g["end"] + 0.08:
            active_group = g
            break

    if not active_group:
        return

    font_normal = load_font(FONT_ARIAL_BOLD, 68)
    font_active = load_font(FONT_ARIAL_BOLD, 74)

    words = active_group["words"]
    # 구절 등장 첫 0.08초 동안 전체 구절이 살짝 떠오르는 모션
    group_age = max(0.0, t - active_group["start"])
    pop_y = int(max(0.0, (0.08 - group_age) / 0.08) * 20)

    # 각 단어 폭 계산하여 중앙 정렬 배치
    word_metrics = []
    space_w = 22
    total_w = 0

    for w_info in words:
        is_speaking = (w_info["start"] - 0.04 <= t <= w_info["end"] + 0.04)
        f_use = font_active if is_speaking else font_normal
        disp_text = w_info["word"].upper()
        bbox = overlay_draw.textbbox((0, 0), disp_text, font=f_use)
        ww = bbox[2] - bbox[0]
        wh = bbox[3] - bbox[1]
        word_metrics.append((disp_text, is_speaking, f_use, ww, wh))
        total_w += ww

    total_w += space_w * max(0, len(words) - 1)

    # 만약 폭이 940px을 넘으면 2줄로 자동 분할
    if total_w > 940 and len(word_metrics) >= 3:
        rows = [word_metrics[:2], word_metrics[2:]]
    else:
        rows = [word_metrics]

    for r_idx, row in enumerate(rows):
        row_w = sum(m[3] for m in row) + space_w * max(0, len(row) - 1)
        cur_x = (WIDTH - row_w) // 2
        cur_y = y_pos + pop_y + r_idx * 92

        for disp_text, is_speaking, f_use, ww, wh in row:
            clean_w = disp_text.strip(".,?!:;\"'").lower()
            if is_speaking:
                if clean_w in danger_words:
                    fill_col = (255, 65, 85, 255)  # 강렬한 경고 레드
                else:
                    fill_col = accent_color
                wy = cur_y - 6
            else:
                fill_col = (255, 255, 255, 255)
                wy = cur_y

            # 1) 깊은 드롭 섀도우 (배경 박스 없이도 어떤 영상 위에서든 100% 읽히게 함)
            overlay_draw.text(
                (cur_x + 5, wy + 7),
                disp_text,
                font=f_use,
                fill=(0, 0, 0, 210),
                stroke_width=10,
                stroke_fill=(0, 0, 0, 210),
            )
            # 2) 선명한 본문 + 블랙 아웃라인
            overlay_draw.text(
                (cur_x, wy),
                disp_text,
                font=f_use,
                fill=fill_col,
                stroke_width=8,
                stroke_fill=(10, 12, 16, 255),
            )
            cur_x += ww + space_w


# ==============================================================================
# 5. [영상 1] 미국 유튜브 1위: 3D 인체·뇌과학 다큐 쇼츠 (Zack D. Films / Vox 스타일)
# ==============================================================================
def build_video_1_body_science():
    print("\n============================================================")
    print("🎬 [1/3] 미국 유튜브 1위: 3D 인체·뇌과학 호기심 쇼츠 제작 시작")
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

    # 4개의 멀티 카메라 샷 로드
    shots = [
        Image.open(ASSETS_DIR / "v1_shot1_eye.jpg").convert("RGB"),
        Image.open(ASSETS_DIR / "v1_shot2_brain_scan.jpg").convert("RGB"),
        Image.open(ASSETS_DIR / "v1_shot3_neurons.jpg").convert("RGB"),
        Image.open(ASSETS_DIR / "v1_shot4_mri.jpg").convert("RGB"),
    ]
    shot_labels = [
        ("STAGE 01 // 03:00 AM", "SLEEP DEPRIVATION ONSET"),
        ("STAGE 02 // NEURAL CORTEX", "METABOLIC TOXIN BUILDUP"),
        ("STAGE 03 // SYNAPSE LEVEL", "MICROGLIAL CELL OVERDRIVE"),
        ("STAGE 04 // CLINICAL MRI", "-40% MEMORY CAPACITY"),
    ]

    # 컷 전환 시점 계산 (4등분)
    shot_dur = total_dur / 4.0
    cut_times = [shot_dur * 1, shot_dur * 2, shot_dur * 3]

    final_audio = TEMP_DIR / "v1_master.wav"
    build_studio_soundtrack(wav_path, cut_times, total_dur, style="science", final_wav=final_audio)

    out_mp4 = OUTPUT_DIR / "US_1_BodyScience_BrainSleep_Shorts.mp4"
    total_frames = int(total_dur * FPS)

    font_hud_sm = load_font(FONT_SEGOE_BOLD, 26)
    font_hud_lg = load_font(FONT_SEGOE_BOLD, 34)

    cmd = [
        FFMPEG_EXE, "-y",
        "-f", "rawvideo", "-vcodec", "rawvideo",
        "-s", f"{WIDTH}x{HEIGHT}", "-pix_fmt", "rgb24", "-r", str(FPS),
        "-i", "-", "-i", str(final_audio),
        "-c:v", "libx264", "-preset", "fast", "-crf", "23",
        "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k",
        "-shortest", "-movflags", "+faststart", str(out_mp4),
    ]
    proc = subprocess.Popen(cmd, stdin=subprocess.PIPE, stderr=subprocess.DEVNULL)

    for f_idx in range(total_frames):
        t = f_idx / float(FPS)
        shot_idx = min(3, int(t / shot_dur))
        t_local = t - (shot_idx * shot_dur)

        # 컷 전환 직후 0.14초 동안 카메라 휩(Whip) 모션
        whip = max(0.0, (0.14 - t_local) / 0.14) if shot_idx > 0 else 0.0

        base_frame = render_camera_motion(shots[shot_idx], t_local, shot_dur, shot_idx, whip_intensity=whip)
        filmic_frame = apply_film_look(base_frame, f_idx)

        overlay = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
        odraw = ImageDraw.Draw(overlay)

        # 다큐멘터리 미니멀 메디컬 HUD (왼쪽 상단 깔끔한 텔레메트리만 표시)
        tag_top, tag_main = shot_labels[shot_idx]
        odraw.rounded_rectangle((64, 96, 560, 198), radius=14, fill=(8, 14, 24, 165), outline=(0, 245, 212, 110), width=2)
        odraw.ellipse((88, 118, 102, 132), fill=(0, 245, 212, 255))
        odraw.text((116, 109), tag_top, font=font_hud_sm, fill=(0, 245, 212, 230))
        odraw.text((88, 144), tag_main, font=font_hud_lg, fill=(245, 250, 255, 255))

        # 단어별 Active-Word Kinetic Captions
        draw_active_word_captions(
            odraw,
            phrases,
            t,
            accent_color=(0, 245, 212, 255),
            y_pos=1390,
        )

        # 하단 얇은 시안 진행바 (4px)
        prog_w = int(WIDTH * (f_idx / float(max(1, total_frames - 1))))
        odraw.rectangle((0, HEIGHT - 8, prog_w, HEIGHT), fill=(0, 245, 212, 230))

        comp = Image.alpha_composite(filmic_frame.convert("RGBA"), overlay).convert("RGB")
        proc.stdin.write(comp.tobytes())

    proc.stdin.close()
    proc.wait()
    print(f"✅ [완료] {out_mp4} ({total_dur:.1f}초)")


# ==============================================================================
# 6. [영상 2] 미국 인스타 릴스 1위: '저장 폭탄' 다크 럭셔리 리스트 릴스
# ==============================================================================
def build_video_2_insta_reels_listicle():
    print("\n============================================================")
    print("📸 [2/3] 미국 인스타 릴스 1위: 다크 럭셔리 '저장 폭탄' 리스트 릴스 제작 시작")
    print("============================================================")

    # 미국 인스타 릴스 특유의 짧은 감성 훅 보이스 + 11.5초 무한 루프 구성
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
    # 릴스 최적 길이 11.0초 보장 (음성이 끝난 뒤에도 리스트를 읽느라 자동 루프되도록 설계)
    total_dur = max(11.0, voice_dur + 3.8)
    cut_time = total_dur * 0.52

    # 음성 WAV 뒤에 무음을 붙여 total_dur 길이로 맞춤
    padded_wav = TEMP_DIR / "v2_voice_padded.wav"
    subprocess.run(
        [
            FFMPEG_EXE, "-y", "-i", str(wav_path),
            "-af", f"apad=whole_dur={total_dur}",
            "-ar", "44100", "-ac", "2", str(padded_wav),
        ],
        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True,
    )

    final_audio = TEMP_DIR / "v2_master.wav"
    build_studio_soundtrack(padded_wav, [cut_time], total_dur, style="reels_luxury", final_wav=final_audio)

    shots = [
        Image.open(ASSETS_DIR / "v2_shot1_porsche_rain.jpg").convert("RGB"),
        Image.open(ASSETS_DIR / "v2_shot2_macbook_desk.jpg").convert("RGB"),
    ]

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
    total_frames = int(total_dur * FPS)

    cmd = [
        FFMPEG_EXE, "-y",
        "-f", "rawvideo", "-vcodec", "rawvideo",
        "-s", f"{WIDTH}x{HEIGHT}", "-pix_fmt", "rgb24", "-r", str(FPS),
        "-i", "-", "-i", str(final_audio),
        "-c:v", "libx264", "-preset", "fast", "-crf", "23",
        "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k",
        "-shortest", "-movflags", "+faststart", str(out_mp4),
    ]
    proc = subprocess.Popen(cmd, stdin=subprocess.PIPE, stderr=subprocess.DEVNULL)

    for f_idx in range(total_frames):
        t = f_idx / float(FPS)
        if t < cut_time:
            shot_idx = 0
            t_local = t
            s_dur = cut_time
            whip = 0.0
        else:
            shot_idx = 1
            t_local = t - cut_time
            s_dur = total_dur - cut_time
            whip = max(0.0, (0.15 - t_local) / 0.15)

        base_frame = render_camera_motion(shots[shot_idx], t_local, s_dur, shot_idx, whip_intensity=whip)
        # 다크 에스테틱 무드를 위해 배경 밝기를 살짝 낮추고 대비를 높임
        base_frame = ImageEnhance.Brightness(base_frame).enhance(0.76)
        filmic_frame = apply_film_look(base_frame, f_idx)

        overlay = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
        odraw = ImageDraw.Draw(overlay)

        # 상단 애플 에디토리얼 스타일 헤더
        odraw.rounded_rectangle((90, 240, 440, 294), radius=27, fill=(255, 255, 255, 32), outline=(255, 255, 255, 85), width=1)
        odraw.text((118, 252), "BOOKMARK THIS FOR LATER", font=font_header_tag, fill=(235, 240, 245, 240))

        draw_title_1 = "5 Websites So Powerful They"
        draw_title_2 = "Feel Illegal to Know (2026)"
        odraw.text((92, 322), draw_title_1, font=font_title, fill=(255, 255, 255, 255), stroke_width=2, stroke_fill=(0, 0, 0, 180))
        odraw.text((92, 382), draw_title_2, font=font_title, fill=(255, 218, 120, 255), stroke_width=2, stroke_fill=(0, 0, 0, 180))

        # 중앙 글래스모피즘(Glassmorphism) 리스트 카드 5종 (0.4초 간격으로 순차 슬라이드 인)
        card_start_y = 495
        card_h = 162
        card_gap = 22

        for idx, (num_str, site_name, site_desc) in enumerate(list_items):
            appear_t = 0.25 + idx * 0.42
            if t < appear_t:
                continue
            item_prog = min(1.0, (t - appear_t) / 0.28)
            ease = 1.0 - (1.0 - item_prog) ** 3
            slide_dy = int((1.0 - ease) * 35)
            alpha_card = int(205 * ease)
            alpha_txt = int(255 * ease)

            cy1 = card_start_y + idx * (card_h + card_gap) + slide_dy
            cy2 = cy1 + card_h

            # 반투명 다크 프로스트 글래스 카드
            odraw.rounded_rectangle(
                (84, cy1, WIDTH - 84, cy2),
                radius=24,
                fill=(14, 17, 24, alpha_card),
                outline=(255, 255, 255, int(65 * ease)),
                width=2,
            )
            # 번호 뱃지
            odraw.rounded_rectangle(
                (112, cy1 + 32, 176, cy1 + 92),
                radius=16,
                fill=(255, 215, 110, int(38 * ease)),
                outline=(255, 215, 110, int(140 * ease)),
                width=1,
            )
            odraw.text((126, cy1 + 44), num_str, font=font_num, fill=(255, 220, 130, alpha_txt))
            odraw.text((202, cy1 + 28), site_name, font=font_site, fill=(255, 255, 255, alpha_txt))
            odraw.text((202, cy1 + 84), site_desc, font=font_desc, fill=(195, 205, 218, alpha_txt))

        # 하단 미국 릴스 ManyChat 자동 DM 수익화 퍼널 배너
        cta_box_y = 1495
        odraw.rounded_rectangle(
            (84, cta_box_y, WIDTH - 84, cta_box_y + 104),
            radius=52,
            fill=(255, 255, 255, 238),
        )
        cta_txt = 'Comment "LIST" & I\'ll DM you all 5 links'
        cb = odraw.textbbox((0, 0), cta_txt, font=font_cta)
        cw = cb[2] - cb[0]
        odraw.text(((WIDTH - cw) // 2, cta_box_y + 32), cta_txt, font=font_cta, fill=(12, 14, 18, 255))

        comp = Image.alpha_composite(filmic_frame.convert("RGBA"), overlay).convert("RGB")
        proc.stdin.write(comp.tobytes())

    proc.stdin.close()
    proc.wait()
    print(f"✅ [완료] {out_mp4} ({total_dur:.1f}초)")


# ==============================================================================
# 7. [영상 3] 미국 역사·미스터리 'What-If' 다큐 쇼츠 (Ridley Scott 영화 질감)
# ==============================================================================
def build_video_3_history_whatif():
    print("\n============================================================")
    print("🏛️ [3/3] 미국 역사 'What-If' 다큐 쇼츠 제작 시작")
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

    shots = [
        Image.open(ASSETS_DIR / "v3_shot1_rome_street.jpg").convert("RGB"),
        Image.open(ASSETS_DIR / "v3_shot2_roman_coins.jpg").convert("RGB"),
        Image.open(ASSETS_DIR / "v3_shot3_thermae_bath.jpg").convert("RGB"),
        Image.open(ASSETS_DIR / "v3_shot4_colosseum_dusk.jpg").convert("RGB"),
    ]
    chapter_titles = [
        ("06:00 AM // SUBURA DISTRICT", "1,000,000 CITIZENS AWAKEN"),
        ("11:00 AM // ROMAN MEDICINE", "THE GLADIATOR SWEAT CURE"),
        ("03:00 PM // PUBLIC BATHS", "ANCIENT HYGIENE SECRETS"),
        ("11:00 PM // NIGHTFALL IN ROME", "PRIVATE FIRE BRIGADES"),
    ]

    shot_dur = total_dur / 4.0
    cut_times = [shot_dur * 1, shot_dur * 2, shot_dur * 3]

    final_audio = TEMP_DIR / "v3_master.wav"
    build_studio_soundtrack(wav_path, cut_times, total_dur, style="history", final_wav=final_audio)

    out_mp4 = OUTPUT_DIR / "US_3_History_SurviveAncientRome_Shorts.mp4"
    total_frames = int(total_dur * FPS)

    font_ch_sm = load_font(FONT_SEGOE_BOLD, 25)
    font_ch_lg = load_font(FONT_SEGOE_BOLD, 33)

    cmd = [
        FFMPEG_EXE, "-y",
        "-f", "rawvideo", "-vcodec", "rawvideo",
        "-s", f"{WIDTH}x{HEIGHT}", "-pix_fmt", "rgb24", "-r", str(FPS),
        "-i", "-", "-i", str(final_audio),
        "-c:v", "libx264", "-preset", "fast", "-crf", "23",
        "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k",
        "-shortest", "-movflags", "+faststart", str(out_mp4),
    ]
    proc = subprocess.Popen(cmd, stdin=subprocess.PIPE, stderr=subprocess.DEVNULL)

    for f_idx in range(total_frames):
        t = f_idx / float(FPS)
        shot_idx = min(3, int(t / shot_dur))
        t_local = t - (shot_idx * shot_dur)
        whip = max(0.0, (0.14 - t_local) / 0.14) if shot_idx > 0 else 0.0

        base_frame = render_camera_motion(shots[shot_idx], t_local, shot_dur, shot_idx, whip_intensity=whip)
        filmic_frame = apply_film_look(base_frame, f_idx)

        overlay = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
        odraw = ImageDraw.Draw(overlay)

        # 넷플릭스 다큐멘터리 스타일 상단 타임스탬프 캡션
        c_top, c_main = chapter_titles[shot_idx]
        odraw.rounded_rectangle((64, 96, 595, 198), radius=14, fill=(18, 14, 10, 175), outline=(255, 200, 110, 120), width=2)
        odraw.text((92, 109), c_top, font=font_ch_sm, fill=(255, 205, 115, 235))
        odraw.text((92, 144), c_main, font=font_ch_lg, fill=(255, 250, 240, 255))

        # 단어별 Active-Word Kinetic Captions (시네마 골드 하이라이트)
        draw_active_word_captions(
            odraw,
            phrases,
            t,
            accent_color=(255, 214, 60, 255),
            y_pos=1390,
        )

        prog_w = int(WIDTH * (f_idx / float(max(1, total_frames - 1))))
        odraw.rectangle((0, HEIGHT - 8, prog_w, HEIGHT), fill=(255, 205, 90, 230))

        comp = Image.alpha_composite(filmic_frame.convert("RGBA"), overlay).convert("RGB")
        proc.stdin.write(comp.tobytes())

    proc.stdin.close()
    proc.wait()
    print(f"✅ [완료] {out_mp4} ({total_dur:.1f}초)")


if __name__ == "__main__":
    build_video_1_body_science()
    build_video_2_insta_reels_listicle()
    build_video_3_history_whatif()
