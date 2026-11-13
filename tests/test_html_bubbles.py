import unittest

from services.html_bubbles import (
    SendWidget,
    load_tictactoe_html,
    normalize_tictactoe_difficulty,
)


class HtmlBubbleTests(unittest.TestCase):
    def test_tictactoe_html_embeds_numeric_difficulty(self) -> None:
        for difficulty in ("0", "0.5", "0.7", "1"):
            with self.subTest(difficulty=difficulty):
                html = load_tictactoe_html(difficulty)

                self.assertIn("<main class=\"game\">", html)
                self.assertIn(f"const DIFFICULTY={difficulty}", html)
                self.assertNotIn("__TICTACTOE_DIFFICULTY__", html)

    def test_difficulty_is_normalized_and_range_checked(self) -> None:
        self.assertEqual(normalize_tictactoe_difficulty(".70"), "0.7")
        for value in ("-0.1", "1.1", "NaN", "impossible"):
            with self.subTest(value=value):
                with self.assertRaisesRegex(ValueError, "числом от 0 до 1"):
                    load_tictactoe_html(value)

    def test_send_widget_uses_expected_bot_api_method(self) -> None:
        method = SendWidget(chat_id=123, html="<main>game</main>")

        self.assertEqual(method.__api_method__, "sendWidget")
        self.assertEqual(method.chat_id, 123)
        self.assertEqual(method.html, "<main>game</main>")


if __name__ == "__main__":
    unittest.main()
