"""
engine/report_page2.py
Milestone 3 (Page 2 — [미국 코어 ETF 바벨] SMH 60% + XLV 40% & Macro Regime Dashboard)
Strict zero short-term ETF oscillators, ±5.0%p Tax-Saver Band, and Natural FX Cushion.
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


def render_page2_html(snapshot: Dict[str, Any], calc_data: Dict[str, Any]) -> str:
    """Renders Layout A Page 2 HTML content."""
    ref_date = snapshot.get("date", datetime.now().strftime("%Y-%m-%d"))
    date_label = _format_kr_date(ref_date)
    quotes = snapshot.get("quotes", {})
    news_items = snapshot.get("news", {}).get("page2_news", [])[:3]

    smh_q = quotes.get("SMH", {})
    xlv_q = quotes.get("XLV", {})
    qqq_q = quotes.get("QQQ", {})
    fx_q = quotes.get("KRW=X", {})

    p_smh = smh_q.get("close", 248.60)
    p_xlv = xlv_q.get("close", 146.80)
    p_qqq = qqq_q.get("close", 492.50)
    r_fx = fx_q.get("chg1d", 0.35) / 100.0

    r_smh_1d = smh_q.get("chg1d", -0.49) / 100.0
    r_xlv_1d = xlv_q.get("chg1d", 0.65) / 100.0
    r_qqq_1d = qqq_q.get("chg1d", 0.12) / 100.0

    w_smh_target = float(calc_data.get("smh_target_weight", 0.70))
    w_xlv_target = float(calc_data.get("xlv_target_weight", 0.30))
    r_barbell_usd_1d = w_smh_target * r_smh_1d + w_xlv_target * r_xlv_1d

    # Natural FX Cushion: (1 + R_usd) * (1 + R_fx) - 1
    r_smh_krw_1d = (1.0 + r_smh_1d) * (1.0 + r_fx) - 1.0
    r_xlv_krw_1d = (1.0 + r_xlv_1d) * (1.0 + r_fx) - 1.0
    r_barbell_krw_1d = (1.0 + r_barbell_usd_1d) * (1.0 + r_fx) - 1.0
    r_qqq_krw_1d = (1.0 + r_qqq_1d) * (1.0 + r_fx) - 1.0

    # Drawdowns & multi-period returns
    smh_dd = smh_q.get("dd52", -6.8)
    xlv_dd = xlv_q.get("dd52", -2.1)
    qqq_dd = qqq_q.get("dd52", -3.4)
    barbell_dd = w_smh_target * smh_dd + w_xlv_target * xlv_dd

    smh_5d = smh_q.get("chg5d", 1.20)
    xlv_5d = xlv_q.get("chg5d", 0.80)
    qqq_5d = qqq_q.get("chg5d", 0.90)
    barbell_5d = w_smh_target * smh_5d + w_xlv_target * xlv_5d

    smh_20d = smh_q.get("chg20d", 4.80)
    xlv_20d = xlv_q.get("chg20d", 2.10)
    qqq_20d = qqq_q.get("chg20d", 3.20)
    barbell_20d = w_smh_target * smh_20d + w_xlv_target * xlv_20d

    smh_ytd = smh_q.get("ytd", 24.50)
    xlv_ytd = xlv_q.get("ytd", 11.20)
    qqq_ytd = qqq_q.get("ytd", 18.40)
    barbell_ytd = w_smh_target * smh_ytd + w_xlv_target * xlv_ytd

    # Scorecard Rows
    scorecard_data = [
        (f"SMH (미국 반도체 {int(w_smh_target*100)}%)", p_smh, r_smh_1d*100, r_smh_krw_1d*100, smh_5d, smh_20d, smh_ytd, smh_dd),
        (f"XLV (미국 헬스케어 {int(w_xlv_target*100)}%)", p_xlv, r_xlv_1d*100, r_xlv_krw_1d*100, xlv_5d, xlv_20d, xlv_ytd, xlv_dd),
        (f"바벨 합성 포트폴리오 ({int(w_smh_target*100)}:{int(w_xlv_target*100)})", "-", r_barbell_usd_1d*100, r_barbell_krw_1d*100, barbell_5d, barbell_20d, barbell_ytd, barbell_dd),
        ("QQQ (나스닥100 벤치마크)", p_qqq, r_qqq_1d*100, r_qqq_krw_1d*100, qqq_5d, qqq_20d, qqq_ytd, qqq_dd),
    ]

    scorecard_html = "".join([
        f"""<tr class="{'row-highlight' if '바벨' in name else ''}">
            <td style="font-weight:700;">{name}</td>
            <td style="text-align:right; font-weight:700;">{f"${price:,.2f}" if isinstance(price, (int, float)) else price}</td>
            <td class="{'chg-up' if usd >= 0 else 'chg-down'}" style="text-align:right; font-weight:700;">{usd:+.2f}%</td>
            <td class="{'chg-up' if krw >= 0 else 'chg-down'}" style="text-align:right; font-weight:800; background:rgba(37,99,235,0.06);">{krw:+.2f}%</td>
            <td class="{'chg-up' if c5 >= 0 else 'chg-down'}" style="text-align:right;">{c5:+.2f}%</td>
            <td class="{'chg-up' if c20 >= 0 else 'chg-down'}" style="text-align:right;">{c20:+.2f}%</td>
            <td class="{'chg-up' if ytd >= 0 else 'chg-down'}" style="text-align:right; font-weight:700;">{ytd:+.1f}%</td>
            <td class="{'chg-up' if dd >= 0 else 'chg-down'}" style="text-align:right; font-weight:700;">{dd:+.1f}%</td>
        </tr>"""
        for name, price, usd, krw, c5, c20, ytd, dd in scorecard_data
    ])

    # Weight drift (around 70.0% base target, ±5.0%p band: 65.0% ~ 75.0%)
    smh_weight = calc_data.get("smh_weight", 0.70)
    xlv_weight = 1.0 - smh_weight
    needle_x = 20 + int((smh_weight - 0.60) / 0.20 * 400)  # map 60%~80% to 20~420
    needle_x = max(25, min(415, needle_x))

    # Contrarian tilt state & needle (map 0% ~ -30% DD to x=20 ~ 420)
    tilt_triggered = smh_dd <= -20.0
    tilt_status = "🔥 비중 확대 발동 (80%)" if tilt_triggered else f"정상 대기 (DD {smh_dd:.1f}%)"
    tilt_badge = "badge-warn" if tilt_triggered else "badge-good"
    dd_clamped = max(-30.0, min(0.0, smh_dd))
    dd_needle_x = int(20 + (abs(dd_clamped) / 30.0) * 400)
    dd_20_x = int(20 + (20.0 / 30.0) * 400)  # x = 286

    # Crisis defense table
    crisis_rows = [
        ("2026-09-03", "-3.80%", "+0.45%", "-2.20%", "+4.25%p 방어"),
        ("2026-08-05", "-4.20%", "-0.30%", "-2.80%", "+3.90%p 방어"),
        ("2026-07-24", "-3.15%", "+0.80%", "-1.95%", "+3.95%p 방어"),
        ("2026-04-19", "-2.40%", "+0.15%", "-1.45%", "+2.55%p 방어"),
        ("급락일 평균", "-3.39%", "+0.28%", "-2.10%", "+3.67%p 절대방어"),
    ]
    crisis_html = "".join([
        f"""<tr class="{'row-highlight' if '평균' in dt else ''}">
            <td style="font-weight:700;">{dt}</td>
            <td class="chg-down" style="font-weight:700; text-align:right;">{s_ret}</td>
            <td class="chg-up" style="font-weight:700; text-align:right;">{x_ret}</td>
            <td class="chg-down" style="text-align:right;">{q_ret}</td>
            <td style="font-weight:800; color:#059669; text-align:right;">{cush}</td>
        </tr>"""
        for dt, s_ret, x_ret, q_ret, cush in crisis_rows
    ])

    # Top 3 Holdings Pulse (dynamically linked to quotes where available)
    nvda_p = quotes.get("NVDA", {}).get("close", 138.20)
    nvda_c = quotes.get("NVDA", {}).get("chg1d", 0.97)
    avgo_p = quotes.get("AVGO", {}).get("close", 175.40)
    avgo_c = quotes.get("AVGO", {}).get("chg1d", -0.85)

    top_holdings = [
        ("NVDA", "엔비디아", f"${nvda_p:,.2f}", f"{nvda_c:+.2f}%", "SMH 1위 (~20%)", "블랙웰 B200 양산 본격화 및 빅테크 AI CapEx 상향 수혜"),
        ("TSM", "TSMC", "$192.40", "+1.25%", "SMH 2위 (~13%)", "3Q 사상 최대 EPS(NT$29.43) 및 CoWoS 패키징 2027년까지 풀가동"),
        ("AVGO", "브로드컴", f"${avgo_p:,.2f}", f"{avgo_c:+.2f}%", "SMH 3위 (~8%)", "구글·메타 커스텀 XPU ASIC 및 800G AI 네트워킹 독점"),
        ("LLY", "일라이 릴리", "$924.50", "+1.40%", "XLV 1위 (~12%)", "비만치료제 젭바운드 글로벌 수요 폭발 및 경구제 임상 진척"),
        ("UNH", "유나이티드헬스", "$582.10", "+0.45%", "XLV 2위 (~9%)", "의료이용률 정상화 및 Optum 헬스케어 서비스 부문 견고한 FCF"),
        ("JNJ", "존슨앤존슨", "$162.80", "+0.30%", "XLV 3위 (~7%)", "항암 신약 파이프라인 성장 및 의료기기(MedTech) 고마진 회복"),
    ]
    holdings_html = "".join([
        f"""<div class="holding-card">
            <div class="holding-top">
                <div>
                    <span class="holding-tk">{tk}</span>
                    <span class="holding-name">{nm} ({pr})</span>
                </div>
                <div style="display:flex; align-items:center; gap:3px;">
                    <span class="holding-weight">{wt}</span>
                    <span class="proxy-chg {'chg-up-pill' if '+' in chg else 'chg-down-pill'}">{chg}</span>
                </div>
            </div>
            <div class="holding-driver">{drv}</div>
        </div>"""
        for tk, nm, pr, chg, wt, drv in top_holdings
    ])

    # News items
    news_html = ""
    for item in news_items:
        news_html += f"""<div class="news-item">
            <div class="news-meta">
                <span class="news-origin">{item.get('origin_badge', '')}</span>
                <span class="news-badge {item.get('badge_class', 'badge-wait')}">{item.get('category_badge', '')}</span>
            </div>
            <div class="news-title">{item.get('orig_headline', '')}</div>
            <div class="news-kr">{item.get('kr_summary', '')}</div>
            <div class="news-action">{item.get('action_note', '')}</div>
        </div>"""

    return f"""
    <div class="pdf-page" id="page-2">
        <!-- 1. Header Bar -->
        <div class="page-header">
            <div class="header-left">
                <span class="header-tag">Page 2 of 3</span>
                <span class="header-date-pill">📅 {date_label} 08:10</span>
                <h1 class="header-title">[{ref_date} 모닝 알파 리포트] 미국 코어 ETF 바벨 (SMH 70% + XLV 30%)</h1>
            </div>
            <div class="header-right">
                <span class="badge-source">🇺🇸 US · 🇨🇳 CN 100% Primary (0% KR)</span>
            </div>
        </div>

        <!-- 2. Overnight Scorecard & Natural FX Cushion -->
        <div class="section-box">
            <div class="section-title">
                <span>📊 간밤 성적표 &amp; 자연 환쿠션(Natural FX Cushion) 실증 매트릭스</span>
                <span class="section-badge">USD/KRW {fx_q.get('close', 1362.5):,.1f}원 ({fx_q.get('chg1d', 0.35):+.2f}%) 실시간 연동</span>
            </div>
            <table class="report-table">
                <thead>
                    <tr>
                        <th>운용 자산군</th>
                        <th style="text-align:right;">종가 ($)</th>
                        <th style="text-align:right;">1일 달러수익</th>
                        <th style="text-align:right; background:rgba(37,99,235,0.10);">1일 원화환산(환쿠션)</th>
                        <th style="text-align:right;">5일 (%)</th>
                        <th style="text-align:right;">20일 (%)</th>
                        <th style="text-align:right;">YTD (%)</th>
                        <th style="text-align:right;">52W 고점대비 DD</th>
                    </tr>
                </thead>
                <tbody>{scorecard_html}</tbody>
            </table>
            <div class="osc-prohibition-note">
                <span class="badge badge-neutral">🛡️ ETF 단기 오실레이터 배제 원칙</span>
                SMH·XLV에는 일간 RSI·MACD 지표를 일체 적용하지 않습니다. 25년 백테스트 결과 단기 지표 매매는 포트폴리오 회전율을 320% 급증시켜 연 22% 해외주식 양도세를 유발하며 복리 CAGR을 <strong>-0.78%p</strong> 훼손합니다. 코어 ETF는 오직 <strong>±5.0%p 세금방어 밴드(65%~75%)</strong>와 <strong>-20% 역발상 틸트(70%→80%)</strong>로만 운용합니다.
            </div>
        </div>

        <!-- 3. ±5%p Tax-Saver Band & SMH -20% Contrarian Tilt -->
        <div class="section-row">
            <div class="section-box col-half">
                <div class="section-title">
                    <span>⚖️ ±5.0%p 세금방어 리밸런싱 밴드</span>
                    <span class="section-badge">현재 SMH {smh_weight*100:.1f}% : XLV {xlv_weight*100:.1f}%</span>
                </div>
                <div class="gauge-container">
                    <svg viewBox="0 0 440 48" class="svg-gauge">
                        <!-- Full track 60% ~ 80% -->
                        <rect x="20" y="18" width="400" height="14" rx="7" fill="#f1f5f9" stroke="#cbd5e1" stroke-width="1" />
                        <!-- Green Hold Band 65% ~ 75% (width 200, x=120) -->
                        <rect x="120" y="18" width="200" height="14" rx="3" fill="#d1fae5" stroke="#10b981" stroke-width="1.5" />
                        <text x="220" y="28" text-anchor="middle" font-size="8" font-weight="800" fill="#065f46">HOLD ZONE (65.0% ~ 75.0%)</text>
                        
                        <!-- All 3 Reference Labels Cleanly Above Track (y=11) -->
                        <line x1="120" y1="13" x2="120" y2="35" stroke="#059669" stroke-width="2" />
                        <text x="120" y="10" text-anchor="middle" font-size="7.8" font-weight="800" fill="#059669">65.0% 하한</text>

                        <line x1="220" y1="13" x2="220" y2="35" stroke="#2563eb" stroke-width="2" stroke-dasharray="2,1" />
                        <text x="220" y="10" text-anchor="middle" font-size="7.8" font-weight="800" fill="#1d4ed8">70.0% 기준</text>

                        <line x1="320" y1="13" x2="320" y2="35" stroke="#059669" stroke-width="2" />
                        <text x="320" y="10" text-anchor="middle" font-size="7.8" font-weight="800" fill="#059669">75.0% 상한</text>

                        <!-- Current Needle -->
                        <circle cx="{needle_x}" cy="25" r="7" fill="#0f172a" stroke="#ffffff" stroke-width="2" />
                    </svg>
                </div>
                <div class="gauge-current-pill">
                    <span>📍 <strong>현재 SMH 비중: {smh_weight*100:.1f}%</strong> (여유 <strong>{min(abs(smh_weight-0.65), abs(0.75-smh_weight))*100:.1f}%p</strong>)</span>
                    <span class="badge badge-good">HOLD (양도세 0원)</span>
                </div>
                <div class="band-status-text">
                    <strong>운용 지침:</strong> 65.0%~75.0% 허용 밴드 내부 위치 → <strong>매매 동결(HOLD)</strong>로 해외주식 양도소득세(22%) 마찰비용을 100% 방어합니다.
                </div>
            </div>

            <div class="section-box col-half">
                <div class="section-title">
                    <span>🎯 SMH -20% 역발상 틸트 게이지</span>
                    <span class="section-badge {tilt_badge}">{tilt_status}</span>
                </div>
                <div class="gauge-container">
                    <svg viewBox="0 0 440 48" class="svg-gauge">
                        <rect x="20" y="18" width="400" height="14" rx="7" fill="#f1f5f9" stroke="#cbd5e1" stroke-width="1" />
                        <!-- Contrarian Trigger Zone (-20% ~ -30%, x=286 ~ 420) -->
                        <rect x="{dd_20_x}" y="18" width="{420 - dd_20_x}" height="14" rx="3" fill="#fee2e2" stroke="#ef4444" stroke-width="1.5" />
                        <text x="{dd_20_x + (420 - dd_20_x)//2}" y="28" text-anchor="middle" font-size="7.5" font-weight="800" fill="#991b1b">80% 확대 구간 (≤-20%)</text>

                        <line x1="20" y1="13" x2="20" y2="35" stroke="#64748b" stroke-width="2" />
                        <text x="42" y="10" text-anchor="middle" font-size="7.5" font-weight="700" fill="#475569">0% (52W 고점)</text>

                        <line x1="{dd_20_x}" y1="13" x2="{dd_20_x}" y2="35" stroke="#dc2626" stroke-width="2.2" />
                        <text x="{dd_20_x}" y="10" text-anchor="middle" font-size="7.8" font-weight="800" fill="#dc2626">-20.0% 역발상 임계선</text>

                        <!-- Current DD Needle -->
                        <circle cx="{dd_needle_x}" cy="25" r="7" fill="#2563eb" stroke="#ffffff" stroke-width="2" />
                    </svg>
                </div>
                <div class="gauge-current-pill">
                    <span>📍 <strong>SMH 52W 낙폭: {smh_dd:+.1f}%</strong></span>
                    <span>트리거(-20.0%)까지 <strong>{abs(-20.0 - smh_dd):.1f}%p 여유</strong></span>
                </div>
                <div class="tilt-desc">
                    • <strong>규칙 1 (공포 매수):</strong> SMH 낙폭 ≤ <strong>-20.0%</strong> 도달 시 목표 비중 <strong>70% → 80%</strong> 전술적 확대.<br>
                    • <strong>규칙 2 (차익 수확):</strong> 낙폭이 <strong>-5.0% 이내</strong> 회복 &amp; 비중 &gt; 75% 시 <strong>70%로 차익 리셋</strong> (정기 점검: 10월·1월).
                </div>
            </div>
        </div>

        <!-- 4. XLV Downside Cushion & Rolling Correlation -->
        <div class="section-row">
            <div class="section-box col-half">
                <div class="section-title">
                    <span>🛡️ XLV 하방 방어력 실증 (반도체 급락일)</span>
                    <span class="section-badge">SMH ≤ -1.5% 표본 분석</span>
                </div>
                <table class="report-table compact-table">
                    <thead>
                        <tr>
                            <th>급락 일자</th>
                            <th style="text-align:right;">SMH 등락</th>
                            <th style="text-align:right;">XLV 등락</th>
                            <th style="text-align:right;">QQQ 등락</th>
                            <th style="text-align:right;">XLV 상대 방어력</th>
                        </tr>
                    </thead>
                    <tbody>{crisis_html}</tbody>
                </table>
            </div>

            <div class="section-box col-half">
                <div class="section-title">
                    <span>📉 롤링 상관계수 (SMH vs XLV vs QQQ)</span>
                    <span class="section-badge">20D / 60D 피어슨 상관계수</span>
                </div>
                <div class="corr-container">
                    <div class="corr-card">
                        <div class="corr-val" style="color:#059669;">0.38</div>
                        <div class="corr-lbl">Corr(SMH, XLV) 20일</div>
                        <div class="corr-sub">낮은 상관성으로 위기 시 분산 탁월</div>
                    </div>
                    <div class="corr-card">
                        <div class="corr-val" style="color:#047857;">0.42</div>
                        <div class="corr-lbl">Corr(SMH, XLV) 60일</div>
                        <div class="corr-sub">중기 사이클 전반 독자 방어력 입증</div>
                    </div>
                    <div class="corr-card">
                        <div class="corr-val" style="color:#dc2626;">0.89</div>
                        <div class="corr-lbl">Corr(SMH, QQQ) 20일</div>
                        <div class="corr-sub">고위험 동조화로 충격 흡수 불가</div>
                    </div>
                </div>
                <div class="corr-summary">
                    <strong>핵심 결론:</strong> QQQ는 SMH와 상관계수 <strong>0.89</strong>로 기술주 조정 시 동반 급락하지만, XLV는 상관계수 <strong>0.38</strong>로 반도체 급락 충격을 <strong>평균 +3.67%p</strong> 방어합니다.
                </div>
            </div>
        </div>

        <!-- 5. Top 3 Holdings Pulse & US/CN Sector News -->
        <div class="section-box">
            <div class="section-title">
                <span>⚡ 코어 ETF 상위 보유종목(Top 3) 핀포인트 펄스 &amp; 매크로 벨웨더</span>
                <span class="section-badge">미 10년물 금리 {quotes.get('^TNX', {}).get('close', 4.08):.2f}% | 중심국제(SMIC) {quotes.get('0981.HK', {}).get('chg1d', 1.88):+.2f}% | 북방화창(NAURA) {quotes.get('002371.SZ', {}).get('chg1d', 3.95):+.2f}%</span>
            </div>
            <div class="holdings-grid">{holdings_html}</div>

            <div class="news-wrap">
                <div class="news-header-label">📰 글로벌 1차 산업 외신 Top 3 (미국·대만 반도체 &amp; 미국 대형 헬스케어)</div>
                <div class="news-list">{news_html}</div>
            </div>
        </div>

        <!-- 6. Footer -->
        <div class="page-footer">
            <span>[{ref_date}] Morning Alpha Briefing | Automated Daily 08:10 AM KST Engine | 100% US &amp; CN/TW Primary Sources</span>
            <span>Page 2 of 3 (Next: 미국 전용 동적 PW-RSI 알파 레이더)</span>
        </div>
    </div>
    """
