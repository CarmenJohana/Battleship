import unittest

from game.ship import Ship
from game.fleet import Fleet


class TestFleet(unittest.TestCase):

    def setUp(self):
        ship1 = Ship(
            0, 3,
            ((0, 0), (0, 1), (0, 2))
        )

        ship2 = Ship(
            1, 2,
            ((2, 0), (2, 1))
        )

        self.fleet = Fleet([ship1, ship2])

    def test_initial_state(self):
        self.assertFalse(self.fleet.is_sunk)
        self.assertEqual(len(self.fleet.remaining_ships), 2)

    def test_remaining_lengths(self):
        self.assertEqual(
            self.fleet.remaining_lengths,
            [3, 2]
        )

    def test_get_ship_at(self):
        ship = self.fleet.get_ship_at((0, 1))

        self.assertEqual(ship.ship_id, 0)

    def test_sunk_ship(self):
        ship = self.fleet.get_ship_at((0, 0))

        for cell in ship.cells:
            ship.receive_hit(cell)

        self.assertEqual(
            self.fleet.remaining_lengths,
            [2]
        )


if __name__ == "__main__":
    unittest.main()
