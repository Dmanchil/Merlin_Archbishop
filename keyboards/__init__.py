from keyboards.main import (
    church_selection_keyboard,
    lotm_menu_keyboard,
    main_menu_keyboard,
    task_confirmation_keyboard,
)
from keyboards.difficulty import difficulty_games_keyboard
from keyboards.rps import rps_keyboard
from keyboards.settings import delete_account_keyboard, language_keyboard
from keyboards.tictactoe import tictactoe_keyboard

__all__ = [
    "church_selection_keyboard",
    "delete_account_keyboard",
    "difficulty_games_keyboard",
    "language_keyboard",
    "lotm_menu_keyboard",
    "main_menu_keyboard",
    "rps_keyboard",
    "task_confirmation_keyboard",
    "tictactoe_keyboard",
]
