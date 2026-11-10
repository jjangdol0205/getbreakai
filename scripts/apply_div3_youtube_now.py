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
SHOT_BEFORE_PUB = str(YT_DIR / "yt_before_publish.png")
SHOT_AFTER_PUB = str(YT_DIR / "yt_after_publish.png")
SHOT_SETTINGS = str(YT_DIR / "yt_settings_saved.png")


def click_visible_done_button(page) -> bool:
    try:
        clicked = page.evaluate("""() => {
            const selectors = [
                'ytcp-profile-image-editor ytcp-button#done-button',
                'ytcp-banner-editor ytcp-button#done-button',
                'ytcp-Watermark-image-editor ytcp-button#done-button',
                'tp-yt-paper-dialog ytcp-button#done-button',
                'ytcp-dialog ytcp-button#done-button',
                'ytcp-button#done-button'
            ];
            for (const sel of selectors) {
                const btns = Array.from(document.querySelectorAll(sel));
                for (const b of btns) {
                    const r = b.getBoundingClientRect();
                    if (r.width > 0 && r.height > 0) {
                        b.click();
                        const innerBtn = b.querySelector('button');
                        if (innerBtn) innerBtn.click();
                        return true;
                    }
                }
            }
            return false;
        }""")
        if clicked:
            page.wait_for_timeout(2000)
        return clicked
    except Exception:
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
yt_page.wait_for_timeout(2500)

if "/editing/profile" not in yt_page.url:
    yt_page.goto("https://studio.youtube.com/channel/UCz_lV9K4EUZylnnS8zXGrng/editing/profile", wait_until="domcontentloaded", timeout=30000)
    yt_page.wait_for_timeout(4000)

log = []

# Close any open crop modal first
if click_visible_done_button(yt_page):
    log.append("Closed open image crop modal")
else:
    yt_page.keyboard.press("Escape")
    yt_page.wait_for_timeout(1000)

# STEP 1: Fill all text inputs FIRST (Name, Handle, Links)
all_inputs = yt_page.locator("input")
editable_indices = yt_page.evaluate("""() => {
    const list = [];
    document.querySelectorAll('input').forEach((el, i) => {
        if (el.id === 'query-input' || el.type === 'file') return;
        const r = el.getBoundingClientRect();
        if (r.width === 0 && r.height === 0) return;
        if (!el.readOnly && !el.disabled) {
            list.push({ i, val: el.value });
        }
    });
    return list;
}""")
log.append(f"Found {len(editable_indices)} editable inputs")


def set_input_by_global_idx(idx: int, val: str):
    el = all_inputs.nth(idx)
    el.scroll_into_view_if_needed()
    el.fill(val, force=True)
    yt_page.evaluate("""([index, value]) => {
        const el = document.querySelectorAll('input')[index];
        if (el) {
            el.focus();
            el.value = value;
            el.dispatchEvent(new Event('input', { bubbles: true, composed: true }));
            el.dispatchEvent(new Event('change', { bubbles: true, composed: true }));
            el.blur();
        }
    }""", [idx, val])
    yt_page.wait_for_timeout(500)


if len(editable_indices) >= 2:
    # 0: Channel Name
    set_input_by_global_idx(editable_indices[0]["i"], CFG["channel_name"])
    log.append(f"Set Channel Name -> {CFG['channel_name']}")

    # 1: Handle
    for h_cand in CFG["handle_candidates"]:
        set_input_by_global_idx(editable_indices[1]["i"], h_cand)
        yt_page.wait_for_timeout(2200)
        body_t = yt_page.locator("body").inner_text()
        if "이미 사용 중" not in body_t and "사용할 수 없" not in body_t:
            log.append(f"Set Handle -> @{h_cand}")
            break

# STEP 2: Fill Description (#textbox)
desc_box = yt_page.locator("div#textbox[contenteditable='true']").first
if desc_box.count() > 0:
    desc_box.scroll_into_view_if_needed()
    desc_box.fill(CFG["description"], force=True)
    yt_page.wait_for_timeout(800)
    log.append("Set Channel Description")

# STEP 3: Update Links 1 & 2, and Add Link 3
if len(editable_indices) >= 6:
    set_input_by_global_idx(editable_indices[2]["i"], CFG["links"][0]["title"])
    set_input_by_global_idx(editable_indices[3]["i"], CFG["links"][0]["url"])
    log.append(f"Set Link 1 -> {CFG['links'][0]['title']} ({CFG['links'][0]['url']})")

    set_input_by_global_idx(editable_indices[4]["i"], CFG["links"][1]["title"])
    set_input_by_global_idx(editable_indices[5]["i"], CFG["links"][1]["url"])
    log.append(f"Set Link 2 -> {CFG['links'][1]['title']} ({CFG['links'][1]['url']})")

add_link_btn = yt_page.locator("ytcp-button:has-text('링크 추가')").first
if add_link_btn.count() > 0 and add_link_btn.is_visible():
    add_link_btn.scroll_into_view_if_needed()
    add_link_btn.click(force=True)
    yt_page.wait_for_timeout(1200)
    editable_after = yt_page.evaluate("""() => {
        const list = [];
        document.querySelectorAll('input').forEach((el, i) => {
            if (el.id === 'query-input' || el.type === 'file') return;
            const r = el.getBoundingClientRect();
            if (r.width === 0 && r.height === 0) return;
            if (!el.readOnly && !el.disabled) list.push({ i, val: el.value });
        });
        return list;
    }""")
    if len(editable_after) >= 8:
        set_input_by_global_idx(editable_after[6]["i"], CFG["links"][2]["title"])
        set_input_by_global_idx(editable_after[7]["i"], CFG["links"][2]["url"])
        log.append(f"Added Link 3 -> {CFG['links'][2]['title']} ({CFG['links'][2]['url']})")

# STEP 4: Upload Banner, Profile Picture, and Video Watermark via input[type=file]#file-selector
file_inputs = yt_page.locator("input[type='file']#file-selector")
f_count = file_inputs.count()
log.append(f"Found {f_count} file inputs")

if f_count >= 1:
    try:
        file_inputs.nth(0).set_input_files(BANNER_PATH)
        yt_page.wait_for_timeout(2500)
        click_visible_done_button(yt_page)
        log.append("Uploaded Banner (2560x1440)")
    except Exception as e:
        log.append(f"Banner upload err: {e}")

if f_count >= 2:
    try:
        file_inputs.nth(1).set_input_files(PROFILE_PATH)
        yt_page.wait_for_timeout(2500)
        click_visible_done_button(yt_page)
        log.append("Uploaded Profile Picture (800x800)")
    except Exception as e:
        log.append(f"Profile upload err: {e}")

if f_count >= 3:
    try:
        file_inputs.nth(2).set_input_files(PROFILE_PATH)
        yt_page.wait_for_timeout(2500)
        click_visible_done_button(yt_page)
        log.append("Uploaded Video Watermark (800x800)")
    except Exception as e:
        log.append(f"Watermark upload err: {e}")

yt_page.screenshot(path=SHOT_BEFORE_PUB)

# STEP 5: Click Publish (게시)
pub_btn = yt_page.locator("ytcp-button#publish-button").first
if pub_btn.count() > 0:
    pub_btn.scroll_into_view_if_needed()
    yt_page.wait_for_timeout(1000)
    pub_btn.click(force=True)
    yt_page.evaluate("""() => {
        const b = document.querySelector('ytcp-button#publish-button');
        if (b) {
            b.click();
            const ib = b.querySelector('button');
            if (ib) ib.click();
        }
    }""")
    yt_page.wait_for_timeout(5000)
    log.append("Clicked Publish (게시)")

yt_page.screenshot(path=SHOT_AFTER_PUB)

# STEP 6: Open Settings (설정) -> Channel (채널) -> Basic Info (기본 정보) for Keywords
try:
    settings_btn = yt_page.locator("tp-yt-paper-icon-item#settings-item, tp-yt-paper-icon-item:has-text('설정')").first
    if settings_btn.count() > 0:
        settings_btn.click(force=True)
        yt_page.wait_for_timeout(2500)
        ch_tab = yt_page.locator("tp-yt-paper-item:has-text('채널')").first
        if ch_tab.count() > 0:
            ch_tab.click(force=True)
            yt_page.wait_for_timeout(2000)
            kw_input = yt_page.locator("ytcp-chip-bar input#text-input, input[aria-label*='키워드'], input[placeholder*='키워드']").first
            if kw_input.count() > 0 and kw_input.is_visible():
                kw_list = "米国株, 新NISA, エヌビディア, NVDA, パランティア, PLTR, テスラ, TSLA, SOXL, 半導体株, 東京エレクトロン, アドバンテスト, 株式投資, スイングトレード, 損切り, ATR, クオンツ投資, GetBreakAI,"
                kw_input.fill(kw_list, force=True)
                yt_page.keyboard.press("Enter")
                yt_page.wait_for_timeout(1000)
                log.append("Filled Channel SEO Keywords")
            yt_page.screenshot(path=SHOT_SETTINGS)
            save_btn = yt_page.locator("ytcp-button#save-button, ytcp-button:has-text('저장')").first
            if save_btn.count() > 0 and save_btn.is_visible():
                save_btn.click(force=True)
                yt_page.wait_for_timeout(3000)
                log.append("Saved Channel Settings")
except Exception as e:
    log.append(f"Settings step note: {e}")

print("RESULT:", json.dumps(log, ensure_ascii=False, indent=2))
sys.stdout.flush()
os._exit(0)
