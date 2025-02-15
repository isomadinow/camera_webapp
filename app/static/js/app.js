document.addEventListener("DOMContentLoaded", function () {
    // 1. Находим элементы
    const loadTrucksButton = document.getElementById("loadTrucks");
    const truckSelect = document.getElementById("truckSelect");
    const startButton = document.getElementById("startCameras");
    const stopButton = document.getElementById("stopCameras");
    const startRecordingButton = document.getElementById("startRecording");
    const stopRecordingButton = document.getElementById("stopRecording");

    const cameraStream = document.getElementById("cameraStream");
    const frontCamera = document.getElementById("frontCamera");
    const backCamera = document.getElementById("backCamera");
    const leftCamera = document.getElementById("leftCamera");
    const rightCamera = document.getElementById("rightCamera");

    const reportTableBody = document.getElementById("reportTableBody");

    // 2. Функция загрузки списка грузовиков
    function loadTrucks() {
        fetch("/api/trucks")
            .then(response => response.json())
            .then(data => {
                truckSelect.innerHTML = '<option value="">Выберите грузовик...</option>';
                data.forEach(truck => {
                    let option = document.createElement("option");
                    option.value = truck.stateNumber;
                    option.textContent = `${truck.name} (${truck.stateNumber})`;
                    truckSelect.appendChild(option);
                });
                alert("Список грузовиков загружен!");
            })
            .catch(error => {
                console.error("Ошибка загрузки списка грузовиков:", error);
                alert("Ошибка загрузки списка!");
            });
    }

    // 3. Функция запуска камер
    function startCameras() {
        const selectedTruck = truckSelect.value;
        if (!selectedTruck) {
            alert("Выберите грузовик!");
            return;
        }

        fetch("/api/start_cameras", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ truck_number: selectedTruck })
        })
        .then(response => response.json())
        .then(data => {
            if (data.message) {
                alert(data.message);

                // Если хотите убрать ?truck=..., меняйте на /video_feed/front
                frontCamera.src = `/video_feed/front?truck=${selectedTruck}`;
                backCamera.src  = `/video_feed/back?truck=${selectedTruck}`;
                leftCamera.src  = `/video_feed/left?truck=${selectedTruck}`;
                rightCamera.src = `/video_feed/right?truck=${selectedTruck}`;

                cameraStream.classList.remove("d-none");
            } else {
                alert(data.error);
            }
        })
        .catch(error => {
            console.error("Ошибка запуска камер:", error);
            alert("Ошибка запуска камер!");
        });
    }

    // 4. Функция остановки камер
    function stopCameras() {
        fetch("/api/stop_cameras", { method: "POST" })
        .then(response => response.json())
        .then(data => {
            alert(data.message);
            // Очищаем src
            frontCamera.src = "";
            backCamera.src  = "";
            leftCamera.src  = "";
            rightCamera.src = "";
            cameraStream.classList.add("d-none");
        })
        .catch(error => {
            console.error("Ошибка остановки камер:", error);
            alert("Ошибка остановки камер!");
        });
    }

    // 5. Запись видео (пример)
    function startRecording() {
        const cameraType = prompt("Камера (front, back, left, right):");
        const outputPath = prompt("Путь для записи (например, output.avi):");
        const duration = parseInt(prompt("Длительность записи (секунд):", "60"), 10);

        if (!cameraType || !outputPath) {
            alert("Необходимо указать камеру и путь для записи!");
            return;
        }

        fetch("/api/record", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                camera_type: cameraType,
                action: "start",
                output_path: outputPath,
                duration_seconds: duration || 60
            })
        })
        .then(response => response.json())
        .then(data => alert(data.message))
        .catch(error => {
            console.error("Ошибка запуска записи:", error);
            alert("Ошибка запуска записи!");
        });
    }

    function stopRecording() {
        const cameraType = prompt("Введите камеру для остановки записи (front, back, left, right):");
        if (!cameraType) {
            alert("Необходимо указать камеру!");
            return;
        }

        fetch("/api/record", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                camera_type: cameraType,
                action: "stop"
            })
        })
        .then(response => response.json())
        .then(data => alert(data.message))
        .catch(error => {
            console.error("Ошибка остановки записи:", error);
            alert("Ошибка остановки записи!");
        });
    }

    // 6. Привязываем события к кнопкам
    loadTrucksButton.addEventListener("click", loadTrucks);
    startButton.addEventListener("click", startCameras);
    stopButton.addEventListener("click", stopCameras);
    startRecordingButton.addEventListener("click", startRecording);
    stopRecordingButton.addEventListener("click", stopRecording);

    // 7. (Опционально) Загрузить отчёт, если нужно
    fetch("/api/reports/trucks_with_cameras")
        .then(response => {
            if (!response.ok) {
                throw new Error(`Ошибка сервера: ${response.status}`);
            }
            return response.json();
        })
        .then(data => {
            console.log("Полученные данные:", data);
            reportTableBody.innerHTML = ""; // Очищаем таблицу

            if (!Array.isArray(data) || data.length === 0) {
                reportTableBody.innerHTML = "<tr><td colspan='6'>Нет данных</td></tr>";
                return;
            }

            data.forEach(truck => {
                let row = document.createElement("tr");
                truck.forEach(value => {
                    let cell = document.createElement("td");
                    cell.textContent = value;
                    row.appendChild(cell);
                });
                reportTableBody.appendChild(row);
            });
        })
        .catch(error => {
            console.error("Ошибка при загрузке данных:", error);
            reportTableBody.innerHTML =
                `<tr><td colspan="6">Ошибка загрузки данных</td></tr>`;
        });
});
