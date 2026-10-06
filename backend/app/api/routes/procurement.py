from fastapi import APIRouter

router = APIRouter(prefix="/procurement", tags=["Member 6: Procurement (Pending)"])


@router.get("/status")
def procurement_status():
    """Module status placeholder for Member 6."""
    return {
        "module": "Procurement",
        "assigned_to": "Member 6",
        "status": "In Development",
        "planned_entities": ["suppliers", "purchase_orders", "purchase_invoices"],
    }
