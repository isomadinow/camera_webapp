# app/controllers/camera_controller.py
from flask import Blueprint, jsonify, request, Response
from app.services.camera_service import (
    start_cameras_for_truck,
    stop_all_cameras,
    get_camera_frames
)
import cv2
import time

camera_bp = Blueprint("camera", __name__)

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
