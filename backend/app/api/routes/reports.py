from fastapi import APIRouter

router = APIRouter(prefix="/reports", tags=["Member 7: Reports & Analytics (Pending)"])


@router.get("/status")
def reports_status():
    """Module status placeholder for Member 7."""
    return {
        "module": "Reports & Analytics",
        "assigned_to": "Member 7",
        "status": "In Development",
        "planned_entities": ["sales_report", "purchase_report", "inventory_report", "financial_report"],
    }
