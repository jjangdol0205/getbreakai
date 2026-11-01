#!/usr/bin/env python3
"""
Generates YouTube Studio & Instagram Profile Assets for SemiFearGreed:
1. assets/youtube/youtube_profile_800x800.png (800x800 PNG)
2. assets/youtube/youtube_banner_2560x1440.png (2560x1440 PNG — YouTube Safe Area 1546x423 centered)
"""
import math
import shutil
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT_DIR = Path(__file__).resolve().parents[1]


def _load_font(size: int, bold: bool = True) -> ImageFont.FreeTypeFont:
    candidates = [
        "C:/Windows/Fonts/segoeuib.ttf" if bold else "C:/Windows/Fonts/segoeui.ttf",
        "C:/Windows/Fonts/arialbd.ttf" if bold else "C:/Windows/Fonts/arial.ttf",
        "C:/Windows/Fonts/malgunbd.ttf" if bold else "C:/Windows/Fonts/malgun.ttf",
    ]
    for c in candidates:
        if Path(c).exists():
            try:
                return ImageFont.truetype(c, size)
            except Exception:
                pass
    return ImageFont.load_default()


def _draw_grid(draw: ImageDraw.ImageDraw, w: int, h: int, step: int = 80) -> None:
    grid_color = (19, 28, 46)
    for x in range(0, w, step):
        draw.line([(x, 0), (x, h)], fill=grid_color, width=1)
    for y in range(0, h, step):
        draw.line([(0, y), (w, y)], fill=grid_color, width=1)


def _draw_gauge_icon(
    draw: ImageDraw.ImageDraw,
    cx: float,
    cy: float,
    radius: float,
    thickness: int,
    score: float = 18.0,
) -> None:
    """Draws the 5-segment Semiconductor Fear & Greed dial gauge and needle."""
    bbox = [cx - radius, cy - radius, cx + radius, cy + radius]
    # PIL angles: 0 is 3 o'clock, clockwise. Top semi-circle is 180° to 360°.
    segments = [
        (180, 214, (239, 68, 68)),    # Extreme Fear (Red)
        (217, 250, (249, 115, 22)),   # Fear (Orange)
        (253, 287, (148, 163, 184)),  # Neutral (Slate)
        (290, 323, (16, 185, 129)),   # Greed (Green)
        (326, 360, (5, 150, 105)),    # Extreme Greed (Deep Emerald)
    ]
    for start_a, end_a, col in segments:
        draw.arc(bbox, start=start_a, end=end_a, fill=col, width=thickness)

    # Needle pointing to score (0 -> 180 deg, 100 -> 360 deg)
    ang_deg = 180.0 + (max(0.0, min(100.0, score)) / 100.0) * 180.0
    ang_rad = math.radians(ang_deg)
    tip_r = radius - thickness * 0.65
    tip_x = cx + tip_r * math.cos(ang_rad)
    tip_y = cy + tip_r * math.sin(ang_rad)

    left_rad = ang_rad + math.pi / 2
    right_rad = ang_rad - math.pi / 2
    base_r = max(6.0, thickness * 0.24)
    bx1 = cx + base_r * math.cos(left_rad)
    by1 = cy + base_r * math.sin(left_rad)
    bx2 = cx + base_r * math.cos(right_rad)
    by2 = cy + base_r * math.sin(right_rad)

    draw.polygon([(tip_x, tip_y), (bx1, by1), (bx2, by2)], fill=(248, 250, 252))
    hub_r = max(10.0, thickness * 0.42)
    draw.ellipse([cx - hub_r, cy - hub_r, cx + hub_r, cy + hub_r], fill=(15, 23, 42), outline=(56, 189, 248), width=4)


def generate_profile_logo(out_path: Path) -> None:
    w, h = 800, 800
    img = Image.new("RGB", (w, h), (9, 13, 22))
    draw = ImageDraw.Draw(img)
    _draw_grid(draw, w, h, step=80)

    # Outer glowing ring
    margin = 36
    draw.ellipse([margin, margin, w - margin, h - margin], fill=(11, 17, 30), outline=(239, 68, 68), width=12)
    inner_m = 56
    draw.ellipse([inner_m, inner_m, w - inner_m, h - inner_m], outline=(56, 189, 248), width=3)

    # Draw Fear & Greed Gauge in center-top
    _draw_gauge_icon(draw, cx=400, cy=415, radius=235, thickness=44, score=18.0)

    # Score badge Pill
    pill_w, pill_h = 210, 62
    px1, py1 = 400 - pill_w // 2, 455
    draw.rounded_rectangle([px1, py1, px1 + pill_w, py1 + pill_h], radius=31, fill=(220, 38, 38))
    f_score = _load_font(34, bold=True)
    txt_score = "18 EXTREME"
    tb = draw.textbbox((0, 0), txt_score, font=f_score)
    draw.text((400 - (tb[2] - tb[0]) / 2, py1 + 10), txt_score, font=f_score, fill=(255, 255, 255))

    # Main Title: SEMI FEAR & GREED
    f_title = _load_font(62, bold=True)
    t1 = "SEMI FEAR"
    tb1 = draw.textbbox((0, 0), t1, font=f_title)
    draw.text((400 - (tb1[2] - tb1[0]) / 2, 540), t1, font=f_title, fill=(255, 255, 255))

    f_sub = _load_font(34, bold=True)
    t2 = "$SMH : $XLV QUANT"
    tb2 = draw.textbbox((0, 0), t2, font=f_sub)
    draw.text((400 - (tb2[2] - tb2[0]) / 2, 622), t2, font=f_sub, fill=(56, 189, 248))

    out_path.parent.mkdir(parents=True, exist_ok=True)
    img.save(out_path, format="PNG")


def generate_channel_banner(out_path: Path) -> None:
    w, h = 2560, 1440
    img = Image.new("RGB", (w, h), (9, 13, 22))
    draw = ImageDraw.Draw(img)
    _draw_grid(draw, w, h, step=80)

    # YouTube Safe Area is 1546 x 423 centered at (1280, 720)
    card_w, card_h = 1520, 404
    cx1 = (w - card_w) // 2
    cy1 = (h - card_h) // 2
    cx2 = cx1 + card_w
    cy2 = cy1 + card_h

    draw.rounded_rectangle(
        [cx1, cy1, cx2, cy2],
        radius=28,
        fill=(15, 23, 42),
        outline=(56, 189, 248),
        width=4,
    )

    # Left icon box inside card
    icon_box = [cx1 + 42, cy1 + 48, cx1 + 350, cy2 - 48]
    draw.rounded_rectangle(icon_box, radius=20, fill=(9, 13, 22), outline=(30, 41, 59), width=2)
    _draw_gauge_icon(draw, cx=cx1 + 196, cy=cy1 + 245, radius=112, thickness=24, score=18.0)

    f_mini = _load_font(22, bold=True)
    m_txt = "80% $SMH : 20% $XLV"
    mb = draw.textbbox((0, 0), m_txt, font=f_mini)
    draw.text((cx1 + 196 - (mb[2] - mb[0]) / 2, cy1 + 290), m_txt, font=f_mini, fill=(248, 113, 113))

    # Right text column
    tx = cx1 + 392
    f_kicker = _load_font(26, bold=True)
    draw.text(
        (tx, cy1 + 52),
        "INSTITUTIONAL SEMICONDUCTOR & AI CHIP QUANT TERMINAL",
        font=f_kicker,
        fill=(248, 113, 113),
    )

    f_main = _load_font(68, bold=True)
    draw.text(
        (tx, cy1 + 94),
        "SemiFearGreed | $SMH Quant",
        font=f_main,
        fill=(255, 255, 255),
    )

    f_desc = _load_font(28, bold=False)
    draw.text(
        (tx, cy1 + 194),
        "7-Factor Semi Fear & Greed Index  |  80:20 Contrarian Barbell  |  US 72-Stock PW-RSI",
        font=f_desc,
        fill=(203, 213, 225),
    )

    # Bottom CTA Pill inside safe zone
    pill_box = [tx, cy1 + 266, cx2 - 46, cy1 + 344]
    draw.rounded_rectangle(pill_box, radius=14, fill=(2, 132, 199))
    f_cta = _load_font(27, bold=True)
    draw.text(
        (tx + 24, cy1 + 288),
        "LIVE TERMINAL: TRUTHOFMARKET.COM   |   TELEGRAM: @SEMIFEARGREEDBOT",
        font=f_cta,
        fill=(255, 255, 255),
    )

    out_path.parent.mkdir(parents=True, exist_ok=True)
    img.save(out_path, format="PNG")


def main() -> None:
    yt_dir = ROOT_DIR / "assets" / "youtube"
    yt_dir.mkdir(parents=True, exist_ok=True)
    prof_path = yt_dir / "youtube_profile_800x800.png"
    ban_path = yt_dir / "youtube_banner_2560x1440.png"

    generate_profile_logo(prof_path)
    generate_channel_banner(ban_path)

    for target_root in [ROOT_DIR / "frontend" / "public" / "assets" / "youtube", ROOT_DIR / "dist" / "assets" / "youtube"]:
        target_root.mkdir(parents=True, exist_ok=True)
        shutil.copy2(prof_path, target_root / "youtube_profile_800x800.png")
        shutil.copy2(ban_path, target_root / "youtube_banner_2560x1440.png")

    print("Generated:", prof_path, ban_path)


if __name__ == "__main__":
    main()
