from typing import TypeVar, Type

from sqlalchemy.orm import Session

from monorepo.core.db.ledger_repository import LedgerRepository
from monorepo.core.ledgers.schemas import SharedLedgerOperation

LEDGER_OPERATION_CONFIG = {
    SharedLedgerOperation.DAILY_REWARD: 1,
    SharedLedgerOperation.SIGNUP_CREDIT: 3,
    SharedLedgerOperation.CREDIT_SPEND: -1,
    SharedLedgerOperation.CREDIT_ADD: 10,
}

T = TypeVar('T', bound=SharedLedgerOperation)


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

        def _check_sufficient_balance(self, session: Session, owner_id: str, amount: int) -> bool:
            if amount >= 0:
                return True
            current_balance = self.repository.get_balance(session, owner_id)
            return (current_balance - amount) >= 0
