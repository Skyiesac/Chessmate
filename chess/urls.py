from django.urls import path

from .views import chess_home

urlpatterns = [
    path("", chess_home, name="home")
]
