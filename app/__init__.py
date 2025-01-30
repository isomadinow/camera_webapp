import os
from flask import Flask
from app.models.database import db
from config import Config
from app.controllers.camera_controller import camera_bp
from app.controllers.truck_controller import truck_bp
from app.controllers.report_controller import report_bp
from app.controllers.view_controller import view_bp

# Функция для создания и конфигурации приложения Flask
def create_app():
    app = Flask(__name__, template_folder='views/')  # Указываем папку для HTML-шаблонов
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL", "postgresql://csd_server:csd_server@172.20.76.82:5432/DispatcherXDb_test2")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    # Инициализация БД
    db.init_app(app)
    # Регистрация Blueprint (маршруты контроллера камеры)
    app.register_blueprint(camera_bp)
    app.register_blueprint(truck_bp)
    app.register_blueprint(report_bp)
    app.register_blueprint(view_bp)

    return app  # Возвращаем приложение
