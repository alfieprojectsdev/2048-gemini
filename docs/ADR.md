# Architecture Decision Records (ADR)

## ADR 1: Game Engine Design
**Status**: Accepted  
**Context**: Decoupled engine needed for headless simulation.  
**Decision**: Class-based `Board` in `src/logic.py`.  
**Steelman**: NumPy adds speed for large matrices but standard lists are better for teaching 4x4 logic.

## ADR 2: Strategy Persistence
**Status**: Accepted  
**Context**: How to store student-created heuristics?  
**Decision**: Markdown files with `Priority:` fields in `strategies/`.  
**Steelman**: Python scripts are more powerful but Markdown is a lower barrier for beginners.

## ADR 3: 1v1 Comparison Loop
**Status**: Accepted  
**Context**: Demonstrating "optimal" play.  
**Decision**: Real-time concurrent side-by-side boards.

## ADR 4: Advanced AI Search (Expectimax & MCTS)
**Status**: Accepted  
**Context**: Moving beyond simple heuristics to optimal search.  
**Decision**: Implement **Expectimax** (for random environments) and **MCTS** (for survival probability).  
**Steelman**: Deep Reinforcement Learning (DQN) is "flashier" but algorithmic search is better for teaching state-space exploration and tree pruning.

## ADR 5: Headless Simulation & Progress Reporting
**Status**: Accepted  
**Context**: Statistical significance requires 100+ games.  
**Decision**: Implement a headless `Simulator` with a CLI progress bar.

## ADR 6: Computer Vision (CV) Gesture Controls
**Status**: Accepted  
**Context**: Integrated aerobic exercise and CV education.  
**Decision**: Use **MediaPipe Tasks API** with a background thread (Producer-Consumer).  
**Steelman**: Custom CNNs for gestures are educational but MediaPipe is robust and allows students to focus on *mapping* landmarks to game logic rather than training models.
