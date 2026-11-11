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
SHOT_FINAL_IG = str(YT_DIR / "ig_profile_final.png")

p = sync_playwright().start()
browser = p.chromium.connect_over_cdp("http://127.0.0.1:9223")
ctx = browser.contexts[0]
ig_page = None
for pg in ctx.pages:
    if "instagram.com" in pg.url and "facebook.com" not in pg.url:
        ig_page = pg
        break

log = []
if ig_page:
    ig_page.bring_to_front()
    # Try Accounts Center to set Display Name ('이름')
    try:
        ig_page.goto("https://accountscenter.instagram.com/profiles/", wait_until="domcontentloaded", timeout=20000)
        ig_page.wait_for_timeout(3500)
        # Click the getbreakai profile row
        prof_row = ig_page.locator("a[href*='/profiles/'], div[role='button']:has-text('getbreakai'), span:has-text('getbreakai')").first
        if prof_row.count() > 0 and prof_row.is_visible():
            prof_row.click()
            ig_page.wait_for_timeout(3000)
            name_row = ig_page.locator("a[href*='/name'], div[role='button']:has-text('이름'), span:has-text('이름')").first
            if name_row.count() > 0 and name_row.is_visible():
                name_row.click()
                ig_page.wait_for_timeout(2500)
                inp = ig_page.locator("input[type='text'], input").first
                if inp.count() > 0 and inp.is_visible():
                    inp.click()
                    ig_page.keyboard.press("Control+A")
                    ig_page.keyboard.press("Backspace")
                    ig_page.keyboard.type("GetBreakAI | 米国株・新NISAクオンツ", delay=20)
                    ig_page.wait_for_timeout(1000)
                    done_btn = ig_page.locator("div[role='button']:has-text('완료'), button:has-text('완료'), div[role='button']:has-text('Done')").first
                    if done_btn.count() > 0 and done_btn.is_visible():
                        done_btn.click()
                        ig_page.wait_for_timeout(3500)
                        log.append("Set Display Name in Meta Accounts Center")
    except Exception as e:
        log.append(f"Accounts Center note: {e}")

    ig_page.goto("https://www.instagram.com/getbreakai/", wait_until="domcontentloaded", timeout=30000)
    ig_page.wait_for_timeout(4000)
    ig_page.screenshot(path=SHOT_FINAL_IG)

print("RESULT:", json.dumps(log, ensure_ascii=False, indent=2))
sys.stdout.flush()
os._exit(0)
