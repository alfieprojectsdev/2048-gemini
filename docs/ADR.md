# Architecture Decision Records (ADR)

## ADR 1: Game Engine Design

### Status
Accepted

### Context
We need a 2048 game engine that is decoupled from any UI to allow for headless simulation of different strategies.

### Decision
We will use a class-based `Board` in `src/logic.py` with methods for each movement direction (UP, DOWN, LEFT, RIGHT).

### Rationale
- **Testability**: The engine can be tested without `pygame`.
- **Modularity**: Allows easy integration of an "Auto Mode" that can simulate thousands of moves per second for strategy evaluation.

### Steelman Design Tradeoffs
- **Against Matrix-Based Operations (NumPy)**: While NumPy can handle grid shifts and merges very quickly, it adds a large dependency. For a 4x4 grid, standard Python lists are more than fast enough and more approachable for teaching.
- **Against Functional Programming**: A purely functional approach (returning a new board for every move) is elegant, but might be harder for beginners to grasp compared to an object-oriented `Board` that maintains its own state.

---

## ADR 2: Strategy Definition and Persistence

### Status
Accepted

### Context
How should "Auto Mode" strategies be defined and stored for persistence and ease of modification by students?

### Decision
Strategies will be stored as `.md` files in a `strategies/` directory. Each file will contain a `Priority` field (e.g., `Priority: DOWN, RIGHT, LEFT, UP`).

### Rationale
- **Readability**: Students can read the reasoning behind a strategy in plain English within the same file as the rules.
- **Ease of Modification**: Changing a strategy is as simple as reordering a list of directions in a text file.

### Steelman Design Tradeoffs
- **Against Scripted Python Strategies**: While writing strategies in Python allows for more complex logic (e.g., "move LEFT only if no merge is possible DOWN"), it requires students to learn the API. Markdown-based priority lists are a lower barrier to entry for the first lesson on heuristics.
- **Against JSON/YAML**: Markdown is more user-friendly for documentation. We can parse the necessary rules from it while keeping the "human-first" format.

---

## ADR 3: 1v1 Comparison Loop

### Status
Accepted

### Context
How to demonstrate "optimal" play?

### Decision
A real-time side-by-side comparison of two different strategies running concurrently.

### Rationale
- **Visual Impact**: Seeing one strategy struggle while another thrives is a powerful teaching moment.
- **Competitive Element**: Students can "pit" their custom strategies against each other.

### Steelman Design Tradeoffs
- **Against Sequential Testing**: Running one strategy and then another is easier to implement but less engaging. The concurrent display emphasizes the "real-time" decision-making process.

---

## ADR 5: Headless Simulation and Automated Generation

### Status
Accepted

### Context
To truly compare strategies, we need statistically significant data (averaging results over hundreds of games). The GUI is too slow for this.

### Decision
Implement a headless `Simulator` and a `generate` mode to produce random heuristic permutations.

### Rationale
- **Data-Driven Evaluation**: Provides an objective way to see which strategy is actually "best" beyond a single lucky game.
- **Exploratory Learning**: Allowing students to generate and test all 24 possible move-priority permutations ($4!$) encourages them to look for patterns in the results.

### Steelman Design Tradeoffs
- **Against High-Performance Multiprocessing**: While we could use `multiprocessing` to speed up simulations even further, the single-threaded speed of the logic-only engine is already sufficient for hundreds of games per second. Keeping it simple makes the code more readable for teaching.
