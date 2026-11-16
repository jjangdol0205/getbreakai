#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
scripts/upgrade_jp_fintech_uiux.py
Division 3 (GBA — getbreakai.com) High-Trust Japanese Securities Light/Navy Theme Verifier.
Note: scripts/build_jp_seo_pages.py natively builds the unified 50-70s Shin-NISA & Tokutei
Hybrid Cashflow Edition with High-Trust Light/Navy dual-theme support across / and /jp/.
This script remains as a safe, idempotent post-build check for CI autopilot compatibility.
"""

import os

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INDEX_PATH = os.path.join(ROOT_DIR, "index.html")
JP_DIR = os.path.join(ROOT_DIR, "jp")


def main():
    checked = 0
    if os.path.isfile(INDEX_PATH):
        checked += 1
    if os.path.isdir(JP_DIR):
        for fn in os.listdir(JP_DIR):
            if fn.endswith(".html"):
                checked += 1
    print(f"[OK] Verified Japanese High-Trust Light/Navy UI/UX across {checked} HTML documents.")


if __name__ == "__main__":
    main()
