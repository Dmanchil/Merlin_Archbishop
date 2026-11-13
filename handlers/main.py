from aiogram import F, Router
from aiogram.filters import Command, CommandStart
from aiogram.types import CallbackQuery, Message

from keyboards import (
    church_selection_keyboard,
    delete_account_keyboard,
    language_keyboard,
    lotm_menu_keyboard,
    main_menu_keyboard,
)
from localization import CHURCHES, Language, SUPPORTED_LANGUAGES, text
from services.database import SQLiteDatabase

router = Router(name="main")
LANGUAGE_CALLBACKS: dict[str, Language] = {
    "settings:language:ru": "ru",
    "settings:language:en": "en",
}
CHURCH_CALLBACKS = {
    f"church:{index}": church for index, church in enumerate(CHURCHES)
}
MENU_TEXTS = {
    text(language, key)
    for language in SUPPORTED_LANGUAGES
    for key in ("menu_help", "menu_about", "menu_settings")
}


@router.message(CommandStart())
async def start_command(message: Message, database: SQLiteDatabase) -> None:
    if message.from_user is None:
        return

    is_new_user, language = await database.register_user(message.from_user.id)
    if is_new_user:
        await message.answer(
            "Добро пожаловать, выберите свою религию",
            reply_markup=church_selection_keyboard(),
        )
        return

    await message.answer(
        text(language, "start"),
        reply_markup=main_menu_keyboard(language),
    )


@router.message(Command("menu"))
async def lotm_menu_command(message: Message) -> None:
    await message.answer(
        "Потусторонний, благодарю за службу.",
        reply_markup=lotm_menu_keyboard(),
    )


@router.callback_query(
    F.data.in_({"menu:get_task", "menu:contribution", "menu:character"})
)
async def acknowledge_menu_button(callback: CallbackQuery) -> None:
    await callback.answer()


@router.callback_query(F.data.in_(CHURCH_CALLBACKS))
async def select_church(callback: CallbackQuery, database: SQLiteDatabase) -> None:
    if callback.from_user is None or callback.data is None:
        await callback.answer()
        return

    church = CHURCH_CALLBACKS[callback.data]
    await database.set_church(callback.from_user.id, church)
    language = await database.get_language(callback.from_user.id)
    await callback.answer()
    if isinstance(callback.message, Message):
        await callback.message.edit_text(f"Вы выбрали: {church}")
        await callback.message.answer(
            text(language, "choose_action"),
            reply_markup=main_menu_keyboard(language),
        )


@router.message(Command("help"))
@router.message(F.text.in_(MENU_TEXTS))
async def menu_message(message: Message, database: SQLiteDatabase) -> None:
    if message.from_user is None or message.text is None:
        return

    language = await database.get_language(message.from_user.id)
    if message.text in {text(item, "menu_help") for item in SUPPORTED_LANGUAGES}:
        await message.answer(text(language, "help"))
    elif message.text in {text(item, "menu_about") for item in SUPPORTED_LANGUAGES}:
        await message.answer(text(language, "about"))
    else:
        await message.answer(
            text(language, "settings"),
            reply_markup=language_keyboard(language),
        )


@router.message(Command("settings"))
async def settings_command(message: Message, database: SQLiteDatabase) -> None:
    language = await _message_language(message, database)
    await message.answer(
        text(language, "settings"),
        reply_markup=language_keyboard(language),
    )


@router.message(Command("delete_me"))
async def delete_me_command(message: Message, database: SQLiteDatabase) -> None:
    if message.from_user is None:
        return

    user_id = message.from_user.id
    language = await database.get_language(user_id)
    await message.answer(
        text(language, "delete_account_prompt"),
        reply_markup=delete_account_keyboard(user_id, language),
    )


@router.callback_query(F.data.startswith("account:delete:"))
async def confirm_delete_me(
    callback: CallbackQuery,
    database: SQLiteDatabase,
) -> None:
    if callback.from_user is None or callback.data is None:
        await callback.answer()
        return

    parts = callback.data.split(":")
    if (
        len(parts) != 4
        or parts[:2] != ["account", "delete"]
        or parts[2] not in {"confirm", "cancel"}
        or not parts[3].isdigit()
    ):
        await callback.answer()
        return
    if int(parts[3]) != callback.from_user.id:
        await callback.answer(
            text("ru", "delete_account_forbidden"),
            show_alert=True,
        )
        return

    language = await database.get_language(callback.from_user.id)
    if parts[2] == "confirm":
        await database.delete_user(callback.from_user.id)
        response_key = "delete_account_done"
    else:
        response_key = "delete_account_cancelled"

    await callback.answer()
    if isinstance(callback.message, Message):
        await callback.message.edit_text(text(language, response_key), reply_markup=None)


@router.callback_query(F.data.in_({"settings:language:ru", "settings:language:en"}))
async def set_language(
    callback: CallbackQuery,
    database: SQLiteDatabase,
) -> None:
    if callback.from_user is None or callback.data is None:
        await callback.answer()
        return

    language = LANGUAGE_CALLBACKS[callback.data]
    await database.set_language(callback.from_user.id, language)
    await callback.answer(text(language, "language_saved"))
    if isinstance(callback.message, Message):
        await callback.message.edit_text(
            text(language, "language_saved"),
            reply_markup=None,
        )
        await callback.message.answer(
            text(language, "choose_action"),
            reply_markup=main_menu_keyboard(language),
        )


async def _message_language(
    message: Message,
    database: SQLiteDatabase,
) -> Language:
    if message.from_user is None:
        return "ru"
    return await database.get_language(message.from_user.id)
