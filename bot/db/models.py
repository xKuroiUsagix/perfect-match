from typing import Optional

from sqlalchemy.types import DateTime
from sqlalchemy import ForeignKey, String, Integer, Boolean
from sqlalchemy.orm import DeclarativeBase, Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.sql.functions import current_timestamp

from .constants import OTHER, STATE_START, MAX_NAME_LENGTH, MAX_CITY_LENGTH, MAX_DESCRIPTION_LENGTH


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = 'user'

    id: Mapped[int] = mapped_column(primary_key=True)
    telegram_id: Mapped[int] = mapped_column(Integer(), unique=True, index=True)
    chat_id: Mapped[int] = mapped_column(Integer(), unique=True)
    name: Mapped[Optional[str]] = mapped_column(String(MAX_NAME_LENGTH))
    age: Mapped[int] = mapped_column(Integer(), default=0, index=True)
    city: Mapped[Optional[str]] = mapped_column(String(MAX_CITY_LENGTH), index=True)
    gender: Mapped[int] = mapped_column(Integer(), default=OTHER)
    looking_for: Mapped[Optional[int]] = mapped_column(Integer())
    description: Mapped[Optional[str]] = mapped_column(String(MAX_DESCRIPTION_LENGTH))
    created_at: Mapped[DateTime] = mapped_column(DateTime(), server_default=current_timestamp())

    def __repr__(self) -> str:
        return self.telegram_id


class UserLike(Base):
    __tablename__ = 'user_like'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    user_telegram_id: Mapped[int] = mapped_column(ForeignKey('user.telegram_id'), index=True)
    user_liked_telegram_id: Mapped[int] = mapped_column(ForeignKey('user.telegram_id'), index=True)
    is_mutual: Mapped[Optional[bool]] = mapped_column(Boolean())

    def __repr__(self) -> str:
        return f'User {self.user_id} liked User {self.user_liked}'


class UserPhoto(Base):
    __tablename__ = 'user_photo'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    user_telegram_id: Mapped[int] = mapped_column(ForeignKey('user.telegram_id'), index=True)
    photo_id: Mapped[str] = mapped_column(String(64), unique=True)

    def __repr__(self) -> str:
        return f'User {self.user_telegram_id}, Photo {self.photo_id}'


class UserConversation(Base):
    __tablename__ = 'user_conversation'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    chat_id: Mapped[int] = mapped_column(ForeignKey('user.chat_id'), index=True)
    state: Mapped[int] = mapped_column(Integer(), default=STATE_START)
