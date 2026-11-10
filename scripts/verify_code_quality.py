#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GetBreakAI (Division 3) — Code Quality, Link Integrity & Build Validator
Validates:
  1. JavaScript syntax (node --check on all .js files)
  2. Python syntax (py_compile on all .py files)
  3. HTML link & anchor integrity across index.html, confirmation.html, jp/index.html, jp/confirmation.html, jp/*.html
  4. JSON schema & validity on all data .json files
  5. Build verification (--build / --check-build): static assets, snapshot sync, sitemap coverage
"""

import sys
import os
import glob
import json
import argparse
import subprocess
import py_compile
import urllib.parse
from html.parser import HTMLParser

# Configure UTF-8 stdout for consistent reporting
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

EXCLUDE_DIRS = {'.git', 'node_modules', '.agents', '__pycache__', 'dist', 'dist-global', '.vscode'}


def find_files_by_extension(extension):
    """Recursively discover files matching extension, ignoring excluded directories."""
    matched = []
    for root, dirs, files in os.walk(PROJECT_ROOT):
        dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS]
        for f in files:
            if f.endswith(extension):
                matched.append(os.path.join(root, f))
    return sorted(matched)


# =====================================================================
# 1. JavaScript Syntax Validator
# =====================================================================
def validate_javascript():
    print("\n" + "=" * 72)
    print(" [1/4] JavaScript Syntax Validation (node --check)")
    print("=" * 72)
    js_files = find_files_by_extension('.js')
    if not js_files:
        print("  ⚠️ No JavaScript files found to validate.")
        return 0, 0

    passed = 0
    failed = 0
    for path in js_files:
        rel = os.path.relpath(path, PROJECT_ROOT).replace('\\', '/')
        res = subprocess.run(['node', '--check', path], capture_output=True, text=True)
        if res.returncode == 0:
            print(f"  ✓ [PASS] JS Syntax: {rel}")
            passed += 1
        else:
            print(f"  ✗ [FAIL] JS Syntax: {rel}")
            print(f"     Error: {res.stderr.strip()[:200]}")
            failed += 1

    print(f"  --> JS Summary: {passed} passed, {failed} failed (Total: {len(js_files)})")
    return passed, failed


# =====================================================================
# 2. Python Syntax Validator
# =====================================================================
def validate_python():
    print("\n" + "=" * 72)
    print(" [2/4] Python Syntax Validation (py_compile)")
    print("=" * 72)
    py_files = find_files_by_extension('.py')
    if not py_files:
        print("  ⚠️ No Python files found to validate.")
        return 0, 0

    passed = 0
    failed = 0
    for path in py_files:
        rel = os.path.relpath(path, PROJECT_ROOT).replace('\\', '/')
        try:
            py_compile.compile(path, doraise=True)
            print(f"  ✓ [PASS] PY Syntax: {rel}")
            passed += 1
        except py_compile.PyCompileError as e:
            print(f"  ✗ [FAIL] PY Syntax: {rel}")
            print(f"     Error: {e}")
            failed += 1

    print(f"  --> PY Summary: {passed} passed, {failed} failed (Total: {len(py_files)})")
    return passed, failed


# =====================================================================
# 3. HTML Link & Anchor Integrity Validator
# =====================================================================
class HTMLLinkCollector(HTMLParser):
    def __init__(self):
        super().__init__()
        self.ids = set()
        self.links = []

    def handle_starttag(self, tag, attrs):
        attr_dict = dict(attrs)
        if 'id' in attr_dict and attr_dict['id']:
            self.ids.add(attr_dict['id'].strip())
        for attr in ['href', 'src']:
            if attr in attr_dict and attr_dict[attr]:
                self.links.append((tag, attr, attr_dict[attr].strip()))


def validate_html_link_integrity():
    print("\n" + "=" * 72)
    print(" [3/4] HTML Link & Anchor Integrity Validation")
    print("=" * 72)

    # Required target HTML files
    target_files = ['index.html', 'confirmation.html', 'jp/index.html', 'jp/confirmation.html']
    jp_articles = glob.glob(os.path.join(PROJECT_ROOT, 'jp', '*.html'))
    for jpa in jp_articles:
        rel = os.path.relpath(jpa, PROJECT_ROOT).replace('\\', '/')
        if rel not in target_files:
            target_files.append(rel)
    target_files = sorted(list(set(target_files)))

    # Parse all HTML files first
    parsed_docs = {}
    missing_docs = []
    for rel in target_files:
        full_path = os.path.join(PROJECT_ROOT, rel)
        if not os.path.isfile(full_path):
            missing_docs.append(rel)
            continue
        try:
            with open(full_path, 'r', encoding='utf-8') as f:
                content = f.read()
            collector = HTMLLinkCollector()
            collector.feed(content)
            norm_rel = os.path.normpath(rel).replace('\\', '/')
            parsed_docs[norm_rel] = (collector.ids, collector.links)
        except Exception as err:
            print(f"  ✗ [FAIL] Error reading {rel}: {err}")
            missing_docs.append(rel)

    if missing_docs:
        print(f"  ✗ [FAIL] Missing required HTML documents: {missing_docs}")

    # Now validate all collected links
    total_links_checked = 0
    errors = []

    for rel_path, (doc_ids, doc_links) in parsed_docs.items():
        doc_dir = os.path.dirname(rel_path) or '.'

        for tag, attr, raw_link in doc_links:
            # Skip non-navigational or external non-getbreakai schemes
            if raw_link.startswith(('mailto:', 'tel:', 'javascript:', 'data:', 'chrome:')):
                continue

            # Strip canonical domain if present (e.g. https://getbreakai.com/#pricing)
            normalized_link = raw_link
            if normalized_link.startswith(('https://getbreakai.com/', 'http://getbreakai.com/')):
                normalized_link = '/' + normalized_link.split('getbreakai.com/')[1]
            elif normalized_link in ('https://getbreakai.com', 'http://getbreakai.com'):
                normalized_link = '/'

            # External third-party links (skip)
            if normalized_link.startswith(('http://', 'https://', '//')):
                continue

            total_links_checked += 1
            parsed = urllib.parse.urlparse(normalized_link)
            path_part = parsed.path
            fragment_part = parsed.fragment

            # Case A: Same-page internal anchor (e.g. #pricing, #vip-vault)
            if not path_part and fragment_part:
                if fragment_part not in doc_ids:
                    errors.append(f"Broken anchor in {rel_path}: #{fragment_part} (tag <{tag} {attr}=\"{raw_link}\">)")
                continue

            # Case B: Local relative or absolute path reference
            if path_part:
                if path_part.startswith('/'):
                    target_rel = path_part.lstrip('/')
                else:
                    target_rel = os.path.normpath(os.path.join(doc_dir, path_part)).replace('\\', '/')

                # Resolve root or folder default index.html
                if target_rel in ('', '.'):
                    target_rel = 'index.html'
                elif os.path.isdir(os.path.join(PROJECT_ROOT, target_rel)):
                    target_rel = os.path.normpath(os.path.join(target_rel, 'index.html')).replace('\\', '/')

                target_full = os.path.join(PROJECT_ROOT, target_rel)
                if not os.path.exists(target_full):
                    errors.append(f"Missing referenced file in {rel_path}: '{raw_link}' -> resolved '{target_rel}'")
                elif fragment_part:
                    norm_target = os.path.normpath(target_rel).replace('\\', '/')
                    if norm_target in parsed_docs:
                        target_ids = parsed_docs[norm_target][0]
                        if fragment_part not in target_ids:
                            errors.append(f"Broken anchor in {rel_path} -> {norm_target}: #{fragment_part} (from '{raw_link}')")

    if not errors and not missing_docs:
        print(f"  ✓ [PASS] All {len(parsed_docs)} HTML documents parsed cleanly.")
        print(f"  ✓ [PASS] Validated {total_links_checked} internal anchors and file references with 0 broken targets.")
        return len(parsed_docs), 0
    else:
        for err in errors:
            print(f"  ✗ [FAIL] {err}")
        return len(parsed_docs) - len(errors), len(errors) + len(missing_docs)


# =====================================================================
# 4. JSON Data Validity Validator
# =====================================================================
def validate_json_files():
    print("\n" + "=" * 72)
    print(" [4/4] JSON Data & Configuration Validation")
    print("=" * 72)
    json_files = find_files_by_extension('.json')
    if not json_files:
        print("  ⚠️ No JSON files found to validate.")
        return 0, 0

    passed = 0
    failed = 0
    for path in json_files:
        rel = os.path.relpath(path, PROJECT_ROOT).replace('\\', '/')
        try:
            with open(path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            # Ensure not empty
            if data is None or (isinstance(data, (dict, list)) and len(data) == 0):
                print(f"  ✗ [FAIL] JSON Empty: {rel}")
                failed += 1
            else:
                entry_count = len(data) if isinstance(data, (dict, list)) else 1
                print(f"  ✓ [PASS] JSON Valid: {rel} ({entry_count} top-level entries)")
                passed += 1
        except Exception as e:
            print(f"  ✗ [FAIL] JSON Malformed: {rel} -> {e}")
            failed += 1

    print(f"  --> JSON Summary: {passed} passed, {failed} failed (Total: {len(json_files)})")
    return passed, failed


# =====================================================================
# 5. Build Verification (Static Assets & Market Snapshot Synchronization)
# =====================================================================
def validate_build():
    print("\n" + "=" * 72)
    print(" [BUILD] Static Asset Integrity & Live Snapshot Synchronization Check")
    print("=" * 72)

    required_assets = [
        'index.html',
        'confirmation.html',
        'jp/index.html',
        'jp/confirmation.html',
        'robots.txt',
        'sitemap.xml',
        'favicon.svg',
        'og-preview.png',
        'CNAME',
        'package.json',
        'data/live_market_snapshot.json'
    ]

    # Required 30 Japanese SEO articles
    expected_articles = 30
    jp_articles = glob.glob(os.path.join(PROJECT_ROOT, 'jp', '*.html'))
    # Filter out index and confirmation
    research_articles = [p for p in jp_articles if not (p.endswith('index.html') or p.endswith('confirmation.html'))]

    errors = []

    # 1. Check all required assets exist and have non-zero size
    for asset in required_assets:
        full_path = os.path.join(PROJECT_ROOT, asset)
        if not os.path.isfile(full_path):
            errors.append(f"Required static asset missing: {asset}")
        else:
            size = os.path.getsize(full_path)
            if size == 0:
                errors.append(f"Required static asset is empty (0 bytes): {asset}")
            else:
                print(f"  ✓ [PASS] Asset exists & non-empty: {asset} ({size:,} bytes)")

    # 2. Check 30 JP SEO articles
    if len(research_articles) < expected_articles:
        errors.append(f"Expected at least {expected_articles} Japanese research articles in jp/*.html, found {len(research_articles)}")
    else:
        print(f"  ✓ [PASS] Japanese Research Reports verified: {len(research_articles)} articles present in /jp/")

    # 3. Check live_market_snapshot.json schema and synchronization
    snapshot_path = os.path.join(PROJECT_ROOT, 'data', 'live_market_snapshot.json')
    try:
        with open(snapshot_path, 'r', encoding='utf-8') as f:
            snapshot = json.load(f)

        # Check indices
        indices = snapshot.get('indices', {})
        for idx in ['^N225', '^TOPX']:
            if idx not in indices:
                errors.append(f"Snapshot missing index benchmark: {idx}")
            else:
                item = indices[idx]
                if not (item.get('price') and item.get('donchian_20d_high') and item.get('atr_14d')):
                    errors.append(f"Index benchmark {idx} missing essential quant fields")

        # Check flagship TSE Prime and US Tech tickers
        tickers = snapshot.get('tickers', {})
        expected_tse = ['8035.T', '6857.T', '9984.T', '7203.T', '6758.T']
        expected_us = ['NVDA', 'PLTR', 'TSLA', 'META']

        for sym in expected_tse:
            if sym not in tickers:
                errors.append(f"Snapshot missing flagship TSE Prime ticker: {sym}")
        for sym in expected_us:
            if sym not in tickers:
                errors.append(f"Snapshot missing flagship US Tech ticker: {sym}")

        usd_jpy = snapshot.get('usd_jpy', 0)
        if usd_jpy <= 0:
            errors.append(f"Invalid USD/JPY exchange rate in snapshot: {usd_jpy}")

        print(f"  ✓ [PASS] Market Snapshot verified: {len(indices)} indices, {len(tickers)} tickers, USD/JPY={usd_jpy}")

    except Exception as e:
        errors.append(f"Failed to parse live_market_snapshot.json: {e}")

    # 4. Check sitemap.xml coverage
    sitemap_path = os.path.join(PROJECT_ROOT, 'sitemap.xml')
    try:
        with open(sitemap_path, 'r', encoding='utf-8') as f:
            sitemap_content = f.read()
        if 'https://getbreakai.com/' not in sitemap_content or 'https://getbreakai.com/jp/index.html' not in sitemap_content:
            errors.append("sitemap.xml missing root or jp/index.html location")
        else:
            loc_count = sitemap_content.count('<loc>')
            print(f"  ✓ [PASS] sitemap.xml verified: {loc_count} URLs indexed")
    except Exception as e:
        errors.append(f"Failed to read sitemap.xml: {e}")

    # Final build status
    if errors:
        print("\n" + "=" * 72)
        print(" [BUILD FAILED] Static asset verification detected errors:")
        for e in errors:
            print(f"  ✗ {e}")
        print("=" * 72)
        return False

    print("\n" + "=" * 72)
    print(" [BUILD VERIFIED] All static assets and snapshot data are present and synchronized.")
    print("=" * 72)
    return True


# =====================================================================
# Main CLI Entrypoint
# =====================================================================
def main():
    parser = argparse.ArgumentParser(description="GetBreakAI Division 3 Code Quality & Build Validator")
    parser.add_argument('--build', action='store_true', help="Run static asset and build synchronization verification")
    parser.add_argument('--all', action='store_true', help="Run both lint and build validations")
    args = parser.parse_args()

    total_failures = 0

    if args.build or args.all:
        build_ok = validate_build()
        if not build_ok:
            total_failures += 1

    if not args.build or args.all:
        js_pass, js_fail = validate_javascript()
        py_pass, py_fail = validate_python()
        html_pass, html_fail = validate_html_link_integrity()
        json_pass, json_fail = validate_json_files()

        total_failures += (js_fail + py_fail + html_fail + json_fail)

        print("\n" + "=" * 72)
        print(f" CODE QUALITY REPORT: {js_pass + py_pass + html_pass + json_pass} Checks Passed, {total_failures} Failures")
        print("=" * 72)

    if total_failures > 0:
        print(f"\n❌ Validation finished with {total_failures} error(s).")
        sys.exit(1)
    else:
        print("\n✨ All verification checks passed cleanly with ZERO errors.")
        sys.exit(0)


if __name__ == '__main__':
    main()
