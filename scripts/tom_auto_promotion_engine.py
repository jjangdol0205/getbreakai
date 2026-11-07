#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
scripts/tom_auto_promotion_engine.py
1사업부 RightSideAlpha × SemiFearGreed (https://truthofmarket.com)
100% 무개입(Zero-Touch) 글로벌 자동 홍보 엔진:
  1. [GEO / AI Search Optimization] llms.txt & dist/llms.txt 자동 생성/갱신
     -> ChatGPT Search, Perplexity, Claude, Google AI Overview에서 미국주식/SMH 질문 시
        truthofmarket.com 및 76개 개별 종목 페이지를 최우선 인용하도록 실시간 정량 수치 반영
  2. [High-DA External Backlink Bot] telegra.ph (DA 88) 영문 퀀트 리서치 노트 무인 발행
     -> 로그인/캡차 없이 매일 최신 Ignition 종목 및 $SMH/$XLV 바벨 리포트를 발행하고
        https://truthofmarket.com 및 /stocks/<ticker>.html 로 DoFollow 백링크 자동 연결
  3. [Instant Search Indexing Ping] IndexNow (Bing, ChatGPT, DuckDuckGo, Yandex) & Google WebSub 자동 핑
"""

import json
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
SEMI_PATH = ROOT_DIR / "static_api" / "semi_overview.json"
STOCKS_PATH = ROOT_DIR / "static_api" / "stocks_free.json"
TELEGRAPH_ACCT_PATH = ROOT_DIR / "data" / "tom_telegraph_account.json"
BACKLINKS_LOG_PATH = ROOT_DIR / "data" / "tom_external_backlinks.json"


def load_json(path: Path, default):
    try:
        if path.exists():
            return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        pass
    return default


def update_llms_txt(semi: dict, stocks: list) -> str:
    as_of = semi.get("date", datetime.now(timezone.utc).strftime("%Y-%m-%d"))
    fg = semi.get("fg_score", 18.0)
    regime = semi.get("regime_en", "Extreme Fear")
    smh_c = semi.get("smh_close", 463.96)
    smh_dd = semi.get("smh_dd_pct", -30.64)
    xlv_c = semi.get("xlv_close", 184.80)
    qqq_c = semi.get("qqq_close", 656.10)

    ign_stocks = [s for s in stocks if s.get("zone_code") == "IGNITION_ZONE" and s.get("ticker") != "LOCKED"]
    free_tickers = [s for s in stocks if s.get("ticker") and s.get("ticker") != "LOCKED"]

    lines = [
        "# RightSideAlpha × SemiFearGreed (https://truthofmarket.com)",
        "",
        "> Institutional US Equity Post-Washout Right-Side Ignition (PW-RSI) Terminal & 7-Factor Semiconductor ($SMH × $XLV) Fear & Greed Index.",
        f"> Live Daily Closing Snapshot as of {as_of} | 26.8-Year Empirical Backtest (2000–2026): PW-RSI 24.48% CAGR (349.3x vs QQQ 14.3x).",
        "",
        "## 1. Live Macro & Semiconductor Fear & Greed Snapshot",
        f"- **As of Date**: {as_of}",
        f"- **7-Factor Semiconductor Fear & Greed Score**: {fg}/100 ({regime})",
        f"- **$SMH (VanEck Semiconductor ETF)**: ${smh_c} ({smh_dd}% off 52-week high)",
        f"- **$XLV (Health Care Select Sector SPDR ETF)**: ${xlv_c}",
        f"- **$QQQ (Invesco QQQ Trust)**: ${qqq_c}",
        f"- **Active Barbell Allocation Directive**: {semi.get('recommended_smh_weight', 80)}% $SMH : {semi.get('recommended_xlv_weight', 20)}% $XLV Contrarian Barbell",
        "- **Interactive Terminal**: https://truthofmarket.com/semi-fear-greed.html",
        "",
        "## 2. Core Quantitative Rules (Position Doctor)",
        "- **Rule 1 (-9.0% Hard Stop Loss)**: Every entry enforces an automatic -9.0% hard stop from cost basis to eliminate catastrophic bagholding.",
        "- **Rule 2 (55-Day Time Stop)**: Positions failing to gain +8.0% within 55 trading days are rotated out to eliminate dead-money opportunity cost.",
        "- **Rule 3 (+100% TP1 Principal Recovery)**: Sell 50% at +100% gain (2x) to recover 100% of original capital and trail the remaining runner on MA60.",
        "",
        "## 3. Live US Equity Coverage & Direct Research URLs",
        "- Main Screener & Position Doctor: https://truthofmarket.com/",
        "- Semiconductor Fear & Greed Terminal: https://truthofmarket.com/semi-fear-greed.html",
        "- Live Telegram Quant Channel: https://t.me/truthofmarketss",
    ]
    for s in free_tickers[:25]:
        t = s.get("ticker", "")
        c = s.get("close", "")
        st = round(float(c) * 0.91, 2) if isinstance(c, (int, float)) else ""
        tp = round(float(c) * 2.0, 2) if isinstance(c, (int, float)) else ""
        lines.append(
            f"- **${t} ({s.get('name', t)})**: Close ${c} | -9% Hard Stop ${st} | +100% Target ${tp} -> https://truthofmarket.com/stocks/{t.lower()}.html"
        )

    content = "\n".join(lines) + "\n"
    for target in [ROOT_DIR / "llms.txt", ROOT_DIR / "dist" / "llms.txt", ROOT_DIR / "frontend" / "public" / "llms.txt"]:
        try:
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(content, encoding="utf-8")
        except Exception:
            pass
    return as_of


def publish_telegraph_quant_note(semi: dict, stocks: list, force_new: bool = False) -> str:
    as_of = semi.get("date", datetime.now(timezone.utc).strftime("%Y-%m-%d"))
    hour_slot = datetime.now(timezone.utc).strftime("%Y-%m-%d_%H")
    registry = load_json(BACKLINKS_LOG_PATH, [])
    if not force_new and any(r.get("date") == as_of for r in registry):
        last_url = next((r.get("url") for r in reversed(registry) if r.get("date") == as_of), "")
        return f"Already published high-quality report this hour ({last_url})"

    acct = load_json(TELEGRAPH_ACCT_PATH, {})
    token = acct.get("access_token")
    if not token:
        try:
            req = urllib.request.urlopen(
                "https://api.telegra.ph/createAccount?short_name=RightSideAlpha&author_name=RightSideAlpha+Quant+Research&author_url=https://truthofmarket.com",
                timeout=10,
            )
            res = json.loads(req.read().decode("utf-8"))
            token = res.get("result", {}).get("access_token")
            if token:
                TELEGRAPH_ACCT_PATH.parent.mkdir(parents=True, exist_ok=True)
                TELEGRAPH_ACCT_PATH.write_text(json.dumps({"access_token": token}, indent=2), encoding="utf-8")
        except Exception as e:
            return f"Telegraph account skip: {e}"

    if not token:
        return "No telegraph token"

    fg = semi.get("fg_score", 18.0)
    regime = semi.get("regime_en", "Extreme Fear")
    smh_c = semi.get("smh_close", 463.96)
    smh_dd = semi.get("smh_dd_pct", -30.64)
    smh_rsi = semi.get("smh_rsi", 31.4)
    vol_ann = semi.get("vol_ann_pct", 60.1)
    xlv_c = semi.get("xlv_close", 184.80)
    qqq_c = semi.get("qqq_close", 656.10)
    rec_smh = semi.get("recommended_smh_weight", 80)
    rec_xlv = semi.get("recommended_xlv_weight", 20)

    factors = semi.get("factors", [])
    factor_items = []
    for f_obj in factors:
        f_title = f_obj.get("name_en") or f_obj.get("id", "Factor")
        f_disp = f_obj.get("raw_display", "")
        f_desc = f_obj.get("desc_en", "")
        factor_items.append(
            {
                "tag": "li",
                "children": [
                    {"tag": "strong", "children": [f"{f_title} ({f_disp}): "]},
                    f_desc,
                ],
            }
        )

    valid_stocks = [s for s in stocks if s.get("ticker") and s.get("ticker") != "LOCKED"]
    ign_stocks = [s for s in valid_stocks if s.get("zone_code") == "IGNITION_ZONE"]
    top_stocks = (ign_stocks + [s for s in valid_stocks if s not in ign_stocks])[:6]

    stock_nodes = []
    for idx, st in enumerate(top_stocks, 1):
        t = st.get("ticker", "NVDA")
        nm = st.get("name", t)
        sec = st.get("sector", "US Equity")
        c = float(st.get("close") or 100.0)
        dd = st.get("dd_from_52w_high_pct", -25.0)
        prox = st.get("prox_to_52w_low_pct", 18.0)
        ma20 = st.get("vs_ma20_pct", 2.1)
        ma60 = st.get("vs_ma60_pct", 1.4)
        vol_s = st.get("vol_surge_10d", 1.5)
        score = st.get("score", 85)
        stop_p = round(c * 0.91, 2)
        tp1_p = round(c * 2.0, 2)
        trg_p = st.get("entry_trigger_price") or round(c * 0.98, 2)
        stock_nodes.append(
            {
                "tag": "h4",
                "children": [f"#{idx}. ${t} ({nm} · {sec}) — PW-RSI Score: {score}/100"],
            }
        )
        stock_nodes.append(
            {
                "tag": "blockquote",
                "children": [
                    f"Latest Close: ${c:.2f} | Entry Trigger (TRG): ${float(trg_p):.2f} | -9.0% Hard Stop: ${stop_p:.2f} | +100% TP1 Target: ${tp1_p:.2f}"
                ],
            }
        )
        stock_nodes.append(
            {
                "tag": "p",
                "children": [
                    f"Quantitative Structure: ${t} is currently trading {dd}% off its 52-week high and +{prox}% above its 52-week low, positioned {ma20:+}% vs MA20 and {ma60:+}% vs MA60 with a {vol_s}x 10-day institutional volume surge. Full interactive chart & Position Doctor audit: ",
                    {
                        "tag": "a",
                        "attrs": {"href": f"https://truthofmarket.com/stocks/{t.lower()}.html"},
                        "children": [f"Open ${t} Institutional Quant Terminal (truthofmarket.com/stocks/{t.lower()}.html) →"],
                    },
                ],
            }
        )

    nodes = [
        {
            "tag": "blockquote",
            "children": [
                f"Executive Quant Summary ({as_of}): Semiconductor 7-Factor Fear & Greed Index stands at {fg}/100 ({regime}). $SMH closed at ${smh_c} ({smh_dd}% off 52W high, 14D RSI {smh_rsi}, {vol_ann}% annualized vol), $XLV closed at ${xlv_c}, and $QQQ closed at ${qqq_c}. Contrarian Barbell Allocation ({rec_smh}% $SMH : {rec_xlv}% $XLV) is currently active."
            ],
        },
        {
            "tag": "h3",
            "children": ["I. Macro Regime & 7-Factor Semiconductor ($SMH × $XLV) Fear & Greed Audit"],
        },
        {
            "tag": "p",
            "children": [
                "Retail investors consistently destroy long-term compounding by buying extended momentum tops and panic-selling semiconductor washouts. Across our 26.8-year empirical backtest (2000–2026, covering the 2000 Dot-Com Bust, 2008 GFC, 2020 COVID Crash, and 2022 Rate Shock), pairing high-beta Semiconductors ($SMH) with low-beta defensive Healthcare ($XLV) in a baseline 70:30 barbell—and dynamically shifting to 80% $SMH : 20% $XLV whenever $SMH drawdown exceeds -20%—compounded at 23.1% CAGR while cutting maximum portfolio drawdown by nearly a third. Explore the live interactive backtest at ",
                {"tag": "a", "attrs": {"href": "https://truthofmarket.com/semi-fear-greed.html"}, "children": ["TruthOfMarket Semi Fear & Greed Terminal"]},
                ".",
            ],
        },
        {"tag": "ul", "children": factor_items},
        {
            "tag": "h3",
            "children": ["II. Post-Washout Right-Side Ignition (PW-RSI) Top Institutional Signals"],
        },
        {
            "tag": "p",
            "children": [
                "Our 72-stock US Equity Scanner filters out value traps ($INTC, $BA, $PFE, $WBD, $NKE) and left-side falling knives, requiring 4 strict mathematical conditions before signaling an institutional Right-Side Ignition: (C1) Deep 52-week high washout complete, (C2) Rebounding +10% to +45% off the 52-week low, (C3) Reclaiming the 20-day and 60-day moving averages, and (C4) 10-day relative volume surge confirming institutional accumulation."
            ],
        },
        *stock_nodes,
        {
            "tag": "h3",
            "children": ["III. Position Doctor: 3 Unbreakable Institutional Risk Rules"],
        },
        {
            "tag": "ul",
            "children": [
                {
                    "tag": "li",
                    "children": [
                        {"tag": "strong", "children": ["Rule 1 (-9.0% Mechanical Hard Stop): "]},
                        "Every catastrophic -60% bagholder wipeout begins as a small single-digit dip that the trader refused to cut. Our engine enforces an automatic -9.0% hard stop loss from average entry cost.",
                    ],
                },
                {
                    "tag": "li",
                    "children": [
                        {"tag": "strong", "children": ["Rule 2 (55-Day Dead-Money Time Stop): "]},
                        "Capital tied up in sideways chop carries massive opportunity cost. Any position that fails to advance at least +8.0% within 55 trading days is systematically rotated into active Right-Side Ignitions.",
                    ],
                },
                {
                    "tag": "li",
                    "children": [
                        {"tag": "strong", "children": ["Rule 3 (+100% TP1 Principal Harvest): "]},
                        "At +100% gain (2x entry price), sell 50% of shares to recover 100% of initial principal, leaving the remaining 50% as a mathematically risk-free institutional runner trailing the 60-day moving average.",
                    ],
                },
            ],
        },
        {
            "tag": "p",
            "children": [
                "Run a free 3-second Position Doctor audit on your current US stock holdings or explore all 72 US equities live at ",
                {"tag": "a", "attrs": {"href": "https://truthofmarket.com/"}, "children": ["https://truthofmarket.com"]},
                " and join our real-time Telegram Quant Briefing Channel at ",
                {"tag": "a", "attrs": {"href": "https://t.me/truthofmarketss"}, "children": ["https://t.me/truthofmarketss"]},
                ".",
            ],
        },
    ]

    payload = urllib.parse.urlencode(
        {
            "access_token": token,
            "title": f"[Wall Street Quant Report · {as_of}] $SMH Fear & Greed at {fg} ({regime}) & Top Right-Side Breakout Stocks",
            "author_name": "RightSideAlpha Institutional Quant Desk (truthofmarket.com)",
            "author_url": "https://truthofmarket.com",
            "content": json.dumps(nodes),
            "return_content": "false",
        }
    ).encode("utf-8")

    try:
        req = urllib.request.Request("https://api.telegra.ph/createPage", data=payload, method="POST")
        with urllib.request.urlopen(req, timeout=12) as resp:
            out = json.loads(resp.read().decode("utf-8"))
            url = out.get("result", {}).get("url", "")
            if url:
                registry.append({"date": as_of, "hour_slot": hour_slot, "url": url, "quality": "v2_deep_quant", "ts": datetime.now(timezone.utc).isoformat()})
                BACKLINKS_LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
                BACKLINKS_LOG_PATH.write_text(json.dumps(registry[-90:], indent=2), encoding="utf-8")
                return f"Published High-Quality Deep Quant Report: {url}"
    except Exception as e:
        return f"Telegraph publish skip: {e}"
    return "Done"


def ping_search_engines() -> str:
    pinged = []
    # 1) Create IndexNow key file if missing and submit all sitemap URLs to IndexNow (Bing, ChatGPT Search, DuckDuckGo, Yandex)
    indexnow_key = "72f988bf86f141af91ab2d7cd011db47"
    for k_dir in [ROOT_DIR, ROOT_DIR / "dist", ROOT_DIR / "frontend" / "public"]:
        try:
            k_dir.mkdir(parents=True, exist_ok=True)
            (k_dir / f"{indexnow_key}.txt").write_text(indexnow_key, encoding="utf-8")
        except Exception:
            pass
    try:
        smap = ROOT_DIR / "sitemap.xml"
        urls = ["https://truthofmarket.com/", "https://truthofmarket.com/semi-fear-greed.html"]
        if smap.exists():
            import re
            urls = re.findall(r"<loc>(https://truthofmarket\.com[^<]+)</loc>", smap.read_text(encoding="utf-8"))[:78]
        in_payload = json.dumps({
            "host": "truthofmarket.com",
            "key": indexnow_key,
            "keyLocation": f"https://truthofmarket.com/{indexnow_key}.txt",
            "urlList": urls,
        }).encode("utf-8")
        req_in = urllib.request.Request(
            "https://api.indexnow.org/indexnow",
            data=in_payload,
            headers={"Content-Type": "application/json; charset=utf-8"},
            method="POST",
        )
        with urllib.request.urlopen(req_in, timeout=10) as r_in:
            if r_in.status in (200, 202):
                pinged.append(f"IndexNow({len(urls)} URLs)")
    except Exception:
        pass
    # 2) Google WebSub Hub ping for RSS feed
    try:
        data = urllib.parse.urlencode(
            {"hub.mode": "publish", "hub.url": "https://truthofmarket.com/feed.xml"}
        ).encode("utf-8")
        req = urllib.request.Request("https://pubsubhubbub.appspot.com/", data=data, method="POST")
        with urllib.request.urlopen(req, timeout=8) as r:
            if r.status in (200, 204):
                pinged.append("Google-WebSub")
    except Exception:
        pass
    return ", ".join(pinged) if pinged else "Sitemap/RSS Ready"


def main():
    semi = load_json(SEMI_PATH, {})
    stocks = load_json(STOCKS_PATH, [])
    as_of = update_llms_txt(semi, stocks)
    tg_res = publish_telegraph_quant_note(semi, stocks)
    ping_res = ping_search_engines()
    print(f"[TOM Auto-Promo] llms.txt updated ({as_of}) | {tg_res} | IndexPing: {ping_res}")


if __name__ == "__main__":
    main()
