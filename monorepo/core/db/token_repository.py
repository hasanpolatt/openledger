from typing import final

from sqlalchemy.orm import Session

from monorepo.core.db.models import Token, generate_key


@final
class TokenRepository:

    def generate(self, db: Session) -> Token:
        """
        Generate new Token.

        Args:
            db: database session.

        Returns:
            Created Token object.
        """
        token_obj = Token(key=generate_key())
        db.add(token_obj)
        db.commit()
        db.refresh(token_obj)
        return token_obj

    def get_by_key(self, db: Session, api_key: str) -> Token | None:
        """
        Get token by key.

        Args:
            db: database session.
            api_key: api key.

        Returns:
            Token object if exists.
        """
        return db.query(Token).filter_by(key=api_key).one_or_none()


token = TokenRepository()
