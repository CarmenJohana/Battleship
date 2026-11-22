from dataclasses import dataclass

from .board import CellState


@dataclass(frozen=True)
class GameObservation:
    n: int
    shots: tuple[tuple[CellState, ...], ...]

    def __post_init__(self):

        if self.n <= 0:
            raise ValueError("Board size must be positive.")

        if len(self.shots) != self.n:
            raise ValueError("Observation must have n rows.")

        if any(len(row) != self.n for row in self.shots):
            raise ValueError("Observation must have n columns.")

    def get_unknown_cells(self) -> list[tuple[int, int]]:

        return [
            (r, c)
            for r in range(self.n)
            for c in range(self.n)
            if self.shots[r][c] == CellState.UNKNOWN
        ]
