import random
from constants import VALOR_PIEZAS, PST, BLANCO, NEGRO

class ChessEngine:
    def __init__(self, board, difficulty="Intermedio"):
        self.board = board
        if difficulty == "Fácil":
            self.depth = 2
        elif difficulty == "Difícil":
            self.depth = 6
        else:
            self.depth = 4

    def get_best_move(self):
        best_move = None
        best_value = -99999
        alpha = -100000
        beta = 100000
        
        moves = self.board.get_legal_moves(BLANCO)
        # Ordenamiento de jugadas (Heurística de captura)
        moves.sort(key=lambda m: self._score_move(m), reverse=True)

        for move in moves:
            memo = self.board.make_move(move)
            board_value = self._minimax(self.depth - 1, alpha, beta, False)
            self.board.undo_move(memo)
            if board_value > best_value:
                best_value = board_value
                best_move = move
            alpha = max(alpha, best_value)
        return best_move

    def _score_move(self, move):
        # Priorizar capturas para optimizar poda alfa-beta
        target = self.board.grid[move[1][1]][move[1][0]]
        if target != ' ':
            return VALOR_PIEZAS[target.lower()]
        return 0

    def _minimax(self, depth, alpha, beta, is_max):
        if depth == 0:
            return self.evaluate_board()

        color = BLANCO if is_max else NEGRO
        moves = self.board.get_legal_moves(color)

        if is_max:
            value = -100000
            for move in moves:
                memo = self.board.make_move(move)
                value = max(value, self._minimax(depth - 1, alpha, beta, False))
                self.board.undo_move(memo)
                alpha = max(alpha, value)
                if beta <= alpha: break
            return value
        else:
            value = 100000
            for move in moves:
                memo = self.board.make_move(move)
                value = min(value, self._minimax(depth - 1, alpha, beta, True))
                self.board.undo_move(memo)
                beta = min(beta, value)
                if beta <= alpha: break
            return value

    def evaluate_board(self):
        total = 0
        for f in range(8):
            for c in range(8):
                ficha = self.board.grid[f][c]
                if ficha != ' ':
                    tipo = ficha.upper()
                    val = VALOR_PIEZAS[ficha.lower()]
                    
                    # Aplicar Piece-Square Tables para posicionamiento estratégico
                    if tipo in PST:
                        fila_pst = f if ficha.isupper() else 7 - f
                        val += PST[tipo][fila_pst][c]

                    total += val if ficha.isupper() else -val
        return total