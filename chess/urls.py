from django.urls import path

from .views import chess_game, chess_home, chess_memory_puzzle

urlpatterns = [
    path("", chess_home, name="chess_home"),
    path("game/<int:game_id>", chess_game, name="chess_game"),
    path("memorypuzzle/", chess_memory_puzzle, name="chess_memory_puzzle"),
]
