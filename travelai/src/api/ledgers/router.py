from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from monorepo.core.db.ledger_repository import LedgerRepository
from monorepo.core.ledgers.schemas import LedgerEntry
from monorepo.core.ledgers.services.base_ledger_service import \
    BaseLedgerService
from travelai.src.core.db.database import get_db

from . import deps
from .schemas import OperationRequest, TravelAILedgerOperation

router = APIRouter(
    prefix="/ledger", tags=["ledger"], dependencies=[Depends(deps.get_api_key)]
)


@router.get("/{owner_id}", response_model=int)
def get_balance(owner_id: str, session: Session = Depends(get_db)) -> int:
    """Get owner current balance.

    Args:
        owner_id: Owner unique identifier
        session: Database session

    Returns:
        int: Current balance
    """
    service = BaseLedgerService(LedgerRepository(), TravelAILedgerOperation)
    return service.get_balance(session, owner_id)


@router.get("/{owner_id}/entries", response_model=List[LedgerEntry])
def get_ledger_entries(
    owner_id: str, session: Session = Depends(get_db)
) -> List[LedgerEntry]:
    """Get all ledger entries for owner.

    Args:
        owner_id: Owner unique identifier
        session: Database session

    Returns:
        List: List of ledger entries
    """
    service = BaseLedgerService(LedgerRepository(), TravelAILedgerOperation)
    return service.get_ledger_entries(session, owner_id)


@router.post("/", response_model=LedgerEntry)
def create_ledger_entry(
    request: OperationRequest, session: Session = Depends(get_db)
) -> LedgerEntry:
    """Create new ledger entry.

    Args:
        request: Operation request details
        session: Database session

    Returns:
        LedgerEntry: Created ledger entry

    Raises:
        HTTPException: If operation is invalid
    """
    try:
        service = BaseLedgerService(LedgerRepository(), TravelAILedgerOperation)
        return service.process_operation(session, request.owner_id, request.operation)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
