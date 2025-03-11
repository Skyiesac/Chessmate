from django.db import models

class Game(models.Model):
    board = models.CharField(max_length=200)
    date_created = models.DateTimeField("date created")

