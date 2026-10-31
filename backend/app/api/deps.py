"""
backend/app/api/deps.py - Shared API dependencies and authentication resolution
"""
from typing import Optional
from fastapi import Header, Query, HTTPException, status, Depends

from backend.app.services.license_service import license_service


def get_is_pro(
    authorization: Optional[str] = Header(None),
    license_key: Optional[str] = Query(None),
) -> bool:
    """
    Extracts license key from Authorization Bearer token or license_key query param.
    Instantly unlocks Pro for verified Pro license keys (such as PRO-DEMO-2026).
    """
    key: Optional[str] = None

    if authorization:
        parts = authorization.strip().split(" ", 1)
        if len(parts) == 2 and parts[0].lower() == "bearer":
            key = parts[1].strip()
        else:
            # Malformed auth header (e.g. Basic ... or without Bearer)
            return False
    elif license_key:
        key = license_key.strip()

    if not key:
        return False

    return license_service.is_valid_pro_key(key)


def require_pro(is_pro: bool = Depends(get_is_pro)) -> bool:
    """
    FastAPI dependency enforcing verified Pro subscription.
    Raises 401 Unauthorized if request does not contain a valid Pro token.
    """
    if not is_pro:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Unauthorized: Pro subscription required",
        )
    return True
