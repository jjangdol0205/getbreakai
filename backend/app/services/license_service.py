"""
backend/app/services/license_service.py - Lemon Squeezy and Demo License Key Validator
"""
from typing import Optional
from backend.app.config import settings
from backend.app.models.auth import LicenseValidateResponse


class LicenseService:
    """Service validating paid subscriber licenses and local demo keys."""

    def __init__(self):
        self.demo_key = settings.DEMO_LICENSE_KEY.strip().upper()

    def validate_key(
        self, license_key: str, instance_name: Optional[str] = None
    ) -> LicenseValidateResponse:
        """
        Validates a license key.
        - Supports instant verification for demo key PRO-DEMO-2026 (case-insensitive).
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

        # Check demo bypass key
        if trimmed_key.upper() == self.demo_key:
            return LicenseValidateResponse(
                valid=True,
                tier="pro",
                license_key="PRO-DEMO-2026",
                expires_at="2099-12-31T23:59:59Z",
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

        # Lemon Squeezy integration hook if API key is provided
        if settings.LEMON_SQUEEZY_API_KEY:
            # Lemon Squeezy API call could be implemented here
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
        return license_key.strip().upper() == self.demo_key


license_service = LicenseService()
