from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from localization import Language, text
from services.tictactoe import (
    COMPUTER_MARK,
    EMPTY_CELL,
    PLAYER_MARK,
)


def tictactoe_keyboard(
    board: str,
    user_id: int,
    language: Language,
    finished: bool,
) -> InlineKeyboardMarkup:
    keyboard = []
    for row_start in range(0, len(board), 3):
        row = []
        for index in range(row_start, row_start + 3):
            mark = board[index]
            label = {
                EMPTY_CELL: str(index + 1),
                PLAYER_MARK: "❌",
                COMPUTER_MARK: "⭕",
            }[mark]
            callback_data = (
                f"ttt:move:{user_id}:{board}:{index}"
                if not finished
                else f"ttt:finished:{user_id}"
            )
            row.append(
                InlineKeyboardButton(
                    text=label,
                    callback_data=callback_data,
                )
            )
        keyboard.append(row)

    keyboard.append(
        [
            InlineKeyboardButton(
                text=text(language, "ttt_new_game"),
                callback_data=f"ttt:restart:{user_id}",
            )
        ]
    )
    return InlineKeyboardMarkup(inline_keyboard=keyboard)
