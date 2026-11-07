#!/usr/bin/env python3
"""
scripts/render_dual_yt_ig_cta.py
Generates two platform-specific videos from a single master MP4 (zero extra Flow generation load):
  1) <base>_YT_Shorts.mp4 : YouTube Shorts edition (Profile Tap + Pinned Comment CTA)
  2) <base>_IG_Reels.mp4  : Instagram Reels edition (ManyChat Comment Keyword -> Auto-DM CTA)

Harmonious Layout Rule:
  - Existing voice subtitles occupy y = 1335..1530 (69.5%..79.7% of 1080x1920).
  - The CTA pill is placed harmoniously right below the voice subtitles at y = 1558..1696 (81.1%..88.3%),
    using NanumSquareRoundEB.ttf with stroked text and matching Mint/Yellow accents so it never covers
    a single pixel of the voice subtitles and blends naturally with the video typography.
"""

import os
import re
import subprocess
import sys
import tempfile
import imageio_ffmpeg
from PIL import Image, ImageDraw, ImageFont

FFMPEG_EXE = imageio_ffmpeg.get_ffmpeg_exe()

FONT_CANDIDATES_KR = [
    r"D:\사업아이템\src\fonts\NanumSquareRoundEB.ttf",
    r"D:\사업아이템\src\fonts\Pretendard-ExtraBold.otf",
    r"C:\Windows\Fonts\malgunbd.ttf",
]

FONT_CANDIDATES_EN = [
    r"D:\사업아이템\src\fonts\Pretendard-ExtraBold.otf",
    r"D:\사업아이템\src\fonts\NanumSquareRoundEB.ttf",
    r"C:\Windows\Fonts\arialbd.ttf",
]


def load_font(size, is_kr=True):
    candidates = FONT_CANDIDATES_KR if is_kr else FONT_CANDIDATES_EN
    for fp in candidates:
        if os.path.exists(fp):
            try:
                return ImageFont.truetype(fp, size)
            except Exception:
                pass
    return ImageFont.load_default()


def get_video_info(video_path):
    res = subprocess.run(
        [FFMPEG_EXE, "-i", video_path],
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    info = res.stderr
    dur = 8.0
    m_dur = re.search(r"Duration:\s*(\d+):(\d+):(\d+(?:\.\d+)?)", info)
    if m_dur:
        dur = int(m_dur.group(1)) * 3600 + int(m_dur.group(2)) * 60 + float(m_dur.group(3))
    w, h = 1080, 1920
    m_dim = re.search(r"Stream #.*Video:.*?\s(\d{3,4})x(\d{3,4})", info)
    if m_dim:
        w, h = int(m_dim.group(1)), int(m_dim.group(2))
    return w, h, dur


def create_cta_overlay_png(width, height, badge_title, badge_sub, border_rgb, title_rgb, is_kr=True):
    img = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    box_w = int(width * 0.855)
    box_h = int(height * 0.072)
    x0 = (width - box_w) // 2
    # Placed harmoniously below voice subtitles (which end at ~79.5% height) and above platform bottom UI
    y0 = int(height * 0.812)
    x1 = x0 + box_w
    y1 = y0 + box_h

    # 100% opaque Midnight Navy pill (alpha=255) to guarantee zero ghosting over underlying text/video
    draw.rounded_rectangle(
        [x0, y0, x1, y1],
        radius=int(box_h * 0.28),
        fill=(10, 16, 28, 255),
        outline=border_rgb + (255,),
        width=4,
    )

    f_title = load_font(max(20, int(width * 0.036)), is_kr=is_kr)
    f_sub = load_font(max(16, int(width * 0.030)), is_kr=is_kr)

    tb1 = draw.textbbox((0, 0), badge_title, font=f_title)
    tw1 = tb1[2] - tb1[0]

    tb2 = draw.textbbox((0, 0), badge_sub, font=f_sub)
    tw2 = tb2[2] - tb2[0]

    ty1 = y0 + int(box_h * 0.14)
    ty2 = y0 + int(box_h * 0.56)

    draw.text(
        ((width - tw1) // 2, ty1),
        badge_title,
        font=f_title,
        fill=title_rgb + (255,),
        stroke_width=4,
        stroke_fill=(0, 0, 0, 230),
    )
    draw.text(
        ((width - tw2) // 2, ty2),
        badge_sub,
        font=f_sub,
        fill=(255, 255, 255, 255),
        stroke_width=3,
        stroke_fill=(0, 0, 0, 230),
    )

    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".png")
    img.save(tmp.name, "PNG")
    tmp.close()
    return tmp.name


def render_overlay_video(src_video, dst_video, png_path, start_sec):
    filter_complex = f"[0:v][1:v]overlay=0:0:enable='gte(t,{start_sec:.2f})'[v]"
    cmd = [
        FFMPEG_EXE,
        "-y",
        "-i",
        src_video,
        "-i",
        png_path,
        "-filter_complex",
        filter_complex,
        "-map",
        "[v]",
        "-map",
        "0:a?",
        "-c:v",
        "libx264",
        "-preset",
        "veryfast",
        "-crf",
        "20",
        "-c:a",
        "copy",
        "-movflags",
        "+faststart",
        dst_video,
    ]
    res = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace")
    if res.returncode != 0:
        raise RuntimeError(f"FFmpeg error: {res.stderr[-500:]}")


def ensure_dual_videos(src_video, division="KFG", force=False):
    if not os.path.exists(src_video):
        raise FileNotFoundError(src_video)

    base, ext = os.path.splitext(src_video)
    yt_out = f"{base}_YT_Shorts{ext}"
    ig_out = f"{base}_IG_Reels{ext}"

    if not force and os.path.exists(yt_out) and os.path.exists(ig_out):
        return yt_out, ig_out

    w, h, dur = get_video_info(src_video)
    # Show only during the final closing beat (~3.0 seconds) so it pairs naturally with the closing voice line
    start_sec = max(0.5, dur - 3.0)

    div = division.upper()
    if div == "TOM":
        yt_title = "▶ YOUTUBE SHORTS: TAP @rightsidealpha BELOW"
        yt_sub = "Click Profile Link & Pinned Comment -> Free US Stock Terminal"
        ig_title = '▶ INSTAGRAM REELS: COMMENT "ALPHA" BELOW'
        ig_sub = "We'll DM You the Direct Live Terminal Link in 1 Second!"
        png_yt = create_cta_overlay_png(w, h, yt_title, yt_sub, (110, 255, 210), (255, 232, 0), is_kr=False)
        png_ig = create_cta_overlay_png(w, h, ig_title, ig_sub, (255, 232, 0), (110, 255, 210), is_kr=False)
    elif div == "KFK":
        yt_title = "▶ 아래 @키즈핏 프로필 아이콘 터치!"
        yt_sub = "프로필 상단 링크에서 100% 무료 진단 & 공식 혜택가 보기"
        ig_title = '▶ 댓글에 "진단" 또는 "키즈핏" 입력!'
        ig_sub = "댓글 남기시면 1초 만에 DM으로 무료 진단 링크 발송!"
        png_yt = create_cta_overlay_png(w, h, yt_title, yt_sub, (110, 255, 210), (255, 232, 0), is_kr=True)
        png_ig = create_cta_overlay_png(w, h, ig_title, ig_sub, (255, 232, 0), (110, 255, 210), is_kr=True)
    else:
        yt_title = "▶ YOUTUBE SHORTS: TAP @kisfitglobal BELOW"
        yt_sub = "Click Channel Bio Link -> Free 30-Sec US CDC Growth Scan!"
        ig_title = '▶ INSTAGRAM REELS: COMMENT "GROWTH" BELOW'
        ig_sub = "We'll DM You the Free 30-Sec CDC Growth Report Link Instantly!"
        png_yt = create_cta_overlay_png(w, h, yt_title, yt_sub, (110, 255, 210), (255, 232, 0), is_kr=False)
        png_ig = create_cta_overlay_png(w, h, ig_title, ig_sub, (255, 232, 0), (110, 255, 210), is_kr=False)

    try:
        render_overlay_video(src_video, yt_out, png_yt, start_sec)
        render_overlay_video(src_video, ig_out, png_ig, start_sec)
    finally:
        for p in (png_yt, png_ig):
            if os.path.exists(p):
                try:
                    os.remove(p)
                except Exception:
                    pass

    return yt_out, ig_out


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python render_dual_yt_ig_cta.py <src_video> [TOM|KFG|KFK] [--force]")
        sys.exit(1)
    src = sys.argv[1]
    div = sys.argv[2] if len(sys.argv) >= 3 and not sys.argv[2].startswith("-") else "KFG"
    force = "--force" in sys.argv
    yt_path, ig_path = ensure_dual_videos(src, div, force=force)
    print(f"YT_SHORTS={yt_path}")
    print(f"IG_REELS={ig_path}")
