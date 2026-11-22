import unittest

from game.configurations import generate_configurations


class TestGenerateConfigurations(unittest.TestCase):

    def test_single_ship(self):
        configurations = generate_configurations(3, [2])

        self.assertEqual(len(configurations), 12)

    def test_no_overlapping_ships(self):
        configurations = generate_configurations(3, [2, 2])

        for configuration in configurations:
            occupied = set()

            for placement in configuration:
                cells = set(placement)

                self.assertTrue(occupied.isdisjoint(cells))
                occupied.update(cells)

    def test_no_duplicate_configurations(self):
        configurations = generate_configurations(3, [2, 2])

        self.assertEqual(
            len(configurations),
            len(set(configurations))
        )

    def test_ships_can_touch(self):
        configurations = generate_configurations(3, [2, 2])

        placement_1 = ((0, 0), (0, 1))
        placement_2 = ((1, 0), (1, 1))

        self.assertTrue(
            any(
                placement_1 in configuration
                and placement_2 in configuration
                for configuration in configurations
            )
        )

    def test_ship_longer_than_board(self):
        configurations = generate_configurations(3, [4])

        self.assertEqual(configurations, [])

    def test_empty_fleet(self):
        configurations = generate_configurations(3, [])

        self.assertEqual(configurations, [()])

    def test_invalid_board_size(self):
        with self.assertRaises(ValueError):
            generate_configurations(0, [2])

    def test_invalid_ship_length(self):
        with self.assertRaises(ValueError):
            generate_configurations(3, [0])


if __name__ == "__main__":
    unittest.main()
