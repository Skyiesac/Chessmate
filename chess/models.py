from django.db import models

class Game(models.Model):
    board        = models.CharField(max_length=100)
    date_created = models.DateTimeField("date created", auto_now_add=True)
    moves        = models.TextField()
    info         = models.TextField()
    to_move      = models.CharField(max_length=5, default='white')


