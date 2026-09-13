from sqlalchemy import create_engine, inspect

from alembic import command
from tests.conftest import make_alembic_config


def test_migration_up_and_down_on_empty_database(database_url: str) -> None:
    config = make_alembic_config(database_url)
    command.upgrade(config, "head")

    engine = create_engine(database_url)
    assert {"alembic_version", "roles", "users"}.issubset(inspect(engine).get_table_names())
    engine.dispose()

    command.downgrade(config, "base")
    engine = create_engine(database_url)
    assert "roles" not in inspect(engine).get_table_names()
    assert "users" not in inspect(engine).get_table_names()
    engine.dispose()


def test_migration_head_matches_registered_models(database_url: str) -> None:
    config = make_alembic_config(database_url)
    command.upgrade(config, "head")
    command.check(config)
