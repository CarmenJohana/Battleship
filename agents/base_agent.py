import random
from abc import ABC, abstractmethod

from game.game_engine import ShotResult


class BaseAgent(ABC):

    def __init__(self, n: int, rng: random.Random | None = None):

        if n <= 0:
            raise ValueError("Board size must be positive.")

        self.n = n

        self.rng = (
            rng if rng is not None
            else random.Random()
        )

        self.observations: dict[
            tuple[int, int], ShotResult
        ] = {}

        self.shots: set[tuple[int, int]] = set()

    def observe(self, cell, result):

        row, col = cell

        if not (0 <= row < self.n and 0 <= col < self.n):
            raise ValueError("Cell is outside the board.")

        if cell in self.shots:
            raise ValueError("Cell has already been observed.")

        if result not in (
            ShotResult.MISS,
            ShotResult.HIT,
            ShotResult.SUNK
        ):
            raise ValueError("Invalid observation result.")

        self.observations[cell] = result
        self.shots.add(cell)

    def get_available_cells(self):

        return [
            (r, c)
            for r in range(self.n)
            for c in range(self.n)
            if (r, c) not in self.shots
        ]

    @abstractmethod
    def choose_shot(self) -> tuple[int, int]:
        pass

