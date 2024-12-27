from aiogram import Router, F, types
from aiogram.filters import Command
from aiogram.fsm.state import StatesGroup, State, default_state
from aiogram.fsm.context import FSMContext



from BOT_CONFIG import database


complaints_router = Router()
@complaints_router.message(Command("books"))
async def show_all_complaints(message: types.Message):
    complaints_list = database.get_all_complaints()
    for complaint in complaints_list:
        await message.answer(f"Name: {complaint['name']}\n"
                                             f"Phone_number: {complaint['phone_number']}\n"
                                             f"Complaint: {complaint['complaint']}\n")