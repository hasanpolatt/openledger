import enum


class BaseLedgerOperation(enum.Enum):
    # How to make sure that all ledger operations that inherits from BaseLedgerOperation have all of the SharedLedgerOperations defined below?
    pass


class SharedLedgerOperation(BaseLedgerOperation):
    DAILY_REWARD = "DAILY_REWARD"
    SIGNUP_CREDIT = "SIGNUP_CREDIT"
    CREDIT_SPEND = "CREDIT_SPEND"
    CREDIT_ADD = "CREDIT_ADD"
