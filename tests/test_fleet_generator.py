import unittest
import random

from game.fleet_generator import generate_random_fleet


class TestFleetGenerator(unittest.TestCase):

    def test_correct_number_of_ships(self):

        fleet = generate_random_fleet(4, [3, 2, 2])

        self.assertEqual(len(fleet.ships), 3)

    def test_correct_ship_lengths(self):

        fleet = generate_random_fleet(4, [3, 2, 2])

        self.assertEqual(
            sorted(fleet.remaining_lengths, reverse=True),
            [3, 2, 2]
        )

    def test_ships_do_not_overlap(self):

        fleet = generate_random_fleet(4, [3, 2, 2])

        occupied = set()

        for ship in fleet.ships:

            cells = set(ship.cells)

            self.assertTrue(occupied.isdisjoint(cells))

            occupied.update(cells)

    def test_all_ships_are_inside_board(self):

        n = 4

        fleet = generate_random_fleet(n, [3, 2, 2])

        for ship in fleet.ships:
            for row, col in ship.cells:

                self.assertTrue(0 <= row < n)
                self.assertTrue(0 <= col < n)

    def test_reproducibility_with_same_seed(self):

        rng_1 = random.Random(42)
        rng_2 = random.Random(42)

        fleet_1 = generate_random_fleet(
            4, [3, 2, 2], rng_1
        )

        fleet_2 = generate_random_fleet(
            4, [3, 2, 2], rng_2
        )

        positions_1 = [ship.cells for ship in fleet_1.ships]
        positions_2 = [ship.cells for ship in fleet_2.ships]

        self.assertEqual(positions_1, positions_2)

    def test_impossible_fleet(self):

        with self.assertRaises(ValueError):
            generate_random_fleet(3, [4, 2])

    def test_empty_fleet(self):

        with self.assertRaises(ValueError):
            generate_random_fleet(3, [])

    def test_invalid_board_size(self):

        with self.assertRaises(ValueError):
            generate_random_fleet(0, [2])


if __name__ == "__main__":
    unittest.main()
