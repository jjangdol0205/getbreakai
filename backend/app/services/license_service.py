"""
backend/app/services/license_service.py - Lemon Squeezy and Demo License Key Validator
"""
import os
import re
from typing import Optional
import httpx

from backend.app.config import settings
from backend.app.models.auth import LicenseValidateResponse

RSA_LIVE_KEY_PATTERN = re.compile(r"^RSA-(PRO|LTD)-2026-[A-Z0-9]{4,12}$")
UUID_KEY_PATTERN = re.compile(
    r"^[0-9A-F]{8}-[0-9A-F]{4}-[0-9A-F]{4}-[0-9A-F]{4}-[0-9A-F]{12}$"
)


class LicenseService:
    """Service validating paid subscriber licenses and local demo keys."""

    def __init__(self):
        self.demo_key = settings.DEMO_LICENSE_KEY.strip().upper()
        self._validated_keys: set[str] = {self.demo_key}
        extra = os.getenv("ADDITIONAL_PRO_KEYS", "")
        if extra:
            for k in extra.split(","):
                k_clean = k.strip().upper()
                if k_clean:
                    self._validated_keys.add(k_clean)

    def register_key(self, license_key: str) -> None:
        """Registers a verified license key (e.g., from Lemon Squeezy webhook)."""
        if license_key and license_key.strip():
            self._validated_keys.add(license_key.strip().upper())

    def validate_key(
        self, license_key: str, instance_name: Optional[str] = None
    ) -> LicenseValidateResponse:
        """
        Validates a license key.
        - Supports instant verification for demo key PRO-DEMO-2026 (case-insensitive).
        - Supports self-issued live activation keys (RSA-PRO-2026-XXXX / RSA-LTD-2026-XXXX).
        - Supports Lemon Squeezy License API validation when LEMON_SQUEEZY_API_KEY is configured.
        - Rejects empty, whitespace-only, or invalid keys safely.
        """
        if not license_key or not license_key.strip():
            return LicenseValidateResponse(
                valid=False,
                tier="free",
                license_key=license_key or "",
                message="License key cannot be empty",
            )

        trimmed_key = license_key.strip()
        clean_key = trimmed_key.upper()

        # Check demo bypass key
        if clean_key == self.demo_key:
            return LicenseValidateResponse(
                valid=True,
                tier="pro",
                license_key="PRO-DEMO-2026",
                expires_at="2027-12-31T23:59:59Z",
                message="Demo license key verified successfully",
            )

        # Basic format check - keys with invalid format or short length
        if len(trimmed_key) < 4:
            return LicenseValidateResponse(
                valid=False,
                tier="free",
                license_key=trimmed_key,
                message="Invalid license key length",
            )

        # Check self-issued live activation keys: RSA-PRO-2026-XXXX or RSA-LTD-2026-XXXX
        m_rsa = RSA_LIVE_KEY_PATTERN.match(clean_key)
        if m_rsa:
            self._validated_keys.add(clean_key)
            key_type = m_rsa.group(1)
            tier = "pro_lifetime" if key_type == "LTD" else "pro"
            expires_at = None if key_type == "LTD" else "2027-12-31T23:59:59Z"
            return LicenseValidateResponse(
                valid=True,
                tier=tier,
                license_key=clean_key,
                expires_at=expires_at,
                message="RightSideAlpha Pro license activated successfully",
            )

        # Check pre-registered or webhook-activated keys
        if clean_key in self._validated_keys:
            return LicenseValidateResponse(
                valid=True,
                tier="pro",
                license_key=clean_key,
                expires_at="2027-12-31T23:59:59Z",
                message="Pro license key verified successfully",
            )

        # Lemon Squeezy integration hook if API key is provided
        if settings.LEMON_SQUEEZY_API_KEY:
            try:
                payload = {"license_key": trimmed_key}
                if instance_name:
                    payload["instance_name"] = instance_name
                headers = {
                    "Accept": "application/json",
                    "Authorization": f"Bearer {settings.LEMON_SQUEEZY_API_KEY}",
                }
                with httpx.Client(timeout=4.0) as client:
                    resp = client.post(
                        "https://api.lemonsqueezy.com/v1/licenses/validate",
                        data=payload,
                        headers=headers,
                    )
                if resp.status_code == 200:
                    data = resp.json()
                    if data.get("valid") is True:
                        self._validated_keys.add(clean_key)
                        meta_key = data.get("license_key") or {}
                        expires_at = meta_key.get("expires_at")
                        return LicenseValidateResponse(
                            valid=True,
                            tier="pro",
                            license_key=clean_key,
                            expires_at=expires_at,
                            message="Lemon Squeezy license verified successfully",
                        )
            except Exception:
                pass

        return LicenseValidateResponse(
            valid=False,
            tier="free",
            license_key=trimmed_key,
            message="Invalid license key",
        )

    def is_valid_pro_key(self, license_key: Optional[str]) -> bool:
        """Quick boolean validation for authentication dependencies."""
        if not license_key or not license_key.strip():
            return False
        clean = license_key.strip().upper()
        if clean in self._validated_keys:
            return True
        if RSA_LIVE_KEY_PATTERN.match(clean):
            self._validated_keys.add(clean)
            return True
        return False


license_service = LicenseService()
