from aiogram import Router, F, types
from aiogram.filters import Command
from aiogram.fsm.state import StatesGroup, State, default_state
from aiogram.fsm.context import FSMContext

from BOT_CONFIG import database

survey_router = Router()

class Survey(StatesGroup):
    name = State()
    age = State()
    genre = State()


@survey_router.message(Command("stop"))
@survey_router.message(F.text == "стоп")
async def stop_dialog(message: types.Message, state: FSMContext):
    print(message.text)
    await state.clear()
    await message.answer("Survey terminated")

@survey_router.message(Command("survey"), default_state)
async def start_survey(message: types.Message, state: FSMContext):
    await message.answer("To terminate the survey type 'стоп'")
    await message.answer("What is your name?")
    await state.set_state(Survey.name)

@survey_router.message(Survey.name)
async def process_name(message: types.Message, state: FSMContext):
    name = message.text
    print(name)
    await state.update_data(name=message.text)
    await message.answer("How old are you?")
    await state.set_state(Survey.age)

@survey_router.message(Survey.age)
async def process_age(message: types.Message, state: FSMContext):
    age = message.text
    if not age.isdigit():
        await message.answer("Please, enter only numbers")
        return
    age = int(age)
    if age < 10 or age > 90:
        await message.answer("Please, enter your age between 10 and 90")
        return
    kb = types.ReplyKeyboardMarkup(
        keyboard=
        [
            [
                    types.KeyboardButton(text= "Adventure"),
                    types.KeyboardButton(text= "Animation"),
                    types.KeyboardButton(text="Detective")
            ],
            [
                types.KeyboardButton(text="Science Fiction"),
                types.KeyboardButton(text= "Drama"),
                types.KeyboardButton(text= "Horror"),
            ]
        ],
        resize_keyboard=True,
        input_field_placeholder="Choose genre: "
    )
    await state.update_data(age=age)
    await message.answer("What is your favorite genre?", reply_markup=kb)
    await state.set_state(Survey.genre)

@survey_router.message(Survey.genre)
async def process_genre(message: types.Message, state: FSMContext):
    kb = types.ReplyKeyboardRemove()
    await state.update_data(genre=message.text)
    await message.answer("Thank You!", reply_markup=kb)
    data = await state.get_data()
    print(data)
    database.save_survey(data)
    await state.clear()



# survey_router = Router()
# users=[]
#
# class Survey(StatesGroup):
#     name = State()
#     age = State()
#     genre = State()
#
#
# @survey_router.callback_query(F.data == "survey")
# async def start_survey(callback: types.CallbackQuery, state: FSMContext):
#     if callback.from_user.id in users:
#         await callback.answer("You are already registered")
#         return
#     users.append(callback.from_user.id)
#     await callback.answer()
#     await callback.message.answer("What is your name?")
#     await state.set_state(Survey.name)