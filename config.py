import os

class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "postgresql://csd_server:csd_server@172.20.76.82:5432/DispatcherXDb_test2")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
