import pytest

from app.core.config import Settings
from tests.db_support import test_database_engine as checked_engine


WORKING = "postgresql+psycopg://runner@127.0.0.1:5432/gymtracker"


@pytest.mark.parametrize("test_url", [
    None,
    WORKING,
    "postgresql://different_user@localhost/gymtracker?sslmode=prefer",
    "postgresql+psycopg://runner@localhost/other?dbname=gymtracker",
])
def test_rejects_missing_or_shared_database_before_connecting(test_url):
    settings = Settings(_env_file=None, database_url=WORKING, test_database_url=test_url)
    with pytest.raises(ValueError, match="TEST_DATABASE_URL"):
        checked_engine(settings)


def test_configuration_h():
    settings = Settings(_env_file=None, database_url=WORKING)
    assert settings.features == ""
    assert settings.ai_enabled is False
