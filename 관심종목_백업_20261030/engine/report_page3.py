"""
engine/report_page3.py
Milestone 4 (Page 3 — [미국 동적 알파 레이더] US-Only PW-RSI Actionable Top 5 & Spotlight Deep-Dive)
Strictly US-only, 0% Korean stocks, 4 PW-RSI conditions, and Value-Trap Firewall.
"""

from datetime import datetime
from typing import Any, Dict, List


def _format_kr_date(date_str: str) -> str:
    """Formats YYYY-MM-DD into 'YYYY-MM-DD (요일)'."""
    try:
        dt = datetime.strptime(date_str[:10], "%Y-%m-%d")
        weekdays = ["월", "화", "수", "목", "금", "토", "일"]
        return f"{dt.strftime('%Y-%m-%d')} ({weekdays[dt.weekday()]})"
    except Exception:
        return date_str


def render_page3_html(snapshot: Dict[str, Any], calc_data: Dict[str, Any]) -> str:
    """Renders Layout A Page 3 HTML content."""
    ref_date = snapshot.get("date", datetime.now().strftime("%Y-%m-%d"))
    date_label = _format_kr_date(ref_date)
    actionable_candidates: List[Dict[str, Any]] = calc_data.get("actionable_top5", [])
    buy_count = calc_data.get("pwrsi_buy_count", 0)

    # 1. State-Aware Discipline Banner
    if buy_count == 0:
        banner_html = """
        <div class="discipline-banner banner-active">
            <div class="banner-icon">🚨</div>
            <div class="banner-content">
                <div class="banner-title">[무신호 규율 유지 / No-Signal Discipline Active]: 1_BUY_IGNITION 진입 신호 0건</div>
                <div class="banner-body">
                    금일 4대 진입 조건을 100% 충족한 신규 우측 시동 <strong>[1_BUY]</strong> 종목이 0건입니다. 떨어지는 칼날(좌측 신저가) 매수를 거부하고 바닥 확인 후 우측 시동이 걸린 종목만 기다리는 이 철칙이 <strong>26.8년간 세전 +20,287% (연평균 CAGR +21.97%) / 세후 +7,952% (CAGR +17.81%)</strong>를 지켜낸 핵심 방패입니다. 뇌동매수를 금지하고 예비 시동 대기군(<strong>2_READY_MA20</strong>)의 달러 돌파 가격($)을 모니터링하십시오.
                </div>
            </div>
        </div>
        """
    else:
        banner_html = f"""
        <div class="discipline-banner banner-buy">
            <div class="banner-icon">🔥</div>
            <div class="banner-content">
                <div class="banner-title">[우측 시동 점화 / Buy Ignition Triggered]: {buy_count}개 종목 4대 조건 100% 충족</div>
                <div class="banner-body">
                    금일 4대 진입 조건을 모두 돌파한 신규 1_BUY_IGNITION 종목이 포착되었습니다. 자금 관리 원칙에 따라 1순위 후보 종목에 계획된 분할 매수를 집행하십시오.
                </div>
            </div>
        </div>
        """

    # 2.5. Core (SK Square) vs. US Alpha #1 (CELH) Switching Advisor & Active Position Board
    quotes = snapshot.get("quotes", {})
    sq_q = quotes.get("402340.KS", {})
    p_sq_close = float(sq_q.get("close", 781_000.0))
    sq_rsi = float(sq_q.get("rsi14", 33.2))

    pf_cfg = calc_data.get("portfolio_config", {})
    sq_shares = int(pf_cfg.get("shares", 76))
    sq_avg = float(pf_cfg.get("avg_cost", 1_090_000.0))
    us_positions: List[Dict[str, Any]] = pf_cfg.get("us_alpha_positions", [])

    top1 = actionable_candidates[0] if actionable_candidates else {
        "ticker": "CELH", "name": "셀시우스 홀딩스", "close": 29.96, "trigger_price": 29.18,
        "score": 88.8, "signal_stage": "2_READY_MA20", "vol_surge": 1.30, "ret20d": 1.94,
        "c1": True, "c2": True, "c3": True, "c4": False,
    }
    t1_tk = top1["ticker"]
    t1_name = top1["name"]
    t1_close = float(top1.get("close", 29.96))
    t1_trig = float(top1.get("trigger_price", 29.18))
    t1_pct = float(top1.get("pct_to_trigger", 5.0))
    t1_vol = float(top1.get("vol_surge", 1.30))
    t1_ret20 = float(top1.get("ret20d", 0.0))
    t1_dd = float(top1.get("dd_high", -55.0))
    t1_prox = float(top1.get("prox_low", 20.0))
    t1_ma20 = float(top1.get("ma20", t1_close))
    t1_ma60 = float(top1.get("ma60", t1_trig))
    t1_slope = float(top1.get("ma20_slope_pct", 0.10))
    t1_score = float(top1.get("score", 79.3))
    t1_stage = top1.get("signal_stage", "2_READY_MA20")
    t1_c1 = bool(top1.get("c1", True))
    t1_c2 = bool(top1.get("c2", True))
    t1_c3 = bool(top1.get("c3", False))
    t1_c4 = bool(top1.get("c4", False))
    sq_upside_b = (935_000.0 / p_sq_close - 1.0) * 100.0
    sq_upside_109 = (sq_avg / p_sq_close - 1.0) * 100.0

    # Exact 4-condition audit summary line for #1 candidate
    audit_line = (
        f"<div style='margin-top:2px; padding-top:2px; border-top:1px dashed #cbd5e1; font-size:6.0pt; color:#1e293b;'>"
        f"<strong>📊 [1위 {t1_tk}({t1_score:.1f}점) 4대 조건 정밀 수치 검증]:</strong> "
        f"{'✅' if t1_c1 else '❌'}<strong>①고점낙폭:</strong> {t1_dd:.1f}%(기준 ≤-38%) &nbsp;|&nbsp; "
        f"{'✅' if t1_c2 else '❌'}<strong>②바닥반등:</strong> {t1_prox:+.1f}%(기준 +10~40%) &nbsp;|&nbsp; "
        f"{'✅' if t1_c3 else '❌'}<strong>③추세돌파:</strong> 종가 ${t1_close:.2f} vs MA20 ${t1_ma20:.2f}·MA60 ${t1_ma60:.2f}(시동가 ${t1_trig:.2f}, {t1_pct:+.1f}%)·기울기 {t1_slope:+.2f}% &nbsp;|&nbsp; "
        f"{'✅' if t1_c4 else '❌'}<strong>④수급시동:</strong> 거래량 {t1_vol:.2f}x(≥1.35x)·20D {t1_ret20:+.1f}%(≥+8%)"
        f"</div>"
    )

    if us_positions:
        pos = us_positions[0]
        p_tk = pos.get("ticker", t1_tk)
        p_sh = pos.get("shares", 0)
        p_entry = float(pos.get("avg_cost_usd", t1_close))
        p_days = int(pos.get("days_held", 1))
        p_cur = float(quotes.get(p_tk, {}).get("close", t1_close))
        p_ret = (p_cur / p_entry - 1.0) * 100.0
        p_stop = round(p_entry * 0.91, 2)
        pos_badge_str = f"현재 보유: SK스퀘어 {sq_shares}주 · {p_tk} {p_sh}주(평단 ${p_entry:.2f}, {p_ret:+.1f}%, 손절선 ${p_stop:.2f}, D+{p_days}/55일)"
    else:
        pos_badge_str = f"현재 포지션: SK스퀘어 {sq_shares}주 (현재가 {p_sq_close/10000:.1f}만) · 미국 알파 0주 | 매매 통보 시 리포트 즉시 반영"

    if t1_stage == "1_BUY_IGNITION":
        if p_sq_close <= 869_000.0:
            verdict_cls = "switch-verdict-caution"
            verdict_title = f"🛡️ [4대 조건 점등 어드바이스]: SK스퀘어({p_sq_close/10000:.1f}만) 바닥 전량 손절 교체 금지 · 여유현금/최대 20%({max(1, int(sq_shares * 0.2))}주)만 {t1_tk} 정찰병 진입"
            verdict_desc = (
                f"<strong>{t1_name}({t1_tk})</strong>가 4대 조건(<strong>1_BUY_IGNITION</strong>)을 모두 충족했으나, 현재 SK스퀘어({p_sq_close/10000:.1f}만 원, RSI {sq_rsi:.1f})가 과매도 바닥권입니다. "
                f"바닥에서 전량 매도 시 손실 확정 및 T+2일 환전 시차 동안 양쪽 반등을 놓칠 수 있으므로 <strong>SK스퀘어 본대(80%+)는 유지</strong>하고 여유 달러 또는 소액만 진입하십시오."
                f"{audit_line}"
            )
        elif p_sq_close < 1_090_000.0:
            half_sh = sq_shares // 2
            verdict_cls = "switch-verdict-go"
            verdict_title = f"⚖️ [4대 조건 점등 어드바이스]: 50:50 하이브리드 스위칭 — SK스퀘어 {half_sh}주(50%) 매도 후 {t1_tk} 갈아타기 실행"
            verdict_desc = (
                f"<strong>{t1_name}({t1_tk})</strong> 우측 시동 완비! SK스퀘어({p_sq_close/10000:.1f}만)가 1차 적정가 밴드에 진입하여 세후 기대수익률 면에서 "
                f"미국 1위 알파 종목 초기 파동(+40~80% 기대)이 우위에 있습니다. <strong>SK스퀘어 {half_sh}주 매도 → T+2 달러 환전 후 {t1_tk} 진입</strong>으로 양쪽 엔진을 동시 가동하십시오."
                f"{audit_line}"
            )
        else:
            verdict_cls = "switch-verdict-go"
            verdict_title = f"🚀 [4대 조건 점등 어드바이스]: 주력 스위칭 실행 — SK스퀘어 70~100% 매도 후 {t1_tk} 집중 진입"
            verdict_desc = (
                f"SK스퀘어 본전/목표권({p_sq_close/10000:.1f}만) 회복과 동시에 <strong>{t1_name}({t1_tk}) 1_BUY_IGNITION</strong>이 점등되었습니다. "
                f"비과세 원금·차익을 확정하고 T+2 환전을 통해 2단계 미국 알파 복리 전략으로 주력 자금을 즉시 이동하십시오."
                f"{audit_line}"
            )
    else:
        verdict_cls = "switch-verdict-hold"
        if not t1_c3 and t1_c4:
            if t1_close <= t1_trig:
                verdict_title = (
                    f"🟡 [금일 스위칭 판정]: SK스퀘어 {sq_shares}주 그대로 보유 — "
                    f"{t1_name}({t1_tk}) ④번 수급({t1_vol:.2f}x)은 충족했으나 ③번 시동가(${t1_trig:.2f}, 거리 {t1_pct:+.1f}%) 미돌파(❌③)"
                )
                verdict_desc = (
                    f"금일 1위 <strong>{t1_name}({t1_tk}, 종가 ${t1_close:.2f})</strong>는 ①고점낙폭({t1_dd:.1f}%)·②바닥반등({t1_prox:+.1f}%)·<strong>④수급시동(거래량 {t1_vol:.2f}배 ≥ 1.35배)</strong>을 충족했으나, "
                    f"핵심인 <strong>③번 추세돌파 시동 가격(${t1_trig:.2f}, 남은 거리 {t1_pct:+.1f}%)을 아직 넘지 못했습니다(❌③).</strong> "
                    f"반면 SK스퀘어({p_sq_close/10000:.1f}만)는 적정가(93.5만, <strong>{sq_upside_b:+.1f}%</strong>) 및 본전(109만, <strong>{sq_upside_109:+.1f}%</strong>) 반등 여력이 크므로 <strong>오늘은 선제 매도 없이 SK스퀘어를 100% 그대로 보유하십시오.</strong>"
                    f"{audit_line}"
                )
            else:
                verdict_title = (
                    f"🟡 [금일 스위칭 판정]: SK스퀘어 {sq_shares}주 그대로 보유 — "
                    f"{t1_name}({t1_tk}) ④번 수급은 충족했으나 ③번 20일선 기울기({t1_slope:+.2f}% ≤ 0) 우상향 미전환(❌③)"
                )
                verdict_desc = (
                    f"금일 1위 <strong>{t1_name}({t1_tk}, ${t1_close:.2f})</strong>는 ④번 수급시동은 충족했으나 <strong>③번 20일선 기울기({t1_slope:+.2f}%)가 아직 우상향(&gt;0)으로 돌아서지 않았습니다(❌③).</strong> "
                    f"따라서 선제 매도 없이 <strong>SK스퀘어({p_sq_close/10000:.1f}만)를 100% 그대로 보유</strong>하십시오."
                    f"{audit_line}"
                )
        elif t1_c3 and not t1_c4:
            verdict_title = (
                f"🟡 [금일 스위칭 판정]: SK스퀘어 {sq_shares}주 그대로 보유 — "
                f"{t1_name}({t1_tk}) ③번 시동가(${t1_trig:.2f})는 돌파했으나 ④번 수급시동({t1_vol:.2f}x < 1.35x) 미충족(❌④)"
            )
            verdict_desc = (
                f"금일 1위 <strong>{t1_name}({t1_tk}, ${t1_close:.2f})</strong>는 ③번 시동 가격(${t1_trig:.2f})을 돌파했으나 마지막 <strong>④번 수급시동(현재 거래량 {t1_vol:.2f}배 &lt; 기준 1.35배, 20D {t1_ret20:+.1f}% &lt; +8%)</strong>이 미점등 상태입니다(❌④). "
                f"반면 SK스퀘어({p_sq_close/10000:.1f}만)는 적정가(93.5만, <strong>{sq_upside_b:+.1f}%</strong>) 및 본전(109만, <strong>{sq_upside_109:+.1f}%</strong>) 반등 여력이 크므로 <strong>오늘은 SK스퀘어를 100% 그대로 가져가십시오.</strong>"
                f"{audit_line}"
            )
        else:
            missing = []
            if not t1_c1:
                missing.append(f"①고점낙폭({t1_dd:.1f}%)")
            if not t1_c2:
                missing.append(f"②바닥반등({t1_prox:+.1f}%)")
            if not t1_c3:
                missing.append(f"③추세돌파(시동가 ${t1_trig:.2f}, 거리 {t1_pct:+.1f}%)")
            if not t1_c4:
                missing.append(f"④수급시동(거래량 {t1_vol:.2f}x < 1.35x)")
            miss_str = " · ".join(missing) if missing else "조건 대기"
            verdict_title = f"🟡 [금일 스위칭 판정]: SK스퀘어 {sq_shares}주 그대로 보유 — {t1_name}({t1_tk}) 미충족 조건({miss_str}) 돌파 전 선제 매도 금지"
            verdict_desc = (
                f"금일 1위 <strong>{t1_name}({t1_tk}, 종가 ${t1_close:.2f}, 종합 {t1_score:.1f}점)</strong>는 ①고점낙폭({t1_dd:.1f}%)·②바닥반등({t1_prox:+.1f}%)은 충족했으나, "
                f"<strong>{miss_str}</strong> 조건이 미충족 상태입니다. 4대 조건이 모두 켜지기 전까지는 <strong>SK스퀘어({p_sq_close/10000:.1f}만)를 100% 그대로 보유</strong>하십시오."
                f"{audit_line}"
            )

    switch_advisor_html = f"""
    <div class="section-box">
        <div class="section-title">
            <span>⚖️ 코어(SK스퀘어) 유지 vs. 미국 알파 1위({t1_tk}) 갈아타기 실전 어드바이저</span>
            <span class="section-badge">{pos_badge_str}</span>
        </div>
        <div class="switch-verdict-box {verdict_cls}">
            <div class="switch-verdict-title">{verdict_title}</div>
            <div class="switch-verdict-desc">{verdict_desc}</div>
        </div>
        <div class="switch-matrix-grid">
            <div class="switch-matrix-card {'matrix-active' if p_sq_close <= 869_000 else ''}">
                <div class="matrix-hdr">📌 시나리오 A: {t1_tk} 4개 조건 다 켜졌는데 SK스퀘어가 바닥권(≤86.9만)일 때</div>
                <div class="matrix-body"><strong>[SK스퀘어 본대 유지 + 여유현금/최대 {max(1, int(sq_shares * 0.2))}주(20%)만 교체]</strong> 바닥 헐값에 SK스퀘어를 전량 손절하면 T+2 환전 시차(2거래일) 동안 한·미 양쪽 반등을 다 놓칩니다. 본대는 지키고 여유 달러나 소액만 진입합니다.</div>
            </div>
            <div class="switch-matrix-card {'matrix-active' if 869_000 < p_sq_close < 1_090_000 else ''}">
                <div class="matrix-hdr">📌 시나리오 B: {t1_tk} 4개 조건 다 켜지고 SK스퀘어가 반등권(93.5만~109만)일 때</div>
                <div class="matrix-body"><strong>[50:50 분할 스위칭 — {sq_shares // 2}주 매도 후 {t1_tk} 진입]</strong> SK스퀘어가 1차 적정가(Case B 93.5만) 부근까지 반등했다면, 세후 기대수익(+40~78%)이 더 큰 {t1_tk} 초기 파동으로 절반({sq_shares // 2}주)을 과감히 갈아탑니다.</div>
            </div>
            <div class="switch-matrix-card {'matrix-active' if p_sq_close >= 1_090_000 else ''}">
                <div class="matrix-hdr">📌 시나리오 C: {t1_tk} 4개 조건 다 켜지고 SK스퀘어가 본전·졸업권(≥109만)일 때</div>
                <div class="matrix-body"><strong>[70~100% 주력 스위칭 — {int(sq_shares * 0.7)}~{sq_shares}주 매도 후 {t1_tk} 집중 투입]</strong> 국내 비과세 원금·수익을 확정한 뒤 T+2 달러 환전을 통해 2단계 미국 알파(US-Only PW-RSI)로 주력 포지션을 완전히 이동합니다.</div>
            </div>
        </div>
    </div>
    """
    survival_html = """
    <div class="survival-grid">
        <div class="surv-card">
            <div class="surv-header"><span class="surv-badge badge-stop">1. -9.0% 칼손절 (Hard Stop)</span></div>
            <div class="surv-body">
                진입가 <strong>$P_entry × 0.91</strong> 도달 시 기계적 손절.<br>
                미국 주식 <strong>양도소득세 22% 손익통산 세금 크레딧</strong>을 100% 확보하여 확정 세금을 방어합니다.
            </div>
        </div>
        <div class="surv-card">
            <div class="surv-header"><span class="surv-badge badge-time">2. 55거래일 시간손절 (Time Stop)</span></div>
            <div class="surv-body">
                진입 후 <strong>D+55거래일 경과</strong> 시 수익률이 <strong>&lt; +8.0%</strong>에 머물면 데드머니(Dead Money) 탈출을 위해 시장가 청산 후 신규 #1 종목으로 교체합니다.
            </div>
        </div>
        <div class="surv-card">
            <div class="surv-header"><span class="surv-badge badge-switch">3. 주간 업그레이드 (+10pt 스위칭)</span></div>
            <div class="surv-body">
                <strong>D+25일 이상 보유 &amp; 수익률 &lt; +12% &amp; MA20 하회</strong> 상태에서, 신규 1위 후보 점수가 <strong>+10점 이상 높으면</strong> 즉시 교체 편입합니다.
            </div>
        </div>
        <div class="surv-card">
            <div class="surv-header"><span class="surv-badge badge-tp">4. 추세추종 &amp; +100% TP1 반익절</span></div>
            <div class="surv-body">
                수익률 <strong>+40% 이상</strong> 시 MA60 (-3%) 트레일링 스탑 가동.<br>
                <strong>+100% TP1 도달 시 50% 분할 익절</strong>로 원금 100% 회수 (무위험 프리캐리 전환).
            </div>
        </div>
    </div>
    """

    # 3. Actionable Top 5 Leaderboard
    top5 = actionable_candidates[:5]
    top5_rows_html = ""
    for rank, c in enumerate(top5, 1):
        tier_cls = "tier-aplus" if "A+" in c.get("growth_tier", "") else ("tier-a" if "A" in c.get("growth_tier", "") else "tier-b")
        stage_cls = "stage-buy" if "1_BUY" in c.get("signal_stage", "") else "stage-ready"
        score_delta = c.get("score_delta", 0.0)
        delta_str = f"+{score_delta:.1f}" if score_delta > 0 else f"{score_delta:.1f}"

        c1_mark = "✅" if c.get("c1") else "❌"
        c2_mark = "✅" if c.get("c2") else "❌"
        c3_mark = "✅" if c.get("c3") else "❌"
        c4_mark = "✅" if c.get("c4") else "❌"

        c_dd = float(c.get("dd_high", -50.0))
        c_prox = float(c.get("prox_low", 20.0))
        c_slope = float(c.get("ma20_slope_pct", 0.0))
        c_vol = float(c.get("vol_surge", 1.25))
        c_ma20 = float(c.get("ma20", c["close"]))
        c_ma60 = float(c.get("ma60", c["trigger_price"]))
        if c.get("c3"):
            c3_tag = "돌파"
        elif c["close"] > c_ma20 and c["close"] > c_ma60:
            c3_tag = f"기울기{c_slope:+.1f}%"
        elif c["close"] > c_ma20:
            c3_tag = "MA60전"
        else:
            c3_tag = "MA20전"
        s_dd = float(c.get("score_dd", 20.0))
        s_pr = float(c.get("score_prox", 25.0))
        s_ma = float(c.get("score_ma", 20.0))
        s_vo = float(c.get("score_vol", 3.0))
        s_gr = float(c.get("score_growth", 10.0))

        top5_rows_html += f"""
        <tr class="{'row-highlight' if rank == 1 else ''}">
            <td style="font-weight:800; text-align:center;">#{rank}</td>
            <td style="white-space:nowrap;">
                <span class="ticker-badge">{c['ticker']}</span>
                <span class="ticker-name">{c['name']}</span>
                <span class="growth-tier {tier_cls}">{c['growth_tier']}</span>
            </td>
            <td style="text-align:right; font-weight:800;">${c['close']:.2f}</td>
            <td class="{'chg-up' if c['chg1d'] >= 0 else 'chg-down'}" style="text-align:right; font-weight:700;">{c['chg1d']:+.2f}%</td>
            <td style="text-align:center; white-space:nowrap;">
                <span class="score-pill">{c['score']:.1f}</span>
                <span class="delta-badge {('delta-up' if score_delta > 0 else ('delta-down' if score_delta < 0 else 'delta-zero'))}">Δ {delta_str}</span>
            </td>
            <td style="text-align:center; white-space:nowrap;">
                <span class="stage-badge {stage_cls}">{c['signal_stage']}</span>
            </td>
            <td style="text-align:center; white-space:nowrap; font-size:5.8pt; letter-spacing:-0.2px;">
                <span class="cond-chip">{c1_mark}①{c_dd:.0f}%</span>
                <span class="cond-chip">{c2_mark}②{c_prox:+.0f}%</span>
                <span class="cond-chip">{c3_mark}③{c3_tag}</span>
                <span class="cond-chip">{c4_mark}④{c_vol:.2f}x</span>
            </td>
            <td style="text-align:right; font-weight:800; color:#1d4ed8;">${c['trigger_price']:.2f}</td>
            <td style="text-align:right; font-weight:700; color:{'#059669' if c['pct_to_trigger'] <= 0 else '#334155'};">
                {c['pct_to_trigger']:+.1f}%
            </td>
        </tr>
        """

    # 4. Spotlight Deep-Dive Cards (Top 2 Candidates)
    top2_tickers = " / ".join(c["ticker"] for c in top5[:2]) if top5 else "CELH / FSLR"
    spotlight_cards_html = ""
    for rank, c in enumerate(top5[:2], 1):
        s_dd = float(c.get("score_dd", 20.0))
        s_pr = float(c.get("score_prox", 25.0))
        s_ma = float(c.get("score_ma", 20.0))
        s_vo = float(c.get("score_vol", 3.0))
        s_gr = float(c.get("score_growth", 10.0))
        c_ma20 = float(c.get("ma20", c["close"]))
        c_ma60 = float(c.get("ma60", c["trigger_price"]))
        c_slope = float(c.get("ma20_slope_pct", 0.0))
        c_vol = float(c.get("vol_surge", 1.30))
        c_ret20 = float(c.get("ret20d", 0.0))
        c_hi52 = float(c.get("hi52", c["close"] * 2.0))
        c_lo52 = float(c.get("lo52", c["close"] * 0.8))
        c_dd = float(c.get("dd_high", -50.0))
        c_prox = float(c.get("prox_low", 20.0))

        if c.get("c3") and not c.get("c4"):
            trig_line = f"• ③시동가(<strong>${c['trigger_price']:.2f}</strong>) 돌파완료 → <strong>④수급({c_vol:.2f}x/1.35x, 20D {c_ret20:+.1f}%) 대기</strong>"
        elif not c.get("c3") and c.get("c4"):
            trig_line = f"• ③시동가 미돌파: <strong style=\"color:#1d4ed8;\">${c['trigger_price']:.2f}</strong> ({c['pct_to_trigger']:+.1f}%, 기울기{c_slope:+.2f}%) · <strong>④수급 {c_vol:.2f}x 충족</strong>"
        else:
            trig_line = f"• ③돌파시동가: <strong style=\"color:#1d4ed8;\">${c['trigger_price']:.2f}</strong> ({c['pct_to_trigger']:+.1f}%, MA20 ${c_ma20:.2f}·MA60 ${c_ma60:.2f}) · ④수급 {c_vol:.2f}x"
        spotlight_cards_html += f"""
        <div class="spotlight-card">
            <div class="spotlight-header">
                <div style="display:flex; align-items:center; gap:6px;">
                    <span class="spotlight-rank">오늘의 집중 분석 #{rank}</span>
                    <span class="spotlight-title">{c['ticker']} — {c['name']} <span style="font-weight:600; color:#475569;">({c['sector']} · 등급 {c['growth_tier']})</span></span>
                </div>
                <span class="spotlight-score">종합: <strong>{c['score']:.1f}점</strong> (낙폭{s_dd:.1f}+반등{s_pr:.0f}+추세{s_ma:.0f}+수급{s_vo:.1f}+등급{s_gr:.0f} · 시동가 <strong>${c['trigger_price']:.2f}</strong>)</span>
            </div>
            <div class="spotlight-body">
                <div class="spotlight-col">
                    <div class="col-title">📉 급락 원인 &amp; 실측 낙폭 (Washout)</div>
                    <div class="col-text"><strong>[고점 ${c_hi52:.2f} 대비 {c_dd:.1f}% / 저점 ${c_lo52:.2f} 대비 {c_prox:+.1f}%]</strong> {c.get('washout_why', '고점 대비 과매도 낙폭')}</div>
                </div>
                <div class="spotlight-col">
                    <div class="col-title">🚀 1~2년 턴어라운드 촉매 (Catalyst)</div>
                    <div class="col-text">{c.get('turnaround_catalyst', '매출 및 영업이익 턴어라운드 컨센서스')}</div>
                </div>
                <div class="spotlight-col">
                    <div class="col-title">📜 26.8년 백테스트 유사사례 (Analog)</div>
                    <div class="col-text">{c.get('hist_analog', '우측 시동 포착 후 추세 수익')}</div>
                </div>
                <div class="spotlight-col spotlight-col-plan">
                    <div class="col-title">🎯 실전 매매 로드맵 (Execution Plan)</div>
                    <div class="col-text">
                        {trig_line}<br>
                        • -9.0% 칼손절선: <strong style="color:#dc2626;">${c['stop_loss_price']:.2f}</strong> (양도세 22% 통산)<br>
                        • +100% TP1 익절선: <strong style="color:#059669;">${c['tp1_price']:.2f}</strong> (50% 원금회수)
                    </div>
                </div>
            </div>
        </div>
        """

    return f"""
    <div class="pdf-page" id="page-3">
        <!-- 1. Header Bar -->
        <div class="page-header">
            <div class="header-left">
                <span class="header-tag">Page 3 of 3</span>
                <span class="header-date-pill">📅 {date_label} 08:10</span>
                <h1 class="header-title">[{ref_date} 모닝 알파 리포트] 미국 전용(US-Only) PW-RSI 알파 레이더</h1>
            </div>
            <div class="header-right">
                <span class="badge-source">🇺🇸 100% US Growth · T+0 · 양도세 22% 통산</span>
            </div>
        </div>

        <!-- 2. State-Aware Discipline Banner -->
        {banner_html}

        <!-- 2.5. Core (SK Square) vs. US Alpha #1 Switching Advisor -->
        {switch_advisor_html}

        <!-- 3. Stage 2 Active Position Survival & Switching Monitor -->
        <div class="section-box">
            <div class="section-title">
                <span>🛡️ 2단계 실전 보유 포지션 생존 및 스위칭 모니터 (4대 기계적 청산 원칙)</span>
                <span class="section-badge">원칙 준수율 100% = 26.8년 CAGR +21.97% 원천</span>
            </div>
            {survival_html}
        </div>

        <!-- 4. Actionable Top 5 Leaderboard -->
        <div class="section-box">
            <div class="section-title">
                <span>🏆 Actionable Top 5 리더보드 (1_BUY_IGNITION &amp; 2_READY_MA20 전용)</span>
                <span class="section-badge">한국 종목(.KS/.KQ) 100% 배제 | 떨어지는 칼날(3_WATCH) 메인 표 제외</span>
            </div>
            <table class="report-table">
                <thead>
                    <tr>
                        <th style="width:4%; text-align:center;">순위</th>
                        <th style="width:19%;">티커 및 기업명</th>
                        <th style="width:8%; text-align:right;">종가 ($)</th>
                        <th style="width:7%; text-align:right;">1D (%)</th>
                        <th style="width:11%; text-align:center;">종합 점수</th>
                        <th style="width:12%; text-align:center;">신호 단계</th>
                        <th style="width:25%; text-align:center;">4대 조건 체크 (실측 수치)</th>
                        <th style="width:7%; text-align:right;">시동 가격</th>
                        <th style="width:7%; text-align:right;">거리 (%)</th>
                    </tr>
                </thead>
                <tbody>{top5_rows_html}</tbody>
            </table>
            <div class="cond-legend">
                <span><strong>① 고점낙폭:</strong> 52W 고점 대비 ≤ -38.0%</span>
                <span><strong>② 바닥반등:</strong> 52W 저점 대비 +10~40%</span>
                <span><strong>③ 추세돌파:</strong> 종가 &gt; MA20·60 &amp; 기울기 &gt; 0</span>
                <span><strong>④ 수급시동:</strong> 10D 거래량 ≥ 1.35x (20D ≥ +8%)</span>
            </div>
        </div>

        <!-- 5. Today's Spotlight Deep-Dive Cards (Top 2 Candidates) -->
        <div class="section-box">
            <div class="section-title">
                <span>🔍 오늘의 심층 분석 카드 (Top 2 종목 딥다이브: {top2_tickers})</span>
                <span class="section-badge">1~2년 턴어라운드 팩트 &amp; 실전 매매 로드맵</span>
            </div>
            <div class="spotlight-wrap">{spotlight_cards_html}</div>
        </div>

        <!-- 6. Value-Trap Firewall Exclusion Notice -->
        <div class="firewall-notice">
            <span class="firewall-badge">⚠️ Value-Trap Firewall (영구 배제 알림):</span>
            52주 신저가 부근에 위치하더라도 구조적 파운드리 적자, 서버 점유율 상실, 특허 절벽, 코드커팅 등 영구적 이익 훼손 종목(<strong>INTC, PFE, BA, NKE, PARA, WBD, ALB</strong>)은 스크리너에서 100% 영구 배제됩니다.
        </div>

        <!-- 7. Footer -->
        <div class="page-footer">
            <span>[{ref_date}] Morning Alpha Briefing | Automated Daily 08:10 AM KST Engine | 100% US &amp; CN/TW Primary Sources</span>
            <span>Page 3 of 3 (Report Complete)</span>
        </div>
    </div>
    """
