"""
backend/app/api/auth.py - Authentication and License API routes
"""
from fastapi import APIRouter
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
