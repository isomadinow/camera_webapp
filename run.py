
import sys
import os
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
opencv_path = os.path.join(BASE_DIR, "opencv/build/lib/python3")
sys.path.insert(0, opencv_path)

import cv2


from app import create_app  # Импортируем функцию создания приложения
import cv2
app = create_app()  # Создаём экземпляр Flask-приложения

# Запуск приложения
if __name__ == '__main__':
    print(cv2.getBuildInformation())
    app.run(host='0.0.0.0', port=5000)  # Запускаем сервер на порту 5000