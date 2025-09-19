# test_ps2.py
# Test Circuit Board Solutions
# David Kopec
import unittest
from zbps2 import Chip, generate_grid, solution, display_grid, Grid


class CircuitBoardTestCase(unittest.TestCase):
    def check_grid(self, grid: Grid, expected_blank_count: int) -> None:
        print(f"Expected blank count: {expected_blank_count}")
        display_grid(grid)
        # Check solution has right number of blank spots
        self.assertEqual(sum([row.count("-") for row in grid]), expected_blank_count)

    def test_easy_one_chip(self):
        easy_grid = generate_grid(10, 10)
        easy_chips = [Chip(5, 5, "*")]
        sol = solution(easy_chips, easy_grid)
        self.assertIsNotNone(sol)
        if sol is not None:
            self.check_grid(sol, 75)

    def test_easy_three_chips(self):
        easy_grid = generate_grid(10, 10)
        easy_chips = [Chip(5, 5, "*"), Chip(4, 4, "#"), Chip(2, 2, "@")]
        sol = solution(easy_chips, easy_grid)
        self.assertIsNotNone(sol)
        if sol is not None:
            self.check_grid(sol, 55)
    
    def test_one_chip_does_not_fit(self):
        easy_grid = generate_grid(10, 10)
        easy_chips = [Chip(11, 5, "*")]
        sol = solution(easy_chips, easy_grid)
        self.assertIsNone(sol)
    
    def test_two_chips_do_not_fit(self):
        easy_grid = generate_grid(10, 10)
        easy_chips = [Chip(10, 5, "*"), Chip(10, 6, "#")]
        sol = solution(easy_chips, easy_grid)
        self.assertIsNone(sol)
    
    def test_two_chips_fit_through_rotation(self):
        easy_grid = generate_grid(10, 10)
        easy_chips = [Chip(10, 5, "*"), Chip(4, 10, "#")]
        sol = solution(easy_chips, easy_grid)
        self.assertIsNotNone(sol)
        if sol is not None:
            self.check_grid(sol, 10)
    
    def test_eight_small_chips(self):
        easy_grid = generate_grid(10, 10)
        easy_chips = [Chip(2, 5, "*"), Chip(4, 3, "#"), Chip(1, 8, "$"), Chip(6, 2, "@"), Chip(3, 3, "%"), Chip(2, 2, "^"), Chip(3, 4, "0"), Chip(3, 4, "8")]
        sol = solution(easy_chips, easy_grid)
        self.assertIsNotNone(sol)
        if sol is not None:
            self.check_grid(sol, 21)
    
    def test_four_small_chips_dont_fit(self):
        easy_grid = generate_grid(6, 6)
        easy_chips = [Chip(3, 3, "*"), Chip(3, 3, "#"), Chip(3, 3, "@"), Chip(4, 3, "0")]
        sol = solution(easy_chips, easy_grid)
        self.assertIsNone(sol)

if __name__ == "__main__":
    unittest.main()
