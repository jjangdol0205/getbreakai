"""
backend/app/api/auth.py - Authentication and License API routes
"""
import hashlib
import hmac
import json
from typing import Optional
from fastapi import APIRouter, Header, HTTPException, Request, status

from backend.app.config import settings
from backend.app.models.auth import LicenseValidateRequest, LicenseValidateResponse
from backend.app.services.license_service import license_service

router = APIRouter()


@router.post("/license/validate", response_model=LicenseValidateResponse)
@router.post("/validate", response_model=LicenseValidateResponse, include_in_schema=False)
def validate_license(payload: LicenseValidateRequest):
    """
    Validates subscriber license key or demo bypass key (PRO-DEMO-2026).
    """
    return license_service.validate_key(
        license_key=payload.license_key,
        instance_name=payload.instance_name,
    )


@router.post("/webhook/lemonsqueezy")
async def lemonsqueezy_webhook(
    request: Request,
    x_signature: Optional[str] = Header(default=None, alias="X-Signature"),
):
    """
    Receives Lemon Squeezy order_created / license_key_created / subscription_created webhooks,
    verifies X-Signature when LEMON_SQUEEZY_WEBHOOK_SECRET is configured, and registers license keys.
    """
    raw_body = await request.body()

    if settings.LEMON_SQUEEZY_WEBHOOK_SECRET:
        if not x_signature:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Missing X-Signature webhook header",
            )
        digest = hmac.new(
            settings.LEMON_SQUEEZY_WEBHOOK_SECRET.encode("utf-8"),
            raw_body,
            hashlib.sha256,
        ).hexdigest()
        if not hmac.compare_digest(digest, x_signature.strip()):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid Lemon Squeezy webhook signature",
            )

    try:
        payload = json.loads(raw_body.decode("utf-8")) if raw_body else {}
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid JSON webhook body",
        )

    meta = payload.get("meta") or {}
    event_name = meta.get("event_name", "unknown")
    data_obj = payload.get("data") or {}
    attributes = data_obj.get("attributes") or {}

    extracted_key = (
        attributes.get("key")
        or attributes.get("license_key")
        or (meta.get("custom_data") or {}).get("license_key")
        or payload.get("license_key")
    )

    if isinstance(extracted_key, str) and extracted_key.strip():
        license_service.register_key(extracted_key.strip())
        return {
            "status": "ok",
            "event": event_name,
            "registered": True,
            "license_key": extracted_key.strip().upper(),
        }

    return {"status": "ok", "event": event_name, "registered": False}
