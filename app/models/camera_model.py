import cv2
import threading

# Класс для работы с камерой
class CameraModel:
    def __init__(self, camera_index=0):
        self.camera_index = camera_index  # Индекс камеры
        self.current_frame = None  # Переменная для хранения текущего кадра
        self.lock = threading.Lock()  # Блокировка для потокобезопасности
        self.running = True  # Флаг для управления потоком

    # Метод для запуска отдельного потока, который захватывает кадры
    def start(self):
        threading.Thread(target=self._capture_frames, daemon=True).start()

    # Внутренний метод, выполняющий захват кадров
    def _capture_frames(self):
        cap = cv2.VideoCapture(self.camera_index)  # Инициализация камеры
        if not cap.isOpened():  # Проверяем, открылась ли камера
            print(f"Не удалось открыть камеру {self.camera_index}")
            self.running = False
            return

        while self.running:  # Захват кадров в цикле
            success, frame = cap.read()
            if success:
                with self.lock:  # Обновляем текущий кадр в потокобезопасной среде
                    self.current_frame = frame
        cap.release()  # Освобождаем камеру после завершения

    # Метод для получения последнего кадра
    def get_frame(self):
        with self.lock:  # Обеспечиваем потокобезопасный доступ
            return self.current_frame
