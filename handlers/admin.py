from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from config import Config
from localization import text
from services.database import SQLiteDatabase

router = Router(name="admin")


@router.message(Command("admin"))
async def admin_command(
    message: Message,
    config: Config,
    database: SQLiteDatabase,
) -> None:
    language = (
        await database.get_language(message.from_user.id)
        if message.from_user is not None
        else "ru"
    )
    if message.from_user is None or message.from_user.id not in config.admin_ids:
        await message.answer(text(language, "no_access"))
        return

    await message.answer(text(language, "admin_panel"))
