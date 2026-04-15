# Game Specifications: 2048 Strategy Comparison

## Game Mechanics
- **Grid**: 4x4.
- **Goal**: Reach 2048 (or highest score).
- **Movement**: Slide & merge identical adjacent tiles.
- **Spawning**: Random 2 (90%) or 4 (10%) spawned after each move.

## Modes of Operation
1.  **Manual Mode (`--mode manual`)**: Arrow keys or WASD.
2.  **Manual CV Mode (`--mode manual --cv`)**: Aerobic gesture controls via webcam.
3.  **Auto Mode (`--mode auto`)**: 1v1 split-screen real-time comparison.
4.  **Evaluate Mode (`--mode evaluate`)**: Headless batch simulation with statistical output.
5.  **Generate Mode (`--mode generate`)**: Automated creation of random heuristic `.md` files.

## AI Engines
- **Priority Heuristic**: Tries directions in a fixed sequence from a `.md` file.
- **Expectimax Search**: Recursive tree search maximizing expected board value.
- **MCTS**: Monte Carlo Tree Search using random "rollouts" to calculate survival.

## Heuristics (Board Evaluation)
Boards are scored based on:
- **Monotonicity**: Keeping tiles sorted in a direction.
- **Smoothness**: Minimizing differences between neighbors.
- **Empty Space**: Maintaining maneuverability.
- **Max Tile Positioning**: Keeping the largest tile in a corner.

## CV Gesture Controls
- **Up/Down/Left/Right**: Triggered by reaching outside a **Deadzone (0.25)** in the camera view.
- **Throttling**: 0.4s between gesture-based moves.
- **Tooling**: OpenCV + MediaPipe Tasks API.

## Technical Stack
- **Language**: Python 3.x
- **UI/Input**: Pygame
- **CV Engine**: MediaPipe Tasks API, OpenCV
- **Dependency Management**: `uv`
- **Logic Matrix Handling**: NumPy
