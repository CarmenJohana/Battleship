import unittest
import random

from agents.maximum_probability_agent import MaximumProbabilityAgent
from game.game_engine import ShotResult


class TestMaximumProbabilityAgent(unittest.TestCase):

    def setUp(self):

        self.agent = MaximumProbabilityAgent(
            n=3,
            fleet_lengths=[2],
            rng=random.Random(42)
        )

    def test_agent_initialization(self):

        self.assertEqual(self.agent.n, 3)
        self.assertEqual(self.agent.fleet_lengths, [2])
        self.assertGreater(len(self.agent.configurations), 0)

    def test_choose_shot_returns_valid_cell(self):

        cell = self.agent.choose_shot()

        row, col = cell

        self.assertTrue(0 <= row < 3)
        self.assertTrue(0 <= col < 3)

    def test_choose_shot_does_not_repeat_observed_cells(self):

        previous_shot = (1, 1)

        self.agent.observe(
            previous_shot,
            ShotResult.MISS
        )

        next_shot = self.agent.choose_shot()

        self.assertNotEqual(next_shot, previous_shot)

    def test_agent_uses_observations(self):

        self.agent.observe(
            (0, 0),
            ShotResult.MISS
        )

        compatible = [
            configuration
            for configuration in self.agent.configurations
            if all(
                (0, 0) not in placement
                for placement in configuration
            )
        ]

        self.assertTrue(compatible)

        cell = self.agent.choose_shot()

        self.assertNotEqual(cell, (0, 0))

    def test_agent_finishes_small_game(self):

        from game.fleet_generator import generate_random_fleet
        from game.game_engine import GameEngine
        from game.runner import GameRunner

        fleet = generate_random_fleet(
            3,
            [2],
            rng=random.Random(10)
        )

        engine = GameEngine(3, fleet)

        agent = MaximumProbabilityAgent(
            3,
            [2],
            rng=random.Random(42)
        )

        runner = GameRunner(engine, agent)

        history = runner.run()

        self.assertTrue(engine.has_won())
        self.assertGreater(len(history), 0)

    def test_invalid_fleet_configuration(self):

        with self.assertRaises(ValueError):

            MaximumProbabilityAgent(
                n=2,
                fleet_lengths=[5]
            )


if __name__ == "__main__":
    unittest.main()
