document.addEventListener("DOMContentLoaded", () => {
    // Événement bouton Ajouter
    const addBtn = document.getElementById("addEmployeeBtn");
    addBtn.addEventListener("click", addEmployee);

    const tableBody = document.querySelector("tbody");
    tableBody.addEventListener("click", (event) => {
        const target = event.target;
        // Modifier ou Supprimer
        if (target.classList.contains("edit-btn")) editEmployee(event);
        else if (target.classList.contains("delete-btn")) deleteEmployee(event);
    });
});

function editEmployee(event) {
    const button = event.target;
    const id = button.getAttribute("data-id");
    const name = button.getAttribute("data-nom");
    const surname = button.getAttribute("data-prenom");

    // Remplir modal
    document.getElementById("employee-id").value = id;
    document.getElementById("employee-nom").value = name;
    document.getElementById("employee-prenom").value = surname;

    const modal = new bootstrap.Modal(document.getElementById("editEmployeeModal"));
    modal.show();

    const form = document.getElementById("editEmployeeForm");
    form.onsubmit = (e) => {
        e.preventDefault();

        const formData = new FormData(form);
        fetch(`/modifier_employe/`, {
            method: "POST",
            body: formData,
            headers: { "X-CSRFToken": document.querySelector("[name=csrfmiddlewaretoken]").value }
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                alert(data.message);

                // Mettre à jour les données du bouton
                button.setAttribute("data-nom", formData.get("nom"));
                button.setAttribute("data-prenom", formData.get("prenom"));
                const row = button.closest("tr");
                row.children[0].textContent = formData.get("nom");
                row.children[1].textContent = formData.get("prenom");

                modal.hide();
            } else alert(data.message);
        });
    };
}

function deleteEmployee(event) {
    const button = event.target;
    const id = button.getAttribute("data-id");

    const modal = new bootstrap.Modal(document.getElementById("deleteEmployeeModal"));
    modal.show();

    const confirmDelete = document.getElementById("confirmDeleteBtn");
    confirmDelete.onclick = () => {
        fetch(`/delete-employe/${id}/`, {
            method: "DELETE",
            headers: { "X-CSRFToken": document.querySelector("[name=csrfmiddlewaretoken]").value }
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                alert(data.message);
                // Supprimer la ligne
                const row = button.closest("tr");
                row.remove();
                modal.hide();
            } else alert(data.message);
        });
    };
}

function addEmployee() {
    const modalAdd = new bootstrap.Modal(document.getElementById("addEmployeeModal"));
    modalAdd.show();

    const formAdd = document.getElementById("addEmployeeForm");
    formAdd.addEventListener("submit", (event) => {
        event.preventDefault();

        const formData = new FormData(formAdd);
        fetch("/add-employe/", {
            method: "POST",
            body: formData,
            headers: { "X-CSRFToken": document.querySelector("[name=csrfmiddlewaretoken]").value }
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                alert(data.message);

                // Ajouter ligne au tableau
                const tableBody = document.querySelector("tbody");
                const newRow = document.createElement("tr");
                newRow.innerHTML = `
                    <td>${data.nom}</td>
                    <td>${data.prenom}</td>
                    <td>
                        <button class="btn btn-primary edit-btn" data-id="${data.id}" data-nom="${data.nom}" data-prenom="${data.prenom}">
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
                modalAdd.hide();

        } else alert(data.message);

        });
    });
}