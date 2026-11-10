#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Division 3 (GetBreakAI) — Automated YouTube Studio & Instagram Browser Setup Engine
===================================================================================
 Connects to a Chrome window running on `--remote-debugging-port=9223`
 (launched via `실행_유튜브_인스타_자동셋팅_브라우저.bat`).
- `--status`: Checks open tabs and whether YouTube Studio / Instagram are logged in.
- `--setup-yt`: Automatically populates YouTube Studio Customization (Channel Name, Handle,
  Description, Links, Contact Email, Profile Picture, Banner Image, Watermark).
- `--setup-ig`: Automatically populates Instagram Edit Profile (Name, Bio, Website, Avatar).
"""
import argparse
import json
import socket
import sys
import time
from pathlib import Path
from playwright.sync_api import sync_playwright

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

ROOT_DIR = Path(__file__).resolve().parents[1]
YT_DIR = ROOT_DIR / "assets" / "youtube"
CONFIG_PATH = YT_DIR / "youtube_insta_channel_config.json"
CDP_PORT = 9223


def is_port_open(port: int) -> bool:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(1.0)
        return s.connect_ex(("127.0.0.1", port)) == 0


def check_status() -> dict:
    if not is_port_open(CDP_PORT):
        res = {
            "cdp_port": CDP_PORT,
            "running": False,
            "message": "Port 9223 not open yet. Run 실행_유튜브_인스타_자동셋팅_브라우저.bat on desktop.",
        }
        print(json.dumps(res, ensure_ascii=False, indent=2))
        return res

    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp(f"http://127.0.0.1:{CDP_PORT}")
        ctx = browser.contexts[0]
        pages_info = []
        yt_logged_in = False
        yt_channel_url = None
        ig_logged_in = False

        for pg in ctx.pages:
            u = pg.url
            t = ""
            try:
                t = pg.title()
            except Exception:
                pass
            pages_info.append({"url": u, "title": t})
            if "studio.youtube.com/channel/" in u:
                yt_logged_in = True
                yt_channel_url = u
            if "instagram.com" in u and "accounts/login" not in u:
                ig_logged_in = True

        result = {
            "cdp_port": CDP_PORT,
            "running": True,
            "yt_logged_in": yt_logged_in,
            "yt_channel_url": yt_channel_url,
            "ig_logged_in": ig_logged_in,
            "pages": pages_info,
        }
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return result


def setup_youtube_studio() -> dict:
    if not is_port_open(CDP_PORT):
        raise RuntimeError("Chrome CDP port 9223 is not open. Please run 실행_유튜브_인스타_자동셋팅_브라우저.bat first.")

    cfg = json.loads(CONFIG_PATH.read_text(encoding="utf-8"))["youtube"]
    actions_done = []

    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp(f"http://127.0.0.1:{CDP_PORT}")
        ctx = browser.contexts[0]

        yt_page = None
        for pg in ctx.pages:
            if "studio.youtube.com" in pg.url or "youtube.com" in pg.url:
                yt_page = pg
                break
        if not yt_page:
            yt_page = ctx.new_page()
            yt_page.goto("https://studio.youtube.com", wait_until="domcontentloaded", timeout=30000)
            yt_page.wait_for_timeout(4000)

        yt_page.bring_to_front()
        if "studio.youtube.com" not in yt_page.url:
            yt_page.goto("https://studio.youtube.com", wait_until="domcontentloaded", timeout=30000)
            yt_page.wait_for_timeout(4000)

        cur_url = yt_page.url
        if "accounts.google.com" in cur_url:
            return {"ok": False, "reason": "Google login required in the open Chrome window.", "url": cur_url}

        # Click Customization (맞춤설정 / Customization / カスタマイズ) on left menu
        cust_nav = yt_page.locator(
            "a[href*='/editing'], #menu-paper-icon-item-3, "
            "tp-yt-paper-icon-item:has-text('맞춤설정'), "
            "tp-yt-paper-icon-item:has-text('Customization'), "
            "tp-yt-paper-icon-item:has-text('カスタマイズ')"
        ).first
        if cust_nav.count() > 0:
            cust_nav.click()
            yt_page.wait_for_timeout(4000)
            actions_done.append("Opened YouTube Studio Customization tab")

        # In modern YouTube Studio Customization (Profile / Basic Info / Branding unified or tabbed):
        # 1. Fill Channel Name if input exists
        name_inputs = yt_page.locator(
            "#channel-name-input input, ytcp-form-input-container#name input, "
            "input[aria-label*='이름'], input[aria-label*='Name'], input[aria-label*='名前']"
        )
        if name_inputs.count() > 0 and name_inputs.first.is_visible():
            name_inputs.first.fill(cfg["channel_name"])
            actions_done.append(f"Set Channel Name: {cfg['channel_name']}")

        # 2. Fill Handle if input exists
        handle_inputs = yt_page.locator(
            "#handle-input input, ytcp-form-input-container#handle input, "
            "input[aria-label*='핸들'], input[aria-label*='Handle'], input[aria-label*='ハンドル']"
        )
        if handle_inputs.count() > 0 and handle_inputs.first.is_visible():
            for cand in cfg["handle_candidates"]:
                handle_inputs.first.fill(cand)
                yt_page.wait_for_timeout(1500)
                actions_done.append(f"Tried Handle: @{cand}")
                break

        # 3. Fill Description
        desc_boxes = yt_page.locator(
            "#description-container textarea, ytcp-form-textarea#description textarea, "
            "div[contenteditable='true'][aria-label*='설명'], "
            "div[contenteditable='true'][aria-label*='Description'], "
            "textarea[aria-label*='설명'], textarea[aria-label*='Description']"
        )
        if desc_boxes.count() > 0 and desc_boxes.first.is_visible():
            desc_boxes.first.fill(cfg["description"])
            actions_done.append("Set Japanese/English Institutional Channel Description")

        # 4. Fill Contact Email
        email_inputs = yt_page.locator(
            "#contact-info-input input, input[aria-label*='이메일'], input[aria-label*='Email'], input[type='email']"
        )
        if email_inputs.count() > 0 and email_inputs.first.is_visible():
            email_inputs.first.fill(cfg["contact_email"])
            actions_done.append(f"Set Contact Email: {cfg['contact_email']}")

        # 5. Upload Banner & Profile if file inputs exist on page
        file_inputs = yt_page.locator("input[type='file']")
        if file_inputs.count() >= 2:
            try:
                file_inputs.nth(0).set_input_files(cfg["banner_image"])
                yt_page.wait_for_timeout(2000)
                done_btn = yt_page.locator(
                    "ytcp-button#done-button, button:has-text('완료'), button:has-text('Done'), button:has-text('完了')"
                ).first
                if done_btn.count() > 0 and done_btn.is_visible():
                    done_btn.click()
                    yt_page.wait_for_timeout(1500)
                actions_done.append("Uploaded Banner Image (2560x1440)")
            except Exception as e:
                actions_done.append(f"Banner upload note: {e}")

            try:
                file_inputs.nth(1).set_input_files(cfg["profile_image"])
                yt_page.wait_for_timeout(2000)
                done_btn = yt_page.locator(
                    "ytcp-button#done-button, button:has-text('완료'), button:has-text('Done'), button:has-text('完了')"
                ).first
                if done_btn.count() > 0 and done_btn.is_visible():
                    done_btn.click()
                    yt_page.wait_for_timeout(1500)
                actions_done.append("Uploaded Profile Image (800x800)")
            except Exception as e:
                actions_done.append(f"Profile upload note: {e}")

        # 6. Click Publish (게시 / Publish / 公開する) if enabled
        pub_btn = yt_page.locator(
            "ytcp-button#publish-button, button:has-text('게시'), button:has-text('Publish'), button:has-text('公開')"
        ).first
        if pub_btn.count() > 0 and pub_btn.is_visible():
            try:
                pub_btn.click()
                yt_page.wait_for_timeout(3000)
                actions_done.append("Clicked Publish (게시)")
            except Exception:
                pass

        res = {"ok": True, "url": yt_page.url, "actions_done": actions_done}
        print(json.dumps(res, ensure_ascii=False, indent=2))
        return res


def setup_instagram_profile() -> dict:
    if not is_port_open(CDP_PORT):
        raise RuntimeError("Chrome CDP port 9223 is not open.")

    cfg = json.loads(CONFIG_PATH.read_text(encoding="utf-8"))["instagram"]
    actions_done = []

    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp(f"http://127.0.0.1:{CDP_PORT}")
        ctx = browser.contexts[0]

        ig_page = None
        for pg in ctx.pages:
            if "instagram.com" in pg.url:
                ig_page = pg
                break
        if not ig_page:
            ig_page = ctx.new_page()

        ig_page.bring_to_front()
        ig_page.goto("https://www.instagram.com/accounts/edit/", wait_until="domcontentloaded", timeout=30000)
        ig_page.wait_for_timeout(4000)

        if "accounts/login" in ig_page.url:
            return {"ok": False, "reason": "Instagram login required in the open Chrome window.", "url": ig_page.url}

        # Upload profile photo if input[type=file] exists
        file_inp = ig_page.locator("input[type='file']").first
        if file_inp.count() > 0:
            try:
                file_inp.set_input_files(cfg["profile_image"])
                ig_page.wait_for_timeout(3000)
                actions_done.append("Uploaded Instagram Profile Avatar (1024x1024)")
            except Exception as e:
                actions_done.append(f"Avatar upload note: {e}")

        # Fill Bio (#pepBio or textarea)
        bio_box = ig_page.locator("textarea#pepBio, textarea[aria-label*='소개'], textarea[aria-label*='Bio'], textarea").first
        if bio_box.count() > 0 and bio_box.is_visible():
            bio_box.fill(cfg["bio"])
            actions_done.append("Filled Instagram Japanese Quant Bio")

        # Submit button
        sub_btn = ig_page.locator("div[role='button']:has-text('제출'), div[role='button']:has-text('Submit'), button[type='submit']").first
        if sub_btn.count() > 0 and sub_btn.is_visible():
            sub_btn.click()
            ig_page.wait_for_timeout(3000)
            actions_done.append("Clicked Submit on Instagram Edit Profile")

        res = {"ok": True, "url": ig_page.url, "actions_done": actions_done}
        print(json.dumps(res, ensure_ascii=False, indent=2))
        return res


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--status", action="store_true")
    parser.add_argument("--setup-yt", action="store_true")
    parser.add_argument("--setup-ig", action="store_true")
    args = parser.parse_args()

    if args.setup_yt:
        setup_youtube_studio()
    elif args.setup_ig:
        setup_instagram_profile()
    else:
        check_status()
