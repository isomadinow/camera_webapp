import sys
import os
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
opencv_path = os.path.join(BASE_DIR, "../../opencv/build/lib/python3")
sys.path.insert(0, opencv_path)

import cv2
import threading
from app.models.camera_model import CameraModel
from app.models.truck_model import TruckModel
from app.services.report_service import get_trucks_with_cameras

active_cameras = {}

class CameraThread:
    """Класс для управления потоками камер."""
    def __init__(self, camera_index, camera_type):
        self.camera_index = camera_index  # числовой порт
        self.camera_type = camera_type
        self.current_frame = None
        self.lock = threading.Lock()
        self.running = True
        self.thread = threading.Thread(target=self._capture_frames, daemon=True)
        self.thread.start()

    def _capture_frames(self):
        pipeline = (
            f'udpsrc port={self.camera_index} '
            'caps="application/x-rtp, media=(string)video, clock-rate=(int)90000, '
            'encoding-name=(string)H264, payload=(int)96" ! '
            'rtph264depay ! decodebin ! videoconvert ! appsink sync=false'
        )
        print(f"📡 Открываем камеру {self.camera_type} (порт {self.camera_index})...")
        cap = cv2.VideoCapture(pipeline, cv2.CAP_GSTREAMER)

        if not cap.isOpened():
            print(f"❌ Ошибка: Камера {self.camera_type} (порт {self.camera_index}) не открылась!")
            self.running = False
            return

        print(f"✅ Камера {self.camera_type} (порт {self.camera_index}) успешно открыта!")

        while self.running:
            success, frame = cap.read()
            if success:
                with self.lock:
                    self.current_frame = frame
            else:
                # небольшая пауза, чтобы не грузить CPU
                cv2.waitKey(10)

        cap.release()
        print(f"🛑 Камера {self.camera_type} (порт {self.camera_index}) остановлена.")

    def get_frame(self):
        with self.lock:
            return self.current_frame

    def stop(self):
        self.running = False
        self.thread.join()

def start_cameras_for_truck(truck_number):
    """Запускает камеры для указанного грузовика (берёт порты из базы/отчётов)."""
    global active_cameras
    stop_all_cameras()

    if truck_number not in ["10", "11"]:
        truck = TruckModel.get_by_state_number(truck_number)
        if not truck:
            return {"error": "Грузовик не найден"}

    # Предположим, get_trucks_with_cameras() -> [id, stateNumber, front_port, back_port, left_port, right_port]
    truck_data = get_trucks_with_cameras()
    cameras = next((t for t in truck_data if t[1] == int(truck_number)), None)

    if not cameras or len(cameras) < 6:
        return {"error": "Камеры/порты для этого грузовика не найдены или недостаточно данных."}

    _, _, front_port, back_port, left_port, right_port = cameras

    print(f"🚛 Запуск камер: front={front_port}, back={back_port}, left={left_port}, right={right_port}")

    # Запускаем 4 потока CameraThread
    active_cameras = {
        "front": CameraThread(front_port, "Front"),
        "back":  CameraThread(back_port,  "Back"),
        "left":  CameraThread(left_port,  "Left"),
        "right": CameraThread(right_port, "Right"),
    }

    return {"message": f"Камеры для {truck_number} запущены"}

def stop_all_cameras():
    global active_cameras
    for cam in active_cameras.values():
        cam.stop()
    active_cameras.clear()
    print("🛑 Все камеры остановлены")

def get_camera_frames():
    return {cam_type: cam.get_frame() for cam_type, cam in active_cameras.items()}
