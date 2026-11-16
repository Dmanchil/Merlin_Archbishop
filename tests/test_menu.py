import unittest

from aiogram.types import InlineKeyboardMarkup

from keyboards import (
    church_selection_keyboard,
    lotm_menu_keyboard,
    task_confirmation_keyboard,
)
from localization import CHURCHES, church_name


class LotmMenuKeyboardTests(unittest.TestCase):
    def test_menu_buttons_are_arranged_and_localized(self) -> None:
        for language, expected_labels in (
            (
                "ru",
                ("Получить задание", "Мои очки вклада", "Персонаж"),
            ),
            ("en", ("Get a mission", "My contribution points", "Character")),
        ):
            with self.subTest(language=language):
                keyboard = lotm_menu_keyboard(language)

                self.assertIsInstance(keyboard, InlineKeyboardMarkup)
                self.assertEqual(
                    [[button.text for button in row] for row in keyboard.inline_keyboard],
                    [[expected_labels[0]], [expected_labels[1], expected_labels[2]]],
                )

    def test_church_keyboard_is_localized_and_preserves_callbacks(self) -> None:
        for language in ("ru", "en"):
            with self.subTest(language=language):
                keyboard = church_selection_keyboard(language)
                self.assertEqual(
                    [
                        [(button.text, button.callback_data) for button in row]
                        for row in keyboard.inline_keyboard
                    ],
                    [
                        [(church_name(language, church), f"church:{index}")]
                        for index, church in enumerate(CHURCHES)
                    ],
                )

    def test_task_confirmation_keyboard_is_localized_and_user_scoped(self) -> None:
        for language, labels in (
            ("ru", ("Приступить", "Назад")),
            ("en", ("Proceed", "Back")),
        ):
            with self.subTest(language=language):
                keyboard = task_confirmation_keyboard(123, language)
                self.assertEqual(
                    [
                        (button.text, button.callback_data)
                        for button in keyboard.inline_keyboard[0]
                    ],
                    [
                        (labels[0], "task:proceed:123"),
                        (labels[1], "task:back:123"),
                    ],
                )
