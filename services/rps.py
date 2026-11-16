import random
from decimal import Decimal, InvalidOperation
from typing import Literal, TypeGuard

Gesture = Literal["rock", "scissors", "paper"]
GESTURES: tuple[Gesture, ...] = ("rock", "scissors", "paper")
RPS_DIFFICULTY_CONFIG_KEY = "rps_difficulty"
DEFAULT_RPS_DIFFICULTY = "0.5"
BEATS: dict[Gesture, Gesture] = {
    "rock": "scissors",
    "scissors": "paper",
    "paper": "rock",
}
BEATEN_BY: dict[Gesture, Gesture] = {
    beaten: gesture for gesture, beaten in BEATS.items()
}


def random_gesture() -> Gesture:
    return random.choice(GESTURES)


def is_gesture(value: str) -> TypeGuard[Gesture]:
    return value in GESTURES


def normalize_rps_difficulty(value: str | float) -> str:
    try:
        difficulty = Decimal(str(value))
    except InvalidOperation as error:
        raise ValueError("Сложность должна быть числом от 0 до 1") from error

    if not difficulty.is_finite() or not Decimal("0") <= difficulty <= Decimal("1"):
        raise ValueError("Сложность должна быть числом от 0 до 1")
    return format(difficulty.normalize(), "f")


def choose_computer_gesture(
    player: Gesture,
    difficulty: str | float,
) -> Gesture:
    normalized_difficulty = float(normalize_rps_difficulty(difficulty))
    if random.random() < normalized_difficulty:
        return BEATEN_BY[player]
    return random.choice(GESTURES)


def get_result(player: Gesture, computer: Gesture) -> Literal["win", "loss", "draw"]:
    if player == computer:
        return "draw"
    return "win" if BEATS[player] == computer else "loss"
