from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.modules.users.models import User


class UserRepository:
    def __init__(self, session: Session):
        self.session = session

    def get_by_username(self, username: str) -> User | None:
        statement = select(User).where(User.username == username.strip().lower())
        return self.session.scalar(statement)

    def get_by_id(self, user_id: UUID) -> User | None:
        return self.session.get(User, user_id)
