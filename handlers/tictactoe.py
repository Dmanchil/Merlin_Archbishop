from aiogram import F, Router
from aiogram.filters import Command
from aiogram.types import CallbackQuery, Message

from keyboards import tictactoe_keyboard
from localization import Language, text
from services.database import SQLiteDatabase
from services.tictactoe import (
    COMPUTER_MARK,
    DEFAULT_TICTACTOE_DIFFICULTY,
    EMPTY_CELL,
    PLAYER_MARK,
    TICTACTOE_DIFFICULTY_CONFIG_KEY,
    choose_computer_move,
    get_winner,
    is_finished,
    is_valid_board,
    new_board,
    normalize_tictactoe_difficulty,
)

router = Router(name="tictactoe")


@router.message(Command("tictactoe"))
async def tictactoe_command(
    message: Message,
    database: SQLiteDatabase,
) -> None:
    if message.from_user is None:
        return

    language: Language = await database.get_language(message.from_user.id)

    await message.answer(
        text(language, "ttt_your_turn"),
        reply_markup=tictactoe_keyboard(
            new_board(),
            message.from_user.id,
            language,
            finished=False,
        ),
    )


@router.callback_query(F.data.startswith("ttt:"))
async def tictactoe_callback(
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
    language = await database.get_language(callback.from_user.id)
    if int(parts[2]) != callback.from_user.id:
        await callback.answer(
            text(language, "ttt_not_your_game"),
            show_alert=True,
        )
        return
    if parts[1] == "restart" and len(parts) == 3:
        await _update_game_message(
            callback,
            new_board(),
            language,
            text(language, "ttt_your_turn"),
        )
        return

    if parts[1] == "finished" and len(parts) == 3:
        await callback.answer()
        return

    if (
        parts[1] != "move"
        or len(parts) != 5
        or not parts[4].isdigit()
        or not is_valid_board(parts[3])
        or is_finished(parts[3])
    ):
        await callback.answer(text(language, "ttt_invalid_move"), show_alert=True)
        return

    board = parts[3]
    move = int(parts[4])
    if move >= len(board) or board[move] != EMPTY_CELL:
        await callback.answer(text(language, "ttt_invalid_move"), show_alert=True)
        return

    updated_board = list(board)
    updated_board[move] = PLAYER_MARK
    current_board = "".join(updated_board)
    winner = get_winner(current_board)
    if winner is None and not is_finished(current_board):
        difficulty = await database.get_config(
            TICTACTOE_DIFFICULTY_CONFIG_KEY,
            DEFAULT_TICTACTOE_DIFFICULTY,
        )
        try:
            normalized_difficulty = normalize_tictactoe_difficulty(difficulty or "")
        except ValueError:
            await callback.answer(text(language, "difficulty_invalid"), show_alert=True)
            return
        computer_move = choose_computer_move(current_board, normalized_difficulty)
        updated_board[computer_move] = COMPUTER_MARK
        current_board = "".join(updated_board)
        winner = get_winner(current_board)

    if winner == PLAYER_MARK:
        status = text(language, "ttt_player_won")
        result = "win"
    elif winner == COMPUTER_MARK:
        status = text(language, "ttt_computer_won")
        result = "loss"
    elif is_finished(current_board):
        status = text(language, "ttt_draw")
        result = "draw"
    else:
        status = text(language, "ttt_your_turn")
        result = None

    if result is not None:
        await database.append_game_history(
            callback.from_user.id,
            {
                "game": "tictactoe",
                "result": result,
                "board": current_board,
            },
        )
    await _update_game_message(callback, current_board, language, status)


async def _update_game_message(
    callback: CallbackQuery,
    board: str,
    language: Language,
    status: str,
) -> None:
    await callback.answer()
    if isinstance(callback.message, Message):
        await callback.message.edit_text(
            status,
            reply_markup=tictactoe_keyboard(
                board,
                callback.from_user.id,
                language,
                finished=is_finished(board),
            ),
        )
