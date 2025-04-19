import sys
import re
import random
from typing import List, Dict, Optional, Tuple, Any

PAWN = 1
KNIGHT = 2
BISHOP = 3
ROOK = 4
QUEEN = 5
KING = 6

WHITE = True
BLACK = False

SQUARES = list(range(64))

PIECE_VALUES = {PAWN: 100, KNIGHT: 320, BISHOP: 330, ROOK: 500, QUEEN: 900, KING: 20000}

FEN_PIECE_MAP = {
    "p": (PAWN, BLACK),
    "n": (KNIGHT, BLACK),
    "b": (BISHOP, BLACK),
    "r": (ROOK, BLACK),
    "q": (QUEEN, BLACK),
    "k": (KING, BLACK),
    "P": (PAWN, WHITE),
    "N": (KNIGHT, WHITE),
    "B": (BISHOP, WHITE),
    "R": (ROOK, WHITE),
    "Q": (QUEEN, WHITE),
    "K": (KING, WHITE),
}
SQUARE_NAMES = [
    'a1', 'b1', 'c1', 'd1', 'e1', 'f1', 'g1', 'h1',
    'a2', 'b2', 'c2', 'd2', 'e2', 'f2', 'g2', 'h2',
    'a3', 'b3', 'c3', 'd3', 'e3', 'f3', 'g3', 'h3',
    'a4', 'b4', 'c4', 'd4', 'e4', 'f4', 'g4', 'h4',
    'a5', 'b5', 'c5', 'd5', 'e5', 'f5', 'g5', 'h5',
    'a6', 'b6', 'c6', 'd6', 'e6', 'f6', 'g6', 'h6',
    'a7', 'b7', 'c7', 'd7', 'e7', 'f7', 'g7', 'h7',
    'a8', 'b8', 'c8', 'd8', 'e8', 'f8', 'g8', 'h8',
]

class Piece:
    def __init__(self, piece_type, color):
        self.piece_type = piece_type
        self.color = color

    def __str__(self):
        piece_chars = {
            PAWN: "P",
            KNIGHT: "N",
            BISHOP: "B",
            ROOK: "R",
            QUEEN: "Q",
            KING: "K",
        }
        char = piece_chars.get(self.piece_type, "?")
        return char.lower() if not self.color else char


class Board:
    def __init__(self, fen):
        self.fen = fen
        self.pieces = {}
        self.turn = WHITE
        self._parse_fen(fen)

    def _parse_fen(self, fen: str):
        """Parse FEN string and set up the board."""
        try:
            parts = fen.split()
            if len(parts) < 1:
                print(f"Invalid FEN: {fen} - No parts found")
                return

            ranks = parts[0].split("/")
            if len(ranks) != 8:
                print(f"Invalid FEN: {fen} - Expected 8 ranks, got {len(ranks)}")
                return

            for rank_idx, rank in enumerate(ranks):
                file_idx = 0
                for char in rank:
                    if char.isdigit():
                        file_idx += int(char)
                    else:

                        if char in FEN_PIECE_MAP:
                            piece_type, color = FEN_PIECE_MAP[char]
                            square = (7 - rank_idx) * 8 + file_idx
                            self.pieces[square] = Piece(piece_type, color)
                        else:
                            print(f"Invalid piece character: {char}")
                        file_idx += 1

                if file_idx != 8:
                    print(
                        f"Invalid FEN: {fen}- Rank {rank_idx} has {file_idx} files, expected 8"
                    )
                    return

            if len(parts) > 1:
                turn_char = parts[1].lower()
                if turn_char == "b":
                    self.turn = BLACK
                elif turn_char == "w":
                    self.turn = WHITE
                else:
                    print(f"Invalid turn character in FEN: {turn_char}")
        except Exception as e:
            print(f"Error parsing FEN: {e}")

    def piece_at(self, square):
        return self.pieces.get(square)

    def __str__(self):

        result = []
        for rank in range(8):
            row = []
            for file in range(8):
                square = rank * 8 + file
                piece = self.piece_at(square)
                if piece is None:
                    row.append(".")
                else:
                    row.append(str(piece))
            result.append(" ".join(row))
        return "\n".join(result)

    @property
    def legal_moves(self) -> List[str]:

        moves = []

        for square in SQUARES:
            piece = self.piece_at(square)
            if piece is not None and piece.color == self.turn:

                if piece.piece_type == PAWN:
                    # Pawns 1 only
                    direction = -8 if self.turn == WHITE else 8
                    target_square = square + direction
                    if 0 <= target_square < 64 and self.piece_at(target_square) is None:
                        moves.append(
                            f"{SQUARE_NAMES[square]}{SQUARE_NAMES[target_square]}"
                        )

                    # Pawns 2 in front in start
                    if (self.turn == WHITE and 48 <= square <= 55) or (
                        self.turn == BLACK and 8 <= square <= 15
                    ):
                        target_square = square + (direction * 2)
                        if (
                            self.piece_at(target_square) is None
                            and self.piece_at(square + direction) is None
                        ):
                            moves.append(
                                f"{SQUARE_NAMES[square]}{SQUARE_NAMES[target_square]}"
                            )

                    # Pawns attack diagonally
                    for capture_offset in [-9, -7] if self.turn == WHITE else [7, 9]:

                        if (
                            (
                                self.turn == WHITE
                                and square % 8 == 0
                                and capture_offset == -9
                            )
                            or (
                                self.turn == WHITE
                                and square % 8 == 7
                                and capture_offset == -7
                            )
                            or (
                                self.turn == BLACK
                                and square % 8 == 0
                                and capture_offset == 7
                            )
                            or (
                                self.turn == BLACK
                                and square % 8 == 7
                                and capture_offset == 9
                            )
                        ):
                            continue

                        target_square = square + capture_offset
                        if 0 <= target_square < 64:
                            target_piece = self.piece_at(target_square)
                            if (
                                target_piece is not None
                                and target_piece.color != self.turn
                            ):
                                moves.append(
                                    f"{SQUARE_NAMES[square]}{SQUARE_NAMES[target_square]}"
                                )

                elif piece.piece_type == KNIGHT:
                    # Knights can move in L-shapes
                    knight_moves = [
                        square - 17,
                        square - 15,
                        square - 10,
                        square - 6,
                        square + 6,
                        square + 10,
                        square + 15,
                        square + 17,
                    ]
                    for target in knight_moves:
                        if 0 <= target < 64:
                            #  (not off the board)
                            if abs((target % 8) - (square % 8)) <= 2:
                                target_piece = self.piece_at(target)
                                if (
                                    target_piece is None
                                    or target_piece.color != self.turn
                                ):
                                    moves.append(
                                        f"{SQUARE_NAMES[square]}{SQUARE_NAMES[target]}"
                                    )

                elif piece.piece_type == BISHOP:
                    # Bishops can move diagonally
                    for direction in [-9, -7, 7, 9]:
                        if (square % 8 == 0 and direction in [-9, 7]) or (
                            square % 8 == 7 and direction in [-7, 9]
                        ):
                            continue

                        target_square = square + direction
                        while 0 <= target_square < 64:

                            if abs((target_square % 8) - (square % 8)) > 1:
                                break

                            target_piece = self.piece_at(target_square)
                            if target_piece is None:
                                moves.append(
                                    f"{SQUARE_NAMES[square]}{SQUARE_NAMES[target_square]}"
                                )
                            elif target_piece.color != self.turn:
                                moves.append(
                                    f"{SQUARE_NAMES[square]}{SQUARE_NAMES[target_square]}"
                                )
                                break
                            else:
                                break

                            target_square += direction

                elif piece.piece_type == ROOK:
                    # Rooks can move horizontally and vertically
                    for direction in [-8, -1, 1, 8]:

                        if (square % 8 == 0 and direction == -1) or (
                            square % 8 == 7 and direction == 1
                        ):
                            continue

                        target_square = square + direction
                        while 0 <= target_square < 64:
                            # Check if we've wrapped around the board
                            if direction in [-1, 1] and (target_square // 8) != (
                                square // 8
                            ):
                                break

                            target_piece = self.piece_at(target_square)
                            if target_piece is None:
                                moves.append(
                                    f"{SQUARE_NAMES[square]}{SQUARE_NAMES[target_square]}"
                                )
                            elif target_piece.color != self.turn:
                                moves.append(
                                    f"{SQUARE_NAMES[square]}{SQUARE_NAMES[target_square]}"
                                )
                                break
                            else:
                                break

                            target_square += direction

                elif piece.piece_type == QUEEN:

                    for direction in [-9, -7, 7, 9]:

                        if (square % 8 == 0 and direction in [-9, 7]) or (
                            square % 8 == 7 and direction in [-7, 9]
                        ):
                            continue

                        target_square = square + direction
                        while 0 <= target_square < 64:
                            #    Off the board
                            if abs((target_square % 8) - (square % 8)) > 1:
                                break

                            target_piece = self.piece_at(target_square)
                            if target_piece is None:
                                moves.append(
                                    f"{SQUARE_NAMES[square]}{SQUARE_NAMES[target_square]}"
                                )
                            elif target_piece.color != self.turn:
                                moves.append(
                                    f"{SQUARE_NAMES[square]}{SQUARE_NAMES[target_square]}"
                                )
                                break
                            else:
                                break

                            target_square += direction

                    for direction in [-8, -1, 1, 8]:
                        # off the board
                        if (square % 8 == 0 and direction == -1) or (
                            square % 8 == 7 and direction == 1
                        ):
                            continue

                        target_square = square + direction
                        while 0 <= target_square < 64:
                            # Out of the board
                            if direction in [-1, 1] and (target_square // 8) != (
                                square // 8
                            ):
                                break

                            target_piece = self.piece_at(target_square)
                            if target_piece is None:
                                moves.append(
                                    f"{SQUARE_NAMES[square]}{SQUARE_NAMES[target_square]}"
                                )
                            elif target_piece.color != self.turn:
                                moves.append(
                                    f"{SQUARE_NAMES[square]}{SQUARE_NAMES[target_square]}"
                                )
                                break
                            else:
                                break

                            target_square += direction

                elif piece.piece_type == KING:
                    # king 1-1 in every direct
                    king_moves = [
                        square - 9,
                        square - 8,
                        square - 7,
                        square - 1,
                        square + 1,
                        square + 7,
                        square + 8,
                        square + 9,
                    ]
                    for target in king_moves:
                        if 0 <= target < 64:
                            if abs((target % 8) - (square % 8)) <= 1:
                                target_piece = self.piece_at(target)
                                if (
                                    target_piece is None
                                    or target_piece.color != self.turn
                                ):
                                    moves.append(
                                        f"{SQUARE_NAMES[square]}{SQUARE_NAMES[target]}"
                                    )

        if not moves:
            if self.turn == WHITE:
                return ["e2e4"]
            else:
                return ["e7e5"]

        return random.sample(moves, min(5, len(moves)))


class BlunderDetector:
    def __init__(self):
        pass

    def analyze_position(self, fen, depth=20):

        try:
            board = Board(fen)

            score = self._material_evaluation(board)

            legal_moves = list(board.legal_moves)
            best_move = None
            best_score = float("-inf")

            if legal_moves:
                for move in legal_moves:
                    temp_board = Board(fen)
                    from_square = SQUARE_NAMES.index(move[:2])
                    to_square = SQUARE_NAMES.index(move[2:])

                    piece = temp_board.piece_at(from_square)
                    if piece:

                        temp_board.pieces.pop(from_square, None)
                        temp_board.pieces[to_square] = piece

                        move_score = self._material_evaluation(temp_board)

                        mobility = len(temp_board.legal_moves)
                        move_score += mobility * 5

                        # Center control  bonus
                        center_squares = [27, 28, 35, 36]  # e4, d4, e5, d5
                        if to_square in center_squares:
                            move_score += 30

                        is_attacked = False
                        for square in SQUARES:
                            attacker = temp_board.piece_at(square)
                            # captured piece
                            if attacker and attacker.color != piece.color:
                                if (
                                    abs((square % 8) - (to_square % 8)) <= 1
                                    and abs((square // 8) - (to_square // 8)) <= 1
                                ):
                                    is_attacked = True
                                    break

                        if is_attacked:
                            move_score -= 50

                        # Update best move
                        if move_score > best_score:
                            best_score = move_score
                            best_move = move

                # If no good move was found, use the first legal move
                if best_move is None and legal_moves:
                    best_move = legal_moves[0]

                print(f"Legal moves found: {legal_moves}")
                print(f"Selected best move: {best_move}")
            else:
                print("No legal moves found!")

            return score, best_move
        except Exception as e:
            print(f"Error in analyze_position: {e}")
            return 0.0, None

    def _material_evaluation(self, board):

        score = 0
        for square in SQUARES:
            piece = board.piece_at(square)
            if piece is not None:
                value = PIECE_VALUES.get(piece.piece_type, 0)
                if piece.color == WHITE:
                    score += value
                else:
                    score -= value
        # Add bonuses for  center
        center_squares = [27, 28, 35, 36]  # e4, d4, e5, d5
        for square in center_squares:
            piece = board.piece_at(square)
            if piece is not None:
                if piece.color == WHITE:
                    score += 10
                else:
                    score -= 10

        for square in SQUARES:
            piece = board.piece_at(square)
            if piece is not None:
                # a temporary board for legal moves detec
                temp_board = Board(board.fen)
                temp_board.turn = piece.color
                mobility = len(temp_board.legal_moves)

                if piece.color == WHITE:
                    score += mobility * 5
                else:
                    score -= mobility * 5

        for square in SQUARES:
            piece = board.piece_at(square)
            if piece is not None and piece.piece_type == KING:

                if 16 <= square <= 47:  # c3-f6
                    if piece.color == WHITE:
                        score -= 50
                    else:
                        score += 50

        for file in range(8):
            pawn_count = 0
            for rank in range(8):
                square = rank * 8 + file
                piece = board.piece_at(square)
                if piece is not None and piece.piece_type == PAWN:
                    pawn_count += 1

            if pawn_count > 1:
                if board.turn == WHITE:
                    score -= 30 * (pawn_count - 1)
                else:
                    score += 30 * (pawn_count - 1)

        return score

    def detect_blunder(self, fen_before, fen_after, depth=20):

        try:
            eval_before, best_move = self.analyze_position(fen_before, depth)
            print(f"Best move found: {best_move}")

            eval_after, _ = self.analyze_position(fen_after, depth)

            eval_diff = eval_before - eval_after

            # Blunder score calculator
            BLUNDER_THRESHOLD = 50
            MISTAKE_THRESHOLD = 25
            SMALL_MISTAKE_THRESHOLD = 10

            # blunder message print
            if eval_diff > BLUNDER_THRESHOLD:
                print(f"BLUNDER detected! Difference: {eval_diff} centipawns")
                return (
                    True,
                    f"Blunder! Best move was {best_move}. You lost {eval_diff/100:.1f} in evaluation.",
                )

            elif eval_diff > MISTAKE_THRESHOLD:
                print(f"MISTAKE detected! Difference: {eval_diff} centipawns")
                return (
                    True,
                    f"Mistake! Best move was {best_move}. You lost {eval_diff/100:.1f} in evaluation.",
                )

            elif eval_diff > SMALL_MISTAKE_THRESHOLD:
                print(f"Small mistake detected: {eval_diff} centipawns")
                return (
                    True,
                    f"Small mistake. Best move was {best_move}. You lost {eval_diff/100:.1f} in evaluation.",
                )
            else:

                if eval_diff < 0:
                    print(f"Good move! Improvement: {-eval_diff} centipawns")
                    return (
                        False,
                        f"Good move! You gained {-eval_diff/100:.1f} in evaluation.",
                    )
                else:
                    return False, "No significant mistake detected."

        except Exception as e:
            # Life is hard
            return False, "Move analyzed..."


CHESS_AVAILABLE = True
