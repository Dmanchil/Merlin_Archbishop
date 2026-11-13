import asyncio
import logging

from aiogram import Bot, Dispatcher

from config import Config
from handlers import admin_router, main_router, tictactoe_router
from services.database import SQLiteDatabase


async def main() -> None:
    config = Config.from_env()
    database = SQLiteDatabase()
    await database.initialize()

    bot = Bot(token=config.bot_token)
    dispatcher = Dispatcher()
    dispatcher["config"] = config
    dispatcher["database"] = database
    dispatcher.include_routers(main_router, admin_router, tictactoe_router)

    try:
        await dispatcher.start_polling(bot)
    finally:
        await bot.session.close()
        await database.close()


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
