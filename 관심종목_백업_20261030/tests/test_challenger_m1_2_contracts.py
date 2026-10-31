"""Empirical Contract, JSON Serialization, and Determinism Test Suite.

Author: Challenger M1-2 (teamwork_preview_challenger_m1_2_o7)
Mission:
Empirically verify output contracts, determinism, and backwards compatibility:
1. python -m engine.cli timing --json contract compliance & valid complete JSON.
2. Bit-for-bit determinism across repeated executions.
3. Mathematical precision of SK Square 76 shares & TP1 38 shares recovery math.
4. Backwards compatibility of DailyTimingSnapshot.to_dict() and consumer subscription.
5. Boundary conditions & adversarial stress inputs.
"""

from __future__ import annotations

import json
import subprocess
import sys
import unittest
from datetime import date
from typing import Any, Dict, List

from engine.models import DailyMarketData, MarketMetrics, StockFactSheet, STOCK_MASTERS, StockSymbol
from engine.timing_engine import (
    DailyTimingSnapshot,
    FundManagerProposal,
    PortfolioDiagnostic,
    RiskManagementAlert,
    StockTimingEvaluation,
    SwitchingActionScenario,
    TimingEngine,
    STOCK_REFERENCE_PRICES,
)


class TestCliJsonContractCompliance(unittest.TestCase):
    """Empirical verification of engine.cli timing --json CLI execution and JSON output."""

    def test_cli_timing_json_stdout_validity_and_schema(self) -> None:
        """CLI timing --json must return exit code 0 and emit valid, parseable JSON to stdout."""
        cmd = [sys.executable, "-m", "engine.cli", "timing", "--date", "2026-10-12", "--json"]
        proc = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, encoding="utf-8", errors="replace", check=False)

        self.assertEqual(proc.returncode, 0, f"CLI exited with non-zero code {proc.returncode}. Stderr: {proc.stderr}")
        self.assertTrue(len(proc.stdout) > 0, "CLI stdout should not be empty")

        # JSON Parse
        try:
            data = json.loads(proc.stdout)
        except json.JSONDecodeError as e:
            self.fail(f"CLI stdout failed to parse as valid JSON: {e}\nStdout sample: {proc.stdout[:500]}")

        # Top-level schema contract
        required_top_keys = {"date", "timestamp", "stocks", "switching", "managerProposal"}
        self.assertTrue(required_top_keys.issubset(data.keys()), f"Missing top-level keys. Found: {list(data.keys())}")

        self.assertEqual(data["date"], "2026-10-12")
        self.assertIsInstance(data["stocks"], dict)
        self.assertIsInstance(data["switching"], dict)
        self.assertIsInstance(data["managerProposal"], dict)

        # 8 Canonical stocks present in 'stocks'
        expected_stocks = {"SK_HYNIX", "SK_SQUARE", "UBER", "MBLY", "FLNC", "UPST", "CELH", "ENPH"}
        self.assertEqual(set(data["stocks"].keys()), expected_stocks)

        # Validate managerProposal contract
        mp = data["managerProposal"]
        mp_required_keys = {
            "date", "timestamp", "managerPersona", "investmentHorizon", "targetObjective",
            "coreHolding", "tacticalAction", "actionHeadline", "executiveSummary",
            "reasoningPillars", "timeTo100Ranking", "switchingProposal", "riskWarnings",
            "riskWarningMessages", "journalMarkdown"
        }
        self.assertTrue(mp_required_keys.issubset(mp.keys()), f"Missing keys in managerProposal: {mp_required_keys - set(mp.keys())}")

        # Core holding contract & exact mathematical values
        ch = mp["coreHolding"]
        self.assertEqual(ch["stockId"], "SK_SQUARE")
        self.assertEqual(ch["shares"], 76)
        self.assertEqual(ch["principalKrw"], 82840000)
        self.assertEqual(ch["avgCostKrw"], 1090000)
        self.assertEqual(ch["tp1TargetPrice"], 2180000.0)
        self.assertEqual(ch["tp1SharesToSell"], 38)
        self.assertEqual(ch["tp1RecoveredAmount"], 82840000)
        self.assertEqual(ch["tp1SharesToSell"] * ch["tp1TargetPrice"], ch["tp1RecoveredAmount"])
        self.assertEqual(ch["tp1RecoveredAmount"], ch["principalKrw"])

        # Time to 100% ranking
        ranking = mp["timeTo100Ranking"]
        self.assertEqual(len(ranking), 8)
        ranks = [r["rank"] for r in ranking]
        self.assertEqual(ranks, list(range(1, 9)), "Ranks must be contiguous 1..8")
        speed_scores = [r["speedScore"] for r in ranking]
        self.assertEqual(speed_scores, sorted(speed_scores, reverse=True), "Ranking must be sorted descending by speedScore")

        # Journal markdown non-empty and well-structured
        jm = mp["journalMarkdown"]
        self.assertIn("# 🤖", jm)
        self.assertIn("SK스퀘어 76주", jm)
        self.assertIn("8,284만 원", jm)
        self.assertIn("2,180,000원", jm)

    def test_cli_timing_file_output(self) -> None:
        """CLI timing --json with -o <filepath> writes valid JSON to file and runs cleanly."""
        import tempfile
        with tempfile.NamedTemporaryFile("w+", suffix=".json", delete=False) as tmp:
            tmp_path = tmp.name

        try:
            cmd = [sys.executable, "-m", "engine.cli", "timing", "--date", "2026-10-12", "--json", "-o", tmp_path]
            proc = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, encoding="utf-8", errors="replace", check=False)
            self.assertEqual(proc.returncode, 0)
            with open(tmp_path, "r", encoding="utf-8") as f:
                content = f.read()
            parsed = json.loads(content)
            self.assertIn("managerProposal", parsed)
            self.assertEqual(parsed["managerProposal"]["coreHolding"]["shares"], 76)
        finally:
            import os
            if os.path.exists(tmp_path):
                os.remove(tmp_path)


class TestDeterminismAcrossRepeatedRuns(unittest.TestCase):
    """Empirical verification that TimingEngine evaluation is pure and strictly deterministic."""

    def test_evaluate_daily_timing_determinism_5x(self) -> None:
        """Repeated invocations of TimingEngine.evaluate_daily_timing on fixed inputs produce bit-for-bit identical dicts."""
        mdata = DailyMarketData(date="2026-10-12")
        port = {"holdingStock": "SK_SQUARE", "shares": 76}

        results = []
        for _ in range(5):
            snap = TimingEngine.evaluate_daily_timing(mdata, portfolio=port, as_of_date="2026-10-12")
            snap_dict = snap.to_dict()
            # Remove timestamp which reflects wall clock time
            snap_dict.pop("timestamp", None)
            if "managerProposal" in snap_dict:
                snap_dict["managerProposal"].pop("timestamp", None)
            results.append(json.dumps(snap_dict, sort_keys=True, ensure_ascii=False))

        # Check all runs equal run 0
        for i, res in enumerate(results[1:], start=1):
            self.assertEqual(res, results[0], f"Run {i} differed from run 0! Non-deterministic behavior detected.")

    def test_ranking_speed_score_stability(self) -> None:
        """Time-to-100 ranking scores and ordering must be completely deterministic."""
        mdata = DailyMarketData(date="2026-10-12")
        res1 = TimingEngine.generate_manager_proposal(market_data=mdata, date="2026-10-12")
        res2 = TimingEngine.generate_manager_proposal(market_data=mdata, date="2026-10-12")

        rank1 = [(r["stockId"], r["speedScore"], r["rank"]) for r in res1.time_to_100_ranking]
        rank2 = [(r["stockId"], r["speedScore"], r["rank"]) for r in res2.time_to_100_ranking]
        self.assertEqual(rank1, rank2)


class TestBackwardsCompatibility(unittest.TestCase):
    """Empirical verification of backwards compatibility for consumers of DailyTimingSnapshot."""

    def test_snapshot_without_manager_proposal_omits_key(self) -> None:
        """When manager_proposal is None, to_dict() must NOT output 'managerProposal' key."""
        snap = DailyTimingSnapshot(
            date="2026-10-12",
            timestamp="2026-10-12T00:00:00",
            stocks={},
            switching=TimingEngine.evaluate_switching("SK_SQUARE", 76, {}),
            manager_proposal=None,
        )
        d = snap.to_dict()
        self.assertNotIn("managerProposal", d)
        self.assertIn("date", d)
        self.assertIn("stocks", d)
        self.assertIn("switching", d)

    def test_dictionary_subscription_and_get_access(self) -> None:
        """All new dataclasses must implement __getitem__ and .get() for dict-like compatibility."""
        diag = PortfolioDiagnostic()
        self.assertEqual(diag["shares"], 76)
        self.assertEqual(diag.get("shares"), 76)
        self.assertEqual(diag["tp1TargetPrice"], 2180000.0)
        self.assertEqual(diag.get("non_existent", "default_val"), "default_val")

        scenario = SwitchingActionScenario(
            candidate_id="UBER",
            candidate_name="우버",
            action_type="TACTICAL_SWITCH",
            shares_to_sell=10,
            freed_capital_krw=10500000,
            candidate_shares_to_buy=110,
            holding_tp1_upside_pct=88.4,
            candidate_tp1_upside_pct=106.2,
            reason="우버 RRR 우위",
        )
        self.assertEqual(scenario["candidateId"], "UBER")
        self.assertEqual(scenario.get("sharesToSell"), 10)

        alert = RiskManagementAlert(
            alert_type="REVERSE_SWITCH_DEFENSE",
            severity="WARNING",
            stock_id="SK_SQUARE",
            message="방어 경고",
            action_guideline="홀딩 유지",
        )
        self.assertEqual(alert["alertType"], "REVERSE_SWITCH_DEFENSE")
        self.assertEqual(alert.get("severity"), "WARNING")


class TestAdversarialStressAndBoundaryCases(unittest.TestCase):
    """Stress tests and boundary condition verification for manager proposal engine."""

    def test_boundary_price_at_or_above_tp1(self) -> None:
        """When holding price reaches or exceeds TP1 (2,180,000 KRW), status phase triggers TP1 execution."""
        prop = TimingEngine.generate_manager_proposal(
            date="2026-10-12",
            portfolio={"holdingStock": "SK_SQUARE", "shares": 76, "currentPrice": 2200000.0},
        )
        self.assertEqual(prop.core_holding.status_phase, "TP1_REACHED_EXECUTE_SELL_38")
        self.assertEqual(prop.tactical_action, "TAKE_PROFIT_TP1")
        self.assertIn("TP1(218만 원) 달성", prop.action_headline)

    def test_boundary_catalyst_within_20_days_triggers_strict_hold(self) -> None:
        """When holding has confirmed catalyst within 20 days, triggers CATALYST_IMMINENT_STRICT_HOLD."""
        # By default in 2026-10-12, SK Square 자사주 소각 (2026-10-22) is D-10
        prop = TimingEngine.generate_manager_proposal(
            date="2026-10-12",
            portfolio={"holdingStock": "SK_SQUARE", "shares": 76, "currentPrice": 1050000.0},
        )
        self.assertEqual(prop.core_holding.status_phase, "CATALYST_IMMINENT_STRICT_HOLD")

    def test_take_profit_sk_square_tp1_exact_math(self) -> None:
        """SK Square TP1 in TimingEngine.get_take_profit must be 2,180,000 KRW with 38 shares recovery."""
        tp = TimingEngine.get_take_profit("SK_SQUARE")
        self.assertEqual(tp.tp1_price, 2180000.0)
        self.assertIn("38주 매도로 원금 8,284만 원", tp.tp1_action)
        self.assertIn("100% 무위험(Risk-Free) 회수", tp.tp1_action)

    def test_cli_timing_human_summary_mode(self) -> None:
        """CLI timing without --json outputs structured human-readable text."""
        cmd = [sys.executable, "-m", "engine.cli", "timing", "--date", "2026-10-12"]
        proc = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, encoding="utf-8", errors="replace", check=False)
        self.assertEqual(proc.returncode, 0)
        self.assertIn("=== 8-Stock Timing & Switching Diagnosis", proc.stdout)
        self.assertIn("SK Square 76 shares", proc.stdout)
        self.assertIn("2,180,000원", proc.stdout)
        self.assertIn("38주 매도로 원금 8,284만 원", proc.stdout)

    def test_cli_timing_with_input_file(self) -> None:
        """CLI timing --json with -i raw_input_latest.txt parses and produces valid JSON."""
        cmd = [sys.executable, "-m", "engine.cli", "timing", "-i", "raw_input_latest.txt", "--json"]
        proc = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, encoding="utf-8", errors="replace", check=False)
        self.assertEqual(proc.returncode, 0)
        parsed = json.loads(proc.stdout)
        self.assertIn("managerProposal", parsed)
        self.assertEqual(len(parsed["managerProposal"]["timeTo100Ranking"]), 8)

    def test_adversarial_past_and_future_dates(self) -> None:
        """Engine handles dates in distant past (2020) and future (2030) cleanly."""
        for test_date in ["2020-01-01", "2026-02-29", "2030-12-31"]:
            snap = TimingEngine.evaluate_daily_timing(DailyMarketData(date=test_date), as_of_date=test_date)
            self.assertIsNotNone(snap)
            self.assertIsNotNone(snap.manager_proposal)
            self.assertEqual(snap.date, test_date)

    def test_mathematical_recovery_invariants(self) -> None:
        """Invariants of 76 shares, 8,284만 원, 109만 원 avg cost, and 38 shares @ 218만 원."""
        diag = PortfolioDiagnostic()
        self.assertEqual(diag.shares, 76)
        self.assertEqual(diag.principal_krw, 82840000)
        self.assertEqual(diag.avg_cost_krw, 1090000)
        self.assertEqual(diag.tp1_shares_to_sell, 38)
        self.assertEqual(diag.tp1_target_price, 2180000.0)
        self.assertEqual(diag.tp1_recovered_amount, 82840000)
        # Mathematical identity: sell_shares * tp1_price == recovered_amount == principal
        self.assertEqual(diag.tp1_shares_to_sell * diag.tp1_target_price, diag.principal_krw)
        # Half of position remains
        self.assertEqual(diag.shares - diag.tp1_shares_to_sell, 38)


if __name__ == "__main__":
    unittest.main()
