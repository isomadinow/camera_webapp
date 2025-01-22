from flask import Flask
from app.controller.camera import bp as camera_bp

def create_app():
    app = Flask(__name__)
    app.register_blueprint(camera_bp)  # Регистрируем маршруты контроллера
    return app

if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=5000)
