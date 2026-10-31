#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
run_forecast.py - CLI Entry Point Wrapper for SK Square & SK Hynix Forecast Engine.

Usage:
    python run_forecast.py --export-all --verify
    python run_forecast.py --date 2026-10-13 --export-all
"""

import sys
import os
import argparse

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8")

from forecast_engine import ForecastEngine, DEFAULT_DATA_DIR


def main():
    parser = argparse.ArgumentParser(
        description="CLI Wrapper for SK Square & SK Hynix Multi-Domain Forecast Engine"
    )
    parser.add_argument(
        "--export-all",
        action="store_true",
        default=True,
        help="Compute all 6 domains and export clean CSV/JSON datasets (default: True)"
    )
    parser.add_argument(
        "--verify",
        action="store_true",
        default=True,
        help="Run strict mathematical and 0-NaN integrity assertions (default: True)"
    )
    parser.add_argument(
        "--date",
        type=str,
        default="2026-10-13",
        help="Evaluation as-of date in YYYY-MM-DD format (default: 2026-10-13)"
    )
    parser.add_argument(
        "--data-dir",
        type=str,
        default=DEFAULT_DATA_DIR,
        help=f"Target directory for output data artifacts (default: {DEFAULT_DATA_DIR})"
    )

    args = parser.parse_args()

    print(f"===================================================================")
    print(f" SK Square (402340) & SK Hynix (000660) Forecast Engine CLI")
    print(f" As-of Date: {args.date} | Target Directory: {args.data_dir}")
    print(f"===================================================================")

    engine = ForecastEngine(data_dir=args.data_dir, as_of_date=args.date)

    if args.verify:
        print("[run_forecast] Executing automated verification checks...")
        engine.verify_integrity()

    if args.export_all:
        print("[run_forecast] Exporting clean CSV and JSON datasets...")
        exported = engine.export_all()
        print("\nSuccessfully Generated Artifacts:")
        for name, path in exported.items():
            sz = os.path.getsize(path) if os.path.exists(path) else 0
            print(f"  * {name:<18s} -> {path} ({sz:,} bytes)")

    print("\n[run_forecast] Execution completed successfully with exit code 0.\n")
    sys.exit(0)


if __name__ == "__main__":
    main()
