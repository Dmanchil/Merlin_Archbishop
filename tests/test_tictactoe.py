import unittest

from keyboards import tictactoe_keyboard
from services.tictactoe import (
    COMPUTER_MARK,
    EMPTY_CELL,
    PLAYER_MARK,
    choose_computer_move,
    get_winner,
    is_finished,
    is_valid_board,
    new_board,
    normalize_tictactoe_difficulty,
)


class TicTacToeTests(unittest.TestCase):
    def test_difficulty_is_normalized_and_range_checked(self) -> None:
        self.assertEqual(normalize_tictactoe_difficulty(".70"), "0.7")
        for value in ("-0.1", "1.1", "NaN", "impossible"):
            with self.subTest(value=value):
                with self.assertRaisesRegex(ValueError, "числом от 0 до 1"):
                    normalize_tictactoe_difficulty(value)

    def test_new_board_is_empty_and_valid(self) -> None:
        board = new_board()

        self.assertEqual(board, EMPTY_CELL * 9)
        self.assertTrue(is_valid_board(board))
        self.assertFalse(is_finished(board))

    def test_winner_is_detected(self) -> None:
        self.assertEqual(get_winner("XXXOO____"), PLAYER_MARK)
        self.assertEqual(get_winner("X_OX_OX__"), PLAYER_MARK)
        self.assertIsNone(get_winner("XOXOOXXXO"))

    def test_board_validation_requires_equal_turn_counts(self) -> None:
        self.assertFalse(is_valid_board("XX_______"))
        self.assertFalse(is_valid_board("XXXXXXXXX"))
        self.assertTrue(is_valid_board("X_O______"))

    def test_computer_takes_a_winning_move_on_full_difficulty(self) -> None:
        board = "OO_XX____"

        move = choose_computer_move(board, "1")

        self.assertEqual(move, 2)

    def test_computer_blocks_player_win_on_full_difficulty(self) -> None:
        board = "XX__O____"

        move = choose_computer_move(board, "1")

        self.assertEqual(move, 2)

    def test_zero_difficulty_uses_random_move(self) -> None:
        board = "X_O______"

        move = choose_computer_move(board, "0", random_value=0.5)

        self.assertEqual(board[move], EMPTY_CELL)

    def test_keyboard_carries_player_scoped_game_state(self) -> None:
        board = new_board()

        keyboard = tictactoe_keyboard(
            board,
            user_id=123,
            language="en",
            finished=False,
        )

        self.assertEqual(len(keyboard.inline_keyboard), 4)
        self.assertEqual(
            keyboard.inline_keyboard[0][0].callback_data,
            "ttt:move:123:_________:0",
        )
        self.assertLessEqual(
            len(keyboard.inline_keyboard[0][0].callback_data or ""),
            64,
        )

    def test_finished_keyboard_offers_new_game(self) -> None:
        keyboard = tictactoe_keyboard(
            "XXXOO____",
            user_id=123,
            language="en",
            finished=True,
        )

        self.assertEqual(len(keyboard.inline_keyboard), 4)
        self.assertEqual(keyboard.inline_keyboard[-1][0].text, "New game")
        self.assertEqual(
            keyboard.inline_keyboard[-1][0].callback_data,
            "ttt:restart:123",
        )
