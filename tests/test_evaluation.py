
import unittest

from experiments.evaluation import (
    evaluate_results,
    compare_agents_paired
)


class TestEvaluation(unittest.TestCase):

    def setUp(self):

        self.results = {
            "AgentA": [
                {
                    "game_id": 0,
                    "shots": 10,
                    "configuration": (((0, 0), (0, 1)),)
                },
                {
                    "game_id": 1,
                    "shots": 12,
                    "configuration": (((1, 0), (1, 1)),)
                },
                {
                    "game_id": 2,
                    "shots": 8,
                    "configuration": (((2, 0), (2, 1)),)
                }
            ],

            "AgentB": [
                {
                    "game_id": 0,
                    "shots": 15,
                    "configuration": (((0, 0), (0, 1)),)
                },
                {
                    "game_id": 1,
                    "shots": 10,
                    "configuration": (((1, 0), (1, 1)),)
                },
                {
                    "game_id": 2,
                    "shots": 8,
                    "configuration": (((2, 0), (2, 1)),)
                }
            ],

            "_metadata": {
                "seed": 42,
                "n": 5,
                "fleet_lengths": [2],
                "num_games": 3
            }
        }

    def test_evaluate_results(self):

        evaluation = evaluate_results(self.results)

        self.assertEqual(
            evaluation["AgentA"]["num_games"],
            3
        )

        self.assertAlmostEqual(
            evaluation["AgentA"]["mean"],
            10.0
        )

        self.assertEqual(
            evaluation["AgentA"]["median"],
            10
        )

        self.assertAlmostEqual(
            evaluation["AgentA"]["variance"],
            4.0
        )

        self.assertAlmostEqual(
            evaluation["AgentA"]["std_dev"],
            2.0
        )

    def test_metadata_is_excluded(self):

        evaluation = evaluate_results(self.results)

        self.assertNotIn("_metadata", evaluation)

    def test_paired_mean_difference(self):

        comparison = compare_agents_paired(
            self.results,
            "AgentA",
            "AgentB"
        )

        # Differences: 15-10, 10-12, 8-8
        # Result: [5, -2, 0]
        self.assertAlmostEqual(
            comparison["mean_difference"],
            1.0
        )

    def test_paired_median_difference(self):

        comparison = compare_agents_paired(
            self.results,
            "AgentA",
            "AgentB"
        )

        self.assertEqual(
            comparison["median_difference"],
            0
        )

    def test_paired_wins_and_ties(self):

        comparison = compare_agents_paired(
            self.results,
            "AgentA",
            "AgentB"
        )

        self.assertEqual(comparison["wins_a"], 1)
        self.assertEqual(comparison["wins_b"], 1)
        self.assertEqual(comparison["ties"], 1)

    def test_paired_rates(self):

        comparison = compare_agents_paired(
            self.results,
            "AgentA",
            "AgentB"
        )

        self.assertAlmostEqual(
            comparison["win_rate_a"],
            1 / 3
        )

        self.assertAlmostEqual(
            comparison["win_rate_b"],
            1 / 3
        )

        self.assertAlmostEqual(
            comparison["tie_rate"],
            1 / 3
        )

    def test_games_are_matched_by_id(self):

        reversed_results = {
            "AgentA": self.results["AgentA"],
            "AgentB": list(
                reversed(self.results["AgentB"])
            )
        }

        comparison = compare_agents_paired(
            reversed_results,
            "AgentA",
            "AgentB"
        )

        self.assertAlmostEqual(
            comparison["mean_difference"],
            1.0
        )

    def test_different_configurations_are_rejected(self):

        invalid_results = {
            "AgentA": self.results["AgentA"],
            "AgentB": [
                dict(game)
                for game in self.results["AgentB"]
            ]
        }

        invalid_results["AgentB"][0]["configuration"] = (
            ((4, 4), (4, 3)),
        )

        with self.assertRaises(ValueError):

            compare_agents_paired(
                invalid_results,
                "AgentA",
                "AgentB"
            )

    def test_duplicate_game_ids_are_rejected(self):

        invalid_results = {
            "AgentA": [
                dict(game)
                for game in self.results["AgentA"]
            ],
            "AgentB": self.results["AgentB"]
        }

        invalid_results["AgentA"][1]["game_id"] = 0

        with self.assertRaises(ValueError):

            compare_agents_paired(
                invalid_results,
                "AgentA",
                "AgentB"
            )

    def test_missing_agent_is_rejected(self):

        with self.assertRaises(ValueError):

            compare_agents_paired(
                self.results,
                "AgentA",
                "UnknownAgent"
            )

    def test_empty_paired_results_are_rejected(self):

        empty_results = {
            "AgentA": [],
            "AgentB": []
        }

        with self.assertRaises(ValueError):

            compare_agents_paired(
                empty_results,
                "AgentA",
                "AgentB"
            )


if __name__ == "__main__":
    unittest.main()

