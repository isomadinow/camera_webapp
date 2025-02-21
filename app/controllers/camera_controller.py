from flask import Blueprint, jsonify, request, Response
from app.services.camera_service import (
    start_cameras_for_truck,
    stop_all_cameras,
    get_camera_frames
)
import cv2
import time
import os
import datetime
import threading

camera_bp = Blueprint("camera", __name__)

video_writers = {}
recording_threads = {}
VIDEO_DIR = "./recordings"
os.makedirs(VIDEO_DIR, exist_ok=True)

# --- Запуск камер для грузовика ---
@camera_bp.route("/api/start_cameras", methods=["POST"])
def start_cameras():
    data = request.json
    truck_number = data.get("truck_number")

    if not truck_number:
        return jsonify({"error": "Не указан номер грузовика"}), 400

    result = start_cameras_for_truck(truck_number)
    return jsonify(result)

# --- Остановка всех камер ---
@camera_bp.route("/api/stop_cameras", methods=["POST"])
def stop_cameras():
    stop_all_cameras()
    return jsonify({"message": "Все камеры остановлены"})

# --- Генерация видеопотока ---
def gen_frames(camera_type):
    while True:
        frames_dict = get_camera_frames()
        frame = frames_dict.get(camera_type)

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
    Пример: /video_feed/front, /video_feed/back, /video_feed/left, /video_feed/right
    """
    return Response(gen_frames(camera_type),
                    mimetype="multipart/x-mixed-replace; boundary=frame")


# --- Начало записи видео ---
@camera_bp.route("/api/start_recording", methods=["POST"])
def start_recording():
    if video_writers:
        return jsonify({"error": "Запись уже идет для одной или нескольких камер"}), 400

    frames = get_camera_frames()
    if not frames:
        return jsonify({"error": "Не удалось получить кадры с камер"}), 400

    for camera_type, frame in frames.items():
        height, width, _ = frame.shape
        video_path = os.path.join(VIDEO_DIR, f"{camera_type}_{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}.mp4")
        fourcc = cv2.VideoWriter.fourcc('m','p','4','v')
        fps = 20

        video_writer = cv2.VideoWriter(video_path, fourcc, fps, (width, height), True)
        video_writers[camera_type] = video_writer

        def record(camera_type, video_writer):
            while camera_type in video_writers:
                frames = get_camera_frames()
                frame = frames.get(camera_type)
                if frame is not None:
                    video_writer.write(frame)
                else:
                    break
                time.sleep(1 / fps)

            video_writer.release()
            del video_writers[camera_type]

        thread = threading.Thread(target=record, args=(camera_type, video_writer))
        thread.start()
        recording_threads[camera_type] = thread

    return jsonify({"message": "Запись всех камер начата"})


# --- Остановка записи всех камер ---
@camera_bp.route("/api/stop_recording", methods=["POST"])
def stop_recording():
    if not video_writers:
        return jsonify({"error": "Запись не была запущена"}), 400

    for camera_type, video_writer in list(video_writers.items()):
        if camera_type in recording_threads:
            recording_threads[camera_type].join()
            del recording_threads[camera_type]

        if video_writer:
            video_writer.release()
            del video_writers[camera_type]

    return jsonify({"message": "Запись всех камер остановлена"})