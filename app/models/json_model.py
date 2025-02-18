import json
import os

# Получаем путь к папке 'app', так как 'static' находится внутри нее
APP_DIR = os.path.dirname(os.path.dirname(__file__))  # Поднимаемся на один уровень выше (в папку 'app')
STATIC_DIR = os.path.join(APP_DIR, 'static')  # Папка 'static' внутри 'app'
JSON_FILE = os.path.join(STATIC_DIR, 'ports.json')  # Путь к файлу 'ports.json' в папке 'static'


def json_read_data():
    with open(JSON_FILE, "r", encoding="utf-8") as file:
        data = json.load(file)
    return data