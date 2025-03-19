import json
from django.forms.models    import model_to_dict
from django.core            import serializers
from django.http            import JsonResponse
from django.shortcuts       import get_object_or_404, render, redirect
from .models                import Game
from .ChessLogic.ChessBase  import ChessGame

def chess_home(request):
    if request.method == "POST":
        game = Game.objects.create()
        return redirect("chess_game", game_id=game.pk)
    else:
        games = Game.objects.all()
        return render(request, 'chess_home.html', {"games": [x.id for x in games]})

def chess_game(request, game_id):
    game = get_object_or_404(Game, pk=game_id)
    gmoves = ",,".split(game.moves) if game.moves and len(game.moves) > 0 else []
    ng = ChessGame(start_string=game.board, moves=gmoves, to_move=game.to_move)
    if (request.method == "POST"):
        rec_data = json.loads(request.body)
        if 'op' not in rec_data or 'np' not in rec_data:
            return False
        print([int(x) for x in rec_data['op']], [int(x) for x in rec_data['np']])
        resg = ng.move([int(x) for x in rec_data['op']], [int(x) for x in rec_data['np']])
        if resg:
            game.board      = ng.str_board()
            game.moves      = ",,".join(ng.moves)
            game.to_move    = ng.to_move
            game.save()
            result = "valid move"
        else:
            result = "invalid move"
        return JsonResponse({"result": result, "board": game.board, "to_move": game.to_move})
    else:
        return render(request, 'chess_game.html', {"game": {"info": game.info, "moves": ng.moves, "board": ng.str_board(), "to_move": ng.to_move}})

def chess_puzzle(request, puzzle_id):
    return render(request, 'chess_puzzle.html', {"puzzle_info": {"HI": "BYE"}})


