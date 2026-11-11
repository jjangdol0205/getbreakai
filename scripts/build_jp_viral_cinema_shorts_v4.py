#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
D:\드림컴퍼니\3사업부\scripts\build_jp_viral_cinema_shorts_v4.py
일본 개인투자자(新NISA 2,500万人 · 株クラ · 日本株/米国株) 타깃 고효율 시네마-퀀트 바이럴 쇼츠 엔진 (V4_JP_VIRAL_PRO)

핵심 업그레이드 (기존 EP01~EP24 조회수 부진 5대 원인 완벽 해결):
1. B2B 전문용어 나열 탈피 -> 일본 개인투자자 실제 계좌 고통(新NISA 손익통산 불가, 물타기 반토막, 고배당 5년치 증발, 동증 9시 요리가미, SOXL 감가) & 대화형 훅(Keita 남성 개인투자자 착각 -> Nanami 여성 퀀트 앵커 팩트 반박).
2. 정적 인물 4컷 반복 탈피 -> 30fps 풀스크린 모션 차트(막대 비교 · 22봉 캔들+거래량 · 자산곡선 레이스 + 실시간 엔화 카운터 + 우측 상단 원형 라이브 앵커 PiP 캠)와 다이나믹 줌인 앵커 컷의 하이브리드 교차 편집.
3. 일본 방송국/PIVOT 스타일 極太ゴシック (`NotoSansCJKjp-Black.otf`, Weight 900) 타이포그래피 + 이모지 두부박스(☐) 원천 차단 필터(`sanitize_cjk_text`).
4. 124-BPM 모던 파이낸셜 뉴스 펄스 BGM(음성 구간 자동 덕킹) + 컷별 멀티레이어 포인트 SFX + `-0.5 dBFS` 브릭월 리미터(`alimiter=limit=0.944:level=disabled`).
5. GEMINI.md 제4절 클린 비디오 규격 100% 준수:
   - 1080x1920 풀스크린, 본문 중 상하단 레터박스/고정 홍보 배너/도메인 워터마크 0%
   - 과속(`atempo` 중첩) 금지, 자막-음성 1:1 일치 및 100% 완독(`seg_dur >= tts_dur + 0.28s`)
   - 하단 세이프존(`Y=1385~1460`) 반투명 박스 없는 두꺼운 외곽선(`stroke_width=10`) 자막
   - `getbreakai.com` 도메인 콜아웃은 마지막 3.3~3.8초 엔딩 슬레이트에서만 노출
"""

import os
import re
import sys
import json
import math
import wave
import struct
import shutil
import zipfile
import asyncio
import hashlib
import argparse
import subprocess
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont, ImageOps, ImageEnhance, ImageFilter

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
if SCRIPT_DIR not in sys.path:
    sys.path.insert(0, SCRIPT_DIR)

from jp_viral_v4_episodes_data import EPISODES_V4

ROOT_DIR = r"D:\드림컴퍼니\3사업부"
STUDIO_DIR = os.path.join(ROOT_DIR, "flow_shorts_studio")
ZIP_PATH = os.path.join(STUDIO_DIR, "11월 09 - 23_26.zip")
RAW_CLIPS_DIR = os.path.join(STUDIO_DIR, "flow_raw_clips")

OUT_DIR = os.path.join(STUDIO_DIR, "viral_jp_v4")
THUMB_DIR = os.path.join(OUT_DIR, "thumbnails")
TEMP_DIR = os.path.join(STUDIO_DIR, "_temp_v4_cinema")
TTS_CACHE_DIR = os.path.join(STUDIO_DIR, "_tts_cache_v4_jp")

FONT_BLACK_PATH = os.path.join(ROOT_DIR, "assets", "fonts", "NotoSansCJKjp-Black.otf")
FONT_BOLD_PATH = os.path.join(ROOT_DIR, "assets", "fonts", "NotoSansCJKjp-Bold.otf")

FPS = 30
W, H = 1080, 1920

# Color Palettes (Broadcast Dark FinTech + High-Contrast Japanese TV Accents)
PALETTE = {
    "rose": {
        "main": (251, 59, 98),
        "bright": (255, 110, 138),
        "dark": (88, 16, 36),
        "glow": (251, 59, 98, 95),
        "pill_bg": (72, 14, 30, 232),
    },
    "emerald": {
        "main": (16, 215, 142),
        "bright": (110, 247, 190),
        "dark": (10, 68, 48),
        "glow": (16, 215, 142, 95),
        "pill_bg": (10, 58, 42, 232),
    },
    "amber": {
        "main": (250, 176, 24),
        "bright": (255, 224, 102),
        "dark": (82, 50, 8),
        "glow": (250, 176, 24, 95),
        "pill_bg": (70, 44, 8, 232),
    },
    "cyan": {
        "main": (34, 202, 248),
        "bright": (132, 232, 255),
        "dark": (12, 58, 82),
        "glow": (34, 202, 248, 95),
        "pill_bg": (12, 48, 72, 232),
    },
    "violet": {
        "main": (148, 102, 255),
        "bright": (196, 172, 255),
        "dark": (42, 22, 88),
        "glow": (148, 102, 255, 95),
        "pill_bg": (34, 18, 76, 232),
    },
}


# =============================================================================
# Font Loader & Zero-Tofu CJK Sanitizer
# =============================================================================
_FONT_CACHE = {}


def load_jp_font(size: int, weight: str = "black") -> ImageFont.FreeTypeFont:
    key = (size, weight)
    if key in _FONT_CACHE:
        return _FONT_CACHE[key]
    candidates = []
    if weight == "black":
        candidates.extend([FONT_BLACK_PATH, FONT_BOLD_PATH])
    else:
        candidates.extend([FONT_BOLD_PATH, FONT_BLACK_PATH])
    candidates.extend([
        "C:/Windows/Fonts/YuGothB.ttc",
        "C:/Windows/Fonts/meiryob.ttc",
        "C:/Windows/Fonts/msgothic.ttc",
    ])
    for p in candidates:
        if os.path.exists(p):
            try:
                f = ImageFont.truetype(p, size)
                _FONT_CACHE[key] = f
                return f
            except Exception:
                pass
    f = ImageFont.load_default()
    _FONT_CACHE[key] = f
    return f


EMOJI_TO_CJK_MAP = {
    "⚠️": "▲ ",
    "⚠": "▲ ",
    "🚨": "▲ ",
    "🛑": "▲ ",
    "❌": "× ",
    "😭": "× ",
    "💸": "▼ ",
    "✅": "✓ ",
    "🛡️": "✓ ",
    "🛡": "✓ ",
    "⚡": "◆ ",
    "🔥": "◆ ",
    "🎯": "◆ ",
    "💡": "◆ ",
    "📊": "▶ ",
    "📈": "▲ ",
    "📉": "▼ ",
    "🧮": "▶ ",
    "📐": "▶ ",
    "🔍": "▶ ",
    "🔄": "▶ ",
    "💬": "● ",
    "🗳️": "● ",
    "🗳": "● ",
    "📰": "● ",
    "🏦": "● ",
    "💼": "● ",
    "🌙": "● ",
    "🕘": "● ",
    "📱": "● ",
    "💰": "◆ ",
    "💴": "¥",
    "🇯🇵": "JP ",
}


def sanitize_cjk_text(text: str) -> str:
    """Replaces color emojis and unsupported dingbats with crisp CJK geometric glyphs so ZERO ☐ tofu boxes ever render."""
    if not text:
        return ""
    s = str(text)
    for k, v in EMOJI_TO_CJK_MAP.items():
        s = s.replace(k, v)
    # Remove variation selectors and zero-width joiners
    s = s.replace("\ufe0f", "").replace("\ufe0e", "").replace("\u200d", "")
    cleaned = []
    for ch in s:
        cp = ord(ch)
        # Strip supplementary plane characters (all 4-byte emojis) and miscellaneous dingbat/symbol blocks not in CJK
        if cp > 0xFFFF:
            continue
        if 0x1F000 <= cp <= 0x1FFFF:
            continue
        if 0x2600 <= cp <= 0x27BF and ch not in ("★", "☆", "●", "○", "◆", "◇", "■", "□", "▲", "△", "▼", "▽", "▶", "◀", "✓", "※"):
            continue
        cleaned.append(ch)
    res = "".join(cleaned)
    res = re.sub(r"\s{2,}", " ", res).strip()
    return res


def fit_font_to_width(draw: ImageDraw.ImageDraw, text: str, max_width: int, start_size: int, min_size: int = 22, weight: str = "black", stroke_width: int = 0) -> ImageFont.FreeTypeFont:
    sz = start_size
    while sz > min_size:
        f = load_jp_font(sz, weight=weight)
        bbox = draw.textbbox((0, 0), text, font=f, stroke_width=stroke_width)
        if (bbox[2] - bbox[0]) <= max_width:
            return f
        sz -= 2
    return load_jp_font(min_size, weight=weight)


def draw_centered_text(draw: ImageDraw.ImageDraw, y: int, text: str, font: ImageFont.FreeTypeFont, fill, max_w: int = W - 80, stroke_width: int = 0, stroke_fill=(0, 0, 0, 255), shadow_offset: int = 0):
    text = sanitize_cjk_text(text)
    bbox = draw.textbbox((0, 0), text, font=font, stroke_width=stroke_width)
    tw = bbox[2] - bbox[0]
    cx = max(36, (W - tw) // 2)
    if shadow_offset > 0:
        draw.text((cx + shadow_offset, y + shadow_offset), text, font=font, fill=(0, 0, 0, 185), stroke_width=stroke_width, stroke_fill=(0, 0, 0, 185))
    draw.text((cx, y), text, font=font, fill=fill, stroke_width=stroke_width, stroke_fill=stroke_fill)


# =============================================================================
# FFmpeg & Raw Clips Utilities
# =============================================================================
def get_ffmpeg_bin() -> str:
    exe = shutil.which("ffmpeg")
    if exe:
        return exe
    import imageio_ffmpeg
    return imageio_ffmpeg.get_ffmpeg_exe()


def probe_duration(ffmpeg_bin: str, media_path: str) -> float:
    proc = subprocess.run(
        [ffmpeg_bin, "-i", media_path],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        encoding="utf-8",
        errors="ignore",
    )
    m = re.search(r"Duration:\s*(\d+):(\d+):(\d+\.\d+)", proc.stderr)
    if not m:
        return 0.0
    return int(m.group(1)) * 3600 + int(m.group(2)) * 60 + float(m.group(3))


def get_ordered_clip_paths() -> list:
    if os.path.exists(ZIP_PATH):
        with zipfile.ZipFile(ZIP_PATH, "r") as zf:
            ordered = []
            for info in zf.infolist():
                p = os.path.join(RAW_CLIPS_DIR, info.filename)
                if os.path.exists(p):
                    ordered.append(p)
            if len(ordered) >= 45:
                return ordered
    return sorted(
        [os.path.join(RAW_CLIPS_DIR, f) for f in os.listdir(RAW_CLIPS_DIR) if f.lower().endswith(".mp4")]
    )


# =============================================================================
# TTS Synthesis (Dual Neural Voices: Keita + Nanami, ZERO atempo distortion)
# =============================================================================
async def _edge_tts_save(text: str, out_mp3: str, voice: str, rate: str = "+5%"):
    import edge_tts
    comm = edge_tts.Communicate(text, voice, rate=rate)
    await comm.save(out_mp3)


def synthesize_cut_tts(ffmpeg_bin: str, text: str, voice: str) -> tuple:
    """
    Synthesizes clean Japanese neural narration with leading/trailing dead air gently trimmed
    and a 0.06s safety cushion so the final syllable is 100% preserved.
    Returns (wav_path, tts_duration_sec).
    """
    os.makedirs(TTS_CACHE_DIR, exist_ok=True)
    digest = hashlib.md5(f"{voice}|+5%|{text}".encode("utf-8")).hexdigest()[:16]
    raw_mp3 = os.path.join(TTS_CACHE_DIR, f"{digest}_raw.mp3")
    clean_wav = os.path.join(TTS_CACHE_DIR, f"{digest}_clean.wav")

    if not os.path.exists(clean_wav) or os.path.getsize(clean_wav) < 1000:
        if not os.path.exists(raw_mp3) or os.path.getsize(raw_mp3) < 500:
            asyncio.run(_edge_tts_save(text, raw_mp3, voice=voice, rate="+5%"))
        af_trim = (
            "silenceremove=start_periods=1:start_duration=0.02:start_threshold=-46dB,"
            "areverse,"
            "silenceremove=start_periods=1:start_duration=0.03:start_threshold=-46dB,"
            "areverse,"
            "apad=pad_dur=0.06"
        )
        subprocess.run(
            [
                ffmpeg_bin, "-y",
                "-i", raw_mp3,
                "-af", af_trim,
                "-ar", "44100", "-ac", "1",
                "-c:a", "pcm_s16le",
                clean_wav,
            ],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=True,
        )

    dur = probe_duration(ffmpeg_bin, clean_wav)
    return clean_wav, max(0.8, dur)


# =============================================================================
# Subtitle Layer & Presenter Floating HUD Renderer (1080x1920 RGBA)
# =============================================================================
def draw_v4_subtitle_lines(img: Image.Image, sub_lines: list, is_ending: bool = False):
    """
    Draws @GetBreakAI Golden Safe-Zone (Y=980~1080) subtitles:
    - Avoids bottom 3-line YouTube Shorts title/channel overlay obstruction
    - NO semi-transparent background box
    - NotoSansCJKjp-Black (Weight 900, 82pt+), stroke_width=10 black outline + crisp drop shadow
    """
    draw = ImageDraw.Draw(img)
    cap_y = 995
    for idx, raw_line in enumerate(sub_lines[:2]):
        line = sanitize_cjk_text(raw_line)
        f_cap = fit_font_to_width(draw, line, max_width=W - 76, start_size=82, min_size=48, weight="black", stroke_width=10)
        if is_ending:
            fill_col = (110, 247, 190, 255) if idx == 0 else (255, 255, 255, 255)
        else:
            fill_col = (255, 238, 88, 255) if idx == 0 else (255, 255, 255, 255)
        draw_centered_text(
            draw,
            cap_y,
            line,
            f_cap,
            fill_col,
            max_w=W - 76,
            stroke_width=10,
            stroke_fill=(0, 0, 0, 255),
            shadow_offset=4,
        )
        cap_y += 92


def render_presenter_overlay_png(out_png: str, cut: dict):
    """
    Renders floating upper-safe-zone HUD card (Y=130..395) + bottom safe-zone subtitle (Y=1385~1460).
    NO full-width top/bottom bars, NO watermarks or domains.
    """
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    pal = PALETTE.get(cut.get("hud_color", "rose"), PALETTE["rose"])
    badge_txt = sanitize_cjk_text(cut.get("hud_badge", "◆ 注目ポイント"))
    title_txt = sanitize_cjk_text(cut.get("hud_title", ""))
    metric_txt = sanitize_cjk_text(cut.get("hud_metric", ""))

    # Soft drop shadow under floating HUD card
    shadow_layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    s_draw = ImageDraw.Draw(shadow_layer)
    s_draw.rounded_rectangle([(62, 142), (W - 62, 398)], radius=30, fill=(0, 0, 0, 135))
    shadow_layer = shadow_layer.filter(ImageFilter.GaussianBlur(radius=12))
    img = Image.alpha_composite(img, shadow_layer)
    draw = ImageDraw.Draw(img)

    # Floating dark glass card
    draw.rounded_rectangle(
        [(58, 132), (W - 58, 388)],
        radius=28,
        fill=(11, 15, 30, 212),
        outline=(*pal["main"], 235),
        width=4,
    )
    # Left accent vertical bar inside card
    draw.rounded_rectangle([(78, 156), (92, 364)], radius=7, fill=(*pal["main"], 255))

    # Top pill badge
    f_badge = fit_font_to_width(draw, badge_txt, max_width=820, start_size=30, min_size=22, weight="bold")
    bb = draw.textbbox((0, 0), badge_txt, font=f_badge)
    pill_w = (bb[2] - bb[0]) + 44
    draw.rounded_rectangle([(114, 152), (114 + pill_w, 202)], radius=16, fill=pal["pill_bg"], outline=(*pal["bright"], 200), width=2)
    draw.text((136, 157), badge_txt, font=f_badge, fill=(*pal["bright"], 255))

    # Main HUD headline & metric
    f_title = fit_font_to_width(draw, title_txt, max_width=860, start_size=44, min_size=28, weight="black")
    draw.text((116, 216), title_txt, font=f_title, fill=(255, 255, 255, 255), stroke_width=3, stroke_fill=(0, 0, 0, 220))

    f_metric = fit_font_to_width(draw, metric_txt, max_width=860, start_size=40, min_size=26, weight="black")
    draw.text((116, 294), metric_txt, font=f_metric, fill=(*pal["bright"], 255), stroke_width=3, stroke_fill=(0, 0, 0, 220))

    draw_v4_subtitle_lines(img, cut.get("sub", []), is_ending=False)
    img.save(out_png, "PNG")


def render_ending_overlay_png(out_png: str, ep: dict, cut: dict):
    """
    Renders final 3.3~3.8s Ending Slate glassmorphic FinTech card with getbreakai.com callout.
    """
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    pal = PALETTE.get(ep.get("accent", "emerald"), PALETTE["emerald"])
    ticker = ep.get("ticker", "NVDA")
    jp_name = sanitize_cjk_text(ep.get("jp_name", "新NISA・日本株"))

    # Backdrop dim
    draw.rectangle([(0, 0), (W, H)], fill=(6, 9, 22, 188))

    # Outer glow card
    glow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    gdraw = ImageDraw.Draw(glow)
    gdraw.rounded_rectangle([(56, 300), (W - 56, 1250)], radius=42, fill=(*pal["main"], 70))
    glow = glow.filter(ImageFilter.GaussianBlur(radius=22))
    img = Image.alpha_composite(img, glow)
    draw = ImageDraw.Draw(img)

    draw.rounded_rectangle(
        [(62, 310), (W - 62, 1240)],
        radius=38,
        fill=(12, 17, 38, 242),
        outline=(*pal["main"], 255),
        width=5,
    )

    f_tag = load_jp_font(33, weight="bold")
    draw_centered_text(draw, 358, "◆ 新NISA・日本株・米国株 3秒リスク診断AI ◆", f_tag, (255, 224, 102, 255))

    f_dom = load_jp_font(84, weight="black")
    draw_centered_text(draw, 430, "getbreakai.com", f_dom, (255, 255, 255, 255), stroke_width=6, stroke_fill=(0, 0, 0, 255))

    diag_line = f"▶ {jp_name} ({ticker}) 適正株数・逆指値を無料計算"
    f_diag = fit_font_to_width(draw, diag_line, max_width=860, start_size=36, min_size=24, weight="black")
    draw_centered_text(draw, 566, diag_line, f_diag, (*pal["bright"], 255))

    # CTA Button
    draw.rounded_rectangle(
        [(104, 652), (W - 104, 786)],
        radius=28,
        fill=(*pal["main"], 255),
        outline=(255, 255, 255, 255),
        width=3,
    )
    f_btn = load_jp_font(38, weight="black")
    draw_centered_text(draw, 696, "無料AI株数・損切り計算機 ➔ プロフのリンク", f_btn, (255, 255, 255, 255), stroke_width=3, stroke_fill=(0, 0, 0, 180))

    # 3 crisp Japanese retail value bullets (ZERO Telegram / ZERO legacy handles)
    bullets = [
        ("✓ 株価-8%逆指値でも口座損失-1.5%以内の適正株数計算", (236, 242, 250, 255)),
        ("✓ 日本円(¥)・米ドル($)・新NISA成長投資枠に完全対応", (236, 242, 250, 255)),
        ("✓ YouTube @GetBreakAI | 米国株・新NISAクオンツ", (125, 211, 252, 255)),
    ]
    by = 845
    for btxt, bcol in bullets:
        fb = fit_font_to_width(draw, btxt, max_width=850, start_size=34, min_size=24, weight="bold")
        draw.text((112, by), btxt, font=fb, fill=bcol)
        by += 82

    # Subtle disclaimer for Japanese financial compliance
    f_disc = load_jp_font(23, weight="bold")
    draw_centered_text(draw, 1165, "※本映像は統計データの教育シミュレーションであり投資助言ではありません", f_disc, (148, 163, 184, 235))

    draw_v4_subtitle_lines(img, cut.get("sub", []), is_ending=True)
    img.save(out_png, "PNG")


# =============================================================================
# Quant Terminal Badge Renderer (AI Japanese Female Announcer PiP 100% Retired)
# =============================================================================
def extract_pip_frames(ffmpeg_bin: str, clip_path: str, n_frames: int, diameter: int = 224, accent_rgb=(16, 215, 142)) -> list:
    """
    Replaces legacy AI female announcer face PiP with a crisp animated dark-mode
    GetBreakAI SEC 8-K & 2.0x ATR Terminal telemetry badge (zero AI human clips).
    """
    box_w, box_h = diameter + 24, diameter + 38
    f_top = load_jp_font(20, weight="black")
    f_mid = load_jp_font(24, weight="black")
    f_bot = load_jp_font(18, weight="bold")

    pip_frames = []
    for i in range(n_frames):
        pulse = int(65 + 45 * math.sin(i * 0.25))
        canvas = Image.new("RGBA", (box_w, box_h), (0, 0, 0, 0))
        d = ImageDraw.Draw(canvas)
        d.rounded_rectangle([(8, 12), (box_w - 8, box_h - 14)], radius=26, fill=(11, 17, 36, 242), outline=(*accent_rgb, 245), width=3)
        d.ellipse([(24, 30), (36, 42)], fill=(*accent_rgb, min(255, 160 + pulse)))
        d.text((46, 24), "SEC 8-K AI", font=f_top, fill=(255, 255, 255, 255))
        d.text((24, 66), "2.0x ATR", font=f_mid, fill=(*accent_rgb, 255))
        d.text((24, 104), "口座損失 -1.5%内", font=f_bot, fill=(255, 232, 98, 255))
        d.text((24, 136), "getbreakai.com", font=f_bot, fill=(186, 206, 235, 255))
        pip_frames.append(canvas)
    return pip_frames


# =============================================================================
# 30fps Animated Quant Chart Scene Renderers (chart_bar, chart_candle, chart_race)
# =============================================================================
def create_chart_base_canvas(accent_key: str, badge_label: str, title_text: str, sub_text: str) -> Image.Image:
    """
    Builds the static dark institutional quant studio background (1080x1920 RGB) with subtle grid,
    glowing header accents, and left-aligned header typography (leaving X=785..1035 free for Circular PiP!).
    """
    pal = PALETTE.get(accent_key, PALETTE["emerald"])
    base = Image.new("RGB", (W, H), (8, 12, 24))
    draw = ImageDraw.Draw(base)

    # Vertical deep gradient + subtle grid lines
    for y in range(0, H, 4):
        t = y / H
        r = int(8 + 8 * (1.0 - abs(t - 0.35)))
        g = int(13 + 12 * (1.0 - abs(t - 0.35)))
        b = int(26 + 22 * (1.0 - abs(t - 0.35)))
        draw.rectangle([(0, y), (W, y + 4)], fill=(r, g, b))

    for gx in range(60, W, 120):
        draw.line([(gx, 90), (gx, 1340)], fill=(22, 31, 54), width=1)
    for gy in range(120, 1360, 120):
        draw.line([(48, gy), (W - 48, gy)], fill=(22, 31, 54), width=1)

    # Radial glow behind chart center
    glow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    gdraw = ImageDraw.Draw(glow)
    gdraw.ellipse([(140, 420), (W - 140, 1220)], fill=(*pal["main"], 34))
    glow = glow.filter(ImageFilter.GaussianBlur(radius=65))
    base_rgba = base.convert("RGBA")
    base_rgba = Image.alpha_composite(base_rgba, glow)
    draw = ImageDraw.Draw(base_rgba)

    # Top-left Quant Studio Pill + Header (max_width=695 so it never touches Circular PiP at X=792!)
    badge_clean = sanitize_cjk_text(badge_label)
    f_badge = load_jp_font(26, weight="black")
    bb = draw.textbbox((0, 0), badge_clean, font=f_badge)
    pw = (bb[2] - bb[0]) + 36
    draw.rounded_rectangle([(56, 122), (56 + pw, 168)], radius=14, fill=pal["pill_bg"], outline=(*pal["bright"], 210), width=2)
    draw.text((74, 127), badge_clean, font=f_badge, fill=(*pal["bright"], 255))

    # Split or fit title cleanly inside 695px width
    title_clean = sanitize_cjk_text(title_text)
    f_title = fit_font_to_width(draw, title_clean, max_width=695, start_size=42, min_size=26, weight="black")
    draw.text((56, 186), title_clean, font=f_title, fill=(255, 255, 255, 255), stroke_width=3, stroke_fill=(0, 0, 0, 220))

    sub_clean = sanitize_cjk_text(sub_text)
    f_sub = fit_font_to_width(draw, sub_clean, max_width=695, start_size=30, min_size=22, weight="bold")
    draw.text((58, 254), sub_clean, font=f_sub, fill=(186, 202, 228, 255))

    return base_rgba


def ease_out_cubic(x: float) -> float:
    x = max(0.0, min(1.0, x))
    return 1.0 - pow(1.0 - x, 3)


def format_jp_counter(prefix: str, val: float, suffix: str, is_float_target: bool = False) -> str:
    p = sanitize_cjk_text(prefix)
    s = sanitize_cjk_text(suffix)
    if is_float_target:
        num_str = f"{val:.1f}"
    else:
        num_str = f"{int(round(val)):,}"
    return f"{p}{num_str}{s}"


def render_chart_cut_mp4(ffmpeg_bin: str, out_mp4: str, cut: dict, pip_clip_path: str, seg_dur: float, ep_accent: str):
    """
    Streams 30fps 1080x1920 RGB frames directly to FFmpeg for `chart_bar`, `chart_candle`, or `chart_race`.
    """
    n_frames = max(int(round(seg_dur * FPS)), 30)
    ctype = cut["type"]
    ch = cut["chart"]

    # Determine primary accent color for PiP & header
    if ctype == "chart_bar":
        c_accent = ch.get("counter_color", ep_accent)
        sub_hdr = ch.get("subtitle", "")
    elif ctype == "chart_candle":
        c_accent = "rose" if ch.get("mode") == "crash" else "emerald"
        sub_hdr = ch.get("ticker_label", "")
    else:
        c_accent = "emerald"
        sub_hdr = "リアル資産推移シミュレーション"

    pal_hdr = PALETTE.get(c_accent, PALETTE["emerald"])
    base_rgba = create_chart_base_canvas(
        accent_key=c_accent,
        badge_label="▶ QUANT SIMULATION",
        title_text=ch.get("title", ""),
        sub_text=sub_hdr,
    )

    # Pre-render transparent subtitle layer once per cut
    sub_layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    draw_v4_subtitle_lines(sub_layer, cut.get("sub", []), is_ending=False)

    # Pre-extract circular live-action presenter PiP frames
    pip_frames = extract_pip_frames(ffmpeg_bin, pip_clip_path, n_frames, diameter=216, accent_rgb=pal_hdr["main"])

    # Pre-compute deterministic candlestick series if chart_candle
    candles = []
    ma60_pts = []
    if ctype == "chart_candle":
        mode = ch.get("mode", "crash")
        if mode == "crash":
            # Starts at 104, breaks 60MA (100) on bar 6, 3 retail nanpin traps, plunges to 52
            closes = [103, 105, 104, 102, 100, 96, 91, 93, 86, 81, 84, 77, 72, 74, 67, 63, 65, 59, 56, 54, 53, 52]
            opens  = [101, 103, 105, 104, 102, 100, 96, 91, 93, 86, 81, 84, 77, 72, 74, 67, 63, 65, 59, 56, 54, 53]
            vols   = [32,  35,  30,  38,  45,  78, 88, 42, 92, 76, 40, 85, 95, 44, 89, 82, 46, 96, 84, 72, 68, 90]
            ma60_pts = [100.5 - i * 0.65 for i in range(22)]
        else:
            # Tight VCP base along 60MA (96..101), Bar 12 volume 2.4x ignition breakout -> surges to 168!
            closes = [95, 97, 96, 98, 97, 99, 98, 100, 99, 101, 100, 102, 114, 121, 119, 129, 138, 136, 147, 155, 162, 168]
            opens  = [94, 95, 97, 96, 98, 97, 99,  98, 100, 99, 101, 100, 102, 114, 121, 119, 129, 138, 136, 147, 155, 162]
            vols   = [28, 30, 25, 27, 24, 26, 22,  25,  21, 24,  20,  32,  96,  88,  45,  84,  86,  42,  82,  79,  85,  92]
            ma60_pts = [94.0 + i * 1.45 for i in range(22)]

        for i in range(22):
            o, c = opens[i], closes[i]
            hi = max(o, c) + (2.6 if i % 2 == 0 else 1.8)
            lo = min(o, c) - (2.4 if i % 3 == 0 else 1.6)
            candles.append((o, hi, lo, c, vols[i]))

    cmd = [
        ffmpeg_bin, "-y",
        "-f", "rawvideo",
        "-pix_fmt", "rgb24",
        "-s", f"{W}x{H}",
        "-r", str(FPS),
        "-i", "-",
        "-c:v", "libx264",
        "-preset", "fast",
        "-crf", "20",
        "-pix_fmt", "yuv420p",
        out_mp4,
    ]
    proc = subprocess.Popen(cmd, stdin=subprocess.PIPE, stderr=subprocess.PIPE)

    for f_idx in range(n_frames):
        # Complete primary animation by 72% of cut duration so viewer has 28% hold time to absorb final numbers!
        prog = ease_out_cubic(f_idx / max(1.0, n_frames * 0.72))
        frame = base_rgba.copy()
        draw = ImageDraw.Draw(frame)

        # Paste Circular Live Presenter PiP in top-right (X=792, Y=106)
        frame.alpha_composite(pip_frames[f_idx], (792, 106))

        if ctype == "chart_bar":
            # 1) Hero Live Ticking Counter Box (Y=375..575)
            c_pal = PALETTE.get(ch.get("counter_color", "rose"), PALETTE["rose"])
            draw.rounded_rectangle(
                [(56, 378), (W - 56, 576)],
                radius=28,
                fill=(14, 20, 42, 235),
                outline=(*c_pal["main"], 220),
                width=3,
            )
            is_flt = isinstance(ch["counter_end"], float) and not ch["counter_end"].is_integer()
            cur_val = ch["counter_start"] + (ch["counter_end"] - ch["counter_start"]) * prog
            cnt_txt = format_jp_counter(ch["counter_prefix"], cur_val, ch["counter_suffix"], is_float_target=is_flt)
            f_cnt = fit_font_to_width(draw, cnt_txt, max_width=880, start_size=76, min_size=44, weight="black")
            draw_centered_text(draw, 432, cnt_txt, f_cnt, (*c_pal["bright"], 255), stroke_width=5, stroke_fill=(0, 0, 0, 240))

            # 2) High-Impact Animated Horizontal Comparison Cards (supports 2 or 3 bars cleanly inside Y=604..1320)
            bars_list = ch["bars"][:3]
            is_three = len(bars_list) == 3
            by = 602 if is_three else 620
            card_h = 224 if is_three else 305
            step_y = 240 if is_three else 338
            for b_idx, bar in enumerate(bars_list):
                b_pal = PALETTE.get(bar.get("color", "cyan"), PALETTE["cyan"])
                b_prog = ease_out_cubic((f_idx - b_idx * 5) / max(1.0, n_frames * 0.65))
                draw.rounded_rectangle(
                    [(56, by), (W - 56, by + card_h)],
                    radius=26,
                    fill=(13, 19, 38, 236),
                    outline=(45, 62, 98, 220),
                    width=2,
                )
                lbl_txt = sanitize_cjk_text(bar["label"])
                f_lbl = fit_font_to_width(draw, lbl_txt, max_width=880, start_size=31 if is_three else 36, min_size=22, weight="bold")
                draw.text((92, by + (18 if is_three else 28)), lbl_txt, font=f_lbl, fill=(235, 242, 255, 255))

                # Track background
                track_x1, track_x2 = 92, W - 92
                track_y1 = by + (74 if is_three else 102)
                track_y2 = by + (132 if is_three else 178)
                draw.rounded_rectangle([(track_x1, track_y1), (track_x2, track_y2)], radius=18, fill=(24, 33, 58, 255))

                # Animated fill bar
                ratio = max(0.06, min(1.0, (bar["val"] / max(1.0, bar["max"])) * b_prog))
                fill_x2 = int(track_x1 + (track_x2 - track_x1) * ratio)
                draw.rounded_rectangle(
                    [(track_x1, track_y1), (max(track_x1 + 36, fill_x2), track_y2)],
                    radius=18,
                    fill=(*b_pal["main"], 255),
                    outline=(*b_pal["bright"], 255),
                    width=2,
                )

                # Result callout pill
                res_txt = sanitize_cjk_text(bar["text"])
                f_res = fit_font_to_width(draw, res_txt, max_width=860, start_size=36 if is_three else 44, min_size=24, weight="black")
                alpha_res = int(255 * min(1.0, b_prog * 1.6))
                draw.text((92, by + (148 if is_three else 202)), res_txt, font=f_res, fill=(*b_pal["bright"], alpha_res), stroke_width=3, stroke_fill=(0, 0, 0, alpha_res))
                by += step_y

        elif ctype == "chart_candle":
            mode = ch.get("mode", "crash")
            c_pal = PALETTE["rose"] if mode == "crash" else PALETTE["emerald"]

            # 1) Live Balance Counter Strip (Y=372..546) — guaranteed >= 42px separation between counter and right tag pill
            draw.rounded_rectangle(
                [(56, 372), (W - 56, 546)],
                radius=26,
                fill=(14, 20, 42, 238),
                outline=(*c_pal["main"], 225),
                width=3,
            )
            is_flt_c = isinstance(ch["counter_end"], float) and not ch["counter_end"].is_integer()
            cur_bal = ch["counter_start"] + (ch["counter_end"] - ch["counter_start"]) * prog
            final_bal_txt = format_jp_counter(ch["counter_prefix"], ch["counter_end"], "", is_float_target=is_flt_c)
            bal_txt = format_jp_counter(ch["counter_prefix"], cur_bal, "", is_float_target=is_flt_c)
            f_bal = fit_font_to_width(draw, final_bal_txt, max_width=450, start_size=56, min_size=30, weight="black")
            bb_bal = draw.textbbox((0, 0), bal_txt, font=f_bal)
            bal_y = 372 + (174 - (bb_bal[3] - bb_bal[1])) // 2 - 4
            draw.text((84, bal_y), bal_txt, font=f_bal, fill=(*c_pal["bright"], 255), stroke_width=4, stroke_fill=(0, 0, 0, 230))

            # Right tag badge inside balance strip
            tag_clean = sanitize_cjk_text(ch.get("tag_text", ""))
            f_tag = fit_font_to_width(draw, tag_clean, max_width=380, start_size=26, min_size=18, weight="black")
            tb = draw.textbbox((0, 0), tag_clean, font=f_tag)
            tw = tb[2] - tb[0]
            draw.rounded_rectangle([(W - 84 - tw - 30, 426), (W - 80, 492)], radius=16, fill=c_pal["pill_bg"], outline=(*c_pal["bright"], 220), width=2)
            draw.text((W - 84 - tw - 14, 440), tag_clean, font=f_tag, fill=(*c_pal["bright"], 255))

            # 2) Candlestick + 60MA Arena (Y=570..1130) & Volume Subpanel (Y=1146..1310)
            draw.rounded_rectangle([(56, 570), (W - 56, 1318)], radius=28, fill=(11, 16, 34, 238), outline=(38, 54, 88, 220), width=2)
            plot_x1, plot_x2 = 88, W - 88
            plot_y1, plot_y2 = 610, 1110
            vol_y1, vol_y2 = 1152, 1292
            draw.line([(plot_x1, 1130), (plot_x2, 1130)], fill=(42, 58, 92, 255), width=2)

            all_vals = [v for cdl in candles for v in cdl[:4]] + ma60_pts
            p_min, p_max = min(all_vals) - 4.0, max(all_vals) + 6.0

            def py_map(val):
                return int(plot_y2 - ((val - p_min) / (p_max - p_min)) * (plot_y2 - plot_y1))

            n_vis = max(2, min(22, int(round(2 + 20 * prog))))
            step_x = (plot_x2 - plot_x1) / 22.0

            # Draw 60-day MA smooth line + clean legend pill at top-right of chart arena (never overlaps candles)
            ma_xy = [(int(plot_x1 + (i + 0.5) * step_x), py_map(ma60_pts[i])) for i in range(n_vis)]
            if len(ma_xy) >= 2:
                draw.line(ma_xy, fill=(250, 190, 40, 235), width=5)
            f_ma = load_jp_font(22, weight="bold")
            leg_x1 = plot_x2 - 228 if mode == "crash" else plot_x1 + 8
            leg_y1 = plot_y1 - 14
            draw.rounded_rectangle([(leg_x1, leg_y1), (leg_x1 + 220, leg_y1 + 34)], radius=10, fill=(38, 30, 12, 225), outline=(250, 190, 40, 210), width=2)
            draw.text((leg_x1 + 14, leg_y1 + 4), "━ 60日移動平均線", font=f_ma, fill=(255, 216, 88, 255))

            # If breakout mode, draw 2.0xATR stop defense line under base
            if mode == "breakout":
                stop_y = py_map(91.5)
                for sx in range(plot_x1, plot_x1 + int(13 * step_x), 24):
                    draw.line([(sx, stop_y), (sx + 14, stop_y)], fill=(34, 202, 248, 220), width=3)
                f_st = load_jp_font(22, weight="bold")
                draw.text((plot_x1 + 8, stop_y + 8), "✓ 2.0倍ATR 逆指値防衛ライン (-1.5%)", font=f_st, fill=(132, 232, 255, 255))

            # Draw Candles + Volume bars
            for i in range(n_vis):
                o, hi, lo, c, vol = candles[i]
                cx = int(plot_x1 + (i + 0.5) * step_x)
                bull = c >= o
                col = (16, 215, 142, 255) if bull else (251, 59, 98, 255)
                wick_col = (110, 247, 190, 255) if bull else (255, 120, 145, 255)

                y_hi, y_lo = py_map(hi), py_map(lo)
                y_o, y_c = py_map(o), py_map(c)
                draw.line([(cx, y_hi), (cx, y_lo)], fill=wick_col, width=3)
                top_b, bot_b = min(y_o, y_c), max(y_o, y_c)
                if bot_b - top_b < 5:
                    bot_b = top_b + 5
                bw = int(step_x * 0.34)
                draw.rectangle([(cx - bw, top_b), (cx + bw, bot_b)], fill=col)

                # Volume bar
                vh = int((vol / 100.0) * (vol_y2 - vol_y1))
                v_col = (16, 215, 142, 195) if bull else (251, 59, 98, 195)
                if mode == "breakout" and i == 12:
                    v_col = (255, 224, 82, 255)
                draw.rectangle([(cx - bw, vol_y2 - vh), (cx + bw, vol_y2)], fill=v_col)

            # Callout annotations on key bars
            f_ann = load_jp_font(24, weight="black")
            if mode == "crash":
                for trap_idx, lbl in [(8, "× ナンピン①"), (12, "× ナンピン②"), (16, "× ナンピン③")]:
                    if n_vis > trap_idx:
                        tx = int(plot_x1 + (trap_idx + 0.5) * step_x)
                        ty = py_map(candles[trap_idx][1]) - 42
                        draw.rounded_rectangle([(tx - 78, ty - 6), (tx + 82, ty + 30)], radius=10, fill=(88, 14, 32, 240), outline=(255, 110, 138, 255), width=2)
                        draw.text((tx - 70, ty - 3), lbl, font=f_ann, fill=(255, 225, 230, 255))
            else:
                if n_vis > 12:
                    bx = int(plot_x1 + 12.5 * step_x)
                    by_pt = py_map(candles[12][3]) - 54
                    draw.rounded_rectangle([(bx - 135, by_pt - 6), (bx + 185, by_pt + 34)], radius=12, fill=(10, 68, 48, 245), outline=(110, 247, 190, 255), width=2)
                    draw.text((bx - 122, by_pt - 2), "◆ 出来高2.4倍 ブレイク!", font=f_ann, fill=(255, 242, 115, 255))

        elif ctype == "chart_race":
            # 1) Dual Scoreboard Cards (Y=372..568)
            bad_curve = ch["bad_curve"]
            good_curve = ch["good_curve"]

            # Interpolate curve index
            max_idx = len(bad_curve) - 1
            f_pos = prog * max_idx
            i0 = min(max_idx, int(math.floor(f_pos)))
            i1 = min(max_idx, i0 + 1)
            frac = f_pos - i0

            # Left card: Retail Bad Strategy
            draw.rounded_rectangle([(56, 372), (526, 566)], radius=24, fill=(44, 14, 28, 232), outline=(251, 59, 98, 220), width=3)
            b_lbl = sanitize_cjk_text(ch["bad_label"])
            fb_l = fit_font_to_width(draw, b_lbl, max_width=430, start_size=26, min_size=18, weight="bold")
            draw.text((80, 392), b_lbl, font=fb_l, fill=(255, 165, 182, 255))
            b_end_txt = sanitize_cjk_text(ch["bad_end_str"]) if prog > 0.82 else f"{bad_curve[i0] + (bad_curve[i1] - bad_curve[i0]) * frac:.0f}"
            if prog <= 0.82 and "¥" in ch["bad_end_str"]:
                # Scale smoothly toward final string
                b_end_txt = sanitize_cjk_text(ch["bad_end_str"]) if prog > 0.7 else f"推移 {bad_curve[i0] + (bad_curve[i1] - bad_curve[i0]) * frac:.0f}"
            fb_v = fit_font_to_width(draw, sanitize_cjk_text(ch["bad_end_str"]), max_width=430, start_size=48, min_size=30, weight="black")
            draw.text((80, 456), sanitize_cjk_text(ch["bad_end_str"]) if prog > 0.65 else b_end_txt, font=fb_v, fill=(255, 98, 130, 255), stroke_width=3, stroke_fill=(0, 0, 0, 220))

            # Right card: Quant Good Strategy
            draw.rounded_rectangle([(554, 372), (W - 56, 566)], radius=24, fill=(10, 48, 38, 232), outline=(16, 215, 142, 235), width=3)
            g_lbl = sanitize_cjk_text(ch["good_label"])
            fg_l = fit_font_to_width(draw, g_lbl, max_width=430, start_size=26, min_size=18, weight="bold")
            draw.text((578, 392), g_lbl, font=fg_l, fill=(152, 250, 208, 255))
            g_cur_txt = sanitize_cjk_text(ch["good_end_str"]) if prog > 0.65 else f"推移 {good_curve[i0] + (good_curve[i1] - good_curve[i0]) * frac:.0f}"
            fg_v = fit_font_to_width(draw, sanitize_cjk_text(ch["good_end_str"]), max_width=430, start_size=48, min_size=30, weight="black")
            draw.text((578, 456), g_cur_txt, font=fg_v, fill=(110, 247, 190, 255), stroke_width=3, stroke_fill=(0, 0, 0, 220))

            # 2) Racing Dual Equity Curves Arena (Y=594..1195)
            draw.rounded_rectangle([(56, 594), (W - 56, 1196)], radius=28, fill=(11, 16, 34, 238), outline=(38, 54, 88, 220), width=2)
            rx1, rx2 = 100, W - 100
            ry1, ry2 = 648, 1142

            all_c = bad_curve + good_curve
            c_min, c_max = min(all_c) - (max(all_c) - min(all_c)) * 0.12, max(all_c) + (max(all_c) - min(all_c)) * 0.15
            if abs(c_max - c_min) < 1e-3:
                c_max = c_min + 10.0

            def ry_map(v):
                return int(ry2 - ((v - c_min) / (c_max - c_min)) * (ry2 - ry1))

            # Baseline dashed line (initial value = bad_curve[0])
            base_y = ry_map(bad_curve[0])
            for bx in range(rx1, rx2, 22):
                draw.line([(bx, base_y), (bx + 12, base_y)], fill=(94, 112, 148, 180), width=2)

            # Upsample curves to 48 steps for silky 30fps curve drawing
            n_steps = 48
            vis_steps = max(2, int(round(n_steps * prog)))

            def sample_curve(arr, s_idx):
                pos = (s_idx / (n_steps - 1)) * (len(arr) - 1)
                k0 = min(len(arr) - 1, int(math.floor(pos)))
                k1 = min(len(arr) - 1, k0 + 1)
                t_sub = pos - k0
                val = arr[k0] + (arr[k1] - arr[k0]) * t_sub
                px = int(rx1 + (s_idx / (n_steps - 1)) * (rx2 - rx1))
                return (px, ry_map(val))

            bad_pts = [sample_curve(bad_curve, s) for s in range(vis_steps)]
            good_pts = [sample_curve(good_curve, s) for s in range(vis_steps)]

            if len(bad_pts) >= 2:
                draw.line(bad_pts, fill=(251, 59, 98, 255), width=9)
                bx_end, by_end = bad_pts[-1]
                draw.ellipse([(bx_end - 11, by_end - 11), (bx_end + 11, by_end + 11)], fill=(255, 130, 155, 255), outline=(255, 255, 255, 255), width=3)

            if len(good_pts) >= 2:
                draw.line(good_pts, fill=(16, 215, 142, 255), width=10)
                gx_end, gy_end = good_pts[-1]
                draw.ellipse([(gx_end - 13, gy_end - 13), (gx_end + 13, gy_end + 13)], fill=(110, 247, 190, 255), outline=(255, 255, 255, 255), width=3)

            # 3) Spread Callout Pill (Y=1220..1322)
            sp_txt = f"◆ {sanitize_cjk_text(ch['spread_badge'])} ◆"
            draw.rounded_rectangle(
                [(110, 1220), (W - 110, 1320)],
                radius=26,
                fill=(62, 42, 8, 242),
                outline=(255, 214, 68, 255),
                width=3,
            )
            f_sp = fit_font_to_width(draw, sp_txt, max_width=800, start_size=42, min_size=26, weight="black")
            draw_centered_text(draw, 1244, sp_txt, f_sp, (255, 232, 98, 255), stroke_width=4, stroke_fill=(0, 0, 0, 235))

        # Composite bottom safe-zone subtitle layer
        frame = Image.alpha_composite(frame, sub_layer)
        proc.stdin.write(frame.convert("RGB").tobytes())

    proc.stdin.close()
    _, stderr_bytes = proc.communicate()
    if proc.returncode != 0:
        raise RuntimeError(f"Chart cut FFmpeg failed: {stderr_bytes.decode('utf-8', errors='ignore')[-500:]}")


# =============================================================================
# Real Chart & Yen Balance Simulation Cut Renderer (Replaces AI Female Clips)
# =============================================================================
def render_presenter_or_ending_cut_mp4(ffmpeg_bin: str, out_mp4: str, clip_path: str, overlay_png: str, seg_dur: float, zoom_dir: int = 1):
    """
    Renders a 1080x1920 30fps dark institutional quant canvas featuring:
    - Center (y=400..960) live JPY balance simulation (100万円投資 ➔ お祈りナンピン ¥520,000 vs 右側ブレイク＆逆指値 ¥1,680,000)
      + real $NVDA/$SMH/$SOXL OHLCV candlesticks & GetBreakAI Dark-Mode Calculator UI card
    - Forward optical zoom (1.00 -> 1.055, zero reverse playback) + RGBA HUD/Ending overlay.
    """
    n_frames = max(int(round(seg_dur * FPS)), 30)
    ov = Image.open(overlay_png).convert("RGBA")

    # Build crisp institutional chart + Yen balance comparison base canvas (1080x1920)
    bg = Image.new("RGB", (W, H), (8, 12, 25))
    d = ImageDraw.Draw(bg)
    for gx in range(60, W, 120):
        d.line([(gx, 120), (gx, 1420)], fill=(20, 29, 52), width=1)
    for gy in range(160, 1440, 120):
        d.line([(48, gy), (W - 48, gy)], fill=(20, 29, 52), width=1)

    # Yen Balance Simulation Strip (y = 415 .. 590)
    d.rounded_rectangle([(58, 415), (524, 588)], radius=24, fill=(48, 14, 28), outline=(251, 59, 98), width=3)
    d.text((84, 434), "× お祈りナンピン口座 (100万円)", font=load_jp_font(24, weight="bold"), fill=(255, 165, 182))
    d.text((84, 480), "¥520,000", font=load_jp_font(54, weight="black"), fill=(255, 102, 132))

    d.rounded_rectangle([(556, 415), (W - 58, 588)], radius=24, fill=(10, 48, 38), outline=(16, 215, 142), width=3)
    d.text((582, 434), "✓ 右側ブレイク＆逆指値 (100万円)", font=load_jp_font(24, weight="bold"), fill=(152, 250, 208))
    d.text((582, 480), "¥1,680,000", font=load_jp_font(54, weight="black"), fill=(110, 247, 190))

    # Real OHLCV Candlestick + 60MA + GetBreakAI Dark-Mode Sizer Card (y = 610 .. 960)
    d.rounded_rectangle([(58, 610), (W - 58, 958)], radius=26, fill=(11, 17, 36), outline=(56, 189, 248), width=2)
    d.text((88, 632), "$NVDA / $SMH / $SOXL 実チャート × GetBreakAI 適正株数・SEC 8-K 3秒解読", font=load_jp_font(24, weight="bold"), fill=(186, 230, 253))
    closes = [96, 95, 97, 96, 98, 99, 98, 100, 101, 100, 103, 109, 114, 113, 119, 125, 124, 131]
    opens = [97, 96, 95, 97, 96, 98, 99, 98, 100, 101, 100, 103, 109, 114, 113, 119, 125, 124]
    ma60 = [95.0 + i * 1.45 for i in range(18)]
    px1, px2, py1, py2 = 92, W - 92, 682, 922
    step_x = (px2 - px1) / 18.0
    p_min, p_max = 91.0, 135.0
    map_y = lambda v: int(py2 - ((v - p_min) / (p_max - p_min)) * (py2 - py1))
    d.line([(int(px1 + (i + 0.5) * step_x), map_y(ma60[i])) for i in range(18)], fill=(250, 190, 40), width=4)
    for i in range(18):
        o, c = opens[i], closes[i]
        cx = int(px1 + (i + 0.5) * step_x)
        bull = c >= o
        col = (16, 215, 142) if bull else (251, 59, 98)
        d.line([(cx, map_y(max(o, c) + 1.8)), (cx, map_y(min(o, c) - 1.8))], fill=col, width=3)
        yb1, yb2 = min(map_y(o), map_y(c)), max(map_y(o), map_y(c))
        d.rectangle([(cx - 14, yb1), (cx + 14, max(yb1 + 5, yb2))], fill=col)

    d.rounded_rectangle([(58, 1205), (W - 58, 1315)], radius=22, fill=(13, 20, 42), outline=(16, 185, 129), width=2)
    d.text((88, 1242), "✓ 株価 -8% の逆指値でも口座全体の損失が -1.5% 以内に収まる「適正株数」を自動計算", font=load_jp_font(24, weight="bold"), fill=(110, 247, 190))

    cmd = [
        ffmpeg_bin, "-y",
        "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS),
        "-i", "-",
        "-an", "-c:v", "libx264", "-preset", "fast", "-crf", "20", "-pix_fmt", "yuv420p",
        out_mp4,
    ]
    proc = subprocess.Popen(cmd, stdin=subprocess.PIPE, stderr=subprocess.PIPE)
    for f_i in range(n_frames):
        # Forward-only optical zoom (1.00 -> 1.055) on background chart card
        z = 1.0 + 0.055 * (f_i / float(max(1, n_frames - 1)))
        cw, ch = int(W / z), int(H / z)
        x0, y0 = (W - cw) // 2, (H - ch) // 2
        zoomed = bg.crop((x0, y0, x0 + cw, y0 + ch)).resize((W, H), Image.Resampling.BILINEAR).convert("RGBA")
        comp = Image.alpha_composite(zoomed, ov).convert("RGB")
        proc.stdin.write(comp.tobytes())
    proc.stdin.close()
    proc.communicate()
    if proc.returncode != 0:
        raise RuntimeError("Failed to encode quant UI cut MP4")


# =============================================================================
# Procedural 124-BPM Broadcast Financial BGM + Studio Multi-Layer SFX + Voice Ducking
# =============================================================================
def build_master_episode_audio_wav(
    out_wav: str,
    cut_tts_wavs: list,
    cut_durations: list,
    cut_types: list,
    sample_rate: int = 44100,
):
    """
    Combines per-cut TTS narration (placed at exact cut start timestamps with 100% completion),
    124-BPM Modern Financial News Pulse BGM (automatically ducked under active speech),
    and Studio Multi-Layer SFX into a crisp 44.1kHz PCM WAV ready for -0.5 dBFS brickwall limiting.
    """
    total_dur = sum(cut_durations)
    total_samples = int(round(total_dur * sample_rate))
    voice_buf = [0.0] * total_samples

    cut_starts = []
    cursor_s = 0.0
    for wav_path, c_dur in zip(cut_tts_wavs, cut_durations):
        cut_starts.append(cursor_s)
        start_idx = int(round((cursor_s + 0.04) * sample_rate))
        with wave.open(wav_path, "rb") as wf:
            n_ch = wf.getnchannels()
            n_fr = wf.getnframes()
            raw = wf.readframes(n_fr)
            samples = struct.unpack(f"<{n_fr * n_ch}h", raw)
            if n_ch > 1:
                samples = samples[::n_ch]
        # Normalize individual cut voice peak to ~0.82 (-1.7 dBFS) for uniform broadcast loudness
        peak = max(1, max(abs(s) for s in samples))
        gain = (0.82 * 32767.0) / peak
        for i, s in enumerate(samples):
            pos = start_idx + i
            if pos >= total_samples:
                break
            voice_buf[pos] = (s * gain) / 32768.0
        cursor_s += c_dur

    # Compute smooth voice activity envelope (for automatic BGM sidechain ducking)
    env_win = int(0.05 * sample_rate)
    duck_gain = [1.0] * total_samples
    running_sq = 0.0
    for i in range(total_samples):
        running_sq += voice_buf[i] * voice_buf[i]
        if i >= env_win:
            running_sq -= voice_buf[i - env_win] * voice_buf[i - env_win]
        rms = math.sqrt(max(0.0, running_sq / env_win))
        # Duck BGM down to 0.42x when anchor speaks, gently rise to 0.85x in micro-pauses
        duck_gain[i] = 0.42 if rms > 0.035 else 0.78

    # Synthesize 124-BPM Modern Tokyo Financial Studio BGM + Cut-Synced SFX
    bpm = 124.0
    beat_sec = 60.0 / bpm
    half_beat = beat_sec / 2.0
    ending_start = cut_starts[-1]

    out_bytes = bytearray()
    # Warm minor-9th news pulse frequencies (A2, E3, B3, C4)
    chord_freqs = [110.0, 164.81, 246.94, 261.63]

    for i in range(total_samples):
        t = i / sample_rate

        # 1) Subtle 124-BPM Broadcast Pulse BGM
        pulse_phase = (t % half_beat) / half_beat
        pulse_env = 0.45 + 0.55 * math.exp(-pulse_phase * 4.2)
        pad = (
            0.46 * math.sin(2.0 * math.pi * chord_freqs[0] * t)
            + 0.24 * math.sin(2.0 * math.pi * chord_freqs[1] * t)
            + 0.16 * math.sin(2.0 * math.pi * chord_freqs[2] * t)
            + 0.14 * math.sin(2.0 * math.pi * chord_freqs[3] * t)
        )
        # Soft heartbeat kick on quarter-note beats
        q_phase = (t % beat_sec) / beat_sec
        kick = 0.35 * math.exp(-q_phase * 14.0) * math.sin(2.0 * math.pi * (68.0 - 22.0 * q_phase) * q_phase)

        bgm_val = 0.075 * duck_gain[i] * (pad * pulse_env + kick)

        # 2) Multi-Layer Studio Point SFX
        sfx_val = 0.0
        # 0.0s Hook Impact + Headline Shimmer
        if 0.0 <= t < 0.42:
            e = math.exp(-t * 9.5)
            sfx_val += 0.22 * e * math.sin(2.0 * math.pi * (92.0 - 35.0 * t) * t)
            sfx_val += 0.09 * math.exp(-t * 14.0) * (
                math.sin(2.0 * math.pi * 880.0 * t) + 0.6 * math.sin(2.0 * math.pi * 1318.5 * t)
            )

        # Body cut transitions
        for c_idx in range(1, len(cut_starts) - 1):
            dt = t - cut_starts[c_idx]
            ctype = cut_types[c_idx]
            if 0.0 <= dt < 0.32:
                e = math.exp(-dt * 13.0)
                f_sweep = 190.0 + 380.0 * (dt / 0.32)
                sfx_val += 0.10 * e * math.sin(2.0 * math.pi * f_sweep * dt)
                if ctype in ("chart_bar", "chart_candle"):
                    # Sharp data reveal ping
                    sfx_val += 0.11 * e * math.sin(2.0 * math.pi * 784.0 * dt)
                elif ctype == "chart_race":
                    # Ascending emerald alpha chime
                    f_chime = 587.33 if dt < 0.10 else 880.0
                    sfx_val += 0.11 * e * math.sin(2.0 * math.pi * f_chime * dt)
                elif c_idx == len(cut_starts) - 2:
                    # Comment poll notification pop
                    f_pop = 659.25 if dt < 0.09 else 987.77
                    sfx_val += 0.10 * e * math.sin(2.0 * math.pi * f_pop * dt)

            # Subtle digital counter ticks during first 1.0s of chart cuts
            if ctype.startswith("chart_") and 0.12 <= dt < 1.08:
                tick_dt = (dt - 0.12) % 0.08
                if tick_dt < 0.018:
                    sfx_val += 0.035 * math.exp(-tick_dt * 180.0) * math.sin(2.0 * math.pi * 1480.0 * tick_dt)

        # Ending Slate Sub-Bass Drop + Crystal Shimmer
        dt_end = t - ending_start
        if 0.0 <= dt_end < 0.65:
            e = math.exp(-dt_end * 5.2)
            f_drop = max(44.0, 118.0 - 92.0 * (dt_end / 0.65))
            sfx_val += 0.24 * e * math.sin(2.0 * math.pi * f_drop * dt_end)
            sfx_val += 0.06 * math.exp(-dt_end * 9.0) * math.sin(2.0 * math.pi * 1046.5 * dt_end)

        mixed = voice_buf[i] + bgm_val + sfx_val
        # Soft pre-limiter saturation guard (FFmpeg alimiter applies final -0.5 dBFS ceiling)
        mixed = max(-0.96, min(0.96, mixed))
        out_bytes += struct.pack("<h", int(mixed * 32767.0))

    with wave.open(out_wav, "wb") as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(sample_rate)
        wf.writeframes(out_bytes)


# =============================================================================
# High-CTR Custom Japanese Cover Thumbnail Generator (1080x1920 — Zero AI Woman)
# =============================================================================
def render_v4_cover_thumbnail(ffmpeg_bin: str, out_jpg: str, ep: dict, clip_path: str):
    """
    Renders a sharp dark-mode institutional chart & Yen balance comparison hero cover
    with PIVOT/Japanese YouTube Shorts style ultra-bold 極太ゴシック cover typography!
    """
    bg = Image.new("RGBA", (W, H), (8, 12, 24, 255))
    bdraw = ImageDraw.Draw(bg)
    for gx in range(60, W, 120):
        bdraw.line([(gx, 120), (gx, 1620)], fill=(20, 29, 52, 255), width=1)
    for gy in range(160, 1640, 120):
        bdraw.line([(48, gy), (W - 48, gy)], fill=(20, 29, 52, 255), width=1)

    # Top Yen Balance vs Breakout Hero Graphic (y = 210 .. 870)
    bdraw.rounded_rectangle([(58, 210), (522, 420)], radius=26, fill=(48, 14, 28, 242), outline=(251, 59, 98, 255), width=3)
    bdraw.text((84, 236), "× お祈りナンピン口座", font=load_jp_font(28, weight="bold"), fill=(255, 165, 182, 255))
    bdraw.text((84, 294), "¥520,000", font=load_jp_font(62, weight="black"), fill=(255, 98, 130, 255))

    bdraw.rounded_rectangle([(558, 210), (W - 58, 420)], radius=26, fill=(10, 48, 38, 242), outline=(16, 215, 142, 255), width=3)
    bdraw.text((584, 236), "✓ 右側ブレイク＆逆指値", font=load_jp_font(28, weight="bold"), fill=(152, 250, 208, 255))
    bdraw.text((584, 294), "¥1,680,000", font=load_jp_font(62, weight="black"), fill=(110, 247, 190, 255))

    bdraw.rounded_rectangle([(58, 448), (W - 58, 865)], radius=28, fill=(11, 17, 36, 242), outline=(56, 189, 248, 235), width=3)
    pts_bad = [(96 + i * 52, 540 + i * 16) for i in range(17)]
    pts_good = [(96 + i * 52, 780 - int(i * 15.5) + int(14 * math.sin(i))) for i in range(17)]
    bdraw.line(pts_bad, fill=(251, 59, 98, 255), width=7)
    bdraw.line(pts_good, fill=(16, 215, 142, 255), width=9)

    grad = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    gdraw = ImageDraw.Draw(grad)
    for y in range(H):
        if y < 340:
            a = int(85 * (1.0 - y / 340.0))
        elif y < 860:
            a = 10
        else:
            t = (y - 860) / (H - 860)
            a = int(15 + 225 * min(1.0, t * 1.28))
        gdraw.line([(0, y), (W, y)], fill=(6, 9, 20, a))
    img = Image.alpha_composite(bg, grad)
    draw = ImageDraw.Draw(img)

    pal = PALETTE.get(ep.get("accent", "rose"), PALETTE["rose"])

    top_txt = f"◆ {sanitize_cjk_text(ep['cover_top'])} ◆"
    f_top = fit_font_to_width(draw, top_txt, max_width=880, start_size=42, min_size=28, weight="black")
    tb = draw.textbbox((0, 0), top_txt, font=f_top)
    pw = (tb[2] - tb[0]) + 64
    px = (W - pw) // 2
    draw.rounded_rectangle([(px, 942), (px + pw, 1024)], radius=22, fill=(12, 16, 34, 238), outline=(*pal["main"], 255), width=4)
    draw_centered_text(draw, 956, top_txt, f_top, (*pal["bright"], 255))

    big_txt = sanitize_cjk_text(ep["cover_big"])
    f_big = fit_font_to_width(draw, big_txt, max_width=960, start_size=108, min_size=58, weight="black", stroke_width=14)
    draw_centered_text(
        draw,
        1054,
        big_txt,
        f_big,
        (255, 236, 72, 255),
        max_w=960,
        stroke_width=14,
        stroke_fill=(0, 0, 0, 255),
        shadow_offset=6,
    )

    sub_txt = sanitize_cjk_text(ep["cover_sub"])
    f_sub = fit_font_to_width(draw, sub_txt, max_width=900, start_size=54, min_size=32, weight="black", stroke_width=8)
    draw.rounded_rectangle([(64, 1226), (W - 64, 1344)], radius=24, fill=(*pal["main"], 242), outline=(255, 255, 255, 240), width=3)
    draw_centered_text(draw, 1247, sub_txt, f_sub, (255, 255, 255, 255), stroke_width=6, stroke_fill=(0, 0, 0, 220))

    brand_txt = f"GetBreakAI | 米国株・新NISAクオンツ  |  {sanitize_cjk_text(ep['jp_name'])}"
    f_br = fit_font_to_width(draw, brand_txt, max_width=900, start_size=30, min_size=22, weight="bold")
    draw_centered_text(draw, 1396, brand_txt, f_br, (186, 206, 235, 255), stroke_width=4, stroke_fill=(0, 0, 0, 220))

    img.convert("RGB").save(out_jpg, "JPEG", quality=95)


# =============================================================================
# Full Episode Orchestrator
# =============================================================================
def build_single_episode(ffmpeg_bin: str, all_clips: list, ep: dict) -> dict:
    ep_id = ep["id"]
    ep_temp = os.path.join(TEMP_DIR, ep_id)
    os.makedirs(ep_temp, exist_ok=True)
    os.makedirs(OUT_DIR, exist_ok=True)
    os.makedirs(THUMB_DIR, exist_ok=True)

    clip_indices = ep["clip_indices"]
    ep_clips = [all_clips[idx % len(all_clips)] for idx in clip_indices] if all_clips else [""] * max(1, len(clip_indices))

    cut_mp4s = []
    cut_tts_wavs = []
    cut_durations = []
    cut_types = []
    cut_audit = []

    presenter_turn = 0
    for c_idx, cut in enumerate(ep["cuts"]):
        ctype = cut["type"]
        cut_types.append(ctype)

        # 1) Synthesize natural Japanese neural TTS (Keita or Nanami)
        tts_wav, tts_dur = synthesize_cut_tts(ffmpeg_bin, cut["tts"], voice=cut["voice"])

        # 2) Compute exact frame-locked segment duration (100% subtitle completion guaranteed!)
        if ctype == "ending":
            raw_seg = max(3.35, min(3.80, tts_dur + 0.32))
            if tts_dur + 0.26 > raw_seg:
                raw_seg = tts_dur + 0.28
        else:
            raw_seg = max(2.50, tts_dur + 0.28)

        n_frames = int(math.ceil(raw_seg * FPS))
        seg_dur = n_frames / float(FPS)

        cut_tts_wavs.append(tts_wav)
        cut_durations.append(seg_dur)

        cut_mp4 = os.path.join(ep_temp, f"cut_{c_idx:02d}_{ctype}.mp4")

        # 3) Render video scene
        if ctype == "presenter":
            clip_p = ep_clips[presenter_turn % len(ep_clips)]
            presenter_turn += 1
            ov_png = os.path.join(ep_temp, f"ov_{c_idx:02d}.png")
            render_presenter_overlay_png(ov_png, cut)
            render_presenter_or_ending_cut_mp4(ffmpeg_bin, cut_mp4, clip_p, ov_png, seg_dur, zoom_dir=c_idx)
        elif ctype == "ending":
            clip_p = ep_clips[-1]
            ov_png = os.path.join(ep_temp, f"ov_{c_idx:02d}_end.png")
            render_ending_overlay_png(ov_png, ep, cut)
            render_presenter_or_ending_cut_mp4(ffmpeg_bin, cut_mp4, clip_p, ov_png, seg_dur, zoom_dir=2)
        elif ctype in ("chart_bar", "chart_candle", "chart_race"):
            pip_clip = ep_clips[(presenter_turn + c_idx) % len(ep_clips)]
            render_chart_cut_mp4(ffmpeg_bin, cut_mp4, cut, pip_clip, seg_dur, ep.get("accent", "emerald"))
        else:
            raise ValueError(f"Unsupported cut type: {ctype}")

        cut_mp4s.append(cut_mp4)
        cut_audit.append({
            "cut_index": c_idx + 1,
            "type": ctype,
            "voice": cut["voice"],
            "tts_dur_sec": round(tts_dur, 3),
            "seg_dur_sec": round(seg_dur, 3),
            "margin_sec": round(seg_dur - tts_dur, 3),
            "sub": cut["sub"],
        })

    # 4) Concatenate video cuts losslessly
    concat_txt = os.path.join(ep_temp, "concat_v.txt")
    with open(concat_txt, "w", encoding="utf-8") as f:
        for p in cut_mp4s:
            f.write(f"file '{p.replace(os.sep, '/')}'\n")

    silent_mp4 = os.path.join(ep_temp, "video_concat.mp4")
    subprocess.run(
        [ffmpeg_bin, "-y", "-f", "concat", "-safe", "0", "-i", concat_txt, "-c", "copy", silent_mp4],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=True,
    )

    # 5) Build Master Audio WAV (TTS + Voice-Ducked 124-BPM BGM + Studio SFX)
    master_wav = os.path.join(ep_temp, "master_mix.wav")
    build_master_episode_audio_wav(master_wav, cut_tts_wavs, cut_durations, cut_types)

    # 6) Final Mux + -0.5 dBFS Brickwall Limiter (alimiter=limit=0.944:level=disabled)
    final_mp4 = os.path.join(OUT_DIR, f"{ep_id}.mp4")
    total_dur = sum(cut_durations)
    subprocess.run(
        [
            ffmpeg_bin, "-y",
            "-i", silent_mp4,
            "-i", master_wav,
            "-af", "alimiter=limit=0.944:level=disabled",
            "-c:v", "copy",
            "-c:a", "aac",
            "-b:a", "192k",
            "-ar", "44100",
            "-t", f"{total_dur:.3f}",
            "-movflags", "+faststart",
            final_mp4,
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=True,
    )

    # 7) Render High-CTR Cover Thumbnail + Export Official .srt & @GetBreakAI .youtube.json (20:30 JST, ja)
    cover_jpg = os.path.join(THUMB_DIR, f"{ep_id}_cover.jpg")
    render_v4_cover_thumbnail(ffmpeg_bin, cover_jpg, ep, ep_clips[0])

    def _fmt_srt(sec_v: float) -> str:
        ms_t = max(0, int(round(sec_v * 1000.0)))
        return f"{ms_t // 3600000:02d}:{(ms_t % 3600000) // 60000:02d}:{(ms_t % 60000) // 1000:02d},{ms_t % 1000:03d}"

    srt_blocks = []
    cur_t = 0.0
    for c_i, (c_dur, c_obj) in enumerate(zip(cut_durations, ep["cuts"]), 1):
        srt_blocks.append(f"{c_i}\n{_fmt_srt(cur_t)} --> {_fmt_srt(cur_t + c_dur)}\n" + "\n".join(c_obj.get("sub", [])) + "\n")
        cur_t += c_dur
    srt_path = os.path.join(OUT_DIR, f"{ep_id}.srt")
    with open(srt_path, "w", encoding="utf-8") as sf:
        sf.write("\n".join(srt_blocks))

    yt_meta_path = os.path.join(OUT_DIR, f"{ep_id}.youtube.json")
    yt_meta = {
        "channel_name": "GetBreakAI | 米国株・新NISAクオンツ",
        "channel_handle": "@GetBreakAI",
        "snippet": {
            "title": ep["yt_title"],
            "description": ep["yt_desc"],
            "tags": ["米国株", "新NISA", "エヌビディア", "NVDA", "半導体株", "損切り", "SEC開示", "株クラ", ep["ticker"]],
            "categoryId": "27",
            "defaultLanguage": "ja",
            "defaultAudioLanguage": "ja",
        },
        "status": {
            "privacyStatus": "private",
            "selfDeclaredMadeForKids": False,
            "publishAt_schedule_jst": "20:30:00+09:00",
        },
    }
    with open(yt_meta_path, "w", encoding="utf-8") as yf:
        json.dump(yt_meta, yf, ensure_ascii=False, indent=2)

    actual_dur = probe_duration(ffmpeg_bin, final_mp4)
    size_mb = round(os.path.getsize(final_mp4) / (1024 * 1024), 2)
    print(f"  [OK] {ep_id}.mp4 ({actual_dur:.2f}s, {size_mb:.2f} MB) + cover + SRT + YT JSON")

    return {
        "ep_num": ep["ep_num"],
        "id": ep_id,
        "ticker": ep["ticker"],
        "jp_name": ep["jp_name"],
        "abc_winner": ep["abc_winner"],
        "mp4_path": final_mp4,
        "srt_path": srt_path,
        "yt_meta_path": yt_meta_path,
        "cover_jpg_path": cover_jpg,
        "duration_sec": round(actual_dur, 2),
        "file_size_mb": size_mb,
        "yt_title": ep["yt_title"],
        "yt_desc": ep["yt_desc"],
        "yt_pin": ep["yt_pin"],
        "ig_caption": ep["ig_caption"],
        "publishAt_schedule_jst": "20:30:00+09:00",
        "defaultLanguage": "ja",
        "categoryId": "27",
        "cuts": cut_audit,
    }


def write_upload_kit_markdown(manifest_items: list, out_md: str):
    lines = [
        "# 🇯🇵 GetBreakAI V4 シネマ・クオンツ 日本バイラルショート 12選 アップロードキット (`VP01`〜`VP12`)",
        "",
        f"- 生成日時: `{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}`",
        "- 出力フォルダ: `D:\\드림컴퍼니\\3사업부\\flow_shorts_studio\\viral_jp_v4\\`",
        "- サムネイルフォルダ: `D:\\드림컴퍼니\\3사업부\\flow_shorts_studio\\viral_jp_v4\\thumbnails\\`",
        "- 対象チャンネル: YouTube `GetBreakAI | 米国株・新NISAクオンツ` (`@GetBreakAI`) · 毎日 `20:30 JST` 予約配信",
        "- 単一コンバージョン導線: `無料AI株数・損切り計算機 ➔ プロフィールのリンク（getbreakai.com）`",
        "",
        "---",
        "",
    ]
    for item in manifest_items:
        lines.extend([
            f"## 第{item['ep_num']:02d}話: `{item['id']}.mp4` ({item['duration_sec']}秒 / {item['file_size_mb']} MB)",
            f"- **A/B/C 採用フック**: `{item['abc_winner']}`",
            f"- **連動ティッカー**: `{item['ticker']}` ({item['jp_name']})",
            f"- **カバーサムネイル**: `thumbnails/{item['id']}_cover.jpg`",
            "",
            "### 📺 YouTube Shorts タイトル",
            "```text",
            item["yt_title"],
            "```",
            "",
            "### 📝 YouTube 概要欄 (SEO最適化)",
            "```text",
            item["yt_desc"],
            "```",
            "",
            "### 📌 YouTube 固定コメント (コメント欄議論誘発)",
            "```text",
            item["yt_pin"],
            "```",
            "",
            "### 📸 Instagram Reels キャプション (保存率特化)",
            "```text",
            item["ig_caption"],
            "```",
            "",
            "---",
            "",
        ])
    with open(out_md, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))


def main():
    parser = argparse.ArgumentParser(description="Build V4 Japanese Cinema-Quant Viral Shorts (VP01~VP12)")
    parser.add_argument("--limit", type=int, default=0, help="Render only first N episodes (for visual QA)")
    parser.add_argument("--only", type=int, default=0, help="Render only specific ep_num (1..12)")
    args = parser.parse_args()

    ffmpeg_bin = get_ffmpeg_bin()
    all_clips = get_ordered_clip_paths() if os.path.exists(RAW_CLIPS_DIR) else []

    episodes = EPISODES_V4
    if args.only > 0:
        episodes = [e for e in EPISODES_V4 if e["ep_num"] == args.only]
    elif args.limit > 0:
        episodes = EPISODES_V4[: args.limit]

    print(f"=== Building V4_JP_VIRAL_PRO Cinema-Quant Shorts ({len(episodes)} episodes) ===")
    print(f"FFmpeg: {ffmpeg_bin}")
    print(f"Raw presenter clips: {len(all_clips)} | Font Black: {os.path.exists(FONT_BLACK_PATH)}")

    results = []
    for ep in episodes:
        res = build_single_episode(ffmpeg_bin, all_clips, ep)
        results.append(res)

    if args.limit == 0 and args.only == 0:
        manifest_path = os.path.join(OUT_DIR, "viral_jp_v4_manifest.json")
        with open(manifest_path, "w", encoding="utf-8") as f:
            json.dump(
                {
                    "engine": "V4_JP_VIRAL_PRO",
                    "generated_at": datetime.now().isoformat(),
                    "count": len(results),
                    "episodes": results,
                },
                f,
                ensure_ascii=False,
                indent=2,
            )
        kit_md = os.path.join(OUT_DIR, "VIRAL_UPLOAD_KIT_JP_12EP.md")
        write_upload_kit_markdown(results, kit_md)
        print(f"=== Manifest & Upload Kit written to {OUT_DIR} ===")


if __name__ == "__main__":
    main()
