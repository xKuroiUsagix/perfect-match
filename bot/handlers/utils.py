from telebot import TeleBot

from .user_setup import (
    handle_user_conversation,
)
from .commands import (
    start,
    view_profile
)


def _register_command_handlers(bot: TeleBot) -> None:
    bot.register_message_handler(start, commands=['start'])
    bot.register_message_handler(view_profile, commands=['view_profile'])


def _register_message_handlers(bot: TeleBot) -> None:
    bot.register_message_handler(handle_user_conversation, content_types=['text', 'photo'])


def register_handlers(bot: TeleBot) -> None:
    # Call order is important 
    # If put commands below messages, bot will treat commands as messages therefore commands wont work
    _register_command_handlers(bot)
    _register_message_handlers(bot)
