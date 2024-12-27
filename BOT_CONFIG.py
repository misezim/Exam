import random
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from dotenv import dotenv_values
from DATABASE import Database

token = dotenv_values(".env").get("bot_token")
bot = Bot(token=token)
dp = Dispatcher()
database = Database('db.sqlite3')