#!/usr/bin/python3

from ChessLogic.Helper    import ind, seti, str_b, visp, pair_add, lmake
from ChessLogic.Helper    import remove_out_of_range, points_on_line, sign
from ChessLogic.ChessBase import ChessGame, vm_list

def test_points_on_line():
    a = points_on_line((3, 3), (0, 6))
    print(a)
    print(str_b(visp((3, 3), a)))

def test_check():
    test_str  = "k-------\n"
    test_str += "pppppppp\n"
    test_str += "--------\n"
    test_str += "--------\n"
    test_str += "--------\n"
    test_str += "-q------\n"
    test_str += "--PP----\n"
    test_str += "-qKB----"
    ############ ABCDEFGH ############
    a = ChessGame(start_string=test_str, to_move='white')
    #print(a.g('a1'))
    #print(a.move('c2b1'))
    print(a.str_board())
    print(a.move('c2b1'))
    print(a.str_board())
    #print('is_check', a.is_check('black'))
    print('is_mate', a.is_mate())
    #print('is_stalemate', a.is_stalemate())
    ##print('a_move', a.move((7, 2), (7, 1)))
    #print(a.str_board())

def test_game():
    a = ChessGame()
    moves = ['e2e4', 'e7e5', 'f1d3', 'a7a6']
    for i in moves:
        print("\n\n")
        print(a.move(i))
        print(a.str_board())

def lineprint():
    print("\n\n\n\n")

if __name__ == "__main__":

    #pos = (3, 3)
    #x = vm_list('k', pos)
    #print(x)
    #print(str_b(visp(pos, x)))
    #print()

    #test_points_on_line()

    #lineprint()

    #test_game()
    
    test_check()
