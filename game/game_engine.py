from enum import Enum
from .observation import GameObservation
from .board import Board
from .fleet import Fleet


class ShotResult(Enum):
    MISS = 0
    HIT = 1
    SUNK = 2
    INVALID = 3


class GameEngine:

    def __init__(self, n: int, fleet: Fleet):

        if n <= 0:
            raise ValueError("Board size must be positive.")

        self.n = n
        self.fleet = fleet
        self.board = Board(n)

        self.shots_fired = 0
        self.is_over = False

        # Validate that every ship is inside the board.
        for ship in self.fleet.ships:
            for cell in ship.cells:
                if not self.board.is_valid(cell):
                    raise ValueError(
                        "All ships must be inside the board."
                    )

        # Validate that ships do not overlap.
        occupied = set()

        for ship in self.fleet.ships:
            if not occupied.isdisjoint(ship.cells):
                raise ValueError(
                    "Ships cannot overlap."
                )

            occupied.update(ship.cells)

    def is_valid_shot(
        self,
        cell: tuple[int, int]
    ) -> bool:

        return (
            not self.is_over
            and self.board.is_available(cell)
        )

    def fire(
        self,
        cell: tuple[int, int]
    ) -> ShotResult:

        if not self.is_valid_shot(cell):
            return ShotResult.INVALID

        self.shots_fired += 1

        ship = self.fleet.get_ship_at(cell)

        if ship is None:

            self.board.record_shot(cell, hit=False)

            return ShotResult.MISS

        ship.receive_hit(cell)

        self.board.record_shot(cell, hit=True)

        if ship.is_sunk:
            result = ShotResult.SUNK
        else:
            result = ShotResult.HIT

        if self.has_won():
            self.is_over = True

        return result

    def has_won(self) -> bool:

        return self.fleet.is_sunk

    def get_game_state(self) -> GameObservation:

    	shots_snapshot = tuple(
        	tuple(row)
        	for row in self.board.shots
    	)

    	return GameObservation(
        	n=self.n,
        	shots=shots_snapshot
    	)
