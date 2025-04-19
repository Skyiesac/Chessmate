import sys
import re
from typing import Tuple, Optional

from .chess_wrapper import BlunderDetector, CHESS_AVAILABLE

class ChessBlunderDetector:
    def __init__(self):
        self.blunder_detector = BlunderDetector()
        self.chess_available = CHESS_AVAILABLE
        
    def detect_blunder(self, fen_before: str, fen_after: str) -> Tuple[bool, str]:
        if not self.chess_available:
            return False, "Chess analysis is not available."
            
        try:
            return self.blunder_detector.detect_blunder(fen_before, fen_after)
        except Exception as e:
            print(f"Error in blunder detection: {e}")
            return False, f"Error analyzing move: {str(e)}"
            
    def analyze_position(self, fen: str) -> Tuple[float, Optional[str]]:
        if not self.chess_available:
            return  None
            
        try:
            return self.blunder_detector.analyze_position(fen)
        except Exception as e:
            print(f"Error in position analysis: {e}")
            return None 