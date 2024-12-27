from aiogram import Router, F, types
from aiogram.filters import Command
from aiogram.fsm.state import StatesGroup, State, default_state
from aiogram.fsm.context import FSMContext

from BOT_CONFIG import database

survey_router = Router()

class Survey(StatesGroup):
    name = State()
    phone_number  = State()
    complaint = State()


@survey_router.message(Command("stop"))
@survey_router.message(F.text == "стоп")
async def stop_dialog(message: types.Message, state: FSMContext):
    print(message.text)
    await state.clear()
    await message.answer("Опрос остановлен")

@survey_router.message(Command("survey"), default_state)
async def start_survey(message: types.Message, state: FSMContext):
    await message.answer("Для остановки введите слово 'стоп'")
    await message.answer("Как вас зовут?")
    await state.set_state(Survey.name)

@survey_router.message(Survey.name)
async def process_name(message: types.Message, state: FSMContext):
    name = message.text
    if len(name) < 3:
        await message.answer("Имя должно содержать хотя бы 3 символа.")
        return
    elif len(name) > 50:
        await message.answer("Имя не должно превышать 50 символов.")
        return
    await state.update_data(name=message.text)

    await message.answer("Ваш номер телефона: ")
    await state.set_state(Survey.phone_number)

@survey_router.message(Survey.phone_number)
async def process_phone_number(message: types.Message, state: FSMContext):
    phone_number = message.text
    if not phone_number.isdigit():
        await message.answer("Пожалуйста, введите только цифры для номера телефона.")
        return
    await state.update_data(phone_number=phone_number)
    await message.answer("Есть ли у вас дополнительные комментарии или жалобы?")
    await state.set_state(Survey.complaint)


@survey_router.message(Survey.complaint)
async def process_complaint(message: types.Message, state: FSMContext):
    complaint = message.text
    await state.update_data(complaint=complaint)
    await message.answer("Спасибо за ваш отзыв!")
    data = await state.get_data()
    print(data)
    database.save_survey(data)
    await state.clear()
