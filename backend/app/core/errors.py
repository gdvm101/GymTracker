import logging
from uuid import uuid4

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from sqlalchemy import exc as db_errors
from starlette.exceptions import HTTPException


logger = logging.getLogger("gymtracker.errors")

ERRORS = {
    "BAD_JSON": (400, "Проверьте синтаксис JSON."),
    "INVALID_CREDENTIALS": (401, "Неверный e-mail или пароль."),
    "UNAUTHENTICATED": (401, "Войдите в аккаунт."),
    "SESSION_EXPIRED": (401, "Срок сеанса истёк. Войдите снова."),
    "ACCOUNT_BLOCKED": (403, "Аккаунт заблокирован."),
    "FORBIDDEN": (403, "Недостаточно прав для этого действия."),
    "CSRF_FAILED": (403, "Не удалось подтвердить запрос."),
    "NOT_FOUND": (404, "Запись или адрес не найдены."),
    "METHOD_NOT_ALLOWED": (405, "Этот HTTP-метод недоступен."),
    "EMAIL_TAKEN": (409, "Этот e-mail уже зарегистрирован."),
    "CONFLICT": (409, "Данные изменились. Проверьте актуальную запись."),
    "UNSUPPORTED_MEDIA_TYPE": (415, "Передайте тело запроса в формате JSON."),
    "INVALID_INPUT": (422, "Проверьте введённое значение."),
    "DATABASE_ERROR": (500, "Не удалось выполнить операцию с базой данных."),
    "INTERNAL_ERROR": (500, "Не удалось обработать запрос."),
    "STORAGE_UNAVAILABLE": (503, "База данных временно недоступна."),
}

HTTP_CODES = {
    400: "BAD_JSON", 401: "UNAUTHENTICATED", 403: "FORBIDDEN", 404: "NOT_FOUND",
    405: "METHOD_NOT_ALLOWED", 409: "CONFLICT", 415: "UNSUPPORTED_MEDIA_TYPE",
    422: "INVALID_INPUT", 500: "INTERNAL_ERROR", 503: "STORAGE_UNAVAILABLE",
}


class ErrorBody(BaseModel):
    code: str
    message: str
    details: dict | None = None


class ErrorDTO(BaseModel):
    error: ErrorBody


class DomainError(Exception):
    def __init__(self, code: str, *, field: str | None = None):
        if code not in ERRORS:
            raise ValueError("Неизвестный код ошибки")
        super().__init__(code)
        self.code = code
        self.field = field


def database_code(exc: db_errors.SQLAlchemyError) -> str:
    if isinstance(exc, db_errors.TimeoutError):
        return "STORAGE_UNAVAILABLE"
    if isinstance(exc, db_errors.DBAPIError):
        state = getattr(exc.orig, "sqlstate", None) or ""
        if (exc.connection_invalidated or state.startswith(("08", "53"))
                or state in {"57P01", "57P02", "57P03"}
                or (not state and isinstance(exc, db_errors.OperationalError))):
            return "STORAGE_UNAVAILABLE"
    return "DATABASE_ERROR"


def normalize_error(exc: Exception) -> ErrorDTO:
    field = None
    if isinstance(exc, DomainError):
        code, field = exc.code, exc.field
    elif isinstance(exc, RequestValidationError):
        first = next(iter(exc.errors()), {})
        if first.get("type") == "json_invalid":
            code = "BAD_JSON"
        else:
            code = "INVALID_INPUT"
            path = first.get("loc", ())
            parts = path[1:] if path and path[0] in {"body", "query", "path", "header", "cookie"} else path
            field = ".".join(str(part) for part in parts) or (str(path[0]) if path else "body")
    elif isinstance(exc, db_errors.SQLAlchemyError):
        code = database_code(exc)
    elif isinstance(exc, HTTPException):
        code = HTTP_CODES.get(exc.status_code, "HTTP_ERROR")
    else:
        code = "INTERNAL_ERROR"
    message = ERRORS[code][1] if code in ERRORS else "Не удалось выполнить запрос."
    return ErrorDTO(error=ErrorBody(code=code, message=message, details={"field": field} if field else None))


def error_response(request: Request, exc: Exception) -> JSONResponse:
    dto = normalize_error(exc)
    code = dto.error.code
    status = exc.status_code if isinstance(exc, HTTPException) else ERRORS[code][0]
    # Never log the exception message. It may contain SQL parameters or a request body.
    request_id = request.state.request_id
    logger.log(logging.ERROR if status >= 500 else logging.INFO,
               "request_id=%s code=%s cause=%s", request_id, code, type(exc).__name__)
    headers = dict(exc.headers or {}) if isinstance(exc, HTTPException) else {}
    headers["X-Request-ID"] = request_id
    return JSONResponse(dto.model_dump(), status_code=status, headers=headers)


def install_error_handlers(app: FastAPI) -> None:
    for error_type in (DomainError, RequestValidationError, HTTPException, db_errors.SQLAlchemyError):
        app.add_exception_handler(error_type, error_response)

    @app.middleware("http")
    async def identify_request(request: Request, call_next):
        request.state.request_id = uuid4().hex
        try:
            response = await call_next(request)
        except Exception as exc:
            return error_response(request, exc)
        response.headers["X-Request-ID"] = request.state.request_id
        return response
