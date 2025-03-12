#!/usr/bin/python3

#--------------_HELPER_FUNCTIONS_-----------------------#
def rrun(op, np, nosign=False):
    if nosign: return (abs(np[0] - op[0]), abs(np[1] - op[1]))
    else:      return (    np[0] - op[0] ,     np[1] - op[1])

def np0(n):
    if   n < 0: return -1
    elif n > 0: return  1
    else:       return  0

def tupadd(t1, t2):
    return tuple(t1[x] + t2[x] for x in range(0, len(t1)))

#------------------------------------------------------------------------------------------#
#------------------------------------------------------------------------------------------#
#------------------------------------------------------------------------------------------#
#------------------------------------------------------------------------------------------#
class Game(object):
    default_board = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR"

    def __init__(self, game_info=None, moves_arr=[], board_str=None, to_move='white'):
        self.board_array    = self.arr_from(board_str if board_str else self.default_board)
        self.moves_arr      = moves_arr
        self.game_info      = game_info
        self.to_move        = to_move

#--------------_STATIC_METHODS_-------------------------#
    @staticmethod
    def piece_factory(chp):
        dt = {'k': King, 'q': Queen, 'b': Bishop, 'n': Knight, 'r': Rook, 'p': Pawn, '-': Empty}
        return dt[chp.lower()]('white' if (chp.islower()) else 'black')

    @staticmethod
    def alpha_translate(pos):
        move_dict = {'abcdefgh'[x]: x for x in range(0, 8) }
        return (int(pos[1]) - 1), move_dict[pos[0].lower()]

    @staticmethod
    def tuple_translate(pos):
        move_dict = {x: 'abcdefgh'[x] for x in range(0, 8) }
        return move_dict[pos[1]] + str(pos[0] + 1)

#--------------_CLASS_METHODS_--------------------------#
    @classmethod
    def arr_from(cls, from_string):
        new_arr = []
        for i in '123456789':
            from_string = from_string.replace(i, "-"*int(i))
        return [[Game.piece_factory(x) for x in y] for y in from_string.split("/")]

#--------------_METHODS_--------------------------------#
    def reset(self):
        self.board_array = self.arr_from(self.default_board)
        self.moves_arr = []
        self.to_move = 'white'

    def get_piece(self, pos, alpha=False):
        if alpha:
            return self.get_piece(self.alpha_translate(pos))
        return self.board_array[pos[0]][pos[1]]

    def move_piece(self, op, np, alpha=False):
        if alpha:
            return self.move_piece(self.alpha_translate(op), self.alpha_translate(np))
        else:
            if not self.valid_move(op, np):
                return False
            self.board_array[np[0]][np[1]] = self.get_piece(op)
            self.board_array[op[0]][op[1]] = Empty('empty')
            self.moves_arr.append(self.tuple_translate(op) + self.tuple_translate(np))
            self.to_move = 'white' if self.to_move == 'black' else 'black'
            return True

    def valid_move(self, op, np):
        piece       = self.get_piece(op)
        take_piece  = self.get_piece(np)
        return all([(type(piece) != Empty and piece.color == self.to_move),
                    (self.vldm(       piece, take_piece, op, np )),
                    (self.check_intersect( op, np ))])

    def vldm(self, piece, take_piece, op, np):
        return piece.valid_move(op, np) \
           and (type(piece) != Pawn or self.pawn_validate(piece, take_piece, op, np))

    def check_intersect(self, op, np):
        piece       = self.get_piece(op)
        take_piece  = self.get_piece(np)
        if type(piece) != Knight:
            a      = rrun(op, np)
            o0, o1 = np0(a[0]) , np0(a[1])
            t0, t1 = op[0], op[1]
            while True:
                t0 += o0; t1 += o1
                if t0 == np[0] and t1 == np[1]:
                    break
                elif type(self.get_piece((t0, t1))) != Empty:
                    return False
        return piece.color != take_piece.color


    def pawn_validate(self, piece, take_piece, op, np):
        a = rrun(op, np, nosign=True)
        if a[0] == 1:
            pass
        elif a[0] == 2:
            return type(take_piece) == Empty \
               and op[0] == (1 if piece.color == 'white' else 6)
        else:
            return False

    def string_from(self):
        pass
    
    def is_check(self):
        pass

    def is_checkmate(self):
        pass

#--------------_SPECIAL_--------------------------------#

    def __str__(self):
        return "\n".join(["".join([str(x) for x in y]) for y in self.board_array][::-1])

    #def board_from_arr

#------------------------------------------------------------------------------------------#
#------------------------------------------------------------------------------------------#
#------------------------------------------------------------------------------------------#
#------------------------------------------------------------------------------------------#

class Piece(object):
    rep='*'

    def __init__(self, color):
        self.color = color

    @staticmethod
    def verify_vh(op, np):
        return (op[0] == np[0]) or (op[1] == np[1])

    @staticmethod
    def verify_diag(op, np):
        return abs(op[0] - np[0]) == abs(op[1] - np[1])

    def __repr__(self):
        return self.rep if self.color == 'white' else self.rep.upper()

    def __str__(self):
        return self.__repr__()

#------------------PIECES-----------------------------#

class King(Piece):
    rep='k'
    def valid_move(self, op, np):
        a = rrun(op, np, nosign=True)
        return a[0] <= 1 and a[1] <= 1

class Queen(Piece):
    rep='q'
    def valid_move(self, op, np):
        return super.verify_diag(op, np) or super.verify_vh(op, np)

class Bishop(Piece):
    rep='b'
    def valid_move(self, op, np):
        return super.verify_diag(op, np)

class Knight(Piece):
    rep='n'
    def valid_move(self, op, np):
        a = rrun(op, np, nosign=True)
        return 2 in a and 1 in a

class Rook(Piece):
    rep='r'
    def valid_move(self, op, np):
        return super.verify_vh(op, np)

class Pawn(Piece):
    # Pawn move validation is handled specifically by 'Game'.
    rep='p'
    def valid_move(self, op, np):
        a = rrun(op, np, nosign=True)
        return (self.color == 'black' and a[0] < 0) \
            or (self.color == 'white' and a[0] > 0)


class Empty(Piece):
    rep='-'
    def __init__(self, color):
        self.color = 'empty'

    def valid_move(self, op, np):
        return False

#------------------QUICK-TESTING----------------------#
if __name__ == "__main__":
    moves1 = [ ('e2', 'e4'),
               ('e7', 'e5'),
               ('e2', 'e4') ]
    a = Game()
    for i in moves1:
        print("\n\n\n\n")
        print(a.to_move)
        print(str(a))
        a.move_piece(*i, alpha=True)
    #print(a.check_intersect(  (0, 0), (0, 5)  ))
    #print(a.check_intersect(  (0, 1), (2, 2)  ))
    #print(a.check_intersect(  (0, 0), (0, 1)  ))
    #print(a.check_intersect(  (0, 0), (1, 0)  ))
    #print(a.check_intersect(  (0, 2), (3, 4)  ))
    #print(str(a))
    #print(a.get_piece('h8', alpha=True))
    #print(a.check_intersect((0, 0), (0, 5)))

