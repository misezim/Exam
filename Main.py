import asyncio
import logging

from BOT_CONFIG import bot, dp, database

from HANDLERS.START import start_router
from HANDLERS.DIALOG import survey_router
from HANDLERS.COMPLAINTS import complaints_router


async def on_startup(bot):
    database.create_tables()


async def main():
    dp.include_router(start_router)
    dp.include_router(survey_router)
    dp.include_router(complaints_router)
    dp.startup.register(on_startup)
    await dp.start_polling(bot)

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())