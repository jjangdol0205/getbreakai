#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json
import os
import sys
from pathlib import Path
from playwright.sync_api import sync_playwright

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

ROOT_DIR = Path(r"D:\드림컴퍼니\3사업부")
YT_DIR = ROOT_DIR / "assets" / "youtube"
CFG = json.loads((YT_DIR / "youtube_insta_channel_config.json").read_text(encoding="utf-8"))["youtube"]

BANNER_PATH = str(YT_DIR / "youtube_banner_2560x1440.png")
PROFILE_PATH = str(YT_DIR / "youtube_profile_800x800.png")
SHOT_TOP = str(YT_DIR / "yt_top_verified.png")


def click_visible_done(page) -> bool:
    page.wait_for_timeout(1500)
    # Find visible ytcp-button#done-button and click it via mouse coordinates
    box = page.evaluate("""() => {
        const btns = Array.from(document.querySelectorAll('ytcp-button#done-button'));
        for (const b of btns) {
            const r = b.getBoundingClientRect();
            if (r.width > 0 && r.height > 0) {
                return { x: r.left + r.width / 2, y: r.top + r.height / 2 };
            }
        }
        return null;
    }""")
    if box:
        page.mouse.click(box["x"], box["y"])
        page.wait_for_timeout(2500)
        return True
    return False


p = sync_playwright().start()
browser = p.chromium.connect_over_cdp("http://127.0.0.1:9223")
ctx = browser.contexts[0]
yt_page = None
for pg in ctx.pages:
    if "studio.youtube.com" in pg.url:
        yt_page = pg
        break

if not yt_page:
    print("ERROR: No YouTube Studio tab found")
    os._exit(1)

yt_page.bring_to_front()
yt_page.wait_for_timeout(1500)

# Close any open dialog first
click_visible_done(yt_page)
yt_page.keyboard.press("Escape")
yt_page.wait_for_timeout(1000)

log = []

# Scroll to top
yt_page.evaluate("window.scrollTo(0, 0)")
yt_page.wait_for_timeout(1000)

# 1. Type Channel Name using real keyboard events
name_inp = yt_page.locator("input.ytcpChannelEditingChannelNameFormInput").first
if name_inp.count() > 0:
    name_inp.scroll_into_view_if_needed()
    name_inp.click()
    yt_page.keyboard.press("Control+A")
    yt_page.keyboard.press("Backspace")
    yt_page.keyboard.type(CFG["channel_name"], delay=25)
    yt_page.wait_for_timeout(1000)
    log.append(f"Typed Channel Name: {CFG['channel_name']}")

# 2. Type Handle using real keyboard events
# Find the handle input (the editable input right after name_inp)
handle_idx = yt_page.evaluate("""() => {
    const inputs = Array.from(document.querySelectorAll('input'));
    for (let i = 0; i < inputs.length; i++) {
        if (inputs[i].classList.contains('ytcpChannelEditingChannelNameFormInput')) {
            return i + 1;
        }
    }
    return -1;
}""")
if handle_idx >= 0:
    h_inp = yt_page.locator("input").nth(handle_idx)
    h_inp.scroll_into_view_if_needed()
    for cand in ["GetBreakAI", "GetBreakAI_JP", "GetBreakAIQuant"]:
        h_inp.click()
        yt_page.keyboard.press("Control+A")
        yt_page.keyboard.press("Backspace")
        yt_page.keyboard.type(cand, delay=35)
        yt_page.wait_for_timeout(2500)
        # Check if publish button is enabled or if handle has error
        has_err = yt_page.evaluate("""() => {
            const txt = document.body.innerText;
            return txt.includes('이미 사용 중') || txt.includes('사용할 수 없는 핸들');
        }""")
        if not has_err:
            log.append(f"Typed valid Handle: @{cand}")
            break

# 3. Upload Banner via first '변경' (#replace-button) + expect_file_chooser
yt_page.evaluate("window.scrollTo(0, 0)")
yt_page.wait_for_timeout(800)
try:
    rep0 = yt_page.locator("ytcp-button#replace-button").nth(0)
    rep0.scroll_into_view_if_needed()
    with yt_page.expect_file_chooser(timeout=6000) as fc:
        rep0.click()
    fc.value.set_files(BANNER_PATH)
    yt_page.wait_for_timeout(2000)
    if click_visible_done(yt_page):
        log.append("Uploaded & confirmed Banner (2560x1440)")
except Exception as e:
    log.append(f"Banner err: {e}")

# 4. Upload Profile Picture via second '변경' (#replace-button) + expect_file_chooser
try:
    rep1 = yt_page.locator("ytcp-button#replace-button").nth(1)
    rep1.scroll_into_view_if_needed()
    with yt_page.expect_file_chooser(timeout=6000) as fc:
        rep1.click()
    fc.value.set_files(PROFILE_PATH)
    yt_page.wait_for_timeout(2000)
    if click_visible_done(yt_page):
        log.append("Uploaded & confirmed Profile Picture (800x800)")
except Exception as e:
    log.append(f"Profile err: {e}")

# 5. Upload Video Watermark via #upload-button
try:
    wm_btn = yt_page.locator("ytcp-button#upload-button").first
    if wm_btn.count() > 0 and wm_btn.is_visible():
        wm_btn.scroll_into_view_if_needed()
        with yt_page.expect_file_chooser(timeout=6000) as fc:
            wm_btn.click()
        fc.value.set_files(PROFILE_PATH)
        yt_page.wait_for_timeout(2000)
        if click_visible_done(yt_page):
            log.append("Uploaded & confirmed Video Watermark (800x800)")
except Exception as e:
    log.append(f"Watermark err: {e}")

# Scroll back to top and click Publish (#publish-button)
yt_page.evaluate("window.scrollTo(0, 0)")
yt_page.wait_for_timeout(1500)
pub_btn = yt_page.locator("ytcp-button#publish-button").first
if pub_btn.count() > 0:
    box = yt_page.evaluate("""() => {
        const b = document.querySelector('ytcp-button#publish-button');
        if (!b) return null;
        const r = b.getBoundingClientRect();
        return { x: r.left + r.width / 2, y: r.top + r.height / 2, disabled: b.hasAttribute('disabled') };
    }""")
    log.append(f"Publish button state before click: {box}")
    if box and not box["disabled"]:
        yt_page.mouse.click(box["x"], box["y"])
        yt_page.wait_for_timeout(6000)
        log.append("Clicked Publish via mouse coordinates")

yt_page.screenshot(path=SHOT_TOP)
print("RESULT:", json.dumps(log, ensure_ascii=False, indent=2))
sys.stdout.flush()
os._exit(0)
