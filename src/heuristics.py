import numpy as np

def evaluate_board(grid):
    """
    Evaluates the current board state using various heuristics.
    High score = better board.
    """
    board = np.array(grid)
    
    # Heuristic 1: Empty Tiles
    # More empty tiles are generally better for maneuverability.
    empty_cells = np.count_nonzero(board == 0)
    empty_score = empty_cells * 100
    
    # Heuristic 2: Max Tile in Corner
    # Usually bottom-right or top-left. Let's assume bottom-right for simplicity.
    max_tile = board.max()
    corner_score = 0
    if board[3, 3] == max_tile:
        corner_score = max_tile * 2
    elif board[0, 0] == max_tile or board[0, 3] == max_tile or board[3, 0] == max_tile:
        corner_score = max_tile
    
    # Heuristic 3: Monotonicity
    # Check if values are non-increasing/non-decreasing along rows and columns.
    # This keeps higher tiles aligned.
    monotonicity = calculate_monotonicity(board)
    
    # Heuristic 4: Smoothness
    # Minimizing the difference between adjacent tiles.
    smoothness = calculate_smoothness(board)
    
    return empty_score + corner_score + (monotonicity * 20) + (smoothness * 1)

def calculate_monotonicity(board):
    """Calculates if tiles are sorted along rows and columns."""
    score = 0
    # Rows
    for r in range(4):
        row = board[r, :]
        # Check both directions
        inc = all(row[i] <= row[i+1] for i in range(3))
        dec = all(row[i] >= row[i+1] for i in range(3))
        if inc or dec:
            score += np.sum(row)
            
    # Columns
    for c in range(4):
        col = board[:, c]
        inc = all(col[i] <= col[i+1] for i in range(3))
        dec = all(col[i] >= col[i+1] for i in range(3))
        if inc or dec:
            score += np.sum(col)
            
    return score

def calculate_smoothness(board):
    """Minimizes large jumps between adjacent tiles."""
    smoothness = 0
    for r in range(4):
        for c in range(4):
            if board[r, c] != 0:
                val = np.log2(board[r, c])
                # Check right
                if c < 3 and board[r, c+1] != 0:
                    smoothness -= abs(val - np.log2(board[r, c+1]))
                # Check down
                if r < 3 and board[r+1, c] != 0:
                    smoothness -= abs(val - np.log2(board[r+1, c]))
    return smoothness
