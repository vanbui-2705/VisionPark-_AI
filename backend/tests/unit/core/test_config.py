import pytest
from pydantic import ValidationError

from app.core.config import DEV_JWT_SECRET, Settings


def test_production_rejects_development_secret() -> None:
    with pytest.raises(ValidationError, match="Production must provide"):
        Settings(environment="production", jwt_secret_key=DEV_JWT_SECRET)


def test_cors_origins_are_parsed_and_trimmed() -> None:
    settings = Settings(cors_origins="http://one.test, http://two.test")
    assert settings.cors_origin_list == ["http://one.test", "http://two.test"]
