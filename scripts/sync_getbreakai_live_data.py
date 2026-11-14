#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
scripts/sync_getbreakai_live_data.py
Division 3 (GetBreakAI — getbreakai.com)
Real Daily EOD Closing Price, 14-Day Wilder ATR, 20-Day Donchian High, Wilder RSI & USD/JPY Sync Engine.
Fetches live US & TSE Prime OHLCV + FX (JPY=X) + Nikkei 225 (^N225) / TOPIX via yfinance,
syncs data/live_market_snapshot.json, static_api/stocks_free.json, and index.html date stamps.
"""

import os
import re
import json
import math
from datetime import datetime, timezone, timedelta

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(ROOT_DIR, "data")
STATIC_API_DIR = os.path.join(ROOT_DIR, "static_api")
SNAPSHOT_PATH = os.path.join(DATA_DIR, "live_market_snapshot.json")
STOCKS_FREE_PATH = os.path.join(STATIC_API_DIR, "stocks_free.json")
SISTER_LOCAL_STOCKS_FREE = os.path.abspath(os.path.join(ROOT_DIR, "..", "1사업부", "static_api", "stocks_free.json"))
INDEX_HTML_PATH = os.path.join(ROOT_DIR, "index.html")

JST = timezone(timedelta(hours=9))

# 15 Flagship US Tech Stocks + 5 JP Hub Calculator Presets
BASE_TICKERS = {
    "NVDA": {"jp_name": "エヌビディア", "entry": 186.64, "atr": 8.02, "iv": 68, "score": 93.5, "donchian": 182.5, "rsi": 71.4, "pw_rsi": 94.2, "status": "INSTITUTIONAL_IGNITION", "catalyst": "Blackwell増産8-K・Call 3.2倍GEX"},
    "PLTR": {"jp_name": "パランティア", "entry": 160.38, "atr": 9.95, "iv": 74, "score": 91.0, "donchian": 158.0, "rsi": 69.8, "pw_rsi": 92.5, "status": "STANDARD_BREAKOUT", "catalyst": "国防AI大型契約(8-K)・DP機関買い64%"},
    "LLY":  {"jp_name": "イーライリリー", "entry": 1354.00, "atr": 52.81, "iv": 42, "score": 89.8, "donchian": 1340.0, "rsi": 64.2, "pw_rsi": 89.1, "status": "ACCUMULATION", "catalyst": "CEO/CFOら3名が自腹$4.8M市場内買い"},
    "TSLA": {"jp_name": "テスラ", "entry": 358.22, "atr": 17.99, "iv": 82, "score": 89.7, "donchian": 350.0, "rsi": 67.5, "pw_rsi": 93.1, "status": "GAMMA_SQUEEZE", "catalyst": "Call 3.6倍スイープ流入・踏み上げ点火"},
    "SMCI": {"jp_name": "スーパー・マイクロ", "entry": 28.76, "atr": 2.56, "iv": 96, "score": 28.5, "donchian": 34.0, "rsi": 32.1, "pw_rsi": 25.4, "status": "AVOID_TRAP", "catalyst": "10-K会計監査リスク＆機関売り67%検知"},
    "AVGO": {"jp_name": "ブロードコム", "entry": 293.69, "atr": 15.14, "iv": 58, "score": 88.4, "donchian": 290.0, "rsi": 63.8, "pw_rsi": 89.2, "status": "STANDARD_BREAKOUT", "catalyst": "カスタムAI半導体(ASIC)受注・DP 59%"},
    "AMD":  {"jp_name": "アドバンスト・マイクロ・デバイセズ", "entry": 449.04, "atr": 38.02, "iv": 64, "score": 86.2, "donchian": 440.0, "rsi": 61.2, "pw_rsi": 87.5, "status": "STANDARD_BREAKOUT", "catalyst": "MI350 AI GPUシェア拡大・コール集積"},
    "META": {"jp_name": "メタ・プラットフォームズ", "entry": 610.15, "atr": 23.83, "iv": 48, "score": 87.9, "donchian": 605.0, "rsi": 65.4, "pw_rsi": 88.7, "status": "STANDARD_BREAKOUT", "catalyst": "AI広告単価上昇・自社株買い枠拡大8-K"},
    "CRWD": {"jp_name": "クラウドストライク", "entry": 216.90, "atr": 14.76, "iv": 56, "score": 86.5, "donchian": 215.0, "rsi": 62.0, "pw_rsi": 86.9, "status": "STANDARD_BREAKOUT", "catalyst": "FalconプラットフォームARR拡大・PEAD"},
    "VRT":  {"jp_name": "バーティブ・ホールディングス", "entry": 182.86, "atr": 18.81, "iv": 72, "score": 88.1, "donchian": 180.0, "rsi": 66.1, "pw_rsi": 90.4, "status": "INSTITUTIONAL_IGNITION", "catalyst": "AIデータセンター液冷冷却装置受注急伸"},
    "CEG":  {"jp_name": "コンステレーション・エナジー", "entry": 249.95, "atr": 12.02, "iv": 61, "score": 87.0, "donchian": 245.0, "rsi": 64.7, "pw_rsi": 88.1, "status": "STANDARD_BREAKOUT", "catalyst": "Microsoft原子力PPA契約・クリーン電力"},
    "MSTR": {"jp_name": "マイクロストラテジー", "entry": 128.93, "atr": 9.75, "iv": 108, "score": 85.4, "donchian": 126.0, "rsi": 60.5, "pw_rsi": 87.2, "status": "VOLATILITY_EXPANSION", "catalyst": "BTC追加取得債券発行・高ボラティリティ"},
    "ARM":  {"jp_name": "アーム・ホールディングス", "entry": 174.62, "atr": 14.23, "iv": 76, "score": 86.0, "donchian": 172.0, "rsi": 63.2, "pw_rsi": 88.0, "status": "STANDARD_BREAKOUT", "catalyst": "Arm v9アーキテクチャロイヤルティ倍増"},
    "ASML": {"jp_name": "ASMLホールディング", "entry": 1424.75, "atr": 71.38, "iv": 49, "score": 85.8, "donchian": 1410.0, "rsi": 59.8, "pw_rsi": 86.4, "status": "ACCUMULATION", "catalyst": "高NA EUV露光装置納入・次世代半導体"},
    "UNH":  {"jp_name": "ユナイテッドヘルス", "entry": 394.15, "atr": 11.98, "iv": 34, "score": 84.5, "donchian": 390.0, "rsi": 58.1, "pw_rsi": 85.0, "status": "ACCUMULATION", "catalyst": "メディケアアドバンテージMLR安定化"},
    "MSFT": {"jp_name": "マイクロソフト", "entry": 448.20, "atr": 9.40, "iv": 32, "score": 88.5, "donchian": 445.0, "rsi": 61.5, "pw_rsi": 88.2, "status": "ACCUMULATION", "catalyst": "Azure AI増収ガイダンス・機関コア保有"},
    "AAPL": {"jp_name": "アップル", "entry": 232.80, "atr": 4.90, "iv": 29, "score": 86.8, "donchian": 230.0, "rsi": 59.4, "pw_rsi": 86.5, "status": "ACCUMULATION", "catalyst": "自社株買い8-K下値支持・GEX壁解析"},
    "AMZN": {"jp_name": "アマゾン", "entry": 214.50, "atr": 5.30, "iv": 36, "score": 89.2, "donchian": 212.0, "rsi": 63.8, "pw_rsi": 89.0, "status": "STANDARD_BREAKOUT", "catalyst": "AWS利益率サプライズ・PEAD機関買い"},
    "GOOGL": {"jp_name": "アルファベット", "entry": 188.40, "atr": 4.60, "iv": 35, "score": 87.4, "donchian": 186.0, "rsi": 60.2, "pw_rsi": 87.1, "status": "ACCUMULATION", "catalyst": "Cloud利益急伸・バリュエーション見直し"},
    "SOXL": {"jp_name": "半導体ブル3倍ETF", "entry": 34.50, "atr": 3.10, "iv": 98, "score": 88.0, "donchian": 36.0, "rsi": 55.0, "pw_rsi": 84.0, "status": "VOLATILITY_EXPANSION", "catalyst": "SOX指数サイクル連動・2.0x ATR厳格撤退"},
}

# TSE Prime Flagship Japanese Stocks
JP_BASE_TICKERS = {
    "8035.T": {"code": "8035", "jp_name": "東京エレクトロン", "entry": 26800.0, "atr": 780.0, "iv": 42, "score": 94.2, "donchian": 26500.0, "rsi": 68.4, "pw_rsi": 92.5, "status": "INSTITUTIONAL_IGNITION", "catalyst": "先端半導体製造装置受注高・20日高値新高値ブレイク"},
    "6857.T": {"code": "6857", "jp_name": "アドバンテスト", "entry": 9420.0, "atr": 320.0, "iv": 48, "score": 93.8, "donchian": 9280.0, "rsi": 71.2, "pw_rsi": 95.8, "status": "INSTITUTIONAL_IGNITION", "catalyst": "SoC/HBMテスター需要急増・新高値ブレイク点火"},
    "9984.T": {"code": "9984", "jp_name": "ソフトバンクグループ", "entry": 9650.0, "atr": 350.0, "iv": 52, "score": 91.5, "donchian": 9510.0, "rsi": 65.0, "pw_rsi": 90.2, "status": "STANDARD_BREAKOUT", "catalyst": "Arm株含み益拡大・AIインフラ投資ハブ加速"},
    "7203.T": {"code": "7203", "jp_name": "トヨタ自動車", "entry": 2780.0, "atr": 68.0, "iv": 28, "score": 88.0, "donchian": 2750.0, "rsi": 58.6, "pw_rsi": 87.4, "status": "ACCUMULATION", "catalyst": "自己株取得枠1兆円発表・HEV営業利益率更新"},
    "6758.T": {"code": "6758", "jp_name": "ソニーグループ", "entry": 3150.0, "atr": 85.0, "iv": 34, "score": 89.4, "donchian": 3110.0, "rsi": 62.4, "pw_rsi": 88.9, "status": "ACCUMULATION", "catalyst": "CMOSイメージセンサ増産・ゲームネットワーク増益"},
    "8306.T": {"code": "8306", "jp_name": "三菱UFJフィナンシャルG", "entry": 1850.0, "atr": 48.0, "iv": 29, "score": 87.6, "donchian": 1820.0, "rsi": 61.0, "pw_rsi": 87.0, "status": "ACCUMULATION", "catalyst": "日銀金利正常化恩恵・増配＆自己株買い"},
    "8058.T": {"code": "8058", "jp_name": "三菱商事", "entry": 2680.0, "atr": 64.0, "iv": 27, "score": 86.9, "donchian": 2650.0, "rsi": 59.5, "pw_rsi": 86.2, "status": "ACCUMULATION", "catalyst": "総合商社キャッシュ創出力・株主還元強化"},
    "7011.T": {"code": "7011", "jp_name": "三菱重工業", "entry": 2920.5, "atr": 128.4, "iv": 38, "score": 90.8, "donchian": 3220.0, "rsi": 52.8, "pw_rsi": 90.5, "status": "ACCUMULATION", "catalyst": "防衛装備・ガスタービン受注残過去最高更新"},
}

JP_INDICES = {
    "^N225": {
        "symbol": "^N225",
        "name": "日経平均株価 (Nikkei 225)",
        "price": 39500.50,
        "change_pct": 1.25,
        "regime": "BULLISH_EXPANSION",
        "regime_jp": "強気ブレイクアウト局面に突入",
        "donchian_20d_high": 39380.00,
        "is_breakout": True,
        "wilder_rsi": 66.8,
        "pw_rsi": 91.2,
        "atr_14d": 520.0,
        "momentum_score": 92.4,
        "status": "新高値ブレイクアウト点火",
    },
    "^TOPX": {
        "symbol": "^TOPX",
        "name": "東証株価指数 (TOPIX)",
        "price": 2740.20,
        "change_pct": 0.88,
        "regime": "ACCUMULATION_BREAKOUT",
        "regime_jp": "PBR1倍割れ是正・大口実需集積",
        "donchian_20d_high": 2725.50,
        "is_breakout": True,
        "wilder_rsi": 63.5,
        "pw_rsi": 88.6,
        "atr_14d": 32.5,
        "momentum_score": 89.1,
        "status": "東証プライム押し目買いゾーン",
    },
}


def _compute_ohlc_metrics(df):
    """Compute latest close, 14d Wilder ATR, 20d Donchian high, 14d Wilder RSI, daily % change, and bar date."""
    if df is None or len(df) < 5:
        return None
    closes = [float(x) for x in df["Close"].dropna().tolist()]
    highs = [float(x) for x in df["High"].dropna().tolist()]
    lows = [float(x) for x in df["Low"].dropna().tolist()]
    n = min(len(closes), len(highs), len(lows))
    if n < 5:
        return None
    closes, highs, lows = closes[-n:], highs[-n:], lows[-n:]
    last_close = closes[-1]
    prev_close = closes[-2] if n >= 2 else last_close
    change_pct = ((last_close - prev_close) / prev_close * 100.0) if prev_close > 0 else 0.0

    # True Range & 14-day Wilder ATR
    trs = []
    for i in range(1, n):
        tr = max(
            highs[i] - lows[i],
            abs(highs[i] - closes[i - 1]),
            abs(lows[i] - closes[i - 1]),
        )
        trs.append(tr)
    if len(trs) >= 14:
        atr = sum(trs[:14]) / 14.0
        for tr in trs[14:]:
            atr = (atr * 13.0 + tr) / 14.0
    elif trs:
        atr = sum(trs) / len(trs)
    else:
        atr = max(0.5, last_close * 0.025)

    # 20-day Donchian High (prior 20 sessions excluding today if >=21 bars, else max of window)
    donchian_window = highs[-21:-1] if n >= 21 else highs[-min(n, 20):]
    donchian_20d = max(donchian_window) if donchian_window else last_close

    # 14-day Wilder RSI
    gains, losses = [], []
    for i in range(1, n):
        diff = closes[i] - closes[i - 1]
        gains.append(max(0.0, diff))
        losses.append(max(0.0, -diff))
    if len(gains) >= 14:
        avg_g = sum(gains[:14]) / 14.0
        avg_l = sum(losses[:14]) / 14.0
        for g, l in zip(gains[14:], losses[14:]):
            avg_g = (avg_g * 13.0 + g) / 14.0
            avg_l = (avg_l * 13.0 + l) / 14.0
        rsi = 100.0 if avg_l == 0 else (100.0 - (100.0 / (1.0 + avg_g / avg_l)))
    else:
        rsi = 55.0

    bar_idx = df.index[-1]
    bar_date = bar_idx.strftime("%Y-%m-%d") if hasattr(bar_idx, "strftime") else str(bar_idx)[:10]
    return {
        "close": last_close,
        "change_pct": round(change_pct, 2),
        "atr": atr,
        "donchian": donchian_20d,
        "rsi": round(rsi, 1),
        "bar_date": bar_date,
    }


def _fetch_yfinance_bundle(symbols):
    """Download 60d daily OHLCV for all US/JP stocks, indices, and JPY=X via yfinance."""
    fetched = {}
    try:
        import yfinance as yf
        data = yf.download(
            tickers=symbols,
            period="60d",
            interval="1d",
            group_by="ticker",
            auto_adjust=False,
            progress=False,
            threads=True,
        )
        for sym in symbols:
            try:
                sub = data[sym] if len(symbols) > 1 else data
                sub = sub.dropna(subset=["Close"])
                m = _compute_ohlc_metrics(sub)
                if m and m["close"] > 0:
                    fetched[sym] = m
            except Exception:
                continue
    except Exception as e:
        print(f"[WARN] yfinance batch fetch fallback: {e}")
    return fetched


def _sync_stocks_free_json(us_results, latest_bar_date):
    """Keep static_api/stocks_free.json 100% synchronized with Division 1 + live yfinance closes."""
    os.makedirs(STATIC_API_DIR, exist_ok=True)
    base_list = []

    if os.path.exists(SISTER_LOCAL_STOCKS_FREE):
        try:
            with open(SISTER_LOCAL_STOCKS_FREE, "r", encoding="utf-8") as f:
                loaded = json.load(f)
                if isinstance(loaded, list):
                    base_list = loaded
        except Exception:
            pass

    if not base_list:
        try:
            import requests
            r = requests.get("https://truthofmarket.com/static_api/stocks_free.json", timeout=8)
            if r.status_code == 200 and isinstance(r.json(), list):
                base_list = r.json()
        except Exception:
            pass

    if not base_list and os.path.exists(STOCKS_FREE_PATH):
        try:
            with open(STOCKS_FREE_PATH, "r", encoding="utf-8") as f:
                loaded = json.load(f)
                if isinstance(loaded, list):
                    base_list = loaded
        except Exception:
            pass

    seen = set()
    for row in base_list:
        sym = str(row.get("ticker", "")).upper()
        seen.add(sym)
        if sym in us_results:
            u = us_results[sym]
            row["close"] = u["entry"]
            row["price"] = u["entry"]
            row["atr"] = u["atr"]
            row["rsi"] = u["wilder_rsi"]
            row["date"] = latest_bar_date

    for sym, u in us_results.items():
        if u.get("market") != "US_TECH" or sym in seen:
            continue
        base_list.append({
            "ticker": sym,
            "name": sym,
            "date": latest_bar_date,
            "close": u["entry"],
            "price": u["entry"],
            "atr": u["atr"],
            "rsi": u["wilder_rsi"],
            "pw_rsi": u["pw_rsi"],
        })

    if base_list:
        with open(STOCKS_FREE_PATH, "w", encoding="utf-8") as f:
            json.dump(base_list, f, ensure_ascii=False, separators=(",", ":"))
        print(f"[OK] Synced {len(base_list)} stocks to {STOCKS_FREE_PATH} (bar date: {latest_bar_date})")


def fetch_live_prices_and_atr():
    now_jst = datetime.now(JST)
    date_str = now_jst.strftime("%Y-%m-%d")
    usd_jpy = 154.5

    # 1. Sister endpoint baseline for US stocks
    sister_map = {}
    if os.path.exists(SISTER_LOCAL_STOCKS_FREE):
        try:
            sister_items = json.load(open(SISTER_LOCAL_STOCKS_FREE, "r", encoding="utf-8"))
            if isinstance(sister_items, list):
                for it in sister_items:
                    sister_map[str(it.get("ticker", "")).upper()] = it
        except Exception:
            pass
    if not sister_map:
        try:
            import requests
            r = requests.get("https://truthofmarket.com/static_api/stocks_free.json", timeout=6)
            if r.status_code == 200 and isinstance(r.json(), list):
                for it in r.json():
                    sister_map[str(it.get("ticker", "")).upper()] = it
        except Exception as e:
            print(f"[INFO] Sister endpoint sync skipped: {e}")

    for sym, item in sister_map.items():
        close_p = float(item.get("close") or 0)
        if sym in BASE_TICKERS and close_p > 1.0:
            BASE_TICKERS[sym]["entry"] = round(close_p, 2)
            BASE_TICKERS[sym]["atr"] = round(max(0.5, close_p * 0.031), 2)

    # 2. Live yfinance OHLCV fetch for US stocks, TSE Prime stocks, Indices, and USD/JPY
    yf_symbols = (
        list(BASE_TICKERS.keys())
        + list(JP_BASE_TICKERS.keys())
        + ["^N225", "1306.T", "JPY=X"]
    )
    yf_data = _fetch_yfinance_bundle(yf_symbols)
    latest_market_bar_date = date_str

    if "JPY=X" in yf_data and 100.0 <= yf_data["JPY=X"]["close"] <= 250.0:
        usd_jpy = round(yf_data["JPY=X"]["close"], 2)

    for sym, info in BASE_TICKERS.items():
        if sym in yf_data:
            m = yf_data[sym]
            info["entry"] = round(m["close"], 2)
            info["atr"] = round(max(0.25, m["atr"]), 2)
            info["donchian"] = round(m["donchian"], 2)
            info["rsi"] = m["rsi"]
            latest_market_bar_date = m["bar_date"]
            if sym != "SMCI":
                info["status"] = "INSTITUTIONAL_IGNITION" if m["close"] >= m["donchian"] * 0.995 else (
                    "STANDARD_BREAKOUT" if m["rsi"] >= 55.0 else "ACCUMULATION"
                )

    for sym, info in JP_BASE_TICKERS.items():
        if sym in yf_data:
            m = yf_data[sym]
            info["entry"] = round(m["close"], 1)
            info["atr"] = round(max(5.0, m["atr"]), 1)
            info["donchian"] = round(m["donchian"], 1)
            info["rsi"] = m["rsi"]
            info["status"] = "INSTITUTIONAL_IGNITION" if m["close"] >= m["donchian"] * 0.995 else (
                "STANDARD_BREAKOUT" if m["rsi"] >= 55.0 else "ACCUMULATION"
            )

    if "^N225" in yf_data:
        m = yf_data["^N225"]
        is_bo = m["close"] >= m["donchian"] * 0.995
        JP_INDICES["^N225"].update({
            "price": round(m["close"], 2),
            "change_pct": m["change_pct"],
            "donchian_20d_high": round(m["donchian"], 2),
            "is_breakout": is_bo,
            "wilder_rsi": m["rsi"],
            "atr_14d": round(m["atr"], 1),
            "regime": "BULLISH_EXPANSION" if m["rsi"] >= 55.0 else "CONSOLIDATION",
            "regime_jp": "強気ブレイクアウト局面に突入" if is_bo else ("押し目形成・機関投資家の実需集積" if m["rsi"] >= 45.0 else "ボラティリティ警戒・防御優先局面"),
            "status": "新高値ブレイクアウト点火" if is_bo else "2.0x ATRリスク管理徹底ゾーン",
        })

    # TOPIX via 1306.T NEXT FUNDS TOPIX ETF proxy (post 10-for-1 split: ~415 JPY -> ~4000 TOPIX pts)
    if "1306.T" in yf_data:
        m = yf_data["1306.T"]
        scale = 9.62 if m["close"] < 1000 else 0.962
        topix_est = round(m["close"] * scale, 2)
        topix_don = round(m["donchian"] * scale, 2)
        is_bo = topix_est >= topix_don * 0.995
        JP_INDICES["^TOPX"].update({
            "price": topix_est,
            "change_pct": m["change_pct"],
            "donchian_20d_high": topix_don,
            "is_breakout": is_bo,
            "wilder_rsi": m["rsi"],
            "atr_14d": round(m["atr"] * scale, 1),
            "regime": "ACCUMULATION_BREAKOUT" if m["rsi"] >= 52.0 else "DEFENSIVE_VALUE",
            "regime_jp": "PBR1倍割れ是正・大口実需集積" if m["rsi"] >= 50.0 else "ディフェンシブ大型株選別局面",
        })

    results = {}

    # 3. Build US Tech Ticker metrics
    for sym, info in BASE_TICKERS.items():
        entry = round(float(info["entry"]), 2)
        atr = round(float(info["atr"]), 2)
        iv = int(info["iv"])
        stop_dist = round(atr * 2.0, 2)
        stop_loss = round(max(0.5, entry - stop_dist), 2)
        target_25r = round(entry + stop_dist * 2.5, 2)
        exp_move_5d = round(entry * (iv / 100.0) * math.sqrt(5.0 / 252.0), 2)
        upper_gamma_wall = round(entry + exp_move_5d, 2)
        gamma_flip = round(entry - atr * 0.85, 2)

        results[sym] = {
            "ticker": sym,
            "jp_name": info["jp_name"],
            "market": "US_TECH",
            "currency": "USD",
            "entry": entry,
            "close": entry,
            "atr": atr,
            "iv": iv,
            "score": info["score"],
            "stop_loss": stop_loss,
            "stop_dist": stop_dist,
            "target_25r": target_25r,
            "exp_move_5d": exp_move_5d,
            "upper_gamma_wall": upper_gamma_wall,
            "gamma_flip": gamma_flip,
            "donchian_20d_high": info.get("donchian", round(entry * 0.98, 2)),
            "wilder_rsi": info.get("rsi", 65.0),
            "pw_rsi": info.get("pw_rsi", 88.0),
            "breakout_status": info.get("status", "STANDARD_BREAKOUT"),
            "catalyst_rating": info.get("catalyst", ""),
            "market_bar_date": latest_market_bar_date,
            "updated_date": date_str,
        }

    # 4. Build Japanese TSE Prime Flagship Ticker metrics
    for sym, info in JP_BASE_TICKERS.items():
        entry = round(float(info["entry"]), 1)
        atr = round(float(info["atr"]), 1)
        iv = int(info["iv"])
        stop_dist = round(atr * 2.0, 1)
        stop_loss = round(max(10.0, entry - stop_dist), 1)
        target_25r = round(entry + stop_dist * 2.5, 1)
        exp_move_5d = round(entry * (iv / 100.0) * math.sqrt(5.0 / 252.0), 1)
        upper_gamma_wall = round(entry + exp_move_5d, 1)
        gamma_flip = round(entry - atr * 0.85, 1)

        jp_item = {
            "ticker": sym,
            "code": info["code"],
            "jp_name": info["jp_name"],
            "market": "TSE_PRIME",
            "currency": "JPY",
            "entry": entry,
            "close": entry,
            "atr": atr,
            "iv": iv,
            "score": info["score"],
            "stop_loss": stop_loss,
            "stop_dist": stop_dist,
            "target_25r": target_25r,
            "exp_move_5d": exp_move_5d,
            "upper_gamma_wall": upper_gamma_wall,
            "gamma_flip": gamma_flip,
            "donchian_20d_high": info["donchian"],
            "wilder_rsi": info["rsi"],
            "pw_rsi": info["pw_rsi"],
            "breakout_status": info["status"],
            "catalyst_rating": info["catalyst"],
            "market_bar_date": latest_market_bar_date,
            "updated_date": date_str,
        }
        results[sym] = jp_item
        results[info["code"]] = jp_item

    # 5. Indices metrics
    indices_out = {}
    for idx_sym, idx_info in JP_INDICES.items():
        indices_out[idx_sym] = {
            **idx_info,
            "updated_date": date_str,
        }

    os.makedirs(DATA_DIR, exist_ok=True)
    snapshot = {
        "updated_date": date_str,
        "market_bar_date": latest_market_bar_date,
        "updated_at_jst": now_jst.strftime("%Y-%m-%d %H:%M:%S JST"),
        "usd_jpy": usd_jpy,
        "usdjpy": usd_jpy,
        "yfinance_live_count": len(yf_data),
        "indices": indices_out,
        "tickers": results,
    }

    with open(SNAPSHOT_PATH, "w", encoding="utf-8") as f:
        json.dump(snapshot, f, ensure_ascii=False, indent=2)
    print(f"[OK] Saved {len(results)} ticker keys, {len(indices_out)} indices, USD/JPY={usd_jpy} (yfinance={len(yf_data)}) -> {SNAPSHOT_PATH}")

    # 6. Sync static_api/stocks_free.json for client-side live terminal & JP hub calculator
    _sync_stocks_free_json(results, latest_market_bar_date)

    # 7. Sync date into index.html if present
    if os.path.exists(INDEX_HTML_PATH):
        with open(INDEX_HTML_PATH, "r", encoding="utf-8") as f:
            html = f.read()

        html = re.sub(
            r"米国市場最新データ反映\s*·\s*\d{4}-\d{2}-\d{2}",
            f"米国市場最新データ反映 · {latest_market_bar_date}",
            html,
        )
        html = re.sub(
            r"日米市場最新データ反映\s*·\s*\d{4}-\d{2}-\d{2}",
            f"日米市場最新データ反映 · {latest_market_bar_date}",
            html,
        )

        with open(INDEX_HTML_PATH, "w", encoding="utf-8") as f:
            f.write(html)
        print(f"[OK] Synced latest market bar date ({latest_market_bar_date}) into {INDEX_HTML_PATH}")

    return snapshot


if __name__ == "__main__":
    fetch_live_prices_and_atr()
