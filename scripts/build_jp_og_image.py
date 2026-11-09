#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
scripts/build_jp_og_image.py
Generates 1200x630 dark-mode Japanese Open Graph preview image (og-preview.png) for GetBreakAI.com
"""
import os
from PIL import Image, ImageDraw, ImageFont

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT_PATH = os.path.join(ROOT_DIR, "og-preview.png")


def load_jp_font(size):
    candidates = [
        "C:/Windows/Fonts/YuGothB.ttc",
        "C:/Windows/Fonts/meiryob.ttc",
        "C:/Windows/Fonts/msgothic.ttc",
        "/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc",
        "/usr/share/fonts/truetype/noto/NotoSansCJK-Bold.ttc",
    ]
    for path in candidates:
        if os.path.exists(path):
            try:
                return ImageFont.truetype(path, size)
            except Exception:
                pass
    return ImageFont.load_default()


def build_og_image():
    W, H = 1200, 630
    img = Image.new("RGB", (W, H), (8, 6, 18))
    draw = ImageDraw.Draw(img)

    # Subtle grid & terminal glow accents
    for x in range(0, W, 60):
        draw.line([(x, 0), (x, H)], fill=(22, 18, 42), width=1)
    for y in range(0, H, 60):
        draw.line([(0, y), (W, y)], fill=(22, 18, 42), width=1)

    # Outer terminal frame
    draw.rounded_rectangle([(32, 32), (W - 32, H - 32)], radius=24, fill=(14, 11, 28), outline=(139, 92, 246), width=3)
    draw.rounded_rectangle([(56, 56), (480, 102)], radius=20, fill=(38, 24, 78), outline=(167, 139, 250), width=2)

    f_badge = load_jp_font(22)
    f_title = load_jp_font(44)
    f_sub = load_jp_font(27)
    f_card_h = load_jp_font(21)
    f_card_v = load_jp_font(30)

    draw.text((76, 67), "⚡ 米国株・新NISA・株クラ専用AI端末", font=f_badge, fill=(245, 158, 11))
    draw.text((56, 128), "GetBreakAI — 米国株SEC開示・", font=f_title, fill=(248, 250, 252))
    draw.text((56, 188), "インサイダー買い・ガンマスクイーズ", font=f_title, fill=(196, 181, 253))
    draw.text((56, 248), "AI日本語解読＆ATR損切り計算機", font=f_title, fill=(52, 211, 153))

    draw.text(
        (56, 322),
        "英語のSEC 8-K決算・Form-4役員買い・オプションGamma Wallを3秒で日本語化",
        font=f_sub,
        fill=(165, 158, 194),
    )

    cards = [
        ("$NVDA エヌビディア", "AIスコア 93.5 / GEX転換", "ATR損切り & 適正株数算出", (16, 185, 129)),
        ("$PLTR パランティア", "SEC 8-K 国防AI契約解析", "ダークプール機関買い 64%", (139, 92, 246)),
        ("$SMCI 会計リスク警告", "🔴 エントリー禁止判定", "10-K監査リスク・機関売り検知", (244, 63, 94)),
    ]
    cx = 56
    for title, line1, line2, col in cards:
        draw.rounded_rectangle([(cx, 390), (cx + 345, 540)], radius=16, fill=(20, 15, 38), outline=col, width=2)
        draw.text((cx + 20, 408), title, font=f_card_v, fill=(255, 255, 255))
        draw.text((cx + 20, 455), line1, font=f_card_h, fill=col)
        draw.text((cx + 20, 490), line2, font=f_card_h, fill=(203, 213, 225))
        cx += 368

    draw.text((56, 558), "https://getbreakai.com  |  ドル($)＆日本円(¥) 同時対応  |  Sister: TruthOfMarket.com", font=f_badge, fill=(245, 158, 11))
    img.save(OUT_PATH, "PNG", optimize=True)
    print(f"[OK] Generated Japanese OG image: {OUT_PATH} ({os.path.getsize(OUT_PATH)} bytes)")


if __name__ == "__main__":
    build_og_image()
