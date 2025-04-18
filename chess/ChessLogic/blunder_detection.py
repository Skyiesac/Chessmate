try:
    import chess
    from chess import Board, SQUARES, PAWN, KNIGHT, BISHOP, ROOK, QUEEN, KING, WHITE
    CHESS_AVAILABLE = True
except ImportError:
    CHESS_AVAILABLE = False
    print("Warning: python-chess module not available")

from typing import Tuple, Optional

class BlunderDetector:
    def __init__(self):
        # No need for external engine
        pass

    def analyze_position(self, fen: str, depth: int = 20) -> Tuple[float, Optional[str]]:
        """
        Analyze a position using python-chess's built-in evaluation.
        Returns (evaluation, best_move) where evaluation is in centipawns.
        """
        if not CHESS_AVAILABLE:
            return 0.0, None
            
        try:
            board = Board(fen)
            
            # Use a simple material counting evaluation
            score = self._material_evaluation(board)
            
            # Get a legal move as the "best move"
            legal_moves = list(board.legal_moves)
            best_move = None
            if legal_moves:
                best_move = board.san(legal_moves[0])
            
            return score, best_move
        except Exception as e:
            print(f"Error analyzing position: {e}")
            return 0.0, None

    def _material_evaluation(self, board) -> float:
        """
        Simple material evaluation function.
        Returns a score in centipawns (positive for white advantage).
        """
        # Material values in centipawns
        piece_values = {
            PAWN: 100,
            KNIGHT: 320,
            BISHOP: 330,
            ROOK: 500,
            QUEEN: 900,
            KING: 20000
        }
        
        score = 0
        for square in SQUARES:
            piece = board.piece_at(square)
            if piece is not None:
                value = piece_values[piece.piece_type]
                if piece.color == WHITE:
                    score += value
                else:
                    score -= value
        
        return score

    def detect_blunder(self, fen_before: str, fen_after: str, depth: int = 20) -> Tuple[bool, str]:
        """
        Detect if a move was a blunder by comparing evaluations before and after the move.
        Returns (is_blunder, message)
        """
        if not CHESS_AVAILABLE:
            return False, "Chess module not available"
            
        try:
            # Analyze position before the move
            eval_before, best_move = self.analyze_position(fen_before, depth)
            
            # Analyze position after the move
            eval_after, _ = self.analyze_position(fen_after, depth)
            
            # Calculate evaluation difference
            eval_diff = eval_before - eval_after
            
            # Define blunder thresholds (in centipawns)
            BLUNDER_THRESHOLD = 300  # 3 pawns
            MISTAKE_THRESHOLD = 150  # 1.5 pawns
            
            if eval_diff > BLUNDER_THRESHOLD:
                return True, f"Blunder! Best move was {best_move}. You lost {eval_diff/100:.1f} pawns in evaluation."
            elif eval_diff > MISTAKE_THRESHOLD:
                return True, f"Mistake! Best move was {best_move}. You lost {eval_diff/100:.1f} pawns in evaluation."
            else:
                return False, "No significant mistake detected."
                
        except Exception as e:
            return False, f"Error analyzing position: {e}" 