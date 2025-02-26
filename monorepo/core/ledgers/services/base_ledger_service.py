import uuid
from datetime import datetime, timezone
from typing import List, Type, TypeVar

from sqlalchemy.orm import Session

from monorepo.core.db.ledger_repository import LedgerRepository
from monorepo.core.db.models import LedgerEntry
from monorepo.core.ledgers.schemas import SharedLedgerOperation

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
        """Validate the operation type.

        Args:
            operation: Operation type to validate

        Raises:
            ValueError: If operation is invalid
        """
        if operation not in self.operation_class:
            raise ValueError(f"Invalid operation: {operation}")

    def _get_operation_amount(self, operation: T) -> int:
        """Get the amount associated with the operation.

        Args:
            operation: Operation type

        Returns:
            int: Amount associated with the operation

        Raises:
            ValueError: If operation is not valid
        """
        if operation not in LEDGER_OPERATION_CONFIG:
            raise ValueError(f"Operation {operation} is not valid")
        return LEDGER_OPERATION_CONFIG[operation]

    def _check_sufficient_balance(
        self, session: Session, owner_id: str, amount: int
    ) -> bool:
        """Check if the owner has sufficient balance.

        Args:
            session: Database session
            owner_id: Owner's unique identifier
            amount: Amount to check against

        Returns:
            bool: True if balance is sufficient, False otherwise
        """
        if amount >= 0:
            return True
        current_balance = self.repository.get_balance(session, owner_id)
        return (current_balance - amount) >= 0

    def process_operation(
        self, session: Session, owner_id: str, operation: T
    ) -> LedgerEntry:
        """Process a ledger operation and create a new entry.

        Args:
            session: Database session
            owner_id: Owner's identifier
            operation: Operation type from enum

        Returns:
            LedgerEntry: Created ledger entry

        Raises:
            ValueError: If operation is invalid or balance would become negative
        """
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
        """Get current balance for the owner.

        Args:
            session: Database session
            owner_id: Owner's identifier

        Returns:
            int: Current balance amount
        """
        return self.repository.get_balance(session, owner_id)

    def get_ledger_entries(
        self, session: Session, owner_id: str, limit: int = 100
    ) -> List[LedgerEntry]:
        """Retrieve all ledger entries for the owner.

        Args:
            session: Database session
            owner_id: Owner's unique identifier
            limit: Maximum number of entries to retrieve. Defaults to 100.

        Returns:
            List: List of ledger entries
        """
        return self.repository.get_entries(session, owner_id, limit)
