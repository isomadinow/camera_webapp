from flask import Flask
from app.models.database import init_db
from config import Config
# Функция для создания и конфигурации приложения Flask
def create_app():
    app = Flask(__name__, template_folder='views/')  # Указываем папку для HTML-шаблонов

    app.config.from_object(Config)
    # Инициализация БД
    init_db(app)
    # Регистрация Blueprint (маршруты контроллера камеры)
    from .controllers.camera_controller import camera_bp
    app.register_blueprint(camera_bp)

    return app  # Возвращаем приложение
