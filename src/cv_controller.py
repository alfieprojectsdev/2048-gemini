import cv2
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
import threading
import time
import os
import requests
import queue

class GestureController:
    """
    A controller that uses the camera to detect hand positions and translate
    them into game moves (UP, DOWN, LEFT, RIGHT).
    Uses the modern MediaPipe Tasks API.
    """
    def __init__(self, deadzone=0.25, throttle=0.4):
        self.model_path = 'hand_landmarker.task'
        self._ensure_model_exists()
        
        base_options = python.BaseOptions(model_asset_path=self.model_path)
        options = vision.HandLandmarkerOptions(
            base_options=base_options,
            running_mode=vision.RunningMode.VIDEO,
            num_hands=1
        )
        self.detector = vision.HandLandmarker.create_from_options(options)
        
        self.cap = cv2.VideoCapture(0)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)
        self.deadzone = deadzone
        self.throttle = throttle
        self.last_move_time = 0
        self.move_queue = queue.Queue(maxsize=2)
        self.stop_event = threading.Event()
        self.thread = None
        
        self.current_pos = (0.5, 0.5)
        self.is_hand_present = False

    def _ensure_model_exists(self):
        """Downloads the MediaPipe hand landmarker model if missing."""
        if not os.path.exists(self.model_path):
            print(f"Downloading MediaPipe model to {self.model_path}...")
            url = "https://storage.googleapis.com/mediapipe-models/hand_landmarker/hand_landmarker/float16/1/hand_landmarker.task"
            try:
                response = requests.get(url, timeout=10)
                response.raise_for_status()
                with open(self.model_path, "wb") as f:
                    f.write(response.content)
            except Exception as e:
                if os.path.exists(self.model_path):
                    os.remove(self.model_path)
                print(f"FAILED to download MediaPipe model: {e}")
                print("Please download it manually and place it in the project root.")
                raise

    def start(self):
        self.stop_event.clear()
        self.thread = threading.Thread(target=self._run_loop, daemon=True)
        self.thread.start()

    def stop(self):
        self.stop_event.set()
        if self.thread:
            self.thread.join(timeout=1.0)
        if hasattr(self, 'detector'):
            self.detector.close()
        self.cap.release()
        cv2.destroyAllWindows()

    def _run_loop(self):
        while not self.stop_event.is_set():
            success, frame = self.cap.read()
            if not success:
                time.sleep(0.01)
                continue

            frame = cv2.flip(frame, 1)
            mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=frame)
            timestamp_ms = int(time.time() * 1000)
            
            # Perform detection
            result = self.detector.detect_for_video(mp_image, timestamp_ms)

            move_triggered = None
            if result.hand_landmarks:
                self.is_hand_present = True
                # Landmark 9 is middle finger MCP
                landmark = result.hand_landmarks[0][9]
                x, y = landmark.x, landmark.y
                self.current_pos = (x, y)

                now = time.time()
                if now - self.last_move_time > self.throttle:
                    dx = x - 0.5
                    dy = y - 0.5
                    
                    if abs(dx) > abs(dy):
                        if dx < -self.deadzone: move_triggered = "LEFT"
                        elif dx > self.deadzone: move_triggered = "RIGHT"
                    else:
                        if dy < -self.deadzone: move_triggered = "UP"
                        elif dy > self.deadzone: move_triggered = "DOWN"
                    
                    if move_triggered:
                        try:
                            self.move_queue.put_nowait(move_triggered)
                        except queue.Full:
                            pass
                        self.last_move_time = now
            else:
                self.is_hand_present = False

            self._draw_overlay(frame)
            cv2.imshow('2048 CV Control', frame)
            if cv2.waitKey(1) & 0xFF == 27:
                break

    def _draw_overlay(self, image):
        h, w, _ = image.shape
        # Draw deadzone box
        s_pt = (int((0.5 - self.deadzone) * w), int((0.5 - self.deadzone) * h))
        e_pt = (int((0.5 + self.deadzone) * w), int((0.5 + self.deadzone) * h))
        cv2.rectangle(image, s_pt, e_pt, (0, 255, 0), 2)
        
        # Draw current position dot if hand present
        if self.is_hand_present:
            cx, cy = int(self.current_pos[0] * w), int(self.current_pos[1] * h)
            cv2.circle(image, (cx, cy), 10, (0, 0, 255), -1)

        cv2.putText(image, "REACH UP", (int(w/2) - 40, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 2)
        cv2.putText(image, "REACH DOWN", (int(w/2) - 60, h - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 2)
        cv2.putText(image, "LEFT", (10, int(h/2)), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 2)
        cv2.putText(image, "RIGHT", (w - 80, int(h/2)), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 2)

    def get_move(self):
        try:
            return self.move_queue.get_nowait()
        except queue.Empty:
            return None
