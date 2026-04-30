from constants import BLANCO, NEGRO

class Board:
    def __init__(self):
        self.grid = self._crear_tablero_inicial()
        self.castling_rights = {'k': False, 'r_a1': False, 'r_h1': False, 'K': False, 'R_A8': False, 'R_H8': False}

    def _crear_tablero_inicial(self):
        return [
            ['r', 'n', 'b', 'q', 'k', 'b', 'n', 'r'],
            ['p', 'p', 'p', 'p', 'p', 'p', 'p', 'p'],
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
            ['P', 'P', 'P', 'P', 'P', 'P', 'P', 'P'],
            ['R', 'N', 'B', 'Q', 'K', 'B', 'N', 'R']
        ]

    def get_color(self, ficha):
        if ficha == ' ': return None
        return NEGRO if ficha.islower() else BLANCO

    def make_move(self, move):
        (c_o, f_o), (c_d, f_d) = move
        ficha = self.grid[f_o][c_o]
        captura = self.grid[f_d][c_d]
        memo = {
            'move': move, 
            'captured': captura, 
            'piece': ficha, 
            'old_castling': self.castling_rights.copy()
        }

        # Lógica de Enroque (si el rey se mueve 2 espacios)
        if ficha.lower() == 'k' and abs(c_d - c_o) == 2:
            if c_d > c_o: # Corto
                self.grid[f_o][5], self.grid[f_o][7] = self.grid[f_o][7], ' '
            else: # Largo
                self.grid[f_o][3], self.grid[f_o][0] = self.grid[f_o][0], ' '

        # Mover pieza
        self.grid[f_d][c_d] = ficha
        self.grid[f_o][c_o] = ' '

        # Promoción automática a Reina
        if ficha.lower() == 'p' and (f_d == 0 or f_d == 7):
            self.grid[f_d][c_d] = 'q' if ficha.islower() else 'Q'

        self._update_castling_rights(ficha, c_o, f_o)
        return memo

    def undo_move(self, memo):
        (c_o, f_o), (c_d, f_d) = memo['move']
        self.grid[f_o][c_o] = memo['piece']
        self.grid[f_d][c_d] = memo['captured']
        self.castling_rights = memo['old_castling']
        
        if memo['piece'].lower() == 'k' and abs(c_d - c_o) == 2:
            if c_d > c_o:
                self.grid[f_o][7], self.grid[f_o][5] = self.grid[f_o][5], ' '
            else:
                self.grid[f_o][0], self.grid[f_o][3] = self.grid[f_o][3], ' '

    def _update_castling_rights(self, ficha, c, f):
        if ficha == 'k': self.castling_rights['k'] = True
        elif ficha == 'K': self.castling_rights['K'] = True
        elif ficha == 'r':
            if c == 0 and f == 0: self.castling_rights['r_a1'] = True
            elif c == 7 and f == 0: self.castling_rights['r_h1'] = True
        elif ficha == 'R':
            if c == 0 and f == 7: self.castling_rights['R_A8'] = True
            elif c == 7 and f == 7: self.castling_rights['R_H8'] = True

    def get_legal_moves(self, color):
        moves = []
        for f in range(8):
            for c in range(8):
                ficha = self.grid[f][c]
                if ficha != ' ' and self.get_color(ficha) == color:
                    for df in range(8):
                        for dc in range(8):
                            move = ((c, f), (dc, df))
                            if self.is_valid_move(move, color):
                                moves.append(move)
        return moves

    def is_valid_move(self, move, color):
        (c_o, f_o), (c_d, f_d) = move
        ficha = self.grid[f_o][c_o]
        objetivo = self.grid[f_d][c_d]
        color_pieza = self.get_color(ficha)

        if (c_o, f_o) == (c_d, f_d): return False
        if self.get_color(objetivo) == color: return False
        if color_pieza != color: return False

        if not self._rule_check((c_o, f_o), (c_d, f_d), ficha, color):
            return False

        # Verificar si el movimiento deja al rey en jaque
        memo = self.make_move(move)
        en_jaque = self.is_in_check(color)
        self.undo_move(memo)
        
        return not en_jaque

    def _rule_check(self, origen, destino, ficha, color):
        (c_o, f_o), (c_d, f_d) = origen, destino
        objetivo = self.grid[f_d][c_d]
        dx, dy = abs(c_d - c_o), abs(f_d - f_o)
        tipo = ficha.lower()
        es_valido = False

        if tipo == 'p':
            dir = 1 if color == NEGRO else -1
            if c_o == c_d: # Avance
                if f_d == f_o + dir and objetivo == ' ': es_valido = True
                elif f_o == (1 if color == NEGRO else 6) and f_d == f_o + 2*dir and objetivo == ' ' and self.grid[f_o + dir][c_o] == ' ':
                    es_valido = True
            elif dx == 1 and f_d == f_o + dir and objetivo != ' ': # Captura
                es_valido = True
        elif tipo == 'n':
            # El caballo SIEMPRE debe cumplir la proporción 2:1 o 1:2
            es_valido = (dx == 2 and dy == 1) or (dx == 1 and dy == 2)
        elif tipo == 'b':
            es_valido = (dx == dy) and self._check_path((origen, destino), True, False)
        elif tipo == 'r':
            es_valido = (dx == 0 or dy == 0) and self._check_path((origen, destino), False, True)
        elif tipo == 'q':
            es_valido = self._check_path((origen, destino), True, True)
        elif tipo == 'k':
            es_valido = dx <= 1 and dy <= 1
        
        return es_valido

    def _check_path(self, move, diag, orthogonal):
        (c_o, f_o), (c_d, f_d) = move
        dx, dy = c_d - c_o, f_d - f_o
        if diag and abs(dx) == abs(dy):
            step_c = 1 if dx > 0 else -1
            step_f = 1 if dy > 0 else -1
            curr_c, curr_f = c_o + step_c, f_o + step_f
            while curr_c != c_d:
                if self.grid[curr_f][curr_c] != ' ': return False
                curr_c += step_c
                curr_f += step_f
            return True
        if orthogonal and (dx == 0 or dy == 0):
            step_c = 0 if dx == 0 else (1 if dx > 0 else -1)
            step_f = 0 if dy == 0 else (1 if dy > 0 else -1)
            curr_c, curr_f = c_o + step_c, f_o + step_f
            while curr_c != c_d or curr_f != f_d:
                if curr_c == c_d and curr_f == f_d: break
                if self.grid[curr_f][curr_c] != ' ': return False
                curr_c += step_c
                curr_f += step_f
            return True
        return False

    def is_in_check(self, color):
        rey_char = 'k' if color == NEGRO else 'K'
        pos_rey = None
        for f in range(8):
            for c in range(8):
                if self.grid[f][c] == rey_char:
                    pos_rey = (c, f)
                    break
        if not pos_rey: return False
        
        oponente = BLANCO if color == NEGRO else NEGRO
        # Verificar ataques simplificados (amenazas directas)
        for f in range(8):
            for c in range(8):
                ficha = self.grid[f][c]
                if ficha != ' ' and self.get_color(ficha) == oponente:
                    if self._pseudo_valido((c, f), pos_rey):
                        return True
        return False

    def _pseudo_valido(self, origen, destino):
        ficha = self.grid[origen[1]][origen[0]]
        color = self.get_color(ficha)
        return self._rule_check(origen, destino, ficha, color)