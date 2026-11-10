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
    # ================= SET C: Expansion 12 Episodes (EP13..EP24) =================
    {
        "id": "EP13_LLY_GLP1_Insider_Flow",
        "ticker": "LLY",
        "jp_name": "イーライリリー",
        "yt_title": "【イーライリリー】肥満症薬独占と役員の自腹480万ドル買い！プロが見る押し目ライン #米国株 #新NISA #LLY #Shorts",
        "ig_caption": "イーライリリー($LLY)を感覚で高値掴みしていませんか？💊🔥\nGLP-1肥満症薬の独占需要と役員3名の自腹市場内買いをAIがSEC Form-4で検知！\n2.0倍ATR損切りラインと2.5R目標株価をGetBreakAIが3秒で算出！\n👉 プロフィールリンク https://getbreakai.com から無料でチェック！\n#米国株 #新NISA #イーライリリー #LLY #ヘルスケア #株クラ #投資初心者",
        "clip_indices": [4, 5, 12, 13],
        "cuts": [
            {
                "tts": "イーライリリーを高値掴みして、調整で慌てて売っていませんか？",
                "sub": ["イーライリリーを高値掴みして", "調整で慌てて売っていませんか？"],
            },
            {
                "tts": "SECフォーム4で、経営陣3名が自腹480万ドルの市場内買いを検知！",
                "sub": ["SEC Form-4で経営陣3名が", "自腹480万ドルの市場内買いを検知！"],
            },
            {
                "tts": "適正損切りは2.0倍ATR、口座リスク1.5パーセント厳守が鉄則です！",
                "sub": ["適正損切りは2.0倍ATR", "口座リスク1.5%厳守が鉄則です！"],
            },
            {
                "tts": "AIスコア89点点灯！2.5R利確ターゲット1630ドル圏です。",
                "sub": ["AIスコア89点点灯！", "2.5R利確ターゲット1630ドル圏です"],
            },
            {
                "tts": "適正株数を3秒で無料計算、ゲットブレイクAIドットコムへ！",
                "sub": ["適正株数を3秒で無料計算", "▶ getbreakai.com"],
                "is_ending": True,
            },
        ],
    },
    {
        "id": "EP14_AVGO_Custom_ASIC_Breakout",
        "ticker": "AVGO",
        "jp_name": "ブロードコム",
        "yt_title": "【ブロードコム急伸】カスタムAI半導体受注爆発！大口ダークプール59％買いの正体 #米国株 #新NISA #AVGO #Shorts",
        "ig_caption": "ブロードコム($AVGO)の上昇に乗り遅れていませんか？⚡📈\nカスタムAI半導体(ASIC)受注急増とダークプール機関買い59%をAIが瞬時に検出！\n2.0倍ATR損切り＆適正株数を今すぐチェック！\n👉 https://getbreakai.com\n#ブロードコム #AVGO #米国株 #AI半導体 #新NISA #株クラ #クオンツ",
        "clip_indices": [14, 15, 22, 23],
        "cuts": [
            {
                "tts": "ブロードコムの急伸、ニュースが出てから追っていませんか？",
                "sub": ["ブロードコムの急伸", "ニュースが出てから追っていませんか？"],
            },
            {
                "tts": "カスタムAI半導体受注増と、ダークプール機関買い59パーセントを検知！",
                "sub": ["カスタムAI半導体受注増と", "ダークプール機関買い59%を検知！"],
            },
            {
                "tts": "ブレイク後はパーセントではなく、ATR変動幅で損切りを設定！",
                "sub": ["ブレイク後は％ではなく", "ATR変動幅で損切りを設定！"],
            },
            {
                "tts": "2.5R利確ターゲット212ドル、大口資金の追随シグナル点灯です。",
                "sub": ["2.5R利確ターゲット212ドル", "大口資金の追随シグナル点灯です"],
            },
            {
                "tts": "ブロードコムのAIシグナル公開中、ゲットブレイクAIドットコムへ！",
                "sub": ["AVGOのAIシグナル公開中", "▶ getbreakai.com"],
                "is_ending": True,
            },
        ],
    },
    {
        "id": "EP15_AMD_MI350_Donchian_Breakout",
        "ticker": "AMD",
        "jp_name": "AMD",
        "yt_title": "【AMD急反発】ドンチアン20日高値ブレイク！機関コール集積で急所を狙う #米国株 #新NISA #AMD #Shorts",
        "ig_caption": "AMD($AMD)の値動きに感情でトレードしていませんか？🔥💻\nMI350 AI GPUシェア拡大とドンチアン20日高値ブレイクをAIが完全補足！\n👉 https://getbreakai.com で適正株数を3秒計算！\n#AMD #米国株 #半導体株 #新NISA #資産運用 #株クラ",
        "clip_indices": [24, 25, 2, 3],
        "cuts": [
            {
                "tts": "AMDの激しい上下動で、損切り貧乏になっていませんか？",
                "sub": ["AMDの激しい上下動で", "損切り貧乏になっていませんか？"],
            },
            {
                "tts": "ドンチアン20日高値ブレイクと、コールオプションの異常集積を検知！",
                "sub": ["ドンチアン20日高値ブレイクと", "コールオプションの異常集積を検知！"],
            },
            {
                "tts": "適正損切りはATR変動幅の2倍、感情を排除したルール徹底を！",
                "sub": ["適正損切りはATR変動幅の2倍", "感情を排除したルール徹底を！"],
            },
            {
                "tts": "目標株価は2.5Rの175ドル、上値ガンマウォール接近中！",
                "sub": ["目標株価は2.5Rの175ドル", "上値ガンマウォール接近中！"],
            },
            {
                "tts": "無料3秒適正株数計算は、ゲットブレイクAIドットコムへ！",
                "sub": ["無料3秒適正株数計算は", "▶ getbreakai.com"],
                "is_ending": True,
            },
        ],
    },
    {
        "id": "EP16_CRWD_Falcon_ARR_PEAD",
        "ticker": "CRWD",
        "jp_name": "クラウドストライク",
        "yt_title": "【クラウドストライク】決算発表後の株価ドリフト(PEAD)をクオンツで仕留める方法 #米国株 #新NISA #CRWD #Shorts",
        "ig_caption": "クラウドストライク($CRWD)の決算ギャップに慌てて飛びついていませんか？🛡️⚡\n決算発表後ドリフト(PEAD)と大口資金フローをGetBreakAIがリアルタイム算出！\n👉 https://getbreakai.com で無料チェック！\n#クラウドストライク #CRWD #サイバーセキュリティ #米国株 #新NISA #株クラ",
        "clip_indices": [6, 7, 16, 17],
        "cuts": [
            {
                "tts": "クラウドストライクの決算発表直後、感覚でエントリーしていませんか？",
                "sub": ["クラウドストライクの決算直後", "感覚でエントリーしていませんか？"],
            },
            {
                "tts": "ファルコンARR急増による、決算後株価ドリフトPEAD現象を検知！",
                "sub": ["Falcon ARR急増による", "決算後株価ドリフトPEADを検知！"],
            },
            {
                "tts": "ギャップアップ後は慌てず、2.0倍ATRラインを支持線に確認！",
                "sub": ["ギャップアップ後は慌てず", "2.0倍ATRラインを支持線に確認！"],
            },
            {
                "tts": "2.5R利確ターゲット404ドル、リスクリワード良好のシグナル点灯です。",
                "sub": ["2.5R利確ターゲット404ドル", "好リワードのシグナル点灯です"],
            },
            {
                "tts": "米サイバーセキュリティ株のAI解析、ゲットブレイクAIドットコムへ！",
                "sub": ["米セキュリティ株のAI解析", "▶ getbreakai.com"],
                "is_ending": True,
            },
        ],
    },
    {
        "id": "EP17_VRT_Liquid_Cooling_RSI",
        "ticker": "VRT",
        "jp_name": "バーティブ",
        "yt_title": "【バーティブ急騰】AIデータセンター液冷独占！ワイダーRSI強気ブレイクの真実 #米国株 #新NISA #VRT #Shorts",
        "ig_caption": "バーティブ($VRT)を知らずにAI相場を見ていませんか？❄️🔥\nブラックウェル発熱問題で不可欠な液冷システム独占企業！\nワイダーRSI 66強気ブレイクと2.0倍ATRラインを今すぐ確認！\n👉 https://getbreakai.com\n#バーティブ #VRT #AIデータセンター #米国株 #新NISA #株クラ",
        "clip_indices": [18, 19, 26, 27],
        "cuts": [
            {
                "tts": "AIデータセンターの隠れた主役、バーティブをご存知ですか？",
                "sub": ["AIデータセンターの隠れた主役", "バーティブをご存知ですか？"],
            },
            {
                "tts": "GPU冷却需要爆発で、大口機関買いの点火シグナルを検知！",
                "sub": ["GPU冷却需要爆発で", "大口機関買いの点火シグナルを検知！"],
            },
            {
                "tts": "ワイダーRSIが強気の66を突破、勢いあるモメンタム拡大中です。",
                "sub": ["ワイダーRSIが強気66突破", "勢いあるモメンタム拡大中です"],
            },
            {
                "tts": "適正損切り107ドル、2.5R利確ターゲット136ドルを設定！",
                "sub": ["適正損切り107ドル", "2.5R目標136ドルを設定！"],
            },
            {
                "tts": "AI本命銘柄のクオンツデータは、ゲットブレイクAIドットコムへ！",
                "sub": ["AI本命銘柄のクオンツデータ", "▶ getbreakai.com"],
                "is_ending": True,
            },
        ],
    },
    {
        "id": "EP18_CEG_Nuclear_PPA_Breakout",
        "ticker": "CEG",
        "jp_name": "コンステレーション",
        "yt_title": "【マイクロソフト原発契約】コンステレーション・エナジーの急騰に飛び乗る前のATR防衛術 #米国株 #新NISA #CEG #Shorts",
        "ig_caption": "コンステレーション($CEG)の原子力PPA契約急騰、どう立ち回る？⚡⚛️\n巨大テックのクリーン電力争奪戦と2.0倍ATR損切りラインをAIが完全分析！\n👉 https://getbreakai.com で適正株数を無料診断！\n#コンステレーション #CEG #原子力 #米国株 #新NISA #クリーンエネルギー #株クラ",
        "clip_indices": [28, 29, 8, 9],
        "cuts": [
            {
                "tts": "マイクロソフトの原発再稼働ニュースで、高値掴みしていませんか？",
                "sub": ["マイクロソフトの原発契約で", "高値掴みしていませんか？"],
            },
            {
                "tts": "コンステレーションの長期PPA契約で、機関投資家の実需買いが殺到！",
                "sub": ["CEGの長期PPA契約で", "機関投資家の実需買いが殺到！"],
            },
            {
                "tts": "急騰株こそボラティリティに合わせた、ATR損切り幅の確保が命です。",
                "sub": ["急騰株こそボラティリティ連動", "ATR損切り幅の確保が命です"],
            },
            {
                "tts": "2.0倍ATR損切り250ドル、利確目標312ドルでリスク限定！",
                "sub": ["2.0倍ATR損切り250ドル", "利確目標312ドルでリスク限定！"],
            },
            {
                "tts": "米エネルギー株の適正株数計算は、ゲットブレイクAIドットコムへ！",
                "sub": ["米電力株の適正株数計算は", "▶ getbreakai.com"],
                "is_ending": True,
            },
        ],
    },
    {
        "id": "EP19_MSTR_BTC_Convertible_ATR",
        "ticker": "MSTR",
        "jp_name": "マイクロストラテジー",
        "yt_title": "【MSTR超ボラ相場】ビットコイン爆買い銘柄で生き残るクオンツ資金管理の鉄則 #MSTR #ビットコイン #米国株 #Shorts",
        "ig_caption": "マイクロストラテジー($MSTR)の荒波で資金を溶かしていませんか？🪙⚡\n転換社債によるBTC追加購入と超ボラティリティ相場を2.0倍ATRで鉄壁防御！\n👉 https://getbreakai.com で今すぐリスク計算！\n#マイクロストラテジー #MSTR #ビットコイン #仮想通貨 #米国株 #新NISA #株クラ",
        "clip_indices": [10, 11, 30, 31],
        "cuts": [
            {
                "tts": "マイクロストラテジーのジェットコースター相場に、翻弄されていませんか？",
                "sub": ["MSTRの激しい乱高下に", "翻弄されていませんか？"],
            },
            {
                "tts": "ビットコイン買い増し転換社債発行で、出来高とボラティリティが急拡大！",
                "sub": ["BTC買い増し転換社債で", "出来高と変動幅が急拡大！"],
            },
            {
                "tts": "超高ボラ銘柄は口座リスク1パーセント厳守、株数を抑えるのが絶対鉄則！",
                "sub": ["超高ボラ銘柄は口座リスク1%厳守", "株数を抑えるのが絶対鉄則！"],
            },
            {
                "tts": "適正損切りはATR幅208ドル、利確目標は2.5Rの338ドル圏！",
                "sub": ["適正損切りはATR幅208ドル", "利確目標は2.5Rの338ドル圏！"],
            },
            {
                "tts": "超高ボラ銘柄の適正株数シミュレーターは、ゲットブレイクAIドットコムへ！",
                "sub": ["超高ボラ銘柄の適正株数計算", "▶ getbreakai.com"],
                "is_ending": True,
            },
        ],
    },
    {
        "id": "EP20_ASML_HighNA_EUV_Monopoly",
        "ticker": "ASML",
        "jp_name": "ASML",
        "yt_title": "【ASML独占】次世代2ナノ半導体の心臓部！高NA EUV露光装置の押し目を狙え #半導体株 #ASML #米国株 #新NISA #Shorts",
        "ig_caption": "半導体製造の絶対王者ASML($ASML)を単なるニュースで売買していませんか？🔬⚙️\nHigh-NA EUV独占納入と大口買い集積シグナルをAIが数値化！\n👉 https://getbreakai.com で2.0倍ATR損切りラインを確認！\n#ASML #半導体株 #露光装置 #米国株 #新NISA #資産運用 #株クラ",
        "clip_indices": [32, 33, 20, 21],
        "cuts": [
            {
                "tts": "半導体の絶対王者ASMLを、悲観ニュースの底で投げていませんか？",
                "sub": ["半導体の絶対王者ASMLを", "悲観ニュースの底で投げていませんか？"],
            },
            {
                "tts": "次世代2ナノ向け高NA露光装置の独占納入で、大口買い集積を検知！",
                "sub": ["次世代高NA露光装置独占で", "大口買い集積シグナルを検知！"],
            },
            {
                "tts": "プロは感情に惑わされず、14日ATRから算出された損切りを厳守！",
                "sub": ["プロは感情に惑わされず", "14日ATR損切りラインを厳守！"],
            },
            {
                "tts": "適正損切り680ドル、目標株価は2.5Rの839ドル圏へ到達見込み！",
                "sub": ["適正損切り680ドル", "目標株価2.5Rの839ドル圏へ！"],
            },
            {
                "tts": "世界最強半導体株のAI分析、ゲットブレイクAIドットコムへ！",
                "sub": ["最強半導体株のAI分析", "▶ getbreakai.com"],
                "is_ending": True,
            },
        ],
    },
    {
        "id": "EP21_SMCI_10K_Risk_Avoid_Trap",
        "ticker": "SMCI",
        "jp_name": "スーパー・マイクロ",
        "yt_title": "【SMCI大暴落の罠】機関投資家67％逃避！会計リスク株に手を出してはいけない理由 #米国株 #SMCI #株価暴落 #Shorts",
        "ig_caption": "スーパー・マイクロ($SMCI)の急落を「割安」だと思って買っていませんか？⚠️🚨\n10-K会計監査リスクと機関投資家の67%脱出をAIが危険警告！\n罠銘柄を回避し、勝率の高い銘柄だけを厳選する方法！\n👉 https://getbreakai.com\n#スーパーマイクロ #SMCI #米国株 #暴落 #新NISA #リスク管理 #株クラ",
        "clip_indices": [43, 44, 38, 39],
        "cuts": [
            {
                "tts": "スーパー・マイクロの暴落を、割安のチャンスだと勘違いしていませんか？",
                "sub": ["SMCIの暴落を割安だと", "勘違いしていませんか？"],
            },
            {
                "tts": "10-K会計監査問題で、大口機関投資家の67パーセントが脱出！",
                "sub": ["10-K会計監査問題で", "大口機関の67%が脱出！"],
            },
            {
                "tts": "AIスコアは危険水準の28点！落ちるナイフを掴んではいけません。",
                "sub": ["AIスコアは危険水準の28点！", "落ちるナイフを掴んではいけません"],
            },
            {
                "tts": "クオンツの極意は、負ける罠銘柄を最初から完全排除することです！",
                "sub": ["クオンツ投資の極意は", "罠銘柄を完全排除することです！"],
            },
            {
                "tts": "危険銘柄判定と安全な買い銘柄は、ゲットブレイクAIドットコムへ！",
                "sub": ["危険銘柄アラートは", "▶ getbreakai.com"],
                "is_ending": True,
            },
        ],
    },
    {
        "id": "EP22_6758_Sony_CMOS_Entertainment",
        "ticker": "6758.T",
        "jp_name": "ソニーグループ",
        "yt_title": "【ソニーグループ】CMOS世界首位＆コンテンツ増益！東証大口資金の集積シグナル #日本株 #ソニー #新NISA #東証プライム #Shorts",
        "ig_caption": "ソニーグループ(6758.T)を感覚で売買していませんか？🎮📷\nCMOSイメージセンサ世界シェア53%とエンタメ好調による大口買い集積をAIが検知！\n東証主力株の2.0倍ATR損切りラインを3秒チェック！\n👉 https://getbreakai.com/jp/\n#ソニー #6758 #日本株 #新NISA #東証プライム #半導体 #株クラ",
        "clip_indices": [34, 35, 36, 37],
        "cuts": [
            {
                "tts": "ソニーグループを、値ごろ感だけでなんとなく買っていませんか？",
                "sub": ["ソニーグループを値ごろ感だけで", "なんとなく買っていませんか？"],
            },
            {
                "tts": "CMOSセンサー世界首位と、ゲーム増益で大口の買い集積を検知！",
                "sub": ["CMOSセンサー世界首位と", "ゲーム増益で大口集積を検知！"],
            },
            {
                "tts": "東証プライム銘柄も、14日ATRを用いた客観的損切りが不可欠！",
                "sub": ["東証プライム銘柄も", "14日ATR客観損切りが不可欠！"],
            },
            {
                "tts": "適正損切り2836円、2.5R利確目標3340円でリスク管理万全！",
                "sub": ["適正損切り2836円", "2.5R目標3340円でリスク管理！"],
            },
            {
                "tts": "東証主力株の日本語AIレポートは、ゲットブレイクAIドットコムへ！",
                "sub": ["東証主力株の日本語AI分析", "▶ getbreakai.com"],
                "is_ending": True,
            },
        ],
    },
    {
        "id": "EP23_SOXL_vs_SMH_Leverage_Trap",
        "ticker": "SOXL",
        "jp_name": "3倍レバ半導体×ATR",
        "yt_title": "【SOXLの罠】3倍レバレッジの恐ろしい減価！資産を溶かさない適正配分ルール #SOXL #SMH #米国株 #新NISA #Shorts",
        "ig_caption": "半導体3倍レバレッジ($SOXL)で資産を大きく減らしていませんか？📉💥\n横ばい相場でのボラティリティ減価の罠と、1倍ETF($SMH)を組み合わせた適正リスク管理をAIが提示！\n👉 https://getbreakai.com\n#SOXL #SMH #半導体株 #レバレッジ #米国株 #新NISA #資産運用 #株クラ",
        "clip_indices": [40, 41, 42, 1],
        "cuts": [
            {
                "tts": "SOXLの3倍レバレッジで、一攫千金を夢見ていませんか？",
                "sub": ["SOXLの3倍レバレッジで", "一攫千金を夢見ていませんか？"],
            },
            {
                "tts": "レンジ相場が続くと、複利効果の逆回転で資産が急速に目減りします！",
                "sub": ["レンジ相場が続くと", "複利の逆回転で資産が激減！"],
            },
            {
                "tts": "レバ株は口座資金の3パーセント以下、現物SMHとの併用が正解！",
                "sub": ["レバ株は口座資金の3%以下", "現物SMHとの併用が正解！"],
            },
            {
                "tts": "2.0倍ATR幅から逆算した株数制御が、暴落から命を守ります。",
                "sub": ["2.0倍ATR幅から逆算した", "株数制御が暴落から命を守る！"],
            },
            {
                "tts": "レバレッジ株の適正株数計算は、ゲットブレイクAIドットコムへ！",
                "sub": ["レバレッジ適正株数の計算は", "▶ getbreakai.com"],
                "is_ending": True,
            },
        ],
    },
    {
        "id": "EP24_MACRO_CPI_FOMC_Gamma_Defense",
        "ticker": "MACRO",
        "jp_name": "CPI・FOMC発表直前",
        "yt_title": "【CPI・FOMC直前】経済指標の直前にやってはいけないギャンブル買い！IVクラッシュ防衛術 #米国株 #経済指標 #FOMC #新NISA #Shorts",
        "ig_caption": "今夜のCPIやFOMC発表直前に、丁半博打で株やオプションを買っていませんか？🎲⚠️\n発表直後のボラティリティ急落(IVクラッシュ)とガンマサポートの防衛ラインをAIが分析！\n指標発表を安全に乗り越えるクオンツ戦略！\n👉 https://getbreakai.com\n#CPI #FOMC #米国株 #経済指標 #新NISA #オプション #株クラ",
        "clip_indices": [0, 1, 44, 15],
        "cuts": [
            {
                "tts": "CPIやFOMCの発表直前、ギャンブル買いをしていませんか？",
                "sub": ["CPIやFOMCの発表直前", "ギャンブル買いをしていませんか？"],
            },
            {
                "tts": "指標発表と同時にインプライドボラティリティが急落するIVクラッシュが発生！",
                "sub": ["発表と同時にIV急落！", "恐ろしいIVクラッシュが発生します"],
            },
            {
                "tts": "プロは発表前にポジションを縮小し、ガンマウォール支持線を待ち伏せます！",
                "sub": ["プロは発表前にポジション縮小", "ガンマ壁の支持線を待ち伏せます！"],
            },
            {
                "tts": "5日予想変動幅を把握し、発表後の初動ブレイクを数値で狙い撃ち！",
                "sub": ["5日予想変動幅を把握し", "発表後の初動を数値で狙い撃ち！"],
            },
            {
                "tts": "指標発表前のリスク管理ツールは、ゲットブレイクAIドットコムへ！",
                "sub": ["指標前のリスク管理ツールは", "▶ getbreakai.com"],
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
    print(f"[{ep_idx+1:02d}/{len(EPISODES)}] Mastered {ep_id}.mp4 ({final_dur:.2f}s, {size_kb} KB) | cut_durs={[round(d,2) for d in cut_durs]}")
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


def generate_manifest_and_kit(results_map):
    """
    Builds the 24-episode manifest and markdown copy-paste kit.
    Writes to:
    - STUDIO_DIR/mastered_24_shorts_manifest.json
    - MASTER_OUT_DIR/mastered_24_shorts_manifest.json
    - STUDIO_DIR/UPLOAD_COPY_PASTE_KIT_24EP.md
    - MASTER_OUT_DIR/UPLOAD_COPY_PASTE_KIT_24EP.md
    """
    manifest_list = []
    kit_lines = [
        "# 🎬 GetBreakAI 日本女性金融アナウンサー V3 マスターリング ショート・リール 24編 全編アップロードキット (EP01~EP24 Full Curriculum)",
        "",
        f"- **マスターリング保存先**: `{MASTER_OUT_DIR}`",
        "- **Clean Video V3 規格**: 1080×1920 (縦型 9:16 @ 30fps), 日本語アナウンサー自然音声(`ja-JP-NanamiNeural`, `rate=+4%`), 100%全文字完読(`seg_dur = max(2.30, tts_dur + 0.22)`), 0秒〜終了2.5秒前クリーンフルスクリーン, 下部セーフゾーン(`Y=1385~1460`) 太枠(`stroke_width=10`)字幕, ポイント効果音＆`-0.5 dBFS`リミッター(`alimiter=limit=0.944:level=disabled`), 2.5〜3.8秒 `getbreakai.com` ドメインコールアウト",
        "",
        "## 目次 (24エピソード一覧)",
    ]
    for idx, ep in enumerate(EPISODES):
        kit_lines.append(f"{idx+1:02d}. **{ep['id']}** ({ep['jp_name']} / `{ep['ticker']}`)")

    kit_lines.append("")
    kit_lines.append("---")
    kit_lines.append("")

    for idx, ep in enumerate(EPISODES):
        ep_id = ep["id"]
        res = results_map.get(ep_id)
        if not res:
            out_mp4 = os.path.join(MASTER_OUT_DIR, f"{ep_id}.mp4")
            dur = 25.0
            size_kb = 0
            if os.path.exists(out_mp4):
                try:
                    ffmpeg_bin = get_ffmpeg_bin()
                    dur = round(probe_duration(ffmpeg_bin, out_mp4), 2)
                    size_kb = os.path.getsize(out_mp4) // 1024
                except Exception:
                    pass
            res = {
                "id": ep_id,
                "ticker": ep["ticker"],
                "jp_name": ep["jp_name"],
                "yt_title": ep["yt_title"],
                "ig_caption": ep["ig_caption"],
                "mp4_path": out_mp4,
                "duration_sec": dur,
                "cut_durations_sec": [],
                "size_kb": size_kb,
            }
        manifest_list.append(res)

        dur_text = f"{res.get('duration_sec', 0.0):.2f}초"
        kit_lines.extend([
            f"## {idx+1:02d}. `{ep_id}.mp4` ({ep['jp_name']} / `{ep['ticker']}` · {dur_text})",
            f"- **파일 경로**: `{res.get('mp4_path', os.path.join(MASTER_OUT_DIR, ep_id + '.mp4'))}`",
            "- **유튜브 쇼츠 제목 (`@GetBreakAI`)**:",
            "  ```text",
            f"  {ep['yt_title']}",
            "  ```",
            "- **인스타그램 릴스 / 유튜브 설명란 (`@semifeargreed`)**:",
            "  ```text",
            f"  {ep['ig_caption']}",
            "  ```",
            "",
        ])

    # Save manifests
    manifest_paths = [
        os.path.join(STUDIO_DIR, "mastered_24_shorts_manifest.json"),
        os.path.join(MASTER_OUT_DIR, "mastered_24_shorts_manifest.json"),
    ]
    for p in manifest_paths:
        with open(p, "w", encoding="utf-8") as f:
            json.dump(manifest_list, f, ensure_ascii=False, indent=2)

    # Save kits
    kit_content = "\n".join(kit_lines)
    kit_paths = [
        os.path.join(STUDIO_DIR, "UPLOAD_COPY_PASTE_KIT_24EP.md"),
        os.path.join(MASTER_OUT_DIR, "UPLOAD_COPY_PASTE_KIT_24EP.md"),
    ]
    for p in kit_paths:
        with open(p, "w", encoding="utf-8") as f:
            f.write(kit_content)

    print(f"Manifest & Kit generated: {len(manifest_list)} episodes recorded.")


async def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--ep", type=int, default=0, help="If >0, build only that episode (1..24)")
    parser.add_argument("--start", type=int, default=1, help="Start episode index (1-based)")
    parser.add_argument("--end", type=int, default=24, help="End episode index (1-based)")
    parser.add_argument("--skip-existing", action="store_true", help="Skip if mp4 already exists")
    args = parser.parse_args()

    os.makedirs(MASTER_OUT_DIR, exist_ok=True)
    os.makedirs(TEMP_WORK_DIR, exist_ok=True)
    os.makedirs(OUTBOX_TODAY_DIR, exist_ok=True)

    ffmpeg_bin = get_ffmpeg_bin()
    ordered_clips = get_ordered_clip_paths()
    print(f"Loaded {len(ordered_clips)} Flow raw actress clips from {RAW_CLIPS_DIR}")

    # Load existing manifest if available
    results_map = {}
    old_manifest_12 = os.path.join(MASTER_OUT_DIR, "mastered_12_shorts_manifest.json")
    if os.path.exists(old_manifest_12):
        try:
            with open(old_manifest_12, "r", encoding="utf-8") as f:
                old_list = json.load(f)
                for item in old_list:
                    results_map[item["id"]] = item
        except Exception as e:
            print(f"Warning loading old manifest: {e}")

    old_manifest_24 = os.path.join(MASTER_OUT_DIR, "mastered_24_shorts_manifest.json")
    if os.path.exists(old_manifest_24):
        try:
            with open(old_manifest_24, "r", encoding="utf-8") as f:
                old_list = json.load(f)
                for item in old_list:
                    results_map[item["id"]] = item
        except Exception as e:
            pass

    if args.ep > 0:
        idx = args.ep - 1
        res = await build_episode(ffmpeg_bin, ordered_clips, idx, EPISODES[idx])
        results_map[res["id"]] = res
        generate_manifest_and_kit(results_map)
        print(f"Single Episode {args.ep} mastered -> {res['mp4_path']}")
        return

    start_idx = max(0, args.start - 1)
    end_idx = min(len(EPISODES), args.end)

    for idx in range(start_idx, end_idx):
        ep = EPISODES[idx]
        out_mp4 = os.path.join(MASTER_OUT_DIR, f"{ep['id']}.mp4")
        if args.skip_existing and os.path.exists(out_mp4) and os.path.getsize(out_mp4) > 1000000:
            print(f"[{idx+1:02d}/{len(EPISODES)}] Skipping already existing {ep['id']}.mp4")
            continue
        res = await build_episode(ffmpeg_bin, ordered_clips, idx, ep)
        results_map[res["id"]] = res

    generate_manifest_and_kit(results_map)

    shutil.rmtree(TEMP_WORK_DIR, ignore_errors=True)
    print(f"\nV3 JAPANESE SHORTS MASTERING COMPLETE -> {MASTER_OUT_DIR}")


if __name__ == "__main__":
    asyncio.run(main())
