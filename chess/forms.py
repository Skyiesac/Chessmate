#!/usr/bin/python3

from django import forms
from .models import Game

class GameForm(forms.ModelForm):
    game_info = forms.TextField()
