from django.urls import path

from .views import chess_home, chess_puzzle

urlpatterns = [
    path("",                       chess_home  , name="chess_home"  ),
    path("puzzle/<int:puzzle_id>", chess_puzzle, name="chess_puzzle"),
]
