from telebot.async_telebot import AsyncTeleBot
from token_api import TOKEN


bot = AsyncTeleBot(token=TOKEN, parse_mode='HTML')


