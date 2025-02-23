from telebot.types import (
    Message,
    ReplyKeyboardRemove,
)

from db.functions import (
    set_user_age,
    set_user_name,
    set_user_gender,
    set_user_looking_for,
    set_user_city,
    set_user_description,
    add_user_photo,
    get_user_photo_list,
    update_user_conversation_state,
    delete_user_conversation_state,
    get_user_conversation_state,
    delete_all_user_photos
)
from db.constants import (
    PHOTO_LIMIT, 
    USER_MINIMUM_AGE, 
    USER_MAXIMUM_AGE,
    MAX_DESCRIPTION_LENGTH,
    MAX_NAME_LENGTH,
    MAX_CITY_LENGTH,
    STATE_START, 
    STATE_FINISH, 
    STATE_INTERNET_WARNING, 
    STATE_ASK_NAME,
    STATE_ASK_AGE, 
    STATE_ASK_GENDER, 
    STATE_ASK_LOOKING_FOR, 
    STATE_ASK_CITY,
    STATE_ASK_DESCRIPTION, 
    STATE_ASK_PHOTOS, 
    STATE_HANDLING_PHOTOS,
    STATE_UPDATE_DESCRIPTION,
    STATE_UPDATE_NAME,
    STATE_UPDATE_AGE,
    STATE_UPDATE_CITY,
    STATE_UPDATE_PHOTOS,
)
from bot_insatnce import bot
from keyboards import (
    GENDER_CHOICE_KEYBOARD,
    INTERNET_WARNING_KEYBOARD
)

from .messages import (
    NOT_A_NUMBER, 
    STATE_MESSAGES, 
    TOO_YOUNG_MESSAGE, 
    TOO_MANY_PHOTOS, 
    PHOTOS_SAVED_MESSAGE,
    WRONG_GENDER_MESSAGE,
    INNAPROPRIATE_AGE_MESSAGE,
    TOO_LONG_NAME_MESSAGE,
    TOO_LONG_CITY_MESSAGE,
    TOO_LONG_DESCRIPTION_MESSAGE,
    UPDATE_SAVED_MESSAGE,
    PHOTO_IS_REQUIRED
)
from .helpers import get_gender


async def handle_user_conversation(message: Message) -> None:
    chat_id = message.chat.id
    user_id = message.from_user.id
    conversation_state = get_user_conversation_state(chat_id)
    
    if conversation_state == STATE_START:
        await _handle_initial_message(chat_id)
    elif conversation_state == STATE_INTERNET_WARNING:
        await _handle_internet_warning(chat_id)
    elif conversation_state == STATE_ASK_NAME:
        await _handle_name(chat_id, user_id, message.text)
    elif conversation_state == STATE_ASK_AGE:
        await _handle_age(chat_id, user_id, message.text)
    elif conversation_state == STATE_ASK_GENDER:
        await _handle_gender(chat_id, user_id, get_gender(message.text))
    elif conversation_state == STATE_ASK_LOOKING_FOR:
        await _handle_looking_for(chat_id, user_id, get_gender(message.text))
    elif conversation_state == STATE_ASK_CITY:
        await _handle_city(chat_id, user_id, message.text.lower())
    elif conversation_state == STATE_ASK_DESCRIPTION:
        await _handle_description(chat_id, user_id, message.text)
    elif conversation_state in (STATE_ASK_PHOTOS, STATE_HANDLING_PHOTOS):
        await _handle_photos(message, chat_id, user_id)
    elif conversation_state == STATE_UPDATE_NAME:
        await _handle_update_name(chat_id, user_id, message.text)
    elif conversation_state == STATE_UPDATE_DESCRIPTION:
        await _handle_update_description(chat_id, user_id, message.text)
    elif conversation_state == STATE_UPDATE_AGE:
        await _handle_update_age(chat_id, user_id, message.text)
    elif conversation_state == STATE_UPDATE_CITY:
        await _handle_update_city(chat_id, user_id, message.text.lower())
    elif conversation_state == STATE_UPDATE_PHOTOS:
        await _handle_update_photos(message, chat_id, user_id)


async def _handle_initial_message(chat_id: str) -> None:
    update_user_conversation_state(chat_id, STATE_INTERNET_WARNING)

    response = STATE_MESSAGES.get(STATE_INTERNET_WARNING)
    await bot.send_message(chat_id, response, reply_markup=INTERNET_WARNING_KEYBOARD)


async def _handle_internet_warning(chat_id: str) -> None:
    update_user_conversation_state(chat_id, STATE_ASK_NAME)
    
    response = STATE_MESSAGES.get(STATE_ASK_NAME)
    await bot.send_message(chat_id, response, reply_markup=ReplyKeyboardRemove())


async def _handle_name(chat_id: str, user_id: str, name: str) -> None:
    if len(name) > MAX_NAME_LENGTH:
        await bot.send_message(chat_id, TOO_LONG_NAME_MESSAGE)
        return

    set_user_name(user_id, name)
    update_user_conversation_state(chat_id, STATE_ASK_AGE)
    
    response = STATE_MESSAGES.get(STATE_ASK_AGE)
    await bot.send_message(chat_id, response)


async def _handle_age(chat_id: str, user_id: str, age: int) -> None: 
    try:
        age = int(age)
    except ValueError:
        await bot.send_message(chat_id, NOT_A_NUMBER)
        return
    
    if age < USER_MINIMUM_AGE:
        delete_user_conversation_state(chat_id)
        await bot.send_message(chat_id, TOO_YOUNG_MESSAGE)
        return
    if age > USER_MAXIMUM_AGE:
        await bot.send_message(chat_id, INNAPROPRIATE_AGE_MESSAGE)
        return

    set_user_age(user_id, age)
    update_user_conversation_state(chat_id, STATE_ASK_GENDER)
    
    response = STATE_MESSAGES.get(STATE_ASK_GENDER)
    await bot.send_message(chat_id, response, reply_markup=GENDER_CHOICE_KEYBOARD)


async def _handle_gender(chat_id: str, user_id: str, gender: int) -> None:
    if gender is None:
        await bot.send_message(chat_id, WRONG_GENDER_MESSAGE, reply_markup=GENDER_CHOICE_KEYBOARD)
        return
    
    set_user_gender(user_id, gender)
    update_user_conversation_state(chat_id, STATE_ASK_LOOKING_FOR)

    response = STATE_MESSAGES.get(STATE_ASK_LOOKING_FOR)
    await bot.send_message(chat_id, response, reply_markup=GENDER_CHOICE_KEYBOARD)


async def _handle_looking_for(chat_id: str, user_id: str, gender: int) -> None:
    if gender is None:
        await bot.send_message(chat_id, WRONG_GENDER_MESSAGE, reply_markup=GENDER_CHOICE_KEYBOARD)
        return

    set_user_looking_for(user_id, gender)
    update_user_conversation_state(chat_id, STATE_ASK_CITY)
    
    response = STATE_MESSAGES.get(STATE_ASK_CITY)
    await bot.send_message(chat_id, response, reply_markup=ReplyKeyboardRemove())


async def _handle_city(chat_id: str, user_id: str, city: str) -> None:
    if len(city) > MAX_CITY_LENGTH:
        await bot.send_message(chat_id, TOO_LONG_CITY_MESSAGE)
        return

    set_user_city(user_id, city)
    update_user_conversation_state(chat_id, STATE_ASK_DESCRIPTION)
    
    response = STATE_MESSAGES.get(STATE_ASK_DESCRIPTION)
    await bot.send_message(chat_id, response)


async def _handle_description(chat_id: str, user_id: str, description: str) -> None:
    if len(description) > MAX_DESCRIPTION_LENGTH:
        await bot.send_message(chat_id, TOO_LONG_DESCRIPTION_MESSAGE)
        return

    set_user_description(user_id, description)
    update_user_conversation_state(chat_id, STATE_ASK_PHOTOS)
    
    response = STATE_MESSAGES.get(STATE_ASK_PHOTOS)
    await bot.send_message(chat_id, response)

    
async def _handle_photos(message: Message, chat_id: str, user_id: str) -> None:
    update_user_conversation_state(chat_id, STATE_HANDLING_PHOTOS)
    user_photos = get_user_photo_list(user_id)
    
    if len(user_photos) == 0 and message.photo is None:
        await bot.send_message(chat_id, PHOTO_IS_REQUIRED)
        return
    
    if len(user_photos) >= 1 and message.photo is None:
        update_user_conversation_state(chat_id, STATE_FINISH)
        return
    
    if len(user_photos) == PHOTO_LIMIT:
        update_user_conversation_state(chat_id, STATE_FINISH)
        await bot.send_message(chat_id, TOO_MANY_PHOTOS)
        return
    
    photo_id = message.photo[0].file_id
    add_user_photo(user_id, photo_id)
    
    if len(user_photos) == 1:
        await bot.send_message(chat_id, PHOTOS_SAVED_MESSAGE)

        response = STATE_MESSAGES.get(STATE_FINISH)
        await bot.send_message(chat_id, response)


async def _handle_update_name(chat_id: str, user_id: str, name: str) -> None:
    if len(name) > MAX_NAME_LENGTH:
        await bot.send_message(chat_id, TOO_LONG_NAME_MESSAGE)
        return

    set_user_name(user_id, name)
    update_user_conversation_state(chat_id, STATE_FINISH)

    await bot.send_message(chat_id, UPDATE_SAVED_MESSAGE)


async def _handle_update_description(chat_id: str, user_id: str, description: str) -> None:
    if len(description) > MAX_DESCRIPTION_LENGTH:
        await bot.send_message(chat_id, TOO_LONG_DESCRIPTION_MESSAGE)
        return

    set_user_description(user_id, description)
    update_user_conversation_state(chat_id, STATE_FINISH)
    
    await bot.send_message(chat_id, UPDATE_SAVED_MESSAGE)


async def _handle_update_age(chat_id: str, user_id: str, age: int) -> None:
    try:
        age = int(age)
    except ValueError:
        await bot.send_message(chat_id, NOT_A_NUMBER)
        return
    
    if age < USER_MINIMUM_AGE:
        delete_user_conversation_state(chat_id)
        await bot.send_message(chat_id, TOO_YOUNG_MESSAGE)
        return
    if age > USER_MAXIMUM_AGE:
        await bot.send_message(chat_id, INNAPROPRIATE_AGE_MESSAGE)
        return
    
    set_user_age(user_id, age)
    update_user_conversation_state(chat_id, STATE_FINISH)

    await bot.send_message(chat_id, UPDATE_SAVED_MESSAGE)


async def _handle_update_city(chat_id: str, user_id: str, city: str) -> None:
    if len(city) > MAX_CITY_LENGTH:
        await bot.send_message(chat_id, TOO_LONG_CITY_MESSAGE)
        return

    set_user_city(user_id, city)
    update_user_conversation_state(chat_id, STATE_FINISH)
    
    await bot.send_message(chat_id, UPDATE_SAVED_MESSAGE)


async def _handle_update_photos(message: Message, chat_id: str, user_id: str) -> None:
    user_photos = get_user_photo_list(user_id)
    
    if len(user_photos) == 0 and message.photo is None:
        await bot.send_message(chat_id, PHOTO_IS_REQUIRED)
        return
    
    if len(user_photos) >= 1 and message.photo is None:
        update_user_conversation_state(chat_id, STATE_FINISH)
        return
    
    if len(user_photos) == PHOTO_LIMIT:
        update_user_conversation_state(chat_id, STATE_FINISH)
        await bot.send_message(chat_id, TOO_MANY_PHOTOS)
        return
    
    photo_id = message.photo[0].file_id
    add_user_photo(user_id, photo_id)
    
    if len(user_photos) == 1:
        await bot.send_message(chat_id, PHOTOS_SAVED_MESSAGE)
