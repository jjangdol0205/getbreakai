"""Command-Line Interface (CLI) for Multi-Stock Personal Investment Processing Engine.

Usage:
    python -m engine.cli clean -i raw_dump.txt -o cleaned.txt
    python -m engine.cli parse -i raw_dump.txt -o facts.json --date 2026-09-29
    python -m engine.cli parse -i raw_dump.txt --summary
    python -m engine.cli digest -i raw_dump.txt -o daily_digest/2026-09-29_digest.md
    python -m engine.cli digest -i raw_dump.txt --out-dir daily_digest
"""

from __future__ import annotations

import argparse
from datetime import datetime
import json
from pathlib import Path
import sys
from typing import Optional

from engine.cleaner import RawDumpCleaner, clean_raw_dump
from engine.extractor import FactExtractor, extract_facts


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="python -m engine.cli",
        description="Multi-Stock Personal Investment Processing Engine (R1: Raw Dump Cleaning & Extraction)"
    )
    subparsers = parser.add_subparsers(dest="command", help="Available subcommands")

    # 'clean' subcommand
    clean_parser = subparsers.add_parser("clean", help="Strip UI noise from raw chatbot dump")
    clean_parser.add_argument("-i", "--input", help="Path to input raw dump text file (default: stdin)")
    clean_parser.add_argument("-o", "--output", help="Path to output cleaned text file (default: stdout)")
    clean_parser.add_argument("--meta", action="store_true", help="Print cleaning metadata to stderr")

    # 'parse' subcommand
    parse_parser = subparsers.add_parser("parse", help="Clean raw dump and extract structured market facts")
    parse_parser.add_argument("-i", "--input", help="Path to input raw dump text file (default: stdin)")
    parse_parser.add_argument("-o", "--output", help="Path to output JSON file (default: stdout)")
    parse_parser.add_argument("-d", "--date", help="Override report date (YYYY-MM-DD)")
    parse_parser.add_argument("--summary", action="store_true", help="Print human-readable summary instead of JSON")
    parse_parser.add_argument("--indent", type=int, default=2, help="JSON indentation level (default: 2)")

    # 'digest' subcommand
    digest_parser = subparsers.add_parser("digest", help="Generate daily multi-stock digest markdown report")
    digest_parser.add_argument("-i", "--input", help="Path to input raw dump text file (default: stdin)")
    digest_parser.add_argument("-o", "--output", help="Path to output markdown file (default: stdout)")
    digest_parser.add_argument("-d", "--date", help="Override report date (YYYY-MM-DD)")
    digest_parser.add_argument("--out-dir", default="", help="Directory to save digest to (default: daily_digest)")

    # 'insight' subcommand
    insight_parser = subparsers.add_parser("insight", help="Generate daily deep investment insight markdown report")
    insight_parser.add_argument("-i", "--input", help="Path to input raw dump text file (default: stdin)")
    insight_parser.add_argument("-o", "--output", help="Path to output markdown file (default: stdout)")
    insight_parser.add_argument("-d", "--date", help="Override report date (YYYY-MM-DD)")
    insight_parser.add_argument("--out-dir", default="", help="Directory to save insight report to (default: daily_insight)")
    insight_parser.add_argument("--json", action="store_true", help="Output insight report as JSON")

    # 'timing' subcommand
    timing_parser = subparsers.add_parser("timing", help="Evaluate valuation bands, composite triggers, and switching recommendations")
    timing_parser.add_argument("-i", "--input", help="Path to input raw dump text file (default: stdin)")
    timing_parser.add_argument("-o", "--output", help="Path to output file (default: stdout)")
    timing_parser.add_argument("-d", "--date", help="Override report date (YYYY-MM-DD)")
    timing_parser.add_argument("--json", action="store_true", help="Output as JSON (default: human-readable summary)")
    timing_parser.add_argument("--indent", type=int, default=2, help="JSON indentation level (default: 2)")

    # 'weekly_pick' subcommand
    weekly_pick_parser = subparsers.add_parser(
        "weekly_pick",
        help="Screen 52-week low turnaround candidates, select top-pick, generate deep-dive report, and sync to data.js",
    )
    weekly_pick_parser.add_argument("-i", "--input", help="Path to input raw dump text file (optional)")
    weekly_pick_parser.add_argument("-o", "--output", help="Explicit path to output markdown report file")
    weekly_pick_parser.add_argument("-d", "--date", help="Override evaluation date (YYYY-MM-DD)")
    weekly_pick_parser.add_argument("--out-dir", default="weekly_picks", help="Directory to save deep-dive markdown report to (default: weekly_picks)")
    weekly_pick_parser.add_argument("--sync", action="store_true", help="Sync weekly screener data to data.js")
    weekly_pick_parser.add_argument("--data-js", default="", help="Path to target data.js file (default: root data.js)")
    weekly_pick_parser.add_argument("--json", action="store_true", help="Output screening result as JSON")
    weekly_pick_parser.add_argument("--indent", type=int, default=2, help="JSON indentation level (default: 2)")

    # 'sync' subcommand
    sync_parser = subparsers.add_parser("sync", help="Run full pipeline: clean raw dump, extract facts, generate digest & insight, and sync to data.js")
    sync_parser.add_argument("-i", "--input", help="Path to input raw dump text file (default: stdin)")
    sync_parser.add_argument("-d", "--date", help="Override report date (YYYY-MM-DD)")
    sync_parser.add_argument("--data-js", default="", help="Path to target data.js file (default: data.js in root)")
    sync_parser.add_argument("--digest-file", default="", help="Explicit path to write daily digest markdown file")
    sync_parser.add_argument("--digest-dir", default="daily_digest", help="Directory for daily digest output (default: daily_digest)")
    sync_parser.add_argument("--insight-file", default="", help="Explicit path to write daily deep insight markdown file")
    sync_parser.add_argument("--insight-dir", default="daily_insight", help="Directory for daily deep insight output (default: daily_insight)")
    sync_parser.add_argument("--weekly-picks-dir", default="weekly_picks", help="Directory for weekly turnaround report (default: weekly_picks)")
    sync_parser.add_argument("--weekly-file", default="", help="Explicit path to write weekly top-pick markdown file")
    sync_parser.add_argument("--quiet", action="store_true", help="Suppress status output messages")

    # 'backtest' subcommand
    backtest_parser = subparsers.add_parser(
        "backtest",
        help="Run 25-year institutional backtest simulation, optimization & report generator",
    )
    backtest_parser.add_argument("--sync", action="store_true", help="Sync backtest25yr store to data.js")
    backtest_parser.add_argument("--report", action="store_true", help="Generate backtest_report_25yr.md report")
    backtest_parser.add_argument("-o", "--output", help="Explicit path to output report markdown file")
    backtest_parser.add_argument("--data-js", default="", help="Path to target data.js file (default: root data.js)")
    backtest_parser.add_argument("--cycle", default="MONTHLY", help="Target rebalancing frequency (default: MONTHLY)")
    backtest_parser.add_argument("--step", type=float, default=0.10, help="Simplex grid step (default: 0.10)")
    backtest_parser.add_argument("--weights", default="0.35,0.35,0.30", help="Weights triplet QQQ,SOXX,Turnaround (default: 0.35,0.35,0.30)")
    backtest_parser.add_argument("--json", action="store_true", help="Output champion metrics as JSON to stdout")
    backtest_parser.add_argument("--quiet", action="store_true", help="Suppress status output messages")

    return parser


def read_input(input_path: Optional[str]) -> str:
    """Reads input text from file or stdin with UTF-8 encoding."""
    if input_path and input_path != "-":
        with open(input_path, "r", encoding="utf-8", errors="replace") as f:
            return f.read()
    else:
        return sys.stdin.read()


def write_output(content: str, output_path: Optional[str]) -> None:
    """Writes output text to file or stdout with UTF-8 encoding."""
    if output_path and output_path != "-":
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(content)
    else:
        sys.stdout.write(content)
        if not content.endswith("\n"):
            sys.stdout.write("\n")


def cmd_clean(args: argparse.Namespace) -> int:
    raw_text = read_input(args.input)
    cleaner = RawDumpCleaner()
    cleaned_text, metadata = cleaner.clean_with_metadata(raw_text)

    write_output(cleaned_text, args.output)

    if args.meta:
        sys.stderr.write("\n[Cleaning Metadata]\n")
        sys.stderr.write(json.dumps(metadata, ensure_ascii=False, indent=2))
        sys.stderr.write("\n")

    return 0


def cmd_parse(args: argparse.Namespace) -> int:
    raw_text = read_input(args.input)
    cleaner = RawDumpCleaner()
    cleaned_text, metadata = cleaner.clean_with_metadata(raw_text)

    extractor = FactExtractor()
    market_data = extractor.extract(cleaned_text, date_override=args.date)
    market_data.cleaned_metadata = metadata

    if args.summary:
        summary_lines = [
            f"=== Daily Multi-Stock Digest Data ({market_data.date}) ===",
            f"Macro Summary: {market_data.macro_summary}",
            f"Pair Strategy: {market_data.pair_strategy.action_label} | {market_data.pair_strategy.relative_spread}",
            "\n[Stock Fact Sheets]"
        ]
        for sid, sf in market_data.stocks.items():
            price = sf.metrics.close_price_formatted or f"{sf.metrics.close_price} {sf.metrics.currency}"
            change = sf.metrics.change_percent_formatted or f"{sf.metrics.change_percent}%"
            vol = sf.metrics.volume_formatted or str(sf.metrics.volume)
            summary_lines.append(
                f"- [{sid}] {sf.stock_name} ({sf.ticker}): {price} ({change}) | Vol: {vol}"
            )
            if sf.core_drivers:
                summary_lines.append(f"  Drivers ({len(sf.core_drivers)}): {sf.core_drivers[0]}")
            if sf.interviews:
                summary_lines.append(f"  Interview: {sf.interviews[0].speaker_name} ({sf.interviews[0].source_media})")
            if sf.ib_comments:
                summary_lines.append(f"  IB: {sf.ib_comments[0].brokerage} ({sf.ib_comments[0].rating_current})")

        write_output("\n".join(summary_lines), args.output)
    else:
        json_output = market_data.to_json(indent=args.indent)
        write_output(json_output, args.output)

    return 0


def cmd_digest(args: argparse.Namespace) -> int:
    raw_text = read_input(args.input)
    cleaner = RawDumpCleaner()
    cleaned_text, metadata = cleaner.clean_with_metadata(raw_text)

    date_override = args.date or metadata.get("date_hint")
    extractor = FactExtractor()
    market_data = extractor.extract(cleaned_text, date_override=date_override)
    market_data.cleaned_metadata = metadata

    from engine.timing_engine import TimingEngine
    from engine.digest_generator import generate_digest

    timing_snapshot = TimingEngine.evaluate_daily_timing(
        market_data,
        portfolio={"holdingStock": "SK_SQUARE", "shares": 76},
        as_of_date=market_data.date,
    )
    manager_proposal = getattr(timing_snapshot, "manager_proposal", None)

    out_dir = args.out_dir or "daily_digest"
    digest_content = generate_digest(market_data, output_dir=out_dir, manager_proposal=manager_proposal)

    if args.output:
        write_output(digest_content, args.output)
    else:
        write_output(digest_content, None)

    return 0


def cmd_insight(args: argparse.Namespace) -> int:
    raw_text = read_input(args.input)
    cleaner = RawDumpCleaner()
    cleaned_text, metadata = cleaner.clean_with_metadata(raw_text)

    date_override = args.date or metadata.get("date_hint")
    extractor = FactExtractor()
    market_data = extractor.extract(cleaned_text, date_override=date_override)
    market_data.cleaned_metadata = metadata

    from engine.timing_engine import TimingEngine
    from engine.insight_generator import InsightGenerator

    timing_snapshot = TimingEngine.evaluate_daily_timing(
        market_data,
        portfolio={"holdingStock": "SK_SQUARE", "shares": 76},
        as_of_date=market_data.date,
    )
    manager_proposal = getattr(timing_snapshot, "manager_proposal", None)

    out_dir = args.out_dir or "daily_insight"
    generator = InsightGenerator(output_dir=out_dir)
    report = generator.generate(market_data, raw_text=cleaned_text, output_dir=out_dir, manager_proposal=manager_proposal)

    if getattr(args, "json", False):
        write_output(report.to_json(), args.output)
    elif args.output:
        write_output(report.markdown_content, args.output)
    else:
        write_output(report.markdown_content, None)

    return 0


def cmd_timing(args: argparse.Namespace) -> int:
    raw_text = read_input(args.input) if args.input else ""
    metadata = {}
    if raw_text.strip():
        cleaner = RawDumpCleaner()
        cleaned_text, metadata = cleaner.clean_with_metadata(raw_text)
        date_override = args.date or metadata.get("date_hint")
        extractor = FactExtractor()
        market_data = extractor.extract(cleaned_text, date_override=date_override)
        market_data.cleaned_metadata = metadata
    else:
        from engine.models import DailyMarketData
        from datetime import date as dt_date
        eval_date = args.date or dt_date.today().strftime("%Y-%m-%d")
        market_data = DailyMarketData(date=eval_date, stocks={})

    # Enrich missing stock metrics via FinanceFeed fallback
    from engine.finance_feed import FinanceFeed
    from engine.models import StockSymbol, STOCK_MASTERS, MarketMetrics, StockFactSheet
    for sym_enum in StockSymbol:
        sid = sym_enum.value
        if sid not in market_data.stocks:
            quote = FinanceFeed.get_quote(sym_enum, date=market_data.date)
            if quote:
                master = STOCK_MASTERS[sym_enum]
                mock_metrics = MarketMetrics(
                    stock_id=sid,
                    currency=master.currency,
                    close_price=quote.close_price,
                    close_price_formatted=quote.close_price_formatted,
                    change_percent=quote.change_percent,
                    change_percent_formatted=quote.change_percent_formatted,
                    volume=quote.volume,
                    volume_formatted=quote.volume_formatted,
                    day_range=quote.day_range,
                )
                market_data.stocks[sid] = StockFactSheet(
                    stock_id=sid,
                    stock_name=master.name_kr,
                    name_kr=master.name_kr,
                    name_en=master.name_en,
                    ticker=master.ticker,
                    market=master.market,
                    category=master.category,
                    badge_color=master.badge_color,
                    metrics=mock_metrics,
                )

    from engine.timing_engine import TimingEngine
    snapshot = TimingEngine.evaluate_daily_timing(
        market_data,
        portfolio={"holdingStock": "SK_SQUARE", "shares": 76},
        as_of_date=args.date or market_data.date,
    )

    if args.json:
        output_content = json.dumps(snapshot.to_dict(), ensure_ascii=False, indent=args.indent)
        write_output(output_content, args.output)
    else:
        # Human-readable summary
        lines = [
            f"=== 8-Stock Timing & Switching Diagnosis ({snapshot.date}) ===",
            f"Portfolio Holding: SK Square 76 shares | Total Valuation: {snapshot.switching.holding_eval_amount}",
            f"Switching Status: {snapshot.switching.status} | {snapshot.switching.summary}",
            "\n[Stock Timing & Composite Triggers]"
        ]
        for sid, eval_obj in snapshot.stocks.items():
            tr = eval_obj.trigger
            band = eval_obj.valuation_band
            tp = eval_obj.take_profit
            lines.append(
                f"- [{sid}] {eval_obj.stock_name} ({eval_obj.ticker}): {tr.current_price_formatted} | "
                f"Signal: {tr.signal} (Score: {tr.composite_score}/3) | RRR: {tr.risk_reward_ratio:.2f} | Dead Money: {tr.dead_money_risk}"
            )
            lines.append(f"  Safety Band: {band.min_price_formatted} ~ {band.max_price_formatted} (Support: {band.key_support_formatted})")
            lines.append(f"  TP Roadmap: TP1 {tp.tp1_price_formatted} ({tp.tp1_action}) -> TP2 {tp.tp2_price_formatted} ({tp.tp2_action})")
            if eval_obj.catalysts:
                imminent_cats = [c for c in eval_obj.catalysts if 0 <= c.days_remaining <= 60]
                if imminent_cats:
                    lines.append(f"  Catalysts ({len(imminent_cats)} imminent): [D-{imminent_cats[0].days_remaining}] {imminent_cats[0].name}")

        if snapshot.switching.scenarios:
            lines.append("\n[Reallocation Scenarios]")
            for sc in snapshot.switching.scenarios:
                lines.append(f"- {sc['title']} ({sc['freedCapital']} 재배분)")

        write_output("\n".join(lines), args.output)

    return 0


def cmd_weekly_pick(args: argparse.Namespace) -> int:
    eval_date = args.date
    if not eval_date and args.input:
        raw_text = read_input(args.input)
        if raw_text.strip():
            cleaner = RawDumpCleaner()
            _, metadata = cleaner.clean_with_metadata(raw_text)
            eval_date = metadata.get("date_hint")

    if not eval_date:
        eval_date = datetime.now().strftime("%Y-%m-%d")

    from engine.turnaround_screener import TurnaroundScreener, generate_weekly_deep_dive_report
    from engine.sync_dashboard import build_weekly_screener_store, load_data_store, save_data_store, DEFAULT_DATA_JS_PATH

    candidates = TurnaroundScreener.screen_universe(date=eval_date)
    top_pick = TurnaroundScreener.select_weekly_top_pick(candidates, date=eval_date)

    if not top_pick:
        sys.stderr.write(f"[CLI Error] No qualified turnaround top-pick found for date {eval_date}.\n")
        return 1

    cand = top_pick.candidate

    # Generate deep dive report
    out_dir = args.out_dir or "weekly_picks"
    report_target = args.output or out_dir
    report_content = generate_weekly_deep_dive_report(top_pick, output_dir=report_target)
    report_file_path = f"{out_dir}/{eval_date}_{cand.ticker}.md" if not (args.output and args.output.endswith(".md")) else args.output

    # If --sync is requested:
    if args.sync:
        target_path = Path(args.data_js) if args.data_js else DEFAULT_DATA_JS_PATH
        data_store = load_data_store(target_path)
        existing_screener = data_store.get("weeklyScreener")
        data_store["weeklyScreener"] = build_weekly_screener_store(
            candidates=candidates,
            top_pick=top_pick,
            date=eval_date,
            existing_store=existing_screener,
        )
        saved = save_data_store(data_store, target_path)
        if not saved:
            sys.stderr.write("[CLI Error] Failed to sync weekly screener data to data.js\n")
            return 1

    # Output representation
    if args.json:
        payload = {
            "date": eval_date,
            "topPick": top_pick.to_dict(),
            "candidates": [c.to_dict() for c in candidates],
            "markdownPath": report_file_path,
        }
        write_output(json.dumps(payload, ensure_ascii=False, indent=args.indent), None if args.output and args.output.endswith(".md") else args.output)
    else:
        lines = [
            f"=== [Weekly Turnaround Screener Top-Pick ({eval_date})] ===",
            f"Top-Pick: {cand.name_kr} ({cand.ticker}) | {cand.market} ({cand.currency})",
            f"Current Price: {cand.current_price_formatted} (52W Low Proximity: +{cand.proximity_52w_low_pct:.1f}%)",
            f"Risk/Reward: 1 : {cand.risk_reward_ratio:.1f} (Downside: -{cand.downside_risk_pct:.1f}% vs TP1: +{cand.upside_tp1_pct:.1f}%)",
            f"Composite Score: {cand.composite_turnaround_score:.1f} / 100.0 (Tier: {cand.conviction_tier})",
            f"Report Generated: {report_file_path}",
            "",
            "Candidates Evaluated:",
        ]
        for idx, c in enumerate(candidates, 1):
            lines.append(
                f"  {idx}. {c.name_kr} ({c.ticker}): {c.current_price_formatted} | "
                f"Score: {c.composite_turnaround_score:.1f} | RRR: {c.risk_reward_ratio:.1f}x | "
                f"Tier: {c.conviction_tier}"
            )
        if args.sync:
            lines.append(f"\n[Dashboard Sync] Successfully synced weeklyScreener store to {args.data_js or 'data.js'}")

        output_txt = "\n".join(lines) + "\n"
        if not args.output or args.output.endswith(".md"):
            sys.stdout.write(output_txt)
        else:
            write_output(output_txt, args.output)

    return 0


def cmd_sync(args: argparse.Namespace) -> int:
    raw_text = read_input(args.input)
    if not raw_text.strip():
        sys.stderr.write("[CLI Error] Empty input provided to sync command.\n")
        return 1

    cleaner = RawDumpCleaner()
    cleaned_text, metadata = cleaner.clean_with_metadata(raw_text)

    date_override = args.date or metadata.get("date_hint")
    extractor = FactExtractor()
    market_data = extractor.extract(cleaned_text, date_override=date_override)
    market_data.cleaned_metadata = metadata

    from engine.finance_feed import FinanceFeed
    from engine.models import StockSymbol, STOCK_MASTERS, MarketMetrics, StockFactSheet
    if len(market_data.stocks) >= 3:
        for sym_enum in StockSymbol:
            sid = sym_enum.value
            if sid not in market_data.stocks:
                quote = FinanceFeed.get_quote(sym_enum, date=market_data.date)
                if quote:
                    master = STOCK_MASTERS[sym_enum]
                    mock_metrics = MarketMetrics(
                        stock_id=sid,
                        currency=master.currency,
                        close_price=quote.close_price,
                        close_price_formatted=quote.close_price_formatted,
                        change_percent=quote.change_percent,
                        change_percent_formatted=quote.change_percent_formatted,
                        volume=quote.volume,
                        volume_formatted=quote.volume_formatted,
                        day_range=quote.day_range,
                    )
                    market_data.stocks[sid] = StockFactSheet(
                        stock_id=sid,
                        stock_name=master.name_kr,
                        name_kr=master.name_kr,
                        name_en=master.name_en,
                        ticker=master.ticker,
                        market=master.market,
                        category=master.category,
                        badge_color=master.badge_color,
                        metrics=mock_metrics,
                    )
            elif market_data.stocks[sid].metrics:
                m = market_data.stocks[sid].metrics
                quote = FinanceFeed.get_quote(sym_enum, date=market_data.date)
                if quote:
                    if m.volume is None and quote.volume is not None:
                        m.volume = quote.volume
                        m.volume_formatted = quote.volume_formatted
                    if m.close_price is None and quote.close_price is not None:
                        m.close_price = quote.close_price
                        m.close_price_formatted = quote.close_price_formatted


    # 1. Evaluate Timing Engine & AI Fund Manager Proposal prior to report generation
    from engine.timing_engine import TimingEngine
    timing_snapshot = TimingEngine.evaluate_daily_timing(
        market_data,
        portfolio={"holdingStock": "SK_SQUARE", "shares": 76},
        as_of_date=market_data.date,
    )
    manager_proposal = getattr(timing_snapshot, "manager_proposal", None)

    # 2. Generate Daily Multi-Stock Digest (with AI Head Fund Manager subsection in Section 4)
    from engine.digest_generator import generate_digest
    out_target = getattr(args, "digest_file", "") or getattr(args, "digest_dir", "daily_digest") or "daily_digest"
    digest_content = generate_digest(market_data, output_dir=out_target, manager_proposal=manager_proposal)

    # 3. Generate Daily Deep Insight Report (with Section 5 Manager's Daily Journal)
    from engine.insight_generator import generate_insight
    insight_target = getattr(args, "insight_file", "") or getattr(args, "insight_dir", "daily_insight") or "daily_insight"
    insight_report = generate_insight(market_data, raw_text=cleaned_text, output_dir=insight_target, manager_proposal=manager_proposal)

    # 4. Evaluate Turnaround Screener & Generate Weekly Top-Pick Deep-Dive Report
    from engine.turnaround_screener import TurnaroundScreener, generate_weekly_deep_dive_report
    screener_candidates = TurnaroundScreener.screen_universe(date=market_data.date)
    weekly_top_pick = TurnaroundScreener.select_weekly_top_pick(screener_candidates, date=market_data.date)
    weekly_pick_summary = ""
    if weekly_top_pick:
        weekly_picks_dir = getattr(args, "weekly_picks_dir", "weekly_picks") or "weekly_picks"
        weekly_target = getattr(args, "weekly_file", "") or weekly_picks_dir
        generate_weekly_deep_dive_report(weekly_top_pick, output_dir=weekly_target)
        cand_p = weekly_top_pick.candidate
        report_file_path = f"{weekly_picks_dir}/{market_data.date}_{cand_p.ticker}.md" if not getattr(args, "weekly_file", "") else args.weekly_file
        weekly_pick_summary = f"Top-Pick {cand_p.ticker} ({cand_p.current_price_formatted}, RRR {cand_p.risk_reward_ratio:.1f}, Score {cand_p.composite_turnaround_score:.1f}) -> {report_file_path}"

    # 5. Synchronize reports, records, timing, manager journal, and weekly screener into data.js
    from engine.sync_dashboard import sync_to_dashboard
    success = sync_to_dashboard(
        market_data,
        digest_md=digest_content,
        data_js_path=args.data_js,
        insight_report=insight_report,
        timing_snapshot=timing_snapshot,
        manager_proposal=manager_proposal,
        weekly_screener=(screener_candidates, weekly_top_pick),
    )
    if not success:
        sys.stderr.write("[CLI Error] Failed to sync data to data.js\n")
        return 1

    if not args.quiet:
        sys.stdout.write(
            f"[Pipeline Sync Complete]\n"
            f"  - Date: {market_data.date}\n"
            f"  - Stocks Processed: {len(market_data.stocks)} ({', '.join(market_data.stocks.keys())})\n"
            f"  - Digest Output: {out_target}\n"
            f"  - Insight Output: {insight_target}\n"
            f"  - Timing Analysis: 8 stocks evaluated & SK Square 76 shares diagnosed\n"
            f"  - Manager Journal: AI Head Fund Manager proposal archived\n"
        )
        if weekly_pick_summary:
            sys.stdout.write(f"  - Weekly Screener: {weekly_pick_summary}\n")
        sys.stdout.write(f"  - Dashboard Target: {args.data_js or 'data.js'}\n")
    return 0


def cmd_backtest(args: argparse.Namespace) -> int:
    """Executes 25-year institutional backtest simulation, report generation, and data.js synchronization."""
    from engine.strategy_hybrid_master import (
        HybridWeightVector,
        RebalanceFrequency,
        StrategyHybridMaster,
        normalize_cycle,
    )
    from engine.backtest_report import generate_backtest_report, DEFAULT_REPORT_PATH
    from engine.sync_dashboard import sync_backtest_to_dashboard, build_backtest25yr_store

    # 1. Parse weights
    weights_tuple = (0.35, 0.35, 0.30)
    if getattr(args, "weights", ""):
        try:
            parts = [float(x.strip()) for x in args.weights.split(",") if x.strip()]
            if len(parts) == 3:
                weights_tuple = (parts[0], parts[1], parts[2])
        except Exception:
            pass
    target_weights = HybridWeightVector(*weights_tuple)
    target_cycle = normalize_cycle(getattr(args, "cycle", "MONTHLY"))

    # 2. Run simulation
    eval_res = StrategyHybridMaster.simulate_hybrid(
        weights=target_weights,
        cycle=target_cycle,
    )

    # 3. Handle JSON output
    if getattr(args, "json", False):
        store_dict = build_backtest25yr_store(
            champion_weights=target_weights,
            cycle=target_cycle,
        )
        sys.stdout.write(json.dumps(store_dict, ensure_ascii=False, indent=2) + "\n")
        return 0

    # 4. Handle Report generation
    # Default behavior: generate report if --report flag is given OR if neither --sync nor --json is specified
    report_file_path = ""
    if getattr(args, "report", False) or not getattr(args, "sync", False):
        out_target = getattr(args, "output", "") or DEFAULT_REPORT_PATH
        generate_backtest_report(
            output_path=out_target,
            champion_weights=target_weights,
            champion_cycle=target_cycle,
        )
        report_file_path = str(out_target)

    # 5. Handle data.js synchronization
    synced = False
    if getattr(args, "sync", False):
        data_js_target = getattr(args, "data_js", "")
        synced = sync_backtest_to_dashboard(
            champion_weights=target_weights,
            cycle=target_cycle,
            data_js_path=data_js_target,
        )

    # 6. Terminal status output
    if not getattr(args, "quiet", False):
        sys.stdout.write(
            f"[25-Year Institutional Backtest Complete]\n"
            f"  - Champion Allocation: QQQ {int(target_weights.w_qqq*100)}% / SOXX {int(target_weights.w_soxx*100)}% / Turnaround {int(target_weights.w_turnaround*100)}%\n"
            f"  - Rebalance Cycle: {target_cycle.value}\n"
            f"  - CAGR: Pre-Tax {eval_res.cagr_pre_tax:.2f}% | After-Tax {eval_res.cagr_after_tax:.2f}%\n"
            f"  - MDD: Pre-Tax {eval_res.mdd_pre_tax:.2f}% | After-Tax {eval_res.mdd_after_tax:.2f}%\n"
            f"  - Calmar: Pre-Tax {eval_res.calmar_pre_tax:.2f} | After-Tax {eval_res.calmar_after_tax:.2f}\n"
            f"  - Sharpe: Pre-Tax {eval_res.sharpe_pre_tax:.2f} | After-Tax {eval_res.sharpe_after_tax:.2f}\n"
            f"  - Tax Drag: {eval_res.tax_drag_pct:.2f}%p (Total Tax: {int(eval_res.total_tax_paid/10000):,}만 원)\n"
        )
        if report_file_path:
            sys.stdout.write(f"  - Report Output: {report_file_path}\n")
        if getattr(args, "sync", False):
            sys.stdout.write(f"  - Dashboard Sync: {'Success' if synced else 'Failed'} -> {args.data_js or 'data.js'}\n")

    return 0


def main(argv: Optional[List[str]] = None) -> int:
    if hasattr(sys.stdin, "reconfigure"):
        try:
            sys.stdin.reconfigure(encoding="utf-8")
        except Exception:
            pass
    if hasattr(sys.stdout, "reconfigure"):
        try:
            sys.stdout.reconfigure(encoding="utf-8")
        except Exception:
            pass

    parser = build_parser()
    args = parser.parse_args(argv)

    if not args.command:
        parser.print_help()
        return 1

    if args.command == "clean":
        return cmd_clean(args)
    elif args.command == "parse":
        return cmd_parse(args)
    elif args.command == "digest":
        return cmd_digest(args)
    elif args.command == "insight":
        return cmd_insight(args)
    elif args.command == "timing":
        return cmd_timing(args)
    elif args.command == "weekly_pick":
        return cmd_weekly_pick(args)
    elif args.command == "sync":
        return cmd_sync(args)
    elif args.command == "backtest":
        return cmd_backtest(args)
    else:
        parser.print_help()
        return 1


if __name__ == "__main__":
    sys.exit(main())
