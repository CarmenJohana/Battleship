import unittest

from agents.maximum_information_gain_agent import (
    MaximumInformationGainAgent
)
from game.game_engine import ShotResult


class TestMaximumInformationGainAgent(unittest.TestCase):

    def setUp(self):
        self.agent = MaximumInformationGainAgent(
            n=3,
            fleet_lengths=[2]
        )

    def test_agent_initializes(self):
        self.assertEqual(self.agent.n, 3)
        self.assertEqual(self.agent.fleet_lengths, [2])

    def test_agent_has_legal_configurations(self):
        self.assertTrue(self.agent.configurations)

    def test_choose_shot_returns_valid_cell(self):
        shot = self.agent.choose_shot()

        row, col = shot

        self.assertTrue(0 <= row < 3)
        self.assertTrue(0 <= col < 3)

    def test_choose_shot_does_not_repeat(self):
        first_shot = self.agent.choose_shot()

        self.agent.observe(
            first_shot,
            ShotResult.MISS
        )

        second_shot = self.agent.choose_shot()

        self.assertNotEqual(first_shot, second_shot)

    def test_agent_uses_only_available_cells(self):
        self.agent.observe((0, 0), ShotResult.MISS)

        shot = self.agent.choose_shot()

        self.assertNotEqual(shot, (0, 0))

    def test_no_available_cells_raises_error(self):
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
