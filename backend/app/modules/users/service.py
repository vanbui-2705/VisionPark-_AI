from app.modules.users.models import User
from app.modules.users.schemas import RoleName, UserPublic


def to_public_user(user: User) -> UserPublic:
    return UserPublic(
        id=user.id,
        username=user.username,
        display_name=user.display_name,
        role=RoleName(user.role.name),
        is_active=user.is_active,
        last_login_at=user.last_login_at,
    )
