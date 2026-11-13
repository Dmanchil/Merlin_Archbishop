from typing import Literal

Language = Literal["ru", "en"]
DEFAULT_LANGUAGE: Language = "ru"
SUPPORTED_LANGUAGES: tuple[Language, ...] = ("ru", "en")
CHURCHES: tuple[str, ...] = (
    "Церковь Вечной Ночи",
    "Церковь Повелителя Бури",
    "Церковь Бога Пара и Машин",
)

TEXTS: dict[Language, dict[str, str]] = {
    "ru": {
        "start": "Привет! Бот запущен. Выбери пункт меню или отправь /help.",
        "choose_action": "Выбери пункт меню.",
        "help": (
            "Доступные команды:\n"
            "/start — запустить бота\n"
            "/help — показать помощь\n"
            "/settings — настройки\n"
            "/menu — открыть меню\n"
            "/delete_me — удалить свои данные из бота\n"
            "/admin — команда для администраторов"
        ),
        "delete_account_prompt": (
            "Вы уверены, что хотите удалить свои данные из базы бота? "
            "Это действие нельзя отменить."
        ),
        "delete_account_confirm": "Удалить мои данные",
        "delete_account_cancel": "Отмена",
        "delete_account_done": "Ваши данные удалены из базы бота.",
        "delete_account_cancelled": "Удаление отменено.",
        "delete_account_forbidden": "Эта кнопка предназначена для другого пользователя.",
        "about": "Здесь будет информация о боте.",
        "settings": "Настройки пользователя\nВыбери язык:",
        "language_saved": "Язык сохранён: Русский.",
        "menu_help": "Помощь",
        "menu_about": "О боте",
        "menu_settings": "Настройки",
        "language_russian": "Русский 🇷🇺",
        "language_english": "English 🇬🇧",
        "no_access": "У вас нет доступа к этой команде.",
        "admin_panel": "Панель администратора. Добавьте сюда нужные команды.",
        "difficulty_invalid": (
            "В конфиге указана неверная сложность. Укажите число от 0 до 1."
        ),
        "difficulty_usage": "Укажите сложность числом от 0 до 1, например: /setdifficulty 0.7",
        "difficulty_updated": "Сложность крестиков-ноликов установлена: {difficulty}.",
        "widget_unavailable": (
            "Не удалось отправить HTMLBubble. Возможно, используемый сервер "
            "Telegram Bot API не поддерживает метод sendWidget."
        ),
    },
    "en": {
        "start": "Hello! The bot is running. Choose a menu item or send /help.",
        "choose_action": "Choose a menu item.",
        "help": (
            "Available commands:\n"
            "/start — start the bot\n"
            "/help — show help\n"
            "/settings — settings\n"
            "/menu — open the menu\n"
            "/delete_me — delete your data from the bot\n"
            "/admin — admin command"
        ),
        "delete_account_prompt": (
            "Are you sure you want to delete your data from the bot database? "
            "This action cannot be undone."
        ),
        "delete_account_confirm": "Delete my data",
        "delete_account_cancel": "Cancel",
        "delete_account_done": "Your data has been deleted from the bot database.",
        "delete_account_cancelled": "Deletion cancelled.",
        "delete_account_forbidden": "This button belongs to another user.",
        "about": "Bot information will be here.",
        "settings": "User settings\nChoose a language:",
        "language_saved": "Language saved: English.",
        "menu_help": "Help",
        "menu_about": "About",
        "menu_settings": "Settings",
        "language_russian": "Русский 🇷🇺",
        "language_english": "English 🇬🇧",
        "no_access": "You do not have access to this command.",
        "admin_panel": "Admin panel. Add your commands here.",
        "difficulty_invalid": (
            "Invalid difficulty in config. Enter a number from 0 to 1."
        ),
        "difficulty_usage": "Enter a difficulty from 0 to 1, for example: /setdifficulty 0.7",
        "difficulty_updated": "Tic-tac-toe difficulty set to {difficulty}.",
        "widget_unavailable": (
            "Could not send the HTMLBubble. The configured Telegram Bot API "
            "server may not support the sendWidget method."
        ),
    },
}


def text(language: Language, key: str) -> str:
    return TEXTS[language][key]
