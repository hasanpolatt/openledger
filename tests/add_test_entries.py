from datetime import datetime, timezone
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from monorepo.core.config import SQLALCHEMY_DATABASE_URI
from monorepo.core.db.models import LedgerEntry
from monorepo.core.ledgers.schemas import SharedLedgerOperation
from monorepo.core.db.ledger_repository import ledger_repository

test_entries = [
    {
        "operation": SharedLedgerOperation.DAILY_REWARD,
        "amount": 100,
        "nonce": "test1",
        # owner_id belirtmiyoruz, otomatik generate edilecek
    },
    {
        "operation": SharedLedgerOperation.CREDIT_SPEND,
        "amount": -50,
        "nonce": "test2",
        # owner_id belirtmiyoruz, otomatik generate edilecek
    },
    {
        "operation": SharedLedgerOperation.SIGNUP_CREDIT,
        "amount": 200,
        "nonce": "test3",
        # owner_id belirtmiyoruz, otomatik generate edilecek
    }
]

engine = create_engine(SQLALCHEMY_DATABASE_URI)

# Add test entries
with Session(engine) as session:
    for entry_data in test_entries:
        entry = LedgerEntry(
            **entry_data,
            created_on=datetime.now(timezone.utc)
        )
        try:
            created_entry = ledger_repository.create_entry(session, entry)
            print(f"Entry added with generated owner_id: {created_entry.owner_id}")
        except ValueError as e:
            print(f"Error: {e}")
