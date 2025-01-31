from flask import Blueprint, jsonify
from app.services.report_service import get_trucks_with_cameras

report_bp = Blueprint("report", __name__)

@report_bp.route("/api/reports/trucks_with_cameras", methods=["GET"])
def get_report():
    data = get_trucks_with_cameras()
    return jsonify([data]), 200
