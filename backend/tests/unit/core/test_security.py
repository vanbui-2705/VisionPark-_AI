from datetime import timedelta
from uuid import uuid4

import pytest

from app.core.config import Settings
from app.core.errors import AppError
from app.core.security import (
    create_access_token,
    decode_access_token,
    hash_password,
    verify_password,
)
from tests.conftest import TEST_JWT_SECRET


def test_password_is_argon2id_hash_and_verifies() -> None:
    password_hash = hash_password("correct horse battery staple")
    assert password_hash.startswith("$argon2id$")
    assert verify_password("correct horse battery staple", password_hash)
    assert not verify_password("wrong", password_hash)


def test_expired_token_is_rejected() -> None:
    settings = Settings(environment="test", jwt_secret_key=TEST_JWT_SECRET)
    token = create_access_token(uuid4(), settings, expires_delta=timedelta(seconds=-1))
    with pytest.raises(AppError) as error:
        decode_access_token(token, settings)
    assert error.value.status_code == 401
