import pytest
from pydantic import ValidationError

from app.core.config import Settings


def test_placeholder_secret_key_is_rejected():
    with pytest.raises(ValidationError):
        Settings(
            database_url="sqlite:///./test.db",
            secret_key="replace-with-a-random-secret-of-at-least-32-characters",
        )


def test_non_sqlite_database_is_rejected():
    with pytest.raises(ValidationError):
        Settings(
            database_url="unsupported://localhost/smarterp",
            secret_key="01234567890123456789012345678901",
        )
