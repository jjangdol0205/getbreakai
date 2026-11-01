#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generates:
1. flow_10_promo_shorts_board.html (1-click interactive Copy Board for 10 US Viral Promo Shorts)
2. FLOW_10_PROMO_SHORTS_GUIDE.md (Markdown reference guide)
"""
import shutil
import sys
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from scripts.merge_10_promo_shorts import EPISODES

KR_SUMMARIES = {
    1: (
        "반도체 새벽 2시 패닉셀 vs 공포지수 18 역발상 매집",
        "반도체가 20% 빠질 때마다 개미들은 바닥에서 패닉셀합니다. 지금 반도체 공포·탐욕 지수는 18점(극단적 공포)입니다. 26년 데이터상 평시 70:30에서 극단적 공포 때 80% SMH : 20% XLV로 비중을 확대한 전략이 나스닥을 압도했습니다.",
    ),
    2: (
        "-50% 반토막 주식 줍다가 지하실 가는 이유 (떨어지는 칼날)",
        "고점 대비 50% 빠진 주식이 싸 보여서 샀다가 거기서 또 40% 물린 적 있으시죠? 좌측 하락장에서 떨어지는 칼날을 잡으면 수년간 자금이 묶입니다. 월가 퀀트는 반드시 60일선을 거래량과 함께 돌파하는 우측 시동(Right-Side Ignition)만 노립니다.",
    ),
    3: (
        "월가 헤지펀드의 80:20 반도체·헬스케어 바벨 비밀",
        "상승장엔 반도체 100%가 천재 같지만, -35% 폭락장이 오면 멘탈이 무너집니다. 그래서 기관은 평시 70% SMH(반도체) + 30% XLV(헬스케어) 황금 바벨을 유지하다가, 공포지수 25 미만 폭락장에서만 XLV를 팔아 80% SMH를 헐값에 쓸어 담습니다.",
    ),
    4: (
        "내 계좌 물린 종목 3초 심폐소생술 (포지션 닥터)",
        "솔직히 지금 언젠가 오르겠지 하며 방치 중인 파란불 종목이 몇 개입니까? 희망고문은 전략이 아닙니다. 모든 기관 매매에는 -9% 칼손절과 55일 시간손절 원칙이 있습니다. 티커·매수가·보유일을 포지션 닥터에 넣고 3초 만에 수학적 판정을 받으세요.",
    ),
    5: (
        "기관들이 몰래 매집할 때 무조건 남기는 4가지 흔적",
        "월가 기관들이 턴어라운드 주식을 수백만 주 매집할 때 절대 숨기지 못하는 4가지 수학적 흔적이 있습니다: 매도 클라이맥스 통과, 저점 높아짐, 60일선 탈환, 그리고 10일 거래량 폭발입니다. PW-RSI 엔진이 미국 72개 핵심주에서 이 시동을 매일 포착합니다.",
    ),
    6: (
        "반도체 폭락장에서 SOXL 몰빵 계좌가 녹아내리는 이유",
        "엔비디아와 SMH가 신고가일 땐 모두가 반도체를 사랑하지만, 20% 조정 한 번에 레버리지 몰빵 계좌는 박살 납니다. 2000~2026년 26.8년 백테스트에서 SMH와 XLV를 바벨 리밸런싱한 계좌는 1만 달러를 200만 달러 이상으로 불렸습니다.",
    ),
    7: (
        "계좌를 조용히 죽이는 55일 데드머니(기회비용)의 저주",
        "계좌를 망치는 가장 무서운 적은 폭락이 아니라 안 오르고 옆으로 기는 데드머니(Dead Money)입니다. 본전 생각에 수개월간 횡보주에 묶여 있으면 시장의 진짜 주도주 시동을 전부 놓칩니다. 55거래일 동안 +8% 못 가면 즉시 교체하는 것이 규칙 2번입니다.",
    ),
    8: (
        "+100%(2배) 수익 찍고 다시 본전까지 반납하지 않는 법",
        "수익이 2배 찍혔던 종목을 욕심부려 끝까지 들고 있다가 수익을 다 날려본 적 있으신가요? 프로 트레이더는 +100% 도달 즉시 절반(50%)을 팔아 원금 100%를 회수하고, 남은 50%만 60일선 트레일링 스탑으로 공짜 러너(Free Runner)로 굴립니다.",
    ),
    9: (
        "CNBC 뉴스 보고 사면 이미 40% 늦는 이유 (텔레그램 봇)",
        "TV 뉴스 앵커가 반도체 주식을 사라고 말할 때쯤이면 기관들은 이미 40% 수익 구간입니다. 하루 6시간씩 차트를 볼 시간이 없다면 텔레그램에서 @SemifearGreedbot을 시작하세요. 버튼 하나로 공포탐욕 지수 18점과 우측시동 Top 5 타점이 1초 만에 도착합니다.",
    ),
    10: (
        "폭락장 첫날 현금 100% 몰빵하면 절대 안 되는 이유 (3분할 공식)",
        "기술주 하락장에서 개미들이 하는 최악의 실수는 첫 -5% 조정에 현금을 다 써버리는 것입니다. 스마트머니는 공포 진입 시 30%, 극단적 공포(25 미만) 시 40%, 우측 반등 확인 시 30%의 3트랜치(Tranche)로 투입합니다. 지금 내 현금 투입액을 계산해 보세요.",
    ),
}


def main() -> None:
    cards_html = []
    md_lines = [
        "# 🎬 US Viral Promo Shorts 10-Episode Google Flow Prompts & Script Pack",
        "",
        "- **Target**: US & Global Retail Traders (YouTube Shorts `@rightsidealpha` / Instagram Reels `@semifeargreed` / Telegram `@SemifearGreedbot`)",
        "- **How to Use**:",
        "  1. Open Google Flow (`https://labs.google/fx/tools/flow`) in **9:16 Portrait** mode.",
        "  2. Copy either **Shot 1 (Fast 1-Clip Mode)** or **Shots 1~3 (Full 3-Clip Mode)** for any episode below.",
        "  3. Download the generated `.mp4` clip(s) into your `Downloads` folder (or save as `ep01.mp4` / `ep01_shot1..3.mp4` in `3_AI영상_홍보_스튜디오/ai_shorts_output/flow_clips/`).",
        "  4. Tell Antigravity **\"1편 합쳐줘\"** (or run `python scripts/merge_10_promo_shorts.py --ep 1 --from-downloads`) — it automatically attaches **Shot 4 Live Website UI**, **Native US Voiceover**, **0.01s Word-by-Word Pop-up Subtitles**, and **Sub-Bass Punchline Audio**!",
        "",
    ]

    for ep_num, ep in EPISODES.items():
        kr_title, kr_desc = KR_SUMMARIES[ep_num]
        plat_badge = (
            "🧭 SemiFearGreed (truthofmarket.com)"
            if ep["platform"] == "semi"
            else "🚀 RightSideAlpha (getbreakai.com)"
        )
        badge_bg = "rgba(239,68,68,0.18)" if ep["platform"] == "semi" else "rgba(16,185,129,0.18)"
        badge_col = "#fca5a5" if ep["platform"] == "semi" else "#6ee7b7"

        p1, p2, p3 = ep["flow_prompts"]
        s1, s2, s3, s4 = ep["shot_scripts"]

        md_lines.extend(
            [
                "---",
                f"## 🎬 EP{ep_num:02d}: {ep['title']} ({kr_title})",
                f"- **Style**: {ep['style_tag']} | **Target**: {plat_badge}",
                f"- **Save Filename**: `ep{ep_num:02d}.mp4` (1-Clip Mode) or `ep{ep_num:02d}_shot1.mp4`, `ep{ep_num:02d}_shot2.mp4`, `ep{ep_num:02d}_shot3.mp4` (3-Clip Mode)",
                "",
                "### ⭐ Shot 1 Prompt (Main Hook / 1-Clip Fast Mode)",
                "```text",
                p1,
                "```",
                "### 🔹 Shot 2 Prompt (Conflict / Visual Metaphor)",
                "```text",
                p2,
                "```",
                "### 🔹 Shot 3 Prompt (Institutional Quant Solution)",
                "```text",
                p3,
                "```",
                "### 🎙️ Matched US Voiceover & Auto-Subtitle Script (+ Shot 4 Live UI)",
                f"1. **Shot 1**: \"{s1}\"",
                f"2. **Shot 2**: \"{s2}\"",
                f"3. **Shot 3**: \"{s3}\"",
                f"4. **Shot 4 (Auto Live UI)**: \"{s4}\"",
                f"- **한국어 요약**: {kr_desc}",
                "",
            ]
        )

        cards_html.append(
            f"""
    <div class="section">
      <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:8px; margin-bottom:10px;">
        <div>
          <span class="badge" style="background:{badge_bg}; color:{badge_col}; margin-bottom:4px;">{plat_badge} · {ep['style_tag']}</span>
          <h2 style="margin:4px 0 0; color:#fff;">🎬 EP{ep_num:02d}. {kr_title}</h2>
        </div>
        <span style="font-family:monospace; font-size:12.5px; color:#94a3b8; background:#080c14; padding:6px 10px; border-radius:8px; border:1px solid #1e293b;">
          저장 파일명: <b>ep{ep_num:02d}.mp4</b> (1컷) 또는 <b>ep{ep_num:02d}_shot1~3.mp4</b> (3컷)
        </span>
      </div>

      <p style="margin:0 0 12px; font-size:13.5px; color:#cbd5e1;">
        💡 <b>스토리 기획</b>: {kr_desc}
      </p>

      <div class="copy-box" style="border-color:rgba(56,189,248,0.45);">
        <div class="copy-label">
          <span style="color:#38bdf8;">⭐ [EP{ep_num:02d} — Shot 1 프롬프트] (초반 3초 훅 / 1클립 빠른 제작 시 이것만 생성!)</span>
          <button class="copy-btn" onclick="copyText('ep{ep_num}-p1', this)">📋 Shot 1 프롬프트 복사</button>
        </div>
        <pre id="ep{ep_num}-p1">{p1}</pre>
      </div>

      <div class="copy-box">
        <div class="copy-label">
          <span>🔹 [EP{ep_num:02d} — Shot 2 프롬프트] (갈등 심화 / 시각적 메타포 — 3클립 풀버전용)</span>
          <button class="copy-btn" onclick="copyText('ep{ep_num}-p2', this)">📋 Shot 2 프롬프트 복사</button>
        </div>
        <pre id="ep{ep_num}-p2">{p2}</pre>
      </div>

      <div class="copy-box">
        <div class="copy-label">
          <span>🔹 [EP{ep_num:02d} — Shot 3 프롬프트] (월가 퀀트 반전 솔루션 — 3클립 풀버전용)</span>
          <button class="copy-btn" onclick="copyText('ep{ep_num}-p3', this)">📋 Shot 3 프롬프트 복사</button>
        </div>
        <pre id="ep{ep_num}-p3">{p3}</pre>
      </div>

      <div class="copy-box" style="background:#060a12; border-color:#1e293b;">
        <div class="copy-label">
          <span style="color:#a7f3d0;">🎙️ 자동 입혀질 미국 원어민 성우 대본 & 단어별 팝업 자막 (Shot 4 라이브 사이트 UI 자동 결합)</span>
          <button class="copy-btn" style="background:#334155; color:#fff;" onclick="copyText('ep{ep_num}-vo', this)">📋 영문 대본 복사</button>
        </div>
        <pre id="ep{ep_num}-vo" style="font-size:12.5px; color:#94a3b8;">[Shot 1] {s1}
[Shot 2] {s2}
[Shot 3] {s3}
[Shot 4 - Live Website UI Auto-Attached] {s4}</pre>
      </div>
    </div>
"""
        )

    html_doc = f"""<!DOCTYPE html>
<html lang="ko">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Google Flow (Veo) 미국 바이럴 홍보 쇼츠 10편 프롬프트 1클릭 보드</title>
  <style>
    :root {{
      --bg: #0b0f17;
      --card: #131b2e;
      --border: #23304d;
      --accent: #10b981;
      --accent-blue: #38bdf8;
      --text: #f1f5f9;
      --muted: #94a3b8;
    }}
    * {{ box-sizing: border-box; }}
    body {{
      margin: 0;
      padding: 32px 20px 64px;
      font-family: -apple-system, BlinkMacSystemFont, "Pretendard", "Segoe UI", Roboto, sans-serif;
      background: var(--bg);
      color: var(--text);
      line-height: 1.55;
    }}
    .container {{ max-width: 980px; margin: 0 auto; }}
    .header {{
      background: linear-gradient(135deg, rgba(239,68,68,0.18), rgba(56,189,248,0.18), rgba(16,185,129,0.15));
      border: 1px solid var(--border);
      border-radius: 16px;
      padding: 24px 28px;
      margin-bottom: 24px;
    }}
    .badge {{
      display: inline-block;
      padding: 4px 10px;
      border-radius: 999px;
      font-size: 12px;
      font-weight: 700;
    }}
    h1 {{ margin: 6px 0 10px; font-size: 24px; }}
    h2 {{ font-size: 18px; margin: 0; }}
    .section {{
      background: var(--card);
      border: 1px solid var(--border);
      border-radius: 14px;
      padding: 20px 24px;
      margin-bottom: 20px;
    }}
    .studio-btn {{
      display: inline-block;
      text-decoration: none;
      background: #ef4444;
      color: #fff;
      font-weight: 700;
      font-size: 13.5px;
      padding: 10px 18px;
      border-radius: 8px;
      margin-right: 8px;
      margin-top: 8px;
    }}
    .copy-box {{
      background: #080c14;
      border: 1px solid #1e293b;
      border-radius: 10px;
      padding: 12px 15px;
      margin-top: 10px;
    }}
    .copy-label {{
      font-size: 12.5px;
      font-weight: 700;
      color: var(--muted);
      margin-bottom: 6px;
      display: flex;
      justify-content: space-between;
      align-items: center;
      gap: 8px;
    }}
    pre {{
      margin: 0;
      white-space: pre-wrap;
      word-break: break-word;
      font-family: "JetBrains Mono", Consolas, monospace;
      font-size: 13px;
      color: #e2e8f0;
    }}
    button.copy-btn {{
      background: var(--accent);
      color: #04130d;
      border: none;
      border-radius: 8px;
      padding: 6px 14px;
      font-size: 12px;
      font-weight: 700;
      cursor: pointer;
      white-space: nowrap;
    }}
    button.copy-btn.copied {{ background: #0284c7; color: #fff; }}
  </style>
</head>
<body>
  <div class="container">
    <div class="header">
      <span class="badge" style="background:rgba(56,189,248,0.2); color:#38bdf8;">GOOGLE FLOW (VEO) 9:16 PORTRAIT · 10 VIRAL US SHORTS PACK</span>
      <h1>🎬 미국 인기 바이럴 쇼츠 스타일 홍보 프롬프트 10편 (1클릭 복사 보드)</h1>
      <p style="margin:0 0 10px; color:#cbd5e1; font-size:14px;">
        1️⃣ 아래에서 원하는 에피소드(EP01~EP10)의 <b>프롬프트를 1클릭 복사</b>하여 <b>Google Flow (9:16 세로 모드)</b>에서 영상을 생성·다운로드하세요.<br/>
        2️⃣ <b>빠른 제작(편당 1클립)</b>은 <code>⭐ Shot 1 프롬프트</code>만 만드셔도 되고, <b>풀 시네마틱(편당 3클립)</b>은 <code>Shot 1~3</code>을 만드시면 됩니다.<br/>
        3️⃣ 다운로드만 받으신 뒤 채팅창에 <b>"1편 합쳐줘"</b> (또는 <b>"다운받은거 합쳐줘"</b>)라고 말씀만 하시면, <b>실제 홈페이지 라이브 UI(Shot 4) + 미국 원어민 성우 + 0.01초 단어별 팝업 자막 + 서브베이스 음향</b>까지 자동으로 합쳐서 완성본 MP4를 만들어 드립니다!
      </p>
      <a class="studio-btn" href="https://labs.google/fx/tools/flow" target="_blank">🚀 Google Flow (labs.google/fx/tools/flow) 열기 ↗</a>
      <a class="studio-btn" style="background:#0284c7;" href="./instagram_us_setup.html" target="_blank">🧭 유튜브 스튜디오 & 인스타 프로필 세팅 보드 ↗</a>
    </div>
    {"".join(cards_html)}
  </div>
  <script>
    function copyText(id, btn) {{
      const text = document.getElementById(id).innerText;
      navigator.clipboard.writeText(text).then(() => {{
        const orig = btn.innerText;
        btn.innerText = '✅ 복사 완료!';
        btn.classList.add('copied');
        setTimeout(() => {{
          btn.innerText = orig;
          btn.classList.remove('copied');
        }}, 1500);
      }});
    }}
  </script>
</body>
</html>"""

    out_html = ROOT_DIR / "flow_10_promo_shorts_board.html"
    out_md = ROOT_DIR / "FLOW_10_PROMO_SHORTS_GUIDE.md"
    out_html.write_text(html_doc, encoding="utf-8")
    out_md.write_text("\n".join(md_lines), encoding="utf-8")

    for target_dir in [ROOT_DIR / "frontend" / "public", ROOT_DIR / "dist"]:
        if target_dir.exists():
            shutil.copy2(out_html, target_dir / "flow_10_promo_shorts_board.html")

    print("Generated:", out_html, out_md)


if __name__ == "__main__":
    main()
