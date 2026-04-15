# Computer Vision (CV) Gesture Controls: Teaching Aid

This guide explains how we integrated real-time hand gesture recognition into 2048 using **OpenCV** and the **MediaPipe Tasks API**.

## 🧠 Architectural Overview
The CV integration follows a **Producer-Consumer** pattern to ensure the game remains responsive:
1.  **Producer (`src/cv_controller.py`)**: A background thread using the **MediaPipe Tasks (Vision)** API (`HandLandmarker`) to process camera frames.
2.  **Consumer (`src/ui.py`)**: The main game loop checks for triggered moves without waiting for the camera.

## 🛠 How It Works

### 1. Hand Landmarker Model
We use a pre-trained `.task` model from MediaPipe. The project automatically downloads this if missing.

### 2. Tracking Landmarks
We track **Landmark 9** (Middle Finger MCP), which represents the center of the palm. This provides a stable point for overall hand movement.

### 3. Normalization & Deadzones
- Camera coordinates (0.0 to 1.0) are used for calculation.
- **Center (0.5, 0.5)** is the resting position.
- A **Deadzone (e.g., 0.25)** box in the middle prevents unintended moves.

### 4. Debouncing & Throttling
Unlike a keyboard press, a hand stays in a "reaching" position for many frames.
- **Throttling**: We use a `throttle` (default: `0.4s`) to ensure the AI doesn't process dozens of moves per second.

## 🏋️ Aerobic Exercise Mode
By making the deadzone large and requiring the player to reach for the corners of the camera's view, the game becomes physically active.
- **UP**: Reach high above your head.
- **DOWN**: Squat or reach low.
- **LEFT/RIGHT**: Stretch wide to either side.

## 🎓 Exercises for Students
1.  **Change the Landmark**: Modify `src/cv_controller.py` to track the **Index Finger Tip** (Landmark 8).
2.  **Adaptive Deadzone**: Implement a system where the deadzone shrinks as the player's score increases, requiring more precise movement.
3.  **Visual Feedback**: Modify the OpenCV window to show a "charging bar" while a hand is in the trigger zone.
