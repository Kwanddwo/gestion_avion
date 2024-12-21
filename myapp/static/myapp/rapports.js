document.addEventListener("DOMContentLoaded", () => {
    // Event listener for "Add Report" button
    const addBtn = document.getElementById("addReportBtn");
    addBtn.addEventListener("click", addReport);

    const tableBody = document.querySelector("tbody");
    tableBody.addEventListener("click", (event) => {
        const target = event.target;
        // Edit or Delete
        if (target.classList.contains("edit-btn")) editReport(event);
        else if (target.classList.contains("delete-btn")) deleteReport(event);
    });
});

function editReport(event) {
    const button = event.target;
    const id = button.getAttribute("data-id");
    const avionId = button.getAttribute("data-avion");
    const texte = button.getAttribute("data-texte");
    const heures_vol = button.getAttribute("data-heures_vol");

    // Fill the modal with data
    document.getElementById("report-id").value = id;
    document.getElementById("report-texte").value = texte;
    document.getElementById("report-heures_vol").value = heures_vol;
    document.getElementById("report-avion").value = avionId; // Set the avion ID in the modal

    const modal = new bootstrap.Modal(document.getElementById("editReportModal"));
    modal.show();

    const form = document.getElementById("editReportForm");
    form.onsubmit = (e) => {
        e.preventDefault();

        const formData = new FormData(form);
        fetch(`/modifier_rapport/`, {
            method: "POST",
            body: formData,
            headers: { "X-CSRFToken": document.querySelector("[name=csrfmiddlewaretoken]").value }
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                alert(data.message);

                // Update button data
                button.setAttribute("data-texte", formData.get("texte"));
                button.setAttribute("data-heures_vol", formData.get("heures_vol"));
                button.setAttribute("data-avion", formData.get("avion"));
                
                const row = button.closest("tr");
                row.children[0].textContent = formData.get("avion");  // Update avion type
                row.children[1].textContent = formData.get("texte");
                row.children[2].textContent = formData.get("heures_vol");

                modal.hide();
            } else alert(data.message);
        });
    };
}

function deleteReport(event) {
    const button = event.target;
    const id = button.getAttribute("data-id");

    const modal = new bootstrap.Modal(document.getElementById("deleteReportModal"));
    modal.show();

    const confirmDelete = document.getElementById("confirmDeleteBtn");
    confirmDelete.onclick = () => {
        fetch(`/delete-rapport/${id}/`, {
            method: "DELETE",
            headers: { "X-CSRFToken": document.querySelector("[name=csrfmiddlewaretoken]").value }
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                alert(data.message);
                // Remove the row
                const row = button.closest("tr");
                row.remove();
                modal.hide();
            } else alert(data.message);
        });
    };
}

function addReport() {
    const modalAdd = new bootstrap.Modal(document.getElementById("addReportModal"));
    modalAdd.show();

    const formAdd = document.getElementById("addReportForm");
    const submitButton = formAdd.querySelector("button[type='submit']");

    formAdd.addEventListener("submit", (event) => {
        event.preventDefault();

        // Disable the submit button to prevent multiple submissions
        submitButton.disabled = true;

        const formData = new FormData(formAdd);
        fetch("/add-rapport/", {
            method: "POST",
            body: formData,
            headers: { "X-CSRFToken": document.querySelector("[name=csrfmiddlewaretoken]").value }
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                alert(data.message);

                // Add new row to table
                const tableBody = document.querySelector("tbody");
                const newRow = document.createElement("tr");
                newRow.innerHTML = `
                    <td>${data.avion}</td>
                    <td>${data.texte}</td>
                    <td>${data.heures_vol}</td>
                    <td>${data.date}</td>
                    <td>
                        <button class="btn btn-primary edit-btn" data-id="${data.id}" data-texte="${data.texte}" data-heures_vol="${data.heures_vol}" data-avion="${data.avion_id}">
                            Modifier
                        </button>
                    </td>
                    <td>
                        <button class="btn btn-danger delete-btn" data-id="${data.id}">
                            Supprimer
                        </button>
                    </td>
                `;
                tableBody.appendChild(newRow);

                // Clear the form fields and re-enable the submit button after submission
                formAdd.reset();  // This clears all input fields in the form
                submitButton.disabled = false;  // Re-enable the submit button
                modalAdd.hide();  // Close the modal
            } else {
                alert(data.message);
                submitButton.disabled = false;  // Re-enable button in case of error
            }
        })
        .catch(error => {
            console.error("Error:", error);
            alert("Une erreur est survenue.");
            submitButton.disabled = false;  // Re-enable button if error happens
        });
    });
}

