from typing import Literal

Language = Literal["ru", "en"]
DEFAULT_LANGUAGE: Language = "ru"
SUPPORTED_LANGUAGES: tuple[Language, ...] = ("ru", "en")
CHURCHES: tuple[str, ...] = (
    "Церковь Вечной Ночи",
    "Церковь Повелителя Бури",
    "Церковь Бога Пара и Машин",
)
CHURCH_NAMES: dict[Language, tuple[str, ...]] = {
    "ru": CHURCHES,
    "en": (
        "Church of the Eternal Night",
        "Church of the Lord of Storms",
        "Church of the God of Steam and Machinery",
    ),
}

TEXTS: dict[Language, dict[str, str]] = {
    "ru": {
        "welcome_choose_church": "Добро пожаловать, выберите свою религию",
        "start": "Привет! Бот запущен. Выбери пункт меню или отправь /help.",
        "choose_action": "Выбери пункт меню.",
        "church_selected": "Вы выбрали: {church}",
        "lotm_menu_greeting": "Потусторонний, благодарю за службу.",
        "lotm_menu_get_task": "Получить задание",
        "lotm_menu_contribution": "Мои очки вклада",
        "lotm_menu_character": "Персонаж",
        "task_warning": "Потусторонний, вы уверенны? Задание довольно опасно",
        "task_proceed": "Приступить",
        "task_back": "Назад",
        "task_started": "Вы приступили к заданию.",
        "task_returned": "Возвращено в меню.",
        "task_button_forbidden": "Эта кнопка предназначена для другого пользователя.",
        "help": (
            "Доступные команды:\n"
            "/start — запустить бота\n"
            "/help — показать помощь\n"
            "/settings — настройки\n"
            "/menu — открыть меню\n"
            "/tictactoe — сыграть в крестики-нолики\n"
            "/rps — сыграть в камень, ножницы, бумага\n"
            "/setdifficulty — настроить сложность игр (админ)\n"
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
        "difficulty_usage": "Отправьте число от 0 до 1, например: 0.7.",
        "difficulty_choose_game": "Выберите игру для настройки сложности:",
        "difficulty_tictactoe": "Крестики-нолики — {difficulty}",
        "difficulty_tictactoe_name": "Крестики-нолики",
        "difficulty_rps": "Камень, ножницы, бумага — {difficulty}",
        "difficulty_rps_name": "Камень, ножницы, бумага",
        "difficulty_enter_value": (
            "Текущая сложность игры «{game}»: {difficulty}.\n"
            "Отправьте новое число от 0 до 1 или /cancel для отмены."
        ),
        "difficulty_cancelled": "Изменение сложности отменено.",
        "difficulty_updated": "Сложность игры «{game}» установлена: {difficulty}.",
        "ttt_your_turn": "Крестики-нолики\nВаш ход — ❌.",
        "ttt_player_won": "Крестики-нолики\nВы победили!",
        "ttt_computer_won": "Крестики-нолики\nКомпьютер победил.",
        "ttt_draw": "Крестики-нолики\nНичья!",
        "ttt_new_game": "Новая игра",
        "ttt_not_your_game": "Эта игра принадлежит другому пользователю.",
        "ttt_invalid_move": "Этот ход недоступен. Используйте актуальную игровую клавиатуру.",
        "rps_start": "Камень, ножницы, бумага\nВыберите свой ход:",
        "rps_rock": "Камень",
        "rps_scissors": "Ножницы",
        "rps_paper": "Бумага",
        "rps_new_game": "Новая игра",
        "rps_result": "Раунд {round}\nВы: {player}. Бот: {computer}.\n{result}",
        "rps_win": "Вы победили!",
        "rps_loss": "Вы проиграли.",
        "rps_draw": "Ничья!",
        "rps_not_your_game": "Эта игра принадлежит другому пользователю.",
        "rps_difficulty_invalid": "В конфиге указана неверная сложность игры. Укажите число от 0 до 1.",
    },
    "en": {
        "welcome_choose_church": "Welcome! Please choose your church.",
        "start": "Hello! The bot is running. Choose a menu item or send /help.",
        "choose_action": "Choose a menu item.",
        "church_selected": "You selected: {church}",
        "lotm_menu_greeting": "Otherworlder, thank you for your service.",
        "lotm_menu_get_task": "Get a mission",
        "lotm_menu_contribution": "My contribution points",
        "lotm_menu_character": "Character",
        "task_warning": "Otherworlder, are you sure? This mission is quite dangerous.",
        "task_proceed": "Proceed",
        "task_back": "Back",
        "task_started": "You have accepted the mission.",
        "task_returned": "Returned to the menu.",
        "task_button_forbidden": "This button belongs to another user.",
        "help": (
            "Available commands:\n"
            "/start — start the bot\n"
            "/help — show help\n"
            "/settings — settings\n"
            "/menu — open the menu\n"
            "/tictactoe — play tic-tac-toe\n"
            "/rps — play rock, paper, scissors\n"
            "/setdifficulty — configure game difficulty (admin)\n"
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
        "difficulty_usage": "Send a number from 0 to 1, for example: 0.7.",
        "difficulty_choose_game": "Choose a game to configure its difficulty:",
        "difficulty_tictactoe": "Tic-tac-toe — {difficulty}",
        "difficulty_tictactoe_name": "Tic-tac-toe",
        "difficulty_rps": "Rock, Paper, Scissors — {difficulty}",
        "difficulty_rps_name": "Rock, Paper, Scissors",
        "difficulty_enter_value": (
            "Current difficulty for {game}: {difficulty}.\n"
            "Send a new value from 0 to 1, or /cancel to abort."
        ),
        "difficulty_cancelled": "Difficulty change cancelled.",
        "difficulty_updated": "Difficulty for {game} set to {difficulty}.",
        "ttt_your_turn": "Tic-tac-toe\nYour turn — ❌.",
        "ttt_player_won": "Tic-tac-toe\nYou won!",
        "ttt_computer_won": "Tic-tac-toe\nThe computer won.",
        "ttt_draw": "Tic-tac-toe\nIt's a draw!",
        "ttt_new_game": "New game",
        "ttt_not_your_game": "This game belongs to another user.",
        "ttt_invalid_move": "That move is unavailable. Use the current game keyboard.",
        "rps_start": "Rock, Paper, Scissors\nChoose your move:",
        "rps_rock": "Rock",
        "rps_scissors": "Scissors",
        "rps_paper": "Paper",
        "rps_new_game": "New game",
        "rps_result": "Round {round}\nYou: {player}. Bot: {computer}.\n{result}",
        "rps_win": "You won!",
        "rps_loss": "You lost.",
        "rps_draw": "It's a draw!",
        "rps_not_your_game": "This game belongs to another user.",
        "rps_difficulty_invalid": "Invalid game difficulty in config. Enter a number from 0 to 1.",
    },
}


def text(language: Language, key: str) -> str:
    return TEXTS[language][key]


def church_name(language: Language, church: str) -> str:
    return CHURCH_NAMES[language][CHURCHES.index(church)]
