import unittest

from game.ship import Ship


class TestShip(unittest.TestCase):

    def setUp(self):
        self.ship = Ship(
            ship_id=0,
            length=3,
            cells=((0, 0), (0, 1), (0, 2))
        )

    def test_initial_state(self):
        self.assertFalse(self.ship.is_sunk)
        self.assertEqual(len(self.ship.hits), 0)

    def test_receive_hit(self):
        result = self.ship.receive_hit((0, 0))

        self.assertTrue(result)
        self.assertEqual(len(self.ship.hits), 1)

    def test_invalid_hit(self):
        result = self.ship.receive_hit((2, 2))

        self.assertFalse(result)
        self.assertEqual(len(self.ship.hits), 0)

    def test_duplicate_hit(self):
        self.ship.receive_hit((0, 0))
        self.ship.receive_hit((0, 0))

        self.assertEqual(len(self.ship.hits), 1)

    def test_ship_sunk(self):
        for cell in self.ship.cells:
            self.ship.receive_hit(cell)

        self.assertTrue(self.ship.is_sunk)


if __name__ == "__main__":
    unittest.main()
