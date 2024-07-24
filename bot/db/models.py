from typing import Optional, List

from sqlalchemy.types import DateTime
from sqlalchemy import ForeignKey, String, Integer, Column, Table
from sqlalchemy.orm import DeclarativeBase, Mapped
from sqlalchemy.orm import mapped_column, relationship
from sqlalchemy.sql.functions import current_timestamp


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = 'user'

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(128), unique=True)
    telegram_id: Mapped[str] = mapped_column(String(32), unique=True)
    chat_id: Mapped[str] = mapped_column(String(32), unique=True)
    age: Mapped[int] = mapped_column(Integer(), default=0)
    city: Mapped[Optional[str]] = mapped_column(String(64))
    gender: Mapped[int] = mapped_column(Integer())
    looking_for: Mapped[int] = mapped_column(Integer())
    description: Mapped[str] = mapped_column(String(512))
    photo_message_id: Mapped[Optional[str]] = mapped_column(String(32), unique=True)
    created_at: Mapped[DateTime] = mapped_column(DateTime(), server_default=current_timestamp())
    received_likes: Mapped[int] = mapped_column(Integer(), default=0)
    liked_others: Mapped[int] = mapped_column(Integer(), default=0)

    def __repr__(self) -> str:
        return self.username


class UserLike(Base):
    __tablename__ = 'user_like'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('user.id'))
    user_liked: Mapped[int] = mapped_column(ForeignKey('user.id'))

    def __repr__(self) -> str:
        return f'User {self.user_id} liked User {self.user_liked}'
