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
