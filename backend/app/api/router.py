from fastapi import APIRouter, Request
from fastapi.routing import APIRoute

from app.core.errors import DomainError, ErrorDTO


class JSONRoute(APIRoute):
    def get_route_handler(self):
        handler = super().get_route_handler()
        if self.body_field is None:
            return handler

        async def require_json(request: Request):
            media_type = request.headers.get("content-type", "").partition(";")[0].strip().lower()
            is_json = media_type == "application/json" or (
                media_type.startswith("application/") and media_type.endswith("+json")
            )
            if not is_json and await request.body():
                raise DomainError("UNSUPPORTED_MEDIA_TYPE")
            return await handler(request)

        return require_json


def api_router() -> APIRouter:
    return APIRouter(route_class=JSONRoute, responses={
        422: {"model": ErrorDTO, "description": "Ошибка полей запроса"},
        500: {"model": ErrorDTO, "description": "Внутренняя ошибка"},
        503: {"model": ErrorDTO, "description": "Хранилище временно недоступно"},
    })
