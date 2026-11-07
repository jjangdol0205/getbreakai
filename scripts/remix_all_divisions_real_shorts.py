"""
Unified Real YouTube/Instagram Viral Shorts Remix Engine for 1사업부 (TOM) & 2사업부 (KFG)
-----------------------------------------------------------------------------------------
Instead of relying solely on Google Flow AI clips, this engine downloads real YouTube
Shorts footage via yt-dlp (e.g. CNBC/Nvidia semiconductor reactions for 1사업부,
real pediatric height/growth & kids vitamin reviews for 2사업부) and composites them
with a Split-Screen / Broadcast HUD + Live Data Card + 1-Click Bio Link CTA.
"""
import os
import sys
import math
import wave
import shutil
import asyncio
import subprocess
import numpy as np
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import edge_tts
import yt_dlp
import imageio_ffmpeg

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

FFMPEG_EXE = imageio_ffmpeg.get_ffmpeg_exe()
FPS = 30
SAMPLE_RATE = 48000
SAMPLES_PER_FRAME = SAMPLE_RATE // FPS

TOM_ROOT = Path("d:/투자홈페이지/1_RightSideAlpha_미국주식터미널")
KFG_ROOT = Path("d:/키즈핏 영문")
FONT_BOLD = Path("d:/사업아이템/src/fonts/Pretendard-Black.otf")
if not FONT_BOLD.exists():
    FONT_BOLD = Path("C:/Windows/Fonts/arialbd.ttf")

W_WHITE = (255, 255, 255, 255)
W_YELLOW = (255, 232, 0, 255)
W_MINT = (16, 185, 129, 255)
W_CYAN = (56, 189, 248, 255)
W_RED = (248, 113, 113, 255)


def run_ffmpeg(args):
    cmd = [FFMPEG_EXE, "-y"] + args
    res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, encoding="utf-8", errors="ignore")
    if res.returncode != 0:
        raise RuntimeError(f"FFmpeg error: {res.stderr[-600:]}")
    return res


def download_yt_clip(query: str, out_mp4: Path) -> Path:
    out_mp4.parent.mkdir(parents=True, exist_ok=True)
    if out_mp4.exists() and out_mp4.stat().st_size > 150_000:
        return out_mp4

    raw_tmpl = str(out_mp4.parent / f"{out_mp4.stem}_raw.%(ext)s")
    ydl_opts = {
        "format": "bestvideo[ext=mp4][height<=1920]+bestaudio[ext=m4a]/best[ext=mp4]/best",
        "outtmpl": raw_tmpl,
        "noplaylist": True,
        "quiet": True,
        "no_warnings": True,
        "ignoreerrors": True,
        "max_filesize": 35 * 1024 * 1024,
        "ffmpeg_location": FFMPEG_EXE,
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            info = ydl.extract_info(query, download=False)
        except Exception:
            info = None
        for entry in (info or {}).get("entries") or []:
            if not entry:
                continue
            dur = entry.get("duration") or 0
            if 5 <= dur <= 180:
                url = entry.get("webpage_url") or entry.get("url")
                print(f"  [yt-dlp] Downloading ({dur}s): {entry.get('title', '')} -> {url}", flush=True)
                try:
                    ydl.download([url])
                    raws = list(out_mp4.parent.glob(f"{out_mp4.stem}_raw.*"))
                    if raws:
                        break
                except Exception:
                    continue

    raws = list(out_mp4.parent.glob(f"{out_mp4.stem}_raw.*"))
    if raws:
        src = raws[0]
        run_ffmpeg([
            "-ss", "1.0", "-t", "14.0",
            "-i", str(src),
            "-vf", "scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,fps=30",
            "-c:v", "libx264", "-preset", "fast", "-crf", "20", "-an",
            str(out_mp4),
        ])
        try:
            src.unlink()
        except Exception:
            pass
    return out_mp4


def draw_centered_text(draw: ImageDraw.ImageDraw, y: int, text: str, font, fill, stroke_w: int = 10):
    bbox = draw.textbbox((0, 0), text, font=font)
    w = bbox[2] - bbox[0]
    x = (1080 - w) // 2
    draw.text((x, y), text, font=font, fill=fill, stroke_width=stroke_w, stroke_fill=(0, 0, 0, 255))


def render_division_hud_png(
    badge: str,
    hook_top: str,
    hook_bot: str,
    subtitle_l1: str,
    subtitle_l2: str,
    card_title: str,
    card_metric: str,
    cta_text: str,
    out_png: Path,
):
    W, H = 1080, 1920
    canvas = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    draw = ImageDraw.Draw(canvas)

    f_badge = ImageFont.truetype(str(FONT_BOLD), 34)
    f_hook = ImageFont.truetype(str(FONT_BOLD), 56)
    f_sub = ImageFont.truetype(str(FONT_BOLD), 64)
    f_card_t = ImageFont.truetype(str(FONT_BOLD), 36)
    f_card_m = ImageFont.truetype(str(FONT_BOLD), 42)
    f_cta = ImageFont.truetype(str(FONT_BOLD), 40)

    # Top Broadcast Header
    draw.rounded_rectangle([42, 92, 1038, 398], radius=32, fill=(10, 15, 28, 228), outline=(56, 189, 248, 235), width=4)
    draw.rounded_rectangle([76, 114, 1004, 174], radius=20, fill=(220, 38, 38, 240))
    draw_centered_text(draw, 124, badge, f_badge, W_WHITE, stroke_w=5)
    draw_centered_text(draw, 196, hook_top, f_hook, W_YELLOW, stroke_w=10)
    draw_centered_text(draw, 276, hook_bot, f_hook, W_WHITE, stroke_w=10)

    # Live Footage Tag
    draw.rounded_rectangle([680, 420, 1036, 478], radius=18, fill=(15, 23, 42, 230), outline=(255, 232, 0, 220), width=2)
    f_tag = ImageFont.truetype(str(FONT_BOLD), 28)
    draw.text((708, 434), "🎥 REAL FOOTAGE REMIX", font=f_tag, fill=W_YELLOW)

    # Center-Lower Subtitles
    draw_centered_text(draw, 1190, subtitle_l1, f_sub, W_WHITE, stroke_w=14)
    draw_centered_text(draw, 1275, subtitle_l2, f_sub, W_YELLOW, stroke_w=14)

    # Bottom Data / Terminal Card + CTA
    draw.rounded_rectangle([42, 1445, 1038, 1735], radius=30, fill=(9, 16, 32, 238), outline=(16, 185, 129, 235), width=4)
    draw_centered_text(draw, 1472, card_title, f_card_t, W_CYAN, stroke_w=6)
    draw_centered_text(draw, 1528, card_metric, f_card_m, W_WHITE, stroke_w=7)

    draw.rounded_rectangle([68, 1602, 1012, 1708], radius=24, fill=(5, 150, 105, 250), outline=(255, 232, 0, 255), width=3)
    draw_centered_text(draw, 1630, cta_text, f_cta, W_YELLOW, stroke_w=7)

    canvas.save(out_png)


async def build_english_remix_short(
    slug: str,
    yt_queries: list[str],
    badge: str,
    hook_top: str,
    hook_bot: str,
    card_title: str,
    card_metric: str,
    cta_text: str,
    beats: list[dict],
    out_dir: Path,
) -> Path:
    out_dir.mkdir(parents=True, exist_ok=True)
    work_dir = out_dir / f"_work_{slug}"
    work_dir.mkdir(parents=True, exist_ok=True)

    clips = []
    for idx, q in enumerate(yt_queries):
        c_path = work_dir / f"yt_{idx}.mp4"
        download_yt_clip(q, c_path)
        if c_path.exists():
            clips.append(c_path)

    beat_mp4s = []
    wav_files = []
    for b_idx, beat in enumerate(beats):
        mp3_p = work_dir / f"b{b_idx}.mp3"
        wav_p = work_dir / f"b{b_idx}.wav"
        comm = edge_tts.Communicate(text=beat["tts"], voice="en-US-AndrewMultilingualNeural", rate="+18%", pitch="+2Hz")
        await comm.save(str(mp3_p))
        run_ffmpeg(["-i", str(mp3_p), "-ac", "1", "-ar", str(SAMPLE_RATE), "-c:a", "pcm_s16le", str(wav_p)])
        with wave.open(str(wav_p), "rb") as w:
            n_samples = w.getnframes()
        nf = max(45, int(math.ceil(n_samples / SAMPLES_PER_FRAME)))
        dur = nf / FPS
        wav_files.append(wav_p)

        png_p = work_dir / f"b{b_idx}.png"
        render_division_hud_png(
            badge=badge,
            hook_top=hook_top,
            hook_bot=hook_bot,
            subtitle_l1=beat["l1"],
            subtitle_l2=beat["l2"],
            card_title=card_title,
            card_metric=card_metric,
            cta_text=cta_text,
            out_png=png_p,
        )

        src_clip = clips[b_idx % len(clips)]
        ss = 0.8 + (b_idx * 2.2)
        b_mp4 = work_dir / f"b{b_idx}_v.mp4"
        fc = (
            f"[0:v]trim=start={ss:.2f}:duration={dur:.2f},setpts=PTS-STARTPTS,"
            f"scale=1160:2062:force_original_aspect_ratio=increase,crop=1080:1920,fps={FPS},"
            f"eq=contrast=1.08:saturation=1.14[bg];"
            f"[bg][1:v]overlay=0:0:format=auto,format=yuv420p[outv]"
        )
        run_ffmpeg([
            "-i", str(src_clip),
            "-loop", "1", "-t", f"{dur + 0.3:.2f}", "-i", str(png_p),
            "-filter_complex", fc,
            "-map", "[outv]", "-frames:v", str(nf),
            "-c:v", "libx264", "-preset", "fast", "-crf", "19", "-r", str(FPS), "-an",
            str(b_mp4),
        ])
        beat_mp4s.append(b_mp4)

    concat_txt = work_dir / "concat.txt"
    concat_txt.write_text("\n".join(f"file '{p.as_posix()}'" for p in beat_mp4s), encoding="utf-8")
    merged_v = work_dir / "merged_v.mp4"
    run_ffmpeg(["-f", "concat", "-safe", "0", "-i", str(concat_txt), "-c:v", "libx264", "-preset", "fast", "-crf", "19", "-pix_fmt", "yuv420p", str(merged_v)])

    voice_wav = work_dir / "voice_all.wav"
    chunks = []
    for wp in wav_files:
        with wave.open(str(wp), "rb") as w:
            chunks.append(np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16))
    full_pcm = np.concatenate(chunks)
    with wave.open(str(voice_wav), "wb") as w_out:
        w_out.setnchannels(1)
        w_out.setsampwidth(2)
        w_out.setframerate(SAMPLE_RATE)
        w_out.writeframes(full_pcm.tobytes())

    final_mp4 = out_dir / f"{slug}.mp4"
    run_ffmpeg([
        "-i", str(merged_v),
        "-i", str(voice_wav),
        "-map", "0:v:0", "-map", "1:a:0",
        "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-shortest", "-movflags", "+faststart",
        str(final_mp4),
    ])
    print(f"  ✅ Built Division Remix Video: {final_mp4} ({final_mp4.stat().st_size // 1024} KB)", flush=True)
    return final_mp4


async def main():
    # 1사업부 (TOM - truthofmarket.com): Real NVDA / Semiconductor Market Clips + Quant Signal HUD
    await build_english_remix_short(
        slug="tom_real_remix_nvda_smh_signal",
        yt_queries=[
            "ytsearch5:Nvidia stock CNBC semiconductor rally shorts",
            "ytsearch5:SOXL SMH semiconductor ETF trading shorts",
        ],
        badge="🚨 LIVE US QUANT TERMINAL · $NVDA × $SMH",
        hook_top="WALL STREET CHASES HEADLINES...",
        hook_bot="WE TRACK 7-FACTOR SEMI REGIME",
        card_title="📊 LIVE TERMINAL: TRUTHOFMARKET.COM",
        card_metric="$SMH Fear & Greed + RightSideAlpha 6-Factor Score",
        cta_text="👆 Link in Bio: truthofmarket.com (Free Live Scan)",
        beats=[
            {
                "tts": "While retail traders panic on every Nvidia headline, institutional quant desks watch one thing.",
                "l1": "Retail Chases Headlines",
                "l2": "Quants Track Regime Flow",
            },
            {
                "tts": "Our Semi-Fear-and-Greed index combines SOX breadth, options skew, and dark pool momentum in real time.",
                "l1": "7-Factor Semiconductor",
                "l2": "Fear & Greed + Alpha Score",
            },
            {
                "tts": "Check the live semiconductor regime free right now at Truth Of Market dot com, link in bio!",
                "l1": "Check Live Regime Free:",
                "l2": "truthofmarket.com 👆",
            },
        ],
        out_dir=TOM_ROOT / "dist" / "samples" / "real_remix",
    )

    # 2사업부 (KFG - kisfitglobal.com): Real Pediatric Growth / Nutrition Clips + US CDC 2000 HUD
    await build_english_remix_short(
        slug="kfg_real_remix_cdc_height_tracker",
        yt_queries=[
            "ytsearch5:pediatrician kids height growth tips shorts",
            "ytsearch5:kids vitamin D3 K2 calcium gummies review shorts",
        ],
        badge="🩺 US CDC 2000 CLINICAL GROWTH AI",
        hook_top="IS YOUR CHILD HITTING THEIR",
        hook_bot="TRUE GENETIC HEIGHT POTENTIAL?",
        card_title="📌 LIVE REPORT: KISFITGLOBAL.COM",
        card_metric="Exact US CDC 2000 Percentile + 6-Month Height Forecast",
        cta_text="👆 Link in Bio: kisfitglobal.com (Free 60s Scan)",
        beats=[
            {
                "tts": "Most parents guess their child's height percentile until the annual pediatric visit.",
                "l1": "Stop Guessing Your Child's",
                "l2": "True Growth Percentile!",
            },
            {
                "tts": "KIDS-FIT Global runs the official US CDC 2000 LMS algorithm to map your child's exact growth curve and daily D3 and Calcium targets.",
                "l1": "Official US CDC 2000 Curve",
                "l2": "+ Exact D3 & Calcium Dose",
            },
            {
                "tts": "Run your free sixty-second clinical growth scan right now at Kis Fit Global dot com, link in bio!",
                "l1": "Free 60-Second Scan:",
                "l2": "kisfitglobal.com 👆",
            },
        ],
        out_dir=KFG_ROOT / "dist-global" / "samples" / "real_remix",
    )


if __name__ == "__main__":
    asyncio.run(main())
