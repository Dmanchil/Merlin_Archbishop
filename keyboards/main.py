from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    KeyboardButton,
    ReplyKeyboardMarkup,
)

from localization import CHURCHES, Language, church_name, text


def church_selection_keyboard(language: Language) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=church_name(language, church),
                    callback_data=f"church:{index}",
                )
            ]
            for index, church in enumerate(CHURCHES)
        ],
    )


def lotm_menu_keyboard(language: Language) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=text(language, "lotm_menu_get_task"),
                    callback_data="menu:get_task",
                )
            ],
            [
                InlineKeyboardButton(
                    text=text(language, "lotm_menu_contribution"),
                    callback_data="menu:contribution",
                ),
                InlineKeyboardButton(
                    text=text(language, "lotm_menu_character"),
                    callback_data="menu:character",
                ),
            ],
        ],
    )


def task_confirmation_keyboard(
    user_id: int,
    language: Language,
) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=text(language, "task_proceed"),
                    callback_data=f"task:proceed:{user_id}",
                ),
                InlineKeyboardButton(
                    text=text(language, "task_back"),
                    callback_data=f"task:back:{user_id}",
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
