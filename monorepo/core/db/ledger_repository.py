from typing import Optional
from sqlalchemy import select, func
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from monorepo.core.db.models import LedgerEntry


class LedgerRepository:
    # This class should be used for db operations
    def create_entry(self, session: Session, entry: LedgerEntry) -> LedgerEntry:
        db_entry = LedgerEntry(
            operation=entry.operation,
            amount=entry.amount,
            nonce=entry.nonce,
            owner_id=entry.owner_id,
            created_on=entry.created_on
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
        result = session.execute(
            select(func.sum(LedgerEntry.amount))
            .where(LedgerEntry.owner_id == owner_id)
        )
        balance = result.scalar_one_or_none()
        return balance or 0

    def get_entries(self, session: Session, owner_id: str, limit: int = 100):
        result = session.execute(
            select(LedgerEntry)
            .where(LedgerEntry.owner_id == owner_id)
            .order_by(LedgerEntry.created_on.desc())
            .limit(limit)
        )
        return list(result.scalars().all())

    def get_entry_by_nonce(self, session: Session, nonce: str) -> Optional[LedgerEntry]:
        result = session.execute(
            select(LedgerEntry).where(LedgerEntry.nonce == nonce)
        )
        return result.scalar_one_or_none()


ledger_repository = LedgerRepository()
