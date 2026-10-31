"""
SK하이닉스(000660) & SK스퀘어(402340) [조선업 패러다임 유사성 & 2030 중국(CXMT/YMTC) 침투 후폭풍 반영 적정 밸류에이션 모델]
"""
import sys
import json
from datetime import datetime
import requests
import urllib3
import pandas as pd
import numpy as np

sys.stdout.reconfigure(encoding="utf-8")
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
headers = {"User-Agent": "Mozilla/5.0"}

# 1. Fetch Korean Shipbuilding vs Memory 20-year historical milestones
tickers = {
    "009540.KS": "HD한국조선해양",
    "010140.KS": "삼성중공업",
    "042660.KS": "한화오션",
    "000660.KS": "SK하이닉스",
    "005930.KS": "삼성전자",
    "402340.KS": "SK스퀘어",
}

hist_summary = {}
for tkr, name in tickers.items():
    u = f"https://query1.finance.yahoo.com/v8/finance/chart/{tkr}?range=20y&interval=1mo"
    r = requests.get(u, headers=headers, verify=False, timeout=8).json()["chart"]["result"][0]
    ts = r["timestamp"]
    q = r["indicators"]["quote"][0]
    df = pd.DataFrame({
        "Date": [datetime.fromtimestamp(x).strftime("%Y-%m") for x in ts],
        "Close": q["close"],
        "High": q["high"],
        "Low": q["low"],
    }).dropna(subset=["Close"]).reset_index(drop=True)

    # Era 1: 2006-2008 Supercycle Peak
    df_2007 = df[df["Date"] <= "2008-12"]
    peak_2007 = float(df_2007["High"].max()) if not df_2007.empty else None
    peak_2007_date = df_2007.loc[df_2007["High"].idxmax(), "Date"] if not df_2007.empty else None

    # Era 2: 2015-2020 China Overcapacity Trough
    df_trough = df[(df["Date"] >= "2014-01") & (df["Date"] <= "2020-12")]
    trough_2015_20 = float(df_trough["Low"].min()) if not df_trough.empty else None
    trough_date = df_trough.loc[df_trough["Low"].idxmin(), "Date"] if not df_trough.empty else None

    # Era 3: 2025-2026 High-Value-Added Re-rating Peak & Current (2026-10)
    df_recent = df[df["Date"] >= "2025-01"]
    peak_recent = float(df_recent["High"].max()) if not df_recent.empty else None
    peak_recent_date = df_recent.loc[df_recent["High"].idxmax(), "Date"] if not df_recent.empty else None
    current_close = float(df["Close"].iloc[-1])
    dd_from_recent_peak = (current_close / peak_recent - 1.0) * 100.0 if peak_recent else 0.0

    hist_summary[name] = {
        "ticker": tkr,
        "peak_2007": peak_2007,
        "peak_2007_date": peak_2007_date,
        "trough_2015_20": trough_2015_20,
        "trough_date": trough_date,
        "peak_2025_26": peak_recent,
        "peak_2025_26_date": peak_recent_date,
        "current_2026_10": current_close,
        "dd_from_2025_26_peak_pct": round(dd_from_recent_peak, 2),
    }

print("=== [1] 조선업(2007 호황 -> 중국 벌크 침공 침체 -> 2025-26 고부가 LNG 부활) vs 반도체 시계열 비교 ===")
for k, v in hist_summary.items():
    p07 = f"{v['peak_2007']:,.0f}원({v['peak_2007_date']})" if v["peak_2007"] else "N/A"
    tr = f"{v['trough_2015_20']:,.0f}원({v['trough_date']})" if v["trough_2015_20"] else "N/A"
    p26 = f"{v['peak_2025_26']:,.0f}원({v['peak_2025_26_date']})" if v["peak_2025_26"] else "N/A"
    print(f" * {k:10s} | 07고점: {p07:20s} | 15-20저점: {tr:20s} | 25-26고점: {p26:22s} | 현재: {v['current_2026_10']:,.0f}원 ({v['dd_from_2025_26_peak_pct']:+.1f}%)")

# 2. Global Memory TAM & China (CXMT/YMTC) Crowding-Out Simulation (2025 -> 2030)
# Segments:
#   S1: Frontier AI & Hyperscale Data Center (HBM3E/4/5, Custom CXL, High-Density eSSD, 128GB+ Server DDR5)
#   S2: China Domestic Standard Memory (PC, Smartphone, Consumer, Local Cloud/Auto)
#   S3: Rest of World (Emerging Markets / Global South + Non-Big-Tech Consumer/Industrial OEMs)
tam_simulation = [
    {
        "year": 2025,
        "global_bit_share_china_pct": 11.5,
        "global_bit_share_korea_pct": 66.0,
        "china_share_in_S2_china_domestic_pct": 28.0,
        "china_share_in_S3_emerging_oem_pct": 8.0,
        "china_share_in_S1_frontier_ai_pct": 1.0,
        "frontier_ai_share_of_global_profit_pool_pct": 52.0,
        "hynix_share_of_global_profit_pool_pct": 38.0,
    },
    {
        "year": 2026,
        "global_bit_share_china_pct": 16.5,
        "global_bit_share_korea_pct": 61.5,
        "china_share_in_S2_china_domestic_pct": 45.0,
        "china_share_in_S3_emerging_oem_pct": 16.0,
        "china_share_in_S1_frontier_ai_pct": 2.0,
        "frontier_ai_share_of_global_profit_pool_pct": 64.0,
        "hynix_share_of_global_profit_pool_pct": 44.0,
    },
    {
        "year": 2027,
        "global_bit_share_china_pct": 22.0,
        "global_bit_share_korea_pct": 56.5,
        "china_share_in_S2_china_domestic_pct": 60.0,
        "china_share_in_S3_emerging_oem_pct": 28.0,
        "china_share_in_S1_frontier_ai_pct": 3.0,
        "frontier_ai_share_of_global_profit_pool_pct": 70.0,
        "hynix_share_of_global_profit_pool_pct": 46.5,
    },
    {
        "year": 2028,  # Cyclical Digestion + China Legacy Flood Year ("Aftermath Test")
        "global_bit_share_china_pct": 28.5,
        "global_bit_share_korea_pct": 51.0,
        "china_share_in_S2_china_domestic_pct": 72.0,
        "china_share_in_S3_emerging_oem_pct": 38.0,
        "china_share_in_S1_frontier_ai_pct": 4.0,
        "frontier_ai_share_of_global_profit_pool_pct": 76.0,
        "hynix_share_of_global_profit_pool_pct": 48.0,
    },
    {
        "year": 2030,  # Mature "Shipbuilding Equilibrium" (China owns Bulk/Legacy, Korea owns LNG/HBM5)
        "global_bit_share_china_pct": 34.0,
        "global_bit_share_korea_pct": 46.5,
        "china_share_in_S2_china_domestic_pct": 82.0,
        "china_share_in_S3_emerging_oem_pct": 48.0,
        "china_share_in_S1_frontier_ai_pct": 5.5,
        "frontier_ai_share_of_global_profit_pool_pct": 78.0,
        "hynix_share_of_global_profit_pool_pct": 47.5,
    },
]

print("\n=== [2] 2025~2030 중국(CXMT/YMTC) 레거시 장악 및 조선업형 양극화 시뮬레이션 ===")
print(pd.DataFrame(tam_simulation).to_string(index=False))

# 3. SK Hynix (000660) & SK Square (402340) SOTP & Cycle-Adjusted Valuation Matrix
# Current baseline (2026-10-15 close):
#   SK Hynix: 1,256,000 KRW (Market Cap ~917.5T KRW, 730.49M shares -> post-40T burn ~706.42M shares)
#   SK Square: 758,000 KRW (Market Cap ~100.0T KRW, 131.9M shares -> post-buyback ~128.0M shares)
#   Naver 12M Forward Consensus for Hynix: EPS 353,888 KRW (Net Income ~258.5T KRW, OP ~330T-396T KRW), BPS 368,998 KRW (2027E BPS ~650,000 KRW)

hynix_shares_post_burn = 706_420_000  # 7.064억 주 (2,407만 주 소각 후)
square_shares = 131_920_000           # 현재 약 1.319억 주 (향후 자사주 소각 시 1.25억 주)
square_stake_post_burn = 0.2076       # 20.76%
square_non_hynix_nav_trillion = 22.0  # 솔리다임 지분가치/보유현금/비상장 포트폴리오 보수적 순가치 (조 원)

# Define 4 Valuation Regimes under the "Shipbuilding + China Aftermath" Thesis:
regimes = [
    {
        "regime_id": "R1_EXTREME_PANIC_FLOOR",
        "name": "① 극단적 공포 하단 (2008·2015 조선업 패닉 / 중국발 다운사이클 선반영 바닥)",
        "desc": "시장이 2026~27 호실적을 완전히 무시하고, 중국 CXMT/YMTC 공급과잉과 AI 투자 둔화로 하이닉스 이익이 Peak 대비 반토막(연 순이익 140조) 난다고 가정한 뒤 시클리컬 최저 멀티플(PER 4.5x / 27E PBR 1.35x)을 적용한 절대 락바텀(Rock-Bottom)",
        "commodity_net_inc_trillion": 15.0,
        "commodity_per": 3.0,
        "ai_hbm_net_inc_trillion": 125.0,
        "ai_hbm_per": 4.7,
        "square_target_nav_discount": 0.58,
    },
    {
        "regime_id": "R2_CONSERVATIVE_SHIPBUILDING_BASE",
        "name": "② 보수적 조선업형 균형가 (범용은 중국에 상실 + 고부가 HBM만 인정하는 후폭풍 반영 적정가)",
        "desc": "사용자 가설을 100% 반영한 핵심 기준점. 범용 D램/낸드는 중국(CXMT/YMTC)에 밀려 저마진 벌크선화(PER 3.5x)되고, 미국 투자자들의 '한국 부품주 할인'까지 반영해 AI HBM/eSSD 이익(순이익 175조)에도 빅테크(25x)가 아닌 조선 대장주/산업재 평균 멀티플(PER 7.0x)만 부여",
        "commodity_net_inc_trillion": 30.0,
        "commodity_per": 3.5,
        "ai_hbm_net_inc_trillion": 175.0,
        "ai_hbm_per": 7.0,
        "square_target_nav_discount": 0.48,
    },
    {
        "regime_id": "R3_HIGH_VALUE_LNG_RERATING",
        "name": "③ 고부가 독점 리레이팅 (HD한국조선해양식 신고가 모델: 2030 AI 장기호황 + 주주환원)",
        "desc": "중국이 벌크(레거시)를 가져가도 하이닉스가 HBM4/HBM5 및 맞춤형 베이스다이에서 50% 이익 점유율을 유지(AI 순이익 210조, PER 8.5x)하고, 범용은 감산/전환으로 현금흐름만 창출(순이익 40조, PER 4.0x)하며 자사주 소각·밸류업으로 스퀘어 할인율이 38%로 축소",
        "commodity_net_inc_trillion": 40.0,
        "commodity_per": 4.0,
        "ai_hbm_net_inc_trillion": 210.0,
        "ai_hbm_per": 8.5,
        "square_target_nav_discount": 0.38,
    },
    {
        "regime_id": "R4_CUSTOM_FOUNDRY_BULL",
        "name": "④ AI 커스텀 파운드리 격상 (2028 불황 방어 입증 + ADR/지배구조 개편 완성)",
        "desc": "2028~2030년에도 AI 추론/에이전트 서버 확대로 HBM이 TSMC급 필수재로 인정받아 AI 부문 PER 10.5x를 부여받고, 상법 개정/합병 압박으로 SK스퀘어 NAV 할인율이 28%까지 해소되는 강세 시나리오",
        "commodity_net_inc_trillion": 45.0,
        "commodity_per": 4.5,
        "ai_hbm_net_inc_trillion": 235.0,
        "ai_hbm_per": 10.5,
        "square_target_nav_discount": 0.28,
    },
]

results = []
for reg in regimes:
    comm_val = reg["commodity_net_inc_trillion"] * reg["commodity_per"]
    ai_val = reg["ai_hbm_net_inc_trillion"] * reg["ai_hbm_per"]
    total_hynix_mcap_trillion = comm_val + ai_val
    total_net_inc = reg["commodity_net_inc_trillion"] + reg["ai_hbm_net_inc_trillion"]
    blended_per = total_hynix_mcap_trillion / total_net_inc

    # Hynix price per share (using 706.42M shares post 40T burn)
    hynix_target_price = (total_hynix_mcap_trillion * 1e12) / hynix_shares_post_burn
    hynix_upside_pct = (hynix_target_price / 1_256_000.0 - 1.0) * 100.0

    # SK Square NAV & Target Price
    square_hynix_stake_val = total_hynix_mcap_trillion * square_stake_post_burn
    square_total_nav_trillion = square_hynix_stake_val + square_non_hynix_nav_trillion
    square_target_mcap_trillion = square_total_nav_trillion * (1.0 - reg["square_target_nav_discount"])
    square_target_price = (square_target_mcap_trillion * 1e12) / square_shares
    square_upside_pct = (square_target_price / 758_000.0 - 1.0) * 100.0
    square_vs_avg_cost_pct = (square_target_price / 1_090_000.0 - 1.0) * 100.0

    results.append({
        "시나리오": reg["name"],
        "범용(중국경쟁) 가치": f"{comm_val:.0f}조 (이익 {reg['commodity_net_inc_trillion']:.0f}조×{reg['commodity_per']}배)",
        "AI/HBM(초격차) 가치": f"{ai_val:.0f}조 (이익 {reg['ai_hbm_net_inc_trillion']:.0f}조×{reg['ai_hbm_per']}배)",
        "하이닉스 적정시총(합산PER)": f"{total_hynix_mcap_trillion:,.0f}조 (PER {blended_per:.2f}배)",
        "하이닉스 적정주가(현재대비)": f"{hynix_target_price:,.0f}원 ({hynix_upside_pct:+.1f}%)",
        "스퀘어 NAV할인율 가정": f"{reg['square_target_nav_discount']*100:.0f}%",
        "SK스퀘어 적정주가(현재대비)": f"{square_target_price:,.0f}원 ({square_upside_pct:+.1f}%)",
        "평단(109만) 대비 수익률": f"{square_vs_avg_cost_pct:+.1f}%",
    })

print("\n=== [3] 조선업식 양극화(중국 범용 잠식 + AI 고부가 독점) 반영 SOTP 적정 밸류에이션 매트릭스 ===")
res_df = pd.DataFrame(results)
for idx, row in res_df.iterrows():
    print(f"\n[{row['시나리오']}]")
    for col in res_df.columns[1:]:
        print(f"  - {col}: {row[col]}")

# Save structured output to JSON for reference
from pathlib import Path
with open(Path(__file__).resolve().parent / "data" / "shipbuilding_2030_valuation.json", "w", encoding="utf-8") as f:
    json.dump({"historical_comparison": hist_summary, "tam_simulation_2025_2030": tam_simulation, "valuation_regimes": results}, f, ensure_ascii=False, indent=2)
