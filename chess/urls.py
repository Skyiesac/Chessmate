from django.urls import path

from .views import chess_game, chess_home, chess_news

urlpatterns = [
    path("", chess_home),
    path("game/<int:game_id>", chess_game),
    path("news/", chess_news),
]
