from enum import Enum

from monorepo.core.ledgers.schemas import (
    SharedLedgerOperation,
    register_ledger_operation,
)
from pydantic import BaseModel


class HealthAILedgerOperation(Enum):
    """Health AI specific ledger operations"""
    DAILY_REWARD = SharedLedgerOperation.DAILY_REWARD.value
    SIGNUP_CREDIT = SharedLedgerOperation.SIGNUP_CREDIT.value
    CREDIT_SPEND = SharedLedgerOperation.CREDIT_SPEND.value
    CREDIT_ADD = SharedLedgerOperation.CREDIT_ADD.value
    
    COMPLETE_CHALLENGE = "COMPLETE_CHALLENGE"
    ACHIEVE_GOAL = "ACHIEVE_GOAL"
    REFER_FRIEND = "REFER_FRIEND"


HEALTH_OPERATION_CONFIG = {

    HealthAILedgerOperation.COMPLETE_CHALLENGE.value: 5,
    HealthAILedgerOperation.ACHIEVE_GOAL.value: 10,
    HealthAILedgerOperation.REFER_FRIEND.value: 15
}

register_ledger_operation(HealthAILedgerOperation, HEALTH_OPERATION_CONFIG)


class OperationRequest(BaseModel):
    """Request model for ledger operations"""
    owner_id: str
    operation: HealthAILedgerOperation
    nonce: str | None = None
