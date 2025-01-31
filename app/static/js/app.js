document.addEventListener("DOMContentLoaded", function () {
    fetch("/api/reports/trucks_with_cameras")
        .then(response => {
            if (!response.ok) {
                throw new Error(`Ошибка сервера: ${response.status}`);
            }
            return response.json();
        })
        .then(data => {
            console.log("Полученные данные:", data); // Лог в консоль

            const tableBody = document.querySelector("#reportTableBody");
            tableBody.innerHTML = ""; // Очищаем таблицу перед обновлением

            if (!Array.isArray(data) || data.length === 0) {
                tableBody.innerHTML = "<tr><td colspan='6'>Нет данных</td></tr>";
                return;
            }

            data.forEach(truck => {
                let row = document.createElement("tr");

                truck.forEach(value => {
                    let cell = document.createElement("td");
                    cell.textContent = value;
                    row.appendChild(cell);
                });

                tableBody.appendChild(row);
            });
        })
        .catch(error => {
            console.error("Ошибка при загрузке данных:", error);
            document.querySelector("#reportTableBody").innerHTML = 
                `<tr><td colspan="6">Ошибка загрузки данных</td></tr>`;
        });
});

document.addEventListener("DOMContentLoaded", function () {
    const loadTrucksButton = document.getElementById("loadTrucks");
    const truckSelect = document.getElementById("truckSelect");

    // Функция для загрузки списка грузовиков
    function loadTrucks() {
        fetch("/api/trucks")
            .then(response => response.json())
            .then(data => {
                truckSelect.innerHTML = '<option value="">Выберите грузовик...</option>'; // Очищаем список

                data.forEach(truck => {
                    let option = document.createElement("option");
                    option.value = truck.stateNumber; // Госномер как value
                    option.textContent = `${truck.name} (${truck.stateNumber})`; // Название + госномер
                    truckSelect.appendChild(option);
                });

                alert("Список грузовиков загружен!");
            })
            .catch(error => {
                console.error("Ошибка загрузки списка грузовиков:", error);
                alert("Ошибка загрузки списка!");
            });
    }

    // Привязываем кнопку к функции загрузки
    loadTrucksButton.addEventListener("click", loadTrucks);
});

document.addEventListener("DOMContentLoaded", function () {
    const loadTrucksButton = document.getElementById("loadTrucks");
    const truckSelect = document.getElementById("truckSelect");
    const startButton = document.getElementById("startCameras");
    const stopButton = document.getElementById("stopCameras");
    const cameraStream = document.getElementById("cameraStream");

    const frontCamera = document.getElementById("frontCamera");
    const backCamera = document.getElementById("backCamera");
    const leftCamera = document.getElementById("leftCamera");
    const rightCamera = document.getElementById("rightCamera");

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

                // Подставляем ссылки на видеопоток, привязанные к выбранному грузовику
                frontCamera.src = `/video_feed/front?truck=${selectedTruck}`;
                backCamera.src = `/video_feed/back?truck=${selectedTruck}`;
                leftCamera.src = `/video_feed/left?truck=${selectedTruck}`;
                rightCamera.src = `/video_feed/right?truck=${selectedTruck}`;

                cameraStream.classList.remove("d-none"); // Показываем видеопотоки
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

            cameraStream.classList.add("d-none"); // Скрываем видеопотоки
        })
        .catch(error => {
            console.error("Ошибка остановки камер:", error);
            alert("Ошибка остановки камер!");
        });
    }

    // Привязываем кнопки к функциям
    loadTrucksButton.addEventListener("click", loadTrucks);
    startButton.addEventListener("click", startCameras);
    stopButton.addEventListener("click", stopCameras);
});
