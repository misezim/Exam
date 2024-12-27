from aiogram import Router, F, types
from aiogram.filters import Command

from BOT_CONFIG import database
from pprint import pprint

shop_router = Router()

"""с кортежами"""
# @shop_router.message(Command("books"))
# async def show_all_books(message: types.Message):
#     book_list = database.get_all_books()
#     pprint(book_list)
#     for book in book_list:
#         await message.answer(f"Name: {book[1]}\n"
#                              f"Price: {book[2]}\n"
#                              f"Genre: {book[3]}\n")

"""со словарем"""
@shop_router.message(Command("books"))
async def show_all_books(message: types.Message):
    book_list = database.get_all_books()
    pprint(book_list)
    for book in book_list:
        cover = book["cover"]
        print("Book cover:", cover)
        await message.answer_photo(photo = cover,
                                   caption = f"Name: {book['name']}\n"
                                             f"Price: {book['price']}\n"
                                             f"Genre: {book['genre']}\n")
