from telebot.types import ReplyKeyboardMarkup, KeyboardButton

from db.constants import MAN, WOMAN, OTHER
from messages import (
    GENDER_MESSAGE_RESPONSES, 
    INITIAL_MESSAGE_RESPONSE,
    INTERNET_WARNING_RESPONSE
)


INITIAL_MESSAGE_KEYBOARD = ReplyKeyboardMarkup(resize_keyboard=True)
INITIAL_MESSAGE_KEYBOARD.add(
    KeyboardButton(INITIAL_MESSAGE_RESPONSE)
)

INTERNET_WARNING_KEYBOARD = ReplyKeyboardMarkup(resize_keyboard=True)
INTERNET_WARNING_KEYBOARD.add(
    KeyboardButton(INTERNET_WARNING_RESPONSE)
)

GENDER_CHOICE_KEYBOARD = ReplyKeyboardMarkup(resize_keyboard=True)
GENDER_CHOICE_KEYBOARD.add(
    KeyboardButton(GENDER_MESSAGE_RESPONSES[MAN]),
    KeyboardButton(GENDER_MESSAGE_RESPONSES[WOMAN]),
    KeyboardButton(GENDER_MESSAGE_RESPONSES[OTHER])
)
