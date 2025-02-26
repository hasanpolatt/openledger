from typing import List, Optional

from sqlalchemy import func, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from monorepo.core.db.models import LedgerEntry


class LedgerRepository:
    # This class should be used for db operations
    def create_entry(self, session: Session, entry: LedgerEntry) -> LedgerEntry:
        """Create a new ledger entry.

        Args:
            session: Database session
            entry: Entry to create

        Returns:
            LedgerEntry: Created entry

        Raises:
            IntegrityError: If entry with same nonce already exists
        """
        db_entry = LedgerEntry(
            operation=entry.operation,
            amount=entry.amount,
            nonce=entry.nonce,
            owner_id=entry.owner_id,
            created_on=entry.created_on,
        )
        try:
            session.add(db_entry)
            session.commit()
            session.refresh(db_entry)
            return db_entry
        except IntegrityError:
            session.rollback()
            raise ValueError("Ledger entry already exists")

    def get_balance(self, session: Session, owner_id: str) -> int:
        """Get the current balance for an owner.

        Args:
            session: Database session
            owner_id: Owner unique identifier

        Returns:
            int: Current balance, defaults to 0 if no entries exist
        """
        result = session.execute(
            select(func.sum(LedgerEntry.amount)).where(LedgerEntry.owner_id == owner_id)
        )
        balance = result.scalar_one_or_none()
        return balance or 0

    def get_entries(
        self, session: Session, owner_id: str, limit: Optional[int] = None
    ) -> List[LedgerEntry]:
        """Get ledger entries for an owner.

        Args:
            session: Database session
            owner_id: Owner's unique identifier
            limit: Maximum number of entries

        Returns:
            List: List of ledger entries
        """
        result = session.execute(
            select(LedgerEntry)
            .where(LedgerEntry.owner_id == owner_id)
            .order_by(LedgerEntry.created_on.desc())
            .limit(limit)
            if limit
            else select(LedgerEntry)
            .where(LedgerEntry.owner_id == owner_id)
            .order_by(LedgerEntry.created_on.desc())
        )
        return list(result.scalars().all())

    def get_entry_by_nonce(self, session: Session, nonce: str) -> Optional[LedgerEntry]:
        """Get ledger entry by nonce.

        Args:
            session: Database session
            nonce: Entry's unique nonce

        Returns:
            Optional: Ledger entry if found
        """
        result = session.execute(select(LedgerEntry).where(LedgerEntry.nonce == nonce))
        return result.scalar_one_or_none()


ledger_repository = LedgerRepository()
