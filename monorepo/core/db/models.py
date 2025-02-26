from datetime import datetime, timezone
from typing import final
import binascii
import os
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
    nonce: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)
    owner_id: Mapped[str] = mapped_column(String(50), nullable=False)
    created_on: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, default=lambda: datetime.now(timezone.utc)
    )

    def __repr__(self) -> str:
        return f"<LedgerEntry(id={self.id}, operation={self.operation}, amount={self.amount}, owner_id={self.owner_id})>"


def generate_key() -> str:
    return binascii.hexlify(os.urandom(20)).decode()


@final
class Token(Base):
    __tablename__ = "tokens"
    id = mapped_column(Integer, primary_key=True, index=True)
    key: Mapped[str] = mapped_column(String, unique=True, default=generate_key)
    created: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(timezone.utc))
