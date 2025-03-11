#!/usr/bin/python3


def rrun(op, np):
    return (op[0] - np[0], op[1] - np[1])

#------------------GAME-------------------------------#
class Game(object):
    default_board = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR"

    def validate_move(self, op, np):
        pass

    def __init__(self, game_info=None, moves_arr=None, board_str=None, to_play='white'):
        self.board_array    = self.arr_from(board_str if board_str else self.default_board)
        self.moves_arr      = moves_arr
        self.game_info      = game_info
        self.to_play        = to_play

    @staticmethod
    def piece_factory(chp):
        dt = {'k': King, 'q': Queen, 'b': Bishop, 'n': Knight, 'r': Rook, 'p': Pawn, '-': Empty}
        lc = chp.lower()
        if lc in dt: return dt[lc]('white' if (chp == lc) else 'black')
        else:        raise ValueError("'chp' needs to be char: 'k', 'q', 'n', 'r', or 'p' (or equivalent uppercase).")

    @classmethod
    def arr_from(cls, from_string):
        new_arr = []
        for i in '123456789':
            from_string = from_string.replace(i, "-"*int(i))
        return [[Game.piece_factory(x) for x in y] for y in from_string.split("/")]

    def get_piece(pos):
        return self.board_array[pos[0]][pos[1]]

    def move_piece(op, np):
        if not self.valid_move(op, np):
            return False
        self.board_array[np[0]][np[1]] = self.get_piece(op)
        self.board_array[op[0]][op[1]] = self.get_piece(op)
        return True

    def valid_move(op, np):
        piece       = self.get_piece(op)
        take_piece  = self.get_piece(np)
        return all([(type(piece) != Empty),
                    (type(piece) == Pawn   or self.valid_move(op, np)),
                    (type(piece) == Knight or not self.intersects(op, np)),
                    (piece.color != take_piece.color)])

    def handle_pawn(op, np):
        pass

    def intersects(op, np):
        a       = rrun(op, np)
        temp    = list(op)
        add_1   = a[0] // a[1] if a[0] != 0 else 0
        add_2   = 1            if a[1] != 0 else 0
        while temp[0] < np[0] and temp[1] < np[1]:
            temp[0] += add_1; temp[1] += add_2
            if type(self.get_piece(temp)) != Empty:
                return True
        return False


    @classmethod
    def string_from(cls, board_arr):
        pass
    
    def is_check(self):
        pass

    def is_checkmate(self):
        pass

    def __str__(self):
        return "\n".join(["".join([str(x) for x in y]) for y in self.board_array][::-1])

    #def board_from_arr

#------------------ABSTRACT---------------------------#

class Piece(object):
    valid_colors = ['white', 'black']
    rep='*'

    def __init__(self, color):
        if color not in self.valid_colors:
            raise ValueError("Color must be an element within '" + self.__class__.__name__ + ".valid_colors'")
        else:
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
        a = rrun(op, np)
        return abs(a[0]) <= 1 and abs(a[1]) <= 1

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
        a = rrun(op, np)
        return 2 in a and 1 in a

class Rook(Piece):
    rep='r'
    def valid_move(self, op, np):
        return super.verify_vh(op, np)

class Pawn(Piece):
    # Pawn move validation is handled specifically by 'Game'.
    rep='p'

class Empty(Piece):
    rep='-'

#------------------QUICK-TESTING----------------------#
if __name__ == "__main__":
    a = Game()
    #print(a.board_array)
    print(str(a))

