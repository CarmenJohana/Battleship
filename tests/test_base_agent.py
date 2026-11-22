
import unittest

from agents.base_agent import BaseAgent
from game.game_engine import ShotResult


class DummyAgent(BaseAgent):

    def choose_shot(self):
        return (0, 0)


class TestBaseAgent(unittest.TestCase):

    def setUp(self):
        self.agent = DummyAgent(3)

    def test_initial_observations(self):

        self.assertEqual(self.agent.observations, {})
        self.assertEqual(self.agent.shots, set())

    def test_initial_available_cells(self):

        self.assertEqual(
            len(self.agent.get_available_cells()),
            9
        )

    def test_observe_miss(self):

        self.agent.observe((0, 0), ShotResult.MISS)

        self.assertEqual(
            self.agent.observations[(0, 0)],
            ShotResult.MISS
        )

        self.assertIn((0, 0), self.agent.shots)

    def test_observe_hit(self):

        self.agent.observe((1, 1), ShotResult.HIT)

        self.assertEqual(
            self.agent.observations[(1, 1)],
            ShotResult.HIT
        )

    def test_observe_sunk(self):

        self.agent.observe((2, 2), ShotResult.SUNK)

        self.assertEqual(
            self.agent.observations[(2, 2)],
            ShotResult.SUNK
        )

    def test_available_cells_after_shot(self):

        self.agent.observe((0, 0), ShotResult.MISS)

        self.assertEqual(
            len(self.agent.get_available_cells()),
            8
        )

    def test_cannot_observe_repeated_cell(self):

        self.agent.observe((0, 0), ShotResult.MISS)

        with self.assertRaises(ValueError):
            self.agent.observe((0, 0), ShotResult.HIT)

    def test_cannot_observe_out_of_bounds_cell(self):

        with self.assertRaises(ValueError):
            self.agent.observe((3, 3), ShotResult.MISS)

    def test_cannot_observe_invalid_result(self):

        with self.assertRaises(ValueError):
            self.agent.observe((0, 0), ShotResult.INVALID)

    def test_abstract_agent_cannot_be_instantiated(self):

        with self.assertRaises(TypeError):
            BaseAgent(3)


if __name__ == "__main__":
    unittest.main()
