#!/usr/bin/python3

#--------------_HELPER_FUNCTIONS_-----------------------#
def rrun(op, np, nosign=False):
    if nosign: return (abs(np[0] - op[0]), abs(np[1] - op[1]))
    else:      return (    np[0] - op[0] ,     np[1] - op[1])

def np0(n):
    if   n < 0: return -1
    elif n > 0: return  1
    else:       return  0

def pair_add(t1, t2):
    return (t1[0] + t2[0], t1[1] + t2[1])

def pair_average(t1, t2):
    return ((t1[0] + t2[0]) // 2, (t1[1] + t2[1]) // 2)

def tupadd(t1, t2):
    return tuple(t1[x] + t2[x] for x in range(0, len(t1)))

#------------------------------------------------------------------------------------------#
#------------------------------------------------------------------------------------------#
#------------------------------------------------------------------------------------------#
#------------------------------------------------------------------------------------------#
class Game(object):
    default_board = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR"

    def __init__(self, board_str=None, moves_arr=[], game_info=None, to_move='white'):
        self.board_array    = self.arr_from(board_str if board_str else self.default_board)
        self.moves_arr      = moves_arr
        self.game_info      = game_info
        self.to_move        = to_move

#--------------_STATIC_METHODS_-------------------------#
    @staticmethod
    def piece_factory(chp):
        dt = {'k': King, 'q': Queen, 'b': Bishop, 'n': Knight, 'r': Rook, 'p': Pawn, '-': Empty}
        return dt[chp.lower()]('white' if (chp.isupper()) else 'black')

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
        return [[cls.piece_factory(x) for x in y] for y in from_string.split("/")][::-1]

#--------------_METHODS_--------------------------------#
    def reset(self):
        self.board_array = self.arr_from(self.default_board)
        self.moves_arr   = []
        self.to_move     = 'white'

    def get_piece(self, pos, alpha=False):
        if alpha:
            return self.get_piece(self.alpha_translate(pos))
        return self.board_array[pos[0]][pos[1]]

    def set_piece(self, pos, c, alpha=False):
        if alpha:
            self.get_piece(self.alpha_translate(pos))
        elif type(c) == str:
            self.board_array[pos[0]][pos[1]] = self.piece_factory(c)
        else:
            self.board_array[pos[0]][pos[1]] = c

    # ONLY TO BE USED INTERNALLY, USE `move` FOR EXTERNAL USE
    def internal_move(self, op, np, en_pass=False, promo=False):
        if en_pass:
            self.moves_arr.append((op, np, en_pass, str(self.get_piece(op)), str(self.get_piece(en_pass)), 'en_pass'))
            self.set_piece(en_pass, '-')
        elif promo:
            print("NOT IMPLEMENTED")
            pass
        else:
            self.moves_arr.append((op, np, str(self.get_piece(op)), str(self.get_piece(np))))

        self.set_piece(np, self.get_piece(op))
        self.set_piece(op, '-')
        print('---------', self.to_move)
        self.to_move = 'white' if self.to_move == 'black' else 'black'
        return self.to_move

    def move(self, op, np, move=True, alpha=False):
        if alpha:
            return self.move(self.alpha_translate(op), self.alpha_translate(np), move=move, alpha=False)
        piece       = self.get_piece(op)
        take_piece  = self.get_piece(np)
        vld_move    = piece.valid_move(op, np)
        cint        = self.check_intersect(op, np)
        if piece.color != self.to_move or not cint or not vld_move:
            return False
        elif type(piece) == Pawn:
            en_pass  = self.en_passant(op, np)
            vld_move = (vld_move and (self.pawn_validate(piece, take_piece, op, np) or en_pass))
            return vld_move and (not move or self.internal_move(op, np, en_pass=en_pass))
        else:
            return vld_move and (not move or self.internal_move(op, np))

    def validate_move(self, op, np, alpha=False):
        return self.move(op, np, move=False, alpha=alpha)

    def check_intersect(self, op, np):
        piece       = self.get_piece(op)
        take_piece  = self.get_piece(np)
        if type(piece) != Knight:
            a      = rrun(op, np)
            o0, o1 = np0(a[0]) , np0(a[1])
            t0, t1 = op[0], op[1]
            # Ensure endless loop doesn't occur #
            if op[0] != np[0] and op[1] != np[1] and abs(o0) != abs(o1):
                return False
            while True:
                t0 += o0; t1 += o1
                if t0 == np[0] and t1 == np[1]:
                    break
                elif type(self.get_piece((t0, t1))) != Empty:
                    return False
        return piece.color != take_piece.color


    def pawn_validate(self, piece, take_piece, op, np):
        a = rrun(op, np, nosign=True)
        lt = type(take_piece)
        if   a[0] == 1:
            if type(take_piece) == Empty:
                return a[1] == 0
            else:
                return a[1] == 1 and piece.color != take_piece.color
        elif a[0] == 2:
            return type(take_piece) == Empty and op[0] == (1 if piece.color == 'white' else 6)
        else:
            return False

    def undo_last_move(self):
        if len(self.moves_arr) <= 0:
            return False
        else:
            a = self.moves_arr.pop()
            self.board_array[a[0][0]][a[0][1]] = self.piece_factory(a[2])
            self.board_array[a[1][0]][a[1][1]] = self.piece_factory(a[3])
            self.to_move = 'white' if self.to_move == 'black' else 'black'
            return a

    def en_passant(self, op, np):
        if len(self.moves_arr) >= 1 and type(self.get_piece(op)) == Pawn:
            a = rrun(op, np, nosign=True)
            if a[0] == 1 and a[1] == 1:
                last_move = self.moves_arr[-1]
                mid_point = pair_average(last_move[0], last_move[1])
                if last_move[2].lower() == 'p' and mid_point == np:
                    return last_move[1]
        return False

    def promotion(self, op, np):
        pass

    def string_from(self):
        pass
    
    def put_into_check(self, op, np):
        c = self.to_move
        self.internal_move(op, np)
        return (self.is_check(c) and self.undo_last_move())

    def king_position(self, color):
        for i in range(0, 8):
            for j in range(0, 8):
                if str(self.board[i][j]) == ('K' if color == 'white' else 'k'):
                    return (i, j)
        return False

    def is_check(self, color=None):
        if color == None:
            color = self.to_move
        kpos = self.king_position(color)
        for i in range(0, 8):
            for j in range(0, 8):
                if self.validate_move((i, j), kpos):
                    return True
        return False

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
        return self.rep.upper() if self.color == 'white' else self.rep.lower()

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
        return super().verify_diag(op, np) or super().verify_vh(op, np)

class Bishop(Piece):
    rep='b'
    def valid_move(self, op, np):
        return super().verify_diag(op, np)

class Knight(Piece):
    rep='n'
    def valid_move(self, op, np):
        a = rrun(op, np, nosign=True)
        return 2 in a and 1 in a

class Rook(Piece):
    rep='r'
    def valid_move(self, op, np):
        return super().verify_vh(op, np)

class Pawn(Piece):
    # Pawn move validation is handled specifically by 'Game'.
    rep='p'
    def valid_move(self, op, np):
        a = rrun(op, np)
        return (self.color == 'black' and a[0] < 0) or (self.color == 'white' and a[0] > 0)


class Empty(Piece):
    rep='-'
    def __init__(self, color):
        self.color = 'empty'

    def valid_move(self, op, np):
        return False

#------------------QUICK-TESTING----------------------#
if __name__ == "__main__":
    moves1 = [
              ('e2', 'e4'),
              ('e7', 'e5'),
              ('g1', 'f3'),
              ('b8', 'c6'),
              ('f1', 'b5'),
              ('b7', 'b5'), #False, invalid move
              ('d7', 'd5'),
              ('e4', 'd5'),
              ('c6', 'b4'),
              ('a2', 'a4'),
              #('c7', 'c5'),
              #('d5', 'c6'),
              #('h4', 'b4'),
             ]
    a = Game()
    for i in moves1:
        print("\n\n\n\n")
        a.move(*i, alpha=True)
        print(a.to_move)
        print(str(a))
    #print(a.to_move)
    #print(a.en_passant((4, 3), (5, 2)))


