from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from monorepo.core.config import SQLALCHEMY_DATABASE_URI
from monorepo.core.db.ledger_repository import ledger_repository

engine = create_engine(SQLALCHEMY_DATABASE_URI)

test_owners = ["user1", "user2", "nonexistent_user"]

# Check balance for each owner
with Session(engine) as session:
    print("\nBalance Checks:")
    print("-" * 50)
    for owner_id in test_owners:
        balance = ledger_repository.get_balance(session, owner_id)
        print(f"Owner ID: {owner_id:15} | Balance: {balance}")
