from telebot import TeleBot

from handlers.user_setup import (
    proccess_new_user,
    view_profile,
    receive_photo,
    initial_user_setup
)
from handlers.user_settings import (
    change_photos
)


def _register_command_handlers(bot: TeleBot) -> None:
    bot.register_message_handler(proccess_new_user, commands=['start'])
    bot.register_message_handler(view_profile, commands=['view_profile'])
    bot.register_message_handler(change_photos, commands=['change_photos'])


def _register_message_handlers(bot: TeleBot) -> None:
    bot.register_message_handler(receive_photo, content_types=['photo'])
    bot.register_message_handler(initial_user_setup)


def register_handlers(bot: TeleBot) -> None:
    _register_command_handlers(bot)
    _register_message_handlers(bot)
