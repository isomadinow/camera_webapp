from app.models.database import db

# Модель камеры (только для работы с БД)
class CameraModel(db.Model):
    __tablename__ = "Cameras"
    
    Id = db.Column(db.Integer, primary_key=True)
    Front = db.Column(db.Integer, nullable=False, default=0)
    Back = db.Column(db.Integer, nullable=False, default=0)
    Left = db.Column(db.Integer, nullable=False, default=0)
    Right = db.Column(db.Integer, nullable=False, default=0)
    TransportId = db.Column(db.Integer, nullable=False, default=0)

    @staticmethod
    def get_all():
        return db.session.query(CameraModel).all()
