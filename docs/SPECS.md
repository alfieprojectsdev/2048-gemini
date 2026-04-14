# Game Specifications: 2048 Strategy Comparison

## Game Mechanics
- **Grid**: 4x4 squares.
- **Initial State**: Two tiles (2 or 4) spawned at random locations.
- **Movement**:
  - Tiles slide in the chosen direction (UP, DOWN, LEFT, RIGHT).
  - Identical adjacent tiles merge into their sum.
  - A new tile (2 or 4) spawns after every successful move.
- **Goal**: Achieve the 2048 tile (or highest possible score).
- **Game Over**: No empty tiles and no possible merges.

## User Interface
- **Manual Mode**:
  - Single board display.
  - Controlled by Arrow keys or WASD.
- **Auto Mode (Comparison)**:
  - Two boards side-by-side.
  - Each board is controlled by a distinct "Strategy" loaded from a `.md` file.
  - Real-time score and high-tile tracking for both.
  - Adjustable simulation speed.

## Strategy Definition (`strategies/*.md`)
- **Format**:
  - A header or metadata section.
  - A field: `Priority: [DIR1], [DIR2], [DIR3], [DIR4]` (e.g., `Priority: DOWN, RIGHT, LEFT, UP`).
- **Logic**: The auto-bot will attempt to move in the first priority direction. If that move is invalid (no tiles move), it will attempt the next priority direction.

## Technical Requirements
- Python 3.x
- `pygame` for rendering and input handling.
- `uv` for dependency management.
