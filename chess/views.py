from django.shortcuts import render
from django.http      import HttpResponse

def chess_home(request):
    return render(request, 'chess_home.html')
