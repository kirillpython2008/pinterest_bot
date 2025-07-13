from aiogram import Bot, Dispatcher

from dotenv import load_dotenv
from os import getenv
from asyncio import run
import logging
import sys

from routers.user_routers import user_router
from routers.admin_routers import admin_router


async def start_bot():
    load_dotenv(dotenv_path=".env")

    bot = Bot(token=getenv("TOKEN"))
    dp = Dispatcher()

    dp.include_router(admin_router)
    dp.include_router(user_router)

    logging.basicConfig(level=logging.INFO)

    logging.info("бот запущен")

    try:
        await dp.start_polling(bot)
    except KeyboardInterrupt:
        await bot.session.close()
    finally:
        logging.info("бот выключен")
        sys.exit(0)

run(start_bot())
