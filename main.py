import cv2
import threading
from flask import Flask, Response

# Flask-приложение
app = Flask(__name__)

# Глобальная переменная для хранения текущего кадра
current_frame = None
lock = threading.Lock()  # Для синхронизации доступа к кадру

# Функция для получения кадров с камеры (в отдельном потоке)
def camera_thread(camera_index):
    global current_frame
    cap = cv2.VideoCapture(camera_index)  # Индекс камеры

    if not cap.isOpened():
        print(f"Не удалось открыть камеру {camera_index}")
        return

    while True:
        success, frame = cap.read()
        if not success:
            print(f"Ошибка получения кадра с камеры {camera_index}")
            break

        # Обновляем текущий кадр
        with lock:
            current_frame = frame

    cap.release()

# Функция для отправки кадров клиентам
def generate_frames():
    global current_frame
    while True:
        with lock:
            if current_frame is None:
                continue
            # Кодируем текущий кадр в JPEG
            _, buffer = cv2.imencode('.jpg', current_frame)
            frame = buffer.tobytes()

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

# Роут для главной страницы
@app.route('/')
def index():
    return "Перейдите на <a href='/video_feed'>/video_feed</a> для просмотра потока."

# Роут для видеопотока
@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

# Запуск Flask-сервера
if __name__ == '__main__':
    # Запускаем поток для захвата кадров
    camera_index = 0  # Индекс камеры
    threading.Thread(target=camera_thread, args=(camera_index,), daemon=True).start()

    # Запускаем Flask-сервер
    app.run(host='0.0.0.0', port=5000)
