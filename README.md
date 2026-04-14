# 2048 Strategy Comparison (Teaching Aid)

A project designed to teach software engineering principles and heuristic design through the classic game of 2048. It features both a manual play mode and an automated "Strategy Comparison" mode.

## 🎓 Learning Objectives
1.  **Engine/UI Separation**: See how the 2048 logic is entirely independent of the `pygame` interface.
2.  **Heuristic Strategies**: Understand how different "priority rules" (heuristics) affect the final score.
3.  **Persistence**: Learn how to load configuration and logic from external Markdown files.
4.  **Steelman Design**: Observe why we chose Markdown-based priority lists over complex neural networks for this teaching example.

## 🛠 Features
- **Manual Mode**: Standard 2048 gameplay.
- **Auto Mode (Comparison)**: Pits two strategies against each other in real-time.
- **Markdown Strategies**: Define a strategy's logic simply by listing its move priorities in a `.md` file.

## 🚀 Getting Started
Ensure you have [uv](https://github.com/astral-sh/uv) installed.

### 1. Setup
```bash
uv sync
```

### 2. Manual Play
```bash
uv run src/main.py --mode manual
```
- **Arrows / WASD**: Move
- **R**: Restart
- **Esc**: Exit

### 3. Run Strategy Comparison
```bash
uv run src/main.py --mode auto
```

### 4. Batch Simulation & Evaluation (Headless)
For high-speed testing of strategies without the GUI:
```bash
uv run src/main.py --mode evaluate --games 500
```

### 5. Generate Random Strategies
Automatically create new heuristic combinations to test:
```bash
uv run src/main.py --mode generate --count 10
```

## 🤖 Advanced AI Strategies
This project now includes advanced search-based AI strategies:
- **Expectimax**: Uses a recursive search tree with a Transposition Table and board heuristics (monotonicity, smoothness, empty tiles).
- **MCTS (Monte Carlo Tree Search)**: Runs thousands of random rollouts to identify the move with the highest survival probability.

To run these:
```bash
# Auto mode with Expectimax
uv run src/main.py --mode auto --ai expectimax

# Evaluate MCTS performance
uv run src/main.py --mode evaluate --ai mcts --games 50
```

## 🏋️ Aerobic Gesture Controls (Computer Vision)
Turn 2048 into a workout by controlling the game with your hands! This uses your webcam to track your hand positions.

To run with CV enabled:
```bash
# Enable camera controls in manual mode
uv run src/main.py --mode manual --cv
```

### How to Play:
- **REACH UP**: Raise your hand high to move the tiles UP.
- **REACH DOWN**: Lower your hand to move tiles DOWN.
- **REACH LEFT/RIGHT**: Move your hand to the sides to slide tiles.
- *Note: The center of the camera is a "deadzone" where no moves are triggered.*

## 🧪 Customization & Exercises
...
### 5. Explore Computer Vision
Read `docs/CV_GUIDE.md` to understand how the camera tracks your hands.
- **Challenge**: Make the "Deadzone" smaller or larger in `src/cv_controller.py`.
- **Hint**: Change the `deadzone` parameter in the `GestureController` constructor.
...
### 4. Improve the Heuristics
Open `src/heuristics.py`.
- **Challenge**: Add a "weight matrix" heuristic (giving high scores to specific grid positions).
- **Hint**: Define a 4x4 NumPy array of weights and multiply it by the board.

### 1. Create Your Own Strategy
Create a new `.md` file in the `strategies/` folder.
- **Challenge**: Try to beat the "Corner Hugger" strategy.
- **Rule**: You must include a line like `Priority: UP, LEFT, RIGHT, DOWN`.
- **Hint**: The bot will always try the first direction, then the second, and so on until a valid move is found.

### 2. Adjust Simulation Speed
In `src/ui.py`, find the `move_delay` variable in `run_auto`.
- **Challenge**: Make the comparison run faster or slower.
- **Hint**: Decrease the `500` (milliseconds) to `100` for high-speed simulation.

### 3. Modify Tile Spawning
In `src/logic.py`, find the `spawn_tile` method.
- **Challenge**: Change the probability of spawning a `4` instead of a `2`.
- **Hint**: Look for the line `0.1` (which represents a 10% chance).

## 📖 Documentation
- [Architecture Decisions (ADR)](docs/ADR.md)
- [Specifications (SPECS)](docs/SPECS.md)
