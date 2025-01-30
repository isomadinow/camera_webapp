import cv2
import threading
from app.models.camera_model import CameraModel
from app.services.report_service import get_trucks_with_cameras

# Глобальный список активных камер
active_cameras = []

class CameraThread:
    """Класс для управления потоками камер."""
    def __init__(self, camera_index):
        self.camera_index = camera_index
        self.current_frame = None
        self.lock = threading.Lock()
        self.running = True
        self.thread = threading.Thread(target=self._capture_frames, daemon=True)
        self.thread.start()

    def _capture_frames(self):
        cap = cv2.VideoCapture(f'udpsrc port={self.camera_index} \
                           caps="application/x-rtp, media=(string)video, \
                           clock-rate=(int)90000, encoding-name=(string)H264, \
                           payload=(int)96" ! rtph264depay ! \
                           decodebin ! videoconvert ! appsink', cv2.CAP_GSTREAMER)
        if not cap.isOpened():
            print(f"❌ Не удалось открыть камеру {self.camera_index}")
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

    def stop(self):
        self.running = False
        self.thread.join()

def start_cameras_from_reports():
    """Запуск камер на основе данных из reports."""
    global active_cameras
    stop_all_cameras()  # Останавливаем старые камеры перед запуском новых

    trucks_with_cameras = get_trucks_with_cameras()  # Получаем данные
    for truck in trucks_with_cameras:
        name, state_number, front, back, left, right = truck
        print(f"🚛 Запуск камер для {name} ({state_number})")

        active_cameras.append(CameraThread(front))  # Передняя камера
        active_cameras.append(CameraThread(back))   # Задняя камера
        active_cameras.append(CameraThread(left))   # Левая камера
        active_cameras.append(CameraThread(right))  # Правая камера

    return {"message": "Все камеры запущены", "count": len(active_cameras)}

def stop_all_cameras():
    """Останавливает все активные камеры."""
    global active_cameras
    for cam in active_cameras:
        cam.stop()
    active_cameras = []
    print("🛑 Все камеры остановлены")

def get_camera_frames():
    """Возвращает текущие кадры со всех камер."""
    return [cam.get_frame() for cam in active_cameras]
