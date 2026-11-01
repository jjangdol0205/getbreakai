"""
backend/app/config.py - Application configuration and settings
"""
import os
from pathlib import Path
from typing import List

# Resolve base directories
# config.py is in backend/app/ -> parent is backend/ -> parent.parent is project root
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# Load local .env file if present (git-ignored secrets)
_ENV_FILE = BASE_DIR / ".env"
if _ENV_FILE.exists():
    try:
        for _line in _ENV_FILE.read_text(encoding="utf-8").splitlines():
            _clean = _line.strip()
            if not _clean or _clean.startswith("#") or "=" not in _clean:
                continue
            _k, _v = _clean.split("=", 1)
            os.environ.setdefault(_k.strip(), _v.strip())
    except Exception:
        pass


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
        "https://getbreakai.com",
        "https://www.getbreakai.com",
        "https://truthofmarket.com",
        "https://www.truthofmarket.com",
        "https://jjangdol0205.github.io",
    ]
    # Regex allowing any localhost/127.0.0.1 port, production domains, and *.onrender.com
    CORS_ORIGIN_REGEX: str = (
        r"^https?://(localhost|127\.0\.0\.1)(:\d+)?$"
        r"|^https://([a-z0-9-]+\.)?(getbreakai\.com|truthofmarket\.com|onrender\.com|github\.io)$"
    )

    # Data Source File Paths
    # Points to workspace datasets in 4_퀀트백테스트_모닝PDF_연구소 (or legacy 관심종목_백업_20261030)
    _DEFAULT_DATA_ROOT: Path = (
        BASE_DIR / "관심종목_백업_20261030"
        if (BASE_DIR / "관심종목_백업_20261030").exists()
        else BASE_DIR.parent / "4_퀀트백테스트_모닝PDF_연구소"
    )
    DATA_ROOT: Path = Path(os.getenv("DATA_ROOT", str(_DEFAULT_DATA_ROOT)))
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
    LEMON_SQUEEZY_WEBHOOK_SECRET: str = os.getenv("LEMON_SQUEEZY_WEBHOOK_SECRET", "")

    # Admin Authentication (Salted SHA-256 hash in code; raw credentials only in git-ignored .env)
    ADMIN_USERNAME: str = os.getenv("ADMIN_USERNAME", "")
    ADMIN_PASSWORD: str = os.getenv("ADMIN_PASSWORD", "")
    ADMIN_CREDENTIALS_SHA256: str = os.getenv(
        "ADMIN_CREDENTIALS_SHA256",
        "4578349322b7fa9931023e0def82b9d0c19fa2c4fdab1f7d762142d8d78ef2fe",
    )

    # Referral Defaults (for M3)
    DEFAULT_TRADINGVIEW_AFF_ID: str = os.getenv("TRADINGVIEW_AFF_ID", "1173809")
    DEFAULT_SEEKINGALPHA_SOURCE: str = os.getenv("SEEKINGALPHA_SOURCE", "better_life333")
    DEFAULT_TRENDSPIDER_AFF_ID: str = os.getenv("TRENDSPIDER_AFF_ID", "rightside")

    # Telegram Bot & Alert Configuration
    TELEGRAM_BOT_TOKEN: str = os.getenv("TELEGRAM_BOT_TOKEN", "")
    TELEGRAM_CHAT_ID: str = os.getenv("TELEGRAM_CHAT_ID", "")
    TELEGRAM_CHANNEL_URL: str = os.getenv("TELEGRAM_CHANNEL_URL", "https://t.me/RightSideAlphaBot")
    TELEGRAM_CONFIG_PATH: Path = BASE_DIR / "data" / "telegram_config.json"


settings = Settings()
