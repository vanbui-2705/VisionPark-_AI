from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.core.config import Settings
from app.database.seed import seed_database
from app.modules.users.models import Role, User
from app.modules.users.schemas import RoleName


def test_seed_is_idempotent_and_creates_demo_identity_data(
    db_session: Session, settings: Settings
) -> None:
    seed_database(db_session, settings)
    seed_database(db_session, settings)

    assert db_session.scalar(select(func.count()).select_from(Role)) == len(RoleName)
    assert db_session.scalar(select(func.count()).select_from(User)) == 2
    assert set(db_session.scalars(select(Role.name))) == {role.value for role in RoleName}
