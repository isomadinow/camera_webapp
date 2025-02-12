import cv2
import threading
import time
from app.models.camera_model import CameraModel
from app.models.truck_model import TruckModel
from app.services.report_service import get_trucks_with_cameras

# Глобальный список активных камер
active_cameras = {}

class CameraThread:
    """Класс для управления потоками камер."""
    def __init__(self, camera_index, camera_type):
        self.camera_index = camera_index
        self.camera_type = camera_type
        self.current_frame = None
        self.lock = threading.Lock()
        self.running = True
        self.recording = False
        self.recording_thread = None
        self.video_writer = None
        self.thread = threading.Thread(target=self._capture_frames, daemon=True)
        self.thread.start()

    def _capture_frames(self):
        """Запуск потока для получения видео."""
        print(f"📡 Открываем камеру {self.camera_type} (порт {self.camera_index})...")
        cap = cv2.VideoCapture(
            f'udpsrc port={self.camera_index} '
            f'caps="application/x-rtp, media=(string)video, '
            f'clock-rate=(int)90000, encoding-name=(string)H264, '
            f'payload=(int)96" ! rtph264depay ! '
            f'decodebin ! videoconvert ! appsink',
            cv2.CAP_GSTREAMER
        )

        if not cap.isOpened():
            print(f"❌ Ошибка: Камера {self.camera_type} (порт {self.camera_index}) не открылась!")
            self.running = False
            return

        print(f"✅ Камера {self.camera_type} успешно открыта!")

        while self.running:
            success, frame = cap.read()
            if success:
                with self.lock:
                    self.current_frame = frame
                if self.recording and self.video_writer:
                    self.video_writer.write(frame)
        cap.release()

    def get_frame(self):
        """Возвращает последний кадр камеры."""
        with self.lock:
            return self.current_frame

    def stop(self):
        """Останавливает поток камеры."""
        self.running = False
        self.thread.join()
        self.stop_recording()

    def start_recording(self, output_path, duration_seconds=60):
        """Начинает запись видео с камеры."""
        if self.recording:
            print(f"⚠️ Камера {self.camera_type} уже записывает видео.")
            return

        self.recording = True
        self.recording_thread = threading.Thread(
            target=self._record_video, 
            args=(output_path, duration_seconds),
            daemon=True
        )
        self.recording_thread.start()

    def _record_video(self, output_path, duration_seconds):
        """Внутренний метод для записи видео."""
        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        fps = 20.0
        frame_size = (640, 480)

        self.video_writer = cv2.VideoWriter(output_path, fourcc, fps, frame_size)

        print(f"🎥 Начата запись с камеры {self.camera_type} на {duration_seconds} секунд...")

        start_time = time.time()
        while self.recording and (time.time() - start_time) < duration_seconds:
            time.sleep(0.05)

        self.stop_recording()

    def stop_recording(self):
        """Останавливает запись видео."""
        if self.recording:
            self.recording = False
            if self.video_writer:
                self.video_writer.release()
                self.video_writer = None
            print(f"🛑 Запись с камеры {self.camera_type} остановлена.")


def start_cameras_for_truck(truck_number):
    """Запускает камеры для указанного грузовика."""
    global active_cameras

    # Останавливаем старые камеры перед запуском новых
    stop_all_cameras()

    # Ищем грузовик в базе
    truck = TruckModel.get_by_state_number(truck_number)
    if not truck:
        return {"error": "Грузовик не найден"}

    # Получаем камеры из reports
    truck_data = get_trucks_with_cameras()
    cameras = next((t for t in truck_data if t[1] == int(truck_number)), None)

    if not cameras or len(cameras) < 6:
        return {"error": "Камеры для этого грузовика не найдены или данных недостаточно"}

    _, _, front, back, left, right = cameras

    print(f"🚛 Запуск камер для {truck.Name} ({truck.StateNumber})")

    # Запускаем 4 камеры
    active_cameras = {
        "front": CameraThread(front, "Front"),
        "back": CameraThread(back, "Back"),
        "left": CameraThread(left, "Left"),
        "right": CameraThread(right, "Right"),
    }

    return {"message": f"Камеры для {truck_number} запущены"}

def stop_all_cameras():
    """Останавливает все активные камеры."""
    global active_cameras
    for cam in active_cameras.values():
        cam.stop()
    active_cameras.clear()
    print("🛑 Все камеры остановлены")

def get_camera_frames():
    """Возвращает текущие кадры со всех камер."""
    return {cam_type: cam.get_frame() for cam_type, cam in active_cameras.items()}

# Пример использования записи видео
# active_cameras['front'].start_recording('output_front.avi', duration_seconds=120)
