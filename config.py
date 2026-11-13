import os
from dataclasses import dataclass

from dotenv import load_dotenv

load_dotenv()


@dataclass(frozen=True, slots=True)
class Config:
    bot_token: str
    admin_ids: frozenset[int]

    @classmethod
    def from_env(cls) -> "Config":
        bot_token = os.getenv("BOT_TOKEN", "").strip()
        if not bot_token:
            raise ValueError("Укажите токен бота в переменной BOT_TOKEN файла .env")

        raw_admin_ids = os.getenv("ADMIN_IDS", "").strip()
        try:
            admin_ids = frozenset(
                int(admin_id.strip())
                for admin_id in raw_admin_ids.split(",")
                if admin_id.strip()
            )
        except ValueError as error:
            raise ValueError(
                "ADMIN_IDS должен содержать числовые Telegram ID через запятую"
            ) from error

        if not admin_ids:
            raise ValueError("Укажите хотя бы один Telegram ID в переменной ADMIN_IDS")

        return cls(bot_token=bot_token, admin_ids=admin_ids)
