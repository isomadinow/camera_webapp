import cv2
import threading

class CameraManager:
    cameras = {}
    locks = {}

    @classmethod
    def initialize(cls, camera_indices):
        for index in camera_indices:
            cls.cameras[index] = None
            cls.locks[index] = threading.Lock()
            threading.Thread(target=cls._camera_thread, args=(index,), daemon=True).start()

    @classmethod
    def _camera_thread(cls, camera_index):
        cap = cv2.VideoCapture(camera_index)
        if not cap.isOpened():
            print(f"Не удалось открыть камеру {camera_index}")
            return

        while True:
            success, frame = cap.read()
            if not success:
                print(f"Ошибка получения кадра с камеры {camera_index}")
                break

            with cls.locks[camera_index]:
                cls.cameras[camera_index] = frame

        cap.release()

    @classmethod
    def get_frame(cls, camera_index):
        with cls.locks[camera_index]:
            frame = cls.cameras.get(camera_index, None)
            if frame is not None:
                _, buffer = cv2.imencode('.jpg', frame)
                return buffer.tobytes()
        return None
