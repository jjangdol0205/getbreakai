import os
import sys
import json
import ssl
import datetime
import urllib.request
import numpy as np
import pandas as pd

sys.stdout.reconfigure(encoding='utf-8')

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, 'data')
DASHBOARD_PATH = os.path.join(BASE_DIR, 'smh_xlv_fear_greed_dashboard.html')
HISTORY_CSV_PATH = os.path.join(BASE_DIR, 'smh_xlv_fear_greed_history.csv')


def update_csv_from_yahoo(ticker, csv_name=None, range_str='2mo'):
    """Fetch recent daily data from Yahoo Finance v8 API (with SSL bypass) and update local CSV."""
    if csv_name is None:
        csv_name = f"{ticker}.csv"
    csv_path = os.path.join(DATA_DIR, csv_name)
    if not os.path.exists(csv_path):
        return
    df_old = pd.read_csv(csv_path)
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    url = f"https://query1.finance.yahoo.com/v8/finance/chart/{ticker}?range={range_str}&interval=1d"
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        raw = urllib.request.urlopen(req, context=ctx, timeout=10).read().decode('utf-8')
        res = json.loads(raw)['chart']['result'][0]
        timestamps = res['timestamp']
        quote = res['indicators']['quote'][0]
        adj = res['indicators'].get('adjclose', [{}])[0].get('adjclose', quote['close'])
        rows = []
        for i, ts in enumerate(timestamps):
            dt_str = datetime.datetime.fromtimestamp(ts, datetime.timezone.utc).strftime('%Y-%m-%d')
            c = quote['close'][i]
            if c is None:
                continue
            o = quote['open'][i] if quote['open'][i] is not None else c
            h = quote['high'][i] if quote['high'][i] is not None else c
            l = quote['low'][i] if quote['low'][i] is not None else c
            v = quote['volume'][i] if quote['volume'][i] is not None else 0
            ac = adj[i] if (adj and adj[i] is not None) else c
            rows.append({
                'Date': dt_str,
                'Open': o,
                'High': h,
                'Low': l,
                'Close': c,
                'AdjClose': ac,
                'Volume': v
            })
        df_new = pd.DataFrame(rows)
        cols = [c for c in df_old.columns if c in df_new.columns]
        df_combined = pd.concat([df_old[cols], df_new[cols]], ignore_index=True)
        df_combined.drop_duplicates(subset=['Date'], keep='last', inplace=True)
        df_combined.sort_values('Date', inplace=True)
        df_combined.to_csv(csv_path, index=False)
    except Exception as e:
        print(f"[Warning] Live update skipped for {ticker}: {e}")


def rolling_percentile_score(series, window=756, min_periods=126, invert=False):
    """
    Convert a raw indicator series into a 0~100 score using empirical rolling percentile
    over a 3-year (756 trading days) lookback window, blended with a bounded sigmoid z-score
    for smooth behavior at extremes.
    """
    vals = series.values.astype(float)
    n = len(vals)
    scores = np.full(n, 50.0)
    for i in range(n):
        if np.isnan(vals[i]):
            continue
        start = max(0, i - window + 1)
        win = vals[start:i+1]
        win = win[~np.isnan(win)]
        if len(win) < min_periods:
            if len(win) < 10:
                continue
        pct = np.mean(win <= vals[i]) * 100.0
        std = np.std(win)
        if std > 1e-12:
            z = (vals[i] - np.mean(win)) / std
            z_score = 100.0 / (1.0 + np.exp(-0.9 * z))
        else:
            z_score = pct
        sc = 0.65 * pct + 0.35 * z_score
        if invert:
            sc = 100.0 - sc
        scores[i] = np.clip(sc, 0.0, 100.0)
    return pd.Series(scores, index=series.index)


def compute_rsi(series, period=14):
    delta = series.diff()
    gain = delta.clip(lower=0.0)
    loss = -delta.clip(upper=0.0)
    avg_gain = gain.ewm(alpha=1.0/period, min_periods=period, adjust=False).mean()
    avg_loss = loss.ewm(alpha=1.0/period, min_periods=period, adjust=False).mean()
    rs = avg_gain / avg_loss.replace(0, np.nan)
    rsi = 100.0 - (100.0 / (1.0 + rs))
    return rsi.fillna(50.0)


def classify_zone(score):
    if score < 25.0:
        return (
            "EXTREME FEAR (극단적 공포)",
            "Extreme Fear",
            "#ef4444",
            "🚨 [8:2 역발상 매집 발동 구간] XLV 방어주 일부 매도 ➔ 폭락한 SMH 저가 매수 스위칭!"
        )
    elif score < 45.0:
        return (
            "FEAR (공포)",
            "Fear",
            "#f97316",
            "🟠 [저가 매집 대기 / 7:3 유지] 반도체 조정 진행 중 — SMH 고점 대비 -20% 도달 시 8:2 전환"
        )
    elif score <= 55.0:
        return (
            "NEUTRAL (중립)",
            "Neutral",
            "#eab308",
            "⚪ [평시 7:3 균형 유지] SMH 70% : XLV 30% 기본 황금 비중 유지 및 적립식 거치"
        )
    elif score < 75.0:
        return (
            "GREED (탐욕)",
            "Greed",
            "#22c55e",
            "🟢 [상승장 순항 / 7:3 유지] 반도체 강세 구간 — 정기 리밸런싱 시 초과수익 XLV 이체 대기"
        )
    else:
        return (
            "EXTREME GREED (극단적 탐욕)",
            "Extreme Greed",
            "#10b981",
            "🔥 [고점 과열 / 7:3 차익 잠금] SMH 추격매수 금지! 비대해진 SMH를 70%로 깎아 XLV 금고에 수익 잠금!"
        )


def build_fear_greed_index(do_live_update=True):
    if do_live_update:
        for sym, fname in [
            ('SMH', 'SMH.csv'),
            ('XLV', 'XLV.csv'),
            ('QQQ', 'QQQ.csv'),
            ('SPY', 'SPY.csv'),
            ('KRW=X', 'USDKRW.csv')
        ]:
            update_csv_from_yahoo(sym, fname, range_str='1mo')

    df_smh = pd.read_csv(os.path.join(DATA_DIR, 'SMH.csv'), parse_dates=['Date'], index_col='Date')
    df_xlv = pd.read_csv(os.path.join(DATA_DIR, 'XLV.csv'), parse_dates=['Date'], index_col='Date')
    df_qqq = pd.read_csv(os.path.join(DATA_DIR, 'QQQ.csv'), parse_dates=['Date'], index_col='Date')
    df_fx = pd.read_csv(os.path.join(DATA_DIR, 'USDKRW.csv'), parse_dates=['Date'], index_col='Date')

    common = df_smh.index.intersection(df_xlv.index).intersection(df_qqq.index).sort_values()
    smh = df_smh.loc[common, 'AdjClose'].astype(float)
    smh_close = df_smh.loc[common, 'Close'].astype(float)
    xlv = df_xlv.loc[common, 'AdjClose'].astype(float)
    xlv_close = df_xlv.loc[common, 'Close'].astype(float)
    qqq = df_qqq.loc[common, 'AdjClose'].astype(float)
    fx = df_fx['Close'].reindex(common).ffill().bfill().astype(float)

    r_smh = smh.pct_change().fillna(0.0)
    r_xlv = xlv.pct_change().fillna(0.0)
    r_qqq = qqq.pct_change().fillna(0.0)
    r_port73 = 0.70 * r_smh + 0.30 * r_xlv
    port73_cum = (1.0 + r_port73).cumprod()

    # 1. [Momentum - 20%] SMH vs 125-Day Moving Average
    ma125_smh = smh_close.rolling(125, min_periods=20).mean()
    raw_mom = (smh_close / ma125_smh - 1.0) * 100.0
    sc_mom = rolling_percentile_score(raw_mom, window=756, invert=False)

    # 2. [Peak Drawdown - 20%] SMH 52-Week (252-Day) Drawdown (Direct link to -20% -> 8:2 rule!)
    peak252_smh = smh_close.rolling(252, min_periods=20).max()
    raw_dd = (smh_close / peak252_smh - 1.0) * 100.0
    sc_dd_calibrated = np.interp(
        raw_dd.values,
        [-45.0, -30.0, -20.0, -10.0, -5.0, -2.0, 0.0],
        [  0.0,   8.0,  20.0,  48.0, 68.0, 82.0, 95.0]
    )
    sc_dd_pct = rolling_percentile_score(raw_dd, window=756, invert=False)
    sc_dd = pd.Series(0.65 * sc_dd_calibrated + 0.35 * sc_dd_pct.values, index=common)

    # 3. [Safe-Haven Demand - 15%] 20-Day Return Spread (SMH 20d return - XLV 20d return)
    ret20_smh = smh.pct_change(20).fillna(0.0) * 100.0
    ret20_xlv = xlv.pct_change(20).fillna(0.0) * 100.0
    raw_safehaven = ret20_smh - ret20_xlv
    sc_safehaven = rolling_percentile_score(raw_safehaven, window=756, invert=False)

    # 4. [Relative Strength (RSI) - 15%] Blended 14-Day RSI (70% SMH RSI + 30% Port73 RSI)
    rsi_smh = compute_rsi(smh_close, 14)
    rsi_port = compute_rsi(port73_cum, 14)
    raw_rsi = 0.70 * rsi_smh + 0.30 * rsi_port
    sc_rsi_cal = np.clip((raw_rsi - 25.0) / (75.0 - 25.0) * 100.0, 0.0, 100.0)
    sc_rsi_pct = rolling_percentile_score(raw_rsi, window=756, invert=False)
    sc_rsi = 0.55 * sc_rsi_cal + 0.45 * sc_rsi_pct

    # 5. [Volatility Spike - 10%] SMH 20-Day Realized Volatility vs 50-Day Avg (Inverted: High Vol = Fear)
    vol20_smh = r_smh.rolling(20, min_periods=10).std() * np.sqrt(252) * 100.0
    vol_ma50 = vol20_smh.rolling(50, min_periods=15).mean()
    raw_vol_ratio = (vol20_smh / vol_ma50.replace(0, np.nan) - 1.0).fillna(0.0) * 100.0
    sc_vol = 0.50 * rolling_percentile_score(vol20_smh, window=756, invert=True) + \
             0.50 * rolling_percentile_score(raw_vol_ratio, window=756, invert=True)

    # 6. [Sector Leadership - 10%] SMH vs QQQ 60-Day Relative Alpha
    rel_smh_qqq = (smh / qqq).pct_change(60).fillna(0.0) * 100.0
    sc_lead = rolling_percentile_score(rel_smh_qqq, window=756, invert=False)

    # 7. [Portfolio Weight Drift - 10%] Natural SMH Weight Drift over Rolling 126-Day (6-Month) Window
    growth126_smh = (1.0 + r_smh).rolling(126, min_periods=20).apply(np.prod, raw=True).fillna(1.0)
    growth126_xlv = (1.0 + r_xlv).rolling(126, min_periods=20).apply(np.prod, raw=True).fillna(1.0)
    nat_smh_weight = (0.70 * growth126_smh) / (0.70 * growth126_smh + 0.30 * growth126_xlv) * 100.0
    raw_drift = nat_smh_weight - 70.0
    sc_drift = rolling_percentile_score(raw_drift, window=756, invert=False)

    composite = (
        0.20 * sc_mom +
        0.20 * sc_dd +
        0.15 * sc_safehaven +
        0.15 * sc_rsi +
        0.10 * sc_vol +
        0.10 * sc_lead +
        0.10 * sc_drift
    ).clip(0.0, 100.0)

    # Forward returns of the 70:30 portfolio & SMH for validation
    fwd_3m_port = (port73_cum.shift(-63) / port73_cum - 1.0) * 100.0
    fwd_6m_port = (port73_cum.shift(-126) / port73_cum - 1.0) * 100.0
    fwd_1y_port = (port73_cum.shift(-252) / port73_cum - 1.0) * 100.0
    fwd_1y_smh = (smh.shift(-252) / smh - 1.0) * 100.0

    df_out = pd.DataFrame({
        'SMH_Close': smh_close,
        'XLV_Close': xlv_close,
        'SMH_Adj': smh,
        'XLV_Adj': xlv,
        'QQQ_Adj': qqq,
        'USDKRW': fx,
        'Port73_Index': port73_cum,
        'FG_Score': composite,
        'SC_Momentum': sc_mom,
        'SC_Drawdown': sc_dd,
        'SC_SafeHaven': sc_safehaven,
        'SC_RSI': sc_rsi,
        'SC_Volatility': sc_vol,
        'SC_Leadership': sc_lead,
        'SC_WeightDrift': sc_drift,
        'RAW_Momentum_Pct': raw_mom,
        'RAW_Drawdown_Pct': raw_dd,
        'RAW_SafeHaven_Spread': raw_safehaven,
        'RAW_RSI': raw_rsi,
        'RAW_Vol20_Ann': vol20_smh,
        'RAW_Leadership_Pct': rel_smh_qqq,
        'RAW_NatWeight_SMH': nat_smh_weight,
        'RAW_WeightDrift_Pctp': raw_drift,
        'FWD_3M_Port73': fwd_3m_port,
        'FWD_6M_Port73': fwd_6m_port,
        'FWD_1Y_Port73': fwd_1y_port,
        'FWD_1Y_SMH': fwd_1y_smh,
    }, index=common)

    df_out.to_csv(HISTORY_CSV_PATH)
    return df_out


def analyze_historical_events_and_zones(df):
    """Verify historical turning points and forward returns by Fear & Greed zone."""
    windows = [
        ("2008년 금융위기 바닥 (리먼 사태)", "2008-10-01", "2008-12-15", "min"),
        ("2011년 유럽재정위기/미 신용등급 강등 바닥", "2011-08-01", "2011-10-15", "min"),
        ("2018년 미·중 무역전쟁 반도체 급락 바닥", "2018-10-01", "2018-12-31", "min"),
        ("2020년 코로나19 팬데믹 폭락 바닥", "2020-02-15", "2020-04-15", "min"),
        ("2021년 유동성 대호황 고점 (과열)", "2021-11-01", "2021-12-31", "max"),
        ("2022년 금리인상 반도체 폭락장 바닥", "2022-09-01", "2022-11-15", "min"),
        ("2024년 7월 AI 반도체 단기 과열 고점", "2024-06-15", "2024-07-20", "max"),
        ("2024년 8월 엔캐리 청산 발작 바닥", "2024-08-01", "2024-09-10", "min"),
        ("2025년 4월 상호관세 쇼크 폭락 바닥", "2025-03-15", "2025-04-30", "min"),
        ("2026년 여름 반도체 랠리 고점 (과열)", "2026-06-01", "2026-08-15", "max"),
        ("2026년 10월 현재 (-20% 조정 구간)", "2026-10-15", "2026-10-27", "min"),
    ]
    event_rows = []
    for title, s_dt, e_dt, mode in windows:
        sub = df.loc[s_dt:e_dt]
        if sub.empty:
            continue
        idx = sub['FG_Score'].idxmin() if mode == 'min' else sub['FG_Score'].idxmax()
        r = df.loc[idx]
        zk, ze, zc, _ = classify_zone(r['FG_Score'])
        event_rows.append({
            'title': title,
            'date': idx.strftime('%Y-%m-%d'),
            'mode': mode,
            'fg_score': float(r['FG_Score']),
            'zone_kor': zk,
            'zone_eng': ze,
            'zone_col': zc,
            'smh_dd': float(r['RAW_Drawdown_Pct']),
            'safehaven': float(r['RAW_SafeHaven_Spread']),
            'fwd_1y_port': float(r['FWD_1Y_Port73']) if not np.isnan(r['FWD_1Y_Port73']) else None,
            'fwd_1y_smh': float(r['FWD_1Y_SMH']) if not np.isnan(r['FWD_1Y_SMH']) else None,
        })

    # Zone stats (from 2003-01-01 onwards where 3-year rolling window is fully warmed up)
    df_valid = df.loc['2003-01-01':].copy()
    zones_def = [
        ("Extreme Fear (0 ~ 25)", 0.0, 25.0, "#ef4444"),
        ("Fear (25 ~ 45)", 25.0, 45.0, "#f97316"),
        ("Neutral (45 ~ 55)", 45.0, 55.0, "#eab308"),
        ("Greed (55 ~ 75)", 55.0, 75.0, "#22c55e"),
        ("Extreme Greed (75 ~ 100)", 75.0, 100.1, "#10b981"),
    ]
    zone_rows = []
    total_days = len(df_valid)
    for zname, lo, hi, col in zones_def:
        mask = (df_valid['FG_Score'] >= lo) & (df_valid['FG_Score'] < hi)
        sub = df_valid[mask]
        cnt = len(sub)
        pct_days = cnt / total_days * 100.0 if total_days > 0 else 0.0
        f3 = sub['FWD_3M_Port73'].dropna()
        f6 = sub['FWD_6M_Port73'].dropna()
        f12 = sub['FWD_1Y_Port73'].dropna()
        f12_smh = sub['FWD_1Y_SMH'].dropna()
        zone_rows.append({
            'zone': zname,
            'color': col,
            'days': int(cnt),
            'share_pct': float(pct_days),
            'avg_3m': float(f3.mean()) if len(f3) else 0.0,
            'avg_6m': float(f6.mean()) if len(f6) else 0.0,
            'avg_1y': float(f12.mean()) if len(f12) else 0.0,
            'win_1y': float((f12 > 0).mean() * 100.0) if len(f12) else 0.0,
            'avg_1y_smh': float(f12_smh.mean()) if len(f12_smh) else 0.0,
        })

    return event_rows, zone_rows


def generate_html_dashboard(df, event_rows, zone_rows):
    """Generate a standalone interactive HTML dashboard for the SMH 70 : XLV 30 Fear & Greed Index."""
    last_dt = df.index[-1]
    cur = df.iloc[-1]
    prev_1d = df.iloc[-2]
    prev_1w = df.iloc[-6]
    prev_1m = df.iloc[-22]
    prev_3m = df.iloc[-64]
    prev_1y = df.iloc[-253]

    z_kor, z_eng, z_col, z_act = classify_zone(cur['FG_Score'])
    is_82_signal = (cur['FG_Score'] < 25.0) or (cur['RAW_Drawdown_Pct'] <= -20.0)
    target_smh_w = 0.80 if is_82_signal else 0.70
    target_xlv_w = 0.20 if is_82_signal else 0.30

    # Prepare chart data (weekly downsampled for early years + daily for last 3 years to keep HTML fast & crisp)
    df_chart_early = df.iloc[:-756:5]
    df_chart_recent = df.iloc[-756:]
    df_chart = pd.concat([df_chart_early, df_chart_recent])
    df_chart = df_chart[~df_chart.index.duplicated(keep='last')].sort_index()

    chart_data = {
        'dates': [d.strftime('%Y-%m-%d') for d in df_chart.index],
        'fg': [round(float(x), 1) for x in df_chart['FG_Score']],
        'smh': [round(float(x), 2) for x in df_chart['SMH_Close']],
        'xlv': [round(float(x), 2) for x in df_chart['XLV_Close']],
        'dd': [round(float(x), 2) for x in df_chart['RAW_Drawdown_Pct']],
        'port73': [round(float(x / df_chart['Port73_Index'].iloc[0] * 100.0), 2) for x in df_chart['Port73_Index']],
    }

    factors_meta = [
        {
            'num': '01',
            'name': 'SMH 추세 모멘텀 (125일선 이격도)',
            'weight': '20%',
            'score': round(float(cur['SC_Momentum']), 1),
            'raw': f"{cur['RAW_Momentum_Pct']:+.2f}% (125일 평균 대비)",
            'desc': 'CNN의 S&P500 125일 이격도에 대응. SMH가 중기 추세선(6개월선) 대비 얼마나 과열·침체되었는지 측정합니다.'
        },
        {
            'num': '02',
            'name': 'SMH 52주 고점 대비 낙폭 (Drawdown)',
            'weight': '20%',
            'score': round(float(cur['SC_Drawdown']), 1),
            'raw': f"{cur['RAW_Drawdown_Pct']:+.2f}% (8:2 전환 기준: -20.0%)",
            'desc': '포트폴리오 핵심 스위치! SMH가 52주 고점 대비 -20% 하락하면 점수가 20점(극단적 공포) 이하로 떨어지며 8:2 스위칭을 알립니다.'
        },
        {
            'num': '03',
            'name': '안전자산 선호도 (SMH - XLV 20일 격차)',
            'weight': '15%',
            'score': round(float(cur['SC_SafeHaven']), 1),
            'raw': f"{cur['RAW_SafeHaven_Spread']:+.2f}%p (최근 20거래일)",
            'desc': 'CNN의 주식-채권 수익률 격차에 대응. 시장 공포로 반도체를 던지고 헬스케어(XLV)로 도피할수록 극단적 공포로 내려갑니다.'
        },
        {
            'num': '04',
            'name': '포트폴리오 상대강도 (14일 가중 RSI)',
            'weight': '15%',
            'score': round(float(cur['SC_RSI']), 1),
            'raw': f"RSI {cur['RAW_RSI']:.1f} (과매도 30 / 과매수 70)",
            'desc': 'SMH(70%)와 7:3 포트폴리오(30%)의 14일 RSI를 결합하여 단기 매수·매도 클라이맥스를 포착합니다.'
        },
        {
            'num': '05',
            'name': '반도체 변동성 안정도 (20일 변동성 역지표)',
            'weight': '10%',
            'score': round(float(cur['SC_Volatility']), 1),
            'raw': f"연환산 변동성 {cur['RAW_Vol20_Ann']:.1f}%",
            'desc': 'CNN의 VIX 지수에 대응. SMH의 20일 실현 변동성이 50일 평균 대비 급등(패닉 셀링)하면 공포 점수로 반영됩니다.'
        },
        {
            'num': '06',
            'name': '나스닥 대비 반도체 주도력 (60일 상대알파)',
            'weight': '10%',
            'score': round(float(cur['SC_Leadership']), 1),
            'raw': f"SMH vs QQQ {cur['RAW_Leadership_Pct']:+.2f}% (60일)",
            'desc': '기술주 전체(QQQ) 대비 반도체(SMH)로 자금이 쏠리는지(탐욕), 빠져나가는지(공포) 측정합니다.'
        },
        {
            'num': '07',
            'name': '7:3 자연 비중 괴리도 (반기 누적 드리프트)',
            'weight': '10%',
            'score': round(float(cur['SC_WeightDrift']), 1),
            'raw': f"자연비중 SMH {cur['RAW_NatWeight_SMH']:.1f}% : XLV {100-cur['RAW_NatWeight_SMH']:.1f}% ({cur['RAW_WeightDrift_Pctp']:+.2f}%p)",
            'desc': '6개월 전 70:30으로 맞춘 계좌를 방치했을 때 현재 자연 비중입니다. 70% 밑으로 줄어들수록 저가 매수(리밸런싱) 기회입니다.'
        },
    ]

    for f in factors_meta:
        zk, ze, zc, _ = classify_zone(f['score'])
        f['zone_kor'] = zk.split(' ')[0] + (' ' + zk.split(' ')[1] if 'EXTREME' in zk else '')
        f['color'] = zc

    timeline_items = []
    for lbl, row in [
        ("전일 (1일 전)", prev_1d),
        ("1주일 전 (5거래일)", prev_1w),
        ("1개월 전 (21거래일)", prev_1m),
        ("3개월 전 (63거래일)", prev_3m),
        ("1년 전 (252거래일)", prev_1y),
    ]:
        zk, ze, zc, _ = classify_zone(row['FG_Score'])
        timeline_items.append({
            'label': lbl,
            'date': row.name.strftime('%Y-%m-%d'),
            'score': round(float(row['FG_Score']), 1),
            'zone': zk,
            'color': zc,
            'smh': f"${row['SMH_Close']:.2f}",
            'dd': f"{row['RAW_Drawdown_Pct']:+.1f}%"
        })

    # Needle angle for semicircular gauge (-90 deg = 0, +90 deg = 100)
    score_val = float(cur['FG_Score'])
    needle_deg = -90.0 + (score_val / 100.0) * 180.0

    html = f"""<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>SMH 70% : XLV 30% Fear & Greed Index Dashboard</title>
<style>
  :root {{
    --bg: #0b0f19;
    --card: #131b2e;
    --card-border: #1e293b;
    --text: #f1f5f9;
    --muted: #94a3b8;
    --accent: {z_col};
  }}
  * {{ box-sizing: border-box; margin: 0; padding: 0; }}
  body {{
    font-family: 'Pretendard', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    background: var(--bg);
    color: var(--text);
    line-height: 1.55;
    padding: 24px;
  }}
  .container {{ max-width: 1340px; margin: 0 auto; }}
  .header {{
    display: flex;
    flex-wrap: wrap;
    justify-content: space-between;
    align-items: center;
    padding: 20px 26px;
    background: linear-gradient(135deg, #131b2e 0%, #0f172a 100%);
    border: 1px solid var(--card-border);
    border-radius: 16px;
    margin-bottom: 20px;
  }}
  .header h1 {{ font-size: 1.55rem; font-weight: 800; letter-spacing: -0.02em; }}
  .header .sub {{ color: var(--muted); font-size: 0.92rem; margin-top: 4px; }}
  .badge-live {{
    padding: 8px 16px;
    border-radius: 999px;
    font-weight: 700;
    font-size: 0.9rem;
    background: rgba(255,255,255,0.06);
    border: 1px solid rgba(255,255,255,0.14);
  }}
  .top-grid {{
    display: grid;
    grid-template-columns: 1.05fr 1.25fr;
    gap: 20px;
    margin-bottom: 20px;
  }}
  @media (max-width: 980px) {{
    .top-grid {{ grid-template-columns: 1fr; }}
  }}
  .card {{
    background: var(--card);
    border: 1px solid var(--card-border);
    border-radius: 16px;
    padding: 24px;
  }}
  .card-title {{
    font-size: 1.08rem;
    font-weight: 700;
    margin-bottom: 16px;
    display: flex;
    justify-content: space-between;
    align-items: center;
  }}
  .gauge-wrap {{
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding: 6px 0 12px;
  }}
  .score-big {{
    font-size: 3.2rem;
    font-weight: 900;
    color: {z_col};
    line-height: 1.05;
    margin-top: -10px;
  }}
  .zone-pill {{
    display: inline-block;
    margin-top: 8px;
    padding: 6px 18px;
    border-radius: 999px;
    font-weight: 800;
    font-size: 1rem;
    background: {z_col}22;
    color: {z_col};
    border: 1.5px solid {z_col};
  }}
  .signal-box {{
    margin-top: 18px;
    width: 100%;
    padding: 15px 18px;
    border-radius: 12px;
    background: rgba(15, 23, 42, 0.75);
    border-left: 4px solid {z_col};
    font-size: 0.95rem;
  }}
  .kpi-row {{
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 10px;
    margin-top: 14px;
    width: 100%;
  }}
  .kpi-item {{
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 10px;
    padding: 10px 12px;
    text-align: center;
  }}
  .kpi-item .k-lbl {{ font-size: 0.78rem; color: var(--muted); }}
  .kpi-item .k-val {{ font-size: 1.08rem; font-weight: 800; margin-top: 2px; }}
  .timeline-list {{ display: flex; flex-direction: column; gap: 10px; }}
  .tl-row {{
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 11px 14px;
    background: rgba(255,255,255,0.025);
    border: 1px solid rgba(255,255,255,0.06);
    border-radius: 10px;
  }}
  .tl-left .tl-lbl {{ font-weight: 700; font-size: 0.93rem; }}
  .tl-left .tl-dt {{ color: var(--muted); font-size: 0.8rem; margin-left: 6px; }}
  .tl-right {{ display: flex; align-items: center; gap: 10px; }}
  .tl-score {{
    font-weight: 800;
    font-size: 1.05rem;
    padding: 3px 10px;
    border-radius: 8px;
  }}
  .factors-grid {{
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(360px, 1fr));
    gap: 14px;
    margin-bottom: 20px;
  }}
  .factor-card {{
    background: var(--card);
    border: 1px solid var(--card-border);
    border-radius: 14px;
    padding: 16px 18px;
  }}
  .f-top {{ display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px; }}
  .f-name {{ font-weight: 700; font-size: 0.96rem; }}
  .f-weight {{ font-size: 0.76rem; color: var(--muted); background: rgba(255,255,255,0.06); padding: 2px 8px; border-radius: 6px; }}
  .f-bar-bg {{
    width: 100%;
    height: 10px;
    background: #0f172a;
    border-radius: 999px;
    overflow: hidden;
    margin: 8px 0;
    border: 1px solid rgba(255,255,255,0.07);
  }}
  .f-bar-fill {{ height: 100%; border-radius: 999px; }}
  .f-meta {{ display: flex; justify-content: space-between; font-size: 0.84rem; color: #cbd5e1; margin-bottom: 6px; }}
  .f-desc {{ font-size: 0.8rem; color: var(--muted); }}
  table {{ width: 100%; border-collapse: collapse; font-size: 0.88rem; }}
  th, td {{ padding: 10px 12px; text-align: left; border-bottom: 1px solid rgba(255,255,255,0.07); }}
  th {{ color: var(--muted); font-weight: 600; background: rgba(255,255,255,0.02); }}
  .num {{ text-align: right; font-variant-numeric: tabular-nums; }}
  .calc-grid {{
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 14px;
    margin-top: 12px;
  }}
  @media (max-width: 980px) {{
    .calc-grid {{ grid-template-columns: 1fr; }}
  }}
  .calc-box {{
    background: rgba(15, 23, 42, 0.7);
    border: 1px solid rgba(255,255,255,0.09);
    border-radius: 12px;
    padding: 16px;
  }}
  .calc-box h4 {{ font-size: 0.96rem; margin-bottom: 10px; color: #38bdf8; }}
  .inp-group {{ display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px; font-size: 0.85rem; }}
  .inp-group input {{
    width: 120px;
    padding: 6px 10px;
    border-radius: 8px;
    border: 1px solid #334155;
    background: #0f172a;
    color: #fff;
    text-align: right;
    font-weight: 700;
  }}
  .calc-res {{
    margin-top: 10px;
    padding-top: 10px;
    border-top: 1px dashed rgba(255,255,255,0.12);
    font-size: 0.85rem;
  }}
  .btn-group {{ display: flex; gap: 8px; }}
  .btn {{
    padding: 6px 12px;
    border-radius: 8px;
    border: 1px solid #334155;
    background: #1e293b;
    color: #e2e8f0;
    cursor: pointer;
    font-size: 0.82rem;
    font-weight: 600;
  }}
  .btn.active {{ background: #3b82f6; border-color: #60a5fa; color: #fff; }}
  canvas {{ width: 100%; height: 340px; display: block; }}
</style>
</head>
<body>
<div class="container">
  <div class="header">
    <div>
      <h1>📊 [SMH 70% : XLV 30%] 전용 공포·탐욕 지수 (Fear & Greed Index)</h1>
      <div class="sub">CNN 7-Factor 방법론 기반 | 평시 7:3 ➔ 극단적 공포(SMH -20% 하락) 시 8:2 역발상 스위칭 레이더</div>
    </div>
    <div class="badge-live">최종 업데이트: {last_dt.strftime('%Y-%m-%d')} (Yahoo Finance 실시간 연동)</div>
  </div>

  <div class="top-grid">
    <!-- Speedometer Gauge Card -->
    <div class="card">
      <div class="card-title">
        <span>현재 포트폴리오 심리 상태</span>
        <span style="font-size:0.82rem;color:var(--muted);">0 = 극단적 공포 | 100 = 극단적 탐욕</span>
      </div>
      <div class="gauge-wrap">
        <svg viewBox="0 0 320 175" width="310" height="170">
          <!-- 5 Zone Arcs -->
          <!-- Extreme Fear: 0~25 (-90 to -45 deg) -->
          <path d="M 30 150 A 130 130 0 0 1 68.1 58.1" fill="none" stroke="#ef4444" stroke-width="22" />
          <!-- Fear: 25~45 (-45 to -9 deg) -->
          <path d="M 68.1 58.1 A 130 130 0 0 1 139.7 21.6" fill="none" stroke="#f97316" stroke-width="22" />
          <!-- Neutral: 45~55 (-9 to +9 deg) -->
          <path d="M 139.7 21.6 A 130 130 0 0 1 180.3 21.6" fill="none" stroke="#eab308" stroke-width="22" />
          <!-- Greed: 55~75 (+9 to +45 deg) -->
          <path d="M 180.3 21.6 A 130 130 0 0 1 251.9 58.1" fill="none" stroke="#22c55e" stroke-width="22" />
          <!-- Extreme Greed: 75~100 (+45 to +90 deg) -->
          <path d="M 251.9 58.1 A 130 130 0 0 1 290 150" fill="none" stroke="#10b981" stroke-width="22" />
          <!-- Labels -->
          <text x="18" y="168" fill="#94a3b8" font-size="11" font-weight="700">0</text>
          <text x="50" y="48" fill="#ef4444" font-size="10" font-weight="700">25</text>
          <text x="160" y="12" fill="#eab308" font-size="10" font-weight="700" text-anchor="middle">50</text>
          <text x="268" y="48" fill="#22c55e" font-size="10" font-weight="700">75</text>
          <text x="292" y="168" fill="#94a3b8" font-size="11" font-weight="700">100</text>
          <!-- Needle -->
          <g transform="translate(160, 150) rotate({needle_deg:.2f})">
            <polygon points="-4,0 0,-112 4,0" fill="#f8fafc" />
            <circle cx="0" cy="0" r="9" fill="#f8fafc" />
          </g>
        </svg>
        <div class="score-big">{score_val:.1f}</div>
        <div class="zone-pill">{z_kor}</div>

        <div class="signal-box">
          <div style="font-weight:800;margin-bottom:4px;">{z_act}</div>
          <div style="font-size:0.84rem;color:var(--muted);">
            권장 목표 비중: <strong style="color:#fff;">SMH {int(target_smh_w*100)}% : XLV {int(target_xlv_w*100)}%</strong>
            (현재 반기 자연비중: SMH {cur['RAW_NatWeight_SMH']:.1f}% : XLV {100-cur['RAW_NatWeight_SMH']:.1f}%)
          </div>
        </div>

        <div class="kpi-row">
          <div class="kpi-item">
            <div class="k-lbl">SMH 현재가 (52주 고점대비)</div>
            <div class="k-val">${cur['SMH_Close']:.2f} <span style="font-size:0.84rem;color:#ef4444;">({cur['RAW_Drawdown_Pct']:+.1f}%)</span></div>
          </div>
          <div class="kpi-item">
            <div class="k-lbl">XLV 현재가 (20일 방어력)</div>
            <div class="k-val">${cur['XLV_Close']:.2f} <span style="font-size:0.84rem;color:#38bdf8;">({-cur['RAW_SafeHaven_Spread']:+.1f}%p 우위)</span></div>
          </div>
          <div class="kpi-item">
            <div class="k-lbl">원/달러 환율 (USD/KRW)</div>
            <div class="k-val">{cur['USDKRW']:,.1f}원</div>
          </div>
        </div>
      </div>
    </div>

    <!-- Timeline & Rules Card -->
    <div class="card">
      <div class="card-title">
        <span>시점별 공포·탐욕 지수 추이</span>
        <span style="font-size:0.82rem;color:var(--muted);">최근 1년 흐름</span>
      </div>
      <div class="timeline-list">
"""
    for item in timeline_items:
        html += f"""        <div class="tl-row">
          <div class="tl-left">
            <span class="tl-lbl">{item['label']}</span>
            <span class="tl-dt">({item['date']} | SMH {item['smh']}, DD {item['dd']})</span>
          </div>
          <div class="tl-right">
            <span style="font-size:0.82rem;color:{item['color']};font-weight:700;">{item['zone']}</span>
            <span class="tl-score" style="background:{item['color']}22;color:{item['color']};border:1px solid {item['color']};">{item['score']:.1f}</span>
          </div>
        </div>\n"""

    html += f"""      </div>
      <div style="margin-top:18px;padding:14px 16px;background:rgba(56,189,248,0.07);border:1px solid rgba(56,189,248,0.25);border-radius:12px;font-size:0.86rem;">
        <div style="font-weight:800;color:#38bdf8;margin-bottom:6px;">📌 [SMH 70% : XLV 30%] 공포·탐욕 지수 3대 실전 공식</div>
        <div>1️⃣ <strong>지수 25점 미만 (Extreme Fear) & SMH 고점 대비 -20% 도달 시</strong>: XLV 방어주를 팔아 폭락한 SMH를 <strong>80% : 20%</strong>까지 역발상 매집합니다.</div>
        <div style="margin-top:4px;">2️⃣ <strong>지수 25 ~ 75점 (Fear / Neutral / Greed)</strong>: 평시 황금 비중인 <strong>70% : 30%</strong>을 유지하며 적립식·거치식 복리를 누립니다.</div>
        <div style="margin-top:4px;">3️⃣ <strong>지수 75점 이상 (Extreme Greed)</strong>: 반도체 과열 구간이므로 추격 매수를 멈추고, 정기 리밸런싱 시 비대해진 SMH 수익을 잘라 <strong>XLV(30% 금고)</strong>에 잠급니다.</div>
      </div>
    </div>
  </div>

  <!-- 7 Sub-Indicators -->
  <div class="card" style="margin-bottom:20px;">
    <div class="card-title">
      <span>🔍 7대 세부 팩터 실시간 해부 (CNN 7-Component 맞춤형 설계)</span>
      <span style="font-size:0.82rem;color:var(--muted);">가중평균 합산 = 현재 {score_val:.1f}점</span>
    </div>
    <div class="factors-grid" style="margin-bottom:0;">
"""
    for f in factors_meta:
        html += f"""      <div class="factor-card">
        <div class="f-top">
          <span class="f-name">{f['num']}. {f['name']}</span>
          <span class="f-weight">가중치 {f['weight']}</span>
        </div>
        <div class="f-bar-bg">
          <div class="f-bar-fill" style="width:{f['score']}%;background:{f['color']};"></div>
        </div>
        <div class="f-meta">
          <span>측정값: <strong>{f['raw']}</strong></span>
          <span style="color:{f['color']};font-weight:800;">{f['score']:.1f}점 ({f['zone_kor']})</span>
        </div>
        <div class="f-desc">{f['desc']}</div>
      </div>\n"""

    html += f"""    </div>
  </div>

  <!-- Interactive Historical Chart -->
  <div class="card" style="margin-bottom:20px;">
    <div class="card-title">
      <span>📈 2000~2026 히스토리컬 차트 (공포·탐욕 지수 vs SMH 고점대비 낙폭)</span>
      <div class="btn-group">
        <button class="btn" onclick="setRange(252, this)">최근 1년</button>
        <button class="btn active" onclick="setRange(756, this)">최근 3년</button>
        <button class="btn" onclick="setRange(1200, this)">최근 5년</button>
        <button class="btn" onclick="setRange(99999, this)">전체 (2000~2026)</button>
      </div>
    </div>
    <canvas id="fgChart" width="1260" height="340"></canvas>
    <div style="display:flex;justify-content:space-between;font-size:0.8rem;color:var(--muted);margin-top:8px;">
      <span>🔴 빨간 점선 아래(25점 미만): <strong>극단적 공포 (8:2 역발상 매수 구간)</strong></span>
      <span>🟢 초록 점선 위(75점 이상): <strong>극단적 탐욕 (7:3 차익 잠금 구간)</strong></span>
      <span>🔵 파란 실선: <strong>SMH 70:XLV 30 공포·탐욕 지수 (0~100)</strong></span>
    </div>
  </div>

  <!-- 3-Account Interactive Rebalancing Calculator -->
  <div class="card" style="margin-bottom:20px;">
    <div class="card-title">
      <span>🧮 3대 계좌 [7:3 / 8:2] 리밸런싱 주문 수량 자동 계산기</span>
      <div class="btn-group">
        <button class="btn {'active' if not is_82_signal else ''}" id="btn73" onclick="setTargetRatio(0.70)">평시 7:3 모드 (SMH 70 : XLV 30)</button>
        <button class="btn {'active' if is_82_signal else ''}" id="btn82" onclick="setTargetRatio(0.80)">폭락장 8:2 모드 (SMH 80 : XLV 20)</button>
      </div>
    </div>
    <div style="font-size:0.86rem;color:var(--muted);margin-bottom:10px;">
      현재 시세 자동 입력됨: <strong>SMH = ${cur['SMH_Close']:.2f}</strong>, <strong>XLV = ${cur['XLV_Close']:.2f}</strong>, <strong>환율 = {cur['USDKRW']:,.1f}원/$</strong>.
      각 계좌의 현재 보유 주수(또는 투입 원화 금액)를 입력하면 목표 비중에 맞춘 정확한 매수·매도 주문 주수를 계산합니다.
    </div>
    <div class="calc-grid">
      <div class="calc-box">
        <h4>① 본인 계좌 (SK 3,500만 + 27년 3,500만 + 월 70만)</h4>
        <div class="inp-group"><span>현재 SMH 보유 주수</span><input type="number" id="a1_smh" value="65" oninput="recalcAll()"></div>
        <div class="inp-group"><span>현재 XLV 보유 주수</span><input type="number" id="a1_xlv" value="85" oninput="recalcAll()"></div>
        <div class="inp-group"><span>추가 현금 투입 (만원)</span><input type="number" id="a1_cash" value="0" oninput="recalcAll()"></div>
        <div class="calc-res" id="a1_res"></div>
      </div>
      <div class="calc-box">
        <h4>② 아버지 증여·모아타운 계좌 (2027년 4억 원 거치)</h4>
        <div class="inp-group"><span>현재 SMH 보유 주수</span><input type="number" id="a2_smh" value="0" oninput="recalcAll()"></div>
        <div class="inp-group"><span>현재 XLV 보유 주수</span><input type="number" id="a2_xlv" value="0" oninput="recalcAll()"></div>
        <div class="inp-group"><span>신규/추가 현금 (만원)</span><input type="number" id="a2_cash" value="40000" oninput="recalcAll()"></div>
        <div class="calc-res" id="a2_res"></div>
      </div>
      <div class="calc-box">
        <h4>③ 성수3지구 이주비 대출 계좌 (2030년 10억 원 거치)</h4>
        <div class="inp-group"><span>현재 SMH 보유 주수</span><input type="number" id="a3_smh" value="0" oninput="recalcAll()"></div>
        <div class="inp-group"><span>현재 XLV 보유 주수</span><input type="number" id="a3_xlv" value="0" oninput="recalcAll()"></div>
        <div class="inp-group"><span>신규/추가 현금 (만원)</span><input type="number" id="a3_cash" value="100000" oninput="recalcAll()"></div>
        <div class="calc-res" id="a3_res"></div>
      </div>
    </div>
  </div>

  <!-- Historical Verification Tables -->
  <div class="top-grid">
    <div class="card">
      <div class="card-title">
        <span>📊 공포·탐욕 5개 구간별 진입 시 향후 수익률 검증 (2003~2026)</span>
      </div>
      <table>
        <thead>
          <tr>
            <th>지수 구간</th>
            <th class="num">출현 일수(비중)</th>
            <th class="num">3개월 평균</th>
            <th class="num">6개월 평균</th>
            <th class="num">1년 후 7:3 평균</th>
            <th class="num">1년 후 SMH 평균</th>
            <th class="num">1년 승률</th>
          </tr>
        </thead>
        <tbody>
"""
    for zr in zone_rows:
        html += f"""          <tr>
            <td style="color:{zr['color']};font-weight:700;">{zr['zone']}</td>
            <td class="num">{zr['days']:,}일 ({zr['share_pct']:.1f}%)</td>
            <td class="num">{zr['avg_3m']:+.2f}%</td>
            <td class="num">{zr['avg_6m']:+.2f}%</td>
            <td class="num" style="font-weight:800;color:#38bdf8;">{zr['avg_1y']:+.2f}%</td>
            <td class="num" style="font-weight:700;">{zr['avg_1y_smh']:+.2f}%</td>
            <td class="num">{zr['win_1y']:.1f}%</td>
          </tr>\n"""

    html += """        </tbody>
      </table>
    </div>

    <div class="card">
      <div class="card-title">
        <span>🏛️ 역대 주요 폭락장 바닥 & 과열 고점 당시 실제 점수</span>
      </div>
      <table>
        <thead>
          <tr>
            <th>역사적 사건</th>
            <th>날짜</th>
            <th class="num">지수</th>
            <th class="num">SMH 낙폭</th>
            <th class="num">이후 1년 (7:3)</th>
          </tr>
        </thead>
        <tbody>
"""
    for er in event_rows:
        f1y_str = f"{er['fwd_1y_port']:+.1f}%" if er['fwd_1y_port'] is not None else "진행 중"
        html += f"""          <tr>
            <td>{er['title']}</td>
            <td style="color:var(--muted);">{er['date']}</td>
            <td class="num" style="color:{er['zone_col']};font-weight:800;">{er['fg_score']:.1f}점</td>
            <td class="num">{er['smh_dd']:+.1f}%</td>
            <td class="num" style="font-weight:700;color:#38bdf8;">{f1y_str}</td>
          </tr>\n"""

    html += f"""        </tbody>
      </table>
    </div>
  </div>
</div>

<script>
const CHART_DATA = {json.dumps(chart_data)};
const P_SMH = {float(cur['SMH_Close']):.4f};
const P_XLV = {float(cur['XLV_Close']):.4f};
const FX_RATE = {float(cur['USDKRW']):.2f};
let TARGET_SMH_W = {target_smh_w:.2f};
let CURRENT_RANGE = 756;

function setTargetRatio(w) {{
  TARGET_SMH_W = w;
  document.getElementById('btn73').classList.toggle('active', Math.abs(w - 0.70) < 0.01);
  document.getElementById('btn82').classList.toggle('active', Math.abs(w - 0.80) < 0.01);
  recalcAll();
}}

function calcAccount(prefix) {{
  const shSmh = parseFloat(document.getElementById(prefix + '_smh').value || 0);
  const shXlv = parseFloat(document.getElementById(prefix + '_xlv').value || 0);
  const cashManwon = parseFloat(document.getElementById(prefix + '_cash').value || 0);
  const cashUsd = (cashManwon * 10000.0) / FX_RATE;

  const curSmhUsd = shSmh * P_SMH;
  const curXlvUsd = shXlv * P_XLV;
  const totalUsd = curSmhUsd + curXlvUsd + cashUsd;
  const totalKrwMan = (totalUsd * FX_RATE) / 10000.0;

  if (totalUsd <= 0) {{
    document.getElementById(prefix + '_res').innerHTML = '보유 수량 또는 현금을 입력하세요.';
    return;
  }}

  const curSmhW = (curSmhUsd / totalUsd) * 100.0;
  const tgtSmhUsd = totalUsd * TARGET_SMH_W;
  const tgtXlvUsd = totalUsd * (1.0 - TARGET_SMH_W);

  const tgtSmhSh = Math.floor(tgtSmhUsd / P_SMH);
  const remUsd = totalUsd - (tgtSmhSh * P_SMH);
  const tgtXlvSh = Math.floor(remUsd / P_XLV);

  const diffSmh = tgtSmhSh - shSmh;
  const diffXlv = tgtXlvSh - shXlv;

  const fmtDiff = (d) => d > 0 ? `<span style="color:#ef4444;font-weight:800;">+${{d}}주 매수</span>` : (d < 0 ? `<span style="color:#38bdf8;font-weight:800;">${{d}}주 매도</span>` : `<span style="color:#94a3b8;">유지 (0주)</span>`);

  document.getElementById(prefix + '_res').innerHTML = `
    <div>총 평가액: <strong>약 ${{Math.round(totalKrwMan).toLocaleString()}}만 원</strong> ($${{totalUsd.toLocaleString(undefined, {{maximumFractionDigits:0}})}})</div>
    <div>현재 비중: SMH ${{curSmhW.toFixed(1)}}% / 목표: <strong>SMH ${{Math.round(TARGET_SMH_W*100)}}% : XLV ${{Math.round((1-TARGET_SMH_W)*100)}}%</strong></div>
    <div style="margin-top:6px;">👉 <strong>SMH 목표 ${{tgtSmhSh.toLocaleString()}}주</strong> (${{fmtDiff(diffSmh)}})</div>
    <div>👉 <strong>XLV 목표 ${{tgtXlvSh.toLocaleString()}}주</strong> (${{fmtDiff(diffXlv)}})</div>
  `;
}}

function recalcAll() {{
  calcAccount('a1');
  calcAccount('a2');
  calcAccount('a3');
}}

function setRange(n, btn) {{
  CURRENT_RANGE = n;
  document.querySelectorAll('.btn-group .btn').forEach(b => {{
    if (b.onclick && b.onclick.toString().includes('setRange')) b.classList.remove('active');
  }});
  if (btn) btn.classList.add('active');
  drawChart();
}}

function drawChart() {{
  const canvas = document.getElementById('fgChart');
  const ctx = canvas.getContext('2d');
  const W = canvas.width;
  const H = canvas.height;
  ctx.clearRect(0, 0, W, H);

  const totalLen = CHART_DATA.dates.length;
  const startIdx = Math.max(0, totalLen - CURRENT_RANGE);
  const dates = CHART_DATA.dates.slice(startIdx);
  const fg = CHART_DATA.fg.slice(startIdx);
  const dd = CHART_DATA.dd.slice(startIdx);
  const N = dates.length;
  if (N < 2) return;

  const padL = 48, padR = 54, padT = 20, padB = 34;
  const plotW = W - padL - padR;
  const plotH = H - padT - padB;

  const yOfFG = (val) => padT + plotH * (1.0 - val / 100.0);

  // Shaded Extreme Greed (75~100) and Extreme Fear (0~25)
  ctx.fillStyle = 'rgba(16, 185, 129, 0.08)';
  ctx.fillRect(padL, yOfFG(100), plotW, yOfFG(75) - yOfFG(100));

  ctx.fillStyle = 'rgba(239, 68, 68, 0.10)';
  ctx.fillRect(padL, yOfFG(25), plotW, yOfFG(0) - yOfFG(25));

  // Horizontal grid lines
  [0, 25, 50, 75, 100].forEach(v => {{
    const y = yOfFG(v);
    ctx.strokeStyle = (v === 25) ? 'rgba(239,68,68,0.55)' : (v === 75 ? 'rgba(16,185,129,0.55)' : 'rgba(255,255,255,0.08)');
    ctx.setLineDash((v === 25 || v === 75) ? [5, 5] : []);
    ctx.beginPath();
    ctx.moveTo(padL, y);
    ctx.lineTo(padL + plotW, y);
    ctx.stroke();

    ctx.fillStyle = '#94a3b8';
    ctx.font = '11px sans-serif';
    ctx.textAlign = 'right';
    ctx.fillText(v + '점', padL - 6, y + 4);
  }});
  ctx.setLineDash([]);

  // Draw Fear & Greed Line
  ctx.strokeStyle = '#38bdf8';
  ctx.lineWidth = 2.0;
  ctx.beginPath();
  for (let i = 0; i < N; i++) {{
    const x = padL + (i / (N - 1)) * plotW;
    const y = yOfFG(fg[i]);
    if (i === 0) ctx.moveTo(x, y);
    else ctx.lineTo(x, y);
  }}
  ctx.stroke();

  // Highlight Extreme Fear dots (<25)
  ctx.fillStyle = '#ef4444';
  for (let i = 0; i < N; i++) {{
    if (fg[i] < 25.0) {{
      const x = padL + (i / (N - 1)) * plotW;
      const y = yOfFG(fg[i]);
      ctx.beginPath();
      ctx.arc(x, y, 2.3, 0, Math.PI * 2);
      ctx.fill();
    }}
  }}

  // X-axis date labels
  ctx.fillStyle = '#94a3b8';
  ctx.font = '11px sans-serif';
  ctx.textAlign = 'center';
  const step = Math.max(1, Math.floor(N / 7));
  for (let i = 0; i < N; i += step) {{
    const x = padL + (i / (N - 1)) * plotW;
    ctx.fillText(dates[i], x, H - 10);
  }}
}}

window.addEventListener('DOMContentLoaded', () => {{
  recalcAll();
  drawChart();
}});
</script>
</body>
</html>
"""
    with open(DASHBOARD_PATH, 'w', encoding='utf-8') as f:
        f.write(html)


if __name__ == '__main__':
    df = build_fear_greed_index(do_live_update=True)
    event_rows, zone_rows = analyze_historical_events_and_zones(df)
    generate_html_dashboard(df, event_rows, zone_rows)

    last_dt = df.index[-1]
    cur = df.iloc[-1]
    prev_1d = df.iloc[-2]
    prev_1w = df.iloc[-6] if len(df) >= 6 else cur
    prev_1m = df.iloc[-22] if len(df) >= 22 else cur
    prev_3m = df.iloc[-64] if len(df) >= 64 else cur
    prev_1y = df.iloc[-253] if len(df) >= 253 else cur

    z_kor, z_eng, z_col, z_act = classify_zone(cur['FG_Score'])
    print("=" * 96)
    print(f" 📊 [SMH 70% : XLV 30%] 전용 공포·탐욕 지수 (Fear & Greed Index) | 기준일: {last_dt.strftime('%Y-%m-%d')}")
    print("=" * 96)
    print(f" ▶ 현재 종합 점수 : {cur['FG_Score']:5.1f} / 100  [{z_kor}]")
    print(f" ▶ 실전 행동 지침 : {z_act}")
    print(f" ▶ SMH 현재가     : ${cur['SMH_Close']:.2f} (52주 고점 대비 {cur['RAW_Drawdown_Pct']:+.2f}% | 125일선 대비 {cur['RAW_Momentum_Pct']:+.2f}%)")
    print(f" ▶ XLV 현재가     : ${cur['XLV_Close']:.2f} (최근 20일 SMH-XLV 수익률 격차: {cur['RAW_SafeHaven_Spread']:+.2f}%p)")
    print(f" ▶ 반기 자연 비중 : SMH {cur['RAW_NatWeight_SMH']:.1f}% : XLV {100-cur['RAW_NatWeight_SMH']:.1f}% (목표 70% 대비 {cur['RAW_WeightDrift_Pctp']:+.2f}%p)")
    print("-" * 96)
    print(" [시점별 추이 비교]")
    for lbl, row in [
        ("전일 (1일 전)", prev_1d),
        ("1주일 전 (5거래일)", prev_1w),
        ("1개월 전 (21거래일)", prev_1m),
        ("3개월 전 (63거래일)", prev_3m),
        ("1년 전 (252거래일)", prev_1y),
    ]:
        zk, _, _, _ = classify_zone(row['FG_Score'])
        print(f"  • {lbl:<18}: {row['FG_Score']:5.1f}점 ({zk:<24}) | SMH ${row['SMH_Close']:.2f} (DD {row['RAW_Drawdown_Pct']:+.1f}%)")
    print("-" * 96)
    print(" [7대 세부 팩터별 점수 (0=극단적 공포 ~ 100=극단적 탐욕)]")
    factors = [
        ("① SMH 추세 모멘텀 (125일선 이격도, 20%)", cur['SC_Momentum'], f"{cur['RAW_Momentum_Pct']:+.2f}%"),
        ("② SMH 고점 대비 낙폭 (52주 DD, 20%)", cur['SC_Drawdown'], f"{cur['RAW_Drawdown_Pct']:+.2f}% (기준 -20%)"),
        ("③ 안전자산 선호도 (SMH-XLV 20일 격차, 15%)", cur['SC_SafeHaven'], f"{cur['RAW_SafeHaven_Spread']:+.2f}%p"),
        ("④ 포트폴리오 강도 (14일 가중 RSI, 15%)", cur['SC_RSI'], f"RSI {cur['RAW_RSI']:.1f}"),
        ("⑤ 반도체 변동성 안정도 (20일 변동성 역지표, 10%)", cur['SC_Volatility'], f"연변동성 {cur['RAW_Vol20_Ann']:.1f}%"),
        ("⑥ 나스닥 대비 반도체 주도력 (60일 상대알파, 10%)", cur['SC_Leadership'], f"{cur['RAW_Leadership_Pct']:+.2f}%"),
        ("⑦ 7:3 자연 비중 괴리도 (반기 누적 드리프트, 10%)", cur['SC_WeightDrift'], f"SMH {cur['RAW_NatWeight_SMH']:.1f}% ({cur['RAW_WeightDrift_Pctp']:+.1f}%p)"),
    ]
    for name, sc, raw_str in factors:
        zk, _, _, _ = classify_zone(sc)
        bar = "█" * int(round(sc / 5.0)) + "░" * (20 - int(round(sc / 5.0)))
        print(f"  {name:<42} | {bar} {sc:5.1f}점 | {raw_str:<22} | {zk.split(' ')[0]}")
    print("-" * 96)
    print(" [공포·탐욕 5개 구간별 진입 시 향후 수익률 백테스트 (2003~2026)]")
    for zr in zone_rows:
        print(f"  • {zr['zone']:<26} | 출현 {zr['days']:4d}일 ({zr['share_pct']:4.1f}%) | 3M {zr['avg_3m']:+6.2f}% | 6M {zr['avg_6m']:+6.2f}% | 1Y(7:3) {zr['avg_1y']:+6.2f}% | 1Y(SMH) {zr['avg_1y_smh']:+6.2f}% | 1Y승률 {zr['win_1y']:5.1f}%")
    print("-" * 96)
    print(" [역대 주요 폭락장 바닥 & 과열 고점 당시 실제 점수]")
    for er in event_rows:
        f1y = f"{er['fwd_1y_port']:+6.1f}%" if er['fwd_1y_port'] is not None else " 진행중"
        f1y_s = f"{er['fwd_1y_smh']:+6.1f}%" if er['fwd_1y_smh'] is not None else " 진행중"
        print(f"  • {er['title']:<34} ({er['date']}) | 지수 {er['fg_score']:5.1f}점 | SMH DD {er['smh_dd']:+6.1f}% | 1년후(7:3) {f1y} | 1년후(SMH) {f1y_s}")
    print("=" * 96)
    print(f" ✅ 인터랙티브 대시보드 생성 완료: {DASHBOARD_PATH}")
    print(f" ✅ 전체 일별 히스토리 CSV 저장 완료: {HISTORY_CSV_PATH}")
