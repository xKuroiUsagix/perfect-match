import asyncio

from telebot import TeleBot

from bot_insatnce import bot
from handlers.utils import register_handlers


async def main(bot: TeleBot) -> None:
    register_handlers(bot)
    await bot.infinity_polling()


if __name__ == '__main__':
    asyncio.run(main(bot))
