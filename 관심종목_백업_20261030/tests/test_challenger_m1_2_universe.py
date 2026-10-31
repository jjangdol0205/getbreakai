"""Adversarial Challenger Test Suite for Milestone 1: Universe Ranking & Top-Pick Selection.

Target: engine/turnaround_screener.py
Challenger: Challenger 2 (Universe Ranking & Top-Pick Challenger)

Focus Areas:
1. Ranking determinism across universe permutations.
2. Tie-breaking rules and top-pick selection determinism.
3. Scoring formula boundedness [0.0, 100.0] under extreme magnitudes, zeros, negatives, and non-finites.
4. Strict immunity against selecting UPST (+91%), FLNC (+33%), or SKHY (+77%) as top-pick turnaround candidates.
"""

import itertools
import math
import random
import unittest
from typing import Any, Dict, List

from engine.turnaround_screener import (
    ScreeningFilterResult,
    TurnaroundCandidate,
    TurnaroundScreener,
    WeeklyTopPick,
)


class TestUniverseRankingDeterminism(unittest.TestCase):
    """Verifies that screen_universe ranking is mathematically deterministic and invariant to input order."""

    def test_default_universe_720_permutations_determinism(self):
        """All 720 permutations (6!) of the default universe must yield the exact identical ranking."""
        default_universe = ["MBLY", "CELH", "ENPH", "FLNC", "UPST", "UBER"]
        base_ranked = TurnaroundScreener.screen_universe(default_universe, date="2026-10-07")
        base_order = [c.stock_id for c in base_ranked]

        self.assertEqual(len(base_order), 6)
        # Expected canonical order based on scores and RRRs:
        # MBLY (79.0, 12.55) > CELH (76.0, 11.77) > ENPH (75.0, 10.40) > UBER (71.0, 12.27) > FLNC (39.0, 5.85) > UPST (39.0, 4.70)
        self.assertEqual(base_order, ["MBLY", "CELH", "ENPH", "UBER", "FLNC", "UPST"])

        mismatches = []
        count = 0
        for p in itertools.permutations(default_universe):
            count += 1
            ranked = TurnaroundScreener.screen_universe(list(p), date="2026-10-07")
            order = [c.stock_id for c in ranked]
            if order != base_order:
                mismatches.append((p, order))

        self.assertEqual(count, 720)
        self.assertEqual(
            len(mismatches),
            0,
            f"Universe ranking changed across permutations: {mismatches[:3]}",
        )

    def test_expanded_8_stock_universe_determinism(self):
        """Random permutations of 8-stock universe (including SKHY and SK_SQUARE) must yield stable ranking."""
        expanded_universe = ["MBLY", "CELH", "ENPH", "FLNC", "UPST", "UBER", "SK_HYNIX", "SK_SQUARE"]
        base_ranked = TurnaroundScreener.screen_universe(expanded_universe, date="2026-10-07")
        base_order = [c.stock_id for c in base_ranked]

        # Test 100 random shuffles of expanded universe
        rng = random.Random(42)
        mismatches = []
        for _ in range(100):
            shuffled = list(expanded_universe)
            rng.shuffle(shuffled)
            ranked = TurnaroundScreener.screen_universe(shuffled, date="2026-10-07")
            order = [c.stock_id for c in ranked]
            if order != base_order:
                mismatches.append((shuffled, order))

        self.assertEqual(
            len(mismatches),
            0,
            f"Expanded universe ranking is unstable under permutation: {mismatches[:3]}",
        )

    def test_ranking_monotonicity_by_score_and_rrr(self):
        """Candidates in screen_universe must be monotonically non-increasing by (composite_score, rrr)."""
        universe = TurnaroundScreener.screen_universe(date="2026-10-07")
        for i in range(len(universe) - 1):
            curr = universe[i]
            nxt = universe[i + 1]
            curr_key = (curr.composite_turnaround_score, curr.risk_reward_ratio)
            nxt_key = (nxt.composite_turnaround_score, nxt.risk_reward_ratio)
            self.assertGreaterEqual(
                curr_key,
                nxt_key,
                f"Monotonicity violation at index {i}: {curr.stock_id} ({curr_key}) < {nxt.stock_id} ({nxt_key})",
            )


class TestTieBreakingAndTopPickSelection(unittest.TestCase):
    """Verifies tie-breaking behavior and top-pick selection determinism."""

    def test_top_pick_selection_default_universe_unambiguous(self):
        """In the default universe, MBLY is unambiguously selected as #1 Top Pick."""
        universe = TurnaroundScreener.screen_universe(date="2026-10-07")
        top_pick = TurnaroundScreener.select_weekly_top_pick(universe, date="2026-10-07")

        self.assertIsNotNone(top_pick)
        self.assertEqual(top_pick.stock_id, "MBLY")
        self.assertEqual(top_pick.candidate.conviction_tier, "STRONG_CANDIDATE")
        self.assertTrue(top_pick.candidate.is_qualified)

    def test_tie_breaking_order_independence(self):
        """When two candidates have identical composite score and RRR, top-pick selection must NOT depend on list order."""
        c_a = TurnaroundScreener.screen_stock("MBLY", date="2026-10-07")
        c_b = TurnaroundScreener.screen_stock("CELH", date="2026-10-07")

        # Artificially set identical score and RRR
        c_a.composite_turnaround_score = 85.0
        c_a.risk_reward_ratio = 10.0
        c_b.composite_turnaround_score = 85.0
        c_b.risk_reward_ratio = 10.0

        # Run selection in both orders
        pick_order1 = TurnaroundScreener.select_weekly_top_pick([c_a, c_b], date="2026-10-07")
        pick_order2 = TurnaroundScreener.select_weekly_top_pick([c_b, c_a], date="2026-10-07")

        self.assertIsNotNone(pick_order1)
        self.assertIsNotNone(pick_order2)
        # Adversarial check: The selected stock MUST be identical regardless of input order
        self.assertEqual(
            pick_order1.stock_id,
            pick_order2.stock_id,
            f"Non-deterministic tie breaking! [A, B] selected {pick_order1.stock_id} but [B, A] selected {pick_order2.stock_id}",
        )


class TestScoringFormulaBoundsStress(unittest.TestCase):
    """Stress-tests the scoring formula to ensure composite score is strictly bounded in [0.0, 100.0]."""

    def test_calculate_composite_score_mathematical_bounds_fuzzing(self):
        """Fuzzing calculate_composite_score with 10,000 random sub-scores in [-1000, 1000]."""
        rng = random.Random(1337)
        for _ in range(10000):
            s1 = rng.uniform(-1000.0, 1000.0)
            s2 = rng.uniform(-1000.0, 1000.0)
            s3 = rng.uniform(-1000.0, 1000.0)
            s4 = rng.uniform(-1000.0, 1000.0)

            f1 = ScreeningFilterResult("c1", "F1", True, s1, 25.0, 0, "", "")
            f2 = ScreeningFilterResult("c2", "F2", True, s2, 30.0, 0, "", "")
            f3 = ScreeningFilterResult("c3", "F3", True, s3, 20.0, 0, "", "")
            f4 = ScreeningFilterResult("c4", "F4", True, s4, 25.0, 0, "", "")

            score = TurnaroundScreener.calculate_composite_score(f1, f2, f3, f4)
            self.assertGreaterEqual(score, 0.0, f"Score below 0.0: {score} from {(s1, s2, s3, s4)}")
            self.assertLessEqual(score, 100.0, f"Score above 100.0: {score} from {(s1, s2, s3, s4)}")
            self.assertTrue(math.isfinite(score), f"Score is not finite: {score}")

    def test_screen_stock_extreme_magnitude_inputs(self):
        """screen_stock with extreme market inputs (mega-cap vs penny stock magnitudes)."""
        extreme_magnitudes = [
            # Ultra-penny stock (0.000001)
            {"current_price": 1e-6, "fifty_two_week_low": 1e-6, "fifty_two_week_high": 1e-5, "support_price": 9e-7, "tp1_price": 2e-6, "volume": 10},
            # Ultra-mega price (100,000,000)
            {"current_price": 1e8, "fifty_two_week_low": 1e8, "fifty_two_week_high": 2e8, "support_price": 9.5e7, "tp1_price": 2e8, "volume": 10**12},
            # Huge daily change (+10,000%)
            {"current_price": 10.0, "daily_change_pct": 10000.0, "volume": 10**9},
            # Huge crash daily change (-99.99%)
            {"current_price": 10.0, "daily_change_pct": -99.99, "volume": 10**9},
        ]

        for kwargs in extreme_magnitudes:
            cand = TurnaroundScreener.screen_stock("MBLY", **kwargs)
            score = cand.composite_turnaround_score
            self.assertGreaterEqual(score, 0.0)
            self.assertLessEqual(score, 100.0)
            self.assertTrue(math.isfinite(score))

    def test_zero_and_negative_inputs_bounds(self):
        """Zero and negative inputs must result in valid bounded scores without unhandled exceptions."""
        hostile_cases = [
            {"current_price": 0.0, "fifty_two_week_low": 0.0},
            {"current_price": -10.0, "fifty_two_week_low": -10.0},
            {"support_price": -50.0, "tp1_price": -100.0},
            {"volume": -1000000, "daily_change_pct": -50.0},
        ]
        for kwargs in hostile_cases:
            cand = TurnaroundScreener.screen_stock("MBLY", **kwargs)
            score = cand.composite_turnaround_score
            self.assertGreaterEqual(score, 0.0)
            self.assertLessEqual(score, 100.0)
            self.assertTrue(math.isfinite(score))


class TestDisqualifiedCandidateImmunity(unittest.TestCase):
    """Verifies that UPST, FLNC, and SKHY can NEVER be selected as top-pick turnaround candidates."""

    def test_upst_flnc_skhy_metrics_confirm_disqualification(self):
        """Empirically confirms UPST (+91%), FLNC (+33%), SKHY (+77%) are DISQUALIFIED candidates."""
        upst = TurnaroundScreener.screen_stock("UPST", date="2026-10-07")
        flnc = TurnaroundScreener.screen_stock("FLNC", date="2026-10-07")
        skhy = TurnaroundScreener.screen_stock("SK_HYNIX", date="2026-10-07")

        # Proximity to 52w low checks
        self.assertGreater(upst.proximity_52w_low_pct, 50.0, f"UPST proximity was {upst.proximity_52w_low_pct}%")
        self.assertGreater(flnc.proximity_52w_low_pct, 20.0, f"FLNC proximity was {flnc.proximity_52w_low_pct}%")
        self.assertGreater(skhy.proximity_52w_low_pct, 50.0, f"SKHY proximity was {skhy.proximity_52w_low_pct}%")

        # All 3 must fail Filter 1 (52w low proximity <= 20%)
        self.assertFalse(upst.filters["cond1_52w_low"].passed)
        self.assertFalse(flnc.filters["cond1_52w_low"].passed)
        self.assertFalse(skhy.filters["cond1_52w_low"].passed)

        # All 3 must fail Filter 4 (Risk/Reward <= 10% downside & >= 100% upside)
        self.assertFalse(upst.filters["cond4_risk_reward"].passed)
        self.assertFalse(flnc.filters["cond4_risk_reward"].passed)
        self.assertFalse(skhy.filters["cond4_risk_reward"].passed)

        # All 3 must be strictly DISQUALIFIED
        self.assertEqual(upst.conviction_tier, "DISQUALIFIED")
        self.assertEqual(flnc.conviction_tier, "DISQUALIFIED")
        self.assertEqual(skhy.conviction_tier, "DISQUALIFIED")

        self.assertFalse(upst.is_qualified)
        self.assertFalse(flnc.is_qualified)
        self.assertFalse(skhy.is_qualified)

    def test_upst_flnc_skhy_never_selected_in_full_universe(self):
        """In full universe screening, neither UPST, FLNC, nor SKHY can ever be selected as top-pick."""
        universe = TurnaroundScreener.screen_universe(
            universe=["MBLY", "CELH", "ENPH", "FLNC", "UPST", "UBER", "SK_HYNIX"],
            date="2026-10-07",
        )
        top_pick = TurnaroundScreener.select_weekly_top_pick(universe, date="2026-10-07")

        self.assertIsNotNone(top_pick)
        self.assertNotIn(top_pick.stock_id, ["UPST", "FLNC", "SK_HYNIX"])
        self.assertEqual(top_pick.stock_id, "MBLY")

    def test_disqualified_candidates_never_selected_even_if_alone(self):
        """CRITICAL INVARIANT: Disqualified candidates (UPST, FLNC, SKHY) can NEVER be selected as top-pick.

        If a pool contains ONLY disqualified candidates (none qualify), select_weekly_top_pick
        MUST return None, and MUST NEVER promote a disqualified stock (+91%, +33%, +77%) to Top-Pick!
        """
        c_upst = TurnaroundScreener.screen_stock("UPST", date="2026-10-07")
        c_flnc = TurnaroundScreener.screen_stock("FLNC", date="2026-10-07")
        c_skhy = TurnaroundScreener.screen_stock("SK_HYNIX", date="2026-10-07")

        # Test pool of [UPST, FLNC, SKHY]
        pick_all_disqualified = TurnaroundScreener.select_weekly_top_pick(
            [c_upst, c_flnc, c_skhy],
            date="2026-10-07",
        )
        self.assertIsNone(
            pick_all_disqualified,
            f"Violation! Disqualified candidate {getattr(pick_all_disqualified, 'stock_id', None)} was selected as Top-Pick from a disqualified-only pool!",
        )

        # Test pool of [UPST, FLNC]
        pick_flnc_upst = TurnaroundScreener.select_weekly_top_pick(
            [c_flnc, c_upst],
            date="2026-10-07",
        )
        self.assertIsNone(
            pick_flnc_upst,
            f"Violation! Disqualified candidate {getattr(pick_flnc_upst, 'stock_id', None)} was selected as Top-Pick!",
        )

        # Test individual pools
        self.assertIsNone(
            TurnaroundScreener.select_weekly_top_pick([c_upst], date="2026-10-07"),
            "Violation! UPST was selected as Top-Pick!",
        )
        self.assertIsNone(
            TurnaroundScreener.select_weekly_top_pick([c_flnc], date="2026-10-07"),
            "Violation! FLNC was selected as Top-Pick!",
        )
        self.assertIsNone(
            TurnaroundScreener.select_weekly_top_pick([c_skhy], date="2026-10-07"),
            "Violation! SK_HYNIX was selected as Top-Pick!",
        )


if __name__ == "__main__":
    unittest.main()
