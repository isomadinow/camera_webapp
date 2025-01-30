from flask import Blueprint, jsonify, request
from app.models.truck_model import TruckModel
from app.models.database import db

truck_bp = Blueprint("truck", __name__)

# Получить все грузовики
@truck_bp.route("/api/trucks", methods=["GET"])
def get_all_trucks():
    trucks = TruckModel.get_all()
    return jsonify([
        {"id": truck.id, "name": truck.name, "stateNumber": truck.stateNumber}
        for truck in trucks
    ])

# Получить грузовик по ID
@truck_bp.route("/api/trucks/<int:truck_id>", methods=["GET"])
def get_truck(truck_id):
    truck = TruckModel.get_by_id(truck_id)
    if not truck:
        return jsonify({"error": "Грузовик не найден"}), 404
    return jsonify({"id": truck.id, "name": truck.name, "stateNumber": truck.stateNumber})

# Добавить новый грузовик
@truck_bp.route("/api/trucks", methods=["POST"])
def add_truck():
    data = request.json
    if not data.get("name") or not data.get("stateNumber"):
        return jsonify({"error": "name и stateNumber обязательны"}), 400

    truck = TruckModel(Name=data["name"], StateNumber=data["stateNumber"])
    db.session.add(truck)
    db.session.commit()
    
    return jsonify({"message": "Грузовик добавлен", "id": truck.id}), 201
