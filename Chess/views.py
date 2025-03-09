from django.shortcuts import render
from django.http      import HttpResponse

def chess_home(request):
    return HttpResponse("Chess Home (HERE).")
