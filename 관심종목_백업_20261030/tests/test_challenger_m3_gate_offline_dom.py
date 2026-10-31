"""Milestone M3 Gate Adversarial Stress-Testing Suite by Challenger 1.

Tasks:
1. 100% Offline Zero-CDN Compliance of index.html & data.js (zero remote assets, zero network requests).
2. DOM & Script Integrity (getElementById parity, HTML event handler existence, View 5 event functions, live browser interaction).
3. CLI timing subcommand adversarial stress testing (invalid dates, missing files, --json formatting, error exits).
4. data.js Timing Store & History Persistence.
"""

from __future__ import annotations

import base64
import json
import os
from pathlib import Path
import re
import socket
import subprocess
import sys
import tempfile
import time
import urllib.request
import unittest

ROOT_DIR = Path(__file__).resolve().parent.parent
INDEX_HTML_PATH = ROOT_DIR / "index.html"
DATA_JS_PATH = ROOT_DIR / "data.js"

from engine.models import StockSymbol, STOCK_MASTERS, DailyMarketData
import engine.cli as cli_module


class TestTask1OfflineZeroCdnCompliance(unittest.TestCase):
    """Challenge 1: 100% Offline Zero-CDN Compliance."""

    @classmethod
    def setUpClass(cls):
        cls.assertTrue(INDEX_HTML_PATH.exists(), f"index.html must exist at {INDEX_HTML_PATH}")
        cls.html_content = INDEX_HTML_PATH.read_text(encoding="utf-8")
        cls.assertTrue(DATA_JS_PATH.exists(), f"data.js must exist at {DATA_JS_PATH}")
        cls.js_content = DATA_JS_PATH.read_text(encoding="utf-8")

    def test_zero_remote_script_sources(self):
        """Scrape index.html for any remote external scripts (<script src="http...)."""
        script_srcs = re.findall(r'<script[^>]+src=["\']([^"\']+)["\']', self.html_content, re.IGNORECASE)
        for src in script_srcs:
            self.assertFalse(
                src.startswith(("http://", "https://", "//", "ftp://")),
                f"Forbidden remote script src found: {src}"
            )
            self.assertTrue(
                src.startswith("./") or src.startswith("../") or not ("://" in src),
                f"Suspicious script src: {src}"
            )

    def test_zero_remote_link_stylesheets_and_fonts(self):
        """Scrape index.html for any remote stylesheets or font links."""
        link_hrefs = re.findall(r'<link[^>]+href=["\']([^"\']+)["\']', self.html_content, re.IGNORECASE)
        for href in link_hrefs:
            self.assertFalse(
                href.startswith(("http://", "https://", "//", "ftp://")),
                f"Forbidden remote link href found: {href}"
            )

    def test_zero_remote_images_in_html(self):
        """Scrape index.html for any remote images."""
        img_srcs = re.findall(r'<img[^>]+src=["\']([^"\']+)["\']', self.html_content, re.IGNORECASE)
        for src in img_srcs:
            self.assertFalse(
                src.startswith(("http://", "https://", "//")),
                f"Forbidden remote img src found: {src}"
            )

    def test_zero_css_imports_and_remote_urls(self):
        """Embedded <style> must not contain @import or url() pointing to remote assets."""
        style_blocks = re.findall(r'<style[^>]*>(.*?)</style>', self.html_content, re.DOTALL | re.IGNORECASE)
        for idx, block in enumerate(style_blocks):
            imports = re.findall(r'@import\s+[^;]+;', block, re.IGNORECASE)
            self.assertEqual(imports, [], f"Forbidden @import found in style block #{idx}: {imports}")

            urls = re.findall(r'url\s*\(\s*["\']?([^"\'\)]+)["\']?\s*\)', block, re.IGNORECASE)
            for u in urls:
                u_clean = u.strip()
                if u_clean.startswith("data:"):
                    continue
                self.assertFalse(
                    u_clean.startswith(("http://", "https://", "//")),
                    f"Forbidden remote CSS url found in style block #{idx}: {u_clean}"
                )

    def test_zero_cdn_hostnames(self):
        """Ensure no known CDN hostnames exist as resource loaders in index.html."""
        cdn_patterns = [
            r'cdn\.jsdelivr\.net',
            r'cdnjs\.cloudflare\.com',
            r'unpkg\.com',
            r'fonts\.googleapis\.com',
            r'fonts\.gstatic\.com',
            r'ajax\.googleapis\.com',
            r'code\.jquery\.com',
            r'stackpath\.bootstrapcdn\.com',
            r'tailwind',
        ]
        for cdn in cdn_patterns:
            matches = re.findall(rf'<[^>]+{cdn}[^>]*>', self.html_content, re.IGNORECASE)
            self.assertEqual(
                matches, [],
                f"CDN hostname pattern '{cdn}' found in HTML tags: {matches}"
            )

    def test_file_protocol_zero_network_dependency(self):
        """Verify index.html only references local ./data.js and self-contained assets."""
        resource_tags = re.findall(r'<(?:script|link|img|iframe|embed|object|audio|video)[^>]+(?:src|href)=["\']([^"\']+)["\']', self.html_content, re.IGNORECASE)
        for res in resource_tags:
            self.assertFalse(
                res.startswith(("http://", "https://", "//")),
                f"Remote resource dependency found: {res}"
            )
            if res.startswith("./"):
                target = ROOT_DIR / res[2:]
                self.assertTrue(target.exists(), f"Local referenced file does not exist: {res} -> {target}")


class TestTask2DomAndScriptIntegrity(unittest.TestCase):
    """Challenge 2: DOM & Script Integrity."""

    @classmethod
    def setUpClass(cls):
        cls.html_content = INDEX_HTML_PATH.read_text(encoding="utf-8")
        script_matches = re.findall(r'<script(?![^>]*src=)[^>]*>(.*?)</script>', cls.html_content, re.DOTALL | re.IGNORECASE)
        cls.inline_js = "\n".join(script_matches)

    def test_every_get_element_by_id_exists_in_dom(self):
        """Test that every document.getElementById queried in index.html exists in the markup."""
        queried_ids = set(re.findall(r'document\.getElementById\(["\']([^"\']+)["\']\)', self.inline_js))
        self.assertGreater(len(queried_ids), 0, "No getElementById found in inline scripts")

        dom_ids = set(re.findall(r'\bid=["\']([^"\']+)["\']', self.html_content))
        missing_ids = queried_ids - dom_ids
        self.assertEqual(
            missing_ids, set(),
            f"JavaScript queries element IDs via getElementById that do NOT exist in markup: {sorted(missing_ids)}"
        )

    def test_every_html_event_handler_declared_in_js(self):
        """Test that every onclick, onchange, oninput handler in markup is declared as a callable in JS."""
        handler_calls = re.findall(r'\bon[a-z]+=["\']\s*([a-zA-Z0-9_]+)\s*\(', self.html_content)
        unique_handlers = set(handler_calls)
        self.assertGreater(len(unique_handlers), 0, "No event handlers found in HTML")

        for handler in sorted(unique_handlers):
            pattern = re.compile(rf'(?:function\s+{handler}\b|\b{handler}\s*=\s*(?:function|\([^)]*\)\s*=>)|window\.{handler}\s*=)')
            self.assertTrue(
                pattern.search(self.inline_js),
                f"HTML event handler '{handler}' is invoked in markup but NOT declared in JavaScript!"
            )

    def test_view_5_dom_elements_exist(self):
        """Test that all View 5 (Timing & Catalyst) core DOM elements exist in index.html."""
        required_view5_ids = [
            "btnViewTiming",
            "viewTimingSection",
            "timingKpiRibbon",
            "timingPortfolioDiagnosisCard",
            "portfolioDiagnosisContent",
            "timingSwitchingCard",
            "switchingCardContent",
            "timingGaugesGrid",
            "timingCatalystGrid",
            "timingDateSelect",
            "timingCoverageLabel",
            "timingHistoryTable",
            "timingHistoryTableBody",
            "timingStockPills",
        ]
        dom_ids = set(re.findall(r'\bid=["\']([^"\']+)["\']', self.html_content))
        for vid in required_view5_ids:
            self.assertIn(vid, dom_ids, f"Required View 5 DOM element id='{vid}' is missing from index.html")

    def test_view_5_date_nav_buttons_exist_in_markup(self):
        """Test that View 5 date selector toolbar has prev/next date buttons calling navigateTimingDate."""
        nav_prev = re.search(r'<button[^>]*class=["\'][^"\']*btn-nav-day[^"\']*["\'][^>]*onclick=["\']navigateTimingDate\(-1\)["\']', self.html_content)
        nav_next = re.search(r'<button[^>]*class=["\'][^"\']*btn-nav-day[^"\']*["\'][^>]*onclick=["\']navigateTimingDate\(1\)["\']', self.html_content)
        self.assertIsNotNone(nav_prev, "Prev date button calling navigateTimingDate(-1) missing from markup")
        self.assertIsNotNone(nav_next, "Next date button calling navigateTimingDate(1) missing from markup")

    def test_view_5_controller_functions_declared(self):
        """Test that all View 5 controller functions are declared in JavaScript."""
        required_funcs = [
            "renderTimingView",
            "getActiveTimingSnapshot",
            "renderTimingDateSelector",
            "handleTimingDateChange",
            "navigateTimingDate",
            "renderTimingStockPills",
            "setTimingStockFilter",
            "renderTimingKpiRibbon",
            "renderTimingPortfolioDiagnosis",
            "renderTimingSwitching",
            "renderTimingGauges",
            "renderTimingCatalysts",
            "renderTimingHistoryTimeline",
            "selectTimingHistoryDate",
        ]
        for func_name in required_funcs:
            pattern = re.compile(rf'(?:function\s+{func_name}\b|\b{func_name}\s*=\s*(?:function|\([^)]*\)\s*=>)|window\.{func_name}\s*=)')
            self.assertTrue(
                pattern.search(self.inline_js),
                f"Required View 5 JS controller function '{func_name}' is not declared in inline scripts!"
            )

    def test_view_switch_group_includes_timing_button(self):
        """Test that the view-switch-group has btnViewTiming with switchView('timing')."""
        match = re.search(r'<button[^>]*id=["\']btnViewTiming["\'][^>]*onclick=["\']switchView\([\"\']timing[\"\']\)[^>]*>', self.html_content)
        self.assertIsNotNone(match, "btnViewTiming button with onclick=\"switchView('timing')\" not found in nav header")

    def test_switch_view_implementation_handles_timing(self):
        """Test that switchView function handles the 'timing' case cleanly."""
        self.assertIn("function switchView", self.inline_js)
        timing_handled = re.search(r'viewName\s*===\s*["\']timing["\']|case\s*["\']timing["\']|viewTimingSection', self.inline_js)
        self.assertIsNotNone(timing_handled, "switchView does not explicitly handle 'timing' view")


class TestTask2EdgeBrowserEmpiricalInteraction(unittest.TestCase):
    """Empirically test View 5 interactive operations inside headless Microsoft Edge browser."""

    @classmethod
    def setUpClass(cls):
        edge_paths = [
            r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
            r"C:\Program Files\Microsoft\Edge\Application\msedge.exe"
        ]
        cls.edge_exe = next((p for p in edge_paths if os.path.exists(p)), None)
        if not cls.edge_exe:
            raise unittest.SkipTest("Microsoft Edge binary not found on Windows host")

    def test_headless_edge_view_5_clicks_and_zero_errors(self):
        """Run headless Edge via CDP, click View 5, filters, and date navigation; verify zero errors."""
        tmp = tempfile.mkdtemp()
        cmd = [
            self.edge_exe,
            "--headless=new",
            "--remote-debugging-port=9222",
            f"--user-data-dir={tmp}",
            "--no-first-run",
            f"file:///{str(INDEX_HTML_PATH).replace(os.sep, '/')}"
        ]
        proc = subprocess.Popen(cmd)
        try:
            time.sleep(2.0)
            with urllib.request.urlopen("http://localhost:9222/json") as resp:
                targets = json.loads(resp.read().decode("utf-8"))
            page_target = next(t for t in targets if "index.html" in t.get("url", ""))
            ws_url = page_target["webSocketDebuggerUrl"]

            url_part = ws_url.replace("ws://", "")
            host_port, path = url_part.split("/", 1)
            host, port = host_port.split(":")

            # Simple RFC 6455 client
            sock = socket.create_connection((host, int(port)), timeout=5)
            key = base64.b64encode(os.urandom(16)).decode("utf-8")
            req = (
                f"GET /{path} HTTP/1.1\r\n"
                f"Host: {host}:{port}\r\n"
                f"Upgrade: websocket\r\n"
                f"Connection: Upgrade\r\n"
                f"Sec-WebSocket-Key: {key}\r\n"
                f"Sec-WebSocket-Version: 13\r\n\r\n"
            )
            sock.sendall(req.encode("utf-8"))
            handshake = sock.recv(4096).decode("utf-8")
            self.assertIn("101", handshake)

            def send_ws(msg_dict):
                data = json.dumps(msg_dict).encode("utf-8")
                length = len(data)
                frame = bytearray([0x81])
                mask = os.urandom(4)
                if length <= 125:
                    frame.append(0x80 | length)
                elif length <= 65535:
                    frame.append(0x80 | 126)
                    frame.extend(length.to_bytes(2, "big"))
                else:
                    frame.append(0x80 | 127)
                    frame.extend(length.to_bytes(8, "big"))
                frame.extend(mask)
                frame.extend(bytearray(b ^ mask[i % 4] for i, b in enumerate(data)))
                sock.sendall(frame)

            def recv_ws():
                b1, b2 = sock.recv(2)
                masked = (b2 & 0x80) != 0
                length = b2 & 0x7f
                if length == 126:
                    length = int.from_bytes(sock.recv(2), "big")
                elif length == 127:
                    length = int.from_bytes(sock.recv(8), "big")
                if masked:
                    mask = sock.recv(4)
                raw = b""
                while len(raw) < length:
                    chunk = sock.recv(min(4096, length - len(raw)))
                    if not chunk: break
                    raw += chunk
                if masked:
                    raw = bytearray(b ^ mask[i % 4] for i, b in enumerate(raw))
                return raw.decode("utf-8", errors="replace")

            send_ws({"id": 1, "method": "Network.enable"})
            send_ws({"id": 2, "method": "Console.enable"})
            send_ws({"id": 3, "method": "Runtime.enable"})

            eval_script = """
            (() => {
                const results = {};
                // 1. Switch to timing view
                switchView('timing');
                results.activeView = Terminal.activeView;

                // 2. Check timing section visibility
                const sec = document.getElementById('viewTimingSection');
                results.timingSectionVisible = sec && !sec.classList.contains('hidden');

                // 3. Test stock pill clicks
                const pills = document.querySelectorAll('#timingStockPills .btn-stock-pill');
                results.pillCount = pills.length;
                if (pills.length >= 2) {
                    pills[1].click(); // filter to stock 1
                    results.filteredGauges = document.querySelectorAll('.timing-gauge-card').length;
                    results.filteredCatalysts = document.querySelectorAll('.timing-catalyst-card').length;
                    pills[0].click(); // reset to ALL
                    results.allGauges = document.querySelectorAll('.timing-gauge-card').length;
                    results.allCatalysts = document.querySelectorAll('.timing-catalyst-card').length;
                }

                // 4. Test date selector
                const dateSelect = document.getElementById('timingDateSelect');
                if (dateSelect && dateSelect.options.length > 2) {
                    dateSelect.selectedIndex = 1;
                    dateSelect.dispatchEvent(new Event('change'));
                    results.dateSelected = Terminal.selectedTimingDate;
                }

                // 5. Test date navigation buttons
                const navBtns = document.querySelectorAll('#viewTimingSection .btn-nav-day');
                results.navBtnCount = navBtns.length;
                if (navBtns.length >= 2) {
                    const before = Terminal.selectedTimingDate;
                    navBtns[0].click();
                    results.dateAfterPrev = Terminal.selectedTimingDate;
                    navBtns[1].click();
                    results.dateAfterNext = Terminal.selectedTimingDate;
                }

                // 6. Test history row click
                if (typeof selectTimingHistoryDate === 'function') {
                    selectTimingHistoryDate('2026-10-09');
                    results.historyDateClicked = Terminal.selectedTimingDate;
                }

                return results;
            })()
            """
            send_ws({"id": 10, "method": "Runtime.evaluate", "params": {"expression": eval_script, "returnByValue": True}})

            network_requests = []
            console_errors = []
            eval_result = None

            start = time.time()
            while time.time() - start < 8.0:
                msg = json.loads(recv_ws())
                method = msg.get("method", "")
                if method == "Network.requestWillBeSent":
                    req_url = msg["params"]["request"]["url"]
                    if not req_url.startswith("file:"):
                        network_requests.append(req_url)
                elif method == "Console.messageAdded":
                    lvl = msg["params"]["message"]["level"]
                    if lvl in ("error", "warning"):
                        console_errors.append(msg["params"]["message"]["text"])
                elif msg.get("id") == 10:
                    eval_result = msg.get("result", {}).get("result", {}).get("value")
                    break

            sock.close()

            # Empirical checks
            self.assertIsNotNone(eval_result, "Browser evaluation failed to return result")
            self.assertEqual(eval_result.get("activeView"), "timing")
            self.assertTrue(eval_result.get("timingSectionVisible"))
            self.assertEqual(eval_result.get("pillCount"), 9)
            self.assertEqual(eval_result.get("filteredGauges"), 1)
            self.assertEqual(eval_result.get("filteredCatalysts"), 1)
            self.assertEqual(eval_result.get("allGauges"), 8)
            self.assertEqual(eval_result.get("allCatalysts"), 8)
            self.assertEqual(eval_result.get("historyDateClicked"), "2026-10-09")

            # Zero network requests to remote domains
            self.assertEqual(network_requests, [], f"Browser made remote network requests: {network_requests}")
            # Zero console errors
            self.assertEqual(console_errors, [], f"Browser console emitted errors: {console_errors}")

        finally:
            proc.terminate()
            proc.wait()
            import shutil
            shutil.rmtree(tmp, ignore_errors=True)


class TestTask3CliTimingSubcommand(unittest.TestCase):
    """Challenge 3: CLI timing subcommand adversarial stress testing."""

    def setUp(self):
        self.sample_dump = """
[SK하이닉스 일일 시세 요약]
- 종가: $188.80 (+2.15%)
- 거래량: 3,450,000주

[우버 일일 시세 요약]
- 종가: $68.51 (-0.75%)
- 거래량: 15,200,000주
"""

    def test_cli_timing_help(self):
        """CLI timing --help exits with code 0."""
        try:
            cli_module.main(["timing", "--help"])
        except SystemExit as e:
            self.assertEqual(e.code, 0)

    def test_cli_timing_no_input_defaults_gracefully(self):
        """CLI timing without -i should evaluate using fallback/feed data and exit 0."""
        with tempfile.TemporaryDirectory(ignore_cleanup_errors=True) as tmp_dir:
            out_file = Path(tmp_dir) / "out.json"
            code = cli_module.main(["timing", "--json", "-o", str(out_file)])
            self.assertEqual(code, 0, "timing without -i should succeed with fallback data")
            data = json.loads(out_file.read_text(encoding="utf-8"))
            self.assertIn("stocks", data)
            self.assertEqual(len(data["stocks"]), 8)

    def test_cli_timing_with_valid_input_and_json(self):
        """CLI timing with valid input file and --json produces valid JSON."""
        with tempfile.TemporaryDirectory(ignore_cleanup_errors=True) as tmp_dir:
            input_file = Path(tmp_dir) / "dump.txt"
            input_file.write_text(self.sample_dump, encoding="utf-8")
            output_file = Path(tmp_dir) / "output.json"

            code = cli_module.main(["timing", "-i", str(input_file), "-o", str(output_file), "--json", "-d", "2026-10-12"])
            self.assertEqual(code, 0)

            content = output_file.read_text(encoding="utf-8")
            data = json.loads(content)
            self.assertIn("date", data)
            self.assertIn("stocks", data)
            self.assertIn("switching", data)
            self.assertEqual(data["switching"]["holding_stock_id"], "SK_SQUARE")
            self.assertEqual(data["switching"]["holding_shares"], 76)

    def test_cli_timing_with_human_readable_summary(self):
        """CLI timing without --json produces structured text summary."""
        with tempfile.TemporaryDirectory(ignore_cleanup_errors=True) as tmp_dir:
            input_file = Path(tmp_dir) / "dump.txt"
            input_file.write_text(self.sample_dump, encoding="utf-8")
            output_file = Path(tmp_dir) / "output.txt"

            code = cli_module.main(["timing", "-i", str(input_file), "-o", str(output_file), "-d", "2026-10-12"])
            self.assertEqual(code, 0)

            content = output_file.read_text(encoding="utf-8")
            self.assertIn("8-Stock Timing & Switching Diagnosis", content)
            self.assertIn("SK Square 76 shares", content)
            self.assertIn("Switching Status", content)
            self.assertIn("Safety Band", content)

    def test_cli_timing_missing_input_file_fails_cleanly(self):
        """CLI timing with non-existent file should raise or exit with error."""
        non_existent = "C:/non_existent_path_xyz_12345/dump.txt"
        with self.assertRaises((FileNotFoundError, SystemExit, Exception)):
            cli_module.main(["timing", "-i", non_existent])

    def test_cli_timing_empty_input_file_handles_gracefully(self):
        """CLI timing with 0-byte file defaults to fallback feed and exits 0."""
        with tempfile.TemporaryDirectory(ignore_cleanup_errors=True) as tmp_dir:
            empty_file = Path(tmp_dir) / "empty.txt"
            empty_file.write_text("", encoding="utf-8")
            output_file = Path(tmp_dir) / "out.json"

            code = cli_module.main(["timing", "-i", str(empty_file), "-o", str(output_file), "--json"])
            self.assertEqual(code, 0)

            content = output_file.read_text(encoding="utf-8")
            data = json.loads(content)
            self.assertIn("stocks", data)
            self.assertEqual(len(data["stocks"]), 8)

    def test_cli_timing_invalid_date_formats(self):
        """CLI timing with adversarial date strings (e.g., 'invalid-date', '2026-99-99')."""
        adversarial_dates = ["invalid-date", "2026-99-99", "2026/10/12", "NOT_A_DATE"]
        for ad_date in adversarial_dates:
            with tempfile.TemporaryDirectory(ignore_cleanup_errors=True) as tmp_dir:
                out_file = Path(tmp_dir) / "out.json"
                try:
                    code = cli_module.main(["timing", "-d", ad_date, "--json", "-o", str(out_file)])
                    self.assertEqual(code, 0)
                    content = out_file.read_text(encoding="utf-8")
                    data = json.loads(content)
                    self.assertIn("stocks", data)
                except Exception as e:
                    self.assertIsInstance(e, (ValueError, SystemExit))

    def test_cli_timing_corrupted_garbage_input(self):
        """CLI timing with non-market binary/noise text."""
        noise_text = "@@@###$$$%%%^^^&&&***()_+ \x00\x01\x02 random garbage text without any tickers"
        with tempfile.TemporaryDirectory(ignore_cleanup_errors=True) as tmp_dir:
            noise_file = Path(tmp_dir) / "noise.txt"
            noise_file.write_text(noise_text, encoding="utf-8")
            out_file = Path(tmp_dir) / "out.json"

            code = cli_module.main(["timing", "-i", str(noise_file), "-o", str(out_file), "--json"])
            self.assertEqual(code, 0)
            content = out_file.read_text(encoding="utf-8")
            data = json.loads(content)
            self.assertIn("stocks", data)
            self.assertEqual(len(data["stocks"]), 8)


class TestTask4DataJsTimingStoreStructure(unittest.TestCase):
    """Challenge 4: data.js Timing Store & History Persistence."""

    @classmethod
    def setUpClass(cls):
        from tests.test_dashboard import parse_js_data_store
        cls.js_text = DATA_JS_PATH.read_text(encoding="utf-8")
        cls.data_store = parse_js_data_store(cls.js_text)

    def test_timing_store_exists_in_data_js(self):
        """data.js must contain window.WATCHLIST_DATA.timing object."""
        self.assertIn("timing", self.data_store, "timing key missing from data.js store")
        timing = self.data_store["timing"]
        self.assertIsInstance(timing, dict)
        self.assertIn("portfolioDiagnosis", timing)
        self.assertIn("stocks", timing)
        self.assertIn("switchingOpportunities", timing)
        self.assertIn("history", timing)

    def test_timing_portfolio_diagnosis_accuracy(self):
        """Verify SK Square 76 shares diagnosis fields in data.js."""
        pd = self.data_store["timing"]["portfolioDiagnosis"]
        self.assertEqual(pd["holdingStock"], "SK_SQUARE")
        self.assertEqual(pd["shares"], 76)
        self.assertIn("totalValuation", pd)
        self.assertIn("tpGuide", pd)

    def test_timing_stocks_contains_all_8_symbols(self):
        """All 8 canonical stock IDs must exist in timing.stocks."""
        stocks = self.data_store["timing"]["stocks"]
        for sym in StockSymbol:
            self.assertIn(sym.value, stocks, f"Stock {sym.value} missing from timing.stocks in data.js")
            stock_info = stocks[sym.value]
            self.assertIn("valuationBand", stock_info)
            self.assertIn("takeProfit", stock_info)
            self.assertIn("trigger", stock_info)

    def test_timing_history_is_chronological_and_non_empty(self):
        """timing.history must contain descending chronological entries."""
        history = self.data_store["timing"]["history"]
        self.assertIsInstance(history, list)
        self.assertGreater(len(history), 0, "timing.history must not be empty")
        dates = [entry["date"] for entry in history]
        self.assertEqual(dates, sorted(dates, reverse=True), "timing.history must be descending chronological (newest first)")


if __name__ == "__main__":
    unittest.main()
