from telebot.types import Message, InputMediaPhoto

from bot_insatnce import bot

import json


@bot.message_handler(commands=['start', 'help'])
async def send_welcome(message: Message) -> None:
	await bot.reply_to(message, "Hello World!")


@bot.message_handler(commands=['get_photo'])
async def send_photo(message: Message):
    with open('temp.json', 'r') as file:
        photo_ids = json.load(file)

    media_input = [InputMediaPhoto(file_id) for file_id in photo_ids]
    await bot.send_media_group(message.chat.id, media_input)


@bot.message_handler(func=lambda message: True, content_types=['photo'])
async def receive_photo(message: Message) -> None:
    with open('temp.json', 'r') as file:
        data = json.load(file)

    data.append(message.photo[-1].file_id)

    with open('temp.json', 'w') as file:
        json.dump(data, file)

    if len(data) < 2:
        await bot.reply_to(message, f'Your photos are saved.')


@bot.message_handler(func=lambda m: True)
async def echo_all(message: Message) -> None:
	await bot.reply_to(message, message.text)

