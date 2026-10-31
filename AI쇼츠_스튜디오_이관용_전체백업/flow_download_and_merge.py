# -*- coding: utf-8 -*-
"""
Monitors the active Google Flow tab after prompt submission,
automatically clicks any confirmation/generate buttons using REAL hardware mouse events (click_xy),
extracts all generated <video> MP4 streams to `D:\투자홈페이지\AI쇼츠_스튜디오_이관용_전체백업\ai_shorts_output\flow_clips\`,
and runs `flow_shorts_merger.py` to produce the final 100% Clean Full-Screen Short!
"""
import asyncio
import json
import os
import sys
import base64
from pathlib import Path
import websockets

sys.stdout.reconfigure(encoding="utf-8")

from flow_cdp_pilot import FlowSession, FLOW_CLIPS_DIR, SCRATCH_DIR, OUTPUT_DIR
from flow_shorts_merger import render_clean_fullscreen_shorts_from_clips


async def watch_and_merge():
    port_file = os.path.expandvars(r"%LOCALAPPDATA%\Google\Chrome\User Data\DevToolsActivePort")
    lines = open(port_file).read().strip().splitlines()
    ws_url = f"ws://127.0.0.1:{lines[0]}{lines[1]}"
    print("Connecting to Chrome CDP...", flush=True)

    async with websockets.connect(ws_url, open_timeout=120, max_size=100 * 1024 * 1024, ping_interval=20) as ws:
        sess = FlowSession(ws, None)
        r = await sess.send("Target.getTargets", use_sid=False)
        tid = None
        for t in r.get("result", {}).get("targetInfos", []):
            if t.get("type") == "page" and ("flow.google" in t.get("url", "") or "labs.google" in t.get("url", "")):
                tid = t["targetId"]
                print("Found Google Flow tab:", t.get("url"), flush=True)
                break

        r_att = await sess.send("Target.attachToTarget", {"targetId": tid, "flatten": True}, use_sid=False)
        sess.sid = r_att["result"]["sessionId"]
        await sess.send("Page.enable")
        await sess.send("Runtime.enable")

        await sess.screenshot("flow_after_user_click.jpg")

        downloaded_urls = set()
        saved_paths = []

        for step in range(36):  # Up to 3 minutes
            status = await sess.eval_js("""
            (() => {
                // Check if the white arrow_forward button is still visible with unsubmitted text
                const btns = Array.from(document.querySelectorAll('button'));
                let arrowCoords = null;
                const box = document.querySelector('[contenteditable="true"], textarea');
                const hasText = box && (box.innerText || box.value || '').trim().length > 10;
                if (hasText) {
                    const arrow = btns.find(b => b.innerText.trim() === 'arrow_forward');
                    if (arrow && !arrow.disabled) {
                        const r = arrow.getBoundingClientRect();
                        arrowCoords = {x: r.x + r.width / 2, y: r.y + r.height / 2};
                    }
                }

                // Also check if the agent asks for confirmation in chat
                const confirmBtns = btns.filter(b => {
                    const r = b.getBoundingClientRect();
                    const t = (b.innerText || '').trim();
                    return r.x > 1350 && r.y > 150 && r.y < 820 && !b.disabled && (
                        t.includes('생성') || t.includes('확인') || t.includes('승인') || t.includes('실행') ||
                        t.includes('Generate') || t.includes('Confirm') || t.includes('Approve')
                    );
                }).map(b => {
                    const r = b.getBoundingClientRect();
                    return {text: b.innerText.trim(), x: r.x + r.width / 2, y: r.y + r.height / 2};
                });

                const vids = Array.from(document.querySelectorAll('video')).map(
                    v => v.src || v.currentSrc || v.querySelector('source')?.src
                ).filter(Boolean);

                return {arrowCoords, confirmBtns, vids_count: vids.length, vids};
            })()
            """)

            if status.get("arrowCoords"):
                ac = status["arrowCoords"]
                print(f"  -> Auto-clicking submit button at ({ac['x']:.0f}, {ac['y']:.0f})...", flush=True)
                await sess.click_xy(ac["x"], ac["y"])

            for cb in status.get("confirmBtns", []):
                print(f"  -> Auto-clicking agent confirm button '{cb['text']}' at ({cb['x']:.0f}, {cb['y']:.0f})...", flush=True)
                await sess.click_xy(cb["x"], cb["y"])
                await asyncio.sleep(0.5)

            vids = status.get("vids", [])
            print(f"  [Poll {step+1}/36] videos_on_page={len(vids)}", flush=True)

            for v_url in vids:
                if v_url not in downloaded_urls:
                    idx = len(downloaded_urls) + 1
                    print(f"  -> Extracting generated video #{idx}...", flush=True)
                    b64_vid = await sess.eval_js(f"""
                    (async () => {{
                        try {{
                            const resp = await fetch({json.dumps(v_url)});
                            const blob = await resp.blob();
                            return await new Promise((resolve) => {{
                                const reader = new FileReader();
                                reader.onloadend = () => resolve(reader.result.split(',')[1]);
                                reader.readAsDataURL(blob);
                            }});
                        }} catch (e) {{
                            return null;
                        }}
                    }})()
                    """, await_promise=True)
                    if b64_vid:
                        out_f = FLOW_CLIPS_DIR / f"flow_veo_clip_{idx:02d}.mp4"
                        out_f.write_bytes(base64.b64decode(b64_vid))
                        if out_f.stat().st_size > 20000:
                            downloaded_urls.add(v_url)
                            saved_paths.append(out_f)
                            print(f"  ✅ Saved {out_f.name} ({round(out_f.stat().st_size/1024/1024, 2)} MB)", flush=True)

            if step in (0, 3, 7, 12, 20):
                await sess.screenshot(f"flow_watch_{step+1:02d}.jpg")

            if len(saved_paths) >= 4:
                print("🎉 All 4 Google Flow videos downloaded!", flush=True)
                break

            await asyncio.sleep(5.0)

        await sess.screenshot("flow_watch_done.jpg")

    if saved_paths:
        script = (
            "If you sleep less than six hours tonight, your brain literally begins to eat itself. "
            "While you are awake, your neurons produce toxic metabolic waste every single second. "
            "Normally, during deep sleep, spinal fluid flushes those toxins right out. "
            "But when you skip sleep, microglial cells go into overdrive and start destroying healthy synapses. "
            "Even worse, just five nights of poor sleep drops your memory retention by forty percent."
        )
        final_out = OUTPUT_DIR / "Flow_US_1_BrainScience_Clean_Shorts.mp4"
        render_clean_fullscreen_shorts_from_clips(saved_paths, script, final_out)


if __name__ == "__main__":
    asyncio.run(watch_and_merge())
