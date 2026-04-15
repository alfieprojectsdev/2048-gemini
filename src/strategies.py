import os
import re

class Strategy:
    def __init__(self, name):
        self.name = name

    def get_move(self, game):
        raise NotImplementedError

class PriorityStrategy(Strategy):
    def __init__(self, name, priority_list):
        super().__init__(name)
        self.priority_list = [p.strip().upper() for p in priority_list]

    def get_move(self, game):
        # Simply try directions in priority order until one works
        for move in self.priority_list:
            # We don't actually move here, we just check if it WOULD move
            # But since our engine's move() returns True/False, we can just return the move
            # and the Game runner will apply it.
            return move
        return None

class MarkdownStrategy(PriorityStrategy):
    @classmethod
    def from_file(cls, filepath):
        name = os.path.basename(filepath).replace('.md', '').replace('_', ' ').title()
        with open(filepath, 'r') as f:
            content = f.read()

        # Look for Priority: UP, DOWN, etc.
        match = re.search(r'Priority:\s*([A-Z,\s]+)', content, re.IGNORECASE)
        if match:
            priority_str = match.group(1)
            priority_list = [p.strip() for p in priority_str.split(',')]
            return cls(name, priority_list)
        else:
            raise ValueError(f"No Priority field found in {filepath}")

from heuristics import evaluate_board
import numpy as np

class ExpectimaxStrategy(Strategy):
    def __init__(self, name="Expectimax", depth=3):
        super().__init__(name)
        self.depth = depth
        self.transposition_table = {}

    def get_move(self, game):
        self.transposition_table = {}
        best_score = -float('inf')
        best_move = None
        
        available_moves = game.get_available_moves()
        if not available_moves:
            return None
            
        for move in available_moves:
            temp_game = game.copy()
            temp_game.move_no_spawn(move)
            score = self.expectimax(temp_game, self.depth - 1, False)
            if score > best_score:
                best_score = score
                best_move = move
        return best_move

    def expectimax(self, game, depth, is_player):
        # Hash board for Transposition Table
        board_hash = hash(tuple(tuple(row) for row in game.grid))
        if board_hash in self.transposition_table:
            return self.transposition_table[board_hash]

        if depth == 0 or game.game_over:
            return evaluate_board(game.grid)

        if is_player:
            value = -float('inf')
            available_moves = game.get_available_moves()
            if not available_moves:
                return evaluate_board(game.grid)
            for move in available_moves:
                temp_game = game.copy()
                temp_game.move_no_spawn(move)
                value = max(value, self.expectimax(temp_game, depth - 1, False))
        else:
            # Average results of random spawns
            value = 0
            empty_cells = [(r, c) for r in range(game.size) for c in range(game.size) if game.grid[r][c] == 0]
            if not empty_cells:
                return evaluate_board(game.grid)
            
            # For efficiency in deep search, we might only check a few random spawns
            # but for depth 3, checking all is fine.
            for r, c in empty_cells:
                # 90% chance for 2
                game.grid[r][c] = 2
                value += 0.9 * self.expectimax(game, depth - 1, True)
                # 10% chance for 4
                game.grid[r][c] = 4
                value += 0.1 * self.expectimax(game, depth - 1, True)
                # Backtrack
                game.grid[r][c] = 0
            value = value / len(empty_cells)

        self.transposition_table[board_hash] = value
        return value

class MCTSStrategy(Strategy):
    def __init__(self, name="MCTS", simulations=100):
        super().__init__(name)
        self.simulations = simulations

    def get_move(self, game):
        available_moves = game.get_available_moves()
        if not available_moves:
            return None
            
        scores = {}
        for move in available_moves:
            scores[move] = 0
            for _ in range(self.simulations // len(available_moves)):
                temp_game = game.copy()
                temp_game.move_no_spawn(move)
                temp_game.spawn_tile()
                scores[move] += self.random_rollout(temp_game)
        
        return max(scores, key=scores.get)

    def random_rollout(self, game):
        """Play randomly until game ends, return final score. Faster implementation."""
        directions = ['UP', 'DOWN', 'LEFT', 'RIGHT']
        while True:
            # We use test_move logic inside move_fast to avoid unnecessary work
            random.shuffle(directions)
            moved = False
            for move in directions:
                if game.move_fast(move):
                    moved = True
                    break
            if not moved:
                break
        return game.score
Applied fuzzy match at line 133-146.
import itertools
import random

def generate_random_strategies(directory, count=5):
    """Generates random permutations of priority rules and saves them to .md files."""
    directions = ["UP", "DOWN", "LEFT", "RIGHT"]
    all_permutations = list(itertools.permutations(directions))
    selected = random.sample(all_permutations, min(count, len(all_permutations)))

    if not os.path.exists(directory):
        os.makedirs(directory)

    generated = []
    for i, p in enumerate(selected):
        priority_str = ", ".join(p)
        filename = f"random_strategy_{i+1}.md"
        filepath = os.path.join(directory, filename)
        
        content = f"# Random Strategy {i+1}\n\n"
        content += "A randomly generated move-priority heuristic for 2048.\n\n"
        content += f"Priority: {priority_str}\n"
        
        with open(filepath, 'w') as f:
            f.write(content)
        
        generated.append(MarkdownStrategy(f"Random Strategy {i+1}", list(p)))
    
    return generated

def load_strategies(directory):
    strategies = []
    if not os.path.exists(directory):
        return []
    for filename in os.listdir(directory):
        if filename.endswith('.md'):
            try:
                strategies.append(MarkdownStrategy.from_file(os.path.join(directory, filename)))
            except Exception as e:
                print(f"Error loading {filename}: {e}")
    return strategies
