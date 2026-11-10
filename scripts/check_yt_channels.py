#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json
import os
import sys
from pathlib import Path
from playwright.sync_api import sync_playwright

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

OUT_SHOT = Path(r"D:\드림컴퍼니\3사업부\assets\youtube\yt_switcher_current.png")

p = sync_playwright().start()
browser = p.chromium.connect_over_cdp("http://127.0.0.1:9223")
ctx = browser.contexts[0]
sw_page = ctx.new_page()
sw_page.goto("https://www.youtube.com/channel_switcher", wait_until="networkidle", timeout=30000)
sw_page.wait_for_timeout(3000)
sw_page.screenshot(path=str(OUT_SHOT))
channels = sw_page.evaluate("""() => {
    const items = [];
    document.querySelectorAll('ytd-account-item-renderer, tp-yt-paper-icon-item, #channel-title').forEach(el => {
        const t = (el.innerText || '').trim();
        if (t) items.push(t);
    });
    return items;
}""")
print("CHANNELS:", json.dumps(channels, ensure_ascii=False, indent=2))
sw_page.close()
sys.stdout.flush()
os._exit(0)
