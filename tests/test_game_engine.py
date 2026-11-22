
import unittest

from game.ship import Ship
from game.fleet import Fleet
from game.board import CellState
from game.game_engine import GameEngine, ShotResult


class TestGameEngine(unittest.TestCase):

    def setUp(self):

        ship = Ship(
            ship_id=1,
            length=2,
            cells=((0, 0), (0, 1))
        )

        fleet = Fleet([ship])

        self.engine = GameEngine(3, fleet)

    def test_miss(self):

        result = self.engine.fire((2, 2))

        self.assertEqual(result, ShotResult.MISS)

    def test_hit(self):

        result = self.engine.fire((0, 0))

        self.assertEqual(result, ShotResult.HIT)

    def test_sink(self):

        self.engine.fire((0, 0))
        result = self.engine.fire((0, 1))

        self.assertEqual(result, ShotResult.SUNK)

    def test_invalid_repeated_shot(self):

        self.engine.fire((2, 2))
        result = self.engine.fire((2, 2))

        self.assertEqual(result, ShotResult.INVALID)

    def test_invalid_out_of_bounds_shot(self):

        result = self.engine.fire((3, 3))

        self.assertEqual(result, ShotResult.INVALID)

    def test_game_over(self):

        self.engine.fire((0, 0))
        self.engine.fire((0, 1))

        self.assertTrue(self.engine.is_over)

    def test_cannot_shoot_after_game_over(self):

        self.engine.fire((0, 0))
        self.engine.fire((0, 1))

        result = self.engine.fire((2, 2))

        self.assertEqual(result, ShotResult.INVALID)

    def test_game_state_returns_observation(self):

        observation = self.engine.get_game_state()

        self.assertEqual(observation.n, 3)
        self.assertEqual(
            len(observation.get_unknown_cells()),
            9
        )

    def test_observation_is_snapshot(self):

        observation = self.engine.get_game_state()
        self.engine.fire((0, 0))

        # The previous observation must remain unchanged.
        self.assertEqual(
            observation.shots[0][0],
            CellState.UNKNOWN
        )


if __name__ == "__main__":
    unittest.main()

