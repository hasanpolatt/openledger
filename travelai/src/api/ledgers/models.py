from datetime import datetime, timezone
from typing import Optional

from sqlalchemy import DateTime, Enum, Float, Integer, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from api.ledgers.schemas import TravelAILedgerOperation


class Base(DeclarativeBase):
    pass


class TravelAILedgerEntryModel(Base):
    __tablename__ = "ledger_entries"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    operation: Mapped[TravelAILedgerOperation] = mapped_column(
        Enum(TravelAILedgerOperation), nullable=False
    )
    amount: Mapped[int] = mapped_column(Integer, nullable=False)
    category: Mapped[str] = mapped_column(String, nullable=False)  # flight, hotel, activity
    nonce: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    owner_id: Mapped[str] = mapped_column(String, nullable=False)
    created_on: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, default=lambda: datetime.now(timezone.utc)
    )

    def __repr__(self) -> str:
        return f"<TravelAILedgerEntry(id={self.id}, operation={self.operation}, amount={self.amount}{self.currency}, category={self.category}, status={self.status})>"