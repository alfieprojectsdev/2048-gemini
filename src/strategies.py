from __future__ import annotations
import os
import re
import sys
import itertools
import random
from typing import TYPE_CHECKING

# Ensure src/ is on the path regardless of working directory
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from heuristics import evaluate_board

if TYPE_CHECKING:
    from logic import Game2048


class Strategy:
    def __init__(self, name: str) -> None:
        self.name = name

    def get_move(self, game: Game2048) -> str | None:
        raise NotImplementedError


class PriorityStrategy(Strategy):
    def __init__(self, name: str, priority_list: list[str]) -> None:
        super().__init__(name)
        self.priority_list = [p.strip().upper() for p in priority_list]

    def get_move(self, game: Game2048) -> str | None:
        # Simply try directions in priority order until one works
        for move in self.priority_list:
            if game.test_move(move):
                return move
        return None


class MarkdownStrategy(PriorityStrategy):
    @classmethod
    def from_file(cls, filepath: str) -> MarkdownStrategy:
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


class ExpectimaxStrategy(Strategy):
    def __init__(self, name: str = "Expectimax", depth: int = 3) -> None:
        super().__init__(name)
        self.depth = depth
        self.transposition_table: dict = {}

    def get_move(self, game: Game2048) -> str | None:
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

    def expectimax(self, game: Game2048, depth: int, is_player: bool) -> float:
        # Hash board for Transposition Table — key includes depth and player flag
        # to prevent a shallower result from being reused at a deeper search level.
        board_hash = hash(tuple(tuple(row) for row in game.grid))
        tt_key = (board_hash, depth, is_player)
        if tt_key in self.transposition_table:
            return self.transposition_table[tt_key]

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
            value = 0.0
            empty_cells = [(r, c) for r in range(game.size) for c in range(game.size) if game.grid[r][c] == 0]
            if not empty_cells:
                return evaluate_board(game.grid)

            for r, c in empty_cells:
                # 90% chance for 2, 10% chance for 4 — backtrack after each probe
                game.grid[r][c] = 2
                value += 0.9 * self.expectimax(game, depth - 1, True)
                game.grid[r][c] = 4
                value += 0.1 * self.expectimax(game, depth - 1, True)
                game.grid[r][c] = 0
            value = value / len(empty_cells)

        self.transposition_table[tt_key] = value
        return value


class MonteCarloStrategy(Strategy):
    """
    Flat Monte Carlo strategy: for each candidate move, runs `simulations`
    random rollouts and returns the move with the highest average final score.

    Note: despite the common misnomer, this is NOT MCTS (Monte Carlo Tree Search),
    which requires UCT-based selection and backpropagation through a tree. This is
    pure Monte Carlo rollout (a.k.a. flat Monte Carlo).
    """

    def __init__(self, name: str = "Monte Carlo", simulations: int = 100) -> None:
        super().__init__(name)
        self.simulations = simulations

    def get_move(self, game: Game2048) -> str | None:
        available_moves = game.get_available_moves()
        if not available_moves:
            return None

        scores: dict[str, float] = {}
        for move in available_moves:
            scores[move] = 0
            for _ in range(self.simulations // len(available_moves)):
                temp_game = game.copy()
                temp_game.move_no_spawn(move)
                temp_game.spawn_tile()
                scores[move] += self.random_rollout(temp_game)

        return max(scores, key=scores.get)  # type: ignore[arg-type]

    def random_rollout(self, game: Game2048) -> int:
        """Play randomly until game ends, return final score."""
        directions = ['UP', 'DOWN', 'LEFT', 'RIGHT']
        while True:
            random.shuffle(directions)
            moved = False
            for move in directions:
                if game.move_fast(move):
                    moved = True
                    break
            if not moved:
                break
        return game.score


def generate_random_strategies(directory: str, count: int = 5) -> list[MarkdownStrategy]:
    """Generates random permutations of priority rules and saves them to .md files."""
    directions = ["UP", "DOWN", "LEFT", "RIGHT"]
    all_permutations = list(itertools.permutations(directions))

    if count > len(all_permutations):
        print(f"Warning: only {len(all_permutations)} unique direction permutations exist; "
              f"generating {len(all_permutations)} instead of {count}.")
        count = len(all_permutations)

    selected = random.sample(all_permutations, count)

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


def load_strategies(directory: str) -> list[MarkdownStrategy]:
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
