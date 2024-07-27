from telebot.types import Message

from db.functions import user_delete_all_photos
from bot_insatnce import bot
from messages import ASK_PHOTOS, CHANGE_PHOTOS_MESSAGE

from .user_setup import last_bot_message


async def change_photos(message: Message):
    user_id = str(message.from_user.id)
    chat_id = str(message.chat.id)

    user_delete_all_photos(user_id)
    
    last_bot_message[chat_id] = ASK_PHOTOS
    await bot.send_message(chat_id, CHANGE_PHOTOS_MESSAGE)
