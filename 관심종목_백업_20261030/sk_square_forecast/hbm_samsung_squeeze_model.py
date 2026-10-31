"""
[적대적 팩트체크 반영 수정 모델]
중국(CXMT/YMTC)의 범용 잠식 + 삼성전자·마이크론의 HBM 점유율 추격(하이닉스 HBM 점유율 55% -> 38~43% 하락 및 마진율 축소)까지
동시에 반영한 '샌드위치 압박(Sandwich Squeeze)' 시나리오별 SK하이닉스 & SK스퀘어 적정 밸류에이션 재산출
"""
import sys
import json
import pandas as pd

sys.stdout.reconfigure(encoding="utf-8")

# 1. HBM Market Share & Operating Margin Trajectory (2024 -> 2030)
# Comparing Previous Optimistic Assumption vs Realistic Samsung/Micron Catch-up Fact
hbm_competition_trajectory = [
    {
        "year": "2024 (HBM3/3E 초기)",
        "hynix_hbm_share_pct": 58.0,
        "samsung_hbm_share_pct": 36.0,
        "micron_hbm_share_pct": 6.0,
        "hynix_hbm_opm_pct": 62.0,
        "note": "삼성 엔비디아 퀄 지연으로 하이닉스 사실상 독점기",
    },
    {
        "year": "2025 (HBM3E 8/12단)",
        "hynix_hbm_share_pct": 54.0,
        "samsung_hbm_share_pct": 37.0,
        "micron_hbm_share_pct": 9.0,
        "hynix_hbm_opm_pct": 60.0,
        "note": "마이크론 진입 개시, 하이닉스 12단 MR-MUF 수율 우위 유지",
    },
    {
        "year": "2026 (HBM3E 12단/HBM4 초기)",
        "hynix_hbm_share_pct": 49.0,
        "samsung_hbm_share_pct": 38.0,
        "micron_hbm_share_pct": 13.0,
        "hynix_hbm_opm_pct": 57.0,
        "note": "삼성 3Q HBM 출하 QoQ +50% 급증(골드만삭스), 마이크론 LTA 확대",
    },
    {
        "year": "2027E (HBM4 본게임)",
        "hynix_hbm_share_pct": 44.0,
        "samsung_hbm_share_pct": 40.0,
        "micron_hbm_share_pct": 16.0,
        "hynix_hbm_opm_pct": 50.0,
        "note": "번스타인 지적 구간: 삼성 HBM4(턴키 파운드리 활용) 추격으로 독점 프리미엄 축소",
    },
    {
        "year": "2028~2030E (HBM4E/HBM5 3강 균형)",
        "hynix_hbm_share_pct": 40.0,
        "samsung_hbm_share_pct": 42.0,
        "micron_hbm_share_pct": 18.0,
        "hynix_hbm_opm_pct": 42.0,
        "note": "삼성의 물량 공세로 점유율 4:4:2 수렴, 엔비디아 벤더 다변화로 마진율 정상화(60%->42%)",
    },
]

print("=== [1] HBM 3사 점유율 및 하이닉스 HBM 마진율 변화 (삼성·마이크론 추격 팩트 반영) ===")
print(pd.DataFrame(hbm_competition_trajectory).to_string(index=False))

# 2. Revised Valuation Matrix under "Sandwich Squeeze" (아래로는 중국 CXMT 범용 잠식 + 위로는 삼성 HBM 점유율 잠식)
hynix_shares = 706_420_000   # 40조 소각 후 7.064억 주
square_shares = 131_920_000  # 1.319억 주
square_stake = 0.2076        # 20.76%
square_other_nav = 20.0      # 솔리다임/현금 보수적 가치 20조 원

squeeze_scenarios = [
    {
        "case": "Case A. [최악의 샌드위치 (Bear)] 삼성에 HBM 1위 뺏기고(점유율 35%) + 중국에 범용 잠식 + AI 투자 둔화",
        "desc": "삼성이 HBM4/5를 완벽히 뚫어 하이닉스 점유율이 35%로 밀리고, 엔비디아가 단가를 후려쳐 하이닉스 연간 순이익이 현재 추정치(258조)의 절반 이하인 115조 원(범용 15조 + HBM 100조)으로 급감하며 멀티플도 PER 5.0배에 갇히는 시나리오",
        "comm_ni": 15.0,
        "comm_per": 3.0,
        "hbm_ni": 100.0,
        "hbm_per": 5.3,
        "sq_disc": 0.55,
    },
    {
        "case": "Case B. [현실적 점유율 하락 반영 균형가 (Base-Conservative)] 하이닉스 HBM 점유율 54%→40% 하락 & 마진 축소",
        "desc": "사용자님의 지적을 그대로 반영: 삼성이 HBM 점유율을 40~42%까지 뺏어가서 하이닉스 HBM 점유율이 40%로 내려오고 마진율도 60%->42%로 깎이지만, 전체 AI HBM 시장 파이 자체가 2030년까지 커져서 하이닉스 중기 순이익이 160조 원(범용 25조 + HBM 135조) 수준에서 유지되고 합산 PER 6.0배를 받는 경우",
        "comm_ni": 25.0,
        "comm_per": 3.5,
        "hbm_ni": 135.0,
        "hbm_per": 6.5,
        "sq_disc": 0.48,
    },
    {
        "case": "Case C. [파이 확장 상쇄 시나리오 (Base-Bull)] 점유율은 43%로 줄어도 커스텀 HBM4 수율 우위로 이익 방어",
        "desc": "삼성이 일반 HBM 점유율을 뺏어가더라도, TSMC CoWoS와 직결된 최고난도 커스텀 HBM4 16단에서는 하이닉스가 수율 우위를 지켜 순이익 195조 원(범용 30조 + HBM 165조)을 방어하고 합산 PER 7.2배, 스퀘어 할인율 40%를 적용받는 경우",
        "comm_ni": 30.0,
        "comm_per": 4.0,
        "hbm_ni": 165.0,
        "hbm_per": 7.8,
        "sq_disc": 0.40,
    },
]

rows = []
for sc in squeeze_scenarios:
    hynix_mcap = sc["comm_ni"] * sc["comm_per"] + sc["hbm_ni"] * sc["hbm_per"]
    tot_ni = sc["comm_ni"] + sc["hbm_ni"]
    blended_per = hynix_mcap / tot_ni
    hynix_p = (hynix_mcap * 1e12) / hynix_shares
    hynix_chg = (hynix_p / 1_256_000.0 - 1.0) * 100.0

    sq_nav = hynix_mcap * square_stake + square_other_nav
    sq_mcap = sq_nav * (1.0 - sc["sq_disc"])
    sq_p = (sq_mcap * 1e12) / square_shares
    sq_chg = (sq_p / 758_000.0 - 1.0) * 100.0
    sq_vs_avg = (sq_p / 1_090_000.0 - 1.0) * 100.0

    rows.append({
        "시나리오": sc["case"],
        "추정 중기 순이익(258조 대비)": f"{tot_ni:.0f}조 원 ({(tot_ni/258.5 - 1)*100:+.1f}%)",
        "적용 합산 PER": f"{blended_per:.2f}배",
        "하이닉스 적정시총": f"{hynix_mcap:,.0f}조 원",
        "하이닉스 적정주가": f"{hynix_p:,.0f}원 ({hynix_chg:+.1f}%)",
        "스퀘어 할인율": f"{sc['sq_disc']*100:.0f}%",
        "SK스퀘어 적정주가": f"{sq_p:,.0f}원 ({sq_chg:+.1f}%)",
        "내 평단(109만) 대비": f"{sq_vs_avg:+.1f}%",
    })

print("\n=== [2] 삼성의 HBM 점유율 잠식까지 반영한 '샌드위치 압박' 적정주가 재산출 결과 ===")
for r in rows:
    print(f"\n[{r['시나리오']}]")
    for k, v in r.items():
        if k != "시나리오":
            print(f"  - {k}: {v}")

from pathlib import Path
with open(Path(__file__).resolve().parent / "data" / "hbm_samsung_squeeze_valuation.json", "w", encoding="utf-8") as f:
    json.dump({"hbm_trajectory": hbm_competition_trajectory, "squeeze_valuation": rows}, f, ensure_ascii=False, indent=2)
