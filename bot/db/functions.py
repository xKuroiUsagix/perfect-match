from typing import Optional, List

from sqlalchemy import select, delete
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import Session
from sqlalchemy import func

from .engine import engine
from .models import User, UserLike, UserPhoto
from .constants import USER_MAXIMUM_AGE, USER_MINIMUM_AGE, PHOTO_LIMIT, GENDER_CHOICES


def create_user_if_not_exists(telegram_id: str, chat_id: str) -> Optional[User]:
    with Session(engine) as session:
        query = select(User).where(User.telegram_id == telegram_id)
        user_exists = session.execute(query).scalar_one_or_none() is not None

        if user_exists:
            return

        user = User(
            telegram_id=telegram_id,
            chat_id=chat_id
        )
        session.add(user)
        session.commit()
        return user


def get_user(telegram_id: str) -> Optional[User]:
    with Session(engine) as session:
        query = select(User).where(User.telegram_id == telegram_id)
        user_row = session.execute(query).one()
        return user_row[0]


def is_user_exists(telegram_id: str) -> bool:
    with Session(engine) as session:
        query = select(User).where(User.telegram_id == telegram_id)
        user_row = session.execute(query).one_or_none()
        return user_row is not None


def create_user_like_if_not_exists(user_telegram_id: str, user_liked_telegram_id: str) -> Optional[UserLike]:
    if user_telegram_id == user_liked_telegram_id:
        raise ValueError(
            'Arguments user_telegram_id and user_liked_telegram_id are the same. User cannot like themselves :)'
        )

    with Session(engine) as session:
        if not is_user_exists(user_telegram_id):
            raise NoResultFound(f'User {user_telegram_id} does not exist.')
        if not is_user_exists(user_liked_telegram_id):
            raise NoResultFound(f'User {user_liked_telegram_id} does not exist.')

        query = select(UserLike).where(
            UserLike.user_telegram_id == user_telegram_id, 
            UserLike.user_liked_telegram_id == user_liked_telegram_id
        )
        record_exists = session.execute(query).scalar_one_or_none() is not None
        
        if record_exists:
            return

        user_like = UserLike(
            user_telegram_id=user_telegram_id,
            user_liked_telegram_id=user_liked_telegram_id
        )

        session.add_all(user_like)
        session.commit()
        return user_like


def get_user_like(telegram_id: str) -> List[UserLike]:
    if not is_user_exists(telegram_id):
        raise NoResultFound(f'User {telegram_id} does not exist.')

    with Session(engine) as session:
        query = select(UserLike).where(UserLike.user_telegram_id == telegram_id)
        return session.execute(query).scalars().all()


def user_set_age(telegram_id: str, age: int) -> None:
    if not is_user_exists(telegram_id):
        raise NoResultFound(f'User {telegram_id} does not exist.')
    if age < USER_MINIMUM_AGE:
        raise ValueError(f'The user is too young. Minimal age is {USER_MINIMUM_AGE}')
    if age > USER_MAXIMUM_AGE:
        raise ValueError(f'This age does not look real. Maximum age is {USER_MAXIMUM_AGE}')
    
    with Session(engine) as session:
        user = get_user(telegram_id)
        user.age = age
        
        session.add(user)
        session.commit()


def user_set_description(telegram_id: str, description: str) -> None:
    if not is_user_exists(telegram_id):
        raise NoResultFound(f'User {telegram_id} does not exist.')
    
    with Session(engine) as session:
        user = get_user(telegram_id)
        user.description = description
        session.add(user)
        session.commit()


def user_set_city(telegram_id: str, city: str) -> None:
    if not is_user_exists(telegram_id):
        raise NoResultFound(f'User {telegram_id} does not exist.')
    
    with Session(engine) as session:
        user = get_user(telegram_id)
        user.city = city
        session.add(user)
        session.commit()


def user_set_gender(telegram_id: str, gender: int) -> None:
    if gender not in GENDER_CHOICES.values():
        raise ValueError(f'Gender {gender} is not valid.')
    if not is_user_exists(telegram_id):
        raise NoResultFound(f'User {telegram_id} does not exist.')
    
    with Session(engine) as session:
        user = get_user(telegram_id)
        user.gender = gender
        session.add(user)
        session.commit()


def user_set_looking_for(telegram_id: str, gender: int) -> None:
    if gender not in GENDER_CHOICES.values():
        raise ValueError(f'Gender {gender} is not valid.')
    if not is_user_exists(telegram_id):
        raise NoResultFound(f'User {telegram_id} does not exist.')
    
    with Session(engine) as session:
        user = get_user(telegram_id)
        user.looking_for = gender
        session.add(user)
        session.commit()


def user_set_name(telegram_id: str, name: str) -> None:
    if not is_user_exists(telegram_id):
        raise NoResultFound(f'User {telegram_id} does not exist.')
    
    with Session(engine) as session:
        user = get_user(telegram_id)
        user.name = name
        session.add(user)
        session.commit()


def is_user_reached_photo_limit(telegram_id: str) -> bool:
    if not is_user_exists(telegram_id):
        raise NoResultFound(f'User {telegram_id} does not exist.')
    
    with Session(engine) as session:
        query = select(func.count(UserPhoto.id)).where(UserPhoto.user_telegram_id == telegram_id)
        result = session.execute(query).scalar()

        return result >= PHOTO_LIMIT


def user_add_photo(telegram_id: str, photo_id: str) -> None:
    if not is_user_exists(telegram_id):
        raise NoResultFound(f'User {telegram_id} does not exist.')
    if is_user_reached_photo_limit(telegram_id):
        raise ValueError(f'This user has reached photo limit, which equals to {PHOTO_LIMIT}')
    
    with Session(engine) as session:
        user_photo = UserPhoto(
            user_telegram_id=telegram_id,
            photo_id=photo_id
        )
        session.add(user_photo)
        session.commit()


def get_user_photo(telegram_id: str, photo_id: str) -> UserPhoto:
    if not is_user_exists(telegram_id):
        raise NoResultFound(f'User {telegram_id} does not exist.')
    
    with Session(engine) as session:
        query = select(UserPhoto).where(
            UserPhoto.user_telegram_id == telegram_id,
            UserPhoto.photo_id == photo_id
        )
        user_photo = session.execute(query).one()
        return user_photo[0]


def get_user_photo_list(telegram_id: str) -> List[UserPhoto]:
    if not is_user_exists(telegram_id):
        raise NoResultFound(f'User {telegram_id} does not exist.')

    with Session(engine) as session:
        query = select(UserPhoto).where(UserPhoto.user_telegram_id == telegram_id)
        return session.execute(query).scalars().all()


def user_delete_photos(telegram_id: str, photos: List[str]) -> None:
    if not is_user_exists(telegram_id):
        raise NoResultFound(f'User {telegram_id} does not exist.')
    
    with Session(engine) as session:
        query = delete(UserPhoto).where(
            UserPhoto.user_telegram_id == telegram_id, 
            UserPhoto.photo_id.in_(photos)
        )
        session.execute(query)


def user_change_photo(telegram_id: str, current_photo_id: str, new_photo_id: str) -> None:
    if not is_user_exists(telegram_id):
        raise NoResultFound(f'User {telegram_id} does not exist.')
    
    with Session(engine) as session:
        user_photo = get_user_photo(telegram_id, current_photo_id)
        user_photo.photo_id = new_photo_id
        session.add(user_photo)
        session.commit()


def get_likes_for_user(telegram_id: str) -> List[UserLike]:
    if not is_user_exists(telegram_id):
        raise NoResultFound(f'User {telegram_id} does not exist.')
    
    with Session(engine) as session:
        query = select(UserLike).where(UserLike.user_liked_telegram_id == telegram_id)
        return session.execute(query).scalars().all()


def get_mutual_likes(telegram_id: str) -> List[UserLike]:
    if not is_user_exists(telegram_id):
        raise NoResultFound(f'User {telegram_id} does not exist.')
    
    with Session(engine) as session:
        query = select(UserLike).where(
            UserLike.user_telegram_id == telegram_id,
            UserLike.is_mutual == True
        )
        return session.execute(query).scalars().all()


def set_user_like_is_mutual(current_user_id: str, like_recieved_from_id: str, is_mutual: bool) -> None:
    if not is_user_exists(current_user_id):
        raise NoResultFound(f'User {current_user_id} does not exist.')
    if not is_user_exists(like_recieved_from_id):
        raise NoResultFound(f'User {like_recieved_from_id} does not exist.')
    
    with Session(engine) as session:
        query = select(UserLike).where(
            UserLike.user_liked_telegram_id == current_user_id,
            UserLike.user_telegram_id == like_recieved_from_id,
        )
        user_like = session.execute(query).scalars().first()

        if user_like is None:
            raise ValueError('There are no such record in UserLike table.')
        
        user_like.is_mutual = is_mutual
        session.add(user_like)
        session.commit()
