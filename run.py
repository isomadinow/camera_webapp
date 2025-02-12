from app import create_app  # Импортируем функцию создания приложения
import cv2
app = create_app()  # Создаём экземпляр Flask-приложения

# Запуск приложения
if __name__ == '__main__':
    print(cv2.getBuildInformation())
    app.run(host='0.0.0.0', port=5000)  # Запускаем сервер на порту 5000