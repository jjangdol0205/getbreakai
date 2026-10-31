"""
backend/app/services/telegram_service.py - Telegram Bot & Quant Alert Service
"""
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Optional, Tuple

import httpx

from backend.app.config import settings
from backend.app.models.telegram import (
    TelegramConfigRequest,
    TelegramDetectChatResponse,
    TelegramSendRequest,
    TelegramSendResponse,
    TelegramStatusResponse,
)
from backend.app.services.quant_engine import quant_engine
from backend.app.services.semi_engine import semi_engine


def mask_bot_token(token: str) -> str:
    """Safely masks a Telegram Bot token for UI display."""
    t = (token or "").strip()
    if not t:
        return ""
    if "..." in t:
        return t
    if len(t) <= 10:
        return f"{t[:2]}...{t[-2:]}"
    return f"{t[:6]}...{t[-4:]}"


class TelegramService:
    """
    Manages Telegram Bot configuration, real-time Quant & Semiconductor Fear & Greed
    briefing formatting, HTTP delivery via Telegram Bot API, chat ID auto-detection,
    and interactive command handling.
    """

    def __init__(self, config_path: Optional[Path] = None):
        self.config_path: Path = config_path or settings.TELEGRAM_CONFIG_PATH
        self._state: Dict[str, Any] = self._load_state()

    def _default_state(self) -> Dict[str, Any]:
        return {
            "bot_token": settings.TELEGRAM_BOT_TOKEN or "",
            "bot_username": "RightSideAlphaBot",
            "chat_id": settings.TELEGRAM_CHAT_ID or "",
            "channel_url": settings.TELEGRAM_CHANNEL_URL or "https://t.me/RightSideAlphaBot",
            "auto_alert_ignition": True,
            "auto_alert_stop_loss": True,
            "auto_alert_semi_extreme": True,
            "last_sent_at": None,
            "messages_sent_count": 0,
        }

    def _load_state(self) -> Dict[str, Any]:
        state = self._default_state()
        if self.config_path.exists():
            try:
                raw = json.loads(self.config_path.read_text(encoding="utf-8"))
                if isinstance(raw, dict):
                    for k in state:
                        if k in raw and raw[k] is not None:
                            state[k] = raw[k]
            except Exception:
                pass
        # Fallback to environment settings if stored values are empty
        if not state.get("bot_token") and settings.TELEGRAM_BOT_TOKEN:
            state["bot_token"] = settings.TELEGRAM_BOT_TOKEN
        if not state.get("chat_id") and settings.TELEGRAM_CHAT_ID:
            state["chat_id"] = settings.TELEGRAM_CHAT_ID
        if not state.get("channel_url"):
            state["channel_url"] = settings.TELEGRAM_CHANNEL_URL or "https://t.me/RightSideAlphaBot"
        return state

    def _save_state(self) -> None:
        try:
            self.config_path.parent.mkdir(parents=True, exist_ok=True)
            self.config_path.write_text(
                json.dumps(self._state, ensure_ascii=False, indent=2),
                encoding="utf-8",
            )
        except Exception:
            pass

    def _resolve_token(self, override_token: Optional[str] = None) -> str:
        if override_token is not None:
            cand = override_token.strip()
            if cand and "..." not in cand:
                return cand
        stored = str(self._state.get("bot_token") or "").strip()
        if stored and "..." not in stored:
            return stored
        return (settings.TELEGRAM_BOT_TOKEN or "").strip()

    def _resolve_chat_id(self, override_chat_id: Optional[str] = None) -> str:
        if override_chat_id is not None and override_chat_id.strip():
            return override_chat_id.strip()
        stored = str(self._state.get("chat_id") or "").strip()
        if stored:
            return stored
        return (settings.TELEGRAM_CHAT_ID or "").strip()

    def get_status(self) -> TelegramStatusResponse:
        token = self._resolve_token()
        chat_id = self._resolve_chat_id()
        if token and not chat_id:
            det = self.detect_chat_id(bot_token=token)
            if det.ok and det.chat_id:
                chat_id = det.chat_id
        configured = bool(token and chat_id)
        return TelegramStatusResponse(
            configured=configured,
            bot_token_masked=mask_bot_token(token),
            bot_username=self._state.get("bot_username") or "RightSideAlphaBot",
            chat_id=chat_id,
            channel_url=self._state.get("channel_url") or "https://t.me/RightSideAlphaBot",
            auto_alert_ignition=bool(self._state.get("auto_alert_ignition", True)),
            auto_alert_stop_loss=bool(self._state.get("auto_alert_stop_loss", True)),
            auto_alert_semi_extreme=bool(self._state.get("auto_alert_semi_extreme", True)),
            last_sent_at=self._state.get("last_sent_at"),
            messages_sent_count=int(self._state.get("messages_sent_count", 0)),
        )

    def update_config(self, req: TelegramConfigRequest) -> TelegramStatusResponse:
        if req.bot_token is not None:
            clean_token = req.bot_token.strip()
            # Only overwrite stored token if it is not a masked placeholder containing "..."
            if "..." not in clean_token:
                self._state["bot_token"] = clean_token
        if req.chat_id is not None:
            self._state["chat_id"] = req.chat_id.strip()
        if req.channel_url is not None and req.channel_url.strip():
            self._state["channel_url"] = req.channel_url.strip()

        self._state["auto_alert_ignition"] = bool(req.auto_alert_ignition)
        self._state["auto_alert_stop_loss"] = bool(req.auto_alert_stop_loss)
        self._state["auto_alert_semi_extreme"] = bool(req.auto_alert_semi_extreme)
        self._save_state()
        return self.get_status()

    # -------------------------------------------------------------------------
    # Rich Quant & Semiconductor Message Builders (100% synced with engines)
    # -------------------------------------------------------------------------

    def build_test_message(self, lang: str = "kr") -> str:
        if not quant_engine.is_loaded:
            quant_engine.initialize()
        if not semi_engine.is_loaded:
            semi_engine.initialize()

        ignition_stocks = quant_engine.get_stocks(is_pro=True, zone="IGNITION_ZONE")
        semi_ov = semi_engine.get_overview()

        top_summary = ", ".join(
            f"<b>${s.ticker}</b> (${s.close:.2f})" for s in ignition_stocks[:5]
        )

        if (lang or "kr").lower() == "en":
            lines = [
                "🟢 <b>[RightSideAlpha × SemiFearGreed] Telegram Alert Link Verified</b>",
                "━━━━━━━━━━━━━━━━━━━━",
                f"📡 <b>Status</b>: Connected & Ready ({len(quant_engine.stocks)} US Stocks / 26Y Barbell Engine)",
                f"🔥 <b>Active Ignition Zone ({len(ignition_stocks)})</b>: {top_summary}",
                (
                    f"🧭 <b>Semi Fear & Greed</b>: <b>{semi_ov.fg_score:.1f} / 100 ({semi_ov.regime_code.replace('_', ' ')})</b> "
                    f"— Directive: <b>{semi_ov.recommended_smh_weight}% $SMH : {semi_ov.recommended_xlv_weight}% $XLV</b>"
                ),
                (
                    f"📊 <b>ETF Snapshot</b>: $SMH ${semi_ov.smh_close:.2f} ({semi_ov.smh_dd_pct:.2f}% DD) | "
                    f"$XLV ${semi_ov.xlv_close:.2f} | $QQQ ${semi_ov.qqq_close:.2f}"
                ),
                "━━━━━━━━━━━━━━━━━━━━",
                "💡 Commands: <code>/ignition</code> · <code>/semi</code> · <code>/stock CELH</code> · <code>/doctor CELH 27.20 42</code>",
            ]
        else:
            lines = [
                "🟢 <b>[RightSideAlpha × SemiFearGreed] 텔레그램 퀀트 알림 연동 완료</b>",
                "━━━━━━━━━━━━━━━━━━━━",
                f"📡 <b>엔진 상태</b>: 정상 가동 중 (미국주식 {len(quant_engine.stocks)}종목 · 26년 바벨 엔진)",
                f"🔥 <b>우측 돌파 시동 (Ignition {len(ignition_stocks)}선)</b>: {top_summary}",
                (
                    f"🧭 <b>반도체 공포·탐욕 지수</b>: <b>{semi_ov.fg_score:.1f} / 100 ({semi_ov.regime_code.replace('_', ' ')} · {semi_ov.regime_kr})</b>\n"
                    f"   └ 포트폴리오 지침: <b>{semi_ov.recommended_smh_weight}% $SMH : {semi_ov.recommended_xlv_weight}% $XLV</b> 역발상 바벨"
                ),
                (
                    f"📊 <b>핵심 ETF 종가</b>: $SMH ${semi_ov.smh_close:.2f} (52주 고점대비 {semi_ov.smh_dd_pct:.2f}%) | "
                    f"$XLV ${semi_ov.xlv_close:.2f} | $QQQ ${semi_ov.qqq_close:.2f}"
                ),
                "━━━━━━━━━━━━━━━━━━━━",
                "💡 봇 명령어: <code>/ignition</code> · <code>/semi</code> · <code>/stock CELH</code> · <code>/doctor CELH 27.20 42</code>",
            ]
        return "\n".join(lines)

    def build_ignition_briefing(self, lang: str = "kr") -> str:
        if not quant_engine.is_loaded:
            quant_engine.initialize()

        ignition_stocks = quant_engine.get_stocks(is_pro=True, zone="IGNITION_ZONE")
        as_of = ignition_stocks[0].date if ignition_stocks else "2026-10-13"

        if (lang or "kr").lower() == "en":
            lines = [
                f"🚀 <b>[RightSideAlpha] Right-Side Ignition Zone Briefing ({as_of})</b>",
                f"Qualified 4-Condition Turnaround Candidates: <b>{len(ignition_stocks)} Stocks</b>",
                "━━━━━━━━━━━━━━━━━━━━",
            ]
            for idx, s in enumerate(ignition_stocks, 1):
                lines.append(
                    f"{idx}. <b>${s.ticker}</b> ({s.name_en}) — Close <b>${s.close:.2f}</b> | Score <b>{s.score}</b>/100\n"
                    f"   • 52W DD: {s.dd_high52_pct:.1f}% | Off 52W Low: +{s.prox_low52_pct:.1f}% | Vol Surge: {s.vol_surge_10d:.2f}x\n"
                    f"   • 🎯 <b>TRG</b>: <code>${s.entry_trigger_price:.2f}</code> | "
                    f"🛑 <b>STP (-9%)</b>: <code>${s.stop_loss_price:.2f}</code> | "
                    f"💰 <b>TP1 (2x)</b>: <code>${s.tp1_2x_price:.2f}</code>"
                )
            lines.append("━━━━━━━━━━━━━━━━━━━━")
            lines.append("📌 <i>Exit Rules: -9.0% Hard Stop | 55-Day Time Stop | +100% TP1 (50% Principal Recovery)</i>")
        else:
            lines = [
                f"🚀 <b>[RightSideAlpha] 우측 돌파 시동 (IGNITION ZONE) 브리핑 ({as_of})</b>",
                f"4대 우측 시동 조건 완벽 충족: <b>총 {len(ignition_stocks)}종목</b>",
                "━━━━━━━━━━━━━━━━━━━━",
            ]
            for idx, s in enumerate(ignition_stocks, 1):
                lines.append(
                    f"{idx}. <b>${s.ticker}</b> ({s.name_kr}) — 종가 <b>${s.close:.2f}</b> | PW-RSI <b>{s.score}점</b>\n"
                    f"   • 고점대비: {s.dd_high52_pct:.1f}% | 저점대비: +{s.prox_low52_pct:.1f}% | 거래량급증: {s.vol_surge_10d:.2f}배\n"
                    f"   • 🎯 <b>TRG(진입)</b>: <code>${s.entry_trigger_price:.2f}</code> | "
                    f"🛑 <b>STP(-9% 손절)</b>: <code>${s.stop_loss_price:.2f}</code> | "
                    f"💰 <b>TP1(2x 목표)</b>: <code>${s.tp1_2x_price:.2f}</code>"
                )
            lines.append("━━━━━━━━━━━━━━━━━━━━")
            lines.append("📌 <i>비대칭 4대 원칙: -9.0% 기계적 칼손절 | 55일 시간손절 | +100% TP1 도달 시 50% 매도 원금회수</i>")

        return "\n".join(lines)

    def build_semi_briefing(self, lang: str = "kr") -> str:
        if not semi_engine.is_loaded:
            semi_engine.initialize()

        ov = semi_engine.get_overview()
        etf_map = {e.ticker: e for e in ov.etfs}
        smh_etf = etf_map.get("SMH")
        xlv_etf = etf_map.get("XLV")
        qqq_etf = etf_map.get("QQQ")

        smh_dd = smh_etf.dd_52w_pct if smh_etf else ov.smh_dd_pct
        xlv_dd = xlv_etf.dd_52w_pct if xlv_etf else 0.0
        qqq_dd = qqq_etf.dd_52w_pct if qqq_etf else 0.0

        regime_display = ov.regime_code.replace("_", " ")

        if (lang or "kr").lower() == "en":
            lines = [
                f"🧭 <b>[SemiFearGreed] Semiconductor 7-Factor Fear & Greed ({ov.date})</b>",
                "━━━━━━━━━━━━━━━━━━━━",
                f"📊 <b>Composite Score</b>: <b>{ov.fg_score:.1f} / 100</b> — <b>{regime_display}</b> ({ov.regime_en})",
                f"⚡ <b>Barbell Directive</b>: <b>{ov.recommended_smh_weight}% $SMH : {ov.recommended_xlv_weight}% $XLV</b>",
                f"📣 <b>Signal</b>: {ov.action_headline_en}",
                "",
                "<b>[Core ETF Snapshot & 52W Drawdown]</b>",
                f"• <b>$SMH</b>: <b>${ov.smh_close:.2f}</b> (52W DD <b>{smh_dd:.2f}%</b> | RSI {ov.smh_rsi:.1f})",
                f"• <b>$XLV</b>: <b>${ov.xlv_close:.2f}</b> (52W DD <b>{xlv_dd:.2f}%</b>)",
                f"• <b>$QQQ</b>: <b>${ov.qqq_close:.2f}</b> (52W DD <b>{qqq_dd:.2f}%</b>)",
                "━━━━━━━━━━━━━━━━━━━━",
                f"💡 <i>{ov.action_detail_en}</i>",
            ]
        else:
            lines = [
                f"🧭 <b>[SemiFearGreed] 반도체 7-팩터 공포·탐욕 지수 브리핑 ({ov.date})</b>",
                "━━━━━━━━━━━━━━━━━━━━",
                f"📊 <b>현재 지수</b>: <b>{ov.fg_score:.1f} / 100</b> — <b>{regime_display} ({ov.regime_kr})</b>",
                f"⚡ <b>권장 바벨 비중</b>: <b>{ov.recommended_smh_weight}% $SMH : {ov.recommended_xlv_weight}% $XLV</b> Contrarian Barbell",
                f"📣 <b>핵심 지침</b>: {ov.action_headline_kr}",
                "",
                "<b>[핵심 ETF 종가 및 52주 고점 대비 낙폭]</b>",
                f"• <b>$SMH</b> (반도체 70% 성장엔진): <b>${ov.smh_close:.2f}</b> (52W DD <b>{smh_dd:.2f}%</b> | RSI {ov.smh_rsi:.1f})",
                f"• <b>$XLV</b> (헬스케어 30% 방어금고): <b>${ov.xlv_close:.2f}</b> (52W DD <b>{xlv_dd:.2f}%</b>)",
                f"• <b>$QQQ</b> (나스닥100 벤치마크): <b>${ov.qqq_close:.2f}</b> (52W DD <b>{qqq_dd:.2f}%</b>)",
                "━━━━━━━━━━━━━━━━━━━━",
                f"💡 <i>{ov.action_detail_kr}</i>",
            ]
        return "\n".join(lines)

    def build_doctor_alert(
        self,
        ticker: str = "CELH",
        entry_price: float = 27.20,
        days_held: int = 42,
        lang: str = "kr",
    ) -> str:
        if not quant_engine.is_loaded:
            quant_engine.initialize()

        t_clean = (ticker or "CELH").strip().upper()
        e_price = float(entry_price) if entry_price and entry_price > 0 else 27.20
        d_held = int(days_held) if days_held is not None and days_held >= 0 else 42

        diag = quant_engine.diagnose_position(
            ticker=t_clean,
            entry_price=e_price,
            days_held=d_held,
        )

        if (lang or "kr").lower() == "en":
            lines = [
                f"🩺 <b>[Position Doctor] Asymmetric Exit Diagnosis — ${diag.ticker}</b>",
                "━━━━━━━━━━━━━━━━━━━━",
                f"• <b>Status</b>: {diag.status_label} (<code>{diag.status_code}</code>)",
                f"• <b>Latest Close ({diag.as_of_date})</b>: <b>${diag.current_price:.2f}</b>",
                f"• <b>Cost Basis (Entry)</b>: <b>${diag.entry_price:.2f}</b> ({d_held} trading days held)",
                f"• <b>Current Return</b>: <b>{diag.return_pct:+.2f}%</b>",
                f"• <b>Rule Triggered</b>: {diag.rule_triggered}",
                f"• 🛑 <b>Hard Stop (-9%)</b>: <code>${diag.stop_price:.2f}</code> | 💰 <b>TP1 (2x)</b>: <code>${diag.tp1_price:.2f}</code>",
                "━━━━━━━━━━━━━━━━━━━━",
                f"📋 <b>Action Plan</b>: {diag.action_plan}",
            ]
        else:
            lines = [
                f"🩺 <b>[Position Doctor] 보유 포지션 4대 출구 판독 — ${diag.ticker}</b>",
                "━━━━━━━━━━━━━━━━━━━━",
                f"• <b>진단 상태</b>: {diag.status_label} (<code>{diag.status_code}</code>)",
                f"• <b>최신 종가 ({diag.as_of_date})</b>: <b>${diag.current_price:.2f}</b>",
                f"• <b>매수 평단가</b>: <b>${diag.entry_price:.2f}</b> (보유 {d_held}거래일)",
                f"• <b>현재 수익률</b>: <b>{diag.return_pct:+.2f}%</b>",
                f"• <b>적용 규칙</b>: {diag.rule_triggered}",
                f"• 🛑 <b>-9% 칼손절가</b>: <code>${diag.stop_price:.2f}</code> | 💰 <b>TP1 (2x 목표가)</b>: <code>${diag.tp1_price:.2f}</code>",
                "━━━━━━━━━━━━━━━━━━━━",
                f"📋 <b>실행 지침</b>: {diag.action_plan}",
            ]
        return "\n".join(lines)

    def build_stock_card(self, ticker: str, lang: str = "kr") -> str:
        if not quant_engine.is_loaded:
            quant_engine.initialize()

        t_clean = (ticker or "").strip().upper().lstrip("$")
        s = quant_engine.get_stock(t_clean, is_pro=True)
        if not s:
            return (
                f"⚠️ <b>Ticker Not Found</b>: <code>{t_clean}</code> is not in the 72-stock RightSideAlpha universe.\n"
                "Try <code>/stock CELH</code>, <code>/stock TSLA</code>, <code>/stock NVDA</code>, or <code>/ignition</code>."
            )

        c_flags = (
            f"C1(DD≤-20%): {'✅' if s.c1_deep_dd else '❌'} | "
            f"C2(OffLow): {'✅' if s.c2_off_low else '❌'} | "
            f"C3(MA): {'✅' if s.c3_above_mas else '❌'} | "
            f"C4(Vol): {'✅' if s.c4_vol_or_mom else '❌'}"
        )
        zone_display = (
            s.zone_code.replace("_", " ")
            if (lang or "kr").lower() == "en"
            else f"{s.zone_label_kr} (<code>{s.zone_code}</code>)"
        )
        title_name = (
            s.name_en
            if (lang or "kr").lower() == "en"
            else f"{s.name_kr} ({s.name_en})"
        )
        return (
            f"📈 <b>[RightSideAlpha Stock Card] ${s.ticker} — {title_name}</b>\n"
            "━━━━━━━━━━━━━━━━━━━━\n"
            f"• <b>Sector</b>: {s.sector} | <b>As of</b>: {s.date}\n"
            f"• <b>Latest Close</b>: <b>${s.close:.2f}</b> (52W Range: ${s.low52:.2f} ~ ${s.high52:.2f})\n"
            f"• <b>PW-RSI Score</b>: <b>{s.score} / 100</b> — <b>{zone_display}</b>\n"
            f"• <b>52W Drawdown</b>: {s.dd_high52_pct:.1f}% | <b>Off 52W Low</b>: +{s.prox_low52_pct:.1f}%\n"
            f"• <b>RSI(14)</b>: {s.rsi14:.1f} | <b>10D Vol Surge</b>: {s.vol_surge_10d:.2f}x\n"
            f"• 🎯 <b>Entry Trigger (TRG)</b>: <code>${s.entry_trigger_price:.2f}</code>\n"
            f"• 🛑 <b>Hard Stop (-9% STP)</b>: <code>${s.stop_loss_price:.2f}</code>\n"
            f"• 💰 <b>Target 1 (+100% TP1)</b>: <code>${s.tp1_2x_price:.2f}</code>\n"
            "━━━━━━━━━━━━━━━━━━━━\n"
            f"🔍 <b>Ignition Checklist</b>: {c_flags}"
        )

    def build_full_morning_briefing(self, lang: str = "kr") -> str:
        if not quant_engine.is_loaded:
            quant_engine.initialize()
        if not semi_engine.is_loaded:
            semi_engine.initialize()

        ignition_part = self.build_ignition_briefing(lang=lang)
        semi_part = self.build_semi_briefing(lang=lang)
        briefs = quant_engine.list_research_briefs(is_pro=True)

        research_lines = [
            "📑 <b>[Institutional Deep-Dive Research Top Picks]</b>",
        ]
        seen_tickers: set[str] = set()
        for b in briefs:
            if b.ticker in seen_tickers:
                continue
            seen_tickers.add(b.ticker)
            research_lines.append(
                f"• <b>${b.ticker}</b> ({b.company_name}) — <b>{b.opinion}</b> | "
                f"Close <b>${b.current_price:.2f}</b> | STP(-9%) <code>${b.stop_price:.2f}</code> | TP1(2x) <code>${b.target_price:.2f}</code>"
            )
        if not briefs:
            for fallback_t in ("CELH", "MBLY"):
                st = quant_engine.get_stock(fallback_t, is_pro=True)
                if st:
                    research_lines.append(
                        f"• <b>${st.ticker}</b> ({st.name_en}) — Close <b>${st.close:.2f}</b> | "
                        f"STP(-9%) <code>${st.stop_loss_price:.2f}</code> | TP1(2x) <code>${st.tp1_2x_price:.2f}</code>"
                    )

        header = (
            "🌅 <b>[RightSideAlpha × SemiFearGreed] Integrated Morning Quant Briefing</b>"
            if (lang or "kr").lower() == "en"
            else "🌅 <b>[RightSideAlpha × SemiFearGreed] 모닝 퀀트 통합 브리핑</b>"
        )

        return f"{header}\n\n{ignition_part}\n\n{semi_part}\n\n" + "\n".join(research_lines)

    # -------------------------------------------------------------------------
    # Telegram HTTP Delivery & Chat ID Detection
    # -------------------------------------------------------------------------

    def build_us_inline_keyboard(self) -> Dict[str, Any]:
        """Builds clickable Telegram Inline Keyboard buttons for US traders."""
        return {
            "inline_keyboard": [
                [
                    {
                        "text": "🖥️ Live US Quant Terminal (getbreakai.com)",
                        "url": "https://getbreakai.com",
                    },
                    {
                        "text": "▶️ YouTube (@rightsidealpha)",
                        "url": "https://www.youtube.com/@rightsidealpha",
                    },
                ],
                [
                    {"text": "🔥 Ignition Zone (5)", "callback_data": "/ignition"},
                    {"text": "🧭 Semi Fear & Greed", "callback_data": "/semi"},
                ],
                [
                    {
                        "text": "🩺 Position Doctor ($CELH)",
                        "callback_data": "/doctor CELH 27.20 42",
                    },
                    {"text": "🌅 Full Morning Brief", "callback_data": "/full"},
                ],
            ]
        }

    def send_message(
        self,
        text: str,
        override_token: Optional[str] = None,
        override_chat_id: Optional[str] = None,
        reply_markup: Optional[Dict[str, Any]] = None,
    ) -> Tuple[bool, bool, str]:
        """
        Delivers message to Telegram via Bot API if token and chat_id are present.
        Returns (delivered, simulated, detail).
        """
        token = self._resolve_token(override_token)
        chat_id = self._resolve_chat_id(override_chat_id)
        if token and not chat_id:
            det = self.detect_chat_id(bot_token=token)
            if det.ok and det.chat_id:
                chat_id = det.chat_id
        now_iso = datetime.now(timezone.utc).isoformat()

        if not token or not chat_id:
            return (
                False,
                True,
                "Simulated preview mode (configure TELEGRAM_BOT_TOKEN & TELEGRAM_CHAT_ID to deliver live messages)",
            )

        url = f"https://api.telegram.org/bot{token}/sendMessage"
        payload: Dict[str, Any] = {
            "chat_id": chat_id,
            "text": text,
            "parse_mode": "HTML",
            "disable_web_page_preview": True,
        }
        if reply_markup:
            payload["reply_markup"] = reply_markup
        try:
            with httpx.Client(timeout=6.0) as client:
                resp = client.post(url, json=payload)
                data = resp.json() if resp.content else {}
                if resp.status_code == 200 and data.get("ok"):
                    self._state["last_sent_at"] = now_iso
                    self._state["messages_sent_count"] = int(self._state.get("messages_sent_count", 0)) + 1
                    self._save_state()
                    return (True, False, f"Delivered to Telegram chat_id={chat_id}")
                desc = data.get("description") or f"HTTP {resp.status_code}"
                return (False, False, f"Telegram API error: {desc}")
        except Exception as exc:
            return (False, False, f"Telegram transport error: {exc}")

    def send_document(
        self,
        file_path: Path,
        caption: str = "",
        override_token: Optional[str] = None,
        override_chat_id: Optional[str] = None,
    ) -> Tuple[bool, bool, str]:
        """Uploads a PDF or document file to Telegram via sendDocument."""
        token = self._resolve_token(override_token)
        chat_id = self._resolve_chat_id(override_chat_id)
        if not file_path.exists():
            return (False, False, f"File not found: {file_path}")
        if not token or not chat_id:
            return (
                False,
                True,
                f"Simulated PDF upload preview for {file_path.name} (configure token & chat_id for live upload)",
            )

        url = f"https://api.telegram.org/bot{token}/sendDocument"
        try:
            with httpx.Client(timeout=20.0) as client:
                with open(file_path, "rb") as f:
                    files = {"document": (file_path.name, f, "application/pdf")}
                    data = {"chat_id": chat_id, "caption": caption[:1024], "parse_mode": "HTML"}
                    resp = client.post(url, data=data, files=files)
                res_json = resp.json() if resp.content else {}
                if resp.status_code == 200 and res_json.get("ok"):
                    self._state["last_sent_at"] = datetime.now(timezone.utc).isoformat()
                    self._state["messages_sent_count"] = int(self._state.get("messages_sent_count", 0)) + 1
                    self._save_state()
                    return (True, False, f"Uploaded document {file_path.name} to chat_id={chat_id}")
                desc = res_json.get("description") or f"HTTP {resp.status_code}"
                return (False, False, f"Telegram sendDocument error: {desc}")
        except Exception as exc:
            return (False, False, f"Telegram sendDocument transport error: {exc}")

    def dispatch_briefing(self, req: TelegramSendRequest) -> TelegramSendResponse:
        btype = (req.briefing_type or "full").strip().lower()
        lang = (req.lang or "kr").strip().lower()

        if req.custom_message and req.custom_message.strip():
            msg = req.custom_message.strip()
        elif btype == "test":
            msg = self.build_test_message(lang=lang)
        elif btype == "ignition":
            msg = self.build_ignition_briefing(lang=lang)
        elif btype == "semi":
            msg = self.build_semi_briefing(lang=lang)
        elif btype == "doctor":
            msg = self.build_doctor_alert(
                ticker=req.ticker or "CELH",
                entry_price=req.entry_price if req.entry_price is not None else 27.20,
                days_held=req.days_held if req.days_held is not None else 42,
                lang=lang,
            )
        else:
            btype = "full"
            msg = self.build_full_morning_briefing(lang=lang)

        delivered, simulated, detail = self.send_message(
            text=msg,
            override_token=req.bot_token,
            override_chat_id=req.chat_id,
        )
        effective_chat_id = self._resolve_chat_id(req.chat_id) or "SIMULATED_PREVIEW"
        now_iso = datetime.now(timezone.utc).isoformat()

        return TelegramSendResponse(
            ok=delivered or simulated,
            delivered=delivered,
            simulated=simulated,
            briefing_type=btype,
            chat_id=effective_chat_id,
            message_preview=msg,
            timestamp=now_iso,
            detail=detail,
        )

    def detect_chat_id(self, bot_token: Optional[str] = None) -> TelegramDetectChatResponse:
        token = self._resolve_token(bot_token)
        if not token:
            return TelegramDetectChatResponse(
                ok=False,
                chat_id=None,
                chat_title=None,
                username=None,
                detail="Bot token is not configured. Provide a valid Telegram Bot token from @BotFather first.",
            )

        url = f"https://api.telegram.org/bot{token}/getUpdates"
        try:
            with httpx.Client(timeout=6.0) as client:
                resp = client.get(url)
                data = resp.json() if resp.content else {}
                if resp.status_code != 200 or not data.get("ok"):
                    desc = data.get("description") or f"HTTP {resp.status_code}"
                    return TelegramDetectChatResponse(
                        ok=False,
                        detail=f"Telegram getUpdates failed: {desc}",
                    )

                results = data.get("result") or []
                for upd in reversed(results):
                    msg = (
                        upd.get("message")
                        or upd.get("channel_post")
                        or upd.get("edited_message")
                        or (upd.get("my_chat_member") or {})
                    )
                    chat = msg.get("chat") if isinstance(msg, dict) else None
                    if chat and chat.get("id") is not None:
                        cid = str(chat["id"])
                        title = (
                            chat.get("title")
                            or " ".join(filter(None, [chat.get("first_name"), chat.get("last_name")]))
                            or chat.get("username")
                            or "Telegram Chat"
                        )
                        uname = chat.get("username")
                        # Persist detected chat_id and token
                        self._state["bot_token"] = token
                        self._state["chat_id"] = cid
                        self._save_state()
                        return TelegramDetectChatResponse(
                            ok=True,
                            chat_id=cid,
                            chat_title=title,
                            username=uname,
                            detail=f"Detected chat_id={cid} ({title})",
                        )

                return TelegramDetectChatResponse(
                    ok=False,
                    detail="No recent messages found in getUpdates. Send '/start' to your bot in Telegram and try again.",
                )
        except Exception as exc:
            return TelegramDetectChatResponse(
                ok=False,
                detail=f"Error connecting to Telegram getUpdates: {exc}",
            )

    # -------------------------------------------------------------------------
    # Interactive Bot Command Parser (/start, /ignition, /semi, /doctor, /stock)
    # -------------------------------------------------------------------------

    def handle_webhook_update(self, update_dict: Dict[str, Any]) -> str:
        cb_query = update_dict.get("callback_query")
        if isinstance(cb_query, dict):
            cb_id = cb_query.get("id")
            token = self._resolve_token()
            if cb_id and token:
                try:
                    with httpx.Client(timeout=3.0) as client:
                        client.post(
                            f"https://api.telegram.org/bot{token}/answerCallbackQuery",
                            json={"callback_query_id": cb_id},
                        )
                except Exception:
                    pass
            msg_obj = cb_query.get("message") or {}
            text = str(cb_query.get("data") or "").strip()
        else:
            msg_obj = (
                update_dict.get("message")
                or update_dict.get("channel_post")
                or update_dict.get("edited_message")
                or {}
            )
            text = str(msg_obj.get("text") or "").strip()

        chat_obj = msg_obj.get("chat") or {}
        incoming_chat_id = str(chat_obj.get("id") or "").strip()

        if incoming_chat_id and not self._state.get("chat_id"):
            self._state["chat_id"] = incoming_chat_id
            self._save_state()

        if not text:
            return "No command text provided."

        parts = text.split()
        cmd = parts[0].lower().split("@")[0]
        # Default to US English ('en') for global/US trader target; allow 'kr' override
        bot_lang = "kr" if ("kr" in [p.lower() for p in parts[1:]] or cmd == "/kr") else "en"

        if cmd in ("/start", "/help", "/status", "/kr"):
            if bot_lang == "kr":
                reply = (
                    "🤖 <b>RightSideAlpha × SemiFearGreed Quant Bot</b>\n"
                    "━━━━━━━━━━━━━━━━━━━━\n"
                    "사용 가능한 실시간 퀀트 명령어:\n"
                    "• <code>/ignition</code> — 우측 돌파 시동 (IGNITION ZONE) 5종목 타점 브리핑\n"
                    "• <code>/semi</code> — 반도체 7-팩터 공포·탐욕 지수 & 80:20 바벨 지침\n"
                    "• <code>/stock &lt;TICKER&gt;</code> — 개별 종목 손절(-9%)/목표가(2x) 카드 (예: <code>/stock TSLA</code>)\n"
                    "• <code>/doctor &lt;TICKER&gt; &lt;ENTRY&gt; &lt;DAYS&gt;</code> — 포지션 닥터 진단 (예: <code>/doctor CELH 27.20 42</code>)\n"
                    "• <code>/full</code> — 모닝 퀀트 통합 브리핑\n"
                    "━━━━━━━━━━━━━━━━━━━━\n"
                    + self.build_test_message(lang="kr")
                )
            else:
                reply = (
                    "🤖 <b>RightSideAlpha × SemiFearGreed US Quant Bot</b>\n"
                    "🌐 <b>Live Web Terminal</b>: <a href=\"https://getbreakai.com\">https://getbreakai.com</a>\n"
                    "▶️ <b>YouTube Shorts</b>: <a href=\"https://www.youtube.com/@rightsidealpha\">youtube.com/@rightsidealpha</a>\n"
                    "━━━━━━━━━━━━━━━━━━━━\n"
                    "<b>Real-Time Institutional Quant Commands:</b>\n"
                    "• <code>/ignition</code> — Top 5 Right-Side Breakout Candidates (TRG / -9% Stop / 2x Target)\n"
                    "• <code>/semi</code> — Semiconductor 7-Factor Fear & Greed + 80:20 Barbell Directive\n"
                    "• <code>/stock &lt;TICKER&gt;</code> — Instant Stock Quant Card (e.g. <code>/stock NVDA</code>, <code>/stock TSLA</code>)\n"
                    "• <code>/doctor &lt;TICKER&gt; &lt;ENTRY&gt; &lt;DAYS&gt;</code> — Position Doctor 3s Audit (e.g. <code>/doctor CELH 27.20 42</code>)\n"
                    "• <code>/full</code> — Integrated US Morning Quant Briefing\n"
                    "━━━━━━━━━━━━━━━━━━━━\n"
                    + self.build_test_message(lang="en")
                )
        elif cmd == "/ignition":
            reply = self.build_ignition_briefing(lang=bot_lang)
        elif cmd == "/semi":
            reply = self.build_semi_briefing(lang=bot_lang)
        elif cmd == "/full":
            reply = self.build_full_morning_briefing(lang=bot_lang)
        elif cmd == "/stock":
            ticker_arg = parts[1] if len(parts) >= 2 and parts[1].lower() != "kr" else "CELH"
            reply = self.build_stock_card(ticker=ticker_arg, lang=bot_lang)
        elif cmd == "/doctor":
            t_arg = parts[1] if len(parts) >= 2 else "CELH"
            try:
                e_arg = float(parts[2]) if len(parts) >= 3 else 27.20
            except ValueError:
                e_arg = 27.20
            try:
                d_arg = int(parts[3]) if len(parts) >= 4 else 42
            except ValueError:
                d_arg = 42
            reply = self.build_doctor_alert(
                ticker=t_arg,
                entry_price=e_arg,
                days_held=d_arg,
                lang=bot_lang,
            )
        else:
            # If user typed a ticker symbol directly like "TSLA" or "$CELH"
            cand = cmd.lstrip("/$").upper()
            if quant_engine.get_stock(cand, is_pro=True) is not None:
                reply = self.build_stock_card(ticker=cand, lang=bot_lang)
            else:
                reply = self.build_test_message(lang=bot_lang)

        # If live bot token and chat_id are available, send the reply with US inline buttons
        target_chat = incoming_chat_id or self._resolve_chat_id()
        if self._resolve_token() and target_chat:
            self.send_message(
                text=reply,
                override_chat_id=target_chat,
                reply_markup=self.build_us_inline_keyboard(),
            )

        return reply


telegram_service = TelegramService()
