from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import scoped_session, sessionmaker

from monorepo.core.config import SQLALCHEMY_DATABASE_URI


def create_database_engine(database_url: str) -> Engine:
    """Create a new SQLAlchemy engine

    Args:
        database_url: Database connection URL

    Returns:
        Engine: SQLAlchemy engine
    """
    return create_engine(
        database_url,
        pool_pre_ping=True,
        pool_recycle=3600,
        connect_args={
            "keepalives": 1,
            "keepalives_idle": 30,
            "keepalives_interval": 10,
            "keepalives_count": 5,
        },
    )


engine = create_database_engine(SQLALCHEMY_DATABASE_URI)

SessionLocal = scoped_session(
    sessionmaker(autocommit=False, autoflush=False, bind=engine)
)
