from fastapi import FastAPI

from app.api.health import router as health_router
from app.core.config import get_settings
from app.core.errors import install_error_handlers


def create_app() -> FastAPI:
    get_settings()
    app = FastAPI(title="GymTracker", version="0.1.0", docs_url="/api/v1/docs",
                  redoc_url=None, openapi_url="/api/v1/openapi.json")
    install_error_handlers(app)
    app.include_router(health_router, prefix="/api/v1")
    return app


app = create_app()
