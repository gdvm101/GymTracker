from sqlalchemy.orm import Session

from app.db.seed import read_exercises
from app.db.session import session_factory
from app.repositories.training import TrainingRepository


def seed_exercises(db: Session) -> list[int]:
    return TrainingRepository(db).insert_missing_exercises(read_exercises())


def main() -> None:
    with session_factory().begin() as db:
        inserted = seed_exercises(db)
    print(f"Справочник упражнений готов. Добавлено записей: {len(inserted)}.")


if __name__ == "__main__":
    main()
