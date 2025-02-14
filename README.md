# Документация проекта

## Описание
Веб-приложение на Flask для отображения 4 видеопотоков с одной камеры. Использует OpenCV для работы с камерой и MVC-архитектуру для структурированного кода.

---

## Архитектура проекта

```
project/
│
├── app/                # Основной код приложения
│   ├── __init__.py     # Инициализация Flask-приложения
│   ├── controllers/    # Логика маршрутов
│   │   ├── __init__.py
│   │   └── camera_controller.py
│   ├── models/         # Логика работы с камерой
│   │   ├── __init__.py
│   │   └── camera_model.py
│   ├── views/          # HTML-шаблоны
│   │   ├── __init__.py
│   │   └── index.html
│   ├── static/         # Каталог для статических файлов
│   │   ├── css/
│   │   │   └── styles.css  # Стили
│   │   └── js/             # Скрипты
│
├── run.py              # Точка входа приложения
├── requirements.txt    # Зависимости
└── README.md           # Документация

```
---

## Установка

1. Убедитесь, что установлен Python 3.9+.
2. Клонируйте проект:
   ```bash
   git clone https://github.com/isomadinow/camera_webapp
   cd project
   ```
3. Установите зависимости:
   ```bash
   pip install -r requirements.txt
   ```
4. Запустите приложение:
   ```bash
   python run.py
   ```

---

## Использование

1. Откройте в браузере:
   ```
   http://127.0.0.1:5000
   ```

2. Основные маршруты:
   - `/`: Главная страница с видеопотоками.
   - `/video_feed/<camera_index>`: Видеопоток в формате MJPEG. (ну типа если отдельно нужно)

---

## Возможные ошибки

- **Камера не работает**:
  - Проверьте подключение камеры.
  - Измените индекс камеры в `camera_model.py`:
    ```python
    CameraModel(0)  # Используйте другой индекс, например, 1
    ```
- **CSS не загружается**:
  - Убедитесь, что файл `static/css/styles.css` существует.
  - Проверьте, что путь в `index.html` выглядит так:
    ```html
    <link rel="stylesheet" href="/static/css/styles.css">
    ```

---

