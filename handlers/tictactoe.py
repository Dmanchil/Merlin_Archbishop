import logging

from aiogram import Bot, Router
from aiogram.exceptions import TelegramAPIError
from aiogram.filters import Command, CommandObject
from aiogram.types import Message

from config import Config
from localization import Language, text
from services.database import SQLiteDatabase
from services.html_bubbles import (
    DEFAULT_TICTACTOE_DIFFICULTY,
    TICTACTOE_DIFFICULTY_CONFIG_KEY,
    SendWidget,
    load_tictactoe_html,
    normalize_tictactoe_difficulty,
)

logger = logging.getLogger(__name__)
router = Router(name="tictactoe")


@router.message(Command("tictactoe"))
async def tictactoe_command(
    message: Message,
    bot: Bot,
    database: SQLiteDatabase,
) -> None:
    language: Language = (
        await database.get_language(message.from_user.id)
        if message.from_user is not None
        else "ru"
    )

    try:
        difficulty = await database.get_config(
            TICTACTOE_DIFFICULTY_CONFIG_KEY,
            DEFAULT_TICTACTOE_DIFFICULTY,
        )
        try:
            normalized_difficulty = normalize_tictactoe_difficulty(difficulty or "")
        except ValueError:
            await message.answer(text(language, "difficulty_invalid"))
            return

        html = load_tictactoe_html(normalized_difficulty)
        await bot(SendWidget(chat_id=message.chat.id, html=html))
    except TelegramAPIError:
        logger.exception("Could not send the tic-tac-toe HTMLBubble")
        await message.answer(text(language, "widget_unavailable"))


@router.message(Command("setdifficulty"))
async def set_tictactoe_difficulty(
    message: Message,
    command: CommandObject,
    config: Config,
    database: SQLiteDatabase,
) -> None:
    language: Language = (
        await database.get_language(message.from_user.id)
        if message.from_user is not None
        else "ru"
    )
    if message.from_user is None or message.from_user.id not in config.admin_ids:
        await message.answer(text(language, "no_access"))
        return

    try:
        difficulty = normalize_tictactoe_difficulty((command.args or "").strip())
    except ValueError:
        await message.answer(text(language, "difficulty_usage"))
        return

    await database.set_config(TICTACTOE_DIFFICULTY_CONFIG_KEY, difficulty)
    await message.answer(
        text(language, "difficulty_updated").format(difficulty=difficulty)
    )
