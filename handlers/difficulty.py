from aiogram import F, Router
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import CallbackQuery, Message

from config import Config
from keyboards import difficulty_games_keyboard
from localization import Language, text
from services.database import SQLiteDatabase
from services.rps import (
    DEFAULT_RPS_DIFFICULTY,
    RPS_DIFFICULTY_CONFIG_KEY,
    normalize_rps_difficulty,
)
from services.tictactoe import (
    DEFAULT_TICTACTOE_DIFFICULTY,
    TICTACTOE_DIFFICULTY_CONFIG_KEY,
    normalize_tictactoe_difficulty,
)

router = Router(name="difficulty")


class DifficultyStates(StatesGroup):
    waiting_for_value = State()


DIFFICULTY_OPTIONS = {
    "tictactoe": (
        TICTACTOE_DIFFICULTY_CONFIG_KEY,
        DEFAULT_TICTACTOE_DIFFICULTY,
        normalize_tictactoe_difficulty,
    ),
    "rps": (
        RPS_DIFFICULTY_CONFIG_KEY,
        DEFAULT_RPS_DIFFICULTY,
        normalize_rps_difficulty,
    ),
}


@router.message(Command("setdifficulty"))
async def show_difficulty_menu(
    message: Message,
    config: Config,
    database: SQLiteDatabase,
    state: FSMContext,
) -> None:
    if message.from_user is None:
        return

    language: Language = await database.get_language(message.from_user.id)
    if message.from_user.id not in config.admin_ids:
        await message.answer(text(language, "no_access"))
        return

    await state.clear()
    values = {}
    for game, (config_key, default, normalize) in DIFFICULTY_OPTIONS.items():
        value = await database.get_config(config_key, default)
        try:
            values[game] = normalize(value or "")
        except ValueError:
            await message.answer(text(language, "difficulty_invalid"))
            return

    await message.answer(
        text(language, "difficulty_choose_game"),
        reply_markup=difficulty_games_keyboard(
            message.from_user.id,
            language,
            values["tictactoe"],
            values["rps"],
        ),
    )


@router.callback_query(F.data.startswith("difficulty:select:"))
async def select_difficulty_game(
    callback: CallbackQuery,
    config: Config,
    database: SQLiteDatabase,
    state: FSMContext,
) -> None:
    if callback.from_user is None or callback.data is None:
        await callback.answer()
        return

    parts = callback.data.split(":")
    if (
        len(parts) != 4
        or not parts[2].isdigit()
        or parts[3] not in DIFFICULTY_OPTIONS
    ):
        await callback.answer()
        return

    language: Language = await database.get_language(callback.from_user.id)
    if (
        int(parts[2]) != callback.from_user.id
        or callback.from_user.id not in config.admin_ids
    ):
        await callback.answer(text(language, "no_access"), show_alert=True)
        return

    game = parts[3]
    config_key, default, normalize = DIFFICULTY_OPTIONS[game]
    value = await database.get_config(config_key, default)
    try:
        current_difficulty = normalize(value or "")
    except ValueError:
        await callback.answer(text(language, "difficulty_invalid"), show_alert=True)
        return

    await state.set_data({"game": game})
    await state.set_state(DifficultyStates.waiting_for_value)
    await callback.answer()
    if isinstance(callback.message, Message):
        await callback.message.answer(
            text(language, "difficulty_enter_value").format(
                game=text(language, f"difficulty_{game}_name"),
                difficulty=current_difficulty,
            )
        )


@router.message(Command("cancel"), StateFilter(DifficultyStates.waiting_for_value))
async def cancel_difficulty_update(
    message: Message,
    database: SQLiteDatabase,
    state: FSMContext,
) -> None:
    await state.clear()
    if message.from_user is not None:
        language = await database.get_language(message.from_user.id)
        await message.answer(text(language, "difficulty_cancelled"))


@router.message(
    StateFilter(DifficultyStates.waiting_for_value),
    F.text,
    ~F.text.startswith("/"),
)
async def save_difficulty_value(
    message: Message,
    config: Config,
    database: SQLiteDatabase,
    state: FSMContext,
) -> None:
    if message.from_user is None or message.text is None:
        return

    language: Language = await database.get_language(message.from_user.id)
    if message.from_user.id not in config.admin_ids:
        await state.clear()
        await message.answer(text(language, "no_access"))
        return

    game = (await state.get_data()).get("game")
    if game not in DIFFICULTY_OPTIONS:
        await state.clear()
        raise RuntimeError("В состоянии настройки сложности отсутствует игра")

    config_key, _, normalize = DIFFICULTY_OPTIONS[game]
    try:
        difficulty = normalize(message.text.strip())
    except ValueError:
        await message.answer(text(language, "difficulty_usage"))
        return

    await database.set_config(config_key, difficulty)
    await state.clear()
    await message.answer(
        text(language, "difficulty_updated").format(
            game=text(language, f"difficulty_{game}_name"),
            difficulty=difficulty,
        )
    )
