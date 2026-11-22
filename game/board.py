''' Representación del tablero. 

Tablero real: Conoce los barcos.

Tablero de observaciones: Conoce los disparos y sus resultados.


 '''

from enum import Enum


class CellState(Enum):
    UNKNOWN = 0
    MISS = 1
    HIT = 2


class Board:
    
   # Tablero de observaciones (para un jugador)

    def __init__(self, n):
        self.n = n

        self.shots = [
            [CellState.UNKNOWN for _ in range(n)]
            for _ in range(n)
        ]

    def is_valid(self, cell):
        r, c = cell
        return 0 <= r < self.n and 0 <= c < self.n

    def is_available(self, cell):
        r, c = cell

        return (
            self.is_valid(cell)
            and self.shots[r][c] == CellState.UNKNOWN
        )

    def record_shot(self, cell, hit):
        if not self.is_available(cell):
            raise ValueError("Invalid or repeated shot")

        r, c = cell

        self.shots[r][c] = (
            CellState.HIT if hit else CellState.MISS
        )

    def get_unknown_cells(self):
        return [
            (r, c)
            for r in range(self.n)
            for c in range(self.n)
            if self.shots[r][c] == CellState.UNKNOWN
        ]
        
    def __str__(self):

        symbols = {
            CellState.UNKNOWN: "?",
            CellState.MISS: "O",
            CellState.HIT: "X"
        }

        rows = []

        for row in self.shots:
            rows.append(
                " ".join(symbols[cell] for cell in row)
            )

        return "\n".join(rows)
