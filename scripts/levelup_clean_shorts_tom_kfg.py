"""
Clean Level-Up Mastering for 1사업부 (TOM) & 2사업부 (KFG) Existing Viral Shorts
--------------------------------------------------------------------------------
- Removes the old overlapping yellow box that covered the Y=1420 subtitle on _IG_Reels / _YT_Shorts
- Keeps Cuts 1~3 100% clean (full-screen 4K/3D video + single active subtitle ONLY)
- Places a sleek, non-overlapping domain CTA pill ONLY in the final 2.8 seconds!
- Also fixes the old `[] getbreakai.com` header on 1사업부 Shot 4 to `truthofmarket.com`.
"""
import os
import sys
import shutil
import subprocess
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import imageio_ffmpeg

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

FFMPEG_EXE = imageio_ffmpeg.get_ffmpeg_exe()
FONT_BOLD = Path("d:/사업아이템/src/fonts/Pretendard-Black.otf")
if not FONT_BOLD.exists():
    FONT_BOLD = Path("C:/Windows/Fonts/arialbd.ttf")

TOM_DIR = Path("d:/투자홈페이지/1_RightSideAlpha_미국주식터미널/viral_shorts_10_output")
KFG_DIR = Path("d:/키즈핏 영문/flow_shorts_studio/ai_shorts_output")
WORK_DIR = Path("d:/투자홈페이지/1_RightSideAlpha_미국주식터미널/data/_clean_levelup_work")
WORK_DIR.mkdir(parents=True, exist_ok=True)


def get_duration(mp4_path: Path) -> float:
    res = subprocess.run(
        [FFMPEG_EXE, "-i", str(mp4_path)],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        encoding="utf-8",
        errors="ignore",
    )
    import re
    m = re.search(r"Duration:\s*(\d+):(\d+):(\d+\.\d+)", res.stderr)
    if not m:
        return 22.0
    return int(m.group(1)) * 3600 + int(m.group(2)) * 60 + float(m.group(3))


def make_tom_ending_png(out_png: Path):
    W, H = 1080, 1920
    canvas = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    draw = ImageDraw.Draw(canvas)

    # Cleanly replace the old `[] getbreakai.com` pill at Y=82..252 on Shot 4 live UI
    draw.rounded_rectangle([72, 82, 1008, 252], radius=28, fill=(11, 20, 34, 255), outline=(16, 185, 129, 240), width=3)
    f_top = ImageFont.truetype(str(FONT_BOLD), 42)
    f_sub = ImageFont.truetype(str(FONT_BOLD), 28)

    t1 = "truthofmarket.com  |  LIVE QUANT TERMINAL"
    b1 = draw.textbbox((0, 0), t1, font=f_top)
    draw.text(((W - (b1[2] - b1[0])) // 2, 108), t1, font=f_top, fill=(255, 255, 255, 255))

    t2 = "100% Free Live Semiconductor Regime & 72-Stock Scanner"
    b2 = draw.textbbox((0, 0), t2, font=f_sub)
    draw.text(((W - (b2[2] - b2[0])) // 2, 178), t2, font=f_sub, fill=(94, 255, 208, 255))

    # Sleek minimal bottom pill BELOW the Y=1420 subtitle (at Y=1575..1660, zero overlap!)
    pill = "Link in Bio · truthofmarket.com"
    f_pill = ImageFont.truetype(str(FONT_BOLD), 38)
    bp = draw.textbbox((0, 0), pill, font=f_pill)
    pw = bp[2] - bp[0]
    px1, px2 = (W - pw) // 2 - 46, (W + pw) // 2 + 46
    draw.rounded_rectangle([px1, 1575, px2, 1660], radius=42, fill=(10, 16, 28, 225), outline=(255, 232, 0, 235), width=3)
    draw.text(((W - pw) // 2, 1596), pill, font=f_pill, fill=(255, 232, 0, 255))

    canvas.save(out_png)


def make_kfg_ending_png(out_png: Path):
    W, H = 1080, 1920
    canvas = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    draw = ImageDraw.Draw(canvas)

    # Sleek minimal bottom pill BELOW the Y=1420 subtitle (at Y=1575..1660, zero overlap!)
    pill = "Link in Bio · kisfitglobal.com (Free 30s Scan)"
    f_pill = ImageFont.truetype(str(FONT_BOLD), 36)
    bp = draw.textbbox((0, 0), pill, font=f_pill)
    pw = bp[2] - bp[0]
    px1, px2 = (W - pw) // 2 - 44, (W + pw) // 2 + 44
    draw.rounded_rectangle([px1, 1575, px2, 1660], radius=42, fill=(10, 16, 28, 225), outline=(0, 245, 212, 235), width=3)
    draw.text(((W - pw) // 2, 1597), pill, font=f_pill, fill=(0, 245, 212, 255))

    canvas.save(out_png)


def process_division_video(base_mp4: Path, overlay_png: Path, tail_sec: float):
    dur = get_duration(base_mp4)
    start_t = max(0.0, dur - tail_sec)
    tmp_out = WORK_DIR / f"{base_mp4.stem}_clean.mp4"

    fc = f"[0:v][1:v]overlay=0:0:enable='gte(t,{start_t:.2f})':format=auto,format=yuv420p[outv]"
    cmd = [
        FFMPEG_EXE, "-y",
        "-i", str(base_mp4),
        "-loop", "1", "-t", f"{dur + 0.5:.2f}", "-i", str(overlay_png),
        "-filter_complex", fc,
        "-map", "[outv]", "-map", "0:a:0",
        "-c:v", "libx264", "-preset", "fast", "-crf", "19",
        "-c:a", "copy",
        "-movflags", "+faststart",
        str(tmp_out),
    ]
    res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, encoding="utf-8", errors="ignore")
    if res.returncode != 0:
        raise RuntimeError(f"FFmpeg failed on {base_mp4.name}: {res.stderr[-500:]}")

    ig_out = base_mp4.parent / f"{base_mp4.stem}_IG_Reels.mp4"
    yt_out = base_mp4.parent / f"{base_mp4.stem}_YT_Shorts.mp4"
    shutil.copy2(tmp_out, base_mp4)
    shutil.copy2(tmp_out, ig_out)
    shutil.copy2(tmp_out, yt_out)
    print(f"  ✅ Leveled Up Clean Video: {base_mp4.name} + IG_Reels + YT_Shorts ({dur:.1f}s)", flush=True)


def main():
    tom_png = WORK_DIR / "tom_end.png"
    kfg_png = WORK_DIR / "kfg_end.png"
    make_tom_ending_png(tom_png)
    make_kfg_ending_png(kfg_png)

    print("=== 1사업부 (TOM - truthofmarket.com) Clean Level-Up ===", flush=True)
    for i in range(8, 11):
        p = TOM_DIR / f"EP{i:02d}_US_Viral_Shorts.mp4"
        if p.exists():
            try:
                process_division_video(p, tom_png, tail_sec=3.8)
            except Exception as e:
                print(f"  [skip {p.name}]: {e}", flush=True)

    print("\n=== 2사업부 (KFG - kisfitglobal.com) Clean Level-Up ===", flush=True)
    for p in sorted(KFG_DIR.glob("US_KISFIT_*_1A_Punchline.mp4")):
        if "_IG_Reels" in p.name or "_YT_Shorts" in p.name:
            continue
        try:
            process_division_video(p, kfg_png, tail_sec=2.8)
        except Exception as e:
            print(f"  [skip {p.name}]: {e}", flush=True)


if __name__ == "__main__":
    main()
