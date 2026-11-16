from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from localization import Language, text


def difficulty_games_keyboard(
    user_id: int,
    language: Language,
    tictactoe_difficulty: str,
    rps_difficulty: str,
) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=text(language, "difficulty_tictactoe").format(
                        difficulty=tictactoe_difficulty
                    ),
                    callback_data=f"difficulty:select:{user_id}:tictactoe",
                )
            ],
            [
                InlineKeyboardButton(
                    text=text(language, "difficulty_rps").format(
                        difficulty=rps_difficulty
                    ),
                    callback_data=f"difficulty:select:{user_id}:rps",
                )
            ],
        ],
    )
