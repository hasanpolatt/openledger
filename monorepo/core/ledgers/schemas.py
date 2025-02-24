from datetime import datetime, timezone
from enum import Enum, EnumMeta
from typing import Type

from pydantic import BaseModel, Field


class BaseLedgerOperation(EnumMeta):
    """Make sure to define shared operations in all ledger operations"""

    @property
    def shared_operations(cls) -> set[str]:
        return {"DAILY_REWARD", "SIGNUP_CREDIT", "CREDIT_SPEND", "CREDIT_ADD"}

    def __new__(mcs, name, bases, namespace):
        if bases and bases[0] != Enum:
            # Check all shared operations are implemented
            missing_ops = mcs.shared_operations - {k for k, v in namespace.items() if not k.startswith('_')}
            if missing_ops:
                raise TypeError(f"Missing required shared operations: {missing_ops}")
        return super().__new__(mcs, name, bases, namespace)


class SharedLedgerOperation(Enum, metaclass=BaseLedgerOperation):
    """Ledger operations that must be implemented by all applications"""
    DAILY_REWARD = "DAILY_REWARD"
    SIGNUP_CREDIT = "SIGNUP_CREDIT"
    CREDIT_SPEND = "CREDIT_SPEND"
    CREDIT_ADD = "CREDIT_ADD"

    @classmethod
    def values(cls) -> set[str]:
        return {item.value for item in cls}


class LedgerEntry(BaseModel):
    """Pydantic model for ledger entries"""
    id: int | None = None
    operation: SharedLedgerOperation
    amount: int
    nonce: str
    owner_id: str
    created_on: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    class Config():
        from_attributes: True


LEDGER_OPERATION_CONFIG: dict[str, int] = {
    SharedLedgerOperation.DAILY_REWARD.value: 1,
    SharedLedgerOperation.SIGNUP_CREDIT.value: 3,
    SharedLedgerOperation.CREDIT_SPEND.value: -1,
    SharedLedgerOperation.CREDIT_ADD.value: 10,
}


def register_ledger_operation(operation_class: Type[Enum], config: dict[str, int]) -> None:
    """Register ledger operations for a specific application"""
    if not all(op.value in {item.value for item in operation_class}
               for op in SharedLedgerOperation):
        raise ValueError("Implementation must include all shared ledger operations")

    LEDGER_OPERATION_CONFIG.update(config)