from telebot.types import Message, InputMediaPhoto

from db.functions import (
    create_user_if_not_exists,
    get_user_conversation_state,
    delete_all_user_photos,
    update_user_conversation_state,
    get_user,
    get_user_photo_list
)
from db.constants import (
    STATE_HANDLING_PHOTOS,
    STATE_FINISH,
    STATE_START,
)
from bot_insatnce import bot
from keyboards import (
    INITIAL_MESSAGE_KEYBOARD
)

from .messages import (
    STATE_MESSAGES,
    ALREADY_REGISTERED_MESSAGE,
)

async def start(message: Message) -> None:
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
    photos[0].caption = f'{header}\n{user.description}'
    await bot.send_media_group(message.chat.id, photos)
