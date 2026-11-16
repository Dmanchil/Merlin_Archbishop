from handlers.admin import router as admin_router
from handlers.difficulty import router as difficulty_router
from handlers.main import router as main_router
from handlers.rps import router as rps_router
from handlers.tictactoe import router as tictactoe_router

__all__ = [
    "admin_router",
    "difficulty_router",
    "main_router",
    "rps_router",
    "tictactoe_router",
]
