from sqlalchemy import create_engine, Engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.ext.declarative import declarative_base

from core.config import SQLALCHEMY_DATABASE_URI

def create_database_engine(database_url: str) -> Engine:
    """Create SQLAlchemy engine with connection pooling and keepalive settings
    
    Args:
        database_url: Database connection URL
        
    Returns:
        SQLAlchemy Engine instance
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

# Create engine instance
engine = create_database_engine(SQLALCHEMY_DATABASE_URI)

# Session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# SQLAlchemy model base class
Base = declarative_base()

def get_db() -> Session:
    """Database session dependency
    
    Yields:
        Session: Database session that will be automatically closed
        
    Raises:
        Exception: Any database related exception
    """
    db = SessionLocal()
    try:
        yield db
        db.commit()  # Successful transaction commit
    except Exception:
        db.rollback()  # Rollback on error
        raise
    finally:
        db.close()  # Always close the session
