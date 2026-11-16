import random
from decimal import Decimal, InvalidOperation

BOARD_SIZE = 9
EMPTY_CELL = "_"
PLAYER_MARK = "X"
COMPUTER_MARK = "O"
TICTACTOE_DIFFICULTY_CONFIG_KEY = "tictactoe_difficulty"
DEFAULT_TICTACTOE_DIFFICULTY = "0.5"
WINNING_LINES = (
    (0, 1, 2),
    (3, 4, 5),
    (6, 7, 8),
    (0, 3, 6),
    (1, 4, 7),
    (2, 5, 8),
    (0, 4, 8),
    (2, 4, 6),
)


def normalize_tictactoe_difficulty(value: str | float) -> str:
    try:
        difficulty = Decimal(str(value))
    except InvalidOperation as error:
        raise ValueError("Сложность должна быть числом от 0 до 1") from error

    if not difficulty.is_finite() or not Decimal("0") <= difficulty <= Decimal("1"):
        raise ValueError("Сложность должна быть числом от 0 до 1")
    return format(difficulty.normalize(), "f")


def new_board() -> str:
    return EMPTY_CELL * BOARD_SIZE


def is_valid_board(board: str) -> bool:
    if len(board) != BOARD_SIZE or any(
        cell not in {EMPTY_CELL, PLAYER_MARK, COMPUTER_MARK} for cell in board
    ):
        return False
    return board.count(PLAYER_MARK) == board.count(COMPUTER_MARK)


def get_winner(board: str) -> str | None:
    for line in WINNING_LINES:
        mark = board[line[0]]
        if mark != EMPTY_CELL and all(board[index] == mark for index in line[1:]):
            return mark
    return None


def is_finished(board: str) -> bool:
    return get_winner(board) is not None or EMPTY_CELL not in board


def choose_computer_move(
    board: str,
    difficulty: str | float,
    random_value: float | None = None,
) -> int:
    normalized_difficulty = float(normalize_tictactoe_difficulty(difficulty))
    available = [index for index, cell in enumerate(board) if cell == EMPTY_CELL]
    if not available:
        raise ValueError("На поле нет свободных клеток")

    roll = random.random() if random_value is None else random_value
    if roll < normalized_difficulty:
        return _best_move(board, available)
    return random.choice(available)


def _best_move(board: str, available: list[int]) -> int:
    best_score = float("-inf")
    best_moves: list[int] = []
    for move in available:
        state = list(board)
        state[move] = COMPUTER_MARK
        score = _minimax(state, maximizing=False)
        if score > best_score:
            best_score = score
            best_moves = [move]
        elif score == best_score:
            best_moves.append(move)
    return random.choice(best_moves)


def _minimax(board: list[str], maximizing: bool) -> int:
    winner = get_winner("".join(board))
    if winner == COMPUTER_MARK:
        return 10
    if winner == PLAYER_MARK:
        return -10
    if EMPTY_CELL not in board:
        return 0

    mark = COMPUTER_MARK if maximizing else PLAYER_MARK
    scores = []
    for index, cell in enumerate(board):
        if cell == EMPTY_CELL:
            board[index] = mark
            scores.append(_minimax(board, not maximizing))
            board[index] = EMPTY_CELL
    return max(scores) if maximizing else min(scores)
