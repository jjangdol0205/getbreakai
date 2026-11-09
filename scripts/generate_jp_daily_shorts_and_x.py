#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
scripts/generate_jp_daily_shorts_and_x.py
4사업부 (GetBreakAI — getbreakai.com)
일본 株クラ(X)·유튜브 쇼츠 무인 공략용:
1) edge-tts 일본어 아나운서 음성(ja-JP-KeitaNeural, ja-JP-NanamiNeural, +18% 고속 호흡)
2) V3 클린 풀스크린(1080x1920, 상·하단 박스 0%, 2초 고속 컷 전환, 하단 세이프존 Y=1395 두꺼운 외곽선 stroke_width=10 자막, 마지막 2.8초 엔딩 슬레이트 도메인 콜아웃, SFX 및 -0.5dBFS 리미터)
3) 15초 분량 일본어 쇼츠 .mp4 3편($NVDA, $PLTR, $TSLA) + 일본 X(株クラ) 트윗 원고 10종 + 요약 카드 이미지(.png) 3종 + note.com 일본어 칼럼 초안 자동 생성
"""

import os
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
OUTBOX_ROOT = os.path.join(ROOT_DIR, "marketing_outbox_jp")

JST = timezone(timedelta(hours=9))


def get_ffmpeg_bin():
    exe = shutil.which("ffmpeg")
    if exe:
        return exe
    try:
        import imageio_ffmpeg
        return imageio_ffmpeg.get_ffmpeg_exe()
    except Exception:
        raise RuntimeError("ffmpeg executable not found")


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


def generate_sfx_wav(wav_path, duration_sec=15.0, sample_rate=44100):
    """Generates subtle institutional quant SFX bed (0s hook impact, 2.2s cut pings, ending sub-drop)."""
    n_samples = int(duration_sec * sample_rate)
    cut_times = [0.0, 2.2, 4.4, 6.6, 9.0, 11.8]
    with wave.open(wav_path, "w") as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(sample_rate)
        frames = bytearray()
        for i in range(n_samples):
            t = i / sample_rate
            val = 0.0
            for idx, ct in enumerate(cut_times):
                dt = t - ct
                if 0.0 <= dt < 0.35:
                    env = math.exp(-dt * 12.0)
                    freq = 95.0 if idx in (0, 5) else (520.0 + idx * 60.0)
                    val += 0.22 * env * math.sin(2.0 * math.pi * freq * dt)
            sample = max(-32000, min(32000, int(val * 32767)))
            frames += struct.pack("<h", sample)
        wf.writeframes(frames)


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
    is_ending_slate=False,
):
    """
    V3 Clean Shorts Standard (1080x1920):
    - 100% fullscreen rich dark canvas (no top/bottom white/black letterbox bars, no persistent banner in body).
    - Bottom safe-zone (Y=1390~1485) caption with stroke_width=10 black outline and zero translucent box.
    - Domain callout (getbreakai.com) ONLY on final ending slate cut!
    """
    W, H = 1080, 1920
    img = Image.new("RGB", (W, H), (9, 7, 20))
    draw = ImageDraw.Draw(img)

    # Dynamic background chart grid + radial glow simulation
    grid_col = (24, 19, 46)
    for x in range(0, W, 90):
        draw.line([(x, 0), (x, H)], fill=grid_col, width=1)
    for y in range(0, H, 90):
        draw.line([(0, y), (W, y)], fill=grid_col, width=1)

    # Decorative institutional candlestick / gamma curve lines in background
    pts = []
    for step in range(12):
        px = 60 + step * 88
        py = 980 - int(math.sin(step * 0.65 + cut_idx) * 140) - step * 28
        pts.append((px, py))
    if len(pts) > 1:
        draw.line(pts, fill=accent_rgb, width=6)

    f_tag = load_jp_font(36)
    f_head = load_jp_font(54)
    f_lbl = load_jp_font(38)
    f_big = load_jp_font(84)
    f_sub = load_jp_font(40)
    f_cap = load_jp_font(52)

    if not is_ending_slate:
        # Body Cut: 100% Clean Fullscreen Quant Visual Card (NO domain watermark, NO top/bottom letterbox)
        draw.rounded_rectangle([(64, 190), (490, 268)], radius=38, fill=(28, 20, 58), outline=accent_rgb, width=3)
        draw.text((92, 208), f"⚡ 米国株AI速報 · ${ticker}", font=f_tag, fill=accent_rgb)

        # Headline
        y_cursor = 320
        for line in headline_top:
            draw.text(
                (68, y_cursor),
                line,
                font=f_head,
                fill=(248, 250, 252),
                stroke_width=6,
                stroke_fill=(0, 0, 0),
            )
            y_cursor += 76

        # Center Main Quant Metric Card
        draw.rounded_rectangle([(64, 540), (W - 64, 860)], radius=32, fill=(18, 14, 38), outline=accent_rgb, width=4)
        draw.text((104, 585), big_metric_label, font=f_lbl, fill=(180, 173, 208))
        draw.text(
            (104, 655),
            big_metric_val,
            font=f_big,
            fill=accent_rgb,
            stroke_width=4,
            stroke_fill=(0, 0, 0),
        )

        # Secondary Institutional Flow & ATR Box
        draw.rounded_rectangle([(64, 910), (W - 64, 1260)], radius=28, fill=(14, 11, 30), outline=(76, 55, 133), width=3)
        sy = 955
        for sline, scol in sub_box_lines:
            draw.text((100, sy), sline, font=f_sub, fill=scol)
            sy += 88
    else:
        # Final 2.8s Ending Slate Cut: Domain Callout Allowed Here Per V3 Rule #4!
        draw.rounded_rectangle([(64, 280), (W - 64, 1240)], radius=40, fill=(18, 13, 40), outline=(139, 92, 246), width=5)
        draw.text((110, 350), "🇺🇸 米国株・新NISA 専用AI端末", font=f_lbl, fill=(245, 158, 11))
        draw.text(
            (110, 430),
            "GetBreakAI.com",
            font=f_big,
            fill=(255, 255, 255),
            stroke_width=6,
            stroke_fill=(0, 0, 0),
        )
        draw.text((110, 560), f"▶ ${ticker} ({jp_name}) の適正株数・損切りを3秒計算", font=f_sub, fill=(52, 211, 153))
        draw.rounded_rectangle([(110, 670), (W - 110, 810)], radius=24, fill=(139, 92, 246), outline=(255, 255, 255), width=3)
        draw.text((165, 712), f"🔗 getbreakai.com/?ticker={ticker}", font=f_head, fill=(255, 255, 255))
        draw.text((110, 880), "✓ SEC 8-K決算・Form-4役員買い日本語解読", font=f_sub, fill=(226, 232, 240))
        draw.text((110, 965), "✓ ドル($)＆日本円(¥) 同時対応 ATR損切り計算機", font=f_sub, fill=(226, 232, 240))
        draw.text((110, 1050), "✓ 姉妹端末 TruthOfMarket.com 共通VIP対応", font=f_sub, fill=(56, 189, 248))

    # V3 Safe-Zone Caption (Y=1390~1485, thick black stroke_width=10, zero background box)
    cap_y = 1390
    for cline in caption_lines:
        bbox = draw.textbbox((0, 0), cline, font=f_cap, stroke_width=10)
        tw = bbox[2] - bbox[0]
        cx = max(48, (W - tw) // 2)
        draw.text(
            (cx, cap_y),
            cline,
            font=f_cap,
            fill=(255, 240, 100) if not is_ending_slate else (110, 231, 183),
            stroke_width=10,
            stroke_fill=(0, 0, 0),
        )
        cap_y += 74

    img.save(out_png, "PNG")


async def synthesize_tts(text, voice, out_mp3):
    import edge_tts
    communicate = edge_tts.Communicate(text=text, voice=voice, rate="+18%")
    await communicate.save(out_mp3)


def probe_audio_duration(ffmpeg_bin, audio_path):
    cmd = [ffmpeg_bin, "-i", audio_path]
    proc = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, encoding="utf-8", errors="ignore")
    import re
    m = re.search(r"Duration:\s*(\d+):(\d+):(\d+\.\d+)", proc.stderr)
    if not m:
        return 14.5
    return int(m.group(1)) * 3600 + int(m.group(2)) * 60 + float(m.group(3))


def build_summary_card_png(out_png, ticker, jp_name, entry, stop_loss, target_25r, score, catalyst_desc):
    W, H = 1200, 675
    img = Image.new("RGB", (W, H), (8, 6, 18))
    draw = ImageDraw.Draw(img)
    f_b = load_jp_font(26)
    f_t = load_jp_font(48)
    f_m = load_jp_font(38)
    f_s = load_jp_font(28)

    draw.rounded_rectangle([(28, 28), (W - 28, H - 28)], radius=24, fill=(15, 11, 30), outline=(139, 92, 246), width=4)
    draw.text((64, 58), f"⚡ GetBreakAI 米国株・新NISA シグナル速報  |  AIスコア {score}/100", font=f_b, fill=(245, 158, 11))
    draw.text((64, 115), f"${ticker} ({jp_name}) — 機関投資家フロー＆ATR損切り解析", font=f_t, fill=(255, 255, 255))
    draw.text((64, 188), catalyst_desc, font=f_s, fill=(196, 181, 253))

    boxes = [
        ("現在株価 (ドル/円)", f"${entry:.2f} (約¥{int(round(entry*150)):,})", (248, 250, 252)),
        ("2.0x ATR損切りライン", f"${stop_loss:.2f} (口座リスク1.5%)", (244, 63, 94)),
        ("2.5R 利確ターゲット", f"${target_25r:.2f} (リスクリワード1:2.5)", (16, 185, 129)),
    ]
    bx = 64
    for lbl, val, col in boxes:
        draw.rounded_rectangle([(bx, 260), (bx + 345, 440)], radius=18, fill=(22, 17, 44), outline=col, width=3)
        draw.text((bx + 22, 288), lbl, font=f_b, fill=(180, 173, 208))
        draw.text((bx + 22, 348), val, font=f_m, fill=col)
        bx += 365

    draw.rounded_rectangle([(64, 480), (W - 64, 605)], radius=16, fill=(28, 22, 56), outline=(56, 189, 248), width=2)
    draw.text((90, 502), f"🔗 あなたの口座資金(円・ドル)に最適な購入株数を3秒計算 👉 https://getbreakai.com/?ticker={ticker}", font=f_s, fill=(56, 189, 248))
    draw.text((90, 550), "#米国株  #新NISA  #株クラ  #ATR損切り  #ガンマスクイーズ  |  Sister: TruthOfMarket.com", font=f_b, fill=(253, 230, 138))
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

    # 3 Shorts Video Specs ($NVDA, $PLTR, $TSLA) with A/B/C hook selection
    episodes = [
        {
            "file": "jp_shorts_01_NVDA_gamma_atr.mp4",
            "card_png": "card_01_NVDA_signal.png",
            "ticker": "NVDA",
            "jp_name": "エヌビディア",
            "voice": "ja-JP-KeitaNeural",
            "accent": (16, 185, 129),
            "abc_hooks": {
                "A_vs": "移動平均線を見ている人と、オプションGamma Wallを見ている人の決定的な差。",
                "B_loss": "エヌビディア株、感覚でマイナス5%損切りを置くと機関のヒゲで一発退場します！",
                "C_twist": "ウォール街の英語SEC開示とコール3.2倍のガンマスクイーズ、AIが3秒で解読した結果。"
            },
            "selected_hook": "B_loss",
            "tts_script": (
                "エヌビディア株、感覚で5パーセント損切りを置くと機関のノイズで狩られます！"
                "最新SEC開示のAI強気スコアは93.5点、コール3.2倍のガンマスクイーズが発動中。"
                f"現在値{gv('NVDA','entry',186.64):.1f}ドルに対し、2倍ATR損切りラインは{gv('NVDA','stop_loss',170.60):.1f}ドル、"
                f"利確目標は{gv('NVDA','target_25r',226.74):.1f}ドルです。"
                "新NISAの適正株数はゲットブレイクAIドットコムで今すぐ無料計算！"
            ),
            "slides": [
                (["エヌビディア($NVDA)", "感覚の損切りは一発退場！？"], "14日ATRボラティリティ", f"${gv('NVDA','atr',8.02):.2f} / 日", [("⚠️ 浅すぎる逆指値は機関のヒゲで刈られる", (251, 113, 133)), ("✅ 機関標準「2.0x ATR損切り」が必須", (52, 211, 153))], ["エヌビディア株、感覚の損切りは", "機関のノイズで狩られます！"], False),
                (["SEC 8-K ＆ 決算コールNLP", "ウォール街の一次情報を3秒解読"], "AIカタリスト総合スコア", "93.5 / 100点", [("📈 決算ガイダンス強気トーン 94%", (52, 211, 153)), ("🐋 経営陣3名が市場内で自社株買い", (251, 191, 36))], ["最新SEC開示のAIスコアは93.5点！", "機関投資家の実弾買いが集中"], False),
                (["オプション市場 Gamma Squeeze", "ディーラー強制買いトリガー発動"], "Call / Put スイープ比率", "3.2倍 (強気)", [(f"⚡ GEX転換ライン: ${gv('NVDA','gamma_flip',179.82):.2f}", (196, 181, 253)), (f"🎯 5日間IV上限壁: ${gv('NVDA','upper_gamma_wall',204.52):.2f}", (56, 189, 248))], ["コール3.2倍のガンマスクイーズ発動", "マーケットメイカーの強制買い局面"], False),
                (["機関投資家式 ATR損切りライン", "口座リスクを1.5%以内に完全固定"], "2.0x ATR 逆指値ライン", f"${gv('NVDA','stop_loss',170.60):.2f}", [(f"💵 現在株価: ${gv('NVDA','entry',186.64):.2f}", (248, 250, 252)), ("🛡️ 750万円口座なら46株が適正サイズ", (251, 191, 36))], [f"現在値{gv('NVDA','entry',186.64):.1f}ドルに対し", f"2倍ATR損切りは{gv('NVDA','stop_loss',170.60):.1f}ドル！"], False),
                (["リスクリワード比 1 : 2.5", "感情を排して機械的に利益確定"], "2.5R 本命利確ターゲット", f"${gv('NVDA','target_25r',226.74):.2f}", [(f"🚀 5日Gamma Wall: ${gv('NVDA','upper_gamma_wall',204.52):.2f}", (196, 181, 253)), ("💰 期待利益: +$1,845 (約27.7万円)", (52, 211, 153))], [f"本命2.5R利確目標は{gv('NVDA','target_25r',226.74):.1f}ドル！", "リスクリワード1対2.5の黄金比"], False),
                ([], "", "", [], ["ドル・円対応の適正株数計算機は", "GetBreakAI.com で今すぐ無料起動！"], True),
            ],
        },
        {
            "file": "jp_shorts_02_PLTR_sec8k_atr.mp4",
            "card_png": "card_02_PLTR_signal.png",
            "ticker": "PLTR",
            "jp_name": "パランティア",
            "voice": "ja-JP-NanamiNeural",
            "accent": (139, 92, 246),
            "abc_hooks": {
                "A_vs": "英語のSEC 8-Kを3秒で読むAIと、翌日のニュースを待つ個人投資家の差。",
                "B_loss": "パランティア株、高値掴みと塩漬けを防ぐ機関投資家のATRルールを知っていますか？",
                "C_twist": "パランティアの取引所外ダークプール比率64%！機関がこっそり買い集める理由。"
            },
            "selected_hook": "C_twist",
            "tts_script": (
                "パランティア株、取引所外ダークプールで機関投資家の買いが64パーセントに急増中！"
                "英語のSEC 8-K国防AI契約をAIが3秒で解読し、総合スコアは91点を記録。"
                f"現在値{gv('PLTR','entry',160.38):.1f}ドルに対し、2倍ATR損切りラインは{gv('PLTR','stop_loss',140.48):.1f}ドル、"
                f"2.5R利確目標は{gv('PLTR','target_25r',210.13):.1f}ドルです。"
                "ドルと円の適正株数はゲットブレイクAIドットコムで今すぐチェック！"
            ),
            "slides": [
                (["パランティア($PLTR)", "ダークプール比率64%の衝撃！"], "取引所外ダークプール比率", "64.2% (機関集積)", [("🐋 板に見せない機関のブロック買い急増", (196, 181, 253)), ("📑 SEC Form 8-K 国防AI契約拡大", (52, 211, 153))], ["パランティア株、ダークプールで", "機関買いが64%に急増中！"], False),
                (["英語のSEC 8-Kを3秒で日本語解読", "ニュースが出る前に一次情報を捕捉"], "AIカタリスト総合スコア", "91.0 / 100点", [("📈 政府・民間AIP大型契約モメンタム", (52, 211, 153)), ("🏛️ 機関13F保有比率 +14.8%増加", (251, 191, 36))], ["英語のSEC 8-KをAIが3秒解読", "カタリストスコア91点を記録！"], False),
                (["決算後ドリフト (PEAD) 局面", "コールオプションスイープ2.8倍"], "5日間IV予想上値壁", f"${gv('PLTR','upper_gamma_wall',177.10):.2f}", [(f"⚡ GEX転換サポート: ${gv('PLTR','gamma_flip',151.92):.2f}", (56, 189, 248)), ("📊 IV 74% 強気コールスキュー", (196, 181, 253))], ["決算後の継続上昇ドリフト突入", "上値ガンマウォールへ加速中"], False),
                (["高ボラ株こそATR損切りが命綱", "口座の1.5%リスクで安全スイング"], "2.0x ATR 損切りライン", f"${gv('PLTR','stop_loss',140.48):.2f}", [(f"💵 現在株価: ${gv('PLTR','entry',160.38):.2f}", (248, 250, 252)), ("🛡️ 14日ATR: $" + f"{gv('PLTR','atr',9.95):.2f}", (251, 113, 133))], [f"現在値{gv('PLTR','entry',160.38):.1f}ドルに対し", f"2倍ATR損切りは{gv('PLTR','stop_loss',140.48):.1f}ドル！"], False),
                (["2.5R 利確ターゲット算出", "塩漬けゼロのクオンツ資金管理"], "2.5R 本命利確ターゲット", f"${gv('PLTR','target_25r',210.13):.2f}", [("🎯 第一目標: $" + f"{gv('PLTR','upper_gamma_wall',177.10):.2f} (Gamma壁)", (196, 181, 253)), ("💰 リスクリワード比 1 : 2.5", (52, 211, 153))], [f"2.5R利確目標は{gv('PLTR','target_25r',210.13):.1f}ドル！", "機械的ルールで利益を伸ばす"], False),
                ([], "", "", [], ["パランティアの適正株数計算機は", "GetBreakAI.com で今すぐ無料起動！"], True),
            ],
        },
        {
            "file": "jp_shorts_03_TSLA_gex_atr.mp4",
            "card_png": "card_03_TSLA_signal.png",
            "ticker": "TSLA",
            "jp_name": "テスラ",
            "voice": "ja-JP-KeitaNeural",
            "accent": (245, 158, 11),
            "abc_hooks": {
                "A_vs": "テスラ株を雰囲気で買う人と、Gamma WallとATRで計算して買う人の差。",
                "B_loss": "テスラ株の激しい値動き、株数を間違えると1日で口座が吹き飛びます！",
                "C_twist": "テスラにコール3.6倍の異常スイープ流入！ディーラー強制買いラインを公開。"
            },
            "selected_hook": "C_twist",
            "tts_script": (
                "テスラ株にコール3.6倍の異常オプションスイープが流入し、ガンマスクイーズが点火！"
                "FSD触媒と重なり、AIカタリストスコアは89.7点を記録しています。"
                f"現在値{gv('TSLA','entry',358.22):.1f}ドルに対し、2倍ATR損切りラインは{gv('TSLA','stop_loss',322.24):.1f}ドル、"
                f"利確目標は{gv('TSLA','target_25r',448.17):.1f}ドルです。"
                "あなたの資金に合う適正株数はゲットブレイクAIドットコムで3秒計算！"
            ),
            "slides": [
                (["テスラ($TSLA) 異常オプション検知", "コール3.6倍でガンマスクイーズ点火"], "Call / Put スイープ倍率", "3.6倍 (Ask強気買い)", [("⚡ 大口コールスイープ $84M流入", (251, 191, 36)), ("🐋 ダークプール比率 58.1%", (196, 181, 253))], ["テスラ株にコール3.6倍の流入！", "ガンマスクイーズが点火中"], False),
                (["FSD・ロボタクシー触媒NLP解析", "ディーラー正ガンマ領域へ転換"], "AIカタリスト総合スコア", "89.7 / 100点", [(f"📈 GEX転換ストライク: ${gv('TSLA','gamma_flip',342.93):.2f}", (52, 211, 153)), ("📊 オプションIV: 82% (高ボラ局面)", (56, 189, 248))], ["AIカタリストスコアは89.7点！", "ディーラー強制ヘッジ買い領域"], False),
                (["5日間オプションIV予想変動幅", "短期スイングの第一利確壁を特定"], "5日間IV Upper Gamma Wall", f"${gv('TSLA','upper_gamma_wall',399.59):.2f}", [(f"⚡ 5日予想変動幅: ±${gv('TSLA','exp_move_5d',41.37):.2f}", (251, 191, 36)), ("🎯 壁手前での分割利確が有効", (52, 211, 153))], ["5日間IV上値壁は399.6ドル！", "オプション需給から天井を逆算"], False),
                (["14日ATR $" + f"{gv('TSLA','atr',17.99):.2f}" + " の高ボラティリティ", "株数調整でリスクを1.5%に固定"], "2.0x ATR 損切りライン", f"${gv('TSLA','stop_loss',322.24):.2f}", [(f"💵 現在株価: ${gv('TSLA','entry',358.22):.2f}", (248, 250, 252)), ("🛡️ 750万円口座なら20株が適正サイズ", (251, 113, 133))], [f"現在値{gv('TSLA','entry',358.22):.1f}ドルに対し", f"2倍ATR損切りは{gv('TSLA','stop_loss',322.24):.1f}ドル！"], False),
                (["リスクリワード 1 : 2.5 ターゲット", "損小利大を自動化するATR計算機"], "2.5R 本命利確ターゲット", f"${gv('TSLA','target_25r',448.17):.2f}", [("💰 20株保有時の期待利益: +$1,799", (52, 211, 153)), ("💴 日本円換算: 約+27.0万円", (251, 191, 36))], [f"2.5R利確目標は{gv('TSLA','target_25r',448.17):.1f}ドル！", "ドル・円対応で損小利大を実現"], False),
                ([], "", "", [], ["テスラ株の適正株数＆損切り計算は", "GetBreakAI.com で今すぐ無料起動！"], True),
            ],
        },
    ]

    abc_log = []
    for ep in episodes:
        sym = ep["ticker"]
        mp3_path = os.path.join(tmp_dir, f"{sym}_voice.mp3")
        await synthesize_tts(ep["tts_script"], ep["voice"], mp3_path)
        voice_dur = probe_audio_duration(ffmpeg_bin, mp3_path)
        total_dur = max(13.5, min(16.5, voice_dur + 0.4))

        sfx_wav = os.path.join(tmp_dir, f"{sym}_sfx.wav")
        generate_sfx_wav(sfx_wav, duration_sec=total_dur)

        # Render 6 slides & build concat file (first 5 slides ~2.1s each, final ending slate ~2.8s)
        n_slides = len(ep["slides"])
        ending_dur = 2.8
        body_dur = round((total_dur - ending_dur) / (n_slides - 1), 2)

        concat_txt = os.path.join(tmp_dir, f"{sym}_concat.txt")
        concat_lines = []
        for idx, sdata in enumerate(ep["slides"]):
            png_path = os.path.join(tmp_dir, f"{sym}_slide_{idx:02d}.png")
            draw_clean_v3_slide(
                out_png=png_path,
                cut_idx=idx,
                total_cuts=n_slides,
                ticker=sym,
                jp_name=ep["jp_name"],
                headline_top=sdata[0],
                big_metric_label=sdata[1],
                big_metric_val=sdata[2],
                sub_box_lines=sdata[3],
                caption_lines=sdata[4],
                accent_rgb=ep["accent"],
                is_ending_slate=sdata[5],
            )
            dur = ending_dur if idx == n_slides - 1 else body_dur
            safe_png = png_path.replace("\\", "/")
            concat_lines.append(f"file '{safe_png}'")
            concat_lines.append(f"duration {dur:.2f}")
        # Repeat last frame for ffmpeg concat demuxer
        concat_lines.append(f"file '{os.path.join(tmp_dir, f'{sym}_slide_{n_slides-1:02d}.png').replace(chr(92), '/')}'")
        with open(concat_txt, "w", encoding="utf-8") as cf:
            cf.write("\n".join(concat_lines) + "\n")

        out_mp4 = os.path.join(out_dir, ep["file"])
        cmd = [
            ffmpeg_bin, "-y",
            "-f", "concat", "-safe", "0", "-i", concat_txt,
            "-i", mp3_path,
            "-i", sfx_wav,
            "-filter_complex",
            "[1:a]volume=1.15[v];[2:a]volume=0.35[s];[v][s]amix=inputs=2:duration=first:dropout_transition=1,alimiter=limit=0.94[aout]",
            "-map", "0:v:0",
            "-map", "[aout]",
            "-c:v", "libx264", "-pix_fmt", "yuv420p", "-r", "30", "-preset", "fast", "-crf", "21",
            "-c:a", "aac", "-b:a", "192k",
            "-shortest",
            out_mp4,
        ]
        subprocess.run(cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print(f"[OK] Rendered V3 Japanese Shorts MP4: {out_mp4} ({os.path.getsize(out_mp4)} bytes, {total_dur:.1f}s)")

        # Also generate Summary Card PNG
        card_path = os.path.join(out_dir, ep["card_png"])
        build_summary_card_png(
            out_png=card_path,
            ticker=sym,
            jp_name=ep["jp_name"],
            entry=gv(sym, "entry", 186.64),
            stop_loss=gv(sym, "stop_loss", 170.60),
            target_25r=gv(sym, "target_25r", 226.74),
            score=gv(sym, "score", 91.0),
            catalyst_desc="SEC 8-K適時開示 · Form-4役員買い · オプションGamma Wall 日本語AI解析",
        )
        print(f"[OK] Generated Japanese X Summary Card PNG: {card_path}")

        abc_log.append({
            "episode": ep["file"],
            "ticker": sym,
            "voice": ep["voice"],
            "abc_candidates": ep["abc_hooks"],
            "selected_hook": ep["selected_hook"],
            "duration_sec": round(total_dur, 2),
        })

    with open(os.path.join(out_dir, "abc_hook_selection.json"), "w", encoding="utf-8") as f:
        json.dump(abc_log, f, ensure_ascii=False, indent=2)

    # Generate 10 Japanese X (株クラ) High-CTR Posts
    x_posts = [
        {
            "id": 1,
            "ticker": "NVDA",
            "text": f"【エヌビディア($NVDA) 機関投資家AI解析】\n英語のSEC 8-Kと決算コールをAIが3秒解読🔥\n\n📊 AI強気スコア: 93.5/100\n⚡ Call/Put比率: 3.2倍（ガンマスクイーズ発動）\n🛡️ 2.0x ATR損切りライン: ${gv('NVDA','stop_loss',170.60):.2f}\n🎯 2.5R利確ターゲット: ${gv('NVDA','target_25r',226.74):.2f}\n\nドル・円対応の適正株数計算機👇\nhttps://getbreakai.com/?ticker=NVDA\n#米国株 #新NISA #エヌビディア #NVDA #株クラ"
        },
        {
            "id": 2,
            "ticker": "PLTR",
            "text": f"【パランティア($PLTR) ダークプール64%急増🐋】\n板情報に出ない取引所外ブロック取引で機関投資家が猛烈に買い集め中。\n\n📑 SEC 8-K国防AI契約スコア: 91.0/100\n🛡️ 2.0x ATR損切りライン: ${gv('PLTR','stop_loss',140.48):.2f}\n🎯 5日間IV上値壁: ${gv('PLTR','upper_gamma_wall',177.10):.2f} / 2.5R目標: ${gv('PLTR','target_25r',210.13):.2f}\n\n新NISA・スイング適正株数を3秒計算👇\nhttps://getbreakai.com/?ticker=PLTR\n#米国株 #新NISA #パランティア #PLTR #株クラ"
        },
        {
            "id": 3,
            "ticker": "TSLA",
            "text": f"【テスラ($TSLA) コール3.6倍のGamma Wall突破⚡】\nAsk側への大口コールスイープ流入により、マーケットメイカーの強制ヘッジ買い領域へ突入！\n\n💵 基準株価: ${gv('TSLA','entry',358.22):.2f}\n🛡️ 2.0x ATR損切りライン: ${gv('TSLA','stop_loss',322.24):.2f}\n🎯 2.5R利確目標: ${gv('TSLA','target_25r',448.17):.2f}\n\nあなたの口座資金(円/ドル)に合う適正株数👇\nhttps://getbreakai.com/?ticker=TSLA\n#米国株 #新NISA #テスラ #TSLA #株クラ"
        },
        {
            "id": 4,
            "ticker": "LLY",
            "text": f"【イーライリリー($LLY) 経営陣3名が自腹で$4.8M買い💊】\n役員が株を売る理由は様々ですが、自己資金で市場内購入(Form-4)する理由は「株価上昇への確信」ただ1つ。\n\n🐋 Form-4クラスタースコア: 89.8/100\n🛡️ 2.0x ATR損切りライン: ${gv('LLY','stop_loss',1248.38):.2f}\n🎯 2.5R利確目標: ${gv('LLY','target_25r',1618.05):.2f}\n\n詳細データ＆株数計算機👇\nhttps://getbreakai.com/?ticker=LLY\n#米国株 #新NISA #イーライリリー #インサイダー取引"
        },
        {
            "id": 5,
            "ticker": "SMCI",
            "text": f"【⚠️ $SMCI エントリー禁止・会計リスク＆機関売り警告】\n表面的なリバウンド狙いは危険です。\n\n🔴 AIカタリストスコア: 28.5/100 (DO NOT BUY / AVOID)\n📉 ダークプール機関投資家売り比率: 67%\n⚠️ SEC提出書類フォレンジック警告点灯\n\n暴落トラップを回避して$NVDA・$PLTRへ資金を守る👇\nhttps://getbreakai.com/?ticker=SMCI\n#米国株 #SMCI #新NISA #株クラ #リスク管理"
        },
        {
            "id": 6,
            "ticker": "SOXL",
            "text": "【SOXL・SMH 半導体ETFで塩漬けにならない鉄則🔥】\n3倍レバレッジETFを「なんとなくナンピン」するとボラティリティ減価で資産が溶けます。\n\n① TruthOfMarket.com で半導体恐怖強欲指数の底打ちを確認\n② GetBreakAI.com で2.0x ATR損切りと1.5%リスク株数を厳守\n\n日本語解説レポート👇\nhttps://getbreakai.com/jp/soxl-smh-semiconductor-timing.html\n#SOXL #半導体株 #米国株 #新NISA #株クラ"
        },
        {
            "id": 7,
            "ticker": "AVGO",
            "text": f"【ブロードコム($AVGO) カスタムAI半導体(ASIC)受注8-K解析🔬】\nハイパースケーラー向けXPU需要拡大で機関ダークプール買いが59%に到達。\n\n📊 AIスコア: 88.4/100\n🛡️ 2.0x ATR損切りライン: ${gv('AVGO','stop_loss',263.41):.2f}\n🎯 2.5R利確目標: ${gv('AVGO','target_25r',369.39):.2f}\n\n即時シミュレーション👇\nhttps://getbreakai.com/?ticker=AVGO\n#米国株 #ブロードコム #AVGO #新NISA #半導体株"
        },
        {
            "id": 8,
            "ticker": "VRT",
            "text": f"【AIデータセンター液冷の本命 バーティブ($VRT)❄️】\n次世代GPUラックの熱問題を解決する液冷インフラ受注残が過去最高を更新。\n\n📊 AIカタリストスコア: 88.1/100\n🛡️ 2.0x ATR損切りライン: ${gv('VRT','stop_loss',145.24):.2f}\n🎯 2.5R利確目標: ${gv('VRT','target_25r',276.91):.2f}\n\n日本語レポート＆計算機👇\nhttps://getbreakai.com/jp/vrt-ai-datacenter-cooling-catalyst.html\n#米国株 #VRT #AIデータセンター #新NISA"
        },
        {
            "id": 9,
            "ticker": "CEG",
            "text": f"【AI原発電力PPA契約 コンステレーション・エナジー($CEG)⚡】\nハイパースケーラーとの長期原子力電力供給契約(SEC 8-K)をAIが高く評価。\n\n📊 AIスコア: 87.0/100\n🛡️ 2.0x ATR損切りライン: ${gv('CEG','stop_loss',225.91):.2f}\n🎯 2.5R利確目標: ${gv('CEG','target_25r',310.05):.2f}\n\n詳細解析👇\nhttps://getbreakai.com/jp/ceg-nuclear-ai-power-8k-contract.html\n#米国株 #CEG #AI電力 #新NISA #株クラ"
        },
        {
            "id": 10,
            "ticker": "ALL",
            "text": "【新NISA・米国株スイング投資家のための無料AI武器庫🚀】\n英語のSEC 8-K開示・Form-4役員買い・オプションGamma Wallを3秒で日本語解読し、ドル($)と日本円(¥)で「適正株数＆2.0x ATR損切りライン」を自動算出！\n\n全30銘柄の日本語ディープリサーチも公開中👇\nhttps://getbreakai.com/\n#米国株 #新NISA #エヌビディア #パランティア #テスラ #SOXL #株クラ"
        }
    ]

    with open(os.path.join(out_dir, "x_posts_10.json"), "w", encoding="utf-8") as f:
        json.dump(x_posts, f, ensure_ascii=False, indent=2)

    with open(os.path.join(out_dir, "x_posts_10.md"), "w", encoding="utf-8") as f:
        f.write(f"# 日本X (株クラ) ワンクリック投稿用ドラフト10選 ({date_str})\n\n")
        for p in x_posts:
            f.write(f"## Post #{p['id']} (${p['ticker']})\n```text\n{p['text']}\n```\n\n")

    # Generate note.com Japanese Research Column Draft
    note_md = f"""# 【米国株・新NISA】ウォール街の英語SEC開示(8-K)・インサイダー買い(Form-4)・ガンマスクイーズをAIで3秒解読し、ATR損切りで資産を守る方法（{date_str}最新版）

日本の個人投資家が米国株（エヌビディア `$NVDA`、パランティア `$PLTR`、テスラ `$TSLA`、イーライリリー `$LLY` など）で機関投資家に勝つための最大の鍵は、**「一次情報（SEC適時開示・オプション需給）のスピード」**と**「ボラティリティに応じた機械的な資金管理（2.0x ATR損切り）」**にあります。

## 1. 本日の注目米国株 AIカタリスト＆ATR損切りライン一覧（1ドル＝150円換算）

| 銘柄 | AIスコア | カタリスト・機関動向 | 現在株価 | 2.0x ATR損切り | 2.5R 利確目標 |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **$NVDA エヌビディア** | **93.5/100** | Blackwell増産・Call 3.2倍GEX | ${gv('NVDA','entry',186.64):.2f} | ${gv('NVDA','stop_loss',170.60):.2f} | **${gv('NVDA','target_25r',226.74):.2f}** |
| **$PLTR パランティア** | **91.0/100** | 国防AI 8-K契約・DP比率64% | ${gv('PLTR','entry',160.38):.2f} | ${gv('PLTR','stop_loss',140.48):.2f} | **${gv('PLTR','target_25r',210.13):.2f}** |
| **$LLY イーライリリー** | **89.8/100** | 経営陣3名 Form-4自腹買い$4.8M | ${gv('LLY','entry',1354.00):.2f} | ${gv('LLY','stop_loss',1248.38):.2f} | **${gv('LLY','target_25r',1618.05):.2f}** |
| **$TSLA テスラ** | **89.7/100** | 週次Call Wall突破・GEX踏み上げ | ${gv('TSLA','entry',358.22):.2f} | ${gv('TSLA','stop_loss',322.24):.2f} | **${gv('TSLA','target_25r',448.17):.2f}** |
| **$SMCI (⚠️警告)** | **28.5/100** | 🔴 会計リスク・DP機関売り67% | ${gv('SMCI','entry',28.76):.2f} | **エントリー禁止** | **見送り推奨** |

## 2. ドル($)＆日本円(¥)同時対応のATR適正株数シミュレーター
👉 **無料ターミナルはこちら:** [https://getbreakai.com/](https://getbreakai.com/)
👉 **30銘柄の日本語ディープリサーチ一覧:** [https://getbreakai.com/jp/index.html](https://getbreakai.com/jp/index.html)
"""
    with open(os.path.join(out_dir, "note_com_article_jp.md"), "w", encoding="utf-8") as f:
        f.write(note_md)

    shutil.rmtree(tmp_dir, ignore_errors=True)
    print(f"[OK] Saved 10 Japanese X posts + 3 summary cards + note.com article + 3 MP4 shorts in {out_dir}")


if __name__ == "__main__":
    asyncio.run(main())
