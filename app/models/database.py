from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def init_db(app):
    """ Инициализация базы данных """
    db.init_app(app)
    with app.app_context():
        db.create_all()