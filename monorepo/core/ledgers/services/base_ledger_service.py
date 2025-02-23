from monorepo.core.db.ledger_repository import LedgerRepository  # BaseLedgerService should use LedgerRepository for db operations


class BaseLedgerService():

    def update_balance(
        self,
        operation: ?, # What type should this be?
        # Other params if needed
    ):
        # Implementation
        pass