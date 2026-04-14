import unittest
import sys
import os

# Add src to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from logic import Game2048

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
        self.game.move('LEFT')
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

if __name__ == '__main__':
    unittest.main()
