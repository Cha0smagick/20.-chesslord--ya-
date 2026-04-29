from logic import Board
from ai import ChessEngine
from constants import BLANCO, NEGRO

class ChessGame:
    def __init__(self):
        self.board = Board()
        self.engine = ChessEngine(self.board)
        self.turn = NEGRO

    def display(self):
        print("  a b c d e f g h")
        for i, row in enumerate(self.board.grid):
            print(f"{8-i}│ {' '.join(row)} │")

    def play(self):
        while True:
            self.display()
            if self.turn == NEGRO:
                move = self._get_player_move()
            else:
                print("IA pensando...")
                move = self.engine.get_best_move()
            
            if not move: break
            self.board.make_move(move)
            self.turn = BLANCO if self.turn == NEGRO else NEGRO

    def _get_player_move(self):
        # Lógica de input notacion_a_casilla...
        return None # Placeholder

    @staticmethod
    def notacion_a_casilla(notacion):
        pass

if __name__ == "__main__": 
    ChessGame().play()