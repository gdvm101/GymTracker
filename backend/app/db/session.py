from collections.abc import Iterator
from functools import lru_cache

from sqlalchemy import Engine, create_engine
from sqlalchemy.orm import Session, sessionmaker

from app.core.config import get_settings


# SQLAlchemy Session implements begin(), commit() and rollback().
UnitOfWork = Session


def make_engine(url: str, *, schema: str | None = None) -> Engine:
    options = {"connect_timeout": 4}
    if schema is not None:
        # Test schemas are generated locally and must be single, unquoted identifiers.
        if not schema.isascii() or not schema.isidentifier():
            raise ValueError("Некорректное имя схемы")
        options["options"] = f"-csearch_path={schema}"
    return create_engine(url, pool_pre_ping=True, hide_parameters=True, connect_args=options)


@lru_cache
def session_factory() -> sessionmaker[Session]:
    return sessionmaker(make_engine(get_settings().database_url), expire_on_commit=False)


def get_db() -> Iterator[UnitOfWork]:
    factory = session_factory()
    with factory() as session:
        yield session
