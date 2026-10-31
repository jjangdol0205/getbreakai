"""
backend/app/config.py - Application configuration and settings
"""
import os
from pathlib import Path
from typing import List

# Resolve base directories
# config.py is in backend/app/ -> parent is backend/ -> parent.parent is project root (d:\투자홈페이지)
BASE_DIR = Path(__file__).resolve().parent.parent.parent


class Settings:
    # Environment & Server
    BASE_DIR: Path = BASE_DIR
    APP_NAME: str = "RightSideAlpha API"
    APP_VERSION: str = "1.0.0"
    ENV: str = os.getenv("APP_ENV", "development")
    DEBUG: bool = os.getenv("DEBUG", "true").lower() in ("true", "1", "yes")
    HOST: str = os.getenv("HOST", "127.0.0.1")
    PORT: int = int(os.getenv("PORT", "8000"))

    # CORS Origins for Frontend Integration
    CORS_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:8000",
        "http://127.0.0.1:8000",
    ]
    # Regex allowing any localhost or 127.0.0.1 port with credentials
    CORS_ORIGIN_REGEX: str = r"^https?://(localhost|127\.0\.0\.1)(:\d+)?$"

    # Data Source File Paths
    # Points to workspace datasets in 관심종목_백업_20261030
    DATA_ROOT: Path = Path(os.getenv("DATA_ROOT", str(BASE_DIR / "관심종목_백업_20261030")))
    STOCKS_DATA_PATH: Path = DATA_ROOT / "all_100_stocks_screened.json"
    BACKTEST_DATA_PATH: Path = DATA_ROOT / "pw_rsi_2000_2026_backtest.json"
    WEEKLY_PICKS_DIR: Path = DATA_ROOT / "weekly_picks"
    SEMI_HISTORY_CSV_PATH: Path = DATA_ROOT / "smh_xlv_fear_greed_history.csv"
    SEMI_ETF_DATA_DIR: Path = DATA_ROOT / "data"

    # Aliases for compatibility
    STOCKS_JSON_PATH: Path = STOCKS_DATA_PATH
    BACKTEST_JSON_PATH: Path = BACKTEST_DATA_PATH

    # Static Assets Directory (for M4 unified static mounting)
    STATIC_DIR: Path = Path(os.getenv("STATIC_DIR", str(BASE_DIR / "frontend" / "dist")))

    # Demo & Monetization Config
    DEMO_LICENSE_KEY: str = "PRO-DEMO-2026"
    LEMON_SQUEEZY_API_KEY: str = os.getenv("LEMON_SQUEEZY_API_KEY", "")
    LEMON_SQUEEZY_STORE_ID: str = os.getenv("LEMON_SQUEEZY_STORE_ID", "")

    # Referral Defaults (for M3)
    DEFAULT_TRADINGVIEW_AFF_ID: str = os.getenv("TRADINGVIEW_AFF_ID", "rightsidealpha")
    DEFAULT_SEEKINGALPHA_SOURCE: str = os.getenv("SEEKINGALPHA_SOURCE", "affiliate_rightside")
    DEFAULT_TRENDSPIDER_AFF_ID: str = os.getenv("TRENDSPIDER_AFF_ID", "rightside")


settings = Settings()
