# Computer Vision (CV) Gesture Controls: Teaching Aid

This guide explains how we integrated real-time hand gesture recognition into the 2048 game using **OpenCV** and **MediaPipe**.

## 🧠 Architectural Overview
The CV integration follows a **Producer-Consumer** pattern to ensure the game remains responsive:
1.  **Producer (`src/cv_controller.py`)**: A separate background thread captures camera frames, detects hand landmarks using MediaPipe, and determines the move direction.
2.  **Consumer (`src/ui.py`)**: The main game loop periodically checks the `GestureController` for any newly triggered moves.

## 🛠 How It Works

### 1. Hand Landmark Detection
MediaPipe provides 21 "landmarks" (points) for each hand. We specifically track **Landmark 9** (the Middle Finger MCP), which acts as the center of the palm.

### 2. Normalization
The camera frame size can vary (e.g., 640x480 or 1280x720). MediaPipe returns **normalized coordinates** (0.0 to 1.0), where:
- `(0.0, 0.0)` is the top-left corner.
- `(1.0, 1.0)` is the bottom-right corner.
- `(0.5, 0.5)` is the center.

### 3. The "Deadzone" Heuristic
To prevent the game from moving constantly, we define a **Deadzone** in the center of the screen (default: `0.3`).
- If the hand's `x` or `y` is within `0.5 ± 0.3`, no move is triggered.
- A move is only triggered when the hand "reaches" outside this box.

### 4. Debouncing & Throttling
Unlike a keyboard press, a hand stays in a "reaching" position for many frames.
- **Throttling**: We use a `throttle` (default: `0.5s`) to ensure the AI doesn't process 30 moves per second just because your hand is raised.

## 🏃 Aerobic Exercise Mode
By making the deadzone large and requiring the player to reach for the edges of the camera's field of view, the game becomes physically active.
- **UP**: Reach high above your head.
- **DOWN**: Squat or reach low.
- **LEFT/RIGHT**: Stretch wide to either side.

## 🎓 Exercises for Students
1.  **Change the Landmark**: Modify `src/cv_controller.py` to track the **Index Finger Tip** (Landmark 8) instead of the palm. Does it feel more precise?
2.  **Visual Feedback**: Add a "meter" in the OpenCV window that shows how close the hand is to triggering a move.
3.  **Two-Handed Play**: Modify the controller to require *two* hands in specific positions for "Combo" moves (e.g., both hands UP to clear a row).
