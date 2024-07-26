import asyncio

from telebot import TeleBot

from bot_insatnce import bot


async def main(bot: TeleBot) -> None:
    # Just to load all handlers
    import handlers
    
    await bot.infinity_polling()


if __name__ == '__main__':
    asyncio.run(main(bot))
