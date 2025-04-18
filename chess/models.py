from django.db import models

class Game(models.Model):
    board = models.CharField(max_length=100)
    date_created = models.DateTimeField("date created", auto_now_add=True)
    moves = models.TextField(null=True, blank=True)
    info = models.TextField(max_length=255, default="info")
    to_move = models.CharField(max_length=5, default="white")


class BoardPuzzle(models.Model):
    board = models.CharField(max_length=100)
    date_created = models.DateTimeField("date created", auto_now_add=True)
    info = models.TextField()


class GamePuzzle(models.Model):
    board = models.CharField(max_length=100)
    date_created = models.DateTimeField("date created", auto_now_add=True)
    solution = models.TextField()
    info = models.TextField()
    to_move = models.CharField(max_length=5, default="white")
