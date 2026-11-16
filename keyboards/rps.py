from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from localization import Language, text
from services.rps import GESTURES, Gesture


def rps_keyboard(
    user_id: int,
    language: Language,
    round_number: int = 0,
) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=text(language, f"rps_{gesture}"),
                    callback_data=f"rps:choose:{user_id}:{round_number}:{gesture}",
                )
                for gesture in GESTURES
            ],
            [
                InlineKeyboardButton(
                    text=text(language, "rps_new_game"),
                    callback_data=f"rps:new:{user_id}",
                )
            ],
        ],
    )
