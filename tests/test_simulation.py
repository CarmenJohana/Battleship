import unittest

from experiments.simulation import (
    fleet_from_configuration,
    run_single_game,
    run_experiment
)

from agents.random_agent import RandomAgent

from game.configurations import generate_configurations


class TestSimulation(unittest.TestCase):

    def setUp(self):

        self.n = 3
        self.fleet_lengths = [2]

        self.configurations = generate_configurations(
            self.n,
            self.fleet_lengths
        )

    def test_fleet_reconstruction(self):

        configuration = self.configurations[0]

        fleet = fleet_from_configuration(
            configuration,
            self.fleet_lengths
        )

        self.assertEqual(len(fleet.ships), 1)
        self.assertEqual(fleet.ships[0].length, 2)

    def test_reconstructed_fleets_are_independent(self):

        configuration = self.configurations[0]

        fleet_1 = fleet_from_configuration(
            configuration,
            self.fleet_lengths
        )

        fleet_2 = fleet_from_configuration(
            configuration,
            self.fleet_lengths
        )

        fleet_1.ships[0].receive_hit(
            fleet_1.ships[0].cells[0]
        )

        self.assertEqual(fleet_1.ships[0].hits.__len__(), 1)
        self.assertEqual(fleet_2.ships[0].hits.__len__(), 0)

    def test_single_game(self):

        result = run_single_game(
            self.n,
            self.configurations[0],
            self.fleet_lengths,
            RandomAgent
        )

        self.assertTrue(result["won"])
        self.assertGreater(result["shots"], 0)

    def test_experiment_number_of_games(self):

        results = run_experiment(
            self.n,
            self.fleet_lengths,
            [RandomAgent],
            num_games=5,
            seed=42
        )

        self.assertEqual(
            len(results["RandomAgent"]),
            5
        )

    def test_invalid_number_of_games(self):

        with self.assertRaises(ValueError):

            run_experiment(
                self.n,
                self.fleet_lengths,
                [RandomAgent],
                num_games=0
            )

    def test_agents_share_configurations(self):

        results = run_experiment(
            self.n,
            self.fleet_lengths,
            [RandomAgent],
            num_games=3,
            seed=42
        )

        self.assertEqual(
            [r["game_id"] for r in results["RandomAgent"]],
            [0, 1, 2]
        )
        
        
    
    def test_experiment_is_reproducible(self):

        results_1 = run_experiment(
            n=self.n,
            fleet_lengths=self.fleet_lengths,
            agent_classes=[RandomAgent],
            num_games=10,
            seed=42
        )

        results_2 = run_experiment(
            n=self.n,
            fleet_lengths=self.fleet_lengths,
            agent_classes=[RandomAgent],
            num_games=10,
            seed=42
        )

        self.assertEqual(
            results_1["RandomAgent"],
            results_2["RandomAgent"]
        )

    def test_different_seeds_can_produce_different_results(self):

        results_1 = run_experiment(
            n=self.n,
            fleet_lengths=self.fleet_lengths,
            agent_classes=[RandomAgent],
            num_games=10,
            seed=42
        )

        results_2 = run_experiment(
            n=self.n,
            fleet_lengths=self.fleet_lengths,
            agent_classes=[RandomAgent],
            num_games=10,
            seed=123
        )

        self.assertNotEqual(
            results_1["RandomAgent"],
            results_2["RandomAgent"]
        )



if __name__ == "__main__":
    unittest.main()
