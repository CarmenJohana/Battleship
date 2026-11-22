import unittest

from experiments.evaluation import (
    evaluate_results,
    print_evaluation
)


class TestEvaluation(unittest.TestCase):

    def setUp(self):

        self.results = {
            "AgentA": [
                {"shots": 10},
                {"shots": 20},
                {"shots": 30}
            ],
            "AgentB": [
                {"shots": 15},
                {"shots": 15},
                {"shots": 15}
            ]
        }

    def test_number_of_games(self):

        evaluation = evaluate_results(self.results)

        self.assertEqual(
            evaluation["AgentA"]["num_games"],
            3
        )

    def test_mean(self):

        evaluation = evaluate_results(self.results)

        self.assertEqual(
            evaluation["AgentA"]["mean"],
            20
        )

    def test_median(self):

        evaluation = evaluate_results(self.results)

        self.assertEqual(
            evaluation["AgentA"]["median"],
            20
        )

    def test_variance(self):

        evaluation = evaluate_results(self.results)

        self.assertEqual(
            evaluation["AgentA"]["variance"],
            100
        )

    def test_standard_deviation(self):

        evaluation = evaluate_results(self.results)

        self.assertEqual(
            evaluation["AgentA"]["std_dev"],
            10
        )

    def test_minimum(self):

        evaluation = evaluate_results(self.results)

        self.assertEqual(
            evaluation["AgentA"]["min"],
            10
        )

    def test_maximum(self):

        evaluation = evaluate_results(self.results)

        self.assertEqual(
            evaluation["AgentA"]["max"],
            30
        )

    def test_single_game(self):

        results = {
            "AgentA": [{"shots": 12}]
        }

        evaluation = evaluate_results(results)

        self.assertEqual(
            evaluation["AgentA"]["variance"],
            0.0
        )

        self.assertEqual(
            evaluation["AgentA"]["std_dev"],
            0.0
        )

    def test_empty_results(self):

        with self.assertRaises(ValueError):
            evaluate_results({"AgentA": []})

    def test_print_evaluation(self):

        evaluation = evaluate_results(self.results)

        # Ensure that printing does not raise an exception.
        print_evaluation(evaluation)


if __name__ == "__main__":
    unittest.main()
