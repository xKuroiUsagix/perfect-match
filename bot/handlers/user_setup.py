from telebot.types import (
    Message, 
    InputMediaPhoto, 
    ReplyKeyboardRemove,
)

from db.functions import (
    create_user_if_not_exists,
    set_user_age,
    set_user_name,
    set_user_gender,
    set_user_looking_for,
    set_user_city,
    set_user_description,
    add_user_photo,
    get_user_photo_list,
    get_user,
    update_user_conversation_state,
    delete_user_conversation_state,
    get_user_conversation_state,
    delete_all_user_photos
)
from db.constants import (
    PHOTO_LIMIT, 
    USER_MINIMUM_AGE, 
    USER_MAXIMUM_AGE,
    STATE_START, 
    STATE_FINISH, 
    STATE_INTENET_WARNING, 
    STATE_ASK_NAME,
    STATE_ASK_AGE, 
    STATE_ASK_GENDER, 
    STATE_ASK_LOOKING_FOR, 
    STATE_ASK_CITY,
    STATE_ASK_DESCRIPTION, 
    STATE_ASK_PHOTOS, 
    STATE_HANDLING_PHOTOS
)
from bot_insatnce import bot
from keyboards import (
    GENDER_CHOICE_KEYBOARD,
    INITIAL_MESSAGE_KEYBOARD,
    INTERNET_WARNING_KEYBOARD
)
from .messages import (
    NOT_A_NUMBER, 
    STATE_MESSAGES, 
    INNAPROPRIATE_AGE, 
    TOO_MANY_PHOTOS, 
    PHOTOS_SAVED_MESSAGE,
    ALREADY_REGISTERED_MESSAGE
)
from .helpers import get_gender


async def handle_user_conversation(message: Message) -> None:
    chat_id = message.chat.id
    user_id = message.from_user.id
    conversation_state = get_user_conversation_state(chat_id)
    
    if conversation_state == STATE_START:
        await _handle_initial_message(chat_id)
    elif conversation_state == STATE_INTENET_WARNING:
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


async def handle_start(message: Message) -> None:
    chat_id = message.chat.id
    user_id = message.from_user.id

    create_user_if_not_exists(user_id, chat_id)
    conversation_state = get_user_conversation_state(chat_id)
    
    if conversation_state in (STATE_HANDLING_PHOTOS, STATE_FINISH):
        await bot.send_message(chat_id, ALREADY_REGISTERED_MESSAGE)
        return
    
    delete_all_user_photos(user_id)
    update_user_conversation_state(user_id, STATE_START)

    response = STATE_MESSAGES.get(STATE_START)
    await bot.send_message(chat_id, response, reply_markup=INITIAL_MESSAGE_KEYBOARD)


async def view_profile(message: Message):
    user = get_user(message.from_user.id)
    photo_records = get_user_photo_list(user.telegram_id)
    photos = [InputMediaPhoto(record.photo_id) for record in photo_records]
    header = f'<b>{user.name}, {user.age} | {user.city.capitalize()}</b>\n'
    photos[0].caption = header + user.description
    await bot.send_media_group(message.chat.id, photos)


async def _handle_initial_message(chat_id: str) -> None:
    update_user_conversation_state(chat_id, STATE_INTENET_WARNING)

    response = STATE_MESSAGES.get(STATE_INTENET_WARNING)
    await bot.send_message(chat_id, response, reply_markup=INTERNET_WARNING_KEYBOARD)


async def _handle_internet_warning(chat_id: str) -> None:
    update_user_conversation_state(chat_id, STATE_ASK_NAME)
    
    response = STATE_MESSAGES.get(STATE_ASK_NAME)
    await bot.send_message(chat_id, response, reply_markup=ReplyKeyboardRemove())


async def _handle_name(chat_id: str, user_id: str, name: str) -> None:
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
    
    if age < USER_MINIMUM_AGE or age > USER_MAXIMUM_AGE:
        delete_user_conversation_state(chat_id)
        await bot.send_message(chat_id, INNAPROPRIATE_AGE)
        return

    set_user_age(user_id, age)
    update_user_conversation_state(chat_id, STATE_ASK_GENDER)
    
    response = STATE_MESSAGES.get(STATE_ASK_GENDER)
    await bot.send_message(chat_id, response, reply_markup=GENDER_CHOICE_KEYBOARD)


async def _handle_gender(chat_id: str, user_id: str, gender: int) -> None:
    set_user_gender(user_id, gender)
    update_user_conversation_state(chat_id, STATE_ASK_LOOKING_FOR)

    response = STATE_MESSAGES.get(STATE_ASK_LOOKING_FOR)
    await bot.send_message(chat_id, response, reply_markup=GENDER_CHOICE_KEYBOARD)


async def _handle_looking_for(chat_id: str, user_id: str, gender: int) -> None:
    set_user_looking_for(user_id, gender)
    update_user_conversation_state(chat_id, STATE_ASK_CITY)
    
    response = STATE_MESSAGES.get(STATE_ASK_CITY)
    await bot.send_message(chat_id, response, reply_markup=ReplyKeyboardRemove())


async def _handle_city(chat_id: str, user_id: str, city: str) -> None:
    set_user_city(user_id, city)
    update_user_conversation_state(chat_id, STATE_ASK_DESCRIPTION)
    
    response = STATE_MESSAGES.get(STATE_ASK_DESCRIPTION)
    await bot.send_message(chat_id, response)


async def _handle_description(chat_id: str, user_id: str, description: str) -> None:
    set_user_description(user_id, description)
    update_user_conversation_state(chat_id, STATE_ASK_PHOTOS)
    
    response = STATE_MESSAGES.get(STATE_ASK_PHOTOS)
    await bot.send_message(chat_id, response)

    
async def _handle_photos(message: Message, chat_id: str, user_id: str) -> None:
    update_user_conversation_state(chat_id, STATE_HANDLING_PHOTOS)
    user_photos = get_user_photo_list(user_id)
    
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

