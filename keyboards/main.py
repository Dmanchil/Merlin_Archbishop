from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    KeyboardButton,
    ReplyKeyboardMarkup,
)

from localization import CHURCHES, Language, text


def church_selection_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=church,
                    callback_data=f"church:{index}",
                )
            ]
            for index, church in enumerate(CHURCHES)
        ],
    )


def lotm_menu_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="Получить задание",
                    callback_data="menu:get_task",
                )
            ],
            [
                InlineKeyboardButton(
                    text="Мои очки вклада",
                    callback_data="menu:contribution",
                ),
                InlineKeyboardButton(
                    text="Персонаж",
                    callback_data="menu:character",
                ),
            ],
        ],
    )


def main_menu_keyboard(language: Language) -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text=text(language, "menu_help")),
                KeyboardButton(text=text(language, "menu_about")),
            ],
            [KeyboardButton(text=text(language, "menu_settings"))],
        ],
        resize_keyboard=True,
    )
