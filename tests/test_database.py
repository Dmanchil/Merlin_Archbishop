import json
import sqlite3
import tempfile
import unittest
from contextlib import closing
from pathlib import Path

from aiogram.types import InlineKeyboardMarkup
from keyboards import church_selection_keyboard
from localization import CHURCHES
from services.database import SQLiteDatabase


class SQLiteDatabaseTests(unittest.IsolatedAsyncioTestCase):
    async def test_user_registration_reports_first_appearance_once(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            database_path = Path(directory) / "bot.db"
            database = SQLiteDatabase(database_path)

            self.assertEqual(await database.register_user(123), (True, "ru"))
            self.assertEqual(await database.register_user(123), (False, "ru"))
            self.assertEqual(await database.get_game_history(123), [])

            await database.set_church(123, "Церковь Вечной Ночи")
            await database.append_game_history(
                123,
                {"game": "rps", "result": "win", "player_choice": "rock"},
            )
            await database.append_game_history(
                123,
                {"game": "tictactoe", "result": "draw", "board": "XOXOXOOXX"},
            )
            history = await database.get_game_history(123)
            with closing(sqlite3.connect(database_path)) as connection:
                church = connection.execute(
                    "SELECT church FROM users WHERE tg_id = ?",
                    (123,),
                ).fetchone()[0]
                raw_history = connection.execute(
                    "SELECT history_of_games FROM users WHERE tg_id = ?",
                    (123,),
                ).fetchone()[0]

            self.assertEqual(church, "Церковь Вечной Ночи")
            self.assertEqual(len(history), 2)
            self.assertEqual([entry["game"] for entry in history], ["rps", "tictactoe"])
            self.assertTrue(all(entry.get("played_at") for entry in history))
            self.assertEqual(json.loads(raw_history), history)
            await database.close()

    def test_church_keyboard_has_one_button_per_row(self) -> None:
        keyboard = church_selection_keyboard("ru")

        self.assertIsInstance(keyboard, InlineKeyboardMarkup)
        self.assertEqual(
            [
                [(button.text, button.callback_data) for button in row]
                for row in keyboard.inline_keyboard
            ],
            [
                [(church, f"church:{index}")]
                for index, church in enumerate(CHURCHES)
            ],
        )

    async def test_set_church_rejects_unknown_church(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            database = SQLiteDatabase(Path(directory) / "bot.db")
            await database.register_user(123)

            with self.assertRaisesRegex(ValueError, "Неподдерживаемая церковь"):
                await database.set_church(123, "Неизвестная церковь")

            await database.close()

    async def test_delete_user_removes_only_user_record(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            database = SQLiteDatabase(Path(directory) / "bot.db")
            await database.register_user(123)
            await database.set_config("test_setting", "preserved")

            self.assertTrue(await database.delete_user(123))
            self.assertFalse(await database.delete_user(123))
            self.assertEqual(await database.get_config("test_setting"), "preserved")

            with closing(sqlite3.connect(Path(directory) / "bot.db")) as connection:
                user_count = connection.execute(
                    "SELECT COUNT(*) FROM users WHERE tg_id = ?",
                    (123,),
                ).fetchone()[0]

            self.assertEqual(user_count, 0)
            await database.close()

    async def test_language_is_persisted_per_user(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            database_path = Path(directory) / "bot.db"
            database = SQLiteDatabase(database_path)

            self.assertEqual(await database.get_language(123), "ru")
            await database.set_language(123, "en")
            await database.close()

            reloaded_database = SQLiteDatabase(database_path)
            self.assertEqual(await reloaded_database.get_language(123), "en")
            self.assertEqual(await reloaded_database.get_language(456), "ru")

            with closing(sqlite3.connect(database_path)) as connection:
                users = connection.execute(
                    "SELECT tg_id, language FROM users ORDER BY tg_id"
                ).fetchall()
                tables = {
                    row[0]
                    for row in connection.execute(
                        "SELECT name FROM sqlite_master WHERE type = 'table'"
                    )
                }

            self.assertEqual(users, [(123, "en"), (456, "ru")])
            self.assertTrue({"users", "конфиг"}.issubset(tables))
            self.assertNotIn("пользователи", tables)
            await reloaded_database.close()

    async def test_old_users_table_is_migrated_with_language_preserved(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            database_path = Path(directory) / "bot.db"
            with closing(sqlite3.connect(database_path)) as connection:
                connection.execute(
                    """
                    CREATE TABLE "пользователи" (
                        telegram_id INTEGER PRIMARY KEY,
                        language TEXT NOT NULL DEFAULT 'ru'
                    )
                    """
                )
                connection.execute(
                    'INSERT INTO "пользователи" (telegram_id, language) VALUES (?, ?)',
                    (123, "en"),
                )
                connection.commit()

            database = SQLiteDatabase(database_path)
            self.assertEqual(await database.get_language(123), "en")

            with closing(sqlite3.connect(database_path)) as connection:
                columns = [
                    row[1]
                    for row in connection.execute("PRAGMA table_info(users)")
                ]
                row = connection.execute(
                    """
                    SELECT tg_id, language, church, sequence, contribution, first_seen,
                           history_of_games
                    FROM users WHERE tg_id = ?
                    """,
                    (123,),
                ).fetchone()
                old_table = connection.execute(
                    "SELECT 1 FROM sqlite_master WHERE type = 'table' AND name = ?",
                    ("пользователи",),
                ).fetchone()

            self.assertEqual(
                columns,
                [
                    "tg_id",
                    "language",
                    "church",
                    "sequence",
                    "contribution",
                    "first_seen",
                    "history_of_games",
                ],
            )
            self.assertEqual(row[:5], (123, "en", "", None, 0.0))
            self.assertTrue(row[5])
            self.assertEqual(json.loads(row[6]), [])
            self.assertIsNone(old_table)
            await database.close()

    async def test_legacy_json_is_migrated_once(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            legacy_path = root / "user_settings.json"
            legacy_path.write_text(
                json.dumps({"123": {"language": "en"}}),
                encoding="utf-8",
            )
            database = SQLiteDatabase(root / "bot.db", legacy_path)

            self.assertEqual(await database.get_language(123), "en")
            await database.set_language(123, "ru")
            await database.close()

            legacy_path.write_text(
                json.dumps({"123": {"language": "en"}, "456": {"language": "en"}}),
                encoding="utf-8",
            )
            reloaded_database = SQLiteDatabase(root / "bot.db", legacy_path)
            self.assertEqual(await reloaded_database.get_language(123), "ru")
            self.assertEqual(await reloaded_database.get_language(456), "ru")
            await reloaded_database.close()

    async def test_config_can_be_stored(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            database = SQLiteDatabase(Path(directory) / "bot.db")

            self.assertEqual(
                await database.get_config("tictactoe_difficulty"),
                "0.5",
            )
            self.assertIsNone(await database.get_config("maintenance"))
            await database.set_config("maintenance", "enabled")
            await database.set_config("tictactoe_difficulty", "0.7")

            self.assertEqual(
                await database.get_config("maintenance"),
                "enabled",
            )
            self.assertEqual(
                await database.get_config("tictactoe_difficulty"),
                "0.7",
            )
            self.assertEqual(
                await database.get_config("unknown", "disabled"),
                "disabled",
            )
            await database.close()

    async def test_old_named_difficulty_is_migrated(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            database_path = Path(directory) / "bot.db"
            with closing(sqlite3.connect(database_path)) as connection:
                connection.execute(
                    'CREATE TABLE "конфиг" (key TEXT PRIMARY KEY, value TEXT NOT NULL)'
                )
                connection.execute(
                    'INSERT INTO "конфиг" (key, value) VALUES (?, ?)',
                    ("tictactoe_difficulty", "hard"),
                )
                connection.commit()

            database = SQLiteDatabase(database_path)
            self.assertEqual(
                await database.get_config("tictactoe_difficulty"),
                "1",
            )
            await database.close()

    async def test_invalid_legacy_json_is_reported(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            legacy_path = root / "user_settings.json"
            legacy_path.write_text("{invalid", encoding="utf-8")
            database = SQLiteDatabase(root / "bot.db", legacy_path)

            with self.assertRaisesRegex(ValueError, "Файл настроек повреждён"):
                await database.initialize()


if __name__ == "__main__":
    unittest.main()
