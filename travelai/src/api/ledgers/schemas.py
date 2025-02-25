from monorepo.core.ledgers.schemas import SharedLedgerOperation


class TravelAILedgerOperation(SharedLedgerOperation):
    DAILY_REWARD = "DAILY_REWARD"
    SIGNUP_CREDIT = "SIGNUP_CREDIT"
    CREDIT_SPEND = "CREDIT_SPEND"
    CREDIT_ADD = "CREDIT_ADD"

    CONTENT_CREATION = "CONTENT_CREATION"
    CONTENT_ACCESS = "CONTENT_ACCESS"

    TIP_GUIDE = "TIP_GUIDE"
    JOIN_GROUP = "JOIN_GROUP"
    GROUP_ORGANIZE = "GROUP_ORGANIZE"


TRAVEL_OPERATION_CONFIG = {
    TravelAILedgerOperation.CONTENT_CREATION.value: -5,
    TravelAILedgerOperation.CONTENT_ACCESS.value: -2,
    
    TravelAILedgerOperation.TIP_GUIDE.value: -5,
    TravelAILedgerOperation.JOIN_GROUP.value: -1,
    TravelAILedgerOperation.GROUP_ORGANIZE.value: 5
}
