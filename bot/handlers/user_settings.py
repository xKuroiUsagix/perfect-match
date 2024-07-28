from telebot.types import Message

from db.functions import (
    delete_all_user_photos,
)
from bot_insatnce import bot
from handlers.messages import CHANGE_PHOTOS_MESSAGE


# async def change_photos(message: Message):
#     user_id = str(message.from_user.id)
#     chat_id = str(message.chat.id)

#     delete_all_user_photos(user_id)
#     create_bot_message(chat_id, ASK_PHOTOS)
#     await bot.send_message(chat_id, CHANGE_PHOTOS_MESSAGE)
