import unittest

from experiments.simulation import (
    fleet_from_configuration,
    run_single_game,
    run_experiment
)

from agents.random_agent import RandomAgent
from agents.maximum_probability_agent import MaximumProbabilityAgent
from game.configurations import generate_configurations
from agents.maximum_information_gain_agent import (
    MaximumInformationGainAgent
)


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

    
    def test_experiment_with_multiple_agents(self):

        results = run_experiment(
            n=3,
            fleet_lengths=[2],
            agent_classes=[
                RandomAgent,
                MaximumProbabilityAgent
            ],
            num_games=5,
            seed=42
        )

        self.assertEqual(len(results["RandomAgent"]), 5)

        self.assertEqual(
            len(results["MaximumProbabilityAgent"]),
            5
        )

        for agent_name, agent_results in results.items():

            if agent_name == "_metadata":
                continue

            for game in agent_results:
                self.assertTrue(game["won"])

        
        
    def test_fleets_independent_of_agent_list(self):

        agents_a = [
            RandomAgent,
            MaximumProbabilityAgent
        ]

        agents_b = [
            RandomAgent,
            MaximumProbabilityAgent,
            MaximumInformationGainAgent
        ]

        results_a = run_experiment(
            n=3,
            fleet_lengths=[2],
            agent_classes=agents_a,
            num_games=10,
            seed=42
        )

        results_b = run_experiment(
            n=3,
            fleet_lengths=[2],
            agent_classes=agents_b,
            num_games=10,
            seed=42
        )

        for agent_class in agents_a:

            name = agent_class.__name__

            configurations_a = [
                result["configuration"]
                for result in results_a[name]
            ]

            configurations_b = [
                result["configuration"]
                for result in results_b[name]
            ]

            self.assertEqual(
                configurations_a,
                configurations_b
            )


    def test_agent_results_independent_of_order(self):

        agents_a = [
            RandomAgent,
            MaximumProbabilityAgent
        ]

        agents_b = [
            MaximumProbabilityAgent,
            RandomAgent
        ]

        results_a = run_experiment(
            n=3,
            fleet_lengths=[2],
            agent_classes=agents_a,
            num_games=10,
            seed=42
        )

        results_b = run_experiment(
            n=3,
            fleet_lengths=[2],
            agent_classes=agents_b,
            num_games=10,
            seed=42
        )

        for agent_class in agents_a:

            name = agent_class.__name__

            shots_a = [
                result["shots"]
                for result in results_a[name]
            ]

            shots_b = [
                result["shots"]
                for result in results_b[name]
            ]

            self.assertEqual(shots_a, shots_b)


    def test_agents_share_same_fleet_per_game(self):

        agents = [
            RandomAgent,
            MaximumProbabilityAgent,
            MaximumInformationGainAgent
        ]

        results = run_experiment(
            n=3,
            fleet_lengths=[2],
            agent_classes=agents,
            num_games=10,
            seed=42
        )

        for game_id in range(10):

            configurations = [
                results[agent.__name__][game_id]["configuration"]
                for agent in agents
            ]

            self.assertTrue(
                all(
                    configuration == configurations[0]
                    for configuration in configurations
                )
            )


if __name__ == "__main__":
    unittest.main()
