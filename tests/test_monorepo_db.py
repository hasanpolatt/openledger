from sqlalchemy import text

from monorepo.core.config import SQLALCHEMY_DATABASE_URI
from monorepo.core.db.session import create_database_engine


def test_connection():
    print(f"Trying to connect to: {SQLALCHEMY_DATABASE_URI}")
    engine = create_database_engine(SQLALCHEMY_DATABASE_URI)
    try:
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))
            print("Database connection successfull")
    except Exception as e:
        print(f"Database connection failed: {str(e)}")
        raise e

if __name__ == "__main__":
    test_connection()