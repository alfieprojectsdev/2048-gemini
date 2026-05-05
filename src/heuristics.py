from __future__ import annotations
import numpy as np
from numpy.typing import NDArray

# Heuristic weight constants — tune these to change AI playing style.
WEIGHT_EMPTY = 100        # maneuverability is critical; each open cell has high value
WEIGHT_CORNER = 2         # multiplier applied to the raw corner score (see evaluate_board)
WEIGHT_MONOTONICITY = 20  # sorted rows/cols greatly improve merge potential
WEIGHT_SMOOTHNESS = 1     # smoothness is expressed as a negative penalty; scale kept small


def evaluate_board(grid: list[list[int]]) -> float:
    """
    Evaluates the current board state using various heuristics.
    High score = better board.
    """
    board = np.array(grid, dtype=float)
    size = board.shape[0]
    max_idx = size - 1

    # Heuristic 1: Empty Tiles
    # More empty tiles are generally better for maneuverability.
    empty_cells = np.count_nonzero(board == 0)

    # Heuristic 2: Max Tile in Corner
    # The bottom-right corner [max_idx, max_idx] is the preferred target because the
    # dominant winning pattern is sliding left+up, which concentrates the max tile
    # there. Full WEIGHT_CORNER reward for that corner; half for any other corner.
    max_tile = board.max()
    corner_score = 0
    if board[max_idx, max_idx] == max_tile:
        corner_score = max_tile           # preferred corner: full weight
    elif (board[0, 0] == max_tile or board[0, max_idx] == max_tile
          or board[max_idx, 0] == max_tile):
        corner_score = max_tile // 2      # any other corner: half weight

    # Heuristic 3: Monotonicity
    # Check if values are non-increasing/non-decreasing along rows and columns.
    # This keeps higher tiles aligned.
    monotonicity = calculate_monotonicity(board)

    # Heuristic 4: Smoothness
    # Minimizing the difference between adjacent tiles.
    smoothness = calculate_smoothness(board)

    return (empty_cells * WEIGHT_EMPTY
            + corner_score * WEIGHT_CORNER
            + monotonicity * WEIGHT_MONOTONICITY
            + smoothness * WEIGHT_SMOOTHNESS)


def calculate_monotonicity(board: NDArray) -> float:
    """Calculates if tiles are sorted along rows and columns."""
    size = board.shape[0]
    score = 0.0
    # Rows
    for r in range(size):
        row = board[r, :]
        inc = all(row[i] <= row[i + 1] for i in range(size - 1))
        dec = all(row[i] >= row[i + 1] for i in range(size - 1))
        if inc or dec:
            score += float(np.sum(row))

    # Columns
    for c in range(size):
        col = board[:, c]
        inc = all(col[i] <= col[i + 1] for i in range(size - 1))
        dec = all(col[i] >= col[i + 1] for i in range(size - 1))
        if inc or dec:
            score += float(np.sum(col))

    return score


def calculate_smoothness(board: NDArray) -> float:
    """Minimizes large jumps between adjacent tiles."""
    size = board.shape[0]
    smoothness = 0.0
    for r in range(size):
        for c in range(size):
            if board[r, c] != 0:
                val = np.log2(board[r, c])
                # Check right
                if c < size - 1 and board[r, c + 1] != 0:
                    smoothness -= abs(val - np.log2(board[r, c + 1]))
                # Check down
                if r < size - 1 and board[r + 1, c] != 0:
                    smoothness -= abs(val - np.log2(board[r + 1, c]))
    return smoothness
