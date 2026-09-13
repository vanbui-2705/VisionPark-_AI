from datetime import datetime
from enum import StrEnum
from uuid import UUID

from pydantic import BaseModel


class RoleName(StrEnum):
    ADMIN = "ADMIN"
    OPERATOR = "OPERATOR"
    ACCOUNTANT = "ACCOUNTANT"
    TECHNICIAN = "TECHNICIAN"


class UserPublic(BaseModel):
    id: UUID
    username: str
    display_name: str
    role: RoleName
    is_active: bool
    last_login_at: datetime | None
