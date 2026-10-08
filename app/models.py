from datetime import datetime
from sqlalchemy import String, BigInteger, Boolean, Integer, DateTime, Text, ForeignKey, UniqueConstraint, JSON
from sqlalchemy.orm import Mapped, mapped_column
from .db import Base

class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    telegram_id: Mapped[int] = mapped_column(BigInteger, unique=True, index=True)
    username: Mapped[str | None] = mapped_column(String(255))
    display_name: Mapped[str | None] = mapped_column(String(255))
    status: Mapped[str] = mapped_column(String(20), default="active")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    last_seen_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

class UserPermission(Base):
    __tablename__ = "user_permissions"
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), unique=True)
    add_channel: Mapped[bool] = mapped_column(Boolean, default=True)
    remove_channel: Mapped[bool] = mapped_column(Boolean, default=True)
    link_reaction: Mapped[bool] = mapped_column(Boolean, default=True)
    channels: Mapped[bool] = mapped_column(Boolean, default=True)
    settings: Mapped[bool] = mapped_column(Boolean, default=True)
    help: Mapped[bool] = mapped_column(Boolean, default=True)
    contact_admin: Mapped[bool] = mapped_column(Boolean, default=True)
    add_bot: Mapped[bool] = mapped_column(Boolean, default=False)
    remove_bot: Mapped[bool] = mapped_column(Boolean, default=False)
    users: Mapped[bool] = mapped_column(Boolean, default=False)
    add_user: Mapped[bool] = mapped_column(Boolean, default=False)
    ban_user: Mapped[bool] = mapped_column(Boolean, default=False)
    permission: Mapped[bool] = mapped_column(Boolean, default=False)

class UserSetting(Base):
    __tablename__ = "user_settings"
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), unique=True)
    reaction_rate: Mapped[int] = mapped_column(Integer, default=80)
    default_delay_seconds: Mapped[int] = mapped_column(Integer, default=1800)
    allowed_reactions: Mapped[list] = mapped_column(JSON, default=lambda: ["👍"])

class Channel(Base):
    __tablename__ = "channels"
    id: Mapped[int] = mapped_column(primary_key=True)
    owner_user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True)
    telegram_chat_id: Mapped[int] = mapped_column(BigInteger)
    username: Mapped[str | None] = mapped_column(String(255))
    title: Mapped[str | None] = mapped_column(String(255))
    status: Mapped[str] = mapped_column(String(20), default="active")
    monitor_enabled: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    __table_args__ = (UniqueConstraint("owner_user_id", "telegram_chat_id"),)

class BotToken(Base):
    __tablename__ = "bots"
    id: Mapped[int] = mapped_column(primary_key=True)
    token_hash: Mapped[str] = mapped_column(String(64), unique=True)
    encrypted_token: Mapped[str] = mapped_column(Text)
    telegram_bot_id: Mapped[int | None] = mapped_column(BigInteger)
    username: Mapped[str | None] = mapped_column(String(255))
    status: Mapped[str] = mapped_column(String(20), default="active")
    failure_count: Mapped[int] = mapped_column(Integer, default=0)
    last_error: Mapped[str | None] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    disabled_at: Mapped[datetime | None] = mapped_column(DateTime)
    disable_reason: Mapped[str | None] = mapped_column(String(255))

class Job(Base):
    __tablename__ = "jobs"
    id: Mapped[int] = mapped_column(primary_key=True)
    owner_user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True)
    channel_id: Mapped[int | None] = mapped_column(ForeignKey("channels.id"))
    message_id: Mapped[int] = mapped_column(BigInteger)
    message_link: Mapped[str | None] = mapped_column(Text)
    target_count: Mapped[int] = mapped_column(Integer)
    success_count: Mapped[int] = mapped_column(Integer, default=0)
    failed_count: Mapped[int] = mapped_column(Integer, default=0)
    status: Mapped[str] = mapped_column(String(20), default="pending")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    started_at: Mapped[datetime | None] = mapped_column(DateTime)
    deadline_at: Mapped[datetime | None] = mapped_column(DateTime)
    completed_at: Mapped[datetime | None] = mapped_column(DateTime)
    __table_args__ = (UniqueConstraint("owner_user_id", "channel_id", "message_id"),)

class ReactionTask(Base):
    __tablename__ = "reaction_tasks"
    id: Mapped[int] = mapped_column(primary_key=True)
    job_id: Mapped[int] = mapped_column(ForeignKey("jobs.id"), index=True)
    bot_id: Mapped[int] = mapped_column(ForeignKey("bots.id"))
    reaction: Mapped[str] = mapped_column(String(50))
    scheduled_at: Mapped[datetime] = mapped_column(DateTime, index=True)
    status: Mapped[str] = mapped_column(String(20), default="scheduled")
    attempt_count: Mapped[int] = mapped_column(Integer, default=0)
    executed_at: Mapped[datetime | None] = mapped_column(DateTime)
    error_code: Mapped[str | None] = mapped_column(String(100))
    error_message: Mapped[str | None] = mapped_column(Text)
    __table_args__ = (UniqueConstraint("job_id", "bot_id"),)
