from flask import Blueprint, jsonify, request, Response
from app.services.camera_service import (
    start_cameras_for_truck,
    stop_all_cameras,
    get_camera_frames
)
import cv2
import time
import os

camera_bp = Blueprint("camera", __name__)

video_writers = {}
VIDEO_DIR = "recordings"
os.makedirs(VIDEO_DIR, exist_ok=True)

@camera_bp.route("/api/start_cameras", methods=["POST"])
def start_cameras():
    data = request.json
    truck_number = data.get("truck_number")

    if not truck_number:
        return jsonify({"error": "Не указан номер грузовика"}), 400

    result = start_cameras_for_truck(truck_number)
    return jsonify(result)

@camera_bp.route("/api/stop_cameras", methods=["POST"])
def stop_cameras():
    stop_all_cameras()
    return jsonify({"message": "Все камеры остановлены"})

@camera_bp.route("/api/start_recording/<string:camera_type>", methods=["POST"])
def start_recording(camera_type):
    """
    Метод для начала записи видео для определенной камеры.
    """
    if camera_type not in ['front', 'back', 'left', 'right']:
        return jsonify({"error": "Неверный тип камеры"}), 400

    # Проверяем, если запись уже идет
    if camera_type in video_writers and video_writers[camera_type] is not None:
        return jsonify({"error": f"Запись для {camera_type} уже идет"}), 400

    # Получаем кадры с камеры
    frame = get_camera_frames().get(camera_type)
    if frame is None:
        return jsonify({"error": f"Не удалось получить кадры с {camera_type} камеры"}), 400

    # Создаем объект VideoWriter для записи видео
    video_path = os.path.join(VIDEO_DIR, f"{camera_type}_recording.mp4")
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # Используем кодек для MP4
    fps = 20  # Частота кадров
    height, width, _ = frame.shape
    video_writer = cv2.VideoWriter(video_path, fourcc, fps, (width, height))

    # Сохраняем объект VideoWriter в словарь
    video_writers[camera_type] = video_writer

    return jsonify({"message": f"Запись видео для {camera_type} началась"})


@camera_bp.route("/api/stop_recording/<string:camera_type>", methods=["POST"])
def stop_recording(camera_type):
    """
    Метод для остановки записи видео для определенной камеры.
    """
    if camera_type not in video_writers or video_writers[camera_type] is None:
        return jsonify({"error": f"Запись для {camera_type} не была запущена"}), 400

    video_writer = video_writers[camera_type]
    video_writer.release()  # Останавливаем запись
    video_writers[camera_type] = None  # Обнуляем объект VideoWriter

    return jsonify({"message": f"Запись видео для {camera_type} остановлена"})


def gen_frames(camera_type):
    while True:
        frames_dict = get_camera_frames()
        frame = frames_dict.get(camera_type)  # "front", "back", etc.

        if frame is not None:
            ret, buffer = cv2.imencode('.jpg', frame)
            if not ret:
                time.sleep(0.05)
                continue
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + buffer.tobytes() + b'\r\n')
        else:
            time.sleep(0.05)

@camera_bp.route("/video_feed/<string:camera_type>")
def video_feed(camera_type):
    """
    /video_feed/front
    /video_feed/back
    /video_feed/left
    /video_feed/right
    """
    return Response(gen_frames(camera_type),
                    mimetype="multipart/x-mixed-replace; boundary=frame")
