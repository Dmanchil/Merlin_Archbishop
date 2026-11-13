from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from localization import Language, text


def delete_account_keyboard(user_id: int, language: Language) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=text(language, "delete_account_confirm"),
                    callback_data=f"account:delete:confirm:{user_id}",
                ),
                InlineKeyboardButton(
                    text=text(language, "delete_account_cancel"),
                    callback_data=f"account:delete:cancel:{user_id}",
                ),
            ],
        ],
    )


def language_keyboard(language: Language) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=text(language, "language_russian"),
                    callback_data="settings:language:ru",
                ),
                InlineKeyboardButton(
                    text=text(language, "language_english"),
                    callback_data="settings:language:en",
                ),
            ],
        ],
    )
