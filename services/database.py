import asyncio
import json
import sqlite3
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from localization import CHURCHES, Language, SUPPORTED_LANGUAGES


class SQLiteDatabase:
    def __init__(
        self,
        path: Path | None = None,
        legacy_settings_path: Path | None = None,
    ) -> None:
        data_dir = Path(__file__).resolve().parent.parent / "data"
        self._path = path or data_dir / "bot.db"
        self._legacy_settings_path = (
            legacy_settings_path or self._path.parent / "user_settings.json"
        )
        self._connection: sqlite3.Connection | None = None
        self._lock = asyncio.Lock()

    async def initialize(self) -> None:
        async with self._lock:
            if self._connection is not None:
                return

            self._path.parent.mkdir(parents=True, exist_ok=True)
            connection = sqlite3.connect(self._path)
            try:
                connection.execute("PRAGMA foreign_keys = ON")
                connection.execute(
                    """
                    CREATE TABLE IF NOT EXISTS "конфиг" (
                        key TEXT PRIMARY KEY,
                        value TEXT NOT NULL
                    )
                    """
                )
                self._migrate_users_schema(connection)
                connection.execute(
                    'INSERT OR IGNORE INTO "конфиг" (key, value) VALUES (?, ?)',
                    ("tictactoe_difficulty", "0.5"),
                )
                connection.execute(
                    """
                    UPDATE "конфиг"
                    SET value = CASE value
                        WHEN 'easy' THEN '0'
                        WHEN 'normal' THEN '0.5'
                        WHEN 'hard' THEN '1'
                        ELSE value
                    END
                    WHERE key = 'tictactoe_difficulty'
                    """
                )
                self._migrate_legacy_settings(connection)
                connection.commit()
            except Exception:
                connection.close()
                raise

            self._connection = connection

    async def close(self) -> None:
        async with self._lock:
            if self._connection is not None:
                self._connection.close()
                self._connection = None

    async def register_user(self, user_id: int) -> tuple[bool, Language]:
        await self.initialize()
        async with self._lock:
            connection = self._get_connection()
            with connection:
                cursor = connection.execute(
                    "INSERT OR IGNORE INTO users (tg_id) VALUES (?)",
                    (user_id,),
                )
            row = connection.execute(
                "SELECT language FROM users WHERE tg_id = ?",
                (user_id,),
            ).fetchone()
            if row is None:
                raise RuntimeError(f"Не удалось зарегистрировать пользователя {user_id}")
            return cursor.rowcount == 1, row[0]

    async def get_language(self, user_id: int) -> Language:
        await self.initialize()
        async with self._lock:
            connection = self._get_connection()
            with connection:
                connection.execute(
                    "INSERT OR IGNORE INTO users (tg_id) VALUES (?)",
                    (user_id,),
                )
            row = connection.execute(
                "SELECT language FROM users WHERE tg_id = ?",
                (user_id,),
            ).fetchone()
            if row is None:
                raise RuntimeError(f"Не удалось загрузить настройки пользователя {user_id}")
            return row[0]

    async def set_church(self, user_id: int, church: str) -> None:
        if church not in CHURCHES:
            raise ValueError(f"Неподдерживаемая церковь: {church}")

        await self.initialize()
        async with self._lock:
            with self._get_connection():
                cursor = self._get_connection().execute(
                    "UPDATE users SET church = ? WHERE tg_id = ?",
                    (church, user_id),
                )
            if cursor.rowcount != 1:
                raise RuntimeError(f"Не удалось найти пользователя {user_id}")

    async def delete_user(self, user_id: int) -> bool:
        await self.initialize()
        async with self._lock:
            with self._get_connection():
                cursor = self._get_connection().execute(
                    "DELETE FROM users WHERE tg_id = ?",
                    (user_id,),
                )
            return cursor.rowcount == 1

    async def append_game_history(
        self,
        user_id: int,
        entry: dict[str, Any],
    ) -> None:
        if not isinstance(entry, dict) or not isinstance(entry.get("game"), str):
            raise ValueError("Запись истории должна содержать название игры")

        await self.initialize()
        async with self._lock:
            connection = self._get_connection()
            with connection:
                row = connection.execute(
                    "SELECT history_of_games FROM users WHERE tg_id = ?",
                    (user_id,),
                ).fetchone()
                if row is None:
                    raise RuntimeError(
                        f"Не удалось сохранить историю: пользователь {user_id} не найден"
                    )

                try:
                    history = json.loads(row[0])
                except json.JSONDecodeError as error:
                    raise ValueError(
                        f"История игр пользователя {user_id} содержит некорректный JSON"
                    ) from error
                if not isinstance(history, list) or any(
                    not isinstance(item, dict) for item in history
                ):
                    raise ValueError(
                        f"История игр пользователя {user_id} должна быть JSON-массивом объектов"
                    )

                saved_entry = dict(entry)
                saved_entry.setdefault(
                    "played_at",
                    datetime.now(timezone.utc).isoformat(timespec="seconds"),
                )
                history.append(saved_entry)
                connection.execute(
                    "UPDATE users SET history_of_games = ? WHERE tg_id = ?",
                    (
                        json.dumps(history, ensure_ascii=False, separators=(",", ":")),
                        user_id,
                    ),
                )

    async def get_game_history(self, user_id: int) -> list[dict[str, Any]]:
        await self.initialize()
        async with self._lock:
            row = self._get_connection().execute(
                "SELECT history_of_games FROM users WHERE tg_id = ?",
                (user_id,),
            ).fetchone()
            if row is None:
                raise RuntimeError(
                    f"Не удалось загрузить историю: пользователь {user_id} не найден"
                )

            try:
                history = json.loads(row[0])
            except json.JSONDecodeError as error:
                raise ValueError(
                    f"История игр пользователя {user_id} содержит некорректный JSON"
                ) from error
            if not isinstance(history, list) or any(
                not isinstance(item, dict) for item in history
            ):
                raise ValueError(
                    f"История игр пользователя {user_id} должна быть JSON-массивом объектов"
                )
            return history

    async def set_language(self, user_id: int, language: Language) -> None:
        if language not in SUPPORTED_LANGUAGES:
            raise ValueError(f"Неподдерживаемый язык: {language}")

        await self.initialize()
        async with self._lock:
            with self._get_connection():
                self._get_connection().execute(
                    """
                    INSERT INTO users (tg_id, language)
                    VALUES (?, ?)
                    ON CONFLICT(tg_id) DO UPDATE SET language = excluded.language
                    """,
                    (user_id, language),
                )

    async def get_config(self, key: str, default: str | None = None) -> str | None:
        await self.initialize()
        async with self._lock:
            row = self._get_connection().execute(
                'SELECT value FROM "конфиг" WHERE key = ?',
                (key,),
            ).fetchone()
            return row[0] if row is not None else default

    async def set_config(self, key: str, value: str) -> None:
        await self.initialize()
        async with self._lock:
            with self._get_connection():
                self._get_connection().execute(
                    """
                    INSERT INTO "конфиг" (key, value)
                    VALUES (?, ?)
                    ON CONFLICT(key) DO UPDATE SET value = excluded.value
                    """,
                    (key, value),
                )

    def _migrate_users_schema(self, connection: sqlite3.Connection) -> None:
        users_exists = connection.execute(
            "SELECT 1 FROM sqlite_master WHERE type = 'table' AND name = 'users'"
        ).fetchone() is not None
        legacy_exists = connection.execute(
            "SELECT 1 FROM sqlite_master WHERE type = 'table' AND name = ?",
            ("пользователи",),
        ).fetchone() is not None

        expected_columns = {
            "tg_id",
            "language",
            "church",
            "sequence",
            "contribution",
            "first_seen",
            "history_of_games",
        }
        if users_exists:
            current_columns = {
                row[1] for row in connection.execute('PRAGMA table_info("users")')
            }
            if current_columns == expected_columns and not legacy_exists:
                return

        sources: list[tuple[str, set[str]]] = []
        if users_exists:
            sources.append(
                (
                    "users",
                    {
                        row[1]
                        for row in connection.execute('PRAGMA table_info("users")')
                    },
                )
            )
        if legacy_exists:
            sources.append(
                (
                    "пользователи",
                    {
                        row[1]
                        for row in connection.execute(
                            'PRAGMA table_info("пользователи")'
                        )
                    },
                )
            )

        connection.execute("DROP TABLE IF EXISTS users__migration")
        connection.execute(
            """
            CREATE TABLE users__migration (
                tg_id INTEGER PRIMARY KEY,
                language TEXT NOT NULL DEFAULT 'ru'
                    CHECK (language IN ('ru', 'en')),
                church TEXT NOT NULL DEFAULT '',
                sequence INTEGER,
                contribution REAL NOT NULL DEFAULT 0,
                first_seen TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                history_of_games TEXT NOT NULL DEFAULT '[]'
            )
            """
        )

        source_fields = {
            "tg_id": ("tg_id", "telegram_id"),
            "language": ("language",),
            "church": ("church",),
            "sequence": ("sequence",),
            "contribution": ("contribution",),
            "first_seen": ("first_seen",),
            "history_of_games": ("history_of_games",),
        }
        for table_name, columns in sources:
            id_column = next(
                (column for column in source_fields["tg_id"] if column in columns),
                None,
            )
            if id_column is None:
                raise ValueError(f"В таблице {table_name} нет столбца tg_id")

            target_columns = ["tg_id"]
            selected_columns = [id_column]
            for target_column, aliases in source_fields.items():
                if target_column == "tg_id":
                    continue
                source_column = next(
                    (column for column in aliases if column in columns),
                    None,
                )
                if source_column is not None:
                    target_columns.append(target_column)
                    selected_columns.append(source_column)

            quoted_table = '"' + table_name.replace('"', '""') + '"'
            quoted_columns = ", ".join(
                '"' + column.replace('"', '""') + '"'
                for column in selected_columns
            )
            rows = connection.execute(
                f"SELECT {quoted_columns} FROM {quoted_table}"
            ).fetchall()
            placeholders = ", ".join("?" for _ in target_columns)
            insert_columns = ", ".join(
                '"' + column.replace('"', '""') + '"'
                for column in target_columns
            )
            connection.executemany(
                f"""
                INSERT INTO users__migration ({insert_columns})
                VALUES ({placeholders})
                ON CONFLICT(tg_id) DO NOTHING
                """,
                rows,
            )

        if users_exists:
            connection.execute("DROP TABLE users")
        if legacy_exists:
            connection.execute('DROP TABLE "пользователи"')
        connection.execute("ALTER TABLE users__migration RENAME TO users")

    def _migrate_legacy_settings(self, connection: sqlite3.Connection) -> None:
        migration_key = "user_settings_json_migrated"
        already_migrated = connection.execute(
            'SELECT 1 FROM "конфиг" WHERE key = ?',
            (migration_key,),
        ).fetchone()
        if already_migrated is not None:
            return

        if self._legacy_settings_path.exists():
            try:
                data: Any = json.loads(
                    self._legacy_settings_path.read_text(encoding="utf-8")
                )
            except json.JSONDecodeError as error:
                raise ValueError(
                    f"Файл настроек повреждён: {self._legacy_settings_path}"
                ) from error

            if not isinstance(data, dict):
                raise ValueError(
                    f"Ожидался JSON-объект в файле настроек: {self._legacy_settings_path}"
                )

            migrated_users: list[tuple[int, str]] = []
            for user_id, user_settings in data.items():
                if (
                    not isinstance(user_id, str)
                    or not user_id.isdecimal()
                    or not isinstance(user_settings, dict)
                    or user_settings.get("language") not in SUPPORTED_LANGUAGES
                ):
                    raise ValueError(
                        "Некорректная запись настроек пользователя в "
                        f"{self._legacy_settings_path}"
                    )
                migrated_users.append((int(user_id), user_settings["language"]))

            connection.executemany(
                """
                INSERT INTO users (tg_id, language)
                VALUES (?, ?)
                ON CONFLICT(tg_id) DO NOTHING
                """,
                migrated_users,
            )

        connection.execute(
            'INSERT INTO "конфиг" (key, value) VALUES (?, ?)',
            (migration_key, "true"),
        )

    def _get_connection(self) -> sqlite3.Connection:
        if self._connection is None:
            raise RuntimeError("База данных не инициализирована")
        return self._connection
