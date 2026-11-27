from secrets import randbits

from alembic import command
from alembic.config import Config
from sqlalchemy import Engine, text
from sqlalchemy.engine import make_url

from app.core.config import BACKEND_DIR, Settings
from app.db.session import make_engine


def target(url: str) -> tuple[str, int, str]:
    parsed = make_url(url)
    # The driver also accepts connection parameters in the query string.
    host = parsed.query.get("hostaddr") or parsed.query.get("host") or parsed.host or ""
    if host.lower() in {"localhost", "127.0.0.1", "::1"}:
        host = "localhost"
    port = int(parsed.query.get("port") or parsed.port or 5432)
    database = parsed.query.get("dbname") or parsed.database
    return host.lower(), port, database


def test_database_engine(settings: Settings) -> Engine:
    test_url = settings.test_database_url
    if not test_url:
        raise ValueError("Для тестов требуется отдельная TEST_DATABASE_URL")
    working, testing = target(settings.database_url), target(test_url)
    if working == testing:
        raise ValueError("TEST_DATABASE_URL указывает на рабочую базу")

    engine = make_engine(test_url)
    if working[2] == testing[2]:
        # Two different server addresses may still refer to the same database.
        # Transaction-scoped advisory locks are visible only within one database.
        work_engine = make_engine(settings.database_url)
        key = {"key": randbits(62)}
        try:
            with work_engine.begin() as work_conn, engine.begin() as test_conn:
                work_conn.execute(text("SELECT pg_advisory_xact_lock(:key)"), key)
                if not test_conn.scalar(text("SELECT pg_try_advisory_xact_lock(:key)"), key):
                    raise ValueError("TEST_DATABASE_URL указывает на рабочую базу")
        except Exception:
            engine.dispose()
            raise
        finally:
            work_engine.dispose()
    return engine


def migration_config(connection) -> Config:
    config = Config(str(BACKEND_DIR / "alembic.ini"))
    config.attributes["connection"] = connection
    return config


def migrate(engine: Engine) -> None:
    with engine.begin() as connection:
        command.upgrade(migration_config(connection), "head")
