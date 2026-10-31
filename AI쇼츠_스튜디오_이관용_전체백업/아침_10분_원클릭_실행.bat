@echo off
chcp 65001 >nul
cd /d "%~dp0"
echo ============================================================================
echo [RightSideAlpha ^& SemiFearGreed] 오늘 아침 최신 데이터 동기화 및 10분 조종석 실행 중...
echo ============================================================================
python "%~dp0global_marketing_sniper.py" --open
exit
