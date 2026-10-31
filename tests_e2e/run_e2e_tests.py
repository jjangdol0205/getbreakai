#!/usr/bin/env python
"""
RightSideAlpha Unified E2E Test Runner
======================================
Executes Tiers 1-4 opaque-box end-to-end tests against either:
1. Live running server (e.g. http://127.0.0.1:8000 or custom --server-url)
2. In-process FastAPI TestClient (backend.app.main:app)
3. Contract-compliant reference ASGI harness derived from quant datasets

Usage:
    python tests_e2e/run_e2e_tests.py
    python tests_e2e/run_e2e_tests.py --tier 1
    python tests_e2e/run_e2e_tests.py --server-url http://127.0.0.1:8000
    python tests_e2e/run_e2e_tests.py -v
"""

import sys
import os
import argparse
import time
from pathlib import Path

# Add project root to sys.path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import pytest
import httpx


TIER_FILES = {
    1: "tests_e2e/test_tier1_features.py",
    2: "tests_e2e/test_tier2_boundaries.py",
    3: "tests_e2e/test_tier3_interactions.py",
    4: "tests_e2e/test_tier4_scenarios.py",
    5: "tests_e2e/test_tier5_adversarial.py",
}

TIER_NAMES = {
    1: "Tier 1: Primary Features Specification",
    2: "Tier 2: Boundary & Corner Cases",
    3: "Tier 3: Cross-Feature Interactions",
    4: "Tier 4: Real-World Acceptance Scenarios",
    5: "Tier 5: Adversarial Hardening & Penetration",
}


def probe_target(server_url: str) -> str:
    """Probes whether a live server is running, or falls back to in-process app."""
    try:
        r = httpx.get(f"{server_url}/health", timeout=0.4)
        if r.status_code in [200, 404]:
            return f"Live Server at {server_url}"
    except Exception:
        pass

    try:
        from backend.app.main import app
        return "In-Process Production App (backend.app.main:app)"
    except Exception:
        return "Contract-Compliant Reference App (tests_e2e/conftest.py)"


def run_tier(tier_num: int, pytest_args: list) -> tuple:
    """Runs a specific tier and returns (passed, failed, duration)."""
    tier_file = TIER_FILES[tier_num]
    start_t = time.time()

    # Capture results via pytest custom plugin
    class ResultCollector:
        def __init__(self):
            self.passed = 0
            self.failed = 0
            self.skipped = 0

        def pytest_runtest_logreport(self, report):
            if report.when == "call":
                if report.passed:
                    self.passed += 1
                elif report.failed:
                    self.failed += 1
                elif report.skipped:
                    self.skipped += 1

    collector = ResultCollector()
    args = [tier_file] + pytest_args
    exit_code = pytest.main(args, plugins=[collector])
    duration = time.time() - start_t
    return collector.passed, collector.failed, collector.skipped, duration, exit_code


def main():
    if hasattr(sys.stdout, "reconfigure"):
        try:
            sys.stdout.reconfigure(encoding="utf-8", errors="replace")
            sys.stderr.reconfigure(encoding="utf-8", errors="replace")
        except Exception:
            pass

    parser = argparse.ArgumentParser(description="RightSideAlpha Unified E2E Test Runner")
    parser.add_argument("--tier", type=int, choices=[1, 2, 3, 4, 5], help="Run specific tier (1, 2, 3, 4, or 5)")
    parser.add_argument("--server-url", type=str, default=os.getenv("SERVER_URL", "http://127.0.0.1:8000"), help="Server base URL")
    parser.add_argument("-v", "--verbose", action="store_true", help="Verbose test output")
    parser.add_argument("-x", "--exitfirst", action="store_true", help="Exit on first failure")
    parser.add_argument("--tb", type=str, default="short", help="Traceback style (auto/long/short/line/native/no)")
    args = parser.parse_args()

    os.environ["SERVER_URL"] = args.server_url
    target_desc = probe_target(args.server_url)

    print("=" * 76)
    print(" [RIGHTSIDEALPHA FULL-STACK WEB SERVICE] E2E TEST RUNNER")
    print("=" * 76)
    print(f" Target Mode    : {target_desc}")
    print(f" Server URL     : {args.server_url}")
    print(f" Working Dir    : {PROJECT_ROOT}")
    print(f" Python Version : {sys.version.split()[0]}")
    print("-" * 76)

    pytest_args = ["-q"]
    if args.verbose:
        pytest_args.append("-v")
    if args.exitfirst:
        pytest_args.append("-x")
    pytest_args.append(f"--tb={args.tb}")
    pytest_args.append("--disable-warnings")

    tiers_to_run = [args.tier] if args.tier else [1, 2, 3, 4, 5]

    summary_rows = []
    total_passed = 0
    total_failed = 0
    total_skipped = 0
    total_duration = 0.0
    overall_exit_code = 0

    for t in tiers_to_run:
        print(f"\n>> Executing {TIER_NAMES[t]} ({TIER_FILES[t]})...")
        passed, failed, skipped, duration, code = run_tier(t, pytest_args)
        total_passed += passed
        total_failed += failed
        total_skipped += skipped
        total_duration += duration
        if code != 0:
            overall_exit_code = code
        summary_rows.append((t, TIER_NAMES[t], passed, failed, skipped, duration))

    # Formatted ASCII Summary Table
    print("\n" + "=" * 76)
    print(" [RIGHTSIDEALPHA E2E TEST EXECUTION SUMMARY]")
    print("=" * 76)
    print(f" {'Tier':<6} | {'Test Scope':<38} | {'Passed':<6} | {'Failed':<6} | {'Time':<7}")
    print("-" * 76)
    for t_num, t_name, passed, failed, skipped, dur in summary_rows:
        status_flag = "[OK]" if failed == 0 else "[FAIL]"
        print(f" {status_flag:<6} T{t_num:<2} | {t_name:<38} | {passed:<6} | {failed:<6} | {dur:.2f}s")
    print("-" * 76)
    total_tests = total_passed + total_failed
    pass_rate = (total_passed / total_tests * 100.0) if total_tests > 0 else 0.0
    print(f" TOTAL  | All Tiers ({len(summary_rows)} suites executed)         | {total_passed:<6} | {total_failed:<6} | {total_duration:.2f}s")
    print("=" * 76)
    print(f" Total Tests : {total_tests}")
    print(f" Pass Rate   : {pass_rate:.1f}%")
    print(f" Final Status: {'PASSED (100% GREEN)' if overall_exit_code == 0 and total_failed == 0 else 'FAILED'}")
    print("=" * 76 + "\n")

    sys.exit(overall_exit_code)



if __name__ == "__main__":
    main()
