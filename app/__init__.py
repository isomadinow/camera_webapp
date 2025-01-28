from flask import Flask

def create_app():
    app = Flask(__name__, template_folder='views/')  

    # Регистрация Blueprint для контроллеров
    from .controllers.camera_controller import camera_bp
    app.register_blueprint(camera_bp)

    return app
