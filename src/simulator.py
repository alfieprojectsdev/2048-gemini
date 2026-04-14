import time
import statistics
from logic import Game2048

class Simulator:
    def __init__(self, strategy, num_games=100, max_moves=10000):
        self.strategy = strategy
        self.num_games = num_games
        self.max_moves = max_moves
        self.results = []

    def run(self, progress_callback=None):
        """Runs batch simulations and returns statistics."""
        scores = []
        max_tiles = []
        start_time = time.time()

        for i in range(self.num_games):
            game = Game2048()
            moves_count = 0
            while not game.game_over and moves_count < self.max_moves:
                move = self.strategy.get_move(game)
                if move and game.move(move):
                    moves_count += 1
                else:
                    break
            
            scores.append(game.score)
            max_tiles.append(game.get_max_tile())
            
            if progress_callback:
                progress_callback(i + 1, self.num_games)

        end_time = time.time()
        duration = end_time - start_time

        stats = {
            "strategy_name": self.strategy.name,
            "games_played": self.num_games,
            "avg_score": statistics.mean(scores),
            "median_score": statistics.median(scores),
            "max_score": max(scores),
            "max_tile": max(max_tiles),
            "avg_max_tile": statistics.mean(max_tiles),
            "duration_seconds": duration,
            "games_per_second": self.num_games / duration if duration > 0 else 0
        }
        return stats
