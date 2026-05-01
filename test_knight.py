from logic import Board
from constants import BLANCO, NEGRO

def test_knight_movement():
    board = Board()
    # Mover el caballo de blancas (G1) a F3
    # G1 es (6, 7), F3 es (5, 5)
    # F3 es una casilla válida para el caballo desde G1
    move = ((6, 7), (5, 5))
    
    # El movimiento es legal si el caballo salta
    # Para probar el salto, pongamos una pieza en F2
    board.grid[6][5] = 'P' # F2
    
    is_valid = board.is_valid_move(move, BLANCO)
    print(f"¿Es válido el salto del caballo de G1 a F3 con pieza en F2? {is_valid}")
    
    # Otro movimiento: B1 a C3
    move2 = ((1, 7), (2, 5))
    is_valid2 = board.is_valid_move(move2, BLANCO)
    print(f"¿Es válido el movimiento del caballo de B1 a C3? {is_valid2}")

if __name__ == "__main__":
    test_knight_movement()
