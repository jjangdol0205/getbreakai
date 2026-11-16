#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
scripts/build_jp_index_html.py
Delegates root /index.html and /jp/index.html generation to scripts/build_jp_seo_pages.py
so both / and /jp/ stay 100% unified on the Japanese 50-70s Shin-NISA & Tokutei Hybrid Cashflow Edition.
"""

from build_jp_seo_pages import main

if __name__ == "__main__":
    main()
