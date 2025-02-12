document.addEventListener("DOMContentLoaded", function () {
    const loadTrucksButton = document.getElementById("loadTrucks");
    const truckSelect = document.getElementById("truckSelect");
    const startButton = document.getElementById("startCameras");
    const stopButton = document.getElementById("stopCameras");

    const startRecordingButton = document.getElementById("startRecording");
    const stopRecordingButton = document.getElementById("stopRecording");

    const frontCamera = document.getElementById("frontCamera");
    const backCamera = document.getElementById("backCamera");
    const leftCamera = document.getElementById("leftCamera");
    const rightCamera = document.getElementById("rightCamera");

    const cameraStream = document.getElementById("cameraStream");

    // Функция загрузки списка грузовиков
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

    // Функция запуска камер
    // Функция запуска камер
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

                // Подключение видеопотока к элементам <video>
                frontCamera.src = `/video_feed/front?truck=${selectedTruck}`;
                backCamera.src = `/video_feed/back?truck=${selectedTruck}`;
                leftCamera.src = `/video_feed/left?truck=${selectedTruck}`;
                rightCamera.src = `/video_feed/right?truck=${selectedTruck}`;

                cameraStream.classList.remove("d-none"); // Показываем блок с камерами
            } else {
                alert(data.error);
            }
        })
        .catch(error => {
            console.error("Ошибка запуска камер:", error);
            alert("Ошибка запуска камер!");
        });
    }


    // Функция остановки камер
    function stopCameras() {
        fetch("/api/stop_cameras", { method: "POST" })
        .then(response => response.json())
        .then(data => {
            alert(data.message);
            frontCamera.src = "";
            backCamera.src = "";
            leftCamera.src = "";
            rightCamera.src = "";

            cameraStream.classList.add("d-none");
        })
        .catch(error => {
            console.error("Ошибка остановки камер:", error);
            alert("Ошибка остановки камер!");
        });
    }

    // Функция запуска записи видео
    function startRecording() {
        const cameraType = prompt("Введите камеру для записи (front, back, left, right):");
        const outputPath = prompt("Введите путь для сохранения (например, output.avi):");
        const duration = parseInt(prompt("Введите длительность записи в секундах:", "60"), 10);

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

    // Функция остановки записи видео
    function stopRecording() {
        const cameraType = prompt("Введите камеру для остановки записи (front, back, left, right):");

        if (!cameraType) {
            alert("Необходимо указать камеру для остановки записи!");
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

    loadTrucksButton.addEventListener("click", loadTrucks);
    startButton.addEventListener("click", startCameras);
    stopButton.addEventListener("click", stopCameras);
    startRecordingButton.addEventListener("click", startRecording);
    stopRecordingButton.addEventListener("click", stopRecording);
});
