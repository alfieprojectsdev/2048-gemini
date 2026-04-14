import cv2
import mediapipe as mp
import threading
import time
from collections import deque

class GestureController:
    """
    A controller that uses the camera to detect hand positions and translate
    them into game moves (UP, DOWN, LEFT, RIGHT).
    Designed to be 'aerobic' - you have to reach for the edges of the camera view.
    """
    def __init__(self, deadzone=0.3, throttle=0.5):
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=1,
            min_detection_confidence=0.7,
            min_tracking_confidence=0.5
        )
        self.mp_draw = mp.solutions.drawing_utils
        self.cap = cv2.VideoCapture(0)
        
        self.deadzone = deadzone # Area in center where no move is triggered
        self.throttle = throttle # Minimum time between moves (seconds)
        self.last_move_time = 0
        self.latest_move = None
        self.running = False
        self.thread = None
        
        # For visualization in the CV window
        self.current_pos = (0.5, 0.5)
        self.is_hand_present = False

    def start(self):
        self.running = True
        self.thread = threading.Thread(target=self._run_loop, daemon=True)
        self.thread.start()

    def stop(self):
        self.running = False
        if self.thread:
            self.thread.join()
        self.cap.release()

    def _run_loop(self):
        while self.running:
            success, image = self.cap.read()
            if not success:
                continue

            # Flip the image horizontally for a mirror effect
            image = cv2.flip(image, 1)
            h, w, c = image.shape
            
            # Convert to RGB for MediaPipe
            rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            results = self.hands.process(rgb_image)

            move_triggered = None
            if results.multi_hand_landmarks:
                self.is_hand_present = True
                # Get the first hand detected
                hand_landmarks = results.multi_hand_landmarks[0]
                
                # Use the wrist (landmark 0) or palm center for overall position
                # Actually, the tip of the middle finger (landmark 12) or index (8) 
                # might feel more intentional for "reaching".
                landmark = hand_landmarks.landmark[9] # Middle finger MCP (palm center-ish)
                x, y = landmark.x, landmark.y
                self.current_pos = (x, y)

                # Draw landmarks for feedback
                self.mp_draw.draw_landmarks(image, hand_landmarks, self.mp_hands.HAND_CONNECTIONS)

                # Logic: Center of screen is (0.5, 0.5)
                # If x < (0.5 - deadzone), move LEFT
                # If x > (0.5 + deadzone), move RIGHT
                # If y < (0.5 - deadzone), move UP (y is 0 at top)
                # If y > (0.5 + deadzone), move DOWN
                
                now = time.time()
                if now - self.last_move_time > self.throttle:
                    dx = x - 0.5
                    dy = y - 0.5
                    
                    if abs(dx) > abs(dy):
                        if dx < -self.deadzone:
                            move_triggered = "LEFT"
                        elif dx > self.deadzone:
                            move_triggered = "RIGHT"
                    else:
                        if dy < -self.deadzone:
                            move_triggered = "UP"
                        elif dy > self.deadzone:
                            move_triggered = "DOWN"
                    
                    if move_triggered:
                        self.latest_move = move_triggered
                        self.last_move_time = now
            else:
                self.is_hand_present = False

            # Draw "Deadzone" box and directions for the teaching aid
            self._draw_overlay(image)
            
            cv2.imshow('2048 CV Control', image)
            if cv2.waitKey(1) & 0xFF == 27:
                break

    def _draw_overlay(self, image):
        h, w, _ = image.shape
        # Draw deadzone
        start_pt = (int((0.5 - self.deadzone) * w), int((0.5 - self.deadzone) * h))
        end_pt = (int((0.5 + self.deadzone) * w), int((0.5 + self.deadzone) * h))
        cv2.rectangle(image, start_pt, end_pt, (0, 255, 0), 2)
        
        # Add labels
        cv2.putText(image, "REACH UP", (int(w/2) - 40, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 2)
        cv2.putText(image, "REACH DOWN", (int(w/2) - 60, h - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 2)
        cv2.putText(image, "LEFT", (10, int(h/2)), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 2)
        cv2.putText(image, "RIGHT", (w - 80, int(h/2)), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 2)

    def get_move(self):
        """Returns the latest move and clears it."""
        move = self.latest_move
        self.latest_move = None
        return move
