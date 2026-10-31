"""Milestone M3 Iteration 2 Gate Adversarial Stress-Testing Suite by Challenger 1.

Target: index.html synthesizeDigestFromRecords & dynamic UI resilience

Adversarial Vectors:
1. Empty records array: graceful N/A defaults, zero exceptions.
2. Partial stock records: 1 or 2 stocks present without crashing or skipping remaining stocks.
3. Future / Arbitrary date strings: dynamic date interpolation without hardcoded date fallback.
4. Missing metrics or missing summary: defensive null checks, no TypeError on split/matches.
5. Single-day 2026-09-29 constants leakage: zero hardcoded prices or dates in synthesizer.
6. Dynamic Pair Progress Bar & Weights: dynamically bound from pairStrategy/holdings.
"""

from pathlib import Path
import re
import unittest

ROOT_DIR = Path(__file__).resolve().parent.parent
INDEX_HTML_PATH = ROOT_DIR / "index.html"
DATA_JS_PATH = ROOT_DIR / "data.js"


class TestSynthesizeDigestAdversarial(unittest.TestCase):
    """Adversarial stress-testing of synthesizeDigestFromRecords in index.html."""

    @classmethod
    def setUpClass(cls) -> None:
        cls.assertTrue(INDEX_HTML_PATH.exists(), f"index.html must exist at {INDEX_HTML_PATH}")
        cls.html_content = INDEX_HTML_PATH.read_text(encoding="utf-8")

        # Extract synthesizeDigestFromRecords body
        match = re.search(
            r'function\s+synthesizeDigestFromRecords\s*\([^)]*\)\s*\{(.*?)\n\s*function\s+renderDigestMatrix',
            cls.html_content,
            re.DOTALL,
        )
        cls.assertTrue(match is not None, "synthesizeDigestFromRecords function must exist in index.html")
        cls.synth_body = match.group(1)

    def test_vector1_empty_records_graceful_defaults(self):
        """Vector 1: Empty records must yield N/A, 0.0%, and defensive defaults."""
        body = self.synth_body
        self.assertIn('"N/A"', body, "Synthesizer must provide 'N/A' default for closePrice and volume")
        self.assertIn('"0.0%"', body, "Synthesizer must provide '0.0%' default for changePct")
        self.assertIn('"특이 동인 없음"', body, "Synthesizer must provide default driver for empty records")
        self.assertIn('"관망"', body, "Synthesizer must provide default tone for empty records")
        self.assertIn('"특이 시장 루머 없음"', body, "Synthesizer must provide fallback noise entry")

    def test_vector2_partial_stock_records_loop_over_meta(self):
        """Vector 2: Partial stock records handled by iterating over STOCK_META keys."""
        body = self.synth_body
        self.assertIn("STOCK_META", body, "Synthesizer must iterate over STOCK_META to ensure all 6 stocks exist")
        self.assertIn("closeRec", body)
        self.assertIn("ivRec", body)
        self.assertIn("ibRec", body)

    def test_vector3_future_and_arbitrary_date_interpolation(self):
        """Vector 3: Future and arbitrary dates must be dynamically interpolated."""
        body = self.synth_body
        self.assertIn("${date}", body, "Synthesizer macroSummary fallback must dynamically interpolate ${date}")
        self.assertIn("date,", body, "Synthesizer return object must pass through date property")

    def test_vector4_missing_metrics_and_summary_defensive(self):
        """Vector 4: Missing metrics or summary must not cause runtime TypeErrors."""
        body = self.synth_body
        # Check safe null checks before accessing split or metrics
        self.assertIn("if (closeRec.metrics)", body, "Must check closeRec.metrics before property access")
        self.assertIn("if (closeRec.summary)", body, "Must check closeRec.summary before calling split")
        self.assertIn("String(changePct || \"\")", body, "Must defend against non-string changePct")

    def test_vector5_zero_leaked_single_day_constants(self):
        """Vector 5: Zero single-day 2026-09-29 constants leaked in synthesizeDigestFromRecords."""
        body = self.synth_body
        forbidden_hardcoded_prices = [
            "1,100,000원",
            "176,700원",
            "$78.50",
            "$16.80",
            "$21.40",
            "$34.20",
        ]
        for price in forbidden_hardcoded_prices:
            self.assertNotIn(
                price,
                body,
                f"Forbidden single-day price constant '{price}' found in synthesizeDigestFromRecords!",
            )

        # Check for static ternary operator pattern sym === "..." ? ... : ...
        self.assertFalse(
            bool(re.search(r'sym\s*===?\s*["\']\w+["\']\s*\?', body)),
            "Forbidden static ternary pattern found in synthesizeDigestFromRecords!",
        )

        # Check that 2026-09-29 is not hardcoded in the synthesizer
        self.assertNotIn("2026-09-29", body, "Hardcoded date 2026-09-29 found in synthesizeDigestFromRecords!")

    def test_dynamic_pair_ratio_binding(self):
        """Dynamic pair ratio elements must be updated in renderDigestView."""
        content = self.html_content
        self.assertIn("pairBarSquare", content)
        self.assertIn("pairBarHynix", content)
        self.assertIn("pairWeightSquare", content)
        self.assertIn("pairWeightHynix", content)
        self.assertIn("barSq.style.width", content)
        self.assertIn("barHy.style.width", content)
        self.assertIn("txtSq.innerText", content)
        self.assertIn("txtHy.innerText", content)

    def test_offline_data_js_local_inclusion_satisfies_regex(self):
        """index.html must satisfy r'<script[^>]+src=[\"\\']\\./?data\\.js[\"\\']'."""
        self.assertTrue(
            bool(re.search(r'<script[^>]+src=["\']\./?data\.js["\']', self.html_content, re.IGNORECASE)),
            "index.html must include data.js with relative local path",
        )


if __name__ == "__main__":
    unittest.main()
