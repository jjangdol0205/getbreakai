"""
engine/pdf_compiler.py
Milestone 5: Strict 3-Page A4 Portrait HTML/SVG & PDF Compiler Pipeline
Compiles HTML with exact A4 vertical height budgeting, invokes headless Microsoft Edge/Chrome,
and programmatically verifies with PyMuPDF (len(doc) == 3, size > 50KB, y1 <= 838.0 pt).
"""

import os
import sys
import shutil
import pathlib
import subprocess
from datetime import datetime
from typing import Optional, Tuple
import pymupdf


# ---------------------------------------------------------------------------
# Global CSS Stylesheet for Strict A4 Portrait 3-Page Output
# ---------------------------------------------------------------------------
CSS_STYLES = """
@page {
    size: 210mm 297mm;
    margin: 0;
}
* {
    box-sizing: border-box;
    -webkit-print-color-adjust: exact;
    print-color-adjust: exact;
    word-break: keep-all;
    overflow-wrap: break-word;
}
html, body {
    margin: 0;
    padding: 0;
    width: 210mm;
    background: #ffffff;
    font-family: 'Pretendard', 'Malgun Gothic', 'Apple SD Gothic Neo', -apple-system, sans-serif;
    color: #0f172a;
    font-size: 7.8pt;
    line-height: 1.28;
    font-variant-numeric: tabular-nums;
}
.pdf-page {
    width: 210mm;
    height: 297mm;
    max-height: 297mm;
    padding: 5.5mm 7.5mm;
    overflow: hidden;
    page-break-after: always;
    break-after: page;
    box-sizing: border-box;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    background: #f8fafc;
    position: relative;
}
.pdf-page:last-of-type,
.pdf-page:nth-child(3) {
    page-break-after: avoid !important;
    break-after: avoid !important;
}
#page-1 {
    padding: 3.8mm 7.0mm;
}
#page-1 .page-header {
    padding: 3.5px 7px;
    margin-bottom: 2px;
}
#page-1 .exec-banner {
    gap: 4px;
    margin-bottom: 2px;
}
#page-1 .exec-card {
    padding: 3.5px 6px;
}
#page-1 .section-box {
    padding: 3.5px 6px;
    margin-bottom: 2px;
}
#page-1 .section-row {
    gap: 5px;
    margin-bottom: 2px;
}
#page-1 .section-title {
    margin-bottom: 2px;
    padding-bottom: 1.5px;
    font-size: 7.2pt;
}
#page-1 .report-table {
    font-size: 6.4pt;
    line-height: 1.15;
}
#page-1 .report-table th,
#page-1 .report-table td {
    padding: 1.6px 4px;
}
#page-1 .proxy-grid {
    gap: 3px;
    margin-bottom: 2.5px;
}
#page-1 .proxy-chip {
    padding: 1.8px 4px;
}
#page-1 .timing-reminder {
    padding: 2px 5px;
    margin-top: 2px;
    font-size: 6.1pt;
}
#page-1 .trig-grid {
    gap: 3px;
    margin-bottom: 2.5px;
}
#page-1 .trig-card {
    padding: 2px 4px;
}
#page-1 .news-list {
    gap: 2px;
}
#page-1 .news-item {
    padding: 2px 5px;
}
#page-1 .news-title {
    font-size: 6.3pt;
    line-height: 1.15;
}
#page-1 .news-kr {
    font-size: 5.9pt;
    line-height: 1.14;
}
#page-1 .news-action {
    font-size: 5.7pt;
}
#page-1 .killswitch-bar {
    padding: 2px 5px;
    margin-top: 2px;
}

/* Institutional Dark-Navy Page Header & Footer */
.page-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
    color: #ffffff;
    padding: 5px 8px;
    border-radius: 5px;
    margin-bottom: 4px;
    box-shadow: 0 1px 3px rgba(15, 23, 42, 0.12);
    gap: 6px;
}
.header-left {
    display: flex;
    align-items: center;
    gap: 5px;
    min-width: 0;
    flex: 1;
}
.header-tag {
    background: #3b82f6;
    color: #ffffff;
    font-size: 6.4pt;
    font-weight: 800;
    padding: 2px 5px;
    border-radius: 3px;
    white-space: nowrap;
}
.header-date-pill {
    background: #fbbf24;
    color: #0f172a;
    font-size: 6.4pt;
    font-weight: 800;
    padding: 2px 5px;
    border-radius: 3px;
    white-space: nowrap;
}
.header-title {
    margin: 0;
    font-size: 8.1pt;
    font-weight: 800;
    color: #ffffff;
    letter-spacing: -0.3px;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
}
.header-right {
    display: flex;
    align-items: center;
    gap: 4px;
    white-space: nowrap;
    flex-shrink: 0;
}
.badge-source {
    background: rgba(255, 255, 255, 0.12);
    color: #e2e8f0;
    border: 1px solid rgba(255, 255, 255, 0.24);
    font-size: 5.9pt;
    font-weight: 700;
    padding: 2px 5px;
    border-radius: 3px;
    white-space: nowrap;
}
.page-footer {
    display: flex;
    justify-content: space-between;
    align-items: center;
    border-top: 1.5px solid #cbd5e1;
    padding-top: 3px;
    font-size: 6.5pt;
    font-weight: 600;
    color: #475569;
    margin-top: 2px;
}

/* Executive Action Banner */
.exec-banner {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 6px;
    margin-bottom: 4px;
}
.exec-card {
    border-radius: 5px;
    padding: 5px 8px;
    border: 1px solid #cbd5e1;
    border-left-width: 4px;
    background: #ffffff;
}
.card-good {
    background: #f0fdf4;
    border-color: #86efac;
    border-left-color: #16a34a;
}
.card-wait {
    background: #fffbeb;
    border-color: #fde68a;
    border-left-color: #d97706;
}
.card-warn {
    background: #fef2f2;
    border-color: #fecaca;
    border-left-color: #dc2626;
}
.exec-card-title {
    font-size: 7pt;
    font-weight: 800;
    color: #334155;
    display: flex;
    align-items: center;
    gap: 4px;
    margin-bottom: 2px;
    white-space: nowrap;
}
.exec-card-status {
    font-size: 8.6pt;
    font-weight: 900;
    color: #0f172a;
    margin-bottom: 2px;
    white-space: nowrap;
}
.exec-card-sub {
    font-size: 6.4pt;
    color: #475569;
    line-height: 1.22;
}

/* Sections & Boxes */
.section-box {
    background: #ffffff;
    border: 1px solid #cbd5e1;
    border-radius: 5px;
    padding: 5px 7px;
    margin-bottom: 4px;
    box-shadow: 0 1px 2px rgba(15, 23, 42, 0.03);
    overflow: hidden;
}
.section-row {
    display: flex;
    gap: 6px;
    margin-bottom: 4px;
}
.col-half {
    flex: 1;
    min-width: 0;
    margin-bottom: 0 !important;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
}
.section-title {
    display: flex;
    justify-content: space-between;
    align-items: center;
    font-size: 7.6pt;
    font-weight: 800;
    color: #0f172a;
    margin-bottom: 4px;
    border-bottom: 1.5px solid #e2e8f0;
    padding-bottom: 2.5px;
    gap: 4px;
}
.section-title > span:first-child {
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
}
.section-badge {
    font-size: 6.1pt;
    font-weight: 700;
    color: #1e293b;
    background: #f1f5f9;
    border: 1px solid #cbd5e1;
    padding: 1px 5px;
    border-radius: 3px;
    white-space: nowrap;
    flex-shrink: 0;
}

/* Tables */
.report-table {
    width: 100%;
    border-collapse: collapse;
    font-size: 6.9pt;
    line-height: 1.22;
}
.report-table th {
    background: #f1f5f9;
    color: #334155;
    font-weight: 800;
    border: 1px solid #cbd5e1;
    padding: 3px 5px;
    text-align: left;
    white-space: nowrap;
}
.report-table td {
    border: 1px solid #e2e8f0;
    padding: 2.5px 5px;
    color: #0f172a;
}
.report-table tbody tr:nth-child(even) {
    background: #f8fafc;
}
.compact-table th, .compact-table td {
    padding: 2.2px 4px;
}
.row-highlight {
    background: #ecfdf5 !important;
}
.td-sub {
    font-size: 6.2pt;
    color: #475569;
    font-weight: 600;
}

/* Color & Pill Classes */
.chg-up {
    color: #dc2626;
    font-weight: 700;
}
.chg-down {
    color: #2563eb;
    font-weight: 700;
}
.proxy-chg {
    font-size: 6.4pt;
    font-weight: 800;
    padding: 0.5px 4px;
    border-radius: 3px;
    white-space: nowrap;
}
.chg-up-pill {
    background: #fee2e2;
    color: #b91c1c;
}
.chg-down-pill {
    background: #dbeafe;
    color: #1d4ed8;
}
.badge {
    display: inline-block;
    padding: 1px 5px;
    border-radius: 3px;
    font-size: 6.3pt;
    font-weight: 800;
    white-space: nowrap;
}
.badge-good {
    background: #dcfce7;
    color: #15803d;
    border: 1px solid #86efac;
}
.badge-wait {
    background: #fef3c7;
    color: #b45309;
    border: 1px solid #fde68a;
}
.badge-warn {
    background: #fee2e2;
    color: #b91c1c;
    border: 1px solid #fca5a5;
}
.badge-neutral {
    background: #e2e8f0;
    color: #1e293b;
    border: 1px solid #cbd5e1;
}
.badge-oversold {
    background: #fee2e2;
    color: #dc2626;
    border: 1px solid #f87171;
    font-weight: 800;
}

/* 2-Row Clean Proxy Chips Grid */
.proxy-grid {
    display: grid;
    grid-template-columns: repeat(5, 1fr);
    gap: 4px;
    margin-bottom: 4px;
}
.proxy-chip {
    background: #f8fafc;
    border: 1px solid #cbd5e1;
    border-radius: 4px;
    padding: 2.5px 5px;
    display: flex;
    flex-direction: column;
    gap: 1.5px;
}
.proxy-top {
    display: flex;
    justify-content: space-between;
    align-items: center;
    white-space: nowrap;
}
.proxy-bot {
    display: flex;
    justify-content: space-between;
    align-items: center;
    white-space: nowrap;
}
.proxy-tag {
    font-size: 5.6pt;
    font-weight: 700;
    color: #475569;
}
.proxy-tk {
    font-size: 6.2pt;
    font-weight: 900;
    color: #0f172a;
    letter-spacing: -0.2px;
}
.proxy-val {
    font-size: 6.6pt;
    font-weight: 700;
    color: #334155;
}

/* Timing Reminder Bar */
.timing-reminder {
    background: #fffbeb;
    border: 1px solid #fcd34d;
    border-radius: 4px;
    padding: 3px 6px;
    font-size: 6.4pt;
    color: #78350f;
    margin-top: 3px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 5px;
}
.timing-badge {
    background: #fde68a;
    color: #78350f;
    font-weight: 800;
    padding: 1px 5px;
    border-radius: 3px;
    white-space: nowrap;
}
.winrate-badge {
    background: #dcfce7;
    color: #166534;
    border: 1px solid #86efac;
    font-weight: 800;
    padding: 1px 5px;
    border-radius: 3px;
    white-space: nowrap;
}

/* Gauges & Non-Overlapping Summary Pill */
.gauge-container {
    width: 100%;
    margin: 1px 0;
}
.svg-gauge {
    width: 100%;
    height: auto;
    display: block;
}
.gauge-current-pill {
    background: #eff6ff;
    border: 1px solid #bfdbfe;
    border-radius: 4px;
    padding: 2.5px 6px;
    font-size: 6.4pt;
    color: #1e3a8a;
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin: 2px 0;
    white-space: nowrap;
}
.target-notes {
    font-size: 6.3pt;
    color: #334155;
    line-height: 1.25;
    margin-top: 2px;
}

/* 8 Triggers Grid */
.trig-grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 4px;
    margin-bottom: 4px;
}
.trig-card {
    background: #f8fafc;
    border: 1px solid #cbd5e1;
    border-radius: 4px;
    padding: 2.5px 5px;
}
.trig-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 1.5px;
}
.trig-id {
    font-size: 6pt;
    font-weight: 800;
    color: #475569;
}
.trig-badge {
    font-size: 5.8pt;
    font-weight: 800;
    padding: 0.5px 4px;
    border-radius: 2px;
    white-space: nowrap;
}
.trig-name {
    font-size: 6.7pt;
    font-weight: 800;
    color: #0f172a;
    white-space: nowrap;
}
.trig-metric {
    font-size: 6.5pt;
    font-weight: 800;
    color: #1d4ed8;
    white-space: nowrap;
}
.trig-sub {
    font-size: 5.7pt;
    font-weight: 500;
    color: #64748b;
}

/* Curated News Items */
.news-wrap {
    margin-top: 3px;
}
.news-header-label {
    font-size: 7pt;
    font-weight: 800;
    color: #0f172a;
    margin-bottom: 2.5px;
}
.news-list {
    display: flex;
    flex-direction: column;
    gap: 3px;
}
.news-item {
    background: #f8fafc;
    border: 1px solid #cbd5e1;
    border-left: 3.5px solid #2563eb;
    border-radius: 4px;
    padding: 3px 6px;
}
.news-meta {
    display: flex;
    align-items: center;
    gap: 5px;
    margin-bottom: 1px;
}
.news-origin {
    font-size: 6.2pt;
    font-weight: 800;
    color: #1d4ed8;
}
.news-badge {
    font-size: 5.9pt;
    font-weight: 800;
    padding: 0.5px 4px;
    border-radius: 2px;
}
.news-title {
    font-size: 6.7pt;
    font-weight: 800;
    color: #0f172a;
    line-height: 1.2;
}
.news-kr {
    font-size: 6.3pt;
    color: #334155;
    line-height: 1.2;
    margin-top: 1px;
}
.news-action {
    font-size: 6pt;
    color: #047857;
    font-weight: 700;
    margin-top: 1px;
}

/* Kill Switch Bar */
.killswitch-bar {
    background: #fef2f2;
    border: 1px solid #fecaca;
    border-radius: 4px;
    padding: 3px 6px;
    font-size: 6.3pt;
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 6px;
    margin-top: 3px;
    white-space: nowrap;
}
.ks-title {
    font-weight: 800;
    color: #b91c1c;
    white-space: nowrap;
}
.ks-item {
    white-space: nowrap;
}
.ks-item strong {
    color: #0f172a;
}

/* Page 2 Specific */
.osc-prohibition-note {
    background: #f1f5f9;
    border-left: 3.5px solid #475569;
    border-radius: 3px;
    padding: 4px 7px;
    font-size: 6.5pt;
    color: #1e293b;
    margin-top: 4px;
    line-height: 1.3;
}
.band-status-text {
    font-size: 6.5pt;
    color: #334155;
    line-height: 1.3;
    margin-top: 2px;
}
.tilt-desc {
    font-size: 6.4pt;
    color: #334155;
    line-height: 1.32;
    margin-top: 2px;
}
.corr-container {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 5px;
    margin-bottom: 4px;
}
.corr-card {
    background: #f8fafc;
    border: 1px solid #cbd5e1;
    border-radius: 4px;
    padding: 5px 4px;
    text-align: center;
}
.corr-val {
    font-size: 11.5pt;
    font-weight: 900;
    line-height: 1.1;
    margin-bottom: 2px;
}
.corr-lbl {
    font-size: 6.4pt;
    font-weight: 800;
    color: #0f172a;
    margin-bottom: 1px;
}
.corr-sub {
    font-size: 5.8pt;
    color: #475569;
    line-height: 1.2;
}
.corr-summary {
    font-size: 6.4pt;
    color: #1e293b;
    background: #f1f5f9;
    border: 1px solid #e2e8f0;
    padding: 4px 6px;
    border-radius: 4px;
    line-height: 1.3;
}
.holdings-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 5px;
    margin-bottom: 5px;
}
.holding-card {
    background: #f8fafc;
    border: 1px solid #cbd5e1;
    border-radius: 4px;
    padding: 4px 6px;
}
.holding-top {
    display: flex;
    justify-content: space-between;
    align-items: center;
    font-size: 6.8pt;
    margin-bottom: 2px;
    white-space: nowrap;
}
.holding-tk {
    font-weight: 900;
    color: #0f172a;
}
.holding-name {
    font-size: 6.2pt;
    font-weight: 600;
    color: #475569;
    margin-left: 2px;
}
.holding-weight {
    font-size: 5.8pt;
    font-weight: 700;
    background: #e2e8f0;
    color: #334155;
    padding: 1px 4px;
    border-radius: 2px;
}
.holding-driver {
    font-size: 6.2pt;
    color: #334155;
    line-height: 1.25;
}

/* Page 3 Specific */
.discipline-banner {
    border-radius: 5px;
    padding: 4px 8px;
    margin-bottom: 2px;
    display: flex;
    align-items: center;
    gap: 8px;
}
.banner-active {
    background: #fffbeb;
    border: 1.5px solid #fbbf24;
    border-left: 5px solid #d97706;
}
.banner-buy {
    background: #f0fdf4;
    border: 1.5px solid #4ade80;
    border-left: 5px solid #16a34a;
}
.banner-icon {
    font-size: 14pt;
    line-height: 1;
}
.banner-title {
    font-size: 7.8pt;
    font-weight: 900;
    color: #0f172a;
    margin-bottom: 1px;
}
.banner-body {
    font-size: 6.3pt;
    color: #334155;
    line-height: 1.25;
}
.switch-verdict-box {
    border-radius: 4px;
    padding: 4px 7px;
    margin-bottom: 4px;
}
.switch-verdict-hold {
    background: #fefce8;
    border: 1px solid #fde047;
    border-left: 4px solid #ca8a04;
}
.switch-verdict-caution {
    background: #fff7ed;
    border: 1px solid #fdba74;
    border-left: 4px solid #ea580c;
}
.switch-verdict-go {
    background: #ecfdf5;
    border: 1px solid #6ee7b7;
    border-left: 4px solid #059669;
}
.switch-verdict-title {
    font-size: 7.2pt;
    font-weight: 900;
    color: #0f172a;
    margin-bottom: 1.5px;
}
.switch-verdict-desc {
    font-size: 6.2pt;
    color: #334155;
    line-height: 1.26;
}
.switch-matrix-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 4px;
}
.switch-matrix-card {
    background: #f8fafc;
    border: 1px solid #cbd5e1;
    border-radius: 4px;
    padding: 3.5px 5px;
}
.matrix-active {
    background: #eff6ff;
    border: 1.5px solid #3b82f6;
}
.matrix-hdr {
    font-size: 6.2pt;
    font-weight: 800;
    color: #1e293b;
    margin-bottom: 1.5px;
    border-bottom: 1px dashed #cbd5e1;
    padding-bottom: 1px;
}
.matrix-body {
    font-size: 5.9pt;
    color: #334155;
    line-height: 1.24;
}
.survival-grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 4px;
}
.surv-card {
    background: #f8fafc;
    border: 1px solid #cbd5e1;
    border-radius: 4px;
    padding: 3.5px 5px;
}
.surv-badge {
    font-size: 6.2pt;
    font-weight: 800;
    padding: 1px 4px;
    border-radius: 3px;
    display: inline-block;
}
.badge-stop { background: #fee2e2; color: #b91c1c; }
.badge-time { background: #fef3c7; color: #b45309; }
.badge-switch { background: #e0e7ff; color: #3730a3; }
.badge-tp { background: #dcfce7; color: #166534; }
.surv-body {
    font-size: 6.0pt;
    color: #334155;
    line-height: 1.24;
    margin-top: 2px;
}
.ticker-badge {
    background: #0f172a;
    color: #ffffff;
    font-size: 6.8pt;
    font-weight: 800;
    padding: 1.5px 4px;
    border-radius: 3px;
}
.ticker-name {
    font-size: 7pt;
    font-weight: 800;
    color: #0f172a;
    margin-left: 3px;
}
.growth-tier {
    font-size: 6pt;
    font-weight: 800;
    padding: 1px 3px;
    border-radius: 2px;
    margin-left: 3px;
}
.tier-aplus { background: #fee2e2; color: #b91c1c; }
.tier-a { background: #e0e7ff; color: #3730a3; }
.tier-b { background: #f1f5f9; color: #475569; }
.score-pill {
    background: #1d4ed8;
    color: #ffffff;
    font-size: 7pt;
    font-weight: 800;
    padding: 1.5px 5px;
    border-radius: 3px;
}
.delta-badge {
    font-size: 6pt;
    font-weight: 700;
    padding: 1px 3px;
    border-radius: 2px;
    margin-left: 2px;
}
.delta-up { background: #dcfce7; color: #166534; }
.delta-down { background: #fee2e2; color: #b91c1c; }
.delta-zero { background: #f1f5f9; color: #64748b; }
.stage-badge {
    font-size: 6.3pt;
    font-weight: 800;
    padding: 1.5px 5px;
    border-radius: 3px;
}
.stage-buy { background: #dcfce7; color: #15803d; border: 1px solid #86efac; }
.stage-ready { background: #fef3c7; color: #b45309; border: 1px solid #fde68a; }
.cond-chip {
    display: inline-block;
    margin: 0 1px;
    font-weight: 700;
}
.cond-legend {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 4px;
    background: #f1f5f9;
    border: 1px solid #e2e8f0;
    border-radius: 3px;
    padding: 3px 6px;
    font-size: 6pt;
    color: #334155;
    margin-top: 4px;
}

/* Spotlight Deep-Dive Cards */
.spotlight-wrap {
    display: flex;
    flex-direction: column;
    gap: 5px;
}
.spotlight-card {
    background: #f8fafc;
    border: 1px solid #cbd5e1;
    border-left: 4px solid #2563eb;
    border-radius: 4px;
    padding: 5px 7px;
}
.spotlight-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    border-bottom: 1px solid #cbd5e1;
    padding-bottom: 3px;
    margin-bottom: 4px;
}
.spotlight-rank {
    background: #1d4ed8;
    color: #ffffff;
    font-size: 6.4pt;
    font-weight: 800;
    padding: 1.5px 5px;
    border-radius: 3px;
}
.spotlight-title {
    font-size: 7.8pt;
    font-weight: 900;
    color: #0f172a;
}
.spotlight-score {
    font-size: 6.6pt;
    font-weight: 700;
    color: #334155;
}
.spotlight-body {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 5px;
}
.spotlight-col {
    background: #ffffff;
    border: 1px solid #e2e8f0;
    border-radius: 3px;
    padding: 4px 5px;
}
.spotlight-col-plan {
    background: #eff6ff;
    border-color: #bfdbfe;
}
.col-title {
    font-size: 6.4pt;
    font-weight: 800;
    color: #0f172a;
    margin-bottom: 2px;
    border-bottom: 1px dashed #e2e8f0;
    padding-bottom: 1.5px;
}
.col-text {
    font-size: 6.3pt;
    color: #334155;
    line-height: 1.3;
}

/* Value Trap Firewall Notice */
.firewall-notice {
    background: #fef2f2;
    border: 1px solid #fecaca;
    border-left: 4px solid #dc2626;
    border-radius: 4px;
    padding: 4px 7px;
    font-size: 6.4pt;
    color: #991b1b;
    margin-top: 2px;
    line-height: 1.28;
}
.firewall-badge {
    font-weight: 800;
}
"""


def build_full_html_report(
    page1_html: str,
    page2_html: str,
    page3_html: str,
    report_date: Optional[str] = None,
) -> str:
    """Combines 3 pages into complete HTML document adhering strictly to A4 portrait."""
    dt_str = report_date or datetime.now().strftime("%Y-%m-%d")
    return f"""<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <title>[{dt_str}] 08:10 KST 모닝 알파 &amp; 코어 전략 리포트 (Morning Alpha Briefing)</title>
    <style>
        {CSS_STYLES}
    </style>
</head>
<body>
    {page1_html}
    {page2_html}
    {page3_html}
</body>
</html>
"""


def find_browser_executable() -> Optional[str]:
    """Finds installed Microsoft Edge or Google Chrome executable on Windows."""
    candidates = [
        r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
        r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
        r"C:\Program Files\Google\Chrome\Application\chrome.exe",
        r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
    ]
    for p in candidates:
        if os.path.exists(p):
            return p
    for name in ["msedge", "chrome"]:
        w = shutil.which(name)
        if w:
            return w
    return None


def compile_html_to_pdf(html_path: str, pdf_path: str) -> bool:
    """
    Compiles HTML file to PDF using headless Microsoft Edge/Chrome.
    Generates exact A4 vector PDF with --no-pdf-header-footer.
    """
    browser_exe = find_browser_executable()
    if not browser_exe:
        raise RuntimeError("No headless browser (Edge/Chrome) found on system.")

    html_path_obj = pathlib.Path(html_path).resolve()
    pdf_path_obj = pathlib.Path(pdf_path).resolve()
    html_uri = html_path_obj.as_uri()
    pdf_abs = str(pdf_path_obj)

    cmd = [
        browser_exe,
        "--headless=new",
        "--disable-gpu",
        "--no-pdf-header-footer",
        f"--print-to-pdf={pdf_abs}",
        html_uri,
    ]

    try:
        res = subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=25)
        if res.returncode == 0 and os.path.exists(pdf_abs) and os.path.getsize(pdf_abs) > 1000:
            return True
    except Exception as e:
        print(f"[PDF Compiler] Browser compilation error: {e}")

    return False


def verify_pdf_with_pymupdf(pdf_path: str) -> Tuple[bool, str]:
    """
    Programmatically verifies compiled PDF using PyMuPDF (fitz):
      1. len(doc) == 3 (strictly 3 pages)
      2. File size > 50,000 bytes (> 50 KB)
      3. A4 dimensions: 595.28 x 841.89 pt (tolerance ±3.0 pt)
      4. Zero bottom text clipping: y1 <= 838.0 pt for all text blocks
    """
    if not os.path.exists(pdf_path):
        return False, f"PDF file does not exist: {pdf_path}"

    size = os.path.getsize(pdf_path)
    if size <= 50_000:
        return False, f"PDF file size too small: {size} bytes <= 50,000 bytes"

    doc = pymupdf.open(pdf_path)
    try:
        num_pages = len(doc)
        if num_pages != 3:
            return False, f"Page count violation: expected strictly 3 pages, found {num_pages}"

        for i, page in enumerate(doc):
            rect = page.rect
            if abs(rect.width - 595.28) > 3.5:
                return False, f"Page {i+1} width mismatch: {rect.width} != 595.28 pt"
            if abs(rect.height - 841.89) > 3.5:
                return False, f"Page {i+1} height mismatch: {rect.height} != 841.89 pt"

            blocks = page.get_text("blocks")
            if not blocks:
                return False, f"Page {i+1} has no text content"

            for b in blocks:
                y1 = b[3]
                if y1 > 838.0:
                    return False, f"Page {i+1} text block clipped at bottom: y1={y1:.2f} > 838.0 pt. Content: {b[4][:30]}..."
    finally:
        doc.close()

    return True, "Verification passed: Strictly 3 pages, size > 50KB, zero clipping."
