#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json
import os
import sys
from pathlib import Path
from playwright.sync_api import sync_playwright

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

OUT_SHOT = Path(r"D:\드림컴퍼니\3사업부\assets\youtube\yt_studio_current.png")

p = sync_playwright().start()
browser = p.chromium.connect_over_cdp("http://127.0.0.1:9223")
ctx = browser.contexts[0]
yt_page = None
for pg in ctx.pages:
    if "studio.youtube.com" in pg.url:
        yt_page = pg
        break

if not yt_page:
    print("No YouTube Studio tab found")
    os._exit(1)

yt_page.bring_to_front()
# Close any welcome modal if visible
close_btns = yt_page.locator("ytcp-button#dismiss-button, ytcp-button#close-button, button[aria-label='닫기'], button[aria-label='Close']")
if close_btns.count() > 0:
    for i in range(close_btns.count()):
        try:
            if close_btns.nth(i).is_visible():
                close_btns.nth(i).click(timeout=2000)
                yt_page.wait_for_timeout(1000)
        except Exception:
            pass

# Click left nav '맞춤설정' (Customization)
cust_item = yt_page.locator("a[href*='/editing'], tp-yt-paper-icon-item:has-text('맞춤설정'), tp-yt-paper-icon-item:has-text('Customization')").first
if cust_item.count() > 0:
    cust_item.click()
    yt_page.wait_for_timeout(4000)

yt_page.screenshot(path=str(OUT_SHOT))
inputs_info = yt_page.evaluate("""() => {
    const res = [];
    document.querySelectorAll('input, textarea, [contenteditable="true"], ytcp-button').forEach((el, idx) => {
        const rect = el.getBoundingClientRect();
        if (rect.width > 0 && rect.height > 0 || el.type === 'file') {
            res.push({
                idx,
                tag: el.tagName,
                type: el.type || '',
                id: el.id || '',
                aria: el.getAttribute('aria-label') || '',
                text: (el.innerText || '').trim().slice(0, 60),
                val: (el.value !== undefined ? el.value : '') || ''
            });
        }
    });
    return res;
}""")
print("URL:", yt_page.url)
print("ELEMENTS:", json.dumps(inputs_info, ensure_ascii=False, indent=2))
sys.stdout.flush()
os._exit(0)
