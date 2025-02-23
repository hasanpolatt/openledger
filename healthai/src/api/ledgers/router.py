from fastapi import APIRouter
from monorepo.core.ledgers.services.base_ledger_service import BaseLedgerService


router = APIRouter()
ledger_service = BaseLedgerService()  # routers should use the ledger service from the core


# Example endpoint
@router.post(
    "/ledger-entry",
)
def add_ledger_entry(
    operation: ? # What type should this be?
    owner_id: str,
    nonce: str,
    # Other params if needed
):
    # Implementation
    pass
