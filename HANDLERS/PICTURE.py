from aiogram import Router, types
from aiogram.filters import Command

picture_router = Router()

@picture_router.message(Command("picture"))
async def picture_handler(message: types.Message):
    photo = types.FSInputFile("IMAGES/jungkook.jpg")
    await message.answer_photo(photo=photo, caption="Your Future Husband")

@picture_router.message(Command("aisezim"))
async def picture_handler(message: types.Message):
    photo = types.FSInputFile("IMAGES/aisezim.jpg")
    await message.answer_photo(photo=photo, caption="Целую")