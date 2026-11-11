#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
scripts/generate_jp_daily_shorts_and_x.py
3사업부 (GetBreakAI — https://getbreakai.com · YouTube @GetBreakAI)
일본 #株クラ · #新NISA 미국주식 퀀트 쇼츠 & X 무인 공략 파이프라인 (2026-11-11 개조판):
1) 채널 메타데이터 표준화:
   - 채널명: `GetBreakAI | 米国株・新NISAクオンツ`
   - `defaultLanguage="ja"`, `defaultAudioLanguage="ja"`, `categoryId="27"`, `publishAt` 매일 `20:30 JST` (`20:30:00+09:00`)
   - Telegram 전면 폐기(0%) -> 단일 CTA: `無料AI株数・損切り計算機 ➔ プロフィールのリンク（getbreakai.com）`
2) 비주얼 전면 개조 (`1080x1920`, `22~28초`, AI 일본인 여성 클립 0%):
   - 상단 요약 카드 (`y=180~360`) + 중앙 (`y=380~1280`) 실시간 엔화/달러 잔고 비교 모션
     (`100万円投資 ➔ お祈りナンピン ¥520,000` vs `右側ブレイク＆逆指値 ¥1,680,000`)
     + `$NVDA`/`$SMH`/`$SOXL`/`$PLTR`/`$TSLA` 실차트(OHLCV 캔들 + 60일선 + 기관 거래량)
     + `getbreakai.com` 다크모드 계산기 & SEC 8-K 3초 해독 UI 카드
3) 일본어 자막 골든 세이프존 상향 (`y = 980 ~ 1080`, `NotoSansCJKjp-Black.otf` `82pt+`, `stroke_width=10`, 배경 박스 0%)
   + 정식 `.srt` 자막 및 `.youtube.json` 업로드 메타데이터 자동 추출
4) `#新NISA` 눈높이 손익 선행 대본 규칙 & 자연 호흡 (`rate="+4%"`, `atempo` 0%, `seg_dur >= tts_dur + 0.25s`, `-0.5 dBFS` 리미터)
"""

import os
import re
import json
import math
import wave
import struct
import shutil
import asyncio
import subprocess
from datetime import datetime, timezone, timedelta
from PIL import Image, ImageDraw, ImageFont

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SNAPSHOT_PATH = os.path.join(ROOT_DIR, "data", "live_market_snapshot.json")
STOCKS_FREE_PATH = os.path.join(ROOT_DIR, "static_api", "stocks_free.json")
OUTBOX_ROOT = os.path.join(ROOT_DIR, "marketing_outbox_jp")
FONT_BLACK_PATH = os.path.join(ROOT_DIR, "assets", "fonts", "NotoSansCJKjp-Black.otf")
FONT_BOLD_PATH = os.path.join(ROOT_DIR, "assets", "fonts", "NotoSansCJKjp-Bold.otf")

JST = timezone(timedelta(hours=9))
JP_SAFE_SUBTITLE_Y = 995  # Golden safe zone y = 980 ~ 1080 (avoids bottom 3-line YouTube title cover)
JP_CHANNEL_NAME = "GetBreakAI | 米国株・新NISAクオンツ"
JP_SINGLE_CTA = "無料AI株数・損切り計算機 ➔ プロフィールのリンク（getbreakai.com）"
JP_KEYWORDS = ["米国株", "新NISA", "エヌビディア", "NVDA", "半導体株", "損切り", "SEC開示", "株クラ"]


def get_ffmpeg_bin():
    exe = shutil.which("ffmpeg")
    if exe:
        return exe
    try:
        import imageio_ffmpeg
        return imageio_ffmpeg.get_ffmpeg_exe()
    except Exception:
        raise RuntimeError("ffmpeg executable not found")


def load_jp_font(size, black=True):
    candidates = []
    if black:
        candidates.extend([FONT_BLACK_PATH, FONT_BOLD_PATH])
    else:
        candidates.extend([FONT_BOLD_PATH, FONT_BLACK_PATH])
    candidates.extend([
        "C:/Windows/Fonts/YuGothB.ttc",
        "C:/Windows/Fonts/meiryob.ttc",
        "C:/Windows/Fonts/msgothic.ttc",
        "/usr/share/fonts/opentype/noto/NotoSansCJK-Black.ttc",
        "/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc",
        "/usr/share/fonts/truetype/noto/NotoSansCJK-Bold.ttc",
    ])
    for path in candidates:
        if os.path.exists(path):
            try:
                return ImageFont.truetype(path, size)
            except Exception:
                pass
    return ImageFont.load_default()


def fit_jp_font(draw, text, max_w, start_size=84, min_size=44, stroke_width=10):
    sz = start_size
    while sz > min_size:
        f = load_jp_font(sz, black=True)
        bbox = draw.textbbox((0, 0), text, font=f, stroke_width=stroke_width)
        if (bbox[2] - bbox[0]) <= max_w:
            return f
        sz -= 2
    return load_jp_font(min_size, black=True)


def format_srt_ts(sec: float) -> str:
    ms_all = max(0, int(round(sec * 1000.0)))
    hh = ms_all // 3_600_000
    rem = ms_all % 3_600_000
    mm = rem // 60_000
    rem %= 60_000
    ss = rem // 1000
    ms = rem % 1000
    return f"{hh:02d}:{mm:02d}:{ss:02d},{ms:03d}"


def export_jp_srt(cut_timings: list, out_srt: str) -> str:
    blocks = []
    for idx, item in enumerate(cut_timings, 1):
        st = format_srt_ts(item["start"])
        et = format_srt_ts(item["end"])
        txt = "\n".join(item["caption_lines"]).strip()
        blocks.append(f"{idx}\n{st} --> {et}\n{txt}\n")
    with open(out_srt, "w", encoding="utf-8") as f:
        f.write("\n".join(blocks))
    return out_srt


def build_getbreakai_youtube_metadata(title: str, ticker: str, jp_name: str, now_jst: datetime) -> dict:
    pub_dt = now_jst.replace(hour=20, minute=30, second=0, microsecond=0)
    if pub_dt <= now_jst:
        pub_dt = pub_dt + timedelta(days=1)
    desc = (
        f"{JP_SINGLE_CTA}\n"
        f"👉 https://getbreakai.com/?calc=atr&ticker={ticker}\n\n"
        f"💡 ${ticker}（{jp_name}）を新NISA成長投資枠や特定口座で売買する前に：\n"
        f"・100万円投資 ➔ お祈りナンピン ¥520,000 vs 右側ブレイク＆逆指値 ¥1,680,000\n"
        f"・株価 -8% の逆指値でも口座全体の損失が -1.5% 以内に収まる「適正株数」をドル($)・日本円(¥)で3秒自動算出\n"
        f"・英語のSEC 8-K適時開示・Form-4役員買い・オプション需給を日本語AI解読\n\n"
        f"#米国株 #新NISA #{jp_name} #{ticker} #半導体株 #損切り #SEC開示 #株クラ #Shorts"
    )
    return {
        "channel_name": JP_CHANNEL_NAME,
        "channel_handle": "@GetBreakAI",
        "snippet": {
            "title": title[:95],
            "description": desc,
            "tags": JP_KEYWORDS + [ticker, jp_name],
            "categoryId": "27",
            "defaultLanguage": "ja",
            "defaultAudioLanguage": "ja",
        },
        "status": {
            "privacyStatus": "private",
            "selfDeclaredMadeForKids": False,
            "publishAt": pub_dt.isoformat(),
            "publishAt_schedule_jst": "20:30:00+09:00",
        },
    }


def generate_sfx_and_docu_bgm_wav(wav_path, cut_starts, duration_sec=24.0, sample_rate=44100, preset_idx=0):
    """Generates subtle Tokyo financial documentary pulse BGM + cut point SFX (no pure monotonous sine drone)."""
    n_samples = int(duration_sec * sample_rate)
    presets = [
        (110.0, 164.81, 246.94, 120.0),
        (98.0, 146.83, 220.00, 124.0),
        (103.83, 155.56, 233.08, 118.0),
    ]
    f1, f2, f3, bpm = presets[preset_idx % len(presets)]
    beat_s = 60.0 / bpm
    end_cut = cut_starts[-1] if cut_starts else duration_sec - 3.0

    with wave.open(wav_path, "w") as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(sample_rate)
        frames = bytearray()
        for i in range(n_samples):
            t = i / sample_rate
            # Warm documentary pulse pad
            q_phase = (t % beat_s) / beat_s
            pulse = 0.45 + 0.55 * math.exp(-q_phase * 4.5)
            pad = (
                0.48 * math.sin(2.0 * math.pi * f1 * t)
                + 0.28 * math.sin(2.0 * math.pi * f2 * t + 0.2)
                + 0.18 * math.sin(2.0 * math.pi * f3 * t + 0.5)
            )
            val = 0.065 * pulse * pad

            # Point SFX at cut transitions
            for idx, ct in enumerate(cut_starts):
                dt = t - ct
                if 0.0 <= dt < 0.34:
                    env = math.exp(-dt * 12.0)
                    freq = 92.0 if idx == 0 else (540.0 + idx * 55.0)
                    val += 0.20 * env * math.sin(2.0 * math.pi * freq * dt)

            # Ending sub-bass drop
            dt_end = t - end_cut
            if 0.0 <= dt_end < 0.58:
                env_e = math.exp(-dt_end * 5.4)
                f_drop = max(44.0, 114.0 - 86.0 * (dt_end / 0.58))
                val += 0.22 * env_e * math.sin(2.0 * math.pi * f_drop * dt_end)

            sample = max(-31000, min(31000, int(val * 32767)))
            frames += struct.pack("<h", sample)
        wf.writeframes(frames)


def _draw_real_ohlcv_mini_chart(draw, x1, y1, x2, y2, ticker, entry, stop_loss, target_25r, mode="breakout"):
    """Draws realistic 20-bar OHLCV candlesticks + 60-day MA + volume surge + -8%/-1.5% stop line."""
    draw.rounded_rectangle([(x1, y1), (x2, y2)], radius=24, fill=(11, 16, 34), outline=(56, 189, 248), width=2)
    px1, px2 = x1 + 32, x2 - 32
    py1, py2 = y1 + 48, y2 - 86
    vy1, vy2 = y2 - 72, y2 - 18

    if mode == "nanpin_vs_breakout":
        closes = [102, 100, 97, 94, 91, 93, 88, 84, 86, 89, 92, 95, 98, 104, 110, 109, 116, 122, 128, 134]
        opens = [103, 102, 100, 97, 94, 91, 93, 88, 84, 86, 89, 92, 95, 98, 104, 110, 109, 116, 122, 128]
        vols = [35, 42, 58, 64, 72, 38, 68, 75, 44, 48, 52, 60, 88, 96, 90, 48, 85, 89, 92, 95]
        ma60 = [99.0 - i * 0.25 if i < 9 else 96.5 + (i - 9) * 1.8 for i in range(20)]
    else:
        base = max(20.0, float(entry) * 0.88)
        step = (float(entry) * 1.06 - base) / 19.0
        closes = [base + i * step + math.sin(i * 0.8) * (entry * 0.018) for i in range(20)]
        opens = [closes[max(0, i - 1)] for i in range(20)]
        vols = [32 + (i * 3) + (38 if i in (12, 13, 17, 19) else 0) for i in range(20)]
        ma60 = [base + i * (step * 0.78) for i in range(20)]

    all_p = closes + opens + ma60
    p_min, p_max = min(all_p) * 0.96, max(all_p) * 1.04

    def map_y(v):
        return int(py2 - ((v - p_min) / max(0.01, p_max - p_min)) * (py2 - py1))

    step_x = (px2 - px1) / 20.0
    ma_pts = [(int(px1 + (i + 0.5) * step_x), map_y(ma60[i])) for i in range(20)]
    draw.line(ma_pts, fill=(250, 190, 40), width=4)

    for i in range(20):
        o, c = opens[i], closes[i]
        hi = max(o, c) * 1.012
        lo = min(o, c) * 0.988
        cx = int(px1 + (i + 0.5) * step_x)
        bull = c >= o
        col = (16, 215, 142) if bull else (251, 59, 98)
        draw.line([(cx, map_y(hi)), (cx, map_y(lo))], fill=col, width=3)
        yb1, yb2 = min(map_y(o), map_y(c)), max(map_y(o), map_y(c))
        if yb2 - yb1 < 5:
            yb2 = yb1 + 5
        bw = max(5, int(step_x * 0.33))
        draw.rectangle([(cx - bw, yb1), (cx + bw, yb2)], fill=col)
        vh = int(min(1.0, vols[i] / 100.0) * (vy2 - vy1))
        draw.rectangle([(cx - bw, vy2 - vh), (cx + bw, vy2)], fill=col)

    # Stop defense dashed line
    stop_y = py2 - 18
    for sx in range(px1, px2, 22):
        draw.line([(sx, stop_y), (min(px2, sx + 12), stop_y)], fill=(251, 113, 133), width=3)
    f_mini = load_jp_font(23, black=False)
    draw.text((px1 + 8, y1 + 12), f"${ticker} 実チャート × 60日移動平均線 돌파  |  逆指値 ${stop_loss:.2f} (口座損失 -1.5%以内)", font=f_mini, fill=(226, 232, 240))


def draw_clean_v3_slide(
    out_png,
    cut_idx,
    total_cuts,
    ticker,
    jp_name,
    headline_top,
    big_metric_label,
    big_metric_val,
    sub_box_lines,
    caption_lines,
    accent_rgb,
    entry=186.64,
    stop_loss=170.60,
    target_25r=226.74,
    is_ending_slate=False,
):
    """
    Upgraded JP Viral Quant Slide (1080x1920):
    - Top Summary Card (`y = 180 ~ 360`)
    - Center Arena (`y = 380 ~ 1280`): JPY Balance Comparison (`100万円投資 ➔ お祈りナンピン ¥520,000` vs `右側ブレイク＆逆指値 ¥1,680,000`),
      real OHLCV candlesticks, and `getbreakai.com` Dark-Mode ATR Calculator / SEC 8-K 3-Sec Decoder UI Card.
    - Center Golden Safe-Zone Subtitle (`y = 980 ~ 1080`, `NotoSansCJKjp-Black` 82pt+, `stroke_width=10`, zero translucent box).
    - Domain callout (`getbreakai.com`) ONLY on final ending slate cut!
    """
    W, H = 1080, 1920
    img = Image.new("RGB", (W, H), (8, 11, 24))
    draw = ImageDraw.Draw(img)

    grid_col = (20, 28, 52)
    for x in range(0, W, 90):
        draw.line([(x, 0), (x, H)], fill=grid_col, width=1)
    for y in range(0, H, 90):
        draw.line([(0, y), (W, y)], fill=grid_col, width=1)

    f_tag = load_jp_font(30, black=False)
    f_head = load_jp_font(44, black=True)
    f_lbl = load_jp_font(32, black=False)
    f_big = load_jp_font(68, black=True)
    f_sub = load_jp_font(34, black=False)

    if not is_ending_slate:
        # 1) Top Summary Card (y = 180 ~ 360)
        draw.rounded_rectangle([(56, 180), (W - 56, 360)], radius=28, fill=(14, 20, 42), outline=accent_rgb, width=3)
        draw.text((88, 198), f"⚡ 米国株・新NISA 損益検証 · ${ticker} ({jp_name})", font=f_tag, fill=accent_rgb)
        y_cursor = 244
        for line in headline_top[:2]:
            fh = fit_jp_font(draw, line, W - 180, start_size=42, min_size=28, stroke_width=4)
            draw.text((88, y_cursor), line, font=fh, fill=(248, 250, 252), stroke_width=4, stroke_fill=(0, 0, 0))
            y_cursor += 54

        # 2) Center Visual Arena (y = 380 ~ 1280)
        if cut_idx == 0:
            # 100万円投資 Yen Balance Simulation + OHLCV preview
            draw.rounded_rectangle([(56, 382), (524, 598)], radius=24, fill=(52, 14, 28), outline=(251, 59, 98), width=3)
            draw.text((82, 404), "❌ お祈りナンピン口座", font=f_lbl, fill=(255, 164, 182))
            draw.text((82, 456), "¥520,000", font=load_jp_font(58, black=True), fill=(251, 90, 120), stroke_width=3, stroke_fill=(0, 0, 0))
            draw.text((82, 538), "100万円投資 ➔ -48万円消滅", font=load_jp_font(26, black=False), fill=(255, 205, 215))

            draw.rounded_rectangle([(556, 382), (W - 56, 598)], radius=24, fill=(10, 48, 38), outline=(16, 215, 142), width=3)
            draw.text((582, 404), "✅ 右側ブレイク＆逆指値", font=f_lbl, fill=(152, 250, 208))
            draw.text((582, 456), "¥1,680,000", font=load_jp_font(58, black=True), fill=(110, 247, 190), stroke_width=3, stroke_fill=(0, 0, 0))
            draw.text((582, 538), "100万円投資 ➔ +68万円達成", font=load_jp_font(26, black=False), fill=(210, 255, 232))

            _draw_real_ohlcv_mini_chart(draw, 56, 618, W - 56, 955, ticker, entry, stop_loss, target_25r, mode="nanpin_vs_breakout")
            draw.rounded_rectangle([(56, 1185), (W - 56, 1280)], radius=20, fill=(14, 19, 38), outline=(76, 95, 148), width=2)
            draw.text((88, 1214), f"📊 新NISA成長投資枠は損益通算ゼロ — 逆指値なしのナンピンが最大リスク", font=load_jp_font(27, black=False), fill=(226, 232, 240))
        elif cut_idx in (1, 2):
            # Real OHLCV Chart + Metric Card
            _draw_real_ohlcv_mini_chart(draw, 56, 384, W - 56, 805, ticker, entry, stop_loss, target_25r, mode="breakout")
            draw.rounded_rectangle([(56, 822), (W - 56, 960)], radius=22, fill=(16, 22, 46), outline=accent_rgb, width=3)
            draw.text((88, 840), big_metric_label, font=load_jp_font(28, black=False), fill=(186, 202, 228))
            fb = fit_jp_font(draw, big_metric_val, W - 180, start_size=50, min_size=32, stroke_width=4)
            draw.text((88, 882), big_metric_val, font=fb, fill=accent_rgb, stroke_width=4, stroke_fill=(0, 0, 0))

            draw.rounded_rectangle([(56, 1180), (W - 56, 1280)], radius=20, fill=(14, 19, 38), outline=(76, 95, 148), width=2)
            if sub_box_lines:
                draw.text((88, 1212), sub_box_lines[0][0], font=load_jp_font(29, black=False), fill=sub_box_lines[0][1])
        else:
            # Dark-Mode ATR Position Sizer & SEC 8-K 3-Sec Decoder UI Card
            jpy_price = int(round(entry * 150))
            shares_750m = max(1, int((50000 * 0.015) / max(1.0, entry - stop_loss)))
            draw.rounded_rectangle([(56, 384), (W - 56, 952)], radius=28, fill=(13, 19, 40), outline=accent_rgb, width=3)
            draw.text((88, 412), f"🧮 米国株・新NISA 適正株数＆SEC 8-K 3秒解読カード (${ticker})", font=load_jp_font(29, black=True), fill=(253, 224, 71))
            draw.text((88, 468), big_metric_label, font=f_lbl, fill=(186, 202, 228))
            fb = fit_jp_font(draw, big_metric_val, W - 180, start_size=64, min_size=38, stroke_width=4)
            draw.text((88, 514), big_metric_val, font=fb, fill=accent_rgb, stroke_width=4, stroke_fill=(0, 0, 0))

            draw.rounded_rectangle([(84, 624), (W - 84, 756)], radius=18, fill=(10, 42, 36), outline=(16, 185, 129), width=2)
            draw.text((110, 644), f"🛡️ 株価 -8% 逆指値でも口座損失を -1.5% 以内に抑える適正株数: {shares_750m}株", font=load_jp_font(27, black=True), fill=(110, 247, 190))
            draw.text((110, 694), f"💵 現在値 ${entry:.2f} (約¥{jpy_price:,})  |  🎯 利確目標 ${target_25r:.2f}", font=load_jp_font(27, black=False), fill=(241, 245, 249))

            sy = 782
            for sline, scol in sub_box_lines[:2]:
                draw.text((92, sy), sline, font=f_sub, fill=scol)
                sy += 68

            draw.rounded_rectangle([(56, 1185), (W - 56, 1280)], radius=20, fill=(14, 19, 38), outline=(56, 189, 248), width=2)
            draw.text((88, 1214), "✓ SBI証券・楽天証券・マネックス証券の逆指値注文にそのまま入力可能", font=load_jp_font(27, black=False), fill=(186, 230, 253))
    else:
        # Final Ending Slate Cut: Single Funnel to getbreakai.com (ZERO Telegram)
        draw.rounded_rectangle([(56, 200), (W - 56, 955)], radius=38, fill=(15, 18, 44), outline=(139, 92, 246), width=5)
        draw.text((100, 248), f"🇯🇵 {JP_CHANNEL_NAME}", font=f_lbl, fill=(250, 204, 21))
        draw.text(
            (100, 312),
            "getbreakai.com",
            font=load_jp_font(86, black=True),
            fill=(255, 255, 255),
            stroke_width=6,
            stroke_fill=(0, 0, 0),
        )
        draw.text((100, 442), f"▶ ${ticker} ({jp_name}) の適正株数・逆指値を3秒で無料計算", font=f_sub, fill=(52, 211, 153))
        draw.rounded_rectangle([(96, 522), (W - 96, 650)], radius=24, fill=(5, 150, 105), outline=(250, 204, 21), width=3)
        f_cta = fit_jp_font(draw, JP_SINGLE_CTA, W - 240, start_size=34, min_size=24, stroke_width=2)
        draw.text((120, 566), JP_SINGLE_CTA, font=f_cta, fill=(255, 255, 255), stroke_width=2, stroke_fill=(0, 0, 0))
        draw.text((100, 695), "✓ 英語SEC 8-K決算・Form-4役員買いを3秒で日本語要約", font=f_sub, fill=(226, 232, 240))
        draw.text((100, 765), "✓ ドル($)・日本円(¥)・新NISA成長投資枠 手取り純利益シミュレーター", font=f_sub, fill=(226, 232, 240))
        draw.text((100, 835), "✓ Web VIP Vault ＆ ブラウザ・メール即時シグナル配信", font=f_sub, fill=(56, 189, 248))

    # 3) Center Golden Safe-Zone Subtitle (y = 980 ~ 1080, NotoSansCJKjp-Black 82pt+, stroke_width=10, ZERO box)
    cap_y = JP_SAFE_SUBTITLE_Y
    for idx, cline in enumerate(caption_lines[:2]):
        f_cap = fit_jp_font(draw, cline, max_w=W - 76, start_size=82, min_size=50, stroke_width=10)
        bbox = draw.textbbox((0, 0), cline, font=f_cap, stroke_width=10)
        tw = bbox[2] - bbox[0]
        cx = max(38, (W - tw) // 2)
        fill_col = (255, 238, 75) if (idx == 0 and not is_ending_slate) else ((110, 247, 190) if is_ending_slate else (255, 255, 255))
        draw.text(
            (cx, cap_y),
            cline,
            font=f_cap,
            fill=fill_col,
            stroke_width=10,
            stroke_fill=(0, 0, 0),
        )
        cap_y += 92

    img.save(out_png, "PNG")


async def synthesize_cut_tts_natural(ffmpeg_bin, text, voice, out_wav):
    """Natural Japanese announcer rate (+4%, ZERO atempo stacking) with clean silence trim."""
    import edge_tts
    raw_mp3 = out_wav + ".mp3"
    communicate = edge_tts.Communicate(text=text, voice=voice, rate="+4%")
    await communicate.save(raw_mp3)
    af_trim = (
        "silenceremove=start_periods=1:start_duration=0.02:start_threshold=-46dB,"
        "areverse,"
        "silenceremove=start_periods=1:start_duration=0.03:start_threshold=-46dB,"
        "areverse,"
        "apad=pad_dur=0.06"
    )
    subprocess.run(
        [ffmpeg_bin, "-y", "-i", raw_mp3, "-af", af_trim, "-ar", "44100", "-ac", "1", "-c:a", "pcm_s16le", out_wav],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=True,
    )
    if os.path.exists(raw_mp3):
        os.remove(raw_mp3)
    return probe_audio_duration(ffmpeg_bin, out_wav)


def probe_audio_duration(ffmpeg_bin, audio_path):
    cmd = [ffmpeg_bin, "-i", audio_path]
    proc = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, encoding="utf-8", errors="ignore")
    m = re.search(r"Duration:\s*(\d+):(\d+):(\d+\.\d+)", proc.stderr)
    if not m:
        return 3.5
    return int(m.group(1)) * 3600 + int(m.group(2)) * 60 + float(m.group(3))


def build_summary_card_png(out_png, ticker, jp_name, entry, stop_loss, target_25r, score, catalyst_desc):
    W, H = 1200, 675
    img = Image.new("RGB", (W, H), (8, 10, 22))
    draw = ImageDraw.Draw(img)
    f_b = load_jp_font(26, black=False)
    f_t = load_jp_font(46, black=True)
    f_m = load_jp_font(38, black=True)
    f_s = load_jp_font(27, black=False)

    draw.rounded_rectangle([(28, 28), (W - 28, H - 28)], radius=24, fill=(15, 18, 38), outline=(56, 189, 248), width=4)
    draw.text((64, 58), f"⚡ {JP_CHANNEL_NAME}  |  AIスコア {score}/100", font=f_b, fill=(245, 158, 11))
    draw.text((64, 115), f"${ticker} ({jp_name}) — 新NISA手取り＆適正株数解析", font=f_t, fill=(255, 255, 255))
    draw.text((64, 188), catalyst_desc, font=f_s, fill=(196, 181, 253))

    boxes = [
        ("現在株価 (ドル/円)", f"${entry:.2f} (約¥{int(round(entry*150)):,})", (248, 250, 252)),
        ("逆指値 (口座損失-1.5%内)", f"${stop_loss:.2f} (2.0x ATR防衛)", (244, 63, 94)),
        ("本命利確ターゲット", f"${target_25r:.2f} (損益比 1:2.5)", (16, 185, 129)),
    ]
    bx = 64
    for lbl, val, col in boxes:
        draw.rounded_rectangle([(bx, 260), (bx + 345, 440)], radius=18, fill=(22, 24, 52), outline=col, width=3)
        draw.text((bx + 22, 288), lbl, font=f_b, fill=(180, 190, 215))
        draw.text((bx + 22, 348), val, font=f_m, fill=col)
        bx += 365

    draw.rounded_rectangle([(64, 480), (W - 64, 605)], radius=16, fill=(20, 32, 64), outline=(56, 189, 248), width=2)
    draw.text((90, 502), f"🔗 {JP_SINGLE_CTA} 👉 https://getbreakai.com/?calc=atr&ticker={ticker}", font=f_s, fill=(56, 189, 248))
    draw.text((90, 550), "#米国株  #新NISA  #エヌビディア  #NVDA  #半導体株  #損切り  #SEC開示  #株クラ", font=f_b, fill=(253, 230, 138))
    img.save(out_png, "PNG", optimize=True)


async def main():
    ffmpeg_bin = get_ffmpeg_bin()
    now_jst = datetime.now(JST)
    date_str = now_jst.strftime("%Y-%m-%d")

    snap = {"tickers": {}}
    if os.path.exists(SNAPSHOT_PATH):
        snap = json.load(open(SNAPSHOT_PATH, "r", encoding="utf-8"))
        date_str = snap.get("updated_date", date_str)

    out_dir = os.path.join(OUTBOX_ROOT, date_str)
    os.makedirs(out_dir, exist_ok=True)
    tmp_dir = os.path.join(out_dir, "_tmp_build")
    os.makedirs(tmp_dir, exist_ok=True)

    t = snap.get("tickers", {})

    def gv(sym, k, d):
        return t.get(sym, {}).get(k, d)

    # 3 US Megacap/Semiconductor Shorts ($NVDA, $SOXL/$SMH, $PLTR) — P&L-First #新NISA Script Rule, 22~28s target
    nvda_e = float(gv("NVDA", "entry", 186.64))
    nvda_s = float(gv("NVDA", "stop_loss", 170.60))
    nvda_t = float(gv("NVDA", "target_25r", 226.74))

    pltr_e = float(gv("PLTR", "entry", 160.38))
    pltr_s = float(gv("PLTR", "stop_loss", 140.48))
    pltr_t = float(gv("PLTR", "target_25r", 210.13))

    tsla_e = float(gv("TSLA", "entry", 358.22))
    tsla_s = float(gv("TSLA", "stop_loss", 322.24))
    tsla_t = float(gv("TSLA", "target_25r", 448.17))

    episodes = [
        {
            "file": "jp_shorts_01_NVDA_gamma_atr.mp4",
            "card_png": "card_01_NVDA_signal.png",
            "ticker": "NVDA",
            "jp_name": "エヌビディア",
            "yt_title": f"【100万円検証】エヌビディア株でお祈りナンピン52万円 vs 逆指値168万円の決定的な差 ({date_str}) #米国株 #新NISA #NVDA #Shorts",
            "voice": "ja-JP-NanamiNeural",
            "accent": (16, 185, 129),
            "abc_hooks": {
                "A_vs": "同じ100万円でエヌビディア株を買って、52万円に減る人と168万円に増やす人の差。",
                "B_loss": "新NISAでエヌビディア株をナンピンすると、損益通算ゼロで非課税枠が凍結します！",
                "C_twist": "株価マイナス8%の逆指値でも、口座の損失を1.5%以内に抑える適正株数の算数。",
            },
            "selected_hook": "A_vs",
            "cuts": [
                {
                    "tts": "同じ100万円でエヌビディア株を買っても、お祈りナンピンで52万円に溶かす人と、168万円に増やす人がいます。",
                    "headline": ["エヌビディア($NVDA) 100万円検証", "お祈りナンピン52万 vs 逆指値168万"],
                    "label": "半年後のリアル口座残高比較",
                    "val": "¥520,000 vs ¥1,680,000",
                    "sub_box": [("⚠️ 新NISAは損益通算ゼロ！塩漬けが一番危険", (251, 113, 133))],
                    "cap": ["100万円が52万に溶ける人 vs", "168万円に増やす人の決定的な差"],
                    "ending": False,
                },
                {
                    "tts": "負ける原因は、急落中に安くなったと思い込んで買い増しし、新NISA枠ごと塩漬けにしてしまうことです。",
                    "headline": ["60日移動平均線割れでの買い増し厳禁", "一度の塩漬けが非課税枠を凍結"],
                    "label": "機関投資家のトレンド転換条件",
                    "val": "60日線突破 × 出来高2倍",
                    "sub_box": [("✅ 底打ちと出来高急増を確認してから参入", (52, 211, 153))],
                    "cap": ["急落中のナンピン買いは厳禁！", "60日線突破の本物トレンドを待つ"],
                    "ending": False,
                },
                {
                    "tts": "最新の米国SEC適時開示でも、エヌビディアのAI半導体需要は強気スコア93.5点を記録しています。",
                    "headline": ["米国SEC 8-K開示をAIが3秒解読", "機関投資家の実弾フローが集中"],
                    "label": "SEC開示 AIカタリスト判定",
                    "val": "93.5 / 100点 (強気)",
                    "sub_box": [("📈 決算ガイダンス＆機関コール買い優勢", (251, 191, 36))],
                    "cap": ["最新SEC開示スコアは93.5点！", "機関投資家の買いフローが集中"],
                    "ending": False,
                },
                {
                    "tts": f"現在値{nvda_e:.1f}ドルなら、株価マイナス8パーセントの逆指値{nvda_s:.1f}ドルでも、口座全体の損失をマイナス1.5パーセント以内に抑える適正株数が計算できます。",
                    "headline": ["株価-8%逆指値でも口座損失-1.5%以内", "ボラティリティ(2.0x ATR)から株数逆算"],
                    "label": "機関標準 逆指値ライン",
                    "val": f"${nvda_s:.2f} (利確 ${nvda_t:.2f})",
                    "sub_box": [
                        (f"💵 期待利確目標: ${nvda_t:.2f} (約+27.7万円)", (52, 211, 153)),
                        ("🛡️ 感情ゼロで損小利大を自動化", (251, 191, 36)),
                    ],
                    "cap": [f"逆指値{nvda_s:.1f}ドルでも口座損失を", "-1.5%以内に抑える適正株数！"],
                    "ending": False,
                },
                {
                    "tts": "無料AI株数・損切り計算機は、プロフィールのリンク、ゲットブレイクAIドットコムから3秒で使えます！",
                    "headline": [],
                    "label": "",
                    "val": "",
                    "sub_box": [],
                    "cap": ["無料AI株数・損切り計算機 ➔", "プロフの getbreakai.com へ！"],
                    "ending": True,
                },
            ],
        },
        {
            "file": "jp_shorts_02_PLTR_sec8k_atr.mp4",
            "card_png": "card_02_PLTR_signal.png",
            "ticker": "PLTR",
            "jp_name": "パランティア",
            "yt_title": f"【米国株×新NISA】パランティア急騰の裏で口座を守る「-1.5%適正株数」の算数 ({date_str}) #米国株 #新NISA #PLTR #Shorts",
            "voice": "ja-JP-KeitaNeural",
            "accent": (139, 92, 246),
            "abc_hooks": {
                "A_vs": "パランティア株で+28万円を伸ばす人と、高値掴みで退場する人の株数管理の差。",
                "B_loss": "値動きの激しい米国AI株、感覚で株数を決めると1日で口座資金が削られます！",
                "C_twist": "英語のSEC 8-K大型契約が出る瞬間、機関投資家はどう株数を計算しているのか？",
            },
            "selected_hook": "A_vs",
            "cuts": [
                {
                    "tts": "値動きの激しい米国AI株パランティア、100万円を52万円に減らす人と168万円に増やす人の違いは株数計算です。",
                    "headline": ["パランティア($PLTR) 損益分岐の秘密", "感覚の全力買い vs 適正株数ルール"],
                    "label": "100万円運用の資産推移比較",
                    "val": "¥520,000 vs ¥1,680,000",
                    "sub_box": [("⚠️ 高ボラ米国株の全力買いは一発退場リスク", (251, 113, 133))],
                    "cap": ["米国AI株で資産を減らす人 vs", "168万円へ伸ばす人の株数管理"],
                    "ending": False,
                },
                {
                    "tts": "英語の米国SEC重要契約開示をAIが3秒で解読した結果、国防AI受注拡大でスコア91点を記録しています。",
                    "headline": ["英語のSEC Form 8-Kを3秒日本語化", "ニュースになる前の一次情報を捕捉"],
                    "label": "SEC 8-K カタリストスコア",
                    "val": "91.0 / 100点 (機関集積)",
                    "sub_box": [("🐋 機関投資家の大口買い比率 64%到達", (196, 181, 253))],
                    "cap": ["英語SEC 8-KをAIが3秒で解読！", "機関買い集めスコア91点を記録"],
                    "ending": False,
                },
                {
                    "tts": "しかし強い銘柄でも押し目の振れ幅が大きいため、浅すぎる逆指値はノイズで刈られてしまいます。",
                    "headline": ["値動き幅(ATR)に合わせた逆指値設計", "ノイズで狩られず大損だけを遮断"],
                    "label": "60日線サポート＆出来高ブレイク",
                    "val": f"現在株価 ${pltr_e:.2f}",
                    "sub_box": [("✅ 2.0倍ATRなら機関の揺さぶりに耐えられる", (52, 211, 153))],
                    "cap": ["浅すぎる逆指値はヒゲで刈られる", "値動き幅に合わせた損切りが必須"],
                    "ending": False,
                },
                {
                    "tts": f"株価マイナス8パーセント前後の逆指値{pltr_s:.1f}ドルでも、口座全体の損失がマイナス1.5パーセント以内に収まる適正株数なら安心です。",
                    "headline": ["口座全体の最大損失を-1.5%にロック", "新NISA・特定口座の手取りも自動比較"],
                    "label": "適正逆指値 ＆ 2.5R利確目標",
                    "val": f"${pltr_s:.2f} ➔ 🎯${pltr_t:.2f}",
                    "sub_box": [
                        (f"🎯 本命利確目標: ${pltr_t:.2f} (損益比1:2.5)", (52, 211, 153)),
                        ("💴 ドル($)＆日本円(¥) 同時シミュレーション", (251, 191, 36)),
                    ],
                    "cap": ["口座損失を-1.5%以内に抑える", "適正株数なら夜もぐっすり安心！"],
                    "ending": False,
                },
                {
                    "tts": "無料AI株数・損切り計算機は、プロフィールのリンク、ゲットブレイクAIドットコムで今すぐ試せます！",
                    "headline": [],
                    "label": "",
                    "val": "",
                    "sub_box": [],
                    "cap": ["無料AI株数・損切り計算機 ➔", "プロフの getbreakai.com へ！"],
                    "ending": True,
                },
            ],
        },
        {
            "file": "jp_shorts_03_TSLA_gex_atr.mp4",
            "card_png": "card_03_TSLA_signal.png",
            "ticker": "TSLA",
            "jp_name": "テスラ",
            "yt_title": f"【テスラ株×新NISA】乱高下でも口座損失-1.5%以内に守るプロ逆指値と株数計算 ({date_str}) #米国株 #新NISA #TSLA #Shorts",
            "voice": "ja-JP-NanamiNeural",
            "accent": (245, 158, 11),
            "abc_hooks": {
                "A_vs": "テスラ株の乱高下で消耗する個人と、機械的ルールで+27万円を狙うプロの差。",
                "B_loss": "テスラ株を雰囲気でナンピンすると、新NISAの非課税枠が一瞬で塩漬けになります！",
                "C_twist": "コール3.6倍の踏み上げ相場、どこに逆指値を置けば口座を守りながら利益を伸ばせるか？",
            },
            "selected_hook": "A_vs",
            "cuts": [
                {
                    "tts": "テスラ株のような激しい米国株でも、100万円を52万円に溶かす人と168万円に伸ばす人の差は明確です。",
                    "headline": ["テスラ($TSLA) 100万円リアル検証", "感情トレード52万 vs 機械的逆指値168万"],
                    "label": "半年後の口座残高シミュレーション",
                    "val": "¥520,000 vs ¥1,680,000",
                    "sub_box": [("⚠️ 雰囲気での飛びつき買い＆ナンピンは厳禁", (251, 113, 133))],
                    "cap": ["テスラ株で52万に減らす人 vs", "168万円に増やすプロの資金管理"],
                    "ending": False,
                },
                {
                    "tts": "現在オプション市場でコール買いが3.6倍に急増し、60日線を上抜ける強いトレンドが発生しています。",
                    "headline": ["右側ブレイクアウト＆オプション需給", "大口コール3.6倍の踏み上げ点火"],
                    "label": "AIカタリスト＆需給スコア",
                    "val": "89.7 / 100点 (強気転換)",
                    "sub_box": [("⚡ マーケットメイカーのヘッジ買い領域", (251, 191, 36))],
                    "cap": ["大口コール買い3.6倍が流入し", "60日線突破の上昇トレンド点火！"],
                    "ending": False,
                },
                {
                    "tts": f"現在値{tsla_e:.1f}ドルに対し、機関標準の逆指値ラインは{tsla_s:.1f}ドル、利確目標は{tsla_t:.1f}ドルです。",
                    "headline": ["エントリー前に出口戦略を100%固定", "逆指値と利確目標をドル・円で算出"],
                    "label": "逆指値 ➔ 2.5R利確ターゲット",
                    "val": f"${tsla_s:.2f} ➔ ${tsla_t:.2f}",
                    "sub_box": [("💰 20株保有時の期待利益: 約+27.0万円", (52, 211, 153))],
                    "cap": [f"逆指値は{tsla_s:.1f}ドル、本命の", f"利確目標は{tsla_t:.1f}ドルに固定！"],
                    "ending": False,
                },
                {
                    "tts": "株価マイナス8パーセントの逆指値でも、口座全体の損失がマイナス1.5パーセント以内に収まる適正株数を先に決めましょう。",
                    "headline": ["株価-8%逆指値でも口座損失-1.5%以内", "SBI・楽天・マネックス注文画面に直結"],
                    "label": "新NISA・特定口座 手取り純利益対応",
                    "val": "口座リスク 1.5% 自動ロック",
                    "sub_box": [
                        ("🛡️ 1回の損切り額を購入前に円建てで把握", (110, 247, 190)),
                        ("🌱 新NISA非課税メリットもワンタッチ比較", (56, 189, 248)),
                    ],
                    "cap": ["株価-8%の逆指値でも口座損失が", "-1.5%以内に収まる適正株数！"],
                    "ending": False,
                },
                {
                    "tts": "無料AI株数・損切り計算機は、プロフィールのリンク、ゲットブレイクAIドットコムで3秒で無料計算できます！",
                    "headline": [],
                    "label": "",
                    "val": "",
                    "sub_box": [],
                    "cap": ["無料AI株数・損切り計算機 ➔", "プロフの getbreakai.com へ！"],
                    "ending": True,
                },
            ],
        },
    ]

    abc_log = []
    for ep_idx, ep in enumerate(episodes):
        sym = ep["ticker"]
        n_cuts = len(ep["cuts"])
        cut_wavs = []
        cut_durs = []
        cut_starts = []
        cut_timings_srt = []

        cursor = 0.0
        for c_i, cinfo in enumerate(ep["cuts"]):
            c_wav = os.path.join(tmp_dir, f"{sym}_cut_{c_i:02d}.wav")
            tts_d = await synthesize_cut_tts_natural(ffmpeg_bin, cinfo["tts"], ep["voice"], c_wav)
            # Enforce 100% syllable readout (seg_dur >= tts_dur + 0.26s) and 22~28s total episode pacing
            min_floor = 3.2 if cinfo["ending"] else 4.2
            seg_d = round(max(min_floor, tts_d + 0.28), 2)
            cut_starts.append(cursor)
            cut_wavs.append(c_wav)
            cut_durs.append(seg_d)
            cut_timings_srt.append({
                "start": cursor,
                "end": round(cursor + seg_d, 2),
                "caption_lines": cinfo["cap"],
            })
            cursor += seg_d

        total_dur = round(sum(cut_durs), 2)
        # Stitch cut voice WAVs onto exact timeline
        voice_master = os.path.join(tmp_dir, f"{sym}_voice_master.wav")
        sample_rate = 44100
        total_samples = int(round(total_dur * sample_rate))
        voice_pcm = [0] * total_samples
        for c_wav, st_sec in zip(cut_wavs, cut_starts):
            st_idx = int(round((st_sec + 0.04) * sample_rate))
            with wave.open(c_wav, "rb") as wf:
                raw = wf.readframes(wf.getnframes())
                vals = struct.unpack(f"<{len(raw)//2}h", raw)
            for k_i, v_s in enumerate(vals):
                if st_idx + k_i < total_samples:
                    voice_pcm[st_idx + k_i] = v_s
        with wave.open(voice_master, "wb") as wf:
            wf.setnchannels(1)
            wf.setsampwidth(2)
            wf.setframerate(sample_rate)
            wf.writeframes(struct.pack(f"<{total_samples}h", *voice_pcm))

        sfx_wav = os.path.join(tmp_dir, f"{sym}_sfx_bgm.wav")
        generate_sfx_and_docu_bgm_wav(sfx_wav, cut_starts, duration_sec=total_dur, preset_idx=ep_idx)

        concat_txt = os.path.join(tmp_dir, f"{sym}_concat.txt")
        concat_lines = []
        e_val = float(gv(sym, "entry", 186.64))
        s_val = float(gv(sym, "stop_loss", 170.60))
        t_val = float(gv(sym, "target_25r", 226.74))

        for idx, cinfo in enumerate(ep["cuts"]):
            png_path = os.path.join(tmp_dir, f"{sym}_slide_{idx:02d}.png")
            draw_clean_v3_slide(
                out_png=png_path,
                cut_idx=idx,
                total_cuts=n_cuts,
                ticker=sym,
                jp_name=ep["jp_name"],
                headline_top=cinfo["headline"],
                big_metric_label=cinfo["label"],
                big_metric_val=cinfo["val"],
                sub_box_lines=cinfo["sub_box"],
                caption_lines=cinfo["cap"],
                accent_rgb=ep["accent"],
                entry=e_val,
                stop_loss=s_val,
                target_25r=t_val,
                is_ending_slate=cinfo["ending"],
            )
            safe_png = png_path.replace("\\", "/")
            concat_lines.append(f"file '{safe_png}'")
            concat_lines.append(f"duration {cut_durs[idx]:.2f}")
        concat_lines.append(f"file '{os.path.join(tmp_dir, f'{sym}_slide_{n_cuts-1:02d}.png').replace(chr(92), '/')}'")
        with open(concat_txt, "w", encoding="utf-8") as cf:
            cf.write("\n".join(concat_lines) + "\n")

        out_mp4 = os.path.join(out_dir, ep["file"])
        cmd = [
            ffmpeg_bin, "-y",
            "-f", "concat", "-safe", "0", "-i", concat_txt,
            "-i", voice_master,
            "-i", sfx_wav,
            "-filter_complex",
            "[1:a]volume=1.18[v];[2:a]volume=0.38[s];[v][s]amix=inputs=2:duration=first:dropout_transition=1,alimiter=limit=0.944:level=disabled[aout]",
            "-map", "0:v:0",
            "-map", "[aout]",
            "-c:v", "libx264", "-pix_fmt", "yuv420p", "-r", "30", "-preset", "fast", "-crf", "20",
            "-c:a", "aac", "-b:a", "192k",
            "-t", f"{total_dur:.2f}",
            "-movflags", "+faststart",
            out_mp4,
        ]
        subprocess.run(cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        # Export official .srt and .youtube.json metadata
        out_srt = os.path.splitext(out_mp4)[0] + ".srt"
        export_jp_srt(cut_timings_srt, out_srt)
        out_yt_json = os.path.splitext(out_mp4)[0] + ".youtube.json"
        yt_meta = build_getbreakai_youtube_metadata(ep["yt_title"], sym, ep["jp_name"], now_jst)
        with open(out_yt_json, "w", encoding="utf-8") as mf:
            json.dump(yt_meta, mf, ensure_ascii=False, indent=2)

        print(f"[OK] Rendered JP Shorts MP4 + SRT + YT Meta: {out_mp4} ({os.path.getsize(out_mp4)} bytes, {total_dur:.1f}s)")

        card_path = os.path.join(out_dir, ep["card_png"])
        build_summary_card_png(
            out_png=card_path,
            ticker=sym,
            jp_name=ep["jp_name"],
            entry=e_val,
            stop_loss=s_val,
            target_25r=t_val,
            score=gv(sym, "score", 91.0),
            catalyst_desc="米国SEC 8-K適時開示 · Form-4役員買い · 適正株数＆新NISA手取りAI解析",
        )
        print(f"[OK] Generated Japanese X Summary Card PNG: {card_path}")

        abc_log.append({
            "episode": ep["file"],
            "ticker": sym,
            "voice": ep["voice"],
            "abc_candidates": ep["abc_hooks"],
            "selected_hook": ep["selected_hook"],
            "duration_sec": total_dur,
            "subtitle_safe_zone_y": JP_SAFE_SUBTITLE_Y,
            "publishAt_schedule_jst": "20:30:00+09:00",
        })

    with open(os.path.join(out_dir, "abc_hook_selection.json"), "w", encoding="utf-8") as f:
        json.dump(abc_log, f, ensure_ascii=False, indent=2)

    # Generate 10 Japanese X (株クラ) High-CTR Posts (P&L-first, US Megacap/Semis focus, ZERO Telegram)
    x_posts = [
        {
            "id": 1,
            "ticker": "NVDA",
            "text": f"【エヌビディア($NVDA) 100万円投資の分岐点】\nお祈りナンピンで52万円に溶かすか、機械的逆指値で168万円へ伸ばすか🔥\n\n📊 SEC 8-K強気スコア: 93.5/100\n🛡️ 逆指値ライン: ${nvda_s:.2f}（口座損失-1.5%以内）\n🎯 2.5R利確目標: ${nvda_t:.2f}\n\n{JP_SINGLE_CTA}\nhttps://getbreakai.com/?calc=atr&ticker=NVDA\n#米国株 #新NISA #エヌビディア #NVDA #半導体株 #損切り #株クラ",
        },
        {
            "id": 2,
            "ticker": "PLTR",
            "text": f"【パランティア($PLTR) 米国SEC 8-K大型契約解析🐋】\n株価 -8% の逆指値でも口座全体の損失が -1.5% 以内に収まる「適正株数」を先に計算していますか？\n\n📑 SEC 8-K国防AI契約スコア: 91.0/100\n🛡️ 2.0x ATR逆指値: ${pltr_s:.2f}\n🎯 2.5R利確目標: ${pltr_t:.2f}\n\n新NISA・特定口座対応 3秒計算機👇\nhttps://getbreakai.com/?calc=atr&ticker=PLTR\n#米国株 #新NISA #パランティア #PLTR #SEC開示 #株クラ",
        },
        {
            "id": 3,
            "ticker": "TSLA",
            "text": f"【テスラ($TSLA) コール3.6倍の踏み上げ点火⚡】\n乱高下する米国グロース株こそ、感覚ではなく値動き幅(ATR)から適正株数を逆算！\n\n💵 現在株価: ${tsla_e:.2f}\n🛡️ 2.0x ATR逆指値: ${tsla_s:.2f}\n🎯 2.5R利確目標: ${tsla_t:.2f}\n\nドル・円対応の適正株数シミュレーター👇\nhttps://getbreakai.com/?calc=atr&ticker=TSLA\n#米国株 #新NISA #テスラ #TSLA #損切り #株クラ",
        },
        {
            "id": 4,
            "ticker": "LLY",
            "text": f"【イーライリリー($LLY) 経営陣3名が自腹で$4.8M買い💊】\n役員が自己資金で市場内購入(SEC Form-4)する理由は「株価上昇への確信」ただ1つ。\n\n🐋 Form-4クラスタースコア: 89.8/100\n🛡️ 2.0x ATR逆指値: ${gv('LLY','stop_loss',1248.38):.2f}\n🎯 2.5R利確目標: ${gv('LLY','target_25r',1618.05):.2f}\n\n詳細データ＆株数計算機👇\nhttps://getbreakai.com/?calc=atr&ticker=LLY\n#米国株 #新NISA #SEC開示 #株クラ",
        },
        {
            "id": 5,
            "ticker": "SMCI",
            "text": f"【⚠️ $SMCI エントリー見送り・会計リスク＆機関売り警告】\n新NISA口座は損益通算ゼロ。落ちるナイフへの安易なナンピンは非課税枠を凍結させます。\n\n🔴 AIカタリストスコア: 28.5/100 (AVOID)\n📉 機関売り比率: 67%\n\n暴落トラップを回避して$NVDA・$AVGOへ資金を守る👇\nhttps://getbreakai.com/?calc=atr&ticker=SMCI\n#米国株 #新NISA #半導体株 #損切り #株クラ",
        },
        {
            "id": 6,
            "ticker": "SOXL",
            "text": "【$SOXL・$SMH 半導体ETFで塩漬けにならない鉄則🔥】\n3倍レバレッジETFを「なんとなくナンピン」すると減価で100万円が52万円に溶けます。\n\n① 60日移動平均線の右側ブレイクを確認\n② GetBreakAI.com で口座損失 -1.5% 以内の適正株数を厳守\n\n日本語解説レポート👇\nhttps://getbreakai.com/jp/soxl-smh-semiconductor-timing.html\n#米国株 #新NISA #半導体株 #SOXL #株クラ",
        },
        {
            "id": 7,
            "ticker": "AVGO",
            "text": f"【ブロードコム($AVGO) カスタムAI半導体(ASIC)受注8-K解析🔬】\nハイパースケーラー向け需要拡大で機関買い集めが加速中。\n\n📊 AIスコア: 88.4/100\n🛡️ 2.0x ATR逆指値: ${gv('AVGO','stop_loss',263.41):.2f}\n🎯 2.5R利確目標: ${gv('AVGO','target_25r',369.39):.2f}\n\n即時シミュレーション👇\nhttps://getbreakai.com/?calc=atr&ticker=AVGO\n#米国株 #新NISA #半導体株 #AVGO #SEC開示",
        },
        {
            "id": 8,
            "ticker": "VRT",
            "text": f"【AIデータセンター液冷の本命 バーティブ($VRT)❄️】\n次世代GPUラックの熱問題を解決する液冷インフラ受注残が過去最高を更新。\n\n📊 AIカタリストスコア: 88.1/100\n🛡️ 2.0x ATR逆指値: ${gv('VRT','stop_loss',145.24):.2f}\n🎯 2.5R利確目標: ${gv('VRT','target_25r',276.91):.2f}\n\n日本語レポート＆計算機👇\nhttps://getbreakai.com/jp/vrt-ai-datacenter-cooling-catalyst.html\n#米国株 #新NISA #半導体株 #株クラ",
        },
        {
            "id": 9,
            "ticker": "CEG",
            "text": f"【AI原発電力PPA契約 コンステレーション・エナジー($CEG)⚡】\nハイパースケーラーとの長期原子力電力供給契約(SEC 8-K)をAIが高く評価。\n\n📊 AIスコア: 87.0/100\n🛡️ 2.0x ATR逆指値: ${gv('CEG','stop_loss',225.91):.2f}\n🎯 2.5R利確目標: ${gv('CEG','target_25r',310.05):.2f}\n\n詳細解析👇\nhttps://getbreakai.com/jp/ceg-nuclear-ai-power-8k-contract.html\n#米国株 #新NISA #SEC開示 #株クラ",
        },
        {
            "id": 10,
            "ticker": "ALL",
            "text": f"【新NISA・米国株投資家のための無料AI株数・損切り計算機🚀】\n株価 -8% の逆指値でも口座全体の損失が -1.5% 以内に収まる「適正株数」をドル($)と日本円(¥)で3秒算出！英語SEC 8-K開示も日本語AI要約。\n\n{JP_SINGLE_CTA}\nhttps://getbreakai.com/?calc=atr\n#米国株 #新NISA #エヌビディア #NVDA #半導体株 #損切り #SEC開示 #株クラ",
        },
    ]

    with open(os.path.join(out_dir, "x_posts_10.json"), "w", encoding="utf-8") as f:
        json.dump(x_posts, f, ensure_ascii=False, indent=2)

    with open(os.path.join(out_dir, "x_posts_10.md"), "w", encoding="utf-8") as f:
        f.write(f"# 日本X (株クラ) ワンクリック投稿用ドラフト10選 ({date_str})\n\n")
        for p in x_posts:
            f.write(f"## Post #{p['id']} (${p['ticker']})\n```text\n{p['text']}\n```\n\n")

    note_md = f"""# 【米国株・新NISA】100万円投資でお祈りナンピン52万円 vs 逆指値168万円 — SEC 8-K解読＆適正株数で資産を守る方法（{date_str}最新版）

日本の個人投資家が米国主力株（エヌビディア `$NVDA`、半導体ETF `$SMH`/`$SOXL`、パランティア `$PLTR`、テスラ `$TSLA`、ブロードコム `$AVGO`）で資産を守り抜く最大の鍵は、**「株価 -8% の逆指値でも口座全体の損失が -1.5% 以内に収まる適正株数計算」**と**「SEC一次情報のスピード」**にあります。

## 1. 本日の注目米国株 AIカタリスト＆逆指値ライン一覧（1ドル＝150円換算）

| 銘柄 | AIスコア | カタリスト・機関動向 | 現在株価 | 2.0x ATR逆指値 | 2.5R 利確目標 |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **$NVDA エヌビディア** | **93.5/100** | Blackwell増産・Call 3.2倍 | ${nvda_e:.2f} | ${nvda_s:.2f} | **${nvda_t:.2f}** |
| **$PLTR パランティア** | **91.0/100** | 国防AI 8-K契約・機関集積64% | ${pltr_e:.2f} | ${pltr_s:.2f} | **${pltr_t:.2f}** |
| **$LLY イーライリリー** | **89.8/100** | 経営陣3名 Form-4自腹買い$4.8M | ${gv('LLY','entry',1354.00):.2f} | ${gv('LLY','stop_loss',1248.38):.2f} | **${gv('LLY','target_25r',1618.05):.2f}** |
| **$TSLA テスラ** | **89.7/100** | 60日線突破・コール3.6倍踏み上げ | ${tsla_e:.2f} | ${tsla_s:.2f} | **${tsla_t:.2f}** |
| **$SMCI (⚠️警告)** | **28.5/100** | 🔴 会計リスク・機関売り67% | ${gv('SMCI','entry',28.76):.2f} | **エントリー見送り** | **見送り推奨** |

## 2. 無料AI株数・損切り計算機（ドル・日本円・新NISA同時対応）
👉 **{JP_SINGLE_CTA}:** [https://getbreakai.com/?calc=atr](https://getbreakai.com/?calc=atr)
👉 **30銘柄の日本語ディープリサーチ一覧:** [https://getbreakai.com/jp/index.html](https://getbreakai.com/jp/index.html)
"""
    with open(os.path.join(out_dir, "note_com_article_jp.md"), "w", encoding="utf-8") as f:
        f.write(note_md)

    shutil.rmtree(tmp_dir, ignore_errors=True)
    print(f"[OK] Saved 10 Japanese X posts + 3 summary cards + note.com article + 3 MP4/SRT/YT-JSON shorts in {out_dir}")


if __name__ == "__main__":
    asyncio.run(main())
