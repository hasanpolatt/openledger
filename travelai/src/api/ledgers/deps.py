from collections.abc import Generator

from fastapi import Depends, HTTPException, Security, status
from fastapi.security import APIKeyHeader, APIKeyQuery, HTTPBasic
from sqlalchemy.orm import Session

from monorepo.core.db import token_repository
from monorepo.core.db.models import Token
from monorepo.core.db.session import SessionLocal

API_KEY_NAME = "X-API-Key"
X_API_KEY_HEADER = APIKeyHeader(name=API_KEY_NAME, auto_error=False)
X_API_KEY_QUERY = APIKeyQuery(name=API_KEY_NAME, auto_error=False)


def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    yield db
    db.close()


def get_api_key(
        api_key_query: str = Security(X_API_KEY_QUERY),
        api_key_header: str = Security(X_API_KEY_HEADER),
        session: Session = Depends(get_db),
) -> Token:
    x_api_key = api_key_query or api_key_header

    if key := token_repository.token.get_by_key(db=session, api_key=x_api_key):
        return key
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid API Key",
    )


http_basic_security = HTTPBasic()
