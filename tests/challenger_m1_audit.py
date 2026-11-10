#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
tests/challenger_m1_audit.py
Empirical Adversarial Audit Harness for Milestone M1
Visual Readability, Typography, Responsive Layout & Dual-Theme Engine
GetBreakAI (Division 3)
"""

import os
import re
import sys
import glob

# Set UTF-8 output
sys.stdout.reconfigure(encoding='utf-8')

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INDEX_PATH = os.path.join(ROOT_DIR, "index.html")
JP_DIR = os.path.join(ROOT_DIR, "jp")
JP_INDEX_PATH = os.path.join(JP_DIR, "index.html")

passed_tests = 0
failed_tests = 0

def assert_test(cond, name, details=""):
    global passed_tests, failed_tests
    if cond:
        passed_tests += 1
        print(f"  ✓ [PASS] {name}")
    else:
        failed_tests += 1
        print(f"  ❌ [FAIL] {name}: {details}")

print("========================================================================")
print("   CHALLENGER 2 EMPIRICAL AUDIT: MILESTONE M1 DUAL-THEME & TYPOGRAPHY   ")
print("========================================================================")

# ----------------------------------------------------------------------
# 1. HTML & DOM Structure Validation
# ----------------------------------------------------------------------
print("\n[Suite 1: DOM Structure & Page Integrity]")

with open(INDEX_PATH, "r", encoding="utf-8") as f:
    index_html = f.read()

assert_test(index_html.startswith("<!DOCTYPE html>"), "index.html has DOCTYPE html")
assert_test('lang="ja"' in index_html, "index.html has lang=ja")
assert_test('data-jp-theme="light"' in index_html, "index.html default theme is light")
assert_test('<meta name="viewport" content="width=device-width, initial-scale=1.0">' in index_html, "index.html has standard responsive viewport meta")
assert_test('<link rel="canonical" href="https://getbreakai.com/">' in index_html, "index.html has canonical tag")

with open(JP_INDEX_PATH, "r", encoding="utf-8") as f:
    jp_hub_html = f.read()

assert_test(jp_hub_html.startswith("<!DOCTYPE html>"), "jp/index.html has DOCTYPE html")
assert_test('<meta name="viewport"' in jp_hub_html, "jp/index.html has responsive viewport meta")
assert_test('<link rel="canonical" href="https://getbreakai.com/jp/index.html">' in jp_hub_html, "jp/index.html has canonical link")

# Check all 30 jp/*.html files
jp_files = [f for f in glob.glob(os.path.join(JP_DIR, "*.html")) if os.path.basename(f) != "index.html"]
assert_test(len(jp_files) == 30, f"Exactly 30 jp/*.html articles exist (found {len(jp_files)})")

template_leak = False
char_count_ok = True
for fpath in jp_files:
    fname = os.path.basename(fpath)
    with open(fpath, "r", encoding="utf-8") as f:
        content = f.read()
    # Check for unrendered template variables: e.g. {title}, {{something}}
    # Note: avoid matching legitimate CSS like { color: ... } or JS objects
    # Unrendered python f-string placeholders look like {title}, {entry:.2f}, {jp_name}
    bad_tokens = re.findall(r'\{(?:title|jp_name|ticker|date_str|score|summary|verdict_banner|banner_bg|banner_border|banner_color)\b[^\}]*\}', content)
    if bad_tokens:
        template_leak = True
        print(f"    Leaked token in {fname}: {bad_tokens}")
    # Strip HTML tags and count visible characters
    text_only = re.sub(r'<[^>]+>', '', content)
    text_clean = re.sub(r'\s+', ' ', text_only).strip()
    if len(text_clean) < 2500:
        char_count_ok = False
        print(f"    Article {fname} below 2500 chars: {len(text_clean)}")

assert_test(not template_leak, "Zero unrendered template tokens in all 30 articles")
assert_test(char_count_ok, "All 30 jp/*.html articles exceed 2,500 characters")

# Check navigation target anchor integrity in index.html
nav_targets = [
    "radar", "engines", "vip-vault", "jp-research-hub", "pricing",
    "gbQuickMatrixSection", "gbEasyPlaybookBanner", "btnToggleJpTheme"
]
for target in nav_targets:
    assert_test(f'id="{target}"' in index_html, f"Navigation target anchor id='{target}' exists in index.html")

# ----------------------------------------------------------------------
# 2. Responsive Layout & Mobile Components
# ----------------------------------------------------------------------
print("\n[Suite 2: Responsive Layout, Sticky Nav & Mobile Ticker Flexbox]")

# Extract <style> block from index.html
style_match = re.search(r'<style>(.*?)</style>', index_html, re.DOTALL)
assert_test(bool(style_match), "index.html contains embedded <style> block")
style_css = style_match.group(1) if style_match else ""

# Sticky mobile bottom nav
assert_test(".jp-mobile-bottom-nav" in style_css, ".jp-mobile-bottom-nav class defined in CSS")
assert_test("position: fixed" in style_css, "Bottom nav uses position: fixed")
assert_test("bottom: 0" in style_css, "Bottom nav anchored to bottom: 0")
assert_test("z-index: 999" in style_css, "Bottom nav z-index is 999 (above content)")
assert_test("safe-area-inset-bottom" in style_css, "Bottom nav respects safe-area-inset-bottom for modern iOS/Android")
assert_test("padding-bottom: calc(64px + env(safe-area-inset-bottom" in style_css, "Body has padding-bottom offset to prevent bottom-nav obscuring content")

# Mobile ticker horizontal flexbox
ticker_flex_ok = (
    "overflow-x: auto !important" in style_css and
    "flex-wrap: nowrap !important" in style_css and
    "-webkit-overflow-scrolling: touch !important" in style_css
)
assert_test(ticker_flex_ok, "Mobile ticker has smooth touch horizontal scrolling (nowrap + overflow-x: auto)")

ticker_btn_ok = (
    "flex: 0 0 auto !important" in style_css and
    "white-space: nowrap !important" in style_css
)
assert_test(ticker_btn_ok, "Mobile ticker buttons maintain single horizontal line without line wrap")

# Tablet 2-column layout
tablet_grid_ok = (
    "repeat(2, 1fr) !important" in style_css and
    "min-width: 641px" in style_css and
    "max-width: 1024px" in style_css
)
assert_test(tablet_grid_ok, "Tablet media query (641px-1024px) formats grids into balanced 2 columns")

# Mobile 1-column layout
mobile_grid_ok = (
    "grid-template-columns: 1fr !important" in style_css and
    "max-width: 640px" in style_css
)
assert_test(mobile_grid_ok, "Mobile media query (<=640px) collapses grids to single column")

# ----------------------------------------------------------------------
# 3. Table Horizontal Overflow & Viewport Bleed Prevention
# ----------------------------------------------------------------------
print("\n[Suite 3: Table Horizontal Overflow & Viewport Bleed]")

assert_test(".comp-table-wrap" in style_css, ".comp-table-wrap class defined in CSS")
assert_test("overflow-x: auto" in style_css, ".comp-table-wrap has overflow-x: auto")

# Find all <table> tags and verify each is wrapped inside .comp-table-wrap
table_matches = list(re.finditer(r'<table[^>]*>', index_html))
assert_test(len(table_matches) >= 3, f"At least 3 tables exist in index.html (found {len(table_matches)})")

all_tables_wrapped = True
for idx, match in enumerate(table_matches):
    start_pos = match.start()
    lookback = index_html[max(0, start_pos - 600):start_pos]
    if "comp-table-wrap" not in lookback:
        all_tables_wrapped = False
        print(f"    Table {idx+1} at pos {start_pos} is NOT preceded by comp-table-wrap!")

assert_test(all_tables_wrapped, "All <table> elements in index.html are enclosed in overflow-x: auto wrapper (.comp-table-wrap)")

# Check html, body overflow-x hidden
body_overflow_ok = (
    "overflow-x: hidden" in style_css and
    "max-width: 100%" in style_css
)
assert_test(body_overflow_ok, "html, body enforces max-width: 100% and overflow-x: hidden to prevent viewport jitter")

# ----------------------------------------------------------------------
# 4. Japanese Kanji Typography & Metric Settings
# ----------------------------------------------------------------------
print("\n[Suite 4: Kanji Typography & Proportional Metrics]")

assert_test('font-feature-settings: "palt" 1' in style_css, "Japanese proportional glyph kerning ('palt' 1) enabled on body")
assert_test("letter-spacing: 0.01em" in style_css, "Japanese micro-letter-spacing (0.01em) configured")
assert_test("line-height: 1.7" in style_css, "Optimal Japanese kanji line-height (1.7) configured on body")
assert_test("font-size: 0.95rem" in style_css, "Minimum base font-size (0.95rem = 15.2px) satisfies readability threshold")
assert_test("'Noto Sans JP'" in style_css, "'Noto Sans JP' prioritized in font stack")

# Check .jp-num tabular figures
assert_test(".jp-num" in style_css, ".jp-num utility class defined")
assert_test("tabular-nums" in style_css, ".jp-num enforces tabular-nums for aligned financial tables")

# Check hub and article typography
assert_test('font-feature-settings: "palt" 1' in jp_hub_html, "jp/index.html enforces proportional kerning ('palt' 1)")
with open(jp_files[0], "r", encoding="utf-8") as f:
    sample_article = f.read()
assert_test('font-feature-settings: "palt" 1' in sample_article, "jp/*.html enforces proportional kerning ('palt' 1)")

# ----------------------------------------------------------------------
# 5. Dual-Theme Engine & Component CSS Rules
# ----------------------------------------------------------------------
print("\n[Suite 5: Dual-Theme Engine & Component CSS Rules]")

# 7 specialized classes + 2 VIP classes
fintech_classes = [
    "jp-preset-row", "jp-preset-btn", "jp-range-box", "jp-range-track",
    "jp-range-labels", "jp-mobile-bottom-nav", "jp-num", "vip-locked-row", "vip-exec-row"
]
for cls in fintech_classes:
    assert_test(f".{cls}" in style_css, f"Specialized fintech class '.{cls}' is declared in stylesheet")

# Check Dark theme root
assert_test(':root,' in style_css or ':root {' in style_css, ":root CSS variables defined")
assert_test('html[data-jp-theme="dark"]' in style_css, "Dark theme selector html[data-jp-theme='dark'] defined")

# Check Light theme selector
assert_test('html[data-jp-theme="light"]' in style_css, "Light theme selector html[data-jp-theme='light'] defined")

# Check theme toggle JS function
assert_test("function toggleJpTheme()" in index_html, "toggleJpTheme() function declared in index.html")
assert_test("btnToggleJpTheme" in index_html, "#btnToggleJpTheme toggle button present in DOM")
assert_test("setAttribute('data-jp-theme'" in index_html or 'setAttribute("data-jp-theme"' in index_html, "toggleJpTheme updates data-jp-theme attribute on root")

# ----------------------------------------------------------------------
# 6. Empirical WCAG 2.1 AA/AAA Contrast Mathematical Stress Test
# ----------------------------------------------------------------------
print("\n[Suite 6: WCAG 2.1 AA & AAA Contrast Mathematical Stress Test]")

def parse_hex(hex_str):
    h = hex_str.strip().lstrip('#')
    if len(h) == 3:
        h = ''.join([c*2 for c in h])
    return [int(h[i:i+2], 16) for i in (0, 2, 4)]

def srgb_to_linear(val):
    c = val / 255.0
    return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4

def relative_luminance(r, g, b):
    lr, lg, lb = srgb_to_linear(r), srgb_to_linear(g), srgb_to_linear(b)
    return 0.2126 * lr + 0.7152 * lg + 0.0722 * lb

def alpha_blend(fg_hex, bg_hex, alpha):
    f_r, f_g, f_b = parse_hex(fg_hex)
    b_r, b_g, b_b = parse_hex(bg_hex)
    o_r = int(round(f_r * alpha + b_r * (1.0 - alpha)))
    o_g = int(round(f_g * alpha + b_g * (1.0 - alpha)))
    o_b = int(round(f_b * alpha + b_b * (1.0 - alpha)))
    return f"#{o_r:02x}{o_g:02x}{o_b:02x}"

def contrast_ratio(hex1, hex2):
    r1, g1, b1 = parse_hex(hex1)
    r2, g2, b2 = parse_hex(hex2)
    l1 = relative_luminance(r1, g1, b1)
    l2 = relative_luminance(r2, g2, b2)
    return (max(l1, l2) + 0.05) / (min(l1, l2) + 0.05)

# Alpha-blended backgrounds in SEO articles
pale_mint_bg = alpha_blend("#10b981", "#ffffff", 0.12)
pale_rose_bg = alpha_blend("#f43f5e", "#ffffff", 0.12)

contrast_test_cases = [
    # Dark Theme Checks (index.html)
    ("Dark Mode: Text Main (#f8fafc) on Dark Bg (#06050c)", "#f8fafc", "#06050c", 7.0),
    ("Dark Mode: Text Muted (#cbd5e1) on Dark Bg (#06050c)", "#cbd5e1", "#06050c", 4.5),
    ("Dark Mode: Text Sub (#94a3b8) on Dark Bg (#06050c)", "#94a3b8", "#06050c", 4.5),
    ("Dark Mode: Text Main (#f8fafc) on Card Bg (#0e0b1a)", "#f8fafc", "#0e0b1a", 7.0),
    ("Dark Mode: Text Muted (#cbd5e1) on Card Bg (#0e0b1a)", "#cbd5e1", "#0e0b1a", 4.5),
    ("Dark Mode: Accent Violet (#a78bfa) on Dark Bg (#06050c)", "#a78bfa", "#06050c", 4.5),
    ("Dark Mode: Accent Amber (#fbbf24) on Dark Bg (#06050c)", "#fbbf24", "#06050c", 7.0),
    ("Dark Mode: Accent Sky (#38bdf8) on Dark Bg (#06050c)", "#38bdf8", "#06050c", 7.0),
    
    # Light Theme Checks (index.html)
    ("Light Mode: Text Main (#0b1f3a) on Light Bg (#f1f5f9)", "#0b1f3a", "#f1f5f9", 7.0),
    ("Light Mode: Text Muted (#334155) on Light Bg (#f1f5f9)", "#334155", "#f1f5f9", 4.5),
    ("Light Mode: Text Main (#0b1f3a) on Card Bg (#ffffff)", "#0b1f3a", "#ffffff", 7.0),
    ("Light Mode: Text Muted (#334155) on Card Bg (#ffffff)", "#334155", "#ffffff", 4.5),
    ("Light Mode: Text Sub (#475569) on Card Bg (#ffffff)", "#475569", "#ffffff", 4.5),
    ("Light Mode: Accent Violet (#6d28d9) on Card Bg (#ffffff)", "#6d28d9", "#ffffff", 4.5),
    ("Light Mode: Accent Amber (#b45309) on Card Bg (#ffffff)", "#b45309", "#ffffff", 4.5),
    ("Light Mode: Accent Rose (#be123c) on Card Bg (#ffffff)", "#be123c", "#ffffff", 4.5),
    ("Light Mode: Accent Sky (#0369a1) on Card Bg (#ffffff)", "#0369a1", "#ffffff", 4.5),
    ("Light Mode: Header Brand (#f8fafc) on Navy Header (#0b1f3a)", "#f8fafc", "#0b1f3a", 7.0),
    ("Light Mode: Tape Item (#e2e8f0) on Tape Bg (#102a4c)", "#e2e8f0", "#102a4c", 7.0),
    ("Light Mode: Comp Table Th (#ffffff) on Th Bg (#0b1f3a)", "#ffffff", "#0b1f3a", 7.0),
    ("Light Mode: Comp Table Td (#0f172a) on Td Bg (#ffffff)", "#0f172a", "#ffffff", 7.0),
    ("Light Mode: Legal Box Text (#475569) on Legal Bg (#f8fafc)", "#475569", "#f8fafc", 4.5),

    # Static SEO Articles & Hub (/jp/*.html and /jp/index.html)
    ("SEO Articles: Bullish Banner Text (#064e3b) on Mint Bg", "#064e3b", pale_mint_bg, 4.5),
    ("SEO Articles: Bullish Banner Text AAA check (req 7.0:1)", "#064e3b", pale_mint_bg, 7.0),
    ("SEO Articles: Avoid Banner Text (#881337) on Rose Bg", "#881337", pale_rose_bg, 4.5),
    ("SEO Articles: Avoid Banner Text AAA check (req 7.0:1)", "#881337", pale_rose_bg, 7.0),
    ("SEO Hub: Brand Link (#0b1f3a) on Hub Bg (#f4f6fa)", "#0b1f3a", "#f4f6fa", 7.0),
    ("SEO Hub: Subtitle (#334155) on Hub Bg (#f4f6fa)", "#334155", "#f4f6fa", 4.5),
    ("SEO Hub: Card Title (#0b1f3a) on Card Bg (#ffffff)", "#0b1f3a", "#ffffff", 7.0),
    ("SEO Hub: Card Score (#b45309) on Card Bg (#ffffff)", "#b45309", "#ffffff", 4.5),
    ("SEO Articles: Article Heading (#0b1f3a) on Card (#ffffff)", "#0b1f3a", "#ffffff", 7.0),
    ("SEO Articles: Article Body Text (#1e293b) on Card (#ffffff)", "#1e293b", "#ffffff", 7.0),
    ("SEO Articles: Research Links (#1d4ed8) on Card (#ffffff)", "#1d4ed8", "#ffffff", 4.5),
    ("SEO Articles: Mini Calc Header (#0b1f3a) on Calc Card (#f8fafc)", "#0b1f3a", "#f8fafc", 7.0),
    ("SEO Articles: KPI Price Label (#475569) on KPI Card (#f8fafc)", "#475569", "#f8fafc", 4.5),
    ("SEO Articles: KPI Price Value (#0b1f3a) on KPI Card (#f8fafc)", "#0b1f3a", "#f8fafc", 7.0),
]

for label, fg, bg, req_ratio in contrast_test_cases:
    cr = contrast_ratio(fg, bg)
    assert_test(cr >= req_ratio, f"{label} [{cr:.2f}:1 >= {req_ratio:.1f}:1]", f"Actual {cr:.2f}:1 < required {req_ratio:.1f}:1")

print("\n========================================================================")
print(f"Empirical Audit Finished: {passed_tests} Passed / {failed_tests} Failed")
print("========================================================================")

if failed_tests > 0:
    sys.exit(1)
sys.exit(0)
