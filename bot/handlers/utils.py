from telebot import TeleBot

from .messages import (
    COMMAND_START,
    COMMAND_HELP,
    COMMAND_CHANGE_AGE,
    COMMAND_CHANGE_CITY,
    COMMAND_CHANGE_DESCRIPTION,
    COMMAND_CHANGE_NAME,
    COMMAND_CHANGE_PHOTOS,
    COMMAND_VIEW_PROFILE
)
from .user_setup import (
    handle_user_conversation,
)
from .commands import (
    start,
    view_profile,
    change_age,
    change_name,
    change_description,
    change_city,
    change_photos,
)


def _register_command_handlers(bot: TeleBot) -> None:
    bot.register_message_handler(start, commands=[COMMAND_START])
    bot.register_message_handler(view_profile, commands=[COMMAND_VIEW_PROFILE])
    bot.register_message_handler(change_age, commands=[COMMAND_CHANGE_AGE])
    bot.register_message_handler(change_name, commands=[COMMAND_CHANGE_NAME])
    bot.register_message_handler(change_description, commands=[COMMAND_CHANGE_DESCRIPTION])
    bot.register_message_handler(change_city, commands=[COMMAND_CHANGE_CITY])
    bot.register_message_handler(change_photos, commands=[COMMAND_CHANGE_PHOTOS])


def _register_message_handlers(bot: TeleBot) -> None:
    bot.register_message_handler(handle_user_conversation, content_types=['text', 'photo'])


def register_handlers(bot: TeleBot) -> None:
    # Call order is important 
    # If put commands below messages, bot will treat commands as messages therefore commands wont work
    _register_command_handlers(bot)
    _register_message_handlers(bot)
