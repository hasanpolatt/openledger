from monorepo.core.ledgers.schemas import (
    SharedLedgerOperation,
    register_ledger_operation,
)
from pydantic import BaseModel


class TravelAILedgerOperation(SharedLedgerOperation):
    """Travel AI specific ledger operations"""

    DAILY_REWARD = "DAILY_REWARD"
    SIGNUP_CREDIT = "SIGNUP_CREDIT"
    CREDIT_SPEND = "CREDIT_SPEND"
    CREDIT_ADD = "CREDIT_ADD"

    # Content operations
    CONTENT_CREATION = "CONTENT_CREATION"
    CONTENT_ACCESS = "CONTENT_ACCESS"

    # Community operations
    TIP_GUIDE = "TIP_GUIDE"
    JOIN_GROUP = "JOIN_GROUP"
    GROUP_ORGANIZE = "GROUP_ORGANIZE"


TRAVEL_OPERATION_CONFIG = {
    # Content operations
    TravelAILedgerOperation.CONTENT_CREATION.value: -5,
    TravelAILedgerOperation.CONTENT_ACCESS.value: -2,
    # Community operations
    TravelAILedgerOperation.TIP_GUIDE.value: -5,
    TravelAILedgerOperation.JOIN_GROUP.value: -1,
    TravelAILedgerOperation.GROUP_ORGANIZE.value: 5,
}


register_ledger_operation(TravelAILedgerOperation, TRAVEL_OPERATION_CONFIG)


class OperationRequest(BaseModel):
    """Request model for ledger operations"""

    owner_id: str
    operation: TravelAILedgerOperation  # Use Enum directly for type safety
    nonce: str | None = None
