from flask import Flask

# Функция для создания и конфигурации приложения Flask
def create_app():
    app = Flask(__name__, template_folder='views/')  # Указываем папку для HTML-шаблонов

    # Регистрация Blueprint (маршруты контроллера камеры)
    from .controllers.camera_controller import camera_bp
    app.register_blueprint(camera_bp)

    return app  # Возвращаем приложение
