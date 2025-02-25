import uuid
from datetime import datetime, timezone
from typing import List, Type, TypeVar

from monorepo.core.db.ledger_repository import LedgerRepository
from monorepo.core.db.models import LedgerEntry
from monorepo.core.ledgers.schemas import SharedLedgerOperation
from sqlalchemy.orm import Session

T = TypeVar("T", bound=SharedLedgerOperation)

LEDGER_OPERATION_CONFIG = {
    SharedLedgerOperation.DAILY_REWARD: 1,
    SharedLedgerOperation.SIGNUP_CREDIT: 3,
    SharedLedgerOperation.CREDIT_SPEND: -1,
    SharedLedgerOperation.CREDIT_ADD: 10,
}


class BaseLedgerService:
    def __init__(self, repository: LedgerRepository, operation_class: Type[T]):
        self.repository = repository
        self.operation_class = operation_class

    def _validate_operation(self, operation: T) -> None:
        if operation not in self.operation_class:
            raise ValueError(f"Invalid operation: {operation}")

    def _get_operation_amount(self, operation: T) -> int:
        if operation not in LEDGER_OPERATION_CONFIG:
            raise ValueError(f"Operation {operation} is not valid")
        return LEDGER_OPERATION_CONFIG[operation]

    def _check_sufficient_balance(
        self, session: Session, owner_id: str, amount: int
    ) -> bool:
        if amount >= 0:
            return True
        current_balance = self.repository.get_balance(session, owner_id)
        return (current_balance - amount) >= 0

    def process_operation(
        self, session: Session, owner_id: str, operation: T
    ) -> LedgerEntry:
        self._validate_operation(operation)
        amount = self._get_operation_amount(operation)

        if not self._check_sufficient_balance(session, owner_id, amount):
            raise ValueError("Not enough balance")

        entry = LedgerEntry(
            operation=operation,
            amount=amount,
            nonce=str(uuid.uuid4()),
            owner_id=owner_id,
            created_on=datetime.now(timezone.utc),
        )

        return self.repository.create_entry(session, entry)

    def get_balance(self, session: Session, owner_id: str) -> int:
        return self.repository.get_balance(session, owner_id)

    def get_ledger_entries(
        self, session: Session, owner_id: str, limit: int = 100
    ) -> List[LedgerEntry]:
        return self.repository.get_entries(session, owner_id, limit)
