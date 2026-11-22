import unittest

from game.board import Board, CellState


class TestBoard(unittest.TestCase):

    def setUp(self):
        self.board = Board(5)

    def test_initial_state(self):
        self.assertEqual(len(self.board.get_unknown_cells()), 25)

    def test_valid_coordinates(self):
        self.assertTrue(self.board.is_valid((0, 0)))
        self.assertTrue(self.board.is_valid((4, 4)))
        self.assertFalse(self.board.is_valid((5, 5)))

    def test_record_miss(self):
        self.board.record_shot((1, 1), hit=False)

        self.assertEqual(
            self.board.shots[1][1],
            CellState.MISS
        )

    def test_record_hit(self):
        self.board.record_shot((2, 3), hit=True)

        self.assertEqual(
            self.board.shots[2][3],
            CellState.HIT
        )

    def test_repeated_shot(self):
        self.board.record_shot((1, 1), hit=True)

        with self.assertRaises(ValueError):
            self.board.record_shot((1, 1), hit=False)


if __name__ == "__main__":
    unittest.main()
