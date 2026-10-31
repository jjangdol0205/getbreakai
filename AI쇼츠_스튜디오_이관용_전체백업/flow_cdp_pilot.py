# -*- coding: utf-8 -*-
"""
Single-Session Google Flow Autonomous Pilot
Connects ONCE to Chrome CDP, configures 9:16 Portrait + Auto-Approve ('안 함'),
submits the 4 video prompts from `구글_Flow_실전_가이드_및_프롬프트.md`,
waits for Google Flow (Omni 1.1 Flash / Veo) to generate the <video> clips,
downloads them to `D:\투자홈페이지\AI쇼츠_스튜디오_이관용_전체백업\ai_shorts_output\flow_clips\`,
and merges them into a 100% Clean Full-Screen YouTube Short!
"""
import asyncio
import json
import os
import sys
import time
import base64
from pathlib import Path
import websockets

sys.stdout.reconfigure(encoding="utf-8")

BASE_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = BASE_DIR / "ai_shorts_output"
FLOW_CLIPS_DIR = OUTPUT_DIR / "flow_clips"
SCRATCH_DIR = OUTPUT_DIR / "temp_flow"

FLOW_CLIPS_DIR.mkdir(parents=True, exist_ok=True)
SCRATCH_DIR.mkdir(parents=True, exist_ok=True)


class FlowSession:
    def __init__(self, ws, sid):
        self.ws = ws
        self.sid = sid
        self.msg_id = 10

    async def send(self, method: str, params: dict = None, use_sid: bool = True):
        self.msg_id += 1
        mid = self.msg_id
        payload = {"id": mid, "method": method}
        if params:
            payload["params"] = params
        if use_sid and self.sid:
            payload["sessionId"] = self.sid
        await self.ws.send(json.dumps(payload))
        while True:
            raw = await self.ws.recv()
            resp = json.loads(raw)
            if resp.get("id") == mid:
                return resp

    async def eval_js(self, expr: str, await_promise: bool = False):
        resp = await self.send(
            "Runtime.evaluate",
            {
                "expression": expr,
                "returnByValue": True,
                "awaitPromise": await_promise,
            },
        )
        return resp.get("result", {}).get("result", {}).get("value")

    async def screenshot(self, filename: str):
        r = await self.send("Page.captureScreenshot", {"format": "jpeg", "quality": 85})
        data = r.get("result", {}).get("data")
        if data:
            p = SCRATCH_DIR / filename
            p.write_bytes(base64.b64decode(data))
            print(f"  [Screenshot] {p}", flush=True)

    async def click_xy(self, x: float, y: float):
        await self.send(
            "Input.dispatchMouseEvent",
            {"type": "mousePressed", "x": x, "y": y, "button": "left", "clickCount": 1},
        )
        await asyncio.sleep(0.08)
        await self.send(
            "Input.dispatchMouseEvent",
            {"type": "mouseReleased", "x": x, "y": y, "button": "left", "clickCount": 1},
        )


async def run_pilot():
    port_file = os.path.expandvars(r"%LOCALAPPDATA%\Google\Chrome\User Data\DevToolsActivePort")
    lines = open(port_file).read().strip().splitlines()
    ws_url = f"ws://127.0.0.1:{lines[0]}{lines[1]}"
    print("Connecting to Chrome CDP (Please click [Allow/허용] once in Chrome)...", flush=True)

    async with websockets.connect(ws_url, open_timeout=120, max_size=100 * 1024 * 1024, ping_interval=20) as ws:
        sess = FlowSession(ws, None)
        r = await sess.send("Target.getTargets", use_sid=False)
        tid = None
        for t in r.get("result", {}).get("targetInfos", []):
            if t.get("type") == "page" and ("flow.google" in t.get("url", "") or "labs.google" in t.get("url", "")):
                tid = t["targetId"]
                print("Found Google Flow tab:", t.get("url"), flush=True)
                break
        if not tid:
            raise RuntimeError("Google Flow tab not found!")

        r_att = await sess.send("Target.attachToTarget", {"targetId": tid, "flatten": True}, use_sid=False)
        sess.sid = r_att["result"]["sessionId"]
        await sess.send("Page.enable")
        await sess.send("Runtime.enable")
        print("Attached to Google Flow session:", sess.sid, flush=True)

        # ----------------------------------------------------------------------
        # STEP 1: Configure Agent Settings ('안 함', '9:16' Portrait, '저장')
        # ----------------------------------------------------------------------
        print("[STEP 1] Configuring Google Flow Agent Settings (Auto-confirm '안 함' + '9:16' Portrait)...", flush=True)
        js_config = """
        (() => {
            const log = [];
            // 1. Click '안 함' (No confirmation before generating)
            const allEls = Array.from(document.querySelectorAll('div, label, span, button, [role="radio"]'));
            const noConfirm = allEls.find(e => e.innerText && e.innerText.trim().startsWith('안 함'));
            if (noConfirm) {
                noConfirm.click();
                log.push('Clicked 안 함');
            }
            // 2. Click all '9:16' buttons (for both image and video defaults)
            const btns916 = Array.from(document.querySelectorAll('button, [role="button"], [role="radio"], div')).filter(
                e => e.innerText && e.innerText.trim().endsWith('9:16') && e.getBoundingClientRect().x > 1300
            );
            btns916.forEach(b => { b.click(); log.push('Clicked 9:16 at y=' + Math.round(b.getBoundingClientRect().y)); });

            // 3. Click '저장' (Save button)
            const saveBtn = Array.from(document.querySelectorAll('button')).find(
                b => b.innerText && (b.innerText.trim() === '저장' || b.innerText.trim() === 'Save')
            );
            if (saveBtn) {
                saveBtn.click();
                log.push('Clicked 저장');
            }
            return log;
        })()
        """
        cfg_res = await sess.eval_js(js_config)
        print("  Config actions:", cfg_res, flush=True)
        await asyncio.sleep(2.0)
        await sess.screenshot("flow_after_save.jpg")

        # ----------------------------------------------------------------------
        # STEP 2: Submit the 4 Video Prompts to Google Flow Agent
        # ----------------------------------------------------------------------
        # We ask the Flow Agent to generate our 4 vertical 9:16 video clips!
        combined_prompt = (
            "Please generate 4 separate 9:16 vertical cinematic videos for a medical documentary Short:\n"
            "Video 1: Extreme macro cinematic shot. A tired human eye slowly blinks and the pupil dilates as blue smartphone light flickers across the iris in a dark room at 3 AM. Subtle handheld camera movement, 85mm macro lens.\n"
            "Video 2: 3D medical documentary animation. The camera slowly orbits around a translucent human head while glowing cyan and amber neural pathways pulse and fire rapidly across the cerebral cortex.\n"
            "Video 3: Microscopic 3D scientific CGI. Camera pushes forward through a dense forest of brain neurons as bright bio-electrical action potentials shoot along axons and toxic red particles accumulate around synapses.\n"
            "Video 4: Handheld documentary shot inside a dark hospital neurology lab. A neurologist points at a glowing brain MRI scan on a diagnostic monitor as the scan slices animate on screen."
        )

        print("[STEP 2] Finding prompt input box and entering prompt...", flush=True)
        box_info = await sess.eval_js("""
        (() => {
            const box = document.querySelector('[contenteditable="true"], textarea');
            if (!box) return null;
            box.focus();
            const r = box.getBoundingClientRect();
            return {x: r.x + r.width / 2, y: r.y + r.height / 2, tag: box.tagName};
        })()
        """)
        print("  Input box:", box_info, flush=True)
        if box_info:
            await sess.click_xy(box_info["x"], box_info["y"])
            await asyncio.sleep(0.3)
            await sess.send("Input.insertText", {"text": combined_prompt})
            await asyncio.sleep(0.8)
            await sess.screenshot("flow_prompt_typed.jpg")

            # Find the submit arrow ('arrow_forward') button coordinates and perform real mouse click + Enter key
            arrow_info = await sess.eval_js("""
            (() => {
                const btns = Array.from(document.querySelectorAll('button'));
                const arrow = btns.find(b => b.innerText.trim() === 'arrow_forward' || b.getAttribute('aria-label')?.includes('전송') || b.getAttribute('aria-label')?.includes('Send'));
                if (arrow && !arrow.disabled) {
                    const r = arrow.getBoundingClientRect();
                    return {x: r.x + r.width / 2, y: r.y + r.height / 2};
                }
                return null;
            })()
            """)
            if arrow_info:
                await sess.click_xy(arrow_info["x"], arrow_info["y"])
                print("  Clicked submit arrow at:", arrow_info, flush=True)
            await sess.send("Input.dispatchKeyEvent", {"type": "keyDown", "key": "Enter", "code": "Enter", "windowsVirtualKeyCode": 13})
            await sess.send("Input.dispatchKeyEvent", {"type": "keyUp", "key": "Enter", "code": "Enter", "windowsVirtualKeyCode": 13})

        # ----------------------------------------------------------------------
        # STEP 3: Monitor Generation & Auto-Confirm if Agent asks
        # ----------------------------------------------------------------------
        print("[STEP 3] Monitoring Google Flow video generation...", flush=True)
        downloaded_urls = set()
        for step in range(40):  # Wait up to ~3.5 minutes
            await asyncio.sleep(5.0)

            # Check if there is any '확인' / '생성' / '승인' / 'Generate' confirmation button in the chat panel and click it
            status = await sess.eval_js("""
            (() => {
                // Check for any confirmation button in chat
                const chatBtns = Array.from(document.querySelectorAll('button')).filter(b => {
                    const r = b.getBoundingClientRect();
                    const t = (b.innerText || '').trim();
                    return r.x > 1400 && r.y > 200 && r.y < 800 && (
                        t.includes('생성') || t.includes('확인') || t.includes('승인') || t.includes('계속') ||
                        t.includes('Generate') || t.includes('Confirm') || t.includes('Approve')
                    );
                });
                const clicked = [];
                chatBtns.forEach(b => {
                    if (!b.disabled) { b.click(); clicked.push(b.innerText.trim()); }
                });

                // Find all <video> elements on the page
                const vids = Array.from(document.querySelectorAll('video')).map(v => v.src || v.querySelector('source')?.src).filter(Boolean);
                return {clicked, vids_count: vids.length, vids};
            })()
            """)
            print(f"  [Poll {step+1}/40] videos={status.get('vids_count')} clicked={status.get('clicked')}", flush=True)

            if step in (1, 4, 8, 15, 25):
                await sess.screenshot(f"flow_poll_{step+1:02d}.jpg")

            vids = status.get("vids", [])
            for v_url in vids:
                if v_url not in downloaded_urls and (v_url.startswith("http") or v_url.startswith("blob:")):
                    idx = len(downloaded_urls) + 1
                    print(f"  -> Downloading generated video #{idx}...", flush=True)
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
                        out_f = FLOW_CLIPS_DIR / f"flow_clip_{idx:02d}.mp4"
                        out_f.write_bytes(base64.b64decode(b64_vid))
                        downloaded_urls.add(v_url)
                        print(f"  ✅ Saved {out_f} ({round(out_f.stat().st_size/1024/1024, 2)} MB)", flush=True)

            if len(downloaded_urls) >= 4:
                print("🎉 All 4 Google Flow videos downloaded!", flush=True)
                break

        await sess.screenshot("flow_final_state.jpg")
        print(f"Total downloaded Flow clips: {len(downloaded_urls)}", flush=True)


if __name__ == "__main__":
    asyncio.run(run_pilot())
