import unittest
import unittest
import math

from game.game_engine import ShotResult
from agents.inference import (
    is_compatible,
    filter_compatible_configurations,
    calculate_probability_matrix,
    print_probability_matrix,
    calculate_information_gain
)

class TestInformationGain(unittest.TestCase):

    def test_balanced_partition(self):
        configurations = [
            [((0, 0),)],
            [((0, 0),)],
            [((1, 1),)],
            [((1, 1),)],
        ]

        result = calculate_information_gain(
            configurations, (0, 0)
        )

        self.assertAlmostEqual(result, 1.0)

    def test_unbalanced_partition(self):
        configurations = [
            [((0, 0),)],
            [((1, 1),)],
            [((1, 1),)],
            [((1, 1),)],
            [((1, 1),)],
            [((1, 1),)],
            [((1, 1),)],
            [((1, 1),)],
        ]

        result = calculate_information_gain(
            configurations, (0, 0)
        )

        expected = -(
            (1 / 8) * math.log2(1 / 8)
            + (7 / 8) * math.log2(7 / 8)
        )

        self.assertAlmostEqual(result, expected)

    def test_all_configurations_predict_hit(self):
        configurations = [
            [((0, 0),)],
            [((0, 0),)],
        ]

        result = calculate_information_gain(
            configurations, (0, 0)
        )

        self.assertAlmostEqual(result, 0.0)

    def test_all_configurations_predict_miss(self):
        configurations = [
            [((1, 1),)],
            [((2, 2),)],
        ]

        result = calculate_information_gain(
            configurations, (0, 0)
        )

        self.assertAlmostEqual(result, 0.0)

    def test_empty_configurations(self):
        with self.assertRaises(ValueError):
            calculate_information_gain([], (0, 0))


class TestInference(unittest.TestCase):

    def setUp(self):

        self.config_a = (
            ((1, 1), (1, 2)),
            ((3, 3),)
        )

        self.config_b = (
            ((0, 0), (0, 1)),
            ((1, 1),)
        )

        self.config_c = (
            ((2, 1), (2, 2)),
            ((3, 3),)
        )

    def test_no_observations(self):

        self.assertTrue(
            is_compatible(self.config_a, {})
        )

    def test_miss_cell_cannot_contain_ship(self):

        observations = {
            (0, 0): ShotResult.MISS
        }

        self.assertFalse(
            is_compatible(self.config_b, observations)
        )

    def test_hit_cell_must_contain_ship(self):

        observations = {
            (1, 1): ShotResult.HIT
        }

        self.assertFalse(
            is_compatible(self.config_c, observations)
        )

    def test_compatible_configuration(self):

        observations = {
            (0, 0): ShotResult.MISS,
            (1, 1): ShotResult.HIT
        }

        self.assertTrue(
            is_compatible(self.config_a, observations)
        )

    def test_sunk_ship_must_be_completely_hit(self):

        configuration = (
            ((0, 0), (0, 1), (0, 2)),
            ((2, 2),)
        )

        observations = {
            (0, 0): ShotResult.HIT,
            (0, 1): ShotResult.SUNK
        }

        self.assertFalse(
            is_compatible(configuration, observations)
        )

    def test_fully_hit_sunk_ship_is_compatible(self):

        configuration = (
            ((0, 0), (0, 1), (0, 2)),
            ((2, 2),)
        )

        observations = {
            (0, 0): ShotResult.HIT,
            (0, 1): ShotResult.HIT,
            (0, 2): ShotResult.SUNK
        }

        self.assertTrue(
            is_compatible(configuration, observations)
        )

    def test_filter_configurations(self):

        observations = {
            (0, 0): ShotResult.MISS,
            (1, 1): ShotResult.HIT
        }

        configurations = [
            self.config_a,
            self.config_b,
            self.config_c
        ]

        compatible = filter_compatible_configurations(
            configurations,
            observations
        )

        self.assertEqual(
            compatible,
            [self.config_a]
        )

    
    def test_probability_matrix(self):

        configurations = [
            (((0, 0), (0, 1)),),
            (((0, 0), (1, 0)),)
        ]

        matrix = calculate_probability_matrix(
            3,
            configurations
        )

        self.assertEqual(matrix[0][0], 1.0)
        self.assertEqual(matrix[0][1], 0.5)
        self.assertEqual(matrix[1][0], 0.5)
        self.assertEqual(matrix[2][2], 0.0)

    def test_probability_matrix_dimensions(self):

        configurations = [
            (((0, 0), (0, 1)),)
        ]

        matrix = calculate_probability_matrix(
            4,
            configurations
        )

        self.assertEqual(len(matrix), 4)

        for row in matrix:
            self.assertEqual(len(row), 4)

    def test_probability_matrix_with_empty_configurations(self):

        with self.assertRaises(ValueError):
            calculate_probability_matrix(3, [])

    def test_probability_matrix_with_invalid_board_size(self):

        configurations = [
            (((0, 0),),)
        ]

        with self.assertRaises(ValueError):
            calculate_probability_matrix(0, configurations)

    def test_probability_matrix_with_out_of_bounds_cell(self):

        configurations = [
            (((0, 0), (3, 0)),)
        ]

        with self.assertRaises(ValueError):
            calculate_probability_matrix(3, configurations)

    def test_print_probability_matrix(self):

        matrix = [
            [0.5, 0.25],
            [0.75, 0.0]
        ]

        # Ensure that printing does not raise an exception.
        print_probability_matrix(matrix)

    
    def test_probability_sum_equals_fleet_size(self):

        configurations = [
            (((0, 0), (0, 1)), ((2, 2),)),
            (((0, 0), (1, 0)), ((2, 2),))
        ]

        matrix = calculate_probability_matrix(
            3,
            configurations
        )

        total_probability = sum(
            sum(row)
            for row in matrix
        )

        self.assertAlmostEqual(
            total_probability,
            3.0
        )



if __name__ == "__main__":
    unittest.main()
