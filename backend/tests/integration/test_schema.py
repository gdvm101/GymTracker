from concurrent.futures import ThreadPoolExecutor
from datetime import date
from threading import Barrier

import pytest
from alembic import command
from sqlalchemy import delete, func, inspect, select, text
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.db.models import Base, Exercise, Program, ProgramExercise, User, Workout, WorkoutExercise, WorkoutSet
from app.tools.seed_exercises import seed_exercises
from tests.db_support import migration_config


def test_migration_round_trip_in_private_schema(db_engine):
    with db_engine.begin() as conn:
        config = migration_config(conn)
        command.check(config)
        assert set(inspect(conn).get_table_names()) == set(Base.metadata.tables) | {"alembic_version"}
        command.downgrade(config, "base")
        assert set(inspect(conn).get_table_names()) == {"alembic_version"}
        command.upgrade(config, "head")
        assert conn.scalar(select(Exercise.name).where(Exercise.id == 10)) == "Жим гантелей"


def test_seed_identifiers_and_edits_survive_reloads(db_engine):
    with Session(db_engine) as db, db.begin():
        assert db.get(Exercise, 10).load_type == "external"
        assert db.get(Exercise, 11).name == "Тяга верхнего блока"
        assert db.scalar(select(func.count()).select_from(User)) == 0
        assert seed_exercises(db) == []
        db.get(Exercise, 10).description = "Текст администратора"
        db.execute(delete(Exercise).where(Exercise.id == 11))
        own = Exercise(name="Дополнительное упражнение")
        db.add(own)
        db.flush()
        assert own.id == 100

    with Session(db_engine) as db, db.begin():
        assert seed_exercises(db) == [11]
        assert seed_exercises(db) == []
    with Session(db_engine) as db:
        assert db.get(Exercise, 10).description == "Текст администратора"
        assert db.get(Exercise, 100).name == "Дополнительное упражнение"
        assert db.scalar(select(func.count()).select_from(Exercise)) == 7


def test_two_seed_processes_restore_one_row(db_engine):
    with db_engine.begin() as conn:
        conn.execute(delete(Exercise).where(Exercise.id == 11))
    ready = Barrier(2)

    def seed():
        with Session(db_engine) as db, db.begin():
            ready.wait(timeout=10)
            return seed_exercises(db)

    with ThreadPoolExecutor(max_workers=2) as pool:
        futures = [pool.submit(seed) for _ in range(2)]
        assert sorted(future.result(timeout=15) for future in futures) == [[], [11]]


def test_deferred_plan_reorder_and_independent_workout(db_engine):
    with Session(db_engine) as db, db.begin():
        user = User(email="a@example.test", password_hash="fixture")
        db.add(user)
        db.flush()
        plan = Program(user_id=user.id, name="Грудь и спина")
        workout = Workout(user_id=user.id, date=date(2026, 10, 9))
        db.add_all([plan, workout])
        db.flush()
        for position, ex_id in enumerate([10, 11], start=1):
            db.add(ProgramExercise(program_id=plan.id, exercise_id=ex_id,
                                   planned_sets=3, planned_reps=8, position=position))
        entry = WorkoutExercise(workout_id=workout.id, exercise_id=10, position=1)
        db.add(entry)
        db.flush()
        db.add(WorkoutSet(workout_exercise_id=entry.id, set_number=1, repetitions=8, weight=32))
        plan_id, workout_id = plan.id, workout.id

    with db_engine.begin() as conn:
        conn.execute(text("SET CONSTRAINTS uq_program_position DEFERRED"))
        conn.execute(text("UPDATE program_exercises SET position = 3 - position WHERE program_id = :p"), {"p": plan_id})
    with Session(db_engine) as db, db.begin():
        assert list(db.scalars(select(ProgramExercise.exercise_id).order_by(ProgramExercise.position))) == [11, 10]
        db.execute(delete(Program).where(Program.id == plan_id))
        assert db.scalar(select(func.count()).select_from(ProgramExercise)) == 0
        assert db.get(Workout, workout_id) is not None
        assert db.scalar(select(WorkoutSet.weight)) == 32
        db.execute(delete(Workout).where(Workout.id == workout_id))
        assert db.scalar(select(func.count()).select_from(WorkoutExercise)) == 0
        assert db.scalar(select(func.count()).select_from(WorkoutSet)) == 0


def test_invalid_reference_rolls_back_transaction(db_engine):
    with pytest.raises(IntegrityError), Session(db_engine) as db, db.begin():
        user = User(email="rollback@example.test", password_hash="fixture")
        db.add(user)
        db.flush()
        db.add(ProgramExercise(program_id=999, exercise_id=10, planned_sets=2, planned_reps=8, position=1))
        db.flush()
    with Session(db_engine) as db:
        assert db.scalar(select(func.count()).select_from(User)) == 0


def test_negative_working_weight_is_rejected_by_database(db_engine):
    with Session(db_engine) as db, db.begin():
        user = User(email="sets@example.test", password_hash="fixture")
        db.add(user)
        db.flush()
        workout = Workout(user_id=user.id, date=date(2026, 10, 9))
        db.add(workout)
        db.flush()
        exercise = WorkoutExercise(workout_id=workout.id, exercise_id=14, position=1)
        db.add(exercise)
        db.flush()
        parent_id = exercise.id
        db.add(WorkoutSet(workout_exercise_id=parent_id, set_number=1, repetitions=0, weight=0))
    with pytest.raises(IntegrityError) as error, Session(db_engine) as db, db.begin():
        db.add(WorkoutSet(workout_exercise_id=parent_id, set_number=2, repetitions=8, weight=-5))
        db.flush()
    assert error.value.orig.diag.constraint_name == "ck_workout_sets_weight"
