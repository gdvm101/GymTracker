import pytest
from fastapi.exceptions import RequestValidationError
from fastapi.testclient import TestClient
from pydantic import BaseModel, Field
from sqlalchemy import exc as db_errors

from app.api.router import api_router
from app.core.errors import DomainError, normalize_error
from app.main import create_app


def test_ut_18_nested_field_path():
    error = RequestValidationError([{
        "type": "greater_than_equal",
        "loc": ("body", "exercises", 0, "sets", 1, "weight"),
        "input": -5,
    }])
    dto = normalize_error(error)
    assert dto.error.code == "INVALID_INPUT"
    assert dto.error.details == {"field": "exercises.0.sets.1.weight"}


class SetValue(BaseModel):
    weight: float = Field(ge=0)


@pytest.fixture
def http():
    # Only this test app registers the routes that exercise the error handlers.
    app = create_app()
    router = api_router()

    @router.post("/value")
    def post_value(value: SetValue):
        return value

    @router.get("/conflict")
    def conflict():
        raise DomainError("CONFLICT")

    @router.get("/failure")
    def failure():
        raise RuntimeError("private-test-marker")

    app.include_router(router)
    with TestClient(app) as client:
        yield client


@pytest.mark.parametrize(("body", "content_type", "status", "code"), [
    ('{"weight":', "application/json", 400, "BAD_JSON"),
    ('{"weight":-1}', "application/json", 422, "INVALID_INPUT"),
    ('{"weight":1}', "text/plain", 415, "UNSUPPORTED_MEDIA_TYPE"),
])
def test_json_errors_over_http(http, body, content_type, status, code):
    response = http.post("/value", content=body, headers={"Content-Type": content_type})
    assert response.status_code == status
    error = response.json()["error"]
    assert error["code"] == code
    assert error["details"] == ({"field": "weight"} if status == 422 else None)
    assert response.headers["X-Request-ID"]


def test_json_success_and_domain_error(http):
    assert http.post("/value", json={"weight": 30}).json() == {"weight": 30}
    response = http.get("/conflict")
    assert response.status_code == 409
    assert response.json()["error"]["code"] == "CONFLICT"


def test_unexpected_error_is_safe_and_carries_request_id(http, caplog):
    response = http.get("/failure")
    assert response.status_code == 500
    assert response.json()["error"]["code"] == "INTERNAL_ERROR"
    assert response.headers["X-Request-ID"] in caplog.text
    assert "private-test-marker" not in response.text + caplog.text


def test_404_and_405_use_envelope_and_preserve_allow(http):
    missing = http.get("/unknown")
    assert missing.status_code == 404
    assert missing.json()["error"]["code"] == "NOT_FOUND"
    wrong_method = http.get("/value")
    assert wrong_method.status_code == 405
    assert wrong_method.headers["Allow"] == "POST"
    assert wrong_method.json()["error"]["code"] == "METHOD_NOT_ALLOWED"


def test_internal_database_failure_differs_from_lost_connection():
    problem = Exception("private SQL details")
    internal = db_errors.IntegrityError("statement", {}, problem)
    disconnected = db_errors.OperationalError("statement", {}, problem, connection_invalidated=True)
    assert normalize_error(internal).error.code == "DATABASE_ERROR"
    assert normalize_error(disconnected).error.code == "STORAGE_UNAVAILABLE"
