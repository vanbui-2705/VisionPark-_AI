from collections.abc import Generator
from pathlib import Path
from typing import Annotated

import pytest
from alembic.config import Config
from fastapi import Depends, FastAPI
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from alembic import command
from app.core.config import Settings
from app.database.session import database
from app.main import create_app
from app.modules.auth.dependencies import require_roles
from app.modules.users.models import User
from app.modules.users.schemas import RoleName

TEST_JWT_SECRET = "test-secret-key-with-at-least-thirty-two-characters"
BACKEND_ROOT = Path(__file__).resolve().parents[1]
AdminUser = Annotated[User, Depends(require_roles(RoleName.ADMIN))]


def make_alembic_config(database_url: str) -> Config:
    config = Config(str(BACKEND_ROOT / "alembic.ini"))
    config.set_main_option("script_location", str(BACKEND_ROOT / "alembic"))
    config.set_main_option("sqlalchemy.url", database_url.replace("%", "%%"))
    return config


@pytest.fixture
def database_url(tmp_path: Path) -> str:
    return f"sqlite:///{(tmp_path / 'visionpark-test.db').as_posix()}"


@pytest.fixture
def migrated_database_url(database_url: str) -> Generator[str, None, None]:
    command.upgrade(make_alembic_config(database_url), "head")
    yield database_url
    engine = create_engine(database_url)
    engine.dispose()


@pytest.fixture
def settings(migrated_database_url: str) -> Settings:
    return Settings(
        environment="test",
        database_url=migrated_database_url,
        jwt_secret_key=TEST_JWT_SECRET,
        auto_seed=True,
        seed_admin_password="admin-test-password",
        seed_operator_password="operator-test-password",
        cors_origins="http://localhost:5173,http://127.0.0.1:5173",
    )


@pytest.fixture
def app(settings: Settings) -> FastAPI:
    test_app = create_app(settings)

    @test_app.get("/api/v1/test/admin-only")
    def admin_only(_: AdminUser) -> dict[str, bool]:
        return {"allowed": True}

    return test_app


@pytest.fixture
def client(app: FastAPI) -> Generator[TestClient, None, None]:
    with TestClient(app) as test_client:
        yield test_client


@pytest.fixture
def db_session(client: TestClient) -> Generator[Session, None, None]:
    del client  # Ensure the application lifespan has configured the database.
    session = database.create_session()
    try:
        yield session
    finally:
        session.close()


def login(client: TestClient, username: str, password: str) -> dict[str, object]:
    response = client.post(
        "/api/v1/auth/login",
        json={"username": username, "password": password},
    )
    assert response.status_code == 200, response.text
    return response.json()
