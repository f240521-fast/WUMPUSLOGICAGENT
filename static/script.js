function generateGrid() {
    const rows = document.getElementById("rows").value;
    const cols = document.getElementById("cols").value;

    fetch("/generate", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ rows, cols })
    })
    .then(response => response.json())
    .then(data => {
        renderGrid(data.grid);
        updateDashboard(data);
    });
}

function moveAgent() {
    fetch("/move", {
        method: "POST"
    })
    .then(response => response.json())
    .then(data => {
        renderGrid(data.grid);
        updateDashboard(data);
    });
}

function renderGrid(grid) {
    const gridDiv = document.getElementById("grid");

    gridDiv.innerHTML = "";
    gridDiv.style.gridTemplateColumns = `repeat(${grid[0].length}, 50px)`;

    grid.forEach(row => {
        row.forEach(cell => {
            const div = document.createElement("div");
            div.classList.add("cell");

            if (cell === "A") {
                div.classList.add("agent");
                div.innerText = "A";
            } else if (cell === "S") {
                div.classList.add("safe");
            } else {
                div.classList.add("unknown");
            }

            gridDiv.appendChild(div);
        });
    });
}

function updateDashboard(data) {
    document.getElementById("percepts").innerText =
        data.percepts.length > 0 ? data.percepts.join(", ") : "None";

    document.getElementById("steps").innerText = data.steps;
}
