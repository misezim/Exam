import random
from aiogram import Router, types
from aiogram.filters import Command
other_router = Router()

random_names = ("Alice", "Bob", "Charlie", "Diana", "Frank",
                "Grace", "Hannah", "Igor", "Jack")

@other_router.message(Command("myinfo"))
async def myinfo_handler(message: types.Message):
    name = message.from_user.first_name
    id = message.from_user.id
    last_name = message.from_user.last_name if message.from_user.last_name else "No last name"
    await message.answer(f" Your name = {name},\nYour id = {id},\nYour last name = {last_name}")

@other_router.message(Command("random"))
async def random_handler(message: types.Message):
    random_name = random.choice(random_names)
    await message.answer(f"Random name: {random_name}")

# @dp.message()
# async def echo_handler(message: types.Message):
#     txt = message.text
#     # await message.answer(txt)
#     # await bot.send_message(message.chat.id, txt)
#     await bot.send_message(chat_id=message.from_user.id, text= txt)