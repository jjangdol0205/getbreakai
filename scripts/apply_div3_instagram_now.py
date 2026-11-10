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
AVATAR_PATH = str(YT_DIR / "getbreakai_profile_avatar_1024.png")
SHOT_EDIT = str(YT_DIR / "ig_edit_page.png")
SHOT_PROFILE = str(YT_DIR / "ig_profile_verified.png")

p = sync_playwright().start()
browser = p.chromium.connect_over_cdp("http://127.0.0.1:9223")
ctx = browser.contexts[0]
ig_page = None
for pg in ctx.pages:
    if "instagram.com" in pg.url and "facebook.com" not in pg.url:
        ig_page = pg
        break

if not ig_page:
    print("ERROR: No Instagram tab found")
    os._exit(1)

ig_page.bring_to_front()
ig_page.goto("https://www.instagram.com/semifeargreed/", wait_until="domcontentloaded", timeout=30000)
ig_page.wait_for_timeout(4000)

log = []

# Click '프로필 편집' from profile page
edit_btn = ig_page.locator("a[href*='/accounts/edit'], div[role='button']:has-text('프로필 편집'), a:has-text('프로필 편집')").first
if edit_btn.count() > 0 and edit_btn.is_visible():
    edit_btn.click()
    ig_page.wait_for_timeout(4000)
    log.append("Clicked 프로필 편집")
else:
    ig_page.goto("https://www.instagram.com/accounts/edit/", wait_until="domcontentloaded", timeout=30000)
    ig_page.wait_for_timeout(4000)

# 1. Upload Profile Photo
try:
    chg_btn = ig_page.locator("div[role='button']:has-text('사진 변경'), button:has-text('사진 변경')").first
    if chg_btn.count() > 0 and chg_btn.is_visible():
        # Sometimes clicking '사진 변경' opens a modal with '사진 업로드' or triggers file chooser directly
        file_inps = ig_page.locator("input[type='file']")
        if file_inps.count() > 0:
            file_inps.first.set_input_files(AVATAR_PATH)
            ig_page.wait_for_timeout(4000)
            log.append("Uploaded Avatar via input[type=file]")
        else:
            chg_btn.click()
            ig_page.wait_for_timeout(1500)
            up_btn = ig_page.locator("button:has-text('사진 업로드'), div[role='button']:has-text('사진 업로드')").first
            if up_btn.count() > 0 and up_btn.is_visible():
                with ig_page.expect_file_chooser(timeout=5000) as fc:
                    up_btn.click()
                fc.value.set_files(AVATAR_PATH)
                ig_page.wait_for_timeout(4000)
                log.append("Uploaded Avatar via 사진 업로드 dialog")
except Exception as e:
    log.append(f"Avatar upload note: {e}")

# 2. Fill Bio (#pepBio) via React native setter + keyboard events
bio_text = (
    "📊 米国株・東証プライムの機関ブレイクアウトAI\n"
    "🔥 SEC開示・Gamma壁・20日高値突破を毎日速報\n"
    "🛡️ 2.0x ATR逆指値＆新NISA株数を3秒計算\n"
    "👇 無料AI株数・損切り計算機: getbreakai.com"
)

bio_updated = ig_page.evaluate("""(val) => {
    const ta = document.querySelector('textarea#pepBio') || document.querySelector('textarea');
    if (!ta) return false;
    ta.focus();
    const nativeSetter = Object.getOwnPropertyDescriptor(window.HTMLTextAreaElement.prototype, 'value').set;
    nativeSetter.call(ta, val);
    ta.dispatchEvent(new Event('input', { bubbles: true }));
    ta.dispatchEvent(new Event('change', { bubbles: true }));
    return true;
}""", bio_text)
ig_page.wait_for_timeout(1500)
log.append(f"Updated Bio via React setter: {bio_updated}")

ig_page.screenshot(path=SHOT_EDIT)

# 3. Click Submit (제출) via coordinates if enabled
sub_info = ig_page.evaluate("""() => {
    const btns = Array.from(document.querySelectorAll('div[role="button"], button'));
    for (const b of btns) {
        const t = (b.innerText || '').trim();
        if (t === '제출' || t === 'Submit') {
            const r = b.getBoundingClientRect();
            return {
                x: r.left + r.width / 2,
                y: r.top + r.height / 2,
                disabled: b.getAttribute('aria-disabled') === 'true'
            };
        }
    }
    return null;
}""")
log.append(f"Submit button info: {sub_info}")

if sub_info and not sub_info["disabled"]:
    ig_page.mouse.click(sub_info["x"], sub_info["y"])
    ig_page.wait_for_timeout(4000)
    log.append("Clicked Submit (제출)")

# 4. Navigate back to profile page and take screenshot
ig_page.goto("https://www.instagram.com/semifeargreed/", wait_until="domcontentloaded", timeout=30000)
ig_page.wait_for_timeout(4500)
ig_page.screenshot(path=SHOT_PROFILE)

print("RESULT:", json.dumps(log, ensure_ascii=False, indent=2))
sys.stdout.flush()
os._exit(0)
