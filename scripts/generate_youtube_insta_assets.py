#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generates YouTube Studio & Instagram Official Brand Assets for Division 3 (GetBreakAI):
1. assets/youtube/youtube_profile_800x800.png (800x800 PNG — YouTube Profile & Watermark)
2. assets/youtube/getbreakai_profile_avatar_1024.png (1024x1024 PNG — Instagram & YouTube Circle-Safe)
3. assets/youtube/youtube_banner_2560x1440.png (2560x1440 PNG — YouTube Safe Area 1546x423 centered)
4. assets/youtube/youtube_insta_channel_config.json (Metadata for automated Studio setup)
"""
import json
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT_DIR = Path(__file__).resolve().parents[1]
YT_DIR = ROOT_DIR / "assets" / "youtube"


def _load_font(size: int, jp: bool = False, bold: bool = True) -> ImageFont.FreeTypeFont:
    if jp:
        candidates = [
            "C:/Windows/Fonts/YuGothB.ttc" if bold else "C:/Windows/Fonts/YuGothM.ttc",
            "C:/Windows/Fonts/msgothic.ttc",
            "C:/Windows/Fonts/malgunbd.ttf",
        ]
    else:
        candidates = [
            "C:/Windows/Fonts/segoeuib.ttf" if bold else "C:/Windows/Fonts/segoeui.ttf",
            "C:/Windows/Fonts/arialbd.ttf" if bold else "C:/Windows/Fonts/arial.ttf",
            "C:/Windows/Fonts/YuGothB.ttc",
        ]
    for c in candidates:
        if Path(c).exists():
            try:
                return ImageFont.truetype(c, size)
            except Exception:
                pass
    return ImageFont.load_default()


def _draw_grid(draw: ImageDraw.ImageDraw, w: int, h: int, step: int = 80) -> None:
    grid_color = (18, 28, 48)
    for x in range(0, w, step):
        draw.line([(x, 0), (x, h)], fill=grid_color, width=1)
    for y in range(0, h, step):
        draw.line([(0, y), (w, y)], fill=grid_color, width=1)


def _draw_breakout_emblem(draw: ImageDraw.ImageDraw, cx: int, cy: int, scale: float = 1.0) -> None:
    """Draws an institutional Donchian 20-Day Breakout + 2.0x ATR Shield graphic."""
    r = int(175 * scale)
    # Glowing dark inner circle
    draw.ellipse(
        [cx - r, cy - r, cx + r, cy + r],
        fill=(13, 22, 40),
        outline=(56, 189, 248),
        width=max(2, int(4 * scale)),
    )
    # 20-Day Donchian Resistance dashed horizontal line
    y_res = cy - int(35 * scale)
    for x in range(cx - int(130 * scale), cx + int(130 * scale), int(24 * scale)):
        draw.line(
            [(x, y_res), (min(x + int(14 * scale), cx + int(130 * scale)), y_res)],
            fill=(250, 204, 21),
            width=max(2, int(4 * scale)),
        )

    # Candlesticks leading to green breakout surge
    candles = [
        (-95, 55, 15, (148, 163, 184)),
        (-50, 40, -5, (56, 189, 248)),
        (-5, 20, -35, (16, 185, 129)),
        (45, -15, -95, (16, 185, 129)),
        (95, -55, -135, (52, 211, 153)),
    ]
    bw = int(22 * scale)
    for dx, y_low_off, y_high_off, col in candles:
        x_c = cx + int(dx * scale)
        y1 = cy + int(y_high_off * scale)
        y2 = cy + int(y_low_off * scale)
        # Wick
        draw.line([(x_c, y1 - int(14 * scale)), (x_c, y2 + int(14 * scale))], fill=col, width=max(2, int(4 * scale)))
        # Body
        draw.rounded_rectangle([x_c - bw // 2, y1, x_c + bw // 2, y2], radius=max(2, int(4 * scale)), fill=col)


def generate_profile_logo(out_path: Path, size: int = 800) -> None:
    w = h = size
    s = size / 800.0
    img = Image.new("RGB", (w, h), (9, 13, 24))
    draw = ImageDraw.Draw(img)
    _draw_grid(draw, w, h, step=int(64 * s))

    # Outer circle-safe rings
    m1 = int(34 * s)
    draw.ellipse([m1, m1, w - m1, h - m1], fill=(11, 18, 34), outline=(16, 185, 129), width=int(12 * s))
    m2 = int(54 * s)
    draw.ellipse([m2, m2, w - m2, h - m2], outline=(56, 189, 248), width=int(3 * s))

    # Draw Breakout Emblem in upper center
    _draw_breakout_emblem(draw, cx=w // 2, cy=int(275 * s), scale=0.95 * s)

    # Top pill badge: 20D BREAKOUT + 2.0x ATR
    pill_w, pill_h = int(440 * s), int(54 * s)
    px1, py1 = w // 2 - pill_w // 2, int(420 * s)
    draw.rounded_rectangle([px1, py1, px1 + pill_w, py1 + pill_h], radius=int(27 * s), fill=(5, 150, 105))
    f_badge = _load_font(int(24 * s), jp=False, bold=True)
    txt_b = "SEC 8-K  |  GAMMA  |  2.0x ATR"
    tb = draw.textbbox((0, 0), txt_b, font=f_badge)
    draw.text((w // 2 - (tb[2] - tb[0]) / 2, py1 + int(13 * s)), txt_b, font=f_badge, fill=(255, 255, 255))

    # Main Brand Title: GETBREAK AI
    f_title = _load_font(int(74 * s), jp=False, bold=True)
    t1 = "GETBREAK AI"
    tb1 = draw.textbbox((0, 0), t1, font=f_title)
    draw.text((w // 2 - (tb1[2] - tb1[0]) / 2, int(492 * s)), t1, font=f_title, fill=(255, 255, 255))

    # Japanese Subtitle: 米国株・日本株 クオンツAI
    f_jp = _load_font(int(36 * s), jp=True, bold=True)
    t2 = "米国株・新NISA クオンツAI"
    tb2 = draw.textbbox((0, 0), t2, font=f_jp)
    draw.text((w // 2 - (tb2[2] - tb2[0]) / 2, int(590 * s)), t2, font=f_jp, fill=(56, 189, 248))

    # Domain footer inside circle safe zone
    f_dom = _load_font(int(26 * s), jp=False, bold=True)
    t3 = "getbreakai.com"
    tb3 = draw.textbbox((0, 0), t3, font=f_dom)
    draw.text((w // 2 - (tb3[2] - tb3[0]) / 2, int(652 * s)), t3, font=f_dom, fill=(250, 204, 21))

    out_path.parent.mkdir(parents=True, exist_ok=True)
    img.save(out_path, format="PNG")


def generate_channel_banner(out_path: Path) -> None:
    w, h = 2560, 1440
    img = Image.new("RGB", (w, h), (9, 13, 24))
    draw = ImageDraw.Draw(img)
    _draw_grid(draw, w, h, step=80)

    # YouTube Safe Area is 1546 x 423 centered at (1280, 720) -> X: 507..2053, Y: 508..931
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

    # Left icon box inside safe card
    icon_box = [cx1 + 38, cy1 + 42, cx1 + 346, cy2 - 42]
    draw.rounded_rectangle(icon_box, radius=20, fill=(9, 13, 24), outline=(16, 185, 129), width=3)
    _draw_breakout_emblem(draw, cx=cx1 + 192, cy=cy1 + 185, scale=0.68)

    f_mini = _load_font(22, jp=False, bold=True)
    m_txt = "US TECH & TSE PRIME"
    mb = draw.textbbox((0, 0), m_txt, font=f_mini)
    draw.text((cx1 + 192 - (mb[2] - mb[0]) / 2, cy1 + 318), m_txt, font=f_mini, fill=(52, 211, 153))

    # Right text column inside safe zone
    tx = cx1 + 384
    f_kicker = _load_font(25, jp=False, bold=True)
    draw.text(
        (tx, cy1 + 44),
        "WALL STREET SEC 8-K & GAMMA WALL  |  20-DAY DONCHIAN & 2.0x ATR ENGINE",
        font=f_kicker,
        fill=(52, 211, 153),
    )

    f_main = _load_font(58, jp=True, bold=True)
    draw.text(
        (tx, cy1 + 88),
        "GetBreakAI | 米国株・日本株 クオンツAI",
        font=f_main,
        fill=(255, 255, 255),
    )

    f_desc = _load_font(24, jp=True, bold=True)
    draw.text(
        (tx, cy1 + 188),
        "SEC一次情報 × オプションGamma需給 × 2.0x ATR逆指値・新NISA適正株数シミュレーター",
        font=f_desc,
        fill=(203, 213, 225),
    )

    # Bottom CTA Pill inside safe zone
    pill_box = [tx, cy1 + 262, cx2 - 42, cy1 + 348]
    draw.rounded_rectangle(pill_box, radius=14, fill=(5, 150, 105), outline=(250, 204, 21), width=2)
    f_cta = _load_font(27, jp=True, bold=True)
    draw.text(
        (tx + 28, cy1 + 288),
        "無料AI株数・損切り計算機 -> getbreakai.com   |   Telegram: @SemifearGreedbot",
        font=f_cta,
        fill=(255, 255, 255),
    )

    out_path.parent.mkdir(parents=True, exist_ok=True)
    img.save(out_path, format="PNG")


def save_channel_config() -> Path:
    config = {
        "division": "3사업부 (GetBreakAI)",
        "domain": "https://getbreakai.com",
        "jp_research_hub": "https://getbreakai.com/jp/",
        "telegram_bot": "@SemifearGreedbot",
        "youtube": {
            "channel_name": "GetBreakAI | 米国株・新NISA クオンツAI",
            "handle_candidates": ["GetBreakAI", "GetBreakAI_JP", "GetBreakAIQuant"],
            "description": (
                "📊 ウォール街の機関投資家が使う「3大一次情報＋2.0x ATR資金管理」を完全日本語化！\n"
                "米国株（NVDA・PLTR・TSLA・SOXL）＆東証プライム主力株（東京エレクトロン・アドバンテスト・ソフトバンクG・トヨタ・ソニー）の機関ブレイクアウトシグナルを毎日配信。\n\n"
                "✅ 英語のSEC 8-K（重要契約・決算）＆Form-4（役員の自社株買い）を3秒でAI日本語要約\n"
                "✅ オプション市場のGamma壁（コール/プット需給）と20日ドンチャン・ブレイクアウト検知\n"
                "✅ 14日ATR（平均値動き幅）から口座資金1.5%リスク以内の「適正購入株数」と「2.0x ATR逆指値ライン」をドル＆日本円で自動計算\n"
                "✅ 新NISA（成長投資枠・非課税0%）と特定口座（20.315%課税）の手取り純利益をワンタッチ比較！\n\n"
                "👇 登録不要・3秒で使える無料ATR株数＆損切り計算機はこちら\n"
                "https://getbreakai.com\n\n"
                "📚 米国株・新NISA 30銘柄ディープリサーチ一覧\n"
                "https://getbreakai.com/jp/\n\n"
                "📲 VIP機関シグナル速報 Telegramボット\n"
                "https://t.me/SemifearGreedbot\n\n"
                "📩 お問い合わせ・提携: beable9489@gmail.com"
            ),
            "links": [
                {"title": "無料AI株数・損切り計算機 (GetBreakAI)", "url": "https://getbreakai.com"},
                {"title": "米国株・新NISA 30銘柄AIリサーチ", "url": "https://getbreakai.com/jp/"},
                {"title": "VIP Telegram シグナル速報", "url": "https://t.me/SemifearGreedbot"},
            ],
            "keywords": "米国株 新NISA エヌビディア NVDA パランティア PLTR テスラ TSLA SOXL 半導体株 東京エレクトロン アドバンテスト 株式投資 スイングトレード 損切り ATR クオンツ投資 GetBreakAI",
            "contact_email": "beable9489@gmail.com",
            "profile_image": str(YT_DIR / "youtube_profile_800x800.png"),
            "banner_image": str(YT_DIR / "youtube_banner_2560x1440.png"),
        },
        "instagram": {
            "name": "GetBreakAI | 米国株・新NISA クオンツAI📊",
            "username_candidates": ["getbreakai", "getbreakai.jp", "getbreakai_quant"],
            "bio": (
                "📊 米国株・東証プライムの機関投資家ブレイクアウトAI\n"
                "🔥 SEC開示・Gamma壁・20日高値突破を毎日速報\n"
                "🛡️ 2.0x ATR逆指値＆新NISA適正株数をドル/円で3秒計算\n"
                "👇 無料AI株数・損切りシミュレーターはこちら"
            ),
            "website": "https://getbreakai.com",
            "profile_image": str(YT_DIR / "getbreakai_profile_avatar_1024.png"),
        },
    }
    cfg_path = YT_DIR / "youtube_insta_channel_config.json"
    cfg_path.write_text(json.dumps(config, ensure_ascii=False, indent=2), encoding="utf-8")
    return cfg_path


def main() -> None:
    YT_DIR.mkdir(parents=True, exist_ok=True)
    prof_800 = YT_DIR / "youtube_profile_800x800.png"
    prof_1024 = YT_DIR / "getbreakai_profile_avatar_1024.png"
    banner_2560 = YT_DIR / "youtube_banner_2560x1440.png"

    generate_profile_logo(prof_800, size=800)
    generate_profile_logo(prof_1024, size=1024)
    generate_channel_banner(banner_2560)
    cfg_path = save_channel_config()

    print(f"[OK] Profile 800x800:  {prof_800}")
    print(f"[OK] Avatar 1024x1024: {prof_1024}")
    print(f"[OK] Banner 2560x1440: {banner_2560}")
    print(f"[OK] Channel Config:   {cfg_path}")


if __name__ == "__main__":
    main()
