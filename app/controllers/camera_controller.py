from flask import Blueprint, jsonify, request
from app.services.camera_service import start_cameras_for_truck, stop_all_cameras, active_cameras

camera_bp = Blueprint("camera", __name__)

@camera_bp.route("/api/start_cameras", methods=["POST"])
def start_cameras():
    """Запускает камеры для выбранного грузовика."""
    data = request.json
    truck_number = data.get("truck_number")

    if not truck_number:
        return jsonify({"error": "Не указан номер грузовика"}), 400

    result = start_cameras_for_truck(truck_number)
    return jsonify(result)

@camera_bp.route("/api/stop_cameras", methods=["POST"])
def stop_cameras():
    """Останавливает все камеры."""
    stop_all_cameras()
    return jsonify({"message": "Все камеры остановлены"})

@camera_bp.route("/api/start_recording", methods=["POST"])
def start_recording():
    """Запускает запись видео с выбранной камеры."""
    data = request.json
    camera_type = data.get("camera_type")  # front, back, left, right
    output_path = data.get("output_path")  # путь к файлу
    duration_seconds = data.get("duration_seconds", 60)  # по умолчанию 60 секунд

    if not camera_type or camera_type not in active_cameras:
        return jsonify({"error": "Камера не найдена или не указана"}), 400

    if not output_path:
        return jsonify({"error": "Не указан путь для записи"}), 400

    active_cameras[camera_type].start_recording(output_path, duration_seconds)
    return jsonify({"message": f"Запись с камеры {camera_type} начата"})

@camera_bp.route("/api/stop_recording", methods=["POST"])
def stop_recording():
    """Останавливает запись видео с выбранной камеры."""
    data = request.json
    camera_type = data.get("camera_type")

    if not camera_type or camera_type not in active_cameras:
        return jsonify({"error": "Камера не найдена или не указана"}), 400

    active_cameras[camera_type].stop_recording()
    return jsonify({"message": f"Запись с камеры {camera_type} остановлена"})
