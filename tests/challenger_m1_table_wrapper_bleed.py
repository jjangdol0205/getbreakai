#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
Challenger M1-2 Empirical Verification Suite:
Table Wrapper Integrity & Mobile Viewport Bleed Audit (375px) for Division 3 (GetBreakAI)

Target File: D:\드림컴퍼니\3사업부\dist\index.html
Audit Requirements:
1. DOM inspection: Inspect table wrapper around #gbQuickMatrixTable in dist/index.html.
2. CSS validation: Ensure .comp-table-wrap defines 'overflow-x: auto' and inline styles preserve it.
3. Headless Browser (Playwright Chromium) Execution at 375px mobile viewport:
   - window.innerWidth vs document.documentElement.scrollWidth (zero document-level horizontal bleed).
   - .comp-table-wrap computed styles and scrollability.
   - #gbQuickMatrixTable inner scrollWidth vs wrapper clientWidth.
   - Interactive market filter button state changes at 375px (All / TSE / US).
4. Store #296100 and Live UUID preservation in dist/index.html & dist/jp/index.html.
"""

import os
import sys
import re
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright

DIST_DIR = r"D:\드림컴퍼니\3사업부\dist"
DIST_INDEX = os.path.join(DIST_DIR, "index.html")
DIST_JP_INDEX = os.path.join(DIST_DIR, "jp", "index.html")

class EmpiricalAuditResults:
    def __init__(self):
        self.passes = 0
        self.failures = 0
        self.findings = []

    def check(self, condition: bool, description: str, detail: str = ""):
        if condition:
            self.passes += 1
            print(f"  ✓ [PASS] {description}")
        else:
            self.failures += 1
            msg = f"  ✗ [FAIL] {description} ({detail})" if detail else f"  ✗ [FAIL] {description}"
            print(msg)
            self.findings.append(msg)

def run_dom_and_css_audit(results: EmpiricalAuditResults):
    print("\n[Suite 1: Static DOM & CSS AST Audit of dist/index.html]")
    results.check(os.path.exists(DIST_INDEX), f"dist/index.html exists at {DIST_INDEX}")

    with open(DIST_INDEX, "r", encoding="utf-8") as f:
        html_content = f.read()

    soup = BeautifulSoup(html_content, "html.parser")

    # 1. Locate #gbQuickMatrixTable
    table = soup.find("table", id="gbQuickMatrixTable")
    results.check(table is not None, "Element <table id='gbQuickMatrixTable'> exists in dist/index.html")

    if not table:
        return

    # 2. Check classes and structure
    classes = table.get("class", [])
    results.check("comp-table" in classes, "Table has 'comp-table' class")

    thead = table.find("thead")
    results.check(thead is not None, "Table contains <thead> element")

    headers = [th.get_text(strip=True) for th in table.find_all("th")]
    results.check(len(headers) == 7, f"Table header has exactly 7 columns (found {len(headers)}: {headers})")

    tbody = table.find("tbody")
    results.check(tbody is not None, "Table contains <tbody> element")

    rows = table.find_all("tr", class_="matrix-row")
    results.check(len(rows) >= 5, f"Table contains at least 5 matrix rows (found {len(rows)})")

    # 3. Locate immediate parent wrapper
    parent = table.parent
    results.check(parent.name == "div", f"Table immediate parent is a <div> (found <{parent.name}>)")

    parent_classes = parent.get("class", [])
    results.check("comp-table-wrap" in parent_classes, f"Parent has class 'comp-table-wrap' (classes={parent_classes})")

    # 4. Check parent wrapper inline styles do NOT disable overflow-x
    parent_style = parent.get("style", "")
    has_conflicting_overflow = bool(re.search(r"overflow(-x)?\s*:\s*(visible|hidden)", parent_style))
    results.check(not has_conflicting_overflow, f"Parent inline style does not disable overflow ({parent_style})")

    # 5. Check CSS stylesheet rules for .comp-table-wrap
    style_tags = soup.find_all("style")
    all_css = "\n".join(s.get_text() for s in style_tags)

    comp_wrap_rule = re.search(r"\.comp-table-wrap\s*\{([^}]+)\}", all_css)
    results.check(comp_wrap_rule is not None, "CSS rule for '.comp-table-wrap' exists in embedded styles")

    if comp_wrap_rule:
        css_body = comp_wrap_rule.group(1)
        has_overflow_x = bool(re.search(r"overflow-x\s*:\s*auto", css_body))
        results.check(has_overflow_x, "'.comp-table-wrap' CSS rule explicitly specifies 'overflow-x: auto'")

    # 6. Check root/body overflow containment
    has_body_containment = bool(re.search(r"html\s*,\s*body\s*\{[^}]*overflow-x\s*:\s*hidden", all_css))
    results.check(has_body_containment, "html, body enforces 'overflow-x: hidden' to prevent page-level horizontal jitter")

def run_playwright_viewport_audit(results: EmpiricalAuditResults):
    print("\n[Suite 2: Headless Playwright 375px Mobile Viewport Bleed Audit]")
    file_url = f"file:///{DIST_INDEX.replace('\\', '/')}"

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        # Test at standard mobile viewports: 375x667 (iPhone SE), 375x812 (iPhone Mini/X)
        for vp_width, vp_height in [(375, 667), (375, 812)]:
            context = browser.new_context(
                viewport={"width": vp_width, "height": vp_height},
                user_agent="Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/604.1"
            )
            page = context.new_page()
            page.goto(file_url, wait_until="load")

            # 1. Document-level horizontal bleed test
            metrics = page.evaluate("""() => {
                return {
                    windowWidth: window.innerWidth,
                    docScrollWidth: document.documentElement.scrollWidth,
                    bodyScrollWidth: document.body.scrollWidth,
                    matrixTable: (() => {
                        const tbl = document.getElementById('gbQuickMatrixTable');
                        if (!tbl) return null;
                        const rect = tbl.getBoundingClientRect();
                        return {
                            scrollWidth: tbl.scrollWidth,
                            clientWidth: tbl.clientWidth,
                            offsetWidth: tbl.offsetWidth,
                            rectWidth: rect.width
                        };
                    })(),
                    wrapper: (() => {
                        const tbl = document.getElementById('gbQuickMatrixTable');
                        if (!tbl || !tbl.parentElement) return null;
                        const w = tbl.parentElement;
                        const rect = w.getBoundingClientRect();
                        const computed = window.getComputedStyle(w);
                        return {
                            className: w.className,
                            scrollWidth: w.scrollWidth,
                            clientWidth: w.clientWidth,
                            offsetWidth: w.offsetWidth,
                            rectWidth: rect.width,
                            rectLeft: rect.left,
                            rectRight: rect.right,
                            overflowX: computed.overflowX,
                            overflowY: computed.overflowY
                        };
                    })(),
                    section: (() => {
                        const s = document.getElementById('gbQuickMatrixSection');
                        if (!s) return null;
                        const rect = s.getBoundingClientRect();
                        return {
                            rectWidth: rect.width,
                            rectLeft: rect.left,
                            rectRight: rect.right
                        };
                    })()
                };
            }""")

            vp_desc = f"{vp_width}x{vp_height}"
            results.check(
                metrics["docScrollWidth"] <= vp_width,
                f"[{vp_desc}] document.documentElement.scrollWidth ({metrics['docScrollWidth']}px) <= viewport width ({vp_width}px)",
                f"Document horizontal bleed detected: scrollWidth={metrics['docScrollWidth']} > {vp_width}"
            )
            results.check(
                metrics["bodyScrollWidth"] <= vp_width,
                f"[{vp_desc}] document.body.scrollWidth ({metrics['bodyScrollWidth']}px) <= viewport width ({vp_width}px)",
                f"Body horizontal bleed detected: scrollWidth={metrics['bodyScrollWidth']} > {vp_width}"
            )

            wrapper = metrics["wrapper"]
            results.check(wrapper is not None, f"[{vp_desc}] Wrapper element located")
            if wrapper:
                results.check(
                    wrapper["overflowX"] == "auto",
                    f"[{vp_desc}] Wrapper computed overflow-x is 'auto' (got '{wrapper['overflowX']}')"
                )
                results.check(
                    wrapper["rectWidth"] <= vp_width,
                    f"[{vp_desc}] Wrapper bounding rect width ({wrapper['rectWidth']:.1f}px) fits within viewport ({vp_width}px)"
                )
                results.check(
                    wrapper["rectRight"] <= vp_width + 1.0,
                    f"[{vp_desc}] Wrapper right edge ({wrapper['rectRight']:.1f}px) does not overflow viewport ({vp_width}px)"
                )

            table_meta = metrics["matrixTable"]
            results.check(table_meta is not None, f"[{vp_desc}] #gbQuickMatrixTable located")
            if table_meta and wrapper:
                # The table should naturally be wider than 375px on mobile, requiring horizontal scroll
                results.check(
                    table_meta["scrollWidth"] > wrapper["clientWidth"],
                    f"[{vp_desc}] Table content width ({table_meta['scrollWidth']}px) exceeds wrapper client width ({wrapper['clientWidth']}px), proving table scroll activation"
                )

            # 2. Test horizontal scrollability in wrapper
            scroll_result = page.evaluate("""() => {
                const tbl = document.getElementById('gbQuickMatrixTable');
                if (!tbl || !tbl.parentElement) return null;
                const w = tbl.parentElement;
                const initial = w.scrollLeft;
                w.scrollLeft = 80;
                const afterScroll = w.scrollLeft;
                w.scrollLeft = 0;
                return { initial, afterScroll };
            }""")
            results.check(
                scroll_result and scroll_result["afterScroll"] > 0,
                f"[{vp_desc}] Table wrapper smoothly scrolls horizontally (scrolled to {scroll_result.get('afterScroll', 0)}px)"
            )

            # 3. Interactive market filter switching at 375px
            for btn_id, market in [("btnMatrixFilterTse", "tse"), ("btnMatrixFilterUs", "us"), ("btnMatrixFilterAll", "all")]:
                page.click(f"#{btn_id}")
                filter_check = page.evaluate("""() => {
                    return {
                        docScrollWidth: document.documentElement.scrollWidth,
                        windowWidth: window.innerWidth
                    };
                }""")
                results.check(
                    filter_check["docScrollWidth"] <= vp_width,
                    f"[{vp_desc}] After clicking filter #{btn_id} ({market}), page scrollWidth ({filter_check['docScrollWidth']}px) remains <= viewport ({vp_width}px)"
                )

            context.close()
        browser.close()

def run_monetization_and_live_uuid_audit(results: EmpiricalAuditResults):
    print("\n[Suite 3: Lemon Squeezy Store #296100 & Live UUID Protection Audit]")
    results.check(os.path.exists(DIST_INDEX), "dist/index.html exists for monetization check")
    results.check(os.path.exists(DIST_JP_INDEX), "dist/jp/index.html exists for monetization check")

    with open(DIST_INDEX, "r", encoding="utf-8") as f:
        root_html = f.read()

    with open(DIST_JP_INDEX, "r", encoding="utf-8") as f:
        jp_html = f.read()

    # 1. Live UUID checks in dist/index.html
    results.check("gb-starter-29" in root_html, "dist/index.html contains live UUID 'gb-starter-29'")
    results.check("gb-pro-49" in root_html, "dist/index.html contains live UUID 'gb-pro-49'")
    results.check("gb-inst-1499" in root_html, "dist/index.html contains live UUID 'gb-inst-1499'")

    # 2. Checkout URLs with embed=1
    has_starter_embed = "checkout/buy/gb-starter-29?embed=1" in root_html
    results.check(has_starter_embed, "dist/index.html has gb-starter-29 embed=1 overlay link")

    # 3. Japanese Landing Page checkout and Store #296100 badges
    results.check("gb-starter-29" in jp_html, "dist/jp/index.html contains live UUID 'gb-starter-29'")
    results.check("296100" in jp_html, "dist/jp/index.html references Lemon Squeezy Store #296100 badge")
    results.check("1秒 損切り・適正株数 計算機" in jp_html, "dist/jp/index.html contains '⚡ 1秒 損切り・適正株数 計算機'")
    results.check("185,000" in jp_html, "dist/jp/index.html contains '-¥185,000' emotional loss defense comparison")

def main():
    print("========================================================================")
    print("   CHALLENGER M1-2 EMPIRICAL AUDIT: TABLE WRAPPER & 375px BLEED TEST   ")
    print("========================================================================")

    results = EmpiricalAuditResults()

    run_dom_and_css_audit(results)
    run_playwright_viewport_audit(results)
    run_monetization_and_live_uuid_audit(results)

    print("\n========================================================================")
    print(f"AUDIT SUMMARY: {results.passes} Passed / {results.failures} Failed")
    print("========================================================================")

    if results.failures > 0:
        print("\nFAILURES DETECTED:")
        for f in results.findings:
            print(f)
        sys.exit(1)
    else:
        print("\n✨ ALL EMPIRICAL CHALLENGER TESTS PASSED (0 Viewport Bleed at 375px) ✨")
        sys.exit(0)

if __name__ == "__main__":
    main()
