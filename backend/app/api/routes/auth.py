"""
SmartERP - Auth Routes Stub
Member 1 owns this file. Placeholder only.
DO NOT implement anything here — Member 1 will replace this.
"""
from fastapi import APIRouter

router = APIRouter(prefix="/auth", tags=["Authentication (Member 1)"])


@router.get("/status")
def auth_status():
    """Placeholder — Member 1 implements the real auth endpoints."""
    return {"module": "Authentication", "owner": "Member 1", "status": "pending_integration"}
