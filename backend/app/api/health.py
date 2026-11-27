from typing import Literal

from fastapi import Depends
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.api.router import api_router
from app.db.models import Exercise
from app.db.session import get_db


router = api_router()


class HealthDTO(BaseModel):
    status: Literal["ok"]


@router.get("/health", response_model=HealthDTO, tags=["Стенд"])
def check_health(db: Session = Depends(get_db)) -> HealthDTO:
    """Проверяет подключение и доступ к таблице справочника."""
    db.execute(select(Exercise.id).limit(1))
    return HealthDTO(status="ok")
