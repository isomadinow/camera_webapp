from flask import Flask
from app.model.camera_manager import CameraManager
from app.controller.camera import bp as camera_bp

def create_app():
    app = Flask(__name__)

    # Инициализация камер
    CameraManager.initialize([0, 1, 2, 3])  # Добавьте индексы камер

    # Регистрируем маршруты
    app.register_blueprint(camera_bp)

    return app
