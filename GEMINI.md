# Project Overview: 2048 Strategy Comparison

This project is an educational platform designed to teach software engineering principles, heuristic design, and AI search algorithms using the game 2048. It features a decoupled game engine, multiple AI strategies (Expectimax, MCTS), and an aerobic Computer Vision (CV) control mode.

## 🛠 Main Technologies
- **Language**: Python 3.11+
- **Dependency Management**: [uv](https://github.com/astral-sh/uv)
- **UI & Graphics**: `pygame`
- **Computer Vision**: `mediapipe` (Tasks API), `opencv-python`
- **Data Handling**: `numpy`
- **Testing**: `unittest`

## 🏗 Architecture
The project follows a decoupled architecture to support both GUI and headless simulation:
- `src/logic.py`: Core `Game2048` engine, independent of any UI.
- `src/ui.py`: Pygame implementation for Manual and Auto (1v1 Comparison) modes.
- `src/cv_controller.py`: Background thread for processing webcam frames and mapping hand landmarks to game moves.
- `src/strategies.py`: Implements various AI strategies, including `ExpectimaxStrategy`, `MCTSStrategy`, and `PriorityStrategy` (loaded from Markdown files).
- `src/heuristics.py`: Contains board evaluation logic (monotonicity, smoothness, empty space, corner positioning).
- `src/simulator.py`: Logic for running high-speed headless simulations.

## 🚀 Key Commands

### Setup
```bash
uv sync
```

### Running the Application
- **Manual Mode**: `uv run src/main.py --mode manual`
- **Gesture Controls**: `uv run src/main.py --mode manual --cv`
- **1v1 AI Comparison**: `uv run src/main.py --mode auto --ai [priority|expectimax|mcts]`
- **Headless Evaluation**: `uv run src/main.py --mode evaluate --games 100 --ai expectimax`
- **Generate Random Strategies**: `uv run src/main.py --mode generate --count 5`

### Testing
```bash
python3 -m unittest discover tests
```

## 📝 Development Conventions

### Coding Style
- **Engine Decoupling**: Keep game logic in `src/logic.py` completely free of UI or CV dependencies.
- **Strategy Pattern**: New AI strategies should inherit from the base class in `src/strategies.py`.
- **Heuristics**: Add new board evaluation functions to `src/heuristics.py` to keep search logic clean.

### Strategy Definitions
- Simple heuristic-based strategies are stored as `.md` files in the `strategies/` directory.
- They must include a line like `Priority: UP, LEFT, RIGHT, DOWN` which the loader parses.

### Testing Practices
- Use `unittest` for core logic verification.
- Add new tests in `tests/` for any changes to `src/logic.py`.
- For AI/Simulation changes, use `--mode evaluate` to verify statistical performance hasn't regressed.

### Documentation
- Architectural decisions are recorded in `docs/ADR.md`.
- Technical specifications are in `docs/SPECS.md`.
- CV-specific guidance is available in `docs/CV_GUIDE.md`.
