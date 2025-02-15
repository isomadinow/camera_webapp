## 📖 **Документация: Установка и запуск Camera WebApp как службы (systemd)**

Этот документ описывает:
1. **Как запустить Flask-приложение Camera WebApp как службу (`systemd`)**
2. **Как управлять сервисом (запуск, остановка, проверка, удаление)**
3. **Как заново создать службу, если удалил её**

---

## ✅ **1. Подготовка системы**
Перед тем как запускать приложение, **убедитесь**, что у вас:
- **Установлен Python 3** (`python3 --version`)
- **Установлены зависимости** (Flask и другие библиотеки)

### Установка зависимостей:
```sh
cd /home/isomadinovakh/src/camera_webapp
pip3 install -r requirements.txt
```
🔥 Если `requirements.txt` нет, установите Flask вручную:
```sh
pip3 install flask
```

---

## ✅ **2. Создание systemd-сервиса**
📌 Если служба была удалена или её нет, создайте её заново:

Открываем файл конфигурации службы:
```sh
sudo nano /etc/systemd/system/camera_webapp.service
```

Вставляем следующее:
```ini
[Unit]
Description=Flask-приложение Camera WebApp
After=network.target

[Service]
User=isomadinovakh
Group=isomadinovakh
WorkingDirectory=/home/isomadinovakh/src/camera_webapp
ExecStart=/usr/bin/python3 /home/isomadinovakh/src/camera_webapp/run.py
Restart=always
Environment=PYTHONUNBUFFERED=1

[Install]
WantedBy=multi-user.target
```
**📌 ВАЖНО!**  
Убедитесь, что `WorkingDirectory` и `ExecStart` указывают на **реальное местоположение кода**.

Сохраняем файл (`Ctrl + X`, затем `Y`, затем `Enter`).

---

## ✅ **3. Перезагрузка systemd и запуск службы**
После сохранения **перезагружаем `systemd`**:
```sh
sudo systemctl daemon-reload
```

### 🚀 **Запускаем сервис**:
```sh
sudo systemctl start camera_webapp
```

### 🔍 **Проверяем статус**:
```sh
sudo systemctl status camera_webapp
```
Если всё правильно, **должно быть написано**:
```
Active: active (running)
```

---

## ✅ **4. Автозапуск при загрузке**
Чтобы Flask-приложение **запускалось автоматически при старте системы**, включаем автозапуск:
```sh
sudo systemctl enable camera_webapp
```

---

## ✅ **5. Управление сервисом**
📌 Команды для управления `systemd`-службой:

| Действие            | Команда |
|---------------------|--------|
| **Запустить**       | `sudo systemctl start camera_webapp` |
| **Остановить**      | `sudo systemctl stop camera_webapp` |
| **Перезапустить**   | `sudo systemctl restart camera_webapp` |
| **Проверить статус**| `sudo systemctl status camera_webapp` |
| **Отключить автозапуск** | `sudo systemctl disable camera_webapp` |

---

## ✅ **6. Логирование и отладка**
Если сервис не запускается, можно проверить **логи**:
```sh
journalctl -u camera_webapp --no-pager --lines=50
```
Если приложение падает из-за ошибки в коде, попробуйте запустить его вручную:
```sh
cd /home/isomadinovakh/src/camera_webapp
python3 run.py
```
И посмотрите, что пишет в консоли.

---

## ✅ **7. Удаление службы**
Если нужно удалить службу:
```sh
sudo systemctl stop camera_webapp
sudo systemctl disable camera_webapp
sudo rm /etc/systemd/system/camera_webapp.service
sudo systemctl daemon-reload
```

🔥 Теперь система больше не будет запускать Flask-приложение.

---

## ✅ **8. Как создать службу, если удалил её**
Если служба была удалена, просто повторите **Шаг 2**:
1. **Создайте файл** `/etc/systemd/system/camera_webapp.service`
2. **Добавьте конфигурацию (см. выше)**
3. **Перезагрузите systemd**:
   ```sh
   sudo systemctl daemon-reload
   ```
4. **Запустите сервис**:
   ```sh
   sudo systemctl start camera_webapp
   ```
5. **Включите автозапуск** (если нужно):
   ```sh
   sudo systemctl enable camera_webapp
   ```

---
