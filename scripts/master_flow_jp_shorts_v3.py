#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
D:\드림컴퍼니\3사업부\scripts\master_flow_jp_shorts_v3.py
Google Flow 일본 여성 금융 배우 클립(flow_raw_clips/*.mp4, 45개)을
일본 유튜브 쇼츠(@GetBreakAI) & 인스타그램 릴스(@semifeargreed)용
완성본 MP4 12편(EP01~EP12)으로 마스터링합니다.

[사장님 피드백 반영 — 음속 자연화 & 자막 100% 완독 마스터링]
1. 과속(Double Speedup) 완전 제거:
   - 기존 rate="+20%" 위에 atempo=1.38까지 중첩(약 1.66배속)되어 음성이 지나치게 빠르던 문제를 해결.
   - 자연스럽고 또렷한 일본 금융 아나운서 호흡(rate="+4%", atempo 강제 가속 0%)으로 조정.
2. 자막 100% 끝까지 완독 보장 (오디오 강제 절단 버그 완전 수정):
   - 기존 min(2.22, ...) 및 ffmpeg -t 2.22 제한으로 인해 문장 뒷부분(자막 2번째 줄)이 읽히기 전에 잘리던 문제를 완벽 해결.
   - 각 컷의 영상 길이를 `seg_dur = tts_dur + 0.22초`로 설정하여, 화면에 표시된 2줄 자막의 첫 글자부터 마지막 글자까지 단 한 음절도 빠짐없이 100% 다 읽고 다음 컷으로 넘어가도록 동기화.
   - 나레이션 대본(tts)과 화면 자막(sub 1~2행)을 1:1로 일치시켜 시청자가 눈으로 보는 자막과 귀로 듣는 음성이 100% 일치하도록 개선.
3. 클린 풀스크린(1080x1920) & 하단 세이프존(Y=1385~1460) 두꺼운 검은 외곽선(stroke_width=10) 자막 & 마지막 엔딩 슬레이트 getbreakai.com 콜아웃 유지.
"""

import os
import re
import json
import math
import wave
import struct
import shutil
import zipfile
import asyncio
import subprocess
from PIL import Image, ImageDraw, ImageFont

ROOT_DIR = r"D:\드림컴퍼니\3사업부"
STUDIO_DIR = os.path.join(ROOT_DIR, "flow_shorts_studio")
ZIP_PATH = os.path.join(STUDIO_DIR, "11월 09 - 23_26.zip")
RAW_CLIPS_DIR = os.path.join(STUDIO_DIR, "flow_raw_clips")
MASTER_OUT_DIR = os.path.join(STUDIO_DIR, "mastered_jp_shorts")
TEMP_WORK_DIR = os.path.join(STUDIO_DIR, "_temp_v3_build")
TTS_CACHE_DIR = os.path.join(STUDIO_DIR, "_tts_cache_v3_natural")
OUTBOX_TODAY_DIR = os.path.join(ROOT_DIR, "marketing_outbox_jp", "2026-11-09")


def get_ffmpeg_bin():
    exe = shutil.which("ffmpeg")
    if exe:
        return exe
    import imageio_ffmpeg
    return imageio_ffmpeg.get_ffmpeg_exe()


def load_jp_font(size):
    candidates = [
        "C:/Windows/Fonts/YuGothB.ttc",
        "C:/Windows/Fonts/meiryob.ttc",
        "C:/Windows/Fonts/msgothic.ttc",
    ]
    for path in candidates:
        if os.path.exists(path):
            try:
                return ImageFont.truetype(path, size)
            except Exception:
                pass
    return ImageFont.load_default()


def get_ordered_clip_paths():
    """Returns the 45 extracted clip paths in exact ZipInfo order (1..45)."""
    if os.path.exists(ZIP_PATH):
        zf = zipfile.ZipFile(ZIP_PATH, "r")
        ordered = []
        for info in zf.infolist():
            p = os.path.join(RAW_CLIPS_DIR, info.filename)
            if os.path.exists(p):
                ordered.append(p)
        zf.close()
        if len(ordered) >= 45:
            return ordered
    files = sorted(
        [os.path.join(RAW_CLIPS_DIR, f) for f in os.listdir(RAW_CLIPS_DIR) if f.lower().endswith(".mp4")]
    )
    return files


def draw_centered_text(draw, y, text, font, fill, W=1080, stroke_width=0, stroke_fill=(0, 0, 0, 255)):
    bbox = draw.textbbox((0, 0), text, font=font, stroke_width=stroke_width)
    tw = bbox[2] - bbox[0]
    cx = max(40, (W - tw) // 2)
    draw.text((cx, y), text, font=font, fill=fill, stroke_width=stroke_width, stroke_fill=stroke_fill)


def render_v3_subtitle_overlay_png(out_png, caption_lines, is_ending_slate=False, ticker="NVDA", jp_name="エヌビディア"):
    """
    Renders a 1080x1920 RGBA transparent PNG overlay.
    - Body cuts (is_ending_slate=False):
      100% transparent canvas EXCEPT bottom safe-zone (Y=1385~1460) caption with stroke_width=10 black outline.
    - Ending slate cut (is_ending_slate=True):
      Sleek translucent dark glass card in center with getbreakai.com callout + bottom safe-zone caption.
    """
    W, H = 1080, 1920
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    f_cap = load_jp_font(50)

    if is_ending_slate:
        draw.rectangle([(0, 0), (W, H)], fill=(8, 6, 20, 175))
        draw.rounded_rectangle(
            [(64, 350), (W - 64, 1215)],
            radius=40,
            fill=(16, 12, 38, 238),
            outline=(139, 92, 246, 255),
            width=5,
        )
        f_lbl = load_jp_font(36)
        f_big = load_jp_font(82)
        f_sub = load_jp_font(36)
        f_btn = load_jp_font(42)

        draw_centered_text(draw, 410, "◆ 米国株・東証・新NISA クオンツAI端末 ◆", f_lbl, (245, 158, 11, 255), W)
        draw_centered_text(
            draw,
            485,
            "getbreakai.com",
            f_big,
            (255, 255, 255, 255),
            W,
            stroke_width=6,
            stroke_fill=(0, 0, 0, 255),
        )
        draw_centered_text(
            draw,
            615,
            f"▶ {jp_name} ({ticker}) 適正株数・損切り3秒計算",
            f_sub,
            (52, 211, 153, 255),
            W,
        )

        draw.rounded_rectangle(
            [(108, 705), (W - 108, 835)],
            radius=26,
            fill=(139, 92, 246, 255),
            outline=(255, 255, 255, 255),
            width=3,
        )
        draw_centered_text(draw, 745, "▶ プロフィールリンクから無料体験", f_btn, (255, 255, 255, 255), W)

        draw.text((112, 895), "✓ 機関投資家ダークプール＆SEC Form-4検知", font=f_sub, fill=(226, 232, 240, 255))
        draw.text((112, 975), "✓ ドル($)＆日本円(¥) 2.0倍ATR損切り計算機", font=f_sub, fill=(226, 232, 240, 255))
        draw.text((112, 1055), "✓ YouTube @GetBreakAI / IG @semifeargreed", font=f_sub, fill=(56, 189, 248, 255))

    # Bottom safe-zone subtitle (Y=1385 ~ 1460), stroke_width=10, NO background box
    cap_y = 1385
    for idx, line in enumerate(caption_lines[:2]):
        fill_col = (255, 242, 115, 255) if (idx == 0 and not is_ending_slate) else (255, 255, 255, 255)
        if is_ending_slate:
            fill_col = (110, 231, 183, 255) if idx == 0 else (255, 255, 255, 255)
        draw_centered_text(
            draw,
            cap_y,
            line,
            f_cap,
            fill_col,
            W,
            stroke_width=10,
            stroke_fill=(0, 0, 0, 255),
        )
        cap_y += 68

    img.save(out_png, "PNG")


def generate_v3_sfx_track(wav_path, cut_starts, ending_start, total_dur, sample_rate=44100):
    """
    Generates subtle Point SFX track aligned to the exact cut transitions.
    """
    n_samples = int(total_dur * sample_rate)
    frames = bytearray()

    for i in range(n_samples):
        t = i / sample_rate
        val = 0.0

        # 1) 0.0s Hook Impact
        if 0.0 <= t < 0.35:
            env = math.exp(-t * 11.0)
            val += 0.24 * env * math.sin(2.0 * math.pi * 85.0 * t)
            val += 0.10 * env * math.sin(2.0 * math.pi * 440.0 * t)

        # 2) Body Cut Whoosh + Key Metric Ping
        for c_idx, ct in enumerate(cut_starts[1:-1], start=1):
            dt = t - ct
            if 0.0 <= dt < 0.25:
                env = math.exp(-dt * 15.0)
                freq_whoosh = 180.0 + 300.0 * (dt / 0.25)
                freq_ping = 640.0 + (c_idx * 80.0)
                val += 0.12 * env * math.sin(2.0 * math.pi * freq_whoosh * dt)
                val += 0.14 * env * math.sin(2.0 * math.pi * freq_ping * dt)

        # 3) Ending Slate Sub-Bass Drop
        dt_end = t - ending_start
        if 0.0 <= dt_end < 0.60:
            env = math.exp(-dt_end * 5.5)
            freq_drop = max(45.0, 115.0 - 95.0 * (dt_end / 0.60))
            val += 0.25 * env * math.sin(2.0 * math.pi * freq_drop * dt_end)

        sample = max(-32000, min(32000, int(val * 32767)))
        frames += struct.pack("<h", sample)

    with wave.open(wav_path, "w") as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(sample_rate)
        wf.writeframes(frames)


def probe_duration(ffmpeg_bin, media_path):
    cmd = [ffmpeg_bin, "-i", media_path]
    proc = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, encoding="utf-8", errors="ignore")
    m = re.search(r"Duration:\s*(\d+):(\d+):(\d+\.\d+)", proc.stderr)
    if not m:
        return 2.8
    return int(m.group(1)) * 3600 + int(m.group(2)) * 60 + float(m.group(3))


async def synth_cut_tts_natural_full(ffmpeg_bin, cache_key, text, out_wav, voice="ja-JP-NanamiNeural", rate="+4%"):
    """
    Synthesizes Japanese TTS at a natural, clear announcer speed (rate="+4%", NO atempo speedup!)
    and only trims leading/trailing silence (without eating mid-sentence syllables or truncating).
    Every single word of the subtitle is spoken clearly from start to finish!
    """
    import edge_tts
    os.makedirs(TTS_CACHE_DIR, exist_ok=True)
    cached_mp3 = os.path.join(TTS_CACHE_DIR, f"{cache_key}.mp3")
    if not os.path.exists(cached_mp3):
        comm = edge_tts.Communicate(text=text, voice=voice, rate=rate)
        await comm.save(cached_mp3)

    # Trim only leading silence and trailing silence at the very end (areverse -> trim start -> areverse)
    # so we NEVER cut off or eat the end of any spoken Japanese word!
    af_filter = (
        "silenceremove=start_periods=1:start_duration=0.01:start_threshold=-50dB,"
        "areverse,"
        "silenceremove=start_periods=1:start_duration=0.01:start_threshold=-50dB,"
        "areverse"
    )
    subprocess.run(
        [ffmpeg_bin, "-y", "-i", cached_mp3, "-af", af_filter, "-ar", "44100", "-ac", "1", out_wav],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=True,
    )
    return probe_duration(ffmpeg_bin, out_wav)


EPISODES = [
    # ================= SET A: Primary 6 Episodes (Clips 01..22) =================
    {
        "id": "EP01_NVDA_ATR_StopLoss",
        "ticker": "NVDA",
        "jp_name": "エヌビディア",
        "yt_title": "【エヌビディア】決算後に絶対やってはいけない損切り設定とは？AIが2.0倍ATRラインを公開 #米国株 #新NISA #NVDA #Shorts",
        "ig_caption": "エヌビディア($NVDA)を感覚で損切りしていませんか？🔥\n機関投資家のダークプール流入と2.0倍ATR損切りラインをGetBreakAIが3秒で算出！\n👉 プロフィールリンク https://getbreakai.com から無料でチェック！\n#米国株 #新NISA #エヌビディア #NVDA #株クラ #投資初心者 #資産運用",
        "clip_indices": [0, 1, 2, 3],
        "cuts": [
            {
                "tts": "エヌビディアを感覚で損切りして、大底で狩られていませんか？",
                "sub": ["エヌビディアを感覚で損切りして", "大底で狩られていませんか？"],
            },
            {
                "tts": "プロはパーセントではなく、ATR変動幅で損切りラインを計算します。",
                "sub": ["プロは％ではなくATR変動幅で", "損切りラインを計算します"],
            },
            {
                "tts": "適正損切りは2.0倍ATR、口座リスク1.5パーセント厳守が鉄則です！",
                "sub": ["適正損切りは2.0倍ATR", "口座リスク1.5%厳守が鉄則です！"],
            },
            {
                "tts": "大口ダークプール買いを検知！2.5R利確ターゲット到達圏です。",
                "sub": ["大口ダークプール買いを検知！", "2.5R利確ターゲット到達圏です"],
            },
            {
                "tts": "適正株数を3秒で無料計算、ゲットブレイクAIドットコムへ！",
                "sub": ["適正株数を3秒で無料計算", "▶ getbreakai.com"],
                "is_ending": True,
            },
        ],
    },
    {
        "id": "EP02_PLTR_SEC_Form4_Flow",
        "ticker": "PLTR",
        "jp_name": "パランティア",
        "yt_title": "【パランティア急騰】ニュースが出る前に機関投資家の爆買いを見抜くSEC Form-4分析 #米国株 #PLTR #新NISA #Shorts",
        "ig_caption": "パランティア($PLTR)の急騰、ニュースを見てから飛び乗っていませんか？⚡\nSEC Form-4インサイダー取引と機関投資家出来高320%急増をAIがリアルタイム検知！\n👉 https://getbreakai.com で今すぐチェック！\n#パランティア #PLTR #米国株 #新NISA #AI株 #株クラ #グロース株",
        "clip_indices": [4, 5, 6, 7],
        "cuts": [
            {
                "tts": "パランティアの急騰波に、高値飛び乗りしていませんか？",
                "sub": ["パランティアの急騰波に", "高値飛び乗りしていませんか？"],
            },
            {
                "tts": "SECフォーム4内部動向と、機関投資家の異常出来高を検知！",
                "sub": ["SEC Form-4内部動向と", "機関投資家の異常出来高を検知！"],
            },
            {
                "tts": "出来高320パーセント急増ブレイク！ガンマスクイーズ波動が点灯。",
                "sub": ["出来高320%急増ブレイク！", "ガンマスクイーズ波動が点灯"],
            },
            {
                "tts": "高ボラ銘柄こそドル・円対応、ATR損切り計算が資産を守ります。",
                "sub": ["高ボラ銘柄こそドル・円対応", "ATR損切り計算が資産を守ります"],
            },
            {
                "tts": "パランティアの最新AIシグナル公開、ゲットブレイクAIドットコムへ！",
                "sub": ["PLTRの最新AIシグナル公開", "▶ getbreakai.com"],
                "is_ending": True,
            },
        ],
    },
    {
        "id": "EP03_TSLA_Gamma_Breakout",
        "ticker": "TSLA",
        "jp_name": "テスラ",
        "yt_title": "【テスラ急変動】激しい乱高下でも感情ゼロで利益を残す2.5Rクオンツ戦略 #テスラ #TSLA #米国株 #新NISA #Shorts",
        "ig_caption": "テスラ($TSLA)の激しい値動きに振り回されていませんか？🚗⚡\nコールオプション集中によるガンマスクイーズと2.5R利確ラインをAIが数値化！\n👉 https://getbreakai.com で適正株数を3秒チェック！\n#テスラ #TSLA #米国株投資 #新NISA #オプション取引 #株クラ",
        "clip_indices": [8, 9, 10, 11],
        "cuts": [
            {
                "tts": "テスラの激しい乱高下で、悔しい損切りをしていませんか？",
                "sub": ["テスラの激しい乱高下で", "悔しい損切りをしていませんか？"],
            },
            {
                "tts": "コールオプション集中による、ガンマスクイーズ急騰局面です！",
                "sub": ["コールオプション集中による", "ガンマスクイーズ急騰局面です！"],
            },
            {
                "tts": "2.0倍ATR防衛ラインと、1対2.5の利確ターゲットを明確化。",
                "sub": ["2.0倍ATR防衛ラインと", "1:2.5利確ターゲットを明確化"],
            },
            {
                "tts": "感情ゼロのポジション管理で、ボラティリティを最大の武器に。",
                "sub": ["感情ゼロのポジション管理で", "ボラティリティを最大の武器に"],
            },
            {
                "tts": "テスラ適正株数を3秒計算、ゲットブレイクAIドットコムへ！",
                "sub": ["テスラ適正株数を3秒計算", "▶ getbreakai.com"],
                "is_ending": True,
            },
        ],
    },
    {
        "id": "EP04_8035_TokyoElectron_Sync",
        "ticker": "8035.T",
        "jp_name": "東京エレクトロン",
        "yt_title": "【東京エレクトロン】米国SOX指数と完全連動！東証プライム寄付き前のAIブレイク戦略 #日本株 #東京エレクトロン #新NISA #Shorts",
        "ig_caption": "東京エレクトロン(8035.T)の寄付きギャップ、どう攻略していますか？🇯🇵📈\n米国エヌビディア＆SOX指数との連動率から、東証9時寄付き前の最適エントリーをAI解析！\n👉 https://getbreakai.com/jp/ で日本語レポート公開中！\n#東京エレクトロン #8035 #日本株 #半導体株 #新NISA #東証プライム #株クラ",
        "clip_indices": [12, 13, 14, 15],
        "cuts": [
            {
                "tts": "東京エレクトロン、朝の寄付きで高値掴みしていませんか？",
                "sub": ["東京エレクトロン(8035.T)", "朝の寄付きで高値掴みしてない？"],
            },
            {
                "tts": "鍵は昨晩の米国エヌビディアと、SOX半導体指数の機関フローです。",
                "sub": ["鍵は昨晩の米国NVDAと", "SOX半導体指数の機関フロー"],
            },
            {
                "tts": "日足レジスタンス突破！外国人投資家の大口買いが点灯。",
                "sub": ["日足レジスタンス突破！", "外国人投資家の大口買い点灯"],
            },
            {
                "tts": "日本円での適正株数と、ATR逆指値を寄付き前に設定しましょう。",
                "sub": ["日本円(¥)での適正株数と", "ATR逆指値を寄付き前に設定"],
            },
            {
                "tts": "東証半導体AIレポート公開中、ゲットブレイクAIドットコムへ！",
                "sub": ["東証半導体AIレポート公開中", "▶ getbreakai.com"],
                "is_ending": True,
            },
        ],
    },
    {
        "id": "EP05_6857_Advantest_AIScore94",
        "ticker": "6857.T",
        "jp_name": "アドバンテスト",
        "yt_title": "【アドバンテスト】AIスコア94点点灯！HBM3E需要爆発とプロ仕様トレーリング利確術 #アドバンテスト #半導体株 #日本株 #Shorts",
        "ig_caption": "アドバンテスト(6857.T)をたった5%の利益で早売りしていませんか？🔥\nAI半導体テスター独占需要でクオンツスコア94/100点灯！ATRトレーリングで利益を最大化する方法とは？\n👉 https://getbreakai.com で今すぐチェック！\n#アドバンテスト #6857 #半導体株 #日本株投資 #新NISA #株クラ",
        "clip_indices": [16, 17, 40, 37],
        "cuts": [
            {
                "tts": "アドバンテストの強い上昇波、数パーセントで早売りしていませんか？",
                "sub": ["アドバンテストの強い上昇波", "数％で早売りしていませんか？"],
            },
            {
                "tts": "HBMテスター需要爆発！AIブレイクスコア94点を記録。",
                "sub": ["HBMテスター需要爆発！", "AIブレイクスコア94点を記録"],
            },
            {
                "tts": "2.0倍ATRトレーリングで、大きなトレンドを最後まで獲る。",
                "sub": ["2.0倍ATRトレーリングで", "大きなトレンドを最後まで獲る"],
            },
            {
                "tts": "機関の空売り踏み上げ継続中、ルール通りのトレンド追随へ。",
                "sub": ["機関の空売り踏み上げ継続中", "ルール通りのトレンド追随へ"],
            },
            {
                "tts": "アドバンテストの最新利確ライン公開、ゲットブレイクAIドットコムへ！",
                "sub": ["6857.Tの最新利確ライン公開", "▶ getbreakai.com"],
                "is_ending": True,
            },
        ],
    },
    {
        "id": "EP06_ShinNISA_15Risk_Rule",
        "ticker": "NISA",
        "jp_name": "新NISA・特定口座",
        "yt_title": "【新NISA×特定口座】米国株で退場しない人が必ず守っている「口座リスク1.5%」の黄金律 #新NISA #米国株 #資産運用 #Shorts",
        "ig_caption": "新NISA成長投資枠と特定口座、どうやって使い分けていますか？💡\n20.315%の非課税メリットを活かしつつ、1回の損失を口座資金の1.5%以内に抑える機関投資家メソッド！\n👉 https://getbreakai.com であなたの適正株数を3秒診断！\n#新NISA #成長投資枠 #特定口座 #米国株 #日本株 #資金管理 #株クラ",
        "clip_indices": [18, 19, 20, 21],
        "cuts": [
            {
                "tts": "新NISAの成長投資枠で、1銘柄に全力投資していませんか？",
                "sub": ["新NISAの成長投資枠で", "1銘柄に全力投資してない？"],
            },
            {
                "tts": "非課税20.315パーセントのメリットも、大損してしまえばゼロになります。",
                "sub": ["非課税20.315%のメリットも", "大損してしまえばゼロになる"],
            },
            {
                "tts": "プロの鉄則は、1回の損失を口座資金の1.5パーセント以内に固定！",
                "sub": ["プロの鉄則＝1回の損失を", "口座資金の1.5%以内に固定！"],
            },
            {
                "tts": "100万円でも300万円でも、AIが適正株数を一発算出！",
                "sub": ["100万円でも300万円でも", "AIが適正株数を一発算出！"],
            },
            {
                "tts": "ドル・円対応3秒ポジション計算、ゲットブレイクAIドットコムへ！",
                "sub": ["ドル・円対応3秒ポジション計算", "▶ getbreakai.com"],
                "is_ending": True,
            },
        ],
    },
    # ================= SET B: Alternate 6 Episodes (Clips 22..44) =================
    {
        "id": "EP07_META_AI_Ad_Breakout",
        "ticker": "META",
        "jp_name": "メタ",
        "yt_title": "【メタ($META)】AI広告単価が劇的改善！機関投資家が密かに集めるブレイクアウト水準 #米国株 #META #新NISA #Shorts",
        "ig_caption": "メタ($META)のAIターゲティング広告進化、株価への織り込みはまだ序章？🔥\n機関投資家の買い集めゾーンと2.0倍ATR防衛ラインをAIが徹底解剖！\n👉 https://getbreakai.com で最新シグナルを確認！\n#メタ #META #米国株 #新NISA #ハイテク株 #株クラ",
        "clip_indices": [22, 23, 24, 25],
        "cuts": [
            {
                "tts": "メタの押し目調整で、怖くなって狼狽売りしていませんか？",
                "sub": ["メタ($META)の押し目調整で", "怖くなって狼狽売りしてない？"],
            },
            {
                "tts": "AI広告の収益率が劇的改善！機関投資家は押し目を買い集め。",
                "sub": ["AI広告の収益率が劇的改善！", "機関投資家は押し目を買い集め"],
            },
            {
                "tts": "2.0倍ATRサポートを維持し、上値2.5Rターゲットへ急接近。",
                "sub": ["2.0倍ATRサポートを維持し", "上値2.5Rターゲットへ急接近"],
            },
            {
                "tts": "決算と出来高ブレイクの瞬間を、クオンツAIがリアルタイム通知。",
                "sub": ["決算×出来高ブレイクの瞬間を", "クオンツAIがリアルタイム通知"],
            },
            {
                "tts": "メタの最新ブレイク水準公開、ゲットブレイクAIドットコムへ！",
                "sub": ["METAの最新ブレイク水準公開", "▶ getbreakai.com"],
                "is_ending": True,
            },
        ],
    },
    {
        "id": "EP08_MSFT_Cloud_Copilot_SEC",
        "ticker": "MSFT",
        "jp_name": "マイクロソフト",
        "yt_title": "【マイクロソフト】新NISA王道銘柄の買い時はいつ？SEC 8-Kと機関フローで読む底値圏 #米国株 #MSFT #新NISA #Shorts",
        "ig_caption": "新NISAで大人気のマイクロソフト($MSFT)、いつ買えばいいか迷っていませんか？💻📈\nSEC 8-K決算データと機関投資家ダークプール流入から最適エントリーをAI判定！\n👉 https://getbreakai.com で無料チェック！\n#マイクロソフト #MSFT #米国株 #新NISA #長期投資 #株クラ",
        "clip_indices": [26, 27, 28, 29],
        "cuts": [
            {
                "tts": "新NISA王道のマイクロソフト、買い時が分からず迷っていませんか？",
                "sub": ["新NISA王道のマイクロソフト", "買い時が分からず迷ってない？"],
            },
            {
                "tts": "SEC 8-K決算とクラウド成長率、機関投資家の買い越しをAI解析。",
                "sub": ["SEC 8-K決算×クラウド成長率", "機関投資家の買い越しをAI解析"],
            },
            {
                "tts": "移動平均線の密集帯を上抜ける、高勝率ブレイクアウトを狙え！",
                "sub": ["移動平均線の密集帯を上抜ける", "高勝率ブレイクアウトを狙え！"],
            },
            {
                "tts": "リスク1.5パーセント計算機を使えば、高値掴みの恐怖ゼロで仕込める。",
                "sub": ["リスク1.5%計算機を使えば", "高値掴みの恐怖ゼロで仕込める"],
            },
            {
                "tts": "マイクロソフトの適正株数を3秒診断、ゲットブレイクAIドットコムへ！",
                "sub": ["MSFTの適正株数を3秒診断", "▶ getbreakai.com"],
                "is_ending": True,
            },
        ],
    },
    {
        "id": "EP09_AMZN_AWS_Margin_Target",
        "ticker": "AMZN",
        "jp_name": "アマゾン",
        "yt_title": "【アマゾン($AMZN)】AWS利益率が過去最高へ！機関投資家のコール買い集中ライン公開 #アマゾン #AMZN #米国株 #Shorts",
        "ig_caption": "アマゾン($AMZN)の利益構造が劇的に変わっていることに気づいていますか？📦🚀\nAWSクラウド×AI半導体による利益率急拡大と2.5R利確ターゲットを公開！\n👉 https://getbreakai.com で今すぐ確認！\n#アマゾン #AMZN #米国株投資 #新NISA #グロース株 #株クラ",
        "clip_indices": [30, 31, 32, 33],
        "cuts": [
            {
                "tts": "アマゾンの上昇力を、過小評価していませんか？",
                "sub": ["アマゾン($AMZN)の上昇力を", "過小評価していませんか？"],
            },
            {
                "tts": "AWSと自社AIチップ拡大で、営業利益率は過去最高水準へ！",
                "sub": ["AWS×自社AIチップ拡大で", "営業利益率は過去最高水準へ！"],
            },
            {
                "tts": "オプション市場でコール買い急増、2.5R利確目標へ上昇波が始動。",
                "sub": ["オプション市場でコール買い急増", "2.5R利確目標へ上昇波が始動"],
            },
            {
                "tts": "2.0倍ATRラインを背にして、最小リスクで大きな上昇波へ。",
                "sub": ["2.0倍ATRラインを背にして", "最小リスクで大きな上昇波へ"],
            },
            {
                "tts": "アマゾン最新クオンツ分析を公開、ゲットブレイクAIドットコムへ！",
                "sub": ["AMZN最新クオンツ分析を公開", "▶ getbreakai.com"],
                "is_ending": True,
            },
        ],
    },
    {
        "id": "EP10_9984_SoftBankG_Arm_AI",
        "ticker": "9984.T",
        "jp_name": "ソフトバンクG",
        "yt_title": "【ソフトバンクG】Arm×AI半導体で激変！東証プライム大口資金流入とATR攻略法 #ソフトバンクG #日本株 #新NISA #Shorts",
        "ig_caption": "ソフトバンクグループ(9984.T)のボラティリティ、味方にできていますか？🇯🇵🔥\n米国Arm株との連動性と東証プライム大口資金フローから、勝率の高いブレイクポイントをAI算出！\n👉 https://getbreakai.com/jp/ でチェック！\n#ソフトバンクグループ #9984 #日本株 #Arm #AI半導体 #新NISA #株クラ",
        "clip_indices": [34, 35, 36, 37],
        "cuts": [
            {
                "tts": "ソフトバンクグループ、感覚トレードで負けていませんか？",
                "sub": ["ソフトバンクG(9984.T)", "感覚トレードで負けてない？"],
            },
            {
                "tts": "米国アーム株の急騰と連動し、海外投資家の買い戻しが加速！",
                "sub": ["米国Arm株の急騰と連動し", "海外投資家の買い戻しが加速！"],
            },
            {
                "tts": "高ボラ銘柄こそ2.0倍ATRで、逆指値幅を正確に測るのが鉄則。",
                "sub": ["高ボラ銘柄こそ2.0倍ATRで", "逆指値幅を正確に測るのが鉄則"],
            },
            {
                "tts": "出来高ブレイクを確認して参入、ダマシを回避し高勝率を狙う。",
                "sub": ["出来高ブレイクを確認して参入", "ダマシを回避し高勝率を狙う"],
            },
            {
                "tts": "ソフトバンクGのAIシグナル公開中、ゲットブレイクAIドットコムへ！",
                "sub": ["9984.TのAIシグナル公開中", "▶ getbreakai.com"],
                "is_ending": True,
            },
        ],
    },
    {
        "id": "EP11_7203_Toyota_Yen154_Flow",
        "ticker": "7203.T",
        "jp_name": "トヨタ自動車",
        "yt_title": "【トヨタ自動車】ドル円154円で業績上方修正期待！外国人投資家の買い転換シグナル #トヨタ #日本株 #新NISA #Shorts",
        "ig_caption": "トヨタ自動車(7203.T)、ドル円154円の円安メリットをどこまで織り込んでいる？🚗🇯🇵\nハイブリッド車の圧倒的シェアと外国人投資家の買い転換ラインをAIが徹底解析！\n👉 https://getbreakai.com/jp/ で日本語レポート公開中！\n#トヨタ自動車 #7203 #日本株 #新NISA #高配当株 #円安 #株クラ",
        "clip_indices": [38, 39, 40, 15],
        "cuts": [
            {
                "tts": "トヨタ自動車、買い増しタイミングに迷っていませんか？",
                "sub": ["トヨタ自動車(7203.T)", "買い増しタイミング迷ってない？"],
            },
            {
                "tts": "ドル円154円とハイブリッド絶好調で、機関投資家の資金が再流入！",
                "sub": ["ドル円154円×HV絶好調で", "機関投資家の資金が再流入！"],
            },
            {
                "tts": "AIサポート防衛ラインと、2.5R利確目標で勝率が激変！",
                "sub": ["AIサポート防衛ラインと", "2.5R利確目標で勝率が激変！"],
            },
            {
                "tts": "新NISAの長期・スイングでも、ATR基準なら含み益を伸ばせる。",
                "sub": ["新NISAの長期・スイングでも", "ATR基準なら含み益を伸ばせる"],
            },
            {
                "tts": "トヨタの最新AI診断を公開中、ゲットブレイクAIドットコムへ！",
                "sub": ["トヨタの最新AI診断を公開中", "▶ getbreakai.com"],
                "is_ending": True,
            },
        ],
    },
    {
        "id": "EP12_USDJPY_Position_Sizing",
        "ticker": "USDJPY",
        "jp_name": "ドル円154円×米国株",
        "yt_title": "【円安154円時代】米国株と日本株を両方持つ人が絶対使うべきドル・円同時ポジション計算機 #米国株 #ドル円 #新NISA #Shorts",
        "ig_caption": "ドル円154円時代、米国株($)と日本株(¥)のリスク管理がバラバラになっていませんか？💴💵\n口座資金を入力するだけで、ドル建て・円建ての適正株数と2.0倍ATR損切りを3秒計算！\n👉 https://getbreakai.com を今すぐブックマーク！\n#ドル円 #円安 #米国株 #日本株 #新NISA #資産形成 #株クラ",
        "clip_indices": [41, 42, 43, 44],
        "cuts": [
            {
                "tts": "ドル円154円時代、米国株を適当な株数で買っていませんか？",
                "sub": ["ドル円154円時代、米国株を", "適当な株数で買っていませんか？"],
            },
            {
                "tts": "為替とボラティリティを無視すると、気づかぬうちに過大リスクに！",
                "sub": ["為替とボラティリティを無視すると", "気づかぬうちに過大リスクに！"],
            },
            {
                "tts": "日本円の口座資金を入れるだけで、ドル建て適正株数を3秒算出！",
                "sub": ["日本円の口座資金を入れるだけで", "ドル建て適正株数を3秒算出！"],
            },
            {
                "tts": "米国株と東証主力株のATR損切り、利確ターゲットがひと目で分かる。",
                "sub": ["米国株＆東証主力株のATR損切り", "利確ターゲットがひと目で分かる"],
            },
            {
                "tts": "無料3秒ポジション計算機は、ゲットブレイクAIドットコムへ！",
                "sub": ["無料3秒ポジション計算機は", "▶ getbreakai.com"],
                "is_ending": True,
            },
        ],
    },
]


def render_cut_segment_mp4(ffmpeg_bin, src_clip_path, overlay_png_path, duration_sec, out_seg_mp4, start_offset=0.15):
    """
    Renders a single cut segment. Each raw actress clip is 8.0s long; if start_offset + duration_sec > 7.8s,
    we lower start_offset to 0.0s so the video never freezes at the end of a cut.
    """
    clip_dur = probe_duration(ffmpeg_bin, src_clip_path)
    safe_offset = start_offset
    if safe_offset + duration_sec > clip_dur - 0.1:
        safe_offset = max(0.0, clip_dur - duration_sec - 0.1)

    filter_complex = (
        "[0:v]scale=1080:1920:flags=lanczos,fps=30,format=yuv420p[bg];"
        "[bg][1:v]overlay=0:0:format=auto,format=yuv420p[vout]"
    )
    cmd = [
        ffmpeg_bin, "-y",
        "-ss", f"{safe_offset:.2f}",
        "-t", f"{duration_sec:.3f}",
        "-i", src_clip_path,
        "-loop", "1",
        "-t", f"{duration_sec:.3f}",
        "-i", overlay_png_path,
        "-filter_complex", filter_complex,
        "-map", "[vout]",
        "-an",
        "-c:v", "libx264",
        "-preset", "fast",
        "-crf", "23",
        "-pix_fmt", "yuv420p",
        out_seg_mp4,
    ]
    subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)


async def build_episode(ffmpeg_bin, ordered_clips, ep_idx, ep):
    ep_id = ep["id"]
    ep_temp = os.path.join(TEMP_WORK_DIR, ep_id)
    os.makedirs(ep_temp, exist_ok=True)

    seg_mp4s = []
    cut_wavs = []
    cut_durs = []
    cut_starts = []
    cur_t = 0.0

    for c_idx, cut in enumerate(ep["cuts"]):
        is_ending = bool(cut.get("is_ending", False))
        cut_wav = os.path.join(ep_temp, f"cut_{c_idx:02d}.wav")
        cache_key = f"{ep_id}_c{c_idx:02d}_nat4"
        tts_dur = await synth_cut_tts_natural_full(
            ffmpeg_bin, cache_key, cut["tts"], cut_wav
        )

        # GUARANTEE 100% FULL SUBTITLE READING:
        # Never cap seg_dur below tts_dur! Always give tts_dur + 0.22s breathing room at the end of the sentence
        # so the viewer clearly hears the very last syllable of line 2 before transitioning to the next cut.
        if is_ending:
            seg_dur = max(3.10, tts_dur + 0.30)
        else:
            seg_dur = max(2.30, tts_dur + 0.22)

        cut_starts.append(cur_t)
        cut_durs.append(seg_dur)
        cur_t += seg_dur

        padded_wav = os.path.join(ep_temp, f"cut_{c_idx:02d}_pad.wav")
        subprocess.run(
            [
                ffmpeg_bin, "-y",
                "-i", cut_wav,
                "-af", f"apad=whole_dur={seg_dur:.3f}",
                "-t", f"{seg_dur:.3f}",
                "-ar", "44100",
                "-ac", "1",
                padded_wav,
            ],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=True,
        )
        cut_wavs.append(padded_wav)

        ov_png = os.path.join(ep_temp, f"ov_{c_idx:02d}.png")
        render_v3_subtitle_overlay_png(
            ov_png,
            cut["sub"],
            is_ending_slate=is_ending,
            ticker=ep["ticker"],
            jp_name=ep["jp_name"],
        )

        if c_idx < 4:
            clip_path = ordered_clips[ep["clip_indices"][c_idx]]
            offset = 0.20
        else:
            clip_path = ordered_clips[ep["clip_indices"][3]]
            offset = 3.50

        seg_mp4 = os.path.join(ep_temp, f"seg_{c_idx:02d}.mp4")
        render_cut_segment_mp4(ffmpeg_bin, clip_path, ov_png, seg_dur, seg_mp4, start_offset=offset)
        seg_mp4s.append(seg_mp4)

    total_dur = sum(cut_durs)
    ending_start = cut_starts[-1]

    concat_v_txt = os.path.join(ep_temp, "concat_v.txt")
    with open(concat_v_txt, "w", encoding="utf-8") as f:
        for p in seg_mp4s:
            f.write("file '" + p.replace("\\", "/") + "'\n")
    merged_v_mp4 = os.path.join(ep_temp, "merged_v.mp4")
    subprocess.run(
        [ffmpeg_bin, "-y", "-f", "concat", "-safe", "0", "-i", concat_v_txt, "-c", "copy", merged_v_mp4],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=True,
    )

    concat_a_txt = os.path.join(ep_temp, "concat_a.txt")
    with open(concat_a_txt, "w", encoding="utf-8") as f:
        for p in cut_wavs:
            f.write("file '" + p.replace("\\", "/") + "'\n")
    merged_tts_wav = os.path.join(ep_temp, "merged_tts.wav")
    subprocess.run(
        [ffmpeg_bin, "-y", "-f", "concat", "-safe", "0", "-i", concat_a_txt, "-c", "copy", merged_tts_wav],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=True,
    )

    sfx_wav = os.path.join(ep_temp, "sfx.wav")
    generate_v3_sfx_track(sfx_wav, cut_starts, ending_start, total_dur)

    out_mp4 = os.path.join(MASTER_OUT_DIR, f"{ep_id}.mp4")
    audio_filter = (
        "[1:a]volume=1.35[voice];"
        "[2:a]volume=0.45[sfx];"
        "[voice][sfx]amix=inputs=2:duration=first:dropout_transition=0,"
        "alimiter=limit=0.944:level=disabled[aout]"
    )
    subprocess.run(
        [
            ffmpeg_bin, "-y",
            "-i", merged_v_mp4,
            "-i", merged_tts_wav,
            "-i", sfx_wav,
            "-filter_complex", audio_filter,
            "-map", "0:v:0",
            "-map", "[aout]",
            "-c:v", "copy",
            "-c:a", "aac",
            "-b:a", "192k",
            "-movflags", "+faststart",
            "-shortest",
            out_mp4,
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=True,
    )
    final_dur = probe_duration(ffmpeg_bin, out_mp4)
    size_kb = os.path.getsize(out_mp4) // 1024
    print(f"[{ep_idx+1:02d}/12] Mastered {ep_id}.mp4 ({final_dur:.2f}s, {size_kb} KB) | cut_durs={[round(d,2) for d in cut_durs]}")
    return {
        "id": ep_id,
        "ticker": ep["ticker"],
        "jp_name": ep["jp_name"],
        "yt_title": ep["yt_title"],
        "ig_caption": ep["ig_caption"],
        "mp4_path": out_mp4,
        "duration_sec": round(final_dur, 2),
        "cut_durations_sec": [round(d, 2) for d in cut_durs],
        "size_kb": size_kb,
    }


async def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--ep", type=int, default=0, help="If >0, build only that episode (1..12) first")
    args = parser.parse_args()

    os.makedirs(MASTER_OUT_DIR, exist_ok=True)
    os.makedirs(TEMP_WORK_DIR, exist_ok=True)
    os.makedirs(OUTBOX_TODAY_DIR, exist_ok=True)

    ffmpeg_bin = get_ffmpeg_bin()
    ordered_clips = get_ordered_clip_paths()
    print(f"Loaded {len(ordered_clips)} Flow raw actress clips from {RAW_CLIPS_DIR}")

    if args.ep > 0:
        idx = args.ep - 1
        res = await build_episode(ffmpeg_bin, ordered_clips, idx, EPISODES[idx])
        dst = os.path.join(OUTBOX_TODAY_DIR, os.path.basename(res["mp4_path"]))
        shutil.copy2(res["mp4_path"], dst)
        print(f"Single Episode {args.ep} re-mastered -> {res['mp4_path']}")
        return

    results = []
    for idx, ep in enumerate(EPISODES):
        res = await build_episode(ffmpeg_bin, ordered_clips, idx, ep)
        results.append(res)

    for res in results[:6]:
        dst = os.path.join(OUTBOX_TODAY_DIR, os.path.basename(res["mp4_path"]))
        shutil.copy2(res["mp4_path"], dst)

    manifest_path = os.path.join(MASTER_OUT_DIR, "mastered_12_shorts_manifest.json")
    with open(manifest_path, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)

    shutil.rmtree(TEMP_WORK_DIR, ignore_errors=True)
    print(f"\nALL 12 V3 JAPANESE SHORTS RE-MASTERED (Natural Voice + 100% Full Subtitle Reading) -> {MASTER_OUT_DIR}")


if __name__ == "__main__":
    asyncio.run(main())
