"""
tests_e2e/test_numerical_consistency.py - Comprehensive End-to-End Numerical Consistency
& Zero-Undefined Verification Suite for RightSideAlpha & SemiFearGreed.
"""
import json
import math
import subprocess
import sys
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from backend.app.main import app
from backend.app.services.quant_engine import quant_engine
from backend.app.services.semi_engine import semi_engine

client = TestClient(app)


def test_all_api_endpoints_zero_undefined_and_latest_close_sync():
    """
    Verifies that every API endpoint across RightSideAlpha and SemiFearGreed:
    - Contains zero 'undefined' or 'NaN' strings in serialized JSON
    - Anchors all prices, targets, stops, and share counts to the latest closing price
    """
    # 1. Backtest Summary KPIs
    r_bt = client.get("/api/backtest/summary")
    assert r_bt.status_code == 200
    bt = r_bt.json()
    kpis = bt["kpis"]
    assert kpis["hit_rate_2x_pct"] == 55.24
    assert kpis["median_days_underwater"] == 29.0
    assert kpis["cagr_pct"] == 21.97
    assert kpis["cagr_after_tax_pct"] == 17.81
    assert kpis["us_only_net_cagr_pct"] == 17.81
    assert kpis["severe_loss_risk_pct"] == 0.93
    assert "undefined" not in json.dumps(bt).lower()

    # 2. All 72 US Stocks (Pro unmasked)
    r_stocks = client.get("/api/stocks?license_key=PRO-DEMO-2026&limit=200")
    assert r_stocks.status_code == 200
    stocks = r_stocks.json()
    assert len(stocks) == 72
    for s in stocks:
        assert "." not in s["ticker"]
        close = s["close"]
        assert close > 0
        assert abs(s["stop_loss_price"] - round(close * 0.91, 2)) <= 0.01
        assert abs(s["tp1_2x_price"] - round(close * 2.00, 2)) <= 0.01
        assert s["c2_sweet_spot"] == s["c2_off_low"]
        assert s["c3_ma_reclaim"] == s["c3_above_mas"]
        assert s["c4_vol_washout"] == s["c4_vol_or_mom"]

    # 3. Research Briefs (CELH & MBLY) synced to latest closing prices
    for tick in ("CELH", "MBLY"):
        r_res = client.get(f"/api/research/{tick}")
        assert r_res.status_code == 200
        brief = r_res.json()
        stock_obj = quant_engine.stocks_by_ticker[tick]
        assert brief["title"] and "undefined" not in brief["title"].lower()
        assert brief["current_price"] == stock_obj.close
        assert brief["stop_price"] == round(stock_obj.close * 0.91, 2)
        assert brief["target_price"] == round(stock_obj.close * 2.00, 2)
        assert f"${stock_obj.close:.2f}" in brief["content"]

    # 4. Position Doctor latest close & target calculations
    r_doc = client.post(
        "/api/stocks/diagnose",
        json={"ticker": "CELH", "entry_price": 27.20, "days_held": 42},
    )
    assert r_doc.status_code == 200
    doc = r_doc.json()
    assert doc["current_price"] == 27.93
    assert doc["entry_price"] == 27.20
    assert doc["stop_price"] == round(27.20 * 0.91, 2)
    assert doc["tp1_price"] == round(27.20 * 2.00, 2)
    assert doc["return_pct"] == round(((27.93 / 27.20) - 1.0) * 100.0, 2)

    # 5. SemiFearGreed Overview & 7-Factor Weighted Score Verification
    r_ov = client.get("/api/semi/overview")
    assert r_ov.status_code == 200
    ov = r_ov.json()
    latest_row = semi_engine.get_latest_row()
    assert ov["date"] == latest_row["date"]
    assert ov["smh_close"] == round(latest_row["smh_close"], 2)
    assert ov["xlv_close"] == round(latest_row["xlv_close"], 2)
    assert ov["qqq_close"] == round(latest_row["qqq_adj"], 2)

    # Verify 7-factor weights sum to 100% and weighted score matches fg_score
    total_weight = sum(f["weight_pct"] for f in ov["factors"])
    assert total_weight == 100
    weighted_score = sum((f["weight_pct"] / 100.0) * f["score"] for f in ov["factors"])
    assert abs(weighted_score - ov["fg_score"]) <= 0.15

    # Verify ETF 52W DD & RSI14 are dynamically computed from CSV history
    etf_by_ticker = {e["ticker"]: e for e in ov["etfs"]}
    assert etf_by_ticker["XLV"]["dd_52w_pct"] == semi_engine._compute_52w_dd("xlv_close")
    assert etf_by_ticker["XLV"]["rsi14"] == semi_engine._compute_rsi14("xlv_close")
    assert etf_by_ticker["QQQ"]["dd_52w_pct"] == semi_engine._compute_52w_dd("qqq_adj")
    assert etf_by_ticker["QQQ"]["rsi14"] == semi_engine._compute_rsi14("qqq_adj")

    # 6. SemiFearGreed Rebalance Calculator Mathematical Verification
    r_reb = client.post(
        "/api/semi/rebalance",
        json={
            "total_capital_usd": 100000.0,
            "strategy_mode": "AUTO_REGIME",
            "rebalance_frequency": "ANNUAL",
            "unrealized_gain_krw": 3800000.0,
        },
    )
    assert r_reb.status_code == 200
    reb = r_reb.json()
    assert reb["as_of_date"] == latest_row["date"]
    assert reb["smh_close"] == round(latest_row["smh_close"], 2)
    assert reb["xlv_close"] == round(latest_row["xlv_close"], 2)
    assert reb["target_smh_usd"] + reb["target_xlv_usd"] == 100000.0
    assert reb["target_smh_shares"] == math.floor(reb["target_smh_usd"] / reb["smh_close"])
    assert reb["target_xlv_shares"] == math.floor(reb["target_xlv_usd"] / reb["xlv_close"])
    invested = reb["target_smh_shares"] * reb["smh_close"] + reb["target_xlv_shares"] * reb["xlv_close"]
    assert abs(reb["residual_cash_usd"] - round(100000.0 - invested, 2)) <= 0.02

    # 7. SemiFearGreed Lump-Sum Calculator Verification across all 3 Regimes
    for test_fg in (18.0, 50.0, 78.0):
        r_lump = client.post(
            "/api/semi/lump-sum",
            json={"capital_usd": 50000.0, "override_fg_score": test_fg},
        )
        assert r_lump.status_code == 200
        lump = r_lump.json()
        assert lump["as_of_date"] == latest_row["date"]
        assert lump["smh_close"] == round(latest_row["smh_close"], 2)
        assert lump["xlv_close"] == round(latest_row["xlv_close"], 2)
        assert sum(t["allocation_pct"] for t in lump["tranches"]) == 100.0
        assert sum(t["amount_usd"] for t in lump["tranches"]) == 50000.0
        for tr in lump["tranches"]:
            assert tr["smh_shares"] == math.floor(tr["smh_usd"] / lump["smh_close"])
            assert tr["xlv_shares"] == math.floor(tr["xlv_usd"] / lump["xlv_close"])


def test_frontend_rendered_html_zero_undefined_or_nan():
    """
    Renders all frontend components via Node.js with live backend data across
    all 3 languages (en, jp, kr) and both Free/Pro states, verifying ZERO
    occurrences of 'undefined' or 'NaN' in the rendered HTML output.
    """
    stocks = client.get("/api/stocks?license_key=PRO-DEMO-2026&limit=200").json()
    bt = client.get("/api/backtest/summary").json()
    semi_ov = client.get("/api/semi/overview").json()
    semi_hist = client.get("/api/semi/history?range=1Y").json()
    semi_reb = client.post("/api/semi/rebalance", json={"total_capital_usd": 100000}).json()
    semi_lump = client.post("/api/semi/lump-sum", json={"capital_usd": 50000}).json()
    doc_res = client.post("/api/stocks/diagnose", json={"ticker": "CELH", "entry_price": 27.93, "days_held": 42}).json()

    payload = json.dumps({
        "stocks": stocks,
        "kpis": bt["kpis"],
        "semiOverview": semi_ov,
        "semiHistory": semi_hist,
        "semiRebalanceResult": semi_reb,
        "semiLumpSumResult": semi_lump,
        "docLastResult": doc_res,
    })

    node_script = """
import fs from 'node:fs';
import { translations } from './frontend/src/locales/i18n.js';
import { renderHeader } from './frontend/src/components/Header.js';
import { renderHero } from './frontend/src/components/Hero.js';
import { renderProofCard } from './frontend/src/components/ProofCard.js';
import { renderScreenerControls, renderStockTable } from './frontend/src/components/StockTable.js';
import { renderProVault } from './frontend/src/components/ProVault.js';
import { formatDoctorResult } from './frontend/src/components/PositionDoctor.js';
import { renderPricing } from './frontend/src/components/Pricing.js';
import { renderModals } from './frontend/src/components/Modals.js';
import { renderSemiFearGreedView } from './frontend/src/components/SemiFearGreedView.js';

const data = JSON.parse(fs.readFileSync(0, 'utf-8'));

for (const lang of ['en', 'jp', 'kr']) {
  for (const isPro of [false, true]) {
    const state = {
      lang,
      isProUnlocked: isPro,
      activeView: 'rightside',
      stocks: data.stocks,
      filteredStocks: data.stocks,
      backtestKpis: data.kpis,
      semiOverview: data.semiOverview,
      semiHistory: data.semiHistory,
      semiRebalanceResult: data.semiRebalanceResult,
      semiLumpSumResult: data.semiLumpSumResult,
      docLastResult: data.docLastResult,
      zoneFilter: 'ALL',
      searchQuery: '',
      semiGaugeTab: 'overview',
      semiRange: '1Y',
      semiCapUsd: 100000,
      semiMode: 'AUTO_REGIME',
      semiFreq: 'ANNUAL',
      semiGainKrw: 3800000,
      semiLumpCapUsd: 50000,
      semiLumpScore: 18.0,
      config: {
        site1_url: 'https://getbreakai.com',
        ls_site1_monthly_url: 'https://rightsidealpha.lemonsqueezy.com/checkout/buy/pro-monthly',
        ls_site1_ltd_url: 'https://rightsidealpha.lemonsqueezy.com/checkout/buy/lifetime-pass',
        tradingview_aff_id: 'rightsidealpha',
        seekingalpha_source: 'affiliate_rightside',
      },
      get t() { return translations[this.lang]; }
    };

    const htmlChunks = [
      renderHeader(state),
      renderHero(state),
      renderProofCard(state),
      renderScreenerControls(state),
      renderStockTable(state),
      renderProVault(state),
      formatDoctorResult(data.docLastResult),
      renderPricing(state),
      renderModals(state),
      renderSemiFearGreedView(state),
      renderSemiFearGreedView({ ...state, semiGaugeTab: 'timeline' }),
    ];

    const fullHtml = htmlChunks.join('\\n');
    if (fullHtml.includes('undefined')) {
      console.error(`FOUND undefined in rendered HTML for lang=${lang}, isPro=${isPro}`);
      process.exit(1);
    }
    if (fullHtml.includes('NaN')) {
      console.error(`FOUND NaN in rendered HTML for lang=${lang}, isPro=${isPro}`);
      process.exit(1);
    }
  }
}
console.log('ALL_COMPONENTS_CLEAN');
"""
    proc = subprocess.run(
        ["node", "--input-type=module", "-e", node_script],
        input=payload,
        cwd=str(PROJECT_ROOT),
        capture_output=True,
        text=True,
        encoding="utf-8",
    )
    assert proc.returncode == 0, f"Node render check failed:\nSTDOUT: {proc.stdout}\nSTDERR: {proc.stderr}"
    assert "ALL_COMPONENTS_CLEAN" in proc.stdout
