from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.orm import Session

from app.db.models import Exercise


class TrainingRepository:
    def __init__(self, db: Session):
        self.db = db

    def insert_missing_exercises(self, rows: list[dict]) -> list[int]:
        # The unique index arbitrates two concurrent seed runs.
        statement = (insert(Exercise).values(rows)
                     .on_conflict_do_nothing(index_elements=[Exercise.id])
                     .returning(Exercise.id))
        return list(self.db.scalars(statement))
