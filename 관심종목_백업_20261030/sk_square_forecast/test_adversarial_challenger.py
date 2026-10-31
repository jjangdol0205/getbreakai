#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
test_adversarial_challenger.py - Empirical Challenger Verification & Stress Harness.
Audits:
1. Scenario probabilities sum to 1.0 (100%).
2. Mathematical formula identity: P_target = NAV_target * (1 - Target_Discount).
3. Expected value calculations (weighted sum).
4. Investor 76-share position math & TP1 recovery roadmap.
5. Zero-CDN offline self-containment for dashboard.html and charts/*.html.
"""

import os
import re
import json
import math
import pandas as pd

WORKSPACE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(WORKSPACE_DIR, "data")
CHARTS_DIR = os.path.join(WORKSPACE_DIR, "charts")

def test_scenario_probabilities():
    path = os.path.join(DATA_DIR, "scenario_matrix.json")
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    results = {}
    for h_name, h_data in data["horizons"].items():
        p_bull = h_data["bull"]["probability_pct"]
        p_base = h_data["base"]["probability_pct"]
        p_bear = h_data["bear"]["probability_pct"]
        tot = p_bull + p_base + p_bear
        results[h_name] = {
            "bull": p_bull,
            "base": p_base,
            "bear": p_bear,
            "sum": tot,
            "valid": (tot == 100)
        }
    return results

def test_portfolio_math():
    path = os.path.join(DATA_DIR, "scenario_matrix.json")
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    port = data["user_portfolio"]
    shares = port["shares"]
    avg_cost = port["avg_cost_unit_krw"]
    principal = port["principal_krw"]
    cur_price = port["current_price_unit_krw"]
    cur_val = port["current_value_krw"]
    unrealized_pnl = port["unrealized_pnl_krw"]
    unrealized_pct = port["unrealized_return_pct"]

    calc_principal = shares * avg_cost
    calc_cur_val = shares * cur_price
    calc_pnl = calc_cur_val - calc_principal
    calc_return_pct = round((calc_pnl / calc_principal) * 100.0, 2)

    tp1_price = port["tp1_target_unit_price_krw"]
    tp1_sell = port["tp1_shares_to_sell"]
    tp1_cash = port["tp1_recovered_cash_krw"]
    tp1_rem = port["tp1_remaining_shares"]
    tp1_free = port["tp1_free_carry_value_krw"]

    calc_tp1_cash = tp1_sell * tp1_price
    calc_tp1_recovery_pct = (calc_tp1_cash / calc_principal) * 100.0
    calc_tp1_free = tp1_rem * tp1_price

    checks = {
        "principal_match": (principal == calc_principal == 82_840_000),
        "current_val_match": (cur_val == calc_cur_val == 65_132_000.0),
        "unrealized_pnl_match": (unrealized_pnl == calc_pnl == -17_708_000.0),
        "unrealized_return_pct_match": (unrealized_pct == calc_return_pct == -21.38),
        "tp1_price": tp1_price,
        "tp1_cash_recovers_100pct": (tp1_cash == calc_tp1_cash == calc_principal),
        "tp1_recovery_rate_pct": calc_tp1_recovery_pct,
        "remaining_shares_is_half": (tp1_rem == shares - tp1_sell == 38),
        "free_carry_val": calc_tp1_free,
        "is_risk_free": (calc_tp1_cash >= calc_principal)
    }
    return checks

def test_target_price_identity():
    sc_path = os.path.join(DATA_DIR, "scenario_matrix.json")
    seed_path = os.path.join(DATA_DIR, "seed_market_data.json")

    with open(sc_path, "r", encoding="utf-8") as f:
        sc = json.load(f)
    with open(seed_path, "r", encoding="utf-8") as f:
        seed = json.load(f)

    cfg = seed["fundamental_config"]
    n_sq = cfg["sk_square_shares_total"]
    n_hy = cfg["hynix_shares_held"]
    v_unlisted = cfg["unlisted_asset_value_krw"]
    net_debt = cfg["net_debt_krw"]

    discrepancies = []
    for h_name, h_data in sc["horizons"].items():
        for s_key in ["bull", "base", "bear"]:
            s = h_data[s_key]
            p_hy = s["hynix_target_krw"]
            stated_disc = s["target_discount_pct"]
            reported_sq_share = s["square_target_share_krw"]
            reported_sq_unit = s["square_target_unit_krw"]

            tot_nav = (p_hy * n_hy) + v_unlisted - net_debt
            nav_per_share = tot_nav / n_sq
            nav_unit = nav_per_share * 10.0

            # Price from stated discount
            formula_price_share = nav_per_share * (1.0 - (stated_disc / 100.0))
            formula_price_unit = formula_price_share * 10.0

            # Discount implied by reported price
            implied_disc_pct = (1.0 - (reported_sq_share / nav_per_share)) * 100.0

            diff_share = reported_sq_share - formula_price_share
            diff_pct = (diff_share / formula_price_share) * 100.0

            discrepancies.append({
                "horizon": h_name,
                "regime": s_key,
                "hynix_target": p_hy,
                "nav_per_share": round(nav_per_share, 2),
                "stated_discount_pct": stated_disc,
                "formula_price_share": round(formula_price_share, 2),
                "reported_sq_share": reported_sq_share,
                "diff_share": round(diff_share, 2),
                "diff_pct": round(diff_pct, 2),
                "implied_discount_pct": round(implied_disc_pct, 2)
            })
    return discrepancies

def test_expected_values():
    path = os.path.join(DATA_DIR, "scenario_matrix.json")
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    base_unit = data["base_square_price_unit"]
    ev_checks = []
    for h_name, h_data in data["horizons"].items():
        w_bull = h_data["bull"]["probability_pct"] / 100.0
        w_base = h_data["base"]["probability_pct"] / 100.0
        w_bear = h_data["bear"]["probability_pct"] / 100.0

        u_bull = h_data["bull"]["square_target_unit_krw"]
        u_base = h_data["base"]["square_target_unit_krw"]
        u_bear = h_data["bear"]["square_target_unit_krw"]

        r_bull = h_data["bull"]["expected_return_pct"]
        r_base = h_data["base"]["expected_return_pct"]
        r_bear = h_data["bear"]["expected_return_pct"]

        calc_ev_unit = w_bull * u_bull + w_base * u_base + w_bear * u_bear
        calc_ev_ret = ((calc_ev_unit - base_unit) / base_unit) * 100.0

        rep_ev_unit = h_data["expected_value_unit_krw"]
        rep_ev_ret = h_data["expected_return_pct"]

        ev_checks.append({
            "horizon": h_name,
            "calc_ev_unit": calc_ev_unit,
            "rep_ev_unit": rep_ev_unit,
            "unit_match": (abs(calc_ev_unit - rep_ev_unit) < 1.0),
            "calc_ev_ret": round(calc_ev_ret, 2),
            "rep_ev_ret": rep_ev_ret,
            "ret_match": (abs(calc_ev_ret - rep_ev_ret) < 0.05)
        })
    return ev_checks

def test_offline_zero_cdn():
    html_files = ["dashboard.html"]
    if os.path.exists(CHARTS_DIR):
        for f in os.listdir(CHARTS_DIR):
            if f.endswith(".html"):
                html_files.append(os.path.join("charts", f))

    findings = []
    cdn_pattern = re.compile(r'(cdn\.jsdelivr\.net|cdnjs\.cloudflare\.com|unpkg\.com|ajax\.googleapis\.com|fonts\.googleapis\.com|fonts\.gstatic\.com)', re.IGNORECASE)
    remote_script_pattern = re.compile(r'<script[^>]+src=[\'"]https?:', re.IGNORECASE)
    remote_link_pattern = re.compile(r'<link[^>]+href=[\'"]https?:', re.IGNORECASE)

    for hf in html_files:
        full_path = os.path.join(WORKSPACE_DIR, hf)
        if not os.path.exists(full_path):
            continue
        with open(full_path, "r", encoding="utf-8") as f:
            content = f.read()

        cdn_matches = cdn_pattern.findall(content)
        remote_scripts = remote_script_pattern.findall(content)
        remote_links = remote_link_pattern.findall(content)

        findings.append({
            "file": hf,
            "size_chars": len(content),
            "cdn_matches": cdn_matches,
            "remote_scripts": remote_scripts,
            "remote_links": remote_links,
            "is_clean_offline": (len(cdn_matches) == 0 and len(remote_scripts) == 0 and len(remote_links) == 0)
        })
    return findings

if __name__ == "__main__":
    print("=" * 60)
    print("EMPIRICAL CHALLENGER VERIFICATION HARNESS")
    print("=" * 60)

    # 1. Probabilities
    probs = test_scenario_probabilities()
    print("\n1. Scenario Probabilities (Sum to 100%):")
    all_probs_valid = True
    for h, v in probs.items():
        print(f"  {h:18s}: {v['bull']}% + {v['base']}% + {v['bear']}% = {v['sum']}% (Valid: {v['valid']})")
        if not v['valid']: all_probs_valid = False

    # 2. Portfolio Math
    port_res = test_portfolio_math()
    print("\n2. Investor 76-Share Position Math:")
    for k, v in port_res.items():
        print(f"  {k:28s}: {v}")

    # 3. Expected Values
    evs = test_expected_values()
    print("\n3. Expected Value Math:")
    for ev in evs:
        print(f"  {ev['horizon']:18s}: Unit EV Calc={ev['calc_ev_unit']:,.0f} vs Rep={ev['rep_ev_unit']:,} (Match: {ev['unit_match']}) | Ret Calc={ev['calc_ev_ret']}% vs Rep={ev['rep_ev_ret']}% (Match: {ev['ret_match']})")

    # 4. Formula Identity
    discrepancies = test_target_price_identity()
    print("\n4. Formula Identity P = NAV * (1 - Discount):")
    for d in discrepancies:
        print(f"  [{d['horizon']:15s} / {d['regime']:4s}] Hy={d['hynix_target']:,} | NAV={d['nav_per_share']:,} | StatedDisc={d['stated_discount_pct']}% | FormPrice={d['formula_price_share']:,} vs RepPrice={d['reported_sq_share']:,} (Diff: {d['diff_share']:,}, {d['diff_pct']}%) | ImpliedDisc={d['implied_discount_pct']}%")

    # 5. Offline Zero-CDN
    cdn_res = test_offline_zero_cdn()
    print("\n5. Offline Zero-CDN Validation:")
    for c in cdn_res:
        print(f"  {c['file']:30s}: Clean={c['is_clean_offline']} | CDNs={len(c['cdn_matches'])} | RemoteScripts={len(c['remote_scripts'])} | RemoteLinks={len(c['remote_links'])}")

    print("\n" + "=" * 60)
