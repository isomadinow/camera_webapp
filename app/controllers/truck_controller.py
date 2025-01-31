from flask import Blueprint, jsonify, request
from app.models.truck_model import TruckModel
from app.models.database import db

truck_bp = Blueprint("truck", __name__)

# Получить все грузовики
@truck_bp.route("/api/trucks", methods=["GET"])
def get_all_trucks():
    trucks = TruckModel.get_all()
    return jsonify([
        {"id": truck.Id, "name": truck.Name, "stateNumber": truck.StateNumber}
        for truck in trucks
    ])

# Получить грузовик по ID
@truck_bp.route("/api/trucks/<int:truck_id>", methods=["GET"])
def get_truck(truck_id):
    truck = TruckModel.get_by_id(truck_id)
    if not truck:
        return jsonify({"error": "Грузовик не найден"}), 404
    return jsonify({"id": truck.Id, "name": truck.Name, "stateNumber": truck.StateNumber})

