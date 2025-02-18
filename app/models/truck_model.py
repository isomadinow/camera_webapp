from app.models.database import db

# Класс для работы с грузовиками
class TruckModel(db.Model):
    __tablename__ = "BaseTransport"  # Указываем явное имя таблицы
    Id = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String(255), nullable=False)  # Название грузовика
    StateNumber = db.Column(db.String(50), nullable=False, unique=True)  # Госномер
    TypeTransport = db.Column(db.Integer, nullable = False)

    def __init__(self, Name, StateNumber):
        self.Name = Name
        self.StateNumber = StateNumber

    # Метод для получения всех грузовиков из БД
    @staticmethod
    def get_all():
        return db.session.query(TruckModel).filter_by(TypeTransport=1).all()

    # Метод для поиска грузовика по ID
    @staticmethod
    def get_by_id(truck_id):
        return db.session.query(TruckModel).filter_by(Id=truck_id, TypeTransport=1).first()

    # Метод для поиска грузовика по госномеру
    @staticmethod
    def get_by_state_number(state_number):
        return db.session.query(TruckModel).filter_by(StateNumber=state_number, TypeTransport=1).first()
