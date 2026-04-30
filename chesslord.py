from logic import Board
from ai import ChessEngine
from constants import BLANCO, NEGRO

class ChessGame:
    def __init__(self):
        self.board = Board()
        self.engine = ChessEngine(self.board)
        self.turn = NEGRO

    def display(self):
        print("\n    a b c d e f g h")
        print("  +-----------------+")
        for i, row in enumerate(self.board.grid):
            print(f"{8-i} | {' '.join(row)} | {8-i}")
        print("  +-----------------+")
        print("    a b c d e f g h\n")

    def play(self):
        print("¡Bienvenido a ChessLord!")
        print("Juegas con NEGRAS (minúsculas). La IA es BLANCAS (MAYÚSCULAS).")
        while True:
            self.display()
            if self.board.is_in_check(self.turn):
                print(f"⚠️ ¡El rey {self.turn} está en JAQUE!")

            if self.turn == NEGRO:
                move = self._get_player_move()
            else:
                print("🤖 IA pensando...")
                move = self.engine.get_best_move()
            
            if not move:
                print(f"Fin de la partida. Gana {'NEGRO' if self.turn == BLANCO else 'BLANCO'}")
                break

            self.board.make_move(move)
            self.turn = BLANCO if self.turn == NEGRO else NEGRO

    def _get_player_move(self):
        while True:
            entrada = input(f"Tu turno ({self.turn}) - Ingresa movimiento (ej: e7e5) o 'salir': ").lower().strip()
            if entrada in ['salir', 'exit', 'quit']:
                return None
            
            try:
                if len(entrada) == 4:
                    origen = self.notacion_a_casilla(entrada[:2])
                    destino = self.notacion_a_casilla(entrada[2:])
                    move = (origen, destino)
                    if self.board.is_valid_move(move, self.turn):
                        return move
                print("❌ Movimiento ilegal o formato incorrecto.")
            except Exception:
                print("❌ Error de formato. Usa algo como 'e7e5'.")

    @staticmethod
    def notacion_a_casilla(notacion):
        col = ord(notacion[0]) - ord('a')
        fila = 8 - int(notacion[1])
        return (col, fila)

if __name__ == "__main__": 
    ChessGame().play()