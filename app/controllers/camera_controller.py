from flask import Blueprint, jsonify
from app.services.camera_service import start_cameras_from_reports, stop_all_cameras

camera_bp = Blueprint("camera", __name__)

@camera_bp.route("/api/cameras/start", methods=["POST"])
def start_cameras():
    """Запускает камеры на основе reports"""
    result = start_cameras_from_reports()
    return jsonify(result), 200

@camera_bp.route("/api/cameras/stop", methods=["POST"])
def stop_cameras():
    """Останавливает все камеры"""
    stop_all_cameras()
    return jsonify({"message": "Камеры остановлены"}), 200
