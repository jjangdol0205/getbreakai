"""
backend/app/services/referral_service.py - Referral Engine and Outbound Click Tracking Service
"""
import threading
from datetime import datetime, timezone
from typing import Dict, Any, Optional

from backend.app.config import settings
from backend.app.models.referral import ReferralConfig, ReferralClickStats


class ReferralService:
    """Manages partner affiliate links and in-memory click analytics."""

    VALID_PROVIDERS = {"tradingview", "seekingalpha", "trendspider", "broker", "exchange"}

    def __init__(self):
        self._lock = threading.Lock()
        self.config = ReferralConfig(
            tradingview_aff_id=settings.DEFAULT_TRADINGVIEW_AFF_ID,
            seekingalpha_source=settings.DEFAULT_SEEKINGALPHA_SOURCE,
            trendspider_aff_id=settings.DEFAULT_TRENDSPIDER_AFF_ID,
        )
        self.stats = ReferralClickStats()

    def get_config(self) -> ReferralConfig:
        with self._lock:
            return self.config.model_copy()

    def update_config(self, new_config: ReferralConfig) -> ReferralConfig:
        with self._lock:
            self.config = new_config.model_copy()
            return self.config.model_copy()

    def build_url(self, provider: str, ticker: Optional[str] = "SPY") -> str:
        prov = (provider or "").strip().lower()
        if prov not in self.VALID_PROVIDERS:
            raise ValueError(f"Unknown or unsupported referral provider: '{provider}'")

        tick = (ticker or "SPY").strip().upper()
        if not tick:
            tick = "SPY"

        with self._lock:
            cfg = self.config

        if prov == "tradingview":
            return f"https://www.tradingview.com/symbols/{tick}/?aff_id={cfg.tradingview_aff_id}"
        elif prov == "seekingalpha":
            return f"https://seekingalpha.com/symbol/{tick}/earnings?source={cfg.seekingalpha_source}"
        elif prov == "trendspider":
            return f"https://trendspider.com/?_go={cfg.trendspider_aff_id}&symbol={tick}"
        elif prov in ("broker", "exchange"):
            base_url = cfg.broker_referral_url or "https://www.bitget.com/referral/register?clacCode=7nja"
            sep = "&" if "?" in base_url else "?"
            return f"{base_url}{sep}symbol={tick}"
        else:
            raise ValueError(f"Provider '{provider}' not implemented")

    def record_click(self, provider: str, ticker: Optional[str] = "SPY") -> str:
        prov = (provider or "").strip().lower()
        if prov not in self.VALID_PROVIDERS:
            raise KeyError(f"Invalid referral provider: '{provider}'")

        tick = (ticker or "SPY").strip().upper()
        dest_url = self.build_url(prov, tick)

        with self._lock:
            self.stats.total += 1
            if prov == "tradingview":
                self.stats.tradingview += 1
            elif prov == "seekingalpha":
                self.stats.seekingalpha += 1
            elif prov == "trendspider":
                self.stats.trendspider += 1
            elif prov in ("broker", "exchange"):
                self.stats.broker += 1

            self.stats.last_clicked_at = datetime.now(timezone.utc).isoformat()
            self.stats.last_provider = prov
            self.stats.last_ticker = tick

        return dest_url

    def get_stats(self) -> Dict[str, Any]:
        with self._lock:
            return self.stats.model_dump()


referral_service = ReferralService()
