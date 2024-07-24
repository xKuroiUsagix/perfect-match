import sys
import asyncio
import logging

from telebot import TeleBot
from bot_insatnce import bot

from handlers.user_handlers import *


async def main(bot: TeleBot) -> None:
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    await bot.infinity_polling()


if __name__ == '__main__':
    asyncio.run(main(bot))
