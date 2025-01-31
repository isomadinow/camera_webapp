from flask import Blueprint, jsonify, request
from app.services.camera_service import start_cameras_for_truck, stop_all_cameras

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
