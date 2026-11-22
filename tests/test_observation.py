import unittest

from game.board import Board, CellState
from game.observation import GameObservation


class TestGameObservation(unittest.TestCase):

    def test_unknown_cells(self):

        board = Board(2)
        board.record_shot((0, 0), hit=True)

        observation = GameObservation(
            n=2,
            shots=tuple(tuple(row) for row in board.shots)
        )

        self.assertEqual(
            observation.get_unknown_cells(),
            [(0, 1), (1, 0), (1, 1)]
        )

    def test_observation_is_immutable(self):

        observation = GameObservation(
            n=2,
            shots=(
                (CellState.UNKNOWN, CellState.UNKNOWN),
                (CellState.UNKNOWN, CellState.UNKNOWN)
            )
        )

        with self.assertRaises(AttributeError):
            observation.n = 3

        with self.assertRaises(TypeError):
            observation.shots[0][0] = CellState.HIT

    def test_invalid_observation_dimensions(self):

        with self.assertRaises(ValueError):
            GameObservation(
                n=2,
                shots=((CellState.UNKNOWN,),)
            )


if __name__ == "__main__":
    unittest.main()
