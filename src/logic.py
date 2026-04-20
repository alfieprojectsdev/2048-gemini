import random

class Game2048:
    def __init__(self, size=4):
        self.size = size
        self.reset()

    def reset(self):
        self.grid = [[0] * self.size for _ in range(self.size)]
        self.score = 0
        self.game_over = False
        self.spawn_tile()
        self.spawn_tile()

    def spawn_tile(self):
        empty_cells = [(r, c) for r in range(self.size) for c in range(self.size) if self.grid[r][c] == 0]
        if empty_cells:
            r, c = random.choice(empty_cells)
            self.grid[r][c] = 4 if random.random() < 0.1 else 2
            return True
        return False

    def can_move(self):
        # Check for empty cells
        for r in range(self.size):
            for c in range(self.size):
                if self.grid[r][c] == 0:
                    return True
        # Check for possible merges
        for r in range(self.size):
            for c in range(self.size):
                curr = self.grid[r][c]
                # Check right
                if c < self.size - 1 and self.grid[r][c + 1] == curr:
                    return True
                # Check down
                if r < self.size - 1 and self.grid[r + 1][c] == curr:
                    return True
        return False

    def move(self, direction):
        """Standard move with change detection and spawning."""
        if self.game_over: return False
        original_grid = [row[:] for row in self.grid]
        
        if direction == 'UP': self._move_up()
        elif direction == 'DOWN': self._move_down()
        elif direction == 'LEFT': self._move_left()
        elif direction == 'RIGHT': self._move_right()

        if self.grid != original_grid:
            self.spawn_tile()
            if not self.can_move(): self.game_over = True
            return True
        return False

    def move_fast(self, direction):
        """Optimized move for AI rollouts. Returns True if board changed, no deep-copy."""
        # Use our existing test_move to see if it's worth actually moving
        if not self.test_move(direction):
            return False
            
        if direction == 'UP': self._move_up()
        elif direction == 'DOWN': self._move_down()
        elif direction == 'LEFT': self._move_left()
        elif direction == 'RIGHT': self._move_right()
        
        self.spawn_tile()
        # We don't check game_over here to save time; 
        # the rollout loop will detect it via test_move returning False for all dirs
        return True

    def _slide_and_merge(self, row):
        """Slides and merges a single row (to the left)."""
        # Remove zeros
        new_row = [val for val in row if val != 0]
        # Merge identical adjacent values
        merged_row = []
        i = 0
        while i < len(new_row):
            if i + 1 < len(new_row) and new_row[i] == new_row[i + 1]:
                val = new_row[i] * 2
                merged_row.append(val)
                self.score += val
                i += 2
            else:
                merged_row.append(new_row[i])
                i += 1
        # Fill rest with zeros
        while len(merged_row) < self.size:
            merged_row.append(0)
        return merged_row

    def _move_left(self):
        for r in range(self.size):
            self.grid[r] = self._slide_and_merge(self.grid[r])

    def _move_right(self):
        for r in range(self.size):
            reversed_row = self.grid[r][::-1]
            new_row = self._slide_and_merge(reversed_row)
            self.grid[r] = new_row[::-1]

    def _move_up(self):
        for c in range(self.size):
            col = [self.grid[r][c] for r in range(self.size)]
            new_col = self._slide_and_merge(col)
            for r in range(self.size):
                self.grid[r][c] = new_col[r]

    def _move_down(self):
        for c in range(self.size):
            col = [self.grid[r][c] for r in range(self.size)][::-1]
            new_col = self._slide_and_merge(col)
            for r in range(self.size):
                self.grid[r][c] = new_col[::-1][r]

    def copy(self):
        new_game = Game2048(self.size)
        new_game.grid = [row[:] for row in self.grid]
        new_game.score = self.score
        new_game.game_over = self.game_over
        return new_game

    def get_available_moves(self):
        """Returns a list of directions that would change the board without full cloning."""
        moves = []
        for direction in ['UP', 'DOWN', 'LEFT', 'RIGHT']:
            if self.test_move(direction):
                moves.append(direction)
        return moves

    def test_move(self, direction):
        """Checks if a move is possible without modifying the board."""
        if direction == 'LEFT':
            for r in range(self.size):
                row = self.grid[r]
                # Can move if there's a zero before a non-zero, or two adjacent identical non-zeros
                last_val = -1
                has_zero = False
                for val in row:
                    if val == 0:
                        has_zero = True
                    else:
                        if has_zero or val == last_val:
                            return True
                        last_val = val
        elif direction == 'RIGHT':
            for r in range(self.size):
                row = self.grid[r][::-1]
                last_val = -1
                has_zero = False
                for val in row:
                    if val == 0:
                        has_zero = True
                    else:
                        if has_zero or val == last_val:
                            return True
                        last_val = val
        elif direction == 'UP':
            for c in range(self.size):
                col = [self.grid[r][c] for r in range(self.size)]
                last_val = -1
                has_zero = False
                for val in col:
                    if val == 0:
                        has_zero = True
                    else:
                        if has_zero or val == last_val:
                            return True
                        last_val = val
        elif direction == 'DOWN':
            for c in range(self.size):
                col = [self.grid[r][c] for r in range(self.size)][::-1]
                last_val = -1
                has_zero = False
                for val in col:
                    if val == 0:
                        has_zero = True
                    else:
                        if has_zero or val == last_val:
                            return True
                        last_val = val
        return False

    def move_no_spawn(self, direction):
        """Moves in direction without spawning a new tile. Returns True if board changed."""
        original_grid = [row[:] for row in self.grid]
        if direction == 'UP': self._move_up()
        elif direction == 'DOWN': self._move_down()
        elif direction == 'LEFT': self._move_left()
        elif direction == 'RIGHT': self._move_right()
        changed = self.grid != original_grid
        if changed and not self.can_move():
            self.game_over = True
        return changed

    def get_max_tile(self):
        return max(max(row) for row in self.grid)
