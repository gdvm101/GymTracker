from uuid import uuid4

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from sqlalchemy.schema import CreateSchema, DropSchema

from app.core.config import get_settings
from app.db.session import get_db, make_engine
from app.main import create_app
from tests.db_support import migrate, test_database_engine


@pytest.fixture(autouse=True)
def h_configuration(monkeypatch):
    monkeypatch.setenv("FEATURES", "")
    monkeypatch.setenv("AI_ENABLED", "false")
    get_settings.cache_clear()
    yield
    get_settings.cache_clear()


@pytest.fixture
def db_engine():
    settings = get_settings()
    admin = test_database_engine(settings)
    schema = f"gym_test_{uuid4().hex}"
    with admin.begin() as connection:
        connection.execute(CreateSchema(schema))

    engine = make_engine(settings.test_database_url, schema=schema)
    try:
        migrate(engine)
        yield engine
    finally:
        engine.dispose()
        try:
            with admin.begin() as connection:
                connection.execute(DropSchema(schema, cascade=True))
        finally:
            admin.dispose()


@pytest.fixture
def client(db_engine):
    app = create_app()

    def test_db():
        with Session(db_engine) as db:
            yield db

    app.dependency_overrides[get_db] = test_db
    with TestClient(app) as http:
        yield http
