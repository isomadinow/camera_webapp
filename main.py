import cv2
import threading
from flask import Flask, Response, render_template_string

# Flask-приложение
app = Flask(__name__)

# Глобальная переменная для хранения текущего кадра
current_frame = None
lock = threading.Lock()  # Для синхронизации доступа к кадру

# HTML-шаблон для отображения четырёх потоков
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Многокамерный поток</title>
</head>
<body>
    <h1>Четыре видеопотока с одной камеры</h1>
    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 10px;">
        <div><img src="/video_feed/0" width="100%"></div>
        <div><img src="/video_feed/1" width="100%"></div>
        <div><img src="/video_feed/2" width="100%"></div>
        <div><img src="/video_feed/3" width="100%"></div>
    </div>
</body>
</html>
"""

# Функция для получения кадров с камеры (в отдельном потоке)
def camera_thread():
    global current_frame
    cap = cv2.VideoCapture(0)  # Индекс камеры (одна камера)

    if not cap.isOpened():
        print("Не удалось открыть камеру 0")
        return

    while True:
        success, frame = cap.read()
        if not success:
            print("Ошибка получения кадра с камеры 0")
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
    return render_template_string(HTML_TEMPLATE)

# Роут для видеопотока
@app.route('/video_feed/<int:camera_index>')
def video_feed(camera_index):
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

# Запуск Flask-сервера
if __name__ == '__main__':
    # Запускаем поток для захвата кадров
    threading.Thread(target=camera_thread, daemon=True).start()

    # Запускаем Flask-сервер
    app.run(host='0.0.0.0', port=5000)
