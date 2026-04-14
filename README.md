# 2048 Strategy Comparison (Teaching Aid)

A project designed to teach software engineering principles and heuristic design through the classic game of 2048. It features manual play, automated "Strategy Comparison," and high-speed headless simulation.

## 🎓 Learning Objectives
1.  **Engine/UI Separation**: See how the 2048 logic is entirely independent of the `pygame` interface.
2.  **Heuristic Strategies**: Understand how different "priority rules" (heuristics) affect gameplay.
3.  **Search Algorithms**: Explore advanced AI like **Expectimax** and **MCTS**.
4.  **Computer Vision**: Learn how to map real-world movement (hand gestures) to digital controls.
5.  **Steelman Design**: Observe documented tradeoffs between simple rules and complex search trees.

## 🛠 Features
- **Manual Mode**: Standard 2048 gameplay.
- **Auto Mode (Comparison)**: Pits two strategies against each other in real-time.
- **Headless Simulator**: Run thousands of games in seconds to gather statistical data.
- **Aerobic CV Controls**: Move tiles by reaching for the corners of your webcam view.

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

### 3. Aerobic Gesture Controls (Computer Vision)
```bash
# Enable camera controls in manual mode
uv run src/main.py --mode manual --cv
```
- **REACH UP/DOWN/LEFT/RIGHT**: Move your hand to the edges of the camera view.
- *Note: A "Deadzone" box is shown in the center where no moves are triggered.*

### 4. Run Strategy Comparison (GUI)
Compare two different heuristics side-by-side:
```bash
uv run src/main.py --mode auto
```

### 5. Batch Simulation & Evaluation (Headless)
For high-speed statistical testing:
```bash
uv run src/main.py --mode evaluate --games 500 --ai priority
```

## 🤖 Advanced AI Strategies
This project includes advanced search-based AI:
- **Expectimax**: Recursive search with a Transposition Table and heuristics.
- **MCTS**: Random rollouts to identify the most survivable moves.

To run these:
```bash
# Compare Expectimax against MCTS
uv run src/main.py --mode auto --ai expectimax

# Evaluate MCTS performance
uv run src/main.py --mode evaluate --ai mcts --games 50
```

## 🧪 Customization & Exercises

### 1. Create Your Own Heuristic
Create a new `.md` file in `strategies/`.
- **Challenge**: Beat the "Corner Hugger" strategy.
- **Rule**: Include a line like `Priority: UP, LEFT, RIGHT, DOWN`.

### 2. Improve the AI Heuristics
Open `src/heuristics.py`.
- **Challenge**: Add a "weight matrix" heuristic.
- **Hint**: Define a 4x4 NumPy array of weights and multiply it by the board.

### 3. Explore Computer Vision
Read `docs/CV_GUIDE.md` to see how MediaPipe tracks your hands.
- **Challenge**: Change the "Deadzone" size in `src/cv_controller.py`.
- **Hint**: Change the `deadzone` parameter in the `GestureController` constructor.

### 4. Adjust Game Physics
In `src/logic.py`, find `spawn_tile`.
- **Challenge**: Change the probability of spawning a `4`.
- **Hint**: Look for the `0.1` constant (10%).

## 📖 Documentation
- [Architecture Decisions (ADR)](docs/ADR.md)
- [Specifications (SPECS)](docs/SPECS.md)
- [Computer Vision Guide](docs/CV_GUIDE.md)
