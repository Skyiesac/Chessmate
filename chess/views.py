import json
from django.core import serializers
from django.forms.models import model_to_dict
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from .ChessLogic.ChessBase import ChessGame
from .models import Game


def chess_home(request):
    if request.method == "POST":
        game = Game.objects.create()
        return redirect("chess_game", game_id=game.pk)
    else:
        games = Game.objects.all()
        return render(request, "chess_home.html", {"games": [x.id for x in games]})


def chess_game(request, game_id):
    game = get_object_or_404(Game, pk=game_id)
    gmoves = game.moves.split(",,") if game.moves and len(game.moves) > 0 else []
    ng = ChessGame(start_string=game.board, moves=gmoves, to_move=game.to_move)

    if request.method == "POST":
        rec_data = json.loads(request.body)
        if "op" not in rec_data or "np" not in rec_data:
            return False
        
        resg = ng.move(
            (int(rec_data["op"][0]), int(rec_data["op"][1])),
            np=(int(rec_data["np"][0]), int(rec_data["np"][1])),
        )
        if resg:
            game.board = ng.str_board()
            game.moves = ",,".join(ng.moves)
            game.to_move = ng.to_move
            game.save()
            result = "valid move"
            
            # Get blunder message if any
            blunder_message = ng.get_last_blunder_message()
        else:
            result = "invalid move"
            blunder_message = None

        report = ng.analyze_moves()
        return JsonResponse(
            {
                "result": result,
                "board": game.board,
                "to_move": game.to_move,
                "info": ng.moves[-1],
                "report": report,
                "blunder_message": blunder_message,
            }
        )
    else:
        return render(
            request,
            "chess_game.html",
            {
                "chess_id": game_id,
                "game": {
                    "info": game.info,
                    "moves": ng.moves,
                    "board": ng.str_board(),
                    "to_move": ng.to_move,
                    "info": ng.moves[-1] if len(ng.moves) >= 1 else "",
                },
            },
        )


def chess_memory_puzzle(request):
    return render(request, "chess_memory_puzzle.html")
