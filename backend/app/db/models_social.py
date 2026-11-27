"""Tables reserved by the architecture. Their HTTP routes belong to M/L."""

from datetime import datetime

import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column

from app.db.models import Base


class FriendLink(Base):
    __tablename__ = "friend_links"
    __table_args__ = (
        sa.CheckConstraint("sender_id <> recipient_id", name="distinct_users"),
        sa.CheckConstraint("status IN ('pending', 'accepted', 'rejected')", name="status"),
        sa.Index("ix_friend_links_recipient_id_status", "recipient_id", "status"),
    )

    id: Mapped[int] = mapped_column(sa.BigInteger, sa.Identity(), primary_key=True)
    sender_id: Mapped[int] = mapped_column(sa.ForeignKey("users.id", ondelete="CASCADE"))
    recipient_id: Mapped[int] = mapped_column(sa.ForeignKey("users.id", ondelete="CASCADE"))
    status: Mapped[str] = mapped_column(sa.String(20), server_default="pending")
    created_at: Mapped[datetime] = mapped_column(sa.DateTime(timezone=True), server_default=sa.func.now())


sa.Index("uq_friend_pair", sa.func.least(FriendLink.sender_id, FriendLink.recipient_id),
         sa.func.greatest(FriendLink.sender_id, FriendLink.recipient_id), unique=True)


class UserAchievement(Base):
    __tablename__ = "user_achievements"

    user_id: Mapped[int] = mapped_column(sa.ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
    code: Mapped[str] = mapped_column(sa.String(40), primary_key=True)
    awarded_at: Mapped[datetime] = mapped_column(sa.DateTime(timezone=True), server_default=sa.func.now())


class TrainingGroup(Base):
    __tablename__ = "training_groups"
    __table_args__ = (sa.CheckConstraint("length(btrim(name)) > 0", name="name"),)

    id: Mapped[int] = mapped_column(sa.BigInteger, sa.Identity(), primary_key=True)
    name: Mapped[str] = mapped_column(sa.String(120))
    created_by: Mapped[int] = mapped_column(sa.ForeignKey("users.id"))
    created_at: Mapped[datetime] = mapped_column(sa.DateTime(timezone=True), server_default=sa.func.now())


class GroupMember(Base):
    __tablename__ = "group_members"

    group_id: Mapped[int] = mapped_column(sa.ForeignKey("training_groups.id", ondelete="CASCADE"), primary_key=True)
    user_id: Mapped[int] = mapped_column(sa.ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
    joined_at: Mapped[datetime] = mapped_column(sa.DateTime(timezone=True), server_default=sa.func.now())


class Notification(Base):
    __tablename__ = "notifications"
    __table_args__ = (sa.UniqueConstraint("user_id", "kind", "subject_id"),)

    id: Mapped[int] = mapped_column(sa.BigInteger, sa.Identity(), primary_key=True)
    user_id: Mapped[int] = mapped_column(sa.ForeignKey("users.id", ondelete="CASCADE"))
    kind: Mapped[str] = mapped_column(sa.String(40))
    subject_id: Mapped[str] = mapped_column(sa.String(80))
    created_at: Mapped[datetime] = mapped_column(sa.DateTime(timezone=True), server_default=sa.func.now())
