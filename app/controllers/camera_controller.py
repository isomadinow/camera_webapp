import cv2
from flask import Blueprint, Response, render_template
from ..models.camera_model import CameraModel

# Создаём Blueprint для маршрутов, связанных с видеопотоками
camera_bp = Blueprint('camera', __name__)

# Инициализация модели камеры
camera_model = CameraModel(0)
camera_model.start()  # Запускаем процесс захвата видео

# Функция для генерации кадров в формате MJPEG
def generate_frames():
    while True:
        frame = camera_model.get_frame()  # Получаем текущий кадр из модели камеры
        if frame is not None:
            _, buffer = cv2.imencode('.jpg', frame)  # Кодируем кадр в JPEG
            frame_bytes = buffer.tobytes()  # Преобразуем в байты
            # Формируем ответ MJPEG (поток изображений)
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

# Маршрут для отображения HTML-страницы с видеопотоками
@camera_bp.route('/')
def index():
    return render_template('index.html')  # Рендеринг шаблона index.html

# Маршрут для получения видеопотока камеры
@camera_bp.route('/video_feed/<int:camera_index>')
def video_feed(camera_index):
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')
    # Возвращаем поток MJPEG клиенту
