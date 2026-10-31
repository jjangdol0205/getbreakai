#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
build_10_us_viral_shorts.py — 10-Episode US Viral Shorts & Reels Auto-Merger & Subtitle Mastering Engine
========================================================================================================
When the user generates clips in Google Flow (https://labs.google/fx/tools/flow) and downloads them:
- Automatically finds downloaded clips in `flow_clips/` or `~/Downloads`
- Pairs them with our 100% native American voiceover (`en-US-AndrewMultilingualNeural`),
  WordBoundary 0.01s Active-Word Kinetic Captions, Studio SFX/Sub-Bass Boom, and Live Terminal UI (`getbreakai.com`).
- Supports BOTH:
  * 1 Flow clip per episode (`ep01.mp4` .. `ep10.mp4`) + Auto Live UI Cut
  * 3 Flow clips per episode (`ep01_shot1.mp4` .. `ep01_shot3.mp4`) + Auto Live UI Cut
"""
import argparse
import pathlib
import sys
from typing import Dict, List, Any

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

WORKSPACE_DIR = pathlib.Path(__file__).resolve().parent
STUDIO_DIR = sorted(WORKSPACE_DIR.parent.glob("3_*"))[0]
if str(STUDIO_DIR) not in sys.path:
    sys.path.insert(0, str(STUDIO_DIR))

FLOW_CLIPS_DIR = STUDIO_DIR / "ai_shorts_output" / "flow_clips"
OUTPUT_DIR = WORKSPACE_DIR / "viral_shorts_10_output"
FLOW_CLIPS_DIR.mkdir(parents=True, exist_ok=True)
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

EPISODES: List[Dict[str, Any]] = [
    {
        "id": "ep01",
        "num": 1,
        "title": "Why Buying the -50% Dip Destroys Retail Accounts (Right-Side Rule)",
        "accent": (16, 185, 129, 255),
        "ui_type": "rsa",
        "master_prompt": (
            "Vertical 9:16 cinematic 4k photorealistic video. A stressed 32-year-old American male retail trader "
            "sitting in a dark modern bedroom at 2 AM staring at a glowing red crashing stock chart on his phone, "
            "then camera smoothly pans to an ultrawide desk monitor where a flat stock chart suddenly ignites upward "
            "with glowing emerald green volume bars crossing a golden 60-day moving average line. Moody Fincher-style "
            "dark teal and crimson lighting, shallow depth of field."
        ),
        "shot_prompts": [
            "Vertical 9:16 cinematic close-up shot, 4k photorealistic. A stressed 32-year-old American male retail investor sitting on the edge of his bed at 2 AM in a dark bedroom. Red glowing light from his smartphone screen illuminates his tired eyes and face. Subtle handheld camera movement, moody Fincher-style dark teal and crimson lighting, shallow depth of field.",
            "Vertical 9:16 cinematic over-the-shoulder shot, 4k photorealistic. A retail trader at a dimly lit desk staring at a glowing red falling stock chart on a monitor, rubbing his forehead in frustration as red candlesticks cascade downward. Dramatic dark lighting, realistic reflections on glass, slow push-in camera motion.",
            "Vertical 9:16 cinematic medium shot, 4k photorealistic. A calm, disciplined quantitative trader in a sleek dark modern home office. On his ultrawide monitor, a stock chart forms a flat bottom base and suddenly breaks upward with glowing emerald green volume bars crossing moving average lines. Crisp lighting, confident atmosphere, smooth slow pan.",
        ],
        "shot_scripts": [
            "You bought a stock down fifty percent thinking it was cheap, and somehow it dropped another forty percent.",
            "Catching falling knives on the left side of a crash is how retail traders trap their capital for years.",
            "Wall Street quants never buy the crash. They wait for the Right-Side Ignition, when seller washout ends and price reclaims the sixty-day moving average.",
            "Comment ALPHA below or check getbreakai dot com to scan seventy-two US stocks for live Right-Side breakouts right now.",
        ],
    },
    {
        "id": "ep02",
        "num": 2,
        "title": "Bagholding a Losing Stock? The -9% Hard Stop Rule That Saves Fortunes",
        "accent": (239, 68, 68, 255),
        "ui_type": "rsa",
        "master_prompt": (
            "Vertical 9:16 cinematic 4k photorealistic shot. A frustrated American trader in a dark high-rise apartment "
            "watching a red portfolio screen drop deeper into loss, followed by a sleek futuristic institutional terminal "
            "slicing a glowing laser-red stop-loss line at minus nine percent before the chart collapses. High contrast "
            "cyberpunk financial thriller lighting, ultra-detailed reflections."
        ),
        "shot_prompts": [
            "Vertical 9:16 cinematic close-up, 4k photorealistic. An anxious American trader biting his lip while looking at a bright red stock portfolio screen showing a heavy drawdown in a dark room. Dramatic crimson rim lighting, shallow depth of field.",
            "Vertical 9:16 cinematic macro shot, 4k photorealistic. A glowing digital stock chart on a dark glass monitor where a horizontal laser-red line labeled STOP LOSS slices cleanly across a falling candlestick before a massive cliff drop. Crisp macro lens detail.",
            "Vertical 9:16 cinematic medium shot, 4k photorealistic. A confident Wall Street quant analyst in a tailored dark jacket reviewing a clean risk-management dashboard with green profit targets in a sleek Manhattan office at night.",
        ],
        "shot_scripts": [
            "Every massive fifty percent portfolio wipeout starts as a small dip that you refused to sell.",
            "Institutional quants survive every bear market using one ruthless rule: an automatic minus nine percent hard stop loss.",
            "If a breakout fails and drops nine percent below your entry, the thesis is broken and you cut it immediately with zero emotion.",
            "Stuck bagholding right now? Comment ALPHA and run your ticker through our free Position Doctor at getbreakai dot com in three seconds.",
        ],
    },
    {
        "id": "ep03",
        "num": 3,
        "title": "The 55-Day Dead Money Rule Wall Street Quants Live By",
        "accent": (56, 189, 248, 255),
        "ui_type": "rsa",
        "master_prompt": (
            "Vertical 9:16 cinematic 4k photorealistic shot. A luxury mechanical chronograph watch ticking in extreme macro "
            "in front of a flat sideways stock chart on a dark trading terminal, then transitioning to a rocket-like emerald "
            "green breakout chart accelerating vertically. Dark moody institutional aesthetic, razor-sharp focus."
        ),
        "shot_prompts": [
            "Vertical 9:16 cinematic macro shot, 4k photorealistic. A luxury steel chronograph watch ticking in slow motion on a dark mahogany trading desk, with a flat sideways stock chart reflected softly on the watch crystal.",
            "Vertical 9:16 cinematic shot, 4k photorealistic. A bored trader leaning back in his chair staring at a stock chart moving completely sideways in a narrow gray channel while other tickers flash bright green on a side monitor.",
            "Vertical 9:16 cinematic medium shot, 4k photorealistic. A decisive quant trader pressing a glowing key to rotate capital into a surging emerald-green breakout chart on a dual-monitor setup.",
        ],
        "shot_scripts": [
            "The biggest hidden killer of your trading account is not a crash. It is dead money.",
            "When you hold a stock that goes sideways for six months, you miss every real institutional breakout in the market.",
            "Our twenty-six year quant engine enforces a strict fifty-five day time stop: if a stock fails to gain eight percent in fifty-five days, we rotate out immediately.",
            "Comment ALPHA below to get our live Telegram bot and test your portfolio with Position Doctor at getbreakai dot com.",
        ],
    },
    {
        "id": "ep04",
        "num": 4,
        "title": "Semiconductor Fear & Greed Just Hit 18 (Extreme Fear) — The 80/20 Secret",
        "accent": (245, 158, 11, 255),
        "ui_type": "semi",
        "master_prompt": (
            "Vertical 9:16 cinematic 4k photorealistic shot. A dramatic speedometer-style financial Fear and Greed gauge dial "
            "on a dark glass screen swinging sharply into glowing crimson Extreme Fear at number 18 with subtle sparks, "
            "while a calm institutional trader in a modern study rebalances a glowing gold and emerald portfolio chart. "
            "Ultra-detailed, dramatic dark lighting."
        ),
        "shot_prompts": [
            "Vertical 9:16 cinematic shot, 4k photorealistic. A nervous American retail investor in a dimly lit kitchen early in the morning, holding a coffee mug and staring at breaking semiconductor sell-off headlines on his phone with red glowing reflections.",
            "Vertical 9:16 cinematic macro shot, 4k photorealistic. A dramatic speedometer-style financial Fear and Greed gauge dial on a dark glass screen swinging sharply to the left into glowing crimson Extreme Fear at number 18, subtle sparks and moody reflections.",
            "Vertical 9:16 cinematic shot, 4k photorealistic. A confident portfolio manager in a modern minimalist study reviewing a clean dual-line portfolio chart where a steady emerald line climbs smoothly above a volatile red line over ten years.",
        ],
        "shot_scripts": [
            "Every time semiconductor stocks drop twenty percent, retail traders panic and sell at the exact bottom.",
            "Right now, our seven-factor Semiconductor Fear and Greed Index plunged to eighteen, Extreme Fear, while ninety percent of traders are frozen.",
            "Pairing SMH semiconductors with Healthcare XLV and shifting to an eighty-twenty barbell in Extreme Fear delivered a twenty-three percent annual return over twenty-six years.",
            "Comment ALPHA below to get real-time Semiconductor Fear and Greed alerts on our free Telegram bot and live terminal.",
        ],
    },
    {
        "id": "ep05",
        "num": 5,
        "title": "$CELH Crashed 71% — Dead Cat Bounce or Institutional Ignition?",
        "accent": (16, 185, 129, 255),
        "ui_type": "rsa",
        "master_prompt": (
            "Vertical 9:16 cinematic 4k photorealistic video. A sleek dark institutional trading desk showing a deep "
            "seventy-one percent stock crash curve that flattens out and suddenly fires a massive emerald-green volume "
            "breakout candle above a glowing moving average line. Cinematic slow push-in, crisp dark glass reflections."
        ),
        "shot_prompts": [
            "Vertical 9:16 cinematic shot, 4k photorealistic. A dramatic 3D financial chart on a dark glass monitor showing a steep seventy percent waterfall decline in red candlesticks, camera slowly panning down to the bottom.",
            "Vertical 9:16 cinematic macro shot, 4k photorealistic. At the bottom of a dark stock chart, tall glowing emerald-green volume bars suddenly spike nearly two times higher than normal as price crosses a golden moving average line.",
            "Vertical 9:16 cinematic medium shot, 4k photorealistic. A focused institutional analyst pointing at four green checkmarks on a dark quantitative screening terminal in a modern glass office.",
        ],
        "shot_scripts": [
            "When a growth stock like Celsius crashes seventy-one percent from its high, how do you know if the bounce is real or a bull trap?",
            "You stop guessing and check four mathematical conditions: deep drawdown washout, distance off the fifty-two week low, sixty-day trend reclamation, and volume surge.",
            "When all four align with a one point nine five times volume surge, our engine flags an institutional Right-Side Ignition.",
            "Comment ALPHA below to unlock the live seventy-two stock scanner and full institutional research briefs at getbreakai dot com.",
        ],
    },
    {
        "id": "ep06",
        "num": 6,
        "title": "Why $TSLA & $NVDA Traders Get Shaken Out Right Before the Breakout",
        "accent": (56, 189, 248, 255),
        "ui_type": "rsa",
        "master_prompt": (
            "Vertical 9:16 cinematic 4k photorealistic shot. A high-tension Wall Street trading floor monitor showing "
            "volatile red and green candlesticks whipping violently just below a glowing blue horizontal trigger line, "
            "then decisively smashing through the trigger line with explosive green momentum. Cinematic depth of field."
        ),
        "shot_prompts": [
            "Vertical 9:16 cinematic close-up, 4k photorealistic. A retail trader looking shocked in a dark room as a volatile stock candle wicks down sharply on his monitor, shaking him out of his trade.",
            "Vertical 9:16 cinematic macro shot, 4k photorealistic. A dark institutional chart displaying a razor-sharp glowing cyan horizontal line labeled ENTRY TRIGGER, as green candlesticks coil tightly right underneath it.",
            "Vertical 9:16 cinematic shot, 4k photorealistic. A smartphone lying on a dark carbon-fiber desk lighting up with an instant Telegram breakout alert notification while the monitor behind it surges green.",
        ],
        "shot_scripts": [
            "Have you ever noticed how Tesla or Nvidia always shakes you out right before ripping twenty percent higher?",
            "That happens because retail traders buy inside the noise zone before price clears the institutional sixty-day entry trigger.",
            "Instead of staring at charts all day, our quant engine calculates the exact dollar trigger price for seventy-two market leaders.",
            "Comment ALPHA and I will DM you our free Telegram bot that alerts you the moment a stock hits its Ignition trigger.",
        ],
    },
    {
        "id": "ep07",
        "num": 7,
        "title": "The +100% Free-Ride Rule: How Quants Trade With Zero Principal Risk",
        "accent": (16, 185, 129, 255),
        "ui_type": "rsa",
        "master_prompt": (
            "Vertical 9:16 cinematic 4k photorealistic shot. A glowing emerald stock chart doubling to plus one hundred "
            "percent on a dark glass screen, while a calm institutional trader locks in half his chips into a sleek "
            "digital vault and lets the remaining half ride skyward. Dark luxury Wall Street aesthetic."
        ),
        "shot_prompts": [
            "Vertical 9:16 cinematic shot, 4k photorealistic. A thrilled retail trader celebrating a big paper gain on his laptop in a dimly lit room, unaware as the chart behind him suddenly reverses into red.",
            "Vertical 9:16 cinematic macro shot, 4k photorealistic. A dark quantitative chart hitting a glowing gold target line labeled PLUS 100 PERCENT TP1, automatically splitting the position in half with a crisp digital animation.",
            "Vertical 9:16 cinematic medium shot, 4k photorealistic. A relaxed hedge fund trader sipping espresso by a floor-to-ceiling city window while a trailing green trendline climbs steadily on his tablet.",
        ],
        "shot_scripts": [
            "The worst feeling in trading is watching an eighty percent profit round-trip all the way back into a loss.",
            "Wall Street quants prevent this with the Free-Ride Rule: the moment a position hits plus one hundred percent, you sell exactly half.",
            "That pulls one hundred percent of your original cash off the table, turning the rest of your shares into a mathematically risk-free runner.",
            "Comment ALPHA below to get exact minus nine percent stop and two-X target prices for every US stock at getbreakai dot com.",
        ],
    },
    {
        "id": "ep08",
        "num": 8,
        "title": "We Backtested 126 US Stocks Over 26 Years — Here Is What Beat Wall Street",
        "accent": (245, 158, 11, 255),
        "ui_type": "rsa",
        "master_prompt": (
            "Vertical 9:16 cinematic 4k photorealistic shot. A glowing high-speed supercomputer server room transitioning "
            "to an ultrawide glass monitor displaying a massive twenty-six year equity curve climbing three hundred forty-nine "
            "times higher than a flat benchmark line. Dark cinematic lighting, IMAX documentary style."
        ),
        "shot_prompts": [
            "Vertical 9:16 cinematic tracking shot, 4k photorealistic. Inside a dark glass quantitative server room, blue and emerald data lights pulse rapidly as historical stock market timelines from year 2000 to 2026 stream across a screen.",
            "Vertical 9:16 cinematic macro shot, 4k photorealistic. A comparison chart on a dark monitor where a red line labeled Naive Dip Buying crashes repeatedly, while a glowing emerald curve labeled Right-Side PW-RSI compounds steeply upward.",
            "Vertical 9:16 cinematic shot, 4k photorealistic. A quantitative researcher standing in front of a large dark glass display showing 24.48% CAGR and 349x cumulative return metrics.",
        ],
        "shot_scripts": [
            "We backtested one hundred twenty-six US stocks across twenty-six years, including the dot-com crash, two thousand eight, and twenty twenty-two.",
            "Buying fifty-two week lows blindly on the left side underperformed and suffered brutal seventy percent drawdowns.",
            "Waiting for Right-Side Ignition above the sixty-day trendline with asymmetric exits compounded at twenty-four point four eight percent annually.",
            "Want to see which five stocks are in the Ignition Zone today? Comment ALPHA for instant access to getbreakai dot com.",
        ],
    },
    {
        "id": "ep09",
        "num": 9,
        "title": "Fake Breakout vs. Real Institutional Volume: The 1.8x Tell",
        "accent": (16, 185, 129, 255),
        "ui_type": "rsa",
        "master_prompt": (
            "Vertical 9:16 cinematic 4k photorealistic macro shot. Two side-by-side stock breakouts on a dark glass screen: "
            "the left one has tiny hollow volume bars and collapses in red, while the right one erupts with towering glowing "
            "emerald volume pillars and surges higher. Razor-sharp financial visual effects."
        ),
        "shot_prompts": [
            "Vertical 9:16 cinematic macro shot, 4k photorealistic. A green stock candlestick breaking above a resistance line on a dark monitor, but the volume bars underneath are tiny and dim, followed by an immediate red reversal.",
            "Vertical 9:16 cinematic macro shot, 4k photorealistic. Towering glowing emerald-green volume bars surging nearly double the ten-day average at the exact moment price crosses a golden moving average line.",
            "Vertical 9:16 cinematic medium shot, 4k photorealistic. A sharp Wall Street trader in a dark room nodding as his multi-factor scanner highlights institutional volume accumulation.",
        ],
        "shot_scripts": [
            "Ninety percent of retail breakout trades fail because traders only look at price and ignore institutional volume.",
            "When a stock breaks above its moving average on weak volume, market makers use retail buyers as exit liquidity in a bull trap.",
            "True institutional accumulation leaves a footprint: ten-day volume surging one point five to two times above normal right at the trendline.",
            "Comment ALPHA below and our bot will DM you the live institutional volume and breakout scanner at getbreakai dot com.",
        ],
    },
    {
        "id": "ep10",
        "num": 10,
        "title": "Run This 3-Second Quant Check Before Tomorrow's 9:30 AM Market Open",
        "accent": (56, 189, 248, 255),
        "ui_type": "rsa",
        "master_prompt": (
            "Vertical 9:16 cinematic 4k photorealistic shot. New York Wall Street financial district at dawn just before "
            "9:30 AM, transitioning to a sleek dark trading desk where a trader types a stock ticker into a glowing "
            "Position Doctor diagnostic interface and gets an instant green institutional signal. Crisp morning light."
        ),
        "shot_prompts": [
            "Vertical 9:16 cinematic aerial shot, 4k photorealistic. Lower Manhattan and Wall Street skyscrapers at 9:25 AM dawn, moody blue and gold morning light reflecting off glass towers.",
            "Vertical 9:16 cinematic close-up, 4k photorealistic. A disciplined American trader at a clean dark desk before the opening bell, typing a stock ticker and entry price into a glowing dark-mode diagnostic terminal.",
            "Vertical 9:16 cinematic macro shot, 4k photorealistic. A smartphone and monitor simultaneously displaying an instant green quant diagnosis with exact stop-loss and profit target numbers.",
        ],
        "shot_scripts": [
            "Before the US market opens at nine thirty AM tomorrow, stop trading blind on gut feelings and social media hype.",
            "In three seconds, you can check whether any US stock is in an institutional Right-Side Ignition or a dangerous Bull Trap.",
            "And if you already own a stock, enter your average cost into Position Doctor to get your exact mathematical stop-loss and two-X target.",
            "Comment ALPHA right now and I will DM you direct access to getbreakai dot com and our free Telegram quant bot.",
        ],
    },
]


def find_clips_for_episode(ep_id: str, ui_clip_path: pathlib.Path) -> List[str]:
    """
    Looks for user-downloaded Flow clips in FLOW_CLIPS_DIR:
    1) 3-clip mode: `{ep_id}_shot1.mp4`, `{ep_id}_shot2.mp4`, `{ep_id}_shot3.mp4`
    2) Story-matched 3-cut sequence from `ep01.mp4`..`ep10.mp4` + Shot 4 Live UI
    """
    three_clips = [FLOW_CLIPS_DIR / f"{ep_id}_shot{i}.mp4" for i in range(1, 4)]
    if all(p.exists() for p in three_clips):
        return [str(p) for p in three_clips] + [str(ui_clip_path)]

    # Story-matched 3-shot cut map using the 10 downloaded Flow clips so every cut changes angle
    sequence_map = {
        "ep01": ["ep01.mp4", "ep02.mp4", "ep05.mp4"],
        "ep02": ["ep02.mp4", "ep09.mp4", "ep10.mp4"],
        "ep03": ["ep03.mp4", "ep01.mp4", "ep06.mp4"],
        "ep04": ["ep04.mp4", "ep08.mp4", "ep07.mp4"],
        "ep05": ["ep05.mp4", "ep09.mp4", "ep10.mp4"],
        "ep06": ["ep06.mp4", "ep02.mp4", "ep01.mp4"],
        "ep07": ["ep07.mp4", "ep03.mp4", "ep04.mp4"],
        "ep08": ["ep08.mp4", "ep05.mp4", "ep07.mp4"],
        "ep09": ["ep09.mp4", "ep06.mp4", "ep08.mp4"],
        "ep10": ["ep10.mp4", "ep03.mp4", "ep01.mp4"],
    }
    seq = sequence_map.get(ep_id, [f"{ep_id}.mp4"] * 3)
    seq_paths = [FLOW_CLIPS_DIR / name for name in seq]
    if all(p.exists() for p in seq_paths):
        return [str(p) for p in seq_paths] + [str(ui_clip_path)]

    single_clip = FLOW_CLIPS_DIR / f"{ep_id}.mp4"
    if single_clip.exists():
        return [str(single_clip), str(single_clip), str(single_clip), str(ui_clip_path)]

    fallback = [FLOW_CLIPS_DIR / f"shot{i}_flow.mp4" for i in range(1, 4)]
    if all(p.exists() for p in fallback):
        return [str(p) for p in fallback] + [str(ui_clip_path)]

    return [str(ui_clip_path)] * 4


def build_episode(ep: Dict[str, Any], ending_mode: str = "punchline") -> pathlib.Path:
    from flow_shorts_merger import render_clean_fullscreen_shorts_from_clips

    rsa_ui = FLOW_CLIPS_DIR / "rsa_shot4_live_ui.mp4"
    semi_ui = FLOW_CLIPS_DIR / "semi_shot4_live_ui.mp4"
    ui_clip = semi_ui if (ep["ui_type"] == "semi" and semi_ui.exists()) else rsa_ui

    clips = find_clips_for_episode(ep["id"], ui_clip)
    out_mp4 = OUTPUT_DIR / f"{ep['id'].upper()}_US_Viral_Shorts.mp4"

    render_clean_fullscreen_shorts_from_clips(
        clip_paths=clips,
        script=" ".join(ep["shot_scripts"]),
        output_mp4=out_mp4,
        voice="en-US-AndrewMultilingualNeural",
        style="wealth",
        accent_color=ep["accent"],
        top_clean_title="",
        shot_scripts=ep["shot_scripts"],
        ending_mode=ending_mode,
    )
    return out_mp4


def generate_studio_html() -> pathlib.Path:
    import html

    cards = []
    for ep in EPISODES:
        ep_id = ep["id"]
        num = ep["num"]
        title = html.escape(ep["title"])
        mp = html.escape(ep["master_prompt"])
        s1, s2, s3 = [html.escape(x) for x in ep["shot_prompts"]]
        vo = html.escape(" ".join(ep["shot_scripts"]))
        cards.append(
            f"""
    <div class="ep-card">
      <div class="ep-head">
        <span class="ep-badge">EPISODE {num:02d}</span>
        <h2>{title}</h2>
      </div>
      <div class="save-hint">
        💾 다운로드 파일명: 빠른 1컷 모드 <code>{ep_id}.mp4</code> &nbsp;|&nbsp; 3컷 고퀄 모드 <code>{ep_id}_shot1.mp4</code>, <code>{ep_id}_shot2.mp4</code>, <code>{ep_id}_shot3.mp4</code>
        <em>(4번째 컷은 실제 터미널 라이브 UI가 자동 합성됩니다!)</em>
      </div>
      <div class="prompt-box master">
        <div class="p-label">
          <span>⚡ [추천 · 빠른 1컷 모드] 마스터 프롬프트 ({ep_id}.mp4 로 저장)</span>
          <button onclick="copyEl('m-{ep_id}', this)">📋 1클릭 복사</button>
        </div>
        <pre id="m-{ep_id}">{mp}</pre>
      </div>
      <details>
        <summary>🎬 3컷 분할 프롬프트 보기 ({ep_id}_shot1~3.mp4 — 컷 전환 극대화용)</summary>
        <div class="prompt-box">
          <div class="p-label"><span>Shot 1 (0~7초 훅 — {ep_id}_shot1.mp4)</span><button onclick="copyEl('s1-{ep_id}', this)">📋 복사</button></div>
          <pre id="s1-{ep_id}">{s1}</pre>
        </div>
        <div class="prompt-box">
          <div class="p-label"><span>Shot 2 (7~14초 위기/비교 — {ep_id}_shot2.mp4)</span><button onclick="copyEl('s2-{ep_id}', this)">📋 복사</button></div>
          <pre id="s2-{ep_id}">{s2}</pre>
        </div>
        <div class="prompt-box">
          <div class="p-label"><span>Shot 3 (14~22초 월가 퀀트 해법 — {ep_id}_shot3.mp4)</span><button onclick="copyEl('s3-{ep_id}', this)">📋 복사</button></div>
          <pre id="s3-{ep_id}">{s3}</pre>
        </div>
      </details>
      <div class="vo-box">
        <strong>🎙️ 자동 합성될 미국 성우 나레이션 &amp; 0.01초 네온 자막 대본:</strong><br/>
        {vo}
      </div>
    </div>"""
        )

    page_html = f"""<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8"/>
<title>RightSide Alpha — Google Flow 미국 바이럴 쇼츠 10편 프롬프트 스튜디오</title>
<style>
  body {{ background:#090d16; color:#f1f5f9; font-family:-apple-system,BlinkMacSystemFont,'Pretendard',sans-serif; margin:0; padding:32px 20px 80px; line-height:1.55; }}
  .wrap {{ max-width:980px; margin:0 auto; }}
  .hero {{ background:linear-gradient(135deg,rgba(16,185,129,0.18),rgba(59,130,246,0.15)); border:1px solid #23304d; border-radius:16px; padding:24px 28px; margin-bottom:26px; }}
  .flow-btn {{ display:inline-block; background:#10b981; color:#04130d; font-weight:800; text-decoration:none; padding:10px 18px; border-radius:10px; margin-top:12px; }}
  .ep-card {{ background:#111827; border:1px solid #1f2937; border-radius:14px; padding:22px 24px; margin-bottom:20px; }}
  .ep-badge {{ background:#3b82f6; color:#fff; font-weight:800; font-size:12px; padding:4px 10px; border-radius:999px; }}
  .ep-head h2 {{ margin:8px 0 8px; font-size:19px; color:#38bdf8; }}
  .save-hint {{ font-size:13px; color:#94a3b8; margin-bottom:12px; }}
  code {{ background:#070a12; color:#34d399; padding:2px 6px; border-radius:4px; }}
  .prompt-box {{ background:#070a12; border:1px solid #1e293b; border-radius:10px; padding:12px 14px; margin-top:10px; }}
  .prompt-box.master {{ border-color:#10b981; }}
  .p-label {{ display:flex; justify-content:space-between; align-items:center; font-size:13px; font-weight:700; color:#cbd5e1; margin-bottom:6px; }}
  pre {{ margin:0; white-space:pre-wrap; font-family:Consolas,monospace; font-size:13.5px; color:#e2e8f0; }}
  button {{ background:#10b981; color:#04130d; border:none; border-radius:7px; padding:6px 14px; font-weight:800; cursor:pointer; }}
  details {{ margin-top:12px; }}
  summary {{ cursor:pointer; color:#93c5fd; font-weight:700; font-size:13.5px; }}
  .vo-box {{ margin-top:12px; font-size:13px; color:#94a3b8; background:#0b111e; padding:10px 14px; border-radius:8px; }}
</style>
</head>
<body>
<div class="wrap">
  <div class="hero">
    <h1 style="margin:0 0 8px;font-size:24px;">🎬 RightSide Alpha — 미국 바이럴 쇼츠/릴스 10편 Flow 프롬프트 스튜디오</h1>
    <p style="margin:0;color:#cbd5e1;font-size:14px;">
      1️⃣ Google Flow에서 <strong>9:16 (Portrait 세로)</strong> 선택 후 아래 프롬프트를 복사해 영상을 생성하세요.<br/>
      2️⃣ 다운로드한 영상을 <code>Downloads(다운로드)</code> 폴더나 <code>{FLOW_CLIPS_DIR}</code> 폴더에 넣으신 뒤 저에게 <strong>"다 받았어 합쳐줘!"</strong>라고 말씀만 해주시면,<br/>
      3️⃣ <strong>미국 원어민 성우 나레이션 + 0.01초 네온 하이라이트 자막 + 사운드 이펙트 + 실제 사이트 라이브 UI(Shot 4)</strong>까지 자동 합본해 완성해 드립니다!
    </p>
    <a class="flow-btn" href="https://labs.google/fx/tools/flow" target="_blank">🚀 Google Flow (Veo) 열기 ↗</a>
  </div>
  {"".join(cards)}
</div>
<script>
function copyEl(id, btn) {{
  navigator.clipboard.writeText(document.getElementById(id).innerText).then(() => {{
    const old = btn.innerText;
    btn.innerText = '✅ 복사됨!';
    setTimeout(() => btn.innerText = old, 1400);
  }});
}}
</script>
</body>
</html>"""

    out_p = WORKSPACE_DIR / "flow_10_prompts_studio.html"
    out_p.write_text(page_html, encoding="utf-8")
    return out_p


def main() -> int:
    parser = argparse.ArgumentParser(description="Build 10 US Viral Promo Shorts from Google Flow clips")
    parser.add_argument("--ep", type=int, default=0, help="Episode number (1-10), or 0 for all available")
    parser.add_argument("--ending", choices=["punchline", "loop"], default="punchline")
    parser.add_argument("--html", action="store_true", help="Generate flow_10_prompts_studio.html only")
    args = parser.parse_args()

    if args.html:
        p = generate_studio_html()
        print(f"✅ Studio HTML saved: {p}")
        return 0

    targets = [e for e in EPISODES if args.ep == 0 or e["num"] == args.ep]
    for ep in targets:
        print(f"\n🎬 Building Episode {ep['num']:02d}: {ep['title']}...")
        out = build_episode(ep, ending_mode=args.ending)
        print(f"✅ Completed: {out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
