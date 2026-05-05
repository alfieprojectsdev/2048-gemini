import unittest
import sys
import os

# Add src to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from logic import Game2048
from heuristics import evaluate_board


class TestLogic(unittest.TestCase):
    def setUp(self):
        self.game = Game2048(size=4)

    def test_initial_state(self):
        non_zero = sum(1 for r in range(4) for c in range(4) if self.game.grid[r][c] != 0)
        self.assertEqual(non_zero, 2)
        self.assertEqual(self.game.score, 0)

    def test_slide_and_merge(self):
        row = [2, 2, 0, 4]
        new_row = self.game._slide_and_merge(row)
        self.assertEqual(new_row, [4, 4, 0, 0])
        self.assertEqual(self.game.score, 4)

    def test_move_left(self):
        self.game.grid = [
            [2, 2, 0, 0],
            [0, 4, 4, 0],
            [0, 0, 8, 8],
            [16, 0, 16, 0]
        ]
        # Use move_no_spawn for deterministic assertions (no random tile spawn)
        self.game.move_no_spawn('LEFT')
        self.assertEqual(self.game.grid[0][0], 4)
        self.assertEqual(self.game.grid[1][0], 8)
        self.assertEqual(self.game.grid[2][0], 16)
        self.assertEqual(self.game.grid[3][0], 32)

    def test_full_grid_no_moves(self):
        self.game.grid = [
            [2, 4, 2, 4],
            [4, 2, 4, 2],
            [2, 4, 2, 4],
            [4, 2, 4, 2]
        ]
        self.assertFalse(self.game.can_move())

    def test_test_move_returns_false_when_stuck(self):
        self.game.grid = [
            [2, 4, 2, 4],
            [4, 2, 4, 2],
            [2, 4, 2, 4],
            [4, 2, 4, 2]
        ]
        for direction in ['UP', 'DOWN', 'LEFT', 'RIGHT']:
            self.assertFalse(self.game.test_move(direction),
                             msg=f"Expected test_move('{direction}') to be False on a stuck board")

    def test_test_move_detects_valid_move(self):
        # Tile already at the right edge: LEFT is valid (can slide), RIGHT is not
        self.game.grid = [
            [0, 0, 0, 2],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0]
        ]
        self.assertTrue(self.game.test_move('LEFT'))
        self.assertFalse(self.game.test_move('RIGHT'))


class TestHeuristics(unittest.TestCase):
    def test_evaluate_board_standard_4x4(self):
        grid = [[0] * 4 for _ in range(4)]
        grid[3][3] = 2048
        score = evaluate_board(grid)
        self.assertIsInstance(score, float)
        self.assertGreater(score, 0)

    def test_evaluate_board_non_4x4(self):
        """evaluate_board must work correctly on non-4x4 grids after the size-agnostic fix."""
        grid = [[0] * 6 for _ in range(6)]
        grid[5][5] = 2048
        score = evaluate_board(grid)
        self.assertIsInstance(score, float)
        self.assertGreater(score, 0)

    def test_corner_preference(self):
        """The preferred bottom-right corner should score higher than other corners."""
        size = 4
        base_grid = [[2] * size for _ in range(size)]

        grid_br = [row[:] for row in base_grid]
        grid_br[3][3] = 1024

        grid_tl = [row[:] for row in base_grid]
        grid_tl[0][0] = 1024

        score_br = evaluate_board(grid_br)
        score_tl = evaluate_board(grid_tl)
        self.assertGreater(score_br, score_tl,
                           "Bottom-right corner should yield higher heuristic score than top-left")


if __name__ == '__main__':
    unittest.main()
