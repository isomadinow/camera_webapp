import cv2
import threading
import time
from flask import Flask, Response

app = Flask(__name__)

# Словарь, где ключ: порт (int), значение: объект "камера" (CameraThread).
active_cameras = {
    2001: None,
    2002: None,
    2003: None,
    2004: None,
}

class CameraThread:
    """Класс потока для чтения видеопотока через GStreamer/OpenCV."""
    def __init__(self, port):
        self.port = port
        self.current_frame = None
        self.lock = threading.Lock()
        self.running = True
        
        # GStreamer pipeline – обязательно caps, иначе H264‐поток может не распознаться
        pipeline = (
            f'udpsrc port={self.port} '
            'caps="application/x-rtp, media=(string)video, clock-rate=(int)90000, '
            'encoding-name=(string)H264, payload=(int)96" ! '
            'rtph264depay ! decodebin ! videoconvert ! appsink'
        )
        self.cap = cv2.VideoCapture(pipeline, cv2.CAP_GSTREAMER)
        
        self.thread = threading.Thread(target=self._capture_loop, daemon=True)
        self.thread.start()

    def _capture_loop(self):
        if not self.cap.isOpened():
            print(f"[{self.port}] Не удалось открыть поток!")
            self.running = False
            return
        print(f"[{self.port}] Камера успешно открыта!")

        while self.running:
            success, frame = self.cap.read()
            if success:
                with self.lock:
                    self.current_frame = frame
            else:
                time.sleep(0.05)  # небольшой пауз чтобы не сжигать CPU

        self.cap.release()
        print(f"[{self.port}] Камера остановлена.")

    def get_frame(self):
        """Вернуть последний успешно считанный кадр."""
        with self.lock:
            return self.current_frame

    def stop(self):
        """Остановить поток чтения."""
        self.running = False
        self.thread.join()


def ensure_camera_started(port):
    """Убедиться, что для данного порта запущен поток CameraThread."""
    if active_cameras[port] is None:
        active_cameras[port] = CameraThread(port)


def generate_frames_for_port(port):
    """Генератор, который в бесконечном цикле отдаёт JPEG‐кадры для указанного порта."""
    # Убедимся, что поток для порта запущен
    ensure_camera_started(port)

    while True:
        camera_thread = active_cameras[port]
        if camera_thread is None:
            # если почему-то нету, подождём
            time.sleep(0.1)
            continue
        
        frame = camera_thread.get_frame()
        if frame is not None:
            # Кодируем в JPEG
            ret, buffer = cv2.imencode('.jpg', frame)
            if not ret:
                time.sleep(0.05)
                continue
            # Отправляем «кусочками» (multipart/x-mixed-replace)
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + buffer.tobytes() + b'\r\n')
        else:
            # Если кадра нет, передышка
            time.sleep(0.05)


@app.route("/")
def index():
    """
    Просто выдаём HTML, где 4 <img> на 4 порта.
    Вы можете добавить любые стили, чтобы расположить по сетке.
    """
    html = """
    <html>
    <head><title>4 камеры через GStreamer</title></head>
    <body>
        <h1>Видеопотоки:</h1>
        <div style="display: flex; flex-wrap: wrap;">
          <div>
            <h2>Порт 2001</h2>
            <img src="/video_feed/2001" width="320" height="240" />
          </div>
          <div>
            <h2>Порт 2002</h2>
            <img src="/video_feed/2002" width="320" height="240" />
          </div>
          <div>
            <h2>Порт 2003</h2>
            <img src="/video_feed/2003" width="320" height="240" />
          </div>
          <div>
            <h2>Порт 2004</h2>
            <img src="/video_feed/2004" width="320" height="240" />
          </div>
        </div>
    </body>
    </html>
    """
    return html


@app.route("/video_feed/<int:port>")
def video_feed(port):
    """
    Роут для MJPEG‐потока с конкретного порта, например:
      /video_feed/2001
    """
    return Response(generate_frames_for_port(port),
                    mimetype="multipart/x-mixed-replace; boundary=frame")


@app.route("/stop/<int:port>")
def stop_camera(port):
    """Пример: ручной останов камеры по порту (если нужно)."""
    if active_cameras[port] is not None:
        active_cameras[port].stop()
        active_cameras[port] = None
    return f"Камера на порту {port} остановлена"


if __name__ == "__main__":
    # Запускаем Flask на 0.0.0.0:5000
    app.run(host="0.0.0.0", port=5000, debug=True)
