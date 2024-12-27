from aiogram import Router, F, types
from aiogram.filters import Command
from aiogram.fsm.state import StatesGroup, State, default_state
from aiogram.fsm.context import FSMContext

from BOT_CONFIG import database

book_router = Router()
book_router.message.filter(F.from_user.id == 1105418521)
book_router.callback_query.filter(F.from_user.id == 1105418521)

class Book(StatesGroup):
    name = State()
    price = State()
    cover = State()
    genre = State()


@book_router.message(Command("stop"))
@book_router.message(F.text == "стоп")
async def stop_dialog(message: types.Message, state: FSMContext):
    print(message.text)
    await state.clear()
    await message.answer("Survey terminated")

@book_router.message(Command("new_book"), default_state)
async def create_new_book(message: types.Message, state: FSMContext):
    await message.answer("To terminate the survey type 'стоп'")
    await message.answer("Enter the name of the book")
    await state.set_state(Book.name)

@book_router.message(Book.name)
async def process_name(message: types.Message, state: FSMContext):
    name = message.text
    print(name)
    await state.update_data(name=message.text)
    await message.answer("Enter the price of the book")
    await state.set_state(Book.price)

@book_router.message(Book.price)
async def process_price(message: types.Message, state: FSMContext):
    price = message.text
    if not price.isdigit():
        await message.answer("Please, enter only numbers")
        return
    price = int(price)
    await state.update_data(price=price)
    await message.answer("Upload the cover of the book")
    await state.set_state(Book.cover)

@book_router.message(Book.cover, F.photo)
async def process_cover(message: types.Message, state: FSMContext):
    covers = message.photo
    print(covers)
    biggest_image = covers[-1]
    biggest_image_id = biggest_image.file_id
    await state.update_data(cover=biggest_image_id)
    kb = types.ReplyKeyboardMarkup(
        keyboard=
        [
            [
                types.KeyboardButton(text="Adventure"),
                types.KeyboardButton(text="Animation"),
                types.KeyboardButton(text="Detective")
            ],
            [
                types.KeyboardButton(text="Science Fiction"),
                types.KeyboardButton(text="Drama"),
                types.KeyboardButton(text="Horror"),
            ]
        ],
        resize_keyboard=True,
        input_field_placeholder="Choose genre: "
    )
    await message.answer("What is the genre of the book?", reply_markup=kb)
    await state.set_state(Book.genre)


@book_router.message(Book.genre)
async def process_genre(message: types.Message, state: FSMContext):
    kb = types.ReplyKeyboardRemove()
    await state.update_data(genre=message.text)
    await message.answer("Book is saved!", reply_markup=kb)
    data = await state.get_data()
    print(data)
    database.save_book(data)
    await state.clear()