from datetime import datetime, timezone

from sqlalchemy import DateTime, Enum, Integer, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from monorepo.core.ledgers.schemas import SharedLedgerOperation


class Base(DeclarativeBase):
    pass


class LedgerEntry(Base):

    __tablename__ = "ledger_entries"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    operation: Mapped[SharedLedgerOperation] = mapped_column(
        Enum(SharedLedgerOperation), nullable=False
    )
    amount: Mapped[int] = mapped_column(Integer, nullable=False)
    nonce: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    owner_id: Mapped[str] = mapped_column(String, nullable=False)
    created_on: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, default=lambda: datetime.now(timezone.utc)
    )

    def __repr__(self) -> str:
        return f"<LedgerEntry(id={self.id}, operation={self.operation}, amount={self.amount}, owner_id={self.owner_id})>"
