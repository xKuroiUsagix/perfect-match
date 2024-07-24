from sqlalchemy.orm import Session

from engine import engine
from models import User


async def create_user(username: str, telegram_id: str, chat_id: str):
    with Session(engine) as session:
        user = User(
            username=username,
            telegram_id=telegram_id,
            chat_id=chat_id
        )
        session.add(user)
        session.commit()
