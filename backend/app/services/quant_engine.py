"""
backend/app/services/quant_engine.py - Core Quantitative Data Engine
"""
import json
import re
from pathlib import Path
from typing import Dict, List, Optional, Any

from backend.app.config import settings
from backend.app.models.stock import StockBase, StockResponse
from backend.app.models.backtest import (
    BacktestSummaryResponse,
    BacktestKpis,
    StrategySummary,
    YearlyPerformance,
    TradeLog,
    PositionDoctorResponse,
)
from backend.app.models.research import ResearchBriefDetail, ResearchBriefSummary

STOCK_NAMES: Dict[str, tuple[str, str, str, str]] = {
    "AFRM": ("Affirm Holdings", "アファーム・ホールディングス", "어펌 홀딩스", "Fintech & BNPL"),
    "ALB": ("Albemarle Corp", "アルベマール", "앨버말", "Specialty Chemicals"),
    "AMAT": ("Applied Materials", "アプライド・マテリアルズ", "어플라이드 머티어리얼즈", "Semiconductor Equip"),
    "AMD": ("Advanced Micro Devices", "アドバンスト・マイクロ・デバイセズ", "AMD", "Semiconductors"),
    "AMZN": ("Amazon.com Inc", "アマゾン・ドット・コム", "아마존닷컴", "Cloud & E-Commerce"),
    "APP": ("AppLovin Corp", "アップラビン", "앱러빈", "AdTech & AI Software"),
    "ARM": ("Arm Holdings plc", "アーム・ホールディングス", "암 홀딩스", "Semiconductor IP"),
    "ASML": ("ASML Holding N.V.", "ASMLホールディング", "ASML 홀딩", "Semiconductor Equip"),
    "AVGO": ("Broadcom Inc", "ブロードコム", "브로드컴", "Semiconductors"),
    "BA": ("Boeing Co", "ボーイング", "보잉", "Aerospace & Defense"),
    "CCL": ("Carnival Corp", "カーニバル", "카니발", "Leisure & Cruise"),
    "CELH": ("Celsius Holdings", "セルシウス・ホールディングス", "셀시우스 홀딩스", "Consumer Beverages"),
    "COIN": ("Coinbase Global", "コインベース・グローバル", "코인베이스", "Digital Assets & Fin"),
    "CROX": ("Crocs Inc", "クロックス", "크록스", "Consumer Apparel"),
    "CRWD": ("CrowdStrike Holdings", "クラウドストライク", "크라우드스트라이크", "Cybersecurity"),
    "CVNA": ("Carvana Co", "カルバナ", "카바나", "Auto E-Commerce"),
    "DAL": ("Delta Air Lines", "デルタ航空", "델타항공", "Passenger Airlines"),
    "DDOG": ("Datadog Inc", "データドッグ", "데이터독", "Cloud Observability"),
    "DECK": ("Deckers Outdoor", "デッカーズ・アウトドア", "데커스 아웃도어", "Consumer Footwear"),
    "DIS": ("Walt Disney Co", "ウォルト・ディズニー", "월트 디즈니", "Media & Entertainment"),
    "DUOL": ("Duolingo Inc", "デュオリンゴ", "듀오링고", "Consumer EdTech"),
    "ENPH": ("Enphase Energy", "エンフェーズ・エナジー", "엔페이즈 에너지", "Solar & CleanTech"),
    "F": ("Ford Motor Co", "フォード・モーター", "포드 모터", "Automotive"),
    "FLNC": ("Fluence Energy", "フルエンス・エナジー", "플루언스 에너지", "Grid Energy Storage"),
    "FSLR": ("First Solar Inc", "ファースト・ソーラー", "퍼스트솔라", "Solar Modules"),
    "GE": ("GE Aerospace", "GEエアロスペース", "GE 에어로스페이스", "Aerospace & Defense"),
    "GM": ("General Motors Co", "ゼネラル・モーターズ", "제너럴 모터스", "Automotive"),
    "HOOD": ("Robinhood Markets", "ロビンフッド・マーケッツ", "로빈후드", "Fintech & Brokerage"),
    "INTC": ("Intel Corp", "インテル", "인텔", "Semiconductors"),
    "KLAC": ("KLA Corp", "KLAコーポレーション", "KLA", "Semiconductor Equip"),
    "LLY": ("Eli Lilly & Co", "イーライリリー", "일라이 릴리", "Biopharma"),
    "LRCX": ("Lam Research Corp", "ラムリサーチ", "램리서치", "Semiconductor Equip"),
    "LULU": ("Lululemon Athletica", "ルルレモン・アスレティカ", "룰루레몬", "Athletic Apparel"),
    "MBLY": ("Mobileye Global", "モービルアイ・グローバル", "모빌아이", "ADAS & Autonomous"),
    "MDB": ("MongoDB Inc", "モンゴDB", "몽고DB", "Database Software"),
    "META": ("Meta Platforms Inc", "メタ・プラットフォームズ", "메타 플랫폼스", "Internet & AI"),
    "MPWR": ("Monolithic Power Systems", "モノリシック・パワー", "모놀리식 파워 시스템즈", "Power Semiconductors"),
    "MRNA": ("Moderna Inc", "モデルナ", "모더나", "Biotechnology"),
    "MRVL": ("Marvell Technology", "マーベル・テクノロジー", "마벨 테크놀로지", "Semiconductors"),
    "MU": ("Micron Technology", "マイクロン・テクノロジー", "마이크론", "Memory Semiconductors"),
    "NET": ("Cloudflare Inc", "クラウドフレア", "클라우드플레어", "Edge Cloud & Security"),
    "NFLX": ("Netflix Inc", "ネットフリックス", "넷플릭스", "Streaming Media"),
    "NKE": ("Nike Inc", "ナイキ", "나이키", "Consumer Footwear"),
    "NVDA": ("NVIDIA Corp", "エヌビディア", "엔비디아", "AI Semiconductors"),
    "ON": ("ON Semiconductor", "オン・セミコンダクター", "온세미컨덕터", "Power & Auto Chips"),
    "OXY": ("Occidental Petroleum", "オキシデンタル・ペトロリアム", "옥시덴탈 페트롤리움", "Oil & Gas E&P"),
    "PANW": ("Palo Alto Networks", "パロアルトネットワークス", "팔로알토 네트웍스", "Cybersecurity"),
    "PARA": ("Paramount Global", "パラマウント・グローバル", "파라마운트 글로벌", "Legacy Media"),
    "PFE": ("Pfizer Inc", "ファイザー", "화이자", "Pharmaceuticals"),
    "PINS": ("Pinterest Inc", "ピンタレスト", "핀터레스트", "Internet & Social"),
    "PLTR": ("Palantir Technologies", "パランティア・テクノロジーズ", "팔란티어", "Enterprise AI"),
    "PYPL": ("PayPal Holdings", "ペイパル・ホールディングス", "페이팔", "Digital Payments"),
    "QCOM": ("Qualcomm Inc", "クアルコム", "퀄컴", "Semiconductors"),
    "REGN": ("Regeneron Pharma", "リジェネロン", "리제네론", "Biotechnology"),
    "ROKU": ("Roku Inc", "ロク", "로쿠", "Connected TV"),
    "SBUX": ("Starbucks Corp", "スターバックス", "스타벅스", "Consumer Retail"),
    "SEDG": ("SolarEdge Tech", "ソーラーエッジ", "솔라엣지", "Solar Inverters"),
    "SHOP": ("Shopify Inc", "ショッピファイ", "쇼피파이", "E-Commerce SaaS"),
    "SMCI": ("Super Micro Computer", "スーパー・マイクロ", "슈퍼마이크로컴퓨터", "AI Server Hardware"),
    "SNAP": ("Snap Inc", "スナップ", "스냅", "Social Media"),
    "SNOW": ("Snowflake Inc", "スノーフレイク", "스노우플레이크", "Data Cloud SaaS"),
    "SOFI": ("SoFi Technologies", "ソーファイ・テクノロジーズ", "소파이", "Digital Banking"),
    "SPOT": ("Spotify Tech", "スポティファイ", "스포티파이", "Audio Streaming"),
    "TSLA": ("Tesla Inc", "テスラ", "테슬라", "EV & Robotics"),
    "TSM": ("TSMC (ADR)", "TSMC (米国ADR)", "TSMC (ADR)", "Foundry Semis"),
    "U": ("Unity Software Inc", "ユニティ・ソフトウェア", "유니티 소프트웨어", "3D Engine Software"),
    "UAL": ("United Airlines", "ユナイテッド航空", "유나이티드항공", "Passenger Airlines"),
    "UBER": ("Uber Technologies", "ウーバー", "우버", "Mobility Platform"),
    "UPST": ("Upstart Holdings", "アップスタート", "업스타트 홀딩스", "AI Lending Fintech"),
    "VRTX": ("Vertex Pharmaceuticals", "バーテックス・ファーマ", "버텍스 파마슈티컬스", "Biotechnology"),
    "XOM": ("Exxon Mobil Corp", "エクソンモービル", "엑슨모빌", "Integrated Energy"),
    "ZS": ("Zscaler Inc", "ジースケイラー", "지스케일러", "Cloud Security"),
}

VALUE_TRAPS = {"INTC", "BA", "PFE", "PARA", "WBD", "NKE", "ALB"}

PRIORITY_TICKERS = [
    "CELH", "CCL", "TSLA", "UPST", "MBLY", "APP", "ENPH",
    "SEDG", "CVNA", "UBER", "NFLX", "NVDA", "AMD", "MU"
]


class QuantEngine:
    _instance: Optional["QuantEngine"] = None

    def __init__(self):
        self.stocks: List[StockBase] = []
        self.stocks_by_ticker: Dict[str, StockBase] = {}
        self.preview_tickers: set[str] = set()
        self.backtest_data: Optional[Dict[str, Any]] = None
        self.backtest_summary_obj: Optional[BacktestSummaryResponse] = None
        self.trade_logs: List[Dict[str, Any]] = []
        self.research_briefs: Dict[str, List[ResearchBriefDetail]] = {}
        self.research_summaries: List[ResearchBriefSummary] = []
        self.is_loaded: bool = False

    @classmethod
    def get_instance(cls) -> "QuantEngine":
        if cls._instance is None:
            cls._instance = QuantEngine()
            cls._instance.initialize()
        return cls._instance

    def initialize(self):
        """Loads and indexes all dataset artifacts into memory."""
        self._load_stocks()
        self._load_backtest()
        self._load_research()
        self.is_loaded = True

    def _load_stocks(self):
        stocks_file = settings.STOCKS_DATA_PATH
        if not stocks_file.exists():
            raise FileNotFoundError(f"Missing stocks screened file: {stocks_file}")

        with open(stocks_file, "r", encoding="utf-8") as f:
            raw_stocks = json.load(f)

        parsed_stocks: List[StockBase] = []
        for s in raw_stocks:
            t = str(s.get("Ticker", "")).strip().upper()
            # Strictly restrict RightSideAlpha universe to US-listed equities only
            if not t or "." in t or t.endswith(".KS") or t.endswith(".KQ"):
                continue
            close = float(s.get("Close", 0.0))
            low52 = float(s.get("Low52", 0.0))
            high52 = float(s.get("High52", 0.0))
            prox = float(s.get("ProxLow52_Pct", 999.0))
            dd = float(s.get("DDHigh52_Pct", 0.0))
            ma20_pct = float(s.get("Vs_MA20_Pct", -10.0))
            ma60_pct = float(s.get("Vs_MA60_Pct", -10.0))
            ma200_pct = (
                float(s.get("Vs_MA200_Pct"))
                if s.get("Vs_MA200_Pct") is not None
                else None
            )
            rsi = float(s.get("RSI14", 50.0))
            vol = float(s.get("VolSurge10D", 1.0))
            ret5d = (
                float(s.get("Ret5D_Pct"))
                if s.get("Ret5D_Pct") is not None
                else None
            )
            ret20d = (
                float(s.get("Ret20D_Pct"))
                if s.get("Ret20D_Pct") is not None
                else None
            )
            hist_2x = float(s.get("Hist_2x_Rate_After_40Pct_Crash", 25.0))
            hist_med = float(s.get("Hist_Med_PeakGain_After_Crash", 45.0))

            # Algebraic Moving Average reconstruction
            ma20_val = round(close / (1.0 + ma20_pct / 100.0), 2) if ma20_pct != -100.0 else close
            ma60_val = round(close / (1.0 + ma60_pct / 100.0), 2) if ma60_pct != -100.0 else close

            # Risk and profit targets
            stop_loss_val = round(close * 0.91, 2)
            tp1_val = round(close * 2.0, 2)
            entry_trigger_val = round(max(ma20_val, ma60_val), 2)
            pct_to_trig = round(((entry_trigger_val / close) - 1.0) * 100.0, 2) if close > 0 else 0.0

            # PW-RSI Composite Scoring
            score = 0
            # Factor 1: Drawdown
            if dd <= -35.0:
                score += 25
            elif dd <= -20.0:
                score += 15

            # Factor 2: Proximity to 52W Low
            if 10.0 <= prox <= 40.0:
                score += 25
            elif prox < 10.0:
                score += 10

            # Factor 3: Moving Average Structure
            if ma20_pct >= 0.0 and ma60_pct >= 0.0:
                score += 30
            elif ma20_pct >= -1.5:
                score += 20
            elif ma20_pct >= -5.0:
                score += 10

            # Factor 4: Volume Surge
            if vol >= 1.35:
                score += 20
            elif vol >= 1.15:
                score += 12

            # 4 Ignition Conditions
            c1 = bool(dd <= -20.0)
            c2 = bool(10.0 <= prox <= 45.0)
            c3 = bool(ma20_pct >= -0.5 and ma60_pct >= -4.5)
            c4 = bool(vol >= 1.30 or (ret20d is not None and ret20d >= 8.0))
            all_4 = bool(c1 and c2 and c3 and c4 and (t not in VALUE_TRAPS))

            # Technical Zone Classification & Modifiers
            if t in VALUE_TRAPS:
                zone_code = "VALUE_TRAP_FILTERED"
                zone_label_en = "VALUE TRAP · EXCLUDED"
                zone_label_jp = "バリュートラップ · 除外"
                zone_label_kr = "밸류 트랩 · 자동 배제"
                score = max(15, score - 40)
            elif (
                10.0 <= prox <= 45.0
                and ma20_pct >= -0.5
                and ma60_pct >= -4.5
                and vol >= 1.30
                and dd <= -20.0
            ):
                zone_code = "IGNITION_ZONE"
                zone_label_en = "RIGHT-SIDE IGNITION"
                zone_label_jp = "右側イグニッション"
                zone_label_kr = "우측 돌파 시동 (Ignition)"
                score = max(score, 84)
            elif prox < 10.0 and ma20_pct < 0.0:
                zone_code = "LEFT_SIDE_KNIFE"
                zone_label_en = "DOWNTREND · KNIFE"
                zone_label_jp = "左側下落 · 監視外"
                zone_label_kr = "좌측 하락추세 · 주의"
            else:
                zone_code = "WASHOUT_WATCH"
                zone_label_en = "WASHOUT BASE · WATCH"
                zone_label_jp = "出来高クライマックス · 監視"
                zone_label_kr = "워시아웃 베이스 · 대기"

            pw_score = int(min(98, max(0, score)))

            # Multilingual display names
            if t in STOCK_NAMES:
                name_en, name_jp, name_kr, sector = STOCK_NAMES[t]
            elif ".KS" in t or ".KQ" in t:
                name_en = f"{t} (KR)"
                name_jp = f"{t} (韓国)"
                name_kr = f"{t} (한국주)"
                sector = "Korean Equity"
            else:
                name_en = f"{t} Corp"
                name_jp = f"{t}"
                name_kr = f"{t}"
                sector = "US Equity"

            stock_obj = StockBase(
                ticker=t,
                name=name_en,
                name_en=name_en,
                name_jp=name_jp,
                name_kr=name_kr,
                sector=sector,
                date=str(s.get("Date", "2026-10-14")),
                close=round(close, 2),
                low52=round(low52, 2),
                high52=round(high52, 2),
                prox_low52_pct=round(prox, 1),
                dd_high52_pct=round(dd, 1),
                vs_ma20_pct=round(ma20_pct, 1),
                vs_ma60_pct=round(ma60_pct, 1),
                vs_ma200_pct=round(ma200_pct, 1) if ma200_pct is not None else None,
                ma20_price=ma20_val,
                ma60_price=ma60_val,
                rsi14=round(rsi, 1),
                vol_surge_10d=round(vol, 2),
                ret_5d_pct=round(ret5d, 1) if ret5d is not None else None,
                ret_20d_pct=round(ret20d, 1) if ret20d is not None else None,
                hist_2x_rate=round(hist_2x, 1),
                hist_med_gain=round(hist_med, 1),
                score=pw_score,
                zone_code=zone_code,
                zone_label_en=zone_label_en,
                zone_label_jp=zone_label_jp,
                zone_label_kr=zone_label_kr,
                c1_deep_dd=c1,
                c2_off_low=c2,
                c3_above_mas=c3,
                c4_vol_or_mom=c4,
                c2_sweet_spot=c2,
                c3_ma_reclaim=c3,
                c4_vol_washout=c4,
                all_4_ignition_met=all_4,
                stop_loss_price=stop_loss_val,
                tp1_2x_price=tp1_val,
                entry_trigger_price=entry_trigger_val,
                pct_to_trigger=pct_to_trig,
            )
            # Retain computed targets for unmasking
            stock_obj._stop_loss_price = stop_loss_val  # type: ignore[attr-defined]
            stock_obj._tp1_2x_price = tp1_val  # type: ignore[attr-defined]
            stock_obj._ma60_price = ma60_val  # type: ignore[attr-defined]
            stock_obj._entry_trigger_price = entry_trigger_val  # type: ignore[attr-defined]
            stock_obj._pct_to_trigger = pct_to_trig  # type: ignore[attr-defined]

            parsed_stocks.append(stock_obj)

        # Primary sort: Priority tickers first, then by descending score
        parsed_stocks.sort(
            key=lambda x: (
                0 if x.ticker in PRIORITY_TICKERS else 1,
                PRIORITY_TICKERS.index(x.ticker) if x.ticker in PRIORITY_TICKERS else 99,
                -x.score,
            )
        )

        self.stocks = parsed_stocks
        self.stocks_by_ticker = {s.ticker: s for s in self.stocks}
        self.preview_tickers = {s.ticker for s in self.stocks[:4]}

    def _load_backtest(self):
        bt_file = settings.BACKTEST_DATA_PATH
        if not bt_file.exists():
            raise FileNotFoundError(f"Missing backtest file: {bt_file}")

        with open(bt_file, "r", encoding="utf-8", errors="replace") as f:
            raw = json.load(f)

        strategies_raw = raw.get("overall_summary", [])
        yearly_raw = raw.get("yearly_performance", [])
        trades_raw = raw.get("trade_log", [])

        strategies_models = [
            StrategySummary(
                strategy_name=item.get("Strategy", ""),
                final_multiple=float(item.get("Final_Multiple", 0.0)),
                cumulative_return_pct=float(item.get("Cumulative_Return_Pct", 0.0)),
                cagr_pct=float(item.get("CAGR_Pct", 0.0)),
                max_drawdown_pct=float(item.get("Max_Drawdown_Pct", 0.0)),
                sharpe_ratio=float(item.get("Sharpe_Ratio", 0.0)),
                calmar_ratio=float(item.get("Calmar_Ratio", 0.0)),
            )
            for item in strategies_raw
        ]

        yearly_models = [
            YearlyPerformance(
                year=int(y.get("Year", 2000)),
                pw_rsi_return_pct=float(y.get("PW_RSI_Return_Pct", 0.0)),
                pw_pure_price_return_pct=float(y.get("PW_PurePrice_Return_Pct", 0.0)),
                naive_52w_low_return_pct=float(y.get("Naive_52W_Low_Return_Pct", 0.0)),
                qqq_return_pct=float(y.get("QQQ_Return_Pct", 0.0)),
                spy_return_pct=float(y.get("SPY_Return_Pct", 0.0)),
                alpha_vs_qqq_pct=float(y.get("Alpha_vs_QQQ_Pct", 0.0)),
                pw_rsi_mdd_pct=float(y.get("PW_RSI_IntraYear_MDD_Pct", 0.0)),
                nav_multiple=float(y.get("Nav_Multiple", 1.0)),
                key_switched_stocks=y.get("Key_Switched_Stocks"),
            )
            for y in yearly_raw
        ]

        self.trade_logs = trades_raw
        kpis = BacktestKpis()

        # Store dictionary format for .get() compatibility and JSON response
        self.backtest_data = {
            "period": raw.get("period", "2000-01-03 ~ 2026-10-13 (26.78 Years)"),
            "universe_size": int(raw.get("universe_size", 126)),
            "kpis": kpis.model_dump(),
            "strategies": strategies_raw,
            "overall_summary": strategies_raw,
            "yearly_performance": yearly_raw,
            "total_trades_count": int(raw.get("total_trades_count", len(trades_raw))),
        }

        self.backtest_summary_obj = BacktestSummaryResponse(
            period=raw.get("period", "2000-01-03 ~ 2026-10-13 (26.78 Years)"),
            universe_size=int(raw.get("universe_size", 126)),
            kpis=kpis,
            strategies=strategies_models,
            overall_summary=strategies_models,
            yearly_performance=yearly_models,
            total_trades_count=int(raw.get("total_trades_count", len(trades_raw))),
        )

    def _load_research(self):
        picks_dir = settings.WEEKLY_PICKS_DIR
        self.research_briefs = {}
        self.research_summaries = []

        if not picks_dir.exists():
            return

        for p in picks_dir.glob("*.md"):
            content = p.read_text(encoding="utf-8", errors="replace")
            fname = p.name

            # Extract ticker
            m_ticker = re.search(r"대상\s*기업[*\s:]+([^(]+)\(([^)]+)\)", content)
            if m_ticker:
                ticker = m_ticker.group(2).strip().upper()
                cname = m_ticker.group(1).strip()
            else:
                ticker = fname.split("_")[-1].replace(".md", "").upper()
                cname = ticker

            # Extract report date
            m_date = re.search(r"보고서\s*발행일자[*\s:]+([0-9-]+)", content)
            rdate = m_date.group(1).strip() if m_date else fname.split("_")[0]

            # Extract opinion
            m_op = re.search(r"투자의견[*\s:]+\*+([^*]+)\*+", content)
            op = m_op.group(1).strip() if m_op else "STRONG_BUY"

            # Extract score
            m_sc = re.search(r"종합\s*턴어라운드\s*스코어[*\s:]+\*+([0-9.]+)", content)
            score = float(m_sc.group(1)) if m_sc else 75.0

            # Synchronize with latest closing price from quant_engine
            stock = self.stocks_by_ticker.get(ticker)
            if stock is not None:
                c_price = stock.close
                s_price = getattr(stock, "_stop_loss_price", round(c_price * 0.91, 2))
                t_price = getattr(stock, "_tp1_2x_price", round(c_price * 2.00, 2))
                as_of_date = stock.date
                score = float(stock.score)
                # Synchronize stale snapshot prices inside markdown executive summary to latest close
                content = re.sub(
                    r"\|\s*\*\*현재가\s*\(Current Price[^)]*\)\*\*\s*\|\s*\*\*\$[0-9.]+\*\*\s*\|[^|\n]+\|",
                    f"| **현재가 (Current Price · {as_of_date} 최신 종가)** | **${c_price:.2f}** | 52주 신저가(${stock.low52:.2f}) 대비 +{stock.prox_low52_pct:.1f}% 바닥권 안착 |",
                    content,
                )
                content = re.sub(
                    r"\|\s*\*\*52주 가격 범위\s*\(52W Range\)\*\*\s*\|[^|\n]+\|[^|\n]+\|",
                    f"| **52주 가격 범위 (52W Range)** | ${stock.low52:.2f} ~ ${stock.high52:.2f} | 52주 최고점 대비 {stock.dd_high52_pct:.1f}% 과매도 구간 |",
                    content,
                )
                content = re.sub(
                    r"\|\s*\*\*(?:핵심 지지선|-9% 손절 기준가)\s*\([^)]+\)\*\*\s*\|[^|\n]+\|[^|\n]+\|",
                    f"| **-9% 손절 기준가 (Hard Stop Floor)** | ${s_price:.2f} | 진입가(${c_price:.2f}) 대비 -9.0% 기계적 칼손절 안전마진 |",
                    content,
                )
                content = re.sub(
                    r"\|\s*\*\*TP1 1차 목표가\s*\([^)]+\)\*\*\s*\|[^|\n]+\|[^|\n]+\|",
                    f"| **TP1 1차 목표가 (원금 100% 회수 · 2x)** | **${t_price:.2f}** | **기대 수익률 +100.0% (50% 매도로 투자원금 100% 무위험화)** |",
                    content,
                )
                content = re.sub(
                    r"\|\s*\*\*비대칭 기대 손익비\s*\(RRR\)\*\*\s*\|[^|\n]+\|[^|\n]+\|",
                    "| **비대칭 기대 손익비 (RRR)** | **1 : 11.1** | 비대칭 손익비 (하방 -9.0% vs 상방 +100.0%) |",
                    content,
                )
            else:
                c_price = 27.93 if ticker == "CELH" else 7.02
                s_price = round(c_price * 0.91, 2)
                t_price = round(c_price * 2.00, 2)
                as_of_date = "2026-10-13"

            rrr_str = "1 : 11.1"
            title_str = f"{cname} (${ticker}) — {op} | Latest Close ${c_price:.2f} ({as_of_date})"

            brief = ResearchBriefDetail(
                ticker=ticker,
                company_name=cname,
                title=title_str,
                report_date=rdate,
                opinion=op,
                turnaround_score=score,
                current_price=c_price,
                target_price=t_price,
                stop_price=s_price,
                rrr_ratio=rrr_str,
                as_of_date=as_of_date,
                content=content,
                content_markdown=content,
                markdown=content,
                is_pro_locked=False,
            )

            if ticker not in self.research_briefs:
                self.research_briefs[ticker] = []
            self.research_briefs[ticker].append(brief)

            self.research_summaries.append(
                ResearchBriefSummary(
                    ticker=ticker,
                    company_name=cname,
                    title=title_str,
                    report_date=rdate,
                    opinion=op,
                    turnaround_score=score,
                    current_price=c_price,
                    target_price=t_price,
                    stop_price=s_price,
                    as_of_date=as_of_date,
                    file_name=fname,
                    is_pro_locked=False,
                )
            )

        for t in self.research_briefs:
            self.research_briefs[t].sort(key=lambda x: x.report_date, reverse=True)

        self.research_summaries.sort(key=lambda x: x.report_date, reverse=True)

    def get_stocks(
        self,
        is_pro: bool = False,
        zone: Optional[str] = None,
        search: Optional[str] = None,
        query: Optional[str] = None,
        sort_by: Optional[str] = None,
        order: str = "asc",
        limit: Optional[int] = None,
        offset: Optional[int] = 0,
    ) -> List[StockResponse]:
        """Returns filtered, sorted, and masked/unmasked stocks."""
        filtered = list(self.stocks)

        # Filter by Zone
        if zone:
            z_clean = zone.strip().upper()
            filtered = [s for s in filtered if s.zone_code == z_clean]

        # Search by Ticker / Name
        search_term = (search or query or "").strip().upper()
        if search_term:
            filtered = [
                s for s in filtered
                if search_term in s.ticker.upper()
                or search_term in s.name_en.upper()
                or search_term in s.name_kr.upper()
                or search_term in s.name.upper()
            ]

        # Sort
        if sort_by:
            sort_field = sort_by.lower().strip()
            reverse = order.lower().strip() == "desc"
            if sort_field in ("score", "pw_score"):
                filtered.sort(key=lambda s: s.score, reverse=reverse)
            elif sort_field in ("close", "price"):
                filtered.sort(key=lambda s: s.close, reverse=reverse)
            elif sort_field in ("prox_low52_pct", "prox"):
                filtered.sort(key=lambda s: s.prox_low52_pct, reverse=reverse)
            elif sort_field in ("dd_high52_pct", "dd"):
                filtered.sort(key=lambda s: s.dd_high52_pct, reverse=reverse)
            elif sort_field in ("vol_surge_10d", "vol"):
                filtered.sort(key=lambda s: s.vol_surge_10d, reverse=reverse)

        # Apply offset and limit
        if offset is not None and offset > 0:
            filtered = filtered[offset:]

        if limit is not None:
            if limit <= 0:
                return []
            filtered = filtered[:limit]

        # Apply public vs Pro masking
        results: List[StockResponse] = []
        for s in filtered:
            d = s.model_dump()
            # Only authorized preview tickers (CELH, CCL, TSLA, UPST) or Pro subscribers are unmasked
            if is_pro or s.ticker in self.preview_tickers:
                d["is_pro_locked"] = False
                d["stop_loss_price"] = getattr(s, "_stop_loss_price", s.stop_loss_price)
                d["tp1_2x_price"] = getattr(s, "_tp1_2x_price", s.tp1_2x_price)
                d["ma60_price"] = getattr(s, "_ma60_price", s.ma60_price)
                d["entry_trigger_price"] = getattr(s, "_entry_trigger_price", s.entry_trigger_price)
                d["pct_to_trigger"] = getattr(s, "_pct_to_trigger", s.pct_to_trigger)
            else:
                d["is_pro_locked"] = True
                d["stop_loss_price"] = None
                d["tp1_2x_price"] = None
                d["ma60_price"] = None
                d["entry_trigger_price"] = None
                d["pct_to_trigger"] = None
            results.append(StockResponse(**d))

        return results

    def get_stock(self, ticker: str, is_pro: bool = False) -> Optional[StockResponse]:
        """Returns single stock with appropriate masking."""
        t_clean = ticker.strip().upper()
        s = self.stocks_by_ticker.get(t_clean)
        if not s:
            return None

        d = s.model_dump()
        # Preview tickers are unmasked even for free tier
        if is_pro or t_clean in self.preview_tickers:
            d["is_pro_locked"] = False
            d["stop_loss_price"] = getattr(s, "_stop_loss_price", s.stop_loss_price)
            d["tp1_2x_price"] = getattr(s, "_tp1_2x_price", s.tp1_2x_price)
            d["ma60_price"] = getattr(s, "_ma60_price", s.ma60_price)
            d["entry_trigger_price"] = getattr(s, "_entry_trigger_price", s.entry_trigger_price)
            d["pct_to_trigger"] = getattr(s, "_pct_to_trigger", s.pct_to_trigger)
        else:
            d["is_pro_locked"] = True
            d["stop_loss_price"] = None
            d["tp1_2x_price"] = None
            d["ma60_price"] = None
            d["entry_trigger_price"] = None
            d["pct_to_trigger"] = None

        return StockResponse(**d)

    def get_research_brief(self, ticker: str) -> Optional[str]:
        """Returns raw markdown research brief for given ticker or None."""
        t_clean = ticker.strip().upper()
        briefs = self.research_briefs.get(t_clean)
        if briefs and len(briefs) > 0:
            return briefs[0].content
        return None

    def get_research_brief_detail(
        self, ticker: str, is_pro: bool = False
    ) -> Optional[ResearchBriefDetail]:
        """Returns research brief detail without artificial truncation."""
        t_clean = ticker.strip().upper()
        briefs = self.research_briefs.get(t_clean)
        if not briefs or len(briefs) == 0:
            return None

        return briefs[0]

    def list_research_briefs(self, is_pro: bool = False) -> List[ResearchBriefSummary]:
        """Lists available research briefs."""
        return self.research_summaries

    def diagnose_position(
        self,
        ticker: str,
        entry_price: float,
        days_held: int,
        current_price: Optional[float] = None,
    ) -> PositionDoctorResponse:
        """Evaluates position against the 4 asymmetric exit rules."""
        t_clean = ticker.strip().upper()
        if entry_price <= 0:
            entry_price = 1.0

        stock = self.stocks_by_ticker.get(t_clean)
        if current_price is None:
            c_price = stock.close if stock else entry_price
        else:
            c_price = float(current_price)

        as_of_date = stock.date if stock else "2026-10-13"
        c_price_rnd = round(c_price, 2)
        e_price_rnd = round(float(entry_price), 2)
        stop_p = round(float(entry_price) * 0.91, 2)
        tp1_p = round(float(entry_price) * 2.00, 2)

        return_pct = round(((c_price / entry_price) - 1.0) * 100.0, 2)

        # Rule 1: -9% Hard Stop Loss
        if return_pct <= -9.0:
            return PositionDoctorResponse(
                ticker=t_clean,
                status_code="CRITICAL_STOP",
                status_label="🛑 Hard Stop Loss Triggered",
                return_pct=return_pct,
                rule_triggered="Rule 1 (-9.0% Hard Stop Loss)",
                action_plan="Execute immediate market exit. Do not average down on broken support.",
                is_critical=True,
                current_price=c_price_rnd,
                entry_price=e_price_rnd,
                stop_price=stop_p,
                tp1_price=tp1_p,
                as_of_date=as_of_date,
            )
        # Rule 2: 55-Day Dead-Money Time Stop
        elif days_held >= 55 and return_pct < 8.0:
            return PositionDoctorResponse(
                ticker=t_clean,
                status_code="DEAD_MONEY",
                status_label="⏳ 55-Day Time Stop Triggered",
                return_pct=return_pct,
                rule_triggered="Rule 2 (55-Day Dead-Money Exit)",
                action_plan="Exit position. Rebound momentum has stalled; reallocate into active right-side ignition candidates.",
                is_critical=False,
                current_price=c_price_rnd,
                entry_price=e_price_rnd,
                stop_price=stop_p,
                tp1_price=tp1_p,
                as_of_date=as_of_date,
            )
        # Rule 3: +100% Target Price 1 Capital Recovery
        elif return_pct >= 100.0:
            return PositionDoctorResponse(
                ticker=t_clean,
                status_code="TP1_REACHED",
                status_label="🎯 100% Target Price 1 Achieved",
                return_pct=return_pct,
                rule_triggered="Rule 3 (+100% Principal Recovery)",
                action_plan="Sell 50% of position to recoup 100% initial capital. Set trailing stop on remaining 50% using MA60.",
                is_critical=False,
                current_price=c_price_rnd,
                entry_price=e_price_rnd,
                stop_price=stop_p,
                tp1_price=tp1_p,
                as_of_date=as_of_date,
            )
        # Rule 4: Active Healthy Trend Following
        else:
            return PositionDoctorResponse(
                ticker=t_clean,
                status_code="ACTIVE_HOLD",
                status_label="🟢 Active Right-Side Trend Follow",
                return_pct=return_pct,
                rule_triggered="Rule 4 (Healthy Trend Follow)",
                action_plan="Maintain position. Monitor MA20/MA60 trailing support; runner target is +100% TP1.",
                is_critical=False,
                current_price=c_price_rnd,
                entry_price=e_price_rnd,
                stop_price=stop_p,
                tp1_price=tp1_p,
                as_of_date=as_of_date,
            )


quant_engine = QuantEngine.get_instance()
