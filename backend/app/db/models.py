from datetime import date, datetime
from decimal import Decimal

import sqlalchemy as sa
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    metadata = sa.MetaData(naming_convention={
        "ix": "ix_%(table_name)s_%(column_0_N_name)s",
        "uq": "uq_%(table_name)s_%(column_0_N_name)s",
        "ck": "ck_%(table_name)s_%(constraint_name)s",
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
        "pk": "pk_%(table_name)s",
    })


class User(Base):
    __tablename__ = "users"
    __table_args__ = (
        sa.CheckConstraint("email <> '' AND email = lower(btrim(email))", name="normalized_email"),
        sa.CheckConstraint("role IN ('user', 'admin')", name="role"),
    )

    id: Mapped[int] = mapped_column(sa.BigInteger, sa.Identity(), primary_key=True)
    email: Mapped[str] = mapped_column(sa.String(254), unique=True)
    password_hash: Mapped[str] = mapped_column(sa.String(255))
    role: Mapped[str] = mapped_column(sa.String(20), server_default="user")
    is_blocked: Mapped[bool] = mapped_column(server_default=sa.false())


class Profile(Base):
    __tablename__ = "profiles"
    __table_args__ = (
        sa.CheckConstraint("height > 0", name="positive_height"),
        sa.CheckConstraint("current_weight > 0", name="positive_weight"),
    )

    id: Mapped[int] = mapped_column(sa.BigInteger, sa.Identity(), primary_key=True)
    user_id: Mapped[int] = mapped_column(sa.ForeignKey("users.id", ondelete="CASCADE"), unique=True)
    name: Mapped[str] = mapped_column(sa.String(120), server_default="")
    height: Mapped[Decimal | None] = mapped_column(sa.Numeric(5, 1))
    current_weight: Mapped[Decimal | None] = mapped_column(sa.Numeric(6, 2))
    goal: Mapped[str | None] = mapped_column(sa.String(200))


class AuthSession(Base):
    __tablename__ = "auth_sessions"
    __table_args__ = (sa.Index("ix_auth_sessions_user_id_expires_at", "user_id", "expires_at"),)

    id: Mapped[int] = mapped_column(sa.BigInteger, sa.Identity(), primary_key=True)
    user_id: Mapped[int] = mapped_column(sa.ForeignKey("users.id", ondelete="CASCADE"))
    token_hash: Mapped[str] = mapped_column(sa.String(64), unique=True)
    created_at: Mapped[datetime] = mapped_column(sa.DateTime(timezone=True), server_default=sa.func.now())
    expires_at: Mapped[datetime] = mapped_column(sa.DateTime(timezone=True))
    revoked_at: Mapped[datetime | None] = mapped_column(sa.DateTime(timezone=True))


class Exercise(Base):
    __tablename__ = "exercises"
    __table_args__ = (
        sa.CheckConstraint("length(btrim(name)) > 0", name="name"),
        sa.CheckConstraint("load_type IN ('external', 'bodyweight')", name="load_type"),
    )

    id: Mapped[int] = mapped_column(sa.BigInteger, sa.Identity(start=100), primary_key=True)
    name: Mapped[str] = mapped_column(sa.String(160))
    description: Mapped[str | None] = mapped_column(sa.Text)
    load_type: Mapped[str] = mapped_column(sa.String(20), server_default="external")


class Program(Base):
    __tablename__ = "programs"
    __table_args__ = (sa.CheckConstraint("length(btrim(name)) > 0", name="name"),)

    id: Mapped[int] = mapped_column(sa.BigInteger, sa.Identity(), primary_key=True)
    user_id: Mapped[int] = mapped_column(sa.ForeignKey("users.id", ondelete="CASCADE"), index=True)
    name: Mapped[str] = mapped_column(sa.String(120))


class ProgramExercise(Base):
    __tablename__ = "program_exercises"
    __table_args__ = (
        sa.UniqueConstraint("program_id", "position", name="uq_program_position",
                            deferrable=True, initially="IMMEDIATE"),
        sa.CheckConstraint("position > 0", name="position"),
        sa.CheckConstraint("planned_sets > 0", name="planned_sets"),
        sa.CheckConstraint("planned_reps >= 0", name="planned_reps"),
    )

    id: Mapped[int] = mapped_column(sa.BigInteger, sa.Identity(), primary_key=True)
    program_id: Mapped[int] = mapped_column(sa.ForeignKey("programs.id", ondelete="CASCADE"))
    exercise_id: Mapped[int] = mapped_column(sa.ForeignKey("exercises.id"))
    planned_sets: Mapped[int]
    planned_reps: Mapped[int]
    position: Mapped[int]


class Workout(Base):
    __tablename__ = "workouts"
    __table_args__ = (sa.Index("ix_workouts_user_id_date_id", "user_id", "date", "id"),)

    id: Mapped[int] = mapped_column(sa.BigInteger, sa.Identity(), primary_key=True)
    user_id: Mapped[int] = mapped_column(sa.ForeignKey("users.id", ondelete="CASCADE"))
    date: Mapped[date] = mapped_column(sa.Date)
    comment: Mapped[str | None] = mapped_column(sa.Text)


class WorkoutExercise(Base):
    __tablename__ = "workout_exercises"
    __table_args__ = (
        sa.UniqueConstraint("workout_id", "position"),
        sa.CheckConstraint("position > 0", name="position"),
        sa.Index("ix_workout_exercises_exercise_id_workout_id", "exercise_id", "workout_id"),
    )

    id: Mapped[int] = mapped_column(sa.BigInteger, sa.Identity(), primary_key=True)
    workout_id: Mapped[int] = mapped_column(sa.ForeignKey("workouts.id", ondelete="CASCADE"))
    exercise_id: Mapped[int] = mapped_column(sa.ForeignKey("exercises.id"))
    position: Mapped[int]


class WorkoutSet(Base):
    __tablename__ = "workout_sets"
    __table_args__ = (
        sa.UniqueConstraint("workout_exercise_id", "set_number"),
        sa.CheckConstraint("set_number > 0", name="set_number"),
        sa.CheckConstraint("repetitions >= 0", name="repetitions"),
        sa.CheckConstraint("weight >= 0", name="weight"),
    )

    id: Mapped[int] = mapped_column(sa.BigInteger, sa.Identity(), primary_key=True)
    workout_exercise_id: Mapped[int] = mapped_column(sa.ForeignKey("workout_exercises.id", ondelete="CASCADE"))
    set_number: Mapped[int]
    repetitions: Mapped[int]
    weight: Mapped[Decimal] = mapped_column(sa.Numeric(7, 2))


class UserSettings(Base):
    __tablename__ = "user_settings"

    id: Mapped[int] = mapped_column(sa.BigInteger, sa.Identity(), primary_key=True)
    user_id: Mapped[int] = mapped_column(sa.ForeignKey("users.id", ondelete="CASCADE"), unique=True)
    show_weight_to_friends: Mapped[bool] = mapped_column(server_default=sa.false())
    show_stats_to_friends: Mapped[bool] = mapped_column(server_default=sa.false())


class BodyWeightMeasurement(Base):
    __tablename__ = "body_weight_measurements"
    __table_args__ = (
        sa.UniqueConstraint("user_id", "measured_on"),
        sa.CheckConstraint("weight > 0", name="positive_weight"),
    )

    id: Mapped[int] = mapped_column(sa.BigInteger, sa.Identity(), primary_key=True)
    user_id: Mapped[int] = mapped_column(sa.ForeignKey("users.id", ondelete="CASCADE"))
    measured_on: Mapped[date] = mapped_column(sa.Date)
    weight: Mapped[Decimal] = mapped_column(sa.Numeric(6, 2))
