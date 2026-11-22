import unittest

from game.ship import Ship
from game.fleet import Fleet
from game.game_engine import GameEngine, ShotResult
from game.runner import GameRunner

from agents.random_agent import RandomAgent


class TestGameRunner(unittest.TestCase):

    def setUp(self):

        ship = Ship(
            ship_id=1,
            length=2,
            cells=((0, 0), (0, 1))
        )

        fleet = Fleet([ship])

        self.engine = GameEngine(3, fleet)
        self.agent = RandomAgent(3)

        self.runner = GameRunner(
            self.engine,
            self.agent
        )

    def test_game_finishes(self):

        history = self.runner.run()

        self.assertTrue(self.engine.is_over)
        self.assertTrue(self.engine.has_won())

    def test_history_matches_number_of_shots(self):

        history = self.runner.run()

        self.assertEqual(
            len(history),
            self.engine.shots_fired
        )

    def test_agent_observes_all_shots(self):

        self.runner.run()

        self.assertEqual(
            len(self.agent.observations),
            self.engine.shots_fired
        )

    def test_no_repeated_shots(self):

        history = self.runner.run()

        cells = [cell for cell, result in history]

        self.assertEqual(
            len(cells),
            len(set(cells))
        )

    def test_last_shot_sinks_fleet(self):

        history = self.runner.run()

        self.assertEqual(
            history[-1][1],
            ShotResult.SUNK
        )

    def test_different_board_sizes_are_rejected(self):

        agent = RandomAgent(4)

        with self.assertRaises(ValueError):
            GameRunner(self.engine, agent)


if __name__ == "__main__":
    unittest.main()
