from fastapi import APIRouter

router = APIRouter(prefix="/finance", tags=["Member 6: Finance (Pending)"])


@router.get("/status")
def finance_status():
    """Module status placeholder for Member 6."""
    return {
        "module": "Finance",
        "assigned_to": "Member 6",
        "status": "In Development",
        "planned_entities": ["expenses", "expense_categories", "financial_transactions"],
    }
