from typing import List

from fastapi import APIRouter, Depends, HTTPException
from monorepo.core.db.ledger_repository import LedgerRepository
from monorepo.core.ledgers.schemas import LedgerEntry
from monorepo.core.ledgers.services.base_ledger_service import BaseLedgerService
from sqlalchemy.orm import Session
from travelai.src.core.db.database import get_db

from .schemas import OperationRequest, TravelAILedgerOperation

router = APIRouter(prefix="/ledger", tags=["ledger"], dependencies=[Depends(get_db)])


@router.get("/{owner_id}", response_model=int)
def get_balance(owner_id: str, session: Session = Depends(get_db)) -> int:
    service = BaseLedgerService(LedgerRepository(), TravelAILedgerOperation)
    return service.get_balance(session, owner_id)


@router.get("/{owner_id}/entries", response_model=List[LedgerEntry])
def get_ledger_entries(
    owner_id: str, session: Session = Depends(get_db)
) -> List[LedgerEntry]:
    service = BaseLedgerService(LedgerRepository(), TravelAILedgerOperation)
    return service.get_ledger_entries(session, owner_id)


@router.post("/", response_model=LedgerEntry)
def create_ledger_entry(
    request: OperationRequest, session: Session = Depends(get_db)
) -> LedgerEntry:
    try:
        service = BaseLedgerService(LedgerRepository(), TravelAILedgerOperation)
        return service.process_operation(session, request.owner_id, request.operation)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
