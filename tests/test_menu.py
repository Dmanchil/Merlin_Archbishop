import unittest

from aiogram.types import InlineKeyboardMarkup

from keyboards import lotm_menu_keyboard


class LotmMenuKeyboardTests(unittest.TestCase):
    def test_menu_buttons_are_arranged_in_requested_rows(self) -> None:
        keyboard = lotm_menu_keyboard()

        self.assertIsInstance(keyboard, InlineKeyboardMarkup)
        self.assertEqual(
            [
                [(button.text, button.callback_data) for button in row]
                for row in keyboard.inline_keyboard
            ],
            [
                [("Получить задание", "menu:get_task")],
                [
                    ("Мои очки вклада", "menu:contribution"),
                    ("Персонаж", "menu:character"),
                ],
            ],
        )
