const hiddenInput = document.getElementById("pinInput");
const cells = document.querySelectorAll(".pin-cell");
const keys = document.querySelectorAll(".key");

function syncCells() {
    const val = hiddenInput.value;
    cells.forEach((cell, i) => {
        cell.textContent = val[i] || "";
        cell.classList.toggle("filled", Boolean(val[i]));
    });
}

keys.forEach((key) => {
    key.addEventListener("click", () => {
        const action = key.dataset.action;

        if (action === "clear") {
            hiddenInput.value = "";
        } else if (action === "del") {
            hiddenInput.value = hiddenInput.value.slice(0, -1);
        } else if (hiddenInput.value.length < 4) {
            hiddenInput.value += key.dataset.digit;
        }

        syncCells();
        hiddenInput.focus();
    });
});

hiddenInput.addEventListener("input", () => {
    hiddenInput.value = hiddenInput.value.replace(/\D/g, "").slice(0, 4);
    syncCells();
});

document.getElementById("pinForm").addEventListener("submit", (e) => {
    if (hiddenInput.value.length !== 4) {
        // let the server render the validation message
        return;
    }
});

hiddenInput.focus();
syncCells();