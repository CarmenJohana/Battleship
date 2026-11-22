import unittest

from agents.random_agent import RandomAgent
from game.game_engine import ShotResult


class TestRandomAgent(unittest.TestCase):

    def setUp(self):
        self.agent = RandomAgent(3)

    def test_choose_valid_shot(self):

        shot = self.agent.choose_shot()

        self.assertIn(
            shot,
            self.agent.get_available_cells()
        )

    def test_shots_are_not_repeated(self):

        for _ in range(9):

            shot = self.agent.choose_shot()

            self.assertNotIn(shot, self.agent.shots)

            self.agent.observe(shot, ShotResult.MISS)

        self.assertEqual(len(self.agent.shots), 9)

    def test_all_cells_are_available_initially(self):

        self.assertEqual(
            len(self.agent.get_available_cells()),
            9
        )

    def test_no_available_cells(self):

        for row in range(3):
            for col in range(3):
                self.agent.observe(
                    (row, col),
                    ShotResult.MISS
                )

        with self.assertRaises(RuntimeError):
            self.agent.choose_shot()


if __name__ == "__main__":
    unittest.main()
