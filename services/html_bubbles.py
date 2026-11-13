import zlib
from decimal import Decimal, InvalidOperation
from pathlib import Path

from aiogram.methods.base import TelegramMethod
from aiogram.types import Message

MAX_WIDGET_HTML_BYTES = 32 * 1024
MAX_WIDGET_COMPRESSED_BYTES = 4 * 1024
TICTACTOE_DIFFICULTY_CONFIG_KEY = "tictactoe_difficulty"
DEFAULT_TICTACTOE_DIFFICULTY = "0.5"
TICTACTOE_HTML_PATH = (
    Path(__file__).resolve().parent.parent
    / "games"
    / "1 tictactoe"
    / "index.html"
)


class SendWidget(TelegramMethod[Message]):
    __returning__ = Message
    __api_method__ = "sendWidget"

    chat_id: int
    html: str


def normalize_tictactoe_difficulty(value: str | float) -> str:
    try:
        difficulty = Decimal(str(value))
    except InvalidOperation as error:
        raise ValueError("Сложность должна быть числом от 0 до 1") from error

    if not difficulty.is_finite() or not Decimal("0") <= difficulty <= Decimal("1"):
        raise ValueError("Сложность должна быть числом от 0 до 1")
    return format(difficulty.normalize(), "f")


def load_tictactoe_html(
    difficulty: str | float = DEFAULT_TICTACTOE_DIFFICULTY,
) -> str:
    normalized_difficulty = normalize_tictactoe_difficulty(difficulty)

    html = TICTACTOE_HTML_PATH.read_text(encoding="utf-8")
    html = html.replace(
        "const DIFFICULTY=__TICTACTOE_DIFFICULTY__",
        f"const DIFFICULTY={normalized_difficulty}",
    )
    html_bytes = html.encode("utf-8")
    compressed_bytes = zlib.compress(html_bytes, level=9)

    if len(html_bytes) > MAX_WIDGET_HTML_BYTES:
        raise ValueError("HTMLBubble превышает лимит 32 КБ")
    if len(compressed_bytes) > MAX_WIDGET_COMPRESSED_BYTES:
        raise ValueError("HTMLBubble превышает лимит 4 КБ после сжатия")

    return html
