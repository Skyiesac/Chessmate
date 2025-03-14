from django.shortcuts import render
from django.http      import HttpResponse

def chess_home(request):
    return render(request, 'chess_home.html')

def chess_puzzle(request, puzzle_id):
    return render(request, 'chess_puzzle.html', {"puzzle_info": {"HI": "BYE"}})
