import unittest

from game.placements import generate_placements


class TestGeneratePlacements(unittest.TestCase):

    def test_number_of_placements(self):
        placements = generate_placements(5, 3)
        self.assertEqual(len(placements), 30)

    def test_horizontal_placements(self):
        placements = generate_placements(5, 3)

        horizontal = [
            p for p in placements
            if all(cell[0] == p[0][0] for cell in p)
        ]

        self.assertEqual(len(horizontal), 15)

    def test_vertical_placements(self):
        placements = generate_placements(5, 3)

        vertical = [
            p for p in placements
            if all(cell[1] == p[0][1] for cell in p)
        ]

        self.assertEqual(len(vertical), 15)

    def test_single_cell_ship(self):
        placements = generate_placements(5, 1)

        self.assertEqual(len(placements), 25)
        self.assertEqual(len(set(placements)), 25)

    def test_ship_longer_than_board(self):
        placements = generate_placements(5, 6)

        self.assertEqual(placements, [])

    def test_invalid_board_size(self):
        with self.assertRaises(ValueError):
            generate_placements(0, 3)

    def test_invalid_ship_length(self):
        with self.assertRaises(ValueError):
            generate_placements(5, 0)

    def test_placements_are_inside_board(self):
        n = 5
        placements = generate_placements(n, 3)

        for placement in placements:
            for row, col in placement:
                self.assertTrue(0 <= row < n)
                self.assertTrue(0 <= col < n)

    def test_cells_are_consecutive(self):
        placements = generate_placements(5, 3)

        for placement in placements:
            rows = [cell[0] for cell in placement]
            cols = [cell[1] for cell in placement]

            horizontal = all(r == rows[0] for r in rows)
            vertical = all(c == cols[0] for c in cols)

            self.assertTrue(horizontal or vertical)


if __name__ == "__main__":
    unittest.main()
