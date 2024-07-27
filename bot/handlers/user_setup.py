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
)
from db.constants import OTHER, MAN, WOMAN, PHOTO_LIMIT
from bot_insatnce import bot
from messages import (
    UK_INITIAL_MESSAGE, 
    UK_INTERNET_WARNING,
    UKNOWN_RESPONSE,
    INITIAL_MESSAGE_RESPONSE,
    INTERNET_WARNING_RESPONSE,
    ASK_NAME_MESSAGE,
    ASK_AGE_MESSAGE,
    ASK_GENDER_MESSAGE,
    ASK_LOOKING_FOR_MESSAGE,
    ASK_DESCRIPTION,
    ASK_CITY_MESSAGE,
    ASK_PHOTOS,
    NOT_A_NUMBER,
    PHOTO_IS_REQUIRED,
    GENDER_MESSAGE_RESPONSES,
    WRONG_GENDER_MESSAGE,
    SETUP_DONE_MESSAGE,
    TOO_MANY_PHOTOS,
    PHOTOS_SAVED_MESSAGE,
    CHANGE_PHOTOS_MESSAGE
)
from keyboards import (
    GENDER_CHOICE_KEYBOARD,
    INITIAL_MESSAGE_KEYBOARD,
    INTERNET_WARNING_KEYBOARD
)


last_bot_message = {}


async def proccess_new_user(message: Message) -> None:
    telegram_id = str(message.from_user.id)
    chat_id = str(message.chat.id)    
    create_user_if_not_exists(telegram_id, chat_id)

    await bot.send_message(message.chat.id, UK_INITIAL_MESSAGE, reply_markup=INITIAL_MESSAGE_KEYBOARD)


async def view_profile(message: Message):
    user = get_user(message.from_user.id)
    photo_records = get_user_photo_list(user.telegram_id)
    photos = [InputMediaPhoto(record.photo_id) for record in photo_records]
    header = f'<b>{user.name}, {user.age} | {user.city.capitalize()}</b>\n'
    photos[0].caption = header + user.description
    await bot.send_media_group(message.chat.id, photos)


async def receive_photo(message: Message) -> None:
    user_id = str(message.from_user.id)
    chat_id = str(message.chat.id)
    
    if last_bot_message[chat_id] == ASK_PHOTOS:
        user_photos = get_user_photo_list(user_id)
    
        if len(user_photos) == PHOTO_LIMIT:
            await bot.send_message(chat_id, TOO_MANY_PHOTOS)
            await bot.send_message(chat_id, SETUP_DONE_MESSAGE)
            return

        photo_id = message.photo[0].file_id
        add_user_photo(user_id, photo_id)

        if len(user_photos) == 1:
            await bot.send_message(chat_id, PHOTOS_SAVED_MESSAGE)
            await bot.send_message(chat_id, SETUP_DONE_MESSAGE)


async def initial_user_setup(message: Message) -> None:
    chat_id = str(message.chat.id)
    user_id = str(message.from_user.id)
    
    if message.text == INITIAL_MESSAGE_RESPONSE:
        await bot.send_message(chat_id, UK_INTERNET_WARNING, reply_markup=INTERNET_WARNING_KEYBOARD)

    elif message.text == INTERNET_WARNING_RESPONSE:
        last_bot_message[chat_id] = ASK_NAME_MESSAGE
        await bot.send_message(chat_id, ASK_NAME_MESSAGE, reply_markup=ReplyKeyboardRemove())

    elif last_bot_message[chat_id] == ASK_NAME_MESSAGE:
        set_user_name(user_id, message.text)
        last_bot_message[chat_id] = ASK_AGE_MESSAGE
        await bot.send_message(chat_id, ASK_AGE_MESSAGE)
    
    elif last_bot_message[chat_id] == ASK_AGE_MESSAGE:
        try:
            age = int(message.text)
        except ValueError:
            await bot.send_message(chat_id, NOT_A_NUMBER)
            return
        
        set_user_age(user_id, age)
        last_bot_message[chat_id] = ASK_GENDER_MESSAGE
        await bot.send_message(chat_id, ASK_GENDER_MESSAGE, reply_markup=GENDER_CHOICE_KEYBOARD)
    
    elif last_bot_message[chat_id] == ASK_GENDER_MESSAGE:
        if message.text not in GENDER_MESSAGE_RESPONSES.values():
            await bot.send_message(chat_id, WRONG_GENDER_MESSAGE, reply_markup=GENDER_CHOICE_KEYBOARD)
            return
        
        if message.text == GENDER_MESSAGE_RESPONSES[MAN]:
            gender = MAN
        elif message.text == GENDER_MESSAGE_RESPONSES[WOMAN]:
            gender = WOMAN
        else:
            gender = OTHER
        
        set_user_gender(user_id, gender)
        last_bot_message[chat_id] = ASK_LOOKING_FOR_MESSAGE
        await bot.send_message(chat_id, ASK_LOOKING_FOR_MESSAGE, reply_markup=GENDER_CHOICE_KEYBOARD)
    
    elif last_bot_message[chat_id] == ASK_LOOKING_FOR_MESSAGE:
        if message.text not in GENDER_MESSAGE_RESPONSES.values():
            await bot.send_message(chat_id, WRONG_GENDER_MESSAGE, reply_markup=GENDER_CHOICE_KEYBOARD)
            return
        
        if message.text == GENDER_MESSAGE_RESPONSES[MAN]:
            gender = MAN
        elif message.text == GENDER_MESSAGE_RESPONSES[WOMAN]:
            gender = WOMAN
        else:
            gender = OTHER
        
        set_user_looking_for(user_id, gender)
        last_bot_message[chat_id] = ASK_CITY_MESSAGE
        await bot.send_message(chat_id, ASK_CITY_MESSAGE, reply_markup=ReplyKeyboardRemove())
    
    elif last_bot_message[chat_id] == ASK_CITY_MESSAGE:
        city = message.text.lower()
        set_user_city(user_id, city)
        last_bot_message[chat_id] = ASK_DESCRIPTION
        await bot.send_message(chat_id, ASK_DESCRIPTION)
    
    elif last_bot_message[chat_id] == ASK_DESCRIPTION:
        set_user_description(user_id, message.text)
        last_bot_message[chat_id] = ASK_PHOTOS
        await bot.send_message(chat_id, ASK_PHOTOS)
    
    elif last_bot_message[chat_id] == ASK_PHOTOS:
        if message.photo is None:
            await bot.send_message(chat_id, PHOTO_IS_REQUIRED)
