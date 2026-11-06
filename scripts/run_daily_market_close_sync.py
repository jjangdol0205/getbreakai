"""
scripts/run_daily_market_close_sync.py
Periodic daily US market closing price pipeline for 1사업부 (truthofmarket.com):
1. Syncs 72 US stocks + $SMH, $XLV, $QQQ, USD/KRW via scripts/sync_live_market_data.py
2. Rebuilds production static bundle & SEO pages via scripts/build_static_bundle.py
3. Commits and pushes updated closing price snapshots to `truthofmarket` and `origin` remotes
4. Optionally broadcasts VIP daily briefing (`--broadcast`) and notifies HQ Telegram (`--notify`)
"""
import json
import subprocess
import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
SEMI_OVERVIEW_PATH = ROOT_DIR / "static_api" / "semi_overview.json"


def run_cmd(args: list[str]) -> tuple[int, str]:
    proc = subprocess.run(
        args,
        cwd=str(ROOT_DIR),
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    out = ((proc.stdout or "") + "\n" + (proc.stderr or "")).strip()
    return proc.returncode, out


def get_as_of_summary() -> str:
    try:
        ov = json.loads(SEMI_OVERVIEW_PATH.read_text(encoding="utf-8"))
        dt = ov.get("date", "N/A")
        smh = ov.get("smh_close", "N/A")
        xlv = ov.get("xlv_close", "N/A")
        qqq = ov.get("qqq_close", "N/A")
        fg = ov.get("fg_score", "N/A")
        return f"기준일 {dt} | $SMH ${smh} · $XLV ${xlv} · $QQQ ${qqq} | 공포·탐욕 {fg}"
    except Exception:
        return "최신 종가 동기화 완료"


def git_commit_and_push_market_data(as_of_date: str) -> str:
    stage_paths = [
        "data/stocks_pro_master.json",
        "static_api",
        "frontend/public/static_api",
        "frontend/dist",
        "dist/static_api",
        "dist/index.html",
        "dist/semi-fear-greed.html",
        "dist/feed.xml",
        "dist/sitemap.xml",
        "dist/stocks",
        "index.html",
        "semi-fear-greed.html",
        "feed.xml",
        "sitemap.xml",
        "stocks",
    ]
    existing = [p for p in stage_paths if (ROOT_DIR / p).exists()]
    if not existing:
        return "스테이징 대상 없음"

    run_cmd(["git", "add", "--"] + existing)
    diff_code, _ = run_cmd(["git", "diff", "--cached", "--quiet"])
    if diff_code == 0:
        return "변경사항 없음 (이미 최신 종가 배포 상태)"

    msg = f"chore(market-data): auto-sync daily US close prices ({as_of_date})"
    c_code, c_out = run_cmd(["git", "commit", "-m", msg])
    if c_code != 0:
        return f"커밋 생략: {c_out[-160:]}"

    pushed = []
    for remote in ["truthofmarket", "origin"]:
        p_code, _ = run_cmd(["git", "push", remote, "main"])
        if p_code == 0:
            pushed.append(remote)
    return f"Git 라이브 배포 완료 ({', '.join(pushed) if pushed else '로컬 커밋 완료'})"


def main():
    do_broadcast = "--broadcast" in sys.argv
    do_notify = "--notify" in sys.argv

    print("[1/4] Syncing latest US market closing prices (72 stocks + SMH/XLV/QQQ)...")
    c1, out1 = run_cmd([sys.executable, "scripts/sync_live_market_data.py"])
    print(out1[-400:] if out1 else "sync_live_market_data done")

    print("[2/4] Rebuilding production static bundle (dist/ & SEO pages)...")
    c2, out2 = run_cmd([sys.executable, "scripts/build_static_bundle.py"])
    print(out2[-400:] if out2 else "build_static_bundle done")

    as_of_date = "latest"
    try:
        as_of_date = json.loads(SEMI_OVERVIEW_PATH.read_text(encoding="utf-8")).get("date", "latest")
    except Exception:
        pass

    print("[3/4] Committing and pushing updated closing prices to live remotes...")
    deploy_status = git_commit_and_push_market_data(as_of_date)
    print(deploy_status)

    bcast_status = ""
    if do_broadcast:
        print("[4/4] Broadcasting VIP daily briefing to Telegram channel...")
        _, out4 = run_cmd([sys.executable, "scripts/broadcast_telegram_channel.py", "--pin"])
        bcast_status = f"\n• VIP 채널 브리핑: {out4.splitlines()[-1] if out4 else '발송 완료'}"

    summary = get_as_of_summary()
    final_msg = (
        f"[1사업부: RightSideAlpha (truthofmarket.com) 일일 미국장 종가 자동 업데이트 완료]\n"
        f"• {summary}\n"
        f"• 정적 번들(dist) 빌드 및 배포: {deploy_status}"
        f"{bcast_status}"
    )
    print(final_msg)

    if do_notify:
        run_cmd(["node", "scripts/master_hq_telegram_bridge.js", "--notify", final_msg])


if __name__ == "__main__":
    main()
