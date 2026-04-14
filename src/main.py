import argparse
import os
import sys
from ui import run_manual, run_auto
from strategies import load_strategies, generate_random_strategies, ExpectimaxStrategy, MCTSStrategy
from simulator import Simulator

def progress_bar(current, total, prefix="Simulating", size=30):
    percent = (current / total) * 100
    filled = int(size * current // total)
    bar = "=" * filled + "-" * (size - filled)
    sys.stdout.write(f"\r{prefix} [{bar}] {percent:.1f}% ({current}/{total})")
    sys.stdout.flush()

def main():
    parser = argparse.ArgumentParser(description="2048 Teaching Aid & Strategy Comparison")
    parser.add_argument("--mode", choices=["manual", "auto", "evaluate", "generate"], default="manual", help="Operation mode")
    parser.add_argument("--ai", choices=["expectimax", "mcts", "priority"], default="priority", help="AI strategy to use for auto/evaluate")
    parser.add_argument("--games", type=int, default=100, help="Number of games for evaluation")
    parser.add_argument("--count", type=int, default=5, help="Number of random strategies to generate")
    parser.add_argument("--cv", action="store_true", help="Enable camera-based gesture controls (manual mode only)")
    args = parser.parse_args()

    # Resolve paths
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    strat_dir = os.path.join(base_dir, "strategies")

    def get_ai_strategies(mode_name):
        if mode_name == "expectimax":
            return [ExpectimaxStrategy("Expectimax Depth 3", depth=3), ExpectimaxStrategy("Expectimax Depth 2", depth=2)]
        elif mode_name == "mcts":
            return [MCTSStrategy("MCTS 100", simulations=100), MCTSStrategy("MCTS 50", simulations=50)]
        else:
            return load_strategies(strat_dir)

    if args.mode == "manual":
        run_manual(use_cv=args.cv)
    elif args.mode == "auto":
        strategies = get_ai_strategies(args.ai)
        if not strategies:
            print(f"No strategies found.")
            return
        run_auto(strategies)
    elif args.mode == "generate":
        print(f"Generating {args.count} random strategies in {strat_dir}...")
        generate_random_strategies(strat_dir, args.count)
    elif args.mode == "evaluate":
        strategies = get_ai_strategies(args.ai)
        if not strategies:
            print(f"No strategies found.")
            return

        print(f"Evaluating {len(strategies)} strategies over {args.games} games each...")
        print("-" * 55)

        results = []
        for strat in strategies:
            print(f"\nTarget: {strat.name}")
            sim = Simulator(strat, num_games=args.games)
            stats = sim.run(progress_callback=lambda c, t: progress_bar(c, t, prefix="Progress"))
            results.append(stats)
            print() # New line after progress bar

        print("\n" + f"{'Strategy':<20} | {'Avg Score':<10} | {'Max Tile':<8} | {'Games/s':<8}")
        print("-" * 55)
        for stats in results:
            print(f"{stats['strategy_name']:<20} | {stats['avg_score']:<10.1f} | {stats['max_tile']:<8} | {stats['games_per_second']:<8.1f}")

if __name__ == "__main__":
    main()
