#!/usr/bin/python3

l = [-7, -6, -5, -4, -3, -2, -1, 1, 2, 3, 4, 5, 6, 7, 8]
KING_MOVES   = [(1, 0), (0, 1), (1, 1), (-1, 0), (0, -1), (-1, -1), (1, -1), (-1, 1)]
KNIGHT_MOVES = [(-1, -2), (1, -2), (-1, 2), (1, 2), (-2, -1), (2, -1), (-2, 1), (2, 1)]
BISHOP_MOVES = []
for i in l: BISHOP_MOVES += [(i, i), (-i, i), (i, -i), (-i, -i) ]
ROOK_MOVES   = [(0, x) for x in l] +  [(x, 0) for x in l]
QUEEN_MOVES  = BISHOP_MOVES + ROOK_MOVES
MOVE_DICT    = {'k': KING_MOVES, 'q': QUEEN_MOVES, 'b': BISHOP_MOVES, 'r': ROOK_MOVES, 'n': KNIGHT_MOVES}

def visp(pos, moves):
    board = [['_' for x in range(0, 8)] for y in range(0, 8)]
    board[pos[0]][pos[1]] = 'x'
    for i in moves:
        board[i[0]][i[1]] = '+'
    return board
def pair_add(p1, p2):
    return (p1[0] + p2[0], p1[1] + p2[1])
def sign(n):
    if   n < 0: return -1
    elif n > 0: return  1
    else:       return  0
def points_on_line(op, np, mint=1):
    a  = (np[0] - op[0], np[1] - op[1])
    x1 = sign(a[0]); x2 = sign(a[1])
    points = []
    for i in range(1, max(abs(a[0]), abs(a[1])) + mint):
        points.append(pair_add(op, (i*x1, i*x2)))
    return points
def average(*args):
    return sum(args) // len(args)
def midpoint(op, np):
    return (average(op[0], np[0]), average(op[1], np[1]))
def vm_list(piece, pos):
    if piece.lower() in MOVE_DICT:
        l = [pair_add(pos, x) for x in MOVE_DICT[piece.lower()]]
        return list(filter(lambda p: p[0] >= 0 and p[1] >= 0 and p[0] <= 7 and p[1] <= 7, l))
    else:
        return []
def read_pgn(str_pgn):
    pass

class ChessGame(object):
    default_board = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR"
    def __init__(self, start_string=None, moves=[], to_move='white'):
        self.board   = self.board_from_string(start_string)
        self.moves   = moves
        self.to_move = to_move
    def move_unpack(self, str_move):
        a = str_move.split(";;")
        return {"board": a[0],
                "op": self.translate(a[1]),
                "np": self.translate(a[2]),
                "info": a[3:]}
    def en_passant(self, op, np):
        if self.g(op).lower() != 'p' or len(self.moves) <= 0: return False
        last = self.move_unpack(self.moves[-1])
        check = 'p' if self.g(op) == 'P' else 'P'
        if self.g(last['np']) == check and abs(last['op'][0] - last['np'][0]) == 2:
            if midpoint(last['op'], last['np']) == np:
                return last['np']
        return False
    def g(self, pos):
        if type(pos) == str: return self.g(self.translate(pos))
        else: return self.board[pos[0]][pos[1]]
    def s(self, pos, g): self.board[pos[0]][pos[1]] = g
    def toggle_move(self): self.to_move = self.oppo()
    def oppo(self): return 'white' if self.to_move == 'black' else 'black'
    def translate(self, l):
        if type(l) == str: return (int(l[1]) - 1), 'abcdefgh'.index(l[0].lower())
        else:              return 'abcdefgh'[l[1]] + str(l[0] + 1)
    def board_from_string(self, from_string=None):
        if from_string == None or from_string == "":
            return self.board_from_string(self.default_board)
        for i in '123456789':
            from_string = from_string.replace(i, "-"*int(i))
        from_string = from_string.replace("\n", "/")
        return [[x for x in y] for y in from_string.split("/")][::-1]
    def reset(self):
        self.board       = self.board_from_string()
        self.moves       = []
        self.to_move     = 'white'
    def str_board(self):
        return "\n".join(["".join([str(x) for x in y]) for y in self.board][::-1])
    def __str__(self):
        return "\n".join(["".join([str(x) for x in y]) for y in self.board][::-1])
    def undo_move(self):
        if len(self.moves) <= 0:
            return False
        else:
            last_move   = self.move_unpack(self.moves.pop())
            self.board  = self.board_from_string(last_move['board'])
            self.toggle_move()
            return last_move
    def king_position(self, color):
        for i in range(0, 8):
            for j in range(0, 8):
                if self.board[i][j] == ('K' if color == 'white' else 'k'):
                    return (i, j)
        return False
    def internal_move(self, op, np, check_inf=True, promote='q'):
        if promote.lower() not in ('q', 'n', 'r', 'b'): return False
        info=[]
        old_board = self.str_board()
        if (enpass := self.en_passant(op, np)):
            info += ['enpass-' + self.translate(enpass)]
            self.s(enpass, '-')
        elif self.g(op).lower() == 'p' and (np[0] == 7 or np[0] == 0):
            info += ['promote-' + promote]
            self.s(op, promote.upper() if self.to_move == 'white' else promote.lower())
        self.s(np, self.g(op))
        self.s(op, '-')
        self.toggle_move()
        if check_inf:
            if   self.is_mate():  info += ['checkmate']
            elif self.is_check(): info += ['check']

        self.moves.append(";;".join([old_board, self.translate(op), self.translate(np), *info]))
        return True
    def puts_check(self, op, np):
        c = 'white' if self.g(op) == self.g(op).upper() else 'black'
        self.internal_move(op, np, check_inf=False)
        is_check = self.is_check(self.oppo())
        self.undo_move()
        return is_check
    def gcolor(self, op):
        f = self.g(op)
        if f == '-':
            return 'empty'
        elif f == f.upper():
            return 'white'
        else:
            return 'black'
    def is_check(self, color=None):
        if color == None: color = self.to_move
        kpos = self.king_position(color)
        if not kpos:
            return True
        else:
            for i in range(0, 8):
                for j in range(0, 8):
                    if self.gcolor((i, j)) not in (color, 'empty'):
                        aj = (i, j)
                        if self.direct_attack(aj, kpos):
                            return True
        return False
    def ccolor(self, p, color):
        if color == 'white': return p == p.upper()
        else:                return p == p.lower()
    def direct_attack(self, op, np):
        piece = self.g(op).lower()
        if piece == 'p':
            if not self.valid_pawn_move(op, np):
                return False
        elif np not in vm_list(self.g(op), op):
            return False
        if piece != 'n':
            a  = (np[0] - op[0], np[1] - op[1])
            x1 = sign(a[0]); x2 = sign(a[1])
            points = []
            for i in range(1, max(abs(a[0]), abs(a[1]))):
                if self.g(pair_add(op, (i*x1, i*x2))) != '-':
                    return False
        return self.gcolor(op) != self.gcolor(np)
    def valid_move(self, op, np, check_color=True):
        if not check_color or self.ccolor(self.g(op), self.to_move):
            if self.g(op) != '-' and not self.puts_check(op, np):
                if self.direct_attack(op, np):
                    return True
        return False
    def valid_pawn_move(self, op, np):
        correct_direction = -1 if self.g(op) == 'p' else 1
        a = (np[0] - op[0], np[1] - op[1])
        b = (abs(a[0]), abs(a[1]))
        if sign(a[0]) == correct_direction:
            if self.en_passant(op, np):
                return True
            elif b[0] == 1:
                return (b[1] == 1 and self.g(np) != '-') or (b[1] == 0 and self.g(np) == '-')
            elif b[0] == 2:
                return (op[0] == 1 and self.g(np) == '-') or (op[0] == 6 and self.g(np) == '-')
        return False
    def move(self, op, np=None, promote='q'):
        if np == None:
            return self.move(self.translate(op[0:2]), self.translate(op[2:]), promote=promote)
        else:
            return self.valid_move(op, np) and self.internal_move(op, np, promote=promote)
    def is_mate(self):
        if not self.king_position(self.to_move):
            return True
        elif self.is_check(self.to_move) and not self.any_valid():
            return True
        else:
            return False
    def is_stalemate(self):
        return not self.is_check(self.to_move) and not self.any_valid()
    def any_valid(self):
        for ia in range(0, 8):
            for ja in range(0, 8):
                if self.gcolor((ia, ja)) == self.to_move:
                    for kb in range(0, 8):
                        for lb in range(0, 8):
                            if self.valid_move((ia, ja), (kb, lb)):
                                return True
        return False

