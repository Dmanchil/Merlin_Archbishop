from aiogram import F, Router
from aiogram.filters import Command
from aiogram.types import CallbackQuery, InlineKeyboardMarkup, Message

from keyboards import rps_keyboard
from localization import Language, text
from services.database import SQLiteDatabase
from services.rps import (
    DEFAULT_RPS_DIFFICULTY,
    RPS_DIFFICULTY_CONFIG_KEY,
    choose_computer_gesture,
    get_result,
    is_gesture,
    normalize_rps_difficulty,
)

router = Router(name="rps")


@router.message(Command("rps"))
async def rps_command(message: Message, database: SQLiteDatabase) -> None:
    if message.from_user is None:
        return

    language = await database.get_language(message.from_user.id)
    await message.answer(
        text(language, "rps_start"),
        reply_markup=rps_keyboard(message.from_user.id, language),
    )


@router.callback_query(F.data.startswith("rps:"))
async def rps_callback(
    callback: CallbackQuery,
    database: SQLiteDatabase,
) -> None:
    if callback.from_user is None or callback.data is None:
        await callback.answer()
        return

    parts = callback.data.split(":")
    if len(parts) < 3 or not parts[2].isdigit():
        await callback.answer()
        return

    language: Language = await database.get_language(callback.from_user.id)
    if int(parts[2]) != callback.from_user.id:
        await callback.answer(
            text(language, "rps_not_your_game"),
            show_alert=True,
        )
        return

    if parts[1] == "new" and len(parts) == 3:
        await callback.answer()
        await _edit_game(
            callback,
            text(language, "rps_start"),
            rps_keyboard(callback.from_user.id, language),
        )
        return

    if (
        parts[1] != "choose"
        or len(parts) != 5
        or not parts[3].isdigit()
        or not is_gesture(parts[4])
    ):
        await callback.answer()
        return

    round_number = int(parts[3]) + 1
    player = parts[4]
    difficulty = await database.get_config(
        RPS_DIFFICULTY_CONFIG_KEY,
        DEFAULT_RPS_DIFFICULTY,
    )
    try:
        normalized_difficulty = normalize_rps_difficulty(difficulty or "")
    except ValueError:
        await callback.answer(
            text(language, "rps_difficulty_invalid"),
            show_alert=True,
        )
        return

    computer = choose_computer_gesture(player, normalized_difficulty)
    result = get_result(player, computer)
    response = text(language, "rps_result").format(
        round=round_number,
        player=text(language, f"rps_{player}").lower(),
        computer=text(language, f"rps_{computer}").lower(),
        result=text(language, f"rps_{result}"),
    )
    await database.append_game_history(
        callback.from_user.id,
        {
            "game": "rps",
            "round": round_number,
            "player_choice": player,
            "computer_choice": computer,
            "result": result,
        },
    )
    await callback.answer()
    await _edit_game(
        callback,
        response,
        rps_keyboard(
            callback.from_user.id,
            language,
            round_number,
        ),
    )


async def _edit_game(
    callback: CallbackQuery,
    message_text: str,
    keyboard: InlineKeyboardMarkup,
) -> None:
    if isinstance(callback.message, Message):
        await callback.message.edit_text(message_text, reply_markup=keyboard)
