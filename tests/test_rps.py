import unittest
from unittest.mock import patch

from aiogram.types import InlineKeyboardMarkup

from keyboards import difficulty_games_keyboard, rps_keyboard
from services.rps import (
    choose_computer_gesture,
    get_result,
    is_gesture,
    normalize_rps_difficulty,
)


class RockPaperScissorsTests(unittest.TestCase):
    def test_difficulty_menu_shows_games_and_current_values(self) -> None:
        cases = (
            (
                "ru",
                "Крестики-нолики — 0.4",
                "Камень, ножницы, бумага — 0.8",
            ),
            (
                "en",
                "Tic-tac-toe — 0.4",
                "Rock, Paper, Scissors — 0.8",
            ),
        )
        for language, ttt_label, rps_label in cases:
            with self.subTest(language=language):
                keyboard = difficulty_games_keyboard(
                    123,
                    language,
                    "0.4",
                    "0.8",
                )
                self.assertEqual(
                    [[button.text for button in row] for row in keyboard.inline_keyboard],
                    [[ttt_label], [rps_label]],
                )
                self.assertEqual(
                    [
                        row[0].callback_data
                        for row in keyboard.inline_keyboard
                    ],
                    [
                        "difficulty:select:123:tictactoe",
                        "difficulty:select:123:rps",
                    ],
                )

    def test_keyboard_rows_and_callbacks_are_localized(self) -> None:
        cases = (
            (
                "ru",
                ["Камень", "Ножницы", "Бумага"],
                "Новая игра",
            ),
            (
                "en",
                ["Rock", "Scissors", "Paper"],
                "New game",
            ),
        )
        for language, choices, new_game in cases:
            with self.subTest(language=language):
                keyboard = rps_keyboard(123, language)
                self.assertIsInstance(keyboard, InlineKeyboardMarkup)
                self.assertEqual(
                    [[button.text for button in row] for row in keyboard.inline_keyboard],
                    [choices, [new_game]],
                )
                self.assertEqual(
                    [button.callback_data for button in keyboard.inline_keyboard[0]],
                    [
                        "rps:choose:123:0:rock",
                        "rps:choose:123:0:scissors",
                        "rps:choose:123:0:paper",
                    ],
                )
                self.assertEqual(
                    keyboard.inline_keyboard[1][0].callback_data,
                    "rps:new:123",
                )

    def test_all_gesture_outcomes(self) -> None:
        self.assertEqual(get_result("rock", "scissors"), "win")
        self.assertEqual(get_result("scissors", "paper"), "win")
        self.assertEqual(get_result("paper", "rock"), "win")
        self.assertEqual(get_result("scissors", "rock"), "loss")
        self.assertEqual(get_result("paper", "scissors"), "loss")
        self.assertEqual(get_result("rock", "paper"), "loss")
        for gesture in ("rock", "scissors", "paper"):
            self.assertEqual(get_result(gesture, gesture), "draw")

    def test_gesture_validation(self) -> None:
        for gesture in ("rock", "scissors", "paper"):
            self.assertTrue(is_gesture(gesture))
        self.assertFalse(is_gesture("lizard"))

    def test_difficulty_is_normalized_and_range_checked(self) -> None:
        self.assertEqual(normalize_rps_difficulty(".70"), "0.7")
        for value in ("-0.1", "1.1", "NaN", "impossible"):
            with self.subTest(value=value):
                with self.assertRaisesRegex(ValueError, "числом от 0 до 1"):
                    normalize_rps_difficulty(value)

    def test_maximum_difficulty_selects_winning_gesture(self) -> None:
        for player, winning_gesture in (
            ("rock", "paper"),
            ("scissors", "rock"),
            ("paper", "scissors"),
        ):
            with self.subTest(player=player):
                with patch("services.rps.random.random", return_value=0.99):
                    self.assertEqual(
                        choose_computer_gesture(player, "1"),
                        winning_gesture,
                    )

    def test_zero_difficulty_uses_random_gesture(self) -> None:
        with (
            patch("services.rps.random.random", return_value=0.5),
            patch("services.rps.random.choice", return_value="scissors") as choice,
        ):
            self.assertEqual(choose_computer_gesture("rock", "0"), "scissors")
        choice.assert_called_once_with(("rock", "scissors", "paper"))


if __name__ == "__main__":
    unittest.main()
