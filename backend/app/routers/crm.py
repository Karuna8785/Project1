from app.dependencies import get_current_user
from app.models.user import User
from fastapi import APIRouter, Depends

router = APIRouter(prefix="/crm", tags=["CRM (Member 3)"])

@router.get("/summary")
def get_crm_summary(current_user: User = Depends(get_current_user)):
    return {
        "module": "CRM",
        "developer": "Member 3",
        "active_customers": 124,
        "open_leads": 19,
        "conversion_rate": 28.5,
        "status": "Operational"
    }
