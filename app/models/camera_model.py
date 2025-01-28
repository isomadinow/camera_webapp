import cv2
import threading

class CameraModel:
    def __init__(self, camera_index=0):
        self.camera_index = camera_index
        self.current_frame = None
        self.lock = threading.Lock()
        self.running = True

    def start(self):
        threading.Thread(target=self._capture_frames, daemon=True).start()

    def _capture_frames(self):
        cap = cv2.VideoCapture(self.camera_index)
        if not cap.isOpened():
            print(f"Не удалось открыть камеру {self.camera_index}")
            self.running = False
            return

        while self.running:
            success, frame = cap.read()
            if success:
                with self.lock:
                    self.current_frame = frame
        cap.release()

    def get_frame(self):
        with self.lock:
            return self.current_frame
